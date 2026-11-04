# ReviewerR84 — second-seat re-read of corpus/knowledge/tb2-code-from-image-offline.md (Q10/Q13/Q14, Q1/Q21 verdict), round 84

role: reviewer
seat: ReviewerR84
candidate: tb2-code-from-image-offline
candidate mention: corpus/knowledge/tb2-code-from-image-offline.md (kengaku lane; admitted round 83 at ddb903a876648d4f2471345cb20c61959502c3c1)
declared candidate writer field, quoted from the entry for identity comparison (this report is not authored by that seat): `writer: KengakuR84`
final verdict: disagree

VERDICT: disagree — the entry as admitted at BASE fails Q1, Q21 and Q13; content numbers verified; re-admission only after the repaired `recheck:` line and a Gate row that cites a returned second-seat report by path

## Scope

Independent, non-writer re-read of the round-83 admitted entry against QUALITY Q1, Q10, Q13, Q14
and Q21, plus re-opening the cited source myself. Subject: base revision
4087b2f8369fb0c317a8460725a607681ff2fd7f. I am not the writer of the candidate and I did not
edit it, the lesson, the checker or any production file. All probes are read-only on the lane or
ran inside synthetic fixture repositories under my scratch directory.

## 1. Cited source re-opened by this seat (Q10 evidence)

URL: https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py
Opened 2026-11-04 by curl (exit 0). Observed sha256 = b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a,
which equals the pin recorded in `verified-at:` and the committed capture
`corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py` (same sha256 recomputed here).
Byte count 935 matches the S267 row's "live 935 B". The retained copy of this fetch is
`source-recheck.txt` beside this report.

Confirmations with exact line numbers (the file is 31 lines, trailing newline present):

- :25 — the S267 quote exists exactly: `assert output.strip().startswith("bee26a"), (`.
  It is the complete line after strip (leading 4-space indent removed), and it whitespace-splits
  to 3 tokens, matching S267's "(3 whitespace-split words)". Preview output confirms length 3.
- :10 — `def test_output_file_exists():` (first test function, definition order 1).
- :18 — `def test_output_is_correct():` (second test function, definition order 2).
- :14 and :22 — `output_path = Path("/app/output.txt")`; :15 `assert output_path.exists(), ...`.
- :23 — `with open(output_path, "r") as f:`; :25 prefix assertion; :28-31 the equality assertion
  against `bee26a133f103b9ecda444c70ec22cafef6e31a3de7af6d047974dc90ce3defe`.

Entry claims cross-checked against those bytes, all correct: entry line 11 cites the exists leg as
`captured grader :10-15` (function :10, path :14, assertion :15); entry line 12 cites the content leg
as `captured grader :18-31` (function :18 through the closing assertion :31); the "six-character hint"
is `bee26a` (6 characters); the graded path is `/app/output.txt` in both functions. No location or
number defect was found in the entry body.

One entry sentence is not carried by the cited row: entry line 14 states the task statement asks for
"pseudocode shown in `/app/code.png`". S267 is the grader and does not contain that path. I re-opened
the task statement at the same pin (sha256 8c3af6483e409defef9786da51f318ae2ca71afe2327b94471d2f0e2e367442c):
its :1 does say `/app/code.png` and its :3 gives the `bee26a` hint, so the sentence is factually true;
but instruction.md has no admitted `corpus/SOURCES.md` row (the round-83 Gate, line 23, records that URL
only as rejected support for a solved-task claim). This is a Q2/Q3 sourcing residual, not one of the
three frozen C2 legs, and it is reported rather than scored.

## 2. BASE entry verdicts (git show 4087b2f8:corpus/knowledge/tb2-code-from-image-offline.md)

- Q1 verdict: DEFECT at line 3. Lines 1-3 are the triad in order (`source:`, `verified-at:`,
  `recheck:`), and `verified-at:` line 2 carries ISO date 2026-11-04; but line 3 is
  `recheck: python3 plans/round83_c1_replay.py --lane . --work DIR` — a re-check action with no ISO
  date and no cadence. Q1 requires "ISO date or cadence **and** the re-check action".
- Q21 verdict: DEFECT at line 3. Line 1 carries the 40-hex pin
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; line 3 names neither that pin nor a re-pin cadence
  (nor the 7+hex prefix form QUALITY's own check accepts). QUALITY Q21's executable check run on the
  base bytes prints `unpinned entry-base.md`.
- Q13 verdict: DEFECT. The entry's admission tree (ddb903a8) cites no second-seat re-read report, and
  the round-83 lesson does not record the entry admission at all: `corpus/lessons/round-83.md` lines
  10-17 are the SOURCES-row table (columns `id and decision | URL or own-work location | access date |
  located quote | reason / flip`), line 21 states "Independent spot-check of this round's admit and
  reject: not supplied by a lane-authored seat", and `grep -c 'tb2-code-from-image-offline.md'` over
  that lesson at BASE is 0. `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-83.md
  --commit 4087b2f8369fb0c317a8460725a607681ff2fd7f` prints
  `FAIL: no admit rows in ## Gate ...; admissions=0 passed=0 failed=1`, exit 1; the same command at the
  admitting commit ddb903a876648d4f2471345cb20c61959502c3c1 repeats it, exit 1. This is broader than
  R83-V1's "zero report paths": there is no admit row to carry a path.
- Q10 at admission time: DEFECT by the same record — no non-writer re-read existed before admission.
  This seat's current re-read (section 1) is appended evidence after the fact, not a landing-time review.
  Q10 is not in the frozen C2 predicate (q1/q21/q13 only); it is recorded for calibration honesty.

## 3. What the repaired line 3 must contain (Q1 + Q21 together)

The repair is the L1's to land; these are the constraints my re-read supports:

- an ISO date or an explicit cadence, and the re-check action;
- the pin named on the `recheck:` line itself, e.g. the 40-hex
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6` or its 7+hex prefix, or the re-pin cadence that
  regenerates it. The row's own registry cell `recheck` is `2027-01-18` (SOURCES columns
  `... | status | opened | recheck | used-by`), so naming that date plus "re-open S267 at the pin and
  diff against capture b9b7cb00..." satisfies both legs with one sentence.
- Any change to the `source:` line, to the two leg locations (:10-15, :18-31), to the hint length
  (6) or to the answer path `/app/output.txt` voids this re-read; a seat must re-open the source again.

A repaired draft was ABSENT when this report was written: no
`.ufo/waves/round-84/w1/ScribeR84/` directory exists, and the working-tree
`corpus/knowledge/tb2-code-from-image-offline.md` is byte-identical to BASE (sha256
fc42c76cb5a05c131a5fec4d2aa3e441d9627841d130a54d1b616f2042675271 at both), so line 3 still reads
`recheck: python3 plans/round83_c1_replay.py --lane . --work DIR`. I could not judge a repair that
does not exist; this is not a judgement that the repair will fail.

## 4. Q14 identity check for this report, and the structural precondition for Q13

`corpus/knowledge/tb2-code-from-image-offline.md` at BASE declares no `writer:` line
(`grep '^writer:'` exits 1). `gate_timing_check.py` resolves the candidate writer from such a line
(`plans/gate_timing_check.py:55` WRITER_RE, `:252` candidate_writer) and, at `:350-351`, rejects every
cited report with "candidate has no committed writer: field; self-review cannot be excluded" when the
line is missing. Fixture variant C reproduces that exact message. Therefore the successor entry must
declare its writer (the L1) before any Q13 citation can pass, and this report must not declare that
same identity as its own author — it does not; the writer appears only mid-line in the header block.

This seat's registered identity is `ReviewerR84`, role `reviewer` in
`.ufo/waves/round-84/w1/swarm-registry.json`, `agentId` null; `reviewer` is in
ALLOWED_REPORT_ROLES (`plans/gate_timing_check.py:24`). Role, seat and writer distinction therefore
satisfy Q14 in principle.

## 5. BLOCKING mechanics finding for the C2 Q13 leg (delta between the seat plan and the checker at BASE)

The frozen C2 text says Q13 is "checked by plans/gate_timing_check.py --lesson corpus/lessons/round-84.md
--commit REV, exit 0". The checker at BASE (sha256
51c18a9edfecba9cb6e15449b8063668f41225e98347c6221c6df7c2b0b80a2a) cannot reach exit 0 on a citation of
this round's wave directory. Five facts, each reproduced against synthetic fixture repos (not the
lane), one variant per rule; receipts `q13-fixture.out` (synthetic report bytes) and
`q13-realbytes.out` (this report's own bytes) sit beside this report. With the real bytes, the
identical report file and Gate row give exit 0 when cited at `.ufo/waves/round-84/falsify/ReviewerR84.md`
and exit 1 when cited at `.ufo/waves/round-84/w1/ReviewerR84.md` — so the report content is accepted
and only the directory naming blocks the claim.

1. `w1` is not a recognised second-wave directory. `is_second_wave` (`:241`) accepts only `falsify` or
   `wave[-_ ]?0*2`. Variant A (report at `.ufo/waves/round-84/w1/ReviewerR84.md`, registry at
   `w1/swarm-registry.json`, entry with a writer field) → `FAIL ... second-seat-reports=0`, exit 1.
   Variant B, byte-identical content under `.ufo/waves/round-84/falsify/` → `PASS ... second-seat-reports=1`,
   exit 0. Real bytes reproduce both: `REAL_FALSIFY_EXIT=0` (commit 69148115bfe18cd7301b468d907742a72b97ab7b)
   and `REAL_W1_EXIT=1` (commit dfd342485666272fcba7e3cc1cd7b7f57ef20360). So a `w1/` citation is never
   counted, however complete the report is.
2. A nested report path is never extracted. `wave_directory` (`:234-238`) requires exactly 5 path
   components and FULL_REPORT_RE requires `<wave>/<Name>.md`; `.ufo/waves/round-84/w1/ReviewerR84/report.md`
   has 6. Variant E → `cited seat-report paths: none`, exit 1; the real-bytes nested run repeats
   `cited seat-report paths: none` and `REAL_NESTED_EXIT=1`. The L1's instruction to write
   `w1/ReviewerR84/report.md` is therefore not citable; the citable shape is a 5-part `.md` file, which
   is why `.ufo/waves/round-84/w1/ReviewerR84.md` also exists beside it.
3. The wave registry is read only from the second-wave directory. `load_members` (`:284-298`) reads
   `<round>/<falsify|wave2>/swarm-registry.json`; the round's `w1/swarm-registry.json` is never loaded,
   so a `w1`-only registration cannot satisfy `:346-348` either.
4. The Gate table must use the column names the parser keys on. `parse_gate_admissions` (`:144`) needs
   a header containing `candidate`, `decision` and `reason` (case-insensitive, backticks stripped).
   The round-83 Gate's header is `id and decision | URL or own-work location | access date | located
   quote | reason / flip`, which is why admissions=0 above. The round-84 Gate must be a
   `| candidate | decision | reason |` table whose candidate cell is the repo-relative entry path.
5. The candidate entry must declare `writer:` and the report must not repeat it in a `writer:`/`author:`
   line. Variant C (entry without writer) → invalid, exit 1; variant D (report line `writer: KengakuR84`)
   → "report writer/author declaration equals candidate writer 'KengakuR84'", exit 1. This is why the
   header block of this report keeps the writer mid-line. I flag that this deliberately departs from
   the literal `writer: KengakuR84` line named in my seat brief: emitting that line would disqualify
   the very report Q13 needs, so the brief's field is preserved in substance and quoted, not as a
   line-initial key.

Consequences for the L1 (production files are not mine; I did not write under `falsify/`):

- Option A, checker untouched: cite a 5-part report under `.ufo/waves/round-84/falsify/`, with a
  `.ufo/waves/round-84/falsify/swarm-registry.json` carrying this seat and role `reviewer`. Proven
  with this report's own bytes (`REAL_FALSIFY_EXIT=0`, `second-seat-reports=1`); it requires the L1 to
  place a copy of this report there (I may not), and it introduces a wave directory that the frozen
  "ONE v1 wave" shape does not name.
- Option B, checker amended: extend `is_second_wave` (`:241`) to accept the round's actual wave
  directory (`w1`). That commit touches a gate and therefore owes Q20's out-of-band run plus the
  roster's own row (`gate_timing_check.py --selftest`), and Q15/Q16 require a `w1` fixture case in that
  selftest, otherwise the amendment is untested. The amended check must still be red at BASE; it would
  be, because round-83 has no candidate row at all. Option B leaves the frozen predicate's named
  command intact and makes the citation of `.ufo/waves/round-84/w1/ReviewerR84.md` meaningful.
- Either option needs fact 4 (Gate table columns) and fact 5 (entry `writer:` line), and either must
  cite exactly one path: `BARE_REPORT_RE` resolution (`:271-280`) fails on ambiguity, and two cited
  reports would demand two qualifying seats.

## 6. Independent content verdict

The entry's substantive content about the grader is accurate against the re-opened bytes: two
functions in definition order, existence via `Path.exists`, content via stripped prefix plus exact
equality, whitespace tolerated by `strip()`, and the explicit non-claim that replay is not image
understanding or task solving. I did not test the replay instrument itself (that leg belongs to the
C1 seats and is outside this re-read).

## 7. Residual findings routed, not scored

- R84-R-1: entry line 14's `/app/code.png` sentence rests on instruction.md at the pin, which has no
  admitted SOURCES row (Q2/Q3 residual). Fix: admit a row for the task statement, or attach the
  sentence to the row that already opened it, in the next round.
- R84-R-2: the round-83 Gate records no admission row for the entry at all, so the missing second-seat
  citation is compounded by a missing admission cell. The successor Gate in `corpus/lessons/round-84.md`
  must carry the `candidate | decision | reason` row, or the Q13 check cannot even evaluate it.
- Absent, not fabricated: no repaired draft existed at report time (section 3).

## 8. Commands and exits

    curl -o test_outputs.py <pin URL>                                  -> 0 (sha256 match)
    curl -o instruction.md <pin URL>                                   -> 0
    sha256sum test_outputs.py corpus/evidence/.../test_outputs.py       -> b9b7cb00… twice
    python3 - <<'PY' (line/quote/token checks)                          -> 0
    git show 4087b2f8:corpus/knowledge/... > entry-base.md              -> 0
    QUALITY Q21 one-liner on entry-base.md                              -> prints "unpinned entry-base.md"
    python3 plans/gate_timing_check.py --lesson corpus/lessons/round-83.md \
        --commit 4087b2f8369fb0c317a8460725a607681ff2fd7f               -> 1 (no admit rows)
    python3 plans/gate_timing_check.py --lesson corpus/lessons/round-83.md \
        --commit ddb903a876648d4f2471345cb20c61959502c3c1               -> 1 (no admit rows)
    bash q13_fixture_probe.sh (5 synthetic fixtures)                    -> A=1 B=0 C=1 D=1 E=1
    bash q13_realbytes_probe.sh (this report's bytes, two shapes)       -> falsify=0, w1=1, nested=1
    ls .ufo/waves/round-84/w1/ScribeR84/                                -> 2 (absent)
    sha256sum corpus/knowledge/tb2-code-from-image-offline.md vs BASE   -> identical

No tool was installed or upgraded; none was needed. No build, lint or general test suite was run.
