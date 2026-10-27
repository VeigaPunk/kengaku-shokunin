# R48C2RevNoHarm — C2 coverage/quality review

**Axes:** coverage; quality. **REV inspected:** `a543d92083557dd9b33ee674e9b99b03411f80af` (stage-1 freeze; read-only inspection, no scored run). The frozen claims file requires a stage-2 freeze before the first full C2 probe; I did not run the counter or probe. Existing round-46 receipt is prior evidence, not a round-48 measurement: its associated stage-2 commit `4fdeebaa546cfd77a88a55a4a875272b142a8868` is dated `2026-10-27T02:32:46-03:00`, before round-48 stage-1 `a543d920...` at `2026-10-27T06:53:29-03:00`. Any round-48 scored measurement must therefore wait for and cite the subsequent stage-2 commit/REV.

## Finding — admitted entry retains a false class-contrast in its main body (quality; coverage-claim inflation)

The entry's Summary/Finding 7 says prior exemplars do not execute graded bytes as programs (`corpus/knowledge/tb2-polyglot-c-py-grader.md:35`); its own Errata explicitly says this is false because the round-43 `tb2-feal-differential-cryptanalysis-grader.md` imports the agent-written module and calls `attack` (`:314-318`). The cited prior entry independently describes that import-and-call (`corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md:17`). Thus the correction is present only as errata while the body remains self-contradictory. The narrower novelty is specifically compiling the graded artefact or running the same bytes under two language runtimes. Admitting unchanged text can misstate corpus coverage and inflate the stated novelty of the coverage increment.

**Exact falsifiable check:** on the landing REV, read the Summary and Finding 7 and compare their class-contrast sentence with Errata 1. Fail this no-harm check if either body location still asserts that no prior exemplar executes graded bytes; pass only if both state the narrowed compile/two-runtime distinction or are removed. Evidence already observed at inspected REV: `grep -n "none of them executes the graded bytes\\|a grader class new to it\\|twelfth" corpus/knowledge/tb2-polyglot-c-py-grader.md` returned lines 16, 17, and 35; Errata 1 at lines 314–318 calls the broad assertion false. The matching narrow description is already in `corpus/README.md`'s entry row.

## Finding — predictor misses the task's own published passing solution (quality)

The entry calls the predictor the V11 contract and says it is admitted unchanged (`:217-222`), but its implementation rejects sources without `def emit(k):` (`:284-290`). The captured oracle solution instead defines `fib_py` with a loop and prints `fib_py(k)` (`corpus/evidence/round46/tb2-polyglot-c-py/solve.sh`); the receipt records `oracle-solve-sh predicted=pass observed=pass tests=P` and its captured case was the published solution. Directly applying the visible predicate condition to that captured source yields False before any grader leg, while the grader receipt says that source passes. The entry does disclose that the predictor mis-predicts valid polyglots of another shape (`:304-306`), but the oracle is not an arbitrary held-out shape: it is the task's own published solution included as a passing case. This weakens the predictor's value as a semantic reference for future readers.

**Exact falsifiable check:** using only frozen bytes, evaluate the published `predict(files, source)` against the `/app/polyglot` state created by captured `solve.sh`; compare it with the `oracle-solve-sh` result in the receipt. Harm is confirmed if `predict` returns False while the captured test execution is P. No predictor, probe, or counter execution was performed for this report; the code-level rejection follows from the visible required `def emit(k):` test and oracle source, and the receipt's output is quoted as prior evidence.

## Other checks / bounded result

- No duplicate task entry was found in `corpus/knowledge/`: the only search hits for `polyglot`, `main.py.c`, `dual-runtime`, or `two toolchains` were this entry, `tb2-db-wal-recovery-grader.md` (incidental `main.py.c` text), and `SOURCES.md`. The README describes this as the twelfth of 89 task graders and explicitly says it is not breadth or a quality claim. This narrows the coverage concern to the false class-contrast, not duplicate task coverage.
- The frozen C2 receipt digest matches `plans/pkg-spec-r46.json`: `dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277`; `sha256sum -c SHA256SUMS` reported all eight captures `OK`. These integrity checks do not establish that the receipt is a fresh round-48 measurement.
- `instruction.md:7` names `f(1)=1`; the captured `test_outputs.py:27` tests only N=42, 10, and 0. The entry's Errata 2 explicitly says f(1) is untested, and its requirement-map discussion specifies those three tested points. Do not characterize the grader as checking f(1) or general Fibonacci correctness.
- C2 stage-2 measurement remains unverified here. Frozen ordering requires P10-disabled pre-receipt controls and no full probe until after stage 2. Once stage 2 exists, the falsifiable receipt check is the committed counter's frozen V7/V8/V14/V15 predicate plus the first post-stage-2 full probe, with its `REV` matching the measured committed tree; any V defect or mutation count below the frozen floor is a fail. I did not run these checks.

## Evidence sources opened

Access date for all local lane sources: 2026-10-27. Upstream source was not fetched directly; the following URL and quote are from its digest-checked lane capture. Quote is ≤25 words.

- S166, `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py`, accessed 2026-10-27; captured quote at `corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py:27`: “test_cases = [(42, \"267914296\"), (10, \"55\"), (0, \"0\")]”.
- S168, `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/instruction.md`, accessed 2026-10-27; captured quote at `instruction.md:7`: “f(0) = 0, f(1) = 1, etc.”
- S169, `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/solution/solve.sh`, accessed 2026-10-27; captured quote: “for _ in range(n):” (`solve.sh`, inside `fib_py`).
- Local sources: frozen claims `plans/round-48-claims.md`; routed spotcheck `corpus/lessons/round-46-verifier-spotcheck.md`; entry and captured files cited above; `plans/pkg-spec-r46.json`; `corpus/README.md`; prior exemplar `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md`. All were read from the lane clone at REV `a543d920...`; their exact access date is 2026-10-27.

## Exact commands run

```text
mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C2RevNoHarm
cd /fast/scratch/hyaku/kengaku-r48/R48C2RevNoHarm && git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
cd lane && git rev-parse --show-toplevel
cd lane && git log --oneline -3 a543d92083557dd9b33ee674e9b99b03411f80af
cd lane && git cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af
cd lane && (cd corpus/evidence/round46/tb2-polyglot-c-py && sha256sum -c SHA256SUMS)
cd lane && sha256sum corpus/evidence/round46/polyglot-c-py-probe.txt
cd lane && grep receipt_sha256 plans/pkg-spec-r46.json
cd lane && git show a543d92083557dd9b33ee674e9b99b03411f80af:plans/polyglot_c_py_probe.py | sha256sum
cd lane && git show -s --format='%H %cI' a543d92083557dd9b33ee674e9b99b03411f80af
cd lane && git show -s --format='%H %cI' 4fdeebaa546cfd77a88a55a4a875272b142a8868
cd lane && grep -n "none of them executes the graded bytes\\|a grader class new to it\\|twelfth" corpus/knowledge/tb2-polyglot-c-py-grader.md
cd lane && grep -n "f(1)" corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py corpus/evidence/round46/tb2-polyglot-c-py/instruction.md
cd lane && grep -n '^REV\\|^cases=\\|oracle-solve-sh\\|regrade cases' corpus/evidence/round46/polyglot-c-py-probe.txt
```

Observed outputs: clone top-level `/fast/scratch/hyaku/kengaku-r48/R48C2RevNoHarm/lane`; `git cat-file -t` → `commit`; stage-1 timestamp `2026-10-27T06:53:29-03:00`; old stage-2 timestamp `2026-10-27T02:32:46-03:00`; all eight capture checks → `OK`; receipt hash and spec hash both `dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277`; probe hash at stage 1 `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`; receipt lines include `CASE oracle-solve-sh predicted=pass observed=pass tests=P predicted_tests=P match=yes ...`, `regrade cases=18 differ=7`, and `cases=18 observed_pass=7 observed_fail=11 mismatches=0`. The existing round-46 receipt has no `REV` line.

## Limits and verdict

No round-48 scored execution, external fetch, runtime test, or edit to claimed work was performed. This review does not admit C2 and cannot decide its frozen counter or mutation-floor result. **VERDICT: plausible quality harm remains** — the entry's admitted body contradicts its own class-contrast erratum, and the published predictor visibly rejects the package's own recorded passing oracle solution. Coverage overlap was not observed; coverage-claim inflation is limited to the stale broad class-contrast. Scratch was removed before yield.
