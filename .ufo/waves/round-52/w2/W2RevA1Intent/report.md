# W2RevA1Intent — round 52, wave 2 (falsify), revenger, leaf member

Item: recover the intent of the round-35..46 TB2 hand-reading series and of Amendment A1 (`plans/round-52-claims.md`); say what A1 preserved and what it may have lost. Read-only over the lane. No lane file, sibling, `.ufo/state/`, or git/jj state was touched. No tool was installed or upgraded (none needed). No peer was messaged. Measurements were taken on a scratch copy (`/fast/scratch/hyaku/kengaku-r52/w2-W2RevA1Intent/lane`) of `plans/` and `corpus/{evidence/round52/graders,knowledge,lessons}` as they stood at my run; the scratch dir is removed before yield, and the receipts below are copied to `receipts/`.

Companion file with the same content: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevA1Intent.md`.

## 0. Summary (calibration: what is measured, what is inferred)

- **Series question (measured from the entries, the receipts and the README scope rows):** for one Terminal-Bench 2.0 grader at the pin, *what does the reward bit decide, requirement by requirement, and what does a reward-1 end state prove?* Each entry answers it with located byte quotes, a frozen probe over end states, a falsifier and a Negative-space block. The series disclaimed quality verdicts (README rows for rounds 38–43: "no quality, validity, difficulty or gameability verdict"; rounds 44–46: "no quality claim").
- **R52-C1 changes the question** from "what does this grader decide" to "which graders are vacuous" — a population-level quality verdict the series had declined to make per grader. A1 is the step that makes that verdict operable. This is the intent drift the round report should state.
- **A1 preserved:** the frozen population, pin and digest requirement; the located-bytes discipline; the requirement that a counter may only *queue* a grader and that a human second reader must confirm; the threshold `CONFIRMED ≥ 2`; dated, pre-after-run disclosure.
- **A1 may have lost** (each item below has a measurement): (a) "located" — the operative per-test predicate is a lexical proxy with measured recall 32/53 = 60 % against an AST oracle of presence-only tests, and the located-quote check is a bare substring test; (b) "same marker vocabulary, mechanical split" and "file-level before-state stays re-derivable" are not true — the per-test rule adds a comparison vocabulary the frozen text never names, and three file-level labels differ from the frozen literal rule; (c) the code's candidacy (`P1 or V1 or V4`) is not A1's text (`≥1 P1`); (d) the frozen blind-class control no longer fails for its frozen reason; (e) A4 discards a presence-only figure (54 / 42) that an independent AST definition reproduces almost exactly (53 / 42), so the committed rules under-report the population the amendment targets; (f) the amendment's own motivating example, `torch-tensor-parallelism::test_parallel_linear_exists`, is classified P2 by the amended counter.
- **Overlap:** wave-1 seats `C1RevSeriesIntent` (series reconstruction, §2–§5) and `C1CritRoundShape` (candidacy definition, blind-class control, A1 receipt figures) reached parts of this independently. My new measurements are: the AST oracle and recall/precision, the block-absorption defect, the vocabulary/file-class drift, the one-word quote acceptance, the measured blind-class control result, the hf-model-inference false positive, and the 53/42 reproduction.

## 1. The series' question (reconstructed)

Sources read: `corpus/lessons/round-35.md` … `round-46.md` (Gate, Mistakes, Census, Falsifier-wave sections); the twelve `corpus/knowledge/tb2-*-grader.md` entries (Summary, Negative space, Falsifier blocks); `corpus/knowledge/benchmark-grader-semantics.md` (reading-basis and negative-space framing); `corpus/README.md` lines 298–308 (per-round coverage rows and their scope clauses); `corpus/QUALITY.md` rules referenced there.

Evidence for the question's shape:

1. Every entry's **Summary** states what the grader's reward bit depends on at the pin (e.g., `build-pmars`: "Nothing in those four functions builds anything … Provenance is inferred from three cheap signals").
2. Every entry has a **Negative space** block listing what the entry does *not* establish (e.g., `protein-assembly`: "that the literals are the correct PDB/FPbase/antibody answers … task validity in the PROVINCE sense").
3. Every entry has a **Falsifier** block with a re-fetch and re-run condition.
4. The README scope clauses (`corpus/README.md:300`–`308`) say each instance is "not breadth, and no quality, validity, difficulty or gameability verdict" (rounds 38–43, lines 300–304 and 306) or "no quality claim" (rounds 44–46, lines 305, 307–308). The grader-series Mistakes tables are about the *lane's own counters* being vacuous (`corpus/lessons/round-36.md:34` "frozen counters accepted junk"; `round-37.md:41,47,48`; `round-41.md:15` "frozen predicate satisfiable with zero round-41 work").
5. The wave-1 reconstruction (`.ufo/waves/round-52/w1/C1RevSeriesIntent.md` §2–§3) reaches the same reading and adds the cross-task conclusion: a fixed, finite, in-file witness set decides every grader, and ≥56 of 91 passing end states are documented passing violators. I did not re-derive that count.

So the series' question is **descriptive and per-grader**: what the reward bit compares, what a pass licenses, and what it cannot see — settled by bytes plus an executed probe, never by a population statistic. Its stated non-questions are validity, difficulty and gameability as verdicts.

[INFERENCE] The round-52 title "grader-vacuity triage" moves from the per-grader descriptive question to a population verdict. The amendment is where that move becomes operative: before A1 the counter classified files; after A1 it classifies tests and decides the candidate queue.

## 2. What A1 preserved (verified in the frozen text and the counter)

| invariant | where it lives | status after A1 |
|---|---|---|
| Population and pin: 89 tasks, 184 captures, `2fd12b88…` | `plans/round52-tasks.json`, claims §Frozen population | preserved (counter reads the same population) |
| Digest-pinned captures | `corpus/evidence/round52/graders/SHA256SUMS`; counter `collect()` | preserved; `mismatched=0` in the lane copy |
| Triage queues, does not clear | counter `candidate = bool(p1) or cls in (V1,V4)`; no clearance output | preserved formally (absence from the queue is never printed as "sound") |
| Confirmation by a second reader with a located quote | counter `verdict()` confirmation loop | **weakened in form**: quote check is substring; reader is any non-empty string (§3.5) |
| `CONFIRMED ≥ 2` threshold | counter `len(conf_new) >= 2` | unchanged number, but the candidate pool grew from 2 file-level V1 tasks to 29 candidates (§3.3), so the gate is met by human confirmations, not by the counter |
| Never-read condition | `lane_read_tasks()` from the 12 `tb2-*-grader.md` filenames (A2) | preserved; the 12 hand-read ids are reproduced |
| Dated, pre-after-run disclosure | claims §Amendment A1, `.ufo/waves/round-52/claims/a1-observation.txt` | preserved; A4 later corrected the observation's figures |
| File-level classes kept and printed | counter prints `CLASS V1=2 …` | printed, but **not** re-derivable from the frozen text (§3.2) |

## 3. What A1 may have lost — measurements

All commands run in the scratch lane copy; `plans/round52_c1_grader_audit.py` was imported unmodified and its functions were applied (receipts in `receipts/`).

**3.1 The amended counter's own result (as copied at my run; no confirmations file, no prior-art file).**
```
TASKS total=89 records=89 classified=88
CAPTURES expected=184 present=183 mismatched=0
CLASS V1=2 V4=0 V2=53 V3=31 V0=3
TESTCLASS presence_only_tests=33 tasks_with_presence_only=27
CANDIDATES total=29
CONFIRMED new=0 []
PRIOR-ART ok=False urls=0
PREDICATE R52-C1 fail
PREDICATE R52-C1-A5 fail
```
`present=183` / `classified=88` is the A5 exclusion, not a defect of my seat. Receipt: `receipts/counter-lane-copy.txt`.

**3.2 The per-test rule's vocabulary is not the frozen vocabulary.** A1 says "Same marker vocabulary, mechanical split." The code (`plans/round52_c1_grader_audit.py` lines ~49–59 and `classify_test`) adds:
- `VALUE = (==|!=|<=|>=|[<>]|allclose|len\(|np\.|torch\.|\.keys\(\)|\bin\b)` — a comparison vocabulary that appears nowhere in the frozen claim text. P1 vs P3 is decided by this regex, not by the frozen markers.
- `BEHAV_T` adds `multiprocessing|mp\.|threading|dist\.` — `mp\.` has no word boundary, so `tmp.` matches.
- Every block is searched **including its docstring, comments, assert messages and string literals**.
- The file-level `CONTENT` regex gains `assert.*\bin\b`, which is not in the frozen content list; `PRESENCE` gains `os.path.isfile`; `PRESENCE` is `\b`-anchored.

Consequence for the file-level before-state (`receipts/vocab_drift.txt`): comparing the counter with the literal frozen markers over the 88 captured primaries gives three label drifts, all V1 under the frozen literal text:
- `bn-fit-modify` V1 → V3 (via `assert.*\bin\b`);
- `portfolio-optimization` V1 → V3 (same);
- `distribution-search` V1 → V0 (the literal frozen `exists(` matches inside the function *name* `test_distribution_file_exists(`; the counter's `\b` does not).

Hence the frozen literal rule gives **V1 = 5**, while the printed `CLASS V1=2` is the counter's own. A1's sentence "the file-level classes … are kept and still printed, so the before-state stays re-derivable" is therefore false as stated. [INFERENCE on the total: 2 unchanged + 3 drifted; the drift list is exhaustive over the 88 primaries.]

**3.3 Recall and precision of the per-test P1 rule against a presence-only oracle.** Independent oracle (`receipts/a1_oracle.py`, Python `ast`): a test function `def test_*` is PRES when it has ≥1 `assert` and every `assert` test-expression is a call to `exists/is_file/is_dir/isfile/isdir` (possibly `not`/`and`/`or`-combined). Messages are ignored. 305 test functions in the 88 present primaries.

| | count |
|---|---|
| oracle PRES tests / tasks | **53 / 42** |
| counter P1 tests / tasks | 33 / 27 |
| P1 precision vs PRES | 32 / 33 |
| PRES recall by counter P1 | **32 / 53 = 60 %** |
| PRES tests the counter calls P3 | 20 |
| PRES tests the counter calls P2 | 1 (torch-tensor-parallelism::test_parallel_linear_exists, §3.4) |
| new (not hand-read) tasks with ≥1 PRES test | 39 |
| …of which the counter queues | 26 (24 via P1, 2 only via file-level V1) |
| …of which the counter misses | 13: cobol-modernization, custom-memory-heap-crash, extract-moves-from-video, fix-code-vulnerability, gcode-to-text, headless-terminal, llm-inference-batching-scheduler, merge-diff-arc-agi-task, rstan-to-pystan, sparql-university, torch-pipeline-parallelism, tune-mjcf, video-processing |

Why the P3 misses happen — measured on the source, not inferred:
- Docstring/comment words: `pytorch-model-recovery::test_model_file_exists` (comment "the WORKDIR in the Docker env"), `circuit-fibsqrt::test_gates_file_exists` (docstring "in the current directory"), `video-processing::test_example_video_exists` (docstring "exists in the container") — each is a one-assert presence test whose block hits `\bin\b`.
- String literal: `headless-terminal::test_cancel_command` hits `>` inside the shell string `"… > /app/cancel.txt"`, and its real assertion is `assert not path.exists()`.
- Block absorption (§3.4): `tune-mjcf::test_tuned_model_exists` is followed by a non-test helper `simulate_model` that contains `np.`.

Note: the P1 false positive, `hf-model-inference::test_model_downloaded`, is the only counter-P1 test that the oracle does not call PRES. Its body calls `from_pretrained` for the model and tokenizer and asserts `model is not None`; the counter calls it "satisfied by the mere presence of the artefact" because `is not None` contains no value token. That is a loader check, not a presence check.

**3.4 Block absorption makes the amendment's own example misclassified.** `split_tests` cuts a block only at the next `^def test_`. In `torch-tensor-parallelism/tests/test_outputs.py`, `test_parallel_linear_exists` is a one-assert presence test (`assert parallel_linear_path.exists(), …`), but its block runs on through the non-test helpers `_setup_process_group`, `_cleanup_process_group` and `_test_column_parallel_linear`, which contain `dist.` and `torch.allclose`. The amended counter therefore returns **P2** for the very test that A1 cites as the confirmed weakness. The same defect hits `tune-mjcf`. [measured: block text printed in the probe]

**3.5 The hardened CONFIRMED leg accepts a one-word quote.** The A1 check is `quote not in grader.read_text(...)` (a substring test). Scratch-only demonstration (`receipts/demo-and-control.txt`, `demo/` fixture): a `confirmations.json` with `quote: "exists"`, `reader: "W2RevA1Intent"`, `confirmed: true` for `pytorch-model-recovery` and `torch-tensor-parallelism` gives `CONFIRMED new=2 ['pytorch-model-recovery', 'torch-tensor-parallelism']`. Neither is a located quote; the reader field is not checked for independence. The demo was not written into the lane.

**3.6 The candidacy rule diverges from A1's text.** A1: "A task is a vacuity candidate when ≥1 of its tests is `P1`" and the confirmation leg requires "(i) the task … is a vacuity candidate". Code: `candidate = bool(p1) or cls in ("V1","V4")`. Two tasks — `pytorch-model-recovery` and `torch-tensor-parallelism` — are candidates only through the file-level V1 label, which A1 says is false of those graders as a whole, and neither has a counter-P1 test. The divergence only widens the pool (it cannot make the leg stricter), so it is not a hidden weakening of the gate, but it keeps the disowned label operative.

**3.7 The blind-class control no longer fails for its frozen reason.** Frozen control `c1-control-blind-class`: "force every task to V0 → `CANDIDATES total=0` → `CONFIRMED new=0`." Measured by monkeypatching `classify` to return V0 on the lane copy (`receipts/demo-and-control.txt`): `CANDIDATES total=27`. Per-test P1 candidacy does not read the file-level class, so the control's stated kill does not occur. It is still red only because the lane copy has no confirmations file (`CONFIRMED new=0`). A1 says "the control set … unchanged"; the control's mechanism changed.

**3.8 A4 discards a figure that an independent definition reproduces.** A4 says the 54 P1 / 42 tasks figure "is not reproducible and is not evidence" under the committed rules, and that the counter's `33 / 27` is the measurement. That is correct for the committed lexical rules. Under the AST definition in §3.3 the presence-only population is **53 tests / 42 tasks**, essentially the superseded figure. This is my definition, applied after the fact, so it is not evidence for the claim. It does mean the committed counter's 33 / 27 under-reports the referent that A1's per-test unit was introduced to measure (recall 60 %), and that the report should not present 33 / 27 as the size of the presence-only population. [INFERENCE on which definition the claim intended; the claim text is "compares nothing".]

**3.9 The round-38 precedent does not show a per-test presence-only unit.** A1 says the per-test rule "was already implied by … round 38's `build-pmars` entry records a canned 21-line C program passing on presence-level checks." Under the AST oracle `build-pmars` has four tests, none PRES (`test_pmars_works` MIXED, `test_headless_no_x11` OTHER, `test_debian_source_used` MIXED, `test_built_from_source` MIXED); under the counter all four are P3. The entry's finding is provenance-blindness (a canned binary passes), which is a property of the whole grader, not of a presence-only test. The precedent supports the series' "proxy checks, no provenance" class, not A1's unit. [INFERENCE: the rhetorical link is an after-the-fact retrofit.]

**3.10 Process-level risk.** A1 was written after the L1 had seen population marker statistics (disclosed). The lane's own Mistakes tables show the recurring failure of counters written in this series: vacuous predicates (round 36, round 37, round 41). A1 added a new counter surface after data, and the controls set was not re-derived for the new unit (§3.7). The disclosure is honest; the control re-derivation was not done.

## 4. The invariant the amendment preserves, and the one it may have lost

- **Preserved — one-sidedness.** A class can only queue a grader; absence from the queue is never printed as clearance. The series' core lesson (every one of the twelve entries documents passing violators inside marker-rich graders; `C1RevSeriesIntent` §5) is respected by the counter's output shape.
- **Preserved — digest-pinned bytes and a human second reader.** The counter only grades what the digest pins, and confirmation still needs a named reader and a quote.
- **Possibly lost — "located".** The series' verdicts rest on located quotes that a reader checked against bytes (≤25-word quotes, falsifier blocks). A1 turns the located step into a substring test (§3.5) and a lexical predicate with 60 % recall (§3.3). A task can now be confirmed by a one-word quote, and a presence-only task can be silently un-queued because a docstring contains "in".
- **Possibly lost — "the queue is the candidate set".** The queue is now a biased sample (recall 60 %; 13 new presence-only tasks never queued; §3.3). Any downstream reading of "CANDIDATES total=29" as "the presence-only tasks" is wrong.
- **Possibly lost — the frozen controls as kills.** The blind-class control no longer produces the frozen kill (§3.7); the file-level before-state is not re-derivable from the frozen text (§3.2).

## 5. Confidence

| statement | confidence | basis |
|---|---|---|
| The series asks a per-grader descriptive question and disclaims quality/gameability verdicts | high | README scope clauses, entries' Negative-space and Falsifier blocks (quoted above) |
| R52-C1 turns that into a population-level quality verdict | medium-high | claims text ("whole-benchmark grader-vacuity triage"); [INFERENCE] on intent |
| The per-test P1 rule has recall 32/53 and precision 32/33 against the AST oracle | high (measured) | `receipts/a1-oracle-vs-counter.txt`; oracle definition is mine, stated above |
| Vocabulary is not the frozen vocabulary; file-level V1 is 5 under the frozen literal text, 2 printed | high (measured) | `receipts/vocab_drift.txt` |
| torch-tensor-parallelism's named test is classified P2 by block absorption | high (measured) | `receipts/a1-oracle-vs-counter.txt`; source print in the probe |
| Candidacy widened beyond A1's text (V1/V4) | high (read in code) | `plans/round52_c1_grader_audit.py` `candidate = …` |
| Blind-class control does not produce its frozen kill | high (measured) | `receipts/demo-and-control.txt` |
| One-word quote passes the hardened leg | high (measured, scratch only) | `receipts/demo-and-control.txt` (demo) |
| 53/42 reproduces the superseded 54/42 under an AST definition | medium (different definition, one-off count) | §3.3; not evidence for the claim |
| The round-38 precedent is a retrofit | medium [INFERENCE] | §3.9 |

Limits of this seat: I did not read all twelve entries end to end (I used their Summary, Negative-space and Falsifier structure plus the wave-1 reconstruction for the per-entry lists); I did not re-fetch any pinned URL; I did not evaluate the A5 exclusion; I did not check the 308 test-function figure in A4 (the 88 present primaries give 305; the 89th file is excluded and I did not fetch it [INFERENCE: the difference is most likely its tests]); the oracle ignores `pytest.fail` / `raise` guards, so a test with `if not p.exists(): pytest.fail(…)` is counted OTHER, not PRES.

## 6. Exact commands

```
mkdir -p /fast/scratch/hyaku/kengaku-r52/w2-W2RevA1Intent/lane && cp plans/round52_c1_grader_audit.py plans/round52-tasks.json plans/round-52-claims.md  …/lane/plans/ ; cp -r corpus/evidence/round52/graders …/lane/corpus/evidence/round52/ ; cp -r corpus/knowledge corpus/lessons …/lane/corpus/
cd …/lane && python3 plans/round52_c1_grader_audit.py --lane .          # receipts/counter-lane-copy.txt  (exit 1)
cd …/lane && python3 ../a1_oracle.py                                     # receipts/a1_oracle.py, a1-oracle-vs-counter.txt
cd …/lane && python3 ../vocab_drift.py                                   # receipts/vocab_drift.py, vocab_drift.txt
python3 blindclass_driver.py <lane-or-demo> none|blind                   # receipts/blindclass_driver.py, demo-and-control.txt
  (demo/ = lane copy + confirmations.json with quote "exists"; scratch only)
```

## 7. Files

- Report (this file): `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevA1Intent/report.md`
- Companion: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevA1Intent.md`
- Receipts (copied out of scratch): `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevA1Intent/receipts/` — `a1_oracle.py`, `a1_probe.py`, `blindclass_driver.py`, `vocab_drift.py`, `vocab_drift.txt`, `counter-lane-copy.txt`, `a1-oracle-vs-counter.txt`, `demo-and-control.txt`
- Scratch (removed before yield): `/fast/scratch/hyaku/kengaku-r52/w2-W2RevA1Intent/`

## 8. Attack verdict on the item

The item asked for intent and preservation/risk, not a pass/fail on the counter. Within that scope: the series' intent is recoverable and is per-grader and descriptive; A1 preserved the population, digests, one-sided queueing and the human-confirmation requirement; A1 did not preserve the located-reading discipline at its per-test unit, and its disclosure ("same vocabulary", "before-state re-derivable", "the control set … unchanged") does not match the code in four places (§3.2, §3.5, §3.6, §3.7). The amendment's own example is misclassified by the amended counter (§3.4). Any repair is a new amendment dated before the after-run, appended to the claims file; the frozen text must not be rewritten.
