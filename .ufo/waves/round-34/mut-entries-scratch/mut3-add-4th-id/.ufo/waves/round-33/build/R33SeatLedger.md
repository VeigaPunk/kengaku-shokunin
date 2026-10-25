# R33SeatLedger — wave-1 build seat ledger scaffold

- Seat `R33SeatLedger`, role `scribe`, wave `kengaku-r33-build`, axis `operability`.
- Source of truth: `.ufo/waves/round-33/build-spec.json`,
  sha256 `c2986592606ec0ae9966c6732bb055cbfa386b25ac4990129a15c3422ab344aa` (39 770 bytes, 36 items).
- Generated 2026-10-25 from lane-local bytes only; no network fetch, no source opened.
- Wrote exactly one file: this report. No production edits, no Git mutation, no tool install/upgrade
  (none was needed), no model named.

## What was read (and what each read settled)

| path | what it settled |
|---|---|
| `.ufo/waves/round-33/build-spec.json` | item list: 36 items, `reportDir` `.ufo/waves/round-33/build`, fields per item `{axes,name,prompt,role}` only |
| `.ufo/waves/round-33/build/swarm-registry.json` | 36 dispatched members, name set identical to the spec (both set differences empty), `role` identical for all 36, `reportDir` identical |
| `.ufo/waves/round-32/build-spec.json` + `.ufo/waves/round-32/build/*.md` | naming precedent: 34 spec items → exactly 34 reports, every file named `<item name>.md` (both set differences empty) |
| `corpus/lessons/round-31.md` §Seat ledger | the lane's ledger idiom (summary row: wave / seats / roles / attack share / dead seats) |
| `corpus/lessons/round-33.md` | the §Seat ledger section already exists and ends "Seat-level ledger appended below once both results files land." — the insertion anchor |

## Paste-ready table

Insertion point: `corpus/lessons/round-33.md`, inside `## Seat ledger`, immediately after the
sentence ending `...once both results files land.` (that sentence is on line 45 of the file as read,
sha256 `6413e02a7536c5ffa0bbd78d0ad0eb59d9369852177f64efde9055b7c6b1ccef`; anchor on the text, the
line number drifts). Suggested one-line lead-in, then the table, one row per spec item in spec order:

**Wave-1 build (36 seats, spec order):**

| seat | role | report path | status |
|---|---|---|---|
| `R33ReconPackage` | scout | `.ufo/waves/round-33/build/R33ReconPackage.md` | pending |
| `R33ReconRegistry` | scout | `.ufo/waves/round-33/build/R33ReconRegistry.md` | pending |
| `R33CaptureToolathlon` | executor | `.ufo/waves/round-33/build/R33CaptureToolathlon.md` | pending |
| `R33CaptureArxiv` | executor | `.ufo/waves/round-33/build/R33CaptureArxiv.md` | pending |
| `R33CaptureSwePro` | executor | `.ufo/waves/round-33/build/R33CaptureSwePro.md` | pending |
| `R33IdGuard` | executor | `.ufo/waves/round-33/build/R33IdGuard.md` | pending |
| `R33RowDrafts` | scribe | `.ufo/waves/round-33/build/R33RowDrafts.md` | pending |
| `R33EntryPatch` | scribe | `.ufo/waves/round-33/build/R33EntryPatch.md` | pending |
| `R33ReadmePatch` | scribe | `.ufo/waves/round-33/build/R33ReadmePatch.md` | pending |
| `R33ScorecardPatch` | scribe | `.ufo/waves/round-33/build/R33ScorecardPatch.md` | pending |
| `R33Lesson31Err` | scribe | `.ufo/waves/round-33/build/R33Lesson31Err.md` | pending |
| `R33Lesson30Err` | scribe | `.ufo/waves/round-33/build/R33Lesson30Err.md` | pending |
| `R33FleetErrata` | scribe | `.ufo/waves/round-33/build/R33FleetErrata.md` | pending |
| `R33EntryTruth` | reviewer | `.ufo/waves/round-33/build/R33EntryTruth.md` | pending |
| `R33CounterAttack` | mutation-tester | `.ufo/waves/round-33/build/R33CounterAttack.md` | pending |
| `R33C1Counter` | critic | `.ufo/waves/round-33/build/R33C1Counter.md` | pending |
| `R33C3Design` | critic | `.ufo/waves/round-33/build/R33C3Design.md` | pending |
| `R33ClaimsReview` | reviewer | `.ufo/waves/round-33/build/R33ClaimsReview.md` | pending |
| `R33CensusWatch` | executor | `.ufo/waves/round-33/build/R33CensusWatch.md` | pending |
| `R33Connector` | connector | `.ufo/waves/round-33/build/R33Connector.md` | pending |
| `R33FrontierText` | scout | `.ufo/waves/round-33/build/R33FrontierText.md` | pending |
| `R33C1KillRule` | critic | `.ufo/waves/round-33/build/R33C1KillRule.md` | pending |
| `R33ReportOut` | scout | `.ufo/waves/round-33/build/R33ReportOut.md` | pending |
| `R33SeatLedger` | scribe | `.ufo/waves/round-33/build/R33SeatLedger.md` | pending |
| `R33MistakeMine` | scribe | `.ufo/waves/round-33/build/R33MistakeMine.md` | pending |
| `R33WaveBook` | executor | `.ufo/waves/round-33/build/R33WaveBook.md` | pending |
| `R33ExecDefsBefore` | executor | `.ufo/waves/round-33/build/R33ExecDefsBefore.md` | pending |
| `R33ExecVerifySelf` | executor | `.ufo/waves/round-33/build/R33ExecVerifySelf.md` | pending |
| `R33SentinelScope` | sentinel | `.ufo/waves/round-33/build/R33SentinelScope.md` | pending |
| `R33SourcesAdoptDry` | executor | `.ufo/waves/round-33/build/R33SourcesAdoptDry.md` | pending |
| `R33CaptureVerify` | reviewer | `.ufo/waves/round-33/build/R33CaptureVerify.md` | pending |
| `R33IndexTruth` | reviewer | `.ufo/waves/round-33/build/R33IndexTruth.md` | pending |
| `R33GraderSemantics` | revenger | `.ufo/waves/round-33/build/R33GraderSemantics.md` | pending |
| `R33SurveyScope` | critic | `.ufo/waves/round-33/build/R33SurveyScope.md` | pending |
| `R33L0Packet` | scribe | `.ufo/waves/round-33/build/R33L0Packet.md` | pending |
| `R33GateMutants` | mutation-tester | `.ufo/waves/round-33/build/R33GateMutants.md` | pending |

36 data rows, one per spec item. Falsify seats are deliberately absent: the wave-2 falsify spec is not
this item's input, and its ledger is a separate section (see note 7).

## Operability notes

1. **Order is spec order = dispatch order, not alphabetical.** `names == sorted(names)` is false on the
   spec (row 1 is `R33ReconPackage`, which sorts near the end). The dispatch registry stores members
   alphabetically; sorting the ledger to match the registry would break row-for-row correspondence with
   the spec. If a seat is inserted or renamed, regenerate from the spec rather than hand-inserting.
2. **Report path derivation is mechanical:** `<reportDir>/<item name>.md`, with `reportDir`
   `.ufo/waves/round-33/build` agreeing in both the spec and the registry. Precedent is exact, not
   assumed: round-32's spec has 34 items and the build directory has 34 `.md` files, the two name sets
   equal both ways.
3. **Status vocabulary is the L1's call.** Every row ships `pending` by instruction; nothing here infers
   a verdict from a report file existing. The three states the lane has needed before are `landed`
   (report committed, trailer resolves), `landed (no Report: trailer)` (round-31/32 evidence class), and
   `dead` (dispatched, no report — round-31's `R31FxEntryBar`). `superseded` is available if a seat
   returns more than once. Filling statuses keeps the table checkable because the checker below compares
   only the first three columns.
4. **Role tally for the lesson's round-31-style summary row:** scout 4, executor 9, scribe 10,
   reviewer 4, mutation-tester 2, critic 4, connector 1, sentinel 1, revenger 1 (sum 36); attack share
   (reviewer + critic + mutation-tester) = 10/36 = 28 %.
5. **Snapshot at scaffold time, informational only:** the build directory held
   `swarm-registry.json`, `receipts/`, and one report, `R33CensusWatch.md`. That file's row still says
   `pending` — the instruction fixes the status column, and this seat does not grade siblings' work.
6. **Self-reference:** row 24 is this seat. Its report exists only because this file was written; that is
   not evidence of any verdict on the item, and it confers no status.
7. **Out of scope by design:** the falsify-wave ledger (36 seats, `.ufo/waves/round-33/falsify/`), the
   fleet-side ledgers, and every corpus/SCORECARD/report draft byte. This item produces the scaffold only.

## Check for the L1 (self-contained, tested)

Run from the lane root. It re-derives the expected triples from the spec and compares them to the first
three columns of every row in the target file whose report path is under the build directory, so it keeps
working after statuses are filled and ignores falsify rows.

```bash
python3 - corpus/lessons/round-33.md <<'PY'
import json, re, sys
spec = json.load(open(".ufo/waves/round-33/build-spec.json"))
rows = [l for l in open(sys.argv[1]).read().splitlines() if re.match(r"^\| `R33", l)]
got = [tuple(c.strip().strip("`") for c in l.strip("|").split("|")[:3]) for l in rows]
got = [g for g in got if g[2].startswith(".ufo/waves/round-33/build/")]
want = [(i["name"], i["role"], ".ufo/waves/round-33/build/%s.md" % i["name"]) for i in spec["items"]]
print("spec=%d rows=%d match=%s" % (len(want), len(got), got == want))
if got != want:
    for n in range(max(len(got), len(want))):
        g = got[n] if n < len(got) else None
        w = want[n] if n < len(want) else None
        if g != w:
            print("first divergence row %d: got=%r want=%r" % (n + 1, g, w))
            break
sys.exit(0 if got == want else 1)
PY
```

Exercised this round against scratch fixtures (same script, absolute test-file argument; `/tmp` paths
not reusable, the script itself is) — observed, verbatim:

```
table.md            exit 0  spec=36 rows=36 match=True
filled.md (statuses replaced with `landed`)
                    exit 0  spec=36 rows=36 match=True
drop.md (row 5 deleted)
                    exit 1  spec=36 rows=35 match=False
                            first divergence row 5: got=('R33IdGuard', 'executor', '.ufo/waves/round-33/build/R33IdGuard.md') want=('R33CaptureSwePro', 'executor', '.ufo/waves/round-33/build/R33CaptureSwePro.md')
role.md (R33C1Counter critic→reviewer)
                    exit 1  spec=36 rows=36 match=False
                            first divergence row 16: got=('R33C1Counter', 'reviewer', '.ufo/waves/round-33/build/R33C1Counter.md') want=('R33C1Counter', 'critic', '.ufo/waves/round-33/build/R33C1Counter.md')
path.md (R33GraderSemantics.md→R33GraderSemantic.md)
                    exit 1  spec=36 rows=36 match=False
                            first divergence row 33: got=('R33GraderSemantics', 'revenger', '.ufo/waves/round-33/build/R33GraderSemantic.md') want=('R33GraderSemantics', 'revenger', '.ufo/waves/round-33/build/R33GraderSemantics.md')
falsify.md (exact table + one `.ufo/waves/round-33/falsify/` row)
                    exit 0  spec=36 rows=36 match=True
```

Run against this report itself (`.ufo/waves/round-33/build/R33SeatLedger.md`), the same script printed
`spec=36 rows=36 match=True` and exited 0, and the block between the `| seat |` header and the closing
paragraph compared byte-identical to the table re-rendered from the spec (38 lines: header + delimiter +
36 rows). The lesson-path form above was not run against `corpus/lessons/round-33.md` — the table is not
pasted there yet, and pasting it is the L1's act.

**Drift caveat:** if `build-spec.json` no longer hashes to `c2986592…`, the item list changed and this
scaffold is stale — regenerate, do not patch rows by hand.

## Bounds observed

- Wrote only `.ufo/waves/round-33/build/R33SeatLedger.md`. Draft bytes for `corpus/lessons/round-33.md`
  live inside this report (the table above); nothing was written to `corpus/`, `SCORECARD.md`, fleet
  reports, or `.ufo/state`.
- Read-only git was not needed and not used; no Git index touched. No subagents, no background jobs.
- Scratch: `/tmp/r33-R33SeatLedger/` (6 small `.md` fixtures + 1 script, < 32 KB total).
- No tool installed or upgraded.

VERDICT: ledger-scaffold
