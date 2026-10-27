# R44LabratRerun — C2 receipt re-run: byte determinism and -O3 sensitivity

Seat: R44LabratRerun (executor, leaf). Round 44 wave, hypothesis item: the C2 receipt
`corpus/evidence/round44/feal-linear-probe.txt` is byte-equal on re-run in a clean `--no-local` clone (3 runs:
normal, `env -i PATH=/usr/bin:/bin`, a different `--work` root), and its oracle case does not depend on `-O3`.

Read-only use of the lane; every write went to `$S=/fast/scratch/hyaku/kengaku-r44/R44LabratRerun` and to this
report's own subdir `.ufo/waves/round-44/wave/R44LabratRerun/`. No lane, corpus, plans or fleet-root file was
written; `git -C "$S/lane" status --porcelain` printed 0 lines after all runs.

## 1. Fixture: clean `--no-local` clone

```
S=/fast/scratch/hyaku/kengaku-r44/R44LabratRerun; mkdir -p "$S"; export TMPDIR="$S"
git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel   -> /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/lane
git -C "$S/lane" rev-parse HEAD              -> 5e3d3aa06c6b7000929ac3e62563a39159c4501f
ls "$S/lane/.git/objects/info/alternates"    -> No such file or directory   (no alternates: nothing shared)
git -C "$S/lane" count-objects -v            -> count: 0, in-pack: 11737
```

Frozen files inside the clone carry the digests of `.ufo/waves/round-44/claims/frozen-digests.txt`:

```
0e7a59dab76266a167d9c3f51dd01817f7cec2f62896689bc488947dce545297  plans/feal_linear_probe.py
40308211216be063084eb9a1f22faded5a8550d392a83f6e13545e2ddae205a0  corpus/evidence/round44/feal-linear-probe.txt
```

Host tools used by the probe: Python 3.14.8 (`/usr/bin/python3`), gcc 16.2.1 20260810, bubblewrap 0.13.1.
The probe's own bwrap sandbox nests inside the round-44 envelope's bwrap in every run below (worked 7/7).

## 2. Three re-runs, each under `claims/envelope.sh` (cwd `$S/lane`)

Each run's stdout was split into the ENVELOPE lines (`run*.env`) and the probe body (`run*.body`); the body was
`cmp`-ed against `$S/lane/corpus/evidence/round44/feal-linear-probe.txt`.

| run | command (beyond the envelope) | host env | `--work` | envelope window | `~/.local/bin` digest before/after | cmp |
|---|---|---|---|---|---|---|
| 1 | `/usr/bin/python3 plans/feal_linear_probe.py --lane . --work $S/w1` | host env, `TMPDIR=$S` | `$S/w1` | 20:33:47 → 20:33:53, exit 0 | `328be01808ba022f` / `328be01808ba022f` unchanged | **equal** |
| 2 | same | `env -i PATH=/usr/bin:/bin` | `$S/w2` | 20:34:02 → 20:34:09, exit 0 | `328be01808ba022f` / `328be01808ba022f` unchanged | **equal** |
| 3 | same | host env, `TMPDIR=$S` | `$S/w3root/nested/deeper` (did not exist) | 20:34:23 → 20:34:29, exit 0 | `328be01808ba022f` / `328be01808ba022f` unchanged | **equal** |

```
$ cmp lane/corpus/evidence/round44/feal-linear-probe.txt run1.body   -> equal   (rc 0)
$ cmp lane/corpus/evidence/round44/feal-linear-probe.txt run2.body   -> equal   (rc 0)
$ cmp lane/corpus/evidence/round44/feal-linear-probe.txt run3.body   -> equal   (rc 0)
40308211216be063084eb9a1f22faded5a8550d392a83f6e13545e2ddae205a0  run1.body
40308211216be063084eb9a1f22faded5a8550d392a83f6e13545e2ddae205a0  run2.body
40308211216be063084eb9a1f22faded5a8550d392a83f6e13545e2ddae205a0  run3.body
```

Fourth, independent observation (not mine): the L1's first recorded run,
`.ufo/waves/round-44/first-run/envelope-probe.txt` (20:22:23 → 20:22:27, `--work .../L1/fr`), has the same body:

```
body of that file (ENVELOPE lines stripped) == receipt  -> True
40308211216be063084eb9a1f22faded5a8550d392a83f6e13545e2ddae205a0  firstrun.body
```

Every body also carries the same tail, as in the frozen receipt:

```
regrade cases=14 differ=0
cases=14 observed_pass=8 observed_fail=6 mismatches=0
```

Note on method (calibration): run 3 was first launched with the same `env -i` environment as run 2 and then
re-run with the host environment, so that the retained run 3 isolates the `--work` variable; only the second
run 3 is reported above. The first run-3 attempt (`env -i`, different `--work`) was also byte-equal.

ENVELOPE lines (verbatim, one block per run):

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/env1 /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/env1 --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/env1/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 plans/feal_linear_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/w1
ENVELOPE start 20:33:47 cwd=/fast/scratch/hyaku/kengaku-r44/R44LabratRerun/lane
ENVELOPE end 20:33:53 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/env2 /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/env2 --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/env2/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 plans/feal_linear_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/w2
ENVELOPE start 20:34:02 cwd=/fast/scratch/hyaku/kengaku-r44/R44LabratRerun/lane
ENVELOPE end 20:34:09 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/env3 /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/env3 --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/env3/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 plans/feal_linear_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/w3root/nested/deeper
ENVELOPE start 20:34:23 cwd=/fast/scratch/hyaku/kengaku-r44/R44LabratRerun/lane
ENVELOPE end 20:34:29 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

## 3. Is the oracle case `-O3`-dependent? Rebuild at `-O0`

Scratch copy of the probe and of the captures (the frozen files were never touched):

```
cp -a "$S/lane/corpus/evidence/round44/tb2-feal-linear-cryptanalysis" "$S/opt0/cap"
cp "$S/lane/plans/feal_linear_probe.py" "$S/opt0/probe_o0.py"
$S/opt0/cap/solve.sh: "gcc -o attack attack.c -O3" -> "gcc -o attack attack.c -O0"
  -> sha256 6e10c9fbd0e53d5c5d3a86e8496800be5d14848b883350f0d612a34ca43b8768, grep -c -O3 = 0
$S/opt0/probe_o0.py: CAP -> the absolute scratch capture dir; SEED "gcc -O3" x2 -> "gcc -O0"; PINS["solve.sh"] -> above
  -> diff vs the frozen probe = 27 lines (evidence: probe_o0.diff), no other change; only docstring mentions -O3
```

Run (envelope):

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/env0 /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/env0 --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/env0/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/opt0/probe_o0.py --lane . --work /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/w0
ENVELOPE start 20:35:03 cwd=/fast/scratch/hyaku/kengaku-r44/R44LabratRerun/lane
ENVELOPE end 20:35:09 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`diff -u receipt run_o0.body` (11 lines, evidence `run_o0.diff`) — one changed line, the pin echo; **all 14 CASE
lines and the two tail lines are identical**:

```
-# capture solve.sh sha256=be50ae01a3ea850a6dc4bc99dc130d0b7ad37963c85544a02b03a4f5da29cb77
+# capture solve.sh sha256=6e10c9fbd0e53d5c5d3a86e8496800be5d14848b883350f0d612a34ca43b8768
```

So at `-O0`: `oracle-solve-sh`, `oracle-concatenated`, `oracle-plus-decoys`, `oracle-reversed`,
`oracle-zero-padded` all still `observed=pass`, `regrade=same`; the six failing cases still fail; the tail is
`regrade cases=14 differ=0` / `cases=14 observed_pass=8 observed_fail=6 mismatches=0`.

Byte-level cross-check (own scratch probe `optcmp.py`, evidence copy; same bwrap recipe as the frozen probe,
`/app` left on disk for `cmp`):

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/envc3 /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/envc3 --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/envc3/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/optcmp.py --opt 3 --label o3 --work /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/optcmp
ENVELOPE start 20:35:52 cwd=/fast/scratch/hyaku/kengaku-r44/R44LabratRerun/lane
OPT o3 opt=-O3 mode=oracle rc=0 plaintexts=sha256=51a7965207d49ff5ebf13234acae67cda812710b6396827add32d4adb5da4712 lines=265 decimals=99 maybe=161
FOUND o3 Found 68e63 (-1303524760) for round 0
FOUND o3 Found 62571 (219456344) for round 1
FOUND o3 Found 1f61c (-1467418080) for round 2
ENVELOPE end 20:35:53 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/envc0 /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/envc0 --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/envc0/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/optcmp.py --opt 0 --label o0 --work /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/optcmp
ENVELOPE start 20:35:55 cwd=/fast/scratch/hyaku/kengaku-r44/R44LabratRerun/lane
OPT o0 opt=-O0 mode=oracle rc=0 plaintexts=sha256=51a7965207d49ff5ebf13234acae67cda812710b6396827add32d4adb5da4712 lines=265 decimals=99 maybe=161
FOUND o0 Found 68e63 (-1303524760) for round 0
FOUND o0 Found 62571 (219456344) for round 1
FOUND o0 Found 1f61c (-1467418080) for round 2
ENVELOPE end 20:35:57 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/envc0a /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/envc0a --bind /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/envc0a/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/optcmp.py --opt 0 --label o0-atk --work /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/optcmp --donor /fast/scratch/hyaku/kengaku-r44/R44LabratRerun/optcmp/optcmp-o3-odhtpf0n/
ENVELOPE start 20:35:59 cwd=/fast/scratch/hyaku/kengaku-r44/R44LabratRerun/lane
OPT o0-atk opt=-O0 mode=attack rc=0 plaintexts=sha256=51a7965207d49ff5ebf13234acae67cda812710b6396827add32d4adb5da4712 lines=265 decimals=99 maybe=161
FOUND o0-atk Found 68e63 (-1303524760) for round 0
FOUND o0-atk Found 62571 (219456344) for round 1
FOUND o0-atk Found 1f61c (-1467418080) for round 2
ENVELOPE end 20:36:01 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`o0-atk` reuses the `-O3` run's `pairs.txt`/`ciphertexts.txt` and only recompiles `attack` at `-O0`, so it isolates
the attack from the `feal`/`gen.py` rebuild. Results:

```
$ cmp A3/app/plaintexts.txt A0/app/plaintexts.txt      -> equal   (oracle: -O3 vs -O0)
$ cmp A3/app/plaintexts.txt A0A/app/plaintexts.txt     -> equal   (attack only: -O3 vs -O0)
$ cmp A3/app/pairs.txt A0/app/pairs.txt                -> equal   (feal rebuild at -O0 gives the same pairs)
51a7965207d49ff5ebf13234acae67cda812710b6396827add32d4adb5da4712  A3/app/plaintexts.txt
51a7965207d49ff5ebf13234acae67cda812710b6396827add32d4adb5da4712  A0/app/plaintexts.txt
51a7965207d49ff5ebf13234acae67cda812710b6396827add32d4adb5da4712  A0A/app/plaintexts.txt
```

Same 265 lines, same three recovered round keys, same `Maybe` lines, at every level — the oracle's result is not
an optimisation artefact on this toolchain.

Side observation (not used for the verdict, reported because it is visible in the evidence): `/app/plaintexts.txt`
interleaves the attack's `Maybe`/`Found` stdout with the decrypted plaintexts, and one plaintext is embedded in a
truncated attack line — line 147 is `Ma1050628112036199672`. The oracle case still passes because the grader's
`assert c in data` is a substring test over the whole file (`test_outputs.py:121-122`); this is the frozen C2
reading, and it is byte-identical at `-O0` and `-O3`, so the pass does not rest on a compiler-specific
interleaving.

## 4. Limits

- Host `python3` 3.14.8 and host gcc 16.2.1 stand in for the image's python 3.13 (`uvx`) and Debian bookworm gcc
  (the frozen probe's stated limit). The `-O0` experiment therefore tests host-gcc sensitivity, not the Debian
  toolchain; the task image is never pulled.
- `-O0` is one point only. Other levels/flags (`-O1/-O2/-Os`, `-fno-strict-aliasing`) were not tested.
- Only the probe/grader path was re-run. The V11 predictor, the C2 counter and the C1 side were not re-run by this
  seat.
- Determinism is shown for the probe on this host: 3 own runs + the L1's first-run body (4 total), including a
  sanitized environment and three distinct `--work` roots. A different host/kernel is not covered.

## 5. Files and evidence (all in this report's subdir, 72 KiB, 16 files)

```
40308211216be063084eb9a1f22faded5a8550d392a83f6e13545e2ddae205a0  run1.body        run2.body        run3.body   firstrun.body
21df02d1cbd98b512a099bdb6d0aa3292e7441320224c397c794411d5b3fc1cf  run1.env
0e3cc6f450dea8824bee76595c3c6e351d195b30ee5ea063f207536e733db40d  run2.env
4cf4279be6bbdec07090a319525e6fc32a5ccd456feead973b4070ddf1089b65  run3.env
82b1f31f3445d561671e2160e095531f3683148ae93c17979aee8fa138173607  run_o0.body
e2e286be18601052fee32466358f1300a610ab385b9fa1c42ba552a442a57919  run_o0.env
d94c3fd6875ca9097236a05203ecf72980f221a8e87ab01ddef3e3381f26dfdf  run_o0.diff
9461b2964ff7493c9114be0d7d15aa6bc3fbdaf16ad6961d8a69a7127c25cfb3  probe_o0.diff
12cb2a971bd5773db2c4d27bbb5c1fb6e46de1b2992303bb999e5daca419951c  optcmp.py
de86ab6cc55518084a205233bf8adb5a654dabe3e0e97bcd787f2a267fd5f231  o3.full
3d6e44aef766078385992b974628cd1b8273d84ce695f65e5f78ea944f665286  o0.full
a87eb98f22a2fc6d354c33e67f2558d42861793c70d01ff581ca2f65e3cbf86d  o0atk.full
51a7965207d49ff5ebf13234acae67cda812710b6396827add32d4adb5da4712  oracle-o3-plaintexts.txt
```

Scratch `/fast/scratch/hyaku/kengaku-r44/R44LabratRerun` removed after the copies above were made, with
`plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r44 R44LabratRerun "$S"`. No tool was installed or
upgraded; no lane or fleet-root file was written; nothing was committed.

VERDICT: rerun-byte-equal-3/3-opt-sensitive-no
