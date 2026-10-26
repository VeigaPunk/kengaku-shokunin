#!/usr/bin/env python3
"""R40PlanNext TB2 screen: per task at the pin, offline-executability and quote-supply measures. Read-only on the tb2 checkout."""
import ast, importlib.util, json, pathlib, re, sys
T = pathlib.Path(sys.argv[1])
COVERED = {"protein-assembly","regex-log","configure-git-webserver","build-pmars","git-leak-recovery","db-wal-recovery"}
STD = set(sys.stdlib_module_names)
def quotes(text):
    n = 0
    for l in text.splitlines():
        w = l.split()
        if 3 <= len(w) <= 25: n += 1
    return n
CLASSES = [("db", r"sqlite|\.db\b|sqlite3"), ("repo", r"\bgit\b|git_|\.git"), ("service", r"requests\.|urllib|socket|http://|curl|localhost|:\d{4}"),
  ("build", r"\bgcc\b|\bmake\b|cmake|cargo|compile|\.so\b|ELF"), ("crypto", r"openssl|x509|hashlib|sha256|md5|cipher|hash"),
  ("numeric", r"numpy|scipy|torch|np\.|allclose|tolerance|isclose"), ("image", r"PIL|\.png|\.jpg|cv2|image"),
  ("regex", r"\bre\.(compile|search|findall|match)"), ("subprocess", r"subprocess|os\.system"),
  ("embedded-solver", r"def _?(hard_ok|solve|check|verify|validate)\w*\(")]
rows = []
for d in sorted(p for p in T.iterdir() if p.is_dir() and (p / "tests").is_dir()):
    t = d.name
    to = d / "tests" / "test_outputs.py"
    if not to.is_file(): rows.append(dict(t=t, no_test_outputs=True)); continue
    s = to.read_text(errors="replace"); ins = (d / "instruction.md").read_text(errors="replace") if (d / "instruction.md").is_file() else ""
    sol = (d / "solution" / "solve.sh"); solt = sol.read_text(errors="replace") if sol.is_file() else ""
    env = d / "environment"; efiles = [p for p in env.rglob("*") if p.is_file() and p.name != "Dockerfile"] if env.is_dir() else []
    try:
        tree = ast.parse(s); parse = True
    except SyntaxError: tree = None; parse = False
    imports = set()
    if tree:
        for n in ast.walk(tree):
            if isinstance(n, ast.Import): imports |= {a.name.split(".")[0] for a in n.names}
            elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0: imports.add(n.module.split(".")[0])
    missing = sorted(m for m in imports if m not in STD and importlib.util.find_spec(m) is None)
    ntests = len(re.findall(r"^def test_", s, re.M))
    cls = [c for c, rx in CLASSES if re.search(rx, s)]
    toml = (d / "task.toml").read_text(errors="replace") if (d / "task.toml").is_file() else ""
    rows.append(dict(t=t, covered=t in COVERED, lines=len(s.splitlines()), ntests=ntests, qt=quotes(s), qi=quotes(ins),
        envfiles=len(efiles), envbytes=sum(p.stat().st_size for p in efiles), missing_imports=missing, parse=parse,
        fixtures=bool(re.search(r"@pytest\.(fixture|mark)|def test_\w+\(\w", s)), oracle_net=bool(re.search(r"curl|wget|pip install|apt(-get)? install|git clone|npm |uv (pip|run)|https?://", solt)),
        oracle_lines=len(solt.splitlines()), classes=cls, diff=(re.search(r'difficulty\s*=\s*"(\w+)"', toml) or [0, ""])[1] if toml else "",
        cat=(re.search(r'category\s*=\s*"([^"]+)"', toml) or [0, ""])[1] if toml else "",
        gpu=bool(re.search(r"gpus?\s*=\s*[1-9]", toml)), allow_net=bool(re.search(r"allow_internet\s*=\s*true", toml))))
json.dump(rows, open(sys.argv[2], "w"), indent=0)
print("tasks", len(rows))
