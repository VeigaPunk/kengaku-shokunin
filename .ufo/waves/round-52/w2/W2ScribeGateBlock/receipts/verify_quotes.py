import re, sys, html, json
F = "fetch/"
checks = [
 ("readme.md", "tasks are (1) solvable, (2) realistic, and (3) well-specified"),
 ("readme.md", "Each task in TB2.0 has received several hours of human and LM-assisted validation"),
 ("readme.md", "You can view them at https://github.com/laude-institute/terminal-bench-2"),
 ("arxiv-2601.11868.html", "A terminal bench task is considered well-specified if the unit tests will pass if and only if the container ends in an acceptable state."),
 ("arxiv-2605.26079v2.html", "uncovering issues such as hidden environment dependencies, specification gaps, and limited grading logic."),
 ("arxiv-2605.26079v2.html", "Our trajectory audit independently recovered 14 of these 21 issues under strict matching"),
 ("tbench21.html", "Some tasks had instructions that were not aligned to their tests."),
 ("tbench21.html", "fixes 28 tasks"),
 ("hf-zai.html", "the test logic itself misjudged valid submissions or let non-compliant outputs through"),
 ("hf-zai.html", "conducted a comprehensive review of the entire Terminal-Bench 2.0 dataset"),
 ("june.html", "On Terminal-Bench 2.1, 40 of 83 gold-passing tasks (48%) certify success after a careless deletion"),
 ("swe-2503.15223.html", "a patch may pass the tests but nevertheless fail to match the developers’ expectations."),
 ("snorkel.html", "A revision of Terminal-Bench 2.0 that fixes 28 of 89 tasks and introduces continuous validation for agentic benchmarks."),
 ("gh1387.html", "Verifiers that grade against a golden artifact instead of solution properties"),
 ("pr53.api.json", "Tests were updated when they over-specified or let any solution pass."),
 ("pr53.api.json", "polyglot-c-py"),
 ("lacuna.html", "28"),
]
def norm_text(s):
    s = html.unescape(s)
    return s
def find(fname, quote):
    raw = open(F+fname, encoding="utf-8", errors="replace").read()
    words = quote.split()
    pat = r"(?:\s|<[^>]{0,400}>|&nbsp;)+".join(re.escape(w).replace("’", "(?:’|&#8217;|&rsquo;|')") for w in words)
    m = re.search(pat, raw)
    if not m:
        m2 = re.search(pat, html.unescape(raw))
        return ("MISS", None)
    line = raw.count("\n", 0, m.start()) + 1
    return ("HIT", line)
for fn, q in checks:
    nw = len(q.split())
    r = find(fn, q)
    print(f"{r[0]:4} line={str(r[1]):>6} words={nw:>2} {fn} :: {q[:90]}")
