# F35MutLedgerD3 — mutation-test r34_d3 at round-35 tip (wave 2, falsify)

Seat: F35MutLedgerD3 (executor, leaf). Target: `r34_d3` in
`plans/defect_ledger.py:55-66` — the tb2-eval SHA256SUMS manifest must list
`test_outputs.py` and `test.sh`, and every listed digest must equal the file
bytes (`have and not bad`).

Landed tip: `dfee6fff631ebc5f623ba4506e5c7992a215401c` (branch master). The
landed manifest has **6 lines** (the two evaluator entries appended by the wave-1
fix): `antibody.fasta`, `pdb_ids.txt`, `task.toml`, `instruction.md`,
`test_outputs.py`, `test.sh`.

Method: every scenario ran in a fresh fixture clone per the fixture rule
(`git clone --shared --no-checkout` → `sparse-checkout set --no-cone` of
`.ufo/waves/round-34/assimilation/captures/tb2-eval/*`, `plans/defect_ledger.py`,
`corpus/defects.jsonl` → `checkout -q dfee6fff…`; verified both
`rev-parse --show-toplevel` == clone and `rev-parse HEAD` == tip before any
write; no commits; `rm -rf` after). Mutations are plain working-tree edits of
the manifest (the checker reads bytes), so no fixture commit was needed. Checks
run as `python3 plans/defect_ledger.py --lane .` from the clone root. Harness:
`.ufo/waves/round-35/falsify/F35MutLedgerD3/harness.py`; verbatim log:
`run.log` (same dir).

## 1. Baseline — landed state is green (counter agrees)

Lane read-only, at tip:

```
$ python3 plans/defect_ledger.py --lane .        # cwd = lane root
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
(exit=0)
```

Matches the freeze (`rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE
C2 pass`). D3 baseline in a fresh clone: `R34-D3 status=closed observed=pass
agree=yes listed=6 evaluator_listed=True bad=0`.

`sha256sum -c` of the landed manifest, run from the capture directory (the
manifest names are bare, relative to it):

```
$ cd .ufo/waves/round-34/assimilation/captures/tb2-eval && sha256sum -c SHA256SUMS
antibody.fasta: OK
pdb_ids.txt: OK
task.toml: OK
instruction.md: OK
test_outputs.py: OK
test.sh: OK
(exit=0)
```

Invocation caveat (documented, not a defect): the same command run from the lane
root fails with `FAILED open or read` for all six entries, because
`sha256sum -c` resolves the manifest's bare names against cwd. `r34_d3` itself
is immune — it reads `d / "SHA256SUMS"` and resolves listed names via pathlib
under the capture dir, so it does not exhibit this cwd sensitivity.

## 2. Mutants (fresh fixture clone each, at tip commit)

| # | mutation | D3 row (verbatim) | verdict |
|---|---|---|---|
| M1 | flip one hex digit of the `test.sh` digest line (`9ede4664…` → `8ede4664…`) | `R34-D3 status=closed observed=fail agree=NO listed=6 evaluator_listed=True bad=1` | killed |
| M2 | delete the `test_outputs.py` line | `R34-D3 status=closed observed=fail agree=NO listed=5 evaluator_listed=False bad=0` | killed |
| M3 | append a line for a missing file (`<64×0>  missing-probe.txt`) | `R34-D3 status=closed observed=fail agree=NO listed=7 evaluator_listed=True bad=1` | killed |

All three mutants flip the D3 row to `observed=fail agree=NO`: the check's
`bad=` count catches the wrong digest and the missing file, and the
`evaluator_listed` presence test catches the deleted line. Each mutant is
reproducible with: fixture clone at tip → mutate `SHA256SUMS` in the clone →
`python3 plans/defect_ledger.py --lane .` (see `harness.py` for exact code).

Note on the clone-level `rc=1`: the sparse fixture clone omits `SCORECARD.md`,
`.ufo/waves/round-34/build/*.md` and `nec-s091-reopen.html`, so D4/D5 rows
error (`FileNotFoundError`) and the aggregate predicate is red in clones. The
per-row D3 verdict is independent and is the judged artifact; in the real lane
the aggregate counter is green (baseline above).

## 3. Result

`r34_d3` correctly rejects all three mutations of the landed manifest, and the
landed manifest verifies byte-clean under `sha256sum -c` from its own directory.
No disagreement with the frozen claims found. No lane files were modified by
this seat (only scratch + report under `.ufo/waves/round-35/falsify/F35MutLedgerD3/`).
Tooling: no installs made (python3/git/sha256sum built-ins).

VERDICT: d3-killed-3/3
