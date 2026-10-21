# Round 26 C1 — ExecPerturbCore

- Clone base observed: `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d`; no live lane source, Git index, or jj state changed.
- Clone deliverable: `/tmp/kengaku-r26-ExecPerturbCore/plans/grader_perturb.py`, SHA-256 `3e2c380d8081f30aef1e16383e0321fb19fe601b32774e29636e41cd3923df9a`.
- Implements pinned 1964-record population, format-class strata, deduplicated raw/want and file+pid (C=file+cell+rep) worst-case composites.
- F1/F2 edit only the last matched parseable fence; D1 is PC capture, not a grader verdict. C-MONO follows `valid_latin`; four source pins match, excluded=0; CP95 nominal/descriptive.

## `python3 plans/grader_perturb.py --summary`

FAMILY F1 kind=MP n=1819 k=1802 rate=0.990654 cp95_nominal=[0.985079,0.994547] verdict=PASS composite=194/187@0.963918 cp95_nominal=[0.927072,0.985372] unit=file+pid;C=file+cell+rep composite_verdict=INDETERMINATE
CLASSES F1 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/14@0.452[17/0;14/14]cp95_nominal=[0.273,0.640] DANGLE=0/0@NA[0/0;0/0]cp95_nominal=[0.000,1.000] BARE=0/0@NA[0/0;0/0]cp95_nominal=[0.000,1.000]
FAMILY F2 kind=MP n=1819 k=1802 rate=0.990654 cp95_nominal=[0.985079,0.994547] verdict=PASS composite=194/187@0.963918 cp95_nominal=[0.927072,0.985372] unit=file+pid;C=file+cell+rep composite_verdict=INDETERMINATE
CLASSES F2 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/14@0.452[17/0;14/14]cp95_nominal=[0.273,0.640] DANGLE=0/0@NA[0/0;0/0]cp95_nominal=[0.000,1.000] BARE=0/0@NA[0/0;0/0]cp95_nominal=[0.000,1.000]
FAMILY F3 kind=MP n=1964 k=1964 rate=1.000000 cp95_nominal=[0.998124,1.000000] verdict=PASS composite=210/210@1.000000 cp95_nominal=[0.982587,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES F3 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/31@1.000[17/17;14/14]cp95_nominal=[0.888,1.000] DANGLE=57/57@1.000[17/17;40/40]cp95_nominal=[0.937,1.000] BARE=88/88@1.000[9/9;79/79]cp95_nominal=[0.959,1.000]
FAMILY F4 kind=MP n=1720 k=1720 rate=1.000000 cp95_nominal=[0.997858,1.000000] verdict=PASS composite=158/158@1.000000 cp95_nominal=[0.976923,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES F4 FJ1=1143/1143@1.000[703/703;440/440]cp95_nominal=[0.997,1.000] FJM=488/488@1.000[264/264;224/224]cp95_nominal=[0.992,1.000] MULTI=31/31@1.000[17/17;14/14]cp95_nominal=[0.888,1.000] DANGLE=54/54@1.000[16/16;38/38]cp95_nominal=[0.934,1.000] BARE=4/4@1.000[0/0;4/4]cp95_nominal=[0.398,1.000]
FAMILY F5 kind=MP n=1964 k=1964 rate=1.000000 cp95_nominal=[0.998124,1.000000] verdict=PASS composite=210/210@1.000000 cp95_nominal=[0.982587,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES F5 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/31@1.000[17/17;14/14]cp95_nominal=[0.888,1.000] DANGLE=57/57@1.000[17/17;40/40]cp95_nominal=[0.937,1.000] BARE=88/88@1.000[9/9;79/79]cp95_nominal=[0.959,1.000]
FAMILY F6 kind=MP n=1964 k=1964 rate=1.000000 cp95_nominal=[0.998124,1.000000] verdict=PASS composite=210/210@1.000000 cp95_nominal=[0.982587,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES F6 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/31@1.000[17/17;14/14]cp95_nominal=[0.888,1.000] DANGLE=57/57@1.000[17/17;40/40]cp95_nominal=[0.937,1.000] BARE=88/88@1.000[9/9;79/79]cp95_nominal=[0.959,1.000]
FAMILY F7 kind=MP n=1876 k=1876 rate=1.000000 cp95_nominal=[0.998036,1.000000] verdict=PASS composite=194/194@1.000000 cp95_nominal=[0.981165,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES F7 FJ1=1296/1296@1.000[710/710;586/586]cp95_nominal=[0.997,1.000] FJM=492/492@1.000[268/268;224/224]cp95_nominal=[0.993,1.000] MULTI=31/31@1.000[17/17;14/14]cp95_nominal=[0.888,1.000] DANGLE=57/57@1.000[17/17;40/40]cp95_nominal=[0.937,1.000] BARE=0/0@NA[0/0;0/0]cp95_nominal=[0.000,1.000]
FAMILY D1 kind=PC n=909 k=909 capture_rate=1.000000 cp95_nominal=[0.995950,1.000000] verdict=NOT_SCORED composite=129/129@1.000000 cp95_nominal=[0.971809,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=NOT_SCORED
CLASSES D1 FJ1=639/639@1.000[639/639;0/0]cp95_nominal=[0.994,1.000] FJM=244/244@1.000[244/244;0/0]cp95_nominal=[0.985,1.000] MULTI=0/0@NA[0/0;0/0]cp95_nominal=[0.000,1.000] DANGLE=17/17@1.000[17/17;0/0]cp95_nominal=[0.805,1.000] BARE=9/9@1.000[9/9;0/0]cp95_nominal=[0.664,1.000]
FAMILY G1 kind=MC n=1021 k=1021 rate=1.000000 cp95_nominal=[0.996394,1.000000] verdict=PASS composite=143/143@1.000000 cp95_nominal=[0.974534,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES G1 FJ1=710/710@1.000[710/710;0/0]cp95_nominal=[0.995,1.000] FJM=268/268@1.000[268/268;0/0]cp95_nominal=[0.986,1.000] MULTI=17/17@1.000[17/17;0/0]cp95_nominal=[0.805,1.000] DANGLE=17/17@1.000[17/17;0/0]cp95_nominal=[0.805,1.000] BARE=9/9@1.000[9/9;0/0]cp95_nominal=[0.664,1.000]
FAMILY G2 kind=MC n=1021 k=1021 rate=1.000000 cp95_nominal=[0.996394,1.000000] verdict=PASS composite=143/143@1.000000 cp95_nominal=[0.974534,1.000000] unit=file+pid;C=file+cell+rep composite_verdict=PASS
CLASSES G2 FJ1=710/710@1.000[710/710;0/0]cp95_nominal=[0.995,1.000] FJM=268/268@1.000[268/268;0/0]cp95_nominal=[0.986,1.000] MULTI=17/17@1.000[17/17;0/0]cp95_nominal=[0.805,1.000] DANGLE=17/17@1.000[17/17;0/0]cp95_nominal=[0.805,1.000] BARE=9/9@1.000[9/9;0/0]cp95_nominal=[0.664,1.000]
FORMATS FJ1=1296 FJM=492 MULTI=31 DANGLE=57 BARE=88
DEDUP raw+want+grader unique_raw_want_grader=1451 duplicate_groups=294 records_in_duplicate_groups=807 excess_duplicate_records=513
NOTE CP95 is nominal/descriptive; neither records nor pid-composites establish independent generalization.
TOTAL population=1964 excluded=0 audited_verdicts=15168 policy_checks=909 families_with_interval_verdict=9
COMMAND_EXIT_CODE=0

## `python3 plans/grader_perturb.py --selftest`

The command repeated the identical summary above, then reported:
SELFTEST family cases PASS: F1, F2, F3, F4, F5, F6, F7, D1, G1, G2.
SELFTEST branch cases PASS: F2-CRLF, D1-SEQ, G1-MULTI-LAST, G1-SEQ, G2-SEQ, G1-GRADE-C, G2-GRADE-C, G1-VALID-LATIN, G2-VALID-LATIN.
SELFTEST MUTATION-CATCH PASS caught=12
SELFTEST TOTAL families=10 branch_cases=9 failed=0; RESTORED_RUN_EXIT_CODE=0
RED `python3 plans/grader_perturb.py --selftest` exit=1: F2-CRLF, D1-SEQ (PC n 909→892), G1-MULTI-LAST (1004/1021; MULTI 0/17), G2-SEQ (1000/1021); G2-VALID-LATIN also caught the same list no-op mutant.
## Retained evidence and scope

- Four source SHA-256 pins match; population candidate count and accepted count both equal 1964, with excluded=0 (otherwise exit 1).
- LSP unavailable in the mounted tool inventory; source references were read with `grep`/`read`.
- The separate oracle is being amended by its writer with the exact F1/F2 and D1 semantics sent to that seat. No tools installed.

VERDICT: Summary/selftest green after restore; all four targeted mutants were killed, with G2 also caught on the valid_latin list case.