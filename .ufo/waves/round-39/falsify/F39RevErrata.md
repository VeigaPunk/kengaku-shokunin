# F39RevErrata — errata review (kengaku round 39, wave 2 falsify, 2026-10-26)

Seat: F39RevErrata (reviewer, leaf). Lane tip measured: `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` in a clean clone at
`/fast/scratch/hyaku/kengaku-r39/F39RevErrata/lane` (toplevel verified before any write; scratch removed after receipts
were copied out). Freeze `088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8` is a commit and an ancestor of the tip
(`merge-base --is-ancestor` → rc 0). Full command→output record: `F39RevErrata/receipts.md`. No tool installs this session.

## Scope

Four appended `## Errata (round 39)` blocks: `corpus/lessons/round-38.md`, `corpus/knowledge/tb2-regex-log-grader.md`,
`corpus/knowledge/tb2-git-webserver-grader.md`, `corpus/knowledge/tb2-build-pmars-grader.md`. Checks: (1) append-only
vs the freeze; (2) every corrected recheck command green as written from the clean clone root; (3) the lesson's claim
that appending to `tb2-protein-assembly-grader.md` breaks battery38 p7m, reproduced in the clone with the round-38 counter.

## F1 — Append-only: PASS (4/4)

`git diff --numstat 088f7c36… a6832f53… -- <4 files>` → `42 0`, `25 0`, `26 0`, `30 0` — **0 removed lines in all four**;
one commit (`34158b0`) touches them.

## F2 — Corrected recheck commands green as written: PASS (3/3 entries + pin check)

Ran each "Full recheck one-liner" verbatim, from the clone root, `TMPDIR` in scratch:

| entry | rc | refetch | capture | probe tail | "byte-equal to receipt" re-verified |
|---|---|---|---|---|---|
| tb2-regex-log | 0 | 3/3 OK | 5/5 OK | `cases=24 observed_pass=8 observed_fail=16 mismatches=0`, `sha256=345c3bd0…855e8f72` | probe re-run vs `corpus/evidence/round36/regex-log-probe.txt`: diff rc 0, 0 bytes |
| tb2-git-webserver | 0 | 3/3 OK | 6/6 OK | `cases=22 observed_pass=9 observed_fail=13 mismatches=0` | diff vs `round37/git-webserver-probe.txt`: rc 0, 0 bytes |
| tb2-build-pmars | 0 | 2/2 OK | 5/5 OK | `cases=22 observed_pass=7 observed_fail=15 mismatches=0` | diff vs `round38/build-pmars-probe.txt`: rc 0, 0 bytes |

- build-pmars TB2.1 pin check (`7131e437…`): rc 0; all six digests match the erratum's table exactly (test_outputs.py,
  test.sh, task.toml, Dockerfile SAME; instruction.md, solve.sh DIFFERS — as claimed).
- Red legs reproduced: the superseded `sha256sum -c corpus/evidence/round{36,37,38}/…/SHA256SUMS` from the lane root →
  5/6/5 × `FAILED open or read`, `WARNING: N listed file(s) could not be read`, rc 1 — each erratum's quoted failure
  exactly. Old lines still sit at the anchors the errata name (`:5`, `:6`, `:4`).

## F3 — round-38.md lesson errata (2 items): PASS, every citation resolves

- Item 1 (Mistakes row 2 `captured-by` cell, supersedes `:36`): the superseded sentence is verbatim at `:36`; the rule
  forward it omits is verbatim at `corpus/lessons/round-37.md:42` ("Rule forward: a control that executes a frozen
  instrument keeps the run as a receipt."); `plans/round-38-claims.md:10-11` carries "output was discarded unread; it is
  not the first recorded run and is not evidence" verbatim.
- Item 2 (Header "Controls, all red" sentence, supersedes `:12-15`): `census-before.txt` read whole — 15 `W04` rows,
  final `kengaku ok …/corpus/SOURCES.md`, `exit=0` (a clean baseline, not red); `grep -c census plans/round-38-claims.md`
  → `0`; `corpus/lessons/round-39.md:13` says "census-before.txt (exit 0, 15 W04 — a baseline, not a control)";
  `.ufo/waves/round-38/claims/control-c2-skip.txt:11` carries the `P10 DEFECT fresh probe …` line.
- Forward state: `git cat-file -e e0a37853:corpus/evidence/round38/build-pmars-probe.txt` → rc 128 (reproduced);
  `git ls-tree -r 088f7c36 -- .ufo/waves/round-39/` lists 7 files, none a control asserting a run (no `control-c2-skip.txt`),
  matching the erratum's "green on `088f7c36`". Wave-1 pair-check receipt (`build/R39LessonErrata/receipts.md` §C) read
  and consistent; I did not re-execute `order_check.py` at `e0a37853` (residual, §Gaps).

## F4 — Protein claim: CONFIRMED

Claim (`corpus/lessons/round-39.md:44`): the R4 errata appended to `tb2-protein-assembly-grader.md` added four
`recheck:` strings; the next C1 run printed `SETUP module battery38/p7m.py failed to build (rc=1) … expected exactly
one 'recheck:', found 5`.

1. Baseline (clean clone): `python3 plans/round38_c1_verify.py --lane .` → `PINS total=14 mismatched=0`, `BATTERY
   fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=21 survived=1` (N21 SURVIVED),
   `PREDICATE C1 fail`, rc 1 — identical to the disclosed landing measurement (`integrate/measure-final.txt:360-362`);
   N21's unreachable direction is documented at `corpus/lessons/round-38.md:35`, so this red is the known state, not a
   new finding. All p7m fixtures `ok` in the baseline.
2. Append in the clone: appended an errata-shaped block carrying exactly 4 `recheck:` tokens (`grep -o | wc -l`: 1 → 5).
   Round-38 counter: fast abort (4.7 s), `RuntimeError: expected exactly one 'recheck:', found 5` raised at
   `plans/battery38/p7m.py:38` via `_n11` → `_package` — p7m is broken, exactly the claimed mechanism
   (`_only_once` in the fixture build).
3. Same append, round-39 counter: `PINS total=26 mismatched=0`, then `SETUP module battery38/p7m.py failed to build
   (rc=1): … expected exactly one 'recheck:', found 5`, **exit 2** — the lesson's receipt verbatim
   (`plans/round39_c1_verify.py:204` raise → `:288-290` `SETUP` + `return 2`).
4. Restore: entry copied back after each run; `git status --porcelain` on the path empty both times. Tip corroboration:
   `grep -c 'recheck:'` in the entry → `1` — the L1's append was indeed never committed (lesson fix cell: "reverted from
   the branch … never committed"), and the round-39 C1 is green at the tip (`measure-final.txt:103-105`: `MUTANTS total=7
   killed=7 …`, `PREDICATE C1 pass`, `exit=0`).

Mechanism note (not a defect): the SETUP-line + exit-2 shape belongs to the round-39 counter; the round-38 counter
(byte-identical to its freeze, as are the round-39 counter and the gate — `git log 088f7c36…a6832f53` over the three
files is empty) surfaces the same root failure as an uncaught traceback with exit 1. The lesson's quoted receipt is the
round-39 C1 run, which is the run that existed when the L1 append was present. Both counters: p7m broken by the append.

## Defects found

None in the reviewed errata: append-only holds (4/4), all corrected recheck commands are green as written (3/3 + pin
check), and every quoted string, count and exit code I checked resolves at its cited location (11/11 citations).

## Gaps / residual risk

- Refetch legs hit `raw.githubusercontent.com` live (network was up). The TB2.1 `7131e437` pin is point-in-time
  ("git ls-remote HEAD on 2026-10-26"); I verified the pinned digests, not that HEAD still points there.
- I took wave-1's §C order_check pair-check (red at `e0a37853`, green at `088f7c36`) from its receipt instead of
  re-running `order_check.py` at two revisions; the cheap halves (rc-128 absence, claims-tree contents) I did verify.
- Probe byte-equality was confirmed by one fresh run each, so it evidences determinism of these three probes at this
  tip, not a general property.
- The round-38 counter's `PREDICATE C1 fail` (N21) on any tree is pre-documented; no erratum I reviewed claims otherwise.

VERDICT: errata-ok/4-protein-claim-confirmed
