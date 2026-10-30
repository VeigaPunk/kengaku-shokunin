# E12ScratchHygiene — scratch-discipline + disk audit, kengaku round 55 w1

Addendum §7 duty. Read-only audit: no files written outside `.ufo/waves/round-55/w1/` outputs;
nothing deleted (mid-wave census, not a cleanup pass). Scratch dir
`/fast/scratch/hyaku/kengaku-r55/E12ScratchHygiene/` created (empty throughout) and removed
after reporting. No tools installed. No git mutations.

Commands run and exit codes:

- `df -h /fast/scratch /tmp` → 0 (two snapshots, below)
- `find /fast/scratch/hyaku/kengaku-r55 -maxdepth 1 -type d | sort` → 0 (two snapshots)
- `ls /tmp` (+ `grep -iE 'kengaku|r55'`, `stat`, `head`) → 0
- `ls /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round55_c2_entryargv.py /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round55_c3_chess_probe.py` → 2 (both absent at audit time)
- `grep -nE '/tmp|mkdtemp|TemporaryDirectory|TMPDIR|--work' plans/round55_c2_controls.py` → 0
- `du -sh /fast/scratch/hyaku/kengaku-r55{,/*}` → 0

## §1 Disk space — `df -h /fast/scratch /tmp`

Snapshot at audit start (~12:05 -0300):

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  373G  431G  47% /fast
/dev/nvme1n1p1  128G   32G   97G  25% /tmp
```

Snapshot at report write (~12:30 -0300):

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  379G  425G  48% /fast
/dev/nvme1n1p1  128G   32G   97G  25% /tmp
```

Both filesystems healthy; /fast usage grew ~6 GB during the audit (wave in flight).
`du -sh /fast/scratch/hyaku/kengaku-r55` → `1.3G` total: `c1before` 638M + `E10NoharmRuns` 638M
dominate; all seat dirs otherwise ≤12K (or empty).

## §2 Per-script /tmp + work-dir + cleanup audit

### plans/round55_c2_controls.py — present (9308 B, mtime 10-30 11:45)

- **Hardcoded `/tmp`:** none. `grep -n '/tmp'` → no literal; all temp paths via `tempfile`.
- **Work dir:** `main()` uses
  `tempfile.mkdtemp(prefix="kengaku-r55-controls-", dir="/fast/scratch/hyaku/kengaku-r55")`
  (`plans/round55_c2_controls.py:191`) — the sanctioned round scratch root, hardcoded per
  the round freeze ("Scratch lives under `/fast/scratch/hyaku/kengaku-r55/` only").
  **Finding:** the script has **no `--work`/`--receipt` argument** and does not consult
  TMPDIR on the main path; work placement is frozen to the round root. Compliant with the
  round's scratch rule, but does not meet the "honour a --work/--receipt argument" clause
  of the seat contract's committed-tool wording. Flagging for the integrator — likely
  intentional here since the cases are frozen fixtures, but it is the only committed r55
  script so far and it cannot be pointed elsewhere.
  Minor: `dir=` root must exist or `mkdtemp` raises (no `mkdir -p`).
- **Selftest path:** `tempfile.TemporaryDirectory()` (`plans/round55_c2_controls.py:144`)
  honours TMPDIR, falling back to `/tmp` when unset. Fixture mass is a few KB (well under
  the 50 MB /tmp bound), so the fallback is acceptable but not under the round scratch root.
- **Cleanup:** PASS — `try: ... finally: shutil.rmtree(work, ignore_errors=True)`
  (`plans/round55_c2_controls.py:192-195`) wraps the case run; selftest cleans up via the
  `TemporaryDirectory` context manager.
- **Fixture mutation guard:** PASS — asserts `git rev-parse --show-toplevel` of the fixture
  equals the fixture root before proceeding (`plans/round55_c2_controls.py:92-95`), matching
  the host guard. Fixtures are built entirely under the work dir (git init/add/commit inside
  `$work/fixture-*`), never inside the lane; the r54/r55 counters are loaded read-only via
  `importlib` from `LANE/plans/`.
- **/tmp leak check:** `ls -d /tmp/kengaku-r55-controls-*` → none observed.

### plans/round55_c2_entryargv.py — ABSENT at audit time

`ls` → `No such file or directory`. The new C2 binding counter (frozen instrument, claims
§R55-C2) has not landed yet mid-wave; `run_case --against r55` in the controls script will
currently exit 2 (`SETUP plans/round55_c2_entryargv.py absent`, line ~124-127). Nothing to
audit; the integrator should re-run this check once it lands (verify `--work` honoured per
its frozen signature `--lane/--source/--work/--jobs/--timeout/--dry/--selftest`).

### plans/round55_c3_chess_probe.py — ABSENT at audit time

`ls` → `No such file or directory`. The frozen C3 probe has not landed yet mid-wave;
re-audit on landing. (Note: `/tmp/r55-instruction.md`, the C3 chess instruction text, already
appeared in /tmp — see §4.)

## §3 Mid-wave seat-dir census — `find /fast/scratch/hyaku/kengaku-r55 -maxdepth 1 -type d | sort`

First pass (~12:05 -0300), 9 entries:

```
/fast/scratch/hyaku/kengaku-r55
/fast/scratch/hyaku/kengaku-r55/c1before
/fast/scratch/hyaku/kengaku-r55/E10NoharmRuns
/fast/scratch/hyaku/kengaku-r55/E11SelftestReceipts
/fast/scratch/hyaku/kengaku-r55/E1RegistryRows
/fast/scratch/hyaku/kengaku-r55/E4LedgerTruth
/fast/scratch/hyaku/kengaku-r55/E6ChessReceipt
/fast/scratch/hyaku/kengaku-r55/E9IndexAndReadme
/fast/scratch/hyaku/kengaku-r55/upstream
```

Second pass (~12:20 -0300), 16 entries — E3ControlsVerify, E8SourcesRows, E13BindingScan,
E14CaptureIdentity, E15DefectLedgerSweep, S1CaseProse, S3GateQuotes and my own
E12ScratchHygiene appeared between passes (wave actively spawning):

```
/fast/scratch/hyaku/kengaku-r55
/fast/scratch/hyaku/kengaku-r55/c1before
/fast/scratch/hyaku/kengaku-r55/E10NoharmRuns
/fast/scratch/hyaku/kengaku-r55/E11SelftestReceipts
/fast/scratch/hyaku/kengaku-r55/E12ScratchHygiene
/fast/scratch/hyaku/kengaku-r55/E13BindingScan
/fast/scratch/hyaku/kengaku-r55/E14CaptureIdentity
/fast/scratch/hyaku/kengaku-r55/E15DefectLedgerSweep
/fast/scratch/hyaku/kengaku-r55/E1RegistryRows
/fast/scratch/hyaku/kengaku-r55/E3ControlsVerify
/fast/scratch/hyaku/kengaku-r55/E4LedgerTruth
/fast/scratch/hyaku/kengaku-r55/E6ChessReceipt
/fast/scratch/hyaku/kengaku-r55/E8SourcesRows
/fast/scratch/hyaku/kengaku-r55/E9IndexAndReadme
/fast/scratch/hyaku/kengaku-r55/S1CaseProse
/fast/scratch/hyaku/kengaku-r55/S3GateQuotes
/fast/scratch/hyaku/kengaku-r55/upstream
```

All seat dirs are correctly rooted under the round scratch root; no stray `kengaku-r55-*`
mkdtemp dirs at root level. `upstream` and `c1before` are shared/claim-owned dirs, not seat
dirs. Census only — nothing deleted.

## §4 /tmp artifact check — `ls /tmp` vs `kengaku|r55`

The expectation "none" does NOT hold. `ls -la /tmp | grep -iE 'kengaku|r55'` (final state
~12:26 -0300; /tmp is being actively mutated — `closure-kengaku-r53.json` and
`closure-kengaku-r54.json` vanished and reappeared during the audit window):

```
-rw-r--r--    1 vgpnk vgpnk     1604 Oct 28 14:31 census-r55-mut.txt
-rw-r--r--    1 vgpnk vgpnk     1604 Oct 28 14:03 census-r55-rev01.txt
-rw-r--r--    1 vgpnk vgpnk     1604 Oct 28 14:52 census-r55.txt
-rw-r--r--    1 vgpnk vgpnk     1604 Oct 28 14:52 census-r55b.txt
-rw-r--r--    1 vgpnk vgpnk     1604 Oct 28 14:47 census-r55w3revw2.txt
-rw-r--r--    1 vgpnk vgpnk     2954 Oct 27 03:23 closure-kengaku-r46.json
-rw-r--r--    1 vgpnk vgpnk     2906 Oct 27 09:58 closure-kengaku-r48.json
-rw-r--r--    1 vgpnk vgpnk     4057 Oct 28 15:54 closure-kengaku-r51.json
-rw-r--r--    1 vgpnk vgpnk     3066 Oct 28 20:59 closure-mado-r55.json
-rw-r--r--    1 vgpnk vgpnk     4929 Oct 28 15:02 closure-r55-tameshi.json
-rw-r--r--    1 vgpnk vgpnk     3064 Oct 27 11:32 kama-r55-closure-entry.json
-rw-r--r--    1 vgpnk vgpnk   830605 Oct 27 11:21 kama-r55-git-config.html
-rw-r--r--    1 vgpnk vgpnk    31125 Oct 27 11:21 kama-r55-proc5.html
-rw-r--r--    1 vgpnk vgpnk     4778 Oct 28 14:54 kengaku-r50-closure.json
-rw-r--r--    1 vgpnk vgpnk     2709 Oct 28 16:51 kengaku-r52-cited-cmds.txt
-rw-r--r--    1 vgpnk vgpnk     3634 Oct 30 03:13 kengaku-r53-closure.json
-rw-r--r--    1 vgpnk vgpnk     5029 Oct 30 09:11 kengaku-r54-closure.json
-rw-r--r--    1 vgpnk vgpnk     7697 Oct 28 14:53 r55-controls.sh
-rw-r--r--    1 vgpnk vgpnk     4187 Oct 27 04:08 r55-hashes.txt
-rw-r--r--    1 vgpnk vgpnk      260 Oct 30 12:26 r55-instruction.md
drwx------    2 vgpnk vgpnk        6 Oct 28 14:08 r55-lab-mutant.4b2i0t4h
drwx------    2 vgpnk vgpnk        6 Oct 28 14:09 r55-lab-mutant.lj31nhey
drwx------    2 vgpnk vgpnk        6 Oct 28 14:08 r55-lab-mutant.p4ba44si
drwx------    2 vgpnk vgpnk        6 Oct 28 14:09 r55-lab-mutant.pct1l9eq
-rw-r--r--    1 vgpnk vgpnk      490 Oct 28 20:55 r55chk.py
-rw-r--r--    1 vgpnk vgpnk     5751 Oct 28 14:42 r55ctx.txt
-rw-r--r--    1 vgpnk vgpnk    22169 Oct 30 03:29 r55entry.md
-rw-r--r--    1 vgpnk vgpnk     3275 Oct 27 05:45 r55r56-notes.txt
drwxr-xr-x    4 vgpnk vgpnk       31 Oct 28 20:57 r55x
```

**Attribution (content-checked, not guessed):**

- **This kengaku round-55 wave (dated 10-30):**
  - `/tmp/r55-instruction.md` (260 B, 12:26 today) — verbatim the C3 `chess-best-move`
    instruction ("The file chess_board.png has an image of a chess board. It is currently
    white to move. Write the best move ... /app/move.txt ... [src][dst]"). Almost certainly
    a current-wave C3 seat's probe material landing in /tmp instead of the round scratch
    root or a bwrap-private mount. **Scratch-discipline violation; owner likely E6ChessReceipt
    or a C3 probe seat — named for integrator follow-up.**
  - `/tmp/kengaku-r53-closure.json` (10-30 03:13), `/tmp/kengaku-r54-closure.json`
    (10-30 09:11) — kengaku-lane closure receipts written today in /tmp (outside
    `/fast/scratch/hyaku/kengaku-r55/`). Pre-wave timing suggests L1/planning-side tooling.
- **Earlier kengaku rounds' leftovers (10-27/10-28):** `closure-kengaku-r46.json`,
  `closure-kengaku-r48.json`, `closure-kengaku-r51.json`, `kengaku-r50-closure.json`,
  `kengaku-r52-cited-cmds.txt` (list of `python3 plans/...` counter invocations),
  `r55-controls.sh` (7.7K, 10-28 — differs from the landed 9.3K
  `round55_c2_controls.py`), `r55-hashes.txt`, `r55r56-notes.txt` — stale kengaku /tmp
  leakage from prior rounds and r55 planning; a recurring discipline pattern.
- **Other lanes' round-55 files (not kengaku's to police, listed for completeness):**
  `census-r55*.txt` + `r55ctx.txt` (tameshi, verified by content: "tameshi round 55 ...
  Lane repo /home/vgpnk/Projects/shokunin/tameshi-shokunin"), `closure-r55-tameshi.json`,
  `closure-mado-r55.json`, `r55chk.py` + `r55entry.md` (mado: checks
  `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md`; hyprland = mado scope),
  `kama-r55-*` (kama lane).
- **Leftover work dirs:** `r55-lab-mutant.4b2i0t4h|.lj31nhey|.p4ba44si|.pct1l9eq` — 4 empty
  `drwx------` dirs (10-28), labrat/mutation fixture dirs left behind; `/tmp/r55x` — a
  scratch clone layout (`.ufo/`, `tools/` inside) from 10-28 20:57, matching closure-mado-r55
  timing.

No `kengaku-r55-controls-*` dirs in /tmp — the one landed r55 script keeps its work dirs
under the round scratch root as designed.

## Defects / risks reported for the L1

1. `/tmp/r55-instruction.md` — current-wave kengaku C3 material outside the scratch root.
2. `/tmp/kengaku-r5{3,4}-closure.json` written today outside the scratch root (pre-wave).
3. `plans/round55_c2_controls.py:191` — no `--work`/`--receipt` argument; work dir frozen to
   the round root (round-compliant, but misses the committed-tool parameterisation clause).
4. `plans/round55_c2_controls.py:144` — selftest `TemporaryDirectory()` falls back to /tmp
   when TMPDIR is unset (acceptable under the <50 MB clause; not under the round root).
5. `plans/round55_c2_entryargv.py` and `plans/round55_c3_chess_probe.py` not yet landed;
   audit deferred — re-run this seat's §2 checks once they exist.
6. Dead `r55-lab-mutant.*` dirs + `r55x` + multi-round `/tmp` leftovers show /tmp leakage is
   habitual fleet-wide; /tmp has no /fast-style round-root convention at all.
