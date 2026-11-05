# ScribeQuality — draft corpus/QUALITY.md criterion (round 94)

Seat ScribeQuality (leaf scribe). Draft only; the L1 integrates. Nothing in this file is
committed; the lane was read-only (`git rev-parse`/`log`/`show`/`cat-file`/`ls-tree`/`diff`
plus `git clone --shared` into scratch).

## Proposed text (append after Q74, under a new `## Round94 freeze-integrity-counter lesson` heading)

```markdown
## Round94 freeze-integrity-counter lesson

- **Q75 — a freeze-integrity counter is called discriminating only when every known false gate of the previous round is a committed control that goes red at its own designated fixture, and the counter mutates the gate under test through a CLI-path copy whose null copy stays green.** Grounding: `corpus/lessons/round-93.md` Mistakes-mined M4 ("forgery set chosen by the author bounds the counter's discrimination": the four committed round-93 forgeries were all designed by the author who wrote the W2 fixtures, so they shared its blind spots — one post-freeze commit, `--rev` = HEAD, no post-freeze table edit — and the round-93 counter then passed all five known false gates at BASE, `PREDICATE R93-C2 pass`, rc 0, `.ufo/waves/round-94/L1/controls/before-r93-counter-*.txt`). Executable half: `plans/round94_c2_counter.py` W5 generates seven CLI-path mutants of the gate under test — the `evaluate` and `parse_table` functions copied as `*_cli`, one mutation applied to the copy, `main` redirected to the copy, the in-process battery left honest — and requires each mutant to turn its designated W2 fixture RED while the unmutated CLI copy (the null) keeps all 12 W2 fixtures green (`W5 null ok fixtures_ok=12 of 12`; `W5 pass mutants=7 killed=7`); the five known false gates (three round-93 seat forgeries `x-head-not-rev`, `x-diff-rev-minus-1`, `x-table-at-rev` and the two surviving round-93 mutants `m06`, `m13`) are committed controls at `.ufo/waves/round-94/L1/controls/c2-false-*.txt`, each red at its own designated fixture (`c2-false-x-head-not-rev.txt` → `w2-rev-below-head` RED; `c2-false-x-diff-rev-minus-1.txt` → `w2-edit-revert-unrelated` RED; `c2-false-x-table-at-rev.txt` and `c2-false-m13-table-read-at-rev.txt` → `w2-lie-repaired` RED; `c2-false-m06-cne-exit0-pass.txt` → `w2-not-ancestor` RED), so known false gates passing the lane's counter go 5 → 0. A counter that shows only its own author's forgeries, or that tests the gate only through its in-process battery, measures nothing about the gate.
```

## Why this criterion, in the file's own terms

- It is the Q73 family (freeze-integrity) stated for the *counter* rather than the *table*:
  Q73 says a verdict reads "met as frozen" only when the freeze-integrity gate is green on
  the frozen table. This says the gate's own verdict is worth anything only when the gate
  was shown to reject gates it should reject — the W-1/W-4 lesson M4 defect, closed.
- It names the round-93 lesson M4 by file and section, as Q70–Q74 do.
- It has an executable half with the exact printed receipts (`W5 null ok fixtures_ok=12 of 12`,
  `W5 pass mutants=7 killed=7`, `w2-<name> RED`), the same style as Q63–Q66's "Executable
  half" sentences, so a reader can re-run it and get the same strings.
- It states the before/after pair the round claims (5 → 0 known false gates passing), so the
  criterion is falsifiable: a counter that lets any of the five through fails the bar.

## Formatting check against the file's existing style

- Q72–Q74 are one-line bullets under a `## RoundNN …` heading, each starting
  `- **QNN — <statement>.** Grounding: <file> <section>. Executable half: <command> …`.
  The draft above has exactly that shape and the same three-part order.
- The file's last heading is `## Round93 freeze-integrity lesson` (QUALITY.md:1383); the
  draft adds `## Round94 freeze-integrity-counter lesson` after Q74 (QUALITY.md:1386), so
  the numbering continues Q75 with no gap and no reuse.
- Q75 is not taken: `grep -rn "Q75" corpus/QUALITY.md` returns nothing (the Q75 hits in
  the lane are other lanes' corpora — `kotoba`, `kumitate`, `souji` — not this file).

## Measurement backing the draft (all re-run by this seat, receipts beside this file)

| what | receipt | result |
|---|---|---|
| round-94 counter at T, all five legs | `receipt-c2-at-T.txt` | `TARGET legs_passed=5 of 5`, `PREDICATE R94-C2 pass`, rc 0 |
| W5 null copy and the seven CLI-path mutants | `receipt-c2-at-T.txt` | `W5 null ok fixtures_ok=12 of 12`; `W5 pass mutants=7 killed=7` |
| the five known false gates at T | `receipt-false-gates-at-T.txt` | each `PREDICATE R94-C2 fail`, rc 1; designated fixture RED in every one |
| the before value (round-93 counter at BASE) | lane `.ufo/waves/round-94/L1/controls/before-r93-counter-*.txt` | `PREDICATE R93-C2 pass`, rc 0, for all six (the five known false gates + the round-93 gate) |

## Bound on this draft

The criterion is a *statement about what a counter must show*, not a claim that the
round-94 counter does show it. The round-94 counter does satisfy it as measured above, but
the criterion is written so that it will bind the next round's counter whether or not this
one is reused. Round 93's M4 asked for exactly this ("the three seat-built forgeries and
mutants m06/m13 become committed controls that must go red. Not yet shown able to fail");
this draft turns that ask into a standing criterion.
