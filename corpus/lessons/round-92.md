author: kengaku (L1 KengakuR92, hyaku run 15 attempt 1)

# Kengaku round 92 — lesson

Lane `kengaku-shokunin`, branch `master`. Base `4ba56182`; frozen claims and case table commit A
`96f249e0` (`plans/round-92-claims.md`, `plans/round92-cases.json`); instruments B `4f6b3c52` and
pin-ledger refresh B2 `f0018773` (the B2-style disclosed move, before any scoring); official
receipt, ledger flip 35→36, SOURCES S283–S289 and the M14 correction row C `42bd5104`; registry
word-count corrections C2 `d1ccf56d` (the F2 counter caught them, see M1); probe-tool pin D
`b62ea270` (the C1 counter's own L8 leg caught the missing pin, see M2). Wave evidence:
`.ufo/waves/round-92/w1/`; L1 transcripts under `.ufo/waves/round-92/L1/`.

## Gate

Candidates opened this round (CORPUS rule 1: each row written only after its source was opened
here, with URL, access date and a located quote; every fetch HTTP 200 on 2026-11-05).

| candidate | decision | access | located quote and location | reason | flip |
|---|---|---|---|---|---|
| S283 `llm-inference-batching-scheduler/tests/test_outputs.py` @ `2fd12b88` (member replay only) | **admit** (tier A) | 2026-11-05, raw.githubusercontent.com, HTTP 200, 14194 B, sha256 `80b06b7c…d96ffa`, byte-identical to the lane capture | line 91: `def test_output_files_exist() -> None:` (4 words) | the captured module defines the six named test functions (files-exist, integrity, schema, feasibility, coverage, performance) over staged `/app/task_file` files, and pins both input hashes at `:25`; it is the sole source of the ten frozen predicted vectors (`plans/round92-cases.json`) | a claim about the TB2 harness or a real submission would need its own receipt; this row is member replay only |
| S284 `tests/cost_model_for_tests.py` @ `2fd12b88` (member replay only) | **admit** (tier A) | 2026-11-05, same base URL, HTTP 200, sha256 `d3e810a9…c9ab9`, byte-identical to the lane capture | line 35: `def align(x: int, g: int) -> int:` (7 words) | stdlib-only; the grader imports it relatively, so the probe must import the package; it decides the five threshold legs the full-pass case needs | a claim about the task's shipped `scripts/cost_model.py` (different bytes) would be its own row |
| S285 the two task input-data files (member replay only) | **admit** (tier A, dataset) | 2026-11-05, raw.githubusercontent.com, HTTP 200; sha256 `8b3cf1e2…f7de` and `e15e2d4c…5cb5`, byte-identical to the lane captures | `requests_bucket_1.jsonl:1` quote `"request_id": "r-000000", "prompt_len": 51, "gen_len": 19}` (6 words) | 800 requests per bucket; the grader itself pins their hashes at `:25`, so the tampered-input case flips exactly one leg | a workload-change claim would need a new fetch at a new revision |
| S286 `tests/test.sh` @ `2fd12b88` (verifier wrapper) | **reject** | 2026-11-05, same base URL, HTTP 200, sha256 `005f9803…53ca`, byte-identical to the lane capture | line 5: `# Install curl` (3 words) | the wrapper installs curl and uv over the network (apt-get, uvx), which the offline replay forbids; it adds no grader semantics beyond S283 | a claim about verifier-harness reward semantics opened as its own replay with the network legs pinned |
| S287 supersedes S265 (capture pin, round-81 receipt) | **admit** (tier A, own-work) | 2026-11-05, `sha256sum corpus/evidence/round81/log-summary-date-ranges-probe.txt` → `7c8d3f56…f81e78` | line 1: `# tb2 log-summary-date-ranges grader probe (round 81)` (7 words) | the routed round-91 defect 9: the blind-spot chains carried no capture pins; the pin lands as a supersede row per CORPUS rule 2 | the quote verification failing at the cited line would refuse the row |
| S288 supersedes S266 (capture pin, log-summary instruction) | **admit** (tier A, own-work) | 2026-11-05, capture fetched at the pinned revision, sha256 `c1d4516a…3484` | line 9: `Write a CSV file /app/summary.csv with the following structure (including the header):` (12 words) | the log-summary half of the S261 chain, byte-verified | same |
| S289 supersedes S288 (capture pin, vulnerable-secret instruction) | **admit** (tier A, own-work) | 2026-11-05, capture fetched at the pinned revision, sha256 `d43c72e6…7a2f` | line 1: `The goal is to extract this secret key and save it to \`/app/results.txt\`.` (13 words) | the vulnerable-secret half; its own row because `row_defects` verifies every quote of a row against ONE capture file (`sorted(caps)[0]`), so two captures cannot share a row | same |

Round-start census (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
kengaku`): exit 0, `kengaku ok`, 274 rows. Round-end census: exit 0, 281 rows.

## Mistakes

Class · evidence pointer · captured-by · fix.

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | **number-drift (word counts)** | the first C-commit registry rows carried three miscounted quote-word cells: S283 said 5 (actual 4), S285 said 9 (actual 6), S287 said 9 (actual 7); `plans/round92_f2_counter.py` printed `PIN-DEFECTIVE S287 … kinds=['words']` and `live=3` (transcript `.ufo/waves/round-92/L1/`), red | QUALITY row-verification (the pins exist to catch exactly this); the counter caught it before the F2 verdict was recorded | corrected in the same round at C2 `d1ccf56d` with the counter's red output committed as the witness; disclosed here rather than rewritten silently — the three cells were miscounts of quoted bytes, which is the defect class the pins exist to catch |
| M2 | **landing (incomplete pin set)** | the C1 counter's L8 leg failed red at the C commit: `DEFECT L8 probe pin unreadable` — `plans/round92_bs_probe.py` had no sha entry in `plans/counter-pins-r91.json`; the counter refused to pass with an unpinned probe (transcript `c1-tip.txt`) | the counter's own fail-closed leg (L8); QUALITY Q-set on pinned tools | the pin landed as commit D `b62ea270` before any green measurement; disclosed as the fail-closed loop working, not as a silent repair |
| M3 | **frozen-text staleness by legitimate growth** | the C2 claims predicate (frozen at A) says the M9 green leg prints `PINS checked=17 matched=17`; commit D grew the ledger to 18 entries (the probe pin), so the conformance counter's green leg is measured at the C2 tip `d1ccf56d` (17 entries), named in LOG.md, not at D | the frozen-rule discipline: the stale string is reported, not repaired; the claims text also fixed "measured tips are named in LOG.md" | the C2 measured tip is `d1ccf56d`; the C1 measured tip is `b62ea270`; both named here and in LOG.md |
| M4 | **frozen-text misprediction (BASE through v2's eyes)** | `plans/round-92-claims.md` (C3 predicate) predicted the v3 gate at BASE to print `pending=1` with the three `override-unjustified` DEFECTs; the measured BASE run prints `pending=0` and no override DEFECTs — the chain-aware resolver (the fix itself) runs at BASE too, and the only BASE defect is `check-failed R82-V8` (the M6 clone-path defect failing in the worktree, the red-before for its own repair). Also the round-shape line says 3 executor; the dispatched wave has 4. | the frozen-rule discipline (report, never repair); the claims' own do-nothing control anticipated it ("the chain-aware state at BASE already resolves pending to 0") | disclosed here and in the report; the decisive v2-at-tip control (`.ufo/waves/round-92/L1/v2-at-tip.txt`: `freeze=refused oldest_pending_round=82 pending=1` + the three override DEFECTs at the TIP) demonstrates the code fix is what changed the verdict |
| M5 | **inherited leftover** | `.ufo/waves/round-91/gate-f1/wrong-line` — an untracked round-91 fixture leftover in the lane tree at round start | §5 inherited-state sweep | discarded (a throwaway wrong-line fixture, regenerated by the F2 counter whenever needed); named here per protocol |
| M6 | **recursive battery hang** | the first tip gate run died at 600 s: each battery fixture child re-entered the full battery because `in_child_mode` required `--selftest` in the parent argv, which a live-gate parent does not carry (transcript `c3-tip.txt`, TimeoutExpired) | the tip run itself; the standalone selftest passed because its parent IS a `--selftest` run | child-proof relaxed to gate-parent membership (commit E5 `a0c7438a`): every chain of children roots at a default-path gate or a `--selftest` run, and the battery runs at that root — no CLI skip channel exists |
| M7 | **the gate's own tip run found its last two defects** | at E5 the tip gate reported exactly two DEFECTs: (a) `line 125: R82-F1: source must read <path>:<line>` — the invalid-chain branch read the valid-row cache instead of walking the chain, so the R82-F1 prose-source row stayed pending; (b) `check-failed R82-V8 rc=1 'CHECK v8 fail'` — the gate's check runner fell back to the WORKTREE's parent for the fleet root, so the M6 fix was inert inside the worktree (transcript `c3-tip.txt` at E5, committed as the red witness) | the gate's own predicate path; both are fail-closed catches, not silent passes | (a) invalid-chain branch walks `chain_end(sid)`; (b) `run_check` takes the fleet root from the lane's parent / `SHOKUNIN_ROOT` (commits E6 `b72c83e9`, E7 `dd48027f`; selftest 10/10 after each) |

## Honest limits of this round's evidence

- The C1 replay grades lane-authored fixtures (the plans are this lane's own packer output; the
  case table's vectors were confirmed by a pre-freeze scratch dry-run and then held exactly in
  the official receipt). It describes the captured grader bytes on this host's toolchain, not
  Terminal-Bench's harness or a real submission.
- The p95 margin on the full-pass plan is thin (`2.088e5` against `2.1e5` on bucket 2) — the
  measurement is deterministic on this host's python/CostModel, so the receipt reproduces, but
  the margin is not evidence of headroom.
- The disclosed in-tree-pin residual (checker + ledger rewritten in one commit still passes)
  remains open under L0 `kengaku | round-91`; this round does not close it.
- The gate v3's `shokunin.conf` lane-id rule reads the fleet conf live (it is not in the lane
  repo at any revision); a conf edit mid-run would change the verdict, which the gate reports
  as `CouldNotEvaluate` only if the file is unreadable, not if its content changes.
