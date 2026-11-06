#!/usr/bin/env python3
"""ExecC1 independent structural checks (own parser, not the frozen instruments).

1. SKILL.md registry rows at BASE vs T: added/removed rows, kind-cell changes, other-cell changes.
2. The 44 re-typed rows' entry scripts: byte-identical at BASE and T?
3. All gate rows at T: entry script exists and mentions a self-test spelling (coarse detector).
4. Ledger: executed totals, file-artifact cells, executed-member set delta.
5. F..T landing surface.
"""
import hashlib
import json
import re
import subprocess
import sys

LANE = sys.argv[1]
BASE = "4992cd0e32b8db23ca20310deb7de12d485f8bcc"
F = "8d9d271306c4e7e2d586e51cd546652249d286cb"
T = "f1083da60e7ff6b88f7420aae7424f7762d14700"
SPLIT = re.compile(r"(?<!\\)\|")
SCRIPT = re.compile(r"([\w./-]+\.(?:py|sh|mjs))")
SPELLING = re.compile(r"self-?test")


def git(*a):
    return subprocess.run(["git", "-C", LANE, *a], capture_output=True)


def blob(rev, path):
    p = git("show", f"{rev}:{path}")
    return p.stdout if p.returncode == 0 else None


def rows(rev):
    text = blob(rev, "SKILL.md").decode()
    lines = text.splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith("## Gate/probe registry"))
    out = {}
    j = i + 1
    while j < len(lines) and not lines[j].startswith("## "):
        ln = lines[j].strip()
        if ln.startswith("|") and not set(ln) <= set("|-: "):
            c = [x.strip() for x in SPLIT.split(ln)[1:-1]]
            if c and c[0] and c[0].lower() not in ("name", "row"):
                out[c[0]] = c
        j += 1
    return out


b, t = rows(BASE), rows(T)
print("== 1. registry rows ==")
print("rows base=%d rev=%d removed=%d added=%d" % (len(b), len(t), len(set(b) - set(t)), len(set(t) - set(b))))
print("added:", sorted(set(t) - set(b)))
kd, other = [], []
for n in sorted(set(b) & set(t)):
    cb, ct = b[n], t[n]
    if len(cb) != len(ct):
        other.append((n, "width", len(cb), len(ct)))
        continue
    for k, (x, y) in enumerate(zip(cb, ct)):
        if x != y:
            (kd if k == 1 else other).append((n, k, x, y))
print("kind_changes=%d other_cell_changes=%d" % (len(kd), len(other)))
print("kind transitions:", sorted({(x, y) for _, _, x, y in kd}))
print("kind histogram base:", {k: sum(1 for v in b.values() if len(v) > 1 and v[1] == k) for k in ("gate", "probe")})
print("kind histogram rev :", {k: sum(1 for v in t.values() if len(v) > 1 and v[1] == k) for k in ("gate", "probe")})

print()
print("== 2. entry scripts of the %d re-typed rows ==" % len(kd))
same, differ, unresolved = 0, [], []
for n, _, _, _ in kd:
    m = SCRIPT.search(t[n][2])
    if not m:
        unresolved.append((n, "no-script-in-entry"))
        continue
    a, c = blob(BASE, m.group(1)), blob(T, m.group(1))
    if a is None or c is None:
        unresolved.append((n, m.group(1)))
        continue
    if hashlib.sha256(a).hexdigest() == hashlib.sha256(c).hexdigest():
        same += 1
    else:
        differ.append((n, m.group(1)))
print("identical=%d differ=%s unresolved=%s" % (same, differ, unresolved))

print()
print("== 3. gate rows at T ==")
gates = {n: v for n, v in t.items() if len(v) > 1 and v[1] == "gate"}
coarse_no, absent = [], []
for n, v in gates.items():
    m = SCRIPT.search(v[2])
    if not m:
        absent.append((n, "no-script-in-entry"))
        continue
    data = blob(T, m.group(1))
    if data is None:
        absent.append((n, m.group(1)))
        continue
    if not SPELLING.search(data.decode(errors="replace")):
        coarse_no.append((n, m.group(1)))
print("gate_rows=%d script_absent=%s no_self_test_mention=%s" % (len(gates), absent, coarse_no))

print()
print("== 4. ledger ==")
for rev in (BASE, T):
    m = json.loads(blob(rev, "plans/grader-population-ledger.json"))["members"]
    ex = {n: v for n, v in m.items() if v.get("status") == "executed"}
    fa = {n for n, v in ex.items() if "file-artifact" in v.get("classes", [])}
    print("%s members=%d executed=%d file-artifact=%d" % (rev[:8], len(m), len(ex), len(fa)))
    if rev == BASE:
        base_set = set(ex)
    else:
        rev_set = set(ex)
print("set_added=%s set_removed=%s" % (sorted(rev_set - base_set), sorted(base_set - rev_set)))

print()
print("== 5. F..T landing surface ==")
print(git("diff", "--name-status", F, T).stdout.decode().strip())
