ATTACKS: Independently parse the last r21–r23 GT scoring table per receipt; compare counts with calibration JSON and the awk oracle.

- P1 means the last score block; no-block receipts are trial-only; identical tables are deduplicated (`plans/round-25-claims.md:28-33`). Calibration selects `blocks[-1]` and records raw rows/scored/correct (`plans/attrib_calibration.py:519-550`); the oracle prints these counts and per-leg/prediction maps (`plans/fixtures/r25/attrib_oracle.sh:283-322`).
- Wrote throwaway, header-driven Node parser only at `/tmp/k25w2-ThirdParserExec/third_parse.mjs`; SHA-256 `5cb7ef23138446defe67ccd646e79824645f09ab26c6818e42432e62f413f69f`; Node `v24.21.0` already present.
- Command: `node /tmp/k25w2-ThirdParserExec/third_parse.mjs /home/vgpnk/Projects/shokunin/kengaku-shokunin` -> `COMPARISON files=9 calibration_json=5 oracle=9 disagreements=0 calibration_mismatches=0`; every per-file row printed `calibration_json=MATCH` and `oracle=MATCH`.
- Trial-only, all n=0/correct=0, GT/prediction empty, classes empty: `attrib-r21-ds-trials.log`, `attrib-r21-glm-trials.log`, `attrib-r22-legs-hyper.log`, `attrib-r23-stream-trials.log`.
- `attrib-r21-impl-ds-trials.log`: n=20, correct=20; GT/pred `{alibaba-token-plan:20}`; classes `[std]`.
- `attrib-r21-impl-glm-trials.log`: n=22, correct=22; GT/pred `{devin:9,zai:13}`; classes `[err,std]`.
- `attrib-r22-legs.log` and `attrib-r22-opencode-trials.log`: each n=20, correct=20; GT/pred `{alibaba-token-plan:10,hyper:10}`; classes `[force-hyper,force-opencode-go]`.
- `attrib-r23-stream.log`: n=30, correct=30; GT/pred `{alibaba-token-plan:6,hyper:24}`; classes `[stream-stream-hint,stream-stream-inspection,stream-stream-marker]`.
- Direct `sh plans/fixtures/r25/attrib_oracle.sh --root /home/vgpnk/Projects/shokunin/kengaku-shokunin`: all 5 scored blocks passed stored-line checks (4/4, 4/4, 6/6, 6/6, 8/8); `TOTAL files=9 with_block=5 trial_only=4 scored=112 correct=112 unique_samples=4 dedup_scored=92 dedup_correct=92 files_with_mismatch=0`. The 20-row r22 legs/opencode pair is the reported duplicate; 112 raw per-file rows versus 92 after the frozen dedup rule is expected, not a parser disagreement.
- Class values are the independent parser's additional raw-table field; the comparison tools do not print this field. No excluded rows occurred in the scored tables.
- Files changed: this report only. Installs: none.

VERDICT: SURVIVES — third parser agrees on all shared per-file counts/distributions; no counterexample found.