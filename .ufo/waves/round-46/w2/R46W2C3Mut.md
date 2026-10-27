# R46W2C3Mut — C3 counter mutation probe

Axis: behavioral mutation coverage. Frozen target revision: `42d5043afac952fcb43bf4798757785dd258cf85`.

## Detector baseline

Command (inside required envelope):
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/envelope.sh "$S/env" python3 "$S/lane/plans/round46_c3_verify.py" --lane "$S/lane" --work "$S"`

Output: envelope reported bwrap with `/home/vgpnk/.local/bin` protected; `local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged`. V1–V6 passed; V7 DEFECT (two unparsed requirement-map rows and missing tags `both-print`, `toolchain`); V8 DEFECT (`order_exit=1`); V9–V12 passed; V13 passed with six filler defects; `checks=13 defects=2`, `PREDICATE C3 fail`, exit 1. Thus the pristine detector fails the frozen predicate. Under the mutation protocol that makes mutation outcomes inconclusive, not kills.

| Leg | Single-edit mutant | Expected detector | Actual outcome |
|---|---|---|---|
| V1–V13 | Not run | Must first have a passing pristine baseline; then compare mutated verdict | Inconclusive: pristine already fails V7 and V8; no mutant classification claimed |

No probe mutant was applied, so no changed bytes required restoration. Clone was pinned to the requested HEAD. Scratch was removed with `scratch_guard.py safe-rm`; tool output reports deletion of `/fast/scratch/hyaku/kengaku-r46/R46W2C3Mut` (713.1 MiB). Baseline output was copied to this report subdirectory before cleanup. A rerun against fixed baseline/source is needed before mutation verdicts can be meaningful.

VERDICT: c3-mutants-killed-0/13