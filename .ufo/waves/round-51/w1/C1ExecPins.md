# C1ExecPins — round 51, w1 executor (DIGEST pins + Core-row behavioural claims)

Seat: `C1ExecPins` (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Axis worked: **freshness** (R51-C1) — this seat re-derives the three digest pins that the two
PROVINCE surface tables state and re-runs the Core row's behavioural claims, so that C1's
`STALE` and `DRIFT` readings rest on an independent measurement rather than on the counter's
own probe.

Read first, in full: `plans/round-51-claims.md` (frozen stage-1 claims), then the C1 instrument
`plans/round51_surfaces.py` and its manifest `plans/round51-surfaces.json`.

## Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

Stage-1 freeze commit is `e07f131cf7037e58a21db6e1f3986cf401ad257c`; HEAD is one commit later
(`4090c3d`, the wave-spec commit). The three pinned files and `PROVINCE.md` are byte-identical
between freeze and HEAD (blob ids compared with `git rev-parse <rev>:<path>`):

```
SAME grader.py 4811bce1409c912ad4e326703bb542351955e6a4
SAME plans/attrib_probe.py 0510aa11b385d699d46422ffa57b668014dcaae6
SAME PROVINCE.md a1492cdd46c238b8991c3b9aa79939dd78d358dc
SAME plans/round51-surfaces.json 154ba1cfa0871e7b8c26fbe5118e87565a7bf7f6
```

`git diff --stat e07f131 4090c3d` touches only `.ufo/waves/round-51/{build_spec.py,
w1-dispatch.json,w1-spec.json}`. Working tree: no tracked modification (`git status --porcelain`
lists only untracked `.ufo/waves/round-50*`, `.ufo/waves/round-51*`), so the hashes below are the
committed contents. The shim is outside the repo (read-only external path).

## 1. Digest pins — full `sha256sum`, prefix and suffix compared

Command (lane cwd, absolute paths):

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
sha256sum grader.py plans/attrib_probe.py ~/.local/share/ds-flash-shim/shim.py
```

Verbatim output:

```
90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f  grader.py
489f938a198e08cf8c30efc3ca24ea5fac90ef3909d80aec0b1f62c90616e06b  plans/attrib_probe.py
42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386  /home/vgpnk/.local/share/ds-flash-shim/shim.py
```

| Pin (row text, `### Core`) | Asserted | Measured full digest | prefix | suffix | Verdict |
|---|---|---|---|---|---|
| `grader.py` (SF10, "In-repo verdict gate") | `90c87c88…ae941f` | `90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f` | MATCH | MATCH | **match** |
| `plans/attrib_probe.py` (SF12, "Attribution instrument + frozen tables") | `489f938a…16e06b` | `489f938a198e08cf8c30efc3ca24ea5fac90ef3909d80aec0b1f62c90616e06b` | MATCH | MATCH | **match** |
| `~/.local/share/ds-flash-shim/shim.py` (SF15, "ds-flash-shim source (read-only)") | `42d86d99…15a386` | `42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386` | MATCH | MATCH | **match** |

All three: no stale pin. Each asserted pin spans 14 of 64 hex characters (8 prefix + 6 suffix);
both ends were compared independently, not just the prefix.

Cross-check against the frozen C1 counter (`python3 plans/round51_surfaces.py --lane .`, run from
the lane at the same revision, supplementary to this seat's item):

```
PROBES run=19 present=13 absent=6 errors=0
STALE 0
PREDICATE R51-C1 fail
```

`STALE 0` agrees with the independent `sha256sum` reading: the counter's three `sha256` entries
(SF10, SF12, SF15) are all `state=present` and their pins are live today.

**Instrument limit worth recording (freshness-relevant).** `plans/round51_surfaces.py:102-110`
compares only the first 8 hex characters:

```python
h = hashlib.sha256(f.read_bytes()).hexdigest()
pin = p["pin"]
if not h.startswith(pin):
    return "absent", "digest %s does not start with pin %s" % (h[:8], pin)
```

while the rows assert a 14-character `prefix…suffix` composite (`90c87c88…ae941f` etc.). A file
whose first 8 hex characters still match but whose tail drifted would be reported `present` by the
counter although the row's stated pin is stale. Today this gap is not exercised — all three tails
match — but the counter's `STALE 0` does not by itself prove the rows' suffix half, which is why
this seat compared the full digests. Not a defect in the frozen predicate (the manifest records the
prefix pin as the spec), a declared coverage limit of the instrument.

## 2. Core-row behavioural claims

All three run from the lane cwd at `REV 4090c3d`. Exit codes captured from the shell (`EXIT=$?`
immediately after the redirect), first and last line quoted verbatim.

### 2a. `python3 grader.py --selftest`

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 grader.py --selftest
```

- exit: **0** (claimed: exits 0 — met)
- first line: `[selftest] PASS S0 control (clean copies): exit 0, expected 0`
- last line: `[selftest] ALL PASS`
- 9 lines total; it does print S0–S7:

```
[selftest] PASS S0 control (clean copies): exit 0, expected 0
[selftest] PASS S1 stored-ok flip (record layer): exit 1, expected 1 + check-id r8.replay.A-INC.ok (flip applied: True, id fired: True)
[selftest] PASS S2 run.log SUMMARY edit (summary layer): exit 1, expected 1 + check-id r8.summary.A-INC (id fired: True)
[selftest] PASS S3 raw-digit bump (re-parse layer): exit 1, expected 1 + check-id r9.replay.A-MONO.got (mutation applied: True, id fired: True)
[selftest] PASS S4 r11 stored-ok flip (record layer): exit 1, expected 1 + check-id r11.replay.A-CKPT4710.ok (flip applied: True, id fired: True)
[selftest] PASS S5 r11 run.log SUMMARY edit (summary layer): exit 1, expected 1 + check-id r11.summary.A-CKPT4710 (id fired: True)
[selftest] PASS S6 stats anchors (betai/t_crit known values): all known-value assertions hold
[selftest] PASS S7 r12 stats anchors (Page L / grade_seq / Brier-BSS / Newton): all known-value assertions hold
[selftest] ALL PASS
```

Distinct stage tokens present: `S0 S1 S2 S3 S4 S5 S6 S7` (verified by
`grep -oE 'S[0-7]' | sort -u`). Every stage prints `PASS`; no `FAIL` line.

### 2b. `python3 plans/attrib_calibration.py --selftest`

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/attrib_calibration.py --selftest
```

- exit: **0** (the Core row "Interval re-verdict instrument (round 25)" claims `--summary` / `--selftest` = exit 0 / exit 0; the `--selftest` half is met)
- first line: `selftest ok   A1: 126 known-value anchors (closed forms, SciPy 7/50, power ask, Wilson)`
- last line: `selftest: 18 checks, 0 failed`

### 2c. `python3 plans/state_check.py --selftest`

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/state_check.py --selftest
```

- exit: **0** (the Core row "State-assertion check (round 25)" claims exit 0 on the landed tree; met)
- first line: `selftest ok   P2/P3 supersession range: R27 and R29 accepted`
- last line: `[selftest] ALL PASS (canonical seed, pointers, out-of-population box, pointer-only, R25–R29-E exact-token supersession, P2/P3 R27/R29 corrections, P4 R27-only supersession, P2e/P3c OUT_OF_POPULATION retention, P3a–P3e and P4a–P4e red mutations)`

## Summary table

| Claim (Core row) | Expected | Observed | Verdict |
|---|---|---|---|
| `grader.py` digest `90c87c88…ae941f` | present, pin live | full digest matches both ends | match |
| `plans/attrib_probe.py` digest `489f938a…16e06b` | present, pin live | full digest matches both ends | match |
| `~/.local/share/ds-flash-shim/shim.py` digest `42d86d99…15a386` | present, pin live | full digest matches both ends | match |
| `grader.py --selftest` prints S0–S7, exit 0 | exit 0 | exit 0, 8 stages S0–S7 all PASS, `ALL PASS` | met |
| `attrib_calibration.py --selftest` | exit 0 | exit 0, `18 checks, 0 failed` | met |
| `state_check.py --selftest` | exit 0 | exit 0, `ALL PASS` | met |

## Limits

- Point-in-time measurement at `REV 4090c3d` (freeze content for every file cited). `attrib_probe.py`
  is documented in its own row to float between trials and landing; a later revision must re-hash.
- The shim is an external read-only host path (`~/.local/share/ds-flash-shim/`); it is not under
  version control and can change without any lane commit. This seat only read its bytes.
- Only `--selftest` was run for `attrib_calibration.py` and `state_check.py`; the rows' `--summary`
  halves were not in this item and are not measured here.
- The counter's `sha256` probe compares an 8-character prefix only (see §1); the suffix halves
  reported here come from this seat's own `sha256sum` comparison, not from the counter.
- No production file was edited; this seat wrote only this report. Scratch
  `/fast/scratch/hyaku/kengaku-r51/C1ExecPins` was created for this run and removed before yield
  (no fixture git repo was needed — no mutating git call was made anywhere).
- Tooling: nothing installed or upgraded (no tool was needed beyond coreutils/python3 already on
  the host); PACMAN guard respected — no pacman transaction was run.

VERDICT: PASS — all three PROVINCE digest pins (`grader.py` `90c87c88…ae941f`, `plans/attrib_probe.py`
`489f938a…16e06b`, `~/.local/share/ds-flash-shim/shim.py` `42d86d99…15a386`) re-derive to their full
64-hex digests with both prefix and suffix matching (no stale pin), and all three Core-row
behavioural claims hold at `REV 4090c3d`: `grader.py --selftest` prints S0–S7 and exits 0,
`attrib_calibration.py --selftest` exits 0, `state_check.py --selftest` exits 0. Recorded limit:
the C1 counter checks only the 8-character pin prefix, so its `STALE 0` does not cover the rows'
suffix half — today moot, since every suffix also matches.
