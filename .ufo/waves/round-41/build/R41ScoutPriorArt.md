# R41ScoutPriorArt — prior art for the five C2 findings (kengaku r41 wave 1)

Seat: scout, leaf, read-only. All access times are host-local (-03), 2026-10-26, from `date +%FT%T%z` taken in the same command batches. Grader pinned by the lane: terminal-bench-2 @ `2fd12b88…`, `tests/test_outputs.py` sha256 `1422b345…`.

## 0. Ground facts that bound everything below

- **TB2.1 main carries the pinned grader unchanged.** `gh api repos/harbor-framework/terminal-bench-2-1/contents/tasks/constraints-scheduling/tests/test_outputs.py` (main = `7131e4375048a0e408a8fb404b5f499d726b695b`, the PR's own base) hashes `1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1`. The same hash comes from TB2 @ `2fd12b88` (15:40:53) and from the lane capture `corpus/evidence/round41/tb2-constraints-scheduling/test_outputs.py`. Line 14 / 93: `Path(p).read_text()` for both the output and the integrity compare. So a finding that is not in PR #245 is also not fixed upstream.
- **PR #245 (S124) state:** `gh api repos/harbor-framework/terminal-bench-2-1/pulls/245` (15:37:06): `state=closed merged=false closed_at=2026-10-08T19:02:36Z user=camirian comments=0 review_comments=0 changed_files=4`. Timeline: `committed`, `closed` by `camirian` (15:39:58). Opened 2026-10-05T02:41:13Z. The body text calls itself a "local draft only; do not submit without owner authorization", yet the PR is public and open to anyone for reading. It was never reviewed or merged. It is public text, not an upstream fix.
- Files changed by #245: `tasks/constraints-scheduling/{SPECIFICATION.md, tests/test.sh, tests/test_event_binding_adversarial.py (55 cases), tests/test_outputs.py}`. Diff saved only in scratch (deleted); fetched with `gh api … -H "Accept: application/vnd.github.v3.diff"` at 15:38:15.

## Rubric for the count

- **published** = a public source states, in prose or in a test it ships, the observed grader behaviour for that finding.
- **partial/implicit** = the public source only encodes the repaired behaviour (a code change or an expect-accept test) without saying the original grader misbehaves. Not counted in `p`.
- **not found** = queries listed, nothing matches.
- `p` counts only **published**.

## 1. First-DTSTART decoy — PUBLISHED

- URL: https://github.com/harbor-framework/terminal-bench-2-1/pull/245 (section "Current upstream state checked 2026-10-04"; also "Proposed PR description"). Accessed 2026-10-26 between 15:36:00 and 15:37:00 (read tool, before the 15:37:00 date stamp) and re-read via gh api at 15:37:06.
- Quote: "the constraint and earliest-slot tests parse the first DTSTART in the entire output calendar." (PR body, "Current upstream state").
- The body's reproduction is the same class as the lane's `decoy-first-vevent`: invalid target (Bob's 10:00 rule) after a decoy at 11:00-12:00 passes all 3 tests, "With the requested meeting first, the verifier fails." The patch case `conflict-hidden-behind-decoy` encodes it.
- Difference: #245's decoy has no attendees; the lane's probe has the attendee meeting at Fri 15:00 and `decoy-second-vevent` (attendee meeting first, decoy second, PFF). Same finding, so no novelty.

## 2. Earliest test passes an invalid earlier slot (`bob-start-0900-wed`, `wed-1059-overlaps-alice`, tests=PFP) — NOT FOUND

- #245 explicitly leaves it: SPECIFICATION.md in the diff says "Do not change input integrity, conflict, availability, or earliest-time rules while repairing event binding." No test case probes an invalid slot earlier than 11:00 against test 3 (the nearest, `bob-start-hidden`, expects False and is aimed at the decoy path).
- Adjacent, not equal: the JonathanGabor LLM audit says the minute scan makes passing "nearly impossible" for a wrong solution (below). That is a contrary claim, not a finding.
- Queries, all 2026-10-26 15:37-15:41: `search/issues` on repo:harbor-framework/{terminal-bench-2, terminal-bench-2-1, terminal-bench, harbor} for `constraints-scheduling`, `earliest`, `DTSTART`, `DTEND`, `calendar ics`, `meeting_scheduled` (totals: TB2 = 0 for all; TB2.1 = #245 plus leaderboard PRs #206/#208 and unrelated #100 dna-insert; terminal-bench = unrelated task proposals; harbor = unrelated). Global `search/issues` for `constraints-scheduling DTSTART|grader|verifier bug|test_outputs|ics flaw`: only #245 is on topic. `search/code` for `constraints-scheduling DTSTART`: 49 hits, all trajectories, results, or task copies (none an analysis). Web search ×3.

## 3. Input-integrity check blind to CRLF rewrites (`input-crlf-rewrite`, PPP) — NOT FOUND

- #245 does not touch it: the diff changes only `_r()` (the output reader) to `open(newline="")`; the integrity block (`app_text = (Path("/app")/fname).read_text()`, `assert app_text == repo_path.read_text()`) appears only as unchanged context. No #245 case modifies an input calendar (the fixture copies pristine inputs with `write_bytes`).
- Adjacent: #245 makes the *output* parse CRLF (case `crlf`, expect True) — that is finding 4's CRLF half, not 3.
- Queries as in section 2 plus `CRLF`, `line ending`, `newline`, `read_text`: TB2.1 `CRLF` hits #241 (an unrelated ARS verifier PR, open) and #245; others 0.
- Caution: one web-search answer (15:40, tool `web_search`) described this exact weakness ("normalized to LF by `read_text()`") but cited only the tbench.ai homepage and a registry task page, and called it "not a correctness bug". It is generated prose with no checkable source; **not counted as prior art**. The lane's probe (`input-crlf-rewrite` observed PPP) is the only evidence.

## 4. RFC 5545-valid output failing the grader (folding, lowercase names, VALUE=DATE-TIME) — PARTIAL / implicit only

- #245 PR body, "Proposed PR description": "It accepts CRLF, folded lines, case-insensitive property names, attendee parameters, and explicit UTC value parameters." The shipped cases `folded-attendee`, `case-property-names`, `utc-value-parameter`, `crlf` expect accept; SPECIFICATION.md cites "RFC 5545 … sections 3.1, 3.2.20, and 3.4".
- It never says the unpatched grader rejects them; the lane's receipt (`folded-attendee-line` FPP, `lowercase-property-names` FPP, `dtstart-value-datetime` FFF, `crlf-line-endings` PPP) is the observation. The #245 text does fix the specification side (what ought to be accepted), so the lane should cite it as "fix designed, observation not stated".
- Not in zai-org/terminal-bench-2-verified either: its `constraints-scheduling/tests/test_outputs.py` (rev `b456ea6b…`, 209 lines) still has `DTSTART:(\d{8}T\d{6}Z)` on the whole file at lines 135/151 and `read_text()` at 90-93; its README (2026.08.18) fixes 6+5 tasks and `grep -i scheduling` of its README returns nothing.
- Queries: `RFC 5545`, `VALUE=DATE-TIME` on the four repos (TB2.1 only #245).

## 5. DTEND ignored by two tests (`duration-90min`, FPP: S only) — PARTIAL / implicit only

- The #245 diff replaces `e = s + timedelta(hours=1)` in `test_constraints_conflicts_business_hours` with `s, e = _meeting(c)` and `end = sched + timedelta(hours=1)` in the earliest/Carol-buffer test with the event's own DTEND. Body: "obtains DTSTART and DTEND from that event for every target-specific check."
- No sentence says tests 2-3 ignore DTEND, and no case reproduces `duration-90min` against test 2/3 (the case `short-hidden-behind-decoy` varies DTEND only under a decoy). The finding is a consequence of the same event-binding repair, not a published statement.
- Queries: `DTEND` on the four repos (TB2.1 only #245).

## 6. Public audits checked

- **JonathanGabor/terminal-bench-2-audit** (`audit_results/20260120_125158/audit.txt`, fetched via `gh api …/contents/…` 15:38:54, 196 257 bytes). Task section at line 625-: rating 4. Quote (task section, "Could an Incorrect Solution Pass?"): "Very unlikely." It lists hash verification and the minute scan as strengths and raises none of the five findings. Weaknesses named: the hard-coded morning assertion, Carol's unreachable buffer, Bob's informational preference. `human-notes.txt` (1 349 bytes) does not mention the task. Greps of the audit for `crlf|newline|universal|DTEND|first DTSTART|fold|RFC 5545|VALUE=DATE` find only the unrelated CWE-93 entry at lines 1201-1227. Contradicts finding 2 rather than anticipating it.
- **kimjune01/terminal-bench-audit**, **jopoku16/honestboard**: `search/code` for `constraints-scheduling` returned 0 hits in both (15:39:58).
- **prime-radiant-inc/terminal-bench-analysis**, **ahstn/harness-bench** (`results/constraints-scheduling.md`): run results and a partial-credit proposal, three gpt-5.4 harnesses all passing at Wed 11:00; no verifier-flaw content (the file's only grader remark is a weighted scoring recommendation).
- **harbor-framework/terminal-bench#2086** "Vectors and mitigations for reward hacking during verification": `grep -c constraints-scheduling` of the issue body = 0.
- **WildClawBench#43** ("calendar_scheduling grader treats ROLE=OPT-PARTICIPANT attendees as required hard constraints"): a different grader and a different defect.
- HF `harborframework/terminal-bench-2.0` discussions 1-5 (api, 15:40): none on this task.

## 7. Summary table

| # | finding | status | source |
|---|---|---|---|
| 1 | first-DTSTART decoy | published | TB2.1 PR #245 body (closed, unmerged) |
| 2 | earliest test passes invalid earlier slot | not found | — (#245 excludes earliest rules) |
| 3 | integrity check blind to CRLF | not found | — (one unsourced web answer rejected) |
| 4 | RFC-valid forms fail | partial/implicit | #245 `CASES`, SPECIFICATION.md (fix, not observation) |
| 5 | DTEND ignored by two tests | partial/implicit | #245 diff `s, e = _meeting(c)` (fix, not statement) |

`p` = 1 published, 2 partial, 2 not found. Unreachable or unsearched: private repos, Discord/X, the `harbor-framework/terminal-bench-3` family, and any source beyond the first page of each `gh api search`; search ran with ~2-3 s spacing against the secondary rate limit and no 403/429 appeared. Scratch `/fast/scratch/hyaku/kengaku-r41/R41ScoutPriorArt` removed at the end.

VERDICT: prior-art-published-1/5
