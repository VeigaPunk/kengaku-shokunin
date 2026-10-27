# R44BatU14b — battery44 module `u14c_name_b` (order gate, claims-name guard; frozen mutant U14c)

Round 44 wave (build + attack, v2), kengaku lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Seat: executor. Everything below was measured on a `--shared` clone of the lane at
`/fast/scratch/hyaku/kengaku-r44/R44BatU14b/lane` (clone tip `5e3d3aa06c6b7000929ac3e62563a39159c4501f`;
`git -C "$S/lane" rev-parse --show-toplevel` = `/fast/scratch/hyaku/kengaku-r44/R44BatU14b/lane`).
No lane file, no `plans/battery44/` in the real lane, no PATH directory and no `$HOME` path was written.

## 1. Deliverables

| path (under `.ufo/waves/round-44/wave/R44BatU14b/`) | sha256 | role |
|---|---|---|
| `battery/u14c_name_b.py` | `7ac8f05ebf07d78087cdf3239d9cb4d4c550b9bc154c1f0ce89c156deef62620` | the battery44 module (4 fixtures, fids all `u14c_name_b-…`) |
| `controls/u14c_name_b_ctl.py` | `a70e5ebc29b0107eca64b73c7e045242aeb0570881a824c9c0fe0ea6f78e8c54` | specificity control (parseable-name twins), **not** part of the battery |
| `receipts/*.txt` (12 files, 13 110 bytes total) | — | envelope-bracketed receipts for every run below |

Module is stdlib-only, has no imports, no `SIDECHANNEL` token (`[]` from the counter's own scan below),
and the counter's build child accepted every fixture (`wrong=0`).

## 2. The frozen mutant, as quoted from `plans/round44_c1_verify.py`

```
('U14c', 'order', '-', 'error', 'direct',
 "plans/order_check.py:26-27 'Exit: 0 order holds · 1 order broken · 2 setup error (... unparseable round number, bad arguments)' (the claims-name guard disabled)",
 f"{WR} (MUTANT U14c); round-43 wave-1 R43PlanNext B.1 row 14 (U14c)",
 '        if not m:\n            raise SetupError(f"claims file name',
 '        if False:\n            raise SetupError(f"claims file name'),
```

Guard site (`plans/order_check.py`, pin `948d5e1d…`, unchanged):

```
161:        if not m:
162:            raise SetupError(f"claims file name is not round-NN-claims.md: {claims}")
163:        round_no = int(m.group(1))
```

With the guard dead, `m` is `None` and line 163 dereferences it. Direction `error` = reference exit 2,
mutant exit 0 or 1; `defects` is `[]` for every order fixture (the gate reports through its exit code only).

Measured bytecode of `main` over L161–L163 (host `/usr/bin/python3` = Python 3.14.8), from
`python3 -` compile + `dis` on `$S/lane/plans/order_check.py` and on the mutant copy `$S/mut/order_u14c.py`:

```
== REFERENCE 18 instructions on L161-L163
   L161 LOAD_FAST_BORROW m
   L161 TO_BOOL
   L161 POP_JUMP_IF_TRUE to L3
   L161 NOT_TAKEN
   L162 LOAD_GLOBAL SetupError + NULL
   ...
   L162 RAISE_VARARGS
   L163 LOAD_GLOBAL int + NULL
== U14c-MUTANT 8 instructions on L161-L163
   L161 NOP
   L163 LOAD_GLOBAL int + NULL
   L163 LOAD_FAST m
   L163 LOAD_ATTR group + NULL|self
```

So L161 still produces a line event for the tracer (span attribution reaches it) and the frame's next
event moves from L162 (raise) to L163 (dereference) — which is why the counter reports
`attributed=L161 value=differs` rather than `site-record-equal`. [INFERENCE] for the L162→L163 mapping
as the *reason* the site digests differ; measured fact: `attributed=L161 value=differs`.

## 3. The four fixtures

All repos are built from nothing (`ctx.init`/`ctx.write`/`ctx.git`); lanes are subdirectories of `d`;
`--lane` is the absolute repo path inside `d`; `--claims`/`--receipt` are repo-relative and are blobs at
HEAD, so leg i (order argv blobs) and F1–F6 admit them.

| fid | shape | what it demonstrates | reference rc | U14c rc |
|---|---|---|---|---|
| `u14c_name_b-registry-suffix` | 6 commits, 4-round registry table, claims landed as `plans/round-51-claims.md.orig`, receipt 3 commits later, 2 dirs deep | the guard fires on the *only* defect being a trailing `.orig` on an otherwise realistic multi-round registry | 2 | 1 |
| `u14c_name_b-nested-uppercase` | 4 commits, claims at `notes/history/Round-7-claims.md` (capital R), separate checks + receipt commits | second trigger of the same branch through a nested path and a case variation | 2 | 1 |
| `u14c_name_b-round-xx-token` | 3 commits, `plans/round-xx-claims.md`, receipt commit *before* the claims commit | a name with no round digits, in a lane whose history would itself be a `receipt-before-claims` reject | 2 | 1 |
| `u14c_name_b-underscore-name` | 2 commits, `plans/round_44_claims.md` committed together with its receipt | underscore spelling over the `freeze-contains-receipt` shape, so commit order cannot answer the question | 2 | 1 |

Exit codes in the last two columns are measured twice: by the counter's `observed_rc=2` lines (§4) and by
the by-hand reference/mutant pair (§7).

Each fixture carries a one-line comment above its `FIXTURES` entry. Shapes were chosen to be unlike the
witness set and unlike each other; I did not read `.ufo/waves/round-44/claims/witness/w_u.py` (nor the
sibling seat's second U14c module), so the independence the freeze asks for holds by construction here.

## 4. Primary measurement — dev counter, `--only U14c`

```
$ /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/claims/envelope.sh "$S/env" \
    python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py \
    --lane "$S/lane" --battery-dir …/wave/R44BatU14b/battery --only U14c --work "$S/w"
```
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44BatU14b/env /fast/scratch/hyaku/kengaku-r44/R44BatU14b/env --bind /fast/scratch/hyaku/kengaku-r44/R44BatU14b/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r44/R44BatU14b/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44BatU14b/battery --only U14c --work /fast/scratch/hyaku/kengaku-r44/R44BatU14b/w
ENVELOPE start 20:33:44 cwd=/fast/scratch/hyaku/kengaku-r44/R44BatU14b
PINS total=2 mismatched=0
FIXTURE u14c_name_b-registry-suffix tool=order expect=error declared=- observed_rc=2 observed=- ok
FIXTURE u14c_name_b-nested-uppercase tool=order expect=error declared=- observed_rc=2 observed=- ok
FIXTURE u14c_name_b-round-xx-token tool=order expect=error declared=- observed_rc=2 observed=- ok
FIXTURE u14c_name_b-underscore-name tool=order expect=error declared=- observed_rc=2 observed=- ok
MUTANT U14c order error killed by=u14c_name_b-registry-suffix attributed=L161 value=differs hits=4 -- plans/order_check.py:26-27 'Exit: 0 order holds · 1 order broken · 2 setup error (... unpa
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/0 order=1/1
ADVERTISED direct=1 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 20:33:46 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
Every FIXTURE line `ok`, `wrong=0 tampered=0 sidechannel=0`, `null_detected=0 unattributed=0`,
`U14c … killed … attributed=L161 value=differs`, `PINS-AFTER mismatched=0`. Receipt:
`receipts/dev_run1.txt`.

## 5. Load-bearing table — is each fixture load-bearing?

Generated variants in `$S/abo/` are slices of the same module (head + a reduced `FIXTURES` list, same fids,
same build functions); each variant is a directory holding one `.py`, run with `--only U14c` under the envelope.

| variant | fixtures kept | U14c result | envelope |
|---|---|---|---|
| `solo_registry` | registry-suffix only | `killed by=u14c_name_b-registry-suffix … hits=1` | start 20:34:04 / end 20:34:06 exit=0 before=after=`328be01808ba022f` unchanged |
| `solo_nested` | nested-uppercase only | `killed by=u14c_name_b-nested-uppercase … hits=1` | start 20:34:08 / end 20:34:10 exit=0 unchanged |
| `solo_xx` | round-xx-token only | `killed by=u14c_name_b-round-xx-token … hits=1` | start 20:34:12 / end 20:34:14 exit=0 unchanged |
| `solo_underscore` | underscore-name only | `killed by=u14c_name_b-underscore-name … hits=1` | start 20:34:16 / end 20:34:17 exit=0 unchanged |
| `loo_registry` | drop registry-suffix (3 left) | `killed by=u14c_name_b-nested-uppercase … hits=3` | start 20:34:19 / end 20:34:21 exit=0 unchanged |
| `loo_nested` | drop nested-uppercase | `killed by=u14c_name_b-registry-suffix … hits=3` | start 20:34:22 / end 20:34:24 exit=0 unchanged |
| `loo_xx` | drop round-xx-token | `killed by=u14c_name_b-registry-suffix … hits=3` | start 20:34:26 / end 20:34:28 exit=0 unchanged |
| `loo_underscore` | drop underscore-name | `killed by=u14c_name_b-registry-suffix … hits=3` | start 20:34:30 / end 20:34:32 exit=0 unchanged |

Reading: **every fixture alone kills U14c** (`hits=1`, one fixture in the battery), and every one-fixture-out
battery still kills (`hits=3`). No single fixture is the sole load bearer, so the module's kill is not an
artefact of one shape; the four shapes are redundant *witnesses* of the same branch, not four distinct
signals — the counter reports only the first killer. Every one of the eight runs printed
`wrong=0 tampered=0 sidechannel=0` and `null_detected=0 unattributed=0`. Receipts: `receipts/lb_*.txt`.

## 6. Specificity control — are the histories answerable without the name defect?

`controls/u14c_name_b_ctl.py` repeats the same four histories with a **parseable** claims name. If the exit-2
above were an artefact of the histories rather than the name guard, these twins would not answer 0/0/1/1.

```
ENVELOPE start 20:34:54 cwd=/fast/scratch/hyaku/kengaku-r44/R44BatU14b
PINS total=2 mismatched=0
FIXTURE u14c_name_b-ctl-registry-parseable tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u14c_name_b-ctl-nested-parseable tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u14c_name_b-ctl-inverted-parseable tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE u14c_name_b-ctl-onecommit-parseable tool=order expect=reject declared=- observed_rc=1 observed=- ok
MUTANT U14c order error SURVIVED exhibits=none -- plans/order_check.py:26-27 'Exit: 0 order holds · 1 order broken · 2 setup error (... unpa
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0 unattributed=0
PINS-AFTER mismatched=0
ENVELOPE end 20:34:56 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
(`exit=1` is the counter's dev-mode exit for `survived=1`, which is the intended control result.)
So: the registry and nested histories accept (0), the inverted and one-commit histories reject (1) on their
own merits; only the unparseable name makes the delivered fixtures exit 2, and with the name fixed the mutant
behaves exactly like the reference (`SURVIVED exhibits=none`). Receipt: `receipts/ctl_run.txt`.

## 7. Direction measured by hand (reference vs the same mutant)

Fixtures materialised once with the counter's own `--build-module` entry, inside the envelope
(`ENVELOPE start 20:35:22 / end 20:35:23 exit=0 … unchanged`, `BUILT [...]` 4 fixtures). Then, inside the
envelope (`ENVELOPE start 20:35:32 / end 20:35:33 exit=0 … unchanged`, receipt `receipts/direction.txt`):

```
registry-suffix REFERENCE                  rc=2 | ORDER ERROR claims file name is not round-NN-claims.md: plans/round-51-claims.md.orig
registry-suffix U14c-mutant                rc=1 |
nested-uppercase REFERENCE                 rc=2 | ORDER ERROR claims file name is not round-NN-claims.md: notes/history/Round-7-claims.md
nested-uppercase U14c-mutant               rc=1 |
round-xx-token REFERENCE                   rc=2 | ORDER ERROR claims file name is not round-NN-claims.md: plans/round-xx-claims.md
round-xx-token U14c-mutant                 rc=1 |
underscore-name REFERENCE                  rc=2 | ORDER ERROR claims file name is not round-NN-claims.md: plans/round_44_claims.md
underscore-name U14c-mutant                rc=1 |
--- mutant traceback shape (registry fixture)
  File "/fast/scratch/hyaku/kengaku-r44/R44BatU14b/mut/order_u14c.py", line 163, in main
    round_no = int(m.group(1))
                   ^^^^^^^
AttributeError: 'NoneType' object has no attribute 'group'
--- reference stderr (registry fixture)
ORDER ERROR claims file name is not round-NN-claims.md: plans/round-51-claims.md.orig
ORDER RESULT ERROR
```
Declared direction `error` (2 → 0 or 1) holds on all four fixtures, 2 → 1, with the reference's own
`ORDER ERROR` sentence as the cause.

## 8. Full default counter with the module in the clone's `plans/battery44/`

```
$ cp …/wave/R44BatU14b/battery/u14c_name_b.py "$S/lane/plans/battery44/"
$ envelope.sh "$S/env" python3 …/plans/round44_c1_verify.py --lane "$S/lane" --work "$S/w2"
```
```
ENVELOPE start 20:35:03 cwd=/fast/scratch/hyaku/kengaku-r44/R44BatU14b
PINS total=2 mismatched=0
FIXTURE u14c_name_b-registry-suffix tool=order expect=error declared=- observed_rc=2 observed=- ok
FIXTURE u14c_name_b-nested-uppercase tool=order expect=error declared=- observed_rc=2 observed=- ok
FIXTURE u14c_name_b-round-xx-token tool=order expect=error declared=- observed_rc=2 observed=- ok
FIXTURE u14c_name_b-underscore-name tool=order expect=error declared=- observed_rc=2 observed=- ok
MUTANT U5 anchor silence SURVIVED exhibits=none -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
MUTANT U6 anchor silence SURVIVED exhibits=none -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
MUTANT U7 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:98-99 'A token that resolves to several of the row's captures
MUTANT U9 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:106-107 'lessons are read from the working tree for paths com
MUTANT U14c order error killed by=u14c_name_b-registry-suffix attributed=L161 value=differs hits=4 -- plans/order_check.py:26-27 'Exit: 0 order holds · 1 order broken · 2 setup error (... unpa
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=5 killed=1 survived=4 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/4 order=1/1
ADVERTISED direct=5 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 20:35:05 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
This is the expected development shape for one seat: order floor met `order=1/1`, the four anchor mutants
survive because no anchor module is in this clone (other seats own them), and the predicate fails only on the
missing anchor work. Receipt: `receipts/full_run.txt`.

## 9. Limits

1. **Exit-code only.** The order gate prints no `class=` token, so no fixture can show a class difference and
   `defects=[]` is forced by the contract. The kill is a reference-rc vs mutant-rc difference, nothing richer.
2. **Redundant witnesses, not four signals.** `hits=4`: all four fixtures exhibit and the counter names only
   the first killer (`registry-suffix`). The solo table shows each is individually load-bearing, but a reader
   should not count four independent confirmations.
3. **The mutant dies by crash.** Its exit 1 is an `AttributeError` at `order_check.py:163`, and direction
   `error` accepts 0 or 1, so the same fixture would also kill a mutant that silently continued and returned 0.
   The fixture cannot distinguish the two ends of the declared window; only the measured rc (1) pins which one
   happened on this host.
4. **CPython-version sensitivity.** The `if False:` line survives as a `NOP` with a line event on the host's
   Python 3.14.8, which is what makes the span execution (`attributed=L161`) observable. An interpreter that
   dropped the line event entirely would turn these hits into `span-not-run` (unattributed), not into a false
   kill. The batch host's python3 stands in for the graded environment.
5. **Control scoped to these histories.** §6 shows the four delivered histories are answerable with the name
   fixed; it does not show that every conceivable order-gate history is.
6. **Independence is by construction, not verified.** I never read `claims/witness/w_u.py` or the sibling
   U14c module, so this module is not derived from them; the counter cannot see intent, so non-author review
   of "not a re-spelling" is still required at admission (as the freeze states).
7. **One module only.** The clone's `plans/battery44/` holds this module alone in §8; the lane's `plans/battery44`
   does not exist and was deliberately not created (lane files are the L1's to integrate).
8. **Envelope discipline.** Every counter/battery/tool run above ran under `claims/envelope.sh`; all twelve
   receipts show `local_bin_content_before = local_bin_content_after = 328be01808ba022f unchanged`, so no
   PATH-directory content moved. `~/.local/bin` was never written; no tool was installed or upgraded.
9. **No scratch remains.** `$S` was removed with `plans/scratch_guard.py safe-rm` after the receipts were
   copied into `receipts/`; the receipt files quoted above are the retained evidence.

VERDICT: battery44-u14c_name_b-U14c-killed-yes-fixtures-4
