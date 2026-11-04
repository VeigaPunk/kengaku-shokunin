# Entry-hold review — `corpus/knowledge/tb2-hf-model-inference-offline.md` (EntryFalsifyR73, round 73 w1)

Reviewed 2026-11-03 at lane tip `255c261d` (master). Read-only seat: the entry, its SOURCES rows
and the lessons were not modified by this seat. This file is the item's assigned evidence write.

## 1. The bar, and the exact hold condition

QUALITY.md's admission bar is conjunctive: "An entry is admitted only when every row below
passes" (`corpus/QUALITY.md`, `## Admission bar — knowledge entries`), over Q1–Q17 plus the
later criteria that apply (here Q21).

- **Q10** (what the re-read is): before admission, a seat other than the entry's writer
  re-opens each cited source and confirms every quote location and every number.
- **Q13** (the gate that holds this entry): the admitting commit must already contain, in its
  own tree, every second-seat re-read report its `## Gate` row cites; the Gate cell names each
  report by repo-relative path; the report's seat is not the entry's writer; a generic
  reference ("wave-2 seats", "falsify seats") supports nothing; "A Gate cell never cites a seat
  that has not returned." Check: `python3 plans/gate_timing_check.py --lesson
  corpus/lessons/round-<N>.md --commit <admitting commit>` exits 0.
- **Q14** (who may re-read): qualifying roles are exactly `reviewer`, `scout`, `critic`,
  `sentinel`, `revenger`; identity means the registered seat; a report whose declared writer
  equals the candidate writer does not count.
- **Mechanism** (the lane's own enforcement): `plans/gate_timing_check.py` — `is_second_wave`
  accepts only a wave directory named `falsify` or matching `wave[-_ ]?0*2` (:241-243), and
  `resolve_citations`/`load_members` (:257-308) read report support and seat roles only from
  those directories in the **requested commit's tree** (Q15/Q16: commit-tree authority; a
  working-copy report cannot support an early commit).

The entry's own record of the hold (`corpus/knowledge/tb2-hf-model-inference-offline.md`):

- :5 `writer: KnowledgeEntryDraft`
- :6 `admission: hold — the QUALITY Q13/Q14 second-seat re-read is not yet on record; see`
  `corpus/lessons/round-71.md` `## Gate` `(Admission status).`

**What would discharge it, exactly:**

1. A returned report under `.ufo/waves/round-<N>/falsify/` (or a directory matching
   `wave[-_ ]?0*2`) from a seat whose registered role is one of the five Q14 roles and whose
   seat identity is not `KnowledgeEntryDraft`. Minimal shape: one such report; the Gate cell
   must cite every report it names, and one is enough for the gate.
2. The report re-opens S245/S246 — from the committed captures
   `corpus/evidence/round71/hf/instruction.md` (sha256 `29151c5b…dcc1`) and
   `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` (sha256
   `61a686d6…87857`) — and re-reads the entry's quote locations and numbers: the grader's
   107 lines / 4239 bytes; the four legs' spans (`:8-22`, `:25-31`, `:34-92`, `:95-107`); the
   six texts at `:36-44` and their labels; the instruction-to-leg map; the eight frozen vectors
   and the receipt of record (sha256 `136ec423…e6067`); the class-survey census line
   (`corpus/evidence/round62/class-survey.txt:11`); the `executed 3 of 8` → `executed 4 of 8`
   move in `SKILL.md`.
3. The round lesson's `## Gate` admission cell for this entry cites that report by
   repo-relative path, and the report is present in the admitting commit's tree (Q7 + Q13 +
   Q15/Q16).
4. `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-<N>.md --commit <admitting
   commit>` exits 0. Only then does `admission:` flip — append-only (R1), naming the report and
   this review's evidence path.

## 2. The entry's own bytes against that bar (line-by-line)

| row | verdict | evidence |
|---|---|---|
| Q1 triad opens | pass | :1 `source: S245 … — anchor: instruction.md:3-7,11-28 — sha256 29151c5b…dcc1; and S246 … — anchor: tests/test_outputs.py:8-107 — sha256 61a686d6…87857`; :2 `verified-at: 2026-11-03 (live re-fetch at the pin: instruction HTTP 200, 1264 bytes … grader HTTP 200, 4239 bytes …)`; :3 `recheck: pinned at 2fd12b88…` — the first three lines are exactly the triad |
| Q2 tier floor | pass | S245 (docs, tier A) and S246 (code, tier A), `corpus/SOURCES.md:260-261`, both "fetched live 2026-11-03 (HTTP 200 …)"; every load-bearing claim (leg laws, six texts, eight vectors, class row) rests on these two rows |
| Q3 claim inside its quote | pass | anchors carry the claims: leg 2's universal is anchored in the same sentence to `requests.get("http://0.0.0.0:5000")` `(:29)` "with no `raise_for_status`, no status assertion and no timeout" (:67-69); the oracle statement names its three `grep -c` probes (:45-49); verbatim quotes are short — the longest, K8's load failure, is ~20 tokens |
| Q4 negative space | pass | :206 `## What this does not establish` — nine bullets, including the falsifier: "the falsifier is direct: change the fixture's `hidden_size`/`num_hidden_layers` (keeping the directory, tokenizer and weight file loadable) and K1 stays `PPPP`" (:227-229); the unpriced hang mode is "declared here rather than priced" (:82-83) |
| Q5 sources labelled | pass | :237-239 "S245/S246 are the maintainers' own task text and grader — read at a pin, not endorsed" |
| Q6 extends, never duplicates | pass | :241-245 `## Carried forward` names the four entries it extends (pypi-server replay, kv-store-grpc, nginx-request-logging, grader-class census) |
| Q7 landed and discoverable | pass | index row `corpus/README.md:95`; coverage-map row `corpus/README.md:460` ("Partly discharged round 71"); landed with round 71 |
| Q8/Q9 rejections kept / reason follows evidence | pass (n/a) | the entry screens no sources; the one verdict recorded beside it — the hold itself — sits in `corpus/lessons/round-71.md` `## Gate` with its grounds |
| **Q10/Q13/Q14 second-seat re-read on record** | **FAIL — the hold** | no `falsify`/`wave-2` directory exists under `.ufo/waves/round-71/`, `round-72/` or `round-73/` (each holds `w1` only; listed 2026-11-03); measured: `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-71.md --commit master` → `gate_timing_check: FAIL: no admit rows in ## Gate of corpus/lessons/round-71.md at master`, `admissions=0 passed=0 failed=1`, rc 1 |
| Q21 pin named in recheck | pass | :3 `recheck: pinned at 2fd12b88aafdd04a52c298e3940bcb189f9766d6 (an immutable commit): …` |

**Universal clauses** (the item's question): the entry quantifies, but every universal is
scoped to the pinned 107-line grader whose sha256 the entry binds (:1, :11-13) and carries its
anchor or its declared limit in the same breath:

- :8 "every leg witnessed green and red" — bounded by the eight-case table it summarizes
  (legs 1-4 × K1-K8, each `P` and `F` witnessed in the receipt of record).
- :68-69 "any HTTP status — 200, 404, 500 — and any body pass" and :71-72 "(Any other transport
  exception is not caught, propagates, and also fails the leg.)" — code-path statements over
  leg 2's one unguarded `requests.get` (:29), anchored in the same sentence; the one input
  class that could escape them (a listener that never answers) is explicitly declared unpriced,
  not claimed (:80-83).
- :45 "The instruction states none of them." — over the six named texts only, backed by three
  named probes (`grep -c` on the committed capture returns `0` for `not bad`,
  `horribly beautiful`, `enjoyed this movie`; re-run by this seat 2026-11-03, all `0`).
- :78 "the grader cannot tell the difference" — scoped to what leg 2 inspects (no status, body
  or Flask-specific check), anchored at :67-76.

No unbounded universal stands without its anchor. Verdict of the byte-level test: **the entry
clears every byte-level row of the bar (Q1-Q9, Q21)**; the failing row is the process row
Q10/Q13/Q14, which the entry's own bytes cannot cure.

Spot-checks re-run by this seat against committed bytes (all reproduce the entry's claims):
`sha256sum` → instruction `29151c5b…dcc1`, grader `61a686d6…87857`; `wc -lc` → `107 4239`;
three instruction probes → `0 0 0`; `grep -c 'executed 4 of 8' SKILL.md` → `1`,
`'executed 3 of 8'` → `0`; the six literals verbatim at `test_outputs.py:36-44` including text
2's two-line split with the single space after `terrible`.

## 3. Verdict: `hold`

**Deciding line: Q13/Q14 — no returned second-seat re-read from a `falsify`/`wave[-_ ]?2`
directory exists in any round's tree (rounds 71, 72 and 73 each dispatched `w1` only), the
admission bar is conjunctive, and the lane's own gate check exits 1 at the reviewed tip.** The
bytes are not the problem; the missing artefact is one second-wave report, and no seat in this
round's one-wave shape can produce one.

Corroborating lane record — the promised discharge never happened and is now pre-committed to
slip again:

- `corpus/lessons/round-71.md` `## Gate` (Admission status): "Round 72 dispatches the falsify
  wave that admits the entry; the S245/S246 rows and the class-row move do not depend on the
  entry's admission."
- `corpus/lessons/round-72.md` `## Limits`: "The knowledge entry's admission is `hold`, not
  `admit`. No `w2`/`falsify` directory exists at draft time; the Q13 second-seat re-read is not
  on record, and this lesson is not one." (§Gate says the same for the round-72 provenance
  entry, which is held under the identical gate.)
- `plans/round-73-claims.md` non-claim 3: the entry "stays on `admission: hold` this round: no
  second-wave falsify seats exist to discharge Q13/Q14 under the run-15 one-wave shape; the
  hold is re-recorded, not silently lifted."

Note on the item's premise: the item text says "round-72 planned a 2–4 seat falsify second
wave". The committed record contains round-71's one-line promise of a round-72 falsify wave; no
committed lane byte this seat could find states a "2–4 seat" size (searched:
`plans/round-72-claims.md`, `corpus/lessons/round-72.md`, `LOG.md` round-72 section,
`.ufo/waves/round-72/w1-spec.json`). The checkable fact the hold rests on — no second wave
dispatched in rounds 71-73 — is verified above.

## 4. What the next round must add

1. Dispatch at least one second-wave seat (directory `.ufo/waves/round-<N>/falsify/` or
   `wave-2/`) whose registered role is `reviewer`, `scout`, `critic`, `sentinel` or `revenger`
   and whose seat is not `KnowledgeEntryDraft`.
2. That seat's report re-opens S245/S246 from the committed captures and re-reads every quote
   location and every number listed in §1 step 2 (Q10's scope sets the report's size).
3. The round lesson's `## Gate` admission cell for this entry cites the report by
   repo-relative path; report and admission land in the same commit (Q13/Q15/Q16).
4. Run `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-<N>.md --commit
   <admitting commit>` → rc 0; flip `admission:` append-only, naming the report and this file.

## 5. Paste-able blocks for the L1

### Round report (paste)

> **Entry admission (non-claim 3 re-record).** `corpus/knowledge/tb2-hf-model-inference-offline.md`
> stays on `admission: hold` at round 73. Deciding line: Q13/Q14 — the QUALITY second-seat
> re-read (roles reviewer/scout/critic/sentinel/revenger, seat ≠ writer `KnowledgeEntryDraft`)
> is still not on record from any `falsify`/`wave-2` directory; rounds 71-73 dispatched `w1`
> only, and `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-71.md --commit
> <tip>` exits 1 (`no admit rows … failed=1`) at the reviewed tip `255c261d`. The entry's bytes
> pass every byte-level row of the admission bar (Q1-Q9, Q21: triad, tier-A rows S245/S246,
> anchored claims, limits + falsifier, source labelling, extends-chain, index row, pin in
> recheck) and every quoted number this seat re-ran reproduces from committed bytes; only the
> second-seat process row fails. Next-round action: one qualifying w2/falsify report re-reading
> S245/S246, cited by repo-relative path in the admitting lesson's `## Gate` and committed in
> the admitting tree. Review: `corpus/evidence/round73/w1/entry-hold-review.md`.

### SCORECARD non-claim section (paste)

> - Entry `knowledge/tb2-hf-model-inference-offline.md`: hold re-recorded, not lifted (Q13/Q14
>   second-seat re-read still absent; `gate_timing_check` rc 1 at the reviewed tip). Bytes pass
>   Q1-Q9/Q21; re-run spot-checks all reproduce; discharge route and next-round action in
>   `corpus/evidence/round73/w1/entry-hold-review.md`.
