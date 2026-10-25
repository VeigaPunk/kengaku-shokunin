# Round-10 fleet — integrator notes (L1 provenance)

Convention (round 9): L2 artifacts are committed **verbatim**; corrections and
integration decisions live in this file, never as edits to an L2's text.
10 L2s, one batched `task` call; routes per `../../../MISSION.md`
(scout/executor/scribe @m_flash, critic/reviewer/connector/labrat/
mutation-tester @m_zfl per fleet route map). No L2 wrote into the repo;
single integration owner: L1.

## 1. Fleet map — artifact → integration site

| L2 (role) | Artifact (this dir) | Integrated into |
|---|---|---|
| ScoutEndpoint (scout) | `r10-scout-endpoint.md` (+ raw captures `models-34113.json`, `props.json`, `slots.json`) | `PROVINCE.md` served-model row (process-level pin, ceiling closed); `SKILL.md` scope-limit paragraph (q4_0 KV, `--kv-unified`, `--no-context-shift`, custom template); report §routed evidence |
| ScoutWiki (scout) | `r10-scout-wiki.md` | `corpus/knowledge/eval-prior-art-calibration.md` §Status note (#7052 state contested); digest-queue ceiling reclassified in `SCORECARD.md` round-10 rows (queue is external, fetched-and-cited, not llm-wiki-resident) |
| ScoutBench (scout) | `r10-scout-bench.md` | `corpus/knowledge/bench-arena-fresh-run.md` §Errata round 10 (claim C causal chain falsified: `loop.sh` field-count bug; "scrape fails" premise false today); `corpus/knowledge/bench-arena-round7-noise-n25.md` §Errata round 10 (claim D: 97→125 dirs; "(ephemeral)" label corrected) |
| CriticScorecard (critic) | `r10-critic.md` (+ `recompute_r8.py`, `recompute_r9.py`) | `SCORECARD.md` round-10 errata subsection (F1 runnable-count 11→12 wrong at birth; F2 `sha256sum -c` cwd defect; F3 partial freshness-row citation); 30/35 claims REPRODUCE recorded in the round-10 rows |
| ReviewerCites (reviewer) | `r10-review-cites.md` (+ `url-status.txt`) | `SCORECARD.md` depth row (citation resolution 91.2% strict / 98.0% convention ≥90% holds; 20 bullets reproduce; "14 distinct paths" ruled convention-bound — 58 under the finer extractor) |
| ConnectorSiblings (connector) | `r10-connector.md` | `grader.py` conventions (all 5 adoption recommendations — see §3); `PROVINCE.md` round-10 report-outs (kumitate adjacency: `scripts/cite-check.mjs` is a citation-pin gate, not evidence replay; protocol owns any fleet-wide gate standard) |
| LabratSchema (labrat) | `r10-labrat-schema.md` (+ `schema_probe.py`) | `grader.py` special cases confirmed before build: A-MONO/B `want==truth[9]` at turn 1; C-MONO reduced key set; the 2 r9 records parseable only via the brace-regex fallback |
| MutationHarness (mutation-tester) | `r10-mutation-sh.md` (+ `mutate_test.sh` sha256 `ad0511f2…`, `probe_ref.py`, `final-harness.log`) | falsification battery: M0–M3 executed against the landed grader, 4/4 as expected; also caught the first-version grader defect (§2) — failing-before evidence in `r10-mutation-sh.md` §7.1 |
| ExecutorDocs (executor) | `r10-drafts.md` | `SKILL.md` §Hermetic grader + anti-pattern 14; `corpus/README.md` gate note; LOG entry skeleton (L1 filled all placeholders from own runs, per the draft's fill rule) |
| ScribeReport (scribe) | `r10-report-draft.md` (+ `r10-scribe.md`) | `.ufo/reports/round-10/kengaku.md` on the main repo (L1 filled every `{{PLACEHOLDER}}` from own measurements) |

## 2. Grader first-version defect (caught by the independent harness, not by L1)

The first landed `grader.py` (41777 B, mtime 19:15) **failed its own M0
control**: it carried a bogus check `r9.onset.predicted_vs_observed` that
compared the preregistered onset prediction (5.0) against the observed mean
(5.8) as an equality — a predicted *miss* is a result, not a mismatch.
MutationHarness's first live run captured `MISMATCH r9.onset.predicted_vs_observed:
stored='5.0 predicted' recomputed='5.8 observed'` → exit 1 on unmutated copies
(failing-before evidence, `r10-mutation-sh.md` §7.1). Fixed at 19:17:54 by
replacing the check with `r9.onset.prediction_preregistered` (verifies the
prediction exists; the observed mean is checked against `replication.md`'s
stored 5.8 only). Post-fix: committed tree exit 0 (`CHECKS n=149
mismatches=0`), selftest 4/4 with check-id assertions, harness M0–M3 4/4,
byte-identical output under `PYTHONHASHSEED` 1/99/unset.

## 3. Connector adoption ruling (all five recommendations adopted)

1. 0/1/2 fail-closed exit split (kagi `drift-pins.sh` convention; kotoba's
   `3=no baseline` deliberately not inherited — missing evidence maps to 2).
2. Stable check-ids + machine-readable `MISMATCH <check-id>: stored=<x>
   recomputed=<y>` lines, deterministic ordering.
3. `--selftest` exercises the real grader on private temp copies and asserts
   **both** exit code and expected check-id (strengthened after the survey —
   first version asserted codes only).
4. Expected values committed and independent of the recomputation: stored side
   comes from the evidence files, recomputed side from `raw`+meta; md5 pins
   live in-repo (`PINS`), satisfying `../../../PROTOCOL.md`'s "a pin only
   counts if its expected values are persisted in-repo".
5. Defaults resolve relative to the script directory; the invocation, observed
   verdicts and commit pointer are recorded in `LOG.md`/`SCORECARD.md`.

## 4. Adjudicated erratum pinned in the gate

`replication.md` §Onset-and-failures stores state errors "12/32" at the final
graded turn; recomputation from the committed `results-r9.jsonl` gives
**24/32** (passes 4+2+2+0 = 8/32, parse failures 0/32). Ruling: `grader.py`
`ERRATA["r9.failure_classes.state_error"]` pins the pair (stored-defective
"12/32", corrected "24/32") — the check passes iff the stored text still shows
12/32 AND the recomputation equals 24/32, so silently editing either side
fails the gate. `replication.md` gained an appended §Errata (round 10); its
md5 pin was updated `a70980a5f465da1bedd0ffa474a0c032` →
`d9235e41f3ebfdcabd368c71cde878a1`, the only change being that appendix.
Provenance of the "12" (checkpoint cells' 6+6 over the all-cells denominator)
is **conjectural**; the corrected value is arithmetic on committed bytes.

## 5. Operator rule received mid-round (binding)

Domain source repos (`ufo-fsd-alpha`, `bounties`, `webzites`, `llm-wiki`) are
READ-ONLY for this lane; commits/pushes only to `VeigaPunk/shokunin` (main,
report) and `VeigaPunk/kengaku-shokunin` (this repo). Upstream-bound work
(e.g. the `loop.sh` field-count bug in `~/bench-arena` — not a git repo, not
in the operator's four) travels in the round report; this lane recorded it as
corpus errata and backlog instead of patching the live battery mid-round.

## 6. Known limits of this round's evidence

- The endpoint scout's `Δ 5,973,152 B` between on-disk gguf size and
  `/v1/models` `meta.size` stays UNVERIFIED (no 10 GB md5 run); recorded as
  such in `r10-scout-endpoint.md`.
- `final-harness.log` and the M-battery outputs cite the grader as of
  19:17:54+ edits; the committed `grader.py` sha256 is recorded in the
  round-10 `LOG.md` entry so future rounds can tell which build produced
  which log.
- `local://r10-*` paths inside the committed artifacts were session URIs at
  authoring time; the files in this directory are their durable copies
  (byte-identical at copy time, 2026-09-28 ~19:3x local).
