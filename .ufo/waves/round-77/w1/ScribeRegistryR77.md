# ScribeRegistryR77 — scoped report

## Behavior and axes

Coverage: R77-C1, held at L0 cap 7. Calibration: R77-C2, held at ceiling 10. Deliverable is a proposal, not integrated product changes or a target verdict.

Proposal: `.ufo/waves/round-77/w1/proposals/registry.md` contains two corrected R76 registry rows, two new R77 registry rows, and two proposed SCORECARD capability rows. All registry rows use the existing eight-column shape. C2's unexecuted tallies are explicitly marked declaration-only, not execution evidence.

## Commands and outcomes

Read the entire 146-line `plans/round-77-claims.md` before any shell command. Read the R77-C2 counter and grep-anchored V2's required nine classes. Read godspeed and self-evaluation skills.

1. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format=%H -- plans/round-77-claims.md` — exit 0, printed `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`.
2. `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c1_surface_resolver.py --help && python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round76_c2_defect_discharge.py --help` — exit 0. C1 exposes `--expect-manifest`, omitted from the old registry flag list; C2 exposes `--selftest-git`.
3. `mkdir -p /fast/scratch/hyaku/kengaku-r77/ScribeRegistryR77/snapshot && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb | tar -x -C /fast/scratch/hyaku/kengaku-r77/ScribeRegistryR77/snapshot` — exit 0. Read-only archive extraction, not a clone; no Git mutation.
4. Specialized `grep` on the four extracted committed R76 receipts with `SELFTEST cases=|MUTANTS |LANE_TIP` returned:
   - `corpus/evidence/round76/c1-selftest.txt:15`: `SELFTEST cases=12 red=11 failures=0 ok=True`.
   - `corpus/evidence/round76/c1-mutants.txt:12`: `MUTANTS total=9 killed=9 expected_matched=9 wrong_id=0 survived=0`.
   - `corpus/evidence/round76/c2-selftest.txt:17`: `SELFTEST cases=14 red=13 failures=0 ok=True`.
   - `corpus/evidence/round76/c2-mutants.txt:15`: `MUTANTS total=12 killed=12 expected_matched=12 wrong_id=0 survived=0`.
   These are stored lines, not fresh runs. C1 receipts stamp `c8c116b48fdc1334baf73174ca4f95c86b082590`; C2 stamps `d68c11430a789da106265d66eeb22f739e461cf1`. All four say `WORKTREE dirty`. The requested `MUTANTS real=` literal does not occur in these receipts; the actual key is `total=`.
5. `python3 /fast/scratch/hyaku/kengaku-r77/ScribeRegistryR77/snapshot/plans/round77_c1_declared_surfaces.py --lane /fast/scratch/hyaku/kengaku-r77/ScribeRegistryR77/snapshot --selftest --work /fast/scratch/hyaku/kengaku-r77/ScribeRegistryR77/c1-selftest` — exit 0; printed six `SELFTEST ok` lines and `SELFTEST cases=6 red=5 failures=0`.
6. `python3 /fast/scratch/hyaku/kengaku-r77/ScribeRegistryR77/snapshot/plans/round77_c1_declared_surfaces.py --lane /fast/scratch/hyaku/kengaku-r77/ScribeRegistryR77/snapshot --mutants --work /fast/scratch/hyaku/kengaku-r77/ScribeRegistryR77/c1-mutants` — exit 0; printed six killed rows and `MUTANTS real=6 expected_matched=6 wrong_id=0 survived=0`.
7. `python3 /fast/scratch/hyaku/kengaku-r77/ScribeRegistryR77/snapshot/plans/round77_c1_declared_surfaces.py --help && python3 /fast/scratch/hyaku/kengaku-r77/ScribeRegistryR77/snapshot/plans/round77_c2_defect_discharge.py --help` — exit 0; registry flags drafted from those outputs.
8. Specialized `grep` on frozen C2 source with `"init"|"add"|"commit"|"checkout"|SELFTEST cases=|MUTANTS real=|cases =|def selftest|def mutants` returned mutation callsites: fixture `init/add/commit` at 516–520; stamp `add/commit` 552–553; side branch `checkout/commit` 561–565; git-arm `init/commit` 612–616; mutant side-pin `add/commit` 673–674. No C2 battery was run.
9. `rm -rf /fast/scratch/hyaku/kengaku-r77/ScribeRegistryR77 && test ! -e /fast/scratch/hyaku/kengaku-r77/ScribeRegistryR77` — exit 0. Owned scratch tree removed; no remaining scratch-tree defect.

The two C1 battery calls ran concurrently. No extra battery rerun was performed to decorate the report. Specialized grep/read outcomes are named by their returned lines rather than invented subprocess exit codes.

## Findings and exact contract conflict

- Frozen R76 registry entries advertise C1 `cases=7 red=6` and C2 `cases=10 red=9`; committed final receipts establish C1 12/11 and 9/9, C2 14/13 and 12/12. A subsequent live-file read already showed another owner had corrected those entries; proposal is not a claim that they remain stale at landing.
- Required C1 classes are included: NONLOCAL-ANCHOR, ESCAPE-ANCHOR, OVERFLOW-ANCHOR, MALFORMED-DATE, DUPLICATE-SURFACE, MANIFEST-DRIFT. Required C2 classes are included: EMPTY-SCOPE, LEG-PENDING, NEGATED-DISCHARGE. Existing additional defect classes are preserved.
- Binding contract verbatim: **“No commits, no pushes, no mutating git/jj anywhere.”** Item verbatim: **“run `--selftest` and `--mutants` in a scratch clone at the freeze revision and paste the tallies”**. Frozen R77-C2 implements those modes through Git mutations above. These requirements conflict; the battery runs were withheld and Main was notified. Declared C2 `cases=10 red=9`, git arms 3/3, and mutant six-of-six are not this seat's execution evidence. The proposal retains that limitation rather than fabricating a pass.
- Snapshot extraction uses `git archive`, because the binding contract also prevents a mutating `git clone` invocation. Exported committed tree bytes suffice for C1's non-Git fixture runs; they do not establish a Git-clone execution environment.
- Specialized grep of frozen `corpus/evidence/round77/` for `SELFTEST cases=|MUTANTS real=|GIT-ARMS cases=` returned no matches. There is no frozen C2 battery receipt available there to substitute for the blocked run.

## Gates and known limits

Observed green: R77-C1 fixture selftest and six-mutant matrix only. Not exercised: R77-C1 landing target, R77-C2 landing target, R77-C2 batteries, V2 integrated gate, capability first-working landing receipts. No statement that all seven discharge legs pass. No fresh R76 battery execution; committed receipt tallies only. Capability rows distinguish scope from demonstration and nominate round 77 conditionally on the integration owner's receipts.

## Touched surfaces and out of scope

Permanent writes only:
- `.ufo/waves/round-77/w1/proposals/registry.md`
- `.ufo/waves/round-77/w1/ScribeRegistryR77.md`

Scratch export/fixtures were owned and removed. No production edits, Git mutations, commits, pushes, judge/runtime dispatch, installations, package operations, fleet tracked-file writes, or other-lane changes. Integration and judgment remain with their designated owners.

## Self-evaluation

Accuracy 4/5: observed C1 output and committed R76 lines are separated from C2 source-only values; blocked C2 prevents full empirical coverage. Completeness 3/5: every requested row is drafted, but C2 execution is prohibited by the quoted contract. Clarity 4/5: proposal is pasteable but qualifications must remain visible. Actionability 4/5: exact rows and blockers are provided; authorized C2 receipt remains necessary. Conciseness 4/5: command provenance requires a longer report. Overall 3.8/5. Highest-impact improvement requires resolving the conflicting C2 execution authorization, not weakening frozen rules. User agreement self-check: the remaining execution gap is explicit and attributable to the binding contract.
