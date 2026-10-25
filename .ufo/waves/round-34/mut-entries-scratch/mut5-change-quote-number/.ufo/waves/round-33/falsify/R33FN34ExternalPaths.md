# R33FN34ExternalPaths — N3/N4 lane-argument hermeticity falsification

- **Seat:** `KengakuR33.R33FN34ExternalPaths` (Falsify wave, round 33, hyaku run 7)
- **Target claim:** C2 (round-33-claims.md lines 83–101) — `python3 plans/round33_defects.py --lane .` prints `checks=6 defects=6` on the pre-repair tree and `checks=6 defects=0` on the repaired tree, where N3 reads `.ufo/reports/round-31/kengaku.md` and N4 reads `.ufo/reports/round-32/kengaku.md` **as lane inputs**.
- **Verdict:** **CAUGHT / claim false as stated.** The lane argument does **not** control the N3/N4 report inputs. `check_n3`/`check_n4` read absolute fleet paths (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-{31,32}/kengaku.md`) regardless of `--lane`; the lane parameter is unused in both functions. The counter therefore cannot reproduce its own frozen `defects=6` control on an archived/repaired-anywhere lane — it now prints `defects=4` unless the fleet-side bytes are also pinned. N3/N4 are green on any lane (including a nonexistent one) whenever the live fleet reports are repaired. Body of B6 in R33CounterAttack.md confirmed and completed by independent reproduction.

## Evidence

### 1. Static: `lane` is never read by N3/N4

AST scan of `plans/round33_defects.py`:

```
check_n3 args=['lane', 'r31_report'] lane-loads=[] lineno=100
check_n4 args=['lane', 'r32_report'] lane-loads=[] lineno=114
```

The `lane` parameter is loaded zero times in either body. Module constants:

```python
FLEET = Path("/home/vgpnk/Projects/shokunin")
R31_REPORT = FLEET / ".ufo/reports/round-31/kengaku.md"
R32_REPORT = FLEET / ".ufo/reports/round-32/kengaku.md"
```

and the default:

```python
def check_n3(lane: Path, r31_report: Path | None = None) -> str:
    r31_report = r31_report or R31_REPORT
```

`main()` calls `check(lane)` with the single positional form, so the optional override parameter is unreachable from the CLI — `--lane` cannot flow into the report path.

### 2. Empirical: `--lane` does not control N3/N4 inputs

Fresh sandbox `/tmp/r33-fn34` (lane copies built by `cp -a` from the live lane working tree — no fleet/lane bytes modified; all git operations scoped to `/tmp`).

| Run | Lane | Fleet bytes in play | N3 | N4 | total |
|---|---|---|---|---|---|
| A | `lane-a` (mirror of live repaired lane, git-committed) | live repaired (`3d3ca566`) | green | green | `checks=6 defects=0` exit 0 |
| B | `lane-b` (same, but lane-local `.ufo/reports/round-31/kengaku.md` **poisoned**: only `a44b5a8`, no erratum/`ae95fe0`; round-32 lane-local report names `bcd2a6c`, no `112091c`) | live repaired | green | green | `checks=6 defects=0` exit 0 |
| C | `lane-c` (lane-local reports crafted to pass: erratum + `ae95fe0`, `112091c`) | live repaired | green | green | `checks=6 defects=0` exit 0 |
| D | `no-such-lane` — **directory does not exist** | live repaired | green | green | `checks=6 defects=4` exit 1 (only N1/N2/N5/N6 red) |

Run D is the sharpest proof: N3/N4 report green even when the lane itself does not exist. Lane-local report bytes (B vs C) produce byte-identical output — the lane never influences N3/N4.

### 3. The binding is the fleet path, not the lane

Same lane, different fleet state (module constants repointed in-process via `run_fleet.py` — exact `main()` codepath):

```
K1 lane-a + pre-repair fleet bytes (r31-pre.md / r32-pre.md, from /tmp/r33-counterattack receipts):
  DEFECT N3 round31-report-phantom-hash: no appended erratum supersedes the a44b5a8 citation
  DEFECT N4 round32-report-closure-tip: the round-32 report does not name the round-32 closure tip 112091c
  checks=6 defects=2
K2 lane-a + live repaired fleet (default main): checks=6 defects=0
```

Same lane, two results — the only input that changed is the **fleet** file. And the reverse (E1–E3): with fleet pinned to pre-repair bytes, `lane-a`, poisoned `lane-b`, and a nonexistent lane all print the identical N3/N4 reason strings. E4 shows the fail-closed path also names the absolute fleet path:

```
DEFECT N3 round31-report-phantom-hash: /tmp/r33-fn34/fleet-missing/.ufo/reports/round-31/kengaku.md is unreadable: …
```

### 4. Frozen control `defects=6` is not reproducible on an archived lane

`lane-d` = pre-repair-shaped lane (untracked wave tree for N1, no `## Round 32` for N2, stale lesson bytes for N5/N6), run with **live repaired fleet**:

```
DEFECT N1 … 89 untracked files remain …
DEFECT N2 … SCORECARD.md carries no '## Round 32' section …
DEFECT N5 … no appended correction … :39-40
DEFECT N6 … no appended correction … :72 / :82-83
checks=6 defects=4   exit=1
```

This reproduces exactly the R33CounterAttack §2 delta (4 defects, not the frozen 6). Only when the fleet bytes are also pinned to the pre-erratum state does the same lane print `defects=6` (run G). So the frozen `defects=6` receipt is a joint property of lane *and* fleet state; the CLI exposes no way to pin fleet state, and `--lane` alone cannot restore it.

### 5. The only override is the Python API, and it is unreachable from the CLI

```
direct check_n3(lane, repaired_fleet)       -> '' (green)
direct check_n3(lane, pre_repair_fleet)     -> 'no appended erratum supersedes the a44b5a8 citation'
direct check_n4(lane, pre_repair_fleet)     -> 'the round-32 report does not name the round-32 closure tip 112091c'
```

The optional parameter works when passed directly; `main()` never passes it. The selftest itself documents the coupling (round33_defects.py:183–185): *"N3/N4 read absolute fleet paths by default, which would couple the selftest to the live repair state"* — it dodges the problem by injecting fixtures; the production CLI has no such injection.

## Consequence for C2

- `--lane .` on the repaired lane prints `defects=0` **only because the live fleet reports were already repaired** by fleet commit `3d3ca566`. A mirror/archive of the lane cannot reproduce the frozen pre-repair `defects=6` from its own bytes.
- N3/N4 are therefore not lane-hermetic inputs: they are live fleet reads. The counter's "repaired tree" result is contingent on fleet state that is outside the lane's bytes, so the C2 counting command certifies fleet erratum presence, not the lane's repair.
- Kill-rule check: a lane that *does* contain all six repairs but whose fleet reports are unrepaired will print `defects=2` (N3/N4 red) — a false negative for lane satisfaction — while a lane with the N3/N4 lane-local content poisoned/present prints identical output. The lane argument is misleading for exactly these two items.

## Blind-spot boundary

This falsification covers the **input-path binding** (B6). The related N3 weaknesses (width 300 vs frozen 400, `near()` newline blindness, file-wide `ae95fe0` substring) are E3b/E3c/E3 in R33CounterAttack and are separate items. This report does not touch N1/N2/N5/N6 semantics.

## Receipts / reproduction commands

- Sandbox: `/tmp/r33-fn34/` — lane-a/b/c/d, `fleet-pre/` (real pre-erratum bytes copied from `/tmp/r33-counterattack/r31-pre.md`, `r32-pre.md` — 20998 B / 6231 B), `fleet-missing/`, `run_fleet.py` (repoints module `R31_REPORT`/`R32_REPORT` then executes real `main()`).
- Key commands (all in `/tmp` sandbox; no fleet/lane bytes touched):

```
(cd /tmp/r33-fn34/lane-a && python3 plans/round33_defects.py --lane .)          # checks=6 defects=0
python3 /tmp/r33-fn34/run_fleet.py /tmp/r33-fn34/lane-a \
  /tmp/r33-fn34/fleet-pre/.ufo/reports/round-31/kengaku.md \
  /tmp/r33-fn34/fleet-pre/.ufo/reports/round-32/kengaku.md \
  /tmp/r33-fn34/lane-a/plans                                                  # checks=6 defects=2
(cd /tmp/r33-fn34/lane-d && python3 plans/round33_defects.py --lane .)          # checks=6 defects=4
python3 /tmp/r33-fn34/lane-a/plans/round33_defects.py --lane /tmp/r33-fn34/no-such-lane  # N3/N4 green in defects=4
```

- No tools installed; no production files written; the only lane-tree write is this report.

## Verdict

**Falsified.** "`--lane` controls the N3/N4 report inputs" is false: absolute fleet paths override `--lane` unconditionally, the lane parameter is unused in both checks, and the frozen 6/6 control is unreproducible from any lane copy alone. N3/N4 are live fleet reads; the C2 counter cannot be hermetic under `--lane` as frozen.
