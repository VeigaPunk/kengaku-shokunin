# F38RevBatC — attack on battery38 `p3m.py` / `p5m.py` (C1, mutants N02/N07/N08)

Seat: reviewer (wave 2, falsify). Target: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/battery38/p3m.py`
(N02 mirror) and `p5m.py` (N07 silence, N08 mirror). For each fixture: does it demonstrate the
ADVERTISED behaviour its mutant names (the `adv` cell in `plans/round38_c1_verify.py` MUTANTS), or kill
incidentally? Side-channel hunt beyond the counter's token scan; fixture-name keying. All runs on a clean
clone of the landing tip `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`
(`/fast/scratch/hyaku/kengaku-r38/F38RevBatC/lane`), scratch deleted at the end.

## Setup

```
$ git -C "$S/lane" rev-parse HEAD            -> 8c7422d7a646515d80af44844e8ecc8a1fc1d30a
$ git -C "$S/lane" status --porcelain | wc -l -> 0
$ sha256sum p3m.py(lane) p3m.py(clone) p5m.py(lane) p5m.py(clone)
  851d4e82829b9b8fa688180bcba6295e531267d58b05e32af0b088d6d95c57d8 (all four identical)
  db9627e8cf3834202057e575416dc454c6c42b9ec9d136bf287ceadb7940803b (all four identical)
```
Frozen spec facts (from `plans/pkg-spec-r35.json`): `min_quotes=8`, `min_distinct_locations=8`, registry
rows in order `S105(→ capture test_outputs.py), S106(→ test.sh), S107(→ instruction.md)`.
The gate's P5 row loop (`pkg_gate.py` `c_captures`) iterates `p.spec["rows"].items()`; the N07 mutant
truncates that loop to `[:1]`; the N08 mutant disables the blank-line `continue`.

## 1. Baseline (counter, `--only N02,N07,N08`) — receipt `baseline-only.txt`

```
$ python3 plans/round38_c1_verify.py --lane "$S/lane" --only N02,N07,N08 --work "$S/w"
PINS total=14 mismatched=0
...
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N02 P3 mirror killed by=p3m-exact-min-distinct-locations -- a package with exactly min_distinct_locations quote lines is accepted [...]
MUTANT N07 P5 silence killed by=p5m-row-off-pin-later-row -- every registry row's capture is pinned in the manifest, not only the first [...]
MUTANT N08 P5 mirror killed by=p5m-manifest-blank-line -- a blank manifest line is tolerated, not an unparsed line [...]
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
exit=0
```

## 2. Ref-vs-mutant stdout (driver `drv.py`, receipt `driver-ref-mutant-stdout.txt`)

Built the three fixtures with the counter's own helpers (`Ctx`, the fixture modules), wrote the reference
gate and the exact single-replacement mutants, ran both on each fixture dir:

```
fixture p3m-exact-min-distinct-locations        reference rc=0: P3 ok rows=8 distinct_quotes=8 distinct_lines=8 out_of_word_range=0
                                               N02       rc=1: P3 DEFECT rows=8 distinct_quotes=8 distinct_lines=8 out_of_word_range=0
fixture p5m-row-off-pin-later-row               reference rc=1: P5 DEFECT manifest_entries=6 bad=1 first=S107: manifest digest differs from the spec pin
                                               N07       rc=0: P5 ok manifest_entries=6 bad=0 first=0
fixture p5m-manifest-blank-line                 reference rc=0: P5 ok manifest_entries=6 bad=0 first=0
                                               N08       rc=1: P5 DEFECT manifest_entries=6 bad=1 first=unparsed manifest line ''
```
The P3/P5 note numbers are the evidence:
- N02's package has exactly 8 distinct (capture, start) locations — `distinct_lines=8` — and the mutant's
  `>=`→`>` flip is the only difference between the two runs, so the P3 flip is exactly the `==` boundary.
- N07's defect is `first=S107`, and S107 is the LAST row (`spec rows order: ['S105','S106','S107']`): the
  mutant's `[:1]` truncation is the only difference, so the silenced check is a non-first row's pin check.
  All other clauses stay silent (`P4 ok checked=22`, `P5 bad=1` only, `P6-P9 ok`).
- N08's mutant (blank-`continue` disabled) is the only difference; it turns the tolerated blank line into
  `unparsed manifest line ''`.

## 3. Deletion experiments (each fixture in turn) — receipts `delete-p3m.txt`, `delete-p5m.txt`,
    `isolate-n07-only.txt`, `isolate-n07-only-n08.txt`, `isolate-n08-only.txt`, `isolate-n08-only-n07.txt`

```
rm plans/battery38/p3m.py
$ python3 plans/round38_c1_verify.py --lane "$S/lane" --only N02 --work "$S/w"
BATTERY fixtures=85 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N02 P3 mirror SURVIVED -- a package with exactly min_distinct_locations quote lines is accepted [...]
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
```
```
rm plans/battery38/p5m.py
$ python3 plans/round38_c1_verify.py --lane "$S/lane" --only N07,N08 --work "$S/w"
BATTERY fixtures=83 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N07 P5 silence SURVIVED -- every registry row's capture is pinned in the manifest, not only the first [...]
MUTANT N08 P5 mirror SURVIVED -- a blank manifest line is tolerated, not an unparsed line [...]
MUTANTS total=2 killed=0 survived=2 invalid=0 null_detected=0
```
Per-fixture isolation inside p5m (clone copy edited to keep one fixture):
```
p5m.py keeps ONLY N07 fixture:  MUTANT N07 killed by=p5m-row-off-pin-later-row;  N08 SURVIVED
p5m.py keeps ONLY N08 fixture:  MUTANT N08 killed by=p5m-manifest-blank-line;    N07 SURVIVED
```
Each fixture is necessary and sufficient for its own mutant; no other battery fixture (r36 + battery37 +
rest of battery38) kills any of N02/N07/N08.

## 4. Boundary probes (dev `--battery-dir` variants) — receipts `probe-p3m-want7.txt`,
    `probe-p3m-want9.txt`, `probe-p5m-first-row.txt`, `probe-p5m-mid-blank.txt`

- p3m variant keeping 9 rows (`want=9`): ref accepts (`FIXTURE p3m-dev-want9 expect=accept ... ok`) and
  `N02 P3 mirror SURVIVED` — the mutant passes everything strictly above 8. Combined with §2 (kill at
  exactly 8) and the genuine-package run below, the kill is boundary-specific.
- Genuine 22-row package (with `git add`, clean tree): reference `rc=0 P3 ok rows=22 ...` AND
  `N02-mutant rc=0 P3 ok rows=22 ...` — the mutant is not a blanket rejecter.
- p3m variant keeping 7 rows: the module's own guard aborts at build time
  (`RuntimeError: fixture would also break min_quotes`) because `min_quotes == min_distinct_locations == 8`
  — a 7-row cut would break both floors. The fixture cannot be built below the floor; it refuses rather
  than mis-attribute (defensive property).
- p5m N07 variant moving the FIRST row (S105) instead of S107: fixture fires correctly on ref
  (`observed_defects=P5 ok`) and `N07 SURVIVED` — the mutant covers the first row, so the kill indeed comes
  from the loop-truncation skipping a later row. The later-row choice is load-bearing.
- p5m N08 variant with the blank line inserted mid-manifest (not trailing): `N08 killed
  by=p5m-manifest-blank-MID-dev` — the demonstration is position-independent, not a trailing-whitespace
  artifact.

## 5. Side channels (manual review beyond the counter's token scan)

`sidechannel=0` in every run (counter tokens `/proc ppid cmdline psutil environ`). Manual review:
- Imports: p3m.py imports only `pathlib`; p5m.py only `hashlib`, `re`. No `os`/`sys`/`subprocess`,
  no `getenv`/`environ`, no argv/timing/socket/random/date reads, no reads of the gate or counter files.
- All file access is confined to the fixture dir `d` (entry, capture file, manifest) built by
  `ctx.genuine_package(d)`; the only non-d reads are the frozen spec via `ctx.spec` (the same spec the gate
  reads). Nothing writes outside `d`.
- No fixture-name keying: the gate never sees the FID; directory names are counter-generated and the
  renamed-copy rerun agrees (`renamed_disagree=0` in every run).
- No spec the gate would never see: both fixtures use the frozen `--spec` (no `--spec` in their argv).

## 6. Observations (not defects)

- The p3m fixture sits on BOTH floors at once (`min_quotes=8 == min_distinct_locations=8`: 8 texts, 8
  locations), so it would also kill the round-37 `Y3`-class mutant (`min_quotes >=`→`>`). In the frozen
  counter the kill is attributed to N02 by name, and the single-replacement argument ties the P3 flip to
  the `locs` floor specifically; the adv-cell sentence names only `min_distinct_locations`. Worth knowing
  when interpreting the fixture's breadth.
- The 7-row counterpart is impossible by the module's guard (above), so the below-floor side of the `locs`
  floor remains pinned by battery37's `p23-p3-seven-locations` (7 locations), not by p3m.
- N07 demonstrates the later-row check via the spec-pin branch (`manifest digest differs from the spec
  pin`), exactly reproducing the round-37 F37XMutP5 X1 witness; the `pinned in the manifest` branch on a
  later row (M16-style) is still only demonstrated on the first row (S105) by battery37. Both branches are
  silenced by the same N07 truncation, so the kill is correct either way.

## Conclusion

No defects found in `p3m.py`/`p5m.py`. All three fixtures demonstrate the exact behaviour their `adv` cells
name, kill only their own mutant, are necessary and sufficient (deletion + isolation), are boundary-specific
(exactly-8 / later-row / blank-line), and are free of side channels the token scan could miss. The N21
`silence`/mirror mislabelling and the other battery38 modules are out of this seat's scope.

Receipts: `baseline-only.txt`, `driver-ref-mutant-stdout.txt`, `delete-p3m.txt`, `delete-p5m.txt`,
`isolate-n07-only.txt`, `isolate-n07-only-n08.txt`, `isolate-n08-only.txt`, `isolate-n08-only-n07.txt`,
`probe-p3m-want7.txt`, `probe-p3m-want9.txt`, `probe-p5m-first-row.txt`, `probe-p5m-mid-blank.txt`.

VERDICT: battery-p3m-p5m-attack-0-defects
