# TB2 grader class table — 13 executed graders as one dataset

Seat: CN2CrossSource (kengaku round 55, wave 1, connector). Date: 2026-10-30.
Base: `798f5e9ef30ef39291295565209b65a17343c00e` (freeze `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`).
Sources read: the 13 task-grader knowledge entries in `corpus/knowledge/` (12 held, rounds 35–46;
`tb2-chess-best-move-grader.md` landed this round) plus their committed probe receipts under
`corpus/evidence/`. Operation labels follow the seat spec's five-class vocabulary
(membership / literal / ldd-scan / chain-compare / multiset); rows name a primary operation and
annotate mixtures. Every receipt line below was re-read from the committed receipt bytes this seat.

## The 13-row class table

| # | task (round) | graded artefact | grader operation (primary) | partial credit | receipt cases |
|---|---|---|---|---|---|
| 1 | `protein-assembly` (r35) | agent-authored DNA text file (`/app/gblock.txt`; one line, lower-cased, translated in-process with Biopython) | **literal** — five amino-acid literals located by `str.find`; positional order chain, linker alphabet/length regexes, sliding GC window | none — one test fn → one reward bit | 18 cases: 5 P / 13 F, mismatches=0 (`corpus/evidence/round35/tb2-grader-probe.txt`) |
| 2 | `regex-log` (r36) | agent-authored regex pattern file (`/app/regex.txt`), compiled and executed **in the grader's process** against a 25-line log hard-coded in the test file | **literal** — full-list equality of `re.findall(...)` output vs 9 literal expected dates (count, order, type all matter) | none | 24 cases: 8 P / 16 F, mismatches=0 (`corpus/evidence/round36/regex-log-probe.txt`) |
| 3 | `configure-git-webserver` (r37) | live-service state (HTTP responses on :8080), read only through a captured helper script | **literal** — case-sensitive substring `TEST PASSED` in helper stdout; helper exit status never read | none | 22 cases: 9 P / 13 F, mismatches=0 (`corpus/evidence/round37/git-webserver-probe.txt`) |
| 4 | `build-pmars` (r38) | build provenance: installed binary at `/usr/local/bin/pmars` + `/app/pmars-*` source-tree shape | **ldd-scan** (class new at r38) — substring-absence scan of `ldd` output over four X11 lib names, plus presence check, start-anchored output regexes (`\d{5}` debugger addresses, `Results: \d+ \d+ \d+`), one-level directory-shape glob | none — four fns → one bit | 22 cases: 7 P / 15 F, mismatches=0 (`corpus/evidence/round38/build-pmars-probe.txt`) |
| 5 | `git-leak-recovery` (r39) | repository history state: refs + object store + reflog, one flag file, one work-tree checksum | **chain-compare** — ordered chain of git probes: two `log --all` searches (`--grep`, `-S`) must print nothing, init-message substring, `fsck --lost-found` → per-dangling-object `cat-file` substring-absence, pinned work-tree sha256; flag file literal equality | none — five fns → one bit | 25 cases: 13 P / 12 F, mismatches=0 (`corpus/evidence/round39/git-leak-probe.txt`) |
| 6 | `db-wal-recovery` (r40) | JSON export (`/app/recovered.json`) of a SQLite DB + XOR-encrypted WAL pair (the DB/WAL are read by no test) | **literal** — seven fns of per-cell equality against literals (22 of 33 cells pinned), type gates, sortedness and uniqueness over the export | none — seven fns → one bit | 28 cases: 8 P / 20 F, mismatches=0; regrade differ=0 (`corpus/evidence/round40/db-wal-probe.txt`) |
| 7 | `constraints-scheduling` (r41) | one-event ICS file, read by regexes (not an ICS parser), over sha256-pinned input calendars | **chain-compare** — the grader carries the constraint model that **decides the answer** (hard clauses + overlap + minute-by-minute earliest-slot scan); submission compared against the model's verdict | none — three fns → one bit | 25 cases: 6 P / 19 F, mismatches=2 (both carried from the r40 planning pilot, disclosed in-entry); regrade differ=0 (`corpus/evidence/round41/constraints-probe.txt`) |
| 8 | `circuit-fibsqrt` (r42) | gate-list data file (`/app/gates.txt`) that the grader never parses itself — it is **executed** by a 353-line C simulator the grader compiles at grading time | **chain-compare** — 28-value chain of simulator outputs vs `fibonacci(isqrt(N)) % 2**32` table; existence + raw line-count (<32000) | none — three fns → one bit | 16 cases: 7 P / 9 F, mismatches=0; regrade differ=0 (`corpus/evidence/round42/fibsqrt-probe.txt`) |
| 9 | `feal-differential-cryptanalysis` (r43) | agent-authored Python module (`/app/attack.py`) **imported into the grader's own interpreter** | **literal** — one equality after an in-process call: `feal_in_c.get_keys()[5] == attack.attack(feal_in_c.encrypt)` | none — one fn → one bit | 12 cases: 8 P / 4 F, mismatches=0; regrade differ=0 (`corpus/evidence/round43/feal-probe.txt`) |
| 10 | `feal-linear-cryptanalysis` (r44) | agent-written text file (`/app/plaintexts.txt`), read whole | **membership** (constant-compare family F1) — each of 100 decimal literals asserted as a substring of the file text (`assert c in data`); no count/order/format check | none — one fn → one bit | 14 cases: 8 P / 6 F, mismatches=0; regrade differ=0 (`corpus/evidence/round44/feal-linear-probe.txt`) |
| 11 | `password-recovery` (r45) | agent-written line file (`/app/recovered_passwords.txt`) | **membership** (constant-compare family F1, second exemplar) — one literal constant as a whole line among newline-split guesses; extras/decoys free (`decoys-1000` passes) | none — two fns → one bit | 16 cases: 5 P / 11 F, mismatches=0; regrade differ=0 (`corpus/evidence/round45/password-recovery-probe.txt`) |
| 12 | `polyglot-c-py` (r46) | agent-authored source file executed by **two toolchains at grading time** (python3 and gcc-compiled C) | **chain-compare** (dual-runtime class new at r46) — exact directory-listing equality, grader-side gcc build, then a 3-fixed-point chain compared in BOTH runtimes (6 stdout equalities against literals) | none — one fn → one bit | 18 cases: 7 P / 11 F, mismatches=0; **regrade differ=7** (same-process regrade instability, recorded in-entry) (`corpus/evidence/round46/polyglot-c-py-probe.txt`) |
| 13 | `chess-best-move` (r55) | agent-written token file (`/app/move.txt`) | **multiset** (class new at r55) — order-insensitive full-multiset equality over whitespace-split tokens vs the literal pair `["g2g4","e2e4"]`: `sorted(move) == sorted(...)` | none — one assertion → one bit | 12 cases: 5 P / 7 F, mismatches=0 (`corpus/evidence/round55/chess-best-move-probe.txt`) |

Totals: 13 tasks, 269 receipt cases (18+24+22+22+25+28+25+16+12+14+16+18+12), 12 of 13 with
mismatches=0 (constraints-scheduling carries 2 disclosed pilot mismatches), 12 of 13 with
regrade differ=0 (polyglot-c-py records differ=7).

## Cross-row structure

**Partial credit is uniform: none.** All 13 tasks map pytest exit status to a single reward bit
(`test.sh` writes 1 on exit 0, else 0 — byte-identical runner at chess and regex-log per amendment A1).
Multi-function graders (build-pmars 4 fns, git-leak 5, db-wal 7, constraints 3, fibsqrt 3) expose
per-test texture inside the receipt, but the reward collapses it to one bit. No grader in the set
graduates partial compliance; in the multiset and membership rows a partially-right artefact
scores exactly 0, same as an empty file.

**Every row is a constant-compare against literals held in the test file.** Even the
non-literal-primary rows reduce to literal material: the ldd-scan row scans for four literal lib
names; the chain-compare rows compare chains against literal tables (init message, 28-value
fib table, 3 Fibonacci fixed points) or literal-shaped model verdicts; the F1 membership rows
hold their answer constants in the published test file itself (feal-linear's 100 decimals are
copied verbatim out of `test_outputs.py:4-103`; password-recovery's 23-char constant likewise;
chess's move pair likewise). The fleet-level consequence measured across the dataset: for 3 of 13
tasks the published grader file alone yields a passing artefact with no task work
(`copy-public-constants`, `constant`, and chess's literal pair — though chess's instruction
example `h1h8` is *not* a graded winner, so the naive copy fails: `instruction-example-h1h8`).

**Receipt-case shape is uniform too:** each entry froze N synthetic end states with
prediction-before-run, executed the captured grader hermetically, and printed
`cases=N observed_pass=P observed_fail=F mismatches=0` (the round-53-onward probe discipline).

## Where chess-best-move sits

1. **Operation class: the multiset pole of the constant-compare family.** Chess bounds the two
   membership rows on the strict side. Same content, three rules:
   `g2g4 e2e4 h7h5` (both winners + one decoy) — feal-linear **P**, password-recovery **P**,
   chess **F**. `g2g4 e2g4…` duplicates flip chess to F where membership stays P. The r45
   receipt's headline `decoys-1000` (answer + 1000 wrong lines, shuffled, P) is exactly the
   state chess's `extra-decoy-move` case measures F. Order-freeness is shared with r45
   (both sort or are order-insensitive); what chess adds is multiplicity-exactness and
   any-whitespace token granularity (r45 splits on `\n` only — `constant-joined` fails there
   while chess's one-line `both-space-separated` passes).
2. **Novelty is combinatorial, not per-axis** — the wave-1 critic C4ClassNovelty ruled
   (`w1/C4ClassNovelty/ruling.md`): order-freeness alone appears at r45, exact
   count/multiplicity at r36/r40/r46. What no prior executed grader combines is
   order-free **and** multiplicity-exact **and** exact-count **and** any-whitespace-token over a
   bare agent-written token file. A repo sweep of all captured `test_outputs.py` files found no
   other `sorted(…)==sorted(…)` / `Counter(…)` decision (db-wal's `ids == sorted(ids)`
   *enforces* order on a structured JSON export — the opposite use).
3. **Simplest grader in the set:** one file, one assert, one literal pair, 25 lines of test code
   — and an instruction-to-grader gap of its own (the instruction's example `h1h8` is a format
   example the grader treats as an attempt; case 11).
4. **Frontier position:** 13th of 89 TB2 graders executed offline; the multiset row completes
   the dataset's span from most-permissive (membership) to most-strict (multiset) constant-compare.

## Routing recommendation — the fleet-level pattern goes to **kotoba**

**The pattern.** Across all 13 rows the reusable finding is not any single grader's quirk but the
**instruction-vs-grader gap, operationalized**: every entry carries a requirement map whose
`enforced / unenforced / partly` labels are derived from receipt cases, and 12 of 13 headline
cases are states that pass while violating the instruction's stated requirements
(`canned-shape` builds nothing; `literals-never-open-db` never opens the database; `lookup-28`
is a 28-point table, not a function; `decoy-first-vevent` schedules the wrong event first;
`token-in-body` serves no git server; `input-crlf-rewrite` modifies pinned inputs). The gap runs
both directions: instructions also state shapes graders never check (fibsqrt's "last 32 lines",
feal-linear's unnamed decimal format, chess's "one per line" enforced only as a token discipline).
The craft rule hiding in the data: an instruction's prose and its grader's assertions are two
artifacts, and the only honest bridge between them is a violation case per advertised requirement
— exactly the discipline these 13 entries ran.

**Why kotoba (primary).** Kotoba-shokunin's province is prompt/skill-file and output-contract
craft (`kotoba-shokunin/SKILL.md:3-15`; fleet routing precedent: prompt-craft implications →
kotoba in rounds 11/12/13/14 connectors). The requirement-map gap is an instruction-authoring
craft problem — how to phrase requirements so a constant-compare grader is faithful to them, and
how grader authors should read instructions before writing assertions. Send kotoba: the class
table's gap column (unenforced instruction lines per task), the three F1 attack-free passes, and
the chess `h1h8` example-literal trap, as evidence-sent-never-absorbed.

**Why not tameshi (as the primary).** Tameshi-shokunin already owns the *method* these entries
exercised — frozen predictions, hermetic suites, regrade legs, mismatch counters are its playbook,
and kengaku's 13 probes are applications of that method, not new craft. Routing the probe pattern
to tameshi would re-transfer its own doctrine. One genuine tameshi-adjacent residue exists: the
five-operation class table as a **fixture-discrimination taxonomy** (which decoy shapes
discriminate membership vs multiset vs literal — e.g. an "extras" decoy is load-bearing for
multiset graders and vacuous for membership graders). That residue is an optional secondary copy;
the primary fleet pattern — the gap discipline — is kotoba's.

**Suggested referral text (for the L1/connector to file):** "Kotoba: kengaku rounds 35–55 executed
13 TB2 task graders offline; every instruction-vs-grader map is receipt-derived. Reusable craft
candidates: (1) any advertised requirement without a violating test state should be labelled
unenforced, not assumed; (2) example literals in instructions are graded as attempts when the
grader constant-compares (chess `h1h8`); (3) answer constants live in published test files for
membership/multiset/token-file classes — instruction prose should either avoid naming them or the
grader should derive them. Return a craft rule only; the 13 measurements stay kengaku-owned."

## Defects / anomalies observed in the dataset (reported, not fixed — siblings own the files)

- `constraints-scheduling` receipt carries mismatches=2 (r40 pilot errors carried verbatim,
  disclosed in-entry). Not a defect of the instrument; recorded for calibration honesty.
- `polyglot-c-py` receipt records `regrade differ=7` — same-process regrade instability in the
  r46 probe; every other row's regrade leg is differ=0. Calibration-relevant if regrade legs are
  ever wired into a predicate.
- `tb2-chess-best-move-grader.md` header still records `second-seat re-read: pending (R3)` —
  the Q13/Q14 admission re-read was outstanding at the time of this seat's read; admission is
  the L1's call.
- Round-55 claims note chess `test.sh` is byte-identical to the held regex-log runner (S109);
  the class table therefore lists 13 receipts but only 12 distinct runner bytes.
