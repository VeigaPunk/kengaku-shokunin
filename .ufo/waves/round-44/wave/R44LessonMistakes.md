# R44LessonMistakes — `## Mistakes` draft for `corpus/lessons/round-44.md`

Seat: scribe, round 44 (kengaku, hyaku run 9), one v2 wave. Time of measurement: 2026-10-26 20:36–20:41 -03.
Lane cwd for every command: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. No lane file was edited; nothing was
committed; no subagent was spawned.

**Deliverable:** `.ufo/waves/round-44/wave/R44LessonMistakes/round-44-mistakes.md` — the ready-to-paste `## Mistakes`
block (5 rows, class · evidence pointer · captured-by · fix). The L1 pastes it into the round-44 lesson; I did not.

## Axes (named before work)

- **Truth of each row** — every class sentence had to survive its own re-measurement; I ran each fix's instrument
  myself instead of quoting a seat, and where a fix is still in flight I ran it and pasted the failure.
- **Coverage of the four named items + the sweep find** — five rows; the fifth is the sweep's own product.
- **Falsifiability of every fix** — "a fix counts only once shown able to fail": each row names a red state I produced
  (not a proposed instrument), and the one instrument I could not fault (the envelope) was demoted to a boundary note.
- **Non-intrusion** — writes confined to `.ufo/waves/round-44/wave/R44LessonMistakes/` and `/fast/scratch/hyaku/kengaku-r44/R44LessonMistakes`.

## Behaviour

I read `plans/round-44-claims.md` in full, then the round-43 closure `corpus/lessons/round-43-verifier-spotcheck.md`
(§1 D1–D3, §3, §4, §5 R1), the round-43 lesson's `## Gate`/`## Mistakes` rows, and the round-44 claims receipts, and
wrote one row per named item. Each row's evidence pointer names a file and a line (or a receipt line); each row's fix
carries the command I ran and the red (or green→red reversal) it produced. Two small read-only checkers and six receipts
were written under my subdir so the L1 can re-run every claim.

## Findings (the 5 rows, and what each fix's red state is)

1. **False `not fired` flip verdict** (`corpus/lessons/round-43.md:46`). The verdict says no entry sentence rests on
   `task.toml`/`setup.py`/`solve.sh`, while the landed entry cites `task.toml:22` at `:41`, `:122`, `:240`, `:300`,
   `:332` and `solve.sh:90` at `:230`, `:252`, `:306`. Captured-by: none — `plans/gate_flip_check.py:256-257` accepts
   the state token and never opens the entry. Fix shown to fail: the in-flight citation leg
   (`.ufo/waves/round-44/wave/R44FlipVerdict/gate_flip_check.py`) prints `FLIP-CITE line=46 item=task.toml …
   verdict=RED` four times on the real lesson, `not_fired=2 red=1`, `exit=1`, and its own `SELFTEST ok=26/26` includes
   `case=cite-not-fired-red expect=red got=red`. My independent sweep agrees (`red=1` block-scoped, `red=2`
   all-scoped, with the over-fire on `round-42.md:215` recorded as the leg's named limit).
2. **Round filed at 38 seats** (D1). `build-spec.json seats 38 floor64 FAIL` / `wave-spec.json seats 68 floor64 PASS`,
   `wave-dispatch.json counts={'spawn': 68, 'resume': 0, 'total': 68}`; `falsify.ready` absent while the spec and
   dispatch exist.
3. **Seat with no report file** (D3, `R43ConnClaims`). `REPORTS seats=38 files=37 missing=1:R43ConnClaims`, exit=1 on
   the closed round-43 data; the same command on round 44 at 20:41:04 reads `seats=68 files=47 missing=21` (in flight —
   43 → 47 between two runs a minute apart, so only the close-time run decides).
4. **Freeze priced U3, which the standing batteries already kill** — caught before freeze. Draft receipt:
   `MUTANT U3 anchor rc-mirror killed by=a_alt-slug-deepest attributed=L354 value=differs hits=16`,
   `MUTANTS total=6 killed=1 survived=5`; frozen receipt: `BATTERY fixtures=71 … MUTANTS total=5 killed=0 survived=5`.
   The instrument that fired is the one the row prescribes; it reversed its answer when the row was dropped.
5. **Sweep symptom (new, from my own sweep): a corpus-wide law over a silently reduced denominator.** The round-43 flip
   survey quotes `FLIPS total=45 over 18 lessons`, but its receipt has 55 lesson lines of which 35 are
   `rc=2 SETUP no '## Gate' section` (64 %), and one of those skipped lessons,
   `corpus/lessons/round-42-verifier-spotcheck.md`, carries the flip condition the whole class was mined from at `:37`.
   Re-run today: the landed checker exits 2 (`SETUP no '## Gate' section`) on that lesson, and on **41 of 62** lessons
   overall (21 read: 4 `exit=0`, 17 `exit=1`). My re-aggregation of the receipt's 20 per-file `FLIPS` lines reproduces
   `45/45` over 18 lessons — the aggregate is right, the denominator is not stated.

## Gates and receipts (every run with its envelope lines)

All envelope runs used
`.ufo/waves/round-44/claims/envelope.sh "$S/env" …` with `S=/fast/scratch/hyaku/kengaku-r44/R44LessonMistakes`.

| run | command (lane cwd) | observed |
|---|---|---|
| flipped verdict, real lesson | `envelope … python3 .ufo/waves/round-44/wave/R44FlipVerdict/gate_flip_check.py --lesson corpus/lessons/round-43.md` | `FLIP-CITE line=46 item=task.toml … verdict=RED` ×4; `FLIP-CITE entries=… missing=instruction.md,README.md,R43MergeRescreen.md,SOURCES.md not_fired=2 red=1`; `FLIPS total=2 unresolved=0`; `exit=1`; `ENVELOPE end 20:38:05 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` |
| citation leg selftest | `envelope … …/gate_flip_check.py --selftest` | `SELFTEST ok=26/26`, incl. `cite-not-fired-red expect=red got=red … cite_red=1`; `ENVELOPE end 20:37:58 exit=0 … unchanged` |
| independent sweep | `envelope … python3 …/flip_cite_sweep.py --lane . --scope block` then `--scope all` | block: `FLIP-CITE corpus/lessons/round-43.md:46 item=task.toml verdict=RED … (+6)`, `FLIPS-CITE total=6 named=3 red=1`, `exit=1`; all: `red=2`, `ENVELOPE end 20:39:25 … unchanged` |
| sweep denominator | `grep -c 'rc=2' …/R43FlipCheck/sweep.txt`; re-aggregation; `envelope … python3 plans/gate_flip_check.py --lesson corpus/lessons/round-42-verifier-spotcheck.md` | `35`; `skip 35 flip_lines 20 sum_total 45 sum_unresolved 45 flip_files_with_total_gt0 18`; `SETUP no '## Gate' section`, `exit=2`, `ENVELOPE end 20:39:28 exit=2 … unchanged` |
| checker over all lessons | `envelope … bash -c 'for f in corpus/lessons/*.md; do python3 plans/gate_flip_check.py --lesson "$f"; done'` | 62 lessons: 41 `exit=2`, 4 `exit=0`, 17 `exit=1`; `ENVELOPE end 20:39:40 exit=0 … unchanged` |
| report files | `envelope … python3 …/report_file_check.py --lane . --reports .ufo/waves/round-43/build --results .ufo/waves/round-43/build-results.json`; same on round 44 with `--dispatch .ufo/waves/round-44/wave-dispatch.json` | round 43: `REPORTS seats=38 files=37 missing=1:R43ConnClaims`, `ENVELOPE end 20:40:15 exit=1 … unchanged`; round 44 at 20:41:04: `REPORTS seats=68 files=47 missing=21`, `ENVELOPE end 20:41:06 exit=1 … unchanged` (in flight; 43 → 47 between two runs) |
| seat floor + battery size | inline `python3` over the two spec files and `ast` over `plans/battery4{2,3}/*.py` | `38 FAIL` / `68 PASS`; `{'spawn': 68, 'resume': 0, 'total': 68}`; battery42 `29` + battery43 `42` = `71` = the control's `BATTERY fixtures=71` |
| frozen digests | `sha256sum -c .ufo/waves/round-44/claims/frozen-digests.txt` | 12/12 `OK` (frozen inputs untouched at my read time) |
| envelope sweep | inline `python3` over `.ufo/waves/round-44/claims/*.txt` | `receipts 22 with_digest 18`, `digest_changed []`, `no_digest` = `c2-stage-check.txt`, `census-before.txt`, `fetch-time.txt`, `frozen-digests.txt` |
| receipt consistency | inline `python3` + greps over the round-44 receipts | probe `cases 14 tests_P 8 tests_F 6 match_yes 14 regrade_same 14` = dry table `cases=14 predicted_pass=8 predicted_fail=6`; `witness-run` `killed=5 survived=0 anchor=4/4 order=1/1`; `control-c1-nothing` `killed=0 survived=5`; hostile f1–f6 each `1` round-44 `SETUP` with `exit=2`, f4's round-43 half `exit=124` |

## Touched surfaces

- Created: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44LessonMistakes.md` (this report)
  and `.ufo/waves/round-44/wave/R44LessonMistakes/`:
  `round-44-mistakes.md` (the draft), `flip_cite_sweep.py`, `report_file_check.py`, `draft-flip-selftest.txt`,
  `draft-flip-real43.txt`, `sweep-flip-cite.txt`, `sweep-flip-skip.txt`, `sweep-flip-all-lessons.txt`,
  `sweep-reports.txt`, `sweep-floor.txt`, `sweep-envelope.txt`, `sweep-consistency.txt` (largest 10.4 KB).
- Scratch: `/fast/scratch/hyaku/kengaku-r44/R44LessonMistakes` (deleted before yield with `scratch_guard.py safe-rm`).
- Read-only, executed (not modified): `plans/gate_flip_check.py`, `.ufo/waves/round-44/wave/R44FlipVerdict/gate_flip_check.py`
  (in-flight seat's file, run twice as evidence), `.ufo/waves/round-44/claims/envelope.sh`.
- Not touched: no lane `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`, `PROVINCE.md`,
  `SHONEN.md`; no git/jj command at all (no `git ls-tree` mutation, no commit).

## Out of scope / deliberately not claimed

- I did not paste the block into `corpus/lessons/round-44.md`, and did not edit `plans/gate_flip_check.py` (the citation
  leg belongs to seat `R44FlipVerdict`; its file was in flight and changed under me, so my quotes carry a timestamp).
- Row 2's fix is green today but the round is not closed; the row says the check must be re-run on the landed wave.
- The envelope gap (`c2-stage-check.txt`) is recorded as a **named boundary, not a mistake**: the probe's
  `--stage-check` writes only under `mkdtemp(…, dir=a.work)` (`plans/feal_linear_probe.py:226`, `:303`), so the claims'
  sentence about counter runs holds, and the receipt's missing start/end + PATH digest cannot be repaired without
  re-running a frozen-order step.
- No claim about the two C1/C2 predicates: they belong to the executors and the L1's landing measurement.
- The draft's second sentence of row 1's fix is a recommendation (pair the name match with a reading), not a measured
  result — the draft says so explicitly.

## Artefacts

- Draft (deliverable): `.ufo/waves/round-44/wave/R44LessonMistakes/round-44-mistakes.md`
- Receipts + checkers: `.ufo/waves/round-44/wave/R44LessonMistakes/{sweep-*.txt, draft-flip-*.txt, flip_cite_sweep.py, report_file_check.py}`
- Host safety: every executed run went through the round-44 envelope; all 7 `ENVELOPE end` lines I produced read
  `local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` (receipts `draft-flip-selftest.txt`,
  `draft-flip-real43.txt`, `sweep-flip-cite.txt`, `sweep-flip-skip.txt`, `sweep-flip-all-lessons.txt`,
  `sweep-reports.txt`, `sweep-reports-round44.txt`). The three inline `python3` sweeps (`sweep-floor.txt`, `sweep-envelope.txt`,
  `sweep-consistency.txt`) only read files and print, and ran without the envelope. Nothing was installed; no package
  manager was invoked.

VERDICT: mistakes-drafted-5
