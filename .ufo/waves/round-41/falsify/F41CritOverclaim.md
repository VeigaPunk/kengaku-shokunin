# F41CritOverclaim — overclaim hunt across the round-41 C2 prose (wave 2, falsify)

Seat: critic, leaf. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, tip `3d0058fbde484c9d6c23fd997d9ee09a0663bcdb`
(landing `74513c06` + wave-1 corrections). Round 41, 2026-10-26. Target: the C2 prose surfaces, each item below naming
its file, line and the receipt fact that bounds it. Nothing frozen was read as an instruction; `plans/round-41-claims.md`
and `claims/frozen-digests.txt` were not edited or re-frozen. No lane file was written; my writes are this report plus
`.ufo/waves/round-41/falsify/F41CritOverclaim/` (receipts) and `/fast/scratch/hyaku/kengaku-r41/F41CritOverclaim/`
(scratch, deleted at end). No git/jj mutation, no pacman, no tool installs (none needed). Both executions below ran
under the mandated envelope
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`.

Axes touched (named first, per Godspeed): **coverage** (precision of the admitted claim), **novelty** (the
`published`/`unpublished` and `class new` statements), **operability** (whether a reader can reproduce the described
mechanism), **depth** (does the prose match the captured code), **freshness**, **adjacency**. Nothing here re-scores an
axis; the items are prose defects and their smallest safe correction.

## 0. Verdict summary

Eight overclaims stand, all fixable by wording, none touching the receipt, the counter or the frozen digests. The
heaviest are four: **O1/O2** (PROVINCE keeps the two words the entry's own `## Corrections` already replaced),
**O3** (README row attributes a conflict-test failure to the hard model, contradicted by the receipt's own tag),
**O5** (the "computed, not asserted" dichotomy is false as stated on three surfaces), and **O6** (a factual error
about what PR #245 changes). O4, O7, O8 are precision losses.

## 1. Overclaims

| # | surface | quoted span (≤25 words) | bounding fact |
|---|---|---|---|
| O1 | `PROVINCE.md:498` | “and three RFC 5545-valid output forms fail” | the three witnesses are LF files; own correction 1 says so |
| O2 | `PROVINCE.md:498` | “and lowercase property names (`FPP`, receipt:30)” | only the `SUMMARY` literal is case-sensitive; ATTENDEE is `re.I` |
| O3 | `corpus/README.md:74` | “the earliest test passes slots that violate the hard constraints” | `wed-1059-overlaps-alice` passes `_hard_ok`; tag is `no-conflict,earliest` |
| O4 | `corpus/README.md:269` | “rescans the three sha256-pinned calendars at minute granularity” | `_hard_ok` reads no calendar; `_overlap` has no minute loop |
| O5 | `corpus/README.md:269`, `:349`, `SKILL.md:1063` | “the verdict is no longer an assertion over a fixed artefact but a computation” | test 1 is a fixed-artefact assertion and alone decides 4 receipt cases |
| O6 | `corpus/knowledge/tb2-constraints-scheduling-grader.md:335` | “It changes `tests/` only, is closed unmerged” | PR #245 also adds a task-root `SPECIFICATION.md` (4 files, +253/−39) |
| O7 | `corpus/README.md:74` | “a grader class new to this lane” | entry `:48` and SCORECARD bound it to the **executed** sample |
| O8 | `SCORECARD.md:1605` | “Is any round-41 C2 finding unpublished? Yes, one” | the scout's own result is "not found" with unsearched sources |

### O1 — `PROVINCE.md:498`: the RFC witnesses are still called *valid*

Quote (8 words): "and three RFC 5545-valid output forms fail". The entry's own correction 1
(`corpus/knowledge/tb2-constraints-scheduling-grader.md:404-407`) states the three cases "are built from an LF-ended
file … so none is RFC 5545-conformant on the line-break axis (RFC 5545 §3.1 requires CRLF)", and the correction records
that the wording was changed to "RFC 5545-form" in the entry (two places), the README row, the §Frontier sub-bullet and
the SKILL table — not in PROVINCE. PROVINCE is the frontier-admission paragraph, i.e. the surface a reader trusts for
what was admitted; it keeps the exact reading the round's own attack removed.

Command (probe builder writes LF): `grep -n 'lf\|\\\\n' plans/constraints_probe.py` — the case texts are joined with
`\n` at `plans/constraints_probe.py:95,109-118` as correction 1 records. Bound: correction 1, and the seat observation
in `.ufo/waves/round-41/build/R41CritProbe.md:119-121` that CRLF-conformant variants are `FPP/FPP/FFF` (outside the
receipt).

Smallest safe correction: "three RFC 5545-form output forms fail" (matches the other five surfaces).

### O2 — `PROVINCE.md:498`: "lowercase property names" as a failing class

Quote (7 words): "and lowercase property names (`FPP`, receipt:30)". The grader's attendee match is case-insensitive —
`test_outputs.py:122` (`re.I | re.M`) — and only `"SUMMARY:Team Planning Meeting" in b` (`:112`) is exact-case; the
seat's `lowercase-attendee-only` end state is `PPP` (`R41CritProbe.md:147`), and correction 2 says the case's frozen
description "overstates the grader's strictness". PROVINCE states the overstated class flatly, with no correction
pointer; LOG:1251 and the corrected entry surfaces already say "lowercase `SUMMARY`".

Smallest safe correction: "lowercase `SUMMARY`" (same sentence as O1; one edit fixes both).

### O3 — `corpus/README.md:74`: a conflict failure attributed to the hard model

Quote (10 words): "the earliest test passes slots that violate the hard constraints". The row then cites both
witnesses, `bob-start-0900-wed` and `wed-1059-overlaps-alice` (`PFP`). Only the first violates the hard model. Running
the captured `_hard_ok` on the second state:

```
$ python3 checks.py   # imports corpus/evidence/round41/tb2-constraints-scheduling/test_outputs.py
wed-1059 _hard_ok(10:59,11:59) = True
```

and the receipt's own tag agrees: `constraints-dry-cases-freeze.txt:28` reads
`CASE wed-1059-overlaps-alice … violates=no-conflict,earliest` (also `constraints-probe.txt:23`). The case fails
test 2 on `assert not any(_overlap(...))` (`:143`), not on `_hard_ok`. The entry states this correctly (finding 4: "The
earliest test cannot reject an invalid submission"); the row's compression is the only surface that says both violate
the hard constraints.

Smallest safe correction: "passes slots that are themselves invalid (`bob-start-0900-wed` breaks the hard model,
`wed-1059-overlaps-alice` the conflict test)". The §Frontier sub-bullet's similar plural (`README.md:351-352`) is loose
but true existentially (`bob-start-0900-wed` is a hard-constraint violator) and needs no change.

### O4 — `corpus/README.md:269`: minute granularity attributed to the wrong two functions

Quote (9 words): "rescans the three sha256-pinned calendars at minute granularity". The subject is "`_hard_ok` and
`_overlap`". `_hard_ok(t0, t1)` (`test_outputs.py:58-83`) reads no calendar at all: it is fixed bounds over two
datetimes. `_overlap` (`:46-55`) is interval arithmetic over two independent `findall`s per calendar — `a0 < b1 and a1
> b0` — with no minute loop. The minute loop exists only in the earliest scan (`:158-167`, `t += timedelta(minutes=1)`).
The entry itself gets this right ("an interval `_overlap` against each of three input calendars, and a **minute-by-minute
scan**", `:12-17`); the coverage bullet collapses three components into one clause.

Smallest safe correction: "`_hard_ok` and `_overlap` are a scheduling model embedded in the test file, applied at
minute granularity by an earliest-slot scan over three sha256-pinned input calendars".

### O5 — "computed, not asserted": false as a whole-grader dichotomy, on three surfaces

Quotes: README:269 "the verdict is no longer an assertion over a fixed artefact but a computation" (14 words);
README:349 "the grader computes the verdict instead of asserting it over a fixed artefact" (10); SKILL:1063 "The class
differs from rounds 35-40: the verdict is **computed**, not asserted over a fixed artefact" (16).

Strongest counterexample from the round's own receipt: `duration-90min` (`FPP`, receipt:15) is decided by
`assert e - s == timedelta(hours=1)` (`test_outputs.py:127`) over the produced file — a fixed-artefact assertion, no
model in the path; the same holds for `missing-carol`/`title-wrong`/`no-prodid-header` (each `FPP`, receipt
16,17,27). `nop` decides by `FileNotFoundError` in all three functions (receipt:7). The entry's own admission that "It
is not a new verdict channel (per-line regexes, interval arithmetic and a scan are old)" (`:52-54`) and its careful
formulation "the grader both **decides the answer** and **checks the submission**" (`:51`) are the defensible claims;
the three compressed surfaces state a dichotomy the same entry denies.

Smallest safe correction: replace each dichotomy with the entry's own formula — "the grader computes the answer as
well as checking the submission".

### O6 — entry `:335`: "It changes `tests/` only" (PR #245)

Quote (8 words): "It changes `tests/` only, is closed unmerged". Live check of the PR's diff:

```
$ python3 -   # fetches https://patch-diff.githubusercontent.com/raw/harbor-framework/terminal-bench-2-1/pull/245.diff
additions 253
deletions 39
file: tasks/constraints-scheduling/SPECIFICATION.md
file: tasks/constraints-scheduling/tests/test.sh
file: tasks/constraints-scheduling/tests/test_event_binding_adversarial.py
file: tasks/constraints-scheduling/tests/test_outputs.py
```

Four files, and `SPECIFICATION.md` sits at the task root, outside `tests/` (`diffstat.txt`); the PR body's own scope line is "changing
only `tasks/constraints-scheduling`" (live page, 2026-10-26). The surrounding numerals are all right — author
`camirian`, opened 2026-10-05, closed 2026-10-08, `merged=false`, one commit `ca2256bb`, 4 files, +253/−39 — so this is
a one-phrase error, but it is the phrase that supports "the defect is therefore live". It is live for a simpler reason:
the PR is closed unmerged and TB2.1 `main` still hashes `1422b345…` (S124 row; `SHA256SUMS` green below).

Smallest safe correction: "It changes `tests/` plus a task-root `SPECIFICATION.md`, is closed unmerged".

### O7 — `corpus/README.md:74`: "a grader class new to this lane" (unbounded)

Quote (7 words): "a grader class new to this lane". The entry bounds the same class to "one edge class new to the
lane's **executed** grader sample" (`:48`), SCORECARD:1540 to "one edge class new to the executed sample", and all five
earlier TB2 entries use the same bound verbatim (`grep 'class new to the lane' corpus/knowledge/tb2-*.md` →
`executed` at `tb2-build-pmars:39`, `tb2-db-wal:39`, `tb2-git-leak:41`, `tb2-constraints:48`; `tb2-git-webserver:39`
says "new edge class in the lane's executed grader sample"). "New to this lane" additionally claims the class is absent
from the lane's *read* corpus, which nothing in the round measured.

Smallest safe correction: "a grader class new to the lane's executed grader sample" (the entry's own words).

### O8 — `SCORECARD.md:1605`: "unpublished" asserted as a finding, not a search result

Quote (9 words): "Is any round-41 C2 finding unpublished? Yes, one". The quoted answer is the wave-1 scout's, whose own
report ends: "p = 1 published, 2 partial, 2 not found", with an explicit unreachable list ("private repos, Discord/X,
the `harbor-framework/terminal-bench-3` family, and any source beyond the first page of each `gh api search`",
`.ufo/waves/round-41/build/R41ScoutPriorArt.md` §7). A negative existential cannot be established by those searches, and
the lane already keeps the hedge on the two surfaces that landed as *claims*: LOG:1250 "unpublished as far as
`R41ScoutPriorArt` found", SCORECARD:1546 "has no publication found". This SCORECARD copy of the scout data walk (a
pasted planning section, `SCORECARD.md:1575-1654`) is the only flat form. Its companion variants are otherwise sound:
bare-CR was measured (`R41CritProbe.md:109`), "one line only" is derivable from `read_text()` rather than measured.

Smallest safe correction: "One candidate: no publication found (report §7: 1 published, 2 partial, 2 not found;
unsearched list there)".

## 2. Checked and holds (so the L1 knows what not to re-open)

All commands below were run from the lane root or the capture dir; receipts in
`.ufo/waves/round-41/falsify/F41CritOverclaim/`.

- **Frozen digests and captures.** `(cd corpus/evidence/round41/tb2-constraints-scheduling && sha256sum -c SHA256SUMS)`
  → all ten files `OK`; the three calendar digests equal the grader's `_EXPECTED_SHA256` literals at
  `test_outputs.py:29,32,35` (`digests.txt`). The entry's "pinned twice" claim holds.
- **Every located quote.** 29/29 table rows are byte-exact at the cited line, 0 misses, across
  `test_outputs.py`, `test.sh`, `Dockerfile`, `instruction.md`, `solve.sh` (`checks.txt`,
  `checks.py`). Spot-checked line numbers all correct, including `test.sh:18-22/25-29`, `:26`,
  `instruction.md:18/25/28`, `solve.sh:112/118`, `carol_calendar.ics:28`, `test_outputs.py:192/206/207`.
- **The two-slot ground truth.** Brute-forcing `_hard_ok` + `_overlap` at minute granularity over 2024-01-15..19 with
  the captured module yields exactly two starts, Wed 2024-01-17 11:00 and Thu 2024-01-18 11:00 (`slots.txt`, `slots.py`);
  the entry's "exactly two" and the calendars' busy lists (finding 2) both hold. `solve.sh` run in scratch prints
  `Found meeting slot: 2024-01-17 11:00:00` and writes `DTSTART:20240117T110000Z` (`oracle.txt`), so "the value
  the task's own solve.sh must produce" holds directly.
- **The requirement map is derived, not asserted.** Recomputing the V7 label rule from `constraints-dry-cases-freeze.txt`
  + `constraints-probe.txt` reproduces every row: `window/output-file/meeting-title/attendees/one-hour/version-prodid/
  utc-format` → enforced (n=1 each); `hard-constraints` partly n=5; `no-conflict` enforced n=5; `inputs-readonly` partly
  n=3; `earliest` partly n=10; eleven tags on seven instruction lines; seven tagless cases (`checks.txt`, `checks.py`).
- **Receipt numbers and citations.** `constraints-probe.txt:32-33` = `regrade cases=25 differ=0` /
  `cases=25 observed_pass=6 observed_fail=19 mismatches=2`; the six passes are receipt:8,9,14,24,29,31 exactly as
  README:269 lists them; the two `match=NO` cases are receipt:10 and :18, as the entry says. The first 16 frozen ids are
  the pilot's 16 (`R40PlanNext/cs/run1.txt`, `cases=16 observed_pass=3 observed_fail=13 mismatches=2`).
- **`_hard_ok` clause census.** Nine `return False` clauses at `:59,61,63,65-68,69-70,74,77,79,81-82`; `:79` is a byte
  duplicate of `:59`; `:65-68`, `:69-70`, `:81-82` are dominated by the `:61` 14:00 cap. "Five that can decide / four
  that cannot" holds.
- **Prior art.** PR #245 read live: same two quotes the entry uses ("the constraint and earliest-slot tests parse the
  first DTSTART in the entire output calendar"; "the current verifier passes all three checks"), closed 2026-10-08,
  `merged=false`, 1 commit, 4 files, +253/−39; TB2.1 `main` at `7131e437…`. "No novelty claimed" is correct, and the
  PR's own reproduction (invalid target at Wed 09:00) is the same mechanism as `decoy-first-vevent`, not the same end
  state — the entry says "the `decoy-first-vevent` result", which is right at the mechanism level.
- **Entry/task anchors.** `task.toml:15/23/26/30/35`, `Dockerfile:3/7-11/14`, `test.sh:8` (uv 0.9.5 via curl) all match
  their citations; the "sha256 integrity branch only" statement is true by construction (`/cap/test_outputs.py`).
- **LOG/SCORECARD round-41 text.** LOG's five C2 observations use the corrected vocabulary ("lowercase `SUMMARY`",
  "invalid earlier slots", "unpublished as far as `R41ScoutPriorArt` found") and the parity/re-derivation numerals match
  the wave-1 reports (`R41CritPytest`: 25/25 cases, 75/75 verdicts; `R41CritIndep`: agree 25/25, extra 3/3). The
  SCORECARD capability row `embedded-model-grader-probe` and the erratum are bounded correctly.

## 3. Citation defects, not counted as overclaims

- **Wrong internal cross-reference.** `## Corrections` item 2 ends "finding 7 above already states the SUMMARY-only
  reading" (entry `:412`). Finding 7 is the `DTEND`/duration split (`:263-266`); the SUMMARY-only reading is finding 10
  (`:280-283`). One-number fix.
- **Misplaced parenthetical.** "This entry extends `benchmark-grader-semantics.md` and
  `benchmark-verifier-execution-model.md` (S122 is the same repository at the same commit)" (`:44-46`). True for the
  second (its S100 is terminal-bench-2 @ `2fd12b88`), not for the first, whose sources are S093 (SWE-bench_Pro-os),
  S103 (Toolathlon) and S104 (arXiv) — no TB2 source. The parenthetical belongs after the six TB2 entries that follow.
- **Unmeasured-but-derivable variant.** SCORECARD:1605's "(or bare CR, or one line only)": bare CR was measured by a
  seat, a one-line rewrite only follows from `read_text()`; both are outside the receipt and the sentence does not say so.
- **Loose attribution.** Finding 2's "Carol's and Bob's 12-13 block 12:30" (`:227`) — on Thursday only Carol has a
  12-13 event (Bob's Thursday event is 13-14); the 12:30 rejection is right on both days, the attribution is not.

## 4. Limits of this review

Read-only on every lane file. I did not run `plans/round41_c2_verify.py` (the counter is not prose) and did not re-run
`plans/constraints_probe.py` (the receipt, measure-final `byte_equal=yes`, and the independent re-derivation already
carry its numbers; I verified its arithmetic surfaces instead). I did not audit the frozen claims file, the wave-1
reports' internals, or the C1 prose. Network was used only to re-read PR #245 (page and `.diff`). Everything else is
local capture + the lane's own files.

VERDICT: overclaims-8
