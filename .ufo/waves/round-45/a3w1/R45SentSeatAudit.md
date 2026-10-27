# R45SentSeatAudit — round-45 seat hygiene audit (wave a3w1, attempt 3)

Seat: sentinel, leaf. Scope: hygiene of the round's seats (w1 primary, w2 for completeness) — writes outside a
seat's own subdir (lane tree, fleet root, `~/.local/bin`, `/tmp` receipts), git/jj mutations by seats, and committed
lane-file hashes versus the freeze inputs. No lane file was edited; this seat wrote only this report and
`.ufo/waves/round-45/a3w1/R45SentSeatAudit/`. No fixture build, counter or probe was run, so no envelope run was
needed; every command below is read-only host inspection (`git`/`find`/`grep`/`stat`/`sha256sum`/`ps`, no `jj`).

## Measured state

- Lane tip measured: **`fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc`** (`git -C <lane> rev-parse HEAD`), branch `HEAD`
  (exported from jj), 10 commits since the freeze commit `52d7486`. Matches the a3w1 dispatch hash.
- Worktree at measurement was **not clean**: `git status --porcelain` reported ` M SCORECARD.md`, ` M corpus/QUALITY.md`
  (mtimes 00:23–00:26, content = attempt-3 L1 landing text, e.g. QUALITY Q39 and a SCORECARD citation correction) plus
  untracked `.ufo/waves/round-45/{a3w1*,claims/fences/keyed_name.py,claims/dev-blind-c1*,integrate/a3-*}`. Therefore
  every "committed lane file" statement below is scoped to **HEAD `fbad1c5`**, not to the dirty worktree.
- Frozen inputs: `sha256sum -c .ufo/waves/round-45/claims/frozen-digests.txt` → **19/19 OK, exit 0** (claims md,
  C1/C2 counters, probe, spec, dry table, tb2 `SHA256SUMS`, predictor control, and all 10 `plans/refusals45/f*.py`).
  No frozen input drifted after the amendment pin.

## Method / evidence

```
$ git -C <lane> rev-parse HEAD                     → fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc
$ git -C <lane> log --format='%an <%ae>' 52d7486..HEAD | sort | uniq -c
                                                   → 10 kengaku-shokunin <kengaku@shokunin.local>
$ git -C <lane> reflog -40                         → 11 entries, every one "export from jj"; no reset/checkout/amend
$ git -C <lane> fsck --no-progress | grep -c 'dangling commit'   → 0
$ git -C <lane> config --list --local | grep -iE 'hook|filter|alias|template|worktree'
                                                   → core.* only; no hooksPath, no filters, hooks dir = *.sample (Oct 13)
$ ls -l <lane>/.jj/repo/op_heads/heads | wc -l     → 1
$ find <lane>/.jj/repo/op_store/operations -newermt '2026-10-26 22:00' ... | uniq -c
   → 00:15(7) 23:06(8) 23:20(7) 23:27(5) 23:40(8) 23:42(7) 23:43(6) 23:44(5) 23:45(5) 23:48(7) 23:49(7) 23:50(1) 23:51(1) 23:55(6)
     (each cluster == an L1 commit/export time; no op in the seats-only windows 23:28–23:38)
$ find <lane>/.ufo/waves/round-45/w1 -type l        → (none)
$ find <lane>/.ufo/waves/round-45/w1 -type f | wc -l → 335 files, 3.2 MB, largest 127,415 B
$ find <lane>/.ufo/waves/round-45/w2 -type f | wc -l → 93 files, 1.7 MB
$ grep -rh '^ENVELOPE /' w1 | wc -l ; ... | grep -vc -- '--ro-bind /home/vgpnk'
                                                   → 152 envelope commands, 1 without the home ro-bind
$ grep -rh '^ENVELOPE /' w2 | wc -l ; ... | grep -vc -- '--ro-bind /home/vgpnk'   → 43 / 0
$ python3 (w1-spec.json seats vs w1/*.md)          → 39 seats, 39 reports, 34 seat dirs, 0 missing, 0 extra
$ git -C <lane> diff 52d7486 --name-only | wc -l    → 461 at 00:19 (24 non-.ufo), 462 at 00:23 (25 non-.ufo, +QUALITY.md dirty)
$ git -C <fleet-root> status --porcelain            → ?? .ufo/reports/round-45/kengaku.md   (only kengaku-named entry)
$ find ~/.local/bin -newermt '2026-10-26 23:30' -printf '%TH:%TM %f\n'
   → 23:36:46 OpenBot-0.51.1-x86_64.AppImage ; (00:02:23 omp, 00:02:24 bin — next day, operator update)
$ stat -c '%y' ~/.local/bin/agy.1793063119693176144.old → 2026-10-22 23:51:12  (not round-45)
```

Every w1 path in `git diff 52d7486 --name-only` matches `.ufo/waves/round-45/w1/<Seat>/…` or `w1/<Seat>.md` (checked
with `grep -vE '^\.ufo/waves/round-45/w1/[A-Za-z0-9]+(\.md|/)'` → no output); the only non-seat file at that level is
the orchestrator's `swarm-registry.json`. No seat script writes an absolute lane path: `grep -rInE '>[>]?
"/home/vgpnk/Projects/shokunin/kengaku-shokunin/(corpus|plans|…)'` over w1 and w2 → no hits; the one `cp …
"$LANE/corpus/SOURCES.md"` (`w1/R45PkgRows/validate.sh:77`) writes into `LANE=$S/lane`, a scratch clone
(`validate.sh:5`), and line 12 prints that clone's `rev-parse --show-toplevel`.

## Findings

| # | Sev | Finding | Evidence | Impact |
|---|-----|---------|----------|--------|
| H1 | med | **Reportless seat (round-43 D3 recurrence), 1 of 2:** `R45CriticC2Instrument` left no report file; the L1 reconstructed it from `w1-results.json`. | `w1/R45CriticC2Instrument.md:1` — "result recovered from w1-results.json (reportless-seat class, round-45 recurrence)"; commit `a448a47` "+14" | Seat output not self-reported; the recovered text says `"execution_limitation": … no counter run was performed` — the assignment's key demonstration was never executed and exists only as prose. |
| H2 | med | **Reportless seat, 2 of 2:** `R45MutV11States` also returned no report; its reconstruction embeds the seat's raw scratchpad. | `w1/R45MutV11States.md:1` same recovery header, 763 B total, contains a literal `<think>` block quoting the seat's instructions | A leaked reasoning block is now committed as round evidence; a reader cannot tell seat output from L1 reconstruction without opening the file. |
| H3 | med | **PATH-directory mutation during the wave window with no recorded owner:** `~/.local/bin/OpenBot-0.51.1-x86_64.AppImage` (296,219,269 B, mode 755) landed at **23:36:46**; the `~/.local/bin` content digest moved `c263b11afb1cccf6 → e396f23e40a69201`. No round-45 seat records an install; four seats attribute it to "another seat" and one calls it "[INFERENCE]". | `find ~/.local/bin -newermt '2026-10-26 23:30'`; `w1/R45ExecControls.md:159-162`, `w1/R45LabratGitAPIs.md:38-42`, `w1/R45SentFenceDesign.md:221-224`, `w1/R45Lesson.md:60-62` | Class = the round-40 hazard (writer touching a shared PATH dir mid-wave). **No measurement was corrupted**: every seat's own bracket was `before == after … unchanged`, and the two runs that *did* span the change declared `INVALID` and re-ran (see below). Risk is provenance: an unidentified 296 MB binary landed in the fleet's PATH dir with no receipt anywhere in the round's evidence. |
| H4 | low | **Evidence-precision defect:** a w1 report lists `agy.1793063119693176144.old, 23:51` as part of the digest shift; that file's mtime is **2026-10-22 23:51:12**, four days earlier (the round-45 mtime is 22:05 on `agy`). | `w1/R45ExecControls.md:161` vs `stat -c '%y' ~/.local/bin/agy.1793063119693176144.old` | Overstated cause set (OpenBot alone explains the digest shift). No verdict changes; quoted mtimes without dates are what let this slip. |

Verified-good (measured, not assumed):

- **INVALID handling was correct where it fired.** `w1/R45ExecHarnessRO.md:78-86` prints
  `ENVELOPE end 23:38:11 … before=c263b11afb1cccf6 after=e396f23e40a69201 CHANGED` / `measurement INVALID`, says it
  does not count, and pins run 1's sha256 for the re-run comparison; `w1/R45LabratControls.md:42-49` reports one
  INVALID f5 build and a single re-run, and all 13 `verdict.txt` re-runs bracket `e396f23e…` unchanged.
- **No seat git/jj mutation.** Uniform author/committer identity, reflog = `export from jj` only, zero
  dangling commits, default sample hooks, no `core.hooksPath`/filter/alias config, one jj op head, and jj op clusters
  only at L1 export times. Lane `git status` has no modified tracked file except the L1's own two in-flight edits.
  (`git reflog -15` → 15/15 `export from jj`, 0 other operation kinds; the 11 entries at/after the freeze commit are
  the same kind. Receipt log: `.ufo/waves/round-45/a3w1/R45SentSeatAudit/receipts.txt`, 2,576 B.)
- **No lane/fleet/source writes from seat scripts.** All 195 envelope commands (152 w1 + 43 w2) are `/usr/bin/bwrap`
  with `--ro-bind /home/vgpnk … ` (the single exception is an *elided* quote of the L1's own probe run in
  `w1/R45ProbeFirst.md:125`, whose full form is committed at `corpus/evidence/round45/probe-run-envelope.txt:1` and
  does carry `--ro-bind /home/vgpnk`). `/etc/shadow`, `/tmp`, fixture parents tested read-only by seats.
- **Source repo `/home/vgpnk/Projects/shokuknow` unwritten by kengaku.** `absent-defect-register.md` mtime
  `2026-10-24 08:37`, sha pinned by `w1/R45MergeRescreen.md:121`; no kengaku wave file is newer there. The
  `corpus-expansion-1` **directory** mtime moved to 23:26 with no surviving new entry (`__pycache__` 10-24 23:33);
  unattributable and residue-free — recorded, not counted.
- **`/tmp` used only transiently.** `w1/R45ExecControls/compare.sh` writes `/tmp/s-$$`-style files and `rm -f`s them;
  `ls /tmp/s-* /tmp/f-* /tmp/c2h.*` → none. Zero `/tmp` paths are cited as evidence in the round's reports.
- **No oversize seat receipts.** Largest wave file 127,415 B (`w1/R45ExecHarnessRO/run1-driver.out.txt`); w1 3.2 MB,
  w2 1.7 MB; no file ≥ 1 MiB; no symlinks.

## Freeze / surface reconciliation (committed tree at `fbad1c5`)

- 19/19 pinned digests OK (above).
- 24 non-`.ufo` lane files differ from `52d7486`; each maps to a declared surface: C1 (`plans/fixture_fence.py`,
  `corpus/evidence/round45/c1-counter-run.txt`), C2 (`corpus/knowledge/tb2-password-recovery-grader.md`,
  `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md`, 6 of the tb2 captures, 4 evidence receipts,
  `plans/password_recovery_probe.py`), frontier (`SCORECARD.md`, `LOG.md`, `corpus/lessons/round-45.md`), and the
  declared freeze amendments (`plans/round-45-claims.md`, `plans/pkg-spec-r45.json`, `plans/round45_c2_verify.py`).
  `git diff --stat 52d7486 -- plans/refusals45 plans/battery42 plans/battery43 plans/battery44` → empty: the ten
  hostile modules and the 104-fixture honest set are byte-unchanged, so C1's attack surface was not resculpted.
- Fence pin consistency: `git cat-file -p HEAD:plans/fixture_fence.py | sha256sum` =
  `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6` = the `FENCE … sha256=` line in the committed
  receipt (`corpus/evidence/round45/c1-counter-run.txt`. So the receipt's fence pin names the committed fence.
- **Watch item (not a seat violation):** `corpus/QUALITY.md` is **not** in the claims' Surface lists, yet it is the
  third corpus-governance file being edited in this round (+30 lines, Q39, currently uncommitted, author = attempt-3
  L1). If it lands as written, the round's declared surfaces under-name what it touched. Related: the committed C1
  receipt's `ENVELOPE` shows `cwd=<lane>` with `--lane .` — *not* the "clean clone of the landing tip" wording in
  `plans/round-45-claims.md:53`; the clone run exists only as the untracked
  `.ufo/waves/round-45/integrate/a3-tip-c1.txt` (same `FENCE sha256=ac65c03…`, `PINS total=33 mismatched=0`). Hygiene
  is unaffected (the lane was read-only inside the bwrap), but the receipt's provenance and the claim's wording do
  not match — for the C1 receipt critics.

## Residuals deliberately not counted

`/tmp/sc-landed.md` (262,266 B, 22:04, sha256 `be78b2e70154e099d12eb88c027603ec826f5e189fedd64f23fac0c3e79c66bf`) is a
`mori-shokunin` SCORECARD copy left in `/tmp` from attempt-1 prep, referenced by no round-45 receipt — residue, never
evidence. `w1/R45Lesson/corpus/lessons/round-45.md` (sha256 `7ea5ae7a…` ≠ landed `bdf67b20…`) is the scribe's *draft*
stored under a lane-shaped path **inside its own subdir** and digest-pinned in `w1/R45Lesson.md:11`; it is shape-smell,
not a tree copy and not a write outside the subdir.

## Fleet-root misroot

`git -C /home/vgpnk/Projects/shokunin status --porcelain` → **one** kengaku-named entry:
`?? .ufo/reports/round-45/kengaku.md` (6,344 B, 23:47, sha256 `10f9f5f8c1ca42d240da760de8a234473098dc1c55dc915dd17d4728a3c8411f`).
It is the L1's round report at the fleet's conventional `reports/round-N/<lane>.md` path (all seven sibling lanes'
round-45 reports are tracked there), not a seat write and not a lane artifact; it is simply uncommitted by the fleet
integrator. The other kengaku-named fleet files touched today are orchestrator-owned
(`.ufo/prompts/kengaku-round-45.md`, `.ufo/state/kengaku.report-baseline` — ignored per `.gitignore:8`). No seat
wrote into the fleet root: no w1/w2 receipt contains a redirect or `tee` to `/home/vgpnk/Projects/shokunin/…`, and
`find … -iname '*kengaku*' -not -path '*/kengaku-shokunin/*'` returns only those three orchestrator/L1 paths.

Scratch `/fast/scratch/hyaku/kengaku-r45/R45SentSeatAudit` removed with `plans/scratch_guard.py safe-rm` before yield.

VERDICT: hygiene-violations-4-misroot-1
