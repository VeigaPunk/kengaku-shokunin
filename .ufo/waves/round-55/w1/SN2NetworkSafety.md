# SN2NetworkSafety — network-use receipt, kengaku round 55 wave 1

Seat `SN2NetworkSafety` (role: sentinel) · kengaku round 55, wave 1 (v2) · lane `kengaku-shokunin`.
Lane HEAD at inspection: `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (the claims freeze commit).
Read-only seat: no lane file was edited, no git mutation was run, no subagent was spawned.

**Verdict: every fetch a round-55 *seat* performed is an unauthenticated read-only GET. No
seat fetch POSTs, authenticates, or reaches a model-serving endpoint. The three scripts the
round builds are offline-only — proven at runtime, not only by grep. BUT the R55-C2
counter's own after-run performs an out-of-scope PyPI GET through an inherited registry
row: one violation, named below.**

Full receipt (per-file verdicts, evidence, defects): **`.ufo/waves/round-55/w1/SN2NetworkSafety/network.md`**.
Seat report (commands + exit codes, files written, defects, dead ends): **`.ufo/waves/round-55/w1/SN2NetworkSafety/report.md`**.

## Per-file verdict

| file / path | verdict |
|---|---|
| `plans/round55_c3_chess_probe.py` | **offline-only** — no `urllib/requests/socket/http`; full 12-case battery under `strace -f -e trace=network` → **0** AF_INET/connect/getaddrinfo; bwrap `--unshare-all` gives a real netns (`Network is unreachable`) |
| `plans/round55_c2_entryargv.py` | **offline-only** — `--selftest` under strace → exit 0, inet hits 0 |
| `plans/round55_c2_controls.py` | **offline-only** — `--selftest` and both fixture cases under strace → inet hits 0 (the fixture's `uv` argv carries `--offline`) |
| `corpus/knowledge/tb2-chess-best-move-grader.md`, `corpus/lessons/round-55.md`, `corpus/SOURCES.md` S201/S202, `corpus/evidence/round55/chess-best-move-probe.txt` | **offline-only** (data; the URLs are provenance citations, no fetch code, no URL in the receipt) |
| E14 planned GETs (`raw.githubusercontent.com`, `api.github.com/…/commits/<pin>`) | **read-only-GET-in-scope** — unauthenticated public GET, no `--data`/`-X POST`/token |
| SC1 planned GETs (`api.github.com` contents/trees, `raw.githubusercontent.com`, `github.com` blob) | **read-only-GET-in-scope** — ≈1.02 MB, no auth; note: it also fetched upstream `solution/solve.sh` although its item scoped the solution dir to "names only" (read-only GET, body not committed, kill rule (b) unaffected) |
| R3 planned GETs (re-open the two pinned raw URLs) | **read-only-GET-in-scope** — unauthenticated GET, allow-listed host |
| SC3 planned work | **offline-only** — local re-scan of `SKILL.md` + ledger, no GET planned |
| `plans/round52_c2_registry.py` (the C1 counter) | **offline-only** — no network import, no URL, no subprocess network verb |
| `plans/round54_c1_anchor.py` `verify` / `selftest` | **offline-only** — `opentimestamps.core` has no network import; receipts read from disk |
| `plans/round54_c1_anchor.py` `stamp` / `upgrade` | **out-of-scope if run** (they talk to OTS calendars; `calendar.py` POSTs a digest) — **not invoked by any seat** (wave-wide grep → no hit) |
| executed registry rows `attrib-probe` / `catalog-probe` / `round51-surfaces` | **read-only-GET-in-scope / loopback-only** — measured: `freeze-check` 0 inet, `--verify` 0 inet, surfaces 8 hits all to `127.0.0.1` |
| `tb2-grader-probe` row (`uv run --with biopython==1.85`) | **out-of-scope fetch if executed** (proven `CONNECT pypi.org:443`), but **the round-55 counter does not execute it** — L1+L2 binding legs exclude it twice |
| **`round35-c1-coverage` row — executed by the round-55 counter → PyPI** | **VIOLATION: out-of-scope fetch actually performed** (see below) |
| S2 prior-art web search | **read-only-GET-in-scope** — public raw/openreview/arxiv/HF-dataset hosts, no auth, no model endpoint |
| all other 66 seat items | **no fetch planned** — host census over the whole dispatch: `raw.githubusercontent.com` ×2, `api.github.com` ×1 only |

## The one violation — the R55-C2 after-run GETs PyPI

`python3 plans/round55_c2_entryargv.py --lane . --source . --work <scratch> --jobs 3`
executes 61 registry rows. One is **`round35-c1-coverage`**
(`python3 plans/round35_c1_verify.py --lane .`), whose V5 leg falls back to
`uv run --no-project --with biopython==1.85 …` when `import Bio` is unavailable — and `uv`
then GETs **`pypi.org` / `files.pythonhosted.org`**, hosts **outside this round's allow-list**
(`raw.githubusercontent.com` / `api.github.com` / docs sites).

* **Measured:** the counter's own `strace -f -e trace=network` shows **8 × `:443` connects to
  `151.101.{0,64,128,192}.223` and `2a04:4e42::223`** — exactly `pypi.org` /
  `files.pythonhosted.org` — with **1 959 TLS records read back** on those sockets (a real TLS
  session, not a failed connect).
* **Attributed to that one row:** every other network-capable row run alone through the
  counter's own `hermetic_env`+`Worker`+`run_row` path gave **0** external connects; only
  `round35-c1-coverage` refreshed `~/.cache/uv/simple-v26/pypi/biopython.rkyv` (mtime
  `13:17:05` → `13:28:40` across exactly that row's run).
* **Reproduced with an explicit record:** cold `UV_CACHE_DIR` + a loopback recording proxy →
  **`CONNECT pypi.org:443 HTTP/1.1` ×4**.
* **Pre-existing and inherited:** `plans/round35_c1_verify.py` is unchanged since round 35,
  the row is in the base-tip ledger, and the unchanged **r54** counter reaches PyPI via **two**
  rows — round 55 *reduces* it to one (the binding legs exclude `tb2-grader-probe`).
* **Already disclosed** in that row's registry scope cell: "*when `Bio` is not importable it
  runs the probe under `uv run --no-project --with biopython==1.85`, **which reaches the
  network***".
* **Not** a POST, **not** authenticated, **not** a model-serving call — out of scope by
  **host**, not by method.
* **Smallest remediation** (not applied; not my file): add `UV_OFFLINE=1` to the counter's
  hermetic env next to the existing secret-scrubbing (one line, closes the whole uv/PyPI
  class); or `--offline`/vendored wheel at `plans/round35_c1_verify.py:168`; or exclude that
  row from the executed set. Owner: E2/E4/L1.

## Named defects / notes (reported, not fixed — other seats own these files)

1. `plans/round54_c1_anchor.py selftest` is **not runnable from a clean clone** here:
   `ModuleNotFoundError: opentimestamps` (library only inside the `opentimestamps-client` uv
   tool env). Network-safe (fails before any network use). E11 already reports it against C1
   leg 2. Owner: E1/E11/L1.
2. **Latent PyPI reach** via the `tb2-grader-probe` row's `uv --with` entry — round 55 does not
   execute it (binding legs exclude it), but the **r54** counter's `entry_mode_ok()` tolerates
   `uv`, so the reach returns if that row is ever executed. Recommended for the L1:
   `--offline` in the registry cell, or keep the row binding-flagged. Severity: low, latent.
3. **`attrib-probe`'s registry row advertises model-serving trial modes** (`trials` /
   `force-trials` / `stream-trials` POST to the local shims on `127.0.0.1:8791/8793`). The
   declared entry is the offline `freeze-check` and no seat ran a trial mode (wave-wide grep →
   no hit) — keep the declared entry offline so the C1/C2 after-run can never select one.
   Severity: low, latent.
4. **SC1 fetched upstream `solution/solve.sh`** beyond its "names only" item scope — read-only
   GET on an allow-listed host; the body was not committed (lane-tree grep for
   `chess.engine|python-chess|stockfish` → no hit). Owner: SC1/L1.

## Evidence highlights

* probe battery under strace: `socket(AF_NETLINK` ×12, `socket(AF_UNIX` ×12), **0** AF_INET /
  connect / getaddrinfo; sandbox isolation probe → `OSError [Errno 101] Network is unreachable`.
* `python3 plans/round55_c2_entryargv.py --lane . --dry` → `argv_defect=17 wrapper_defect=1`,
  including `ARGV-DEFECT tb2-grader-probe: registry entry cell has no python3 command` and
  `WRAPPER-DEFECT tb2-grader-probe: argv[0]='uv' is not an interpreter` → that PyPI-touching
  row is excluded from the executed set.
* the counter run's own trace → the PyPI traffic above (the one violation).
* loopback-proxy proof of the latent `uv` reach: cold `UV_CACHE_DIR` → `CONNECT pypi.org:443
  HTTP/1.1` ×3 and `Failed to fetch: https://pypi.org/simple/biopython/`; warm cache → no
  contact.
* wave-wide credentialed-request scan (`-X POST|--data|Authorization:|Bearer |GH_TOKEN|
  GITHUB_TOKEN|-u <cred>`) → only the sibling sentinels' own *pattern definitions*; no credential.

## Tooling

No installs, no upgrades, no `pacman` transaction. Tools used were pre-installed:
`python3`, `strace`, `curl`, `sha256sum`, `cmp`, read-only `git`, `grep`, `bwrap`, `uv`
(used only to *measure* the latent `uv` reach).

## Scratch

`/fast/scratch/hyaku/kengaku-r55/SN2NetworkSafety/` — created, used, and **deleted** after the
receipts were copied into the wave dir. One live shared clone
(`git clone --shared`), no full mirror; no mutating git command was run anywhere.
