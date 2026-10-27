# R45RevC1Receipt — C1 receipt re-derivation on a clean clone (kengaku r45, wave 2, falsify)

Seat: R45RevC1Receipt · 2026-10-26 · Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin (tip `4290d6432efa678327d3b69e43205d0d2954f652`)
Assignment: re-derive the C1 receipt end-to-end on a clean `--shared` clone, then hand-verify ONE refused module and ONE honest module under my own strace (not the counter's).
No tool installs were needed; nothing was installed.

## 1. Clean clone and frozen-integrity preconditions

```
$ S=/fast/scratch/hyaku/kengaku-r45/R45RevC1Receipt; export TMPDIR="$S"
$ git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
$ git -C "$S/lane" rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r45/R45RevC1Receipt/lane
$ git -C "$S/lane" rev-parse HEAD
4290d6432efa678327d3b69e43205d0d2954f652
```

Frozen counter integrity (the counter I was told to run, vs the freeze commit `52d7486a8caf930855cd1f748032ac21648303f5`):

```
$ sha256sum <lane>/plans/round45_c1_verify.py "$S/lane/plans/round45_c1_verify.py"
7745eb0a4bdf281acf46cde6e6a4c280a17d02f9668ea309d1020fff9ce1150d  (both copies)
$ git -C "$S/lane" show 52d7486a8caf930855cd1f748032ac21648303f5:plans/round45_c1_verify.py | sha256sum
7745eb0a4bdf281acf46cde6e6a4c280a17d02f9668ea309d1020fff9ce1150d
```

The C1 counter is byte-identical across lane, clone and freeze commit. The fence itself is the work, not pinned: `git show 52d7486:plans/fixture_fence.py` → `fatal: path 'plans/fixture_fence.py' exists on disk, but not in '52d7486a8caf930855cd1f748032ac21648303f5'`; at the tip its digest is `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6` (printed by the counter as `FENCE plans/fixture_fence.py sha256=ac65c032…` and re-verified by my hand-check driver).

## 2. Counter run, end to end, inside the envelope (run 1 — full output)

```
$ cd "$S/lane" && /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh \
    "$S/env" /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round45_c1_verify.py \
    --lane "$S/lane" --work "$S/work" --jobs 8
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45RevC1Receipt/env /fast/scratch/hyaku/kengaku-r45/R45RevC1Receipt/env --bind /fast/scratch/hyaku/kengaku-r45/R45RevC1Receipt/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round45_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r45/R45RevC1Receipt/lane --work /fast/scratch/hyaku/kengaku-r45/R45RevC1Receipt/work --jobs 8
ENVELOPE start 23:49:17 cwd=/fast/scratch/hyaku/kengaku-r45/R45RevC1Receipt/lane
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
FENCE-RUN refusal refusals45/f10_laneinclude.py f10-lane-include-regular BREACH opens=0 -- lane/.git/config carries an include
FENCE-RUN refusal refusals45/f1_gitfile.py f1-gitdir-outside BREACH opens=0 -- .git/.git is a file (gitdir redirect), not a directory
FENCE-RUN refusal refusals45/f2_deep.py f2-deep-worktree BREACH opens=0 -- x/y/z/r/.git/config sets core.worktree=/fast/scratch/.../fx/refusals4
FENCE-RUN refusal refusals45/f3_abbrev.py f3-abbrev-tree-claims BREACH opens=0 -- order argv is not the contract shape ['--lane', '--claims', '--receipt']
FENCE-RUN refusal refusals45/f4_fifo.py f4-fifo-include BREACH opens=0 -- lane/.git/config carries an include
FENCE-RUN refusal refusals45/f5_alternates.py f5-alternates-outside BREACH opens=0 -- lane/.git/objects/info/alternates present
FENCE-RUN refusal refusals45/f6_above.py f6-repo-above-d BREACH opens=0 -- .git exists at /fast/scratch/.../fx/refusals45-f6_above above the fix
FENCE-RUN refusal refusals45/f7_commondir.py f7-cd-accept BREACH opens=0 -- lane/.git/commondir present (store redirect)
FENCE-RUN refusal refusals45/f7_commondir.py f7-cd-reject BREACH opens=0 -- lane/.git/commondir present (store redirect)
FENCE-RUN refusal refusals45/f7_commondir.py f7-cd-anchor BREACH opens=0 -- lane/.git/commondir present (store redirect)
FENCE-RUN refusal refusals45/f8_worktreecfg.py f8-wtcfg-a BREACH opens=0 -- lane/.git/config enables extensions.worktreeConfig
FENCE-RUN refusal refusals45/f8_worktreecfg.py f8-wtcfg-b BREACH opens=0 -- lane/.git/config enables extensions.worktreeConfig
FENCE-RUN refusal refusals45/f9_nodescribe.py f9-bare-repo BREACH opens=0 -- lane/.git/config sets core.bare
FENCE-RUN honest battery42/a_class.py a_class-x6-sibling-digest ADMIT opens=0
… (104 honest FENCE-RUN lines total, every one `ADMIT opens=0`; full list in the run-2 receipt file)
REFUSAL f10_laneinclude.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f1_gitfile.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f2_deep.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f3_abbrev.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f4_fifo.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f5_alternates.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f6_above.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSAL f7_commondir.py clean fixtures=3 admitted=0 hung=0 opens=0
REFUSAL f8_worktreecfg.py clean fixtures=2 admitted=0 hung=0 opens=0
REFUSAL f9_nodescribe.py clean fixtures=1 admitted=0 hung=0 opens=0
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 23:49:25 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

(The two `FENCE-RUN`/`REFUSAL` reason lines truncated above at 120 chars are truncated by the fence itself, not by me.)

## 3. Second independent run, saved as a receipt

```
$ cd "$S/lane" && <envelope.sh> "$S/env3" /usr/bin/python3 <lane>/plans/round45_c1_verify.py \
    --lane "$S/lane" --work "$S/work2" --jobs 8 > .ufo/waves/round-45/w2/R45RevC1Receipt/c1_receipt_run2.txt 2>&1
$ sha256sum c1_receipt_run2.txt
88ec073fbecb9fe1e0e87fd062cfdbcd17e01479a2fdf8194881cd10a8d7ae5f
$ grep -c "^FENCE-RUN honest" c1_receipt_run2.txt   → 104
$ grep -c "^FENCE-RUN refusal" c1_receipt_run2.txt  → 13
PINS total=33 mismatched=0
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
ENVELOPE end 23:51:40 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

Identical numbers on both runs (13 = 10 modules' fixtures: f7×3, f8×2, rest ×1). Receipt kept at `.ufo/waves/round-45/w2/R45RevC1Receipt/c1_receipt_run2.txt` (7.5 KB, well under 1 MiB).

## 4. Hand check under MY OWN strace (not the counter's)

Driver: `.ufo/waves/round-45/w2/R45RevC1Receipt/handcheck_c1.py`. It builds one refused module (`plans/refusals45/f5_alternates.py`) and one honest module (`plans/battery44/u9_worktree_b.py`) with the round-44 builder (`k44.builder_source()`/`ro_sandbox`, loaded from the clean clone, unchanged), then runs the fence itself under its own `strace -f -qq -y -e trace=open,openat,openat2,creat` inside the counter's read-only sandbox shape (lane hidden, only the strace logdir writable), and parses each log with its own parser. The parser counts a successful open as "outside" iff its resolved path (`-y` annotation, taken from the return-fd annotation, the path-argument annotation, or the raw argument) lies under the build scratch (`<root>/fx`, `<root>/btmp`) but not under the fixture dir; never-returned opens and failed opens touching such paths are reported separately.

```
$ mkdir -p "$S/hand" && cd "$S/lane" && <envelope.sh> "$S/env2" /usr/bin/python3 \
    .ufo/waves/round-45/w2/R45RevC1Receipt/handcheck_c1.py "$S/hand"
ENVELOPE start 23:51:08 cwd=/fast/scratch/hyaku/kengaku-r45/R45RevC1Receipt/lane
HAND fence_copy sha256=ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6
HAND module refused refusals45/f5_alternates.py fixtures=1
HAND fixture f5-alternates-outside tool=order dir=$S/hand/fx/refusals45-f5_alternates/f000
HAND verdict='BREACH lane/.git/objects/info/alternates present' rc=0
HAND succ_outside_d=0 failed_touch=0
HAND SUMMARY refused: fixtures=1 admit=0 breach=1 succ_outside=0
HAND module honest battery44/u9_worktree_b.py fixtures=3
HAND fixture u9_worktree_b-registry-erratum-appended tool=anchor dir=$S/hand/fx/battery44-u9_worktree_b/f000
HAND verdict='ADMIT' rc=0
HAND succ_outside_d=0 failed_touch=0
HAND fixture u9_worktree_b-erratum-retargeted-history tool=anchor dir=$S/hand/fx/battery44-u9_worktree_b/f001
HAND verdict='ADMIT' rc=0
HAND succ_outside_d=0 failed_touch=0
HAND fixture u9_worktree_b-erratum-completed-in-place tool=anchor dir=$S/hand/fx/battery44-u9_worktree_b/f002
HAND verdict='ADMIT' rc=0
HAND succ_outside_d=0 failed_touch=0
HAND SUMMARY honest: fixtures=3 admit=3 breach=0 succ_outside=0
HAND RESULT SUPPORTS-C1 refused=(1,0,1,0) honest=(3,3,0,0)
ENVELOPE end 23:51:10 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

The traces are live, not empty (log sizes: `wc -l $S/hand/strace/s*/log` → 114, 189, 189, 189), and the honest runs show the fence's git children really opening store files — inside the fixture dir:

```
5  openat(AT_FDCWD<…/battery44-u9_worktree_b/f000>, ".git/config", O_RDONLY) = 3<…/battery44-u9_worktree_b/f000/.git/config>
```

Corroboration over all four logs — every resolved `-y` path annotation under the hand-check scratch, deduped (`grep -ho '</fast/scratch/…/hand[^>]*>' log | sort -u`): only fixture-internal paths (`f000`, `f000/lane`, `f00X/corpus/…`, `f00X/.git/{config,HEAD}`) plus the two counter inputs (`hand/fence/fixture_fence.py`, `hand/handcheck_harness.py`, opened by the traced `python3 -I` itself). Zero paths under `fx`/`btmp` outside the fixture dir. The f5 refusal never even opened the alternates file: the fence refuses on `os.path.lexists(gd/"objects"/"info"/"alternates")` (fixture_fence.py:178-179), a stat-level check — `grep 'info/alternates' s00001/log` → no match.

### Parser non-vacuousness (positive + negative control)

A zero from a blind parser is worthless, so I controlled it (`pc_parser.py`, run inside the envelope):

```
ENVELOPE start 23:51:46 cwd=/home/vgpnk/Projects/shokunin
PC outside: succ_outside=1 failed_touch=0
PC SUCC-LINE 5  openat(AT_FDCWD<…/pc/d>, "…/pc/outside/f.txt", O_RDONLY|O_CLOEXEC) = 3<…/pc/outside/f.txt>
PC inside: succ_outside=0 failed_touch=0
PC RESULT PARSER-DETECTS outside=(1,0) inside=(0,0)
ENVELOPE end 23:51:48 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

The parser detects an outside open (succ=1) and correctly does not count an inside-d open (succ=0). The counter's own regex reads the same `= fd</resolved>` annotation, which `strace -y` really emits (sample: `openat(AT_FDCWD<…>, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3</etc/ld.so.cache>`), so the counter's `opens=0` columns are measured, not vacuous.

## 5. Findings

1. **[For the L1 — freeze digest drift, not a C1 defect.]** Two of the four artifacts the goal calls FROZEN at `52d7486a…` no longer match it at the tip: `plans/round-45-claims.md` (frozen `1e63c4ba…`, tip `cb2fae38…`, +2 lines) and `plans/round45_c2_verify.py` (frozen `8c302709…`, tip `ab6825e3…`, 50 lines changed). `git log 52d7486..HEAD -- <those files>` → `7d062c0` (C2 package) and `9271dda` ("round-45: freeze amendments (flat captures, bare-stdout receipt, re-pinned spec/counter, V10 quote fixes, claims note) + w1 seat reports"). The drift is self-documented in the claims file itself: "The attempt-2 continuation found four latent defects in the inherited freeze and corrected them before any claim data depended on the tree" (plans/round-45-claims.md:32, "Freeze amendments (pre-data, attempt 2, before landing)"). The C1 counter — the only frozen artifact my predicate depends on — is byte-identical to the freeze commit, and the fence is the declared work, so C1's receipt stands; but the orchestrator's freeze digest is stale for the claims file and the C2 counter, and "nothing frozen may change" is not literally true at the tip. The L1 should either re-pin the freeze at `9271dda` (or the tip) or flag the amendment.
2. **[Residual risk, low.]** The opens rule scopes "outside" to `<root>/fx` ∪ `<root>/btmp`; counter inputs under `<root>` (fence copy, harness) are excluded by construction. A fixture steering an open there is implausible — argv values must resolve inside `d` (fixture_fence.py fact 2), the lane is hidden in the fence sandbox, and my logs show no such path — but the rule as written would not flag it.
3. **[Residual risk, low.]** The never-returned-open branch (FIFO) was exercised by f4 only in the counter's runs (clean, opens=0); my hand-check module f5 has no pending opens, so my own parser's pending branch ran only in the positive control, not against a real hostile fixture. The counter's f4 line and my parser's shared rule cover the case.

## 6. Verification gaps

None blocking. Honest-set hand check limited to one module (3 fixtures) per the assignment; the other 101 honest fixtures are covered by the two counter runs (104/104 `ADMIT opens=0` each). Both envelope runs show `local_bin_content_before=after=e396f23e40a69201 unchanged`; no measurement was invalidated.

Scratch `/fast/scratch/hyaku/kengaku-r45/R45RevC1Receipt` (clone, work dirs, hand-check tree, pc tree, env overlays) removed at the end via `plans/scratch_guard.py safe-rm`; receipts live in this seat dir.

VERDICT: c1-receipt-reproduced-yes-handchecked-2
