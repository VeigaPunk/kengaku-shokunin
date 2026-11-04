# C2RedBeforeR72 — R72-C2 re-derived at both revisions with the freeze instrument

Seat: `C2RedBeforeR72` (leaf executor). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Base revision: `c63229724893c40b11661194ef1dff2987c177e9`. Round tip: `b6336136e0e891522b113a94d8e0bd65e0eae8de`
(`master`; tracked tree clean at both runs — `git status --porcelain` showed no ` M` entries).

## Verdict

Both required revisions re-derive exactly as the frozen claim states. The base run is a **red-*data*
run with the freeze instrument** (the round-72 gate script does not exist at the base tip, rc 128 for
`plans/round72_c2_routed_defects.py` at `c6322972`), which is the only construction available and is
the same class the R71-R7 erratum describes. The tip run is green. The corrections are strictly
append-only and positional: 25 inserted lines, 0 deleted lines, both superseded sentences above the
erratum heading, erratum the file's last `##` section.

| revision | `DEFECTS n=` | predicate line | exit |
|---|---|---|---|
| base `c6322972` | **6** (`4× row-absent`, `E1b no-errata-section`, `E2 no-errata-section`) | `PREDICATE R72-C2 fail` | 1 |
| tip `b6336136` | **0** | `PREDICATE R72-C2 pass` | 0 |

Frozen predicate sub-lines at tip, verbatim: `E1a ok`, `E1b ok`, `E1c ok`, `E2 ok`,
`DEFECTS n=0`, `PREDICATE R72-C2 pass`, rc 0.
`--selftest`: `SELFTEST defects-in-fake=3 want=3 all-fail=True append-only-arm=True
positional-arm=True parser-arm=True ok=True`, rc 0.
`--mutants`: `ARM accept-green=ok refuse-red=ok attribution=ok`, `MUTANTS total=7 killed=6
survived=0 invalid=0 null_detected=1`, rc 0. Both re-run in a second `--work` dir with identical
output (deterministic).

## Commands actually run (exit codes verbatim)

1. `mkdir -p /fast/scratch/hyaku/kengaku-r72/C2RedBeforeR72`
   `git clone -q --shared <lane> .../C2RedBeforeR72/base && git -C .../base checkout -q c6322972…`
   → `BASE_TIP=c63229724893c40b11661194ef1dff2987c177e9`, toplevel `/fast/scratch/hyaku/kengaku-r72/C2RedBeforeR72/base`.

2. Base run, cwd = lane (freeze instrument reading the base tree), stdout+rc captured to
   `corpus/evidence/round72/c2-red-before.txt` (14 lines including 4 header lines):

   ```
   E1c ok
   DEFECT E1a row-absent:round71-c1-hf-probe
   DEFECT E1a row-absent:round71-c2-routed-defects
   DEFECT E1a row-absent:round72-c1-hf-probe
   DEFECT E1a row-absent:round72-c2-routed-defects
   DEFECT E1b no-errata-section
   DEFECT E2 no-errata-section
   DEFECTS n=6
   PREDICATE R72-C2 fail
   EXIT=1
   ```
   Payload is byte-identical to the committed `.ufo/waves/round-72/c2-red-before.txt`
   (`diff` over the payload lines → `PAYLOAD_IDENTICAL`).

3. Tip run, cwd = lane: `python3 plans/round72_c2_routed_defects.py --lane .` →
   `corpus/evidence/round72/c2-green.txt` (11 lines):

   ```
   E1a ok
   E1b ok
   E1c ok
   E2 ok
   DEFECTS n=0
   PREDICATE R72-C2 pass
   EXIT=0
   ```

4. `python3 plans/round72_c2_routed_defects.py --lane . --json` → `{"defects": [], "n": 0}`, rc 0.

5. `python3 plans/round72_c2_routed_defects.py --selftest --work <scratch>/selftest` → rc 0, line quoted above.
6. `python3 plans/round72_c2_routed_defects.py --mutants --work <scratch>/mutants` → rc 0, six
   `verdict=killed` (M1–M6, each `accept_green=True escapes=1 attribution_ok=True null=False`) and
   `MUTANT M7-null-comment … null=True verdict=null`.

7. `git diff --numstat c63229724893c40b11661194ef1dff2987c177e9 master -- SKILL.md plans/round-71-claims.md`:

   ```
   5	0	SKILL.md
   20	0	plans/round-71-claims.md
   ```
   25 insertions, **0 deletions** → no pre-existing line was changed or removed.

8. Positional check (`grep -n`, `text.find`, heading scan) on `plans/round-71-claims.md` (155 lines):

   - `**Do-nothing control (committed at freeze).**` → line **59**, first-occurrence char offset 3753
   - `**Red-before (committed at freeze).**` → line **116**, offset 7641
   - `## Errata — round 72 (2026-11-03)` → line **137**, offset 8907
   - both 3753/7641 < 8907 → both sentences lie **above** the erratum;
   - headings are at lines 13, 77, 121, 137 → 137 is the last `##` section; each label occurs twice
     (body + verbatim quote in the erratum), and `text.find` hits the body copy.

## Corroborating re-derivations (independent of the gate's own code)

- Registry rows: `SKILL.md` lines **695–698**, one per `INSTRUMENTS` entry
  (`round71-c1-hf-probe`, `round71-c2-routed-defects`, `round72-c1-hf-probe`,
  `round72-c2-routed-defects`); each splits into exactly **8** cells, kind `probe`/`gate`/`probe`/`gate`,
  entry cell names its script, owner cell `kengaku`. They sit inside the section opened at line 587
  and closed by the next `## ` at line 797. Section-wide: 107 rows, 107 distinct names,
  no duplicate-named rows.
- Base tree: `SKILL.md` contains **0** occurrences of the four names; `plans/round-71-claims.md`
  contains **0** occurrences of `Errata — round 72`; `plans/round72_c1_hf_probe.py` and
  `plans/round72_c2_routed_defects.py` are both absent (rc 128) → the base defects are real, not staged.
- Erratum's two factual claims, checked against git objects:
  `d8a77d3f:.ufo/waves/round-71/c1-control.txt` → rc **128** (absent);
  `c80fcdb3:…c1-control.txt` → rc **0**; `d8a77d3f:…c2-red-before.txt` → rc **0**;
  `1cb49cac:plans/round71_c2_routed_defects.py` → rc **128**. Both revisions are ancestors of `master`.
- Lane's older registry gate (`plans/round52_c2_registry.py --lane …`) recognizes the fix:
  base `ADVERTISED total=108 REGISTERED total=101 rows=103 MISSING 7` (the two round-71 instruments
  among the 7); tip `ADVERTISED total=110 REGISTERED total=105 rows=107 MISSING 5 DUPLICATE 0`.
  The four rows remove round-71 from MISSING, add both round-72 instruments as registered, and
  introduce no duplicate. The remaining 5 MISSING (`round66_c1_tensor_probe`, `round69_c1_nginx_probe`,
  `round69_c2_routed_defects`, `round70_c1_nginx_probe`, `round70_c2_routed_defects`) are
  pre-existing debt from earlier rounds, identical at base and tip, and outside this claim.

## Findings (reported, not edited)

F1 — **E1b is presence-only; the R71-R7 error class is not repriced.** A copy of the live claims doc
with the two true revisions *swapped* (`c80fcdb3` attached to the red-before, `d8a77d3f` to the
control) still prints `E1b ok`, `E2 ok`, `DEFECTS n=0`, `PREDICATE R72-C2 pass`, rc 0 (probe P4).
The gate checks that both revision tokens occur in the erratum, not which artifact each one holds.
The live erratum is factually correct — checked above — so the claim holds, but the gate would not
have caught a mis-attributed correction of exactly the kind R71-R7 named.

F2 — **E1a is first-row-wins and duplicate-blind.** Appending a second `round72-c2-routed-defects`
row with 3 cells *after* the valid row still prints `E1a problems: []`, `DEFECTS n=0`, rc 0 (probe P1);
placing the same malformed row *before* the valid one reds `row-columns:…=3` and `row-entry:…` (P1b).
`registry_rows`/`by_name.setdefault` keeps only the first row per name. The lane's round-52 gate has a
`DUPLICATE` leg (`DUPLICATE 0` above); this gate has none. Not an overclaim of the frozen predicate —
"every instrument has an eight-column row" stays true — but a duplicate row cannot fail it.

F3 — **E1a prices 3 of the 6 fields its claim sentence names.** Overwriting the verdict-map,
self-test, pinned-values and write-scope cells of a row with `GARBAGE` still prints `E1a ok`,
`DEFECTS n=0`, rc 0 (P7). Only the column count, the entry cell and the kind/owner cells are read.

F4 — **The mutant matrix prices 6 of the gate's ~13 refusal sites, and `null` conflates a true no-op
with a fixture-invisible semantic weakening.** `REDS` covers only `E1a cols|owner`, `E1b
paraphrase|norev`, `E2 top|trailing|moved`. A mutant replacing
`if len(cells) > 2 and script not in cells[2]:` with `if False:` produces the identical verdict vector
over green + 7 reds (`(0,1,1,1,1,1,1,1)`), so the metric would classify it `null`, not
`survived`/`invalid` (P2). The clause itself is live: a row-entry red fixture gives pristine rc 1
(`DEFECT E1a row-entry:round71-c1-hf-probe`), mutant rc 0. Unpriced refusal clauses also include
`row-absent` (mutant vector), `row-kind`, `no-supersedes-wording`, `erratum-too-short`,
`claims-doc-absent`, and duplicate-row blindness. The frozen table of 7 is not claimed exhaustive,
so this is calibration, not a predicate failure.

F5 — **Base `n=6` is not a pure R71-R1 severity measure.** Two of the four `row-absent` defects are
for the round-72 instruments, which do not exist at the base tip (rc 128 for both scripts). The
number matches the frozen red-before exactly; the observation is only that the delta conflates
"round-71 rows added" with "round-72 rows exist at tip".

F6 — **Textual match of the frozen selftest string is prefix-exact, not line-exact.** The emitted line
is `SELFTEST defects-in-fake=3 want=3 all-fail=True append-only-arm=True positional-arm=True
parser-arm=True ok=True`; the frozen predicate quotes it without the trailing ` ok=True` (substring
holds, strict line equality would not). The mutants line matches exactly.

## Limitations

- The gate reads working-tree bytes for `--lane .`; the tip tree is clean, so tip == commit.
- Probes P1/P1b/P2/P4/P7 ran against throwaway copies of `SKILL.md` + `plans/round-71-claims.md` in
  this seat's scratch dir; no lane byte was modified by a probe (`git status --porcelain` after the
  runs shows only this seat's two evidence files plus siblings' files).
- I did not run the round-52 gate as a scored instrument (its 5 MISSING predate this round); it is
  quoted only as a cross-witness for the four rows.

## Tooling

No tool installed or upgraded (pacman paused; nothing needed).

## Scratch

`/fast/scratch/hyaku/kengaku-r72/C2RedBeforeR72/` (clone `base`, `selftest`, `mutants`, `probe*`)
was deleted at the end of this seat; both receipts were written into the lane first and re-read
before deletion. No file of this seat remains in `/tmp` (the three `/tmp/kengaku-*` files present
predate this seat, 15:57–20:55 local, and were not touched).
