# R35MutLedgerD3 — attack check r34_d3 (C2 calibration, wave 1)

Seat: R35MutLedgerD3 (executor, leaf). Target: `r34_d3` in
`plans/defect_ledger.py:55-66` — tb2-eval SHA256SUMS must list
`test_outputs.py` and `test.sh` with correct digests.

Method: every scenario ran in a fresh fixture clone per the fixture rule
(`git clone --shared --no-checkout` + `sparse-checkout set --no-cone` of
`.ufo/waves/round-34/assimilation/captures/tb2-eval/*`, `plans/defect_ledger.py`,
`corpus/defects.jsonl`; verified `rev-parse --show-toplevel` = clone; never
committed; `rm -rf` after). Committed state at master (0b3c627) has a **4-line**
`SHA256SUMS` (antibody.fasta, pdb_ids.txt, task.toml, instruction.md) — the
evaluator files are committed (all six files in `git ls-tree`), only the manifest
omits them. Checks run as `python3 plans/defect_ledger.py --lane .`; only the
R34-D3 row is reported (other rows red/error in a fixture clone as expected —
D1 passes, D2/D4/D5 remain red until the wave lands; the row-level verdict is
independent). Harness: `.ufo/waves/round-35/build/R35MutLedgerD3/harness.py`.

## Baseline

```
R34-D3 status=open observed=fail agree=yes listed=4 evaluator_listed=False bad=0
```
(committed 4-line manifest) — D3 red pre-fix, as the freeze claims.

## Exact two lines for the L1 to append (sha256sum, text mode, two spaces)

```
44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582  test_outputs.py
9ede46648fc67c9ce61975503de3e0fcff0b0fb110adc0f9e1d240a608c267b5  test.sh
```
Computed with `sha256sum test_outputs.py test.sh` in the capture dir; identical to
the digests the round-34 spot-check re-verified against upstream
(`round-34-verifier-spotcheck.md:42`) and to the working-tree manifest already
staged by the build wave. The `defect_ledger.py` regex
`([0-9a-f]{64})\s+\*?(\S+)` accepts exactly this format.

## Mutation results (fresh fixture clone each, from committed baseline)

| scenario | mutation | D3 observed | caught? |
|---|---|---|---|
| (a) | append the two correct lines | `listed=6 evaluator_listed=True bad=0` → **pass** | n/a (fix) |
| (b) | test.sh digest wrong (first hex char flipped) | `listed=6 evaluator_listed=True bad=1` → fail | yes |
| (c) | test.sh listed, physical file deleted | `listed=6 evaluator_listed=True bad=1` → fail | yes |
| (d) | only test_outputs.py listed (no test.sh line) | `listed=5 evaluator_listed=False bad=0` → fail | yes |
| (e1) | paths written `./test_outputs.py` `./test.sh` | `listed=6 evaluator_listed=False bad=0` → fail | documented |
| (e2) | `sha256sum -b` style `*` binary marker lines | `listed=6 evaluator_listed=True bad=0` → **pass** | documented |
| (f) | bonus: unlisted task.toml deleted | `listed=6 evaluator_listed=True bad=1` → fail | documented |

Every row above carries the `defect_ledger.py` row line verbatim from the run.

## Documented behaviour (e)

- **`./test.sh` (e1):** the regex captures the literal name `./test.sh`; the
  digest check still resolves it (pathlib normalizes `./`; `d / "./test.sh"`
  → `d/test.sh`, so `bad=0`), but the presence check is an exact key test
  (`all(k in listed for k in ("test_outputs.py","test.sh"))`), so `./`-prefixed
  rows never count and the check stays **red even with correct digests**.
  Append bare filenames, not `./`-prefixed ones.
- **`*` binary marker (e2):** the optional `\*?` in the regex deliberately
  swallows the marker; `sha256sum -b` output is accepted and behaves exactly like
  text mode → **green**. (The commit style is text mode, two spaces — as above.)
- **Unlisted file deleted (f):** `bad` covers every listed row, so deleting any
  listed file (even a non-evaluator one like task.toml) fails the check; deleting
  an *unlisted* file is invisible. The manifest is a complete-file guard.

## Notes for L1 integration

- The ledger rows in `corpus/defects.jsonl` still read `"status": "open"`.
  After appending the two lines, R34-D3 observes pass but agrees=NO (row open)
  → the C2 predicate additionally requires flipping R34-D3 to `closed`
  (closed_round 35). Other rows' fixes land via their own seats.
- No lane files were modified by this seat (only scratch + report under
  `.ufo/waves/round-35/build/R35MutLedgerD3/`).
- Tooling: no installs made (python3/git built-ins; no pacman/uv activity).

VERDICT: d3-mutants-3/3
