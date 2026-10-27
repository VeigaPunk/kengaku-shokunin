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

## Round33 criterion — a receipt is only evidence if something re-runs it at the tip

- **Q22 — a committed counter output is a claim about bytes at a revision; it must re-run at the
  lane tip and reproduce, or it is stale debt.** A `defects=0` / `exit=0` receipt proves the
  counter's reading of the tree it ran on — nothing else. When the receipt and the tip disagree
  (round 31's `gate-cli-exits.txt` greened only at the wrong path; round 32's draft receipt said
  "not the claimed after-state" while seats cited it as closure), the receipt is debt, and the
  honest fix is to re-run the same command on the current tip and commit the new output beside the
  old one. Executable check: every receipt a claim cites must name the revision it was produced
  at, and the round's final receipts must re-run at `git rev-parse master` before the report
  closes.
  The proposal and its date are `considerthese/2026-10-25.md` §Self-improvement suggestions 2
  ("one persistent routed-defect ledger … includes a tip-receipt validator", 2026-10-25) — this
  criterion is the cheap half of that proposal: the per-round counter pattern continues, but every
  final receipt now re-derives at tip. Limits: it does not build the persistent `defects.jsonl`
  ledger the proposal sketches; that stays unimplemented and is named here as debt. Lesson:
  `corpus/lessons/round-33.md`.

## Round35 criterion — a routed defect lives in one ledger and re-runs forever

- **Q23 — every defect a non-author closure routes to this lane enters `corpus/defects.jsonl` with a
  check in `plans/defect_ledger.py` that is red when the row is written; a row says `closed` only
  while its check passes at the tip.** A defect closed in prose and checked by a one-round counter
  (`plans/round30_defects.py` … `round33_defects.py`) is checked once and then forgotten: round 34's
  D1 (round-34 work left untracked) recurs round 33's N1 (round-32 wave paths untracked at the tip,
  `plans/round-33-claims.md:87`), and nothing re-ran N1's check after round 33 closed it. The ledger checker re-runs every row at every
  tip and counts a calibration mismatch for a `closed` row whose check fails and for an `open` row
  whose check passes. Executable check: `python3 plans/defect_ledger.py --lane .` — any
  `agree=NO` line, or a nonzero exit while a round report says its defects are closed, is a failure.
  Each check compares the lane's self-assessment with an observation computed from repo bytes (a
  manifest digest, a tag-stripped capture, the branch tree), so a correctly labelled but false
  sentence does not pass. Shown able to fail: all five round-34 rows red at the round-35 freeze
  (`.ufo/waves/round-35/claims/control-c2-nothing.txt`) and a status-only flip scores `mismatches=4`
  (`control-c2-flip.txt`). The proposal and its date are `considerthese/2026-10-25.md`
  §Self-improvement suggestions 2 ("one persistent routed-defect ledger instead of a new
  `plans/roundNN_defects.py` per round", 2026-10-25); this discharges the debt Q22 named. Limits:
  part (b) of that proposal (block pre-registration when a class recurs twice) is not implemented —
  `recurrence_of` is recorded, not enforced; checks are per-defect functions, so a new routed defect
  still needs code. Mutation scratch runs in a `mktemp` clone outside the lane and commits only
  receipts (round-34 D2: 106,323 committed mirror blobs). Lesson: `corpus/lessons/round-35.md`
  §Mistakes.

## Round36 criterion — a counter of record is attacked by its own junk

- **Q24 — a counter of record for an admitted-entry package is proved, before it scores any data, by a
  frozen battery built from the genuine package's own bytes: the genuine package must be accepted, every
  single-property junk mutant must be rejected, and an unevaluated run is never a rejection.** A counter
  that is only ever pointed at the package it was written for proves that package, not the check. The
  round-35 counter of record accepted all seven junk packages —
  `LEGACY accepted=7/7` (`.ufo/waves/round-36/claims/control-c1-legacy.txt`) — among them an entry of
  eight one-word quotes, `junk` teaches cells, a stub probe that prints the receipt, and an untracked
  leftover file; the same weakness let labelled-but-false D4/D5 lines pass
  (`corpus/lessons/round-35-verifier-spotcheck.md:86`, routed defect 1). So each round's counter carries
  a battery whose control receipts are committed at the freeze, and the cheapest all-junk package is
  built and scored by a seat that is not the counter's author *before* the round's first data receipt is
  committed. The tip-receipt clause is why the ordering matters: `plans/round36_c1_verify.py` runs
  `battery()` (`:217`) and only then the tip re-run inside `r35_d1` (`:267`), so a green aggregate
  cannot be reached by a counter that accepts everything or rejects everything.
  Measured at the criterion's creation (2026-10-25): `ls plans/pkg_gate.py` → `No such file or
  directory`, the counter prints `FIXTURES total=14 false_green=0 false_red=0 unevaluated=14`
  (`.ufo/waves/round-36/claims/control-c1-nothing.txt`), and the round-35 counter prints
  `LEGACY accepted=7/7` (same control set, committed in freeze commit `3241b86`).
  Check (executable, round-36 instance): `python3 plans/round36_c1_verify.py --lane .` must exit 0 and
  print `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0` then `PREDICATE C1 pass`. The
  battery is 14 fixtures built in a `mktemp` git repo from committed round-35 bytes
  (`build_package_fixtures`, `plans/round36_c1_verify.py:126`): P0 genuine plus seven single-property
  junk packages (P1..P7, P7 the all-junk combination) and six D4/D5 line fixtures. Name-blindness leg —
  copy P0 and P7 to directories that carry no fixture id and expect exit 0 and exit 1:
  `d=$(mktemp -d /tmp/k36-ren-XXXX); python3 - "$d" <<'PY'` … `import round36_c1_verify as c` …
  `for fid, want in (("P0", 0), ("P7", 1)):` … `print(fid, "renamed_rc", rc, "want", want)` `PY`
  → `renamed_rc 0` for P0 and `renamed_rc 1` for P7.
  Shown able to fail: the accept-everything control scores `false_green=11 false_red=0`
  (`control-c1-accept-all.txt`), the reject-everything control scores `false_green=0 false_red=3`
  (`control-c1-reject-all.txt`), and the no-gate control scores `unevaluated=14` (`control-c1-nothing.txt`);
  `unevaluated` is printed beside `false_green`/`false_red` so a crash cannot masquerade as a rejection.
  The proposal and its date are `considerthese/2026-10-25.md` §Self-improvement suggestions 2(c)
  ("includes a tip-receipt validator (every `corpus/evidence/**` receipt re-run and byte-compared)",
  2026-10-25) — this criterion takes the pre-data half of it and leaves the persistent ledger to Q23.
  Limits: the battery is single-property mutants, so a junk class no fixture occupies survives (P7 covers
  only the named properties combined, not new ones); 14 fixtures is a budget, not a search; the builder
  names its fixture directories `k36-P<n>-…`, so a gate that keyed on its `--root` basename would pass
  the battery — the rename leg is the cheap defence, not a proof; and no mechanical battery separates
  well-formed false prose from a true claim once every field parses, which stays a reviewer's job (Q10).
  Lesson: `corpus/lessons/round-36.md` §Mistakes (1).

## Round36 criterion — a frozen instrument is repaired in the open window, and its case table does not move

- **Q25 — a frozen instrument that fails its own determinism on the first real run is amended only
  before any seat has scored, by a commit that pins both digests, names the changed lines, and shows the
  deterministic case table byte-identical at both revisions.** Amendment 1 of round 36 is the instance:
  the frozen probe printed a `mkdtemp` path in two assertion texts
  (`corpus/evidence/round36/regex-log-probe-first-run.txt:21-22`), so the frozen W5 check "fresh run
  byte-equal to the receipt" could never hold; the repair replaced the temp directory with `<tmp>` in the
  printed text only (`plans/round-36-claims.md:123-140`), and the amended digest
  `d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc` is pinned in
  `plans/round36_c2_verify.py:41`. What keeps the amendment from being a rule change is the case table:
  `--dry` at the freeze commit and at the amended tip are byte-identical, and both equal the committed
  table `corpus/evidence/round36/regex-log-dry-cases-freeze.txt`. A repair that moved a prediction, a
  case, a check definition or a predicate sentence is a new claim and re-freezes.
  Check (executable, round-36 instance):
  `git show 3241b86:plans/regex_log_probe.py >/tmp/pre_probe.py &&
  python3 /tmp/pre_probe.py --dry | cmp - <(python3 plans/regex_log_probe.py --dry) && echo identical`
  → `identical`, and `sha256sum plans/regex_log_probe.py` gives the pinned `d58194c8…`. The remaining
  legs are the pins and the order: the note names both digests
  (`grep -n 'amended probe digest' plans/round-36-claims.md`), and the amendment commit is an ancestor of
  every commit that first adds a receipt scoring the instrument —
  `git merge-base --is-ancestor acbda2f3936838ba4849f14937fbecb8aed461e5 <first-scoring-commit>`.
  Shown able to fail: `cmp corpus/evidence/round36/regex-log-probe-first-run.txt
  corpus/evidence/round36/regex-log-probe.txt` exits 1 and differs on exactly lines 21-22 — the
  pre-amendment instrument cannot reproduce the receipt, which is the failure this criterion names; a
  `--dry` that differed would be caught by the `cmp` above.
  The question this criterion does not settle is open on the L0 queue: `revenger | round-69` asks whether
  an instrument defect (not the artifact under test) may be repaired pre-scoring as a new revision with a
  fresh red-before, or whether the claim must stand falsified and wait a round
  (`.ufo/l0-questions.md:160`); `kumitate | round-63` and `round-64` ask the neighbouring question —
  whether a post-freeze enlargement or relaxation of a control set is a ratchet or a rule change
  (`:167`, `:170`). This criterion takes the position both can live with: a repair is admissible only
  while the case table is unmoved and no seat has scored, and the window's admissibility stays the
  operator's.
  Limits: commit order is the only mechanical witness — an untracked seat build directory leaves no
  commit, so a seat that scored before the amendment and reported later is invisible to the ancestry
  check; `--dry` identity proves the printed case table only, so an amendment to a non-`--dry` code path
  (there was none here) would pass it; and the criterion does not decide whether a pre-scoring repair
  voids a claim, so a round that amends still reports the verdict either way.
  Lesson: `corpus/lessons/round-36.md` §Mistakes (2).

## Round37 criterion — an anchor digest resolves to committed bytes

- **Q26 — every `sha256` token in a `SOURCES.md` registry row is in the row's `anchor` cell, is 64
  lowercase hex (or a declared prefix ending in `…`), and equals a digest of committed bytes under
  `corpus/evidence/` or a digest listed in a committed `SHA256SUMS` there; a wrong token is corrected only
  by an appended `Erratum (round 37): S<id> anchor sha256 …` lesson line that carries the wrong token and a
  64-hex digest that itself resolves.** The anchor cell is where a row says "these are the bytes I read",
  and a digest that lost a character still parses: the round-36 spot-check found S110's anchor carrying 63
  hex while the manifest, the capture and the live bytes carried 64
  (`corpus/lessons/round-36-verifier-spotcheck.md:71`) and routed the missing check (`:88`). Check
  (executable): `python3 plans/anchor_digest_check.py --lane .` → `rows=<n> tokens=<n> defects=0`, exit 0
  (contract in its docstring; it reads committed blobs only, so an uncommitted capture cannot launder a
  digest). Shown able to fail: on the lane at `3ea9a1d9` it prints `rows=103 tokens=11 defects=5` — S110
  `digest-short` (63 hex) and S070, S072, S073, S074 `digest-unknown` (true digests of pinned upstream files
  that no committed byte supported) — and `build/R37AnchorSweep.md` §5 records eleven falsifier cases
  (erratum with a wrong correction, correction absent from every manifest, a shortened S108 token, uppercase
  hex, a token moved out of the anchor cell). Round 37 lands the S110 erratum line in
  `corpus/lessons/round-37.md` §Gate and byte copies of the four upstream files in
  `corpus/evidence/round37/anchor-captures/`; the rows themselves are not rewritten (R1).
  Limits: membership, not binding — a 64-hex token that is the digest of the wrong committed file passes,
  and several manifests share basenames, so the pin-to-capture binding stays with the counters that run the
  probe (`plans/pkg_gate.py` P5, `plans/round37_c2_verify.py` V3); a row that names a digest without a token
  (S037 "pinned by sha256 in the script") is not scanned; and a committed manifest edited to list a bad
  digest would launder its rows — those digests are re-derived by the package gate's P5, not here.
  Lesson: `corpus/lessons/round-37.md` §Mistakes (1). Supersedes: none.

## Round37 criterion — an advertised defect class is held only when a fixture kills its silence mutant

- **Q27 — a gate's advertised defect class counts as held only when a single-defect fixture kills
  that class's silence mutant; a class whose mutant no fixture kills is advertised debt.** A
  battery that shows the gate accepts the genuine package and rejects a few junk packages proves
  the battery's reach, not the gate's: the round-36 battery was green at 14/14 while the gate's
  branch silences went untested, so the round-37 counter against the same 14 fixtures and 55
  frozen single-branch mutants prints `MUTANTS total=55 killed=5 survived=50 invalid=0
  null_detected=0` and `PREDICATE C1 fail`, exit 1
  (`.ufo/waves/round-37/claims/control-c1-nothing.txt`) — 50 of the classes the gate's docstring,
  Q24 and the `package-gate` capability row (`SCORECARD.md:564`) advertise changed nothing
  observable on any fixture. Check (executable, round-37 instance): `python3
  plans/round37_c1_verify.py --lane .` prints `BATTERY fixtures=<n> wrong=0 renamed_disagree=0`,
  then `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`, then `PREDICATE C1
  pass`, exit 0, on a clean clone of the landing tip with `plans/pkg_gate.py` at
  `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`. A class is demonstrated
  when its one frozen `old → new` replacement applies exactly once and compiles (`invalid=0`) and
  some fixture's observable result — the pair (exit code, set of clause ids printing `DEFECT`) —
  differs from the unmodified gate's (`killed`); an unmodified copy of the gate must change
  nothing (`null_detected=0`), each fixture must carry the reference's exact verdict and `DEFECT`
  set (`wrong=0`), and every fixture must give the same result under another directory name
  (`renamed_disagree=0`). Shown able to fail: the do-nothing control at the freeze reads
  `killed=5/55`; editing the gate so the mutants stop applying reads `invalid=55`
  (`control-c1-gate-edited.txt`); mislabelling the genuine package a reject reads `wrong=1`
  (`control-c1-mislabel.txt`); and the one-fixture API example kills exactly one further class,
  `killed=6/55` (`control-c1-example.txt`, M08) — which is why the standard is per class, not per
  battery.
  Limits: demonstration is observational — a killing fixture shows the branch is reached and its
  result is visible, never that the check is the right check; the branches excluded from the 55
  are named in `plans/round-37-claims.md` and stay unclaimed (the empty `frozen_instruments`
  branch of P1, every `spec not found` / `root not a directory` setup path, P10's
  `OSError`/`SubprocessError` branch, `run_checks`' clause-crash handler, `main`'s crash→exit-2
  handler, the `--require-clean-tree`/`--rerun` option gating), so a gate can hold this criterion
  and still be wrong on a setup path; the mutant list is the denominator, so a branch nobody wrote
  a mutant for is invisible, and an equivalent mutant found later is reported as a limit of the
  freeze, never removed; a kill records a result difference, not a reason — the result is the raw
  exit code, so a mutant killed by making the gate crash on a fixture counts the same as one
  killed by its clause firing, and single-defect fixtures reduce but do not remove co-occurrence
  (the round-36 all-junk fixture declares `P1,P3,P6,P9`); 55 fixtures is a budget, not a search
  for every reachable defect.
  Lesson: `corpus/lessons/round-37.md` §Mistakes (2); the freeze control is
  `.ufo/waves/round-37/claims/control-c1-nothing.txt`. Supersedes Q24's middle clause, "every
  single-property junk mutant must be rejected", as the proof standard: a property-level battery
  is satisfied by 14 fixtures while 50 branch silences go untested. Q24's ordering rule (battery
  before the first data receipt) and its `unevaluated` leg stand unamended.

## Round38 criterion — a requirement-map label is derived from every violating case

- **Q28 — a requirement-map label is derived from every executed case that violates the requirement, never
  from one witness; every case the row cites must itself violate the row's line.** A map row that names one
  convenient case can be green and wrong at the same time, because a check that reads only the cited cases
  never sees the violating case cited nowhere. The round-37 instance is `corpus/knowledge/tb2-git-webserver-grader.md:107`,
  `| instruction.md:9 | enforced | capitalised, leading-space |`, beside `CASE token-in-body … observed=pass`
  in the same receipt (`corpus/evidence/round37/git-webserver-probe.txt:35`) — a state whose served body is
  not `hello world`, observed passing. Under the map's own definition (`:97-98`, `enforced` = a violating case
  observed `fail`) the row is false, and the frozen counter printed `V7 ok rows=4 bad=0`, `checks=7
  defects=0`, `PREDICATE C2 pass` over it (falsifier receipt
  `.ufo/waves/round-37/falsify/F37CritC2Map/c2-verify-run.txt`; V7 itself re-run by this criterion's seat →
  `(True, 'rows=4 bad=0')`), because `plans/round37_c2_verify.py:192-201` asks only for the
  direction among the **cited** cases. Two wave-2 seats reached it independently
  (`F37CritC2Map` row 9; `F37CritC2Overclaim` F1) and the round-37 closure routed it as D2
  (`corpus/lessons/round-37-verifier-spotcheck.md` §5). The same rule on the same receipt reddens row 8
  (`:106`): its `catch-all-200` witness answers `/hello.html` with `200 hello world`, which satisfies the line
  as written, so it is not a violating case and may not be cited as one (`F37CritC2Map` row 8).
  Check (executable, round-38 instance): `python3 plans/round38_c2_verify.py --lane .` prints
  `V7 ok rows=7 tags=7 bad=0` (one row per `TAG` line of the frozen dry table, seven of them), then
  `checks=7 defects=0`, then `PREDICATE C2 pass`, exit 0. V7's rule
  (`plans/round38_c2_verify.py:239-248`): for each row, the violating set is every receipt case whose
  `violates=` set carries the row's tag; the label must equal `derive` over that set — `enforced` iff all are
  observed `fail`, `unenforced` iff all are observed `pass`, `partly` otherwise (`:205-210`) — and every id the
  row cites in backticks must be a member of that set. Row layout is
  `| \`instruction.md:<L>\` | \`<tag>\` | <label> | <cases> |` with `<L>` the tag's frozen line (`MAP_ROW`,
  `:66`), so a three-cell map copied from the round-37 entry is rejected as an unparsed row rather than
  silently accepted.
  Shown able to fail: the round-37 row 9. Its tag's violating set contains `capitalised` (observed fail) and
  `token-in-body` (observed pass), so the derived label is `partly` and the filed `enforced` trips the
  `label != want` leg (`:243-245`); the round-37 row 8 trips the citation leg (`:246-248`) with
  `catch-all-200`. Neither row is red under the round-37 counter, which is the defect this criterion names —
  the correction of record is the erratum appended at `corpus/knowledge/tb2-git-webserver-grader.md` §Errata
  (round 38), and the new entry's map (`corpus/knowledge/tb2-build-pmars-grader.md`) carries `violates=` tags
  in its receipt so V7 can derive rather than trust.
  Limits: the derived label is only as good as the frozen `violates=` tags — a violating case nobody tagged is
  invisible, and the dry table is the denominator, frozen before the run, so a case added later does not enter;
  "violates" is a human judgement recorded pre-run, so this criterion moves the decision into a reviewable
  artifact, it does not mechanise the semantics; one label per tag collapses a line that carries two clauses
  (row 7's port half and push half), which still needs prose qualification — the erratum carries it; a set with
  one observed verdict derives `enforced` or `unenforced` outright, so a thin tag set passes cheaply; and the
  rule cannot be applied retroactively to a receipt without tags (round-37's has none, `grep -c violates=` →
  `0`), which is why round 37 gets an erratum and not a re-score.
  Lesson: routed item D2, `corpus/lessons/round-37-verifier-spotcheck.md` §5; the two falsifier reports are
  `.ufo/waves/round-37/falsify/F37CritC2Map.md` and `F37CritC2Overclaim.md`. Supersedes: none.

## Round38 criterion — a frozen mutant's kill direction is witnessed, not assumed

- **Q29 — a frozen gate mutant carries a declared kill direction (silence: the clause stops firing;
  mirror: the clause fires on a passing input), and the declaration is checked against what a battery can
  exhibit before the predicate is scored.** A direction written from the mutant's text alone can be
  unreachable: round 38 froze N21 (`sums.splitlines()` → `sums.splitlines()[:1]` in the gate's D5 manifest
  lookup, `plans/round38_c1_verify.py` MUTANTS) as `silence`, but restricting an `any(...)` lookup to a
  prefix makes the clause stricter on every input, so its DEFECT set always contains the reference's and no
  fixture can satisfy the silence rule — the frozen `killed=22` was unreachable by any battery
  (`.ufo/waves/round-38/build/R38BatD5.md` §BLOCKER, found within the first wave-1 hour). Check
  (executable): `python3 plans/mutant_direction_check.py --lane .` prints one `DIR <id> <clause>
  declared=<dir> observed=<set> ok|MISLABELLED|UNWITNESSED` line per frozen mutant and
  `DIRECTIONS total=<n> mislabelled=<m>`, exit 1 iff `m > 0`. Shown able to fail: on the round-38 landed
  battery it prints `DIR N21 D5 declared=silence observed=mirror MISLABELLED`, `DIRECTIONS total=22
  mislabelled=1`, exit 1 (`.ufo/waves/round-38/integrate/direction-check.txt`). Rule: a round that freezes a
  mutant list states, per mutant, whether the replacement makes its clause laxer or stricter, and runs the
  check at its first battery integration; a `MISLABELLED` mutant is an honest stop of the frozen predicate,
  never a relabel after scoring. Limits: `UNWITNESSED` (no fixture separates the mutant yet) is not a
  verdict, so the check cannot run before some battery exists; it observes the attributed rule of the
  counter it loads, not a semantic proof. Lesson: `corpus/lessons/round-38.md` §Mistakes. Supersedes: none.

## Round39 criterion — a class that recurs twice is closed by a gate over committed history

- **Q30 — a mistake class that recurs twice is closed by a gate that reads committed history — red on
  both occurrences and green on the round that lands it — never by a second prose rule.** A forward
  rule leaves nothing to observe. The order-of-operations class (a skip-control that runs the frozen
  instrument before the round's first recorded run) was recorded with a forward fix in
  `corpus/lessons/round-37.md:42` ("the discarded run cannot become evidence … the write-up must not be
  the only artefact") and recurred in round 38 (`corpus/lessons/round-38.md:36`), where the artefact was
  again only the claims header; round 37's stated fix "does not prevent the ordering, it only makes the
  discarded run harmless" (same row). The round-38 closure named the shape the class needed —
  "Append a correction and turn the lint into a gate with a red-before state"
  (`corpus/lessons/round-38-verifier-spotcheck.md:162-165`, routed item R3) — and the recurrence is the
  case `considerthese/2026-10-25.md:42-44`, proposal 2(b), predicted. The gate is
  `plans/order_check.py`: it reads commits only (working tree and index ignored) and FAILS when a file
  committed under `.ufo/waves/round-<N>/claims/` at or before the first commit adding the receipt shows
  the frozen probe executed (a `P10` line whose detail is anything but `receipt unreadable`, or a
  receipt-shaped `CASE … observed=` line), when the freeze commit already contains the receipt, and when
  the receipt was committed before the claims file; exit 2 on setup errors, never a silent pass.
  Measured at the criterion's creation (2026-10-26, before the tool landed): `ls plans/order_check.py` →
  `No such file or directory`; `grep -c 'order-of-operations' corpus/lessons/round-37.md
  corpus/lessons/round-38.md` → `1` and `2` (one row, one cross-reference to it); every occurrence was
  closed in prose.
  Check (executable, round-39 instance) — the pair that makes this a gate rather than a rule:
  `python3 plans/order_check.py --lane . --claims plans/round-38-claims.md --receipt
  corpus/evidence/round38/build-pmars-probe.txt` prints `ORDER HIT
  .ufo/waves/round-38/claims/control-c2-skip.txt@e0a378539a45:11 kind=gate-p10`, quoting the control
  line `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`, then `ORDER RESULT FAIL`,
  exit 1; and the same
  command with `--claims plans/round-39-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt`
  prints `ORDER scanned commits=1 file_entries=7 distinct_blobs=7`, `ORDER RESULT PASS`, exit 0 — round
  39's only `P10` line is the exempt `P10 DEFECT receipt unreadable`
  (`.ufo/waves/round-39/claims/control-c2-nothing.txt:11`).
  Shown able to fail: the recurrence's origin is red as well — `--claims plans/round-37-claims.md
  --receipt corpus/evidence/round37/git-webserver-probe.txt` → `ORDER HIT
  .ufo/waves/round-37/claims/control-c2-skip.txt@ca790460e9b7:12`, `ORDER RESULT FAIL`, exit 1 — and
  three synthetic two-commit repos make each leg bite alone: claims+receipt in one commit → `ORDER FAIL
  freeze-contains-receipt`, exit 1; receipt committed first → `ORDER FAIL freeze-contains-receipt
  receipt-before-claims`, exit 1; clean freeze-then-receipt → `ORDER RESULT PASS`, exit 0 (the tool is
  not always red).
  Limits: commits only — an executed probe whose output was never committed is invisible, and round 38
  is red only because its skip control kept one `P10` line; the `receipt unreadable` exemption is
  textual, so an instrument that prints that detail after executing would be excused; `CASE …
  observed=` binds the probe's line shape, so another instrument needs its own pattern; the gate detects
  and does not block, so 2(b)'s "blocks pre-registration" half stays unimplemented, and Q23's limit line
  (`corpus/QUALITY.md:291`) is named here, not amended (R1); no `recurrence=2` row is written to `corpus/defects.jsonl`
  (its checker is the round-35 frozen `plans/defect_ledger.py`, which has no check for this class; routed); and a gate that only ever runs on the round that
  introduces it proves nothing, which is why the red pair is part of the check.
  Lesson: routed item R3, `corpus/lessons/round-38-verifier-spotcheck.md` §5 item 3; occurrences
  `corpus/lessons/round-37.md:42`, `corpus/lessons/round-38.md:36`; proposal
  `considerthese/2026-10-25.md:42-44`. Supersedes: none.

## Round41 criterion — a frozen predicate's denominator is a literal the counter cannot self-satisfy

- **Q31 — a frozen predicate of the shape `MUTANTS total=<n> killed=<n> survived=0` is non-vacuous only when
  the counter binds the total and a per-tool floor to module literals and its pass conjunct reads them; a
  predicate whose only guard is `len(MUTANTS) == TOTAL`, with `TOTAL` written by the same author who writes
  the list, is satisfied by an empty list.** The round-41 plan as landed in round 40 failed exactly here: a
  copy of the round-40 counter with four appended lines (`MUTANTS = []`, `TOTAL = 0`) printed the full green
  predicate — `MUTANTS total=0 killed=0 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`, exit 0 —
  with the landed battery present (`.ufo/waves/round-40/falsify/F40CritPlanNext.md:30-33`; receipt
  `F40CritPlanNext/runA-vacuous.txt:24,26`), and the plan's drafted predicate left `<n>` unbound
  (`F40CritPlanNext.md:105-115`, D1). The round-41 freeze binds both: `plans/round41_c1_verify.py:123-124`
  `TOTAL = 23`, `FLOORS = {"receipts": 13, "sources": 10}`; `:640-641` requires every floor ≥1,
  `sum(FLOORS.values()) == TOTAL`, and each tool's `[counted, killed]` equal to `[floor, floor]`; `:642` puts
  `len(MUTANTS) == TOTAL and floors_ok` in the pass conjunct; and `:631` prints
  `MUTANTS-BY-TOOL receipts=<k>/<n> sources=<k>/<n>`, so one total cannot stand for two tools. The
  discriminating control D2 asked for is committed and red with the literal untouched: the frozen counter
  copied with one appended line `MUTANTS = []` (`claims/control-c1-no-mutants.patch`, hunk `233a234`) prints
  `BATTERY fixtures=22 wrong=0 tampered=0 sidechannel=0` (`claims/control-c1-no-mutants.txt:24`),
  `MUTANTS total=0 killed=0 survived=0 invalid=0 null_detected=0` (`:25`), `MUTANTS-BY-TOOL receipts=0/0
  sources=0/0` (`:26`), `PREDICATE C1 fail` (`:29`), `exit=1` (`:30`), with `TOTAL = 23` and `FLOORS`
  unchanged — so the red is the binding and not a second edit, and it is sharper than the round-40
  falsifier's own copy, which zeroed the total as well.
  Check (executable, round-41 instance): `python3 plans/round41_c1_verify.py --lane .` prints `PINS total=2
  mismatched=0`, then `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, then `MUTANTS total=23
  killed=23 survived=0 invalid=0 null_detected=0`, then `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`, then
  `PINS-AFTER mismatched=0`, then `PREDICATE C1 pass`, exit 0; the one-line-emptied copy prints
  `MUTANTS total=0` … `PREDICATE C1 fail`, exit 1. Both controls are committed with the freeze
  (`8ef8b4fc`), before `plans/battery41` existed (`ls plans/battery41` → `No such file or directory`,
  2026-10-26), so neither is fitted to the battery; the counter's own digest is a freeze row
  (`claims/frozen-digests.txt`: `8835a94b…  plans/round41_c1_verify.py`), which is what makes an edit of the
  list *and* the literals together visible at closure.
  Shown able to fail: the falsifier's run A is green with the list empty — the defect this criterion names; at
  the round-41 freeze the two controls are red for different reasons: no battery prints `BATTERY fixtures=0`,
  `MUTANTS total=23 killed=0 survived=23`, `PREDICATE C1 fail` (`claims/control-c1-nothing.txt`), and one
  appended line in `plans/tip_receipts.py` prints `PINS mismatched=1`, the 13 receipts mutants `invalid`,
  `PREDICATE C1 fail` (`claims/control-c1-tool-edited.txt`); a development run cannot be filed as either,
  because `--battery-dir`/`--only` print `PREDICATE C1 n/a …` (`claims/control-c1-hostile.txt:32`).
  Limits: the floors are literals the same author writes as the list, so the binding proves the list was not
  emptied and never that 23 is the right denominator (Q27's "the mutant list is the denominator" stands — a
  round can clear a 13/10 floor with reachable mutants only); the control is a copy plus a patch, so it prices
  the predicate's shape, not the frozen file, and the green half is the round's own predicate, not this
  control; the total counts rows, not distinct replacement sites — a row is only checked for
  `src.count(old) == 1` (`:589`) and mutant ids are not uniqueness-checked (fixture ids are, `:547`), so two
  rows carrying the same replacement both count; the per-tool equality leg makes a mutant's declared `tool`
  cell load-bearing, so a misfile reports `invalid` instead of reddening a floor; and the digest pin sees an
  edit, not a round that freezes low and lands green.
  Lesson: `.ufo/waves/round-40/falsify/F40CritPlanNext.md` §0 and D1/D2 (2026-10-26); discharged in
  `plans/round-41-claims.md` §C1, which states that "the predicate binds `TOTAL = 23` and `FLOORS =
  {receipts: 13, sources: 10}`", and in `plans/round41_c1_verify.py:13-17`. `corpus/lessons/round-41.md` does
  not exist at this draft (2026-10-26: `ls corpus/lessons/round-41.md` → `No such file or directory`), so the
  lesson pointer moves there when the round writes it. Supersedes: none; extends Q27's fourth limit and Q24's
  ordering leg (a control lands with the freeze, not after the first score).

## Round41 criterion — an attack seat's sandbox is part of its evidence

- **Q32 — a seat that runs a counter, a battery or a fixture build runs it inside a sandbox that makes every
  shared PATH directory and the host home read-only, with only its fixture root and a private tmp writable; its
  receipt carries the envelope command, a post-run check that the forbidden target is absent, and `date +%T`
  for every write it makes outside its report and its scratch dir.** A host-safety breach is not a style
  defect: round 40's `R40CritC1Counter` wrote a `git` shim, from inside the counter's build child, to
  `/home/vgpnk/.local/bin`, "a shared host directory ahead of `/usr/bin` on every lane's PATH"
  (`corpus/lessons/round-40.md:67`), and "the seat's receipts do not timestamp the writes"
  (`corpus/lessons/round-40.md:69`), so the window had to be inferred from other lanes' failures at
  ~14:05–14:07 -03 (`:69-71`); the attack's scoped form measured the same result, so the ambient write
  "bought nothing" (`:73`). The round-40 closure routed it as R2 (`corpus/lessons/round-40-verifier-spotcheck.md:95-96`)
  and neutralized both attack modules, which now raise `SystemExit` at import and point `SHIM_DIR` at
  `/nonexistent` (`build/R40CritC1Counter/crit_git_shim.py:10-12,18`, `crit_ledger_selfread.py:9-11`); measured
  2026-10-26:
  `ls -l /home/vgpnk/.local/bin/git` → `No such file or directory`. The round-41 implementation is the
  counter's own envelope — builds and tool runs in `bwrap --ro-bind / /` with the lane hidden,
  `--unshare-pid --unshare-net`, a fixed system PATH and `HOME=/nonexistent`
  (`plans/round41_c1_verify.py:56-70`, `:116`, `:318-325`) — plus a freeze control written to try the round-40
  vectors: `claims/hostile/h_host_writes.py` ("Targets are marker files under the user's home, NOT a PATH
  directory, so a sandbox failure is harmless", `:1-2`), whose receipt prints `SIDECHANNEL
  hostile/h_host_writes.py tokens=/home/` (`claims/control-c1-hostile.txt:2`),
  `build_write=OSError.lane_read=FileNotFoundError` (`:3`), `sidechannel=1` (`:27`) and `markers after the run:
  ls: cannot access '/home/vgpnk/k41-hostile-*': No such file or directory` (`:34`). Measured absence at the
  criterion's creation: `grep -c 'host-safety\|Host-safety' corpus/QUALITY.md` → 0 and
  `grep -c 'bwrap\|read-only-PATH' corpus/QUALITY.md` → 0; Q20 and Q23 govern where a gate run and a mutation
  clone live, not what the sandbox may write or what the receipt must show.
  Check (executable, round-41 instance): the two red halves are one command each —
  `grep -n 'markers after the run' .ufo/waves/round-41/claims/control-c1-hostile.txt` prints line 34 with
  `No such file or directory`, and `ls -l /home/vgpnk/.local/bin/git` fails with the same message; the forward
  leg is a per-receipt sweep — every report a round's claim cites as having run a counter, battery or fixture
  build contains its `bwrap … --ro-bind` line and a timestamp line for each host write it made, and the round
  names the sweep's result in its report.
  Shown able to fail: the incident itself — the shim sat outside every fixture directory, so no fingerprint
  covered it (`corpus/lessons/round-40.md:67-71`); a re-run of either neutralized module is an import-time
  `SystemExit`, not an attack; and on the round-41 control the token scan catches a hostile module by name
  (`sidechannel=1`) while the sandbox denies the write (`build_write=OSError`) and the marker set is empty
  after the run (`:34`).
  Limits: the token scan is textual, so a module that names no forbidden token while writing there is invisible
  — the sandbox, not the scan, is the guard; the receipt quotes the envelope and does not prove the flags, so a
  forged receipt passes and only a non-author re-run (Q10) prices it; `--ro-bind / /` says nothing about the
  network or pids (`--unshare-net`/`--unshare-pid` do, unverified by the receipt); `date +%T` is seat-supplied
  text and proves order, not authorship; the criterion cannot reach a write made before the sandbox exists,
  which is exactly the round-40 case (a build child in a pid namespace over a shared filesystem), and a vector
  the envelope does not name — a socket to a host daemon, a shared device — stays open; and it protects
  neighbours, not the claim: a shim scoped under the seat's own scratch is compliant and measured the same
  attack result (`corpus/lessons/round-40.md:73`), so a green attack receipt says nothing about the counter's
  soundness.
  Lesson: `corpus/lessons/round-40.md:64-75` §Conformance incident; routed item R2,
  `corpus/lessons/round-40-verifier-spotcheck.md:95-96`; controls `plans/round-41-claims.md` §C1 "Other
  controls". Supersedes: none; extends Q23's scratch clause (where the scratch lives) with how it runs and
  what the receipt must show.

Round-41 wave-2 errata to Q31/Q32 (`F41RevQuality` D1–D3; appended, criteria text not rewritten):
- Q31 Lesson line: `corpus/lessons/round-41.md` now exists; the pointer is its `## Mistakes` row "Frozen predicate
  satisfiable with zero round-41 work".
- Q32: the "bought nothing" quote is `corpus/lessons/round-40.md:74`, not `:73`.
- Q32 forward-leg sweep, named as the criterion requires: of the receipts round 41 cites, the L1's seven
  (`claims/witness-run.txt`, `claims/control-c1-{nothing,no-mutants,tool-edited,hostile}.txt`,
  `integrate/measure-{baseline,final}.txt`) carry no `bwrap` envelope line and no timestamp line — the L1 ran the C1
  counter outside the seat envelope (the counter sandboxes every build and tool run itself, `--ro-bind / /`), and made no
  host write outside the lane and scratch. Seat receipts: wave-1 and wave-2 attack reports quote the envelope
  (e.g. `R41RevWitness.md` §1, `F41CritC1Count.md` §0). Result: Q32's forward leg is red on the L1's receipts this round;
  the criterion stays as written and binds L1 counter runs from round 42.


## Round42 criterion — a carried direction cell is re-derived through the frozen counter before freeze

- **Q33 — a kill-direction cell carried from another round's campaign into this round's mutant table is
  re-derived from that campaign's own recorded reference/mutant outcome before the table is frozen, and the
  re-derivation is priced by a control that restores the carried cell and reddens the predicate.** Q29 binds a
  *frozen* mutant's direction and cannot run before a battery exists — its own Check line says `UNWITNESSED`
  "is not a verdict, so the check cannot run before some battery exists" (`corpus/QUALITY.md:516-517`) — so a
  table inherited from a prior round is exactly the object that escapes it. Round 40 exhibits the gap: its
  near-variant table labelled `XO5` and `XO6` `rc-silence`
  (`.ufo/waves/round-40/falsify/F40XMutLedgerOrder.md:70-71`) while its own §2 witness text recorded the opposite
  pair for both — "the reference scans `commits=1` and PASSes; the mutant scans `commits=2` … → FAIL rc=1"
  (`:122-124`), and "a claims blob `P10 PASS receipt unreadable` is invisible to the reference and a HIT to the
  mutant" (`:127-128`). Under the round-42 counter's own vocabulary (`plans/round42_c1_verify.py:42-45`:
  `rc-silence` = fixture `expect=reject`, reference exits 1, mutant exits 0; `rc-mirror` = fixture `expect=accept`,
  reference exits 0, mutant exits 1) those recorded pairs are `rc-mirror`: reference 0 → mutant 1, the mutant
  STRICTER. The round-41 plan carried the list without re-deriving it (`plans/round-42-claims.md:105-109`), and
  round 42's freeze re-derives both to `rc-mirror` (`plans/round42_c1_verify.py:38-41`, table rows `:201`, `:206`).
  Measured at the criterion's creation (2026-10-26, this lane, tip `fda71ae`): `CARRIED-DIRECTIONS total=14
  differ=2 ids=XO5,XO6` — the other twelve carried cells (X1 X3 X6 X7 X9 X12 X13 X14 X15 XO1 XO3 XO7) re-derive
  unchanged at the head, and the three that carry a class keep it too (X6 `digest-wrong-capture`, X7
  `digest-unknown`, X14 `erratum-digest-unresolved`, read off `.ufo/waves/round-40/falsify/F40XMutAnchor.md:71-72,79`
  and `plans/round42_c1_verify.py:156,161,181`).
  Check (executable, round-42 instance), three commands, the first two red and the third the landed green:
  (a) `python3 plans/carried_direction_diff.py --lane .` prints one `CARRIED <id> round40=<cell> round42=<cell>
  same|DIFFERS fixture=<fid> attributed=<Lnnn>` line per carried mutant and `CARRIED-DIRECTIONS total=14
  differ=2 ids=XO5,XO6`, exit 0 — this is a derivation report, not the gate: it prints `differ=2` because the
  freeze corrected two cells, and a freeze that had copied the round-40 labels would print `differ=0` and look
  clean, which is why (b) is the discriminating half (tool draft at
  `.ufo/waves/round-42/build/R42QualityDraft/carried_vs_rederived.py`, sha256 `47151f23…`, to land as
  `plans/carried_direction_diff.py` for this line to run as written);
  (b) restore the carried cells — `git apply .ufo/waves/round-42/claims/control-c1-direction-mislabel.patch`
  (four lines: `XO5` and `XO6` back to `rc-silence`) on a scratch copy of `plans/round42_c1_verify.py`, run it in
  development mode with the witness fixtures — prints `MUTANT XO5 order rc-silence SURVIVED
  exhibits=0>1,rc-mirror` (`claims/control-c1-direction-mislabel.txt:29`), the same for `XO6` (`:30`),
  `MUTANTS total=14 killed=12 survived=2 invalid=0 null_detected=0 unattributed=0` (`:33`),
  `MUTANTS-BY-TOOL anchor=9/9 order=3/5` (`:34`), `PREDICATE C1 fail` (`:37`), `exit=1` (`:38`);
  (c) unpatched, the frozen labels — `MUTANT XO5 order rc-mirror killed by=w-xo5-post-receipt-blob attributed=L117`
  and `MUTANT XO6 order rc-mirror killed by=w-xo6-p10-pass-line attributed=L53`
  (`claims/witness-run.txt:29-30`), `MUTANTS total=14 killed=14 survived=0 … unattributed=0` (`:33`),
  `MUTANTS-BY-TOOL anchor=9/9 order=5/5` (`:34`).
  Shown able to fail: (b) is the red half and it fails on exactly the two restored cells — the receipt shows the
  declared cell and the exhibited set disagreeing on the same line (`declared=rc-silence … exhibits=…,rc-mirror`)
  and the predicate at `killed=12`; the round-40 record itself is the other red half, where a table cell contradicts
  the §2 paragraph three lines above it. The green half is not trivially green either: the same run reports
  `killed=14` only with the re-derived cells, so a round that copies a label without re-deriving it loses a kill
  it could have had.
  Limits: the cell vocabulary is the counter's four names (`silence`, `rc-silence`, `rc-mirror`, `error`, `:42-45`),
  so the re-derivation compares the *head* — X6/X7/X8/X10/X14's round-40 cells carried a class as
  `silence/<class>` (`.ufo/waves/round-40/falsify/F40XMutAnchor.md:71-73,75,79`) and the frozen table keeps it
  in a separate `class` column (`plans/round42_c1_verify.py:156,161,181`, e.g. `('X6', 'anchor',
  'digest-wrong-capture', 'silence', 'direct',`), so `carried_direction_diff.py` compares heads only and a wrong
  class under the right head passes both it and the counter's direction check (the counter still matches the
  fixture's printed classes, `FIXTURE … declared=digest-wrong-capture`); a mislabel's cost is a survivor, not a
  wrong green —
  (b) shows `killed=12` and `fail`, so the failure mode is an honest stop plus a wasted fixture, which is why the
  criterion prices the re-derivation at freeze instead of in the battery; the check reads a *recorded* run
  (`claims/witness-run.txt`), so a wrong label paired with a matching wrong witness would pass (a) and only (b)'s
  independent restore would catch it; twelve of fourteen cells already agreed, so this freeze's discrimination is
  two cells and a wholly copied-and-correct table demonstrates nothing; and Q29's instrument remains the
  post-battery one and defaults to a different counter (`plans/mutant_direction_check.py:92`
  `--counter plans/round38_c1_verify.py`), so it must be pointed at `plans/round42_c1_verify.py` to speak about
  this round at all.
  Lesson: `plans/round-42-claims.md:105-109` §Frontier step (mined mistake, captured-by Q29 "not applied because
  that table was never frozen"); carried-table provenance
  `.ufo/waves/round-40/falsify/F40XMutLedgerOrder.md:70-71` against its own §2 `:120-128`; the class lands in
  `corpus/lessons/round-42.md` §Mistakes when the round writes it (absent at this draft: `ls
  corpus/lessons/round-42.md` → `No such file or directory`). Supersedes: none; extends Q29's direction rule with
  the pre-battery leg Q29's own check cannot reach.

## Round42 criterion — a SOURCES row is corrected by a new superseding row, never in place

- **Q34 — every cell of a `corpus/SOURCES.md` registry row except `status`, `recheck` and `used-by` is immutable
  under its id: a correction lands as a NEW row whose `teaches` cell opens `supersedes S0NN —`, and an in-place
  change is a rule-2 defect even when the round wrote the row itself and the cell it corrects is its own anchor.**
  The rule is written twice and enforced nowhere: `SOURCES-CONTRACT-v1.md:49-51` "Only `status`, `recheck` and
  `used-by` change in place … A correction is a new row whose `teaches` opens `supersedes S0NN —`"
  (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`), restated at
  `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`. No lane tool reads it from committed history: of the tools
  naming `corpus/SOURCES.md`, none calls `rev-list`/`git show`/`git log` (`grep -ln 'corpus/SOURCES.md' plans/*.py`
  crossed with `grep -E 'rev-list|git\.show|git log'` → no file); `plans/registry_check.py` parses the working-tree
  registry only (`parse_registry(text, …)`, `:20`); `plans/state_check.py`'s supersede regexes match round-revision
  lines, not registry rows (`:206`); and `plans/round33_c1_verify.py:170,210` only *writes* the refused-duplicate
  rows (`"supersedes {sid} — duplicate staged row refused"`) without checking any row's immutability. Round 41
  measured one instance and
  routed the fix as prose (R4): in `53b9e4e5` the `S124` `anchor` cell changed in place —
  `git diff --numstat 74513c06 53b9e4e5 -- corpus/SOURCES.md` → `1	1`, old text "`PR body §Proposed PR
  description`", new text "`PR body preamble paragraph (pr245-body.md:11; …)`" — no `supersedes S124 —` row
  exists in the file (`corpus/lessons/round-41-verifier-spotcheck.md:30-36`, routed `:116`). Measured at the
  criterion's creation (2026-10-26, tip `fda71ae`, `python3 …/sources_appendonly.py <lane>` /
  `build/R42QualityDraft/receipt-lane.txt`): `SOURCES-COMMITS scanned=36 rows_at_tip=117`, `SOURCES-APPENDONLY
  violations=15 arity=0`, exit 1 — the class is older and wider than the routed item: `S081 scope`, `S082 anchor`
  (`706ed3f2`), `S086 tier` + `S086 scope` (`9af639c9`), `S092 anchor`, `S100 anchor` (`f6422263`), `S100 anchor`
  (`634ded8e`), `S103 source`, `S104 source`, `S104 teaches` (`6c20dd8d`), `S105 anchor`, `S107 anchor`
  (`1d4084fa`), `S046 anchor`, `S052 anchor` (`ec172168`), `S124 anchor` (`53b9e4e5`) — 15 cells in 8 commits
  across rounds 30, 31, 33, 35, 40 and 41, and none of the 15 was ever repaired by a superseding row for that id
  (`repair_row=none` on all 15; a second run also asked whether a `supersedes` row appeared in ANY later commit:
  `supersede_same_or_later=NO` for all 15). The mechanism is not invented here:
  `grep -c 'supersedes S0[0-9][0-9]' corpus/SOURCES.md` → `17`, of which 15 are correcting rows —
  `S026←S023 S036←S025 S039←S034 S040←S035 S042←S030 S047←S037 S048←S043 S058←S050 S064←S054 S066←S038
  S067←S066 S068←S061 S069←S062 S075←S071 S076←S075` — and two are refused-duplicate records that name
  themselves (`S094`, `S097`: "duplicate staged row refused after registry collision").
  Check (executable, round-42 instance): `python3 plans/sources_appendonly.py --lane .` prints one
  `CELL <sha8> <id> <cell> repair_row=same-commit|none` line per in-place non-mutable-cell change, then
  `SOURCES-COMMITS scanned=<n> rows_at_tip=<n>` and `SOURCES-APPENDONLY violations=<n> arity=<n>`, exit 1 iff
  `violations>0`; it reads commits only (`git log`/`git show` over `corpus/SOURCES.md`), so the working tree and
  index cannot satisfy it. On the lane tip it prints `violations=15`, exit 1 (red list above). The check is not
  always red: a two-commit fixture whose second commit only ADDS a row opening `supersedes S001 —` prints
  `SOURCES-COMMITS scanned=2 rows_at_tip=2`, `violations=0`, exit 0, and the same fixture plus a third commit that
  edits `S001`'s `anchor` in place prints `CELL 6888d84c S001 anchor repair_row=none`,
  `SOURCES-APPENDONLY violations=1`, exit 1 (`build/R42QualityDraft/receipt-{green,red}.txt`; the tool is a draft
  at `build/R42QualityDraft/sources_appendonly.py`, sha256 `f1b84d8a…`, and must land as
  `plans/sources_appendonly.py` for this line to run as written).
  Shown able to fail: the two fixtures above differ by one commit and one cell — the green one corrects by adding
  a row, the red one corrects by editing the row — and the tool separates them with exit 0 / exit 1; on the lane's
  own history the 15 `CELL` lines are the red half, the routed `S124` case among them.
  Limits: the check is act-level and red on history from round 30, so as a gate it binds from round 42 forward;
  this criterion names the 15 older cells and does **not** re-adjudicate them — at least one was a substantive
  tier change made in place on purpose (`9af639c9` "S086 is not peer-reviewed (society stamp) — relabel and tier
  to B", `tier` A→B plus a `scope` change), which rule 2 forbids and which the round-30 lesson's old→new logging
  does not cure, since the three mutable cells are the only ones logging covers; a row carrying a literal `|`
  inside a cell would parse as an arity mismatch and is reported (`arity=<n>`, exit 1) rather than silently
  misread — `arity=0` over 117 rows × 36 commits says no such row exists today; an in-place edit that was never
  committed is invisible (the same blind spot Q30's gate names); `status`, `recheck` and `used-by` changes are
  deliberately not flagged and their required old→new logging is not checked, because the log lives in the lesson
  and this tool reads `corpus/SOURCES.md` only; a commit that edits a cell and adds the superseding row in the same
  commit is still reported (rule 2 is act-level: the old row is never rewritten), and the column is printed as
  `repair_row=same-commit` so a reader can see the shape; a squash-merge that folds an edit and its revert into
  one tree hides both; and the check says nothing about whether the correcting row's new content is true — that is
  Q1/Q3/Q26's work — nor whether the id a `supersedes` cell names exists: two registry rows name themselves
  (`S094`, `S097`, both refused-duplicate records), which this tool reports as context and does not adjudicate.
  Lesson: routed item R4 and closure defect D2, `corpus/lessons/round-41-verifier-spotcheck.md:30-36` and `:116`;
  rule text `SOURCES-CONTRACT-v1.md:49-51` and `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`. Supersedes: none;
  it is the first executable leg of rule 2 and supersedes no criterion.

## Round42 criteria — corrections appended in round 43 (Q33, Q34)

`F42RevQuality` (`.ufo/waves/round-42/falsify/F42RevQuality.md`) routed six defects; all six re-held at `d33350f` and
all six are recorded here. The criteria stay as written; these are the corrections a reader needs and the fixes owed.
Line numbers are this file's.

- **C1 (D1) — the tools the Check lines name exist in no commit.** Q33 (`:718-719`) and Q34 (`:800-801`) say the drafts
  "to land as" `plans/carried_direction_diff.py` and "must land as" `plans/sources_appendonly.py`. Neither exists at
  `d33350f` and neither appears in any commit (`git log --oneline --all -- plans/carried_direction_diff.py
  plans/sources_appendonly.py` → empty). Both Check lines were dead text as landed. Owed: land the two drafts from
  `.ufo/waves/round-42/build/R42QualityDraft/` (`carried_vs_rederived.py` `47151f23…`, `sources_appendonly.py`
  `f1b84d8a…`) under those names, or rewrite each Check line to name the draft path — the fallback now resolves,
  because the draft directory is committed since `f9bbee6`.
- **C2 (D2) — the Check lines do not match the drafts' CLI.** Both drafts take the lane positionally
  (`build/R42QualityDraft/carried_vs_rederived.py:5` `LANE = sys.argv[1]`; `sources_appendonly.py:13` `LANE = sys.argv[1]
  if len(sys.argv) > 1 else "."` — the review said `:14`, one line late), so `--lane .` is consumed as the path `--lane`.
  Measured 2026-10-26 at `d33350f`:
  `carried_vs_rederived.py --lane .` → `FileNotFoundError: … '--lane/.ufo/waves/round-40/falsify/F40XMutAnchor.md'`,
  exit 1; `sources_appendonly.py --lane .` → `SETUP git log failed: fatal: cannot change to '--lane': No such file or
  directory`, exit 2. The form that runs is `python3 <tool> <lane>` (positional run: `CARRIED-DIRECTIONS total=14
  differ=2 ids=XO5,XO6`; `SOURCES-COMMITS scanned=37 rows_at_tip=121`, `SOURCES-APPENDONLY violations=15 arity=0`,
  exit 1). A byte-identical landing alone would not make either Check runnable.
- **C3 (D3) — Q33 (b) cites a predicate line its own instruction cannot print.** Development mode
  (`plans/round42_c1_verify.py:525` `dev = a.battery_dir is not None or a.only is not None`) prints `PREDICATE C1 n/a
  (non-default battery or mutant subset)` (`:657`), so the `PREDICATE C1 fail` at
  `claims/control-c1-direction-mislabel.txt:37` belongs to the default battery run (29 fixtures), not to (b)'s
  "development mode with the witness fixtures". Correction: (b) keeps its discriminating lines — XO5/XO6 `rc-silence
  `SURVIVED exhibits=0>1,rc-mirror`, `MUTANTS total=14 killed=12 survived=2 …`, `MUTANTS-BY-TOOL order=3/5`, `exit=1`
  (`:38`) — and names the default battery as the mode that additionally prints the predicate, or drops the `:37`
  citation.
- **C4 (D4) — Q34's pipe sentence is false where it matters, and its inference is invalid.** `:809-811` says a cell
  carrying a literal `|` "would parse as an arity mismatch and is reported … rather than silently misread — `arity=0`
  over 117 rows × 36 commits says no such row exists today". The tool skips every row it has not seen before
  (`build/R42QualityDraft/sources_appendonly.py:58-60` `if rid not in prev: continue`), so a row *born* with a pipe can
  never produce an `ARITY` line, and its later in-place edits are attributed to the cell the pipe shifted into —
  `F42RevQuality`'s `fx-pipe3` fixture reported `violations=0 arity=0`, exit 0. `arity=0` therefore cannot establish the
  conclusion. The conclusion is nevertheless true: `awk -F'|' '/^\| S[0-9]+/ && NF!=13' corpus/SOURCES.md | wc -l` → `0`
  over 121 rows at `d33350f`. Correction: keep the conclusion, cite that scan, and state the limit — arity is a length
  guard for ids already present, nothing else.
- **C5 (D5) — wrong pin.** `:767` cites `parse_registry(text, …)` at `plans/registry_check.py:20`; `:20` is
  `def safe_path(value):`, `parse_registry` is defined at `:25`, and the working-tree call is `:55`.
- **C6 (D6) — the last sentence of `:767` needs the creation-time scope.** "No lane tool reads it from committed history"
  is true at `d33350f` only because C1 left the instrument unlanded; landing `sources_appendonly.py` — C1's own fix —
  would falsify it with the criterion's instrument. Correction: "no lane tool read it from committed history at this
  criterion's creation", the scope the neighbouring measured sentences already carry.

## Round43 criterion — a conditional Gate refusal is resolved by a recorded flip check

- **Q35 — every Gate refusal whose reason states a flip condition is resolved, in the same lesson and
  on a line after the flip statement, by `Flip check (round N): <item> — fired|not fired — <evidence>`;
  a condition that fires at landing must not be representable as silence, because the lane's only
  record that a flip was examined at all is the sentence that says so.**
  The obligation is written 45 times across 18 lessons and was executed on none of them. Of the 55 files
  in `corpus/lessons/`, 20 carry a `## Gate` heading (`grep -l '^## Gate$' corpus/lessons/*.md` →
  `round-13-coverage.md`, `round-24.md` … `round-42.md`), 18 of those carry at least one refusal whose
  reason states a flip, and the checker below counts 45 such obligations with 45 unresolved
  (`FLIPS total=45 unresolved=45` summed over the 18; the per-lesson numbers are in
  `.ufo/waves/round-43/build/R43FlipCheck/sweep.txt`). No line in `corpus/` or `plans/` says
  `Flip check` (`grep -rn "Flip check" corpus plans` → no matches), so nothing in the lane has ever
  recorded that a flip fired or did not.
  The measured instance is round 42. Its Gate refuses `Dockerfile` conditionally —
  `corpus/lessons/round-42.md:44`, "if the entry keeps the `WORKDIR /app` sentence" (10 words) — and the
  landed entry kept the sentence and made it load-bearing
  (`corpus/lessons/round-42-verifier-spotcheck.md:92`), so "by the Gate's own flip the file should be a
  row"; no `S###` row was opened and no line records the flip at all
  (`corpus/lessons/round-42-verifier-spotcheck.md:37`, "D3 Gate flip condition fired and was not
  executed (Dockerfile)."). A second obligation on the same section, `README.md` (`:43`), is in the same
  state. The old instruments cannot see this class: `plans/gate_timing_check.py` checks that admits name
  returned second-seat reports, `plans/round_close.py` checks the round's order of operations, and
  `plans/state_check.py` re-derives frozen assertions — none reads a lesson's flip conditions, and the
  only `flip:` string anywhere in `plans/*.py` is a fixture literal a registry test writes
  (`plans/round33_c1_verify.py:215`, "REJECTED: duplicate id; flip: a future candidate uses a new id"),
  never a line read or checked.
  Check (executable, round-42 instance): `python3 plans/gate_flip_check.py --lesson
  corpus/lessons/round-42.md` prints one `FLIP line=<n> flip_line=<n> item=<item> … resolution=<detail>`
  line per conditional refusal, then `FLIPS total=<n> unresolved=<u>`; exit 1 iff `u>0`, exit 2 when the
  lesson is unreadable or carries no `## Gate` section. On the landed lesson it prints `FLIP line=43 … item=README.md
  … unresolved:no-line`, `FLIP line=44 … item=Dockerfile shapes=flip:,if-admit … unresolved:no-line`,
  `FLIPS total=2 unresolved=2`, exit 1. A scratch copy of the same file with the two resolution lines
  appended prints `FLIPS total=2 unresolved=0`, exit 0; the same copy carrying only the `Dockerfile`
  resolution prints `FLIPS total=2 unresolved=1`, exit 1. The tool landed as `plans/gate_flip_check.py` (drafted by `R43FlipCheck` at
  `.ufo/waves/round-43/build/R43FlipCheck/gate_flip_check.py`, sha256 `d849250d…bf1d`, 504 lines, stdlib only).
  Shown able to fail: `--selftest` builds 19 fixtures in a temporary directory and runs the checker on
  each as a subprocess — `SELFTEST ok=19/19` (10 red, 8 green, 1 setup). The reds are the shapes the
  criterion has to separate: a refusal with no resolution line; a `flips when` refusal with none; a
  resolution placed *before* its flip statement; a resolution naming another candidate; evidence `none`
  and evidence of one word; `(round 4)` under a `round-42` file name; a malformed `<state>`; a
  `- **Rejected:**` bullet with no resolution; and a companion flip bullet with no resolution. The two
  halves of the round-42 demonstration differ by exactly the appended lines and by nothing else
  (`FLIPS total=2 unresolved=2` exit 1 against `total=2 unresolved=0` exit 0), and the partial copy
  differs by one of the two lines and moves `unresolved` 2→1, so the check is per-obligation, not
  all-or-nothing. On the corpus the same run is red on all 18 lessons that carry obligations, the
  landed round-42 lesson among them.
  Limits: the verdict is a recorded *sentence*, never the executed consequence — a `fired` line whose
  evidence names the wrong landing passes, and a `not fired` line whose condition had in fact fired
  passes just as well; the class is 45 obligations wide at creation, so as a gate it binds from round 43
  forward and this criterion does not re-adjudicate the older 43; the section is found by a level-2
  `## Gate` heading, so a lesson with no such section is exit 2 (`SETUP`) and not a pass — 35 of the 55
  lesson files are in that state and two more (round-13-coverage, round-31) have a Gate section and zero
  obligations, which reads green but demonstrates nothing; a flip phrased imperatively rather than
  conditionally is not counted (`round-30.md:34`, "flip one entry at a time under CORPUS rule 4"), so
  round 30's obligation count is 3 of its 4 rejects; the item name is derived from the refusal's first
  id-shaped token, else its first code span, so a candidate named only in prose needs the resolution to
  repeat that prose; a companion bullet attaches to every refused candidate it names and to none it does
  not; `fired`/`not fired` is a two-word vocabulary, so a round that resolves a flip with a third state
  (`moot`, `superseded`) gets an unresolved line until it says one of the two and explains the other in
  its evidence; and the checker reads the working tree only, so a resolution line committed and later
  deleted is invisible and a resolution line that lives in another file (a seat report, `PROVINCE.md`)
  does not count — the criterion deliberately keeps the record beside the condition.
  Lesson: `corpus/lessons/round-43.md` mined mistake (round-42 D3, routed as closure R2 in
  `corpus/lessons/round-42-verifier-spotcheck.md:125-128`: "a conditional reject's flip is re-checked at
  landing"); the class's first instance is `corpus/lessons/round-42.md:44` against
  `corpus/lessons/round-42-verifier-spotcheck.md:37-42` and `:92`. Supersedes: none; it is the first
  executable leg of the flip condition the Gate has been writing since round 25.

## Round44 criterion — a flip verdict is checked against the entry it concerns

- **Q36 — a `Flip check (round N): <item> — not fired — <evidence>` resolution counts only when the entry the refusal is
  about carries no unbacked `<item>:<line>` citation; Q35 reads that the sentence exists, never that it is true, and a
  present false sentence is the round-43 defect Q35 was written to close.** Q35 landed as `plans/gate_flip_check.py`
  (sha256 `d849250da6b3815dba421d5a…`) and reads one lesson file: it takes `## Gate`, keeps the refusals whose text states
  a flip, and accepts a later line whose state is `fired` or `not fired`, whose evidence is ≥2 non-placeholder words and
  whose round is not older than the file name (`:37-46`). It never opens an entry. On the round-43 lesson, whose
  `task.toml` resolution is false, it prints `FLIPS total=2 unresolved=0`, exit 0
  (`.ufo/waves/round-44/wave/R44QualityQ/q35-round43.txt`). The verdict is false by the entry's own citations:
  `awk '/^## Located quotes/{s=1;next} /^## /&&s{s=0} !s' corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md`
  keeps 7 lines citing `task.toml:<line>`, none carrying an `S1xx` co-citation, among them the Mechanism row
  `| slow-oracle-45s | task.toml:22 |` and `:122` "the only ceiling is `task.toml:22`'s 1800 s verifier timeout"; the same
  scan gives `solve.sh` 3 unbacked, `setup.py` 1, `feal.h` 0, `SHA256SUMS` 0. The disagreement is recorded at
  `corpus/lessons/round-43-verifier-spotcheck.md:124` — "**disagree** (on the flip verdict; I agree with refusing them as
  rows)" — and routed as closure R1 at `:156`.
  Check (executable, round-44 instance): take each `not fired` resolution, the items it names and the entry the lesson's
  Gate concerns; strip the entry's `## Located quotes` section; red the line when any `<item>:<line>` hit carries no `S1xx`.
  The round-44 demonstration driver is `.ufo/waves/round-44/wave/R44QualityQ/flip_verdict_demo.py` (receipt beside it);
  `python3 …/flip_verdict_demo.py <clone>` prints `INSTANCE lesson=corpus/lessons/round-43.md:46 item=task\.toml
  recorded=not fired body_hits=7 unbacked=7 verdict_truth=fired RED` and `INSTANCE lesson=corpus/lessons/round-42.md:215
  item=README\.md recorded=not fired body_hits=0 unbacked=0 verdict_truth=not fired ok`. The same leg, drafted at
  `.ufo/waves/round-44/wave/R44FlipVerdict/gate_flip_check.py` (digest `31db1154…`, unlanded at this draft), prints
  `FLIP-CITE … verdict=RED` with `not_fired=2 red=1` and exit 1 on round 43, exit 0 on round 42. The leg lands in
  `plans/gate_flip_check.py` — a file that exists at this draft — as a `FLIP-CITE` line; a Check line that names only an
  unlanded wave path repeats the round-42 closure C1 defect.
  Shown able to fail: the red and the green above differ by the entry's bytes alone. The round-42 `README.md` verdict is
  true (0 body citations) and stays green, so the leg is per item, not a blanket `not fired` → red; the round-43
  `task.toml` line is red on 7 hits, and per named item the same rule reddens `setup.py` (1) and `solve.sh` (3) while
  `feal.h` and `SHA256SUMS` stay clear.
  Limits: the rule reads citations, not meaning — an entry that rests on a refused file without writing `<file>:<line>`
  passes, and a `fired` line's evidence is still never read (Q35's limit survives this leg); item names are bare file
  names, so a sibling task's entry is counted — the wave draft reports `item=task.toml … citation=
  tb2-circuit-fibsqrt-grader.md:332`, a different task's `task.toml`, so one line reddens for two right reasons and one
  wrong one; an inactive leg reads green — the same draft prints `FLIP-CITE entries=- missing=instruction.md,README.md,
  R42PkgRows.md not_fired=1 red=0` on the round-42 lesson because that lesson's Gate names no resolvable entry, and an
  entry never examined must be exit 2, not exit 0; a resolution naming a package rather than a file (`round-43.md:47`
  `merge/kengaku/`) has no citation to read and prints `files=- verdict=clear`, which is not a pass either; the
  `## Located quotes` exclusion is the current entry shape's convention, so a `<file>:<line>` quoted in another section
  counts as prose; and no leg says whether the refused item deserved a row — the S135–S137 admit path stays a judgement.
  Lesson: `corpus/lessons/round-43-verifier-spotcheck.md:124` (the disagreement) and `:156` (closure R1, the fix this
  criterion states); the first instance is `corpus/lessons/round-43.md:46`. Supersedes: none; it adds a truth leg to Q35
  and leaves Q35's existence rule, its exit 2 and its malformed-line handling unchanged.

## Round44 criterion — a do-nothing control runs the lane's standing batteries too

- **Q37 — the do-nothing control of a calibration claim is two runs over the same frozen mutant list — no battery, and the
  lane's standing batteries copied in as the battery — and every mutant the second run kills leaves the frozen list before
  the freeze, because "no battery kills it" is new work only when the batteries already in the lane do not.** Q31's
  control proves a predicate is not vacuous with respect to its own list (`claims/control-c1-nothing.txt`:9-14 `BATTERY
  fixtures=0`, `MUTANTS total=5 killed=0 survived=5`, `PREDICATE C1 fail`); it cannot see that a mutant was already
  demonstrated by a battery that landed after the table was written. Round 44's pre-freeze draft is the measured instance:
  `R43PlanNext` priced six mutants with the cell "**6/6 killed attributed** by scratch fixtures (B.3); 0 killed by
  battery42 (B.2)" (`.ufo/waves/round-43/build/R43PlanNext.md:184`), true while battery42 was the whole lane; battery43
  landed in round 43 (`77ea425`, 19:24:42) and its `a_alt-slug-deepest` (`plans/battery43/a_alt.py:411`) kills U3. The
  standing-battery run over all six prints `MUTANT U3 anchor rc-mirror killed by=a_alt-slug-deepest attributed=L354
  value=differs hits=16` (`claims/control-c1-standing-batteries-six-mutant-draft.txt:88`), `BATTERY fixtures=71 …` (`:94`),
  `MUTANTS total=6 killed=1 survived=5 …` (`:95`), `PREDICATE C1 fail`; the frozen five print `total=5 killed=0
  survived=5` (`claims/control-c1-standing-batteries.txt:92-93`). U3 was dropped before the freeze
  (`plans/round-44-claims.md:33`, "U3 was priced too and **dropped before freeze**") and the counter records why
  (`plans/round44_c1_verify.py:6`: "U3 is killed there by battery43 `a_alt-slug-deepest`, so it is already demonstrated and
  left out").
  Check (executable, round-44 instance): copy `plans/battery42/*.py` and `plans/battery43/*.py` into one directory under
  distinct file names and run the frozen counter twice on a clean clone — `python3 plans/round44_c1_verify.py --lane
  <clone> --battery-dir <dir> --work <w>` must print `BATTERY fixtures=71 wrong=0 tampered=0 sidechannel=0`, `MUTANTS
  total=5 killed=0 survived=5 invalid=0 null_detected=0 unattributed=0`, `PREDICATE C1 n/a (non-default battery or mutant
  subset)`; without `--battery-dir` the same counter must print `BATTERY fixtures=0`, the same `MUTANTS total=5 killed=0
  survived=5 …`, `PREDICATE C1 fail`. Receipts for both: `.ufo/waves/round-44/wave/R44QualityQ/standing-battery.txt` and
  `…/no-battery.txt`. Both are freeze controls run before the freeze; a claims file that does not name each removed mutant
  with its standing killer has not run the second.
  Shown able to fail: the six-mutant list over the same 71 fixtures prints `killed=1`, so the control reddens exactly the
  row a round would otherwise book as new work, and the red half is reconstructible from committed material — U3's tuple is
  `.ufo/waves/round-43/build/R43PlanNext/u_mutants_table.txt:2-6`, the frozen literals `TOTAL = 5` / `FLOORS = {"anchor":
  4, "order": 1}` are `plans/round44_c1_verify.py:147-148`.
  Limits: the standing-battery run is development mode and prints `PREDICATE C1 n/a`, so it is never landing evidence; the
  copied modules keep their fixture ids, so a standing id reused by a `battery44` module is refused as `SETUP duplicate
  fixture id` (`plans/round44_c1_verify.py:809`, exit 2) and one side must rename; the control sees only batteries present
  in the tree at the freeze; it forbids counting one kill twice, not a second kill of the same mutant for a different
  reason; a battery module the counter's contract cannot express is outside the run; and the six-mutant half is the L1's
  own pre-freeze receipt — a non-author reconstructs it from `u_mutants_table.txt` plus the frozen counter, not by
  re-running a counter draft that was never committed.
  Lesson: the U3 mis-price (`R43PlanNext.md:184` against `claims/control-c1-standing-batteries-six-mutant-draft.txt:88`) and
  the lane's pre-freeze correction (`plans/round-44-claims.md:33`; `plans/round44_c1_verify.py:6-7`). Supersedes: none; it
  extends Q31 — which asks whether the predicate can be satisfied without the work — by the question Q31 cannot ask:
  whether the work was already done by the lane.

## Round44 criterion — a content leg's key comes from executing the pinned source

- **Q38 — a content leg's verdict key is produced by executing the pinned source over generated end states and is stored
  nowhere in the counter; a key read off the instrument's own map, or off the source's prose, is a copyable answer and it
  disagrees with the source on exactly the states that separate the readings.** V10 (round 43) keeps a readable DECISIVE
  map in the counter, so a filler satisfies it (`R43CritClaims` §1; closure R5 at
  `corpus/lessons/round-43-verifier-spotcheck.md:169`). V11 is the first executed leg: `plans/round44_c2_verify.py:34-43`
  builds 48 end states from the 100 pinned constants, runs the captured grader's `test_attack` on each inside a sandbox and
  the entry's `predict` on each in a second, requires 0 disagreements and ≥8 passes and ≥8 fails, and states at `:40-42`
  "The verdicts are never stored here: they exist only by executing the grader, so a filler cannot copy them from the
  counter" and at `:379` "STATES is a generator, not an answer key: no verdict is stored in this file".
  Measured (`claims/control-c2-predictor.txt:3-7`, re-run by this seat into
  `.ufo/waves/round-44/wave/R44QualityQ/c2-predictor.txt` at 20:39:40): always-true `disagree=24`; whitespace-token-set
  `disagree=12` at `concat#4,zero-pad#5,comma#11,prefixed-digit#15,…`; exact-lines `disagree=18`; substring `disagree=0`;
  `CONTROL-C2-PREDICTOR red-as-required`, every line `states=48 grader_pass=24 grader_fail=24`. The reds are the readings a
  careful reader writes from the test file's text — one constant per line, the file's tokens are the constants — and they
  are wrong only where the executed `assert c in data` over the whole file accepts concatenated, zero-padded or
  decoy-bearing content.
  Check (executable, round-44 instance): `python3 plans/round44_c2_verify.py --lane .` prints `checks=11 defects=0`, then
  `PREDICATE C2 pass`, exit 0, V11 among the 11; `python3 .ufo/waves/round-44/claims/c2_predictor_control.py <work>`
  prints the four `CONTROL` lines and `CONTROL-C2-PREDICTOR red-as-required`, exit 0.
  Shown able to fail: three of the four control keys are red with named states and counts, and the non-vacuity leg (24
  passes and 24 fails of the 48) removes the always-pass escape, so the green substring key is not the empty key.
  Limits: the states come from `random.Random(44)` cycling 16 state kinds, so a predictor can be tuned to the generator —
  the docstring's answer is that tuning requires running the grader, which is the reading asked for; only
  `/app/plaintexts.txt` varies between states, so a decision that also read another input is under-modelled; the captured
  grader runs under the host `python3`, not the image's 3.13 (the claims' own limit); a correct predictor is a predictor of
  the graded decision, never of whether that decision is worth grading; and "no key stored" is a property of the frozen
  bytes at the pinned digest — nothing prevents a counter that executes the source once at freeze and embeds booleans
  behind a generator, so the pin makes that a reviewable edit, not an invisible one.
  Lesson: `.ufo/waves/round-43/build/R43CritClaims.md` §1 (V10's readable key) and closure R5
  (`corpus/lessons/round-43-verifier-spotcheck.md:169`); the lane's own statement of the residual is `plans/round-44-claims.md`
  §C2 V11. Supersedes: none; it closes V10's readable-key limit without relaxing V10.

## Round45 criterion — a fence counter's freeze controls include a fence that keys on the counter's own names

- **Q39 — a counter that grades a decision procedure (a fence, a classifier, a gate) over fixtures it builds itself
  hides from that procedure every name the counter chose — fixture directory, build root, module copy — and its freeze
  controls include one procedure that inspects nothing and keys its verdict on those names; that keyed control must
  print the frozen predicate's fail line before the freeze, or the predicate is reachable without the work.** Round 45's
  C1 froze four controls (`fences/admit_all.py`, `refuse_all.py`, `static_only.py`, `r44_tail.py`) — every one inspects
  the fixture or nothing at all, none reads the path. `plans/round45_c1_verify.py:135-141` names each fixture dir
  `fx/<battery-or-refusals45>-<stem>/fNNN`, so a one-line fence (`.ufo/waves/round-45/claims/fences/keyed_name.py`:
  refuse iff `"/refusals45-" in str(d)`) prints `REFUSALS total=10 clean=10`, `HONEST fixtures=104 admitted=104`,
  `CALIBRATION advertised=10 contradicted=0`, `PREDICATE C1 pass`, exit 0
  (`.ufo/waves/round-45/claims/control-c1-fence-keyed_name.txt`, frozen counter unchanged, clone of `fbad1c56`). The
  wave critic found the class first (`.ufo/waves/round-45/w1/R45CriticPredicate.md` B2); nobody ran it as a control
  before the claim landed.
  Check (executable, round-45 instance): `.ufo/waves/round-45/claims/dev_blind_c1_verify.py` (the frozen counter with
  the three names replaced by sha256-derived opaque names; `dev-blind-c1.diff`, 3 lines) run with `keyed_name.py` as
  the fence prints `REFUSALS total=10 clean=0 leaked=10`, `contradicted=10`, fail, exit 1
  (`dev-blind-c1-keyed.txt`), and with the landed `plans/fixture_fence.py` prints `clean=10`, `HONEST … admitted=104`,
  `contradicted=0`, exit 0 (`dev-blind-c1-landed.txt`).
  Shown able to fail: the same keyed fence passes the frozen counter and fails the blinded one, so the criterion
  separates a counter that leaks its names from one that does not, on committed bytes.
  Limits: blinding names is necessary, not sufficient — argv tokens that embed `d` (f4/f5 `--lane`), the count of
  fixtures per module and build order remain side channels, and R45CriticPredicate's B1 (the fence erases its own
  strace log), B3 (opens outside `fx|btmp` uncounted), B4 (stdout verdict spoof), B5 (stat/readlink channels) are
  separate counter defects this criterion does not close; the dev-blind counter is development evidence, never a
  frozen predicate.
  Lesson: `corpus/lessons/round-45.md` §Mistakes (attempt 3, keyed-control row). Supersedes: none; it extends Q31/Q37 —
  which ask whether the predicate is reachable without the work, or by work already in the lane — to the counter's
  own naming as an answer channel.

## Round46 criterion — every frozen requirement tag has a frozen violating case before its counter is pinned

- **Q40 — before a counter that derives requirement labels from a receipt is pinned, every `TAG` its frozen dry table
  declares is carried by at least one frozen case's `violates=` set; and a control run before the first recorded probe
  run never executes a leg that re-runs the probe.** Round 46's C3 pinned `plans/round46_c3_verify.py` against
  `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`, whose seven tags include `both-print` and `toolchain`
  that no frozen case violates; V7 requires a violating case per tag, so C3 failed V7 whatever the package held
  (`.ufo/waves/round-46/integrate/c3-landing.txt`). The same round's `control-c3-echo` ran V2, whose gate leg P10 runs
  the probe, before the receipt existed; `plans/order_check.py` read the committed control receipt as
  `probe-executed-before-receipt` and V8 failed.
  Check (executable): `python3 -c "import re,sys; t=open(sys.argv[1]).read(); tags=re.findall(r'^TAG (\S+)',t,re.M);
  v={x for m in re.findall(r' violates=(\S*)',t) for x in m.split(',') if x}; print(' '.join(x for x in tags if x not in
  v) or '-')" <dry table>` must print `-`. Shown able to fail: on the round-46 table it prints `both-print toolchain`; on
  `corpus/evidence/round45/password-recovery-dry-cases-freeze.txt` it prints `-`. Second leg: `python3 plans/order_check.py
  --lane . --claims plans/round-N-claims.md --receipt <receipt>` must print `ORDER RESULT PASS` on the tip; on round 46 it
  prints `ORDER HIT .ufo/waves/round-46/claims/control-c3-echo.txt@4fdeebaa546c:15 kind=gate-p10` and `ORDER RESULT FAIL`.
  Limits: the tag check reads the dry table only (a tag the probe could violate but no case does is caught; a case that
  lists a tag it does not in fact violate is not); the order leg sees only committed receipts.
  Lesson: `corpus/lessons/round-46.md` §Mistakes (frozen-tag and stage-2-control rows). Supersedes: none; it extends
  Q24 (a counter proved by its junk) with a positive precondition and Q30 (order) to the L1's own controls.
