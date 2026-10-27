# R48C2ExecProbe — round-48 C2 (coverage): hardened probe integration candidate + P10-disabled gate mode

Seat `R48C2ExecProbe` (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` **read-only**; no
lane file was written except this report. Scratch `S=/fast/scratch/hyaku/kengaku-r48/R48C2ExecProbe` (NVMe),
`TMPDIR=$S` for every command; scratch tree removed at the end of this wave.

**Axes named before the work** (per the seat's item):

1. **coverage** — does the hardened probe candidate actually exercise every frozen case shape, and can the package
   gate be run on the pre-receipt controls without executing the frozen probe?
2. **freeze integrity** — is the artifact that would be integrated at the digest the frozen claims name, and does the
   integration preserve the frozen pins (spec pin, receipt pin, dry-table pin)?
3. **operability** — do the permitted pre-stage-2 modes (`--dry`, `--stage-check`) run on this host today, and does the
   P10-disabled control mode execute without touching the probe?

**REV measured:** `a543d92083557dd9b33ee674e9b99b03411f80af` (the stage-1 freeze commit named by the item; the
scratch clone `S/lane` is checked out at exactly this commit, `git -C "$S/lane" rev-parse HEAD` →
`a543d92083557dd9b33ee674e9b99b03411f80af`, `git -C "$S/lane" rev-parse --show-toplevel` →
`/fast/scratch/hyaku/kengaku-r48/R48C2ExecProbe/lane`).

**No scored run was made.** The stage-1 freeze exists in the committed lane tree at `a543d920` (`git ls-tree
a543d920 plans/round-48-claims.md` → `100644 blob 3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5`) and predates every
measurement here. Only `--dry` and `--stage-check` were run (both permitted by the Q30 ordering rule), plus gate runs
in a **P10-disabled** mode that never executes the probe. The full probe run was **not** performed: the item forbids
it, and the C2 ordering rule forbids it before the stage-2 commit.

---

## 1. Deliverables (absolute paths)

| file | bytes | sha256 |
|---|---|---|
| `S/candidate/plans/polyglot_c_py_probe.py` | 31355 | `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d` |
| `S/candidate/plans/pkg_gate_pre_receipt.py` | 7030 | `03785e039b5606d6d90da3c17430352387622a8cd002e95f9a6e3b46b48deeae` |

`S/candidate/plans/polyglot_c_py_probe.py` is the **verbatim** integration candidate for `plans/polyglot_c_py_probe.py`.
It is byte-identical to the wave artifact the frozen claim names:

```
$ A=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py
$ cp -p "$A" "$S/candidate/plans/polyglot_c_py_probe.py"
$ cmp "$A" "$S/candidate/plans/polyglot_c_py_probe.py" && echo "cmp: IDENTICAL"
cmp: IDENTICAL
$ sha256sum "$A" "$S/candidate/plans/polyglot_c_py_probe.py"
22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d  .../R46ExecC3Probe/polyglot_c_py_probe.py
22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d  .../R48C2ExecProbe/candidate/plans/polyglot_c_py_probe.py
```

**Digest matches the frozen claim exactly** (`plans/round-48-claims.md` §C2 Surface: sha256
`22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d`). The artifact is committed in the lane at the
stage-1 freeze: `git ls-tree a543d920 .ufo/waves/round-46/w1/R46ExecC3Probe/` →
`100755 blob 5a89786ac2681893fd63ac629a818810620601bd  .../polyglot_c_py_probe.py`.

**Landing it verbatim breaks a frozen pin.** The committed lane currently holds the *unhardened* revision at
`plans/polyglot_c_py_probe.py`, digest `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26` (27966 B),
and both `plans/pkg-spec-r46.json` (`frozen_instruments`) and `plans/round46_c3_verify.py` (`PROBE_SHA256`, line 121)
pin that digest. Landing `22b7779e…` moves the probe digest, so those pins (and `SPEC_SHA256`) must move in the same
stage-2 commit, and the receipt must be re-run and re-pinned because the two revisions do **not** produce the same
receipt (see §3). This is a stage-2 literal fill, which the frozen claims permit; it is **not** a predicate change.

---

## 2. The P10-disabled gate mode (design + candidate)

**Why a wrapper and not a flag on `plans/pkg_gate.py`.** The gate is a frozen instrument, pinned twice
(`plans/pkg-spec-r46.json` → `frozen_instruments["plans/pkg_gate.py"] = ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`
and `plans/round46_c3_verify.py:119` → the same digest, commented *"round-45 bytes, unedited"*). Editing its bytes
breaks the gate's own **P1** clause and the counter's **V2** freeze check at once, and moving a frozen pin after a
seat has scored is forbidden. A wrapper adds a new file and changes no frozen byte.

**The switch already exists inside the gate.** `cmd_package` keeps the P10 clause only when `--rerun` is passed
(`plans/pkg_gate.py`: `wanted = [... if (n != "P9" or args.require_clean_tree) and (n != "P10" or args.rerun)]`).
P10 = `c_rerun` = the fresh probe re-run byte-compared against the receipt. The round-46 **V8** defect was not that
the gate lacks a switch — it was that the pre-receipt controls ran the gate **with** `--rerun`, so the frozen probe
executed before its receipt was committed.

**Candidate:** `S/candidate/plans/pkg_gate_pre_receipt.py` — four defence layers, each checkable from the receipt alone:

| layer | mechanism |
|---|---|
| L1 | `--rerun` is **never** passed to the gate, so `c_rerun` is not in the clause list. |
| L2 | The effective spec handed to the gate has `probe_cmd` replaced by a **sentinel** that prints `P10-PROBE-DISABLED` and exits 3. If a mis-wired `--rerun` ever reached the gate, the sentinel runs instead of the frozen probe — the probe cannot execute, and the sentinel's line is visible in stdout. |
| L3 | The wrapper asserts the gate's stdout contains **no** line beginning `P10` and **no** sentinel line. A violation is a setup error (exit 2), never a pass. |
| L4 | The wrapper asserts the gate file's sha256 equals the spec's frozen pin for it, so the mode cannot be run against a doctored gate. |

Stable, machine-checkable output (safe to commit as a control receipt):

```
GATE MODE pre-receipt p10=disabled
GATE P10 disabled=1 probe_executed=no sentinel=<path>
<the gate's own clause lines, verbatim>
GATE RESULT accept|reject|setup-error
```

Exit: 0 accept · 1 reject (the gate found a defect) · 2 setup/ordering error.

### 2.1 Measured on the scratch clone at the frozen base

```
$ python3 candidate/plans/pkg_gate_pre_receipt.py --root "$S/lane" \
      --spec "$S/lane/plans/pkg-spec-r46.json" --work "$S/work/pre"
GATE MODE pre-receipt p10=disabled
GATE P10 disabled=1 probe_executed=no sentinel=/fast/scratch/hyaku/kengaku-r48/R48C2ExecProbe/work/pre/p10-disabled-sentinel.py
P1 DEFECT pinned=2 mismatched=['plans/polyglot_c_py_probe.py']
P2 ok receipt_sha256=pinned
P3 ok rows=20 distinct_quotes=20 distinct_lines=20 out_of_word_range=0
P4 ok checked=20 bad=0 first=0
P5 ok manifest_entries=8 bad=0 first=0
P6 ok rows=7 bad=0 first=0
P7 ok source_lines=7 bad=0 first=0
P8 ok index_rows=53 knowledge_files=53 bad=0 first=0
defects=1
GATE RESULT reject
exit=1
```

The single **P1 DEFECT** is the expected consequence of the candidate probe being installed in the clone (the spec
still pins the old digest) — the wrapper correctly reports it rather than hiding it. **No `P10` line was printed and
the probe never executed.**

### 2.2 L2 verified: a mis-wired `--rerun` hits the sentinel, not the probe

```
$ python3 "$S/lane/plans/pkg_gate.py" package --root "$S/lane" --spec "$S/work/pre/spec-sentinel.json" --rerun
...
P10 DEFECT fresh probe exit=3 stderr=''
defects=2

$ python3 "$S/work/pre/p10-disabled-sentinel.py"
P10-PROBE-DISABLED
sentinel exit=3
```

### 2.3 L4 verified: a doctored gate is refused

```
$ python3 candidate/plans/pkg_gate_pre_receipt.py --root "$S/lane" \
      --spec "$S/lane/plans/pkg-spec-r46.json" --gate "$S/work/doctored_gate.py" --work "$S/work/neg"
setup: gate is not at its frozen pin: plans/pkg_gate.py sha256=5e7fa1d639e22a63909e45e58f9e404a6be4bed5db2e56250a007356b6d9e56b want=ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41
GATE RESULT setup-error
exit=2
```

### 2.4 The V8 fix, measured against `plans/order_check.py`

`plans/order_check.py` scans every committed blob under `.ufo/waves/round-NN/claims/` for a gate `P10` line whose
detail is anything other than `receipt unreadable`, or a receipt-shaped `CASE … observed=` line. Replaying its exact
regexes (`GATE_P10`, `CASE_LINE`, `EXECUTED_EXCUSE`, lines 53–60) over the two receipts:

```
round-46 echo control receipt hits: [(15, 'gate-p10', 'gate: P10 DEFECT fresh probe output is not byte-equal to the receipt')]
P10-disabled receipt hits: []
```

The round-46 `control-c3-echo.txt` trips the order gate precisely because its gate ran P10 before the receipt was
committed. The P10-disabled receipt trips nothing. **That is the V8 fix, measured.**

The wrapper also works on the filler control package (`plans/filler46/pkg-spec-filler.json`) → `defects=5`,
`GATE RESULT reject`, exit 1, still with no `P10` line.

---

## 3. Two defects measured in the hardened `22b7779e…` artifact

Both defects live in the **grade** path, so **neither is visible in `--dry` or `--stage-check`**. Both are measured,
not inferred.

### 3.1 The grade path never runs the recipe (the sandbox hardening broke the case recipes)

The hardened harness guards the seed/recipe scripts with `if mode in ("stage", "recipe"):`
(`polyglot_c_py_probe.py:322`), but `run_case()` invokes the harness with mode **`"all"`** for grading
(`polyglot_c_py_probe.py:442`: `return harness(cap, work, "stage" if mode == "stage" else "all")`). Mode `"all"` is
not in that tuple, so it falls straight through to the grading legs: **`/seed.sh` and `/recipe.sh` never execute and
`/app/polyglot` is never created.** The old revision had no such mode — it ran `"recipe"` and then two `"grade"`
invocations over a host-bound `/app`, so the recipe ran.

Measured with a **stub** grader (the captured `test_outputs.py` was never imported in this experiment):

```
mode=all     -> grader sees /app/polyglot: exists=False names=None   (recipe never ran)
mode=recipe  -> STAGE seed rc=0 / STAGE recipe rc=0 / STAGE dir=main.py.c / STAGE file=bytes=2
mode=stage   -> STAGE seed rc=0 / STAGE recipe rc=0 / STAGE dir=main.py.c / STAGE file=bytes=2
```

End-to-end consequence, measured with the stub grader substituted at the capture pin (still no captured grader
executed):

```
cases=18 observed_pass=0 observed_fail=18 mismatches=7
```

**Every one of the 7 predicted passes becomes a failure.** The hardened probe's receipt would therefore **not**
byte-equal the committed receipt `corpus/evidence/round46/polyglot-c-py-probe.txt`
(`dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277`), so gate clause **P10** would fail and the
counter's **V4/V5** receipt legs would fail. The committed receipt was produced by the *unhardened* revision
(`67a8f4a6…`), as the round-46 seat itself recorded (`.ufo/waves/round-46/w1/R46ExecC3Probe.md` §8.2).

**Minimal repair** (for the L1's stage-2 amendment, not applied by this seat): extend the guard to
`if mode in ("stage", "recipe", "all"):` and have the `"all"` path run seed+recipe before the two grade legs, or
restore the old three-invocation shape. The one-sandbox design itself (so the re-grade sees the `cmain` the first
grade's `gcc` wrote) is sound and worth keeping.

### 3.2 `prlimit --nproc=48` cannot create a sandbox on this host today

The hardened probe wraps every sandbox in `prlimit --nproc=48 --cpu=5 --fsize=1048576 --core=0 --as=536870912
--nofile=512` (`polyglot_c_py_probe.py:105` `LIMITS`). `RLIMIT_NPROC` is checked against the **real uid's host-wide
thread count**, and the 64-seat wave puts uid 1000 at ~1100–1150 threads — far above 48. The result is a hard failure
before any case runs:

```
$ python3 candidate/plans/polyglot_c_py_probe.py --lane "$S/lane" --stage-check --work "$S/work/sc"
STAGECHECK nop rc=1 expect=absent file= dir=  match=NO
...
stagecheck cases=18 failed=18
exit=1
```

with the sandbox error visible on stderr (`bwrap: Creating new namespace failed: Resource temporarily unavailable`).

Isolation (the committed probe, which has no `prlimit`, run on the same host in the same minute):

```
$ git -C "$S/lane" stash push -- plans/polyglot_c_py_probe.py   # back to 67a8f4a6…
$ sha256sum "$S/lane/plans/polyglot_c_py_probe.py"
67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26
$ python3 "$S/lane/plans/polyglot_c_py_probe.py" --lane "$S/lane" --stage-check --work "$S/work/old"
STAGECHECK nop rc=0 expect=absent file=absent dir=absent pycheck=n/a ccheck=n/a match=yes
...
stagecheck cases=18 failed=0
exit=0
```

Threshold sweep (the failure tracks the uid's thread count, not a fixed constant):

```
uid-1000 THREAD count: 1106
nproc=512   threads=1146  -> bwrap: Creating new namespace failed: Resource temporarily unavailable
nproc=1024  threads=1135  -> bwrap: Creating new namespace failed: Resource temporarily unavailable
nproc=1536  threads=1108  -> rc=0
nproc=2048  threads=1132  -> rc=0
```

Raising **only** `--nproc` to 8192 (nothing else changed) makes the hardened probe's stage-check pass and be
**byte-identical** to the round-46 recorded lines:

```
$ cmp receipts/sc-variant.txt receipts/sc-r46.txt && echo "cmp: BYTE-IDENTICAL"
cmp: BYTE-IDENTICAL to the round-46 recorded stage-check lines
```

So `--nproc=48` is not a sandbox-integrity requirement — it is a host-load-dependent failure mode that will bite any
wave with a large seat count. A value at or above the uid's thread count, or dropping `--nproc` and relying on the
`--as`/`--fsize`/`--cpu` bounds, is the operable choice.

### 3.3 What the candidate probe does reproduce correctly

`--dry` is byte-identical to the committed frozen dry table, so the **case table, predictions and tags are
unchanged** by the hardening:

```
$ python3 candidate/plans/polyglot_c_py_probe.py --lane . --dry > receipts/candidate-dry.txt
exit=0
$ sha256sum receipts/candidate-dry.txt
99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536
$ sha256sum "$S/lane/corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt"
99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536
$ cmp receipts/candidate-dry.txt "$S/lane/corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt"
cmp: BYTE-IDENTICAL to the committed freeze table
```

The hardened probe pins the same 7 captures (`gitignore` is capture-only and unread, as the round-46 seat recorded);
`PINS` in the candidate matches `CAPTURES` in `plans/round46_c3_verify.py:97-104`.

---

## 4. Sources opened (§2b) — URL, access date, located quote

| source | URL | accessed | located quote (≤25 words) |
|---|---|---|---|
| S166 primary (pinned raw source) | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py` | 2026-10-27 | `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]` (line 27) — the three graded fixed points |

This is the source the frozen §C2 "Sourced basis" rests on; it is the same pinned revision the lane already holds as
capture `corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py`
(sha256 `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec`). The lane's committed capture is the
citable copy; no new network fetch was needed for this seat's item, and the round-48 lesson's `## Gate` should cite
the row above.

Lane sources read (all read-only, all at `a543d920`): `plans/round-48-claims.md`,
`corpus/lessons/round-46-verifier-spotcheck.md`, `plans/pkg_gate.py`, `plans/pkg-spec-r46.json`,
`plans/order_check.py`, `plans/round46_c3_verify.py`, `plans/filler46/pkg-spec-filler.json`,
`.ufo/waves/round-46/w1/R46ExecC3Probe.md`, `.ufo/waves/round-46/claims/control-c3-echo.txt`,
`.ufo/waves/round-46/integrate/c3-landing.txt`, `.ufo/waves/round-46/claims/envelope.sh`, `SCORECARD.md` (via the
routing note; the round-46 wave-2 verdicts are quoted in the spot-check above).

---

## 5. Exact commands run (all inside `S`, all read-only against the lane)

```
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" checkout --detach a543d92083557dd9b33ee674e9b99b03411f80af
git -C "$S/lane" rev-parse --show-toplevel ; git -C "$S/lane" rev-parse HEAD
git ls-tree a543d920 plans/round-48-claims.md .ufo/waves/round-46/w1/R46ExecC3Probe/
git ls-tree 0f77f9b plans/polyglot_c_py_probe.py plans/pkg_gate.py
sha256sum .ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py plans/polyglot_c_py_probe.py plans/pkg_gate.py
cmp <artifact> "$S/candidate/plans/polyglot_c_py_probe.py"
cp <artifact> "$S/candidate/plans/polyglot_c_py_probe.py" ; cp <candidate> "$S/lane/plans/polyglot_c_py_probe.py"
python3 candidate/plans/polyglot_c_py_probe.py --lane . --dry
python3 candidate/plans/polyglot_c_py_probe.py --lane "$S/lane" --stage-check --work "$S/work/sc"
python3 candidate/variant_nproc8192.py --lane "$S/lane" --stage-check --work "$S/work/vA"
git -C "$S/lane" stash push/pop -- plans/polyglot_c_py_probe.py
python3 "$S/lane/plans/polyglot_c_py_probe.py" --lane "$S/lane" --stage-check --work "$S/work/old"
python3 candidate/plans/pkg_gate_pre_receipt.py --root "$S/lane" --spec "$S/lane/plans/pkg-spec-r46.json" --work "$S/work/pre"
python3 candidate/plans/pkg_gate_pre_receipt.py --root "$S/lane" --spec "$S/lane/plans/filler46/pkg-spec-filler.json" --work "$S/work/filler"
python3 candidate/plans/pkg_gate_pre_receipt.py --root "$S/lane" --spec … --gate "$S/work/doctored_gate.py" --work "$S/work/neg"
python3 "$S/lane/plans/pkg_gate.py" package --root "$S/lane" --spec "$S/work/pre/spec-sentinel.json" --rerun
bwrap (stub-grader harness-mode isolation, modes all/recipe/stage)
prlimit --nproc={48,128,256,512,700,1024,1536,2048,4096,8192} -- bwrap --unshare-all … (threshold sweep)
```

Every fixture Git call used `git -C "$D"` with `D` inside the scratch, and the toplevel was asserted before any
write to the clone (`git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r48/R48C2ExecProbe/lane`).
The only write to the clone was the candidate probe file (then restored/removed by `stash pop`/`cp`); the clone was
never committed, pushed, or mutated in history (`git -C "$S/lane" status --porcelain` showed only
`M plans/polyglot_c_py_probe.py`).

**PATH-dir digest unchanged:** `/home/vgpnk/.local/bin` content digest `7747d38e2042d398` before and after every
measurement batch (same value the round-46 receipts carry).

---

## 6. Limits (stated)

1. **No full probe run was made** — forbidden by the item and by the Q30 ordering rule before the stage-2 commit. The
   receipt consequences in §3.1 are established from the harness source plus stub-grader measurements, not from a real
   graded run; the *shape* of the failure is measured, the exact byte-level receipt is not (and cannot be until after
   stage 2).
2. **The stub-grader experiments never imported the captured `test_outputs.py`.** The stub was substituted at the
   capture pin in a scratch copy of the probe; the captured grader was never executed, so no case of this task was
   graded and no outcome exists. `--stage-check` is parse-only by construction (`compile()` of the text,
   `gcc -fsyntax-only`) and never imports the grader either.
3. **§3.1's minimal repair is a proposal, not a landed fix.** This seat's write scope excludes `plans/`; the L1 owns
   the stage-2 amendment. No predicate, control, kill rule or pin was changed by this seat.
4. **The `nproc` threshold is host-load dependent.** The measured 48-vs-1100 contrast is a property of *this* wave's
   seat count on *this* host; on a quiet host `nproc=48` would have worked (as it did for the round-46 seat at
   02:34). The finding is that the limit is fragile, not that it was always broken.
5. **`pkg_gate.py`'s P9 (`--require-clean-tree`) was not exercised** — the wrapper supports the flag but the
   measurement runs did not pass it, because the scratch clone carries the modified candidate probe.
6. The receipt `dd0e3546…` and the dry table `99adfea6…` are the round-46 stage-2 pins; this seat did not attempt any
   re-pin, and no pin in the lane was touched.

---

## 7. Recommendations for the L1 (advisory, not applied)

1. **Do not land `22b7779e…` verbatim until §3.1 is repaired.** As it stands it would break P10/V4/V5 and force a
   re-pin of a *wrong* receipt. Either repair the `"all"` mode guard, or land the committed `67a8f4a6…` revision (whose
   grade path is correct) and carry the sandbox hardening as a separate, repaired step.
2. **If the hardening is landed, change `--nproc=48`** to a value above the uid's host-wide thread count (or drop it),
   and re-measure the stage-check — the rest of the hardened argv (tmpfs sizes, `--as`, `--fsize`, the reader thread,
   `--remount-ro /` last) is sound and reproduces the round-46 stage-check byte-for-byte.
3. **Adopt the P10-disabled wrapper** (`S/candidate/plans/pkg_gate_pre_receipt.py`, sha256
   `03785e039b5606d6d90da3c17430352387622a8cd002e95f9a6e3b46b48deeae`) for the three stage-2 controls (base tree,
   filler package, echo receipt). It changes no frozen byte, and its receipt is clean under `plans/order_check.py`'s
   own regexes — which is precisely the V8 fix the round-48 claims froze.
4. **Any amendment to the case table** (the V7 fix that gives `both-print` and `toolchain` a violating case) moves the
   `--dry` digest, so `pkg-spec-r46.json`'s `DRY_SHA256` and the frozen dry-table file must both be re-pinned at
   stage 2, and the receipt re-run **after** the stage-2 commit and re-pinned. Peer `R48C2ExecCases` owns that
   amendment and was told the sequencing.

---

## 8. Blockers

None for this seat's item: both deliverables exist as scratch candidates with verified digests, and the P10-disabled
mode is measured working. The **two defects in §3 are blockers for the L1's landing plan**, not for this seat.

**Scratch cleanup:** `S=/fast/scratch/hyaku/kengaku-r48/R48C2ExecProbe` was removed at the end of this wave
(`rm -rf`), after the receipts above were summarised here. The lane holds only this report.

VERDICT: probe-candidate-verbatim-digest-match-22b7779e; p10-disabled-gate-wrapper-measured-clean-under-order-check; two-defects-found-in-hardened-grade-path-recipe-never-runs-and-nproc48-host-blocked; no-full-probe-run; no-scored-run
