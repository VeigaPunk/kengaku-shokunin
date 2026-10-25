# R30Yield — round-30 seat-yield rows generator (Q19)

Seat: `L1Kengaku30.R30Yield`. Leaf. No files under this repo were created or modified except this
report; the generator lives in scratch at `/tmp/r30-Yield/mkyield.py` (bounds forbid production edits).
No pacman transaction, no tool install, no subagent spawned (the fleet card forbids spawning; the
"single labrat" allowance in the ticket was not exercised — nothing needed delegating).

## What it is

`/tmp/r30-Yield/mkyield.py` (Python 3.14.8, stdlib only, argparse CLI) reads a wave registry JSON and
emits the four derivable Q19 columns per dispatched seat, leaving `caused_change`/`commit` empty for the
L1 to fill after landing:

```
round  seat  role_family  report  caused_change  commit
```

- Registry shapes accepted: full dispatch (`{"wave":…,"registry":{…}}`), bare registry
  (`.ufo/waves/round-30/build/swarm-registry.json`), or a plain member list. Members are read in
  registry order — the order rows must appear in the TSV.
- `report` = `<registry.reportDir>/<name>.md`; a member-level `report` key or `--report-dir` overrides it,
  which is how off-directory seats (round-29 `residual/`) are regenerated.
- `--round` defaults to the round parsed out of the registry path/reportDir (`round-29` → 29).
- `--dry-run` prints rows to stdout and writes nothing; stdout is pure TSV, the run summary (per-family
  seat/changed counts, the Q19 cut signal) goes to stderr.
- A re-run **carries the recorded** `caused_change`/`commit` for any (round, seat) already in the file, so
  regenerating after landing cannot blank evidence. A role/report disagreement with a recorded row is
  refused (`exit 2`) unless `--force`.
- Write mode rewrites atomically (temp + rename), replacing only rows whose (round, seat) it owns and
  copying every other round/seat through verbatim — no duplicates on re-run, no loss of rounds 25-29.

## Acceptance 1 — it runs, and the column count equals yield.tsv

`yield.tsv` header and all 40 data rows are 6 tab-separated fields:

```
$ awk -F'\t' 'NR>1{print NF}' .ufo/waves/yield.tsv | sort | uniq -c
     40 6
```

Round-29 fixture (registry `.ufo/waves/round-29/attempt2/build-dispatch.json`, 36 members):

```
$ python3 /tmp/r30-Yield/mkyield.py .ufo/waves/round-29/attempt2/build-dispatch.json --dry-run --round 29
exit=0
[dry-run] 36 rows for round 29; .../kengaku-shokunin/.ufo/waves/yield.tsv untouched
[preserve] carried recorded verdict for 36 seat(s), e.g. R29a2SrcS077
seats=36 families=10
  reviewer: seats=10 changed=10
  scout: seats=10 changed=5
  critic: seats=3 changed=3
  executor: seats=3 changed=2
  scribe: seats=3 changed=1
  connector: seats=2 changed=0
  simplifier: seats=2 changed=2
  mutation-tester: seats=1 changed=1
  revenger: seats=1 changed=1
  sentinel: seats=1 changed=0

fixture rows: 36 cols per row: [6]
```

The dry run wrote nothing — `yield.tsv` `sha256  e505d5a2…3b964fb` and mtime `1792911454` were identical
before and after (`sha_equal=yes mtime_equal=yes`).

## Acceptance 2 — three round-29 seats, field-for-field

Tab renders as `<TAB>`; `<EOL>` marks the line end. Each line below is the fixture output, and each was
also byte-compared against the live row (`line in live_file`).

```
29<TAB>R29a2SrcS077<TAB>scout<TAB>.ufo/waves/round-29/attempt2/build/R29a2SrcS077.md<TAB>no<TAB>8cf7b60/ff476d0/4b82ff7/7bc2aaf/c88310f<EOL>
29<TAB>R29a2GateAudit<TAB>executor<TAB>.ufo/waves/round-29/attempt2/build/R29a2GateAudit.md<TAB>yes<TAB>8cf7b60/ff476d0/4b82ff7/7bc2aaf/c88310f<EOL>
29<TAB>R29a2SimpCheck<TAB>simplifier<TAB>.ufo/waves/round-29/attempt2/build/R29a2SimpCheck.md<TAB>yes<TAB>8cf7b60/ff476d0/4b82ff7/7bc2aaf/c88310f<EOL>
```

`repr` of the same three lines (6 fields each, 115/123/125 bytes):

```
'29\tR29a2SrcS077\tscout\t.ufo/waves/round-29/attempt2/build/R29a2SrcS077.md\tno\t8cf7b60/ff476d0/4b82ff7/7bc2aaf/c88310f'
'29\tR29a2GateAudit\texecutor\t.ufo/waves/round-29/attempt2/build/R29a2GateAudit.md\tyes\t8cf7b60/ff476d0/4b82ff7/7bc2aaf/c88310f'
'29\tR29a2SimpCheck\tsimplifier\t.ufo/waves/round-29/attempt2/build/R29a2SimpCheck.md\tyes\t8cf7b60/ff476d0/4b82ff7/7bc2aaf/c88310f'
```

Whole-fixture comparison against the live file:

```
byte-identical against live: 36 / 36
mismatches: []
```

## Operative readiness for round 30

```
$ python3 /tmp/r30-Yield/mkyield.py .ufo/waves/round-30/build-dispatch.json --dry-run
30	R30SrcS081	scout	.ufo/waves/round-30/build/R30SrcS081.md		
…
30	R30RevFlip	revenger	.ufo/waves/round-30/build/R30RevFlip.md		
30	R30SimplGate	simplifier	.ufo/waves/round-30/build/R30SimplGate.md		

rows=36  cols=6  (round derived as 30 from registry.reportDir `.ufo/waves/round-30/build`)
families=9: scout 10, reviewer 7, executor 6, scribe 4, critic 3, connector 2, mutation-tester 2,
            revenger 1, simplifier 1
```

`caused_change` and `commit` are the two trailing empty fields (line ends in `<TAB><TAB>`), to be filled
after landing. Bare-registry input also works: the same 36 rows come out of
`.ufo/waves/round-30/build/swarm-registry.json` with no `--round`.

Write mechanics proven on a sandbox copy (`/tmp/r30-Yield/sandbox/.ufo/waves/yield.tsv`, copied from the
live file, 41 lines):

```
[write] .../yield.tsv: appended 36, updated 0     → 77 lines, all 6 fields, 36 lines start with `30\t`
re-run: [write] .../yield.tsv: appended 0, updated 36 → still 77 lines (idempotent, no duplicates)
all 41 pre-existing lines byte-identical and in order after the rewrite: True
appended block all round 30: True 36
```

## Failure-capable selftest (`--selftest`, 15/15 passed, exit 0)

Guards that reject rather than repair, measured by running them:

```
ok  two seats, roles and report paths from registry
ok  duplicate seat rejected                          duplicate seat 'R30A': two spawns would collide on report and report row
ok  missing role rejected                            seat 'R30A': role None is not a lowercase family slug
ok  uppercase role rejected                          seat 'R30A': role 'Scout' is not a lowercase family slug
ok  tab in role rejected                             seat 'R30A': role 'sc\tout' is not a lowercase family slug
ok  path traversal in report rejected                path '../x.md' is not a safe repo-relative path
ok  non-md report rejected                           seat 'R30A': report 'a.txt' does not end in .md
ok  empty member list rejected                       registry has zero seats: a round with no rows is a broken registry, not a yield
ok  recorded verdict carried, not blanked
ok  conflicting role refused                         registry disagrees with the recorded rows (pass --force to overwrite)
ok  conflicting report refused                       registry disagrees with the recorded rows (pass --force to overwrite)
ok  --force overwrites a conflict
ok  bad header refused                               header 'round\tseat\trole' != expected 'round\tseat\trole_family\treport\tcaused_change\tcommit'
ok  bad column count refused                         yield.tsv:2: 3 columns, expected 6
ok  dry-run leaves the file untouched
selftest: 15/15 passed
```

## Findings for the L1 (advisory, not fixed — production edits are out of scope)

1. **Round-29's build registry covers 36 of its 40 recorded rows.** The four `R29a2r*` residual seats came
   from a residual dispatch that is not on disk; `live round-29 rows: 40 … seats absent from fixture:
   ['R29a2rCounterRerun','R29a2rGateAttack','R29a2rEntryVerify','R29a2rCalibration']`. Regenerating
   round 29 therefore needs a residual registry (or `--report-dir …/residual` with a member list); the
   generator refuses to guess, and the write path preserves those four rows verbatim meanwhile.
2. **Two Q19 evidence pointers do not resolve.** `('29','R29a2rGateAttack', '.ufo/waves/round-29/attempt2/residual/R29a2rGateAttack.md')`
   and `('29','R29a2rEntryVerify', '.ufo/waves/round-29/attempt2/residual/R29a2rEntryVerify.md')` — the
   files on disk are `L1Kengaku29.R29a2rGateAttack.md` and `L1Kengaku29.R29a2rEntryVerify.md`. 38 of 40
   recorded report paths exist; these 2 do not. A row whose report cannot be opened is not evidence, so
   either the two cells or the two filenames should be corrected when the round-30 rows are appended.
3. **The generator is not standing yet** — it is scratch-only by construction. If the L1 wants it
   standing (the Q19 "reports yield per role family" half depends on running it every round), it must be
   landed as `plans/mkyield.py` in a round that owns a production claim; the sandbox rewrite in §"Write
   mechanics" is the behaviour to preserve.

## Files

- written: `.ufo/waves/round-30/build/R30Yield.md` (this report)
- scratch: `/tmp/r30-Yield/mkyield.py`, `/tmp/r30-Yield/r29-fixture.tsv`, `/tmp/r30-Yield/r30-fixture.tsv`,
  `/tmp/r30-Yield/sandbox/` (throwaway copy, deletable)
- production repo: no edits; `.ufo/waves/yield.tsv` `sha256 e505d5a2…3b964fb` unchanged by this seat
