# FSourceS064 — S064 source-row and Gate-anchor falsification (round 28)

Seat: `KengakuR28.FSourceS064` (scout; author-side, not outside closure).
Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Report trailer: `.ufo/waves/round-28/falsify/FSourceS064.md`.
Baseline: `b9b24796277020d1b9b01923b45313d6a565e664`. Build package per assignment context:
`18b192266389e8d6c74d0e1f1f2db337739e63dd` (not re-verified here).
Frozen candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, SHA256
`77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (recomputed, matches freeze).
Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md` is **absent** (not admitted).
No production edits, no builds/tests/linters, no tool installs or updates. My only write is this report;
my source capture is scratch-only at `.ufo/waves/round-28/scratch/FSourceS064/commonmark-0.31.2.html`.

Scope: new source row S064 (`corpus/SOURCES.md:86`) and its quote/anchor in the round-28 Gate
(`corpus/lessons/round-28.md:43`), plus its use by the append-only knowledge erratum
(`corpus/knowledge/extraction-policy-comparison.md:128-130`), the frozen candidate's source use, and
the nearby S066 access-limitation statement. Method: independent read-only reopen of the pinned URL,
byte hash, literal substring/word counts, cell parse, `git diff` against baseline, and one read-only
`python3 plans/registry_check.py --summary` probe.

## 1. Source reopen (observed)

| item | observation |
|---|---|
| URL | `https://spec.commonmark.org/0.31.2/#fenced-code-blocks` |
| Access | 2026-10-21, `curl -sS -L`, HTTP 200, 514698 bytes, effective URL `https://spec.commonmark.org/0.31.2/` |
| Body SHA256 | `c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d` (byte-identical to the OpenS054 scratch copy; OpenS054 also reports it equals the round-27 gate hash) |
| Version | `Version 0.31.2 (2024-01-28)`, HTML line 117 |
| Section anchor | `<h2 id="fenced-code-blocks" class="definition">`, HTML line 2726 (header text `4.5 Fenced code blocks`) |
| Quoted passage | HTML lines 2743-2744: “…and with at least as many backticks / or tildes as the opening code fence.” The containing paragraph starts at HTML line 2741 (“The content of the code block consists of all subsequent lines, until a closing code fence…”). |
| Supporting examples | Examples 124 and 125 at HTML lines 2858 and 2876, after the lead-in at line 2857: “The closing code fence must be at least as long as the opening fence:”. Example 124 closes a 4-backtick fence with 6 backticks; Example 125 closes a 4-tilde fence with 4 tildes. |
| Quote word count | **12** words (`at least as many backticks or tildes as the opening code fence`), independently counted; ≤25. |

The exact quote is present verbatim after whitespace normalization, both in the raw HTML and in
tag-stripped text. The source sentence preceding the fragment supplies the same-type clause:
“a closing code fence of the same type as the code block began with (backticks or tildes)…” (18 words);
the remaining words of that sentence are the length clause quoted above.

## 2. Row narrow tier/scope/teaches (observed)

Parsed `corpus/SOURCES.md:86` inside the Registry section (heading line 19; next section line 90): 11
content cells, no malformed/duplicate row.

| cell | value | check |
|---|---|---|
| source | CommonMark closing-fence length correction — pinned URL | exact URL and version; `#fenced-code-blocks` exists |
| kind / tier | `spec` / `A` | primary versioned specification for this scope; allowed values |
| scope | “exact closing-fence type and minimum-length rule” | supported: same type + at least opening length; source is a rendering grammar, not answer selection |
| anchor | “CommonMark0.31.2 §4.5 closing fence paragraph, examples124–125; reopened2026-10-21” | section/version correct; quote is in the §4.5 closing-fence/content paragraph at HTML 2741-2746; examples 124-125 are the length examples |
| teaches | supersedes S054's type/length shorthand — same character type and at least opening length, not necessarily equal; answer-selection rules lane-defined | supported by the source sentence at 2741-2744 and Examples 124-125; “not necessarily equal” follows from a longer fence closing in Example 124; answer-selection boundary is not a source claim |
| status / opened / recheck | `mined` / `2026-10-21` / `on-release` | cited row is mined; access date matches independent reopen; `on-release` is an established cadence in this registry (e.g. S005, S006, S052) |
| used-by | `corpus/lessons/round-28.md, corpus/knowledge/extraction-policy-comparison.md` | both files exist and contain standalone S064 at lesson lines 17 and 43 and knowledge line 128 |

The Gate row at `corpus/lessons/round-28.md:43` repeats the same 12-word quote, URL, date, and location;
M68 at line 17 records the supersession without rewriting S054. `S054`'s row is byte-identical to
baseline: baseline and current row hashes are both
`d996ae3c6f84283ccfc095eedd3268002b883e5702b8e8175ebe6e92c4df82c2`.

## 3. Frozen candidate source use (observed)

The candidate draft's `source:` line lists S061, S062, S063 only (task JSON, evaluator code, helpers).
A literal scan of the full draft finds **no** `S064`, `S065`, `S066`, `CommonMark`, or `fence` mention.
This is consistent with the row's declared used-by (lesson + existing extraction-policy knowledge, not
the candidate) and with the C1/C2 partition: S064 is a calibration-correction source, not a WebArena
task-spec source. The canonical candidate path is absent, so there is no canonical-byte use to check.

## 4. Old-knowledge append-only correction (observed)

`git diff b9b2479 -- corpus/knowledge/extraction-policy-comparison.md` is `+24/-0`: a new
`## Round28 source-location and authority errata (2026-10-21)` section beginning at line 116, with the
S064 paragraph at lines 128-130:

> S064 clarifies CommonMark's rule: same fence character type, closing length **at least** the opening
> length (not necessarily equal).

> This leaves the paragraph's “fence-length rules” limitation true while superseding S054's ambiguous
> shorthand.

No earlier content is deleted or changed; this is an append-only erratum. The limitation at line 51
(“E6 is not a CommonMark parser: it omits valid info strings and fence-length rules (S054)”) remains
true: `plans/parser_policy_compare.py:36` defines `FENCE_ANY` as exactly-three-backtick, non-greedy
closing with no fence-length or info-string enforcement, so the corrected at-least rule does not make
the lane's parser CommonMark-conformant.

The erratum adds no new reference edge to any frozen13 ID: S049/S050/S051 were already cited in this
file, while S064/S065 are outside the frozen population. Read-only
`python3 plans/registry_check.py --summary` reports
`source_rows_checked=13 knowledge_files_expected=35 reference_links=12 mismatch_sources=0 finding_count=0 exit=0`,
identical to `corpus/evidence/round28-calibration/registry-summary.txt`. `population.json` contains
S054 but not S064, consistent with Amendment 4 (“new rows do not enter its verdict”).

## 5. Findings

### F1 — Admitted S064 quote, location, and count are exact. PASS.

The Gate/row quote is a 12-word verbatim fragment of the §4.5 closing-fence paragraph. The anchor’s
“closing fence paragraph” names the paragraph that defines the closing fence (HTML 2741-2746);
Examples 124-125 (HTML 2858/2876) illustrate the same minimum-length rule. The label compresses two
locations—the quoted wording is in the paragraph, while the examples are far below it in the same
section—but it is not a false location or a paraphrase. No row change is required.

Precision note (not a failure): a maximally literal anchor could say “§4.5 content/closing-fence
paragraph (HTML 2741-2746), length lead-in/Examples 124-125 (HTML 2857-2891).” The current label is
defensible because both parts identify the same rule.

### F2 — Row cells and used-by are supported. PASS.

All 11 cells match the source and the lane’s allowed values; both used-by files exist and cite S064;
the row is inside the Registry section; S054 remains byte-identical to baseline while S064 carries the
correction. No hidden immutable-cell edit or status drift was found.

### F3 — `build/OpenS054.md`’s second located quote is 32 words, not the claimed 25. Non-blocking defect in the supporting report.

`build/OpenS054.md` states a passage beginning “until a closing code fence of the same type as the code
block began with (backticks or tildes)…” (18 words) and continuing “…and with at least as many backticks
or tildes as the opening code fence” (14 words) — then says “This passage is 25 words.” Independent
count of the combined passage is **32**. The admitted Gate/row quote is a distinct 12-word fragment of
that sentence, so the lesson’s “Every listed quote is ≤25 words” rule is satisfied for the admitted row;
the build report’s claimed count is nonetheless false. L1 should append a correction/annotation to
`build/OpenS054.md` (or disclose the 32-word passage as over-limit analysis, not a row quote). This does
not require a row edit and is not load-bearing for S064’s admitted quote.

### F4 — Append-only correction and C2 counters are intact. PASS.

The knowledge erratum is +24/-0, explicitly labeled errata, leaves the original numeric/behavioral
content intact, adds no new frozen13 edge, and preserves S054’s limitation. The delivered C2 summary
still reports 13 rows/35 paths/12 links/0 mismatches/exit0. The new S064 mention in a frozen knowledge
path is outside the frozen13 `source_ids` and is ignored by the instrument, as Amendment 4 specifies.
No C2 population or count was silently changed.

### F5 — Candidate source use is correctly absent. PASS.

The frozen candidate does not cite S064 and S064’s used-by does not claim the candidate. This matches
the C1/C2 partition and the row’s calibration-correction role. Candidate SHA256 matches the freeze;
canonical path is absent.

### F6 — Adjacent S066 boundary check (not my row; noted for the S066 seat/L1).

Without any live publisher call, I verified the local archived publisher PDF
`.ufo/waves/round-28/scratch/OpenS038/wb20261004.pdf`, SHA256
`fc935f40a6f58cb7fea9407490a768fd63078eaf46ccd3b40b260d109de82e8c`, matching the lesson and
`build/OpenS038.md`. The Discussion p.1677 sentence “the proposed methods assume that sensitivity and
specificity are known exactly” is present (ligature/hyphenation normalized), 11 words. The lesson’s
access limitation is exact: live DOI/publisher fetches returned 429; the opened artifact is a
2026-10-04 Internet Archive capture of the publisher PDF, and live publisher HTML was corroborating,
possibly cached, not a live PDF download. I made no live S066 request.

One adjacent metadata observation: the S066 row’s anchor cell (`SOURCES.md:88`) lists “Introduction/
Methods p.1675 and Conclusion p.1677” but not “Discussion p.1677”, although the quoted known-vs-
estimated caveat is in the Discussion; the lesson Gate and the attribution-interval erratum do name
Discussion p.1677 correctly. This is for the S066 owner/L1, not a defect in S064.

## 6. Observed / inferred / unresolved

Observed: URL/200/bytes/hash/version/anchor; quote substring/12-word count; paragraph and example
locations; row cells and used-by; draft absence of S064; append-only +24/-0 erratum; S054 row identity;
C2 summary 13/35/12/0 exit0; OpenS054 32-word quote claim; archived S066 PDF hash and 11-word quote.

Inference: the anchor label’s compression of the quoted paragraph and Examples 124-125 is a stylistic
precision issue, not a false location; the lesson’s “L1 reopened” wording has no separate L1 receipt in
the files I read, but my independent reopen and the OpenS054 capture are byte-identical.

Unresolved: no material S064 gap. The only open calibration item is F3’s false claimed count in the
supporting build report and F6’s adjacent S066 anchor omission; both are L1/other-seat dispositions.
No production change was made by this seat.

VERDICT: PASS

Verdict scope: PASS applies to the S064 row and its Gate quote/anchor: the source was independently
reopened at the pinned version, the 12-word quote is exact and within the word limit, the tier/scope/
teaches/status/used-by cells are supported, the frozen candidate correctly does not use S064, and the
old-knowledge correction is a genuine append-only erratum with unchanged C2 counters. It is not a
PASS for the 32-word supporting quote in `build/OpenS054.md` (F3), which should be annotated, and not a
PASS for any S066 row detail (F6). This is author-side evidence, not outside closure.
