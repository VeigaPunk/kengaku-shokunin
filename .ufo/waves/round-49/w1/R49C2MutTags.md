# R49C2MutTags — per-requirement-tag mutation probe

**Axes:** coverage (R49-C2). **Revision measured:** `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93` (clean, detached scratch clone; `git status --porcelain` count `0`). The lane freeze commit exists, is an ancestor of lane `HEAD` (`af88aab193e6034cb9b386472064e3c18fa90128`), and its commit time is `2026-10-28T09:14:40-03:00`, before these measurements. Its tree contains `plans/round-49-claims.md` and the frozen C2 probe, capture, dry table and receipt.

## Method

The bounded detector was the captured `test_fibonacci_polyglot` function, invoked via the frozen probe's `run_case` in its bubblewrap sandbox (two grader invocations per case, recording first and regrade verdicts). For each tag, a private scratch copy of the captured grader was measured pristine → mutated → restored; restoration was byte-exact and the restored detector output equalled pristine. Frozen violating cases were used for five tags; scratch-authored violating cases cover the two tags that the frozen table left unexercised. Mutants remove or weaken only the corresponding decision (the C-build mutant bypasses its dependent C execution too, since no binary exists when build is omitted).

The pristine capture hash in every row was `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec`. Exact observed detector verdicts and mutation/restoration hashes:

| Tag / violating case | Mutant (scratch grader copy) | Pristine → mutant → restored | Mutant SHA-256 | Verdict |
|---|---|---|---|---|
| `single-file` / frozen `extra-file` | Remove exact-list assertion (`assert True`) | `F/F → P/P → F/F` | `9826dad2901923e487c698ae2e15b4687c21a0aedbc700198aaa07c265519a24` | KILLED |
| `python-run` / frozen `c-only` | Bypass Python invocation/output check | `F/F → P/F → F/F` | `d7becc23a7adaa2dddcf4c3c7101499742edf16fb3047cc4d1dc1b1456a6e5cc` | KILLED |
| `c-build` / frozen `python-only` | Bypass gcc build and dependent C execution check | `F/F → P/P → F/F` | `972daf863a4d2771e10c42dd43417515f37717e942d9fd522ae68d546c201342` | KILLED |
| `fib-kth` / frozen `wrong-value` | Remove expected-value assertion | `F/F → P/F → F/F` | `6a73e59506095f5461f65ad4e0773d0bcef541aa3d1a5b8ac8706aacb2c89ed1` | KILLED |
| `stdout-only` / frozen `value-plus-line` | Compare only each output's first line | `F/F → P/F → F/F` | `82e34342828ab236da82e37f8ad5b173577b1a2ea1dbc1e49a4183855e2565b9` | KILLED |
| `both-print` / scratch `mut-both-print` (Python runs successfully but prints no value; C prints expected value) | Drop Python side of joint output assertion | `F/F → P/F → F/F` | `5dfe07233d5fcbbaff031d685de7b6c293de1ff2f4b29172c5e368a2893618ab` | KILLED |
| `toolchain` / scratch `mut-toolchain` (oracle under host gcc/Python, versions differ from instruction) | Change executable names to `/usr/bin/gcc` and `/usr/bin/python3` | `P/F → P/F → P/F` | `4ed09dbd04488afaf48a55bb2260cb3753869dd5c19b107d46cba15f32dedd56` | SURVIVED — no version check exists |

In all seven rows the restored grader hash was exactly the pristine hash above (`exact=True`), and restored output matched pristine. Existing frozen cases matched their round-46 receipt's first verdict. The host tool versions observed before the run were `gcc (GCC) 16.2.1 20260810` and `Python 3.14.8`, not the instruction's gcc 13.2.0 / Python 3.12.3; nevertheless the grader accepts the oracle case under those versions. The toolchain mutant therefore survives for a substantive reason: the captured grader invokes tools by name and does not enforce versions. This is a coverage finding, not a change to the frozen contract.

The run's per-tag output was:

```text
TAG single-file CASE extra-file EXPECT_PRISTINE=F
  pristine=F/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec
  mutant=P/P sha256=9826dad2901923e487c698ae2e15b4687c21a0aedbc700198aaa07c265519a24
  restored=F/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec exact=True
  verdict=KILLED baseline_ok=True restored_ok=True mutant_flip=True
TAG python-run CASE c-only EXPECT_PRISTINE=F
  pristine=F/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec
  mutant=P/F sha256=d7becc23a7adaa2dddcf4c3c7101499742edf16fb3047cc4d1dc1b1456a6e5cc
  restored=F/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec exact=True
  verdict=KILLED baseline_ok=True restored_ok=True mutant_flip=True
TAG c-build CASE python-only EXPECT_PRISTINE=F
  pristine=F/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec
  mutant=P/P sha256=972daf863a4d2771e10c42dd43417515f37717e942d9fd522ae68d546c201342
  restored=F/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec exact=True
  verdict=KILLED baseline_ok=True restored_ok=True mutant_flip=True
TAG fib-kth CASE wrong-value EXPECT_PRISTINE=F
  pristine=F/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec
  mutant=P/F sha256=6a73e59506095f5461f65ad4e0773d0bcef541aa3d1a5b8ac8706aacb2c89ed1
  restored=F/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec exact=True
  verdict=KILLED baseline_ok=True restored_ok=True mutant_flip=True
TAG stdout-only CASE value-plus-line EXPECT_PRISTINE=F
  pristine=F/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec
  mutant=P/F sha256=82e34342828ab236da82e37f8ad5b173577b1a2ea1dbc1e49a4183855e2565b9
  restored=F/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec exact=True
  verdict=KILLED baseline_ok=True restored_ok=True mutant_flip=True
TAG both-print CASE mut-both-print EXPECT_PRISTINE=F
  pristine=F/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec
  mutant=P/F sha256=5dfe07233d5fcbbaff031d685de7b6c293de1ff2f4b29172c5e368a2893618ab
  restored=F/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec exact=True
  verdict=KILLED baseline_ok=True restored_ok=True mutant_flip=True
TAG toolchain CASE mut-toolchain EXPECT_PRISTINE=P
  pristine=P/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec
  mutant=P/F sha256=4ed09dbd04488afaf48a55bb2260cb3753869dd5c19b107d46cba15f32dedd56
  restored=P/F sha256=b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec exact=True
  verdict=SURVIVED baseline_ok=True restored_ok=True mutant_flip=False
```

## Commands, source and limits

Exact commands (paths shortened only by shell variables shown in each command):
```sh
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
git -C "$L" cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C "$L" log -1 --format='%H%n%an %ae%n%cI%n%s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C "$L" merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD
git -C "$L" ls-tree -r --name-only 9d2900af41e4d1fc6022eff99010436fde6dbd93
mkdir -p /fast/scratch/hyaku/kengaku-r49/R49C2MutTags && export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C2MutTags && echo "TMPDIR=$TMPDIR" && df -h /fast/scratch | tail -1 && command -v gcc cc python3 git && gcc --version | head -1 && python3 --version
D=/fast/scratch/hyaku/kengaku-r49/R49C2MutTags
git clone --quiet --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane" && git -C "$D/lane" checkout --quiet --detach 9d2900af41e4d1fc6022eff99010436fde6dbd93 && T=$(git -C "$D/lane" rev-parse --show-toplevel) && echo "toplevel=$T" && [ "$T" = "$D/lane" ] && echo TOPLEVEL-OK && git -C "$D/lane" rev-parse HEAD && git -C "$D/lane" status --porcelain | wc -l && sha256sum "$D/lane/plans/polyglot_c_py_probe.py" "$D/lane/plans/round46_c3_verify.py" "$D/lane/corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt" "$D/lane/corpus/evidence/round46/polyglot-c-py-probe.txt" "$D/lane/corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py"
command -v bwrap || true; test -x /usr/bin/bwrap && echo BWRAP-EXECUTABLE || echo BWRAP-MISSING; test -r /fast/scratch/hyaku/kengaku-r49/R49C2MutTags/lane/corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py && echo CAPTURE-READABLE; sha256sum /fast/scratch/hyaku/kengaku-r49/R49C2MutTags/lane/corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py
export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C2MutTags; python3 /fast/scratch/hyaku/kengaku-r49/R49C2MutTags/tag_mutation.py
```
Freeze outputs: commit type `commit`, author `kengaku-shokunin`, commit time `2026-10-28T09:14:40-03:00`, ancestor check `YES`; clone `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93`, top-level `/fast/scratch/hyaku/kengaku-r49/R49C2MutTags/lane`, `TOPLEVEL-OK`, clean count `0`.
Procedural limit: clone checkout occurred before its top-level assertion; subsequent reads confirmed the expected scratch toplevel and frozen `REV`, and no git mutation followed. All grader mutants and restorations were ordinary writes to per-tag cap copies under the scratch root, not to the lane or clone.

The first detector launch failed before any case ran (`AttributeError: 'NoneType' object has no attribute '__dict__'`) because the scratch import omitted registration in `sys.modules`; the scratch script was corrected, then the command above completed with exit 0. No package/counter result is claimed. Limits: host tool versions stand in for the pinned image versions; the `toolchain` mutant survives; the C2 admission, V14 floor and any stage-3 receipt are outside this seat's finding.

Source basis: captured S166 `test_outputs.py`, local capture `corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py` (SHA-256 above), with source metadata URL `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py`, access date 2026-10-27. Located quote at line 44 (8 words): `assert python_out == expected and c_out == expected, (`. No external URL was opened by this seat; quote and date are from the lane's pinned source metadata.

Cleanup command after report creation: `test -f /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C2MutTags.md && rm -rf /fast/scratch/hyaku/kengaku-r49/R49C2MutTags && test ! -e /fast/scratch/hyaku/kengaku-r49/R49C2MutTags && echo SCRATCH_REMOVED && test -f /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C2MutTags.md && echo REPORT_PRESENT`; observed `SCRATCH_REMOVED` and `REPORT_PRESENT`.

**VERDICT: 6/7 tag mutants killed; `toolchain` survived because no version-enforcement check exists. Coverage finding only; no R49-C2 admission claim.**
