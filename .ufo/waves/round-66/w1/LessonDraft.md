# LessonDraft — kengaku round 66, wave 1 (v1) — seat report

Seat: `LessonDraft` (scribe, leaf member; no dispatch). Date: 2026-11-03.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Lane-root base for every path in this report:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## What I did

Drafted the round-66 lesson in my seat dir only — `.ufo/waves/round-66/w1/LessonDraft/round-66.md` (the L1
files it as `corpus/lessons/round-66.md`). I wrote **no lane file**: no registry row, no lesson, no
knowledge entry, no SKILL/SCORECARD/LOG edit, no `plans/` file. I changed no frozen case, no frozen table, no
predicate, no kill rule, no quote, and no receipt.

Files written (all inside my seat dir):

- `.ufo/waves/round-66/w1/LessonDraft/round-66.md` — the lesson draft (sections: `## Gate`, `## Mistakes`,
  `## Carried -> closed / open`, `## Discernment spot-check`, `## Sources census`, `## Assimilation`).
- `.ufo/waves/round-66/w1/LessonDraft/receipts/01-c1-checks.txt` — R66-C1 re-checks (receipt of record,
  frozen control receipt, K2-alone).
- `.ufo/waves/round-66/w1/LessonDraft/receipts/02-c2-strict.txt` — the R66-C2 strict proposal re-run over
  the fabricated and the committed receipt, and the default-mode regression.
- `.ufo/waves/round-66/w1/LessonDraft/receipts/03-counter-gaps.txt` — the counter gaps (no-`CASE` receipt
  accepted; unknown-case crash), the sha/row-count facts, and the `battery-run.txt` / `census-before.txt`
  counts.
- `.ufo/waves/round-66/w1/LessonDraft/receipts/census-proposed-rows.txt` — the census run over the proposed
  S236/S237 rows, red (E04) and green.
- `.ufo/waves/round-66/w1/LessonDraft/receipts/04-amendment-a1-state.txt` — the state of the lane's C1 counter
  **after** the L1's mid-wave Amendment A1 (working-tree probe sha `7640a639…`), including the three gaps
  this seat measured against the frozen bytes now closed, and the new control receipt `control-a1.txt`.
- This report.

Scratch: `/fast/scratch/hyaku/kengaku-r66/LessonDraft/` (fixtures and the proposed strict copy; removed
before yield). Nothing was written under `/tmp`. Tooling: **nothing installed or upgraded** (the tooling-only
rule applies and no tool was needed); pacman untouched.

## Key observed values (each with its command; transcripts in the receipts above)

1. `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt` →
   `CHECK ok cases=5` / `PREDICATE R66-C1 pass`, exit 0.
2. `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/prefreeze-run2.txt`
   → five `CHECK defect: … junit_sha does not match committed junit bytes`, `PREDICATE R66-C1 fail`, exit 1 —
   the frozen control receipt no longer re-derives from committed bytes because the post-freeze run
   overwrote the shared `junit/` directory (the probe resolves it as `receipt.parent / "junit"`, not
   receipt-local as the claims doc's pre-freeze-honesty sentence states). The pre-freeze bytes are still
   recoverable from the freeze commit: each junit file's sha256 at `9a07df6a` equals the `junit_sha` its
   receipt names.
3. K2 alone cannot meet the predicate (kill rule d): a receipt carrying only K2's `VECTOR` line → five
   `has no VECTOR line` defects, exit 1.
4. The proposed `--strict` gate over the committed bytes: fabricated fixture → exit 1 with named findings
   (`fabrication-declaration`, `toolchain-not-well-formed` ×4, `toolchain-banner-count` ×3,
   `probe-binding-missing`); committed R65 receipt → exit 0 (`CHECK ok cases=5 strict=yes`); default mode
   unchanged on both fixtures (exit 0, `PREDICATE R65-C1 pass`) — the M-1 defect is still live in default
   mode, as the frozen predicate requires.
5. Registry: the three `QUOTE` lines of the lesson draft pass the round's own counter
   (`round66_registry_check.py quote … --root <lane>` → three `result=FOUND`, `CHECK quote quotes=3
   misses=0`, exit 0). The two rows proposed by the QuoteGateBuild seat **fail the lane's census as
   drafted** (`E04 S236 duplicate url … within scope`), because the supersession marker sits in the `source`
   cell instead of opening the `teaches` cell with `supersedes S0NN —` (CORPUS.md rule 2;
   `scripts/sources-census.sh:646-649`). With the `teaches` cells opened `supersedes S233 — …` /
   `supersedes S234 — …` the same scratch copy is clean of E04 and still passes the meta counter
   (`CHECK meta rows=2 findings=0`).
6. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0, 24 lines,
   byte-identical to the committed `corpus/evidence/round66/census-start.txt`.
7. S183's committed row has read `status = mined`, `opened = 2026-10-28`,
   `used-by = corpus/knowledge/tb2-grader-vacuity-triage.md` in **every** one of the 18 commits that touched
   `corpus/SOURCES.md` — it was never `queued`. The frozen claims doc's "S183 status `queued` → `mined`" is
   contradicted by the committed bytes; the lesson logs the observed old value (`mined` → `mined`) plus the
   `used-by` append, and reports the conflict rather than editing the frozen doc.
8. The routed item "battery-run.txt pointer" points at `SKILL.md:686` and `.ufo/reports/round-65/kengaku.md:14`
   and `:78`; the closure's own citation of `SKILL.md:83` does **not** carry the string
   (`sed -n '83p' SKILL.md | grep -c 'battery-run'` → `0`, at every revision of `SKILL.md` I checked), and
   `corpus/SKILL.md` does not exist (the lane's `SKILL.md` is at the lane root). The lesson records the
   pointer as measured.
9. `grep -cE '^(BUILD|RUN|FILES|ENV) ' corpus/evidence/round65/battery-run.txt` → `0`;
   the same count on `corpus/evidence/round65/sqlite-gcov-probe.txt` → `20`; `battery-run.txt` is 6 lines
   (5 `CASE` lines + `PREDICATE R65-C1 pass`).
10. `grep -c 'S234' corpus/evidence/round65/census-before.txt` → `1` (it is not a base capture); the base
    count is `git show 12a62551:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → `224`.

## Findings that need the L1's attention (nothing edited)

1. **The two new registry rows must open `teaches` with `supersedes S0NN —`.** As proposed
   (`QuoteGateBuild/proposed/rows.md`) they fail `sources-census.sh validate` with `E04` on S236. The landing
   must write the teaches cells as `supersedes S233 — the amalgamation ships sqlite3.c at 9582521 bytes, …`
   and `supersedes S234 — seven legs execute in file order; …`. Verified clean of E04 and green on the meta
   counter in scratch (`receipts/census-proposed-rows.txt`).
2. **S183's registry change is a `used-by` append, not a status flip** — the claims doc's `queued → mined`
   premise is false against the committed row (see observed value 7). The lesson logs `mined → mined` plus
   `corpus/knowledge/tb2-grader-vacuity-triage.md` → `…, corpus/knowledge/tb2-torch-tensor-parallel-offline.md`
   (the existing citation is real and is kept).
3. **Landing order is bound by census E11**: the new knowledge entry
   `corpus/knowledge/tb2-torch-tensor-parallel-offline.md` and the lesson `corpus/lessons/round-66.md` (both
   named as `used-by` paths) must exist on disk when the registry rows land, or the census reports
   `E11 S183 missing used-by …`. Reproduced in scratch.
4. **The frozen C1 receipt checker accepts a receipt with every `CASE` line removed** (exit 0,
   `PREDICATE R66-C1 pass`), so the predicate's "every `case_sha` and `junit_sha` equals the committed bytes"
   clause is unenumerated on the `CASE` side while it is enumerated on the `VECTOR` side. Reported as
   Mistakes row 10; the frozen probe was not edited. (Independently: FreezeReview F1.)
5. **The claims doc's "the junit directory is receipt-local, so a re-run cannot overwrite committed junit
   bytes" is false as executed** and the frozen control receipt no longer re-checks. Reported as Mistakes
   row 11; the frozen probe and cases were not edited. (Independently: ProbeMutate F-A, FreezeReview F5,
   TensorRecon Finding 1.)
6. **The L1 amended the frozen counter mid-wave, after the wave's seats had measured it.** At 18:28
   `plans/round66_c1_tensor_probe.py` changed in the working tree (frozen sha `c5ef1b54…` → `7640a639…`;
   `git status --porcelain plans/` → ` M plans/round66_c1_tensor_probe.py`), the receipt of record was
   re-issued against it, a per-receipt junit directory appeared (`corpus/evidence/round66/tensor/receipt.junit/`,
   `control-a1.junit/`), and a new control receipt `corpus/evidence/round66/tensor/control-a1.txt` was added
   (checks green; its `junit_sha` values equal the bytes in `control-a1.junit/`). The amendment closes
   Mistakes rows 10, 11 and 12 as measured against the frozen bytes — measured, not assumed (receipt
   `04-amendment-a1-state.txt`, A1/A2/A3/A5). **`plans/round-66-claims.md` carries no `Amendment A1` text
   yet** (`grep -n 'Amendment A1' plans/round-66-claims.md` → no hits), although the counter's own docstring
   cites one. The L1 should land the amendment *with* a dated amendment block in the claims doc, so the
   predicate, the counter's bytes and the receipt of record agree in one committed state. Reported as
   Mistakes row 13; nothing in the lane edited by this seat.
7. **The census `validate` command is not `E`-clean on the lane's own copy in scratch** (many `E11
   missing used-by` for paths I did not copy into the scratch tree); only the E-codes for the rows and
   `used-by` paths under this round's change are reported above, and the live lane census is exit 0.

## Out of scope for this seat (not done, by the item's boundary)

- The L1's landing of the lesson, the knowledge entry, the registry rows, the SCORECARD capability row and
  the dated corrections; the `considerthese/` selection (the SiblingOverlap seat's scope); the round report.
- Any edit to `plans/round-66-claims.md`, `plans/round66_c1_tensor_probe.py`,
  `plans/round65_c1_sqlite_probe.py`, the frozen cases, the frozen table, the receipts or the captures.
