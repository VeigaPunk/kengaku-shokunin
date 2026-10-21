# ExecPerturbCases (KengakuR26-2.ExecPerturbCases-4), round 26 build

**Clone:** `/tmp/kengaku-r26-ExecPerturbCases`, branch `r26-ExecPerturbCases`, observed base `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d` (`git rev-parse HEAD`). Nothing committed: `git status --porcelain` → `?? plans/fixtures/r26/`.
**File written (the only one in the clone):** `plans/fixtures/r26/perturb_cases.jsonl`, sha256 `7a95677e6650fb27b3b397af5b289d6527034618e1f8625af8fb974c0c4c034d`, 277 lines, 290540 B, ASCII, LF endings, 277 unique ids.
**Schema, one case per line:** `id fid kind(MP|MC) variant scope edges file line cell grader(state|seq|c) pid turn want prev_truth raw baseline_got baseline_ok stored_ok applicable counted transform perturbed regraded_got regraded_ok outcome(invariant|flip|detected|missed|n/a) why`. Real cell names drive the grade_c inputs (grader.py:483-484) and route C-MONO to valid_latin (:498-501). D1 cases carry `prev_truth` because the fixture has no meta; ExecPerturbCore added a `rec.prev_truth` fallback for this.
**Scope:** `family` (258 cases) means (applicable, regraded_ok) holds for every implementation consistent with round-26-claims.md:56-67. `instance` (19 cases) means the outcome depends on a choice that text leaves open; `variant` and `why` name the choice. Consumers should assert `apply_family` agreement only on family cases; `regrade(rec, perturbed) == regraded_ok` holds on all cases.
**Applicability rules** (agreed with ExecPerturbCore by message: "All your stated applicability rules should now match"): F1 when "```" is in raw (strip all markers) · F2 when "```json" is in raw (replace all) · F3 when extraction is non-null · F4 when the extracted dict has at least 2 keys · F5/F6 always · F7 when an LF has no CR · D1 when prev_truth is non-null · G1/G2 when baseline_ok is true and the answer has a mutable value / is non-empty.
**Method:** I entered the expectations by hand first, as a P/F/- matrix of 27 bases × 10 families, in scratch `/tmp/kengaku-r26-ExecPerturbCases-scratch/gen_cases.py`, which reported `hand-vs-computed disagreements: 0`. The independent one-off `verify_cases.py` (same dir) reads only the JSONL plus grader.py (sha256 `90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f`). It recomputes baseline and regraded got/ok with extract_json_block/grade_state/grade_seq/grade_c/valid_latin, plus the rule, outcome and counted fields, and checks that each default perturbed text is an admissible instance of its family.

`python3 /tmp/kengaku-r26-ExecPerturbCases-scratch/verify_cases.py /tmp/kengaku-r26-ExecPerturbCases` → exit 0:
```
base edges (P=regraded PASS, F=FAIL, -=n/a, *=scope instance)   bl F1  F2  F3  F4  F5  F6  F7  D1  G1  G2
B01  fence-json,single-line,real-shape-r8:11                    P  P   P   P   P   P   P   P   F   F   F
B02  fence-json,indented,turn-1,real-shape-r9:9                 P  P   P   P   P   P   P   P   F*  F   F
B03  fence-no-language-tag                                      P  P   -   P   P   P   P   P   F   F   F
B04  bare-json,single-line,real-shape-r11:689                   P  -   -   P   P   P   P   -*  F   F   F
B05  bare-json,indented                                         P  -   -   P   P   P   P   P   F   F   F
B06  two-fenced-blocks,real-shape-r8:223                        P  P*  P   P   P   P   P   P   F   F   F
B07  two-fenced-blocks,last-block-not-json,fallback-extracted   P  P   P   P   P   P   P   P   F   F   F
B08  crlf-native                                                P  P   P   P   P   P   P   -*  F   F   F
B09  prose-braces-before                                        P  P   P   P   P   P   P   P   F   F   F
B10  prose-brackets-after,json-parseable-prose                  P  F   F   P   P   P   P   P   F   F   F
B11  prose-braces-after,unparseable-prose                       P  P   P   P   P   P   P   P   F   F   F
B12  prose-braces-after,json-parseable-prose,empty-object       P  F   F   P   P   P   P   P   F   F   F
B13  filler-ready,no-json,baseline-fail                         F  -   -   -   -   F   F   -*  F   -   -
B14  truncated-output,unterminated-fence,baseline-fail          F  F*  F*  -   -   F   F   F   F   -   -
B15  dangling-close-fence,real-shape-r11:92                     P  P*  -   P   P   P   P   P   F   F   F
B16  duplicate-keys,real-shape-r12:157                          P  P   P   P   P   P   P   P   F   F   F
B17  single-key-object                                          P  P   P   P   -*  P   P   P   F   F   F
B18  baseline-fail,noop-turn,prev-equals-want                   F  F   F   F   F   F   F   F   P   -   -
B20  seq,fence-json                                             P  P   P   P   -   P   P   P   F   F   F
B21  seq,bare-json,single-line,real-shape-r12:232               P  -   -   P   -   P   P   -*  F   F   F
B22  seq,nested-list-values,depth-3,fence-json                  P  F   F   P   -   P   P   P   F   F   F
B23  seq,nested-list-values,depth-2,bare-json                   P  -   -   P   -   P   P   -*  F   F   F
B30  grade_c,nested-list-values,fence-json,real-shape-r8:253    P  P   P   P   P   P   P   P   -   F   F
B31  grade_c,nested-list-values,bare-json,indented              P  -   -   P   P   P   P   P   -   F   F
B32  grade_c,extra-ungraded-key,empty-list-value                P  P   P   P   P   P   P   P   -   F*  P*
B33  grade_c,with_rule-false,claimed-violation                  P  P   P   P   P   P   P   P   -   P*  F
B34  grade_c,valid_latin,nested-list-values,real-shape-r8:256   P  P   P   P   -   P   P   P   -   F   F
variants: B06-F1-last=F(flip,instance); B16-F4-textual=F(flip,instance); B32-G2-first-key=F(detected,instance); B32-G1-note-value=P(missed,instance); B33-G1-square-token=F(detected,instance); B13-D1-prev-equals-want=P(flip,family); B02-D1-no-prev=-(n/a,family)
outcomes: F1 flip=4 invariant=18 n/a=6 | F2 flip=3 invariant=16 n/a=8 | F3 invariant=25 n/a=2 | F4 flip=1 invariant=19 n/a=8 | F5 invariant=27 | F6 invariant=27 | F7 invariant=22 n/a=5 | D1 flip=21 invariant=2 n/a=6 | G1 detected=24 missed=2 n/a=3 | G2 detected=24 missed=1 n/a=3
cases=277 scope_family=258 scope_instance=19 verified=277 failures=0
```
**Red check:** in a copy of the fixture I planted 4 defects (B10-F1 regraded_ok flipped, B08-F7 marked applicable, a B01-F5 lead-in containing `[note]`, the B20-D1 outcome relabelled). The verifier reports `cases=277 … verified=273 failures=7`, exits 1, and names every planted defect.

**Findings.** Real-data figures come from read-only eval one-offs over the 1964 records in the four files that carry both raw and ok.
1. **F1/F2 flip PASS→FAIL when prose after the answer holds a JSON-parseable bracket group.** The fallback returns the LAST parseable candidate (grader.py:128-133): B10 `…operations [2, 5].` → got `[2,5]`; B12 `…removed set is {}.` → got `{}`. Unparseable braces are harmless, before (B09) or after (B11) the answer. Real exposure: 0 of 1964 raws have a bracket or brace outside the fences and the answer text.
2. **F1/F2 also flip when list nesting goes deeper than one level.** B22 `[["alpha",["beta"]],"gamma"]` → `["alpha",["beta"]]`, because the bare regex balances only one nested `[...]`. Dicts with list values are safe (B30, B31, B34). Real answer-depth histogram {1: 1948, 2: 4, 3: 12}; the depth-3 records are C-cell dicts, whose braces nest only one level. Real exposure: 0.
3. **The F1 wording "strip the code fence" (round-26-claims.md:58) is ambiguous on multi-block raws, and the choice changes real counts.** On the 31 multi-block r8 B-cell raws, stripping all fences flips 0 records while stripping only the final fence pair flips 17 (first: round8-horizon:223); B06 vs B06-F1-last shows the same split. The core strips all fences; the oracle works from the pre-registration text alone, so its F1 count could differ by up to 17. Decision for L1: pin "strip all fences" in an amendment before comparing counts.
4. **F4 must reverse the extracted object, not the raw text.** Reversing the text changes which duplicate key json.loads keeps (real shape r12:157), so B16-F4-textual flips PASS→FAIL.
5. **D1 flips 21 of 23 applicable cases, in both directions.** On no-op turns it turns FAIL into PASS (B18, B13-D1-prev-equals-want). It also overrides truncated answers (B14) and dangling-fence answers (B15), via a mis-paired fence plus the fallback.
6. **G1/G2 sensitivity holds for every implementation on state and seq answers; for grade_c it depends on which value is touched.** C-norule ignores the claimed violation index when the kept rows match: B33-G1 `[3]→[4]` stays PASS (grader.py:255-261). Extra keys are never read, so B32-G2 (deleting `note`) and B32-G1-note-value are missed. Real exposure: all 9 baseline-PASS r8 C dicts are detected under both G1 and G2 (no extra keys; their C-norule violation lists are empty).
7. **F3, F5, F6 and F7 never flip on any base.** F5/F6 prose without backticks or brackets is provably inert, because no regex match can start inside it. F7 is safe because `\s*\n` accepts `\r\n` and json.loads skips `\r`. These are synthetic cases, not population rates.

**Risks:** the expectations are bound to grader.py at sha256 90c87c88…941f; any change to the extractor or graders means re-running the verifier. I did not run grader_perturb.py against the fixture (not assigned). Suggested integrator gate: for every case, regrade(Rec built from the case, perturbed) == regraded_ok; on scope=family cases, also (apply_family(fid, raw, baseline_got, rec) is None) == (not applicable).
**Installs:** none. Scratch stayed in /tmp; I made no write, jj or git mutation in the live lane tree beyond this report.

VERDICT: DONE. perturb_cases.jsonl has 277 cases (27 bases × F1–F7/D1/G1/G2 plus 7 variants) covering all 8 requested edge classes, 277/277 verified against grader.py, and the red check exits 1. One pre-registration ambiguity (F1 on multi-block raws, 17 real records) is routed to L1.
