# R53CritDoNothing — scoped review

Axes: **calibration, novelty**. Reviewed claims A1–A3 and facts.md. No admission/judgment is issued here.

## Result

Literal omission controls fail both predicates. However, **C1 accepts fabricated confirmations/prior art**, and **C2 accepts measuring selftests in place of four documented entry commands**. These are distinct from literal do-nothing controls: neither should be described as an unchanged base tree passing.

Measured current-tip clone: `9ead4476bf55b1ea6490d0204b668195db4a4d1d` (lane advanced from the assignment's `b1f79a54…`). Frozen base: `536925b5320fa64298030b4ee76a58fc4b82723f`. All experiments used scratch clones; instrument sources and registry rows were unchanged in the successful counterexamples.

## Required omission controls

### Frozen base

The counters **do not exist at the base commit**: their addition is `a34838f8`. Therefore the literal commands cannot run from that checkout without supplying the instrument. I copied the current-tip counter scripts into the scratch base checkout and ran the requested commands there. This adds untracked counter files, but FREEZE already fails on absence before checking cleanliness.

C1, exit 1:

```text
PINS population_sha=ok pin_tree_sha=BAD tests_index_sha=BAD r52_audit_sha=ok captures_blob_match=0 blob_bad=0 absent=0 excluded_blob=BAD files=-1
FREEZE absent missing=18 first=plans/round53-c1-freeze.json
ORACLE not evaluable (pins or freeze failed)
CONFIRM new_confirmed=0
PRIOR-ART rows=0
PREDICATE R53-C1 fail
```

C2 `--dry`, exit 1 (75 MISSING rows between the first and LEDGER lines):

```text
ROWS registry=75 ledger=0 missing=75 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=BAD
  LEDGER ledger absent: plans/round53-tipstate.json
ARGV entry=0 selftest=0 help=0 help_limit=7.5
DRY static legs only: no predicate
```

`--dry` intentionally prints no predicate. `row_set_pinned=BAD` reflects the three round-53 extras absent from the base registry. The 75 missing names were:

```text
adoption-check anchor-digest-check attrib-probe benchmark-spec-audit build-pmars-probe catalog-probe config-projection constraints-probe coverage-census db-wal-probe defect-ledger extraction-policy-compare feal-linear-probe feal-probe fibsqrt-probe gate-flip-check gate-timing git-leak-probe git-webserver-probe grader-perturb hermetic-grader interval-reverdict ledger-tip mutant-direction-check order-check package-gate password-recovery-probe polyglot-c-py-probe regex-log-probe registry-reference-check round-close-check round28-census round30-defects round31-c1-literals round31-defects round33-c1-literals round33-defects round35-c1-coverage round35-hardening round36-c1-battery round36-c2 round37-c1-mutants round37-c2 round38-c1-mutants round38-c2 round39-c1-audit round39-c1-mutants round39-c2 round40-c1-mutants round40-c2 round41-c1-mutants round41-c2 round42-c1-mutants round42-c2 round43-c1-mutants round43-c2 round44-c1-mutants round44-c2 round45-c1 round45-c2 round46-c1 round46-c2 round46-c3 round50-c1 round50-c2 round51-surfaces round52-c1 round52-c2 routed-findings scratch-root-guard sources-adopt state-assertion-check tb2-grader-probe tip-receipts
```

### Current tip with evidence removed

At the cloned tip, confirmations.json and plans/round53-tipstate.json existed; prior-art.json and fetched/ were already absent. Removed all four requested inputs with `rm -f` / `rm -rf`, scratch only.

Uncommitted deletion fails C1 first at `FREEZE clean=NO`, masking evaluation of the missing-work legs. To isolate those legs, I additionally committed the deletion in an isolated scratch clone (own object store, no alternates), local revision `e35f15ea9f09edb2f63e8ae2feba7b522de6525a`. FREEZE then passes clean=yes and C1 prints:

```text
CONFIRM candidates_never_read=28 new_confirmed=0 rejected=0 target>=3
PRIOR-ART rows=0 tasks_covered=0/0 known=0 new=0 urls=0 rejected=0 target: urls>=3 new>=1
PREDICATE R53-C1 fail
```

C2 full command on that clone prints:

```text
ROWS registry=78 ledger=0 missing=78 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok
  LEDGER ledger absent: plans/round53-tipstate.json
ARGV entry=0 selftest=0 help=0 help_limit=7.8
PREDICATE R53-C2 fail
```

Both exit 1. The ledger-absent full C2 run executes no rows.

### Committed selftests re-executed

At the unmodified tip clone, both exit 0, matching the committed receipts:

```text
C1: SELFTEST cases=47 failures=0
C2: SELFTEST cases=52 failures=0
```

These counts supersede the older 44/50 prose figures as A2/A3 specify.

## Counterexample 1 — fabricated C1 evidence passes

**Attack landed.** The 20 real confirmations were retained, but every prior-art archive was locally authored, not fetched. URLs used the reserved `.invalid` TLD. A row's digest was computed from the same locally authored file; its first line asserted SOURCE-URL. New rows received two similarly authored sweep files. No network request was made.

At local revision `ffff88755cbcb51ee32461e622bf2f1417acbb7c`:

```text
CONFIRM candidates_never_read=28 new_confirmed=20 rejected=0 target>=3
PRIOR-ART rows=20 tasks_covered=20/20 known=1 new=19 urls=20 rejected=0 target: urls>=3 new>=1
PREDICATE R53-C1 pass
```

Exit 0. Thus even retaining the full 20-task set does not authenticate the prior-art work.

A second control fabricated the confirmations too: three candidate tests, a quote copied mechanically from each normalized span prefix, and one self-written FakeReader report per task naming that task. With three fabricated prior-art rows:

```text
CONFIRM candidates_never_read=28 new_confirmed=3 rejected=0 target>=3
PRIOR-ART rows=3 tasks_covered=3/3 known=1 new=2 urls=3 rejected=0 target: urls>=3 new>=1
PREDICATE R53-C1 pass
```

Exit 0. An initial fixture accidentally overwrote one shared report file three times; two digest mismatches correctly rejected it. Distinct reports removed that fixture defect.

Evidence: `plans/round53_c1_triage.py:325-361` verifies report/quote consistency, not reader identity; `:383-454` verifies local archive/header/digest/quote consistency. The URL test at `:417` accepts a URL-shaped host unless it contains example.org. The counter has no URL-fetching implementation and no SOURCES.md reference. The selftest's local archive construction at `:619-643` also illustrates the distinction.

**Impacted axes:** novelty (new/known and negative sweeps are unauthenticated), calibration (a passing predicate cannot certify independent reading or real fetching).

**Smallest safe correction:** preserve the existing structural checks, but bind report and archive digests to an independently attested, immutable manifest from the assigned reader/fetcher seats; verify seat identity outside self-authored path text. Keep the grader offline. A SOURCES.md cross-reference would improve consistency with the stated frontier, but **another lane-authored URL/digest pair alone does not authenticate provenance**. Otherwise explicitly limit the claim to local evidence consistency and retain independent review as a separate acceptance condition. The 3-task threshold is allowed by the frozen claim; pricing all 20 is a wave milestone, not an extra frozen predicate leg. Do not silently raise that threshold after scoring.

## Counterexample 2 — C2 can measure selftests instead of entry commands

**Attack landed, clean full-run witness.** Starting from the tip ledger, changed four red rows to argv ending in --selftest, declared green/0, kind=selftest: state-assertion-check, round51-surfaces, round52-c1, gate-flip-check. Their documented entry commands exit 1 in the original ledger; the alternative selftests each exited 0 in direct probes. No script or registry text changed. Separately corrected the stale round53-c1 declaration from green/0 to red/1 (evidence: PRIOR-ART rows=0).

Local revision `95dae3088e2d971bb7dd35dba95638a9837e6781`, clean full run:

```text
ROWS registry=78 ledger=78 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok
ARGV entry=70 selftest=8 help=0 help_limit=7.8
SOURCE rev=95dae3088e2d971bb7dd35dba95638a9837e6781 clean=yes lane_rev_equal=yes
RUN executed=78 timeout=0 mismatched=0 evidence_missing=0
TIPSTATE declared_green=69 declared_red=9 observed_green=69 observed_red=9
PREDICATE R53-C2 pass
```

Exit 0; 274.55 seconds. See c2-repoint-pass.txt.

Evidence: `argv_ok` at `plans/round53_c2_tipstate.py:150-166` checks the script path, not the entry flags; `run_row` executes the ledger argv. Example registry entry: `SKILL.md:567`, state-assertion-check uses --summary; its self-test column uses --selftest. The substituted argv remains the same script and passes kind_ok.

This is **permitted by the frozen script-only rule**, not an implementation deviation. The claim must therefore be read as truth about the ledger-selected invocation, not necessarily about each registry entry invocation. Selftest-kind is uncapped; help-kind is capped at 10%. An exploratory all-red-to-green help/selftest variant produced eight help rows, exceeding 7.8; that is not a passing witness and is not relied on here.

**Impacted axis:** calibration. The observation leg is real, but observes a claimant-selected invocation.

**Smallest safe correction:** preserve the declared-exit comparison, but bind each row to an independently frozen concrete entry argv (with explicit placeholder substitutions). Selftest/help may be separately named, disclosed instruments, not substitutes for the entry's tip-state. Under the existing frozen contract, retain this as a disclosed scope limitation rather than claiming the counter rejects it.

## Execution notes and commands

Scratch prefix S=/fast/scratch/hyaku/kengaku-r53/R53CritDoNothing; TMPDIR=$S/tmp was explicitly supplied to counter runs. Lane L=/home/vgpnk/Projects/shokunin/kengaku-shokunin. Core commands:

```sh
bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
git clone -q --shared "$L" "$S/base"
git -C "$S/base" rev-parse --show-toplevel
git -C "$S/base" checkout --detach 536925b5320fa64298030b4ee76a58fc4b82723f
git clone -q --shared "$L" "$S/tip"
git -C "$S/tip" rev-parse --show-toplevel
cp "$S/tip/plans/round53_c1_triage.py" "$S/base/plans/"
cp "$S/tip/plans/round53_c2_tipstate.py" "$S/base/plans/"
# cwd=$S/base
python3 plans/round53_c1_triage.py --lane .
python3 plans/round53_c2_tipstate.py --lane . --dry
# cwd=$S/tip
python3 plans/round53_c1_triage.py --lane .
python3 plans/round53_c1_triage.py --selftest
python3 plans/round53_c2_tipstate.py --selftest
python3 plans/round53_c1_triage.py --lane . --candidates
# dedicated isolated clones used git clone -q --no-hardlinks "$L" "$D"
# every mutation followed an explicit toplevel assertion; commits were scratch-local only.
# cwd=clean deletion clone
python3 plans/round53_c1_triage.py --lane .
python3 plans/round53_c2_tipstate.py --lane . --source . --work "$S/work-tipdel2" --jobs 4
# cwd=C1 fabricated fixture
python3 plans/round53_c1_triage.py --lane .
# cwd=C2 re-point fixture; the successful solo run
timeout 900 python3 plans/round53_c2_tipstate.py --lane . --source . --work "$S/work-solo2" --jobs 8
```

Additional direct probes ran python3 SCRIPT with no flags, --selftest, --help, --json and --summary against the twelve original red rows. Per-call timeouts were 45, 60, 90 or 120 seconds; timeout outcomes were not counted as genuine exits. Those probes informed the four-row witness above. Some full-run launches used nohup and returned only the launcher's status; these are **not** evidence that the child completed. Earlier concurrent runs reused a work directory and produced clone errors/missing temporary files. Their three mismatches are not attributed to the ledger change; the successful isolated run supersedes them. No claim is made that a tip change itself causes those failures.

Disk guard initially reported 467.6G free under /fast/scratch/hyaku; df reported 464G available on /fast. No ENOSPC observed. No tools installed or upgraded. No lane instrument, registry, fleet tracked file, or sibling artifact edited. Commands that attempted to read a nonexistent path or lacked output are not treated as measurement evidence.

## Kept artifacts

All absolute paths below share prefix `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53CritDoNothing/`:

- receipts.txt — required control/selftest outputs and earlier observations.
- c2-repoint-pass.txt — successful clean C2 witness.
- c1-fabricated-both/ — fabricated confirmations.json, prior-art.json, FakeReader reports and fetched/ files; no grader source.
- c1-three-real/ — three retained real confirmations and fabricated prior art inputs.
- c2-repoint/round53-tipstate.json — passing re-pointed ledger.
- Nonempty out/*.txt files copied into this directory retain diagnostics, including failed/contaminated launches; do not confuse them with the successful witness.

The report itself is `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53CritDoNothing.md`.

Self-evaluation: accuracy 4 (earlier contaminated runs excluded); completeness 4 (all required controls exercised; source scripts absent at base disclosed); clarity 4 (literal omission separated from fabrication); actionability 4 (concrete witnesses and corrections); conciseness 3 (long transcript reduced to scoped evidence here). Overall 3.8. No admission score is inferred from these self-ratings.

Cleanup completed: terminated five processes whose actual cwd was within this seat's scratch, then removed `/fast/scratch/hyaku/kengaku-r53/R53CritDoNothing/`. Preserved 28 artifact files; largest is 16,800 bytes. No scratch clone remains.
