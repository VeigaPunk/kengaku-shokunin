# F35ConnFrontier — frontier walk: corpus/README.md §Frontier & §Coverage map, 58a19f37 → dfee6fff

Seat: `F35ConnFrontier` (connector, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Date: 2026-10-25. Pre-round state: `58a19f37` (round-34 tip, "clarify frontier evaluator scope").
Landed tip: `dfee6fff631ebc5f623ba4506e5c7992a215401c` (`git merge-base --is-ancestor 58a19f37 dfee6fff` → ancestor, so the pair is pre-r35 vs post-r35).

---

## 1. Method

- `git -C <lane> diff 58a19f37 dfee6fff -- corpus/README.md` — full file diff (4 hunks).
- `git log --oneline dfee6fff` → round-35 commit chain (freeze `11d6453` → C2 `dfcd294` → C1 admit `4fe72a9` → SCORECARD `6ac9611` → Gate `056e192` → wave-1 evidence + lesson `dfee6ff`).
- Frozen counters re-run read-only in the lane at tip (both green, §3).
- Wave-1 reports read for candidates: `.ufo/waves/round-35/build/R35ScoutPriorArt.md` (40 hits), `R35ScoutTB2Oracle.md` (oracle read/replay), `R35ScoutMergePkg.md` (merge package screen).

## 2. Which frontier clause moved, by exactly how much

**One clause moved**, inside the first Frontier bullet **"Agentic benchmark task-spec audits"**:
the scoring-code clause **"Terminal-Bench 2.0's"**.

- Pre-round (round-33 sub-bullet, verbatim at `58a19f37`): *"the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity…"* → clause expressly OPEN.
- Post-round (round-35 sub-bullet, verbatim at `dfee6fff`): *"The "Terminal-Bench 2.0's" clause is discharged **for that one task only**; it stays open for the other TB2 tasks, for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity…"* → clause moved OPEN → discharged-for-one-task.

**Amount: exactly one TB2 task of 89** — `protein-assembly` @ `2fd12b88` (`tests/test_outputs.py` + `tests/test.sh` vs `instruction.md`). The tip's own coverage-map row names the same quantum and remainder: *"Discharges the round-33 frontier clause "Terminal-Bench 2.0's" scoring code for `protein-assembly` only … Not the other 88 TB2 tasks, not the correctness of the grader's literals against PDB/FPbase, not runtime execution…"*. 89 tasks confirmed by the live S100 anchor ("92 top-level entries — 89 directories plus .gitignore, LICENSE, README.md", per R35ScoutMergePkg R7). So the clause is now 1/89 discharged; 88 tasks, the SWE-bench Pro V2 beyond-round-31 grader, and runtime task validity (PROVINCE-refused) remain open.

The diff adds exactly 4 lines elsewhere, none of which moves another clause: one knowledge-index row (`tb2-protein-assembly-grader.md`), one coverage-map row (quoted above), one `### Round-35 evidence` section (S105–S107 trio + probe receipt + defects ledger). No other bullet in §Frontier or §Coverage map changed byte-for-byte.

## 3. Evidence the move is grounded (and what would have shown disagreement)

| Check | Command | Output |
|---|---|---|
| Frozen C1 counter (the moved clause's support) | `python3 plans/round35_c1_verify.py --lane .` | `checks=6 defects=0` / `PREDICATE C1 pass` (V1–V6 ok) |
| Frozen C2 counter | `python3 plans/defect_ledger.py --lane .` | `rows=5 closed=5 observed_pass=5 mismatches=0` / `PREDICATE C2 pass` |
| Wave-1 oracle cross-check | R35ScoutTB2Oracle | 6 pinned captures byte-identical to upstream @ `2fd12b88`; upstream `test_outputs.py` (path-patched) executed → `1 passed`; grader self-contained (only file read is `/app/gblock.txt`; repo-wide `git grep` empty outside the task) — agrees with the landed entry's claims |
| Wave-1 prior-art adjacency | R35ScoutPriorArt H9 | Horizon audit already reports the same task's author solution scoring zero in TB2.1 because live PDB data changed while grader literals stay; "Benchmarks as Software" (ICML 2026): 28/89 TB2 tasks defective; TB2.1 changed `protein-assembly` −7.1 pp (tbench.ai). The lane's mechanism observation is the mechanism behind Horizon's failure — the C1 entry should cite that adjacency (frame note, not a clause move) |

Disagreement evidence that would have shown the move invalid: (a) C1 counter not printing `checks=6 defects=0` (it does); (b) probe receipt with `mismatches>0` or a grader whose literals disagreed with the pinned upstream bytes (TB2Oracle found byte-identity, so no disagreement); (c) a round-35 bullet that discharged more than one task or a clause that wasn't open in the round-33 text (the open text is verbatim present); (d) a new knowledge file breaking C1's V4 42/42 shape (the landing used the already-indexed-entry amendment path consistent with R35ScoutMergePkg's measured V4 constraint).

## 4. Round-36 frontier candidates (from wave-1 reports, with the source each needs)

Landing-shape constraint (measured by R35ScoutMergePkg): C1's V4 requires committed knowledge files == index rows == 42, so a **new knowledge file cannot land**; every candidate below must land as a **dated amendment inside an already-indexed entry**, with own-work locators re-homed into the lane (`grep -c shokuknow corpus/SOURCES.md` → 0 today) and rows renumbered around live S001–S107.

1. **Toolathlon clause completion — "for Toolathlon" beyond `ab-testing` (R35ScoutMergePkg A1, +A2 lineage).** Discharge the round-33/round-35-open "for Toolathlon" clause by executing the 16-pin Toolathlon fixture probe (16/16 discriminates, reproduced byte-exact by the scout against `9be8d8fe`). *Source it needs:* the upstream probe script `lanes/kengaku/round7/toolathlon-grader-fixture-probe.py` re-homed into the lane (e.g. `plans/` + `corpus/evidence/round36/` receipt), pinned tree files at commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`, and the A2 amendment lineage (rounds 8–16) folded into the same entry with scriptless rounds (11/12/15) either re-derived or labelled `on-commit`.
2. **TB2 reference-solution live-drift (R35ScoutTB2Oracle §4).** A wave-1-discovered, not-in-the-landed-entry defect: RCSB FASTA rendering changed 2026-03-18 for `5WJ2`/`2H5Q` (chromophore `GYG`/`MYG` → `X`), so the oracle `solve.sh` as written crashes (`dnachisel…NoSolutionError: Wrong translation at locations [324-327(+), 1611-1614(+)]`) and writes no gBlock → grader scores 0; upstream `main` still byte-identical (unfixed); TB2.1 rewrote `solve.sh` and retagged the image (`20260403`) while the grader files stayed byte-identical. This changes how the task's "reference solution" must be described and is adjacent to the discharged clause's boundary ("not the correctness of the grader's literals against PDB/FPbase" — the drift is oracle-side, not grader-side). *Source it needs:* live RCSB FASTA + FPBase APIs (network), pinned tree `2fd12b88` vs TB2.1 `7131e437` (diff), Wayback pair `20260206054503`/`20260409234812`, `REVDAT … 18-MAR-26 … SEQRES` records.
3. **Second TB2 task grader probe — the still-open 88.** The clause is open for the other 88 TB2 tasks and the wave-1 instrument (`plans/tb2_grader_probe.py` pattern, frozen-case probe, receipt format) is portable per-task. Use the prior-art defect map (R35ScoutPriorArt H9: 28/89 defective per "Benchmarks as Software"; tbench.ai TB2.1 "What changed") to select the next task (e.g. one with a known instruction/grader misalignment, or the TB2.1-changed `protein-assembly` fix verification). *Source it needs:* `terminal-bench-2` tree @ `2fd12b88` / `7131e437` (any task dir's `tests/test_outputs.py`+`test.sh`+`instruction.md`), the probe instrument, and the listed prior-art papers for selection and novelty pricing.

Also flagged, not a candidate: the landed C1 entry should cite the Horizon/H9 adjacency (same task, published author-solution-zero phenomenon) — a framing repair, not a frontier move.

## 5. Falsifier limits

I ran no network fetches and no campaign tools; all wave-1 citations are taken as authored by their seats (R35ScoutPriorArt = 40 hits, R35ScoutTB2Oracle verdict `oracle-found-consistent-yes`, R35ScoutMergePkg verdict `package-2-admit-8-refuse`). The frontier movement itself is read directly from the committed README diff, which I verified byte-for-byte.

VERDICT: frontier-moved-1-candidates-3
