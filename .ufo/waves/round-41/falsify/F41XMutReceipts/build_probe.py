#!/usr/bin/env python3
"""F41XMutReceipts: splice a near-variant mutant list into a scratch copy of round41_c1_verify.py.

The frozen counter is NOT edited. This writes counter_x.py in scratch with MUTANTS replaced by 20
single-line near-variants of plans/tip_receipts.py outside the frozen T01-T13/S* set, then validates
each old string occurs exactly once in the pristine tool and each variant compiles.
"""
import pathlib
import py_compile
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r41/F41XMutReceipts")
SRC = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round41_c1_verify.py")
TR = "plans/tip_receipts.py"
NOTE = "F41XMutReceipts generalisation probe (no pre-freeze witness)"


def M(mid, direction, cls, adv_kind, adv, old, new):
    return (mid, "receipts", cls, direction, adv_kind, adv, NOTE, old, new)


MUTANTS = [
    M("N01", "silence", "map:corpus/evidence/r/Foo-Probe.txt:derived", "direct",
      f"{TR}:12 'Population, stated mechanically: committed files `corpus/evidence/**/*probe*.{{txt,log}}`' (match is case-blind)",
      r'CANDIDATE_RE = re.compile(r"probe.*\.(?:txt|log)$", re.IGNORECASE)',
      r'CANDIDATE_RE = re.compile(r"probe.*\.(?:txt|log)$")'),
    M("N02", "silence", "map:corpus/evidence/r/Foo-Probe.txt:derived", "direct",
      f"{TR}:15-16 'with non-alphanumerics dropped and case folded, the receipt stem ... are the same token'",
      '    return STEM_RE.sub("", name.lower())',
      '    return STEM_RE.sub("", name)'),
    M("N03", "error", "-", "direct",
      f"{TR}:30-31 '2 usage/setup (..., absent git, clone or cleanup failure, ...)'",
      '    if shutil.which("git") is None:',
      '    if False:'),
    M("N04", "rc-mirror", "-", "direct",
      f"{TR}:7-8 'resolves each one''s committed re-run command from the probe script''s own `Run as:` line'",
      '        if s.startswith(("python3 ", "uv run ")) and base in s:',
      '        if s.startswith(("python3 ", "uv run ")):'),
    M("N05", "rc-mirror", "-", "direct",
      f"{TR}:147 'docstrings pad the command with 2+ spaces before a prose description: keep only the command'",
      '                argv = shlex.split(re.split(r"\\s{2,}", s)[0])',
      '                argv = shlex.split(s)'),
    M("N06", "rc-mirror", "-", "direct",
      f"{TR}:67 'Fallback argv tails, used only when a script''s `Run as:` line cannot be parsed.'",
      '    if script in FALLBACK:',
      '    if False:'),
    M("N07", "rc-mirror", "-", "none",
      f"{TR}:190-191 first_diff 'byte i (line n)' detail carries no advertised sentence",
      '            line = a.count(b"\\n", 0, i) + 1',
      '            line = a.count(b"\\n", 0, i)'),
    M("N08", "rc-mirror", "-", "direct",
      f"{TR}:25-26 '`--tamper REL` ... flips one byte of that receipt''s committed bytes: the comparator must answer `differ`'",
      '            nb = b ^ 0x01\n            return data[:off] + bytes([nb]) + data[off + 1:], off, b, nb',
      '            nb = b\n            return data[:off] + bytes([nb]) + data[off + 1:], off, b, nb'),
    M("N09", "rc-mirror", "-", "direct",
      f"{TR}:235 'restrict to receipts whose rel path contains this' (--only, mapped half)",
      '        mapped = [r for r in mapped if args.only in r]',
      '        mapped = [r for r in mapped if True]'),
    M("N10", "rc-mirror", "-", "direct",
      f"{TR}:235 'restrict to receipts whose rel path contains this' (--only, unmapped half)",
      '        unmapped = [r for r in unmapped if args.only in r]',
      '        unmapped = [r for r in unmapped if True]'),
    M("N11", "silence", "skip:corpus/evidence/r/foo-probe.txt:no-committed-re-run-command", "direct",
      f"{TR}:18-19 'printed on its own `skip reason=no-committed-re-run-command` line' (--list branch)",
      '            print(f"receipt {rel} skip reason=no-committed-re-run-command")',
      '            print(f"receipt {rel} skip reason=no-re-run-command")'),
    M("N12", "error", "-", "direct",
      f"{TR}:9 'clones the lane at HEAD into a scratch directory' (clone-HEAD equality guard)",
      '        if head != tip:',
      '        if False:'),
    M("N13", "rc-mirror", "-", "direct",
      f"{TR}:57 'kind \"byte\" must reproduce exactly; kind \"temp-paths\" declares embedded mkdtemp paths' (table kind assignment)",
      '    plan: dict[str, tuple[str, str, str]] = {r: (s, k, "table") for r, (s, k) in RECEIPTS.items()}',
      '    plan: dict[str, tuple[str, str, str]] = {r: (s, "byte", "table") for r, (s, k) in RECEIPTS.items()}'),
    M("N14", "rc-mirror", "-", "direct",
      f"{TR}:21 'A receipt that declares embedded scratch paths (`temp-paths`) is still re-run' (compare-side kind branch)",
      '            if res["kind"] == "temp-paths":',
      '            if False:'),
    M("N15", "rc-mirror", "-", "direct",
      f"{TR}:26-27 'one control runs automatically on the cheapest byte-equal receipt'",
      '            controls = [min(equal, key=lambda r: len(results[r]["blob"]))] if equal else []',
      '            controls = [max(equal, key=lambda r: len(results[r]["blob"]))] if equal else []'),
    M("N16", "silence", "control:differ", "direct",
      f"{TR}:29-30 '0 every mapped receipt reproduces ... and the control reports `differ`' (auto-control trigger)",
      '            equal = [r for r in mapped if results[r].get("verdict") == "equal"]',
      '            equal = []'),
    M("N17", "rc-silence", "-", "direct",
      f"{TR}:22 'equality after masking is a reproducibility claim up to those paths' (control-side mask)",
      '            same = mask(res["fresh"]) == mask(bad) if res["kind"] == "temp-paths" else res["fresh"] == bad',
      '            same = mask(res["fresh"]) == mask(bad) if False else res["fresh"] == bad'),
    M("N18", "error", "-", "direct",
      f"{TR}:25 '`--tamper REL` (repeatable, comma-splittable)'",
      '        tamper = [t for spec in args.tamper for t in spec.split(",") if t]',
      '        tamper = list(args.tamper)'),
    M("N19", "rc-mirror", "-", "direct",
      f"{TR}:35 'TMPDIR/TEMP/TMP inside the work directory (--work, else the environment''s TMPDIR, else the platform temp dir)' (work-parent creation)",
      '    if work_parent is not None:',
      '    if False:'),
    M("N20", "rc-mirror", "-", "direct",
      f"{TR}:36 'the work directory is removed on exit'",
      '        shutil.rmtree(ws, ignore_errors=True)',
      '        pass'),
]

text = SRC.read_text()
start = text.index("MUTANTS = [")
end = text.index("\n]\n", start) + len("\n]\n")
lines = []
for (mid, tool, cls, direction, adv_kind, adv, w, old, new) in MUTANTS:
    lines.append("    (%r, %r, %r, %r, %r,\n     %r,\n     %r,\n     %r, %r),\n"
                 % (mid, tool, cls, direction, adv_kind, adv, w, old, new))
block = "MUTANTS = [\n" + "".join(lines) + "]\n"
out = S / "counter_x.py"
out.write_text(text[:start] + block + text[end:])

src = (S / "lane" / "plans" / "tip_receipts.py").read_text()
val = S / "val"
val.mkdir(exist_ok=True)
ok = True
for (mid, tool, cls, direction, adv_kind, adv, w, old, new) in MUTANTS:
    c = src.count(old)
    line = src[:src.index(old)].count("\n") + 1 if c == 1 else -1
    v = val / f"{mid}.py"
    v.write_text(src.replace(old, new, 1))
    try:
        py_compile.compile(str(v), doraise=True, cfile=str(val / (mid + ".pyc")))
        comp = "ok"
    except py_compile.PyCompileError:
        comp = "COMPILE-FAIL"
        ok = False
    if c != 1:
        ok = False
    print(f"{mid} mutate_line={line} count={c} compile={comp} dir={direction} cls={cls}")
print("counter_x.py bytes:", out.stat().st_size)
print("VALIDATION", "OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
