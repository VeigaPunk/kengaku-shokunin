# R31DefR7 — routed defect R7, entry delta sentence vs its own R3 row

Seat: reviewer (leaf), round 31 / hyaku run 6, 2026-10-25. Lane: `kengaku-shokunin` at tip `0883e72`.
Access date for every source opened here: **2026-10-25**.

Target: `.ufo/waves/round-31/build/R31DefR7.md` scope — the entry sentence that claimed *"S2's tri-state
integrity flag is the only new field"* against its own R3 mapping row, which records `unknown` /
`not_controlled` as valid values in a published form.

## 0. State of the bytes reviewed (read this before the quotes)

The worktree is **modified against HEAD** (`git status --porcelain` → ` M corpus/knowledge/contamination-transparency-card.md`,
plus `M plans/sources_adopt.py` and five round-30 seat reports). The routed sentence no longer exists in the
live file: an in-flight repair landed it between my first read and my second. Both states are quoted below,
because the routed line numbers (`:68`/`:71` in `corpus/lessons/round-30-verifier-spotcheck.md:177`) have
**drifted +1** — the R6 repair added one line at `:41-43`, so the delta paragraph is now `:72-83`.

- Pre-repair (HEAD, `476d2dc` blob), `corpus/knowledge/contamination-transparency-card.md:71-72`:
  > `So the delta is one field, and the rest is not a delta at all. **S2's tri-state integrity flag is the`
  > `only new field.** S1 is not a new field: the CTC v1.1 column beside it reads `type 5 recorded per run`,`
- Live worktree now, `:72-75`:
  > `So the delta is one field, and the rest is not a delta at all. **The card-level integrity field is the`
  > `only new one; its tri-state vocabulary is not** — the form's per-type column beside it already reads`
  > `` `unknown` / `not_controlled`, so what the card adds is a state recorded *for the card itself* rather ``
  > `than for a contamination type. S1 is not a new field: the CTC v1.1 column beside it reads ...`

Counter state at review time (read-only run, `python3 plans/round31_defects.py --lane .`):
`checks=10 defects=6` exit 1 — open: R1, R2, R3, R6, R9, R10; R7 prints no defect (see F5).

## (a) Does the R3 row carry the tri-state vocabulary? Yes — and it is a *four*-value set, not three

`corpus/knowledge/contamination-transparency-card.md:63` (the R3 row; `:61` in the pre-repair file):

> `| R3 contamination type tested | "Contamination controls" | per-type `controlled` / `not_controlled` / `unknown` / `n/a` | Decontamination | **already a column**; S081's five types give it values |`

The `unknown` / `not_controlled` phrasing the routed item names is carried in two further cells of the same
table, not in R3's cell:

- `:64` — `| "what a negative cannot rule out" | "their coverage, and known gaps" | `unknown` and `not_controlled` are valid entries | Evidence Provided | **already a column** |`
- `:69` — `| S2 card integrity flag | (absent) | `unknown` / `not_controlled` are valid values | (absent) | **delta in field** — a state for the card itself |`

So the routed framing is right in substance and slightly off in attribution: R3's row carries the
four-value per-type set; the two-value "valid values / valid entries" wording sits in the negative row
and in S2's own row.

Verified against the cited document, not just against the entry's reading of it. Fetched one file
(`curl`, `raw.githubusercontent.com`, 200, 2181 bytes → `/tmp/r31-R31DefR7/disclosure.yaml`), pinned
commit `4dba1ed9b2ace8b71a2edcd5fa6ce0337cf08ba6`, `templates/disclosure.yaml` — the S123 locator in the
staged file `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md:3`:

- `disclosure.yaml:5` — `# "unknown" is a valid entry. So is "not_controlled". Declare what you don't know.`
- `disclosure.yaml:36` — `  direct: "unknown"           # controlled | not_controlled | unknown | n/a`
- `disclosure.yaml:46` — `  boundary_integrity_monitored: ""` (inside the `contamination_controls:` block opened at `:34`, under the `# Type 5 is evaluation-time` comment at `:40-41`)

The staged tabulation records the same two facts at `benchmark-card-field-schema-2026-10-23.md:48` and `:73`.
**The vocabulary is published in the form's own bytes, twice: as a header rule (`:5`) and as an enumerated
per-type comment (`:36`). It is not new, and it is not a tri-state — `n/a` is the fourth member.**

## (b) What is genuinely new

**The card-level field — the *subject* of the state — and nothing else.** Not the vocabulary, and not
"neither":

- Vocabulary: published, `disclosure.yaml:5` and `:36`; already recorded in the entry at `:63`, `:64`, `:69`. Not new.
- Field: `:69`'s status cell `**delta in field** — a state for the card itself`, and it is the table's only
  delta-status row (every other row reads *already a column*, *already a column in one of three*, or
  *not a delta* at `:62-70`). New **relative to the union table** — the three tabulated designs have no column
  whose subject is the card's own state.

Two qualifications a precise sentence must carry, both grounded:

1. **The form has an adjacent key.** `disclosure.yaml:46` is `boundary_integrity_monitored: ""` — a run-side
   record of boundary monitoring, with no declared value vocabulary. An unqualified "new field" invites the
   same rebuttal that killed S1's "new field" claim at `:68` ("it is a rename, not a relocation"). The field is
   new *as a card-level subject in the union table*, not as "the form records nothing of the kind".
2. **The entry cannot cite the form's keys.** The entry states at `:76-77` that it "cannot settle it without
   reading that form, which it has not admitted". So the novelty must be scoped to the union table (which the
   entry sees through the staged tabulation), never asserted as an absence in the form's schema.

"Tri-state" is wrong on both counts: the vocabulary is not new (defect as routed), and the set it labels has
four members, not three (`:63`; `disclosure.yaml:36`). The word is defensible only as the lane's own
convention — `corpus/knowledge/local-model-index.md:28`: "Tri-state: missing = unknown, `null` = not applicable
(tier/comparison only), populated = known" — which is the lane's index convention, not the CTC form's
vocabulary, and the sentence at `:72-73` attaches it to the form ("the form's per-type column ... its tri-state
vocabulary").

## (c) The narrowest true sentence that keeps the delta claim

Drop-in replacement for live `:72-75`, same paragraph, same claim strength (one delta row), no vocabulary novelty:

> So the delta is one field, and the rest is not a delta at all. **The only field this entry adds to the
> union table is S2, and what it adds is the field — a state recorded for the card itself rather than for a
> contamination type. Its values are not new: the CTC v1.1 form already publishes `controlled` /
> `not_controlled` / `unknown` / `n/a` per type, and `unknown` / `not_controlled` as valid entries.**

What it keeps: "one field, and the rest is not a delta at all"; S2 as the single delta; the card-level subject
(`:69`). What it drops: the word "tri-state"; the unscoped "only new one"; the two-value citation that made the
set look three-valued. What it fixes: the evidence is pointed at the rows that actually carry it (`:63`, `:64`)
instead of at "the form's per-type column beside it", which is not per-type beside S2 (`:69`).

If the lane wants to keep the word, the only true form is to label it as the lane's convention and to give the
published set in full, e.g. "the lane's tri-state reading of the form's four-value set (`controlled` /
`not_controlled` / `unknown` / `n/a`)". That is longer and buys nothing; dropping the adjective is narrower.

## (d) Sweep — every sentence that could depend on the retracted reading

`grep -rn "tri-state\|only new field\|one genuinely new field\|one new value set\|new value set"` over
`corpus/`, `plans/`, `LOG.md`, `SCORECARD.md`, `.ufo/waves/round-30/`:

| Location | Text | Depends on the retracted reading? |
|---|---|---|
| `corpus/knowledge/contamination-transparency-card.md:72-73` (live) | "**The card-level integrity field is the only new one; its tri-state vocabulary is not**" | **Yes, partially** — retracts the vocabulary claim but keeps the mis-description "tri-state" and cites 2 of 4 values. Finding F1. |
| `corpus/knowledge/contamination-transparency-card.md:81-82` | "Two earlier readings of this paragraph ("two new fields", then "one field, one placement, one value set") overclaimed; this is the corrected one" | No — it is the correction ledger and stays true under (c). |
| `corpus/knowledge/contamination-transparency-card.md:120-121` | "So the entry's one genuinely new field (S2) is *not* one its source validated" | No — field-level claim, which survives; consistent with (c), no edit needed. |
| `corpus/knowledge/contamination-transparency-card.md:172` | "leave `unknown` where unknown" | No — uses the vocabulary as a published valid value; supports the corrected reading. |
| `corpus/knowledge/contamination-transparency-card.md:139` | falsifier: `*populated* (not "unknown")` | No — same published vocabulary. |
| `corpus/README.md:65`, `:242` | index row and coverage row ("maps the release-side R1–R5 and score-side S1–S2 fields into the union table's columns") | No — no vocabulary or "only new field" claim. |
| `SCORECARD.md:1022` | "S2's tri-state flag is the only surviving field delta. Not core, not real expansion." | **Yes** — carries "tri-state" in a live ledger row. Outside `check_r7`, which reads the entry only. Finding F6. |
| `LOG.md:792-793` | "declared the delta (two new fields, one new value set)" | No for R7 — that is R1's superseded arithmetic, not the vocabulary claim; R1 owns it. |
| `corpus/lessons/round-30.md:66-67` | "the delta is stated as one field, one placement, one value set" | No for R7 — the arithmetic reading; R2 owns it. |
| `corpus/lessons/round-30-verifier-spotcheck.md:177-180` | quotes the retracted sentence as the routed defect | No — historical quotation; **must stay** (it is the defect record). |
| `.ufo/waves/round-30/{build/R30ConnCorpus.md:96,186; falsify/R30FxEntryQ4Q6.md:319,408; R30FxCoverageAxis.md:102,243; R30FxStagedContrast.md:123}` | describe the S2 claim and its failure at the time | No — historical wave artifacts; **must not be rewritten**. |
| `plans/round31_defects.py:25`, `:189` | docstring + predicate quote the retracted sentence | No — the counter's own defect record; correct to keep. |

Only two live sites depend on the retracted reading: the entry's repaired sentence (F1) and
`SCORECARD.md:1022` (F6).

## Findings by severity

**F1 — medium — the retraction still uses the retracted description.** Live `:72-73` retracts "the vocabulary
is new" while calling that vocabulary "tri-state", and the only values it cites are `unknown` /
`not_controlled` (`:73-74`), which is exactly what makes a four-value set look three-valued. Against `:63`
(`controlled` / `not_controlled` / `unknown` / `n/a`) and `disclosure.yaml:36`, the adjective is false in the
one sentence whose job is to stop asserting it. Repair: (c).

**F2 — medium — "The card-level integrity field is the only new one" is unscoped.** True of the union table
(`:62-70`, S2 the only delta row); not true as an absence claim about the form, which carries
`boundary_integrity_monitored: ""` at `disclosure.yaml:46`. Scope it ("the only field this entry adds to the
union table") — which also keeps it consistent with `:76-77`'s admission that the form has not been read.

**F3 — medium — evidence mis-located.** "the form's per-type column beside it already reads `unknown` /
`not_controlled`" (`:73-74`): beside S2's row the CTC cell (`:69`) is the two-value "valid values" cell, not a
per-type column. The per-type enumeration is R3's row (`:63`). A reviewer checking the cited row finds the
evidence one row away and only two of four values.

**F4 — high, cross-item, blocks C2 — `check_r6` is satisfied by its own repair's wording.** Not R7's text, but
the same counter and the same paragraph family; it makes `defects=0` unreachable:

```
$ python3 -c '...flat(entry)...'
R6 old-phrase present: True
R6 context: lane's `corpus/knowledge/`, and two of its three source rows are not in this lane's registry (the GEM
```
`plans/round31_defects.py:168` tests `"its three source rows are not in this lane's registry"`, and the repaired
sentence `"two of |its three source rows are not in this lane's registry|"` contains it. The comment at `:165-167`
asserts the opposite property ("The exact superseded phrase, not ... as a substring ... so the first version of
this check greened its own repair") — the tightening stopped one token short. Either the entry's wording must
avoid the phrase (`"two of its three source rows are unregistered here"`) or the check needs a boundary
(`" three source rows"` preceded by neither `of ` nor a digit, or a regex `(?<!of )three source rows`). This is
R6's repair to make; reported here because it gates the claim, not because R7 owns it.

**F5 — medium — `check_r7` cannot see the defect it closes.** `plans/round31_defects.py:187-192` is a two-string
guard: absence of the literal `"S2's tri-state integrity flag is the only new field"`, presence of `"card-level"`
anywhere in the entry. Live text has `tri-state` ×1 and `card-level` ×1 → green. The same check would also green
"the card-level field is new and its tri-state vocabulary is new too". `defects=0` therefore does not prove R7
closed; the claim's predicate (C2: "R7 entry S2 'only new field' narrowed to the card-level field") is met
literally, but the calibration item is met only if (c) lands.

**F6 — low — residual in a live ledger row.** `SCORECARD.md:1022` ends "S2's tri-state flag is the only surviving
field delta. Not core, not real expansion." The field-delta half is true; "tri-state" repeats F1's
mis-description in a file `check_r7` does not read. If SCORECARD rows are treated as append-only, the correction
is a named appended line, not a rewrite.

## Residual risk and verification gaps

- The union table's CTC column is the entry's reading of a **staged** document; I verified it against the pinned
  form itself (`disclosure.yaml:5,36,46`) and it holds. The entry's own disclosure that the mapping is not
  lane-sourced (`:41-44`, `:131-133`) remains accurate.
- `disclosure.yaml:46` (`boundary_integrity_monitored`) is the strongest available counter to any unqualified
  "new field" wording. I did not fetch `templates/disclosure.schema.json`, so I cannot say whether that key is
  required or has an enum; the `yaml` value is an empty string with no comment, which is enough to say the key
  exists and its vocabulary is undeclared.
- Line numbers in the routed item (`:68`/`:71`) no longer resolve; the content predicates survive the shift,
  human citations do not. Anyone re-checking R7 by line number will read the wrong rows.
- I ran no build, no census and no adoption check — out of this seat's scope. The one counter run above is the
  claim's own counting command, read-only (`check_*` read; `tempfile` only under `--selftest`).
- No tool was installed or upgraded (host pacman is paused); the only network use was one 2.2 KB `curl` into
  `/tmp/r31-R31DefR7/`, total scratch well under 60 MB.

VERDICT: R7 IS NOT CLOSED — the live sentence at `contamination-transparency-card.md:72-74` retracts "only new field" but keeps the false "tri-state" label and cites two of the form's four published values (`:63`; `disclosure.yaml:36`), and its "only new one" is unscoped against `boundary_integrity_monitored` (`disclosure.yaml:46`); land (c), rescope the novelty to the union table, and note that `check_r7` (`plans/round31_defects.py:187-192`) and `check_r6` (`:168`) cannot by themselves prove R7/R6 closed.
