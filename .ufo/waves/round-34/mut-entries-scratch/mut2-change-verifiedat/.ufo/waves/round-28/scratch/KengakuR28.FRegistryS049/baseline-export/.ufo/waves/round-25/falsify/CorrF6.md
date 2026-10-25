ATTACKS: kaika W3 F6 correction — corpus/lessons/round-24.md §Errata :147-149 (`SCORECARD.md:567` → `:569`) at tip 8ea41f9ed vs kengaku-review.md:137 (append-only, facts, closure)

## Survives
- S1 append-only. `git diff --no-ext-diff -U0 6180e4f 8ea41f9ed -- corpus/lessons/round-24.md` → one hunk `@@ -141,0 +142,16 @@`; `| grep -cE '^-[^-]'` → 0. `git log -p 6180e4f..8ea41f9ed -- <file>` → only 8ea41f9. Base 22,493 B `cmp`-equal to the first 22,493 B of tip (23,655 B). Live file `cmp`-identical to 8ea41f9ed.
- S2 history. `git log --diff-filter=A -- corpus/lessons/round-24.md` → 94da19e; there `grep -no 'SCORECARD.md:567'` → :24 (M14), :52 (disposition; :54 at tip) — exactly F6's two cites. At 94da19e SCORECARD.md:567 = blank, :569 = `## Round 23 — stream-path leg forcing …`; same at 06872d4 (W3 subject), e21f9ea, a42bb40, 6180e4f, 4e57f14, 3f371d2, 710409f. "Born stale in 94da19e" reproduces. Sibling `LOG.md:208` = r23 header at every commit 94da19e..8ea41f9ed.

## Breaks
- B1 (Medium; falsifies "Closes kaika W3 F6") the fix is born stale in its own landing commit. Resolver over `git rev-list 99cf615..8ea41f9ed` (r23 header line | :567 | :569 | errata present):
  `94da19e…710409f  569 | blank | ## Round 23 | 0`
  `8ea41f9          571 | blank | blank       | 1`
  Pristine `git archive 8ea41f9ed`: `sed -n 569p SCORECARD.md` → empty; `grep -nE '^## Round 23 ' SCORECARD.md` → `571:`. The same commit inserted capability rows `interval-reverdict` / `state-assertion-check` at SCORECARD.md:558-559 (hunk `@@ -557,2 +557,4 @@`), shifting the header +2. `git log -S'SCORECARD.md:569' -- corpus/lessons` → 8ea41f9 only: no commit that carries the errata has ever resolved it. At tip all three lesson pointers to the r23 record (:24, :54 → `:567`; :148 → `:569`) land on blank lines. That is F6's symptom, recreated by its fix; by RevF6.md:8's own test ("never pointed at a true line"), the new pointer is born stale.
- B2 (Low) the stale target is repeated at `corpus/lessons/round-25.md:53` (`round-24.md §Errata → :569`); `LOG.md:290` lists F6 among appended corrections.
- B3 (Low; root cause) :147-149 carries no recompute command. The same commit's R25-E3/E4 (`SCORECARD.md:648-649`) each carry a `grep -n …`, and QUALITY.md:94 R1 asks for "the recompute command", though R1 is worded for counts and verdicts. RevF6 verified `:569` at 3f371d2 (RevF6.md:7), and nothing re-checked it in the landing tree.
- B4 (Low; wording not verifiable) "that line was blank when cited" holds only at commit level. The jj op log, read from a scratch copy of .git+.jj, starts at `2026-10-20T21:05:23-0300 add workspace 'default'`, so no 2026-10-19 snapshot exists. round-24.md:3 claims "every pointer re-verified 2026-10-19 against the working tree", which fits pre-commit drift just as well. The errata states the write-time state as fact.

## Instrument blind spot
`python3 plans/state_check.py --summary --root <pristine 8ea41f9ed>` → `assertions=236 match=232 mismatch=0 superseded=1 offline_unverifiable=3`, `VERDICT: PASS`, exit 0, while the errata pointer is blank. P2 (state_check.py:4-8) has no lesson-pointer population (RevF6.md:32 already said so), so nothing guards this closure. QUALITY.md:105 R12's stated scope excludes it.

## Residual (adjacent; not part of F6 as stated)
- The same disposition sentence (round-24.md:54) cites corpus/README.md `:89`, `:150-151`, `:166`. At 94da19e, :166 = `plans/attrib-r22-frozen.md` while the r23 frozen row is :167, so that cite was born stale [INFERENCE: :167 intended]. At tip the r23 rows sit at :90, :153-154, :172. RevF6.md:24-25 said these cites "hold", which is false for :166 at 3f371d2. The landed errata dropped that sentence, so no landed claim is false, but these cites stay uncorrected.
- Counter-reading: if lesson pointers are pinned to the 94da19e frame, `:569` is right. But the errata pins only its history, not its instruction, while round-24.md:3 and R25-E3/E4 resolve pointers against the working tree.

## Smallest fix (not applied)
Append a dated line superseding the instruction on round-24.md:148. Anchor the header with `grep -nE '^## Round 23 ' SCORECARD.md` (571 at 8ea41f9ed; 569 at 94da19e..710409f). Apply the same fix to round-25.md:53.

## Gaps
- The live tree has uncommitted drift vs 8ea41f9ed (`cmp` → SCORECARD.md line 559, LOG.md line 286, plans/state_check.py line 195). All judgments are at 8ea41f9ed; the live r23 header is also at :571.
- Fleet `.ufo/reports/round-24/kengaku.md:43` (`SCORECARD.md:569`, a frozen round-24 report) was not judged.

VERDICT: PARTIAL — append-only and the 94da19e history survive; the closure breaks: at landing tip 8ea41f9ed `SCORECARD.md:569` is blank (header at :571, shifted +2 by the same commit), so F6's stale-pointer symptom persists in its own fix.
Installs: none (git, jj 0.45.1 already in ~/.local/bin, python3, coreutils). Scratch: /tmp/k25w2-CorrF6/{tip,jjrepo}.
