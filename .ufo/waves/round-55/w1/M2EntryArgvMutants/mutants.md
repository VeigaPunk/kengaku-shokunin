# R55 w1 seat M2EntryArgvMutants — per-mutant kill evidence

Target: `plans/round55_c2_entryargv.py` NEW legs (L1 argv identity, L2 wrapper, L3 abbreviation,
L4 registry-cell ground truth). Scratch-only: every mutant is a patched **copy** under
`/fast/scratch/hyaku/kengaku-r55/M2EntryArgvMutants/mods/<mutant>/plans/`; the lane file was
never written.

- Pristine lane `plans/round55_c2_entryargv.py` sha256
  `2bf9e66ce3d5bace914cdd3402f43333edf81eb05c12819d6e819fe199c6ea74` — identical before and
  after the probe (restoration evidence; the r54 module
  `44c3f412852396451b34fa7d0373b0a5901480189cbf77447b3b050d1cc0da97` likewise unchanged).
- Detector: each module variant's `evaluate(fixture, fixture, work, jobs=1, timeout=60, dry=False)`
  over one-row git fixtures (toplevel-guarded, built with the lane's own
  `round55_c2_controls._fixture` for the frozen two). Bounded: 60 s steps, probe wall 1.8 s of
  the 25 min budget. Detector validity: pristine `--selftest` = `4/4 PASS` exit 0; truthful
  fixture F0 exits 0 (`PREDICATE R55-C2 pass`) under **all six** module variants — no mutant
  breaks honest input.
- Full rc matrix + salient lines: `receipts/matrix.json`, `receipts/matrix.txt`; per-mutant
  patch diffs: `receipts/diff-*.patch`.

## Fixtures (one row each, name `fixture-gate`)

| id | registry cell | ledger entry_argv | declared | isolates |
|---|---|---|---|---|
| F0 | `python3 plans/fixture_gate.py` | same | red 1 + evidence | truthful baseline (must pass) |
| F1 | `python3 plans/fixture_gate.py` | `… decoy-positional` | red 1 + evidence | only L1 fires (r54 legs clean, L2/L3 clean) |
| F2 | `python3 plans/fixture_gate.py -cprint('wrapper green')` | token-equal (shlex) | red 1 + evidence | only L2 fires (inline `-c` token; L1 token-equal, L3 clean) |
| F3 | `python3 plans/fixture_gate.py --selft` | token-equal | green 0 (truthful: argparse accepts the abbrev) | only L3 fires (L1 token-equal, L2 clean) |
| F4c | `python3 plans/fixture_gate.py` | `… --go` (gate-green flag) | green 0 | laundering shape; caught by L1 statically, L4 dynamically (see M1 row) |
| FRZN | the two frozen controls (`abbreviated-selftest`, `uv-decoy-script`) via `controls._fixture` | green 0 | frozen fixture-kill cases |

## M1 — L1 comparison removed — **KILLED**

- Patch (unique site in `binding_static_legs`): `if led != reg:` → `if False and led != reg:`
  (`receipts/diff-M1-L1-silenced.patch`). Mutant sha256 `ed35e005…9afbd`.
- Expected detector: F1 flips (pristine fail → mutant pass); frozen cases stay killed (L2/L3).
- Observed F1: pristine `rc=1` with
  `ARGV-DEFECT fixture-gate: ledger entry_argv != registry cell argv ['python3', 'plans/fixture_gate.py', 'decoy-positional'] != ['python3', 'plans/fixture_gate.py']`,
  `BINDING l1=1 l2=0 l3=0`, `RUN executed=0`, `PREDICATE R55-C2 fail`;
  mutant `rc=0`, `BINDING l1=0 l2=0 l3=0`, `RUN executed=1 timeout=0 mismatched=0 evidence_missing=0 laundered=0`,
  **`PREDICATE R55-C2 pass`** → flip. **Leg load-bearing.**
- Frozen cases under M1 still killed (redundant depth): abbreviated → `ABBREV-DEFECT … '--selft'` rc 1;
  uv-decoy → `WRAPPER-DEFECT … argv[0]='uv' is not an interpreter` rc 1.
- Bonus evidence (L4 catches what L1 misses): under M1, F4c goes from static `ARGV-DEFECT` rc 1
  to runtime `LAUNDERED fixture-gate declared green, entry exit=1`, `laundered=1`, rc 1 — L1 and
  L4 back each other up.

## M2 — L2 wrapper check removed — **KILLED**

- Patch: `w = _wrapper_defect(n, led)` → `w = None` (unique site). Mutant sha256 `cd7cf530…703b`.
- Expected detector: F2 flips; frozen uv-decoy stays killed (L1).
- Observed F2: pristine `rc=1` with
  `WRAPPER-DEFECT fixture-gate: inline program token '-cprint(wrapper green)' (-c)`,
  `BINDING l1=0 l2=1 l3=0`, `PREDICATE R55-C2 fail`; mutant `rc=0`, `RUN executed=1 … laundered=0`,
  **`PREDICATE R55-C2 pass`** → flip. **Leg load-bearing** — note the isolated defect is the
  inline `-c` clause; r54's `entry_mode_ok` passes this argv (bare `-c` in SHELLS only), so this
  route launders the r54 counter (F2 is a third r54 laundering shape beyond the frozen two).
- Frozen uv-decoy under M2 still killed via `ARGV-DEFECT` (ledger≠registry tokens) rc 1.

## M3 — L3 abbreviation check removed — **KILLED**

- Patch: `a = _abbrev_defect(n, led, body_flags)` → `a = None` (unique site). Mutant sha256
  `7851b13e…f8ea`.
- Expected detector: F3 flips; frozen abbreviated stays killed (L1).
- Observed F3: pristine `rc=1` with
  `ABBREV-DEFECT fixture-gate: flag '--selft' abbreviates a script flag (prefix, not verbatim)`,
  `BINDING l1=0 l2=0 l3=1`, `PREDICATE R55-C2 fail`; mutant `rc=0`, `RUN executed=1 … laundered=0`,
  **`PREDICATE R55-C2 pass`** → flip. **Leg load-bearing** — F3 puts the abbreviation in the
  registry cell itself with a truthful green ledger (the abbreviated argv genuinely exits 0), so
  no other leg fires; L3 is the only guard against argparse-abbreviation entries.

## M4 — L4 registry-cell ground truth replaced by ledger-argv execution (r54 behavior) — **SURVIVED at single-leg granularity** (coverage finding)

- Patch: in `evaluate.job`: `spec["entry_argv"] = registry_entry_argv(s["rows"][n])` →
  `spec["entry_argv"] = list(s["ledger"]["rows"][n]["entry_argv"])`. Mutant sha256
  `9b3b1db4…f2543`.
- Acceptance expectation: re-introduces laundering. **Observed: no flip on any of the 7
  fixtures** — outputs byte-identical to pristine everywhere (e.g. F4c under M4 shows the same
  `ARGV-DEFECT … '--go' …` line, `RUN executed=0`, rc 1; frozen cases identical to pristine).
- Why (structural, confirmed by the matrix): `evaluate` excludes every L1-flagged row from
  execution (`names = [n for n in names if not any(d.startswith(f"{n}:") …)]` over
  `argv_defect`, which `binding_l1` entries are appended to), so ledger-argv execution is never
  reached; and for L1-clean rows ledger argv ≡ registry argv, making the two argv sources
  indistinguishable. A single-leg L4 silence is therefore **unobservable** — L4's
  registry-binding is dead weight *given L1*, but it is not removable: it is the runtime
  backstop when L1 is bypassed (see M1/F4c `LAUNDERED` above) and the sole executed-vs-declared
  ground truth.
- Supplementary probe (clearly labelled — NOT single-leg): **M1+M4 combined** (exactly the r54
  behavior: no argv-identity check + ledger-argv execution) flips F4c: `rc=0`,
  `RUN executed=1 timeout=0 mismatched=0 evidence_missing=0 laundered=0`,
  **`PREDICATE R55-C2 pass`** while the registry-declared entry `python3 plans/fixture_gate.py`
  exits 1 and the ledger declares green 0 — **laundering re-introduced**. Mutant sha256
  `ed7151f7…a0dbd`. The frozen two fixtures remain killed even under M1+M4 (L3 / L2
  respectively still fire), so F4c (a clean-flag divergence) is the minimal laundering shape.
- Verdict: single-leg M4 = **SURVIVED / vacuous** (the acceptance's "L4 mutant re-introduces
  laundering" is achievable only jointly with L1 silence). Per the mutation-tester contract this
  is a coverage finding about redundancy ordering (L1 statically covers L4's argv source; L4
  dynamically covers L1's bypass), **not** a contract change and not a soundness break of
  R55-C2: the frozen kill-rule attack (all static legs clean + true entry fails) still cannot
  pass — under the combined mutant only, which no longer is the r55 counter.

## Verdict summary

| mutant | verdict | flipping fixture | baseline break |
|---|---|---|---|
| M1 L1 silenced | KILLED | F1-L1sole-positional-decoy | none |
| M2 L2 silenced | KILLED | F2-L2sole-inline-c-token | none |
| M3 L3 silenced | KILLED | F3-L3sole-registry-abbrev | none |
| M4 L4 → ledger argv (single-leg) | SURVIVED (vacuous; finding) | — | none |
| M1+M4 (supplementary, r54 behavior) | laundering re-introduced | F4c-laundering-go-flag | none |

Analysis finding (derived, not run): L2's `argv[0]`-interpreter clause cannot be the sole
detector while L1 is intact — any wrapper at `argv[0]` breaks token-identity with the registry
span (which must start `python3`) and so always co-fires L1; only L2's inline `-c` clause is
independently load-bearing (F2).
