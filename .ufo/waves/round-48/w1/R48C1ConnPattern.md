Round 48 seat R48C1ConnPattern — C1 counter-boundary comparison

Axes: calibration (assigned); operability/evidence-integrity are discussed only as secondary effects, not claimed.

Evidence and commands:
- Read `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` (full) and `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` first. Claims state the C1 honest set is frozen before scoring; only traced outside access (`touches>0` or READ) classifies as LEAK; touches=0 admissions are BENIGN-ADMIT; kill rule targets traced hostile admission and honest refusal. Round-46 lesson records 3 held-out admissions, 9/9 novel honest refusals, and fence mutants caught 2/13.
- `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r48/R48C1ConnPattern/lane`; asserted `git -C "$D" rev-parse --show-toplevel` equals `$D`; `git -C "$D" checkout --detach a543d92083557dd9b33ee674e9b99b03411f80af`.
- Observed `REV a543d92083557dd9b33ee674e9b99b03411f80af`; committed tree includes `plans/round-48-claims.md`, `grader.py`, and `plans/pkg_gate.py`, but no `plans/round48_c1_verify.py`, no drift-pins-named path, and no stage-2 population/pin/control receipts. No scoring command was run.
- Read `plans/pkg_gate.py` lines 1–15, 90–120, 260–310; read `grader.py` lines 1–22, 80–100. `pkg_gate.py` P10 executes configured `probe_cmd` via subprocess only when `--rerun`; `cmd_package` omits P10 unless requested. It runs clauses with exception-to-defect mapping. `grader.py` documents pinned evidence bytes and mismatch verdicts; round-12 inherited gate checks ordering and preregistration pins, including script hashes before run and request timestamps.

Pattern comparison / bounded move:
The C1 boundary itself is materially stronger than the older package-gate “receipt reproducibility” boundary: it requires an immutable pre-scoring honest/hostile population and observed traced opens/reads as the leak predicate, rather than inferring leak from a final admission. The direct inherited failure mode to guard against is **measurement timing/provenance drift**: a correct predicate can still be invalidated if the counter, input pins, frozen population, or control receipts are introduced after measurement. Lane precedent in `grader.py` lines 17–19 explicitly limits pins to default in-repo grading paths; overridden paths are treated as mutated copies, so a pin can silently stop authenticating the measured tree if the harness accepts an override without a separately bound revision. `pkg_gate.py` P10 is optional and explicitly triggers a fresh probe rerun; hence pre-receipt controls must disable it as the round-48 contract says, and a full P10 must not occur before stage 2. This is consistent with round-48 claims Q30 ordering. No contradictory behavior was observed in the frozen tree because the v3 counter does not yet exist there.

Proposed move: retain the claim's stage-2-before-scoring rule as a hard measurement boundary, and ensure the eventual v3 counter receipt records `REV` for the exact clean landing tree while resolving all population and control inputs from committed pinned paths (not caller overrides). This addresses the grader override pin caveat without weakening the traced-access predicate or changing the kill rule. No counter implementation/edit performed.

Contradictions and limits: stage 1 explicitly says stage 2 comes after wave 1 but before any claimed work is scored; freeze is therefore incomplete at measured revision `a543d920`. Stage 1 committed claim text exists, but stage-2 counter/input/population/control freeze does not. No scored counter/probe execution was attempted. Cannot establish whether forthcoming v3 counter reuses a failure mode absent its implementation. No external sources opened.

Sources opened: `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` (accessed 2026-10-27), `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` (accessed 2026-10-27), `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/pkg_gate.py` (accessed 2026-10-27), `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/grader.py` (accessed 2026-10-27). Located quotes (each <=25 words):
- claims §C1: “a fixture result is `LEAK` only if traced opens/reads outside `d` are observed”
- claims §Freeze shape: “before any claimed work is scored”
- pkg_gate.py: “a receipt a fresh run does not reproduce are defects.”
- grader.py: “overridden paths are by definition mutated copies”

Scratch cleanup: `trap 'rm -rf /fast/scratch/hyaku/kengaku-r48/R48C1ConnPattern' EXIT` was installed on the clone command; scratch was removed on command completion.

VERDICT: calibration-specific boundary comparison only; no admission judgment. Measurement blocked pending committed stage-2 freeze.