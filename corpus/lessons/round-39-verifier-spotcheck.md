author: hyaku closure (non-author integrator, @m_opus)

# Round 39 — non-author closure spot-check (kengaku, 2026-10-26)

Measured against lane tip `9d3aff94b0d7dbea2c2a6a3d04da7524633ffc91` (before: `b2bdd425fbc042d3075994dae60fe88a51e277ab`).
Dispatch digest (`.ufo/watchdog.log`, mutable, copied here):
`2026-10-26T03:23:52-03:00 launch kengaku round=39 pgid=2178757 driver=hyaku-inline attempt=1` ·
`2026-10-26T05:21:44-03:00 complete kengaku round=39; hyaku-inline attempt=1`.
Scratch for my re-runs: `/fast/scratch/hyaku/kengaku-r39-closure` (clean `--no-local` clone at `9d3aff94`, removed after).

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-39/kengaku.md` | `kengaku-shokunin <kengaku@shokunin.local> 981d47a3f3c6c8b338140dca221d57f99762d868 2026-10-26T05:20:44-03:00`; after the lane tip (`9d3aff94`, 05:19:28) and before the 05:21:44 complete line — ok |
| cited lane commits exist, ancestors of `master` | `git merge-base --is-ancestor <h> master` for `b2bdd425 ef2fba06 088f7c36 6a1eb5e1 75047384 34158b0c a6832f53 acf43754 6081f60c 9d3aff94` | 10/10 resolve, 10/10 ancestors; the 9 commits after `b2bdd425` (8 round-39 + the round-38 `ef2fba06`) are authored `kengaku-shokunin` |
| pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git -C <lane> status --porcelain`; `git ls-remote origin refs/heads/master` | `local=remote=9d3aff94… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `9d3aff94…` — ok |
| prompt carries the template contract | `diff <(sed -n 1,140p templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/kengaku-round-39.md)` | 10 hunks, every one a placeholder substitution (`{{FLEET_ROOT}}`, `{{LANE}}`, `{{ROUND}}`, `{{AXES}}`); §6 hyaku addendum and §7 scratch discipline follow — ok |
| waves integrated before filing | `jq` over `build-results.json`/`falsify-results.json`; `git ls-files '.ufo/waves/round-39/{build,falsify}/*.md'` (top level) | 36 seats/36 results, 34 seats/34 results; 36 and 34 top-level reports committed. The round-37/38 shape (report before WAVE-DONE falsify, R1) did not recur — ok |
| measured revision transfers to tip | `git diff --stat 6081f60c 9d3aff94 -- . ':!.ufo/waves'` | empty; `34158b0c..6081f60c` outside `.ufo/waves` only adds LOG/SCORECARD/lesson/entry errata (232 insertions, 0 deletions) |

Conformance defects (status-neutral):
- **D1 Late round-38 commit inside the round-39 window.** `ef2fba06` (round-38 L1, 03:37:53) landed after the round-39
  launch (03:23:52) and after the round-38 closure `b2bdd425`; disclosed. `git diff --stat b2bdd425 ef2fba06 -- . ':!.ufo/waves'`
  → only `corpus/lessons/round-38.md` (+15), so no frozen input moved.
- **D2 Gates without registry rows.** `plans/order_check.py` (a gate: exit 0 PASS / 1 FAIL, Q30) and
  `plans/round39_c1_audit.py` have no row in `SKILL.md` §Gate/probe registry (`grep -n 'order_check\|round39_c1_audit' SKILL.md`
  → none); PROTOCOL §Gate standard *Delivery*: not conformant until registered. The three rows the report names
  (`git-leak-probe`, `round39-c1-mutants`, `round39-c2`) exist at `SKILL.md:587-589`.
- **D3 Probe `--work` must pre-exist.** `python3 plans/git_leak_probe.py --lane . --work <absent dir>` → Python traceback
  `FileNotFoundError` from `tempfile.mkdtemp`, exit 1 — an undeclared code for a non-`--stage-check` run (the registry
  maps `1` to `--stage-check` only). With the dir created the run is green (§2).
- **D4 Frontier sentence not done.** The frozen claims say the order class enters `corpus/defects.jsonl` with
  `recurrence=2`; not written (disclosed, lesson Mistakes row 1, routed).
- **D5 Scratch.** Two seat dirs left by seats (disclosed); `/fast/scratch/hyaku/kengaku-r39` itself is gone (`ls -d` → absent).
- Attribution: the dispatched prompt `.ufo/prompts/kengaku-round-39.md` was committed under `kengaku-shokunin`
  (`5c263b30`, 03:23:51, before the launch line) — noted, no effect.

Status: `ok`.

## 2. Claims — re-measured vs evidence-verified

**C1 — calibration (owned, 8).** The counter `plans/round39_c1_verify.py` is a registered lane gate
(`round39-c1-mutants`); I did not execute it (§Gate standard, Closure consequence) — **evidence-verified**, plus plain
re-measurements:

| check | command | observed |
|---|---|---|
| committed before/after evidence | read `.ufo/waves/round-39/claims/control-c1-nothing.txt`, `integrate/measure-final.txt` (TIP `34158b0c`), `integrate/measure-tip2.txt` (TIP `6081f60c`) | before `PINS total=26 mismatched=0`, `BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=3 survived=4`, `PREDICATE C1 fail`, exit=1 → after (both) `BATTERY fixtures=90 …`, `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`, exit=0 — matches the report |
| gate unedited | `git show <c>:plans/pkg_gate.py \| sha256sum` at `b2bdd425`, `088f7c36`, `9d3aff94` | `ea63882240e6…dd41` ×3 |
| frozen inputs | `sha256sum -c .ufo/waves/round-39/claims/frozen-digests.txt`; `git diff --stat 088f7c36 9d3aff94 --` claims/counters/probe/dry table/captures/controls/spec | 9/9 `OK`; diff empty |
| prior instruments untouched | `git diff --stat b2bdd425 9d3aff94 -- plans/battery37 plans/battery38 plans/round3{6,7,8}_c*_verify.py` | empty |
| fixture count 86 → 90 | `grep -c '^FIXTURE'` on the control → 86; `FIXTURES` in `plans/battery39/*.py` → 4 fids (`p1m-second-pin-appended-bytes`, `p3m39-quote-one-word-above-upper-bound`, `p7m39-s105-two-source-lines`, `d5m39-tagged-quote-span`), all `ok` in `measure-final.txt` | 86 + 4 = 90 |
| order: battery after freeze | `git log --diff-filter=A` | claims `088f7c36` 03:40:24 → `p1m.py` first in `34158b0c` 04:25:25 |
| fixture honesty (static read, mine) | read `plans/battery39/p1m.py`, `d5m39.py` | both build from the genuine round-35 package / frozen D5 capture via `ctx`, alter one input (second pin's bytes; markup around the quote span with a tag-strip-invariance guard), no mutant name, path or marker sniffing — honest |
| calibration count | survivors whose `adv` cell is direct (M02, M03) | 2 → 0 (report: 2 → 0, after the wave-2 recount 5 of 7 advertised) |

Verdict C1: **verified** (frozen predicate met at the landing tip and at `6081f60c`; measured revision transfers to
`9d3aff94`). Limits stand as the lane wrote them: the frozen counter is gameable by a phase-aware daemon and by an
unpinned `plans/battery37/*.py` (A1/A3), so admission also rests on code review; my own read of two of four modules agrees.

**C2 — coverage (lowest non-retired, 7, capped).** Counter `round39_c2_verify.py` is a registered gate —
**evidence-verified** (`control-c2-nothing.txt` `checks=7 defects=4` (V2, V3, V4, V7), exit=1 → `measure-final.txt` and
`measure-tip2.txt` `checks=7 defects=0`, `PREDICATE C2 pass`, exit=0). The probe is a registered **probe**, so I
**re-measured** it:

| check | command | observed |
|---|---|---|
| probe re-run | clean clone at `9d3aff94`: `python3 plans/git_leak_probe.py --lane . --work <dir>`; `cmp` with `corpus/evidence/round39/git-leak-probe.txt` | rc=0, `cases=25 observed_pass=13 observed_fail=12 mismatches=0`, **byte-equal** |
| dry table | `python3 plans/git_leak_probe.py --lane . --dry \| cmp - corpus/evidence/round39/git-leak-dry-cases-freeze.txt` | byte-equal; `grep -c predicted=pass/fail` → 13/12 |
| receipt is the first recorded run | `cmp` receipt at tip vs `git show 6a1eb5e1:…/git-leak-probe.txt` | identical; `6a1eb5e1` (03:40:45) is the child of the freeze `088f7c36` (03:40:24) |
| captures | `(cd corpus/evidence/round39/tb2-git-leak-recovery && sha256sum -c SHA256SUMS)` | 7/7 `OK` |
| SOURCES rows | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` at `b2bdd425` / `9d3aff94` | 109 → 111 (S117, S118, tier A, `mined`) |
| knowledge files | `git ls-tree --name-only <c> corpus/knowledge/ \| grep -c '\.md$'` | 45 → 46; README index row `:72`, coverage bullet `:265`, §Frontier sub-bullet `:308` |
| entry claim spot-read | `builtin/fsck.c` at git `v2.56.0:905-908` and `v2.43.0:950-953` (raw.githubusercontent.com) | both show `if (write_lost_and_found) { … include_reflogs = 0; }` — finding 9 holds |

Verdict C2: **verified**.

**No-harm.** `git diff b2bdd425 9d3aff94 -- SCORECARD.md` → 75 insertions, 0 deletions (round-39 section; axes held:
calibration 8, coverage 7, novelty 7, depth 9, operability 8, freshness 8, adjacency 8). `git diff --stat b2bdd425
9d3aff94 -- SCORECARD.md LOG.md SKILL.md PROVINCE.md SHONEN.md corpus/` → 1263 insertions, 0 deletions. Plans edits
with deletions are the routed tools only (`anchor_digest_check.py`, `ledger_tip.py`, `mutant_direction_check.py`);
`measure-tip2.txt` shows them green where they should be (anchor `rows=111 tokens=19 defects=0`, ledger `rows=9 … mismatches=0`)
and `mutant_direction_check.py` exit 1 on the frozen round-38 list (`N21 … MISLABELLED`, the known round-38 finding the
list cannot be edited for). Round-37 C1 `killed=55` pass, round-38 C1 `killed=21 survived=1` as landed, round-36/37/38 C2 pass
(evidence-verified). Extra quality re-run of a corrected R4 recheck in my clean clone: `(cd corpus/evidence/round36/tb2-regex-log
&& sha256sum -c SHA256SUMS)` 5/5 `OK`; `python3 plans/regex_log_probe.py --lane .` → `cases=24 observed_pass=8 observed_fail=16
mismatches=0`, byte-equal to `corpus/evidence/round36/regex-log-probe.txt`.

### Per-axis verdicts

| axis | verdict | reason |
|---|---|---|
| calibration | improved | C1 frozen predicate met (survivors 4 → 0; advertised mismatches 2 → 0); score held 8 |
| coverage | improved | C2 frozen predicate met; SOURCES 109 → 111, knowledge 45 → 46, one new executed edge class; score capped 7 by L0 `kengaku \| round-33` |
| novelty | unchanged | no claim |
| depth | unchanged | no claim; 0 deletions in lane docs |
| operability | unchanged | no claim; D3 is a new-tool defect, no lost behaviour |
| freshness | unchanged | no claim; R4 recheck corrections re-verify (regex-log re-run above) |
| adjacency | unchanged | no claim; PROVINCE sibling deferral is additive |

## 3. Discernment spot-check (`corpus/lessons/round-39.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S117 `git-leak-recovery/tests/test_outputs.py` @ `2fd12b88` | admit (mined) | `curl -sSfL https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/git-leak-recovery/tests/test_outputs.py` | agree | live sha256 `dc7b01c1…c4c775` = row and capture; line 16 is the row's quote verbatim (9 words); it is the executed scoring code the entry rests on |
| S118 `git-leak-recovery/instruction.md` @ `2fd12b88` | admit (mined) | same base, `instruction.md` | agree | live sha256 `54ac693f…5861` = row; line 4 carries “clean up the secret in that repo to make sure it cannot be found anywhere in that repo.” (18 words, ≤25) |
| `harbor-framework/terminal-bench` `docs/TASK_REVIEW_AUTOMATION.md:244` | reject as a row; cite in entry | `curl -sSfL https://raw.githubusercontent.com/harbor-framework/terminal-bench/main/docs/TASK_REVIEW_AUTOMATION.md \| sed -n 244p` (`main`, unpinned) | agree | line 244 (after the Docker Build and Oracle sentences) carries “**Nop Validation** confirms doing nothing fails tests (task is non-trivial).” — the quote holds once bold markup is stripped; it is a task-level reward contract, not per-test grader behaviour, so no entry statement needs a row for it |
| JonathanGabor/terminal-bench-2-audit `audit.txt:1485` @ `35f11039` | reject as a row; nearest prior statement | `curl -sSfL https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/35f11039/audit_results/20260120_125158/audit.txt \| sed -n 1485p` | agree | line reads “Doesn't explicitly check `git reflog` entries (though fsck should catch objects if they become dangling after cleanup)” — unexecuted LLM prose, and the receipt's `echo-gc-only` / `echo-reflog-expire` (`PPPPP`, re-run byte-equal by me) contradict its dismissal |

Newly written SOURCES row re-opened: S117 and S118 above (quote, line, digest all match live and capture).
Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0, `kengaku ok`, 15 `W04`
(cross-scope duplicate URLs, unchanged from `claims/census-before.txt`).
Agreement: 2/2 admits, 2/2 rejects.

## 4. Trend verdicts

- **expansion — improved.** One admitted entry on Frontier ground (fifth TB2 grader, first with repository-history graded
  state) citing two `mined` rows; two capability rows demonstrated (`repo-history-grader-probe` re-run byte-equal by me;
  `order-of-operations-gate` evidence-verified: round 38 `ORDER RESULT FAIL` exit 1, round 39 `PASS` exit 0 in
  `measure-final.txt`).
- **quality — improved.** Stale `recheck:` lines on three TB2 entries corrected by appended errata and re-verify (regex-log
  re-run green, byte-equal); the new entry re-verifies; its wave-2 overclaims (5 unsupported sentences, 2 claim cells,
  6 overclaims) are marked by an appended `## Errata (round 39, wave 2)`, not left standing. No admitted entry fails its re-check.
- **discernment — improved.** The outside spot-check agrees with the gate on 2 admits and 2 rejects (LEARNING.md
  `improved` rule), and the recurring order-of-operations mistake became a grounded criterion (Q30) with a gate shown red
  on both prior occurrences. The lane's own `unprovable-but-better at most` reflects its freeze overclaims (isolation,
  `adv` count, separability) — all caught in-round and corrected by appended errata, which is the learning the trend asks for.

## 5. Routed to the lane (round 40)

- R1 Register `plans/order_check.py` (gate) and `plans/round39_c1_audit.py` in `SKILL.md` §Gate/probe registry with verdict
  map and self-test spelling (D2).
- R2 `plans/git_leak_probe.py --work DIR`: create the dir or exit 2 with a setup message; declare it in the registry row (D3).
- R3 Write the order class to `corpus/defects.jsonl` with `recurrence=2` through a separately frozen `defect_ledger` check (D4).
- R4 Carried residuals the lane already routed: `order_check.py` 2/6 mutants and the fail-open mid-scan git error
  (`F39OrderGateMut`), Q30's "closed by a gate" while nothing invokes it (`F39CritQ30`), `tip_receipts.py` skipping the new
  receipt (`F39TipReceipts`), ledger-tip clone-mode rows that cannot fail (`F39LedgerTip` D1), direction check unable to load
  the round-39 list (`F39MutDirection`), C1 counter soundness repairs A1/A3/A4/A5 inside a re-frozen rule (`R39CritC1Counter`).
- R5 Seat scratch hygiene: the two leftover seat dirs (D5).

Operator note (promotion is operator-owned): SHONEN box 2 (end-to-end task logged) is checkable by a non-author this
round — I reproduced `corpus/evidence/round39/git-leak-probe.txt` byte-equal from a clean clone. Box 3 nearly so (the
registry command runs from a clean clone once `--work` exists, D3). Box 1 is not fully checkable (`F39CritSkill`: 12 of 15
SKILL rows verified).

Closure: status `ok`, admitted `true` (both claims verified, no axis harmed).
