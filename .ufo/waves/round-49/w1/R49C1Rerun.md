# R49C1Rerun — independent v3 counter candidate rerun

Axes: calibration (R49-C1). Scope: rerun the submitted `candidate.py` against the frozen-base fence and each submitted fence variant; no admission judgment.

## Freeze and measurement boundary

Before measurements, confirmed the committed lane contains the stage-1 freeze:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
commit
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %cI %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering)
$ date -Iseconds
2026-10-28T09:30:34-03:00
```

The independent clone's `HEAD` was `9d2900af41e4d1fc6022eff99010436fde6dbd93`, `git rev-parse --show-toplevel` was `/fast/scratch/hyaku/kengaku-r49/R49C1Rerun/lane`, and `git status --porcelain` had 0 lines before reruns. Freeze predates all three measurements. Stage-2 freeze is absent: `plans/round49_c1_verify.py`, `plans/honest49/`, `plans/sealed49/`, and `plans/mutants49/c1-mutants.json` are absent in that frozen tree. Thus these are candidate reruns with explicit testing overrides, not a stage-2/landing receipt.

Fence A SHA-256 was independently reconstructed by extracting the §7 diff from the round-48 FenceA report and applying it in the clone: `git -C "$D" rev-parse --show-toplevel` printed `$D`; `git -C "$D" apply --check /fast/scratch/hyaku/kengaku-r49/R49C1Rerun/fence_a.diff` returned 0; after apply, `sha256sum plans/fixture_fence.py` printed `b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52`; the clone was restored clean. This matches the submitted `fence_a.py` digest. Fence B digest: `c89bc524ea5d751fd7ca6f22fe13b732c0231b7b789d43ea5b507e430571f116`.

The `--honest` testing override used a scratch-flat copy of the 20 `.py` modules under the submitted tree-shaped `R49C1ExecHonest/plans/honest49/modules/{r46novel,novel48,novel49}`; the counter's `module_files()` scans only immediate `*.py` children, so flattening was necessary to exercise them. Its frozen constants remain `HONEST_TOTAL=104`, `HONEST_NOVEL_EXPECTED=0`, `SEALED_TOTAL=12`, `MUTANT_FLOOR=0`, `PINS_EXTRA={}`. The 23-row mutant JSON was passed exactly as submitted, through `--mutants`; no `sealed49` override/artifact existed. All testing overrides disable default-mode clean-tree and population pin enforcement, as the counter itself reports.

## Exact commands and measured revision

All three commands ran the same submitted counter source (`candidate.py`, SHA-256 `9c7b73e31e64ef61c021324af5a10dfdd42c1d23163b20f784c93ab0c0dd0daa`), same scratch clone at `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93`, same `--jobs 8`, `--seed 49c1`, flattened honest override, and mutation manifest. Each had its own external `--work` directory and stdout/stderr receipt under the scratch root; the counter exit was appended as `EXIT=<n>`.

```
export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C1Rerun
D="$TMPDIR/lane"
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1ExecCounter/candidate.py --lane "$D" --work "$TMPDIR/work/base" --jobs 8 --honest "$TMPDIR/honest_override" --fence "$D/plans/fixture_fence.py" --mutants /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1MutBattery.c1-mutants.json --seed 49c1
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1ExecCounter/candidate.py --lane "$D" --work "$TMPDIR/work/fence_a" --jobs 8 --honest "$TMPDIR/honest_override" --fence /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1ExecFenceA/fence_a.py --mutants /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1MutBattery.c1-mutants.json --seed 49c1
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1ExecCounter/candidate.py --lane "$D" --work "$TMPDIR/work/fence_b" --jobs 8 --honest "$TMPDIR/honest_override" --fence /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1ExecFenceB/fence_b.py --mutants /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1MutBattery.c1-mutants.json --seed 49c1
```

Observed summary fields (verbatim; identical common lines are shown for each run):

```
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
TREE clean
PINS total=66 mismatched=0
LITERALS refusals=20 sealed=12 honest=104 mutants=23
MODULES refusal total=20
MODULES sealed total=12
MODULES honest total=42
REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0
SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
HONEST-POP battery=104 novel=20 expected_novel=0 novel_modules=20
CALIBRATION advertised=32 contradicted=0
MUTANTS total=23 caught=0 floor=23/2 verdict=unmet
REASON honest-fixtures=124!=104,honest-not-admitted,mutants-caught=0<23/2,mutants-broken=23,mutants-declared=23
PREDICATE R49-C1 fail
EXIT=1
```

Per-fence fields:

| Fence | `FENCE source` digest | `HONEST fixtures/admitted/refused/read/hung/build_errors` | `BENIGN total` | `PREDICATE` / exit |
|---|---|---|---:|---|
| frozen base | `.../lane/plans/fixture_fence.py` `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` | `124 / 113 / 11 / 0 / 0 / 0` | 113 | `PREDICATE R49-C1 fail`, 1 |
| variant A | `.../R49C1ExecFenceA/fence_a.py` `b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52` | `124 / 121 / 3 / 0 / 0 / 0` | 121 | `PREDICATE R49-C1 fail`, 1 |
| variant B | `.../R49C1ExecFenceB/fence_b.py` `c89bc524ea5d751fd7ca6f22fe13b732c0231b7b789d43ea5b507e430571f116` | `124 / 122 / 2 / 0 / 0 / 0` | 122 | `PREDICATE R49-C1 fail`, 1 |

Additional observed run fields: all runs printed `COPY-CHECK skipped (refusals dir overridden for testing)`, `BENIGN-MODULES refusals=0 sealed=0 honest=<same BENIGN total>`, and `FENCE-RUN` rows had `touches=0`. Base honest refusals: `n03_detached_head`, `n07_reflog_gc`, `n12_local_config_user`, `n13_remote_origin`, `n14_stash_entry`, `n15_commit_graph`, `n16_notes_ref` (8 r48 classes) plus `n17_replace_ref`, `n18_shallow_fetch`, `n20_linked_worktree`. Variant A refused `n17_replace_ref`, `n18_shallow_fetch`, `n20_linked_worktree`; variant B refused `n18_shallow_fetch`, `n20_linked_worktree`.

The 23 mutants each printed `MUTANT <id> broken unreadable FileNotFoundError`; collectively the counter emitted `MUTANTS total=23 caught=0 floor=23/2 verdict=unmet` and `MUTANT-ISSUE <id>:unreadable FileNotFoundError` for every id `c1-mut-01-gitdir-file` through `c1-mut-23-gitdir-repo-reorder`. The submitted manifest stores each unified diff inline in `payload` and names `target_payload_path`; the candidate's `mutant_bytes()` treats `payload` as a path to a full mutated fence module. None of those paths exists in the frozen clone, so the mutation leg cannot execute. This is a concrete counter/manifest interface mismatch; do not interpret `caught=0` as behavioral mutation sensitivity.

## Limits and verdict

- Stage 2 has not frozen the added populations/literals. `PINS total=66 mismatched=0` is only the base counter pin set under explicit overrides; it does not validate the uncommitted 20-module override, does not include held-out `sealed49`, and is not a stage-2 pin receipt.
- The direct results are informative candidate reruns only, not a valid claim verdict. The default counter literals expect 104 honest fixtures and zero novel modules, while the supplied override contains 20 extra modules; its nested honest tree had to be flattened due the candidate's top-level-only glob.
- The submitted mutant JSON's inline-diff payload schema is incompatible with the candidate's path-to-full-module loader (23/23 unreadable); its floor leg is therefore not measured.
- No external sources were opened; all sources were local. Access date: 2026-10-28. Local source URLs and located quotes (each ≤25 words):
  - `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-49-claims.md` — “the counter applies each mutant to a copy of the landed fence and re-measures the three legs on that copy”.
  - `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-48-verifier-spotcheck.md` — “Any future C1 admission attempt needs the mutation floor committed with receipts.”
  - `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1ExecCounter/candidate.py` — `payload is a full mutated copy of the landed fence`.
  - `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1MutBattery.c1-mutants.json` — `payload_format`: “inline unified diff payload; apply with git apply to the candidate fence”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1ExecFenceA.md` — “variant A re-applied at the round-49 freeze with NO DRIFT” (accessed 2026-10-28).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C1ExecFenceB.md` — “fence repair variant B measured pass on the three frozen behavioural legs” (accessed 2026-10-28).
- Fence candidate files `R49C1ExecFenceA/fence_a.py` and `R49C1ExecFenceB/fence_b.py` were hashed with `sha256sum` but not opened for source text; no content quotes apply.

VERDICT: Independent reruns completed on the exact committed base and both submitted fence variants, revision `9d2900af41e4d1fc6022eff99010436fde6dbd93`. All three printed `PREDICATE R49-C1 fail` and exited 1 under explicit pre-stage-2 overrides; the base, A, and B admitted respectively 113/124, 121/124, and 122/124 honest fixtures. All three had clean 20/20 refusal and 12/12 sealed legs but the 23-mutant leg was entirely broken by the inline-diff/path schema mismatch. No R49-C1 or R49-C2 admission is claimed.
