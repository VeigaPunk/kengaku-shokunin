# R30ConnSibling — roster-fit scan: does the contamination-card surface belong to another province?

Seat: connector, round 30 (kengaku, hyaku run 6, 2026-10-25). Leaf: no subagents, no production edits.
Access date for every source and every repo row read here: **2026-10-25**.

## Verdict

**No overlap.** The per-benchmark contamination-transparency card and its Q1–Q8 gate sit inside
kengaku's province, and no sibling row is contested by C1. The card moves a frontier bullet this lane
already owns (`corpus/README.md:272`, `PROVINCE.md:125`), and every landable neighbour either refuses
evaluation claims toward kengaku by its own text or holds a homonym ("card", "canary") on unrelated
ground. One adjacent artefact does exist — kagi's `corpus/sources-census.sh` quote arm — and it is
*not* contested, but it names a value C3 should adopt rather than invent (§Proposal).

## Sibling rows read (each with the check actually run)

| Lane | Row read | Bytes that decide the boundary |
|---|---|---|
| chousa | `chousa-shokunin/PROVINCE.md:6` | "unsourced); citation chaining and hop resolution; claim-vs-source verification;" — chousa owns the **method**. |
| chousa | `chousa-shokunin/PROVINCE.md:10-11` | "**Refuses:** bounty-program scope and claim packages (→ kasegi); model-quality / or evaluation claims (→ kengaku);" — chousa's own text routes the **claim** to kengaku. |
| chousa | `chousa-shokunin/SKILL.md:58` | "- **Refuses model-quality claims** — that is kengaku." |
| chousa | `chousa-shokunin/corpus/knowledge/engine-swap-canary-r36.md:1-5` | "The engine-swap canary — fourteen pin/contract scenarios" over "`tools/research-gate.sh` and `corpus/evidence/round36/c1-count.py`" — a **tool-integrity tripwire**, not a benchmark canary. |
| kotoba | `kotoba-shokunin/PROVINCE.md:57` | "| kengaku | adjacent | 1f3b0f1e… | LLM and model research and evaluation …; kengaku keeps measured capability effects of prompt format, kotoba owns the craft rules … | basis both |" |
| kotoba | `kotoba-shokunin/PROVINCE.md` § Core | kotoba's Core is SKILL.md/AGENTS.md/dispatch craft and "four fidelity checklists" over those surfaces — no benchmark row anywhere in the file. |
| kasegi | `kasegi-shokunin/PROVINCE.md:48` | "- kengaku — LLM evaluation and benchmarks" (kasegi's own adjacency row, naming this lane as the owner). |
| kasegi | `kasegi-shokunin/PROVINCE.md:3` | "**Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages" — "claim package" is a bounty artefact, not a benchmark disclosure form. |
| kagi | `kagi-shokunin/PROVINCE.md:55` | "- `corpus/sources-census.sh` — source-registry gate (round 21): the SOURCES-CONTRACT-v1 census over `corpus/SOURCES.md` … Checks the citation chain and declared capture/classification records, never page content". |
| kagi | `kagi-shokunin/PROVINCE.md:56` | "- Helpers, not gates: `corpus/rendered-text-v1.py` — the one quote/page normalizer declaration (`digest`, `locate`, …)". |
| kagi | `kagi-shokunin/corpus/sources-census.sh:277-278` | `words=$(printf '%s' "$fquote" \| wc -w); words=${words//[[:space:]]/}` then `[[ -n $fquote && $words -le 25 ]] \|\| finding SC_FETCH "id=$fid quote"` — the only sibling **quote** rule. |
| tameshi | `tameshi-shokunin/PROVINCE.md:14` | "**Refuses:** product domains — every lane's gate remains its own; tameshi owns only the reusable craft…" — the Q1–Q8 gate, being this lane's gate, is not tameshi's. |
| kake | `kake-shokunin/PROVINCE.md:160` | "Link-preview metadata — the Open Graph properties a platform reads to build a card for a shared URL" — kake's "card" is a PreviewCard/OG card. |
| kengaku | `kengaku-shokunin/PROVINCE.md:125` | "…unopened leads), contamination transparency cards, judge calibration applied" — the bullet C1 moves. |
| kengaku | `kengaku-shokunin/corpus/README.md:272` | "**Contamination transparency cards**: why — `knowledge/contamination-detection-and-transparency.md` establishes the tier/access vocabulary but the lane has no standard card format … draft a card template and gate a knowledge entry on Q1–Q8." — the Q1–Q8 requirement is **this lane's own** frontier text. |

Scans run (whole-fleet, read-only):
- `grep -l -i "contamination" */PROVINCE.md */SKILL.md` → **only** `kengaku-shokunin/{PROVINCE.md,SKILL.md}`.
- per-`PROVINCE.md` count of "benchmark" → kengaku 12, kasegi 1 (its row routing to kengaku), all others 0.
- `grep -qi "transparency card|disclosure card|per-benchmark card|card format" */PROVINCE.md */SKILL.md` → only `kengaku-shokunin/PROVINCE.md`.
- `grep -rl -i "contamination\|canary\|disclosure card"` over `corpus/knowledge/` of chousa/kotoba/kasegi/kagi/tameshi → chousa (engine-swap canary, above), kotoba/tameshi (the word inside fixture and harness entries), kasegi 0, kagi 0.
- `kengaku-shokunin/corpus/SOURCES.md`: no S081–S086 rows yet (`grep -nE '^\|[[:space:]]*S08[1-6][[:space:]]*\|'` → 0 hits), and S122–S124 (the three tabulated card designs) are **not** in the lane registry either (`grep -cE '^\|[[:space:]]*S12[234][[:space:]]*\|'` → 0). The staged round-6 entry `benchmark-card-field-schema-2026-10-23.md` is **ABSENT** from `corpus/knowledge/` (staged only, `~/Projects/shokuknow/merge/kengaku/`).

## The contested surface, named precisely

**C1 — card + Q1–Q8 gate: no sibling row is contested.** The precise surface is the frontier row at
`corpus/README.md:272` (kengaku) and no other lane's file mentions a card at all. Three near-misses,
each refused on fetched bytes:

1. **chousa's "canary"** is `tools/research-gate.sh`'s engine-swap tripwire (`engine-swap-canary-r36.md:3`);
   S077's canary — "Prevents training data contamination by ensuring a unique canary string is present in
   task files." (`SOURCES.md:100`) — is a *task-file* string a benchmark maintainer plants. Same word,
   disjoint referents. More importantly chousa's own refusal (`PROVINCE.md:10-11`) hands evaluation
   claims to this lane.
2. **kake's "card"** is the Open Graph/PreviewCard of a shared URL (`PROVINCE.md:160`); publishing a
   benchmark card is a domain document, not a web property.
3. **kagi's "detector access" vocabulary collision.** The card's Q2 asks "model parameters only, the
   training corpus, a public web index, or a canary" — access *tiers* of a detector, which is the
   registry `tier` cell's job in every lane, not credential custody. kagi's province is
   "secrets & vault ops — the-janitor flows, credential hygiene evidence" (`PROVINCE.md:3`); nothing in it
   reads a benchmark's disclosure.

**C3 — quote validation: adjacent artefact, still not contested, with one naming obligation.**
Two facts decide it:
- The fleet contract's quote rule is `≤25 words` plus location (`SOURCES-CONTRACT-v1.md:47`), and the
  **fleet** census at `scripts/sources-census.sh` has no quote check at all (its declared finding set is
  E01–E12: malformed row, id, duplicate, dup URL+scope, kind, tier, status, opened, recheck, community-A,
  used-by path, row-outside-registry — no quote or word arm). So quote validation is unclaimed fleet ground.
- The only *sibling* implementation is kagi's lane-local SC_FETCH, which (a) enforces the same `≤25`
  cap on a **declared** `source-fetches.tsv` field, (b) requires the normalizer name to be one of
  `rendered-text-v1` / `raw-literal-v1` (`sources-census.sh:279`), (c) requires a normalized digest
  only for `rendered-text-v1`, and (d) **never checks containment** of the quote in the artifact.

So C3's containment arm is new ground and kagi's gate is not reached — kengaku has no
`corpus/source-fetches.tsv` and no `corpus/inrow-pins.tsv` (both `test -e` → ABSENT), so SC_FETCH does not
run against this lane at all today.

**Where a contest would appear if the framing drifts** (state it now, not after the fact):
- If the round describes the new arm as *claim-vs-source verification*, it restates chousa's Owns line
  (`PROVINCE.md:6`) and trips contract rule 3 — "**No second method.** Claim admission stays in
  `corpus/QUALITY.md`; the research method stays chousa's" (`SOURCES-CONTRACT-v1.md:52`). Correct framing:
  enforcement of contract rule 1 (`SOURCES-CONTRACT-v1.md:47`), inside the lane's own admission gate.
- If the round describes byte-substring as quote *location* truth, it becomes a second normalizer beside
  `kagi-shokunin/corpus/rendered-text-v1.py` — a row kagi's province declares as "the one quote/page
  normalizer declaration". kengaku's PROVINCE already promises the opposite posture for the census
  ("compose with the fleet census, which remains the registry's authority; neither replaces it",
  §Round29 attempt-2).

## Report-out line (for the owning lane, if the drift above is not avoided)

Adjacent, not contested — file only if the framing text ships unchanged:

```
kagi | round-30 | kengaku C3's quote arm is raw-byte containment over a supplied artifact and claims no
normalizer; it declares the fleet handshake's existing `raw-literal-v1` value, not a new one. No change
requested to `kagi-shokunin/corpus/sources-census.sh` or `corpus/rendered-text-v1.py`; the fleet census
stays authority and a kengaku refusal is lane-local and may only be stricter.
```

No report-out is owed to chousa, kotoba, kasegi, tameshi or kake for C1: each boundary is already stated
in the sibling's own text, in kengaku's favour.

## Proposal (one bounded move)

**Declare C3's `--artifact` arm as normalization `raw-literal-v1`, and write the bound into the gate's
docstring instead of discovering it in a later round.** `raw-literal-v1` is a value the fleet handshake
already accepts (`kagi-shokunin/corpus/sources-census.sh:279`, with `normalized-digest = -` at
`:280-283`), so kengaku reuses the fleet's existing name for "the quote must appear in these bytes
verbatim" instead of minting a third semantics.

Evidence and trace:
- The card's own Q-cells and the round's six cited rows are ASCII-bearing public documents, so a
  raw-literal arm does not silently refuse a quote the rendered arm would accept *for this round's
  population* — but it will, for any artifact whose bytes carry markup or a line break inside the quote
  (kagi's `rendered-text-v1` collapses whitespace and strips markup; `rendered-text-v1.py:70-84`).
  The docstring must say: *raw-literal containment; a quote spanning a source line break is refused by
  design, re-quote or use the rendered form, which this gate does not implement.*
- Second-order: with the name declared, a later round that publishes `corpus/source-fetches.tsv` can
  carry `raw-literal-v1` + `-` and pass both gates without kagi's enum changing — and without kengaku
  editing a sibling's gate (tameshi `PROVINCE.md:14`: gates are their own lane's).
- Exit-code constraint on the same edit: the new failure cases must use codes disjoint from
  `EXIT_COLLISION=3`, `EXIT_MALFORMED=4`, `EXIT_REQUEST=5` (`plans/sources_adopt.py:40-43`) **and from
  argparse's 2**, because C3's frozen control is "the pre-change bytes … reject the same invocation with
  argparse exit 2" (`plans/round-30-claims.md` §C3). A quote refusal coded 2 would make the control and
  the target indistinguishable. A natural pair: 6 = quote-too-long, 7 = quote-not-in-artifact.

Affected axes: **operability** (C3's gate gains the rule the contract already states, under the fleet's
own value name) and **calibration** (C3/quality: the arm can fail for the right reason); **coverage**
(C1) is untouched — no row, no entry byte, no predicate changes.

Risks (named, not smoothed):
- `raw-literal-v1` is *declared* by kagi's gate but kengaku has no `source-fetches.tsv`, so on the day
  the name is used it is consistent-but-unexercised by the fleet handshake — a naming claim, not a run.
  Say so in the gate docstring; do not report it as census parity.
- A raw-literal arm can refuse a legitimately normalized quote. That is a *bounded refusal* the lane can
  see and re-quote; the failure mode it must never have is silently accepting a normalized-only match
  under the name `rendered-text-v1`, which this proposal forbids.

## Verification

Executed this seat (read-only; no writes outside this report):
- `python3 plans/sources_adopt.py --selftest` → `SELFTEST cases=10 failed=0` (matches C3's control figure).
- `test -e corpus/source-fetches.tsv` / `corpus/inrow-pins.tsv` → both ABSENT.
- `grep -cE '^\|[[:space:]]*S12[234][[:space:]]*\|' corpus/SOURCES.md` → 0; S081–S086 → 0 rows.
- `test -e corpus/knowledge/{contamination-transparency-card,benchmark-card-field-schema-2026-10-23,contamination-mitigation-comparative-evidence-2026-10-23,per-benchmark-contamination-verdicts-2026-10-23}.md` → all ABSENT (staged only).
- `grep -l -i contamination */PROVINCE.md */SKILL.md` → kengaku only; per-lane "benchmark" counts as in §rows read.

Not run, and not claimed: no network fetch (the six S081–S086 URLs were not opened by this seat), no
counter beyond the selftest, no `git` command.

Tool installs/upgrades: **none**.

## Corollary for the amendment's referent (one line, in-lane)

C1 says the admitted entry "names the lane entry it extends". The three-designs tabulation is staged
only, so the only in-lane referent that exists is
`corpus/knowledge/contamination-detection-and-transparency.md` (present). Naming a staged-only path
would reproduce D1's exact defect class (a citation to a path absent from the tree). Naming
`benchmark-card-field-schema-2026-10-23.md` also risks D5's asymmetry: it would be a prose reference to
a study whose rows S122–S124 are not in this lane's registry.
