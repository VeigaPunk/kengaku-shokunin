# C2CritPadding — R52-C2 padding falsification

## Finding

The frozen counter can be satisfied by padding. It checks only that (a) each advertised script path occurs in the registry entry cell, (b) all eight parsed cells are nonempty, (c) the entry path exists, and (d) a self-test cell does not match its narrow exactly-one-script/flag pattern with no matching flag in source. It does not validate any other cell's meaning or truth.

I built a lane copy under `/fast/scratch/hyaku/kengaku-r52/C2CritPadding/` and inserted 28 rows whose seven non-entry cells are all `x`; the entry cell necessarily contains the actual advertised `python3 plans/<name>.py` path so the row can register. With the original `order-check` row retained, the frozen counter reported:

```
ADVERTISED total=72
REGISTERED total=72 rows=74
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 1
  SELFTEST-UNBACKED `order-check`
PREDICATE R52-C2 fail
exit=1
```

The only remaining predicate leg was the already-known `order-check` self-test claim; the 28 padding rows themselves removed all 28 MISSING entries. In a second fixture, changing only that existing cell to `x` (the counter accepts it as non-self-test text) produced the complete after-predicate despite the 28 rows' seven `x` cells:

```
ADVERTISED total=72
REGISTERED total=72 rows=74
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
PREDICATE R52-C2 pass
exit=0
```

Thus the after-state is reachable with truthless registry content plus a syntactic dodge of the existing unbacked-self-test check. This is a counterexample to treating `PREDICATE pass` as evidence that the registry rows are truthful.

An additional variant (`lane-pad2`) included 29 rows (the same 28 plus a duplicate row), an inverted verdict-map claim for `round28_census.py`, and a self-test cell naming two scripts and `--selftest` (neither script accepts that flag). The counter still reported `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 1` (only the retained `order-check`), and failed solely on that existing item. This demonstrates that the ambiguity guard does not check such a cell and the counter does not detect duplicate rows or the false verdict-map cell. With `order-check` changed to `x`, the corresponding pure-padding fixture passes.

## Frozen-counter and source evidence

Read the frozen claims file in full before inspection. Read `plans/round52_c2_registry.py` lines 1–194. Its relevant implementation is:

- `parse_rows()` accepts lines with exactly eight cells, skipping separator rows; it does not inspect cell semantics.
- `collect()` derives `MISSING` from the entry command path only, `INCOMPLETE` from `not all(row)`, and entry existence from the path.
- `selftest_unbacked()` returns false unless it sees exactly one script; therefore the two-script ambiguous cell evades the check.
- `verdict()` passes when the four zero-count lists are empty.

Observed round28 counter line: `plans/round28_census.py:47` is `return 0 if clean else 1`. Running the advertised command `python3 plans/round28_census.py --revision 78e6df8171edf8afbb85e7345aea97f6cb2c7228` on the current lane exited 1. This is also a useful reminder that a pinned-value claim must be tied to a dated tree/tip digest and re-run; a historical SCORECARD receipt is not evidence that the same value holds now.

## Cheapest evidence the L1 can demand per row

A single bundled receipt with one independently verifiable record per row is cheap and blocks the observed padding attack. Minimum record: (1) exact entry invocation and script SHA-256 at the tested tip; (2) exit status plus a short located output line (and stdout digest); (3) verdict-map source quote with file/line range for the actual branch, plus an observed receipt for each verdict arm the row claims; (4) exact self-test flag and its exit/output receipt, or literal `none declared`—never an unqualified `x`; (5) pinned value copied from that same run and the tested tree/tip digest; (6) before/after tree digest or diff for any write-scope claim. A quote alone is not execution evidence, and a run alone cannot establish an unexercised verdict arm.

Per-row cheapest evidence route (receipt must use the exact mode/arguments claimed by the registry row; scratch/work arguments must stay under the seat scratch directory):

| Missing instrument | Cheapest measurable row evidence |
|---|---|
| `adoption_check.py` | Run the recorded `--expect … --census` invocation against its named expectation; capture verdict/count line, exit and tip digest. |
| `attrib_probe.py` | `freeze-check --frozen plans/attrib-r23-frozen.md`; capture pin comparison output and script digest. A `trials --shim` row must instead identify and receipt the shim/trial invocation. |
| `catalog_probe.py` | Offline `--verify --lane .` receipt for the saved capture. A row claiming live freshness/capture must carry a dated live-fetch receipt and fetched-body digests (see limits below). |
| `defect_ledger.py` | `--lane .`; capture defect count and exit plus digest of the ledger input. |
| `gate_flip_check.py` | `--selftest` receipt; if the row claims lesson-specific behavior, also run its exact `--lesson <path>` invocation and cite the refusal/flip line. |
| `parser_policy_compare.py` | `--selftest` receipt plus `--summary` output/count line. |
| `password_recovery_probe.py` | Run the pinned grader probe with its `--work` rooted in scratch; receipt includes captured grader digest and case/result summary. A dry/stage check alone is not evidence for grader behavior. |
| `polyglot_c_py_probe.py` | Same: sandboxed pinned-grader run with `--work` in scratch; receipt includes grader digest and case/result summary. |
| `round28_census.py` | Run exact pinned `--revision`; record current tip/tree digest, census line and exit. Historical exit values must not be carried forward without remeasurement. |
| `round30_defects.py` | `--selftest` receipt and `--lane .` defect-count/exit receipt. |
| `round31_c1_verify.py` | `--selftest` receipt and `--lane .` checks/defects output. |
| `round31_defects.py` | `--selftest` receipt and `--lane .` checks/defects output. |
| `round33_c1_verify.py` | `--selftest` receipt and `--lane .` checks/defects output. |
| `round33_defects.py` | `--selftest` receipt and `--lane .` checks/defects output. |
| `round35_c1_verify.py` | `--lane .` receipt with checks/defects line; include any fleet input digest if the row uses `--fleet`. |
| `round35_hardening.py` | `--lane .` receipt and reported hardening checks; label it post-hoc, not as a frozen claim rule. |
| `round36_c2_verify.py` | `--lane .` receipt with checks/defects output and referenced grader digest. |
| `round45_c1_verify.py` | Run with `--lane .` and `--work` under scratch; receipt the fence/case result and exit. |
| `round45_c2_verify.py` | Run with `--lane .` and `--work` under scratch; receipt checks/defects plus pinned grader digest. |
| `round46_c1_verify.py` | Run with `--lane .` and `--work` under scratch; receipt fence/refusal result and exit. |
| `round46_c2_verify.py` | Run with `--lane .` and `--work` under scratch; receipt checks/defects and the supersession result. |
| `round46_c3_verify.py` | Run with `--lane .` and `--work` under scratch; receipt grader digest and case/result summary. |
| `round50_c1_verify.py` | Run with `--lane .` and `--work` under scratch; receipt geometry/fence result and exit. |
| `round50_c2_audit.py` | `--selftest` plus `--lane .`; receipt its pointer-count/verdict line and exit. |
| `round51_routing.py` | `--selftest` plus the claimed `--run-checks` mode with `--scratch` under seat scratch; receipt rows/checks/verified counts and exit. |
| `round51_surfaces.py` | `--selftest` plus `--lane .`; receipt surface statuses and exit. For HTTP surfaces, preserve the URLs, access time and response/status evidence. |
| `routed_open.py` | `--selftest` plus the exact claimed observation/list mode; receipt item IDs, evidence paths and exit. |
| `tb2_grader_probe.py` | Run the pinned offline probe with its documented `uv` environment; receipt grader SHA-256, case summary and exit. |

I could propose measurable evidence for all 28 rows; none is intrinsically unevidencable. I cannot propose *cheap offline evidence for current external-state behavior* in the live `catalog_probe.py` capture/probe mode or the HTTP-resolution leg of `round51_surfaces.py`: the former calls `urllib.request.urlopen` for live catalogs, and the latter calls `urlopen` for HTTP surfaces. For those specific verdicts, the cheapest honest evidence is a dated network receipt (URL, status, fetched-body digest, command and exit); alternatively the row must explicitly narrow its verdict to the offline verify/self-test mode, which does not substantiate freshness/current availability. `attrib_probe.py` imports `HTTPConnection` and has a `trials --shim` mode; I can propose an offline freeze-check receipt, but not claim that this demonstrates live trial behavior without a trial receipt.

## Exact commands run and measured outcomes

Working directory for lane reads/runs: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; fixture work was under `/fast/scratch/hyaku/kengaku-r52/C2CritPadding`.

1. `mkdir -p /fast/scratch/hyaku/kengaku-r52/C2CritPadding/tmp` — created seat scratch.
2. `wc -l plans/round52_c2_registry.py` — 194 lines.
3. `python3 plans/round52_c2_registry.py --lane .` — baseline: advertised 72; registered 44 (46 rows); missing 28; incomplete 0; entry-missing 0; selftest-unbacked 1 (`order-check`); predicate fail, exit 1.
4. `python3 plans/round52_c2_registry.py --selftest` — `SELFTEST cases=3 failures=0`, exit 0.
5. `du -sh --exclude=.git --exclude=.jj .` — lane was 581M; scratch copy was 587M.
6. `tar -C /home/vgpnk/Projects/shokunin/kengaku-shokunin --exclude=.git --exclude=.jj -cf - . | tar -C /fast/scratch/hyaku/kengaku-r52/C2CritPadding/lane-pad -xf -` — created isolated full lane fixture; copied it to `lane-pad2`.
7. `python3 make_fixture.py` — created the 28-row pure-padding fixture and the second fixture; 28 padded rows in lane-pad, 29 in lane-pad2.
8. `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c2_registry.py --lane lane-pad3` — exact 28 rows plus original `order-check`: MISSING 0, incomplete 0, entry-missing 0, selftest-unbacked 1 (`order-check`), predicate fail, exit 1.
9. Same counter on `lane-pad` — MISSING 0, incomplete 0, entry-missing 0, selftest-unbacked 0, predicate pass, exit 0 (the existing `order-check` selftest cell had also been changed to `x`).
10. Same counter on `lane-pad2` — 29 rows including duplicate; MISSING 0, incomplete 0, entry-missing 0, selftest-unbacked 1 (`order-check`), predicate fail, exit 1.
11. `grep -n -E 'SystemExit|sys\\.exit|return [0-9]|exit\\(' plans/round28_census.py` — found line 47 `return 0 if clean else 1` and line 51 `raise SystemExit(main())`.
12. `python3 plans/round28_census.py --revision 78e6df8171edf8afbb85e7345aea97f6cb2c7228` — exit 1 on the current tree.
13. Profiled all 28 source scripts for argparse flags, `--selftest` presence, docstring and network markers; 12 expose `--selftest`. `attrib_probe.py`, `catalog_probe.py`, and `round51_surfaces.py` matched network/API indicators; source inspection confirmed `catalog_probe.py` calls `urllib.request.urlopen` and `round51_surfaces.py` calls it for HTTP surfaces.

## Scratch artifacts produced

All artifacts are under `/fast/scratch/hyaku/kengaku-r52/C2CritPadding/` and are removed before handoff: `make_fixture.py`, `restore_order.py`, `trim_duplicate.py`, and lane copies `lane-pad`, `lane-pad2`, `lane-pad3`.

No tools were installed or updated.
