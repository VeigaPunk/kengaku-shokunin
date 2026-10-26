# R41PkgRows — SOURCES rows S122/S123/S124 for C2 (kengaku round 41, wave 1)

Seat: scribe (leaf). Lane repo read-only; nothing written outside this report dir and
`/fast/scratch/hyaku/kengaku-r41/R41PkgRows` (removed at exit). No tool installed, upgraded or
pinned this seat (`brew/pacman/uv` untouched; no `~/.local/bin` write).

## 1. What was done

Drafted three registry rows in the exact 11-cell schema of `corpus/SOURCES.md` (header
`corpus/SOURCES.md:21`, template rows S119–S121 at `:134-136`), validated them inside a scratch
copy of the registry at `$S/reg/corpus/SOURCES.md` (rows appended directly after S121, still
inside `## Registry` so no E12), and located every anchor quote in its capture with the frozen
`plans/sources_adopt.py --quote-file/--artifact/--url-map`.

## 2. Freshness — both raw URLs re-fetched and compared with the captures

```
$ curl -sS -o test_outputs.raw -w '%{http_code} %{size_download} %{url_effective}\n' \
    https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/tests/test_outputs.py
200 7679 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/tests/test_outputs.py
$ curl -sS -o instruction.raw -w '%{http_code} %{size_download}\n' \
    https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/instruction.md
200 2415
```
(fetched 2026-10-26 15:36:45 -03 = 18:36:45Z)

```
$ cmp test_outputs.raw corpus/evidence/round41/tb2-constraints-scheduling/test_outputs.py
CMP test_outputs.py: identical          # cmp exit 0
$ cmp instruction.raw  corpus/evidence/round41/tb2-constraints-scheduling/instruction.md
CMP instruction.md: identical           # cmp exit 0

1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1  test_outputs.py (fetched)
1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1  capture test_outputs.py
342def78177f9bc41bea4d11af679bc385a9dda2ac8a1e425be384a5b7f937b6  instruction.md (fetched)
342def78177f9bc41bea4d11af679bc385a9dda2ac8a1e425be384a5b7f937b6  capture instruction.md
```
Both digests equal `plans/pkg-spec-r41.json` `rows.S122.sha256` / `rows.S123.sha256` and the
capture `SHA256SUMS`. Capture dir `ls` = 10 files + `SHA256SUMS` (matches the claims: 10 captures).

## 3. S124 opened LIVE (this is the load-bearing divergence)

`gh api repos/harbor-framework/terminal-bench-2-1/pulls/245` at 2026-10-26 15:37 -03:

```
{"additions":253,"base":"main","changed_files":4,"closed_at":"2026-10-08T19:02:36Z","commits":1,
 "created_at":"2026-10-05T02:41:13Z","deletions":39,"head":"codex/fix-constraints-scheduling-event-binding",
 "html_url":"https://github.com/harbor-framework/terminal-bench-2-1/pull/245","merged":false,
 "merged_at":null,"number":245,"state":"closed","title":"Bind constraints-scheduling checks to the requested event",
 "user":"camirian"}
comments=0  review_comments=0  mergeable_state=blocked  closed_by=null  merged_by=null  base.sha=7131e4375048a0e408a8fb404b5f499d726b695b
files: added +34 SPECIFICATION.md | modified +1 -1 tests/test.sh | added +116 tests/test_event_binding_adversarial.py | modified +102 -38 tests/test_outputs.py
```

**Finding.** The PR is **closed, never merged** (`state=closed`, `merged=false`,
`closed_at 2026-10-08T19:02:36Z`, 0 comments, `mergeable_state=blocked`), and its body opens
"**Status:** local draft only; do not submit without owner authorization" and closes
"**External action required:** owner authorization to open this PR. No upstream issue, PR, or
comment has been created." So the decoy finding is **published as an unmerged/closed patch
proposal**, not an accepted upstream change; the entry and the lesson must not call it a fix
that landed. The rows below say exactly that. This also means the claims' `S124` wording
("prior art", tier B) is right but any sentence that reads "published fix" would be wrong.

Quote used (verified byte-present at line 7 of the raw body, capture line 11):
`the constraint and earliest-slot tests parse the first DTSTART in the entire output calendar`
(14 words), from the body's *Proposed PR description* section, immediately after "The current
grader still obtains the target VEVENT for the structure test, but …".

Body capture (must be copied byte-exact by the L1 to the cited path):
- draft: `.ufo/waves/round-41/build/R41PkgRows/pr245-body.md` (50 lines, 4869 bytes)
- target: `corpus/evidence/round41/pr245-body.md`
- `sha256 8f3b04c34edeb558d8b1e45ac49462bf28fdaa3392cec03bc6ee54d30253410f`
- contains a 4-line provenance header (`fetched … via gh api`, `state=closed merged=false …`) then
  the verbatim `.body`. Any re-authoring breaks the digest in the row's anchor.
- `sha256sum corpus/evidence/round41/pr245-body.md` must print the digest above after the copy.

## 4. Validation receipts

### 4a. Census (scratch copy of the registry, rows appended after S121)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/reg/corpus/SOURCES.md
```
First run (bare scratch: no `corpus/knowledge` or `corpus/lessons` trees) → **exit 1**, every
E11 line is a *scratch-copy* artifact (no `used-by` target exists under `$S/reg`), 146 findings,
including `E11 S122/S123/S124 missing used-by corpus/knowledge/tb2-constraints-scheduling-grader.md`.
After creating the same 26 empty `used-by` placeholders the registry already cites:

```
exit=0
E-codes: 0
W04: 15        # same 15 duplicate-url warnings the lane already carries; none is S122-S124
no S122-S124 finding (clean)
```
So the three rows introduce no E01 (NF!=13), E02, E03, E04, E05, E06, E07, E08, E09, E12 or
W01/W02/W03. **In the real lane, until `corpus/knowledge/tb2-constraints-scheduling-grader.md`
lands, the same census prints exactly three `E11` lines for S122, S123, S124 and exits 1** — the
row file alone cannot be green; the entry and the rows must land in one commit.

### 4b. Quote location + citation binding (`plans/sources_adopt.py`)

```
$ python3 plans/sources_adopt.py --quote-file row-S122.md --artifact corpus/evidence/round41/tb2-constraints-scheduling/test_outputs.py --url-map map-S122.json
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=test_outputs.py mismatch=0 unmapped=0 urlmap=map-S122.json entries=1
  ok S122 words=11 at test_outputs.py quote="assert not any(_overlap(s, e, cal) for cal in (A, B, C))" bound=test_outputs.py->https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/tests/test_outputs.py
exit=0

$ python3 plans/sources_adopt.py --quote-file row-S123.md --artifact corpus/evidence/round41/tb2-constraints-scheduling/instruction.md --url-map map-S123.json
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=instruction.md mismatch=0 unmapped=0 urlmap=map-S123.json entries=1
  ok S123 words=8 at instruction.md quote="Any modification will cause the tests to fail." bound=instruction.md->https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/instruction.md
exit=0

$ python3 plans/sources_adopt.py --quote-file row-S124.md --artifact .ufo/waves/round-41/build/R41PkgRows/pr245-body.md --url-map map-S124.json
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=pr245-body.md mismatch=0 unmapped=0 urlmap=map-S124.json entries=1
  ok S124 words=14 at pr245-body.md quote="the constraint and earliest-slot tests parse the first DTSTART in the entire output calendar" bound=pr245-body.md->https://github.com/harbor-framework/terminal-bench-2-1/pull/245
exit=0
```

(Quote-check was run per row because the tool takes one artifact per invocation; all three rows
share the registry file, which is what the census run above validates.)

**Re-run after the `:1-209` line-range correction** (the file is 209 lines, `wc -l`), reading the
three rows straight out of §5 with `sed -n '141,143p'` so the paste block itself is what was
tested: census `exit=0`, `E=0`, `W04=15`; the three quote runs `exit=0` with identical
`QUOTE rows=1 spans=1 located=1 found=1 … mismatch=0 unmapped=0` lines and an 11-cell row for
each id.

### 4c. Row shape, as `plans/round41_c2_verify.py` V3 parses it

```
11 S122 kind=code tier=A status=mined opened=2026-10-26 recheck=180d usedby=corpus/knowledge/tb2-constraints-scheduling-grader.md
   sha tokens: ['1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1']  quotes: [('assert not any(_overlap(s, e, cal) for cal in (A, B, C))', 11)]
11 S123 kind=docs tier=A status=mined opened=2026-10-26 recheck=180d usedby=corpus/knowledge/tb2-constraints-scheduling-grader.md
   sha tokens: ['342def78177f9bc41bea4d11af679bc385a9dda2ac8a1e425be384a5b7f937b6']  quotes: [('Any modification will cause the tests to fail.', 8)]
11 S124 kind=docs tier=B status=mined opened=2026-10-26 recheck=180d usedby=corpus/knowledge/tb2-constraints-scheduling-grader.md
   sha tokens: ['8f3b04c34edeb558d8b1e45ac49462bf28fdaa3392cec03bc6ee54d30253410f']  quotes: [('the constraint and earliest-slot tests parse the first DTSTART in the entire output calendar', 14)]
```
`len(cells)==11` for all three and the anchor cell holds exactly one `sha256 <64 hex>` token —
V3's `len(found[0]) != 11` and `toks != [row["sha256"]]` both pass for S122/S123. Quotes are
ASCII `"`-delimited (the registry's existing rows mix ASCII and curly; ASCII is what
`QUOTE_SPAN_RE = re.compile(r'"([^"]+)"')` at `plans/sources_adopt.py:277` pairs), and no cell
contains a `|`.

## 5. The three rows (paste verbatim, in this order, after S121)

```markdown
| S122 | Terminal-Bench 2.0 constraints-scheduling task grader (tests/test_outputs.py) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/tests/test_outputs.py | code | A | the executed scoring predicate of this one TB2 task at a pinned commit: three pytest functions over /app/meeting_scheduled.ics and the three input calendars, as this capture shows it | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, test_outputs.py:1-209, :135, :143 "assert not any(_overlap(s, e, cal) for cal in (A, B, C))" (11 words); sha256 1422b345ba3aacdfc4184e962811b6379988435896c50d8cf62903e70990c5d1 | three tests, not one: a structure test binding the Team Planning Meeting VEVENT by its summary and three ATTENDEE lines and requiring a one-hour Jan 15-19 weekday slot, a constraints test that takes the FIRST DTSTART of the whole file into an embedded model of per-person windows plus a 12:00-12:30 lunch block, and an earliest-slot test scanning 2024-01-15 09:00 minute by minute; the input calendars pass integrity by read_text equality or a pinned sha256 | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-constraints-scheduling-grader.md |
| S123 | Terminal-Bench 2.0 constraints-scheduling task instruction (instruction.md) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/instruction.md | docs | A | the request this one task states to the agent at a pinned commit, as the maintainer's own specification the grader is mapped against | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, instruction.md:1-30, :15-18, :18 "Any modification will cause the tests to fail." (8 words); sha256 342def78177f9bc41bea4d11af679bc385a9dda2ac8a1e425be384a5b7f937b6 | a 1-hour Team Planning Meeting for Alice, Bob and Carol in Jan 15-19 2024 with three per-person availability profiles, an output ICS the earliest valid slot must fill at minute granularity, two named tie-breakers, and a read-only clause naming all three calendars | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-constraints-scheduling-grader.md |
| S124 | Terminal-Bench 2.1 pull request #245 “Bind constraints-scheduling checks to the requested event” — https://github.com/harbor-framework/terminal-bench-2-1/pull/245 | docs | B | what the benchmark's own repository reports about this task's grader: the constraint and earliest-slot tests parse the first DTSTART in the whole output calendar, so an unrelated first VEVENT can supply the time evidence; closed unmerged at access | PR body §Proposed PR description, opened 2026-10-05, state closed, merged false, closed_at 2026-10-08T19:02:36Z, 0 comments at 2026-10-26 15:37 -03: "the constraint and earliest-slot tests parse the first DTSTART in the entire output calendar" (14 words); capture corpus/evidence/round41/pr245-body.md sha256 8f3b04c34edeb558d8b1e45ac49462bf28fdaa3392cec03bc6ee54d30253410f | the published reproduction (an unrelated context VEVENT first, the invalid target second, all three checks pass), a one-VEVENT binding fix, 55 adversarial fixtures and a fail-closed duplicate-target policy; the pull request was closed without merge on 2026-10-08, so this is prior-art disclosure, not an accepted upstream change | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-constraints-scheduling-grader.md |
```

Line-number check for the quote-bearing lines (`nl -ba` on the captures, and the body capture):
`test_outputs.py:143` = `assert not any(_overlap(s, e, cal) for cal in (A, B, C))`;
`instruction.md:18` = `  repo inputs. Any modification will cause the tests to fail.`;
`pr245-body.md:11` = the quoted sentence (raw body line 7). Line ranges in the anchors were
read off the same files (`wc -l`: `test_outputs.py` 209 lines, `instruction.md` 30 lines).

## 6. Lesson `## Gate` lines (for `corpus/lessons/round-41.md`, access date 2026-10-26)

Existing shape followed: a small table `row | URL / path | location | quote (≤25 words)` under
`## Gate`, one line per row (cf. `corpus/lessons/round-26.md:43-47`). Add the access **time**
because S124's state is the thing that can change:

```markdown
### Sources opened this round (access date 2026-10-26 for every row)

| row | URL / path | accessed (-03) | location | quote (≤25 words) |
|---|---|---|---|---|
| S122 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/tests/test_outputs.py | 2026-10-26 15:36:45 | tests/test_outputs.py:143 | "assert not any(_overlap(s, e, cal) for cal in (A, B, C))" (11 words); re-fetch cmp-identical, sha256 1422b345…0c5d1 |
| S123 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/instruction.md | 2026-10-26 15:36:45 | instruction.md:18 | "Any modification will cause the tests to fail." (8 words); re-fetch cmp-identical, sha256 342def78…37b6 |
| S124 | https://github.com/harbor-framework/terminal-bench-2-1/pull/245 | 2026-10-26 15:37 | PR body §Proposed PR description | "the constraint and earliest-slot tests parse the first DTSTART in the entire output calendar" (14 words); live state closed, merged false, closed_at 2026-10-08T19:02:36Z |
```

If the lesson prefers the round-25 style (one prose line per row) use the same three URL /
timestamp / quote triples — the timestamps are the receipt lines quoted verbatim in §4b.

## 7. Touched surfaces / out of scope

Written (this seat only):
- `.ufo/waves/round-41/build/R41PkgRows.md` (this report)
- `.ufo/waves/round-41/build/R41PkgRows/pr245-body.md` (S124 capture draft; 2026-10-26 15:38:29)
- scratch `/fast/scratch/hyaku/kengaku-r41/R41PkgRows/` — removed at exit (`trap`); `TMPDIR` was
  this dir for the census/quote runs.

Not written, by rule: `corpus/SOURCES.md`, `corpus/evidence/round41/`, `corpus/knowledge/`,
`corpus/lessons/`, `plans/`, any frozen file, the lane's Git index, `~/.local/bin`, `/usr`, `/tmp`.

Out of scope for this seat and left to the L1:
1. Landing the rows **together with** `corpus/knowledge/tb2-constraints-scheduling-grader.md`
   (otherwise census exits 1 with three E11 lines, §4a).
2. Copying `pr245-body.md` byte-exact to `corpus/evidence/round41/pr245-body.md` and checking
   `sha256sum` against the digest in the S124 anchor (§3); if the L1 prefers no new capture file,
   the S124 anchor must drop the `capture … sha256 …` tail, not keep a dangling path.
3. Any wording downstream that calls PR #245 a fix: it is closed unmerged.
4. `corpus/README.md` index row, PROVINCE paragraph, §Frontier sub-bullet — not this seat's files.

## 8. Findings / limits

- **F1 (freshness, for the entry):** S124 is closed unmerged with 0 comments, so the "decoy-first-VEVENT
  passes 3/3" observation stands as a lane probe result plus an *unmerged* upstream proposal. The
  PR body's own reproduction (context event first, invalid target second, all checks pass) is the
  closest independent corroboration, and it is the author's prose, not an executed artefact.
- **F2:** the PR body's draft header asks for owner authorization and says nothing was created
  upstream, yet the PR exists and was closed by an account that now resolves to `null`
  (`closed_by=null`). Record state/dates as read; do not infer a maintainer rejection.
- **F3:** my S124 capture is a body-only capture (4 provenance lines + `.body`); it does not carry
  the diff. The 4 changed files and +253/-39 line counts in the anchor are API metadata read at
  15:37, not diff content.
- **L1 (limit):** quote location is byte presence in the capture; it does not prove the sentence is
  load-bearing in the grader (that is the entry's `min_quotes`/`min_distinct_locations` job, spec
  `entry_rules`), nor that the grader is correct.
- **L2 (limit):** the two raw files are pinned by commit `2fd12b88…`; they were re-fetched at that
  same commit URL, so this checks the pin, not whether upstream `main` has since moved.

VERDICT: rows-drafted-3-census-exit-0
