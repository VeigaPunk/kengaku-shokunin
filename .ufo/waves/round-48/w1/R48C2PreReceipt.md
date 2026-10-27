# R48C2PreReceipt — Q30 pre-receipt ordering review

**Axes:** coverage (R48-C2). **Revision measured:** `REV a543d92083557dd9b33ee674e9b99b03411f80af` (stage-1 frozen base). Read-only reconstruction; no scored counter or full probe run. The only probe invocation was `--dry` stage-check.

## Result

The round-46 V8 defect is reproducible from committed evidence: the echo control receipt was committed before the first committed probe receipt and records a P10 mismatch, which means its gate reran the probe. Round 48 freezes the right intended safeguard: controls must omit P10, and `pkg_gate.py` already supports this by skipping P10 when `--rerun` is omitted. However, stage-1 does not itself prevent a seat from invoking the old counter or `pkg_gate.py --rerun`; enforcement depends on the stage-2 counter/control invocation and committed ordering receipts. Thus **a pre-receipt control can still run P10 through the old/direct path**; the frozen intended path should not, if implemented and invoked as frozen.

## Evidence and reconstruction

1. Stage-1 claims freeze is committed at `a543d920` (parent `0f77f9b27931b3c76b3d095fc0fa70edb79556d9`, commit time `2026-10-27T06:53:29-03:00`). Its claims-file blob is `3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5`, identical to the live tree copy; `a543d920` is an ancestor of `master`. The frozen text says: “Pre-receipt controls run the C2 gate with its P10 (fresh probe re-run) leg disabled” (claims §Ordering, Q30) and “the first full probe run follows the stage-2 commit” (C2 delta b). `Freeze amendments` says “None yet.” At the measured base, `git ls-tree -r --name-only a543d920 -- .ufo/waves/round-48/` returned no entries; the round-48 live committed tree likewise had no entries under that path. The live untracked claims directory held only `README.txt` and `freshness-r48.txt`, neither a C2 control receipt.

2. Round-46 ancestry/timing from committed history:
   - `fd4129e` (`2026-10-27T01:44:14-03:00`): round-46 stage-1 claims freeze.
   - `4fdeeba` (`2026-10-27T02:32:46-03:00`): stage-2 amendment, including control receipts; it is an ancestor of `8d7f74ce`.
   - `8d7f74c` (`2026-10-27T02:33:05-03:00`): first recorded probe receipt commit.
   - Committed `.ufo/waves/round-46/claims/control-c3-echo.txt` records `ENVELOPE start 02:32:09` and line 15 `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`. This is a P10 execution before the first recorded receipt. The landing output confirms the detector: `ORDER HIT .ufo/waves/round-46/claims/control-c3-echo.txt@4fdeebaa546c:15 kind=gate-p10 [...]
` (the committed line itself is `ORDER HIT .ufo/waves/round-46/claims/control-c3-echo.txt@4fdeebaa546c:15 kind=gate-p10 `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt``), followed by `ORDER FAIL probe-executed-before-receipt hits=1` and `ORDER RESULT FAIL`. SCORECARD round-46 coverage row records V8 as “control-c3-echo ran the gate's P10 before the receipt.”

3. The committed round-46 counter explains why: `plans/round46_c3_verify.py` `v2()` invokes `pkg_gate.py package ... --rerun --require-clean-tree`; its top comment explicitly says V2 runs the gate with `--rerun` (P10). It has no disable option, only `--lane`, `--work`, `--filler`. `plans/pkg_gate.py` `cmd_package()` filters legs with `(n != "P10" or args.rerun)`; with no `--rerun`, P10 is omitted entirely. Therefore the stage-2 R48 control runner must call the gate without `--rerun` (or equivalently implement a skip) for base/filler/echo controls. A direct old-counter run on a package control or direct `pkg_gate.py ... --rerun` remains technically able to execute P10 before stage 2; Q30 is not an OS/code-level execution barrier.

4. `plans/order_check.py` is detection, not prevention. It scans committed blobs under `.ufo/waves/round-NN/claims/` through the receipt's first-add commit and flags P10 lines except the exact “receipt unreadable” excuse, as well as observed CASE lines. It cannot detect an uncommitted local execution. The R48 frozen wording to pin each control's ordering receipt is important: the inherited probe receipt `corpus/evidence/round46/polyglot-c-py-probe.txt` was first committed at `8d7f74ce`, before the R48 freeze, so using that inherited receipt as the order-check `--receipt` would hit the order check's `receipt-before-claims` condition. Use new control receipt paths committed after the R48 freeze, as frozen, and ensure the control receipt output does not encode a P10 execution. Omit `--rerun`, which emits no P10 line.

## Commands and observed outputs

All Git fixture/history commands were run against clone `$D=/fast/scratch/hyaku/kengaku-r48/R48C2PreReceipt/lane`; verified `git -C "$D" rev-parse --show-toplevel` printed exactly `$D`. Clone was `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane`, checked out at the frozen base. No writes were made to the clone.

Commands run (in addition to the initial required reads):

- `git log --format='%H %cI %s' -5` at `$D` → HEAD `a543d920...`, parent `0f77f9b...`; stage-1 timestamp above.
- `git log --format='%H %cI %an %s' -3` in lane → live HEAD `bf783c1...`; stage-1 plus two later w1 marker commits.
- `git log --reverse --format='%h %cI %s' -- plans/round-46-claims.md` and same for `corpus/evidence/round46/polyglot-c-py-probe.txt` and the three control paths → timestamps listed above.
- `git merge-base --is-ancestor 4fdeebaa 8d7f74ce` → success; `git merge-base --is-ancestor a543d920 master` → success.
- `git diff a543d920 HEAD -- plans/round-48-claims.md` → empty; `git hash-object plans/round-48-claims.md` and `git rev-parse a543d920:plans/round-48-claims.md` both `3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5`.
- `grep -n 'add_argument\|ArgumentParser' plans/round46_c3_verify.py` → only `--lane`, `--work`, `--filler`.
- `grep -n 'rerun\|add_argument' plans/pkg_gate.py` → P10 included only under `args.rerun`; CLI defines `--rerun`.
- `cat .ufo/waves/round-46/integrate/c3-landing.txt` → V7 and V8 DEFECT; ORDER scan reports the echo P10 hit and fail (quoted above).
- `cat .ufo/waves/round-46/claims/control-c3-echo.txt` → line 15 P10 mismatch (quoted above).
- `sha256sum corpus/evidence/round46/polyglot-c-py-probe.txt plans/polyglot_c_py_probe.py` → `dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277` and `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`, matching the committed spec pins.
- `timeout 120 python3 plans/polyglot_c_py_probe.py --lane . --dry` → began with `TAG single-file instruction.md:1`, `TAG python-run instruction.md:3`, `TAG c-build instruction.md:5`, `TAG both-print instruction.md:7`, `TAG fib-kth instruction.md:7`; dry-only, not a scored/full run.
- `git ls-tree -r --name-only HEAD -- .ufo/waves/round-48/claims/` plus committed-blob scan for `P10 (ok|DEFECT)|CASE .* observed=` → no committed claims paths / no hits.

## Limits, axes, correction

No stage-2 amendment or R48 C2 counter/control receipts were committed in the measured base, so I cannot verify the intended control mode exists in the eventual stage-2 counter. No scored run was performed. The R48 order-check scan sees only committed claims-directory blobs; it does not stop or reveal an uncommitted direct probe run. This review makes no admission claim. **Impacted axis: coverage** (the V8 counterexample affects C2 ordering validity).

**Smallest safe correction:** stage-2 `round48_c2_verify.py` must explicitly run every pre-receipt base/filler/echo gate without `--rerun`, with a control receipt showing the skip and the expected non-P10 failure; commit those receipts only after the R48 freeze. Run the frozen `order_check.py` against each newly committed control receipt and require pass. Keep the first P10-enabled/full probe invocation after the stage-2 commit. Do not use the inherited round-46 probe receipt as the order-check receipt for R48, because its first-add commit predates the R48 freeze.

**VERDICT: V8 recurrence remains technically possible via direct/old-counter pre-stage-2 execution; the frozen intended control path avoids it only if stage-2 implements and uses the P10-disabled invocation.**

## Sources opened

Access date for all local sources: **2026-10-27**. URLs are local file URLs at the measured clone or lane path.

- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — §Ordering Q30: “Pre-receipt controls run the C2 gate with its P10 (fresh probe re-run) leg disabled.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` — C3 verdict: “V8 finds the pre-receipt P10 execution (`control-c3-echo`).”
- `file:///fast/scratch/hyaku/kengaku-r48/R48C2PreReceipt/lane/plans/round46_c3_verify.py` — lines 18–20: “This counter's `V2` runs the gate WITH `--rerun` (P10 = a fresh probe run byte-compared).”
- `file:///fast/scratch/hyaku/kengaku-r48/R48C2PreReceipt/lane/plans/pkg_gate.py` — `cmd_package`: “(n != "P10" or args.rerun)”
- `file:///fast/scratch/hyaku/kengaku-r48/R48C2PreReceipt/lane/plans/order_check.py` — lines 192–198: “no claims/ file committed at or before the receipt commit may show the probe executed.”
- `file:///fast/scratch/hyaku/kengaku-r48/R48C2PreReceipt/lane/.ufo/waves/round-46/claims/control-c3-echo.txt` — line 15: “gate: P10 DEFECT fresh probe output is not byte-equal to the receipt”.
- `file:///fast/scratch/hyaku/kengaku-r48/R48C2PreReceipt/lane/.ufo/waves/round-46/integrate/c3-landing.txt` — ORDER tail: “ORDER FAIL probe-executed-before-receipt hits=1”.
- `file:///fast/scratch/hyaku/kengaku-r48/R48C2PreReceipt/lane/SCORECARD.md` — round-46 coverage row: “control-c3-echo ran the gate's P10 before the receipt”.
