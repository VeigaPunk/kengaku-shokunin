# R30FxSibling — does the round's *final* wording claim a sibling surface?

Seat: falsify (leaf), round 30, kengaku. Access date 2026-10-25. Lane tip read: `363a4eb`
(round-30 bytes are uncommitted working-tree bytes — `git status --porcelain` lists
`corpus/knowledge/contamination-transparency-card.md`, `corpus/lessons/round-30.md`,
`corpus/SOURCES.md`, `corpus/README.md`, `corpus/QUALITY.md`, `SCORECARD.md`, `plans/sources_adopt.py`,
`plans/round30_defects.py`, `plans/round-30-claims.md`, `corpus/evidence/round30/`; read as landed
bytes, not as a commit).

## Verdict

**None owed.** No phrase the round ships claims chousa's research-method verification, kagi's
secrets custody, kotoba's prompt craft, kasegi's bounty/security ground, or the fleet census's
quote arm. One residual (§Residual) is a *latent naming gap*, not a claim, and the one-line
report-out to kagi is drafted below and **not filed**.

This verdict is re-derived on the **final** wording, not inherited from the build-time scan: the
build seat `R30ConnSibling` made its finding conditional ("file only if the framing text ships
unchanged") against a gate that did not yet exist in its final form, and the gate landed with a
different framing than that seat proposed.

Not a source re-read and not the `FxEntryCompleteSet` complete-set review, so this report carries no
`VERDICT:` line on purpose: `plans/gate_timing_check.py` requires an anchored verdict only inside
`audit_admission` for the report paths it extracts from the Gate cell's reason (`:356-362` over
`report_paths`); an uncited falsify report is out of that check's inventory.

## Shipped bytes examined (final wording)

`corpus/knowledge/contamination-transparency-card.md` (all 8 sections + frontmatter triad),
`corpus/lessons/round-30.md` (Gate, Round 30 admission, Sources opened, Mistakes, Measured),
`corpus/SOURCES.md` S081–S086 cells, `corpus/README.md` index + coverage + frontier rows,
`corpus/QUALITY.md` Q20, `SCORECARD.md` round-30 block, `plans/round-30-claims.md`,
`plans/sources_adopt.py` (docstring + quote mode 254-424), `plans/adoption_check.py:96-116`.

## The sibling rows, quoted

| Lane | Row | Bytes that decide the boundary |
|---|---|---|
| chousa | `chousa-shokunin/PROVINCE.md:6` | "unsourced); citation chaining and hop resolution; claim-vs-source verification;" |
| chousa | `chousa-shokunin/PROVINCE.md:10-11` | "**Refuses:** bounty-program scope and claim packages (→ kasegi); model-quality / or evaluation claims (→ kengaku)" |
| kotoba | `kotoba-shokunin/PROVINCE.md:57` | "kengaku keeps measured capability effects of prompt format, kotoba owns the craft rules … basis both" |
| kagi | `kagi-shokunin/PROVINCE.md:3` | "**Domain:** secrets & vault ops — the-janitor flows, credential hygiene evidence" |
| kagi | `kagi-shokunin/PROVINCE.md:56` | "`corpus/rendered-text-v1.py` — the one quote/page normalizer declaration" |
| kasegi | `kasegi-shokunin/PROVINCE.md:3,48` | "bounty & security research — scopes ~/Projects/bounties, program rules, claim packages" · "- kengaku — LLM evaluation and benchmarks" |
| fleet | `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` rule 3 (carried in fleet `CORPUS.md:66-67`) | "**No second method.** Claim admission stays in `corpus/QUALITY.md`; the research method stays chousa's" |

## Checks executed (with output)

1. **Sibling-surface vocabulary is absent from both prose surfaces.**
   `grep -noiE 'prompt|secret|vault|custody|security|bounty'` over the entry and
   `corpus/lessons/round-30.md` → **no hits** in either file.
2. **The drift the build seat named did not ship.** `grep -nE 'claim-vs-source|research method|normalizer|raw-literal|rendered-text|source hierarchy|citation chain'`
   over entry + lesson + `plans/round-30-claims.md` + `plans/sources_adopt.py` → **no hits**.
3. **The only "credential" token is quoted, twice, never glossed.** `grep -n credential` → entry `:2`
   (S082's anchor cell) and entry `:24`; `:24` sits inside the double-quoted span
   "transparency should attach primarily to procedures, governance, credentials, and validity
   testing, not necessarily to live item pools". No CG question asks for credential material; the
   card's access question is CG2 ("parameters only, the training corpus, a public index, a canary").
4. **The fleet census has no quote arm to claim.** `grep -ciE 'quote|word' shokunin/scripts/sources-census.sh`
   → `0`. The only quote arm in the fleet is kagi's lane-local SC_FETCH
   (`kagi-shokunin/corpus/sources-census.sh:277-283`: `words … -le 25`, `normalization` ∈
   `rendered-text-v1|raw-literal-v1`, location ≥8 chars), over a 16-column `source-fetches.tsv`.
   `test -e corpus/source-fetches.tsv` → **ABSENT**; `corpus/inrow-pins.tsv` → **ABSENT**, so SC_FETCH
   does not run against this lane at all.
5. **`census=ok` is the fleet census's own exit code, lane-scoped.** `plans/adoption_check.py:104-108`
   runs `sources-census.sh validate --root <lane.parent> <lane_name>`; kengaku ships no second census.
6. **Gate selftest re-run (not accepted from a report).** `python3 plans/sources_adopt.py --selftest`
   → `SELFTEST cases=14 failed=0`, exit 0.
7. **Fleet scans re-run.** `grep -l -i contamination */PROVINCE.md */SKILL.md` → kengaku only;
   `grep -li 'transparency card|disclosure card|card format'` → kengaku only; `benchmark` counts →
   chousa 0, kagi 0, kotoba 0, kasegi 1 (its routing row to kengaku).

## Why each sibling is clear, with the nearest shipped phrase

- **chousa — research-method verification.** Nearest shipped phrase: the gate's capability 5
  ("every quoted span in a supplied row's anchor cell is measured against the contract's <=25-word
  cap and located as a byte substring of the named artifact") plus its scope sentence ("Scope:
  registry row mechanics and quote presence only. Source truth, tier judgement and the census itself
  stay where they are (CORPUS.md contract v1; census is fleet-owned)"). Both name **presence and
  cap**, never *support*: the arm cannot tell whether a located quote grounds `teaches`. The round
  files the work as enforcement of the fleet contract's rule 1 (`CORPUS.md:114`: "a ≤25-word quote
  with its location grounding `teaches`. Non-author verification re-opens a sample"), which is why
  the lesson can say "a `reviewer` seat … re-opened all six sources" without asserting a method of
  its own. `CORPUS.md:66-67` carries contract v1 in full from the kaika file, so the docstring's
  pointer is a live target, not a dangling reference — I checked it because a broken deference
  pointer would have weakened the non-claim.
- **kotoba — prompt craft.** Nearest shipped phrase: the union table's `elicitation_budget` column
  and CG6 ("Was the elicitation budget stated?"). The entry **names** the column and never defines
  an elicitation — no example count, no wording, no format. `prompt` occurs zero times in either
  prose surface. Nothing in the round touches SKILL.md/AGENTS.md/dispatch surfaces that kotoba's
  Core governs, and kotoba's row already records kengaku's own split in kengaku's favour.
- **kagi — secrets custody.** Two adjacencies, both refused: (a) the quoted "credentials" (check 3);
  (b) the quote arm itself. The arm's docstring will not take a normalizer name — it says byte
  substring **of the normalised text** and adds "never a fuzzy or whitespace-insensitive match", and
  the only normalization is `\r\n|\r → \n` (`normalize_text`). So it neither declares
  `rendered-text-v1` (which collapses whitespace and strips markup) nor `raw-literal-v1`; kagi's
  "one normalizer declaration" row is not contested by a claim. Contract rule 6 ("No credential
  material … ever") is not engaged: the round adds no fetch table, no session URL, no `op://` token.
- **kasegi — bounty/security.** Nearest shipped phrases: the prose word "disclosure" (`:25`, `:111`,
  `:141`) and "practical threat model" (`CG7`, inside S083's quoted cell). kasegi's Core is program
  rules, claim packages and *bounty* submission/disclosure packaging; a benchmark's own disclosure
  design is evaluation governance, and kasegi's own adjacency row (`:48`) names kengaku owner of LLM
  evaluation and benchmarks. "threat model" appears only as a quoted span of S083.
- **fleet-census quote arm.** Not claimed, and not duplicated: the fleet census has no quote check
  (check 4), the lane's `census=ok` is that census's exit code (check 5), and `PROVINCE.md`
  §Round29 attempt-2's bound ("compose with the fleet census, which remains the registry's
  authority; neither replaces it") already covers `sources_adopt.py`, which is one of the two tools
  it names — the new arm lands inside a bound that was written before it existed.

## Residual (named, not smoothed) — the arm's normalization is a third semantic

The newline normalization means the arm is *narrower* than `rendered-text-v1` and *wider* than
`raw-literal-v1`. Today that costs nothing (no `source-fetches.tsv` exists, and the gate names no
value). It becomes a real adjacency on the day kengaku publishes a 16-column fetch table: kagi's
SC_FETCH would accept the row only under one of its two names, and neither name describes a
CRLF-normalising containment — `raw-literal-v1` would understate the arm, `rendered-text-v1` would
overstate it (no markup strip, no whitespace collapse). **Flip condition for this verdict:** any
shipped text that (a) calls the arm quote *location* truth, (b) declares a normalizer value, or
(c) publishes `corpus/source-fetches.tsv` — then a kagi report-out is owed, in this shape.

Report-out line — **NOT FILED** (no claim exists to report against):

```
kagi | round-30 | kengaku's new quote arm is lane-local newline-normalised containment over a supplied
artifact and declares no normalizer value; it claims neither `rendered-text-v1` nor `raw-literal-v1`
and no `source-fetches.tsv` exists in that lane. No change requested to `corpus/sources-census.sh` or
`corpus/rendered-text-v1.py`; filed only so the third semantic is known before any fetch table lands.
```

## Contradiction found on the way (verification surface; not a sibling claim, routed to this wave)

The entry's recheck action — "re-fetch S081–S086 at their pinned locators, re-locate each quoted span
in fresh captures and re-run `python3 plans/sources_adopt.py --quote-file <admission rows>
--artifact <capture>`" — is unsatisfiable for half its population as written. Three of the six
sources are PDFs (S083 2697379 B, S085 1949572 B, S086 371155 B, sizes from the lesson's fetch-identity
column), and the arm refuses a PDF artifact. Executed on a scratch copy of one real PDF
(`/usr/share/doc/speexdsp/manual.pdf`) with an S081-shaped row carrying a text-layer string:

- `--artifact <manual.pdf>` → **exit 2**, `QUOTE cap=25 problem=--artifact holds no UTF-8 text (unreadable: manual.pdf)`
- `--artifact <pdftotext of page 1>` → **exit 0**, `rows=1 spans=3 located=3 found=3 overlong=0 absent=0`

So the prescription needs an unstated text-extraction step before the gate can see a PDF source's
quotes — the same class the round records as its own mistake ("a repair that prints green while
making the check unsatisfiable"), here in a *prescription* rather than a counter. Related and also
unclaimed rather than smoothed: no committed receipt shows the quote mode run over the six real
captures (`corpus/evidence/round30/` holds `adoption-after`, `census-after`, `census-before`,
`gate-selftest-after`, `r29-counter-unchanged`, `rows-opened.tsv` — no `QUOTE …` line), so the six
quotes were located by seats, not by the shipped arm. Whether that is a defect in C1's wording or
only in the recheck sentence is not this seat's ruling.

## Lane bounds and hygiene

No subagent, no background job, no model call, no `agent://all`, no lane edit except this report;
scratch in `/tmp/r30fx-Sibling/`; no edit to `/home/vgpnk/Projects/shokuknow`, to the fleet repo, or
to `.ufo/state`, `watchdog.log`, `MANIFEST.json`, sibling lanes. Every read above is either a lane
path or a sibling `PROVINCE.md`/contract read-only. Tool installs/upgrades: **none** (no package,
`uv tool`, `npm -g` or `~/.local/bin` write occurred). Not run: no network fetch of S081–S086 (not
this seat's axis — `FxEntryCompleteSet` and the per-source re-reads own it), no commit, no
`adoption_check.py` full run.
