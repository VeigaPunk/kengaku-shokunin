# ExecFreezeCensus — scoped findings (round 93, w1, report-only)

Census: the round-93 freeze-integrity gate applied in paths mode to kengaku rounds 85–91.
Full method, assumptions and raw gate output: `.ufo/waves/round-93/w1/ExecFreezeCensus/report.md`
and `census.tsv` + `receipts/` (12 runs, every one `SELFTEST cases=10 ok=10`; gate bytes
sha256 `18b01b42fb54ce658dbb98ff3afd12d06600960fae46700fec9218e73bcefcb6` = the frozen table
row; lane never mutated, work dirs in scratch).

| round | freeze | tip | intact/broken | rc |
|---|---|---|---|---|
| 85 | `99a7cb3b` (instrument landing; claims freeze `1a45aeb5` predates instruments → rc 2 demonstrated) | `88651a72` (MANIFEST closure fallback; LOG names no final tip) | 1/3 | 1 |
| 86 | `61b0e074` (round's own claims freeze; instruments inherited at `0481a6d3`) | `276abd46` (LOG tip measurement) | 2/2 | 1 |
| 87 | `21da383b` | `10de494d` | 5/0 | 0 |
| 88 | `1f267d4b` | `7fcc680b` | 4/0 | 0 |
| 89 | `0e6bb05f` | `00462b59` (attempt-2 tip; attempt-1 `a9b8a1a0` identical) | 3/1 | 1 |
| 90 | `664435cf` (commit B) | `9cf98d90` | 5/0 | 0 |
| 91 | `386184a6` (commit B) | `cefabd44` (tip D; tip C `a8de3e69` identical) | 5/1 | 1 |

Broken rows are bytes-facts, not verdicts: 85 (c1_replay, c2_debt, probe), 86 (c1_replay,
c2_repin), 89 (claim_figures), 91 (counter_pin) — each maps to edits the round itself disclosed
in LOG/lessons; 87, 88, 90 pass with zero breaches. Verdicts are stable under every alternate
freeze/tip window tried (touched counts vary, intact/broken counts do not).

FINDING CEN-85 minor round-85 bytes: broken=3 intact=1 rc 1 (window `99a7cb3b`→`88651a72`); broken=3 also at receipt tip `dc02d818`; rc 2 at the claims freeze (paths absent)
FINDING CEN-86 minor round-86 bytes: broken=2 intact=2 rc 1 (window `61b0e074`→`276abd46`); broken=2 also from first landing `0481a6d3`
FINDING CEN-87 info round-87: 5/5 intact, rc 0
FINDING CEN-88 info round-88: 4/4 intact, rc 0
FINDING CEN-89 minor round-89 bytes: broken=1 (`plans/round89_claim_figures.py`) rc 1, identical at both named tips
FINDING CEN-90 info round-90: 5/5 intact, rc 0
FINDING CEN-91 minor round-91 bytes: broken=1 (`plans/round91_counter_pin.py`, the disclosed B→B2 edit) rc 1; the r91 pinned-set tip rule anchored at B disagrees with the bytes — routed to round 94
FINDING CEN-GATE info gate ran as frozen bytes, 12/12 selftests green, rc 0/1/2 all exercised
FINDING CEN-HIST info all four broken rows correspond to in-round-disclosed edits; census adds machine-checkable counts, three rounds clean

Paths written: `.ufo/waves/round-93/w1/ExecFreezeCensus.md`,
`.ufo/waves/round-93/w1/ExecFreezeCensus/report.md`,
`.ufo/waves/round-93/w1/ExecFreezeCensus/census.tsv`,
`.ufo/waves/round-93/w1/ExecFreezeCensus/receipts/` (12 gate transcripts + `parameters.txt`).
No tools installed; no sysctls touched; scratch removed after receipt copy.
