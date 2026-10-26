# F41CritPriorArt — prior art for the two C2 observations wave 1 left unpublished (kengaku r41, wave 2)

Seat: critic, leaf, read-only on the lane. Target: widen the prior-art search for the two C2 observations that
`R41ScoutPriorArt` recorded as not found, and price a *possible* round-42 novelty claim. Nothing is claimed this
round. Access window 2026-10-26 16:13:10 → 16:28:40 host-local (-03, last command), `date +%FT%T%z` in every
batch; `gh` authenticated as VeigaPunk, search quota 30/min, no 403/429 observed.

Report path: `.ufo/waves/round-41/falsify/F41CritPriorArt.md`. Query log and excerpts:
`.ufo/waves/round-41/falsify/F41CritPriorArt/`.

## 0. The two observations, grounded in the lane's own receipts

The objects of the search are these two, both produced by the frozen probe and both **not** novelty-claimed this round
(`plans/round-41-claims.md` C2 "Limits named now", entry corrections (7)).

- **(a) The earliest test passes an invalid submitted slot.** `bob-start-0900-wed` and `wed-1059-overlaps-alice` are
  `tests=PFP` in `corpus/evidence/round41/constraints-probe.txt:13` and `:23`; the receipt's own gloss for the first is
  "the earliest test passes because no valid slot precedes it" (10 words). The mechanism is the loop bound: the scan
  is `while t < sched:` (`corpus/evidence/round41/tb2-constraints-scheduling/test_outputs.py:159`) and never passes
  `sched` itself to `_hard_ok`.
- **(b) The input-integrity check is blind to newline rewrites.** `input-crlf-rewrite` is `tests=PPP` at
  `constraints-probe.txt:31` — "all three input calendars rewritten with CRLF line ends, the right slot booked"
  (13 words). Mechanism: `read_text()` on both sides of the compare (`test_outputs.py:90`, `:93`) and
  `hashlib.sha256(app_text.encode())` on the fallback (`:95`), i.e. decoded text, not bytes (`:90` read,
  `:93` compare, `:95` digest).

Rubric carried from wave 1 and applied strictly: **published** = a public source states, in prose or in a test it
ships, the observed grader behaviour for that finding; **partial/implicit** = a public source encodes the repaired
behaviour without saying the current grader misbehaves; **not found** = queries listed, no match.
A search-engine *answer synthesis* is **not** a source (see §4).

## 1. Status: both NOT FOUND

| # | observation | status | closest public artifact |
|---|---|---|---|
| a | earliest test passes an invalid earlier slot (`PFP`) | **not found** | JonathanGabor TB2 audit asserts the *opposite* (§2.2); PR #245 freezes earliest rules and records an invalid target alone failing (§2.3) |
| b | integrity blind to newline rewrites (decoded-text compare) | **not found** | PR #245 explicitly declines to change integrity rules (§3.2); Python docs publish the mechanism only (§3.3) |

No source was found that states either behaviour for this grader. `k = 2` unpublished under this search bound.

## 2. (a) Earliest test passes an invalid earlier slot — searches and the strongest counterexample

### 2.1 What was searched (all 2026-10-26, totals are `search/issues`/`search/code` `.total_count`)

- TB2.1 (`harbor-framework/terminal-bench-2-1`) issues+PRs: `earliest` → 2 (#100 dna-insert, #245), `slot` → 2 (#245,
  #142 leaderboard), `calendar` → 1 (#245), `constraints` → 6 (none other on-task), `"input calendar"` → 1 (#245),
  `"line endings"` → 0.
- TB2 (`…/terminal-bench-2`): `earliest`, `slot`, `calendar`, `newline` → **0 each**; `constraints` → 3 (#44, #53, #32;
  #53 is the 2.1 release issue, `grep -c constraints` on its body = 0).
- Org-wide `harbor-framework`: `earliest slot`, `grader false positive`, `verifier`, `constraints-scheduling`,
  `newline`, `CRLF`, `input integrity`, `reward hacking` — 8 queries; the only on-task hit across all sets is #245
  (other hits are TB-science task proposals, harness I/O issues and leaderboard submissions).
- Global: `"constraints-scheduling" earliest|verifier|integrity|CRLF` (4 queries), `"Found earlier valid slot"` (3
  unrelated repos), `"Team Planning Meeting" verifier` (#245 + unrelated), `"_hard_ok"` → 0.
- Code search: `"test_earliest_tiebreakers_and_carol_buffer"` and `"Found earlier valid slot"` return the lane plus
  `hamishivi/tmax` `verifier/ctrf.json` files — grader *output*, no prose; `constraints-scheduling earliest` /
  `… verifier` / `… integrity` `extension:md` return task copies, harness-bench, openbench PROVENANCE, OpenAgentsInc
  docs, AgentStepVerification reports, a "lettabench" skill — none states the behaviour (read: `hb.md`, `ob.md`,
  `oa1.md`, `whip.md`, `sk1.md`, `sk2.md`, `rev.md`, `bib.md`).
- PR #245: `comments` = 0, `review_comments` = 0, state `closed`, `merged=false`, 4 files. There is no thread in which
  the author or a reviewer could have stated the blind spot.
- TB2 `docs/REVIEWING.md` (9 716 B): no `earliest|integrity|newline|byte` guidance.

### 2.2 The strongest counterexample available: a public audit examined this exact test and concluded the reverse

`JonathanGabor/terminal-bench-2-audit`, `audit_results/20260120_125158/audit.txt` (3 687 lines; task section at 625),
fetched raw 2026-10-26:

- `:651` (structure of test 3): "Exhaustively checks every minute from Jan 15 9:00 AM to scheduled time to ensure no
  earlier valid slot exists" (19 words). The description is of the loop bound, and the auditor read it as sufficient.
- `:668` ("Could an Incorrect Solution Pass?"): "The minute-by-minute exhaustive search for earlier slots makes it
  nearly impossible for a solution to pass unless it correctly:" (20 words), followed by four bullets including
  "Finds the truly earliest valid slot".
- `:662-665` lists its weaknesses: the hardcoded morning assertion, Carol's unreachable buffer, Bob's informational
  preference. The earliest blind spot is not among them.
- It also names "Input integrity protection - hash verification prevents cheating by modifying inputs" (`:658`) as a
  strength — the inverse of (b).

Why this matters for pricing: the only public source that analyses test 3 line by line **states the contrary
inference** and credits the same code as rigorous. A round-42 novelty claim for (a) would therefore be the first
public *reading* claim against a published contrary reading — novelty in the weak sense (no one has published the
observation) but with an adversarial public baseline that a reviewer can cite against it.

### 2.3 The nearest public statement, and why it is not the finding

PR #245 body (`gh api repos/harbor-framework/terminal-bench-2-1/pulls/245 --jq .body`, 4 514 B):

- `:22` "With the invalid target alone, it fails." (7 words). The author's reproduction tests exactly the invalid-slot
  state — a 09:00 Team Planning Meeting as the only VEVENT — and records the whole-suite outcome `fail`.
- The receipt's `bob-start-0900-wed` is also `fail`; the difference is only the per-test split (`PFP`). PR #245 never
  reports a per-test split, so the observation is not published there.
- Diff `:34-35`: "Do not change input integrity, conflict, availability, or earliest-time rules while repairing event
  binding." (16 words) — the earliest rule is deliberately untouched by the one public patch to this grader.

The mechanism the PR describes (event binding) is a different, published defect. Wave 1 already priced it as published
(finding 3 of the entry).

### 2.4 Reading this as a critic: (a) cannot change a verdict

This is the tradeoff the novelty claim has to own, and it is why the observation should be priced as a *redundancy*,
not a hole:

- Tests 2 and 3 parse the **same** expression from the **same** file:
  `s = _dt(r"DTSTART:(\d{8}T\d{6}Z)", c)` (`test_outputs.py:135`) and `sched = _dt(…, c)` (`:151`), with
  `c = _r("/app/meeting_scheduled.ics")` in both. `s == sched` always.
- Test 2 asserts `_hard_ok(s, e)` (`:137`). Therefore any end state in which test 3's missing validity check could
  matter (invalid `sched`) already fails test 2. The blind spot cannot turn a fail into a pass.
- The receipt agrees: both witnesses are `PFP` and observed `fail` (`constraints-probe.txt:13`, `:23`).

So "the earliest test cannot reject an invalid submitted slot" is literally true and **observationally inert** for
grading. A claim worded as a reward-hack or a false-positive path would be overclaiming; the honest object is "a check
whose name promises more than its loop does, relying on a sibling test for the prerequisite".

## 3. (b) Integrity blind to newline rewrites — searches and the nearest public artifacts

### 3.1 What was searched

Same issue/code sweeps as §2.1 plus: TB2.1 `integrity` → #213, #154, #175 (other tasks); TB2.1 `"read-only"` → #241
("Fix whitespace-sensitive ARS verification…", other task, and the *inverse* direction — over-strict whitespace);
TB2 `integrity checker` → 46, none on this task; org `newline|CRLF|input integrity` → harness-level (#1240 "Windows:
CRLF line endings in test scripts break verifier execution", #3768, TB #2244 `.gitattributes`), all about *task scripts
on disk*, not grader input comparison; org code `"newline=None"` → 0, `"universal newlines"` → 0.
`org:harbor-framework "read_bytes" integrity` → several `terminal-bench-science` `tests/contract_integrity.py` files,
i.e. other tasks in the same org compare bytes — a convention, not a statement about this grader.

### 3.2 The one public artifact that touches the integrity rule declines to change it

PR #245 diff `:34-35` (quoted in §2.3) is the closest public sentence: it tells the patch author *not* to change
"input integrity … rules", and the integrity block appears in the diff only as unchanged context (`:292`). So the only
published patch to this task put the decoded-text comparison out of scope for its repair; no public source says it is
blind. (Wave 1 reached the same conclusion; I re-verified the body and diff greps.)

### 3.3 The mechanism is published; the instance is not

- `docs.python.org/3/library/functions.html`, `newline` parameter: "When reading input from the stream, if newline is
  None, universal newlines mode is enabled." (15 words), and "Lines in the input can end in '\n', '\r', or '\r\n', and
  these are translated into '\n'" (17 words). `Path.read_text()` opens in text mode with that default.
- Consequence for a claim: the *mechanism* is textbook and cannot be presented as a discovery. The only novel content
  is the instance (this task's two-branch check) and its stated requirement (`instruction.md:15-18`: "Treat the
  provided calendar files as read-only." / "Any modification will cause the tests to fail.").
- Like (a), (b) is inert under the frozen probe's own semantics: a newline rewrite changes no decoded character, so the
  hard-constraint and conflict tests read the same content, and any edit that *does* change decoded text is caught
  (`input-appended` `FPP`, `input-event-deleted-wed-1000` `FPP`, `constraints-probe.txt:21`, `:22`). Only
  line-ending representation is invisible, and it carries no semantic change.
  The unenforced requirement yields no scoring benefit — it is a requirement/assertion divergence, which the entry
  already says ("the entry's clearest divergence between a stated requirement and the assertion behind it").

## 4. Search-summary contamination: three of three answer syntheses fabricated the finding

Wave 1 rejected one web answer for this reason. This wave hit the same failure three times, and it is worth recording
because it is the trap that would corrupt a novelty claim:

1. Query `"earliest valid slot" constraints-scheduling verifier terminal-bench` returned a fluent analysis of the
   per-test split. Its cited sources are the tbench.ai homepage, a Harbor registry task page, a HuggingFace
   instruction.md, the TB2 audit, and a StackOverflow question about reading files. None contains the analysis.
2. Query `terminal-bench "Input modified" grader CRLF …` returned the exact decoded-text argument, citing `[2]` = a
   Turing job posting for an EE/CS pod lead and `[1]` = the tbench.ai homepage.
3. Query `"earliest" test "submitted" slot never validated …` returned "the loop stops before sched" with `[1]` = a
   county fairground PDF.

All three read as prior art and none survives a click. Rule applied here: only `gh api` output, raw repository files,
downloaded PDFs and rendered pages count. If a later seat prices novelty from a synthesis, it will "find" the lane's
own unpublished claim already published.

## 5. Venues newly checked this wave (beyond wave 1), with verdicts

| venue | what it is | result |
|---|---|---|
| Horizon Analytics, "Benchmarks are more broken than we could have imagined" (2026-09-21) | 20 datasets / 5 241 tasks scanned, 29 confirmed broken; 8 TB2.1 tasks named in the appendix | neither observation; constraints-scheduling absent. "The Terminal-Bench 2.1 sample had more incomplete tests, shortcuts, and grading failures." (14 words) |
| `few-sh/terminal-wrench-trajectories` + paper 2606.08960 | 1 968 tasks across 5 terminal-agent benchmarks, 323 hackable; dataset: 331 tasks, 6 289 hacker trajectories, 3 models; TB2 subset 14/89 (186 hacks) | constraints-scheduling not in the dataset (`grep -i scheduling` → `schedule-vacation`; `calendar` → 0) and not in the paper's exploit vignettes (appendix G lists 5) |
| Harbor-Index release (2026-07-07) | 82-task meta-benchmark, 3 TB2 tasks, audit-and-fix loop | no per-task defect list; the task is not discussed |
| Berkeley RDI "We Scored 100% on AI Benchmarks" (2026-04) | 13 benchmarks, 45 PoCs | Terminal-Bench example is `portfolio-optimization`; no calendar task |
| Tokenless EnvCheck + TB #2150 (`tokenless-ai/envcheck-findings`) | 24 TB4 write-ups | TB4/DeepSWE/BFCL only; `grep -c constraints` = 0 |
| Epoch TB4 review, Preference Model TB4 issues (242 findings) | TB4 audits | TB4 only; `grep -i constraints|calendar` on the Preference Model page = 0 |
| `shreyashgondane.com` TB2 oracle audit (2026-10-16) | 8/65 oracle failures | package rot and timeouts; not verifier semantics |
| arXiv 2609.26826 "fake-hardness" (TB3), 2608.22103 HVTB, 2601.11868 TB2 paper, 2610.16067 oracle failures, 2609.01354 verifier metamorphic | papers | no mention of this task's earliest or integrity rules; TB2 paper only describes the task |
| HF `harborframework/terminal-bench-2.0` discussions | 4 threads | none on this task |
| PR #245 thread | 0 comments, 0 reviews | nothing |

## 6. Unreachable (recorded, not worked around)

- **"Benchmarks as Software: A Case Study on Terminal-Bench"** (Buchanan, Linderman, Ré; ICML 2026 DL4C poster;
  OpenReview `AhXMZPnOPS`) — an audit of all 89 TB2 tasks that reports task-side defects in 28 of them (per the
  record's public abstract snippet; full text unreachable). Unreadable from here:
  `curl` (default and browser UA) → OpenReview challenge page; `api2.openreview.net/notes?id=AhXMZPnOPS` → `403
  ChallengeRequiredError`; Wayback → no snapshot; `r.jina.ai` → challenge page; real Chromium (`browser.open`) →
  "Verifying your browser", 248 bytes of text. I cannot solve a CAPTCHA, so the appendix was not inspected.
  Indirect bound measured here: TB2.1 `main`'s `tasks/constraints-scheduling/tests/test_outputs.py` hashes
  `1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1`, identical to the lane capture, so this task is
  **not** among that paper's 28 repaired tasks.
- TB3 task port (`RyanMarten/terminal-bench-3#15`, titled "Add constraints-scheduling task") — API returns 132 B
  (private). If TB3 contains a rewritten grader, its discussion could later publish one of these behaviours; it is not
  public today.
- Not reached: X/Discord/private repos, non-English blogs, page 2+ of each GitHub search, gated HF datasets.

## 7. Pricing for a round-42 novelty claim

- **Status: unpublished-2/2** under this search bound. Neither behaviour is stated by any public source found; the
  single public analysis of test 3 states the opposite.
- **What a claim may say:** that the TB2 `constraints-scheduling` earliest check never validates the submitted slot,
  documented by two `PFP` receipts and the loop bound; and that its input-integrity check compares decoded text, so a
  line-ending rewrite of all three pinned calendars passes, documented by `input-crlf-rewrite` `PPP` and `:90-95`.
- **What a claim must not say:** that either yields a false positive, a reward hack, or a scoring consequence. (a) is
  masked by test 2 on the same bytes; (b) cannot change any decoded character. Stated as exploits they are falsifiable
  from the lane's own receipts (`bob-start-0900-wed` = `fail`; `input-appended` = `fail`) and would be the first thing
  an adversarial reviewer breaks.
- **Priors the claim inherits and should cite:** the published contrary reading (JonathanGabor `:651`, `:668`), the
  published refusal to touch these rules (PR #245 diff `:34-35`), the published mechanism for (b) (Python docs), and
  the fact that two public audits of TB2/TB2.1 samples (Horizon, Terminal Wrench) did not list this task, and the
  DL4C repair set is byte-identical for it (indirect, §6). Novelty is "no one has published this reading", not "no one
  could have seen it" — the contrary reading is public and the requirement text sits in the same repository as the
  grader.
- **Cheapest strengthening if round 42 wants the claim:** make it a *check-vs-name* claim over a pair of checks with
  receipts in both directions (one state where test 3 is inert because test 2 fires, one where the integrity branch's
  decoded-text compare is exercised), and pair it with the requirement map row (`inputs-readonly` `partly`,
  `earliest` `partly`) rather than with a reward-hacking narrative.
- **Smallest safe corrections** (for the record; not claims, not applied): pass `sched` through `_hard_ok(sched,
  sched+1h)` and the overlap test before the scan; compare `read_bytes()` (the org's own `contract_integrity.py`
  pattern) instead of `read_text()`/decoded-text digests.

## 8. What this seat did not establish

- That no publication exists. It establishes that the listed queries, in the listed venues, found none, and that four
  named sources were either contrary, partial, or out of scope.
- Anything about prevalence, agent behaviour, or the DL4C appendix (CAPTCHA).
- Any edit to the lane: no lane file was written except this report and its subdirectory; the frozen claims and
  digests were read only. Search scratch `/fast/scratch/hyaku/kengaku-r41/F41CritPriorArt` removed after the excerpts
  were copied here; two transient HTML caches for docs.python.org (`/tmp/pyfunc.html`, `/tmp/pypath.html`) were
  removed; no other path outside this report dir holds anything from this seat.

VERDICT: unpublished-2/2
