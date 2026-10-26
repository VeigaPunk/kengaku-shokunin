# R36CritScope — C2 scope against PROVINCE (round 36, wave 1, 2026-10-25)

Seat: `R36CritScope`, critic, leaf. Lane `kengaku-shokunin` at `b662a5d6`; reports only, no lane file
edited, no counter run for scoring, no commit. Scratch:
`.ufo/waves/round-36/build/R36CritScope/`.

**Answer in one line:** executing the pinned `regex-log` grader on lane-authored candidate patterns is
**inside** province — the same class as round 35's `protein-assembly` probe and strictly narrower than
round 29's generator projection — but the drafted bytes carry five pressure points that a wave-2 seat
will read as task-validity or model-performance claims, plus an axis name that invites "quality work on
new inputs". Ten wording fixes below; none changes the frozen predicate.

---

## 1. Does executing cross the line? (no — with the test I ran)

PROVINCE's three relevant boundaries:

- round 29a2 (`PROVINCE.md:206-211`): owns *reading* published maintainer artefacts; "it does not run a
  benchmark, certify a task, or own deployment configuration, runtime task validity, hosted judges,
  contamination measurement".
- round 35 (`PROVINCE.md:230-240`): "static interpretation and offline synthetic-fixture execution of
  one pinned … grader function … does not run Terminal-Bench or the task image, validate or certify the
  task or any real submission, … or measure model performance."
- round 29 (`PROVINCE.md:204-207`): the lane already *executes* pinned maintainer code offline — "an
  offline, source-faithful projection of the pinned WebArena generator … over the 812 raw tasks × 3
  synthetic `*.invalid` profiles".

Applied to C2's instrument:

| Boundary question | Answer | Evidence (command → output) |
|---|---|---|
| Runs a benchmark / the task image? | No | `plans/regex_log_probe.py:82-95`: `spec_from_file_location` on the captured file, `tempfile.TemporaryDirectory`, `mod.Path` rebind, `mod.test_regex_matches_dates()`; no docker/pytest/`test.sh`/`/logs` write. `grep -n 'Path\|import' plans/tb2_grader_probe.py` shows the identical `mod.Path = lambda …` pattern at `:126` for round 35. |
| Certifies/validates a task or a real submission? | No (but see the oracle pressure point, §2.3) | The 24 inputs are lane-authored; no agent output, trajectory or model is read anywhere; the probe's only verdict is `pass`/`fail` + first `AssertionError` text. |
| Runtime task validity / model performance? | No | no image, no harness, no model call; probe imports only `argparse, hashlib, importlib.util, pathlib, sys, tempfile` — no network, no endpoint. |
| New *surface* relative to round 35? | One instance, same code shape | `cmp`-level structure: capture digest pin + `run_grader` + frozen case table; the only difference is the input class (a pattern string rather than a data string). |

So: `round-29 projection (executes maintainer code) ⊃ round-35 function execution ⊃ C2 function
execution on lane patterns`. C2 is the weakest member of an already-admitted family. **Inside.**

### The strongest counterexample available, and why it still holds

Tested: *"C2 executes the maintainers' own oracle (`solution/solve.sh`) through the grader and reports
instruction↔oracle divergence — that is a maintainer oracle-consistency check, and round 29a2 says this
lane reads such instruments but does not run them."*

Ruling: still inside, for three reasons, each checkable locally — (a) `solve.sh` is a published
maintainer artefact in the pinned tree, the class round 29a2 explicitly admits *reading*; (b) what was
executed is the *pattern text* the lane extracted, not the script, and it entered the same
`run_grader()` path as every lane-authored case (`entry.md` oracle block states "same `mod.Path`
redirection the probe uses"); (c) no verdict follows from it — an offline `pass` on one pattern is not
"the task is solvable", not "the task is consistent", not "the oracle is wrong". **But** the draft's
current sentence ("the instruction's line-4 rule is not enforced by the oracle either") is one reader
step from a validity verdict; F3/F4 remove that step.

Second counterexample tested: *"`still score 1` is a reward statement, i.e. a run claim."* The receipt's
`observed=pass` comes from catching `AssertionError` only; `test.sh` (S109) was read, not run; the image
executes `uvx -p 3.13 … pytest==8.4.1` (`test.sh:18,22`) while the probe ran host Python 3.14.8
(`python3 --version`). The conclusion "scores 1" therefore crosses two unexecuted links. That is a
provenance overstatement (and an operability risk for byte-equality, §5), not a scope crossing.

## 2. Where the drafted bytes press on the line

Files read: `build/R36EntryDraft/entry.md` (214 lines), `build/R36ProvinceDraft.md`,
`build/R36ReadmeDraft.md`, `build/R36SkillDraft.md:57-86`, `plans/regex_log_probe.py`,
`corpus/evidence/round36/tb2-regex-log/{test_outputs.py,test.sh,instruction.md,task.toml}`.

1. **`still score 1` / `scores 1` (entry:21-22, :109, :164; skill draft:78-80, "a passing submission can
   be a hardcoded alternation").** Reads as a task reward, i.e. a harness run. It is an inference from the
   read-only `test.sh` mapping.
2. **`the fixed, visible log is the whole test surface` (entry:21-22; repeated at :109-110).** "Visible" is a solve-time
   harness premise this lane has not established. Round 31's entry (`benchmark-verifier-execution-model.md:61-70`)
   reads the *verification-time* path only: the harness re-uploads the tests into `/tests` as part of
   `Verifier.verify()`. Nothing there says the test file is readable by the agent during its run; the
   honest statement is the weaker, sufficient one: the graded input is the grader's own fixed fixture and
   the expected values are literals in the test file. As written, "visible" converts a grader-semantics
   finding into a solver-reachability claim (and invites "an agent can just hardcode it").
3. **Oracle block (entry:147-178).** "Executed against the captures … `captured grader on oracle pattern:
   pass`" is the closest approach to a maintainer validity instrument (oracle-passes). It is admissible
   only if the sentence names it as *one offline application of the captured function to the extracted
   pattern text*, says `solve.sh` itself was read, not run, and refuses the solvability/consistency
   inference. Currently the section header says "own reading, not a graded result" but the findings read
   as adjudication.
4. **`the instruction's line-4 rule is not enforced by the oracle either` (entry:177-178)** — a
   compliance verdict on a maintainer artefact. The observable is narrower: *the extracted pattern
   admits `01.`-style octets, where `instruction.md:4` asks for none*. Which artefact is authoritative
   is the maintainers' call and should be routed out, not decided in the entry.
5. **Skill draft's `What to do: read tests/ before trusting a pass` (:78-80).** This is solver guidance
   (read the held-out test file) resting on the same unestablished visibility premise, in a permanent
   `SKILL.md` section. Its own province does not own solver strategy, and the sentence is the most
   quotable thing in the round for a reader who wants to say this lane published a gaming recipe. The
   same draft's own §Limits (:190-193) already says "whether a TB2 agent can see `/tests` at solve time is
   not established by any committed byte here" — the body sentence contradicts its own limit, so deleting
   it costs nothing.

Not defects: the entry's `## What the grader checks` table, the six findings' mechanics, the
`1134`-absence claim (`grep -n '1134' test_outputs.py` → exit 1), the Feb-29 absence
(`grep -n '02-29' …` → exit 1), and every located-quote line number I checked
(`test_outputs.py:8,21,87,90`; `test.sh:22,25,26,28`; `25` log lines, `9` expected dates by AST walk).

## 3. Wording fixes (10; each is drop-in)

**F1 — score verb discipline (entry + skill draft).** Define the receipt vocabulary once, immediately
after the summary line:

> `pass` below means *the captured `test_regex_matches_dates` returned without raising `AssertionError`
> under the probe's `Path` redirect*; `fail` means it raised, and the first assertion text is quoted.
> `tests/test.sh` (read, not run) maps a zero pytest exit to `reward.txt = 1`; this probe never runs
> pytest, the image or the harness, so "scores 1" is shorthand for that mapping, conditional on pytest
> collecting and running the file inside the image.

Then replace each "scores 1" with "returns without `AssertionError` (⇒ reward 1 under S109's mapping)".
Skill draft `:85`: "so a passing submission can be a hardcoded alternation" → "so a green fixed log
cannot distinguish a stated-rule regex from a literal alternation of the expected values".

**F2 — drop "visible" (entry:21-22, :109-110).**

> … the graded input is the grader's own fixed 25-line fixture and the expected values are literals in
> the test file; whether the test file is readable by the agent at solve time is a harness property this
> entry does not establish (`knowledge/benchmark-verifier-execution-model.md` reads the verification-time
> restore, not the solve-time image state).

**F3 — oracle framing (entry:147-178).** Heading: "The oracle (`solution/solve.sh`, captured; tier C —
pattern text extracted, script not run)". Body: "one offline application of the captured function to the
pattern text the lane extracted; it is not the maintainers' oracle-passes check, not a solvability or
instruction-consistency verdict, and no submission was involved."

**F4 — report, don't adjudicate (entry:177-178).**

> the extracted pattern admits two-digit leading-zero octets (`01.`), while `instruction.md:4` asks for
> none; the same pattern is not a graded artefact here. Which of the two the maintainers intend is
> theirs to resolve; this entry records the difference only. (Routed out, not absorbed.)

**F5 — Negative-space additions (entry `## Negative space`).** Append four refusals the draft lacks:

> … nor **regex or log-parsing correctness**: no case here establishes a correct pattern for real logs,
> that a canonical pattern exists, or that the maintainers' 25-line log represents any real log; nor
> **contamination**: the test file's canary banner and its literal expected dates are the maintainers'
> fixture, the capture exists for digest-pinned re-execution, and this lane's province does not measure
> contamination; nor **task difficulty, quality or gameability**: that a shortcut pattern is accepted by
> this fixture says nothing about how any agent behaves, how hard the task is, or whether the task is
> worth grading; nor **harness fidelity**: the probe runs host Python 3.14.8 (`python3 --version`), while
> `test.sh:18,22` runs the file under `uvx -p 3.13` with `pytest==8.4.1`, so the `invalid-regex` case's
> `re.error` text is interpreter-version dependent.

**F6 — PROVINCE paragraph rewrite (134 words; the draft is 139 of a 140 ceiling).** Full drop-in at
`build/R36CritScope/province-rewrite.txt`. The three substantive deltas: `(lane-authored patterns, not
agent outputs)` after the 24 candidates; `establish regex or log-parsing correctness or which pattern
the instruction demands`; `measure … contamination (the in-test log and its literal dates are the
grader's own fixture)` and `the remaining 87 TB2 tasks` (89 tasks per
`benchmark-verifier-execution-model.md:93`; the draft's "other 88" arithmetic reads as 88 unchanged).

**F7 — README coverage bullet (insertion 2).**

> - **Terminal-Bench 2.0 task grader (second task, same instrument)**: covered at source-code depth and
>   executed offline (round 36, 2026-10-25) — knowledge/tb2-regex-log-grader.md; S108, S109, S110; probe
>   `plans/regex_log_probe.py`, receipt `evidence/round36/regex-log-probe.txt`. A second instance of the
>   round-35 ground, not new ground and not an axis move: what its one test asserts (exact equality of
>   `re.findall(pattern, log_text, re.MULTILINE)` against a literal nine-date list over a fixed 25-line
>   in-test log), how `tests/test.sh` turns the pytest exit into `/logs/verifier/reward.txt`, and which
>   `instruction.md` bullets no assertion can decide. Not the remaining 87 TB2 tasks, not task validity,
>   difficulty or quality, not the correctness of any regex or of the grader's literals, not
>   contamination measurement, not runtime execution.

Replace the draft's `Extends the round-35 row from protein-assembly to regex-log` — "extends" is the
(F7) vector that makes two of 89 read as coverage progress.

**F8 — axis naming (claims file + SCORECARD row).** `coverage` is the least-wrong name and the frozen
tie-break stands, but it must carry its sub-row and its arithmetic:

> coverage (lowest, tied; **7 held** by the L0 cap) — `coverage/surfaces`: index parity only
> (knowledge files/index rows 42→43, one coverage bullet, one PROVINCE paragraph); `coverage/constructs`:
> **unchanged**; second working round of the existing `pinned-grader-probe` capability, **no new
> construct claimed**. Instance increment, not breadth: two of TB2's 89 task graders, which is not
> benchmark coverage and carries no quality, validity or difficulty verdict.

And the claims file's `a new edge class for the probe` should be demoted in the same edit: "a new input
class for an existing capability (pattern strings rather than data strings), recorded as a property of
this probe — not a construct claim, since the frozen prior-art rule prices no new construct this round."
Without that demotion the sentence ticks `coverage/constructs` (the row novelty maps to) by assertion.

**F9 — SKILL.md section (`R36SkillDraft.md:57-86`, advice at :78-80).** Delete "read `tests/` before trusting a pass";
replace with "when interpreting a reported pass, check which instruction bullets this fixture can
decide". Append one bound line: "A property of `regex-log` at `2fd12b88`; not a task-validity,
difficulty or quality verdict, and not a statement about any agent's behaviour."

**F10 — capability definition (`SCORECARD.md:562`).** `pinned-grader-probe` is defined over "a frozen
table of synthetic **outputs**". C2's table is of patterns. Amend the cell to "… synthetic grader inputs
(data artefacts or pattern strings) …" and keep its two exclusions verbatim ("Not task certification,
not runtime inside the task image"), so the second task sits inside its own capability instead of
silently outside it.

## 4. Is `coverage` the right axis name?

**Defensible only as `coverage/surfaces` (index parity) + `coverage/constructs` (unchanged).** The
canonical rubric line is `SCORECARD.md:247`: coverage +1 when "every surface the corpus *describes* is
indexed **and** every index row exists on disk (both directions); `PROVINCE.md` enumerates surfaces that
resolve". C2 adds no resolving surface — the TB2 raw URL surface is already enumerated by the round-35
paragraph; regex-log is a path *inside* it. The index 42→43 leg is Q7 bookkeeping, not a coverage move.
Every instrument-shaped round since 25 was scored `novelty → canonical coverage/constructs` with the
score held (`SCORECARD.md:665,757,817,893,954,961`), and round 35's identical claim is
"**7 → 7 held (L0 cap)**". So `coverage (held 7)` is the lane's established convention; the defect is the
unqualified label.

**Would a reader call it quality work on new inputs?** Yes, and the vector is F7's word *extends* plus the
coverage-map heading: "second task … extends the round-35 row from `protein-assembly` to `regex-log`"
reads as progress toward covering 89 TB2 graders, i.e. a breadth/quality judgment about the benchmark —
the one thing this surface cannot support (one fixture, 24 patterns, no model, no harness). With F7+F8,
the same reader gets "one more instance of a capability we already had, on inputs we wrote", which is
what the bytes show.

## 5. Adjacent risk worth a line in the entry (not a scope issue)

W5 requires a fresh run to be byte-equal to the receipt. `corpus/evidence/round36/regex-log-probe.txt:21`
contains `invalid-regex … missing ), unterminated subpattern at position 0`, a CPython `re.error` string;
the counter ran here on Python 3.14.8. The probe directory already holds `__pycache__` for cpython-311
through 314, so the instrument has been run under several interpreters — but only the 3.14 byte stream is
pinned. On another host Python that one line can differ and turn the counter red for a reason that is not
a content change. Cheapest safe wording: name the interpreter in the entry's Negative-space sentence
(F5) and in the receipt's label ("CPython 3.14.8"); do not "repair" the receipt.

## 6. Evidence (every number with its command)

| Fact | Command | Output |
|---|---|---|
| probe executes the captured function | `read plans/regex_log_probe.py:82-95` | `spec_from_file_location` → `mod.Path = lambda _arg: real(p)` → `mod.test_regex_matches_dates()`; `except AssertionError` |
| receipt reproduces byte-for-byte (W5 premise) | `python3 plans/regex_log_probe.py --lane . > /tmp/k36-crit-probe.txt; diff -q … receipt` | exit 0; `BYTE_EQUAL` |
| summary line | `tail -1 corpus/evidence/round36/regex-log-probe.txt` | `cases=24 observed_pass=8 observed_fail=16 mismatches=0` |
| fixture size | AST walk over the capture | `sample_logs 25`, `expected_dates 9` |
| `1134` not in the fixture | `grep -n '1134' test_outputs.py` | exit 1 |
| no Feb-29 in the fixture | `grep -n '02-29' test_outputs.py` | exit 1 |
| line numbers of located quotes | `grep -n 'def test_…\|regex_file = Path\|re.findall\|assert matches'` | `8, 21, 87, 90` |
| `test.sh` mapping lines | `grep -n 'uvx\|pytest --ctrf\|if \[\|echo [01] >'` | `18, 22, 25, 26, 28` |
| probe reads no network | `grep -n '^import\|^from' plans/regex_log_probe.py` | `argparse, hashlib, importlib.util, pathlib, sys, tempfile` |
| host interpreter | `python3 --version` | `Python 3.14.8` |
| TB2 task count (for "87") | `grep -n '89 \`tests/test.sh\`' corpus/knowledge/benchmark-verifier-execution-model.md` | `:93 … of its 89 \`tests/test.sh\` files` |
| canonical coverage rubric | `read SCORECARD.md:247` | the two-direction index/enumeration line quoted in §4 |
| r35 identical claim scored held | `read SCORECARD.md` round-35 section | `**7 → 7 held** (L0 cap); frozen predicate met` |

No tool installed or upgraded. No fixture clone needed (all reads were path-scoped, no git/index touch).

## 7. Limits of this review

- I judged wording against the drafts as of this seat's read, not the landed bytes; the L1 owns
  integration and may re-cut every string.
- I did not run either counter for a score (C1/C2 scoring is the frozen counters' job) and I make no
  finding on C2's predicate; W5's premise was checked only as a probe re-run.
- I did not test a second interpreter, so the CPython-dependence in §5 is inferred from the
  `re.error` text and the `__pycache__` set, not demonstrated on 3.13.
- I did not adjudicate whether Amendment 1 (pre-scoring instrument repair) is legitimate; that is the
  open L0 question the claims file names.

VERDICT: scope-inside-10-wording-fixes
