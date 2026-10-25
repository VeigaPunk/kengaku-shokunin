# Probe C — late rule integration (round-8 evidence, analyzed in round 9)

## 0. Scope, provenance, and what n=4 buys

| item | value |
|---|---|
| data analyzed | `/tmp/bench-r8/results.jsonl` (268 lines, md5 `df154cb524bf210782fb0f4a46fd1bdc`), C cells = 16 records |
| probe source | `corpus/evidence/round8-horizon/horizon.py` (349 lines; probe C = lines 225–300, grader 270–289) |
| run log | `/tmp/bench-r8/run.log`, C jobs = plan positions 63–78 of 78 (`horizon.py:320-321`), SUMMARY C-conflict 4/4, C-benign 1/4, C-norule 4/4, C-MONO 4/4 — matches OK counts recomputed from the JSONL |
| n | 4 reps/cell by construction (`NREP_C = 4`, `horizon.py:304`) |

**n = 4 per cell supports description only. No p-values are computed or reported anywhere in this file** —
both because the assigned n forbids them and because this endpoint's draws are established non-iid
(lane prior art: lag-1 autocorr +0.26/+0.32, 5–10-request burst horizon, near-deterministic same-seed replays).

**Effective-n warning (reduces every "x/4" below):** the 4 reps are largely the *same string* replayed.

| cell | distinct `raw` of 4 | distinct `got` | completion tokens | prompt tokens |
|---|---|---|---|---|
| C-conflict | **1** | 1 | 64,64,64,64 | 296 |
| C-benign | **2** | 2 | 64,67,67,67 | 296 |
| C-norule | **1** | 1 | 62,62,62,62 | 238 |
| C-MONO | **1** | 1 | 59,59,59,59 | 78 |

So "conflict 4/4" = one distinct response seen four times; "benign 1/4" = two distinct responses
(rep0 vs reps1–3 byte-identical). Cell-level inference here is n≈1–2 distinct generations.

**Provenance divergence (finding for L1):** the two copies are **not** byte-identical, contrary to the brief's
expectation. `md5 df154cb5…` (/tmp, 125,577 B) vs `md5 01547cfa…` (repo, 97,023 B); the repo copy is exactly
the /tmp copy with the `raw` key removed from all 268 records (verified: for every pair, `{k:v for k,v in A[i].items() if k!='raw'} == B[i]`; 0 mismatches). All graded fields (`ok`, `got`, `finish`, `usage`, `wall_s`) are identical, so nothing in this analysis depends on the choice — but free-text re-grading is impossible from the landed copy, and `/tmp` is ephemeral. Land `raw` or re-run.

## 1. Per-cell table (16 records; `n/a` = key absent by construction)

| cell | rule added | ok | viol_ok | square_valid | preserved | over_repair | parse | finish | wall_s (rep0..3) | completion tokens |
|---|---|---|---|---|---|---|---|---|---|---|
| C-conflict | binding (rows 1–3 not col-complete) | **4/4** | 4/4 | 4/4 | 4/4 | 0/4 | 4/4 | stop×4 | 0.50, 0.41, 0.41, 0.41 | 64×4 |
| C-benign | vacuous (rows 1–3 already col-complete) | **1/4** | 4/4 | 1/4 | 4/4* | **4/4** | 4/4 | stop×4 | 0.47, 0.49, 0.49, 0.49 | 64,67,67,67 |
| C-norule | none (same transcript, "emit row 4") | **4/4** | 4/4 | 4/4 | 4/4 | 0/4 | 4/4 | stop×4 | 0.44, 0.43, 0.43, 0.44 | 62×4 |
| C-MONO | none, one-shot "emit a Latin square" | **4/4** | n/a | 4/4 | n/a | n/a | n/a | stop×4 | 0.40, 0.37, 0.37, 0.37 | 59×4 |

\* `preserved` is **vacuous** for benign reps 1–3: `kept_ok` only inspects rows 1–3 that are *not* declared
changed (`horizon.py:277-279`), and those reps declared `[2,3]`, so only row 1 was checked. Rows 2 and 3 were in
fact rewritten. Treat the 4/4 as uninformative, not as evidence of preservation. `parse`/`viol_ok`/`preserved`
are absent for C-MONO because `run_c_mono` uses a different log schema (`horizon.py:291-299`) — not a defect.

Task semantics (verified offline, §4): CONFLICT_ROWS minimal removal = **{3}** (size 1, unique);
BENIGN_ROWS minimal removal = **{}** (size 0); BENIGN's forced row 4 = `[D,C,B,A]`, which is a permutation,
so a **zero-change** answer exists and is valid.

## 2. C-benign failure modes, per rep (raw outputs)

Prior fabricated rows (all three cells share the transcript): `ABCD`, `BADC`, `CDAB` — column distinct counts
[3,3,3,3], i.e. already col-complete; correct answer is `violations: []`, `square: [[ABCD],[BADC],[CDAB],[DCBA]]`.
C-norule produced exactly that, byte-identically, 4/4.

| rep | declared `violations` | emitted `square` | row-perm valid | col dup | square_valid | shipped `ok` | failure mode |
|---|---|---|---|---|---|---|---|
| 0 | `[3]` (correct: `[]`) | `ABCD / BADC / DCBA / CDAB` | T,T,T,T | none | true | true | **wrong violations list = over-repair** (rows 3↔4 swapped); square is a valid Latin square, so the shipped grader passes it — `over_repair=true` is the only flag |
| 1 | `[2,3]` | `ABCD / CABD / BDAC / DCDA` | T,T,T,**F** | col4 `D`×2 | false | false | **over-repair + invalid square**: row 4 has duplicate `D`, no `B`; rows 2 and 3 rewritten although both were conflict-free |
| 2 | `[2,3]` | identical to rep 1 | T,T,T,F | col4 `D`×2 | false | false | same as rep 1 (byte-identical replay) |
| 3 | `[2,3]` | identical to rep 1 | T,T,T,F | col4 `D`×2 | false | false | same as rep 1 (byte-identical replay) |

Failure-mode census over the 4 benign reps: wrong `violations`/over-repair **4/4**; invalid square **3/4**;
non-preserved rows **0/4** (vacuous, see §1); format/parse failure **0/4**. Mechanism visible in rep0/rep0-vs-reps1-3:
the model treats the new rule as a mandate to *patch* — swap a row (rep0) or rewrite two rows then fill the last
without re-validating it (reps 1–3).
Under a **strict** criterion (violations `== []` **and** rows 1–3 untouched **and** valid Latin), benign is **0/4**
(recomputed in the appendix: `strict=False` for all four). Report both numbers: shipped-`ok` 1/4, strict 0/4.

## 3. Attribution: rule-integration cost, not transcript-shape cost

Two prompt-level facts, both verified by rebuilding `run_c`'s message lists offline from the source strings
(`probeC_prompt_check.py` output quoted in §4):

| contrast pair | shared | differs |
|---|---|---|
| C-benign vs C-conflict | message 0 identical; final ask **byte-identical** (476 chars, ORDER_NOTE + re-check directive + fillable `violations` slot); prompt_tokens 296 = 296 | only the 3 fabricated assistant row payloads (msg indices 4, 6), i.e. `BADC`/`CDAB` vs `BCDA`/`ABDC` |
| C-benign vs C-norule | same fabricated transcript, same response *shape* (`{"violations":[], "square":[…4 rows…]}`) | the whole with_rule apparatus (rule sentence, "Re-check the rows already emitted", ORDER_NOTE, slot vs `[]` literal); 476 vs 173 chars |

Decision: **'rule-integration cost'**, with 'transcript-shape cost' excluded.

- Transcript-shape cost ≈ 0: C-norule reads the identical transcript, must still compute the forced row 4, and
  returns the canonical zero-change square 4/4 (one distinct string). C-MONO 4/4 confirms Latin-square ability
  is not the limit.
- The re-check directive / ORDER_NOTE / slot-template confound is **held constant** between benign and conflict,
  and conflict is 4/4 — so the with_rule scaffolding is not the failure source; only the transcript state differs.
- **Interpretation (sharpest C finding):** on this endpoint the model can integrate a **binding** new constraint —
  it isolates the offending row, declares `violations:[3]`, and emits a valid Latin square preserving rows 1–2
  (4/4, one distinct answer) — but cannot represent that a **vacuous** new constraint requires nothing: it
  manufactures violations 4/4 times and corrupts the square 3/4 times. Over-application of a satisfied constraint,
  not rule-blindness. `viol_ok` is 4/4 in *both* with_rule cells, so shipped `ok` conflates "answered consistently"
  with "answered correctly"; `over_repair` is the discriminating field.
- Not excluded by this design: rep0's output is a *valid* Latin square with only a mislabeled violation set, which is
  also consistent with "cheapest repair workflow + buggy bookkeeping" rather than a reasoning failure. Distinguishing
  probe: benign transcript with an explicit "if no row needs to change, reply `violations: []`" hint (mirrors the
  B-probe `hint` condition), or a benign transcript where changing any row destroys a valid completion.

## 4. Grader-convention check (critic defect #9)

| check | result | source |
|---|---|---|
| ORDER_NOTE defined once, interpolated only in the with_rule ask | `ORDER_NOTE` at `horizon.py:243-244`, concatenated at `horizon.py:254`; absent from the norule ask (`horizon.py:258-260`) | grep of 226–289 + offline rebuild: `ORDER_NOTE in with_rule ask = True`, `in norule ask = False` |
| conflict vs benign ask identical | True (476 chars both); differing msg indices `[4, 6]` | `probeC_prompt_check.py` |
| minimal-removal logic yields {3} for CONFLICT_ROWS | **size 1, sets=[{3}]** (unique); keep-all-3 `col_conflict_free=False`, col distinct counts [2,2,2,3] | `probeC_grader_check.py` (logic copied from `horizon.py:284-286`) |
| minimal-removal logic yields {} for BENIGN_ROWS | **size 0, sets=[{}]**; keep-all-3 `col_conflict_free=True`, col distinct counts [3,3,3,3]; forced row 4 `[D,C,B,A]` is a permutation | same |
| does benign `viol_ok` demand `violations == []`? | **No.** `viol_ok(violations=[]) = True`, and also `True` for `[2]`, `[3]`, `[2,3]`, `[1,2,3]`, and even `[99]`. `viol_ok` only requires (`horizon.py:281-282`) that the *kept* rows remain col-conflict-free **and** that undeclared rows 1–3 match the prior rows; declared rows are exempt from both checks. `over_repair` (`:287`) is computed only when `viol_ok` is true and only compares `len(changed)` to the minimal size — it never checks that declared violations actually conflict. | appendix |
| conflict side behaves as intended | `viol_ok([]) = False`, `viol_ok([3]) = True` — the conflict rule does force removal of row 3 | appendix |

Consequence for the headline: the grader's `ok` is a *consistency* metric, not a correctness metric, in the with_rule
cells. Benign 1/4 means "1/4 emitted internally consistent answers", and that single answer (rep0) is itself an
over-repair. The 3/4 failures are genuine model errors (invalid square), so the headline direction is unaffected;
the *magnitude* should be quoted as strict 0/4, not 1/4.

## 5. Harness-artifact flags for probe C

| class | count in C | verdict |
|---|---|---|
| `finish == "length"` | **0** of 16 (all `stop`) | the known round-8 `finish=length` defect family does **not** touch C |
| `parse == false` | **0** of 12 dict-schema records (C-MONO has no `parse` key) | no parse/extraction failures recorded |
| malformed `square` (dup symbol / non-permutation row) | 3 (benign reps 1–3) | **model** artifact, not harness: the fenced JSON was extracted and parsed successfully and the grader scored it as `square_valid=false` |
| `wall_s` outliers | none: C range 0.37–0.50 s | C jobs ran in 0.37–0.50 s, no timeout/retry signature |

Also worth flagging as design artifacts (not defects, but limits on what C can conclude):
(i) `square_valid` is graded by `valid_latin` for **all four** rows, but `preserved`/`kept_ok` only ever inspects
rows 1–3 (`horizon.py:278`) — a rewritten row 4 is never flagged; (ii) C records carry no `want` field, so the
corrected square is checked structurally, not against a canonical completion; both conflict and benign therefore
admit many "correct" squares; (iii) the C block is the last 16 of 78 jobs and the intra-block order is fixed
(conflict, benign, norule, MONO for every rep, `horizon.py:320-321`) — not order-counterbalanced. Position cannot
explain the benign dip (positions 1 and 3 score 4/4 while position 2 scores 1/4), but benign is *always* the job
immediately following conflict, so burst-state adjacency is unexcluded.

## 6. Re-verify commands (L1)

```
python3 /tmp/kengaku-r9/probeC_grader_check.py    # rows + minimal removals + per-rep grades (18 lines out)
python3 /tmp/kengaku-r9/probeC_prompt_check.py    # ask/ORDER_NOTE identity + differing msg indices
md5sum /tmp/bench-r8/results.jsonl corpus/evidence/round8-horizon/results.jsonl   # 268-line divergence check
wc -l /tmp/bench-r8/run.log                        # 91 lines, SUMMARY block
```

## Appendix — `/tmp/kengaku-r9/probeC_grader_check.py` (38 lines, import-free)

```python
import itertools, json
CONFLICT_ROWS = [["A","B","C","D"], ["B","C","D","A"], ["A","B","D","C"]]   # h.py:226
BENIGN_ROWS   = [["A","B","C","D"], ["B","A","D","C"], ["C","D","A","B"]]   # h.py:227
SYM = {"A","B","C","D"}
def col_conflict_free(rows):                       # h.py:229-230
    return all(len(set(r[c] for r in rows)) == len(rows) for c in range(4))
def valid_latin(sq):                               # h.py:232-236
    if not isinstance(sq, list) or len(sq) != 4: return False
    if not all(isinstance(r, list) and len(r) == 4 and set(r) == SYM for r in sq): return False
    return all(set(sq[r][c] for r in range(4)) == SYM for c in range(4))
def minimal_removal(prior):                        # h.py:284-286, over prior_rows[0:3]
    sz = next((sz for sz in range(4)
               if any(col_conflict_free([prior[i] for i in range(3) if i not in c])
                      for c in itertools.combinations(range(3), sz))), None)
    return sz, sorted(set(i+1 for i in c) for c in itertools.combinations(range(3), sz)
                      if col_conflict_free([prior[i] for i in range(3) if i not in c]))
def viol_ok(viol, sq, prior):                      # h.py:277-282 (with_rule=True path)
    changed = set(viol)
    kept = all(sq[i] == prior[i] for i in range(3) if (i+1) not in changed)
    return kept and col_conflict_free([prior[i] for i in range(3) if (i+1) not in changed])

for name, prior in [("CONFLICT_ROWS", CONFLICT_ROWS), ("BENIGN_ROWS", BENIGN_ROWS)]:
    sz, sets = minimal_removal(prior)
    print(f"{name}: min-removal size={sz} sets={sets} col_distinct_counts={[len(set(r[c] for r in prior)) for c in range(4)]}")
print("BENIGN forced row 4:", [next(s for s in "ABCD" if s not in [r[c] for r in BENIGN_ROWS]) for c in range(4)])
for v in ([], [2], [3], [2, 3], [1, 2, 3], [99]):
    print(f"  BENIGN viol_ok(violations={v!s:<9}) = {viol_ok(v, BENIGN_ROWS + [list('DCBA')], BENIGN_ROWS)}")
print("  CONFLICT viol_ok([]) =", viol_ok([], CONFLICT_ROWS, CONFLICT_ROWS),
      "| viol_ok([3]) =", viol_ok([3], CONFLICT_ROWS, CONFLICT_ROWS))

for r in (json.loads(l) for l in open("/tmp/bench-r8/results.jsonl")):
    if r["cell"] in ("C-conflict", "C-benign"):
        q, c = r["got"]["square"], range(4)
        strict = None if r["cell"] == "C-conflict" else (r["got"]["violations"] == []
                 and q[:3] == BENIGN_ROWS and valid_latin(q))
        print(f"{r['cell']} rep{r['rep']}: ok={r['ok']} over_repair={r['over_repair']} sq_valid={r['square_valid']} "
              f"viol={r['got']['violations']} rowperm={[set(x)==SYM for x in q]} "
              f"coldup={[[s for s in 'ABCD' if [x[j] for x in q].count(s)>1] for j in c]} strict={strict}")
```

## Confidence

| claim | grade | reason |
|---|---|---|
| Per-cell counts (conflict 4/4, benign 1/4, norule 4/4, MONO 4/4; viol_ok 4/4 in both with_rule cells; over_repair 4/4 benign) | **high** | direct recomputation over all 16 C records; OK totals reproduce `run.log` SUMMARY exactly |
| Effective-n reduction (distinct raw: conflict 1, benign 2, norule 1, MONO 1) | **high** | byte-equality count over recorded `raw` fields |
| Benign failure modes (rep0 over-repair with valid square; reps 1–3 invalid row 4 `DCDA` + col-4 `D` duplicate) | **high** | recomputed row-permutation and column-duplicate structure from `got`; raw strings quoted verbatim |
| Grader conventions: ORDER_NOTE present only in with_rule ask; minimal removals {3}/{ }; benign `viol_ok` true even for `[]`/`[99]`, so it does not demand `violations == []` | **high** | logic copied from `horizon.py:226-230,270-289` and re-run offline; prompt identity confirmed by offline message reconstruction |
| Attribution to 'rule-integration cost', transcript-shape cost ≈0 | **medium** | benign-vs-conflict share a byte-identical ask, which rules out the with_rule scaffolding, but effective n is 1–2 distinct generations, a single fabricated transcript per cell, and no isolation cell for the "hit rate under a satisfied constraint" question |
| Sharp claim: cannot integrate a vacuous constraint without over-applying it | **medium** | direction is consistent across all 4 benign reps (strict 0/4) and two independent rule-free controls are clean; not downgraded to low because the failing behaviour is reproducible and the controls are clean, not upgraded because "cheap-repair + bad bookkeeping" (rep0) is an unexcluded alternative explanation |
| No C record with `finish=="length"` or `parse==false` | **high** | full scan of the 16 C records; C-MONO's missing `parse` key is by construction (`horizon.py:297-299`) |
| Two copies diverge (repo copy == /tmp copy minus `raw`) | **high** | field-by-field comparison of all 268 records, 0 mismatches; md5 and byte sizes recorded |