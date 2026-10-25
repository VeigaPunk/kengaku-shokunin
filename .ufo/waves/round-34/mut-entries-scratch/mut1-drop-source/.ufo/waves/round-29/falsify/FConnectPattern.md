writer: KengakuR29-2.FConnectPattern-2

# FConnectPattern — is the r29 "derived control vs source operation unit" lesson new?

Seat `KengakuR29-2.FConnectPattern-2` (leaf connector, no subagents). Lane root
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`; lane HEAD `56fd949a6478342531e61f4feecb4a685d831640`.
Round 29 only. Target: `.ufo/waves/round-29/drafts/lesson-and-mistake.md` (sha256
`399666d8fca5ebea316e9f51f5b647bcb8665b8e581e4c38512456e6410485e7`, 128 lines), compared against
`corpus/lessons/round-26.md`, `round-27.md`, `round-28.md`, plus the working-tree lesson
`corpus/lessons/round-29.md` (sha256 `989991715e7a8458b4b9850ce7e153c2cff10401e8952c95b527391fc2aaad76`,
25 lines, `git status` = `??` untracked).

**Independence statement.** I did **not** read `plans/config_projection.py` source. I executed it
read-only (`--summary`, `--json`) and read its stdout only; all production claims below are CLI output
or receipts. No production, fixture, corpus, SOURCES, SCORECARD, candidate, Git/JJ or sibling file was
edited. No delegation, no network, no linter. No tool install or update was performed (nothing needed;
existing `/usr/bin/python3` 3.14).

## Axes named

1. **Novelty accounting** (C1, score 7 held) — a repeat booked as a new principal inflates the ledger's
   novelty story even while the score stays fixed.
2. **Calibration 8** — must be untouched; this item scores no forecasts.
3. **Ledger / admission integrity** — mistake-id uniqueness, class semantics, and a count unit that can
   actually discriminate.
4. **Verification surface** — no instrument/fixture edits; the fix must reuse receipts that already exist.

## Evidence

### E1 — Ledger state: M85 is not free, and the draft's id premise is false

`python3` row inventory over `corpus/lessons/round-*.md` (union of the table form `| M<n> | class |` and
three bullet forms): **66 row definitions, 66 unique ids, no duplicate definition**. All ids M1–M89 occur
(an any-mention scan over the same lesson files finds no gap in 1..89); **no id above M89 occurs in
`corpus/lessons/`**; the earliest lesson block (round-24) uses a form my patterns do not match and is not
counted here. Observed definitions at the top end:

| id | file:line | class |
|---|---|---|
| M84 | `corpus/lessons/round-28.md:175` | number-drift |
| M85 | `corpus/lessons/round-28.md:281` | attribution |
| M86 | `corpus/lessons/round-28.md:285` | scope |
| M87 | `corpus/lessons/round-29.md:15` | attribution |
| M88 | `corpus/lessons/round-29.md:16` | provider |
| M89 | `corpus/lessons/round-29.md:17` | scope |

The draft says `the next free number after M84 is M85` (8 words, `drafts/lesson-and-mistake.md:26`).
M85/M86 are r28 bullet rows appended in the **post-falsification "Actual-commit conformance correction"**
section, i.e. outside the main mistakes table that ends at M84. [INFERENCE] The draft's parenthetical was
derived from a table-only read. Next free id is **M90**, not M85.

Consequence beyond numbering: the principal the draft proposes to record is **already recorded** at
`round-29.md:15` as M87. If admitted as written, the draft duplicates a row that already exists.

### E2 — The lesson is a repeat in principle: at least eight prior rows record the same invariant

The invariant r29 states ("a control can agree with the instrument on every frozen input while disagreeing
with the source operation") already has a continuous record. All quotes below are ≤25 words
(`len(q.split())` run by this seat; counts in parentheses).

| row | file:line | class | recorded content (fragment) |
|---|---|---|---|
| M43 | `round-26.md:15` | vacuous | `no exact transform-span rule` (4); fix: transform span fixed, `independent oracle must agree` |
| M51 | `round-26.md:105` | scope | `frozen aggregate counts alone did not test exact transform semantics` (10); fix: oracle corrected to exact transform semantics, edge controls added |
| M52 | `round-26.md:106` | vacuous | `a generic-input mutation could be semantic no-op` (7); fix: collision-safe token plus explicit selftest |
| M54 | `round-26.md:177` | vacuous | `the intended negative controls stayed green` (6); fix: remove inherited correction, red then green |
| M55 | `round-27.md:13` | survivor | `replacing commit-tree reads with working-copy reads survives the old exit-vector` (10) |
| M59 | `round-27.md:149` | vacuous | `E6 last→first fence mutant survived the shipped selftest58 cases` (9) |
| M63 | `round-27.md:175` | vacuous | `exposed positive-fixture-only guards` (3) |
| M76 | `round-28.md:167` | survivor | `Hand-expected malformed/precedence cases added` (4); the r28 "untested-control" row the prereg names |

r29's own instances fit this lineage exactly: order-insensitivity (M51/M52) and a green selftest that
only saw positive fixtures (M54/M59/M63/M76). Two of the three r29 mutants are no-ops on frozen data —
the M52/M54 mechanism, not a new failure mode: `mutation-witness.txt` records
`wrong_order_reversed ... TOTAL findings=0 exit=0` and `index_by_task_id ... TOTAL findings=0 exit=0`.
Only the key-name URL-only mutant is a genuine frozen-data failure (`findings=6 exit=1`), and it is the
sole evidence for the capability's non-URL reach.

**Methodological note on the assignment window.** The comparison was framed as `M65-M86`, which is r28's
range only. Inside that window the r29 lesson looks new; widening one round back (M39–M64) shows it is a
repeat of r26 M51/M52 and r27 M63. [INFERENCE] The window, not the lesson, produces the appearance of
novelty.

### E3 — What is genuinely new is narrower: two instance properties, both already prereg-required

`grep -n "json.loads\|ordinal\|enumerate(" corpus/lessons/round-2*.md` returns **no row**: no prior
mistake row covers a text→parse pipeline or positional output identity. Those are the only increments:

1. **Representation level with a parse-failure codomain.** The source is `text → json.loads` (generator
   lines 10, 20). A control that operates after the parse cannot represent the source's failure mode
   (`projection_json_invalid`), only a different value. No r26–r28 row had a two-stage pipeline whose
   correct unit can emit non-parseable output.
2. **Positional output identity.** Filenames come from `enumerate` (lines 21–22), so identity is the list
   position; the frozen 812/812 `index == task_id` equality is a population coincidence, not the rule.

Both are already frozen in the prereg (`plans/round-29-claims.md:73-80`), so they are scope, not a new
method. The draft's "principal" is the general form of E2, not E3.

### E4 — The draft's evidence pointer inverts the prereg

Draft `:30` states `the r29 plan requires an independent oracle that is a URL-only leaf walk` (13 words).
The prereg says the opposite in two places:

- `plans/round-29-claims.md:80`: `performs its own leaf walk/census for benign profiles` (8 words) — a
  census walk, not a URL-only substitution.
- `plans/round-29-claims.md:45-46`: `No URL normalization, escaping repair or URL-only substitution is silently introduced.`
  (11 words) — URL-only is permitted only as a *named* control, which is what the draft itself proposes in §4.

So the row's justification ("the plan requires the wrong thing") is not supported by the prereg text. The
stated plan requirement is already the correct text contract; the real open item is whether the *control*
implements it, which is a different sentence.

### E5 — The draft mines a different set than the prereg names

- Prereg `:98`: `Mine r28's source/projection attribution and untested-control mistakes (M74/M75/M76) into a new specific` (12 words).
- Draft `:15-17`: M74, M75, **M81**.

M76 (`round-28.md:167`, survivor: mutants survived a positive-fixture-only selftest) is the closest single
ancestor of the draft's own "a control counts only after its witness is observed to fail", and the prereg
names it explicitly. M81 (`round-28.md:172`, reference-drift: citation ranges and runtime assumptions) is
not in the prereg's named set and is the least related. One slot is swapped.

### E6 — The live row M87 carries three defects: class, lineage, count unit

`corpus/lessons/round-29.md:15` (untracked at HEAD):

- **Class.** `attribution`. Every prior `attribution` row is about *which authority a claim or byte is
  attributed to*: M33 (`round-25.md:72`, a rejection reason misstates a theorem's coverage), M74
  (`round-28.md:165`, hash then re-read), M75 (`round-28.md:166`, invented defaults), M79
  (`round-28.md:170`, hand annotation called AST-derived), M85 (`round-28.md:281`, heading-form PASS
  substituted for an anchored verdict line). M87's subject is a **control's operation unit**, which r26
  already classes as `scope` (M51) or `vacuous` (M52/M54); r27 has a composite precedent
  (`M62 · survivor/scope`). [INFERENCE] No identity or evidence-hash claim is at stake in M87, so the
  attribution label follows neither its own subject nor the corpus's use of that class.
- **Lineage.** `round-29.md:19-21`: `M87 is the round's principal mined mistake; it extends r28 M74/M75`.
  The nearest ancestors are r26 M51/M52 and r28 M76 (and r27 M63), none cited. The prose's
  `not whether a control reproduces the source operation's unit` (9 words) is exactly what M51 already
  covers.
- **Count unit.** Row text: `URL-only leaf rules miss 0 frozen URL leaves` (8 words). This number is 0
  under *both* URL-only definitions and therefore cannot discriminate. The same receipt distinguishes
  them: `url_only_substitution ... TOTAL findings=6 exit=1` (killed) versus
  `wrong_order_reversed ... findings=0 exit=0` and `index_by_task_id ... findings=0 exit=0` (identical on
  frozen data). `build/R29CritCountUnit.md` CE-2 supplies the discriminating figure — key-name URL-only
  misses 61 leaves, value-shape misses 0 — and requires the definition to be named. M87 names neither.

M87 uses the unit that is 0 by construction; M89 in the same file records the discriminating 61 vs 0 for
the adjacent quantity, so the two rows give a reader opposite impressions of whether URL-only can be
distinguished on frozen data.

### E7 — The candidate knowledge entry is already instance-scoped, so the overclaim is confined to the row

`drafts/webarena-config-projection.md` (sha256
`7006b93dcacff38736cb49f2153e2b3960591887576b3e8c2ddc3519565653dc`) says, correctly, that the `url-only`
hand witness and its mutant fail; that `Order is invisible on the frozen profiles.` (7 words); that
`Positional output naming is invisible on the frozen order.` (8 words); and that this is
`not a new method (novelty score held)` (7 words). The candidate frames these as **population limits**; the
lesson row frames the same facts as a **new principal**. The contradiction is inside the round package: the
entry is honest, the row is not.

## Mismatches (exact location, exact value)

| # | location | observed value | conflicting value |
|---|---|---|---|
| D1 | `drafts/lesson-and-mistake.md:26` | `the next free number after M84 is M85` | M85 = `round-28.md:281`, M86 = `:285`; ids M1–M89 all in use, no M90 occurs; next free is **M90** |
| D2 | `drafts/lesson-and-mistake.md:30` | `the r29 plan requires an independent oracle that is a URL-only leaf walk` | prereg `:80` `leaf walk/census`; prereg `:45-46` forbids silent URL-only substitution |
| D3 | `drafts/lesson-and-mistake.md:15-17` | mined set {M74, M75, M81} | prereg `:98` names {M74, M75, M76} |
| D4 | `corpus/lessons/round-29.md:15` | class `attribution` | precedent M51 `scope`, M52/M54 `vacuous`, M76 `survivor`; all five prior `attribution` rows (M33, M74, M75, M79, M85) concern claim/evidence identity, not a control's operation unit |
| D5 | `corpus/lessons/round-29.md:15` | `URL-only leaf rules miss 0 frozen URL leaves` | discriminating value: 61 missed non-URL leaves (key-name rule, observed mutant `findings=6`) vs 0 (value-shape rule, critic census); the row names neither definition |
| D6 | `corpus/lessons/round-29.md:19-21` | `extends r28 M74/M75` | nearest ancestors: r26 M51/M52, r27 M63, r28 M76 (prereg `:98` names M76) |
| D7 | `drafts/lesson-and-mistake.md:19` | `Gap these leave open (the principal of this draft)` | r28 M74's own fix is `Permanent post-read-replacement controls cover raw JSON and scorer bytes` (9 words, `round-28.md:165`) — the red-witness discipline is prior art inside the three rows the draft says leave it open |

No mismatch in the draft's witness *design*: W1/W2/W4 map onto the fixtures actually adopted
(`plans/fixtures/r29/hand/cascade-order.case.json`, `url-only.*`, `index-shuffled-ids.fixture.json`) and
the instrument selftest names them (`build-selftest.txt`: `hand_cascade_order_R29_ORDER_CASCADE_01`, …,
`cases=20`, exit 0). The fix is sound; the novelty framing and ledger placement are not.

## Proposed move (one, bounded)

**Rewrite M87 in place in `corpus/lessons/round-29.md` before it is committed** (the file is untracked, so
this is a pre-landing correction, not an erratum), and withdraw the draft's `M85` label. No other file
changes. Proposed row:

```
| M87 | scope | corpus/evidence/round29-calibration/mutation-witness.txt: reversed-order and index-by-task_id
mutants each print TOTAL findings=0 exit=0 on the frozen 812x3 data; key-name URL-only misses 61/1416
changed leaves and dies at findings=6 exit=1, while the critic's value-shape URL-only census misses 0
leaves (build/R29CritCountUnit.md CE-2 requires the definition to be named); CE-1: all 720 orders
byte-identical. Captured-by: prereg line 100; no general QUALITY criterion (Q15/Q16 are
gate-fixture-specific). |
Selftest consumes three hand fixtures (cascade, URL-only, shuffled IDs), cases=20 exit0. Instance, not a new
principle: the same invariant is recorded at round-26 M43/M51/M52/M54, round-27 M55/M59/M63 and round-28 M76 -
a control must be shown to fail on a witness the frozen population cannot supply. Instance-level increments
only: (i) representation level `text -> json.loads`, so the control must share the source's parse-failure
codomain (projection_json_invalid); (ii) positional output identity (enumerate ordinal, not task_id). No
method, score or calibration credit. |
```

Second-order effects traced:

- **Novelty**: no score change; the correction keeps C1's "no method novelty" boundary (`round-29-claims.md`
  C1 text, F5) and the candidate's own `not a new method (novelty score held)` statement consistent with the
  lesson. The two instance increments stay on record, so the capability's coverage is not shrunk.
- **Calibration**: untouched — no forecast is rescored; F1/F2/F4 are already observed elsewhere.
- **Ledger**: class counts move attribution 6→5 and scope 14→15. No frozen assertion covers class counts:
  P4e's ids are `P4e.sources.S0xx.used-by` SOURCES cells (`plans/state_check.py:432`,
  `plans/fixtures/r27/p4_assertion_ids.txt:45-50`), and no SOURCES row changes.
- **Verification surface**: the row cites receipts that already exist; no new test, fixture or code.

If L1 prefers to keep the draft's two provenance defects as their own row (the false id and the inverted
plan claim), that row is class `number-drift`, id **M90**; it must not be folded into M87, whose subject is
the control unit.

## Risks and contradictions

1. **Ownership**: `corpus/lessons/round-29.md` is L1-owned and untracked; this seat cannot and does not edit
   it. The proposal is text for L1, not a change.
2. **Unstated contradiction to resolve, not smooth**: the same round records both "URL-only cannot be
   distinguished" (M87's unit) and "URL-only mutant fails at findings=6" (mutation-witness, candidate). Both
   are true for *different definitions*; the row must name the definition, as CE-2 says.
3. **Class taxonomy has no canonical enumeration** in `corpus/QUALITY.md` (grep for class names returns
   nothing); it is precedent-based. A reader who greps `attribution` for evidence-pin controls (the r28 M74
   use) will get a false hit while M87 keeps that class.
4. **Demoting "principal" could look like scope shrinkage.** It is not: the row keeps all observed
   failure evidence and both new instance properties; only the novelty claim changes.
5. **Comparison window**: the target names `M65-M86`, which excludes M43/M51/M52/M54 and M55/M59/M63; if
   L1 keeps that window for the novelty comparison, the repeat finding disappears by construction.

## Verification

1. `python3 plans/config_projection.py --summary` → exit 0, `TOTAL findings=0 exit=0`,
   `INDEX {"index_equals_task_id": 812, "violations": 0}`, occurrences 385/336/281/300/0/133 = 1435,
   `changed_leaf_count=1416`, `changed_leaves_by_category={"non_url_field": 61, "url_field": 1355}`.
2. `cat corpus/evidence/round29-calibration/mutation-witness.txt` → control `cases=20` exit 0;
   `wrong_order_reversed` exit 1 killed, `summary [... findings=0 exit=0]`;
   `url_only_substitution` exit 1 killed, `summary [... findings=6 exit=1]`;
   `index_by_task_id` exit 1 killed, `summary [... findings=0 exit=0]`.
3. `cat corpus/evidence/round29-calibration/build-selftest.txt` → `SELFTEST clean cases=20`, names include
   `hand_cascade_order_R29_ORDER_CASCADE_01`, `hand_url_only_R29-URL-ONLY-UNREAD-METADATA-01`, `exit=0`.
4. Re-run the id inventory: `grep -n "^| M8[5-9]\|^| M90" corpus/lessons/round-2*.md` plus the bullet-row
   regex; expect M85/M86 at `round-28.md:281/285`, M87–M89 at `round-29.md:15-17`, no M90.
5. After L1's edit, re-run `python3 plans/config_projection.py --selftest` (expect `cases=20`, exit 0) and
   confirm the row's cited numbers still match the receipts byte-for-byte.
6. Q10 re-read of any corrected row must find the cited ancestor lines in `round-26.md:105-106,177`,
   `round-27.md:175`, `round-28.md:167`.

## Unknowns and boundaries

- I did not read production source, so I make no claim about how the instrument implements order, URL
  categories or the index check beyond CLI output and the mutation receipt.
- Whether L1 will admit a separate M90 number-drift row is a planner decision; this item proposes one
  row, not the ledger's final shape.
- The frozen `812x3` nondiscrimination of order, WIKIPEDIA, codepoint-vs-byte offsets and ordinal identity
  is a property of this pinned population (`build/R29CritCountUnit.md`), not of WebArena generally.
- Adjacent observation, not load-bearing: `plans/fixtures/r29/hand/cascade-order.case.json` still carries
  `status: "hand-expected design; no behavioral experiment executed"` while `build-selftest.txt` shows that
  fixture consumed and the mutant killed; the status string is stale, the fixture is live.
- No credentials, env values, cookies, profile stores or private URLs were read or recorded. All profile
  values in scope are synthetic `*.invalid`.

VERDICT: PARTIAL
