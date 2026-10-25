# ExecStateSelftestRed: P3 red-mutation fixtures (round 26 build)

Seat KengakuR26-2.ExecStateSelftestRed-4 (writer). Clone `/tmp/kengaku-r26-ExecStateSelftestRed`, branch `r26-ExecStateSelftestRed` at observed base `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d`. Files are left untracked for L1. There are 15 patches, each a `git diff` (a/ b/ prefixes) against the P3 base `f11bffbf9caa9c9e286fb32c568b81b97719656a`. `plans/fixtures/r26/state_p3/manifest.tsv` has 25 rows × 13 columns: fixture, class, patch, patch_sha256, base_rev, apply, assertion_id, base_status, expected_status, role (target|control|collateral|v2-blind), paired_with, p2_mismatch_expected, note. The assertion ids are ExecStateCheckV3's exact strings, agreed by message ("No further ID changes planned").

| fixture | mutation | assertion: base → expected |
|---|---|---|
| p3a-selftest-count / -control | SCORECARD.md:558 `--selftest` 14→17 / 14→18 | P3a.capability.interval-reverdict.selftest-checks MISMATCH→MISMATCH / →MATCH |
| p3b-province-count | PROVINCE.md:117 "10 mismatches"→11 | P3b.province.state-assertion-check.base-mismatch MATCH→MISMATCH |
| p3c-pointer-moved / -content-shifted | SHONEN.md:10 `:48`→`:49` / 1 line inserted after coldrun.md:47 | P3c.box.3.pointer.1 MATCH→MISMATCH; P2c.box.3.pointer.1 stays MATCH (v2-blind) |
| p3c-province-append | 2 lines after PROVINCE.md:119 | P3c.box.4.pointer.1 MATCH→MISMATCH; P2c.box.4.pointer.1 stays MATCH |
| p3d-anchor-shifted / -content-shifted | SCORECARD.md:612 `:162`→`:163` / 1 line after :158 | P3d.axis.novelty.anchor.1.pin MATCH→MISMATCH; collateral P2b.axis.novelty.anchor.1 →MISMATCH |
| p3e-row-removed / -file-deleted / -row-and-file-removed | corpus/README.md:93 row, corpus/lessons/round-25.md, or both | P3e.row-to-file + P3e.file-to-row lessons/round-25.md MATCH→MISMATCH |
| supersede-partial / -full-control | R26-E1 at SCORECARD EOF: `18 checks` / `18 checks` `0 failed` | selftest-checks stays MISMATCH / →SUPERSEDED |
| supersede-frozen-restatement / supersede-rederived-control | province-append + row-and-file-removed + R26-E8/E9 at SCORECARD EOF restating the frozen pins / the tree-derived state (`exists=false` `row_count=0`, `token_hits=0` + text now at :129) | P3e.row-to-file…round-25.md and P3c.box.4.pointer.1 stay MISMATCH / →SUPERSEDED |

## Evidence
- Apply: `cd <git archive f11bffbf> && git apply --check P && patch -p1 --dry-run -s < P` passes for all 15 patches. `git apply --check` on `git archive e0037a8da268` also passes for all 15 (git 2.56.0, GNU patch 2.8).
- v2 (`plans/state_check.py` sha256 8da21567…; base `mismatch=0 superseded=1`), run with `--json` on each patched tree. P2 mismatch is 0 on all trees except p3d-* (1: `P2b.axis.novelty.anchor.1` MATCH→MISMATCH). The only other P2 change is P2e OUT_OF_POPULATION row ids renumbering in p3e-row*. So v2 is blind to 13 of the 15 fixtures.
- v3 is ExecStateCheckV3's file, tested read-only at the exact current sha256 f95193e6…, with `check_p3` and the `--json` CLI. All 25 manifest rows agree (`rows=25 failing=0`), and the P2 subset is identical to v2 on all 16 trees. Earlier snapshots: ef14d648 and 39561c6e agreed with 23/23 rows; 9b5941e5 with 21/23 (the 2 failures were F4). Each fixture changes exactly its listed P3 ids, plus `P3d.out-of-population.round24.novelty.anchor.1` for p3d-anchor-shifted.
- v3 CLI on f95193e6 (exit 1 on every tree; superseded=1 unless noted), mismatch counts: base 5, control 4, red twin 5, p3b and p3c-* 6, p3d-* and p3e-* 7, frozen-restatement 8, re-derived control 6 (superseded=3), full-control 4 (superseded=2), partial 5.

## Findings sent to KengakuR26-2.ExecStateCheckV3-4 (by message)
- F1, fixed: in snapshot f64227ff the selftest-checks claim regex `--selftest\s+(\d+)` missed the backtick in "`--selftest` 14 checks". The claim was `null` (base red only by accident) and the control stayed MISMATCH. Fixed by cdf5ca19: the control is MATCH and the 17 twin stays MISMATCH.
- F2, fixed: in f64227ff, P3c refs were taken over the whole SHONEN text, so `refs.count('SKILL.md')==2` turned P3c.box.1 red at base (false red). Refs now come from the evidence lines.
- F3, fixed: in f64227ff `check_all` returned None, so `main()` raised TypeError in `counts()`. Fixed by 9f510d13.
- F4, fixed in ef14d648 (supersession laundering): in 9b5941e5, P3c/P3e/P3d superseded on the frozen pin tokens, not on values re-derived from the tree. An R26-E row restating `pointer=PROVINCE.md:129` `line=129` `token=### Adjacent` turned P3c.box.4.pointer.1 MISMATCH→SUPERSEDED. Restating `exists=true` `row_count=1` turned P3e.row-to-file MISMATCH→SUPERSEDED for the deleted lessons/round-25.md. Pre-registration C2 requires "the full re-derived value". Fixture supersede-frozen-restatement now keeps both rows MISMATCH.
- F5, fixed in ef14d648: `P3E_FILE_PATHS` (9b5941e5 `plans/state_check.py:233-238`) left out `lessons/round-25-verifier-spotcheck.md`, a base-run OUT_OF_POPULATION file with no README row. It is now included, so base gains `P3e.file-to-row.lessons/round-25-verifier-spotcheck.md` MISMATCH (a 5th base red).
- F6, fixed in 39561c6e and re-tested on f95193e6 (correction source): in ef14d648 corrections were read only from SCORECARD.md, so a PROVINCE R26-E3 could never close P3b. Now P3b reads PROVINCE and P3e reads README, each with SCORECARD as fallback; P3c/P3d read SCORECARD only, because SHONEN prose is a P2c MISMATCH. PROVINCE `- **R26-E3 (…)** supersedes `<P3b id>` — now `rows=42`` turns both P3b rows SUPERSEDED. The live italic draft (PROVINCE.md EOF) leaves both MISMATCH, so L1 must land R26-E3 in that line format. Frozen restatements in README, SHONEN or SCORECARD stay MISMATCH; re-derived ones supersede.

## Risks
- R1 (landing hazard, first flagged by ExecContentPins): an R26-E3 PROVINCE correction appended after PROVINCE.md:119 moves `### Adjacent` from :129 to :131 and turns P3c.box.4.pointer.1 red (fixture p3c-province-append). Either place it elsewhere or re-pin SHONEN.md:12.
- R2: patches carry 3 lines of context. Landed edits next to a hunk mean regenerating; the hunks are SCORECARD.md:156-161/555-561/609-615/EOF, PROVINCE.md:114-123, corpus/README.md:90-96, SHONEN.md:7-12 and coldrun.md:45-50.
- R3: the expected statuses are checked against v3 snapshots, not the integrated file. Re-run after integration.
- Observed and not mine (live tree `git status`, read-only): ` M PROVINCE.md` (03:12; R26-E3 draft at EOF), ` M corpus/QUALITY.md` (03:51; Q13 row), `?? plans/state_check.cover` (03:50; probably `python -m trace` output [INFERENCE]). This seat wrote only this report in the live tree.

Reproduce: `T=$(mktemp -d); git -C <lane> archive f11bffbf | tar -x -C $T; (cd $T && git apply <lane>/plans/fixtures/r26/state_p3/<fixture>.patch); python3 <lane>/plans/state_check.py --root $T --json`, then compare assertion_id → expected_status (base_status = unpatched $T).

## Files written in clone, all under plans/fixtures/r26/state_p3/ (sha256)
```
c66b7c4c80f137c29b6971993254fbe5241de87ac75b5388f680df274dd93acf  manifest.tsv
09ec9894aa1668ef5c1a09ecc19e37a9134f7e761430331d3d8647fe311239cc  p3a-selftest-count-control.patch
56e365fd84d40496d1a5f24d555f3c119cc8686409a70c97862c81d831bd7558  p3a-selftest-count.patch
7e717d74c8db4d575efe925c10e2b75f720decbd9f6e05acd86ac0a2c314ba24  p3b-province-count.patch
2838b700b15aa3f6d61f9743589b2835a8d015611f758ab84d7f1bcd2a0fd094  p3c-content-shifted.patch
841829921899175786e8312bed1daadbd4639328173fb18839c445459e4ee12b  p3c-pointer-moved.patch
905163ea27581608dc093695c65e2d7f8134421db565a390028c7848e251f836  p3c-province-append.patch
53667a88665f25de32a06d4bb8f0a05391fe70fd65209f8cbabae03b515fe3c4  p3d-anchor-shifted.patch
a2418991ef041263da09a4fb7ac2c208bcfbfa4eade1e3e90db4c03f4bf0187e  p3d-content-shifted.patch
2eda861ca4f62d82d31e18fc716f08060cbf81dd7cc0c1ca8d4689ecec864767  p3e-file-deleted.patch
18680f570d26a9165a49270dd6f2353dfc17b6cd8fb11a5e56d6ada37497dcf0  p3e-row-and-file-removed.patch
b5be0c72a62f9b7a2152d4d7aa769295e7d29dcfd995ef1d57f7beb1ac67dc83  p3e-row-removed.patch
fad01276a980f8bee8c7dc76ecbc5f2119d81a006231a987a4d79b4a350bfb71  supersede-frozen-restatement.patch
37caffbc7a7437f7db2d16b0dc31b06ba337282576f00d26fbb916bd81cbebd5  supersede-rederived-control.patch
66ad003777ec37c60c832dda907c24bf306d11c5ea6089801668079d5fce2fcb  supersede-full-control.patch
9346ad6dca41919bf24a56c8ef83a26aad7f4a8c5162e1394e81680a107cdff7  supersede-partial.patch
```
Installs: none.

VERDICT: 15 patches plus a 25-row manifest; every P3 class (a–e) goes red, each against a green control or base. All 25 rows agree with the current v3 (f95193e6), and P2 matches v2 on 16 trees. The fixtures surfaced 6 instrument defects (F1–F6), all fixed by ExecStateCheckV3. Open for L1: land R26-E3 in the SUPERSEDE line format (F6) and avoid the R1 landing hazard.
