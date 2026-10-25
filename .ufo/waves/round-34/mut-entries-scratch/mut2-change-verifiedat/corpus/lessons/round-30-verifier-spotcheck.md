author: hyaku closure (non-author integrator, @m_flash)
round: kengaku 30 (attempt 1, hyaku run 6)
date: 2026-10-25
scope: non-author verification of `.ufo/reports/round-30/kengaku.md` plus its three appended errata; no lane-authored file was edited

# Round 30 — non-author verifier spot-check

I did not author this round. Baseline `363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db`; lane tip
`2dcf06c56acb63cbaaba59e74908a721ad153709` (local = remote, `ahead=0`). Every number below is a
command I ran myself over committed bytes. No lane gate or selftest was executed (PROTOCOL
§Gate standard, Closure consequence — a sibling's gate is evidence-verified, never run by the
integrator); the counter and gate lines are verified as committed evidence and their *inputs* are
re-derived independently.

Graded against the filed bytes **plus** the three appended errata, per the dispatch. Where an
erratum supersedes a cell in the measurement table, the erratum is what I checked the bytes against
and the superseded cell is named.

## 1. Step-1 conformance

| item | result |
|---|---|
| report committed in the fleet repo by the lane identity | **pass** — `git log --format='%an %H %s' -- .ufo/reports/round-30/kengaku.md` → 4 commits, author `kengaku-shokunin` on all: `b5cd9d69` (04:49:22), `068c7c41` (04:51:34), `3d38d633` (04:53:44), `c5807fe7` (04:56:55) |
| `SHONEN` heading, one line per box | **pass** — `grep -cE '^- \[[ x~]\]' SHONEN.md` → 4 boxes; the report's §SHONEN has 4 lines, each `[~]` with a resolvable pointer, none `[x]` |
| every cited lane commit exists and is an ancestor of the branch | **pass** — 12/12: `623c1fc9`, `706ed3f2`, `501d0707`, `6f6d6c98`, `d0253c52`, `5cd92295`, `baa53e70`, `bdcd7bed`, `a6a9b57a`, `caf1e2b4`, `9af639c9`, `2dcf06c5` → `git cat-file -t` = commit and `git merge-base --is-ancestor <h> master` OK for each |
| pushed, no uncommitted round work | **partial** — `jj-lane.sh state …` → `branch=master local=remote=2dcf06c… ahead=0 behind=0 head=detached`; but `git status --porcelain` shows **5 modified wave seat reports** (`.ufo/waves/round-30/{build/R30DraftGate.md,build/R30RevLesson.md,falsify/R30FxCoverageAxis.md,falsify/R30FxEntryCompleteSet.md,falsify/R30FxEntryQ4Q6.md}`), and a writer was still appending to them during this pass (mtimes 04:59:28 → 05:02:48, `date` at check 05:03:08). Uncommitted round work at closure → routed, see §5 item 6 |
| prompt carries the template contract | **pass** — `.ufo/prompts/kengaku-round-30.md` carries `## 1. MISSION / AXES binding` … `## 5. Commit, push scope, L0 side channel` (`:131`) plus `## 6. Campaign addendum — hyaku`; the five child-lane items are present verbatim: report path/filename (§4), commit-before-report ordering (`:328` "The report lands last and cites the pushed lane hash"), the `SHONEN` heading requirement (§4), the hash-citation rule (§4 "Cite ONLY the helper's final `landed <hash>` line"), write scope (§3) |
| L2 route map quoted in the prompt matches the current table | **pass** — prompt §6 says every role routes `@m_flash`; `~/.omp/agent/config.yml` `agentModelOverrides` maps all 18 roles (`task`, `main`, `executor`, `planner`, `labrat`, `mutation-tester`, `sentinel`, `simplifier`, `revenger`, `scout`, `sonic`, `scribe`, `distiller`, `seance`, `critic`, `reviewer`, `connector`, `security-reviewer`) to `@m_flash` |
| marker test | **not a marker** — real committed work, evidence pointers, all required sections |

**Report defects (status-neutral, named in the closure notes).**

- **Filed before its final lane commit.** The last report commit is `c5807fe7` at 04:56:55; three
  lane commits landed after it — `6966645` (04:57:02), `c1daaa7` (04:57:10), `2dcf06c` (04:57:19),
  all "final seat-report revisions". The third erratum says "**Lane tip at this erratum:
  `caf1e2b4…`**", which is three commits stale; the dispatched after-hash `2dcf06c…` is the true
  tip. Nothing cited is dead or orphaned, so this is the commit-before-report ordering item, not a
  marker.
- **Round shape disagrees with its own registries.** `corpus/lessons/round-30.md:3` says "two v1
  waves (36 build, 34 falsify)"; the report says 33 falsify / 69 total; the committed registries say
  build `members` = 36 and falsify `members` = 33, with role mixes identical to the report's
  (`build`: 10 scout, 7 reviewer, 6 executor, 4 scribe, 3 critic, 2 connector, 2 mutation-tester, 1
  revenger, 1 simplifier; `falsify`: 12 scout, 8 reviewer, 5 critic, 5 executor, 1 mutation-tester, 1
  revenger, 1 connector — 16/33 attack). The lesson's `34` is the outlier.
- **Uncommitted wave evidence** — see the table row above.

## 2. Claim re-checks

### C1 — coverage: the contamination-transparency card admitted as an amendment

| measurement (mine, over committed bytes) | before `363a4ebf` | after `2dcf06c5` | report + errata |
|---|---|---|---|
| registry rows: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` | **82** | **88** | 82 → 88 ✓ |
| knowledge files: `git ls-tree -r --name-only <rev> corpus/knowledge \| wc -l` | **38** | **39** | 38 → 39 ✓ |
| index rows: `grep -cE '^\| \`knowledge/' corpus/README.md` | **38** | **39** | 38 → 39 ✓ |
| tier split (own awk over the tier column) | A **76** / B **4** / C **2** | A **78** / B **8** / C **2** | table says A 79 / B 7 — **superseded by erratum 2**, which says 78/8 and matches the bytes; the lesson `:93` also says 78/8 ✓ |
| the six new rows' cells | ids absent | S081 B, S082 B, S083 A, S084 A, S085 B, S086 B; every row `status=mined opened=2026-10-25 recheck=180d`; `used-by` = `corpus/knowledge/contamination-transparency-card.md, corpus/lessons/round-30.md` on all six | mined, tier A/B, used-by the entry ✓ |
| no existing row touched | — | `git diff --numstat 363a4ebf 2dcf06c5 -- corpus/SOURCES.md` → **6 2**; both deleted lines are empty separator lines (`git diff … \| grep '^-' \| cat -A` → `-$`, `-$`), i.e. the placement fix removed blank rows that had split the table — no existing row's status/recheck/used-by changed | "6 insertions, 0 deletions before the placement fix" ✓ |
| entry triad | — | `git show 2dcf06c5:corpus/knowledge/contamination-transparency-card.md \| grep -nE '^(source\|verified-at\|recheck\|writer):'` → 6 `source:` lines (S081–S086), `verified-at: 2026-10-25`, `recheck: 180d — …`, `writer: KengakuR30` | ✓ |
| fleet census (my run) | — | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → 14 `W04` + `ok <path>/corpus/SOURCES.md`, **exit 0**, byte-identical to `corpus/evidence/round30/census-after.txt` | exit 0, same 14 W04 ✓ |

**Counter line — evidence-verified, not executed** (lane-owned gate): `corpus/evidence/round30/adoption-after.txt`
→ `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok` / `exit=0`
(unchanged since `623c1fc`); freeze control `.ufo/waves/round-30/claims/control-nothing.txt` →
`entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok` / `exit=1`;
hardening control `corpus/evidence/round30/counter-hardening-control.txt` → same stub now
`census=fail` / `exit=1`. The three numbers the counter prints that I *can* re-derive independently
— 6 cited rows, 6 present rows, 6 mined rows — hold; `usedby_ok=1` holds by the six `used-by` cells
above.

**Verdict: improved.** Coverage moves on real ground (one admitted entry, six opened rows, index
parity 39/39, frontier bullet 275 partly discharged) and every count in the claim reproduces.

### C2 — calibration: the five routed defects D1–D5 closed

| measurement (mine) | observed | report + errata |
|---|---|---|
| before evidence `.ufo/waves/round-30/claims/defects-before.txt` | `DEFECT D1 … D5`, `defects=5`, `exit=1` | `defects=5`, exit 1 ✓ |
| after evidence `corpus/evidence/round30/defects-after.txt` | `ok D1/D2/D3/D4/D5`, `checks=5 defects=0`, `exit=0`; header names the measured commits `623c1fc9 -> d0253c52`; file last changed at `5cd9229` | table says "measured at `706ed3f2`" — **stale revision label**; erratum 1 re-measures at the tip with the same values ✓ |
| D1 | `git show 2dcf06c5:corpus/evidence/round29-attempt2/control-nothing.txt` → present at the path round 29 cites, carrying the report's seven-field line **and** the wave file's eight-field line, each labelled, plus a provenance header | ✓ |
| D2 | `corpus/lessons/round-29.md:231-236` → the kappa sentence now names the scope its command measured (`grep -rn kappa corpus/knowledge/*.md` → 0 hits) with the lane-wide 65/66/67 counts stated separately | ✓ |
| D3 | `corpus/lessons/round-29.md:194` → S078 line-75 quote priced "8 words" | 9 → 8 ✓ |
| D4 | `git show 2dcf06c5:.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md \| wc -l` → 714 lines, in the HEAD tree | addendum committed ✓ |
| D5 | `.ufo/waves/round-29/attempt2/adoption-expect.json:12` → the S091 asymmetry note, with "the counter's seven printed fields are unchanged (`cited_rows=5`)" | ✓ |
| counter self-guard | `defects-after.txt` → `SELFTEST checks=5 failed=0` (evidence) | ✓ |

**Residual calibration defects found at the tip (routed, not scored).** The round's own *record*
still carries three superseded or wrong statements, plus one entry copyedit residue — all located
by me in committed bytes, all listed in §5. They do not falsify C2, whose five items verify, but they
are the class the round's Q20 criterion says a count check cannot see.

**Verdict: improved.** Five named defects go from red to green with an independent self-guard, and
three of the five I re-derived from the artifacts themselves rather than from the counter's print.

### C3 — operability: the adoption gate validates quotes

| measurement (mine) | before `363a4ebf` | after `2dcf06c5` | report |
|---|---|---|---|
| quote mode in the committed script | `git show 363a4ebf:plans/sources_adopt.py \| grep -c 'quote-file'` → **0** | `--quote-file` (`:741`), `--artifact` (`:746`), pairing errors (`:765`, `:769`), `quote_check()` with exit 6 over-long / 7 absent (`:340-344`), dispatch at `:770` | gained a quote mode ✓ |
| selftest | `SELFTEST cases=10 failed=0` (`.ufo/waves/round-30/claims/gate-before.txt`) | `SELFTEST cases=14 failed=0`, `exit=0` (`corpus/evidence/round30/gate-selftest-after.txt`, unchanged since `623c1fc`) | 10 → 14 ✓ |
| the "before" failure is real | `gate-before.txt` → `sources_adopt.py: error: unrecognized arguments: --quote-file /tmp/x --artifact /tmp/y`, `quote_mode_exit=2` | n/a | ✓ |
| pre-existing behaviour unchanged | — | `.ufo/waves/round-30/falsify/R30FxGateRegression.md` (committed): old sha256 `6fe6e762…`, new `e9b6bc04…`, 14 functions/classes byte-identical, ten original case names/order/verdicts preserved, five assigned invocations stdout- and exit-identical | five pre-existing invocations identical ✓ (evidence-verified; the seat's run, not mine) |
| disclosed limits | — | my own check: the S086 caveat is **30 CJK characters and 1 whitespace token**, so a 25-"word" cap cannot refuse it — the CJK inertness the round discloses is real, and a row could hide a long CJK quote behind one token | CJK cap inert ✓, zero-row file exits 0, 115 unexercised lines |

**Verdict: improved.** A real option pair, two distinguishable refusal codes, four new selftest
cases, and a pre-existing-invocation regression check with byte hashes — all committed, together with
an honest statement of what the gate does not bind (artifact ↔ cited URL).

## 3. Discernment spot-check (LEARNING.md, non-author sample)

I re-opened each source myself; two fetches are byte-identical to the round's own captures.

| item | decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|
| `corpus/knowledge/contamination-transparency-card.md` | **admit as amendment** | `https://doc.opencompass.org.cn/zh_CN/latest/advanced_guides/contamination_eval.html` (S084) and `https://www.anlp.jp/proceedings/annual_meeting/2025/pdf_dir/Q2-11.pdf` (S086), fetched 2026-10-25 05:00 -03 | **agree** | S084: HTTP 200, 32762 B, sha256 `c4447d93…` — identical to the row's recorded capture; all three quotes present at exactly the claimed lines 344 / 397 / 315, counting 3 / 7 / 1 whitespace tokens. S086: HTTP 200, 371155 B, sha256 `c3706aca…` — identical to the row; title on text-layer line 3, and the caveat `一致したものを一律に混入とみなして除去することには疑問が残る` is 30 CJK characters spanning lines 80-81, locatable only on newline-unwrapped extraction — which is exactly what the row says. The Q5 label the errata added ("the society publishes these proceedings **without peer review**") is present in the entry at `:150-152`. Two of six sources re-opened byte-identically is enough to accept the admission; the other four rest on the six second-seat re-reads the Gate names |
| `card-publication-contracts.md` (staged package) | **reject this round** | `shokuknow/lanes/kengaku/round6/SOURCES-PROPOSED.md:24` (S126, arXiv 2606.09809, tier **B**) and `shokuknow/.ufo/scopes/corpus-expansion-9/ScoutKengaku.md:40` ("The Chinese alphaXiv page is tier **C**: it is a machine rendering of arXiv 2606.09809, cited only for the Chinese wording, never as the paper's authoritative text"); staged file `shokuknow/merge/kengaku/knowledge/corpus/knowledge/card-publication-contracts.md` | **agree** | The candidate's third source is S167, the alphaXiv Chinese rendering the same campaign already scopes as tier C, and its strongest paragraph — "In Chinese the same genre is already framed as a corpus problem", whose abstract claims it then restates — is load-bearing on that row, not on a tier-A/B original the package already holds (S126). The Q2 tier floor refuses it. One nuance for the lane's flip condition: the scout's carve-out allows a tier-C mirror "for the Chinese wording", so a *narrower* claim (the Chinese title/wording only, with the abstract's substance re-cited to S126) would not be refused by this ground; the flip the lane wrote ("re-cited to the tier-B row") is the correct one |
| `judge-calibration-thresholds.md` (staged package) | **reject this round** | staged file `shokuknow/merge/kengaku/knowledge/corpus/knowledge/judge-calibration-thresholds.md:40-42`; the lane's S078 / S081 / S087 rows | **agree** | The entry's §2 carries per-variable kappa "0.00 to 0.35", "median 0.21", "ceiling 0.84" and pooled "0.46" and attributes them to S081. S081's own anchor cell — re-ticked this round — is the arXiv abs page plus three quoted spans, and `git show 2dcf06c5:corpus/SOURCES.md \| grep S081 \| grep -ci kappa` → **0**. A number no anchor cell carries is a numeric claim with no located quote (Q3), so the rejection stands on evidence I read myself, not only on the round's say-so |
| S084 row (new SOURCES row) | quote audit | the same OpenCompass fetch | **agree** | three quotes, 3 / 7 / 1 whitespace tokens — all ≤25 words and all byte substrings of the capture whose sha256 the row records |
| S086 row (new SOURCES row) | quote audit | the same ANLP fetch | **agree**, with the row's own caveat | title 3 tokens and the 30-CJK-character caveat counted as 1 token; both hold in the capture. This row is also the demonstration of the disclosed cap defect: the caveat is 30 characters and would pass a 25-*word* cap even at 12× its length |

Sample: 5 items — 1 admit, 2 rejects, 2 new registry rows. **All agree**; no disagreement to convert
into a `QUALITY.md` criterion this round.

## 4. Axis verdicts

| claim | axis | verdict | basis |
|---|---|---|---|
| C1 assimilation round 2 (card admitted as amendment) | **coverage** (lowest non-retired, tie-break over novelty) | **improved** | 82 → 88 rows, 38 → 39 entries with 39/39 index parity, tier split 76/4/2 → 78/8/2, six mined rows with correct `used-by`, census exit 0; frontier bullet 275 partly discharged. Not a coverage *saturation* claim: `PROVINCE.md` gained no round-30 section, and the round says so |
| C2 routed-defect closure D1–D5 | **calibration** | **improved** | `defects=5` exit 1 → `checks=5 defects=0` exit 0 with a self-guard; D1/D3/D4/D5 re-derived from the artifacts themselves, D2's scope sentence read at `round-29.md:231-236`. Residual record defects named and routed (§5) |
| C3 quote-validating adoption gate | **operability** | **improved** | option pair present in committed code with exit 6 / 7 / 4 / 2, selftest 10 → 14 cases, pre-existing invocations byte-identical per the committed regression receipt, limits disclosed |
| depth | depth | **unchanged** | `SCORECARD.md` diff base → tip is `33 0` (pure append; no score cell rewritten), so no owned score moved. The entry adds a field mapping, no new instrument claim |
| freshness | freshness | **unchanged** | census identical at both ends (same 14 `W04`); six rows opened 2026-10-25 with `recheck=180d`; round-29 receipts re-run unchanged per `LOG.md` |
| novelty | novelty | **unchanged** | no prior-art or phenomenon claim; the entry is declared an amendment and S091 stays priced as prior art |
| adjacency | adjacency | **unchanged** | connector + falsify sibling seats report no sibling contest; no `PROVINCE.md` change |

**No axis is harmed.** The evidence for that is mechanical, not a reading: the base→tip
`SCORECARD.md` diff contains zero deletions, so no score was lowered; no previously admitted entry
was deleted or falsified by this round's diff (`git diff --name-status` shows one added knowledge
file and no entry removals); and the fleet census is byte-identical before and after.

## 5. Trend verdicts and routed defects

**Trends (mine, not the lane's).**

- **expansion: improved** — one net-new admitted entry on ground the coverage map did not hold (the
  card-format row `:242` moves from "no standard card format" to a landed amendment), six `mined`
  rows it cites, index parity 39/39, and frontier bullet 275 moved from unopened lead to partly
  discharged. Bound: the coverage/surfaces leg did not move (no `PROVINCE.md` round-30 section).
- **quality: improved** — a ten-repair falsification pass over the round's own bytes (twelve landed
  claims corrected before the second commit, per the report), a quote valve with killed mutants, a
  counter whose own neutering is now visible, and Q13 green at the landing commit. No previously
  verified artifact regressed: the round-29 receipts re-run unchanged and the census is identical.
  Bounds: the entry copyedit residue and two wrong lesson cells listed below, plus the disclosed CJK
  cap, zero-row pass and 115 unexercised lines.
- **discernment: improved** — the round refused its own staged anchors (a 30-word quote absent from
  both fetches, a section that does not exist in v2, flattened fullwidth quotes), kept its own "two
  new fields" overclaim out of the entry, and quarantined two register rows with a verdict instead of
  appending. My outside sample agrees on 1 admit and 2 rejects. Cost, disclosed by the lane itself:
  four of its self-assessments needed a falsify seat to correct.

**Routed defects the lane must fix next round** (queue of record until they land):

1. `LOG.md:792-793` still declares the delta as "**two new fields, one new value set**", which the
   entry retracts at `:78-79` ("Two earlier readings … overclaimed; this is the corrected one") and
   the mapping's own S2/R1/S1 rows contradict. `LOG.md` is append-only: append a named correction
   entry, never rewrite the line (PROTOCOL §Evidence standard, "a falsified claim in an append-only
   file gets a named correction entry in the lane's next round").
2. `corpus/lessons/round-30.md:66-67` states Q6 pass on "the delta is stated as one field, one
   placement, one value set" — the exact reading the entry now retracts. Replace the cell's basis
   with the admitted wording ("one field, and the rest is not a delta at all").
3. `corpus/lessons/round-30.md:60-61` lists the Q2 tier set as "`S085 B, S086 A`"; the registry says
   `S086 B` and the same lesson says so at `:93` ("tier A 76 → 78, tier B 4 → 8"). Q2 still passes
   (B clears the A-or-B floor) — the cell, not the verdict, is wrong.
4. `corpus/knowledge/contamination-transparency-card.md:125-126` repeats "**the card records what
   each stated, not a reconciled truth**" twice in one sentence — residue of the fix that removed a
   doubled bullet marker.
5. `corpus/knowledge/contamination-transparency-card.md:68`/`:71` — "**S2's tri-state integrity flag
   is the only new field**" against its own S2 row ("`unknown` / `not_controlled` are valid values"
   in the published form) and R3's row (the form's per-type `controlled | not_controlled | unknown |
   n/a`). Either narrow the sentence to what is new (the card-level *field*, not the tri-state
   vocabulary) or cite the form line that lacks it. Second seat-reported item in the same paragraph:
   `:139` names "the CC0 card" where the form is reported CC BY 4.0 — re-check the licence before
   the next citation.
6. **Uncommitted round work:** five wave seat reports are modified in the working tree
   (`build/R30DraftGate.md`, `build/R30RevLesson.md`, `falsify/R30FxCoverageAxis.md`,
   `falsify/R30FxEntryCompleteSet.md`, `falsify/R30FxEntryQ4Q6.md`; 349 insertions / 82 deletions
   against `2dcf06c`) and a writer was still active at 05:02:48 -03 — after the driver's `complete`
   line at 04:57:31. Commit them under a round-30 entry or revert them; the closure could not, and
   did not, touch them.
7. **Report ordering:** the report's last commit (`c5807fe7`, 04:56:55) precedes the lane's final
   three commits (`6966645`, `c1daaa7`, `2dcf06c`), so erratum 3's "lane tip at this erratum:
   `caf1e2b4…`" is stale. Cite the tip the round actually leaves, and add the erratum as its own
   commit after the last lane commit.
8. **Round shape:** `corpus/lessons/round-30.md:3` says "34 falsify" seats; the registries and the
   report say 33 (16 attack roles, 48%). Correct the lesson.

**Promotion note for the operator (not mine to act on).** The four `SHONEN.md` boxes look checkable
by a non-author from this round's own evidence: box 2 (end-to-end task logged) and box 3 (executable
without oral context — four commands with their exits in `corpus/lessons/round-30.md` §Landing and
the evidence directory) have fresh round-30 pointers, box 4 rests on `PROVINCE.md:129` (unchanged,
and the round states the non-move), and box 1 rests on `SKILL.md` content unchanged since round 29.
Promotion is operator-owned; this artifact writes no `[x]`.
