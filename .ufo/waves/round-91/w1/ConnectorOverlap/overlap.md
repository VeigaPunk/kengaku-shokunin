# ConnectorOverlap — sibling-overlap scan, round 91 (read-only)

Seat: ConnectorOverlap (connector, leaf). Scope: fleet siblings `<id>-shokunin` (kengaku excluded), read-only over `plans/`, `tools/`, `scripts/`, `tests/`. No file was opened for write in any sibling. Scratch: `/fast/scratch/hyaku/kengaku-r91/ConnectorOverlap` (removed on exit). No tool was installed or upgraded.

Method: per-lane counts with `grep -rIliE` (read-only, `-l`); line numbers for hits with `grep -nIE -m1` and direct reads. Patterns were regex tokens, so counts are upper bounds on candidates, not verified mechanisms. Each hit below was read at its line before classification.

Surfaces:
- (a) freeze-refusal gate keyed on routed-finding age: `freeze.{0,80}(refus|admit)` ∩ `opened_round|oldest_round|routed_open|routed-findings|routed-defects|defects.jsonl`.
- (b) sha/blob pin ledger over counters or receipts with a checker self-pin: `counter-pins|pins?.json|PIN-MISMATCH|PIN_MISMATCH|TRUSTED_TOOL_SHA|TOOL_SHA|self.?pin`; self-byte read = `(open|read_bytes|read_text)(__file__)` or `hashlib…__file__`.
- (c) offline replay of a pinned Terminal-Bench 2.0 grader in bubblewrap: `bwrap|bubblewrap` ∩ `Terminal-Bench|terminal-bench|test_outputs`.

## Per-lane counts (files)

| lane | scanned dirs | files | (a) freeze∧refus/admit | (a) age-ledger tokens | (a) both | (b) pin tokens | (b) self-byte read | (c) bwrap | (c) TB2 names | (c) both |
|---|---|---|---|---|---|---|---|---|---|---|
| chousa | tools | 19 | 0 | 0 | 0 | 1 | 7 | 0 | 0 | 0 |
| kagi | plans | 40 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| kaidoku | plans, tools | 482 | 20 | 0 | 0 | 43 | 118 | 4 | 0 | 0 |
| kake | plans, scripts | 520 | 0 | 0 | 0 | 3 | 10 | 0 | 0 | 0 |
| kama | plans, tools, tests | 246 | 0 | 0 | 0 | 0 | 30 | 1 | 0 | 0 |
| kasegi | plans | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kotoba | plans | 64 | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| kotodama | tools | 388 | 0 | 0 | 0 | 11 | 38 | 0 | 0 | 0 |
| kumitate-shokunin | scripts | 38 | 0 | 0 | 0 | 5 | 0 | 4 | 0 | 0 |
| mado | plans, tools | 47 | 0 | 0 | 0 | 0 | 5 | 1 | 0 | 0 |
| mori | tools | 124 | 0 | 0 | 0 | 4 | 26 | 0 | 0 | 0 |
| souji | tools, tests | 1240 | 2 | 0 | 0 | 4 | 31 | 4 | 0 | 0 |
| tabi | plans, scripts | 93 | 1 | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| tameshi | plans, tools | 121 | 0 | 2 | 0 | 6 | 27 | 1 | 0 | 0 |
| tsukuroi | plans, tools | 147 | 0 | 0 | 0 | 1 | 75 | 0 | 0 | 0 |

No scannable plans/tools/scripts/tests directory: `kumitate-shokinin` (directory present, no scan dirs), `audio-shokunin`, `game-dev-2d-shokunin`, `game-dev-3d-shokunin`, `lore-shokunin`, `revenger-shokunin` (git repos, no scan dirs; counted 0). Not `-shokunin` lanes, skipped: `exp-full`, `history-recheck`, `research` (empty).

Column caveat: the (b) self-byte column is broad (it counts any tool that hashes its own file, including data-artifact digests); the stricter self-pin list is in §2.

## 1. Surface (a) — freeze refusal keyed on routed-finding age

Hits (none implements the mechanism):
- `kotoba-shokunin/plans/round-89.md:42` — freeze gate refuses a freeze whose declared expectation is unsatisfiable; refusal is on expectations, not finding age. Owner: kotoba lane.
- `kaidoku-shokunin/tools/round-84/freeze-precheck.py:9` — prefreeze refusal of claim metadata (counter path not pinned, pin mismatch); no age clause. Owner: kaidoku lane. Same family in `tools/round-87/freeze-precheck.py:14`.
- `kaidoku-shokunin/tools/round-30/prefreeze-gate.py:28` — `PIN_MISMATCH` refusal of a recorded counter sha at the freeze commit; a pin refusal, not an age refusal. Owner: kaidoku lane.
- `kaidoku-shokunin/tools/round-29/freeze-gate.py:28` — `INSTRUMENT_PIN_MISMATCH` post-hoc audit; exits 0 on disclosed findings. Owner: kaidoku lane.
- `souji-shokunin/tools/souji-freeze-check.py:301-306` — a receipt whose bytes first exist at FREEZE is refused (commit-age of receipts, not of routed findings). Owner: souji lane.
- `tabi-shokunin/scripts/check-frontier-admission.mjs:38` — `r4-opened`: a frontier row's `opened` date must be ≥ `--since` (age-keyed admission of rows, not a freeze over routed findings). Owner: tabi lane.
- `kotoba-shokunin/plans/round-61.md:36`, `:171` — blob no older than the row's recorded open date (provenance age, not finding age). Owner: kotoba lane.
- `tameshi-shokunin/plans/round-60.plan.md:53-64`, `round-60-attempt2.plan.md:29` — `corpus/routed-defects.json` rows `R59.x` counted by status; `tools/defect-bind.py` (header lines 1-12) binds routed defects to repo state. No age clause observed in `defect-bind.py` (grep for older/opened/age/freeze/refus found refusal-of-input clauses only). Owner: tameshi lane.

Answer: **no sibling implements a freeze refusal on routed-finding age.** No sibling has an `opened_round`, `oldest_round` or `routed_open` gate.

## 2. Surface (b) — pin ledger over counters/receipts and checker self-pin

Sibling checker self-pins (checker's own running bytes compared to a value it or its contract pins):
- `kaidoku-shokunin/tools/round-34/version-needs-counter.py:177` — `digest(Path(__file__).read_bytes()) != contract["instruments"]["tools/round-34/version-needs-counter.py"]` raises `Unevaluable("running_counter_pin")`; the self-entry is in the frozen contract's instrument ledger (`:174-176`). **Closest exact match to R91-C2's self-pin**. Whether its selftest runs inside the predicate path was not verified. Owner: kaidoku lane.
- `kaidoku-shokunin/tools/round-46/attest.py:499`, `:524` — `PIN_SELF = sha256(open(__file__))` used as the default pin of the attestation (`pin = pin or PIN_SELF`). Owner: kaidoku lane. Same default-self-pin pattern: `tools/round-47/exact.py:468`, `tools/round-48/meanings.py:629`.
- `kaidoku-shokunin/tools/round-78/attack-gate.py:806`; `round-80/receipt-provenance.py:273`; `round-79/gate-mutation.py:243`; `round-81/strictness-battery.py:176` — a receipt's recorded `instrument.sha256` is compared with the tool's running bytes. This binds receipt to tool, with the pin written by the same tool; it is weaker than an external pin ledger. Owner: kaidoku lane.
- `kotodama-shokunin/tools/gates/typed-pipeline-gate.py:455` ("assembler self-pin broken") and `tools/assemble-culture-d4.py:35` (documents its own digest as a self-pin, D3 `serializer_sha256`). Checker-side self-pin inside a gate. Owner: kotodama lane.
- `souji-shokunin/tools/souji-seat-audit.py:79`, `:478` — `AUDITOR_SOURCE_SHA256` is computed from the file at import, then the same file is re-read and compared. This detects mid-run change only; the constant is not an independent pin. Owner: souji lane.

Sibling pin ledgers over counters (no self-entry found):
- `kumitate-shokunin/scripts/counter-pins.mjs` with registry `.ufo/pins/counter-pins.json` (45 path entries; `grep` for `counter-pins.mjs` in the registry returns nothing). This is a sha pin ledger over frozen counters, with `--selftest` and `COUNTER_PINS: DRIFT/FAIL-CLOSED` verdicts. **It does not pin the checker itself.** Owner: kumitate lane.
- `kaidoku-shokunin/tools/round-42/prior-pins.json`, `round-44/c1-counter.py:263`, `round-49/c1-counter.py:271` — pin lists of prior carriers, not checker self-pins.

Disclaimers, not pins: `souji-shokunin/tools/souji-evidence-cache.py:201` and `souji-preservation-evidence.py:206` state their trust anchors are "not self-pinned". `mori-shokunin/tools/mori-pin-check.py:1498` writes a `tools/selfpin.py` fixture (test artifact).

Answer: **yes, siblings self-pin their checkers.** Exact-mechanism matches: `kaidoku round-34/version-needs-counter.py:177` (self entry in the frozen instrument ledger, checked in the predicate path) and `kotodama assemble-culture-d4.py:35` / `typed-pipeline-gate.py:455`. No sibling combines a pin ledger that covers its own checker, a blob entry for a case table, and a selftest inside the predicate. R91-C2's `counter-pins-r91.json` combination is therefore not implemented by any sibling in the form scanned.

## 3. Surface (c) — offline replay of a pinned TB2 grader in bubblewrap

Zero sibling files match both `bwrap|bubblewrap` and `Terminal-Bench|terminal-bench|test_outputs`. Sibling bwrap uses, none of them a TB2 grader:
- `kaidoku-shokunin/tools/round-90/upx-later-block-battery.py:27` — carrier re-score in bwrap (UPX firmware). Owner: kaidoku lane.
- `kumitate-shokunin/scripts/cap-run.mjs:18`, `scripts/bind-oracle.mjs:30`, `scripts/harm-matrix-gates.json:37` — capture/oracle sandbox for kumitate's own gates. Owner: kumitate lane.
- `kotoba-shokunin/plans/round-86.md:61` — scored module runs only inside bwrap (session transcripts). Owner: kotoba lane.
- `kama-shokunin/tools/round58-battery-exec-check.py:14` — states in-process confinement is not a sandbox. Owner: kama lane.
- `mado-shokunin/tools/mado-hostguard.py:8` — bubblewrap namespace runner. Owner: mado lane.
- `tameshi-shokunin/tools/env-diff.py:76` — `bwrap=` parameter in `execute`. Owner: tameshi lane.
- `souji-shokunin/tests/fixtures/r20-audit-contract.py:668`, `r20-input-binding.py:1296`, `r34-sandbox-junk.py:107`, `r35-sandbox-junk.py:118` — bwrap in test fixtures. Owner: souji lane.

Answer: **no sibling overlaps the TB2 bwrap replay**. The in-lane precedents are kengaku's own (`plans/build_pmars_probe.py`, `constraints_probe.py`, `feal_probe.py`, etc.), so no sibling absorbs or duplicates them.

## Summary for the integrator (KengakuR91)

- (a) freeze refusal on routed-finding age: **no sibling implements it**; nearest mechanisms are pin-refusal and receipt-age refusal in kaidoku/souji. Owners: their lanes; nothing absorbed.
- (b) checker self-pin: **siblings do self-pin** (kaidoku round-34 in predicate path; kotodama assembler self-pin). No sibling pins its checker via a ledger plus a selftest in the predicate path.
- (c) TB2 bwrap replay: **no sibling overlap**.
- No sibling file was opened for write; no install or upgrade; nothing written outside the report paths.
