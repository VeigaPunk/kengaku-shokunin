# R49C2ExecProbe — round-49 C2 (coverage): the hardened probe repaired to v2 (grade path runs seed+recipe; `--nproc` measured per run), with the three falsifiable controls the frozen C2 row needs

Seat `R49C2ExecProbe` (executor, leaf, no dispatch). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
**read-only** for this seat; the only lane writes are this report and its sibling artifact
`.ufo/waves/round-49/w1/R49C2ExecProbe/probe_v2.py`. Scratch `S=/fast/scratch/hyaku/kengaku-r49/R49C2ExecProbe`
(NVMe), `TMPDIR=$S`, one `git clone --shared` of the lane, scratch tree removed at yield (§9).

**Axes named before the work** (this seat serves R49-C2, worked axis `coverage`):

1. **coverage** — do the 18 frozen cases actually build their end states on the *grade* path, i.e. does the probe
   exercise the recipes its own case table describes? (This is the leg V7/V14 must be able to score; a grade path
   that never runs a recipe measures nothing.)
2. **freeze integrity** — is the repair applied to the exact committed artifact revision (`22b7779e…`), with the
   case table, tags, predictions and dry table unchanged, and every capture pin still verified?
3. **operability** — does the permitted pre-stage-2 mode (`--stage-check`) run on this host today? The frozen C2 row
   names this as the fresh falsifiable control the stage-2 amendment must pass (claims §C2 (e)).

**Mutation of scope:** none. No scored counter run, no full probe run (Q30), no counter/fence/package byte edited,
no claim admission asserted.

---

## 0. Freeze verification (done before any measurement)

The item names base lane tip (stage-1 freeze) `9d2900af41e4d1fc6022eff99010436fde6dbd93`. Verified in the committed
lane tree before any scored/probe execution:

```
$ git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
commit
$ git log --format='%H %ci %s' -1 9d2900af…
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence
over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims
$ git merge-base --is-ancestor 9d2900af… HEAD
IS-ANCESTOR-OF-HEAD
$ git ls-tree 9d2900af… plans/round-49-claims.md
100644 blob 3ad92f056155b5cc0c3e2a60068b6b3cecf0c21d	plans/round-49-claims.md
$ git show 9d2900af…:plans/round-49-claims.md | sha256sum ; sha256sum plans/round-49-claims.md
7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83
7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83
$ git ls-tree 9d2900af… .ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py
100755 blob 5a89786ac2681893fd63ac629a818810620601bd	…/polyglot_c_py_probe.py
```

The freeze commit exists, is an ancestor of the lane HEAD (`af88aab`), carries the claims file byte-for-byte as
this seat read it, and carries the hardened probe at git blob `5a89786ac2681893fd63ac629a818810620601bd`, whose file
content sha256 is the `22b7779e…` digest the round-48 row names. Commit time `2026-10-28 09:14:40 -0300` predates
every measurement below (09:21–09:25). **No blocker: the measurements are permitted.**

Clone used for every run (read-only; nothing was written into it):

```
$ git clone --shared --no-checkout <lane> "$S/lane"
$ git -C "$S/lane" rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r49/R49C2ExecProbe/lane
$ git -C "$S/lane" checkout -q 9d2900af… ; git -C "$S/lane" rev-parse HEAD
9d2900af41e4d1fc6022eff99010436fde6dbd93
$ git -C "$S/lane" status --porcelain | wc -l
0
```

`REV 9d2900af41e4d1fc6022eff99010436fde6dbd93` (clean clone, no `TREE-BYTES`) — the revision every receipt below
measured. Host: `Python 3.14.8`, `bubblewrap 0.13.1`, uid 1000.

---

## 1. Deliverable

| file | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-49/w1/R49C2ExecProbe/probe_v2.py` | 35219 | `29c2387f26b1594e61a953f0ecca256ececbb917b4b65dc697be24690aacf340` |
| base revision (round-46 wave artifact, unmodified in the lane) | 31355 | `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d` |

`probe_v2.py` is the tested candidate byte-for-byte (transcribed with `cp`, then `cmp` IDENTICAL; `py_compile` OK on
both copies). It is the proposed stage-2 replacement for `plans/polyglot_c_py_probe.py`; this seat lands nothing.

Two repairs, 11 hunks, `+82 −20` lines (`diff -u <22b7779e> probe_v2.py`):

| # | site | change |
|---|---|---|
| i | `HARNESS_PY` guard (hunks at `@@ -319` and `@@ -349`) | `if mode in ("stage", "recipe")` → `if mode in ("stage", "recipe", "all")`; the terminal `sys.exit(0)` becomes `if mode != "all": sys.exit(0)`, so mode `all` runs `/seed.sh` + `/recipe.sh` and then continues into the two grade legs on the same `/app` tmpfs. A recipe that fails still `sys.exit(3)` before grading (surfaced by the caller as `SETUP case … sandbox failed (rc=3)`), never as a fabricated verdict. |
| ii | `LIMITS` / `sandbox_argv` / `harness` / `run_case` / `main` (hunks `@@ -104`, `-376`, `-399`, `-427`, `-439`, `-516`, `-540`) | the frozen `--nproc=48` leaves `LIMITS`; new `nproc_ceiling()` reads the real uid's live host-wide thread count from `/proc/*/status` and returns `threads + NPROC_HEADROOM` (256), else `NPROC_FALLBACK` (8192) when `/proc` is unreadable. `prlimit --nproc=<ceiling>` is built per run; `harness()` wraps the invocation and retries once at double headroom only when the sandbox produced *no output and rc=1* (the namespace-creation shape), so a sandbox that never started can never be read as a case verdict. |
| — | docstring (`@@ -16`, `-62`) | the ORDER-RULE text now states both repairs and the measured numbers they answer; the `--nproc=48` prose and the one-sandbox consequence (a) are corrected to the adaptive ceiling. No other byte moves: `CASES`, `TAGS`, `TEMPLATE`, `POLYGLOT`, `PINS`, `PUBLIC`, `CAP`, the five other prlimit bounds (`--cpu=5 --fsize=1048576 --core=0 --as=536870912 --nofile=512`), the bind set, `CAP_BYTES`, `TIMEOUT`, `SBOX_ENV`, `letters()`, `regrade_tag()`, `stage_line()` and both output formats are unchanged. |

Rationale for (ii) as a *measured* ceiling rather than a bigger constant: `RLIMIT_NPROC` is checked against the
**real uid's host-wide thread count**, not the sandbox's processes, so no constant is safe — the live count moved
between this seat's own runs (3093 → 3105 → 3103 → 3076 in four minutes) and the round-48 seat measured 1106–1146.
What the hardening actually needs to bound is the *spare* budget a recipe may fork into; that is now exactly
`NPROC_HEADROOM`, delivered regardless of host load. Dropping `--nproc` entirely was rejected: the one-sandbox
design shares a pid namespace across seed, recipe and both grade legs (docstring consequence (a)), and the ceiling is
the only thing bounding an orphan a recipe leaves behind.

---

## 2. Control (a) — `22b7779e` `--stage-check` on this host: FAIL (reproduced)

```
$ python3 "$S/orig/polyglot_c_py_probe_22b7779e.py" --lane "$S/lane" --stage-check --work "$S/work/sc-orig"
STAGECHECK nop rc=1 expect=absent file= dir=  match=NO
STAGECHECK oracle-solve-sh rc=1 expect=src file= dir=  match=NO
STAGECHECK lookup-table rc=1 expect=src file= dir=  match=NO
STAGECHECK python-only rc=1 expect=src file= dir=  match=NO
STAGECHECK c-only rc=1 expect=src file= dir=  match=NO
STAGECHECK extra-file rc=1 expect=src file= dir=  match=NO
STAGECHECK leftover-cmain rc=1 expect=src file= dir=  match=NO
STAGECHECK wrong-value rc=1 expect=src file= dir=  match=NO
STAGECHECK trailing-ws rc=1 expect=src file= dir=  match=NO
STAGECHECK nonzero-exit rc=1 expect=src file= dir=  match=NO
STAGECHECK stderr-noise rc=1 expect=src file= dir=  match=NO
STAGECHECK n-parsed-differently rc=1 expect=src file= dir=  match=NO
STAGECHECK compile-warning rc=1 expect=src file= dir=  match=NO
STAGECHECK regrade-same-state rc=1 expect=src file= dir=  match=NO
STAGECHECK empty-file rc=1 expect=src file= dir=  match=NO
STAGECHECK dir-in-place rc=1 expect=dir file= dir=  match=NO
STAGECHECK crlf-source rc=1 expect=src file= dir=  match=NO
STAGECHECK value-plus-line rc=1 expect=src file= dir=  match=NO
stagecheck cases=18 failed=18
exit=1
```

Cause, isolated with the probe's own argv shape (same binds, one `prlimit` value changed):

```
# nproc sweep, final candidate bytes sha256=29c2387f…, 2026-10-28T09:25:11-03:00
uid=1000 uid_threads=3105 nproc_ceiling=3361 headroom=256
nproc=48    rc=1 stdout='' stderr='bwrap: Creating new namespace failed: Resource temporarily unavailable'
nproc=3361  rc=0 stdout='sandbox-ok' stderr=''
nproc=6722  rc=0 stdout='sandbox-ok' stderr=''
```

Every `rc=1` row above is that namespace failure; the sandbox never starts, so no `file=`/`dir=` value is printed.
This is the round-48 measurement reproduced on a differently loaded host (then ~1100 threads, now ~3100).

**Additional before-receipt (not in the item, needed for the claims §C2 do-nothing control):** the `22b7779e`
revision's *mode-all* receipt also dies at the same gate before any case runs —

```
$ python3 driver/mode_all_stub.py orig/polyglot_c_py_probe_22b7779e.py "$S/lane" "$S/work/stub-asmode"
… SETUP case nop sandbox failed (rc=1)        (on stderr; probe exit 2, zero CASE lines)
```

---

## 3. Control (b) — v2 `--stage-check` on this host: PASS, and byte-identical to the round-46 record

```
$ python3 probe_v2.py --lane "$S/lane" --stage-check --work "$S/work/sc-final"
STAGECHECK nop rc=0 expect=absent file=absent dir=absent pycheck=n/a ccheck=n/a match=yes
STAGECHECK oracle-solve-sh rc=0 expect=src file=bytes=872 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK lookup-table rc=0 expect=src file=bytes=582 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK python-only rc=0 expect=src file=bytes=205 dir=main.py.c pycheck=ok ccheck=fail cwarn=0 match=yes
STAGECHECK c-only rc=0 expect=src file=bytes=288 dir=main.py.c pycheck=fail ccheck=ok cwarn=0 match=yes
STAGECHECK extra-file rc=0 expect=src file=bytes=872 dir=NOTES.md,main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK leftover-cmain rc=0 expect=src file=bytes=872 dir=cmain,main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK wrong-value rc=0 expect=src file=bytes=537 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK trailing-ws rc=0 expect=src file=bytes=513 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK nonzero-exit rc=0 expect=src file=bytes=502 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK stderr-noise rc=0 expect=src file=bytes=554 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK n-parsed-differently rc=0 expect=src file=bytes=482 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK compile-warning rc=0 expect=src file=bytes=522 dir=main.py.c pycheck=ok ccheck=ok cwarn=2 match=yes
STAGECHECK regrade-same-state rc=0 expect=src file=bytes=872 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK empty-file rc=0 expect=src file=bytes=0 dir=main.py.c pycheck=ok ccheck=ok cwarn=0 match=yes
STAGECHECK dir-in-place rc=0 expect=dir file=dir dir=main.py.c pycheck=n/a ccheck=n/a match=yes
STAGECHECK crlf-source rc=0 expect=src file=bytes=514 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK value-plus-line rc=0 expect=src file=bytes=524 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
stagecheck cases=18 failed=0
exit=0
```

Byte-identical to the table the round-46 seat recorded (`.ufo/waves/round-46/w1/R46ExecC3Probe.md:98-116`):

```
$ diff -u <r46 recorded 19 lines> <v2 stage-check 19 lines>   → no output
sha256 371470589eba33cb3361ac28bb6cb212dfd149a27197f8d976cd13becd3bf654   (both)
```

So the nproc repair restores the stage legs to their recorded values exactly — it changes no end state, no parse
verdict and no warning count. The same run also re-verified all seven capture pins (the probe checks them before any
case; a mismatch would have printed `SETUP capture …` and exited 2) and, per the ORDER RULE, imported no grader.

**Retry branch measured** (it is the host-load race mitigation, so it was exercised rather than assumed — only
`nproc_ceiling` patched to return 2000, i.e. below the live count):

```
RETRY-CONTROL uid_threads=3093 patched_ceiling=2000 (below the live count -> first attempt must fail)
stagecheck cases=18 failed=0
RETRY-CONTROL invocations=36 first_attempts=18 (all rc=1 with no output: True) retries=18 (all rc=0: True)
RETRY-CONTROL probe_exit=0
```

---

## 4. Control (c) — stub-grader mode-all run: the grade path now runs seed+recipe

The captured grader was **never imported**. In the scratch copy only, `CAP` was pointed at a copy of the frozen
capture directory whose `tests/test_outputs.py` is replaced by a stub (sha256
`958bab8172924bd2f64c95794b6e92655ddd2ca9926575150beede766c533e9e`), `PINS` was recomputed from that copy so the
probe's own digest check still runs, and the real capture file was left untouched (`real_grader_untouched=
b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec` — the lane pin). The stub reads the end state
only and reports it through the exception name the harness prints:

```python
# stub grader (scratch control); test_cases is a dummy point, never compared — the frozen `lookup-table`
# recipe AST-reads that name out of the public grader copy, so it must exist for that case to run.
import os
test_cases = [(0, "0")]
class DirMissing(Exception): pass
class NamesUnexpected(Exception): pass
def test_fibonacci_polyglot():
    if not os.path.isdir("/app/polyglot"):
        raise DirMissing("no /app/polyglot: the seed/recipe never ran")
    names = sorted(os.listdir("/app/polyglot"))
    if names != ["main.py.c"]:
        raise NamesUnexpected(",".join(names))
```

**Before** — `22b7779e`, with *only* the nproc defect neutralized (module-level `LIMITS` patched to
`--nproc=3427` + v2's other bounds; every other byte as committed), stub grader:

```
CONTROL nproc_neutralized=--nproc=3427 (v2 nproc_ceiling; all other bytes as committed)
CASE nop predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=single-file error=DirMissing -- …
CASE oracle-solve-sh predicted=pass observed=fail tests=F predicted_tests=P match=NO regrade=same violates= error=DirMissing -- …
CASE lookup-table predicted=pass observed=fail tests=F predicted_tests=P match=NO regrade=same violates=fib-kth error=DirMissing -- …
CASE trailing-ws predicted=pass observed=fail tests=F predicted_tests=P match=NO regrade=same violates= error=DirMissing -- …
CASE stderr-noise predicted=pass observed=fail tests=F predicted_tests=P match=NO regrade=same violates= error=DirMissing -- …
CASE compile-warning predicted=pass observed=fail tests=F predicted_tests=P match=NO regrade=same violates= error=DirMissing -- …
CASE regrade-same-state predicted=pass observed=fail tests=F predicted_tests=P match=NO regrade=same violates=single-file error=DirMissing -- …
CASE crlf-source predicted=pass observed=fail tests=F predicted_tests=P match=NO regrade=same violates= error=DirMissing -- …
cases=18 observed_pass=0 observed_fail=18 mismatches=7
RAW-BEGIN oracle-solve-sh
TEST leg1 F error=DirMissing
TEST leg2 F error=DirMissing
RAW-END oracle-solve-sh
STAGE lines printed: 0
```

`observed_pass=0 observed_fail=18 mismatches=7` is the round-48 figure reproduced exactly, and **zero** `STAGE`
lines: no seed, no recipe, `os.listdir("/app/polyglot")` raises for every case. Every predicted pass flips. (The
block above shows 8 of the 18 `CASE` rows — every one of the seven predicted passes among them; the ten rows not
shown are `observed=fail … error=DirMissing` as well; requirement text elided after `--`.)

**After** — v2, same stub, same clone:

```
CASE nop predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=single-file error=DirMissing -- …
CASE oracle-solve-sh predicted=pass observed=pass tests=P predicted_tests=P match=NO regrade=same violates= -- …
CASE lookup-table predicted=pass observed=pass tests=P predicted_tests=P match=NO regrade=same violates=fib-kth -- …
CASE extra-file predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=single-file error=NamesUnexpected -- …
CASE leftover-cmain predicted=fail observed=fail tests=F predicted_tests=F match=yes regrade=same violates=single-file error=NamesUnexpected -- …
CASE empty-file predicted=fail observed=pass tests=P predicted_tests=F match=NO regrade=same violates=fib-kth -- …
CASE dir-in-place predicted=fail observed=pass tests=P predicted_tests=F match=NO regrade=same violates=c-build -- …
cases=18 observed_pass=15 observed_fail=3 mismatches=15
STAGE lines printed: 16
RAW-BEGIN oracle-solve-sh
STAGE seed rc=0
STAGE recipe rc=0
STAGE dir=main.py.c
STAGE file=bytes=872
TEST leg1 P
TEST leg2 P
RAW-END oracle-solve-sh
RAW-BEGIN nop
STAGE seed rc=0
STAGE recipe rc=0
STAGE dir=absent
STAGE file=absent
TEST leg1 F error=DirMissing
RAW-END nop
RAW-BEGIN extra-file
STAGE seed rc=0
STAGE recipe rc=0
STAGE dir=NOTES.md,main.py.c
STAGE file=bytes=872
TEST leg1 F error=NamesUnexpected
RAW-END extra-file
```

Reading: seed and recipe run on the grade path (16 `STAGE` lines over the four echoed cases; the two-act case
switches from `error=DirMissing` to `P`, and the two deliberate extra-entry cases switch from `DirMissing` to the
listing-specific `NamesUnexpected` — i.e. their recipes are distinguishable end states now). `nop` still reports
`dir=absent`, so an absent `/app/polyglot` is still an honest verdict, not a silently empty sandbox. (7 of the 18
`CASE` rows shown; the other eleven are `observed=pass tests=P`, the stub's "exactly `["main.py.c"]`" outcome.)
The stub's `observed_pass=15/observed_fail=3` split is exactly the stub's end-state predicate (15 cases end with
`["main.py.c"]`; `nop`, `extra-file`, `leftover-cmain` do not) — it is **not** a grader receipt and is not offered as
one.

---

## 5. Freeze-integrity regression: the case table did not move

```
$ python3 probe_v2.py --lane "$S/lane" --dry > dry-v2.txt ; exit=0
$ sha256sum dry-v2.txt corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt
99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536  dry-v2.txt
99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536  …/polyglot-c-py-dry-cases-freeze.txt
cmp: DRY BYTE-IDENTICAL to frozen table
```

18 cases, 7 tags, predictions identical to the frozen freeze table. The two repairs change no case, no tag, no
prediction and no requirement text; the V7 case-table amendment the claims reserve for stage 2 is **not** this
seat's item and was not attempted.

---

## 6. Exact commands run

`S=/fast/scratch/hyaku/kengaku-r49/R49C2ExecProbe`, `TMPDIR=$S`, `cwd=$S` for every run (the scratch tree is
removed at yield; every output quoted above is transcribed verbatim into this report).

```
# freeze verification (lane, read-only)
git cat-file -t 9d2900af… ; git log --format='%H %ci %s' -1 9d2900af… ; git merge-base --is-ancestor 9d2900af… HEAD
git ls-tree 9d2900af… plans/round-49-claims.md ; git show 9d2900af…:plans/round-49-claims.md | sha256sum
git ls-tree 9d2900af… .ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py

# host thread census (RLIMIT_NPROC is uid-wide)
for f in /proc/[0-9]*/status; do … Uid/Threads … done            # uid=1000 uid_threads=3076…3105

# clone at the frozen base
git clone --shared --no-checkout <lane> "$S/lane" ; git -C "$S/lane" rev-parse --show-toplevel
git -C "$S/lane" checkout -q 9d2900af… ; git -C "$S/lane" rev-parse HEAD ; git -C "$S/lane" status --porcelain

# candidate
cp <r46 wave artifact> orig/polyglot_c_py_probe_22b7779e.py ; cp orig/… candidate/plans/polyglot_c_py_probe.py
<edits> ; python3 -m py_compile candidate/plans/polyglot_c_py_probe.py ; diff -u orig/… candidate/plans/…

# control (a) / (b) / retry / dry
python3 orig/polyglot_c_py_probe_22b7779e.py --lane "$S/lane" --stage-check --work "$S/work/sc-orig"
python3 candidate/plans/polyglot_c_py_probe.py --lane "$S/lane" --stage-check --work "$S/work/sc-final"
python3 driver/retry_probe.py candidate/plans/polyglot_c_py_probe.py "$S/lane" "$S/work/retry"
python3 candidate/plans/polyglot_c_py_probe.py --lane "$S/lane" --dry

# control (c): stub grader in a scratch copy of the capture dir (real capture never imported)
python3 driver/mode_all_stub.py orig/polyglot_c_py_probe_22b7779e.py "$S/lane" "$S/work/stub-asmode"
python3 driver/mode_all_stub.py orig/… "$S/lane" "$S/work/stub-orig-final" --neutralize-nproc candidate/plans/…
python3 driver/mode_all_stub.py candidate/plans/polyglot_c_py_probe.py "$S/lane" "$S/work/stub-v2-final"

# nproc sweep (the probe's argv shape, one limit varied)
python3 <inline>: prlimit --nproc={48,ceiling,2*ceiling} -- bwrap --unshare-all … -- /usr/bin/python3 -c 'print(…)'

# transcription
cp candidate/plans/polyglot_c_py_probe.py .ufo/waves/round-49/w1/R49C2ExecProbe/probe_v2.py ; cmp ; sha256sum
```

No `pacman`/`uv`/`npx` install, no network fetch, no git mutation outside the scratch clone (checkout only, and
`git -C "$S/lane" rev-parse --show-toplevel` asserted before it). **Tooling record: nothing installed or upgraded;
no pacman transaction attempted** (host-wide pause respected).

---

## 7. Sources

**No external URL was opened by this seat** (no network use). The pinned capture the stub stands in for was re-read
from the lane tree to ground the substitution, not to re-litigate S166:

| source | location | accessed | located quote (≤25 words) |
|---|---|---|---|
| S166, `tests/test_outputs.py` at TB2 `2fd12b88…` (committed capture of the pinned raw source `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py`) | `corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py:27`, sha256 `b94a7a98…ddec` | 2026-10-28 | `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]"` (line 27, 8 words) |

Lane sources read (all read-only, at `9d2900af…` unless noted): `plans/round-49-claims.md`,
`corpus/lessons/round-48-verifier-spotcheck.md`, `corpus/lessons/round-48.md`,
`.ufo/waves/round-48/w1/R48C2ExecProbe.md`, `.ufo/waves/round-46/w1/R46ExecC3Probe.md`,
`.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py`, `plans/round46_c3_verify.py` (line 31/306–330
receipt parsing only, to confirm that added `STAGE` lines cannot be mistaken for `CASE …`/summary lines).

---

## 8. Limits (what this seat did not do, and what the numbers cannot carry)

1. **No full probe run.** Not one case was graded by the captured grader: the item forbids it and Q30 forbids it
   before the stage-3 commit. So this seat does **not** claim the v2 receipt equals the committed round-46 receipt
   (`dd0e3546…`) or any prediction row. The claims must still re-pin the receipt (and the SPEC/probe digests) at
   stage 2, and only the stage-3 run can show V3–V5 pass.
2. **The stub control proves execution, not verdicts.** Under the stub, `observed_pass=15/observed_fail=3` and
   `mismatches=15` are end-state signals. They must never be quoted as a grader result.
3. **The `22b7779e` mode-all before-receipt needed the nproc defect neutralized** to expose the recipe defect in
   isolation; the as-committed run aborts at `SETUP case nop sandbox failed (rc=1)` and yields zero `CASE` lines.
   Both facts are recorded (§2, §4); the neutralization touched only the `LIMITS` module constant.
4. **`--stage-check` is parse-only** by design (`compile()` + `gcc -fsyntax-only`), so no run-time prediction is
   confirmed here.
5. **`STAGE` lines are new receipt content** on the grade path. They are ignored by the counter's receipt filters
   (which key on `CASE `/summary prefixes), but a byte-compare against the round-46 receipt will differ for reasons
   unrelated to verdicts; the stage-2 amendment must re-pin rather than compare to the old digest.
6. **Host-dependent numbers.** `nproc_ceiling` varies per run by design (measured 3335→3427 within this seat's
   session); no receipt prints it, so the probe output stays deterministic, but a reader cannot recover the ceiling
   from a receipt alone. If the L1 wants that auditable, it is a one-line receipt change — deliberately not made
   here, because it would change the receipt format the counter pins.
7. Nothing was committed, staged, pushed or asserted beyond this seat; no claim admission is claimed.

---

## 9. Scratch state

Scratch `S=/fast/scratch/hyaku/kengaku-r49/R49C2ExecProbe` was created for this seat only (clone, `orig/`,
`candidate/`, `driver/`, `receipts/`, `work/`) and **removed before yield**, so no scratch tree remains on disk —
no self-reported scratch defect. Everything this report cites is transcribed above; the citable artifacts are this
report and `probe_v2.py` in the same directory.

---

VERDICT: probe-repaired-v2 — mode-all grade path now runs seed+recipe (stub control: 0 → 16 STAGE lines; before
`observed_pass=0/observed_fail=18/mismatches=7` with `error=DirMissing` on every case, after the two-act case flips
`DirMissing`→`P` and the extra-entry cases show `NamesUnexpected`), `--nproc` measured per run (48 fails
`bwrap: Creating new namespace failed`, ceiling 3361 passes; retry branch measured 18/18 first-fail → 18/18
retry-pass), `--stage-check` 18/18 pass and byte-identical to the round-46 record on this host; `--dry` still
byte-identical to the frozen freeze table (`99adfea6…`); no full probe run, no scored run, no claim admission.
