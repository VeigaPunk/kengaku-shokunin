# R33L0Packet — L0 coverage-cap decision packet + Q22 criterion row (round 33, hyaku run 7)

Seat `R33L0Packet-2`, lane `kengaku-shokunin`, access date **2026-10-25** for every source opened.
Assignment: draft verbatim (1) the `l0-questions.md` append line for the coverage-cap decision
packet (considerthese/2026-10-25 proposal 3) and (2) the `QUALITY.md` Q22 row (proposal 2), plus the
proposal-status table.

## State observed before drafting

| observation | value | how read |
|---|---|---|
| lane `master` (local = `origin/master`) | `78955888542258ba369f5aa72c200c913b4c3c90` | `git rev-parse master`; `git branch -avv` |
| lane worktree HEAD while this report was written | `2b4cef2` (detached: `git branch -avv` shows `* (no branch)`) | `git rev-parse --short HEAD` |
| Q22 criterion already in the tree | `corpus/QUALITY.md:255-271` | `sed -n '255,271p'`; `git show HEAD:corpus/QUALITY.md` |
| L0 line already in the fleet queue | `.ufo/l0-questions.md:163`, fleet commit `22d28422` | `git log -1 -- .ufo/l0-questions.md` (read-only) |

Both artifacts this seat was asked to draft had already been integrated when it started: the Q22
criterion in lane commit `7895588` ("… Q22, defects-after receipt") and the L0 append in fleet
commit `22d28422` ("round-33: kengaku l0 question — coverage-cap decision packet"). I wrote neither
(my write scope is this file). The blocks below are therefore the drafts **as they must read**, and
each is byte-identical to the integrated bytes — asserted mechanically by the checks recorded under
"Receipts", not by eye.

## L0 questions

Block 1 — the `l0-questions.md` append line, one line, verbatim:

```text
kengaku | round-33 | decision packet: what committed evidence lifts the round-25 L0 coverage cap (SCORECARD coverage held at 7 across four rounds of real expansion)? Candidate classes: (a) a PROVINCE.md coverage-surfaces section with N newly resolving surfaces, (b) N further rounds of net-new admitted entries, (c) a rubric change the operator names, (d) the cap stays until the absent surfaces return.
```

Shape and provenance:

- Format matches the queue header (`<lane> | round-<N> | <question>`, `.ufo/l0-questions.md:24`
  "append-only"). 404 bytes on one line; sha256
  `3013ae12bce1ab46f7829231343ca26650ec71a3346d1079bf131a0a1272de4e`.
- It is a decision, not an implementation request: the operator can rule (a), (b), (c) or (d); the
  line names the evidence class each option accepts, which is what proposal 3 asks for
  ("stating exactly what evidence lifts the cap", considerthese/2026-10-25.md:46-51).
- It supersedes nothing: the round-25 filing (`.ufo/l0-questions.md:72`, coverage cap) stays as the
  original question; this line is the packet filed against it.
- The parenthetical's round count is **not** the count its source gives — see finding F2. The queue
  is append-only, so a correction is a further line, never an edit of this one.

## Q22 criterion row

Block 2 — `corpus/QUALITY.md` lines 255-271, verbatim (the row with the criterion heading it lives
under; 1294 bytes, sha256
`e6167a154732df8ff5a3875a95fdb9e0774beedc99793b813e4be0661500d020`):

```markdown
## Round33 criterion — a receipt is only evidence if something re-runs it at the tip

- **Q22 — a committed counter output is a claim about bytes at a revision; it must re-run at the
  lane tip and reproduce, or it is stale debt.** A `defects=0` / `exit=0` receipt proves the
  counter's reading of the tree it ran on — nothing else. When the receipt and the tip disagree
  (round 31's `gate-cli-exits.txt` greened only at the wrong path; round 32's draft receipt said
  "not the claimed after-state" while seats cited it as closure), the receipt is debt, and the
  honest fix is to re-run the same command on the current tip and commit the new output beside the
  old one. Executable check: every receipt a claim cites must name the revision it was produced
  at, and the round's final receipts must re-run at `git rev-parse master` before the report
  closes.
  The proposal and its date are `considerthese/2026-10-25.md` §Self-improvement suggestions 2
  ("one persistent routed-defect ledger … includes a tip-receipt validator", 2026-10-25) — this
  criterion is the cheap half of that proposal: the per-round counter pattern continues, but every
  final receipt now re-derives at tip. Limits: it does not build the persistent `defects.jsonl`
  ledger the proposal sketches; that stays unimplemented and is named here as debt. Lesson:
  `corpus/lessons/round-33.md`.
```

How the assigned compressed draft was adjusted to QUALITY.md's row format:

1. **Section heading.** QUALITY.md files each criterion under `## Round<NN> criterion — <short
   title>` (`## Round30 criterion …` at `:196`, `## Round31 criterion …` at `:235`). Q22 gets
   `## Round33 criterion — a receipt is only evidence if something re-runs it at the tip`.
2. **Bold lead kept to two sentences.** The assigned one-sentence lead is split after "stale debt.";
   "the frozen counter" became "it" because the criterion binds *any* committed counter output, not
   only a frozen predicate's counter. The row states the failure mode first, then the remedy —
   Q21's order (`:237-250`).
3. **Demonstration widened from one instance to two.** The assigned draft named round 31; the
   landed row adds round 32's draft receipt. Both resolve verbatim in the tree:
   `corpus/evidence/round31/gate-cli-exits.txt:2` ("pre-repair copy superseded: its run resolved
   `../../../plans/` to the absent `.ufo/plans` and every line failed") and
   `corpus/evidence/round32/defects-after.txt:6` ("This is not the claimed after-state; the
   remaining five checks are still red.").
4. **Citation moved to the row's provenance sentence, citing the lesson file.** The assigned
   trailing "Cites considerthese/2026-10-25.md." becomes the format's three-part close: "The
   proposal and its date are …" + "Limits: …" + "Lesson: `corpus/lessons/round-33.md`." The lesson
   cited names Q22 back (`corpus/lessons/round-33.md` §Round-33 disclosures, "corpus/QUALITY.md
   gains **Q22** …"), so the citation resolves in both directions.
5. **Cheap half declared.** The proposal's fuller mechanism (`corpus/defects.jsonl` ledger,
   two-recurrence registration block, tip-receipt validator) is named as unimplemented debt in the
   row's Limits — verified absent: `ls corpus/defects.jsonl` → No such file, and no plan re-runs a
   closed defect's check across rounds (only per-round `plans/roundNN_defects.py`).
6. **One gap carried over from the assigned draft:** the "Executable check:" sentence is an
   obligation in prose, not a command — see finding F1.

## Proposal-status table (considerthese/2026-10-25.md §Self-improvement suggestions)

| # | proposal (short) | status | ground |
|---|---|---|---|
| 1 | Model-diverse verification: run the §3 discernment sample through a second, different model on a seeded sample ≥5/round, log agreement + disagreements in SCORECARD | **Operator-side, not lane-actionable.** A lane cannot discharge it: it needs (i) a second model bound to the sample — routing is the operator's table and a lane never passes a model (this round's run-7 role map is host-side; seat prompts carry no model field), and (ii) a SCORECARD agreement/disagreement block plus the "admissible discernment improved" rule, both fleet scoring policy. The lane can only report the symptom the proposal names (all 18 roles route to `@m_flash`, so "non-author" = same model). | considerthese/2026-10-25.md:34-38; `corpus/lessons/round-33.md` §Round-33 disclosures ("operator-side and not lane-actionable") |
| 2 | One persistent routed-defect ledger (`corpus/defects.jsonl`: id, class, opened_round, closing_commit, recurrence) with a checker that re-runs closed defects forever, blocks pre-registration on a twice-recurring class, and validates receipts at tip | **Grounded this round as Q22 — cheap half only.** Q22 lands the tip-re-run hygiene rule and is mechanically exercised by C2's counter and C3's `--verify`; the ledger, the recurrence block and the receipt validator are *not* built and Q22 names that as debt (`corpus/defects.jsonl` absent). | `corpus/QUALITY.md:255-271`, landed `7895588`; block 2 |
| 3 | A decision packet for the round-25 L0 coverage cap: state exactly what evidence lifts the cap (e.g. a `PROVINCE.md` coverage-surfaces section with N new demand-side surfaces), and stop spending the lowest-axis slot on counts until ruled | **Grounded this round as the L0 append.** Filed in the fleet queue with four candidate evidence classes (a)-(d), so the operator rules by class. The second half (redirect the lowest-axis slot) stays the lane's round-planning judgement, not a criterion. | `.ufo/l0-questions.md:163`, fleet `22d28422`; block 1 |
| — | 2026-10-24 proposal 1 (run the gates on every push, `.github/` workflow) | **Grounded in round 30** as Q20 (out-of-band gate run as a landing obligation). The workflow itself is still unimplemented, and Q20 records that as measured absence (`.github/` absent). | `corpus/QUALITY.md:196-233` |
| — | 2026-10-24 proposal 2 (as-of date + live/dead status per entry, then re-probe the live ones) | **Grounded in round 31** as Q21 (cheap half: a pinned source must name its pin). The re-probe half was taken by round 32's C3, which *failed as declared*; round 33's C3 is the byte-retained retry. | `corpus/QUALITY.md:235-253`; `SCORECARD.md` §Round 32 |
| — | 2026-10-24 proposal 3 (demand-side coverage measurement: 30-40 frozen questions graded answerable/correct/cited/stale) | **Not grounded.** No Q row and no L0 line cites it; coverage stays supply-side (index parity, census counts, construct counts). | grep over `corpus/`, `SCORECARD.md`, `LOG.md`, `plans/`, `considerthese/`: the only 2026-10-24 citations are `QUALITY.md:230`, `QUALITY.md:248`, `LOG.md:909`, `plans/round-32-claims.md:91` |
| — | 2026-10-21:44-49 (seat-yield ledger per role family, cut a zero-yield family after two rounds) | **Grounded in round 29 attempt 2** as Q19. | `corpus/QUALITY.md:186-195` |

## First falsifiers — Q22 applied to the round that lands it

Q22's first clause ("every receipt a claim cites must name the revision it was produced at") and
its second clause ("the round's final receipts must re-run at `git rev-parse master`") are testable
today. Round 33's receipts, as read at `2b4cef2`:

| receipt | names its revision? | re-run at the reading tip |
|---|---|---|
| `corpus/evidence/round33/defects-after.txt` | **yes** — `# revision: c227e486a622ff82aae780c6fc58f023dcc82430` (line 5) | `python3 plans/round33_defects.py --lane .` → `checks=6 defects=0` / `exit=0` |
| `corpus/evidence/round33/catalogs/after.txt` | **no** — date only (`probed=2026-10-25`); bytes bound by `SHA256SUMS` instead | `python3 plans/catalog_probe.py --verify --lane .` → `raw=ok … verify=ok`, exit 0; `sha256sum -c SHA256SUMS` → `hf.raw.json: OK`, `or.raw.json: OK` |
| `.ufo/waves/round-33/assimilation/gate-receipts.txt` | **no** | not re-run by this seat (gate commands are C1's receipt chain) |
| `.ufo/waves/round-33/claims/census-before.txt` | **no** | freeze control, not re-run |
| `.ufo/waves/round-33/claims/defects-before.txt` | **no** | freeze control, not re-run |
| `.ufo/waves/round-33/claims/control-nothing.txt` | **no** | freeze control, not re-run |
| `.ufo/waves/round-33/claims/control-verify.txt` | **no** | freeze control, not re-run |

One of seven round-33 receipts names a revision. The second clause is satisfied for C2 (the
counter reproduces) and for C3's four numbers (the verifier re-derives them offline from the
committed bytes); it is not satisfied for C1, which has no committed after-receipt at all — see F4.

## Findings

**F1 — Q22 ships an obligation labelled "Executable check" with no command.** Q20 and Q21 each name
a literal one-command check at that place in the row (`:207-209` the `git archive` extract-and-run
line; `:245-246` the `for f in corpus/knowledge/*.md …` line), and Q19 names its absence check
(`:190-192`); Q22's
sentence is prose, and no instrument implements it: no plan reads `# revision:` lines, and there is
no tip-receipt validator (Q22 itself names only the `defects.jsonl` ledger as debt). The cheap
mechanical form is real and was run here —
`grep -rL '^# revision: [0-9a-f]\{7\}' --include='*.txt' corpus/evidence/round33/` prints exactly
`corpus/evidence/round33/catalogs/after.txt`, i.e. the one receipt with no revision line. That
command (or its equivalent) is the missing sentence; landing it is a QUALITY.md amendment, which is
not this seat's write scope.

**F2 — the filed L0 line's "four rounds of real expansion" is one more than its source.** The
proposal reads "Three rounds of real expansion each recorded '7 → 7 held'"
(`considerthese/2026-10-25.md:46`); the filed line says four. A four-round reading is defensible
only by counting round 24 (five sourced entries, `SCORECARD.md:585-626`) alongside rounds 29a2, 30
and 31 — the line does not say which four, and under the cap SCORECARD records coverage 7 in far
more rounds (24, 25, 26, 27, 28, 29, 29a2, 30, 31, 32). The queue is append-only: a correction must
be a further line naming the four, not an edit of line 163.

**F3 — round 33's C3 receipt carries a stale field at the landing commit.**
`corpus/evidence/round33/catalogs/after.txt` ends `entry=pending` while the same commit contains
the entry block it refers to (`corpus/knowledge/open-model-catalogs.md:66` "## Re-probe 2026-10-25
(round 33)") with the same four numbers; `catalog_probe.py --verify` checks the four numeric tokens
and the entry block, not the `entry=` field, so `verify=ok` coexists with a false statement about
tree state. This is exactly Q22's class (a receipt that describes a tree other than the one it
landed on); Q22's own remedy is to commit a fresh receipt beside the old one, not to edit it.

**F4 — C1 has no committed after-receipt.** `corpus/evidence/round33/` contains only
`catalogs/` and `defects-after.txt`; `adoption_check.py`'s after-value (`entries=1 … usedby_ok=1
census=ok`, the value the claims file freezes as C1's counting command) exists only in
SCORECARD/report prose at the landing commit, while rounds 30 and 31 each committed
`corpus/evidence/roundNN/adoption-after.txt`. Under Q22 the final receipt is the unit of evidence,
so C1's closure is missing one. The claim's verdict is not mine to judge; this is the receipt layer
only.

**F5 — both demonstrations Q22 cites resolve verbatim.** Verified above: round 31's
`gate-cli-exits.txt:2` and round 32's `defects-after.txt:6`. No paraphrase is being passed as a
quote.

**F6 — sequencing.** The Q22 row and the L0 line were landed by other seats before this one ran, so
this report is the drafting record plus the provenance/compliance audit, not the landing. If the L1
acts on F1/F2/F3/F4 it must do so as new bytes (a QUALITY.md amendment line, a new queue line, a
new receipt) — the append-only rules for the fleet queue and for filed reports forbid rewriting
what is already there.

## Out of scope / not done

- No production edits: this file is the only byte written under the lane. Nothing written to
  `/home/vgpnk/Projects/shokunin`, `/home/vgpnk/Projects/shokuknow`, sibling lanes, `.ufo/state`,
  `watchdog.log`, `MANIFEST.json`, or any Git index; all Git use was read-only
  (`log`, `show`, `diff`, `status`, `rev-parse`, `branch -avv`, `ls-tree`).
- Not run by this seat: `plans/adoption_check.py`, `plans/round33_c1_verify.py` (C1 is another
  seat's claim and neither is needed for these two artifacts), the falsify wave, any wave tool, and
  any live network probe (C3's bytes were already committed; `--verify` is offline by design).
- No tool installed or upgraded — `python3` and coreutils were sufficient, so the tooling directive
  has nothing to record for this seat.
- Lane state moved under concurrent integration during this seat (Q22/defects commit `7895588` at
  `master`; round-33 landing commit `2b4cef2` detached at read time). Every statement above names
  the revision it was read at; nothing here asserts what the final branch will contain.

## Receipts

Byte identities of the two blocks (canonical text extracted to scratch, then asserted present
verbatim in this report):

- `sed -n '163p' /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` → 404 bytes, sha256
  `3013ae12bce1ab46f7829231343ca26650ec71a3346d1079bf131a0a1272de4e`
- `sed -n '257,272p' corpus/QUALITY.md` → 1294 bytes, sha256
  `e6167a154732df8ff5a3875a95fdb9e0774beedc99793b813e4be0661500d020`

Executed checks (this seat, lane worktree; `git rev-parse master` = `7895588…`, HEAD = `2b4cef2`;
each command's own output is quoted, not summarised):

```
$ sh plans/l0_filed_check.sh .ufo/waves/round-33/build/R33L0Packet.md /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md
FILED   report:29 queue:163 kengaku | round-33 | decision packet: what committed evidence lifts the round-25
l0_filed_check: sections=1 questions=1 filed=1 unfiled=0
exit=0
```

```
block1: present=True bytes=404 sha256=3013ae12bce1ab46f7829231343ca26650ec71a3346d1079bf131a0a1272de4e
block2: present=True bytes=1294 sha256=e6167a154732df8ff5a3875a95fdb9e0774beedc99793b813e4be0661500d020
```

(Substring assertion: the canonical text extracted from `.ufo/l0-questions.md:163` and from
`corpus/QUALITY.md:257-271` occurs verbatim in this report.)

```
$ python3 plans/round33_defects.py --lane .
checks=6 defects=0
exit=0
```

```
$ python3 plans/catalog_probe.py --verify --lane .
raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok
HF missing fields: author, sha, lastModified, gated
exit=0
```

```
$ (cd corpus/evidence/round33/catalogs && sha256sum -c SHA256SUMS)
hf.raw.json: OK
or.raw.json: OK
```

```
$ grep -rL '^# revision: [0-9a-f]\{7\}' --include='*.txt' corpus/evidence/round33/
corpus/evidence/round33/catalogs/after.txt
exit=0
```

VERDICT: l0-drafted
