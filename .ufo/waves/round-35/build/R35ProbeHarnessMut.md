# R35ProbeHarnessMut — probe-harness mutation tests (kengaku r35 wave 1)

Seat: R35ProbeHarnessMut (executor, leaf). Target: `plans/tb2_grader_probe.py` `run_grader`
(the `mod.Path = lambda _arg: real(p)` monkeypatch). All work in
`.ufo/waves/round-35/build/R35ProbeHarnessMut/` (scratch) + `/tmp`; lane untouched.

## Setup (copies, byte-identical)

```
S=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-35/build/R35ProbeHarnessMut
mkdir -p "$S/corpus/evidence/round35/tb2-eval" "$S/lane-tampered/corpus/evidence/round35/tb2-eval"
cp .../plans/tb2_grader_probe.py "$S/probe_orig.py"
cp .../corpus/evidence/round35/tb2-eval/{test_outputs.py,test.sh,instruction.md,SHA256SUMS} "$S/corpus/evidence/round35/tb2-eval/"
cp .../corpus/evidence/round35/tb2-grader-probe.txt "$S/"
cp "$S/corpus/evidence/round35/tb2-eval/test_outputs.py" "$S/lane-tampered/corpus/evidence/round35/tb2-eval/"
sha256sum "$S/corpus/evidence/round35/tb2-eval/test_outputs.py"   # 44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582 (pinned)
```

Tooling: `uv 0.13.0` at `~/.local/bin/uv` (pre-existing; **no installs/updates performed** —
nothing to record). Biopython 1.85 via `uv run --no-project --with biopython==1.85`.
`/app/gblock.txt` is absent on the host (`ls -ld /app/gblock.txt` → No such file or directory) —
precondition for mutation (a).

## Baseline (control): fresh run reproduces the committed receipt byte-for-byte

Command:
```
cd /tmp && uv run --no-project --with biopython==1.85 python3 "$S/probe_orig.py" --lane "$S"
```

Output (saved to `$S/baseline.out`, `diff` vs committed receipt → `BASELINE_BYTE_EQUAL`, exit 0):
```
grader=corpus/evidence/round35/tb2-eval/test_outputs.py sha256=44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582 pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6 biopython=1.85
components_aa=8,259,158,235,182 max_passing_nt=2766 cap_nt=3000
case=valid-balanced predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='all bullets: GS linkers 5..20, order, no Met/stop, GC windows, <=3000 nt'
...
cases=18 observed_pass=5 observed_fail=13 mismatches=0
EXIT=0
```

## Mutation (a): break the patch → grader reads a nonexistent path → valid case turns fail

Two variants, both from `$S/probe_orig.py`; both keep case bytes identical to baseline.

- `probe_a_unpatched.py`: `mod.Path = lambda _arg: real(p)` removed (line 126 → comment). Grader's own
  `Path("/app/gblock.txt")` resolves on the host; `/app/gblock.txt` absent.
- `probe_a_missing.py`: patch retargeted to `real(d) / "MUTATION-does-not-exist" / "gblock.txt"`.

Command (each):
```
cd /tmp && uv run --no-project --with biopython==1.85 python3 "$S/probe_a_unpatched.py" --lane "$S"
```

Output (first + last lines shown; identical shape for both variants):
```
case=valid-balanced predicted=pass observed=fail match=NO nt=2586 gcwin=ok assertion='File /app/gblock.txt does not exist.' requirement='all bullets: GS linkers 5..20, order, no Met/stop, GC windows, <=3000 nt'
...
cases=18 observed_pass=0 observed_fail=18 mismatches=5
EXIT=1
```

`probe_a_missing.py` identical except assertion path `.../MUTATION-does-not-exist/gblock.txt does not exist.`, `mismatches=5`, exit 1.
**Valid case turns fail** (assertion `File ... does not exist.`), 5 mismatches (the 5 predicted-pass
cases), exit 1 — the harness observes the file it actually wires into the grader.

## Mutation (b): feed every case the valid content → mismatches > 0

`probe_b_allvalid.py`: after `cases = build_cases(parts)` insert
`VALID = cases[0][1]; cases = [(name, VALID, pred, req) for name, _, pred, req in cases]`.

Command:
```
cd /tmp && uv run --no-project --with biopython==1.85 python3 "$S/probe_b_allvalid.py" --lane "$S"
```

Output:
```
case=valid-balanced predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='all bullets: GS linkers 5..20, order, no Met/stop, GC windows, <=3000 nt'
case=linker-4aa predicted=fail observed=pass match=NO nt=2586 gcwin=ok assertion='-' requirement='linkers 5..20 aa'
case=donor-repeated predicted=fail observed=pass match=NO nt=2586 gcwin=ok assertion='-' requirement='do not repeat a protein'
case=non-acgt-base predicted=fail observed=pass match=NO nt=2586 gcwin=ok assertion='-' requirement='gBlock is a DNA sequence'
...
cases=18 observed_pass=18 observed_fail=0 mismatches=13
EXIT=1
```

**mismatches=13 > 0** (all 13 predicted-fail cases now observe pass), exit 1. Note every `nt=2586`
(the valid length) — the observations track the bytes fed, not the case names.

## Mutation (c): tamper one byte of copied test_outputs.py → probe refuses on digest

`$S/lane-tampered/corpus/evidence/round35/tb2-eval/test_outputs.py`: first char `#` → `X` (offset 1,
octal `43` → `130`, `cmp -l` shows exactly one differing byte). sha256 changes to
`a25354f835c97426a430aba212cec3d01e82ae0bc5df51a7e8d780fddef21afe`.

Command:
```
cd /tmp && uv run --no-project --with biopython==1.85 python3 "$S/probe_orig.py" --lane "$S/lane-tampered"
```

Output:
```
REFUSE grader digest a25354f835c97426a430aba212cec3d01e82ae0bc5df51a7e8d780fddef21afe != pinned 44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582
EXIT=2
```

Probe **REFUSEs** (exit 2) before loading/executing the grader.

## Conclusion

Harness proven to grade the actual case bytes: baseline reproduces the receipt byte-for-byte; the
same grader bytes observe different outcomes when (a) the read target is broken (valid → fail) or
(b) the content is swapped to valid everywhere (13 mismatches); one flipped byte in the grader copy is
caught by the pinned-digest gate (REFUSE, exit 2). All runs used `uv run --no-project --with
biopython==1.85`; every number above carries its producing command.

Files changed (scratch only, under `build/R35ProbeHarnessMut/`): `probe_orig.py`, `probe_a_unpatched.py`,
`probe_a_missing.py`, `probe_b_allvalid.py`, `baseline.out`, `corpus/evidence/round35/tb2-eval/*`,
`lane-tampered/corpus/evidence/round35/tb2-eval/test_outputs.py`. Lane, corpus, plans, and all other
lane files untouched.

VERDICT: harness-mutants-3/3
