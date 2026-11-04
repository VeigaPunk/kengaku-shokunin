# Round 77 — verifier spot-check (kengaku)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-04 (UTC)
lane: `kengaku-shokunin`
base `07c97fcd2fcca74f72df1d3c6b9dfe662fd75b59` (round-76 verifier spot-check)
lane tip `5eb74eed3aa3f0b70986867f560f34c1da4f3427`
report `.ufo/reports/round-77/kengaku.md` @ `32d24117c5c15f3e838b6eae6d3589ba878adeb6`
dispatch/complete digest (mutable `.ufo/watchdog.log`, copied):
`2026-11-04T02:23:41-03:00 launch kengaku round=77 pgid=3391919 driver=hyaku-inline attempt=1`;
`2026-11-04T02:46:03-03:00 complete kengaku round=77; hyaku-inline attempt=1`.

This file is integrator work, not lane work: I did not author the round and changed no lane-authored
file. Every number below was re-derived by me over committed bytes, from a clean clone of the lane at
`5eb74eed` under `/fast/scratch/hyaku/kengaku-r77/closure/` (deleted after the pass).

## 1. Step-1 conformance

| item | result |
|---|---|
| report identity | `git log --format='%an %H' -- .ufo/reports/round-77/kengaku.md` → `kengaku-shokunin 32d24117…` (author and committer `kengaku-shokunin <kengaku@shokunin.local>`); committer time 02:45:42 -03, i.e. 8 s after the lane tip commit 02:45:34 -03; ancestor of fleet `origin/master` |
| SHONEN heading | `grep -c '^## SHONEN'` → 1; four `[~]` lines with pointers against the four `SHONEN.md` boxes; no `[x]` |
| cited commits | all 13 cited (`9ebb8ed1 8da90eb7 6f0c7ad9 d181e16b 08309a5a 4f2ff9be 51ffc14f d488f0cb a5c81b76 7023db7e a3299c33 113c7ef0 5eb74eed`) exist and `git merge-base --is-ancestor <hash> master` holds; base `07c97fcd` is an ancestor |
| lane state | `jj-lane.sh state` → `branch=master local=5eb74eed remote=5eb74eed ahead=0 behind=0`; `git status --porcelain` empty |
| report sections | Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN, Stale-lane, Tool installs — in the contract's order |
| prompt fidelity | `.ufo/prompts/kengaku-round-77.md` lines 1–140 diff against a re-render of `templates/round-prompt.md` (substitutions `{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`, `<kengaku-repo>`): **0 diff lines**; run-15 addendum `## 6` follows; the five child-lane items (report path and filename, commit-before-report ordering, `SHONEN` heading, commit-hash citation rule, lane write scope) and the L2 floor are present; no route map contradicts `MISSION.md` (the quoted run-15 alias map is the host route table, which `MISSION.md` delegates to it) |
| wave | one v1 wave, 12 seats, band 8–16; `w1-spec.json` 12 items, no `model` key; `w1-dispatch.json` `counts.spawn=12`; validator `w1-validate.rc` = 0; `w1-results.json` 12 results, every `output` non-empty, 0 dead; roles executor 3 / scribe 2 / scout 1 / connector 1 / reviewer 2 / critic 1 / mutation-tester 1 / sentinel 1; attack seats (reviewer, critic, mutation-tester) 4/12 = 33 %; connector 1 |

No conformance defect bars admission. Defects are named in §6.

## 2. Claims — re-derived, not evidence-read

Both counters were re-run by me in a clean clone at the tip (worktree mode) and against the base
revision (`--rev 07c97fcd…`); the lane's committed receipts were additionally read and compared.

### R77-C1 / coverage — `python3 plans/round77_c1_declared_surfaces.py --lane .`

Observed at the tip (rc 0):

```
CANONICAL source=## Declared surfaces rows=28
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
IDENTITIES n=28 unique=28 sha256=1d5f5dc1aa6d5577…
DEFECTS n=0
PREDICATE R77-C1 pass
```

Observed with `--rev 07c97fcd…` (rc 1): `CANONICAL source=none rows=0`, `SURFACES total=0 present=0
absent=0 remote=0`, `UNLISTED n=33`, `RESOLVED live=0`, `AGREE agree=0 disagree=0`, `DEFECTS n=34`
(`CANONICAL-MISSING` + 33 `UNLISTED-SURFACE`), `PREDICATE R77-C1 fail`.

Plain corroboration: the canonical section carries 28 rows (PROVINCE.md lines 1023–1050); the three
superseded tables declare 11 + 10 + 12 = 33 rows, matching the before state's `UNLISTED n=33`.
Reported values match observation; the after receipt (`c1-after.txt`, `LANE_TIP 4f2ff9be`, `WORKTREE
clean`) is consistent with the tip by construction (the tool at `4f2ff9be` is `a4777acf…`, unchanged
through the tip).

### R77-C2 / calibration — `python3 plans/round77_c2_defect_discharge.py --lane .`

Observed at the tip (rc 0):

```
SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
DEFECTS n=0
TARGET ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
PREDICATE R77-C2 pass
```

Observed with `--rev 07c97fcd…` (rc 1): `SCOPE ids=7 registered=0 closed=0 open=0 discharged=0
legs_passed=0 legs_pending=2 wrong=12`, `DEFECTS n=12` (7 `MISSING-ROW` + 5 `LEG-FAIL`),
`PREDICATE R77-C2 fail`.

Plain corroboration: `corpus/routed-findings.jsonl` 86 → 93 rows; parsed both revisions — the 7 new
keys are exactly `R76-V1`…`R76-V7`, **0 existing rows changed and 0 removed** (the 30 deleted JSONL
lines are key-order re-serialisation only); all seven carry `status=closed`, `close_commit=8da90eb7…`
(an ancestor of `master`) and a `check` naming their own id. Batteries, read from committed bytes:
C1 `cases=6 red=5`, `6/6` mutants, control `live=0 target_reached=False`; C2 `cases=10 red=9`, git
arms `3/3`, `6/6` mutants, control `defects=7 target_reached=False`.

### Other numbers in the report

- Sources registry `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 244 at
  `07c97fcd`, 245 at the tip; `corpus/SOURCES.md` diff is 1 insertion / 0 deletions (no row touched).
- `sources-census.sh validate --root … kengaku` → rc 0, 25 `W04` warnings at the tip; committed
  `census-before.txt` rc 0 at 244 rows.
- `routed_open.py --lane .` at the tip → `ROWS total=93 open=31 blocked=1 closed=59 refused=2`
  (arithmetic closes: 31 + 1 + 59 + 2 = 93).
- R75 universes at the tip, plain count: knowledge 74/74, lessons 127/127, evidence dirs 68/68 —
  the rerun receipt's tallies hold at the tip.
- Round-76 re-mint (R76-V1): `c1-selftest.txt`/`c1-mutants.txt` stamp `LANE_TIP 9ebb8ed1` with
  `TOOL_SHA 552cc63b…`; `git show 9ebb8ed1:plans/round76_c1_surface_resolver.py | sha256sum` →
  `552cc63b…` — the stamp recomputes.

## 3. Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | **improved** (score held 7 by the open L0 cap `kengaku \| round-25`) | declaration universe 0 → 28 machine-checked rows, `UNLISTED n=33 → 0`, `DEFECTS n=34 → 0`; both states re-run by me |
| calibration | **improved** (score held 10, exercised) | 7 routed ids registered + closed in the ledger with re-deriving legs, 0 → 7; ledger semantically append-only (0 rows changed, 0 removed) |
| depth | unchanged | no new knowledge entry claimed; S253 + Q56 already accounted in the round's own scores |
| operability | unchanged | two new gates registered with selftest/mutant/control batteries (`SKILL.md` rows present); no score move claimed |
| freshness | unchanged | every canonical surface re-resolved live this round; no score move claimed |
| adjacency | unchanged | `PROVINCE.md` §Round 77 refuses the serving plane / benchmark runtime / route resolution to kama, the benchmark images and kumitate; connector matrix records 14 lanes' report-outs |
| novelty | unchanged | two instruments, no new construct claimed |

No axis harmed: `git diff 07c97fcd 5eb74eed -- SCORECARD.md` is append-only (51 insertions, 0
deletions); the lane diff has **no deleted path** (`--name-status` has no `D`/`R`); the 41 deleted
lines sit in the six named files (PROVINCE one-name correction, two SKILL rows re-pinned, the
round-76 receipts re-minted, the round's own ledger rows, the SF14 pin).

## 4. Discernment spot-check (LEARNING.md)

`corpus/lessons/round-77.md` `## Gate`, sampled admit and both rejects; each source re-opened.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S253 — Git `git-cat-file` docs | admit (tier A, `docs`) | `https://git-scm.com/docs/git-cat-file` fetched live 2026-11-04: HTTP 200, 79 488 bytes, sha256 `91805d9aec858f88581552fc1fe105a40a649544f872e72e6daff210a113e910` — identical to the committed capture; sentence at capture line 2584 reads "If `<type>` is specified, the raw (though uncompressed) contents of the `<object>` will be returned." (15 words) | agree | the quote is located at the named line, is 15 words (≤25), and grounds exactly the at-revision object read both counters use; the row's `anchor` names the section and the capture stamp |
| "a receipt that names a revision was produced by the tool committed there" | reject | same page, re-opened | agree | the page defines `<rev>:<path>` / object content; it says nothing that binds a *run* to a tool, so the inference is ungrounded. The round's own R76-V7 rerun receipts are a live instance of the class (defect D1) — the reject is well grounded, the gate's V7 leg does not yet catch it |
| "a declaration is evidence of resolution" | reject | `corpus/evidence/round77/c1-control-declared.txt`, re-read | agree | `CONTROL rows=7 declared_verdicts=7 agree=7 live=0 target_reached=False` — a declaration-trusting counter reaches `agree=7` but never the C1 target's `live=27`, so the declaration is not evidence |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → rc 0, 245 rows, 25 `W04`.

Newly written row check: `S253` is the only new row; eleven columns, `status=mined`, `used-by`
`corpus/lessons/round-77.md, plans/round-77-claims.md` (both exist), ≤25-word quote, located.

## 5. Trend verdicts

- **expansion: improved.** Three capability rows enter `SCORECARD.md` (`canonical-declared-surface-inventory`,
  `receipt-tool-binding-discharge`, `receipt-remint-with-tool-sha`), each with a command whose run I
  reproduced above; one source row enters the registry at tier A (244 → 245). The report correctly
  says no `knowledge/` entry was admitted and no frontier row moved.
- **quality: improved.** `R75-C1`, `R51-C1`, `R74-C1`/`R74-C2` are green at the tip where they were
  red earlier in the round (README index rows, `SF14` pin 244 → 245, remint-driver row); two new
  gates ship with selftest/git-arm/mutant/control batteries; the round-76 battery receipts now carry
  a `TOOL_SHA` that recomputes at their stamp. Routed defect D1/D2: some round-77 receipts carry a
  pre-fix `LANE_TIP` with post-fix bytes (`WORKTREE dirty` disclosed) — the class the round repairs.
- **discernment: improved.** This outside spot-check agrees with the gate on the admit and both
  rejects; the wave's attacks changed committed bytes (A3 duplicate identities / remote-anchor
  mismatch / id-bound checks, A4 redirect refusal + loopback-only TCP, A5 five false greens), and
  survivors are recorded as stated limits rather than smoothed away.

## 6. Routed defects for the next round (none of them bars admission)

1. **D1 (high) — R76-V7 receipts are mis-stamped.** `corpus/evidence/round77/rerun-r51-c1.txt`
   (and `rerun-r75-c1.txt`) stamp `LANE_TIP 9ebb8ed1` with `WORKTREE dirty`. At `9ebb8ed1`,
   `plans/round51-surfaces.json` `SF14.count_claim` is **244** while `corpus/SOURCES.md` already holds
   **245** rows — so the gate is red at the stamped tip (`NUMBER-DRIFT`), yet the receipt prints
   `NUMBER-DRIFT 0` / `PREDICATE R51-C1 pass`. The pass comes from the post-`8da90eb7` working tree,
   not the named revision: this is the R76-V1 class re-shipped by the round that closes it. Fix:
   re-mint the three rerun receipts at the commit that carries their fixes (or at a tip where the
   verdicts reproduce), and tighten V7 to require `WORKTREE clean` or to re-derive the predicate from
   the tip's bytes.
2. **D2 (medium) — round-77 battery receipts stamp pre-fix tips.** `c1-selftest.txt`,
   `c1-mutants.txt`, `c1-control-declared.txt` stamp `LANE_TIP 51ffc14f` with `TOOL_SHA a4777acf…`,
   but the tool at `51ffc14f` hashes to `5a507c08…` (A5 landed at `4f2ff9be`); `c2-selftest.txt`,
   `c2-mutants.txt`, `c2-selftest-git.txt`, `c2-control-status.txt` stamp `6f0c7ad9` with
   `97166dac…` against `52419b0b…` at that commit. `WORKTREE dirty` discloses it, but the digest does
   not recompute at the named tip.
3. **D3 (low) — stale stamp in SCORECARD.** The round-77 rows say the after receipts are "stamped
   `d181e16b`"; the committed receipts and the report say `4f2ff9be`. Re-pin the SCORECARD text.
4. **D4 (low) — "at the final tip" claims lack at-tip receipts.** The report's "Other gates at the
   final tip" list rests on receipts measured at `9ebb8ed1`; `routed_open`'s `total=93` has no
   committed receipt at the tip (I re-derived it: 93/31/1/59/2, true). Land one at-tip rerun block or
   say which revision each number was measured at.
5. **D5 (low) — `WORKTREE clean` on the before receipts is narrower than it reads.** `c1-before.txt`
   stamps `WORKTREE clean` although the C1 counter cannot exist at `07c97fcd` (it was supplied
   untracked); the cleanliness check ignores untracked files. State the tool-supply step in the
   receipt, or make the check include untracked paths.

## 7. Provisional non-author rulings (for the MANIFEST row)

- claims: R77-C1 **verified (re-measured)**, R77-C2 **verified (re-measured; D1 routed against the
  V7 discharge's evidence, predicate itself holds)**.
- axis verdicts: coverage improved, calibration improved, depth/operability/freshness/adjacency/novelty unchanged.
- trends: expansion improved, quality improved, discernment improved.
- admission: **admitted** — every claim verifies and no axis is harmed; the D1–D5 defects are
  conformance/evidence defects routed to the lane, not admitted work.

Non-author attrs: this file was written by a fresh closure session that did not author any round-77
byte. Lane gates were not executed (PROTOCOL §Gate standard): the two claim counters were re-run as
the claims' own counting commands; the remaining gate verdicts were evidence-verified from committed
receipts.
