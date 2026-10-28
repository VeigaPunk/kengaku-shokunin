# R49RevReport — pre-check of the round-49 report structure against the frozen contract

Seat: reviewer, wave w1. Item: pre-check the round report structure (`.ufo/reports/round-49/kengaku.md` on the fleet
repo) against the frozen report contract (`.ufo/prompts/kengaku-round-49.md` §1–§6 + `plans/round-49-claims.md`
freeze shape) before the L1 files it. Reviewer scope only: no admission claim, no counter/probe scored run.

## Axes named

calibration (R49-C1 evidence-pointer conformance) and coverage (R49-C2 structural/conformance completeness). This
seat attacks the *structure the verifier will check*: required sections, resolvable evidence pointers, SHONEN
boxes, census command, ordering/fresh-start duties.

## Stage-1 freeze gate (required before any scored run)

`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show -s --format='%H %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93` →
`9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 …` — exists,
committed, `merge-base --is-ancestor 9d2900af master` → ancestor OK. Lane tip now `af88aab193e6…` (wave-spec
commit, 09:18:20, also ancestor). Wave is in flight (dispatched 09:20:02); **no scored counter/probe run was made
by this seat** — structural review only.

## Contract terms checked (source: `.ufo/prompts/kengaku-round-49.md`, cited by line)

- §4: report at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-49/kengaku.md`; required sections in order —
  **Work performed** (claims + target axes named first, evidence pointer per bullet), **Landed changes** (LOG.md
  entry + commit hash each), **Before → after measurements** (counting command + measured commit per claim),
  **Sources & frontier** (rows before→after with counting command; a no-corpus line is `SOURCES: unchanged —`),
  **Trend verdicts** (expansion/quality/discernment ∈ improved|harmed|unchanged|unprovable-but-better, with
  evidence, no scalar), **SHONEN** (one line per SHONEN.md box; `[x]` only with named non-author verifier, `[~]`
  with resolvable pointer, `[ ]` if untouched). Marker rule: missing sections other than Sources & frontier /
  Trend verdicts = failed round; skipping those two = `ok` + conformance defect.
- §2b: census command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin kengaku` pasted at round start AND round end with exit codes (exit 0 required at
  end); one mined mistake in `corpus/lessons/round-49.md`; ≥1 sourced claim (S166 cited at
  `plans/round-49-claims.md:142-144` — gate quote must appear in the round-49 lesson `## Gate`).
- §6/run-10: file only after WAVE-DONE + `w1-results.json`; fresh-start duty (r45 `73540ccc`, r46 `a5ed97f1`,
  r47 `98a0cb51` read before claims; claims a do-nothing control cannot reach); ≥25 % attack share; misroot
  sweep; no `model` field and no role→alias map in lane artifacts.
- Freeze file: receipts prepend `REV <40-hex>`; stage-2 amendment fills literals/pins only, lands BEFORE scoring,
  committed only after amended probe passes `--stage-check` on this host; stage-3 lands the C2 fresh receipt
  (first-commit = stage-3 commit, descendant of stage-2, with `CASE … observed=` lines); any other edit to the
  claims file is named in `Freeze amendments` with its commit.

## Verified now (commands run + verbatim outputs)

- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → 15× `kengaku W04 …`
  duplicate-url warnings then `kengaku ok …/corpus/SOURCES.md`, `exit=0` (bit-identical to round-48's pasted
  output — safe to cite).
- `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `165`; tiers `A=141 B=22 C=2`;
  status `mined=149 queued=8 rejected=8`. If no row lands, before→after is `165→165`.
- Dispatch (`w1-dispatch.json`, taskCall.tasks): **64 seats, 0 `model` fields** (`grep -c '"model"'` on
  dispatch + spec = 0,0), every seat's item names its own `w1/<seat>.md` path (routed defect 1: repaired).
  `w1-spec.json` context (3803 B) contains **no role→alias map** — routed defect 2 repaired at spec level.
  Role counts: executor 11, scribe 4, connector 4, scout 3, reviewer 11, critic 15, mutation-tester 14,
  sentinel 1, revenger 1.
- Commits `3a548330`, `9d2900af`, `af88aab1` all `merge-base --is-ancestor … master` OK; `ls-remote origin` =
  `af88aab1` (pushed). `w1.ready.dispatched` (2331 B) lists the 64 seats; `w1-results.json` absent → wave live.
- Watchdog: `2026-10-28T08:59:38-03:00 launch kengaku round=49 … attempt=1`, no earlier r49 attempt —
  no inherited-outputs paragraph needed.
- SHONEN.md: 4 boxes, all `[~]`-grade — `SKILL.md:23-46` ("## Decision table — benchmark selection"), `LOG.md:7`
  (round-4 eval entry), `corpus/lessons/round-8-aggregator-box3-coldrun.md:48` ("## Box-3 verdict"),
  `PROVINCE.md:129` ("### Adjacent") — all resolve at lane tip.
- No report file yet (`ls .ufo/reports/round-49/kengaku.md` → ENOENT) — correct at this point; required at yield.

## Defects to fix before filing

1. **Attack-share number must say 40/64 (or 41 if revenger is counted) — not just copied 41.** Round-48 counted
   the revenger as attack (41/64). Round-49's own wave-spec commit message says `40 attack`. The report must name
   the counting rule and the number it yields; either way ≥25 % holds (25/64 minimum met with margin).
2. **Before→after rows must carry the *landing-tip* counting command + measured commit.** Round-48's table cited
   only scratch `REV a543d920…` runs and both claims fell to "no committed landing-tip result" — the same row
   shape this round is a guaranteed not-admitted unless the stage-2/3 commits land and
   `python3 plans/round49_c1_verify.py --lane .` / `round49_c2_verify.py` actually run on a clean clone of the
   tip with `REV <40-hex>` prepended to every receipt (Q22).
3. **C1 MUTANTS leg needs committed per-mutant receipts** (`plans/mutants49/c1-mutants.json`, `<M>`≥12,
   `caught ≥ <M>/2`, output `MUTANTS … verdict=met` inside the landing receipt) — routed defect 4; a scorecard
   assertion without receipt repeats the round-48 kill-battery gap.
4. **C2 V7 precondition evidence:** the stage-2 pinned counter must positively verify all 7 frozen tags have
   `violates=` committed cases before scoring; the report must cite the before-control receipt showing the r46
   table *failing* and the amended table passing (routed defect 3; `corpus/lessons/round-48.md:11` requires
   exactly that pairing).
5. **C2 ordering (V8):** only `--dry`/`--stage-check` pre-receipt; the fresh full-run receipt lands at stage 3
   with first-commit = the stage-3 commit. The report must cite `plans/order_check.py` output per control and
   the `git log` ordering evidence; citing a stage-2 receipt as the fresh receipt auto-fails V7+V8.
6. **Claims receipts dir `.ufo/waves/round-49/claims/` does not exist yet** — every frozen control
   (no-fence / base fence @`3a548330` / r45-keyed / admit-all / refuse-all / name-keyed for C1; base tree /
   filler / echo / `22b7779e` fail-receipts for C2) must land there at stage 2 or the controls line is
   unevidenced.
7. **Filing before WAVE-DONE is a run-9 repeat defect** — `w1-results.json` must exist and dead seats must be
   named with last-output state (routed defect 1's seat-item receipt paths already satisfy the naming half).
8. **Round-49 lesson must exist** (`corpus/lessons/round-49.md` absent now) with `## Mistakes` (≥1 mined fix
   shown able to fail), `## Gate` (S166 URL + 2026-10-28 access + ≤25-word quote — claims-file L142-144 promises
   it), and old→new logging of any SOURCES `status`/`recheck`/`used-by` change.
9. **Freeze-amendments paragraph:** stage-2 may touch literals/pins only; any predicate/control/kill-rule edit
   after `9d2900af` must appear under `Freeze amendments` with its commit — check `git log -p
   plans/round-49-claims.md` after the amendment before filing.
10. **Marker-rule nuance:** a report skipping only **Sources & frontier** or **Trend verdicts** is `ok` + a
    conformance defect, not a fail; missing any other required section = failed round / relaunch. Don't pad —
    file both sections (they're cheap: census output above + three trend verdicts).
11. **Honest verdict lines:** if stage-2 lands and a control passes, the claim stops honestly and the report
    says so; if the wave leaves dead seats or a failed stage-check, file with the defects named rather than
    rounded up — the r48 closure's `rejected-honest-stop` precedent rewards honest naming.
12. **Fleet-root misroot sweep** before filing: `git -C /home/vgpnk/Projects/shokunin status --porcelain`
    currently shows only orchestrator artifacts (`?? .scratch/closure-mado-r50.json`, `?? .scratch/
    source-routing-queue.md`, `?? o.bin`, `?? oldrep1.out`, `?? oldrep2.out`, ` M round-58/chousa.md`) — confirm
    no kengaku bytes leaked there at filing.
13. **Return-summary ≤12 lines** to orchestrator: claims+verdicts, lane HEAD, report commit, wave size, role
    mix, dead seats, open L0 questions (`kengaku | round-33` coverage cap still open).

## Limits

Report file absent at check time (wave live) — this pre-check lists contract-shaped defects + verified values;
the landed-diff check itself is the closure's job. Census/histograms measured on lane tip `af88aab1` (tree bytes
identical to `9d2900af` for `corpus/SOURCES.md`). No counter, probe, or fence executed; nothing scored. No tools
installed (pacman paused; nothing needed). Scratch `/fast/scratch/hyaku/kengaku-r49/R49RevReport` removed on
yield via trap.

VERDICT: report contract is checkable and its citable values are frozen above; 13 defects listed — the
structural killers to guard are landing-tip measurement rows (2), C1 mutant receipts (3), C2 V7/V8 ordering
evidence (4–5), and filing only after WAVE-DONE (7).
