# R43BatAncRow — battery43 module killing frozen mutant NA1 (round 43, wave 1)

Seat: executor `R43BatAncRow`. Lane repo under test: a `git clone -q --shared` of
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` at `/fast/scratch/hyaku/kengaku-r43/R43BatAncRow/lane`
(`git -C "$S/lane" rev-parse --show-toplevel` printed that path). No lane file was edited; the frozen files named in
`plans/round-43-claims.md` are read only (`PINS total=2 mismatched=0` and `PINS-AFTER mismatched=0` in every run
below). No package was installed; no `pacman` call was made; nothing was written to a PATH directory.

## 1. Deliverable

**New file:** `.ufo/waves/round-43/build/R43BatAncRow/battery/a_row.py`
(sha256 `b140efcf3f9088b471453cf731be0d4e57c12207efc42d2c510a998c3e8c421b`, 4725 B, stdlib only, every fid starts
`a_row-`). The L1 copies it to `kengaku-shokunin/plans/battery43/a_row.py`.

Target mutant (read from `plans/round43_c1_verify.py:215-219`): `NA1`, tool `anchor`, class `row-malformed`,
direction `silence`, `direct`, advertisement `plans/anchor_digest_check.py:34-35`, replacement
`        if len(r["cells"]) != NCELLS:` → `        if len(r["cells"]) < NCELLS:` — the over-long side of the row
length test. Suite `defects` for the anchor tool are the `class=<C>` tokens of its `DEFECT ` lines
(`round43_c1_verify.py:424-433`); a `silence` kill needs the class printed by the reference, absent from the mutant,
both exits in 0/1 (`exhibits`, `:728-734`).

Contract implemented exactly as the counter docstring states: module-level `FIXTURES` of
`{fid, tool, expect, defects, build}`; `build(ctx, d)` fills the empty `d`, builds every repo from nothing with
`ctx.init`/`ctx.write`/`ctx.git`, and returns `["--lane", <repo inside d>]`. Each fixture commits
`corpus/SOURCES.md` and at least one capture under `corpus/evidence/` (the tool refuses an empty evidence tree,
`anchor_digest_check.py:241-243`).

## 2. Fixtures and what each demonstrates

| fid | shape | cells | expect | declared defects | comment in module |
|---|---|---|---|---|---|
| `a_row-na1-tail12` | four-row registry (three green rows + one malformed), duplicate `used-by` cell on the LAST row | 12 | reject | `row-malformed` | "A duplicate used-by cell at the END of a four-row registry (12 cells)" |
| `a_row-na1-mid13` | eight-row registry, malformed row in the MIDDLE with a repeated tier and a repeated status cell | 13 | reject | `row-malformed` | "Two duplicated mid-table fields in an eight-row registry (13 cells)" |
| `a_row-na1-wide20` | one row pasted from a wider table, nine extra token-free cells, anchor cell already CORRECT for its capture | 20 | reject | `row-malformed` | "A row pasted from a wider table (20 cells) whose anchor is CORRECT" |

Green rows carry an explicit `corpus/evidence/...` locator (route 3, `anchor_digest_check.py:288-299`) and a
`sha256 <digest>` equal to the committed capture's digest, so the only defect on each fixture is the malformed row.
`a_row-na1-wide20` is the strong shape: under the reference the row is refused before its token is read
(`:477-481`), under NA1 it is not malformed, its token resolves, and the tool exits 0 — a silent acceptance of a
claim that only an over-long row hid.

## 3. Measured evidence

### 3.1 NA1-only run (required)

Command (wrapped in the round-43 envelope):

```
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/claims/envelope.sh "$S/env" \
  python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round43_c1_verify.py \
  --lane "$S/lane" \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/build/R43BatAncRow/battery \
  --only NA1 --work "$S/w"
```

Output (`.ufo/waves/round-43/build/R43BatAncRow/na1-run1.txt`):

```
ENVELOPE start 19:08:14 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE a_row-na1-tail12 tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
FIXTURE a_row-na1-mid13 tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
FIXTURE a_row-na1-wide20 tool=anchor expect=reject declared=row-malformed observed_rc=1 observed=row-malformed ok
MUTANT NA1 anchor silence killed by=a_row-na1-tail12 attributed=L477 value=differs hits=3 -- plans/anchor_digest_check.py:34-35 'A row that matches the census regex but does not have
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/1 order=0/0
ADVERTISED direct=1 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 19:08:16 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`attributed=L477` is the replaced line (`anchor_digest_check.py:477`); `value=differs` is leg g, the site record
(next event: the `defects.append` branch for the reference versus falling through to `exempt` for the mutant);
`hits=3` records that all three fixtures exhibit the direction.

### 3.2 Load-bearing table (each fixture removed, then each fixture alone)

Six subset runs, each in its own envelope, from scratch copies of the module under `$S/bat/<name>/a_row.py`
(`.ufo/waves/round-43/build/R43BatAncRow/load-table.txt`):

| subset | fixtures | NA1 result |
|---|---|---|
| only `a_row-na1-tail12` | 1 | `killed by=a_row-na1-tail12 attributed=L477 value=differs hits=1` |
| only `a_row-na1-mid13` | 1 | `killed by=a_row-na1-mid13 attributed=L477 value=differs hits=1` |
| only `a_row-na1-wide20` | 1 | `killed by=a_row-na1-wide20 attributed=L477 value=differs hits=1` |
| drop `tail12` | 2 | `killed by=a_row-na1-mid13 … hits=2` |
| drop `mid13` | 2 | `killed by=a_row-na1-tail12 … hits=2` |
| drop `wide20` | 2 | `killed by=a_row-na1-tail12 … hits=2` |

Every subset printed `wrong=0 tampered=0 sidechannel=0`, `killed=1 survived=0 invalid=0 unattributed=0`, and envelope
`local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` (19:08:42, 19:08:45, 19:08:49,
19:08:52, 19:08:56, 19:08:59). **No single removal flips NA1**: the three fixtures are independently sufficient, not
one demonstration split three ways. That redundancy is the honest result of the table, not a load-bearing claim.

### 3.3 Full default counter with the module in the clone

`cp …/battery/a_row.py "$S/lane/plans/battery43/a_row.py"` (sha256 again
`b140efcf3f9088b471453cf731be0d4e57c12207efc42d2c510a998c3e8c421b`), then

```
envelope.sh "$S/env" python3 …/plans/round43_c1_verify.py --lane "$S/lane" --work "$S/w2"
```

Output (`.ufo/waves/round-43/build/R43BatAncRow/full-run.txt`):

```
ENVELOPE start 19:09:07 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE a_row-na1-tail12 … ok ; a_row-na1-mid13 … ok ; a_row-na1-wide20 … ok
MUTANT NA1 anchor silence killed by=a_row-na1-tail12 attributed=L477 value=differs hits=3 -- …
MUTANT NA5 … SURVIVED exhibits=none
MUTANT NA7 … SURVIVED exhibits=none
MUTANT NA18 … SURVIVED exhibits=none
MUTANT NA20 … SURVIVED exhibits=none
MUTANT NA21 … SURVIVED exhibits=none
MUTANT NO5 order rc-silence SURVIVED exhibits=none
MUTANT NO7 order rc-mirror SURVIVED exhibits=none
MUTANT NO22 order rc-silence SURVIVED exhibits=none
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=9 killed=1 survived=8 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/6 order=0/3
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 19:09:09 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

The eight survivors are the other seats' mutants (five anchor, three order); `PREDICATE C1 fail` is the expected
state of a single-seat wave, not a defect of this module.

## 4. Non-duplication and hygiene

- `claims/witness/w_near.py` was read only to learn its shapes; the module does not import, copy or read it, and no
  fixture construction is shared: no `round42/w2` path, no erratum, no slashed-`task.toml` URL, no order fixture,
  no `extra="extra"` cell. Shapes here are multi-row registries with the malformed row at three different positions
  (last, middle, only) and widths 12/13/20, which the witness's single 12-cell row does not cover.
- Counter token scan: `sidechannel=0` on every run; the module text was also scanned locally against the counter's
  token tuple after removing the one hit (`witness` in a docstring, now "freeze probe module").
- No `git add`/`commit` in the lane; commits happen only inside the fixtures through `ctx.git` (fixed identity and
  date from `Ctx.ENV`). Nothing was written to `/home/vgpnk/Projects/shokunin` outside this seat's build directory.
- No build, lint, test or formatter run was performed on the lane; the only executions are the counter runs above.

## 5. Limits named

1. Scope: this seat covers NA1 only. NA5, NA7, NA18, NA20, NA21, NO5, NO7, NO22 remain unwitnessed here by design.
2. A kill is a result difference in the declared direction on a fixture that executes line 477 and changes its site
   record; it is not proof that the fixture's intent is broad. Three independent widths/positions is a sample of the
   over-long side (12/13/20, tail/middle/single), not an exhaustive one.
3. Leg-g value attribution compares next events and locals digests; a mutant whose only effect were attribute state
   invisible to `repr` would read `unattributed` (a false negative). Here the difference is control flow (defect
   branch versus fall-through), so it is visible.
4. The token scan is a heuristic and the counter cannot see intent; non-author review of this module stays required
   by the claims file.
5. All runs used the host `/usr/bin/python3` and nested `bwrap` inside the round-43 envelope; no image, no uvx, no
   network.

VERDICT: battery43-a_row-killed-1/1-wrong-0
