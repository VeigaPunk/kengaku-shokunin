# KnowledgeDraft — round 67 w1 (seat KnowledgeDraft, scribe)

Scope: draft the knowledge entry for the frozen torch-pipeline grader from committed bytes. Write only `W/KnowledgeDraft/entry.md`; no edits to the lane (`corpus/`, `plans/`, `corpus/evidence/**`) and no landing. No grader run, no network, no install, no subagent dispatch.

## Written

- `.ufo/waves/round-67/w1/KnowledgeDraft/entry.md` (draft of `corpus/knowledge/tb2-torch-pipeline-parallelism-grader.md`; sha256 `b2e46f4373fba8f25f5569e56ec2a7f8d293542047a35aef8a1d839771600a15`, 21464 bytes)
- `.ufo/waves/round-67/w1/KnowledgeDraft/cited/receipt.txt` (copy of `corpus/evidence/round67/pipe/receipt.txt`, sha256 `a9b9735bcc42fa673540de6e7c70cdfc45b97e008b033492033942261554f1e7`)
- `.ufo/waves/round-67/w1/KnowledgeDraft/cited/receipt.junit/{q1-ref,q2-none,q3-stub,q4-hooks-noop,q5-full-model,q6-unscaled-loss}.xml` (copies of the six junit files)
- `.ufo/waves/round-67/w1/KnowledgeDraft/cited/SHA256SUMS`
- `.ufo/waves/round-67/w1/KnowledgeDraft/check-receipt-cited.txt`, `.ufo/waves/round-67/w1/KnowledgeDraft/check-receipt-handcopy.txt`
- `.ufo/waves/round-67/w1/KnowledgeDraft.md` (this report)

## Cited S-ids

S238 (grader, `tests/test_outputs.py` at pin `2fd12b88`), S239 (instruction, `instruction.md` at pin `2fd12b88`). Both tier A per `corpus/SOURCES.md:253-254`.

## Key lines with verdicts

1. `python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt` → `CHECK ok cases=6`, `PREDICATE R67-C1 pass`, rc 0 (on the committed receipt). Verdict: PASS on committed bytes.
2. Hand-copy test: the committed receipt and its `receipt.junit/` copied into a scratch dir → `PREDICATE R67-C1 pass`, rc 0. Verdict: the checker binds bytes, not execution (named limitation in the entry).
3. Six vectors copied from receipt lines 7/9/11/13/15/17 (`exists/no_hooks/ws1/ws2`): q1-ref PPPP; q2-none FFFF; q3-stub PPFF; q4-hooks-noop PFPP; q5-full-model PPPF; q6-unscaled-loss PPFF. Each `frozen=match`.
4. Junit failure mechanisms read by python ElementTree parse (this seat): q5 ws2 `Rank 1 has too many layers: 8` (grader :144); q4 no_hooks `register_forward_hook must not be used in implementation` (:38-39); q3 `NotImplementedError` at `/app/pipeline_parallel.py:5`; q6 `mismatch at lm_head.bwd` (:163) at ws1 and ws2.
5. Grader sha `23574246…c64f` matches the committed grader and the S238 capture (`cmp` identical). Instruction sha `989bfcf0…2dcd2`.
6. No-hook rule is a literal substring test (S238 :38, :41). `register_forward_pre_hook`, `register_backward_hook` do not match; `register_forward_hook` and a comment containing it do match (string test, `/usr/bin/python3`, no grader run).
7. AFAB rule at ws1: labrat verdict H-AFAB **confirmed** — a 1F1B variant passes `test_pipeline_parallel[1]` rc 0; identical hook key order and counts (`.ufo/waves/round-67/w1/AfabLab/labrat.md`). Verified in this seat: labrat file hashes match its stated values; junit parse gives `P` for `1f1b-junit.xml` and `ref-junit.xml`, `F` for `ctl`/`ctl2`.
8. AFAB rule at ws2: **not established** (labrat ran ws1 only). Entry states it as open.
9. Labrat detector control: `case-ctl` fires the AFAB raise at :156 on `lm_head.fwd`; `case-ctl2` does not reach it (fails at :163 first). The detector is reachable only by a forward-first-entry substitution.
10. Before-count: `grep -c 'torch-pipeline-parallelism' corpus/evidence/round52/graders/executed17.lst` → `0`, rc 1. The member was not executed before this round.
11. Coverage: the lane's axis stays L0-capped at 7; `kengaku | round-25/33/51` remains open. The entry says so.

## Commands run (exit codes)

- `sha256sum` on the two round-67 source captures, the round-52 grader capture, the receipt, the six case files and six junit files — rc 0 (values in the entry).
- `cmp corpus/evidence/round52/graders/torch-pipeline-parallelism/tests/test_outputs.py corpus/evidence/round67/sources/torch-pipeline-parallelism-test_outputs.py` — rc 0 (IDENTICAL).
- `grep -n 'S238\|S239' corpus/SOURCES.md` — rc 0.
- `grep -n` on grader and case files for line numbers — rc 0.
- `/usr/bin/python3 plans/round67_c1_pipeline_probe.py --check-receipt <committed receipt>` — rc 0 (output above).
- `/usr/bin/python3 -c` string containment test on the two no-hook literals — rc 0.
- `cp` of receipt and junit into the seat dir; `--check-receipt` on the seat copy — rc 0; `--check-receipt` on the hand-copy in a scratch dir — rc 0; `sha256sum` SHA256SUMS — rc 0.
- `grep -c 'torch-pipeline-parallelism' corpus/evidence/round52/graders/executed17.lst` — 0, rc 1 (zero-match exit).
- `ls …/AfabLab/labrat.md` — rc 0 (file present at the second check, after the first check had found it absent).
- `sha256sum` on labrat cited files — rc 0; `/usr/bin/python3` ElementTree parse of labrat junit — rc 0.
- `grep -niE 'TODO|to be filled|TBD|placeholder|FIXME|lorem' entry.md` — rc 1 (no matches).
- `rm -rf -- /fast/scratch/hyaku/kengaku-r67/KnowledgeDraft` — scratch removed.

Not run: the grader (pytest / bwrap), the probe `--run` or `--selftest`, any `flock` or port 12355 listener, any network fetch, any install, any git command.

## Installs

None. No tool installed or upgraded by this seat.

## Open items (not closed by this seat)

- **Q10/Q13 second-seat re-read**: not performed. The writer cannot re-read its own entry. A non-writer reviewer-like seat must re-open S238 and S239 and report by path before admission.
- **Landing**: the entry is a draft in the wave directory. Admission to `corpus/knowledge/tb2-torch-pipeline-parallelism-grader.md`, its `corpus/README.md` index row, its coverage-map row, and the `## Gate` row in the round lesson land together in one commit (Q7). This seat did not land them, by item instruction.
- **AFAB ws2**: open. Needs a ws2 1F1B run under the lock by a labrat seat; not run here.
- **Access date**: S238/S239 access date is the freeze-day live open (claims F1, 2026-11-03), recorded from the frozen claims doc and the SOURCES rows; this seat re-hashed the committed captures and did not re-fetch the URLs.

## Rejected (summary; full list in the entry's Rejected section)

- "The grader enforces AFAB order by schedule" — rejected (dictionary-order check, confirmed at ws1 by labrat).
- "The no-hook rule forbids every hook use" — rejected (literal substring; pre-hook and backward_hook spellings do not match).
- "transformers 5.22.1 is the pinned image's version" — rejected (container pins not read).
- "13 s q1-ref run time" as receipt data — rejected (receipt carries no timing).
- "AFAB separates AFAB from 1F1B at ws2" — rejected (not run).
- "Labrat scratch as verdict before labrat.md landed" — superseded by the landed labrat.md verdict, cited by path.
