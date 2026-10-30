# SC3ForgeRead — round 54 wave 1

Axes: novelty and calibration. Read-only scout mapping, no fixes or scoring.

## Deliverable

`.ufo/waves/round-54/w1/SC3ForgeRead/vectors.md`: numbered 18-vector table, exact frozen-claims quotations, source pointers, scope-hygiene notes, and routed gaps. Both requested round-53 critic reports were read in full; `C1CritNeverRead.md` skimmed. `plans/round-54-claims.md` read in full and never edited.

Round-53 outcomes are attributed to their original reports, not freshly reproduced. R54 coverage is a design/source mapping, not measured closure. Source inspection used `functions.grep` and ranged `functions.read` on the named counters. **LSP unavailable:** `read xd://lsp` returned “No such tool”; literal grep is fallback only, not semantic caller/reference proof. No tests, builds, fixture runs, network calls, git mutations, installations, scratch clones or scratch directories.

## Gaps — pasted from the vector map

1. **G1 — Object boundary / instrument trust (C1).** External BINDING names claims bytes, not r53 classifier/labels or counter bytes. O §5's proposed counter-digest pin is absent from the frozen claims text. Retaining claims while replacing other artifacts is not checked by BINDING. Counter replacement is a trusted-verifier boundary, not a reproduced R54 PASS.
2. **G2 — Non-forbidden argv substitution (C2).** E `entry_mode_ok` checks only script and exact tokens `--selftest`, `--help`, `-h`, `--dry`, `--version`; `run_row` executes the ledger's argv. A10's changed argument or another instrument-specific benign invocation may remain. High-confidence source gap; end-to-end reproduction outstanding.
3. **G3 — Worker-local config (C2).** E `Worker.reset` does not restore `.git/config`; ENV control only tests caller-global config. A11/B4 mechanics remain source-visible. Jobs-dependent reproduction outstanding.
4. **G4 — Malformed timeout receipt (C2).** Unguarded `int(timeout_s)` remains outside the execution try. A12-style malformed input is expected to crash without a predicate line. This fails nonzero, not fail-open; negative-timeout bypass unproven.
5. **G5 — Registry population/cell pins (C2).** No r53-style fixed row-set pin found in E; static equality is against current registry. A2/A13 consistent rewrites are residual fixture candidates. Real SKILL.md changes are prohibited by Q12; distinguish process breach from admitted input.
6. **G6 — Blind-reader protocol.** No R54 leg addresses O's shared-answer-key exposure. No collusion proven; R54 does not commission another label experiment, so this is inherited protocol scope rather than a live classifier claim.
7. **G7 — Instrument strength.** A9 remains outside declaration-versus-observation measurement. P explicitly treated it as accepted scope, not a new objection.
8. **G8 — EXTERNAL-PIN provenance (C1; additional source-inferred candidate).** A:412–430 checks receipt field presence, matching header values and distinct `source` strings; `fetched_at` freshness/source authenticity are not checked there and verify is offline. Thus Q3 freshness/independent-public-source provenance requires external evidence. No forged-receipt experiment performed. An honest late re-stamp also needs a real Bitcoin confirmation and differs from the assignment-pinned digest; not a demonstrated attack here.

Abbreviations: O = `.ufo/waves/round-53/w3/C1CritOracle2.md`; P = sibling `C2CritPredicate2.md`; A = `plans/round54_c1_anchor.py`; E = `plans/round54_c2_entrytruth.py`. Q12 = frozen claims' byte-identical artifact constraint. Exact quotes appear in vectors.md.

## Absence evidence / limits

Literal `functions.grep` pattern `sha256|FROZEN|REDECLARED|r53|MIGRATION|pinned` on `plans/round54_c2_entrytruth.py` returned migration/r53 matches but no fixed digest enforcement; ranged reads of `static_legs` and `entry_mode_ok` ground G2/G5. This is source evidence, not an executed bypass. Frozen claims read in full contains no counter digest literal. No immutable snapshot of live counter files was captured; cited source lines describe the reads made during this seat, not a promise about later integration.

N's scope-hygiene lesson applied: a broader historical/protocol weakness is not silently promoted to failure of a narrower frozen predicate. Malformed timeout crashing nonzero is not false PASS. Existing r53 artifact tamper rejection is not misattributed to r54 claims-byte BINDING. C1 proof controls are new proof negatives, not attacks the r53 critics actually ran.

## Self-evaluation

Accuracy 4/5: explicit separation of report evidence, literal source facts and unexecuted inference; no fresh route reproduction. Completeness 4/5: all reported attack families mapped, grouped variants retained by label. Clarity 4/5: quote key avoids oversized table cells, but references require consulting vectors.md. Actionability 4/5: G2/G3/G4/G5 identify exact reproduction targets; no fixtures by design. Conciseness 4/5: gap list intentionally repeated to meet acceptance. Overall 4.0/5. Highest-impact improvements applied: removed unsupported PASS assertions, corrected crash versus fail-open distinction, and separated scope constraints from instrument closure. User should find this useful as a scout map rather than a substitute for critic receipts.

No scratch cleanup needed; no tooling installs. Only the two named seat artifacts written.

**Report:** `.ufo/waves/round-54/w1/SC3ForgeRead.md`
