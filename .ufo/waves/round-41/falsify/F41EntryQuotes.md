# F41EntryQuotes — sentence-level support check of the TB2 `constraints-scheduling` entry

Seat: F41EntryQuotes (critic, leaf). Lane tip `3d0058fbde484c9d6c23fd997d9ee09a0663bcdb`, 2026-10-26, ~16:25.
Target: `corpus/knowledge/tb2-constraints-scheduling-grader.md`.
Support surfaces: receipt `corpus/evidence/round41/constraints-probe.txt` (25 cases, lines 7–33), captures
`corpus/evidence/round41/tb2-constraints-scheduling/` (`test_outputs.py` 209 lines, `test.sh`, `Dockerfile`,
`instruction.md`, `solve.sh`, three calendars; `SHA256SUMS`), probe `plans/constraints_probe.py`, wave-1 reports in
`.ufo/waves/round-41/build/`.

Scope: every factual sentence/claim unit in §Summary (15 units), §What is graded (8 table rows + 5 bullets),
§Findings (11 findings, ~45 sentences), §Corrections (7 items, ~14 sentences); plus verbatim verification of the 29
rows of §Located quotes.

Method — all read-only, nothing written to the lane:
- the captured grader was imported with `sys.dont_write_bytecode = True` and its `_hard_ok`/`_overlap` used to
  enumerate every minute of Jan 15–19;
- the three test functions were called with `_r`/`_repo` replaced by in-memory strings, so no `/app`, no files, no
  sandbox write (this is why no bwrap envelope was needed: no battery, counter or fixture was run);
- the package gate's own `P3`/`P4` clauses were executed in-process against `plans/pkg-spec-r41.json`
  (`entry: corpus/knowledge/tb2-constraints-scheduling-grader.md`, 29 parsed quotes);
- line-ending facts measured with `tr -cd '\r' | wc -c`.

One residue note: `corpus/evidence/round41/tb2-constraints-scheduling/__pycache__/test_outputs.cpython-314.pyc`
appeared at 16:15:05. My imports ran with bytecode writing disabled; peers are concurrently running the C2
counter/probe against the same captures, so I did not attribute it and did not delete it (deletion would be a write
outside my allowance). It is gitignored — `git status --porcelain` shows only the falsify paths. I made no other
write outside this report dir and `/fast/scratch/hyaku/kengaku-r41/F41EntryQuotes/` (RFC 5545 fetch only, deleted).

---

## A. §Located quotes — 29/29 verbatim; P3/P4 green

Command (parsed the table, compared each quote to the cited line of the cited capture; then the gate's clauses):

```
rows 29 words min/max 3 14 substring-ok 29 full-line-equal 28
P3 (True,  'rows=29 distinct_quotes=29 distinct_lines=29 out_of_word_range=0')
P4 (True,  'checked=29 bad=0 first=0')
```

- **Every quote is byte-exact on its cited `capture:line`.** 28 of 29 equal the whole stripped line; 1 is a
  byte-exact prefix: `instruction.md:10` (“Output: Create `/app/meeting_scheduled.ics` with a 1-hour "Team Planning
  Meeting"”) stops mid-line with no ellipsis. `pkg_gate.c_quote_verbatim` accepts substrings
  (`q.text not in "\n".join(...)`), so the entry's “verified … by the gate's `P4` clause” holds; the prefix is a
  presentation nit, not a false quote. No quote is outside 3–25 words.
- **Claim column:** 28 of 29 claims are supported by the quoted line. One is not — row 19, entry:134, “the buffer is
  fifteen minutes, inside that block only” ← `b1 = ee + timedelta(minutes=15)` (`test_outputs.py:206`): `:206` sits
  in the loop opened at `:202`, which is *outside* the `if` at `:192`. Same root as **W7** below.
- `_repo_input` really is defined and never called: `grep -c '_repo_input' test_outputs.py` → `1` (line 22 only), so
  “the defined-but-unused repo-input helper” holds.

## B. §Summary — 15 units: 3 wrong, 2 unsupported

Holds (evidence in parentheses):
- **S1 (entry:9-17)** “three pytest functions … all three required for the reward bit”: `test.sh:18-22`, `:25-29` read;
  the `_hard_ok` clause count is exact — nine `if` statements at `:59, :61, :63, :65, :69, :74, :77, :79, :81`, of
  which `:65` (Tue/Thu 16:30), `:69` (Carol 17:00), `:79` (duplicate of `:59`) and `:81` (18:00) cannot fire because
  `:61` returns `False` for any end after 14:00; the five live ones are `:59, :61, :63, :74, :77`.
- **S2 pins** “sha256 literals … equal the capture digests”: measured — all three capture digests are members of the
  grader's three literals (`capture_digest_in_grader_literals= True` ×3).
- **S3 (entry:22-25)** “exactly **two** 1-hour slots, Wed 17 Jan 11:00 and Thu 18 Jan 11:00”: enumerated with the
  captured `_hard_ok` + `_overlap` at one-minute steps —
  `valid slots: ['Wed 2024-01-17 11:00', 'Thu 2024-01-18 11:00'] count 2`. The probe's ground-truth paragraph is
  `plans/constraints_probe.py:29-31`; `solve.sh` scores both at 20 and sorts by time, so “must produce Wed 11:00”
  follows from its `PPP`.
- **items (1), (2), (3), (5)**: every case letter is the receipt's (`decoy-first` `PPP` receipt:14,
  `decoy-second` `PFF` :28, `bob-start-0900-wed` `PFP` :13, `wed-1059-overlaps-alice` `PFP` :23,
  `input-crlf-rewrite` `PPP` :31, `duration-90min` `FPP` :15).
- **S7** “new to the lane's executed grader sample”: the six earlier TB2 entries compare literals/checksums/substrings
  (README rows 68–73); none computes a verdict from a model over pinned inputs.
- **S9** “narrows … this one task only (7 of 89 read)”: the index row `corpus/README.md:269` and the §Frontier
  round-41 bullet `corpus/README.md:343-355` both say “narrowed for that one task only” and “7 of the 89”.

Defects: **W1, W2, W3, U2, U3** (table F).

## C. §What is graded — mechanism table holds except the Carol-buffer row

Verified against `test_outputs.py`: entry point `test.sh:18-22`; reward `:25-29` (1 iff exit 0); initial state
`Dockerfile:14` `COPY inputs/ /app/`; integrity `:88-96` (both branches decoded text); structure `:97-129`
(`strip()` header asserts, `findall` VEVENT split, first match `next(...)`, one `re.I` attendee line per email, 1 h,
Jan 15–19, weekday); constraints `:132-143`; earliest `:146-188` (minute scan from `Mon 09:00`, `Found earlier valid
slot`, same-minute Monday tie-break, unconditional `9 <= sched.hour < 12`).

The five “structural consequences” hold: only test 1 selects by summary+attendees (`:108-115`); tests 2–3 call
`_dt` on the whole file (`:135`, `:151`); `DTEND` is asserted once (`:127`) and recomputed (`:136`, `:191`);
integrity is a decoded-text compare; one unparameterised `DTSTART:(\d{8}T\d{6}Z)` with no unfolding step
(`:48`, `:125-126`, `:135`, `:151`).

**The Carol-buffer row (entry:89) is wrong as written** — see **W7**: `:190-209` contains two blocks, and only the
first is gated on the meeting's end; the second loop (`:202-209`) runs unconditionally.

## D. §Findings — 11 items: 6 carry a defect (5 wrong, 1 unsupported)

Letter-by-letter the receipt reproduces, and I re-derived the mechanism of the letters by calling the captured
functions with in-memory readers:

```
conflict-mon-1230   test_constraints_conflicts_business_hours FAIL ''
conflict-mon-1230   test_earliest_tiebreakers_and_carol_buffer FAIL "Prefer Alice's morning (9-12) when possible"
bob-start-0900-wed  test_constraints_conflicts_business_hours FAIL ''
bob-start-0900-wed  test_earliest_tiebreakers_and_carol_buffer PASS
wed-1059            test_constraints_conflicts_business_hours FAIL ''
wed-1059            test_earliest_tiebreakers_and_carol_buffer PASS
duration-90min      test_constraints_conflicts_business_hours PASS
duration-90min      test_earliest_tiebreakers_and_carol_buffer PASS
```

That last pair is finding 7's mechanism (`DTEND` ignored by tests 2–3) seen directly. Findings 1 (all three open
`:97`, `:134`, `:150`; receipt:7 records three `FileNotFoundError`s), 2 (slot table re-derived per day against the
calendars), 3 (order defect: test 1 reads the attendee block, tests 2–3 the first `DTSTART`), 5 (sha256 branch; probe
binds `/cap/test_outputs.py` — `plans/constraints_probe.py:202`, `:247-249`), 8 (clause audit), 10 (superset +
asymmetric case; wave-1 `lowercase-attendee-only` `PPP`) all hold.

RFC quotes in finding 6 check against RFC 5545: §3.1 `line 511` “When parsing a content line, folded lines MUST first
be unfolded”; §3.1 `line 476` fixes the CRLF content line; §3.8.2.4 `line 5425` “Property Parameters: IANA,
non-standard, value data type, and time zone identifier …”.

Defects in this section: **W4** (F2), **W5** (F4), **W6** (F6), **W7** (F9), **W9** (F8), **U1** (F11).

## E. §Corrections — 6 of 7 items trace; 1 pointer wrong

- (1) probe builders are LF: `plans/constraints_probe.py:95` (`HDR = "...\n..."`), `:109-118` (FOLDED/VALUE/LOWER
  built from `GOOD_ICS`); CRLF-conformant variants in `.ufo/waves/round-41/build/R41CritProbe.md:119-121`
  (`crlf-folded FPP`, `crlf-lowercase-summary FPP`, `crlf-value-datetime FFF`). RFC §3.1 CRLF at RFC 5545 line 476.
- (3) 11:05–12:05 invalid confirmed: `_hard_ok(Wed 11:05, 12:05)=False`, `any_overlap=True`.
- (4) Fri 15:00 rejects under both reading: `_hard_ok(Fri 15:00,16:00)=False`.
- (5)/(6) D5 and the lone-CR `3/3` are in `R41CritProbe.md:96-124`.
- (7) S124 closed/unmerged and the no-publication search are in `corpus/SOURCES.md:139` and
  `build/R41ScoutPriorArt.md:8,64-68`.
- **(2) is wrong in one clause** — **W8**.

---

## F. Counted defects

Quotes are ≤25 words. “Smallest correction” is what I would change, nothing else.

### Wrong (w = 9)

| ID | Entry | Sentence (abridged) | Evidence | Smallest correction |
|---|---|---|---|---|
| **W1** | §Summary, entry:25 | “Offline execution … reproduced the reward bit on 23 and was wrong on 2” | Receipt:33 `mismatches=2`; the two `match=NO` rows are receipt:10,18 with `predicted_tests=PPF tests=PFF`; the entry's own §Regrade (entry:298) calls them “**prediction** errors across runs … not regrade differences”. Nothing measures the execution as wrong. | “matched the frozen prediction on 23 and left 2 mismatches, both the pilot's prediction errors carried verbatim” |
| **W2** | §Summary, entry:17 | “The graded artefact is a one-event ICS file” | `decoy-first-vevent` is a two-VEVENT artefact, observed `PPP` (receipt:14) — the grader never checks the count (`:106-115`). The same wording recurs in the README §Frontier bullet (`corpus/README.md:347`) and needs the same fix. | “the graded artefact is an ICS file (the task asks for one event; the grader does not check the count)” |
| **W3** | §Summary (4), entry:41 | “while the task's own CRLF line breaks pass” | The task's own artefacts are LF: `tr -cd '\r' < solve.sh \| wc -c` → `0` (same for the three calendars, `instruction.md`, `test_outputs.py`), and `solve.sh:152-153` writes text mode → LF on the image; the frozen case itself says CRLF is “RFC 5545's own line break” (`plans/constraints_probe.py:174`). | “while RFC 5545's own CRLF line break passes” |
| **W4** | §Findings 2, entry:227-228 | “Carol's and Bob's 12-13 block 12:30” (applied to Wed and Thu) | Bob has no 12-13 on Thu: `bob_calendar.ics:45-46` is `20240118T130000Z/140000Z` (13-14); only Carol has Thu 12-13 (`carol_calendar.ics:45-46`). Measured: Thu 12:30–13:30 → `A=False B=True C=True` (Bob's 13-14, not a 12-13). | “Carol's 12-13 and Bob's 13-14 on Thu (Bob's 12-13 on Wed) block 12:30” |
| **W5** | §Findings 4, entry:244 | “yet every slot before it overlaps the same event” | Counterexample: Mon 11:00–12:00 has `_hard_ok=True`, `_overlap(…, alice)=False`, and does not overlap Alice's Wed 10–11 event (it is blocked by Bob's and Carol's 11–12). Wed 09:00–09:59 fail `_hard_ok` at `:63`, not the overlap. The conclusion still holds: computed earlier valid slots before Wed 10:59 = `0`. | “no slot before it passes both the model and the conflict test (Mon/Tue have no valid slot; Wed 09:00–09:59 fail Bob's bound, 10:00–10:58 overlap Alice's 10–11)” |
| **W6** | §Findings 6, entry:259 | “requires the exact-case `SUMMARY:`/`ATTENDEE:` names” | `rf"^ATTENDEE[:;].*{…}$", meeting, re.I \| re.M` (`:122`) is case-insensitive — finding 10 says so, correction 2 says the frozen description overstated, and the wave-1 `lowercase-attendee-only` state is `PPP`. Only `"SUMMARY:Team Planning Meeting" in b` (`:112`) is exact-case. | “requires the exact-case `SUMMARY:` name (`ATTENDEE:` is matched with `re.I`)” |
| **W7** | §What is graded entry:89, §Findings 9 entry:274, quote-claim entry:134 | “runs only when the meeting ends after 16:45 … so the inner assertion (`:207`) is never evaluated” | `:192` gates only the first block (`:193-200`). `:202-209` is unconditional; its gate is `:204` (a Carol `DTEND` ≥16:45). `:207` is inside that loop. Carol's latest `DTEND` is 14:00 (`carol_calendar.ics:28`), so `:204` never fires; no receipt case ends ≥16:45, so `:200` never runs either. Conclusion (“vacuous”) stands; the causal chain and the table row do not. | “`:200` is gated on an end after 16:45 (`:192`), `:207` on a Carol `DTEND` after 16:45 (`:202-204`); neither is evaluated in any receipt case (max Carol `DTEND` 14:00), so the buffer is vacuous” |
| **W8** | §Corrections 2, entry:412 | “finding 7 above already states the SUMMARY-only reading” | Finding 7 is “Duration is graded by one test only”; the SUMMARY-only/asymmetric reading is finding 10 (“`re.I`, `:122` … the summary match at `:112` is exact-case”). | “finding 10 above” |
| **W9** | §Findings 8, entry:271-273 | “a 12:30 start is accepted by the model and rejected by the overlap test alone” | `conflict-mon-1230` is `PFF` (receipt:12); measured, test 3 fails with `Prefer Alice's morning (9-12) when possible` — the unconditional `:188`, not the earliest scan. So two tests reject it, and the model-level half is true. | “accepted by the model; test 2 rejects it on the overlap check and test 3 on the unconditional morning assert (`:188`)” |

### Unsupported (u = 3)

| ID | Entry | Sentence (abridged) | Why unsupported | Smallest correction |
|---|---|---|---|---|
| **U1** | §Findings 11, entry:286 | “A valid 11:05 slot would be invisible to the oracle's grid” | No valid 11:05 exists on the pinned data: `_hard_ok(Wed 11:05, 12:05)=False`, `any_overlap=True` (Carol/Bob 12–13 and the lunch window) — exactly what §Corrections 3 says. The 30-minute grid (`solve.sh:112`) is coarser than the grader's minute rule, but no receipt case witnesses a missed *valid* slot. | mark it hypothetical (“on an input where a valid start is off the 30-minute grid …”) or drop the 11:05 exemplar |
| **U2** | §Summary, entry:44 | “(S122 is the same repository at the same commit)” attached to both named docs | True for `benchmark-verifier-execution-model.md` (S100 terminal-bench-2 @2fd12b88); false for `benchmark-grader-semantics.md`, whose sources are S093 (SWE-bench_Pro-os `66f92766`), S103 (Toolathlon `9be8d8fe`), S104 (arXiv) — no terminal-bench-2 source. | move the parenthetical onto the verifier-execution-model clause (or the six TB2 entries) |
| **U3** | §Summary, entry:51 | “not a new verdict channel (per-line regexes, interval arithmetic and a scan are old)” | `grep -rn "interval" corpus/knowledge/` returns only this entry; no earlier lane entry uses interval arithmetic as a verdict channel, and the six TB2 graders have no interval check. | cite where interval arithmetic is already old, or drop that item |

### Wording only, not counted (for the L1)

- §Findings 8: “`:79` is a byte-duplicate of `:59`” — the line differs by `  # Alice start`; the condition is identical.
- §Findings 6: “stricter … on three syntax points” — the case point is SUMMARY-only (same root as W6).
- §Summary (4): “RFC 5545-form forms fail” rests on LF witnesses; the CRLF-conformant evidence is a seat observation
  (`R41CritProbe.md:119-121`), disclosed by correction 1.
- Quote-claim row 3 (“the VEVENT split is the only structure the reader knows”) — the reader also asserts the header
  strings (`:98-103`).
- `instruction.md:10` quote is a prefix without an ellipsis (P4 accepts it).

## G. Adjacent observation (outside the four sections, but measured)

§Requirement map, entry:201: “only valid starts are 11:00, so **no receipt case separates the two readings**” of the
Alice-morning sentence. The measurement above contradicts it: `conflict-mon-1230` (Mon 12:30) fails test 3 with
`Prefer Alice's morning (9-12) when possible`. Under a tie-breaker reading the same-minute candidate set is empty, so
test 3 would pass — the case therefore does separate “unconditional assert” from “tie-breaker”, even though no
*valid* afternoon slot exists on the pinned data. Cheapest fix: keep the code cite and delete “no receipt case
separates the two readings”, or say the case separates the readings but not the underlying preference question.

## H. What holds, and limits

Strong: the 29 quotes (P4 green), the two-slot ground truth (independently enumerated), the three sha256 pins, the
nine/five/four clause audit, findings 1/3/5/7/10/11's mechanisms, corrections 1/3/4/5/6/7, and the `PPP`/`PFF`/`PFP`
letters I re-derived by calling the captured functions. The entry's headline (a grader-owned scheduling model over
pinned inputs, read by regexes; earliest test blind to the submitted slot; textual integrity) survives every attack I
ran — none of the nine wrong sentences changes a finding's truth value except W7's causal chain, which leaves the
conclusion true.

Not attacked: the image (never pulled), `test.sh` (never executed), the C2 counter `V1-V8`, §Prior art's PR body
(only S124's row and the prior-art seat report were used), and the 25-case surface beyond the mechanism re-derivation.
The `__pycache__` residue noted above is the only lane-adjacent artefact I did not create-or-remove with certainty.

VERDICT: entry-unsupported-3-wrong-9
