# F35MutRowsIndex — rows/index mutation battery (round 35, wave 2 FALSIFY)

Date: 2026-10-25 · Lane tip under test: `dfee6fff631ebc5f623ba4506e5c7992a215401c` (master).
Target: the C1 rows/index invariant chain (SOURCES rows S105–S107, README index row, coverage bullet, 42-file knowledge census) and whether the landed detectors notice when it breaks.

## Fixture

Exactly per the fixture rule (driver: `/tmp/k35f-mutrows-mutprobe.py`, results `/tmp/k35f-mutrows-results.json`):

```
D=$(mktemp -d /tmp/k35f-XXXX)                 # -> /tmp/k35f-4a6iums8
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone --stdin   # SOURCES/README/knowledge/round35 evidence/plans probes + every mined used-by path
git -C "$D/lane" checkout -q dfee6fff631ebc5f623ba4506e5c7992a215401c
git -C "$D/lane" rev-parse --show-toplevel    # == /tmp/k35f-4a6iums8/lane (guard passed; never the live lane)
git -C "$D/lane" rev-parse HEAD               # == dfee6fff631ebc5f623ba4506e5c7992a215401c
git -C "$D/lane" ls-files 'corpus/knowledge/*.md' | wc -l   # 42
```

Pristine bytes (sha256, verified identical after every restore):

- `corpus/SOURCES.md` = `a00684a42d0effda23a036fadf35e1657646b3a66cd2c7b00755e69de491da1a`
- `corpus/README.md`  = `fd5568b83e73ea37237c39376c7bd0f69d5b04a5ba97a8013e800c57d4f03f56`

`rm -rf /tmp/k35f-4a6iums8` (exact path only) at the end.

## Detectors (same three on pristine, mutated, and restored bytes)

1. C1 counter (frozen predicate): `python3 plans/round35_c1_verify.py --lane .` in the fixture clone.
2. Census validate: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $D/lane/corpus/SOURCES.md` (the mode the counter's own V6 uses for a fixture lane).
3. Census census: `... sources-census.sh census --file $D/lane/corpus/SOURCES.md` (row/tier/status counts).

## Baseline (pristine) — both detectors green, so verdicts below are conclusive

- Counter: `checks=6 defects=0` + `PREDICATE C1 pass`, rc 0. (V5 replays the probe receipt via `uv run --with biopython==1.85`.)
- Census validate rc 0, output is W04 warnings only (pre-existing, e.g. `file W04 S040 duplicate url arxiv.org/abs/2301.09633 across scopes`), no E-codes.
- Census `--file`: `rows 100, tier.A 85, tier.B 13, tier.C 2; status mined 84, queued 8, rejected 8`.

## Mutants — one behavior-bearing point each, restored to pristine bytes after each run

| # | Mutation | Mutated sha256 (changed file) | Counter output | Census validate | Verdict |
|---|---|---|---|---|---|
| M1 | S106 used-by gains a second existing path: `…grader.md, corpus/README.md` | SOURCES `9733a73a…cd9cd09` | rc 1, `V2 DEFECT S106 used-by 'corpus/knowledge/tb2-protein-assembly-grader.md, corpus/README.md'`, `checks=6 defects=1`, `PREDICATE C1 fail` | rc 0, W04-only | **killed** (by counter; census survives — E11 only checks path existence per comma part) |
| M2 | S107 opened `2026-10-25` → `2026-10-24` | SOURCES `b44125c1…925af9` | rc 1, `V2 DEFECT S107 tier/status/opened = A/mined/2026-10-24`, fail | rc 0 (2026-10-24 is a legal past date, E08 silent) | **killed** (counter) |
| M3 | S105 source URL gains `?raw=1` | SOURCES `f55eee7c…6645b0` | rc 1, `V2 DEFECT S105 source URL […test_outputs.py?raw=1'] != […test_outputs.py]`, fail | rc 0 (URL stays unique; E04/W04 silent) | **killed** (counter) |
| M4 | README index row loses S107 (now `S105, S106 (terminal-bench-2 @ 2fd12b88)`) | README `8bc1279d…ab63150` | rc 1, `V4 DEFECT index row absent or missing S105/S106/S107`, fail | rc 0 (census never reads corpus/README.md) | **killed** (counter) |
| M5 | coverage-map bullet renamed to `knowledge/tb2-protein-assembly-grader-renamed.md` | README `dbc69190…3ca55e` | rc 1, `V4 DEFECT coverage-map bullet absent`, fail | rc 0 | **killed** (counter) |
| M6 | stub 43rd knowledge file `corpus/knowledge/zzz-stub-round35-mutation.md` added (`git add` in the clone) + README index row | README `36fbbb28…5ec0d9c`; knowledge files 43, index rows 43 | rc 1, `V4 DEFECT knowledge files=43 index rows=43 (want 42/42)`, fail | rc 0 | **killed** (counter) |

Each mutation tripped exactly one check (V2 ×3, V4 ×3) — the counter's checks are single-point sensitive, no collateral defects.

## Calibration finding

`sources-census.sh` in both `--file` modes is **insensitive to all six mutants**: validate rc 0 with W04-only output every time, and `census --file` metrics identical to baseline (`rows 100 / tier.A 85 / B 13 / C 2 / mined 84 / queued 8 / rejected 8` for every run, including M1–M6). The census constrains shape (E01–E12) and freshness, not row content, pinned URLs, index membership, or the 42/42 files==index clause. For the C1 claim, `plans/round35_c1_verify.py` is the load-bearing detector; its V2 (exact used-by match, exact opened date, exact pinned URL) and V4 (index row S105+S106+S107, coverage bullet, 42/42) are what hold the rows/index contract. Coverage finding, not a contract change: the census was never claimed to check these.

## Restoration evidence

After every mutant: both files re-hashed == pristine values above; `git ls-files corpus/knowledge/*.md` back to 42; M6 stub gone from worktree and index; detectors re-run on restored bytes returned to baseline green (`PREDICATE C1 pass`, census validate rc 0) in all six cases (`restored_ok`/`restored_green` true in `/tmp/k35f-mutrows-results.json`). No file outside the fixture clone or this report was written; no installs were needed.

VERDICT: rows-index-killed-6/6
