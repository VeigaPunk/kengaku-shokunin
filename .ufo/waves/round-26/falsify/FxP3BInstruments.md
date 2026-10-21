# FxP3BInstruments — round 26 falsify

Scope: P3b PROVINCE instrument claims vs pinned receipts; one scratch mutation; P2 preservation. No lane files changed. Scratch exports: `/tmp/kengaku-r26-FxP3BInstruments-20261021/{base,integrated,mutated}`.

## Finding — P3b census corrections remain incomplete (C2 does not reach claimed clean state)

The integration export `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8` returns exit 1; P3b assertions `P3b.province.public-literature-registry.rows` (line 112) and `P3b.province.round25-correction.rows` (line 119) remain MISMATCH. Observed frozen census is 42 rows with exact S001–S042 set. Latest R26-E8/E7 corrections (PROVINCE.md lines 184–185) parse as `correction_tokens=["rows=42"]`, while the checker derives `["rows=42","id_set=exact"]`; strict full-token supersession therefore does not close either assertion. This conflicts with the registered after-state `mismatch=0`; add the missing exact-id-set token to the corrections or otherwise meet the existing exact-token contract.

## Instrument checks — scoped pass

On both base `f11bffbf9caa9c9e286fb32c568b81b97719656a` and integration exports, the receipt-backed P3b instrument assertion IDs all MATCH:
- `P3b.province.interval-reverdict.exits`: 0/0; `.unique-samples`: 4; `.scored-trials`: 92/92; `.transitions`: 2/1.
- `P3b.province.state-assertion-check.landed-exits`: 0/0; `.base-exit`: 1; `.base-mismatch`: 10.
Receipts: `corpus/evidence/round25-calibration/attrib-calibration-summary-v2.txt`, `attrib-calibration-selftest-v2.txt`, `state-check-after-v2.txt`, `state-check-selftest-v2.txt`, and `state-check-before-6180e4f-v2.txt`.

## Commands and evidence

- `git archive f11bffbf9caa9c9e286fb32c568b81b97719656a | tar -x -C /tmp/.../base`; same archive command for integration SHA into `/tmp/.../integrated`; both exports consumed successfully.
- `python3 /tmp/.../base/plans/state_check.py --root /tmp/.../base --json` — exit 0 (v2).
- `python3 /tmp/.../integrated/plans/state_check.py --root /tmp/.../base --json` — exit 1; instrument IDs above MATCH; only P3b historical census rows are outside this instrument check.
- `python3 /tmp/.../integrated/plans/state_check.py --root /tmp/.../integrated --json` — exit 1; P3b census IDs above MISMATCH; overall summary 275 assertions, 3 mismatches.
- In a copied `/tmp/.../mutated` export only, changed PROVINCE line 116 from `92/92 correct` to `91/92 correct`; `python3 /tmp/.../mutated/plans/state_check.py --root /tmp/.../mutated --json` — exit 1; `P3b.province.interval-reverdict.scored-trials` MISMATCH, claim 91/92 vs receipt 92/92.
- `python3 /tmp/.../integrated/plans/state_check.py --selftest` — exit 0; reports P3b instrument mutation and exact-id-set red mutations pass.
- P2 preservation: filtered P2 assertion objects (`id,source_line,check,observed,verdict`) from base v2 and integration v3-on-base JSON, sorted by id; `cmp` exit 0, identical.

Residual risk: P3b source-census correction behavior is the concrete failure above; other non-P3b assertions in the whole-tree exit-1 result were not adjudicated in this seat.

Verification gaps: no build/lint/tests run; only the assigned state_check invocations and JSON comparison were exercised.

VERDICT: FAIL — the four receipt-backed instrument rows match and mutations are detected, but integration still has two unsuperseded P3b census mismatches, so the claimed clean C2 state is not established.
