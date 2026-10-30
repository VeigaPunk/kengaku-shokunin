#!/usr/bin/env python3
"""C1MutClassifier reachability probe (runtime line tracing on the mutated lines).

A mutant that changes no output is either (a) semantically equivalent (the mutated
branch is reached but the verdict is unchanged) or (b) an unreachable branch (the
mutated code never executes on this corpus).  (b) is a real coverage finding: the
detectors cannot kill it because the code it would break is never exercised.

This probe runs the *pristine* classifier under sys.settrace and counts, for each
anchor, how many times the **exact line the corresponding mutant edits** executes
over the union of the three corpora (83 frozen selftest cases, 90 adversarial cases,
the 305 population ids).

Anchors are (line text, previous-line text or None) so that a line that appears more
than once in the file still resolves uniquely.

usage: reach.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE / "lane"
CAP = HERE / "capture"
ADVDIR = LANE / ".ufo/waves/round-53/w1/C1ExecAdvCases"
TESTS_INDEX = LANE / "corpus/evidence/round53/tests-index.json"
SRC = (LANE / "plans/round53_c1_classify.py").read_text()
SRC_LINES = SRC.splitlines()

# key -> (line the mutant edits, previous line text or None, description)
ANCHORS = {
    "M01-join-KN": ("        return N", "    if s == {K, N}:", "join() maps {K,N} -> N (M01 flips it to K)"),
    "M02-join-KL": ("        return L", "    if s == {K, L} or s == {N, L}:", "join() maps {K,L}/{N,L} -> L (M02 flips it to N)"),
    "M03-join-BQ": ("        return Q", "    if s == {B, Q}:", "join() maps {B,Q} -> Q (M03 flips it to B)"),
    "M04-join_all": ("    return K if out is None else out", None, "join_all() of an empty kind list -> K (M04 flips it to X)"),
    "M05-num_const": ("                k = C", "            elif is_num_const(vnode) is not None:", "a numeric constant is bound to a count (M05 drops the bool guard)"),
    "M06-req_param": ("            return K", "            # request.param is a fixture parameter value: a name, not filesystem state.", "request.param is a constant (M06 flips it to X)"),
    "M07-boolop_B": ("            return B", "        if any(k in (B, Q, V, C) for k in ks):", "e_BoolOp sees a predicate operand (M07 drops the branch)"),
    "M08-existq": ("                return B", "            if allk and all(self.pathish(k) for k in allk):", "an existence query returns a predicate (M08 flips it to K)"),
    "M09-listq": ("                return LIST_Q[q]", "            if allk and all(self.pathish(k) for k in allk):", "a listing query returns a listing (M09 drops os.scandir)"),
    "M10-cmp_C": ('            return self.v("count/size comparison (a count is a value, not a path state)", at)', '            # A count is a value, not a path state: the spec\'s N clause lists "a count" explicitly.', "a count comparison is a violation (M10 returns K)"),
    "M11-cmp_const": ('                return self.v("value comparison of computed values", at)', '            if fr is not None and getattr(fr, "in_assert", False):', "a constant comparison inside an assertion is a violation (M11 returns K)"),
    "M12-rec_assert_K": ('            self.v("assertion depends on no path state (constant/computed value)", node)', "        elif k == K:", "an assertion of kind K is a violation (M12 drops it)"),
    "M13-rec_assert_X": ('            self.v("assertion depends on content/value/unknown", node)', "        if k == X:", "an assertion of kind X is a violation (M13 drops it)"),
    "M14-fail_uncond": ('            self.v("unconditional or constant-guarded failure", node)', "        else:", "an unconditional failure is a violation (M14 drops it)"),
    "M15-open_write": ("        return mode in WRITE_OPEN_MODES", None, "an open() mode is write-only (M15 drops 'w'/'a'/'x')"),
    "M16-all_listing": ('                return self.v("all(...) over a listing (universal: depends on absence of other entries)", n)', '            if name == "all" and k in (L, V, W, E):', "all() over a listing is a violation (M16 drops it)"),
    "M17-try_hk": ("        hk = B if self.fs_touch > before else K    # an exception can only encode path state if the body touched paths", None, "an exception handler encodes path state (M17 forces K)"),
    "M18-if_exit": ("            fr.exit_guard = tk", "            # is still path-dependent (``if path.exists(): return`` followed by ``pytest.fail``).", "the 'if <path>: return' exit guard is set (M18 drops the exits() test)"),
    "M19-for_break": ("                cur = self.break_stack[-1]", "            if g is not None and g in FS:", "a break guard is honoured (M19 drops the FS test)"),
    "M20-no_assert": ('        reasons.append("no assertion reached that tests path existence")', "    if not reasons and r.fs_asserts == 0:", "a test with no path assertion is flagged (M20 drops the reason)"),
    "M21-async_fixture": ("                isf, nm, auto = self.fixture_info(st)", "            elif isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)):", "Module._scan meets a function definition (M21/M22 drop AsyncFunctionDef)"),
    "M22-async_test": ('            out.append((st.name, st, None))', '        if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)) and st.name.startswith("test_"):', "test_units() meets a test definition (M22 drops AsyncFunctionDef)"),
    "M23-decorators": ("    r.exec_stmts(fd.body, fr)", None, "a test body is analysed (M23 adds the decorators to the body)"),
    "M24-parametrize": ("                pk = {K: K, L: N}.get(vk, X)", None, "a parametrize argument's kind is mapped (M24 flips L to K)"),
    "M25-elem": ('        return {K: K, N: N, L: N, W: "WT", E: "ET", Q: X, V: X, B: X, C: X, X: X}.get(k, X)', None, "an element kind is mapped (M25 flips L to K)"),
    "M26-subscript": ("            return N if isinstance(n.slice, ast.Constant) else L   # pick a named entry / slice of the listing", None, "a named entry is picked out of a listing (M26 keeps it a listing)"),
    "M27-assert_ctx": ("        fr.in_assert = True", None, "an assert statement sets the assertion context (M27 forces False)"),
    "M28-implicit_setup": ("    if IMPLICIT_SETUP:", None, "the implicit-setup helper visit runs (M28 switches it off)"),
    "M29-class_chain": ("            for b in self.classes[c].bases:", None, "a base class is followed (M29 drops the walk)"),
    "M30-module_helper": ("                    self.funcs[st.name] = st", None, "a module-level helper is registered (M30 drops the registration)"),
    "M31-bool_const": ("    return isinstance(n, ast.Constant) and isinstance(n.value, bool)", None, "is_bool_const() is consulted (M31 accepts any Constant)"),
    "M32-e_Constant": ("        return K", "    def e_Constant(self, n, fr):", "a literal constant is evaluated (M32 returns X)"),
    "M33-known_k_modules": ('            return K if q.split(".")[0] in KNOWN_K_MODULES else X', '        if q is not None:', "a qualified attribute is checked against the known-value module table (M33 drops 'os')"),
    "M34-exist_q": ('        if q in EXIST_Q:', None, "a qualified call is checked against the existence-query table (M34 drops os.path.exists)"),
    "M35-list_m": ('            if attr in LIST_M:', None, "a method is checked against the listing-method table (M35 drops iterdir)"),
    "M36-pure_q": ('        if q in PURE_Q:', None, "a qualified call is checked against the pure-value table (M36 drops pathlib.Path)"),
    "M37-membership": ('            if rk in (L, W, E, Q, K, N) and lk in (K, N):', None, "membership over names is a predicate (M37 returns K)"),
    "M38-write_count": ('                return C if attr in WRITE_COUNT_M else K', None, "a write method is checked against the write-count table (M38 empties it)"),
    "M39-mutate": ("        self.set_var(fr, name, L)", None, "a mutating call updates the variable (M39 drops it)"),
    "M40-class_chain": ("            for c in self.m.class_chain(cn):", None, "a class attribute is read along the class chain (M40 reads only the exact class)"),
    "M41-autouse": ("                        self.autouse.append((st, cls))", None, "an autouse fixture is registered (M41 drops the registration)"),
    "M42-tmp_fixtures": ('        elif p in TMP_FIXTURES:', '            fr.vars[p] = r.fixcache[p] if r.fixcache[p] is not None else X', "a test parameter is checked against the tmp fixture table (M42 empties it)"),
}


def resolve_anchors():
    out = {}
    for k, (pat, prev, _) in ANCHORS.items():
        hits = [i + 1 for i, ln in enumerate(SRC_LINES) if ln == pat]
        if prev is not None:
            hits = [i + 1 for i, ln in enumerate(SRC_LINES)
                    if ln == pat and i > 0 and SRC_LINES[i - 1] == prev]
        if len(hits) != 1:
            raise SystemExit(f"anchor {k} resolves to {len(hits)} lines: {hits}")
        out[k] = hits[0]
    return out


def load_mod(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    lineno = resolve_anchors()
    for k in ANCHORS:
        print(f"{k:22s} line {lineno[k]:5d}: {SRC_LINES[lineno[k] - 1].strip()[:86]}")
    mod = load_mod(LANE / "plans/round53_c1_classify.py", "reach_pristine")
    modfile = str((LANE / "plans/round53_c1_classify.py").resolve())
    watched = set(lineno.values())
    linemap = {ln: k for k, ln in lineno.items()}

    hits = {k: 0 for k in lineno}
    per_case = []

    def tracer(frame, event, arg):
        if event == "call" and frame.f_code.co_filename == modfile:
            return tracer
        if event == "line" and frame.f_code.co_filename == modfile:
            ln = frame.f_lineno
            if ln in watched:
                hits[linemap[ln]] += 1
        return tracer

    adv = json.loads((ADVDIR / "cases.json").read_text())
    idx = json.loads(TESTS_INDEX.read_text())["tests"]
    srcs = [("selftest:" + name, (mod.HDR + s) if s else "") for name, s, _w in mod.CASES]
    srcs += [("adv:" + c["id"], c["source"]) for c in adv]
    srcs += [("pop:" + t["file"], (CAP / t["file"]).read_text(encoding="utf-8", errors="replace"))
             for t in idx]

    sys.settrace(tracer)
    for tag, s in srcs:
        before = dict(hits)
        try:
            mod.classify_detail(s)
        except Exception as e:  # noqa: BLE001
            print("ERR", tag, e)
        per_case.append((tag, {k: hits[k] - before[k] for k in hits}))
    sys.settrace(None)

    totals = {k: sum(d.get(k, 0) for _, d in per_case) for k in hits}
    ncases = {k: sum(1 for _, d in per_case if d.get(k)) for k in hits}
    print(f"\ncorpora: selftest cases={len(mod.CASES)} adv cases={len(adv)} population ids={len(idx)}")
    print(f"{'anchor':22s} {'hits':>8s} {'cases':>6s}  description")
    for k in ANCHORS:
        print(f"{k:22s} {totals[k]:8d} {ncases[k]:6d}  {ANCHORS[k][2]}")
    (HERE / "reachability.json").write_text(json.dumps(
        {"totals": totals, "cases": ncases, "lines": lineno,
         "per_case": {t: d for t, d in per_case}}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
