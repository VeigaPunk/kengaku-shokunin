# R45ExecR45CounterDocs — both counters run from a clean clone exactly as the claims promise

Seat: executor (leaf), kengaku round 45 wave 1 of 2 (build, v1). Judged on: operability.
Scratch: `/fast/scratch/hyaku/kengaku-r45/R45ExecR45CounterDocs` (deleted at the end via `scratch_guard.py safe-rm`).
Receipts: `.ufo/waves/round-45/w1/R45ExecR45CounterDocs/` (172 KB, 17 files, none > 1 MiB).

## Verdict

`VERDICT: counters-clone-runnable-yes`

Both counters run to a complete verdict from a clean `git clone` with cwd inside the clone and `--lane .`,
inside the round-45 envelope, at the freeze commit **and** at the final tip; both reach their own passing
predicate; `--work` and `--jobs` behave as documented; neither writes into the lane.

## Method (clone rule + envelope, per the seat contract)

* Clones: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/<name>"`; before any write
  `git -C "$S/<name>" rev-parse --show-toplevel` printed the clone dir for every clone used
  (`lane`, `lane-freeze`@`b4fcd35`, `lane-fence`@`b4fcd35`, `lane-tip2`@`7d062c0`, `lane-final`@`8f9a898`).
  No `git add/commit/stash/checkout/reset/push/pull` in the lane; only `checkout --detach` inside scratch clones.
* Every counter/probe run: `cd <clone>` then
  `.ufo/waves/round-45/claims/envelope.sh "$S/env" /usr/bin/python3 plans/round45_cX_verify.py --lane . --work "$S/work/<id>"`.
  `TMPDIR="$S"` exported. `ENVELOPE … unchanged` on every run (no `INVALID`, nothing re-run).
* Lane reads only. `git -C <clone> status --porcelain` empty after every run (verified, below).

## A. C1 counter — `plans/round45_c1_verify.py`

### A1. Freeze commit `b4fcd35`, `plans/fixture_fence.py` absent → reproduces the committed control **byte-identically**

```
$ cd "$S/lane-freeze" && python3 plans/round45_c1_verify.py --lane . --work "$S/work/c1"
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py absent
REFUSALS total=10 clean=0 leaked=10 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=0 refused=104 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=10
PREDICATE C1 fail
exit=1                                     (7 s: 23:32:21 -> 23:32:28)
```

```
$ diff <(grep -v '^exit=' .ufo/waves/round-45/claims/control-c1-nothing.txt) \
       <(grep -v '^ENVELOPE' "$S/out/c1-freeze.txt")
IDENTICAL
```

So the claim's "no `plans/fixture_fence.py` → every refusal module `LEAKED`, `contradicted=10`, `PREDICATE C1
fail`" reproduces exactly, including all 114 `FENCE-RUN` lines and the per-module `REFUSAL` lines.

### A2. Every committed C1 control with a fence present reproduces exactly

Fences assembled per the claims' own recipe into a scratch clone
(`cat plans/round44_c1_verify.py "$CL/fences/r44_tail.py" > plans/fixture_fence.py`, sha256
`db71ea2af35bb552188990fb4ba4985ba052b716bb8dfa01b9c302cbf05bafcb` — the same digest the committed control
records on its `FENCE` line):

| fence | my run (verdict lines) | exit | committed control |
|---|---|---|---|
| r44 adapter | `REFUSALS total=10 clean=3 leaked=3 read=4 hung=0 build_errors=0` / `HONEST … 104 admitted` / `CALIBRATION advertised=10 contradicted=7` / `PREDICATE C1 fail` | 1 | **IDENTICAL** (summary lines and whole `REFUSAL` block) |
| `admit_all` | `clean=0 leaked=10 …` / `HONEST … admitted=104` / `contradicted=10` / fail | 1 | **IDENTICAL** |
| `refuse_all` | `clean=10 leaked=0 …` / `HONEST … admitted=0 refused=104` / `contradicted=0` / fail | 1 | **IDENTICAL** |
| `static_only` | `clean=9 leaked=1 …` / `HONEST … refused=104` / `contradicted=1` / fail | 1 | **IDENTICAL** |

Diff method: `diff <(grep -E '^(PINS|REFUSALS|HONEST|CALIBRATION|PREDICATE) ' <control>) <(same from run>)` and
`diff <(grep '^REFUSAL ' <control>) <(same from run>)` → both empty for all four.

This also confirms the goal's before-state number: **r44-fence control `contradicted=7`**, and that
`contradicted=0` alone is not the predicate (`refuse_all` prints `contradicted=0` yet fails on `HONEST refused=104`).

### A3. The predicate is reachable — `PREDICATE C1 pass`, exit 0

`plans/fixture_fence.py` did not exist at the freeze, so I proved satisfiability with the wave-1 candidate
fences other seats authored (read-only copies into **my** scratch clone; I wrote nothing in the lane):

```
$ cd "$S/lane-fence"   # fence = .ufo/waves/round-45/w1/R45FenceVarA/fixture_fence.py
FENCE plans/fixture_fence.py sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
exit=0     (8 s: 23:44:39 -> 23:44:47)
```

Same pass, exit 0, for `R45FenceVarB` (sha256 `f2cd51d5…`) and `R45ExecWitnessFence` (sha256 `a860672f…`).
So the instrument's full path (build in the round-44 sandbox → `strace -f -y` fence run under bwrap →
`opens` accounting → predicate) executes end-to-end and admits a pass.

### A4. At the final tip `8f9a898` the lane's own fence passes

```
$ cd "$S/lane-final" && python3 plans/round45_c1_verify.py --lane . --work "$S/work/c1-final"
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
exit=0     (7 s: 23:47:05 -> 23:47:12)
```

That is the claim's frozen predicate, verbatim, from a clean clone of the landing tip.

### A5. `--jobs` behaves: `--jobs 2` is verdict-identical to the default (8)

```
$ python3 plans/round45_c1_verify.py --lane . --work "$S/work/c1-j2" --jobs 2     # fence absent
REFUSALS total=10 clean=0 leaked=10 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=0 refused=104 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=10
PREDICATE C1 fail                                     exit=1
$ diff <(grep -v '^ENVELOPE' out/c1-freeze.txt) <(grep -v '^ENVELOPE' out/c1-jobs2.txt)   -> IDENTICAL
```

and in the passing state (`--jobs 2`, variant-A fence): `PREDICATE C1 pass`, exit 0, 13 s (23:45:16→23:45:29);
its verdict lines diff empty against the default-jobs pass run. So concurrency changes wall time only
(36 s for the r44 fence at default 8 → 13–14 s at `--jobs 2` for a lighter fence), never the verdict.

### A6. `--work` behaves, and guards the lane

```
$ python3 plans/round45_c1_verify.py --lane . --work "$S/lane-freeze/inside"
PINS total=33 mismatched=0
SETUP --work must not lie inside the lane
exit=2
```

Absent `--work` dirs are created (`--work "$S/work/c1-R45FenceVarA"` exists after the run). `--work` is never
needed for correctness: the counter also runs from `$TMPDIR` scratch (A1's control run used an explicit
`--work`; the tool defaults to `tempfile.mkdtemp(dir=None)`).

## B. C2 counter — `plans/round45_c2_verify.py`

### B1. Freeze commit `b4fcd35` → the committed control's verdict, with one explainable line difference

```
$ cd "$S/lane-freeze" && python3 plans/round45_c2_verify.py --lane . --work "$S/work/c2"
V1 ok listed=9 bad=0 extra=0        gate: P9 ok untracked=0     gate: defects=8
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V3 DEFECT rows=9 bad=[S149:row … S157:row]      V4/V7/V9/V10/V11 DEFECT (receipt, entry absent)
V5 ok probe=frozen dry_byte_equal=True          V6 ok census_exit=0      V8 DEFECT order_exit=2
checks=11 defects=8
PREDICATE C2 fail
exit=1                                     (2 s: 23:33:10 -> 23:33:12)
```

Diff against `git show b4fcd35:.ufo/waves/round-45/claims/control-c2-nothing.txt`:

```
10c10
<     gate: P9 DEFECT untracked=151 first=.ufo/waves/round-45/attempt1-unclaimed/corpus/evidence/round45/f1-census/SHA256SUMS
---
>     gate: P9 ok untracked=0 first=0
12c12
<     gate: defects=9
---
>     gate: defects=8
```

Every counter-level verdict line (`V1`…`V11`, `checks=11 defects=8`, `PREDICATE C2 fail`) is identical; only the
gate's clean-tree leg differs, because that control was captured in the **dirty lane working tree**
(`untracked=151`) while a clean clone has none. Finding F3 below.

### B2. Tip `05b02e2` — real defect found, then found fixed by a peer

```
$ cd "$S/lane" && python3 plans/round45_c2_verify.py --lane . --work "$S/work/c2-tip"
    gate: P10 DEFECT fresh probe output is not byte-equal to the receipt
checks=11 defects=7     PREDICATE C2 fail     exit=1
```

Cause, measured: that commit's receipt carried the envelope's own lines. `corpus/evidence/round45/password-recovery-probe.txt`
had 3 `ENVELOPE` lines (2 header at `:1-2`, 1 trailer at `:26`), none of which the probe prints. Proof:

```
$ python3 plans/password_recovery_probe.py --lane . > probe.txt            # 4659 bytes, exit 0
$ grep -v '^ENVELOPE ' corpus/evidence/round45/password-recovery-probe.txt > stripped.txt   # 4659 bytes
$ cmp stripped.txt probe.txt        -> BYTE-EQUAL
$ sha256sum probe.txt stripped.txt  -> cf74f451df90aa4adfcc45dc6d9023ba288bf456de939377c97e24ca3c6c924e (both)
$ (swap the stripped receipt in) gate P10 -> ok probe_rerun=byte-equal bytes=4659
```

`plans/pkg_gate.py` `c_rerun` compares `r.stdout` to the receipt bytes with no filter, so the pollution made
P10 → V2 permanently red. Peer commit `7d062c0` (23:40:57) reframed the receipt to bare stdout
(`…password-recovery-probe.txt | 3 -`) and kept the envelope transcript separately
(`corpus/evidence/round45/probe-run-envelope.txt`), which is the round-44 convention (`grep -c ENVELOPE
corpus/evidence/round44/feal-linear-probe.txt` → `0`).

### B3. Tip `7d062c0` — second real defect found, then found fixed by a peer

```
$ cd "$S/lane-tip2" && python3 plans/round45_c2_verify.py --lane . --work "$S/work/c2-tip2"
V1..V9 ok, V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0
V10 DEFECT mechanism_rows=16/16 bad=['constant-crlf:test_outputs.py:14 quote not on the line',
     'dir-state:test_outputs.py:14 quote not on the line', 'crlf-line:test_outputs.py:14 quote not on the line',
     'under-varsea:test_outputs.py:10 quote not on the line']
checks=11 defects=1     PREDICATE C2 fail     exit=1
```

Root cause is the frozen counter's ≥2-word floor, not the quotes' location:

```
$ python3 … (counter's own MECH_ROW/norm, run over the entry)
constant-crlf    verdict=DEFECT cause=len(q.split())=1<2  quote_actually_on_line=True
dir-state        verdict=DEFECT cause=len(q.split())=1<2  quote_actually_on_line=True
crlf-line        verdict=DEFECT cause=len(q.split())=1<2  quote_actually_on_line=True
under-varsea     verdict=DEFECT cause=len(q.split())=1<2  quote_actually_on_line=True
```

`plans/round45_c2_verify.py` V10: `if len(q.split()) < 2 or int(line) > len(lines) or q not in norm(lines[…])`
— a one-token quote such as `recovered_pass_path.exists()` is rejected whatever line it sits on, and the
message names only the last disjunct. With those four quotes lengthened to ≥2 words in a scratch copy (I
restored the file; the clone ended clean):

```
V10 ok mechanism_rows=16/16 bad=0
checks=11 defects=0
PREDICATE C2 pass          exit=0        (6 s: 23:46:05 -> 23:46:10)
```

Peer commit `8f9a898` then lengthened exactly those four rows (`corpus/knowledge/tb2-password-recovery-grader.md:124,126,135,136`).

### B4. Final tip `8f9a898` — the frozen predicate, verbatim

```
$ cd "$S/lane-final" && python3 plans/round45_c2_verify.py --lane . --work "$S/work/c2-final"
V1 ok … gate: P1..P10 ok … gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0      V3 ok rows=8 bad=0
V4 ok cases=16 mismatches_named=0/0            V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0                            V7 ok rows=9 tags=9 bad=0
V8 ok order_exit=0 result=PASS                 V9 ok case_rows=16/16 bad=0
V10 ok mechanism_rows=16/16 bad=0              V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0
checks=11 defects=0
PREDICATE C2 pass
exit=0                                     (5 s: 23:47:20 -> 23:47:25)
```

`checks=11 defects=0`, `PREDICATE C2 pass`, exit 0 — the claims' frozen predicate, from a clean clone.

### B5. Determinism, flags, cwd independence

* `--lane .` with cwd inside the clone (the claimed invocation) and `--lane <abs clone>` from an outside cwd both
  work: the outside-cwd run produced the same `checks=11 defects=8` / `PREDICATE C2 fail` as the in-clone run at
  that commit.
* Two back-to-back `--lane .` runs on the same tree: `diff out/c2-det1.txt out/c2-det2.txt` → byte-identical;
  and identical to the enveloped run. The receipt the probe prints is deterministic (same 4659 bytes, sha256
  `cf74f451…`, inside and outside the envelope).
* `--work` is created if absent. C2 has **no** inside-lane guard — unlike C1 — see F4.
* C2 does not take `--jobs`: `round45_c2_verify.py: error: unrecognized arguments: --jobs 2`, exit 2. Correct
  for its contract (only C1 documents `--jobs`).

## C. Cross-cutting checks

* **Exit-code contract** exercised: C1 `0` pass / `1` predicate fail / `2` setup error
  (`--work` inside the lane); C2 `0` pass / `1` predicate fail / `2` for an unknown flag.
* **Digest pins bite**: appending a comment to a pinned module gave `PINS total=33 mismatched=1
  first=plans/refusals45/f1_gitfile.py` and a failing predicate; only a mismatch of the round-44 builder
  (`plans/round44_c1_verify.py`) forces `SETUP … exit 2`.
* **Nested sandboxing works**: C1's own `bwrap`+`strace` sandboxes run inside the envelope's `bwrap`
  (`bwrap --ro-bind / / … 'nested bwrap ok'`, exit 0) — the 114 fence decisions and the 32 fixture builds all
  completed under it.
* **No lane writes by either counter**: `git -C <clone> status --porcelain` printed nothing after every run
  (`lane-freeze`, `lane-fence`, `lane-tip2`, `lane-final`), including after the `--work`-inside-lane test once I
  removed the empty dir C2 created (F4).
* **`claims/frozen-digests.txt` is current**: 18 entries, 18 distinct paths, all matching the working tree
  (`round45_c1_verify.py` `7745eb0a…`, `round45_c2_verify.py` `ab6825e3…`, `pkg-spec-r45.json` `2f924ffa…`,
  `password_recovery_probe.py` `9363e03e…`). `pkg_gate.py` is pinned by the spec and by the counter
  (`ea638822…`), not by that file.

## Findings for the L1 (ranked by what would block admission)

* **F1 (C1, operability) CLOSED-BY-VERIFICATION.** The C1 counter's full path is runnable from a clean clone and
  its predicate is reachable: `PREDICATE C1 pass`, exit 0, both with wave-1 candidate fences and with the lane's
  landed fence at `8f9a898`. All five committed C1 controls (nothing, r44 adapter, admit_all, refuse_all,
  static_only) reproduce byte-identically. No action.
* **F2 (C2, defect found → fixed).** The receipt committed at `05b02e2` embedded the envelope's 3 `ENVELOPE`
  lines, so the gate's `P10`/`V2` could never pass (`fresh probe output is not byte-equal to the receipt`).
  Replaced at `7d062c0` by bare stdout plus `probe-run-envelope.txt`. If any future receipt is captured by
  redirecting envelope stdout into the receipt path, this recurs — the receipt must be the probe's stdout only.
* **F3 (C2, control artifact does not match a clean clone).** `claims/control-c2-nothing.txt` (both the freeze
  and the `52d7486` refresh) records `gate: P9 DEFECT untracked=151/6`, `gate: defects=9`, because it was
  captured in the dirty lane tree; the frozen predicate says "measured on a clean clone of the landing tip",
  where P9 is `ok` and the gate shows `defects=8`. The counter-level verdict (`checks=11 defects=8`,
  `PREDICATE C2 fail`) is unaffected, but the control should say which tree it was taken from, or be re-taken
  from a clean clone.
* **F4 (C2, minor asymmetry).** `round45_c2_verify.py` creates `--work` without the `C1` guard
  (`if pathlib.Path(a.work).resolve().is_relative_to(lane): SETUP … exit 2`). `--work <lane>/x` silently creates
  a directory inside the lane, which then makes the gate's `P9` clean-tree leg red on the next run. Cheap
  hardening if the L1 wants symmetry; not a predicate issue as long as seats use scratch.
* **F5 (C1, V10-style trap worth knowing for the C2 package).** The frozen C2 `V10` rejects any mechanism quote
  whose normalised form is a single token, and reports it as `quote not on the line`. Four rows hit this at
  `7d062c0`; fixed at `8f9a898`. Any later edit to `## Mechanism` must keep ≥2 words per quote.
* **F6 (governance, flagged not judged).** Post-freeze commits changed frozen-listed artefacts:
  `7d062c0` rewrote `plans/round45_c2_verify.py` (`+50/-42`: `CAPTURES` keys, `SPEC_SHA256`, `PROBE_SHA256`,
  `DECISIVE`, `ANSWER_PATH`, `MECH_ROW`), `plans/pkg-spec-r45.json` (row/capture layout), the probe
  (`plans/password_recovery_probe.py`), and moved the nine captures from
  `tests/…|environment/…|solution/…` to a flat capture dir (byte-identical contents — the moves show `0`
  changed lines, and every pinned digest is unchanged). `claims/frozen-digests.txt` was re-pinned to the new
  digests in the same wave. The C1 counter was never touched (`7745eb0a…` at freeze and at tip). The goal text
  lists the C2 counter, spec, probe and captures as frozen, so the L1 should confirm the re-pin was its own
  authorised edit rather than a seat's.

## Risks and limits of this report

* The lane moved three times while I measured (`05b02e2` → `7d062c0` → `8f9a898`); every number above names the
  commit it was taken at, and the receipts are kept, so a later tip can be re-measured the same way.
* I judged **operability only** — does the instrument run, does it reproduce the controls, is its predicate
  reachable. I did not judge whether the C1 fence or the C2 entry *should* be admitted; a passing predicate here
  is not an admission, and the fence/entry content is other seats' work.
* `refuse_all` shows why `contradicted=0` is not the whole predicate: it prints `contradicted=0` and still fails
  (`HONEST … refused=104`). Any reading of "a passed counter prints contradicted=0" must keep the HONEST line.
* No tool was installed or upgraded; nothing was written outside my scratch dir and this seat's report subdir.

## Receipts (`sha256`, all < 1 MiB)

```
a633b8fbb5f5cd8011251d03ff6e871c42bce61ea94b210495b5fa7f995eda0d  c1-final.txt            (8f9a898, pass)
fe756b4756ec44918c7e4782840bf282fbfd68e443b3ecc2bc379c1cbf3852b2  c2-final.txt            (8f9a898, pass)
6576756bb20e763dbc0fc3fc1593438894d4ee474b4706c8a67a0ea54b89db5f  c1-freeze.txt           (b4fcd35, == control-c1-nothing)
22879ac513734ec976c2846ccea8000b3efce47d7925b80746893b2097378199  c2-freeze.txt           (b4fcd35)
243e41f26b6e0087563b7debb9f84ca4496bb84a170059a7a8a4599cffe3a3a5  c1-r44fence.txt         (== control-c1-fence-r44)
8b5ec27753d42b0ef658b1fed06b2ba1cd16a2c77d395f0d543920dfe0e3b76e  c1-admit_all.txt        (== control …admit_all)
aafb625b0ff731a679e64c1680e47fac70916a0927b1869597c6c7b5755e92d6  c1-refuse_all.txt       (== control …refuse_all)
f82791b758df500f06bdd3ccbe5100dee71f08cb803aafdb10bc3b52e24e29f9  c1-static_only.txt      (== control …static_only)
fccf66088fd824a5ae1143e5272eddda9328211a2b3f84ceed5ed520374cbf07  c1-jobs2.txt            (--jobs 2, == default)
43a449addef4ad4e1da4f1087170ba0b7ddb47aee4d0e898f655b4f1d7063e58  c1-pass-j2.txt          (--jobs 2, pass state)
d53c0c90f37d5cfe036286ab2fb5c44802094ccec25a8a41500ca7b273fe689f  c1-R45FenceVarA.txt     (PREDICATE C1 pass)
3c021124bcfd31def3579365765aa1e8161a45373721a1618091d70438e12faa  c1-tip-05b02e2.txt
def1b940982beb404aa07325591f404da8009d6a1b0e8508ae102e57816e778a  c2-tip-05b02e2.txt      (P10 receipt defect)
9b00d397364dca7d73cab108de7208b9d101214e3047a6f5942a861bfbbb4e10  c2-tip2.txt             (7d062c0, V10 defect)
eb3a91dd70612b8fc75fa92f452bf888841e082a30b17cfe4f13241e4ec95343  c2-tip2-pass.txt        (V10 fixed in scratch copy)
cf74f451df90aa4adfcc45dc6d9023ba288bf456de939377c97e24ca3c6c924e  probe-env.body.txt      (receipt w/o ENVELOPE lines)
```

Each `c1-*.txt` / `c2-*.txt` is the full envelope stdout, i.e. `ENVELOPE …` line, `ENVELOPE start …`,
the counter's own lines, `ENVELOPE end … exit=N … unchanged`.

## ENVELOPE lines (Q32)

```
c1-freeze            ENVELOPE start 23:32:21  |  end 23:32:28 exit=1 before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
c2-freeze            ENVELOPE start 23:33:10  |  end 23:33:12 exit=1 before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
c1-tip (05b02e2)     ENVELOPE start 23:33:33  |  end 23:33:40 exit=1 before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
c2-tip (05b02e2)     ENVELOPE start 23:33:57  |  end 23:34:04 exit=1 before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
c1-r44fence          ENVELOPE start 23:37:33  |  end 23:38:09 exit=1 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
c1-admit_all         ENVELOPE start 23:38:26  |  end 23:38:33 exit=1 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
c1-refuse_all        ENVELOPE start 23:38:46  |  end 23:38:53 exit=1 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
c1-static_only       ENVELOPE start 23:38:54  |  end 23:39:03 exit=1 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
c2-tip2 (7d062c0)    ENVELOPE start 23:41:45  |  end 23:41:50 exit=1 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
c1-tip2 (7d062c0)    ENVELOPE start 23:42:00  |  end 23:42:07 exit=1 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
c1-R45FenceVarA      ENVELOPE start 23:44:39  |  end 23:44:47 exit=0 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
c1-pass-j2 (--jobs 2)ENVELOPE start 23:45:16  |  end 23:45:29 exit=0 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
c2-tip2-pass         ENVELOPE start 23:46:05  |  end 23:46:10 exit=0 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
c1-final (8f9a898)   ENVELOPE start 23:47:05  |  end 23:47:12 exit=0 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
c2-final (8f9a898)   ENVELOPE start 23:47:20  |  end 23:47:25 exit=0 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
probe-env (probe)    ENVELOPE start …        |  end … exit=0 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

Full envelope command line for the final C1 run:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind <S>/env <S>/env
         --bind <S>/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc
         --unshare-pid --die-with-parent -- /usr/bin/python3 plans/round45_c1_verify.py --lane .
         --work <S>/work/c1-final
```

No `INVALID`, no digest change, nothing re-run.

## Addendum — re-measured after the L1's integration commits (tip `d4c0cdf`)

The lane moved twice more while I wrote this (`8f9a898` → `4290d64` → `d4c0cdf`; the L1 committed the w1
reports and this seat's receipts in `4290d64`). Fresh clean clone at `d4c0cdf`, same invocation, inside the
envelope:

```
$ git -C "$S/lane" rev-parse HEAD            -> d4c0cdfbdc3886eadac4710ee49630ce00722ee1
$ python3 plans/round45_c1_verify.py --lane . --work "$S/work/c1"     exit=0
PINS total=33 mismatched=0
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
$ python3 plans/round45_c2_verify.py --lane . --work "$S/work/c2"     exit=0
checks=11 defects=0
PREDICATE C2 pass
ENVELOPE c1: start 23:50:18 | end 23:50:26 exit=0 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
ENVELOPE c2: start 23:50:28 | end 23:50:33 exit=0 before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

Receipts: `c1-recheck-d4c0cdf.txt` (`92348907…`), `c2-recheck-d4c0cdf.txt` (`1d9a4ec4…`). Both counters stay
clone-runnable and green after integration; the verdict below is unchanged.

VERDICT: counters-clone-runnable-yes
