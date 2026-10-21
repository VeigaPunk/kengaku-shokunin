# Round 25 — interval-calibrated attribution verdicts; current-state assertions re-derived

Round 25 (hyaku block 25–34), L1 KengakuR25, base `6180e4f`; pre-registration `plans/round-25-claims.md`
(landed `3f371d2`, Amendment 1 `710409f`, both before any instrument output). Wave reports:
`.ufo/waves/round-25/build/*.md` (92 seats) and `.ufo/waves/round-25/falsify/*.md`.

## Mistakes

Classes from the fleet vocabulary (`CORPUS.md` §Rules added from the kaika campaign). A fix counts only once
shown able to fail; the red run is named in each row.

| id | class | mistake · evidence pointer | captured-by | fix (red run) |
|---|---|---|---|---|
| M23 | landing | round 24 wrote three L0 questions only in its report (`.ufo/reports/round-24/kengaku.md:221,224,226`); none reached `.ufo/l0-questions.md` (`L0FilingScout.md`: 0/3, `git log -S` 0 commits) | prompt §5 L0 rule, not a lane check | QUALITY R11 + `plans/l0_filed_check.sh`; red: exit 1 on the round-24 report (`UNFILED` ×3), green on `plans/fixtures/r25/l0_filed_check/queue-all-filed.md`; the questions are re-filed under round 25 |
| M24 | survivor | r22 `TARGET hyper 10/10 -> PASS` (`attrib-r22-opencode-trials.log:236`, `attrib-r22-legs.log:344`) and "hyper validated" (`SCORECARD.md:541`) rested on a point fraction with min-n 10; the exact CP95 lower bound is 0.691503 | none (no SKILL/QUALITY rule asked for an interval — `SkillRuleScout.md`) | QUALITY Q11 + `plans/attrib_calibration.py`; red: the r22 line re-verdicts INDETERMINATE (`need_n=17`), and `--selftest` R1/R1b/R4 exit 1 on flipped cells |
| M25 | number-drift | the `sources-registry` capability cell (`SCORECARD.md:557`) kept "rows 25 / C=1 / rejected=2" after S026 landed (`e21f9ea`); the orchestrator closure already said 26 rows | round-24 census was presence-based (kaika W3 F9) | QUALITY R12 + `plans/state_check.py` P2a; red: base run `mismatch=11` incl. this row (`corpus/evidence/round25-calibration/state-check-before-6180e4f.txt`), closed by SCORECARD R25-E1 → `SUPERSEDED` |
| M26 | stale-premise | `SHONEN.md` carried prose evidence lines through rounds 13–24 (D17; M18 named it in round 24 and left it); PROVINCE `## Surfaces` kept four absent first paths unmarked (`ProvinceScout.md`) | PROTOCOL.md:432 form and QUALITY R4 existed; nothing ran them | `state_check.py` P2c pointer-only + P2d ABSENT rule; red: base run flags 4 SHONEN boxes and 5 PROVINCE rows; regenerated SHONEN and dated ABSENT markers make them MATCH |
| M27 | scope | round 24's C1 created the `sources-registry` row that C2's `capability_rows` counted (`RevSeparabilityR24.md`; `plans/round-24-claims.md:51,64,73`) — one artifact credited to two claims | AXES.md:30-32 prose only | QUALITY R13; round 25 freezes C2's population at base `6180e4f` and scopes the registry census to S001–S026 — red: the round-24 claims file names `capability_rows` under both claims |
| M28 | reference-drift | the round-25 pre-registration's "0 interval estimates exist" (`plans/round-25-claims.md:59`) was false: `knowledge/attrib-r21.md:139,154,156` hold descriptive Wilson intervals; the frozen sweep excluded `corpus/knowledge` | CORPUS "a negative claim carries its sweep" — the sweep was there, too narrow | Amendment 1 item 1 narrows the claim (0 exact, 0 per-leg, 0 verdict-carrying); red: the widened sweep `grep -rnE 'Clopper\|Wilson\|confidence interval' corpus plans SKILL.md grader.py` hits attrib-r21.md |
| M29 | scope | three wave-1 seats (RevF6, RevF9, RevM19Critic) wrote their reports into the fleet root `.ufo/waves/round-25/build/` despite the absolute-path rule | prompt §6.3 misroot rule | moved byte-exact into the lane (`cmp` ok) and the fleet copies deleted; the falsify-wave context repeats the absolute trailer path |
| M30 | number-drift | the pre-registration printed the n=16 CP lower bound as 0.7940 (truncated); exact 0.794093 rounds to 0.7941 (`PowerTableExec.md`, `CpReferenceExec.md`) | none | `plans/fixtures/r25/power_table.tsv` and `cp_reference.tsv` carry exact values; verdict unchanged (n=17 → 0.804936) |

## Gate

Admission bar `corpus/QUALITY.md` Q1–Q10 (Q11 added this round from M24; applied to the entry below).

| candidate | decision | reason |
|---|---|---|
| `knowledge/attribution-interval-calibration.md` | **admit** | Q1 triad first; Q2 every load-bearing claim on tier-A rows S027–S030/S033/S034/S011 or own-work S036/S037; Q3 quotes ≤25 words with locations (`corpus/evidence/round25-sources/gate.md`); Q4 "What this does not establish" names clustering, journal GT, derived specificity, dedup undercount, unopened primaries and a falsifier; Q5 abstract-only and author/repository copies labelled in the rows; Q6 extends `attrib-r21.md` and `llm-judge-calibration.md`; Q7 index and coverage-map rows land in the same commit; Q8 two rejections below; Q10 numbers re-derived by a second parser (`plans/fixtures/r25/attrib_oracle.sh`) and by wave-2 seats |
| rule of three as the verdict rule | reject | one-sided approximation; would PASS 15/15 and 16/16 at 0.80 where two-sided CP is INDETERMINATE (`plans/fixtures/r25/power_table.tsv`); flip: an operator ruling that one-sided bounds suffice |
| prediction-powered inference (S035) as the share correction | reject (row kept `queued`) | scope is means/quantiles/regression, not classifier sensitivity/specificity (`SrcPredictionPowered.md`); flip: a PPI variant for misclassified multiclass labels |
| Clopper & Pearson 1934 as a row | reject (lead only) | not openable this round (publisher 403, JSTOR challenge, Unpaywall closed — `SrcClopperPearson.md`); flip: an opened copy with a located quote |
| Reiczigel, Földi & Ózsvári 2010 as a row | reject (not a row) | the opening seat had not returned by integration; flip: an opened copy |
| pooled r22 40/40 as a verdict | reject | the frozen dedup rule counts the identical table once; the pooled line is printed as sensitivity only (Amendment 1 item 4) |

New SOURCES rows S027–S037 (receipts `corpus/evidence/round25-sources/gate.md`). Status/recheck/used-by
changes logged old→new: **S011** used-by `corpus/knowledge/llm-judge-calibration.md` →
`corpus/knowledge/llm-judge-calibration.md, corpus/knowledge/attribution-interval-calibration.md`. S036
supersedes S025 (tier A → B for a recorded live-run log; kaika W3 F7); S025's own cells are unchanged.

Spot-check: the outside non-author check of one admit and one reject belongs to the orchestrator's closure
(QUALITY R6); lane-dispatched wave seats are not that check.

## Kaika W3 findings — round-25 disposition

| finding | status at `3f371d2` | round-25 action |
|---|---|---|
| F1 recheck cells | fixed `e21f9ea` (RevF1) | none |
| F2 quote locations | fixed `e21f9ea` (RevF2) | none |
| F3 Ref-5 range | partial (RevF3: 48.58% column unverified) | routed to a falsify-wave re-open of S009 Table 3 |
| F4 S023 reason | fixed `e21f9ea`; search-log residual | appended SOURCES search-log correction |
| F5 overstated self-verdict | partial (RevF5) | `round-24.md` §Errata supersedes the Gate pass lines |
| F6 `:567` pointer | open (RevF6) | `round-24.md` §Errata → `:569` |
| F7 S025 tier | open (RevF7) | S036 supersedes S025 at tier B |
| F8 capability rows | partial (RevF8) | SCORECARD R25-E1 for the stale counts |
| F9 presence census | open (RevF9) | `plans/state_check.py` (C2) |
| F10 dynamic-page hashes | open (RevF10) | caveat appended to `round24-sources/gate.md` |
| F11 Cramér's V qualifier | open (RevF11) | correction appended to `llm-judge-calibration.md` |
| F12 Extends target | open (RevF12) | correction appended to `paired-eval-uncertainty-reporting.md` |
| F13 census TZ | fixed in the fleet tool (RevF13, RevengeCensusTZ) | none |
| F14 placeholder | benign (RevF14) | none |
