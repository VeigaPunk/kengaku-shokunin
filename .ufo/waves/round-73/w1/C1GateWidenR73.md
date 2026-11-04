# C1GateWidenR73

Axes: coverage, calibration. Scoped verification complete; no implementation edits.

Evidence: `corpus/evidence/round73/w1/c1-widen-verify.txt` (independent transcripts, explicit rc values, complete path-to-advertising-files attribution).

## Results

- **(a) refuted for the originally frozen gate.** The lane changed during execution. The initial run reported `ADVERTISED total=113`, `MISSING 8`, both predicates fail, rc 1. After rows landed, the live amended gate reported `UNIVERSE mode=full files=133 plans_seen=82 plans_only=0`, `ADVERTISED total=113`, `REGISTERED total=113 rows=115`, all five defect counts zero, both predicates pass, rc 0. Running the independently extracted **freeze-version gate** (`git show 255c261d:plans/round52_c2_registry.py`) on that same row-complete lane instead printed `PREDICATE R73-C1 fail`, rc 1, despite `MISSING 0`.
- **(b) refuted at the row-complete tree; confirmed before rows landed.** Legacy initially reproduced `ADVERTISED total=110 / MISSING 5`, rc 1. After registration, both live and frozen legacy runs print `ADVERTISED total=113 / MISSING 0`, rc 1. The control is tree-dependent, not invariant under registration. Both gate versions' selftests independently printed `SELFTEST cases=4 failures=0`, rc 0.
- **(c) confirmed.** Scratch fixture had exactly an empty registry, existing `plans/tool_z.py`, and its sole advertisement in `plans/round-99-plan.md`. Frozen full: `ADVERTISED total=1`, `MISSING 1`, `MISSING plans/tool_z.py`, rc 1. Frozen legacy: `ADVERTISED total=0`, `MISSING 0`, rc 1 (R73 requires full mode). Both complete transcripts retained.
- **(d) confirmed.** Independent enumeration found `files=133 advertised=113 plans_seen=82 plans_only=0`, matching the live gate. Receipt lists all 113 paths and every advertising filename. No attribution/count disagreement.

## Decisive findings

1. Original exact target **112 differs from observed 113**; 113 nevertheless satisfies the original frozen sentence's `>=111` bound.
2. Registration in SKILL.md itself advertises each registered entry. Consequently `MISSING 0` forces `plans_only=0`; the original `plans_only>=1` arm cannot pass on a complete registry. The landing changed that executable predicate to `plans_seen>=1`. Amendment A1 documents this change but does not make the original frozen instrument pass. This seat did not edit either rule.
3. A1 says no seat had returned before amendment; this seat had already obtained its initial full/legacy/selftest observations. The tool transcript proves observation preceded this seat's discovery of the changed predicate. This does not establish when other seats scored or returned.
4. The L1 after-receipt read during research labels its run `02:48:04Z`, while A1 labels its append `02:54Z`. Those stored labels alone do not establish when code changed; this seat's independently retained reruns avoid relying on that receipt.

## Reproduction of independent attribution

The retained D table was generated independently (no gate import for this derivation) by enumerating the four fixed self-assessment files, `corpus/knowledge/*.md`, and `plans/*.md`; scanning the documented `python3` path grammar; retaining existing script paths; and grouping source filenames per script. A path is plans-only iff every advertising filename is directly under `plans/` and ends `.md`. The receipt records each resulting group, not just a tally.

## Execution and scope

Commands and rc values for the scoring matrix are retained in the receipt. Additional exploratory commands read git history, source, claims amendments, registry content, and dispatch metadata; no build, lint, formatter, commit, checkout, push, installation, or delegation was performed. No supported LSP interface was available; this was source/text inspection, not a symbol refactor.

Own scratch was removed in Python `finally: shutil.rmtree(S)` after receipt persistence. Retained selftest reruns set `TMPDIR` to own scratch; the initial selftest used the gate's default temporary-directory context (which removes its directory on exit). No tools installed.

Scope caveat: an exploratory `importlib` import of the lane gate was used before the independent derivation. Python may have generated an ignored `plans/__pycache__` file outside assigned write scope; this was not checked or removed because unrelated/shared files must not be deleted. The retained independent derivation and final matrix do not import the lane script.

## Risks and handoff

The L1 must distinguish original frozen-rule scoring from Amendment A1 scoring; do not label the amended pass proof of the original predicate. Name the landing revision in the integration report. Further verification remains the L1's responsibility; no additional checks are requested merely to reconfirm these observed failures.

Deliverables changed: this advisory report and `corpus/evidence/round73/w1/c1-widen-verify.txt`. No blocker prevents delivery.

## Self-evaluation

Accuracy 4/5: direct frozen/live transcripts distinguish the two predicates; concurrent lane edits prevent one immutable tree attribution for the entire session. Completeness 4/5: all four arms and every advertising source are retained; exploratory outputs are summarized rather than all copied. Clarity 4/5: original versus amended behavior is separated, though the report is necessarily longer than a single verdict. Actionability 4/5: integration must choose honest original/amended labeling; no rule edit offered. Conciseness 3/5: early exploration and narration were excessive; this report consolidates the decisive evidence. Overall 3.8/5. Improvements: preserve frozen versus amended scoring labels, retain per-command provenance, reduce exploratory narration. Self-check: the user should agree the measured refutations are findings, not unfinished work.
