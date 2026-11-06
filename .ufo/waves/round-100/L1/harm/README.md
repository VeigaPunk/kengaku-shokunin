# Round 100 L1 harm battery (BASE 78460376 vs T dbe0cefa)

Runner `run_harm.sh <rev> <out>` (successor of round 99's): each revision in its own `git clone --shared`
checkout; r82c1 gets `--tip HEAD` of that checkout (round-99 M5); per check the finding SET difference
(`new`/`gone` lines, `loc=` stripped) is printed, not a count. Summary: `summary-dbe0cefa.txt`.

- Every check's rc is unchanged BASE → T (23/23).
- `anchor`: gone 11 = the 9 R100-C2 population tokens, S295 (re-bound by C1's P0 capture; amendment 1),
  and S300 `fa53d657`'s old class; new 1 = the same S300 token reclassified `abbrev-unresolved`. 33 → 23.
- `r77c1`, `r78c1`, `r81c1`, `r82c3`: each `new` line replaces a `gone` line carrying a per-member count
  (rows 333 → 341, crypto-credential 4 → 5, file-artifact 34 → 35, executed 43 → 44), plus r82c3's
  `STATUS-LINE-MISSING financial-document-processor` — the same per-member delta rounds 97–99 recorded
  (r82c3 was red at BASE and is red at T). No check turned green → red.
- `anchorline` live 0 → 0; `r82c1` DEFECT set equal at BASE and T (the five `round100-*` registry rows
  carry `none declared —` selftest cells).
- considerthese proposal 1 check (`../frozen-union-at-T.txt`): 8 historical frozen-instruments tables,
  99 rows, 0 differ at T — no closed-round instrument was edited.
