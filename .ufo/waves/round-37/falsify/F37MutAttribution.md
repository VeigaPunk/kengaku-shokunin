# F37MutAttribution — round 37, wave 2 (falsify): attack on `plans/round37_c1_attribution.py`

Seat: mutation tester, lane `kengaku-shokunin`, integration tip `357dece` (branch master).
Target: the **post-hoc attribution audit** `plans/round37_c1_attribution.py` (audit bytes sha256
`7064cf1a2ef8e6ef26224b17d7da13a6b9aa6630fd83c13110d9474bbd7db147`), NOT the frozen rule
(`plans/round37_c1_verify.py`, sha256 `dbc9f719…73413cc`, untouched). Attacked receipts:
`.ufo/waves/round-37/integrate/c1-attribution.txt` (`ATTRIBUTED 55/55`) and
`c1-attribution-hostile.txt` (`6/55`).

Method: clone of the tip in NVMe scratch `/fast/scratch/hyaku/kengaku-r37/F37MutAttribution/fx/lane`
(HEAD verified `357dece`, `rev-parse --show-toplevel` verified, `status --porcelain` = 0 before any
write). Four single-point mutants of the audit were applied as separate copies (diffs:
`receipts/diff_attr_m*.txt`; mutant bytes: `mutants/`); each was run on (i) the landed battery and
(ii) the wave-1 hostile side-channel battery, produced exactly as the hostile receipt was
(`plans/battery37` replaced by the three `crit_p10_*.py` modules — the hostile receipt's
`BATTERY fixtures=17` = 14 r36 + 3 sidechannel fixtures). All runs used `--work` under the scratch dir;
`TMPDIR` pointed there.

## Baselines (both reproduced before mutating)

- Landed battery, pristine audit:
  `python3 plans/round37_c1_attribution.py --lane . --work "$S/w"` → `ATTRIBUTED 55/55 UNATTRIBUTED=0`,
  exit 0 (`receipts/r0_landed_pristine.txt`) — equals `c1-attribution.txt`.
- Sidechannel-only battery, pristine audit: same command → `ATTRIBUTED 6/55 UNATTRIBUTED=49`, exit 1
  (`receipts/r1_sidechannel_pristine.txt`) — equals `c1-attribution-hostile.txt`. The 6: M01 (r36-P5),
  M05 (r36-P3), M40 (r36-P6), M43 (crit-p10-mismatch), M47 (r36-L2), M54 (r36-L6).

## (a) The four audit mutants

| mutant | removed guard | landed battery | sidechannel battery | verdict |
|---|---|---|---|---|
| A1 `attr_m1_nofamily.py` | family check (`argv[0] != fam`) | 55/55, by= identical to pristine (0 differing ATTR lines) | 6/55, byte-identical to pristine | **survives — equivalent mutant** |
| A2 `attr_m2_nodeclared.py` | declared-defects check | 55/55, by= identical | 6/55, byte-identical | survives both batteries; exposed by purpose-built fixture (below) |
| A3 `attr_m3_anyrc.py` | `rc in (0, 1)` guard | 55/55, by= identical | 6/55, byte-identical | survives both batteries; exposed by purpose-built fixture (below) |
| A4 `attr_m4_noref.py` | `clause not in ref[j][1]` check | 55/55 but **all 55 by= lines flip** (110 differing ATTR lines) | **6/55 → 55/55, exit 0** | **exposed by the wave-1 hostile battery** |

Commands: `python3 "$S/attr_mX.py" --lane . --work "$S/w"` per state; outputs in
`receipts/r_attr_m*_{landed,sidechannel}.txt`.

- **A4 is the one the hostile battery catches.** With the reference-print check dropped, every mutant is
  attributed by the first family-matching *accept* fixture: on the sidechannel battery 43 P-kills go
  `by=r36-P0`, 4 D4-kills `by=r36-L1`, 8 D5-kills `by=r36-L4` (`receipts/r_attr_m4_noref_sidechannel.txt`)
  — accept fixtures where any non-crashing mutant trivially "hides" a clause that was never defective.
  On the landed battery the count stays 55/55 (so the count alone would NOT expose A4 there); only the
  by= map changes.
- **A1 is an equivalent mutant, provably.** The gate prints `D4`/`D5` DEFECT lines only from the
  d4-line/d5-line subcommands (`pkg_gate.py:325` `run_checks([("D4", check)])`, `:356` D5), and P-clauses
  only from the package subcommand — so `clause in ref[j][1]` already implies the family match. The
  audit's docstring advertises four guards; one is dead weight. Empirically: byte-identical output on
  both batteries.
- **A2 and A3 are untested by both wave batteries.** A2: on any counter-clean battery the counter itself
  enforces `res[1] == frozenset(declared)` for battery37 fixtures (`wrong=0` in both receipts) and r36
  fixtures carry `defects=None`, so the declared guard is implied — it only bites on a *misdeclared*
  fixture, which neither battery contains. A3: no kill in either battery has `rc ∉ {0,1}` (Python
  tracebacks exit 1, so only signals/exit≥2/timeout are excluded). Both exposed below by purpose-built
  hostile fixtures.

## (b) Residual: a counter-clean fixture the pristine audit still attributes wrongly

Fixture `fixtures/bait_p10_oracle.py` (fid `attr-p10-bait`, `expect=reject`, `defects=["P10"]`), dropped
into the clone's `plans/battery37/`. Its unpinned `plans/argparse.py` shim (imported by the frozen probe
before its own code) reads the running gate's bytes via `/proc` and **defects only under pristine gate
bytes** (receipt + marker line, exit 0 → P10 byte-mismatch); under every mutant gate it emits the receipt
verbatim, exit 0.

- Direct observation (driver, counter's own `run_gate`): pristine gate → `(rc 1, {P10})`; M41-mutant
  gate → `(rc 0, ∅)`.
- The frozen counter on sidechannel+bait: `python3 plans/round37_c1_verify.py --lane .` →
  `FIXTURE attr-p10-bait expect=reject declared=P10 observed_rc=1 observed_defects=P10 ok`,
  `BATTERY fixtures=18 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=55 … null_detected=0`,
  `PREDICATE C1 pass`, exit 0 (`receipts/r_v2_counter_sidechannel_bait.txt`). The fixture passes every
  counter integrity check.
- The pristine audit on sidechannel+bait: `ATTRIBUTED 8/55` — M41 and M42, previously UNATTRIBUTED, are
  now attributed `by=attr-p10-bait`; M43 is re-sourced to it (`receipts/r_p0_sidechannel_bait.txt`).
- The pristine audit on **landed+bait**: `ATTRIBUTED 55/55`, exit 0, with M41/M42/M43 flipped from
  `p910-*` to `by=attr-p10-bait` (`receipts/r_p1_landed_bait.txt`). One dropped file silently re-sources
  three attributions on the landed tip; the receipt's count and exit are unchanged — invisible unless the
  by= lines are compared.
- Why the attributions are wrong: under every mutant the receipt is readable, the fresh probe exits 0 and
  its output is byte-equal — none of M41/M42/M43's advertised classes is present; the kill is pure
  gate-identity detection. All four audit guards pass (family `package`; `P10 ∈ ref`; `P10 ∈ defects`;
  `rc 0`).

**Lesson:** every audit guard is satisfiable by a fixture that conditions on the running gate's bytes.
The counter's null/renamed checks cannot catch this class (null and renamed gates carry pristine bytes,
so an identity oracle behaves identically for them); the audit re-runs neither. A guard that would catch
it: run each fixture once under a *no-op-perturbed* gate (bytes differ, semantics identical) and require
the fixture's result to be unchanged — an identity oracle flips on exactly that. Advisory finding; the
frozen rule and the lane were not modified.

## Bonus: purpose-built fixtures exposing A2 and A3

Both are counter-clean in behavior; `aa` is deliberately misdeclared to show the audit ignores what the
counter flags.

- `fixtures/aa_p10_misdeclared.py` (fid `attr-p10-aa`, `expect=reject`, `defects=[]`, same oracle):
  counter on sidechannel+aa → `FIXTURE attr-p10-aa … observed_defects=P10 WRONG`, `wrong=1`,
  `PREDICATE C1 fail`, exit 1 (`receipts/r_v4_counter_sidechannel_aa.txt`). Pristine audit on the same
  battery: 6/55 (aa skipped — the declared guard works). A2 audit: **8/55**, M41/M42/M43
  `by=attr-p10-aa` (`receipts/r_a2_sidechannel_aa.txt`) — kills accepted from a fixture the counter
  rejects. The audit never consults the counter's `wrong` flag; the declared guard is its only defense,
  and no counter-clean battery exercises it.
- `fixtures/bait_p10_sigkill.py` (fid `attr-p10-sigkill`, `defects=["P10"]`): under a non-pristine gate
  the probe SIGKILLs the gate process itself (the `/proc` ancestor carrying the gate marker — not
  `getppid()`, which under the gate's `uv run` probe wrapper is uv, not the gate; first attempt killed uv
  and the gate survived to print `fresh probe exit=-9`, fixed by targeting the walked pid). Driver:
  pristine gate → `(1, {P10})`; M41 gate → `(-9, ∅)`. Counter on sidechannel+sigkill: `PREDICATE C1
  pass`, `killed=55`, `wrong=0 renamed_disagree=0 null_detected=0`
  (`receipts/r_v3_counter_sidechannel_sigkill.txt`). Pristine audit: 6/55 — the rc guard correctly
  refuses crashed-gate kills. A3 audit: **8/55**, M41/M42/M43 `by=attr-p10-sigkill`
  (`receipts/r_a3_sidechannel_sigkill.txt`).

## Exposure map (final)

- A1 (family check): equivalent mutant — unkillable by construction; the audit has three effective
  guards, not four.
- A2 (declared-defects check): exposed by `aa_p10_misdeclared` (6/55 → 8/55); not by either wave battery.
- A3 (rc guard): exposed by `bait_p10_sigkill` (6/55 → 8/55); not by either wave battery.
- A4 (reference-print check): exposed by the wave-1 hostile sidechannel battery itself (6/55 → 55/55).

## Integrity

- Lane untouched: `plans/round37_c1_attribution.py` sha256 `7064cf1a…7d7db147` before and after;
  `plans/pkg_gate.py` `ea6388…6edd41` = the freeze digest; `plans/round37_c1_verify.py`
  `dbc9f719…3413cc`. No lane file was written; no git/jj mutating command ran in the lane.
- Mutant and fixture bytes hashed in `receipts/SHA256SUMS`; per-mutant diffs in `receipts/diff_*.txt`.
- Scratch `/fast/scratch/hyaku/kengaku-r37/F37MutAttribution` (clone included) deleted after archiving;
  the tasking declares the scratch copy disposable, so no byte restoration beyond the lane-integrity
  check above applies.

VERDICT: attribution-mutants-1/4-residual-1
