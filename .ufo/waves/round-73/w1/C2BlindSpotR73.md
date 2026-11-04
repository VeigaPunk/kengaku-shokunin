# C2BlindSpotR73

Axes: coverage, calibration. Frozen claims read before shell commands; frozen instrument and predicates unchanged. No dispatch, git/jj mutation, install, or landing verdict.

## Results

Ran 16 isolated cases through `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round73_c2_registry_audit.py --lane /fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/cases/<ID>`, each pristine → mutated → restored.

- 3 caught / killed, rc 1: gate without zero, exact duplicate, owner sibling.
- 13 accepted / survived, rc 0: omitted probe exit 2; entry flag in comment; bare self-test script; missing self-test script; nonexistent pinned path; case-only duplicate; kengaku-ish owner; zero-only gate with failure word; nine-cell and seven-cell rows silently dropped; entirely absent entry flag; self-test flag in comment; contradictory third erratum item.
- Every final pristine/restored run rc 0. Every full fixture SHA-256 map restored exactly. Baseline failures: none. Inconclusive: none.
- Driver: `python3 /fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73/probe.py`, exit 0; `all_agree=True cases=16`.
- Frozen instrument SHA-256 before/after: `9ec8f4d2ba2233751f3ef54c31fe169dfd89b39249dcc459b6b9e75756345828`.

Evidence: `corpus/evidence/round73/w1/c2-blindspots.md` includes every row, actual output/rc, per-case leg and landing-relevance sentence, full harness, raw receipts and file-hash maps.

## Calibration

D2 is most fragile: the broad eight-field description covers raw substring/prefix checks and nonempty-only cells. `command_flags` is defined but never called. Strongest findings are nonexistent self-test accepted, malformed rows disappearing before every-row accounting, and D4 checking only the first matching item while ignoring a later contradiction.

Not all accepted fixtures violate frozen wording: prefix owner, exact-case names, nonempty pins, and failure-word acceptance are explicit contract boundaries, not permission to change the rule. Bare self-test scripts can also be legitimate. No claim of a landing-tip failure is made.

## Process limitations and cleanup

Initial driver classified `DEFECTS n=0` as a defect; corrected to the exact `DEFECT ` prefix. A repeated fixture run retained an extra script in baseline; final run removed all cases first. Final raw receipts exclusively represent the clean run. Read-only Python module import may generate incidental __pycache__ bytes; source immutability is established, but zero cache writes is not established.

No tools installed; Python 3.14.8. Scratch removed after evidence persisted: `test ! -e /fast/scratch/hyaku/kengaku-r73/C2BlindSpotR73` succeeded and printed `SCRATCH absent`. Nothing created in /tmp.

## Self-evaluation

Accuracy 4: actual CLI receipts and full hashes; semantic defects distinguished from literal boundaries, but cache side effects not established. Completeness 5: sixteen cases exceed six, all required per-case evidence supplied. Clarity 4: candidate vs literal-rule distinction explicit; raw appendix lengthy. Actionability 4: harness preserved, but no instrument edits authorized. Conciseness 4: report concise; evidence intentionally exhaustive. Mean 4.2. Improvement: preserve the substantive distinction between semantic validity and the weaker frozen pricing rule; avoid implying all survivors falsify the literal claim. User agreement expected on observed acceptance, not assumed on landing policy.
