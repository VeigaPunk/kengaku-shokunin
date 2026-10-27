# R48C2RevAdmission — C2 coverage review

## Scope and verdict

**Axes named:** coverage (the assigned C2 axis); ordering/pre-registration (the C2 order-proof subcheck, not a separate SCORECARD axis).

**VERDICT: C2 admission is not established from committed bytes at the stage-1 freeze.** The frozen round-46 table has violating cases for only 5/7 tags; `both-print` and `toolchain` have none. The round-48 order proof is not yet adjudicable as a completed proof because stage 2 and its receipts are absent from the committed tree. The round-46 predecessor order failure is, however, directly evidenced in committed receipts. This is an evidence review only: no scored counter or probe was run and no R48-C1/R48-C2 admission is claimed.

## Revision / freeze status

Inspected a read-only `git clone --shared` at `a543d92083557dd9b33ee674e9b99b03411f80af` (`git rev-parse HEAD` printed that exact hash). The claims file exists in that commit and its blob hash is `87e6075ff2c0748be0b087a4d6d6a2dd9b7a0891691fcec70dc6239978768672`. The freeze commit timestamp is `2026-10-27 06:53:29 -0300`; lane history shows later commits `453ddfd` and `bf783c1`, but no stage-2 commit. At the frozen revision `plans/round48_c2_verify.py` is absent. The only live `round-48/claims/` files observed were untracked `README.txt` and `freshness-r48.txt`; they are not committed evidence and were not used to infer a result.

The claims freeze explicitly says Stage 2 comes after wave 1 and before claimed work is scored, and that C2 pre-receipt controls disable P10 (claims lines 22–32). Thus this review did not run any scored command. All measured revision references below are to committed source artifacts at the stage-1 base; the inherited round-46 run receipt identifies its own revision as `e9d201455c3774921aa5dfc287f07b4b9f113e76`.

## Frozen-tag coverage from committed bytes

The committed dry-case table `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` has seven tags: `single-file`, `python-run`, `c-build`, `both-print`, `fib-kth`, `stdout-only`, `toolchain`. Its SHA-256 is `99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536`, matching `DRY_SHA256` in `plans/round46_c3_verify.py`.

Reading each committed `CASE ... violates=` row gives:

| Frozen tag | Committed violating cases | Result |
|---|---|---|
| `single-file` | `nop`, `extra-file`, `leftover-cmain`, `regrade-same-state` | present |
| `python-run` | `c-only` | present |
| `c-build` | `python-only`, `dir-in-place` | present |
| `both-print` | none | **missing** |
| `fib-kth` | `lookup-table`, `wrong-value`, `n-parsed-differently`, `empty-file` | present |
| `stdout-only` | `value-plus-line` | present |
| `toolchain` | none | **missing** |

The committed knowledge entry's Requirement map independently states `both-print` and `toolchain` are “not exercised” and “no frozen case violates it” (lines 77, 83–89). The committed `plans/round46_c3_verify.py` V7 implementation requires a receipt case for each frozen tag and parses the map rows. The committed round-46 landing receipt `.ufo/waves/round-46/integrate/c3-landing.txt` reports:

```
V7 DEFECT rows=5 tags=7 bad=["unparsed row '| instruction.md:7 | both-print | not exercised | '", "unparsed row '| instruction.md:9 | toolchain | not exercised | n'", "tags missing=['both-print', 'toolchain'] duplicated=0"]
```

This is independently consistent with the two absent `violates=` tags. The R48 stage-1 plan acknowledges the required stage-2 table amendment without rewording tags; that amendment is not present at the reviewed revision. The R48 kill rule says any frozen tag without a committed violating case stops C2, so it is not satisfied by the stage-1 bytes.

## Order-proof evidence and limits

The committed round-46 landing receipt records the prior order defect:

```
V8 DEFECT order_exit=1 result=not-PASS
ORDER HIT .ufo/waves/round-46/claims/control-c3-echo.txt@4fdeebaa546c:15 kind=gate-p10 `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`
ORDER FAIL probe-executed-before-receipt hits=1
ORDER RESULT FAIL
```

The committed `plans/pkg_gate.py` makes P10 conditional on `--rerun` (leg filtering at line 308; CLI flag at line 365), so a control invocation without that option disables the fresh probe leg. `plans/order_check.py` is read-only and checks (1) freeze commit does not contain the receipt, (2) receipt does not precede claims, and (3) committed claim-directory blobs through the receipt-add commit contain no executed-P10/observed-case evidence. This supports the frozen design of P10-disabled controls plus order receipts.

**The R48 order proof itself is pending, not passed:** at the inspected stage-1 revision there is no `round48_c2_verify.py`, no committed R48 C2 controls or receipt, and no amended case table. Therefore neither each-control order pin nor the claim that the first full run follows stage 2 can yet be checked from committed R48 bytes. `order_check.py` documents its limit: commit order is not authorship order, so it cannot prove that an uncommitted scratch execution never occurred. This report does not claim such proof.

## Identity discrepancy noted

The claims describe the wave-46 probe artifact as “integrated verbatim” into `plans/polyglot_c_py_probe.py`. The cited artifact hashes to `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d`, while the committed plans copy hashes to `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`; `diff` shows substantive documentation/design differences, and the round-46 counter pins the latter hash (`PROBE_SHA256`, line 121). Thus “verbatim” is not supported. The operational probe identity is the committed/pinned `67a8f4a6…` copy. This discrepancy does not alter the tag-coverage finding but should not be mistaken for a verified artifact identity.

## Commands run and observed outputs

All commands below were read-only except creation/removal of this seat's private scratch clone and the permitted report write. The clone top-level was `/fast/scratch/hyaku/kengaku-r48/R48C2RevAdmission/lane`; no fixture Git writes were made.

- `git cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af` → `commit`.
- `git log --format='%H %ci %s' -1 a543d92083557dd9b33ee674e9b99b03411f80af` → `a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27 06:53:29 -0300 ...`.
- `git rev-parse HEAD` in frozen clone → `a543d92083557dd9b33ee674e9b99b03411f80af`.
- `ls plans/round48_c2_verify.py` → `No such file or directory`.
- `sha256sum corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` → `99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536`.
- `sha256sum corpus/evidence/round46/polyglot-c-py-probe.txt` → `dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277` (also matches `pkg-spec-r46.json`).
- `cat .ufo/waves/round-46/integrate/c3-landing.txt` → the V7/V8 excerpts quoted above; overall `checks=13 defects=2`, `PREDICATE C3 fail`.
- `sha256sum .ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py plans/polyglot_c_py_probe.py` → respectively `22b7779e…` and `67a8f4a6…`; `diff` showed different committed contents.
- `grep -n 'MAP_ROW\|TAG_LINE' plans/round46_c3_verify.py` → `MAP_ROW` requires backticked `instruction.md:<line>` and backticked tag; the two “not exercised” rows lack those marks, explaining the parse defects.
- `grep -n 'rerun\|P10' plans/pkg_gate.py` → P10 conditionally included when `args.rerun`; `--rerun` CLI flag present.
- `grep -n 'dry\|add_argument' plans/polyglot_c_py_probe.py` → `--dry` is “print the frozen case table only (no sandbox)” and `--stage-check` exists.
- A CASE-column comparison command was attempted with mismatched field selections (dry rows and receipt rows use different schemas); it did **not** establish whole-row sequence equality and is not used as evidence here.

## Sources opened (URL, access date, located quote)

The assignment required URL/date/quote for each source opened. The repository files above are local committed sources (no external URL); source URLs below were already embedded in the committed knowledge entry/spotcheck and were not fetched anew by this reviewer:

- `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py` — accessed date recorded in committed spotcheck: 2026-10-27. Located quote in spotcheck, “`test_cases = [(42, "267914296"), (10, "55"), (0, "0")]`”.
- `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/instruction.md` — access date in committed package entry: 2026-10-27. Located quote from its mapped instruction content as recorded by the package: “I'm using python3 3.12.3 and gcc 13.2.0.”

No external source was opened during this review. No tools were installed.

## Limits

This is a committed-byte review of the stage-1 base and inherited round-46 receipts, not a stage-2 evaluation. No full probe, `--dry` probe, counter, or control was executed. Therefore no conclusion is made about any unseen stage-2 case amendment, order receipt, mutation floor, or final C2 admission. Scratch was removed before handoff.
