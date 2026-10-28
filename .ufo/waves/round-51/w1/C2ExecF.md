# C2ExecF — routed-findings.jsonl rows 46–54 (0-based 45..53) attribution

Seat: C2ExecF (executor). Axes named: **adjacency** (this seat's judged axis — owner + disposition
per row); freshness untouched. Item: attribute rows 46–54 of `corpus/routed-findings.jsonl`,
decide owner + disposition under `plans/round-51-claims.md` §C2 rules, author missing checks,
run every check under frozen-instrument conditions.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7 (wave tip; parent e07f131 is the stage-1 freeze).
Sibling fragment: `.ufo/waves/round-51/w1/C2ExecF.jsonl` (9 rows, all original fields preserved
plus `owner`, `disposition`; no `next` needed — no row is `routed`/`referral`).

## Scratch-execution note (instrument interaction every C2 seat must know)

`plans/round51_routing.py` runs each `fixed-verified` check as `bash -lc <cmd>` with `cwd=<scratch tmp>`
and exports `LANE=<lane>` (`subprocess.run(..., cwd=str(tmp), env={...,"LANE": str(lane)})`).
**Every pre-existing `check` in my slice is cwd-relative and exits nonzero under the frozen
command.** I amended each check to be cwd-independent via `cd "$LANE" &&` or `$LANE/` paths —
the claim re-derived is unchanged, verbatim originals below. All 9 candidate checks were executed
in `/fast/scratch/hyaku/kengaku-r51/C2ExecF/work` with `LANE=/fast/scratch/hyaku/kengaku-r51/C2ExecF/lane`
(a `--shared` clone of 4090c3d) exactly as the counter executes them.

## Mid-run defect observed (flagged to L1, not mine to fix)

While working, the lane working copy `corpus/routed-findings.jsonl` was truncated to 0 bytes
(`git status` shows ` M`, observed 15:20; it held 71 rows when first read minutes earlier).
A sibling mutation is in flight against the lane working copy. My fragment was therefore derived
from the **committed tip** `git show 4090c3d:corpus/routed-findings.jsonl` (71 rows; rows 45–53
byte-identical to my earlier working-copy read). If the wipe is unintended, the L1 must restore
the file before landing.

## Summary table

| # | idx | id | class | owner | disposition | check (as written in fragment) | run rc |
|---|-----|----|-------|-------|-------------|--------------------------------|--------|
| 46 | 45 | R42-R3-27 | guard-selftest-gap | kengaku | accepted-risk | `test "$(cd "$LANE" && python3 plans/scratch_guard.py --selftest 2>/dev/null \| sed -n 's/.*SELFTEST ok=\([0-9]*\)\/.*/\1/p' \| tail -1)" -ge 37` | 1 (live: SELFTEST ok=36/36) |
| 47 | 46 | R42-R3-28 | registry-missing-row | kengaku | fixed-verified | `cd "$LANE" && grep -qE 'scratch[_-]guard' SKILL.md` | 0 |
| 48 | 47 | R42-R3-29 | frozen-cell-wrong-citation | kengaku | fixed-verified | `cd "$LANE" && grep -rqs ':59-61' corpus/lessons/` | 0 |
| 49 | 48 | R42-R3-30 | frozen-cell-wrong-citation | kengaku | fixed-verified | `cd "$LANE" && grep -rqsE 'X7[^|]*:91-92' corpus/lessons/` | 0 |
| 50 | 49 | R42-R3-31 | scorecard-overstatement | kengaku | fixed-verified | `cd "$LANE" && grep -qF 'S1 — the envelope note is one counter too wide' SCORECARD.md` | 0 |
| 51 | 50 | R42-R3-32 | envelope-drift-record | kengaku | accepted-risk | `cd "$LANE" && grep -qF 'measure-final.txt:938' corpus/lessons/round-42.md` | 1 (live) |
| 52 | 51 | R42-R3-33 | plan-mutant-numerator | kengaku | fixed-verified | `grep -qF '9 witnessed of 20' "$LANE/plans/round-43-claims.md"` | 0 |
| 53 | 52 | R42-R3-34 | plan-missing-restore-control | kengaku | fixed-verified | `grep -qF 'NA7' "$LANE/.ufo/waves/round-43/claims/control-c1-direction-mislabel.txt"` | 0 |
| 54 | 53 | R42-R3-35 | plan-missing-refusals | kengaku | accepted-risk | `cd "$LANE" && ls .ufo/waves/round-43/claims/ \| grep -qiE 'xo\|substitute'` | 1 (live: no XO/substitute control) |

## Per-row evidence

**All owners are `kengaku`** — every row's subject is a kengaku-owned artifact
(`plans/scratch_guard.py`, `SKILL.md`, frozen round-42 C1 cells, `SCORECARD.md`,
round-42/43 claims and lesson records under `plans/`+`corpus/`+`.ufo/waves/round-4x/`).
No row's ask belongs to a sibling lane, so `routed`/`referral` (which require a non-kengaku
owner + `next`) honestly apply to none. `kengaku` ∈ `FALLBACK_OWNERS` in the frozen instrument
(the conf's lane list is pipe-format, unparsed by `load_owners`, but the fallback set covers it).

- **R42-R3-27** — finding: no unreadable-sentinel selftest case. `python3 plans/scratch_guard.py
  --selftest` still prints `SELFTEST ok=36/36`; SKILL.md:608 still records "no unreadable-sentinel
  `check` case yet". Gap live → `accepted-risk` (carried, documented; check is the
  green-when-fixed condition, currently exit 1).
- **R42-R3-28** — SKILL.md:608 now carries a `scratch-root-guard` registry row → fixed.
- **R42-R3-29 / R42-R3-30** — `corpus/lessons/round-42.md:194` names both errata: "X3 `:57-58`
  for a sentence at `:59-61`, X7 `:92-93` for a sentence at `:91-92`" → fixed.
- **R42-R3-31** — `SCORECARD.md:1829` carries the appended correction "S1 — the envelope note
  is one counter too wide" → fixed. (`close` first token `round-43` does not resolve as a ref/path,
  so `fixed-historical` was not usable; `fixed-verified` is.)
- **R42-R3-32** — lesson `corpus/lessons/round-42.md` still lacks `measure-final.txt:938` (grep
  exit 1); drift is only at `corpus/lessons/round-42-verifier-spotcheck.md:46`. Record uncorrected
  → `accepted-risk`.
- **R42-R3-33** — `plans/round-43-claims.md:79` discloses "(F42CritPlanNext D1: 9 witnessed of 20)",
  correcting the "20 rc-witnessed survivors" numerator → `fixed-verified` (authored check, exit 0).
  Residual limit: the 9 unwitnessed survivors still have no witness fixture; `status` stays `open`
  (preserved) — L1 may flip status/close at landing.
- **R42-R3-34** — `.ufo/waves/round-43/claims/control-c1-direction-mislabel.txt` exists and is the
  carried-cell restore control (NA7 `rc-silence` relabel → `SURVIVED exhibits=0>1,rc-mirror`) →
  `fixed-verified` (authored check, exit 0). Residual limit: one restore control, not per-mutant;
  `status` stays `open`.
- **R42-R3-35** — legs h/i and controls h1–h6 all landed (files present), but **no red control
  exists for the XO3/X13 substitute shapes** and the token scan stays a heuristic (disclosed as a
  limit at `plans/round-43-claims.md:77`) → `accepted-risk`; authored check greps claim dir for an
  xo/substitute control — exit 1, live risk.

## Exact commands run (verbatim)

- `git clone --shared --quiet /home/vgpnk/Projects/shokunin/kengaku-shokunin lane` (scratch)
- `git -C lane rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r51/C2ExecF/lane`; `rev-parse HEAD` → `4090c3d…`
- `git -C lane show 4090c3d…:corpus/routed-findings.jsonl` (71 rows)
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -e 77ea425a^{commit}` → resolves
- Per-check: `bash -lc <cmd>` in `cwd=/fast/scratch/hyaku/kengaku-r51/C2ExecF/work`,
  `env TMPDIR=<work> LANE=<scratch clone>` — results in the table (rc column).
- Greps at lane tip (all at REV 4090c3d): `scratch[_-]guard` SKILL.md → :608 hit;
  `:59-61` + `X7…:91-92` corpus/lessons/ → round-42.md:194; `S1 —` SCORECARD.md → :1829;
  `measure-final.txt:938` round-42.md → no hit (rc 1); `9 witnessed of 20` round-43-claims.md → :79;
  `NA7` control-c1-direction-mislabel.txt → hits; `token scan is a heuristic` round-43-claims.md → :77.

## Limits

- Dispositions for R3-33/R3-34 assert the routed ask is answered at the tip; the original
  `status: open` is preserved — landing may want `status: closed` + `close` filled (my scope forbids
  it: original fields preserved).
- `accepted-risk` checks encode the green-when-fixed condition by ledger convention; they exit 1
  today, which is the live-risk evidence, not a counter failure (the counter only runs
  `fixed-verified` checks).
- Owner evidence is subject-matter (all kengaku artifacts); no sibling-lane claim exists on any row.

VERDICT: 9/9 rows attributed (owner=kengaku), dispositions set (6 fixed-verified — R3-28/29/30/31/33/34 — all exit 0 under frozen conditions; 3 accepted-risk — R3-27/32/35 — live risks measured at exit 1), 3 authored checks, all 9 checks executed and recorded; fragment written; one routed-to-L1 defect (ledger working copy truncated mid-wave).
