| mutant | situation | verdict | first semantic delta vs pristine |
|---|---|---|---|
| m01-l7-set-check-dropped | FS | KILLED | `LEGS L1=fail L2=fail L3=fail L4=fail L5=fail L6=fail L7=fail L8=fail L9=fail` → `LEGS L1=fail L2=fail L3=fail L4=fail L5=fail L6=fail L7=pass L8=fail L9=fail` |
| m02-base-absent-empty-set-pass | T,FL,FS | SURVIVES | (all receipts identical to pristine) |
| m03-l5-accepts-extra-cases | FL,FS | KILLED | `LEGS L1=fail L2=fail L3=fail L4=fail L5=fail L6=fail L7=pass L8=fail L9=fail` → `LEGS L1=fail L2=fail L3=fail L4=fail L5=pass L6=fail L7=pass L8=fail L9=fail`; `LEGS L1=fail L2=fail L3=fail L4=fail L5=fail L6=fail L7=fail L8=fail L9=fail` → `LEGS L1=fail L2=fail L3=fail L4=fail L5=pass L6=fail L7=fail L8=fail L9=fail` |
| m04-l6-counts-not-lines | T,FL,FS | SURVIVES | (all receipts identical to pristine) |
| m05-l4-table-read-at-rev | T,FL,FS | SURVIVES | (all receipts identical to pristine) |
| m06-l9-stamps-skipped | FL,FS | KILLED | `LEGS L1=fail L2=fail L3=fail L4=fail L5=fail L6=fail L7=pass L8=fail L9=fail` → `LEGS L1=fail L2=fail L3=fail L4=fail L5=fail L6=fail L7=pass L8=fail L9=pass`; `LEGS L1=fail L2=fail L3=fail L4=fail L5=fail L6=fail L7=fail L8=fail L9=fail` → `LEGS L1=fail L2=fail L3=fail L4=fail L5=fail L6=fail L7=fail L8=fail L9=pass` |
| m07-l2-only-grader-pin | T,FL,FS | SURVIVES | (all receipts identical to pristine) |
| m08-cne-sandbox-collapsed-to-fail | T,FL,FS | SURVIVES | (all receipts identical to pristine) |
| m09-l1-receipt-absent-accepted | FL,FS | KILLED | `LEGS L1=fail L2=fail L3=fail L4=fail L5=fail L6=fail L7=pass L8=fail L9=fail` → `LEGS L1=pass L2=fail L3=fail L4=fail L5=fail L6=fail L7=pass L8=fail L9=fail`; `LEGS L1=fail L2=fail L3=fail L4=fail L5=fail L6=fail L7=fail L8=fail L9=fail` → `LEGS L1=pass L2=fail L3=fail L4=fail L5=fail L6=fail L7=fail L8=fail L9=fail` |
| m10-l3-ancestor-check-dropped | T,FL,FS | SURVIVES | (all receipts identical to pristine) |
| m11-l8-probe-sha-dropped | T,FL,FS | SURVIVES | (all receipts identical to pristine) |
| m12-exit-code-collapsed | FL,FS | KILLED | `rc=1` → `rc=0`; `rc=1` → `rc=0` |
| m13-handler-cne-exit-collapsed | T,FL,FS | SURVIVES | (all receipts identical to pristine) |
