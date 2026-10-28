# R49C2PreReceipt — C2 ordering attack

Axis: **coverage**. Revision measured: frozen stage-1 commit `9d2900af41e4d1fc6022eff99010436fde6dbd93` (verified present as a commit in the lane; commit time `2026-10-28T09:14:40-03:00`). The current `HEAD` at inspection was `af88aab193e6034cb9b386472064e3c18fa90128`; no scored probe/counter run was performed. I inspected the frozen ordering contract and existing `plans/order_check.py` / `plans/pkg_gate.py` and ran only a synthetic Git fixture in my scratch clone.

## Strongest concrete bypass

The strongest **committed-evidence** bypass is an early receipt/output staged outside `.ufo/waves/round-49/claims/`, then the canonical receipt path first added by a later commit. `order_check.py` derives `claims_dir` from the round number and `scan_claims()` scans only its blobs (`plans/order_check.py` lines 115–138, 164, 192–198). It does not inspect the early evidence or receipt bytes committed elsewhere. It also checks receipt-vs-freeze order, not the frozen requirement that the receipt's first commit be a strict stage-3 descendant of stage 2.

Fixture commands (all Git writes were made with cwd at the fixture, and `git rev-parse --show-toplevel` returned that fixture path):

```sh
export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C2PreReceipt
D=/fast/scratch/hyaku/kengaku-r49/R49C2PreReceipt/fx
mkdir -p "$D" && cd "$D" && git init -q .
git config user.email t@t && git config user.name t
mkdir -p plans corpus/evidence/round49 .ufo/waves/round-49/claims
echo claims > plans/round-49-claims.md
git add -A && git commit -qm 'stage-1 freeze'
printf 'CASE demo predicted=fail observed=fail tests=F match=yes violates=x\nP10 ok probe_rerun=byte-equal bytes=100\n' > corpus/evidence/round49/early-run.txt
git add -A && git commit -qm 'early full probe run evidence (outside claims/)'
printf 'CASE demo observed=fail\n' > corpus/evidence/round49/polyglot-c-py-probe.txt
git add -A && git commit -qm 'receipt committed pre-stage-2'
echo 'literals filled' >> plans/round-49-claims.md
git add -A && git commit -qm 'stage-2 amendment'
python3 /fast/scratch/hyaku/kengaku-r49/R49C2PreReceipt/lane/plans/order_check.py --lane . --claims plans/round-49-claims.md --receipt corpus/evidence/round49/polyglot-c-py-probe.txt
```

Observed output (hashes abbreviated only where shown):

```text
ORDER claims=plans/round-49-claims.md round=49 freeze=133c0f034408eeb1ef262bd8fe3e40a9438159c4
ORDER receipt=corpus/evidence/round49/polyglot-c-py-probe.txt receipt_commit=46438542439d25f0244c8d7f0ce2d284fe9105d4 claims_dir=.ufo/waves/round-49/claims/
ORDER scanned commits=0 file_entries=0 distinct_blobs=0
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
EXIT=0
```

This PASS occurs although the fixture's receipt was committed before its stage-2 amendment, and before it was committed the output file recorded `CASE … observed=` and `P10 ok`. So neither “receipt commit is after stage 2” nor “no committed evidence of execution before receipt” is established by this gate. A control fixture putting the same two evidence lines under `.ufo/waves/round-49/claims/early-run.txt` instead produced `ORDER HIT` for both lines, `ORDER FAIL probe-executed-before-receipt hits=2`, `ORDER RESULT FAIL`, exit 1. Thus the concrete weakness is the scan boundary, not a failed matcher.

A path/identity variant also passed: I committed `CASE demo observed=fail` at `corpus/evidence/round49/staged-early.txt`, then `git mv`'d it to `corpus/evidence/round49/polyglot-c-py-probe.txt` and committed that rename, before amending claims. `git log --reverse --diff-filter=A --format='%H %s' -- corpus/evidence/round49/polyglot-c-py-probe.txt` reported the rename commit as the path's addition, and `order_check.py` returned `ORDER RESULT PASS` with zero scanned claims entries. Thus first-add-by-path is not proof the blob originated at that commit.

## Forgery / dry-table echo and effective check

A dry-table echo with `observed=<predicted>` can be made to look like a complete CASE receipt; I transformed all 18 frozen dry rows and checked them against the existing `round46_c3_verify.py` receipt parser and `order_check.py` CASE-line regex. Output: `parsed observed-tokens: 18 | ids == dry ids: True`; first row parsed as a CASE with `observed=fail`, and `matches order_check CASE_LINE regex: True`. This is not proof the forged receipt passes the full C2 counter. The decisive existing defense is scoring-time P10: `pkg_gate.py:c_rerun` runs the pinned probe and requires its stdout byte-equal to receipt bytes (lines 267–285); `round46_c3_verify.py:v2` invokes the gate with `--rerun --require-clean-tree` (lines 250–263). Therefore a fabricated or dry-table-derived receipt that differs from fresh probe output is killed by P10. Do not disable P10 for the claimed scoring run; the frozen P10-disabled exception is only for base/filler/echo pre-receipt controls.

However, byte-equal P10 cannot prove *when* an identical receipt was produced: an output produced before stage 2 and replayed later is content-indistinguishable if it matches the fresh run. Git metadata also cannot establish wall-clock run time. Most importantly, existing `order_check.py` only rejects evidence within the claims directory through receipt commit; it does not enforce the frozen stage-2-to-stage-3 ancestry predicate. The future Q40/V8 implementation must enforce that explicitly.

## Smallest safe correction

1. In V8, derive the committed stage-2 amendment anchor from the frozen claims history/pin and require the receipt's **first-commit** to be a strict descendant of that anchor (`merge-base --is-ancestor stage2 receipt_commit`, and reject equality); pin/verify the stage-3 receipt blob and its digest at that commit. This closes pre-stage-2 receipt commits and prevents treating a later path-add/rename as the source receipt. Do not infer stage 2 from committer timestamps.
2. Extend the early-execution evidence scan to all committed evidence locations the workflow permits before stage 3, excluding the canonical receipt blob itself to avoid self-matching. Keep the current claims scan as well. At minimum, wave reports and `corpus/evidence/round49/` must not be invisible to V8.
3. Keep P10 enabled for the claimed scoring run, requiring fresh stdout byte equality. This is the check that kills a forged/echo receipt. It does **not** solve unrecorded scratch execution timing; report that residual as a trust/provenance limit rather than claiming Git proves physical production time.

## Commands, limits, source

Commands run: `git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93`; `git log -1 --format='%H %cI %s' <freeze>` and same for `HEAD`; `git ls-tree -r <freeze> --name-only`; scratch-only `git init`, `git add`, `git commit`, `git mv`, `git log`, `git rev-parse --show-toplevel`; two `python3 …/plans/order_check.py` fixture runs; a Python parser/regex script over the dry table; and source reads of `order_check.py`, `pkg_gate.py`, `round46_c3_verify.py`, the frozen dry table and pinned grader capture. No scored run, production edit, commit, or external web request was made. The synthetic fixture checks the existing checker, not the future R49 counter; its exact final source/commit sequence is recorded in command block/output above. Scratch cleanup is performed before yield.

Source URL (pinned capture; accessed locally 2026-10-28, no HTTP request): `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py`. Located quote, lines 27–27 (10 words): `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]`.

Limits: stage-2/stage-3 commits, the R49 Q40 counter, and the new stage-3 receipt do not yet exist at the frozen revision, so their exact implementation and behavior are unobserved. No result here establishes claim admission. A never-committed scratch run is not provable from Git history; an output nonce newly committed at stage 2 can reject pre-stage-2 cached outputs only if the pinned probe itself consumes and emits it, but still cannot prove the run occurred after stage 2 rather than being replayed during stage-2-to-stage-3.

**VERDICT: ordering check has a concrete bypass; require strict stage-2 ancestry and broaden the pre-receipt evidence scan; retain scoring-time P10 byte-equality. Git alone cannot prove physical run time.**