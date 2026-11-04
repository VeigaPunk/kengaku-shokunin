# C2LegsReplayR73

Axes: coverage and calibration. Measured replay only; no implementation, predicate, registry or target changes.

## Results

Clean shared clone master: `255c261db2119906c70195291a2b6f9f46f82a72` (freeze tip, not landing).

- Audit selftest: `SELFTEST arms=4 red=3 ok=True`, rc 0; clean, fifth-row, second-row and errata arm lines present.
- Mutants: `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=1`, rc 0.
- Audit at clone tip: `INSTRUMENTS total=106 derived=registry rows=106`, `PARSED scripts=106 failed=0`, `MISMATCH 2`, rc 1. Exactly the claims-named defects: `sources-adopt` gate-verdict lacks failure class; `round62-c1-class-survey` has `kind=census gate`. SKILL.md unchanged in freeze commit.
- Each leg directly replayed through unmodified `--lane` CLI on frozen-builder fixtures. D1 broken script: `DEFECT SCRIPT-PARSE plans/tool_bad.py:1:invalid syntax`; D2: `DEFECT \`tool-b\`:owner:sibling`; D3: `DEFECT DUPLICATE-ROW \`tool-a\`` plus the second row's bad-kind defect; D4: both swapped label/revision bindings red. All red cases rc 1; clean control rc 0. Missing-script alternative also red.

## Calibration findings / risks

1. **C1 prose target undercounts freeze-tip advertising:** frozen full gate prints `ADVERTISED total=113`, `MISSING 8`, rc 1, not the prose target 112. Base tree with amended full gate prints 112/7; legacy prints 110/5. The extra freeze-tip advertiser is `plans/round73_c2_registry_audit.py`, named by `plans/round-73-claims.md`. Three plans-only instruments are observed, not two. Adding registry rows alone cannot lower advertised count. The frozen predicate sentence uses `>=111`; this is not a claimed predicate kill or landing verdict. No rule edited.
2. M6-script-parse is killed by uncaught `SyntaxError`, not an ordinary priced rejection. Other non-null mutants remove defect lines. Frozen mutant tally nevertheless matches exactly.
3. D1 red is not in the four selftest arms; it exists in the mutants battery. Reached directly here using frozen `build_fixture(broken=True)` and actual CLI.
4. Gate and audit counters differ intentionally in observed parsing: gate counts the table header (107 rows) and excludes the hyphenated `corpus/evidence/round13-coverage/coverage_census.py` entry (105 scripts); audit skips header and includes that entry (106 rows/scripts).
5. Both audit battery modes recursively delete their entire `--work` directory; use an exclusive disposable child.

## Evidence / retained files

- `corpus/evidence/round73/w1/c2-legs-replay.txt`: commands, return codes, full required battery outputs, all four legs' exact DEFECT lines, fixture driver, clone provenance, extra gate/base-tree excerpts and mutant kill mechanisms.
- This advisory report.

No installs or upgrades. No landing verification asserted. Parent owns integrated audit/gate execution after row changes. No blockers to the scoped replay.

## Hygiene and procedural limitations

Final cleanup command used a trap plus explicit removal of this seat's scratch; rc 0, output `CLEANUP scratch_absent=1`. Scratch and fixtures removed; no retained scratch tree. No intentionally created /tmp files; gate selftest used its own TemporaryDirectory cleanup.

Initial claims read and mkdir/status were dispatched concurrently instead of awaiting the full claims read. Godspeed skill was read late. Supplemental C1 checks exceeded the core replay. Some early shell reads/searches used shell instead of specialized file tools. Initial scratch setup lacked a trap; final cleanup corrected residue, not the earlier procedural omission. No credentials read or external state remediation. LSP device unavailable among this seat's mounted tools; no symbol refactor performed.

Report: .ufo/waves/round-73/w1/C2LegsReplayR73.md
