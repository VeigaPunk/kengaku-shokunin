# P2b — round-24 re-derived axis table (7 rows), base `6180e4f`

Seat: AxisRowsScout (read-only). Base observed `6180e4f` (`git rev-parse`); pre-registration `3f371d2`.
Bytes: `git show 6180e4f:SCORECARD.md` lines 608–616 — header 608–609, **7 data rows 610–616** (matches the pre-registration's `:608-616`).
All commands offline; no endpoint contacted; no installs.

## Row 1 — novelty (`SCORECARD.md:610`) — MATCH (2/2)
- A1 `:162` resolves: `SCORECARD.md:162` = `| **novelty** *(owned)* | 6 → **7** |` under `## Rounds 12–14 … (novelty axis-move)` (`:153`) → numeric anchor 7 confirmed.
- A2 "r21 improved never converted": `:509` says `novelty **improved**`; no numeric value in the r21 (`:487-522`), r22 (`:523-550`) or r23 (`:569-581`) sections. Verdict-only claim holds.

## Row 2 — calibration (`:611`) — MATCH (3/3), 1 NOTE
- A3 "held r14": `:163` = `8 → **8 (held — breach recorded)**`.
- A4 "r19/r20 improved verdict-only": r19 `:447` and r20 `:475` both say `calibration **improved**`; neither carries a numeric row/`→` value.
- A5 "r24 held (C2)": r24 C2 `:597` = `8 → **8 (held)**`; move log `:371` = `8 | 8 (held; counts moved)`. Value 8 reproduces.
- NOTE (not counted): base also contains the integrator adjudication `corpus/lessons/round-24-verifier-spotcheck.md:15-17` (commit `a42bb40`) recording "calibration **improved** (score held 8)". Number unaffected; the row's descriptor omits the admitted move. Same base, so this is a live 94da19e-vs-a42bb40 anachronism.

## Row 3 — depth (`:612`) — MATCH (2/2)
- A6 "held (anti-double-count)": `:168` = `9 → **9 (held — anti-double-count)**`.
- A7 "r24 adds one 2-line SKILL pointer, no new rule": `94da19e` is the only r24 commit touching `SKILL.md` (`git log 6180e4f -8 -- SKILL.md`); its diff adds exactly 2 lines — `Where to learn next (round 24): corpus/SOURCES.md …` + `study paths); admission bar: corpus/QUALITY.md.` (at `94da19e:SKILL.md:617-618`), a pointer, no rule text.

## Row 4 — coverage (`:613`) — MATCH (5/5)
- A8 `PROVINCE.md` §Historical resolves: `### Historical — absent, not governed` at `PROVINCE.md:141`.
- A9 route telemetry absent: `:155` `~/Projects/bounties/ledger/telemetry.jsonl … absent`; my `test -e` today → absent.
- A10 wiki absent: `:148` `~/Projects/webzites/repos/llm-wiki … absent`; my `test -e` → absent (`~/wikillm/llm-wiki` also absent, `:149`).
- A11 bench-arena absent: `:150-151` `~/archive/bench-arena` and `~/bench-arena` absent; my `test -e` → both absent.
- A12 cap value: r24 C1 `:596` = `7 → **7 (held by the unresolvable-surface cap)**`.

## Row 5 — operability (`:614`) — MATCH (3/3)
- A13 `python3 grader.py` (rerun, lane tree) → `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully re-derives offline`, exit 0 (0.2 s).
- A14 `freeze-check OK` (capability row `:556` gives the command; rerun on a `git archive 6180e4f` at `/tmp/k25-base`) → `FREEZE-CHECK: reads=1 block_sha=1b2d6a01bfa431ec pinned=1b2d6a01bfa431ec stable=True -> OK`, exit 0.
- A15 "no new gate": `git log 6180e4f -- grader.py` last touched `0c16a79` (r14); r24 added `plans/round24_census.sh` (counting command) and capability `sources-registry` (`:557`, registry+census, no exit-gate) — no gate added.

## Row 6 — freshness (`:615`) — MATCH (3/3)
- A16 `§Province map` resolves: `## Province map — round 24 (2026-10-19)` at `PROVINCE.md:95`; all 9 `## Surfaces` rows (`:12-20`) are enumerated across Core/Historical.
- A17 "23 public sources" re-derives: `corpus/SOURCES.md` has 26 rows, 24 http rows, **23 distinct URLs** (`grep -oE 'https?://[^ |)]+' | sort -u | wc -l` → 23; S023/S026 share scale.com/swe-bench-pro), all 26 rows carry `2026-10-19`.
- A18 methods reproduce: `sha256sum` grader.py → `90c87c88…ae941f`, plans/attrib_probe.py → `489f938a…16e06b`, `~/.local/share/ds-flash-shim/shim.py` → `42d86d99…15a386` (all match the map's pins); `ss -ltn 'sport = :8791'` → LISTEN, `:34113` → no listener (matches `PROVINCE.md:102-108`). Historical rows cite prior receipts but all 11 listed paths re-`test -e` absent today.

## Row 7 — adjacency (`:616`) — MISMATCH (1/2)
- A19 "SiblingConnector-3 report-outs to kotoba, tameshi, chousa, named in the round report": resolves at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-24/kengaku.md:211` (`## Adjacency report-outs (SiblingConnector-3)`) with all three at `:213/:215/:216`; roster at `:60`, 0 URL collisions at `:195`; committed `dec4b51`. MATCH — note the report lives fleet-side, not in the lane repo, so it is not reproducible via `git show 6180e4f:`.
- A20 "no integrator arbitration": **contradicted at base** — `corpus/lessons/round-24-verifier-spotcheck.md:15-17` is `## Adjudication`: "ADMITTED after post-review fixes … Orchestrator ruling on the lane's L0: C2 is a calibration move … calibration improved (score held 8)", committed by `a42bb40` "round-24 verifier spot-check (integrator, kaika): non-author admit/reject sample + adjudication". The same file records per-axis `adjacency … unchanged`, so adjacency itself was not arbitrated; only the row's unqualified wording fails.

## Totals
`assertions=20 match=19 mismatch=1 notes=1` (6/7 rows fully MATCH; row 7 has the one mismatch, row 2 the note).
Actionable for round 25: if the re-derived table is carried forward, qualify `:616` to "no integrator arbitration of adjacency" and update `:611` to "r24 improved, score held 8 (a42bb40)".

VERDICT: P2b at base 6180e4f — 6 of 7 rows MATCH; 1 MISMATCH (adjacency "no integrator arbitration", falsified by a42bb40, adjacency scope unaffected); calibration value 8 holds; no installs.
