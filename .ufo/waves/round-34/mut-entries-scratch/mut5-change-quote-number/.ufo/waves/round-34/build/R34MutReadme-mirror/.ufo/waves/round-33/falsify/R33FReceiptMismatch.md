# R33FReceiptMismatch — the adoption counter's relationship to its gate receipt

Seat: `KengakuR33.R33FReceiptMismatch` (reviewer, leaf; no subagent dispatch).
Lane: `kengaku-shokunin`, HEAD `77ac8c1307ba60e9572a7e2789b71ae31b133440` (read-only; 19 in-flight porcelain entries at read time, untouched).
Target: `plans/adoption_check.py`, `plans/round33_c1_verify.py`, `assimilation/gate-receipts.txt`, current `corpus/SOURCES.md` rows S103/S104.
Sandbox (fresh /tmp, no git used): `/tmp/r33-receipt-mismatch/kengaku-shokunin/` — minimal copy of exactly the bytes the two counters read; runs below used the sandbox copies only. Access date 2026-10-25.
Verdict: **UNCAUGHT — adoption counter and C1 second receipt neither consume `assimilation/gate-receipts.txt` nor bind it to the rows currently in SOURCES.md.**

## 1. What each script reads (function-level audit)

### `plans/adoption_check.py` (sha256 `f9f8188efb3612c1a1a9d7a3e2272255096b76bd3100d3dacdded63dd7d69926`)
Inputs consumed in `main()` / `registry_rows()` (lines 40–163):
- `--expect` (required JSON file; `args.expect.read_text()` then `json.loads`),
- `lane / "corpus" / "SOURCES.md"` via `registry_rows()` (parses `| S### |` rows with `ROW_RE`, 11 cells),
- `lane / "corpus" / "README.md"` (index-row scan),
- each `entry["path"]` file (present/`verified-at`/`source:` lines),
- with `--census`: subprocess `CENSUS` = `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <lane.parent> <lane_name>` (line 19, 113–121).

No reference to `gate-receipts`/`receipt`/`assimilation` anywhere in the file (grep over `plans/` for `gate-receipts|assimilation` hits only claims prose, never a script). The hidden gates are: `verified_at_ok`, `ids_ok` (`set(declared) != set(entry["sources"])`), `duplicates_ok`, `opened_ok` (registry cell 8 vs `access_date`), `index_shape_ok`, plus printed `rows_present/rows_mined/usedby_ok` — all bind registry **rows ⇄ expect-file ⇄ entry text**, never rows ⇄ gate receipt.

### `plans/round33_c1_verify.py` (sha256 `b04716c4571206366d606774547af90f9e793658e089ddd495d0843d579543ca`)
Module constants (lines 13–22): `ENTRY`, `REGISTRY`, `README`, `LESSON`, `EXPECT`, `CONTROL = ".ufo/waves/round-33/claims/control-nothing.txt"`, `PINS`, `RENAMES`, `REFUSAL_IDS`. Checks:
- `check_v1` — `ENTRY` exists + `verified-at: <access_date>` line,
- `check_v2` — entry `source: S###` line names the registry row's first URL (`URL_RE.search(rows[sid][0]) or URL_RE.search(rows[sid][1])`, `host_path` substring; rows ⇄ entry only),
- `check_v3` — entry text contains all three `PINS` literals,
- `check_v4` — exactly one README index row, non-trivial title cell,
- `check_v5` — entry length ≥40 lines / ≥3000 bytes,
- `check_v6` — `CONTROL` receipt pins `expect_sha256=<digest>` and `exit=1`,
- `check_v7` — lesson `round-33.md` records the renumber map (S094→S103, S097→S104) as prose,
- `check_v8` — refusal rows S094/S097/S101/S102 keep `supersedes`/rejected markers.

The **only "receipt" consumed** is `claims/control-nothing.txt` (freeze control) in `check_v6`. Nothing reads `.ufo/waves/round-33/assimilation/gate-receipts.txt`. The gate receipt is therefore consumed by **no counter**; the only producer/search consumer is `plans/sources_adopt.py` (the gate itself) and prose citations.

## 2. Mutation evidence (sandbox, byte-identical reruns)

Baseline R0 (sandbox copy of committed bytes): `round33_c1_verify.py --lane <sb>` → `checks=8 defects=0`, exit 0; `adoption_check.py --lane <sb> --expect …adoption-expect.json` → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=skipped`, exit 1 (exit requires `--census`; sandbox census cannot reproduce the fleet census — see §4).

| Run | Mutation in sandbox | `round33_c1_verify.py` | `adoption_check.py` (no `--census`) |
|---|---|---|---|
| R1 | `gate-receipts.txt` **deleted** | `checks=8 defects=0`, exit 0 — byte-identical to R0 | printed line byte-identical to R0, exit 1 |
| R2 | `gate-receipts.txt` **replaced with fabricated contradiction** (asserts `defects=99`, `EXIT=8`, `located=0 found=0 overlong=8 absent=8`, every quote REFUSED, all `bound=` point to `https://example.invalid/never-fetched`) | `checks=8 defects=0`, exit 0 — byte-identical | printed line byte-identical, exit 1 |
| R3 | pristine receipt restored; **landed S103 row mutated**: pinned blob URL → `https://example.org/not-the-pinned-blob`; anchor quotes `"# Validate with 0.05% tolerance"` → `"# Fabricated tolerance comment never captured"` and `"validate_record_data(actual_records, expected_records, tolerance_pct=0.05)"` → `"fabricated_call_entirely(records, tolerance_pct=0.5)"` (entry `source: S103` line untouched) | `checks=8 defects=0`, exit 0 — byte-identical | printed line byte-identical, exit 1 |

stdout hashes: R0=R1=R2=R3 for both counters (`480ca1eb…` verify; `ff436270…` adopt). In R3 the row's anchor spans no longer exist in any capture and the pinned blob is gone — yet both frozen-predicate counters still pass, including the receipt that is supposed to be the C1 kill-rule record. The receipt would have to be wrong *and* ignored for this to happen; on these bytes it is ignored.

## 3. Root cause

The C1 kill rule ("a cited source whose located quote cannot be found in this round's captured bytes at the pinned revision is refused for that row … `plans/sources_adopt.py` … bind") is enforced only inside `sources_adopt.py` at gate time. Its only artifact is `gate-receipts.txt`, which is descriptive (no command line, no revision, per `R33FQ22.md` F5) and is not consumed by either counter named in the frozen predicate (`adoption_check.py`; `round33_c1_verify.py`). `adoption_check` binds rows to the expect file, entry, and fleet census; `round33_c1_verify` binds rows to entry text, pins, and lesson prose — neither binds the receipt to the rows. A receipt that entered the record as green can therefore be rotated, deleted, or replaced with a fabric sheet without any claim-facing counter noticing; conversely a landed S103/S104 row can drift from the validated quotes/artifacts without any counter noticing.

## 4. Limitations
- `adoption_check.py`'s frozen `--census` leg is not reproducible in a /tmp sandbox (`CENSUS` is an absolute host path; sandbox run gave `census=fail` — a sandbox artifact, not a receipt signal).
- R3 keeps `check_v2` green by design (it reads only the *first* URL of the row cell); the receipt⇄row divergence is what is demonstrated, not a claim that `check_v2`'s other blind spots are resolved here.
- Corroboration: sibling reports `R33C1KillRule.md` rows 2–3 (root-binding, receipt-vs-landed-bytes disagreement) and `R33GateMutants.md` already documented receipt/map/row divergences; `R33FMap.md` shows the committed `gate-receipts.txt` itself bounds the blob URL — i.e. the committed receipt bytes are *not* the ones those two build reports describe, a dispute only possible because nothing re-runs the receipt.

`VERDICT: receipt-mismatch-uncaught`

`REPORT: .ufo/waves/round-33/falsify/R33FReceiptMismatch.md`
