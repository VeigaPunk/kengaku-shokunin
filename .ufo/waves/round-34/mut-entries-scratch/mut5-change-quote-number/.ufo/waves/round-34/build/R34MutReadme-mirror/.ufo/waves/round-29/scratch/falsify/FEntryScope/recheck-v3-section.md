
## Final re-check of candidate v3 (follow-up)

This is a second-seat Q10 re-read for the same item, FEntryScope. Everything above is left unedited.
This section covers only v3, across source, numbers, quality and scope.

- **Candidate path:** `.ufo/waves/round-29/drafts/webarena-config-projection.md`
- **Canonical path:** `corpus/knowledge/webarena-config-projection.md`
- **sha256, printed first:** `59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca`,
  equal to the digest the coordinator named. I reviewed these exact 99 lines.
- **Freeze record:** `candidate-freeze-v3.json` does not exist (only v1 and v2 exist).
- **Lane HEAD:** `dbcecded4a04247cf6fd12919327af973da10bdd`. The working tree has `plans/config_projection.py`
  at sha256 `d81a6af8…4f9f`, and both it and `plans/fixtures/r29/mutation_witness.py` are uncommitted
  (`M`). These are the coordinator's changes; I did not write them. Their hashes were the same before and
  after my runs.
- **Production source:** NOT read.
- **Writes:** this appended section, plus new scratch files (`summary-v3.txt`, `out-v3.json`,
  `selftest-v3.txt`, `mutation-v3.txt`, `recheck-v3-section.md`).
- **No lane, git or jj mutation.** Installs: none.
- **`/tmp`:** used only by the witness's auto-deleting `TemporaryDirectory`. Afterwards
  `ls -d /tmp/kengaku-r29-witness-*` counted 0. I made no `/tmp` copies of my own.

### What changed from v2 (observed)

- v3 lines 2–36 are textually the same as v2 lines 2–36. v3 lines 71–99 are the same as v2 lines 62–90,
  shifted by nine lines.
- Line 1 was not byte-compared, because I kept no v2 copy. It keeps the same S070–S074 source set.
- The changes are confined to line 37 and lines 58–70, matching the coordinator's description.

### Commands re-run (observed)

| command | exit | identity |
|---|---|---|
| `--json` | 0 | sha256 `a4fb5d6d…d851`, **byte-identical** to the v2 freeze `json_output_sha256` and to my `out-v2.json` |
| `--summary` | 0 | `TOTAL findings=0 exit=0`. Diffed against v2 with `LIMIT` lines excluded, only labels differ: an added `INPUT` line (raw `7b50386f…`, manifest `f6390b92…`, revision `dce04686…`) and `index_task_id_mismatches` renamed to `index_task_id_mismatch_count`, still 0 |
| `--selftest` | 0 | `SELFTEST clean cases=30` |
| `mutation_witness.py` | 0 | tool `d81a6af8`, `killed` 12, `url_only_substitution` killed, restored `d81a6af8` |

The objects and metrics are unchanged. My v2 checks still apply to these output bytes: 2436/2436
projected objects including key order, would-be digests and filenames, plus every table number
(790/22, 32, 462, 55/9, 697, 61/1355).

### The changed sentences, attacked

- **Line 37: "a value containing `\` can make it invalid or be interpreted as a JSON escape" (15 words).**
  - Supported. My probe parses `\n` as an escape and gets a decode failure for a trailing `\`.
  - Dropping the `\n` example removes nothing a reader needs, and the `"` restructuring clause on
    lines 35–36 is intact.
- **Lines 58–59: "Four oracles, separately written by distinct same-lane seats (independent logic, not independent identity)" (13 words).**
  - Supported. The writers are four distinct seats: `KengakuR29-2.FOracleText-2`, `.FOracleLeaf-2`,
    `.FOracleProvenance-2` and `.FOracleIndex-2`.
  - All four end in `VERDICT: PASS`, and each states that production source was not read.
  - The qualifier concedes exactly what `FCritOracleIndependence` disputed.
  - The claim is now narrowed to "population/profile metrics", 1435 provenance records, 2436 objects and
    would-be digests. That fixes v2's broader "every count".
- **Lines 62–63: "were separately re-derived by the entry-review seats, not by those four oracle reports" (13 words).**
  - Supported. `FEntryNumbers.md` lines 80–96 and 288–290 re-derive 790/22 and 32.
  - My own census re-derived all four: 790/22, 32 and 462 (`census_v2.out`), and 55/9 (v1 census).
- **Lines 64–65: "binds the repaired objects to the objects the oracles compared" (10 words).**
  - Supported with one qualification. The receipt compares `56fd949:plans/config_projection.py` with
    tool `135cc682`: objects equal ignoring key order, and provenance equal.
  - FOracleProvenance pins the v1 output `c8da0c5a…`, which was produced at 56fd949. The other three
    oracle reports pin no output digest, so for them the binding rests on wave timing.
  - The gap from `135cc682` to the current `d81a6af8` is closed by the byte-identical `a4fb5d6d` output
    observed above.
  - This is non-blocking. It is the same residual R3 as before, now partly closed.
- **Lines 67–70, the "Falsifiers" paragraph:**
  - Every named falsifier is observable with the shipped instrument: changed pin digest, nonzero remaining
    tokens, changed 61/1355 split, index/task-ID mismatch, object disagreement.
  - Line 70, "Agreement on this population alone does not establish general-input equivalence" (10 words),
    removes any reading of general semantic certification. This is a scope gain with no harm.

### Final verdict by axis

- **Source:** the S070, S072 and S074 bytes I re-verified earlier support every source sentence; these
  lines are unchanged in v3.
- **Numbers:** every table and bridge number reproduces, and the output bytes are unchanged.
- **Quality:** the units are named, the oracle attribution is scoped by which seat derived what, and the
  falsifiers are explicit.
- **Scope:** no sentence implies deployment configs, runtime validity, scoring effects, task invalidity,
  novelty gain, or coverage of all six tokens by the population (re-screened lines 1–99).
- **Decision rule (lines 86–94):** byte-unchanged from v2, and still supported as assessed above.
- **My seven v1 objections:** all remain resolved.

### Non-blocking residuals

- R1 ("established practice" vs the S074 row's "prior practice") and R2 (no byte-identity check on the
  run's raw file) stand unchanged and are optional.
- R3 is partly closed, as described under lines 64–65.
- Admission bookkeeping, outside this item: there is no `candidate-freeze-v3.json`, and the current
  instrument (`d81a6af8`) is uncommitted. The candidate text names no tool hash, so this verdict does not
  depend on either.

The verdict below is scoped to this exact v3 re-read, not to round admission.

VERDICT: PASS
