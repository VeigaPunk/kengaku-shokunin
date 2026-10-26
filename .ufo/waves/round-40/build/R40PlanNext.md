# R40PlanNext — `### Planned (round 41)` data walk (kengaku r40, wave 1, scout)

Seat: R40PlanNext (scout, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; read at HEAD
`3077adbc7145726519f60f01426a5d03381ad444` through a shared clone in `/fast/scratch/hyaku/kengaku-r40/R40PlanNext/lane`
(HEAD verified equal to the lane's). Nothing in the lane was edited, staged or committed; the frozen files were only read.
Receipts are copied to `.ufo/waves/round-40/build/R40PlanNext/` (harness, case tables, result JSON, run logs); scratch was
removed at the end (§9). The L1 holds the planner seat; this is data plus a draft block (§6).

Axes named before work (Godspeed): **A1** advertised-vs-demonstrated gap of a tool, measured by a mutant harness (kill
rate under the committed standing detector); **A2** reachability of each priced mutant by a *witness* (round-40 lesson:
"reachability asserted, not witnessed", O13); **A3** TB2 class distance from the six graders read; **A4** offline
executability with oracle and nop controls run now; **A5** quote supply; **A6** prior-art clearance; **A7** cost in seats.
A1/A4 ran first (executable), A6 last and only on survivors.

## 0. Headline

1. **Calibration — pick `plans/tip_receipts.py` (plus the CLI half of `plans/sources_adopt.py`).** Cheap mutant harness
   (AST operators, one replacement per mutant, result-difference kill): `tip_receipts.py` 51 killed / 53 survived of 104
   under its standing detector; `sources_adopt.py` 78 / 63 (+4 invalid) of 145, with **`main()` killed 2 of 32**;
   `state_check.py` 138 / 62 on a 200-mutant sample of 1141; `mutant_direction_check.py` 10 / 4 on a 14-mutant sample;
   `round39_c1_audit.py` not measurable by this detector (§2.4). Six `tip_receipts` survivors are **witnessed** in their
   declared directions now (§2.3) and four `sources_adopt` `main()` survivors likewise. Two **docstring-vs-behaviour
   defects** are measured in `tip_receipts.py` on top: it prints no `boundary` line, and 2 of the lane's 5 newest probe
   receipts (`git-leak-probe`, `db-wal-probe`) carry a committed `Run as:` line yet are not compared (`skip reason=
   no-committed-re-run-command`), against the registry sentence "every committed `probe*` receipt with a committed re-run
   command".
2. **Coverage — pick TB2 `constraints-scheduling`** (a grader that embeds its own constraint model; 3 tests; no
   environment beyond three ICS files; no network). A 16-case probe is already built and run this seat:
   `cases=16 observed_pass=3 observed_fail=13 mismatches=2`, every case graded twice (`regrade_differ=0`), second run
   byte-equal. **Prior art exists for its sharpest finding** (TB2.1 PR #245, same defect: tests 2–3 read the first
   `DTSTART` in the file, test 1 reads the attendee VEVENT) — no novelty is claimed for it. Fallbacks, each with an
   executed control: `circuit-fibsqrt` (oracle passes, nop fails, offline, gcc only), `schemelike-metacircular-eval` (oracle
   63/63 in 82 s, nop 0/63).
3. **Routed-findings burn-down (considerthese 2026-10-26 proposal 1) — price: a thin slice as a rider, not a claim.**
   71 routed top-level items across the round-29…39 spot-check §5 sections (heuristic count) against 5 rows in
   `corpus/defects.jsonl`; the round-39 §5 items R1–R5 have measured tip status now (R1 open, R2 open with traceback, R3
   open, R5 closed). Seeding the 11 round-39 rows costs about one executor seat and its counter is a printed
   `routed_open=` line; the full 71-row migration is not cheap (§4).

## 1. Inputs read

`plans/round-40-claims.md` (full); `considerthese/2026-10-26.md` (full); `.ufo/waves/round-39/build/R39PlanNext.md` (full, the
template and the prior pricing); `plans/tip_receipts.py` (full), `plans/sources_adopt.py` (docstring, `main`, selftest
region boundaries), `plans/mutant_direction_check.py` (docstring + body), `plans/round39_c1_audit.py` (docstring),
`plans/state_check.py` (docstring, `find_protocol`, selftest boundaries), `plans/round40_c1_verify.py` (tool table, MUTANTS
heads — not run, wave-1 work in progress), `corpus/lessons/round-39-verifier-spotcheck.md` §5, SKILL.md rows 573 and 586;
TB2 at the pin (`git checkout 2fd12b88aafdd04a52c298e3940bcb189f9766d6`, `git rev-parse HEAD` printed that value; 89 task
directories with `tests/`); `constraints-scheduling`, `circuit-fibsqrt`, `schemelike-metacircular-eval` graders, instructions,
oracles, Dockerfiles in full.

## 2. Candidate A — calibration

### 2.1 Method (executed)

`mut_harness.py` (report dir). Operators: comparison flips (`==`↔`!=`, `<`↔`<=`, `>`↔`>=`, `in`↔`not in`, `is`↔`is not`),
`and`↔`or`, `not x`→`x`, exit-constant `return n`/`SystemExit(n)`→0/1, `if <test>`→`if False` (clause removed), integer
constant in a comparison +1. Self-test fixture regions are never mutated (`sources_adopt` lines 610–972, `state_check`
3583–4648). A mutant is **killed** when `(rc, normalised stdout+stderr)` of any standing-detector command differs from the
unmodified tool's on the same command (scratch paths and timings masked), or it times out; **invalid** = does not compile.
This is a result difference, not an attributed kill (round-40 counter semantics are stricter). Baseline stability and an
identity copy at the mutant path are checked first (`BASE-STABLE`, `IDENTITY-COPY-EQUALS-BASE`). Survivors are **not**
proven non-equivalent; where I classified them it is a hand read and marked so.

An early `state_check` run killed 150 of 150 — an artefact: the tool locates its corpus from `__file__` (`parents[1]`,
`find_protocol`), so any copy outside a lane-shaped tree crashes. The harness now builds a symlinked lane-shaped tree per
mutant (`tree()`); the identity copy then equals the baseline and the sample gives 138 / 62. The artefact is recorded here
so no reader quotes the 150/150.

### 2.2 Results

```
$ python3 mut_harness.py --lane $S/lane --tool <tool> ...        (logs: run_<tool>.txt; JSON: res_<tool>.json)
tool                    standing detector (what the lane commits/uses)              base t   population  killed survived invalid
tip_receipts.py         --list; --only round38/build-pmars; --only round35;           5.4 s   104         51     53       0
                        --only round36/regex-log-probe.txt   (webserver receipt, 55 s, not in the detector)
sources_adopt.py        --selftest (17 cases)                                         0.1 s   145         78     63       4
state_check.py          --selftest + --summary                                        3.0 s   1141 (n=200) 138    62       0
mutant_direction_check  tip run on plans/round38_c1_verify.py (rc 1: known N21)      95.8 s   70 (n=14)   10      4        0
round39_c1_audit.py     --battery r38 (predicate n/a)                                 74.3 s   201 (n=9)     3      6        0
```

Survival rate (valid mutants): tip_receipts 51 %, sources_adopt 45 %, state_check 31 % (sample), mutant_direction_check 29 %
(sample). `state_check.py` is already the best demonstrated of the five: its self-test carries named red mutations P3a–P4e
(docstring/test names at `state_check.py:3601+`), and its survivors are mostly `is None` guards plus four `main()` exit-2
paths (`return 2`→0 at L4666/4694, empty-population L4701) — a small, real, advertised gap ("never a vacuous PASS").

By function (hand-aggregated, `res_*.json`):

- `tip_receipts.py`: `main` 26 of 59 survive, `usage_argv` 8 of 9, `provenance` 6 of 12, `lane_root` 5 of 9, `first_diff`
  4 of 4, `tamper_one_byte` 2 of 4, `die` 1 of 1.
- `sources_adopt.py`: **`main` 30 of 32 survive**, `check` 8 of 18, `row_defects` 5 of 9, `build_block` 4 of 15, `quote_check`
  3 of 19, `print_report`/`print_quote_report` 6 of 6. The selftest exercises the library functions and quote checks; the
  CLI wiring that maps to the eight advertised exit codes (SKILL.md:573: `2 3 4 5 6 7 8 9`) is almost undemonstrated.

### 2.3 Witnesses (Q29: reachability shown, not asserted)

`tipwit/witness.py` builds fake lanes (git repos carrying the exact RECEIPTS rel paths and a stub probe script), runs the
unmodified tool and each mutant (`tipwit/out.txt`):

```
W1 T01 die SystemExit(2)->0        lane not a toplevel      ref rc=2 SETUP ...        mut rc=0       DIFFER   (error)
W2 L210 no-evidence guard off      lane without corpus/evidence ref rc=2 SETUP ...    mut rc=0 receipts=0  DIFFER   (error)
W3 L280 probe-exit guard off       probe prints blob, exits 3   ref rc=1 differ=1     mut rc=0 byte_equal=1 DIFFER  (rc-silence)
W5 L285 masked-equal `==`->`!=`    temp-paths receipt equal after masking  ref rc=0 skipped=1  mut rc=1 differ=1  DIFFER (rc-mirror)
W6 L302 unknown-tamper guard off   --tamper corpus/evidence/nope.txt  ref rc=2 SETUP   mut rc=1 KeyError  DIFFER (error)
W7 L347 `and`->`or`                empty receipt, control unavailable  ref rc=1       mut rc=0       DIFFER   (rc-silence)
```

`srcwit/witness.py` (`srcwit/out.txt`): four `main()` mutants differ from the reference — L1022 quote/registry exclusivity
(rc 2 → 4), L1041 usage guard (rc 2 → 1 with `AttributeError`), L1052 ISO-date guard (rc 2 → 5), and L1048 (rc 2 → 2, message
only: the next guard catches it, so L1048 is rc-equivalent, an O07-style redundant guard — it must NOT enter a frozen list
as an rc direction). L1068 (`if missing:` in `main`) is **not** witnessed: my fixture hit the earlier `check()` missing-id
refusal (rc 5 both); it needs a package row that is not opened this round. Mutants proposed below carry their witness
status; unwitnessed ones need wave-1 witnesses before freeze.

One counter-example class found while triaging: `tip_receipts.py:317` (`res["kind"] == "temp-paths"` flipped) survives
because for a byte receipt the masked comparison is equivalent to the raw one — **near-equivalent, do not freeze**.

### 2.4 Not priced / limits

- `round39_c1_audit.py`: the detector I could run (`--battery r38`) prints `PREDICATE C1 n/a`, so its predicate/exit-code
  lines (L423–426) are unreachable by it — 6 of 9 survive for that reason, not as an estimate of the real gap. Its A1/A3/A4/A5
  repairs are carried by `round40_c1_verify.py` (claims file: "carries the round-39 closure R4 soundness repairs"), so the
  surface is superseded; its only committed hostile evidence lives in wave directories (`.ufo/waves/round-39/falsify/
  F39CritAudit/`), not `plans/`.
- `mutant_direction_check.py`: 14-mutant sample only (95.8 s per detector run under load average ~50–95); the 4 survivors are
  `or`→`and` in setup guards and the exit-3 mapping (`return 1 if mis else (3 if ...)`, L176).
- The tip_receipts detector omits the 55 s webserver receipt and the `regex-log-probe-first-run.txt` receipt (my `--only`
  substring `round36/regex-log-probe.txt` does not match the `-first-run` name), so the temp-paths branch is exercised only
  by the unmatched fixtures of W5; the committed gate runs them. Kill counts for tip_receipts could rise by a few mutants
  with the full run; survivors below that are witnessed against the unmodified tool, not against my detector.
- Hand classification of tip_receipts survivors: of 53, about 20 map to a docstring sentence on exit codes (L24–27), skip
  reasons (L14–15), control (L20–22) or temp-paths masking (L16–18); the rest are cosmetic (`provenance`, `first_diff` text)
  or defensive guards. [INFERENCE — not proven.]
- Load average was 45–96 on this host during the runs; wall times are inflated; no kill depends on timing except the
  timeouts counted separately (none occurred).

### 2.5 Advertised-vs-demonstrated findings for `tip_receipts.py` that need no mutant

| finding | command | observed |
|---|---|---|
| registry sentence vs population | `python3 plans/tip_receipts.py --lane . --list` | 5 mapped receipts; 21 `skip reason=no-committed-re-run-command`, of which `corpus/evidence/round39/git-leak-probe.txt` and `.../round40/db-wal-probe.txt` have a committed `Run as:` line (`plans/git_leak_probe.py:4`, `plans/db_wal_probe.py:4`: `python3 plans/<x>.py --lane .`) |
| docstring token | `grep -n boundary plans/tip_receipts.py` | one hit, in the docstring (L14: "printed on one `boundary` line"); the tool prints one `skip reason=` line per receipt |
| silent empty selection | `python3 plans/tip_receipts.py --lane . --list --only nomatch` | `tip <sha>`, rc 0 (the known F5 residual; no control, nothing compared) |
| work dir that is a file | `... --only round35 --work <a file>` | `FileExistsError` traceback, rc 1 (not an advertised exit-2 shape; minor) |

SKILL.md:586 verdict map: "`0` every committed `probe*` receipt with a committed re-run command is byte-equal at the tip".
Fix-then-freeze (Q30) applies: extending RECEIPTS changes the tool's bytes, so the two rows are either added **before** a
freeze (then the mutants' `old` strings target landed bytes) or declared as limits.

**Update at report close (read-only `git diff`, not mine):** the lane working tree now carries an uncommitted edit of
`plans/tip_receipts.py` by another wave-1 seat (`git diff --stat`: 52 lines). Its docstring replaces the `boundary` sentence
with "Every other file is printed on its own `skip reason=no-committed-re-run-command` line" and adds a *derived* mapping
(receipt stem == script stem once non-alphanumerics are dropped; `--list` prints `origin=derived`), which would map the
`git-leak-probe` and `db-wal-probe` receipts without a table edit. So both §2.5 defects are being fixed this round; every
line number, survivor and mutant in §2 is for the committed bytes at `3077adbc`, and a round-41 list must be re-derived
on the landed bytes (the derived-mapping clause adds new advertised behaviour: exact-one-match rule, `origin=derived`
text, strictness `kind=byte`; mutants for it are unpriced). The witnesses W1–W7 target clauses that the diff does not touch
by description, but were not re-run on the edited bytes.

### 2.6 Proposed frozen mutant list (to be witnessed and frozen by the L1; none is a score claim)

| id | tool | `old -> new` (line at 3077adb) | advertised sentence | direction | witness |
|---|---|---|---|---|---|
| T01 | tip_receipts | L76 `raise SystemExit(2)` → `SystemExit(0)` | docstring L24–27 "2 usage/setup" | error | W1 |
| T02 | tip_receipts | L210 `if not (lane / EVIDENCE).is_dir():` → `if False:` | L26 "no `corpus/evidence/`" | error | W2 |
| T03 | tip_receipts | L280 `if run["exit"] != 0:` → `if False:` | L25 "a probe that did not complete (exit != 0)" | rc-silence | W3 |
| T04 | tip_receipts | L285 `mask(fresh) == mask(blob)` → `!=` | L16–18 temp-paths masked on both sides | rc-mirror | W5 |
| T05 | tip_receipts | L302 `if unknown:` → `if False:` | L27 "unknown `--tamper` id" | error | W6 |
| T06 | tip_receipts | L347 `d == 0 and control_ok` → `d == 0 or control_ok` | L22 "A control that answers `equal` exits 1" (reachable only through `unavailable`) | rc-silence | W7 |
| T07 | tip_receipts | L92 `if not top or ... != lane.resolve():` → `if False:` | L26 "lane not a git work-tree root" | error | needs a fixture (W1 reaches the whole `die`, not this clause) |
| T08 | tip_receipts | L257 `elif shutil.which(argv[0]) is None:` → `elif False:` | L15 "whose dependency is absent" | rc-mirror | unwitnessed (needs a `uv run` line with `uv` off PATH — the counter inherits PATH; may be unreachable) |
| S01 | sources_adopt | L1022 `if args.registry or args.package:` → `if False:` | SKILL.md:573 exit `2` (usage), comment L1019–1020 | error | srcwit L1022 |
| S02 | sources_adopt | L1041 `if not args.registry or not args.package:` → `if False:` | `2` usage | error | srcwit L1041 |
| S03 | sources_adopt | L1052 `if not ISO_DATE_RE.match(args.access_date):` → `if False:` | `2` usage | error | srcwit L1052 |
| S04 | sources_adopt | L1068 `if missing:` → `if False:` | `5` requested id absent / not opened | rc-silence | unwitnessed |
| S05… | sources_adopt | `EXIT_*` mapping in `check()`/`quote_check()` (exits 3, 4, 6, 7, 8, 9) | SKILL.md:573 | error / rc-silence | one witness each needed |

Non-frozen notes: L1048 is rc-equivalent (redundant guard); T08 and S04 are candidates for the O13 treatment — withdrawn
before freeze if their witness shows equivalence.

Mutation-harness cost to freeze: counter = a copy of `round40_c1_verify.py` (576 lines) with two new tool kinds (`receipts`,
`sources`) in the `TOOLS` table (L92–94) and result parsers (L336–342 show the anchor/ledger/order classifiers); fixtures
are throwaway git repos plus fake probe scripts (tip_receipts, ~10 lines each) or package/registry text files
(sources_adopt, 0.1 s runs). Estimated seats: 1 counter copy, 2 battery writers, 1 witness/critic — [INFERENCE from round
40's 3-tool shape].

## 3. Candidate B — coverage / novelty: the next TB2 grader

### 3.1 Census of the 83 graders not yet read (`tb2_screen.py` → `tb2_screen.json`; pin `2fd12b88`)

| measure | result | command |
|---|---|---|
| tasks with `tests/test_outputs.py` | 89 of 89; 6 covered by the lane (protein-assembly, regex-log, configure-git-webserver, build-pmars, git-leak-recovery, db-wal-recovery) | `python3 tb2_screen.py tb2 cen/screen.json` → `tasks 89` |
| uncovered, module parses, no fixtures/marks, no missing host import | **50 of 83** (33 need absent imports — `pytest` 10, `pandas` 4, `torch` 4, `cv2` 3, `selenium` 2, `transformers` 2, …; 7 use fixtures/marks) | same |
| of those, ≥ 30 quotable test lines and ≥ 5 quotable instruction lines (3–25 words) | 18 | same |
| of those, oracle `solve.sh` with no network-ish token | **7**: circuit-fibsqrt, constraints-scheduling, git-multibranch (service class, already covered), large-scale-text-editing (needs `vim`; host has `nvim` only), llm-inference-batching-scheduler (package-relative import, 111 KB of environment), openssl-selfsigned-cert, schemelike-metacircular-eval | same |

(`allow_net` in the JSON is a regex artefact — true for every task — and is ignored.) Host facts: `bwrap`, `gcc`, `openssl`,
`python3`, `nvim` present; **no `Rscript`** (adaptive-rejection-sampler and mcmc/rstan tasks are not offline here); `node` exists
only under an `fnm` path, not inside a `/usr`-bound sandbox (extract-elf needs an extra bind).

### 3.2 `constraints-scheduling` — pilot executed (the recommended grader)

Class: the graded artefact is a one-event ICS file; the verdict is computed by a model **embedded in the grader**
(`_hard_ok`, `_overlap`, a minute-granularity scan) over inputs pinned by sha256. Pin: `tests/test_outputs.py` 209 lines, 3
tests; `instruction.md` 16 quotable lines; grader 118 quotable lines; environment = three ICS files (4132 B), Ubuntu base
image. Oracle `solve.sh` = python3 only, no network. Brute force with the grader's own `_hard_ok`: first valid slot is
2024-01-17 11:00 (checked by script; matches the hand reading of the three calendars).

Probe (`cs/cases.py` with predictions written first; `cs/dry-table.txt` sha256 prefix `8910143d9c5f742e`; `cs/run.py` in
bwrap `--unshare-net --unshare-pid`, `/app` = the three ICS + case file, `/tests` and `/solution` bound, grader module
imported and its three test functions called twice per case):

```
$ python3 cs/run.py > cs/run1.txt ; python3 cs/run.py > cs/run2.txt ; cmp cs/run1.txt cs/run2.txt     -> BYTE-EQUAL
cases=16 observed_pass=3 observed_fail=13 mismatches=2 regrade_differ=0
```

| case | fail set (S structure, C constraints, E earliest) | note |
|---|---|---|
| nop | C,E,S | no file |
| oracle-solve.sh | – | task oracle, 3/3 |
| literal-correct-slot | – | hand-typed ICS for Wed 11:00, never reads the calendars |
| decoy-first-vevent | – | first VEVENT = decoy at the right slot, attendee VEVENT at Fri 15:00 → 3/3 pass (tests 2–3 read the first `DTSTART` of the file, test 1 reads the attendee VEVENT) |
| duration-90min | S | `DTEND` is read only by test 1 |
| bob-start-0900-wed | C | `earliest` passes because `_hard_ok` rejects 09:00 too |
| later-valid-thu-1100 | E | valid but not earliest |
| missing-carol / title-wrong | S | |
| input-appended | S | calendar byte change |
| input-event-deleted-wed-1000 | S | only the sha256 integrity check sees the deleted event |
| tzid-form / weekend-sat-20 / conflict-mon-1230 | C,E,S / C,E,S / C,E | |
| **mismatches (2)** | later-valid-wed-1105: predicted `E`, observed `C,E`; seconds-30: predicted `E`, observed `C,E` | both are **my errors**: both slots run into Carol's Wed 12:00–13:00 event, which I had not tied to the case. They are reported, not edited out. |

The grader is idempotent on every case (two gradings equal). Limits: host python 3.14.8 vs the image's python 3.13 via `uvx`
(test.sh needs network for `apt-get`/`uv`, so the runner itself cannot run offline; the lane's probes call the test functions,
as in rounds 36–40); the image is not pulled.

**Prior art (A6):** `harbor-framework/terminal-bench-2-1` PR #245 "Bind constraints-scheduling checks to the requested event"
(closed 2026-10-08; body quoted: "the constraint and earliest-slot tests parse the first DTSTART in the entire output
calendar") — the decoy finding is published; it supplies a B-tier source for the entry and rules out a novelty claim. The
PR body also says the 55 adversarial fixtures never measured prevalence. A `gh` issue search on `terminal-bench-2` returned
`total_count=0` for `constraints-scheduling`.

### 3.3 Fallbacks priced with a control run now

- **`circuit-fibsqrt`** (class: an agent-authored data artefact executed by a grader-owned compiled simulator on a fixed
  28-input table; 3 tests; 76 / 12 quotable lines). Executed in bwrap (gcc present): `nop` → `test_sqrt_fib FAIL` (28/28
  rows wrong), `oracle` (python `solve.sh` that writes `gates.txt`, 33.0 s) → `test_sqrt_fib PASS`, 3/3 tests green. No case
  table written. `gh` search: 0 on `terminal-bench-2`; `terminal-bench-2-1` returned 4 results that include leaderboard
  submissions — titles not enumerated (rate limit hit, §7). Open question I did not close: the grader compiles `-o sim`
  into the current directory but executes `/app/sim`; whether they coincide depends on the runner's working directory.
- **`schemelike-metacircular-eval`** (class: differential grader — the agent's evaluator is run through the task's reference
  interpreter and compared with the direct run on 32 visible + 31 hidden `shadow_test` programs). Oracle 63/63 in 82.3 s
  offline, `nop` 0/63; a `terminal-bench-2-1` open issue #135 "metacirc tests gamed by special-casing eval.scm path" and PR
  #235 "Reject false passes in Scheme evaluator grading" already cover its gaming surface, so little novelty remains.
- **`openssl-selfsigned-cert`**: unchanged from round 39 (`R39PlanNext.md` §3.3: 26 cases, 25/26 predicted, oracle 5/6 on host
  OpenSSL 3.6.5 because of the `CN = ` format) — still the richer probe, still carrying the version limit.
- **`extract-elf`**: 234 quotable test lines but 4 instruction lines and a `node` binding problem; refused for quote supply
  and offline reach. `fix-git`, `cancel-async-tasks` remain refused (0 quotable instruction lines, round 39).

### 3.4 Cross-check for the C2 landing (not asked, found)

`harbor-framework/terminal-bench-2-1` open issue #3 "fix(db-wal-recovery): Move encrypted WAL out of SQLite live sidecar path"
is published prior art for the destructive-read trap the round-40 entry reports as a probed instance; the claims file calls the
trap "published (the oracle's own … comment)". If the entry's wording ("limits": published trap) predates this link, it can cite
the issue. `gh api search/issues` result, not opened beyond its title.

## 4. Candidate C — considerthese 2026-10-26 proposal 1 (routed-findings burn-down), priced

Population (heuristic count of top-level bullets/numbered/table rows under each spot-check's "routed" §5 heading,
`corpus/lessons/round-N-verifier-spotcheck.md`): r29 8, r30 11, r31 7, r32 4, r33 2, r34 6, r35 6, r36 7, r37 8, r38 7, r39 5 =
**71**. Ledger today: `corpus/defects.jsonl` 5 rows (`wc -l`), all `closed`; `ledger_tip.py` audits 9 rows. `considerthese` cites
`F39CritR38Dispositions` finding 16 of 79 round-38 dispositions verifiable at the tip.

Round-39 §5 status at the lane tip, by command (the only batch I could re-derive cheaply):

| item | command | observed at 3077adb |
|---|---|---|
| R1 registry rows for `order_check.py`, `round39_c1_audit.py` | `grep -c "order_check.py" SKILL.md; grep -c round39_c1_audit SKILL.md` | 0 and 0 (QUALITY.md:533–543 does name `order_check.py`) → open |
| R2 `git_leak_probe.py --work <absent dir>` | `python3 plans/git_leak_probe.py --lane . --stage-check --work $S/absent/x` | `FileNotFoundError` traceback → open |
| R3 order class in `corpus/defects.jsonl` | `grep -c order corpus/defects.jsonl` | 0 → open (counter-blocked: `ledger_tip.py` is pinned by C1) |
| R4 `tip_receipts.py` skipping the new receipt | §2.5 | open, now 2 receipts |
| R4 direction check cannot load the round-39 list | `python3 plans/mutant_direction_check.py --lane . --counter plans/round39_c1_verify.py` | `SETUP counter ... is not a round-38-list counter` → open |
| R4 C1 counter soundness A1/A3/A4/A5 | claims file | addressed by `round40_c1_verify.py` (pending its own run) |
| R5 leftover seat dirs | `ls -d /fast/scratch/hyaku/kengaku-r39*` | absent → closed |

(Wave-1 seats may be closing R1–R3 in this round's integration; the table is tip-at-3077adb, not tip-after.)

Price: rows are cheap where a command exists (above); the full 71-row migration is not (each row needs the source line and
a closing commit; the 16/79 verifiability figure says ~20 % of dispositions have a mechanical check). The freeze-refusal
rule ("refuse a new coverage claim while the oldest open finding is more than two rounds old") would first bite at round 42
for round-39 residuals still open, so adopting it at round 41 costs nothing now and removes the
"routed to round N+1" dead end. It belongs to operability/discernment, not calibration; as a rider it adds a printed
`routed_open=<n> oldest_round=<r>` line, not a frozen mutant claim.

## 5. Axis recommendation (data, the planner decides)

Carried axes (claims file, SCORECARD round 39): calibration 8, coverage 7 (L0-capped), novelty 7, depth 9, operability 8,
freshness 8, adjacency 8. Candidates by gap measured:

| candidate | gap measured now | witnessed | prior art | cost |
|---|---|---|---|---|
| C1 tip_receipts + sources_adopt CLI | 53/104 and 63/141 survivors; 2 defects with no mutant | 6 + 3 (+1 rc-equivalent) | none needed | 1 counter copy + batteries; fix-then-freeze for RECEIPTS |
| C2 constraints-scheduling | pilot 16 cases, 2 honest mismatches, byte-equal, regrade 0 diff | n/a | **decoy finding published (TB2.1 #245)** | low: cases.py/run.py exist; spec/gate/counter per round 40 |
| C2′ circuit-fibsqrt | oracle/nop only | n/a | 0 in tb2; tb2-1 4 hits unread | medium: no case table yet |
| rider: burn-down | R1–R5 status by command | n/a | none | ~1 seat for 11 rows |

Novelty (7, tied lowest): none of the three yields a *novel* finding — the one new grader-level finding (decoy-first-VEVENT)
is published. The honest novelty options on record are the stability column (taken in round 40) and the two
registry-vs-behaviour mismatches in §2.5, which are lane-internal. [INFERENCE: a novelty claim would need an unpublished
grader finding; none was found this seat.]

## 6. DRAFT — `### Planned (round 41)` (paste-ready for `SCORECARD.md`)

```markdown
### Planned (round 41)

- **Calibration (8; lowest-tied non-capped axis — L1 to confirm against the round-40 axis table):** mutation-test the next
  undemonstrated tripwire surface, `plans/tip_receipts.py` (round 38, `considerthese/2026-10-25.md` proposal 2(c); never
  mutation-priced) and the CLI half of `plans/sources_adopt.py` (its `--selftest` exercises the library functions, not
  `main()`). Measured at `3077adbc` with a cheap AST mutant harness and each tool's standing detector
  (`.ufo/waves/round-40/build/R40PlanNext.md` §2): `tip_receipts.py` 51 killed / 53 survived of 104 (detector: `--list` plus
  three `--only` runs), `sources_adopt.py` 78 / 63 of 145 with `main()` killed 2 of 32, `state_check.py` 31 % survival on a
  200-mutant sample (not chosen: it already carries named red mutations). Six `tip_receipts` survivors (exit-2 setup
  paths, the probe-exit-≠0 clause, temp-paths masking, the unknown-`--tamper` guard, the control-unavailable exit) and
  three `sources_adopt` `main()` guards are witnessed in their declared directions by `tipwit/` and `srcwit/`; one candidate
  (`sources_adopt` L1048) is rc-equivalent and stays out of the list. Two further advertised-vs-behaviour defects have no mutant:
  `tip_receipts.py` prints no `boundary` line (docstring L14) and does not compare `corpus/evidence/round39/git-leak-probe.txt`
  or `corpus/evidence/round40/db-wal-probe.txt` although both probe scripts carry a `Run as:` line (SKILL.md:586 says
  "every committed `probe*` receipt with a committed re-run command"); a round-40 working-tree edit already adds a derived
  receipt-to-script mapping and fixes the docstring (L1 to confirm it lands), and the list is re-derived on the landed
  bytes before the freeze (Q30), including mutants for the derived-mapping clause. Frozen list (to freeze after wave-1
  witnesses): ~8 `tip_receipts` + ~8 `sources_adopt` mutants, each with its docstring/SKILL sentence and file:line, direction
  per Q29 (`error`, `rc-silence`, `rc-mirror`), pre-freeze witness committed. Counter `plans/round41_c1_verify.py` = the
  round-40 counter with two new tool kinds; predicate `MUTANTS total=<n> killed=<n> survived=0 invalid=0 null_detected=0`,
  `PREDICATE C1 pass`. Before (do-nothing control, measured at freeze): no `plans/battery41` → `killed=0`. Kill rule as
  round 40: any survivor, invalid mutant or null detection → not admitted; a mutant later shown equivalent is reported
  as a limit, never relabelled.
- **Coverage (7, capped by the open L0 question `kengaku | round-33`; judged on its counter, no score move claimed):** a
  seventh Terminal-Bench 2.0 grader, `constraints-scheduling` @ `2fd12b88` — the first whose decisive check is a constraint
  model embedded in the grader over sha256-pinned inputs (rows S121 `tests/test_outputs.py`, S122 `instruction.md`, ids
  re-derived at freeze). Probe pilot already run offline (`--unshare-net`): `cases=16 observed_pass=3 observed_fail=13
  mismatches=2` (both mismatches are the planner's: the slots hit Carol's Wed 12:00 event), every case graded twice
  (`regrade_differ=0`), byte-equal second run; task oracle 3/3, nop 0/3; a hand-typed ICS that never reads the calendars
  passes 3/3, `DTEND` is read by one test of three, a deleted input event is seen only by the sha256 integrity check.
  Prior art, declared: the first-`DTSTART` binding defect is published (`terminal-bench-2-1` PR #245, closed 2026-10-08), so
  no novelty is claimed for it; the entry cites it. The 16-case probe is rebuilt under the round-40 spec/gate/counter pattern
  (cases and `violates=` tags frozen before the first recorded run, receipt checked by `plans/order_check.py`, counter
  = round 40's V1–V7). Fallback, executed controls only: `circuit-fibsqrt` (oracle passes, nop fails, offline, 33 s) and
  `schemelike-metacircular-eval` (oracle 63/63 in 82 s, nop 0/63; gaming surface covered by TB2.1 #135/#235).
  Refused: `adaptive-rejection-sampler` and the R/stan tasks (no `Rscript` on host), `extract-elf` (4 quotable instruction
  lines; `node` outside the sandbox bind), `fix-git`, `cancel-async-tasks`.
- **Rider (operability, no claim): routed-findings burn-down** (`considerthese/2026-10-26.md` proposal 1), thin slice: seed
  `corpus/defects.jsonl` (or a sibling append-only file) with the round-39 §5 items R1–R5 and the six carried residuals, each
  with a closing commit or `open`, and print `routed_open=<n> oldest_round=<r>` in the round close. Measured at `3077adbc`:
  R1, R2, R3 open, R5 closed; 71 routed items across the round-29…39 spot-checks against 5 ledger rows. The freeze refuses a
  new coverage claim only when the oldest open row is more than two rounds old (first applicable at round 42).
```

## 7. Limits

- The mutant harness measures result differences under each tool's standing detector, not attributed kills; survivors are
  not proven non-equivalent (hand classification marked). Samples: `state_check` 200 of 1141, `mutant_direction_check` 14 of
  70, `round39_c1_audit` 9 of 201 (detector cannot reach its predicate) — rates for those three are samples.
- `tip_receipts` detector omitted the slow webserver receipt and the `-first-run` receipt (see §2.4).
- `gh api search/issues` hit the rate limit during the final per-task sweep: counts for `circuit-fibsqrt` (4), `extract-elf`
  (15), `large-scale-text-editing` (9), `db-wal-recovery` (15) on `terminal-bench-2-1` are `total_count` values that include
  leaderboard-submission noise and were not opened; only #245, #135, #235 and #3 were read (title + `#245` body). Absence
  claims rest on search-index `total_count=0` for `terminal-bench-2`, not proof.
- `constraints-scheduling` was priced on host python 3.14.8 and without the runner (`test.sh` needs network); `circuit-fibsqrt` and
  `schemelike` only have nop/oracle controls; none of the three has a frozen dry table beyond the 16-case `cs/dry-table.txt`.
- Host load average 45–96 throughout; no timings are comparable to quiet-host numbers.
- Wave-1 seats are editing/closing items (R1–R3, battery40); §4's table is tip-at-3077adb.
- The working tree changed under me (`plans/tip_receipts.py`, SKILL.md, README, PROVINCE, SOURCES modified by other seats); my
  clone was taken at HEAD and is not affected, my numbers are not re-measured on the edited bytes.

## 8. Evidence ledger

| claim | command | output |
|---|---|---|
| lane HEAD | `git -C $S/lane rev-parse HEAD` | `3077adbc7145726519f60f01426a5d03381ad444` (= the lane's) |
| tip_receipts mutants | `python3 mut_harness.py --lane $S/lane --tool tip_receipts --jobs 5` | `population=104 ... {"survived": 53, "killed": 51}` (`run_tip_receipts.txt`) |
| sources_adopt mutants | same, `--tool sources_adopt` | `population=145 ... {"killed": 78, "survived": 63, "invalid": 4}` |
| state_check mutants | same, `--tool state_check --sample 200`, `IDENTITY-COPY-EQUALS-BASE True` | `{"killed": 138, "survived": 62}` |
| mutant_direction_check | same, `--sample 14` (identity copy compared: `IDENT-SAME`) | `{"killed": 10, "survived": 4}` |
| round39_c1_audit | same, `--sample 9` | `{"survived": 6, "killed": 3}` (predicate n/a, §2.4) |
| tip_receipts witnesses | `python3 tipwit/witness.py $S $R $S/lane/plans/tip_receipts.py` | six `DIFFER` lines, §2.3 (`tipwit/out.txt`) |
| sources_adopt witnesses | `python3 srcwit/witness.py ...` | four `DIFFER` (one message-only), one `same` (`srcwit/out.txt`) |
| tip_receipts listing | `python3 plans/tip_receipts.py --lane . --list` | 5 mapped, 21 `skip reason=no-committed-re-run-command` incl. r39 git-leak, r40 db-wal |
| `--only nomatch` | `python3 plans/tip_receipts.py --lane . --list --only nomatch` | `tip <sha>` rc 0 |
| sources_adopt selftest | `python3 plans/sources_adopt.py --selftest` | `SELFTEST cases=17 failed=0` |
| state_check | `--selftest`; `--root lane --summary` | `[selftest] ALL PASS`; `VERDICT: PASS` |
| TB2 pin / screen | `git -C tb2 rev-parse HEAD`; `python3 tb2_screen.py tb2 cen/screen.json` | `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; `tasks 89`, 50 callable of 83 |
| constraints-scheduling probe | `python3 cs/run.py` ×2, `cmp` | `cases=16 observed_pass=3 observed_fail=13 mismatches=2`; `BYTE-EQUAL`; `cs/dry-table.txt` sha256 `8910143d9c5f742e…` |
| circuit-fibsqrt controls | bwrap + `gcc`, `solve.sh`, grader function | nop: `T test_sqrt_fib FAIL`; oracle (33.0 s): `T test_sqrt_fib PASS` |
| schemelike controls | bwrap, `solve.sh`, grader | nop `0 passed, 63 failed`; oracle (82.3 s) `63 passed, 0 failed out of 63` |
| prior art | `gh api repos/harbor-framework/terminal-bench-2-1/issues/245`; `gh api -X GET search/issues` | #245 closed 2026-10-08 "Bind constraints-scheduling checks to the requested event"; #135, #235, #3 open |
| round-39 §5 status | commands in §4 | R1 0/0 rows; R2 traceback; R3 0; R5 absent |
| routed population | script over `corpus/lessons/round-*-verifier-spotcheck.md` | per-round 8,11,7,4,2,6,6,7,8,7,5 = 71 |

## 9. Tools, scope, scratch

No tool installed (`bwrap`, `gcc`, `gh`, `git`, `python3` present); no pacman use. Writes: this report and
`.ufo/waves/round-40/build/R40PlanNext/` (`mut_harness.py`, `tb2_screen.py`, `tb2_screen.json`, `res_*.json`, `run_*.txt`,
`tipwit/`, `srcwit/`, `cs/`) only; the lane tree, claims, counters, probe, spec, gate, dry table, captures, receipt and
`claims/` were read, not written; no git add/commit in the lane; the source repo `shokuknow` untouched; no subagents.
Scratch `/fast/scratch/hyaku/kengaku-r40/R40PlanNext/` is removed after the last receipt copy.

VERDICT: plan41-drafted
