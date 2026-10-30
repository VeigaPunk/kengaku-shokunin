#!/usr/bin/env python3
"""C1MutClassifier harness: build >=15 mutants of the frozen classifier and score three detectors.

Detectors
  D1  classifier's own --selftest      (83 frozen cases)
  D2  C1ExecAdvCases/check.py           (90 adversarial cases / 371 tests)
  D3  population class movement over the 305 tests-index ids (capture bytes in scratch)

D3 is scored twice: raw class movement vs pristine, and the counter's ORACLE leg
(disagree vs the merged blind labels) so a mutant that moves a class but stays
inside the 3 % budget is visible as a survivor of the leg, not only of the class.

usage: mutate.py build | run
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE / "lane"
CAP = HERE / "capture"                       # capture bytes (copy of corpus/evidence/round52/graders)
PRISTINE = HERE / "mutants" / "pristine.py"
MUTDIR = HERE / "mutants"
ADVCASE = LANE / ".ufo/waves/round-53/w1/C1ExecAdvCases/check.py"
TESTS_INDEX = LANE / "corpus/evidence/round53/tests-index.json"

# ---------------------------------------------------------------------------------------------
# mutants: (name, family, note, [(old, new), ...])
# every replacement is asserted to occur exactly once in the pristine source
# ---------------------------------------------------------------------------------------------
MUTANTS: list[tuple[str, str, str, list[tuple[str, str]]]] = [
    ("M01-join-KN-to-K", "join-lattice", "join() maps {K,N} to N instead of K (one comparison result flipped)", [
        ("    if s == {K, N}:\n        return N\n", "    if s == {K, N}:\n        return K\n"),
    ]),
    ("M02-join-KL-to-N", "join-lattice", "join() maps {K,L}/{N,L} to N instead of L", [
        ("    if s == {K, L} or s == {N, L}:\n        return L\n",
         "    if s == {K, L} or s == {N, L}:\n        return N\n"),
    ]),
    ("M03-join-BQ-to-B", "join-lattice", "join() maps {B,Q} to B instead of Q", [
        ("    if s == {B, Q}:\n        return Q\n", "    if s == {B, Q}:\n        return B\n"),
    ]),
    ("M04-join_all-empty-to-X", "join-lattice", "join_all() of an empty set is X instead of K (default kind dropped)", [
        ("    return K if out is None else out\n", "    return X if out is None else out\n"),
    ]),
    ("M05-is_num_const-accepts-bool", "constant-check", "is_num_const() drops the 'not bool' guard (Constant-value check weakened)", [
        ("    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):\n",
         "    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):\n"),
    ]),
    ("M06-request-param-to-X", "constant-check", "request.param (a fixture parameter value) is treated as unknown", [
        ("            # request.param is a fixture parameter value: a name, not filesystem state.\n            return K\n",
         "            # request.param is a fixture parameter value: a name, not filesystem state.\n            return X\n"),
    ]),
    ("M07-boolop-drop-B-branch", "join-lattice", "e_BoolOp drops the B/Q/V/C branch (a boolean predicate in an 'and' is no longer a predicate)", [
        ("        if any(k in (B, Q, V, C) for k in ks):\n            return B\n", ""),
    ]),
    ("M08-existq-B-to-K", "exist-query", "os.path.exists() returns a constant instead of an existence predicate", [
        ("        if q in EXIST_Q:\n            if allk and all(self.pathish(k) for k in allk):\n                return B\n",
         "        if q in EXIST_Q:\n            if allk and all(self.pathish(k) for k in allk):\n                return K\n"),
    ]),
    ("M09-listq-drop-scandir", "list-query", "os.scandir is removed from LIST_Q (a listing call is no longer recognised)", [
        ('LIST_Q = {"os.listdir": L, "os.scandir": L, "glob.glob": L, "glob.iglob": L, "os.walk": W}',
         'LIST_Q = {"os.listdir": L, "glob.glob": L, "glob.iglob": L, "os.walk": W}'),
    ]),
    ("M10-cmp-count-not-flagged", "comparison", "a count comparison (len(...) == 3) is not a clause-2 violation", [
        ('        if C in (lk, rk):\n            # A count is a value, not a path state: the spec\'s N clause lists "a count" explicitly.\n            return self.v("count/size comparison (a count is a value, not a path state)", at)\n',
         '        if C in (lk, rk):\n            # A count is a value, not a path state: the spec\'s N clause lists "a count" explicitly.\n            return K\n'),
    ]),
    ("M11-const-cmp-in-assert-allowed", "assertion", "a value comparison inside an assertion is allowed (the assertion-context check is dropped)", [
        ('            if fr is not None and getattr(fr, "in_assert", False):\n                return self.v("value comparison of computed values", at)\n',
         '            if fr is not None and getattr(fr, "in_assert", False):\n                return K\n'),
    ]),
    ("M12-record-assert-constant-ok", "assertion", "an assertion that depends on no path state is not a violation", [
        ('        elif k == K:\n            self.v("assertion depends on no path state (constant/computed value)", node)\n', ""),
    ]),
    ("M13-record-assert-unknown-ok", "assertion", "an assertion depending on content/value/unknown is not a violation", [
        ('        if k == X:\n            self.v("assertion depends on content/value/unknown", node)\n', ""),
    ]),
    ("M14-unconditional-fail-ok", "assertion", "an unconditional / constant-guarded failure is not a violation", [
        ('        else:\n            self.v("unconditional or constant-guarded failure", node)\n', ""),
    ]),
    ("M15-open-write-modes-drop-w", "write-vs-read", "open() in mode 'w' is no longer write-only (a write is read as content)", [
        ('WRITE_OPEN_MODES = {"w", "wb", "a", "ab", "x", "xb"}', 'WRITE_OPEN_MODES = {"wb", "ab", "xb"}'),
    ]),
    ("M16-all-over-listing-allowed", "universality", "all() over a listing is not a universal-quantifier violation", [
        ('            if name == "all" and k in (L, V, W, E):\n                return self.v("all(...) over a listing (universal: depends on absence of other entries)", n)\n',
         ""),
    ]),
    ("M17-try-handler-never-path-state", "control-flow", "an exception handler never encodes path state (try/except pytest.fail loses its predicate)", [
        ("        hk = B if self.fs_touch > before else K    # an exception can only encode path state if the body touched paths",
         "        hk = K    # an exception can only encode path state if the body touched paths"),
    ]),
    ("M18-if-exit-guard-without-exits", "control-flow", "the 'if <exists>: return' exit guard is set even when the block does not exit", [
        ("        if not s.orelse and tk in FS and self.exits(s.body):", "        if not s.orelse and tk in FS:"),
    ]),
    ("M19-for-break-guard-any", "control-flow", "a break guard is honoured even when the condition is not path state", [
        ("            if g is not None and g in FS:", "            if g is not None:"),
    ]),
    ("M20-no-assertion-reason-dropped", "assertion", "a test with no path assertion is not flagged (the 'no assertion reached' reason is dropped)", [
        ('    if not reasons and r.fs_asserts == 0:\n        reasons.append("no assertion reached that tests path existence")\n', ""),
    ]),
    ("M21-async-fixture-not-scanned", "async-vs-sync", "Module._scan drops AsyncFunctionDef: an async fixture is not registered", [
        ("            elif isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)):\n                isf, nm, auto = self.fixture_info(st)",
         "            elif isinstance(st, ast.FunctionDef):\n                isf, nm, auto = self.fixture_info(st)"),
    ]),
    ("M22-async-test-not-a-unit", "async-vs-sync", "test_units drops AsyncFunctionDef: an async test is not a test unit", [
        ('        if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)) and st.name.startswith("test_"):\n            out.append((st.name, st, None))\n',
         '        if isinstance(st, ast.FunctionDef) and st.name.startswith("test_"):\n            out.append((st.name, st, None))\n'),
    ]),
    ("M23-decorators-as-body", "decorators", "a test's decorators are analysed as body statements", [
        ("    r.exec_stmts(fd.body, fr)", "    r.exec_stmts(list(fd.decorator_list) + list(fd.body), fr)"),
    ]),
    ("M24-parametrize-listing-K", "parametrize", "a listing-valued parametrize argument is a constant instead of a name", [
        ("                pk = {K: K, L: N}.get(vk, X)", "                pk = {K: K, L: K}.get(vk, X)"),
    ]),
    ("M25-elem-listing-to-K", "element-kind", "the element kind of a listing is a constant instead of a name", [
        ("        return {K: K, N: N, L: N, W: \"WT\", E: \"ET\", Q: X, V: X, B: X, C: X, X: X}.get(k, X)",
         "        return {K: K, N: N, L: K, W: \"WT\", E: \"ET\", Q: X, V: X, B: X, C: X, X: X}.get(k, X)"),
    ]),
    ("M26-subscript-pick-is-listing", "subscript", "picking a named entry out of a listing stays a listing instead of a name", [
        ("            return N if isinstance(n.slice, ast.Constant) else L   # pick a named entry / slice of the listing",
         "            return L   # pick a named entry / slice of the listing"),
    ]),
    ("M27-assert-context-flag-off", "assertion", "s_Assert does not mark the assertion context (in_assert stays False)", [
        ("        old_ia = fr.in_assert\n        fr.in_assert = True\n        try:\n            k = self.eval(t, fr)\n        finally:\n            fr.in_assert = old_ia\n",
         "        old_ia = fr.in_assert\n        fr.in_assert = False\n        try:\n            k = self.eval(t, fr)\n        finally:\n            fr.in_assert = old_ia\n"),
    ]),
    ("M28-implicit-setup-off", "helper-visit", "the implicit setUp/setup_module helper visit is switched off", [
        ("IMPLICIT_SETUP = True ", "IMPLICIT_SETUP = False "),
    ]),
    ("M29-class-chain-no-inheritance", "helper-visit", "the class chain does not follow base classes (an inherited method is not found)", [
        ("            for b in self.classes[c].bases:\n                nm = dotted(b)\n                if nm and nm.split(\".\")[-1] in self.classes:\n                    todo.append(nm.split(\".\")[-1])\n",
         "            for b in []:\n                nm = dotted(b)\n                if nm and nm.split(\".\")[-1] in self.classes:\n                    todo.append(nm.split(\".\")[-1])\n"),
    ]),
    ("M30-module-helper-not-registered", "helper-visit", "a module-level helper is not registered, so calls into it are undefined", [
        ("                if cls is None:\n                    self.funcs[st.name] = st\n",
         "                if cls is None:\n                    pass\n"),
    ]),

    ("M31-is_bool_const-any-constant", "constant-check", "is_bool_const() accepts any Constant as a boolean (the bool-value check is dropped)", [
        ("    return isinstance(n, ast.Constant) and isinstance(n.value, bool)",
         "    return isinstance(n, ast.Constant)"),
    ]),
    ("M32-e_Constant-unknown", "constant-check", "a literal constant is unknown instead of a known value", [
        ("    def e_Constant(self, n, fr):\n        return K",
         "    def e_Constant(self, n, fr):\n        return X"),
    ]),
    ("M33-known-k-modules-drop-os", "constant-check", "the 'os' module is not a known-value module", [
        ('KNOWN_K_MODULES = {"os", "sys", "pathlib", "glob", "fnmatch", "stat", "time", "pytest", "unittest", "logging", "typing",',
         'KNOWN_K_MODULES = {"sys", "pathlib", "glob", "fnmatch", "stat", "time", "pytest", "unittest", "logging", "typing",'),
    ]),
    ("M34-exist-q-drop-os-path-exists", "exist-query", "os.path.exists is not an existence query", [
        ('EXIST_Q = {"os.path.exists", "os.path.isfile", "os.path.isdir", "os.path.islink", "os.path.lexists",',
         'EXIST_Q = {"os.path.isfile", "os.path.isdir", "os.path.islink", "os.path.lexists",'),
    ]),
    ("M35-list-m-drop-iterdir", "list-query", "Path.iterdir is not a listing method", [
        ('LIST_M = {"iterdir": L, "glob": L, "rglob": L, "scandir": L}', 'LIST_M = {"glob": L, "rglob": L, "scandir": L}'),
    ]),
    ("M36-pure-q-drop-pathlib", "constant-check", "pathlib.Path is not a pure-value constructor", [
        ('PURE_Q = {"pathlib.Path", "pathlib.PurePath", "pathlib.PosixPath", "pathlib.PurePosixPath",',
         'PURE_Q = {"pathlib.PurePath", "pathlib.PosixPath", "pathlib.PurePosixPath",'),
    ]),
    ("M37-membership-not-a-predicate", "comparison", "membership over names is not an existence predicate", [
        ('            if rk in (L, W, E, Q, K, N) and lk in (K, N):\n                return B',
         '            if rk in (L, W, E, Q, K, N) and lk in (K, N):\n                return K'),
    ]),
    ("M38-write-count-not-a-count", "write-vs-read", "a write that returns a byte count is not a count value", [
        ('WRITE_COUNT_M = {"write_text", "write_bytes"}          # these return a byte/char count',
         'WRITE_COUNT_M = set()          # these return a byte/char count'),
    ]),
    ("M39-mutate-drops-var", "write-vs-read", "a mutating call does not update the variable it mutates", [
        ("        if cur == K and add == K:\n            return\n        self.set_var(fr, name, L)",
         "        if cur == K and add == K:\n            return\n        pass"),
    ]),
    ("M40-class-attr-self-only", "helper-visit", "a class attribute is only read from the exact class, not its chain", [
        ("            for c in self.m.class_chain(cn):\n                if attr in self.m.cassign.get(c, {}):",
         "            for c in [cn]:\n                if attr in self.m.cassign.get(c, {}):"),
    ]),
    ("M41-fixture-autouse-dropped", "helper-visit", "an autouse fixture is not run", [
        ("                    if auto:\n                        self.autouse.append((st, cls))",
         "                    if False:\n                        self.autouse.append((st, cls))"),
    ]),
    ("M42-tmp-fixtures-dropped", "helper-visit", "tmp_path/tmpdir are not pure fixtures", [
        ('TMP_FIXTURES = {"tmp_path", "tmpdir", "tmp_path_factory", "tmpdir_factory"}', 'TMP_FIXTURES = set()'),
    ]),
]


def read_src() -> str:
    return (LANE / "plans/round53_c1_classify.py").read_text()


def build() -> int:
    src = read_src()
    MUTDIR.mkdir(parents=True, exist_ok=True)
    PRISTINE.write_text(src)
    manifest = []
    for name, family, note, edits in MUTANTS:
        s = src
        for old, new in edits:
            n = s.count(old)
            if n != 1:
                print(f"ABORT {name}: pattern occurs {n} times: {old[:70]!r}")
                return 2
            s = s.replace(old, new)
        p = MUTDIR / f"{name}.py"
        p.write_text(s)
        # a mutant must still be valid python
        r = subprocess.run([sys.executable, "-c", f"import ast,sys;ast.parse(open({str(p)!r}).read())"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"ABORT {name}: syntax error {r.stderr[:200]}")
            return 2
        manifest.append({"name": name, "family": family, "note": note, "path": str(p)})
    (HERE / "mutants-manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"built {len(manifest)} mutants + pristine")
    return 0


def load_classify(path: Path):
    spec = importlib.util.spec_from_file_location("c1_mut_" + path.stem.replace("-", "_"), path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.classify_source


def population(classify):
    """-> {test id: class} over the 305 tests-index ids, using the scratch capture bytes."""
    idx = json.loads(TESTS_INDEX.read_text())["tests"]
    by_file: dict[str, dict] = {}
    out = {}
    for t in idx:
        f = t["file"]
        if f not in by_file:
            src = (CAP / f).read_text(encoding="utf-8", errors="replace")
            by_file[f] = classify(src)
        key = f"{t['class']}.{t['name']}" if t["class"] else t["name"]
        out[t["id"]] = by_file[f].get(key)
    return out


def decided_labels():
    """Merge the eight blind label seats' own files over the pinned shards (counter's rule, A1)."""
    lane = LANE
    seats = {"A": "C1LabelScoutA", "B": "C1LabelRevB", "C": "C1LabelScoutC", "D": "C1LabelRevD",
             "E": "C1LabelScoutE", "F": "C1LabelRevF", "G": "C1LabelScoutG", "H": "C1LabelRevH"}
    shards = {k: json.loads((lane / f".ufo/waves/round-53/labels/shard-{k}.json").read_text()) for k in seats}
    in_shards: dict[str, list[str]] = {}
    for k, rows in shards.items():
        for r in rows:
            in_shards.setdefault(r["id"], []).append(k)
    per_seat = {}
    for k, s in seats.items():
        d = json.loads((lane / f".ufo/waves/round-53/w1/{s}/labels.json").read_text())
        per_seat[k] = d["labels"]
    decided = {}
    for tid, ks in in_shards.items():
        if len(ks) != 2 or len(set(ks)) != 2:
            continue
        a, b = (per_seat[k][tid]["label"] for k in ks)
        if a == b and a in ("Y", "N"):
            decided[tid] = a
    return decided


def selftest(path: Path) -> dict:
    r = subprocess.run([sys.executable, str(path), "--selftest"], capture_output=True, text=True,
                       cwd=str(HERE))
    out = r.stdout + r.stderr
    fails = None
    for line in out.splitlines():
        if line.startswith("cases="):
            for part in line.split():
                if part.startswith("failures="):
                    fails = int(part.split("=")[1])
    if fails is None:
        fails = -1
    return {"rc": r.returncode, "failures": fails, "tail": out.strip().splitlines()[-3:]}


def advcheck(path: Path) -> dict:
    r = subprocess.run([sys.executable, str(ADVCASE), str(path), "-q"], capture_output=True, text=True,
                       cwd=str(HERE))
    out = r.stdout + r.stderr
    cf = tf = None
    for line in out.splitlines():
        if line.startswith("TOTAL"):
            for part in line.split():
                if part.startswith("case_fail="):
                    cf = int(part.split("=")[1])
                if part.startswith("test_fail="):
                    tf = int(part.split("=")[1])
    fails = []
    for line in out.splitlines():
        if line.startswith("FAIL "):
            fails.append(line[:160])
    return {"rc": r.returncode, "case_fail": cf, "test_fail": tf, "fails": fails[:12]}


def run() -> int:
    decided = decided_labels()
    base = population(load_classify(PRISTINE))
    base_moved = {k: v for k, v in base.items() if v is None}
    print(f"pristine population ids={len(base)} unclassified={len(base_moved)} "
          f"P1={sum(1 for v in base.values() if v == 'P1')} P0={sum(1 for v in base.values() if v == 'P0')}")
    base_dis = sum(1 for t, y in decided.items() if (base.get(t) == 'P1') != (y == 'Y'))
    print(f"pristine ORACLE disagree={base_dis} decided={len(decided)} limit={0.03 * len(decided):.1f}")
    results = []
    for name, family, note in [("PRISTINE", "-", "frozen classifier")] + [(m[0], m[1], m[2]) for m in MUTANTS]:
        p = PRISTINE if name == "PRISTINE" else MUTDIR / f"{name}.py"
        st = selftest(p)
        ad = advcheck(p)
        try:
            cls = load_classify(p)
            pop = population(cls)
            err = None
        except Exception as e:  # noqa: BLE001
            pop, err = {}, f"{type(e).__name__}: {e}"
        moved = sorted(t for t, v in pop.items() if v != base.get(t))
        uncls = sorted(t for t, v in pop.items() if v is None)
        dis = sum(1 for t, y in decided.items() if (pop.get(t) == 'P1') != (y == 'Y'))
        killed_d1 = st["failures"] != 0
        killed_d2 = ad["case_fail"] not in (0, None) or ad["rc"] != 0
        killed_d3 = len(moved) > 0
        oracle_breaks = dis > 0.03 * len(decided)
        results.append({
            "mutant": name, "family": family, "note": note,
            "d1_selftest": st, "d2_adv": ad,
            "d3_population": {"ids": len(pop), "moved": len(moved), "moved_ids": moved[:20],
                              "unclassified": len(uncls), "error": err,
                              "oracle_disagree": dis, "oracle_leg_breaks": oracle_breaks},
            "killed": {"d1": killed_d1, "d2": killed_d2, "d3": killed_d3},
            "killed_by_any": killed_d1 or killed_d2 or killed_d3,
            "killed_by_all": killed_d1 and killed_d2 and killed_d3,
        })
        print(f"{name:34s} D1={'K' if killed_d1 else 's'} D2={'K' if killed_d2 else 's'} "
              f"D3={'K' if killed_d3 else 's'} moved={len(moved):3d} dis={dis:3d} "
              f"oracle_breaks={oracle_breaks}")
    (HERE / "results.json").write_text(json.dumps(results, indent=1))
    surv = [r for r in results if r["mutant"] != "PRISTINE" and not r["killed_by_any"]]
    print(f"\nsurvivors (no detector fired): {len(surv)}")
    for r in surv:
        print("  ", r["mutant"], r["family"])
    return 0


if __name__ == "__main__":
    sys.exit(build() if sys.argv[1] == "build" else run())
