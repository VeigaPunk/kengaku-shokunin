# F42ConnClaims — cross-document consistency at 508434ad55c709337065611691c426f05875492d

Seat: connector (leaf). Scope: every number/hash in `plans/round-42-claims.md`, the two counters' docstrings,
`.ufo/waves/round-42/claims/*.txt`, `.ufo/waves/round-42/integrate/*.txt`, `SCORECARD.md §Round 42`,
`LOG.md §Round 42`, `corpus/lessons/round-42.md`, `corpus/knowledge/tb2-circuit-fibsqrt-grader.md`,
`corpus/README.md` rows, `corpus/SOURCES.md` S125–S128. All reads were read-only; no lane file was edited.

## 1. Verified-consistent numbers (no drift)

| item | value | evidence (command → output) |
|---|---|---|
| freeze hash | `bc856d803576e182b6c3c12afc6b23f392071c25` | `git log --format="%H %s"` → `bc856d803576e182b6c3c12afc6b23f392071c25 bc856d8 round-42: freeze …`; round_close ORDER line in `integrate/measure-final.txt` (`freeze=bc856d803576e182b6c3c12afc6b23f392071c25`); `SCORECARD.md:1733` same |
| first probe run | `523b27806be0df26d2235089d845265a29f8cedf` | git log → `523b27806be0df26d2235089d845265a29f8cedf 523b278 round-42: first recorded fibsqrt probe run (receipt)`; `measure-final.txt` ORDER line `receipt_commit=523b27806be0df26d2235089d845265a29f8cedf`; LOG `523b2780` |
| landing hash | `ff14d76d32d662f7b7073a2acb049594cb740d84` | git log → `ff14d76d32d662f7b7073a2acb049594cb740d84 ff14d76 round-42: landing — battery42 (29 fixtures) …`; `SCORECARD.md:1734` |
| docs-tip hash | `508434ad55c709337065611691c426f05875492d` | git log → `508434ad55c709337065611691c426f05875492d 508434a round-42: docs — SCORECARD/LOG …` |
| 14 = 9+5 mutants | anchor X1 X3 X6 X7 X9 X12 X13 X14 X15 (9), order XO1 XO3 XO5 XO6 XO7 (5) | `claims/control-c1-nothing.txt` lists all 14; every receipt prints `MUTANTS-BY-TOOL anchor=9/9 order=5/5`; claims doc §C1; scorecard row |
| 29 fixtures | battery42 = 29 | `python3 - <<…` importing each `plans/battery42/*.py` → `a_class 6 a_route 6 a_row 6 o_clause 5 o_scan 6 TOTAL 29`; `measure-final.txt:51` `BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0`; LOG/lessons "29 fixtures" |
| 16 cases, 7/9 | `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0` | `corpus/evidence/round42/fibsqrt-probe.txt` (tail); dry table `cases=16 predicted_pass=7 predicted_fail=9`; `measure-final.txt:73` `V4 ok cases=16 mismatches_named=0/0 bad=0`; scorecard/LOG/lessons/SKILL agree |
| informed filler 7/9 | `R42CritClaims` verdict | `build/R42CritClaims.md:68` `7/9, fail`, `:73` "passes **7 of 9** checks", `:251` `VERDICT: claims-attack-defects-5-informed-filler-7/9`; `SCORECARD.md` "passes 7 of 9 (`R42CritClaims` §1)" |
| prior art 2/6 | `R42ScoutPriorArt` verdict | `build/R42ScoutPriorArt.md:20` "= 2/6", `:104` `VERDICT: prior-art-published-2/6` |
| SOURCES 117→121 | baseline `registry_rows=117` → final `registry_rows=121` | `diff` baseline vs final (last lines) → `registry_rows=117 knowledge_files=48 index_rows=48` vs `registry_rows=121 knowledge_files=49 index_rows=49`; current `grep -cE '^\s*\|?\s*S[0-9]{3}' corpus/SOURCES.md` → `121`; census exit 0 both ends, `W04=15` both |
| knowledge/index 48→49 | P8 gate 48/48 → 49/49 | `measure-baseline.txt` `P8 … index_rows=48 knowledge_files=48` vs `measure-final.txt` `index_rows=49 knowledge_files=49`; current `grep -cE '^\| `knowledge/[^`]+` \|' corpus/README.md` → 49; `ls corpus/knowledge/*.md | wc -l` → 49 |
| 8 of 89 | claims `§Frontier narrowing (8 of 89)`; `corpus/README.md:271,374` "8 of the 89 TB2 task graders"; entry `:53` "8 of 89 read" | grep |
| capture inventory | 9 files + SHA256SUMS | `ls corpus/evidence/round42/tb2-circuit-fibsqrt/` → Dockerfile README.md gates.txt instruction.md sim.c solve.sh task.toml test.sh test_outputs.py + SHA256SUMS; SHA256SUMS digests equal SOURCES/S125–S127 cells, spec pins and probe header (e.g. `test_outputs.py 6117b8ed…0438`) |
| quoted lines | `test_outputs.py:23` `assert line_count < 32000`; `sim.c:335` `for (int step = 0; step < 32000; step++)`; `instruction.md:8` stdin sentence | `sed -n` on captures → exact lines; SOURCES/lessons quotes match |
| frozen digests | all 12 pins hold | `while read d f; do sha256sum "$f"; done < claims/frozen-digests.txt` → 12× `OK` (incl. claims `2c4a5e…`, counters, probe `fc58bf3f…`, dry table, SHA256SUMS, witness modules) |
| C2 none-control | `checks=9 defects=6` (V2 V3 V4 V7 V8 V9) | `claims/control-c2-nothing.txt` tail; scorecard before-state; baseline `defects=5` (V8 ok once receipt landed) — consistent |
| C1 none-control | `BATTERY fixtures=0 … MUTANTS total=14 killed=0 survived=14 … anchor=0/9 order=0/5 PREDICATE C1 fail` | `claims/control-c1-nothing.txt`; scorecard before-state |
| stage check | `stagecheck cases=16 failed=0` | `claims/c2-stage-check.txt` |
| routed | `routed_open=5 → 10`, oldest round 39, +6 rows | baseline vs final diff; `build/R42RoutedRider.md` `VERDICT: routed-rows-16-open-10-oldest-39`; `corpus/routed-findings.jsonl` now 16 lines |
| envelope coverage | 9 of 13 claims/*.txt carry ENVELOPE | `grep -lc "ENVELOPE start" claims/*.txt | wc -l` → 9; `ls claims/*.txt | wc -l` → 13 (matches lesson §R2) |
| R5/R2 | round_close rerun fix red→green; scratch guard selftest 36/36 | `integrate/r5-round-close-check.txt` `run1_rc=0 run2_rc=0 … PASS`; `build/R42ScratchGuard.md` `SELFTEST ok=36/36` |

## 2. Drift 1 — measure-final's own Q32 envelope records a CHANGED `~/.local/bin` listing

Locations:
- `.ufo/waves/round-42/integrate/measure-final.txt:938` (the only ENVELOPE-end in the file): `ENVELOPE end 17:52:40 exit=0 local_bin_listing_before=763032563d3739aa after=77408cab9a10361a CHANGED`
- Contra: every other round-42 receipt prints the unchanged digest `763032563d3739aa` both sides — `claims/control-c1-nothing.txt`, `control-c1-attribution.txt`, `control-c1-direction-mislabel.txt`, `control-c1-hostile-escape.txt`, `control-c1-no-mutants.txt`, `control-c1-tool-edited.txt`, `control-c1-witness-as-battery.txt`, `control-c2-nothing.txt`, `witness-run.txt`, and `integrate/measure-baseline.txt` (`after=763032563d3739aa unchanged` at 17:33:32).

The measure window was `17:42:34` (`measure-final.txt:2`) → `17:52:40` (:938). Within it, `~/.local/bin/firefox` (symlink → `~/.local/opt/firefox-158.0.1/firefox`) was created: `stat -c "%y %n" /home/vgpnk/.local/bin/firefox` → `2026-10-26 17:48:46 -0300`. `measure.sh` runs inside bwrap with `--ro-bind /home/vgpnk /home/vgpnk`, so no instrument in the receipt could have written `~/.local/bin`; the change is external to the measurement (likely another seat's tooling install — the tooling directive allows installs, and `firefox` is the only `~/.local/bin` entry with mtime in the round-42 landing window). Current host listing has moved again: `ls -A /home/vgpnk/.local/bin | sha256sum` → `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52` (102 entries).

Why it matters: `corpus/lessons/round-42.md` §R2 asserts the Q32 forward leg is green — "9 of 13 files carry it … + unchanged listing digest" — counting only `claims/*.txt`. The landing measurement receipt itself (`measure-final.txt`) contradicts that pattern; the round's own top-level evidence does **not** show an unchanged `~/.local/bin` across the landing run. This does not change any counter verdict (all counters/gates still green; digest pinning confirmed in §1), and it is consistent with the firefox install happening mid-flight, but it is a genuine cross-document drift in the envelope-hygiene record between `measure-final.txt:938` and all other receipts, and the lesson's "forward leg green" sentence should not be read as covering the landing measurement.

## 3. No other drift found in the mandated set

All mandated numbers (freeze/landing/probe/docs hashes; 14 = 9+5; 29 fixtures; 16 cases; 7/9; 117→121; 48→49; 8 of 89; census W04=15; per-tool 9/9 5/5; direct=13 indirect=1; checks=9 defects=6 before / 0 after; `PINS total=2 mismatched=0`) agree verbatim across claims, counter docstrings, claims receipts, integrate receipts, SCORECARD §Round 42, LOG §Round 42, lessons, entry, SOURCES S125–S128 and README rows, with the single drift above.

VERDICT: drift-1
