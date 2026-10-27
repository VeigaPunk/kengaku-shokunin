import importlib.util, itertools, pathlib, sys
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45SimplifierCounter")
def load(p, name):
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
new = load(S/"patched/round45_c1_verify.py", "c45_new")
orig = load(S/"lane/plans/round45_c1_verify.py", "c45_old")
fails = []

# --- 1. outside(): `p == s or p.is_relative_to(s)` is p.is_relative_to(s) ---
paths = [pathlib.Path(x) for x in ["/a", "/a/b", "/a/b/c", "/a/bc", "/x", "/", "/a/b/../b/c", "b", ""]]
n = 0
for p, s, d in itertools.product(paths, paths, paths):
    old = any(p == s or p.is_relative_to(s) for s in (s,)) and not (p == d or p.is_relative_to(d))
    got = new.outside(p, (s,), d)
    n += 1
    if old != got: fails.append(("outside", str(p), str(s), str(d), old, got))
print(f"outside(): {n} path triples, mismatches={len(fails)}")

# --- 2. DONE_RE return-code class test ---
toks = [str(i) for i in range(0, 200)] + ["-" + str(i) for i in range(1, 200)] + ["E" + c * k for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for k in (1, 2, 3)]
m = 0
for t in toks:
    line = f'1234  openat(AT_FDCWD, "/p", O_RDONLY) = {t}<x>'
    mo = orig.DONE_RE.search(line)
    if not mo: continue
    assert mo.group(1) == t, (t, mo.group(1))
    old = mo.group(1).startswith("E") or mo.group(1).startswith("-")
    m += 1
    if old != (not mo.group(1).isdigit()): fails.append(("digit", t, old))
non = ["?", "0x1", "E", "-", "", "3 <unfinished ...>"]
print(f"DONE_RE rc class: {m} tokens in the regex language, non-language samples={non}, "
      f"mismatches={len([f for f in fails if f[0]=='digit'])}")

# --- 3. count(): old per-row comprehensions vs new helper ---
class Fx: pass
def rows_of(kinds):
    return [({"fid": f"x{i}"}, v, "", o) for i, (v, o) in enumerate(kinds)]
VERDICTS = ["ADMIT", "BREACH", "HUNG", "ERROR"]
KINDS = [(v, o) for v in VERDICTS for o in (0, 1, 2)]
def old_refusal(rows):
    n_admit = sum(v in ("ADMIT", "ERROR") for _fx, v, _w, _o in rows)
    n_hung = sum(v == "HUNG" for _fx, v, _w, _o in rows)
    n_open = sum(o for _fx, _v, _w, o in rows)
    if not rows or n_admit: verdict = "LEAKED"
    elif n_hung: verdict = "HUNG"
    elif n_open: verdict = "READ"
    else: verdict = "clean"
    return n_admit, n_hung, n_open, verdict
def new_refusal(rows):
    c, n_open, _r, _c = new.count(rows)
    n_admit = c.get("ADMIT", 0) + c.get("ERROR", 0)
    n_hung = c.get("HUNG", 0)
    if not rows or n_admit: verdict = "LEAKED"
    elif n_hung: verdict = "HUNG"
    elif n_open: verdict = "READ"
    else: verdict = "clean"
    return n_admit, n_hung, n_open, verdict
def old_honest(rows):
    return (sum(v == "ADMIT" and o == 0 for _fx, v, _w, o in rows),
            sum(v in ("BREACH", "ERROR") for _fx, v, _w, _o in rows),
            sum(o > 0 for _fx, _v, _w, o in rows),
            sum(v == "HUNG" for _fx, v, _w, _o in rows))
def new_honest(rows):
    c, _opens, h_read, h_adm = new.count(rows)
    return h_adm, c.get("BREACH", 0) + c.get("ERROR", 0), h_read, c.get("HUNG", 0)
sets = 0
for k in (0, 1, 2, 3):
    for combo in itertools.product(KINDS, repeat=k):
        rows = rows_of(combo)
        sets += 1
        if old_refusal(rows) != new_refusal(rows): fails.append(("refusal", combo, old_refusal(rows), new_refusal(rows)))
        if old_honest(rows) != new_honest(rows): fails.append(("honest", combo, old_honest(rows), new_honest(rows)))
print(f"count(): {sets} row multisets over {len(KINDS)} verdict/open kinds (len 0-3), "
      f"mismatches={len([f for f in fails if f[0] in ('refusal','honest')])}")

# --- 4. honest-row pool derivation ---
def build_fake(order, permaps):
    per, built = {}, {"refusal": [], "honest": []}
    for g, fname, rows in order:
        built[g].append((fname, None))
        per[(g, fname)] = rows
    return per, built
order = [("refusal", "r1", []), ("honest", "h1", ["a", "b"]), ("refusal", "r2", []), ("honest", "h2", ["c"])]
per, built = build_fake(order, None)
old_pool = [row for (g, _f), rows in per.items() if g == "honest" for row in rows]
new_pool = [row for f, _fxs in built["honest"] for row in per.get(("honest", f), [])]
print(f"honest pool: old={old_pool} new={new_pool} equal={old_pool == new_pool}")
if old_pool != new_pool: fails.append(("pool", old_pool, new_pool))

# --- 5. `mism and K44_REL in mism` ---
for mism in ([], ["x"], [orig.K44_REL], ["x", orig.K44_REL], ["y"]):
    # both are used only as an `if` condition: compare truthiness, not the value ([] vs False)
    if bool(mism and orig.K44_REL in mism) != bool(orig.K44_REL in mism): fails.append(("mism", mism))
print(f"K44 pin guard: 5 mism lists, truthiness mismatches={len([f for f in fails if f[0]=='mism'])}")

# --- 6. dead `first`: no name load escapes ---
import ast
src = (S/"lane/plans/round45_c1_verify.py").read_text()
fn = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == "run_fence"][0]
esc = [n.lineno for n in ast.walk(fn) if isinstance(n, ast.Name) and n.id == "first" and isinstance(n.ctx, ast.Load)]
assigns = [n.lineno for n in ast.walk(fn) if isinstance(n, ast.Name) and n.id == "first" and isinstance(n.ctx, ast.Store)]
returns = [n.lineno for n in ast.walk(fn) if isinstance(n, ast.Return)]
print(f"`first`: stores at {assigns}, loads at {esc} (both inside their own assignment RHS), return lines {returns}")
srcn = (S/"patched/round45_c1_verify.py").read_text()
print(f"`first` in patched source: {'first' in srcn.replace('first={mism[0]}','')}")

print("FAILURES:", fails[:5], "total", len(fails))
sys.exit(1 if fails else 0)
