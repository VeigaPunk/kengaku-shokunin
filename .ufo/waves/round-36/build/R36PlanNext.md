# R36PlanNext — `### Planned (round 37)` draft (kengaku r36, wave 1, scribe)

Seat: R36PlanNext (scribe, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Deliverable: a paste-ready `### Planned (round 37)` block for `SCORECARD.md`, the matching `LOG.md`
next-iteration line, and the grounding for both. No lane file was edited; nothing was committed.
Scratch: `.ufo/waves/round-36/build/R36PlanNext/` (census receipt) and `/tmp` (removed, §9).

Axes named before work (Godspeed): **A1 class distance** (is the candidate a grader class the lane has
never read?), **A2 offline executability / receipt byte-determinism**, **A3 independent
recomputability of the expected verdicts**, **A4 source supply** (≥8 distinct 3–25-word quotes at ≥8
distinct located lines), **A5 id/registry collision**, **A6 prior-art clearance**. A1/A2/A5 were cheap
and ran first; A6 was spent only on the candidate that survived them.

## 0. Inputs read, in this order

| Input | State at read time (2026-10-25) |
|---|---|
| `plans/round-36-claims.md` (freeze `3241b86c`, Amendment 1 `acbda2f3`) | read in full; C1 gate contract + battery, C2 W1–W6, separability, frozen digests |
| `SCORECARD.md:1152-1206` (`## Planned (round 34)`, `### Planned (round 35)`, `### Planned (round 36)`) | read; round-36 planned block is the input the assignment names |
| `LOG.md` tail (through the round-35 errata) | read; style for the next-iteration line |
| `.ufo/waves/round-36/build/R36ScoutNextTasks.md` | **present**, read in full (17 tasks surveyed, grader-fed taxonomy a–g, top-3 ranked) |
| `.ufo/waves/round-36/build/R36ScoutMergePkg.md` | **present**, read in full (1 admit-candidate, 1 refuse, 3 text repairs open) |
| `.ufo/waves/round-36/build/R36ScoutTB2Visibility.md` | present, read in full (`tests/` uploaded after the agent run) |
| `.ufo/waves/round-36/build/R36ReopenPins.md` | present, read in full (pin 5/5, drift no, `main` == pin) |
| `.ufo/waves/round-36/build/R36ScoutPriorArt/` | **empty directory** — no prior-art scout report exists yet; §1.4 is this seat's own pricing |
| `.ufo/waves/round-36/claims/control-c1-nothing.txt`, `control-c2-nothing.txt` | read; format mirrored for the round-37 control receipts |

Axis state carried forward unchanged (frozen in `round-36-claims.md:5-7`): coverage 7, novelty 7
(tied lowest non-retired), calibration 8, depth 9, operability 8, freshness 8, adjacency 8; coverage
capped by the open L0 (`.ufo/l0-questions.md:163`). No stagnation waiver is claimed by this plan.

## 1. Ground this seat opened (not previously in the corpus)

### 1.1 TB2 task class census at the C2 pin

`harbor-framework/terminal-bench-2 @ 2fd12b88aafdd04a52c298e3940bcb189f9766d6` — the same pin C2 uses.

```
$ curl -sS "https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88…?recursive=1"
entries 1446      (matches R36ReopenPins A1: entries 1446, truncated=false)
$ curl -fsSL -o tb2.tar.gz "https://codeload.github.com/harbor-framework/terminal-bench-2/tar.gz/2fd12b88…"
bytes 40357259   extracted 47 MB, 89 task dirs (every one carries tests/test_outputs.py)
```

Class census over `tests/` with `tests/test.sh` **excluded** (test.sh always curls the uv installer, so
including it inflates every task's "service" count — the first pass of this census was discarded for
that reason):

| class marker | definition used | tasks |
|---|---|---|
| live-service / process | `test_outputs.py` + helper scripts issue `requests.get`/`socket.`/`grpc.`/`localhost`/`ss -`/`pgrep` | 9 of 89 |
| file-tree / repository state | `os.walk`/`rglob`/`filecmp`/`iterdir`/`git.Repo`/`repo.commit` | 6 of 89 at ≥2 hits: `build-pmars` 3, `financial-document-processor` 3, `sanitize-git-repo` 3, `reshard-c4-data` 2, `schemelike-metacircular-eval` 2, `sqlite-with-gcov` 2 |

Service-class ranking (marker hits, files, grader bytes):

```
kv-store-grpc              12  test_outputs.py                       6070
nginx-request-logging      10  test_outputs.py                       5947
configure-git-webserver     6  test_outputs.py,verify.sh             3216
hf-model-inference          5  test_outputs.py                       4239
git-multibranch             4  test_outputs.py                       2625
install-windows-3.11        3  qemu-control.sh,test_outputs.py      21067
headless-terminal           2  test_outputs.py                       3676
pypi-server                 2  test_outputs.py                       3173
qemu-startup                2  test_outputs.py                       1732
```

Receipt: `.ufo/waves/round-36/build/R36PlanNext/tb2-census.txt` (tarball `sha256` + the two tables +
the local capability census). Cross-check that the census bytes are the pinned bytes: for five files the
raw fetch and the tarball agree byte for byte (§1.2 digests were computed from both).

`R36ScoutNextTasks.md` surveyed 17 *non-service* tasks and ranked `log-summary-date-ranges` first; its
taxonomy (a) data string, (b) agent-authored regex file, (c) output file vs constants, (d) numeric file
under tolerance, (e) artefact vs brute-force search, (f) file-tree hash compare, (g) agent code under
signals/timing deliberately excludes the service class (it marked `hf-model-inference` and
`filter-js-from-html` "excluded: service + network"). The 9-task service family above is therefore new
ground, and it is the family the assignment's direction (a) names.

### 1.2 Direction (a) primary package: `configure-git-webserver`

Pinned digests (raw `raw.githubusercontent.com/.../2fd12b88…/configure-git-webserver/<path>` ==
`codeload` tarball, byte-identical; sizes from the tree API agree):

| file | bytes | sha256 |
|---|---|---|
| `tests/test_outputs.py` | 553 | `526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37` |
| `tests/verify.sh` | 2681 | `1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05` |
| `instruction.md` | 451 | `62151b7371bc364277a3c118bba755334c640fb0cefc7a5af106e6e763cf1d97` |
| `task.toml` | 932 | `ebb40d72f689512cbd90d865d88ef966b6665ab215544f9247b898b7fa94751b` |
| `solution/solve.sh` (oracle) | 2354 | `c31cd92ecb1b357d8c0abcf4821717e83a1770cf58f028620cd0ee3e6b1e4c62` |

Structure (static read, **unexecuted** — every behavioural statement below is `[INFERENCE]` until the
round-37 probe runs; that is exactly what the claim would buy):

- The whole graded surface is one pytest function whose assertion is a substring:
  `test_outputs.py:9-13` — `run(["bash", "/tests/verify.sh"])` then
  `assert "TEST PASSED" in result.stdout`. The function is named `test_hello_html_exists` but never
  tests a file (`:9`), only a token in another process's stdout (`:13`).
- `verify.sh` is the real grader and has no `set -e`: `:16-31` writes an `expect` script, `:49` runs it,
  and nothing reads its exit status; `:53-71` then curls `http://localhost:8080/hello.html` and prints
  the token at `:64` (curl branch) or `:81` (wget branch). The only failing prints are
  `❌ TEST FAILED` (`:66`, `:71`, `:83`, `:88`), which do not contain the token.
- `instruction.md:1-9` asks for three things — a git server, push/commit, and automatic deployment to a
  web server on :8080 — and the verdict token is printed iff the *web content* equals `hello world`.
  So the git-server and post-receive halves are, on a static reading, unenforced: a file written
  straight into the document root prints the token without a repository, a hook or a push.
- `task.toml`: `difficulty = "hard"`, `category = "system-administration"`, `allow_internet = true`,
  `docker_image = "alexgshaw/configure-git-webserver:20251031"`, verifier timeout 900 s.
- `R36ScoutTB2Visibility.md` settles the channel question that the entry must respect: `tests/` is
  uploaded to `/tests/` only at verification, so `verify.sh` is not agent-visible during the run — but
  the repository is public and `allow_internet = true`. "Hidden from the agent" is not writable without
  the public-repo/internet qualifier.

Why this one and not the higher-hit `nginx-request-logging`: the probe must be executable offline on
this host. Census of local capability (`command -v`, this host):

```
nginx=ABSENT  expect=ABSENT  sshd=/usr/bin/sshd  git=/usr/bin/git  curl=/usr/bin/curl
docker=/usr/bin/docker (server 29.9.1)  uv=/home/vgpnk/.local/bin/uv  port8080_listeners=0
```

`nginx-request-logging` grades through `nginx -t` and `/etc/nginx/*`, `/var/log/nginx/*`
(`test_outputs.py:59-121`), which this host cannot provide without root writes outside the lane or a
container pull — A2 fails. `configure-git-webserver`'s verdict channel needs only bash, a loopback HTTP
server on the free :8080, and `git`; `sshd` is present if a verbatim git arm is attempted. A4 is
satisfied with margin: 3–25-word quote-eligible lines measured at 46 in `tests/verify.sh`, 9 in
`instruction.md`, 7 in `tests/test_outputs.py`.

### 1.3 Direction (a) alternates, priced not chosen

| alternate | class | digests / evidence | why it is not the primary |
|---|---|---|---|
| `nginx-request-logging` | service | test_outputs.py `045cc716…`, test.sh `27761195…`, instruction `26a7ac98…`, task.toml `b7a78d00…`, solve.sh `2454bbbf…`; 8 pytest functions, 5947 B | `nginx` absent locally; grading needs `/etc/nginx` + `/var/log/nginx` (A2) |
| `sanitize-git-repo` | file-tree + history | test_outputs.py `57e49041…`, test.sh `16014722…`, instruction `d9e10a56…`; ships three reference files inside `tests/` | `git.Repo("/app/dclm").commit("d6987af…")` pins a specific upstream commit, so an offline fixture cannot reproduce it verbatim (A3) |
| `fix-git` | file-tree hash compare | scout-measured `a8a6f51e…43f3` test_outputs.py, `f98174e4…ec4e` instruction | 1194 B + 158 B instruction: quote supply thin (A4), and setup needs a network clone |
| `log-summary-date-ranges` | output file vs constants | scout's #1; source digests in `R36ScoutNextTasks.md`; generator recompute `mismatch 0` | best A3 of the set, but class (c) is the closest to the two admitted classes; keep as the fallback if A2 fails for the service probe |

### 1.4 Direction (b) prior-art pricing (A6)

The construct named in the assignment — mutate each requirement/instruction clause and measure which
clauses the grader leaves unenforced, across two tasks — is **covered by published work**. The one
source this seat opened itself:

- *Mutation Testing of Task-Scoped State Oracles in Software-Agent Benchmarks: A Cross-Benchmark
  Empirical Study* — `https://www.researchsquare.com/article/rs-10665114/v1`, DOI
  `10.21203/rs.3.rs-10665114/v1`, `citation_publication_date = 2026-08-18`. Its abstract (opened page,
  metadata tag `description`) reads in part: "Stateful software-agent benchmarks increasingly use
  executable evaluators to decide whether an agent produced the requested persistent effects. Yet a
  high task score is informative only if the evaluator rejects harmful extra effects without rejecting
  equivalent representations." That is both directions of the census the assignment proposes.

Search-summary hits (**not opened by this seat**; a round-37 gate must open them before citing):
specification mutation (Gopal & Budd 1983 lineage), CTL-clause mutation (Ammann/Black/Majurski),
property-based mutation testing (TU Wien), SWE-ABS, *Evaluating the Test Adequacy of Benchmarks for LLMs
on Code Generation* (2025), TestJack (2026-10). The corpus already carries the adjacent row S045
(evalmut 0.1.0) and the round-26 verdict that "equivalent-response mutation testing of answer graders is
already shipped tooling" (`corpus/SOURCES.md:67`, `:143`).

Consequence for the plan: (b) is not fileable as a novelty claim on this evidence. The plan therefore
files it **with a kill switch and a demotion clause** rather than betting the novelty axis on it (§6,
C3). This is the same discipline round 36 used when it declined a novelty claim for want of an opened
source — except that now the opened source exists and is adverse, which is a stronger reason to price
it before freeze rather than after.

## 2. Competing wave-1 coverage candidate and id allocation

`R36ScoutMergePkg.md` §1 puts `grader-predicate-input-types.md` (staged S143/S144, proposed S111/S112)
at **ADMIT-CANDIDATE, conditional**, with five landing conditions and three text defects (§5: the
"never bare strings" claim contradicted by 6 of 16 string-typed functions; denominator 38 vs 37; an
unreproduced `compare_rating` narrative). It is a Toolathlon comparison-function probe — the scout's
own note is that it "is adjacent to C2: both execute a pinned benchmark grader offline with typed
fixtures", i.e. the *same* class family, not a new one. On A1 it loses to the service-class grader; on
A2 it is cheap. Both candidates are opened, so the tie-break sentence selects on class distance and
executability, in that order.

Ids are not pre-assigned by this plan: `corpus/SOURCES.md` currently ends at S107, round 36 C2 reserves
S108–S110, and the merge package wants S111/S112. The freeze must re-derive the next free id
(`grep -oE '^\| S[0-9]{3}' corpus/SOURCES.md | tail -1`) and allocate in landing order if both
candidates are claimed in the same round; the two must not share an id.

## 3. What the round-36 gate leaves for round 37 (calibration input)

`round-36-claims.md` names its own limits, and they are the round-37 calibration work without any new
invention:

1. "A mutant that survives a wave-2 mutation seat is reported as a limit, never repaired into the
   frozen battery" — so gate weakness must be found *mechanically* next round, not by another wave of
   seats that cannot change the frozen predicate.
2. The battery's own semantics are frozen at 14 fixtures and 4 ledger rows; a gate that recognises a
   fixture by name/path/marker is the named attack for wave 2.
3. Amendment 1's pre-scoring repair of a frozen instrument is still an open L0 question
   (`revenger | round-69`); the plan keeps every instrument frozen before its first run, so round 37
   does not repeat the situation.

The natural instrument is therefore a mutant battery over `plans/pkg_gate.py` itself (a copy is mutated
byte-wise inside the existing fixture root; the unmutated copy is the null mutant that must *not* be
detected). This is the same shape as `R35ProbeHarnessMut` / `R36ProbeHarnessMut` (m0-unmodified control
plus per-defect mutants), already proven to work in this lane.

## 4. DRAFT — `### Planned (round 37)` (paste-ready for `SCORECARD.md`)

```markdown
### Planned (round 37)

- **Calibration (8):** attack the round-36 gate instead of the counters it replaced. `plans/round37_gate_mutants.py`
  copies `plans/pkg_gate.py` into the frozen battery's fixture root and applies one byte-level mutant per defect
  class — fixture recognised by path/name/marker, receipt digest pin dropped, one-word quotes accepted, duplicate
  S105/S106/S107 row accepted, non-pairwise-distinct teaches accepted, capture manifest unpinned, `--rerun` byte
  compare skipped, d4 swapped-citation accepted, untracked scan narrowed to one subdirectory, unparsed quote row
  skipped — with an unmodified copy as the null mutant.
  Predicate (to freeze): `python3 plans/round37_gate_mutants.py --lane .` prints `MUTANTS total=<N> detected=<N>
  null_detected=0`, then `PREDICATE C1 pass`, exit 0, and the round-36 battery still prints its frozen
  `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0` unchanged.
  Before / do-nothing: on the pre-round-36 tree the gate is absent, so the harness prints
  `total=<N> detected=0 unevaluated=<N>`; a detector that reports "detected" unconditionally prints
  `null_detected=1`. Both red controls freeze at `.ufo/waves/round-37/claims/`.
  Survivors are reported as gate limits; the 14-fixture battery and its predicate are not edited (round-36 kill rule).

- **Coverage (7, lowest, tied with novelty 7; tie-break: pinned local source + offline-executable probe):** a third
  Terminal-Bench 2.0 task grader, chosen for class distance — `configure-git-webserver` @ `2fd12b88` grades live
  system state (ssh git server, post-receive deploy, nginx on :8080) and its entire verdict is one stdout substring,
  `"TEST PASSED" in result.stdout` (`tests/test_outputs.py:13`) over a helper script with no `set -e`
  (`tests/verify.sh:49`, token at `:64`). Round 35 admitted a data string; round 36 an agent-authored regex executed
  inside the grader; this is the first state/process grader the lane would read. Rows S111 (`tests/test_outputs.py`),
  S112 (`tests/verify.sh` — the first admitted row for a helper script that *carries the checks*; S106 was a runner
  that only mapped pytest's exit status to a reward), S113 (`instruction.md`), captures at
  `corpus/evidence/round37/tb2-git-webserver/` with `SHA256SUMS`, entry
  `corpus/knowledge/tb2-git-webserver-grader.md`, probe `plans/git_webserver_probe.py` with predictions written
  before the first run, receipt `corpus/evidence/round37/git-webserver-probe.txt`.
  Predicate (to freeze): `python3 plans/round37_c2_verify.py --lane .` prints `checks=7 defects=0` then
  `PREDICATE C2 pass`, exit 0, and the receipt's summary line reads
  `cases=<n> observed_pass=<p> observed_fail=<f> mismatches=0`.
  Before / do-nothing: entry, rows and captures absent — the same command is red on W2–W6 with only the capture and
  registry checks live (`.ufo/waves/round-37/claims/control-c2-nothing.txt`); the cheap skip-control (junk rows,
  one-word quotes, a hand-typed receipt, an index row with no coverage bullet) must stay red.
  Fallback order if the service probe cannot hold a byte-equal receipt: `fix-git` (file-tree hash compare, grader half
  offline) → `log-summary-date-ranges` (output file vs 15 recomputable constants, wave-1 scout measured `mismatch 0`).
  One task is claimed, not two; the choice is recorded at freeze.

- **Novelty (7, tied lowest) — filed only behind a prior-art gate:** the two-task requirement-class census (which
  classes the frozen graders leave unenforced: boundary adjacency, month validity, leading zeros, hard-coded fixed
  inputs) measured on regex-log and protein-assembly. The construct is already published — *Mutation Testing of
  Task-Scoped State Oracles in Software-Agent Benchmarks* (`10.21203/rs.3.rs-10665114/v1`, 2026-08-18) states the
  two-sided requirement explicitly — so no novelty credit is requested on the present reading.
  Predicate (to freeze): `python3 plans/round37_priorart.py --lane .` prints `constructs=1 covered=0 verdict=clear`
  before any novelty move is claimed; `covered=1` files the adverse row and takes no novelty move, while the census
  still runs as calibration data (`tasks=2 classes>=4 mismatches=0` over the two admitted receipts).
  Do-nothing / skip-control: the two admitted probe receipts are unchanged at freeze, and a census that re-labels
  existing probe cases instead of deriving one mutant per instruction clause is rejected — each class carries a
  mutant id, its own frozen prediction and an observed verdict.
```

## 5. DRAFT — `LOG.md` next-iteration line (paste-ready, one paragraph)

```markdown
**Next iteration (round 37, planned in the round-36 wave-1 build — not a claim until frozen):** calibration turns on
the instrument it just built — `plans/round37_gate_mutants.py` must print `MUTANTS total=N detected=N
null_detected=0` against `plans/pkg_gate.py`, with the round-36 14-fixture battery byte-unchanged and any survivor
reported as a gate limit; coverage (7, lowest, tie-broken over novelty 7) opens a third Terminal-Bench 2.0 grader of a
different class, `configure-git-webserver` @ `2fd12b88`, whose whole verdict is one stdout substring over a helper
script, adding rows S111–S113 with captures and a frozen-prediction probe (`checks=7 defects=0`, `PREDICATE C2 pass`);
novelty stays 7 — the requirement-class census across regex-log and protein-assembly is prior-art covered
(researchsquare `10.21203/rs.3.rs-10665114/v1`, 2026-08-18) and is filed only behind a kill switch that demotes it to
calibration data. Class census: 9 of 89 TB2 tasks at the pin grade a live service; controls, fallback ranking
and the census receipt are in `.ufo/waves/round-36/build/R36PlanNext.md`.
```

## 6. Controls named (so the round-37 freeze can reuse the sentence discipline)

| claim | do-nothing control (pre-landing) | skip-control (cannot reach the target) |
|---|---|---|
| C1 gate mutants | gate absent at the pre-round-36 tree → `detected=0 unevaluated=<N>` | detector that always prints "detected" → `null_detected=1`; harness pointed at an unmutated gate must print `detected=0` |
| C2 third grader | entry/rows/captures/probe absent → `checks=7 defects=<k>` exit 1 (mirrors `control-c2-nothing.txt`) | junk rows + one-word quotes + hand-typed receipt + index row without a coverage bullet; probe whose printed receipt is pasted rather than run (counter pins the probe digest and re-runs it) |
| C3 census | the two admitted receipts unchanged; `classes=0 tasks=0` | re-labelled probe cases (no per-class mutant id, no own prediction) must be rejected |

## 7. Ranking, stated as a decision the L1 can reverse cheaply

1. **Coverage claim = third TB2 grader, service class (`configure-git-webserver`).** A1 maximal among
   opened candidates (first state/process grader), A2 satisfied by bash + loopback :8080 + git, A3 weak
   (no independent expected-value oracle, unlike `log-summary-date-ranges`), A4 ample, A5 clean if ids
   are re-derived at freeze. Its weakness is A3: the probe's expected verdicts come from a static
   reading of `verify.sh`, so the receipt proves grader behaviour, not task validity — the entry must
   say so, and the case table must include at least one *permitting* case (a direct file write with no
   git) to show the git half is unenforced, plus one *rejecting* case (wrong content) to show the token
   is not free.
2. **Fallback = `log-summary-date-ranges`** if the service probe cannot produce a byte-equal receipt in
   two runs (the round-36 Amendment-1 lesson: byte-determinism must be proved *before* the freeze).
3. **Novelty claim = not filed on this evidence.** Filing it as novelty would repeat round 26's outcome
   (`novelty +1 capped by published tooling`, `SCORECARD.md:707`), one round later and with a stronger
   citation against it.

## 8. Evidence ledger

| Claim | Command | Output |
|---|---|---|
| TB2 tree at the pin has 1446 entries / 89 tasks | `curl …/git/trees/2fd12b88…?recursive=1` + python | `entries 1446`; `tasks 89` |
| tarball at the pin is 40,357,259 B | `curl -o tb2.tar.gz codeload…/tar.gz/2fd12b88…`; `stat -c%s` | `40357259` |
| 9 of 89 tasks grade a live service | census script over `tests/` excluding `test.sh` | table §1.1 (receipt `R36PlanNext/tb2-census.txt`) |
| `configure-git-webserver` digests | `sha256sum` over raw fetch **and** tarball | identical, 5/5, §1.2 |
| its verdict is one stdout substring | `cat -n tests/test_outputs.py` | `:13 assert "TEST PASSED" in result.stdout` |
| `verify.sh` never propagates the git half's status | `grep -n "TEST PASSED\|git_test.exp\|^# This script"` | token `:64`,`:81`; script run `:49`; no `set -e` |
| quote supply for the three rows | python line scan, 3–25 words | verify.sh 46, instruction.md 9, test_outputs.py 7 eligible lines |
| host can run the loopback fixture | `command -v …`; `ss -ltn \| grep -c ':8080'` | nginx/expect ABSENT; sshd/git/curl/docker/uv present; 0 listeners |
| (b) is prior-art covered | `curl -fsSL https://www.researchsquare.com/article/rs-10665114/v1` + metadata scan | title, DOI `10.21203/rs.3.rs-10665114/v1`, date 2026-08-18, abstract quoted §1.4 |
| registry/id state | `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md`; `grep -oE '^\| S[0-9]{3}' corpus/SOURCES.md \| tail -4` | `registry_rows=100`, ids end at S107; S108–S110 reserved by round 36 |

## 9. Limits (what this seat did not do)

- **Nothing was executed.** Every statement about `configure-git-webserver` behaviour is a static read of
  the pinned bytes, marked `[INFERENCE]` in §1.2. The round-37 probe is what turns those into evidence;
  the plan's predicate numbers for that probe are deliberately left as `<n>`/`<p>`/`<f>` rather than
  predicted here.
- **No container run.** `docker` server 29.9.1 is available but no task image is local; the plan does
  not depend on pulling one.
- The prior-art pricing is one opened primary page plus search summaries; four of the five anchors are
  unopened and must be opened before any row is registered. `R36ScoutPriorArt/` is an empty directory
  at the time of writing — a wave-1 prior-art seat may still land a report after this file; if it does,
  its verdict supersedes §1.4 only.
- The TB2 class census is marker-based (regex over grader text), not a manual read of 89 graders: the
  counts are lower bounds on each class and could not resolve a task that grades a service through a
  helper the regex misses (e.g. a dynamically written script, as `git-multibranch` does).
- Scratch `/tmp/tb2`, `/tmp/tb2.tar.gz`, `/tmp/tb2tree.json`, `/tmp/rs.html` were this seat's; the
  census receipt in `R36PlanNext/` is self-contained (`sha256` of the tarball included) and the `/tmp`
  copies were removed after the receipt was written.
- No lane file, `plans/`, `corpus/` or git state was touched; no tool was installed or upgraded.

VERDICT: plan-drafted
