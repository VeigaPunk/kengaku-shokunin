# E12ScratchHygiene — scratch-discipline + disk audit, kengaku round 55 w1

Addendum §7 duty. Read-only audit; nothing deleted; no installs; no git mutations.
Full verbatim report: `.ufo/waves/round-55/w1/E12ScratchHygiene/report.md`.

## 1. `df -h /fast/scratch /tmp` (exit 0)

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  373G  431G  47% /fast        (second snapshot: 379G used / 425G avail)
/dev/nvme1n1p1  128G   32G   97G  25% /tmp
```

`/fast/scratch/hyaku/kengaku-r55` totals 1.3G — `c1before` 638M + `E10NoharmRuns` 638M;
all other seat dirs ≤12K. Healthy free space.

## 2. Script audit (per script)

- **`plans/round55_c2_controls.py` (present):** no hardcoded `/tmp` (no literal; all paths
  via `tempfile`). Work dir at `plans/round55_c2_controls.py:191` is
  `mkdtemp(dir="/fast/scratch/hyaku/kengaku-r55")` — the round-mandated scratch root, but the
  script has **no `--work`/`--receipt` argument** and ignores TMPDIR on the main path
  (finding 3 below). Selftest at `:144` uses `TemporaryDirectory()` → honours TMPDIR, falls
  back to `/tmp` if unset (KB-sized fixtures, inside the <50 MB clause). Fixture cleanup
  PASS: `try/finally shutil.rmtree(work)` at `:192-195`; selftest via context manager.
  Git-mutation guard PASS: asserts `rev-parse --show-toplevel` equals the fixture root at
  `:92-95`. No `/tmp/kengaku-r55-controls-*` leak dirs observed.
- **`plans/round55_c2_entryargv.py`: ABSENT** at audit time (ls exit 2) — frozen C2 counter
  not yet landed; controls `--against r55` would exit 2 today. Re-audit on landing.
- **`plans/round55_c3_chess_probe.py`: ABSENT** at audit time (ls exit 2) — frozen C3 probe
  not yet landed; re-audit on landing.

## 3. Seat-dir census — `find /fast/scratch/hyaku/kengaku-r55 -maxdepth 1 -type d | sort`

Mid-wave (dirs appeared between two passes; nothing deleted):

```
c1before  E1RegistryRows  E3ControlsVerify  E4LedgerTruth  E6ChessReceipt
E8SourcesRows  E9IndexAndReadme  E10NoharmRuns  E11SelftestReceipts  E12ScratchHygiene
E13BindingScan  E14CaptureIdentity  E15DefectLedgerSweep  S1CaseProse  S3GateQuotes
upstream
```

All correctly rooted under the round scratch root; `c1before`/`upstream` are claim-owned,
not seat dirs.

## 4. `/tmp` artifact check — expectation "none" does NOT hold

- **This wave:** `/tmp/r55-instruction.md` (260 B, mtime 2026-10-30 12:26) — verbatim the C3
  chess-best-move instruction. Current-wave kengaku material outside the scratch root;
  owner likely the C3 probe seat (E6ChessReceipt). **Violation — for integrator follow-up.**
- **Kengaku lane, today pre-wave:** `/tmp/kengaku-r53-closure.json` (03:13),
  `/tmp/kengaku-r54-closure.json` (09:11).
- **Kengaku leftovers, prior rounds/planning (10-27/10-28):** `closure-kengaku-r46.json`,
  `closure-kengaku-r48.json`, `closure-kengaku-r51.json`, `kengaku-r50-closure.json`,
  `kengaku-r52-cited-cmds.txt`, `r55-controls.sh`, `r55-hashes.txt`, `r55r56-notes.txt`.
- **Other lanes (listed, not policed):** `census-r55*.txt` + `r55ctx.txt` (tameshi,
  content-verified), `closure-r55-tameshi.json`, `closure-mado-r55.json`, `r55chk.py` +
  `r55entry.md` (mado/hyprland), `kama-r55-*` (kama).
- **Dead dirs:** 4× empty `r55-lab-mutant.*` (10-28), `r55x` scratch clone (10-28).
- /tmp was being actively mutated during the audit (kengaku r53/r54 closures vanished and
  reappeared between `ls` and `stat` passes).

## Named violations (file:line)

- `/tmp/r55-instruction.md` — r55 wave artifact outside `/fast/scratch/hyaku/kengaku-r55/`.
- `/tmp/kengaku-r5{3,4}-closure.json` — r55-day closure receipts outside the scratch root.
- `plans/round55_c2_controls.py:191` — no `--work`/`--receipt` argument; work dir frozen to
  the round root (round-compliant scratch-wise; misses the parameterisation clause).
- `plans/round55_c2_controls.py:144` — selftest falls back to `/tmp` when TMPDIR unset.
