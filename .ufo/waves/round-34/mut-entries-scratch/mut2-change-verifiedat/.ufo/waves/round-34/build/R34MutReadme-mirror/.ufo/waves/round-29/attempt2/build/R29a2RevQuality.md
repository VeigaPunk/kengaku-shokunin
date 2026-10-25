# R29a2RevQuality — QUALITY Q1–Q8 walkthrough of the task-validity entry

Seat: `L1Kengaku29.R29a2RevQuality` (leaf reviewer; no dispatch, no production edits).
Round 29 attempt 2, 2026-10-25. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Criteria read from `corpus/QUALITY.md` lines 15–66 (all line numbers below are that file).

Method disclosure: **no `lsp` device is mounted in this session's device list** (the `xd://`
inventory holds `ast_edit`, `debug` and the aseprite/blender/godot/tripo/unity MCP paths only), so
no semantic `references`/`definition`/`diagnostics` were available. Every locator below is a literal
`file:line` read or a grep whose command and output are shown. No tool was installed or upgraded
(no pacman transaction attempted; host guard respected).

## Objects under test — two different texts, both pinned

| # | path | sha256 | lines | state at review |
|---|---|---|---|---|
| 1 | `/tmp/r29a2-EntryDraft/entry.md` (the seat's draft) | `2ca8ecaad6d8c72405eb2c86b13c0bc182073f615173abac6386aea6b40e4398` | 157 | declared stable by its writer (message 03:5x); the draft this ticket names |
| 2 | `corpus/knowledge/benchmark-task-validity-checklist.md` — **committed** as blob `a18d4e87…` in `8cf7b60` | `a18d4e87cfba14d2103020ee4deef47ea3478947341d5ba246a26cdbe21cce69` (committed) | 97 | tracked and admitted; the working copy has since diverged and is still being edited (now `b80072f7…`) |

## Table 1 — the draft (`/tmp/r29a2-EntryDraft/entry.md`, `2ca8ecaa`, 157 lines)

| Q | criterion | verdict | criterion line | draft line(s) that satisfy or break it |
|---|---|---|---|---|
| Q1 | triad opens the entry: `source:` (id(s), URL, exact anchor), `verified-at:`, `recheck:` (date/cadence **and** action) | **PASS** | `QUALITY.md:15` | `:1-5` five `source:` lines, each with `S###`, pinned raw URL and anchor (`:3` anchors S079 to lines 18/19, the values actually quoted); `:6` `verified-at: 2026-10-25`; `:7` `recheck: 90d — re-open … re-grep … date the result; next due 2027-01-23` (cadence + action + due date). Caveats: the literal "first three lines" reading is met only field-wise (five `source:` lines precede `verified-at:`), which Q1's own "`S###` row id(s)" anticipates — and the frozen counter *requires* ≥5 `source:` lines (`SOURCE_LINE_RE` + target `cited_rows=5`). `:8` `writer: KengakuR29` is a placeholder (F4). |
| Q2 | tier floor, per load-bearing claim, tier A or B for that claim's scope; no tier-C alone; `community` never A | **PASS** | `QUALITY.md:24` | Per-claim tier: A→S077 **A**; B→S077 **A**; C→S077 **A**; D→S090 **A**; E→S078 **A**; F→S078 **A**; G→S079 **A**; H→S079 **A**; I→S080 **A**; J→S080 **A**; K→S090 **A** (`:37-47`). Registry rows now exist: `SOURCES.md:100-104`, all `status=mined`, `used-by` = the entry (awk over `$5/$9/$12`). Counter: `rows_present=5 rows_mined=5`. |
| Q3 | each load-bearing sentence → anchored quote ≤25 words with location; paraphrase narrows, never widens | **PASS** | `QUALITY.md:31` | Word counts on the draft's own strings: `:37` 4; `:38` 3; `:39` 15; `:40` 11; `:41` 9; `:42` 8; `:45` 24; `:47` 18 — all ≤25, each with a `Where` anchor (`:35` header). No widening found: `:39`/`:40` explicitly refuse to equate the two canary strings, `:79-81` refuse to read F as a validity result, `:93-113` refuse cross-benchmark transfer. One number lacks an in-entry command: `:77` "one of the 89 task directories carries neither time baseline" (F5). `:46` does carry its command (`git ls-tree -d --name-only 9be8d8f:tasks/finalpool \| wc -l`). |
| Q4 | negative space written down: what the sources do **not** establish **and** the falsifying observation | **PASS** | `QUALITY.md:36` | `:127-157` — eleven bullets, including `:133-135` "a detector-negative would not be a clean bill even if one had been run" (no laundering), `:147-150` the S090 date limit, and `:154-157` **"Falsifier of this entry"** naming both the location failure and the anchor-mismatch failure, plus what would *not* falsify it. |
| Q5 | every source labelled for what it is; own-benchmark disclosure = self-report, not independent replication | **PASS** | `QUALITY.md:43` | `:24-26` classifies all five as maintainer-authored and "None is an independent replication"; `:45` labels the S080 release sentence "a maintainer self-report"; `:82` "As a self-report … not evidence that the work succeeded"; `:145-146` repeats it under negative space with the explicit `(Q5)` marker. No "canonical older method" claim exists, so that half is not applicable. |
| Q6 | names the existing entry/coverage row it extends; never duplicates or overwrites; errata append | **PASS** | `QUALITY.md:50` | `:14-17` names the coverage surface (`corpus/README.md` §Frontier) **and** `knowledge/agent-time-horizon-and-task-validity.md`, and states it does not replace `knowledge/webarena-task-spec-audit.md`; `:18-19` distinguishes itself from a contamination audit. No in-place edit of an existing row is proposed. |
| Q7 | entry + `corpus/README.md` index row + coverage-map row land **in the same commit**; no support on `/tmp`, `local://`, unlanded copy | **FAIL** (for this text) | `QUALITY.md:56` | The three surfaces did land together — `8cf7b60` adds index row `corpus/README.md:64`, coverage row `:249`, frontier partial-discharge `:271`, verified in Table 2 — but that commit contains a **different text** (`a18d4e87…`), so nothing in it carries this draft's rows A–K, its `Where` column or its Q5 labels (F1). Support side is clean: `grep -n '/tmp\|local://'` over both texts returns **no lines**. |
| Q8 | every candidate screened and not admitted recorded with reason and flip condition, in the Gate or a `rejected` row | **PASS** (round surface, not the draft) | `QUALITY.md:61` | `corpus/lessons/round-29.md:150` §Attempt 2 → `:169` `### Gate` table with candidate / decision / reason / **flip condition** columns (admit row; `contamination-transparency-card.md` reject; "remaining 168 staged rows and 64 staged entries" reject with reason and flip) and `:212` `### Rejected candidates — three staged entries, scored by an independent scout` with per-candidate reason + flip. The entry file itself carries no rejection duty. |

**Count: PASS 7/8** (Q7 the only FAIL; it is landing-coupled, not a defect in the prose).

## Table 2 — the committed entry (commit `8cf7b60`, blob `a18d4e87…`, 97 lines)

This is the **binding** artifact: it is what the admitting commit contains, so it is what Q7 and the
Q13/Q14 timing checks read. Between my first read and this table the working copy moved three more
times (`4769ce2e…` 96 lines → `a769fad8…` 113 → `b80072f7…` 97+), so every verdict here is against
the committed blob, extracted with
`git show 8cf7b60:corpus/knowledge/benchmark-task-validity-checklist.md | sha256sum` → `a18d4e87…`.

| Q | verdict | committed line(s) / evidence |
|---|---|---|
| Q1 | **PASS** | `:1-5` source lines (S077 `../docs/…` line 95 + table lines 29/31; S078 lines 99/75 + `v2/GATE.md` line 1; S079 lines 1, 15, 18, 19, 22; S080 line 27 + `task_config.json` lines 2-12; S090 as served); `:6` `verified-at: 2026-10-25`; `:7` `recheck: 180d … next due 2027-04-23` (cadence + action + due date). No `writer:` line. |
| Q2 | **PASS** | same five A-tier rows (`SOURCES.md:100-104`, committed in the same commit), counter `rows_present=5 rows_mined=5 usedby_ok=1`. |
| Q3 | **PASS** on quotations | every quoted span located at its stated line in bytes I re-read; row D's quote is 20 words with one whitespace normalization (F8a). **But** `:47-52` assert "1 of 89 task directories (`caffe-cifar-10`) … neither time baseline" and "6 lines across 3 tasks write integer literals", and §Counts `:63-73` supplies commands only for 92/89 and 109/108 while itself stating "A row that carries a count must carry the command that produced it" — the entry breaks its own rule for those two numbers (F5). |
| Q4 | **PASS** | `:84-97` "What this does not establish" ending in `:95` `**Falsifier.**` (both the contradiction test and the absent-field test). |
| Q5 | **FAIL** | `grep -n 'self-report\|maintainer claim\|claims the work'` over the committed blob → **no match**. It quotes a maintainer's own release notes and announcement and never labels them self-reports; `QUALITY.md:43` requires the label. The draft carries it four times (`:26`, `:45`, `:82`, `:145`) — the fix never reached the commit. |
| Q6 | **FAIL** | committed text has **no** `extends`/`Extends` and names no existing entry (`grep -n 'extends\|Extends\|agent-time-horizon\|webarena-task-spec-audit'` → no match); `QUALITY.md:50` requires the entry to name what it extends. The draft does (`:14-17`); an intermediate working copy briefly did too (`a769fad8:18`). |
| Q7 | **PASS** | same-commit test: `git show --stat --name-only 8cf7b60 -- corpus/` lists `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/benchmark-task-validity-checklist.md`, `corpus/lessons/round-29.md` and `corpus/evidence/round29-attempt2/*`; the README diff in that commit adds the index row (`+ | \`knowledge/benchmark-task-validity-checklist.md\` | Ten-axis …`) and the coverage row (`Benchmark task-validity instruments`, 1 match) plus the frontier partial-discharge line. Neither text cites `/tmp` or `local://`. |
| Q8 | **PASS** | `corpus/lessons/round-29.md` `:169` Gate table and `:212` rejected-candidates section, both in the same commit. |

**Count: PASS 6/8** (Q5, Q6). This is the round's operative score.

**Score summary.** Draft `2ca8ecaa`: **7/8** (Q7 — that text did not land). Committed `a18d4e87`:
**6/8** (Q5, Q6). The gap between the two tables is the entry's central risk: the draft solved Q5 and
Q6 and the commit does not contain those solutions.

## Findings by severity

### HIGH

**F1 — the committed entry is not the reviewable best text; it is missing the Q5 and Q6 fixes that
exist in the draft.** The admitting commit `8cf7b60` contains blob `a18d4e87…` (97 lines, checklist
rows **A–J**, no `Where` column, no self-report label, no `extends` line). The draft that its own
scribe declared stable is `2ca8ecaa…` (157 lines, rows **A–K**, five-column checklist, four Q5
labels, an explicit `extends` paragraph). Between them the working copy also passed through
`4769ce2e…` (96) and `a769fad8…` (113, which briefly carried `This entry extends …` at `:18`) and is
now `b80072f7…`. Evidence: `sha256sum` of all four, `wc -l`, and
`git show 8cf7b60:corpus/knowledge/benchmark-task-validity-checklist.md | sha256sum`.
Consequence: the admitted text scores **6/8** while the draft scores **7/8**, and Q13's cited
second-seat reports re-read yet another hash, so "which text did the reviewers pass?" is not
answerable from the tree. Resolution: land the draft's Q5/Q6 sentences as an appended correction
(R1 keeps the committed bytes) or amend the commit, then re-run Table 2 against the new hash.

**F2 — the committed entry fails Q5 (`QUALITY.md:43`) and Q6 (`QUALITY.md:50`).** Committed blob:
`grep -n 'self-report\|maintainer claim\|claims the work'` → no match; `grep -n 'extends\|Extends\|
agent-time-horizon\|webarena-task-spec-audit'` → no match. The entry quotes a maintainer's own
release notes and announcement without ever labelling them self-reports, and names nothing it
extends, while the lane already holds `knowledge/agent-time-horizon-and-task-validity.md` on the
same ground. The draft's `:24-26`, `:45`, `:145` (labels) and `:14-17` (extends) are the ready-made
wording.

### MEDIUM

**F3 — the committed receipts were produced by counter revisions that no longer exist; the frozen
7-field target now passes, but nothing on disk records the transition.** Timeline observed inside this
review: (i) at 03:46 the counter printed an eighth field —
`entries=1 … usedby_ok=1 verified_at=1 census=ok`, which is what
`corpus/evidence/round29-attempt2/adoption-measured.txt` still contains, and that line cannot satisfy
`plans/round-29-attempt2-claims.md:27` ("prints exactly" 7 fields); (ii) the file was rewritten at
03:50 (sha256 `949c367d…`, mtime 03:50) to print *exactly* the frozen seven fields, with the
access-date check still enforced but unprinted
(`re.search(r"^verified-at: " + … + r"$", text, re.MULTILINE)`; comment: "Exactly the frozen seven
fields; the access-date check gates without being printed"); (iii) my run of the current file gives
`entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`, `exit=0` — a
literal match. So the claim's target is met by the current artifact, but every receipt the round cites
was emitted by an earlier revision of that artifact, and `git diff plans/adoption_check.py` against
freeze commit `8c14a5d` now shows a substantially rewritten file (not only the M93 census-argument
line). Recommend: re-run the target command after the final counter edit and append that receipt
(R1) naming the counter's sha256, so closure can bind a receipt to the code that produced it.

**F4 — `writer: KengakuR29` is a placeholder.** Its own writer states so; Q14 makes the candidate
`writer:` an identity input and rejects a declared writer equal to a review seat's identity, and Q13
requires the Gate's cited reports to come from a seat other than the candidate's writer. As landed
(it has no `writer:` line at all) the identity check has nothing to read. Set the real writer (or
drop the line and record identity in the Gate).

**F5 — axis-H numbers carry no in-entry derivation, against the entry's own stated rule.** Landed:
"1 of 89 task directories (`caffe-cifar-10`) carries … neither time baseline" and "6 lines across 3
tasks write integer literals" — no command, while §Counts asserts "A row that carries a count must
carry the command that produced it" and supplies endpoints only for 92/89 and 109/108. Draft: `:77`
"one of the 89 task directories" likewise. The derivation does exist in-repo:
`.ufo/waves/round-29/attempt2/build/R29a2SrcS079.md:143-155` (88/89 carry both baselines;
`caffe-cifar-10` 0; six integer-literal lines across `count-dataset-tokens`, `reshard-c4-data`,
`train-fasttext`). Cite it, or paste the per-file count.

**F6 — withdrawn (self-correction).** I first recorded `usedby_ok` as satisfied by a single cell.
That was inferred from a range the `read` call had elided, not from code, and it is wrong: the current
file is all-of per entry —
`linked = all(row_id in registry and rel in registry[row_id][10] for row_id in entry["sources"])`
followed by `usedby_ok += 1 if linked else 0` (`plans/adoption_check.py:93-96`, comment "per-entry,
all-of: one linked row out of five is not a linked entry"). The property C1 asserts is enforced.
Kept in the report so no one acts on the retracted version; the registry itself also checks out —
an awk over `SOURCES.md:100-104` shows all five `used-by` cells name the entry.

**F7 — registry `recheck` equals `opened` on all five rows.** `SOURCES.md:100-104` carry
`opened = recheck = 2026-10-25`, so each row is due for recheck on the day it was written and carries
no forward cadence, while the entry says `90d … 2027-01-23` (draft `:7`) or `180d … 2027-04-23`
(landed `:7`). This follows from the frozen C2 clause 3 ("prose `recheck` cells are normalized to the
frozen access date"), and `gate-preappend.txt` shows the prose that was stripped
(`2026-10-23 — re-verify at the next upstream release`). The consequence is untracked: two cadences
for one source. Recommend the rows carry the entry's cadence, or the Gate record that the access
date *is* the normalization output.

### LOW

**F8 — quotation surface nits (no widening, no wrong claim).**
(a) Landed `:31` row D quotes `in download-youtube YouTube's constantly …`, but the served bytes read
`download-youtube␠␠YouTube's` (two spaces; `s090.html` offsets, chars `0x65 0x20 0x20 0x59` at
`banner`-independent position 17629-region). Words match (20 ≤ 25); the string is not byte-contiguous.
The draft's 18-word form *is* contiguous.
(b) Draft `:40` calls the S090 banner a "page footer" — it is the `text-right` paragraph immediately
before the "Hosted by / Stanford / Harbor / Laude" block, with 35 761 bytes of duplicated RSC payload
after it (`s090.html`, 53 390 bytes). "Closing banner before the Hosted-by line" is the locator a
re-reader can hit unambiguously.
(c) Draft `:39` axis label "Per-task canary" slightly narrows "unique canary string is present in task
files" (Q3's narrow-only rule allows narrowing, so this is a label-precision note, not a violation).

**F9 — a lane without a registry crashes the counter instead of scoring zero.**
`python3 plans/adoption_check.py --lane /tmp/r29a2-RevQuality/nothing --expect … --census` →
`FileNotFoundError: [Errno 2] No such file or directory: '/tmp/r29a2-RevQuality/nothing/corpus/SOURCES.md'`
(traceback, no counter line). The frozen do-nothing control is unaffected — it ran against the real
lane at `1f3b0f1`, where the registry exists, and its receipt
(`.ufo/waves/round-29/attempt2/control.nothing.txt`: `entries=0 … exit=1`) is consistent — but a
zero-scoring *empty* lane is only reported when the registry file happens to exist. One-line fix:
treat a missing `corpus/SOURCES.md` as an empty registry.

## Checks that passed (run, not assumed)

- **Counter, as the frozen target runs it (current artifact, `949c367d…`):** `python3
  plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census` →
  `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`, `exit=0` —
  a literal match for `plans/round-29-attempt2-claims.md:27`. Without `--census` the same command
  prints `census=skipped` and exits **1** (`census_code = 1  # an unrun census is not a pass`), so the
  census can no longer be skipped into a pass. Both behaviours were reproduced in this review; the
  8-field line quoted in `corpus/evidence/round29-attempt2/adoption-measured.txt` belongs to the
  superseded revision (F3).
- **M93 reproduces, so the post-freeze counter edit is justified** (I first suspected it was
  unnecessary; it is not). From the lane's own cwd: `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin kengaku-shokunin` → `exit=2`,
  `ERROR: unknown lane (not a dir, not in conf or root): kengaku-shokunin`; with `kengaku` → `exit=0`.
  From the fleet parent cwd the directory name *does* resolve (`exit=0`) — the failure is cwd-dependent,
  which is why the counter (which runs with `--lane .`) saw it. Rebuilding the pre-patch counter
  (`/tmp/r29a2-RevQuality/pre.py`, only the census argument restored) reproduces
  `… usedby_ok=1 census=fail`, `exit=1`. `scripts/sources-census.sh` is unmodified since 2026-10-19
  (`git status` clean, mtime 2026-10-19 21:22), so the failure is in the caller, as M93 says.
- **Every quote is located in bytes I re-read, at the stated line:** S077 line 29 (`Nop Validation`,
  "Doing nothing fails tests"), line 31 (`Cheat Trials`), line 95 (canary purpose sentence), line 244
  (Oracle restatement), line 301 ("The LLM-based analysis determines whether actual hacking
  occurred."); S078 line 75 (`## The locked protocol` item 2), line 99 (`## What changed from v1`),
  line 103 (hidden-test restoration), line 25 (sanitised history); `v2/GATE.md` line 1 heading
  "Release gate — SWE-bench Pro V2 (v2.0.0), 2026-09-22"; S079 line 1 `schema_version = "1.1"`,
  line 15 `difficulty = "hard"`, lines 18/19 the two baselines, line 22 `timeout_sec = 1800.0`
  (line 21 is the `[verifier]` header, and the landed `:3` no longer cites it);
  S080 line 27 news entry, `ab-testing/task_config.json` line 2 `needed_mcp_servers` / line 6
  `needed_local_tools`; S090 the anti-bot sentence and the GUID banner (both present in the served
  bytes; `publishedAt` count 0, supporting the "no date on the article page" bullet).
- **Artifact identity matches the lesson's own table exactly:** sha256
  `b0a7cb14…78b61` (41842 B), `dde4168f…8231f` (6858 B), `d7149606…98f24` (973 B), `d06165b5…a5b46a`
  (16883 B), `cbc50108…ef7911` (53390 B) — all five agree with `corpus/lessons/round-29.md`
  §Sources opened this round, including the byte counts.
- **Tier arithmetic:** `awk` over `corpus/SOURCES.md` → 75 A / 4 B / 2 C, 81 rows; the lesson's
  "Registry 76 → 81; tiers A 70 → 75, B 4 → 4, C 2 → 2" is consistent. S090's A (against the
  package's B) is justified in the Gate on SOURCES-contract grounds ("a first-party release
  announcement is a maintainer statement"), and the page-scoped reason for B is answered by the
  index date.
- **No `/tmp` or `local://` support inside either entry text** (`grep -n '/tmp\|local://'` → no
  lines); the round's receipts live in `corpus/evidence/round29-attempt2/` and
  `.ufo/waves/round-29/attempt2/`.

## Residual risk and verification gaps

1. **The entry file is a moving target.** Table 2 binds the committed blob `a18d4e87…` in `8cf7b60`;
   the working copy moved four times during the review (`4769ce2e…` → `a769fad8…` → `b80072f7…`, and
   further ` M` edits since). A later reader must re-hash before quoting any verdict, and Q13's
   reports must be re-bound to whatever hash finally stands.
2. **I did not re-fetch the five sources from the network.** I verified quotes against the bytes the
   round fetched (sha256-pinned to the lesson's table) and against the pins; whether the *live* `main`
   still equals the pin is the S0xx/RevQuoteS0xx seats' question, not a check I ran. Q10's "second seat
   re-opens each cited source" is therefore still supported only by those seats' reports.
3. **Q13/Q14 timing is out of my scope** and unverified here: the Gate at
   `corpus/lessons/round-29.md:169` cites reports and an admitting commit now exists (`8cf7b60`), so
   `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-29.md --commit 8cf7b60` is
   runnable — I did not run it, and no result of it should be inferred from Table 2's Q7 PASS, which
   tests only that the three surfaces share a commit.
4. **Q9/Q6-on-rejections:** the `benchmark-grader-semantics.md` rejection's reason rests on S093 being
   schema-malformed (`package-gate.txt` → `S093:escaped-pipe`); that is a Q9 property match I did not
   audit (RejectGate's lane).
