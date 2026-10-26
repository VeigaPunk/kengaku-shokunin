# R42ExecNoHarm — no-harm baseline at the round-42 receipt commit (wave 1)

Seat: executor, leaf. Assignment: run the standing instruments named by the seat task on a clean clone of the
round-42 first recorded probe run `523b27806be0df26d2235089d845265a29f8cedf`, every leg inside the ruled
host-safety envelope, and leave a re-runnable `measure.sh`. Nothing in the lane was written; the frozen tools,
both round-42 counters, the probe, spec, gate, dry table, captures, receipt and `claims/` are read-only inputs here.

Re-runnable driver (scratch root is **`$1`**, sha256 `3e1027ee87af8a60ab4a537bf5ee8bb6d3fbd6792106351d9d48d71fd2d4a4c4`):

```
.ufo/waves/round-42/build/R42ExecNoHarm/measure.sh [SCRATCH]     # default scratch .../R42ExecNoHarm/run; ~475 s
COMMIT=<tip> .ufo/waves/round-42/build/R42ExecNoHarm/measure.sh [SCRATCH]   # same set at another commit
```

Environment overrides: `LANE=` (lane path), `COMMIT=` (commit to pin), `LOGDIR=` (per-leg logs), `KEEP=1` (keep
scratch). Scratch guard: the script refuses any `SCRATCH` outside `/fast/scratch/hyaku/kengaku-r42/<seat>` and
deletes only that directory (round-41 closure R2). Full per-leg logs are committed with this report under
`.ufo/waves/round-42/build/R42ExecNoHarm/logs/` (30 files, 99 450 bytes total; largest `run.log`, 14 166 B).

## Result: 24 green of 24 (exit 0 **and** the verdict line in the leg's log)

Run window 17:35:34→17:43:28 on 2026-10-26, `elapsed=474s`, `baseline green=24 of 24 reds= none`.

| # | instrument (cwd = clone root) | exit | verdict line (log) |
|---|---|---|---|
| 1 | `plans/round41_c1_verify.py --lane . --work $S/w/r41_c1` | 0 | `PINS total=2 mismatched=0` · `BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0` · `MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0` · `MUTANTS-BY-TOOL receipts=13/13 sources=10/10` · `PINS-AFTER mismatched=0` · `PREDICATE C1 pass` (`r41_c1.log`) |
| 2 | `plans/round40_c1_verify.py …` | 0 | `PINS total=3 mismatched=0` · `BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0` · `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0` · `PREDICATE C1 pass` (`r40_c1.log`) |
| 3 | `plans/round39_c1_verify.py …` | 0 | `PINS total=26 mismatched=0` · `BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0` · `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0` · `PREDICATE C1 pass` (`r39_c1.log`) |
| 4 | `plans/round37_c1_verify.py …` | 0 | `BATTERY fixtures=64 wrong=0 renamed_disagree=0` · `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0` · `PREDICATE C1 pass` (`r37_c1.log`) |
| 5 | `plans/round41_c2_verify.py …` | 0 | `checks=8 defects=0` · `PREDICATE C2 pass` (`r41_c2.log`) |
| 6 | `plans/round40_c2_verify.py …` | 0 | `checks=7 defects=0` · `PREDICATE C2 pass` (`r40_c2.log`) |
| 7 | `plans/round39_c2_verify.py …` | 0 | `checks=7 defects=0` · `PREDICATE C2 pass` (`r39_c2.log`) |
| 8 | `plans/round38_c2_verify.py …` | 0 | `checks=7 defects=0` · `PREDICATE C2 pass` (`r38_c2.log`) |
| 9 | `plans/round37_c2_verify.py …` | 0 | `checks=7 defects=0` · `PREDICATE C2 pass` (`r37_c2.log`) |
| 10 | `plans/round36_c2_verify.py --lane . --fleet /home/vgpnk/Projects/shokunin` | 0 | `W1 ok` `W2 ok` `W3 ok` · `checks=6 defects=0` · `PREDICATE C2 pass` (`r36_c2.log`) |
| 11 | `plans/anchor_digest_check.py --lane .` | 0 | `rows=117 tokens=24 defects=0` (`anchor.log`) |
| 12 | `plans/ledger_tip.py --source $S/lane --work $S/lt` | 0 | `REF AUDIT ref=refs/heads/master rev=523b278… tip=523b278… state=match` · `rows=9 closed=9 observed_pass=9 mismatches=0` (`ledger_tip.log`) |
| 13 | `plans/tip_receipts.py --lane . --work $S/tr` | 0 | `tip 523b278…` · `note compared=8 declared_bounded=1 no_command=19` · `receipts=28 byte_equal=8 differ=0 skipped=20` · auto control `control receipt=corpus/evidence/round35/tb2-grader-probe.txt flip=byte 1699 0x27->0x26 verdict=differ` (`tip_receipts.log`) |
| 14 | `plans/order_check.py --lane . --claims plans/round-39-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt` | 0 | `ORDER freeze=088f7c36…` `receipt_commit=6a1eb5e1…` `ORDER RESULT PASS` (`order39.log`) |
| 15 | same, `round-40-claims.md` + `corpus/evidence/round40/db-wal-probe.txt` | 0 | `ORDER freeze=bbb10950…` `receipt_commit=055748f7…` `ORDER scanned commits=1 file_entries=12 distinct_blobs=12` `ORDER RESULT PASS` (`order40.log`) |
| 16 | same, `round-41-claims.md` + `corpus/evidence/round41/constraints-probe.txt` | 0 | `ORDER freeze=8ef8b4fc…` `receipt_commit=f774a87a…` `ORDER RESULT PASS` (`order41.log`) |
| 17 | same, `round-42-claims.md` + `corpus/evidence/round42/fibsqrt-probe.txt` | 0 | `ORDER freeze=bc856d80…` `receipt_commit=523b2780…` `ORDER scanned commits=1 file_entries=21 distinct_blobs=21` `ORDER RESULT PASS` (`order42.log`) |
| 18 | `plans/round_close.py --lane . --round 41 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | 0 | `ROUND-CLOSE order receipt=corpus/evidence/round41/constraints-probe.txt exit=0 verdict=PASS` · `census exit=0 warnings=15 verdict=PASS` · `ROUND-CLOSE RESULT PASS exit=0` (`close41.log`) |
| 19 | same, `--round 42` | 0 | `ROUND-CLOSE order receipt=corpus/evidence/round42/fibsqrt-probe.txt exit=0 verdict=PASS` · `census exit=0 warnings=15 verdict=PASS` · `ROUND-CLOSE RESULT PASS exit=0` (`close42.log`) |
| 20 | `plans/constraints_probe.py --lane . --work $S/pr`, stdout byte-compared with `corpus/evidence/round41/constraints-probe.txt` | 0 | `byte_equal=yes` `fresh_sha256=c5aa6742…` = `receipt_sha256=c5aa6742…`, 5775 B · `regrade cases=25 differ=0` · `cases=25 observed_pass=6 observed_fail=19 mismatches=2` (`constraints_probe.out`, `.err` empty) |
| 21 | `plans/db_wal_probe.py --lane . --work $S/pr`, stdout byte-compared with `corpus/evidence/round40/db-wal-probe.txt` | 0 | `byte_equal=yes` `fresh_sha256=c74c6b91…` = `receipt_sha256=c74c6b91…`, 8257 B · `regrade cases=28 differ=0` · `cases=28 observed_pass=8 observed_fail=20 mismatches=0` (`db_wal_probe.out`, `.err` empty) |
| 22 | `plans/routed_open.py --lane .` | 0 | `ROWS total=10 open=4 blocked=1 closed=5 refused=0` · `routed_open=5 oldest_round=39` (`routed_open.log`) |
| 23 | `sha256sum -c .ufo/waves/round-42/claims/frozen-digests.txt` (clone root) | 0 | `frozen_ok=12 want=12 failed=0` (`frozen42.log`) |
| 24 | `sha256sum -c .ufo/waves/round-41/claims/frozen-digests.txt` (clone root) | 0 | `frozen_ok=11 want=11 failed=0` (`frozen41.log`) |

Strictness of the tally: `check` needs exit 0 **and** the named verdict line (a summary-only pass cannot count);
`check_frozen` needs `ok == wc -l <digest list>` and `failed == 0`; `cmpcheck` needs exit 0 **and** `cmp -s` silence
against the committed receipt, and prints both sha256 so a byte-equal claim is checkable from the log alone.

`round_close` was given `--census` explicitly (a scratch clone's parents hold no fleet census script) and
`ledger_tip` `--source $S/lane` (the clone, not the live lane) — setup inputs, not verdicts.

## Uncounted: freeze-state observation of the round-42 counters (`r42_c1_observe.log`, `r42_c2_observe.log`)

Both round-42 counters are **red at this commit by construction** — wave 1 is the wave that builds them — so they
are printed here as observations and kept out of the 24. They reproduce the frozen controls exactly:

- `plans/round42_c1_verify.py --lane . --work $S/w/r42_c1` → exit 1, `BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=14 killed=0 survived=14 invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=0/9 order=0/5`, `PINS-AFTER mismatched=0`, `PREDICATE C1 fail` — the same shape as `.ufo/waves/round-42/claims/control-c1-nothing.txt` (`killed=0 survived=14`).
- `plans/round42_c2_verify.py --lane . --work $S/w/r42_c2` → exit 1, `checks=9 defects=5`, `PREDICATE C2 fail`; V1 `gate: P10 ok probe_rerun=byte-equal bytes=4212`, `gate: P2 ok receipt_sha256=pinned`, `gate: P9 ok untracked=0`; the defects are the unadmitted entry (`P3/P4/P6/P7/P8/V2/V3/V4/V7/V9`), i.e. the entry does not exist yet at the receipt commit.

Useful calibration inside that red: at this commit the counter's V8 leg is **green** (`V8 ok order_exit=0 result=PASS`),
so the round-42 order pair (claims before receipt) already holds *before* the entry lands.

## Host-safety receipts (orchestrator rule; QUALITY Q32)

Envelope, verbatim, wrapping **every** leg (nesting-safe: the counters build their own read-only sandboxes inside it):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
      --proc /proc --unshare-pid --die-with-parent  <command>
```

Each leg additionally got `TMPDIR=$S/tmp/<leg>` and `HOME=$S/tmp/<leg>/home` (created), so a write attempted by any
instrument lands in scratch, never in `$HOME`.

- `ls -A /home/vgpnk/.local/bin | sha256sum` = `763032563d3739aa6513b8aa3f0852d1cd7e7e4ba0a21165a391fc4026d60a78` **before** (17:35:34) and the same value **after** (17:43:28): `pathdir_sha_after=763032563d3739aa…` — unchanged. The run printed 26 `INSTRUMENT` lines (24 counted legs + 2 uncounted) and all 52 per-leg 16-char `pathdir_sha_before/after` fields are `763032563d3739aa`.
- `pathdir_new_entries=0` (`find /home/vgpnk/.local/bin -newermt @<start> | wc -l`), `git_entry_before=absent`, `git_entry_after=absent`, `files_before=52 files_after=52` — the round-40 `git`-shim vector stayed closed for the whole run.
- `clone_head_after=523b27806be0df26d2235089d845265a29f8cedf`, `clone_dirty_after=0` — no instrument modified the measured tree (untracked files included).
- `lane_tip_before=fda71ae0…` → `lane_tip_after=ff14d76d…`: the **live** lane advanced while the run was in flight (another seat's landing `round-42: landing — battery42 (29 fixtures), circuit-fibsqrt entry + S125-S128, …`); the measured tree is the pinned clone and never moves. No git or jj mutation was issued against the lane from this seat.
- Tool installs: **none** (nothing was missing; no pacman, no `uv tool`, no binary fetch).

## Calibration: the run that was thrown away

Run 1 (17:29:08→17:35:15, kept as `logs/run-1-cmpcheck-bug.log`, sha256 `c2a598ed…`) reported
`baseline green=22 of 24 reds= constraints_probe db_wal_probe`. Both reds were **my harness**, not the lane:

```
python3: can't open file '.../lane/constraints_probe': [Errno 2] No such file or directory    (constraints_probe.err)
```

`cmpcheck` declared `local name=$1 receipt=$2` without `shift 2`, so `python3` received the bare leg name as its
script. Fixed (`shift 2`, plus `mkdir -p "$S/w/$name"`), re-ran from a fresh clone at the same commit: both legs exit 0
with `byte_equal=yes`. The lesson is recorded because it is the failure mode a green tally must survive: a leg that
never executed still prints `exit=` and `byte_equal=no`, so the tally must key on exit **and** on the byte-compare,
never on the absence of a complaint.

## Limits / what was not run, and why

- **Round-42 counters are not counted legs.** They are the wave in flight (C1 battery, C2 entry); their red state at
  this commit is the freeze state, observed above against the frozen control, not a no-harm regression.
- The no-harm claim covers **this commit**. The lane has since landed `ff14d76`; a post-integration no-harm check is
  the parent's gate, and `measure.sh` runs it unchanged with `COMMIT=ff14d76d32d662f7b7073a2acb049594cb740d84`.
- Cross-check on the live lane (read-only, 17:43:39 and 17:43:51, at tip `ff14d76`): `sha256sum -c
  .ufo/waves/round-42/claims/frozen-digests.txt` → 12 `OK` lines, 0 `FAILED`; round-41's list → 11 `OK`, 0 `FAILED`.
  The landing did not disturb the frozen bytes.
- `routed_open` was run without `--observe`: the ticket names the burn-down line (`routed_open=<n>`), and `--observe`
  executes each row's `check` shell command against the lane tip — a different measurement (and R39-R4's check is
  known to exit 2 at this commit, per the row's own `note`).
- `constraints_probe` exits 0 with `mismatches=2`: prediction mismatches are on the summary line by design
  (`corpus/evidence/round41/constraints-probe.txt` carries the same two), and the receipt reproduces byte for byte.
- No build, lint, formatter or test was run beyond the named instruments; no corpus/plans/lane file was edited by this seat.

VERDICT: no-harm-baseline-24-green-of-24
