# R42R5Carried — round-41 closure R5: `round_close.py --selftest` second run on the same `--work`

Seat: R42R5Carried (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (tip `fda71ae033224e1d0ed5ddd0fdcb1b63a02f2473`, "round-42: wave-1 spec and dispatch").
Scratch: `/fast/scratch/hyaku/kengaku-r42/R42R5Carried` (removed at exit). Nothing in the lane, `plans/`, `corpus/`, the fleet root, `~/.local/bin` or any PATH dir was written.

Measured claim (round-41 R5): `python3 plans/round_close.py --lane <clone> --census <census> --selftest --work DIR` run **twice on the same DIR** dies with a `CalledProcessError` traceback on the second run.

## 1. Re-measured at the tip: still red, same lines

Tip bytes are unchanged since round 41: `sha256sum` of the pristine clone's `plans/round_close.py` is
`112b52f0051357491b1654932948989d57b923c22bea817c15b710e5f9785c3b`, byte-identical to the `sha` field of
`.ufo/waves/round-41/build/R41PlanNext/res_round_close.json` (the round-41 mutation harness's base hash).

Envelope used for every run (host-safety rule):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <cmd>
```
with `HOME=<scratch>/home PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`. `~/Projects/shokunin/scripts/sources-census.sh` is the census (the lane has no `scripts/`).

Run 1 (fresh `--work`, `17:27:59`→`17:28:02`): `SELFTEST checks=5 ok=5 failed=0`, rc 0.
Run 2 (same `--work` DIR, `17:28:15`): rc 1, traceback identical in shape to the round-41 receipt
(`.ufo/waves/round-41/build/R41PlanNext/round_close-selftest-second-run-traceback.txt`):

```
plans/round_close.py", line 316, in main        return selftest(lane, census, ...)
plans/round_close.py", line 284, in selftest    build_fixture(root, lane, control, shape)
plans/round_close.py", line 275, in build_fixture    commit("receipt")
plans/round_close.py", line 241, in commit      subprocess.run([...], check=True, ...)
subprocess.CalledProcessError: Command '['git', '-C', '.../w/A-excused-p10', ..., 'commit', '-q', '-m', 'receipt']' returned non-zero exit status 1
```

The underlying git refusal, run by hand on the reused fixture:
`git -C w/A-excused-p10 ... commit -m receipt` → `On branch main` / `nothing to commit, working tree clean`, rc 1.

## 2. Cause (file:line)

`plans/round_close.py` (pre-patch numbering):

* `:279-280` `selftest` reuses the caller's `--work` verbatim: `base = work or …` then `base.mkdir(parents=True, exist_ok=True)` — nothing clears the previous run's fixture directories.
* `:236-283` `build_fixture(root, …)` assumes `root` is empty; the only reset is `git init -q` at `:261`, which on an existing repo is a no-op on content.
* `:239-242` `commit()` runs `git add -A` + `git commit -q -m <msg>` with `check=True`.

Second run, case `A-excused-p10` (shape `receipt-last`): `write_claims()` writes the same bytes → no diff; `cp -a` at `:258` copies `corpus/knowledge`/`corpus/lessons` **into** the existing destinations, so it nests `corpus/knowledge/knowledge` and `corpus/lessons/lessons`; `git add -A` therefore stages those new files and `commit("freeze")` succeeds (third commit `a3a7f4f freeze` on top of `9e73bb5 freeze`, `7197482 receipt`); the receipt bytes are also unchanged, so `commit("receipt")` at `:275` finds a clean tree, git exits 1, and `check=True` at `:241` raises. The traceback aborts the whole selftest, so cases B–E never run and no `SELFTEST checks=` line is printed.

Two defects behind one crash: (i) no reset of the reused fixture root; (ii) consequently `cp -a` nests the copied trees (observed: `w/A-excused-p10/corpus/knowledge/knowledge/` existed after run 2, before the abort). A `--allow-empty` commit alone would hide the crash but keep the polluted tree; clearing the root fixes both.

## 3. Frozen-pin check: **no pin — the fix need not wait**

```
$ for f in .ufo/waves/round-*/claims/frozen-digests.txt; do grep -n "round_close" "$f" || echo "(no round_close)"; done
(no round_close)     # rounds 37, 38, 39, 40, 41, 42  (rounds 25-36 have no frozen-digests.txt)
```
The round-42 list (12 lines) pins only `plans/round-42-claims.md`, `round42_c1_verify.py`, `round42_c2_verify.py`, `fibsqrt_probe.py`, `pkg-spec-r42.json`, `pkg_gate.py`, `anchor_digest_check.py`, `order_check.py`, the round-42 dry table, `tb2-circuit-fibsqrt/SHA256SUMS` and the two witness modules — not `plans/round_close.py`. `plans/round-42-claims.md:62` names `round_close.py` survivors only as an open (non-frozen) item. The round-41 R5 item therefore stays actionable; integration is the L1's (seats never edit the lane).

## 4. Draft patch (smallest fix)

`round_close-rerun-work-reuse.patch` (8 insertions, 0 deletions; sha256 `c5fb1b1048b77c485433e051b6e9dab2447e21e0d925aae94f7c2b59a8de15ac`), against tip `fda71ae`:

```diff
--- i/plans/round_close.py
+++ w/plans/round_close.py
@@ -68,6 +68,7 @@ import hashlib
 import os
 import re
 import shlex
+import shutil
 import subprocess
 import sys
 import tempfile
@@ -236,6 +237,13 @@ FIXTURE_RECEIPT = "CASE c01 observed=PASS predicted=PASS\n"
 def build_fixture(root: Path, lane: Path, control: str | None, shape: str) -> None:
     """A minimal lane-shaped repo whose only difference between cases is commit order."""
 
+    # A reused --work still holds the last run's fixture: clear it first, or `cp -a` nests the
+    # copied trees and `git commit` finds nothing to commit (exit 1, raised by check=True).
+    if root.is_symlink() or root.is_file():
+        root.unlink()
+    elif root.is_dir():
+        shutil.rmtree(root)
+
     def commit(msg: str) -> None:
```

Why here: `build_fixture` is the only writer of a fixture root and is called once per case id, so it is the single place that must guarantee an empty `root`; `selftest` keeps its `--work` semantics ("scratch parent", reused) and its output is unchanged. The `is_symlink()/is_file()` branch also removes a symlink planted at `<work>/<case-id>`, which would otherwise make the run write through it (tested, §5.3) or crash in `mkdir(exist_ok=True)`.

Verify the draft is complete and compiles:
```
$ git -C lane-red apply --check round_close-rerun-work-reuse.patch   # APPLY_CHECK_OK on pristine tip
$ git -C lane-red apply      round_close-rerun-work-reuse.patch
$ sha256sum lane-red/plans/round_close.py lane/plans/round_close.py
0148c8e7680d6cd06dc99295cbac6453926008b98f0223bc760c938b41b288f5  lane-red/plans/round_close.py
0148c8e7680d6cd06dc99295cbac6453926008b98f0223bc760c938b41b288f5  lane/plans/round_close.py
$ python3 -c "compile(open('lane/plans/round_close.py').read(),'round_close.py','exec'); print('COMPILES 16311')"
$ git -C lane-red apply -R round_close-rerun-work-reuse.patch   # REVERTED -> sha back to 112b52f0…
```
(The reverse apply also returns the control clone to the pristine sha, so the red lane was byte-exact at tip for §5.)

## 5. Check command: red before, green after

`check.sh LANE [WORK]` (sha256 `62b7e85fef912689dc8a353939aa19654a9d49ca696b0e3b3717b4fe11e1ad63`) runs the selftest twice on the same `--work` inside the envelope and asserts: run 1 rc 0; run 2 rc 0; run 2 stdout byte-identical to run 1; no nested `corpus/knowledge/knowledge`. It prints Q32 evidence (`date +%T`, `ls -A ~/.local/bin | sha256sum`) before and after.

```
$ check.sh <scratch>/lane-red <scratch>/w-red2      # control clone = tip bytes, unpatched
CHECK run1_rc=0 run2_rc=1
CHECK run2_tail: subprocess.CalledProcessError: Command '['git', '-C', '<scratch>/w-red2/A-excused-p10', …, 'commit', '-q', '-m', 'receipt']' returned non-zero exit status 1.
CHECK FAIL run 2 exit=1 (rerun on an existing --work)
CHECK FAIL run 2 output differs from run 1
CHECK FAIL nested corpus/knowledge/knowledge from a second 'cp -a'
RED_RC=1

$ check.sh <scratch>/lane <scratch>/w-green2        # patched clone
CHECK run1_rc=0 run2_rc=0
CHECK run1=5 cases; tail: SELFTEST checks=5 ok=5 failed=0
CHECK run2_tail: SELFTEST checks=5 ok=5 failed=0
CHECK PASS rc=0 twice, identical output, no nested copy
GREEN_RC=0
```
Raw receipts: `red-run.txt` (sha256 `55dba869…`), `green-run.txt` (sha256 `211c73a7…`).

Extra measures, all on the patched clone:
1. third run on the same `--work` (`w-green`) → `SELFTEST checks=5 ok=5 failed=0`, rc 0 (idempotent beyond two runs).
2. no `--work` at all (fresh temp) → `SELFTEST checks=5 ok=5 failed=0`, rc 0 (default path unchanged).
3. reused `--work` with `<work>/A-excused-p10` as a symlink to an empty victim dir → run rc 0, `victim/` still contains only `.keep`, `<work>/A-excused-p10` is no longer a symlink (the parent cannot be used to redirect fixture writes).
4. non-selftest gate path unchanged: `round_close.py --lane lane --round 42 --census …` → `ROUND-CLOSE census exit=0 warnings=15 verdict=PASS`, `ROUND-CLOSE RESULT PASS exit=0`, rc 0.

## 6. Risks / notes for integration

* **Line-number re-key.** The patch inserts 1 line after `:70` and 7 lines at `:237`; lines ≥237 shift by +8 and lines 71–236 by +1. Round-41's `R41RoundCloseMut` survivor rows and any counter that quotes `round_close.py:<line>` by number must be re-derived (the harness parses lines itself; recorded rows in `res_round_close.json` are keyed by the old numbers). Post-patch: `commit("receipt")` 283, `selftest` def 286, `cp -a` 265, `git init` 268.
* The fix deletes only `<work>/<case-id>` (fixture roots the selftest itself created), never `<work>` itself and never the default temp parent; `--work` is documented as a scratch parent, so no caller data is at risk.
* The patch is a draft for the L1: it is **not** applied to the lane, and `plans/round_close.py` must be updated together with nothing else (no frozen digest, no counter, no claims row changes because the selftest summary text is byte-identical).
* The symlink branch was added beyond the bare crash fix because the same reused-`--work` hole allowed writes outside the fixture root; if the L1 prefers the 2-line minimum, dropping `if root.is_symlink() or root.is_file(): root.unlink()` and keeping `if root.is_dir(): shutil.rmtree(root)` still turns the check green (the symlink case then crashes at `mkdir(exist_ok=True)`, never writes through).
* Q32 note: the harness shell's `ls` is a wrapper that groups directories first, so `ls -A ~/.local/bin | sha256sum` reads `436b361f…` there, while GNU `ls` under the fixed system PATH reads `763032563d…`. The entry **set** is identical (100 names; `sort` of both listings → `763032563d…`). Pre==post inside every run (with the same `ls`); no run of mine wrote to `~/.local/bin` (it is `--ro-bind`ed inside the envelope).

## 7. Verdict

Cause found and reproduced at the tip (`plans/round_close.py:275` → `:241`, from `selftest:279-284` reusing `--work` with no fixture reset, plus the `cp -a` nesting at `:258`). No frozen digest list pins `round_close.py`, so the fix does not have to wait. Smallest fix drafted as an 8-line patch with a red→green check; not applied to the lane.

VERDICT: r5-round-close-rerun-fixed-draft
