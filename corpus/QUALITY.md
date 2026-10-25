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

- **Q9 — a rejection's reason follows from its evidence.** The source cited
  against a rejected claim must address the same property the claim asserts
  (contamination evidence against a contamination claim, task-validity evidence
  against a validity claim); otherwise the reason is rewritten as a superseding
  row. A correct verdict with a wrong reason is a gate failure.
  Lesson: `corpus/lessons/round-24.md` M21 (S023 rejected Scale's
  contamination claim by citing S006's task-validity audit; caught only by the
  non-author spot-check).
- **Q10 — locations and numbers are re-read by a second seat.** Before admission,
  a seat other than the entry's writer re-opens each cited source and confirms
  every quote location and every number against it (exact cells or a stated
  range, never an approximation such as "~45–48%").
  Lesson: `corpus/lessons/round-24.md` M22 (five location slips and one
  unreproduced range in four sources passed the lane's own Q1–Q8 self-check).

- **Q11 — a pass bar is interval-gated.** A knowledge entry or verdict that calls a binary rate a PASS
  against a bar must show the exact two-sided 95% Clopper–Pearson lower bound at or above the bar; a point
  fraction with a min-n gate is INDETERMINATE until n reaches the zero-error minimum (17 at 0.80), and a
  target with 0 ground-truth trials is UNTESTED, never FAIL.
  Lesson: `corpus/lessons/round-25.md` M24 (r22 `TARGET hyper 10/10 -> PASS` and "hyper validated" stood
  four rounds on a point fraction; `python3 plans/attrib_calibration.py --summary` re-verdicts it
  INDETERMINATE).

- **Q12 — supersedes Q11's second sentence.** A point fraction with errors can also FAIL (CP95 upper bound
  below the bar); INDETERMINATE applies only when the interval straddles the bar, and the zero-error minimum
  (17 at 0.80) is one row of `plans/fixtures/r25/power_table.tsv` (26 / 34 at 1 / 2 errors). A verdict on a leg
  the instrument never predicted carries no PASS (non-firing). Q11 is enforced by
  `python3 plans/attrib_calibration.py --selftest` (A3 boundary anchors), not by prose review.
  Lesson: `corpus/lessons/round-25.md` M24, M31 (falsify seats RevQ11, CritSpecificity).

- **Q13 — an admit lands only after its second-seat re-read is on record (extends Q10).** The commit that
  admits an entry must already contain, in its own tree, every second-seat (Q10) re-read report its `## Gate`
  row cites; the Gate cell names each such report by repo-relative path, the report's seat is not the entry's
  writer, and a generic reference ("wave-2 seats", "falsify seats", "by wave-N") supports nothing. A Gate cell
  never cites a seat that has not returned. Check: `python3 plans/gate_timing_check.py --lesson
  corpus/lessons/round-<N>.md --commit <admitting commit>` exits 0; red-before: on `--commit 8ea41f9 --lesson
  corpus/lessons/round-25.md` it exits 1 because no second-seat report path is cited (also red at `9d8a00d`).
  Timing is separately proved by the commit trees: 0 falsify reports at `8ea41f9`, first added at `8239a56`.
  The check requires a nonempty regular report from a registered reviewer-like seat, a candidate mention and
  a final verdict, and a candidate `writer:` different from that seat. Presence is not endorsement: Q9/Q10
  still require all cited findings resolved; this check does not decide their truth.
  Lesson: `corpus/lessons/round-26.md` M39; `corpus/lessons/round-25-verifier-spotcheck.md:36-39` and
  `.ufo/waves/round-26/build/CritQ13Mechanism.md` (a later tree or a placeholder is not a landing-time review).

- **Q14 — supersedes Q13's “reviewer-like” ambiguity and clarifies identity authority.** Qualifying re-read
  roles are exactly `reviewer`, `scout`, `critic`, `sentinel`, `revenger`; other, missing or malformed role
  values do not count. A registered scout can re-open a source; a connector's overlap advice or a mutation
  test is not the complete source/number re-read. Reject explicit report writer/author or registry identity
  declarations that equal the candidate writer. Without report-author metadata, identity means the registered
  seat, not independent proof of human authorship. The caller must supply the actual admission commit;
  the checker grades the requested tree but does not discover that commit or interpret review conclusions.
  Check: the Q13 CLI plus `--selftest` role/declared-writer controls; a late-report/same-commit sandbox pair
  separates absent/present support using identical lesson bytes.
  Lesson: `corpus/lessons/round-26.md` M49; `falsify/FxGatePlaceholder.md`, `FxGateGeneric.md`,
  `FxGateWriter.md`, `FxGateCommit.md` under `.ufo/waves/round-26/`.

- **Q15 — commit-tree authority includes report inventory, not just the final exit.** Q13/Q14 checks must
  read the requested commit for both cited report support and total report inventory. A working-copy report
  cannot make an early commit look reviewed, even when some other missing support already keeps exit1.
  `python3 plans/gate_timing_check.py --selftest` includes an identical-lesson two-commit fixture: early
  report present only on disk → exit1/inventory0; later committed report → exit0/inventory1. The worktree
  inventory mutant must fail that fixture. This is structural timing, not source-truth endorsement.
  Lesson: `corpus/lessons/round-27.md` M55; `.ufo/waves/round-27/build/MutGateTiming.md` and
  `plans/fixtures/r27/gate-timing-worktree-{mutant,restored}.txt`.

- **Q16 — extends Q15 to complete traversal and isolated fixture writes.** Q15's one-report example is
  strengthened to two separately cited reports: identical lesson, early exit1/inventory0 while reports
  exist only on disk, later exit0/inventory2. Both worktree-inventory and parse-tree early-break mutants
  must fail the selftest. All Git writes in that selftest use a temporary repository and an isolated
  environment: inherited repository/index/worktree/object/config/template/hook selectors cannot redirect
  writes; a caller-selected sentinel index remains unwritten. This does not change read-only admission
  truth or make structural support an endorsement. `python3 plans/gate_timing_check.py --selftest`.
  Lesson: `corpus/lessons/round-27.md` M62; `falsify/FGateQ15.md`, `falsify/FGateMutant.md`;
  `plans/fixtures/r27/gate-timing-v2-worktree-{mutant,restored}.txt` and
  `plans/fixtures/r27/gate-timing-parse-tree-mutant.txt`. Earlier one-report receipts remain historical.
  Production read-only Git calls also bind authority to the requested `--repo`, ignoring inherited
  GIT_DIR/object-directory selectors; the hostile bare-victim probe must read the requested tree and
  leave the victim/object sentinel unchanged. Final receipts: `plans/fixtures/r27/gate-timing-v3-*`.

- **Q17 — literal reference coverage is not source endorsement.** A calibration claim about source-use
  consistency names its frozen source/path population, its exact lexical/semantic matching contract,
  and both source-row and row-file-link denominators. A corrective/supersession mention indexed under
  a literal contract remains explicitly corrective; it never revives the superseded teaching. Show
  the identical checker failing on a committed baseline export and clearing the named finding with
  only allowed-cell changes; if another finding remains, do not call that intermediate state clean.
  Current bounded check: `python3 plans/registry_check.py --summary` / `--selftest`, population
  `plans/fixtures/r28/registry/population.json`. It does not establish source truth or cover new files.
  Lesson: `corpus/lessons/round-28.md` M65/M67/M72; failure-capable evidence
  `corpus/evidence/round28-calibration/build-acceptance/registry-only-delta.json` and its red/green stdout.

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
- **R11 — a report's L0 questions reach the queue.** Every `kengaku | round-<N> |` question in the round report's `## L0 questions` is appended to `.ufo/l0-questions.md` before the report lands. Check: `sh plans/l0_filed_check.sh .ufo/reports/round-<N>/kengaku.md .ufo/l0-questions.md` (fleet paths) exits 0. Lesson: corpus/lessons/round-25.md M23.
- **R12 — current-state assertions re-derive at close.** SCORECARD capabilities and axis basis, SHONEN canonical form, PROVINCE surface rows and the corpus index are re-derived by command, not by heading presence; a stale assertion is closed by an appended correction that itself re-derives. Check: `python3 plans/state_check.py --summary` exits 0 (superseded rows counted separately). Lesson: corpus/lessons/round-25.md M25, M26.
- **R13 — one artifact, one claim.** No claim's counting command counts an artifact another claim of the same round creates; each claim's count is re-run with the other claim's paths reverted and must not move. Check: the round's pre-registration names each claim's population and its freeze commit, and the report states the revert test result. Lesson: corpus/lessons/round-25.md M27.
- **R14 — supersedes R4's Check.** R4's awk reads field 2 of `## Surfaces`, which is the surface name, so it cannot see the table it governs. Check: `python3 plans/state_check.py --summary` reports every `## Surfaces` row with a missing first local path as MISMATCH unless the row carries `**ABSENT**` or `**ABSENT <date>**`; endpoint-first rows are offline-unverifiable. Lesson: corpus/lessons/round-25.md M35 (falsify seat RevProvinceAbsent).
- **R15 — supersedes R11's Check.** Run from the fleet root: `sh kengaku-shokunin/plans/l0_filed_check.sh .ufo/reports/round-<N>/kengaku.md .ufo/l0-questions.md` exits 0 (the paths in R11 resolve from no single directory). When the round prompt makes the integrator the appender, an unfiled question is routed to the integrator, not mined as a lane mistake. Lesson: corpus/lessons/round-25.md M23 correction (falsify seat LessonM23).

## Round29 criterion — forecast resolution scope

- **Q18 — a forecast freezes its resolution criterion.** Before seeing output, name the measured unit,
  population and category rule (e.g. JSON-path role versus URL-shaped value). If the frozen wording admits
  incompatible outcomes, record the forecast UNSCORABLE; observed counts may still be reported but supply
  no prospective calibration credit. Lesson: `corpus/lessons/round-29.md` M89; `.ufo/waves/round-29/falsify/FCritForecasts.md`.

## Round29 attempt-2 criterion — wave yield is recorded

- **Q19 — a round records what its seats bought.** Every round appends one row per dispatched seat to
  `.ufo/waves/yield.tsv` (role family, report path, whether it caused a landed correction, supersede or
  verdict change, and the commit that carries it) and reports yield per role family. A family at zero
  yield for two consecutive rounds is merged or cut. The proposal and its measured motivation — first-pass
  yield 1/179 in round 25 and 11/125 in round 26 — are `considerthese/2026-10-21.md:44-49` (2026-10-21);
  the absence check at round 29 is `test -e .ufo/waves/yield.tsv` → exit 1 and
  `grep -rn 'seat.?yield\|yield\.tsv' plans corpus *.md` → 0 hits. Landed as a criterion, not an
  implementation: round 29 spent its claim slots on assimilation and the adoption gate.
  Lesson: `.ufo/waves/round-29/attempt2/build/R29a2Considerthese.md`.

## Round30 criterion — a gate landing carries an out-of-band run

- **Q20 — a landing that touches a gate carries a mechanical run made outside the working copy.**
  A commit touching `grader.py`, `plans/*.py`, `plans/*.sh`, the `corpus/SOURCES.md` schema or
  `.github/` must cite a gate run made in a landing tree extracted from the commit
  (`git archive <sha> | tar -x -C <tmp>`), printing the exit code and the pinned count line of every
  gate it names: `python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1` plus its
  `VERDICT: PASS`; `plans/sources_adopt.py --selftest` → a `SELFTEST cases=N failed=0` line;
  `plans/registry_check.py --selftest`, `plans/config_projection.py --selftest`,
  `plans/benchmark_spec_audit.py --selftest` → their CASE counts. A count that differs from the
  previous commit is a failure unless the same commit's diff explains old→new with a reason.
  Check (executable, one command): `d=$(mktemp -d) && git -C . archive <sha> | tar -x -C "$d" && (cd
  "$d" && python3 grader.py | grep -E 'CHECKS n=|VERDICT:'; for t in sources_adopt registry_check
  config_projection benchmark_spec_audit; do python3 plans/$t.py --selftest | tail -1; done; for t in
  gate_timing_check state_check; do python3 plans/$t.py --selftest; done)` — every line must match the
  previous landing's receipt for that gate, and the receipt is committed with the landing that cites it
  (`.ufo/waves/round-<N>/gate-receipt.txt`). **The roster closes over the touched gate:** a commit that
  edits a gate tool also runs *that tool's own* row, so a landing touching `plans/grader_perturb.py`
  must carry `caught=12`, not just five green strangers (a falsify seat shipped a fully green five-gate
  run while the touched tool's own gate read `MUTATION-CATCH FAIL … failed=1`).
  `plans/sources_adopt.py --selftest` prints `SELFTEST cases=<n>` where `<n>` is a value (10 at
  `363a4eb`, 14 at `623c1fc9`), never a literal `N`. The fleet census is
  `sh scripts/sources-census.sh validate --root <fleet root> kengaku`.
  Limits, each measured on scratch copies (`.ufo/waves/round-30/build/R30Considerthese.md` §Limits and
  `.ufo/waves/round-30/falsify/R30FxConsiderthese.md`): an exit-code-only criterion loses (deleting two
  `grader.py` selftest cases leaves `ALL PASS`, exit 0) and **the detector is the PASS-line count, not
  the pinned integer** — on that same tree all five roster gates stay green and `n` stays 733; the
  integer detects shrinkage, not correctness (one check deleted → `n=732`; a tautologised assertion →
  `n=733` PASS), so the gate diff still needs a reviewer; and this is not a non-author verifier by
  itself — `R6` defines non-author by roster id, so a gate run only becomes outside evidence when a
  non-author runs it. It cannot cover `plans/adoption_check.py` — which is green with `--census` from
  the lane and red only from a `/tmp` extraction, a path-derivation argument bug `corpus/lessons/
  round-29.md` M93 already records, not a design property — or the two count-less selftests, named
  here: `gate_timing_check` and `state_check`.
  The proposal and its date are `considerthese/2026-10-24.md` §Self-improvement suggestions 1
  (2026-10-24); the absence check at round 30 is `ls .github` → no such file or directory and
  `grep -n 'author-observed, never non-author closure' LOG.md` → `LOG.md:372`.
  Lesson: `.ufo/waves/round-30/build/R30Considerthese.md`.

## Round31 criterion — a pinned source says it is pinned

- **Q21 — an entry whose source is a pinned revision names the pin in its `recheck:` line.**
  A pinned revision is a *historical* object: re-fetching the same URL on the default branch returns
  different bytes, so "re-check this source" is not an instruction a reader can follow unless the pin is
  named. An entry whose `source:` lines carry a commit (or a dated snapshot) must therefore name the same
  pin, or the cadence that re-pins it, in its `recheck:` line; an entry whose sources are live documents
  must instead name the fetch. Measured absence at the criterion's creation (2026-10-25):
  `grep -lE '^source:.*[0-9a-f]{40}' corpus/knowledge/*.md | wc -l` → **5 of 40** and
  `grep -lE '^recheck:.*(commit|pinned|pin)' corpus/knowledge/*.md | wc -l` → **5 of 40**, so 35 entries
  give a reader no way to tell a pinned claim from a live one. Check (executable, one command):
  `for f in corpus/knowledge/*.md; do grep -qE '^source:.*[0-9a-f]{40}' "$f" && ! grep -qE '^recheck:.*(commit|pinned|pin|[0-9a-f]{7})' "$f" && echo "unpinned $f"; done`
  — a pinned-source entry that prints is a failure.
  The proposal and its date are `considerthese/2026-10-24.md` §Self-improvement suggestions 2
  ("put an as-of date and a live/dead status on every knowledge entry, then re-probe the live ones",
  2026-10-24). Limits: this criterion is the cheap half of that proposal — it does not add an `as_of`
  field, does not classify a source live/historical/dead, and cannot tell whether a *live* source's claim
  is still true; it only forbids a pinned claim from hiding its pin. Lesson:
  `corpus/lessons/round-31.md` §Assimilation record.
