# R45NoHarmBaseline — pre-claim no-harm baseline (kengaku round 45, wave 1)

Seat: `R45NoHarmBaseline` (executor, leaf). Scope: **measure only** — no lane file was edited, no counter/fixture/probe/frozen
artifact was touched, nothing committed anywhere. All runs happened inside the frozen envelope.

## Axes (Godspeed)

1. **host-safety** — no write to any PATH dir / `/usr` / `/etc` / `$HOME` outside scratch (envelope content digest brackets every run).
2. **operability** — the pre-claim red/green lines the round-45 final measure must not regress beyond, produced from a clean clone of the freeze commit.
3. **fidelity** — instrument identity (lane copy vs clone copy) recorded per tool so the baseline cannot be silently compared against a different counter.
4. **reproducibility** — exact commands, seeds, scratch paths and exit codes are in the receipt.

## Setup (exact)

```
S=/fast/scratch/hyaku/kengaku-r45/R45NoHarmBaseline ; mkdir -p "$S/w" ; export TMPDIR="$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" checkout -q b4fcd35141acda5fa0980a34dd29ab880b702ee6
git -C "$S/lane" rev-parse --show-toplevel      -> /fast/scratch/hyaku/kengaku-r45/R45NoHarmBaseline/lane
git -C "$S/lane" rev-parse HEAD                 -> b4fcd35141acda5fa0980a34dd29ab880b702ee6  ("round-45: freeze claims, C1 fence counter + hostile/control evidence, C2 password-recovery instruments")
git -C "$S/lane" status --porcelain             -> (empty; clean clone)
```

Envelope on **every** run (no exceptions):
`.ufo/waves/round-45/claims/envelope.sh "$S/env" <cmd…>` — `bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk`,
scratch writable, `~/.cache` overlaid from `$S/env/home-cache`, `--unshare-pid`.
PATH-dir content digest `local_bin_content_before=after=c263b11afb1cccf6` and `unchanged` in **all ten** measurement runs below (no
`exit=4`/`INVALID` occurred; nothing was re-run).

Instrument identity (sha256 lane HEAD `52d7486` vs clone `b4fcd35`) — recorded because a baseline against a *different*
counter is not a baseline:

| tool | lane | clone | verdict |
|---|---|---|---|
| `plans/round44_c1_verify.py` | 6cf05323bafa9cdb… | 6cf05323bafa9cdb… | SAME |
| `plans/round44_c2_verify.py` | 334ce2dac6828f8d… | 334ce2dac6828f8d… | SAME |
| `plans/anchor_digest_check.py` | 11bb2cad87be1c29… | 11bb2cad87be1c29… | SAME |
| `plans/order_check.py` | 948d5e1d2b3429d7… | 948d5e1d2b3429d7… | SAME |
| `plans/routed_open.py` | 3ce44d941b14a28c… | 3ce44d941b14a28c… | SAME |
| `plans/pkg_gate.py` | ea63882240e67e99… | ea63882240e67e99… | SAME |
| `plans/password_recovery_probe.py` | f87a9eebe464b29d… | f87a9eebe464b29d… | SAME |
| `plans/round45_c1_verify.py` | 7745eb0a4bdf281a… | 7745eb0a4bdf281a… | SAME |
| `plans/round45_c2_verify.py` | 8c30270963ebefe3… | 804df72560e5f14a… | **DIFF** (post-freeze re-pin, 8 rows vs 9) |
| `plans/pkg-spec-r45.json` | 3eb696b47095627b… | b8fc1e537acbdfa7… | **DIFF** (8 rows vs 9) |

## Expected-red / expected-green lines (the baseline)

Receipt: `.ufo/waves/round-45/w1/R45NoHarmBaseline/measure-baseline.txt` (439 lines, sha256 `028ed1020e841ea0efd1e23b0572991e810409977642b0908f18942d33b84c1e`) — header summary + all ten measurement runs verbatim; per-run files `m1-c1.txt … m8b-r45c2-freeze.txt` sit beside it.

| # | command | baseline line(s) | exit |
|---|---|---|---|
| M1 | `python3 <lane>/plans/round44_c1_verify.py --lane "$S/lane" --work "$S/w"` | `PINS total=2 mismatched=0` · `BATTERY fixtures=33 wrong=0 tampered=0 sidechannel=0` · `MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0` · `MUTANTS-BY-TOOL anchor=4/4 order=1/1` · `ADVERTISED direct=5 indirect=0 none=0` · `PINS-AFTER mismatched=0` · **`PREDICATE C1 pass`** | 0 |
| M2 | `python3 <lane>/plans/round44_c2_verify.py --lane "$S/lane"` | `V1 ok listed=11` · gate `P1..P10 ok`, `P3 rows=22 distinct_quotes=22`, `P6 rows=9`, `P8 index_rows=51 knowledge_files=51`, `P10 probe_rerun=byte-equal bytes=3630` · `V4 cases=14` · `V11 states=48 grader_pass=24 grader_fail=24 disagree=0` · `checks=11 defects=0` · **`PREDICATE C2 pass`** | 0 |
| M3 | `python3 <lane>/plans/anchor_digest_check.py --lane "$S/lane"` | **`rows=141 tokens=47 defects=0`** | 0 |
| M4 | `python3 <lane>/plans/routed_open.py --lane "$S/lane" --list` | **`ROWS total=60 open=23 blocked=1 closed=34 refused=2`** · `routed_open=24 oldest_round=39` (60 `ROW` lines) | 0 |
| M5 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | `W04` duplicate-url advisories `S040,S048,S057,S058,S059,S064,S065,S066,S067,S068,S069,S071,S075,S076,S100` (15) · `kengaku ok …/lane/corpus/SOURCES.md` | 0 |
| M6 | `python3 <lane>/plans/round_close.py --lane "$S/lane" --round 44` | `ROUND-CLOSE ERROR no census script (scripts/sources-census.sh); pass --census PATH` · `ROUND-CLOSE RESULT ERROR` | 2 |
| M6b | … `--round 44 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | `ORDER RESULT PASS` (freeze `5f16ed04`, receipt `corpus/evidence/round44/feal-linear-probe.txt`, commit `45dc0bc8`) · `census exit=0 warnings=15 verdict=PASS` · **`ROUND-CLOSE RESULT PASS exit=0`** | 0 |
| M7 | `python3 <lane>/plans/round45_c1_verify.py --lane "$S/lane" --work "$S/w45"` | `FENCE plans/fixture_fence.py absent` · `REFUSALS total=10 clean=0 leaked=10 read=0 hung=0 build_errors=0` · `HONEST fixtures=104 admitted=0 refused=104 read=0 hung=0 build_errors=0` · `CALIBRATION advertised=10 contradicted=10` · **`PREDICATE C1 fail`** | 1 |
| M8 | `python3 <lane>/plans/round45_c2_verify.py --lane "$S/lane"` (post-freeze instrument) | `V1 ok listed=9` · `V2..V4,V7..V11 DEFECT error ValueError: spec template not at its freeze digest` · `V5 ok` · `V6 ok` · `checks=11 defects=8` · `PREDICATE C2 fail` | 1 |
| M8b | `python3 "$S/lane/plans/round45_c2_verify.py" --lane "$S/lane"` (freeze-clone's own copy, `804df7…`) | gate `P1 ok pinned=2`, `P9 ok untracked=0`; `P2/P3/P5/P6/P7/P8/P10 DEFECT` (`P6 rows=9 bad=9`, `P5 bad=5` capture pins, `P8 bad=2` index rows) · `V3 DEFECT rows=9 bad=[S149…S157]` · `checks=11 defects=8` · **`PREDICATE C2 fail`** | 1 |

Envelope bracket of every run (last line of each, verbatim shape):
`ENVELOPE end HH:MM:SS exit=<rc> local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged`
Starts: M1/M2 `23:26:40`, M3/M4 `23:26:4x-23:27:0x`, M5/M6 `23:27:16`, M6b `23:27:28`, M7/M8 `23:28:21`, M8b `23:28:44`.

## What the baseline says for the landing measure

- **C1 before-state is exactly the frozen control**: `leaked=10`, `contradicted=10`, `PREDICATE C1 fail`, exit 1 on a
  *clean* clone of `b4fcd35` (M7) — matching `claims/control-c1-nothing.txt` line for line. So the round-45 C1 gain
  target (`contradicted=0`, `clean=10`, `admitted=104`) is measured against a reproducible zero-fence state.
- **C2 before-state on a clean tree is `defects=8`**, not 9: the frozen `claims/control-c2-nothing.txt` carries one extra
  defect (`P9 untracked=6`, attempt-1 leftovers) that cannot appear on a clean clone (M8b `P9 ok untracked=0`). A final
  measure printing `checks=11 defects=8` on a clean tree is therefore **not** progress unless the specific V/gate rows
  change; the landing predicate is `defects=0`.
- **C2 must be measured at the landing tip, not at the freeze commit**: the post-freeze re-pin (`52d7486`, 8 rows,
  `gitignore` rejected) hard-pins the spec digest, so the current counter on the freeze clone dies with
  `spec template not at its freeze digest` (M8, 8_of_11 DEFECT by ValueError). This is an instrument/clone mismatch, not a
  package defect — the claim's row list (S149–S156) matches the lane spec, and the freeze clone's spec still holds S157
  (`gitignore`). Recorded so nobody reads M8 as a C2 regression.
- **No-harm envelope holds**: ten measurement runs (nine receipt files; M6 and M6b share one), `~/.local/bin` content digest identical before/after in all of them; the lane
  worktree was only ever read by this seat (no lane file written, no git/jj command run there). `git status` in the lane
  does show live wave-1 sibling activity — `M plans/round45_c2_verify.py` (MECH_ROW regex + `under-varsea` DECISIVE lines)
  and many new `.ufo/waves/round-45/w1/*` files — none of it attributable to this seat. Consequence for the digest table
  above: the lane copy of `round45_c2_verify.py` was `8c3027…` when it was hashed (23:27, and that is the copy M8 ran) and
  `156a4242…` at 23:29 (sibling edit in flight); the C2 instrument is a moving target during wave 1, so a final measure
  must name the tip it used.
- **Regression floors for the final measure** (beyond the claim's own predicate): M3 `rows=141 tokens=47 defects=0`, M4
  `open=23 blocked=1 refused=2 routed_open=24`, M5 `ok` + 15 W04 advisories, M6b `ROUND-CLOSE RESULT PASS`, M1/M2 `pass`.

## Retained evidence

- `.ufo/waves/round-45/w1/R45NoHarmBaseline/measure-baseline.txt` — sha256 `028ed102…b84c1e`, 439 lines (summary + 9 runs).
- `.ufo/waves/round-45/w1/R45NoHarmBaseline/m1-c1.txt` (50 lines), `m2-c2.txt`, `m3-anchor.txt`, `m4-routed.txt`,
  `m5-census.txt`, `m6-roundclose.txt` (M6 + M6b), `m7-r45c1.txt` (12.5 KiB), `m8-r45c2.txt`, `m8b-r45c2-freeze.txt` — the
  largest is 40 KiB (`measure-baseline.txt`), each carrying its `ENVELOPE` line and the command's own exit code.

## Risks / notes

- `round_close.py` without `--census` exits 2 with `ROUND-CLOSE RESULT ERROR` on any lane that keeps the census script in
  the fleet root (`scripts/sources-census.sh`) rather than in-lane; only the `--census PATH` form is a meaningful green.
  Both forms are recorded so the final measure does not "fix" this by pointing `--census` at a different file.
- `round45_c2_verify.py` in the lane (`8c3027…`) and in the freeze commit (`804df7…`) differ; the frozen-digests file lists
  both `804d…` and `8c3027…`-era lines, so a digest check must state **which** pin it compares. No file was changed by me.
- M4's `--list` is a count only; `--observe` (it runs each row's check) was not executed — outside this measurement's
  assigned set and time-boxed by nothing but cost.
- No tool was installed or upgraded (no `pacman`, no `uv`, no PATH-dir write); nothing to record under the tooling directive.

## Scratch

`/fast/scratch/hyaku/kengaku-r45/R45NoHarmBaseline` (clone + `w`/`w45` work dirs + `env` cache overlay) — removed with
`plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r45 R45NoHarmBaseline "$S"` after this report was written.

VERDICT: baseline-recorded-lines-10
