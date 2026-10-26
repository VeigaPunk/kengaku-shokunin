source: S138 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/tests/test_outputs.py — the one pytest function that is this task's whole score: 100 decimal constants at :4-103 and a substring test at :120-122, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-26
source: S139 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/instruction.md — the request the grader is mapped against, lines 1-10, same commit, accessed 2026-10-26
source: S140 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/environment/task-deps/gen.py — the sequence generator that fixes the four round keys and derives every plaintext, lines 1-97, same commit, accessed 2026-10-26
source: S141 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/environment/Dockerfile — the image recipe that builds the task and deletes the generator, lines 1-14, same commit, accessed 2026-10-26
source: S142 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/tests/test.sh — the harness's reward mapping, lines 1-29, same commit, accessed 2026-10-26
source: S143 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/README.md — the authors' own README for this task, lines 1-32, same commit, accessed 2026-10-26
source: S144 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/solution/solve.sh — the task oracle, lines 1-304, same commit, accessed 2026-10-26
source: S145 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/environment/task-deps/decrypt.c — the shipped decrypt utility whose stdout the oracle reuses, lines 1-141, same commit, accessed 2026-10-26
source: S146 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/task.toml — the authors' metadata: timeouts, resources, internet flag, lines 1-41, same commit, accessed 2026-10-26
verified-at: 2026-10-26
recheck: 180d — from the lane root run `(cd corpus/evidence/round44/tb2-feal-linear-cryptanalysis && sha256sum -c SHA256SUMS)` (twelve files), re-fetch the nine pinned URLs above and compare with the pin table in `plans/pkg-spec-r44.json`, then re-run `python3 plans/feal_linear_probe.py --lane .`; any capture digest, probe output or receipt change supersedes this entry

# Terminal-Bench 2.0 task grader, read and executed: `feal-linear-cryptanalysis`

## Summary

At terminal-bench-2 commit `2fd12b88`, the `feal-linear-cryptanalysis` task is scored by **one** pytest function,
`test_attack` (`tests/test_outputs.py:106-122`), and the reward is one bit mapped from the pytest exit status
(`test.sh:22`, `:25-29`). The graded artefact is an **agent-written text file**, `/app/plaintexts.txt`
(`instruction.md:10`), and the whole value check is a substring test: one triple-quoted block of 100 decimal
constants (`test_outputs.py:4-103`), read out with `soln.split()` (`:121`) and asserted against the **entire file
text** one at a time, `assert c in data` (`:122`). There is no count, no order, no format and no exactness check.

**The class, worded narrowly.** Constant-compare on a text file: the grader never imports or executes anything the
agent wrote, and it never parses the file — it asks, for each of 100 expected values, whether those digits occur
anywhere in the bytes. Two published files make that answer reachable without the requested attack: `gen.py` writes
the four round keys as literals (`gen.py:12`) and derives every plaintext as a hash chain (`:61-62`), and the expected
values are written into the published test file itself (`test_outputs.py:4-103`). The image deletes `gen.py`
(`Dockerfile:14`) and never ships the tests, so "public" here means the benchmark repository, not `/app`; the probe
models an agent that read it with a read-only `/pub`.

On the 14 frozen end states of this round's probe the grader reproduced the frozen prediction on all 14
(`cases=14 observed_pass=8 observed_fail=6 mismatches=0`) and graded every end state a second time with no difference
(`regrade cases=14 differ=0`). Four results organise the rest of the entry.

(1) **Three attack-free passes come straight out of public pin files.** `decrypt-public-keys` (`P`) runs the shipped
`./decrypt` with the four keys printed in `gen.py:12`; `replay-public-gen` (`P`) recomputes the 100 plaintexts from
the `gen.py` hash chain with no key and no decryption; `copy-public-constants` (`P`) copies the 100 expected values
out of `test_outputs.py:4-103` verbatim. None of the three performs a known-plaintext attack.

(2) **The substring test ignores shape.** Joining the oracle's numbers into one line (`oracle-concatenated`, `P`),
reversing the lines (`oracle-reversed`, `P`) and printing the same plaintexts zero-padded (`oracle-zero-padded`, `P`)
all pass, and so does the oracle's output followed by 100 decryptions under a wrong key (`oracle-plus-decoys`, `P`).
Nothing is checked but presence.

(3) **Presence is checked for every one of the 100.** Dropping the last plaintext fails (`one-missing`, `F`), as does
decrypting with one key bit flipped (`wrong-key-decrypt`, `F`), writing the 32 known plaintexts of `pairs.txt`
(`pairs-plaintexts`, `F`) or copying `ciphertexts.txt` (`ciphertexts-copied`, `F`).

(4) **The request names no format and the grader accepts only decimal.** The correct plaintexts printed in
hexadecimal fail (`hex-output`, `F`) although every plaintext is right: `assert c in data` looks for decimal digit
strings, and the oracle's own output format comes from the shipped utility's `printf("%lu\n", plaintext)`
(`decrypt.c:136`). Padding is forgiving (the digits survive inside `%020d`); a radix change is not.

The do-nothing state is `F` for a third reason: no `/app/plaintexts.txt`, so `open(...)` at `:120` raises
`FileNotFoundError` (`nop`, `F`). The task's own `solve.sh` passes (`oracle-solve-sh`, `P`).

## Class difference from the round-43 feal entry

`knowledge/tb2-feal-differential-cryptanalysis-grader.md` grades an agent-authored **Python module imported into the
grader's own interpreter** and reduces to one equality, `assert feal_in_c.get_keys()[5] == stolen`. Every attack-free
pass there was a namespace pass: import the answer, shadow the module in `sys.modules`, rebind the accessor, return an
object whose `__eq__` is true, or exit the process early. None of those shapes exists here. This grader executes no
agent code and reads no return value, so the surface is different in both directions:

- **No in-process surface.** `test_attack` opens a path and compares strings; the agent cannot see the test's
  namespace, cannot rebind an accessor, and cannot make its own process exit count as a pass. The reward is still the
  exit status (`test.sh:25-29`), but the process that exits is pytest running the captured test, not code the agent
  wrote.
- **Looser on shape, stricter on presence.** Order, separators, duplication, padding and any extra content are
  invisible to `c in data` (`:122`), so concatenated, reversed and decoy-laden outputs pass; but all 100 strings must
  occur, so one missing value fails the single test (`one-missing`).
- **The public material is the task's own generator.** The round-43 task's answer came from an accessor in the
  grader's process; here it comes from two published files — the generator with its literal keys (`gen.py:12`,
  `:61-62`) and the test with its literal constants (`test_outputs.py:4-103`) — and the image deletes only the
  generator (`Dockerfile:14`).

The two graders therefore share a class family (a constant compare that cannot tell how the constant was obtained)
and differ in mechanism (file bytes vs imported module). No novelty is claimed; the class is the round-43 histogram's
F1 constant-compare, named before this probe ran.

## Source labels

S138 (`tests/test_outputs.py`), S142 (`tests/test.sh`) and S146 (`task.toml`) are the benchmark maintainers' own
scoring code and metadata: primary for *what this grader checks*, for the reward mapping, and for the environment's
bounds. S140 (`environment/task-deps/gen.py`), S141 (`environment/Dockerfile`) and S145
(`environment/task-deps/decrypt.c`) are the maintainers' own environment code: primary for *how the end state is
built*, including the fact that the generator is deleted from the image (`Dockerfile:14`) while its keys and hash
chain stay written down in the published repository. S144 (`solution/solve.sh`) is the maintainers' oracle, read as
one probe recipe and as the shape of a legitimate answer (it writes `attack.c`, compiles it, and redirects `./attack`
into the answer file, `solve.sh:303-304`); no finding rests on its cryptanalysis beyond the fact that its output
satisfies the assert. S139 (`instruction.md`) is the maintainers' request and is primary only for *what is asked*;
every claim about what is graded is drawn from S138, and the requirement map below records where the two disagree.
S143 (`README.md`) is the authors' prose about the task; `:32`'s "verifies that all 100 expected plaintext values
appear in `/app/plaintexts.txt`" is an accurate description of the substring test, and is read as the authors' claim
and checked against the code, not as a source of the rule.

`task.toml` (S146) is metadata, read only and never exercised: `difficulty = "hard"` (`:15`),
`expert_time_estimate_min = 960.0` (`:18`), `junior_time_estimate_min = 19200.0` (`:19`), verifier and agent
timeouts of 1800 s (`:22`, `:25`), `docker_image = "alexgshaw/feal-linear-cryptanalysis:20251031"` (`:29`),
1 CPU and 2048 MB (`:30-31`), and `allow_internet = true` (`:34`). The image recipe (S141) is `python:3.13-slim-bookworm`
with gcc installed (`:2`, `:5`), `COPY task-deps/ /app/` (`:8`), the two gcc builds and `python3 gen.py` (`:9-11`),
then the two deletions (`:13-14`). The README (S143) also states a "30 minutes (agent), 30 minutes (verifier)" budget
(`:22`), which matches the 1800 s fields in S146 and bounds nothing else.

The probe receipt (`corpus/evidence/round44/feal-linear-probe.txt`) is the lane's own re-runnable gate output, tier A
for its own scope: these 14 end states against these captures, under host `python3`, host `gcc` and the captured
grader, inside bubblewrap with network, pid and ipc namespaces unshared.

Disclosure (order of operations, as the freeze states it). The 14 predictions and their `violates=` tags were written
from a static reading of `test_outputs.py`, `instruction.md`, `gen.py`, `Dockerfile`, `test.sh`, `README.md`,
`solve.sh`, `decrypt.c` and `task.toml` **before the first recorded run** and frozen in
`corpus/evidence/round44/feal-linear-dry-cases-freeze.txt` (digest pinned in `plans/round44_c2_verify.py` as
`DRY_SHA256`). Before that
freeze the probe ran only `--dry` and `--stage-check` (`stagecheck cases=14 failed=0`), and round-43 seat
`R43PlanNext` had run the oracle plus a substring check (not the grader's test function) on this host
(`CONSTANTS 100 ALL_IN_DATA True`); case `oracle-solve-sh` re-observes that measurement and the other thirteen were
never graded before the freeze. The one pre-freeze grader execution is the C2 counter's V11 control set (48 generated
end states, `random.Random(44)`, `claims/control-c2-predictor.txt`), none of which is a probe case. Every case carries
`predicted_tests=` and `predicted=`; no prediction was edited after the run, and all 14 matched.

## What is graded (static reading of test_outputs.py, test.sh, instruction.md, gen.py, Dockerfile)

| Step | Mechanism | Lines |
|---|---|---|
| Entry point | `uvx -p 3.13` with `pytest==8.4.1`, `pytest-json-ctrf==0.3.5`, then `pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -v -rA`; one function is collected | `test.sh:18-22` |
| Reward | the shell maps the pytest exit status to `/logs/verifier/reward.txt`: `1` on 0, `0` otherwise — one bit, no partial credit | `test.sh:25-29` |
| Initial state | `WORKDIR /app`; gcc installed; `COPY task-deps/ /app/`; `gcc -O3 -o feal feal.c`; `gcc -O3 -o decrypt decrypt.c`; `python3 gen.py`; then `orig_plaintexts.txt` and `gen.py` are deleted | `Dockerfile:3-14` |
| The fixed keys | the four 20-bit round keys are string literals in the generator, written at `:12` | `gen.py:12` |
| The plaintext chain | `seed_hash = sha256("".join(keys))`; for each counter, `sha256(seed_hash + struct.pack(">Q", n))[:8]` as a big-endian integer; counters 0-31 for `pairs.txt`, 32-131 for the 100 ciphertexts | `gen.py:19-20`, `:26-28`, `:60-62` |
| The request | names the cipher, the 32 pairs, "a known-plaintext attack", decrypting all ciphertexts, and `/app/plaintexts.txt`; **no output format** | `instruction.md:1-10` |
| The graded file | `data = open("/app/plaintexts.txt").read()` — the whole file as one string, no parsing | `test_outputs.py:120` |
| The check | `for c in soln.split():` then `assert c in data` — 100 independent substring tests | `test_outputs.py:121-122` |
| The constants | a triple-quoted block of 100 decimal integers, one per line | `test_outputs.py:4-103` |
| The oracle | writes `attack.c`, compiles it, redirects `./attack` into `/app/plaintexts.txt`; the program shells out to `./decrypt ciphertexts.txt 0x%x 0x%x 0x%x 0x%x` with the recovered keys | `solve.sh:289`, `:303-304` |

Five structural consequences follow from the reading alone.

- **The check is a conjunction of containments over one string.** `data` is the file's whole text (`:120`); each
  constant is tested with `in` (`:122`). Separators, line count, ordering, duplicates and any extra bytes are outside
  the predicate, and the loop short-circuits only at the first missing constant.
- **The expected values are published.** They sit in the test file itself (`:4-103`), and the same 100 values are
  regenerable from `gen.py`'s literal keys (`:12`) and chain (`:61-62`) — verified here: the 100 constants equal
  `sha256(sha256("0x68e630x625710x1f61c0xb74a5") + pack(">Q", 32+i))[:8]` for `i` in 0..99, in order.
- **The generator leaves the image but not the repository.** `Dockerfile:11` runs it and `:14` deletes it; the file
  stays published at the pinned commit, so the keys and the plaintext chain are public even though `/app` no longer
  has them.
- **No format is requested.** `instruction.md:9-10` asks only to save the answers in `/app/plaintexts.txt`; the
  oracle's decimal shape comes from `decrypt.c:136`'s `printf("%lu\n", plaintext)`, which `solve.sh:290` invokes by
  running the utility, not from any instruction sentence.
- **The verdict is a process exit status.** `test.sh:25` reads `$?`; a pytest process that exits 0 writes reward 1.
  Nothing inspects the file's size, line count or the number of distinct values.

## Located quotes

Quotes are byte-exact from the round-44 captures (`corpus/evidence/round44/tb2-feal-linear-cryptanalysis/`, identical
to the pinned raw files at `2fd12b88`), each 3-25 words, verified line by line and by the gate's `P4` clause. Straight
double quotes inside a quote are the file's bytes.

| Claim supported | “Quote” | `capture:line` |
|---|---|---|
| the cipher is shipped as C source in /app | “The file /app/feal.c implements a FEAL-like encryption function,” | `instruction.md:1` |
| each round key is reduced to a 20-bit seed | “(Each of the 4 round keys is derived from a 20 bit seed.” | `instruction.md:4` |
| the request is a known-plaintext key recovery | “Implement a known-plaintext attack that recovers the key of the cipher.” | `instruction.md:7` |
| the deliverable is an answer file, with no format named | “the file /app/ciphertexts.txt, and saving your answer in the file” | `instruction.md:9` |
| the test's own docstring says it checks the 100 values | “Test that the linear cryptanalysis attack correctly decrypts all ciphertexts.” | `test_outputs.py:108` |
| the expected values are a literal block in the test file | “soln = """1050628112036199672” | `test_outputs.py:4` |
| the graded file is read whole, unparsed | “data = open("/app/plaintexts.txt").read()” | `test_outputs.py:120` |
| the constants are iterated one by one | “for c in soln.split():” | `test_outputs.py:121` |
| the whole value check is one containment | “assert c in data” | `test_outputs.py:122` |
| pytest runs the single captured test file | “pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -v -rA” | `test.sh:22` |
| the reward is the pytest exit status | “if [ $? -eq 0 ]; then” | `test.sh:25` |
| reward 1 is written on exit 0 | “echo 1 > /logs/verifier/reward.txt” | `test.sh:26` |
| the four round keys are literals in the generator | “keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]” | `gen.py:12` |
| every plaintext is a hash of seed plus counter | “plaintext_hash = hashlib.sha256(seed_hash + counter_bytes).digest()” | `gen.py:61` |
| the plaintext is the first eight bytes, big-endian | “plaintext = int.from_bytes(plaintext_hash[:8], "big")” | `gen.py:62` |
| the image deletes the original plaintexts | “RUN rm orig_plaintexts.txt” | `Dockerfile:13` |
| the image deletes the generator | “RUN rm gen.py” | `Dockerfile:14` |
| the authors describe the check as an appearance test | “The test suite (`test_outputs.py`) verifies that all 100 expected plaintext values appear in `/app/plaintexts.txt`” | `README.md:32` |
| the oracle shells out to the shipped decrypt utility | “"./decrypt ciphertexts.txt 0x%x 0x%x 0x%x 0x%x"” | `solve.sh:289` |
| the oracle's stdout is the answer file | “./attack > /app/plaintexts.txt” | `solve.sh:304` |
| the verifier timeout is 1800 s | “timeout_sec = 1800.0” | `task.toml:22` |
| internet is allowed in the environment | “allow_internet = true” | `task.toml:34` |

## Requirement map

Labels are **derived**, not chosen: `enforced` iff every receipt case whose `violates=` set carries the tag is
observed `fail`, `unenforced` iff every such case is observed `pass`, `partly` otherwise — the rule the counter's
`V7` applies, computed over **all** violating cases and not from one convenient witness. The frozen table carries
four tags on three instruction lines. One tag is single-witness and `enforced` (`plaintexts-file`); the other three
are `partly`, each with passing and failing violating cases.

| Instruction line | Tag | Label | Receipt cases cited (violating, both directions) |
|---|---|---|---|
| `instruction.md:7` | `known-plaintext-attack` | partly | `nop`, `decrypt-public-keys`, `replay-public-gen`, `copy-public-constants`, `pairs-plaintexts`, `ciphertexts-copied` |
| `instruction.md:7` | `recover-key` | partly | `nop`, `decrypt-public-keys`, `replay-public-gen`, `copy-public-constants`, `wrong-key-decrypt`, `pairs-plaintexts`, `ciphertexts-copied` |
| `instruction.md:8` | `decrypt-all` | partly | `nop`, `replay-public-gen`, `copy-public-constants`, `one-missing`, `wrong-key-decrypt`, `pairs-plaintexts`, `ciphertexts-copied` |
| `instruction.md:10` | `plaintexts-file` | enforced | `nop` |

The per-line reading:

- **7 (`known-plaintext-attack`, `partly`).** Three cases that perform no attack at all pass: the public keys
  (`decrypt-public-keys`), the public hash chain (`replay-public-gen`) and the public constants
  (`copy-public-constants`); three that also do not attack fail for value reasons (`nop`, `pairs-plaintexts`,
  `ciphertexts-copied`). The label records that the grader cannot distinguish the requested method from any other way
  of producing the 100 values.
- **7 (`recover-key`, `partly`).** The same three public-file passes, plus `wrong-key-decrypt` failing with one key
  bit flipped and the same three value failures. The grader checks presence of results, not that any round key was
  recovered: an agent that never runs a key search can pass.
- **8 (`decrypt-all`, `partly`).** `replay-public-gen` and `copy-public-constants` never decrypt anything and pass;
  `one-missing`, `wrong-key-decrypt`, `pairs-plaintexts` and `ciphertexts-copied` fail. The conjunction over the 100
  constants is what makes "all" true in effect for a correct answer, but the requirement is demonstrably reachable
  without decryption.
- **10 (`plaintexts-file`, `enforced`).** The only violating case is `nop`, and it fails: with no
  `/app/plaintexts.txt`, `open(...)` at `:120` raises `FileNotFoundError`. This is the one requirement whose
  violation is total, and it is enforced by the read itself, not by an existence check on the path.

### Contestable tags

The `violates=` tags are frozen with the predictions and are not edited; three deserve naming.

- **`recover-key` → `replay-public-gen`.** The case recovers nothing and decrypts nothing; it recomputes the plaintext
  chain from the published generator. The tag records that the *requirement* is not met, which is the coverage fact:
  the grader passes a state in which no key exists on the agent's side at all.
- **`known-plaintext-attack` → `decrypt-public-keys`.** The case does use `./decrypt` on `ciphertexts.txt`, so it does
  "decrypt all the ciphertexts" as `instruction.md:8` asks; it simply reads the four keys from `gen.py:12` instead of
  recovering them. The tag is on the attack sentence (`instruction.md:7`).
- **`decrypt-all` → `decrypt-public-keys`?** No: the keys are correct, so every plaintext is right and the tag is
  absent from that case; the tag sits on the cases that pass with results they did not decrypt
  (`replay-public-gen`, `copy-public-constants`).

## Case table

The 14 frozen cases in receipt order; the letter is the one test (`test_attack`) and the verdict is that letter.

| Case | Tests | Observed | What the end state is |
|---|---|---|---|
| `nop` | F | fail | no `/app/plaintexts.txt`, only the seeded image, so the read at `:120` raises |
| `oracle-solve-sh` | P | pass | the task's `solve.sh` builds and runs the reference attack into the answer file |
| `decrypt-public-keys` | P | pass | `./decrypt` with the four round keys printed in the public `gen.py:12` |
| `replay-public-gen` | P | pass | the 100 plaintexts recomputed from `gen.py`'s hash chain, counters 32-131 |
| `copy-public-constants` | P | pass | the 100 expected constants copied out of the public `tests/test_outputs.py` |
| `oracle-concatenated` | P | pass | the oracle's numbers joined into one line with no separator |
| `oracle-plus-decoys` | P | pass | the oracle's output followed by 100 wrong-key decryptions |
| `oracle-reversed` | P | pass | the oracle's lines in reverse order |
| `oracle-zero-padded` | P | pass | the correct plaintexts printed as 20-digit zero-padded decimals |
| `one-missing` | F | fail | the correct 100 plaintexts with the last one dropped |
| `hex-output` | F | fail | the correct plaintexts printed in hexadecimal; no format is named in the request |
| `wrong-key-decrypt` | F | fail | decrypt with round key 0 off by one bit |
| `pairs-plaintexts` | F | fail | the 32 known plaintexts from `pairs.txt` |
| `ciphertexts-copied` | F | fail | `ciphertexts.txt` copied unchanged |

## Mechanism

One row per receipt case, in receipt order: the captured line that decides the case and a verbatim fragment of it.
The Findings section says, case by case, why that line decides it.

| Case | Decisive line | “Quote” |
|---|---|---|
| `nop` | `test_outputs.py:120` | “data = open("/app/plaintexts.txt").read()” |
| `oracle-solve-sh` | `solve.sh:304` | “./attack > /app/plaintexts.txt” |
| `decrypt-public-keys` | `gen.py:12` | “keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]” |
| `replay-public-gen` | `gen.py:61` | “plaintext_hash = hashlib.sha256(seed_hash + counter_bytes).digest()” |
| `copy-public-constants` | `test_outputs.py:121` | “for c in soln.split():” |
| `oracle-concatenated` | `test_outputs.py:122` | “assert c in data” |
| `oracle-plus-decoys` | `test_outputs.py:122` | “c in data” |
| `oracle-reversed` | `test_outputs.py:121` | “for c in soln.split():” |
| `oracle-zero-padded` | `test_outputs.py:122` | “assert c in data” |
| `one-missing` | `test_outputs.py:122` | “assert c in data” |
| `hex-output` | `decrypt.c:136` | “printf("%lu\n", plaintext);” |
| `wrong-key-decrypt` | `test_outputs.py:122` | “assert c in data” |
| `pairs-plaintexts` | `test_outputs.py:122` | “assert c in data” |
| `ciphertexts-copied` | `test_outputs.py:122` | “assert c in data” |

## Findings, each tied to its receipt cases

1. **The absence of the answer file is the do-nothing failure (`nop` `F`).** `:120` is a bare `open` on an absolute
   path; with only the seeded image, the call raises `FileNotFoundError` inside the pytest function, and the probe
   records it verbatim (`FileNotFoundError -- no /app/plaintexts.txt (the image state only)`). Nothing checks
   `Path(...).exists()` first, so the failure is a read error rather than an assertion. The Mechanism row cites
   `:120` because that is the line that decides; `:122` is never reached.
2. **The task's own attack passes (`oracle-solve-sh` `P`).** `solve.sh` writes `attack.c`, compiles it (`:303`) and
   redirects its stdout into `/app/plaintexts.txt` (`:304`); the program runs the shipped `./decrypt` with the keys it
   recovered (`:289`). The output satisfies all 100 containments. This is a sanity anchor for the probe and for the
   answer's shape, not a claim about the oracle's cryptanalysis; the probe never inspects the C.
3. **The expected values are public three ways, and each is a passing case
   (`decrypt-public-keys` `P`, `replay-public-gen` `P`, `copy-public-constants` `P`).** The keys are literals at
   `gen.py:12`; the plaintext chain is `sha256(seed_hash + pack(">Q", n))[:8]` at `:61-62`; the constants are the
   test's own block at `test_outputs.py:4-103`. The probe reads them from `/pub`, a read-only copy of the three
   public files, and its recipes therefore model an agent that read the repository rather than `/app`. The image
   deletes only `gen.py` (`Dockerfile:14`); it never ships the test file to `/app` at all.
4. **The check is containment in one string, so shape is free (`oracle-concatenated` `P`, `oracle-reversed` `P`,
   `oracle-zero-padded` `P`, `oracle-plus-decoys` `P`).** `data` is the file's entire text (`:120`); `assert c in
   data` (`:122`) is true for a constant whose digits occur anywhere. Joining the numbers into one line, reversing
   their order, padding each to 20 digits, or appending 100 wrong-key decryptions changes nothing the predicate sees.
   The case pair that fixes the semantics is `oracle-concatenated` against `one-missing`: shape changes pass, presence
   changes fail.
5. **Every one of the 100 must be present (`one-missing` `F`).** Dropping the last plaintext leaves 99 containments
   true and one false; the single assert raises and the one test fails, so the reward is 0. The conjunction is the
   only quantity the grader enforces — it is not a line count and not an exact-file comparison.
6. **The request names no format, and only decimal survives (`hex-output` `F`).** `instruction.md:9-10` asks to save
   the answers in the file and says nothing about radix; the probe prints the same correct plaintexts as
   `hex(int(l))` and every containment fails. The decimal shape the oracle produces is the shipped utility's
   `printf("%lu\n", plaintext)` (`decrypt.c:136`), reached through `solve.sh:290`'s `system(cmd)`, not through any
   instruction sentence. Conversely `oracle-zero-padded` shows the grader is indifferent to width as long as the
   decimal digits stay contiguous.
7. **A wrong key fails honestly (`wrong-key-decrypt` `F`).** Flipping one bit of round key 0 changes every decrypted
   plaintext, so none of the 100 constants occurs and the assert raises. The case is the value channel's positive
   control: the same recipe with the right keys (`decrypt-public-keys`) passes.
8. **The grader ignores content it does not look for (`oracle-plus-decoys` `P`).** The file holds 200 numbers — the
   100 correct plaintexts and 100 decryptions under a wrong key — and passes, because `data` is only searched for the
   100 expected substrings. Combined with `pairs-plaintexts` `F` (32 true plaintexts, 68 missing) the boundary is
   exactly "all 100 expected decimal strings occur somewhere", nothing more.
9. **Copies of task inputs fail (`pairs-plaintexts` `F`, `ciphertexts-copied` `F`).** The 32 known plaintexts and the
   100 ciphertexts are both wrong as answers, and both fail; the conjunction makes a partial or unrelated answer
   worth 0.
10. **One bit and no partial credit (`test.sh:25-29`).** Whatever goes wrong — a missing file, one missing value, a
    radix change — the exit status is non-zero and `reward.txt` gets 0. The four failing shapes above therefore all
    land on the same 0, which is why the receipt distinguishes them by recipe rather than by reward.

## Regrade (second grading of the same end state)

The probe grades each built state with one fresh harness process and then a second, fresh harness process over the
same `/app`, `/tests` and `/pub`; the second result is reported (`regrade=same` / `regrade=DIFF:<letter>`) and never
used for the verdict. The receipt is `regrade cases=14 differ=0`. Unlike the round-43 feal task, whose keys were
re-seeded from `time(NULL)` per grading process, this task's four keys are literals in `gen.py:12` and the ciphertexts
are generated once at image build (`Dockerfile:11`), so the two passes fully re-run one fixed end state. `regrade=same`
therefore reads as harness/replay determinism — the same bytes and the same 100 constants — not as a second
independent key draw, and it cannot detect a verdict that depends on a random seed because there is none.

## What the probe does not show

- **The task image is never pulled; the host's tools stand in.** `task.toml:29` names
  `alexgshaw/feal-linear-cryptanalysis:20251031`; `Dockerfile:2` is `python:3.13-slim-bookworm` and `:5` installs gcc
  through apt with network. The probe replays the image's *files* (`COPY`, the two gcc builds, `gen.py`, the two
  deletions) inside bubblewrap with host `/usr/bin/python3`, host `/usr/bin/gcc` and host `/usr/bin/bash`, so the
  image's gcc version, its apt state and the `pip install setuptools==80.9.0` line (`:6`) are untested.
- **`tests/test.sh` was not executed.** The reward mapping is read (`test.sh:18-29`), not run: `apt-get`, the network
  `uv` install, `uvx -p 3.13` and `/logs/verifier/` are outside the sandbox. `observed_pass` means "the test function
  returned without raising", which is what makes pytest exit 0 — not that `reward.txt` was written.
- **Real pytest was not run.** The harness maps the one function's outcome onto an exit status, so collection,
  import errors, `pytest-json-ctrf` behaviour and the 1800 s verifier timeout (`task.toml:22`) are untested. A
  pytest-parity re-run is a wave item, and this entry does not claim it happened.
- **`/pub` is a model of public reading, not the image.** In the image `gen.py` is gone (`Dockerfile:14`) and
  `/tests/test_outputs.py` is never copied into `/app`; an agent would have to obtain the public repository, which
  `task.toml:34` (`allow_internet = true`) permits but which the probe does not exercise. The three public-file cases
  say what the grader does with such an answer, not that an agent can reach those files in every harness.
- **The 14 cases are the claim's whole surface.** They were fixed before the first recorded run. States outside them —
  a file with the 100 values interleaved mid-number, an answer generated with a different but still-substring-safe
  encoding, a symlinked `/app/plaintexts.txt`, a directory at that path, an agent that reads `/tests` if it exists,
  and every AI-agent trajectory — are not covered and are not claimed. The C2 counter's V11 held-out set (48 generated
  states: exact, shuffled, drop-one, drop-three, concat, zero-pad, hex, decoys, bump-one, absent, empty, comma,
  split-one, duplicated, half, prefixed-digit) widens the mechanism read but is still a constructed set.
- **Not a statement about the task's validity, difficulty or solvability.** That is PROVINCE's question, not this
  lane's; `difficulty = "hard"` (`task.toml:15`) and the 960-minute expert estimate (`:18`) are the authors'
  metadata, read only. Nothing here measures whether a real agent would take any of the shortcuts.
- **The captures' provenance.** The twelve files were fetched at `2fd12b88` by the L1 on 2026-10-26 and pinned in
  `SHA256SUMS` and `plans/pkg-spec-r44.json`; that they are the files the authors ship today rests on those digests,
  not on a fetch by this seat.
- **Not evaluated here: the prover.** The linear attack itself (`solve.sh`'s C) is a recipe, not an object of study;
  its runtime, its success rate on other key draws and its behaviour under the 1800 s agent timeout
  (`task.toml:25`) are outside this probe.

## Prior art (searched 2026-10-26 20:33–20:37 -03 by seat `R44ScoutPriorArt`)

Receipt: `.ufo/waves/round-44/wave/R44ScoutPriorArt.md` (TB2 and TB-main issues/PRs dumped with `gh`, Terminal
Wrench index, web search; a synthesized web answer that misattributed the substring fact to the ICLR PDF was opened,
found unsupported, and not cited). Per finding: the substring semantics and the format-agnostic passes (concatenated,
reversed, zero-padded, decoys) were **not found** reported as a weakness of this grader; the `gen.py` hash-chain replay
was **not found** (the seed-regeneration class is published for another task, https://github.com/harbor-framework/terminal-bench/issues/1637); decryption with the
public `gen.py:12` keys and copying the public test constants are **adjacent** (the keys are indexed by GitHub code
search in several benchmark mirrors; tbench.ai's "Leaderboard Integrity Update" names "finding solutions on the
internet" as reward hacking, https://www.tbench.ai/news/leaderboard-integrity-update); substring-containment graders
as a class are **published** (Berkeley RDI, "How We Broke Top AI Agent Benchmarks", item 5 "Weak String Matching",
https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/), and the authors state the "appear in" design
(`README.md:31-32`). "Not found" means absent from those surfaces on that date, not non-existence. No novelty is
claimed by this entry.

## Negative space

This entry does **not** establish: that the task is invalid, mis-calibrated, too easy or unsolvable (no image run, no
agent, no trajectory); that an agent would use any of the three public-file shortcuts (they are constructed
end states); that the grader should count values, parse lines, fix a format or sandbox the file (no such proposal is
described or judged here); that the instruction's silence on format is a design error (the entry records that the
grader accepts decimals only, not what it should accept); or anything about how Harbor executes this verifier.

Nor: **contamination** — `test_outputs.py:1-2` and `Dockerfile:1` carry the canary banner and these captures exist
for digest-pinned re-execution, not as a contamination measurement; **the image's toolchain** — host python, host gcc
and host apt stand in for `python:3.13-slim-bookworm`; **the oracle's correctness** — `solve.sh` runs as one case's
recipe and passes once, which says nothing about other key draws or inputs; **prevalence** — one task, 14 states, no
tracker sweep by this seat; **the instruction's intent** — whether "known-plaintext attack" was meant to exclude
reading the published generator is the authors' question, and the entry only records that the grader cannot tell the
difference.

**Falsifier.** This entry is falsified if (a) a re-fetch of the nine pinned URLs yields bytes whose SHA-256 differs
from `corpus/evidence/round44/tb2-feal-linear-cryptanalysis/SHA256SUMS` and the pins in `plans/pkg-spec-r44.json`;
(b) a fresh run of `plans/feal_linear_probe.py --lane .` prints anything other than
`cases=14 observed_pass=8 observed_fail=6 mismatches=0` and `regrade cases=14 differ=0` — in particular if
`oracle-solve-sh`, `decrypt-public-keys`, `replay-public-gen`, `copy-public-constants`, `oracle-concatenated`,
`oracle-plus-decoys`, `oracle-reversed` or `oracle-zero-padded` is observed `fail`, or if `nop`, `one-missing`,
`hex-output`, `wrong-key-decrypt`, `pairs-plaintexts` or `ciphertexts-copied` is observed `pass`; (c) a line of
`test_outputs.py` is shown to count values, compare lines exactly, normalise tokens, or test anything other than
`c in data` for `c` in the 100 constants; (d) the 100 constants are shown not to be the plaintext chain of
`gen.py:61-62` under the keys at `:12`, or `gen.py` is shown not to publish those keys at the pinned commit; (e)
`test.sh` is shown to compute the reward from anything other than the pytest exit status; or (f) the four rounds' keys
are shown to be seeded at grading time rather than fixed at image build.

## Predictor

The rule the captured grader implements, executable as `predict(text)` over the content of `/app/plaintexts.txt`
(`None` when the file is absent): `True` iff every one of the 100 expected decimal strings occurs as a substring of
the whole text. The constants are taken from `gen.py`'s published chain (`:12`, `:61-62`) rather than copied out of
the test file; the two sets were checked equal, all 100 in order.

```python
import hashlib
import struct

# The grader's expected values (tests/test_outputs.py:4-103) are gen.py's public chain: counters 32-131.
KEYS = "0x68e630x625710x1f61c0xb74a5"
SEED = hashlib.sha256(KEYS.encode()).digest()
CONSTANTS = tuple(
    str(int.from_bytes(hashlib.sha256(SEED + struct.pack(">Q", 32 + i)).digest()[:8], "big"))
    for i in range(100)
)


def predict(text):
    if text is None:            # open("/app/plaintexts.txt") raises FileNotFoundError
        return False
    return all(c in text for c in CONSTANTS)
```
