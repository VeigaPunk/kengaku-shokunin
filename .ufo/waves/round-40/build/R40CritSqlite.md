# R40CritSqlite — the host-vs-image SQLite limit on round 40's C2 receipt

Seat `R40CritSqlite` (critic), kengaku round 40, wave 1 of 2, 2026-10-26. Attacked surface: the C2 receipt
`corpus/evidence/round40/db-wal-probe.txt` and the sentence that licenses it, `plans/round-40-claims.md:88`
— "host sqlite3 3.54.0 / python3 / xxd stand in for the image's Ubuntu 24.04 packages; the image is never
pulled". No lane file was edited; everything below is a finding, not an integration.

## Answer

**No verdict differs.** All 28 frozen cases produce the same seven-letter test string — and the receipt text is
byte-identical — under the task's own declared image (Ubuntu 24.04.3, python 3.12.3, SQLite 3.45.1), a
3.40.1 bracket, and this host (python 3.14.8, SQLite 3.54.0). The five cases named in the assignment
(`plain-read-then-solve`, `xor-wrong-key`, `decrypt-checkpoint-truncate`, `decrypt-then-extract`,
`oracle-solve-sh`) are stable, and so are the mechanisms behind them: the destructive plain read, the
wrong-key WAL rejection, decryption, and WAL checkpoint all behave the same at 3.40.1 and 3.45.1 as at 3.54.0.

## Environments actually executed (measured, not assumed)

| environment | OS | python | `sqlite3.sqlite_version` | CLI | how obtained |
|---|---|---|---|---|---|
| this host | Arch, kernel 7.2.11 | 3.14.8 | 3.54.0 | `3.54.0 2026-10-09` | system |
| `ubuntu:24.04` + apt | Ubuntu 24.04.5 LTS | 3.12.3 | 3.45.1 | `3.45.1 2024-01-30` | `docker build`, `apt-get install python3 sqlite3 xxd` |
| `debian:bookworm` + apt | Debian 12 | 3.11.2 | 3.40.1 | `3.40.1 2022-12-28` | same |
| **task image** | Ubuntu 24.04.3 LTS | 3.12.3 | **3.45.1** | `3.45.1 2024-01-30` | pulled `alexgshaw/db-wal-recovery:20251031` (`task.toml:29`) |

The last row is the image the task actually runs (`Dockerfile:3` is `FROM ubuntu:24.04`, so the apt route and
the image agree). Its `/app/main.db` and `/app/main.db-wal` hash to the capture digests exactly
(`68cb288e…`, `68753bdce…`), so the image ships the same bytes the probe captured.

`uv`-managed interpreters cannot supply this bracket — every locally installed one bundles a **newer** SQLite
than the image: `3.11.17`, `3.12.15`, `3.13.16` → `sqlite 3.53.1` each (measured with
`python3.x -c 'import sqlite3;print(sqlite3.sqlite_version)'`). A real Ubuntu 24.04 userland was needed.

## Method

The frozen probe was not modified. `docker_runner.py` imports `plans/db_wal_probe.py` (digest `69af65df…`,
matching `.ufo/waves/round-40/claims/frozen-digests.txt:4`) and reuses its `CASES`, `MK_PY`, `HARNESS_PY`,
`PINS` and `overall()` verbatim; only the sandbox changes (bwrap with host `/usr` → docker image with the
image's own `/usr/bin/python3`, `/usr/bin/sqlite3`, `/usr/bin/xxd`). `docker_runner_taskimg.py` does the same
for the task image, which lacks `/cap` and `/k`, by copying the same harness inputs in from a read-only `/w`.
Recipes, seeding, `bash -euo pipefail`, seven-test import order and the double (regrade) grading are the
probe's own code paths, so a difference can only come from the toolchain.

Baseline control: the unmodified probe was also run on a `git clone --shared` of the lane
(`HEAD 3077adbc…`) with `--work` under the seat scratch. It reproduced the committed receipt **byte for byte**:
`sha256sum` gives `c74c6b91c8c49b1788f2dd7aa0d66edce0db0b52b549baf89ce69cfa8e2a730e` for both my run and
`corpus/evidence/round40/db-wal-probe.txt`, and `cmp` prints nothing (`FULL-BYTE-EQUAL`). Three consecutive
host runs were also byte-equal to each other.

## Results

### 1. All 28 cases, four environments, one receipt

The bodies (everything but the `#` header) of the host run and the three container runs hash identically:

```
d0a46c023a8d17a102133580b3842d3d5ea3a287f59b047287f96e43e34feb4f  body-host.txt
d0a46c023a8d17a102133580b3842d3d5ea3a287f59b047287f96e43e34feb4f  docker-3.40.1.txt
d0a46c023a8d17a102133580b3842d3d5ea3a287f59b047287f96e43e34feb4f  docker-3.45.1.txt
d0a46c023a8d17a102133580b3842d3d5ea3a287f59b047287f96e43e34feb4f  docker-taskimg.txt
```

Each run ends `cases=28 observed_pass=8 observed_fail=20 mismatches=0` and `regrade cases=28 differ=0`.
So the image is not merely prediction-compatible: it reproduces the same 28 predictions, the same 8/20 split
and the same re-grade stability column.

### 2. The five SQLite-behaviour-dependent cases (receipt lines 8, 10, 11, 12, 13)

| case | tests (identical in all four envs) | verdict |
|---|---|---|
| `oracle-solve-sh` | `PPPPPPP` | pass |
| `plain-read-then-solve` | `PPPPFPF` | fail |
| `xor-wrong-key` | `PPPPFPF` | fail |
| `decrypt-then-extract` | `PPPPPPP` | pass |
| `decrypt-checkpoint-truncate` | `PPPPPPP` | pass |

These are the receipt's own letters (`corpus/evidence/round40/db-wal-probe.txt:8,10,11,12,13`), reproduced on
3.45.1 and 3.40.1 without a single flipped test.

### 3. Mechanism, measured per version

`mech.sh` seeds the same `/app` for each variant and prints row counts and WAL presence after the same
operations the recipes perform (`mech-host.txt`, `mech-taskimg.txt`, `mech-docker.txt`):

| variant | 3.40.1 | 3.45.1 (image) | 3.54.0 (host) |
|---|---|---|---|
| A plain read-write `sqlite3` SELECT | 5 rows, WAL **deleted** | 5 rows, WAL **deleted** | 5 rows, WAL **deleted** |
| B `mode=ro` read | 5 rows, WAL kept (16512 B) | same | same |
| C XOR 0x43 then read | 5 rows, WAL deleted, no error | same | same |
| D XOR 0x42 then read | 11 rows | 11 rows | 11 rows |
| E XOR 0x42 + `wal_checkpoint(TRUNCATE)` | 11 rows, WAL gone | same | same |
| F `solve.sh` (oracle) | rc 0, JSON 11 rows | same | same |
| G plain read then `solve.sh` | rc 0, JSON **5** rows | same | same |

The receipt's causal sentence for `plain-read-then-solve` — a plain read-write open destroys the encrypted WAL
(`plans/db_wal_probe.py:39`) — holds identically back to 3.40.1: the WAL file is deleted, not merely ignored,
which is why the later oracle recovers only the 5 base rows (variant G).

### 4. The other stand-in, `xxd`

Host carries `tinyxxd 1.3.17`, the image carries `xxd 2023-10-25 by Juergen Weigert et al.` (vim-common); both
print `753d44` for `xxd -l 3 -p main.db-wal.encrypted`. `solve.sh` prints that value but never compares it
(`corpus/evidence/round40/tb2-db-wal-recovery/solve.sh:8` only narrates the read-only query), so it cannot
reach any verdict.

## Counterexample search (what would have had to be true for a difference)

Tried and refuted:

1. *A newer SQLite applies the decrypted WAL differently.* Refuted: 11 rows at 3.40.1/3.45.1/3.54.0, and the
   frames survive intact — no checksum/salt rejection at any of the three versions.
2. *A plain read-write open stops deleting the undecryptable WAL at some version.* Refuted: deletion at all
   three versions, with no error output.
3. *An invalid-magic WAL makes an older SQLite error out instead of being ignored, changing the recipe exit.*
   Refuted: zero stderr, 5 rows, recipe rc 0 in every environment (variant C).
4. *`wal_checkpoint(TRUNCATE)` behaves differently older.* Refuted: 11 rows and the WAL consumed in all three
   (variant E).
5. *Python-version JSON semantics flip a grader test* (ints vs floats, `True` as int, string ids). Refuted:
   host 3.14.8 and image 3.12.3 produce identical letters for `truth-ids-as-floats`, `truth-value-float-id1`,
   `truth-bool-value-id5`, `truth-ids-as-strings`, `truth-wrapped-object`.
6. *Docker (root, bridge-less) vs bwrap changes file outcomes.* Refuted: the identical receipt body; runs used
   `--network none`, which the recipes do not need.

No candidate survived. The strongest available counterexample — 3.40.1, four minor versions older than the
image — agrees with the host on every case.

## Residual limits (what this measurement does not establish)

- **Patch drift inside 3.45.1.** The pinned image was built 2025-10-24 and my `ubuntu:24.04` image today; both
  report `3.45.1`. Since behaviour is identical across 3.40.1…3.54.0, a patch-level delta cannot flip a verdict;
  a *rebuilt* image with a different SQLite minor would need this re-run, not a new argument.
- **pytest-vs-direct-call substitution.** The probe imports `test_outputs.py` and calls the seven functions
  directly, while `test.sh` runs them under `pytest 8.4.1`/`uvx -p 3.13`. The seven tests touch only `json`
  and `os`; SQLite cannot re-enter after the recipe. That substitution is a different axis and is not measured
  here (it is named in the probe docstring as a limit and belongs to the C2 entry's own prose).
- **Sandbox identity.** Docker replicas differ from bwrap in uid (root vs the probing user) and namespaces;
  the byte-identical receipts make this immaterial for these cases.
- Only the operations the 28 cases exercise were compared; other SQLite behaviours are not covered by this
  probe in any version.

## Impacted axes and smallest safe correction

- **Coverage** (C2): the limit at `plans/round-40-claims.md:88` is empirically discharged — the entry can say
  the declared image was pulled and re-run with 28/28 identical verdicts, instead of only naming a stand-in.
  The claim stays frozen; this is entry prose for the L1, not a claims edit.
- **Freshness**: the receipt reproduces today, byte for byte, on the host and in the image — the receipt is not
  a one-day artifact.
- **Depth**: the mechanism table now backs the receipt's causal sentences (WAL deletion, wrong-key rejection,
  checkpoint) at the image's own version.

Smallest safe correction: one sentence in the (unfrozen) `corpus/knowledge/tb2-db-wal-recovery-grader.md`
limits paragraph — name the pulled image digest and the measured 28/28 equality, and keep the host stand-in
listed for the parts not re-measured (pytest runner, root uid). No frozen artifact changes; the probe, counter,
spec, gate, dry table, captures, receipt and claims all stay as filed.

## Reproducibility

Receipts and the exact runners are in this directory (`host-3.54.0.txt`, `docker-3.45.1.txt`,
`docker-3.40.1.txt`, `docker-taskimg.txt`, `mech-host.txt`, `mech-docker.txt`, `mech-taskimg.txt`,
`docker_runner.py`, `docker_runner_taskimg.py`, `mech.sh`). Commands:

```
git clone -q --shared .../kengaku-shokunin $S/lane            # HEAD 3077adbc7145726519f60f01426a5d03381ad444
(cd $S/lane && python3 plans/db_wal_probe.py --lane . --work $S/probe-host)
python3 docker_runner.py          --lane $S/lane --image r40sqlite:u2404 --work $S/w-u2404
python3 docker_runner.py          --lane $S/lane --image r40sqlite:bookworm --work $S/w-bw
python3 docker_runner_taskimg.py  --lane $S/lane --image alexgshaw/db-wal-recovery:20251031 --work $S/w-taskimg
docker run --rm --network none -v mech.sh:/mech.sh:ro -v <captures>:/seed:ro -v <captures>:/cap:ro <image> bash /mech.sh
```

Scratch (`/fast/scratch/hyaku/kengaku-r40/R40CritSqlite`, including the shared lane clone) is removed before
this report is filed; the copies above are the only retained artifacts. No lane file, lane index, jj state or
sibling lane was written.

## Tooling record (operator directive 2026-10-19)

- Pulled `alexgshaw/db-wal-recovery:20251031` (`sha256:0e33ea5ec823975d1bd6c3778395c9f94251dd88f571146057bff6adb7e4594e`)
  — the image `task.toml:29` declares — reason: turn the "image is never pulled" limit into a measurement;
  channel: Docker Hub image pinned by the captured task definition.
- Built two local verification images from `ubuntu:24.04` and `debian:bookworm` plus their distro
  `python3`/`sqlite3`/`xxd` packages; reason: the 3.45.1 and 3.40.1 brackets. pacman was not run; no host
  package was installed or changed.

VERDICT: sqlite-version-same
