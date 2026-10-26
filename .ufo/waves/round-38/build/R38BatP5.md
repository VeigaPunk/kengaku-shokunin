# R38BatP5 — battery38 module for frozen mutants N07, N08 (P5 capture manifest)

Seat: executor, kengaku round 38 wave 1. Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(read only for this seat). No lane file was edited; the module lives only under this build dir.

Axes named up front:
- **Calibration** — do two frozen advertised P5 behaviours move from survived to attributably killed?
- **Attribution/isolation** — is each kill tied to the mutant's own clause and direction, with `defects`
  equal to the exact DEFECT set the unmodified gate prints?
- **Operability** — stdlib only, one module, fids unique (`p5m-`), no forbidden side-channel token,
  load-bearing proven by deletion.

## 1. The two mutants (frozen, `plans/round38_c1_verify.py`)

```
N07 P5 silence  'for sid, row in p.spec["rows"].items():' -> '... list(...)[:1]:'
                "every registry row's capture is pinned in the manifest, not only the first [F37XMutP5 X1]"
N08 P5 mirror   'if not line.strip():\n continue\n m = MANIFEST_LINE' -> 'if False:\n continue\n m = MANIFEST_LINE'
                "a blank manifest line is tolerated, not an unparsed line [Q24 genuine accepted; R37PlanNext B2]"
```

Gate branches (`plans/pkg_gate.py`, digest `ea638822…`):

- `plans/pkg_gate.py:159-163` — `if not line.strip(): continue` then `MANIFEST_LINE.match(line.strip())`
  else `bad.append(f"unparsed manifest line …")`. N08 disables the blank-line skip, so a blank line
  becomes an unparsed line → P5 `DEFECT` (mirror direction: needs an accept-side fixture).
- `plans/pkg_gate.py:169-174` — `for sid, row in p.spec["rows"].items():` … `elif pinned[name] !=
  row["sha256"]: bad.append(f"{sid}: manifest digest differs from the spec pin")`. N07 restricts this
  loop to the first row, so a defect on a later row is silenced.

## 2. Module

`battery/p5m.py` (copy to `plans/battery38/p5m.py` at integration; stdlib `hashlib`, `re` only):

| fid | expect | declared defects | build |
|---|---|---|---|
| `p5m-row-off-pin-later-row` | reject | `["P5"]` | genuine package; take `list(ctx.spec["rows"])[-1]` (S107, **not** the first row), append one line to its capture, rewrite that row's manifest line to the new bytes' digest (`<sha>  instruction.md`), `ctx.git_add`. One P5 branch fires: `S107: manifest digest differs from the spec pin`. |
| `p5m-manifest-blank-line` | accept | `[]` | genuine package; append one blank line to `<capture_dir>/SHA256SUMS` (`text.rstrip("\n") + "\n\n"`), `ctx.git_add`. Unmodified gate skips it → P5 `ok`, exit 0. |

Why each fixture isolates one P5 branch (P5 accumulates into one `bad` list, `plans/pkg_gate.py:157-182`):

- N07: the appended line lands after every line the entry quotes (all round-35 quote rows cite
  `test_outputs.py:13-28`; the row used is `instruction.md`), so P4 is silent; the manifest digest is
  moved *with* the bytes, so the bytes-match branch (`:167`) is silent; no file is added or removed, so the
  not-covered sweep (`:178-181`) is silent. Verified: `bad=1 first=S107: manifest digest differs from the
  spec pin` (§4).
- N08: no other clause reads `SHA256SUMS`; the manifest content is otherwise byte-identical to the accept
  case, so the reference accepts (rc 0) and P5 is the only clause that can move.

## 3. Command and output (development run, clean clone)

```
S=/fast/scratch/hyaku/kengaku-r38/R38BatP5; export TMPDIR="$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel            -> /fast/scratch/hyaku/kengaku-r38/R38BatP5/lane
sha256sum "$S/lane/plans/pkg_gate.py"                 -> ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41
python3 plans/round38_c1_verify.py --lane "$S/lane" \
  --battery-dir .ufo/waves/round-38/build/R38BatP5/battery --only N07,N08 --work "$S/w"
```

Output (full receipt `R38BatP5/run-n07-n08.txt`, exit 0; a second run with `--work "$S/w2"` is
byte-identical, `sha256 d25441ab…8f10` for both receipts):

```
PINS total=14 mismatched=0
FIXTURE p5m-row-off-pin-later-row expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5m-manifest-blank-line expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N07 P5 silence killed by=p5m-row-off-pin-later-row -- every registry row's capture is pinned in the manifest, not only the first [F37XMutP5 X1]
MUTANT N08 P5 mirror killed by=p5m-manifest-blank-line -- a blank manifest line is tolerated, not an unparsed line [Q24 genuine accepted; R37PlanNext B2]
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

`fixtures=66` = 64 frozen (14 r36 + 50 battery37) + this module's 2; `wrong=0` means both declared
DEFECT sets equal the reference's exact DEFECT set, and the accept fixture's reference DEFECT set is empty.
`renamed_disagree=0`: both fixtures are path-independent (no absolute path is baked into any file the gate
reads). `sidechannel=0`: `grep -nE '/proc|ppid|cmdline|psutil|environ' battery/p5m.py` → no hit (rc 1).

## 4. Detail lines — the attributed branch, under each mutant

Command: `python3 "$S/probe.py" "$S/lane" .ufo/waves/round-38/build/R38BatP5/battery "$S/pw"`
(receipt `R38BatP5/p5-detail-lines.txt`; the probe runs ref, N07 and N08 copies of the gate over the same
built fixture and prints the gate's own `P5 …` line):

```
p5m-row-off-pin-later-row        ref rc=1 P5 DEFECT manifest_entries=6 bad=1 first=S107: manifest digest differs from the spec pin
p5m-row-off-pin-later-row        N07 rc=0 P5 ok manifest_entries=6 bad=0 first=0
p5m-row-off-pin-later-row        N08 rc=1 P5 DEFECT manifest_entries=6 bad=1 first=S107: manifest digest differs from the spec pin

p5m-manifest-blank-line          ref rc=0 P5 ok manifest_entries=6 bad=0 first=0
p5m-manifest-blank-line          N07 rc=0 P5 ok manifest_entries=6 bad=0 first=0
p5m-manifest-blank-line          N08 rc=1 P5 DEFECT manifest_entries=6 bad=1 first=unparsed manifest line ''
```

So the N07 kill is exactly "a row that is not the first is off its pin" (S107, the spec's last row by
dict order; the r35 mapping is S105, S106, S107), and the N08 kill is exactly "a blank line became an
unparsed manifest line".

## 5. Load-bearing table (delete one fixture, its mutant survives)

Variant modules in scratch keep exactly one fixture (each is the same module with the other fid filtered
out). Command: the same counter, `--only N07` with the blank-line module and `--only N08` with the row
module. Receipt `R38BatP5/load-bearing.txt`:

```
== N07 with p5m-row-off-pin-later-row dropped (module keeps p5m-manifest-blank-line) ==
FIXTURE p5m-manifest-blank-line expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N07 P5 silence SURVIVED -- every registry row's capture is pinned in the manifest, not only the first [F37XMutP5 X1]
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
== N08 with p5m-manifest-blank-line dropped (module keeps p5m-row-off-pin-later-row) ==
FIXTURE p5m-row-off-pin-later-row expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N08 P5 mirror SURVIVED -- a blank manifest line is tolerated, not an unparsed line [Q24 genuine accepted; R37PlanNext B2]
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
```

Each mutant has exactly one killer (the other fixture does not kill it), so neither kill is an accident of
the other fixture's clause set.

## 6. Artifacts and digests

```
db9627e8cf3834202057e575416dc454c6c42b9ec9d136bf287ceadb7940803b  R38BatP5/battery/p5m.py   (3666 bytes)
d25441ab14b6951acdfacb3993bcaa6d6a012c556b1c60404d962ce343718f10  R38BatP5/run-n07-n08.txt
d25441ab14b6951acdfacb3993bcaa6d6a012c556b1c60404d962ce343718f10  R38BatP5/run-n07-n08-repeat.txt
9a2257342803d1dfc484525ca2ae6bfd9b3a785a6644a4c862163379d3f090d6  R38BatP5/p5-detail-lines.txt
c27a5cb9dbee3d6dfae8d0edfc6022efd954e8721875d672efbb3a3a54e96a02  R38BatP5/load-bearing.txt
```

Module sha256 (the number C1 pins indirectly through review, and the one to re-check after any copy):
**`db9627e8cf3834202057e575416dc454c6c42b9ec9d136bf287ceadb7940803b`**.

## 7. Limits and risks (named, not repaired)

- **N07 is killed at the dict-tail row only.** The fixture proves the loop is not first-row-only; it does
  not prove every row is checked (a `[:2]` mutant would survive this module — the r35 spec has 3 rows).
  Adding a middle-row fixture would close that, but the frozen mutant is `[:1]`, so one fixture is
  sufficient for the predicate.
- **N07's fixture depends on the r35 row order** (`list(ctx.spec["rows"])[-1]` = `S107`). If the spec were
  replaced by one with a single row the builder raises (`RuntimeError`), never silently building a first-row
  fixture that could not kill N07.
- **N08 requires the accept side**, so the fixture is only load-bearing while the genuine package passes
  P5 at reference (it does: P0 path, rc 0). If a future pin changes the capture bytes it fails loudly as
  `WRONG`, not silently.
- **Attribution is clause-level, not reason-level** (the round-37 counter's known limit): both fixtures are
  single-defect at branch level (`bad=1` on the reject fixture, `bad=0` accept), so the clause move is the
  reason move here.
- No pacman/pip/npx installs were made (python3 stdlib only); no host service restarted; nothing written
  outside `R38BatP5/` in this build dir and `/fast/scratch/hyaku/kengaku-r38/R38BatP5` (deleted).
- Integration is L1's: copy `R38BatP5/battery/p5m.py` → `plans/battery38/p5m.py` (no `__pycache__`; the
  build dir's copy is removed). The `battery/` dir holds exactly one module, per the seat rule.

VERDICT: battery38-p5m-killed-2/2-wrong-0
