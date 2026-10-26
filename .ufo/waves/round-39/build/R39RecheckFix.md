# R39RecheckFix — round-38 closure R4: the four TB2 `recheck:` lines that red as written

Seat `R39RecheckFix` (scribe), kengaku round 39 wave 1, 2026-10-26. Item: round-38 closure
`corpus/lessons/round-38-verifier-spotcheck.md:166` (R4) plus its second half F38R-3 (TB2.1 comparison unpinned,
`F38ReopenRows` §5).

**Measured against** lane tip `750473847af9c7a461487ba3a589b5519fac5ed8` (clone HEAD; the dispatch names
`b2bdd425` as the round-39 baseline and `088f7c36` as the claims freeze — `git merge-base --is-ancestor <h> HEAD`
→ ok for `b2bdd425`, `088f7c36` and `6a1eb5e1`; tip subject `round-39: wave-1 spec and validated dispatch (36
seats, policy v1)`) in a clean
`git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane`,
`git -C $S/lane rev-parse --show-toplevel` → `$S/lane`, `git status --porcelain --untracked-files=all | wc -l` → `0`
before and after every run below. `S=/fast/scratch/hyaku/kengaku-r39/R39RecheckFix` (removed at exit).
**No lane file was written** — every correction here is a draft for the L1.

Axes named: **operability** (a follower's recheck is false-red today — the axis R4 sits on), **freshness** (the
recheck is the freshness instrument; F38R-3 is its unpinned leg), **quality** (the correction must not move a label
or a verdict). No score claim; nothing frozen touched (the gate, both counters, probe, spec, dry table, captures
and receipt are read-only here).

## 1. Verdict table — four entries, four reds, four green fixes

| # | entry | `recheck:` at | broken leg (verbatim from the entry) | red | corrected one-liner green |
|---|---|---|---|---|---|
| 1 | `corpus/knowledge/tb2-protein-assembly-grader.md` | `:5` | `sha256sum -c corpus/evidence/round35/tb2-eval/SHA256SUMS` | exit 1, 6 files unreadable | exit 0, 5/5 refetch + 6/6 capture + `cases=18 observed_pass=5 observed_fail=13 mismatches=0` |
| 2 | `corpus/knowledge/tb2-regex-log-grader.md` | `:5` | `sha256sum -c corpus/evidence/round36/tb2-regex-log/SHA256SUMS` | exit 1, 5 files unreadable | exit 0, 3/3 + 5/5 + `cases=24 observed_pass=8 observed_fail=16 mismatches=0` |
| 3 | `corpus/knowledge/tb2-git-webserver-grader.md` | `:6` | `sha256sum -c corpus/evidence/round37/tb2-git-webserver/SHA256SUMS` | exit 1, 6 files unreadable | exit 0, 3/3 + 6/6 + `cases=22 observed_pass=9 observed_fail=13 mismatches=0` |
| 4 | `corpus/knowledge/tb2-build-pmars-grader.md` | `:4` | `sha256sum -c corpus/evidence/round38/tb2-build-pmars/SHA256SUMS` | exit 1, 5 files unreadable | exit 0, 2/2 + 5/5 + `cases=22 observed_pass=7 observed_fail=15 mismatches=0` |

Cause, one sentence: the four TB2 captures use the upstream manifest convention (bare basenames), so `sha256sum -c`
resolves every name against the CWD — the lane root — while the files live in the capture directory. The lane's own
manifests use repo-root-relative paths and are unaffected (`sha256sum -c corpus/evidence/round12-ladder/prereg-bundle.sha256`
→ `corpus/evidence/round12-ladder/precheck_r12.py: OK`, exit 0; `head -2` shows the prefixed paths).

Nothing was superseded: every probe re-run is **byte-equal** to the committed receipt, and every refetched pinned
file matches its manifest digest (§3), so the four entries' claims stand as filed.

## 2. Ran each recheck line verbatim from the clean clone root — output pasted

```
$ cd $S/lane && sha256sum -c corpus/evidence/round35/tb2-eval/SHA256SUMS
sha256sum: test_outputs.py: No such file or directory (os error 2)
test_outputs.py: FAILED open or read
sha256sum: test.sh: No such file or directory (os error 2)
test.sh: FAILED open or read
sha256sum: instruction.md: No such file or directory (os error 2)
instruction.md: FAILED open or read
sha256sum: task.toml: No such file or directory (os error 2)
task.toml: FAILED open or read
sha256sum: antibody.fasta: No such file or directory (os error 2)
antibody.fasta: FAILED open or read
sha256sum: pdb_ids.txt: No such file or directory (os error 2)
pdb_ids.txt: FAILED open or read
sha256sum: WARNING: 6 listed file(s) could not be read
exit=1
```

```
$ sha256sum -c corpus/evidence/round36/tb2-regex-log/SHA256SUMS      # test_outputs.py test.sh instruction.md task.toml solve.sh FAILED open or read
sha256sum: WARNING: 5 listed file(s) could not be read
exit=1
$ sha256sum -c corpus/evidence/round37/tb2-git-webserver/SHA256SUMS # instruction.md solve.sh task.toml test.sh test_outputs.py verify.sh FAILED open or read
sha256sum: WARNING: 6 listed file(s) could not be read
exit=1
$ sha256sum -c corpus/evidence/round38/tb2-build-pmars/SHA256SUMS   # instruction.md solve.sh task.toml test.sh test_outputs.py FAILED open or read
sha256sum: WARNING: 5 listed file(s) could not be read
exit=1
```

(The three abbreviated blocks are byte-identical in shape to the first, `2` lines per file; full stdout is in
`R39RecheckFix/recheck-red-verbatim.txt` beside this report.)

**Entry 1 has a second red leg.** Its recheck says "re-run `plans/tb2_grader_probe.py`" with no interpreter and no
environment, and the script is executable, so the bare form runs — and fails on the dependency the probe's own
docstring pins:

```
$ plans/tb2_grader_probe.py
  File ".../plans/tb2_grader_probe.py", line 145, in main
    import Bio  # noqa: F401  (fail loudly if Biopython is absent)
ModuleNotFoundError: No module named 'Bio'
exit=1
```

`plans/tb2_grader_probe.py:12` carries the fix already: `uv run --no-project --with biopython==1.85 python3
plans/tb2_grader_probe.py --lane .`. The other three recheck probe legs are sound as written
(`plans/build_pmars_probe.py --lane .` exit 0, `plans/regex_log_probe.py --lane .` exit 0, both executable with
shebangs and both self-managing their scratch when `--work` is omitted; `--work <missing dir>` does red —
`FileNotFoundError` — so the corrected lines create the directory first).

## 3. Corrected one-liners, run green

All four are one line each (bash, from the lane root), 539–660 characters, and each does the three things its entry
promised: re-fetch the pinned files and check them against the manifest, check the capture manifest, re-run the
probe. `TMPDIR` was `$S`.

**1 — protein-assembly (exit 0):**

```
T=$(mktemp -d) && B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly && for p in tests/test_outputs.py tests/test.sh instruction.md environment/antibody.fasta environment/pdb_ids.txt; do curl -fsS "$B/$p" -o "$T/$(basename "$p")"; done && grep -E ' (test_outputs\.py|test\.sh|instruction\.md|antibody\.fasta|pdb_ids\.txt)$' corpus/evidence/round35/tb2-eval/SHA256SUMS > "$T/SUB" && (cd "$T" && sha256sum -c SUB) && (cd corpus/evidence/round35/tb2-eval && sha256sum -c SHA256SUMS) && uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane . && rm -rf "$T"
```

```
test_outputs.py: OK
test.sh: OK
instruction.md: OK
antibody.fasta: OK
pdb_ids.txt: OK
test_outputs.py: OK
test.sh: OK
instruction.md: OK
task.toml: OK
antibody.fasta: OK
pdb_ids.txt: OK
grader=corpus/evidence/round35/tb2-eval/test_outputs.py sha256=44a05a24…096582 pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6 biopython=1.85
components_aa=8,259,158,235,182 max_passing_nt=2766 cap_nt=3000
cases=18 observed_pass=5 observed_fail=13 mismatches=0
exit=0
```

**2 — regex-log (exit 0):**

```
T=$(mktemp -d) && B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log && for p in tests/test_outputs.py tests/test.sh instruction.md; do curl -fsS "$B/$p" -o "$T/$(basename "$p")"; done && grep -E ' (test_outputs\.py|test\.sh|instruction\.md)$' corpus/evidence/round36/tb2-regex-log/SHA256SUMS > "$T/SUB" && (cd "$T" && sha256sum -c SUB) && (cd corpus/evidence/round36/tb2-regex-log && sha256sum -c SHA256SUMS) && python3 plans/regex_log_probe.py --lane . && rm -rf "$T"
```

```
test_outputs.py: OK
test.sh: OK
instruction.md: OK
test_outputs.py: OK
test.sh: OK
instruction.md: OK
task.toml: OK
solve.sh: OK
grader=corpus/evidence/round36/tb2-regex-log/test_outputs.py sha256=345c3bd0…855e8f72 pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6
cases=24 observed_pass=8 observed_fail=16 mismatches=0
exit=0
```

**3 — git-webserver (exit 0):**

```
T=$(mktemp -d) && B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver && for p in tests/test_outputs.py tests/verify.sh instruction.md; do curl -fsS "$B/$p" -o "$T/$(basename "$p")"; done && grep -E ' (test_outputs\.py|verify\.sh|instruction\.md)$' corpus/evidence/round37/tb2-git-webserver/SHA256SUMS > "$T/SUB" && (cd "$T" && sha256sum -c SUB) && (cd corpus/evidence/round37/tb2-git-webserver && sha256sum -c SHA256SUMS) && mkdir -p "$T/w" && python3 plans/git_webserver_probe.py --lane . --work "$T/w" && rm -rf "$T"
```

```
instruction.md: OK
test_outputs.py: OK
verify.sh: OK
instruction.md: OK
solve.sh: OK
task.toml: OK
test.sh: OK
test_outputs.py: OK
verify.sh: OK
cases=22 observed_pass=9 observed_fail=13 mismatches=0
exit=0
```

**4 — build-pmars (exit 0):**

```
T=$(mktemp -d) && B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/build-pmars && for p in tests/test_outputs.py instruction.md; do curl -fsS "$B/$p" -o "$T/$(basename "$p")"; done && grep -E ' (test_outputs\.py|instruction\.md)$' corpus/evidence/round38/tb2-build-pmars/SHA256SUMS > "$T/SUB" && (cd "$T" && sha256sum -c SUB) && (cd corpus/evidence/round38/tb2-build-pmars && sha256sum -c SHA256SUMS) && mkdir -p "$T/w" && python3 plans/build_pmars_probe.py --lane . --work "$T/w" && rm -rf "$T"
```

```
instruction.md: OK
test_outputs.py: OK
instruction.md: OK
solve.sh: OK
task.toml: OK
test.sh: OK
test_outputs.py: OK
cases=22 observed_pass=7 observed_fail=15 mismatches=0
exit=0
```

**Minimal variant of the broken leg** (F38R-2's own recommendation, run green for all five captures incl. round 39):
`(cd corpus/evidence/<dir> && sha256sum -c SHA256SUMS)` → `6/6 OK` (round35/tb2-eval), `5/5` (round36),
`6/6` (round37), `5/5` (round38), `7/7` (round39/tb2-git-leak-recovery), each exit 0.

**Probe receipts reproduce byte-for-byte** (`cmp` in the clone, receipt path vs a fresh run under `$S`):
`regex_log_probe.out` → `BYTE-EQUAL`, `git_webserver_probe.out` → `BYTE-EQUAL`, `build_pmars_probe.out` →
`BYTE-EQUAL`, `protein.out` → `BYTE-EQUAL`. No receipt or digest change; nothing superseded.

**Refetch leg (all 11 pinned raw files identical to their manifests):**

```
44a05a24…096582 protein-assembly/tests/test_outputs.py      9ede4664…c267b5 protein-assembly/tests/test.sh
1bb2af1d…b003f7c5 protein-assembly/instruction.md           345c3bd0…855e8f72 regex-log/tests/test_outputs.py
4770437e…16e6c334 regex-log/tests/test.sh                    4f7ac05e…2e96f9c regex-log/instruction.md
526aee3d…3346b37 configure-git-webserver/tests/test_outputs.py  1dc44c92…2f53d05 configure-git-webserver/tests/verify.sh
62151b73…63cf1d97 configure-git-webserver/instruction.md     d9d2796d…b01f4e85 build-pmars/tests/test_outputs.py
16068505…fbcf3b82 build-pmars/instruction.md
```

## 4. Draft `## Errata (round 39)` per entry — paste at EOF, append-only

### 4a. `corpus/knowledge/tb2-protein-assembly-grader.md`

```markdown
## Errata (round 39)

Appended 2026-10-26 (round 39, wave 1, seat `R39RecheckFix`; round-38 closure R4). Append-only: the bytes above
stand as filed; this section is the correction of record. Every line below was measured in a clean
`git clone --shared` of the lane at `75047384` (`git status --porcelain --untracked-files=all | wc -l` → `0`), run
from that clone's root.

**Erratum (round 39): the `recheck:` line reds as written.** `corpus/evidence/round35/tb2-eval/SHA256SUMS` lists
**bare basenames**, so `sha256sum -c` resolves them against the CWD, not the manifest's directory: the `recheck:`
command exits 1 with `sha256sum: WARNING: 6 listed file(s) could not be read` and `test_outputs.py: FAILED open or
read` (and the same for all six). The capture is intact — the digests were never wrong. Corrected leg:
`(cd corpus/evidence/round35/tb2-eval && sha256sum -c SHA256SUMS)` → 6/6 `OK`, exit 0.

**Erratum (round 39): the probe leg names no interpreter and no environment.** The recheck says "re-run
`plans/tb2_grader_probe.py`"; run as-is it exits 1 with `ModuleNotFoundError: No module named 'Bio'`, because the
grader imports Biopython. The recipe is the probe docstring's (`plans/tb2_grader_probe.py:11-12`):
`uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .`.

**Corrected `recheck:` line (replaces `:5`, one line):**

    recheck: 180d — at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`: re-fetch the three pinned URLs, `(cd corpus/evidence/round35/tb2-eval && sha256sum -c SHA256SUMS)`, and re-run `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .`; the full one-liner is under `## Errata (round 39)`; any digest or receipt change supersedes this entry

**Full recheck one-liner (run from the lane root, bash; verified exit 0 on 2026-10-26):**

    T=$(mktemp -d) && B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly && for p in tests/test_outputs.py tests/test.sh instruction.md environment/antibody.fasta environment/pdb_ids.txt; do curl -fsS "$B/$p" -o "$T/$(basename "$p")"; done && grep -E ' (test_outputs\.py|test\.sh|instruction\.md|antibody\.fasta|pdb_ids\.txt)$' corpus/evidence/round35/tb2-eval/SHA256SUMS > "$T/SUB" && (cd "$T" && sha256sum -c SUB) && (cd corpus/evidence/round35/tb2-eval && sha256sum -c SHA256SUMS) && uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane . && rm -rf "$T"

Green on 2026-10-26: 5/5 refetched files `OK` against the manifest, 6/6 capture files `OK`, then
`grader=… biopython=1.85`, `components_aa=8,259,158,235,182 max_passing_nt=2766 cap_nt=3000`,
`cases=18 observed_pass=5 observed_fail=13 mismatches=0`. The probe output is byte-equal to
`corpus/evidence/round35/tb2-grader-probe.txt`, so this entry's claims are unchanged by the correction.
```

### 4b. `corpus/knowledge/tb2-regex-log-grader.md`

```markdown
## Errata (round 39)

Appended 2026-10-26 (round 39, wave 1, seat `R39RecheckFix`; round-38 closure R4). Append-only: the bytes above
stand as filed; this section is the correction of record. Measured in a clean clone of the lane at `75047384`
(`git status --porcelain --untracked-files=all | wc -l` → `0`), run from its root.

**Erratum (round 39): the `recheck:` line reds as written — and so does the round-37 erratum that repeats it.**
`corpus/evidence/round36/tb2-regex-log/SHA256SUMS` lists bare basenames, so `sha256sum -c` resolves them against
the CWD: `sha256sum -c corpus/evidence/round36/tb2-regex-log/SHA256SUMS` printed `test_outputs.py: FAILED open or
read` (and the same for `test.sh`, `instruction.md`, `task.toml`, `solve.sh`) and
`sha256sum: WARNING: 5 listed file(s) could not be read`, exit 1. The same command string appears in the round-37
erratum (`:271`, "→ 5/5 `OK`, 2026-10-26"), which is the result of running it **inside** the capture directory;
read that occurrence as `(cd corpus/evidence/round36/tb2-regex-log && sha256sum -c SHA256SUMS)`. Corrected leg:
5/5 `OK`, exit 0.

**Corrected `recheck:` line (replaces `:5`, one line):**

    recheck: 180d — at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`: re-fetch the three pinned URLs, `(cd corpus/evidence/round36/tb2-regex-log && sha256sum -c SHA256SUMS)`, and re-run `python3 plans/regex_log_probe.py --lane .`; the full one-liner is under `## Errata (round 39)`; any digest or receipt change supersedes this entry

**Full recheck one-liner (lane root, bash; verified exit 0 on 2026-10-26):**

    T=$(mktemp -d) && B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log && for p in tests/test_outputs.py tests/test.sh instruction.md; do curl -fsS "$B/$p" -o "$T/$(basename "$p")"; done && grep -E ' (test_outputs\.py|test\.sh|instruction\.md)$' corpus/evidence/round36/tb2-regex-log/SHA256SUMS > "$T/SUB" && (cd "$T" && sha256sum -c SUB) && (cd corpus/evidence/round36/tb2-regex-log && sha256sum -c SHA256SUMS) && python3 plans/regex_log_probe.py --lane . && rm -rf "$T"

Green: 3/3 refetched `OK`, 5/5 capture `OK`, `grader=… sha256=345c3bd0…855e8f72 pin=2fd12b88…`,
`cases=24 observed_pass=8 observed_fail=16 mismatches=0`, byte-equal to `corpus/evidence/round36/regex-log-probe.txt`.
```

### 4c. `corpus/knowledge/tb2-git-webserver-grader.md`

```markdown
## Errata (round 39)

Appended 2026-10-26 (round 39, wave 1, seat `R39RecheckFix`; round-38 closure R4). Append-only: the bytes above
stand as filed; this section is the correction of record. Measured in a clean clone of the lane at `75047384`
(`git status --porcelain --untracked-files=all | wc -l` → `0`), run from its root.

**Erratum (round 39): the `recheck:` line reds as written.** `corpus/evidence/round37/tb2-git-webserver/SHA256SUMS`
lists bare basenames, so `sha256sum -c` resolves them against the CWD: the `recheck:` command printed
`instruction.md: FAILED open or read` (and the same for `solve.sh`, `task.toml`, `test.sh`, `test_outputs.py`,
`verify.sh`) plus `sha256sum: WARNING: 6 listed file(s) could not be read`, exit 1. Corrected leg:
`(cd corpus/evidence/round37/tb2-git-webserver && sha256sum -c SHA256SUMS)` → 6/6 `OK`, exit 0. The probe leg is
sound as written (`plans/git_webserver_probe.py --lane .`, exit 0).

**Corrected `recheck:` line (replaces `:6`, one line):**

    recheck: 180d — at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`: re-fetch the three pinned URLs, `(cd corpus/evidence/round37/tb2-git-webserver && sha256sum -c SHA256SUMS)`, and re-run `python3 plans/git_webserver_probe.py --lane .`; the full one-liner is under `## Errata (round 39)`; any digest or receipt change supersedes this entry

**Full recheck one-liner (lane root, bash; verified exit 0 on 2026-10-26):**

    T=$(mktemp -d) && B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver && for p in tests/test_outputs.py tests/verify.sh instruction.md; do curl -fsS "$B/$p" -o "$T/$(basename "$p")"; done && grep -E ' (test_outputs\.py|verify\.sh|instruction\.md)$' corpus/evidence/round37/tb2-git-webserver/SHA256SUMS > "$T/SUB" && (cd "$T" && sha256sum -c SUB) && (cd corpus/evidence/round37/tb2-git-webserver && sha256sum -c SHA256SUMS) && mkdir -p "$T/w" && python3 plans/git_webserver_probe.py --lane . --work "$T/w" && rm -rf "$T"

Green: 3/3 refetched `OK`, 6/6 capture `OK`, `cases=22 observed_pass=9 observed_fail=13 mismatches=0`, byte-equal
to `corpus/evidence/round37/git-webserver-probe.txt`. `--work` must be an existing directory (a missing one raises
`FileNotFoundError`); omitting `--work` also works.
```

### 4d. `corpus/knowledge/tb2-build-pmars-grader.md` — R4 **and** F38R-3

```markdown
## Errata (round 39)

Appended 2026-10-26 (round 39, wave 1, seat `R39RecheckFix`; round-38 closure R4 and F38R-3). Append-only: the
bytes above stand as filed; this section is the correction of record. Measured in a clean clone of the lane at
`75047384` (`git status --porcelain --untracked-files=all | wc -l` → `0`), run from its root.

**Erratum (round 39): the `recheck:` line reds as written.** `corpus/evidence/round38/tb2-build-pmars/SHA256SUMS`
lists bare basenames, so `sha256sum -c` resolves them against the CWD: the `recheck:` command printed
`instruction.md: FAILED open or read` (and the same for `solve.sh`, `task.toml`, `test.sh`, `test_outputs.py`) plus
`sha256sum: WARNING: 5 listed file(s) could not be read`, exit 1. Corrected leg:
`(cd corpus/evidence/round38/tb2-build-pmars && sha256sum -c SHA256SUMS)` → 5/5 `OK`, exit 0.

**Erratum (round 39, F38R-3): the TB2.1 comparison is now pinned.** The prior-art bullet "Upstream changed the
instruction, not the grader" compared against a moving branch. Pinned ref
`7131e4375048a0e408a8fb404b5f499d726b695b` (`tasks/build-pmars`, terminal-bench-2-1; `git ls-remote` HEAD on
2026-10-26). Measured at that ref:

| file | sha256 | vs TB2.0 pin |
|---|---|---|
| `tests/test_outputs.py` | `d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85` | **SAME** |
| `tests/test.sh` | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` | SAME |
| `task.toml` | `7ee2eac27b99fd462e0760552a430454db693f86608af5bb570b020270e4c9cd` | SAME |
| `instruction.md` | `dd4a3aa762e6b3c09e67bd7f61d9b6afbe379dcd7297c2c0ebe2e9bd0082215e` | DIFFERS (line 3 only) |
| `solution/solve.sh` | `111b4e532ec411c9826cd67309f39efac21063e3a76d5cb268e62ce5fadc713f` | DIFFERS (apt pins dropped) |
| `environment/Dockerfile` | `ff0a9f766151b6304a33b8fe8787dc27d75f6ea679eec4e9a4f2c8876fe08b25` | SAME |

The grader byte-equality that the bullet rests on is confirmed; the requirement text is not, so no map label
transfers to TB2.1 unread. Pin check (lane root, one line, exit 0 on 2026-10-26):

    B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2-1/7131e4375048a0e408a8fb404b5f499d726b695b/tasks/build-pmars && for p in tests/test_outputs.py tests/test.sh task.toml instruction.md solution/solve.sh environment/Dockerfile; do printf '%s  %s\n' "$(curl -fsS "$B/$p" | sha256sum | cut -d' ' -f1)" "$p"; done

**Corrected `recheck:` line (replaces `:4`, one line):**

    recheck: 180d — at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`: re-fetch the two pinned URLs, `(cd corpus/evidence/round38/tb2-build-pmars && sha256sum -c SHA256SUMS)`, and re-run `python3 plans/build_pmars_probe.py --lane .`; the TB2.1 comparison is pinned at `7131e437` in `## Errata (round 39)`, which also carries the full one-liner; any digest or receipt change supersedes this entry

**Full recheck one-liner (lane root, bash; verified exit 0 on 2026-10-26):**

    T=$(mktemp -d) && B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/build-pmars && for p in tests/test_outputs.py instruction.md; do curl -fsS "$B/$p" -o "$T/$(basename "$p")"; done && grep -E ' (test_outputs\.py|instruction\.md)$' corpus/evidence/round38/tb2-build-pmars/SHA256SUMS > "$T/SUB" && (cd "$T" && sha256sum -c SUB) && (cd corpus/evidence/round38/tb2-build-pmars && sha256sum -c SHA256SUMS) && mkdir -p "$T/w" && python3 plans/build_pmars_probe.py --lane . --work "$T/w" && rm -rf "$T"

Green: 2/2 refetched `OK`, 5/5 capture `OK`, `cases=22 observed_pass=7 observed_fail=15 mismatches=0`, byte-equal
to `corpus/evidence/round38/build-pmars-probe.txt`.
```

## 5. F38R-3 answer — the comparison is pinned, not declined

Pinned by measurement, not by copying `F38ReopenRows`' table: I fetched all six files at
`7131e4375048a0e408a8fb404b5f499d726b695b` with `curl -fsS` (all HTTP 200), hashed them, and cross-checked the ref
with `git ls-remote https://github.com/harbor-framework/terminal-bench-2-1 HEAD` →
`7131e4375048a0e408a8fb404b5f499d726b695b`. Every digest reproduced the round-38 falsify seat's numbers exactly
(§4d table), including `test_outputs.py` = the TB2.0 capture digest `d9d2796d…`. Cheap, and it converts a re-diff
against `main` into a digest compare, which is what R4's whole item is about. Why pin rather than decline: the
entry's prior-art bullet rests on "byte-equal to S115", a fact about a *revision*; left as a branch it is
unfalsifiable the moment upstream touches the grader, and the fix costs one line.

## 6. Findings beyond the item

1. **R4 is 4 entries wide, and the same string appears a fifth time inside an admitted entry's errata.**
   `corpus/knowledge/tb2-regex-log-grader.md:271` files `sha256sum -c corpus/evidence/round36/…/SHA256SUMS` → "5/5
   `OK`". That number is right; the command is only right inside the capture directory. The draft in §4b corrects
   it by reading instruction rather than editing the round-37 bytes (append-only precedent).
2. **A fifth red that R4 did not name: the protein entry's probe leg.** `plans/tb2_grader_probe.py` needs
   Biopython; the entry names no environment, so the documented recheck exits 1 with `ModuleNotFoundError: No module
   named 'Bio'` on a host without it. The probe's own docstring carries the remedy. The other three probe legs are
   green as written (verified each, §2).
3. **`--work` semantics.** `git_webserver_probe.py` and `build_pmars_probe.py` raise
   `FileNotFoundError: … /k37-cgw-…` if `--work` names a directory that does not exist; both are green when it is
   created first or omitted. The corrected lines create it. Not a defect in the entries (they do not use `--work`)
   but it is the one way a follower can turn these rechecks red while trying to be careful.
4. **Pre-emptive: round 39's own capture has the same manifest shape.** `corpus/evidence/round39/tb2-git-leak-recovery/SHA256SUMS`
   lists seven bare basenames (verified `7/7 OK` from inside the directory, exit 0). The new entry
   `tb2-git-leak-recovery-grader.md` does not exist yet at this tip; when it is written, its `recheck:` should be
   born in the `(cd corpus/evidence/round39/tb2-git-leak-recovery && sha256sum -c SHA256SUMS)` form so this class
   stops at four.
5. **`QUALITY.md` Q21 passes lexically on a pin it does not name.** Its lint
   (`for f in corpus/knowledge/*.md; do … grep -qE '^recheck:.*(commit|pinned|pin|[0-9a-f]{7})' …`) is green for all
   four TB2 entries because their lines contain the word "pinned" — while the pin sha appears nowhere in the
   `recheck:` line. The drafts in §4 add `at pin `2fd12b88…`` for that reason. Not a new claim; the same hole Q21
   already names in its own Limits paragraph, demonstrated on four entries.
6. **The four entries' claims are intact.** Four probe re-runs byte-equal, eleven pinned raw files digest-equal,
   five capture manifests OK. The correction moves no label, no case and no verdict.

## 7. What this seat did not do

- **Did not edit any entry.** All five errata sections and the four replacement `recheck:` lines are drafts for the
  L1 (`KengakuR39`), as the lane bounds require.
- **Did not run the package gate or either counter.** Not my item; `pkg_gate.py`, `round39_c1_verify.py` and
  `round39_c2_verify.py` were not executed here, so the drafts' gate-compatibility is a claim I did not measure. The
  structural risk I can name statically: the appended sections add no `## Located quotes` row and no `## Negative
  space` heading, so P3/P4/P6/P7 parse the same text; P7's `^recheck:\s*\S` is satisfied by the one-line
  replacements; and the round-37/round-38 errata sections are the same shape, already green.
- **Did not test a cold `uv` cache.** The protein one-liner's `uv run --with biopython==1.85` resolved from the local
  cache in ~2 s; on a host without `uv` or without the wheel it needs network. Named as a limit, not measured.
- **Did not re-open TB2.1 beyond `tasks/build-pmars`** (six files at one ref), and did not re-derive any map label.

Tool installs: **none** (no package installed or upgraded; `uv` and `curl` were already present). Scratch
`/fast/scratch/hyaku/kengaku-r39/R39RecheckFix` removed at exit; receipts kept in this seat's subdir.

Receipts beside this report (`R39RecheckFix/`): `recheck-red-verbatim.txt` (full stdout of the four verbatim red
runs), `recheck-green.txt` (full stdout of the four corrected one-liners), `tb21-pin.txt` (the TB2.1 digest run),
`byte-equal.txt` (`cmp` results of the four probe re-runs), `lines.sh` (the four corrected one-liners as run).

VERDICT: recheck-red-4-fixed-4
