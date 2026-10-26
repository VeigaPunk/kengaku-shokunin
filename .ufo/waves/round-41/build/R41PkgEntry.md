# R41PkgEntry — C2 knowledge-entry draft (`tb2-constraints-scheduling-grader.md`)

Seat: `R41PkgEntry` (scribe), kengaku round 41 wave 1, 2026-10-26. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Draft only: **no lane file outside this report dir was written or edited**; nothing committed, nothing pushed, no
product code, judge, counter, probe, capture or claims file touched.

## Behavior (what was produced)

| Artifact | Path | Digest |
|---|---|---|
| C2 entry draft | `.ufo/waves/round-41/build/R41PkgEntry/tb2-constraints-scheduling-grader.md` | `sha256 3855dc4195b724b05a5c365a5f21b97d7cade8c889ad8075f4a442a944ec10f8`, 38,534 bytes, 396 lines, 5,474 words |
| This report | `.ufo/waves/round-41/build/R41PkgEntry.md` | — |

The draft is modelled line for line on `corpus/knowledge/tb2-db-wal-recovery-grader.md`: the four header lines
(`source:` S122, `source:` S123, `verified-at:`, `recheck:`), then `## Summary`, `## Source labels`, `## What is graded
(static reading)`, `## Located quotes`, `## Requirement map` (with a `### Contestable tags` subsection), `## Findings,
each tied to its receipt cases`, `## Regrade (second grading of the same end state)`, `## What the probe does not show`,
`## Prior art` (+ `source-note: S124`), `## Negative space` (ending in a falsifier). Nothing in it is a claim about
novelty: the decoy result is attributed to S124 (TB2.1 PR #245) in the Summary, in finding 3, and in §Prior art.

## Gates — run, with outputs

All run against the **delivered draft path**, not a scratch copy. The validator re-implements the gate's own regular
expressions (`pkg_gate.py` `QUOTE_SECTION`, `QUOTE_ROW`, `MAP_ROW`) and the counter's `V7` derivation
(`plans/round41_c2_verify.py:232-270`), reading the frozen captures, dry table and receipt in place:

| Clause | Check | Result |
|---|---|---|
| P3 quote shape | rows parsed / distinct texts / distinct `(capture,start)` / out of 3-25 words | `quotes 29 badrows [] distinct_text 29 distinct_loc 29 oor []` |
| P4 verbatim | every quote found on its cited line(s) of the named capture | `verbad []` |
| P5 capture coverage | every quote capture is pinned in `SHA256SUMS` | `unpinned quote captures set()` |
| V7 requirement map | one row per frozen TAG, frozen line, DERIVED label, cited ids all violating | `map 11 bad [] missing [] dup []` |
| V4 mismatch naming | both `match=NO` cases in backticks in the entry | `match=NO named True` |
| P7 provenance | `source:` lines at the pinned raw URLs, `verified-at`, `recheck:`, `## Negative space` + falsifier | `source lines 2`, `url ok True`, `verified-at True`, `recheck True`, `negative space falsifier True` |
| headings | the ten required sections present | `['Summary', 'Source labels', 'What is graded (static reading)', 'Located quotes', 'Requirement map', 'Findings, each tied to its receipt cases', 'Regrade (second grading of the same end state)', 'What the probe does not show', 'Prior art', 'Negative space']` |

Spec thresholds met with margin: `min_quotes 8` → **29**, `min_distinct_locations 8` → **29**, `quote_words [3,25]` →
0 violations. `min_teaches_words 8` is a SOURCES-side rule (L1 hand-off below).

**Not run by this seat, by design:** `plans/round41_c2_verify.py`, `plans/constraints_probe.py`, `plans/pkg_gate.py`
and `scripts/sources-census.sh`. The counter's `V4/V5/V7/V8` are the L1's predicate; a scribe that re-ran the probe
would be decorating the receipt, not reporting it. The digests and numbers quoted in the entry are read from the
committed receipt, dry table and captures at their frozen digests.

## Live checks this seat did run (with commands and outputs)

1. **S124 opened live.** `read https://api.github.com/repos/harbor-framework/terminal-bench-2-1/pulls/245` →
   `"state": "closed"`, `"merged": false`, `"closed_at": "2026-10-08T19:02:36Z"`, `created_at 2026-10-05T02:41:13Z`,
   `"commits": 1`, `"additions": 253`, `"deletions": 39`, `"changed_files": 4`, head
   `ca2256bb61d1f1f77fcbf1b9ad461bf60057ee95`, base `7131e4375048a0e408a8fb404b5f499d726b695b`, `"merged_by": null`.
   The claims file's "S124 = TB2.1 PR #245 (tier B, open it live)" is satisfied by opening it; the PR is **closed
   unmerged**, which the entry states, and the defect is therefore live.
2. **TB2.1 `main` carries the same bytes as the pins.**
   `curl -sS -m 30 -o f -w 'http=%{http_code} bytes=%{size_download}' <raw url>` then `sha256sum f` →
   `tasks/constraints-scheduling/tests/test_outputs.py`: `http=200 bytes=7679`,
   `1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1`; `instruction.md`: `http=200 bytes=2415`,
   `342def78177f9bc41bea4d11af679bc385a9dda2ac8a1e425be384a5b7f937b6`. Both equal the spec pins in
   `plans/pkg-spec-r41.json`.
3. **RFC 5545 forms grounded.** `curl https://www.rfc-editor.org/rfc/rfc5545.txt` (9,411 lines). §3.1 p.9:
   “When parsing a content line, folded lines MUST first be unfolded” (10 words, line 511); §3.1 line 2821:
   “Property names, parameter names, and enumerated parameter values are case-insensitive.” (9 words); §3.8.2.4
   grammar `(";" "VALUE" "=" ("DATE-TIME" / "DATE")) /` and “Property Parameters: IANA, non-standard, value data
   type, and time zone identifier property parameters can be specified on this property.” (line 5425 area).
4. **The grader's own integrity literals equal the captures.** `test_outputs.py:29,32,35` are `5a5d4580…`,
   `c97e85db…`, `32a0f868…`; `SHA256SUMS` lists the same three for `alice_calendar.ics`, `bob_calendar.ics`,
   `carol_calendar.ics`. Written into §Source labels as the proof that the lane captured the pristine inputs.

## Derived-label table, with the receipt lines it rests on

Rule: `enforced` iff **every** receipt case whose `violates=` carries the tag is observed `fail`; `unenforced` iff
every such case is observed `pass`; `partly` otherwise. Cases are the 25 `CASE` lines of
`corpus/evidence/round41/constraints-probe.txt`; the tag list is the 11 `TAG` lines of
`corpus/evidence/round41/constraints-dry-cases-freeze.txt`.

| Tag | Frozen line | Violating cases and their observed verdict (`observed=`) | Derived label |
|---|---|---|---|
| `window` | `instruction.md:1` | `weekend-sat-20` fail | enforced |
| `output-file` | `instruction.md:10` | `nop` fail | enforced |
| `meeting-title` | `instruction.md:10` | `title-wrong` fail | enforced |
| `attendees` | `instruction.md:10` | `missing-carol` fail | enforced |
| `one-hour` | `instruction.md:10` | `duration-90min` fail | enforced |
| `hard-constraints` | `instruction.md:12` | `bob-start-0900-wed` fail, `decoy-first-vevent` **pass**, `seconds-30` fail, `weekend-sat-20` fail, `decoy-second-vevent` fail | partly |
| `no-conflict` | `instruction.md:12` | `later-valid-wed-1105` fail, `conflict-mon-1230` fail, `seconds-30` fail, `input-event-deleted-wed-1000` fail, `wed-1059-overlaps-alice` fail | enforced |
| `inputs-readonly` | `instruction.md:15` | `input-appended` fail, `input-event-deleted-wed-1000` fail, `input-crlf-rewrite` **pass** | partly |
| `version-prodid` | `instruction.md:23` | `no-prodid-header` fail | enforced |
| `utc-format` | `instruction.md:25` | `tzid-form` fail | enforced |
| `earliest` | `instruction.md:27` | `later-valid-wed-1105` fail, `later-valid-thu-1100` fail, `conflict-mon-1230` fail, `bob-start-0900-wed` fail, `decoy-first-vevent` **pass**, `seconds-30` fail, `weekend-sat-20` fail, `input-event-deleted-wed-1000` fail, `wed-1059-overlaps-alice` fail, `decoy-second-vevent` fail | partly |

Witnesses for the two `partly` labels and the two `match=NO` cases, quoted as field fragments so each stays inside
the 25-word quote rule (locations are lines of `corpus/evidence/round41/constraints-probe.txt`):

| Case | Receipt line | Decisive fragment (verbatim) |
|---|---|---|
| `decoy-first-vevent` | `:14` | `observed=pass tests=PPP predicted_tests=PPP match=yes regrade=same` |
| `input-crlf-rewrite` | `:31` | `observed=pass tests=PPP predicted_tests=PPP match=yes regrade=same` |
| `bob-start-0900-wed` | `:13` | `observed=fail tests=PFP predicted_tests=PFP match=yes regrade=same` |
| `later-valid-wed-1105` | `:10` | `observed=fail tests=PFF predicted_tests=PPF match=NO regrade=same` |
| `seconds-30` | `:18` | `observed=fail tests=PFF predicted_tests=PPF match=NO regrade=same` |

and the receipt's own summary at `:33` — `cases=25 observed_pass=6 observed_fail=19 mismatches=2` — with
`regrade cases=25 differ=0` at `:32`. Counts cross-checked: the six passes are `oracle-solve-sh`,
`literal-correct-slot`, `decoy-first-vevent`, `crlf-line-endings`, `extra-attendee-dave`, `input-crlf-rewrite`. So the
only passing cases that carry any tag are `decoy-first-vevent` (`hard-constraints`, `earliest`) and
`input-crlf-rewrite` (`inputs-readonly`) — exactly the set of `partly` labels. Every enforced tag's violating cases are
all among the 19 fails.

## Findings recorded in the draft (each tied to receipt cases)

1. Do-nothing 0 of 3 (`nop` `FFF`), unlike round 39's untouched state.
2. One answer up to the day — Wed 11:00 (`literal-correct-slot` `PPP`, `oracle-solve-sh` `PPP`,
   `later-valid-thu-1100` `PPF`); the per-day blocking reading is spelled out.
3. VEVENT order decides the score (`decoy-first-vevent` `PPP` vs `decoy-second-vevent` `PFF`) — **published**, S124,
   no novelty claimed.
4. The earliest test cannot reject an invalid submission (`bob-start-0900-wed`, `wed-1059-overlaps-alice`, both `PFP`).
5. Input integrity is decoded-text equality: CRLF rewrite of all three inputs passes (`input-crlf-rewrite` `PPP`) while
   an appended byte and a deleted event fail (`input-appended`, `input-event-deleted-wed-1000`, `FPP`), against
   `instruction.md:17-18`.
6. RFC 5545-valid forms fail (`folded-attendee-line` `FPP`, `lowercase-property-names` `FPP`,
   `dtstart-value-datetime` `FFF`) while CRLF output passes (`crlf-line-endings` `PPP`).
7. Duration is graded by one test only (`duration-90min` `FPP`).
8. `_hard_ok` has nine clauses, five live: `:79` duplicates `:59`, and `:65`, `:69`, `:81` are dominated by the 14:00
   cap at `:61` (`bob-start-0900-wed`, `later-valid-wed-1105`, `seconds-30`, `weekend-sat-20`, `conflict-mon-1230`).
9. The Carol 15-minute buffer is vacuous on the pinned inputs (`:192` gate; Carol's latest `DTEND` is 14:00) — no tag,
   no case.
10. Attendee matching is a superset, case-insensitive on `ATTENDEE` and exact-case on `SUMMARY`
    (`extra-attendee-dave` `PPP`, `title-wrong` `FPP`, `lowercase-property-names` `FPP`).
11. The oracle is a preference-ranked 30-minute grid (`solve.sh:112`, `:118`), so its earliest result is incidental
    (`oracle-solve-sh` `PPP`).

## Findings about the package, for the L1 (not done by this seat)

- **`corpus/SOURCES.md` has no S122/S123/S124 rows yet** (`grep -n 'S122\|S123\|S124' corpus/SOURCES.md` → no output).
  The gate's `P6`/`V3` need 11-cell rows. Copy-ready, matching the S119 shape (id | title — URL | scope | tier |
  what-it-is | anchor with exactly one `sha256 <hex>` | teaches ≥8 words | status | opened | recheck | used-by):

```
| S122 | Terminal-Bench 2.0 constraints-scheduling task grader (tests/test_outputs.py) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/tests/test_outputs.py | code | A | the executed scoring predicate of this one TB2 task at a pinned commit: three pytest functions that compute the verdict from a scheduling model over three sha256-pinned input calendars, as this capture shows it | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, test_outputs.py:1-209, :188 “assert 9 <= sched.hour < 12, "Prefer Alice's morning (9-12) when possible"” (10 words); sha256 1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1 | three pytest functions: decoded-text input integrity, a structure check on the VEVENT carrying the meeting, and a constraints-plus-earliest scan over the file's first DTSTART | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-constraints-scheduling-grader.md |
| S123 | Terminal-Bench 2.0 constraints-scheduling task instruction (instruction.md) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/instruction.md | docs | A | the request this one task states to the agent at a pinned commit, as the maintainer's own specification the grader is mapped against | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, instruction.md:1-30, :25 “- All times must be in UTC format (YYYYMMDDTHHMMSSZ)” (9 words); sha256 342def78177f9bc41bea4d11af679bc385a9dda2ac8a1e425be384a5b7f937b6 | one finding sentence plus three availability bullets, an output line, read-only input rules and a technical list fixing UTC timestamps and minute-granularity earliest-slot evaluation | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-constraints-scheduling-grader.md |
```

  and for prior art, mirroring S121's B-row shape:

```
| S124 | Terminal-Bench 2.1 pull request #245 “Bind constraints-scheduling checks to the requested event” — https://github.com/harbor-framework/terminal-bench-2-1/pull/245 | docs | B | what the benchmark's own repository reports about this task's grader: the constraint and earliest-slot tests parse the first DTSTART of the whole output calendar, so an unrelated VEVENT can supply the graded time; closed unmerged at access | PR body §Proposed PR description, opened 2026-10-05, state closed, merged false at 2026-10-26: “the constraint and earliest-slot tests parse the first DTSTART in the entire output calendar” (14 words) | the order defect of constraints-scheduling is published upstream with a patch binding every target check to one title-matching VEVENT, 55 adversarial fixtures and a fail-closed duplicate policy | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-constraints-scheduling-grader.md |
```

- **`corpus/README.md`** needs (a) exactly one index row starting
  `` | `knowledge/tb2-constraints-scheduling-grader.md` | `` whose citation cell names **both** S122 and S123, and
  (b) one bullet starting `- ` containing both the entry name and `evidence/round41/constraints-probe.txt` (the gate's
  `c_readme` receipt substring is the spec path minus `corpus/`).
- **`PROVINCE.md`** and the `§Frontier` sub-bullet: the entry claims 7 of 89 TB2 task graders read at `2fd12b88`; the
  draft says the clause is narrowed for this task only and stays open (a reading of rounds 35-40's six entries plus
  this one).
- **`plans/pkg-spec-r41.json` `receipt_sha256` is `null`** at freeze; the counter fills it before calling the gate
  (`round41_c2_verify.py:113-115`), so nothing needs editing.
- The draft's `recheck:` names the concrete re-run (`sha256sum -c SHA256SUMS`, both raw URLs, the probe) and the
  180-day interval used by every sibling entry.

## Conflicts and limits (verbatim where they are claims)

- **The claims file calls S124 "tier B"; I opened it and it is closed, not open.** Recorded as `state closed, merged
  false`. No conflict with `R40PlanNext.md:398` ("#245 closed 2026-10-08"), which already said this. The claims file's
  parenthetical reads "S124 = TB2.1 PR #245 (tier B, open it live)", i.e. an instruction to open it, which was done.
- **The pilot's two mismatches are carried, not corrected**: `later-valid-wed-1105` and `seconds-30` keep
  `predicted_tests=PPF` against `tests=PFF`. The entry names both in backticks (V4) and reads the failure mechanism
  (Carol's 12:00-12:30 lunch for `later-valid-wed-1105`, the lunch-crossing 12:00:30 end for `seconds-30`).
- **`seconds-30` does not demonstrate minute granularity.** The case was frozen for it (`instruction.md:28`) and fails
  as a lunch-boundary case instead; the entry says so in `### Contestable tags` rather than claiming a sub-minute rule
  was measured.
- **`_hard_ok`'s dead clauses are a reading, not a case.** No receipt case isolates a dead clause (it cannot change
  any verdict); the entry gives the code cite and says the screening is by reading.
- **The probe always takes the sha256 integrity branch** (`/cap/test_outputs.py` → parent.parent `/`). The
  text-equality branch (`:93`) never ran; the entry states finding 5 for both branches as a reading and marks only the
  digest branch as measured.
- **Scratch hazard.** My draft was written under `/fast/scratch/hyaku/kengaku-r41/R41PkgEntry/` and that **parent
  directory was removed by another seat mid-wave** (`ls /fast/scratch/hyaku/kengaku-r41/` → `No such file or
  directory`), destroying it. The draft was then written directly to the report dir and every gate was re-run there;
  nothing in this report rests on the lost copy. Seats whose `trap 'rm -rf -- "$S"' EXIT` names a shared parent are a
  live cross-seat hazard.
- **Not measured here:** the probe's own run, the counter's `checks=8`, `sources-census validate`, `pkg_gate` P1-P10,
  the order gate, and the image's pytest. The entry's `What the probe does not show` section already lists the
  substantive limits (no image, `test.sh` not executed, 25 cases only, no agent, no prevalence sweep).

## Frozen surfaces — verified unchanged by this seat

| Surface | Digest now | Matches |
|---|---|---|
| `plans/pkg-spec-r41.json` | `8e96421d91080d220cd8976abf62a1499b8a1bc92eb5d36eb0f55179b065d0dd` | counter `SPEC_SHA256` |
| `plans/pkg_gate.py` | `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` | `GATE_SHA256` and the spec's `frozen_instruments` |
| `plans/constraints_probe.py` | `8c471fbd0d83450793271d75fe3735a735226a725a73e0f16e02034e9d3c7242` | `PROBE_SHA256` |
| `corpus/evidence/round41/constraints-dry-cases-freeze.txt` | `a656ce9b9adb4e88bb49b6a8a45064a8c4f459cffbbf76d70cca7f43a0c77a03` | `DRY_SHA256` |
| `corpus/evidence/round41/tb2-constraints-scheduling/*` | `sha256sum -c SHA256SUMS` → `10` lines `: OK`, `0` failures | the manifest |
| `corpus/evidence/round41/constraints-probe.txt` | `c5aa674277f9b9473de4c0884629c577f2b6467d8b73c3a90eec33b24b7701da` | read only; the spec's `receipt_sha256` is `null` at freeze by design |

Commands: `sha256sum plans/pkg-spec-r41.json plans/pkg_gate.py plans/constraints_probe.py
corpus/evidence/round41/constraints-dry-cases-freeze.txt corpus/evidence/round41/constraints-probe.txt` and
`(cd corpus/evidence/round41/tb2-constraints-scheduling && sha256sum -c SHA256SUMS)`.

## Out of scope (untouched, and why)

No edit to `corpus/knowledge/`, `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`,
`LOG.md`, `plans/*` (spec, gate, probe, counter, dry table, claims), `corpus/evidence/round41/*` captures or receipt,
the two C1 tools, `plans/battery41/`, the lane's git index or jj state, and the fleet root or sibling lanes. No
`git add/commit/stash/checkout/reset/push/pull`, no `pacman`, no tool install, no network fetch beyond the three
read-only GETs listed above. No background jobs, no subagents.

VERDICT: entry-drafted-quotes-29-tags-11/11
