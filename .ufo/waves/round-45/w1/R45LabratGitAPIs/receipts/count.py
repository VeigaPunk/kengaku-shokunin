import pathlib, re, sys
OPEN_RE = re.compile(r"\bopen(?:at|at2)?\(|creat\(")
DONE_RE = re.compile(r"=\s+(-?\d+|E[A-Z]+)(?:<(.+)>)?\s*$")
UNFINISHED_RE = re.compile(r"(<unfinished \.\.\.>|=\s*\?)\s*$")
RESUMED_RE = re.compile(r"^\s*(\d+)\s*<\.\.\.\s+\w+\s+resumed>")
root, d = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
scratch = (root / "fx", root / "btmp")
opens, first = 0, ""
pending = {}
for line in pathlib.Path(sys.argv[3]).read_text(errors="replace").splitlines():
    pidm = re.match(r"^\s*(\d+)", line)
    pid = pidm.group(1) if pidm else "-"
    if RESUMED_RE.search(line):
        pending.pop(pid, None)
    if not OPEN_RE.search(line):
        continue
    if UNFINISHED_RE.search(line):
        pending[pid] = line
        continue
    done = DONE_RE.search(line)
    if not done or done.group(1).startswith("E") or done.group(1).startswith("-"):
        continue
    p = pathlib.Path(done.group(2) or "")
    if any(p == s or p.is_relative_to(s) for s in scratch) and not (p == d or p.is_relative_to(d)):
        opens += 1
        first = first or str(p)
for line in pending.values():
    for m in re.finditer(r'"(/[^"]+)"', line):
        p = pathlib.Path(m.group(1))
        if any(p == s or p.is_relative_to(s) for s in scratch) and not (p == d or p.is_relative_to(d)):
            opens += 1
            first = first or str(p)
            break
print(f"outside_opens={opens} first={first or '-'}")
