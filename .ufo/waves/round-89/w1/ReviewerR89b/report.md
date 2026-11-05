# ReviewerR89b — Q66 v2 attack, seven new fixtures (scratch clone only)

Seat: leaf reviewer, round-89 w1. Lane clone at the measured tip
`a9b8a1a00b6a5ab5206be4d377dba439e02f8244`, taken with `git clone --no-hardlinks`
into `/fast/scratch/hyaku/kengaku-r89/ReviewerR89b/lane` (HEAD inside the clone was
`63d61d0f` because the clone follows the branch; the instrument was pinned to the
measured tip by passing `REV = a9b8a1a0…` explicitly, which is the byte set the
counter reads via `git -C lane show REV:<path>` — no worktree write, no commit,
no push, no mutating git command anywhere).

Attack methodology: `plans/round89_claim_figures.py` was imported from the clone
(`sys.path.insert(0, clone/plans)`) and each fixture was applied as one byte-level
edit to the tip claims file, passed through `run_check(lane, REV, work,
overrides={path: text})` (the overrides argument is the counter's own fixture
surface — nothing was written to a production path, and no counter was ever run
with `--lane` pointing at the real lane).

## Result table (predicted BEFORE each run; see fixtures.txt for the full rows)

| # | fixture | file | predicted | observed | verdict |
|---|---------|------|-----------|----------|---------|
| F1 | one word of prose changed ("round 84"→"round 90") | plans/round-84-claims.md | green | rc=0, defects=[] (130 s) | agrees (green) |
| F2 | `located=0`→`located=1` on R86-C1 before-figure | plans/round-86-claims.md | red | rc=1, first DEFECT `F7-record-missing ('R86-C1','kv','located','=',0)` | agrees (red) |
| F3 | R80-C1 before-figure line duplicated verbatim | plans/round-80-claims.md | green (dedupe by `(claim,kind,key,op,claimed)`) | rc=0, defects=[] | agrees (green) |
| F4 | R87-C1 `defects=7`→`defects=3` | plans/round-87-claims.md | red | rc=1, first DEFECT `F7-record-missing ('R87-C1','kv','defects','=',7)` | agrees (red) |
| F5 | new `Before (BASE…` line appending `TARGET x=1` to R80-C2 | plans/round-80-claims.md | red | rc=1, first DEFECT `F7-record-extra ('R80-C2','kv','x','=',1)` | agrees (red) |
| F6 | after-figure `ids=8`→`ids=9` (spec anomaly below) | plans/round-85-claims.md | **red** | **rc=0, defects=[] (43 s)** | **MISMATCH — finding** |
| F7 | whole `## R85-C2` section body → one prose line | plans/round-85-claims.md | red | rc=1, first DEFECT `F7-record-missing ('R85-C2','code','indexed=no','present',1)` (5 records missing) | agrees (red) |

Every run printed the full `RECORDS … / DEFECTS n=… / TARGET … / PREDICATE R89-C2 …`
block; a predicted-green fixture that went red or a predicted-red that stayed green
would be a finding. Exactly one such finding exists.

## Findings

### Finding 1 (the after-figure hole, F6): a doctored after-figure stays green

Command (its driver fragment, run from the scratch clone):

```
python3 - <<'PY'
import round89_claim_figures as cf
cf.run_check(lane, "a9b8a1a0…", work, overrides={"plans/round-85-claims.md": doctored_text})
PY
```

Observed output (first/only relevant lines): `RECORDS claims=17 files=8 records=56
checked=56 matched=55 mismatches=1 prose=0`, then `DEFECTS n=0`, then
`PREDICATE R89-C2 pass` — exit 0.

The edit: the R85-C2 **Target** line's frozen after-figure
`` `TARGET ids=8 closed=8 checks_passed=8 indexed=yes defects=0` `` was changed to
`` `TARGET ids=9 closed=8 checks_passed=8 indexed=yes defects=0` `` in the tip bytes
of `plans/round-85-claims.md`. The counter still exits 0 with zero defects. Cause:
the counter's record extraction (`claim_spans` / `extract_records_from_text`) only
builds records from `Before (BASE…` / `at BASE` spans, and the record-multiset pin
`plans/round89-q66-records.json` contains exactly those before-figure records — the
after-figure `ids=8` is not a record, not checked against the R85-C2 counter output,
and not pinned, so changing it is invisible to `run_check`. This is the same defect
class round 88 mined as `figure-not-measured`, surviving on the after-figure side of
the same claims line family.

### Spec anomaly (F6 anchor, reported, not repaired)

The item's literal anchor is "digit `4` in `ids=8`". `grep -n "ids="` over every
claims file in the corpus returns exactly two `ids=` figures, both in
`plans/round-85-claims.md` (lines 106 and 108), neither contains a digit `4`, and
`plans/round-84-claims.md` contains **no** `ids` figure at all (its R84-C2 records are
`entries/q1/q13/q21/defects`). I ran the nearest reading of the intent — the R85-C2
after-figure `ids=8` → `ids=9` edit — and report the discrepancy here instead of
editing any frozen spec. (Had the intent been the R84-C2 corpus, no fixture with the
literal anchor "digit 4 in ids=8" could exist.)

## Coverage and calibration verdicts (this seat's own measurement, in-scope reading)

- **Coverage of the Q66 v2 counter**: six of seven fixtures (F1 green, F2 red, F3 green, F4 red,
  F5 red, F7 red) agree with the pinned `KNOWN` set and the record-table pin; the counter's
  before-figure surface is sound on the probes thrown at it here.
- **Calibration defect**: one, F6, above. Its severity is bounded: after-figure records
  (`records=56 checked=56`) mean the counter never even sees line 106, so a doctored
  after-figure shows through as a green run with `mismatches=1` (the known R87-C1 mismatch) and
  `defects=0` — the tip-green gate still holds, but the after-figure, unlike the before-figure,
  is not a guard.
- No fixture exceeded 10 minutes (longest wall time 130 s).

## Record-hygiene note

F3's predicted green assumed keyed dedupe; the observed dedupe key
`(claim, kind, key, op, claimed)` makes the duplicate line collapse to one record —
predicted and observed agree, and the counter did not double-count the duplicated
before-figure. This validates the `add()` dedupe (unlike the round-88 KNOWN check,
which used only `(claim, key)` pairs).

No tool installs were needed for this seat (no `pacman`, no `uv`, no downloads), so
the tooling-authorization ledger has no new entries from this seat.
