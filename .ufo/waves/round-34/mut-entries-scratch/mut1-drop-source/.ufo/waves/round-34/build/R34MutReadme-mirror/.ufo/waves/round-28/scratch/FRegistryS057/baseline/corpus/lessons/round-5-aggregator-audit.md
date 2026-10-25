# round-5 aggregator audit — kengaku-shokunin

- **Round:** aggregator round-5 (steered 16:47:37), 2026-09-28. Audited state:
  round-5 commit `782dd2d` (16:18:14). Method: one read-only reviewer L2 —
  **32 citations re-executed** (incl. a CSV join of the v2 vs round-5 battery
  reports and the canary arithmetic) + L1 adjudication of both majors
  (independently re-derived). Untracked in-flight file at audit time
  (`corpus/knowledge/bench-arena-round7-scaffold-ablation.md`, later
  `eval-design-digest-3.md`) excluded — live round-7 work, not charged here.
- **Verdict (round-5 delta `782dd2d`): NOT conformant** — 2 majors, 3 minors.

## Majors

1. **`corpus/knowledge/eval-design-digest-2.md:109` — false count, false at
   write time.** "run 2026-09-28 against the **22 files** listed above": the
   document's own enumeration is **25** distinct wiki files. Counting command
   (re-run 2026-09-28): `grep -oE '[A-Za-z0-9._-]+\.md' corpus/knowledge/eval-design-digest-2.md | sort -u | wc -l`
   → 30 distinct names, minus 5 corpus/SKILL self-references
   (`SKILL.md`, `bench-arena-fresh-run.md`, `eval-theory-notes.md`,
   `local-bench-arena.md`, `open-model-catalogs.md`) = **25** wiki files
   (rules-cited + mechanism-cited + "Skimmed" list). The wiki working copy is
   frozen (`llm-wiki` @ `e66e614`, 2026-08-08) — the surface could not drift
   after the write, so 22 was wrong when written. The same count repeats in
   `LOG.md` round-5 entry, `corpus/lessons/round-5.md` lesson 6, and
   `corpus/README.md:23` — a correction must sweep **all four mentions**
   (P-b). Forward correction entry owed next round (P-c).
2. **`corpus/README.md` index regression introduced by the audited delta.**
   `git show a1af83c:corpus/README.md | grep -n catalogs` → table row at :22
   (`knowledge/open-model-catalogs.md`); `git show 782dd2d:corpus/README.md | grep -n catalogs`
   → only the coverage-map mention at :35 — the round-5 commit **deleted the
   table row** while `git ls-tree 782dd2d corpus/knowledge/` still contains the
   file. An index row is a claim in both directions; a delta may not drop the
   row of a file it keeps. Fix: restore the row (owning lane).

## Minors

3. `bench-arena-round5-battery.md:17` vs `:36` — flip taxonomy contradiction:
   L17 counts "8 status flips (4 P→F, 3 F→P, 1 F→HARNESS_DEFECT)" which
   requires task 06, while L36 declares 06 "not a flip". The reviewer's CSV
   join confirms exactly 8 status deltas incl. 06 (F→HD, `finish=length`,
   4096 tok, `fence_found=0`) and the canary reconciles (17+8+8=33). Pick one
   terminology and sweep both lines.
4. `eval-design-digest-2.md:47` — `partial-autonomy.md:32,69,81` cited as
   "slider table + jagged-intelligence rationale"; L32/L69 carry other content,
   slider material only at L81. A quote names its location.
5. `eval-design-digest-2.md:82-83` — the "~20:1 compute overhead" figure in the
   DDL-loop note is not contained in the cited `ai-daydreaming.md:36-39`
   (loop stages verify exactly). Cite the figure's location or mark it
   opinion-by-source.

## Verified clean (re-executed, not restated)

- Battery headline numbers reproduce: 20/33 PASS; 8 deltas (03,09,13,20 P→F;
  08,12,31 F→P; 06 F→HD); sha-identity set {16,25,28,32,33}; FAIL-vs-PASS
  latency sign flip vs v2 confirmed from the joined CSVs.
- Credential sweep 0 hits (`grep -rn 'op://' corpus/ SKILL.md SHONEN.md LOG.md`;
  token/secret/cookie/bearer patterns). Append-only PASS (`round-1-aggregator-audit.md`
  = a1af83c only; `round-4-aggregator-audit.md` = 91f021c only).
- `LOG.md` round-5 entry present with resolvable pointers (it repeats the
  false 22-count — major 1). `/tmp/bench-r5/*` artifacts labeled ephemeral in
  the entry — acceptable while the decisive outputs are pasted into the
  knowledge file (they are); note the fleet proposal that ephemeral pointers
  never stand alone.
- SHONEN.md: 3 boxes checked — conformant **as to box count** against the
  3-bullet bar in force at write time (`c5abaac`, 16:16:14, 2 min pre-commit);
  but all marks are bare lane-written `[x]` with no named non-author verifier →
  effective `[~]` author-attestation, 0/3 verified for the gate. Current bar
  text has since drifted (main-repo `097c75e` + in-flight round-8 edits):
  regeneration owed on the next steered round (round 6+, steered 16:24:56 —
  first owed round after `097c75e` is round 8).

## Falsification

Majors re-check with their printed git/grep commands against `782dd2d`. If a
forward-correction entry naming 22→25 and a restored README row land in the
lane's next committed round, this lesson's open items close; the majors
themselves (append-only history) never rewrite.
