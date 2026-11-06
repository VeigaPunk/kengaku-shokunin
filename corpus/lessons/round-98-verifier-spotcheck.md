author: hyaku closure (non-author integrator, @m_zfl)

# Round 98 — non-author verifier spot-check (kengaku)

Closure of lane-round kengaku r98. BASE `49a1c4f1097db7c923da56d4213cad75772ed1c0`, lane HEAD after the
round `4a5dc030ba7dcf2398f2a5c424757b812cca2225`, measured T `8e37fc65d5649bb37166fdd6b1657445a8cb55b9`.
Report `.ufo/reports/round-98/kengaku.md` (fleet repo). Driver digest copied from `.ufo/watchdog.log`
(lines 2988, 2994): `2026-11-06T08:00:57-03:00 launch kengaku round=98 pgid=1082935 driver=hyaku-inline attempt=1`;
`2026-11-06T10:23:13-03:00 complete kengaku round=98; hyaku-inline attempt=1`.
All measurements below were run by this reviewer on 2026-11-06 over committed bytes (`git show REV:path`).

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %ae %H %ci' -- .ufo/reports/round-98/kengaku.md` | `kengaku-shokunin kengaku@shokunin.local 2e2ba43b… 2026-11-06 10:22:33 -0300` (after lane HEAD commit 10:21:29, before completion 10:23:13) | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | four `[~]` lines, each with an evidence pointer | pass |
| cited commits exist and are ancestors of `master` | `git cat-file -e H^{commit} && git merge-base --is-ancestor H master` for 5584a6f7, 350d0e59, c71f04e6, e1a3afd9, 8e37fc65, 363fa03c, 4654ffc1, f90cf415, 4a5dc030, 49a1c4f1, febd88b9 | 11/11 `ok` | pass |
| pushed, no uncommitted round work | `scripts/hyaku/jj-lane.sh state …/kengaku-shokunin`; `git status --porcelain` | `ahead=0 behind=0 … tracked=0 untracked=2`; untracked = `.ufo/waves/round-97/w1.ready{,.dispatched}` (orchestrator markers, not lane work) | pass |
| remote tip | `git ls-remote origin refs/heads/master` | `4a5dc030ba7dcf2398f2a5c424757b812cca2225` | pass |
| prompt carries template contract | `diff <(sed -n 1,140p .ufo/prompts/kengaku-round-98.md) templates/round-prompt.md` | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions; §1–§5 verbatim; hyaku addendum §6 onward | pass |
| wave settled | `ls .ufo/waves/round-98/w1/*.md` | 11 seat reports (ConnectorOverlap, CriticClaims, ExecC1, ExecC2, ExecHarm, MutC1, MutC2, ReviewC1, ReviewC2, ScoutSources, ScribeLesson) | pass |

Not a marker: nine round commits, a probe receipt and two measured claims.

## Claims — re-check

Re-measured = plain counts I ran myself; evidence-verified = committed receipt of a lane instrument read
(not executed, per §Gate standard Closure consequence).

### R98-C1 — coverage (sixteenth offline TB2 replay, `regex-chess`)

- Re-measured (jq over `plans/grader-population-ledger.json` at each rev): BASE `members 88 executed 41
  regex-chess unexecuted file-artifact 32 serialization-schema 7`; C/T `executed 42 regex-chess executed
  file-artifact 33 serialization-schema 8`. Executed set difference T−BASE = `{'regex-chess'}`, BASE−T = `∅`.
  Matches the report and the SKILL class cells (`executed 33 of 76`, `executed 8 of 10`).
- Re-measured: SOURCES rows (`^ {0,3}\|\s*S[0-9]{3,}\s*\|`) BASE 317 → C 325 → T 325; `git diff BASE T --
  corpus/SOURCES.md` = 0 removed, 8 added lines (insert-only).
- Re-measured freeze: all 13 frozen-instrument sha256 from `plans/round-98-claims.md`@F equal the bytes at T
  (0 mismatches); all 4 candidate-bytes sha256 equal the bytes at C, unchanged at T; `git diff --name-only F C`
  = the 4 candidates + `corpus/evidence/round98/regexchess-probe.txt`.
- Re-measured capture integrity: `sha256sum -c SHA256SUMS` in `corpus/evidence/round98/tb2-regex-chess/` →
  8/8 OK; live re-fetch of `test_outputs.py` and `check.py` at pin `2fd12b88` gives the pinned sha256
  (`4983c44d…`, `f9c416ae…`).
- Evidence-verified: probe receipt `corpus/evidence/round98/regexchess-probe.txt` — 12 `CASE … ok=True`,
  `mismatches 0`; `L1/c1-base.txt` `PREDICATE R98-C1 fail` rc=1; `L1/c1-tip.txt` `LEGS L1..L10=pass`,
  `TARGET executed_rows=42 … legs=60 mismatches=0 new_rows=8 new_rows_flagged=0 defects=0`, `PREDICATE R98-C1 pass` rc=0.
- Mechanism spot-read (live grader): `run_solution` returns a list; line 35 checks per-line membership with the
  `rpartition(" ")[0]+" -"` fallback; line 39 compares only `len`. C04 (duplicate for omission) and C07
  (invented en-passant square) follow from these bytes.
- Verdict: **verified**; axis `coverage` **improved** (score held 7 at the L0 cap; the move is measured by the ledger).

### R98-C2 — freshness (39 nested-capture digests bound through `corpus/evidence/PROVENANCE.md`)

- Re-measured independently of the lane counter: for each of the 39 rows of `PROVENANCE.md`@T, sha256 of
  `git show T:corpus/evidence/<file>` equals the row's sha column, that digest appears in the same SOURCES
  row's text, the path is nested (`round<N>/graders/<task>/<sub>/…`), and the capture blob is identical at
  BASE and T → **39/39**; rounds covered {52, 92–97}. Old SOURCES rows changed BASE→T: **0**.
- Evidence-verified (gate not executed): `L1/c2-base.txt` `GATE defects base=86 rev=86`, `still=39`,
  `PREDICATE R98-C2 fail` rc=1; `L1/c2-tip.txt` `GATE defects base=86 rev=45`, `TARGET pop=39 cleared=39 still=0
  unbound=0 rows_changed=0 captures_changed=0 new_old_row_defects=0`, `PREDICATE R98-C2 pass` rc=0.
- Disclosed side effect (lesson M4, `L1/outside-pop-census.txt`): the URL column also re-binds S213, S230,
  S237, S272. Re-measured: the bound files' sha256 appear in S213, S230, S272; S237 carries no 64-hex token
  and its rebind target is byte-identical to its old binding (`round66/sources/kv-store-grpc-test_outputs.py`
  and `round52/graders/kv-store-grpc/tests/test_outputs.py` both `115de2e9…`). The two extra clears are true
  clears, not masked defects. Undeclared at freeze → routed (defect 1), not harm.
- Verdict: **verified on the frozen predicate**; axis `freshness` **improved** (score held at ceiling 10).

### Harm

- `git diff BASE T -- SCORECARD.md`: append-only round-98 section; other axes held (novelty 8, depth 10,
  operability 10, calibration 10, adjacency 9).
- Evidence-verified `L1/harm/summary-4654ffc1.txt`: 23 checks, every rc unchanged; finding deltas only
  anchor 86→45 (cleared) and r82c3 29→30 (`STATUS-LINE-MISSING regex-chess`, the per-member frozen-declaration
  delta, same shape as r97 27→28, gate already red at BASE).
- No owned axis harmed.

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | improved | ledger 41→42, set diff `{regex-chess}`, 12/12 cases |
| freshness | improved | 39/39 bindings re-derived; gate findings 86→45 (receipt) |
| novelty | unchanged | no claim; score 8 held |
| depth | unchanged | no claim; score 10 held |
| operability | unchanged | no claim; score 10 held |
| calibration | unchanged | no claim; score 10 held |
| adjacency | unchanged | no claim; score 9 held |

## Discernment spot-check (round-98 `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S326 `tests/test_outputs.py` | admit (mined, A) | live raw URL at `2fd12b88`, HTTP 200, sha256 `4983c44d…` = capture | agree | quote at line 35 verbatim (11 words ≤25); per-line membership + `len` equality (l.35–41) is exactly the mechanism the entry teaches; primary code → tier A correct |
| S333 `README.md` | reject (B) | live raw URL, HTTP 200, sha256 `9296cbee…` = capture | agree | line 33 quote verbatim (18 words); grader imports only `chess, chess.pgn, io, json, re` — README is never read; its "no more, no fewer" is contradicted by the count-only check |
| S331 `environment/check.py` | reject (A) | live raw URL, HTTP 200, sha256 `f9c416ae…` | agree | line 98 `def test_morphy_opera_game(self):` verbatim; not imported by the grader, whose games are immortal/century/naroditsky |

SOURCES row re-opened: S326 row text carries the same line-35 quote (11 words), HTTP 200, 5356 B and the
matching sha256. Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` →
`kengaku ok …/corpus/SOURCES.md`, rc 0 (only pre-existing W04 warnings).

## Trend verdicts

- **expansion: improved** — new `corpus/knowledge/tb2-regex-chess-grader.md` opens with source/verified-at/recheck,
  cites mined S326–S330, indexed under `corpus/README.md` §Round-98 coverage-map addition (ground not held at BASE).
- **quality: improved** — 39 previously unverifiable digest claims re-verify against committed bytes with no admitted
  entry failing re-check (re-derived 39/39); Q82/Q83 added with lesson grounding.
- **discernment: improved** — the outside spot-check agrees with the gate on 1 admit and 2 rejects (LEARNING.md
  `improved` rule); the lane self-graded `unchanged` pending this check.

## Routed defects (lane owes next round)

1. Provenance side channel (M4): the frozen C2 predicate could not see the 4 outside-population re-bindings
   (K7 sees only additions). Land the planned three-column provenance table or a symmetric census.
2. MutC2 survivors (21/29 killed) and MutC1 receipt-field survivors: add killing legs in a successor counter;
   do not edit round-98 instruments (Q79).
3. Measurement receipts `L1/c1-*.txt`, `L1/c2-*.txt` name their revision only in the commit message
   (`363fa03c`) and SCORECARD, not in the file (§Gate standard: a verdict names the revision measured). Stamp REV
   in successor receipts.
4. Carried: L0 `kengaku | round-98` coverage-cap ruling (operator), `kengaku | round-54` hold.

SHONEN note for the operator: all four `[~]` boxes cite pointers a non-author can check (box 2: ledger flip,
capture sha256 and the 12-case receipt were re-checked here from committed bytes; the replay itself was
evidence-verified, not re-executed); promotion remains operator-owned.
