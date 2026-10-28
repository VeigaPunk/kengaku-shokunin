# R49C2ExecMutBattery — C2 mutation battery (round 49, wave 1)

seat: `R49C2ExecMutBattery` (executor), claim R49-C2 (coverage)
axes named: **coverage** (primary — V14 mutation sensitivity of the frozen C2 leg contract);
secondary observation only: **operability** (the battery is re-runnable by the L1 before stage 2)
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93
(spec projection uncommitted in the measurement mirror: `plans/pkg-spec-r49.json` sha256
`c07427776e7c21c09fb6642128edf13cb928f1bfb22a18d68ff3cc59c1e74108` — every other byte read by the legs is
the committed byte at the frozen base)
VERDICT: **23 mutants authored and measured; 20 caught / 23 (floor 11.5) — mutation floor MET at content
level. Behavioural findings: probe mutants are structurally uncatchable by V14's substantive set (V5 only),
one entry mutant is masked by the V7 baseline defect, and one spec mutant is caught only by the spec digest
pin (blind at content level). Plan + payloads emitted; no admission claimed.**

## 1. Freeze check (before any measured leg run)

```
$ git -C /fast/scratch/hyaku/kengaku-r49/R49C2ExecMutBattery/lane rev-parse HEAD
9d2900af41e4d1fc6022eff99010436fde6dbd93
$ git -C … lane log -1 --format='%H %ci %s' 9d2900af…
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence
over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims
$ git -C … lane merge-base --is-ancestor 9d2900af… origin/master && echo …
freeze is ancestor of origin/master
```

Measurement wall clock: `2026-10-28T09:24:34-03:00` … `2026-10-28T09:27:17-03:00`. The freeze commit predates
the first measured leg run by 9m54s and is an ancestor of `origin/master`, so the freeze-precedes-measurement
precondition holds. No scored counter or scored probe run was made: the leg
functions were invoked directly by a scratch instrument (below), never `plans/round49_c2_verify.py` (absent
at the freeze) and never the probe's full-run path.

Frozen pins verified at the base before measuring (byte-equal to the imported counter's constants):

```
masked spec digest   560c7bfb3f12fcfeaed6cb33ed3adc4b881b59b1c8f5ca9e3a094f10c1513f6e  (== SPEC_SHA256)
probe               67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26  (== PROBE_SHA256)
dry table           99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536  (== DRY_SHA256)
```

## 2. What was measured, and how

Instrument (in this directory, verbatim): `mut_harness.py` (sha256
`185bb3f3f13c20b7ec19f7df56b6877dc423709f8d13c6a3790cf164176ce33c`). It

1. imports the frozen counter `plans/round46_c3_verify.py` from the base clone (never copies it) and calls its
   `v3`, `v4`, `v9`, `v10`, `v12`, plus the round-48 v4 **V7 delta transcribed verbatim** (positive
   tag/violates preconditions, then the imported label/citation rule);
2. builds a **symlink-mirror** of the base: `corpus/knowledge` and the capture dir are copied (a mutant can
   never write through a directory symlink into the lane), `corpus/SOURCES.md`, `corpus/README.md`,
   `PROVINCE.md` are symlinked, and only the six mutable byte classes are real files;
3. constructs the package object from `plans/pkg-spec-r49.json` **re-read per measurement** (so a spec mutant
   is seen, as the counter's `real_pkg()` does), runs the six substantive legs on the pristine mirror
   (baseline), then installs exactly one payload, re-runs the legs, and restores the pristine bytes (sha256
   asserted equal after every restore);
4. refuses to install outside the mirror (absolute/`..`/parent-resolution guard, same rule as V14).

Landing projection, stated because the freeze has no round-49 artefacts: `plans/pkg-spec-r49.json` in the
mirror is `plans/pkg-spec-r46.json` with `receipt`/`dry`/`probe` repointed to the round-49 slots fixed by the
claims (`corpus/evidence/round49/polyglot-c-py-probe.txt`, `corpus/evidence/round49/polyglot-c-py-dry-cases.txt`,
`plans/polyglot_c_py_probe.py`) and `receipt_sha256` recomputed; the two round-49 evidence slots carry the
**committed round-46 bytes**. Every payload is therefore a mutation of a committed base byte; only the
addressing is projected. Nothing in the lane was written.

Command (cwd `/fast/scratch/hyaku/kengaku-r49/R49C2ExecMutBattery`, `TMPDIR` same dir):

```
python3 mut_harness.py
```

Baseline (verbatim, `mut-battery-run.log`):

```
BASELINE V3=ok V4=ok V7=DEFECT V9=ok V10=ok V12=ok
BASELINE-NOTE V3 rows=7 bad=0
BASELINE-NOTE V4 cases=18 mismatches_named=0/0 bad=0
BASELINE-NOTE V7 rows=7 tags=7 violated=5/7 bad=7 first=both-print:no committed case carries violates=both-print
BASELINE-NOTE V9 case_rows=18/18 bad=0
BASELINE-NOTE V10 mechanism_rows=18/18 bad=0
BASELINE-NOTE V12 rows=7 defective=0 live=0
```

The V7 baseline defect is the stage-1 state the claims already name (`both-print`/`toolchain` carry no
violating case; the two `not exercised` requirement-map rows are non-canonical). V14 credits a mutant only
when a leg that was **ok at baseline** flips, so V7 is disclosed as `baseline_defects=V7` and cannot be
credited in this measurement.

## 3. Mutants and measured flips (23)

Targets are the landing-era mutable set derived from the projected spec:
`plans/pkg-spec-r49.json`, `corpus/knowledge/tb2-polyglot-c-py-grader.md`,
`corpus/evidence/round49/polyglot-c-py-probe.txt`, `corpus/evidence/round49/polyglot-c-py-dry-cases.txt`,
`plans/polyglot_c_py_probe.py`, and the 8 entries of `CAPTURES` under `corpus/evidence/round46/tb2-polyglot-c-py/`.
All 23 targets are inside that set (machine-checked; `measurement.json` → `mutable`). Payloads are at
`payloads/<name>.payload`, digest-pinned in `plan.json`; every payload differs from the byte it replaces.

| mutant | class | target | content flips (V3/V4/V7/V9/V10/V12) | caught |
|---|---|---|---|---|
| `cap-test-outputs-values` | capture | `corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py` | V10,V12 | yes |
| `cap-test-outputs-listing` | capture | `corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py` | V10,V12 | yes |
| `cap-instruction-stdout` | capture | `corpus/evidence/round46/tb2-polyglot-c-py/instruction.md` | V12 | yes |
| `cap-test-sh-reward` | capture | `corpus/evidence/round46/tb2-polyglot-c-py/test.sh` | V12 | yes |
| `cap-solve-sh-comment` | capture | `corpus/evidence/round46/tb2-polyglot-c-py/solve.sh` | V12 | yes |
| `cap-dockerfile-base` | capture | `corpus/evidence/round46/tb2-polyglot-c-py/Dockerfile` | V12 | yes |
| `cap-task-toml-internet` | capture | `corpus/evidence/round46/tb2-polyglot-c-py/task.toml` | V12 | yes |
| `cap-readme-cases` | capture | `corpus/evidence/round46/tb2-polyglot-c-py/README.md` | V12 | yes |
| `entry-casetable-verdict-flip` | entry | `corpus/knowledge/tb2-polyglot-c-py-grader.md` | V9 | yes |
| `entry-mechanism-line-shift` | entry | `corpus/knowledge/tb2-polyglot-c-py-grader.md` | V10 | yes |
| `entry-source-id-removed` | entry | `corpus/knowledge/tb2-polyglot-c-py-grader.md` | V9 | yes |
| `entry-reqmap-label-invert` | entry | `corpus/knowledge/tb2-polyglot-c-py-grader.md` | — (V7 note delta only) | no |
| `receipt-verdict-swap-compile-warning` | receipt | `corpus/evidence/round49/polyglot-c-py-probe.txt` | V4,V9 | yes |
| `receipt-prediction-drift` | receipt | `corpus/evidence/round49/polyglot-c-py-probe.txt` | V4 | yes |
| `receipt-summary-splice` | receipt | `corpus/evidence/round49/polyglot-c-py-probe.txt` | V4 | yes |
| `receipt-inventory-rename` | receipt | `corpus/evidence/round49/polyglot-c-py-probe.txt` | V4,V9,V10 | yes |
| `dry-inventory-rename` | dry table | `corpus/evidence/round49/polyglot-c-py-dry-cases.txt` | V4,V10 | yes |
| `dry-inventory-duplicate` | dry table | `corpus/evidence/round49/polyglot-c-py-dry-cases.txt` | V4,V10 | yes |
| `spec-s168-digest-drift` | spec | `plans/pkg-spec-r49.json` | V3,V12 (content), plus spec pin refusal | yes |
| `spec-s172-capture-name` | spec | `plans/pkg-spec-r49.json` | V12 (content), plus spec pin refusal | yes |
| `spec-row-set-contraction` | spec | `plans/pkg-spec-r49.json` | none (content); spec pin refusal only | yes |
| `probe-tags-line-shift` | probe | `plans/polyglot_c_py_probe.py` | none | no |
| `probe-case-expect-flip` | probe | `plans/polyglot_c_py_probe.py` | none | no |

```
SUMMARY total=23 caught=20 floor=11.5 uncaught=entry-reqmap-label-invert,probe-tags-line-shift,probe-case-expect-flip
```

Caught accounting follows the frozen V14 rule: a mutant is caught iff at least one substantive leg that was
ok on the pristine mirror flips to DEFECT. A spec payload is additionally refused by the frozen spec digest
pin before any leg runs, which the frozen V14 semantics score as a defect of every content leg
(`spec_pin_refused=True` on the three spec rows); the content-level flips listed beside them are the
measured *secondary* evidence (pin bypassed in the instrument only).

Representative verbatim leg deltas (`mut-battery-run.log`):

```
MUTANT cap-test-outputs-values … NOTE-DELTA V12: rows=7 defective=1 live=1 first=S166:capture_unresolved capture=0
  NOTE-DELTA V10: mechanism_rows=18/18 bad=['nop:test_outputs.py capture not pinned', …]
MUTANT entry-mechanism-line-shift … NOTE-DELTA V10: mechanism_rows=18/18 bad=['lookup-table:test_outputs.py:26 not decisive']
MUTANT entry-source-id-removed … NOTE-DELTA V9: case_rows=18/18 bad=["row ids absent outside source lines: ['S169']"]
MUTANT receipt-verdict-swap-compile-warning … NOTE-DELTA V4: bad=['summary disagrees with the CASE lines',
  "match=yes on a mismatching case: ['compile-warning']"]  NOTE-DELTA V9: bad=['case table rows=18 receipt cases=18 equal=False']
MUTANT receipt-prediction-drift … NOTE-DELTA V4: bad=['summary disagrees with the CASE lines',
  "match=yes on a mismatching case: ['stderr-noise']"]
MUTANT dry-inventory-rename … NOTE-DELTA V4: bad=['case ids differ from the frozen table']
MUTANT spec-s168-digest-drift … NOTE-DELTA V3: rows=7 bad=['S168:anchor_digest']  NOTE-DELTA V12: first=S168:capture_unresolved
MUTANT spec-s172-capture-name … NOTE-DELTA V12: rows=7 defective=1 live=1 first=S172:capture_unresolved capture=['README.md']
MUTANT spec-row-set-contraction … NOTE-DELTA V3: rows=6 bad=0  NOTE-DELTA V12: rows=6 defective=0 live=0
```

## 4. Findings that change how the battery should be scored

1. **Probe mutants cannot be caught by V14's substantive set.** The two `plans/polyglot_c_py_probe.py`
   mutants demonstrably change the probe's observable frozen table — `--dry` stdout sha256
   `77e46962d884d196362f5e7a5b3c777c51de9c954dbe6546a96a6970924d1acc` and
   `ecd8086695d22d642441b13ce9dea1e55b874d538015bba44e6762e972fd196b`, both `equal=False` against the frozen
   dry-table digest `99adfea6…` — yet no substantive leg reads the probe: `V3/V4/V7/V9/V10/V12` read the spec,
   entry, receipt, dry table, registry and captures only. The probe is read by **V5** (and by V15's
   precondition). With the frozen substantive set, a probe tamper is only visible at V5, so V14 reports
   `probe-*:CLEAN`. Options for the L1 (stage-2 literals only, no predicate change requested): keep the two
   probe mutants in the plan (they stay CLEAN and the 20/23 catch stands), or pin `<N>` over the 21
   non-probe mutants and keep the probe mutants as disclosed near-misses. Promoting V5 into the substantive
   set would change a frozen line and is **not** proposed here.
2. **`entry-reqmap-label-invert` is masked by the V7 baseline defect.** Its V7 note moves
   `bad=7 → bad=8` (the label rule names `python-run: labelled unenforced, receipt derives enforced`), so once
   the stage-2 requirement-map repair makes V7 green this mutant flips V7 and becomes caught. At the stage-1
   baseline it is correctly not credited.
3. **`spec-row-set-contraction` is invisible at content level.** Dropping S172 from the spec leaves
   `V3 rows=6 bad=0` and `V12 rows=6 defective=0 live=0`: V3/V9/V12 iterate the spec's *own* row set and
   nothing cross-checks it against the registry's S166–S172. At landing the spec digest pin refuses the
   mutant (caught), but the blind spot becomes live the moment a contracted spec is itself re-pinned. A V15
   row-set precondition (`spec rows == {S166..S172}`) or a V3 row-count check would close it; both are
   stage-2/leg-contract decisions for the L1, not changes made here.
4. **Mutable-set boundary is narrower than the bytes the legs read.** `corpus/SOURCES.md` (read by V3 and V12)
   and the capture `SHA256SUMS` (read by V1) are committed package bytes but are not V14-mutable targets, so an
   anchor-row tamper or a manifest tamper cannot be expressed as a plan mutant. V3/V12/V1 do catch such
   tampering content-wise; only the battery's coverage is limited. Named, not worked around.
5. **Content-level measurement is not V15-blocked, by design.** V14 calls the substantive legs directly, so
   the instrument does the same. A scored counter run would additionally show V15 blocking V1/V10/V12 for
   capture mutants, V4/V5/V7/V10 for dry-table mutants and V2/V5 for probe mutants; those blocks are *not*
   counted here, which makes this a conservative lower bound on the counter's rejection behaviour.

## 5. Handoff to the L1 (stage 2)

- Deliverables in `.ufo/waves/round-49/w1/R49C2ExecMutBattery/`: `plan.json` (sha256
  `eafa74619b6e13706e5aaadc109aa2d886d9d8f00ea5b01835e98a28c182cd20`, 23 mutants with
  `name`/`class`/`target`/`payload`/`sha256`/`intent`, plus `mut_n=23`/`mut_floor=12`), `payloads/` (23 files), `measurement.json`
  (baseline + per-mutant leg notes), `mut-battery-run.log`, `mut_harness.py` (the instrument).
- Landing: copy `payloads/*.payload` → `plans/mutants49/` and `plan.json` → `plans/mutants49/plan.json`;
  the payload field is already `plans/mutants49/<name>.payload`, which is what V14 resolves against the lane
  root. Recommended stage-2 literals: `MUT_N = 23`, `MUT_FLOOR = 12` — V14 passes iff `caught >= floor`, and
  the claims fail the leg when `caught < 23/2` (i.e. caught ≤ 11), so the integer floor must be 12. Measured
  caught is 20.
- **Path dependency:** 4 receipt mutants + 2 dry-table mutants name
  `corpus/evidence/round49/polyglot-c-py-probe.txt` and `corpus/evidence/round49/polyglot-c-py-dry-cases.txt`
  (the paths fixed by the claims, and by `DRY_REL` in the v4 counter). If the landed spec names different
  paths, those 6 mutants become "target is not a frozen package byte" → 14/23 caught, still above the 11.5
  floor. The 8 capture-class, 4 entry-class, 3 spec-class and 2 probe-class mutants are path-stable.
- **Freshness under stage-2/3 drift:** the 8 capture payloads and the 2 probe payloads mutate bytes that do not
  change at stage 2. The receipt, dry-table and entry payloads are derived from the *base* bytes, so at landing
  they replace the amended bytes with a mutate-and-revert payload; they still introduce the internal
  inconsistencies recorded above and are caught for those reasons (verified logic, not re-executed against the
  amended bytes, which do not exist yet). If the L1 prefers minimal mutations of the landed bytes, the substitution table is one string per
  mutant, recorded in `intent` and in `mut_harness.py::mutants()` (e.g. `receipt-verdict-swap-compile-warning`
  replaces `CASE compile-warning predicted=pass observed=pass tests=P` with
  `… observed=fail …`); re-authoring changes the digests and must be followed by a re-run of the instrument.
- No admission is claimed here: the predicate still needs the stage-2 entry/case-table amendment for V7, the
  stage-2 probe revision, and the stage-3 receipt.

## 6. Limits

- Measured on the frozen base `9d2900af` with a projected spec; not on the stage-2/3 tree, which does not
  exist. The projection is byte-identical to the committed spec except the receipt/dry/probe paths and their
  recomputed receipt digest.
- V7 is a defect at the frozen baseline (claims' own stage-1 state), so V7 flips are disclosed, not credited.
- Only the six substantive legs were exercised; V1/V2/V5/V6/V8/V11/V13/V15 were not run, so this report says
  nothing new about them beyond the V5 read-path observation in finding 1.
- The instrument re-reads the spec per measurement but bypasses the counter's spec digest pin; the pin-refusal
  path is asserted (`spec_pin_refused`) rather than executed, because the round-49 counter is still a sibling's
  scratch candidate.
- No external source was opened this seat: the captures, entry, registry, receipt and probe were read from the
  committed lane tree at the frozen base. The one located quote relied on is the pinned S166 capture line,
  read locally at `corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py:27` and matching its pinned URL
  `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py`
  (not re-fetched today; capture digest `b94a7a98…` re-verified byte-equal from the tree): “test_cases = [(42,
  "267914296"), (10, "55"), (0, "0")]” (8 words).

## 7. Scratch discipline

Scratch root `/fast/scratch/hyaku/kengaku-r49/R49C2ExecMutBattery` (one `--shared` clone, one mirror, one
instrument); `TMPDIR` exported there; all fixture-side writes guarded inside the mirror and every mutation
restored with a sha256 assertion. Evidence was copied into this directory before teardown; the scratch tree is
removed at the end of this seat. No lane file, no `.ufo/state`, no sibling repo, no `MANIFEST.json` was written;
no commit, push or mutating lane git command was run. Tool installs: none (existing `python3`/`git` sufficed).
