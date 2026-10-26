# F41NoHarm — re-run of the landing measurement at the live tip (round 41, wave 2 falsify)

Seat: `F41NoHarm` (executor, leaf). Axes: **operability** (does the L1's own measurement driver still run unmodified
under the ruled envelope from my scratch?) and **freshness** (does the receipt still describe the lane bytes that are
there now?). Lane `kengaku-shokunin`, measured commit `d7c77895752a2a5f317fa22f2362416ada50a04b` (live
`refs/heads/master`; assigned tip `3d0058f…` = this commit minus two `.ufo` files, §4). Receipt under attack:
`.ufo/waves/round-41/integrate/measure-final.txt`, sha256
`870f18471e1649249b6174156522125aea955352787dfb2acc51c4315c3aa5b5`, taken at `74513c0…`.

Nothing frozen was changed: `sha256sum -c .ufo/waves/round-41/claims/frozen-digests.txt` on the live lane at
16:17:29 → 11/11 `OK`, exit 0.

## 1. Method — two runs inside the binding envelope

```
S=/fast/scratch/hyaku/kengaku-r41/F41NoHarm          # my only scratch root; TMPDIR=$S
cp .ufo/waves/round-41/integrate/measure.sh $S/measure.sh            # one edit: S= line (L1/measure → F41NoHarm/measure)
cp .ufo/waves/round-41/integrate/measure.sh $S/measure-pinned.sh     # S= line + TIP pinned + -B master (see below)
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent bash $S/measure.sh
```

- **A (freshness)** `$S/measure.sh`, `TIP=$(git -C "$L" rev-parse refs/heads/master)` → `d7c7789…`, rc=0, 800 lines,
  356 s. Original script sha256 `512255013fe0…`; my copy `e96d4ba05a0b…` (diff = the `S=` line only).
- **B (reproduction)** `$S/measure-pinned.sh`, same script with `TIP=74513c0625df7…` literal and
  `checkout -q -B master "$TIP"`; copy sha256 `af3eb5f3e5ea…`. rc=0, 800 lines, 343 s.
  The `-B master` deviation is forced and is *not* a weakening: my `--no-local` clone has `master=d7c7789` while the
  measured HEAD is `74513c0`, and a detached clone hands every **child** clone the source's `master` — the failure
  mode recorded by wave 1 (`.ufo/waves/round-41/build/R41ExecNoHarm/measure.sh:38-40`). At landing, `master == TIP`,
  so `-B master` restores the landing run's exact conditions. Evidence that it does: run B is byte-identical to the
  receipt after path normalisation (§2).
- One aborted attempt is disclosed: the first B launch used the literal `checkout -q "$TIP"`; I cancelled it
  (16:15:4x) before it could produce a misleading transcript, and its scratch was reaped by its own trap.
- Comparator `cmp_measure.py` (sha256 `74038b59cb45…`) rewrites only the scratch root vs `<S>` and, in the strict
  mode, the three commit ids; nothing else is touched. Transcripts and diffs are beside this report:
  `out-master.txt`, `out-pinned74513c0.txt`, `diff-pinned-vs-final.txt`, `diff-master-vs-final.txt`,
  `diff-master-vs-final-keep-tip.txt`.

## 2. Result — no verdict drift

| run | transcript vs `measure-final.txt` | verdict lines | identical |
|---|---|---|---|
| B @ `74513c0` (strict, tips **not** normalised) | `DIFF none` | 730/730 | **800/800 lines** |
| A @ `d7c7789` (tips normalised) | `DIFF none` | 730/730 | 800/800 lines |
| A @ `d7c7789` (tips **not** normalised) | 18 diff lines = 3 hunks | 730/730 (multiset equal) | 796/800 lines |

The four non-identical lines in A are commit identity alone — `TIP`, `TIP commit=` + `REF AUDIT rev=/tip=` (both
`state=match`), and `tip` in `tip_receipts`. `$ python3 ... cmp_measure.py <final> out-master.txt --keep-tip` →
`verdict_multiset_equal=False`, and the only hunks are those lines.

Freshness checks that the tip movement could have broken, and did not:

```
$ git -C <lane> diff --name-only 3d0058f… d7c7789… | grep -vc '^\.ufo/'        → 0      (dispatch commit = 2 .ufo files)
$ git -C <lane> diff --name-only 74513c0… HEAD -- plans corpus README.md SKILL.md PROVINCE.md .ufo/waves/round-41/claims
corpus/lessons/round-41.md                                                    (the only counter input that moved)
```

## 3. Every verdict line, both rounds' C1/C2 and the no-harm set

25 instrument checks (24 `r()` commands each printing `exit=`, plus the inline `constraints_probe` check); all 25
equal to the receipt, in order:

| instrument | verdict | exit |
|---|---|---|
| `round41_c1_verify` | `PINS total=2 mismatched=0`; `BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0`; `MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0`; `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`; `ADVERTISED direct=21 indirect=2 none=0`; `PINS-AFTER mismatched=0`; `PREDICATE C1 pass` | 0 |
| `round41_c2_verify` | `V1 ok listed=10 bad=0 extra=0` … `P10 ok probe_rerun=byte-equal bytes=5775`; `checks=8 defects=0`; `PREDICATE C2 pass` | 0 |
| `order_check` r41 | `ORDER RESULT PASS` (freeze `8ef8b4fc…`, receipt commit `f774a87…`) | 0 |
| `round40_c1_verify` | `fixtures=21 wrong=0 tampered=0 sidechannel=0`; `MUTANTS 21/21`; `PREDICATE C1 pass` | 0 |
| `round40_c2_verify` | `checks=7 defects=0`; `PREDICATE C2 pass` | 0 |
| `order_check` r40 / r39 | `ORDER RESULT PASS` / `ORDER RESULT PASS` | 0 / 0 |
| `order_check` r38 | `ORDER FAIL probe-executed-before-receipt hits=1` | **1** (carried in receipt) |
| `round39_c1` | `fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0`; `MUTANTS 7/7 killed`; `PREDICATE C1 pass` | 0 |
| `round39_c2` | `checks=7 defects=0` | 0 |
| `round38_c1` | `fixtures=86`; `MUTANTS total=22 killed=21 survived=1`; `PREDICATE C1 fail` | **1** (carried in receipt) |
| `round38_c2` | `checks=7 defects=0` | 0 |
| `round37_c1` | `fixtures=64`; `MUTANTS 55/55`; `PREDICATE C1 pass` | 0 |
| `round37_c2` / `round36_c2` | `checks=7 defects=0` / `checks=6 defects=0` | 0 / 0 |
| `anchor_digest_check` | `rows=117 tokens=24 defects=0` | 0 |
| `sources-census.sh validate` | 15 `W04` duplicate-url warnings, `ok` | 0 |
| `sha256sum -c` frozen r41 / r40 / r39 | 11 `OK` / 11 `OK` / 9 `OK` | 0 / 0 / 0 |
| `ledger_tip` | `REF AUDIT … state=match`; `rows=9 closed=9 observed_pass=9 mismatches=0` | 0 |
| `tip_receipts` | `receipts=27 byte_equal=7 differ=0 skipped=20`; control `verdict=differ` | 0 |
| `db_wal_probe` | `cases=28 observed_pass=8 observed_fail=20 mismatches=0` | 0 |
| `constraints_probe` (inline) | `exit=0 byte_equal=yes` | 0 |
| `round_close --round 41` | `ROUND-CLOSE RESULT PASS exit=0`; `census warnings=15 verdict=PASS` | 0 |

Tail: `registry_rows=117 knowledge_files=48 index_rows=48` in all three transcripts.

The two `exit=1` results are **pre-existing and recorded in the receipt** (round-38 order gap and round-38's one
surviving mutant N21); they are identical here, so they are not drift and not a round-41 regression. My runs
reproduce them rather than hiding them.

## 4. Host-safety receipts (post-run, 16:20:41 and 16:21:28)

- `~/.local/bin`: full listing `(name,size,mtime)` before (16:15:41 — inside run A's window; the `-newermt 16:05`
  check below also covers run A's 16:12:40 start) and after both runs (16:21:28) —
  `diff pathdir-before.txt pathdir-after-both.txt` → **identical**, listing sha256 `5f0d473b73eb…`, 52 files.
  `find /home/vgpnk/.local/bin -newermt '2026-10-26 16:05:00' -print | wc -l` → **0**. `~/.local/bin/git` → **absent**.
  Inside the envelope the same directory refuses writes: `touch /home/vgpnk/.local/bin/.wtest` →
  `Read-only file system`.
- Neutralized attack modules unchanged and unreferenced:
  `f532423bd90b…` (`crit_git_shim.py`), `7c4f434b750b…` (`crit_ledger_selfread.py`), one `NEUTRALIZED` banner each,
  and `grep -rl 'crit_git_shim\|crit_ledger_selfread' plans | wc -l` → **0**.
- Lane untouched by me: `git -C <lane> status --porcelain -uno | wc -l` → 0; `rev-parse HEAD` → `d7c7789…` unchanged;
  of 397 untracked entries at 16:26, 395 are other seats' `falsify/` files and 2 are the L1's own
  `falsify.ready`/`falsify.ready.dispatched` markers — none is mine.
- Write-scope audit of the one instrument that executes the captured grader, strace'd inside the envelope
  (`audit/c2.out` rc=0 `checks=8 defects=0`; summary in `strace-c2-summary.txt`): opens under the **live** lane root
  = **0**, write-intent opens under it = **0**, `__pycache__` creations = **0**; the 25 grader copies go to
  sandbox-local relative names (`test_outputs.py`, `solve.sh`, `recipe.sh`, `harness.py`).
- Scratch `S` contains no clones or worktrees after the runs (both drivers' traps fired); the 573 MB strace audit tree
  is removed before this seat ends.

**One lane observation, not mine.** `corpus/evidence/round41/tb2-constraints-scheduling/__pycache__/test_outputs.cpython-314.pyc`
exists with mtime `16:15:05`, inside run A's window. It is gitignored (`.gitignore:2` `__pycache__/`), so it cannot
move `untracked_in_clone=0`, P9 or any committed-bytes verdict — both of my runs and the receipt report
`untracked_in_clone=0`. My instrument set is cleared by the strace above (0 live-lane opens); the
`__pycache__` must come from another seat importing the grader in place. For the L1: harmless to every gate, but it
is an untracked live-lane write by some wave-2 seat and worth one line in the integration notes.

## 5. Limits

- I did not re-attack the C1 admission vectors (probe stub steering, dead-site crediting, relative-argv escape,
  AF_UNIX/SysV isolation, source-text-only sidechannel scan) or the C2 prose surfaces — those are the battery,
  counter and prose seats' items; my `fixtures=48 wrong=0 tampered=0 sidechannel=0`, `killed=23/23` lines only
  reproduce that the *counter* says so.
- `-B master` in run B is the one script deviation; justified in §1 and validated by the byte-identical result.
- Both runs used host `python3`/`git`/`bwrap`; sandboxes are the instruments' own (nested inside the envelope).
- No tool was installed, upgraded or removed; no `pacman`, no subagent, no background job of mine beyond the two
  driver runs, no commit, no `git add`, no mutating `jj`.

VERDICT: no-harm-verdicts-equal-25/25
