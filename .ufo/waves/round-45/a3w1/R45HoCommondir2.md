# R45HoCommondir2 — held-out commondir/gitfile/worktree-metadata attack on the landed fence (round-45 a3w1)

Mutation-tester seat, kengaku round 45 attempt-3 wave a3w1. Four hostile modules in the f7/f1 contract
(`FIXTURES = [{'fid','tool','expect','defects','build'}]`, `build(ctx, d)` fills empty `d`, returns argv tail;
outside artefact under `pathlib.Path(d).parent`) were built with the frozen round-44 builder and run against
THE LANED `plans/fixture_fence.py` through the frozen counter's own `build_module`/`run_fence`
(`plans/round45_c1_verify.py`), i.e. the exact detector of `PREDICATE C1 pass`, under the mandated envelope.

- Lane tip measured: `master` = `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (clean shared clone,
  `git status --porcelain` empty). `plans/fixture_fence.py` sha256 `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`
  (identical before and after every run).
- Provenance: this seat's w2 incarnation was killed 2026-10-26 23:57; its scratch and any w2 files were NOT
  read or cited — scratch `/fast/scratch/hyaku/kengaku-r45/R45HoCommondir2` was wiped (one `sudo rm -rf` of my
  own seat dir only; leftovers were `d--x--x--x` bwrap artefacts) and every measurement below was re-run fresh.
- No tool installed (none needed); no pacman transaction.

## 1. Baseline (pristine fence, clean clone) — detector valid

Command: `envelope.sh "$S/env" /usr/bin/python3 "$S/lane/plans/round45_c1_verify.py" --lane "$S/lane" --work "$S/w" --jobs 8`
(receipt `receipts/baseline-c1-pass.out`, sha256 `a4413e7f281ddff2614fa623a129988fdade31c6202efea4c6fcd3100ed9ba48`)

```
ENVELOPE start 00:37:22 cwd=/home/vgpnk/Projects/shokunin
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 00:37:27 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

C1's claim reproduces on the clean clone; a baseline failure would have made everything below inconclusive.

## 2. Held-out run

Command: `K45_KEEP_STRACE="$S/keep" envelope.sh "$S/env" /usr/bin/python3 <mydir>/driver.py "$S/lane" "$S/w/root" <mydir>/modules`
(receipt `receipts/heldout-modules.out`, sha256 `5bf474c11aeebdd1877dc73f2a8eeeb40d4cda0dde4034549f315884da14aac1`)

```
ENVELOPE start 00:39:14 cwd=/home/vgpnk/Projects/shokunin
FENCE-COPY sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
FENCE-RUN g1_cdrel.py g1-cd-rel BREACH opens=0 -- repo/.git/commondir present (store redirect)
FENCE-RUN g2_gitfile.py g2-gitfile-pad BREACH opens=0 -- lane/.git/.git is a file (gitdir redirect), not a directory
FENCE-RUN g3_wtmeta.py g3-wtmeta-out ADMIT opens=0
FENCE-RUN g4_cdrel_hidden.py g4-cd-hidden ADMIT opens=32
HELDOUT g1_cdrel.py clean fixtures=1 admitted=0 hung=0 opens=0
HELDOUT g2_gitfile.py clean fixtures=1 admitted=0 hung=0 opens=0
HELDOUT g3_wtmeta.py LEAKED fixtures=1 admitted=1 hung=0 opens=0
HELDOUT g4_cdrel_hidden.py LEAKED fixtures=1 admitted=1 hung=0 opens=32
ENVELOPE end 00:39:16 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

## 3. Module-by-module verdicts

| module (sha256) | vector | expected | observed | verdict |
|---|---|---|---|---|
| `g1_cdrel.py` f2d4370f…b6d14 | commondir RELATIVE `../../../g1-out/.git` resolved against the gitdir, escaping d via `..` | refused at collection, opens=0 | `BREACH opens=0 -- repo/.git/commondir present (store redirect)` | killed (clean) |
| `g2_gitfile.py` c43556e6…63f0a | `.git` FILE, `gitdir:   ../../g2-out/.git` relative + space-padded | refused at collection, opens=0 | `BREACH opens=0 -- lane/.git/.git is a file (gitdir redirect)` | killed (clean) |
| `g3_wtmeta.py` bd0414a7…67edd | real `git worktree add --detach <d.parent>/g3-wt` → `repo/.git/worktrees/g3-wt/` metadata pointing outside d | admitted (walk never enters `.git`) | `ADMIT opens=0` | **admitted (survivor)** |
| `g4_cdrel_hidden.py` 0f8aee44…c65af | same relative commondir escape as g1, hidden at `repo/.git/modules/escape/.git/commondir`, `--lane` names it | admitted AND fence reads outside d | `ADMIT opens=32` | **admitted + read (survivor, defect)** |

## 4. The g4 defect, in detail (the coverage finding)

Fixture: `d/repo` honest; hidden store `d/repo/.git/modules/escape` (never walked — fact 4 prunes every
`.git` dir) whose `.git/commondir` is one line:

```
../../../../../../g4-out/.git
```

i.e. git's common dir — config, refs, objects — resolves to `<build root>/g4-out/.git`, OUTSIDE d, exactly
by relative resolution against the gitdir (vector a). `--lane repo/.git/modules/escape` passes fact 2
(resolves inside d). Fence-view answers (measured on the built fixture with the fence's own ceiling):

```
rev-parse --show-toplevel      -> <d>/repo/.git/modules/escape            (inside d  -> leg passes)
rev-parse --absolute-git-dir   -> <d>/repo/.git/modules/escape/.git       (inside d  -> leg passes)
rev-parse --git-common-dir     -> <build root>/g4-out/.git                (OUTSIDE d -> never asked)
```

The fence never asks for the common dir, so it admits the fixture, and its own git children open the outside
store while deciding (strace receipt `receipts/strace-g4.txt`, sha256 `da00bfc2…95b57`; 13 of the 32 are
opens of `g4-out/.git/config` by the fence's `git -C <lane>` children, e.g. pid 8):

```
8 openat(AT_FDCWD<…/f000/repo/.git/modules/escape>, "…/g4-out/.git/config", O_RDONLY) = 3</…/g4-out/.git/config>
```

Independent recount with the counter's own open-classification rule: `recount outside opens=32` (matches).
This contradicts both halves of the fence's advertisement (docstring, `plans/fixture_fence.py:1-14`):
"admit only a fixture whose git store, discovered repos and argv stay inside `d`" (the store's config/refs/
objects live outside d) and "the fence's whole process tree must never open a path under the build scratch
outside `d`" (32 successful opens). Note the frozen C1 predicate itself is not contradicted — held-out
modules are "reported, not part of the predicate" (`plans/round-45-claims.md` §C1, "Held-out attack"). This
is a coverage finding for the L1: the f7 fix (refuse any walked `.git/commondir`) closes the absolute-redirect
shape only; a relative one hidden below a pruned `.git` reopens the round-44 defect (f7's own docstring:
"`rev-parse --show-toplevel` and `--absolute-git-dir` both answer inside d").

## 5. g3 nuance and g2 cosmetic note

- **g3 (admitted, opens=0).** The repo's store stays inside d; only `worktrees/g3-wt/{gitdir,commondir,HEAD}`
  point at the outside checkout (`gitdir` content `…/modules-g3_wtmeta/g3-wt/.git`, checkout exists). The
  fence never inspects `.git/worktrees/`, so my assigned hostile shape is admitted. Honest reading: the
  written contract sentence (store/repos/argv inside d) is arguably satisfied, so this is a robustness/coverage
  gap, not a contradiction of the letter of the advertisement — but the "discovered repo" of this fixture does
  have a worktree outside d that no leg looks at. Reported, not judged.
- **g2 (killed).** The refusal reason string doubles the component: `lane/.git/.git is a file` for the file at
  `d/lane/.git` (fact 4 prints `f"{p.relative_to(d)}/.git is a file"` where `p` already ends in `.git`).
  Behavior correct, message misleading — cosmetic, for the L1 only.

## 6. Restoration / integrity evidence

No lane byte was mutated at any point (the mutants are my held-out modules; the fence ran pristine). After
both runs, on the same clone:

```
git -C "$S/lane" rev-parse HEAD   -> fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc   (unchanged)
git -C "$S/lane" status --porcelain -> (0 lines)
sha256 lane/plans/fixture_fence.py   -> ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6 (before = after)
sha256 lane/plans/round45_c1_verify.py -> 7745eb0a4bdf281acf46cde6e6a4c280a17d02f9668ea309d1020fff9ce1150d
sha256 lane/plans/round44_c1_verify.py -> 6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad (= PINS entry)
```

Both envelopes report `local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`; neither
run exited 4/INVALID. Scratch cleanup: `python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r45
R45HoCommondir2 "$S"` runs after this report is written.

## 7. Receipts (all under 1 MiB, in my subdir)

| file | bytes | sha256 |
|---|---|---|
| `receipts/baseline-c1-pass.out` | 11634 | `a4413e7f281ddff2614fa623a129988fdade31c6202efea4c6fcd3100ed9ba48` |
| `receipts/heldout-modules.out` | 1652 | `5bf474c11aeebdd1877dc73f2a8eeeb40d4cda0dde4034549f315884da14aac1` |
| `receipts/strace-g1.txt` | 28117 | `10caee90…eec511` |
| `receipts/strace-g2.txt` | 25856 | `8f044cae…a174d5` |
| `receipts/strace-g3.txt` | 59742 | `ab26580a…a72e021` |
| `receipts/strace-g4.txt` | 86427 | `da00bfc2…95b57` |

Driver + modules: `driver.py` 58fdcf96…71923, `modules/g1_cdrel.py` f2d4370f…b6d14, `modules/g2_gitfile.py`
c43556e6…63f0a, `modules/g3_wtmeta.py` bd0414a7…67edd, `modules/g4_cdrel_hidden.py` 0f8aee44…c65af.

Counting for the verdict line: n = 4 modules tested; k = 2 with a fixture ADMITTED by the landed fence
(g3, g4); r = 1 whose deciding process tree opened a path outside d (g4 — inside the admitted pair; g3 made
0 outside opens; g1/g2 refused with 0 opens).

VERDICT: commondir2-modules-4-admitted-2-read-1
