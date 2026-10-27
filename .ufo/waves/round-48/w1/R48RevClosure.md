# R48RevClosure — closure-prep adversarial review

Axes: **calibration (R48-C1)** and **coverage (R48-C2)**. This is a read-only review; no scored counter, probe, or claimed-work execution was run, and this report does not claim either admission.

## Freeze and measured state

I cloned the lane read-only with `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane` into my assigned scratch directory. `git rev-parse --show-toplevel` returned `/fast/scratch/hyaku/kengaku-r48/R48RevClosure/lane`. The requested stage-1 revision `a543d92083557dd9b33ee674e9b99b03411f80af` is present; `git log -1 --format='%H%n%an <%ae>%n%ad%n%s' a543d92083557dd9b33ee674e9b99b03411f80af` returned that full revision, author `kengaku-shokunin <kengaku@shokunin.local>`, `Tue Oct 27 06:53:29 2026 -0300`, and subject `round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims`.

The fetched clone's measured HEAD was `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767` (`round-48: w1 ready handoff marker`). Its only descendants of stage 1 were `453ddfd` (w1 v2 dispatch evidence) and `bf783c1` (w1 ready handoff marker). `git diff a543d920 HEAD -- plans/round-48-claims.md` was empty; the claims file still ends `Freeze amendments / None yet. Stage 2 fills literals and pins only.`

At that measured HEAD, `plans/round48_c1_verify.py` and `plans/round48_c2_verify.py` were absent; no committed `.ufo/waves/round-48/claims/` receipts existed. Therefore the staged literals/pins, frozen stage-2 populations/cases, and before-control receipts were not yet committed. **Stage-2 prerequisite not met: no scored run was attempted.** The absence of a stage-2 commit means this review cannot establish that no uncommitted or scratch execution occurred elsewhere; it establishes only the committed-tree state at the revision above. C2's no-probe-before-stage-2 rule remains an explicit closure gate.

## R48-C1 — calibration

**Strongest non-author rejection case.** The v3 predicate can certify only the finite honest population pinned at stage 2; it does not establish that the fence generally admits ordinary Git repository states beyond those fixtures. The newly authored honest classes are wave-1 products, leaving an overfit risk even with instructions to author against the base description. The held-out hostile set also includes modules authored in the same wave as the repair, so name-hiding and shuffled execution protect runtime identity but do not make their authorship independent. Finally, changing classification so admitted `touches=0` cases become `BENIGN-ADMIT` rather than leaks is defensible against the r46 detector's false label, but it makes completeness of the strace envelope decisive: an unobserved outside access could evade the kill rule. The frozen mutation floor is also unproven; r46 caught only 2/13 fence mutants, while r48 requires at least half of at least 12 fresh mutants caught.

**Does landing evidence answer it?** Not yet. No stage-2 pin/population, C1 counter, control receipt, landed-tip receipt, or mutation receipt is committed at measured HEAD. R46 establishes the motivating defect, not its repair: `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` reports 9/9 novel honest classes refused; `R46W2C1HoArgv.md` reports two admitted held-outs with `touches=0`; `R46W2C1HoPaths.md` reports one admitted newline-name case with `touches=0`. The new frozen contract explicitly requires every frozen honest class admitted and ties hostile kill to observed outside access; that is a useful correction to the old detector semantics, not evidence that the new counter's tracing is complete or that generalization is broad. Landing must show all exact predicate lines on the clean landing tip, the five required C1 controls failing, the committed frozen population/pins, and mutation catch count at or above the frozen floor. Residual risk remains finite-population generalization and same-wave held-out construction even if those checks pass.

## R48-C2 — coverage

**Strongest non-author rejection case.** V7's stage-2 case-table amendment could satisfy a syntactic `violates=` census without demonstrating that the cited committed cases genuinely falsify each requirement in the frozen requirement map. The counter inherits substantial r46 machinery, while r46 itself had V7 and V8 defects and caught 0/13 package mutants; V14 must prove substantive sensitivity, not merely report a mutant count. V15's digest/table preflight is only as complete as its stage-2 input inventory: an omitted dependency can still alter a leg without being caught. The P10-disabled base/filler/echo controls avoid an early probe, but must still fail for the proper substantive reason; in particular the echo receipt must not pass merely because P10 is disabled. `order_check.py` documents its own boundary: commit order cannot prove an execution in scratch whose output was never committed. Thus its committed-history receipt alone cannot rule out every pre-commit probe run. The no-full-probe-before-stage-2 constraint is material, not paperwork.

**Does landing evidence answer it?** Not yet. At measured HEAD there is no r48 C2 counter, stage-2 case-table amendment, order receipt, control receipt, V14/V15 output, or landing-tip predicate receipt. The r46 baseline demonstrates why these are necessary: `.ufo/waves/round-46/integrate/c3-landing.txt` reports `V7 DEFECT` for missing `both-print` and `toolchain` violations, `V8 DEFECT order_exit=1`, `checks=13 defects=2`, `PREDICATE C3 fail`; its order detail identifies `control-c3-echo` with `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`. The committed r46 dry table has seven tags and 18 cases, but `both-print` and `toolchain` lack violating cases. The new contract directly addresses those defects by requiring all tags be violated by committed cases, disabling P10 in pre-receipt controls, adding V14/V15 and freezing `<V>/<N>`. That is design coverage, not landing evidence. Closure needs stage 2 committed before any full probe, receipts with `REV` for the controls and claimed tree, exact `checks=<V> defects=0`/pass at the clean landing tip, all three controls failing, and at least `<N>/2` substantive mutants caught. Even then, the case-to-requirement semantic validity and uncommitted scratch execution remain review limits unless the evidence specifically closes them.

## Exact commands and observed outputs

Commands run in the assigned clone (inspection only):

- `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane` — `Cloning into 'lane'... done.`
- `git rev-parse --show-toplevel` — `/fast/scratch/hyaku/kengaku-r48/R48RevClosure/lane`.
- `git log -1 --format='%H%n%an <%ae>%n%ad%n%s' a543d92083557dd9b33ee674e9b99b03411f80af` — confirmed full freeze revision, author, timestamp and subject quoted above.
- `git log --oneline a543d920..HEAD` — `bf783c1 round-48: w1 ready handoff marker`; `453ddfd round-48: w1 v2 dispatch evidence (64 seats, 41 attack, policy v2 accepted)`.
- `git diff a543d920 HEAD -- plans/round-48-claims.md` — empty.
- `git ls-tree -r --name-only HEAD .ufo/waves/round-48/` — only `build_spec.py`, `w1-dispatch.json`, `w1-spec.json`, `w1-validate.err`, and `w1.ready` (no claims receipts or seat reports).
- Presence checks for `plans/round48_c1_verify.py` and `plans/round48_c2_verify.py` — both `ABSENT`.
- `cat .ufo/waves/round-46/integrate/c3-landing.txt` — includes verbatim `V7 DEFECT ... tags missing=['both-print', 'toolchain']`, `V8 DEFECT order_exit=1`, `checks=13 defects=2`, `PREDICATE C3 fail`; order detail `ORDER HIT .ufo/waves/round-46/claims/control-c3-echo.txt@4fdeebaa546c:15 kind=gate-p10 ...`; `ORDER RESULT FAIL`.
- Read-only listing/counts: `plans/refusals46/` has 20 entries; `plans/sealed46/` has 12; `plans/battery42`, `battery43`, `battery44` contain 5, 7, 10 module files respectively. These counts match the stated 22 modules / 104 fixtures context, not a r48 run.
- The claims file names `corpus/evidence/round46/tb2-polyglot-c-py-dry-cases-freeze.txt`; that exact path was absent. The committed table is `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` (18 cases). This path discrepancy is documentation-level; the table itself contains seven tags and no `violates=both-print` or `violates=toolchain` case, consistent with the recorded r46 V7 defect.
- `sha256sum plans/polyglot_c_py_probe.py` — `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`; the round-46 wave artifact digest cited by claims is `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d`. These refer to installed and source-artifact bytes respectively; the r46 package spec pins the installed digest.

No tool was installed or updated. No counter, probe, gate, build, lint, or test was run for r48.

## Source record

Source references below are local lane files read from the clone at measured revision `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`; accessed 2026-10-27. The claims file itself records no external URL. Quotes are located excerpts, each under 25 words.

- `plans/round-48-claims.md`, sections Freeze shape, C1, C2, Separability, Freeze amendments. Quote: “Stage 2 may fill literals and pins; it may not change a predicate line, a control, or a kill rule” (Freeze shape).
- `corpus/lessons/round-46-verifier-spotcheck.md`, §§ Claim re-checks, Routed defects. Quote: “wave-2 reports count 3 admitted held-outs (2 argv, 1 paths)” (§ Claim re-checks).
- `.ufo/waves/round-46/w2/R46W2C1HoHonest.md`. Quote: “Thus **9/9 were refused**, with no outside touches.”
- `.ufo/waves/round-46/w2/R46W2C1HoArgv.md`. Quote: “The two probes were also counted under SEALED because the same directory was passed to both overrides.”
- `.ufo/waves/round-46/w2/R46W2C1HoPaths.md`. Quote: “the newline filename was admitted.”
- `plans/round46_c1_verify.py`, C1 counter contract. Quote: “a missing, empty, NUL-holed or execve-less log counts as READ, never as zero.”
- `plans/round46_c3_verify.py`, V7/V8/V13 definitions. Quote: “V8 ok order_check.py ... exits 0 and prints ORDER RESULT PASS.”
- `plans/order_check.py`, contract and limits. Quote: “Commit order is not authorship order: it polices what the history proves.”
- `plans/pkg-spec-r46.json`, frozen instrument digests. Quote: `"plans/polyglot_c_py_probe.py": "67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26"`.
- `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`, tag/case table. Quote: `TAG both-print instruction.md:7`.
- `.ufo/waves/round-46/integrate/c3-landing.txt`, round-46 counter and order receipt. Quote: `checks=13 defects=2`.
- `.ufo/waves/round-46/integrate/final-tip.txt`, final C1/C2/C3 outcomes. Quote: `PREDICATE C3 fail`.
- `plans/round46_c1_verify.py`, pinned inputs/baseline C1 contract; `plans/round46_c3_verify.py`, inherited package counter contract; both are baseline context, not r48 result.
- `SCORECARD.md`, historic scorecard and routed plan. Quote: “coverage 7 tied with novelty 7; coverage wins the most-falsifiable-claim tie-break” (round-13 plan text is historical; round-48 frozen claims govern this review).

## Verdict

**VERDICT: C1 and C2 not reviewable for admission yet — stage-2 freeze and scored landing evidence absent at measured HEAD.** The strongest rejection cases are not answered by current landing evidence because no r48 landing receipts exist. C1 has an explicit, coherent changed classification and honest-population design, but finite-population, trace completeness, and same-wave held-out risks remain. C2 directly addresses r46 V7/V8 failures and adds frozen mutation/preflight controls, but their actual execution, ordering, and sensitivity are unproven. This is a closure-prep recommendation only; no claim admission is made.