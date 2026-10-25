# L0CheckExec: `plans/l0_filed_check.sh` (round 25 build, writer, axis: calibration)

Clone `/tmp/kengaku-r25-L0CheckExec`, branch `r25-L0CheckExec`, observed base `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a` (`git rev-parse HEAD`).
Uncommitted for L1 pickup: `git status --short` → `?? plans/fixtures/`, `?? plans/l0_filed_check.sh`.

## Files (sha256)
- `plans/l0_filed_check.sh` `2dc30511…7b95`: executable (`round24_census.sh` is 100755). POSIX sh plus one awk program. Offline; reads only its 2 args.
- `plans/fixtures/r25/l0_filed_check/report-r24-l0.md` `080e5017…55f8`: byte-identical to lines 219-229 of the fleet `.ufo/reports/round-24/kengaku.md`
  (file `7ff19e31…4dc5`). Check: `sed -n 219,229p … | cmp -` → VERBATIM-OK.
- `…/queue-all-filed.md` `4e636a50…014a`: the queue header plus the 3 questions, one per line. An independent awk unwrap of report `:221-227` is `cmp`-equal (UNWRAP-OK).
- `…/report-r24-l0-rewrapped.md` `29fd7c7c…7a71`: the same 3 questions wrapped at ~45 columns, so every key crosses a line break. Q3 is backtick-wrapped; 1 citation line sits outside the section (REWRAP-TEXT-OK).
- `…/queue-near-miss.md` `03847…5450`: Q1 is filed with its anchor; Q2's text is under `round-25` and Q3's under `kagi` (NEARMISS-TEXT-OK).

## Behavior (`plans/l0_filed_check.sh:2-16`)
- **Section:** each h2 containing "L0 questions", up to the next h1/h2. **Entry:** an optional list marker or backtick, then `kengaku | round-<N> |`. Continuation lines join until a blank line, heading, code fence or the next list item.
- **Key:** the first 60 characters (C.UTF-8) of the joined, whitespace-collapsed text after the round tag; a trailing space is dropped.
- **FILED** iff `kengaku | round-<N> | <key>` occurs in the whitespace- and pipe-normalised queue stream with no lane-name character before it. This is the lane + round + opening-words identity in PROTOCOL.md:527.
  A key found without that anchor still counts as UNFILED; the output adds a `queue:<line>` hint.
- **Exit:** 0 = all filed (a section that lists none also gives 0); 1 = any unfiled; 2 = usage error, unreadable input, or no L0 section.

## Red run (assigned). Live queue sha256 `51f183e9…09d9`, last committed in fleet `52b3863`.
```
$ sh plans/l0_filed_check.sh /home/vgpnk/Projects/shokunin/.ufo/reports/round-24/kengaku.md /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md; echo "exit=$?"
UNFILED report:221 kengaku | round-24 | Coverage cap: does a surface explicitly retired to `PROVINCE
UNFILED report:224 kengaku | round-24 | Novelty r21: the r21 "novelty axis-move — improved" verdict
UNFILED report:226 kengaku | round-24 | C2 admission: is a measured closeout/state-accuracy calibrat
l0_filed_check: sections=1 questions=3 filed=0 unfiled=3
exit=1
```
## Green run (assigned fixture)
```
$ sh plans/l0_filed_check.sh plans/fixtures/r25/l0_filed_check/report-r24-l0.md plans/fixtures/r25/l0_filed_check/queue-all-filed.md; echo "exit=$?"
FILED   report:3 queue:3 kengaku | round-24 | Coverage cap: does a surface explicitly retired to `PROVINCE
FILED   report:6 queue:4 kengaku | round-24 | Novelty r21: the r21 "novelty axis-move — improved" verdict
FILED   report:8 queue:5 kengaku | round-24 | C2 admission: is a measured closeout/state-accuracy calibrat
l0_filed_check: sections=1 questions=3 filed=3 unfiled=0
exit=0
```
## Other discrimination runs (cwd = clone root, final revision)
- Live report vs `<(cat live queue; sed -n 3,5p queue-all-filed.md)` → FILED at queue:72/73/74, filed=3, exit=0. Appending the 3 lines turns the live queue green.
- Rewrapped report vs all-filed → filed=3, exit=0. stderr: `note: … outside the L0 section, not checked: report:25`.
- Verbatim report vs near-miss → filed=1 unfiled=2, exit=1, with hints `[opening words at queue:4 …]` and `[… queue:5 …]`.
- Anchor boundary, Q1 under each queue prefix: `shinkengaku | round-24 |` → UNFILED; `` `kengaku | round-24 | `` → FILED; `- kengaku|round-24|` → FILED; `kengaku | round-245 |` → UNFILED.
- No args → usage, exit=2. Swapped args → `no "## L0 questions" section …; nothing to evaluate`, exit=2. `/nonexistent` → exit=2.
- Byte semantics (scratch PATH shim `gawk -b`, since removed): same counts and exits on all 3 queues, with the Q2 key cut at `verdic`.
  `bash --posix` gives the same 0/3, 3/3 and 1/2. Host `/bin/sh` is bash; dash and busybox are absent, so they are untested.
- All 16 fleet kengaku reports vs the live queue: round-24 → exit 1. The other 15 (r1, r3–r14, r16, r18) have no L0 section → exit 2, so none passes vacuously. This agrees with `L0FilingScout.md:9,12,18-23`.

## Risks / for L1
- Matching on lane + round + key is stricter than key-only: a question re-filed under another round stays UNFILED, with a hint.
- Exit 2 when the section is missing: the round-25 report contract (`.ufo/prompts/kengaku-round-25.md:99-119`) does not require `L0 questions`, so write `## L0 questions` plus `None raised.` to get exit 0.
  Under the round-24 contract the integrator appended L0 lines (`.ufo/prompts/kengaku-round-24.md:115-116`); these 3 never reached the queue.
- Not written (outside scope): the `corpus/README.md:160-173` `plans/` table has no row for `plans/l0_filed_check.sh` or `plans/fixtures`. Until the L1 indexes them, the C1.plans_indexed denominator in `plans/round24_census.sh:18` grows by 2. No LOG entry was written.
- Limitation: if a filer rewrites a question's first 60 characters, the check reports it as UNFILED. Not run: shellcheck and tests (wave rule).

Installs: none. Used the existing gawk 5.4.1 (`/usr/bin/awk`) and the `C.utf8` locale.
VERDICT: l0_filed_check.sh works and discriminates: the live round-24 run is red (3 unfiled, exit 1); the fixture is green (3/3, exit 0); near-miss, boundary and exit-2 runs behave as designed.
