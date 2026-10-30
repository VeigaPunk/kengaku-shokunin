# Report — C1ScribeSources2B (kengaku round 53, wave 3, R53-C1 prior-art leg, group B) — 2026-10-30

Seat: source scribe (leaf, no subagents). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Deliverables: `.ufo/waves/round-53/w3/C1ScribeSources2B/{rows.md, gate.md, fetch-log.tsv,
quote-locations.tsv, fetched/}`.

## What I did

1. Read the frozen claims (`plans/round-53-claims.md`, amendments A1–A3 in full), the wave-3 seat brief
   (`.ufo/waves/round-53/build_spec_w3.py:247-260`), the SOURCES contract v1 (fleet `CORPUS.md`), the
   existing registry (`corpus/SOURCES.md`, 186 rows), the census script, and both wave-1 group-B scout drafts.
2. Resolved the group-B scope. The brief named `C1ScoutSrcKaggle.md` and `C1ScoutSrcPapers.md`; neither
   exists (`ls .ufo/waves/round-53/w1/C1ScoutSrc*.md` → `C1ScoutSrcAudit.md`, `C1ScoutSrcBench.md`,
   `C1ScoutSrcTB2.md`, `C1ScoutSrcTesting.md`). I took the group-B pair by the wave-2 assignment
   (`build_spec_w2.py:195-197`: group B = `C1ScoutSrcBench` + `C1ScoutSrcTB2`) and by the sibling group-A
   scribe's own header (`C1ScribeSources2A/rows.md`: group A = `C1ScoutSrcTesting` + `C1ScoutSrcAudit`).
   So my group B is **Bench + TB2**, 28 candidate sources.
3. Re-opened **every one of the 28 sources live on 2026-10-30** (not the wave-1 archives): 30 HTTP fetches
   — the 28 canonical URLs plus the GitHub issue/pull body via the API for each tracker item, plus the four
   `.diff` files for the pull requests, plus the raw README for the one fork. **All 30 returned HTTP 200.**
   For every row the quoted text was located in the bytes I fetched and the sha256 of that fetch recorded.
4. De-duplicated against the registry before writing: extracted all 158 distinct URLs already in
   `corpus/SOURCES.md` (`grep -oE 'https?://[^ |)]+' corpus/SOURCES.md | sort -u`) — **none of my 28 URLs is
   already rowed**, and all 28 of mine are distinct from each other.
5. Applied contract v1's tier and keep/reject rules (below) and wrote 28 rows: **12 `queued`, 16 `rejected`**.
6. Validated the result against the census and the manual CORPUS.md checks (below).

## Exact commands

```sh
# scope resolution
ls /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ScoutSrc*.md

# registry de-duplication
grep -oE 'https?://[^ |)]+' corpus/SOURCES.md | sed 's/[.,;]$//' | sort -u > registry-urls.txt   # 158 URLs
#   -> all 28 candidate URLs reported "new"

# live re-opening (30 fetches, all HTTP 200)
curl -sSL --max-time 90 -A "kengaku-r53-C1ScribeSources2B/1.0" -o <slug>.html -w '%{http_code}\t%{size_download}' <url>
curl -sSL --max-time 90 -A "kengaku-r53-C1ScribeSources2B/1.0" -o <slug>.api.json -w '%{http_code}\t%{size_download}' <api url>
curl -sSL --max-time 90 -A "kengaku-r53-C1ScribeSources2B/1.0" -o <slug>.diff    -w '%{http_code}\t%{size_download}' <pr.diff url>

# quote location + digests (per row, re-run by the generator)
python3 gen_rows.py        # asserts every quote is present in the fetched bytes and <= 25 words

# census on a scratch copy with my 28 rows appended (ids renumbered S900-S927 to avoid clashing)
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/corpus/SOURCES.md --today 2026-10-30

# manual CORPUS.md census on the same scratch copy
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
awk -F'|' '.../ {t=$5; ...} END{...}' corpus/SOURCES.md          # tier histogram
awk -F'|' '.../ {s=$9; ...} END{...}' corpus/SOURCES.md          # status histogram
awk -F'|' '.../ {i=$2; ...; print i}' corpus/SOURCES.md | sort | uniq -d    # duplicate ids
awk -F'|' '.../ && NF==13 {if (t !~ /^[ABC]$/) ...; if (t=="A" && k=="community") ...}' corpus/SOURCES.md
```

## Measured numbers

- Sources re-opened: **28 of 28** (30 HTTP fetches including API bodies and diffs); **HTTP 200 on 30 of 30**.
- Rows written: **28** (12 `queued`, 16 `rejected`); ids `U01…U28` in document order.
- Quotes located in the bytes fetched today: **28 of 28**; longest quote **23 words** (limit 25); the
  `rows.md` anchor count and the `gate.md` count agree for all 28 rows after the corrections below.
- Quote re-verification against the archived bytes: **28/28 pass**, digests **52/52 match** `fetched/SHA256SUMS`.
- Archived files: 52, **none over 1 MiB** (one fetch, the Terminal Bench 4 page at 1,059,068 B, is archived
  as its first 1,048,576 B, `preftb4.html.head1MiB`, with both digests recorded).
- Duplicate URLs: **0** of my 28 rows against the registry's 158 distinct URLs; **0** within my 28.
- Census on the scratch copy with my rows appended: **exit 0**, `ok`, **15 W04** — exactly the same 15
  pre-existing duplicate-URL warnings as the unmodified registry (baseline: `ok` + 15 W04); **no finding
  names any of my rows**. Manual CORPUS.md checks on the same file: 214 rows, **0 malformed** (NF != 13),
  **0 duplicate ids**, **0 enum or tier-inflation violations**, tier histogram `A=162 B=32 C=20`,
  status histogram `mined=167 queued=20 rejected=27`.
- Credential-shaped scan of every file I wrote (pattern `ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{12,}|op://…|Bearer …|sk-…`):
  **0 hits**.

## Rows kept (12) and why

| id | source | kind | tier | bearing |
|---|---|---|---|---|
| U01 | UTBoost (arXiv 2506.09289) | paper | A | published count that benchmark test patches are insufficient (36 instances, 345 erroneous patches labeled passed) |
| U02 | SWE-Bench+ (arXiv 2410.06992) | paper | A | a quantified weak-test share: 31.08% suspicious patches, resolution rate 12.47% → 3.97% after filtering |
| U03 | Probe to Generate (arXiv 2604.01518) | paper | A | 77% of Verified instances admit a surviving variant; accepted patches exploit test gaps |
| U04 | SWE-ABS (arXiv 2603.00520) | paper | A | 19.71% of previously passing patches rejected by strengthening 50.2% of instances |
| U05 | UC Berkeley RDI, "We Scored 100%…" (lab blog) | docs | B | function-and-interface existence on Terminal-Bench: `test_c_extension_exists` satisfied by a dummy `.so` with two stub functions, never called |
| U06 | TB2.1 issue #156 (pytorch-model-cli) | docs | B | a contract mismatch the tracker records: README demands C, instruction and verifier demand none |
| U15 | TB2.1 issue #242 (modernize-scientific-stack) | docs | B | names `test_dependency_file_exists` by its exact name and says "The file is never opened" |
| U16 | TB2 issue #67 (make-doom-for-mips) | docs | B | a frame test satisfied by a byte copy of the verifier's own reference image |
| U17 | TB2.1 issue #237 (git-multibranch) | docs | B | expected strings published in the instruction, so pre-staged static files pass |
| U18 | TB2.1 issue #185 (custom-memory-heap-crash, polyglot-rust-c) | docs | B | a quick_exit shortcut satisfies the valgrind gate; a stale binary is re-run |
| U19 | TB2.1 PR #234 (make-doom-for-mips stale frame) | docs | B | the existence-poll boot signal and the corrective diff that removes the stale artefact |
| U20 | TB2.1 PR #235 (Scheme evaluator grading) | docs | B | the verifier runs a participant-writable interpreter for both expected and submitted output, so an empty one makes the two captured outputs equal and all 63 programs pass |

**Honest scoping of the weak-oracle rows.** As the reviewer `C1RevSources2` advised, I did not describe the
broad weak-oracle routes as literal presence-only. U16's scope says "a weak-oracle route, not a bare
existence-only test"; U17 "a pre-staged-artefact route rather than a bare existence check"; U18 "side-effect
and stale-artefact routes, not a bare existence-only test"; U19 "a stale-artefact route rather than
presence-only acceptance" (the existence poll is one step; the frame tests then compare image content); U20
"a participant-writable verifier input whose empty content is accepted". **After the reviewer's second pass
only U15 is a literal presence-only claim** — its quote names `test_dependency_file_exists` and says "The
file is never opened". U05 is scoped as function-and-interface existence, U06 as a contract mismatch, and
each says so in its own row.

**Two rows name tasks this round is pricing.** Measured today: U15's archived issue body contains the string
`test_dependency_file_exists`, which is the test name of `modernize-scientific-stack` in
`corpus/evidence/round53/tests-index.json`, and `modernize-scientific-stack` is one of the 28 never-read
candidates in `.ufo/waves/round-53/claims/c1-candidates.txt`. U06's archived body names `pytorch-model-cli`,
one of the 20 tasks the wave-2 readers confirmed and one of the 28 candidates. These are the rows that can
serve a `phenomenon-known` prior-art entry naming a confirmed task.

**One row is a duplicate project and is scoped to the part the arXiv lacks.** U05 is the UC Berkeley RDI blog
for the BenchJack project whose arXiv paper the group-A scribe rowed. I fetched
`https://arxiv.org/html/2605.12673v1` today (HTTP 200, 1,908,264 B, sha256
`568e71c9ba1bcd491c5b9baf8989e0fac5f917f4412fff9f87ef80ec12e2f70b`) and counted: **0** occurrences of
`test_c_extension_exists`, **0** of the phrase "never calls", **0** of "portfolio". The C-extension
existence-check walkthrough therefore exists only in the blog, which is why U05 is kept and scoped to it and
tiered B (a self-published lab post, not peer reviewed) rather than A.

## Rows rejected (16)

Every source I opened that does not bear on the phenomenon became a `rejected` row with a
`REJECTED: <reason>; flip: <condition>` teaches cell, per contract v1:

- **Different defect axis** (the weakness is real but not test-suite weakness): U07 SWE-Gate (review-constraint
  compliance), U08 June Kim's determinacy audit (task determinacy), U09 sympify input injection, U10 verifier
  tampering, U12 howardism's reward-hacking taxonomy, U28 caffe-cifar-10 label poisoning, U23 sanitize-git-repo
  (the *opposite* failure mode — a correct solution cannot pass), U24 nginx-request-logging (the config's content
  still matters).
- **Already registered or superseded by a kept row**: U21 issue #161 (same stale-frame defect as kept U19, which
  carries the diff), U22 issue #135 (same task as kept U20, weaker because it is the issue not the change),
  U25 PR #37 (the configure-git-webserver soft-verifier defect the lane already registers as S114).
- **Same task, different axis, already carried**: U26 PR #236 (the quick_exit shortcut is carried by kept U18).
- **Methodology lead, not a finding**: U27 PR #241 (an over-permissive output-format oracle; its
  verifier-regression CI is tooling prior art).
- **Not evidence about a benchmark grader**: U11 bohrin's in-repo weaknesses note (states the phenomenon class
  but grounds nothing in a benchmark, a task or a count).
- **Wrong benchmark generation / task identity**: U13 the dynamo-log-report fork (the original grader checked
  existence plus a size value — the size class, not presence-only — and the task is absent from the frozen
  population; the string `dynamo` occurs 0 times in `corpus/evidence/round53/tests-index.json`), and U14 the
  Terminal Bench 4 issues post (measured on TB4, not the pin: the fetched bytes mention `test_outputs.py` 8
  times, all for TB4 tasks such as `telecom-entity-resolution`, and **none** of the 88 pinned task names occurs
  anywhere in the page).

## Reviewer-driven corrections (peer `C1RevSources2`, applied before yield)

The reviewer independently re-opened all 28 URLs and confirmed every quote; it then raised five
grounded-teaches defects, all of which I fixed in `rows.md` and re-verified:

1. **U02 dropped an unbounded priority claim.** "the earliest quantified weak-test share" was not
   established by the source, so the teaches cell now says "a quantified weak-test share … the paper
   dates itself 9 Oct 2024 but claims no priority over earlier screens".
2. **U05's existence claim was too strong.** The blog's own list of the task's three tests (rendered
   line 174) says test 1 verifies a compiled `.so` file **exists with the `portfolio_risk_c` and
   `portfolio_return_c` functions**, so the row no longer claims a bare path-existence check: U05 is
   now scoped as *function-and-interface existence* (a dummy shared object with two stub functions
   passes), and the teaches cell says the blog names no TB2.0-pin task id, so it is prior art on the
   class rather than a citation of a pinned grader.
3. **U06 no longer claims a demonstrated presence-only test.** The issue gives the verifier's checks
   only in the aggregate ("existence, executability, prediction correctness"), with no test code, so
   U06's teaches cell now calls it a **contract mismatch** (README demands C, instruction and verifier
   do not) and states explicitly that it is not a demonstrated presence-only test.
4. **U20's route was relabelled.** "an artefact that merely exists and holds nothing is enough"
   conflated the participant-writable-interpreter route with bare existence; the teaches cell now
   states the actual mechanism: the verifier runs a participant-writable script for both the expected
   and the submitted output, so an empty script makes the two captured outputs equal and empty and all
   63 programs pass — the weakness is the writable interpreter plus failed-execution handling.
5. **Two word counts were inconsistent between `rows.md` and `gate.md`** (U13 said 5 against the
   gate's 4; U15 said 18 against 14). Both anchors now carry the count of the exact string quoted, and
   a re-check of all 28 rows finds **0 mismatches** between the two files.

## Deviations from the wave-1 drafts, and why

- **Ids `U01…U28`, not `T01…`.** The brief and `build_spec_w3.py:258` say `T01…` for both groups, but the
  sibling group-A scribe `C1ScribeSources2A` already holds `T01…T18`, and the census flags duplicate ids
  (`E03`). The wave-2 group-B scribe used `U01…`. I used `U` and documented the collision in `rows.md` so the
  L1 can renumber both documents into one contiguous S-range from S194.
- **Tier changes against the drafts.** The drafts tiered the Bench papers S901–S904 A/B/B/B and the RDI blog
  A; I keep the four papers A (each is the primary source of its own measurement) and drop the RDI blog to B
  (self-published lab post whose arXiv rendering is already rowed by group A). Tracker items that the draft
  tiered B I keep at B; the draft's rejected tracker rows S907–S910 and S947–S954 that I tiered B I move to C,
  because a row that does not bear on the lane's scope is a lead only and tier C is exactly that.
- **Rejected rows kept as rows.** The drafts rejected 8 + 8 sources. Contract v1 says a rejection is evidence
  of taste and is kept, so all 16 are rows with `status rejected` and a `REJECTED: …; flip: …` teaches cell,
  rather than being dropped.

## Files produced (absolute paths)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2B.md` (this report)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2B/rows.md` — 28 rows,
  11-column schema, ids `U01…U28`, `opened` 2026-10-30, `recheck` 90d/180d, `used-by` `—`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2B/gate.md` — per row:
  URL, HTTP status, access date, the located ≤25-word quote, its location, the sha256 of the fetch, and the
  archived file with its own digest
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2B/fetch-log.tsv` —
  all 30 fetches with URL, status, bytes and digest
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2B/quote-locations.tsv`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1ScribeSources2B/fetched/` — 52 archived
  files, each ≤ 1 MiB, with `SHA256SUMS`

Nothing was written by this seat outside its own seat directory and its scratch. The lane tree was not
edited by this seat; the `corpus/SOURCES.md` change recorded in the next section was made by the L1's
integration path, not by me.

## State of the lane registry at yield (observed, not written by this seat)

While I worked, another actor (the L1's integration path, `.ufo/waves/round-53/integrate_sources.py`,
written 02:20) appended **my 28 rows to `corpus/SOURCES.md`** under ids **S900–S927**. I did not write
that file — my seat never edits the lane — but I verified what landed:

- **0 cell mismatches** between the 28 integrated rows and my corrected `rows.md`: scope, anchor, teaches,
  status, opened, recheck and used-by are identical for all 28 rows, so the five reviewer corrections are
  present in the registry (spot-checks: S904 carries the function-and-interface-existence wording, S905 the
  contract-mismatch wording, S901 no longer claims "earliest quantified", S919 the writable-interpreter
  mechanism).
- **Word counts** in the integrated anchors match the exact quoted strings for all 28 rows.
- The ids landed are **S900–S927**, not the S194+ the seat brief and the integrator's own docstring name.
  The S-range is the L1's call, but the L1 should know that the round-53 source rows therefore sit at
  S900–S927 while the brief promised S194+, and that S194–S899 is currently unused in the registry.
- Census on the live lane registry (not a scratch copy) after the integration: **exit 0**, `ok` + the same
  **15 pre-existing W04** duplicate-URL warnings as the pre-round baseline, so none of my 28 URLs collides
  with an existing registry URL or with a sibling seat's row. Manual CORPUS.md checks on the live file:
  214 rows, **0 malformed** (awk `NF != 13` → 0), **0 duplicate ids**, **0 enum or tier-inflation
  violations**, tiers `A=162 B=32 C=20`, statuses `mined=167 queued=20 rejected=27`.
- One counting detail: U12's anchor reads "(12 words, the HARDCODE_OUTPUT case)", so a naive
  `\((\d+) words\)` scan misses it; the count 12 is correct.

## Notes, limits and hand-off to the L1

- **Scratch removed** before yield: `/fast/scratch/hyaku/kengaku-r53/C1ScribeSources2B/` (it held the
  generator `gen_rows.py`, the raw fetch tree, the fetch digests and the census scratch tree). Free space seen
  on /fast before the heavy pass: 456 G available (44% used); no ENOSPC.
- **No clone was needed**: this seat neither runs a counter nor mutates a tree, so it never touched git in the
  lane. The seat spec's clone instruction applies to seats that run the counters.
- **Tools installed: none.** No pacman transaction (the host-wide pacman pause of 2026-10-20 was respected);
  no `uv`/`npm` install was needed — `curl`, `python3` (stdlib only) and `sha256sum` sufficed. No tool output
  behaved inconsistently with its documented behaviour, so there is no tool-issue line to report.
- **What the L1 still owes.** `corpus/SOURCES.md` itself is not edited by this seat; the L1 appends these 28
  rows under renumbered S-ids from S194 (group B continues after group A's T-range → the sibling's S-range).
  If the L1 prefers the brief's `T` prefix for group B, the ids must be changed in both `rows.md` and
  `gate.md` consistently, or the census will report `E03 duplicate id`.
- **For the C1 prior-art leg**: U06 and U15 are the rows whose archives name a confirmed task
  (`pytorch-model-cli`, `modernize-scientific-stack` with its exact test name `test_dependency_file_exists`);
  of the two, **U15 is the only one whose quote itself names a test and states that the file is never
  opened**, so it is the row that can carry a `phenomenon-known` entry naming a confirmed task's own test.
  U05 is the row whose archive carries a Terminal-Bench existence-of-exported-symbol pass that the arXiv
  rendering of the same project does not contain, and it names no pinned task id. U01–U04 are the dated
  weak-suite prior art that bounds the round's novelty claim.
- **Not claimed by this seat**: no row is `mined`, no knowledge entry was written, and no `used-by` path is
  cited; the lesson and the knowledge entry that cite these rows are the L1's to write.
