
## Final re-check of D5r and D6 (follow-up 2)

Same seat and item. Scope is limited to the two gaps left open in the previous section, as the coordinator directed.
Measured state: the **working tree** on top of dbcecded4a04247cf6fd12919327af973da10bdd (HEAD has not moved). The repairs are
uncommitted: `plans/config_projection.py` sha256 cb9104264a82e5c6794a3d1a88a5e51445060f8c8e4708740ad0871b1d04fc3c (modified),
`plans/fixtures/r29/mutation_witness.py` (modified), and `plans/fixtures/r29/projection_cases.json` sha256
d4c9ac5cacc2cad2f9839ffa179fdce050af830271d564e4bef8b69bf68e588d (**untracked**; `git ls-files --error-unmatch` fails). The prereg is
byte-unchanged since 31934e5. No tools installed. My only /tmp file (`/tmp/fccm-old.py`) has been removed; the leftover
`/tmp/kengaku-r29-freview` belongs to another seat.

### D5r: findings → exit 1 through the real `audit()`: **CLOSED**

- New selftest case `real_audit_finding_exit_one` (config_projection.py:595–599) patches `audit_text` to return one
  `projection_json_invalid` finding, calls the real `audit(scratch)` on the pinned /tmp copy, and asserts `finding_code == 1`.
  This exercises l.414, which the previous `exit_mapping` case bypassed.
- My mutant from the previous section is now persisted as `finding_exit_forced_zero` (`return result, int(bool(findings))` →
  `return result, 0`). Rerunning `python3 plans/fixtures/r29/mutation_witness.py` gives selftest exit 1 (`AssertionError`),
  killed. The extra `url_templates_narrowed` mutant is also killed. Totals: **12/12 killed**, restored sha = tool sha, and the
  parsed receipt is **equal** to corpus/evidence/round29-calibration/final-mutation-witness.json. [OBSERVED]
- `python3 plans/config_projection.py --selftest` exits 0 with `SELFTEST clean cases=31`, including
  `real_audit_finding_exit_one`, `independent_nine_domain_error_cases` and `all_url_path_categories`. [OBSERVED]
- Projection unchanged: `--json` sha256 is still a4fb5d6dd9b7d509be55ae9d5c779dccaf9e29a7727447a30c568a174579d851. The provenance
  pointer edit at l.259–260 only affects key-role occurrences, of which the frozen input has 0. [OBSERVED]

### D6: errors hand-case file and out-of-domain disclosure: **CLOSED**

- `plans/fixtures/r29/projection_cases.json` is byte-equal to `.ufo/waves/round-29/scratch/falsify/FOracleLeaf/projection_cases.json`
  (both sha256 d4c9ac5c…). The writer is FOracleLeaf-2, not the instrument author. It holds 9 cases, each with raw text, six
  values, `expected_json`, `expected_error` (exact `JSONDecodeError` strings) and `expected_leaf_json`. Together with the 3
  adopted fixtures, this meets prereg l.82 ("transforms/errors/order and output index values").
- Selftest l.502–512 checks the sha and asserts every text-side expectation, including exact error strings.
- **My own check**, a separate 20-line script applying six ordered `str.replace` to the text and the same sequence to every
  decoded key and value: **9/9 cases meet all three expectations** (text JSON, text error, sequential-leaf JSON). Text and
  sequential leaf **differ** in exactly the 6 cases that break escape-safety or verbatim values: quote_invalid,
  quote_structural_injection, backslash_decode, backslash_invalid_escape, backslash_trailing, escaped_token. They **agree** on
  cascade_later_token, earlier_token_control and keys_too_benign. That matches the corrected domain D1∧D2 in FOracleLeaf's
  appended §5, so the prereg l.43–44 disclosure ("where that alternative is not equivalent") is now stated and reproducible.
- FCritOracleIndependence §4 objections, as addressed in FOracleLeaf's appended correction:
  - (a) A sequential decoded-leaf oracle now exists and agrees 2436/2436 on the frozen data; single-pass is kept only as a
    labeled alternative.
  - (b) The write-before-parse wording is corrected, consistent with generator l.17–20; the case-file `contract` field says
    the same.
- Hygiene note, not a C1 issue: the earlier FOracleLeaf bytes are intact, but its old final `VERDICT: PASS` line now follows
  the appended section rather than staying in place. All bytes before that line are unchanged (prefix hash da61e29b… equal).

### Bounded caveats (outside the two gaps; they do not change the verdict)

- [INFERENCE from l.502 and l.660–663] The selftest now requires `projection_cases.json`. If an admitting commit included the
  instrument without that untracked file, `--selftest` would hit `FileNotFoundError` and exit 2 (`selftest_could_not_run`).
  The admitting commit must contain both files with the hashes above.
- Interpreter range: `--selftest` prints `SELFTEST clean cases=31` on CPython 3.9.25, 3.10.22, 3.11.17, 3.12.15, 3.13.16, 3.14.8
  and 3.15.0, so the exact error strings are stable across these versions. On 3.8.20, `--summary` exits 2 with an
  `internal_error` finding (no `ast.unparse`), and `--selftest` exits 1 with an uncaught traceback. 3.8 is below the source's
  stated 3.9+ floor; noted, not credited.

### Final bounded claim-met judgment

As frozen, C1 is **met** on the measured working-tree bytes:
- 812 tasks / 3 profiles / 2436 projections with no hidden exclusions;
- occurrence and field provenance with named codepoint offsets;
- the output-index versus task_id mapping, with shuffled-ID and order witnesses emitted in `--summary`;
- independent oracle agreement: four oracle seats, bridged across the repair by object equality, and limited to the benign
  frozen domain;
- all 10 Required-output items (l.62–71) and every selftest requirement (l.73–77), including exits;
- the independent hand-case file with errors and the non-equivalence disclosure (l.43–44, l.82);
- the failing wrong-URL-only and wrong-order witnesses (l.100).

Not claimed: a score change, round admission, deployment, runtime behavior, blind or model-calibrated oracle independence,
or exhaustive mutation coverage. The judgment holds only if the admitting commit contains these exact bytes (instrument
cb910426…, cases d4c9ac5c…, JSON output a4fb5d6d…).

VERDICT: PASS
