source: S149 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/tests/test_outputs.py — the two pytest functions that are this task's whole score: an existence assert at :9-10 and exact line membership of one embedded constant at :14-18, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-26
source: S150 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/instruction.md — the request the grader is mapped against, lines 1-9, same commit, accessed 2026-10-26
source: S151 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/environment/setup.sh — the image seed that plants the two zip fragments at the 1MB and 3MB offsets, lines 1-43, same commit, accessed 2026-10-26
source: S152 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/environment/Dockerfile — the image recipe that installs the forensic tools and runs the seed, lines 1-20, same commit, accessed 2026-10-26
source: S153 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/tests/test.sh — the harness's reward mapping (pytest exit status), lines 1-29, same commit, accessed 2026-10-26
source: S154 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/README.md — the authors' own README for this task, lines 1-33, same commit, accessed 2026-10-26
source: S155 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/solution/solve.sh — the task oracle that window-scans the image and emits candidate lines, lines 1-68, same commit, accessed 2026-10-26
source: S156 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/task.toml — the authors' metadata: timeouts, image pin, internet flag, lines 1-41, same commit, accessed 2026-10-26
verified-at: 2026-10-26
recheck: 180d — from the lane root run `(cd corpus/evidence/round45/tb2-password-recovery && sha256sum -c SHA256SUMS)` (nine files), re-fetch the eight pinned URLs above and compare with the pin table in `plans/pkg-spec-r45.json`, then re-run `python3 plans/password_recovery_probe.py --lane .`; any capture digest, probe output or receipt change supersedes this entry

# Terminal-Bench 2.0 task grader, read and executed: `password-recovery`

## Summary

`password-recovery` asks the agent to recover a deleted password from fragments hidden inside a 4 MB disk image
and write every guess, one per line, to `/app/recovered_passwords.txt`. Its grader is the second exemplar of the
**F1 constant-compare family** this lane has executed (after `feal-linear-cryptanalysis`, round 44): the score
reduces to an existence check plus exact **line membership** of one hard-coded 23-character constant,
`"8XDP5Q2RT9ZK7VB3BV4WW54" in guesses`, computed over `read_text().strip().split("\n")`. Where round 44's
exemplar checked 100 constants as substrings of a whole file, this checks ONE constant as a WHOLE LINE among
an arbitrary set of guesses — tighter on format (the answer must be its own line), looser on count and
uniqueness (1000 decoys around it still pass). Every measured end state agrees with the frozen prediction:
`cases=16 observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16 differ=0`
(`corpus/evidence/round45/password-recovery-probe.txt`).

## Located quotes

Quotes are byte-exact from the round-45 captures (`corpus/evidence/round45/tb2-password-recovery/`, identical
to the pinned raw files at `2fd12b88`), each 3-25 words, verified line by line and by the gate's `P4` clause.

| Claim supported | “Quote” | `capture:line` |
|---|---|---|
| the task is forensic recovery of a deleted file | “Your task is to recover the PASSWORD from the deleted file.” | `instruction.md:2` |
| the password's printed format is an assignment | “The password in launchcode.txt was written in this format: PASSWORD=XXXXXXXXXX” | `instruction.md:4` |
| the published shape constraints are length, prefix/suffix, charset | “- It starts with "8XD" and ends with "W54"” | `instruction.md:6` |
| guesses go one per line into one file | “Write each matching password you find, one per line, to the file: /app/recovered_passwords.txt” | `instruction.md:9` |
| the first test asserts existence only | “recovered_pass_path = Path("/app/recovered_passwords.txt")” | `test_outputs.py:9` |
| the second test splits the file into guesses by newline | “guesses = Path("/app/recovered_passwords.txt").read_text().strip().split("\n")” | `test_outputs.py:14` |
| the deciding assert is exact membership of one constant | “assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses, "Password not found"” | `test_outputs.py:18` |
| the reward is pytest's exit status | “if [ $? -eq 0 ]; then” | `test.sh:25` |
| reward 1 is written on exit 0 | “echo 1 > /logs/verifier/reward.txt” | `test.sh:26` |
| the image writes the answer then deletes the file | “echo "PASSWORD=8XDP5Q2RT9ZK7VB3BV4WW54" > /app/launchcode.txt” | `setup.sh:25` |
| the zip is split after the PASSWORD= prefix | “split_point=$((offset + 20)) # Split after "PASSWORD=8XdP5"” | `setup.sh:30` |
| the fragments land at the 1MB and 3MB offsets | “dd if=/app/secret.part.aa of="$IMG_PATH" bs=1M seek=1 conv=notrunc status=none” | `setup.sh:36` |
| the oracle window-scans for the first fragment | “OFFSET=$(grep -aob "$FIRST_PARTIAL_PART" "$IMG_PATH" | head -n1 | cut -d: -f1)” | `solve.sh:16` |
| the oracle joins trimmed fragments into 23-char candidates | “if [ ${#combined} -eq $PASSWORD_LENGTH ]; then” | `solve.sh:62` |
| the oracle window-scans around each fragment offset | “dd if="$IMG_PATH" bs=1 skip="$START" count=$WINDOW_SIZE” | `solve.sh:41` |
| the image runs the seed then deletes it | “RUN bash /app/setup.sh \” | `Dockerfile:17` |
| the authors describe the check as existence plus membership | “That the correct password `8XDP5Q2RT9ZK7VB3BV4WW54` is among the recovered passwords” | `README.md:31` |
| the verifier and agent timeouts are 900 s | “timeout_sec = 900.0” | `task.toml:22-25` |
| internet is enabled in the environment | “allow_internet = true” | `task.toml:34` |

## Requirement map

Labels are **derived**, not chosen: `enforced` iff every receipt case whose `violates=` set carries the tag is
observed `fail`, `unenforced` iff every such case is observed `pass`, `partly` otherwise — the rule the counter's
`V7` applies, computed over **all** violating cases. Nine frozen tags on five instruction lines.

| Instruction line | Tag | Label | Receipt cases cited (violating, both directions) |
|---|---|---|---|
| `instruction.md:1` | `forensic` | partly | `nop`, `constant`, `constant-crlf`, `constant-joined`, `empty-file`, `wrong-23`, `prefix-decoy`, `sub-first`, `sub-last`, `lower23`, `decoys-1000`, `password-eq`, `crlf-line` |
| `instruction.md:2` | `recover` | enforced | `nop`, `dir-state`, `empty-file`, `wrong-23`, `prefix-decoy`, `sub-first`, `sub-last`, `lower23`, `password-eq`, `under-varsea` |
| `instruction.md:5` | `len23` | enforced | `sub-first`, `sub-last` |
| `instruction.md:6` | `prefix` | enforced | `wrong-23`, `sub-last`, `lower23` |
| `instruction.md:6` | `suffix` | enforced | `wrong-23`, `sub-first`, `lower23` |
| `instruction.md:7` | `charset` | enforced | `lower23` |
| `instruction.md:9` | `write-file` | enforced | `nop`, `dir-state`, `under-varsea` |
| `instruction.md:9` | `one-per-line` | enforced | `constant-joined` |
| `instruction.md:9` | `one-guess` | enforced | `nop`, `dir-state`, `empty-file`, `under-varsea` |

The per-line reading (the package's SOURCES rows are S149, S150, S151, S152, S153, S154, S155 and S156, all tier A):

- **1 (`forensic`, `partly`).** The task is framed as digital forensics, but the grader cannot tell recovery
  from copying: `constant` (the answer read out of the public `tests/test_outputs.py`), `constant-crlf` and
  `decoys-1000` all pass without touching `/app/varsea`; thirteen forensic-free end states fail for value
  reasons. The requirement is enforced only as far as the answer is present, not how it was obtained.
- **2 (`recover`, `enforced`).** Every violating case fails — but "recover" in the grader's sense is only
  that the constant appears among the guesses; cases that place it by reading public files are tagged
  `forensic`, not `recover` (the tag records that the PASSWORD's content is required, whatever its provenance).
- **5–7 (`len23`, `prefix`, `suffix`, `charset`, `enforced`).** The published format is the oracle's
  search aid, never the grader's predicate: truncated (`sub-first`, `sub-last`), wrong-content (`wrong-23`)
  and lowercase (`lower23`) lines all fail — but they fail on membership, which incidentally enforces every
  format rule. A case that passes while violating a format constraint would refute these labels; none exists.
- **9 (`write-file`, `one-guess`, `one-per-line`, `enforced`).** The graded artefact must exist as a readable
  file at the exact path (`nop`, `dir-state`, `under-varsea`), its split must yield lines (`empty-file`
  produces `['']`, not a match; `constant-joined` keeps the answer inside a longer line), and at least one
  line must equal the answer — while `decoys-1000` shows 1000 wrong lines do not matter beside one right one.

## Case table

The 16 frozen cases in receipt order; `Tests` is the two captured test letters in file order
(`test_recovery_file_exists`, `test_password_match`; `-` = never reached) and `Observed` is the harness verdict.

| Case | Tests | Observed | What the end state is |
|---|---|---|---|
| `nop` | F- | fail | the seeded image state only — no `recovered_passwords.txt` |
| `oracle-solve-sh` | PP | pass | the task's `solve.sh`: window-scans the image, emits candidates one per line, the true password among them |
| `constant` | PP | pass | the 23-char answer read out of the public test file, written as one line |
| `constant-crlf` | PP | pass | the public answer on a CRLF-terminated line |
| `constant-joined` | PF | fail | the public answer concatenated with two decoys on ONE line |
| `dir-state` | PF | fail | a directory at `/app/recovered_passwords.txt` (IsADirectoryError on read) |
| `empty-file` | PF | fail | a zero-byte `recovered_passwords.txt` — the len>0 assert at :16 cannot fire, membership decides |
| `wrong-23` | PF | fail | one format-conforming 23-char wrong guess |
| `prefix-decoy` | PF | fail | a guess matching every published format constraint, wrong content |
| `sub-first` | PF | fail | the first 20 chars of the answer |
| `sub-last` | PF | fail | the last 20 chars of the answer |
| `lower23` | PF | fail | the answer lowercased |
| `decoys-1000` | PP | pass | the answer plus 1000 wrong guesses, shuffled |
| `password-eq` | PF | fail | `PASSWORD=<answer>` — the file's own launchcode format, not a bare guess |
| `crlf-line` | PP | pass | the answer on a CRLF line followed by another guess |
| `under-varsea` | F- | fail | the oracle's recovery done from inside `/app/varsea` — guesses land at `varsea/recovered_passwords.txt` |

## Mechanism

One row per receipt case, in receipt order: the captured line that decides the case and a verbatim fragment of it.
The Findings section says, case by case, why that line decides it.

| Case | Decisive line | “Quote” |
|---|---|---|
| `nop` | `test_outputs.py:10` | “assert recovered_pass_path.exists(), "Recovery file not found"” |
| `oracle-solve-sh` | `solve.sh:63` | “echo "$combined" >> "$OUTPUT_FILE"” |
| `constant` | `test_outputs.py:18` | “assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses, "Password not found"” |
| `constant-crlf` | `test_outputs.py:14` | “guesses = Path("/app/recovered_passwords.txt").read_text()” |
| `constant-joined` | `test_outputs.py:18` | “in guesses, "Password not found"” |
| `dir-state` | `test_outputs.py:14` | “guesses = Path("/app/recovered_passwords.txt").read_text()” |
| `empty-file` | `test_outputs.py:18` | “assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses, "Password not found"” |
| `wrong-23` | `test_outputs.py:18` | “"8XDP5Q2RT9ZK7VB3BV4WW54" in guesses” |
| `prefix-decoy` | `test_outputs.py:18` | “"8XDP5Q2RT9ZK7VB3BV4WW54" in guesses” |
| `sub-first` | `test_outputs.py:18` | “"8XDP5Q2RT9ZK7VB3BV4WW54" in guesses” |
| `sub-last` | `test_outputs.py:18` | “"8XDP5Q2RT9ZK7VB3BV4WW54" in guesses” |
| `lower23` | `test_outputs.py:18` | “"8XDP5Q2RT9ZK7VB3BV4WW54" in guesses” |
| `decoys-1000` | `test_outputs.py:18` | “assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses” |
| `password-eq` | `test_outputs.py:18` | “"8XDP5Q2RT9ZK7VB3BV4WW54" in guesses” |
| `crlf-line` | `test_outputs.py:14` | “guesses = Path("/app/recovered_passwords.txt").read_text()” |
| `under-varsea` | `test_outputs.py:10` | “assert recovered_pass_path.exists(), "Recovery file not found"” |

## Findings, each tied to its receipt cases

1. **Absence is the do-nothing failure (`nop`, `under-varsea`; `F-`).** `test_recovery_file_exists` dies on its
   exists assert (`:9-10`) whenever the graded path is missing — including when the real recovery happened one
   directory too deep (`under-varsea`: the oracle's `OUTPUT_FILE` is relative, so cwd decides where guesses
   land). Existence is the only gate; the file's location is absolute.
2. **The oracle passes (`oracle-solve-sh` `PP`).** `solve.sh` finds `FIRST_PARTIAL_PART`/`LAST_PARTIAL_PART`
   in the image with `grep -aob`, window-scans each hit, emits every 23-char `combined` candidate into
   `recovered_passwords.txt` (`:63`) — the true password rides among the guesses and membership is satisfied.
3. **Reading the public test file passes (`constant`, `constant-crlf`, `decoys-1000`; `PP`).** The answer is
   hard-coded at `test_outputs.py:18`, and `allow_internet = true` (`task.toml:34`) plus the published repo
   mean the constant is obtainable without touching the disk image at all. A CRLF line passes because
   `read_text()` runs universal-newline mode (`:14`), which turns a lone `\r` into `\n` as well; a thousand
   decoys pass because the check is membership, not exactness or count.
4. **Format violations all fail on the same line (`constant-joined` through `password-eq`; `PF`).** Every
   wrong shape lands at `:18`: a joined line (`<answer><decoy1><decoy2>`), a `PASSWORD=`-prefixed line, a
   truncated, lowercased or wrong-content line — none is `in guesses` as an element. `dir-state` instead dies
   earlier: `exists()` is true but `read_text()` raises `IsADirectoryError`, which the harness records as `F`
   of the second test, not an assertion failure of the first.
5. **The dead assert (`empty-file` `PF`).** `:16` asserts `len(guesses) > 0` after `"".split("\n")` yields
   `['']` — the split of any string is non-empty, so no end state can fire it. The zero-byte file fails at
   `:18` because `''` is not the answer. This is the second dead assert this lane has executed
   (feal-linear had none; the class is smaller here).

## Negative space

This entry does **not** establish: that the task is invalid, mis-calibrated, too easy or unsolvable (no image run, no
agent, no trajectory); that an agent would use the public-file shortcut (the `constant` case is a constructed end
state); that the grader should check format, count guesses, hash a single file or sandbox the answer (no such
proposal is described or judged here); that the instruction's "write each matching password" phrasing requires the
one-per-line shape to be enforced (the entry records only that it is); or anything about how Harbor executes this
verifier.

Nor: **contamination** — `test_outputs.py:2` and `Dockerfile:1-2` carry the canary banner and these captures exist
for digest-pinned re-execution, not as a contamination measurement; **the image's toolchain** — host python3 stands
in for `uvx -p 3.13` python, and pytest itself is not run (the harness reproduces the per-test verdict that is the
only thing `tests/test.sh` rewards); **the oracle's correctness** — `solve.sh` runs as one case's recipe and passes
once, which says nothing about other images or inputs; **prevalence** — one task, 16 cases, no tracker sweep by this
seat; **the instruction's intent** — whether "recover the PASSWORD" was meant to exclude reading the published test
file is the authors' question, and the entry only records that the grader cannot tell the difference.

**Falsifier.** This entry is falsified if (a) a re-fetch of the eight pinned URLs yields bytes whose SHA-256 differs
from `corpus/evidence/round45/tb2-password-recovery/SHA256SUMS` and the pins in `plans/pkg-spec-r45.json`; (b) a
fresh run of `plans/password_recovery_probe.py --lane .` prints anything other than
`cases=16 observed_pass=5 observed_fail=11 mismatches=0` and `regrade cases=16 differ=0` — in particular if
`oracle-solve-sh`, `constant`, `constant-crlf`, `decoys-1000` or `crlf-line` is observed `fail`, or if `nop`,
`constant-joined`, `dir-state`, `empty-file`, `wrong-23`, `prefix-decoy`, `sub-first`, `sub-last`, `lower23`,
`password-eq` or `under-varsea` is observed `pass`; (c) `test_outputs.py` is shown to check the guess list by
anything other than `strip().split("\n")` line membership of `"8XDP5Q2RT9ZK7VB3BV4WW54"` at `:18`, or to read a file
other than `/app/recovered_passwords.txt`; (d) the fragments are shown to be planted anywhere other than the 1MB and
3MB offsets of `$IMG_PATH` (`setup.sh:36-37`); (e) `tests/test.sh` is shown to compute the reward from anything
other than the pytest exit status; or (f) `task.toml` is shown to have `allow_internet = false` at the pinned commit.

## Predictor

The grader's exact rule on the file content (or None when absent): the text is first normalized to LF exactly as
`read_text`'s universal-newline translation does it — every `\r\n` and then every lone `\r` becomes `\n` — then
`.strip()`ped and split on `\n`; the answer passes iff one resulting element equals the 23-character constant.

```python
def predict(text):
    if text is None:
        return False
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return "8XDP5Q2RT9ZK7VB3BV4WW54" in text.strip().split("\n")
```

## Limits

- Host python3 stands in for the image's `uvx -p 3.13` python; pytest itself is not run — the harness
  reproduces the per-test verdict, the only thing `tests/test.sh` rewards (`:26-28`).
- `/dev/urandom` is a 64 KB zeros file inside the sandbox (stated in the probe); fragment offsets are
  reproduced byte-for-byte but noise content differs from a real image.
- The V11 predictor check cannot refuse an open-coded 48-bit truth table small enough to pass the lint;
  non-author review of the predictor block is part of admission.

## Errata (round 46)

Round 45 landed this entry with one false rule and four mislocated citations; the round-45 closure
(`corpus/lessons/round-45-verifier-spotcheck.md` §2 C2 row and §5 items 1-2) routed them. Rows S161, S162 and S163
supersede S152, S153 and S154 under Q34; this entry's `source:` lines still name the rows of record. Each item below
names the old text it replaces and the evidence that decides it.

1. **`## Predictor` block — lone CR not translated (`lone-CR` gap).** Old block:
   `text.replace("\r\n", "\n").strip().split("\n")`. The captured grader's `read_text()` (`test_outputs.py:14`)
   reads in universal-newline mode, which turns a lone `\r` into `\n` too, so the old block false-negatived 6 of
   the counter's 16 frozen states — `C\rD`, `D\rC`, `D\n\rC`, `C\r\r\nD`, `D\r\rC` and `D\r\nC\rD` — while the 2
   CRLF controls and the 4 non-newline separators already agreed. Corroboration: closure §2, row "predictor
   review" — for `C"\r"a`, `"x\r"+C` and `"x\n\r"+C` the "grader True, predictor False". The
   block now replaces `\r\n` and then `\r`, and the round-46 counter's leg B over the same 16 frozen newline
   states (9 carrying a lone `\r`, one CR-CR-LF, 4 non-newline separators — VT, FF, NEL, LS — and 2 CRLF
   controls) reports `disagree=0`.
2. **`## Predictor` and Finding 3 prose — claimed a read the block did not implement.** Old text (line numbers at
   the base revision): "`read_text`'s universal-newline read, `.strip()` and `.split("\n")`" (`:193-194`), with
   Finding 3 (`:150`) saying only that
   "`read_text()` runs universal-newline mode (`:14`)". True of the captured grader, false of the old block, which
   handled CRLF only; both places now state the same rule the code implements — `\r\n` and lone `\r` become `\n`,
   then `.strip()`, then split on `\n` — and Finding 3 names the lone-`\r` case explicitly.
3. **S152/S153/S154 anchor lines — quote and cited line disagree.** Old anchors: `Dockerfile:15`,
   `test.sh:28`, `README.md:44`. The quotes sit at `Dockerfile:17` ("RUN bash /app/setup.sh"), at `test.sh:26`
   ("echo 1 > /logs/verifier/reward.txt"; `:28` carries `echo 0`), and at `README.md:31`; `README.md` has 33
   lines, so `:44` cannot exist. Superseded by S161, S162 and S163 (Q34). Evidence: closure §3 ("S153 anchor
   quote … is verbatim in the re-opened `test.sh`, at `:26`, not the cited `:28`") and the captures.
4. **`empty-file` Mechanism row — named the assert that cannot fire.** Old row: decisive line
   `test_outputs.py:16`, quote `assert len(guesses) > 0, "No guesses found"`. For a zero-byte file the split yields
   `['']`, so `:16` passes on every input; the case fails at `:18`, the membership assert the row now cites.
   Evidence: `test_outputs.py:16,18`, the case table's `empty-file` cell and Finding 5, which already said "fails at
   `:18`".
5. **`source:` range cells — upper bounds past the end of the captures.** Old ranges, against line counts
   re-measured on the captures at `corpus/evidence/round45/tb2-password-recovery/` (`bytes.decode(); .splitlines()`):
   S151 `1-45` → 43, S152 `1-16` → 20, S153 `1-31` → 29, S154 `1-46` → 33, S155 `1-70` → 68. The S150 `1-9`,
   S156 `1-41` and S149 `:9-10`/`:14-18` ranges were already exact and are unchanged. Evidence: the round-46
   counter's leg C reported `source_ranges_bad=4` on the base (the four over-long bounds; the S152 short bound did
   not trip it but still understated a 20-line file) and reports `source_ranges_bad=0` on this revision.
