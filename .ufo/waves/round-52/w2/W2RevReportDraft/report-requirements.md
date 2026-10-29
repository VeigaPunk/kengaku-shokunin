# kengaku round 52 — report requirements checklist (for the L1 to tick)

Target file: /home/vgpnk/Projects/shokunin/.ufo/reports/round-52/kengaku.md (NOT YET WRITTEN at review time).
Basis: .ufo/prompts/kengaku-round-52.md §2, §2b, §4, §5, §6; plans/round-52-claims.md (frozen at 1315234, A1–A5);
PROTOCOL.md §Gate standard, §File contract, §Promotion gates; LEARNING.md trend table; SHONEN.md (4 boxes).
Lane tip observed at review: master = 87301bacca90c03fa915716fbe6d7023762c5ab3 (ahead=0 behind=0, untracked=16).

## A. Required sections, in this order (headings exactly; marker rule: missing sections other than Sources & frontier / Trend verdicts = round FAILED)
- [ ] `## Work performed` — FIRST line names the declared claims: R52-C1 (novelty 8->9) and R52-C2 (operability 8->9); then one bullet per work item, each with an evidence pointer (path:line, command output, or commit hash). State that coverage 7 is NOT claimed (open L0 kengaku round-25/33/51) and that the stagnation nudge is not invoked.
- [ ] `## Landed changes` — every change tied to a LOG.md entry AND the commit hash carrying it.
- [ ] `## Before → after measurements` — one block per claim: counting command + the commit it was measured against (not bare HEAD; lane tip hash).
- [ ] `## Sources & frontier` — conformance item (not a marker predicate); see section D.
- [ ] `## Trend verdicts` — exactly three verdicts: expansion, quality, discernment; each one of improved | harmed | unchanged | unprovable-but-better; evidence per verdict; no scalar.
- [ ] `## SHONEN` — heading appears exactly once (`grep -c '^## SHONEN' <report>` must print 1); then one line per SHONEN.md box (see section E).
- [ ] Report extras (§5.6): `Stale-lane` line (respawn-per-round driver; no other mission open); tool-install line (record tool/version/channel/reason, or state none).

## B. Claim-level measurements (what the Before → after block must carry)
R52-C1 (novelty), frozen counter `python3 plans/round52_c1_grader_audit.py --lane .`
- [ ] Before (base 30801b47): TASKS classified=0; CAPTURES present=0; CLASS V0=89; CANDIDATES 0; CONFIRMED new=0; PRIOR-ART ok=False urls=0; `PREDICATE R52-C1 fail` (exit 1).
- [ ] After: paste the LITERAL output and exit code at the final landing commit. Measured at master 87301ba (this review, archive copy): TASKS total=89 records=89 classified=88; CAPTURES expected=184 present=183 mismatched=0; CONFIRMED new=0; PRIOR-ART ok=False urls=0; LABELS agree=0 of 0; PREDICATE R52-C1 fail, exit 1. Do NOT write pass. Do NOT re-fetch sanitize-git-repo.
- [ ] A5 line(s) printed separately: `A5 EXCLUDED listed=1 digest_pinned=1`, `A5 CAPTURES present+pinned_excluded=184 of 184`, `A5 TASKS classified+excluded=89 of 89`, `PREDICATE R52-C1-A5` (measured 87301ba: fail). The report must say A5 is additive and does NOT replace the literal verdict; novelty stays 8 unless the literal predicate passes.
- [ ] Legs not met at master: (3) CONFIRMED new>=2 — corpus/evidence/round52/confirmations.json ABSENT; (4) PRIOR-ART ok=True urls>=3 — corpus/evidence/round52/prior-art.md ABSENT. Report must say which legs are met and which are not, with the numbers.
- [ ] LABELS agree/total reported (evidence only; labels.json ABSENT at master -> report 0 of 0 or the real value).
- [ ] Score rule recorded: phenomenon-new (novelty 8->9 possible) vs phenomenon-known (novelty held at 8). Row must say which case happened.
- [ ] Stale receipts: .ufo/waves/round-52/claims/c1-after.txt shows CAPTURES present=89 and TASKS classified=89 (pre-A2 / pre-A5). It is NOT the final after-run. Report must cite the final receipt, or label the stale one as historical.
- [ ] Controls (each must FAIL the predicate; receipts under .ufo/waves/round-52/claims/): c1-control-nothing, c1-control-name-only, c1-control-blind-class, c1-control-drop-capture. ABSENT at review time (`ls .ufo/waves/round-52/claims | grep -i control` -> 0). Each needs its receipt + the expected failing leg named.

R52-C2 (operability), frozen counter `python3 plans/round52_c2_registry.py --lane .`
- [ ] Before (base 30801b47): ADVERTISED total=72; REGISTERED total=44 rows=46; MISSING 28; INCOMPLETE 0; ENTRY-MISSING 0; SELFTEST-UNBACKED 1 (`order-check`); PREDICATE R52-C2 fail (exit 1).
- [ ] After: final receipt at the landing commit. Measured at master 87301ba (this review): ADVERTISED total=72; REGISTERED total=72 rows=74; MISSING 0; INCOMPLETE 0; ENTRY-MISSING 0; SELFTEST-UNBACKED 0; PREDICATE R52-C2 pass, exit 0. Note: `rows=74` vs `total=72` — the 2-row difference must be explained (duplicate or non-entry rows) or the reviewer will catch it.
- [ ] Stale receipt: .ufo/waves/round-52/claims/c2-after.txt still prints SELFTEST-UNBACKED 1 and PREDICATE R52-C2 fail (pre-A3). Final receipt must be the corrected-parser run (Amendment A3). c2-after-w1rows-pre-scorecard.txt is a pre-scorecard intermediate; say so if cited.
- [ ] Controls (each must FAIL): c2-control-nothing (MISSING 28), c2-control-empty-cells (INCOMPLETE 28), c2-control-drop-row (MISSING 1), c2-control-false-selftest (SELFTEST-UNBACKED 1). ABSENT at review time -> same as C1 controls.
- [ ] Causal separability sentence present (C1 never reads SKILL.md registry; C2 never reads captures).
- [ ] Round-51 defects routed: D1 closed by C2 (rows for round51_surfaces.py / round51_routing.py); D2 LOG erratum (present in LOG.md at the "Round-51 erratum (round 52…)" heading, ~line 1598 — cite its commit); D3 named in lesson (not reproduced by counter); D4 named as open `vacuous` class, not claimed.

## C. Commits, LOG, SCORECARD, lesson, knowledge
- [ ] Every landed change has a LOG.md entry (round-52 LOG entry ABSENT at master 87301ba; only the round-51 erratum exists) and a commit hash.
- [ ] Amendments A1–A5 disclosed in the report, each with a cited receipt or finding; A1 and A2 explicitly asked to be attacked by wave 2 — report must cite the wave-2 findings.
- [ ] Wave shape disclosed: frozen claims say "two v1 waves, total 64 (32 + 32)". Actual: wave 1 = 35 seats (w1-results.json has 35 entries), wave 2 = 33 seats (w2-dispatch.json counts.total 33) -> 68 total. Still inside the run-11 64–128 band; the deviation from the frozen 32+32 must be named.
- [ ] Attack share (>=25%) per wave, numerically: wave 1 = reviewer 5 + critic 3 + mutation-tester 1 = 9/35 = 25.7% (no labrat seat in wave 1); wave 2 = reviewer 7 + critic 3 + mutation-tester 2 = 12/33 = 36.4% (no labrat). Planner held by L1 (claims wave-shape ruling) — state it.
- [ ] Role mapping sentence: "bounded planning data-walk rides a scout/connector item" (claims) — say which item.
- [ ] SCORECARD.md: row(s) for novelty (C1) and operability (C2) with score delta, evidence pointer, counting command, measured commit. Verify the round-52 row(s) exist; none were found in the grep for 'round 52' (only older rounds).
- [ ] corpus/lessons/round-52.md ABSENT at master. Must contain `## Mistakes` (class · evidence pointer · captured-by · fix; fix shown able to fail, or `Found none` + the sweep command and output) and a `## Gate` block (URL, access date, <=25-word located quote per new SOURCES row; rejections with reason + flip condition; every status/recheck/used-by change old->new).
- [ ] C1 is the sourced claim: its knowledge entry and the lesson Gate cite the S### ids opened this round (TB2 pin and prior-art primaries). At master SOURCES.md still has 171 rows: zero rows opened/added this round -> the sourced-claim leg is unmet unless rows land.
- [ ] corpus/knowledge/tb2-*-grader.md: the 12 hand-read entries are the basis of "never read by this lane" — the report must show `ls corpus/knowledge/tb2-*-grader.md | wc -l` before (12) and after.
- [ ] Round-51 closure: `corpus/lessons/round-51-verifier-spotcheck.md` exists (156 lines) — turn each disagreement into a QUALITY.md criterion or fix, or say why not (§5.5). QUALITY.md exists.
- [ ] considerthese/ exists (8 dated files 2026-10-19…2026-10-26). §10 requires: mine at most ONE still-unimplemented proposal, landing as lesson/QUALITY criterion/SOURCES row citing `considerthese/<file>` + date — OR a report line saying none was mined.
- [ ] Assimilation: either an assimilation block (theme, 1–3 entries, id-collision check, census, quarantine slice verdicts) OR the exact line `Assimilation: none` in Sources & frontier (no penalty).

## D. Sources & frontier (conformance item — also a verdict-free section)
- [ ] Census before: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` at round start, output + exit code pasted. SOURCES.md EXISTS, so round-start exit must be 0 (exit 2 is only expected when the file is absent). No round-start receipt was located in the wave dir (verify).
- [ ] Census after: same command, exit code 0 required. Measured at master 87301ba: exit 0; warnings W04 duplicate-url lines (e.g. S069, S071, S075, S076, S100) — warnings allowed, state them.
- [ ] Rows before->after with the counting command: at master 87301ba, registry data rows = 171 (same as base 30801b4 = 171). Any row added must be counted by tier.
- [ ] Rows added by tier; rows touched old->new (status/recheck/used-by); frontier rows advanced.
- [ ] If the lane has no corpus/ writes -> exact `SOURCES: unchanged — ...` line. Lane HAS corpus/, so this line is not applicable.

## E. SHONEN (one line per box; four boxes; all [~] unless a NAMED non-author verifier exists)
- [ ] `grep -c '^## SHONEN' <report>` prints 1.
- [ ] `[~] SKILL.md contains real decision tables, error patterns, checklists, cited sources` (evidence: SKILL.md)
- [ ] `[~] At least one end-to-end domain task executed and logged in LOG.md` (evidence: LOG.md:7)
- [ ] `[~] Instructions executable by an agent without oral context` (evidence: corpus/lessons/round-8-aggregator-box3-coldrun.md:48 — resolves to `## Box-3 verdict`)
- [ ] `[~] No cross-domain bleed (PROVINCE.md still accurate)` — evidence pointer PROVINCE.md:129 is a BLANK line (verified: `sed -n 129p` prints empty). Not a resolvable pointer; repoint it or the box fails §4 `[~]` rule. Lane's own dispatched seats do not count as non-author verifiers (PROTOCOL §Promotion gates), so no `[x]` line is available this round.

## F. Closure hygiene (last)
- [ ] Pre-report gate: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-remote origin refs/heads/master` MUST print the final lane hash (not an older one).
- [ ] Inherited state: jj-lane state reports untracked=16 at review; resolve per PROTOCOL (commit under this round's entry, or revert) and name it in the report.
- [ ] Report commit only via: `/home/vgpnk/Projects/shokunin/scripts/hyaku/fleet-commit.sh --as kengaku -m "round-52: kengaku report" -- .ufo/reports/round-52/kengaku.md`. Round-end lane commit via jj-lane.sh only.
- [ ] Report lands LAST and cites the pushed lane hash; file the report only after WAVE-DONE for every launched wave (run-9 lesson).
- [ ] Scratch: $HYAKU_SCRATCH/kengaku-r52 removed by the L1 after landing; no `/tmp` evidence paths cited (§7.5).
- [ ] Every number in the report re-derives from committed bytes (no `/tmp` or scratch pointers).

## G. Items the L1 is most likely to miss (ranked)
1. R52-C1 is NOT landed at master: no confirmations.json, no prior-art.md, no labels.json -> literal `PREDICATE R52-C1 fail`. Writing "pass" or citing the A5 line as the verdict is the single biggest failure mode.
2. All 8 control receipts (4 C1 + 4 C2) absent from .ufo/waves/round-52/claims/. The frozen claims require them.
3. Stale receipts in claims/ (c1-after.txt pre-A5/A2; c2-after.txt pre-A3) are presented as the after-run.
4. A1 implementation gap: plans/round52_c1_grader_audit.py:193 sets candidate = bool(p1) OR cls in (V1,V4); CONFIRMED gate at :308 uses that flag. Amendment A1 says a vacuity candidate needs >=1 P1 test. Result: pytorch-model-recovery and torch-tensor-parallelism (both P1=none per the counter's own output) are CANDIDATES. The report must disclose or fix this; the A1 P1 count is not printed by the counter (p1_tests/p1_tasks are computed, never printed).
5. Wave shape deviation 68 vs frozen 64 (32+32) not disclosed.
6. SHONEN box 4 pointer PROVINCE.md:129 is blank.
7. Round-52 LOG entry, lesson file (corpus/lessons/round-52.md with Mistakes and Gate), SCORECARD rows, and SOURCES rows (171 -> ?) all absent at master.
8. Discernment verdict: wave-2 seats are lane seats (PROTOCOL: a subagent the lane dispatched is still the lane). `improved` for discernment needs an outside spot-check; without a named non-author reviewer use `unchanged` (or unprovable-but-better with a named non-author).
9. Pre-report gate: ls-remote must print the final hash; a report written before the last lane commit fails the pre-report gate.
10. The C2 `rows=74` vs `total=72` gap unexplained.
