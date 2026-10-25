# R29a2RevQuoteS078 — independent verification of the S078 quotes and the release gate

Seat: `L1Kengaku29.R29a2RevQuoteS078` (leaf reviewer; no dispatch, no production edits).
Scope: re-fetch `v2/README.md` and `v2/GATE.md` at the pinned commit myself, verify the two claimed
S078 quotes with line number + word count, and report the GATE.md heading, date, oracle and nop cells
verbatim. Access date **2026-10-25**. Scratch: `/tmp/r29a2-revquoteS078/`.

Verdicts are stated per quote. Nothing was read from a sibling's artifact before fetching; §6
reconciles against `R29a2SrcS078.md` *after* the fact and records one disagreement.

## 1. What was fetched, and why these bytes are the pin

Pinned commit `66f92766bba642462d4bbe5479e83f91f9211862` (tag `v2.0.0`).

```
curl -sS -o README.md -w '%{http_code} %{size_download}\n' \
  https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/v2/README.md
  -> 200 6858
curl -sS -o GATE.md -w '%{http_code} %{size_download}\n' \
  https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/v2/GATE.md
  -> 200 1659
```

| file @ pin | bytes | lines | sha256 (mine) | sha256 in `v2/SHA256SUMS` @ pin | matches |
|---|---|---|---|---|---|
| `v2/README.md` | 6858 | 126 | `dde4168fed17ca1ea00b26a93aca78dad43c7b3f981b93a2872428259428231f` | `dde4168fed17ca1ea00b26a93aca78dad43c7b3f981b93a2872428259428231f` | **yes** |
| `v2/GATE.md` | 1659 | 18 | `7c30b8d6aef5ea7413831ac5618220f8c01ff15439bc6732a25ceaeb2c401e71` | `7c30b8d6aef5ea7413831ac5618220f8c01ff15439bc6732a25ceaeb2c401e71` | **yes** |

The maintainer's own manifest (`v2/SHA256SUMS`, 1176416 bytes, 6436 lines, sha256
`9d84f8507c89241d42d8b3ef911600a1ec75dbbb32687ce9b45b93318502c0bd`) names both files with
exactly these digests, so the bytes quoted below are the publisher-checksummed bytes, not merely
"what raw.githubusercontent returned". A third, unrelated manifest entry was spot-checked to prove the
manifest is live, not stale:

```
tasks/instance_NodeBB__NodeBB-00c70ce7b0541cfc94afe567921d7668cdc8f4ac-vnan/task.toml
  manifest=e05817107e10163e3e903dd314a26abbae5dca429d2193f4884689c9f67ce926
  actual  =e05817107e10163e3e903dd314a26abbae5dca429d2193f4884689c9f67ce926   MATCH=True
```

Drift check (pin vs `main`, 2026-10-25): all three files byte-identical
(`README.md` `dde4168f…` both, `GATE.md` `7c30b8d6…` both, `SHA256SUMS` `9d84f850…` both), so the
citation anchor is still current and there is nothing for the 180 d recheck to catch yet.

Commit provenance (`api.github.com/repos/scaleapi/SWE-bench_Pro-os/commits/66f9276…` -> HTTP 200):
sha `66f92766bba642462d4bbe5479e83f91f9211862`, committer date `2026-09-22T21:00:20Z`, message head
`Merge pull request #119 from scaleapi/release/v2.0.0`, and `GET /tags` returns
`v2.0.0 66f92766bba642462d4bbe5479e83f91f9211862`. The pin *is* the release tag.

## 2. The two claimed quotes — PASS/FAIL

Word counts are whitespace-split tokens (`len(text.split())`), the same convention the lane states at
`corpus/QUALITY.md:31-33` ("anchored quote (≤25 words, with location)"). `exact` below means
`quote in file_bytes` was true, `str.count == 1`.

| # | claimed quote | verdict | location | words | match |
|---|---|---|---|---|---|
| Q1 | `731 -> 642 tasks: 89 dropped after review.` | **PASS** | `v2/README.md:99` (§ `## What changed from v1`, bullet 1) | **8** | exact, count 1 |
| Q2 | `The verifier never runs in the agent's sandbox.` | **PASS** | `v2/README.md:75` (§ `## The locked protocol`, item 2) | **8** | exact, count 1 |

Both are ASCII (Q1 42 chars, Q2 47 chars), both are ≤25 words, and neither occurs anywhere in
`GATE.md` (count 0 in GATE for both) — so the file+line pairing in any future row is unambiguous.

Raw source lines, for the scribe to copy rather than retype:

```
README:99: - 731 -> 642 tasks: 89 dropped after review. Same repositories, same base commits.
README:75: 2. **The verifier never runs in the agent's sandbox.** The locked agents capture the agent's `git diff` as
```

Q2 note: the sentence is wrapped in `**…**` in the source, but the quote text excludes the markers and
is a literal substring of the raw line (`'The verifier never runs in the agent\'s sandbox.' in line` ->
True, apostrophe is U+0027 ASCII, not U+2019). No fold is needed for Q1 or Q2.

Sentence-boundary check: Q1 ends at `review.` and the next byte is `' Same repositories, '` (a new
sentence in the same bullet); Q2 ends at `sandbox.**` and the next byte is `' The locked agents '`.
Neither quote spills past the sentence it names.

## 3. The release gate — GATE.md cells verbatim

`v2/GATE.md` is 18 lines; its only two headings are the H1 (line 1) and `## Infrastructure retries
(first pass)` (line 12).

**Heading (GATE.md:1), verbatim — contains a literal U+2014 em dash:**

```
# Release gate — SWE-bench Pro V2 (v2.0.0), 2026-09-22
```

- Non-ASCII codepoints in that line: `['0x2014']` (em dash only). Substituting `-` for `—` still
  matches the campaign linter's typographic fold but **fails** a byte-exact check, so the em dash must
  be preserved.
- Heading text without the `#` marker is **8 words** (with the marker, 9) — both ≤25.

**Date: `2026-09-22`** — the only `YYYY-MM-DD` token in the file
(`re.findall(r'\d{4}-\d{2}-\d{2}', GATE.md)` -> `['2026-09-22']`), and it equals the pinned commit's
committer date `2026-09-22T21:00:20Z`. It is the **gate's own run date, not this round's access date**;
the entry's Gate block must keep `2026-10-25` as access/verified-at and `2026-09-22` as the gate date.

**Oracle cell (GATE.md:7), verbatim:**

```
| Reference patch (`-a oracle`) | **642 / 642** tasks resolved |
```

**Nop cell (GATE.md:8), verbatim:**

```
| Empty patch (`-a nop`) | **642 / 642** tasks unresolved (0 spurious passes) |
```

Row-level word counts (whitespace tokens, pipes included): oracle **12**, nop **15**; content
tokens as cited by the entry: oracle **5**, nop **8**. All ≤25. Both rows are exact
(`gate.count(row) == 1`) and identical rows recur at `README.md:92` / `README.md:93`.

Supporting cells at the same gate, for completeness (exact, count 1 each):
- `GATE.md:3` — `Run on the exact tree published under `v2/tasks/` with Harbor 0.22 on Modal, 50 concurrent, no registry credentials.`
- `GATE.md:9` — `| Images | `ghcr.io/scaleapi/swe-bench_pro-v2`, pulled anonymously; 642 manifests verified, 211 rebuilt images digest-identical to the graded originals |`
- `GATE.md:10` — `| Infrastructure retries | oracle 3 trial(s), empty-patch 3 trial(s) hit Modal sandbox errors on the first pass and passed on re-run (no task-level failures) |`

### Independent corroboration of the `642` in those cells

The number is not only asserted in prose; it is countable at the pin:

```
GET /contents/v2/tasks?ref=66f9276…  -> 642 entries, type_counts {'dir': 642}
v2/SHA256SUMS                        -> 6436 entries; 6420 under tasks/; 642 distinct task dirs
v2/hard51_ids.txt                    -> 51 lines (matches "HARD-51")
731 - 642 = 89                       -> matches Q1's arithmetic
```

## 4. Secondary S078 fragments the C1 entry cites — fold-level verdicts

Not in the ticket's acceptance, but the entry cannot be admitted on S078 alone; each S078 fragment in
the staged entry (`shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-task-validity-checklist.md`
lines 22-31) was checked against the same bytes. Fold names are the campaign ladder documented at
`shokuknow/.ufo/waves/corpus-expansion-1/quote-lint.py:18-19` and implemented at `:531-566`
(`exact → whitespace-normalised → case-folded → all-whitespace-removed → markdown-stripped → NFKC →
typographic-fold`). I re-implemented those pure fold functions in `/tmp` rather than running the
campaign tool (it writes under shokuknow).

| # | fragment | words | doc | strongest fold that matches | verdict |
|---|---|---|---|---|---|
| Q3 | `529 problem statements rewritten so that every graded assertion traces back to a sentence in the text` | 17 | README | whitespace-normalised | **PASS (fold 2)** |
| Q4 | `642 / 642 tasks resolved` | 5 | GATE | markdown-stripped | **PASS (fold 5) — not literal** |
| Q5 | `642 / 642 tasks unresolved (0 spurious passes)` | 8 | GATE | markdown-stripped | **PASS (fold 5) — not literal** |
| Q6 | `hidden-test paths are restored or removed before the test patch is applied` | 12 | README:103 | exact | **PASS** |
| Q7 | `checked out at the task's base commit with a sanitised git history` | 12 | README:25-26 | whitespace-normalised | **PASS (fold 2)** |
| Q8 | `Probe before you trust.` | 4 | README:79 | exact | **PASS** |
| QH | `Release gate — SWE-bench Pro V2 (v2.0.0), 2026-09-22` | 8 | GATE:1 | exact | **PASS** |

Why Q3/Q7 match only at fold 2 — the source hard-wraps them:

```
README:100: - Instructions: 529 problem statements rewritten so that every graded assertion traces back to a sentence in the
README:101:   text (only problem statement, requirements and interfaces changed); each correction was implemented blind by a
README:25:  repository is at `/app` (a few tasks use `/testbed`), checked out at the task's base commit with a sanitised git
README:26:  history (no fixing commit, stray refs, stashes or hooks).
```

Why Q4/Q5 match only at fold 5 — the source bolds the number, so the de-emphasised form is not present:

```
GATE:7: | Reference patch (`-a oracle`) | **642 / 642** tasks resolved |
GATE:8: | Empty patch (`-a nop`) | **642 / 642** tasks unresolved (0 spurious passes) |
```

`gate.count('642 / 642 tasks resolved') == 0`. The literal alternatives both exist and are exact:
`**642 / 642** tasks resolved` (5 w) or the full row (12 w); same for nop (`… **642 / 642** tasks
unresolved (0 spurious passes)`, 8 w; full row 15 w).

## 5. Findings, by severity

**F1 (HIGH, operability — cue for the scribe).** Q4 and Q5 as written in the staged entry are **not**
literal substrings of `GATE.md`; they exist only after the `**`-stripping fold. If the lane's Q3/Q10
check ("claim stays inside its quote", `corpus/QUALITY.md:31-33`, and the second-seat "every quote
location and every number against it", `QUALITY.md:77`) is done with a plain `grep -F`, these two look
like fabrications. Cite the full row (`GATE.md:7`, 12 w; `GATE.md:8`, 15 w) or the marked-up cell
(`**642 / 642** tasks resolved`, 5 w) — both are exact, `count == 1`, and still ≤25 words.
**Shipped-state note:** the landed entry's registry anchor (`corpus/SOURCES.md:101`) drops the
quotation marks and glosses the cells numerically (`oracle 642 / 642 resolved and nop 642 / 642
unresolved`), which is safe; the de-emphasised fragment survives only at
`corpus/knowledge/benchmark-task-validity-checklist.md:40-41`, inside quotation marks — see F9.

**F2 (MEDIUM, operability — does not apply to shipped bytes).** Q3 and Q7 span hard wraps
(`README.md:100→101`, `README.md:25→26`), so they are byte-exact only after whitespace normalisation.
Safer single-line forms from the same sentences: `529 problem statements rewritten so that every
graded assertion` (10 w, README:100) and `checked out at the task's base commit` (7 w, README:25).
The landed entry cites both axes by section reference instead of quoting them (`entry:26`
"S078 §What changed from v1"; `entry:31` "S078 sanitised-history clause"), and the landed row quotes
only Q1 and Q2, so this finding is a guardrail for any later revision rather than a live defect.

**F3 (LOW, anchor fidelity — CLOSED on landed bytes).** The campaign entry's S078 anchor says
`` `# What changed from v1` `` and `` `# The locked protocol` ``, but the document's headings are
level 2: `README.md:97` `## What changed from v1`, `README.md:70` `## The locked protocol`. The
location is still findable; the heading depth is off by one. (`#` on README:53 and :66 is inside a
bash code block, not a heading.) The landed anchor avoids the problem by citing `§What changed from v1
line 99` and `§The locked protocol line 75` with no heading marker (`corpus/SOURCES.md:101`), so this
finding is closed on shipped bytes.

**F4 (LOW, provenance hygiene — CLOSED on landed bytes).** The staged/campaign entry carries
`verified-at: 2026-10-23` and `recheck: 180d … (ran 2026-10-23)` (campaign entry lines 7-8). C1's
re-grounding duty (`plans/round-29-attempt2-claims.md:39-42`) requires this round's `2026-10-25` and
this round's located quotes; that campaign copy is stale by construction and must not be copied
through. The landed entry already satisfies this (`verified-at: 2026-10-25`, entry:7; row
`opened = 2026-10-25`, `corpus/SOURCES.md:101`), so this finding is closed and is recorded only so the
stale campaign dates are not reintroduced.

**F5 (INFO, honest limits on the numbers).** `642` is independently reproducible from the tree (§3).
`731` is **not** verifiable from this repository — it appears only as maintainer prose
(`README.md:7` "original 731 tasks", `README.md:99`) with the data shipped on HuggingFace config `v1`.
So `89 dropped` is arithmetic on a maintainer-asserted 731 (`731-642 = 89` is internally consistent,
but the 731 itself is a self-report). The row's `teaches`/`scope` should attribute the 89 to the
maintainer's release note rather than to a count this lane reproduced.

**F6 (INFO, what the gate is).** `GATE.md` is a maintainer self-report of a run on Modal with Harbor
0.22. I verified the document's identity (checksummed at the pin), its internal consistency (642
oracle rows = 642 tree dirs, 0 spurious passes, dated `2026-09-22` matching the release commit), and
that the tree it claims to gate has 642 task dirs. I did **not** re-run the gate, so nothing here
certifies that the run produced those results — only that the published instrument and its numbers are
as quoted.

**F7 (INFO, registry state — state at review start).** When this review began, `corpus/SOURCES.md`
had 76 id rows (`S001`–`S076`) with no `S077`–`S090` row
(`grep -cE '^\| S(077|078|079|080|090) ' corpus/SOURCES.md` -> `0`) and
`corpus/knowledge/benchmark-task-validity-checklist.md` did not exist (`ls` -> No such file or
directory), so the append was genuinely new; `.ufo/waves/round-29/attempt2/adoption-expect.json`
expects exactly that one path with `["S077","S078","S079","S080","S090"]`. Both files landed from
sibling seats during the review — the shipped state is assessed in §5b, which supersedes this
paragraph for everything except the "was the append new" question.

## 5b. The landed entry — same checks against shipped bytes

`corpus/SOURCES.md` and `corpus/knowledge/benchmark-task-validity-checklist.md` were written by
sibling seats while this review ran (both were absent when I started: 76 rows `S001`–`S076`, entry
file missing). So the checks below run against the **shipped** bytes, which is what matters. The
landed artefacts are already re-grounded correctly on the access date — `verified-at: 2026-10-25`
(entry:7), `recheck … (next due 2027-04-23)` (entry:7), row `opened = 2026-10-25`
(`corpus/SOURCES.md:101`), and the anchor now carries line locators
(§What changed from v1 line 99, §The locked protocol line 75) instead of the campaign's section-only
anchor. F4 is therefore **closed** on the landed bytes.

Three defects remain in the landed bytes, all reproduced by command:

**F8 (MEDIUM, accuracy in the registry row).** The row's anchor cell annotates the S078 quotes with
word counts, and the Q2 count is wrong:

```
row cells: 13 => columns 11
anchor: … §What changed from v1 line 99: "731 -> 642 tasks: 89 dropped after review." (8 words);
        §The locked protocol line 75: "The verifier never runs in the agent's sandbox." (9 words); …
Q1: words=8 chars=42        Q2: words=8 chars=47
```

`"The verifier never runs in the agent's sandbox."` is **8** whitespace tokens, not 9
(`The|verifier|never|runs|in|the|agent's|sandbox.`); Q1's `(8 words)` is correct. The fix is `(9 words)`
→ `(8 words)`. This is the row's own evidence annotation, so a wrong count here is a wrong number in
the artefact the C1 counter reads — exactly what `corpus/QUALITY.md:77` makes a second seat re-read.

**F9 (MEDIUM, quote widening in the entry body).** `corpus/knowledge/benchmark-task-validity-checklist.md:39-41`,
verbatim:

```
- S078's release gate ships both triviality bounds together: the reference patch resolves
  **642 / 642** and the empty patch resolves **0 / 642 → "642 / 642 tasks unresolved
  (0 spurious passes)"**. Axes B and C are therefore checkable on one page, per release.
```

Two problems in the same span. (a) The quoted fragment `642 / 642 tasks unresolved (0 spurious
passes)` is **not** in `GATE.md` — `g.count(...) == 0`; the source bytes are
`**642 / 642** tasks unresolved (0 spurious passes)` (`count == 1`, `GATE.md:8`), so the quotation
marks enclose a de-emphasised rewrite, not the published text. (b) `0 / 642` is a **derived** number —
`GATE.md.count('0 / 642') == 0`. It is a sound inference (642 of 642 unresolved ⇒ 0 resolved, and the
cell's own `(0 spurious passes)` says the same thing), but it sits inside the same bold span as a
quotation, so a reader can take it for the maintainer's words. Fix: keep `0 / 642` outside the
quotation marks and as prose ("the empty patch resolves none of them"), and quote either the full row
or `**642 / 642** tasks unresolved (0 spurious passes)`.

**F10 (INFO, registry cadence vs entry cadence).** The row's `recheck` cell is the access date
(`2026-10-25`, same as `opened`), while the entry's frontmatter states the 180 d cadence with
`next due 2027-04-23`. That is consistent with C2 item 3 (a prose `recheck` is normalised to the
frozen access date and the stripped prose reported separately), so it is not a defect — but the
registry row no longer carries the cadence, and only the entry does. The lane should confirm that is
the intended split rather than a lost field.

Everything else the landed entry cites from S078 is exact or fold-2 at worst, per §4: the Q2 quote at
`entry:30` occurs exactly once in the pinned README (`e.count(q2) == 1`), and the gate heading, oracle
number and nop number in the row's anchor and in `entry:35` are numerically correct (`642 / 642` both
sides, `2026-09-22`).

## 6. Reconciliation with `R29a2SrcS078.md` (read after my own fetch)

Agreement: same two digests, same manifest hash `9d84f850…`, same sizes, same line numbers and word
counts for Q1 (README:99, 8 w), Q2 (README:75, 8 w) and the gate heading/cells, same date distinction,
same registry gap.

One disagreement, and it is the reason F1 exists: that report's §2 labels the *de-emphasised* cell
forms `642 / 642 tasks resolved` and `642 / 642 tasks unresolved (0 spurious passes)` as "LOCATED"
without naming a fold. Measured here: `GATE.md.count('642 / 642 tasks resolved') == 0`; the only
literal forms are `**642 / 642** tasks resolved` and the full row. Its §3 table is careful about the
wrap for Q7 but marks Q3 "PRESENT" without saying it too spans `README.md:100→101`. Both are recoverable
by the scribe; neither is a fabrication, and neither forces a refusal under C1's kill rule.

## 7. Tooling record

No tool installs or upgrades were needed or performed — `curl`, `python3`, `sha256sum`, `grep` only. No
pacman/uv/npm/cargo transaction was attempted, so the host-wide pacman pause was not engaged. No
campaign tool under `/home/vgpnk/Projects/shokuknow` was executed (the fold functions were re-implemented
locally from `quote-lint.py:531-566`); nothing outside this report was written under the lane, and
nothing at all was written under `/home/vgpnk/Projects/shokuknow` or any sibling lane.

**Durability.** Scratch is `/tmp/r29a2-revquoteS078/` (`README.md` 6858 B
`dde4168f…`, `GATE.md` 1659 B `7c30b8d6…`, `SHA256SUMS` 1176416 B `9d84f850…`) and it is
**ephemeral by design**; nothing in this report depends on it surviving. Every cited fact is either
inlined here (line numbers, word counts, verbatim cells, manifest digests) or re-derivable with the
exact three `curl` commands in §1 at the pinned commit `66f92766…`, whose own `v2/SHA256SUMS` lets a
later reader confirm the refetched bytes match the digests quoted above. This report body — not any
scratch tree — is the evidence locus.
