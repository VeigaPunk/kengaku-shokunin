# R44PkgProse — integration prose for the C2 package (kengaku round 44)

Seat: scribe, leaf (no subagents, no background jobs). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Read-only against the lane: **no lane file was edited**; the only file this seat wrote is this report (plus its
directory). No counter, battery, probe or fixture was run, so no envelope run exists and no scratch dir was created
(`/fast/scratch/hyaku/kengaku-r44/R44PkgProse` never needed; nothing was written outside the report path).

## Axes named (godspeed)

1. **coverage** — the C2 entry is invisible until README, PROVINCE and SKILL name it; three surfaces, each with the
   exact insertion anchor.
2. **adjacency** — the PROVINCE routing clause: what this lane owns (what the captured grader checks and what passes
   it), what is unowned (linear-cryptanalysis technique; the published `sha256(seed+counter)` generator as a subject),
   and which sibling owns what, grounded in sibling PROVINCE text and a dated sweep.
3. **falsifiability** — every number and quote in the blocks carries a receipt line or capture file:line.
4. **operability** — the SKILL section opens with the probe's exit-code contract, so a later seat cannot read
   `--dry`/`--stage-check` as evidence.
5. **no-harm** — every block is additive; no existing round-35…43 paragraph, row or bullet is rewritten, so no
   previous admission's prose moves.

## Blocks

Six paste-ready blocks: three for `corpus/README.md`, one `PROVINCE.md` section, one `SKILL.md` section, and one
optional `SKILL.md` registry addendum. All line references below are to the lane as read today
(`corpus/README.md` 560 lines, `PROVINCE.md` 643, `SKILL.md` 1279).

---

### Block 1 — `corpus/README.md` index row

**Where:** the `## What's here` table, immediately after the row at line 76
(`| \`knowledge/tb2-feal-differential-cryptanalysis-grader.md\` | …`), i.e. as the new line 77, before
`| \`lessons/round-1.md\` | …`. It must be one physical line and must match `^\|\s*\`(knowledge/[^\`]+\.md)\`\s*\|`
(`plans/pkg_gate.py:29`) — the row below does.

```markdown
| `knowledge/tb2-feal-linear-cryptanalysis-grader.md` | A tenth Terminal-Bench 2.0 task grader read and executed, and a grader class new to this lane: `feal-linear-cryptanalysis` grades an **agent-written text file** by substring membership — `/app/plaintexts.txt` (`instruction.md:10`) is read whole (`test_outputs.py:120`) and each of the 100 decimal constants embedded in the test file (`:4-103`) is asserted to occur in it (`:121-122`), with no count, order, format or exactness check — so three passes need no attack (the four round keys are literals in the published `gen.py:12`, the 100 plaintexts are that file's `sha256(seed+counter)` chain at `:59-62`, and the constants themselves are in the published test file), and concatenated, reversed, zero-padded and 100-decoy outputs also pass, while one missing plaintext, hex output, a key off by one bit, the 32 known plaintexts and the ciphertexts copied unchanged fail; `cases=14 observed_pass=8 observed_fail=6 mismatches=0`; `regrade cases=14 differ=0` | S138, S139, S140, S141, S142, S143, S144, S145, S146 (terminal-bench-2 @ 2fd12b88); probe `plans/feal_linear_probe.py`, receipt `evidence/round44/feal-linear-probe.txt` |
```

---

### Block 2 — `corpus/README.md` coverage-map bullet

**Where:** the `## Coverage map` list, immediately after the ninth-task bullet ending at line 273, i.e. as the new
line 274, before the blank line that precedes `## Open gaps` (line 275). **One physical line**: the gate selects it
with `l.startswith("- ")` plus the entry name plus `evidence/round44/feal-linear-probe.txt`
(`plans/pkg_gate.py:248-251`).

```markdown
- **Terminal-Bench 2.0 task grader (tenth task, constant-compare class)**: covered at source-code depth and executed offline (round 44, 2026-10-26) — knowledge/tb2-feal-linear-cryptanalysis-grader.md; S138–S146; probe `plans/feal_linear_probe.py`, receipt `evidence/round44/feal-linear-probe.txt`. A tenth instance of the same ground (10 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `feal-linear-cryptanalysis` only: the graded artefact is an agent-written text file, `/app/plaintexts.txt` (`instruction.md:10`), and the whole verdict is one pytest function that reads it whole (`test_outputs.py:120`) and asserts that each of 100 decimal constants held in the test file (`:4-103`) occurs in it as a substring (`:121-122`) — no count, no order, no format and no exactness check — while `tests/test.sh:22` runs pytest and `:25-26` writes `/logs/verifier/reward.txt` from its exit status. Three passes involve no attack: the four round keys are literals in the published `gen.py:12`, the 100 plaintexts are that file's `sha256(seed+counter)` chain (`:59-62`) although the image deletes `gen.py` (`Dockerfile:14`), and the expected constants are in the published test file; concatenated, reversed, zero-padded and 100-decoy outputs also pass, while one missing plaintext, hex output, a round key off by one bit, the 32 known plaintexts and the ciphertexts copied unchanged fail (`cases=14 observed_pass=8 observed_fail=6 mismatches=0`, `regrade cases=14 differ=0`). Not the task image (never pulled; `task.toml:29`) or a harness run (the task's own `solve.sh` is executed as one case and observed pass), not contamination, not model or agent behaviour.
```

---

### Block 3 — `corpus/README.md` `## Frontier` narrowing sub-bullet

**Where:** inside `## Frontier` (the section runs from line 289 to the next `^## `, line 406), immediately after the
round-43 sub-bullet that ends `not model or agent behaviour.` at line 395, i.e. as the new lines 396-…, before the
`- **Contamination transparency cards**` bullet at line 396. Continuation lines are indented two spaces like the
round-38…43 sub-bullets. **Why this exact shape:** `plans/round44_c2_verify.py:315-317` requires the token
`feal-linear-cryptanalysis` somewhere in the `## Frontier` body.

```markdown
  - *Partly discharged round 44 (2026-10-26):* `knowledge/tb2-feal-linear-cryptanalysis-grader.md` reads and
    executes a tenth Terminal-Bench 2.0 task's scoring code (`feal-linear-cryptanalysis/tests/test_outputs.py` and
    `tests/test.sh` @ `2fd12b88`; S138–S146) against its `instruction.md`, probe `plans/feal_linear_probe.py`,
    receipt `corpus/evidence/round44/feal-linear-probe.txt`. The graded state is a class the lane had not executed
    before: an **agent-written text file judged by substring membership**. `test_outputs.py` holds 100 decimal
    constants in one triple-quoted string (`:4-103`) and one test function (`:106-122`) that reads
    `/app/plaintexts.txt` whole (`:120`) and asserts `c in data` for each constant (`:121-122`): membership over the
    entire file text, with no count, no order, no format and no exactness check, and `test.sh:22` runs pytest while
    `:25-26` writes `/logs/verifier/reward.txt` from its exit status. Eight of the fourteen observed passes, one of
    them the task's own oracle (`oracle-solve-sh`), need no attack: three read the published task source — the four
    round keys at `gen.py:12`, the `sha256(seed+counter)` plaintext chain at `:59-62` under the same published seed,
    and the constants in `tests/test_outputs.py` — although the image deletes `gen.py` (`Dockerfile:14`) and ships
    no tests, and four more pass by shape (concatenated, reversed, zero-padded, correct plus 100 wrong-key decoys)
    because the assertion is membership over the whole file. The six failures are one missing plaintext, hex
    output, a round key off by one bit, the 32 known plaintexts, the ciphertexts copied unchanged and `nop`
    (`cases=14 observed_pass=8 observed_fail=6 mismatches=0`, `regrade cases=14 differ=0`). The "Terminal-Bench
    2.0's" clause is **narrowed for that one task only**; it stays open for the remaining TB2 task graders (10 of 89
    read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which
    `PROVINCE.md` refuses to this lane). Not the task image (never pulled) or a harness run (the task's own
    `solve.sh` is executed as one case and observed pass), not contamination, not model or agent behaviour.
```

---

### Block 4 — `PROVINCE.md` round-44 section

**Where:** appended at end of file (file today ends at line 643, after the round-43 erratum paragraph, with a blank
line). **The `**Core addition:**` line must stay ONE physical line**: `plans/round44_c2_verify.py:313-314` requires
some single line of `PROVINCE.md` to contain both `feal-linear-cryptanalysis` and
`tb2-feal-linear-cryptanalysis-grader.md`.

```markdown
## Round44 partial frontier admission (2026-10-26)

**Core addition:** offline execution of one more pinned Terminal-Bench 2.0 grader — `feal-linear-cryptanalysis` (`tests/test_outputs.py` and `tests/test.sh` at terminal-bench-2 `2fd12b88`) — over 14 frozen end states, via `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md` (S138, S139, S140, S141, S142, S143, S144, S145, S146), `plans/feal_linear_probe.py` and receipt `corpus/evidence/round44/feal-linear-probe.txt` (`cases=14 observed_pass=8 observed_fail=6 mismatches=0`; `regrade cases=14 differ=0`).

The graded state is a class new to this lane: not an assertion over a structure, not a computation inside the test
and not a module the grader imports, but an **agent-written text file judged by substring membership**. One test
function does everything (`test_outputs.py:106-122`): `data = open("/app/plaintexts.txt").read()` (`:120`) takes the
whole file text, then `for c in soln.split(): assert c in data` (`:121-122`) requires each of 100 decimal constants —
held in the same test file as one triple-quoted string (`:4-103`) — to occur somewhere in it. There is no count, no
order, no format and no exactness check: the grader never asks how many numbers the file holds, in which order, or
whether anything else is in it. `tests/test.sh:22` runs that one test under `uvx -p 3.13` with pytest 8.4.1 and
`:25-26` writes `/logs/verifier/reward.txt` from the exit status, so the verdict is pytest's exit status and nothing
else. `instruction.md:1-10` asks for a known-plaintext attack that recovers the cipher's key and then for all
ciphertexts in `/app/ciphertexts.txt` decrypted into `/app/plaintexts.txt` (`:9-10`), and names no output format;
the benchmark's own `README.md:32` states the membership reading ("verifies that all 100 expected plaintext values
appear in `/app/plaintexts.txt`"). The 100 expected values are not hidden from a reader of the repository: the four
round keys are literals in the published `environment/task-deps/gen.py` (`gen.py:12`), `gen.py:19-20` derives its
seed hash from them and `gen.py:27`/`:61` derive every plaintext as `sha256(seed_hash + counter_bytes)[:8]`, and the
constants are in the published `tests/test_outputs.py` — while the image deletes `gen.py` (`Dockerfile:14`) and
ships no tests, so "public" here means the benchmark repository, never the task image.

Observed on the 14 frozen cases: eight pass and six fail, with no prediction mismatch (`cases=14 observed_pass=8
observed_fail=6 mismatches=0`, receipt:24) and a second grading of each end state by a fresh harness process agreeing
case by case (`regrade cases=14 differ=0`, receipt:23). The eight passes are the task's own oracle (`oracle-solve-sh`,
receipt:10) plus seven that need no cryptanalysis: decrypting with the four round keys the public `gen.py` states
(`decrypt-public-keys`, receipt:11), recomputing the 100 plaintexts from the public `sha256` chain and never
decrypting (`replay-public-gen`, receipt:12), copying the constants out of the public test file
(`copy-public-constants`, receipt:13), and four shapes the membership test cannot distinguish — the correct numbers
on one line with no separator (`oracle-concatenated`, receipt:14), the correct numbers followed by 100 decryptions
under a wrong key, two answers per ciphertext (`oracle-plus-decoys`, receipt:15), the correct lines reversed
(`oracle-reversed`, receipt:16), and the correct plaintexts as 20-digit zero-padded decimals
(`oracle-zero-padded`, receipt:17). The six failures are the shapes that omit a constant or produce the wrong one:
no `/app/plaintexts.txt` (`nop`, a `FileNotFoundError` at `test_outputs.py:120`, receipt:9), the correct 100 with
the last dropped (`one-missing`, receipt:18), the correct plaintexts in hexadecimal, which no longer contains the
decimal strings (`hex-output`, receipt:19 — `instruction.md` names no format, so this is the grader's decimal
rendering, not the instruction's), a round key off by one bit (`wrong-key-decrypt`, receipt:20), the 32 known
plaintexts from `pairs.txt` (`pairs-plaintexts`, receipt:21) and `ciphertexts.txt` copied unchanged
(`ciphertexts-copied`, receipt:22). It records how that captured grader answers those synthetic states only: it does
not run Terminal-Bench, the task image (`task.toml:29` names `alexgshaw/feal-linear-cryptanalysis:20251031`;
`allow_internet = true` at `:34`; the image is never pulled) or a harness (`tests/test.sh`'s `uvx`/pytest path and
its reward write are read, not run), does not validate or certify the task, measure difficulty, gameability or
contamination, and does not speak for the remaining 79 TB2 task graders (89 carry `tests/test.sh`; 10 are read).
Limits: host python3 and host gcc stand in for the image's python 3.13 under `uvx` and Debian bookworm gcc; pytest
is not run — the harness calls the one test function and maps its outcome onto pytest's exit status; the image's
`pip install setuptools==80.9.0` is not replayed; recipes run as the probing user, not root; each case stages its
own `/app` and `/tests`, and `/pub` holds read-only copies of `gen.py`, `test_outputs.py` and `solve.sh`, so a case
that reads it models an agent who read the public repository, not one who read the image; the cases are constructed
end states, not agents. Disclosed ordering: before the freeze the probe ran only `--dry` and `--stage-check`
(`stagecheck cases=14 failed=0`, `.ufo/waves/round-44/claims/c2-stage-check.txt`), and round-43 wave-1 seat
`R43PlanNext` had run the task oracle and a substring check of the same constants on this host
(`CONSTANTS 100 ALL_IN_DATA True LINES 928`,
`.ufo/waves/round-43/build/R43PlanNext/feal_linear_run_oracle.sh`); `oracle-solve-sh` re-observes that shape and the
other thirteen cases were never graded before the freeze (`plans/round-44-claims.md` §Order of operations).

Round-44 routing (drafted by `R44PkgProse`; the L1 confirms). This lane owns what the captured grader checks and
what passes it — nothing else. **Two findings are unowned: the cryptanalysis itself — whether a linear attack on
this 4-round FEAL-like construction recovers its four 20-bit round keys from 32 known pairs, and the cipher's own
implementation semantics beyond what decides this verdict — and the published-generator question, i.e. whether a
`sha256(seed + counter)` plaintext chain whose seed is a hash of the round keys is a leak in any sense beyond
"a reader of the repository can recompute it".** That the repository publishes `gen.py` and the constants is a fact
of this capture and is recorded here; grading whether that is a defect of the benchmark, and how it should be
repaired, is not this lane's. Named sweep, 2026-10-26 from `/home/vgpnk/Projects/shokunin`:
`for pat in "cryptanalys" "linear cryptanalysis" "known-plaintext" "hash chain"; do printf '%s -> ' "$pat"; hits=$(grep -lri "$pat" --include=PROVINCE.md ./*/PROVINCE.md 2>/dev/null); echo "${hits:-<none>}"; done`
returns `cryptanalys -> ./kengaku-shokunin/PROVINCE.md` (this lane's own round-43 paragraph) and
`<none>` for the other three patterns; no sibling declares the subject. What the siblings do own and would receive
such a finding: **chousa** the research method (`PROVINCE.md:137`), **kotoba** prompt- and skill-craft rules
(`PROVINCE.md:138`), **tameshi** verification-fixture craft — hermetic suites, mutation testing, fail-closed arms,
verdict-line discipline (`tameshi-shokunin/PROVINCE.md:3-4`), **protocol / aggregator** fleet process
(`PROVINCE.md:139`). Advising an agent how to attack this cipher, and prior-art pricing of linear cryptanalysis on
FEAL, are likewise not this lane's: the task's own `solve.sh` is executed as one case and observed pass, nothing
more. Terminal-Bench's task, image and oracle stay the benchmark's; the round35-43 paragraphs above stay as written,
and this paragraph narrows only their "remaining TB2 tasks" clause for this one task.
```

---

### Block 5 — `SKILL.md` section

**Where:** appended at end of file (file today ends at line 1279, the round-43 section's limits paragraph). Placed
after the round-43 section so the two `feal-*` graders stay adjacent and in chronological order.

```markdown
## Constant-compare TB2 grader — round 44

Before citing the pinned TB2 `feal-linear-cryptanalysis` scorer, run `python3 plans/feal_linear_probe.py --lane .`
and read its summary line: exit `0` means only that every one of the 14 cases produced two verdicts — a prediction
mismatch does not change the exit code, it is printed as `match=NO` on the case line and counted in `mismatches=`;
exit `1` is a `--stage-check` failure; exit `2` is a probe error (a capture missing or off its pinned digest, a
required binary not executable, an uncreatable `--work`, a case whose recipe exited non-zero — a recipe error is
never a verdict). `--dry` and `--stage-check` are not evidence. The receipt's summary
(`corpus/evidence/round44/feal-linear-probe.txt:24`) reads `cases=14 observed_pass=8 observed_fail=6 mismatches=0`,
and grading each end state a second time in a fresh harness process agrees case by case (`regrade cases=14 differ=0`,
`:23`).

The class is new: the graded artefact is an **agent-written text file judged by substring membership**, with no
grader-owned model, interpreter or import in play. `tests/test_outputs.py` holds 100 decimal constants in one
triple-quoted string (`:4-103`) and one test function (`:106-122`) that reads `/app/plaintexts.txt` whole
(`:120 data = open("/app/plaintexts.txt").read()`), then asserts `c in data` for each constant (`:121-122`). That is
membership over the entire file text: no count, no order, no format, no exactness, and no rejection of anything else
in the file. `tests/test.sh:22` runs that one test under `uvx -p 3.13` (pytest 8.4.1) and `:25-26` writes
`/logs/verifier/reward.txt` from the exit status. The expected values are reachable without an attack from the
benchmark repository: the four round keys are literals in `gen.py:12`, `gen.py:19-20` hashes them into the seed and
`:27`/`:61` derive every plaintext as `sha256(seed_hash + counter_bytes)[:8]`, and the constants are in the test file
itself — while the image deletes `gen.py` (`Dockerfile:14`), so those are public files, not image files.
`instruction.md:9-10` names the output file and no format.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| the whole file text, `open("/app/plaintexts.txt").read()` (`test_outputs.py:120`) | the correct numbers joined into one line with no separator passes (`oracle-concatenated`, `P`) | whether a line/record shape was asked for; `instruction.md` asks for no format, so nothing is enforced here | `oracle-concatenated` (receipt:14) |
| `assert c in data` per constant (`:121-122`) — membership only | the correct lines in reverse order pass (`oracle-reversed`, `P`) | a per-line comparison (`data.splitlines()` equality) | `oracle-reversed` (receipt:16) |
| the same membership, nothing else (`:122`) | the correct 100 followed by 100 decryptions under a wrong key pass — two answers per ciphertext (`oracle-plus-decoys`, `P`) | that extra tokens are rejected; nothing in the test reads a count or a second column | `oracle-plus-decoys` (receipt:15) |
| the same membership on decimal strings (`:121-122`) | the correct plaintexts as 20-digit zero-padded decimals pass (`oracle-zero-padded`, `P`); the same values in hexadecimal fail (`hex-output`, `F`) because the decimal constants are no longer substrings | that the number format is the one the task means — the test forgives decimal padding, never a change of base | `oracle-zero-padded` (receipt:17), `hex-output` (receipt:19) |
| 100 constants, each required once (`:121-122`) | all 100 to pass with one dropped fails (`one-missing`, `F`): the conjunction is complete even though nothing else about the file is checked | that each expected value is present — completeness is the only real constraint | `one-missing` (receipt:18) |
| `gen.py:12`'s four round keys, published in the repository | decrypting `ciphertexts.txt` with those keys, no attack at all, passes (`decrypt-public-keys`, `P`) | which key material the answer came from; whether the task's premise (key recovery) was touched | `decrypt-public-keys` (receipt:11) |
| `sha256(seed_hash + counter_bytes)` at `gen.py:27`/`:61`, seed from `gen.py:19-20`, published | recomputing the 100 plaintexts from the hash chain, no key and no decryption, passes (`replay-public-gen`, `P`) | whether the plaintexts are derivable from published bytes — here they are | `replay-public-gen` (receipt:12) |
| the constants themselves, in the published `tests/test_outputs.py:4-103` | copying all 100 constants into `/app/plaintexts.txt` passes (`copy-public-constants`, `P`) | that the expected values are not in the repository the agent can read (they are) | `copy-public-constants` (receipt:13) |
| nothing — no file at `/app/plaintexts.txt` (`:120`) | the test raises `FileNotFoundError` and the case fails (`nop`, `F`) | that the file exists and is the one named at `instruction.md:10` | `nop` (receipt:9) |
| values that are not the constants (`:121-122`) | a round key off by one bit (`wrong-key-decrypt`), the 32 known plaintexts (`pairs-plaintexts`) and `ciphertexts.txt` copied unchanged (`ciphertexts-copied`) all fail (`F`) | that the plaintexts are the decryption of `ciphertexts.txt`, not of `pairs.txt` and not the ciphertexts | `wrong-key-decrypt` (receipt:20), `pairs-plaintexts` (receipt:21), `ciphertexts-copied` (receipt:22) |
| pytest's exit status as the whole verdict (`test.sh:22`, `:25-26`) | the task's own oracle passes (`oracle-solve-sh`, `P`); nothing asserts that an attack file exists, that a key was recovered, or that anything was timed | what the reward actually measures — `README.md:32` states the same membership reading | `oracle-solve-sh` (receipt:10), `README.md:32` |

V7 labels derived from the receipt (frozen tag lines, `corpus/evidence/round44/feal-linear-dry-cases-freeze.txt:1-4`:
`known-plaintext-attack` `instruction.md:7`, `recover-key` `:7`, `decrypt-all` `:8`, `plaintexts-file` `:10`):
`plaintexts-file` **enforced** (1 case, 0 pass — `nop`); `decrypt-all` **partly** (7 cases, 2 pass);
`known-plaintext-attack` **partly** (6 cases, 3 pass); `recover-key` **partly** (7 cases, 3 pass). Every label is a
property of this frozen 14-case set only, not a reading of the instruction prose.

Limits: the probe never runs the task image (`task.toml:29`, `allow_internet = true` at `:34`, never pulled) or a
harness; host python3 and host gcc stand in for the image's python 3.13 under `uvx` and Debian bookworm gcc; pytest
itself is not run — the harness calls the one test function and maps its outcome onto pytest's exit status; the
image's `pip install setuptools==80.9.0` is not replayed; recipes run as the probing user; each case stages its own
`/app` and `/tests`, and `/pub` holds read-only copies of the three public files (`gen.py`, `test_outputs.py`,
`solve.sh`), so a case that reads it models an agent who read the repository; the cases are constructed end states,
not agents. A property of this capture at `2fd12b88`; not a task-validity, difficulty or gameability verdict, not
solver advice, not a statement about linear cryptanalysis, the FEAL cipher or `sha256` in general, and not a
statement about any agent's behaviour.
```

---

### Block 6 (optional) — `SKILL.md` gate/probe registry addendum

**Where:** the `## Gate/probe registry` table, after the `feal-probe` row (line 604) and its continuation — i.e. as
two new rows before the `scratch-root-guard` row (line 605), keeping the per-round gate/probe pairing used since
round 41. **Clause sources, not re-runs:** the predicate text is the counter's docstring
(`plans/round44_c2_verify.py:1-40`) and its `main()` (`:529-549`); the probe text is
`plans/feal_linear_probe.py:1-48`. This seat did not run either, so these rows state documented behaviour, exactly
as the round-43 rows do; the L1's landing run is what makes them measured.

```markdown
| `round44-c2` | gate | `python3 plans/round44_c2_verify.py --lane .` (lane root; `--work DIR` scratch parent, created if absent) | `0` `checks=11 defects=0` then `PREDICATE C2 pass` · `1` any `Vn DEFECT <note>` (a check that raises is a defect, never a pass); V11 is the held-out predictor — the entry's `## Predictor` block must agree with the captured grader on 48 generated end states with ≥8 passes and ≥8 fails · `2` argparse usage only | itself; freeze control `.ufo/waves/round-44/claims/control-c2-nothing.txt` (`PREDICATE C2 fail`, exit 1); predictor control `.ufo/waves/round-44/claims/control-c2-predictor.txt` (`red-as-required`: always-True 24 disagreements, whitespace-token-set 12, exact-lines 18, substring ok) | spec `plans/pkg-spec-r44.json`, gate, probe, dry table, eleven captures and DECISIVE pinned in the counter | scratch only | kengaku round 44 |
| `feal-linear-probe` | probe | `python3 plans/feal_linear_probe.py --lane .` (`--dry` prints the four `TAG` lines and the 14 frozen `CASE` lines, no sandbox; `--stage-check` builds every case's end state and reports whether `/app/plaintexts.txt` exists, never grading; `--work DIR` scratch parent) | `0` every case graded by two fresh harness processes and both summary lines printed — prediction mismatches are on the summary line (`cases=14 observed_pass=8 observed_fail=6 mismatches=0`), never in the exit code · `1` `--stage-check` only: a case's setup or recipe stage exited non-zero · `2` setup: a capture missing or off its pinned digest, bwrap/python3/bash/gcc not executable, an uncreatable `--work`, or a case whose recipe exited non-zero | receipt `corpus/evidence/round44/feal-linear-probe.txt` (`regrade cases=14 differ=0`), dry table `corpus/evidence/round44/feal-linear-dry-cases-freeze.txt` | scratch under `--work` | kengaku round 44 |
```

---

## Gates these blocks answer (and what stays with the L1)

| gate clause | what it needs | satisfied by |
|---|---|---|
| `pkg_gate` P8, index row (`plans/pkg_gate.py:237-244`) | exactly one `INDEX_ROW` for `knowledge/tb2-feal-linear-cryptanalysis-grader.md`, citing every spec row id | Block 1 (one physical row, cites S138–S146) |
| `pkg_gate` P8, coverage bullet (`:248-251`) | a line starting `- ` containing the entry name and `evidence/round44/feal-linear-probe.txt` | Block 2 |
| `pkg_gate` P8, parity (`:252-255`) | `knowledge/*.md` set equals index keys | the entry file must land in the same commit as Block 1 — L1 |
| `round44_c2_verify` V9, PROVINCE (`:313-314`) | one physical line with `feal-linear-cryptanalysis` **and** `tb2-feal-linear-cryptanalysis-grader.md` | Block 4's `**Core addition:**` line (kept unwrapped) |
| `round44_c2_verify` V9, README Frontier (`:315-317`) | `## Frontier` body contains `feal-linear-cryptanalysis` | Block 3 |
| `round44_c2_verify` V7 (labels) | label derived by `derive()` from the receipt's violating cases | Block 5's label paragraph, computed with the receipt (enforced 1/0; partly 7/2, 6/3, 7/3) |
| entry-side V4/V10/V11 | Case table, Mechanism, Predictor, quotes | not this seat (L1 + entry author) |

## Evidence

Every number above comes from one of these reads (all read-only; commands run from the lane root or the capture dir):

1. `wc -l corpus/README.md PROVINCE.md SKILL.md` → `560 / 643 / 1279`.
2. Index/coverage anchors: `grep -n "tb2-feal-differential-cryptanalysis-grader.md\|ninth task, in-process\|Partly discharged round 43\|Contamination transparency cards\|Round-43 evidence" corpus/README.md` → `76`, `273`, `379`, `396`, `556`; `sed -n '273,276p'` shows the ninth bullet at 273 and `## Open gaps` at 275; `sed -n '393,396p'` shows the round-43 sub-bullet ending at 395 and the next bullet at 396.
3. PROVINCE tail: `sed -n '530,643p' PROVINCE.md` — round-43 section then its erratum; file ends with a blank line (`tail -c 300 | od -c`).
4. SKILL tail: `grep -n "^#\|^##\|^###" SKILL.md | tail -50` → last heading `## In-process module-import TB2 grader — round 43` (1221), limits paragraph ends at 1279; registry rows at 596-604.
5. Receipt: `grep -n "CASE\|regrade\|cases=" corpus/evidence/round44/feal-linear-probe.txt` → CASE lines 9-22 (`nop` 9, `oracle-solve-sh` 10, `decrypt-public-keys` 11, `replay-public-gen` 12, `copy-public-constants` 13, `oracle-concatenated` 14, `oracle-plus-decoys` 15, `oracle-reversed` 16, `oracle-zero-padded` 17, `one-missing` 18, `hex-output` 19, `wrong-key-decrypt` 20, `pairs-plaintexts` 21, `ciphertexts-copied` 22), `regrade cases=14 differ=0` at 23, `cases=14 observed_pass=8 observed_fail=6 mismatches=0` at 24.
6. Capture line numbers (`corpus/evidence/round44/tb2-feal-linear-cryptanalysis/`): `test_outputs.py` — `soln = """…` at 4, 100 constants to `:103` (`python3 -c` regex + `split()` → `constants 100`), `def test_attack():` 106, `data = open("/app/plaintexts.txt").read()` 120, `for c in soln.split():` 121, `assert c in data` 122; `gen.py` — keys literal 12, `seed_hash` 19-20, chain 27 and 61; `Dockerfile` — `RUN python3 gen.py` 11, `RUN rm orig_plaintexts.txt` 13, `RUN rm gen.py` 14; `test.sh` — pytest 22, `if [ $? -eq 0 ]` 25, reward writes 26/28; `task.toml` — `timeout_sec = 1800.0` 22, `docker_image = …` 29, `allow_internet = true` 34; `README.md` — 32 (membership sentence), 22 (timeouts); `instruction.md` — 4-6 (20-bit seed hint), 7 (known-plaintext), 8-10 (decrypt all into `/app/plaintexts.txt`).
7. Labels: a `python3` read of the receipt + the frozen tag lines reproduced `derive()` (`plans/round44_c2_verify.py:228-233`) — `known-plaintext-attack 6 cases 3 pass`, `recover-key 7/3`, `decrypt-all 7/2`, `plaintexts-file 1/0`.
8. Gate/counter clauses: `sed -n '233-260p' plans/pkg_gate.py`; `sed -n '285-320p' plans/round44_c2_verify.py` (`TASK = "feal-linear-cryptanalysis"` at `:83`, V9 at `:287-317`); `sed -n '520,549p' plans/round44_c2_verify.py` (checks list, exits 0/1, argparse 2); `sed -n '1,48p' plans/feal_linear_probe.py` (exit contract, limits).
9. SOURCES state: `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → `130`; `grep -c "S138" corpus/SOURCES.md` → `0`; last rows `S136`, `S137` — so S138–S146 do not exist yet.
10. Sibling sweep (fleet root, 2026-10-26): `for pat in "cryptanalys" "linear cryptanalysis" "known-plaintext" "hash chain"; do printf '%s -> ' "$pat"; hits=$(grep -lri "$pat" --include=PROVINCE.md ./*/PROVINCE.md 2>/dev/null | tr '\n' ' '); echo "${hits:-<none>}"; done` → `cryptanalys -> ./kengaku-shokunin/PROVINCE.md`, the other three `<none>`. Sibling ownership citations: `PROVINCE.md:136-143` (Adjacent table: chousa 137, kotoba 138, protocol/aggregator 139), `tameshi-shokunin/PROVINCE.md:3-4` (domain sentence).

## Findings / conflicts (verbatim, for the canonical judge)

1. **Claim line number vs capture.** `plans/round-44-claims.md` §C2 says "gen.py is deleted from the image
   (Dockerfile:12-13)". The capture has `RUN python3 gen.py` at `Dockerfile:11`, `RUN rm orig_plaintexts.txt` at
   `:13` and `RUN rm gen.py` at `:14`. My blocks cite `Dockerfile:14` for the gen.py deletion. Not a change to the
   frozen file; reported, not edited.
2. **Claim wording vs capture.** The claims and the probe case line say the four round keys are "printed in the
   public gen.py:12". In the capture `gen.py:12` *defines* them as literals (`keys = ["0x68e63", …]`); `gen.py`
   prints only counts (`:52`, `:92-93`). My blocks say the keys are "literals in the published `gen.py:12`", which
   is the observable fact.
3. **Confirmed exactly.** `test_outputs.py:4-103` holds 100 decimal constants; `:120` is
   `data = open("/app/plaintexts.txt").read()`; `:121-122` are `for c in soln.split():` / `assert c in data`; the
   receipt's `cases=14 observed_pass=8 observed_fail=6 mismatches=0` and `regrade cases=14 differ=0` reproduce on a
   plain read; `test.sh:25-26` is `if [ $? -eq 0 ]; then / echo 1 > /logs/verifier/reward.txt`.
4. **Receipt line numbering used by round 43 differs by one file.** Round-43 prose cites `receipt:11` for
   `oracle-solve-sh`, `:15-21` for the cheat passes, on a 12-case receipt whose CASE lines start at 10. Here the CASE
   lines start at 9, so the same shapes sit one line earlier; my cites are the round-44 receipt's own numbers.
5. **`corpus/SOURCES.md` holds 130 rows, last `S137`.** S138–S146 are absent today, so the registry rows are the
   L1's (the spec names `sources: corpus/SOURCES.md` but supplies only the digests at `plans/pkg-spec-r44.json`).
6. **No `### Round-44 evidence` section exists in `corpus/README.md`** (the file ends with `### Round-43 evidence` at
   556-560). Out of scope for this seat; the L1's landing will need one for the captures and the receipt.
7. **The nine-case count of sibling ownership is unchanged.** The sweep finds no sibling declaring cryptanalysis,
   linear cryptanalysis, known-plaintext or hash-chain work, so the routing clause routes to the orchestrator and
   credits no sibling with the subject — matching the round-43 routing paragraph it sits under.

## Out of scope (untouched, by rule)

`corpus/SOURCES.md` rows S138–S146; the entry `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md` itself
(Case table, Mechanism, Requirement map, Located quotes, Predictor); `corpus/README.md`'s Round-44 evidence section;
`SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md` and `PROVINCE.md` as files (all blocks above are drafts for the L1);
any counter, battery, probe, fixture, clone or git/jj operation. No tool was installed or upgraded this seat.

## Artifact paths

- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44PkgProse.md`
- Seat subdir (empty; the blocks are inline above so they cannot drift from a second copy):
  `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44PkgProse/`
- No scratch dir was created: nothing was written outside the two paths above.

VERDICT: prose-blocks-6
