# R38RevCounters — review of round-38 C1/C2 counters and the build-pmars probe

Seat: reviewer, kengaku round 38 wave 1 (leaf; no subagents used, no scratch clone needed — read-only review of the lane plus two control receipts; nothing was written outside this report).

## Scope and method

Under review (all confirmed byte-equal to freeze commit `e0a378539a45cc9388c66cfba22f44275131de23` by
`sha256sum <file>` vs `git -C <lane> show e0a3785:<path> | sha256sum`, job bg_5787, all six MATCH:
c1 `8069739990c7…`, c2 `d906d55f2656…`, probe `32f0771cd5c4…`, claims `5a7437835791…`, gate `ea63882240e6…`,
spec `bd9bfe71c1c9…`). Probe/gate/spec digests also equal the pins inside the C2 counter
(`plans/round38_c2_verify.py:56-62`) and C1's gate pin (`plans/round38_c1_verify.py:73`).

Read in full: both counters, the probe, `plans/pkg_gate.py` (grep-verified scratch/write surface),
`plans/round37_c1_verify.py` (Ctx, loaders), `plans/round36_c1_verify.py` (helpers the fixtures call),
frozen dry table, probe receipt, both committed controls. Evidence commands are named inline.

## Findings by severity

### 1. MEDIUM — C2 V6 executes an unpinned, outside-the-lane input, contradicting the counter's own pin claim
- `plans/round38_c2_verify.py:9-11`: "Every input this counter reads that exists at the freeze is pinned here
  by digest". `:63`: `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"` — an executed input
  (`:199-202`, `subprocess.run([CENSUS, "validate", …])`) that is neither pinned nor in the lane. The pin block
  `:48-62` cannot cover it.
- Drift is silent: a weakened census (`exit 0`) turns V6 permanently green with no `PINS`/V-alarm; a broken one
  turns V6 permanently red. The predicate's "measured on a clean clone" only reproduces on this workstation —
  on any other host V6 fails with FileNotFoundError (honest red, but non-portable).
- Impact bounded: V3 (`:137-148`) independently binds each S-row's 11-cell registry anchor to its own spec-r38
  pin, and V2 pins gate+spec, so S115/S116 authenticity does not rest on the census; census adds registry-shape
  validation. Precedent for the absolute path: `plans/adoption_check.py:35` (same fleet instrument) — but this
  counter's docstring claims more than the code does, on the exact axis (D7) this round is closing.
- Fix: pin the census digest and print it with the V6 note, copy the script into the lane, or narrow the
  docstring sentence to "every lane input".

### 2. MINOR-MEDIUM — C1 mirror attribution does not enforce the accept-side demonstration the assignment's kill rule states
- Assignment kill rule: "mirror → reference prints the clause `ok`, mutant prints it `DEFECT` (so a mirror needs
  an ACCEPT-side fixture where that clause runs and passes)". Code: `plans/round38_c1_verify.py:197-198` only
  requires both rc ∈ {0,1}; the mirror arm `:204` is `return clause in ref[2] and clause in mut[1]` — no
  `ref[0] == 0`. The counter's own docstring formal rule (mirror sentence) matches the code, but both drop the
  assignment's accept-side requirement.
- Concrete false-green shape: a battery38 reject fixture whose package has valid quotes (P3 prints `ok` in the
  reference) but e.g. P6 teaches defects (declared={P6}) — mutant N02 flips P3 `ok`→`DEFECT` on an input the
  gate already rejects, and the kill is attributed, while "a package with exactly min_distinct_locations quote
  lines is accepted" was never demonstrated on any accepting input. Same for N08/N15. The calibration count
  (killed=22) can then include kills that demonstrate strictness, not the advertised false-red direction — the
  exact gaming the ATTRIBUTED rule was built to prevent.
- Fix: in the mirror arm require `ref[0] == 0` (reference accepts), keeping the clause flip as the delta.

### 3. MINOR — C1 pin set incomplete vs its own "every input" claim: round-35 package corpus bytes are unpinned
- `plans/round38_c1_verify.py:49-50`: pins are "every input of this counter that exists at the freeze";
  `:72-87` pins only gate, r36/r37 counters, r35 spec, attribution audit, nine battery37 modules.
- Fixtures consume unpinned lane corpus bytes through the pinned helpers: `copy_package` copies entry, receipt,
  sources, readme, frozen instruments, the whole capture_dir tree, plus every `corpus/knowledge/*.md` and
  `corpus/lessons/*.md` (`plans/round36_c1_verify.py:55-68`); `d4_line`/`d5_line` read `spec["d4_source_file"]`/
  `spec["d5_source_file"]` (`:161-172`); line fixtures read `spec["d5_capture_dir"]`
  (`plans/round37_c1_verify.py:211`).
- Mitigation: drift in gate-validated bytes trips the accept fixtures (r36-P0/L1/L4) → `wrong>0` → red — loud,
  but diagnosed as `FIXTURE … WRONG`, not `PINS mismatched`. Drift in bytes no clause validates (lessons/*.md,
  non-entry knowledge content) changes fixture inputs silently over time: a reproducibility hole for kill
  attribution, not an immediate false-green at one landing.
- Fix: pin the spec-named package files (fixed list once the r35 spec is pinned), or state the exception.

### 4. MINOR — C1 executes pinned-but-unverified code before enforcing the pin verdict
- `plans/round38_c1_verify.py:218` prints the pin state; `:219` `r37 = load(lane / R37_REL, …)` executes the
  round-37 counter module unconditionally, `:222` `load_r36` likewise; `gate_ok` (`:221`) guards only the gate
  pin, and only the mutant block. With a mutated r37 module, every BATTERY/MUTANTS diagnostic between `PINS`
  and `PREDICATE` is produced by unverified code (it supplies `Ctx`, the fixture builders, `GATE_REL`).
- No false-green: `good` (`:328-329`) requires `not mism`, so any pin mismatch keeps the predicate red.
- Fix: on any pin mismatch, print the predicate as fail and return before any `load`.

### 5. MINOR — a battery38 module without FIXTURES is silently skipped
- `plans/round38_c1_verify.py:172-173`: `out.extend(… for fx in getattr(mod, "FIXTURES", []))` — a misspelled
  or missing FIXTURES shrinks the battery with no diagnostic (`fixtures=<n>` just drops). Cannot false-green the
  predicate (kills must still reach 22), but it can silently discard an executor's wave-1 work and mislead the
  wave. Same pattern in the pinned `battery37_fixtures` (r37 counter), harmless there.
- Fix: require a list-typed FIXTURES per module, or print `MODULE <name> fixtures=0`.

### 6. MINOR — probe: per-case failures abort with a traceback and a truncated receipt instead of a SETUP diagnostic
- `plans/build_pmars_probe.py:268` (`timeout=180`) and `:220` (gcc `check=True`) raise through the unguarded
  case loop (`:323` `rc, out = run_case(cap, root, c)`); main has no per-case except. Failure is honest (nonzero
  exit; a false receipt is impossible), but the output is a Python traceback after partial CASE lines, giving
  C2 V2/P10 a byte-different receipt with no machine-readable reason — inconsistent with the C2 counter's own
  hygiene rule "a check that cannot run is a defect, never a pass" (`plans/round38_c2_verify.py:269-271`).
- Fix: wrap the per-case call, print `SETUP case <id> …`, return 2 (style of `:329-332`).

## Verified clean (evidence)

- **TMPDIR/--work honoured, no host /tmp**: C1 root `tempfile.mkdtemp(prefix="k38-c1-", dir=a.work)`
  (`round38_c1_verify.py:230`); C2 `TemporaryDirectory(prefix="k38-c2-", dir=a.work)` (`round38_c2_verify.py:262`);
  probe `mkdtemp(prefix="k38-bpm-", dir=a.work)` (`:308`) plus per-case `mkdtemp(dir=root)` (`:256`). `dir=None`
  falls to the tempfile default, i.e. $TMPDIR. The only `/tmp` literals are sandbox-internal (probe `:245`
  `--tmpfs /tmp`, `:265` `HOME=/tmp` — inside bwrap namespaces). All three clean up in `finally`.
- **Determinism**: sorted module globs (C1 `:165-173`; battery37 likewise), fixed fixture order, index-derived
  renamed-dir names (`:273-277`), sorted pin echo (probe), insertion-ordered JSON, receipt carries no paths or
  timing (checked against the committed `corpus/evidence/round38/build-pmars-probe.txt` — every line path-free);
  null-mutant rerun (`:281-284`) catches run-to-run fixture nondeterminism; the claims record a second full run
  byte-equal; control-c1-nothing.txt shows `real 0m48.467s` for the whole 64-fixture × 23-gate sweep.
- **Attribution vs docstring**: silence `:202-203` (declaration required; battery38 forced to declare via
  `:261-264`), RUN `:200-201`, MAIN `:196`, family routing `:190-193` + `:90` — all match the docstring kill
  rule and family sentence. Legacy laxity (`declared := ref[1]`, `:199`) exists but control-c1-nothing.txt
  proves the legacy battery kills 0/22 (`MUTANTS total=22 killed=0 survived=22 invalid=0 null_detected=0`), so
  all 22 kills at landing must come from declared battery38 fixtures or enforced mirror semantics.
- **Mutant hygiene**: `old` must occur exactly once and the mutant must compile, else `invalid` (control shows
  `invalid=0` at the frozen gate digest — all 22 olds unique); mutant file re-hashed after the kill loop.
- **C2 checks**: V4 pins receipt ids to the frozen dry-table order and cross-checks the summary against parsed
  CASE lines; V7 derives each label from ALL violating cases (`:239-243`), requires ≥1 cited violating case
  (`:246-248`), exactly one row per frozen tag (`:249-252`); V3 binds each anchor to its row's own spec pin —
  routed items D2/D3 are genuinely implemented. Skip-control red path confirmed:
  control-c2-skip.txt shows the hand-typed `observed=predicted` receipt stays red via V2 (gate P10 fresh-run
  byte-compare) plus V6, `checks=7 defects=2`, exit 1. No pin bypass: spec/dry digest mismatches raise into the
  per-check except (`:269-271`) → DEFECT, never pass; probe verifies capture pins before any case (`:300-303`).
- **Pins answer**: C1 reads no unpinned input beyond battery38 (by design, the measured work product) and the
  round-35 package corpus bytes (finding 3). C2 reads no unpinned lane input; its one unpinned input is the
  fleet census (finding 1). Separability as claimed: C1 touches no C2 surface and vice versa (code read).

## Residual risk and verification gaps

- V1 is manifest-scoped: a *tracked* stray file in `corpus/evidence/round38/tb2-build-pmars/` is invisible to
  V1 (`extra=` covers only listed-but-unknown entries) and P9 catches only untracked files. "5 files +
  SHA256SUMS" directory closure is not enforced.
- C2 V2 `timeout=1800` (`:122`) is below the probe's theoretical worst case (22×180 s); several hung cases
  surface as V2 TimeoutExpired → DEFECT (honest red, noisy).
- Probe sandbox binds host `/etc` and `/usr` read-only; ldd/bash are the host's (disclosed in the probe
  docstring limits) — cross-host receipt reproduction is not guaranteed; the predicate is measured here.
- The sidechannel scan is a case-sensitive substring heuristic (`:89`, `:168-171`); documented as heuristic;
  non-author battery38 code review remains part of admission.
- I did not re-run either counter or the probe (frozen artifacts; digest equality plus the two committed
  controls stand in). No scratch dir was created, so none needed cleanup.

VERDICT: review-6-defects
