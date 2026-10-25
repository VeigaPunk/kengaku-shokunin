# FSeparability — two-way causal separation falsification (round 28)

Seat: KengakuR28.FSeparability (author-side). Scope: falsify C1↔C2 causal separation by
reviewing/rerunning `plans/fixtures/r28/acceptance.py` in own scratch; check row/cell
partitions on shared SOURCES.md, baseline35 knowledge, new-entry exclusion; verify M65 is an
only-delta repair and not an S038-alone falseclaim. Read-only over production; all writes
under `.ufo/waves/round-28/scratch/FSeparability/` (acceptance outdir + own controls).

## Executed evidence

- Full acceptance rerun (explicitly permitted): `python3 plans/fixtures/r28/acceptance.py
  --root <lane> --out .ufo/waves/round-28/scratch/FSeparability/acceptance` → **exit 0**,
  11 recorded commands all at expected exits (incl. two expected exit-1 reds). Scratch
  `acceptance.json` and `registry-only-delta.json` retained. Baseline export went to /tmp
  (TemporaryDirectory, auto-removed); no lane/VCS writes by the harness beyond my outdir.
- **Replay parity**: my rerun's `registry-only-delta.json` is byte-identical to the build
  receipt `corpus/evidence/round28-calibration/build-acceptance/registry-only-delta.json`
  (both sha256 081e176ec42b9d08f271a99babd82aca31036b18e22adc6ba691b5b6b6cc6263).
- Instrument digests measured by my rerun == `candidate-freeze.json` pins
  (audit f72a8569…, registry 41561dfb…, state_check 5db1eb78…). Candidate draft sha256
  77e19d5b… confirmed at `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`.

## Partition checks (independent recomputation, not just assert trust)

- **Row/cell partition on shared corpus/SOURCES.md** (BASE b9b24796 → HEAD 18b19226):
  exactly two frozen rows changed — S038 cells {status, used_by}, S050 {used_by}; 6 added
  rows S061–S066; 0 removed; every other row (frozen and non-frozen) byte-identical cells.
  Matches lesson table lines 62–68. Acceptance's allowed-index set (7,9,10 =
  status/recheck/used_by) has unused slack at index 9 — no recheck cell actually changed;
  slack is conservative, not a false claim.
- **Baseline35 knowledge**: all 35 `population.json` knowledge_paths exist at BASE
  (no `knowledge_missing` in baseline-red output). Literal `S[0-9]{3,}` citing sets for the
  frozen13 are **identical** BASE vs HEAD (12 links both, S060 uncited both). Round-28 edits
  to two baseline35 files added only mentions of new rows (S064/S065/S066), outside frozen13
  → zero effect on C2 counters or findings. C2 owns mutable cells; C1 owns new rows/new
  knowledge — Amendment1 ¶4 partition holds exactly.
- **New-entry exclusion**: `corpus/knowledge/webarena-task-spec-audit.md` does not exist at
  HEAD and is not in `knowledge_paths`; the draft lives in `.ufo/…/drafts/` outside the
  scanned set. C2 cannot observe the candidate pre- or post-admission (frozen paths only).

## Two-way separation results

- **C2 survives C1 absence**: `registry-s038-only-delta-green` ran on the BASE export +
  current population + only the S050 used-by and S038 status/used-by cell deltas — no
  `plans/fixtures/r28/webarena`, no S061–S066 rows, no round-28 knowledge/lesson — →
  **exit 0, finding_count 0, reference_links 12**, per-source projection (status, citing,
  missing) equal to `registry-current`. C2 verdict needs none of C1's artifacts.
- **C1 survives C2 reversion**: `audit-without-c2` ran the same baseline export (baseline
  SOURCES/knowledge/lessons, i.e. all C2 repairs reverted — and in fact a superset revert
  that also strips C1 corpus additions) with only the webarena fixture injected → metrics
  byte-equal to current: 812 tasks/812 distinct IDs/5 evaluator-type sets/27 strata/16
  selected (IDs 389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399)/651 targets;
  selected_task_ids equal. C1 depends only on pinned fixtures + script — control: audit on
  the bare baseline (no fixture) → exit 2 `input_missing`.
- Oracle parity: `benchmark_oracle`/`registry_oracle` outputs equal to production counters.

## M65 falsification chain (honest only-delta, verified)

| state | exit | mismatch sources | findings |
|---|---|---|---|
| original baseline + frozen population | 1 | {S038, S050} | cited_not_mined(S038), missing_used_by(S038), missing_used_by(S050) |
| + S050 used-by only | 1 | {S038} | as receipt |
| + S038 status/used-by | 0 | {} | 0, links 12 |

Own additional falsification control (baseline export in
`scratch/FSeparability/s038-only-control`, receipt `control-s038-only.json`): **S038
status/used-by repair applied alone to the ORIGINAL baseline → exit 1, mismatch {S050}.**
So the red→green delta is S038's allowed-cell repair *given* S050's corrective used-by
index; an "S038-alone fixes baseline" claim would be false, and the claims/lesson do not
make it — the experiment's (a)/(b)/(c) staging exactly prevents it (Amendment1 ¶4).

## Residual notes (not defects)

- `audit-without-c2` is a superset revert (whole baseline corpus), stronger than a C2-only
  revert; separation still follows since C1's sole data dependency is the injected fixture.
- `green` vs `current` projection equality covers source/status/citing_files/missing_used_by;
  `used_by` itself is not tuple-compared, but finding_count==0 + reference_links equality
  plus my independent citing-set recomputation close the gap.
- `run()` truncates `commands.json`/stdout into `--out`; reruns in the same dir overwrite —
  receipt retention is per-run. Baseline tempfile path appears in commands.json.
- Pre-admission execution: harness needs only landed build artifacts; canonical candidate
  absent at HEAD is expected and consistent with the deferred gate.

## VERDICT: PASS

Two-way causal separation verified end-to-end: C2 green with all C1 additions absent; C1
metrics identical with all C2 repairs reverted; partitions are row/cell-precise with new
rows and new-entry exclusion confirmed; M65 is a genuine only-delta repair staged so S038
alone cannot be credited, corroborated by an independent S038-alone control staying red.
