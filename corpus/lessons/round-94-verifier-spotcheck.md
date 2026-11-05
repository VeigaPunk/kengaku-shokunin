author: hyaku closure (non-author integrator, @m_zfl)

# Kengaku round 94 — non-author verifier spot-check

Reviewed lane tip: `a618227e4c4d09a04c1f613fc5e5cf9f298a12ef` (BASE `0cbb927914e07818e1aaee7e72d8b3c90a2d21c2`; P0 `bdcb1ec0`; P1 `997a6fe5`; P2 `74b3d2a1`; freeze F `844c504e5147ce767a146af98e4d9b2cacb4258d`; measured tip T = C `90c7677f0ba95d0930d93bda6a14aa50605ebe2e`; receipts `242b3669`; wave `d04e6664`). Report: `.ufo/reports/round-94/kengaku.md` (fleet commit `5aa2e0cb26b4f80e446f6546a80c9c888abcc1c9`, author `kengaku-shokunin <kengaku@shokunin.local>`, 2026-11-05 19:32:22 -0300). Driver digest (`.ufo/watchdog.log`, copied 2026-11-05): `2026-11-05T18:47:18-03:00 launch kengaku round=94 pgid=1548917 driver=hyaku-inline attempt=1`; `2026-11-05T19:32:50-03:00 complete kengaku round=94; hyaku-inline attempt=1`.

Method. Plain measurements over committed bytes (`git show | sha256sum`, `git log`, `git rev-list --full-history`, `git merge-base --is-ancestor`, a Python/`json` read of the ledger at three revisions, `grep`), the census CLI, and live re-fetches of five upstream files. The lane's counters (`round94_c1_replay.py`, `round94_c2_counter.py`), the freeze-integrity gate v2 and its battery were **not executed** by this integrator (PROTOCOL §Gate standard, "Closure consequence"); their committed receipts under `.ufo/waves/round-94/L1/` were read and graded evidence-verified.

## 1. Step-1 conformance

| check | command (observed) | result |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-94/kengaku.md` → `kengaku-shokunin 5aa2e0cb…` | pass |
| `SHONEN` heading, one line per box | report `## SHONEN` with 4 `[~]` lines; `grep -c '^- \[' SHONEN.md` → 4 | pass |
| cited commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for 0cbb9279, bdcb1ec0, 997a6fe5, 74b3d2a1, 844c504e, 90c7677f, 242b3669, d04e6664, a618227e → all ok; all seven round commits authored `kengaku-shokunin` | pass |
| lane pushed, clean | `jj-lane.sh state` → `branch=master local=remote=a618227e… ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` → empty; `ls-remote origin refs/heads/master` → `a618227e…` | pass |
| report filed after its commits | lane tip committed 19:31:08, report 19:32:22, completion line 19:32:50 | pass |
| prompt carries template contract | `.ufo/prompts/kengaku-round-94.md` (fleet `b63c6b29`, 896 lines, dispatch-evidence commit 18:46:23 — same inline-driver pattern as round 93's `135bb880`): §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract (SHONEN), §5 commit scope, §6 hyaku addendum, §7 scratch | pass |
| marker? | real report, 8 lane commits with checkable work | not a marker → status `ok` |

Round-93 routed defects: #1 registry row present (`SKILL.md:698` under `## Gate/probe registry` at `:592`, fields name/gate/entry/verdict map 0·1·2/self-test spelling "in-process battery, no flag"/pinned path/write scope/owner); #2 capability row in `## Capabilities` (`SCORECARD.md:575`, heading `:553`); #3/#4 closed by gate v2 (below); #5 L7 now compares the member set (`controls/c1-forgery-member-swap.txt`: `set_added=[path-tracing, write-compressor] set_removed=[circuit-fibsqrt]`, rc 1); #6 SELFTEST echoed (`c2-tip.txt`: `W3 echo SELFTEST cases=15 ok=15` ×2); #7 carried (claims file "Not claimed").

Conformance defects (status-neutral, routed in §6): (a) the anchor gate `plans/anchor_line_check.py` was red at T (`live=1`, S299 word count) and the L1 committed SOURCES rows without running it (lesson M1) — repaired after T in `a618227e` (`anchorline-end.txt`: `live=0 cells=0` rc 0); (b) legacy `plans/round79_c1_population_ledger.py --rev` gains one `RECEIPT-UNTRACKED write-compressor` (receipt under key `evidence`, gate reads `receipt`) — same kind as round 93, disclosed in `SCORECARD.md:4367`; (c) three dead wave seats (ScoutSources, ReviewerC1, ReviewerC2) not replaced (`w1-results.json`); (d) W-8 dry-run-1 probe bytes `6c820857…` exist in no commit.

## 2. Claims — re-derivation

### R94-C1 — coverage (twelfth offline replay, `write-compressor`)

| item | command | observed | reported | match |
|---|---|---|---|---|
| ledger executed | `git show <rev>:plans/grader-population-ledger.json` → count `members[*].status=="executed"` | BASE 37 of 88 → T 38 of 88 → tip 38 of 88 | 37 → 38 of 88 | yes |
| executed set | set difference T − BASE / BASE − T | `{write-compressor}` / `{}`; tip set = T set | BASE ∪ {write-compressor} | yes |
| class cells (executed/total) | group over `members[*].classes` | file-artifact 28/76→29/76; stdout-inspection 12/29→13/29; subprocess-exec 14/45→15/45; all other cells unchanged | same | yes |
| ledger diff | `git diff --numstat 0cbb9279 a618227e -- plans/grader-population-ledger.json`; `git log` on it | `4 3`, one commit `90c7677f`; member now `status executed, round 94, reason replayed`, receipt pointer added | one-member flip | yes |
| receipt | `cat corpus/evidence/round94/compressor-probe.txt` | 8 `CASE` lines all `ok=True`, `mismatches 0`; `TOOL_SHA 3e1e1764…`, `CASE_TABLE_SHA e3c0c0ea…` equal the F table; `LANE_TIP 844c504e` (F) | 8/8, mismatches 0 | yes |
| capture bytes | `sha256sum` over `corpus/evidence/round94/graders/write-compressor/{tests,solution,environment}/*` | test_outputs.py `809f4860…384e2` = SUBJECT_SHA; solve.sh `01550b7d…b409` = SOLVE_SHA; original-decomp.c = environment/decomp.c `7f8d9ef6…f62a`; original-data.txt = environment/data.txt `0fc483d0…4fa4e` | same | yes |
| upstream bytes (live) | `curl -w '%{http_code}'` from `raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/write-compressor/` | test_outputs.py 200/2427 B/`809f4860…`; solve.sh 200/24841 B/`01550b7d…`; original-data.txt 200/4868 B/`0fc483d0…` — byte-identical to the capture | same | yes |
| counter verdict at T | committed `.ufo/waves/round-94/L1/c1-tip.txt` | `LEGS L1..L9=pass`, `TARGET executed_rows=38 member=write-compressor located=1 executed=1 cases=8 legs=32 mismatches=0 defects=0`, `PREDICATE R94-C1 pass`, `rc=0` | same | evidence-verified |
| controls | `controls/c1-base.txt`, `c1-at-P1.txt`, `c1-forgery-ledger-only.txt`, `c1-forgery-member-swap.txt`, `c1-sandbox-red.txt` | fail rc 1 ×4 (ledger-only: only L7 passes; swap: L7 fails on set); rc 2 (could-not-evaluate) | same | evidence-verified |

Verdict: **verifies, narrowed** to "at the grader's pinned `gcc -o decomp2 decomp.c` compile on this host" (W-7: `-O3` flips 3 of 8 vectors; the captured decoder prints an unterminated stack buffer, `decomp.c:75`). Re-measured: ledger count/set/cells, receipt, capture and upstream bytes; evidence-verified: counter legs/rc and controls.

### R94-C2 — calibration (known false gates passing the freeze-integrity counter, 5 → 0)

| item | command | observed | reported | match |
|---|---|---|---|---|
| frozen table holds at F, T and tip | for each row of the single ` ```frozen-instruments ` block (`grep -c` → 1): `git show <rev>:<path> \| sha256sum` | 11/11 at 844c504e, 90c7677f and a618227e | W4 summary=(11, 11, 0) | yes |
| no tabled instrument touched after F | `git log F..a618227e -- <11 paths> plans/round-94-claims.md`; `git log --full-history F..a618227e -- <paths>`; `git rev-list --merges 0cbb9279..a618227e` | 0; 0; 0 merges | touched=0 ×11 | yes |
| nor between P1 and F (controls ran frozen bytes) | `git log 997a6fe5..844c504e -- <11 paths>` | empty | — | yes |
| W1 round-93 history | round-93 table at `d8d0a4b8` vs `7b8719f3`, `sha256sum` + `git rev-list --full-history … \| wc -l` | 9/9 same, touched=0 | `W1b r93 summary=(9, 9, 0)` | yes |
| W1 round-92 history | committed `c2-tip.txt` | `W1a r92 rc=1 summary=(4, 1, 3) intact=['plans/round92_c1_replay.py']` (re-derived by plain git in the round-93 closure) | same | evidence-verified |
| gate v2 closes the three round-93 property gaps | `grep -n` in `plans/round94_freeze_integrity.py` | `:131` `rev-list --full-history`; `:96` `blocks={blocks}, exactly one allowed`; `:102` `duplicate table paths` (all CouldNotEvaluate) | TREESAME / second block / duplicate row | yes |
| BEFORE: frozen round-93 counter over the 5 known false gates | committed `controls/before-r93-counter-{x-head-not-rev,x-diff-rev-minus-1,x-table-at-rev,m06-cne-exit0-pass,m13-table-read-at-rev}.txt` | each `TARGET legs_passed=4 of 4`, `PREDICATE R93-C2 pass`, `rc=0` → **5 pass** | 5 | evidence-verified |
| AFTER: round-94 counter over the same 5 | committed `controls/c2-false-*.txt` | each `TARGET legs_passed=1 of 5`, `PREDICATE R94-C2 fail`, `rc=1` → **0 pass** (README: each designated fixture RED) | 0 | evidence-verified |
| counter verdict at T | committed `L1/c2-tip.txt` | W1 pass, `W2 pass fixtures=12 ok=12`, W3 pass (SELFTEST 15/15 echoed ×2), `W4 pass freeze=844c504e5147 rc=0 summary=(11, 11, 0)`, `W5 pass mutants=7 killed=7` (null 12/12), `TARGET legs_passed=5 of 5`, `PREDICATE R94-C2 pass`, `rc=0` | same | evidence-verified |
| do-nothing control | `controls/c2-base.txt` | `legs_passed=0 of 5`, rc 1 | same | evidence-verified |

Ruling on the critic's dissent (W-1, "does not verify as calibration: confounded and in-sample"). The frozen claim names its measure exactly — the five false gates round 93 recorded — and declares it in-sample at F (`plans/round-94-claims.md:79-89`); the predicate passes at T on frozen bytes, and the measure moved 5 → 0 on committed receipts. The confound is real (each false gate is also red on v2-only fixtures and W3), but the claim's calibration content is narrower and holds: the round-93 admitted capability row stated three properties its gate did not have, and v2 now has them in code (re-read above) with each attack re-made as a CLI-path mutant of v2 itself and killed at its designated fixture (K5–K7). The wave's ≥9 new false gates passing 5/5 (W-2, W-3) bound the counter's generality; none flips T (0 merges, renames, deletes in the W1/W4 windows; real battery 15/15). Verdict: **verifies, narrowed** to "5 → 0 over the recorded set; general discrimination not established" — the lane states the same scope (lesson "Honest limits", M2).

### Harm check

`git diff --numstat 0cbb9279 a618227e -- SCORECARD.md SKILL.md LOG.md corpus/QUALITY.md corpus/SOURCES.md PROVINCE.md SHONEN.md` → SCORECARD +58/−0, LOG +42/−0, QUALITY +5/−0, SOURCES +6/−0, SKILL +1/−0, PROVINCE/SHONEN untouched; no axis score line changed in the SCORECARD diff (novelty 8, depth 10, operability 10, freshness 10, adjacency 9; coverage held at L0 cap 7; calibration held at ceiling 10). Whole-round diff: 316 files, +28764/−3 (the −3 are the ledger member's old fields). Spot reads: `corpus/QUALITY.md:1390-1391` (Q75 grounded in M2, Q76 in M1), `corpus/lessons/round-94.md` (Gate, M1–M4, W-1…W-13). No owned axis harmed.

## 3. Per-axis verdicts (this closure)

| axis | verdict | basis |
|---|---|---|
| coverage | improved | ledger executed 37→38 of 88, file-artifact 28→29/76, stdout-inspection 12→13/29, subprocess-exec 14→15/45 (re-measured); score held at L0 cap 7 |
| calibration | improved | known false gates passing the lane's counter 5→0 on committed receipts (evidence-verified); the round-93 capability row's three overstated properties now hold in v2 (re-read); scope narrowed to the recorded set; score held at ceiling 10 |
| novelty | unchanged | no claim; score 8 held |
| depth | unchanged | no claim; score 10 held |
| operability | unchanged | no claim; score 10 held |
| freshness | unchanged | no claim; score 10 held |
| adjacency | unchanged | no claim; score 9 held |

## 4. Discernment spot-check (LEARNING.md — from outside)

Re-fetched 2026-11-05 from `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/write-compressor/…` with `curl -w '%{http_code}'`.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S297 `tests/test_outputs.py` | admit (A) | HTTP 200, 2427 B, sha256 `809f4860…384e2`; `:15` = `subprocess.run(["gcc", "-o", "decomp2", "decomp.c"], check=True)`; `:63` = `max_size_bytes = 2500`; `def test_` at :18, :25, :60 | agree | bytes identical to capture and receipt SUBJECT_SHA; quote and line hold; the plain `gcc` build (no `-O`) is exactly what scopes C1 |
| S299 `tests/original-data.txt` | admit (A) | HTTP 200, 4868 B, sha256 `0fc483d0…4fa4e`; line 1 begins `In information theory, data compression, source coding,[1] or bit-rate reduction` | agree | identical to capture; the corrected "(10 words)" is right (10 whitespace tokens) |
| S300 `solution/solve.sh` | admit (A) | HTTP 200, 24841 B, sha256 `01550b7d…b409`; `:4` = `cat <<'EOF' > main.rs`; `:732` = `rustc main.rs -o main` | agree | identical to capture and SOLVE_SHA; it is the replay's positive control |
| S301 `tests/test.sh` | reject | HTTP 200, 608 B, sha256 `4770437e…c334`; `:3` `# Install curl`, `:5` `apt-get install -y curl`, `:8` `curl -LsSf https://astral.sh/uv/0.9.5/install.sh \| sh` | agree | network installs are incompatible with the offline replay; sha equals S294's wrapper (round-93 closure re-fetch), so it carries no member-specific grader semantics |
| S302 `environment/Dockerfile` | reject | HTTP 200, 283 B, sha256 `9a583d29…93b`; `:5` `RUN apt-get update && apt-get install -y gcc rustc bc`; `:8` `RUN gcc -O3 decomp.c -o /app/decomp` | agree | a docker build with network apt is not a replay input; keeping it as the pointer for the `-O3` divergence is correct, since the grader rebuilds `decomp2` without `-O` |

SOURCES rows re-opened: S297 (`corpus/SOURCES.md:313`) — quote is 5 whitespace tokens (≤25), located at `:15` in the live bytes; S299 (`:315`) — 10 tokens, at line 1; S302 (`:318`) — 6 tokens, at `:8`. Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok`, exit 0 (30 pre-existing W04 duplicate-url warnings); rows 288 at BASE → 294 at tip (`grep -c '^| \?S[0-9]\+ '`).

Result: 3 admits + 2 rejects sampled, 5/5 agree.

## 5. Trend verdicts (this closure)

- **expansion: improved** — population frontier 37→38 of 88 with three class-cell moves (re-measured), 4 admitted tier-A rows (S297–S300) on a member the corpus did not hold, and new member findings (C04/C06/C08, the `-O3` divergence).
- **quality: unchanged** — no admitted `knowledge/` entry was superseded or re-verified; the S299 correction fixed a row written this same round.
- **discernment: improved** — outside spot-check agrees on admits and rejects (5/5); two rejects carry flip conditions; Q75 and Q76 are new criteria grounded in mistakes M2 and M1; the non-author critic's dissent on C2 stands beside the self-verdict and is ruled on here with reasons.

## 6. Routed defects the lane must fix next round (round 95)

1. M1/Q76: run `plans/anchor_line_check.py` before any commit carrying SOURCES rows (was red at T); compute anchor word counts.
2. W-2/W-3/M2: commit the ≥9 wave-built false gates (ExecC2Rerun F1–F7, CriticClaims C2-F1 stubbed battery, MutTesterGate M20 concealed red battery) as controls under a new frozen predicate; W3 must not trust a printed `SELFTEST` line alone.
3. W-4: replace refs and non-three-backtick fences (CriticClaims C2-F2/C2-F3) — refuse or read them.
4. W-5/W-6: surviving gate mutants (9 of 20) and C1 counter mutants (m03+m04, m10, m11); add receipt-side positive-direction controls not based on P1.
5. Legacy `plans/round79_c1_population_ledger.py`: `receipt` vs `evidence` key (`RECEIPT-UNTRACKED` ×2 now) — fix the gate or the ledger key.
6. W-8: commit or stop citing dry-run-1 probe bytes `6c820857…`; W-10 reject `--work` inside the lane; SP-2 pin `LANG` for C08.
7. Carried from round 92: override vacuity `plans/round92_burndown.py:306-329`, marker skip `:445`/`:558`, unpinned round-92 counters, `cost_model_for_tests.py` guard.

Operator note: the four SHONEN boxes carry committed evidence pointers a non-author can check (SKILL registry row `:698`, LOG `:3565` end-to-end replay with receipt, one-command predicates in `plans/round-94-claims.md`, ConnectorOverlap for PROVINCE); promotion is operator-owned.
