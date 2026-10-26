# Lesson draft — round-37 wave 2 (paste-ready rows for `corpus/lessons/round-38.md`)

Shape follows `corpus/lessons/round-37.md` (`## Mistakes` table: `# | observation | fix | captured by`).
Every row cites the wave-2 report and line that established it.

## Mistakes

| # | observation | fix | captured by |
|---|---|---|---|
| 1 | A wave-2 report is not integrated by being written: round-37's closure read 19 of 37 reports and none of their findings reached the landing (`.ufo/waves/round-37/falsify/F37ConnCrossCheck.md:90`). | Commit the wave and read all of it before the closure claims "wave 2 returned". | `21e6251` (37/37 committed), this round's `R38R37Integrate` |
| 2 | A calibration count that is not resolved per item over-counts: 6 of the 55 frozen round-37 mutants advertise nothing, so the count is 44, not 50 (`F37CritC1Axis.md:9`, against `plans/round-37-claims.md:19`). | Every count names its per-item map; unadvertised branches are labelled coverage, not calibration. | frozen N01–N22 `adv` cells (`R38CritClaims`) |
| 3 | A check exercised only in its failing direction cannot notice an over-strict rule: no round-37 fixture let P10 pass, so three P10 weakenings survived (`F37XMutP910.md:50`). | Mirror mutant per clause (N02, N08, N15 this round). | `F37XMutP910.md:50`–`:56` |
| 4 | The predicate's observable is part of its claim: `(exit code, DEFECT set)` cannot see a gate that recognises the genuine fixture by content, which prints the full `PREDICATE C1 pass` (`F37CritRenamed.md:47`). | Extend the observable to the sorted clause-status lines, or state the limit where the pass is quoted. | `F37CritRenamed.md:174`–`:190` |
| 5 | `wrong=0` over declarations transcribed from the gate's own output is a drift pin, not class evidence (`F37CritOverfit.md:60`). | One sentence in the counter docstring and the claims' Battery bullet: class coverage rests on kills only. | `F37CritOverfit.md:58`–`:95` |
| 6 | A lesson may quote a receipt the fix overwrote: the lesson quotes `defects=3/1 … WRONG` from a file that now reads `defects=3/3 … ok` (`F37CritCalibStatements.md:134`, `F37RevLesson.md:33`). | Re-quote every cited receipt after the fix; a pointer that no longer reproduces is a defect, not a leftover. | `.ufo/waves/round-37/build/R37AnchorSweep/fixture-receipt.txt:26,32` |
| 7 | A documented recheck command can fail as written: `sha256sum -c corpus/evidence/.../SHA256SUMS` prints 6× `FAILED open or read` from the lane root because the sums file lists bare names (`F37RevEntryQuotes.md:21`). | Run the documented command once, from the directory the clause names. | `F37RevEntryQuotes.md:21` |
| 8 | A spot-check item must be satisfiable by a legitimate fix: "the S110 63-hex cell must be gone" contradicts append-only rule 2, and the cell is still there by design (`F37RevLesson.md:29`, `corpus/lessons/round-37.md:102`). | Write items as the check that must be green (`rows=107 tokens=15 defects=0` with the erratum present), not as a state change. | `F37CritCalibStatements.md:145`–`:155` |
| 9 | A registry paragraph can describe a state that the tip no longer has: `SKILL.md:608-610` calls a green tool "a red state" and attaches "lane tip" to a five-commit-old revision (`F37CritNoHarmDiff.md:61`). | Measure a present-tense registry sentence at the tip it names, and say which revision the numbers are from. | `F37CritNoHarmDiff.md:61`–`:94` |
| 10 | A check that needs its environment documented does not: `ledger-tip` needs `refs/heads/master == HEAD` in the `--source` tree and `--work` to pre-exist (`F37RevSkillReadme.md:28`, `F37NoHarmSweep.md:121`). | Document the precondition on the row, or make the check refuse with exit 2 instead of reporting a mismatch. | closure D4 → `R38LedgerTip` |

## What wave 2 changed in the lane's own habits

- Mutation testing found the lane's *survivors*, not only its defects: 13 non-frozen gate survivors became
  the round-38 mutant list (`plans/round38_c1_verify.py:93-133`).
- Three seats report "no defect found" over their whole scope (`F37ReopenRows`, `F37RevBatteryCode`,
  `F37MutProbeCases`) — the wave is not only a defect generator, and a clean seat's scope is worth naming.
- The two seat-facing costs are unchanged and both cheap: the P10 path needs `uv` plus a warm
  `biopython==1.85` cache (`F37ProbeOnTip.md:229`), and every C1 run costs ~80 s.
