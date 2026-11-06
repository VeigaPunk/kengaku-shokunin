# Round 97 pre-freeze controls

All commands and fixture revisions are recorded in each `c1-*.txt` / `c2-*.txt` receipt. The fixture is a shared clone outside the lane under `/fast/scratch/hyaku/kengaku-r97/fx`; every Git write names that root, verified with rev-parse. Expected rc was declared in the control runner before invocation. `fixture-refs.json` records revisions; these are fixture identities, not landed lane commits.

C1: do-nothing rc1; positive rc0; wrong cwd rc2; forged receipt lacking DETAIL observations rc1; c1-only rc0; c2-only rc1.
C2: do-nothing rc1 (44 mismatches); positive rc0; blanket demotion rc1; deleted rows rc1; changed self-test cells rc1; appended script spelling rc1; c1-only rc1; c2-only rc0.

The candidate's three complete files are retained under `candidate/` byte-identical to those subsequently frozen. `harm-pre-freeze/` holds BASE and candidate+receipt output for twelve standing checks. All exit codes hold; changed population counters are disclosed, not called repaired. The existing r79 subject mismatch and r78 legacy-ledger drift remain open.
