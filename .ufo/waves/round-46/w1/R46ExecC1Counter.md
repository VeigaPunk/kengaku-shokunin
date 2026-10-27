# R46ExecC1Counter — `plans/round46_c1_verify.py` drafted, 18/18 controls fail

Seat: executor, kengaku round 46 wave 1 (build), lane `kengaku-shokunin`. Lane measured: `fd4129eb74191cd7cc1cf5a0e6353fd8ce1a6c9f`
(the stage-1 claims commit) on a `git clone -q --shared` at `/fast/scratch/hyaku/kengaku-r46/R46ExecC1Counter/lane`;
`git -C <clone> rev-parse --show-toplevel` = that path, `git status --porcelain` = `?? plans/round46_c1_verify.py` only.
No tool installed or upgraded (strace 7.2, bubblewrap 0.13.1, python 3.14.8, git 2.56 were already present); no pacman
transaction, no host service touched.

## 1. Deliverable

`plans/round46_c1_verify.py` — written in the clone, copied byte-identical to this seat's report subdir:

| file | sha256 | lines |
|---|---|---|
| `.ufo/waves/round-46/w1/R46ExecC1Counter/round46_c1_verify.py` | `fd14188778bc683e319bb5695332570d66e50329abcf8b71015a000d7721abf4` | 603 |

`sha256sum` on both paths printed that one digest for each (`sha256sum "$W/round46_c1_verify.py" "$S/lane/plans/round46_c1_verify.py"`).
It is **not** integrated into the lane: the L1 lands it (this seat writes no lane file). Nothing else in the lane or the
report subdir was created beyond `receipts/`, `probes/` and `kept/`.

Constants (exactly as assigned): `REFUSAL_REL = "plans/refusals46"`, `SEALED_REL = "plans/sealed46"`
(`round46_c1_verify.py:120-121`), with `--refusals DIR`, `--sealed DIR` and `--fence PATH`, `--seed HEX` as
testing-only overrides. The docstring is the full rule and ends with the six frozen predicate lines verbatim from
`plans/round-46-claims.md` §C1, with `<P>`, `<R>`, `<S>` left as the stage-2 literals.

## 2. How each frozen requirement is implemented

| claims §C1 | code | what it does |
|---|---|---|
| (a) round-44 legs/builder imported, digest-pinned; HONEST 104 unchanged | `PINS` (33 entries: `round44_c1_verify.py`, `refusals45/f1-f10`, 22 battery modules), `build_module:370`, `HARNESS:183` printed by `k44.builder_source()` into `--ro-bind-data` | the round-44 counter's own `Ctx`/`build_module_child` build every fixture; the honest glob is `battery42|43|44` (22 modules, 104 fixtures) |
| (b) Q39 name hiding | `token:220`, `build_module:370-414` | build dir, module copy, fixture parent and log dir are `secrets`-backed 16-hex tokens; fixture dirs stay `fNNN` under an opaque parent (no name carries identity); each parent is padded to `PAD = 24` children with empty decoy dirs, so child count and `st_nlink` carry no module signal; build and run lists are `rng.shuffle`d |
| (c) REFUSALS + byte-copy check | `copy_rows:416` | every `plans/refusals45/*.py` present in the refusals dir is compared byte-for-byte (`COPY <name> ok|DIFFERS|ABSENT`); a difference/absence is counted in the leg's `build_errors`, so the frozen `build_errors=0` cannot hide a mutated copy |
| (d) SEALED from a dir this seat never writes | `groups["sealed"]` | same builder, same verdicts, own `SEALED` line |
| (e) B1 log integrity | `run_fence:329-368`, `HARNESS:188` | `strace` is started on the host **outside** the sandbox and writes `<root>/strace/<token>/log`, a mount the sandbox has read-only (no writable bind exists at all); the harness `os.closerange(3, 1024)` before `breach`, so the log fd (inherited through strace→bwrap→python) is closed; a missing/empty/NUL-holed/execve-less log is returned as `LOG-TAMPER` with one touch, never as zero |
| (f) B3 whole scratch root | `_outside:260` | a touch is any normalized path under `<root>` that is not `d`, not under `d`, and not under `<root>/ctl` (the only exclusion: harness + fence copy). Module copies, sibling fixtures, `d.parent`, logs are all in scope |
| (g) B5 stat channel | `TRACE_SET:164`, `analyse:268-305` | traced: open/openat/openat2/creat, stat/lstat/newfstatat/statx/statfs, access/faccessat/faccessat2, readlink(at), getxattr/lgetxattr/listxattr, inotify_add_watch, name_to_handle_at, open_by_handle_at, execve(at), unlink(at)/rename(at2)/truncate/mkdir(at)/rmdir/symlink(at)/link(at). Success rule: open-family counts on success **or** on any errno except ENOENT; access counts on success or EACCES; stat-family counts on success for **non-directory** paths |
| (h) B6 blocked/never-returned | `analyse:281-317` | `<unfinished ...>` is stored and stitched with its `<... resumed>` tail; a call that never returns (or prints `= ?`) is counted from the stored text; dirfd-relative paths resolve against strace `-y`'s `fd<dir>` annotation, else cwd `d` |
| (i) B4 verdict channel | `HARNESS:189-195` | the harness exits 10 (BREACH) / 11 (ADMIT) / 12 (exception); anything else is ERROR. stdout is never read |

Non-vacuity: `REFUSAL_FLOOR = 10`, `SEALED_FLOOR = 1`, `HONEST_TOTAL = 104` (`:158-160`), so empty hostile dirs cannot
print a passing predicate.

## 3. Method (every run inside the mandated envelope)

```
S=/fast/scratch/hyaku/kengaku-r46/R46ExecC1Counter
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"     # toplevel verified, HEAD fd4129eb
<envelope.sh> "$S/env" /usr/bin/python3 "$S/lane/plans/round46_c1_verify.py" --lane "$S/lane" --work "$S/w" \
    --jobs 8 <override args>
```
Each receipt in `receipts/` starts with the `ENVELOPE …` command line and ends with the envelope's digest line; none
printed `CHANGED`. Two representative pairs:

```
ENVELOPE start 02:13:28 cwd=/fast/scratch/hyaku/kengaku-r46/R46ExecC1Counter
ENVELOPE end 02:13:39 exit=1 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
   (control-base-fence.out; the script also prints `--refusals …/plans/refusals45 --sealed …/emptysealed`)
ENVELOPE start 02:10:49 cwd=/fast/scratch/hyaku/kengaku-r46/R46ExecC1Counter
ENVELOPE end 02:11:07 exit=1 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
   (control-base-holds.out; `--refusals …/holds`)
```

`PINS total=33 mismatched=0` in every control (the pin set is the base's inputs; `refusals46`/`sealed46` do not exist
at wave 1, so the frozen `total=<P>` is the stage-2 amendment's job). The held-out refusal set used for the
`base-holds*` controls is 10 modules copied verbatim into `$S/holds` — `h1_cr_include.py`, `h2_includeif_cond.py`,
`h3_bom_symlink.py`, `link_hostiles.py`, `argv_env.py`, `configkeys.py`, `g1_cdrel.py`, `g2_gitfile.py`,
`g3_wtmeta.py`, `g4_cdrel_hidden.py` (digests e.g. `argv_env.py 1656db9c…f8a4dcf`, `configkeys.py 72c98fae…4b5dab`,
matching `a3w1/R45HoArgvEnv.md`/`R45HoConfigKeys.md`). They stand in for the not-yet-converted `plans/refusals46/`;
the L1's conversion is the frozen input.

## 4. Controls — 18/18 print `PREDICATE C1 fail`

All controls were run with `--refusals lane/plans/refusals45` and `--sealed <empty>` unless the row says otherwise.
`SEALED total=0` in every one of them, so `sealed-total=0<1` is part of the fail reason in all 17 rows that do not
exercise the sealed leg: at wave 1 there is no `plans/sealed46/` (the four `R46CritC1Seal*` seats are still writing).
The behavioural fail reason is quoted in the last column.

| control (`receipts/control-*.out`) | REFUSALS | HONEST | CALIBRATION | behavioural fail reason |
|---|---|---|---|---|
| `no-fence` (absent `--fence`) | `total=10 clean=0 leaked=10 read=0 hung=0 build_errors=0` | `104 admitted=0 refused=104 read=0 hung=0 build_errors=0` | `advertised=10 contradicted=10` | refusals-not-clean, honest-not-admitted |
| `base-fence` (`fixture_fence.py` @ `64ba8385`, sha256 `ac65c032…ce5eda6`) | `total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0` | `104 admitted=104 refused=0 read=0 hung=0 build_errors=0` | `advertised=10 contradicted=0` | **sealed-total=0<1 only** (see §5) |
| `base-holds` (same fence, `--refusals $S/holds`) | `total=10 clean=2 leaked=8 read=0 hung=0 build_errors=0` | `104 admitted=104 refused=0 read=0 hung=0 build_errors=0` | `advertised=10 contradicted=8` | refusals-not-clean, contradicted=8 |
| `base-holds-sealed` (same fence, `--sealed $S/holds`) | `total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0` | `104 admitted=104 refused=0 read=0 hung=0 build_errors=0` | `advertised=20 contradicted=8` | sealed-not-clean (`SEALED total=10 clean=2 leaked=8 read=0 hung=0 build_errors=0`) |
| `keyed_name` (`round-45/claims/fences/keyed_name.py`) | `total=10 clean=0 leaked=10 …` | `104 admitted=104 …` | `advertised=10 contradicted=10` | refusals-not-clean — the Q39 name key finds nothing |
| `admit_all` | `total=10 clean=0 leaked=10 …` | `104 admitted=104 …` | `advertised=10 contradicted=10` | refusals-not-clean |
| `refuse_all` | `total=10 clean=10 …` | `104 admitted=0 refused=104 …` | `advertised=10 contradicted=0` | honest-not-admitted |
| `static_only` | `total=10 clean=9 leaked=1 …` | `104 admitted=0 refused=104 …` | `advertised=10 contradicted=1` | refusals-not-clean (f4 fifo-include), honest-not-admitted |
| `r44_tail` (round-45 adapter, names undefined standalone) | `total=10 clean=0 leaked=10 …` | `104 admitted=0 refused=104 …` | `advertised=10 contradicted=10` | harness ERROR on every fixture |
| `forged-hostread` | `total=10 clean=10 …` | `104 admitted=0 refused=104 …` | `advertised=10 contradicted=0` | honest-not-admitted |
| `forged-stat` | `total=10 clean=0 leaked=10 …` | `104 admitted=0 refused=104 …` | `advertised=10 contradicted=10` | refusals-not-clean (hard-coded paths raise) |
| `forged-spoof` | `total=10 clean=0 leaked=10 …` | `104 admitted=104 …` | `advertised=10 contradicted=10` | refusals-not-clean — its `print("BREACH …")` changes nothing |
| `forged-killshot` | `total=10 clean=0 leaked=10 …` | `104 admitted=104 …` | `advertised=10 contradicted=10` | refusals-not-clean — `/refusals45-` key is gone |
| `forged-nokill` | `total=10 clean=0 leaked=10 …` | `104 admitted=104 …` | `advertised=10 contradicted=10` | refusals-not-clean |
| `forged-logkill2` | `total=10 clean=0 leaked=10 …` | `104 admitted=0 refused=104 …` | `advertised=10 contradicted=10` | refusals-not-clean |
| `forged-modsread` | `total=10 clean=0 leaked=10 …` | `104 admitted=0 refused=104 …` | `advertised=10 contradicted=10` | refusals-not-clean (module-copy path is randomised) |
| `probe-nlink-key` (new structure-keyed control, `probes/p_nlink_key.py`) | `total=10 clean=0 leaked=10 …` | `104 admitted=104 …` | `advertised=10 contradicted=10` | refusals-not-clean — `st_nlink` of every parent is 26 |
| `probe-dirkey-ok` (`probes/p_listdir_parent.py`) | `total=10 clean=0 leaked=0 read=10 …` | `104 admitted=0 refused=104 read=104 …` | `advertised=10 contradicted=10` | every run counted as READ |

`PREDICATE C1 fail`, exit 1, in all 18 receipts; `base-fence` is `receipts/control-base-fence.out`, sha256
`eb9757ae5f1ea5f5e79a526f2b73bc6cc6fd2386f52ffa88957f8c1cac2c48b5`.

Stage-2 rehearsal (`receipts/control-defaultmode-unpinned.out`): with `plans/refusals46/` = the ten byte copies and
`plans/sealed46/` = one module placed in the clone and **no** overrides, the counter prints
`PINS total=33 mismatched=11 first=plans/refusals46/f10_laneinclude.py:unpinned`, ten `COPY … ok` rows,
`REFUSALS total=10 clean=10 …`, `SEALED total=1 clean=1 …`, `HONEST fixtures=104 admitted=104 …`,
`CALIBRATION advertised=11 contradicted=0`, `REASON pins=11`, `PREDICATE C1 fail`. So a landing that forgets to pin a
hostile input cannot pass; the clone dirs were removed afterwards (`git status --porcelain` back to the one added file).

## 5. The base fence's before value, stated precisely

`plans/fixture_fence.py` at the base is **not** contradicted by the ten `plans/refusals45` modules — it was landed to
refuse exactly those (`REFUSALS clean=10`, `HONEST 104/104`, `contradicted=0`). The contradiction the claim counts
lives in the held-out and sealed modules: the same fence admits 8 of the 10 converted held-outs (`base-holds`,
`contradicted=8`) and 8 of 10 on the sealed leg (`base-holds-sealed`, `SEALED total=10 clean=2 leaked=8`), with
outside-`d` touches inside the admitted modules (`h2_includeif_cond.py … touches=72`, `h3_bom_symlink.py … touches=30`,
`g4_cdrel_hidden.py … touches=51`, `h1_cr_include.py … touches=28`, `link_hostiles.py … touches=2`). Two of my ten
(`g1_cdrel.py`, `g2_gitfile.py`) are refused clean and would therefore be **dropped** from `plans/refusals46/` under
claims §C1(c) — they are control material here, not a proposed conversion.

Therefore the base-fence control at wave 1 fails only on the sealed floor, and the L1's stage-2 receipt must re-run it
with `plans/refusals46/` and `plans/sealed46/` in the tree (the numbers above are the wave-1 proxies for that run).

## 6. Leg receipts (unit level, `probes/leg-driver.py`, envelope-wrapped)

Each line below is the first `f7_commondir.py` fixture of `receipts/leg-*.out`, which also carries its `ENVELOPE`
pair (`exit=0`, digest unchanged):

- B1, log tamper-proof: `leg-p_log_attack.out` — `f7-cd-accept BREACH touches=0 calls=427 why=BREACH log-attack no:ValueError,no:ValueError`.
  The fence cannot even name the log: `/proc/1/cmdline` is the sandbox init, and `strace` is outside the pid namespace,
  so no `-o` path exists to find; the harness has already closed fd ≥ 3, and `open(<log>, "wb")` returns EROFS (proved
  in the earlier scratch probe, `openat(…) = -1 EROFS (Read-only file system)`).
- B3, module-source / sibling reads: `probes/p_open_outside.py` → `touches=2`, first hit
  `newfstatat(… /fx/<token>/outside.cfg)`; `p_listdir_parent.py` → `openat(… /fx/<token>)` counted (control row
  `probe-dirkey-ok`: `read=10` refusals / `read=104` honest).
- B5: `probes/p_stat_file.py` → `touches=2`, both hits `newfstatat(… /outside.cfg)` — a stat-only read is counted.
- B6: `probes/p_blocked_open.py` (driver plants a FIFO in `d.parent`) → `touches=2`: the `newfstatat` and the
  never-returned `openat(… "/blocked.fifo", O_RDONLY|O_CLOEXEC) = ?` from the killed child (`kept/blocked-open-strace.txt:428`).
- B4: `probes/p_spoof_stdout.py` → `ADMIT touches=0` although it printed `BREACH planted-by-print`: verdict is exit 11.
- Padding/nlink: `probes/p_stat_parent.py` → `nlink=26` for every fixture of every module (24 pads + `.`/`..`), and
  `probe-nlink-key` therefore cannot split the two legs.
- Why directory stats are exempt (`round46_c1_verify.py:295-298`): git's bounded discovery stats every ancestor
  directory successfully — `receipts/probe-git-ceiling-walk.log` shows `newfstatat(… , "/fast", …) = 0` through
  `…/gt/root/fx` with `GIT_CEILING_DIRECTORIES` set. Counting those would make a correct fence `READ` on every honest
  fixture; a directory stat carries no name, and the one channel it has (`st_nlink`) is nulled by padding.

## 7. Limits this counter still carries (named, not hidden)

1. **B7 io_uring** — `io_uring_setup` succeeds in the sandbox and SQE `OPENAT`/`READ` emit no traced syscall; the
   counter does not install a seccomp filter. Recorded in the docstring and here.
2. **Host paths outside the scratch root** are not counted: `/etc`, `/proc`, `/sys` reads are invisible (the base
   fence's own `--ro-bind / /` allows them). The `forged-hostread` control still fails, but only on the honest leg. The
   advertised wording is "without reading outside `d`"; this counter measures the scratch root, as claims §C1(f) says.
3. **Directory stat** is exempt by design (see §6) — `st_nlink` is nulled, not measured.
4. **`/proc` channel**: a fence can still read `/proc/self/mountinfo`, `/proc/<pid>/cmdline` (uncounted). The log path
   is not there (§6 B1) but the harness path is; opening anything under the scratch root is counted.
5. The round-44 counter's `SIDECHANNEL` token scan is not repeated over hostile modules, and `--refusals/--sealed/
   --fence/--seed` runs print the predicate of the inputs they name — never a receipt for the frozen run.

## 8. Stage-2 handoff (what the L1 must do)

1. Land `plans/round46_c1_verify.py` unchanged; record its sha256 `fd141887…7721abf4` in
   `.ufo/waves/round-46/claims/frozen-digests.txt`.
2. Fill `PINS` with every `plans/refusals46/*.py` and `plans/sealed46/*.py` digest (the counter fails with
   `<rel>:unpinned` otherwise — rehearsal above), and set `<P>`, `<R>`, `<S>` in the docstring/claims to
   `len(PINS)`, the refusal module count and the sealed module count.
3. Re-run the before-controls **in the lane** (`--lane .`, no overrides) with `refusals46`/`sealed46` present, and
   freeze those receipts; the `base-holds*` rows above are the wave-1 proxies, not the frozen receipts.
4. Do not score a repaired fence with this counter before step 2 is committed (claims §C1 order rule). This seat ran the
   counter only on controls — no repaired fence exists yet and none was run.

## 9. Receipts (this subdir, all ≤ 1 MiB, total 1.0 MB)

`receipts/control-*.out` (the 18 control receipts: `no-fence`, `base-fence`, `base-holds`, `base-holds-sealed`, `keyed_name`,
`admit_all`, `refuse_all`, `static_only`, `r44_tail`, `forged-{hostread,stat,spoof,killshot,nokill,logkill2,modsread}`,
`probe-nlink-key`, `probe-dirkey-ok`), `receipts/control-defaultmode-unpinned.out`, `receipts/RUNLOG.txt` (the 17-run
table as printed), `receipts/leg-*.out` (seven probe-fence runs: blocked-open, listdir-parent, log-attack, open-outside, spoof-stdout, stat-file, stat-parent), `receipts/probe-git-ceiling-walk.log`,
`kept/blocked-open-strace.txt` (the FIFO run's post-mortem strace, line 428 is the never-returned open), `probes/*.py` (the
eight probe fences and `leg-driver.py`). `plans/refusals46/` and `plans/sealed46/` are absent from the lane at this
commit (`ls -d plans/refusals46 plans/sealed46` → `No such file or directory`); `plans/sealed46/` must be assembled by
the L1 from the seal seats' wave-1 modules — this seat did not read them.

Scratch `/fast/scratch/hyaku/kengaku-r46/R46ExecC1Counter` removed with
`python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r46 R46ExecC1Counter "$S"`
after the copies above were verified.

VERDICT: c1-counter-drafted-controls-failing-18/18
