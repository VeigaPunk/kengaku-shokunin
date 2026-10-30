# Round 55 — kengaku lesson (hyaku run 11, 2026-10-30)

author: kengaku L1 (KengakuR55). Frozen claims: `plans/round-55-claims.md` (freeze commit
`80afa613`, base `798f5e9e`). Wave evidence: `.ufo/waves/round-55/`.

## Gate

Sources opened this round (2026-10-30, read tool and `curl` GET of pinned raw URLs). The two rows
below are PROPOSED: the registry append (`corpus/SOURCES.md`) was an un-settled wave-1 seat edit
and is NOT committed, so neither row is landed registry state at this round's honest stop. The
decisions record what was opened, not what the registry holds.

| row | URL and location | access date | located quote (at most 25 words) | decision |
|---|---|---|---|---|
| S201 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/tests/test_outputs.py — tests/test_outputs.py:25 | 2026-10-30 | `assert sorted(move) == sorted(["g2g4", "e2e4"]), "File is wrong"` | admit A — executed scoring predicate of this task's grader for its own behaviour |
| S202 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/instruction.md — instruction.md:1 | 2026-10-30 | `If there are multiple winning moves, print them all, one per line.` | admit A — maintainer requirement the grader is mapped against |

Upstream identity (fetched and sha-pinned this round; receipt `.ufo/waves/round-55/claims/`
and the wave `E14CaptureIdentity` output): `chess-best-move/tests/test_outputs.py` sha256
`a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286`; `tests/test.sh` sha256
`4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334`; `instruction.md` sha256
`6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a`.

Dropped planned row (amendment A1, pre-dispatch): the runner `chess-best-move/tests/test.sh` is
byte-identical to the regex-log runner already held as S109 (same sha256), so no new row; the
entry cites S109 for runner semantics.

Flip check: no existing row's `status`, `recheck` or `used-by` cell changes this round unless
logged below. Rejections this round: none yet (the wave's distiller/critic output is pending).

Admit/reject spot-check (LEARNING.md discernment): pending the non-author closure. The round's
gate decisions to sample: admit S201, admit S202, the dropped runner row (reject-as-duplicate),
and the reject of "full-multiset = new class" framing if C4 ruled it a re-label.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| counter computes a verdict leg and never wires it into the predicate (`entry_mode_ok` in `plans/round54_c2_entrytruth.py` is called nowhere in `evaluate`'s predicate) — laundering routes: abbreviated argparse flag and `uv run … python3 -c` decoy both pass with PREDICATE pass while the registry entry exits 1 | `.ufo/waves/round-54/w1/R2C2Counter/laundering-probes.txt`; `plans/round54_c2_entrytruth.py` (predicate at its `evaluate` tail); round-54 closure §2 | none — the round-54 counter's own selftest (cases 1–3) and the r54 closure did not exercise either route; the closure reproduced it from the reviewer's probes only | R55-C2: binding legs L1–L4 in `plans/round55_c2_entryargv.py`; fixture red-before `.ufo/waves/round-55/claims/c2-before-*.txt` (both `PREDICATE R54-C2 pass`, exit 0, true entry exit 1) |
| registry advertised two counters (`round54_c1_anchor.py`, `round54_c2_entrytruth.py`) without rows — the round-52 closure counter went red (`MISSING 2`) | `.ufo/waves/round-55/claims/c1-before.txt`; `.ufo/waves/round-54/integrate/round52-c2-regression.txt` | none — no check ran the registry counter after the round-54 LOG/SCORECARD landed | R55-C1 registry rows; the frozen after-predicate reruns the round-52 counter at the landing revision |
| sizing error at wave build: the first E5 item exceeded the 4096-byte item cap and a `sonic` role is not a swarm role — both refused at `plan`, nothing dispatched | `.ufo/waves/round-55/build_spec_w1.py` history (two refusals reproduced in-round) | the validator, caught at `plan` (the designed gate) | shortened the case table to the frozen 12 rows; remapped `sonic` seats to `scribe`/`scout` (sonic is not a swarm role) |

## Frontier step — sourced claim

NOT LANDED at this honest stop. R55-C3's sourced claim (S201/S202 rows and the
`corpus/knowledge/tb2-chess-best-move-grader.md` entry) exists only as un-settled wave-1 seat
output and is not committed. The round files no sourced claim as landed.

## Assimilation

`Assimilation: none` — the `merge/kengaku/` package mass id drift (114 of 190 registry/175 staged
ids collide, L0 `kengaku | round-54`) is unanswered; nothing is adopted and no staged row is appended.

## Measurement and limits

Pending the wave close. The round's claims are frozen before data; this section records what the
measured close will say, not what it says yet.
