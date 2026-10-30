# SN2NetworkSafety — network-use receipt for kengaku round 55 wave 1

Seat: `SN2NetworkSafety` (sentinel). Date: 2026-10-30.
Scope: every fetch performed or planned by round 55 is read-only and in-scope.
Lane repo: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` at `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`
(freeze commit) + uncommitted round-55 working-tree files.
Scratch (deleted on exit): `/fast/scratch/hyaku/kengaku-r55/SN2NetworkSafety/`.

## Method (not just grep)

Static greps are weak evidence for "does this fetch", so every candidate was also
**observed at runtime under `strace -f -e trace=network`** (network syscalls only), and
the network-positive cases were re-proved by *forcing* the network path (a loopback
HTTP proxy that records the `CONNECT` line, plus a cold `UV_CACHE_DIR`).

Host note: `unshare -n` is not permitted on this host (`Operation not permitted`), so
namespace isolation could not be measured that way; `strace` and the loopback proxy
were used instead. `bwrap --unshare-all` was measured directly (it does unshare the
network namespace — see verdict `plans/round55_c3_chess_probe.py`).

---

## Per-file verdicts

| # | File / path | Verdict | Evidence |
|---|---|---|---|
| 1 | `plans/round55_c3_chess_probe.py` | **offline-only** | see §1 |
| 2 | `plans/round55_c2_entryargv.py` | **offline-only** (as a program) | see §2 |
| 3 | `plans/round55_c2_controls.py` | **offline-only** | see §3 |
| 4 | `corpus/knowledge/tb2-chess-best-move-grader.md` | **offline-only** (data; URLs are citations) | see §4 |
| 5 | `corpus/lessons/round-55.md` | **offline-only** (data; URLs are citations) | see §4 |
| 6 | `corpus/evidence/round55/chess-best-move-probe.txt` | **offline-only** (no URL, no fetch) | see §4 |
| 7 | `corpus/SOURCES.md` rows S201/S202 (+ `PROVINCE.md`, `corpus/README.md` deltas) | **offline-only** (data; URLs are citations) | see §4 |
| 8 | E14 planned GETs | **read-only-GET-in-scope** | see §5 |
| 9 | SC1 planned GETs | **read-only-GET-in-scope** | see §6 |
| 10 | R3 planned GETs | **read-only-GET-in-scope** | see §7 |
| 11 | SC3 planned work | **offline-only** (no GET planned) | see §8 |
| 12 | `plans/round52_c2_registry.py` (the C1 counter the round advertises) | **offline-only** | see §9 |
| 13 | `plans/round54_c1_anchor.py` (`stamp`/`upgrade` paths) | **read-only-GET-in-scope for `verify`/`selftest`; `stamp`/`upgrade` are OUT-OF-SCOPE if run** | see §10 |
| 14 | Registry rows the R55-C2 counter *executes* (`attrib-probe`, `catalog-probe`, `round51-surfaces`) | **read-only-GET-in-scope / loopback-only**, with one named caveat | see §11 |
| 15 | `tb2-grader-probe` registry row (`uv run --with biopython==1.85`) | **out-of-scope fetch if executed** (PyPI), but **not executed by the round-55 counter** | see §12 |
| 16 | **`round35-c1-coverage` registry row — executed by the round-55 counter → PyPI** | **VIOLATION: out-of-scope fetch (PyPI) actually performed** | see §12a |
| 17 | S2 prior-art web search | **read-only-GET-in-scope** (public docs/arxiv/openreview/HF datasets) | see §13 |
| 18 | Every other seat's item in the frozen dispatch | **no fetch planned** | see §14 |

---

## §1 `plans/round55_c3_chess_probe.py` — offline-only

Static: no `urllib`, `requests`, `socket`, `http.client`, `httpx`, `aiohttp`, no URL
literal at all. The only subprocess is `/usr/bin/bwrap`; the only network-capable
primitive in the file is `subprocess.run`.

Runtime: full 12-case battery under `strace -f -qq -e trace=network`:

    strace -f -qq -e trace=network -o E2.txt \
      python3 plans/round55_c3_chess_probe.py --lane . --work <scratch> --receipt <scratch>/r.txt
    exit=0 ; grep -cE "AF_INET|connect\(|getaddrinfo" E2.txt  -> 0
    socket families seen: AF_NETLINK (12), AF_UNIX (12)   # namespace setup + local IPC only

The sandbox really is network-isolated — the probe's own `sandbox_argv()` (which uses
`bwrap --unshare-all`) was driven with a socket-connect probe and returned
`NET-BLOCKED OSError [Errno 101] Network is unreachable`.

The grader itself is pure text I/O: the captured `tests/test_outputs.py` imports only
`pathlib` and reads `/app/move.txt`. The probe copies that file in from the **committed
in-repo capture** (`corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py`,
sha256 `a540714e…f286`, checked before every run) — it never fetches it.

**No POST, no authentication, no model-serving endpoint.**

## §2 `plans/round55_c2_entryargv.py` — offline-only

Static: no network import, no URL literal. It imports the unchanged r54 module
`plans/round54_c2_entrytruth.py` (also network-free: stdlib only, `subprocess` used for
`git` and for the row executions) and reuses its `Worker`/`run_row` hermetic path.

Runtime: `python3 plans/round55_c2_entryargv.py --selftest --work <scratch>` under strace
→ exit 0, `grep -cE "AF_INET|connect\(|getaddrinfo"` → **0**.

The counter *executes* other registry rows (§11, §12) — that is the counter's job and is
where the only fetch surfaces in the round live; they are classified there, not here.

## §3 `plans/round55_c2_controls.py` — offline-only

Static: no network import; `subprocess` only for `git init/add/commit` inside its own
throw-away fixture and for the two counters it drives. The `uv` token appears only inside
the **fixture argv it fabricates** (`uv run --no-project --offline python3 -cprint(...)`)
— that argv is never executed by this seat's control flow: `run_case()` calls
`mod.evaluate(root, root, …)` on a fixture whose ledger row argv is the laundering argv,
so the r54 counter *does* execute it — and that is the point of the fixture. `--offline`
makes it non-fetching even so (measured: the `uv` decoy path produces **0** AF_INET
syscalls under strace).

Runtime: `python3 plans/round55_c2_controls.py --selftest` under strace → exit 0, inet
hits **0**.

## §4 Data files (knowledge entry, lesson, SOURCES rows, probe receipt)

`corpus/knowledge/tb2-chess-best-move-grader.md`, `corpus/lessons/round-55.md` and the
`corpus/SOURCES.md` rows S201/S202 carry `https://raw.githubusercontent.com/harbor-framework/…`
as **provenance citations** (source line 1–3 / Gate table), not as fetch instructions;
the entry's `recheck:` line asks a future re-reader to re-fetch those pinned URLs, i.e.
read-only GETs to the same allow-listed host. `corpus/evidence/round55/chess-best-move-probe.txt`
contains only `CASE …` lines and a summary line — no URL.

No new upstream bytes landed: the upstream `solution/solve.sh` (7555 B) fetched by SC1 was
**not** written into the lane tree (grep for `chess.engine|python-chess|stockfish` over
`corpus/`, `plans/`, `.ufo/waves/round-55/` → no hit). `git status` shows the only new
corpus files are the receipt, the knowledge entry and the lesson.

## §5 E14 — read-only-GET-in-scope

Planned and executed GETs:
`raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/{chess-best-move,regex-log}/tests/…`,
`…/chess-best-move/{instruction.md,task.toml}`, and
`https://api.github.com/repos/harbor-framework/terminal-bench-2/commits/2fd12b88…`.

Both hosts are on the allow-list; the API call is a plain unauthenticated `GET` of a
public commit object (`curl -fsS`, no `Authorization`, no token, no `--data`, no `-X POST`).
The landed receipt `.ufo/waves/round-55/w1/E14CaptureIdentity/identity.txt` records three
`MATCH` sha256 pairs and the pin's commit date — no credentialed call anywhere in the seat's
output. **No POST, no auth, no model-serving endpoint.**

## §6 SC1 — read-only-GET-in-scope

Planned: `api.github.com` contents/tree API listings, `raw.githubusercontent.com` file
bytes, `github.com/…/blob/…` HTML. Unauthenticated public GETs on allow-listed hosts,
"<2 MB total" as the seat states. Landed output contains 29 `api.github.com` + 14
`github.com` + 4 `raw.githubusercontent.com` URL mentions and **zero** credential markers
(grep for `Authorization|Bearer |-X ?POST|--data|GH_TOKEN` over the seat dir → no hit).
The one scope note: SC1 also fetched upstream `solution/solve.sh` (read-only GET, allowed
host) although its item said "solution/ dir names only" — it reports the body was fetched
for its size/sha and explicitly "not used as an oracle source"; that keeps R55-C3 kill
rule (b) clean, and the body was not committed to the lane. **In scope; note the mild
over-fetch of a solution artifact (see §15).**

## §7 R3 — read-only-GET-in-scope

Planned and executed: re-open the two pinned `raw.githubusercontent.com` URLs for S201/S202.
Unauthenticated GETs, allow-listed host, `curl -fsSL --max-time 60 -o <scratch>` into its
own scratch (deleted afterwards). No token, no POST. `.ufo/waves/round-55/w1/R3ChessSourcesReopen/reopen.md`
records AGREE/AGREE with byte and quote checks.

## §8 SC3 — offline-only

The item is a local re-implementation of the binding scan over `SKILL.md` +
`plans/round54-entrytruth.json`: no GET planned, none observed in its output.

## §9 `plans/round52_c2_registry.py` — offline-only

The counter R55-C1 depends on. Static: no network import, no URL literal, no `subprocess`
network verb. It parses `SKILL.md` and the lane tree. **No fetch of any kind.**

## §10 `plans/round54_c1_anchor.py` — `verify`/`selftest` offline; `stamp`/`upgrade` out-of-scope

`verify` and `selftest` re-derive everything from committed bytes: the OTS proof is
deserialized with `opentimestamps.core` only (`opentimestamps/core/notary.py` imports
`opentimestamps.core.serialize` and nothing network-capable; the network-capable
`opentimestamps/calendar.py` is **not** imported by the core path), `block-explorer-*.json`
receipts are read from disk, and the calendar URL appears only as the *string* inside a
`PendingAttestation` object that is serialized offline. Measured: `selftest` under strace
→ 0 AF_INET hits (it fails locally with `ModuleNotFoundError: opentimestamps` — see §15).

`stamp` and `upgrade` **do** talk to the network: `stamp` shells out to the `ots` CLI and
`upgrade` polls the calendars (`opentimestamps/calendar.py` issues `urllib.request.Request(…, data=digest)`
— a POST-shaped body to the calendar). **Neither subcommand was invoked by any round-55
seat** (grep over `.ufo/waves/round-55/` for `anchor.py stamp|upgrade|ots stamp|ots upgrade`
→ no hit). The `ots` client is installed at `~/.local/bin/ots` (pre-existing, from
2026-10-30 08:17, before this wave), but nothing in round 55 calls it.

So the anchor is **safe as used** (offline `verify`/`selftest` only) and **must stay that
way**: `stamp`/`upgrade` are out-of-scope for this round's network budget and must not be
run by any seat.

## §11 Registry rows the R55-C2 counter executes — read-only-GET-in-scope / loopback-only (except §12a)

The new counter executes 66 of the 83 registry rows (the L1/L2/L3-clean ones). Three of
those scripts contain network primitives; each was measured:

| Row | Declared entry | What it can reach | Measured |
|---|---|---|---|
| `attrib-probe` | `python3 plans/attrib_probe.py freeze-check --frozen plans/attrib-r23-frozen.md` | `http.client` is imported at module level, but the declared mode never opens a socket | strace: exit 0, **0** AF_INET/connect/getaddrinfo |
| `catalog-probe` | `python3 plans/catalog_probe.py --verify --lane .` | `--verify` re-derives from committed raw bytes; only the no-flag/`--capture` modes reach `huggingface.co/api/models` and `openrouter.ai/api/v1/models` | strace: exit 0, **0** AF_INET/connect/getaddrinfo |
| `round51-surfaces` | `python3 plans/round51_surfaces.py --lane .` | its manifest's `http`/`port` probes target **127.0.0.1 only** (`127.0.0.1:34113`, `:8791`, `:45669`, `:1234`) | strace: 8 loopback `connect()`s to `127.0.0.1`, **no external address** |

**Named caveat (severity: low, pre-existing, not introduced by round 55):** the
`attrib-probe` registry row's *scope* text advertises the trial modes
(`trials` / `force-trials` / `stream-trials`) which **POST to the local model-serving
shims** on `127.0.0.1:8791` (ds-flash-shim) and `127.0.0.1:8793` (glm-flash-shim) via
`HTTPConnection`. Those modes are **not** the declared entry (`freeze-check`) and **were
not** run by any round-55 seat (grep over the wave dir for `attrib_probe.py (trials|…)` →
no hit). The round-55 counter executes the *declared entry*, so it never reaches a
model-serving endpoint. **Recommendation for the L1:** keep the `attrib-probe` registry
row's declared entry on `freeze-check` (or the `--verify`-style offline mode) so the
C1/C2 after-run can never select a trial mode.

## §12 `tb2-grader-probe` registry row — an out-of-scope fetch that round 55 does NOT execute

The registry row's declared entry is
`uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .`.
`uv` resolves `biopython` from **PyPI** — an unauthenticated GET to `pypi.org` that is
outside this round's allow-list. Proven by forcing it:

* cold `UV_CACHE_DIR` + loopback proxy → the proxy log records
  `CONNECT pypi.org:443 HTTP/1.1` (×3 retries) and uv fails with
  `Failed to fetch: https://pypi.org/simple/biopython/`;
* the same command with the host's warm uv cache resolves without any proxy contact.

**The round-55 counter does not execute this row.** Under the new binding legs it is
excluded twice over: L1 reports `ARGV-DEFECT tb2-grader-probe: registry entry cell has no
python3 command` (its cell's first backtick span starts with `uv`, not `python3`) and L2
reports `WRAPPER-DEFECT tb2-grader-probe: argv[0]='uv' is not an interpreter`. Rows
carrying a binding defect are excluded from the execution set, and the row is absent from
the 66 executed rows. So the R55-C2 after-run performs **no PyPI fetch**.

**Named caveat (severity: low, latent):** the *r54* counter, which the round-55 counter
reuses for the L4 execution leg, has no such exclusion — its `entry_mode_ok()` explicitly
*allows* a `uv` argv. If the round-55 after-run is ever executed with the **r54** counter
as the row-execution engine, or if a future round registers the `tb2-grader-probe` row as
clean, the `uv --with biopython` fetch becomes live again (PyPI GET, unauthenticated).
No round-55 seat did this. Recommended remediation (not applied here — out of my write
scope): have the L1 add `--offline` to the `tb2-grader-probe` registry entry cell, or keep
that row flagged by the binding legs so it is never executed.

## §12a **VIOLATION — the round-55 counter run performs an out-of-scope PyPI fetch**

This is the one real network-posture violation found, and it is **executed by the round's own
after-run instrument** (the R55-C2 counter).

### What happens

`python3 plans/round55_c2_entryargv.py --lane . --source . --work <scratch> --jobs 3`
executes 61 registry rows. One of them is **`round35-c1-coverage`**
(`python3 plans/round35_c1_verify.py --lane .`). That counter's `v5` leg runs the TB2
`protein-assembly` probe; when `import Bio` fails it falls back to

    ["uv", "run", "--no-project", "--with", "biopython==1.85", "python3",
     "plans/tb2_grader_probe.py", "--lane", "."]

and `uv` resolves `biopython`/`numpy` from **PyPI** — an outbound HTTPS GET to
`pypi.org/simple/biopython/` and `files.pythonhosted.org`, which are **not** on this round's
allow-list (the allow-list is `raw.githubusercontent.com` / `api.github.com` / docs sites).

### Proof (measured, not inferred)

1. **The counter run itself**, under `strace -f -e trace=network`, shows the traffic.
   Remote (non-loopback) connection targets observed in the whole run:

       8 × 151.101.0.223:443      8 × 151.101.64.223:443    8 × 151.101.128.223:443
       8 × 151.101.192.223:443    3 × 2a04:4e42::223:443    3 × 2a04:4e42:400::223
       2 × 2a04:4e42:200::443

   `151.101.0/64 .223` and `2a04:4e42::/48 .223` are **exactly** `pypi.org` /
   `files.pythonhosted.org` (verified: `getaddrinfo('pypi.org',443)` returns
   `151.101.0.223, 151.101.64.223, 151.101.128.223, 151.101.192.223,
   2a04:4e42::223, 2a04:4e42:200::223, 2a04:4e42:400::223, 2a04:4e42:600::223`).
   The three pids that made the `:443` connections read **1 959 TLS records back**
   (`recvfrom`, payloads beginning `\26\3\3` = TLS handshake / `\17\3\3` = TLS application
   data) — i.e. a real TLS session with PyPI, not a failed connect.

2. **Causal attribution to the one row.** Running each network-capable registry row
   individually through the counter's own hermetic execution path (`m.hermetic_env` +
   `m.Worker` + `m.run_row`), with the uv cache warm, produced **0** external connects for
   `round36-c2`, `round43-c1-mutants`, `round52-c1`, `catalog-probe`, `attrib-probe`,
   `round51-surfaces`, `git-webserver-probe` — and the `round35-c1-coverage` row refreshed the
   uv **simple-index cache** file `~/.cache/uv/simple-v26/pypi/biopython.rkyv`:
   mtime `13:17:05` → `13:28:40` across exactly that one row's run.

3. **Forced reproduction with an explicit CONNECT record.** With a cold
   `UV_CACHE_DIR` and a loopback recording proxy in front of the row:

       CONNECT pypi.org:443 HTTP/1.1     (×4, from the uv client)
       rc=1  V5 DEFECT fresh probe output differs from receipt (exit 2)

   The same row with a cold cache under strace shows **45** pypi/Fastly connect lines.

### Blast radius and attribution

* **Pre-existing, not introduced by round 55.** `plans/round35_c1_verify.py` is unchanged
  since round 35 (`git diff 11d64530 HEAD -- plans/round35_c1_verify.py` is empty), the row
  is in the base-tip ledger (`git show 798f5e9e…:plans/round54-entrytruth.json` →
  `round35-c1-coverage`, `entry_argv = ["python3","plans/round35_c1_verify.py","--lane","."]`),
  and the **unchanged r54 counter also executes it** (83 rows executed; the row is in that
  set). So the reach is inherited by the round-55 counter from the r54 leg it reuses.
* **Partly *reduced* by round 55.** The new binding legs exclude `tb2-grader-probe`
  (a second PyPI-reaching row) from execution: under r54 both PyPI-reaching rows are
  executed; under r55 only `round35-c1-coverage` is.
* **Declared, not hidden.** The registry's own scope cell for `round35-c1-coverage` says:
  *"when `Bio` is not importable it runs the probe under `uv run --no-project --with
  biopython==1.85`, **which reaches the network**"*. The lane documents the reach; it simply
  does not constrain it to the allow-list.
* **What it is NOT:** it is not a POST, not an authenticated request, not a model-serving
  call, and it uploads nothing — it is a read-only GET of public package metadata plus
  wheels. It is out-of-scope by **host**, not by method.

### Smallest remediation (not applied — not my file)

Any one of:
1. add `--offline` to the `uv` argv in `plans/round35_c1_verify.py:168` (the wheels are
   already in the local uv cache — the offline path was measured to fail only because the
   *simple index* refresh is what the flag blocks, so `--offline` needs the index cached, or
   `--no-index --find-links` to a vendored wheel); **or**
2. have the R55-C2 counter's execution leg run with `UV_OFFLINE=1` in `hermetic_env` — a
   one-line change in `plans/round55_c2_entryargv.py` that forecloses *every* uv/PyPI reach
   in the after-run at once (the counter already scrubs `TOKEN|KEY|SECRET|…` from the
   environment, so a network-scrubbing entry belongs there too); **or**
3. exclude `round35-c1-coverage` from the counter's executed set, as the binding legs already
   do for `tb2-grader-probe`.

Option 2 is the smallest change that closes the whole class, not just this instance.

## §13 S2 prior-art — read-only-GET-in-scope

The seat's own report states: "~20 read-only web searches and URL GETs
(raw.githubusercontent.com, huggingface.co resolve endpoint, hub.harborframework.com,
benchmarksolutions.org, arxiv.org). No POST/auth endpoints." Its output contains no
credential marker and no model-serving call. The `huggingface.co` hits are the public
**TB2 dataset** mirror (`/datasets/harborframework/terminal-bench-2.0/resolve/main/…`), not
a model-inference endpoint — read-only GET on a public dataset host, no auth. **In scope.**

## §14 Every other seat's item — no fetch planned

A scan of all 70 dispatch items for `curl|wget|https?://|POST|Authorization|Bearer|token|api_key|gh api|push`
returns URL mentions only in: E14 / SC1 / R3 / S2 (the fetchers, §5–§7, §13), the
`SOURCES.md` row text (E8), the corpus README/province prose (E9), and the two sibling
sentinels' own pattern lists (SN1/SN3 — pattern *definitions*, not calls). The full
host census over all 70 items is:

    2 × raw.githubusercontent.com   1 × api.github.com

No seat item mentions a POST, an authenticated endpoint, a push, or a model-serving
endpoint. The whole-wave output scan for
`-X POST|--data|Authorization:|-u <cred>|GH_TOKEN|GITHUB_TOKEN|--header` returns only the
two sibling sentinels' *pattern definitions* (SN3CorpusHygiene) and one M6 mutant-receipt
line containing the word "token" as an SOURCES *anchor token* column value — no credential.

## §15 Defects / notes found (reported, not fixed — other seats own these files)

1. **`plans/round54_c1_anchor.py` `selftest` is not runnable from a clean clone on this
   host** — `ModuleNotFoundError: No module named 'opentimestamps'` (the library is only
   present inside the `opentimestamps-client` uv tool env at
   `~/.local/share/uv/tools/opentimestamps-client/`). E11SelftestReceipts already reports
   this as a round54-c1 **DEFECT** against C1 leg 2. Network-wise it is *safe* (it fails
   before any network use). Owner: E1/E11/L1 — not mine to fix.
2. **VIOLATION — the R55-C2 after-run fetches PyPI** (§12a): the `round35-c1-coverage`
   registry row, which the counter executes, runs `uv run --with biopython==1.85` and
   therefore GETs `pypi.org` / `files.pythonhosted.org` — hosts outside this round's
   allow-list. Measured end-to-end (TLS session with PyPI, 8 `:443` connects, 1 959 TLS
   records read back) and attributed to that single row by differential measurement
   (every other network-capable row: 0 external connects). Pre-existing and inherited
   from the unchanged r54 counter, and *partly reduced* by round 55 (which excludes the
   second PyPI-reaching row, `tb2-grader-probe`). Owner: E2/E4/L1 — the file is not mine.
3. **The `uv` wrapper reachability** (§12) — latent, not exercised this round.
4. **`attrib-probe`'s registry row advertises model-serving trial modes** (§11) — the
   declared entry is the offline `freeze-check`; keep it that way.
5. **SC1 fetched upstream `solution/solve.sh`** although its item said "names only"
   (§6). Read-only GET on an allow-listed host; body not committed; kill rule (b)
   unaffected. Owner: SC1/L1.
6. **`round52_c2_registry.py`'s advertised universe** — no network surface at all; noted
   only to close out §9.

## §16 Overall verdict

**One network-posture violation, and it is in the round's own after-run instrument.**

* **Everything the wave's seats did is clean.** Every fetch performed by a round-55 seat is
  an unauthenticated, read-only GET landing on `raw.githubusercontent.com`, `api.github.com`,
  or a public docs/arxiv/openreview/HF-dataset host. **No fetch POSTs, authenticates, or
  reaches a model-serving endpoint.**
* **The three scripts the round builds are offline-only** (`plans/round55_c3_chess_probe.py`,
  `plans/round55_c2_entryargv.py` as a program, `plans/round55_c2_controls.py`) — proven at
  runtime under `strace -f -e trace=network`, not just by grep.
* **BUT the R55-C2 counter's *execution* leg performs an out-of-scope PyPI GET** through the
  inherited `round35-c1-coverage` row (§12a). It is a read-only, unauthenticated GET of
  public package metadata — out of scope by **host** (`pypi.org`, `files.pythonhosted.org`
  are not on the round's allow-list), not by method. It is pre-existing (the unchanged r54
  counter reaches PyPI too, via two rows; round 55 reduces it to one), and the lane's own
  registry scope cell already discloses it ("*which reaches the network*").
* **Remediation is one line** in the counter's hermetic environment (`UV_OFFLINE=1`, next to
  the existing secret-scrubbing) — see §12a for the three options.

Everything else in the round is within the stated network posture.

