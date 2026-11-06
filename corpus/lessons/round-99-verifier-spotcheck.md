author: hyaku closure (non-author integrator, @m_zfl)

# Round 99 — non-author verifier spot-check (kengaku)

Closure of lane-round kengaku r99. BASE `2233a66195e3d3d85856248fb8f66c1d8127cede`, lane HEAD after the
round `64be3b7ed3b7189ffb13664647e832a35477425d`, freeze F `24a5a5554130065917d55618ae10309403abf60d`,
measured T `f72a8bc710b12473b5c768004e2581f980d924f4`. Report `.ufo/reports/round-99/kengaku.md` (fleet
repo). Driver digest copied from `.ufo/watchdog.log` (lines 2995, 2998):
`2026-11-06T10:26:52-03:00 launch kengaku round=99 pgid=2919677 driver=hyaku-inline attempt=1`;
`2026-11-06T11:53:53-03:00 complete kengaku round=99; hyaku-inline attempt=1`.
All measurements below were run by this reviewer on 2026-11-06 over committed bytes (`git show REV:path`)
or live upstream URLs. No lane gate was executed (§Gate standard, Closure consequence).

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-99/kengaku.md` | `kengaku-shokunin <kengaku@shokunin.local> 6b7a3b4a… 2026-11-06T11:53:10-03:00` (after lane HEAD 11:52:07, before completion 11:53:53) | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | four `[~]` lines, each with an evidence pointer | pass |
| cited commits exist and are ancestors of `master` | `git cat-file -t H; git merge-base --is-ancestor H master` for f9d29eb3, e219e785, b08a0192, 24a5a555, f72a8bc7, 23d58036, b71b990a, fc65aa9a, 182a40bc, 3fdecf31, c329f955, 64be3b7e (+ BASE) | 12/12 `commit anc=0`; BASE anc=0; `git log BASE..HEAD` = exactly these 12, all `kengaku-shokunin` | pass |
| pushed, no uncommitted round work | `scripts/hyaku/jj-lane.sh state …/kengaku-shokunin`; `git status --porcelain` | `branch=master local=64be3b7e… remote=64be3b7e… ahead=0 behind=0 head=detached tracked=0 untracked=2`; untracked = `.ufo/waves/round-97/w1.ready{,.dispatched}` (orchestrator markers) | pass |
| remote tip | `git ls-remote origin refs/heads/master` | `64be3b7ed3b7189ffb13664647e832a35477425d` | pass |
| prompt carries template contract | `diff <(sed -n 1,140p .ufo/prompts/kengaku-round-99.md) templates/round-prompt.md` | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions; §1–§5 verbatim; hyaku addendum §6 onward | pass |
| wave settled | `ls .ufo/waves/round-99/w1/*.md`; `w1-results.json` | 12 seat reports (ConnectorOverlap, CriticClaims, ExecC1, ExecC2, ExecHarm, ExecKS, MutC1, MutC2, ReviewC1, ReviewC2, ScoutSources, ScribeLesson); results file `seats:12` | pass |

Not a marker: twelve round commits, a probe receipt and two measured claims.

## Claims — re-check

Re-measured = plain counts I ran myself; evidence-verified = committed receipt of a lane instrument read,
not executed.

### Freeze integrity (both claims)

- Re-measured: every sha256 line of `plans/round-99-claims.md` (18 frozen-instrument + 11 candidate-bytes)
  against `git show REV:path | sha256sum`: **T 29/29 match**; tip `64be3b7e` 27/29 — mismatches only
  `SKILL.md` and `corpus/SOURCES.md`, the two disclosed post-T dated corrections (`3fdecf31`, `b71b990a`).
  `git diff --stat F 64be3b7e -- <18 frozen instruments>` is empty.
- Re-measured: `git diff --name-status F T` = the 11 candidate files + `corpus/evidence/round99/bnfit-probe.txt`.
- Re-measured: `sha256sum -c SHA256SUMS` in `corpus/evidence/round99/tb2-bn-fit-modify/` → 8/8 OK.

### R99-C1 — coverage (seventeenth offline TB2 replay, `bn-fit-modify`)

- Re-measured (jq over `plans/grader-population-ledger.json`): `.members|length` 88 at BASE/T/tip; executed
  BASE 42 → T 43 → tip 43; executed set difference T−BASE = `{bn-fit-modify}` (`diff` of key lists: `0a1 > bn-fit-modify`);
  executed ∧ `file-artifact` BASE 33/76 → T 34/76. The T row reads `status executed, reason replayed, round 99,
  receipt corpus/evidence/round99/bnfit-probe.txt`. `SKILL.md:74` at T reads `executed 34 of 76`.
- Re-measured: receipt `bnfit-probe.txt`@T → `grep -c '^CASE '` 13, `ok=True` 13, final `mismatches 0`.
- Re-measured, independent of the lane probe (`uv run -p 3.13 --with scipy==1.16.1 --with pandas==2.3.2`):
  the committed R positive fixture `final_bn_sample.csv` has columns `U,Y,R,D,M`, 10 000 rows, and KS p = 0.2907
  against the grader's hard-coded constants (passes p ≥ 0.001). My own deterministic quantile grids shifted by
  +0.045 sd give p = 0.00303 (pass) and +0.050 sd p = 0.00066 (fail) — the same C11/C12 boundary the lane locates.
  `intervened_dag.csv` = U→R, U→D, U→M, Y→D, R→M (U→Y removed), the grader's line-92 set.
- Mechanism spot-read (live grader, sha256 `364069f8…` = capture): `final_bn_sample["D"]` (l.148) is the only
  value-level read of the sample; other sample asserts are emptiness, columns, 10 000 rows, 5 columns (l.106–139).
  C03/C13 (marginal-only / grid pass) follow from these bytes.
- Evidence-verified: `L1/c1-base.txt` `REV 2233a661…`, `PREDICATE R99-C1 fail`, rc=1; `L1/c1-tip.txt` `REV f72a8bc7…`,
  `LEGS L1..L11=pass`, `TARGET executed_rows=43 … cases=13 legs=130 mismatches=0 new_rows=8 new_rows_flagged=0 defects=0`,
  `PREDICATE R99-C1 pass`, rc=0; `L1/final-verification.txt` same at `c329f955`. Matches the report.
- Verdict: **verified**; axis `coverage` **improved** (score held 7 at the L0 cap; the move is measured by the ledger).

### R99-C2 — freshness (12 digests bound by eight URL-free three-column `PROVENANCE.md`)

- Re-measured independently of the lane counter: each of the eight files is absent at BASE, has header
  `| row | file here | sha256 |` and 0 `https?://` matches. For all 12 rows (S173–S177, S180, S220, S225, S270,
  S285, S293, S306): sha256 of `git show BASE:corpus/evidence/round<N>/<file>` equals the sha column, and that
  token appears in the same BASE SOURCES row → **12/12**; the set equals `L1/c2-pop.txt` (`POP_COUNT 12`).
- Re-measured: SOURCES rows BASE 325 → tip 333 (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`);
  `diff` of BASE vs tip row lines = 8 `>` lines (S334–S341) and **0** `<` lines: no BASE row changed.
- Live freshness re-check (my own, 2 of 12): `https://encoding.spec.whatwg.org/index-windows-1252.txt` HTTP 200,
  sha256 `2c5fa192…0795` = S225 binding; TB2 `README.md` at pin `2fd12b88` HTTP 200, sha256 `7dfa9992…2364` = S180 binding.
- Evidence-verified (gate not executed): `L1/c2-base.txt` `GATE defects base=45 rev=45`, `still=12`, `PREDICATE
  R99-C2 fail` rc=1; `L1/c2-tip.txt` `GATE defects base=45 rev=33`, `LEGS K1..K7=pass`, `TARGET pop=12 cleared=12
  still=0 outside_rows=313 outside_removed=0 outside_added=0 outside_rebound=0 url_channel_files=0 rows_changed=0
  captures_changed=0`, `PREDICATE R99-C2 pass` rc=0; same at `c329f955`. ExecHarm `anchor-{BASE,T}.log`: `comm`
  empty, exactly the 12 cleared.
- Axis-name dispute (CriticClaims F10): the claim binds digests rather than re-fetching, but it converts 12
  digest claims from gate-unverifiable to re-verifiable on every run, and the 2 live re-fetches above plus
  ScoutSources' 12 show the bound bytes are current. Ruled within `freshness` (drift detection), same as r98-C2.
- Verdict: **verified on the frozen predicate**; axis `freshness` **improved** (score held at ceiling 10).

### Post-T dated corrections (status-neutral)

- `b71b990a` (M3): five SOURCES word-count cells for this round's own rows; `anchor_line_check` live 5 → 0
  (evidence `L1/harm/anchor-line-{T,corrected}.txt`). Same shape as the r94 S299 repair, which closure treated
  status-neutral. No C1 counter reads the cell; the C1 kill rule (frozen file change / C bytes) does not fire.
- `3fdecf31` (M5): four `round99-*` registry selftest cells → `none declared`. Evidence-verified:
  `L1/harm/r82c1-tip-{2233a661,f72a8bc7,3fdecf31}.txt` defect lines 25 / 33 / 25; sorted defect set at `3fdecf31`
  = BASE set (`diff` empty).
- Both depart from the frozen claims file's "never repaired in round" clause; disclosed in the report. Conformance
  defect, routed (1).

### Harm

- `git diff BASE HEAD -- SCORECARD.md`: append-only round-99 section; no score cell edited; other axes held
  (novelty 8, depth 10, operability 10, calibration 10, adjacency 9).
- Evidence-verified `L1/harm/summary-fc65aa9a.txt`: 23 checks, every rc unchanged; deltas anchor 45 → 33
  (cleared) and r82c3 30 → 31 (`STATUS-LINE-MISSING bn-fit-modify` per-member delta, r97 27→28, r98 29→30; red at BASE).
- The L1 battery reported r82c1 17 → 17 at `fc65aa9a` while ExecHarm found 25 → 29 at T (4 `ROW-SELFTEST-UNBACKED`);
  the battery under-reported a standing red gate. Repaired at tip (above); routed (2). Not harm at the tip.
- No owned axis harmed.

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | improved | ledger 42→43, set diff `{bn-fit-modify}`, file-artifact 33→34/76, 13/13 cases |
| freshness | improved | 12/12 bindings re-derived; gate 45→33 (receipt); 2 live re-fetches equal |
| novelty | unchanged | no claim; score 8 held |
| depth | unchanged | no claim; score 10 held |
| operability | unchanged | no claim; score 10 held; r82c1 defect set at tip = BASE |
| calibration | unchanged | no claim; score 10 held |
| adjacency | unchanged | no claim; score 9 held |

## Discernment spot-check (round-99 `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S334 `tests/test_outputs.py` | admit (mined, A) | live raw URL at `2fd12b88`, HTTP 200, sha256 `364069f8…` = capture | agree | line 150 `assert p_value >= 0.001, (` verbatim (5 words ≤25); D-only KS at l.146–152 is exactly the mechanism the entry teaches; primary grader code → tier A correct |
| S340 `task.toml` | reject (A) | live raw URL, HTTP 200, sha256 `6493f716…` = capture | agree | line 29 `docker_image = "alexgshaw/bn-fit-modify:20251031"` verbatim; the replay models the grader with a pinned venv and never pulls the image, so the row grounds no replay byte; flip stated |
| S341 `README.md` | reject (B) | live raw URL, HTTP 200, sha256 `647d14a7…` = capture | agree | line 38 contains the 13-word quote verbatim; restates S334/S337 ("validated via Kolmogorov-Smirnov test at 99.9% confidence") and no grader byte reads it |

SOURCES row re-opened: S334 (`corpus/SOURCES.md:350`@tip) carries the l.150 quote with "(5 words)" — 5
whitespace tokens, ≤25 — HTTP 200, 5892 B and the matching sha256. (At T the cell read 4 words; corrected in
`b71b990a`.) Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` →
`kengaku ok …/corpus/SOURCES.md`, rc 0, 31 W04 (30 pre-existing + S334 duplicate-url vs S181, as reported).

## Trend verdicts

- **expansion: improved** — new `corpus/knowledge/tb2-bn-fit-modify-grader.md` opens with
  `source: S334–S339` / `verified-at` / `recheck`, cites mined rows, indexed under `corpus/README.md:1054`
  §Round-99 coverage-map addition (ground not held at BASE; ledger 42→43).
- **quality: improved** — 12 previously gate-unverifiable digest claims re-verify against committed bytes
  (re-derived 12/12; 2 re-fetched live) with no BASE row changed; Q84–Q86 carry lesson grounding (M1, M2, M4/
  considerthese). The S334–S339 word-count error was in rows written this round and was corrected in-round.
- **discernment: improved** — the outside spot-check agrees with the gate on 1 admit and 2 rejects
  (LEARNING.md `improved` rule); the lane self-graded `unprovable-but-better` pending this check.

## Routed defects (lane owes next round)

1. Frozen-clause departure: two post-T dated corrections (`b71b990a`, `3fdecf31`) repaired candidate bytes
   although `plans/round-99-claims.md` says defects after F are never repaired in round. Run
   `anchor_line_check` and `round82-c1` against the candidate tree before F (Q76 recurrence; r94 routed the
   same pre-commit duty), or state the precedent-based exception in the frozen clause itself.
2. L1 harm battery (`L1/harm/run_harm.sh`) reported r82c1 17→17 while the T registry added 4
   `ROW-SELFTEST-UNBACKED` (ExecHarm 25→29): make the battery run each gate in the mode that reads the
   measured revision's registry and diff defect sets, not counts.
3. C2 census is finding-level, not row-level (CriticClaims F6/F7, MutC2 M17; 105/313 outside rows carry no
   gate output): planned successor row-level census.
4. Mutation survivors: MutC1 10/40, MutC2 6/24 (receipt run identity, F..C file set, new-row count).
5. Ledger class note: `bn-fit-modify` classed `file-artifact` only while its decisive test is numeric-band KS.
6. Carried: L0 `kengaku | round-98` coverage-cap ruling (operator), `kengaku | round-54` hold; CriticClaims
   F10 axis-name question to the operator.

Round-98 routed defects 1 (URL side channel: K3 forbids URL column, K7 symmetric), 3 (receipts now open
with `REV <hash>`) confirmed addressed in the r99 receipts read above; 2 partly (new survivors, item 4).

SHONEN note for the operator: all four `[~]` boxes cite pointers a non-author can check (box 2: ledger
flip, capture sha256, the 13-case receipt and an independent KS re-computation on the positive fixture
were re-checked here; the replay itself was evidence-verified, not re-executed); promotion remains
operator-owned.
