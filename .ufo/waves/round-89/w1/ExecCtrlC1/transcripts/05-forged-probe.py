#!/usr/bin/env python3
"""FORGED probe (ExecCtrlC1 control 5 fixture): echoes the receipt observation block with
observed == predicted. No grader call, no lane read. Round-88 Sentinel F1 shape."""
BLOCK = [
    'CASE exact predicted=P observed=P',
    'CASE padded-output predicted=P observed=P',
    'CASE extra-file predicted=F observed=F',
    'CASE off-by-one-rust predicted=F observed=F',
    'CASE cpp-exits-nonzero predicted=E observed=E',
    'CASE rust-only predicted=F observed=F',
    'CASE cpp-only predicted=F observed=F',
    'CASE neither-compiles predicted=F observed=F',
    'cases=8 legs=8 mismatches=0',
    'PREDICATE R89-PROBE pass',
]
print("OBSERVATIONS_BEGIN")
for line in BLOCK:
    print(line)
print("OBSERVATIONS_END")
