# R50C2CritScope — critic, R50-C2 pointer surface (calibration)

REV: measured lane tip `c3372a9b24d3a200946a6b37dc0a31ed5c982cc1` (origin/master in my `--shared` clone);
measured tree `3b02d573d58cc6d2e0d27ef92ac0815354912252` (stage-1 freeze, HEAD of my clone);
before-state re-derived at `71f5f5f77591d8c3d19297ee9785436da45209e4`. Freeze ancestry verified first:
`git merge-base --is-ancestor 3b02d573… HEAD` → exit 0 (`FREEZE_IS_ANCESTOR_OK`).

Axes named: **calibration** (the only axis R50-C2 touches). I attacked the audit's *surface definition* on two
sides at once — pointers it misses (false negatives) and pointers it counts that are not lane artifacts
(false positives) — because a calibration predicate is only as good as its tokenizer.

---

## 0. Method (read-only, one `--shared` clone, no lane writes)

```
S=/fast/scratch/hyaku/kengaku-r50/R50C2CritScope
git clone --shared -q <lane> $S/lane && git -C $S/lane checkout -q 3b02d573…   # scratch clone only
python3 plans/round50_c2_audit.py --lane .            # in $S/lane  → the frozen command, verbatim
python3 probe.py  <dir> <label> <tree>                # wide path surface vs TOKEN
python3 probe2.py $S/lane                             # per-class quantification
git show c3372a9:{SCORECARD,SHONEN,PROVINCE}.md > $S/tipdir/*   # tip text, no checkout
```
`probe.py`/`probe2.py` are scratch-only; the corrected tokenizer is inlined in §5 so it is reproducible
without them. No production file, no `.ufo/state`, no sibling repo touched.

---

## 1. The frozen command, verbatim, on the freeze tree

```
$ python3 plans/round50_c2_audit.py --lane .
TIP c3372a9b24d3a200946a6b37dc0a31ed5c982cc1 branch=master
POINTERS total=275 paths=216 hashes=59 resolved=263 exists=204 superseded=0 never-landed=0 unresolved=12
UNRESOLVED corpus/defects.json
UNRESOLVED corpus/evidence/analyze.py
UNRESOLVED corpus/evidence/round9-replication/predictions-r9.sh
UNRESOLVED corpus/knowledge/repo-git-state.md
UNRESOLVED corpus/routed-findings.json
UNRESOLVED plans/round34_c1_verify.py
UNRESOLVED plans/round34_defects.py
UNRESOLVED plans/round34_mutate.py
UNRESOLVED plans/round48_c1_verify.py
UNRESOLVED plans/round48_c2_verify.py
UNRESOLVED plans/round49_c1_verify.py
UNRESOLVED plans/round49_c2_verify.py
EXIT=1
```
Note the `TIP` line already: the printed tip is `c3372a9` while the three files read are the `3b02d57` tree
(HEAD is detached at the freeze; the code takes `rev-parse --abbrev-ref origin/HEAD` → `master`). Latent, not
live: **0 of 59** hashes pass only because of `master` (all 59 are ancestors of both revisions), so no verdict
changes today — but a receipt that prints this `TIP` line names a revision it did not measure.

Before-state re-derived independently (`git show 71f5f5f:` + `git cat-file -e 71f5f5f:<p>`):

```
BEFORE@71f5f5f paths=213 hashes=58 total=271 unresolved=12
  plans=7 corpus=5
```

**Calibration defect in the frozen prose (F0).** `plans/round-50-claims.md` §C2 says the 12 are
"**six** pointers … counters … and **four** corpus paths" — that is 10, and the measured split is
**7 plans counters + 5 corpus paths**. Both numerals in the binding document are wrong about its own receipt.
The totals (`271/213/58/12`) are right; only the breakdown sentence is wrong. Cheapest correction: change
`six`→`seven`, `four`→`five` in the C2 prose (or restate as the measured split). This matters because every
seat is bound by that sentence.

---

## 2. F1 — the tokenizer fabricates 3 of the 12 "unresolved pointers" (decisive)

`EXTS` lists `json` before `jsonl`/`json5` and `sh` before nothing, and `TOKEN` has **no right boundary**.
The non-greedy `[A-Za-z0-9_./+-]*?` stops at the first alternation that matches, so a real extension is
truncated to a shorter listed one:

```
TOKEN on 'corpus/defects.jsonl'             -> 'corpus/defects.json'
TOKEN on 'corpus/routed-findings.jsonl'     -> 'corpus/routed-findings.json'
AUDIT-regex on '…/predictions-r9.sha256.repo' -> '…/predictions-r9.sh'
```

All ten `.jsonl` occurrences in the three files are truncated (`truncated=10/10`). The true paths exist at both
freeze and tip; the truncated ones never existed:

```
corpus/defects.jsonl               at_freeze=True  at_tip=True
corpus/routed-findings.jsonl       at_freeze=True  at_tip=True
corpus/defects.json                at_freeze=False at_tip=False
corpus/routed-findings.json        at_freeze=False at_tip=False
corpus/evidence/round9-replication/predictions-r9.sha256.repo  exists=True
```

So **3 of the 12 unresolved rows — `corpus/defects.json`, `corpus/routed-findings.json`,
`corpus/evidence/round9-replication/predictions-r9.sh` — are artifacts of the instrument, not lane defects**,
and the corresponding three correction rows in SCORECARD:

```
SUPERSEDED corpus/defects.json -> corpus/defects.jsonl
SUPERSEDED corpus/routed-findings.json -> corpus/routed-findings.jsonl
SUPERSEDED corpus/evidence/round9-replication/predictions-r9.sh -> corpus/evidence/round9-replication/predictions-r9.md
```
assert that the lane carried pointers it never carried. That is **false provenance manufactured by the counter
and blessed by the correction block** — the exact class calibration exists to prevent.

Worse on the third row: its own reason line says *"the round-9-prediction guard is `predictions-r9.sha256.repo`"*,
yet the target is `predictions-r9.md` — a **different artifact**. Both exist, so the row resolves; the kill rule
("a correction row whose target does not exist") cannot see a target that is merely the *wrong* file.

---

## 3. F2 — 2 more of the 12 are pointers that are not this lane's artifacts

| pointer | evidence | why it is not a lane defect |
|---|---|---|
| `corpus/knowledge/repo-git-state.md` | `PROVINCE.md:415` — "**Kasegi's** `corpus/knowledge/repo-git-state.md` is cited as the sibling precedent" | cross-repo citation; the audit reads it as a lane pointer and the correction row asserts `never-landed` for a path this lane was never supposed to hold |
| `corpus/evidence/analyze.py` | `SCORECARD.md:113` — "`test -e` → absent; the analyzer on disk is `corpus/evidence/round9-fleet/analyze.py`" | the file *documents an absence*. A self-assessment that honestly records a missing path is counted as an unresolved pointer and "corrected" |

So **5 of 12 unresolved (42 %) are not lane defects** (3 tokenizer phantoms + 1 cross-repo + 1 documented
absence). The genuine set is **7** — exactly the seven promised counters (`round34`×3, `round48`×2, `round49`×2),
which is the defect the claim was written to catch and does catch.

---

## 4. F3 — what the surface misses, quantified per shape

Wide surface over the three files: 1022 unique path-like tokens (SCORECARD 1318 occurrences, PROVINCE 328,
SHONEN 1). Audit-matched: **412 occurrences → 216 unique** (plans 249 occ, corpus 163 occ).

| shape | count | verdict |
|---|---|---|
| `.ufo/` pointers (lane receipts, the lane's largest evidence tree) | **88 occurrences, 82 unique; 70 file-shaped, 63 exist, 7 absent** | **invisible to the audit.** The 7 absent all have `git log --all -- <p>` = 0 rows, i.e. never-landed promised artifacts: `.ufo/l0-questions.md`, `.ufo/evidence/round-18/defect-probes.py`, `.ufo/waves/round-20/isolate.sh`, `.ufo/waves/round-31/count-c2-a1.py`, `.ufo/waves/round-36/sealed_count_v2.py`, `.ufo/waves/round-42/c42_count.py`, `.ufo/waves/round-57/c57_idresolver_gate.py`. This is *the same defect class the claim corrects*, 7 times, outside the surface. |
| extensions absent from `EXTS` (live, existing) | 3 unique | `corpus/evidence/attrib-r23-stream.log` (exists), `corpus/evidence/round9-replication/predictions-r9.sha256.repo` (exists), `…/round10-fleet/final-harness.log` (exists, via brace) — real artifacts never counted. The audit sees the *nonexistent* `.sh` sibling and misses the *existing* `.repo` on the same SCORECARD row (`SCORECARD.md:97`). |
| brace groups | 9 groups; **5 members missing on disk** | members are invisible (no `plans/`/`corpus/` prefix inside `{…}`); e.g. `corpus/evidence/round14-fleet/{r14-critic-landed,r14-review-priorart,r14-landing-gate}` → 3/3 absent, undetected |
| star globs | 8 | `plans/battery37|42|43|44/*.py` expand (9/5/7/10), `corpus/knowledge/*.md` → 53 — never expanded, so a vanished battery member is invisible |
| directories (no extension) | 18 (`plans/battery42`, `corpus/evidence/round8-horizon`, …) | all exist today; skipped by construction |
| `considerthese/` | 2 unique, **both exist** (`2026-10-25.md`, `2026-10-26.md`) | real lane artifacts (assimilation proposals), never counted |
| `scripts/`, `merge/` | 6 + 1 unique, **0 exist in the lane** | cross-root pointers the claim's sentence ("every artifact pointer") would flag, the surface cannot |
| `~/` | 26 unique (62 occ) | host paths cited as evidence sources; out of surface by design |
| `..`-relative into plans/corpus | **0 live** | latent only: `(?<![\w/.-])` silently drops `../corpus/x.md`; the 6 live lookbehind misses are all cross-repo (`kagi-shokunin/`, `mado-shokunin/`, `kumitate-shokunin/`, `kotodama-shokunin/`) and correctly out of scope |
| JSON-embedded paths | **0 fenced ```` ```json ```` blocks; 2 prose-quoted spans** | class absent in these three files |
| example/placeholder paths in prose | **0** (`plans/foo`, `plans/example`, `plans/your` → 0) | class absent |
| PROVINCE table cells | 65 table rows, 13 pointer occurrences, 11 unique, **0 unresolved** | tables are line-agnostic to the regex; nothing missed here |
| `path:NN` line anchors | 14 unique | 13 land on a non-blank line; the 14th is `mado-shokunin/corpus/lessons/round-15.md:39` (cross-repo, correctly out of surface). Line *numbers* are never validated — a drifting anchor passes. |
| short hashes 7–12 hex | **111 unique, 35 not git objects** | outside the hash leg entirely (only 40-hex is checked). Mostly content digests/dates (`20251031`, `1234567`, md5 prefixes like `029c3bcd…`, `42d86d99…15a386`), but ≥3 are asserted *revisions* (`22b7779e…`, `2fd12b88`, `11bb2cad…`) that do not resolve as objects. |
| 64-hex digests | **0** in the three files | tested, absent — so the audit's blindness to sha256 pins is currently harmless here, but the round's own identity pins (see §6) live only in the claims file and no C2 leg can see drift in them |

---

## 5. F4 — the correction mechanism admits fabrication (authority is unscoped)

`superseded_map()` regex-scans **all of SCORECARD.md**, not the `## Round 50 — C2 corrections` block, and a
target-mapped row has no identity check. Demonstrated on a scratch symlink farm holding the tip files
(`audit(..., check_hashes=False)`, path leg only):

```
[baseline tip files, no history]                                   rc=0 unresolved=0
[+ SUPERSEDED plans/fabricated_never_existed.py -> never-landed]   rc=0 unresolved=0  total 277→278, never-landed 9→10
[+ SUPERSEDED plans/fabricated_never_existed.py -> corpus/defects.jsonl]  rc=0 unresolved=0  superseded 3→4
[+ SUPERSEDED plans/ghost_counter.py -> never-landed in prose above the block] rc=0 unresolved=0
```
A path that never existed, and a `SUPERSEDED` line placed anywhere in the file (including prose quoting the
rule), both satisfy the predicate. The kill rule catches `never-landed`-for-a-path-in-history only; it does not
catch *invented sources* or *wrong targets*. Also: the same farm shows the whole path leg is green in a repo
with **no history at all** (all `never-landed` rows pass vacuously) — a shallow or single-ref clone makes the
`never-landed` evidence unfalsifiable. The scored receipt must therefore state the clone is full-history.

**F5 — the correction block is its own source of 3 pointers (measured, not inferred).** Because `scan()` reads
the whole SCORECARD text, a `SUPERSEDED <src> -> <target>` row injects `<src>` into the pointer set and resolves
it in the same line. So the phantom rows do **not** become dead once the tokenizer is fixed — I first assumed
they would and the measurement refuted it (`dead correction rows: []`). The principled split — scan the
self-assessment text *before* the corrections block and use the block only as resolution data — gives, on the
tip files at `c3372a9`:

```
pre-correction text + corrected regex: paths=217 unresolved=0
correction rows whose source is NOT in the pre-correction pointer set:
  ['corpus/defects.json', 'corpus/evidence/round9-replication/predictions-r9.sh', 'corpus/routed-findings.json']
correction rows whose source IS in the pre-correction set: 9
  ['corpus/evidence/analyze.py', 'corpus/knowledge/repo-git-state.md', 'plans/round34_c1_verify.py',
   'plans/round34_defects.py', 'plans/round34_mutate.py', 'plans/round48_c1_verify.py',
   'plans/round48_c2_verify.py', 'plans/round49_c1_verify.py', 'plans/round49_c2_verify.py']
```
Exactly the 3 tokenizer phantoms are self-sourced; the other 9 rows correct pointers the files really carry.
The predicate is green either way (`unresolved=0`), so the defect is not a false red — it is 3 rows of
**false provenance in a document whose axis is calibration**.

---

## 6. What survives, and the smallest safe correction

Corrected tokenizer (order matters + right boundary + the two live extensions):

```python
EXTS = ("md","py","jsonl","json5","json","txt","patch","whl","sh","tres","repo","log")
TOKEN = re.compile(r"(?<![\w/.-])((?:plans|corpus)/[A-Za-z0-9_][A-Za-z0-9_./+-]*?\.(?:"
                   + "|".join(EXTS) + r"))(?![A-Za-z0-9])")
```
Measured effect, same three files (freeze tree):

```
audit paths=216  corrected paths=217
only-in-audit (fabricated by truncation):  corpus/defects.json, corpus/evidence/round9-replication/predictions-r9.sh, corpus/routed-findings.json
only-in-corrected (hidden real pointers):  corpus/defects.jsonl, corpus/evidence/attrib-r23-stream.log,
                                           corpus/evidence/round9-replication/predictions-r9.sha256.repo,
                                           corpus/routed-findings.jsonl
@3b02d57: audit_unresolved=12  corrected_unresolved=9
```
The 9 corrected-unresolved at the freeze tree are exactly the 9 existing `never-landed` rows. On the **tip files
themselves** (`c3372a9`, corrections block used only as resolution data): `paths=217 unresolved=0`. So **the C2
predicate still holds under the correction** — this is a fixable defect, not a redesign. The three phantom rows
must be withdrawn by an append-only note (they cannot be deleted; see F5: they are self-sourcing) and the
pointer scan must exclude the corrections block.

Smallest safe correction set, in order:
1. `plans/round50_c2_audit.py`: reorder `EXTS` (`jsonl|json5` before `json`, add `repo`,`log`), append
   `(?![A-Za-z0-9])` to `TOKEN`. → 3 phantoms gone, 4 real pointers recovered, freeze unresolved 12→9.
2. Scan pointers over the self-assessment text **with the `## Round 50 — C2 corrections` block removed**, and
   parse the block only as resolution data. → the 3 self-sourced rows become provably dead (F5) instead of
   silently self-justifying.
3. Append-only withdrawal note for the 3 phantom rows; if `predictions-r9.sh` is kept at all its target must be
   `predictions-r9.sha256.repo`, not `predictions-r9.md` (wrong artifact, §2).
4. Reclassify `corpus/knowledge/repo-git-state.md` (cross-repo) and `corpus/evidence/analyze.py` (documented
   absence) — they are not `never-landed` lane pointers; a `SUPERSEDED … -> never-landed` row for them is a
   false statement even though `git log --all` is empty.
5. Scope `SUPERSEDED` parsing to the corrections block (line-anchored to the block, not the whole file).
6. Hash leg: use the revision actually read (`HEAD` / `rev-parse HEAD`), not `origin/HEAD`→`master`.
7. Fix the claims-file numerals (F0: seven/five).
8. *Frontier, not minimal:* extend the surface to `.ufo/` (70 file-shaped pointers, 7 broken) and expand brace
   groups — that is where the same defect class still hides, and it is a surface widening, not a repair.

Identity pins check out (so the C1 side of calibration is not damaged by my findings): at `c3372a9`
`round50_c1_verify.py` = `d8787b34…` (the open-window table's new digest), `population.txt` = `b5197f94…`,
`build_honest_population.py` = `35e3de60…`, `fixture_fence.py` = `05d5fe03…`, `c1-mutants.json` = `2e5cfe66…`
— all five match the frozen text. `plans/sealed50/` and `corpus/evidence/round50/c1-receipt.txt` are absent at
tip (C1 S2/S3 open-window items, outside my axis; noted only so the round does not read C2's green as C1's).

---

## Limits

- I ran the frozen command only on the freeze tree of my clone (exit 1, 12 unresolved). The tip path leg was
  measured directly on the tip files without a checkout — audit `TOKEN` + tip existence + the real
  `SUPERSEDED` map + `git log --all` in my full-history clone → `paths=218 unresolved=[]`; the corrected
  tokenizer over the pre-correction text → `paths=217 unresolved=0`. The farm run corroborates the path leg
  (`resolved=218 … unresolved=0`) but its hash leg cannot run (fresh `git init`, no objects), so the tip
  `unresolved=0` line rests on the direct path-leg measurement, not on a farm exit code. The integrator's S3
  receipt remains the authority for the tip run.
- Tokenizer counts are over the three `FILES` only; the claims file, `.ufo/` receipts and sibling repos were
  scanned for context but are outside the frozen surface by definition.
- Short-hash classification (`≥3 asserted revisions`) is a context heuristic over the citing line; the hard
  numbers are `111 unique / 35 not objects`.
- No claim of R50-C1 or R50-C2 admission. I did not run `--selftest` (the integrator's receipt covers it);
  the self-test cannot catch any defect in §2–§5 because it only appends a bogus `plans/…py` pointer.

Scratch removed: `/fast/scratch/hyaku/kengaku-r50/R50C2CritScope` deleted before yield; all cited numbers are
reproduced in this report, so no `/tmp` or scratch path is load-bearing.

VERDICT: **defect — fixable, not admissible as landed.** R50-C2's `unresolved=0` is reachable today, but 3 of
its 12 rows were fabricated by its own tokenizer (`.jsonl`→`.json`, `.sha256.repo`→`.sh`), 2 more are not lane
pointers (cross-repo citation, documented absence), 3 correction rows therefore assert provenance the lane never
had, one of them targets the wrong artifact, and the surface is blind to 70 `.ufo/` pointers of which 7 are
broken — the very defect class the claim exists to fix. Calibration axis is harmed, not merely unimproved:
a self-assessment that invents 3 of its own defects and "corrects" them is a false-provenance artifact. The
claim survives correction §6.1–§6.7 with no predicate change (`unresolved=0` at tip, 9 real rows), so the fix is
a tokenizer repair plus an append-only withdrawal note before the scored run — not a redesign.
