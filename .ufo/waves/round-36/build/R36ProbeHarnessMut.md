# R36ProbeHarnessMut — probe-harness mutants (round 36, wave 1)

Seat: executor, leaf. Scope: attack `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/regex_log_probe.py`
in fixture copies only. No lane file, no `plans/`, no `corpus/`, no git state touched.

## Instrument under test (digests re-measured at the tip, `f9efce3`)

```
$ sha256sum plans/regex_log_probe.py corpus/evidence/round36/tb2-regex-log/test_outputs.py
d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc  plans/regex_log_probe.py   # = Amendment 1 digest
345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72  .../test_outputs.py        # = GRADER_SHA256 / SHA256SUMS
$ python3 --version
Python 3.14.8
```

The mini lane tree (`.../build/R36ProbeHarnessMut/mini/`) is byte-identical to the lane for every file it
carries (`sha256sum` compared file by file: `plans/regex_log_probe.py`, `test_outputs.py`, `test.sh`,
`instruction.md` — all `same`). Each mutant is an independent `copytree` of that tree; mutation patterns
are asserted to hit exactly once (`mutate.py`, `pyc_fix.py`), so no mutant is a silent no-op.
Driver: `build/R36ProbeHarnessMut/mutate.py`; raw outputs in `build/R36ProbeHarnessMut/logs/`.

`m0` control (unmodified copy, `python3 plans/regex_log_probe.py --lane .`, cwd = copy root):
`rc=0`, `byte_equal_receipt=True`, `two_runs_equal=True` — the fixture tree reproduces the committed
receipt `corpus/evidence/round36/regex-log-probe.txt` exactly, so any delta below is caused by the
mutant alone.

## (a) Path patch broken → grader reads the real `/app/regex.txt` — DETECTED

Precondition, this host (`ls -la /app` → `No such file or directory`, exit 2): the real path does not exist.

Mutation: `mod.Path = lambda _arg: real(p)` → `mod.Path = real`.

```
$ python3 plans/regex_log_probe.py --lane .        (m1-path-patch-broken)
grader=corpus/evidence/round36/tb2-regex-log/test_outputs.py sha256=345c3bd0… pin=2fd12b88…
case=reference-lenient-days predicted=pass observed=fail match=NO assertion='Regex file /app/regex.txt does not exist' …
case=reference-month-aware predicted=pass observed=fail match=NO assertion='Regex file /app/regex.txt does not exist' …
…
case=padded-file predicted=pass observed=fail match=NO assertion='Regex file /app/regex.txt does not exist' …
case=feb-29-rejected predicted=pass observed=fail match=NO assertion='Regex file /app/regex.txt does not exist' …
cases=24 observed_pass=0 observed_fail=24 mismatches=8
rc=1
```

`match=NO` on exactly 8 lines = exactly the 8 `predicted=pass` cases; all 24 cases observe
`Regex file /app/regex.txt does not exist`, i.e. the assertion text itself proves the grader left the
patched temp path and hit the real filesystem. Valid cases turn fail, `mismatches=8`, exit 1.

## (b) Every case fed the reference regex — DETECTED

Mutation (`m2-every-case-reference`): module-level `REF = line_rx(ip(), date())` (= the
`reference-lenient-days` regex) + `p.write_text(regex)` → `p.write_text(REF)`.

```
$ python3 plans/regex_log_probe.py --lane .        (m2-every-case-reference)
case=reference-lenient-days predicted=pass observed=pass match=yes assertion='-' …
…
case=regex-file-absent predicted=fail observed=fail match=yes assertion='Regex file <tmp>/absent-regex.txt does not exist' …
cases=24 observed_pass=23 observed_fail=1 mismatches=15
rc=1
```

15 of the 16 fail-predictions flip to pass. The one survivor is `regex-file-absent`: `mode=="absent"`
never writes the file (it names a second file, `absent-regex.txt`, and relies on absence), so that case
is structurally insensitive to its `regex` argument. That is a coverage quirk of the frozen harness, not
a detection failure — the count still moves 15 ≫ 0 and the exit code is 1.

## (c) One prediction flipped — DETECTED

Mutation (`m3-flip-one-prediction`): `padded-file` prediction `"pass"` → `"fail"`.

```
$ python3 plans/regex_log_probe.py --lane .        (m3-flip-one-prediction)
case=padded-file predicted=fail observed=pass match=NO assertion='-' requirement='the file is read and stripped'
cases=24 observed_pass=8 observed_fail=16 mismatches=1
rc=1
```

`mismatches=1`, exit 1, and the single `match=NO` line names the flipped case.

## (d) One-byte tamper of the copied grader — REFUSED, exit 2

Mutation (`m4-tamper-one-byte`): in `expected_dates`, `"1999-03-05"` → `"1999-03-06"` (a *semantic*
single-byte tamper, not junk in a comment). Forensics: same length, exactly one differing byte.

```
byte_diffs=[(3403, '5', '6')]   len_equal=True
$ sha256sum m4-tamper-one-byte/corpus/evidence/round36/tb2-regex-log/test_outputs.py
22a630148cd15c11a6d79bac620bc68c85b09209c3282cdcb2686b240fe21cb6  …
$ python3 plans/regex_log_probe.py --lane .        (m4-tamper-one-byte)
REFUSE grader digest 22a630148cd15c11a6d79bac620bc68c85b09209c3282cdcb2686b240fe21cb6 != pinned 345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72
rc=2
```

Refusal happens before any case executes (stdout is that single line), and the reported digest equals the
independently computed `sha256sum` of the tampered file.

## (e) `mkdtemp` path leaks again (`Amendment 1`'s `.replace(d, "<tmp>")` reverted) — DETECTED

Mutation (`m5-tmp-path-leaks`): delete `.replace(d, "<tmp>")` from the assertion-text line.

Two consecutive runs of the same unmodified-except-m5 tree:

```
$ diff logs/m5-run1 logs/m5-run2
21,22c21,22
< … assertion='Regex in /tmp/tmpprxxpdj7/regex.txt is invalid: missing ), unterminated subpattern at position 0' …
< … assertion='Regex file /tmp/tmpmblo4hsf/absent-regex.txt does not exist' …
---
> … assertion='Regex in /tmp/tmppia2k3i3/regex.txt is invalid: missing ), unterminated subpattern at position 0' …
> … assertion='Regex file /tmp/tmp4fuvvs43/absent-regex.txt does not exist' …
DIFF_EXIT=1   (4 differing lines)
```

Both runs are `mismatches=0`, `rc=0` — the verdicts are identical; only the *receipt text* differs. The
committed receipt differs from the mutated run in the same 4 lines, so the C2 counter's W5
"fresh run byte-equal to the receipt" fails on this mutant. Amendment 1's scrub is therefore load-bearing,
and W5 is a real detector of exactly this regression (not a formality).

## Bonus integrity finding (beyond the assigned five): the source pin does not cover the code that runs

The captured grader lives beside a gitignored `__pycache__/`, and the probe loads it through
`importlib.util.spec_from_file_location` + `exec_module`. `SourceFileLoader` validates the pyc by
**source mtime+size**, not by content (PEP 552 timestamp mode is the default). So a poisoned pyc with a
forged header executes while the source digest pin still passes.

```
$ python3 pyc_probe.py
m6-pyc-substitution     rc=1  src_sha_unchanged=345c3bd09ab6  cases=24 observed_pass=24 observed_fail=0 mismatches=16
m6ctl-pyc-stale-header  rc=0  src_sha_unchanged=345c3bd09ab6  cases=24 observed_pass=8  observed_fail=16 mismatches=0
forged_pyc_header mtime=1792976100 size=3730 | genuine_source mtime=1792976100 size=3730
```

`m6` replaces `__pycache__/test_outputs.cpython-314.pyc` with an always-pass grader and forges bytes 8-15
of the pyc header to the genuine source's mtime+size. The printed pin is still `345c3bd0…` (unchanged),
yet every case passes: the probing instrument reports 24/24 pass with `mismatches=16`. The `m6ctl`
control (same poison, header left stale) behaves exactly like `m0`, proving the effect is the header
forgery and not the mere presence of the file.

This is live in the lane today — the capture dir already holds six valid-header caches from sibling probe
runs (read-only check, `git check-ignore` confirms they are ignored so `--require-clean-tree` is unaffected):

```
source size=3730 mtime=1792976100
test_outputs.cpython-311.pyc      flags=0 … VALID_FOR_CURRENT_SOURCE=True
test_outputs.cpython-312.pyc      flags=0 … VALID_FOR_CURRENT_SOURCE=True
test_outputs.cpython-313.pyc      flags=0 … VALID_FOR_CURRENT_SOURCE=True
test_outputs.cpython-313.opt-1.pyc flags=0 … VALID_FOR_CURRENT_SOURCE=True
test_outputs.cpython-314.pyc      flags=0 … VALID_FOR_CURRENT_SOURCE=True
test_outputs.cpython-314.opt-1.pyc flags=0 … VALID_FOR_CURRENT_SOURCE=True
```

**Operable repair, demonstrated** (`pyc_fix.py`, advisory — not applied, `plans/` is the L1's) — load the
already-pinned bytes with `compile()`/`exec` into a real module namespace, so no cache entry is read or
written:

```python
import types as _types
src = pathlib.Path(mod_path).read_bytes()
mod = _types.ModuleType("tb2_regex_log_grader")
mod.__file__ = str(mod_path)
exec(compile(src, str(mod_path), "exec"), mod.__dict__)
```

```
$ python3 pyc_fix.py        (m7-source-exec-repair, forged pyc from m6 planted in the same tree)
m7-source-exec-repair  rc=0  cases=24 observed_pass=8 observed_fail=16 mismatches=0
two_runs_byte_equal=True   stderr=''
pycache_after_runs=['test_outputs.cpython-314.pyc']   (only the planted forged file; nothing written)
matches_committed_receipt=True
```

Implementation note for whoever applies it: `exec` into a plain dict breaks the harness's
`mod.Path = …` patch (the function's `__globals__` is that dict, not `mod`); the first m7 attempt did
exactly that and regressed to `mismatches=8` with `Regex file /app/regex.txt does not exist`. The
`types.ModuleType(...)` form preserves the existing patch line unchanged.

## Verdict per assigned mutant

| mutant | required signal | observed | detected |
|---|---|---|---|
| (a) m1 path patch broken | valid cases fail, `mismatches>0`, exit 1 | `mismatches=8`, `rc=1`, 8/8 pass-cases red on `/app/regex.txt does not exist` | yes |
| (b) m2 all-reference | `mismatches>0`, exit 1 | `mismatches=15`, `rc=1` (1 structurally regex-blind case) | yes |
| (c) m3 flip one prediction | `mismatches=1` | `mismatches=1`, `rc=1` | yes |
| (d) m4 one-byte tamper | REFUSE, exit 2 | `REFUSE … 22a63014… != 345c3bd0…`, `rc=2` | yes |
| (e) m5 tmp-path leak | receipts differ between two runs | 4 differing lines across two `rc=0`/`mismatches=0` runs | yes |

## Evidence retained

`build/R36ProbeHarnessMut/`: `mutate.py`, `pyc_probe.py`, `pyc_fix.py`, `mini/`, `m0-unmodified/`,
`m1-path-patch-broken/`, `m2-every-case-reference/`, `m3-flip-one-prediction/`, `m4-tamper-one-byte/`,
`m5-tmp-path-leaks/`, `m6-pyc-substitution/`, `m6ctl-pyc-stale-header/`, `m7-source-exec-repair/`,
`logs/*.txt`. All writes are inside this directory; `git status --porcelain` in the lane shows nothing
from this seat outside `.ufo/waves/round-36/build/`. No `/tmp/k36-*` fixture was created by this seat.

## Risks / limits (advisory, for the L1)

1. `mode=="absent"` never writes its file, so 1 of 24 cases cannot detect a regex-selection mutation.
   Nothing to repair for the frozen battery; it just bounds m2-style detections at 15.
2. The pyc-substitution gap above is real for any run of the *lane* probe, and both the probe's
   `GRADER_SHA256` and the counter's `PROBE_SHA256` (`plans/round36_c2_verify.py:41`) pass through it.
   A wave-2 mutation seat that copies `test_outputs.py` and replants a forged cache in
   `corpus/evidence/round36/tb2-regex-log/__pycache__/` would fool W5's byte-equality of the receipt.
   Suggest the L1 either apply the m7 loader or add a `__pycache__`-absence check to W5.
3. Every probe run appends a pyc to `corpus/evidence/round36/tb2-regex-log/__pycache__/` (six tags
   already). Gitignored, so `--require-clean-tree` is unaffected; the m7 loader stops the accumulation.

Checks main should run after integration: `python3 plans/regex_log_probe.py --lane .` on a clean clone
(expect `cases=24 observed_pass=8 observed_fail=16 mismatches=0`, exit 0, byte-equal to the receipt),
then `python3 plans/round36_c2_verify.py --lane .`.

VERDICT: harness-mutants-5/5
