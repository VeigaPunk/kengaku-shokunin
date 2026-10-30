# R3KnowledgeSources review

Reviewer: R3KnowledgeSources-2 (reviewer; not either draft's writer).
Axes: novelty and calibration; no score admission recommended by this review.
Scope: drafted knowledge entry and SOURCES rows only. Frozen claims read in full. Bars: fleet CORPUS.md and QUALITY Q1–Q8, Q26, Q34.
LSP unavailable: `read xd://lsp` returned `No such tool`; fallback is literal text inspection, not semantic proof. Markdown/source-truth review needs no runtime rerouting or resume execution.

## Knowledge draft — not conformant for admission yet

Reviewed `.ufo/waves/round-54/w1/S1KnowledgeEntry/external-anchor-freeze.md` snapshot BF89 (85 lines).

### Medium — missing located quotations (Q3)

Offending lines 17–19: “The website's §How it Works describes existence-before evidence, not a content audit / or proof that measurements followed preregistration. The client README §Usage / separates pending calendar attestations from complete Bitcoin proofs.”

Locations are named, but the entry provides no anchored quotation for these load-bearing paraphrases. Sources reopened independently: https://opentimestamps.org/ §How it Works and https://github.com/opentimestamps/opentimestamps-client README §Usage.

Replacement text:

> Website §How it Works: “A timestamp proves that some data existed prior to some point in time.” Client README §Usage: “You can also upgrade an incomplete timestamp, which adds the path to the Bitcoin blockchain to the timestamp itself”. These describe existence-before and proof completion; they do not establish measurement ordering.

Each quotation is at most 25 words (whitespace splitting); the exact quote strings are short enough to inspect directly.

### Medium — lineage not explicitly extended (Q6)

Offending lines 9–11: “Round 53's `.ufo/waves/round-53/w3/C1CritOracle2.md` records the motivating / coordinated-history forgery: internally re-pinnable inputs can preserve FREEZE/ORACLE / agreement while changing the apparent freeze.”

The attack report is named, but no existing knowledge entry or coverage row is explicitly extended. `corpus/knowledge/tb2-presence-only-triage.md` lines 11 and 20 describe the pinned-input instrument and its integrity limitation.

Replacement text:

> Extends `corpus/knowledge/tb2-presence-only-triage.md` §Limits and contrary evidence: this note examines an external timestamp witness for the integrity limitation recorded in `.ufo/waves/round-53/w3/C1CritOracle2.md`; it does not supersede that entry's task-level findings.

### Low — absence observation lacks its sweep (CORPUS negative-claim rule)

Offending lines 62–63: “Directory enumeration found only `anchor.json` and `claims.ots`: no header or / explorer receipts at observation. Attestation height: **TBD, not established**.”

Replacement text:

> At draft review, `find corpus/evidence/round54/anchor -maxdepth 1 -type f -printf '%f\n'` returned `anchor.json` and `claims.ots` (2026-10-30); header/explorer receipts were not observed. This enumeration does not establish attestation height.

The reviewer independently obtained this two-file inventory with `glob` on the anchor directory; the proposed portable shell sweep is for the final entry and is not claimed executed here.

### Low — recheck omits external-source fetch action (Q1)

Offending line 3: “recheck: 180d — rerun the frozen command below on a clean landing-tip clone; inspect source receipts and chain assumptions separately.”

The cadence and local action exist, but retained receipts do not re-open the live sources cited in `source:`.

Replacement text:

> recheck: 180d — re-open the three cited URLs at their named sections; rerun the frozen command on a clean landing-tip clone; separately authenticate chain inclusion and compare retained source receipts.

## Entry positives and limits

First three lines have the required shape; source ids are explicitly integration placeholders, not invented assignments. No credential material observed in the inspected 85-line draft. Conditional witness/order wording and lines 75–85 avoid “unforgeable” or a claimed after-pass. Its static-conflict observations agree with literal counter locations: deserialize raw stream at 256/356; missing fifth helper argument at 216 versus definition 272; controls count unexpected passes at 188–192; root-equality requirement at 371; receipt-field requirement at 422–424. These are source inspection, not executed defects. Before receipt lines 2–6 supports the historical failure only. Digest/date values are attributed to commands or metadata; thresholds are identified as frozen requirements rather than measured results.

Q7 remains an integration gate: entry, README index and coverage row must land together. Q8 requires the round Gate's rejected candidates; draft alone cannot establish that inventory. Q26/Q34 govern registry integration and cannot be certified from this entry. Resolve source placeholders only when L1 assigns unused ids. Do not promote the entry's pending state to evidence of C1 success.

## SOURCES draft — text/shape conformant; admission conditional

Final reviewed snapshot: `.ufo/waves/round-54/w1/S2SourcesRows/rows.md` 551D. Earlier 34F8 overclaims and quote-count assertions were superseded before this final review; they are not findings against 551D.

Executed the explicitly requested awk check (2026-10-30):

```sh
awk -F'|' '/^\|[[:space:]]*(TBD-)?S[0-9][0-9][0-9]+[[:space:]]*\|/ {rows++; if(NF!=13){bad++; print "bad_line=" NR " NF=" NF}} END{print "rows=" rows+0 " malformed=" bad+0; exit (rows==0 || bad!=0)}' .ufo/waves/round-54/w1/S2SourcesRows/rows.md
```

Output: `rows=6 malformed=0`, exit 0. This proves 11-cell arity for each placeholder row and catches additional literal pipe delimiters; it is not source-truth or admission proof. The optional `TBD-` matters: a real-id-only selector would silently inspect no proposed rows.

Independent Python data inspection of `rows.md` extracted each `^- Quote: “(.*?)”` and applied `len(q.split())`: `quote_word_counts=13,19,10,11,10,10`, `quotes_over_25=0`. It parsed placeholder rows with `line.split('|')[1:-1]`: ids are TBD-S198 through TBD-S203; `row_sha256_outside_anchor=0`. These are draft checks, not production corpus counters.

Collision sweep: literal `grep` tool pattern `^\|[[:space:]]*S(198|199|200|201|202|203)[[:space:]]*\|` over `corpus/SOURCES.md` returned `No matches found`. No current production-id collision observed; repeat allocation at integration because other seats can propose ids. Placeholder ids are explicitly not valid final registry ids.

Reopened all canonical sources independently, including:
- https://opentimestamps.org/ — How it Works; saved HTML line 212 matches.
- https://github.com/opentimestamps/opentimestamps-client — README Usage; saved lines 82–83 match.
- https://github.com/opentimestamps/python-opentimestamps/blob/master/opentimestamps/core/notary.py — class docstring; saved line 240 matches.
- https://en.bitcoin.it/wiki/Block_hashing_algorithm — pre-example hashing sentence; saved HTML line 113 matches.
- https://developer.bitcoin.org/reference/block_chain.html — Block Headers and field table; saved HTML line 209 and 235–237 match.
- https://zenodo.org/records/22769923/files/184_phase22E_prereg_v1.md — section 9 step 2 matches the Greek quote; steps 1 and 3 support preregistration stamp → await Bitcoin anchor → acquisition ordering. The document's NOT LOCKED status is correctly disclosed. The file's own date is not independently verified deposit history.

Tier A is scoped to project/reference/depositor statements, not correctness or execution; supplemental wiki tier B is justified and not sole support. No credential material observed in the inspected draft. Teachings are bounded and falsifiable, and final verdicts do not call the mechanism novel or unforgeable. No additional actionable textual finding remains against 551D.

Admission gates intentionally still open:
- Q26: final line 77 explicitly acknowledges that hash-bearing evidence lives only in wave captures and requires committed `corpus/evidence/` bytes or committed SHA256SUMS membership before admission. This is not currently a passed Q26 check; no committed-blob digest counter was run here.
- Q7 / used-by: Python `Path(.../corpus/knowledge/external-anchor-freeze.md).exists()` returned `False`. The path is plausible but proposed, and current entry provenance cites only the three OTS sources. Integrate an entry citing each mined row, its index and coverage row together, or leave unused rows queued with used-by `—`. The draft explicitly makes mined status conditional, so this is a landing prerequisite, not an undisclosed claim.
- Q34: proposal adds new placeholder rows, not changes under existing ids. After assigning ids, never alter immutable row cells in place; corrections need new superseding rows. This review does not establish historical append-only compliance.
- Q8: row draft claims no exhaustive rejection inventory; the final lesson Gate must retain screened rejections and flip conditions.

## Residual risk and verification gaps

No C1 success, novelty increase, scoring-order proof, external chain authentication, or C2 execution is established by this review. The canonical frozen claim's replication-pricing rule at `plans/round-54-claims.md:111–115` must be applied to the relevant preregistration prior art; a published NOT LOCKED protocol establishes published procedure, not execution. Final source ids, capture commits, used-by citations, source digest membership, source census, admission commit timing and index/coverage integration remain L1 checks. This seat installed no tools, mutated no git state, created no scratch clone, and made no production edits.

Self-evaluation: accuracy 4/5 (direct source rereads and explicit non-execution limits; no committed digest membership check); completeness 4/5 (both drafts reviewed, final admission tree unavailable); clarity 4/5 (per-file verdict and severity-separated findings; report necessarily distinguishes multiple draft snapshots); actionability 5/5 (each finding has replacement text and landing gates name exact prerequisites); conciseness 4/5 (evidence detail makes this longer than a verdict-only review). Overall 4.2/5. Highest-impact improvements belong at integration: commit the evidence/index package, replace placeholders, and rerun admission counters on that actual tree. The user should regard this as a bounded draft review, not admission.
