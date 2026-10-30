# C2MeasureExecA — independent C2 measurement

## What ran

Fresh shared clone path: `/fast/scratch/hyaku/kengaku-r53/C2MeasureExecA/lane`; `git rev-parse --show-toplevel` printed that exact path. Measured HEAD: `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe`.

Commands:
```sh
S=/fast/scratch/hyaku/kengaku-r53/C2MeasureExecA
mkdir -p "$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel
git -C "$S/lane" rev-parse HEAD
cat /proc/loadavg
/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
cd "$S/lane"
mkdir -p "$S/work"
env TMPDIR="$S/tmproot" nohup setsid python3 plans/round53_c2_tipstate.py --lane . --source "$S/lane" --work "$S/work" --jobs 3 --timeout 900 > "$S/out.txt" 2>&1 &
```
The detached run exited 1. Its complete stdout/stderr:
```text
ROWS registry=78 ledger=78 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok
ARGV entry=74 selftest=4 help=0 help_limit=7.8
SOURCE rev=b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe clean=yes lane_rev_equal=yes
  MISMATCH round53-c1 declared exit=0 observed exit=1 sec=0.8
RUN executed=78 timeout=0 mismatched=1 evidence_missing=0
TIPSTATE declared_green=66 declared_red=12 observed_green=65 observed_red=13
PREDICATE R53-C2 fail
```
The diagnostic `disagreed-round53-c1.txt` contains:
```text
exit=1 sec=0.8
PINS population_sha=ok pin_tree_sha=ok tests_index_sha=ok r52_audit_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184
FREEZE clean=yes classifier_and_freeze_one_commit=yes classifier_sha=ok label_files_pinned=ok shards_pinned=ok labels_after_freeze_and_untouched=yes authors=4
ORACLE tests=305 bad_label_files=0 bad_label_rows=0 decided=305 contested=0 oracle_Y=52 oracle_N=253 v2_P1=52 unclassified=0 disagree=0 limit=9.2 per_label_agree=1.000 (min 0.9)
ORACLE-CONTROL r52_classifier_disagree=23 all_P0_disagree=52 control_ok=yes
CONFIRM candidates_never_read=28 new_confirmed=0 rejected=0 target>=3
PRIOR-ART rows=0 tasks_covered=0/0 known=0 new=0 urls=0 rejected=0 target: urls>=3 new>=1
PREDICATE R53-C1 fail
```
Verbatim disagreeing-row fragment (under 200 chars): `MISMATCH round53-c1 declared exit=0 observed exit=1 sec=0.8`. It fails because the current C1 output has `PREDICATE R53-C1 fail`, despite the declared C2 exit 0.

Load averages: before run `7.04 6.77 5.43 30/6318 3251870`; after run `17.89 12.95 9.64 10/8321 2949486` (a later read after inspecting diagnostic showed `18.30 13.11 9.71 18/8594 2993121`). Exact wall time was not instrumented/captured; the run completed before the 900-second wait ended, so only an upper bound of 900 seconds is available. Row-reported runtime for the disagreement is 0.8 sec.

## Red-row reason check

The measured rows and their stored reasons agree with observed outputs and the frozen facts' stated causes: `round51-surfaces` (NUMBER-DRIFT: SF14 says 171, output counts 186); `state-assertion-check` and `round28-census` (P3c box-4 pointer mismatch to blank line 129); `round35-c1-coverage` (V4 expects 42/42); `round38-c1-mutants` (N21 survives); `mutant-direction-check` (N21 is MISLABELLED); `round46-c3` (V7 requirement-map omissions and V8 not-PASS); `round52-c1` (literal 184 expected versus 183 present); `anchor-digest-check` (S173–S193 sha256 anchors lack capture locators); `gate-flip-check` (three unresolved flips); `adoption-check` (hardcoded fleet path); and `round40-c1-mutants` (21 anchor-unbound rows cause battery fixture mismatches). This is a reason-text review against the ledger and frozen facts; only `round53-c1` was an exit mismatch.

## Artifacts and disposition

No ledger changes made. The temporary clone, work directory and output file were removed after recording results. No tools installed. Disk guard reported 463.2G free under `/fast/scratch/hyaku` before the run. Produced report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C2MeasureExecA.md`.
