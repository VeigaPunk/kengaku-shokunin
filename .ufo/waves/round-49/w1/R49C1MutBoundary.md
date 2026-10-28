# R49C1MutBoundary — inside-`d` boundary mutations

Axes named: calibration (R49-C1).

**VERDICT: PROVISIONAL DEVELOPMENT PROBE; not an R49-C1 score or admission.** The stage-1 freeze exists and predates these runs, but the R49 stage-2 v3 counter, stage-2 frozen population, and landed fence are not yet present at the measured base. I therefore ran only the committed R48 v2 detector as a bounded development probe against the live wave-1 `R49C1ExecFenceA/fence_a.py` candidate, using the currently available 120 honest (104 battery + 16 R48 novel), 20 refusal, and 12 sealed cases. Wave-1 R49 additions are not included. Findings below are provisional case-to-mutant mappings for L1 to re-run/pin after stage 2; no R49 predicate or mutation floor is claimed.

## Freeze and harness evidence

The full frozen claims and routed spotcheck were read first. Verification:

```text
git rev-parse 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93
git log -1 --format='%H %cI %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering)
git merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 master
ANCESTOR-OF-MASTER-OK
```

The frozen commit adds `plans/round-49-claims.md`; it predates measurement on 2026-10-28. Clone was made with `git clone --shared --no-checkout ...` and detached at the frozen revision. Before fixture work, `git -C "$D" rev-parse --show-toplevel` returned `/fast/scratch/hyaku/kengaku-r49/R49C1MutBoundary/lane`, equal to the clone path (`TOPLEVEL-OK`). Fixture builder inspection confirmed its `git()` wrapper checks `rev-parse --show-toplevel` equals the fixture path before every write-capable Git operation. All detector `--work` roots were under this seat's scratch; no fixture Git operation targeted the lane.

Bounded detector: committed `.ufo/waves/round-48/w1/R48C1ExecControls/fences/round48_c1_verify.v2.py`, using its `--fence`, `--honest`, and `--work` overrides and the pinned R46 builder/counter. Host prerequisites observed: `/usr/bin/bwrap`, `/usr/bin/strace`, `/usr/bin/python3` executable; `strace -- version 7.2`, `bubblewrap 0.13.1`. Candidate file read from the live wave-1 scratch artifact (not committed/landed) and copied into my scratch; pristine SHA-256 `b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52`.

Exact detector command shape used for each pass (substitute `ID` with `base`, `followsymlink`, `pathnorm`, `relativeargv`, `dotdot`, `lanesymlink`, or `restored`):

```sh
python3 "$D/.ufo/waves/round-48/w1/R48C1ExecControls/fences/round48_c1_verify.v2.py" \
  --lane "$D" --work "$S/work/ID" --jobs 8 \
  --honest "$D/plans/honest48" --fence "$S/candidates/ID.py" > "$S/ID.out" 2>&1
```

For `base`, fence path was `candidates/pristine.py`; `restored` was a byte-copy of that same pristine file. Every detector receipt printed `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93`, `TREE dirty=1 (override)`, `PINS total=82 mismatched=0`; `FENCE-RUN` count was 169 (verified by counting lines beginning `FENCE-RUN ` in `base.out`). The one dirty path was the scratch-only `plans/honest48/` copy of the 16 already-pinned R48 modules. All logged cases had `touches=0`; the candidate's R48 baseline was clean on this population.

## Mutants and case attribution

| ID | One behavior mutation (against pristine candidate) | Mutant SHA-256 | Observed result and frozen cases |
|---|---|---|---|
| MB-SYM-FOLLOW | `_entries`: `DirEntry.stat(follow_symlinks=False)` → `follow_symlinks=True`, so a symlinked store directory is classified by its target | `7fc1781499e600ff1cb02238eb1f57c3efb6d2ac292fefb1db13acdd4d0c1c55` | **KILLED** (counter signature failed). These cases changed from `BREACH clean` to `ADMIT benign touches=0`: refusal `f15_objects_symlink_out.py / link-objects-symlink-out`; sealed `s_objects_link.py / seal-objects-link`, `s_refs_link.py / seal-refs-link`, `s_packed_refs.py / seal-packed-refs-link`, `p_info_redirect.py / sealed-info-redirect`, `p_pack_redirect.py / sealed-pack-redirect`, and `p_refs_redirect.py / sealed-refs-redirect`. Rollups: `REFUSALS total=20 clean=19 leaked=0 read=0 hung=0 build_errors=0`; `SEALED total=12 clean=6 leaked=0 read=0 hung=0 build_errors=0`; `PREDICATE R48-C1 fail`. These are benign admissions, not traced outside reads; they still break the hostile clean signature. |
| MB-REL-BASE | `_argv`: resolve relative path values against `parent(d)` rather than `d` | `83b3dd76cd734261006bd0c4b7fff6238c0ff346e731e96cb26392c9567f2d3a` | **KILLED** by honest cases: 61/120 honest fixtures changed from `ADMIT benign` to `BREACH clean`, including battery42 `o_clause-clean-order`, battery43 `o_scan-n5c-case-third-commit`, and R48 honest `n10-empty-repo`, `n03-detached-head`, `n08-tag-detached` (all 61 case keys were compared by `(group,module,fid)`). Hostile legs remained clean; `HONEST fixtures=120 admitted=59 refused=61 read=0 hung=0 build_errors=0`; `PREDICATE R48-C1 fail`.
| MB-DOTDOT | `_inside`: preserve raw `p` instead of `_norm(p)` before the component-prefix check, allowing a `d/../...` spelling to match the `d/` prefix | `865c86efe62a67fdd6bd2cfc9ce283eb6d0b2fabb6dfa7a8edeca10e78fbd02e` | **SURVIVED** this frozen population: no `FENCE-RUN` case changed; all rollups remained clean and `PREDICATE R48-C1 pass`. `f17_argv_nul.py / argv-nul-lane` still breaches at the earlier NUL check, so this is not evidence of un-NULed `..` traversal coverage. |
| MB-NORM-ID | `_norm(p)`: return `str(p)` rather than `os.path.normpath(str(p))` | `c1ec62153e6c24e0f8a3b7991fe07630f7f143fb3a08c1f50984530690b1b51e` | **SURVIVED**: no case changed; same clean rollups and `PREDICATE R48-C1 pass`. |
| MB-D-SYMLINK | Disable the `lstat(d)` symlink refusal in `breach` | `4383d3c2343b248b41bd98f586268495cc8a700b305f014a5a7a619198b7e934` | **SURVIVED**: no case changed; same clean rollups and `PREDICATE R48-C1 pass`. No available frozen case makes the fixture root itself a symlink. |

Pristine baseline verbatim signature:

```text
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
PINS total=82 mismatched=0
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=120 admitted=120 refused=0 read=0 hung=0 build_errors=0
PREDICATE R48-C1 pass
```

Restoration: `pristine.py` and `restored.py` both hashed to `b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52`. The same detector rerun on `restored.py` printed the same `REV`, `PINS total=82 mismatched=0`, `REFUSALS ... clean=20`, `SEALED ... clean=12`, `HONEST ... admitted=120`, and `PREDICATE R48-C1 pass`. Mutations were separate scratch copies; the pristine file was never changed. No lane source was edited.

## Exact setup and detector commands

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r49/R49C1MutBoundary
export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C1MutBoundary
D=/fast/scratch/hyaku/kengaku-r49/R49C1MutBoundary/lane
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D"
git -C "$D" checkout --detach 9d2900af41e4d1fc6022eff99010436fde6dbd93
# After checking clone top-level equals $D:
mkdir -p "$D/plans/honest48" "$TMPDIR/candidates" "$TMPDIR/work"
cp "$D/.ufo/waves/round-48/w1/R48C1ExecHonest/modules/r46novel/"*.py \
   "$D/.ufo/waves/round-48/w1/R48C1ExecHonest/modules/novel48/"*.py "$D/plans/honest48/"
cp /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1ExecFenceA/fence_a.py "$TMPDIR/candidates/pristine.py"
```

Detector was then run once per ID with the exact command template above. No package/tool was installed.

## Limits

- R49 stage-2 counter/population and landed fence are absent from the frozen base; this is not the R49 C1 mutant floor receipt. R48 v2 is only the available bounded detector and reports `R48-C1`, not `R49-C1`.
- 16 R48 honest modules and the 104 standing battery fixtures, 20 refusals, and 12 sealed modules were tested; wave-1 R49 honest/held-out sealed cases were not available in this base snapshot.
- `..` preservation survived because the currently frozen cases do not exercise an un-NULed `..` argv escape. Do not treat this coverage finding as a contract change; stage 2 must rerun against its pinned population and landed fence.
- No R49 admission, score, or full mutation-floor conclusion is made.

## Source locator records (accessed 2026-10-28)

All sources below are local files; `file://` URLs identify the exact opened source. Each located quote is ≤25 words.

- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-49-claims.md` — “Stage 1 (this commit): the predicate sentence, the counter contract and its deltas, the controls that must fail, and the kill rule — for each claim.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-48-verifier-spotcheck.md` — “Any future C1 admission attempt needs the mutation floor committed with receipts.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1ExecFenceA/fence_a.py` — “argv must be the tool's exact option shape; every value must be a path that stays inside `d` lexically”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecControls/fences/round48_c1_verify.v2.py` — “the fixture fence is admitted only when it admits every fixture”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round46_c1_verify.py` — “Round-46 C1 counter (calibration): does the lane's fixture fence do what the lane says it does?”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py` — “if top.returncode != 0 or pathlib.Path(top.stdout.strip()).resolve() != repo:”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/refusals46/f15_objects_symlink_out.py` — “One class: object store symlinked out of `d`.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sealed46/s_objects_link.py` — “(r / ".git" / "objects").symlink_to(outside / "objects", target_is_directory=True)”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sealed46/p_refs_redirect.py` — “Hostile filesystem-shape module: refs directory redirected outside the fixture.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/refusals46/f17_argv_nul.py` — “the `--lane` value carries an embedded NUL.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1MutBoundary.md` — “no mutants scored.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecControls/receipts/control-c1-base-fence.txt` — “REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0”.

## Cleanup

Scratch root `/fast/scratch/hyaku/kengaku-r49/R49C1MutBoundary` is removed before yield. This report contains all findings and the relevant receipt outputs; no R49 production file, claims file, lesson, scorecard, or log was changed.
