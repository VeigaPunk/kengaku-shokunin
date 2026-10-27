# R45CriticC2Instrument — result recovered from w1-results.json (reportless-seat class, round-45 recurrence)

{
  "counterexample": "V4 accepts hand-authored receipts matching the dry CASE ids/order and summary, because it parses only CASE predicted/observed/violates fields and match=NO strings; it does not bind receipt bytes to execution or authenticate its origin. A fabricated CASE set with consistent counts and no mismatches can satisfy V4 (while V5 only pins probe and dry table, not the receipt).",
  "evidence": "round45_c2_verify.py:187-223: receipt_cases parses CASE lines; V4 verifies ids, one summary, count agreement, and mismatch IDs in entry only. V5 at :226-232 pins probe/dry, not receipt. This falsifies provenance but whether full counter accepts depends on V2 gate's P10 fresh-probe byte comparison, which likely catches it; V8 independently checks committed order, not receipt contents.",
  "impacted_axes": [
    "coverage",
    "operability"
  ],
  "v8": "V8 runs order_check against git history. order_check.py:166-175 requires claims and receipt committed at HEAD; :192-205 scans claims history for executed probe evidence and emits PASS. It requires an existing committed receipt path, not that it be genuine; V2 package gate supplies fresh probe comparison as a separate authority.",
  "v11": "Lint bypass is intrinsically admitted by documented limit: counter header :25-28 explicitly allows open-coded truth tables that fit lint and requires non-author review. Exact membership implemented using chr() concatenation evades banned tokens (no braces/import/IO/hash) and works across all generated states; not actually run here due failed fixture construction. Also current grader membership fact is line-membership; a constant assembled via chr satisfies it.",
  "pins": "Frozen digests pin spec, gate, probe, dry table, captures; order_check.py and claims are not digest-pinned by C2. Potential over-pin: CAPTURES includes gitignore despite claim stating gitignore rejected as repo hygiene; V1 treats nine listed captures as frozen data, but spec rows only enumerate S149-S156 (eight knowledge rows), with ninth README? README is source S154 and gitignore is unrelated. Under-pin: ORDER_REL and CLAIMS_REL consumed by V8 but not digested, allowing their logic/evidence contract to drift. No frozen claim requires exact order_check implementation digest; source intent review must establish whether under-pin changes meaning.",
  "execution_limitation": "I did not complete the requested scratch mirror demonstration: mirror clone succeeded, but predictor-fixture editing command failed with a Python quoting SyntaxError. No counter run was performed. No envelope result exists."
}
