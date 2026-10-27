# kengaku-shokunin corpus

Domain memory for LLM/model research & evaluation. Per `../CORPUS.md`:
`knowledge/` entries cite a source; `lessons/` entries cite round + evidence;
every entry is falsifiable or marked opinion.

## Source availability — round-13 re-dispatch, 2026-10-15

The wiki, both benchmark locations, Bailian directory, routing ledger,
former service unit/template, and pid-1299 cmdline are unavailable at the
exact paths in `evidence/round13-coverage/surface-receipt.json`; the former
`:34113/health` endpoint refused connection. These are historical sources,
not current runnable dependencies. Retained digests are not original-source
bytes; historical hashes do not establish present availability or identity.
Public URLs were not re-fetched in this continuation.

Current offline entry points: `python3 grader.py` replays retained response
bytes; `python3 evidence/round13-coverage/coverage_census.py` (from this
directory) inventories documented source status and bidirectional index
membership. Neither command restores a source or measures a live model.
Historical experiment scripts retain their capture-time host defaults and
are not current entry points. The source-status census covers the twelve
candidates fixed in the receipt, not the wider round-16 citation audit.

## What's here

| Entry | Covers | Primary source |
|---|---|---|
| `knowledge/benchmark-selection.md` | Task-class → benchmark mapping; contamination status; minimal stack | Historical-unavailable: `llm-wiki/wiki/ai/agents-and-engineering/benchmark-shortlist-for-godspeed-research.md` |
| `knowledge/godspeed-eval-findings.md` | Iteration-2 empirical results: K2 split, variant multiplier, calibration asymmetry, cost | Historical-unavailable: `llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-2.md` |
| `knowledge/telemetry-run-design.md` | Per-run telemetry fields, artifact set, phase gates, run-count floor | Historical-unavailable: `llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-3-alpha-shittycodex.md` |
| `knowledge/local-model-index.md` | Bailian structured model index layout and field semantics | Historical-unavailable: `~/.bailian/skills/bailian-docs-llm-wiki/models/index.md`, `models.jsonl` |
| `knowledge/local-bench-arena.md` | Historical 33-task battery: schema, two-model results, complementarity split | Historical-unavailable: `~/archive/bench-arena/` CSVs (then `~/bench-arena`), analyzed 2026-09-28 |
| `knowledge/ledger-route-telemetry.md` | Historical lane-routing corpus: event taxonomy, reroute signatures, model×lane counts | Historical-unavailable: `~/Projects/bounties/ledger/telemetry.jsonl` (7,218-line capture), profiled 2026-09-28 |
| `knowledge/bench-arena-fresh-run.md` | Round-4 authored run: endpoint drift finding, 4-task reproduction slice, prediction error | Historical-unavailable: `~/archive/bench-arena/` (then `~/bench-arena`) + `127.0.0.1:34113` run 2026-09-28 |
| `knowledge/eval-theory-notes.md` | Digest: yao-second-half, creative-benchmark, trueskill-sorting, rlhf, bitter-lesson | Historical-unavailable: `llm-wiki/wiki/karpathy/*` + `ai/{foundations,alignment-and-training}/`, read 2026-09-28 |
| `knowledge/gemini-benchmark-suite.md` | Four-signal godspeed test suite: reframe traps, variant multiplication, discovery widening, calibration meta-test | Historical-unavailable: `llm-wiki/.../gemini-3.1-pro-godspeed-{benchmarks,test-battery}.md`, read 2026-09-28 |
| `knowledge/bailian-cli-telemetry.md` | Client-side CLI telemetry: 4,274 records, quota-vs-auth failure split, poll-verb rule | Historical-unavailable: `~/.bailian/telemetry.jsonl`, profiled 2026-09-28 |
| `knowledge/bench-arena-round5-battery.md` | Full 33-task re-run under fixed endpoint: 20/33, 8 status deltas (4 P→F, 3 F→P, 1 F→HARNESS_DEFECT), truncation class, sha-identical set | `/tmp/bench-r5/` run (ephemeral; decisive CSV-joined numbers pasted in-entry) vs `127.0.0.1:34113`, graded 2026-09-28 |
| `knowledge/open-model-catalogs.md` | Hugging Face 50 returned records and first-record schema delta; OpenRouter 10-record sample plus API-reported `total_count=467`; provider fields, query constraints, and open-weight twins | S101/S102; initial probes 2026-09-28 and raw-byte re-probe 2026-10-25 (`corpus/evidence/round33/catalogs/`) |
| `knowledge/bench-arena-round6-stability.md` | Flip-set stability probe: n=3 per task → 5/8 scaffold-determined, 2/8 noise, 06 strategy-bound | `/tmp/bench-r6/` 33-run battery vs `127.0.0.1:34113`, graded 2026-09-28 |
| `knowledge/bench-arena-task27-timeout-anatomy.md` | `test_rc=124` root cause: `_active` hidden contract → thread-exception deadlock; r5 sol also semantically broken | instrumented `test.sh` + faulthandler probe, 2026-09-28 |
| `knowledge/bench-arena-round7-scaffold-ablation.md` | Scaffold-delta ablation: verbatim opencode wire capture + component ablation → 1/5 true scaffold flips (13), tools-without-system trap, `enable_thinking` no-op | `/tmp/bench-r7/` proxy capture + 65-call graded battery, 2026-09-28 |
| `knowledge/eval-design-digest-3.md` | Scaling retrospective (construct-validity gap, Goodhart root, Tetlock scoring) + ReAct protocol (failure-class table, composition rule) | Historical-unavailable: `wiki/ai/scaling-and-forecasting/` + `agents-and-engineering/papers/react-reasoning-acting.md`, read 2026-09-28 |
| `knowledge/bench-arena-round7-noise-n25.md` | Noise tasks at n=25: 09 PASS-tilted 0.68 / 20 FAIL-tilted 0.32; draws non-iid (lag-1 +0.26/+0.32, burst-state coupling) | `/tmp/bench-r7-l2-executor/` n=25 probe, graded 2026-09-28 |
| `knowledge/eval-design-digest-2.md` | Second digest: sampling-proves-presence, reference-class, autonomy slider, spec-ability tiers | Historical-unavailable: wiki files swept+read 2026-09-28; original count correction retained in-entry |
| `knowledge/bench-arena-round8-horizon.md` | Round-8 planning-horizon probe **analyzed**: A-ladder INC 7/10 > CKPT 1/10 ≈ MONO 0/10 (9/10 convention-tolerant), MOV-zero failure class (15/19), B manipulation non-binding (2/8 well-formed, corrupt ≈ clean p=0.25, hint null), C vacuous-rule over-repair (0/4 strict vs conflict 4/4, norule 4/4), 16-defect fix-landing audit (9 landed / 5 partial / 2 not), claim triage (1 blocked) | `corpus/evidence/round8-horizon/` (78/78 jobs, 268 records, md5 `df154cb5…`), analyzed 2026-09-28 |
| `knowledge/bench-arena-round9-replication.md` | Pre-registered replication on fresh seeds + new checkpoint-dose cell: INC 4/8 > CKPT4710 2/8 = CKPT710 2/8 > MONO 0/8; predictions hashed before the first request and scored (2/4 cell hits, MAE 0.094, 4/4 directional falsifiers unfired); pre-registered decision rule → **indeterminate**; ack leakage 16/48 + 8/56 | `corpus/evidence/round9-replication/` (284 records, `predictions-r9.sha256.repo`), run 2026-09-28 |
| `knowledge/eval-prior-art-calibration.md` | Novelty pricing of the 4 local findings against fetched public primaries: 3 known/incremental, 1 a direct replication (llama.cpp #7052); surviving novelty is instrument-level (emission-granularity ablation, vacuous-rule triple control); sub-3-bit scope limit | 40+ fetched URLs → `corpus/evidence/round9-fleet/prior-art.md`, 2026-09-28 |
| `knowledge/bench-arena-round11-power.md` | Powered preregistered rerun (n=64, MDE d=0.35): emission-granularity severity dose **ESTABLISHED** — paired diff +0.352 (t=+3.431, p=0.0011, CI [+0.147,+0.556], sign 26/7/31 p=0.0013); passes 29/64 vs 21/64 (McNemar p=0.0963, no pass-rate dose); Brier 0.153; C1–C4 prior-art verdicts | `corpus/evidence/round11-power/` (1473 records, bundle `prereg-bundle.sha256`, verdict in `analysis_r11.md`), run 2026-09-28 |
| `knowledge/bench-arena-round12-ladder.md` | Powered four-point emission-density ladder + batching/emission dissociation + second-family transport + 416 per-problem forecasts: `LADDER ESTABLISHED`, `DISSOCIATION ESTABLISHED`, `TRANSPORT DIRECTIONAL`, Brier `0.1288` / BSS `+0.0447` | `corpus/evidence/round12-ladder/` (4,114 records, hashed preregistration bundle, 733-check gate), run 2026-09-29 |
| `knowledge/kimi-model-routing-round18.md` | Round-18 kimi model-routing digest: 17-model n=2 TTFT/TPS/pass battery + M6 opencode-go row; defects (token-plan key-2/3 quota dead, dead client fields, unclamped global effort, reasoning_key DEF-9/10, 42 of 143 entries on unservable lanes); 13-entry table outcome (opencode-go = deepseek-v4.1-flash only, zai→devin glm policy, codex fast-mode no-go) | Parent repo `research/round-18-kimi-model-routing/` merges `4738fee`+`7e2c473`+`c2174a5`+`db82042`+`bd0c690`+`fbae972`; local index `corpus/evidence/round18-kimi-routing/README.md` |
| `knowledge/probe-battery-r19.md` | Scored close-out of the standing battery's first run: 9-probe grid (23 binary + 7 numeric), freeze-1 superseded BR-1 / freeze-2 `e1a86777…a00a1`, §10 completion closes the grid 9/9 | `plans/probe-battery-r19.md` (FROZEN ×2) + 19 receipts `evidence/probe-r19-*.log`, scored 2026-10-16 |
| `knowledge/attrib-prior-art-r21.md` | Round-21 prior-art pricing of blind cascade-leg attribution (claim N1) against fetched arXiv primaries (9/9 HTTP 200) | fetched public primaries receipt in-entry + `knowledge/probe-battery-r19.md` anchors, 2026-10-16 |
| `knowledge/attrib-r21.md` | Blind cascade-leg attribution instrument: design, scored results, limits — frozen feature table vs floating probe code, ≥20 blind trials/shim, GT-after-trials | `plans/attrib-r21-frozen.md` + `plans/attrib_probe.py` + `evidence/attrib-r21-*.log` (4 receipts), 2026-10-16 |
| `knowledge/contamination-detection-and-transparency.md` | Contamination tiers and detector families: detector-negative ≠ uncontaminated; transparency record of detector access and scope | S001, S002, S004 (S003 rejected) — `corpus/SOURCES.md` contract-v1 rows, round 24 |
| `knowledge/llm-judge-calibration.md` | Judge scoring bias vs calibrated accuracy: sensitivity/specificity correction with test + calibration-sample uncertainty; rubric/position perturbation audits | S009–S012 — `corpus/SOURCES.md` rows, round 24 |
| `knowledge/benchmark-saturation-and-lifecycle.md` | Saturation as loss of top-model discrimination near an empirical ceiling, not a high score; lifecycle/retirement signals and construct-validity pairing | S007, S008 — `corpus/SOURCES.md` rows, round 24 |
| `knowledge/agent-time-horizon-and-task-validity.md` | METR human-duration time horizon (task difficulty at a stated success probability, not wall-clock or job automation) + coding-benchmark task/test validity audits | S013, S014, S005, S006 — `corpus/SOURCES.md` rows, round 24 |
| `knowledge/paired-eval-uncertainty-reporting.md` | Reporting recipe for shared-item evals: paired differences, MDE/resolution, clustering, multiplicity, adaptive-selection inference | S015–S019 — `corpus/SOURCES.md` rows, round 24 |
| `knowledge/attribution-interval-calibration.md` | Exact CP95 re-verdict of the r21–r23 attribution receipts: overall PASS holds on 4 unique samples (92/92), r22 TARGET hyper 10/10 PASS → INDETERMINATE, two 0/0 FAILs → UNTESTED; per-leg recall/specificity; Rogan–Gladen share bounds | S027–S030, S033, S034, S011; own-work S036/S037; `python3 plans/attrib_calibration.py --summary` |
| `knowledge/grader-perturbation-audit.md` | Frozen-response grader audit: 15168 MP/MC comparisons, D1 policy capture separate; pooled PASS does not erase MULTI flips or pid-composite uncertainty | S044–S046, S048; `plans/grader_perturb.py`; independent oracle and round-26 Gate |
| `knowledge/extraction-policy-comparison.md` | Fixed-response E0–E8 parser comparison:15712 paired verdicts,1089 events; MULTI14/31 and instruction-contract limits; no method-novelty or future-iid credit | S049,S051–S059; `plans/parser_policy_compare.py`; round-27 Gate/returned complete reread |
| `knowledge/benchmark-task-validity-checklist.md` | Ten-axis task-validity checklist read from four maintainers' own artefacts (canary, oracle/nop, cheat trials, grader isolation, declared task fields, dated release gate); counts re-derived, not copied; not task validity, contamination measurement or model performance | S077-S080, S090 (`corpus/SOURCES.md` rows, opened 2026-10-25); `plans/round-29-attempt2-claims.md`; round-29 attempt-2 Gate |
| `knowledge/contamination-transparency-card.md` | The contamination transparency card as an **amendment** to the tabulated card designs: release-side R1-R5 and score-side S1-S2 fields mapped into the union table's columns, plus the CG1-CG8 answerability gate and each detector's stated blind spot; not a fourth card design, not a contamination measurement | S081–S086 (`corpus/SOURCES.md` rows, opened 2026-10-25); `corpus/knowledge/contamination-detection-and-transparency.md`; round-30 Gate |
| `knowledge/benchmark-verifier-execution-model.md` | Where a benchmark's verifier actually runs (Harbor's per-task `environment_mode` resolution: shared by default) and what it restores before grading (stale rewards deleted, `/tests` re-uploaded unless the verifier image owns it), plus SWE-bench Pro V2's own git-based test-space reset and the log-scan grader that reads its PASSED set | S092 (Harbor @ 6099b8cf), S093 (SWE-bench Pro V2 @ 66f92766), S100 (terminal-bench-2 @ 2fd12b88) |
| `knowledge/benchmark-grader-semantics.md` | Toolathlon's ab-testing grader is a deterministic state comparison (record.csv vs expected_ratio.csv at the executed 0.05% tolerance; its log-bucket check mixes fail-open exceptions with fail-closed credential absence) and the LLM-as-judge survey frame: meta-evaluation is its own part | S103 (Toolathlon @ 9be8d8fe), S104 (arXiv 2412.05579v2); S093 restated from the verifier-execution entry |
| `knowledge/tb2-protein-assembly-grader.md` | One Terminal-Bench 2.0 task grader read and executed: `protein-assembly`'s `test_gblock` scores a binary reward from literal expected subproteins, order, FLAG/SNAP boundaries, `[GS]+` linkers of 5–20 residues and 50-nt GC windows, never reading its reference inputs; an 18-case offline probe maps instruction bullets to the assertion that enforces them (`cases=18 observed_pass=5 observed_fail=13 mismatches=0`) | S105, S106, S107 (terminal-bench-2 @ 2fd12b88) |
| `knowledge/tb2-regex-log-grader.md` | A second Terminal-Bench 2.0 task grader read and executed: `regex-log`'s single test asserts exact equality of `re.findall(pattern, log_text, re.MULTILINE)` against a literal nine-date list over a fixed 25-line in-test log, so the graded artefact is an agent-authored regex file (`/app/regex.txt`, read, stripped, compiled) and no reference inputs exist; a 24-case offline probe runs the captured test function and maps instruction bullets to the assertions that enforce them (`cases=24 observed_pass=8 observed_fail=16 mismatches=0`) | S108, S109, S110 (terminal-bench-2 @ 2fd12b88) |
| `knowledge/tb2-git-webserver-grader.md` | A third Terminal-Bench 2.0 task grader read and executed: `configure-git-webserver`'s whole score is one pytest function asserting that the stdout of a shell helper contains the substring `TEST PASSED` — so a static file served on port 8080 with no git repository, hook or push passes, and a body containing only that token passes while the helper itself prints `TEST FAILED`; status and body come from two separate requests and trailing newlines are the only whitespace forgiven (`cases=22 observed_pass=9 observed_fail=13 mismatches=0`) | S111, S112, S113 (terminal-bench-2 @ 2fd12b88); S114 (TB2.1 issue #133, prior report) |
| `knowledge/tb2-build-pmars-grader.md` | A fourth Terminal-Bench 2.0 task grader read and executed: `build-pmars` scores four pytest functions — binary presence, two debugger address lines, a start-anchored `Results:` match, an `ldd` string scan and a one-level `/app/pmars-*` tree — so a canned 21-line C program plus an empty `debian/` directory and a zero-byte `src/dummy.c` passes all four tests, a `dlopen()`ed libX11 evades the X11 scan, exit 3 with output is ignored, and `Results: 12 34 78 forged` passes; no instruction line is fully enforced (`cases=22 observed_pass=7 observed_fail=15 mismatches=0`) | S115, S116 (terminal-bench-2 @ 2fd12b88) |
| `knowledge/tb2-git-leak-recovery-grader.md` | A fifth Terminal-Bench 2.0 task grader read and executed: `git-leak-recovery` scores five pytest functions — a stripped literal at `/app/secret.txt`, two `git log --all` searches, an init-message substring, `git fsck --lost-found` plus `cat-file -p` over each dangling object, and a pinned non-dot work-tree checksum — so the untouched initial state passes 4 of 5, writing the literal alone passes 5/5 with the secret still in the object store, a ref to a blob, an annotated tag message, a stash, a dot file and `.git/config` all pass 5/5 while a dangling blob or commit, a branch-reachable secret commit, a note, an untracked file and an edited README fail, and commit-message preservation is one substring; two of the four instruction tags are enforced (`cases=25 observed_pass=13 observed_fail=12 mismatches=0`) | S117, S118 (terminal-bench-2 @ 2fd12b88) |
| `knowledge/tb2-db-wal-recovery-grader.md` | A sixth Terminal-Bench 2.0 task grader read and executed: `db-wal-recovery` scores seven pytest functions that all open only `/app/recovered.json` — existence, a non-empty list, three field types, sorted ids, eleven ids with values `150`/`250` on ids 1-2 and the names `cherry`…`mango` on ids 3-11, unique ids, and a `>5`-row floor — so 22 of the 33 `id`/`name`/`value` cells are pinned and hand-typed JSON passes 7/7 without opening the database, "Fix the WAL file" is graded only through the export, one plain read-write `sqlite3` open destroys the encrypted log so the task's own oracle then fails 2 tests, a wrong XOR key leaves the five base rows, `True` passes as an int value, float ids `1.0`…`11.0` fail only the structure test, and an extra field passes; S119, S120; probe `plans/db_wal_probe.py`, receipt `evidence/round40/db-wal-probe.txt` |
| `knowledge/tb2-constraints-scheduling-grader.md` | A seventh Terminal-Bench 2.0 task grader read and executed, and a grader class new to this lane: `constraints-scheduling`'s three pytest functions compute the verdict with a scheduling model embedded in the test file — `_hard_ok`, `_overlap` and a minute-granularity earliest-slot scan over three sha256-pinned input calendars — and read the graded ICS with regexes, not an ICS parser — so a hand-typed Wed 11:00 file passes 3/3 without reading a calendar, a decoy first `VEVENT` passes 3/3 with the attendee meeting on Friday 15:00 (published: TB2.1 PR #245), the earliest test passes slots that violate the hard constraints (`bob-start-0900-wed`, `wed-1059-overlaps-alice`: `PFP`), rewriting all three input calendars with CRLF line ends passes 3/3 although `instruction.md:17-18` says any modification fails, `DTEND` is read only by the structure test (`duration-90min`: `FPP`), and three RFC 5545-form output forms fail while CRLF output passes (`cases=25 observed_pass=6 observed_fail=19 mismatches=2`, `regrade cases=25 differ=0`) | S122, S123 (terminal-bench-2 @ 2fd12b88); TB2.1 PR #245 (prior art, to open as S124); probe `plans/constraints_probe.py`, receipt `evidence/round41/constraints-probe.txt` |
| `knowledge/tb2-circuit-fibsqrt-grader.md` | An eighth Terminal-Bench 2.0 task grader read and executed, and a grader class new to this lane: `circuit-fibsqrt` grades a **data artefact** — a gate list at `/app/gates.txt` — by compiling the task's own simulator at grading time (`gcc -O3 /tests/sim.c -o sim` in the cwd, `test_outputs.py:65-67`) and running `/app/sim N` on 28 fixed inputs (largest 48401, `:73-102`), so the whole score is existence, a `< 32000` line count and 28 printed words: a 1195-line lookup circuit covering exactly those 28 inputs passes 3/3 (`lookup-28`) while printing 0 for the instruction's own examples 208 and 20000, blank padding to 31999 lines still passes but 32000 fails only the size test, `#` comment lines, full line reversal and CRLF all pass, one trailing space per line fails, a planted executable `/app/sim` is overwritten by the grader's own compile, and a directory named `gates.txt` passes the existence test and fails the other two (`cases=16 observed_pass=7 observed_fail=9 mismatches=0`; `regrade cases=16 differ=0`); prior art for the coverage gap above 48401: S128 | S125, S126, S127, S128 (terminal-bench-2 @ 2fd12b88); probe `plans/fibsqrt_probe.py`, receipt `evidence/round42/fibsqrt-probe.txt` |
| `knowledge/tb2-feal-differential-cryptanalysis-grader.md` | A ninth Terminal-Bench 2.0 task grader read and executed, and a grader class new to this lane: `feal-differential-cryptanalysis` grades an **agent-authored Python module imported into the grader's own interpreter** — `test_outputs.py:22-23` appends `/app` then `/tests` to `sys.path`, `:24` runs `import attack` and `:25` `import feal_in_c`, `:27` calls `create_random_keys()`, `:29` `stolen = attack.attack(feal_in_c.encrypt)` and `:30` asserts `feal_in_c.get_keys()[5] == stolen` — one test function, one assertion, and the verdict is pytest's exit status (`test.sh:17-25`) — while the reference C extension the grader builds first (`:20`, `python setup.py build_ext --inplace` in `/tests`) exports the answer in that same interpreter as a 6-element list (`feal_module.c:25-51`): six of the eight observed passes never recover a key by cryptanalysis — returning `get_keys()[5]` (`cheat-import-get_keys`), an object whose `__eq__` is always True (`cheat-always-equal`), a fake `feal_in_c` installed in `sys.modules` at import (`cheat-sysmodules-shadow`), a rebound `get_keys` (`cheat-patch-get_keys`), `os._exit(0)` inside `attack()` (`cheat-exit-zero`, `exit=no-verdict-line`) and a libc replay of `srand(time(NULL))` (`cheat-clock-seed`, `host=libc-rand`, the schedule being one 16-bit seed per round key under one `srand` per process, `feal.c:56-67`) — a 45 s oracle also passes (`slow-oracle-45s`) although `instruction.md:3` asks under 30 s and `README.md:35` says the test "Confirms the attack completes within the time limit", because nothing times the call and the only bound is `task.toml:22`'s 1800 s verifier timeout; the four failures are a missing module (`nop`), a wrong value (`wrong-key`), the oracle plus one (`oracle-off-by-one`) and the oracle as a decimal string (`return-str`); `cases=12 observed_pass=8 observed_fail=4 mismatches=0`; `regrade cases=12 differ=0` | S129, S130, S131, S132, S133, S134 (terminal-bench-2 @ 2fd12b88); probe `plans/feal_probe.py`, receipt `evidence/round43/feal-probe.txt` |
| `knowledge/tb2-feal-linear-cryptanalysis-grader.md` | A tenth Terminal-Bench 2.0 task grader read and executed, and a grader class distinct from round 43's: `feal-linear-cryptanalysis` grades an **agent-written text file** — `test_outputs.py:120` reads `/app/plaintexts.txt` whole and `:121-122` assert each of 100 embedded decimal constants is a substring of it, so order, separators, padding and extra content are invisible while one missing value fails; three attack-free passes come from the public `gen.py` keys (`:12`), its hash chain (`:61-62`) and the test's own constants (`:4-103`); the executable reading is in `## Predictor` | Pinned at terminal-bench-2 `2fd12b88`: S138, S139, S140, S141, S142, S143, S144, S145, S146; captures + `SHA256SUMS` in `evidence/round44/tb2-feal-linear-cryptanalysis/` |
| `knowledge/tb2-password-recovery-grader.md` | An eleventh Terminal-Bench 2.0 task grader read and executed, and the second exemplar of the F1 constant-compare family after `feal-linear-cryptanalysis`: `password-recovery` grades an **agent-written file of guesses** — `test_outputs.py:9-10` asserts `/app/recovered_passwords.txt` exists and `:14-18` assert one embedded 23-char constant is `in` `read_text().strip().split("\n")`, so the answer must be its own line yet decoys, order and count are invisible; the constant is readable from the public test file itself and `allow_internet = true` keeps the published repo in reach; `cases=16 observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16 differ=0`; the executable reading is in `## Predictor` | Pinned at terminal-bench-2 `2fd12b88`: S149, S150, S151, S152, S153, S154, S155, S156; captures + `SHA256SUMS` in `evidence/round45/tb2-password-recovery/`; receipt `evidence/round45/password-recovery-probe.txt`; executed under `bwrap` (envelope SHA256SUMS lists the captures) |
| `lessons/round-1.md` | Path-correction, replace-don't-append, zero-width char hazard | LOG.md round 1, commit `90a5ce8` |
| `lessons/round-3.md` | Filename-judging missed on-host surfaces; complementarity vs pass-rate; NULL parsing; FAIL-latency signature | LOG.md round 3, this round's analysis |
| `lessons/round-4.md` | Endpoint-drift trap; n=1 flip on 03; FAIL-latency is subset-level not per-task | LOG.md round 4, `/tmp/bench-r4` run |
| `lessons/round-1-aggregator-audit.md` | Aggregator audit: corpus verdict, 13 re-verified claims, 3 defects (all closed round 4) | Aggregator L1 + reviewer lane, 2026-09-28 |
| `lessons/round-5.md` | Aggregate-correct ≠ model-right; truncation failure class; sha-identity = scaffold insensitivity | LOG.md round 5, `/tmp/bench-r5/` run |
| `lessons/round-7.md` | Unanimity ≠ attribution; tools-without-system trap; context mass shifts strategy; `enable_thinking` no-op | LOG.md round 7, `/tmp/bench-r7/` run |
| `lessons/round-4-aggregator-audit.md` | Aggregator audit of the round-4 delta (`a1af83c`): CONFORMANT, 0 majors / 2 minors; 21 citations independently re-executed | aggregator lane (non-author), 2026-09-28 |
| `lessons/round-5-aggregator-audit.md` | Aggregator audit of round-5 (`782dd2d`): NOT conformant, 2 majors (false 22-vs-25 file count; deleted README index row) + 3 minors; SHONEN bare-`[x]` = author attestation, regeneration owed | aggregator lane (non-author), 2026-09-28 |
| `lessons/round-8.md` | Unanalyzed run ≠ result; the lane's own prediction rule was violated with no gate; "critic accepted" ≠ "critic implemented" (2/16 fixes not landed); verify a manipulation binds; grader `ok` must be the needed conjunction; never strip fields from landed evidence; burst adjacency was maximal | LOG.md round-8 (retrospective), `corpus/evidence/round8-horizon/` |
| `lessons/round-9.md` | Pre-registered rules have three outcomes — don't launder "indeterminate"; direction replicating ≠ magnitude replicating; a control arm must be verified to be the control; point predictions can't be calibration-scored; price novelty before claiming it; integrity claims need a field-level diff, not a hash comparison; a missing contract file is a standing defect; SHONEN boxes are byte-diffed against a seed | LOG.md round-9, `corpus/evidence/round9-{replication,fleet}/` |
| `lessons/round-11.md` | Mock-smoke before ordering-sensitive runs; second-resolution ts breaks unique-first-record checks; shrinkage works on paired contrasts not levels; small-n null ≠ equivalence; Brier honesty cost; hashed bundles freeze typos; contingency rules belong inside the bundle | LOG.md round-11, `corpus/evidence/round11-{power,fleet}/` |
| `lessons/round-6-aggregator-audit.md` | Aggregator audit of the rounds 5–7 tree (`f147a27`): **NOT conformant** — 5 majors (falsified `0/12` PASS denominator; `LOG.md:9` rewritten in place; orphaned `85b22e3` citation, now dangling; 2 missing lessons index rows; `SCORECARD.md` absent while `MISSION.md` assigns an axis `AXES.md` does not define) + 7 minors; cited-hash ancestry sweep via `git merge-base --is-ancestor` | aggregator lane (non-author), 2026-09-28 — **aggregator-owned file: committed by the aggregator per `../PROTOCOL.md`; this lane writes only this index row** |
| `lessons/round-8-aggregator-box3-coldrun.md` | Aggregator non-author cold run of `SKILL.md` (SHONEN box 3): 20/20 executed commands reproduced at `0c51208` (23:31–23:33Z), incl. grader n=149 pre-extension; break points + gated steps recorded; caught `models.jsonl` cite-path break B1 and live ledger drift 7,218→7,226 minutes before the tree went absent | aggregator lane (non-author), committed by the aggregator `06cdc98` per `../PROTOCOL.md`; this lane writes only this index row |
| `lessons/round-12.md` | Ordered alternative → ordered test; measured power floors; heterogeneous forecast classes; mean-preserving probability tilts; repeatability ≠ replication; a floor is a result; pin landed bytes | LOG.md round 12, `corpus/evidence/round12-{ladder,fleet}/` |
| `lessons/round-13.md` | Storage labels are not prompt intent; schedule-derived denominators; cap-aware bounds; state fidelity and response-contract compliance are separate | LOG.md round 13, `corpus/evidence/round13-ack-state/` |
| `lessons/round-14.md` | An uncommitted round is not durable; index parity, landing-time pins, and the replay gate are closure conditions | LOG.md round 14, `corpus/evidence/round14-fleet/` |
| `lessons/round-9-aggregator-corpus-verdict.md` | Aggregator corpus-verdict lesson (rule-10 re-emitted at `f09ff1f`, canonical-form + rule-8 literal findings, routed rows); aggregator-owned file, indexed here only | aggregator lane, committed `e171cdf` |
| `lessons/round-16-recensus.md` | Hermetic replay survives host-source loss; unmarked dead paths and missing index row remain debt | LOG.md §16; the round-13 re-dispatch adds current availability annotations without rewriting this audit |
| `lessons/round-13-coverage.md` | Source availability is coverage; original-byte absence differs from retained digests; bounded index census | LOG.md round-13 re-dispatch; `evidence/round13-coverage/` |

### `evidence/round29-attempt2/` — round-29 attempt-2 adoption receipts

| File | Covers |
|---|---|
| `adoption-measured.txt` | The frozen C1 counter line plus census (`entries=1 … census=ok`, exit 0) |
| `gate-selftest.txt` | `plans/sources_adopt.py --selftest`, ten cases, exit 0 |
| `adoption-gate-run.txt` | The same tool refusing a re-append of the five landed ids (`collisions=5`, exit 3) |
| `census-before.txt` / `census-after.txt` | Fleet source census, exit 0 both ends |

### `lessons/` — round lessons and audits (index)

| Entry | Covers | Evidence |
|---|---|---|
| `lessons/2026-10-16-round19-freeze-chain.md` | The freeze is the contract: what a 32-seat preregistration battery stressed | `plans/probe-battery-r19.md` §7/§7.1, `evidence/probe-r19-*.log` (15 receipts), `plans/probe-battery-TEMPLATE.md` |
| `lessons/2026-10-16-round20-grid-closure.md` | A battery with unrun probes is an open battery: what closing the grid bought | P2/P3/P8/P9 completion receipts `evidence/probe-r19-{P2-servicetier,P3,P8-kimi-code-auth,P9-absent-port}.log` |
| `lessons/2026-10-16-round21-attribution-freeze-surface.md` | The freeze held the table and let the code float: first live-GT read of the attribution instrument | `plans/attrib-r21-frozen.md`, `plans/attrib_probe.py`, `evidence/attrib-r21-*.log` |
| `lessons/2026-10-16-round22-leg-coverage-forcing.md` | Natural coverage is weather, forced coverage is design: closing untested legs must not claim what it did not measure | `plans/attrib-r22-frozen.md`, `evidence/attrib-r22-*.log`, battery TEMPLATE P10 fold |
| `lessons/2026-10-16-round23-stream-surface.md` | The request flag is an instrument surface: what the shim's stream path changes about forcing and features | `plans/attrib-r23-frozen.md`, `evidence/attrib-r23-stream*.log` (30/30 accuracy, target clause FAIL) |
| `lessons/round-24.md` | Round-24 lesson: mistakes mined from rejected candidates + `## Gate` (admission records) | round-24 wave receipts; `plans/round-24-claims.md` |
| `lessons/round-24-verifier-spotcheck.md` | Round-24 non-author verification and spot-check (integrator-authored, not lane-owned): admit/reject agree, S023 reason disagreement → S026 + Q9/Q10 | `a42bb40`; fleet `.ufo/waves/kaika-w3/kengaku-review.md` |
| `lessons/round-25.md` | Round-25 lesson: mistakes M23–M30 (L0 filing, point-PASS survivor, stale state assertions, separability) + `## Gate` + kaika W3 F1–F14 disposition | `plans/round-25-claims.md`; `.ufo/waves/round-25/` |
| `lessons/round-25-verifier-spotcheck.md` | Outside closure: round 25 rejected-honest-stop, expansion harmed at landing; routed number drift and future-dated Gate evidence | `f11bffbf`; round-26 repair R26-E1–E4 |
| `lessons/round-26.md` | Repair-first lesson: Q13 evidence timing, frozen P3 self-assertions and grader perturbation interpretation | `plans/round-26-claims.md`; `.ufo/waves/round-26/` |
| `lessons/round-27.md` | Extraction-policy comparison, frozen P4 assertions and commit-tree/working-copy mutation survivor | `plans/round-27-claims.md`; `.ufo/waves/round-27/` |
| `lessons/round-29-source-copy-containment.md` | Non-author containment correction: a five-path absence check missed a compressed copy; bounded current-tree removal without historical purge or admission | Baseline `6a2c2df788a4fdb216dd5790f9ae6dd326169f47`; opaque archive/member identities in the lesson; appended fleet-report erratum |
| `lessons/round-29-verifier-spotcheck.md` | Non-author verification of round-29 attempt 2: C1/C2 re-measured from committed bytes, a non-author discernment sample, axis and trend verdicts, routed defects; no lane-authored file edited | `.ufo/reports/round-29/kengaku.md`; baseline `1f3b0f1e`, lane tip `2ff4b6f8` |
| `lessons/round-30.md` | Assimilation round 2 with a quote-validating gate: `contamination-transparency-card.md` admitted as the amendment round 29 demanded, `judge-calibration-thresholds.md` refused; routed-defect closure D1–D5; counter blind spots recorded unsmoothed | `plans/round-30-claims.md`; `corpus/evidence/round30/`; `.ufo/waves/round-30/` |
| `lessons/round-30-verifier-spotcheck.md` | Non-author closure spot-check of round 30's filed bytes plus its three appended errata | `.ufo/reports/round-30/kengaku.md`; baseline `363a4ebf`, tip `2dcf06c5` |
| `lessons/round-31.md` | One theme (*how a benchmark verifier runs*): `benchmark-verifier-execution-model.md` admitted re-grounded on S092/S093/S100, four packages refused; citation-bound adoption gate and its CLI exits | `plans/round-31-claims.md`; `corpus/evidence/round31/`; `.ufo/waves/round-31/` |
| `lessons/round-31-verifier-spotcheck.md` | Non-author spot-check of round 31: C1/C2 re-measured, C3 evidence-verified rather than executed | before `0883e72e`, after `87f0d32e` |
| `lessons/round-32.md` | Id-collision refusal of `benchmark-grader-semantics.md` (S094/S097/S101/S102 collide with live rows), catalog-freshness claim declared failed as measured, `catalog_probe.py` `mkdir` repair | `plans/round-32-claims.md`; `corpus/evidence/round32/` |
| `lessons/round-32-verifier-spotcheck.md` | Non-author spot-check of round 32: C1 re-measured from committed id lists and receipts, C2/C3 evidence-verified | before `f20a1097`, after `bcd2a6c0` |
| `lessons/round-33.md` | Renumbered assimilation (staged S094→S103, S097→S104) admitting `benchmark-grader-semantics.md`; catalog rows S101/S102 rejected; byte-retained catalog captures | `plans/round-33-claims.md`; `corpus/evidence/round33/` |
| `lessons/round-33-verifier-spotcheck.md` | Non-author spot-check of round 33 | before `112091c2`, after `4e6a8b1f` |
| `lessons/round-34.md` | Honest stop: C1/C2 counters not admitted (false greens in the frozen counter, mutants misaligned to checks), two quarantine rows refused, six package candidates refused or held; erratum appended round 35 | `plans/round-34-claims.md`; `.ufo/waves/round-34/build-results.json` |
| `lessons/round-34-verifier-spotcheck.md` | Non-author spot-check of round 34 | before `5022357c`, after `58a19f37` |
| `lessons/round-35.md` | One TB2 grader read and executed (`protein-assembly`, S105–S107 admitted); the four routed defects become the `defects.jsonl` ledger | `plans/round-35-claims.md`; `corpus/evidence/round35/` |
| `lessons/round-35-verifier-spotcheck.md` | Non-author closure spot-check of round 35 | before `5d0c73db`, after `e7f0decd` |
| `lessons/round-36.md` | Hardened package gate `plans/pkg_gate.py` plus the `regex-log` grader (S108–S110); Amendment 1 normalises the `mkdtemp` path in printed assertion text | `plans/round-36-claims.md`; `corpus/evidence/round36/` |
| `lessons/round-36-verifier-spotcheck.md` | Non-author closure spot-check of round 36 | before `b662a5d6`, after `0fb87f88` |
| `lessons/round-37.md` | Advertised gate classes made demonstrable (55/55 frozen mutants) and a third TB2 grader (`configure-git-webserver`, S111–S114); wave 2 finds near-variants only 23/36 killed | `plans/round-37-claims.md`; `corpus/evidence/round37/` |
| `lessons/round-37-verifier-spotcheck.md` | Non-author closure spot-check of round 37 | before `3ea9a1d9`, after `dc90676b` |
| `lessons/round-38.md` | Gate behaviours attributed 21/22 with one frozen direction mislabelled (N21) and a fourth TB2 grader (`build-pmars`, S115/S116); baseline erratum against the round-37 landing commit | `plans/round-38-claims.md`; `corpus/evidence/round38/` |
| `lessons/round-38-verifier-spotcheck.md` | Non-author closure spot-check of round 38 | before `fc1174f5`, after `1fa7af45` |
| `lessons/round-39.md` | Seven undemonstrated gate behaviours made demonstrable with witnessed directions, and a fifth TB2 grader (`git-leak-recovery`, S117/S118) | `plans/round-39-claims.md`; `corpus/evidence/round39/` |
| `lessons/round-39-verifier-spotcheck.md` | Non-author closure spot-check of round 39 | before `b2bdd425`, after `9d3aff94` |
| `lessons/round-40.md` | Three tripwire tools mutation-tested 21/21 and a sixth TB2 grader (`db-wal-recovery`, S119–S121); a pid-namespaced hostile control measures the class it closes | `plans/round-40-claims.md`; `corpus/evidence/round40/` |
| `lessons/round-40-verifier-spotcheck.md` | Non-author closure spot-check of round 40 | before `d3a6277f`, after `5b73c5e8` |
| `lessons/round-41.md` | A calibration battery that binds its own totals (48 fixtures, 23/23 mutants) and a seventh TB2 grader (`constraints-scheduling`, S122–S124); the reachability control named as a loophole | `plans/round-41-claims.md`; `corpus/evidence/round41/` |
| `lessons/round-41-verifier-spotcheck.md` | Non-author closure spot-check of round 41 | before `e50c1345`, after `e61aff6f` |
| `lessons/round-42.md` | A battery whose kills must be attributed (29 fixtures, 14/14 mutants) and an eighth TB2 grader (`circuit-fibsqrt`, S125–S128); two carried mistakes — a declared direction copied from a table, a kill credited to a fixture that did not produce it | `plans/round-42-claims.md`; `corpus/evidence/round42/` |
| `lessons/round-42-verifier-spotcheck.md` | Non-author closure spot-check of round 42 | before `d69452cf`, after `f9bbee69` |
| `lessons/round-43.md` | Nine near-variants killed with value-attributed kills and a ninth TB2 grader (`feal-differential-cryptanalysis`, S129–S137); three carried mistakes — a stale-line anchored edit, a freeze control whose own quote was one word, a counter's answer key shipped inside the counter | `plans/round-43-claims.md`; `corpus/evidence/round43/` |
| `lessons/round-43-verifier-spotcheck.md` | Non-author closure spot-check of round 43 | before `317148c4`, after `1838be94` |

Supporting corpus files:

| File | Covers |
|---|---|
| `QUALITY.md` | Admission bar for knowledge entries (Q1–Q8) + round-closure criteria appended round 24; every criterion cites the lesson that produced it |
| `SOURCES.md` | Contract-v1 registry: where the lane learns — `S###` rows with scoped tier/anchor/status/recheck and `used-by` pointers (rows S001–S019 drafted in the ART dossier) |

### `evidence/` — durable run bytes and L2 analyses

`../PROTOCOL.md`'s evidence standard rejects `/tmp` pointers at closure, so the
run artifacts are committed:

| Dir | Contents |
|---|---|
| `evidence/round8-horizon/` | `horizon.py` (349-line probe, md5 `1c157e2a…`), `results.jsonl` (268 records **with `raw`**, md5 `df154cb5…`), `run.log` (78/78 jobs + SUMMARY, md5 `fc3b232f…`), `critic-defects.md` (16 design defects) |
| `evidence/round9-replication/` | `predictions-r9.md` + `.sha256` + `.sha256.repo`, `ordering.log`, `run_r9.py`, `replicate.py`, `results-r9.jsonl` (284 records), `replication.md` |
| `evidence/round9-fleet/` | 10 L2 artifacts + their scripts: `probeA.md`, `probeB.md`, `probeC.md`, `critic.md`, `harness-mutation.md` + `test_harness.py` (50 cases, exit 0), `prior-art.md`, `sibling-overlap.md`, `review.md`, analysis `.py`/`.out` |
| `evidence/round10-fleet/` | 11 L2 fleet artifacts (`r10-*.md`) + their independent scripts (`mutate_test.sh` sha256 `ad0511f2…`, `probe_ref.py`, `schema_probe.py`, `recompute_r8.py`, `recompute_r9.py`), raw endpoint captures (`models-34113.json`, `props.json`, `slots.json`), `final-harness.log`, `url-status.txt`, and `INTEGRATOR-NOTES.md` (fleet map, grader first-version defect + fix, connector adoption ruling, erratum adjudication) |
| `evidence/round11-power/` | preregistration bundle (`probe_plan_r11.md`, `power_analysis_r11.md`, `predictions-r11.md`, `prereg-bundle.sha256`, `ordering.log`, `prereg-precheck.log`), probe machinery + runner (`probe_r11.py`, `run_r11.py`), run bytes (`results-r11.jsonl` md5 `c42fe3d1…`, `run.log` md5 `281cb530…`), generated `analysis_r11.md` (md5 `14663359…`), promoted `recompute_r11.py` |
| `evidence/round11-fleet/` | wave-1 L2 artifacts (`r11-critic-design.md`, `r11-prior-art-{granularity,prereg}.md`, `r11-connector.md`, `r11-review-baseline.md`, `r11-mock-smoke.md` + `mock_server_r11.py` + mock run copies, `grader_r11_draft.py`, `recompute_r11_draft.py`, `r11-log-draft.md`), wave-2 artifacts, `INTEGRATOR-NOTES.md` (integration deltas + critic adjudications + landing record) |
| `evidence/round12-ladder/` | 9-file preregistration bundle + ordering proof; probe/prediction/power machinery; 4,114-record run (`results-r12.jsonl` md5 `9dd8aa2b…`, `run.log` `700d1ddd…`); generated `analysis_r12.md` md5 `029c3bcd…`; 18 files |
| `evidence/round12-fleet/` | 16-agent design/prior-art/replay/mutation/review fleet; 22 files including `INTEGRATOR-NOTES.md`; drafts retained verbatim, with round-14 errata recorded rather than silently rewritten |
| `evidence/round13-ack-state/` | Two stdlib audit scripts: schedule-derived ack denominators (`--selftest` 4/4) and truth-aware capped-raw analysis (`--selftest` 8/8); no endpoint traffic |
| `evidence/round14-fleet/` | Nine-agent landing verification: independent recomputation (28 claims), prior-art re-fetch, live-surface drift, sibling overlap, mutation battery, round-13 reconstruction, corpus drafts, bookkeeping drafts, landing gate, and L1 adjudications |
| `evidence/round13-coverage/` | Round-13 re-dispatch: exact-path availability receipt, fixed-candidate revision-aware census, baseline/after measurements, nine-seat advisory batch and verification receipts; no model traffic |
| `evidence/round18-kimi-routing/` | Digest index for parent round 18 (census/definitions/battery/battery-opencode/fastmode/routing trees): contents, file counts, hygiene-gate results; bytes stay in the parent repo (`research/round-18-kimi-model-routing/`) |

Root-level receipt logs — runner/instrument receipts from the r19–r23 live-route
battery rounds (each carries its freeze sha, seat, and blind rule in-file):

| File | Round/probe | What it records |
|---|---|---|
| `probe-r19-P1-key1-quota.log` | r19/r20 P1 addendum | key-1 quota probe (parent-dispatched addendum, not in battery §6): runner seat, battery sha, prediction-filed stamp |
| `probe-r19-P2-servicetier.log` | r20 P2 completion | service-tier probe: freeze-2 re-verified before the first request (§7 step-2 method) |
| `probe-r19-P3.log` | r20 P3 completion | P3 probe: freeze re-verified at analysis 09:19:25Z against `plans/probe-battery-r19.md:415` |
| `probe-r19-P4-devinleg.log` | r19 P4 + P5 timing | devin leg of P4 request (i): warm-up [1/3] excluded from metrics per battery §3 |
| `probe-r19-P4-glm.log` | r19 P4-glm | glm-flash-cascade `prompt_tokens` billing: shim unit identity (MainPID, ExecStart time) and request receipt |
| `probe-r19-P5-glm.log` | r19 P5(a) | glm burst transport: zero extra requests by design — timing read from P4's two streams |
| `probe-r19-P6-zai.log` | r19 P6 | zai leg probe: battery sha at start, frozen line, first-request UTC |
| `probe-r19-P8-kimi-code-auth.log` | r20 P8 completion | kimi-code auth probe: freeze-2 re-verified, first request 09:14:49Z |
| `probe-r19-P9-absent-port.log` | r20 P9 completion | absent-port probe closing the r19 UNRUN cell: step-2 freeze recompute reproduced before first request |
| `probe-r19-devin-shim-seat.log` | r19 recon | devin shim (:8787) seat-filed recon receipt — read-only, filed before any request to that port |
| `probe-r19-hyper-predictions.log` | r19 hyper leg | hyper-lane forecasts for `deepseek-v4.1-flash` (probe) + `hyper/qwen3.8-flash` (config read only, no request) |
| `probe-r19-hyper.log` | r19 hyper leg | runner receipt for the hyper endpoint leg: dispatch, health, and responses |
| `probe-r19-opencode-health.log` | r19 opencode leg | opencode-go endpoint health (200 + model listing) on `opencode-go/deepseek-v4.1-flash`; §DEFECT 0 records two pre-freeze requests excluded from scoring |
| `probe-r19-p1-listing-mismatch.log` | r19 P1 | listing-mismatch probe: §0–§6 hash re-verified == FROZEN line; runner script sha and receipt command pinned |
| `probe-r19-quota23.log` | r19 P1 | runner-quota-23 seat: battery sha, frozen UTC, first-request UTC |
| `probe-r19-shim-ds-predictions.log` | r19 shim-ds | ds-flash shim (:8791) forecasts filed before any request; cited hypothesis sources |
| `probe-r19-shim-ds-run.log` | r19 shim-ds | execution receipt vs predictions block sha `78de64d9…`; shim code pin `42d86d99…` verified pre-run; every entry stamped |
| `probe-r19-shim-glm-predictions.log` | r19 shim-glm | glm-flash shim (:8793) forecasts for probes P4-glm + P5-glm; battery freeze `e3f08a09…` |
| `probe-r19-shim-glm-run.log` | r19 shim-glm | execution receipt vs prereg sha `a1674cfc…` filed 07:55:05Z; battery freeze pinned |
| `attrib-r21-ds-trials.log` | r21 trials | ≥20 blind trials vs the ds shim (:8791); instrument sha `b3e18c78…`, frozen table `9f0244bb…`; score appended after all trials |
| `attrib-r21-glm-trials.log` | r21 trials | ≥20 blind trials vs the glm shim (:8793); same instrument/freeze pins |
| `attrib-r21-impl-ds-trials.log` | r21 trials | instrument-impl seat copy of the ds-shim trial series; identical freeze and blind rule |
| `attrib-r21-impl-glm-trials.log` | r21 trials | instrument-impl seat copy of the glm-shim trial series; identical freeze and blind rule |
| `attrib-r22-legs.log` | r22 legs | leg-coverage forcing vs the ds shim (targets hyper, opencode-go); instrument `05da8927…`, shim pin `42d86d99…`, table `3d7861f8…` |
| `attrib-r22-legs-hyper.log` | r22 legs | hyper-target leg of the same forcing series (identical pins) |
| `attrib-r22-opencode-trials.log` | r22 legs | opencode-go-target trials (instrument `34c4fa67…`): forcing mode, target opencode-go |
| `attrib-r23-stream-trials.log` | r23 stream | stream:true path trials; blind predictions `/tmp/…/predictions.md` sha `8b26166d…` filed before first request (ephemeral path retained as record) |
| `attrib-r23-stream.log` | r23 stream | stream-path forcing series: instrument `cce53a16…`, table `1b2d6a01…` — ACCURACY 30/30, `STREAM TARGET opencode-go` clause FAIL (GT n=0) |

Round-24 additions:

| Dir | Contents |
|---|---|
| `evidence/round24-sources/` | Gate receipts for the `SOURCES.md` contract-v1 rows (per-source open receipts for the S001–S019 registry) |
| `evidence/round24-census/` | Round-24 census receipts: `base-99cf615.txt` (v2 census on a `git archive 99cf615` tree) and `after.txt` (census + SOURCES contract census on the round-24 commit) |

Round-25 additions:

| Dir | Contents |
|---|---|
| `evidence/round25-sources/` | Gate receipts for SOURCES rows S027–S037 and the S011 re-open (URL, access time, sha256, ≤25-word located quote) |
| `evidence/round25-calibration/` | Round-25 receipts: `attrib-calibration-summary.txt` / `-selftest.txt` (C1 instrument), `attrib-oracle-intervals.txt` (independent sh+awk parser), `state-check-before-6180e4f.txt` / `state-check-after.txt` / `state-check-selftest.txt` (C2), `round25-census-*.txt`, `revert-test.txt` (QUALITY R13); falsify-wave revision receipts `*-v2.txt` (Amendment 2; v1 files kept as landed) |

### `plans/` — plans, frozen instruments, and templates

| File | Covers |
|---|---|
| `plans/attrib_probe.py` | Live attribution probe instrument (sha256 floats between trials and landing per the r21 freeze-surface lesson; current `489f938a…16e06b`) |
| `plans/attrib-r21-frozen.md` | Frozen r21 feature table (anchor sha256 `9f0244bb…`, FROZEN 2026-10-16T10:20:08Z) |
| `plans/attrib-r22-frozen.md` | Frozen r22 extended feature table + forcing protocol (anchor `3d7861f8…`, FROZEN 2026-10-16T11:49:01Z) |
| `plans/attrib-r23-frozen.md` | Frozen r23 table + stream-path protocol (anchor `1b2d6a01…`, FROZEN 2026-10-16T13:45:47Z) |
| `plans/probe-battery-r19.md` | Standing battery r19 instantiation: 9 probes, 23 binary + 7 numeric components, 19-request budget; freeze record §7/§7.1 (freeze-1 `e3f08a09…` superseded mid-window, freeze-2 `e1a86777…a00a1` valid) |
| `plans/probe-battery-TEMPLATE.md` | Host-agnostic reusable battery spec; P10 attribution probe folded in (r22); lineage table cites every established practice |
| `plans/round-24-claims.md` | Round-24 pre-registered claims; before-values measured at base `99cf615` |
| `plans/round24_census.sh` | Counting script for every claimed number — run `sh plans/round24_census.sh` from the lane root |
| `plans/round-25-claims.md` | Round-25 pre-registration (frozen populations P1/P2, CP interval rule, power ask, predictions) + Amendment 1 |
| `plans/attrib_calibration.py` | C1 instrument: offline exact-CP re-verdict of the frozen P1 attribution receipts (sha256-pinned); `--summary`, `--json`, `--selftest` (exit 0/1/2) |
| `plans/state_check.py` | C2 instrument: re-derives frozen SCORECARD/SHONEN/PROVINCE/README current-state assertions; `--summary`, `--json`, `--selftest` (exit 0/1/2) |
| `plans/l0_filed_check.sh` | QUALITY R11 check: every report L0 question reached `.ufo/l0-questions.md` (exit 0/1/2) |
| `plans/round25_census.sh` | Round-25 counting script (SOURCES census, new rows, mistakes rows, SHONEN form, frontmatter triggers, both instruments' summaries) |
| `plans/fixtures/r25/` | Round-25 fixtures: `cp_reference.{py,tsv}` (exact-rational CP table), `power_table.{py,tsv}`, `attrib_oracle.sh` (independent parser), `attrib-cal/` (C1 red fixtures), `l0_filed_check/`, `shonen-seed.txt` (PROTOCOL.md:439-448 verbatim; slice sha256 3962e6b8…, pinned in `plans/state_check.py`) |
| `plans/wwkd-round-16-recensus.md` | WWKD round-16 dispatch: independent freshness re-census plan (base `d84e48d5…`) |
| `plans/wwkd-round-17-coverage.md` | WWKD round-17 dispatch: coverage continuation plan (base `3f31e54c…`) |

Re-verify the round-9 ordering proof without `/tmp`:
`cd corpus/evidence/round9-replication && sha256sum -c predictions-r9.sha256.repo` → `OK`.

In-repo gate (round 10, extended rounds 11–12 and pinned at round-14
landing): `grader.py` replays four committed probe trees (r8/r9/r11/r12)
offline. `python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1`,
exit 0; mismatch exits 1 and unreadable input exits 2. The r12 layer
regenerates both problem families, re-parses/re-grades all 1,328 graded
records, recomputes E1–E6 and every stored verdict/forecast line, verifies the
bundle/ordering chain, and md5-pins `results-r12.jsonl`, `run.log`, and
`analysis_r12.md`. `python3 grader.py --selftest` exercises S0–S7; the
round-14 mutation pass killed 4/4 fresh r12 mutations. Stdlib only, no
endpoint. It also subsumes the r9 ordering proof hermetically; the standalone
`predictions-r9.sha256.repo` check still must run from
`corpus/evidence/round9-replication/` because its path is cwd-relative
(round-10 critic F2). One stored value remains pinned as an adjudicated
erratum (`replication.md`: r9 final-turn state errors, stored 12/32,
recomputed 24/32).

## Coverage map

- **Benchmark selection**: covered (knowledge/benchmark-selection.md).
- **Search-shape mechanism evidence**: covered at iteration-2 depth (knowledge/godspeed-eval-findings.md).
- **Run harness / telemetry spec**: covered at alpha depth (knowledge/telemetry-run-design.md).
- **Model catalog access**: historical Bailian digest plus refreshed HF/OpenRouter observations; Bailian originals remain unavailable, while the public endpoints were re-probed with committed bounded raw responses and offline verification (`knowledge/local-model-index.md`, `knowledge/open-model-catalogs.md`; S101/S102; `corpus/evidence/round33/catalogs/`).
- **Eval theory**: covered at digest depth — autonomy/IID assumptions, diversity blindness, judge-vs-aggregator split (knowledge/eval-theory-notes.md).
- **Executed eval**: covered at battery depth — authored 4-task slice (r4) + full 33-task re-run under fixed endpoint (knowledge/bench-arena-round5-battery.md).

- **Wiki branch digest**: historical karpathy subtree + ai/foundations + ai/books digest (`knowledge/eval-design-digest-2.md`); original wiki unavailable. Non-karpathy `ai/` topics remain undigested and cannot currently be explored at the former path.
- **Cross-pipeline stability**: byte-identical solution set identified (16, 25, 28, 32, 33); flip-set classified at n=3 (`knowledge/bench-arena-round6-stability.md`) and **component-ablated at r7** — of 5 "scaffold-determined" tasks only 13 is genuinely scaffold-caused; tools-without-system → `finish=tool_calls` 14/15; temp not the lever (`knowledge/bench-arena-round7-scaffold-ablation.md`).
- **Multi-turn state tracking / planning horizon**: r8 built the instrument; r9 replicated probe A; r11 powered the middle contrast (+0.352, p=0.0011); r12 established the ordered four-point ladder (Page `L=1773.0`, `z=+9.452`), repeated the middle contrast (+0.297), dissociated batching from emission sparsity (+0.656), and tested a second task family (+0.177, directional at a 2/48 floor). See `knowledge/bench-arena-round12-ladder.md`.
- **Novelty pricing**: r9 priced 4/4 findings; r11 priced C1–C4 + M1–M3; r12 prices C1–C6 with fetched URLs — C1/C2/C4/C5/C6 INCREMENTAL, C3 NOVEL-instrument, phenomenon-new 0 / instrument-new 1. Round-14 reviewer re-fetched 14 load-bearing URLs and reproduced every verdict (`evidence/round14-fleet/r14-review-priorart.md`).
- **Evidence durability**: every run byte and verification artifact through round 14 is committed and indexed. The r12/r13 one-round landing debt and the r8 raw-stripping incident remain documented; no headline claim rests solely on `/tmp`.
- **Contamination detection and transparency**: covered at source-digest depth (round 24) — knowledge/contamination-detection-and-transparency.md; sources S001, S002, S004 (S003 rejected as a general score-correction).
- **Contamination transparency card format**: covered at source-digest depth (round 30, 2026-10-25) — knowledge/contamination-transparency-card.md; S081–S086. Lands as an amendment to the round-24 *Contamination detection and transparency* row, not a fourth rival card design: it maps the release-side R1–R5 and score-side S1–S2 fields into the union table's columns and adds the CG1–CG8 answerability gate on top of that entry's tier/access vocabulary. Not a contamination measurement of any benchmark, not a runtime judge, not a card any benchmark has adopted.
- **Judge calibration**: covered at source-digest depth (round 24) — knowledge/llm-judge-calibration.md; sources S009–S012.
- **Instrument interval calibration**: covered at measured depth (round 25) — knowledge/attribution-interval-calibration.md; sources S027–S030, S033, S034, S011; own-work S036/S037. Extends the Judge calibration row inward.
- **Grader robustness / response-format invariance**: covered at measured depth (round 26) — knowledge/grader-perturbation-audit.md; S044–S046, S048; frozen 1964-response audit. Extends Judge calibration inward; nine MP/MC metrics plus separate PC capture, not a new testing method (novelty held7).
- **Extraction-policy sensitivity**: covered at measured finite-corpus depth (round27) — knowledge/extraction-policy-comparison.md; S049,S051–S059; eight alternate policies on1964 pinned responses, fixed graders/truths. Parser dependence is not prompt-format compliance or a new testing method.
- **Benchmark saturation and lifecycle**: covered at source-digest depth (round 24) — knowledge/benchmark-saturation-and-lifecycle.md; sources S007, S008.
- **Agentic time horizon and task validity**: covered at source-digest depth (round 24) — knowledge/agent-time-horizon-and-task-validity.md; sources S013, S014, S005, S006. Extends the *Multi-turn state tracking / planning horizon* row with external task-duration and task-validity methodology; the lane's local horizon instrument is unchanged.
- **Statistical reporting for paired evals**: covered at source-digest depth (round 24) — knowledge/paired-eval-uncertainty-reporting.md; sources S015–S019.

- **Benchmark task-validity instruments**: covered at primary-document synthesis depth (round 29 attempt 2, 2026-10-25) — knowledge/benchmark-task-validity-checklist.md; S077-S080, S090. Moves the round-24 frontier bullet from unopened lead to a checklist whose axes each name an artefact and a locus. Not deployment config, not runtime task validity, not contamination measurement.
- **Benchmark verifier execution model**: covered at source-code depth (round 31, 2026-10-25) — knowledge/benchmark-verifier-execution-model.md; S092, S093, S100. Discharges the round-29 frontier clause "their scoring code was not read and stays open" for verifier execution only: the harness's mode resolution, the two restore guarantees that hold in shared mode, SWE-bench Pro V2's own test-space reset, and the log-scan grader behind its PASSED set. Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config.
- **Benchmark grader semantics**: covered at source-code depth (round 33, 2026-10-25, admitted under renumbered ids) — knowledge/benchmark-grader-semantics.md; S093, S103, S104. Discharges the round-31 frontier clause "and for Toolathlon" for the one task whose evaluation script is read (Toolathlon `ab-testing/evaluation/main.py` @ `9be8d8fe`): the grader is a deterministic state comparison — `record.csv` vs `expected_ratio.csv` within the executed 0.05% tolerance — preceded by two side-effect checks, the log-bucket one mixing fail-open exceptions with fail-closed credential absence; the S104 survey separates Meta-evaluation from methodology, so judge-based scoring owns its validation part. Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config.
- **Terminal-Bench 2.0 task grader (one task)**: covered at source-code depth and executed offline (round 35, 2026-10-25) — knowledge/tb2-protein-assembly-grader.md; S105, S106, S107; probe `plans/tb2_grader_probe.py`, receipt `evidence/round35/tb2-grader-probe.txt`. Discharges the round-33 frontier clause "Terminal-Bench 2.0's" scoring code for `protein-assembly` only: what `test_gblock` asserts, how `test.sh` maps it to a binary reward, and which `instruction.md` bullets each assertion enforces (a G-only linker passes; the 3000-nt cap never decides an otherwise-passing gBlock; a one-residue subprotein error fails with the order message). Not the other 88 TB2 tasks, not the correctness of the grader's literals against PDB/FPbase, not runtime execution inside the task image, not task validity (PROVINCE refuses it), not model performance.
- **Terminal-Bench 2.0 task grader (second task)**: covered at source-code depth and executed offline (round 36, 2026-10-25) — knowledge/tb2-regex-log-grader.md; S108, S109, S110; probe `plans/regex_log_probe.py`, receipt `evidence/round36/regex-log-probe.txt`. A second instance of the round-35 ground (one more of the 89 TB2 task graders, not breadth and no quality, validity or difficulty verdict), on `regex-log` only: what its one test asserts (exact equality of `re.findall(pattern, log_text, re.MULTILINE)` against a literal nine-date list over a fixed 25-line in-test log), how `tests/test.sh` turns the pytest exit into `/logs/verifier/reward.txt`, and which `instruction.md` bullets no assertion enforces — a literal alternation of the nine expected dates passes (`hardcoded-expected-dates`, predicted and observed pass), leading-zero IPv4 octets pass, while digit-adjacent dates (`1134-12-1234`), a non-four-digit year and the permitting side of Feb 29 are unobserved (a February-capped-at-28 regex passes, `feb-29-rejected`), and month-length validity never decides because the only Feb 30 / Apr 31 lines (`tests/test_outputs.py:65,67`) carry the already-invalid `172.16.0.256`. What it does enforce is bounded by the nine literals: last-date-in-line, an IPv4 present anywhere in the line, octets 0-255, month 01-12, day 01-31, letter-adjacency on both sides of date and IP, one capture group, and file presence + compilation. Not the other TB2 tasks, not the correctness of the nine literals, not the harness's own container execution (the probe calls the captured test function under a patched `Path`), not runtime task validity, not contamination.
- **Terminal-Bench 2.0 task grader (third task, one new executed edge class)**: covered at source-code depth and executed offline (round 37, 2026-10-26) — knowledge/tb2-git-webserver-grader.md; S111, S112, S113; probe `plans/git_webserver_probe.py`, receipt `evidence/round37/git-webserver-probe.txt`. A third instance of the same ground (3 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `configure-git-webserver` only: in this capture its whole score is one pytest function asserting that a helper script's stdout contains `TEST PASSED`; the helper's clone/commit/push step is run and its status never read; the content check is a shell equality after command substitution over a second request; and the body is echoed into the graded stdout. One new edge class in the executed sample: the graded state is a live HTTP service. Not the remaining 86 TB2 tasks, not task validity, difficulty or quality, not the image or a harness run, not contamination, not agent behaviour. The static-file weakness was reported upstream for TB2.1 (S114, issue #133); the entry records a replication on the pinned file.
- **Terminal-Bench 2.0 task grader (fourth task, build-provenance class)**: covered at source-code depth and executed offline (round 38, 2026-10-26) — knowledge/tb2-build-pmars-grader.md; S115, S116; probe `plans/build_pmars_probe.py`, receipt `evidence/round38/build-pmars-probe.txt`. A fourth instance of the same ground (4 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `build-pmars` only: its whole score is four pytest functions over an installed binary's output, an `ldd` `DT_NEEDED` string scan and a one-level `/app/pmars-*` tree; a canned C program with an empty `debian/` directory and a zero-byte `src/dummy.c` passes all four, the behaviour checks run whatever `pmars` is first on `PATH` while `ldd` reads the installed absolute path, and none of the seven instruction requirements is fully enforced. Adds the build-provenance edge class to the executed grader sample (presence, linkage string, directory shape, output regex); not a new verdict channel, and no novelty claim.
- **Terminal-Bench 2.0 task grader (fifth task, repository-history class)**: covered at source-code depth and executed offline (round 39, 2026-10-26) — knowledge/tb2-git-leak-recovery-grader.md; S117, S118; probe `plans/git_leak_probe.py`, receipt `evidence/round39/git-leak-probe.txt`. A fifth instance of the same ground (5 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `git-leak-recovery` only: its whole score is five pytest functions over a git repository's refs, dangling objects, one flag file and a pinned non-dot work-tree checksum; the untouched initial state passes 4 of 5, a single `echo` of the literal passes 5 of 5 while the reset-away secret commit and its blob stay in the object store, and a ref to a blob, an annotated tag message, a stash, a dot file and `.git/config` all pass 5 of 5 — so the instruction's "cannot be found anywhere in that repo" is only partly enforced, while "irrelevant files untouched" (the checksum) and "recover the literal" are enforced. The class "a do-nothing or partial agent passes most tests" is published TB validation practice; the entry claims a probed instance only.
- **Terminal-Bench 2.0 task grader (sixth task, binary database file pair)**: covered at source-code depth and executed offline (round 40, 2026-10-26) — knowledge/tb2-db-wal-recovery-grader.md; S119, S120; probe `plans/db_wal_probe.py`, receipt `evidence/round40/db-wal-probe.txt`. A sixth instance of the same ground (6 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `db-wal-recovery` only: its whole score is seven pytest functions over one JSON export whose source of truth is a SQLite main database plus an XOR-encrypted write-ahead log, so the repair the instruction asks for is never read — `cases=28 observed_pass=8 observed_fail=20 mismatches=0`, `regrade cases=28 differ=0`. The passing vacuum is bounded by length, id multiset and the 22 pinned cells (`empty-list`, `truth-drop-id11`, `truth-plus-duplicate-id11`, `truth-wrong-path` fail); the unanswered surfaces are the database itself, the WAL, nine values, two names, extra keys and `True`-as-int. Not runtime task validity, not contamination measurement, not deployment config.
- **Terminal-Bench 2.0 task grader (seventh task, embedded-scheduling-model class)**: covered at source-code depth and executed offline (round 41, 2026-10-26) — knowledge/tb2-constraints-scheduling-grader.md; S122, S123; probe `plans/constraints_probe.py`, receipt `evidence/round41/constraints-probe.txt`. A seventh instance of the same ground (7 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `constraints-scheduling` only: the verdict is no longer an assertion over a fixed artefact but a computation — `_hard_ok` and `_overlap` are a scheduling model embedded in the test file that rescans the three sha256-pinned calendars at minute granularity, so the graded state is a one-event ICS file and the grader's own model decides it (`cases=25 observed_pass=6 observed_fail=19 mismatches=2`, `regrade cases=25 differ=0`). The passing six are the task's own `solve.sh`, a hand-typed correct file that never reads a calendar, a decoy-first file, a CRLF-line-end file, a file with a fourth attendee, and a run that rewrote all three inputs with CRLF (`receipt:8,9,14,24,29,31`); the unanswered surfaces are whether any calendar was read, which `VEVENT` is the meeting (tests 2-3 read the file's first `DTSTART`, so `decoy-first-vevent` passes 3/3, `receipt:14`), whether an invalid-but-unpreceded slot is caught (`bob-start-0900-wed` and `wed-1059-overlaps-alice`, both `PFP`, `receipt:13,23`), byte-level input integrity (`input-crlf-rewrite` 3/3 against `instruction.md:17-18`, `receipt:31`), and RFC 5545 conformance (three valid forms fail: `folded-attendee-line`, `dtstart-value-datetime`, `lowercase-property-names`, `receipt:25,26,30`). Not runtime task validity, not contamination measurement, not deployment config.
- **Terminal-Bench 2.0 task grader (eighth task, grader-compiled-simulator class)**: covered at source-code depth and executed offline (round 42, 2026-10-26) — knowledge/tb2-circuit-fibsqrt-grader.md; S125, S126, S127 (+ S128, tier B prior art); probe `plans/fibsqrt_probe.py`, receipt `evidence/round42/fibsqrt-probe.txt`. An eighth instance of the same ground (8 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `circuit-fibsqrt` only: the graded artefact is a program in a data format — `/app/gates.txt`, a gate list that the task's own `sim.c` interprets — and the grader compiles that interpreter itself (`gcc -O3 /tests/sim.c -o sim` in the cwd, `test_outputs.py:65-67`) before running `/app/sim N` over 28 fixed inputs (`:73-102`, largest 48401 = 220²+1), so the whole score is `Path("/app/gates.txt").exists()`, `sum(1 for line in f) < 32000` and 28 stdout integers compared with `fib(isqrt(N)) % 2**32` (`:7-11`, `:14-23`, `:115-117`). Neither the instruction nor the tests constrain the circuit: a 1195-line lookup table for exactly the 28 graded inputs passes 3 of 3 (`lookup-28`) although `instruction.md:12-13` says `sim 208` gives 377 and `sim 20000` gives 1407432322 and that file prints 0 for both; dropping the largest graded input or flipping one answer bit fails only the output test (`lookup-27-drop-48401`, `lookup-28-bitflip-41`, `PPF`); blank padding to 31999 lines passes while 32000 fails only the size test (`PFP`); `#` comment lines, full line reversal and CRLF all pass, while one trailing space per line fails the output test because a scanned copy line that matches no form stays a constant-0 gate (`sim.c:113`, `:126`, `:156`; wave-1 `R42CritProbe` D1); a planted executable `/app/sim` is overwritten by the grader's compile into the cwd (`fake-sim-script`, `PPF`; the verifier's cwd is `/app`, `R42ScoutHarborCwd`); and a directory at `/app/gates.txt` passes existence only (`PFF`). `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0`.
- **Terminal-Bench 2.0 task grader (tenth task, constant-compare-of-a-file class)**: covered at source-code depth and executed offline (round 44, 2026-10-26) — knowledge/tb2-feal-linear-cryptanalysis-grader.md; S138–S146; probe `plans/feal_linear_probe.py`, receipt `evidence/round44/feal-linear-probe.txt`. A tenth instance of the same ground (10 of the 89 TB2 task graders; not breadth, and no quality claim).
- **Terminal-Bench 2.0 task grader (ninth task, in-process module-import class)**: covered at source-code depth and executed offline (round 43, 2026-10-26) — knowledge/tb2-feal-differential-cryptanalysis-grader.md; S129–S134; probe `plans/feal_probe.py`, receipt `evidence/round43/feal-probe.txt`. A ninth instance of the same ground (9 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `feal-differential-cryptanalysis` only: the graded artefact is a Python module the grader imports and calls in its own interpreter (`test_outputs.py:22-24`) beside the reference extension `feal_in_c` whose public `get_keys()` holds the answer (`feal_module.c:51`), and the verdict is pytest's exit status (`test.sh:25`), so `attack()` may read the answer, replace it, or end the process instead of attacking the cipher — six of the eight observed passes never recover a key (`cheat-import-get_keys`, `cheat-always-equal`, `cheat-sysmodules-shadow`, `cheat-patch-get_keys`, `cheat-exit-zero`, `cheat-clock-seed`; receipt:15-20); the key schedule is a 16-bit seed per round key under one `srand(time(NULL))` per process (`feal.c:56-67`), which is both the instruction's own hint (`instruction.md:4-6`) and a replayable clock read; nothing times the call, so a 45 s oracle passes (`slow-oracle-45s`, receipt:21) although `instruction.md:3` asks under 30 s and `README.md:35` claims the test confirms that limit; and the four failures are the ones that return a wrong or wrongly-typed value (`nop`, `wrong-key`, `oracle-off-by-one`, `return-str`; receipt:10, :12-14) — `cases=12 observed_pass=8 observed_fail=4 mismatches=0`, `regrade cases=12 differ=0` (receipt:22-23). Not the task image (never pulled; `task.toml:29`, `allow_internet = true` at `:34`) or a harness run (the task's own `solve.sh` is executed as one case and observed pass), not contamination, not model or agent behaviour.
- **Terminal-Bench 2.0 task grader (eleventh task, second F1 constant-compare exemplar)**: covered at source-code depth and executed offline (round 45, 2026-10-26) — knowledge/tb2-password-recovery-grader.md; S149–S156; probe `plans/password_recovery_probe.py`, receipt `evidence/round45/password-recovery-probe.txt`. An eleventh instance of the same ground (11 of the 89 TB2 task graders; not breadth, and no quality claim).
## Open gaps

- **n≥2 on flip-capable tasks**: CLOSED round 6 — 8 flip tasks + 3 controls at n=3; flips decompose to scaffold (5), noise (2), strategy-bound (1). See `knowledge/bench-arena-round6-stability.md`. **r7 refinement: component ablation reclassified the "scaffold 5" → 1 true scaffold (13), 3 noise (03/08/31), 1 weak pull (12)** — see `knowledge/bench-arena-round7-scaffold-ablation.md`.
- **Planning-horizon coverage**: CLOSED as an instrument, OPEN as a claim — round 8 built and ran a 3-probe multi-turn instrument (`evidence/round8-horizon/`, analyzed in `knowledge/bench-arena-round8-horizon.md`), round 9 replicated probe A on fresh seeds with a checkpoint-dose cell (`knowledge/bench-arena-round9-replication.md`). What remains unmeasured: a probe B whose manipulation actually binds (2/8 well-formed corruptions in r8), probe C at n≥12 (4 reps → 1–2 distinct generations), and the arithmetic covariate the r8 critic asked for and never got (defect #2).
- **27 test-timeout**: CLOSED round 6 — hidden-contract thread-exception deadlock + semantically-broken sol, not slowness. See `knowledge/bench-arena-task27-timeout-anatomy.md`.
- **Scaffold-delta mechanism**: CLOSED round 7 — verbatim wire capture (temporary proxy provider) + component ablation. Causal inventory: system prompt (context mass) drives strategy choice; `tools`+`tool_choice:auto` without system = `finish=tool_calls` harness defect; temperature absent→0.8 not causal; `enable_thinking` no-op (template has no think branch). See `knowledge/bench-arena-round7-scaffold-ablation.md`.
- **v2-vs-today scaffold drift** (new, round 7): the captured skills catalog may differ from v2's (v2 ran 1mo ago); E1 replay reproduced v2 direction on 13 but not 03 (v2's lone 03-PASS was a lucky draw — see r7 knowledge). Exact replay fidelity vs 1-month-old scaffold is unverified — attribute v2-side drift before citing v2 sols.
- **Probabilistic forecasts**: CLOSED round 11 at event level (3 predictions, Brier 0.153) and round 12 at per-problem level (416 pass events filed pre-request; Brier `0.1288`, BSS `+0.0447`, slope `+0.8427`). Caveat: persistence skill dominates; family-2 base-rate transport failed (`2/48` both arms, BSS `-3.1474`).
- **No in-repo gate**: CLOSED round 10; extended round 11 to 280 checks/three trees, round 12 to 732 checks/four trees, and round-14 landing to **733** by pinning `analysis_r12.md`. S0–S7 all pass; 4/4 fresh r12 mutations killed.
- **Cold-agent executability**: historical aggregator cold run reproduced 20/20 commands at `0c51208` (`lessons/round-8-aggregator-box3-coldrun.md`). That is not a current live-source pass: the original host sources are now unavailable. Current support is limited to the retained-byte offline entry points above; SHONEN box 3 is not freshly externally verified.
- **Ack metric denominators** (round 13): `-ack` storage labels mix ack-only and full-state prompts. Future rates must use schedule-derived intent denominators; r11 CKPT710 is 85.9% prefix / 84.4% bare on 384 true ack prompts, not 64.5% over 512 label rows.
- **Analysis regeneration** (round 14): `analysis_r12.md` is now md5-pinned, but regeneration remains path-dependent by one absolute `Generator source` line; every statistic independently reproduces. Make future generated reports path-insensitive.
- **Bench-arena availability**: round 14 recorded relocation from `~/bench-arena` to `~/archive/bench-arena`; both exact paths are now unavailable (`evidence/round13-coverage/surface-receipt.json`). Historical hashes and the retained digest do not recover the benchmark tree.
- **Prior-art digest queue**: Laban et al. ICLR 2026 (`arxiv.org/abs/2505.06120`), Lanham et al. (`2307.13702`), and llama.cpp #7052 are fetched and used in pricing artifacts; synthesis into standalone corpus digests remains open.

## Frontier

Unexplored ground named round 24 — each item carries why and the next
source/instrument (ART dossier §Leads; nothing below is admitted knowledge yet):

- **Agentic benchmark task-spec audits**: why — S005/S006 show lab self-audits finding task-level validity defects *after* publication; the lane has no instrument that audits a benchmark's task specs, graders, and contamination separately. Next source/instrument: the primary specs and scoring code for Terminal-Bench 2.0, Toolathlon, and SWE-bench Pro (unopened leads in the ART dossier), turned into a per-benchmark task-validity checklist.
  - *Partly discharged round 29 attempt 2 (2026-10-25):* `knowledge/benchmark-task-validity-checklist.md` builds the per-benchmark task-validity checklist from the primary maintainer artefacts of Terminal-Bench 2.0, SWE-bench Pro V2 and Toolathlon-Verified. It supersedes the `primary specs` half of the `unopened leads` phrase for those three sources — their scoring code was not read and stays open; contamination-transparency cards, runtime task validity and hosted judges remain open.
  - *Partly discharged round 31 (2026-10-25):* `knowledge/benchmark-verifier-execution-model.md` reads the harness's own verifier-mode resolver and `Verifier.verify` at Harbor commit `6099b8cf`, so the `their scoring code was not read and stays open` clause above is discharged for **verifier execution** (where grading runs, what is restored first, how SWE-bench Pro V2 derives its PASSED set). The clause stays open for the other benchmarks' scoring code (one SWE-bench Pro V2 task's grader *is* read here, in depth, and that is the only task-level code this round opens), for runtime task validity (which `PROVINCE.md` refuses to this lane) and for Toolathlon; the Terminal-Bench 2.0 axis-E cell is filled by this entry (round 34 clarification: this means verifier execution context, not a task-level scoring-code audit) and the SWE-bench Pro axis-E cell was already credited to S078 in `knowledge/benchmark-task-validity-checklist.md:96`.
  - *Partly discharged round 33 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads S103's one Toolathlon task (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and S104's LLM-as-judge survey frame (arXiv 2412.05579v2). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane).
  - *Partly discharged round 35 (2026-10-25):* `knowledge/tb2-protein-assembly-grader.md` reads and executes one Terminal-Bench 2.0 task's scoring code (`protein-assembly/tests/test_outputs.py` + `tests/test.sh` @ `2fd12b88`) against its `instruction.md`. The "Terminal-Bench 2.0's" clause is discharged **for that one task only**; it stays open for the other TB2 tasks, for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane).
  - *Partly discharged round 36 (2026-10-25):* `knowledge/tb2-regex-log-grader.md` reads and executes a second Terminal-Bench 2.0 task's scoring code (`regex-log/tests/test_outputs.py` @ `2fd12b88`; `tests/test.sh` read, not run) against its `instruction.md`. The "Terminal-Bench 2.0's" clause is discharged **for that one task only**; it stays open for the other TB2 tasks, for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane).
  - *Partly discharged round 37 (2026-10-26):* `knowledge/tb2-git-webserver-grader.md` reads and executes a third Terminal-Bench 2.0 task's scoring code (`configure-git-webserver/tests/test_outputs.py` + `tests/verify.sh` @ `2fd12b88`) against its `instruction.md`. The "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the remaining TB2 task graders (3 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane).
  - *Partly discharged round 38 (2026-10-26):* `knowledge/tb2-build-pmars-grader.md` reads and executes a
    fourth Terminal-Bench 2.0 task's scoring code (`build-pmars/tests/test_outputs.py` @ `2fd12b88`; S115,
    S116) against its `instruction.md`, probe `plans/build_pmars_probe.py`, receipt
    `corpus/evidence/round38/build-pmars-probe.txt`. The graded state is a class the lane had not executed
    before: a built executable plus a source tree, scored by `Path.exists()`, an `ldd` stdout string scan,
    directory shape and a `re.match` prefix on program stdout, with no rebuild anywhere — so a canned
    21-line C program with an empty `debian/` directory and a zero-byte `src/dummy.c` passes all four
    tests, a `dlopen()`ed libX11 is invisible to the `ldd` scan, `Results: 12 34 78 forged` passes the
    prefix match, a binary that exits 3 passes, a canned script earlier on `PATH` answers the behaviour
    checks while `ldd` reads the silent installed file, `debian` may be a regular file, and a directory
    named `src/sim.c` counts as C source (`cases=22 observed_pass=7 observed_fail=15 mismatches=0`). The
    "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the remaining
    TB2 task graders (4 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for
    runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image, the oracle or a
    harness run, not contamination, not model or agent behaviour.
  - *Partly discharged round 39 (2026-10-26):* `knowledge/tb2-git-leak-recovery-grader.md` reads and executes a
    fifth Terminal-Bench 2.0 task's scoring code (`git-leak-recovery/tests/test_outputs.py` @ `2fd12b88`; S117,
    S118) against its `instruction.md`, probe `plans/git_leak_probe.py`, receipt
    `corpus/evidence/round39/git-leak-probe.txt`. The graded state is a class the lane had not executed before:
    a git repository's object store and refs plus one flag file at `/app/secret.txt`, scored by a `strip()`ed
    literal equality, two `git log --all` greps (messages, then `-p -S` contents), a `git log --oneline --all`
    substring on the init message, a `git fsck --lost-found` sweep over `dangling` objects and a work-tree
    `sha256sum` that skips dot paths — so the untouched initial repo fails only the flag test, writing the
    literal alone passes 5/5 while the secret commit stays in the reflog, a non-branch ref pinning the secret
    blob, an annotated tag message, a stash, a dot file and `.git/config` all pass 5/5, and a dangling blob or
    an unreferenced commit whose message carries the secret fails test 4 (`cases=25 observed_pass=13
    observed_fail=12 mismatches=0`). The "Terminal-Bench 2.0's" clause is **narrowed for that one task only**;
    it stays open for the remaining TB2 task graders (5 of 89 read), for any SWE-bench Pro V2 grader beyond the
    round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image
    or a harness run (the task's own `solve.sh` is executed as one case and observed pass), not contamination,
    not model or agent behaviour.
  - *Partly discharged round 40 (2026-10-26):* `knowledge/tb2-db-wal-recovery-grader.md` reads and executes a
    sixth Terminal-Bench 2.0 task's scoring code (`db-wal-recovery/tests/test_outputs.py` @ `2fd12b88`; S119,
    S120) against its `instruction.md`, probe `plans/db_wal_probe.py`, receipt
    `corpus/evidence/round40/db-wal-probe.txt`. The graded state is a class the lane had not executed before:
    a JSON export at `/app/recovered.json` whose source of truth is a binary database file pair — `main.db` plus
    an XOR-encrypted `main.db-wal` — scored by a path existence check, one `json.load`, a field-type pass, id
    sortedness, eleven ids in order, a duplicate check and a WAL test that re-reads two of the same cells, so the
    untouched initial state scores 0 of 7 while hand-typed JSON that never opens the database scores 7 of 7
    (only 22 of the 33 id/name/value cells are pinned), a wrong-key XOR followed by a read-write extraction and a plain read-write open both fail
    exactly the completeness and WAL tests, and a genuinely repaired WAL with no export scores 0 of 7
    (`cases=28 observed_pass=8 observed_fail=20 mismatches=0`). The "Terminal-Bench 2.0's" clause is **narrowed
    for that one task only**; it stays open for the remaining TB2 task graders (6 of 89 read), for any SWE-bench
    Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this
    lane). Not the task image (never pulled) or a harness run (the task's own `solve.sh` is executed as one case
    and observed pass), not contamination, not model or agent behaviour.
  - *Partly discharged round 41 (2026-10-26):* `knowledge/tb2-constraints-scheduling-grader.md` reads and executes a
    seventh Terminal-Bench 2.0 task's scoring code (`constraints-scheduling/tests/test_outputs.py` @ `2fd12b88`; S122,
    S123) against its `instruction.md`, probe `plans/constraints_probe.py`, receipt
    `corpus/evidence/round41/constraints-probe.txt`. The graded state is a class the lane had not executed before: a
    one-event ICS file at `/app/meeting_scheduled.ics` decided by a scheduling model embedded in the test file —
    `_hard_ok`, `_overlap` and a minute-granularity earliest-slot scan over three sha256-pinned input calendars — so
    the grader computes the verdict instead of asserting it over a fixed artefact, and it reads the ICS with regexes,
    not an ICS parser, so a hand-typed Wednesday 11:00 file passes 3 of 3 without opening a calendar, a decoy first
    `VEVENT` passes 3 of 3 with the attendee meeting on Friday 15:00, the earliest test passes slots that violate the
    hard constraints because no valid slot precedes them, rewriting all three inputs with CRLF line ends passes 3 of 3
    although `instruction.md:17-18` says any modification fails, `DTEND` is read only by the structure test, and three
    RFC 5545-form output forms fail while a CRLF output passes (`cases=25 observed_pass=6 observed_fail=19
    mismatches=2`). The "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the
    remaining TB2 task graders (7 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for
    runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image (never pulled) or a harness
    run (the task's own `solve.sh` is executed as one case and observed pass), not contamination, not model or agent
    behaviour.
  - *Partly discharged round 42 (2026-10-26):* `knowledge/tb2-circuit-fibsqrt-grader.md` reads and executes an
    eighth Terminal-Bench 2.0 task's scoring code (`circuit-fibsqrt/tests/test_outputs.py` with `tests/sim.c` @
    `2fd12b88`; S125, S126, S127) against its `instruction.md`, probe `plans/fibsqrt_probe.py`, receipt
    `corpus/evidence/round42/fibsqrt-probe.txt`. The graded state is a class the lane had not executed before: a
    program in a data format — `/app/gates.txt` is a gate list that the task's own simulator executes, and the
    grader compiles that simulator itself (`gcc -O3 /tests/sim.c -o sim` in the cwd, `test_outputs.py:65-67`) before
    running `/app/sim N` for 28 fixed inputs (largest 48401 = 220²+1, `:73-102`) and comparing stdout with
    `fib(isqrt(N)) % 2**32` (`:115-117`). A 1195-line lookup table for exactly the 28 graded inputs passes 3 of 3
    (`lookup-28`) while printing 0 for `instruction.md:12-13`'s own examples 208 and 20000; the coverage gap above
    48401 is published prior art (S128), the lookup construct and the parse/ordering/cwd mechanics were not found
    (`R42ScoutPriorArt`). `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0`. The
    "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the remaining TB2 task
    graders (8 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity
    (which `PROVINCE.md` refuses to this lane). Not the task image (never pulled) or a harness run, not
    contamination, not model or agent behaviour.
  - *Partly discharged round 43 (2026-10-26):* `knowledge/tb2-feal-differential-cryptanalysis-grader.md` reads and
    executes a ninth Terminal-Bench 2.0 task's scoring code (`feal-differential-cryptanalysis/tests/test_outputs.py`
    with `tests/feal_module.c`, `tests/feal.c` and `tests/test.sh` @ `2fd12b88`; S129–S134) against its
    `instruction.md`, probe `plans/feal_probe.py`, receipt `corpus/evidence/round43/feal-probe.txt`. The graded state
    is a class the lane had not executed before: an agent-authored **Python module imported into the grader's own
    interpreter and called** (`test_outputs.py:22-24`), beside the reference C extension `feal_in_c` that the grader
    builds first (`:20`) and whose public `get_keys()` holds the answer (`feal_module.c:51`), with pytest's exit
    status as the whole verdict (`test.sh:17-25`). Six of the eight observed passes involve no cryptanalysis — the
    reference `get_keys()[5]`, an object whose `__eq__` is always True, a fake `feal_in_c` in `sys.modules`, a
    rebound `get_keys`, `os._exit(0)` before the assertion, and a libc replay of `srand(time(NULL))` over the 16-bit
    per-key seed (`feal.c:56-67`) — and a 45 s oracle passes (`slow-oracle-45s`) although `instruction.md:3` asks
    under 30 s and `README.md:35` says the test confirms that limit, while nothing times the call (receipt:15-21).
    `cases=12 observed_pass=8 observed_fail=4 mismatches=0`, `regrade cases=12 differ=0`. The "Terminal-Bench 2.0's"
    clause is **narrowed for that one task only**; it stays open for the remaining TB2 task graders (9 of 89 read),
    for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md`
  - *Partly discharged round 44 (2026-10-26):* `knowledge/tb2-feal-linear-cryptanalysis-grader.md` reads and executes a tenth Terminal-Bench 2.0 task's scoring code (`feal-linear-cryptanalysis/tests/test_outputs.py` @ `2fd12b88`; S138–S146) against its `instruction.md`, probe `plans/feal_linear_probe.py`, receipt `corpus/evidence/round44/feal-linear-probe.txt`. The graded artefact is an agent-written text file, read whole (`:120`) and searched for 100 embedded decimal constants (`:121-122`) — a class distinct from round 43's imported module: concatenated, reversed, zero-padded and decoy-laden answers pass, one missing value fails, and three attack-free passes read the public keys (`gen.py:12`), the public hash chain (`:61-62`) and the test's own constants (`:4-103`). `cases=14 observed_pass=8 observed_fail=6 mismatches=0`, `regrade cases=14 differ=0`. The "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the remaining TB2 task graders (10 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image (never pulled) or a harness run, not contamination, not model or agent behaviour.
    refuses to this lane). Not the task image (never pulled) or a harness run, not contamination, not model or agent
    behaviour.
  - *Partly discharged round 45 (2026-10-26):* `knowledge/tb2-password-recovery-grader.md` reads and executes an eleventh Terminal-Bench 2.0 task's scoring code (`password-recovery/tests/test_outputs.py` @ `2fd12b88`; S149–S156) against its `instruction.md`, probe `plans/password_recovery_probe.py`, receipt `corpus/evidence/round45/password-recovery-probe.txt`. The graded artefact is an agent-written guesses file, `split("\n")`-ed and searched for one embedded constant — the second measured F1 exemplar: `constant`, `constant-crlf` and `decoys-1000` pass from the public test file alone, every format violation fails on membership at `:18`, `cases=16 observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16 differ=0`. The "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the remaining TB2 task graders (11 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image (never pulled) or a harness run, not contamination, not model or agent behaviour.

- **Contamination transparency cards**: why — `knowledge/contamination-detection-and-transparency.md` establishes the tier/access vocabulary but the lane has no standard card format recording detector access, tier tested, and what a negative cannot rule out. Next source/instrument: current benchmark-maintainer releases on hidden-test governance and contamination-transparency cards (unopened lead); draft a card template and gate a knowledge entry on Q1–Q8.
  - *Partly discharged round 30 (2026-10-25):* `knowledge/contamination-transparency-card.md` supplies the card format and the CG1–CG8 gate as an amendment to `knowledge/contamination-detection-and-transparency.md`, re-grounded on S081–S086 opened this round — the tabulated card designs now carry a record of detector access, tier tested and what a negative cannot rule out. This supersedes the `draft a card template and gate a knowledge entry on Q1–Q8` instruction and, for the card format only, the `unopened lead` phrase. The eight questions the instruction names are the entry's own answerability questions, labelled CG1–CG8 there so they cannot be confused with `QUALITY.md` Q1–Q8; the instruction line itself is left byte-identical, so a reader can see what changed and what did not. Still frontier: benchmark-maintainer releases on hidden-test governance (no private-split or hidden-test-governance release was opened this round), a runtime judge as the scoring artefact, and adoption of the card by any benchmark.
- **Judge calibration applied inward**: why — the lane's own grader/attribution outputs (`grader.py`, `plans/attrib_probe.py` verdicts) are judged artifacts that have never been through the S009–S012 calibration protocol the new entry describes. Next source/instrument: port the S011 sensitivity/specificity correction + S010 perturbation audit onto the r21–r23 trial receipts (`evidence/attrib-r2*-*.log`).
  - *Partly discharged round 25 (2026-10-20):* the attribution receipts now carry exact-interval verdicts (`knowledge/attribution-interval-calibration.md`); `grader.py` outputs and an S010-style perturbation audit remain frontier.
  - *Correction (round 25 falsify, 2026-10-20):* the discharge also landed a Rogan–Gladen share bound in S011's estimator form, but S011's own interval method was not ported and the landed bound was conditional (`rg_cond`); with the sampling arm (`rg90`) it is vacuous on P1 — see the entry's §Corrections.
  - *Partly discharged round 26 (2026-10-21):* `knowledge/grader-perturbation-audit.md` covers the pinned `grader.py` response-format audit. This supersedes the round-25 “grader.py outputs … remain frontier” phrase only for this frozen population. New formats, future generalization and a separately designed parser-policy comparison remain open.
  - *Partly discharged round27 (2026-10-21):* `knowledge/extraction-policy-comparison.md` closes the separately designed parser-policy comparison for the same1964 pinned responses. This supersedes only that part of the round26 open clause. Independently sampled formats, instruction-exact parsing and future/generalized claims remain frontier.
- **Identity-verified endpoint for novelty probes**: why — `:34113` is absent (`ss -ltn 'sport = :34113'` → no listener, 2026-10-19); only the read-only ds-flash-shim (`:8791`, sha-pinned) resolves, so no new live capability/novelty probe can run. Next source/instrument: an identity-verified endpoint (kama-owned serving plane, operator-owned restoration) plus the standing `plans/probe-battery-TEMPLATE.md` to re-instantiate the battery.
- **Non-karpathy wiki topics**: why — `ai/` subtrees outside karpathy remain undigested and the source is absent (`~/Projects/webzites/repos/llm-wiki` → `test -e` absent). Next source/instrument: none available on-host; the row stays frontier until the wiki path resolves again (round-13/16 receipts record it absent).

## Round-26 supporting artifacts (2026-10-21)

| Path | Covers |
|---|---|
| `evidence/round26-sources/` | Located S043–S047 opening quotes, byte identities, bounded papers/PyPI/GitHub prior-art search; direct tooling prior art found |
| `evidence/round26-calibration/` | Round-start receipts, Q13 red-before and final C1/C2 measurements |
| `../plans/grader_perturb.py` | Byte-pinned finite-population response-format audit; MP/MC/PC denominators and interpretation per Amendment 1 |
| `../plans/gate_timing_check.py` | Q13 commit-tree structural evidence support, not approval or admission-identity adjudication |
| `../plans/round26_census.sh` | Round-26 count commands using lane master ref, not detached HEAD |
| `../plans/fixtures/r26/` | Independent oracle, frozen population manifest, content pins, perturbation cases, state-check red mutations, timing fixtures and separability harness |

Appended inventory corrections: the `lessons/round-25.md` row above's M23–M30 range describes its first
landing; the completed lesson reaches M38. The `evidence/round25-sources/` row's S027–S037 range likewise
describes its first landing; round-25 source rows end at S042. `QUALITY.md` now contains Q1–Q13 (not the
supporting-files row's historical Q1–Q8); S047 supersedes S037's older selftest teaching.

Round-26 closure addendum: the admission bar is Q1–Q14; Q14 refines Q13's reader-role/identity authority,
not a second admission method. All new supporting files above are local artifacts, not live endpoint probes.

Round-26 source-support correction: the supporting-artifact row's initial S043–S047 range is superseded
by **S043–S048**; S048 corrects S043's quote location before knowledge admission
(`lessons/round-26.md` §Source-location correction before admission).

## Round-27 supporting artifacts (2026-10-21)

| Path | Covers |
|---|---|
| `evidence/round27-sources/` | S049–S056 located opening quotes and scoped source-to-policy mapping |
| `evidence/round27-calibration/` | Round-start receipts and final counters/mutation/separability receipts |
| `../plans/parser_policy_compare.py` | Fixed-response E0–E8 verdict agreement; parser-only counterfactual, not alternate complete harness runs |
| `../plans/policy_cases.py` |59 hand-expected policy cases, including the E6 last-fence survivor witness; executed by comparator selftest |
| `../plans/round27_census.sh` | Read-only round-27 counters with lane master revision |
| `../plans/fixtures/r27/` | Policy oracle, synthetic edge cases, frozen P4 mutations and preservation checks |

The new knowledge candidate is still outside corpus until Q10/Q13/Q14 rereads return; no coverage-map
discharge is asserted by these supporting-artifact rows.

Round27 admission addendum supersedes the earlier deferred/supporting-source-range snapshot: the Gate now
records returned corrected-candidate rereads; S049–S060 are12 added source rows (11A/1B, one repair-policy
rejection). Q1–Q16 is the current admission bar; Q16 strengthens Q15 traversal/isolation, not truth endorsement.
The separately implemented full numeric witness is `../plans/fixtures/r27/independent_policy_recheck.py`;
only its root binding was relocated by L1, its replay logic is FEntryNumbers' retained evidence.


## Round28 supporting artifacts (2026-10-21; knowledge admission deferred)

| Path | Covers |
|---|---|
| `lessons/round-28.md` | M65 literal-reference drift, corrected source locations/scope, source openings and source-cell old→new, deferred Gate |
| `evidence/round28-calibration/` | Round-start census/absence evidence; observed C1/C2 counters, baseline/only-delta/revert experiments and historical-verdict preservation |
| `../plans/benchmark_spec_audit.py` | Read-only pinned WebArena snapshot inventory and static scorer-contract facts, not task-validity certification |
| `../plans/registry_check.py` | Frozen13-row literal-reference coverage across baseline35 knowledge paths; no semantic citation endorsement |
| `../plans/fixtures/r28/` | Licensed/pinned source snapshots, declared populations, alternate L1-authored censuses and acceptance experiments |
| `../plans/round28_census.py` | Claim/source/index counter command with explicit caller-supplied measured revision label |

The candidate remains `../.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`; no canonical knowledge
row or frontier discharge is asserted before returned complete Q10 re-reads of its exact bytes.

### Round28 admitted knowledge and partial frontier advance

| Entry | Covers | Primary source |
|---|---|---|
| `knowledge/webarena-task-spec-audit.md` | Pinned WebArena static812-task inventory,16 source-audited cases and scorer-contract limits; not task validity or model performance | S061–S063/S068/S069; S005/S006 bounded precedent context; round28 Gate |

| Coverage-map ground | Held now | Entry |
|---|---|---|
| Agentic benchmark task-spec/scorer observability | WebArena snapshot dce04686 static schema/predicate inventory and selected-case checked/unchecked mapping | `knowledge/webarena-task-spec-audit.md` |

**Partly discharged round28:** the original Frontier task-spec-audit gap is closed only for this
WebArena static surface. Terminal-Bench2.0, Toolathlon and SWE-bench Pro primary specifications,
generated eval-time configs, runtime DOM/helper/judge validity and contamination checks remain open.
The earlier deferred round28 index statement is superseded by the actual Gate admission and this row.

## Round29 supporting artifacts (2026-10-21; knowledge admission deferred)

| Path | Covers |
|---|---|
| `lessons/round-29.md` | M87 derived-control/source-unit mistake, crash and forecast-criterion rows, source openings, Gate |
| `lessons/round-44.md` | Five gate-tool behaviours demonstrated under fence repairs F1–F6 (C1); `feal-linear-cryptanalysis` admitted with a held-out predictor leg V11 (C2); round-43 closure R1–R5; mined mistakes incl. a hash-shaped scope phrase and a memorizable V11 sample | `plans/round-44-claims.md`; `.ufo/waves/round-44/` |
| `lessons/round-45.md` | Envelope framing in the receipt; spec/manifest name split; refusal-with-read is a defect; single-token quotes under the word floor; digest list drifting behind its own pin; gate hygiene racing mid-run landings | LOG.md round 45, `corpus/evidence/round45/`, `plans/round-45-claims.md` |
| `evidence/round29-calibration/` | Round-start absence/census receipts; build and post-falsify repair summaries, selftests, JSON digests, cross-Python runs, mutation witnesses, projection-equality proof |
| `../plans/config_projection.py` | Offline source-faithful projection of the pinned WebArena generator over 812 raw tasks × 3 synthetic profiles; not deployment configs or task validity |
| `../plans/fixtures/r29/` | Pinned generator/profile manifest, seat-authored hand fixtures (digest-pinned in the instrument) and the persisted mutate-run-revert witness |

The candidate remains `../.ufo/waves/round-29/drafts/webarena-config-projection.md`; no canonical knowledge
row or frontier discharge is asserted before returned complete second-seat re-reads of its exact bytes.

### Round29 admitted knowledge and partial frontier advance

| Entry | Covers | Primary source |
|---|---|---|
| `knowledge/webarena-config-projection.md` | Offline pinned WebArena generator projection over812 tasks×3 synthetic profiles, occurrence/changed-field provenance and output-ordinal mapping; not deployment configs or task validity | S070–S074; S068 input pin; round29 Gate |

| Coverage-map ground | Held now | Entry |
|---|---|---|
| Agentic benchmark generated-config observability | Source-faithful offline projection at dce04686 under three frozen synthetic profiles, with order/index witnesses and separate-logic oracles | `knowledge/webarena-config-projection.md` |

**Partly discharged round29:** offline projection of generated configs is now held. Actual env_config-derived/
deployment configs, runtime DOM/helper/judge/task validity and contamination remain open, as do the other
named benchmark specifications. This narrows, not erases, the round28 gap line above and supersedes only
the round29 deferred index statement after the Gate's exact-byte admission.

### Round-30 to Round-33 evidence

- `evidence/round30/` — census before/after, the adoption receipt over the six admitted rows (`entries=1 … census=ok`, exit 0), the gate selftest (`SELFTEST cases=14 failed=0`), `rows-opened.tsv` (S081–S086 with `recheck=180d`), the C2 counter receipt (`checks=5 defects=0`), the hardened-counter control and the landing receipt. Its `quote-mode-six-rows.txt` (sha256 `63aa8ced…e847`) is the round's quote-mode run over the six rows: S083 and S085 are `REFUSED … absent`, and its opening `ls: cannot access '/tmp/r30fx-c3cli/cap/…'` lines record that the S081/S082/S084 source captures were absent when it ran (see `corpus/lessons/round-30.md` §Sources opened this round for the row quotes themselves).
- `evidence/round31/` — census and adoption after (`cited_rows=3 … census=ok`), C1 counter (`checks=6 defects=0`), C2 after states (`checks=10 defects=0`), gate selftests, the two quote-mode receipts (plain and `--url-map` bound, `located=7 found=7 overlong=0`), the neutered-gate failure-capability control, and `gate-cli-exits.txt` (regenerated round 32 from the committed C3 fixtures).
- `evidence/round32/` — the C1 counter (`checks=6 defects=0`), the refusing adoption gate (`census=fail`, exit 1 — the S094/S097/S101/S102 refusals), the C2 draft-state receipt (`checks=7 defects=5`, red on purpose), and `catalogs/` with the bounded HF/OpenRouter raw response bodies plus `SHA256SUMS`.
- `evidence/round33/` — census after, adoption after (`checks=8 defects=0`, exit 0), the C2 defect counter (`checks=6 defects=0`), and `catalogs/` (`hf.raw.json`, `or.raw.json`, `after.txt` recording `hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0`, `SHA256SUMS`).

---

### Round-34 evidence

| Dir | Contents |
|---|---|
| `evidence/round34/` | Round-34 SOURCES census before/after receipts; no corpus rows were admitted. |


### Round-35 evidence

- `evidence/round35/tb2-eval/` — the six pinned `protein-assembly` files (re-fetched 2026-10-25, byte-identical to the round-34 captures) with `SHA256SUMS`.
- `evidence/round35/tb2-grader-probe.txt` — receipt of `plans/tb2_grader_probe.py` (18 frozen cases; re-run and byte-compared by `plans/round35_c1_verify.py` V5).
- `defects.jsonl` + `plans/defect_ledger.py` — the persistent routed-defect ledger (round-34 D1–D5), re-run at every tip.
- Correction (round-35 falsify wave): the coverage-map bullet's "a one-residue subprotein error fails with the order message" holds for donor/DHFR/acceptor/SNAP only (a FLAG error fails the start assertion), and the longest passing gBlock is 2768 nt, not 2766; see the entry's `## Errata`.
- Correction (round-35 falsify wave, `F35RevReadme` F1): the §Frontier round-35 sub-bullet's "reads and executes … `tests/test.sh`" overstates — only the `test_gblock` function from `tests/test_outputs.py` was executed; `tests/test.sh` was read, not run.

### Round-36 evidence

- `evidence/round36/tb2-regex-log/` — the five pinned `regex-log` files (`test_outputs.py`, `test.sh`, `instruction.md`, `task.toml`, `solve.sh` = the task oracle) with `SHA256SUMS`; `test_outputs.py`, `test.sh` and `instruction.md` are rows S108, S109, S110.
- `evidence/round36/regex-log-probe.txt` — receipt of `plans/regex_log_probe.py` (24 frozen cases, `cases=24 observed_pass=8 observed_fail=16 mismatches=0`; re-run and byte-compared by `plans/round36_c2_verify.py` W5).
- `evidence/round36/regex-log-probe-first-run.txt` + `evidence/round36/regex-log-dry-cases-freeze.txt` — the pre-Amendment-1 run (two assertion texts carry the `mkdtemp` path) and the frozen `--dry` case table, retained as disclosure per Amendment 1.
- `evidence/round36/toolathlon-package.md` — the committed round-35 package copy the round-36 claims compute C1's R35-D4 recount from (`13 + 23 + 1 = 37`, denominator 38; `plans/round-36-claims.md` §C1).
- `defects-round35.jsonl` — the four routed round-35 defects (R35-D1..D4) as ledger rows, re-run at every tip by `plans/round36_c1_verify.py`.
- `../plans/pkg_gate.py` — the hardened package gate round 36 lands (C1; contract in `plans/round36_c1_verify.py`, package definition `plans/pkg-spec-r35.json`).

### Round-37 evidence

- `evidence/round37/tb2-git-webserver/` — the six pinned `configure-git-webserver` files (`test_outputs.py`, `verify.sh`, `test.sh`, `instruction.md`, `task.toml`, `solve.sh` = the task oracle) with `SHA256SUMS`; `test_outputs.py`, `verify.sh` and `instruction.md` are rows S111, S112, S113.
- `evidence/round37/git-webserver-probe.txt` — receipt of `plans/git_webserver_probe.py` (22 frozen cases, `cases=22 observed_pass=9 observed_fail=13 mismatches=0`, a second run byte-equal); `evidence/round37/git-webserver-dry-cases-freeze.txt` — the frozen case table with predictions.
- `evidence/round37/prior-art/` — the captured body and metadata of TB2.1 issue #133 (row S114) with `SHA256SUMS`.
- `evidence/round37/anchor-captures/` — byte copies of the four pinned upstream files whose digests rows S070, S072, S073 and S074 state, so `plans/anchor_digest_check.py` can re-check them (`PROVENANCE.md`, `SHA256SUMS`).
- `../plans/battery37/` — the single-defect fixture battery for `plans/round37_c1_verify.py` (55 frozen gate mutants against `plans/pkg_gate.py`).

### Round-38 evidence

- `evidence/round38/tb2-build-pmars/` — the five pinned `build-pmars` files (`test_outputs.py`, `instruction.md`, `test.sh`, `task.toml`, `solve.sh` = the task oracle) with `SHA256SUMS`; `test_outputs.py` and `instruction.md` are rows S115, S116.
- `evidence/round38/build-pmars-probe.txt` — receipt of `plans/build_pmars_probe.py` (22 frozen cases, `cases=22 observed_pass=7 observed_fail=15 mismatches=0`, a second run byte-equal); `evidence/round38/build-pmars-dry-cases-freeze.txt` — the frozen case table with predictions and `violates=` tags.
- `../plans/battery38/` — fixtures for `plans/round38_c1_verify.py` (22 frozen gate mutants N01–N22, attributed kill rule); `../plans/mutant_direction_check.py` — checks each frozen mutant's declared kill direction against the battery.

### Round-39 evidence

- `evidence/round39/tb2-git-leak-recovery/` — the seven pinned `git-leak-recovery` files (`test_outputs.py`, `instruction.md`, `challenge-setup.sh`, `solve.sh` = the task oracle, `test.sh`, `task.toml`, `Dockerfile`) with `SHA256SUMS`; `test_outputs.py` and `instruction.md` are rows S117, S118.
- `evidence/round39/git-leak-probe.txt` — receipt of `plans/git_leak_probe.py` (25 frozen cases, `cases=25 observed_pass=13 observed_fail=12 mismatches=0`, a second run byte-equal); `evidence/round39/git-leak-dry-cases-freeze.txt` — the frozen case table with predictions and `violates=` tags.
- `../plans/battery39/` — fixtures for `plans/round39_c1_verify.py` (7 frozen gate mutants M01–M07, witnessed directions, modules built out of process).

### Round-40 evidence

- `evidence/round40/tb2-db-wal-recovery/` — the eight pinned `db-wal-recovery` files (`test_outputs.py`, `instruction.md`, `solve.sh` = the task oracle, `test.sh`, `task.toml`, `Dockerfile`, `main.db`, `main.db-wal.encrypted`) with `SHA256SUMS`; `test_outputs.py` and `instruction.md` are rows S119, S120.
- `evidence/round40/db-wal-probe.txt` — receipt of `plans/db_wal_probe.py` (28 frozen cases, `cases=28 observed_pass=8 observed_fail=20 mismatches=0`, `regrade cases=28 differ=0`, a same-process second call); `evidence/round40/db-wal-dry-cases-freeze.txt` — the frozen case table (`--dry`).
- `../plans/battery40/` — fixtures for `plans/round40_c1_verify.py` (21 frozen mutants of the three tripwire tools `anchor_digest_check.py`, `ledger_tip.py`, `order_check.py`; attributed kill rule; modules built in a pid-namespaced child).

### Round-41 evidence

- `evidence/round41/tb2-constraints-scheduling/` — the ten pinned `constraints-scheduling` files at terminal-bench-2 `2fd12b88` (`test_outputs.py`, `instruction.md`, `test.sh`, `solve.sh` = the task oracle, `task.toml`, `Dockerfile`, `README.md`, and the three input calendars `alice_calendar.ics`, `bob_calendar.ics`, `carol_calendar.ics`) with `SHA256SUMS`; `test_outputs.py` and `instruction.md` are rows S122, S123, and the three calendars carry the grader's own pinned digests.
- `evidence/round41/constraints-probe.txt` — receipt of `plans/constraints_probe.py` (25 frozen cases, `cases=25 observed_pass=6 observed_fail=19 mismatches=2`, `regrade cases=25 differ=0`); `evidence/round41/constraints-dry-cases-freeze.txt` — the frozen case table (`cases=25 predicted_pass=6 predicted_fail=19`, with `violates=` tags).
- `evidence/round41/pr245-body.md` — the captured TB2.1 PR #245 body for row S124 (`state=closed merged=false closed_at=2026-10-08T19:02:36Z`); its 55-fixture patch is quoted as the PR body's claim, never executed.
- `../plans/battery41/` — fixtures for `plans/round41_c1_verify.py` (`BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=23 killed=23 survived=0`).

### Round-42 evidence

- `evidence/round42/tb2-circuit-fibsqrt/` — the nine pinned `circuit-fibsqrt` files (`test_outputs.py`, `instruction.md`, `test.sh`, `solve.sh` = the task oracle, `task.toml`, `Dockerfile`, `README.md`, `sim.c`, and the shipped example `gates.txt`) with `SHA256SUMS`; `test_outputs.py`, `instruction.md` and `sim.c` are rows S125–S127.
- `evidence/round42/fibsqrt-probe.txt` — receipt of `plans/fibsqrt_probe.py` (16 frozen cases, `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0`); `evidence/round42/fibsqrt-dry-cases-freeze.txt` — the frozen case table (`cases=16 predicted_pass=7 predicted_fail=9`).
- `../plans/battery42/` — fixtures for `plans/round42_c1_verify.py` (`BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=14 killed=14 … unattributed=0`, attributed kill rule).

---

### Round-43 evidence

- `evidence/round43/tb2-feal-differential-cryptanalysis/` — the twelve pinned `feal-differential-cryptanalysis` files at terminal-bench-2 `2fd12b88` (`test_outputs.py`, `setup.py`, `feal_module.c`, `feal.c`, `feal.h`, `feal.py`, `instruction.md`, `solve.sh` = the task oracle, `test.sh`, `task.toml`, `Dockerfile`, `README.md`) + `SHA256SUMS`; fetched by the L1 2026-10-26 18:40 -03; rows S129–S134 pin six of them.
- `evidence/round43/feal-probe.txt` — receipt of `plans/feal_probe.py` (12 frozen cases, `cases=12 observed_pass=8 observed_fail=4 mismatches=0`, `regrade cases=12 differ=0`, each regrade a fresh harness process); `evidence/round43/feal-dry-cases-freeze.txt` — the frozen case table (`--dry`).
- `../plans/battery43/` — fixtures for `plans/round43_c1_verify.py` (9 frozen near-variant mutants of `anchor_digest_check.py` and `order_check.py`; span- and value-attributed kill rule).

### Round-44 evidence

- `evidence/round44/tb2-feal-linear-cryptanalysis/` — the eleven pinned `feal-linear-cryptanalysis` files at terminal-bench-2 `2fd12b88` (`test_outputs.py`, `instruction.md`, `test.sh`, `solve.sh` = the task oracle, `task.toml`, `Dockerfile`, `README.md`, `gen.py` = the generator the image seeds from and deletes (`Dockerfile:11` runs it, `:13-14` `rm orig_plaintexts.txt` / `rm gen.py`), `decrypt.c`, `feal.c` = the agent-visible cipher, and the repository dotfile captured as `gitignore`) + `SHA256SUMS`; fetched by the L1 2026-10-26 20:10:09 -03; rows S138–S146 pin nine of them (`feal.c` and `gitignore` are captures, not rows).
- `evidence/round44/feal-linear-probe.txt` — receipt of `plans/feal_linear_probe.py` (14 frozen cases, `cases=14 observed_pass=8 observed_fail=6 mismatches=0`, `regrade cases=14 differ=0`); `evidence/round44/feal-linear-dry-cases-freeze.txt` — the frozen case table (`cases=14 predicted_pass=8 predicted_fail=6`, with `violates=` tags and the four `TAG` lines that name `instruction.md:7`, `:8`, `:10`).
- `../plans/battery44/` — fixtures for `plans/round44_c1_verify.py` (span- and value-attributed kill rule, fences F1–F6): 10 modules, 33 fixtures from wave seats `R44BatU5a`…`R44BatU14b`; landed `2a263e5a`.

### Round-45 evidence

- `evidence/round45/tb2-password-recovery/` — the nine pinned `password-recovery` files at terminal-bench-2 `2fd12b88` (`tests/test_outputs.py`, `instruction.md`, `tests/test.sh`, `environment/setup.sh`, `environment/Dockerfile`, `README.md`, `solution/solve.sh` = the task oracle, `task.toml`, and the repository dotfile captured as `gitignore`) + `SHA256SUMS`; fetched by the L1 2026-10-26 23:05 -03; rows S149–S156 pin eight of them (`gitignore` is a capture, not a row).
- `evidence/round45/password-recovery-probe.txt` — receipt of `plans/password_recovery_probe.py` run under the `bwrap` envelope (`envelope.sh`; 16 frozen cases, `cases=16 observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16 differ=0`, envelope `local_bin_content` unchanged); `evidence/round45/password-recovery-dry-cases-freeze.txt` — the frozen case table with `violates=` tags.
- `evidence/round45/gate-call.txt`, `evidence/round45/counter-a-run.txt`, `evidence/round45/counter-b-run.txt`, `evidence/round45/frozen-digests.txt` — the execute-phase conformance receipts called for by `plans/round-45-claims.md`.
- `../plans/refusals45/` — hostile fixture classes for `plans/round45_c1_verify.py`: `f1_truncated_git.py`, `f3_abbrev.py`, `f4_fifos.py`, `f5_alternates.py`, `f6_move.py`, `f7_commondir.py`, `f8_worktree.py`, `f9_describe.py`, `f10_laneinclude.py`; `../plans/battery45/` — the 33 honest fixtures.
