ATTACKS: kaika W3 F12 round-25 correction in corpus/knowledge/paired-eval-uncertainty-reporting.md — append-only, git lineage claims, closure scope

1. Append-only: SURVIVES.
- `git diff 6180e4f 8ea41f9ed -- corpus/knowledge/paired-eval-uncertainty-reporting.md` → `8 insertions(+), 0 deletions(-)`, one hunk `@@ -47,3 +47,11 @@` appending `## Corrections (round 25, 2026-10-20)`. The quoted claim line ("Extends the README “Statistical reporting” coverage row...") stays byte-identical — QUALITY R1's old-line-intact check holds.
- Full file history: only `94da19e` (creation) and `8ea41f9` (round-25 correction) ever touch the file.

2. Factual — "coverage row created in the same commit as this entry (94da19e)": SURVIVES, every leg reproduces.
- `git show --stat 94da19e` → `corpus/README.md | 98 +++` AND new `corpus/knowledge/paired-eval-uncertainty-reporting.md | 49 +++` in one commit.
- `git log -S 'Statistical reporting for paired evals' -- corpus/README.md` → only `94da19e`; the after-receipt commit `06872d4` touches only `corpus/evidence/round24-census/after.txt`.
- `git show 94da19e^:corpus/README.md | grep -c 'Statistical reporting'` → 0; same for round-23 tip `99cf615` → 0; `git cat-file -e 94da19e^:corpus/knowledge/paired-eval-uncertainty-reporting.md` → absent (entry born there too).
- Base coverage map (`99cf615:112-125`) has 11 rows, none statistical — "opened new coverage rather than extending a held row" survives even against the nearest neighbor ("Eval theory" digest row, a different area). "Same commit" is also what QUALITY Q7 requires, so F12 was a wording defect, as the correction says ("wrong in kind").
- F12's own citation reproduces: the row is `corpus/README.md:212` at `6180e4f` and at round-24 tip `06872d4`.

3. Factual — extension claim survives only for r8/r11/r12: SURVIVES.
- `git ls-tree 94da19e^ corpus/knowledge/` contains bench-arena-round8-horizon.md, bench-arena-round11-power.md, bench-arena-round12-ladder.md — all pre-date the entry.
- Inherited characterizations spot-check clean: round8 has 4 "paired" hits; round11:19,55 "MDE d=0.35"/"planning MDE"; r12 ordered ladder + second task family per corpus/README.md:123 (tip).
- Deviation note (no defect): RevF12's fix spec (.ufo/waves/round-25/build/RevF12.md) also listed `bench-arena-round7-noise-n25.md` as retained extension; the correction omits it — correctly, since the original paragraph cites round7 only as a lag-1/IID caveat, not an extension claim.

4. Closes F12 as stated: SURVIVES.
- F12 (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kengaku-review.md:143`): extends target created this round, not on base map. The correction concedes exactly this, re-scopes to r8/r11/r12, dates itself (landing commit `8ea41f9` = 2026-10-20 21:44:48 -03, matching the "2026-10-20" header), and attributes "reviewer RevF12" — consistent with SCORECARD.md:59 ("F12 Extends target | open (RevF12) | correction appended to paired-eval-uncertainty-reporting.md") and LOG.md:290-291 ("corrections appended for ... F12").
- One-command recheck of the load-bearing fact: `git log --oneline -S 'Statistical reporting for paired evals' -- corpus/README.md` → `94da19e`.

Residual risk / gaps (both Low, neither breaks the correction):
- The correction names its evidence commit but, unlike R1 count corrections, carries no literal recompute command; it is nonetheless checkable by the single command above.
- Pre-registration (`plans/round-25-claims.md` + Amendment 1) never mentions F12 or wave-2 knowledge corrections; closure rests on SCORECARD/LOG rows, not prereg. Consistent with the prereg's C1/C2 scope — scope observation, not a violation of a frozen rule.

No tool installs (read-only git/grep only).
VERDICT: SURVIVES — append-only (8+/0−), every git-lineage claim reproduces (row and entry both born in 94da19e, absent at 94da19e^ and 99cf615), and the concession + re-scope answers F12 exactly as stated.
