# R77-C2 correction proposals — ScribeCorrectionsR77

Axes: coverage and calibration. Proposal only; no production files changed by this seat. Date: 2026-11-04. Freeze: `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`.

The blocks below are append-only alternatives, not instructions to rewrite filed lines. Keep each V3 bullet on one physical line: the frozen counter tests date and both literals on the same line (`plans/round77_c2_defect_discharge.py:219–241`). Existing integration edits were already visible during this seat's reads; do not duplicate an equivalent correction.

## V3 — append to LOG.md, round-76 block

```markdown
- **Round-76 correction (appended 2026-11-04; R76-V3).** In the round-76 Verification boundary, `agree=9 disagree=2` is superseded by `agree=8 disagree=3`; C1 `cases=7 red=6` and mutants `5/5` are superseded by `cases=12 red=11` and `9/9`; C2 `cases=10 red=9` and mutants `8/8` are superseded by `cases=14 red=13` and `12/12`. For the cross-record C2 before reading, SCORECARD.md's `wrong=12` is superseded by `wrong=13`; this does not attribute a `wrong=12` literal to the original LOG block. Filed lines remain unchanged. Values are transcribed from corpus/evidence/round76/{c1-before,c2-before,c1-selftest,c1-mutants,c2-selftest,c2-mutants}.txt, not rerun here.
```

## V3 — append to corpus/lessons/round-76.md

```markdown
## Round-76 Census and instrument readings correction (appended 2026-11-04; R76-V3)

- **Correction 2026-11-04.** In Census and instrument readings, `agree=9 disagree=2` is superseded by `agree=8 disagree=3`, and that section's `wrong=14` is superseded by `wrong=13`; the associated SCORECARD.md main-row reading `wrong=12` is also superseded by `wrong=13`. These are distinct superseded C2 readings, not a claim that this lesson originally said `wrong=12`. Final stored batteries report C1 `cases=12 red=11` and mutants `9/9`, C2 `cases=14 red=13` and mutants `12/12`. Filed lines remain unchanged; this correction transcribes the round-76 receipts and does not claim a new execution.
```

## V3 — append to SCORECARD.md, round-76 section

```markdown
- **Round-76 main-row correction (appended 2026-11-04; R76-V3).** The R76-C1 main row's `agree=9 disagree=2` is superseded by `agree=8 disagree=3`; the R76-C2 main row's `wrong=12` is superseded by `wrong=13`. Final stored battery readings are C1 `cases=12 red=11`, mutants `9/9`, and C2 `cases=14 red=13`, mutants `12/12`. Filed rows remain unchanged; these values are transcribed from corpus/evidence/round76/ receipts, not rerun here.
```

## V4 — append to LOG.md, round-76 block

```markdown
### Second-reviewer classes (round 76; appended 2026-11-04; R76-V4)

The round-76 report associated commit R (`d31feec9`) with a LOG entry named "Second-reviewer classes" that did not exist at filing time. This append records the A9 content from corpus/lessons/round-76.md; it does not assert that this LOG block existed at commit R or alter that historical tree.

- **Empty scope:** an empty routed-id scope (`ids=0`) could pass; A9 recorded the `EMPTY-SCOPE` rejection.
- **Raw-byte markdown legs:** HTML-commented text could satisfy a markdown leg (the lesson identifies D2); A9 recorded rendered-text handling instead of treating hidden markdown as discharge evidence.
- **PENDING legs:** a PENDING leg could accompany a full pass; A9 recorded `LEG-PENDING` so pending evidence cannot count as full discharge.
- **Limits retained:** `CHECK-TRIVIAL` is syntactic and executes no row-provided command. The round-76 lesson states that code fences are stripped only from the index-gate derivation, not receipt files; this block does not claim universal fence stripping or fresh execution.
```

## V6 — complete occurrence inventory and one-name text

Exact literal search, using `functions.grep` with pattern `declared-surface-resolver|province-surface-resolver-table-anchored` over PROVINCE.md and SCORECARD.md, returned two sites:

| Site | Frozen text / current observed text | One-name disposition |
|---|---|---|
| PROVINCE.md:999 | Freeze: `capability declared-surface-resolver` (backticked in source); current read: `capability province-surface-resolver-table-anchored` | Use `province-surface-resolver-table-anchored`; current integration already has it. |
| SCORECARD.md:3509 | Capability cell `province-surface-resolver-table-anchored` at freeze and current read | Retain that exact capability cell; no row reflow or replacement needed. |

The historical PROVINCE token is evidenced by `git diff 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb -- PROVINCE.md LOG.md SCORECARD.md corpus/lessons/round-76.md` (rc 0), not inferred from L1 prose. Current grep returned no legacy-name site in either file.

Append-only one-name text for PROVINCE.md:

```markdown
**Round-76 capability clarification (appended 2026-11-04; R76-V6).** The canonical capability name is `province-surface-resolver-table-anchored`, matching SCORECARD.md's round-76 capability row and plans/round76_c1_surface_resolver.py. This is a naming clarification, not a new capability or a new execution receipt.
```

Append-only one-name text for SCORECARD.md:

```markdown
**Round-76 capability clarification (appended 2026-11-04; R76-V6).** The `province-surface-resolver-table-anchored` capability row uses the same canonical name as PROVINCE.md's round-76 declaration; this append changes neither the filed row nor its evidence.
```

### Contract conflict and limit

The item requires: "Every draft must be copy-pasteable markdown and must not reflow the filed lines (append-only)." The frozen V6 implementation rejects any visible PROVINCE.md line containing `declared-surface-resolver` (`plans/round77_c2_defect_discharge.py:274–276`). Appending a clarification to frozen PROVINCE.md cannot remove its legacy literal, so an append-only-only application cannot discharge V6 from the frozen bytes. The observed worktree already contains a one-line replacement by another actor. This seat neither made nor authorizes that replacement. No counter, predicate, kill rule or frozen target was changed or reinterpreted.
