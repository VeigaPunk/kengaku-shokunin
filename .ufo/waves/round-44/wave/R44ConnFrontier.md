# R44ConnFrontier — TB2 grader-class frontier map (connector, coverage axis)

**Method (all observed, read-only).** Corpus coverage map and `## Frontier` (`corpus/README.md:238-395`), round-43 histogram (`.ufo/waves/round-43/build/R43ConsiderThese.md:12-27,132-137`), frozen round-44 claims (`plans/round-44-claims.md:71-104`), knowledge tree (`corpus/knowledge/tb2-*.md` ×9), the feal-differential entry (`corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md`), and the round-44 wave spec (`.ufo/waves/round-44/wave-spec.json`, counted with `python3 -c` → 68 items). No commands were run beyond reads and one JSON count.

## 1. What is read: 10 TB2 graders, 7 of 11 classes

| # | class | task | round | knowledge entry |
|---|---|---|---|---|
| 1 | F2 | protein-assembly | 35 | tb2-protein-assembly-grader.md |
| 2 | F2 | regex-log | 36 | tb2-regex-log-grader.md |
| 3 | S1 | configure-git-webserver | 37 | tb2-git-webserver-grader.md |
| 4 | B1 | build-pmars | 38 | tb2-build-pmars-grader.md |
| 5 | G1 | git-leak-recovery | 39 | tb2-git-leak-recovery-grader.md |
| 6 | F2 | db-wal-recovery | 40 | tb2-db-wal-recovery-grader.md |
| 7 | F2 | constraints-scheduling | 41 | tb2-constraints-scheduling-grader.md |
| 8 | P1 | circuit-fibsqrt | 42 | tb2-circuit-fibsqrt-grader.md |
| 9 | M1 | feal-differential-cryptanalysis | 43 | tb2-feal-differential-cryptanalysis-grader.md |
| 10 | F1 | feal-linear-cryptanalysis | 44 (in flight) | tb2-feal-linear-cryptanalysis-grader.md (C2 claim, S138-S146) |

Matches the round-43 histogram's lane-read column (6 classes before round 44; `R43ConsiderThese.md:27`), plus the round-44 F1 read.

## 2. Classes remaining uncovered after round 44

4 classes, 8 tasks (from `R43ConsiderThese.md:27` counts, minus the F1 read):

| class | meaning | tasks | members (histogram rows) |
|---|---|---|---|
| V1 | VM / emulator | 3 | install-windows-3.11, qemu-alpine-ssh, qemu-startup |
| W1 | model/weights artefact | 2 | pytorch-model-recovery, train-fasttext |
| O1 | browser-in-the-loop | 2 | break-filter-js-from-html, filter-js-from-html |
| D1 | database queried | 1 | query-optimize |

(Counted before the round-44 F1 landing, F1 adds a fifth class / 14 tasks.)

## 3. feal-linear-cryptanalysis is genuinely new ground — not a re-read of feal-differential

**New: yes.** The round-43 histogram classified `feal-linear-cryptanalysis` as F1 (`R43ConsiderThese.md:63`: class F1, deciding line `:122` `assert c in data`, lane-unread), the largest uncovered class (14 tasks, 0 read), and its §"3 uncovered classes most worth a round" names F1 first (`:132-133`). Round 44 is the lane's first executed F1 read. The R43ConsiderThese prose even pre-identified this task's loose check as an F1 example (`:133`: "`feal-linear-cryptanalysis.py:122` substring `in data`").

**Not a re-read of feal-differential (M1).** Distinct on every dimension:

- Class: M1 (module imported into the grader's interpreter, `test_outputs.py:22-24`) vs F1 (file constant/answer compare).
- Graded artefact: `/app/attack.py` module, imported and called, answer via `feal_in_c.get_keys()[5] == stolen` at `:30` vs a text file `/app/plaintexts.txt` checked by substring membership `assert c in data` at `:122` over 100 in-grader decimal constants.
- Passing mechanics: differential cheats are in-process import tricks (sys.modules shadow, `__eq__` reflection, `os._exit(0)`, clock-seed replay — entry `:35-48`); linear passes are out-of-band copies (public gen.py keys, public hash chain, constants from the public test file — claims `:82-87`).
- Sources disjoint: S129-S134 (differential) vs S138-S146 (linear).

## 4. What a 64-seat round needs to cover two of them

Ground truth for scale: the round-44 wave spec is **68 seats** (64-seat floor, R4) for ONE new grader (feal-linear, C2) plus the C1 battery and closure — role counts: executor 22, scribe 11, critic 9, scout 7, mutation-tester 5, reviewer 5, connector 4, sentinel 2, simplifier 2, revenger 1. Of those, the grader-specific stack is ~15-18 seats (ScoutRefetch, RevProbe, PytestParity, CritIndep, CritCases, CritV11, MutC2V11, MutC2Guards, CritGateRows, PkgEntry, PkgRows, PkgProse, ReadmeIndex, …), the rest shared.

Per-class claim stack (reusable across two classes, parallelizable): L1 fetch+pin (1 seat shared for both), refetch verify (1), probe build+execute+regrade (2), entry scribe (1), counter critic + predicate/indep (2), counter mutation-guards (1-2), reviewer (1-2) → ~8-10 dedicated seats/class.

A 64-seat round covering two classes therefore needs: **2 × ~9 dedicated (≈18) + ~20-25 shared/round-wide** (planner/L1, sentinels, envelope, scorecard, lessons, QUALITY, routed burn-down, index scribes/reviewers, connectors, hygiene, prior-art scouts per class) ≈ **38-43 seats** — fits 64 with margin. The slack is the safety buffer for infra-heavy classes and review churn; with two claims the round should still run as one v2 wave, with the two probe/entry/counter lanes in parallel.

Which two: **D1 + O1** are the feasible pair (D1 = one sqlite3-only task, offline probe cheap, `R43ConsiderThese.md:134`; O1 = 2 browser tasks, needs headless Chrome + selenium — offline feasibility inferred, not tried, `:135`). V1 (qemu image/ISO+emulator cost) and W1 (hidden reference weights/data, heavy deps) stay deferred per `R43ConsiderThese.md:137`. If forced to cover V1/W1, add 4-8 infra/GPU seats and the round becomes tight but still within 64.

## VERDICT
VERDICT: frontier-new-uncovered-4
