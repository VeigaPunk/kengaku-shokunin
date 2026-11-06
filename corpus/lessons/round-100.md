Author: kengaku (L1 KengakuR100)

# Round 100 — financial-document-processor grader replay and path-matched provenance with a row-level census

BASE `78460376`; P0 `fb0f125c`; P1 `4df35de8`; P1b `934b984a` (amendment 1); P1c `f07c026e` (amendment
1b); P2 `5220b71d`; F `54df15ca`; C = T `dbe0cefa`; receipts `d8ed39bd`.
Frozen predicates: `plans/round-100-claims.md`. Receipts: `.ufo/waves/round-100/L1/c1-tip.txt`, `c2-tip.txt`,
`c1-base.txt`, `c2-base.txt`, `freeze-tip.txt`; controls `.ufo/waves/round-100/L1/controls/` (README).

## Gate

**Search.** Round-99 ConnectorOverlap (c) (`.ufo/waves/round-99/w1/ConnectorOverlap.md:72-144`) ranked the
thin-class candidates; Q86's class arithmetic at BASE gives a three-way tie at 0.333 (crypto-credential
4/12, shell-exec 2/6, subprocess-exec 15/45). `financial-document-processor` is the cheapest feasible
member that lifts `crypto-credential` (+1/12). The pinned tree listing (`corpus/evidence/round53/pin-tree-2fd12b88.json`)
has 26 blobs; all 26 were opened on 2026-11-06 between 12:06 and 12:07 -03, HTTP 200, and each local
copy's git blob id equals the pin-tree id (`.ufo/waves/round-100/L1/capture-time.txt`). The 17 documents'
sha512 digests equal the grader's 17 hard-coded digests (10 invoices + 7 others).

**Captures.** Flat under `corpus/evidence/round100/tb2-financial-document-processor/` (documents under
`documents/`), with `SHA256SUMS` (25 lines) and the task's `task.toml`, so the frozen anchor-digest gate
binds the new rows by `url-task`. `.gitignore` was opened and not captured (no grader, solution or replay
byte reads it).

**Stop rule.** One new member with a positive control, a no-work control, mechanism-specific negatives,
boundary cases and the gaps located. No claim is made about any submitted solution.

| row | URL / access | located quote | decision / reason / flip |
|---|---|---|---|
| S342 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/financial-document-processor/tests/test_outputs.py; 2026-11-06 | `tests/test_outputs.py:66`: assert actual_file_hashes == expected_original_documents, ( (5 words) | mined, tier A: sha512 SET comparison per directory; lookup-by-key CSV check without coverage or uniqueness. Leads to C03, C04, C07, C08 |
| S343 | …/financial-document-processor/tests/test.sh; 2026-11-06 | `tests/test.sh:22`: -w pytest-json-ctrf==0.3.5 (2 words) | mined, tier A: python 3.13, pytest 8.4.1, pandas 2.3.2, pytest-json-ctrf 0.3.5; reward 1 iff pytest exits 0 |
| S344 | …/financial-document-processor/solution/solve.sh; 2026-11-06 | `solution/solve.sh:62`: text = pytesseract.image_to_string(image, config='--psm 6') (5 words) | mined, tier A: the OCR positive control, run once offline with host tesseract 5.5.3; its output equals the grader's table |
| S345 | …/financial-document-processor/instruction.md; 2026-11-06 | `instruction.md:12`: add a final row with the filename 'total' (8 words) | mined, tier A: the contract asks for a FINAL total row and an empty documents directory; neither is enforced (C03, C07) |
| S346 | …/financial-document-processor/environment/Dockerfile; 2026-11-06 | `environment/Dockerfile:14`: RUN uv run /root/randomize_filenames.py (4 words) | mined, tier A: names are randomized at build; staging captured names is grader-equivalent |
| S347 | …/financial-document-processor/environment/randomize_filenames.py; 2026-11-06 | `environment/randomize_filenames.py:14`: random_base = secrets.token_urlsafe(9) (3 words) | mined, tier A: CSPRNG names; sha512 is the only ground truth |
| S348 | …/financial-document-processor/task.toml; 2026-11-06 | `task.toml:29`: docker_image = "alexgshaw/financial-document-processor:20251031" (3 words) | rejected, tier A: the prebuilt image is never pulled; a pinned venv models the grader side. Flip: pull the image and compare its verifier versions to GRADER_SIDE |
| S349 | …/financial-document-processor/README.md; 2026-11-06 | `README.md:40`: Correct summation in the final "total" row (7 words) | rejected, tier B: the README says the tests verify a summation and a final position; the grader bytes check a hard-coded total only, and 11 total rows pass (C03). Flip: a grader revision that sums the invoice rows |

Word counts are computed (`len(quote.split())`), and the candidate tree's line gate was run before F
(Q76, M1): `prefreeze-both-run{1,2}.txt` `VERDICT clean`.

**Admit / reject for the closure spot-check:** admit S342 (A), reject S348 (A) and S349 (B).

**Registry old→new.** No existing SOURCES row changed (C2 K8: `base_rows_not_equal=0` over all 333 BASE
rows). S342–S349 were added: 7 tier A, 1 tier B; 6 mined, 2 rejected. Rows 333 → 341. No status,
recheck or used-by change to an existing row. Outside row S295 (round 93's rejection of this same member:
"a full-pass case needs the 17 environment documents") is not edited; its flip condition is now met by
this round's capture, and the frozen gate re-binds it by url-task (its `capture-unanchored` finding clears,
gate 33 → 32 at P1; amendment 1). Its status cell stays `rejected` as a historical decision.

**Frontier.** Member `financial-document-processor` moved from unexecuted to executed. Ledger executed
43 → 44; `crypto-credential` 4 → 5 of 12 (the class leaves the three-way minimum tie: min_class is now
shell-exec/subprocess-exec at 0.333); `file-artifact` 34 → 35 of 76.

**Census.** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` was rc 0 at
start (31 W04; `L1/census-start.txt`). Pre-append scratch validation of the candidate registry on a
`git archive` mirror: rc 0, 32 W04; the new W04 is S342, whose URL equals an earlier row's across scopes
(`controls/candidate/sources-validate.txt`). End: `L1/census-end.txt`.

**Anchor re-verification (R100-C2).** Nine BASE rows whose digest equals the committed copy of the very
upstream file their pinned URL names, but which the frozen gate bound by `row-path` to a probe receipt the
row merely mentions (`digest-wrong-capture`, 8 rows) or to nothing (S300's 64-hex token), are now bound
by three new three-cell `corpus/evidence/round<N>/PROVENANCE.md` files (rounds 52, 58, 94). Every one of
the nine upstream files was re-fetched live before the freeze and still hashes to the row's digest
(`L1/c2-live-refetch.txt`, 9/9 HTTP 200). Gate findings 33 (BASE) / 32 (REF) → 23 at T. S298 binds the
committed `tests/original-decomp.c` its URL names, not the byte-identical `environment/decomp.c` (round-99
CO-11 risk 2 answered by the population rule, not by exclusion). S300's other two findings keep their
tokens; `fa53d657` sharpens to `abbrev-unresolved` (the 8-hex prefix belongs to `environment/main.rs`).

**Assimilation:** none (inherited `merge/kengaku/` hold, L0 `kengaku | round-54`).

**considerthese:** `considerthese/2026-11-06.md` §1 proposal 1 (make prior `frozen-instruments` paths
immutable under admission), opened this round. Grounded through the lane's own bytes: every
`frozen-instruments` table in `plans/round-*-claims.md`, read at its adding commit, was compared with T —
8 claims files carry a table, 99 rows, **0 differ at T** (`.ufo/waves/round-100/L1/frozen-union-at-T.txt`).
The union check the proposal asks for is therefore green today and is recorded as a harm check of this
round; it is not yet a standing gate (no counter reads it), and Q79 already states the rule. Proposals 2
(Q86) and 3 were not acted on this round.

## Round-99 routed defects — disposition

1. Frozen-clause departure (post-T corrections): `plans/round100_prefreeze_check.py` ran both standing
   gates on the candidate tree before F (clean); the round-100 claims file plans no post-T correction.
   Mistake M1.
2. Harm battery counted findings and read untargeted trees: the round-100 battery
   (`.ufo/waves/round-100/L1/harm/run_harm.sh`) diffs finding SETS and passes `--tip HEAD` to r82c1 inside
   each revision's own checkout.
3. C2 finding-level census: R100-C2 K8 is row-level over every BASE row (P2 `outside-row-delete`: S001
   deleted, K8 the only failing leg).
4. Mutation survivors: C1 L3 (run identity = F), L10 (exact new-row count), L12 (F..rev file set and
   candidate bytes); C2 K3 (three cells), K4 (no id outside POP). Each has a P2 forgery that fails it.
5. Ledger class note (`bn-fit-modify` numeric-band vs `file-artifact`): carried, not changed.
6. L0 `kengaku | round-98` (coverage cap) and `kengaku | round-54` (assimilation hold): carried, open.

## Mistakes

| id | class | evidence | captured-by | fix / shown able to fail |
|---|---|---|---|---|
| M1 | standing gates not run on the candidate tree before the freeze (round 99, mined) | round-99 dated corrections `b71b990a` (typed word counts, line gate live 0 → 5) and `3fdecf31` (registry selftest cells, 13 → 17 DEFECT) after T; `corpus/lessons/round-99-verifier-spotcheck.md` routed defects 1–2 | none: Q76 states the word-count rule and r82c1 existed, but nothing ran them on the candidate tree before F, and the battery compared counts on master | `plans/round100_prefreeze_check.py` (finding-set diff, BASE bytes of both gates, explicit revisions). Able to fail: on round-99 BASE→T it prints 9 `NEW` findings, `VERDICT red`, rc 1 (`L1/prefreeze/able-to-fail-r99-T.txt`); on round-99 BASE→tip `VERDICT clean` rc 0 (`r99-tip-clean.txt`); on this round's candidate tree clean (`controls/prefreeze-both-run{1,2}.txt`). QUALITY Q87 |
| M2 | census reference blind to the round's own pre-freeze bytes | P1a dry battery `controls/dryrun-p1a/c2-do-nothing-run1.txt`, `c2-positive-run1.txt`: K7 `moved=S295` (C1's P0 capture re-binds a row C2 never touched) and K5 fails on S300's sharpened second finding | the P1a control battery (Q80), before any freeze | amendment 1 (`L1/amendment-1.txt`): censuses compare against REF = F~1; K5 compares the token set of a row's other findings and prints `RECLASS`. The P1a receipts are the committed red. QUALITY Q88 |
| M3 | revision syntax: `<F>^{commit}` peels to F, not its parent | P1b dry battery receipts print `REF` = the fixture freeze commit (`controls/dryrun-p1b/c2-positive-run1.txt`) while the docstring promised the parent | none: no leg reads REF's identity; the L1 noticed the hash while reading receipts | amendment 1b (`<F>~1`); the battery of record prints `REF f07c026e…` = P1c, the freeze fixture's parent, and the measurement at T prints `REF 5220b71d…` = F~1. Able to fail: the P1b receipts |
| M4 | a located quote invisible to the line gate | P1a `controls/dryrun-p1a/c1-typed-words-run1.txt`: S343's word count forged 3 → 4 and L13 passed; the frozen line gate does not cite a quote ending in a backslash (`-w pytest-json-ctrf==0.3.5 \`), so 7 of 8 new rows were checkable | the P1a typed-words control | S343 quotes `-w pytest-json-ctrf==0.3.5` (2 words): line gate cited 146 → 147 on the candidate mirror; the battery of record's typed-words control fails L13. QUALITY Q89 |

## Wave findings

Wave w1: 12 seats (ExecC1, ExecC2, ExecHarm, ExecOCR, ReviewC1, ReviewC2, CriticClaims, MutC1, MutC2,
ScoutSources, ConnectorOverlap, ScribeLesson). Role mix: 4 executor, 2 reviewer, 1 critic, 2
mutation-tester, 1 scout, 1 connector, 1 scribe; 5/12 attack seats. The planner seat is held by the L1;
ConnectorOverlap (c) carried the bounded next-round planning data-walk. **Dead seat: ScribeLesson** — it ran
2 h 13 min without writing a report and was cancelled by the orchestrator; its partial scratch
(`.ufo/waves/round-100/w1/ScribeLesson/`) is not evidence and nothing below rests on it. 11 reports at
`.ufo/waves/round-100/w1/<seat>.md`.

| seat / finding | observed verdict or defect | disposition |
|---|---|---|
| ExecC1 | counter pass at T, fail at BASE; two archive probe runs byte-identical to the receipt; C03, C04, C07, C08 rebuilt with its own code under real pytest: 7/7 pass, reward 1 each | C1 met, gaps independently reproduced |
| ExecC2 | its own checker: 90 PASS / 0 FAIL (blob = token = sha cell, one three-cell no-URL line per row); REF→T gate diff over BASE rows = exactly the 9 tokens cleared + the S300 reclass; 333 BASE rows byte-equal | C2 met, independently reproduced |
| ExecHarm | no standing gate green→red; r82c1 `--tip` sets equal; pre-freeze check clean; frozen-instruments union unchanged; round-99 C1 (L7) and C2 (K7) counters fail at T by construction (their BASE sets predate this round's member and bindings) | no harm; by-construction fails noted |
| ExecOCR (hypothesis seat) | **falsified**: host tesseract 5.5.3 and conda-forge 5.3.4 (the pinned version) both reproduce `placement.tsv` and `summary.csv` byte-for-byte and the grader passes 7/7 on each; raw OCR text differs word-level between engines | positive control is engine-version-robust on these 17 documents |
| ReviewC1 | hook observe-only; all 15 builder kinds realise their `why`; captured-name staging grader-equivalent (sha512 recomputed); L1–L13 match the frozen text | no defect |
| ReviewC2 | population re-derived independently (9/9); bindings semantically right (S298 binds `tests/original-decomp.c`); REF amendment sound; K8 row-level; builder re-run at REF reproduces the three files. MINOR: S210/S219 have two byte-identical eligible copies (lexicographic pick); `c2-pop.txt` labels `REV fb0f125c` though derivation is at BASE; K9 ignores `bytes=` | no defect above MINOR; routed |
| CriticClaims | F1 L3+L6 cannot distinguish a probe run at F from one at T (LANE_TIP is self-reported; outputs equal); F2 C2 alone accepts an added SOURCES row or a SKILL edit (C1 catches them); F3 K9 checks a receipt, not liveness (its own 9/9 re-fetch is what proves freshness); F4 `freshness` defensible this round; F5 Q86 choice defensible; F6 separability disclosed; F7 no frozen-clause violation; F8 no do-nothing control reaches either TARGET | F1–F3 routed |
| MutC1 | 47 mutants: 27 killed, 19 survived (+1 inconclusive), every tree forgery killed by its named leg; survivors are sole-guard clauses (L3, L7 conjuncts, L10 count, L12, L13) and F1: the TARGET line is printed, never asserted by the counter's rc | routed: assert TARGET fields in the counter |
| MutC2 | 65 mutants / 87 runs: 44 killed, 19 survived; one real gap T21 — a duplicated SOURCES row (same id) is invisible to K8/K10 and to C1 L10 (ids are a set); other survivors sole-detector or unreachable | T21 routed |
| ScoutSources | S342–S349 re-opened live: 8/8 agree (bytes, quote line, computed words); 9/9 C2 URLs equal; gates, census and counters agree; Gate decisions agree (admit S342, reject S348, S349) | agree |
| ConnectorOverlap | no sibling replays this member or uses row-scoped provenance; next members by Q86: `build-cython-ext` (subprocess-exec, highest summed lift), shell-exec none feasible; 23 remaining anchor findings grouped, 3 zero-byte cell edits measured 23 → 20 | next-round planning input |
| ScribeLesson | dead (no report) | disclosed; not evidence |
