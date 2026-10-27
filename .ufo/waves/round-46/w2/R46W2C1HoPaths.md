# R46W2C1HoPaths — filesystem-shape falsification

Axes: calibration (primary); filesystem-path coverage (evidence family).

Counterexample module: `links_special_names.py`, a new held-out module, not a refusal/sealed variant. It builds four accepted-order fixtures with lane-local ordinary tracked input/output plus (1) hard link alias, (2) dangling symlink, (3) FIFO, or (4) newline-containing filename. The first three were rejected by the fence; the newline filename was admitted. It is the smallest surviving counterexample: a non-Git repository filename with an embedded newline remains admissible although the fence rejects newline in `--lane` itself.

Evidence/command: `receipt.txt`; executed under the required envelope on clone HEAD `42d5043afac952fcb43bf4798757785dd258cf85`. Output: PINS 65/65; four fixtures built; hardlink, dangling symlink, FIFO each BREACH; newline fixture ADMIT. Module summary `LEAKED fixtures=4 admitted=1 hung=0 touches=0`; `read=0`. HONEST 104/104 admitted, 0 refused/read/hung/build errors. The overridden one-module refusal set makes the aggregate frozen predicate fail on expected cardinality; this is not a claim about the frozen C1 run.

Counts: modules written=1; admitted=1; read=0. Status per module: LEAKED. Filesystem-family observations: hardlink and special-file classes were detected; dangling symlink was detected; unusual newline filename was not refused.

Smallest safe correction: extend the lane-tree name validation to reject newline-bearing entry names, using the same explicit name policy applied to argv paths. Re-run the pinned counter and honest battery after incorporating this check. Impact: calibration remains falsified under the stated held-out kill rule (one admitted/read module is below the threshold of two); family coverage reveals a specific unguarded path-shape case, not enough alone to reject C1.

Receipt: `.ufo/waves/round-46/w2/R46W2C1HoPaths/receipt.txt`.
VERDICT: heldout-paths-1-admitted-1-read-0