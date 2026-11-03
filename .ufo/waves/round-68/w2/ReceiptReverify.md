# ReceiptReverify — round 68 attempt 2, wave w2

Axes: coverage and calibration. Scoped result: the frozen R68-C1 receipt passes; the assigned selftest refuses 5/5 red fixtures and accepts the green receipt. Every requested anchor meets its stated value. No lane implementation, predicate, counter, case table, kill rule or target was changed.

## Execution and retained receipts

All eight assigned commands below ran with cwd `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Python subprocess runners captured combined stdout/stderr and the child return code immediately; the displayed `rc=` lines are runner captures, not inferred from output. Environment overrides were `TMPDIR=/fast/scratch/hyaku/kengaku-r68/ReceiptReverify` and `PYTHONDONTWRITEBYTECODE=1` to keep temporary files and bytecode out of the lane. The selftest work directory was created before invoking the instrument, as its existing-directory check requires.

### Frozen receipt check

Receipt: `.ufo/waves/round-68/w2/ReceiptReverify/receipt-check.txt`.

```text
$ python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/pypi/receipt.txt
CHECK ok cases=4 vector=P/F/F/F wheel_sha256=6fad8ea86492...
CHECK stored-predicate=pass derived=pass
PREDICATE R68-C1 pass
rc=0
```

Expected pass/exit 0; measured pass/exit 0. No discrepancy.

### Assigned selftest

Receipt: `.ufo/waves/round-68/w2/ReceiptReverify/selftest.txt`.

```text
$ python3 plans/round68_c1_pypi_finish.py --selftest --work /fast/scratch/hyaku/kengaku-r68/ReceiptReverify/selftest --green-receipt corpus/evidence/round68/pypi/receipt.txt
RED r1-all-p rc=1 refused=True
RED r2-probe-sha rc=1 refused=True
RED r3-dup-case rc=1 refused=True
RED r4-no-k2-clause rc=1 refused=True
RED r5-stderr-sha rc=1 refused=True
GREEN receipt rc=0 accepted=True
SELFTEST red_refused=5/5 green_ok=1 ok=True
rc=0
```

Expected `red_refused=5/5 green_ok=1`; measured exactly that, with `ok=True` and exit 0. No discrepancy.

### Per-item anchors

Receipt: `.ufo/waves/round-68/w2/ReceiptReverify/anchors.txt`.

```text
$ grep -c 'executed 2 of 8' SKILL.md
1
rc=0
$ grep -cE '^\|[[:space:]]*S240[[:space:]]*\|' corpus/SOURCES.md
1
rc=0
$ grep -c '^## Erratum (round 68)' plans/round-67-claims.md
1
rc=0
$ grep -c 'ERRATUM-68' corpus/evidence/round67/pipe/a1-mutants.txt
1
rc=0
$ test -e corpus/evidence/round68/r67-probe-selftest.txt; echo $?
0
rc=0
$ grep -c 'round67_c1_pipeline_probe' SKILL.md
2
rc=0
```

The four exact-count anchors each equal the declared 1. The existence test prints 0, meaning the file exists; the compound command also returns 0. The last count is 2 versus the declared lower bound ≥1, so it satisfies the stated rule rather than constituting a discrepancy.

## Committed-byte binding and observed tip difference

Receipt: `.ufo/waves/round-68/w2/ReceiptReverify/committed-bytes.txt` retains the commit observation, individual byte-comparison results, SHA-256 values, and exact `git show 0e52fb5d:<path>` commands with their return codes.

```text
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
7803bdd4da5bda14713f23dae8278aef479b9c19
rc=0
```

**Environment difference:** the observed HEAD is `7803bdd4`, not the assignment's stated `0e52fb5d`. This was not smoothed away. Read-only `git show` comparisons found all 14 measured/input paths byte-identical both to HEAD and to the assigned attempt-1 landing `0e52fb5d`; each git-show rc was 0. Thus the scoped predicate and anchor results do apply to the assigned committed bytes despite the tip difference. The compared paths comprise the C1 probe, base probe, grader, receipt, server log, four stderr captures, SKILL, source registry, round-67 claims, mutant record, and committed round-67 selftest receipt.

Selected byte bindings:

- C1 probe: `4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc`.
- Base probe: `2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929`.
- Grader: `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c`.
- Receipt: `c6ed306e80bf01a36a35b8f0c38f0f9e13fdff276d53444ca03caecf20a665de`.

## Interpretation, limitations and attack observation

Read the frozen claims document in full, including A1/A2, and inspected `check_receipt`, `run_selftest` and argument dispatch in the committed C1 instrument. The receipt checker re-hashes the bound captures and derives the expected vector without running the live battery. No listener was started and no live battery was run.

**Selftest strength limitation (static inspection):** `run_selftest` constructs its red fixtures with zero-valued server-log/stderr hashes (`round68_c1_pypi_finish.py:420–470`). Consequently all five reds carry binding failures independently of their named mutation. The measured 5/5 aggregate refusal does not isolate whether each named guard alone caused refusal. This is a limitation of the evidence, not an observed false green or permission to change the frozen counter. The unmodified committed green receipt did pass.

A1's disclosed timeout discrepancy remains outside this receipt-only exercise: the 900-second/exit-2 kill-rule wording is not demonstrated by these runs. Receipt consistency does not establish live-run occurrence or resolve the open provenance ruling. No broader R68-C2 gate or A2 report-contract verdict is claimed by this seat.

## Scope and cleanup

Created only this advisory report and four receipts under `.ufo/waves/round-68/w2/ReceiptReverify/`. Temporary selftest fixtures were under the exclusive scratch root, then deleted with that root; removal observed `exists=False`. No tools were installed or upgraded. No git writes, code edits, external-state changes, subagents, builds, linters or formatters were used. No supported-symbol navigation was needed; no LSP capability was exposed in this seat's tools. Blockers: none.

Parent handoff: retain these receipts as C1 re-verification evidence; assess the selftest's non-isolation separately without modifying the frozen rule. Parent owns remaining integration/report-contract gates.

## Self-evaluation

Accuracy 4/5: exact outputs and committed-byte comparisons retained; receipt-only work cannot establish live provenance. Completeness 5/5: all eight assigned commands, outputs and return codes recorded, scratch removed. Clarity 4/5: evidence is grouped by command, with some intentional duplication of raw receipts. Actionability 4/5: the non-isolated red fixtures are pinpointed, but no mutation repair is authorized. Conciseness 4/5: full verbatim output makes this longer than a summary. Overall 4.2/5. Highest-value improvements are independent single-clause red fixtures in a separately authorized future instrument and retaining the distinction between receipt consistency and execution provenance. Self-check: the assessment follows the seat's scoped acceptance criteria.
