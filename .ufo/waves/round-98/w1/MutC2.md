# MutC2 — R98-C2 mutation matrix (round 98)

**Verdict.** 29 single mutants (21 input-side, 8 counter-logic): **21 killed, 8 survived**. The
frozen predicate reproduces exactly on pristine and restored bytes at T. No survivor contradicts
the predicate at T; the survivors are coverage findings routed to round 99 (the claim forbids
repairing a frozen instrument in round). The lane was never edited; every write below is in
scratch or in this seat's evidence directory.

## Fixture and detector

- Scratch `/fast/scratch/hyaku/kengaku-r98/MutC2` (`TMPDIR` set to it, removed after receipts were
  copied). Fixture: `git clone --shared <lane> clone`, detached at T
  `8e37fc65d5649bb37166fdd6b1657445a8cb55b9`; `git -C clone rev-parse --show-toplevel` asserted
  equal to the clone before every write. Each input mutant is one commit whose parent is T.
- Detector: the frozen counter `plans/round98_c2_nested_bind.py` at T (`sha256 77c6ba05…`), run
  from the clone root: `python3 plans/round98_c2_nested_bind.py --lane . --rev <mutant> --work <dir>`.
- Counter-logic mutants are copies of the counter with one leg forced true (`kX = True` inserted
  after the assignment, so the `if not kX` defect branch is never taken), run against pristine T
  and against the negative fixture that leg is supposed to catch.
- Pristine baseline (`receipts/M00-baseline.txt`) and restored baseline
  (`receipts/M00b-restored.txt`) both print the frozen line verbatim:
  `TARGET pop=39 cleared=39 still=0 unbound=0 rows_changed=0 captures_changed=0 new_old_row_defects=0`,
  `PREDICATE R98-C2 pass`, rc 0. `GATE defects base=86 rev=45` (informational) in both.

## Table A — input mutants (21)

| id | single change | rev | failing legs | verdict |
|---|---|---|---|---|
| M01 | PROVENANCE.md: delete the S181 binding line | cdb6e5e5271a | K3 K4 | killed |
| M02 | PROVENANCE.md: delete S181 and S323 lines (partial) | e79ea9241a50 | K3 K4 | killed |
| M03 | PROVENANCE.md: swap the capture paths of S181 and S182 | 8bc11b27fca7 | K3 K4 K7 | killed |
| M04 | PROVENANCE.md: rename the S181 row id to S999 | 0d81c45bf6ad | K4 | killed |
| M05 | PROVENANCE.md: change the S181 sha256 column to 64 zeros | b0392e9989ea | — | **SURVIVOR** |
| M06 | PROVENANCE.md: point S181 at a non-committed path | 98042951d559 | K3 K4 | killed |
| M07 | SOURCES.md: edit the S181 anchor token | cdf6aecac592 | K3 K4 K5 K7 | killed |
| M08 | SOURCES.md: append one space to the S181 row line (same cells) | 6e1bf5305fd8 | K5 | killed |
| M09 | capture: append one newline byte to the S181 capture | b5b0c979b508 | K3 K4 K6 K7 | killed |
| M10 | capture: delete the S181 capture | 10d932adb2dd | K3 K4 K6 | killed |
| M11 | second PROVENANCE.md under corpus/evidence binds S181 to a byte-identical copy | 4462cc607766 | — | **SURVIVOR** |
| M12 | M11 plus the main S181 line deleted (sole binding = the copy) | f1c3c4b86d49 | K4 | killed |
| M13 | gate: append one comment line to plans/anchor_digest_check.py | 77948a735777 | K1 | killed |
| M14 | SOURCES.md: give clean non-POP row S105 an unknown 64-hex token | 6b510b67011e | K7 | killed |
| M15 | SOURCES.md: change the S306 URL subpath (same anchor-unbound class) | a65f67e5e23b | — | **SURVIVOR** |
| M16 | PROVENANCE.md: duplicate the S181 binding line (same path twice) | 710f07b3d296 | — | **SURVIVOR** |
| M17 | delete corpus/evidence/PROVENANCE.md entirely | 08e10f970747 | K3 K4 | killed |
| M18 | PROVENANCE.md: change the S181 pinned-URL column to a novel URL | da06ea6ccf13 | — | **SURVIVOR** |
| M19 | lessons: erratum line naming POP row S181 with an unresolved token | d67a8fcfd2be | K3 K7 | killed |
| M20 | second PROVENANCE.md at `corpus/evidence/0-mutant/` sorts FIRST and binds S181 to a copy | 0bec11d557e1 | K4 | killed |
| M21 | second PROVENANCE.md binds S181 to a foreign capture (different bytes) | 76a7b3eec2a4 | K3 K7 | killed |

Killing-leg detail (from the receipts): M01/M02 `K3 POP rows still defective n=…`, `K4 not bound …`;
M03 adds `K7 … S181:digest-wrong-capture,S182:digest-wrong-capture`; M04 `K4` only (see note N1);
M07 adds `K5 POP SOURCES rows changed` and `K7 … S181:digest-unknown`; M08 `K5` only; M09 adds
`K6 expected captures changed` and `K7 … digest-wrong-capture`; M10 `K3 K4 K6`; M12 `K4` only;
M13 `K1 gate base=11bb2cad87be rev=58eae3c97199 frozen=11bb2cad87be`; M14 `K7 … S105:digest-unknown`;
M17 `K3 K4` with all 39 sids; M19 `K3` and `K7 … S181:erratum-digest-unresolved+erratum-incomplete`
(K4 passes — the row is still bound); M20 `K4`; M21 `K3` and `K7 … S181:capture-unanchored`.

## Table B — counter-logic mutants (8)

| leg disabled | at T | detector fixture | observed with the leg disabled | verdict |
|---|---|---|---|---|
| L1 `k1 = True` | pass | M13 (gate +1 comment) | pass | killed by M13 |
| L2 `k2 = True` | pass | M17 (no provenance) | fail K3 K4 | **SURVIVOR** (see S5) |
| L3 `k3 = True` | pass | M17 / M19 (erratum) | fail K4 / fail K7 | **SURVIVOR** (see S5) |
| L4 `k4 = True` | pass | M12 (sole binding = copy) | pass | killed by M12 |
| L5 `k5 = True` | pass | M08 (row byte change) | pass | killed by M08 |
| L6 `k6 = True` | pass | M09 / M10 (capture change/delete) | fail K3 K4 K7 / fail K3 K4 | **SURVIVOR** (see S5) |
| L7 `k7 = True` | pass | M14 (non-POP row gains a defect) | pass | killed by M14 |
| L8 (counter POP drops S181) | fail K2 | — (positive control) | `K2 population derived=39 frozen=38 extra=['S181']` | killed by the T run |

L4 was also run against M11 and M16 (both pass) and L6 against both capture mutants; L3 against
both. All runs are in `receipts/logic-*.txt`.

## Survivors and reproducers

Reproducer shape (patches are in `patches/`, the exact mutated file hashes in `mutants.json`):

```
git clone --shared <lane> f && git -C f checkout 8e37fc65d5649bb37166fdd6b1657445a8cb55b9
git -C f apply .ufo/waves/round-98/w1/MutC2/patches/M11.patch
git -C f add -A && git -C f commit -m M11
python3 f/plans/round98_c2_nested_bind.py --lane f --rev HEAD --work <dir-outside-f>
```

**S1 — M11 / M16: K4 never reads the gate's `BIND+` line.** The gate prints one `BIND` line per
row (the first capture in `git ls-tree` path order) and a `BIND+` line for every additional
binding. The counter's regex is `^BIND (S\d{3,}) capture=(\S+) by=(\S+)`; `BIND+` does not match,
so `at["binds"][sid]` holds only the first binding. With a second `PROVENANCE.md` binding S181 to a
byte-identical copy (M11), or with the S181 line duplicated in the same file (M16), the gate emits

```
BIND  S181 capture=corpus/evidence/round52/graders/bn-fit-modify/tests/test_outputs.py by=provenance-row
BIND+ S181 capture=corpus/evidence/round52/graders/bn-fit-modify/tests/test_outputs.copy.py by=provenance-row
CAPTURES S181 n=2 claimed=<copy>,<expected> paths=<copy>,<expected>
```

and the counter still prints `PREDICATE R98-C2 pass` (receipts `in-M11.txt`, `in-M16.txt`). The
claim's "not to a copy" is therefore enforced only for the first-listed binding. The gap is
bounded and order-dependent: M20 (second file at `corpus/evidence/0-mutant/PROVENANCE.md`, which
sorts before `corpus/evidence/PROVENANCE.md`) makes the copy the first binding and K4 fails;
M21 (extra binding to *foreign bytes*) is caught by the gate's own `capture-unanchored` rule and
fails K3/K7. So only extra bindings to byte-identical copies, from a path sorting after the main
file, are invisible.

**S2 — M05: the PROVENANCE.md sha256 column is unverified.** Replacing S181's column with 64 zeros
still prints the frozen pass line; the gate binds by the backticked path and takes the digest from
the committed bytes, and K4 compares that digest to the POP token. The column is documentation,
not an input. (The claim's prose says the column "is the digest of the committed capture"; no leg
checks it.)

**S3 — M18: the pinned-URL column is unused while the row id binds.** Changing S181's URL to
`…/bn-fit-modify/tests/other.py` still passes, because `prov_sid` (the row id) is consulted before
`prov_url`. The column is not decorative, though: M04 shows that when the row id is wrong the same
URL binds the row by `provenance-url`, and K4's `how == provenance-row` check is what kills it.

**S4 — M15: K7 is class-level.** Changing non-POP row S306's upstream subpath from `bottle.py` to
`src/bottle.py` changes the gate's defect detail from `no-capture-for-upstream-?/bottle.py-task=?`
to `no-capture-for-upstream-src/bottle.py-task=src` while the class stays `anchor-unbound`; the
counter passes. This matches the claim's stated K7 ("(sid, class) DEFECT pairs"), so it is a
documented limit, but a non-POP row's unbound *reason* can regress silently.

**S5 — L2 / L3 / L6: three legs are not independently reachable from rev-side inputs.**
- K2 compares the frozen POP to the derivation at BASE, and BASE is immutable (resolved by hash),
  so no fixture input can move it; L2 survives every input mutant. It is still load-bearing
  against counter drift: L8 (S181 dropped from the POP dict) fails K2 at T.
- K3 is implied by K4 ∨ K7 for this population: every POP row has exactly one BASE defect
  (`anchor-unbound`), so a rev-side defect on a POP row either leaves it unbound (K4 fails, M17)
  or is a new class (K7 fails, M19). L3 survives both detectors.
- K6 is implied by K4 ∧ K5: a changed expected capture either no longer resolves the SOURCES token
  (K4 fails) or the row had to be edited to keep it resolving (K5 fails). L6 survives M09 and M10.

## Killed-mutant notes worth keeping

- **N1 (M04).** Renaming the PROVENANCE row id does not unbind the row: the URL column on the same
  line still feeds `prov_url`, and the gate binds S181 by `provenance-url` to the expected capture
  with the right digest (K3 passes). K4 fails on the `how` value alone — the `by=provenance-row`
  check is load-bearing, not cosmetic.
- **N2 (M03 vs M12/M20).** Swapping two POP rows' paths to captures with *different* bytes fails
  K3/K4/K7 (`digest-wrong-capture`); binding to a *byte-identical* copy fails K4 only. The
  counter's K4 is the leg that distinguishes "the replay's own capture" from "a copy".
- **N3 (M19).** An erratum defect on a POP row leaves K4 passing (the row is still bound) and is
  caught by K3 and K7; this is the only observed input where K3 fires while K4 passes.

## Restoration

Every mutant was built from T and the fixture was reset to T afterwards; `mutants.json` records
`restore_ok: true`. Final hashes of the four frozen inputs in the fixture:

```
d3fc4b7c9c69614fd2656407c5161780f903f0e5d1c66acad467135ba0f530b9  corpus/evidence/PROVENANCE.md
793b0520be4ac6b074dc463b7b74f79c15af2962c4657e67a3e8f040e206008a  corpus/SOURCES.md
11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2  plans/anchor_digest_check.py
364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455b  corpus/evidence/round52/graders/bn-fit-modify/tests/test_outputs.py
```

The restored-bytes detector run (`receipts/M00b-restored.txt`) prints the frozen pass line. The
lane's `git status --porcelain` showed only other seats' concurrent paths; this seat wrote nothing
outside its scratch and this evidence directory.

## Receipts

`receipts/M00-baseline.txt`, `M00b-restored.txt`, `in-M01…M21.txt`, `logic-L1-M13.txt`,
`logic-L2-{T,M17}.txt`, `logic-L3-{T,M17,M19}.txt`, `logic-L4-{T,M11,M12,M16}.txt`,
`logic-L5-{T,M08}.txt`, `logic-L6-{T,M09,M10}.txt`, `logic-L7-{T,M14}.txt`, `logic-L8-T.txt`,
`gate-T-verbose.txt`, `gate-BASE-verbose.txt`; `matrix.tsv`; `mutants.json` / `mutants2.json`
(commits, before/after file hashes); `runs.json` / `summary.json`; `patches/M01…M21.patch`;
`counter/L1…L8.py`; the builders `mutate.py`, `mutate2.py`, `run_matrix.py`, `summarize.py`.

Tooling: no installs or upgrades were needed (python3 3.13 stdlib, git); no pacman transaction was
run.
