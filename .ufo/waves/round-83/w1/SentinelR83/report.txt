# SentinelR83 — bounded safety and evidence-boundary review

Axes: coverage and calibration. Scope: replay sandbox, receipt execution, paths, historical immutability, revision isolation, cleanup. No production remediation or production verdict.

## Evidence and limits

Read RULES.md and the complete frozen claims. BASE and freeze subject were read with `git -C <absolute lane> show <rev>:<subject>`; both are 935 bytes, SHA256 b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a. No git mutation, clone, fleet write, host /app write, package installation, service action, build, lint, or general tests were performed.

All four assigned draft paths were absent at capture: ReplayR83/round83_code_image_probe.py, CounterR83/round83_c1_replay.py, DebtR83/round83_c2_debt.py and DebtR83/round83_c2_checks.py. Thus the findings below distinguish observed prior-pattern defects from conditional R83 threats. They do not certify unseen R83 code. No waiting/polling was used.

Retained receipts: `.ufo/waves/round-83/w1/SentinelR83/capture.txt` and the harmless capture driver `boundary_capture.py`. Python ran with -B and TMPDIR explicitly set to the seat scratch. The driver used a mocked subprocess only for argv capture and a real fixed harmless bubblewrap harness, NOT the R83 grader or counter. It invoked no receipt COMMAND and no offensive payload.

## Findings

### S1 — High if inherited: historical evidence can trigger current-tree host code

Exploit path: a caller requests --rev; a Tree reads historical receipt/tool bytes, but replay launches a relative tool from tree.root in the live lane. A changed current instrument can then execute outside bubblewrap before any grader sandbox, while the reader appears historical. A self-consistent receipt digest is integrity evidence, not independent authorization to execute arbitrary code.

Evidence: plans/round80_c1_located_replay.py:153-165 constructs revision readers but retains the live lane root; :190-194 runs spec tool with cwd=tree.root; :664 reads the table from the current lane even in revision mode. The harmless intercepted run captured argv [/usr/bin/python3, plans/fixture_probe.py], cwd=/home/vgpnk/Projects/shokunin/kengaku-shokunin, despite a historical-labelled Tree. This capture launched no process. These are prior-pattern findings, NOT a reproduced defect in absent R83 drafts.

Impact: mixed-tree evidence; possible arbitrary host execution if historical or mutable instrument bytes are treated as trusted solely because a receipt names their hash.

Smallest remediation: reconstruct fixed replay argv from the reviewed R83 contract; read ledger, receipt, subject, table and tool consistently from the measured tree; materialize required measured bytes only in a fresh private --work child and launch there. Reject path/digest defects before invoking a runner. Do not execute a receipt's COMMAND string. No new validation architecture is requested.

### S2 — Medium if inherited: substring COMMAND checks do not satisfy exact replay provenance

Exploit path: an unrelated command containing the expected tool string passes a substring check; a receipt can falsely attribute execution. Executing that receipt string with a shell would additionally turn evidence into instructions, but no such execution was observed.

Evidence: prior replay :281-282 checks only `spec["tool"] in COMMAND`; :190-194 actually constructs a separate argv list, which is safer than executing COMMAND. Frozen R83 claims require exact reconstructed argv modulo work path.

Impact: fabricated provenance can look located even when the cited command did not run the probe. No claim of demonstrated R83 shell injection.

Smallest remediation: compare tokenized COMMAND to the canonical argv, normalize only the designated work argument, and keep the stored string inert. Reject prefixes/suffixes, extra options, duplicate stamps or embedded newlines that change interpretation. Retain actual stdout/exit receipts rather than a header-only check.

### S3 — Medium conditional: unbounded path joining or cleanup can escape scratch

Exploit path: an absolute or ../ component from a receipt, table, archive member, or caller work path escapes the intended root; symlinked directories redirect staging or deletion. Merely using `Path(root) / value` is not confinement.

Evidence: harmless path arithmetic recorded ROOT / '/app/output.txt' = /app/output.txt and ROOT / '../outside' resolving outside the seat. Prior replay :137-140 follows joined paths; :182-187 derives output paths from member names. Prior sandbox :134 uses mkdtemp beneath its explicit root and :150-151 removes that fresh child, a better cleanup boundary. The R83 member/case names are frozen constants, so keeping those constants removes attacker control; no traversal against a real target was attempted.

Impact: arbitrary host output overwrite or cleanup outside scratch if untrusted names or an unguarded work directory reach these operations.

Smallest remediation: retain canonical subject/table/tool paths and frozen case IDs; reject absolute/parent-traversing record paths; resolve and check containment before reading/materializing. Create a unique scratch child and delete only that owned child in finally; never rmtree a caller-supplied --work root or lane. Do not introduce host /app as a staging directory.

### S4 — Informational confirmed: existing sandbox pattern supports private /app, but is not a proof of R83 safety

Evidence: harmless real sandbox returned rc=0, cwd=/app, read sentinel-sandbox-only from the scratch-backed /app/output.txt, and reported host_home_visible=False and sentinel_env=None. It used the prior round81 sandbox_argv builder (:119-129): /usr and /etc read-only, private net/pid/ipc, private /tmp, explicit scratch /app bind, capture/harness read-only, --die-with-parent, --new-session. Prior run_case :141-144 supplies a minimal environment and timeout; :150-151 cleans in finally. None of this demands host /app writes or fleet git writes.

Residual boundary: /etc is readable (read-only does not mean secret-free); the fixed captured grader is trusted only after its frozen digest is checked, and the host-side Python instrument executes before bubblewrap. The smoke did not test all namespace escape, timeout, descendant, mount or race behaviors. The absent sentinel_env is not a claim that host secrets were enumerated or inspected.

Smallest remediation: preserve the minimal environment, fixed capture SHA, fixed inner argv, timeout, parent-death behavior and scratch-only staging; expose no home/fleet mount and no broader writable bind. Test the R83 implementation's actual exception and cleanup paths when available, without treating this prior-pattern smoke as its grader receipt.

### S5 — Low evidence-quality issue: pre-data controls are not counter rejection receipts

Evidence: plans/round83_freeze_controls.py:12-14 and :20-21 print target_reached=False literally; no C1/C2 counter is invoked. Its docstring explicitly says pre-data anti-vacuity and no production verdict, so this is not presently a fabricated production result.

Impact: using that output as the frozen contract's actual losing-control evidence would overstate calibration. It counts/predicts rather than proving final counters reject actual corrupted fixtures.

Smallest remediation: retain it as a freeze-only receipt and keep it labelled that way. Final controls must actually invoke the integrated counter against do-nothing, ledger-only, fabricated-observation and presence-only fixtures and retain their observed stdout/exit, as the existing frozen contract already requires.

## Historical and rejection boundaries

C2 must append supersede rows and new correction prose, preserving historical SOURCES cells, filed round82 report/LOG/SCORECARD/lesson and prior gates. BASE/freeze equality was observed only for the C1 subject; no blanket historical immutability claim is made. --rev must not materialize or overwrite historical evidence in the checkout. V2/V4 git operations can remain read-only `git -C <absolute lane>` historical queries; any fixture writes belong only in verified private scratch. No examined instruction required host /app writes or fleet git mutations.

resume_continuity_v1 is not on this assignment's replay/record surface and no such entry point was observed; zero-mutation rejection behavior for it was not exercised or claimed. For the reviewed surface, fail-before-execution is the smallest relevant ordering requirement, not a new continuity subsystem.

## Handoff and self-evaluation

No changes proposed for direct installation; L1 owns integration. Recommended assigned checks: inspect integrated R83 code for S1-S3, run its frozen controls/selftests, and retain real --rev isolation and cleanup receipts. This review does not judge, ship or change predicates.

Self-evaluation: accuracy 4/5 (prior-pattern and conditional claims explicitly separated; R83 drafts unavailable); completeness 4/5 (all assigned boundaries covered, actual draft implementation unavailable); clarity 4/5 (five severity-labelled findings, with conditionality requiring careful reading); actionability 4/5 (small localized remedies, not patches to unseen files); conciseness 4/5 (receipts and limitations add length). Overall 4.0/5. Highest-impact improvement is applying S1-S3 to the integrated draft, not claiming this source review validates it. Would the user agree: likely, given explicit absence handling.

Install/update ledger: none. Scratch is removed before terminal handoff; retained capture resides only in the exclusive output directory.

Report: .ufo/waves/round-83/w1/SentinelR83.md
