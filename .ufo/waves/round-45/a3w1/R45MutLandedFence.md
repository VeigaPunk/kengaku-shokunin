# R45MutLandedFence — a3w1 mutation probe

## Setup and pristine control

Measured clone tip: `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`git -C "$S/lane-src" rev-parse HEAD`; output `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc`). The original fence was SHA-256 `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`; the scratch clone's pristine fence had the same hash. Fifteen independently edited copies were compiled and run; frozen counter and refusal/honest modules remained unmodified. The mutation table names the exact single edit and the counter-observed detector.

Pristine command (all commands use the envelope):

```sh
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" /usr/bin/python3 "$S/lanes/m00_baseline/plans/round45_c1_verify.py" --lane "$S/lanes/m00_baseline" --work "$S/work/m00" --jobs 8
```

Receipt: `R45MutLandedFence/m00_baseline.txt`. Output: `PINS total=33 mismatched=0`; `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`; `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; `CALIBRATION advertised=10 contradicted=0`; `PREDICATE C1 pass`. Envelope: `ENVELOPE start 00:29:57 cwd=/home/vgpnk/Projects/shokunin`; `ENVELOPE end 00:30:04 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`.

## Mutant results

Each run used the same bounded counter command shape, substituting its lane and scratch work directory:

```sh
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" /usr/bin/python3 "$S/lanes/<mutant>/plans/round45_c1_verify.py" --lane "$S/lanes/<mutant>" --work "$S/work/<mutant>" --jobs 4
```

Full raw output for each measured command is in the correspondingly named receipt below. Each failed predicate had exit 1; each survivor had exit 0. The output columns are the observed counter summary (not inferred). `caught` means a refusal went non-clean or honest fixture admission dropped, per the assignment.

| Mutant; one edit | Caught by / outcome | Observed output | Receipt |
|---|---|---|---|
| m01 `return p == d or p.is_relative_to(d)` → negate | **caught: honest set** | `HONEST fixtures=104 admitted=0 refused=104 ...`; predicate fail | `R45MutLandedFence/m01_flip_inside.txt` |
| m02 remove `.git`-file return in tree walk | **caught: f1_gitfile.py READ** | `REFUSAL f1_gitfile.py READ fixtures=1 admitted=0 hung=0 opens=6`; predicate fail | `R45MutLandedFence/m02_drop_gitfile_leg.txt` |
| m03 remove `commondir` refusal | **caught: f7_commondir.py LEAKED** | `REFUSAL f7_commondir.py LEAKED fixtures=3 admitted=3 hung=0 opens=71`; predicate fail | `R45MutLandedFence/m03_drop_commondir.txt` |
| m04 remove `re.MULTILINE` from include regex | **caught: f10_laneinclude.py LEAKED; f4_fifo.py READ** | `REFUSAL f10_laneinclude.py LEAKED fixtures=1 admitted=1 hung=0 opens=7`; `REFUSAL f4_fifo.py READ fixtures=1 admitted=0 hung=0 opens=1`; predicate fail | `R45MutLandedFence/m04_include_nomultiline.txt` |
| m05 remove `GIT_CEILING_DIRECTORIES` from `_git` env | **survived** | `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`; `HONEST fixtures=104 admitted=104 ...`; `PREDICATE C1 pass` | `R45MutLandedFence/m05_drop_ceiling.txt` |
| m06 swallow `_collect`'s `why` (`return why` → `return None`) | **caught: all refusals LEAKED** | `REFUSALS total=10 clean=0 leaked=10 read=0 hung=0 build_errors=0`; predicate fail | `R45MutLandedFence/m06_swallow_collect_reason.txt` |
| m07 omit `pathlib.Path(d).resolve()` | **survived** | `REFUSALS total=10 clean=10 ...`; `HONEST fixtures=104 admitted=104 ...`; `PREDICATE C1 pass` | `R45MutLandedFence/m07_drop_resolve_d.txt` |
| m08 remove escaping-directory-symlink return in walk | **survived** | `REFUSALS total=10 clean=10 ...`; `HONEST fixtures=104 admitted=104 ...`; `PREDICATE C1 pass` | `R45MutLandedFence/m08_drop_symlink_escape.txt` |
| m09 remove alternates-file refusal | **caught: f5_alternates.py LEAKED** | `REFUSAL f5_alternates.py LEAKED fixtures=1 admitted=1 hung=0 opens=0`; predicate fail | `R45MutLandedFence/m09_drop_alternates.txt` |
| m10 disable textual `core.worktree` check | **survived** | `REFUSALS total=10 clean=10 ...`; `HONEST fixtures=104 admitted=104 ...`; `PREDICATE C1 pass` | `R45MutLandedFence/m10_drop_worktree_text.txt` |
| m11 invert `_probe` top-level rc check (`!= 0` → `== 0`) | **caught: honest set** | `HONEST fixtures=104 admitted=0 refused=104 ...`; predicate fail | `R45MutLandedFence/m11_flip_toplevel_rc.txt` |
| m12 remove `.git`-above-fixture check | **survived** | `REFUSALS total=10 clean=10 ...`; `HONEST fixtures=104 admitted=104 ...`; `PREDICATE C1 pass` | `R45MutLandedFence/m12_drop_above_leg.txt` |
| m13 remove `_probe` absolute-git-dir probe | **survived** | `REFUSALS total=10 clean=10 ...`; `HONEST fixtures=104 admitted=104 ...`; `PREDICATE C1 pass` | `R45MutLandedFence/m13_drop_gitdir_probe.txt` |
| m14 lower config byte ceiling from 1 MiB to 256 B | **survived** | `REFUSALS total=10 clean=10 ...`; `HONEST fixtures=104 admitted=104 ...`; `PREDICATE C1 pass` | `R45MutLandedFence/m14_configcap_256.txt` |
| m15 lower walked-entry ceiling from 200,000 to 100 | **survived** | `REFUSALS total=10 clean=10 ...`; `HONEST fixtures=104 admitted=104 ...`; `PREDICATE C1 pass` | `R45MutLandedFence/m15_entrycap_100.txt` |

Every mutant receipt has `PINS total=33 mismatched=0`, reports its mutated fence SHA-256, and contains the full counter output plus envelope start/end. For all fifteen, envelope end reported `local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`; no run was invalidated. Start/end times: m01 00:30:33–00:30:47; m02 00:30:33–00:30:48; m03 00:30:33–00:30:49; m04 00:30:33–00:31:10; m05 00:30:33–00:30:48; m06 00:30:33–00:30:49; m07 00:30:33–00:30:48; m08 00:30:33–00:30:48; m09 00:30:33–00:30:49; m10 00:30:33–00:30:49; m11 00:30:33–00:30:47; m12 00:30:33–00:30:49; m13 00:30:33–00:30:48; m14 00:30:33–00:30:49; m15 00:30:33–00:30:49. See each named receipt for its literal `ENVELOPE start` and `ENVELOPE end` lines.

## Coverage findings from survivors

- m05: no current hostile fixture isolates repository discovery above the configured ceiling while the resulting repository remains otherwise describable/inside the fixture. Existing f6 is still refused by the parent `.git` / outside-toplevel checks.
- m07: current counter always supplies resolved fixture paths; no hostile case exercises unresolved `d` (for example, a symlinked fixture root).
- m08: no refusal module plants an escaping directory symlink in the collected fixture tree.
- m10: f2 still fails at `_probe`'s toplevel check, so the textual worktree-config scan has no isolated hostile case.
- m12: no fixture distinguishes the explicit parent `.git` check from the remaining Git probe checks.
- m13: no fixture makes the absolute git-dir probe uniquely necessary while the other repo/store checks and open detector remain clean.
- m14: no honest fixture has `.git/config*` in (256 B, 1 MiB]; this mutation did not reach the limit on current inputs.
- m15: no honest fixture tree has >100 entries; cap reduction did not reach the limit on current inputs.

## Restoration / integrity

Only scratch-clone copies of `plans/fixture_fence.py` were modified; the original lane file and scratch clone pristine copy both hash to `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6` (observed `sha256sum` output). Mutants were independent copies; the originals were never edited, so restoration is exact by non-mutation. Scratch test artifacts remain under `$S` pending operator cleanup; report receipts are under this seat's assigned subdirectory.

VERDICT: fence-mutants-caught-7/15
