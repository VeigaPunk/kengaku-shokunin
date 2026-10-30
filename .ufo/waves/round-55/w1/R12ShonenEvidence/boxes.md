# SHONEN box evidence — seat R12ShonenEvidence (kengaku round 55, w1)

Non-author evidence for the four `[~]` boxes in `SHONEN.md`. All commands run
2026-10-30 from `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (lane working
tree, base-tip freeze `798f5e9e…` + landed before-receipts; no lane writes).
Raw run bytes: `grader-selftest.out`, `controls-selftest.out`, `case-abbrev.out`
in this directory.

## Box 1 — SKILL.md decision tables / error patterns / checklists with cited sources → SUPPORTED

SKILL.md (1,370 lines) carries all three required shapes:
- **Error patterns:** `## Benchmark anti-patterns`, 19 numbered entries, each
  closing with a cited source path.
- **Decision tables:** `## Route-telemetry interpretation` (Observation |
  Interpretation | Action, 6 rows) and the `Planning-horizon & transcript-shape
  probes` cell-semantics table.
- **Checklists:** the r8/r9 "Measurement rules" numbered list, each rule citing
  the round that established it.

Sampled citations, resolved this session:
1. **File cite** (anti-pattern 16): `corpus/evidence/round8-horizon/run.log:81-83`
   → `test -e` OK (2,353 bytes); lines 81–83 read `A-INC: 7/10`, `A-MONO: 0/10`,
   `A-CKPT: 1/10` — exactly the figures the pattern's text asserts.
2. **File cite** (anti-pattern 13): `corpus/evidence/round9-fleet/harness-mutation.md`
   → `test -e` OK (17,372 bytes).
3. **Command cite** (anti-pattern 14): `python3 grader.py --selftest` →
   executed, **exit 0**, tail `[selftest] ALL PASS` (S6/S7 stats anchors PASS;
   full output in `grader-selftest.out`; 2.73 s wall).

## Box 2 — end-to-end domain task executed and logged in LOG.md → SUPPORTED

Latest landed round entry: **Round 54 + "Round-54 measured close"** (LOG.md tail,
2026-10-30). It names the executed frozen commands and receipt paths; every named
receipt exists and its bytes match the entry's claims:
- `.ufo/waves/round-54/integrate/c1-after.txt` → `SETUP header.bin absent`,
  `PREDICATE R54-C1 fail`, `EXIT 1` == entry's "C1 exit1, header absent".
- `.ufo/waves/round-54/integrate/c2-after.txt` → `RUN executed=78 timeout=0
  mismatched=0 evidence_missing=1 laundered=1`, `TIPSTATE` declared green62/red16
  vs observed green61/red17, `MIGRATION redeclared=4`, `PREDICATE R54-C2 fail`
  == entry's "executed78, evidence_missing1, laundered1, green61/red17, redeclared4".
- `.ufo/waves/round-54/integrate/round52-c2-regression.txt` → `ADVERTISED total=79`,
  `REGISTERED total=77`, `MISSING 2` naming `plans/round54_c1_anchor.py` and
  `plans/round54_c2_entrytruth.py`, exit 1 == the registry-closure regression the
  entry reports (and the motivating surface of frozen R55-C1).
- `.ufo/waves/round-54/integrate/census-end.txt` → `ROWS 193`,
  `TIERS {"A": 164, "B": 24, "C": 5}`, `STATUS mined172/queued8/rejected13`
  == entry's census line.

The round-55 entry is not yet landed (this wave is in flight); the latest
*landed* entry is the round judged here.

## Box 3 — instructions executable without oral context → SUPPORTED (executed cold)

Chosen instruction, read from the written bytes only
(`plans/round55_c2_controls.py` argparse + `plans/round-55-claims.md` R55-C2):

    python3 plans/round55_c2_controls.py --selftest

Run with `TMPDIR=/fast/scratch/hyaku/kengaku-r55/R12ShonenEvidence/tmp` (seat
scratch; the instrument otherwise defaults to system temp for its fixtures).
**Exit 0**, output `SELFTEST cases=4 failures=0` — all four cells ok
(`r54-passes-abbreviated-selftest`, `r54-passes-uv-decoy-script`,
`truthful-fixture-passes-r54`, `abbreviation-live (--selft exits 0)`).
Full bytes in `controls-selftest.out`.

Corroborating second cold run of the same file's other documented invocation,
`--case abbreviated-selftest --against r54`: **exit 0**,
`COUNTER EXIT 0` (r54 counter passes the laundering fixture) while
`TRUE REGISTRY ENTRY ["python3", "plans/fixture_gate.py"] exit=1`, closing with
`ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)` — the exact
frozen R55-C2 before-red shape, reproduced non-author. Bytes in `case-abbrev.out`.

## Box 4 — no cross-domain bleed / PROVINCE.md accurate → SUPPORTED (spot 3)

`PROVINCE.md` §Province map → `### Core` table. Three rows spot-re-run today:
1. **In-repo verdict gate** — `test -e grader.py && sha256sum grader.py` →
   `90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f`, exact
   match to the row's pin `90c87c88…ae941f`.
2. **Own probe artifacts** — the row's literal 12-dir `test -d` loop over
   `corpus/evidence/{round8-horizon,round9-replication,round9-fleet,round10-fleet,round11-power,round11-fleet,round12-ladder,round12-fleet,round13-ack-state,round13-coverage,round14-fleet,round18-kimi-routing}`
   → prints nothing; all present.
3. **Public-literature registry** — `test -e corpus/SOURCES.md` → present; live
   `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → **195** rows. The row's
   "171 rows" is explicitly dated (round 51, with its deriving command) and the
   round-54 census-end receipt records 193 — so the surface resolves and the row
   is truthful as a dated snapshot; the 171→193→195 drift is registry growth,
   not bleed.

No cross-domain bleed observed in the spot-checked rows; the Adjacent table's
owner routing (kama/chousa/kotoba/kagi/kumitate/kasegi/kake/protocol) is
unchanged and matches the round-38/39 reported-out blocks in LOG.md/PROVINCE.md.

## Residual notes (not defects)

- Box 1 sampled 2 file cites + 1 command cite (the seat minimum); the other ~40
  cited paths in SKILL.md were not re-walked this seat.
- PROVINCE Core count cells are dated snapshots by design; only 3 rows re-run.
- Box 2 judges the latest *landed* round (54); round 55's entry lands after w1
  settles.
