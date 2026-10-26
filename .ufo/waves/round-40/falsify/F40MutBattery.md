# F40MutBattery — battery-fixture mutation probe (round 40, wave 2 FALSIFY)

- Seat: F40MutBattery (mutation-tester, leaf). Date: 2026-10-26.
- Lane tip measured: `ec1005a2a28bc5cfdde7723374368ed4cc956eed` (master), scratch clone `/fast/scratch/hyaku/kengaku-r40/F40MutBattery/lane` (`git clone --no-local` + `checkout -q ec1005a2a…`; `rev-parse --show-toplevel` verified equal to the clone before any write; `git status --porcelain` = 0 lines).
- Target: `plans/battery40/*.py` (7 modules, 21 fixtures), attacked at the fixture level. For each fixture I reverted the one behavior-bearing edit that makes the fixture exhibit its advertised behaviour (scratch copy only), then ran the frozen counter `plans/round40_c1_verify.py` against the mutated battery under the HOST-SAFETY sandbox.
- Axes (godspeed): detection power (does the counter visibly flip), fidelity (one behavioral point per fixture, receipts carry the exact diff), coverage (all 21 fixtures, all 7 modules).

## Detector and sandbox (every invocation)

Every run was the frozen counter, wrapped exactly as ruled:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
  --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
  python3 "$S/lane/plans/round40_c1_verify.py" --lane "$S/lane" \
  --battery-dir <battery copy> [--only <MID>] --work "$S/c1work" --jobs 8
```

`S=/fast/scratch/hyaku/kengaku-r40/F40MutBattery`, `TMPDIR=$S`. No systemd-run/cron/at, no writes outside the scratch and this report dir; the neutralized wave-1 evidence scripts were never executed.

## Baseline leg (pristine battery — inconclusive-if-failing gate)

`--battery-dir $S/base/battery40` (pristine copy), full mutant set. rc=0, 57.7 s wall:

- `PINS total=3 mismatched=0`
- `BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0` and 21 `FIXTURE … ok` lines
- `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0`
- `PINS-AFTER mismatched=0`

Every mutant printed `killed by=<fid>` naming exactly the fixture I then mutated — that is the witness mapping the probes test. Receipt: `receipts/baseline-pristine-battery.txt`.

## Fixture mutants and results

One battery-module copy per mutant (`$S/mut-<MID>/battery40`); each probe ran the counter with `--battery-dir` on that copy and `--only <MID>`, so the only changed input vs baseline is the fixture edit. "Caught" = the targeted fixture prints `WRONG` or the targeted mutant flips to `SURVIVED`. All 21 probes: rc=1 (dev predicate fails on exactly the intended flip), `tampered=0 sidechannel=0`, no `NULL` line (sweep across all 22 outputs: `NO_NULL_TAMPERED_SIDECHANNEL`).

### a_tok (3/3 caught) — token-shape fixtures

| MID | fixture | mutation (mut copy file:line, diff receipt) | FIXTURE verdict | MUTANT verdict | caught |
|---|---|---|---|---|---|
| A01 | a_tok-upper-anchor | `a_tok.py:32` keep token lowercase (`S111.upper()`→`S111`) | WRONG rc=0 observed=- (declared digest-uppercase) | A01 SURVIVED exhibits=none | YES |
| A02 | a_tok-abbrev-7hex | `a_tok.py:38` keep the 8-hex abbreviation (no 7-hex rewrite) | WRONG rc=0 observed=- | A02 SURVIVED | YES |
| A03 | a_tok-abbrev-64hex | `a_tok.py:45` keep the 8-hex abbreviation (no 64-hex+`…` rewrite) | WRONG rc=0 observed=- | A03 SURVIVED | YES |

### a_row (3/3 caught) — row-shape fixtures

| MID | fixture | mutation | FIXTURE verdict | MUTANT verdict | caught |
|---|---|---|---|---|---|
| A06 | a_row-indent4-wrong | `a_row.py:43` keep the row at column 0 (drop `"    " +`) — still carries S108's real digest | WRONG rc=1 observed=digest-wrong-capture | A06 SURVIVED | YES |
| A08 | a_row-token-in-teaches | `a_row.py:53-54` keep the token in the anchor cell (no cell move) | WRONG rc=0 observed=- | A08 SURVIVED | YES |
| A09 | a_row-12-cells | `a_row.py:63` keep 11 cells (no 12th appended) | WRONG rc=0 observed=- | A09 SURVIVED | YES |

### a_bind (3/3 caught) — binding fixtures

| MID | fixture | mutation | FIXTURE verdict | MUTANT verdict | caught |
|---|---|---|---|---|---|
| A15 | a_bind-a15-slug-ambiguity | `a_bind.py:72` drop the second `task.toml` owner (slug unambiguous) | WRONG rc=0 observed=- | A15 SURVIVED | YES |
| A17 | a_bind-a17-index-bytes | `a_bind.py:85,94` row anchors the committed view's digest (`hb`→`ha`) | WRONG rc=1 observed=digest-unknown | A17 SURVIVED | YES |
| A27 | a_bind-a27-token-per-capture | `a_bind.py:61` drop the added second capture URL | WRONG rc=1 observed=digest-wrong-capture (declared capture-unanchored) | A27 SURVIVED | YES |

### a_man (2/2 caught) — manifest-view fixtures

| MID | fixture | mutation | FIXTURE verdict | MUTANT verdict | caught |
|---|---|---|---|---|---|
| A21 | a_man-uppercase-manifest-entry | `a_man.py:65` keep the SHA256SUMS entry lowercase (`dig.upper()`→`dig`) | ok rc=0 | A21 SURVIVED exhibits=none | YES |
| A22 | a_man-stale-manifest-digest | `a_man.py:72` manifest names the committed bytes' digest (not stale) | WRONG rc=1 observed=digest-unknown | A22 still killed by=a_man-uppercase-manifest-entry | YES (fixture-WRONG) |

### l_rows (4/4 caught) — ledger row accounting

| MID | fixture | mutation | FIXTURE verdict | MUTANT verdict | caught |
|---|---|---|---|---|---|
| L05 | l_rows-open-row | `l_rows.py:17-20` keep the row closed (no `open` relabel) | WRONG rc=0 observed=- (declared NO:R34-D2) | L05 SURVIVED | YES |
| L06 | l_rows-empty-ledgers | `l_rows.py:27-28` keep both ledgers populated | WRONG rc=0 observed=- | L06 SURVIVED | YES |
| L14 | l_rows-check-crashes | `l_rows.py:35` keep the TB2 manifest present (no unlink) | WRONG rc=0 observed=- (declared NO:R34-D3) | L14 SURVIVED | YES |
| L15 | l_rows-unknown-check | `l_rows.py:43-46` keep check name `r34_d5` | WRONG rc=0 observed=- (declared NO:R34-D5) | L15 SURVIVED | YES |

### l_refuse (3/3 caught) — ledger setup refusals

| MID | fixture | mutation | FIXTURE verdict | MUTANT verdict | caught |
|---|---|---|---|---|---|
| L01 | l_refuse-source-not-a-repo | `l_refuse.py:38-40` `--source` is a real clone (`ctx.clone`) | WRONG rc=0 (declared error/rc 2) | L01 still killed by=l_refuse-work-lane-exists | YES (fixture-WRONG) |
| L11 | l_refuse-work-lane-exists | `l_refuse.py:47` `{WORK:lane}`→`{WORK}` (no pre-existing `lane/`) | WRONG rc=0 | L11 SURVIVED | YES |
| L21 | l_refuse-stale-pin-ref | `l_refuse.py:53-54` keep `refs/heads/master` at the tip (no rewind) | WRONG rc=0 | L21 SURVIVED | YES |

### o_gate (3/3 caught) — order gate

| MID | fixture | mutation | FIXTURE verdict | MUTANT verdict | caught |
|---|---|---|---|---|---|
| O04 | o_gate-p10-ok-excuse | `o_gate.py:49` control line becomes a DEFECT line (no `ok` + excuse) | WRONG rc=0 (declared hit:gate-p10) | O04 SURVIVED | YES |
| O12 | o_gate-claims-gitlink | `o_gate.py:55` drop the gitlink (`gitlink_ref=None`) | ok rc=0 | O12 SURVIVED exhibits=none | YES |
| O14 | o_gate-claims-bak-name | `o_gate.py:61` claims file named correctly (`claims_name=CLAIMS_BASE`) — cf. `o_gate.py:56-57` "is not a round-NN-claims.md name" | WRONG rc=0 (declared error/rc 2) | O14 SURVIVED | YES |

## Score

Caught/total per module: a_tok 3/3, a_row 3/3, a_bind 3/3, a_man 2/2, l_rows 4/4, l_refuse 3/3, o_gate 3/3 — **21/21**. Two probes (A21, O12) show the flip only as `MUTANT … SURVIVED` (fixture stays ok by design: the mutated fixture still satisfies its `expect`); 19 show `FIXTURE … WRONG` (`BATTERY … wrong=1`; raw counts: 2× `wrong=0`, 19× `wrong=1` across the 21 probe BATTERY lines). No probe tripped `tampered`, `sidechannel`, or `NULL`.

## Findings (coverage, not contract changes)

1. **A22 and L01 have sibling killers**, as their module docstrings state ("the uppercase fixture kills both", a_man.py:23-25; "the two other refusal fixtures also exhibit L01's relabelled exit", l_refuse.py:29-31). For those two the fixture-level mutation cannot produce a `SURVIVED` flip — the catch is the `FIXTURE … WRONG` verdict. Removing the sibling fixture as well would be a two-fixture mutation and was not needed.
2. **Every fixture's exhibit-edit is load-bearing**: un-doing it either silently accepts a declared reject (16 fixtures) or silently rejects/misclassifies a declared accept (A06, A17, A22) — the counter's per-fixture `ok/WRONG` check plus the mutant-kill check jointly detect all 21 single-point fixture corruptions measured here.
3. Process note: the first A17 probe died in build (`SETUP module battery40/a_bind.py failed to build`) because the mutation referenced the wrong local name; rewired to the committed-view digest (`a_bind.py:85`) and re-run green. The failed-run receipt is not among the probes; the fix is visible in `receipts/mut-A17.diff`.

## Restoration evidence

- The lane was never written to: only reads and `git status --porcelain` (= 0 lines at setup); the mandated `PINS total=3 mismatched=0` / `PINS-AFTER mismatched=0` lines in all 22 runs confirm the three pinned tools' bytes before and after every probe.
- All mutations lived in `$S/mut-*/battery40` (scratch); per the fixture rule the scratch is removed after receipts were copied: `rm -rf -- /fast/scratch/hyaku/kengaku-r40/F40MutBattery` (with `TMPDIR` pointing inside it). Nothing was left running.
- Receipts (43 files): `receipts/baseline-pristine-battery.txt`, `receipts/probe-<MID>.txt` (full counter stdout, 21), `receipts/mut-<MID>.diff` (exact one-point edit, 21).
- Tooling: nothing installed or upgraded (bwrap 0.13.1, git, python3 already present — pacman untouched per the pause).

VERDICT: battery-fixture-mutants-caught-21/21
