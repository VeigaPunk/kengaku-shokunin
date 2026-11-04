# DefectGateReverify — R71-C2

Axes: coverage (both revisions, append-only changes, selftest and mutants); calibration (exact output versus frozen prose).

## Findings by severity

### P2 — E2a passes without the frozen verbatim quotation

`plans/round-71-claims.md:92-94` requires “quoting the superseded sentence verbatim”; `:108` requires keeping that sentence verbatim. The original is at `corpus/knowledge/tb2-nginx-request-logging-offline.md:14-15`:

> The instruction at the same pin states the same bodies, the rate-limit zone location and the log path (`instruction.md:6-11`).

The appended erratum at `:92-95` instead says:

> The round-69 sentence above that cites `instruction.md:6-11` for the two HTTP bodies is superseded: the instruction `states the same bodies` at `instruction.md:15-18`, and the full range is `instruction.md:6-11,15-18` (the `source:` anchor already carries that range). Original sentence kept as written (append-only).

It identifies and corrects the citation, but does not quote the original sentence verbatim. Gate `plans/round71_c2_routed_defects.py:169` defines only `SUPERSEDED_SENTENCE = "states the same bodies"`; `:176-188` checks that fragment anywhere in the file and anywhere after its first Errata heading. Therefore the observed `E2a ok` does not establish the frozen verbatim condition. The same fragment remaining in the erratum also means original-only removal would not trip these membership checks [INFERENCE from canonical code; no additional mutation run]. Selftest `:318` globally replaces both occurrences, not just the original, so its green append-only arm does not address this gap. Recommendation: do not treat the printed pass as proof of the complete frozen D2 fix shape. No predicate, case, vector, digest, kill rule or target was edited.

### P3 — Literal base command cannot run: gate absent at the base revision

Pinned clone is `/fast/scratch/hyaku/kengaku-r71/base.NFi4`, revision `1cb49cac52999475de35f8955d5c01f2ddb66ccf`. The requested `python3 $D/plans/round71_c2_routed_defects.py --lane $D` exited 2:

> python3: can't open file '/fast/scratch/hyaku/kengaku-r71/base.NFi4/plans/round71_c2_routed_defects.py': [Errno 2] No such file or directory

Fallback ran the unchanged current-lane gate against base data using `--lane $D`; this reproduced all six defects and rc 1. This is a red-data re-derivation with the current instrument, not execution of an instrument committed at base.

## Commands and results

Read frozen claims in full before any shell command. Godspeed axes named above. LSP device lookup returned `No such tool: xd://lsp`; semantic references/definition/diagnostics unavailable. Used direct canonical source and literal search, not semantic-proof claims.

- `mkdir -p /fast/scratch/hyaku/kengaku-r71/DefectGateReverify-2` succeeded (initial directory inspection also succeeded).
- `git clone --shared --quiet /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r71/base.NFi4` and `git -C .../base.NFi4 checkout --detach 1cb49cac52999475de35f8955d5c01f2ddb66ccf`: rc 0. `git -C .../base.NFi4 rev-parse HEAD`: exact pinned hash. Procedural deviation: clone-root assertion was not made before detached checkout; no commit or lane git mutation occurred.
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master`: rc 0, `d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0` (observed branch tip; gate reads working-tree bytes).
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff -U0 1cb49cac -- corpus/knowledge/tb2-nginx-request-logging-offline.md corpus/lessons/round-70.md corpus/README.md LOG.md`: rc 0. Nginx adds seven lines after old line 88; lesson adds eight after old line 61; LOG adds eight after old line 2648. Those three files have additions only, no removed data lines. README old/new visible at line 565 (eight, six listed classes → eight with all eight classes) and line 799 (six → eight with all eight classes). The original citation sentence is preserved.

All gate commands below used `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round71_c2_routed_defects.py` and subprocess-captured actual return codes. No C1 battery or port listener was run.

### tip

Command: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round71_c2_routed_defects.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin`

rc 0

```text
E1a ok
E1b ok
E1c ok
E2a ok
DEFECTS n=0
PREDICATE R71-C2 pass
```

### base-current-gate

Command: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round71_c2_routed_defects.py --lane /fast/scratch/hyaku/kengaku-r71/base.NFi4`

rc 1

```text
E1a ok
DEFECT E1b no-R70-D1-correction-entry
DEFECT E1c index-row:missing=self-unreadable receipt,argument-order,speedy claim about isolation,dead check clause,unre-derived landing prose
DEFECT E1c support-block:count=6
DEFECT E1c support-block:missing=staged-digest blind spot,self-unreadable receipt,argument-order,exception-red,speedy claim about isolation,freeze-doc overclaim,dead check clause,unre-derived landing prose
DEFECT E2a no-E-D2
DEFECT E2a erratum-does-not-quote-superseded-sentence
DEFECTS n=6
PREDICATE R71-C2 fail
```

### selftest

Command: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round71_c2_routed_defects.py --selftest --work /fast/scratch/hyaku/kengaku-r71/DefectGateReverify-2/st`

rc 0

```text
E1a ok
E1a ok
E1b ok
E1c ok
E2a ok
E1a ok
E1a ok
E1b ok
E1c ok
DEFECTS-RED n=14 codes=E1a,E1b,E1c,E2a want=E1a,E1b,E1c,E2a
SELFTEST defects-in-fake=4 want=4 all-fail=True append-only-arm=True ok=True
```

### mutants

Command: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round71_c2_routed_defects.py --mutants --work /fast/scratch/hyaku/kengaku-r71/DefectGateReverify-2/mu`

rc 0

```text
MUTANT E1a defect_absent=True killed=True rc=1
MUTANT E1b defect_absent=True killed=True rc=1
MUTANT E1c defect_absent=True killed=True rc=1
MUTANT E2a defect_absent=True killed=True rc=1
MUTANTS total=4 killed=4 survived=0
```

## Residual risk and verification gaps

- Exact expected base/tip, SELFTEST and MUTANTS output lines reproduced with the base-instrument substitution disclosed above. Repeated base/tip runs were needed because an initial shell sequence stopped at the expected base rc 1 before reaching selftest/mutants.
- Mutants report `killed=True` when the corresponding diagnostic disappears (`plans/round71_c2_routed_defects.py:343-344`); all four mutant processes still exited 1. This is the implemented diagnostic-deletion metric, not evidence that each mutant accepted the red lane.
- Current gate reads disk with `Path.read_text`, not git objects; branch hash labels observation, not an assertion of a clean immutable run.
- No code or rule changes; only this requested report. No tool installs/updates. Scratch clone and fixture directories removed after report creation.
- Self-evaluation: accuracy 4/5 (working-tree provenance limitation explicit); completeness 4/5 (literal base gate absent, fallback disclosed); clarity 4/5 (long exact receipts retained); actionability 4/5 (specific frozen quote gap identified, no unauthorized repair); conciseness 4/5 (full output required). Overall 4.0/5; user can distinguish reproduced outputs from unmet prose.

Verdict: expected gate outputs REPRODUCED, append-only diffs CONFIRMED; R71-C2 full frozen D2 verbatim-quotation condition NOT ESTABLISHED (current erratum omits the sentence). Recommendation only; no admission or judgment performed.
