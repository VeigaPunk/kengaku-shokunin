# C1ScoutSurfaces — surfaces declared outside the two tables

Axes: (1) manifest coverage — does `plans/round51-surfaces.json` anchor the declaration; (2) reach — is it a path this lane reads today, not a refusal, a sibling pointer, or an explicitly ungoverned absence; (3) rank for the next manifest — keep a row only when it is declared in the scoped PROVINCE regions and cap the list at 20.

Scope read: `PROVINCE.md` outside `## Surfaces` (lines 10–20) and `### Core` (lines 106–117). Regions: `## Refusals and reported-out scope` (22–93), `## Province map` prose including `### Frontier` / `### Adjacent` / `### Historical` (95–190; there is no `## Frontier` heading), and the round-33..50 paragraphs. Those paragraphs exist only for rounds 35–46. Rounds 44–46 are bold lines 644–648, not `##` headings. Rounds 33, 34, 47, 48, 49, 50 have no paragraph in this file (648 lines; last `##` heading is round 43 at line 570).

## Coverage fact

`plans/round51-surfaces.json` `sections` is exactly `["## Surfaces", "### Core"]`, 19 entries `SF01`–`SF19`. `plans/round51_surfaces.py` `section_rows` walks only the first table after each of those headings. A string search of the manifest found none of `Refusals`, `Frontier`, `pkg_gate`, `tb2_`, `feal_`, `Historical`, `Adjacent`. Every row below is uncovered. Restatements of an SF01–SF06 target are noted as already probed via that in-table row.

## Ranked list (20)

| # | class | declaration | manifest | why |
|---|---|---|---|---|
| 1 | should-be-a-surface | `plans/pkg_gate.py` — "this lane's own gate", PROVINCE.md:262, :284, :343, :410–411 | uncovered; SF08/SF10 probe `grader.py`, a different file | PRESENT. Standing in-lane gate, distinct from the verdict gate. |
| 2 | should-be-a-surface | Round 46, :648 — `corpus/knowledge/tb2-polyglot-c-py-grader.md` reads `polyglot-c-py/tests/test_outputs.py` @ `2fd12b88` | uncovered | Knowledge file PRESENT. Probe is not named in PROVINCE; the entry's recheck names `plans/polyglot_c_py_probe.py`, `plans/pkg-spec-r46.json`, `corpus/evidence/round46/tb2-polyglot-c-py` — all PRESENT. |
| 3 | should-be-a-surface | Round 45, :646 — `corpus/knowledge/tb2-password-recovery-grader.md` | uncovered | Same shape. `plans/password_recovery_probe.py`, `plans/pkg-spec-r45.json`, `corpus/evidence/round45/tb2-password-recovery` PRESENT. |
| 4 | should-be-a-surface | Round 44, :644 — `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md` | uncovered | Same shape. `plans/feal_linear_probe.py`, `plans/pkg-spec-r44.json`, `corpus/evidence/round44/feal-linear-probe.txt`, `corpus/evidence/round44/tb2-feal-linear-cryptanalysis` PRESENT. |
| 5 | should-be-a-surface | Round 43, :572 — `plans/feal_probe.py` + `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` + `corpus/evidence/round43/feal-probe.txt` | uncovered | All three PRESENT. Core addition, not a routing sentence. |
| 6 | should-be-a-surface | Round 42, :539 — `plans/fibsqrt_probe.py` + `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` + `corpus/evidence/round42/fibsqrt-probe.txt` | uncovered | All three PRESENT. |
| 7 | should-be-a-surface | Round 41, :474 — `plans/constraints_probe.py` + `corpus/knowledge/tb2-constraints-scheduling-grader.md` + `corpus/evidence/round41/constraints-probe.txt` | uncovered | All three PRESENT. |
| 8 | should-be-a-surface | Round 40, :423 — `plans/db_wal_probe.py` + `corpus/knowledge/tb2-db-wal-recovery-grader.md` + `corpus/evidence/round40/db-wal-probe.txt` | uncovered | All three PRESENT. |
| 9 | should-be-a-surface | Round 39, :374–375 — `plans/git_leak_probe.py` + `corpus/knowledge/tb2-git-leak-recovery-grader.md` + `corpus/evidence/round39/git-leak-probe.txt` | uncovered | All three PRESENT. |
| 10 | should-be-a-surface | Round 38, :291–292 — `plans/build_pmars_probe.py` + `corpus/knowledge/tb2-build-pmars-grader.md` + `corpus/evidence/round38/build-pmars-probe.txt` | uncovered | All three PRESENT. |
| 11 | should-be-a-surface | Round 37, :268–269 — `plans/git_webserver_probe.py` + `corpus/knowledge/tb2-git-webserver-grader.md` + `corpus/evidence/round37/git-webserver-probe.txt` | uncovered | All three PRESENT. |
| 12 | should-be-a-surface | Round 36, :246–247 — `plans/regex_log_probe.py` + `corpus/knowledge/tb2-regex-log-grader.md` + `corpus/evidence/round36/regex-log-probe.txt` | uncovered | All three PRESENT. |
| 13 | should-be-a-surface | Round 35, :234–235 — `plans/tb2_grader_probe.py` + `corpus/knowledge/tb2-protein-assembly-grader.md` | uncovered | Both PRESENT. No receipt path is named in the paragraph. |
| 14 | should-be-a-surface | Round 39–40 C1 harness — `plans/battery39/` (:411), `plans/round40_c1_verify.py` and `plans/battery40/` (:462) | uncovered | All three PRESENT. Declared as this lane's own self-assessment instruments, not tameshi's method. |
| 15 | declared-but-not-a-surface | `### Historical — absent, not governed` table, :150–163, with the ruling at :165–166 ("not current dependencies") | uncovered as rows. Duplicates of SF01–SF06 are already probed via those entries | Extras have no SF probe: `~/wikillm/llm-wiki`, `~/bench-arena`, `/proc/1299/cmdline`, `~/.config/systemd/user/qwen-coder.service`, `~/.config/llama/qwen-coder-godspeed.jinja`, `~/Projects/the-bounty-hunter`, `/tmp/bench-r{4,5,6,7}`. All ABSENT today. HF + OpenRouter left unverified, matching the row. Do not add them as live surfaces. |
| 16 | not-a-surface | `### Frontier`, :123–127 | uncovered | Topic list (unopened leads, contamination cards, judge calibration, an identity-verified endpoint, absent wiki topics). Names `corpus/README.md` §Frontier, not a reach path. Still says the three benchmark specs are unopened; rounds 35–46 narrow that later. `contamination-transparency-card.md` and `llm-judge-calibration.md` exist but this paragraph does not name them. |
| 17 | not-a-surface | `## Refusals and reported-out scope`, :22–93 | uncovered | Owner boundaries (integrator, kagi, kumitate, kasegi, kotoba, kake) and report-outs. Evidence pointers such as `corpus/evidence/round9-fleet/sibling-overlap.md` exist; they are citations, not declared reach surfaces. `:34113` and `~/Projects/bounties/` here restate SF03/SF04. |
| 18 | not-a-surface | `### Adjacent` table, :134–143 | uncovered | Routes work to kama, chousa, kotoba, protocol/aggregator, kagi, kumitate, kasegi, kake. `corpus/QUALITY.md` and `SOURCES.md` named here are already SF13/SF14. |
| 19 | not-a-surface | Province-map count prose, :119 and R26-E3..E10 at :175–190 | uncovered; the number they correct is SF14 | Corrections of the in-table "25 rows" cell. The :175–190 token is `rows=42` at `f11bffbf` and says "not future additions". Not a new surface. Do not mint a second SOURCES entry from it. |
| 20 | not-a-surface | Round 38 sibling sandbox inventory, :316–333 | uncovered | Other lanes' instruments (tameshi, kumitate, mado, kake, mori, kotodama, kaidoku). The paragraph says nothing was absorbed and no sibling file was copied into `plans/`. |

## Commands

```
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse e07f131cf7037e58a21db6e1f3986cf401ad257c
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --stat e07f131cf7037e58a21db6e1f3986cf401ad257c HEAD -- PROVINCE.md plans/round51-surfaces.json plans/round51_surfaces.py
```

HEAD and master printed `4090c3db79d11279ab5e5121ba25e74aa316e6e7`. Freeze printed `e07f131cf7037e58a21db6e1f3986cf401ad257c`. `diff --stat` printed no lines: `PROVINCE.md` and the C1 instrument are identical at HEAD and at the freeze.

Existence (`test -e` from the lane root) for rows 1–14 and the capture/spec paths named above: every one printed `PRESENT`. Historical extras and `/tmp/bench-r4` through `/tmp/bench-r7`: every one printed `ABSENT`.

Port check (`socket.connect` 127.0.0.1, 0.4s): `CLOSED 34113 ConnectionRefusedError`; `LISTEN 8791`; `LISTEN 8793`.

Manifest dump: `sections ['## Surfaces', '### Core'] n 19`, ids `SF01`..`SF19`.

No tool was installed.

## Limits

- Rounds 33, 34, 47, 48, 49 and 50 are not declared in `PROVINCE.md`, so they are not rows. On-disk instruments those rounds left (`plans/catalog_probe.py`, `plans/round33_c1_verify.py`, `plans/fixture_fence.py`, `plans/round50_c1_verify.py`, and `corpus/knowledge/benchmark-grader-semantics.md`, which `corpus/README.md` §Frontier names and this PROVINCE does not) are invisible to C1. This seat does not promote undeclared files into the next manifest.
- `:8793` answered LISTEN today. It is named inside the `### Core` row SF16 ("`:8793` not probed this round"), so it is inside a covered table, not an out-of-table declaration. Out of this list on purpose.
- HF and OpenRouter were not fetched. The Historical row already says they were not probed.
- Round 28, 29 and 29-attempt-2 sit outside the asked round-33..50 window. Their instruments (`plans/benchmark_spec_audit.py`, `plans/config_projection.py`, `plans/sources_adopt.py`, `plans/adoption_check.py`, `plans/registry_check.py`) are real and uncovered, and were left off the capped list.
- "The lane reads it" is file presence plus the declaration's own verb (core addition / own gate). Probes were not executed.
- Scratch `/fast/scratch/hyaku/kengaku-r51/C1ScoutSurfaces` was created and removed. No clone. Nothing of this seat remains on disk there.

REV e07f131cf7037e58a21db6e1f3986cf401ad257c

VERDICT: manifest covers none of the out-of-table declarations; 14 should be next-manifest surfaces (pkg_gate, twelve TB2 grader admissions r35–r46, and the r39/r40 C1 harness), the Historical table is declared but not a live surface, and refusals, frontier topics, adjacent owners, the rows=42 correction, and the r38 sibling inventory are not surfaces.
