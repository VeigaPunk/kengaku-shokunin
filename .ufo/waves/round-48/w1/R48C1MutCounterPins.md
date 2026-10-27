# R48C1MutCounterPins — C1 input-pin / inventory mutation probe

Axes named: **calibration** (R48-C1). This is a mutation-sensitivity probe of the committed round-46 C1 counter contract that R48-C1 stage 1 says the v3 counter extends; it does not evaluate or admit R48-C1 claimed work. `plans/round48_c1_verify.py` is absent at measured revision `a543d92083557dd9b33ee674e9b99b03411f80af`, so this seat could not test the future v3 counter itself.

Freeze check: stage-1 commit `a543d92083557dd9b33ee674e9b99b03411f80af` exists, timestamp `2026-10-27 06:53:29 -0300`; it is an ancestor of lane HEAD. Measurement began after that timestamp. The claims file at that commit freezes the C1 counter contract/deltas/controls/kill rule. All execution used a `git clone --shared` at exactly that revision under `/fast/scratch/hyaku/kengaku-r48/R48C1MutCounterPins/lane`; `git rev-parse --show-toplevel` returned that directory. No lane production bytes were written.

## Source opened

URL: `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round46_c1_verify.py` (read from the identical frozen-revision clone); access date: 2026-10-27. Located quote (line 123 onward): “Legs, every input pinned below by digest (PINS).” The counter’s `pin_issues` checks pinned digests and flags extra refusal/sealed modules as `:unpinned`; predicate logic fails on pin issues and rechecks pins after legs.

## Commands and observations

Environment: `/usr/bin/bwrap` present (0.13.1), `/usr/bin/strace` present (7.2), Python 3.14.8. Pristine pin manifest: **65/65** expected digests matched.

Detector command for each run (same command on pristine, each mutant and restored bytes):

```sh
python3 plans/round46_c1_verify.py --lane . --work /fast/scratch/hyaku/kengaku-r48/R48C1MutCounterPins/work --jobs 8
```

Pristine baseline output (exit 0):

```text
PINS total=65 mismatched=0
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=32 contradicted=0
PREDICATE C1 pass
```

Mutants were applied only in the scratch clone and restored before the next case:

| Mutant | Scratch mutation | Observed detector output / exit | Verdict |
|---|---|---|---|
| M1 | Appended bytes to pinned `plans/battery42/a_class.py` | `PINS total=65 mismatched=1 first=plans/battery42/a_class.py`; `REASON pins=1,pins-after=1`; `PREDICATE C1 fail`; exit 1 | Killed |
| M2 | Appended bytes to pinned `plans/sealed46/s_packed_refs.py` | `PINS total=65 mismatched=1 first=plans/sealed46/s_packed_refs.py`; `REASON pins=1,pins-after=1`; fail; exit 1 | Killed |
| M3 | Deleted pinned `plans/refusals46/f11_cr_include.py` | `PINS total=65 mismatched=1 first=plans/refusals46/f11_cr_include.py`; refusal total 19; `REASON pins=1,pins-after=1,refusals-total=19!=20`; fail; exit 1 | Killed; missing-file input was reported rather than crashing |
| M4 | Added unpinned module to `plans/refusals46/` | `PINS total=65 mismatched=1 first=plans/refusals46/f99_pinprobe_extra.py:unpinned`; refusal total 21; fail; exit 1 | Killed |
| M5 | Added an honest battery module by copying an existing module to `plans/battery44/` | `PINS total=65 mismatched=0`; `HONEST fixtures=107 admitted=107`; `REASON honest-not-admitted`; fail; exit 1 | Killed (inventory count binding) |
| M6 | Appended bytes to pinned builder `plans/round44_c1_verify.py` | `PINS total=65 mismatched=1 first=plans/round44_c1_verify.py`; `SETUP the round-44 counter (builder) is not at its pinned digest`; exit 2 | Killed (setup guard) |
| M7 | Appended bytes to pinned COPY-row source `plans/refusals45/f1_gitfile.py` | `PINS total=65 mismatched=1 first=plans/refusals45/f1_gitfile.py`; `COPY f1_gitfile.py DIFFERS`; fail; exit 1 | Killed |
| M8 | Swapped contents of pinned `plans/battery44/u7_twin_a.py` and `u7_twin_b.py` | `PINS total=65 mismatched=2 first=plans/battery44/u7_twin_a.py`; `REASON pins=2,pins-after=2`; fail; exit 1 | Killed |

Restored-bytes run (exit 0) reproduced the pristine summary and `PREDICATE C1 pass`. M8’s first driver attempt accidentally tested a one-sided duplicate; it was not counted as the swap result. The corrected true swap above was run and caught. That corrected run returned exit 1 as expected; the shell stopped on that expected nonzero, after which both files were explicitly restored.

## Restoration evidence

Restored SHA-256 values match original pinned digests:

- `plans/battery42/a_class.py`: `eef02b5df0a8b5e7e558956eaf3d5fca6fa5701872f11632d5327717def8f1bb`
- `plans/sealed46/s_packed_refs.py`: `3f7d4e08bc7c2c5ba4a42b6ac376344942cc70d2b23ef6873f4f1dafccc08fda`
- `plans/refusals46/f11_cr_include.py`: `33f11fd88ba912f2df864abbb6a6bdfe61d5923940da11dd6687c5fb210c9176`
- `plans/round44_c1_verify.py`: `6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad`
- `plans/refusals45/f1_gitfile.py`: `bac0df8aa55e35de2964f0e98a8c461aa6eeeba9daa2f18ca113a383f24a4c8d`
- `plans/battery44/u7_twin_a.py`: `8c322cf38293f34b82669734e793e75f8cb6d82071bdb7ac854e34bf387e66e5`
- `plans/battery44/u7_twin_b.py`: `6bee837959584e12577647fb280d1ea50228edf03106868ec2c4cb11087f4d89`

Temporary added modules were removed; missing refusal module restored. Final clone `git status --porcelain` was empty and HEAD remained `a543d92083557dd9b33ee674e9b99b03411f80af`. The scratch tree was removed after report creation.

Limits: this measures only the round-46 counter in the frozen-base clone, not the uncommitted R48 v3 counter. Mutants cover pinned bytes, missing input, extra hostile inventory, extra honest inventory, builder pin, copy-row source, and two-file permutation; they do not test all possible digest/inventory defects. No R48-C1 or R48-C2 admission is claimed.

VERDICT: **8/8 corrected mutants killed; pristine and restored controls pass.** The committed round-46 detector’s pins and fixed honest/hostile inventory totals detect each tested mutation. R48-C1 v3 remains untested pending its committed stage-2 counter.
