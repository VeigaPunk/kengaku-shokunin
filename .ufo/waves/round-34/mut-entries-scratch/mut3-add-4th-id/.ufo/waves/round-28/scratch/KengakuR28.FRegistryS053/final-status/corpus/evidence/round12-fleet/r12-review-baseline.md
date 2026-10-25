# r12 review baseline — ReviewerBaseline (baseline auditor)

Task: audit HEAD before round-12 run bytes so later breakage is attributable. No repository files other than this report were modified. Commands below were run from the repository root unless stated.

## 1. Gate baseline and determinism

`git rev-parse HEAD` → `f09ff1fc4d9e1e106d07c02b5bf9c148579175df` (`round-11`).

| Command | Exit | Exact observed output |
|---|---:|---|
| `python3 grader.py` | 0 | `CHECKS n=280 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully re-derives offline` |
| `PYTHONHASHSEED=1 python3 grader.py` | 0 | same two lines |
| `PYTHONHASHSEED=99 python3 grader.py` | 0 | same two lines |
| `env -u PYTHONHASHSEED python3 grader.py` | 0 | same two lines |

`sha256sum /tmp/r12-bl-g1.out /tmp/r12-bl-g99.out /tmp/r12-bl-gu.out` → `88aa308929de04d5126c5cfe326640fa54074db049f0d01adcfe6210d54d2153` for each file; byte-identical under all three environments. (The files are captures of the commands above; the command and hash are reproducible.)

`python3 grader.py --selftest` → exit 0:

```text
[selftest] PASS S0 control (clean copies): exit 0, expected 0
[selftest] PASS S1 stored-ok flip (record layer): exit 1, expected 1 + check-id r8.replay.A-INC.ok (flip applied: True, id fired: True)
[selftest] PASS S2 run.log SUMMARY edit (summary layer): exit 1, expected 1 + check-id r8.summary.A-INC (id fired: True)
[selftest] PASS S3 raw-digit bump (re-parse layer): exit 1, expected 1 + check-id r9.replay.A-MONO.got (mutation applied: True, id fired: True)
[selftest] PASS S4 r11 stored-ok flip (record layer): exit 1, expected 1 + check-id r11.replay.A-CKPT4710.ok (flip applied: True, id fired: True)
[selftest] PASS S5 r11 run.log SUMMARY edit (summary layer): exit 1, expected 1 + check-id r11.summary.A-CKPT4710 (id fired: True)
[selftest] PASS S6 stats anchors (betai/t_crit known values): all known-value assertions hold
[selftest] ALL PASS
```

## 2. Re-run of all 41 r11 committed pointers

Classifications mean the command ran and the current result matches the current, documented round-11 state. A changed numeric pin is marked `REPRODUCE (superseded)` when the round-11 landing intentionally extended the tree; host disappearance is `DRIFTED-HOST`, not falsification.

| # | Pointer command | Observed output | Classification |
|---:|---|---|---|
| 1 | `git ls-tree -r 2575be6 --name-only \| grep -cE '\\.(py\\|sh)$'` | `12` | REPRODUCE |
| 1b | `find . \( -name '*.py' -o -name '*.sh' \) -not -path './.git/*' \| wc -l` | `27` (includes current untracked r12 ladder scripts if present) | REPRODUCE (superseded count) |
| 2 | `python3 grader.py` (r9 ordering gate) | exit 0, `n=280`, mismatches 0 | REPRODUCE (superseded count) |
| 3 | `sha256sum grader.py` | `14d54051a00e4ca1bed5d7b12f4ac3bff17e3b159251946444b8310dd0202af9` | REPRODUCE (superseded grader) |
| 4 | `wc -l grader.py` | `1711 grader.py`; source header says round-11 tree | REPRODUCE (superseded 936-line pin) |
| 5 | `md5sum corpus/evidence/round8-horizon/horizon.py` | `1c157e2a5f5cd3b8516d30c3d4a9c01d` | REPRODUCE |
| 6 | `md5sum corpus/evidence/round8-horizon/results.jsonl` | `df154cb524bf210782fb0f4a46fd1bdc` | REPRODUCE |
| 7 | `sha256sum corpus/evidence/round9-replication/predictions-r9.md` | `2a4f62ef20a65e7a7cb3b7414b54d0f995126209c3126ae674b7cc3af2bc1099` | REPRODUCE |
| 8 | `md5sum corpus/evidence/round9-replication/replication.md` | `d9235e41f3ebfdcabd368c71cde878a1` | REPRODUCE |
| 9 | `wc -l corpus/evidence/round8-horizon/horizon.py` | `349` | REPRODUCE |
| 10 | `wc -l SKILL.md` | `518` (r11 additions supersede 472) | REPRODUCE (superseded) |
| 11 | `awk '/^## Cited local sources/,0' SKILL.md \| grep -cE '^- '` | `23` (r11 additions supersede 20) | REPRODUCE (superseded) |
| 12 | cited `~/` extractor | `15` distinct paths (supersedes 14) | REPRODUCE (superseded) |
| 13 | cited backtick path-token extractor | `113` (classifier census changed with appended citations) | REPRODUCE (superseded) |
| 14 | `ls ~/Projects/webzites/repos/llm-wiki/wiki/karpathy/** 2>/dev/null \| wc -l` | `34` | REPRODUCE |
| 15 | path-by-path `test -e` over cited set | all current positive paths resolve except the two documented negative/host-drift paths below | REPRODUCE |
| 16 | `test -e /home/vgpnk/wikillm/llm-wiki` | `absent` | REPRODUCE (documented absence) |
| 17 | `find ~/bench-arena /tmp/bench-r8 -maxdepth 1 -newermt '2026-09-28 18:00' ...` | `0` lines; bench-arena mtime `2026-08-29 03:58` | REPRODUCE |
| 18 | `ls /tmp/bench-r7-l2-executor/graded \| wc -l` | `125` | REPRODUCE |
| 19 | `sha256sum /tmp/bench-r8/results.jsonl corpus/evidence/round8-horizon/results.jsonl` | both `bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204` | REPRODUCE |
| 20 | `python3 grader.py` metadata regeneration | exit 0, extended gate `n=280` | REPRODUCE (superseded count) |
| 21 | `grep -c 'seed *= *2000 *+ *pid *\\* *29' corpus/evidence/round9-replication/run_r9.py` | `0` (formula is delegated; same known finder artifact) | REPRODUCE (finder caveat) |
| 22 | `grep -o 977 grader.py \| wc -l` | `2` | REPRODUCE |
| 23 | two `grep -o '"cell":"A-CKPT...'` counts | `A-CKPT4710=24`, `A-CKPT710=16` | REPRODUCE |
| 24 | `grep -c '"pid":104' .../results-r9.jsonl` | `32` | REPRODUCE |
| 25 | grader record-shape replay | exit 0; all stored trees re-derived | REPRODUCE (superseded gate count) |
| 26 | `python3 grader.py --selftest` S3 | `r9.replay.A-MONO.got`, mutation/id fired true | REPRODUCE |
| 27 | `awk '/^## Surfaces/,/^## Refusals/' PROVINCE.md \| grep -cE '^\\| [^|-]'` | `10` surface rows (current table; prior “9” count was stale) | REPRODUCE (superseded) |
| 28 | `find corpus/evidence/round10-fleet -maxdepth 1 -type f \| wc -l` | `22` | REPRODUCE |
| 29 | README knowledge/lessons row counts | `22` / `13`, matching `find corpus/knowledge -maxdepth 1 -type f`=`22` and lessons=`13` | REPRODUCE (superseded) |
| 30 | `python3 grader.py` and `--selftest` | exit 0 / exit 0 | REPRODUCE |
| 31 | `test -e` for PROVINCE paths | all positive paths OK; bounties ledger missing | DRIFTED-HOST (documented round-11 disappearance) |
| 32 | `grep -rln '2505.06120' ~/Projects/webzites/repos/llm-wiki \| wc -l` | `0` | REPRODUCE |
| 33 | `grep -c '2505.06120\\|2307.13702' corpus/knowledge/eval-prior-art-calibration.md` | `4` | REPRODUCE |
| 34 | `head -4 corpus/evidence/round10-fleet/url-status.txt` | four shown URLs each `200` | REPRODUCE |
| 35 | `ls -l --time-style='+%Y-%m-%d %H:%M' ~/bench-arena/*.csv` | files dated 2026-08-29 03:06–03:30 | REPRODUCE |
| 36 | `wc -l corpus/evidence/round9-replication/ordering.log` | `2` (exists; r11 ordering log `7` lines) | REPRODUCE |
| 37 | `sha256sum corpus/evidence/round11-power/prereg-bundle.sha256` | `bae0a5851a73b71619cfd5ab4dc2ea3027a2e4779cd60379ad5c079f18294c92` | REPRODUCE |
| 38 | `python3 grader.py` r8 replay | exit 0, no mismatches | REPRODUCE |
| 39 | `python3 grader.py --selftest` | S0–S6 PASS, `[selftest] ALL PASS` | REPRODUCE (superseded 4→7) |
| 40 | `find ~/Projects/webzites/repos/llm-wiki/wiki/ai -name '*.md' \| wc -l` | `23` | REPRODUCE |

The two host surfaces that do not resolve are explicitly documented: `PROVINCE.md:8,15` and `SKILL.md` cited-source bullet 9 say `~/Projects/bounties/ledger/telemetry.jsonl` disappeared during round 11; `~/wikillm/llm-wiki` is an intentional documented absence (`PROVINCE.md:15`). No endpoint traffic was made in this audit.

## 3. README/disk index and PROVINCE surfaces

Index commands: `grep -c '^| \`knowledge/' corpus/README.md` → 22; `find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l` → 22. Lessons: 13 and 13. Evidence: `grep -c '^| \`evidence/' corpus/README.md` → 6; `find corpus/evidence -mindepth 1 -maxdepth 1 -type d | wc -l` → 8. Evidence mismatch is `round12-fleet/` and `round12-ladder/` on disk (the former is this untracked report directory and the latter is the r12 design directory); they are not yet README-indexed. Knowledge and lessons have no mismatch.

`PROVINCE.md:8-20` surface `test -e` results (command: the `for p in ...; do test -e "$p" && echo OK || echo MISSING; done` loop): research wiki OK; bench-arena files/tasks OK; served-model process surface not probed (endpoint forbidden to this lane); route telemetry MISSING; client telemetry/state OK; model catalogs/index OK; round8/9/10/11 evidence dirs OK (round12 not yet in PROVINCE); grader.py OK. Thus the round-11 ledger absence remains a documented host drift, not a new repo defect.

## 4. r11 ordering chain

Command `sha256sum -c corpus/evidence/round11-power/prereg-bundle.sha256` from repo root → exit 0, exactly:

```text
corpus/evidence/round11-power/probe_plan_r11.md: OK
corpus/evidence/round11-power/power_analysis_r11.md: OK
corpus/evidence/round11-power/predictions-r11.md: OK
```

Command `cat corpus/evidence/round11-power/ordering.log` → pre-hash and post-hash `2026-09-28T23:10:20Z`; run-script hashes `23:28:37Z`; `main-run-launch 2026-09-28T23:28:57Z`. Command `grep -m1 -o '"request_ts":"[^"]*"' corpus/evidence/round11-power/results-r11.jsonl` → `"request_ts":"2026-09-28T23:28:57Z"`. The bundle hash and script hashes predate the first request (equal timestamp at second precision for launch/first request, as noted in the r11 lesson; hash itself is earlier). F2 status: r11's bundle uses repo-relative paths and works from root; the prior r9 `.sha256.repo` bare-path caveat remains documented at `r11-review-baseline.md:33-37`—from repo root it exits 1, while the in-gate cwd-independent check passes.

## 5. Citation spot-check (10 fixed pseudo-random sample indices)

Selection command: `awk '/^## Cited local sources/{on=1;next} on && /^- /{n++; if(n==1||n==3||n==5||n==7||n==9||n==11||n==13||n==15||n==17||n==19) print n ":" $0}' SKILL.md`. Resolution command: `test -e` on each concrete local path (and glob expansion for `**`); endpoint URL was not fetched. Results: indices 1,3,5,7,11,13,15,17,19 resolve; index 9 (`~/Projects/bounties/ledger/telemetry.jsonl`) is absent and explicitly marked absent in the bullet. Strict resolution rate (all 10 bullets, no documented-negative exemption) = **9/10 = 90%**. The single failure is DRIFTED-HOST, not falsified repo evidence.

## 6. Round-12 planned falsifiable targets and deciding commands

From `SCORECARD.md:163-182`:

- [ ] **(a) Full powered ladder:** same 64 problems across A-INC/A-CKPT4710/A-CKPT710/A-CKPT10/A-MONO; decide with `python3 grader.py` (record census/identity) plus `grep '^E[1-3] \|^VERDICT R1\|^VERDICT R2' corpus/evidence/round12-ladder/analysis_r12.md` and the preregistered paired/Page tests in those exact stored lines.
- [ ] **(b) Per-problem forecasts:** per-problem probabilities scored over 64 problems; decide with `grep '^E6 \|^VERDICT R5' corpus/evidence/round12-ladder/analysis_r12.md` and `python3 grader.py` (the gate pins Brier, BSS, slope, intercept, reliability lines).
- [ ] **(c) Transport family and prior art:** T-DENSE/T-SPARSE second task family plus fetched URLs; decide with `grep '^E5 \|^VERDICT R4' corpus/evidence/round12-ladder/analysis_r12.md`, `grep -nE '^https?://' corpus/evidence/round12-fleet/r12-prior-art*.md`, and `python3 grader.py`.
- [ ] **(d) Same-round grader extension:** extended r12 tree and selftests; decide with `python3 grader.py` (exit 0, zero mismatches, extended check count) and `python3 grader.py --selftest` (S0–S6 all PASS).

## Defect table

| id | pointer | expected | observed | classification |
|---|---|---|---|---|
| — | none | no new baseline defect | all actionable repo checks pass; known host absence documented above | — |

BASELINE: GREEN
