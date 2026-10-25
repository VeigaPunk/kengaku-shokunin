# ConnTameshi — sibling-overlap scan (round 25; C1/C2)

Target `/home/vgpnk/Projects/shokunin/tameshi-shokunin` @ `4b7c6823` (round-18, 2026-10-20; worktree clean).
Read-only; no sibling write, no install. **Premise correction:** this lane is verification-fixture craft,
not LLM test generation — `PROVINCE.md:3-6`.

**F0 — label collision, no referent.** tameshi `calibration` = promotion-claim restraint (`SCORECARD.md:67`
"Two points per correctly restrained … promotion assertion"; `:650` "calibration 8 is a no-harm monitor,
not an additional claim or promotion"). Judge/Brier/ECE/log-loss surface: word-boundary sweep → 1 hit, only
`corpus/lessons/round-16-verifier-spotcheck.md:128` "The rubric score stays 6" (its own rubric). Ruling:
**none** — do not cite tameshi calibration as C2 prior art.

**F1 — interval/CI gates: NONE (adjacent-report-out).** Whole lane incl. archives, `.git`/`.jj` excluded,
4,153 files: `grep -rliE 'clopper|wilson|pearson|confidence interval|credible interval|binom\.test|binomtest'`
→ `0`. Nearest constructs are deterministic, not statistical: `tools/mutate-and-run.sh:180-181`
`BAND_KILLED=1`/`BAND_FLIPS=1` (replay tolerance, `:1301-1302`); `SKILL.md:335` "Bands are a report convention,
not a pass/fail gate"; `corpus/knowledge/fleet-kill-rate-ledger.md:45-47` stores point rates `8/10 (80 %)`,
composition-bound (`:26-27`), no min-n — the point-verdict defect class C1 re-verdicts, not a duplicate
instrument.

**F2 — state checker: ADJACENT, strongest overlap (cite; state delta).**
`.ufo/evidence/round-18/measure.py:6-7` reads "blobs via `git cat-file`/`git show` at an explicit commit only
(no worktree access)"; `:26-31` re-derives `calibration_restraint_score` + SHONEN census + SOURCES census;
`:94-96` exit map `0 measured · 2 missing/unreadable · 64 usage` — **no mismatch state**. C2 must claim
population+contract delta, not concept: measure.py resolves no backticked `:line` anchors, runs no capability
row command (P2a), has no PROVINCE `ABSENT` rule (P2d), no README bidirectional index (P2e), no exit 1.
Supporting precedents: `tools/registry-check.py:52` "0 all held · 1 any differs · 2 could-not-evaluate" with
`--json`/hermetic `--selftest` (`:74-78`); `tools/evidence-disposition.py:4-6,106-113` "every frozen …
expected check exactly once" without executing receipts; `tools/context-capture.py:4-6` re-derives a verdict
from a byte-pinned receipt's raw fields. All adjacent; cite, do not import.

**F3 — repeat-control is a calibration gate, not an interval (adjacent).** `tools/repeat-control.py:32-44,93-94`:
`controls_match` iff N≥3 byte-identical runs; `:93-94` "it is not a determinism proof and it cures no flakiness".
No interval; do not cite as C1 prior art. **F4 — weak-form census (none):** `SCORECARD.md:75` command C is
`git show REV:SHONEN.md` + a mark regex, "mark census only; this upper bound awards no evidence/authority
credit" — the presence form C2 supersedes, not an overlap. `tameshi-shokukin/` (typo dir) has 0 files.

## Proposed move (one)
Add one **neighbour-bound** sentence to C1's novelty evidence cell + knowledge entry (F1 command, `0` result,
the seven searched terms named) and one **contrast** sentence to C2's note (F2: `measure.py` exit 0/2/64,
no mismatch state). Axes: novelty — narrows the claim to "exact-interval estimator absent in the nearest
lane; point-verdict class fleet-wide"; calibration — C2 stops implying conceptual novelty where rev-pinned
score re-derivation already exists. No claim withdrawn, no population or bar changed; C2 keeps its
"calibration +1 is not claimed" sentence.

## Risks
- `0` is lexical, not semantic: `±`/error-bar prose evades the grep; scope the sentence to the seven terms.
- "Nearest lane has 0" ≠ "fleet-first": ConnSoujiKaidoku F10 found a hand-computed CP interval in kaidoku
  r14. Say neighbour lane, never fleet-first.
- Naming tameshi's point rates invites a patch request; mark read-only/report-only, no absorption.

## Verification
- `grep -rliE 'clopper|wilson|pearson|confidence interval|credible interval|binom\.test|binomtest' tameshi-shokunin --exclude-dir=.git --exclude-dir=.jj | wc -l` → `0`.
- `sed -n '94,96p' tameshi-shokunin/.ufo/evidence/round-18/measure.py` → exit map without `1`.
- `sed -n '180,181p' tameshi-shokunin/tools/mutate-and-run.sh` → `BAND_KILLED=1`, `BAND_FLIPS=1`.
- After landing: `grep -niE 'fleet.first|first in the fleet'` over changed kengaku files → empty.

VERDICT: tameshi owns no interval/CI gate and no judge calibration; the only material overlap is a rev-pinned
score re-derivation (F2) that makes C2 adjacent, not novel, while C1's estimator is absent in the nearest lane
(0/4,153 files) — cite the neighbour bound and the exit-map delta, route the rest. Installs: none.
