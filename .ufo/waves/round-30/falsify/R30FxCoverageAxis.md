# R30FxCoverageAxis — is the coverage axis move honest?

Seat: `L1Kengaku30.R30FxCoverageAxis-3` (leaf critic, falsify wave, round 30, 2026-10-25).
Scope: read C1's axis sentence, the landed round-30 SCORECARD section and the README coverage
map; attack the axis claim. No lane writes besides this report; no git mutation; no seat spawn;
no model. Scratch: `/tmp/r30fx-coverage-axis-*`.

Candidate: `corpus/knowledge/contamination-transparency-card.md`

VERDICT: FAIL — the entry's amendment arithmetic ("exactly two fields are new as *fields* (S1, S2)",
`:68-70`) is falsified by its own table (`:64-66`) and by the pinned S123 template; the C1 counting
command itself passes (re-run below). Repair is three cells plus one sentence plus the SCORECARD
wording in §"The exact SCORECARD wording". The score 7 → 7 held is honest; the *reason* printed
beside it is not yet.

## What I re-ran myself (nothing here is accepted from a build report)

| command | printed | exit |
|---|---|---|
| `python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census` | `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok` | 0 |
| `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` | `88` | 0 |
| `ls corpus/knowledge/*.md \| wc -l` / `grep -cE '^\| \`knowledge/' corpus/README.md` | `39` / `39` (parity both directions) | 0 |
| `cat .ufo/waves/round-30/claims/control-nothing.txt` | `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok` / `exit=1` | — |
| `curl -sS -L https://arxiv.org/abs/2608.29463` | 44646 bytes, sha256 `4c81bd3c180736318ed03e31968fa4d109b94025ec596203dbc4e963b396908a` — **byte-identical to the source seat's recorded `abs.html` sha** (`build/R30SrcS081.md` §2) | 0 |
| `curl -sS -L https://raw.githubusercontent.com/Jangulo7/contamination-disclosure-paper/4dba1ed9b2ace8b71a2edcd5fa6ce0337cf08ba6/templates/disclosure.yaml` | 2181 bytes, sha256 `05131be9f72b333a479046a0df4510d48fd5389192d40c595869e718b5c90d0f` (scratch copy, scratch is the only place it lives) | 0 |

The round-25 L0 coverage-cap question is still **unruled**: the fleet
`.ufo/l0-questions.md` carries the line `kengaku | round-25 | Coverage cap (re-filed …) … Until
ruled, kengaku coverage stays capped at 7.` with no operator or orchestrator answer after it.
`PROVINCE.md` has no round-30 paragraph (`grep -n 'Round30\|Round 30' PROVINCE.md` → 0 hits);
its last section is `## Round29 attempt-2 partial frontier admission`.

## Attack 1 — "real expansion on ground the lane did not hold", or a restatement?

**Claim under attack.** `SCORECARD.md:1022` verdict cell: "**7 → 7 held** — real expansion on
ground the lane did not hold (frontier bullet 2 *unopened lead* → amendment + CG1–CG8 gate), but
the canonical coverage score stays 7…". Same phrasing in `plans/round-30-claims.md:42-44` ("new
corpus bytes on ground the lane did not hold") and `:23` ("moves from *unopened lead* to *core*").

**Counterexample (internal, no network needed).** The entry's own field table contradicts the
sentence that summarises it. `corpus/knowledge/contamination-transparency-card.md:64-70`:

```
| S1 acquired contamination | (absent) | type 5 recorded per run | (absent) | **delta** — the run-side half |
| S2 card integrity flag    | (absent) | `unknown` / `not_controlled` | (absent) | **delta** — a state for the card itself |
| R1 strata                 | (absent) | (absent) | (absent) | **delta** — and see §What this does not establish |

So exactly two fields are new as *fields* (S1, S2), one is new as a *value set* (R1's strata,
which no design tabulates …
```

A row whose CTC v1.1 cell reads "type 5 recorded per run" is not a delta; S2's CTC cell
(`unknown` / `not_controlled`) repeats verbatim the cell in the row **above it** that is already
classified "already a column". Three of the eight rows therefore carry a status label that their
own cells refute, and the sentence at `:68` counts two of them as the amendment's new fields.

**Counterexample (external, one fetch).** S123 is CTC v1.1 at the commit the entry's union table
pins (`4dba1ed…`). My fetch of `templates/disclosure.yaml` carries, as tabulated fields:

- `strata_reported:` — `reported`, `strata`, `aggregate_only`, `definition`, `pre_registered`,
  `scores` → this is R1, and it is tabulated, so "no design tabulates" (`:69`) is false;
- `contamination_controls.acquired` plus `network_access_during_eval`, `environment_sanitised`,
  `transcripts_reviewed`, `boundary_integrity_monitored`, `notes` → this is S1 exactly as the
  entry defines it ("network access, environment sanitisation, transcript review or boundary
  monitoring — with the elements actually stated recorded in `notes`");
- the header rule `"unknown" is a valid entry. So is "not_controlled".` → this is S2;
- `eligibility_date`/`evaluation_date`, `elicitation_budget`, the four training-time types,
  `regeneration` → R2, R3, R4, R5.

So by the pinned bytes of one of the three designs the entry itself tabulates, **zero** of the
seven R/S fields is new; the amendment's contribution is the crosswalk into the union table's
columns, the CG1–CG8 gate, and the blind-spot sourcing. S081's own abstract (my capture, sha
matches the seat's) says the same thing from the source side: "We operationalize it as a
four-field disclosure protocol in which \"unknown\" is a valid entry, released under CC BY 4.0
with a JSON Schema, a validator, and worked examples." S081's protocol *is* the field list — and
`corpus/SOURCES.md:107` already scopes S081 that way ("the four-field contamination disclosure
protocol (strata, elicitation budget, five types, regeneration), its JSON Schema and validator").
[INFERENCE-strong: that CTC v1.1 (S123) is S081's released form — repo `contamination-disclosure-paper`,
same four blocks, same declared-negative rule. The R1/S1/S2 finding does not depend on this: R1's
all-absent cells are refuted by the S123 bytes alone.]

**What is *not* a restatement.** `corpus/knowledge/contamination-detection-and-transparency.md`
holds none of this: its `:9-14` requires "a transparency record" and never gives a field, its `:73`
prefers "suites with a documented transparency card" and never defines one, and
`grep -rn 'transparency card' corpus/*.md corpus/knowledge/*.md` returns only that preference plus
the README gap statements. On the lane-corpus denominator the entry is lane-new ground — the
overlap seat reached the same verdict (`build/R30Overlap.md` §(c)) and I agree with it. Nor is the
CG gate newly invented this round: round-29's connector catalogued "card field table + Q1–Q8
answerability gate" as a drafted candidate with line cites
(`.ufo/waves/round-29/attempt2/build/R29a2ConnCapability.md:27-33`), and the round-6 schema already
cross-tabbed the lane's fields against the three designs
(`benchmark-card-field-schema-2026-10-23.md:70-79`).

**The "core" claim has no landed referent.** Claims `:23` says frontier bullet 2 "moves from
*unopened lead* to *core*". The landed README says the opposite in three places: the coverage-map
row is "covered at source-digest depth" (`corpus/README.md:242`), the frontier note is "*Partly
discharged round 30*" and "supersedes … **for the card format only**, the `unopened lead` phrase"
with "Still frontier: benchmark-maintainer releases on hidden-test governance (no private-split or
hidden-test-governance release was opened this round)" (`:275`). No benchmark-maintainer release on
hidden-test governance was opened — S081/S082 are arXiv, S083 an EACL paper, S084 vendor docs,
S085 a sponsoring body's self-report, S086 a conference paper. The word "core" occurs in this lane
only as PROVINCE's round-section heading format (`## Round29 … Core addition:`), and no round-30
PROVINCE paragraph exists.

**Verdict: PASS on "not a restatement of the round-24 entry"; FAIL as worded on the magnitude.**
The lane-new ground is real; the *field* content the row sells as expansion is a published
design's own field list, and the entry's arithmetic for that claim is false.

**Impacts:** coverage (the claim's own axis), calibration (a false sentence inside an admitted
entry), novelty (the row must not inherit construct credit from a restated published protocol).

**Smallest safe correction.** (The entry is still untracked — `git status` shows
`?? corpus/knowledge/contamination-transparency-card.md` — so correct in place now; once committed,
QUALITY's append-only-errata rule applies.) Set R1's CTC cell to `strata_reported`, S1's and S2's
status to `already a column`; replace `:68-70` with: "Every field here is a column one of the three
published designs already carries; the two the lane's staged text called deltas (S1, S2) and the
one it called a new value set (R1) are CTC v1.1's `contamination_controls.acquired` block,
declared-negative vocabulary and `strata_reported` block. What this entry adds is the crosswalk and
the CG1–CG8 gate, not a field." And delete "core" from anything downstream of claims `:23`.

## Attack 2 — does the round claim a coverage score it does not move?

**Claim under attack.** `SCORECARD.md:1022` axis cell "**coverage** (lowest non-retired, tie-break)",
verdict "7 → 7 held … the canonical coverage score stays 7 while the round-25 L0 coverage cap is
open. The claim is the ledger delta, not a raised number." Claims `:42-44` states the same intent.

**What actually checks out.**
- No axis is raised anywhere in the round-30 section: C1 7→7, C2 8→8, C3 8→8, and the
  other-axes paragraph holds depth 9 / novelty 7 / freshness 8 / adjacency 8 / calibration 8.
- The cap being cited is the right cap and it is still open (L0 line verified above).
- The counting command that the frozen predicate names reproduces exactly, both ends.

**Where it still overclaims (the counterexample).** "Real expansion" is not a unit the coverage
rubric measures. The rubric's +1 anchor is two-legged: "every surface the corpus *describes* is
indexed **and** every index row exists on disk (both directions); `PROVINCE.md` enumerates
surfaces that resolve" (`SCORECARD.md:249`). Round 30's row exercises only the first leg, and that
leg was already satisfied before the round (38/38 both directions). The second leg is untouched:
`PROVINCE.md` has no round-30 paragraph, while round 24 — the precedent the row implicitly leans on
— counted `province_map_sections 0 → 4` (`SCORECARD.md:599`) and round 24's verdict cell reads
"improved (counts)" (`:616`). So the honest currency is *counts* (registry 82→88, knowledge
38→39, index 38→39), not "real expansion". Two rounds running (29 attempt 2, 30) have now
discharged the lowest-axis obligation on an axis that `plans/round-25-claims.md:12` itself says
"cannot change its number" — the escape-hatch hazard a round-25 critic named forward
(`.ufo/waves/round-25/falsify/CritMappingFresh.md` §3). That is not this round's defect; it is the
reason the row must not dress a counts delta as expansion.

**Verdict: PASS on the number, FAIL on the currency word.** 7 → 7 held is honest and the cap is
cited correctly; "real expansion on ground the lane did not hold" is an unmeasured upgrade of
round 24's "improved (counts)".

**Impacts:** coverage (the axis), calibration (ledger discipline).

**Smallest safe correction.** Replace "real expansion on ground the lane did not hold" with
"improved (counts); the number does not move", and add the round-24 unit list plus the explicit
statement that the PROVINCE leg is unchanged.

## Attack 3 — is the axis label right (coverage vs depth)?

**Claim under attack.** Axis cell `**coverage** (lowest non-retired, tie-break)`; claims `:42` "the
entry is new corpus bytes…"; and the counter-hypothesis that the artifact is a *depth* move, since
it ships two decision tables (field mapping; CG1–CG8 with "answerable from / not answerable when")
against the depth rubric's "+1 when a decision table/threshold is derived from a read source and a
reader can act on `SKILL.md` alone" (`SCORECARD.md:246`).

**Test of the depth hypothesis.** The second leg fails: `SKILL.md` is untouched this round
(`git status --porcelain` lists no `SKILL.md`; `grep -n 'card\|transparency' SKILL.md` returns only
the pre-existing contamination re-check lines 63-64, 681). A reader cannot act on `SKILL.md` alone —
the CG table lives only in the entry. So depth's +1 does not fire, and "coverage" is the right
label at the six-axis level. AXES' own definition also fits: coverage is "fraction of the domain's
real surfaces the skill governs (repo paths, tools, **edge classes**)", and "how to read a
benchmark's contamination claim" is an edge class the corpus can now reach.

**Where the label is still imprecise — the sub-row is unstated.** Round 25 recorded the mapping of
record: `novelty` is a sub-axis of canonical **coverage/constructs**, and "coverage/surfaces keeps
its own row and cap" (`SCORECARD.md:655-663`). The landed row takes its *expansion* language from
the constructs side ("real expansion … amendment + CG1–CG8 gate") and its *hold reason* from the
surfaces side (the L0 cap, which caps surfaces). A row cannot spend one sub-row's currency and cite
the other's cap. This round it makes no numeric difference — both sub-rows sit at 7 — but it makes
the sentence unauditable: `adoption_check.py` is a registry/index counter (surfaces), and it cannot
see the constructs claim at all, which is exactly the predicate gap CritC1 already recorded
(`build/R30CritC1.md` §Attack 3: the predicate never reads the coverage-map row or the frontier
bullet).

**A second, smaller mis-cite.** The other-axes paragraph holds depth at 9 because "the entry adds a
field mapping against a published union table, **no new instrument claim**". "Instrument" is a
novelty criterion (`:244`), not a depth leg. The depth hold should rest on the depth rubric's own
legs (SKILL.md unchanged; citation resolution unchanged).

**Verdict: PASS on the axis choice (coverage, not depth); FAIL on precision (sub-row unnamed;
depth hold reasoned from the wrong rubric).**

**Impacts:** coverage (label), depth (hold reason), novelty (must not be charged for the crosswalk).

**Smallest safe correction.** Name the sub-row in the axis cell: `coverage (surfaces)`. Keep the
CG-gate/field-mapping description in the verdict cell as *what the bytes are*, not as a constructs
delta. Rewrite the depth hold on the depth rubric's own legs.

## What survived attack (recorded so the round does not over-repair)

1. C1's frozen predicate is mechanically sound and reproduces byte-for-byte; its control receipt
   prints `entries=0 … exit=1`.
2. The entry genuinely lands lane-new corpus bytes; it is not a duplicate of the round-24 entry,
   and it names its extension target (§Extends) as QUALITY Q6 requires.
3. No axis number is raised. The round-25 cap is the correct cap and it is still unruled.
4. The scorecard's scope notes on C3 (no URL binding, CJK-25-word cap inert, PDF text layers) are
   honest and I found nothing to add to them.

## The exact SCORECARD wording (drop-in replacements)

C1 row, axis cell:

> **coverage (surfaces)** — lowest non-retired, tie-break; held by the open round-25 L0 cap

C1 row, verdict cell:

> **7 → 7 held — improved (counts)**, number held by the open round-25 L0 coverage cap (still
> unruled). Counts it moves: registry 82 → 88 rows (S081–S086; tier A 76→79, B 4→7), knowledge
> files 38 → 39, index rows 38 → 39 with 39/39 parity both directions. Counts it does not move:
> `PROVINCE.md` carries no round-30 section, so the rubric's "PROVINCE enumerates surfaces that
> resolve" leg is unchanged. What the new bytes are: S081's published four-field disclosure
> protocol (strata, elicitation budget, five types, regeneration — its released CTC v1.1 form
> carries `strata_reported`, the type-5 run-side block and the declared-negative rule) crosswalked
> into the round-6 union table's columns, plus the CG1–CG8 answerability gate the staged package
> already drafted (`R29a2ConnCapability.md:27`), re-grounded on six rows opened 2026-10-25.
> Frontier bullet 2 is **partly** discharged: the card-format half lands; the bullet's
> `unopened lead` — benchmark-maintainer releases on hidden-test governance — is still unopened.
> No construct, method or phenomenon credit is taken, and the claim is the ledger delta, not a
> raised number.

Other-axes sentence, depth clause:

> depth 9 (held on the depth rubric's own legs: `SKILL.md` is unchanged, so "a reader can act on
> `SKILL.md` alone" is not met, and citation resolution is unchanged; the field mapping is a
> crosswalk, not a new instrument claim — instrument criteria belong to novelty)

Two words the round must not use downstream of this row: **"core"** (no landed referent — README
says "Partly discharged", PROVINCE has no round-30 section) and **"real expansion on ground the
lane did not hold"** (replaced by "improved (counts)" + the list above).

## Adjacent defect this seat found while testing the axis (one-line fix)

The six new rows carry **no byte identity**: `corpus/SOURCES.md:107-112` give URL + quote + line
number, while round 29's S077–S080 rows carry `sha256` and byte counts. The captures live only in
`/tmp/r30-*` (e.g. `/tmp/r30-R30SrcS081/`), which is the `/tmp`-pointer pattern round 14's lesson
rejects at closure, and it means the new `--artifact <capture>` mode of C3's gate has **no committed
artifact** to run against for this round's own six rows. Fix: paste each seat's §2 sha256 + byte
count into its anchor cell (all six are printed in `build/R30SrcS08{1..6}.md`), as round 29 did.
Impacted axes: freshness, operability (the gate's own evidence path).

## Limits of this report

- I did not re-derive the S082–S086 source verdicts; those are other seats' items
  (`falsify/R30FxSrcS08{1,2,4,6}.md` are landed and I read their verdict lines only). My S081 fetch
  is an independent byte-identity cross-check (`4c81bd3c…` matches the seat's), not a re-admission.
- `S123` is not in this lane's registry (the entry says so); my CTC read is against the commit the
  entry's own union table pins, fetched today, sha `05131be9…`, retained in scratch.
- Everything above is measured on the working tree, which is where the round's bytes currently
  live (all round-30 files are untracked/modified; `HEAD` is `363a4eb`).
- No tools installed or upgraded by this seat (curl and `python3` stdlib only, both already on the
  host; PACMAN not invoked).
