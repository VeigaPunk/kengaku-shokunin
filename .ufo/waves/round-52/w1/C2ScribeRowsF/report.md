# R52 wave 1 — seat C2ScribeRowsF (scribe): registry rows for 3 instruments

**Claim served:** R52-C2 (operability 8→9), lane `kengaku-shokunin`, base tip `30801b47`.
**Role:** scribe — draft the missing `SKILL.md` *## Gate/probe registry* rows for
`plans/round51_surfaces.py`, `plans/routed_open.py`, `plans/tb2_grader_probe.py`.
**Deliverable:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsF/rows.md`
(scratch original `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsF/rows.md`, removed with the scratch dir).
**Blocked rows: none.** All three rows are filled, every cell non-empty, every claim measured or
line-cited.

## What I did

1. Read `plans/round-52-claims.md` in full (§C2 universe/rule text), `SKILL.md` lines 555-605 (the
   live registry table, header + 46 rows) and `plans/round52_c2_registry.py` (the frozen counter:
   `CMD` entry regex, 8-cell `parse_rows`, `selftest_unbacked` rule).
2. Read each of the three instruments end to end in the lane tree (docstring, argparse block,
   every `return`, what it writes), then **measured** every claim I put in a row rather than
   inferring it: exit codes on the happy path, on each failure path, and on a deliberately broken
   input; the self-test output; the pinned values; the write surface.
3. Cross-checked the executor's AST facts where they existed. `C2ExecRowFacts/facts.json` was
   **absent** (the seat spec's primary source); `C2ExecRowFacts/facts_ast.json` **was** present
   (28 entries, 62 514 bytes) and agrees with my reading on all three scripts — in particular
   `plans/round51_surfaces.py` `network: true` (`socket`, `urllib`), `plans/tb2_grader_probe.py`
   `network: false` with a single `write_text` at the temp-file line, `plans/routed_open.py`
   writes only inside its selftest temp dir. Everything else in the rows is my own measurement,
   as the seat spec allows when the executor artefacts are absent.
4. Validated the rows against the **frozen counter itself**: copied the executor's lane clone into
   my scratch, appended the three rows to the end of the registry table, and ran
   `plans/round52_c2_registry.py`. Receipts below.

All commands ran with `TMPDIR=/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsF/tmp` and cwd
`/fast/scratch/hyaku/kengaku-r52/C2ExecRowRuns/lane` (the executor's clone at tip `1315234`,
byte-identical lane tree) unless stated. Nothing was run against the lane tree itself; no lane
byte was written by this seat.

## Measured numbers (exact commands)

### `plans/round51_surfaces.py`

| command | exit | measured output |
|---|---|---|
| `python3 plans/round51_surfaces.py --lane .` | **0** | `ANCHORS total=20 dup=0 missing=0`; `ROWS section="## Surfaces" rows=10 entries=10 uncovered=0`; `ROWS section="### Core" rows=10 entries=10 uncovered=0`; `PROBES run=20 present=14 absent=6 errors=0`; DRIFT/STALE/UNVERDICTED/NUMBER-DRIFT/ANCHOR-DUP/ANCHOR-MISSING/UNCOVERED/SECTION-MISSING all `0`; `RESOLVE observed_present=14 floor=13 verdict=met`; `PREDICATE R51-C1 pass` |
| `python3 plans/round51_surfaces.py --selftest` | **0** | nine fixture runs S0–S8 (each printing its own `PREDICATE R51-C1 fail` for the reds), then `[selftest] cases=9 failures=0`, `[selftest] ALL PASS` |
| `python3 plans/round51_surfaces.py --lane . --manifest plans/nope.json` | **1** | `FileNotFoundError: … 'plans/nope.json'` traceback, **no** `PREDICATE` line — a could-not-evaluate that exits 1 |
| `python3 plans/round51_surfaces.py --lane . --manifest <scratch>/badkind.json` (`probe.kind="nonsense"`) | **1** | `unknown probe kind 'nonsense'` (`:139`) |
| `python3 plans/round51_surfaces.py --bogus` | **2** | argparse usage |

Manifest facts read from `plans/round51-surfaces.json`: 20 entries, 2 sections
(`## Surfaces`, `### Core`), `resolve_floor 13`, probe kinds `paths 13 · sha256 3 · http 2 · count 1
· port 1`, states `present 14 · absent 6`. The `http`/`port` targets are all `127.0.0.1`
(`:34113`, `:45669`, `:1234`, `:8791`) — which is why the row's write-scope cell says the
instrument opens loopback sockets and nothing else.

### `plans/routed_open.py`

| command | exit | measured output |
|---|---|---|
| `python3 plans/routed_open.py --lane .` | **0** | `ROWS total=75 open=31 blocked=1 closed=41 refused=2`; `routed_open=32 oldest_round=39` |
| `python3 plans/routed_open.py --lane . --list` | **0** | 77 lines: 75 `ROW <id> status=… opened=… source=…` lines + the two summary lines |
| `python3 plans/routed_open.py --selftest` | **0** | 11 named cases + `SELFTEST defect-ledger-guard rc=2 want=2 ok`, then `SELFTEST 12/12` |
| `python3 plans/routed_open.py --lane . --file corpus/defects.jsonl` | **2** | `SETUP refusing defects.jsonl: the defect ledgers are pinned by plans/ledger_tip.py` |
| `python3 plans/routed_open.py --lane . --file corpus/nope.jsonl` | **2** | `SETUP routed-findings file missing: corpus/nope.jsonl` |
| `python3 plans/routed_open.py --lane . --file <scratch>/observe.jsonl --observe` (RX-1 closed with `check:"false"`, RX-2 open with `check:"false"`) | **1** | `OBSERVE RX-1 rc=1 observed=fail self=closed MISMATCH`; `OBSERVE RX-2 rc=1 observed=fail self=open`; `OBSERVE rows=2 mismatched=1` |
| `python3 plans/routed_open.py --lane . --file <scratch>/bad.jsonl` (closed row, no `close`) | **1** | `DEFECT line=1 a closed row must carry closing evidence in close`; `ROWS total=1 invalid=1`; the `routed_open=` line withheld |

### `plans/tb2_grader_probe.py`

| command | exit | measured output |
|---|---|---|
| `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` | **0** | `grader=corpus/evidence/round35/tb2-eval/test_outputs.py sha256=44a05a24… biopython=1.85`; `components_aa=8,259,158,235,182 max_passing_nt=2766 cap_nt=3000`; 18 `case=` lines, every one `match=yes`; `cases=18 observed_pass=5 observed_fail=13 mismatches=0` |
| same command, `--lane <scratch>/tamper` (one `# tamper` line appended to the captured grader) | **2** | `REFUSE grader digest 70ad2697d7aced806361718ffea8d471d6191e1bd89521750421e61d977db513 != pinned 44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582` |
| `python3 plans/tb2_grader_probe.py --dry` | **2** | `error: unrecognized arguments: --dry` (the script accepts `--lane` only) |
| `python3 plans/tb2_grader_probe.py --lane .` (no Biopython on the host python) | **1** | `ModuleNotFoundError: No module named 'Bio'` at `:145` |
| `diff corpus/evidence/round35/tb2-grader-probe.txt <fresh run output>` | **0** | empty diff → **byte-equal**; receipt sha256 `2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8` (3399 bytes), the same digest `plans/pkg-spec-r35.json` pins |

### Frozen counter, with and without my rows

Both runs on the same copied lane (`…/C2ScribeRowsF/lane`, clone of the executor's lane at tip
`1315234`); the only difference is the three rows appended to the end of the registry table.

| run | REGISTERED | rows | MISSING | INCOMPLETE | ENTRY-MISSING | SELFTEST-UNBACKED | exit |
|---|---|---|---|---|---|---|---|
| base (unpatched copy) | 44 | 46 | 28 | 0 | 0 | 1 (`order-check`) | 1 |
| **with my 3 rows** | **47** | **49** | **25** | **0** | **0** | **1** (`order-check`, pre-existing) | 1 |

`grep` over the patched counter output for `round51_surfaces`, `routed_open`,
`tb2_grader_probe` → no hits: none of the three is still MISSING. The `order-check` unbacked row
is the base-tip defect named in the claims file; it is not mine and my rows do not touch it.

## The rows (deliverable, verbatim)

Kind per row: `round51-surfaces` = **gate**, `routed-findings` = **gate**, `tb2-grader-probe` =
**probe**. Names follow the registry's existing kebab-case convention; entry cells carry the exact
`python3 plans/<script>.py` spelling the counter's `CMD` regex matches.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `round51-surfaces` | gate | `python3 plans/round51_surfaces.py --lane .` (lane root; `--manifest PATH` default `plans/round51-surfaces.json`, `--province PATH` default `PROVINCE.md`, `--selftest`) | `0` frozen predicate holds — every problem counter `0` and `RESOLVE … verdict=met`, then `PREDICATE R51-C1 pass` (measured at tip `1315234`: `ANCHORS total=20 dup=0 missing=0`, `PROBES run=20 present=14 absent=6 errors=0`, `RESOLVE observed_present=14 floor=13 verdict=met`, exit 0) · `1` any of DRIFT, STALE, UNVERDICTED, NUMBER-DRIFT, ANCHOR-DUP, ANCHOR-MISSING, UNCOVERED, SECTION-MISSING non-zero or `RESOLVE … verdict=violated`, each defect on a `DETAIL <KEY> …` line, then `PREDICATE R51-C1 fail` (`plans/round51_surfaces.py:219-226`) · `1` also when the manifest cannot be evaluated — an absent manifest path is a `FileNotFoundError` traceback with no `PREDICATE` line (measured, exit 1) and an unknown `probe.kind` prints `unknown probe kind '<kind>'` (`:139`, measured exit 1); a could-not-evaluate never prints `pass` · `2` argparse usage only (`:345-348`, measured `--bogus` → exit 2) | `python3 plans/round51_surfaces.py --selftest` — nine fixtures S0–S8 on one `tempfile.mkdtemp` that honours `TMPDIR` (`:352`): consistent pass, prose drift, stale manifest, unverdicted absent row, number drift, uncovered row, duplicate anchor, floor violated, missing anchor; measured `[selftest] cases=9 failures=0`, `[selftest] ALL PASS`, exit 0 | nothing pinned in code — the manifest is read by path. `plans/round51-surfaces.json` carries 20 entries in 2 sections with `resolve_floor 13`, and the per-surface values the probes compare: sha256 prefix pins `grader.py 90c87c88`, `plans/attrib_probe.py 489f938a`, `~/.local/share/ds-flash-shim/shim.py 42d86d99` (prefix match, `h.startswith(pin)` at `:108`, so a short pin accepts any digest with that prefix); `count` probe `SOURCES rows` over `corpus/SOURCES.md`; `http`/`port` targets `127.0.0.1:34113`, `127.0.0.1:45669`, `127.0.0.1:1234`, `127.0.0.1:8791` | writes no lane byte — reads `PROVINCE.md`, the manifest and every probed target; `--selftest` writes only its one `mkdtemp` dir and `rmtree`s it (`:352-358`); the `http` and `port` probe kinds open `urllib.request.urlopen(url, timeout=3)` or a 1.5 s socket connect to the manifest's loopback URLs (`:116`, `:126`); one `git -C <lane> rev-parse master` for the `REV` line (`:51`); no other network | kengaku round 51 |
| `routed-findings` | gate | `python3 plans/routed_open.py --lane .` (lane root; `--file PATH` default `corpus/routed-findings.jsonl`, `--list`, `--observe`, `--timeout N` default 180 s, `--selftest`) | `0` every row valid, then `ROWS total=<n> open=… blocked=… closed=… refused=…` and `routed_open=<n> oldest_round=<r or ->` (measured at tip `1315234`: `ROWS total=75 open=31 blocked=1 closed=41 refused=2`, `routed_open=32 oldest_round=39`, exit 0) · `1` one `DEFECT line=<n> <reason>` per invalid row then `ROWS total=<n> invalid=<k>`, and the `routed_open=` line is withheld so a round close cannot quote a number off a broken file (`:226-230`; measured `DEFECT line=1 a closed row must carry closing evidence in close`, exit 1) · `1` also on any `--observe` mismatch — `OBSERVE <id> rc=… observed=… self=… MISMATCH` then `OBSERVE rows=<n> mismatched=<k>` (`:154-160`; measured `mismatched=1`, exit 1) or a failed `--selftest` · `2` setup: `--lane` not a directory (`:216`), a file named as a defect ledger — `corpus/defects*.jsonl` refused by name (`:48-50`, `:218-221`; measured `SETUP refusing defects.jsonl: …`, exit 2), the findings file missing (`:224`; measured exit 2), argparse | `python3 plans/routed_open.py --selftest` — 11 row cases plus a defect-ledger guard, all on `tempfile.TemporaryDirectory`: valid-closed, malformed JSON, missing key, duplicate id, closed without evidence, blocked without blocker, bad status, source past EOF, source missing file, bad opened_round, bad id; measured `SELFTEST 12/12`, exit 0 | nothing pinned in code; the population is the named JSONL (default `corpus/routed-findings.jsonl`), measured at tip `1315234`: 75 rows (75 `ROW` lines under `--list`), open 31 · blocked 1 · closed 41 · refused 2, `routed_open=32 oldest_round=39`. Schema literals in code: `STATUSES = open, closed, refused, blocked`; `REQUIRED = id, class, source, opened_round, status`; `ID_RE = [A-Za-z0-9][A-Za-z0-9._-]*`; `SOURCE_RE = <lane-relative path>:<line>` checked against real lane bytes | writes no lane byte — it reads the JSONL and every `source` file it validates. `--observe` runs each row's own `check` string through `subprocess.run(shell=True, cwd=<lane>, timeout=<--timeout>)` (`:148-149`), so any write there is the row's command, not the tool's; `--selftest` writes only inside its temp dir (`:167`, `:187`); no network, no commit, never reads or moves the pinned `corpus/defects*.jsonl` | kengaku round 41 rider (`considerthese/2026-10-26.md` proposal 1) |
| `tb2-grader-probe` | probe | `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` (the captured grader imports Biopython, which `test.sh` pins to 1.85; `--lane` is the only flag) | `0` every frozen prediction matched: `cases=18 observed_pass=5 observed_fail=13 mismatches=0` (measured at tip `1315234` under biopython 1.85, exit 0) · `1` `mismatches>0`, reported on the summary line (`:163-164`) · `2` the captured grader is not at its pin — `REFUSE grader digest <h> != pinned 44a05a24…` (`:142-144`; measured with one appended comment line: `REFUSE grader digest 70ad2697… != pinned 44a05a24…`, exit 2) — and argparse usage (`:136`; measured `--dry` → `unrecognized arguments: --dry`, exit 2) · limit: a missing Biopython is a traceback under exit `1` (`ModuleNotFoundError: No module named 'Bio'` at `:145`, measured exit 1), not `2` | no `--selftest` in the script — only `--lane` is accepted (`:136`), so this row claims none; the probe is the frozen instrument and its verification is external: the committed receipt `corpus/evidence/round35/tb2-grader-probe.txt` (sha256 `2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8`) re-runs byte-equal (measured today: `diff` empty, `BYTE-EQUAL`), and `plans/pkg_gate.py` `--rerun` byte-compares that receipt to the pin in `plans/pkg-spec-r35.json` | grader `corpus/evidence/round35/tb2-eval/test_outputs.py` sha256 `44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582` (`:24`, checked before the grader is imported); TB2 pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; the five literal components read out of the grader source (aa lengths 8, 259, 158, 235, 182 → `max_passing_nt=2766` against the grader's 3000 nt cap); 18 synthetic cases with predictions written from a static reading before the first run | writes only its own `tempfile.TemporaryDirectory` (`:122`) and monkeypatches the grader's `Path` so the hard-coded `/app/gblock.txt` resolves there; imports the captured grader through `importlib`; no network, no model, no container, no task certification, never the live `/app` | kengaku round 35 |

## Findings worth the L1's attention (not defects of my rows)

1. **Two instruments conflate could-not-evaluate with failure.** `round51_surfaces.py` exits `1`
   on an unreadable manifest (traceback) and on an unknown probe kind; `tb2_grader_probe.py` exits
   `1` when Biopython is missing, where its own digest refusal uses `2`. Both are stated plainly in
   the rows rather than papered over — the registry's verdict-map cell is the only place a stranger
   would learn it.
2. **`round51_surfaces.py`'s `sha256` probe compares a prefix** (`h.startswith(pin)`, `:108`), and
   the round-51 manifest pins are 8 hex characters. A truncated pin accepts any digest sharing the
   prefix; the row says so in the pinned-values cell.
3. **`routed_open.py --observe` executes each row's `check` as shell from the lane root.** The row
   attributes any write to the row's command, not the tool, which is the truthful reading
   (`subprocess.run(shell=True, cwd=lane)`, `:148-149`).
4. **`tb2_grader_probe.py` has no self-test at all.** I did not invent one: the row names the
   external verification that exists (the committed receipt re-runs byte-equal, and the package
   gate's `--rerun` byte-compares it), and says in words that the script accepts no `--selftest`.

## Files produced (absolute)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsF/rows.md` — the three rows, integration-ready.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsF/surfaces-run.txt` — `round51_surfaces.py --lane .` full output (exit 0).
- `…/w1/C2ScribeRowsF/surfaces-selftest.txt` — `--selftest` full output (`cases=9 failures=0`, `ALL PASS`).
- `…/w1/C2ScribeRowsF/routed-run.txt`, `routed-list.txt`, `routed-selftest.txt` — `routed_open.py` verdict, 75 `ROW` lines, `SELFTEST 12/12`.
- `…/w1/C2ScribeRowsF/tb2probe-run.txt` — the 18-case probe run, byte-equal to the committed receipt.
- `…/w1/C2ScribeRowsF/counter-base.txt`, `counter-patched.txt` — the frozen counter before/after my rows.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsF.md` — this report.

## Out of scope / not done

- No lane-tree edit, no commit, no `git`/`jj` mutation, no `agent://all` message, no subagent
  dispatch (leaf seat).
- I did not run `--observe` against the real `corpus/routed-findings.jsonl` (75 rows, each a shell
  command from the lane root — that would execute the lane's own checks and could write); the
  mismatch path was measured on a two-row scratch fixture instead, as recorded above.
- No tool was installed or upgraded (nothing needed it); `uv` and `python3` were already present,
  and `biopython==1.85` was supplied ephemerally by `uv run --with`, not installed into any
  environment. No pacman transaction was attempted.
- Scratch dir `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsF/` (including the 584 MB lane copy
  used for the counter check) removed before yield; free space at the start of the seat was
  538 GB on `/fast`.
