source: S149 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/tests/test_outputs.py — the two pytest functions that are this task's whole score, lines 1-18, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-26
source: S150 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/instruction.md — the request the requirement map is drawn against, lines 1-9, same commit, accessed 2026-10-26
source: S151 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/environment/setup.sh — the environment build that hides the answer in a fragmented disk image, lines 1-43, same commit, accessed 2026-10-26
source: S152 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/environment/Dockerfile — the base image and the tool set the task expects, lines 1-20, same commit, accessed 2026-10-26
source: S153 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/tests/test.sh — the verifier entry point and the reward mapping, lines 1-29, same commit, accessed 2026-10-26
source: S154 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/README.md — the authors' own account of what the tests check, lines 1-33, same commit, accessed 2026-10-26
source: S155 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/solution/solve.sh — the oracle that carves the image and appends candidate passwords, lines 1-68, same commit, accessed 2026-10-26
source: S156 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/task.toml — the authors' declared image, timeouts and resource envelope, lines 1-41, same commit, accessed 2026-10-26
verified-at: 2026-10-26
recheck: 180d — from the lane root run `(cd corpus/evidence/round45/tb2-password-recovery && sha256sum -c SHA256SUMS)` (green as written), re-fetch the eight pinned URLs above, and re-run `plans/password_recovery_probe.py --lane .`; any digest or receipt change supersedes this entry

# Terminal-Bench 2.0 task grader, read and executed: `password-recovery`

## Summary

At terminal-bench-2 commit `2fd12b88`, `password-recovery` is scored by **two** pytest functions in
`tests/test_outputs.py` (S149): `test_recovery_file_exists` asserts
`Path("/app/recovered_passwords.txt").exists()` (`:9-10`), and `test_password_match` reads that file with
`read_text().strip().split("\n")` (`:14`), asserts `len(guesses) > 0` (`:16`) and asserts
`"8XDP5Q2RT9ZK7VB3BV4WW54" in guesses` (`:18`). `tests/test.sh:18-29` (S153) maps the pytest exit status to
`/logs/verifier/reward.txt`: `1` on 0, `0` otherwise — one bit, no partial credit.

The graded artefact is therefore **an agent-written guess list, checked by exact whole-line membership of one
23-character constant**. That is the eleventh TB2 grader class in this lane's executed sample, and a different
reading from the round-44 exemplar: `db-wal-recovery` compared a JSON export against a table (100 pinned cells,
9 free), while this task compares one line against one literal and pins nothing else — no format, case, order,
count or uniqueness check survives into an assertion. The answer constant is **published twice** in the pinned
repository: in the grader itself (S149 `:18`) and in the environment build (S151 `:25`,
`echo "PASSWORD=8XDP5Q2RT9ZK7VB3BV4WW54" > /app/launchcode.txt`), and the authors' README names it a third time
(S154 `:31`). An agent that reads the public tests — or the setup script, or the README — can write the single
passing line without touching the disk image at all; the task's forensic premise (S150 `:1-2`) is not observed
by any assertion.

The environment (S151) builds `/app/varsea`, a decoy file tree (five `sub-*` directories of random binaries and
timestamped logs), plus a 4 MB disk image at `/app/varsea/disks/sub1/subA/subAlpha/ae3f4c.dat` (`:22`): a
`PASSWORD=…` line is zipped, split 20 bytes into the password (`:30`), and the two fragments are `dd`'d at the
1 MB and 3 MB offsets (`:36-37`) with noise at 2 MB (`:41`); the plaintext and the zip are then deleted (`:43`).
The oracle (S155) finds the image with `find` (`:11`), locates the `8XD` and `W54` fragments with `grep -aob`,
and appends every `first_trimmed+last_trimmed` combination of length 23 to `recovered_passwords.txt` in the
current directory (`:51`, `:63`) — the grader accepts a set of guesses, so the plausible ones ride along with the
right one.

The frozen case table carries 16 cases (`predicted_pass=5`, `predicted_fail=11`), every one of them listed
below; the receipt is `corpus/evidence/round45/password-recovery-probe.txt` (sha256 `587c8b34…`), produced by
`plans/password_recovery_probe.py --lane .`, and it records `cases=16 observed_pass=5 observed_fail=11 mismatches=0`
with `regrade cases=16 differ=0` — every observed verdict equals its frozen prediction, so the third column
below is simultaneously the receipt's `predicted=` and `observed=` value.

This entry extends `knowledge/benchmark-grader-semantics.md` and
`knowledge/benchmark-verifier-execution-model.md` (S100 is the same repository at the same commit) and the ten
earlier TB2 grader entries, the most recent being `tb2-db-wal-recovery-grader.md`. It **narrows** the
`corpus/README.md` §Frontier "Terminal-Bench 2.0's" clause for this one task only: 10 of 89 task graders read at
`2fd12b88` before this round, 11 after admission.

## Source labels

S149-S156 are the benchmark maintainers' own task files at the pin: primary for *what this grader checks*, for
the initial state the environment builds and for the requirement text the map is drawn against, and a self-report
for everything else (the README's `:29-31` list is the authors' description of their own tests, not a reading).
The probe receipt is the lane's own re-runnable gate output, tier A for its own scope: these 16 states against
these captures under host `python3`. The captured `solve.sh` (S155) is read statically for the oracle's shape and
its `echo` line; no finding here rests on the oracle being correct — the case `oracle-solve-sh` is the probe's
recipe, not a correctness claim.

## Case table

One row per frozen case, in receipt order. The third column is the **frozen prediction** — the receipt's own
`predicted=` field, which the receipt's `observed=` field must reproduce (a case whose observed verdict
contradicts its prediction is a defect in the receipt, per the freeze's kill rule). The second column is the
per-test letter pair the frozen table records (`P` pass, `F` fail, `-` not reached).

| Case | Tests | Predicted | End state |
|---|---|---|---|
| `nop` | F- | fail | no `/app/recovered_passwords.txt` — the seeded image state; test 1 fails, `read_text()` is never reached |
| `oracle-solve-sh` | PP | pass | the published `solve.sh` run as the recipe: fragments carved, every length-23 combination appended one per line |
| `constant` | PP | pass | the 23-character answer copied out of the public `tests/test_outputs.py` as one line |
| `constant-crlf` | PP | pass | the public answer on one CRLF-terminated line; `read_text()`'s universal-newline mode eats the carriage return |
| `constant-joined` | PF | fail | the answer concatenated with two decoys on ONE line — the line itself is not the answer |
| `dir-state` | PF | fail | a DIRECTORY at `/app/recovered_passwords.txt`: `exists()` is true, `read_text()` raises |
| `empty-file` | PF | fail | zero bytes: `''.split("\n")` is `['']`, the `len > 0` assert cannot fire, membership decides |
| `wrong-23` | PF | fail | one 23-character uppercase/digit guess, format-conforming, wrong content |
| `prefix-decoy` | PF | fail | a guess satisfying every published constraint (23 chars, `8XD`…`W54`, `[A-Z0-9]`) that is not the password |
| `sub-first` | PF | fail | the first 20 characters of the answer — a truncated read |
| `sub-last` | PF | fail | the last 20 characters of the answer — the tail fragment only |
| `lower23` | PF | fail | the public answer lowercased — case is part of the compared line |
| `decoys-1000` | PP | pass | the answer plus 1000 wrong guesses, shuffled: no count and no uniqueness check |
| `password-eq` | PF | fail | the answer in `launchcode.txt`'s own `PASSWORD=` format — the grader wants the bare value |
| `crlf-line` | PP | pass | the answer on a CRLF line followed by a second guess — universal newlines translate before `split` |
| `under-varsea` | F- | fail | the oracle's work done from inside `/app/varsea`: the guesses land at `/app/varsea/recovered_passwords.txt`, never at the graded path |

## Mechanism

One row per case, citing the line of the capture that decides it (the counter's `DECISIVE` table names the
allowed lines; the quote is verbatim from that line).

| Case | `capture:line` | “Quote” |
|---|---|---|
| `nop` | `tests/test_outputs.py:10` | “Recovery file not found” |
| `oracle-solve-sh` | `solution/solve.sh:11` | “find /app/varsea/disks -type f -name '*.dat'” |
| `constant` | `tests/test_outputs.py:18` | “in guesses, "Password not found"” |
| `constant-crlf` | `tests/test_outputs.py:14` | “guesses = Path("/app/recovered_passwords.txt").read_text().strip().split” |
| `constant-joined` | `tests/test_outputs.py:18` | “assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses” |
| `dir-state` | `tests/test_outputs.py:14` | “guesses = Path("/app/recovered_passwords.txt")” |
| `empty-file` | `tests/test_outputs.py:16` | “assert len(guesses) > 0, "No guesses found"” |
| `wrong-23` | `tests/test_outputs.py:18` | “"8XDP5Q2RT9ZK7VB3BV4WW54" in guesses,” |
| `prefix-decoy` | `tests/test_outputs.py:18` | “8XDP5Q2RT9ZK7VB3BV4WW54" in guesses, "Password” |
| `sub-first` | `tests/test_outputs.py:18` | “assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses,” |
| `sub-last` | `tests/test_outputs.py:18` | “in guesses, "Password not found"” |
| `lower23` | `tests/test_outputs.py:18` | “in guesses, "Password” |
| `decoys-1000` | `tests/test_outputs.py:14` | “guesses = Path("/app/recovered_passwords.txt").read_text()” |
| `password-eq` | `instruction.md:4` | “written in this format: PASSWORD=XXXXXXXXXX” |
| `crlf-line` | `tests/test_outputs.py:14` | “guesses = Path("/app/recovered_passwords.txt").read_text().strip().split("\n")” |
| `under-varsea` | `tests/test_outputs.py:9` | “recovered_pass_path = Path("/app/recovered_passwords.txt")” |

Two mechanism rows need the words the grader does **not** have. `dir-state` fails inside `read_text()` (`:14`),
not at the assertion, because `Path.exists()` is true for a directory; `empty-file` is the one case where the
`len(guesses) > 0` guard (`:16`) cannot fire — `''.strip().split("\n")` is `['']`, so the guard passes and only
the membership assert (`:18`) decides. That dead guard is recorded here as the grader's own defect, not as a
property of the guess list.

## Requirement map

Labels are **derived**, not chosen: `enforced` iff every case whose `violates=` set carries the tag is observed
`fail`, `unenforced` iff every such case is observed `pass`, `partly` otherwise — the rule the counter's `V7`
applies over all violating cases. The frozen table carries nine tags on six instruction lines (`:1`, `:2`,
`:5`, `:6`, `:7`, `:9`). Eight are `enforced`; `forensic` is `partly`, because the four cases that violate it
while passing (`constant`, `constant-crlf`, `decoys-1000`, `crlf-line`) are exactly the leak: a guess list built
by reading the public answer scores full marks.

| Instruction line | Tag | Label | Receipt cases cited (violating) |
|---|---|---|---|
| `instruction.md:1` | `forensic` | partly | `nop`, `constant`, `constant-crlf`, `constant-joined`, `decoys-1000` |
| `instruction.md:2` | `recover` | enforced | `nop`, `dir-state`, `empty-file`, `wrong-23`, `prefix-decoy`, `sub-first` |
| `instruction.md:5` | `len23` | enforced | `sub-first`, `sub-last` |
| `instruction.md:6` | `prefix` | enforced | `wrong-23`, `sub-last`, `lower23` |
| `instruction.md:6` | `suffix` | enforced | `wrong-23`, `sub-first`, `lower23` |
| `instruction.md:7` | `charset` | enforced | `lower23` |
| `instruction.md:9` | `write-file` | enforced | `nop`, `dir-state`, `under-varsea` |
| `instruction.md:9` | `one-per-line` | enforced | `constant-joined` |
| `instruction.md:9` | `one-guess` | enforced | `nop`, `dir-state`, `empty-file`, `under-varsea` |

The per-line reading:

- **1 (perform a digital forensic recovery task).** `partly`: four violating cases pass — `constant`,
  `constant-crlf`, `decoys-1000`, `crlf-line` — and every one of them is a guess list written from the answer
  the public tests publish; eight more violating cases fail. Nothing in the file reads the disk image, the
  decoy tree or `launchcode.txt`: "recovery" is graded only as "the right line is present", and presence is
  achievable by copying (`constant`) or by the oracle's combinatorial `echo` (S155 `:63`).
- **2 (recover the PASSWORD from the deleted file).** `enforced`: all ten violating cases fail, but the
  enforcement is the file-existence and membership asserts, so a state that "recovers" nothing and writes the
  published answer still passes (`constant`); the label measures the failing direction only.
- **5, 6, 7 (length, prefix/suffix, charset).** All `enforced` on the narrow set that violates them: `sub-first`
  and `sub-last` fail on length; `wrong-23` fails although it conforms to `prefix`, `suffix` and `charset` too
  (the tag set follows the probe's reading, and the case is the demonstration that format conformance is
  worthless without the exact constant); `lower23` fails on case, which is the only signal that the comparison
  is byte-exact.
- **9 (write each matching password, one per line, to `/app/recovered_passwords.txt`).** Three tags, three
  `enforced` labels: `nop` and `under-varsea` miss the graded path (a guess file at
  `/app/varsea/recovered_passwords.txt` scores nothing), `dir-state` has a directory there, and
  `constant-joined` puts the answer on a line with decoys — the one case that separates "one per line" from
  "somewhere in the file".

### Contestable tags

The `violates=` sets are frozen with the predictions and are not edited here.

- **`forensic` → the passing cases.** The tag is carried by `constant`, `constant-crlf`, `decoys-1000` and
  `crlf-line`, all of which pass. That is what makes the label `partly`; it is also the finding.
- **`wrong-23` carries `prefix`/`suffix`.** It conforms to both, so the tag reads "the requirement is not what
  failed" — the case fails on `recover` and `forensic` grounds only. Dropping the two tags would not move their
  labels (other failing cases carry them).
- **`one-guess` vs `empty-file`.** `one-guess` is enforced because `empty-file` fails; the mechanism is the dead
  `len > 0` assert, not a "one guess" rule — the grader accepts 1001 guesses (`decoys-1000`, `PP`).

## Located quotes

Byte-exact from the round-45 captures (`corpus/evidence/round45/tb2-password-recovery/`, identical to the pinned
raw files at `2fd12b88`; `sha256sum -c SHA256SUMS` green at draft time), each 3-25 words.

| Claim supported | “Quote” | `capture:line` |
|---|---|---|
| the first test's whole assertion is existence | “assert recovered_pass_path.exists(), "Recovery file not found"” | `tests/test_outputs.py:10` |
| one read, strip, split — the entire parsing | “guesses = Path("/app/recovered_passwords.txt").read_text().strip().split("\n")” | `tests/test_outputs.py:14` |
| the emptiness guard that cannot fire | “assert len(guesses) > 0, "No guesses found"” | `tests/test_outputs.py:16` |
| the only content assertion in the task | “assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses, "Password not found"” | `tests/test_outputs.py:18` |
| the task is framed as forensics | “perform a digital forensic recovery task” | `instruction.md:1` |
| the published plaintext format | “written in this format: PASSWORD=XXXXXXXXXX” | `instruction.md:4` |
| the length constraint is 23 characters | “It is exactly 23 characters long” | `instruction.md:5` |
| the prefix and suffix are published | “It starts with "8XD" and ends with "W54"” | `instruction.md:6` |
| the charset constraint is published | “The password contains only uppercase letters and digits” | `instruction.md:7` |
| the grader is a guess list, not one answer | “Write each matching password you find, one per line” | `instruction.md:9` |
| the oracle appends, never selects | “echo "$combined" >> "$OUTPUT_FILE"” | `solution/solve.sh:63` |
| the answer is written in plaintext by the build | “echo "PASSWORD=8XDP5Q2RT9ZK7VB3BV4WW54" > /app/launchcode.txt” | `environment/setup.sh:25` |
| fragment one lands at the 1 MB offset | “dd if=/app/secret.part.aa of="$IMG_PATH" bs=1M seek=1” | `environment/setup.sh:36` |
| the verifier is pytest under uvx | “pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA” | `tests/test.sh:22` |
| the reward is one bit | “echo 1 > /logs/verifier/reward.txt” | `tests/test.sh:26` |
| the environment runs the build script at image time | “COPY setup.sh /app/” | `environment/Dockerfile:16` |
| the authors name the constant in their own README | “the correct password `8XDP5Q2RT9ZK7VB3BV4WW54` is among the recovered passwords” | `README.md:31` |
| the task name is the declared one | “name = "terminal-bench/password-recovery"” | `task.toml:5` |
| the image is prebuilt and not built by the verifier | “docker_image = "alexgshaw/password-recovery:20251031"” | `task.toml:29` |
| internet is allowed during the run | “allow_internet = true” | `task.toml:34` |

## Findings

1. **A do-nothing agent scores 0 of 2 (`nop`, `F-`).** The initial state has no
   `/app/recovered_passwords.txt`, so the existence test fails (`:10`) and `read_text()` is never reached.
2. **Copying the published answer passes both tests (`constant`, `PP`; `constant-crlf`, `PP`; `crlf-line`,
   `PP`).** The constant is in S149 `:18`, in S151 `:25` and in S154 `:31`; the probe's `constant` case writes
   nothing but that line. The forensic work in S151 (zip, split, `dd` at two offsets) and the oracle's carving
   in S155 are not observed by any assertion.
3. **The grader accepts arbitrary many guesses (`decoys-1000`, `PP`).** One thousand wrong 23-character guesses
   plus the answer, shuffled, still passes: there is no count, order, uniqueness or format check.
4. **Membership is whole-line and byte-exact (`constant-joined`, `PF`; `lower23`, `PF`; `password-eq`, `PF`).**
   The answer joined with decoys on one line, the answer lowercased, and `PASSWORD=<answer>` all fail; the
   comparison is `in` over `split("\n")` of the stripped text (`:14`, `:18`).
5. **Format conformance buys nothing (`wrong-23`, `PF`; `prefix-decoy`, `PF`).** A guess that satisfies every
   published constraint — length 23, `8XD` prefix, `W54` suffix, `[A-Z0-9]` — still fails.
6. **Truncation fails asymmetrically (`sub-first`, `PF`; `sub-last`, `PF`).** Either 20-character substring
   fails: the prefix fragment alone misses the tail, the tail alone misses `8XD`. The oracle's combinatorial
   `echo` covers exactly this uncertainty (S155 `:55-66`), which is why it passes.
7. **A directory at the graded path dies on a non-assert exception (`dir-state`, `PF`).** `exists()` is true
   (`:10`), and `read_text()` on a directory raises `IsADirectoryError`, so the second test errors rather than
   failing an assertion; the receipt records it (`error=IsADirectoryError`). The letter pair is the same (`PF`)
   either way; the mechanism is not.
8. **The emptiness guard is dead (`empty-file`, `PF`).** `''.strip().split("\n")` is `['']`, so `len(guesses) >
   0` (`:16`) holds on a zero-byte file and only the membership assert (`:18`) fails it.
9. **Writing the guesses one directory too deep scores 0 of 2 (`under-varsea`, `F-`).** A file at
   `/app/varsea/recovered_passwords.txt` never reaches the graded path; the first test fails and the second is
   not reached.
10. **The task's own oracle is guess-y, not exact (S155).** `solve.sh` appends every `first_trimmed +
    last_trimmed` combination of length 23 (`:55-66`), so `decoys-1000` is not a pathological state — it is the
    oracle's normal output shape.

## Predictor

The block below is the grader's rule restated: `text` is the full content of `/app/recovered_passwords.txt`
(already newline-translated as `read_text()` would have done), or `None` when the file is absent; `True` means
both test functions pass on that end state. It is the membership reading — one literal, whole-line, after
`strip().split("\n")` — and no other check exists to encode.

```python
def predict(text):
    if text is None:
        return False
    guesses = text.replace("\r\n", "\n").strip().split("\n")
    return "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses
```

The one place this reading must be trusted rather than derived is `read_text()`'s decoding and universal-newline
behaviour; `utf-8` (with a BOM left as `\ufeff` by `Path.read_text()` on the pinned Python) and `\r\n`/`\r`
translation are what the two CRLF cases exercise.

## Negative space

This entry claims a reading of two functions and an executed probe over 16 frozen cases; it would be
**falsified** by any of the following, each re-runnable:

- a re-fetch of S149 at `2fd12b88` whose bytes differ from
  `2dc14fc180734b6fbb0ee00f27c4f866071247b57a2217f579465ff8ed3bfc9e`, or an added assertion in
  `tests/test_outputs.py` that reads the disk image, `launchcode.txt` or the decoy tree;
- a probe receipt whose `observed=` verdict for any case contradicts the frozen `predicted=` value (the freeze's
  own kill rule for C2);
- an end state that passes both tests while writing no line equal to the constant — impossible under the
  captured source, and the exact thing to test if the source is ever re-pinned;
- a re-run of `plans/password_recovery_probe.py --lane .` that is not byte-equal to the receipt, or a
  `sha256sum -c SHA256SUMS` failure in the capture directory.

## What the probe does not show

- **The task image is never pulled; host python3 stands in for the image's uvx python.** S153 installs
  `uv` 0.9.5 and runs `pytest==8.4.1` under `-p 3.13` (`:18-22`); the probe calls the two test functions
  directly under host `python3`. `observed_pass` therefore means "the two functions would not raise", not
  "`/logs/verifier/reward.txt` was written".
- **`tests/test.sh` was read, not run.** `apt-get`, the network install of uv and `/logs/verifier/` are outside
  the execised surface; the reward mapping (`:25-29`) is quoted, not executed.
- **The environment build was read, not run.** S151 and S152 are static captures; the probe synthesises the end
  states instead of building the 4 MB image, so the `dd`/`zip`/`strings` arithmetic (`:25-37`) is quoted as
  intent, not verified by rebuilding.
- **`solve.sh` is one recipe, not a correctness claim.** `oracle-solve-sh` runs the captured script and asserts
  only that the graded line is present; a different correct oracle would pass identically. The script's own
  variables (`WINDOW_AFTER=20`, `PASSWORD_LENGTH=23`) are not checked against the answer.
- **The 16 cases are the claim's whole surface.** States outside them — a symlink at the graded path, a guess
  file with NUL bytes, a UTF-16 encoding, an extremely long guess list, `\r`-only line endings, reward-file
  behaviour — are not covered and are not claimed.
- **Not a statement about the task's validity, difficulty or solvability.** `difficulty = "hard"` (`task.toml:15`)
  and the 100/300-minute estimates (`:18-19`) are the authors' metadata, read only.
