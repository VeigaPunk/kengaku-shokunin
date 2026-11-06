# MutTesterC1 (round 95) — index

Scoped findings and the full mutant table: `../MutTesterC1.md` (the seat's `Report:` path).
Lane tip under test: T `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239`. Counter under test:
`plans/round95_c1_replay.py`, sha256 `c7e13dc9146ebc1fc3fcd07b404f985ce842e33fdea38c9a4cc21b3b3a7ff3e2`.

## Layout

- `mutants/MUTANTS.tsv` — pristine + 32 mutants: id, after-sha256, substitution count, description.
- `mutants/files/` — the mutant counter bytes (one file per id; `m03+m04.py` is the two-point interaction).
- `tools/gen_mutants.py` — mutant generator; asserts each anchor occurs exactly once in the pristine bytes.
- `tools/drv_mutant_hook.py` — the committed `c1_controls.py` with one change: counter path from env `MUT_COUNTER`.
- `tools/build_fixtures.py` — held-out forgery fixtures (14) on scratch clones of T.
- `receipts/mutant-matrix.tsv` — one row per mutant: committed verdict/designated/leg-only kills, T, held-out flips, status.
- `receipts/runs/pristine/` — pristine driver run (9 controls + do-nothing BASE/P1) and pristine T/BASE/P1 counter outputs.
- `receipts/runs/<mid>/` — per-mutant driver outputs (`controls/c1-*.txt`, `driver.stdout`), plus `T.txt`, `BASE.txt`, `P1.txt`.
- `receipts/matrix/<fixture>/<mid>.txt` — every mutant against every held-out fixture and special invocation
  (`A-dup`, `B1-table`, `B2-table-claims`, `C-swap`, `D-squash`, `E-upstream`, `F-classes-other`, `G-member-classes`,
  `H-c05-lie`, `I-host-python`, `J-host-bash`, `K-host-sed`, `L-solve-tamper`, `M-extra-line`, `UNRESOLVED`,
  `WORK-INSIDE-LANE`, `BROKEN-SANDBOX`).

Every receipt is a plain copy of the counter or driver stdout; `rc=` is the exit code. Scratch paths inside the
receipts are host-local and not citable; the findings cite only the receipts above.
