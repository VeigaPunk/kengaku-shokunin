# Item 4 — `PROVINCE.md` grader-class paragraph (round 45)

**Surface:** `PROVINCE.md` (644 lines). Shape as it actually stands, read not assumed
(`grep -n "Round" PROVINCE.md`): rounds 35–43 each open a `## RoundNN partial frontier admission (2026-10-26)`
section (`## Round43 …` at `:570`), and **round 44 broke that habit**: it is a single bold-led paragraph appended
at EOF (`:644`), with no `## Round44` heading. The model the assignment names — the round-44 paragraph — is that
paragraph. Rounds 35–43 also carry prose `Round-NN routing` blocks (`Round-43 routing` at `:622`); round 44 has
none.

**Anchor (byte-exact, end of file):**

```
file: PROVINCE.md
lines: 644 is the last line (644 lines total); it ends `\\n` after `…are not this lane's.`
line 644 (sha256 d0701d0c04c417af508203d880519a54c8fdd2754e5cf1210cb333da97f159d0):
      **Round 44 (2026-10-26).** `knowledge/tb2-feal-linear-cryptanalysis-grader.md` reads and executes a tenth
      Terminal-Bench 2.0 task's scoring code — `feal-linear-cryptanalysis/tests/test_outputs.py` @ `2fd12b88`
      with `tests/test.sh`, `instruction.md`, `environment/task-deps/gen.py`, `environment/task-deps/decrypt.c`,
      `environment/Dockerfile`, `README.md`, `solution/solve.sh` and `task.toml` (S138-S146) — over 14 frozen end
      states (…). The graded artefact is an agent-written text file checked by 100 embedded decimal constants as
      substrings: one function, one bit of reward. Advising an agent how to attack this cipher, and prior-art
      pricing of linear cryptanalysis on FEAL, are not this lane's.
```

**Edit:** append one blank line, then the new paragraph, at EOF. The paragraph is **one physical line** — this is
a hard requirement, not style: `plans/round45_c2_verify.py:326-327` checks
`any(TASK in l and name in l for l in province.splitlines())`, i.e. `password-recovery` **and**
`tb2-password-recovery-grader.md` must land on the *same* line. A wrapped paragraph can fail V9.

```diff
@@ PROVINCE.md:644 (EOF) @@
 … pricing of linear cryptanalysis on FEAL, are not this lane's.
+
+**Round 45 (2026-10-26).** `knowledge/tb2-password-recovery-grader.md` reads and executes an eleventh Terminal-Bench 2.0 task's scoring code — `password-recovery/tests/test_outputs.py` @ `2fd12b88` with `tests/test.sh`, `instruction.md`, `environment/setup.sh`, `environment/Dockerfile`, `README.md`, `solution/solve.sh` and `task.toml` (S149-S156) — over 16 frozen end states (`cases=16 observed_pass=<<P>> observed_fail=<<F>> mismatches=0`, `regrade cases=16 differ=0`). The graded artefact is an agent-written guess list checked by exact whole-line membership of one embedded 23-character constant, with no format, case, order, count or uniqueness check: one assertion that can fire and one dead one, one bit of reward, and the constant published by the task's own `README.md:31` and seeded by `setup.sh:25`. Advising an agent how to recover a deleted file from a disk image, and prior-art pricing of forensic recovery tooling, are not this lane's.
```

**Optional closing sentence** (round-43 paragraphs carry a limits sentence, round-44's does not — the frozen
claims demand none, so this is the L1's call). If wanted, append to the *same* line before `Advising`:

```
It does not run Terminal-Bench, the task image (`task.toml:29` names `alexgshaw/password-recovery:20251031`; `allow_internet = true` at `:34`; the image is never pulled) or a harness (`tests/test.sh:18-22`'s uvx/pytest invocation and `:25-28`'s `/logs/verifier/reward.txt` write are read, not run), does not measure difficulty, gameability or contamination, and does not speak for the remaining 78 TB2 task graders (89 carry `tests/test.sh`; 11 are read).
```

**Substitution `<<P>>` / `<<F>>`:** the same two numbers as item 2, taken from the probe receipt's
`cases=16 observed_pass=P observed_fail=F mismatches=0` line. The three round-45 surfaces (frontier bullet,
coverage bullet's sibling counts, PROVINCE paragraph) must agree with the receipt; paste the receipt first, then
copy.

**Attribution note:** the paragraph names an entry file another seat writes
(`corpus/knowledge/tb2-password-recovery-grader.md`). Paste this paragraph only when that file exists —
`plans/pkg_gate.py`'s `knowledge files == index rows` check (P8) will otherwise go red on the README side, which
is item 1.

**Heading decision (no extra prose needed from me):** do **not** add a `## Round45 partial frontier admission
(2026-10-26)` heading to match `:570`-style rounds. Round 44 set the current precedent — paragraph only, no
heading — and a heading line would also cost a second line that cannot carry both `password-recovery` and the
entry name for V9. If the L1 wants the heading for symmetry, put the paragraph immediately under it and keep the
paragraph itself one line; V9 reads the whole file, so a heading neither helps nor hurts it.
