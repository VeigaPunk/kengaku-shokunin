# R37LessonDraft — round-37 lane lesson drafted (kengaku, 2026-10-26)

Seat: `R37LessonDraft` (scribe, axes calibration + coverage). Target: draft the lane lesson
`corpus/lessons/round-37.md` in the shape of `corpus/lessons/round-36.md`. Nothing in the lane was edited;
everything below is either read from committed bytes or measured in `/fast/scratch/hyaku/kengaku-r37/R37LessonDraft`
(deleted at seat end).

## Behavior

Draft at `.ufo/waves/round-37/build/R37LessonDraft/round-37.md` (18.9 KB), sections in round-36 order:
header (baseline `3ea9a1d9`, freeze `ca790460`, first probe run `5c7b34e9`) → `## Gate` → `## Mistakes` →
round-36 §5 disposition → `## Census` → `## Spot-check` → `## Close (appended at closure)`.

Commands and outcomes behind the draft:

| what | command (lane root unless stated) | output |
|---|---|---|
| ancestry of the header's three commits | `git merge-base --is-ancestor 3ea9a1d9 ca790460`; `… ca790460 5c7b34e9`; `… 5c7b34e9 HEAD` | all exit 0 (baseline → freeze → probe → `44b7298a`) |
| frozen digest block is not stale | `git show ca790460:<path> \| sha256sum` for all 11 entries of `claims/frozen-digests.txt` | 11/11 `MATCH` — the round-36 number-drift class does not recur |
| C1 before | `cat .ufo/waves/round-37/claims/control-c1-nothing.txt` | `BATTERY fixtures=14 wrong=0 renamed_disagree=0`; `MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0`; `PREDICATE C1 fail`; exit 1 |
| C1 at drafting (per-seat, not the predicate) | `grep -rhoE "MUTANT M[0-9]+ [A-Z0-9]+ killed by=[^ ]+" .ufo/waves/round-37/build \| awk '{print $2}' \| sort -u \| wc -l` | `51` at 01:44, `55` at 01:46 as `R37BatP910`'s receipts landed; per-seat primary blocks: P2/P3 6/6, P4 4/4, P5 7/7, P6 8/8, P7 6/6, P8 5/5, P9/P10 4/4, D4 3/3, D5 7/7 (50 new + the frozen 5) |
| C2 before | `cat …/control-c2-nothing.txt` | `checks=7 defects=4` (V2, V3, V4, V7), exit 1 |
| C2 skip-control | `cat …/control-c2-skip.txt` | `V2 DEFECT gate_exit=1`, `P10 DEFECT fresh probe output is not byte-equal to the receipt`, `checks=7 defects=1`, exit 1 |
| probe receipt vs frozen predictions | parse `CASE` ids from `corpus/evidence/round37/git-webserver-dry-cases-freeze.txt` and `…-probe.txt` | 22 ids, same order, 9 `predicted=pass`, 9 `observed=pass`, 0 disagreements, summary `cases=22 observed_pass=9 observed_fail=13 mismatches=0` |
| captures vs manifest | `sha256sum -c` equivalent in `corpus/evidence/round37/tb2-git-webserver` | 6/6 match `SHA256SUMS`; manifest digest `e70bb662…` equals the freeze pin |
| quote lines | `sed -n '13p' test_outputs.py`, `sed -n '57p' verify.sh`, `sed -n '9p' instruction.md` | `assert "TEST PASSED" in result.stdout, "Did not pass test"`; `HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/hello.html)`; `then I see the output "hello world".` (9/7/8 words) |
| census counts | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`; `ls corpus/knowledge/*.md \| wc -l`; `grep -cE '^\| `knowledge/[^`]+` \|' corpus/README.md` | `103` / `43` / `43`; `grep -n "S11[1-3]" corpus/SOURCES.md` → 0 |
| S110 defect still present | `grep -o "sha256 [0-9a-f]*" corpus/SOURCES.md \| awk '{print length($2)}' \| sort \| uniq -c` | `1 63` beside `8 64` — S110 at `corpus/SOURCES.md:125` is still 63 hex |
| V3 shown able to fail | scratch clone + `import plans/round37_c2_verify; v3(clone)` | exact rows `v3 ok=True rows=3 bad=0`; S111 digest minus its last hex char `v3 ok=False rows=3 bad=['S111:anchor_digest']` |
| ledger tip (assimilation 2(a)) | `cat .ufo/waves/round-37/build/R37LedgerTip/ledger-tip-run1.txt` | `TIP commit=44b7298a…`; `rows=9 closed=9 observed_pass=9 mismatches=0` |

## Gate (as drafted)

- `knowledge/tb2-git-webserver-grader.md` (C2) — **Admit-candidate, held**: absent from `corpus/knowledge/`
  at drafting (43 files), draft at `build/R37PkgDraft/entry.md`; flip only on `checks=7 defects=0` +
  `PREDICATE C2 pass` at the landing tip.
- S111/S112/S113 — **Held (mined; rows absent at drafting)**: each with its raw URL at `2fd12b88…`, access
  date 2026-10-26, a ≤25-word quote sed-verified against the capture, and its capture digest; rows drafted
  at `build/R37PkgDraft/sources-rows.md`.
- `tests/test.sh`, `task.toml`, `solution/solve.sh` — **Captured, not rows**, each with a reason (duplicate
  reward plumbing already held as S109; manifest metadata not a scoring predicate; the oracle is not the
  grader and the probe never runs it) and a flip condition.
- Assimilation `considerthese/2026-10-25.md` proposal 2(a) — **Mined; one third built**: 2(a) is realised by
  `R37LedgerTip` (9/9 closed rows re-run at the tip), 2(b)/2(c) unbuilt, and round 36's own defects were
  never ledger rows (`grep -rl "R36-D" corpus/ plans/` → empty).

## Findings (beyond the ticket's three rows)

1. The anchor class is wider than S110: `R37AnchorSweep` on the lane as-is prints `rows=103 tokens=11
   defects=5` — S110 `digest-short` plus S070/S072/S073/S074 `digest-unknown` (not committed evidence and
   not in any `SHA256SUMS`), and `defects=0 exit=0` only with the erratum plus four staged captures.
2. `R37AnchorSweep`'s own fixture matrix is not green: `CASE M1-… defects=3/1 … WRONG`, `CASE M2-…
   defects=2/1 … WRONG`, although both report `expect ids=S110` and the matching class set. Cause read from
   the code: `build/R37AnchorSweep/fixture_matrix.py:138` `want = len(expect_ids)` (ids) compared with one
   printed line per defect (lines). Recorded as a `count` row in the draft; the sweep seat owns the fix.
3. The wave's receipts yield two totals for the same mutant id (primary `killed by=` vs ablation `SURVIVED`);
   the grep union is not the predicate. Recorded as a `derived-number` row; the only admissible number is
   the frozen predicate line on a clean clone.

## Numbers deliberately left pending

`PREDICATE C1` / `PREDICATE C2` at the landing tip, the census-after file, `R37R36Absorb`, the second run's
byte-equality (`R37ProbeRerun`), and the anchor sweep's own green receipt (`R37AnchorSweep`). Each is marked
`<pending: seat>` in the draft; none was asserted.

## Touched surfaces

New files only, all inside my allowed write area:
- `.ufo/waves/round-37/build/R37LessonDraft/round-37.md` — the draft lesson.
- `.ufo/waves/round-37/build/R37LessonDraft/v3-falsifier.txt` — V3 pass/fail pair, with the script used.
- `.ufo/waves/round-37/build/R37LessonDraft/c1-kill-union.txt` — union count, per-seat primary blocks,
  ablation blocks, freeze control.
- `.ufo/waves/round-37/build/R37LessonDraft.md` — this report.

No lane file was edited: `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`,
`PROVINCE.md`, `SHONEN.md`, the lane's Git index and jj state are untouched. No `git add/commit/…` and no
mutating `jj` ran in the lane. The scratch clone at `/fast/scratch/hyaku/kengaku-r37/R37LessonDraft` was
created with `git clone -q --shared`, verified with `git -C … rev-parse --show-toplevel` =
`/fast/scratch/…/fx/lane`, used index-free, and removed with `rm -rf` before this report.

## Out of scope / limits

- I did not run either frozen predicate to completion (C1 needs the aggregate battery on a clean clone of the
  landing tip; C2 needs the entry and rows that have not landed). The lesson therefore reports per-seat
  receipts and marks the predicate lines pending. Observed while finishing (01:49), not cited in the lesson
  because the run was still printing: `.ufo/waves/round-37/integrate/measure-c1-landed.txt` at
  `TIP a3163e675374551bc911d97040d01caf2377a7d7` with `untracked_in_clone=0` had reached
  `BATTERY fixtures=64 wrong=0 renamed_disagree=0` and `MUTANT M17 P5 killed …`; no `MUTANTS total=` line
  and no `PREDICATE C1` line yet. That file is the integrate seat's, not mine, and the lesson keeps
  `<pending: integrate>` until it is complete.
- The V3 demonstration calls the counter's `v3()` function directly on a scratch clone rather than running
  the whole counter: the row fixture is the object under test, and the other six checks are untouched. The
  clone's rows reuse S110's cell shape with the spec's digests; the quote text in those throwaway rows is
  S110's, which is fine for V3 (it reads the anchor cell only) and would fail V2's quote clauses.
- Tooling: nothing installed or upgraded this seat.
- No conflict with the frozen claims was observed; nothing frozen was edited or contradicted.

VERDICT: lesson-drafted
