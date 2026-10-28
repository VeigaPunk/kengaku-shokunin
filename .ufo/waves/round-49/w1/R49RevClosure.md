# R49RevClosure — closure-prep adversarial review (C1 + C2)

## Axes

- **Calibration (R49-C1):** whether the repaired fence admits the frozen honest population, refuses all frozen hostile modules without outside access, and survives the committed mutation floor.
- **Coverage (R49-C2):** whether the amended package/counter has satisfiable tag coverage, sound preconditions and mutants, and provable stage-2 → stage-3 receipt ordering.

## Freeze gate and measured revision

Before any scored counter/probe execution: none was performed by this seat. The committed lane tree contains the stage-1 freeze:

```text
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show -s --format='%H%n%ci%n%an%n%s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93
2026-10-28 09:14:40 -0300
kengaku-shokunin
round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering)
```

The lane HEAD observed was `af88aab193e6034cb9b386472064e3c18fa90128`; its only committed descendant of stage 1 is the w1 spec/dispatch commit. `git diff 9d2900af… HEAD -- plans/round-49-claims.md` was empty. A `git clone --shared` was checked out at the frozen base; `git -C /fast/scratch/hyaku/kengaku-r49/R49RevClosure/lane rev-parse --show-toplevel` returned that exact directory and `rev-parse HEAD` returned `9d2900af41e4d1fc6022eff99010436fde6dbd93`. Thus the freeze exists in the committed tree and predates this review; stage-2/3 artifacts are not present in that measured revision.

Commands run included:

```text
mkdir -p /fast/scratch/hyaku/kengaku-r49/R49RevClosure
export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49RevClosure
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show -s --format='%H%n%ci%n%an%n%s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --format='%h %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93..HEAD
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD -- plans/round-49-claims.md
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r49/R49RevClosure/lane
git -C /fast/scratch/hyaku/kengaku-r49/R49RevClosure/lane checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C /fast/scratch/hyaku/kengaku-r49/R49RevClosure/lane rev-parse --show-toplevel
git -C /fast/scratch/hyaku/kengaku-r49/R49RevClosure/lane rev-parse HEAD
```

Observed: `cat-file -t` → `commit`; lane HEAD `af88aab…`; no post-freeze claims diff; clone top-level and HEAD match the frozen path/hash. No scoring command was run. All source references below were read from the committed lane tree at `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93` unless stated otherwise. Local source access date: 2026-10-28. No external URL was opened; the C2 source URL already recorded by the lane is `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py`, accessed 2026-10-28 in `R49C2SourceReopen.md`; located quote (8 words): `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]`.

## Strongest non-author rejection case — R49-C1 (calibration)

**Rejection case:** do not admit C1 on the strength of the scratch fence candidate. The stage-1 predicate is conjunctive: exact pins, 20/20 refusals, all `<S>` sealed modules clean, every `<H>` honest fixture admitted with zero reads/hangs/build errors, and `<M> >= 12` mutants with at least half caught, with the required calibration and predicate lines on the landing tip. Any one failing component kills the claim (`plans/round-49-claims.md:73-92`). The best positive evidence now is not landing evidence: `R49C1ExecFenceA.md` reports a scratch development harness on 120 honest fixtures (not the wave-1 additions), 20 refusals and 12 sealed modules; it explicitly says no predicate and no mutation floor was measured. It therefore does not establish the frozen `<H>`, `<S>` or `<M>` result.

A concrete counter-integrity attack remains unanswered at this stage: the inherited `round46_c1_verify.py` builder accepts a module that emits `BUILT []` without an error, and only counts actual returned fixtures (`round46_c1_verify.py:428-445,536,597-604`). A stage-2 `<H>` inferred from produced rows could silently omit an authored class and still match a claimed count. `R49C1CritPop.md` identifies this exact gap and recommends an authored per-item manifest; no stage-2 counter/population is present in the frozen tree to verify that defense. Also unresolved are `<S>` and `<M>`: `sealed49/` and `mutants49/c1-mutants.json` are absent at stage 1, so the necessary held-out hostile population and per-mutant receipt/floor remain unproven. The mount-boundary clause (`claims.md:85-88`) likewise needs an actual committed case and landing evidence; a scratch 120-case harness is not proof of it.

**Does the landing evidence answer it?** Not yet. The only observed fence candidate result is the non-scored 120/120 dev harness in `R49C1ExecFenceA.md`; it lacks wave-1 honest additions, stage-2 pins, sealed49, and mutants. `R49C1CritBase.md` does give a useful before-control: base fence at `3a548330` returned `HONEST fixtures=120 admitted=112 refused=8`, with `PREDICATE R49-C1 fail` (scratch reconstructed counter, not the stage-2 landing counter). This confirms a do-nothing distinction but cannot substitute for the frozen landing predicate. It does not cure the manifest risk or establish mount behavior.

Further literal check for the eventual counter: the frozen C1 delta requires `BENIGN total=<B>` and `MUTANTS … verdict=met` in the stated order; the imported r46 counter has no `BENIGN` or `MUTANTS` leg and its hostile rollup treats any `ADMIT`/`ERROR` as `LEAKED` (`round46_c1_verify.py:568-585`). Therefore the imported base alone cannot pass the new predicate; the stage-2 implementation must make BENIGN classification, hostile clean rollups, and mutant scoring mutually consistent without changing the frozen kill rule. This is a requirement to verify against the absent landing counter, not an assertion that it already fails.

## Strongest non-author rejection case — R49-C2 (coverage)

**Rejection case:** do not admit C2 unless the stage-2/3 counter proves each frozen V condition, and in particular implements the new order rule rather than merely delegating to `plans/order_check.py`. The committed stage-1 table is known defective: its 18 cases omit violating cases for `both-print` and `toolchain`, and its corresponding requirement-map rows are unparseable. `round-46/integrate/c3-landing.txt` records `V7 DEFECT … tags missing=['both-print', 'toolchain']`; `R49C2RevAdmission.md` independently recomputes the missing tags from probe, dry table, and receipt. The freeze properly requires a stage-2 table amendment, V7 positive checks, V14 mutation floor, V15 preconditions, repaired grade-path execution, and the stage-3 first receipt (`claims.md:108-141`).

There is a concrete V8 attack against relying on the existing helper as the whole proof. `R49C2PreReceipt.md` built a scratch Git history with early full-run evidence outside `.ufo/waves/round-49/claims/`, committed a receipt before the stage-2 amendment, and then ran the unchanged `order_check.py`; observed output was `ORDER scanned commits=0 file_entries=0 distinct_blobs=0`, `ORDER RESULT PASS`, `EXIT=0`. Its receipt-path rename variant also passed. This demonstrates that the helper's claims-directory scan and first-add-by-path do not prove the frozen rule that the receipt's first commit is the stage-3 commit, a strict descendant of stage 2. The new C2 counter must independently enforce that exact ancestry and path-identity requirement (and its before-receipt controls must not themselves commit forbidden `P10` or `CASE … observed=` lines into the scanned claims directory). `R49C2RevAdmission.md` likewise labels strict stage-2 ancestry as a residual for the absent counter.

The proposed V7 table repair is plausible but not yet decisive: `R49C2ExecCases.md` has scratch-only added cases and a passing `--stage-check` (`stagecheck cases=20 failed=0`), but expressly did not run a full probe; the `toolchain` case's gcc 13.2.0 behavior is emulated with `-std=gnu17`, not measured on a gcc 13.2.0 binary. A passing host case tagged `toolchain` is allowed by the frozen wording only if the amended map/leg truly treats it as a supported version-specific violation; stage-2 must demonstrate V7's exact semantics and the final run must provide observed cases. The stage-check cannot answer the execution question, as the R48 report proved the `mode="all"` path can skip seed/recipe despite stage-check passing. The repaired probe report supplies a candidate and stub-grader evidence, not a full receipt.

**Does the landing evidence answer it?** No landing evidence exists yet. `R49C2ExecControls.md` records all three pre-receipt controls failing under a wave-1 candidate and P10 disabled, and the echo control is detected by content legs; this usefully answers the routed P10-control defect for those candidate runs. But the counter is not stage-2 pinned, the actual receipt path is still absent, and those controls do not prove V8's first-commit rule. The explicit freeze requires a fresh first full probe receipt at stage 3, with first-commit exactly stage 3, a descendant of stage 2, and `CASE … observed=` lines. Without a landing counter implementing this and a committed stage-3 receipt plus order evidence, C2 remains unverified/not admitted.

## Residual risk and verification gaps

- The counter/probe implementation and stage-2/3 commits are absent at this review's measured revision; no claim admission can be made here.
- C1 needs an authored identity manifest and checked row-equality so empty-output modules, non-recursive globs, duplicate sources, or rebuilt population pins cannot dilute `<H>`; its mount-boundary clause, sealed49 population, and mutant battery still need committed evidence.
- C2 needs explicit strict stage-2 ancestry + stage-3 first-commit validation; P10-disabled controls must remain clean under the order scan; V7/V14/V15 must be shown on the final pinned counter. The host-predicted toolchain case remains an emulation until the pinned toolchain or a justified direct equivalent is evidenced.
- `lsp` status/device was not exposed in this seat's tool inventory; the text reads above are direct committed-file evidence, not LSP semantic proofs.
- No tool was installed or upgraded. No external source opened by this seat.
- Scratch: one shared clone at `/fast/scratch/hyaku/kengaku-r49/R49RevClosure/lane`; removed before yield. No source, production file, or sibling report was modified.

## VERDICT

**C1: NOT ADMITTED / unverified** — the strongest blocker is the still-unproved authored honest denominator plus absent committed `<S>`/`<M>` results; the 120-fixture scratch candidate and base-control receipt do not answer those kill conditions. **C2: NOT ADMITTED / unverified** — the current frozen table is known to fail V7, and a synthetic pre-receipt/rename history passes `order_check.py` despite violating the stage-2 → stage-3 requirement; the wave-1 controls/candidates do not answer the absent final counter and receipt. These are non-author rejection recommendations, not an admission decision.