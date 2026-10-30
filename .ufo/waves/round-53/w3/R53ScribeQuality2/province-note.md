# PROVINCE.md — does it need a change this round, and the exact replacement line

Seat `R53ScribeQuality2`, round 53 wave 3. Lane HEAD `9ead4476bf55b1ea6490d0204b668195db4a4d1d`.
All probes ran in scratch clones under `/fast/scratch/hyaku/kengaku-r53/R53ScribeQuality2/`; the lane
tree was not edited.

---

## 1. Verdict

**PROVINCE.md needs exactly one change for round 53: the "Public-literature registry" row at
`PROVINCE.md:113`, whose cell still claims 171 SOURCES rows while the registry holds 186.** That
row is the one the registry probe flags (`NUMBER-DRIFT SF14 row claims 171, probe says SOURCES
rows=186`).

**Nothing else changes.** The round's three new surfaces — the classifier, the label files and the
tip-state ledger — do **not** need a PROVINCE row, and adding one would *break* the round-51
surfaces counter (measured, §4). The registry probe's own second complaint, `STALE SF20` (the
round-51 successor endpoint at `127.0.0.1:45669`/`1234`), is an operator-host surface that this
round did not touch and that the round-51 successor row records as a live endpoint; this note does
not propose a change to it, and says so explicitly rather than leaving it ambiguous.

---

## 2. The grep that shows the three new surfaces are not in PROVINCE.md

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ grep -nE "round53|round-53|round53_c1|tipstate|round53-c1|labels\.json|classify" PROVINCE.md
$ echo $?
1
```

Exit 1 = no match. PROVINCE.md names none of: the classifier
(`plans/round53_c1_classify.py`, sha256 `935db122…`), the eight label files
(`.ufo/waves/round-53/w1/C1Label*/labels.json`) and the eight shards
(`.ufo/waves/round-53/labels/shard-*.json`), or the tip-state ledger
(`plans/round53-tipstate.json`). This is consistent with the round-51 landing: `PROVINCE.md` has not
changed since commit `11e79380` (`git log 11e79380..HEAD -- PROVINCE.md` → empty), and the round's
instruments are declared where the lane declares instruments — SKILL.md's gate/probe registry
(`SKILL.md:639-641`, rows `round53-c1`, `round53-c2`, `stage-scan`) and `corpus/README.md`.

**Why a PROVINCE row is not wanted.** `plans/round51-surfaces.json` carries **one manifest entry per
table row** of the two sections it watches (`"sections": ["## Surfaces", "### Core"]`), and the
counter's `UNCOVERED` leg fails any row of those sections without an entry. Measured in a scratch
clone: adding one row to `### Core` **without** a manifest entry gives
`ROWS section="### Core" rows=11 entries=10 uncovered=1` and
`DETAIL UNCOVERED ### Core row line 113 has no manifest entry` → `PREDICATE R51-C1 fail`
(receipt `probes/probe-H-core-row-no-manifest-entry.txt`). Adding the row **and** a manifest entry
gives `rows=11 entries=11 uncovered=0` (receipt
`probes/probe-G-core-row-plus-manifest-entry.txt`) — but that is a second edit to a *frozen*
round-51 manifest, bought for a row that would say nothing the registry does not already say. The
L1 decides; this seat's recommendation is **not** to add the row.

---

## 3. The row the registry probe flags, and the exact replacement

### 3.1 The probe output (scratch clone of HEAD `9ead4476`)

```
$ cd /fast/scratch/hyaku/kengaku-r53/R53ScribeQuality2/lane
$ python3 plans/round51_surfaces.py --lane .
REV 9ead4476bf55b1ea6490d0204b668195db4a4d1d
MANIFEST plans/round51-surfaces.json entries=20 sections=2
ANCHORS total=20 dup=0 missing=0
ROWS section="## Surfaces" rows=10 entries=10 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=20 present=13 absent=7 errors=0
DRIFT 0
STALE 1
  DETAIL STALE SF20 probe=absent state=present (http://127.0.0.1:1234/health -> <urlopen error [Errno 111] Connection refused>)
UNVERDICTED 0
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 171, probe says SOURCES rows=186
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

The claim the probe compares against is **the manifest's** `count_claim`, not the row's prose:
`plans/round51-surfaces.json` → entry `SF14` carries `"count_claim": 171`, and
`plans/round51_surfaces.py:205-208` compares that integer with the probe's count
(`"pattern": "^\\|\\s*S[0-9]{3,}\\s*\\|"` over `corpus/SOURCES.md`, measured 186). **Editing
PROVINCE.md alone does not clear NUMBER-DRIFT** (measured, §4 probe F: the row's prose changed,
`NUMBER-DRIFT 1` remained). **Editing the manifest's `count_claim` alone does clear it** (probe E:
`NUMBER-DRIFT 0`) but leaves the PROVINCE.md prose lying at 171, and the row's own text is what a
reader sees. The honest repair is therefore **both**, in the order the append-only rule allows: an
appended dated correction note in the row's cell, plus the manifest's `count_claim` — but the
manifest is a frozen round-51 artifact, so **the L1 decides whether it may be amended**; this seat
only reports what each edit does.

### 3.2 The exact current row line (byte-for-byte, `PROVINCE.md:113`)

```
| Public-literature registry | `test -e corpus/SOURCES.md` | present; 171 rows (round 51: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 171; 170 at the round-51 base tip plus S178), contract-v1 census clean (`corpus/evidence/round24-census/after.txt`); receipts `corpus/evidence/round24-sources/gate.md` |
```

### 3.3 The exact replacement line (byte-for-byte, tested in a scratch clone)

```
| Public-literature registry | `test -e corpus/SOURCES.md` | present; 186 rows (round 53: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 186; 171 at the round-51 base tip through S178, plus S179–S193), contract-v1 census clean (`corpus/evidence/round24-census/after.txt`); receipts `corpus/evidence/round24-sources/gate.md` |
```

Every number in the replacement is measured, not inferred:

| number | how it was measured |
|---|---|
| 186 rows now | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **186** (and `grep -c '^| S[0-9]' corpus/SOURCES.md` → 186; both patterns agree) |
| 171 at the round-51 base tip | `git show 11e79380:corpus/SOURCES.md \| grep -cE …` → **171** (the round-51 landing itself); its parent `11e79380^` → **170** |
| "through S178" | `git show 11e79380:corpus/SOURCES.md \| grep -oE '^\|[[:space:]]*S[0-9]+' \| tail -1` → `S178` |
| "plus S179–S193" | `git diff 11e79380..43438294 -- corpus/SOURCES.md \| grep -oE '^\+\|[[:space:]]*S[0-9]+'` → exactly `S179 … S193`, 15 rows; `43438294` is the round-52 landing commit |

The wording keeps the row's own house style ("round NN:" prefix, the counting command inline, the row
count first) — the round-51 landing used the same shape for the same row
(`git show 11e79380 -- PROVINCE.md` replaces "25 rows" with the 171-row sentence).

**The count in the replacement is the count at HEAD `9ead4476`, and it will not be the count at the
landing tip.** Measured at the time of writing: the lane's working tree already carries **28
uncommitted SOURCES rows** (`git status --porcelain corpus/SOURCES.md` → ` M corpus/SOURCES.md`;
`git diff corpus/SOURCES.md | grep -oE '^\+\|[[:space:]]*S[0-9]+'` → `S900 … S927`; the working-tree
count is already **214** against HEAD's 186). Those are the wave-3 source seats' rows, and
`.ufo/waves/round-53/facts.md` says the L1 assigns the real ids from S194. So:

* the **L1 must re-run the counting command at the landing tip** and substitute that number into
  the replacement line — the row's own convention already demands it (the round-51 landing wrote
  "round 51: `grep -cE …` → 171", a number that was true at its own tip);
* the **manifest's `SF14.count_claim` must be set to the same landing-tip number**, because the
  counter compares it with the probed count at the tree it is run on (§3.1) — a `count_claim` of 186
  is correct for the tip I measured and wrong for a tip that carries the new rows;
* the prose "171 at the round-51 base tip through S178, plus S179–S193" stays valid regardless of
  how many rows land after S193.

### 3.4 The manifest side (the L1's call)

`plans/round51-surfaces.json`, entry `SF14`, one field:

```json
"count_claim": 171
```

becomes

```json
"count_claim": 186
```

`plans/round-51-claims.md:24` calls the manifest a **frozen** instrument
(`Instrument (frozen): plans/round51_surfaces.py + plans/round51-surfaces.json`), and the round-51
lesson/claims do not provide an amendment path for it the way round 53's claims do. **This seat does
not edit it** — it is the lane's frozen surface manifest, and amending it is the L1's decision. What
is measured is what each edit does (§4).

---

## 4. What each candidate edit does — measured

All four probes are full `python3 plans/round51_surfaces.py --lane .` runs in scratch clones of
HEAD `9ead4476`; the receipts are saved verbatim under
`.ufo/waves/round-53/w3/R53ScribeQuality2/probes/`.

| probe | edit(s) applied | `NUMBER-DRIFT` | `UNCOVERED` | `ROWS "### Core"` | `PREDICATE R51-C1` | receipt |
|---|---|---|---|---|---|---|
| baseline | none | **1** (`SF14 … 171 … 186`) | 0 | rows=10 entries=10 | fail (also `STALE SF20`) | (the §3.1 run) |
| F | PROVINCE.md row prose only | **1** (unchanged) | 0 | rows=10 entries=10 | fail | `probes/probe-F-province-prose-only.txt` |
| E | manifest `count_claim` → 186 only | **0** | 0 | rows=10 entries=10 | fail (only `STALE SF20` left) | `probes/probe-E-manifest-count-only.txt` |
| D | both edits | **0** | 0 | rows=10 entries=10 | fail (only `STALE SF20` left) | `probes/probe-D-both-edits-province-row-and-manifest-count.txt` |
| H | one extra `### Core` row, no manifest entry | 1 | **1** | rows=11 entries=10 | fail | `probes/probe-H-core-row-no-manifest-entry.txt` |
| G | one extra `### Core` row **and** a manifest entry | 0 | 0 | rows=11 entries=11 | fail (only `STALE SF20` left) | `probes/probe-G-core-row-plus-manifest-entry.txt` |

Read this as: **the PROVINCE row edit is a truthfulness fix for the file's reader; the manifest edit
is what the counter reads.** Neither alone makes the `round51-surfaces` registry row green, and
**neither alone makes the row's *exit code* green either** — after both edits the counter still
prints `PREDICATE R51-C1 fail` and exits 1, because `STALE SF20` is independent of the count.

**A consequence the L1 must schedule with the fix (probes I and J).** The tip-state ledger declares
`round51-surfaces` as `state: "red"`, `exit: 1`, with
`"evidence": "NUMBER-DRIFT SF14 row claims 171, probe says SOURCES rows=186"` and a reason that
names only the count. The C2 counter re-executes that row and requires the declared evidence
fragment to appear **verbatim in the observed output**
(`plans/round53_c2_tipstate.py:308`). Measured:

* probe I — the manifest count amended but **uncommitted** → the source tree is dirty
  (`SOURCE … clean=NO`), the row is not executed against the fix, and the old fragment is still
  produced (`evidence_missing=0`);
* probe J — the manifest count amended **and committed** → the row runs against the fixed tree and
  the declared fragment is gone:
  `EVIDENCE-MISSING round51-surfaces fragment not in output`,
  `RUN executed=1 timeout=0 mismatched=0 evidence_missing=1`, `PREDICATE R53-C2 fail`
  (receipt `probes/probe-J-ledger-evidence-after-committed-count-fix.txt`).

So fixing the count **invalidates the ledger row's evidence string**: the L1 must re-declare the
`round51-surfaces` row in `plans/round53-tipstate.json` at the same time as the manifest edit —
its `evidence` must become the fragment that is still printed after the fix (the `STALE SF20` line),
and its `reason` must name both causes. Leaving the ledger as-is while landing the count fix would
turn a truthful red row into an `EVIDENCE-MISSING` row.

### 4.1 The `STALE SF20` line — explicitly *not* proposed for change here

`STALE SF20 probe=absent state=present (http://127.0.0.1:1234/health -> Connection refused)` is a
**host** surface: `PROVINCE.md:15`'s "Served local model (round 51 successor)" row asserts that
`http://127.0.0.1:45669` and `http://127.0.0.1:1234` resolve. This round did not stop that server,
did not move it, and cannot start it (the operator's host service; the seat spec forbids restarting
a host service, and the pacman/host guard forbids it). Repairing it is a host-surface decision for
the L1/operator, not a PROVINCE.md text change this round can make truthfully — a row may only be
marked `ABSENT <date>` when the absence is re-verified on the host, which is outside this seat's
write scope and outside this round's work. **Recommendation: leave `PROVINCE.md:15` alone this
round** and let the L1 decide separately (either re-verify the endpoint or date the absence), so
that the round-53 landing does not assert a host state nobody re-checked.

---

## 5. What was checked and found not to need a change

| check | command | result |
|---|---|---|
| the three round-53 surfaces are absent from PROVINCE.md | `grep -nE "round53\|round-53\|round53_c1\|tipstate\|round53-c1\|labels\.json\|classify" PROVINCE.md` | exit 1, no match (§2) |
| PROVINCE.md has not drifted since round 51 | `git log 11e79380..HEAD -- PROVINCE.md` | empty |
| the round-53 instruments are declared where the lane declares instruments | `grep -n "| \`round53-c1\`\|\| \`round53-c2\`\|\| \`stage-scan\`" SKILL.md` | `SKILL.md:639`, `:640`, `:641` |
| the proposed row edit does not move the `### Adjacent` heading that `SHONEN.md:12` points at (`PROVINCE.md:129`) | `grep -n "^### Adjacent" PROVINCE.md` in the edited clone | still line 130; `SHONEN.md`'s pointer is `PROVINCE.md:129`, which was already a blank line before this round (the `state-assertion-check` red row) and is unchanged by this edit |
| the proposed row edit does not break Q41's pointer audit | `python3 plans/round50_c2_audit.py --lane .` in the edited clone | `POINTERS total=299 paths=233 hashes=66 resolved=299 exists=221 superseded=3 never-landed=9 unresolved=0` |
| the proposed row edit does not add a `state_check` mismatch | `python3 plans/state_check.py --summary` in the edited clone | `assertions=329 match=317 mismatch=1 superseded=6 offline_unverifiable=5` — the same single pre-existing mismatch (`P3c.box.4.pointer.1:12`, the `PROVINCE.md:129` pointer), unchanged |

---

## 6. Summary for the L1

1. **Land** the replacement line in §3.3 at `PROVINCE.md:113` — it is the row the registry probe
   flags and the only PROVINCE.md row whose number is false at HEAD. The provenance of 186 is in
   §3.3's table — **but re-run the counting command at the landing tip and substitute that number**:
   the working tree already carries 28 uncommitted SOURCES rows from the wave-3 source seats
   (count 214 vs HEAD's 186), and the manifest's `count_claim` must carry the same landing-tip
   number.
2. **Decide** whether `plans/round51-surfaces.json`'s `SF14.count_claim` may be amended 171 → the
   landing-tip count. That manifest is round-51-frozen (`plans/round-51-claims.md:24`); this seat
   did not touch it and only reports that the manifest edit is what the counter reads (probe E).
3. **Do not add** a PROVINCE row for the classifier, the labels or the ledger (probe H: it makes
   `UNCOVERED 1`), and **do not touch** `PROVINCE.md:15` / `STALE SF20` this round (§4.1).
4. Whatever is decided, the ledger row `round51-surfaces` in `plans/round53-tipstate.json` must be
   re-declared to name **both** remaining causes — after the count fix, `STALE SF20` is what still
   keeps the exit at 1 (probes D/E) — **and the re-declaration must land with the count fix, not
   after it**: a committed count fix makes the row's current `evidence` fragment disappear and the
   counter then reports `EVIDENCE-MISSING` for that row (probe J,
   `probes/probe-J-ledger-evidence-after-committed-count-fix.txt`).
