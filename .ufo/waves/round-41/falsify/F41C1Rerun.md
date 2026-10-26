# F41C1Rerun — C1 re-measure at the round's tip + battery load-bearing table

Seat: executor, round 41 wave 2 (falsify). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, measured claim tip
`3d0058fbde484c9d6c23fd997d9ee09a0663bcdb` (also current lane HEAD `d7c7789575`). Frozen counter untouched:
`plans/round41_c1_verify.py` sha256 `8835a94b0ad62dc1f58c861e2025b7c4bc8c0b936c202c64e01bc8b43f53eaa8`, matching
`.ufo/waves/round-41/claims/frozen-digests.txt`. Receipts: `.ufo/waves/round-41/falsify/F41C1Rerun/`.

## Setup (clean `--no-local` clone, envelope on every run)

```
S=/fast/scratch/hyaku/kengaku-r41/F41C1Rerun; export TMPDIR="$S"
git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel   -> /fast/scratch/hyaku/kengaku-r41/F41C1Rerun/lane
git -C "$S/lane" checkout -q --detach 3d0058fbde484c9d6c23fd997d9ee09a0663bcdb
git -C "$S/lane" status --porcelain | wc -l  -> 0
sha256sum lane/plans/tip_receipts.py lane/plans/sources_adopt.py
  e4f49714299ca1f2a93303c59ac07e691cc45d6126ccf24e5eecab93733f88f3  plans/tip_receipts.py
  38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0  plans/sources_adopt.py
```
Both hashes equal `PINS` in the frozen counter, so the pins are unchanged from the landing tip `74513c06` to `3d0058fb`
to lane HEAD `d7c77895` (`git diff --name-only 3d0058f d7c7789` lists only `.ufo/.../falsify-{spec,dispatch}.json`).

Envelope used for every counter run (the counter nests its own read-only sandboxes inside it):
```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent python3 plans/round41_c1_verify.py ...
```

## A. Two re-measures, byte-compared

```
PYTHONHASHSEED=1  ... --lane "$S/lane" --work "$S/w1" --jobs 1   real 0m26.258s  exit=0  78 lines
PYTHONHASHSEED=99 ... --lane "$S/lane" --work "$S/w2" --jobs 8   real 0m4.548s   exit=0  78 lines
sha256sum run-seed1-jobs1.txt run-seed99-jobs8.txt
  87a176bdf96bdb62d7c942a06328cab2aeb3f2412eee2ffd9df9c1f8c4d02ed3  run-seed1-jobs1.txt
  87a176bdf96bdb62d7c942a06328cab2aeb3f2412eee2ffd9df9c1f8c4d02ed3  run-seed99-jobs8.txt
cmp run-seed1-jobs1.txt run-seed99-jobs8.txt            -> IDENTICAL_SEED_JOBS
{ cat run-seed1-jobs1.txt; echo exit=0; } | diff ref-c1-block.txt -   -> BYTE_EQUAL_REF
sha256sum run1-plus-exit.txt ref-c1-block.txt
  48b4745cbcc32673b064a78ecba0a4cb3b69c8f8155f3259811c43a42b0ffdfd  (both)
```
`ref-c1-block.txt` is the `$ python3 plans/round41_c1_verify.py …` … `exit=0` span of
`.ufo/waves/round-41/integrate/measure-final.txt` (79 lines). Both re-measures are byte-identical to each other
(78 lines + trailing `exit=0` = same 79-line block, same sha256) and therefore to the landing measurement, across
two hash seeds and two job counts.

A third run at **lane HEAD** `d7c77895752a2a5f317fa22f2362416ada50a04b` (`PYTHONHASHSEED=7 --jobs 8`, 5.5 s, exit 0)
also diffed clean: `-> LANEHEAD_BYTE_EQUAL`, sha256 `87a176bd…`. The recorded numbers reproduce:

```
PINS total=2 mismatched=0
BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0
MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=13/13 sources=10/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 pass
```

## B. Load-bearing table (each module removed in turn, real predicate path)

Method: per module, `git -C lane archive 3d0058f | tar -x -C rm/<mod>`, delete `rm/<mod>/plans/battery41/<mod>.py`,
run the frozen counter with `--lane rm/<mod>` (default `plans/battery41` path, so the real `PREDICATE C1` check runs,
not the `--battery-dir` dev path). All seven showed `PINS total=2 mismatched=0` and `PINS-AFTER mismatched=0`
(faithful copies). Raw outputs: `F41C1Rerun/out-<mod>.txt`.

| module removed | fixtures | killed | flipped to SURVIVED (its unique kills) |
|---|---|---|---|
| r_setup | 40 | 19 | T01, T02, T05, T07 (4) |
| r_run   | 44 | 21 | T03, T04 (2) |
| r_ctl   | 44 | 22 | **T08** (1) |
| r_map   | 38 | 19 | T09, T10, T11, T12 (4) |
| s_usage | 40 | 19 | S02, S03, S05, S06 (4) |
| s_modes | 40 | 19 | S01, S04, S08, S09 (4) |
| s_exit  | 42 | 21 | S07, S11 (2) |

Every removal printed `PREDICATE C1 fail`, exit 1 — so the battery is load-bearing, not decorative:
`MUTANTS total=23 killed=19 survived=4 … PREDICATE C1 fail` (r_setup, r_map, s_usage, s_modes),
`killed=22 survived=1` (r_ctl), `killed=21 survived=2` (r_run, s_exit). Fixture deltas match the modules'
`FIXTURES` lengths (8,4,4,10,8,8,6; sum 48), read by AST.

**Modules that kill nothing alone: none — 7/7 are load-bearing.** Unique kills total 21/23; the two non-unique
mutants are T06 and T13, whose `r_ctl` kills are redundant with `r_run`. With `r_ctl` removed:
```
MUTANT T06 receipts rc-silence killed by=r_run-t03-rc-nonzero-mixed
MUTANT T13 receipts rc-mirror killed by=r_run-t13-auto-control-differ
```
versus the reference run's `T06 killed by=r_ctl-t06-empty-equal-receipt`, `T13 killed by=r_ctl-t08-derived-uv-absent`.
`r_ctl`'s only exclusive credit is T08 — the thinnest margin in the set (1 mutant), so a future edit that moves T08's
kill to another module would silently make `r_ctl` redundant while the predicate still passes. Calibration point, not
a defect: the predicate binds totals and per-tool floors, not per-module necessity — the table above is the only
artifact that shows it.

Direction strictness is visible in the same data: in the `r_map`-removal run, `T10` "SURVIVED exhibits=1>0,1>2,rc-silence"
— the mutant is observable but not in its declared `silence` direction, and the counter refuses to credit it.

## C. Known counter vectors — measured on the 7 landed modules

Cheap non-author checks (not a substitute for the counter-attack seats, but they answer "does this battery use a named vector"):

1. Source-text tokens (`SIDECHANNEL` list): the counter prints `sidechannel=0`; my independent grep of
   `plans/battery41/*.py` for `..|environ|getattr|globals(|exec(|eval(|socket|/proc|chr(|__file__|inspect|importlib|ctypes|sys.path`
   returns one hit, a docstring ellipsis in `r_setup.py:4`. No absolute-path literal anywhere in the 7 modules
   (`grep -nE '"/[a-zA-Z]' *.py` → empty).
2. Argv tokens, measured: I dumped every fixture's `build()` output under bwrap (counter's own `--build-module` child)
   and classified all 286 tokens: `work=10`, `abs_in_fixture=63`, `relative=213`, `abs_OUTSIDE=0`, `..`-bearing=0
   (`F41C1Rerun/argv-token-census.txt`). So the F4/A3 relative-token escape is not exercised here: no token leaves the
   fixture dir, and the tool runs with `cwd=fx["dir"]` (`Runner.run`), so the 213 relative tokens resolve inside it.
3. Sandbox steering: every module writes only through `ctx.write/ctx.git/ctx.init`, which refuse paths outside the
   fixture dir (`Ctx._inside`). No module reads a path outside its fixture, and none references the variant slot path
   that A1′/F1 used. That is source-level evidence only.

## D. What holds / what breaks

Holds: (i) the C1 block is byte-invariant across hash seed, job count, and the three tips `74513c06` → `3d0058fb` →
`d7c77895`; (ii) all 23 mutants stay killed with `wrong=0 tampered=0 null_detected=0`; (iii) all 7 modules are
individually necessary for the pass; (iv) fixture trees are untouched (`tampered=0`) and second unmodified runs agree
(`null_detected=0`) in all ten runs I made.

Breaks / stays open: (i) 2/23 kills (T06, T13) are redundant, so the battery is necessary module-by-module but not
minimal fixture-by-fixture; (ii) `r_ctl` rests on one exclusive kill (T08); (iii) the sidechannel predicate is a token
scan, and my independent scan is source-text too — a module that builds a path or reads `/proc` dynamically would pass
both (`R41CritC1Counter` A8); (iv) nothing here re-tests the A1′/F1 verdict-steering vector for modules I did not
rebuild — these seven are clean by inspection, which is precisely the non-author source review the freeze admits as
the admission basis. No C1 admission failure found on the landed set.

## E. Host safety

Every counter/fixture/builder invocation ran inside the mandated envelope with `~/.local/bin` read-only.
`ls -la /home/vgpnk/.local/bin/git` → "No such file or directory"; the newest entries are pre-session
(`ruff` 09:46, `OpenBot` 10:50). `crit_git_shim.py` still begins `raise SystemExit("NEUTRALIZED by the round-40 L1 …")`.
The lane is untouched: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD` → `d7c77895…` with only the
pre-existing `?? .ufo/waves/round-41/falsify*` untracked entries. My clone `lane/` ends at `d7c77895` with
`status --porcelain | wc -l` → 0. No pacman/uv installs were made. Scratch `/fast/scratch/hyaku/kengaku-r41/F41C1Rerun`
(4.2 G: clone 571 M + seven archive trees 3.6 G) is deleted at the end of this seat.

VERDICT: c1-rerun-byte-equal-yes-load-bearing-7/7
