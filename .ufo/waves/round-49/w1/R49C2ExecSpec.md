# R49C2ExecSpec — round-49 C2 (coverage): `plans/pkg-spec-r49.json` draft + P10-disabled gate wrapper

Seat `R49C2ExecSpec` (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` **read-only**; the
only lane writes are this report and the sibling directory `.ufo/waves/round-49/w1/R49C2ExecSpec/` (transcribed
candidates + receipts). Scratch `S=/fast/scratch/hyaku/kengaku-r49/R49C2ExecSpec`, `TMPDIR=$S` for every command,
scratch tree removed before this seat yielded (see §9).

**Axes named before the work**

1. **spec fidelity** — does the r49 spec carry every r46 key and value that is not a stale pin, and do the new fill
   slots fail closed (a bare placeholder can never read as a pin)?
2. **ordering (Q30 / V8)** — can the three pre-receipt controls run the package gate with P10 *provably* disabled,
   and are their receipts clean under `plans/order_check.py`'s own regexes while the round-46 echo control is red?
3. **operability** — do both deliverables execute on this host at the frozen base, with a stable machine-checkable
   receipt line, and does each defence layer fail closed when its own negative control is applied?

**REV measured:** `9d2900af41e4d1fc6022eff99010436fde6dbd93` (the stage-1 freeze the item names). The scratch clone
`S/lane` is checked out at exactly this commit (`git -C "$S/lane" rev-parse HEAD` →
`9d2900af41e4d1fc6022eff99010436fde6dbd93`; `git -C "$S/lane" rev-parse --show-toplevel` →
`/fast/scratch/hyaku/kengaku-r49/R49C2ExecSpec/lane`; `git -C "$S/lane" status --porcelain` empty at the end).

**Stage-1 freeze verified before any measurement** (this is a spec/wrapper seat, so no scored counter or probe run
happened at all — see §7 limit 1):

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
commit
$ git -C … ls-tree 9d2900af plans/round-49-claims.md
100644 blob 3ad92f056155b5cc0c3e2a60068b6b3cecf0c21d	plans/round-49-claims.md
$ git -C … merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 af88aab193e6034cb9b386472064e3c18fa90128
STAGE1_ANCESTOR_OF_HEAD          (HEAD = af88aab1, the w1 dispatch commit)
$ sha256sum "$S/lane/plans/pkg_gate.py" "$S/lane/plans/polyglot_c_py_probe.py"
ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41  plans/pkg_gate.py
67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26  plans/polyglot_c_py_probe.py
```

Both base digests equal the r46 stage-2 pins (`plans/pkg-spec-r46.json` → `frozen_instruments`), so the freeze the
r49 claim re-pins from is the tree actually measured.

---

## 1. Deliverables

| file (wave dir) | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-49/w1/R49C2ExecSpec/pkg-spec-r49.json` | 2285 | `5ca998d13ed5e0317eacb8f29190acad03ea3ca195cdb7af324b9371bfef0f6f` |
| `.ufo/waves/round-49/w1/R49C2ExecSpec/pkg_gate_pre_receipt.py` | 9609 | `c49e2f4398d57e7ae052ab1b58bd2d9994411f00fecd6cafd00ddd132fe1e259` |
| `.ufo/waves/round-49/w1/R49C2ExecSpec/spec-pins-filled-control.json` | — | `646a271c935ed63df8dca5eb8bc009c35264d32934c77a43e7e5944cd71ef8d3` |

The digests above are those of the files that were measured: the wave-dir copies are byte-identical to the scratch
candidates (`sha256sum` of both paths printed the same two digests), and `python3 -m py_compile` on the wave-dir copy
exits 0. `MANIFEST.sha256` in the same directory pins the candidates and every receipt cited below.

Copy targets when the L1 lands them: `plans/pkg-spec-r49.json`, `plans/pkg_gate_pre_receipt.py` (two new files; no
frozen byte moves — `plans/pkg_gate.py` is untouched and stays at `ea638822…`).

### 1.1 What the spec changes against `plans/pkg-spec-r46.json`

`json` diff, key by key (script output, verbatim):

```
new keys: ['capture_dir', 'claims', 'dry', 'dry_sha256', 'entry', 'entry_rules', 'frozen_instruments',
           'knowledge_glob', 'name', 'probe_cmd', 'raw_base', 'readme', 'receipt', 'receipt_sha256',
           'rows', 'sources']
DIFF dry_sha256 -> (None, '<PIN:stage-2>')
DIFF dry -> (None, 'corpus/evidence/round49/polyglot-c-py-dry-cases.txt')
DIFF claims -> (None, 'plans/round-49-claims.md')
DIFF frozen_instruments -> ({'plans/pkg_gate.py': 'ea638822…', 'plans/polyglot_c_py_probe.py': '67a8f4a6…'},
                            {'plans/pkg_gate.py': 'ea638822…', 'plans/polyglot_c_py_probe.py': '<PIN:stage-2>'})
DIFF name -> ('round-46 tb2-polyglot-c-py package', 'round-49 tb2-polyglot-c-py package (Q40 re-frozen counter)')
DIFF receipt_sha256 -> ('dd0e3546…c277', '<PIN:stage-3>')
DIFF receipt -> ('corpus/evidence/round46/polyglot-c-py-probe.txt',
                 'corpus/evidence/round49/polyglot-c-py-probe.txt')
```

Everything else is **identical**, including `rows` (S166–S172 capture/upstream/sha256), `entry_rules`,
`capture_dir`, `probe_cmd`, `source`/`readme`/`knowledge_glob`/`raw_base`. Nothing was re-derived; the seven row
digests are the r46 pins, matching the eight-entry `SHA256SUMS` at the frozen base.

### 1.2 Fill slots (stage 2 / stage 3), and why a placeholder cannot pass as a pin

| slot | path | fill at | convention |
|---|---|---|---|
| probe-v2 digest | `frozen_instruments["plans/polyglot_c_py_probe.py"]` | stage 2 (with the amended probe) | `<PIN:stage-2>` today |
| new dry-table digest | `dry_sha256` (+ `dry` path) | stage 2 (with the amended case table) | `<PIN:stage-2>` today |
| new receipt | `receipt` = `corpus/evidence/round49/polyglot-c-py-probe.txt` | stage 3 (first full probe run) | path is final now |
| new receipt digest | `receipt_sha256` | stage 3, same commit as the receipt | `<PIN:stage-3>` today |

The gate's `c_instruments` compares `sha256(file)` to the pin, and `c_receipt` compares to `receipt_sha256`; a
`"<PIN:…>"` string is not a digest, so **every unfilled slot is a DEFECT, never a pass** (measured in §3.1: P1 and
P2 defect on the placeholders). This mirrors the round-46 counter's `ready(pin)` convention (`not pin.startswith("<")`),
so a counter that masks the receipt pin for its own `SPEC_SHA256` can keep the same convention.

`dry` / `dry_sha256` are new spec keys. The package gate does not read them (it has no dry-table clause); they exist
so the r49 counter can resolve the amended dry table and its pin from one place instead of a hardcoded constant. The
counter `plans/round49_c2_verify.py` is another seat's file and did not exist in the base tree, so **this seat could
not measure whether that counter consumes the keys** — it is the L1's call to make the counter read them (or to keep
its own `DRY_REL`/`DRY_SHA256` constants, as `plans/round46_c3_verify.py` does). `claims` is likewise advisory (the
filler spec's convention) and is read by `order_check.py` callers, not by the gate.

---

## 2. The P10-disabled wrapper: design

`plans/pkg_gate_pre_receipt.py` adds a new file and changes no frozen byte. Why a wrapper and not a flag: the gate's
bytes are pinned twice (spec `frozen_instruments`, and `plans/round46_c3_verify.py` `GATE_SHA256`), so editing them
breaks the gate's own P1 clause and the counter's freeze check. The switch already exists inside the gate —
`cmd_package` builds `wanted` with `(n != "P10" or args.rerun)` — so the round-46 V8 defect was that the controls
passed `--rerun`, not that the gate lacked a switch.

| layer | mechanism (in the delivered file) |
|---|---|
| L1 | argv is `[sys.executable, gate, "package", "--root", root, "--spec", eff_spec]` (+ `--require-clean-tree` on request); `--rerun` is never appended, and a defensive `if "--rerun" in cmd: raise SetupError` guards the invariant. |
| L2 | the effective spec written to `--work` copies the spec with `probe_cmd = [<absolute sentinel path>]`; the sentinel prints exactly `P10-PROBE-DISABLED` and exits 3. |
| L3 | the gate's stdout is scanned for `^\s*(?:gate:\s*)?P10\s+(DEFECT|ok)\b` lines and for the sentinel token; any hit prints `GATE ORDER VIOLATION …` and exits 2. |
| L4 | the gate's sha256 must equal its frozen pin (`--gate-sha256`, else `frozen_instruments["plans/pkg_gate.py"]`); a missing/placeholder pin is a setup error, a mismatch prints `gate is not at its frozen pin: … sha256=… want=…`. |
| extra | the spec's probe file is stamped (sha256 + `mtime_ns`) before and after the gate run; a change during a pre-receipt run is an ordering violation (exit 2). This substantiates the `probe_executed=no` claim instead of only asserting it. |

Fixed output (the whole point: committable as a control receipt):

```
GATE MODE pre-receipt p10=disabled
GATE P10 disabled=1 probe_executed=no sentinel=<path> probe_stamp=<unchanged|absent|missing>
GATE SPEC effective=<spec> probe=<original probe_cmd[0]> gate=<gate path> gate_sha256=<digest>
<the gate's own clause lines, verbatim>
[GATE ORDER VIOLATION <detail>]
GATE RESULT accept|reject|setup-error
```

Exit: 0 accept · 1 reject · 2 setup/ordering error. No `CASE … observed=` line is ever printed. `--work` is
required, so no fixed path (and no `/tmp`) is baked in; the sentinel and effective spec live where the caller says.

---

## 3. Measured controls (all inside `S`, all read-only against the clone)

Every command below is `python3 <wrapper> …` with the wave/scratch copies of the two candidates; full stdout is in
the receipt file named in each heading, in the wave dir.

### 3.1 The draft spec fails closed on exactly its three unfilled/stage-2 items — `receipt-draft.txt`

```
$ python3 candidate/plans/pkg_gate_pre_receipt.py --root "$S/lane" \
      --spec "$S/candidate/plans/pkg-spec-r49.json" --work "$S/work/draft"
GATE MODE pre-receipt p10=disabled
GATE P10 disabled=1 probe_executed=no sentinel=…/work/draft/p10-disabled-sentinel.py probe_stamp=unchanged
GATE SPEC effective=…/work/draft/spec-p10-disabled.json probe=plans/polyglot_c_py_probe.py gate=…/lane/plans/pkg_gate.py gate_sha256=ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41
P1 DEFECT pinned=2 mismatched=['plans/polyglot_c_py_probe.py']
P2 DEFECT receipt unreadable: corpus/evidence/round49/polyglot-c-py-probe.txt
P3 ok rows=20 distinct_quotes=20 distinct_lines=20 out_of_word_range=0
P4 ok checked=20 bad=0 first=0
P5 ok manifest_entries=8 bad=0 first=0
P6 ok rows=7 bad=0 first=0
P7 ok source_lines=7 bad=0 first=0
P8 DEFECT index_rows=53 knowledge_files=53 bad=1 first=no coverage bullet naming the entry and its receipt
defects=3
GATE RESULT reject
exit=1
```

P1 and P2 are the stage-2/stage-3 slots doing their job. **P8 is a real stage-2 consequence, not a placeholder** —
see §5. P3–P7 (quote shape, quote verbatim, captures, SOURCES rows, provenance) pass unchanged, i.e. the draft's
static content is accepted by the same frozen gate on the same tree.

### 3.2 The same spec with the three slots filled from base values is accepted — `receipt-pins.txt`

Control spec `spec-pins-filled-control.json` = the draft with `receipt` → `corpus/evidence/round46/polyglot-c-py-probe.txt`,
`receipt_sha256` → `dd0e3546…c277`, probe pin → `67a8f4a6…` (all three are the base-tree values; the `dry` slots stay
placeholders because the gate never reads them):

```
P1 ok pinned=2 mismatched=0
P2 ok receipt_sha256=pinned
P8 ok index_rows=53 knowledge_files=53 bad=0 first=0
P9 ok untracked=0 first=0
defects=0
GATE RESULT accept
exit=0
```

This is the spec-shape control: **the draft is coherent with the real tree, and its only rejects are the frozen
fill slots plus the README bullet.** It also exercises the `--require-clean-tree` pass-through into P9.

### 3.3 The round-46 filler control package — `receipt-filler.txt`

```
$ python3 candidate/plans/pkg_gate_pre_receipt.py --root "$S/lane" \
      --spec "$S/lane/plans/filler46/pkg-spec-filler.json" --gate-sha256 ea638822… \
      --work "$S/work/filler"
GATE P10 disabled=1 probe_executed=no sentinel=…/work/filler/p10-disabled-sentinel.py probe_stamp=missing
P1 DEFECT pinned=0 mismatched=0
P2 ok receipt_sha256=pinned
P3 DEFECT rows=7 distinct_quotes=1 distinct_lines=7 out_of_word_range=0
P4 DEFECT checked=7 bad=7 first=test_outputs.py:3: quote not verbatim there
P5 ok manifest_entries=8 bad=0 first=0
P6 DEFECT rows=7 bad=8 first=S166: teaches words=3
P7 ok source_lines=7 bad=0 first=0
P8 DEFECT index_rows=53 knowledge_files=2 bad=3 first=index rows for knowledge/entry.md=0
defects=5
GATE RESULT reject
exit=1
```

`defects=5` reproduces the round-48 measurement of the same control through the same mode, with **no P10 line**.

### 3.4 L2, with a *readable* receipt: a mis-wired `--rerun` runs the sentinel, never the probe — `gate-rerun2.txt`

The gate's `c_rerun` reads the receipt first, so on an unreadable receipt even `--rerun` cannot reach the probe
(measured: `P10 DEFECT receipt unreadable`, `defects=4`). The decisive negative therefore uses the pins-filled
effective spec (readable round-46 receipt) with the sentinel `probe_cmd` the wrapper wrote:

```
$ PYTHONPATH="$S/work/stub" python3 "$S/lane/plans/pkg_gate.py" package \
      --root "$S/lane" --spec "$S/work/pins/spec-p10-disabled.json" --rerun
P10 DEFECT fresh probe exit=3 stderr=''
defects=1
```

(`$S/work/stub/Bio/__init__.py` is an empty stub so `c_rerun` takes its `[sys.executable] + probe` branch instead of
`uv run … --with biopython==1.85`.) The other interpreter branch was measured directly too:

```
$ uv run --no-project --with biopython==1.85 python3 "$S/work/draft/p10-disabled-sentinel.py"
P10-PROBE-DISABLED
uv_sentinel_exit=3
```

Both c_rerun branches hand the sentinel to a Python interpreter, so `--rerun` can never execute the frozen probe in
this mode. The sentinel standalone prints `P10-PROBE-DISABLED` and exits `3`.

### 3.5 L4: a doctored gate is refused — `receipt-l4.txt`

```
$ python3 candidate/plans/pkg_gate_pre_receipt.py --root "$S/lane" --spec "$S/candidate/plans/pkg-spec-r49.json" \
      --gate "$S/work/doctored_gate.py" --work "$S/work/neg"
GATE SETUP gate is not at its frozen pin: /…/work/doctored_gate.py sha256=b21821ffc3f2c0d9fbc539ff45fc1b6b786a3e85daed7b36211de0e7ec3f3aee want=ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41
GATE RESULT setup-error
exit=2
```

### 3.6 L3 and the probe stamp, each with its own negative control

| control | receipt | observed |
|---|---|---|
| a gate that prints `P10 ok probe_rerun=byte-equal bytes=1` | `receipt-l3a.txt` | `GATE ORDER VIOLATION P10 clause ran: lines=1 first='P10 ok probe_rerun=byte-equal bytes=1'`, `GATE RESULT setup-error`, exit 2 |
| a gate that prints the sentinel token | `receipt-l3b.txt` | `GATE ORDER VIOLATION P10 sentinel executed: lines=1 first='P10-PROBE-DISABLED'`, exit 2 |
| a gate that appends a byte to the probe under `--root` | `receipt-stamp.txt` | `GATE ORDER VIOLATION probe bytes moved during a pre-receipt run: 67a8f4a68fcd->ebb1eaaa4857`, exit 2 |
| a gate that exits 2 | `receipt-exit2.txt` | `GATE SETUP gate_exit=2 stderr=''`, `GATE RESULT setup-error`, exit 2 |
| a spec with no gate pin and no `--gate-sha256` | `receipt-nopin.txt` | `GATE SETUP no frozen gate pin: --gate-sha256 not given and frozen_instruments['plans/pkg_gate.py']=None`, exit 2 |

These are negative controls of the *layers*, run against shim gates whose own digests were passed as `--gate-sha256`
(which is the only way to legitimately clear L4 for a deliberately-wrong gate). Each layer fails closed.

### 3.7 The receipts are clean under `plans/order_check.py`'s own scanner

`blob_hits` imported from the frozen `plans/order_check.py` and replayed over every wrapper receipt, plus the
round-46 echo control as contrast:

```
receipt-draft.txt            hits=[]
receipt-exit2.txt            hits=[]
receipt-filler.txt           hits=[]
receipt-l3a.txt              hits=[(5, 'gate-p10', 'P10 ok probe_rerun=byte-equal bytes=1')]
receipt-l3b.txt              hits=[]
receipt-l4.txt               hits=[]
receipt-nopin.txt            hits=[]
receipt-pins.txt             hits=[]
receipt-stamp.txt            hits=[]
control-c3-echo.txt          hits=[(15, 'gate-p10', 'gate: P10 DEFECT fresh probe output is not byte-equal to the receipt')]
```

The round-46 echo control trips the order gate precisely because its gate ran P10 before the receipt was committed;
every mode receipt is clean. `receipt-l3a.txt` is **intentionally** red — it is the receipt of a gate that printed a
P10 line, so order-check red is the correct verdict and it must never be committed under `.ufo/waves/round-49/claims/`.
That is why the L3a/L3b shim receipts are evidence for this report and not claim receipts.

---

## 4. Commands run (exact)

```
mkdir -p /fast/scratch/hyaku/kengaku-r49/R49C2ExecSpec && export TMPDIR=…
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" checkout --detach 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C "$S/lane" rev-parse --show-toplevel ; git -C "$S/lane" rev-parse HEAD ; git -C "$S/lane" status --porcelain
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af… ; ls-tree 9d2900af plans/
git -C … merge-base --is-ancestor 9d2900af… af88aab1…
sha256sum "$S/lane/plans/pkg_gate.py" "$S/lane/plans/polyglot_c_py_probe.py"
python3 -V ; python3 -c "import Bio"
python3 -m py_compile candidate/plans/pkg_gate_pre_receipt.py
python3 - <<'PY'   # json key diff: candidate/plans/pkg-spec-r49.json vs lane/plans/pkg-spec-r46.json
python3 candidate/plans/pkg_gate_pre_receipt.py --root "$S/lane" --spec … --work "$S/work/draft"
python3 candidate/plans/pkg_gate_pre_receipt.py --root "$S/lane" --spec "$S/work/spec-pins-filled.json" --work "$S/work/pins" --require-clean-tree
python3 candidate/plans/pkg_gate_pre_receipt.py --root "$S/lane" --spec "$S/lane/plans/filler46/pkg-spec-filler.json" --gate-sha256 ea638822… --work "$S/work/filler"
PYTHONPATH="$S/work/stub" python3 "$S/lane/plans/pkg_gate.py" package --root "$S/lane" --spec "$S/work/draft/spec-p10-disabled.json" --rerun
PYTHONPATH="$S/work/stub" python3 "$S/lane/plans/pkg_gate.py" package --root "$S/lane" --spec "$S/work/pins/spec-p10-disabled.json" --rerun
python3 "$S/work/draft/p10-disabled-sentinel.py"
uv run --no-project --with biopython==1.85 python3 "$S/work/draft/p10-disabled-sentinel.py"
python3 candidate/plans/pkg_gate_pre_receipt.py --root "$S/lane" --spec … --gate "$S/work/doctored_gate.py" --work "$S/work/neg"
python3 candidate/plans/pkg_gate_pre_receipt.py … --gate "$S/work/shim_{p10,sentinel,touch,exit2}.py" --gate-sha256 <shim digest> …
python3 - <<'PY'   # order_check.blob_hits replay over the receipts + the round-46 echo control
```

Every fixture Git call used `git -C "$S/lane"` and the toplevel was asserted to be `$S/lane` before any write; the
clone was never written to (no file was installed into it — all gate runs read it, and the shim probes ran against
copies in `$S/work` and `$S/fakeroot`), never committed, pushed or otherwise mutated. `git -C "$S/lane" status
--porcelain` was empty at the end. The live lane was only read (`git status` / `git log` / `ls-tree`): the two
porcelain entries in it are `.ufo/waves/round-49/w1.ready.dispatched` and `.ufo/waves/round-49/w1/`, both wave
artifacts written by other seats, not this one.

---

## 5. Finding for the L1: the new receipt path forces a stage-2 `corpus/README.md` edit (gate P8)

`c_readme` requires a bullet that starts `- `, contains the entry's file name **and** `spec["receipt"]`
minus its first path component. With `receipt = corpus/evidence/round49/polyglot-c-py-probe.txt` that fragment is
`evidence/round49/polyglot-c-py-probe.txt`. At the frozen base the only bullet naming the receipt names the round-46
path (`corpus/README.md:308`, `… probe `plans/polyglot_c_py_probe.py`, receipt
`evidence/round46/polyglot-c-py-probe.txt` …`), so P8 defects — measured in §3.1, and it is the *only* defect besides
the two intended slots.

Consequence: whichever way the freeze is honoured, the stage-2 (or stage-3) commit must either
(a) update that coverage bullet to the round-49 receipt path, or (b) keep the round-46 receipt path in the spec.
The frozen claims name `corpus/evidence/round49/polyglot-c-py-probe.txt` as the new receipt, so (a) is the path
consistent with the freeze; the README edit is a production-file change and therefore the L1's, not this seat's.
`corpus/README.md` is not in the claims' C2 Separability list, so it is worth naming in the stage-2 amendment
paragraph for the closure reviewer.

Also verified absent at the frozen base (so the stage-2/stage-3 landings are genuinely new paths):
`corpus/evidence/round49/` and `plans/mutants49/`.

---

## 6. Sources opened (§2b)

No network source was opened by this seat: the item's deliverables are two files whose every input is in the frozen
lane tree, and the spec's seven row digests were carried over verbatim from `plans/pkg-spec-r46.json` (which the
round-48 spot-check already re-opened against the pinned capture). Lane paths read (all read-only, all at
`9d2900af`): `plans/round-49-claims.md`, `corpus/lessons/round-48-verifier-spotcheck.md`,
`corpus/lessons/round-48.md`, `.ufo/waves/round-48/w1/R48C2ExecProbe.md`,
`plans/pkg-spec-r46.json`, `plans/pkg_gate.py`, `plans/order_check.py`, `plans/round46_c3_verify.py`,
`plans/filler46/pkg-spec-filler.json`, `corpus/knowledge/tb2-polyglot-c-py-grader.md` (head),
`corpus/README.md` (index + coverage bullets), `corpus/evidence/round46/tb2-polyglot-c-py/SHA256SUMS`.

---

## 7. Limits

1. **No scored run of any kind.** No counter (`plans/round49_c2_verify.py` does not exist yet), no full probe run,
   no `--rerun` through the wrapper, and the probe was never executed — the sentinel runs in its place in every
   measurement. Nothing here admits R49-C2 or claims any V-leg result.
2. **P10 is proven disabled for the gate invocation, not for an attacker.** L1–L4 make an accidental `--rerun` and a
   doctored gate both fail closed; they are not a sandbox against a caller who deliberately reimplements the gate.
3. **The draft spec's placeholders are by design unfilled.** The accept control in §3.2 substitutes base-tree values
   for the three slots; it proves spec shape, not that the stage-2 probe/dry pins will be correct.
4. **`dry`/`dry_sha256` and `claims` are inert for the gate.** Their consumer is the r49 counter (another seat's
   file), so their usefulness is unverified from here (§1.2).
5. **The probe-stamp layer compares sha256 + `mtime_ns`.** A run that rewrites the probe with identical bytes and
   then restores the original mtime would evade it; that is outside the failure mode it targets (a probe *execution*
   writing nothing) and the digest comparison catches byte changes.
6. **`--gate-sha256` is a caller-supplied pin** used only where a control package's spec has no frozen instruments
   (the filler spec). For the real package the spec pin is authoritative; if both are absent the mode refuses to run.
7. **Stage-1 freeze check covers the freezes, not the claims' satisfiability.** The V7/V15 preconditions and the
   mutation floors are other seats' items; this seat's measurement stops at the spec/wrapper boundary.

**Tooling record:** no tool was installed or upgraded; no pacman transaction was attempted. `uv` (already at
`/home/vgpnk/.local/bin/uv`) was used once to prove the sentinel runs on `c_rerun`'s `uv run --no-project --with
biopython==1.85 python3` branch; that built `biopython==1.85` (+ `numpy` dependency) into uv's own cache, not into
the project or any PATH directory. `~/.local/bin` was not written.

## 8. Blockers

None for this seat's item. Two deliverables exist, compile, and are measured at the frozen base; the only open
consequence is §5 (the README bullet), which is the L1's stage-2 edit.

## 9. Scratch cleanup

`S=/fast/scratch/hyaku/kengaku-r49/R49C2ExecSpec` was removed with `rm -rf` after every receipt cited here was
copied into `.ufo/waves/round-49/w1/R49C2ExecSpec/` and its digest verified (`MANIFEST.sha256`). No scratch tree is
left on disk; no `/tmp` path is cited anywhere in this report as evidence (the `/tmp`-shaped paths in the quoted
gate output are the *gate's* own `HOME=/tmp` sandbox env, not files this seat wrote).

VERDICT: spec-draft-r49-shipped-with-three-fail-closed-fill-slots (probe-v2 + dry digest at stage 2, receipt + digest at stage 3) and p10-disabled-wrapper-shipped; wrapper accepts a pins-filled spec (defects=0), rejects unfilled/stale ones, refuses a doctored gate, catches P10/sentinel/probe-movement violations, and every mode receipt is clean under order_check's own scanner while the round-46 echo control is red; README coverage bullet must move at stage 2 for gate P8; no scored run, no probe execution, no admission claimed
