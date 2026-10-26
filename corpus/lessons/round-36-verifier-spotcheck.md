author: hyaku closure (non-author integrator, @m_opus)

# Round 36 — non-author closure spot-check (kengaku, 2026-10-26)

Measured against lane tip `0fb87f88488839a923c28a777b9b69594259043c` (before: `b662a5d6dd370491049e4206818373c61be44816`).
Dispatch digest (`.ufo/watchdog.log`, mutable, copied here):
`2026-10-25T21:47:15-03:00 launch kengaku round=36 pgid=3060325 driver=hyaku-inline attempt=1` ·
`2026-10-26T01:03:32-03:00 complete kengaku round=36; hyaku-inline attempt=1`.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H %ci' -- .ufo/reports/round-36/kengaku.md` | `kengaku-shokunin 05a69bf06784e79da7ca20905e08302ffa5e1af2 2026-10-25 23:59:43 -0300`. Committed after `0fb87f88` (committer 23:58:49), before the 01:03:32 complete line — ok. The report's author date (23:58:33) precedes the author dates of `612458f3`/`0fb87f88`; ordering holds on commit time |
| `SHONEN` heading, one line per box | read report | `## SHONEN`, 4 lines, all `[~]` with pointers — ok |
| cited lane commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for `b662a5d6 3241b86c acbda2f3 f9efce3b 805fe790 7d1fa691 85655006 c16956d3 b85af35d 612458f3 0fb87f88` | 11/11 resolve, 11/11 ancestors |
| pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state …` ; `git -C lane status --porcelain` ; `git ls-remote origin refs/heads/master` | `local=remote=0fb87f88… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote `0fb87f88…` |
| prompt carries the template contract | `diff templates/round-prompt.md <(sed -n 1,140p .ufo/prompts/kengaku-round-36.md)` (prompt committed `f8a988a4`) | sections 1–5 differ from the canonical template only in substituted placeholders; §6 hyaku addendum follows — ok |
| minimum report content | read report | work + evidence pointers, landed-changes table tied to `LOG.md`, before→after per claim, Sources & frontier (counting command, tier deltas), trend verdicts, stale-lane line — ok |

Conformance defects (status-neutral):
- **Round size below the run-7 floor:** wave 1 only, 40 seats (`.ufo/waves/round-36/build-results.json`) against the directive's 64; wave 2 (34 seats, `falsify-spec.json`) committed and not dispatched. The report says so plainly.
- **Attribution:** `6e1bc4a` ("in-flight snapshot committed by the orchestrator") carries the lane identity; it adds `falsify-spec.json` and `make_falsify_spec.py` only, and the report's landed-changes table does not list it.
- **Measured revision:** `measure-final.txt` is measured at `612458f3`, not the cited tip; `git diff --stat 612458f3 0fb87f88` shows only `measure-final.txt` and `census-after.txt` added, so the measurement transfers. I re-ran C2 at `0fb87f88` (below).

Status: `ok`.

## 2. Claims — re-measured vs evidence-verified

Plain measurements over committed bytes (`git show <rev>:…`, `git ls-tree`), plus a clean `git clone --no-local` of the lane at `0fb87f88` in a `mktemp` dir outside the lane (`git status --porcelain --untracked-files=all` → 0 lines):

| quantity | command | before (`b662a5d6`) | after (`0fb87f88`) | reported |
|---|---|---|---|---|
| SOURCES registry rows | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | 100 | 103 | 100→103 ✓ |
| tier / status histogram | CORPUS census awk | A=85 B=13 C=2; mined=84 queued=8 rejected=8 | A=88 B=13 C=2; mined=87 queued=8 rejected=8 | A 85→88, mined 84→87 ✓ |
| malformed rows (NF≠13) | CORPUS census awk | — | 0 | — |
| knowledge files / README index rows | `git ls-tree --name-only <rev> corpus/knowledge/ \| grep -c '\.md$'`; `git show <rev>:corpus/README.md \| grep -cE '^\| \`knowledge/[^\`]+\` \|'` | 42 / 42 | 43 / 43 | 42/42→43/43 ✓ |
| committed nested wave paths (R35-D3) | `git ls-tree -r --name-only <rev> \| grep -cE '^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-'` | 21 (also 21 at freeze `3241b86c`) | 0 | 21→0 ✓ (912 round-28 nested paths untouched, as the frozen limit states) |
| ledger `corpus/defects-round35.jsonl` | `git show <rev>:… \| jq -c '{id,status,closed_round}'` | freeze `3241b86c`: R35-D1..D4 `open` | R35-D1..D4 `closed`, `closed_round: 36` | rows=4 closed=4 ✓ |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | — | exit 0, 15 W04, `kengaku ok` | exit 0, 15 W04 ✓ |

- **C1 (calibration) — evidence-verified, not executed.** `plans/pkg_gate.py` and `plans/round36_c1_verify.py` are registered gates (`SKILL.md:574-575`), so per §Gate standard I did not run them. Committed evidence I read: `.ufo/waves/round-36/integrate/measure-final.txt` (clean sparse clone, `untracked_in_clone=0`): 14 `FIXTURE … ok` lines, `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`, `rows=4 closed=4 observed_pass=4 mismatches=0`, `PREDICATE C1 pass`, `exit=0`. Red-before and skip-controls committed in `.ufo/waves/round-36/claims/`: absent gate `unevaluated=14` exit 1; round-35 counter `LEGACY accepted=7/7`; accept-all `false_green=11`; reject-all `false_red=3`. Plain cross-checks: `pkg_gate.py` absent at freeze (`git cat-file -e 3241b86c:plans/pkg_gate.py` fails); tip sha256 `ea638822…` equals `build/R36GateB/pkg_gate.py`; the frozen battery `round36_c1_verify.py` (`d7c3687c…`), `pkg-spec-r35.json` (`e085b435…`) and `toolathlon-package.md` (`00132ab0…`) are byte-identical at freeze and tip; `grep -nE 'k36-' plans/pkg_gate.py` is empty (no fixture-root keying). The R35-D4 erratum is one line (`grep -c '^Erratum (round 36):'` → 1), and `toolathlon-package.md:30-36` gives 13 + 23 + 1 = 37 against "of 38". **Verified**: the frozen predicate holds, and the plain quantities behind it re-measure. Limits the lane states itself: the battery is gameable by a fixture-keyed gate (`R36CritBattery`); eight gate clauses have no fixture (`R36RevClaims` FG1); no mutation wave ran.
- **C2 (coverage) — re-measured.** In the clean clone: `python3 plans/round36_c2_verify.py --lane .` → `W1 ok … W6 ok`, `checks=6 defects=0`, `PREDICATE C2 pass`, exit 0 (before, frozen: `checks=6 defects=4` exit 1, `claims/control-c2-nothing.txt`). `python3 plans/regex_log_probe.py --lane .` → exit 0, `cases=24 observed_pass=8 observed_fail=16 mismatches=0`, byte-equal to `corpus/evidence/round36/regex-log-probe.txt` (`cmp`). `sha256sum -c SHA256SUMS` in `corpus/evidence/round36/tb2-regex-log/` → 5/5 OK. The C2 counter is the probe's self-test (`SKILL.md:576`), not a registered gate, which is why I ran it. **Verified.**
- **Amendment 1 neutrality (independent check).** `git diff 3241b86c 0fb87f88 -- plans/regex_log_probe.py plans/round36_c2_verify.py` shows exactly two changed lines: `.replace(d, "<tmp>")` at `regex_log_probe.py:127` and the `PROBE_SHA256` constant. `git log 3241b86c..0fb87f88` touches these instruments only in `acbda2f3`, which precedes the wave-1 dispatch `f9efce3b`. I ran the freeze-commit probe (`git show 3241b86c:plans/regex_log_probe.py`) in the clone. With `/tmp/tmp*/` replaced by `<tmp>/`, its output is byte-equal to the committed receipt, and its `--dry` output is identical to the amended probe's and to `regex-log-dry-cases-freeze.txt`. The amendment changes printed paths only, never a verdict or a prediction. My ruling for the record is `revision`, consistent with `R36ConnAmendment.md`. The open L0 question (`revenger | round-69`) stays the operator's.

### No-harm audit

`git diff b662a5d6 0fb87f88 -- SCORECARD.md` shows +56 lines and 0 deletions: two appended capability rows (`package-gate`, `pattern-valued-grader-probe`, first-working round 36) and an appended round-36 section with planned and errata blocks. Every axis is stated as held (calibration 8, coverage 7 under the L0 cap, novelty 7, depth 9, operability 8, freshness 8, adjacency 8). `git diff b662a5d6 0fb87f88 -- corpus/README.md corpus/QUALITY.md SKILL.md PROVINCE.md LOG.md corpus/knowledge corpus/SOURCES.md` contains 0 removed lines. The one removal in the round is the 21 nested round-34 mirror paths (R35-D3), with a sha256 manifest. `plans/round35_c1_verify.py` V4 now fails on its frozen 42-file pin, as expected for a freeze-only counter; the claims file and report record this.

### Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| calibration (C1) | **improved** | frozen predicate met (committed receipt), red-before controls committed, 4 routed round-35 defects closed with plain re-measures (21→0 nested paths, 4 open→4 closed, erratum present, recount 37 vs 38); the legacy counter's 7/7 junk acceptance is replaced by a gate rejecting all 7; limits (gameable battery, clause gaps) are disclosed by the lane, not hidden; score held 8→8 |
| coverage (C2) | **improved** | counter `defects=4→0` re-run by me at the tip; probe receipt byte-equal; captures match SHA256SUMS and the live pinned URLs; second TB2 task moved from Frontier to core; score 7→7 held by the L0 cap |
| novelty | unchanged | no claim; `R36ScoutPriorArt` priced the instrument incremental |
| depth | unchanged | |
| operability | unchanged | two capability rows entered with demonstrations (probe re-run by me; gate by committed receipt) |
| freshness | unchanged | |
| adjacency | unchanged | PROVINCE round-36 section scopes the admission to one grader's offline behaviour |

No axis harmed. Both claims verify. Neither claim is exploratory.

## 3. Discernment spot-check (`round-36.md` `## Gate`)

| item · decision | re-opened source | agree/disagree | reason |
|---|---|---|---|
| `knowledge/tb2-regex-log-grader.md` · **Admitted** | the entry; probe re-run in clean clone; live `raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/regex-log/` | **agree** | provenance trio first (`source:` S108–S110 with URL + anchor, `verified-at`, `recheck`); probe 24/24 `match=yes` reproduces; the headline finding ("a literal alternation of the nine expected dates passes") is case `hardcoded-expected-dates predicted=pass observed=pass`; live `test_outputs.py` holds 25 sample-log strings and a 9-date literal `expected_dates` list (lines 72–82; the lesson says 71–81 — one-line drift, wording only). Post-hoc findings are labelled post-hoc. |
| S108 `tests/test_outputs.py` · **Admitted (mined)** | live URL, `sha256sum`, `sed -n 87p` | **agree** | live sha256 `345c3bd0…5e8f72` equals row, capture and counter pin; line 87 is `matches = re.findall(pattern_text, log_text, re.MULTILINE)`; quote ≤25 words; tier A right for the code's own behaviour. |
| S109 `tests/test.sh` · **Admitted (mined)** | live URL, `sed -n '20p;26p'` | **agree** | sha256 `4770437e…6c334` matches; `echo 1 > /logs/verifier/reward.txt` at :26 and `-w pytest==8.4.1 \` at :20 present. |
| S110 `instruction.md` · **Admitted (mined)** | live URL, `sed -n 2,4p` | **agree on admission; disagree on one anchor cell** | lesson quote at :2 (19 words) and row quote at :3 (19 words) are verbatim; :4 "without leading zeros in each octet" confirms the entry's reading. **But the row's anchor sha256 is 63 hex digits** (`4f7ac05e70cf922ea0f…`) and the live, capture and `SHA256SUMS` digest is `4f7ac05e70cf9220ea0f…`: one `0` was dropped. Nothing checks the row's digest against the manifest (W1 checks the capture, W2 checks row shape), so the counter cannot catch it. Routed item 1. |
| Package `grader-fixture-probe-stage3.md` (S170, S171) · **Refused** | `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/grader-fixture-probe-stage3.md:1-35`; `spreadsheet-grader-fixtures.md:6-11` | **agree** | the package says it is "not yet a discrimination verdict" (3 of 4 reject the identical pair, the 4th fails to import), and the staged stage-4 entry says "All four spreadsheet graders now discriminate". It is the interim state of a lineage its successor supersedes. S170's locator `lanes/kengaku/round9/…` exists only in shokuknow, not in this lane. |
| Package `grader-fixture-coverage.md` (S155) · **Refused** | same dir, `:2`; `SOURCES.append.md:85` | **agree** | its sole source is own-work S155 at `lanes/kengaku/round8/…`, which has no in-lane receipt to re-run. |
| Package `toolathlon-grader-behaviour-probe-2026-10-23.md` (S130) · **Refused** + erratum | committed copy `corpus/evidence/round36/toolathlon-package.md:19,30-36` | **agree** | stated denominator 38 against rows 13 + 23 + 1 = 37; the erratum line now records the second reason that the round-35 spot-check found missing. |

New SOURCES rows re-opened: S108, S109, S110 (all three, above). URLs resolve at the pinned commit, all quotes are ≤25 words and verbatim at their stated lines, and two of the three digests match. Census exit 0, `kengaku ok`, 15 W04 — the same set as before, with no new duplicate.

**Discernment conclusion:** the spot-check agrees with the gate on 4/4 sampled admits (entry, S108–S110) and 3/3 sampled refusals. The one disagreement is narrow: an S110 anchor-digest transcription error, not a wrong admission. The round-35 disagreement (counters accepting junk, routed items 1–4) became lessons (`round-36.md` §Mistakes 1–2) with grounded criteria `QUALITY.md` Q24 and Q25, each citing its lesson.

## 4. Trend verdicts

- **expansion — improved.** One admitted entry on ground the coverage map held only as Frontier (a second TB2 task, with a regex-artefact grader class). S108–S110 are `mined`, `used-by` resolves (census `kengaku ok`), the probe was re-run by me, and two capability rows entered with demonstrations. It is an instance increment, not new breadth, as `R36CritScope` says.
- **quality — unprovable-but-better.** A stronger instrument supersedes the round-35 counters of record (7/7 junk accepted → 0 wrong on 14 fixtures), errata were appended rather than rewritten (S130 denominator, Amendment 1 digest table, stale frozen-digest block), and the new entry re-verifies against live pinned bytes. Against that, a new admitted row fails its digest re-check by one character (S110) and the planned wave-2 re-verification did not run. That keeps this at better-but-not-proven rather than `improved`. It is not `harmed`: the defect was first found here and is routed, not left standing after notice.
- **discernment — improved.** The spot-check agrees with the gate on sampled admits and rejects, and the previous round's disagreement became grounded `QUALITY.md` criteria (Q24, Q25 → `round-36.md` §Mistakes). The lane graded this `unchanged`. I rule `improved` on LEARNING.md's criteria, with the caveat that the battery and C2 counter weaknesses found in wave 1 are named as limits but not yet built into a stronger criterion.

## 5. Routed defects (lane fixes next round; status-neutral)

1. **S110 anchor digest truncated.** `corpus/SOURCES.md` S110 anchor reads `sha256 4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c` (63 hex). The true digest is `4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c` (`SHA256SUMS`, live). Append a correcting row whose `teaches` opens `supersedes S110 —`, or a lesson erratum (append-only rule 2). Add a counter check that each row's anchor digest equals the capture manifest. The same typo sits in the wave-1 draft `build/R36RowsDraft*.md`.
2. **Frozen battery gameable and clause-incomplete** (`R36CritBattery`, `R36RevClaims` FG1). Round 37's planned mutant harness against `pkg_gate.py` must cover the eight fixture-less clauses and include a renamed-fixture run.
3. **C2 counter admits a junk package** (`R36CritC2Counter`, `checks=6 defects=0`). W2/W3 check shape, not support. The next coverage counter needs a support check (each quote verbatim on its cited capture line, which `pkg_gate.py` already has) before freeze.
4. **Wave-1 findings not absorbed:** `R36CritScope` F3–F6, F8, F10 (wording, the PROVINCE rewrite, sub-row label) and `R36RevProbePred` (cases `ip-no-left-boundary` and `ip-no-right-boundary` fail on lines other than the one they name, so they are not independent evidence). Plus minor anchor drift: the entry's S110 `lines 1–11` vs the row's `:1-19`, and the lesson's "lines 71-81" vs list lines 72–82.
5. **Amendment 1 ruling** stays on the L0 queue (`revenger | round-69`). The closure evidence for it is that the freeze-commit probe reproduces the receipt modulo `<tmp>` and `--dry` is identical (§2).
6. **Spot-check debt:** `round-36.md` `## Spot-check` reads "Pending". This file answers its items 1, 2, 5 and 6. Items 3–4 (hand-running the gate on the six line fixtures; fixture-name keying) were not executed, since I don't run a sibling's gate, beyond `grep -nE 'k36-' plans/pkg_gate.py` → empty.
7. **SHONEN (for the operator).** All four boxes remain `[~]`. The end-to-end-task box now has non-author-checkable evidence in two consecutive rounds: this round's probe re-run byte-equal and the C2 counter green in my clone. I did not tick it; promotion is operator-owned. I did not re-assess the other three boxes.
