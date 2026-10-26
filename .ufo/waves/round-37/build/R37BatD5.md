# R37BatD5 — C1 battery: the D5 (`d5-line`) branch, mutants M48–M53 and M55

Seat: executor, kengaku round 37 wave 1. Scope: one battery37 module, seven single-defect fixtures.
Nothing frozen touched (gate `plans/pkg_gate.py` at its freeze digest, `ea638822…dd41`, confirmed by the
counter's own `GATE … sha256=frozen` line).

Axes named before the first edit:

- **calibration** (the claim's axis): convert seven advertised-but-undemonstrated D5 defect classes into
  classes whose mutant changes the gate's result.
- **operability**: one stdlib-only module, one build helper per fixture, 7.7 s for the whole dev run
  (21 fixtures × reference run + 7 mutants).
- **single-defect clarity**: each fixture has exactly one defect, so its declared `defects` is `["D5"]`
  — `cmd_d5` is one clause with short-circuit returns, so no second clause can fire.

## 1. Deliverable

`battery/d5.py` (draft for L1 to land as `plans/battery37/d5.py`):

```
c3579f175cfe6b2fdba16a80847f88d04831e5b561df4db4af5898cc9aad75ee  battery/d5.py
```

5983 bytes, stdlib only (`hashlib`, `shutil`), `FIXTURES` of seven entries, fids all prefixed `d5-`.
Each builder writes only inside the empty `d`, copies the two files the gate actually reads
(`spec["d5"]["capture_name"]`, `spec["d5"]["manifest_name"]`) into `d/caps`, and returns
`["d5-line", "--file", <inside d>, "--capture-dir", <inside d>]`.

## 2. Fixture → mutant → silenced gate branch

Gate branch read at `plans/pkg_gate.py:327-356` (`cmd_d5`); the mutant `old → new` text at
`plans/round37_c1_verify.py` `MUTANTS`.

| fid | mutant | fixture (the single defect) | branch the mutant silences |
|---|---|---|---|
| `d5-m48-file-unreadable` | M48 | `--file` names a path that does not exist; capture dir genuine | `if lines is None: return False, "file unreadable"` |
| `d5-m49-two-lines` | M49 | the genuine erratum wrapped onto two non-blank lines, split at `" in this round's own reopen capture "` so line 1 keeps the label + `is present` and has no `not present` | `len(lines) != 1` half of the line-count/label test |
| `d5-m50-label-altered` | M50 | same single line with the label only changed (`Erratum (round 35):` → `Erratum (round 34):`), otherwise byte-identical | `startswith(d5["label"])` half of the line-count/label test |
| `d5-m51-require-missing` | M51 | required token replaced once (`is present` → `is here`); assert `require not in mutated and forbid not in mutated` | `bad.append(f"missing {d5['require']!r}")` |
| `d5-m52-forbid-present` | M52 | forbidden token appended (` The quote is not present in the 418-byte fetch.`) while `is present` stays | `bad.append(f"carries {d5['forbid']!r}")` |
| `d5-m53-capture-missing` | M53 | copied capture dir with the capture file unlinked, manifest left in place; line genuine | `if digest is None: return False, "capture unreadable"` |
| `d5-m55-quote-absent` | M55 | genuine capture with the quote removed verbatim (replaced by `（引用は削除されました）`), and `quarantine-SHA256SUMS` rewritten to `sha256(new bytes)` with the same path suffix, so the digest pin passes and only the quote check fires | `bad.append("quote absent from the capture")` |

M48 and M53 are the two `return False, "…unreadable"` exits of the same clause and are deliberately
separate fixtures: each fixture reaches exactly one of them (an absent `--file` never gets to the capture
read, a missing capture file is only reached after a readable, correctly labelled line).

M54 (`capture digest is not the one in the manifest`) is **not** built here: the frozen round-36 battery
already kills it — `MUTANT M54 D5 killed by=r36-L6` in my 8-mutant run (see §5), matching the freeze note.

## 3. Proof run — command and output in full

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
export S=/fast/scratch/hyaku/kengaku-r37/R37BatD5 TMPDIR=$S
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round37_c1_verify.py \
  --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37BatD5/battery \
  --only M48,M49,M50,M51,M52,M53,M55 --work "$S"
```

Exit 0. Output (`R37BatD5/receipt-d5-dev.txt`, verbatim):

```
GATE plans/pkg_gate.py sha256=frozen
FIXTURE r36-P0 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-P1 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P2 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P3 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P4 expect=reject declared=- observed_rc=1 observed_defects=P6 ok
FIXTURE r36-P5 expect=reject declared=- observed_rc=1 observed_defects=P1 ok
FIXTURE r36-P6 expect=reject declared=- observed_rc=1 observed_defects=P9 ok
FIXTURE r36-P7 expect=reject declared=- observed_rc=1 observed_defects=P1,P3,P6,P9 ok
FIXTURE r36-L1 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L2 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L3 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L4 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L5 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE r36-L6 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m48-file-unreadable expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m49-two-lines expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m50-label-altered expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m51-require-missing expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m52-forbid-present expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m53-capture-missing expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m55-quote-absent expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
BATTERY fixtures=21 wrong=0 renamed_disagree=0
MUTANT M48 D5 killed by=d5-m48-file-unreadable -- d5 file unreadable
MUTANT M49 D5 killed by=d5-m49-two-lines -- d5 file is not exactly one line
MUTANT M50 D5 killed by=d5-m50-label-altered -- d5 line does not carry the label
MUTANT M51 D5 killed by=d5-m51-require-missing -- d5 required token missing
MUTANT M52 D5 killed by=d5-m52-forbid-present -- d5 forbidden token present
MUTANT M53 D5 killed by=d5-m53-capture-missing -- d5 capture unreadable
MUTANT M55 D5 killed by=d5-m55-quote-absent -- d5 quote absent from the capture
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Every one of my seven FIXTURE lines ends `ok`; every mutant is `killed by=` its own fid; `wrong=0`,
`renamed_disagree=0`, `null_detected=0`. Because `differs()` scans fixtures in build order (the 14 r36
fixtures first), `killed by=<my fid>` also proves no round-36 fixture hits these seven branches.

Renamed run: the counter copies each fixture directory under a `x{…}q` name and rewrites the `d`-prefix
in argv; `renamed_disagree=0` is the measured statement that nothing here keys on a fixture's name.

## 4. Load-bearing check — delete one fixture, the matching mutant survives

Driver kept at `R37BatD5/drop_check.py`; receipt `R37BatD5/receipt-d5-dropcheck.txt`
(`python3 .ufo/waves/round-37/build/R37BatD5/drop_check.py "$S"`, exit 0):

```
sha256(module) = c3579f175cfe6b2fdba16a80847f88d04831e5b561df4db4af5898cc9aad75ee
dropped_fixture | mutant | counter result
d5-m48-file-unreadable | M48 | MUTANT M48 D5 SURVIVED -- d5 file unreadable
   BATTERY fixtures=20 wrong=0 renamed_disagree=0
d5-m49-two-lines | M49 | MUTANT M49 D5 SURVIVED -- d5 file is not exactly one line
   BATTERY fixtures=20 wrong=0 renamed_disagree=0
d5-m50-label-altered | M50 | MUTANT M50 D5 SURVIVED -- d5 line does not carry the label
   BATTERY fixtures=20 wrong=0 renamed_disagree=0
d5-m51-require-missing | M51 | MUTANT M51 D5 SURVIVED -- d5 required token missing
   BATTERY fixtures=20 wrong=0 renamed_disagree=0
d5-m52-forbid-present | M52 | MUTANT M52 D5 SURVIVED -- d5 forbidden token present
   BATTERY fixtures=20 wrong=0 renamed_disagree=0
d5-m53-capture-missing | M53 | MUTANT M53 D5 SURVIVED -- d5 capture unreadable
   BATTERY fixtures=20 wrong=0 renamed_disagree=0
d5-m55-quote-absent | M55 | MUTANT M55 D5 SURVIVED -- d5 quote absent from the capture
   BATTERY fixtures=20 wrong=0 renamed_disagree=0
```

7/7 flips, one fixture per mutant: no fixture is dead weight and no two fixtures share a kill.

## 5. Retained evidence and limits

- The 8-mutant run (same command with `--only M48,…,M54,M55`) also printed
  `MUTANT M54 D5 killed by=r36-L6 -- d5 capture digest not in the manifest` and
  `MUTANTS total=8 killed=8 survived=0`. M54 needs no fixture from this seat; that is the freeze's own
  "5/55" set, unchanged.
- `M55`'s manifest is rewritten to the new bytes and the builder asserts `quote not in capture` after the
  edit, so the pin passes and the quote check alone fires. Verified indirectly by the declaration: the
  unmodified gate prints `D5` once (a `D5 DEFECT` line is emitted once per clause, not once per bad item),
  and removing M55's branch flips the result — i.e. that branch was the only thing rejecting.
- `M49`'s wrapped line and `M50`'s relabelled line are the only changed bytes in those fixtures
  (`assert` in each builder guards the invariants it relies on: label present, require present, forbid
  absent, split anchor present).
- `M48`'s fixture never creates the file; `M53`'s keeps a genuine labelled line, so each targets one exit.
- Limit (named, not hidden): demonstration is observational — each fixture shows the branch is reached and
  its verdict is visible, not that the check is the right check. And the capture copies carry only the two
  files `cmd_d5` reads (`pkg_gate.py:341-349`), not the rest of
  `.ufo/waves/round-34/assimilation/captures/`; the gate never reads those bytes.
- Scratch `/fast/scratch/hyaku/kengaku-r37/R37BatD5` deleted after the receipts were copied
  (`ls -d` → `No such file or directory`). No lane file edited; `git` index and jj untouched; no
  `battery/__pycache__` left behind.
- Nothing installed this seat (no tool needed).

Integration note for the L1: land `battery/d5.py` as `plans/battery37/d5.py`; the full predicate still
needs the other seats' modules — with only this one, `--battery full` would report the remaining 43
survivors.

VERDICT: battery-d5-killed-7/7-wrong-0
