# Kengaku round 92 — lesson (SKELETON, drafts only; the L1 integrates)

Lane `kengaku-shokunin`, branch `master`. Base `4ba56182`; frozen claims and case table commit A
`96f249e0` (`plans/round-92-claims.md`, `plans/round92-cases.json`); instruments B `4f6b3c52`;
pin-ledger refresh B2 `f0018773` (the disclosed B2-style move, before any scoring). Wave evidence:
`.ufo/waves/round-92/w1/`.

This skeleton supplies the `## Gate` table (one row per candidate S283–S289) and the empty
`## Mistakes` and `## Honest limits` sections, which the L1 fills from the wave's measured
outcomes. Nothing else in the lane was written by this seat.

## Gate

Candidates opened this round (CORPUS rule 1: each row written only after its source was opened
here, with URL, access date and a located quote; every fetch HTTP 200 on 2026-11-05).

| candidate | decision | access | located quote and location | reason | flip |
|---|---|---|---|---|---|
| S283 `llm-inference-batching-scheduler/tests/test_outputs.py` @ `2fd12b88` (member replay only) | **admit** (tier A) | 2026-11-05, `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/llm-inference-batching-scheduler/tests/test_outputs.py`, HTTP 200, 14194 B, sha256 `80b06b7c…d96ffa`, byte-identical to the lane capture | line 91: `def test_output_files_exist() -> None:` (4 whitespace-split words) | the captured module defines the six named test functions (files-exist, input integrity, schema, feasibility, coverage, performance) over the staged `/app/task_file` files and pins both input hashes at `:25`; it is the sole source of the ten frozen predicted vectors (`plans/round92-cases.json`) | a claim about the TB2 harness or a real submission would need its own receipt; this row is member replay only |
| S284 `llm-inference-batching-scheduler/tests/cost_model_for_tests.py` @ `2fd12b88` (member replay only) | **admit** (tier A) | 2026-11-05, `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/llm-inference-batching-scheduler/tests/cost_model_for_tests.py`, HTTP 200, 17396 B, sha256 `d3e810a9…c9ab9`, byte-identical to the lane capture | line 35: `def align(x: int, g: int) -> int:` (7 whitespace-split words) | stdlib-only; the grader imports it relatively, so the probe must import the package; it decides the threshold legs the full-pass case needs | a claim about the task's shipped `scripts/cost_model.py` (different bytes) would be its own row |
| S285 the two task input-data files (member replay only) | **admit** (tier A, dataset) | 2026-11-05, `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_1.jsonl` and `…_2.jsonl`, HTTP 200 both, 48964 B and 50219 B; sha256 `8b3cf1e2…f7de` and `e15e2d4c…5cb5`, byte-identical to the lane captures | `requests_bucket_1.jsonl:1` quote `“"request_id": "r-000000", "prompt_len": 51, "gen_len": 19}”` (6 whitespace-split words) | 800 requests per bucket; the grader itself pins their hashes at `:25`, so the tampered-input case flips exactly one leg | a workload-change claim would need a new fetch at a new revision |
| S286 `llm-inference-batching-scheduler/tests/test.sh` @ `2fd12b88` (verifier wrapper) | **reject** | 2026-11-05, `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/llm-inference-batching-scheduler/tests/test.sh`, HTTP 200, 721 B, sha256 `005f9803…53ca`, byte-identical to the lane capture | line 5: `# Install curl` (3 whitespace-split words) | the wrapper installs curl and uv over the network (apt-get, uvx), which the offline replay forbids; it adds no grader semantics beyond S283 | a claim about verifier-harness reward semantics opened as its own replay with the network legs pinned |
| S287 supersedes S265 (capture pin, round-81 receipt) | **admit** (tier A, own-work) | 2026-11-05, `sha256sum corpus/evidence/round81/log-summary-date-ranges-probe.txt` → `7c8d3f56…f81e78`; the capture was fetched live at the pinned revision and is byte-identical to the tracked file | line 1: `# tb2 log-summary-date-ranges grader probe (round 81)` (7 whitespace-split words) | the routed round-91 defect 9: the blind-spot chains carried no capture pins; the pin lands as a supersede row per CORPUS rule 2 | the quote verification failing at the cited line would refuse the row |
| S288 supersedes S266 (capture pin, log-summary instruction) | **admit** (tier A, own-work) | 2026-11-05, capture fetched at the pinned revision, sha256 `c1d4516a…3484`, byte-identical to the tracked file | line 9: `Write a CSV file /app/summary.csv with the following structure (including the header):` (12 whitespace-split words) | the log-summary half of the S261 chain, byte-verified | same |
| S289 supersedes S288 (capture pin, vulnerable-secret instruction) | **admit** (tier A, own-work) | 2026-11-05, capture fetched at the pinned revision, sha256 `d43c72e6…7a2f`, byte-identical to the tracked file | line 1: `The goal is to extract this secret key and save it to `/app/results.txt`.` (13 whitespace-split words) | the vulnerable-secret half; its own row because `row_defects` verifies every quote of a row against ONE capture file (`sorted(caps)[0]`), so two captures cannot share a row | same |

Round-start census (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
kengaku`): exit 0, `kengaku ok`, 274 rows. Round-end census: recorded in LOG.md after
S283–S289 landed.

### Gate-table notes for the L1

- **The S283 and S287 word counts in the seat brief are wrong** (5 and 9); the mechanical
  whitespace-token counts are 4 and 7. The brief's counts are `live` defects under
  `plans/anchor_line_check.py` (`ROW S283 state=live defects=words:1`, `ROW S287 state=live
  defects=words:1`, exit 1). The counts in the table above are the correct ones and match the
  lane's landed rows.
- **S285 carries one located quote, not two.** The brief asked for a line-1 quote from each of
  the two input-data files; the checker verifies a row's quotes against one capture
  (`sorted(caps)[0]`), so a second quote naming `requests_bucket_2.jsonl` fails with a `line`
  defect. Bucket 2's sha256 is named in the same anchor cell without a second line-cited quote.
  This is the constraint S289's own `teaches` cell records.

## Mistakes

*(empty — the L1 fills this section from the wave's measured outcomes.)*

Class · evidence pointer · captured-by · fix. Each fix is named with the evidence it was shown
against; fixes that are not yet able to fail are routed, not claimed.

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
|  |  |  |  |  |

## Honest limits of this round's evidence

*(empty — the L1 fills this section from the wave's measured outcomes.)*

## M14 correction row (draft for `corpus/routed-findings.jsonl`)

One JSON line, append-only. It corrects the disposition *word* on the judgment close
`R84-V9-R91`; the close itself stands, and the original row is not edited.

```json
{"id": "R84-V9-R91-R92", "class": "gate-blind-spot", "source": "corpus/lessons/round-91.md:1", "opened_round": 92, "status": "closed", "supersedes": "R84-V9-R91", "owner": "kengaku", "disposition": "correction", "close": "Correction row (round 92, routed round-91 spot-check defect 8): the disposition word `fixed-verified` on the judgment close R84-V9-R91 overstates a judgment; the close itself stands (the freeze defines its before against an existing revision, which the spot-check agreed). The original row is not edited (append-only); this row corrects the wording only.", "blocker": null, "check": "grep -q 'R84-V9-R91' corpus/routed-findings.jsonl", "verified_at": "2026-11-05"}
```

This draft is byte-identical to the lane's landed M14 row (`corpus/routed-findings.jsonl:254` at
HEAD), and appending it to the BASE ledger reproduces the landed ledger file byte-for-byte
(`cmp`, 254 lines, exit 0).

Two facts the L1 should know about this row, both measured:

1. **It resolves a two-level chain (M13).** With the row absent the gate prints
   `resolutions=74`; with it present, `resolutions=75`. Both verdicts are `freeze=admitted`
   (`pending=0`, `PREDICATE R92-C3 pass`, rc 0) — the row is a wording correction, not a
   verdict-changing row, so its absence does not break the freeze.
2. **Its `check` is satisfied by the row's own presence.** `grep -q 'R84-V9-R91'
   corpus/routed-findings.jsonl` matches the M14 row's own `id` (`R84-V9-R91-R92`), its own
   `supersedes` value and its own `close` text. Probed: with the predecessor row `R84-V9-R91`
   deleted from the ledger, the check still exits 0. The gate still refuses that tree, but for a
   different reason — `DEFECT supersedes-unknown R84-V9-R91-R92 -> R84-V9-R91`, `freeze=refused`,
   `PREDICATE R92-C3 fail`, rc 1. So the chain link is what catches a missing predecessor, not
   the row's own check. Reported as a finding; not repaired here (the row's `check` is named in
   the frozen C-commit and is not this seat's to change).
