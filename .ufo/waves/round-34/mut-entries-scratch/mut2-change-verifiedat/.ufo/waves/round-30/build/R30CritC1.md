# R30CritC1 — falsification of C1 (coverage: contamination-transparency amendment)

Reviewer seat: R30CritC1 (L1Kengaku30). Leaf; read-only on the lane. No production edit was made; the
only lane file written is this report. Nothing was installed (pdftotext and curl were already present;
no pacman, no uv, no npx).

Lane tip observed: `363a4eb` ("round-29 verifier spot-check (integrator, hyaku)"), detached.
Counting command is the round-29 one, unmodified: `git hash-object plans/adoption_check.py` =
`20726fc0bd1cc9765b2b88bec0e202c0617348e3` = `git rev-parse HEAD:plans/adoption_check.py`
(`git diff --stat HEAD -- plans/adoption_check.py` empty). So "unchanged from round 29" is true and
everything below is a defect of the *frozen* predicate, not of a drifted tool.

`git status` note: the lane tree moved during this review (the entry, the README coverage-map row,
the six registry rows and `plans/sources_adopt.py` landed at 04:31). Probes were run against a
snapshot of `corpus/` taken before that edit, and re-run against the live tree at the end. Both
results are reported; every probe tree is preserved under `/tmp/r30-critC1/`.

## Measured base facts

| fact | command | result |
|---|---|---|
| registry rows | `grep -cE '^\| ?S[0-9]{3}' corpus/SOURCES.md` | 82 pre-edit (S077–S080, S090, S091 last); 88 after the C1 append |
| S081–S086 present pre-edit | `grep -nE '^\| ?S08[1-6] ' corpus/SOURCES.md` | absent — the six rows are a real registry delta |
| control reproduces | `adoption_check.py --lane <pre-append copy> --expect …/adoption-expect.json --census` | `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok` / `exit=1`, **byte-for-byte identical** to `.ufo/waves/round-30/claims/control-nothing.txt` (`diff` empty) |
| live tree now passes | same command, `--lane .` | `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok`, exit 0 |
| freeze is not attested | `git log --all --oneline -- plans/round-30-claims.md` | empty; `git ls-files plans/round-30-claims.md` → 0; `.ufo/waves/round-30/adoption-expect.json` → 0. All `??` untracked |

---

## Attack 1 — is the admission a duplicate of lane-held knowledge?

**Verdict: the duplicate charge FALLS; the amendment's evidence base does not yet carry it (separate defect).**

Side-by-side bytes.

`corpus/knowledge/contamination-detection-and-transparency.md:70` (lane-held, round 24) already orders:

> `| Reporting a contamination check | Name detector family, model access (weights/logits/black-box), contamination tier tested (T1–T4), and what a negative cannot rule out | Write "uncontaminated" from one detector's negative |`

and `:73`:

> `| Choosing a benchmark for a claim | Prefer suites with a documented transparency card or auditable construction | Treat a private/hidden split as proof of cleanliness |`

The card's CG2/CG3/CG4 ask exactly those three things (detector access / tier+datasets tested / what a
negative does not rule out — `contamination-transparency-card.md:78+`). So 3 of 8 gate questions are a
restatement. But the parent *names* a "transparency record" and a "documented transparency card" and
never defines either (parent `:14`: "keep a transparency record rather than report \"clean\""); the
landed entry defines them, and carries CG1, CG5–CG8, R1, R2, R5, S1, S2 that the parent has no bytes
for (`grep -rlnE 'Q1–Q8|card format|transparency card' corpus/knowledge/` → only the parent before
the landing). A restatement of 3 questions over 5 new ones is an extension, not a duplicate.

Two things the claim must still add, both invisible to the counter:

1. **The amendment's decisive table is uncited inside the lane.** The landed §"It is an amendment, not
   a fourth design" derives "exactly two fields are new as *fields* (S1, S2)" from a union table whose
   three columns rest on the campaign file's S122–S124
   (`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md`,
   source lines S122/S123/S124). `grep -nEi 'AI Alliance|contamination-disclosure-paper|Jangulo|gem-main|trust-safety-evals' corpus/SOURCES.md`
   → no match; `grep -nE '^\| S12[0-9]' corpus/SOURCES.md` → no rows. QUALITY Q2 says every
   load-bearing claim rests on a lane `SOURCES.md` row for that scope. The "amendment, not a rival"
   verdict *is* the load-bearing claim C1 claims to discharge, and its evidence is outside the
   registry. Smallest safe correction: admit S122–S124 (three rows) **or** stop asserting the field
   delta and state the union table as an external hand-off that this lane has not verified.
2. **The counter cannot tell the amendment from the rival it refuses.** The entry's own §Rejected says
   the staged text "presents R1–R5/S1–S2 as *the* card format and never names the three published
   designs". Probe A (below) lands the staged text **byte-identical except one date** and the frozen
   counter prints the pass line and exits 0. So the amendment's status rests on §Extends/§Rejected
   prose that no check reads. Correction in Attack 3's list (add a parent-link field).

---

## Attack 2 — can the frozen counter pass with a round that opens nothing?

**Verdict: STANDS.** The literal do-nothing round is killed (control reproduces byte-for-byte), but a
round that re-fetches nothing scores the exact frozen line. Six bypasses, each executed.

The counter reads only these things (line numbers = `plans/adoption_check.py`):

- `:34` `SOURCE_LINE_RE = re.compile(r"^source:[ \t]*(S[0-9]{3,})\b", re.MULTILINE)` — ids only, from any `source:` line in the entry.
- `:77` `if re.search(r"^\| \`knowledge/" + re.escape(name) + r"\` \|", readme, re.MULTILINE):` — the **only** read of `corpus/README.md`.
- `:79` `if re.search(r"^verified-at: " + re.escape(access_date) + r"\b", text, re.MULTILINE):` — the only content check on the entry itself.
- `:81` `cited.update(SOURCE_LINE_RE.findall(text))`.
- `:88` `rows_mined = sum(1 for row_id in cited if row_id in registry and registry[row_id][7] == "mined")` — **cell 7 only**; cell 8 (`opened`), cells 4/5/6 (`teaches`/`anchor`/`quote`) are never read.
- `:98` `usedby_ok += 1 if linked else 0` over `entry["sources"]` and `registry[row_id][10]`.
- `:122` `and len(cited) == required` — a **count**, never a set comparison against `entry["sources"]`.

### B1 — `opened=` is never checked; a re-dated copy of the staged bytes passes
Probe A: lane `corpus/` snapshot + the six staged rows (used-by trimmed to the entry, `recheck` set to a
valid `180d` because the staged prose recheck trips census E09) + the staged card with **only**
`verified-at: 2026-10-23`→`2026-10-25`:

```
$ diff <(sed 's/verified-at: 2026-10-23/verified-at: 2026-10-25/' <staged card>) <probe entry>
IDENTICAL apart from verified-at
$ python3 plans/adoption_check.py --lane /tmp/r30-critC1/probe-shokunin --expect …/expect.json --census
entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok      exit=0
$ (six rows) status=mined opened=2026-10-23 recheck=180d …   ← predicate demands opened=2026-10-25
```

This is precisely round 29's *secondary* rejection reason (`corpus/lessons/round-29.md:226-227`: "all six
sources carry the campaign's `2026-10-23` opened date and none was re-opened this round"). The flip's
required re-opening is unobservable to the counting command.

### B2 — cited-id identity is never checked; the entry can cite rows the lane already holds
Probe B: same tree, entry's six `source:` lines rewritten to the six already-held ids
(S077, S078, S079, S080, S090, S091), the six new rows left uncited:

```
entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok      exit=0
```

(The probe kept the staged URLs beside the substituted ids, so the entry asserted "S077 — https://arxiv.org/abs/2608.29463":
the counter is blind to id↔URL identity too.) Answer to "can it pass with rows the lane already holds":
**yes, for `cited_rows`/`rows_present`/`rows_mined`**; only `usedby_ok` forces the six new rows to exist,
and it forces nothing about their content.

### B3 — `quote`/`anchor`/`teaches` cells are never read; empty rows pass
Probe C: the six new rows with `teaches = anchor = quote = "—"`:

```
entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok      exit=0
```

The row still exists with `status=mined` and a `used-by` path, and the census raises no code for a mined
row with no quote (W03 only fires on `used-by = —`; E-codes never read cells 4/5/6).

### B4 — the entry body is never read; a stub scores
Probe D: entry reduced to the six `source:` lines + `verified-at: 2026-10-25` + `# stub` + "No body. No
quotes. No Q-gate.":

```
entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok      exit=0
```

So "an entry whose quotes were never fetched" passes in the strongest possible form: an entry whose
quotes do not exist. The frozen predicate's sentence — "same condition in the counter's code" — is false
on this clause: the claim's kill rule ("a cited source whose located quote cannot be found in this
round's own fetch is refused") has no code path at all.

### B5 — the kill rule's own middle band is unscoreable
Kill rule: "if fewer than four of the six survive, the entry is not admitted", i.e. 4–5 surviving is an
admission. Probe E cites 5 of 6 (S086 demoted to prose, registry row still mined and used-by):

```
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok      exit=1
```

`exit=1` because `len(cited) == required` demands exactly 6. So the state the kill rule calls *admitted*
can never print the passing line, and the state it calls *refused* (six cited, two quotes unlocatable —
B3/B4) does. The predicate and the kill rule disagree about the same outcome. Correction: the predicate
must either drop the partial-admission clause or gain a counted field (`quotes_located`) so 4/6 is a
scorable state.

### B6 — "frozen" has no git evidence
`plans/round-30-claims.md`, `.ufo/waves/round-30/adoption-expect.json` and `.ufo/waves/round-30/claims/`
are all untracked at `363a4eb` and appear on no ref (`git log --all -- plans/round-30-claims.md` empty).
Round 29 named its freeze commit (`SCORECARD.md:988`, `8c14a5dc…`); round 30 names none, so "a predicate
changed after a seat has scored is not this claim's predicate" cannot be checked, and the claims file's
own phrase "Control (committed at freeze)" is false in the tree. This is the same class as C2's D4.

### Live-state recheck (for fairness, not credit)
The landed tree is far better than the staged object: all six rows `opened=2026-10-25`, quotes carry
line-level locators, S082's URL was corrected from `/abs/2607.01254` to `/html/2607.01254v2`, and the
entry has `## Extends`. None of that is what the counter measures — every row above would pass either way.

Side observation while checking the kill rule (fetched 2026-10-25): the **staged** S081 quote was not a
byte substring — staged row reads `"We operationalize the taxonomy as a four-field disclosure protocol…"`,
the abstract says `"We operationalize it as a four-field disclosure protocol…"` ("taxonomy"→"it",
`arXiv:2608.29463` abs page). The staged S082 quote is absent from the page its row cites (`/abs/`), and
present only in `/html/2607.01254v1`. S083/S084/S085/S086 quotes locate in decoded PDF/HTML bytes
(`pdftotext`). So under the claim's own kill rule the staged set survives 4/6 — the exact band B5 shows
is unscoreable.

---

## Attack 3 — does the axis label match the surface the predicate moves?

**Verdict: STANDS (predicate gap).** The claim names coverage and names two surfaces — the Frontier bullet
("moves from *unopened lead* to *core*") and "the admission bar's fallback ladder". Neither is in the
counting command: `:77` is the *only* README read and it matches the file index row, not the coverage map
(`- **…**: covered at …`) and not the Frontier list. QUALITY **Q7** — the lane's own bar — requires
"Entry file, its `corpus/README.md` index row **and its coverage-map row** land together", and Q6 requires
the entry to name what it extends; the counter checks neither.

Proof: probes A–E all passed with the coverage map and Frontier bullets **byte-identical** to round 29's:

```
$ diff <(grep 'Contamination detection and transparency' <lane README>) <(grep … probe README>)   # probe A..E: no new coverage bullet
$ grep -c 'contamination-transparency-card' /tmp/r30-critC1/probe-shokunin/corpus/README.md
1        ← the index row only
```

The live tree does now carry the coverage-map row (`corpus/README.md:242`, "**Contamination transparency
card format** …") and the Frontier edit (`:274`), added by hand. So the surface exists; what is missing is
that the frozen command would score identically if it did not, and would score a stub entry (B4) beside
it. The axis verdict ("the row records the ledger delta and an `improved` trend") will therefore be
asserted on a surface the counting command cannot see.

On the label itself: the artifact's shape is depth-shaped (SCORECARD `:247`, depth = "a decision
table/threshold is derived from a read source"), and coverage's +1 is "every surface the corpus *describes*
is indexed and every index row exists on disk" — C1 adds a described surface and keeps parity, so it
cannot move the number, which the claim says honestly. The round-24 precedent ("coverage … 7 (held by cap;
counts moved)", `SCORECARD.md:370`) makes a counts-moved coverage claim legitimate — but only if the counts
it moves are counted. The predicate counts registry rows and one index row; it does not count coverage-map
rows or frontier discharges. That gap is the defect, not the label.

---

## Impacted axes

- **coverage** — the axis C1 files on is measured by a command that omits the coverage-map row Q7 requires;
  a regression that dropped it would be invisible. C1's coverage ledger delta is therefore unverified in
  the one artifact the rubric's supervisor reads.
- **calibration** — the claims file asserts a three-way identity ("one sentence, same condition in the
  counter's code, same label in the receipt"). Three of the predicate's conditions (identity of the six
  ids, `opened=2026-10-25`, quote ground truth via the kill rule) have no code; the kill rule's partial band
  is unscoreable; the freeze is unattested. A predicate that overstates its own counter is a calibration
  defect even when the landing happens to be honest.
- **operability (cross-claim, C1↔C3)** — the round's own new gate refuses one of C1's rows. Running C3's
  landed parser over the six live anchor cells (`sources_adopt.quoted_spans`, `plans/sources_adopt.py:281`):

  ```
  S081 spans=3  S082 spans=2  S083 spans=2  S084 spans=3  S085 spans=0 reason='no-quote'  S086 spans=2
  ```

  S085's anchor cell wraps its quotes in curly quotes (“方升”) and leaves the second span undelimited, so
  `quoted_spans` returns `no-quote` and `quote_check` exits 4 (docstring `:343-348`; `EXIT_MALFORMED`
  returned at `:417`). C1 requires S085 `mined`; C3's gate refuses its row. Both are frozen this round. Smallest correction: put straight
  `"` delimiters around the two S085 spans (cheapest, C1-side) or teach `quoted_spans` the lane's CJK
  convention (C3-side) — one, not both, and record which.
- **freshness** — the six rows now carry `opened=2026-10-25` and the entry a matching `verified-at`; the
  counter cannot witness either (B1). No freshness credit should be booked on the counter's line alone.

## Smallest safe correction (in order)

1. **Add the missing checks to the frozen command** (this is what makes the claim's sentence true), one
   new counted field each, all cheap string work:
   - `cited_ids_ok` — `set(cited) == {id for entry in entries for id in entry["sources"]}` (kills B2).
   - `opened_ok` — `registry[row_id][8] == access_date` for every cited id (kills B1).
   - `quote_ok` — `registry[row_id][5]` non-empty and ≠ `—` for every cited id (kills B3); pass each span
     through `plans/sources_adopt.quoted_spans`/`words` so C1 and C3 cannot disagree (kills the S085
     collision).
   - `body_ok` — the entry carries its declared sections (`## Extends`, the gate table, `## Rejected`) —
     a `^## ` heading-set comparison, not prose scoring (kills B4).
   - `coveragemap_ok` — `re.search(r"^- \*\*Contamination transparency card", readme, re.MULTILINE)` and
     the Frontier bullet for the card no longer containing `(unopened lead)` (satisfies Q7, closes Attack 3).
   - `extends_ok` — the entry contains a `## Extends` block naming
     `corpus/knowledge/contamination-detection-and-transparency.md` (satisfies Q6, closes Attack 1's
     predicate half).
   Print all six in the same line and require them in `ok`; keep the old seven so the round-29 comparison
   stays legible.
2. **Reconcile the kill rule with the predicate**: either delete "fewer than four …" or make `quotes_located`
   a counted field and admit 4/5 explicitly. As frozen, the rule cannot be reached (B5).
3. **Commit the freeze** (`plans/round-30-claims.md`, `adoption-expect.json`, `claims/`) before any wave
   seat is scored, and name the commit hash in the claims file the way round 29 does (B6, C2/D4 class).
4. **Source the union table in-lane**: admit S122–S124, or demote "exactly two fields are new" from an
   assertion to a hand-off. Q2 is not satisfiable by a sibling repo's rows.
5. **Fix S085's anchor cell** to carry straight-quoted spans, so C1's admitted rows pass C3's validator.

## What I did not verify (honesty)

- I did not re-open all six sources against the *landed* entry's every locator (line 344/397/315, p.32/p.34,
  printed page numbers); I checked the six *staged* quote strings against fresh captures fetched today
  (curl HTTP 200 for all six URLs; S083/S085/S086 decoded with `pdftotext`; whitespace-normalised CJK
  comparison). The 4/6 survival count is against those captures, not against the round's own receipts —
  so it stands as "the kill rule's band is reachable", not as a verdict on the landing.
- I did not exercise C3's `--quote-file/--artifact` CLI (its `main()` is not yet in the worktree file); I
  imported `quoted_spans` in-process, which is the function the CLI calls at `:376`.
- The lane moved under this review; the pre-edit snapshot is at `/tmp/r30-critC1/probe-shokunin` and the
  live pass line was re-run at the end. A later edit invalidates the live half of the table, not the
  counter's code, which is hash-pinned above.
