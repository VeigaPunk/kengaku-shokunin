# ScribeLessonMistakes — round-26 `## Mistakes` draft (kengaku, build wave)

Scope: draft rows for `corpus/lessons/round-26.md` `## Mistakes`, grounded on the round-25 spot-check
(`corpus/lessons/round-25-verifier-spotcheck.md`). Read-only: no lane, index, jj, or fleet file written.
Base read: master `e0037a8`. Classes: `corpus/CORPUS.md` §Rules added from the kaika campaign.

## Grounding (commands run, observed)

- `git show 8ea41f9:corpus/lessons/round-25.md` line 29 and `git show master:...` line 29 both carry "by wave-2 seats".
- `git ls-tree -r --name-only 8ea41f9 .ufo/waves/round-25/falsify/ | wc -l` → `0`.
- `git log --format='%h %cd %s' -- .ufo/waves/round-25/falsify` → `8239a56` (22:01:48), `9d8a00d` (22:15:58).
- Landing `8ea41f9` commit time: `Tue Oct 20 21:44:48 2026 -0300`.
- Falsify `.md` mtimes: `ScribeMisrootSweep.md` 21:47:51, `CpJoinExec.md` 21:48:35, `SentinelNetns.md` 21:48:45,
  `RevCensusManual.md` 21:48:50. Spot-check `round-25-verifier-spotcheck.md:38-39` gives "first wave-2 report 21:49:53":
  **not reproduced**. Both values are after the landing; mtime is mutable, so the committed tree is the evidence.
- `git show 8ea41f9:corpus/SOURCES.md` → 37 rows; `master:corpus/SOURCES.md` → 42 rows (`grep -cE '^\| *S[0-9]{3,} *\|'`).
- `git log -S` on `holds 37 after round 25`, `mismatch=11`, `14 checks` → introduced at `8ea41f9`.
- Receipts: `state-check-before-6180e4f.txt:1` `mismatch=11` (v1) vs `-v2.txt:2` `mismatch=10`;
  `attrib-calibration-selftest.txt:15` `14 checks` (v1) vs `-v2.txt:19` `18 checks` (v2).
- `state-check-after-v2.txt:2-3` `OUT_OF_POPULATION` for `SCORECARD.md:558` and `:559`; `:5-10` round-25 P2e rows.
- Master text still stale: `SCORECARD.md:558` "`--selftest` 14 checks", `:559` "`mismatch=11`", `PROVINCE.md:119` "holds 37 after round 25".
- `MANIFEST.json:2744` "hyper COVERED (run-2 10/10 = 1.000)" (grep hit); routed at `MANIFEST.json:9070`.

## Draft rows (for `corpus/lessons/round-26.md` `## Mistakes`)

| id | class | mistake · evidence pointer | captured-by | fix (red run) |
|---|---|---|---|---|
| M39 | landing | Gate admit row `corpus/lessons/round-25.md:29` (as landed at `8ea41f9`) says Q10 numbers were re-derived "by wave-2 seats"; `8ea41f9` tree holds 0 falsify files (above); first falsify commit is `8239a56`. Closure's 21:49:53 timestamp not reproduced; verdict unchanged (all after landing) | QUALITY Q10 (`corpus/QUALITY.md:75-80`): "before admission" stated, no check ran it | Q13 (`QUALITY.md:97-106`). Red: `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-25.md --commit 8ea41f9` → exit 1 naming line 29's Q10 cell. **Not yet run** (script unlanded). Erratum R26-E4 in round-26.md; round-25.md bytes unchanged |
| M40 | number-drift | Round-25's own new text, correct at `8ea41f9`, went stale when `8239a56` (Amendment 2, S038–S042, hardened instruments) landed: `SCORECARD.md:558` "14 checks" (v2 = 18); `SCORECARD.md:559` "`mismatch=11`" (v2 = 10); `PROVINCE.md:119` "holds 37" (`master` SOURCES = 42; 37 was the 8ea41f9 count). Each cell carries a command; none re-derived | none inside the frozen population (see M41) | R26-E1–E3 appended corrections. Red (text, observed today): `grep -nE '14 checks\|mismatch=11\|holds 37' SCORECARD.md PROVINCE.md` hits 558/559/119. Instrument red (**not yet run**): state_check v3 P3a/P3b on base → exit 1 |
| M41 | scope | Frozen P2 population (base `6180e4f`) cannot see round-25's own new rows: `state-check-after-v2.txt:2-3` marks SCORECARD `:558/:559` `OUT_OF_POPULATION`; PROVINCE §Province-map never in P2 (spot-check `:96-98`). Landed receipt therefore reads `VERDICT: PASS` with M40's values standing; same shape as M27 | QUALITY R12 (`QUALITY.md:123`) passes vacuously over rows outside its population; R13 (`:124`) tests one-artifact-one-claim, not population coverage | P3a–P3e in `plans/state_check.py` v3 (C2). Red (**not yet run**): v3 selftest with stale 558/559/119 values → exit 1; v2 P2 results unchanged on base |
| M42 | survivor | Fleet ledger keeps the r22 point-fraction overclaim: `MANIFEST.json:2744` "hyper COVERED (run-2 10/10 = 1.000)". Exact CP95 makes it INDETERMINATE on the registered population (spot-check `:163-165`; `round-25.md` §Falsify-wave corrections, M24). Routed at `MANIFEST.json:9070`, not corrected | none: Q11 binds knowledge entries and verdicts; R5 binds lane notes; MANIFEST is closure-owned | Closure-appended MANIFEST precision note (not lane-written; history byte-identical). Red (observed today): `grep -n 'hyper COVERED (run-2 10/10' MANIFEST.json` hits `:2744`; after the note the line remains and the note names the INDETERMINATE re-verdict |
| M43 | reference-drift | SHONEN box 3 points at `corpus/lessons/round-8-aggregator-box3-coldrun.md:48` (`SHONEN.md:10`). Line 48 is `## Box-3 verdict`, but that run graded SKILL.md at `0c51208` (same file, `:93`), superseded text the lesson flags (`round-25.md` §Falsify-wave corrections, "SHONEN pointers"). P2c checks range only (`plans/state_check.py:702`, `:705`) | M26 fix (`state_check.py` P2c form + range, not content) | P3c content pin on the frozen token `## Box-3 verdict` plus a superseded-SKILL disclosure. Red (**not yet run**): v3 selftest moves the pointer to a different heading → exit 1 |

## Not minted (named elsewhere or not named by the spot-check)

- PPI reject reason (spot-check `:120`): already M33 in `round-25.md`; not re-minted.
- Reiczigel 2010 "reject (not a row)" (`round-25.md` falsify corrections): true when written; superseded by S038. Not a mistake.
- Gate range "S027–S037" (`round-25.md:36`): number-drift, corrected in-text by the falsify section; not named by the spot-check, so not minted.
- `round-25.md:16` M25 row still reads "mismatch=11": corrected in-text (`round-25.md` "M25/M26 counts" → 10). Folded into M40 as evidence only.

## Open items

- Four of five red runs (M39, M40 instrument, M41, M43) are planned and **not observed**; the scripts are in the build wave.
  I did not run sibling gates (spot-check rule).
- Observed red today: M40 text (grep hits), M42 (grep hit `MANIFEST.json:2744`).
- Calibration note: the spot-check's own 21:49:53 timestamp is unreproduced; the R26-E4 erratum should cite the tree, not an mtime.

## Installs / side effects

- No tool installed or updated. Read-only git (`show`, `ls-tree`, `log -S`) and grep only.
- Scratch snapshots at `/tmp/r26-scribe-*` (removed at end). Only file written in the lane: this report.

VERDICT: M39–M43 drafted and grounded (M39 landing, M40 number-drift, M41 scope, M42 survivor, M43 reference-drift); red runs for M39/M40-instrument/M41/M43 pending (not observed), M40 text and M42 red observed; no installs.
