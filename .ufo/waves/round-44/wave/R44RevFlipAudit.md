# R44RevFlipAudit — outside audit of `not fired` flip-check verdicts (round 44 wave, 2026-10-26)

Seat R44RevFlipAudit, leaf, reviewer. Scope: every `Flip check (round N): … — not fired — …` line in
`corpus/lessons/*.md` (62 files), each judged against the entry/rows it concerns. Independent of
R44FlipVerdict's tool; this seat re-derived every verdict from the entry text and the filesystem.

## Method and census

- Grep `^Flip check \(round [0-9]+\): .*— not fired` over `corpus/lessons/` → exactly **3 lines**:
  `round-42.md:215`, `round-43.md:46`, `round-43.md:47`.
- Case-insensitive `not fired` over the same dir (both pages) → the same 3 lines plus two non-candidates:
  `round-43-verifier-spotcheck.md:124` (a *quotation* of the round-43.md:46 line inside the closure table —
  audited under round-43.md:46, not counted again) and `:161` (R1's fix wording, not a verdict line).
- Literal flip-check lines in lessons: round-42.md:214–215, round-43.md:44–47 (6 total; the 3 `fired` ones
  are out of scope).

## Table

| lesson:line | item | verdict claimed | true/false | evidence |
|---|---|---|---|---|
| round-42.md:215 | README.md capture (entry `tb2-circuit-fibsqrt-grader.md`) | not fired — "no entry sentence rests on README.md alone; every checkable README sentence is carried by S125-S127" | **true** | `grep -in README corpus/knowledge/tb2-circuit-fibsqrt-grader.md` → exactly 3 hits: `:52` is the *lane's* `corpus/README.md` §Frontier (different file), `:70` "The `README.md` capture is the task's own prose, read once for its example claims, not a row", `:439-440` "pinned by the C2 counter's V1, not by the probe". No `README.md:<line>` citation sources any entry sentence, so no sentence rests on it alone. Caveat: the second clause is weaker — S125-S127 are `test_outputs.py`/`instruction.md`/`sim.c` rows, not README rows — but the flip test itself passes. |
| round-43.md:46 | task.toml, setup.py, solve.sh, feal.h, SHA256SUMS (entry `tb2-feal-differential-cryptanalysis-grader.md`) | not fired — "no entry sentence rests on task.toml, setup.py, solve.sh, feal.h or SHA256SUMS alone" | **false** | `grep -nE 'task\.toml\|solve\.sh\|setup\.py\|feal\.h\|SHA256SUMS'` on the entry → the entry cites the refused files as sole sources: `task.toml:22` at `:41` ("is the verifier timeout of 1800 s"), `:122` ("the only ceiling is `task.toml:22`'s 1800 s verifier timeout"), `:240` (Mechanism row `slow-oracle-45s` → `task.toml:22` "timeout_sec = 1800.0"), `:299-302` (finding 11: "the only time bound the grader's environment actually carries"), also `:326`, `:331-332`, `:352`; `solve.sh:90` at `:230` (Mechanism row `oracle-solve-sh`), `:251-252`, `:306`, `:399`; `setup.py:4` at `:96`, `:137`, `:147`. Finding 11's ceiling sentence rests on `task.toml:22` alone — the flip **fired**. (Sub-verdict: the feal.h part alone would be true — zero feal.h citations.) |
| round-43.md:47 | merge/kengaku/ assimilation set | not fired — "merge/kengaku unchanged (R43MergeRescreen §1) and no staged entry on this round's surfaces" | **true** | Re-ran read-only in `/home/vgpnk/Projects/shokuknow/merge/kengaku`: `sha256sum SOURCES.append.md MERGE-REPORT.json MERGE-REPORT.md` → `a46458851f93…`, `c47fbe68ceac…`, `807b8451f86f…` (byte-identical to the digests recorded at round-43-verifier-spotcheck.md:125); `find . -type f \| wc -l` → `68`; `find . -type f -newermt '2026-10-24 23:33:21' \| wc -l` → `0`; `grep -rliE 'feal\|cryptanaly' . \| wc -l` → `0`. `grep merge/kengaku corpus/knowledge/` → only `benchmark-task-validity-checklist.md:88` ("deliberately not reproduced as this entry's own claim") and `contamination-transparency-card.md:38-40` ("staged, not lane-admitted") — neither rests a sentence on the package and neither is a round-43 surface. |

## Cross-checks

- My **false** on round-43.md:46 independently concurs with round-43-verifier-spotcheck.md §3 (**disagree**)
  and §5 R1, and with the frozen claims file's mined-mistake paragraph ("the entry cited `task.toml:22`
  alone … closure §3 disagreement, R1"). I did not take their word: the verdict above is re-derived from the
  entry's own lines (:41, :122, :230, :240, :299-302).
- The claimed-correct lines (215, 47) also match the spotcheck's **agree** rows (§3), again re-derived here.

## Residual risk and verification gaps

- "Rests on … alone" is a judgment call. I used the closure's own operationalization (any `<file>:<line>`
  citation of the refused item in the entry, R1 wording). Under the stricter reading — a sentence whose only
  source is the refused file — round-43.md:46 is still false: finding 11's ceiling sentence cites only
  `task.toml:22`.
- I did not re-fetch captures; all three verdicts concern entry text plus, for merge/kengaku, the staged
  package's current bytes on this host.
- The `README.md` second clause ("carried by S125-S127") was not sentence-by-sentence proven; the primary
  flip test (no entry sentence sourced to README.md) is what decides, and it passes.

Report: .ufo/waves/round-44/wave/R44RevFlipAudit.md

VERDICT: not-fired-lines-3-false-1
