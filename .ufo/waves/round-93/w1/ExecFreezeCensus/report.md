# ExecFreezeCensus — freeze-integrity census of rounds 85–91 (report-only, no claim leg)

Seat: ExecFreezeCensus, kengaku round 93, 2026-11-05. Lane `kengaku-shokunin`, BASE
`28e9f8bf…`, tip T `22972a317185216596b3dfe1c189e98d1eb86787`.

Gate: `plans/round93_freeze_integrity.py` in **paths mode**, run from a scratch clone
(`git clone --shared`, detached at T; the lane itself was never mutated). The gate bytes used
hash to `18b01b42fb54ce658dbb98ff3afd12d06600960fae46700fec9218e73bcefcb6`, the value the
round-93 frozen-instruments table pins — the census runs the frozen instrument, not a
working-tree variant. Twelve invocations (7 census + 5 sensitivity), every one printing
`SELFTEST cases=10 ok=10`. Scratch receipts copied to `receipts/` here.

Command shape per round (exact, with `$L` = the scratch clone):

```
python3 plans/round93_freeze_integrity.py --lane "$L" --freeze <F> --rev <TIP> \
    --paths plans/round<N>_*.py plans/round<N>-cases.json --work "$S/w-<N>"
```

## Census (rc 1 = at least one broken row; rc 0 = all intact; battery green in all rows)

| round | freeze | tip | instruments | intact | broken | rc |
|---|---|---|---|---|---|---|
| 85 | `99a7cb3b` (instrument first landing) | `88651a72` (MANIFEST closure) | 4 | 1 | 3 | 1 |
| 86 | `61b0e074` (the round's claims freeze) | `276abd46` (LOG "receipt and tip measurement") | 4 | 2 | 2 | 1 |
| 87 | `21da383b` (instrument landing) | `10de494d` (LOG "receipt and measured tip") | 5 | 5 | 0 | 0 |
| 88 | `1f267d4b` (instrument landing) | `7fcc680b` (LOG "receipt and measured tip") | 4 | 4 | 0 | 0 |
| 89 | `0e6bb05f` (instrument landing) | `00462b59` (LOG attempt-2 measured tip) | 4 | 3 | 1 | 1 |
| 90 | `664435cf` (LOG commit B, instruments) | `9cf98d90` (LOG "measured tip for all counters") | 5 | 5 | 0 | 0 |
| 91 | `386184a6` (LOG commit B, instruments) | `cefabd44` (LOG tip D, triage) | 6 | 5 | 1 | 1 |

Broken rows (bytes-facts, from the gate's INSTRUMENT lines; see `receipts/w-<N>.txt`):

- **85**: `round85_c1_replay.py` touched=5 rev-bytes-differ; `round85_c2_debt.py` touched=4
  rev-bytes-differ; `round85_sqlite_truncate_probe.py` touched=1 rev-bytes-differ;
  `round85-cases.json` intact.
- **86**: `round86_c1_replay.py` touched=3 rev-bytes-differ; `round86_c2_repin.py` touched=2
  rev-bytes-differ; `round86_raman_probe.py` and `round86-cases.json` intact.
- **89**: `round89_claim_figures.py` touched=1 rev-bytes-differ; other three intact.
- **91**: `round91_counter_pin.py` touched=1 rev-bytes-differ; other five intact.

The gate's own semantics: `touched` counts commits in `freeze..tip` touching the path
(`rev-list`), an edit-then-revert still counts, and `rev-bytes-differ` means the tip bytes are
not the freeze bytes. **A broken row is a fact about bytes, not a verdict about the round.**

## Assumptions (each named, each with a sensitivity receipt where it could matter)

1. **Paths mode for all seven rounds.** Grep over `plans/round-8[5-9]-claims.md`,
   `round-9[01]-claims.md` at T: only `plans/round-93-claims.md` carries a
   ``` ```frozen-instruments``` ``` table; the legacy claims files have none, so the gate's
   paths mode (freeze the named paths' bytes at the freeze) is the only applicable mode.
2. **Freeze = the round's own claims-freeze commit when the instruments already exist there;
   otherwise the instrument first-landing commit.** Rounds 87–91 freeze the claims file and
   case table at "commit A … before any instrument" (each claims header says so), so commit A
   cannot serve as a paths-mode freeze (the paths are absent → rc 2). The census uses the
   instrument landing commit: r87 `21da383b`, r88 `1f267d4b`, r89 `0e6bb05f`, r90 `664435cf`
   (LOG commit B), r91 `386184a6` (LOG commit B). Round 86 is the mirror case: its claims
   freeze `61b0e074` postdates the inherited instrument landing `0481a6d3` (earlier attempt of
   the same round, named in both the r86 claims header and LOG), so the r86 census row uses the
   round's own claims freeze and the pre-freeze repairs (`c939e6b5`, `bfda0472`, `9972c87c`)
   stay outside its window. Round 85's claims freeze `1a45aeb5` predates its instruments
   (verified: `1a45aeb5` is an ancestor of `99a7cb3b`); using it makes the gate fail closed —
   `receipts/w-85-alt-freeze.txt`: `DEFECT SETUP path plans/round85_c1_replay.py absent at
   freeze 1a45aeb5…`, rc 2. The r85 row therefore uses `99a7cb3b` (LOG: "instruments and
   repairs").
3. **Tips.** Where the round's LOG entry names a measured tip, that tip is used: r86
   `276abd46` ("receipt and tip measurement"), r87 `10de494d`, r88 `7fcc680b`, r89 `00462b59`
   (attempt-2 re-measurement tip; attempt-1 `a9b8a1a0` gives the identical verdict, see
   `receipts/w-89-alt-tip.txt`), r90 `9cf98d90` ("measured tip for all counters"), r91
   `cefabd44` (tip D; tip C `a8de3e69` gives the identical verdict, `receipts/w-91-alt-tip.txt`
   — the D triage commit touched no census instrument). Round 85's LOG names no single final
   tip, so the item's fallback is used: the MANIFEST closure `commit` field `88651a72`
   (MANIFEST idx 1265). Sensitivity: at the r85 receipt's own `LANE_TIP dc02d818` the broken
   count is still 3 with rc 1 (`receipts/w-85-alt-tip.txt`; touched counts differ: 2/3/1 vs
   5/4/1). **The r85/r86 verdicts are stable under every window choice tried; only the touched
   counts move.**
4. **Instrument set = the item's patterns** `plans/round<N>_*.py` + `plans/round<N>-cases.json`,
   as present at T. Excluded, named: `plans/round85-defects.json` (the r85 claims file calls it
   a frozen input, but it matches neither pattern); `plans/round89-q66-records.json` (record
   table, not a cases table); r91's wider pinned-set list (`plans/anchor_line_check.py`,
   `plans/round83_c2_checks.py`, `plans/counter-pins-r91.json`) — outside the item's patterns;
   the claims files themselves; r92 instruments (out of the assigned 85–91 range — the gate's
   own W1 leg, freeze B2 `f0018773` → tip `1df76536`, broken=3, is round 92's row).
5. **Window bounded by each round's own tip.** Later-round edits to a round's instruments are
   outside that round's row by construction (e.g. round-92's `4f6b3c52`/`6a51ff0e` touched
   `round91_c1_replay.py`/`round91_counter_pin.py` after r91 closed; they cannot appear in the
   r91 row and are round-92 territory).
6. **The gate's `--work` battery ran in my scratch** (`$S/w-<N>`), never in the lane; fixture
   repos are the gate's own.

## Byte-facts to history (context only, not part of the census claim)

`git log -- plans/<path>` maps each breach to disclosed in-round commits — [INFERENCE] that the
disclosures below are the same edits the gate counts:

- r85: `2410f403` "probe emits the tb2-header subject line, counter trusts the new bytes",
  `e7b44805` "counter work-dir and v7/v8 repairs", `b1e57097`, `35b1e4e0`, `def5d0ea` "v3
  splits…". Round 85 closed with "post-scoring V8/V3 changes mean the frozen claim is not
  verified" (LOG closing correction) — the census count is the machine-checkable form of that
  disclosure.
- r86: `877f6512` "instruments bound to the freeze revision 61b0e074" (landed *after* that
  freeze), `316811fa` "battery repairs", `e23bec07` "instrument v2 … before any tip data".
  LOG discloses the repairs; the bytes now carry a count.
- r89: `000b7d1c` "C2 control fixes: mkdir, vacuity guard, deleted-figure marker…", disclosed
  in the r89 LOG header ("instrument edits between commits B and the tip are disclosed in
  `corpus/lessons/round-89.md` Mistakes 1–2").
- r91: `b836a862` "checker selftest fixtures corrected … pin ledger regenerated (commit B2,
  before any measured tip)", disclosed in the LOG. Note the tension in bytes: the r91 frozen
  pinned-set tip rule anchors the no-diff window at commit B `386184a6`, and B→tip does touch
  `plans/round91_counter_pin.py` — the letter of that rule and the bytes disagree, which is a
  bytes-fact of the same class round 92 routed (M8); routed to round 94, not judged here.

## Findings

- FINDING CEN-85 minor (bytes) round-85 window freeze `99a7cb3b` → closure `88651a72`: broken=3 intact=1, rc 1; identical broken=3 at the alternate tip `dc02d818`; rc 2 if the claims freeze `1a45aeb5` is used (instruments absent at freeze)
- FINDING CEN-86 minor (bytes) round-86 window claims-freeze `61b0e074` → tip `276abd46`: broken=2 intact=2, rc 1; wider window from first landing `0481a6d3` still broken=2 (touched 6/2/0/0)
- FINDING CEN-87 info round-87 window `21da383b` → `10de494d`: 5/5 intact, rc 0
- FINDING CEN-88 info round-88 window `1f267d4b` → `7fcc680b`: 4/4 intact, rc 0
- FINDING CEN-89 minor (bytes) round-89 window `0e6bb05f` → `00462b59`: broken=1 (`round89_claim_figures.py`), rc 1; identical at attempt-1 tip `a9b8a1a0`
- FINDING CEN-90 info round-90 window `664435cf` → `9cf98d90`: 5/5 intact, rc 0
- FINDING CEN-91 minor (bytes) round-91 window `386184a6` → `cefabd44`: broken=1 (`round91_counter_pin.py`, the B→B2 edit), rc 1; identical at tip C `a8de3e69`; B-anchored pinned-set tip rule and bytes disagree
- FINDING CEN-GATE info gate ran as frozen (sha256 `18b01b42…` matches the round-93 table row); 12/12 invocations `SELFTEST cases=10 ok=10`; rc semantics 0/1/2 exercised (one demonstrated rc 2)
- FINDING CEN-HIST info four broken rows (85, 86, 89, 91) correspond to edits each round disclosed in its own LOG/lesson; this census adds machine-checkable counts, and rounds 87/88/90 pass with zero breaches

No tool was installed or upgraded (none needed; pacman untouched). Host sysctls untouched.
The r85 alternate-freeze rc 2 demonstrates the gate's missing-path fail-closed path, which is
also the reason assumption 2 exists.
