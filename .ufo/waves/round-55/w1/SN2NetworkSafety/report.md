# SN2NetworkSafety — seat report (kengaku round 55, wave 1)

Seat: `SN2NetworkSafety` (sentinel). Date: 2026-10-30.
Scope: network-use receipt for the round — every fetch read-only and in-scope.
Judged on: operability, calibration.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` at `80afa613` (freeze) + round-55 working tree.
Scratch root (created, used, deleted): `/fast/scratch/hyaku/kengaku-r55/SN2NetworkSafety/`.

## Deliverable

* **`.ufo/waves/round-55/w1/SN2NetworkSafety/network.md`** — the per-file network receipt
  (offline-only / read-only-GET-in-scope verdict for 17 files/paths, evidence, defects).
* **`.ufo/waves/round-55/w1/SN2NetworkSafety/report.md`** — this file's copy (contract path).

## What I ran (commands + exit codes)

Read-only inspection of the lane (no mutation anywhere; no `git add/commit/push/checkout/reset`):

| # | Command | Exit | Result |
|---|---|---|---|
| 1 | `git -C <lane> log --oneline -3 ; git rev-parse HEAD` | 0 | `80afa613` = the freeze commit; base tip `798f5e9e` |
| 2 | `read plans/round-55-claims.md` (full) | — | 3 frozen claims, predicates, kill rules read before any data |
| 3 | `grep -nE "requests\|urllib\|http://\|https://\|socket\|urlopen" plans/round55_c3_chess_probe.py plans/round55_c2_entryargv.py plans/round55_c2_controls.py corpus/knowledge/tb2-chess-best-move-grader.md` | 0 | **no match in any of the three round-55 scripts** (the same grep over the three scripts alone exits **1**); the knowledge entry matched only on its 3 provenance-URL `source:` lines |
| 4 | `git -C <lane> status --porcelain` | 0 | round-55 working tree: `plans/round55_c2_entryargv.py`, `plans/round55_c3_chess_probe.py`, `corpus/knowledge/tb2-chess-best-move-grader.md`, `corpus/lessons/round-55.md`, `corpus/evidence/round55/chess-best-move-probe.txt` untracked |
| 5 | `strace -f -qq -e trace=network -o E2.txt python3 plans/round55_c3_chess_probe.py --lane . --work <scratch>/E2work --receipt <scratch>/E2receipt.txt` | **0** | probe battery passes; `grep -cE "AF_INET\|connect(\|getaddrinfo"` → **0**; socket families: AF_NETLINK 12, AF_UNIX 12 |
| 6 | sandbox isolation probe driven through the probe's own `sandbox_argv()` | 0 | `NET-BLOCKED OSError [Errno 101] Network is unreachable` (bwrap `--unshare-all` really unshares net) |
| 7 | `strace … python3 plans/round55_c2_entryargv.py --selftest --work <scratch>/E3work` | **0** | selftest exit 0, inet hits **0** |
| 8 | `strace … python3 plans/round55_c2_controls.py --selftest` | **0** | `SELFTEST cases=4 failures=0`, inet hits **0** |
| 9 | `strace … python3 plans/round55_c2_controls.py --case uv-decoy-script --against r54` | **0** | laundering route demonstrated (`ROUTE laundering demonstrated`), inet hits **0** (the fixture's `uv` argv carries `--offline`) |
| 10 | `strace … python3 plans/catalog_probe.py --verify --lane .` | 0 | inet hits **0** (`--verify` is the offline mode) |
| 11 | `strace … python3 plans/attrib_probe.py freeze-check --frozen plans/attrib-r23-frozen.md` | 0 | inet hits **0** |
| 12 | `strace … python3 plans/round51_surfaces.py --lane .` | 1 (row is red by design) | 8 inet hits, **all `127.0.0.1`** (`34113`, `8791`, `45669`) — loopback only, no external address |
| 13 | `strace … python3 grader.py` | 0 | inet hits **0** |
| 14 | `python3 plans/round55_c2_entryargv.py --lane . --dry` | 0 | `ROWS registry=78 ledger=78 … argv_defect=17 wrapper_defect=1 abbrev_defect=0` — the binding legs **exclude** `tb2-grader-probe` (L1 + L2) |
| 15 | binding-leg analysis: recompute the 66 rows the r55 counter executes, list their scripts' network primitives | 0 | only `attrib-probe`, `catalog-probe`, `round51-surfaces` — all offline/loopback in their declared entry (§11 of the receipt) |
| 16 | `strace … python3 plans/round54_c1_anchor.py selftest` | **1** | `ModuleNotFoundError: opentimestamps` — fails locally *before* any network use (defect #1, already reported by E11) |
| 17 | `grep` over `.ufo/waves/round-55/` for `anchor.py stamp\|upgrade\|ots stamp\|ots upgrade` | 1 | **no hit** — no seat invoked the network-writing OTS subcommands |
| 18 | `grep` over `.ufo/waves/round-55/` for `attrib_probe.py (trials\|force-trials\|stream-trials\|score)` | 1 | **no hit** — no model-serving shim call this round |
| 19 | loopback-proxy test: `uv run --no-project --with biopython==1.85` with cold `UV_CACHE_DIR` | 2 | proxy log: `CONNECT pypi.org:443 HTTP/1.1` ×3; `Failed to fetch: https://pypi.org/simple/biopython/` — the `tb2-grader-probe` row's declared entry *would* fetch PyPI |
| 20 | same, with the host's warm uv cache | 0 | resolves from cache, **no** proxy contact |
| 21 | same, run through the r54 module's own `Worker`/`run_row` hermetic path (the exact path the counter reuses) | 2 | identical PyPI reach — the latent reach is in the *r54* counter's tolerance of `uv`, not in round-55 code |
| 22 | host-census over all 70 dispatch items (`curl\|wget\|https?://\|POST\|Authorization\|Bearer\|token\|api_key\|gh api\|push`) | 0 | only `raw.githubusercontent.com` (×2) and `api.github.com` (×1) as hosts; the `POST/Authorization/token` hits are the SN1/SN3 sentinels' own *pattern definitions* |
| 23 | whole-wave credentialed-request scan (`-X POST\|--data\|Authorization:\|Bearer \|GH_TOKEN\|GITHUB_TOKEN\|-u <cred>`) | 0 | only SN3's pattern list and one M6 receipt line using "token" as an SOURCES column word — **no credential** |
| 24 | per-seat host census of landed outputs (E14, SC1, R3, S2) | 0 | E14: api.github.com ×1 · SC1: api.github.com ×29, github.com ×14, raw.githubusercontent ×4 · R3: raw ×3 · S2: raw ×5, openreview ×3, arxiv ×3, huggingface ×2, hub.harborframework ×1, benchmarksolutions ×1 — all public read-only |
| 25 | `grep -rlE "chess\.engine\|python-chess\|stockfish" corpus/ plans/ .ufo/waves/round-55/` | 1 | **no upstream solution body landed in the lane tree** (SC1 fetched `solution/solve.sh` but kept it out of the repo) |
| 26 | `grep -nE "urlopen\|requests\|socket\|http\|curl\|wget" .ufo/waves/round-55/w1/*/harness.py`, `.../C2BindingBypass/driver.py` | 1 | no network in sibling wave harnesses |
| 27 | `sha256sum corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` | 0 | `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` = the freeze pin; `test.sh` and `regex-log/test.sh` both `4770437e…c334` (byte-identical) |
| 28 | **full R55-C2 counter run under strace** (`round55_c2_entryargv.py --lane . --source . --work <scratch> --jobs 3`) | **1** (`PREDICATE R55-C2 fail`) | **`RUN executed=61 timeout=0 mismatched=0 evidence_missing=1 laundered=3`** — and the trace shows **8 × `:443` connects to `151.101.x.223` / `2a04:4e42::223` (= `pypi.org` / `files.pythonhosted.org`)** with **1 959 TLS records read back** on those sockets → a real TLS session with PyPI inside the round's own after-run |
| 29 | differential attribution: each network-capable registry row run alone through the counter's own `hermetic_env`+`Worker`+`run_row` path under strace | — | `round36-c2`, `round43-c1-mutants`, `round52-c1`, `catalog-probe`, `attrib-probe`, `round51-surfaces`, `git-webserver-probe` → **0 external connects** each; **`round35-c1-coverage` → refreshes `~/.cache/uv/simple-v26/pypi/biopython.rkyv`** (mtime `13:17:05` → `13:28:40` across that one row's run) |
| 30 | forced reproduction: `round35-c1-coverage` row, cold `UV_CACHE_DIR`, loopback recording proxy | 1 | proxy log: **`CONNECT pypi.org:443 HTTP/1.1` ×4**; `V5 DEFECT fresh probe output differs from receipt (exit 2)`; under strace with a cold cache: **45** pypi/Fastly connect lines |
| 31 | `git diff 11d64530 HEAD -- plans/round35_c1_verify.py` | 0 | empty → the script is unchanged since round 35 |
| 32 | `git show 798f5e9e…:plans/round54-entrytruth.json` | 0 | `round35-c1-coverage` present at base with `entry_argv = ["python3","plans/round35_c1_verify.py","--lane","."]` |
| 33 | r54 vs r55 executed-row sets (recomputed) | — | r54 executes 83 rows incl. **both** PyPI-reaching rows; r55 executes 66 incl. **only** `round35-c1-coverage` → round 55 *reduces* the reach by one row |

## Files I wrote

* `.ufo/waves/round-55/w1/SN2NetworkSafety/network.md` — the network receipt (the item's Target).
* `.ufo/waves/round-55/w1/SN2NetworkSafety/report.md` — this file.
* `.ufo/waves/round-55/w1/SN2NetworkSafety.md` — the contract's Report trailer path.

No other file was created or modified. No lane file was touched, no sibling's file was
"fixed", no git mutation was run.

## Defects found (reported, not fixed — other seats own these files)

1. **VIOLATION — the R55-C2 after-run performs an out-of-scope PyPI GET.**
   The counter executes the `round35-c1-coverage` registry row
   (`python3 plans/round35_c1_verify.py --lane .`), whose V5 leg falls back to
   `uv run --no-project --with biopython==1.85 …` when `import Bio` is unavailable — and
   `uv` then GETs `pypi.org/simple/biopython/` and `files.pythonhosted.org`, hosts **outside
   this round's allow-list** (`raw.githubusercontent.com` / `api.github.com` / docs sites).
   Measured: **8 × `:443` connects to `151.101.x.223` / `2a04:4e42::223`** in the counter's
   own trace, **1 959 TLS records read back** on those sockets (a real TLS session, not a
   failed connect); attributed to that single row by differential measurement (every other
   network-capable row: 0 external connects) and reproduced with an explicit
   `CONNECT pypi.org:443 HTTP/1.1` through a recording proxy.
   *Pre-existing and inherited*: `plans/round35_c1_verify.py` is unchanged since round 35,
   the row is in the base-tip ledger, and the unchanged r54 counter reaches PyPI too — via
   **two** rows. Round 55 *reduces* it to one (the binding legs exclude
   `tb2-grader-probe`). *Declared*: the registry's own scope cell for that row already says
   "*when `Bio` is not importable it runs the probe under `uv run --no-project --with
   biopython==1.85`, which reaches the network*".
   *Not a POST, not authenticated, not a model-serving call* — out of scope by **host**.
   **Smallest remediation** (not applied; the file is E2/E4's and the L1's): add
   `UV_OFFLINE=1` to the counter's hermetic environment next to the existing secret-scrubbing
   (one line, closes the whole uv/PyPI class), or `--offline`/vendored-wheel in
   `plans/round35_c1_verify.py:168`, or exclude that row from the executed set.
   Owner: E2/E4/L1.
2. **`plans/round54_c1_anchor.py selftest` is not runnable from a clean clone on this host**
   — `ModuleNotFoundError: No module named 'opentimestamps'`; the library only exists inside
   the `opentimestamps-client` uv tool env. E11SelftestReceipts already records this as a
   round54-c1 DEFECT against C1 leg 2. Network-safe (fails before any network use).
   Owner: E1/E11/L1.
3. **`tb2-grader-probe`'s declared entry `uv run --no-project --with biopython==1.85` can
   fetch PyPI** (proven: `CONNECT pypi.org:443`). Round 55 does **not** execute it — the
   new L1/L2 binding legs exclude it twice (registry cell has no `python3` span; `uv` is a
   wrapper token) — but the **r54** counter's `entry_mode_ok()` *tolerates* `uv`, so the
   reach is latent if that row is ever executed. Recommended (L1, not applied):
   `--offline` in the registry cell, or keep the row binding-flagged.
   Severity: low, latent.
4. **`attrib-probe`'s registry row advertises model-serving trial modes**
   (`trials`/`force-trials`/`stream-trials` POST to the local shims on 127.0.0.1:8791/8793).
   The declared entry is the offline `freeze-check` and no seat ran a trial mode, so the
   round is clean; the L1 should keep the declared entry on the offline mode so the
   C1/C2 after-run can never select a trial mode.
   Severity: low, latent.
5. **SC1 fetched upstream `solution/solve.sh`** although its item scoped the solution dir to
   "names only" — a read-only GET on an allow-listed host, body not committed, R55-C3 kill
   rule (b) unaffected. Owner: SC1/L1.
6. `round52_c2_registry.py` (the C1 counter): no network surface at all — recorded to close
   the C1 leg out.

## Dead ends / limits

* `unshare -n` is **not permitted** on this host (`Operation not permitted`), so a
  netns-based "runs with no network" proof was impossible; `strace -f -e trace=network`
  plus the loopback proxy were used instead, which is equivalent for syscall-level
  reachability.
* A bare `bwrap --unshare-all … /usr/bin/python3` control failed with
  `execvp /usr/bin/python3: No such file or directory` (the probe's own `sandbox_argv()`
  additionally binds `/bin`, `/sbin`, `/lib`, `/lib64`); the isolation check was therefore
  driven **through the probe's own sandbox builder**, which is the configuration that
  actually ships.
* `python3 plans/round54_c1_anchor.py selftest` could not be completed (missing
  `opentimestamps` module) — the network-posture conclusion for that script was reached by
  reading its import graph (`opentimestamps/core/*` has no network import; only
  `opentimestamps/calendar.py` does, and it is not imported by the core path) plus the
  absence of any `stamp`/`upgrade` invocation anywhere in the wave.
* The `uv`-reach measurement needed the loopback proxy on 127.0.0.1:8899; one attempt hit
  `OSError: Address already in use` (a stale proxy from the previous test) — the second
  attempt reused the still-running instance and succeeded.

## Tooling

No installs, no upgrades, no `pacman` transaction. Everything used was already present:
`python3`, `strace`, `curl`, `sha256sum`, `cmp`, `git` (read-only), `grep`, `bwrap`, `uv`
(used only to *measure* the `tb2-grader-probe` reach, never to install anything new).

## Verdict

**One network-posture violation, and it is in the round's own after-run instrument.**

Everything the wave's *seats* did is clean: every fetch a round-55 seat performed is an
unauthenticated read-only GET landing on `raw.githubusercontent.com`, `api.github.com` or a
public docs/arxiv/openreview/HF-dataset host. **No seat fetch POSTs, authenticates, or
reaches a model-serving endpoint.** The three scripts this round builds are **offline-only**
(runtime-proven under `strace -f -e trace=network`, not just grep-proven).

**But the R55-C2 counter's *execution* leg performs an out-of-scope PyPI GET** through the
inherited `round35-c1-coverage` row: `uv run --with biopython==1.85` → `pypi.org` /
`files.pythonhosted.org`, hosts outside this round's allow-list. It is a read-only,
unauthenticated GET of public package metadata — out of scope by **host**, not by method.
It is pre-existing (the unchanged r54 counter reaches PyPI via two rows; round 55 reduces
that to one) and already disclosed in that row's registry scope cell. One line
(`UV_OFFLINE=1` in the counter's hermetic env) closes it.

Four further named defects/notes are carried in the receipt for the L1.
