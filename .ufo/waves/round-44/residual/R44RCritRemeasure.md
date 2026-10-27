# R44RCritRemeasure — residual critic: independent re-measure at landed commit

Seat: R44RCritRemeasure (critic). Date: 2026-10-26. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scratch: `/fast/scratch/hyaku/kengaku-r44/R44RCritRemeasure`.

## Setup

Clean independent clone of the landed integration commit, built from nothing, no shared object store:

```
git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" checkout -q 2a263e5a56ef6d48d06805e1ccd106de5de9ba66
```

Verified inside the envelope: `TOOPLEVEL=/fast/scratch/hyaku/kengaku-r44/R44RCritRemeasure/lane`, `HEAD=2a263e5a56ef6d48d06805e1ccd106de5de9ba66`,
`plans/battery44/` has 10 modules (`u14c_name_a/b`, `u5_short_a/b`, `u6_long_a/b`, `u7_twin_a/b`, `u9_worktree_a/b`).

Every measurement ran inside the round-44 envelope
(`.ufo/waves/round-44/claims/envelope.sh "$S/env" ...`). The envelope line (Q32) for every run is pasted in
the per-run sections; in every run `local_bin_content_before=328be01808ba022f` equals
`local_bin_content_after=328be01808ba022f` → `unchanged`, `exit=` matched the command's rc, no `INVALID`.

## C1 — `plans/round44_c1_verify.py --lane .` (twice: `--jobs 1`, then `--jobs 8`, different `--work` roots)

Run 1 (`--work $S/w1 --jobs 1`), envelope line:
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind <scr>/env <scr>/env --bind <scr>/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- env S=<scr> PYTHONDONTWRITEBYTECODE=1 TMPDIR=<scr> bash -c cd "$S/lane" && python3 plans/round44_c1_verify.py --lane . --work "$S/w1" --jobs 1
```
Output (rc=0, envelope end exit=0):
```
PINS total=2 mismatched=0
FIXTURE u14c_name_a-draft-suffix tool=order expect=error declared=- observed_rc=2 observed=- ok
... (33 FIXTURE lines, all ok, wrong=0) ...
MUTANT U5 anchor silence killed by=u5_short_a-manifest-registry attributed=L522 value=differs hits=7 -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
MUTANT U6 anchor silence killed by=u6_long_a-registry-65 attributed=L522 value=differs hits=7 -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
MUTANT U7 anchor rc-mirror killed by=u7_twin_a-rowpath-registry attributed=L539 value=differs hits=6 -- plans/anchor_digest_check.py:98-99 'A token that resolves to several of the row's captures
MUTANT U9 anchor rc-mirror killed by=u9_worktree_a-registry-wrong-capture attributed=L384 value=differs hits=5 -- plans/anchor_digest_check.py:106-107 'lessons are read from the working tree for paths com
MUTANT U14c order error killed by=u14c_name_a-draft-suffix attributed=L161 value=differs hits=7 -- plans/order_check.py:26-27 'Exit: 0 order holds · 1 order broken · 2 setup error (... unpa
BATTERY fixtures=33 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=4/4 order=1/1
ADVERTISED direct=5 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 pass
```

Run 2 (`--work $S/w1b --jobs 8`), envelope line as above with `--jobs 8`. Output **byte-identical** to run 1
(after stripping the `ENVELOPE ...` lines: `diff c1-jobs1.clean c1-jobs8.clean` → no differences), `rc=0`.

Predicate exact sequence (asserted in order against the clean output, `plans/round-44-claims.md` lines 47-50):
`PINS total=2 mismatched=0` → `BATTERY fixtures=33 wrong=0 tampered=0 sidechannel=0` →
`MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0` →
`MUTANTS-BY-TOOL anchor=4/4 order=1/1` → `PINS-AFTER mismatched=0` → `PREDICATE C1 pass`. Exit 0 both times.

## C2 — `plans/round44_c2_verify.py --lane .` (twice, different `--work` roots)

Run 1 (`--work $S/w2`), envelope line:
```
ENVELOPE /usr/bin/bwrap ... -- env S=<scr> PYTHONDONTWRITEBYTECODE=1 TMPDIR=<scr> bash -c cd "$S/lane" && python3 plans/round44_c2_verify.py --lane . --work "$S/w2"
```
Output (rc=0, envelope end exit=0):
```
V1 ok listed=11 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=0
    gate: P4 ok checked=22 bad=0 first=0
    gate: P5 ok manifest_entries=11 bad=0 first=0
    gate: P6 ok rows=9 bad=0 first=0
    gate: P7 ok source_lines=9 bad=0 first=0
    gate: P8 ok index_rows=51 knowledge_files=51 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=3630
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=9 bad=0
V4 ok cases=14 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 tags=4 bad=0
V8 ok order_exit=0 result=PASS
V9 ok case_rows=14/14 bad=0
V10 ok mechanism_rows=14/14 bad=0
V11 ok states=48 grader_pass=24 grader_fail=24 disagree=0
checks=11 defects=0
PREDICATE C2 pass
```

Run 2 (`--work $S/w2b`): output **byte-identical** to run 1 (clean diff → no differences), `rc=0`.
Predicate exact sequence (`round-44-claims.md` lines 92-93): `checks=11 defects=0` → `PREDICATE C2 pass`, exit 0.

## Probe — `plans/feal_linear_probe.py --lane .` fresh run, byte compare to the receipt

Run (`--work $S/w3`), envelope line as above with `python3 plans/feal_linear_probe.py --lane . --work "$S/w3"`.
Fresh stdout (after stripping envelope lines and `rc=`) is **byte-equal to the receipt**:

```
sha256sum probe-fresh.clean  = 40308211216be063084eb9a1f22faded5a8550d392a83f6e13545e2ddae205a0
sha256sum <lane>/corpus/evidence/round44/feal-linear-probe.txt = 40308211216be063084eb9a1f22faded5a8550d392a83f6e13545e2ddae205a0
```

`diff` over the 24 lines: no differences. 14 cases, `regrade cases=14 differ=0`, `cases=14 observed_pass=8 observed_fail=6 mismatches=0`.
Probe `rc=0`.

## order_check for round 44

Run inside the envelope:
```
ENVELOPE /usr/bin/bwrap ... -- env S=<scr> PYTHONDONTWRITEBYTECODE=1 TMPDIR=<scr> bash -c cd "$S/lane" && python3 plans/order_check.py --lane . --claims plans/round-44-claims.md --receipt corpus/evidence/round44/feal-linear-probe.txt
```
Output (rc=0):
```
ORDER claims=plans/round-44-claims.md round=44 freeze=5f16ed04b04a80a17a5a1a060c12093d9a152a64
ORDER receipt=corpus/evidence/round44/feal-linear-probe.txt receipt_commit=45dc0bc81e42e02ecd272712086c372c8844b108 claims_dir=.ufo/waves/round-44/claims/
ORDER scanned commits=1 file_entries=32 distinct_blobs=32
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
```
Freeze commit `5f16ed04…` and receipt commit `45dc0bc8…` match the assignment's stated freeze and first recorded probe run.

## Nondeterminism / stability

- C1 `--jobs 1` vs `--jobs 8` (different work roots): clean stdout byte-identical, both exit 0. The jobs count did not change the verdict or any line.
- C2 run 1 vs run 2 (different work roots): clean stdout byte-identical, both exit 0 (V11 `states=48 grader_pass=24 grader_fail=24 disagree=0` both times).
- Probe fresh stdout byte-equal to the committed receipt (same sha256).
- Envelope `~/.local/bin` content digest unchanged in every run (before/after `328be01808ba022f`); no measurement invalidated.

## Findings

No falsification found. The landed admission reproduces exactly: C1 predicate passes with `killed=5` all attributed
(every kill `value=differs`, legs f+g engaged), per-tool `anchor=4/4 order=1/1`, 33 fixtures `wrong=0 tampered=0 sidechannel=0`;
C2 passes all V1-V11 with `checks=11 defects=0`; order_check passes; the probe is deterministic and byte-equal to the receipt.
No nondeterminism observed across the repeated runs.

VERDICT: remeasure-c1-pass-c2-pass-stable-yes
