"""Build byte-faithful T06/T08 mutants (same replace as round41_c1_verify.py MUTANTS) plus
traced reference / traced mutant copies that prove the mutated lines execute on the killing
fixtures. Trace hooks only add stderr prints; control flow is unchanged."""
import pathlib
import py_compile
import sys

src = pathlib.Path(sys.argv[1]).read_text()
out = pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

T06_OLD = "    return 0 if d == 0 and control_ok else 1"
T06_NEW = "    return 0 if d == 0 or control_ok else 1"
T08_OLD = "            elif shutil.which(argv[0]) is None:"
T08_NEW = "            elif False:"
assert src.count(T06_OLD) == 1, "T06 old line not unique"
assert src.count(T08_OLD) == 1, "T08 old line not unique"

# pure mutants: exactly the counter's construction
(out / "t06_pure.py").write_text(src.replace(T06_OLD, T06_NEW, 1))
(out / "t08_pure.py").write_text(src.replace(T08_OLD, T08_NEW, 1))

# T06 traced: a print beside the final return; semantics identical to ref / mutant
t06_ref = src.replace(
    T06_OLD,
    '    print(f"TRACE T06 ref final-return reached d={d!r} control_ok={control_ok!r}", '
    'file=sys.stderr)\n' + T06_OLD, 1)
t06_mut = src.replace(
    T06_OLD,
    '    print(f"TRACE T06 MUTATED line reached d={d!r} control_ok={control_ok!r}", '
    'file=sys.stderr)\n' + T06_NEW, 1)
(out / "t06_ref_trace.py").write_text(t06_ref)
(out / "t06_mut_trace.py").write_text(t06_mut)

# T08 traced: the elif condition moves into a helper that prints then returns the same value
HELPER_REF = (
    'def _t08(a0: str) -> bool:\n'
    '    hit = shutil.which(a0) is None\n'
    '    print(f"TRACE T08 ref line evaluated argv0={a0!r} dependency_missing={hit}", '
    'file=sys.stderr)\n'
    '    return hit\n'
    '\n'
    '\n'
    'def main() -> int:')
HELPER_MUT = (
    'def _t08(a0: str) -> bool:\n'
    '    print(f"TRACE T08 MUTATED line evaluated argv0={a0!r} (branch constant False)", '
    'file=sys.stderr)\n'
    '    return False\n'
    '\n'
    '\n'
    'def main() -> int:')
t08_ref = src.replace("def main() -> int:", HELPER_REF, 1).replace(T08_OLD, "            elif _t08(argv[0]):", 1)
t08_mut = src.replace("def main() -> int:", HELPER_MUT, 1).replace(T08_OLD, "            elif _t08(argv[0]):", 1)
(out / "t08_ref_trace.py").write_text(t08_ref)
(out / "t08_mut_trace.py").write_text(t08_mut)

for p in sorted(out.glob("*.py")):
    py_compile.compile(str(p), doraise=True)
    print("compiled", p.name)
