# ExecContentPins — P3c/P3d content-pin fixture (round 26, build wave, writer)

Clone: `/tmp/kengaku-r26-ExecContentPins`, branch `r26-ExecContentPins`. Observed base: `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d` (`git rev-parse HEAD`).
Pins are taken at `f11bffbf`. `git diff --stat f11bffbf e0037a8da268` touches only `plans/round-26-claims.md` and the round-start receipt, so every pinned file is byte-identical at both commits.
Axis: calibration. Git use was read-only (`show`/`blame`/`log`/`diff`). No lane writes except this report.

## Population (enumerated)
- **SHONEN evidence lines.** `git show f11bffbf:SHONEN.md | awk 'NR%2==0 && NR>=6'` gives `SKILL.md`, `LOG.md:7`, `corpus/lessons/round-8-aggregator-box3-coldrun.md:48` and `PROVINCE.md:129`. That is 3 line anchors and 1 whole-file pointer. The whole-file pointer gets 4 needles, one per box-1 claim part, giving 7 rows.
- **SCORECARD backticked `:NNN` / `path:NNN` anchors** in §Round 24 (584–625), §Round 25 (652–686) and the falsify-wave revision (696–730):
  ``git show f11bffbf:SCORECARD.md | awk '(NR>=584&&NR<=625)||(NR>=652&&NR<=686)||NR>=696{s=$0;while(match(s,/`[A-Za-z0-9_.\/-]*:[0-9]+(-[0-9]+)?`/)){print NR": "substr(s,RSTART,RLENGTH);s=substr(s,RSTART+RLENGTH)}}'``
  It prints `612: :162` · `620: SCORECARD.md:305` · `662: :244` · `703: :244`, giving 4 rows.
- **Only `:162` is strictly inside a re-derived axis table** (r24 610–618, r25 677–685, revision 721–722), so its scope is `P3d-table`. The other three sit in the same sections but outside the tables (the D14 bullet, the mapping paragraph, the revision's C1 Score cell), so their scope is `P3d-section`.
- **Excluded:** plain-text `AXES.md:15` (L668) and `PROTOCOL.md:432` (L704) — not backticked, and they point into the fleet repo. Both still resolve at fleet HEAD `a51f7db`; neither file has changed since `7c5b34f`.

## Table — `plans/fixtures/r26/content_pins.tsv` (11 rows × 13 TAB columns; condensed here)
| proposed_id | scope | source → anchor | resolved | frozen token (fixed string) | hits | status @f11bffbf |
|---|---|---|---|---|---|---|
| P3c.box.1.pointer.1.needle.1–4 | P3c | SHONEN.md:6 → `SKILL.md` | SKILL.md (file) | `## Decision table — benchmark selection` (L23) · `## Benchmark anti-patterns` (L60) · `## Production checklist — running an eval` (L568) · `## Cited local sources` (L611) | 1 each | FILE-RESOLVES ×4 |
| P3c.box.2.pointer.1 | P3c | SHONEN.md:8 → `LOG.md:7` | LOG.md:7 | `round 4: executed first authored eval` | 1 | RESOLVES |
| P3c.box.3.pointer.1 | P3c | SHONEN.md:10 → `…box3-coldrun.md:48` | coldrun.md:48 | `## Box-3 verdict` | 1 | RESOLVES |
| P3c.box.4.pointer.1 | P3c | SHONEN.md:12 → `PROVINCE.md:129` | PROVINCE.md:129 | `### Adjacent` | 1 | RESOLVES |
| P3d.r24.novelty.anchor.1 | P3d-table | SCORECARD.md:612 → `:162` | SCORECARD.md:162 | `\| **novelty** *(owned)* \| 6 → **7** \|` | 1 | RESOLVES |
| P3d.r24.D14.anchor.1 | P3d-section | SCORECARD.md:620 → `SCORECARD.md:305` | SCORECARD.md:305 | `All 149 checks recompute` (found at L307) | 1 | **DRIFTED** |
| P3d.r25.mapping.anchor.1 · P3d.r25rev.C1.anchor.3 | P3d-section | SCORECARD.md:662 and :703 → `:244` | SCORECARD.md:244 | `\| novelty \| a probe measures a construct` | 1 | RESOLVES ×2 |

TSV-only columns: `token_at_base`, `token_line_since`, `authored` (the commit that wrote the source line, and whether its tree had the token on the anchored line), `anchored_line_at_base`, `note`.

## Findings
1. **DRIFTED — the only drifted anchor is `SCORECARD.md:305`, cited in the D14 erratum at `SCORECARD.md:620`.**
   - At base, L305 reads "evidence, not a ruling."; the intended line is L307.
   - `git blame -s -L620,620 f11bffbf -- SCORECARD.md` → `94da19e`. That commit wrote `:305` against its parent tree, where `git show 94da19e^:SCORECARD.md | awk 'NR==305'` → "…All 149 checks recompute…". Its own hunk `@@ -265,0 +266,2 @@` (`git diff -U0 94da19e^ 94da19e -- SCORECARD.md`) then shifted the line +2. So the anchor was wrong from its own landing: the kagi L17→L19 failure class.
   - R25-E3 (`SCORECARD.md:648`) states `:307` in prose, not in the `supersedes \`<id>\`` form. Of L645–650, only L646 matches `SUPERSEDE_RE` (`state_check.py:192`) or a v3 `R2[5-9]-E` widening.
   - So under the section reading, v3 reports +1 MISMATCH at base. Closing it needs an R26-E row `supersedes \`P3d.r24.D14.anchor.1\`` with the token `All 149 checks recompute`. R25-E3's own `grep -n 'All 149 checks'` hits 3 lines (307, 620, 648), so it is not unique.
2. **The other 10 rows resolve to their intended content.** Each token has exactly 1 hit at base, and each authoring commit's tree already had it on the anchored line (`on-anchor` / `in-file`). The target lines are unchanged since `90a5ce8` (SKILL), `a1af83c` (LOG:7), `d8f2898` (coldrun:48), `94da19e` (PROVINCE:129), `0c16a79` (:162) and `2575be6` (:244).
3. **Strict P3d is a single anchor.** "Every backticked `:NNN` anchor in the … axis tables" (claims:136) is only `:162`, and v2 already pins it. v2's `AXIS_ANCHOR_CONTENT` needles (`**novelty**`, `**7**`) are unique only together; alone they hit 5 and 6 lines. Base P3c+P3d mismatch is 0 (strict) or 1 (section reading). Either way this count is in addition to the R26-E1–E3 "≥3" prediction, not part of it.
4. **Landing hazard (round 26 itself).** ScribeRepairRows Draft 2 inserts the R26-E3 PROVINCE correction "directly after `:119`".
   - Simulated on base, that moves `### Adjacent` 129→131, and L129 becomes "for novelty probes, and non-karpathy wiki topics (source absent).". P3c.box.4 goes red, while v2 P2c stays green because it only checks the line is in range (`state_check.py:822-823`).
   - The live uncommitted PROVINCE.md (mtime 03:12:40) appends at EOF (:174–178), and L129 is still `### Adjacent`. Keep the EOF placement. SCORECARD Draft 1 (EOF) is safe for :162, :244 and :307.
5. **Live tree:** the sha256 of the live SHONEN, SCORECARD, LOG, SKILL and coldrun files equals the `f11bffbf` blobs. PROVINCE differs only by that EOF append.
6. **Not drift: two pins sit on headings** — coldrun:48 (the verdict text is :49) and PROVINCE:129 (the routing rows are :134–143). They fix which line the pointer lands on, not that the box claim is true; this matches ScoutAnchorsInventory and RevShonenBoxes. ScoutAnchorsInventory missed `SCORECARD.md:305`.
7. **Consumer decision (ExecStateCheckV3, messaged after this report):** v3 uses all 7 P3c pins, taking the first path on each evidence line. For P3d it pins only the registered axis-table `:162`, which is the strict reading of claims:136. So the D14 drift is outside the frozen P3 population: v3's base P3c+P3d mismatch is 0, and D14 needs no R26-E row (R25-E3's prose stands as its record). D14 remains an unguarded anchor — a residual, not a v3 defect; widening P3d would need an L1 amendment.

## Verifier (separate code path: re-reads the TSV against git objects)
```
python3 -c "import csv,subprocess as s;C='/tmp/kengaku-r26-ExecContentPins'
for r in csv.DictReader(open(C+'/plans/fixtures/r26/content_pins.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE):
 f,_,n=r['resolved'].partition(':');L=s.run(['git','-C',C,'show','f11bffbf:'+f],capture_output=True,text=True).stdout.splitlines();print(r['proposed_id'],'CARRIES' if r['token'] in (L[int(n)-1] if n else '\n'.join(L)) else 'MISSING','hits=%d'%sum(r['token'] in l for l in L),r['status_at_f11bffbf'])"
```
Output: 10 CARRIES and 1 MISSING (`P3d.r24.D14.anchor.1 MISSING hits=1 DRIFTED`); every row reports hits=1.

## Files written
- `/tmp/kengaku-r26-ExecContentPins/plans/fixtures/r26/content_pins.tsv` — sha256 `b58c5952b22b4813785059b2337e317624270766d4204f16824006b14c07d94b`, 3663 B, 12 lines. Untracked; not committed.
- This report. The scratch directory `/tmp/r26-contentpins/` has been removed. ExecStateCheckV3, ExecStateSelftestRed and ExecP3Oracle were sent the fixture path.
- Installs: none (git, python3 stdlib, awk).

VERDICT: 11 content pins are frozen (7 P3c, 1 P3d-table, 3 P3d-section). One anchor had already drifted: the D14 `SCORECARD.md:305` should be :307 (self-shifted in `94da19e`), and R25-E3 does not supersede it in a parseable form. All others resolve to their intended content with unique tokens.
