# QUALITY — kengaku's bar for its own corpus

Created round 24 (2026-10-19). What a `corpus/knowledge/` entry must clear to be
admitted, and what a round must show before it closes. Every criterion cites the
lesson that produced it. Criteria are superseded by a new row that names the row
it replaces — never edited in place. Source tiers and the registry live in
`corpus/SOURCES.md` (tier definitions: `SOURCES-CONTRACT-v1`); the research
method stays chousa's (`chousa-shokunin/SKILL.md`). This file holds neither.

## Admission bar — knowledge entries

An entry is admitted only when every row below passes; the round lesson's
`## Gate` records the pass/fail per entry and every rejected candidate.

- **Q1 — the triad opens the entry.** The first three lines are `source:` (the
  `S###` row id(s), the URL, and the exact anchor), `verified-at:` (ISO date the
  source was opened for this entry) and `recheck:` (ISO date or cadence **and**
  the re-check action). A recheck line with no date and a path written as
  current after it vanished are the defect this prevents.
  Lesson: `corpus/lessons/round-16-recensus.md` §Named debt (absent paths
  "all still written as current in `SKILL.md`/`PROVINCE.md`");
  `corpus/lessons/round-13-coverage.md` §Gate (an annotation needs "capture
  date, retained-evidence limits and a recheck").
- **Q2 — tier floor.** Each load-bearing claim rests on ≥1 `SOURCES.md` row of
  tier A or B *for that claim's scope*; a tier-C row never stands alone, and a
  `community` row is never tier A (tier definitions: SOURCES contract v1,
  restated in `corpus/SOURCES.md`).
  Lesson: `corpus/lessons/round-1-aggregator-audit.md` §Verdict — the corpus
  was NOT conformant on citation-level defects alone, which the audit treats
  as hard; a weakly sourced claim is a failure, not a style issue.
- **Q3 — claim stays inside its quote.** Each load-bearing sentence maps to an
  anchored quote (≤25 words, with location; the length rule is SOURCES
  contract v1 rule 1); a paraphrase may narrow the quote, never widen it.
  Lesson: `corpus/lessons/round-9.md` ("Direction replicating is not magnitude
  replicating" — the r8 headline read stronger than its evidence).
- **Q4 — negative space is written down.** The entry states what its sources
  do **not** establish and the observation that would falsify the claim. An
  indeterminate or detector-negative result is reported as such, never
  laundered into a positive.
  Lesson: `corpus/lessons/round-9.md` ("indeterminate is the one that must not
  be laundered"); `corpus/lessons/2026-10-16-round22-leg-coverage-forcing.md`
  (what closing the untested legs must not claim).
- **Q5 — every source is labelled for what it is.** A lab's disclosure about
  its own benchmark or model is labelled a self-report, not an independent
  replication; a canonical older method is labelled canonical, not current art.
  Lesson: `corpus/lessons/round-13-coverage.md` §Gate (the same rule applied to
  the lane's own material: "A source digest retained in this corpus is not the
  original source bytes"; a committed response is evidence of the historical
  run, not of a live model).
- **Q6 — extends, never duplicates or overwrites.** The entry names the
  existing entry or coverage row it extends; a weaker entry is superseded by a
  new entry that names it, and numbers are corrected by appended errata, never
  in-place edits.
  Lesson: `corpus/lessons/round-6-aggregator-audit.md` (the `0/12 → 0/17`
  count corrected by an appended errata line, never an in-place edit).
- **Q7 — landed and discoverable in the same commit.** Entry file, its
  `corpus/README.md` index row and its coverage-map row land together; no
  support rests on `/tmp`, `local://` or an unlanded working copy.
  Lesson: `corpus/lessons/round-8.md` ("An unanalyzed run is not a result");
  `corpus/lessons/round-14.md` ("A cold agent follows the index").
- **Q8 — rejections are kept.** Every candidate screened and not admitted is
  recorded with reason and flip condition — as a `rejected` `SOURCES.md` row
  or a `Rejected:` line in the round `## Gate`.
  Lesson: `corpus/lessons/round-13-coverage.md` §Gate (the rejected moves are
  recorded beside the admitted ones).

## Round-closure criteria

A round closes only when every row below holds; a row that cannot be shown is an open item, not a waiver. Each row cites the mistake it closes in `corpus/lessons/round-24.md`; checks are file or command tests, not prose.

- **R1 — corrections are appended, never rewritten.** A corrected count or verdict is a new dated entry that names the superseded line and carries the recompute command; the old line stays byte-identical. Check: `grep -c '<old value>' <file>` still returns 1 and `grep -n '<new value>' <file>` finds the dated entry with its command. Lesson: corpus/lessons/round-24.md M02.
- **R2 — four artifacts and a clean status close a round.** LOG section, SCORECARD section, index rows and a round report exist before the close is claimed, and no round-owned path is left untracked. Check: `grep -c '^## Round <N>' LOG.md SCORECARD.md` → `1 1`, `test -f .ufo/reports/round-<N>/kengaku.md`, and every path in the round's pathspec-limited commit list plus every `git status --porcelain` entry is either committed or named in the report (an explicit round-owned path manifest, not a filename match). Lesson: corpus/lessons/round-24.md M05, M10; corpus/lessons/round-14.md.
- **R3 — an executed round is logged even on FAIL.** Any wave that issues scored requests gets its LOG and SCORECARD section in that round, with the verdict and receipt lines, even when the verdict is FAIL and nothing is admitted. Check: `grep -c '^## Round <N>' LOG.md SCORECARD.md` → `1 1` and the section names the receipt path and verdict token. Lesson: corpus/lessons/round-24.md M14.
- **R4 — absent surfaces are marked where they are declared.** Every `PROVINCE.md` surface row whose path fails `test -e` carries `ABSENT <date>` or a dated erratum in the same round the absence is found. Check: `awk -F'|' 'NR>10 && $2 ~ /`/ {print $2}' PROVINCE.md` yields one path per row, and every miss under `test -e` has `ABSENT` on that row. Lesson: corpus/lessons/round-24.md M17; corpus/lessons/round-16-recensus.md.
- **R5 — a superseded premise gets a dated erratum.** When later receipts overtake a landed note's premise, the note gains a dated erratum naming the receipt and line; the old sentence is not left as current. Check: `grep -n '<stale sentence>' <note>` and `grep -nE 'erratum|superseded' <note>` both hit, and the erratum cites the receipt. Lesson: corpus/lessons/round-24.md M19; corpus/lessons/2026-10-16-round23-stream-surface.md.
- **R6 — lane-dispatched advice is never non-author evidence.** A verifier counts as non-author only when the report names an id outside the round's dispatch roster; L2 critics, scouts and executors cannot fill the outside spot-check of one admit and one reject. Check: the report's `non-author` line names a verifier id and `grep -rn '<id>' .ufo/prompts/` returns nothing. Lesson: corpus/lessons/round-24.md M06, M15; corpus/lessons/round-13-coverage.md.
- **R7 — runs before the freeze are tagged unscored.** Any trial whose UTC precedes the `FROZEN:` line is labelled `unscored` in its receipt and is never cited as coverage; the scored block names the freeze sha. No live request is sent before the frozen battery/table file exists (M09). Check: the `FROZEN:` timestamp is earlier than the first scored `request_ts`, the earliest `request_ts` of any receipt is later than the frozen file's first commit or `FROZEN:` line, and every pre-freeze receipt contains `unscored`. Lesson: corpus/lessons/round-24.md M09, M13.
- **R8 — the round header names the lowest axis and any waiver.** The `## Round <N>` header names the lowest-scoring non-retired axis and either the tie-break or the stagnation waiver that justifies the chosen axis. Check: `grep -nE 'lowest axis|tie-break|waiver' LOG.md` hits inside the `## Round <N>` section. Lesson: corpus/lessons/round-24.md M16; ../AXES.md:33-34.
- **R9 — a coverage claim is pre-flighted against the target class.** Before claiming a target leg, record a forcing pre-flight (mechanism, request, observed result) and name lost seats; a starved pre-flight yields 0 on-target and zero credit, not a redefinition of coverage. Check: the receipt contains `pre-flight` and the on-target count, and the verdict line matches that count. Lesson: corpus/lessons/round-24.md M12; corpus/lessons/2026-10-16-round22-leg-coverage-forcing.md.
- **R10 — census patterns are anchored.** Section censuses use `^## Gate$`, `^## Round <N>$` or an equivalent end-anchor; a prefix match is not a count. Check: `grep -lE '^## Gate$' corpus/lessons/*.md | wc -l` equals the reported number; if an unanchored rerun differs, the difference is named. Lesson: corpus/lessons/round-24.md M20; plans/round24_census.sh.
