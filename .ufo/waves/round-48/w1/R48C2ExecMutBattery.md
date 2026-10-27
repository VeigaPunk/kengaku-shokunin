# R48C2ExecMutBattery — the 13-mutant battery on the committed C2 package bytes

Seat: `R48C2ExecMutBattery` (executor), serving **R48-C2 (coverage)**. Kengaku round 48 (hyaku run 10), wave 1.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Scratch (now removed): `/fast/scratch/hyaku/kengaku-r48/R48C2ExecMutBattery`.

**REV a543d92083557dd9b33ee674e9b99b03411f80af** — the stage-1 freeze commit
(`round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims`),
commit time `2026-10-27 06:53:29 -0300`, i.e. **before** every measurement in this report (run window
`2026-10-27T08:33-03:00` … `08:48-03:00`). Every receipt copied under this report's directory begins with the
line `REV a543d92083557dd9b33ee674e9b99b03411f80af`. The freeze predates the measurement, so the scored-run
precondition is satisfied for the **base** instruments; see §5 for what is deliberately *not* run.

## 1. Axes named

- **coverage** (judged axis for R48-C2): mutation sensitivity of the committed package bytes — capture, entry,
  receipt, dry table, spec, probe — under the committed detector. The round-48 C2 contract names the counter
  `plans/round48_c2_verify.py` = `plans/round46_c3_verify.py` (digest-pinned import) + frozen deltas, and the
  delta (d) freezes the kill rule: *"each mutant must flip at least one substantive leg (V3/V4/V7/V9/V10/V12) to
  DEFECT; fewer than `<N>/2` caught → the counter prints `MUTATION DEFECT` and the predicate fails (round-46
  observed 0/13)"* (`plans/round-48-claims.md:104-107`).
- **calibration** (secondary): does the detector's *reported* defect set actually change when the package bytes
  change — i.e. is the counter's discrimination visible, not merely its exit status.
- **operability** (tertiary): is the battery re-runnable by the L1 from committed bytes alone, at the frozen base,
  with no probe run and no lane write.

## 2. What was measured, and against what

`plans/round48_c2_verify.py` **does not exist** at the stage-1 freeze (`ls plans/round48_*` → *No such file or
directory*; it is a wave-1 artefact the L1 writes and stage 2 pins). The detector therefore had to be the two
**committed** instruments the frozen contract builds on:

| instrument | path | sha256 (measured) |
|---|---|---|
| base counter (the contract's digest-pinned import) | `plans/round46_c3_verify.py` | `a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4` |
| package gate | `plans/pkg_gate.py` | `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` |
| probe (base tree; the hardened `22b7779e…` revision is **not** yet committed at `a543d920`) | `plans/polyglot_c_py_probe.py` | `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26` |

Leg set run per mutant: **V1, V3, V4, V5, V6, V7, V8, V9, V10, V12, V13** — i.e. the committed counter's legs
**minus V2** and **minus V11**.

- **V2 excluded on purpose.** `v2()` calls the gate with `--rerun`, and the gate's `P10` clause is a *fresh probe
  re-run* (`plans/pkg_gate.py:308` — `(n != "P10" or args.rerun)`). The frozen ordering forbids a probe run of the
  C2 package before the stage-2 commit. The gate was therefore run **without** `--rerun` (P10 disabled) — this is
  exactly the frozen V8/Q40 pre-receipt control mode the claims require — so the gate clauses P1–P8 are observed
  and P10 never fires.
- **V11 excluded from the scored battery** (it is not one of the frozen substantive legs and it is the expensive
  sandbox leg). It was measured **separately as supplementary evidence** over the same mutant trees
  (`v11-supplementary.json`) and is reported in §4. V11 executes the *captured grader* on freshly generated
  synthetic end states inside `bwrap`; it does **not** run the package probe and does **not** execute the task's 18
  graded case recipes.

**No full probe run and no graded case of this task was executed anywhere in this seat.** The only probe
invocation is the counter's own **V5**, which calls the probe with `--dry` (`plans/polyglot_c_py_probe.py:451` —
`if a.dry:`) and byte-compares the printed table against the frozen dry table. `--dry` prints the case table and
returns; it executes no case.

## 3. Baseline at the frozen base (pristine, no mutation)

`python3 mutbattery.py --lane <clone> --work <work> --out <json>` (harness in §6):

```
V1   ok      listed=8 wrong=0 extra=0
V3   ok      rows=7 bad=0
V4   ok      cases=18 mismatches_named=0/0 bad=0
V5   ok      probe=frozen dry_byte_equal=True
V6   ok      census_exit=0 registry=corpus/SOURCES.md
V7   DEFECT  rows=5 tags=7 bad=["unparsed row '| instruction.md:7 | both-print | not exercised | '", "unparsed row '| instruction.md:9 | toolchain | not exercised | n'", "tags missing=['both-print', 'toolchain'] duplicated=0"]
V8   DEFECT  order_exit=1 result=not-PASS
V9   ok      case_rows=18/18 bad=0
V10  ok      mechanism_rows=18/18 bad=0
V12  ok      rows=7 defective=0 live=0
V13  ok      filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
P1   ok      ok pinned=2 mismatched=0
P2   ok      ok receipt_sha256=pinned
P3   ok      ok rows=20 distinct_quotes=20 distinct_lines=20 out_of_word_range=0
P4   ok      ok checked=20 bad=0 first=0
P5   ok      ok manifest_entries=8 bad=0 first=0
P6   ok      ok rows=7 bad=0 first=0
P7   ok      ok source_lines=7 bad=0 first=0
P8   ok      ok index_rows=53 knowledge_files=53 bad=0 first=0
gate_exit=0
```

Two baseline facts drive everything in §4:

1. **V7 is already DEFECT at the freeze** — the round-46 defect this round's claim (a) exists to fix (frozen tags
   `both-print` and `toolchain` are violated by no committed case). A leg that is DEFECT at baseline cannot be
   observed to *flip* `ok→DEFECT`; the battery can only observe its **note** change. This structurally suppresses
   the V7 channel of the battery in this measurement.
2. **V8 is already DEFECT at the freeze** — `plans/order_check.py` reports
   `ORDER FAIL probe-executed-before-receipt hits=1` against the committed round-46 `control-c3-echo.txt`
   (the historical V8 defect). V8 is not a substantive leg and is insensitive to these mutants.

## 4. The 13-mutant battery

13 single-edit mutants of the six committed package-byte surfaces named by the frozen contract (capture ×3,
entry ×3, receipt ×3, dry table ×2, spec ×1, probe ×1). Each mutant is applied to a **fresh scratch copy** of the
frozen clone; the copy is byte-compared file-by-file against the pristine copy so the mutated surface is provably
exactly one file, and `git -C "$D" rev-parse --show-toplevel` is asserted to equal `$D` before any write.

| mutant | surface | single edit | **substantive leg flipped ok→DEFECT** | other leg/clause flipped | substantive leg *note* changed | mutated file |
|---|---|---|---|---|---|---|
| M01 | capture | grader's fixed point `42`→`267914297` | **V10, V12** | counter V1, gate P5 | — | `corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py` |
| M02 | capture | `task.toml` row dropped from `SHA256SUMS` | — | counter V1, gate P5 | — | `corpus/evidence/round46/tb2-polyglot-c-py/SHA256SUMS` |
| M03 | capture | comment line added to captured `README.md` | **V12** | counter V1, gate P4, gate P5 | — | `corpus/evidence/round46/tb2-polyglot-c-py/README.md` |
| M04 | entry | one `## Case table` row removed | **V9** | — | — | `corpus/knowledge/tb2-polyglot-c-py-grader.md` |
| M05 | entry | one `## Mechanism` row removed | **V10** | — | — | `corpus/knowledge/tb2-polyglot-c-py-grader.md` |
| M06 | entry | one `## Requirement map` row removed | — | — | V7 | `corpus/knowledge/tb2-polyglot-c-py-grader.md` |
| M07 | receipt | `nop` `observed=fail`→`observed=pass` | **V4, V9** | gate P2 | — | `corpus/evidence/round46/polyglot-c-py-probe.txt` |
| M08 | receipt | summary counts `7/11`→`8/10` | **V4** | gate P2 | — | `corpus/evidence/round46/polyglot-c-py-probe.txt` |
| M09 | receipt | one case's `violates=` list emptied | — | gate P2 | V7 | `corpus/evidence/round46/polyglot-c-py-probe.txt` |
| M10 | dry table | one `CASE` id renamed | **V4, V10** | counter V5 | — | `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` |
| M11 | dry table | one `TAG` instruction line moved (`7`→`8`) | — | counter V5 | V7 | `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` |
| M12 | spec | one row's `sha256` altered | **V3, V4, V9, V10, V12** | counter V1, V5, V6, V13 | V7 | `plans/pkg-spec-r46.json` |
| M13 | probe | comment line added to the probe | — | counter V5, gate P1 | — | `plans/polyglot_c_py_probe.py` |

### Counts against the frozen kill rule

- **Substantive-leg `ok→DEFECT` flips: 8/13** (M01, M03, M04, M05, M07, M08, M10, M12).
- **Frozen floor** `floor(13/2) = 6` → **8 ≥ 6, the battery clears the floor** against the committed base counter.
- Any counter leg or gate clause flipping `ok→DEFECT`: **12/13** (all but M06).
- Any detector output change at all (incl. note-only): **13/13**.
- Round-46's comparison point was **0/13** (`corpus/lessons/round-46-verifier-spotcheck.md:47` — *"improve mutation
  sensitivity (0/13 mutants killed)"*).

### Which leg flipped, verbatim (the killing note for each substantive flip)

```
M01  V10: mechanism_rows=18/18 bad=['nop:test_outputs.py capture not pinned', 'oracle-solve-sh:test_outputs.py capture n…
M01  V12: rows=7 defective=1 live=1 first=S166:capture_unresolved capture=0
M03  V12: rows=7 defective=1 live=1 first=S172:capture_unresolved capture=0
M04  V9 : case_rows=17/18 bad=['case table rows=17 receipt cases=18 equal=False']
M05  V10: mechanism_rows=17/18 bad=['mechanism rows=17 receipt cases=18 ids_equal=False']
M07  V4 : cases=18 mismatches_named=0/0 bad=['summary disagrees with the CASE lines', "match=yes on a mismatching case: …
M07  V9 : case_rows=18/18 bad=['case table rows=18 receipt cases=18 equal=False']
M08  V4 : cases=18 mismatches_named=0/0 bad=['summary disagrees with the CASE lines']
M10  V4 : cases=18 mismatches_named=0/0 bad=['case ids differ from the frozen table']
M10  V10: DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
M12  V3/V4/V9/V10/V12: package unreadable: plans/pkg-spec-r46.json is not at its freeze digest (receipt_sha256 masked)
```

### The three note-only mutants, verbatim (why they do not *flip* V7)

```
baseline V7: … "tags missing=['both-print', 'toolchain'] duplicated=0"
M06    V7: … "tags missing=['both-print', 'c-build', 'toolchain'] duplicated=0"
M09    V7: … 'single-file: cites no case or a case that does not violate it' …
M11    V7: … 'stdout-only: line 7 is not the frozen instruction.md:8' …
```

M06/M09/M11 are **detected** — the counter's V7 output demonstrably changes — but because V7 is *already* DEFECT at
the frozen base, they cannot be scored as an `ok→DEFECT` flip. This is a property of the base tree, not of the
mutants.

### Supplementary: V11 over the same trees (outside the scored battery)

```
baseline  V11 ok    states=60 grader_pass=15 grader_fail=45 disagree=0
M01       V11 DEFECT grader capture not at its frozen digest
M12       V11 DEFECT package unreadable: plans/pkg-spec-r46.json is not at its freeze digest (receipt_sha256 masked)
M02…M11, M13  V11 ok  states=60 grader_pass=15 grader_fail=45 disagree=0
```

### Supplementary probe M14 — a blind spot found outside the battery

A 14th probe (not part of the 13) edited **only** `plans/pkg-spec-r46.json`'s `receipt_sha256` value. Findings:

```
masked digest of committed spec            : 560c7bfb3f12fcfeaed6cb33ed3adc4b881b59b1c8f5ca9e3a094f10c1513f6e
counter's SPEC_SHA256 pin                   : 560c7bfb3f12fcfeaed6cb33ed3adc4b881b59b1c8f5ca9e3a094f10c1513f6e
masked digest after receipt_sha256 edit     : 560c7bfb3f12fcfeaed6cb33ed3adc4b881b59b1c8f5ca9e3a094f10c1513f6e
pin still holds after that edit             : True
M14 counter legs: every leg identical to baseline (V7/V8 the pre-existing defects only)
M14 gate with the COMMITTED spec, P10 disabled: P2 DEFECT (receipt_sha256 mismatched)
M14 gate with the counter's V2-style effective spec (receipt_sha256 := sha256(receipt)), P10 disabled: exit 0, all clauses ok
```

The counter masks the `receipt_sha256` field out of its own spec pin (`plans/round46_c3_verify.py:200`) and then
**rewrites** that field to the freshly computed receipt digest before invoking the gate
(`plans/round46_c3_verify.py:256` — `s["receipt_sha256"] = sha256(pkg.receipt) or "absent"`). Consequently the
gate's own `P2` receipt-digest clause can never fire through the counter's V2 path: the spec's `receipt_sha256`
pin is verified against itself, not against the receipt. A corrupted spec `receipt_sha256` is invisible to the
committed counter. This is exactly the gap the frozen delta (c) — V15, *"every frozen input digest resolves …
a missing/tamper-pinned input is a DEFECT of that leg"* — is written to close, so it is a live observation for the
stage-2 freeze, not a defect of the base counter.

### Consequences for the stage-2 freeze (reported, not acted on)

Three observations are for the L1 and are **not** acted on here (no predicate, kill rule, control or label was
re-frozen, weakened or re-labelled by this seat):

1. The frozen V14 rule counts a mutant "caught" only when it flips **one of V3/V4/V7/V9/V10/V12** `ok→DEFECT`
   (`plans/round-48-claims.md:106`). M02 (manifest row dropped) and M13 (probe byte changed) are detected — V1 and
   V5 flip for M02, V5 and gate P1 for M13 — but by legs outside that list. The delta (c) V15 would catch both
   classes ("frozen input digest resolves"), but **V15 is not in the substantive list the V14 rule names**, so
   under the frozen wording they would still count as survivors even though a leg reports them. The stage-2 freeze
   should decide explicitly whether V15's DEFECT counts as "caught" for V14.
2. Against the stage-1 base, V7 is red for both-print/toolchain, so V7 cannot carry a flip. The claims' stage-2
   amendment of the case table ("by adding or re-wording cases, never by re-wording tags — so all seven tags are
   violated by a committed case") is what makes V7 green at the landing tip; **if** that amendment lands and the
   v4 counter's V7 positive precondition check is implemented as frozen, then M06/M09/M11 would each flip V7
   `ok→DEFECT`, and the substantive count would rise from 8/13 to 11/13. This is **[INFERENCE]** about instruments
   that do not yet exist; it is **not** a measurement and must not be counted as one.
3. The frozen V14 rule should be read against the *landing* tree, not the stage-1 base. The battery as run here is
   a wave-1 pre-stage measurement of the committed base instruments; the scored V14 leg is the L1's to run against
   `plans/round48_c2_verify.py` at stage 2.

## 5. Exact commands run

All commands ran with `TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C2ExecMutBattery` and `cwd` = that scratch dir
(the fleet root is not a lane and is never used as a cwd for a writing command).

```bash
# clone at the frozen base (read-only against the lane; --shared, no mirror)
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" checkout -q a543d92083557dd9b33ee674e9b99b03411f80af
git -C "$S/lane" rev-parse --show-toplevel      # -> $S/lane   (asserted equal before any write)
git -C "$S/lane" rev-parse HEAD                  # -> a543d92083557dd9b33ee674e9b99b03411f80af

# baseline + battery
python3 mutbattery.py --lane "$S/lane" --work "$S/work/base" --out "$S/out/baseline.json"
python3 run_battery.py                            # 13 copies, 13 mutations, 13 measurements -> $S/out/M*.json, battery.json

# controls
python3 run_battery.py                            # (M00 control: pristine copy, zero edits -> zero flips)
python3 mutbattery.py --lane "$S/mutants/M14" …  # supplementary masked-spec probe
python3 plans/order_check.py --lane "$S/lane" --claims plans/round-46-claims.md \
        --receipt corpus/evidence/round46/polyglot-c-py-probe.txt

# digest facts
sha256sum plans/polyglot_c_py_probe.py plans/pkg-spec-r46.json plans/pkg_gate.py \
          corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt \
          corpus/evidence/round46/polyglot-c-py-probe.txt \
          corpus/knowledge/tb2-polyglot-c-py-grader.md plans/round46_c3_verify.py plans/order_check.py

# upstream re-open (sourced basis)
curl -sS --max-time 25 -o /tmp/tb2_test_outputs.py \
  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py
sha256sum /tmp/tb2_test_outputs.py   # -> b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec (== the capture pin)
```

**Lane discipline.** No git/jj mutating command was run anywhere; no commit, push, checkout of a sibling repo, or
write to `plans/*`, `corpus/*`, `SCORECARD.md`, `LOG.md`, `MANIFEST.json`, `.ufo/state` or `.scratch/`. The lane
is unchanged by this seat: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --name-only HEAD` → **0
lines**; the only lane-side writes are this report and its receipts directory. The scratch tree was removed
before this report was finalised (defect-of-own check: **no scratch left on disk**).

## 6. Harnesses (scratch-only, copied into the wave dir with the receipts)

| file | sha256 | purpose |
|---|---|---|
| `mutbattery.py` | `aed528fca0b6f215169e71d1f607150e0ad3b284314280633080387eb0c006f1` | runs the committed counter's leg set (minus V2, V11) and the gate with P10 disabled on one tree; emits JSON |
| `mutants.py` | `58edff3901a3336e9c69d11dfd03017bd2f1ff3363a1d69861022d5eba8a79cb` | authors the 13 single-edit mutants, each refusing to run on an ambiguous pattern |
| `run_battery.py` | `5ca42d126c8180cce1bc8d094c4c6a51e1cf876fa02420794cc27995bb082cbc` | copies the frozen clone per mutant, asserts `git rev-parse --show-toplevel` equals the copy, applies the mutation, byte-diffs every file, runs the detector, classifies the flip |

Receipts in this seat's directory: `baseline.json`, `M00.json` (no-op control: zero flips), `M01…M13.json`,
`M14.json` (supplementary probe), `battery.json` (classification), `v11-supplementary.json`,
`receipt-mutbattery.txt` (human-readable receipt, `REV` first), plus the three harnesses.

**Control M00** (pristine copy, zero edits) reproduced the baseline exactly: no leg flipped, no gate clause
flipped. The harness therefore attributes flips to mutations only.

## 7. Limits

1. **The scored counter does not exist yet.** `plans/round48_c2_verify.py` is absent at `a543d920`; this battery
   measures the committed base instruments the frozen contract imports. It does **not** establish the v4 counter's
   behaviour and does **not** admit or reject R48-C2.
2. **V2 and its P10 leg were not run**, by the frozen Q30 ordering; the gate was run in P10-disabled mode instead.
   A mutant that only the *fresh probe re-run* would catch is out of reach here (none of the 13 is of that kind).
3. **The base V7 is red**, which suppresses `ok→DEFECT` flips on the V7 channel (§3.1, §4). Three of the 13 are
   note-only detections for that reason.
4. **The base V8 is red** (historical pre-receipt P10 evidence committed under round-46) and is insensitive to all
   13; it is not a substantive leg.
5. **M13's byte class is the base probe** (`67a8f4a6…`). The hardened revision `22b7779e…` is not committed at
   the freeze (that is the wave-1 probe seat's item), so M13's coverage speaks to the base probe bytes.
6. **M12 is a blunt kill**: any change to the spec outside the masked `receipt_sha256` field breaks the spec digest
   pin, so every leg reports "package unreadable". It proves the pin binds, not that each leg independently
   re-derives the package.
7. **One `git` dependency:** V6 runs `scripts/sources-census.sh` and V8 runs `plans/order_check.py` against the
   copy's `.git` (an `alternates` pointer into the lane's object store, read-only). The lane's history was read,
   never written.
8. **V11 was measured outside the scored battery** (§2) and executed the captured grader on synthetic states in
   `bwrap`; no probe run and no graded case of the task.
9. No tool was installed or updated by this seat (nothing in the task needed one); the host pacman guard was
   respected — no pacman transaction was attempted.

## 8. Sources opened (URL / access date / located quote)

| # | source | access | located quote (≤25 words) |
|---|---|---|---|
| S1 | `plans/round-48-claims.md` (lane, `a543d920`) | 2026-10-27 | `:104-107` — *"one substantive leg (V3/V4/V7/V9/V10/V12) to DEFECT; fewer than `<N>/2` caught → the counter prints `MUTATION DEFECT`"* |
| S2 | `corpus/lessons/round-46-verifier-spotcheck.md` (lane) | 2026-10-27 | `:47` — *"improve mutation sensitivity (0/13 mutants killed). Keep the new knowledge unadmitted until the counter passes"* |
| S3 | `SCORECARD.md` (lane) | 2026-10-27 | `:2080-2081` — *"re-freeze C3's counter under Q40 (every frozen tag with a violating case; pre-receipt controls with the gate's P10 disabled)"* |
| S4 | `plans/round46_c3_verify.py` (lane) | 2026-10-27 | `:130` — *"SUBSTANTIVE = (\"V3\", \"V4\", \"V7\", \"V9\", \"V10\", \"V12\")"* |
| S5 | `plans/round46_c3_verify.py` (lane) | 2026-10-27 | `:200` — *"masked = re.sub(r'\"receipt_sha256\": \"[^\"]*\"', '\"receipt_sha256\": \"PENDING-STAGE-2\"',"* |
| S6 | `plans/round46_c3_verify.py` (lane) | 2026-10-27 | `:256` — *"s[\"receipt_sha256\"] = sha256(pkg.receipt) or \"absent\""* |
| S7 | `plans/pkg_gate.py` (lane) | 2026-10-27 | `:308` — *"if (n != \"P9\" or args.require_clean_tree) and (n != \"P10\" or args.rerun)]"* |
| S8 | `plans/polyglot_c_py_probe.py` (lane) | 2026-10-27 | `:451` — *"if a.dry:"* (the dry path prints the case table and returns; no case executes) |
| S9 | `plans/pkg-spec-r46.json` (lane) | 2026-10-27 | `"receipt_sha256"` — *"dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277"* |
| S10 | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py` | 2026-10-27 | `:27` — *"test_cases = [(42, \"267914296\"), (10, \"55\"), (0, \"0\")]"* (fetched sha256 `b94a7a98…81ddec` = the committed capture pin) |
| S11 | `/home/vgpnk/.omp/agent/RULES.md` (host) | 2026-10-27 | `:7` — *"Channel order: `sudo pacman -S --needed --noconfirm <pkg>` → `uv tool install <pkg>` →"* (pacman guard respected; nothing installed) |
| S12 | `.ufo/waves/round-46/w2/R46W2C3Mut.md` (lane, prior round's comparable battery) | 2026-10-27 | `:10` — *"V7 DEFECT (two unparsed requirement-map rows and missing tags `both-print`, `toolchain`); V8 DEFECT (`order_exit=1`)"* |

## 9. Verdict

Measured on the stage-1 freeze `a543d92083557dd9b33ee674e9b99b03411f80af`: the 13-mutant battery on the committed
C2 package bytes is killed **8/13** by a substantive leg flipping `ok→DEFECT` (V3/V4/V7/V9/V10/V12), against the
frozen floor `floor(13/2) = 6` — **the battery clears the floor** (round-46's comparison: 0/13). Twelve of the 13
flip at least one counter leg or gate clause; all 13 change the detector's output; the no-op control M00 changes
nothing. This is a **wave-1 pre-stage measurement of the committed base instruments**, not a scored R48-C2
admission: `plans/round48_c2_verify.py` does not exist at the freeze, the base V7 is red (suppressing the V7 flip
channel), and three findings are routed to the L1's stage-2 freeze — the V14 substantive-list vs V15 question
(M02/M13), the base-red-V7 caveat, and the M14 masked-`receipt_sha256` blind spot in the committed counter's V2
path. No R48-C1 or R48-C2 admission is claimed, and no predicate, kill rule, control or label was changed.

VERDICT: c2-mutant-battery-killed-8/13 (floor floor(13/2)=6 met against the committed base counter; not an admission)
