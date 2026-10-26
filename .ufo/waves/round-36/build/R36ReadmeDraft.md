# R36ReadmeDraft — round-36 C2 corpus/README.md insertions (draft only)

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only for this seat).
Target file: `corpus/README.md` (406 lines at `f9efce3`). **Not edited by this seat** — everything below is a draft for the L1.

## Behavior

Four insertions, no reflow of existing text. Every quoted number below was read from the committed capture/receipt, not re-derived:

| Evidence fact | Command / locus |
|---|---|
| `cases=24 observed_pass=8 observed_fail=16 mismatches=0`, `match=NO` count `0` | `grep '^cases=' corpus/evidence/round36/regex-log-probe.txt`; `grep -c 'match=NO' …` → `0` |
| eight observed-pass cases: `reference-lenient-days`, `reference-month-aware`, `ip-leading-zeros-allowed`, `date-boundary-letters-only`, `hardcoded-expected-dates`, `year-any-digit-count`, `padded-file`, `feb-29-rejected` | `grep -o 'case=[a-z0-9-]* predicted=pass observed=pass' corpus/evidence/round36/regex-log-probe.txt` |
| grader log = 25 lines, expected list = 9 literals | `python3` count over `corpus/evidence/round36/tb2-regex-log/test_outputs.py` → `log_lines= 25`, `expected= 9` |
| Feb 30 / Apr 31 sit only on lines carrying `172.16.0.256` | `test_outputs.py:65`, `test_outputs.py:67` (`cat -n`) |
| one test function, exact-equality assertion, binary reward from pytest exit | `test_outputs.py:8,87,90`; `test.sh` (`echo 1 > /logs/verifier/reward.txt`) |
| probe imports and runs the captured test function under a patched `Path` | `plans/regex_log_probe.py:113-125` (`run_grader`) |
| probe digest == Amendment-1 pin `d58194c8…` | `sha256sum plans/regex_log_probe.py` → `d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc` |
| README index rows `42`, knowledge files `42` (so the new row must make both `43`) | `grep -c '^| \`knowledge/' corpus/README.md` → `42`; `ls corpus/knowledge/*.md \| wc -l` → `42` |

## Draft insertions (with line anchors)

### Insertion 1 — index row, after line 68

Anchor context: line 68 is the `| \`knowledge/tb2-protein-assembly-grader.md\` | … | S105, S106, S107 (terminal-bench-2 @ 2fd12b88) |` row; line 69 is the first `lessons/` row. Insert **after original line 68, before original line 69** (it becomes line 69 once inserted; the knowledge table stays contiguous, `lessons/` follows).

```
| `knowledge/tb2-regex-log-grader.md` | A second Terminal-Bench 2.0 task grader read and executed: `regex-log`'s single test asserts exact equality of `re.findall(pattern, log_text, re.MULTILINE)` against a literal nine-date list over a fixed 25-line in-test log, so the graded artefact is an agent-authored regex file (`/app/regex.txt`, read, stripped, compiled) and no reference inputs exist; a 24-case offline probe runs the captured test function and maps instruction bullets to the assertions that enforce them (`cases=24 observed_pass=8 observed_fail=16 mismatches=0`) | S108, S109, S110 (terminal-bench-2 @ 2fd12b88) |
```

Why this form: `plans/round36_c2_verify.py` W4 (`w4`, lines 155-167) requires **exactly one** line starting `| \`knowledge/tb2-regex-log-grader.md\` |` that contains `S108`, `S109`, `S110`, and requires knowledge files == index rows ≥ 43. 42 + this row = 43 / 43. The task-mandated tail `| S108, S109, S110 (terminal-bench-2 @ 2fd12b88) |` is used verbatim.

### Insertion 2 — coverage-map bullet, after line 257

Anchor context: line 257 is the round-35 `- **Terminal-Bench 2.0 task grader (one task)**: …` bullet and is the **last** line of `## Coverage map`; line 258 is `## Open gaps`. Insert **after original line 257, before `## Open gaps`** (it becomes line 258); the existing blank line separating the section from `## Open gaps` stays after it.

```
- **Terminal-Bench 2.0 task grader (second task)**: covered at source-code depth and executed offline (round 36, 2026-10-25) — knowledge/tb2-regex-log-grader.md; S108, S109, S110; probe `plans/regex_log_probe.py`, receipt `evidence/round36/regex-log-probe.txt`. Extends the round-35 row from `protein-assembly` to `regex-log` only: what its one test asserts (exact equality of `re.findall(pattern, log_text, re.MULTILINE)` against a literal nine-date list over a fixed 25-line in-test log), how `tests/test.sh` turns the pytest exit into `/logs/verifier/reward.txt`, and which `instruction.md` bullets no assertion enforces — a literal alternation of the nine expected dates passes (`hardcoded-expected-dates`, predicted and observed pass), leading-zero IPv4 octets pass, while digit-adjacent dates (`1134-12-1234`), a non-four-digit year and the permitting side of Feb 29 are unobserved (a February-capped-at-28 regex passes, `feb-29-rejected`), and month-length validity never decides because the only Feb 30 / Apr 31 lines (`tests/test_outputs.py:65,67`) carry the already-invalid `172.16.0.256`. What it does enforce is bounded by the nine literals: last-date-in-line, an IPv4 present anywhere in the line, octets 0-255, month 01-12, day 01-31, letter-adjacency on both sides of date and IP, one capture group, and file presence + compilation. Not the other TB2 tasks, not the correctness of the nine literals, not the harness's own container execution (the probe calls the captured test function under a patched `Path`), not runtime task validity, not contamination.
```

### Insertion 3 — §Frontier sub-bullet, after line 282

Anchor context: line 282 is the `  - *Partly discharged round 35 (2026-10-25):* …` sub-bullet of `- **Agentic benchmark task-spec audits**`; line 283 opens `- **Contamination transparency cards**`. Insert **after original line 282, before original line 283** — the new sub-bullet is the last child of the task-spec bullet, not a child of the Contamination bullet. Two-space indent, same shape as its siblings.

```
  - *Partly discharged round 36 (2026-10-25):* `knowledge/tb2-regex-log-grader.md` reads and executes a second Terminal-Bench 2.0 task's scoring code (`regex-log/tests/test_outputs.py` @ `2fd12b88`; `tests/test.sh` read, not run) against its `instruction.md`. The "Terminal-Bench 2.0's" clause is discharged **for that one task only**; it stays open for the other TB2 tasks, for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane).
```

The `read, not run` clause is deliberate: it does not repeat the round-35 F1 overstatement that line 406 corrects.

### Insertion 4 — `### Round-36 evidence` subsection, after line 406 (EOF)

Anchor context: lines 400-406 are `### Round-35 evidence` and its five bullets; 406 is the last line of the file (`wc -l` → `406`). Append **after line 406**, starting with one blank line so the new `###` heading is separated from the round-35 correction bullet.

```

### Round-36 evidence

- `evidence/round36/tb2-regex-log/` — the five pinned `regex-log` files (`test_outputs.py`, `test.sh`, `instruction.md`, `task.toml`, `solve.sh` = the task oracle) with `SHA256SUMS`; `test_outputs.py`, `test.sh` and `instruction.md` are rows S108, S109, S110.
- `evidence/round36/regex-log-probe.txt` — receipt of `plans/regex_log_probe.py` (24 frozen cases, `cases=24 observed_pass=8 observed_fail=16 mismatches=0`; re-run and byte-compared by `plans/round36_c2_verify.py` W5).
- `evidence/round36/regex-log-probe-first-run.txt` + `evidence/round36/regex-log-dry-cases-freeze.txt` — the pre-Amendment-1 run (two assertion texts carry the `mkdtemp` path) and the frozen `--dry` case table, retained as disclosure per Amendment 1.
- `evidence/round36/toolathlon-package.md` — the committed round-35 package copy the round-36 claims compute C1's R35-D4 recount from (`13 + 23 + 1 = 37`, denominator 38; `plans/round-36-claims.md` §C1).
- `defects-round35.jsonl` — the four routed round-35 defects (R35-D1..D4) as ledger rows, re-run at every tip by `plans/round36_c1_verify.py`.
- `../plans/pkg_gate.py` — the hardened package gate C1 lands this round; listed only if the file exists at integration, because C1 is not admitted without it. `[if landed]`
```

Paths follow the file's own convention (`evidence/…`, `defects-…`, `../plans/…`), i.e. corpus-relative — the task's lane-relative forms map to `corpus/evidence/round36/…`, `corpus/defects-round35.jsonl`, `plans/pkg_gate.py`.

## Gates that bind the draft

- W4 (`plans/round36_c2_verify.py:155-167`) turns green only when insertions 1 and 2 are both present **and** `corpus/knowledge/tb2-regex-log-grader.md` exists. Knowledge files today: 42; index rows today: 42. The row must not be duplicated.
  Exercised in a throwaway `/tmp` copy (lane untouched): copied `corpus/README.md` + the 42 knowledge files, added a stub entry, applied the four insertions with the offsets above, then called the counter's own `w4()` — `W4 -> None` (pass), index rows `43`, knowledge files `43`, exactly one row starting `| \`knowledge/tb2-regex-log-grader.md\` |`. Placement re-checked: new sub-bullet at line 285 sits directly after the round-35 sub-bullet (now 284) and before `- **Contamination transparency cards**` (286).
  Caveat: the simulation substitutes a stub entry file and stub bullet tails, so it proves the README-side conditions (row shape, coverage membership, parity), not W3's entry content.
- W5 pins the receipt's summary line and requires the *entry* (not the README) to carry it verbatim; no `match=NO` case exists (`grep -c` → 0), so the entry has no case to name. Nothing in W5 reads the README.
- W3/W2 are owned by other seats (`corpus/knowledge/tb2-regex-log-grader.md` absent, `corpus/SOURCES.md` has no S108-S110 row as of this read) — my insertions reference them but do not create them.

## Findings / limits (for the L1 and wave-2 seats)

1. **`__pycache__` in the capture dir.** `corpus/evidence/round36/tb2-regex-log/__pycache__/` exists (from the probe importing the captured module). It is ignored by `.gitignore:2` (`__pycache__/`), so it does **not** appear in `git ls-files --others --exclude-standard` and does not threaten C1's `--require-clean-tree`. Left in place; noted only so a reviewer does not read it as a stray artefact.
2. **C2 counter digest drift vs the claims' frozen block.** `plans/round-36-claims.md` lists `f70e6d3a…` for `plans/round36_c2_verify.py`; the committed file is `983ed65c…` (`sha256sum`). Explained by Amendment 1's one-line `PROBE_SHA256` change, which the claims disclose — but the frozen-digest block was not rewritten, so a literal-digest reader will see a mismatch. Not repaired here (no write scope in `plans/`).
3. **The index `what` cell is intentionally long-form**, matching the round-35 row's density. If the L1 prefers a shorter cell, only the `<what>` span may shrink; the `S108, S109, S110 (terminal-bench-2 @ 2fd12b88)` tail is the contract and W4 requires all three ids.
4. **Unverified by this seat:** whether `corpus/knowledge/tb2-regex-log-grader.md` will name the same eight observed-pass cases my coverage bullet cites. My sentences are bound to the receipt and the captured grader bytes, so they stay true for any entry that reports those bytes honestly; if the entry's headline differs, the bullet's final "does enforce" list is the only clause worth reconciling.
5. **Untracked wave-1 output is visible to C1's clean-tree check.** `.ufo/` is tracked (8606 files) and only `.ufo/interactive-sessions/` is ignored (`.gitignore:1`); `git ls-files --others --exclude-standard` in the lane currently returns **860** files, 843 of them under `.ufo/waves/round-36/build/`. `plans/round36_c1_verify.py:279-289` (R35-D2) requires that list to be empty, so every wave-1 report — including this one — must be committed at integration, or grouped under an ignore rule, before C1's clean-tree check can hold. Reported, not repaired (out of write scope).
6. **Not touched:** `corpus/README.md` itself, `corpus/SOURCES.md`, `corpus/knowledge/`, `plans/`, the lane git index, jj state. No fixture clone was needed (all reads were path-scoped).

## Artifact paths

- Report: `.ufo/waves/round-36/build/R36ReadmeDraft.md`
- Scratch: `.ufo/waves/round-36/build/R36ReadmeDraft/` (created, empty — no scratch file was needed)

VERDICT: readme-draft-4-insertions
