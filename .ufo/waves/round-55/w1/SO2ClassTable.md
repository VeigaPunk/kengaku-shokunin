# SO2ClassTable — round 55 wave 1 seat report

Mechanical collection of the 12 held TB2 entries' receipt numbers into
`.ufo/waves/round-55/w1/SO2ClassTable/table.tsv` (paths relative to the lane repo).

## What ran (all read-only; no installs; no git mutation)

1. Read frozen claims `plans/round-55-claims.md` (commit `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`) — exit 0.
2. Glob `corpus/knowledge/tb2-*.md` → **15 files**; exit 0.
3. Read the head of each of the 15 to fix the selection set — exit 0.
4. Grep the 12 receipts under `corpus/evidence/round3*/`–`round4*/` for
   `cases=[0-9]+ observed_pass=[0-9]+ observed_fail=[0-9]+ mismatches=[0-9]+` — exactly one match per receipt, exit 0.
5. Grep the 12 entries for their `plans/*probe*.py` instrument names (cross-read from each entry's `recheck:`/falsifier/receipt-summary blocks) — exit 0.
6. Verification pass, exit 0:
   - `test -f plans/<probe>.py` for all 12 probe paths → 12/12 `PROBE-OK`;
   - `grep -cE '^cases=…$'` per receipt → 12/12 `SUMMARY-LINES=1` (one anchored summary line each);
   - `ls corpus/knowledge/tb2-*.md | wc -l` → 15 (selection documented below).

No check in this seat's scope was left unrun. No `RECEIPT-MISSING` row: every one of the 12
entries names a receipt that exists and carries exactly one anchored summary line.

## Selection (why 12 rows from 15 `tb2-*.md`)

- `tb2-chess-best-move-grader.md` — the round-55 C3 entry (13th grader), receipt under
  `corpus/evidence/round55/`, second-seat re-read pending; not yet a held entry.
- `tb2-presence-only-triage.md`, `tb2-grader-vacuity-triage.md` — round-52/53 population
  triage instruments, not per-task grader entries; no TB2-task receipt of the `cases=…` class.
- The remaining 12 are the held "read and executed" grader entries = the table's rows.

Every receipt summary line also cross-checks byte-for-byte against the summary its own entry
states (receipt-summary block or falsifier), e.g. build-pmars `:24`, git-leak `:27`, db-wal `:25`.

## Files written

- `.ufo/waves/round-55/w1/SO2ClassTable/table.tsv` — header + 12 data rows + `TOTALS`
  `cases=240 observed_pass=91 observed_fail=149 mismatches=2` (arithmetic checked: per-row
  pass+fail = cases; totals 91+149=240).
- `.ufo/waves/round-55/w1/SO2ClassTable/report.md` — this file.
- `.ufo/waves/round-55/w1/SO2ClassTable.md` — copy of this report at the prompt's `Report:` path.

## Observations (observed facts, not defects in my scope)

- `constraints-scheduling` receipt: `mismatches=2` — the only nonzero mismatch count; the
  entry's round-41 wave-2 erratum (W1) already records both as pilot prediction errors carried
  verbatim. Copied as observed, not "fixed".
- `polyglot-c-py` receipt also carries `regrade cases=18 differ=7` (the non-idempotence
  finding); out of the requested column set, so not in the TSV.
- `git-leak-probe.txt` (round 39) has no `regrade` line, unlike the other post-42 receipts;
  noted, nothing claimed from it.
- `corpus/evidence/round36/regex-log-probe-first-run.txt` exists (round-36 pilot); the entry
  of record cites `regex-log-probe.txt`, which is what the TSV holds.

## Defects found in sibling-owned files

None. All 12 probes exist; all 12 receipts exist with exactly one summary line; entry-stated
summaries equal receipt bytes.

## Dead ends / scratch

- Scratch `/fast/scratch/hyaku/kengaku-r55/SO2ClassTable/` was created per contract but was
  never needed (pure read task) — deleted before yielding, empty.
- No installs were made; no tooling recorded.
