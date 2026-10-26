# F39RevErrata — receipts (command → output, 2026-10-26)

Fixture: `S=/fast/scratch/hyaku/kengaku-r39/F39RevErrata`; `git clone -q --no-local` of the lane, `checkout -q a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`;
`git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r39/F39RevErrata/lane`; `rev-parse HEAD` → `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`;
`git cat-file -t 088f7c36…` → `commit`; `git merge-base --is-ancestor 088f7c36… a6832f53…` → rc 0 ("freeze-is-ancestor: yes").
`TMPDIR="$S"` exported for every counter run. Scratch removed after receipts were copied here. No installs performed this session.

## 1. Append-only (freeze 088f7c36 → tip a6832f53)

```
$ git -C "$S/lane" diff --numstat 088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8 a6832f53c1a94bb092a6cfd79fb4e449f2d4054c -- \
    corpus/lessons/round-38.md corpus/knowledge/tb2-regex-log-grader.md \
    corpus/knowledge/tb2-git-webserver-grader.md corpus/knowledge/tb2-build-pmars-grader.md
42	0	corpus/knowledge/tb2-build-pmars-grader.md
25	0	corpus/knowledge/tb2-git-webserver-grader.md
26	0	corpus/knowledge/tb2-regex-log-grader.md
30	0	corpus/lessons/round-38.md

$ git -C "$S/lane" log --oneline 088f7c36…a6832f53… -- <same four paths>
34158b0 round-39: battery39 (4 modules), C2 package (entry, S117/S118, README, PROVINCE, SKILL), routed fixes (order gate, anchor, ledger-tip, direction check), Q30, errata, post-hoc C1 audit, wave-1 reports
```

0 removed lines in all four files; one commit.

## 2. Corrected recheck one-liners, run verbatim from the clone root (exit codes at the RC-MARKERs)

- regex-log → rc=0: `test_outputs.py: OK / test.sh: OK / instruction.md: OK` (refetch) + 5/5 capture OK;
  `grader=… sha256=345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72 pin=2fd12b88…`;
  `cases=24 observed_pass=8 observed_fail=16 mismatches=0`.
  Determinism leg: `python3 plans/regex_log_probe.py --lane . > rerun.txt; diff rerun.txt corpus/evidence/round36/regex-log-probe.txt` → rc 0, `diff bytes: 0`.
- git-webserver → rc=0: 3/3 refetch OK + 6/6 capture OK; `cases=22 observed_pass=9 observed_fail=13 mismatches=0`;
  probe `--work` re-run diff vs `corpus/evidence/round37/git-webserver-probe.txt` → rc 0, 0 bytes.
- build-pmars → rc=0: 2/2 refetch OK + 5/5 capture OK; `cases=22 observed_pass=7 observed_fail=15 mismatches=0`;
  probe `--work` re-run diff vs `corpus/evidence/round38/build-pmars-probe.txt` → rc 0, 0 bytes.
- build-pmars TB2.1 pin check (`terminal-bench-2-1 @ 7131e437…`) → rc=0, digests match the erratum table line for line:
  `d9d2796d…4e85` test_outputs.py, `4770437e…c334` test.sh, `7ee2eac2…c9cd` task.toml, `dd4a3aa7…215e` instruction.md,
  `111b4e53…713f` solution/solve.sh, `ff0a9f76…8b25` environment/Dockerfile.

## 3. Red legs of the superseded `recheck:` lines (from the clone root)

```
$ sha256sum -c corpus/evidence/round36/tb2-regex-log/SHA256SUMS   # → 5× FAILED open or read, WARNING 5 listed, rc=1
$ sha256sum -c corpus/evidence/round37/tb2-git-webserver/SHA256SUMS  # → 6× FAILED, WARNING 6 listed, rc=1
$ sha256sum -c corpus/evidence/round38/tb2-build-pmars/SHA256SUMS    # → 5× FAILED, WARNING 5 listed, rc=1
```
Each matches its erratum's quoted failure exactly. Old lines still at regex-log `:5`, webserver `:6`, pmars `:4`
(`grep -n '^recheck: 180d'` over corpus/knowledge), matching the "replaces :5/:6/:4" anchors.

## 4. round-38.md lesson errata — citations

```
$ grep -n "Rule forward: a control that executes" corpus/lessons/round-37.md        → :42 (exact sentence)
$ grep -n "discarded unread" plans/round-38-claims.md                               → :10-11 (exact sentence)
$ grep -n "does not prevent the ordering" corpus/lessons/round-38.md                → :36 (superseded cell, exact)
$ grep -c census plans/round-38-claims.md                                           → 0
$ grep -n "baseline, not a control" corpus/lessons/round-39.md                      → :13
$ grep -n "fresh probe" .ufo/waves/round-38/claims/control-c2-skip.txt              → :11 P10 DEFECT line
$ git cat-file -e e0a37853:corpus/evidence/round38/build-pmars-probe.txt            → rc=128
$ git ls-tree -r 088f7c36 --name-only -- .ufo/waves/round-39/                       → 7 files, none asserts a run
.census-before.txt, control-c1-gate-edited.txt, control-c1-hostile-inproc-module.py,
control-c1-hostile-inproc.txt, control-c1-nothing.txt, control-c2-nothing.txt, frozen-digests.txt
```
census-before.txt read whole: 15 `W04` rows (S040…S100), last lines `kengaku ok …/corpus/SOURCES.md`, `exit=0`.
Wave-1 pair-check receipt: `.ufo/waves/round-39/build/R39LessonErrata/receipts.md` §C1/C2 (red at e0a37853, green at 088f7c36) read; §C1's rc=128 independently reproduced above.

## 5. Protein claim — baseline, append reproduction, restore

Baseline (clean clone, tip):
```
$ python3 plans/round38_c1_verify.py --lane .            # r38-baseline.txt, rc=1
PINS total=14 mismatched=0
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N21 D5 silence SURVIVED …
MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0
PREDICATE C1 fail
```
Same predicate as the disclosed landing measurement (`integrate/measure-final.txt:360-362`: `killed=21 survived=1`, `PREDICATE C1 fail`, `exit=1`; N21 direction documented at `corpus/lessons/round-38.md:35`). All p7m fixtures `ok` (baseline :87).

Append (reproduction block `append-block.md`, +4 `recheck:` tokens; occurrences `grep -o 'recheck:' | wc -l` before=1 after=5):
```
$ cat "$S/append-block.md" >> corpus/knowledge/tb2-protein-assembly-grader.md
$ python3 plans/round38_c1_verify.py --lane .            # r38-append.txt, rc=1, 4.7s
RuntimeError: expected exactly one 'recheck:', found 5   # raised at plans/battery38/p7m.py:38 via _n11/_package
$ python3 plans/round39_c1_verify.py --lane .            # r39-append.txt, rc=2
PINS total=26 mismatched=0
SETUP module battery38/p7m.py failed to build (rc=1): … RuntimeError: expected exactly one 'recheck:', found 5
```
Wrappers: `plans/round39_c1_verify.py:204` (child build raise) → `:288-290` (`print(f"SETUP {e}", …); return 2`). The round-38
counter has no SETUP wrapper (uncaught traceback, exit 1) — both counters and the gate are byte-unchanged since the freeze
(`git log 088f7c36…a6832f53 -- plans/round38_c1_verify.py plans/round39_c1_verify.py plans/pkg_gate.py` → empty).

Restore: `cp "$S/protein-entry.orig" <entry>` after each run; `git -C "$S/lane" status --porcelain -- <entry>` → empty both times.
Tip state corroboration: `grep -c 'recheck:' corpus/knowledge/tb2-protein-assembly-grader.md` → `1` (the L1 append was never committed, per `corpus/lessons/round-39.md:44` fix cell "reverted from the branch … never committed").

## Files copied out of scratch before removal

`r38-baseline.txt`, `r38-append.txt`, `r39-append.txt`, `regex-log-rerun.diff` (0 bytes),
`git-webserver-rerun.diff` (0 bytes), `build-pmars-rerun.diff` (0 bytes), `append-block.md`, `protein-entry.orig`.
