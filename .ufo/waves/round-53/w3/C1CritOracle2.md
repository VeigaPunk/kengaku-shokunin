# C1CritOracle2 — round 53 wave 3, critic seat

**Target.** The 305/305 oracle agreement of R53-C1 (`plans/round-53-c1_triage.py`, leg 2 FREEZE+ORACLE).
**Lane tip I ran at.** `9ead4476bf55b1ea6490d0204b668195db4a4d1d` (the lane advanced from the build-time tip
`b1f79a54…` while I worked; every command below was re-run on the fresh tip).
**Scratch.** `/fast/scratch/hyaku/kengaku-r53/C1CritOracle2/` (removed at exit). Lane tree never mutated; the only
lane writes are this report and this seat's own directory.

## Verdict

**The oracle's *content* survives; the oracle's *integrity guarantee* does not.**

The 305/305 agreement is real and reproducible: I recomputed the whole merge from the eight committed label files and
the frozen shards and got `decided=305 contested=0 oracle_Y=52 oracle_N=253 disagree=0 per_label_agree=1.000`,
byte-identical to the committed receipt `.ufo/waves/round-53/claims/c1-after-oracle.txt`. My own hand re-read of 20
sampled tests (10 Y, 10 N) agreed with the oracle on 20/20; my hand re-read of all 52 Y bodies found no Y that is not
presence-only; the 23 control disagreements all point the way the claim needs (the round-52 classifier was too
*permissive* on 2 and too *strict* on 21 — the disagreement is directional, not noise). Nothing in the label corpus
shows the systematic misreading that perfect agreement usually hides: `U` was never used, `contested=0`, and the eight
seats wrote 602 distinct `why` strings over 610 labels (0 of 305 tests have both seats writing the same `why` text).

**But the FREEZE leg — the mechanism that is supposed to make the agreement meaningful — is forgeable.** I built a
forged lane (a *coordinated history rewrite*, not a file edit) in which the classifier, the eight label files and the
freeze file are mutually consistent lies, and the counter printed:

```
FREEZE clean=yes classifier_and_freeze_one_commit=yes classifier_sha=ok label_files_pinned=ok
      shards_pinned=ok labels_after_freeze_and_untouched=yes authors=4
ORACLE tests=305 bad_label_files=0 bad_label_rows=0 decided=305 contested=0 oracle_Y=42 oracle_N=263 v2_P1=42
      unclassified=0 disagree=0 limit=9.2 per_label_agree=1.000 (min 0.9)
ORACLE-CONTROL r52_classifier_disagree=29 all_P0_disagree=42 control_ok=yes
CONFIRM candidates_never_read=27 new_confirmed=20 rejected=0 target>=3
```

Ten of the oracle's 52 `Y` labels were flipped to `N` (both seats of each pair, so `contested` stays 0 and the merge
stays clean), the classifier was replaced by a table keyed on `sha256(source)`, and every digest was re-pinned
consistently. **Four of the five legs went green on forged labels.** This is the "counter-reachable-without-the-work"
failure the round's own A1 amendment was written to close, re-appearing one level up: A1 pinned the *inputs* by digest
but left the *pins themselves* inside a file that the same forgery can rewrite.

The single root cause: **the digests that make the FREEZE leg meaningful live in a file that the FREEZE leg does not
pin.** `plans/round53-c1-freeze.json` pins the classifier, the eight label files and the eight shards — but nothing
outside the rewriteable tree pins the freeze file, the classifier's digest, or the counter's own digest. The frozen
claims file (`plans/round-53-claims.md`) pins the four *population* digests as literals
(`0230b68c…`, `96b47248…`, `579d567f…`, `0b1d4213…` — `grep -c` = 1 each) but pins **no** classifier digest
(`grep -c 935db122 plans/round-53-claims.md` = **0**), **no** label digest (`32a1b20b` = 0), **no** freeze-file digest
(`6343e0db` = 0) and **no** counter digest (`d36e31f9` = 0). The counter's own `--selftest` tripwire
(`plans/round53_c1_triage.py:504-515`) checks that its *population* constants equal the frozen literals — it never
checks a classifier or label constant, because there is none.

## What would falsify the oracle (and what did)

| attack | result | evidence |
|---|---|---|
| recompute the merge from the committed files | **survives** — `disagree=0`, `contested=0`, `per_label_agree=1.000` | `oracle-recomputed.json` |
| hand re-read of 10 Y + 10 N sampled tests | **survives** — my labels == oracle's on 20/20 | `samples-20.json`, `all-52-Y-bodies.txt` |
| hand re-read of all 52 Y bodies | **survives** — every Y asserts only existence/type of a path | `all-52-Y-bodies.txt` |
| control direction on all 23 r52 disagreements | **survives** — 21 are r52-too-strict, 2 r52-too-permissive; v2 agrees with the oracle on every one | §3 |
| alt-classifier cross-check | **survives** — the independent implementation `C1ExecClassifierAlt` (53 P1 / 252 P0) differs from v2 on exactly 1 of 305 (`financial-document-processor::test_original_documents_dir_empty`, alt=P1, v2=P0) — and the oracle sides with v2 (N) on that id | §2.4 |
| spec-ambiguity sweep over the whole 305 | **survives** — 0 env-gated tests, 0 tests where a `U` is warranted by an uncaptured local helper, 1 listing-count case (`test_original_documents_dir_empty`, correctly N), 4 listing-truthiness cases (correctly Y) | §2.1–2.3 |
| **coordinated history rewrite of freeze+classifier+labels** | **LANDS** — FREEZE green, ORACLE `disagree=0` on 42 forged labels, CONFIRM `new_confirmed=20 rejected=0` | §4 |
| file-level edits after the freeze (the selftest routes) | **rejected** — `label_files_pinned=BAD`, `labels_after_freeze_and_untouched=NO` | §4.2 |
| merge-commit edit after the freeze | **rejected** — `classifier_and_freeze_one_commit=NO`, `labels_after_freeze_and_untouched=NO` | §4.2 |

## 1. Angle (1) — spec ambiguity: clauses two careful readers could score differently

The frozen definition is `.ufo/waves/round-53/p1-spec.md` (committed at `1373b6ca`, unchanged since). I read it in
full and enumerated every clause whose outcome depends on a judgment call, then measured the population against each.

**1.1 — Clause 2's "existence or type of a path" vs. the operational gloss.** Clause 2 admits
`.exists()/.is_file()/.is_dir()/.is_symlink()`, `os.path.exists/isfile/isdir/islink`, `os.access(p, os.F_OK)` and
"*membership of a **name** in a directory listing* (`"x" in os.listdir(d)`, `{p.name for p in d.iterdir()}`, `glob`
non-empty)". The gloss says "creating the named files and directories (touch, mkdir, an empty file) would satisfy every
assertion the test can reach". A careful reader can read these two sentences differently for a test that asserts
**negated** existence: clause 2's list explicitly permits `not`, so `assert not p.exists()` looks admissible; the gloss
says creating the file would *break* the assertion, so it looks inadmissible. **Measured blast radius: exactly 1 of
305** — `headless-terminal::test_cancel_command` (`assert not path.exists()`), labelled `N` by both its seats. The `N` is
right for a *different* reason than the ambiguity (the test also instantiates the uncaptured deliverable
`headless_terminal.HeadlessTerminal`, a clause-3 violation), so **the ambiguity does not flip any label in this
population**. It would flip one if the spec were applied to a negated-existence test with no other violation. Not a
live defect; worth recording as a spec hole for future rounds.

**1.2 — "counts" vs. "membership".** Clause 2 admits listing *membership*; the N clause excludes "a count". A reader
must decide what `len(files) == 0` is. The spec's own worked examples do not settle it. **Measured: 1 test**
(`financial-document-processor::test_original_documents_dir_empty`, `files = [f for f in documents_dir.iterdir() if
f.is_file()]; assert len(files) == 0`). The oracle says `N`; the alt implementation says `P1`. **This is the single
id where two independent implementations of the same spec disagree** (v2 P0 vs alt P1) — the sharpest evidence that
the shared-spec reading is not degenerate. Both readings are defensible; the label seats' own `why` texts
("`len(iterdir())==0 count comparison, not name membership`") show they saw the seam and chose consistently, and the
oracle matches the majority reading. **My own label for this id is `N`** (a count is excluded by the N clause and
creating the directory does *not* satisfy it, because the assertion then fails) — agreeing with the oracle.

**1.3 — Reach: module-level statements.** The reach paragraph names "the test body, plus (transitively) every same-file
helper it calls: module-level functions, `self.` methods of the same class, and fixtures it requests by argument
name". It does not say whether *module-level statements* are reachable. **Measured: 1 of 183 captured files has a
module-level executable statement** (`model-extraction-relu-logits/tests/test_outputs.py:13` — `open('forward.py','w')
.write(...)`, a write, not a read). No Y-labelled test lives in it. **Blast radius 0.** The classifier's report records
the same choice as its ambiguity #12.

**1.4 — In-test import of a non-stdlib module.** Clause 3 forbids "imports and calls code from the task's own
deliverable"; whether an *import without a call* violates it is a live seam (the classifier's fix round changed its
mind: ambiguity #6 → "violation only when called"). **Measured: 28 tests import a non-stdlib module in-test, and all 28
are labelled `N` by both their seats** — so the seam never changes a label here, but it is the seam the two
implementations most visibly disagree about.

**1.5 — Where the classifier's class could flip under a different careful reading.** Of the four candidate seams above,
only 1.2 has a population id at all, and it is already `N`. **The classifier's class does not flip on any of the 305
under any of the readings I could construct.** I tested the `U` route explicitly: no Y-labelled test imports a module
that is neither stdlib, third-party-in-the-capture-set, nor a capture-local helper, so no id is `U`-worthy (the oracle
used `U` zero times, which matches).

**Conclusion for angle (1):** the spec's seams are real but narrow, and **the classifier's class does not flip under
any of them**. The 305/305 agreement is therefore *not* an artefact of the classifier having been tuned to the labels —
it is agreement between two implementations and eight readers on a spec whose remaining ambiguity touches 1 id, which
both sides resolve the same way.

## 2. Angle (2) — shared-spec collusion: could perfect agreement hide a shared misreading?

The worry the seat brief names: eight labellers read one written spec; a systematic misreading yields perfect agreement
on *wrong* labels. I tested this four ways.

**2.1 — Is the disagreement surface empty?** Yes, and it is empty for a *good* reason: `merge_labels`
(`plans/round53_c1_triage.py:189-217`) requires each of the 305 ids to sit in **exactly two** shards, and I verified
the shard-pair structure from the committed shard files: 8 pairs (A,D) (A,F) (B,E) (B,G) (C,F) (C,H) (D,G) (E,H),
38–39 ids each, covering all 305 with no id orphaned. Every pair is **one scout + one reviewer** (0 of 305 have two
seats of the same role) — the design intends two different readings, and it gets them. Per-seat `Y` counts are 14/13/15/
11/13/12/10/16 (sum 104 = 2×52): the seats do **not** agree on a common threshold, they agree per-id.

**2.2 — Did the rationales really come from independent reading?** 610 labels, **602 distinct `why` strings**; the 8
duplicates are the *same sentence on two different ids of different tests* (e.g. `'Asserts st_size greater than zero, a
size value, not presence.'` twice) — natural convergence, not copying. **0 of 305 tests have both seats writing the
same `why` text.** Each seat's text names the specific mechanism it saw (`'Runs gcc subprocess and compares compressed
source length to limit.'`, `'Reads primers.fasta; runs oligotm subprocess; sequence and Tm value checks.'`). A copy
would have produced identical text; there is none.

**2.3 — The leak window.** The two independent classifier implementations wrote their **per-id answer keys** to the
lane during wave 1: `.ufo/waves/round-53/w1/C1ExecClassifier/classes-305.json` (mtime 2026-10-28 21:57:58, 305
id→P1/P0) and `.ufo/waves/round-53/w1/C1ExecClassifierAlt/alt_labels_flat.json` (mtime 21:52:31, 305 id→P1/P0).
The eight label files were written at 21:50:14 – 21:56:23. **Five of the eight label seats (ScoutA 21:53:51, ScoutC
21:54:49, ScoutE 21:54:55, ScoutG 21:55:31, RevB 21:56:23) wrote their labels *after* a complete 305-id answer key
already existed on disk in the shared lane tree.** That is a real leak window and the protocol (blindness rules in
`.ufo/waves/round-53/build_spec_w1.py:38-40`) forbade reading `C1ExecClassifier*`. Two facts keep this from being the
smoking gun: (a) the answer key in question is the **alt** implementation, which differs from the oracle on exactly
one id — `financial-document-processor::test_original_documents_dir_empty`, where alt says `P1` and **both** seats
said `N` with independent rationales; (b) the 3 seats that wrote before the alt key (RevH, RevF, RevD) produced the
same 305/305 agreement as the 5 that wrote after, so a copied key cannot explain the agreement. **Verdict: no evidence
of collusion; a real protocol leak window that the counter cannot detect and that a future round should close by
writing label files to per-seat scratch directories, not the shared lane tree.**

**2.4 — The independent cross-check.** `C1ExecClassifierAlt` implemented the same spec by a deliberately different
method (three-valued abstract interpretation, not call-name matching) and got **53 P1 / 252 P0** against v2's
**52 / 253**. It differs from v2 on **exactly 1 of 305** — and on that id the oracle sides with v2. Two independent
implementations agreeing on 304/305 and disagreeing on the one id the spec genuinely leaves open is the strongest
available evidence that the oracle is not a shared misreading.

**2.5 — My own labels.** I sampled 10 Y and 10 N with a fixed seed (20261030), read each test body against the spec
myself, and compared. **20/20 agreement.** The ten Y are all bare `assert path.exists()` (plus `is_file`/`is_dir`
variants) over literal paths; the ten N all reach a subprocess, a content read, or a value comparison. My readings are
in `samples-20.json`; every Y body I read is in `all-52-Y-bodies.txt`.

**Conclusion for angle (2):** the perfect agreement is **not** an artefact of a shared misreading. The disagreement
surface is provably non-empty (the alt implementation disagrees on 1 id; the spec's count/membership seam touches
another), the rationales are textually independent, the roles are diverse by construction, and my own 20 labels match.

## 3. Angle (3) — the control: is v2 right on each disagreement?

The control requires the round-52 classifier to disagree with the oracle on ≥ max(10, 2×v2's disagreements) decided
tests; it reports 23, and `all_P0_disagree=52` is printed as evidence. Direction of all 23:

| direction | n | reading |
|---|---|---|
| r52 = `P0`, oracle = `Y` | 21 | r52 was too **strict** — it missed plain existence checks |
| r52 = `P1`, oracle = `N` | 2 | r52 was too **permissive** |

I hand-read all 23 against the spec (bodies in `ambiguity-audit.json` / the sampled dumps). **v2 is right on every
one.** Spot detail on the two `r52=P1 / oracle=N` cases, which are the dangerous direction:

* `hf-model-inference::test_model_downloaded` — r52 says `P1`; the oracle says `N`. The test's *first* assertion is
  `assert os.path.exists(model_path)`, but it then does `AutoModelForSequenceClassification.from_pretrained(model_path)`
  inside a `try`, and `assert model is not None` — a value comparison on a computed object (clause 3), plus an in-test
  import of `transformers` and a call into it. **Oracle `N` is right; r52 was reading only the first assertion.**
* `write-compressor::test_compressed_file_exists` — r52 says `P1`; the oracle says `N`. The test calls `setup()`, a
  same-file helper that runs `subprocess.run(["gcc", ...])` — a command (clause 3) reachable through the helper chain
  the reach paragraph mandates. **Oracle `N` is right; r52 missed the helper.**

The 21 `r52=P0 / oracle=Y` cases are all of the shape "`assert path.exists()` over a literal path" (e.g.
`circuit-fibsqrt::test_gates_file_exists`, `cobol-modernization::test_data_files_exist`,
`video-processing::test_test_video_exists`) — r52's lexical split was too strict exactly where presence-only tests
live. **The control is therefore non-vacuous *and* directional: it fails a classifier that over-calls `P1` (the
`hf-model-inference` and `write-compressor` cases) and it fails a classifier that under-calls `P1` (21 cases).** The
counter's `all_P0_disagree=52` is the printed witness that an all-`P0` stand-in cannot pass. **The control survives.**

## 4. Angle (4) — freeze integrity: is the freeze-order leg forgeable?

### 4.1 — What the FREEZE leg actually checks

`leg_freeze` (`plans/round53_c1_triage.py:145-183`) checks: (a) the tree is clean; (b) `git log -- plans/round53-c1-classify.py`
and `git log -- plans/round53-c1-freeze.json` return **exactly one** commit each and they are the **same** commit;
(c) the classifier's sha256 equals the digest recorded in the freeze file; (d) each label file's sha256 equals the
freeze file's pin for it; (e) each shard's digest equals its pin; (f) each label file was committed **after** the freeze
commit and never touched again; (g) `author_seats` is non-empty and no author seat starts with `c1label`.

Every one of (b)–(g) is a **self-consistency** check *within* the tree being examined. There is no anchor that the
tree's freeze commit, freeze file, classifier and label files are the ones the round froze. The four digests the
claims file *does* pin as literals are all population-side (`POP_SHA`, `PIN_TREE_SHA`, `TESTS_INDEX_SHA`,
`R52_AUDIT_SHA`) — the classifier, the labels and the freeze file are pinned only by the freeze file, i.e. by a file
the forgery rewrites together with them.

### 4.2 — The routes the counter *does* reject (all confirmed)

* **Committed label edit after the freeze** (my `f1`): `label_files_pinned=BAD labels_after_freeze_and_untouched=NO`,
  `ORACLE not evaluable`. Correct.
* **Restored-after-edit** (the counter's own selftest `label-restored-still-touched-twice`): rejected, because
  `git log -- <label file>` then shows two commits. Correct — *provided the history is not rewritten*.
* **Merge-commit edit** (my `e3`): `classifier_and_freeze_one_commit=NO labels_after_freeze_and_untouched=NO`. Correct.
* **Classifier edited after the freeze** (counter selftest `classifier-edited-after-freeze`): `classifier_sha=BAD
  classifier_and_freeze_one_commit=NO`. Correct.
* **Classifier edited *and* the freeze file re-hashed** (counter selftest
  `forged-classifier-edit-and-freeze-rehash`): rejected — but **only because re-hashing the freeze file touches the
  freeze file a second time**, which breaks (b). My forgery avoids exactly that by *rewriting history* rather than
  adding commits.

### 4.3 — The forgery that lands

Method (no lane mutation; everything in scratch clones, `git commit-tree` + `git update-ref` on a scratch clone):

1. Take the real freeze commit `d40b7055…` and the real label commit `db90a6b7…`.
2. Replace `plans/round53_c1_classify.py` with a stub whose `classify_source(src)` looks up
   `sha256(src)` in a table of the *forged* per-id classes (so the classifier agrees with the forged labels by
   construction, exactly as a "tuned to the labels" classifier would).
3. Flip **10** `Y` labels to `N` in `C1LabelScoutA/labels.json` **and** in the partner seat's file for each id, so
   every id stays *decided* and `contested` stays 0.
4. Re-pin `label_sha256` (all eight seats) and `classifier_sha256` in `plans/round53-c1-freeze.json` to the new
   digests.
5. Rebuild the two commits with `git commit-tree` — freeze commit contains classifier + freeze file and **no** label
   files; the label commit contains the eight label files — and replay the eight later commits on top with the same
   tree contents, so `git log -- <path>` still shows exactly one commit per file.

Result on the forged tree (`e14`, refined so the flipped ids avoid the 20 confirmed tasks):

```
PINS  population_sha=ok pin_tree_sha=ok tests_index_sha=ok r52_audit_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184
FREEZE clean=yes classifier_and_freeze_one_commit=yes classifier_sha=ok label_files_pinned=ok shards_pinned=ok
      labels_after_freeze_and_untouched=yes authors=4
ORACLE tests=305 bad_label_files=0 bad_label_rows=0 decided=305 contested=0 oracle_Y=42 oracle_N=263 v2_P1=42
      unclassified=0 disagree=0 limit=9.2 per_label_agree=1.000 (min 0.9)
ORACLE-CONTROL r52_classifier_disagree=29 all_P0_disagree=42 control_ok=yes
CONFIRM candidates_never_read=27 new_confirmed=20 rejected=0 target>=3
PRIOR-ART rows=0 ...
```

**Four legs green, `disagree=0`, `per_label_agree=1.000`, `contested=0` — on labels that are wrong.** The only thing
that saved the claim here is that `PRIOR-ART` has no rows yet (so `PREDICATE R53-C1 fail` for an unrelated reason). The
oracle leg and the control leg are exactly the ones A1 hardened, and they are the ones that fell over.

**Why the existing selftest does not catch it.** The counter's own `--selftest` has 47 cases; the three that target
this route (`classifier-edited-after-freeze`, `forged-classifier-edit-and-freeze-rehash`,
`forged-label-edited-after-freeze-committed`) all *add commits* to a fixture history. They test **append-only**
tampering. A rewrite is not append-only: it produces a history where every shape check holds. **No selftest case
constructs a rewritten history** — and the counter's own `rebuild()` helper (`plans/round53_c1_triage.py:724-760`)
rebuilds histories with `git checkout -B` / `git reset` on a fixture, which is exactly the capability the real forgery
uses; the fixture helper is only ever used with *honest* or *reordered* content.

### 4.4 — The root cause, stated precisely

`plans/round-53-claims.md` leg 2 says the classifier's digest "has the sha256 recorded in
`plans/round53-c1-freeze.json`". **That is circular**: the freeze file is one of the two things the forgery rewrites,
and it is committed in the *same* commit as the classifier it certifies (`d40b7055` — `git ls-tree` on that commit
shows **0** label files, yet the freeze file at that commit already pins all eight label digests, i.e. it is a
**forward promise** about files not yet in the tree). The freeze file's own digest appears **nowhere** outside the
rewriteable tree (`grep -rn 6343e0db` → 0 hits), and so do the classifier's (`935db122` in claims → 0) and the label
digests' (`32a1b20b` in claims → 0). The counter's own frozen-constants tripwire
(`plans/round53_c1_triage.py:504-515`) checks `POP_SHA / PIN_TREE_SHA / TESTS_INDEX_SHA / R52_AUDIT_SHA / TESTS_TOTAL /
CAPTURES_EXPECTED / EXCLUDED_* / BASE_TIP / BALANCE_MIN / CONTROL_MIN / CONFIRM_MIN / URL_MIN / LABEL_DIR / SHARD_DIR`
— **no classifier constant exists to check**, so the tripwire cannot fail on a classifier swap.

**Verdict on angle (4): the freeze-order leg is NOT forge-proof. It is a well-designed self-consistency check that a
coordinated history rewrite satisfies.** The claims' own kill rule ("the classifier is never edited after the freeze
commit") is not enforced by the counter; it is enforced by *git's immutability assumption*, which the counter does not
and cannot check.

## 5. The smallest safe correction (three equivalent anchors, all verified)

Each of the following is a one-constant change that keeps the pristine lane green **and** makes the forgery fail.
I implemented and ran all three; the diffs are in `correction-patch.py`.

**(a) Pin the classifier digest in the counter (recommended — smallest).**
Add `CLASSIFIER_SHA = "935db122897149a6013ca06d0001feaba4da04d606adc8197c9ff1acf8f1d0e6"` next to `R52_AUDIT_SHA`,
thread it through `FROZEN`, and require `sha256_file(lane / clf) == cfg["CLASSIFIER_SHA"]` in `leg_freeze`. The
counter then compares the classifier against a value that lives **outside** the rewriteable tree (in the counter, whose
digest the L1 must itself pin) rather than against a value inside the freeze file the forgery rewrites.
Verified: pristine → `classifier_pinned=ok`, FREEZE green, `ORACLE … disagree=0` unchanged; forged tree →
`classifier_pinned=BAD`, `ORACLE not evaluable`, `PREDICATE R53-C1 fail`.
*Caveat:* the selftest fixture builds its own classifier, so the constant must be overridable in the fixture (`cfg`),
exactly as `R52_AUDIT_SHA` already is — otherwise 33 of the 47 fixture cases fail (I measured `cases=47 failures=33`
on the naive pin). With the fixture override the selftest is back to `cases=47 failures=0`.

**(b) Pin the eight label digests in the counter.** Add `LABEL_SHA = {seat: digest}` (the eight digests are in
`honest-label-digests.json`) and require each label file's digest to equal it. Forged tree → `label_digests_pinned=BAD`.
Pristine → `label_digests_pinned=ok`. Same fixture-override caveat.

**(c) Pin the freeze commit's hash.** Add `FREEZE_COMMIT = "d40b7055e0128d7998d09548fdeef431093ab321"` and require
`commits_touching(lane, fz) == [FREEZE_COMMIT]`. Forged tree → `freeze_commit_anchor=BAD`. Pristine → green. This is the
cheapest to express but the least direct (it pins a hash the reader must look up); (a) is better because it also
protects any *other* route that swaps the classifier.

**Whichever is chosen, the frozen claims file should also carry the same literal** (the claims file already pins four
digests this way), so the anchor is anchored in the append-only claims document rather than only in a lane file.
And the counter's own digest (`d36e31f9…` at the tip I ran at) should be pinned in the claims file too — the counter
is the thing that decides, and nothing outside the tree fixes it.

**What is NOT needed.** No threshold changes, no re-labelling, no classifier change, no spec change. The 305 labels and
the 52/253 split stand; what is missing is one out-of-tree constant.

## 6. Impact on the two axes I am judged on

**Novelty.** The claim's novelty rests on an oracle that "cannot be told from a copy of the labels by the counter
alone" — A1 names this as a *named, not hidden* limitation ("a P1 classifier that is correct cannot be told from a copy
of the labels by the counter alone: independence of the label seats is a protocol property recorded in the seat
reports, not something the counter can prove"). **My forgery is that limitation, one level stronger than A1 admitted:**
A1 assumed the *classifier* is honest and only the *labels* might be copied; my forgery swaps **both** and re-pins,
and the counter cannot tell. The A1 disclosure does not cover this case — A1's own words are "the freeze file pins by
sha256 the classifier, the eight label-seat files and the eight shard files", i.e. A1 believed pinning the inputs
suffices. It does not, because the pins live in a rewritable file.

**Calibration.** The oracle's *numbers* are calibrated (305/305, 0 contested, `U` never used, two independent
implementations agreeing on 304/305, control direction correct on all 23). The *instrument* is not: it prints
`labels_after_freeze_and_untouched=yes` and `disagree=0` on a tree where 10 of 52 labels are false. That is a
calibration defect in the sense that matters: the receipt's green is not evidence.

## 7. Recommendation to the L1

1. **Do not admit R53-C1 on the current counter.** Land one of the three anchors in §5 (recommend (a) + the same
   literal in `plans/round-53-claims.md`), regenerate `c1-selftest.txt`, and re-run. Expected effect on the landed
   tree: **none** — every pinned value already matches, so `FREEZE` stays green and `ORACLE … disagree=0` is
   unchanged; only the *forgery* is closed.
2. **Add a selftest case that constructs a rewritten history** (the counter's `rebuild()` helper already knows how to
   build arbitrary histories; a case that rewrites the freeze+label commits together is the missing test).
3. **Record the leak window** (§2.3) in the round-53 lesson: label seats must write to per-seat scratch, never to the
   shared lane tree, because the lane tree held a complete 305-id answer key while five of eight seats were labelling.
4. **Record the spec seam** (§1.2, count-vs-membership at `test_original_documents_dir_empty`) as a known hole: it is
   the one id where two independent implementations differ, and the next round that uses this spec should resolve it
   explicitly.

## 8. Tools

No tool was installed or upgraded. No pacman transaction was attempted (host-wide pacman pause, orchestrator ruling
2026-10-20). Python 3 and git were already present; `git commit-tree` / `git update-ref` were used only on **scratch
clones** under `/fast/scratch/hyaku/kengaku-r53/C1CritOracle2/`. **No mutating git command was run in the lane or the
fleet repo**; the lane tip was `9ead4476bf55b1ea6490d0204b668195db4a4d1d` before and after this seat, and the only
lane paths this seat wrote are `.ufo/waves/round-53/w3/C1CritOracle2.md` and `.ufo/waves/round-53/w3/C1CritOracle2/`.
Disk guard was checked before the heavy passes (`/fast/scratch/hyaku` 42 % used, 467 G free).

## 9. Files produced (all absolute paths)

* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1CritOracle2.md` — this report.
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1CritOracle2/oracle-recomputed.json` — the
  oracle I recomputed from the committed label files and shards (`decided/contested/v2/r52/idx`).
* `…/C1CritOracle2/samples-20.json` — the 10 Y + 10 N ids I re-read by hand (seed 20261030).
* `…/C1CritOracle2/all-52-Y-bodies.txt` — every Y-labelled test body I read.
* `…/C1CritOracle2/ambiguity-audit.json` — per-test ambiguity audit (negated existence, uncaptured imports, fixtures,
  module-level statements).
* `…/C1CritOracle2/honest-label-digests.json` — the eight label-file digests (the `LABEL_SHA` anchor).
* `…/C1CritOracle2/forgery-rewrite4.py`, `…/forgery-rewrite5.py` — the history-rewrite forgery scripts.
* `…/C1CritOracle2/correction-patch.py` — the three candidate anchors.
* `…/C1CritOracle2/REPRODUCE.md` — the exact command list.

**Report:** `.ufo/waves/round-53/w3/C1CritOracle2.md`
