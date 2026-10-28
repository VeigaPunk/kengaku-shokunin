# RevengerLedgerHistory — why `corpus/routed-findings.jsonl` has no owner field

Seat: revenger, round 51 wave 1. Item: reconstruct the ledger's introduction and schema, and
locate where the attribution duty was recorded instead. Read-only against the lane.

Axes named: **adjacency** (primary — this is C2's surface: "cross-domain evidence is named with
its owner and routed, not absorbed"); **freshness** (secondary, observed only: every row is a
dated state record whose append duty lapsed; not claimed here).

## REV / revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

Stage-1 freeze for this round: `e07f131cf7037e58a21db6e1f3986cf401ad257c`. Ledger bytes and all
history below were read at `4090c3d`; `git log -- corpus/routed-findings.jsonl` is identical at
`e07f131` (last touching commit `85a40be`, 2026-10-27).

## 1. Which round created it, and with what schema

```
$ git log --diff-filter=A --format='%H %ad %s' --date=short -- corpus/routed-findings.jsonl
74513c0625df7886357b866074104a0cf4bf9cc1 2026-10-26 round-41: land battery41 (7 modules, 48 fixtures), C2
constraints-scheduling package (entry, S122-S124, README/PROVINCE/SKILL), registry rows, routed-findings rider,
QUALITY Q31/Q32
```

Created in **round 41** (`74513c0`, author date `2026-10-26 15:54:45 -0300`) by the seat
`R41RoutedRider` as `considerthese/2026-10-26.md` proposal 1, seeded with **10 rows** — one per
§5 routed item of the round-39 and round-40 verifier spot-checks (`R39-R1..R5`, `R40-R1..R5`):

```
$ git show 74513c0:corpus/routed-findings.jsonl | wc -l
10
```

The schema it declared, verbatim from the tool docstring at creation
(`plans/routed_open.py:8-23`, unchanged since — the tool has exactly one commit,
`git log --format=%h -- plans/routed_open.py` → `74513c0`):

```
  id           unique, `[A-Za-z0-9][A-Za-z0-9._-]*`; an id appears once, ever. Appending a second
               row for an id is a defect, never an update.
  class        short slug for the finding class
  source       `<lesson file>:<line>` of the routing sentence, relative to the lane
  opened_round int >= 1
  status       one of open | closed | refused | blocked
  close        closing evidence (commit + path:line or receipt) -- required when status=closed
  blocker      the named blocker -- required when status=blocked or refused
  check        optional shell command run from the lane root that exits 0 exactly when the routed
               work is done; `--observe` compares it with `status`
  note         optional free text
```

and in the rider's own report (`.ufo/waves/round-41/build/R41RoutedRider.md:34-36`):
"Row schema: `id, class, source (file:line), opened_round, status (open|closed|refused|blocked),
close, blocker, check, note`." **Nine fields; no `owner`, no `disposition`.**

The field set never changed in any later edit. Measured across every commit that touched the
file (all rows, not a sample):

```
$ python3 -c "..."  # key-set census per commit
74513c0 rows 10 keysets {('blocker','check','class','close','id','note','opened_round','source','status'): 10}
ff14d76 rows 16 keysets {(...same 9...): 16}
77ea425 rows 60 keysets {(...same 9...): 60}
8adf76c rows 60 keysets {(...same 9...): 60}
02287ee rows 60 keysets {(...same 9...): 60}
85a40be rows 71 keysets {(...same 9...): 71}
```

## 2. The rounds that edited it

```
$ git log --format='%h %ad %s' --date=short --numstat -- corpus/routed-findings.jsonl
85a40be 2026-10-27 round-46: … routed ledger rows …                       11   0
02287ee 2026-10-26 round-44: … routed closures (15 field changes) …       15  15
8adf76c 2026-10-26 round-43: … routed ledger closures (clean-clone observe) 13 13
77ea425 2026-10-26 round-43: … routed R1-R6 (errata, S135, flip check Q35, routed ledger) 46 2
ff14d76 2026-10-26 round-42: … routed rows …                               6   0
74513c0 2026-10-26 round-41: … routed-findings rider …                    10   0
```

Row count per commit: `74513c0` 10 → `ff14d76` 16 → `77ea425` 60 → `8adf76c` 60 →
`02287ee` 60 → `85a40be` 71. Six commits total; **rounds 47, 48, 49 and 50 never touched the
file.** Every later edit is a row append or a status/close field rewrite (`02287ee` rewrites 15
existing lines — closures, not new fields).

The append duty also lapsed in content, not just in commits. At the tip:

```
$ python3 -c "..."  # id prefixes / max opened_round
Counter({'R42': 49, 'R45': 11, 'R40': 6, 'R39': 5})
max opened_round 45
```

`85a40be` appended 11 rows, all `opened_round: 45` (`R45-S5-1..6` closed, `R45-S5-7a` closed,
`R45-S5-7b..7e` open). So the ledger's newest finding is from **round 45** while the round-50
spot-check §6 routed four defects (D1 wave outputs, D3 WAVE-DONE, D5 source locations, D7 lesson
spot-check row) and rounds 46–49 routed their own §5 lists — **none of them has a row.** That is
the same adjacency gap this round's C2 measures, seen from the history side.

## 3. Was an owner field ever considered? Yes — twice, and both times kept out of the schema

**(a) Round-40 falsification, `F40CritPlanNext` D7.** The defect that *produced* the rider names
ownership in its title and then drops it from its correction:

```
.ufo/waves/round-40/falsify/F40CritPlanNext.md:174
### D7 — the rider has no artifact, no predicate and no owner [M] — X4
```

```
:182-184  - Smallest correction: keep one printed line (`routed_open=<n> oldest_round=<r>`) and one file, and say
          the rows go to a sibling append-only file that `ledger_tip.py` does not read (so the C1 pin is untouched) or
          defer the rider to the round that re-declares the ledger fixtures (D6).
```

The round-41 freeze copies that correction verbatim and therefore inherits the omission:

```
plans/round-41-claims.md:122-123
- considerthese: `2026-10-26.md` proposal 1 (routed-findings burn-down) as a rider — one append-only file and one
  printed `routed_open=<n> oldest_round=<r>` line, outside every pinned ledger (`F40CritPlanNext` D7).
```

`plans/routed_open.py` history contains the string `owner` zero times:

```
$ git log -p -- plans/routed_open.py | grep -ci owner
0
```

**(b) Round-41 falsification, `F41CritPlanNext` Q3 / D8 — the question asked one day after the
landing, and answered in prose.** The falsify seat was dispatched with "Are the routed items …
each owned?" and answered:

```
.ufo/waves/round-41/falsify/F41CritPlanNext.md:40-47
**Q3 — is each routed item owned?** *No.*

`python3 plans/routed_open.py --lane .` → `ROWS total=10 open=4 blocked=1 closed=5 refused=0`, `routed_open=5 oldest_round=39`.
Named in the plan slot: **1 of 5** (`R40-R1`, `:1650`). Owned (a seat/acceptance that closes it): **0 of 5**. `grep -c 'R39-R' SCORECARD.md`
→ **0**, so `R39-R2` (open), `R39-R3` (blocked), `R39-R4` (open, with a `check` command) and `R40-R5` (open) appear nowhere in the file;
```

```
:96-97
**D8 — routed ownership (high; see Q3).** Correction: restore the draft's `Carried / routed:` bullet, fenced as five rows with owner and
close-check, one per `R39-R2, R39-R3, R39-R4, R40-R1, R40-R5`.
```

Note the shape of D8's correction: five rows **with owner** — but fenced in the *plan slot*, not in
the ledger. So `owner` was proposed as SCORECARD prose, never as a row field. The answer to "was it
ever considered" is: **yes, twice, at falsification level; never at schema level.**

## 4. Where the attribution duty was recorded instead

**(a) `SCORECARD.md` planned-block prose — landed once, then decayed.** D8 was applied in
`53b9e4e` (2026-10-26 16:34, round-41 wave-2 landing), at `SCORECARD.md:1721-1725`:

```
- **Routed, owned (`corpus/routed-findings.jsonl`, `routed_open=5 oldest_round=39`):** R39-R2 (`git_leak_probe.py --work`
  absent dir) and R39-R4 (carried residual bundle) — operability fixes, L1; R39-R3 (order class into a ledger) — blocked
  while `plans/ledger_tip.py` is pinned; R40-R1 (counter soundness) — the calibration bullet above; R40-R5 (carried
  bundle) — L1, one item per round with a check command. Rows close only with evidence and a check.
```

That is the whole population of the convention:

```
$ grep -c 'Routed, owned' SCORECARD.md
1
$ grep -c '^- \*\*Routed (' SCORECARD.md
2
```

Later rounds keep the routed bullet but drop the ownership clause — `SCORECARD.md:1804`
(round 42) "**Routed (`corpus/routed-findings.jsonl`, `routed_open=10 oldest_round=39`):** R3 … —
owned, operability;", `:1915` (round 43) and `:2084` (round 45) "**Routed:** …" with no owner at
all. A one-round convention recorded in a per-round prose block is not a duty.

**(b) `PROVINCE.md` §Adjacent owner table — domain-level, predates the ledger.** `PROVINCE.md:129-146`,
added by `94da19e` (2026-10-19 — a week *before* the ledger existed):

```
### Adjacent

Owner lanes and what is routed to them (grounded in existing PROVINCE/lesson
text, not renegotiated this round):

| Owner | What is routed |
|---|---|
| **kama** | serving plane + endpoint identity … |
| **chousa** | research method … |
| **kotoba** | prompt- and skill-craft rules … |
| **protocol / aggregator** | fleet process … |
| **kagi** | Janitor consumer-side endpoint/credential config (round-9 routing) |
| **kumitate** | OMP route resolution, fallback policy … |
| **kasegi** | bounty-ledger mission-state / dispatcher semantics … |
| **kake** | web properties; the shared word "probe" carries no scope |
```

This table maps a *domain* to a lane. A routed finding is an *instance*; the join from row to
owner was left to the reader, which is why `round51_routing.py` has to test it row by row.

**(c) Free text inside rows.** Exactly one of 71 rows mentions the word at all, in `note`:

```
R42-R5 … "… (2) F39OrderGateMut fail-open - plans/order_check.py is unchanged (sha256 948d5e1d… = PINS at
plans/round42_c1_verify.py:98 and claims/frozen-digests.txt:8), so a repair this round would break PINS: blocked
by the freeze, not by owner absence; …"
```

## 5. Why the omission survived 71 rows: nothing machine-read the ledger

```
$ grep -rn 'routed_open\|routed-findings' plans/*.py SKILL.md | grep -v 'routed_open.py:'
plans/round51_routing.py:8,175,191,193,232        (this round's counter — the first and only reader)
```

`plans/round_close.py` does not invoke `plans/routed_open.py`; `SKILL.md` has no registry row for
it; `plans/ledger_tip.py` deliberately never reads the file. The rider's own report predicted this
failure mode at landing (`.ufo/waves/round-41/build/R41RoutedRider.md:128-131`): "Nothing
references them yet — a round close that does not invoke `routed_open.py` prints no line, exactly
the D7 failure mode." The prediction came true: rounds 47–50 appended nothing.

Measured at `4090c3d` with this round's frozen counter (read-only, no `--run-checks`):

```
$ python3 plans/round51_routing.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
exit=1
```

Identical to the frozen before receipt `.ufo/waves/round-51/claims/c2-before.txt` (which prints the
same eleven lines without the `DETAIL` block). Every row reports `missing owner,disposition`.

## 6. What this feeds (`## Mistakes`)

One sentence: **the owner question was asked and answered twice in prose, never encoded as a
field, so 71 rows accumulated with no owner and no gate noticed.**

Supporting chain, in order:
1. `74513c0` (r41) declares nine fields — the rider was built to D7's *smallest correction*, and
   that correction ("one printed line and one file") silently dropped the ownership half of D7's
   own title ("no artifact, no predicate and no owner").
2. `F41CritPlanNext` Q3 re-asks the question the same day and measures `Owned … 0 of 5`; D8's
   correction puts `owner` in the **plan slot**, not the row. `SCORECARD.md:1721` is that bullet;
   `grep -c 'Routed, owned' SCORECARD.md` → 1, i.e. the convention dies at the next round.
3. `PROVINCE.md:129` §Adjacent (2026-10-19) supplies a domain→lane table, so the *information*
   needed for an owner was present; the ledger simply never joined to it.
4. No counter, close gate or registry row read the ledger, so no append was ever forced: last
   append `85a40be` (r46, rows 60→71, all `opened_round=45`), and rounds 47–50's routed defects —
   including the round-50 spot-check §6 items this round answers — have **zero rows**.

The durable fix is a schema field with a predicate (this round's C2), not another prose bullet: a
prose duty with no reader decays in one round, measurably.

## 7. Limits

- Read-only throughout: `git log/show/blame/diff/rev-parse/ls-tree` and `grep` only; no fixture git
  call was needed (the item asked for lane history, and the lane is read-only for this seat). No
  writes outside this report.
- `--run-checks` was not run (out of scope: it executes 71 shell commands; C2's own seats own that).
- Only the ledger's own history and its declared readers were read. I did not audit whether any
  *individual* row's `close` evidence is truthful — that is C2's attribution work, not provenance.
- One inference is marked as such below; everything else above is a quoted command output.
- `[INFERENCE]` The reason the seed schema stopped at nine fields is not stated in any commit
  message or report; the chain (D7's correction text → freeze line 122-123 → rider report line 34)
  is textual, and I read it as inheritance rather than a deliberate exclusion of `owner`. No
  document in the lane says owner was rejected.
- `corpus/routed-findings.json` (the `.json` name some SCORECARD pointers use) never existed:
  `git log --all --format=%h -- corpus/routed-findings.json | wc -l` → `0`; `SCORECARD.md:2164`
  already supersedes that pointer to the `.jsonl`.
- Scratch `/fast/scratch/hyaku/kengaku-r51/RevengerLedgerHistory` was created, used as `TMPDIR`
  for the counter run, and removed before yield (verified absent). No tool was installed or
  upgraded; nothing was recorded because nothing changed.

VERDICT: ledger-created-round-41-74513c0-nine-fields-no-owner; owner-considered-twice-in-falsification-prose-F40-D7-and-F41-Q3/D8-never-as-a-field; duty-recorded-in-SCORECARD-prose-once-and-PROVINCE-Adjacent-domain-table; 71/71-rows-ownerless-at-4090c3d, predicate fail exit 1
