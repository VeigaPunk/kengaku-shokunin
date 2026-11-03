# ScribeAttempt2 — round 68, attempt 2, wave w2: attempt-2 record drafts

**Seat:** ScribeAttempt2 (scribe, leaf). **Date:** 2026-11-03. **Judged on:** coverage, calibration.
**Scope of this file:** DRAFTS ONLY. This seat wrote no L file except this one. Every draft block below
is for the L1 to integrate into `corpus/lessons/round-68.md`, `SCORECARD.md` and `LOG.md`; the claims
doc, the counters and the targets are frozen and untouched. No git/jj write command was run; no install
was made; no subagent was dispatched.

Fill markers are written `<seat: …>` (or `<scout: …>` for the Gate line the brief asked to leave open).
They are placeholders for a seat's measured value and must be resolved from the named receipt before any
of this text enters an L file. See §5.

---

## 0. Read state and measured facts (all read-only)

| measurement | command | output |
|---|---|---|
| lane tip at read | `git -C L rev-parse HEAD` | `7803bdd4` (attempt-2 freeze A2) over attempt-1 landing `0e52fb5d` |
| lane history | `git -C L log --oneline -6` | `7803bdd4` A2 freeze · `0e52fb5d` attempt-1 landing · `d5b3c309` arg fix · `a8883187` freeze · `d2ed4ca3` round-67 closure |
| working tree | `git -C L status --porcelain` | clean except wave-produced untracked paths (`.ufo/waves/round-68/w2-validate.stderr`, `w2.ready`, `w2.ready.dispatched`, `w2/census-before.txt`, `w2/GateReverify/`, `w2/ReceiptReverify/` at read time) |
| attempt-1 report bytes | `sha256sum` on the fixture and the filed fleet report | both `0399cd5376d27e1c006075929a9b3511c820fc326b4a3751a4cd9b78b8573839` — the fixture `.ufo/waves/round-68/w2/report-fixtures/attempt1-report.md` and the filed `/home/vgpnk/Projects/shokunin/.ufo/reports/round-68/kengaku.md` are byte-identical |
| attempt-1 report shape | `wc -c`; `grep -c '^## '`; `grep -c '^## SHONEN'`; `grep -c '^## Trend verdicts'` | `12415` bytes; `7` `##` sections; `0`; `0` |
| attempt-1 headings | `grep -n '^#\{1,3\} '` | Work performed, Landed changes, Before → after measurements, Sources & frontier, Named limitations, Round shape, Tooling record |
| driver content check | read `scripts/shokunin-watchdog.sh` | `report_of` at `:184–206`: SHONEN heading-or-bold-marker regex + size ≥ `MIN_REPORT_BYTES` (`:54`, default 400); unchanged-digest arm when a same-round baseline exists |
| driver log line | read `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:2132` | `2026-11-03T20:20:14-03:00 lane-dead-no-report kengaku round=68; retry same round (hyaku-inline attempt=1: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-68/kengaku.md)` |
| A2 gate bytes | `wc -c`; `sha256sum`; `git show 7803bdd4:plans/round68_report_contract.py \| sha256sum` | `10242` bytes; `18fbfc2111d747ae9f40220333f0bbd56062c89e93bcd7c2477358228a0723f4` — committed bytes and working tree agree (`git diff` empty) |
| A2 gate checks | read the file | S1 `:80`, S2 `:96`, S3 `:107`, S4 `:116`, S5 `:133` (sentinels at `:45`), S6 `:138`; `box_keys` `:52`, `section` `:62`, `selftest` `:165`, tally print `:200` |
| w2 spec (dispatch ground truth) | `python3` over `.ufo/waves/round-68/w2-spec.json`; `sha256sum`; `git ls-tree 7803bdd4` | `12` items, `maxLanes 12`; sha256 `dfc1b865159581bc229af7a0012919a2e1fa3da3b9574afc3f0630a618637aac`; tracked at `7803bdd4` |
| lesson `## Mistakes` shape | `nl -ba corpus/lessons/round-68.md` | header `:60`, separator `:61`, rows `:62–63` and `:65–67` (blank line at `:64` splits the table), orphan prose `:68–77`; `grep -c '^| '` → `6` = header + separator + 4 rows |
| registry | `awk '/^## Gate\/probe registry/,0' SKILL.md \| grep -c …` | `146` registry rows; `0` mention `round66_c1_tensor_probe`; the only file-wide match is the class-row evidence cell at `SKILL.md:81` |
| round-68 anchors (attempt-1 state) | `grep -c` | `executed 2 of 8` → 1; `round67_c1_pipeline_probe` → 2; `^## Erratum \(round 68\)` → 1; `^\| S240 \|` → 1; SOURCES data rows → 232 |
| L0 lines still present | `grep -n kengaku /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` | `round-25 :72`, `round-33 :163`, `round-51 :200`, `round-54 :213–214`, `round-56 :250–251`, `round-63 :259`, `round-65 :270`, `round-66 :276`, `round-67 :280–281` (plus older `round-10 :7`, `round-13 :35`, `round-29 :88–93`, `round-52 :203`, not carried by the attempt-1 record) |

What this seat did **not** do: run either claim counter or the A2 gate. Re-derivation is owned by
`ReceiptReverify`, `GateReverify` and `ReportGateVerify`; their receipts are cited as fill sources, never
guessed at.

### 0b. State moved under this seat (measured at final read, 2026-11-03)

The lane advanced while this seat drafted. Final read: `git -C L rev-parse HEAD` → `27f649f8`
("round-68 attempt 2: freeze A3 (capability-table completeness gate + red receipt)"), and the working
tree carried six modified tracked files — none of them this seat's:

| path | state at final read |
|---|---|
| `plans/round-68-claims.md` | +13 lines uncommitted: `## Amendment A4` — erratum on A2's seat arithmetic (12 seats; "attack roles 4/12 = 33 % (>= 25 %)"; round total 24) |
| `corpus/lessons/round-68.md` | table merged (blank line gone), orphan paragraph `:68–77` deleted, five attempt-2 rows added (report-contract-omission, record-shape-drift, registry-incompleteness, registry-status-drift, capability-table-omission) |
| `SCORECARD.md` | four capability rows appended (`offline-network-service-…`, `offline-db-state-…`, `offline-torch-tensor-…`, `offline-torch-pipeline-…`) |
| `SKILL.md` | `round66_c1_tensor_probe` registry row appended |
| `corpus/SOURCES.md` | S240 status `queued` → `mined` |
| `plans/round68_capability_table.py` | T3 path extraction changed after the A3 freeze commit (finding 4) |

A3 (committed at `27f649f8`): `plans/round68_capability_table.py` plus the red-before receipt
`.ufo/waves/round-68/w2/capability-table/red-before.txt` (`MISMATCH n=4`, `PREDICATE R68-A3 fail`,
rc 1). At final read the green receipt `…/capability-table/green.txt` existed but was **untracked**
(`T1..T4 ok n=0`, `MISMATCH n=0`, `PREDICATE R68-A3 pass`, rc 0; appended selftest
`SELFTEST n=5 red-refused=4 green-ok=1`, rc 0), and the four rows it scored were uncommitted.

Consequence: §1's rows were integrated in close form by the L1 (its record-shape-drift row folds my rows
2–3 and records A4), so §1 is now a reconciliation note; §§3–4 carry A3 and A4; §6 re-numbers the
findings.

---

## 1. DRAFT — lesson `## Mistakes` attempt-2 rows

<!-- PASTE-BEGIN: rows 1–2 are required by the seat brief; rows 3–4 are grounded extras the L1 may drop -->
<!-- Integration: delete `corpus/lessons/round-68.md:64` (the blank line that splits the table) and
     `:68–77` (the orphan paragraph — fully covered by the `:65` mechanism-attribution row), then append
     these rows directly after the `:67` counter-under-enforcement row, with no blank line between. -->

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| report-contract-omission (report filed with no `## SHONEN` and no `## Trend verdicts`) | the filed round report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-68/kengaku.md` (sha256 `0399cd5376d27e1c006075929a9b3511c820fc326b4a3751a4cd9b78b8573839`, 12415 B; byte-identical to `.ufo/waves/round-68/w2/report-fixtures/attempt1-report.md`) carries seven `##` sections and neither required heading (`grep -c '^## SHONEN'` → 0, `grep -c '^## Trend verdicts'` → 0); the driver's content check therefore failed — `lane-dead-no-report kengaku round=68`, `.ufo/watchdog.log:2132` (2026-11-03T20:20:14-03:00), whose message names the failing arm `report_of (missing, unchanged, no SHONEN heading, or < 400B)`; the fleet report commit is `a7575677` (named by `plans/round-68-claims.md` Amendment A2 item 1) | the driver's `report_of` at return (`scripts/shokunin-watchdog.sh:184–206`, `MIN_REPORT_BYTES` 400 at `:54`); the prompt's pre-report gate `grep -c '^## SHONEN' <report>` (must print 1) would have read 0 — attempt 1 did not run it; no lane-side executable check for the report shape existed | `plans/round68_report_contract.py` (Amendment A2 item 3; committed `7803bdd4`, sha256 `18fbfc21…`, 10242 B): S1 six headings exactly once in order, S2 one checklist line per `SHONEN.md` box, S3 the three trend verdicts; as frozen in A2 item 3, its `--selftest` refuses the attempt-1 bytes on S1/S2/S3 and prints `SELFTEST n=5 red-refused=4 green-ok=1` (the attempt-2 measured rc and tally are `ReportGateVerify`'s) |
| record-shape-drift (the lesson's own `## Mistakes` table split, and a finding restated as orphan prose outside it) | `corpus/lessons/round-68.md:64` is a blank line that splits the table after the number-drift row (so `:62–63` and `:65–67` render as two tables), and `:68–77` restates the `:65` mechanism-attribution row as a paragraph outside the table — same `w1/SourcesRows/S240-receipt.md` §A–§B pointer, same "same wrong-source-memory family … a mechanism sentence, not a sha" conclusion; a naive `grep -c '^| '` reads 6 lines = header + separator + 4 rows while the record holds 5 findings | ScribeAttempt2 (this seat), reading the file for the attempt-2 draft; no gate checks a lesson file's shape — the A2 gate checks the round report, not `corpus/lessons/` | the L1 integrates: delete `:64` and `:68–77` so the table renders as one 5-row table of distinct findings; a lesson-shape gate is not proposed this round (nothing installed after data) |
| number-drift (the attempt-2 amendment's own seat arithmetic) | `plans/round-68-claims.md` Amendment A2 item 4 states "ONE v1 wave, 10 seats (`.ufo/waves/round-68/w2-spec.json`) … Attack roles reviewer 2 + critic 1 + mutation-tester 1 = 4/10 = 40 % … The round total is w1 12 + w2 10 = 22 seats"; the committed spec (sha256 `dfc1b865…`, tracked at `7803bdd4`) has 12 items and `maxLanes 12`, and the round's own classification (round shape, claims doc top: reviewer, critic, mutation-tester, sentinel, revenger, scout) makes the attack-role seats 6/12 = 50 % (reviewer 2, critic 1, mutation-tester 1, sentinel 1, scout 1); the round total is 12 + 12 = 24 | ScribeAttempt2 (this seat), reading the spec to draft the wave paragraph; nothing failed — the policy band (8–16) and the role list pass either number, so no gate caught the drift | recorded in the attempt-2 LOG and SCORECARD addendum with the dispatched counts; the frozen amendment is not edited (a count, not a predicate: no vector, counter, case or kill rule moves) |
| registry-incompleteness (`round66_c1_tensor_probe` never got a registry row; absent at `27f649f8`, appended in the working tree during attempt 2) | the `## Gate/probe registry` section (`SKILL.md:587` onward) holds 146 rows and 0 mentioning `round66_c1_tensor_probe` (`awk '/^## Gate\/probe registry/,0' SKILL.md \| grep -c 'round66_c1_tensor_probe'` → 0); the only file-wide mention is the `process-environment` class row's evidence cell at `SKILL.md:81`, which is not a registry row (`.ufo/waves/round-68/w1/RegistryRows.md` finding 2; carried in `SCORECARD.md` §Round 68 "Planned (round 69)" item 3) | RegistryRows (w1 scribe) — and the whole-file `grep -c` reads 1 because of the `SKILL.md:81` citation, the same mis-anchor trap its finding 3 records | carried to round 69 as a registry row for `plans/round66_c1_tensor_probe.py` (flags taken from the committed argparse, per w1 finding 1's precedent); the class row's citation is not a substitute for a row |

Row notes (not for paste):

- Row 1's driver attribution is deliberately narrow. The attempt-1 report **passes** the two other arms
  I could measure — it exists at 12415 B ≥ `MIN_REPORT_BYTES` 400 — so the failing arm is the SHONEN
  marker. `## Trend verdicts` is the lane contract's own S3 arm; **no driver checks it**, which is why
  the lane needed an executable check of its own (the A2 gate) rather than a restatement of the driver's
  regex. The digest-vs-baseline arm was not inspected by this seat (fleet `.ufo/state` is out of scope).
- Row 2's "orphan" is not a second finding: it repeats `:65` verbatim in substance. Deleting `:68–77`
  loses nothing; keeping it double-counts the mechanism-attribution mistake.
- Rows 3–4 are attempt-2 finds, not round-67 carry-overs. If the L1 prefers to route row 3 as a
  "conflict" in the report and the LOG instead of a Mistakes row, the text above already carries the
  numbers; it must not be dropped silently (it is the only record that the frozen amendment's seat
  arithmetic disagrees with the dispatched wave).
- Row 4 is carried, not fixed: fixing it would edit `SKILL.md` after the round's data, which no seat may
  do without a claim (the L1's integration did append the row — see the status bullet).
- **Status at final read: the L1 integrated rows of this shape** — five attempt-2 rows, the blank line and
  the orphan paragraph deleted, `SKILL.md` gaining the `round66_c1_tensor_probe` registry row and
  `corpus/SOURCES.md` flipping S240 `queued` → `mined`. This section therefore stands as the reconciliation
  note: the integrated record-shape-drift row folds my rows 2–3 together and records A4's seat-count
  correction, but its fix cell states the attack share as "4/12 = 33 %" — under the round's own attack-seat
  definition (reviewer, critic, mutation-tester, sentinel, revenger, scout) it is 6/12 = 50 %. See finding 1;
  the figure, not compliance, is what disagrees.
- **New since this draft: Amendment A4** (uncommitted at final read) corrects A2's seat count to 12 and the
  round total to 24 and changes no predicate, vector, counter, case, kill rule or target. It carries the
  seat-count half of row 3; row 3's remaining value is the denominator and the attack-share definition.

---

## 2. DRAFT — lesson `## Gate` S240 re-open line (attempt 2)

<!-- PASTE-BEGIN: append after `corpus/lessons/round-68.md:49`, i.e. after the S240 ADMITTED bullet and
     before the `**Admitted rows this round:**` summary at :51. -->

- **S240 — RE-OPENED (attempt 2, 2026-11-03).** URL
  https://raw.githubusercontent.com/urllib3/urllib3/2.7.0/src/urllib3/connection.py ·
  accessed 2026-11-03, attempt 2 (<scout: HTTP status>; <scout: byte count> bytes; sha256
  `<scout: sha256>`; capture `w2/SourceReopen/connection.py`).
  Row's stated values re-checked against the fetch: sha256
  `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532` and 42786 bytes →
  <scout: match | mismatch, with the measured value>. Located quote:
  `<scout: located quote, ≤25 words>` — `<scout: line>`, inside `<scout: def/class and line>`.
  Row shape: <scout: 11 columns parse / tier / scope / status `mined` / opened / recheck 180d>;
  `used-by` `<scout: knowledge path>` → <scout: exists | dangling>. Census: <scout: 232 rows →
  measured count, W-warnings, rc>. Row verdict: <scout: stands as written | defect, named>.
- **S240's rejected CPython row — RE-CHECKED (attempt 2, 2026-11-03).**
  https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/http/client.py ·
  <scout: HTTP status> · <scout: byte count> bytes · sha256 `<scout: sha256>` · capture
  `w2/SourceReopen/client.py`; `class HTTPConnection` defines no `__repr__`/`__str__` →
  <scout: confirmed | refuted>; the file's only `def __repr__` is at `:1559`, inside
  `class IncompleteRead` (`:1554`) → <scout: confirmed | refuted>. The rejection stands; the admitted
  row remains the urllib3 2.7.0 renderer.

Fill source: `.ufo/waves/round-68/w2/SourceReopen.md` (its §2–§6). Do not fill from the attempt-1 Gate
block above: the brief requires attempt-2 re-open measurements, and the registry row's itself stated
values are the comparison target, not the measurement.

---

## 3. DRAFT — SCORECARD attempt-2 addendum

<!-- PASTE-BEGIN: append at the end of `SCORECARD.md`, after the Round 68 `**Planned (round 69)**`
     paragraph (the file's current last line), so the addendum sits inside the Round 68 block and
     before any Round 69 section. -->

### Round 68 attempt 2 addendum (2026-11-03)

Attempt 2 is a resume of the same frozen round, not a new one: no predicate, counter, case table,
vector, kill rule or target changed (Amendments A2 item 2, A3 item 3, A4), and attempt 1's lane landing
stays `0e52fb5d` (freeze `a8883187`, arg fix `d5b3c309`). Two lane-side instruments were frozen in
attempt 2: the report-contract gate (`7803bdd4`, `.ufo/waves/round-68/w2-spec.json` sha256 `dfc1b865…`,
12 seats) and, after a self-assessment finding during the re-derivation, the capability-table gate
(`27f649f8`); Amendment A4 corrects A2's seat count to 12 and the round total to 24. Attempt 2 re-derived
both predicates on the committed bytes rather than re-scoring them.

| re-derived | command | attempt-2 result | receipt |
|---|---|---|---|
| R68-C1 | `python3 plans/round68_c1_pypi_finish.py --check-receipt corpus/evidence/round68/pypi/receipt.txt` | <ReceiptReverify: `PREDICATE R68-C1 pass`, rc 0> | `.ufo/waves/round-68/w2/ReceiptReverify/receipt-check.txt` |
| R68-C1 selftest | `python3 plans/round68_c1_pypi_finish.py --selftest --work <scratch> --green-receipt corpus/evidence/round68/pypi/receipt.txt` | <ReceiptReverify: `red_refused=… green_ok=…`, rc> | `.ufo/waves/round-68/w2/ReceiptReverify/selftest.txt` |
| R68-C1 clause review | adversarial clause-by-clause read of `check_receipt` against the frozen sentence | <ReceiptReview2: every clause implemented as written? findings> | `.ufo/waves/round-68/w2/ReceiptReview2.md` |
| R68-C2 | `python3 plans/round68_c2_correction_gate.py` | <GateReverify: `E1..E5 ok`, `DEFECTS n=0`, `PREDICATE R68-C2 pass`, rc 0> | `.ufo/waves/round-68/w2/GateReverify/green.txt` |
| R68-C2 selftest + E1 liveness | `python3 plans/round68_c2_correction_gate.py --selftest --work <scratch>`; fake-root duplicate-heading fixture | <GateReverify: `defects-in-fake=5 want=5 all-fail=True`; duplicate refuses> | `.ufo/waves/round-68/w2/GateReverify/selftest.txt` |
| anchors re-counted | `grep -c '^## Erratum (round 68)' plans/round-67-claims.md`; `grep -c 'ERRATUM-68' corpus/evidence/round67/pipe/a1-mutants.txt`; `test -e corpus/evidence/round68/r67-probe-selftest.txt`; `grep -c 'round67_c1_pipeline_probe' SKILL.md`; `grep -c 'executed 2 of 8' SKILL.md`; `grep -cE '^\|[[:space:]]*S240[[:space:]]*\|' corpus/SOURCES.md` | <GateReverify/CensusAudit: 1 / 1 / exists / 2 / 1 / 1> | `.ufo/waves/round-68/w2/GateReverify/…`, `.ufo/waves/round-68/w2/CensusAudit.md` |
| R68-A2 red | `python3 plans/round68_report_contract.py .ufo/waves/round-68/w2/report-fixtures/attempt1-report.md --shonen SHONEN.md` | <ReportGateVerify: `PREDICATE R68-A2 fail`, rc 1, S1/S2/S3 defects> | `.ufo/waves/round-68/w2/ReportGateVerify/red-attempt1.txt` |
| R68-A2 selftest | `python3 plans/round68_report_contract.py --selftest --work <scratch>` | <ReportGateVerify: `SELFTEST n=5 red-refused=4 green-ok=1`, rc> | `.ufo/waves/round-68/w2/ReportGateVerify/selftest.txt` |
| R68-A2 green | gate on a compliant skeleton built by the seat | <ReportGateVerify: `DEFECTS n=0`, `PREDICATE R68-A2 pass`, rc 0> | `.ufo/waves/round-68/w2/ReportGateVerify/…` |
| R68-A2 mutation | >= 8 single-check deletions of the gate, each scored on its own selftest and on the attempt-1 fixture | <GateMutate: `n=… survived=…`> | `.ufo/waves/round-68/w2/GateMutate.md` |
| R68-A3 | `python3 plans/round68_capability_table.py --lane .` | red: `MISMATCH n=4`, `PREDICATE R68-A3 fail`, rc 1 (committed `27f649f8`) → <L1: green `MISMATCH n=0`, `PREDICATE R68-A3 pass`, rc 0> | `.ufo/waves/round-68/w2/capability-table/red-before.txt`, `…/green.txt` |
| R68-A3 selftest | `python3 plans/round68_capability_table.py --selftest --work <scratch>` | <L1: `SELFTEST n=5 red-refused=4 green-ok=1`, rc 0> | the appended selftest block in `…/capability-table/green.txt` |
| registry + census | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`; row/SKILL counts | <CensusAudit: rc 0, W-warnings, row count, findings> | `.ufo/waves/round-68/w2/CensusAudit.md` |
| S240 re-open | live re-fetch of the admitted and the rejected URLs | <SourceReopen: sha/anchor/row verdict> | `.ufo/waves/round-68/w2/SourceReopen.md` |
| cross-lane overlap | term scan of the sibling lane repos | <SiblingOverlap: n term-level, n surface-level> | `.ufo/waves/round-68/w2/SiblingOverlap.md` |

**The A2 gate (`plans/round68_report_contract.py`, `7803bdd4`, sha256 `18fbfc21…`, 10242 B).** Frozen
before its data as Amendment A2 item 3. Six checks: S1 six headings exactly once and in order (`:80`),
S2 exactly one checklist line per `SHONEN.md` box, matched by the box's first five normalized words
(`:96`), S3 `expansion:`/`quality:`/`discernment:` each carrying one of the four verdict words (`:107`),
S4 ≥ 2 measurement table rows, every row carrying a backticked token or a ≥ 7-hex commit (`:116`), S5 the
five literal sentinels named at `:45` (`:133`), S6 ≥ 400 bytes and ≥ 3 `##` sections (`:138`) — the
driver's 400 B size floor plus a section count. The red fixture is the attempt-1 report bytes themselves
(`.ufo/waves/round-68/w2/report-fixtures/attempt1-report.md`, sha256 `0399cd53…`, 12415 B, 0 `## SHONEN`,
0 `## Trend verdicts`), committed in the same freeze commit as the gate (`7803bdd4`); A2 item 3 states
the bytes were copied before the gate was written, and the fixture's sha256 equals the filed fleet
report's own bytes, so the red input is the real failure rather than a synthetic one. Selftest tally and
mutation survival are the `ReportGateVerify` and `GateMutate` receipts above.

**The A3 gate (`plans/round68_capability_table.py`, frozen `27f649f8`).** A3 is not a new claim: it is
the correction of a measured self-assessment drift — the `## Capabilities` table stopped at round 51 while
round sections 64–68 each said their capability "enters". Four checks: T1 exactly one row per declared
capability, T2 the first-working-round cell names the declaring round, T3 the evidence cell carries a
backticked `plans/…`/`corpus/…` path that exists, T4 no duplicate capability name. Red (committed):
`MISMATCH n=4`, `PREDICATE R68-A3 fail`, rc 1
(`.ufo/waves/round-68/w2/capability-table/red-before.txt`); green: <L1: `MISMATCH n=0`,
`PREDICATE R68-A3 pass`, rc 0> (`…/capability-table/green.txt`, untracked at this seat's final read);
selftest <L1: `SELFTEST n=5 red-refused=4 green-ok=1`, rc 0>. Record note: the green receipt carries no
gate sha (unlike the C1 receipt's `PROBE` line), so it cannot be tied to the frozen bytes, and the working
tree's counter differs from `27f649f8` in T3 (finding 4). Resolve before the green receipt is committed.

**Verdicts unchanged.** R68-C1 pass and R68-C2 pass stand as landed at `0e52fb5d`, re-derived on the
committed bytes in attempt 2 (<ReceiptReverify: rc>, <GateReverify: rc>). Scores carry the attempt-1
values on the attempt-1 arguments: coverage 7 (held; L0 cap `kengaku | round-25/33/51`), calibration 10
(held, exercised — the round's own report-contract omission is recorded as a mistake row, not smoothed,
and the A2 gate is the executable correction of it), operability 10 (held; exercised — the two new gates'
red/selftest/green/mutation receipts are attempt-2 instruments), depth 10 (held; the capability table
gains the four rows the round sections already claimed — a table correction, not a new capability, and the
class row stays `executed 2 of 8`; the SKILL registry gains the `round66_c1_tensor_probe` row its absence
should have carried), freshness 10 (held; S240 re-opened live by
`SourceReopen` on 2026-11-03 and its row verdict is <SourceReopen: stands | defect>), adjacency 9 (held;
<SiblingOverlap: no surface-level hit>), novelty 8 (held). Attempt 2 adds no capability and moves no
claim; the L1 must not raise an axis for re-derivation alone.

**Record corrections integrated with this addendum.** `corpus/lessons/round-68.md` `## Mistakes` gains
the attempt-2 rows (report-contract-omission, record-shape-drift, registry-incompleteness,
registry-status-drift, capability-table-omission) and loses the blank line at `:64` and the orphan
paragraph at `:68–77`; the `## Gate` block gains the S240 re-open bullet; `SKILL.md` gains the
`round66_c1_tensor_probe` registry row and `corpus/SOURCES.md` flips S240 `queued` → `mined`. The seats are
recorded at their dispatched values — 12 seats, round total 24 (Amendment A4, which supersedes A2 item 4's
"10 seats" / "22 seats") — and the attack-role figure is stated with its definition: 4/12 = 33 % under A4's
narrower list (reviewer 2, critic 1, mutation-tester 1), 6/12 = 50 % under the round's own attack-seat list,
which also counts the sentinel and the scout. The record must not carry an unattributed ">= 25 %" floor: no
attack-share floor exists in `scripts/hyaku/ufo-wave-policy.json`, `ufo-wave-policy-v2.json` or
`wave-slot.sh` (grep `attack` → 0 in all three).

**Named limitations of the A2 gate (found this attempt, not patched after data).** (i) S5 refuses five
literal sentinels only (`plans/round68_report_contract.py:45`); an unresolved `<seat: …>` fill marker
passes the gate, so a green gate is not proof that the report's numbers are resolved. (ii) S2 matches a
box by its first five normalized words as a prefix, so an honestly reworded box label fails the gate —
the report must quote `SHONEN.md`'s labels, not paraphrase them. (iii) S1 requires the literal line
`## SHONEN`; the driver's regex accepts any `#+` level and a trailing non-word byte, so a report can
satisfy the driver and still fail A2 — deliberate, but it means the two checks are not interchangeable.
(iv) The gate checks the report's shape, never its truth: it does not open a receipt, a sha or a claim.

**L0 carried (lines still present in `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`; none answered).**
`kengaku | round-25 :72`, `round-33 :163`, `round-51 :200`, `round-54 :213–214`, `round-56 :250–251`,
`round-63 :259`, `round-65 :270`, `round-66 :276`, `round-67 :280–281`. Note: attempt 1's list omitted
`round-65` (`.ufo/l0-questions.md:270`), which the file still carries; it is listed here so the carry
matches the file rather than the prior summary.

---

## 4. DRAFT — LOG.md round-68 attempt-2 entry

<!-- PASTE-BEGIN: append at the end of `LOG.md`, after the attempt-1 entry's `**Erratum-68 note.**`
     bullet (current last line 2553). Headings and bullets follow the attempt-1 entry's house shape. -->

## Round 68 attempt 2 (2026-11-03)

- **Resume cause.** Attempt 1 landed the lane work (freeze `a8883187`, arg fix `d5b3c309`, landing
  `0e52fb5d`, all pushed) but the report it filed carried no `## SHONEN` marker, so the driver's
  `report_of` content check failed (`lane-dead-no-report kengaku round=68`, `.ufo/watchdog.log:2132`,
  2026-11-03T20:20:14-03:00) and the round relaunched as attempt 2. Amendment A2 (dated, same claims doc)
  records the cause and freezes the new report-contract gate; no predicate, vector, case table, kill rule
  or target changed (A2 item 2).
- **Frozen claims (unchanged).** R68-C1 (coverage, L0-capped at 7; capability
  `offline-network-service-grader-probe`) and R68-C2 (calibration, held at 10; the round-67 closure's five
  routed defects as dated corrections), exactly as frozen at `a8883187`/`d5b3c309`; attempt 2 re-derives
  both on the committed bytes and does not re-score.
- **Landed (R68-A2).** `plans/round68_report_contract.py` (10242 B, sha256 `18fbfc21…`) committed at the
  attempt-2 freeze `7803bdd4`, with its red fixture
  `.ufo/waves/round-68/w2/report-fixtures/attempt1-report.md` (the attempt-1 report bytes, sha256
  `0399cd53…`, 12415 B, 0 `## SHONEN`, 0 `## Trend verdicts`) and the 12-seat wave spec
  (`.ufo/waves/round-68/w2-spec.json`, sha256 `dfc1b865…`). Gate checks S1–S6 (headings in order; one
  checklist line per `SHONEN.md` box; the three trend verdicts; ≥ 2 evidence-pointed measurement rows;
  placeholders; the driver's 400 B floor plus a `##` section count). Red: <ReportGateVerify: `PREDICATE R68-A2 fail`,
  rc 1, S1/S2/S3 defects> (`.ufo/waves/round-68/w2/ReportGateVerify/red-attempt1.txt`). Selftest:
  <ReportGateVerify: `SELFTEST n=5 red-refused=4 green-ok=1`, rc>. Green skeleton:
  <ReportGateVerify: `PREDICATE R68-A2 pass`, rc 0>. Mutation: <GateMutate: `n=… survived=…`>. Sentinel:
  <SecurityScan: verdict>.
- **Landed (R68-A3).** `plans/round68_capability_table.py` (frozen `27f649f8`) closes a self-assessment
  drift found during the re-derivation: the `## Capabilities` table stopped at round 51 while rounds 64–68
  each said their capability "enters". Checks T1–T4 (one row per declared capability; first-working-round
  cell names the declaring round; evidence cell carries an existing backticked `plans/…`/`corpus/…` path;
  no duplicate name). Red `MISMATCH n=4`
  (`.ufo/waves/round-68/w2/capability-table/red-before.txt`) → green <L1: `MISMATCH n=0`,
  `PREDICATE R68-A3 pass`, rc 0> (`…/capability-table/green.txt`); selftest <L1: `SELFTEST n=5
  red-refused=4 green-ok=1`, rc 0>; four rows appended to `SCORECARD.md` with their first-working rounds
  and re-derivable evidence commands. Record note: the green receipt carries no gate sha and the working
  tree's counter differs from the frozen bytes in T3 — reconcile before committing the green (finding 4).
- **Re-derivation (attempt 2).** R68-C1 `--check-receipt` on the receipt of record:
  <ReceiptReverify: `PREDICATE R68-C1 pass`, rc 0> (`w2/ReceiptReverify/receipt-check.txt`); probe
  `--selftest`: <ReceiptReverify: `red_refused=… green_ok=…`>; R68-C2 gate: <GateReverify: `E1..E5 ok`,
  `DEFECTS n=0`, `PREDICATE R68-C2 pass`, rc 0> (`w2/GateReverify/green.txt`), selftest
  <GateReverify: `defects-in-fake=5 want=5 all-fail=True`>, E1 exactly-one liveness
  <GateReverify: duplicate refuses>; anchors re-counted <GateReverify: 1 / 1 / exists / 2 / 1 / 1>;
  census <CensusAudit: rc 0, W-warnings, 232 rows>; S240 re-opened <SourceReopen: sha/anchor/row verdict>
  (`w2/SourceReopen.md`); cross-lane overlap <SiblingOverlap: n term-level, n surface-level>.
- **Wave w2.** v1, 12 seats (executor 4, scout 1, reviewer 2, critic 1, mutation-tester 1, scribe 1,
  connector 1, sentinel 1), connector 1 (≤2); <wave: N of 12 settled with reports,
  `.ufo/waves/round-68/w2-results.json`>. Amendment A4 (uncommitted at this seat's read) supersedes A2 item
  4's seat count: 12 seats, round total 24. Attack share stated with its definition — 4/12 = 33 % under A4's
  list (reviewer 2, critic 1, mutation-tester 1), 6/12 = 50 % under the round's own attack-seat list (which
  also counts the sentinel and the scout); no attack-share floor exists in the wave policy files, so A4's
  ">= 25 %" is stated with its source or dropped.
- **Record (attempt-2 integration).** `corpus/lessons/round-68.md` `## Mistakes` gains the attempt-2 rows
  (report-contract-omission, record-shape-drift, registry-incompleteness, registry-status-drift,
  capability-table-omission) and loses the blank line at `:64` plus the orphan paragraph at `:68–77`; the
  `## Gate` block gains the S240 re-open bullet (attempt-2 measurements); `SKILL.md` gains the
  `round66_c1_tensor_probe` registry row; `corpus/SOURCES.md` flips S240 `queued` → `mined`; `SCORECARD.md`
  gains the attempt-2 addendum and the four capability rows. No claim, case table, vector, kill rule or
  target is touched; A4 is the only amendment added to the claims doc in attempt 2 after A2/A3.
- **Verification run this attempt.** The L1's pre-report gate
  `python3 plans/round68_report_contract.py .ufo/reports/round-68/kengaku.md --shonen SHONEN.md` must
  print `DEFECTS n=0` and `PREDICATE R68-A2 pass` (rc 0) before the report is filed — this is the check
  attempt 1 lacked. The A3 gate (`python3 plans/round68_capability_table.py --lane .`) must print
  `MISMATCH n=0` and `PREDICATE R68-A3 pass`, with its receipt committed and bound to the gate's sha. The
  report must also differ from the attempt-1 bytes (the driver's unchanged-digest arm). <L1: recorded rc
  of the pre-report gate runs and of the report's final check>.
- **Open.** L0 `kengaku | round-25/33/51`, `round-54`, `round-56`, `round-63`, `round-65`, `round-66`,
  `round-67` carried (lines at `SCORECARD.md` §Round 68 attempt-2 addendum). Named limitations carried:
  check-receipt provenance bound, kill-rule-(c) misstatement, K1/K3 stderr byte-drift across runs,
  base-probe SETUP typing (F7), and the new A2 limits (S5 sentinel list is literal; S2 quotes box labels
  verbatim; S1 is stricter than the driver's regex; the gate checks shape, not truth). Carried defects:
  the A3 green receipt is unbound to its gate bytes (finding 4); `round66_c1_tensor_probe`'s registry row
  was appended in attempt 2 (`SKILL.md`, working tree) so that carry is closed.

---

## 5. Integration checklist (L1; NOT for paste into the report)

1. Resolve every `<…>` marker from the named receipt before the text enters an L file. The A2 gate's S5
   refuses only the five literal sentinels at `plans/round68_report_contract.py:45`; an unresolved
   `<scout: …>` or `<GateMutate: …>` marker passes S5, so a green gate is not evidence that these drafts
   were filled. Keep the markers out of any file that goes to the fleet report.
2. Verdict guard. The addendum's "Verdicts unchanged" paragraph and the LOG's re-derivation bullets are
   drafts, not results: if any seat's re-derivation returns rc ≠ 0 or a defect, the frozen kill rules
   decide (C1 a–e, C2 a–c, A2 a–c) — paste the measured miss and the kill rule it fires instead of
   "unchanged", and do not narrow a check, edit a predicate or re-run until it passes. The only honest
   "unchanged" is one backed by the cited receipt.
3. Lesson edits are already in the working tree at this seat's final read (§0b): the blank line, the orphan
   paragraph and five attempt-2 rows. Do not re-apply §1 blindly — diff the working tree against §1 and keep
   the integrated text, correcting only the attack-share figure (finding 1); the A3 row
   (capability-table-omission) is already integrated. §2's Gate bullets are still to append after `:49`.
4. SCORECARD: the four capability rows are in the working tree; place the §3 addendum at the end of the
   Round 68 block (re-read the tail — the read-time line was 2954 and the file has moved). Cite the A3
   green only after that receipt is bound to bytes (item 5).
5. A3 reconciliation (finding 4). Either land the T3 edit under a dated amendment naming the old and new
   clause and why the frozen T3 could not read a backticked command, or revert the file to `27f649f8` and
   re-run the green; then commit `green.txt` with the gate's sha added, together with the four SCORECARD
   rows it scored. A green receipt that names no instrument cannot be re-derived.
6. A4 (uncommitted at this seat's read): land it with the attack-share figure qualified per finding 1, or
   drop the parenthetical and keep the seat count and round total.
7. Append the LOG entry after line 2553; the `LOG.md:2542` reference inside the existing number-drift row
   stays valid because the entry is appended, not inserted. Re-read the tail first (the file has moved).
8. The fleet report (`.ufo/reports/round-68/kengaku.md`) is the L1's, not this seat's. It must carry
   `## Work performed`, `## Landed changes`, `## Before → after measurements`, `## Sources & frontier`,
   `## Trend verdicts`, `## SHONEN` in that order, with one checklist line per `SHONEN.md` box quoting the
   box's first five words, and it must differ from the attempt-1 bytes. Run the A2 gate on it before
   filing, and record the rc in the LOG's "Verification run this attempt" bullet. Its landed-changes list
   must name both attempt-2 gates (A2 report contract, A3 capability table) and the A3 correction, or the
   report understates the round.
9. Do not edit `plans/round-68-claims.md`'s frozen sections, either claim counter, or any target. A4 is an
   append the L1 owns; the seat arithmetic is recorded there, not patched into A2.

---

## 6. Findings (reported, not edited)

1. **A2's seat arithmetic, and A4's fix of it.** A2 item 4: "10 seats", "Attack roles reviewer 2 + critic 1
   + mutation-tester 1 = 4/10 = 40 %", "w1 12 + w2 10 = 22 seats". Committed spec (`7803bdd4`, sha256
   `dfc1b865…`): 12 items, `maxLanes 12`; round total 24. Amendment A4 (uncommitted at this seat's final
   read) corrects the seat count and the round total — good — but keeps the narrow list: "attack roles
   4/12 = 33 % (>= 25 %)". Under the round's own attack-seat definition (claims doc round shape: reviewer,
   critic, mutation-tester, sentinel, revenger, scout) w2 has 6/12 = 50 %, counting the sentinel and the
   scout. And no attack-share floor exists in `scripts/hyaku/ufo-wave-policy.json`,
   `ufo-wave-policy-v2.json` or `wave-slot.sh` (`grep -c attack` → 0 in each), so the "(>= 25 %)" has no
   locatable source. Compliance is not in doubt under either count; the record should carry the definition,
   not the bare fraction.
2. **Attempt 1's driver failure was the SHONEN arm alone.** Measured: the filed report is 12415 B (≥ 400)
   and exists; `grep -c '^## SHONEN'` → 0. `## Trend verdicts` is the lane's contract arm (A2 S3), which no
   driver checks — so the executable fix had to be lane-side, and the lesson row says so instead of
   overstating the driver's check.
3. **The lesson file's `## Mistakes` table was split and double-counted one finding.** Blank line at `:64`;
   orphan restatement at `:68–77` of the `:65` row. Both are deleted in the working tree (§0b); no gate
   checks lesson shape, so nothing will catch a recurrence.
4. **The A3 green receipt is not bound to the frozen gate bytes.** `green.txt` carries no gate sha (unlike
   the C1 receipt's `PROBE` line), and the working-tree counter differs from the freeze commit
   `27f649f8` in T3: `git diff -- plans/round68_capability_table.py` shows
   `tok.split()[0] … startswith(("plans/", "corpus/"))` replaced by `PATH_RE.findall(tok)` (a path is now
   extracted from inside a backticked command). So the green cannot be tied to the frozen predicate without
   a dated amendment naming the T3 change or a re-run on the frozen bytes. This is a provenance defect, not
   a verdict: nothing here shows the landed table failing. It is the only attempt-2 amendment-adjacent
   change to a counter, and no amendment names it.
5. **`round66_c1_tensor_probe` had no registry row at `27f649f8`** (146 registry rows, 0 matches; the only
   file-wide mention was the class row's evidence cell at `SKILL.md:81`). The working tree appends the row
   (whole-file `grep -c` → 2); the class-row citation was never a substitute, and the whole-file grep is not
   a safe anchor (w1 `RegistryRows.md` finding 3).
6. **Attempt-1's L0 carry list omitted `kengaku | round-65`** (`.ufo/l0-questions.md:270`), which the file
   still carries; the addendum's carry list includes it. No L0 line is assumed answered.
7. **A2/A3 gate limits worth naming before they are cited as the report standard.** A2: S5 is a five-literal
   sentinel scan (unresolved fill markers pass), S2 requires quoted box labels (first five words), S1 is
   stricter than the driver's regex, and the gate checks shape, never truth. A3: the receipt format has no
   sha line, so any A3 receipt is unbindable by construction — fix the format before round 69 relies on it.
8. **What moved and what did not.** C1, C2 and A2 counter bytes are unmoved (`git status --porcelain` lists
   no path under `corpus/evidence/round68/` or `plans/round68_c1_pypi_finish.py` / `round68_c2_correction_gate.py` /
   `round68_report_contract.py`); A3's counter moved after its freeze commit (finding 4). So the sentence
   "no predicate, counter, case, vector, kill rule or target changed" (A2 item 2, A4) is true of the two
   claims and of A2, and needs the A3 qualifier to be true of the round.

---

## 7. Out of scope / not done

- No gate or counter was run by this seat; the receipts cited are other seats' and the L1's
  (`ReceiptReverify`, `GateReverify`, `ReportGateVerify`, `GateMutate`, `SourceReopen`, `CensusAudit`,
  `SiblingOverlap`, `SecurityScan`, `ReceiptReview2`, `ClaimFalsify2`, `EvidenceIndex`, and the A3
  red/green pair under `.ufo/waves/round-68/w2/capability-table/`). Every value here that depends on a
  run is a fill marker, except the bytes this seat read directly (§0, §0b).
- No L file edited by this seat (claims, lesson, SCORECARD, LOG, SKILL, SOURCES, receipts all untouched by
  ScribeAttempt2 — the working-tree changes documented in §0b belong to the L1 and other seats); no
  fleet-root file written; no git/jj mutation; no install; no subagent; no listener on 8080 or 12355.
- Scratch root `/fast/scratch/hyaku/kengaku-r68/ScribeAttempt2` was created and removed in this seat;
  nothing is left on disk (`rm -rf` executed, `test -e` false). No scratch was needed: this seat only
  read.
- Not verified by this seat (and not claimed): the numeric results in every fill marker, the wave's final
  settled count, the A3 green (read as bytes only, not run), and the state of the fleet report the L1 will
  write.
