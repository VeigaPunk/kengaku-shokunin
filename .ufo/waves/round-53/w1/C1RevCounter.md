# C1RevCounter — round 53, wave 1 — line-by-line review of `plans/round53_c1_triage.py`

Seat: `C1RevCounter` (reviewer, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. No lane file was edited, staged or committed. Scratch: `/fast/scratch/hyaku/kengaku-r53/C1RevCounter/` (removed at exit). Deliverables: `.ufo/waves/round-53/w1/C1RevCounter/`.

## 0. Summary

- **Frozen counter (commit `a34838f`, blob sha256 `1ba1a800…931bf`): `--selftest` reproduces `cases=22 failures=0`** (rc 0), both in the lane root at review start (file = `a34838f`; `git status` clean for `plans/`) and in a `git archive a34838f` extraction under scratch.
- **The lane moved while I reviewed.** `plans/round53_c1_triage.py` was rewritten in the working tree (mtime 22:20:19 -0300; sha256 `61d44a92…cc9`, "amendment A1"); `plans/round-53-claims.md` gained `### A1` and `### A2`; `.ufo/waves/round-53/claims/c1-selftest.txt` now reads `cases=46` (it read `cases=22` when I first opened it); HEAD went `1373b6c` → `56fdff7`. The task asked for the frozen predicate, so the findings below are against `a34838f`. Where A1 appears to address a finding I say so, but **I did not verify A1's fixes** (see §6).
- **The frozen battery is weak.** My mutants (48 runs) were killed 19 times. One of the two ORACLE cases is vacuous for its own rule (the 3 % disagreement bound is deleted and the case still fails, for a different reason). Forcing the CONFIRM leg to always reject passes 21 of 22 cases.
- **Frozen-counter defects that the frozen sentence permits, all measured on fixtures:** D1 report path not confined to `.ufo/waves/round-53/` (accepted, absolute too); D2 quote matched after whitespace normalisation, not verbatim (CONFIRM and PRIOR-ART); D3 `fetched/../` escape accepted; D4 sweep of one file listed twice accepted; D5 two valid rows for one task accepted; D6 substring "naming" (`test_cx` ⊂ `test_cxyz`, `t2` ⊂ `t20`); D7 freeze ordering proves only the freeze file's first commit, so a classifier committed after the labels passes and a classifier edit after the freeze with a rewritten freeze file passes. Details and repairs in §3.

## 1. Blindness and disclosure

- I did not open any `C1Label*` directory, any label file, any `C1ExecClassifier*` file, or any classifier output. I did not run the counter's ORACLE leg on the real lane. All oracle-leg runs used fixtures under scratch.
- Disclosure: the `A2` text in `plans/round-53-claims.md` quotes an L1 oracle printout (`disagree=0`, `control_ok=yes`, file `c1-after-oracle.txt` at `db90a6b`). I read those quoted numbers incidentally. I did not open that receipt and tuned nothing against it.
- Disclosure: one error line from the A1 counter, run on my fixture, printed the path string `.ufo/waves/round-53/w1/C1LabelScoutA/labels.json` (a name only, no content).
- I did not read sibling reports (`C1CritCounterReach`, `C1MutCounter`, etc.); I read only the L1's summary of them in the A1 text.
- `plans/round53_c1_classify.py` does not exist in the lane at my review time (`No such file or directory`), so the real classifier was never run by me.

## 2. Commands run (exact)

```
# lane root, at review start (file == a34838f; TMPDIR on NVMe scratch)
TMPDIR=/fast/scratch/hyaku/kengaku-r53/C1RevCounter python3 plans/round53_c1_triage.py --selftest      -> cases=22 failures=0, rc 0
# scratch extraction of the claims commit
git -C <lane> archive a34838f | tar -x -C <scratch>/clone ; python3 plans/round53_c1_triage.py --selftest   -> cases=22 failures=0, rc 0
git -C <lane> show a34838f:plans/round53_c1_triage.py > FROZEN_counter.py      (sha256 1ba1a800…931bf)
git -C <lane> show a34838f:plans/round53_c1_extract.py > round53_c1_extract.py
# re-measured the working-tree counter (copied to scratch; sha256 61d44a92…cc9)
... --selftest -> cases=46 failures=0 (earlier copy at 22:4x: cases=42 failures=0; claims A1 text says 44)
# pins on the real tree (read-only, via the frozen module)
leg_pins(lane) -> PINS population_sha=ok pin_tree_sha=ok tests_index_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184
```

Mutation and fixture harnesses (copies in the deliverable directory): `mutate.py` (24 single-rule neutralisations of the frozen file), `mutate2.py` (24 more, incl. one duplicate), `verify*.py` (fixture attacks). `mutate.py` and `mutate2.py` read the counter from the lane path; their baseline line printed `cases=22 failures=0` at the time, so they measured the frozen file. To reproduce, point them at `git show a34838f:plans/round53_c1_triage.py`.

## 3. Leg by leg: sentence vs code (frozen `a34838f`)

Line numbers are the frozen file's. "Stricter/looser/different" is relative to `plans/round-53-claims.md` Claim 1 legs 1–4 and the one predicate sentence.

### Leg 1 — PINS (lines 76–112)

- Matches the sentence on every pinned digest: population (81), pin tree and tests index (82–83), each capture's git blob SHA-1 (`blob_sha1`, 90–101), `absent == 0` (97–98), excluded path absent with pinned blob (95), count `183 + 1 = 184` (106–107). Measured on the real tree: `captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184`.
- **Looser (unmeasured, amendment-needed):** `f.is_file()` and `f.read_bytes()` (97, 99) follow symlinks, so a symlink to bytes with the pinned blob passes. Code-read only.
- **Different (cosmetic):** the count check compares the population list, not the directory, so extra files in `corpus/evidence/round52/graders/` are invisible to this leg. The predicate never reads them (CONFIRM and PRIOR-ART read only files named by the pinned index or by the rows), so this has no effect on the verdict.

### Leg 2 — FREEZE + ORACLE (lines 115–214)

- Classifier digest (131): checks the classifier against the **current** freeze file, and the freeze file's own content is never pinned. Looser than "the classifier's sha256 is recorded in the freeze file, which is committed earlier" (D7).
- Ordering (115–118, 132–135): compares only the first `--diff-filter=A` commit of the freeze file with the first add of `oracle-labels.json`, using `merge-base --is-ancestor`. It does not check when the classifier was first committed, whether the freeze file was modified after its first add, or whether the labels file was modified after it (D7). Looser than the spirit ("labels read only after the classifier was committed").
- Disagreement (202, 204–205): `dis <= 0.03 * max(1, len(decided))` over decided tests; `P1 == Y` comparison; decided requires both labels equal and `Y`/`N`. Matches the sentence. Contested `<= 0.15 * n` (205) and `n == 305` (204) match.
- Unclassified (204): `v2_classes` maps an unclassified test to `P0` and records it, and `not uncl` (204) enforces `unclassified = 0`. Matches.
- Labeler independence (`load_labels`): `set(labelers) & authors` and `len(set(labelers)) == 2` match "two distinct labeler seats not in author_seats". Matches.
- Control (180–181, 203): `ctl_ok = dis52 >= 2*max(dis,1) and dis52 >= 10`. Matches "≥ max(10, 2×dis)" (for `dis=0` both forms reduce to ≥10). **The round-52 control module is not digest-pinned** (181 loads it with no hash check; grep finds no pin in the frozen file). Amendment-needed (D8, code-read).
- **Different (cosmetic):** the classifier module is loaded (`v2_classes`, 163–177, via `load_mod`) whenever `author_seats` is non-empty, *before* the FREEZE verdict is judged (verdict guard at 374 lacks `ok_fz`). `ok` still ANDs `ok_fz`, so no verdict effect, but seat-written code runs first (D11).

### Leg 3 — CONFIRM (lines 216–294)

- Never-read texts (216–229): `corpus/knowledge/*.md` at `BASE_TIP` minus `tb2-grader-vacuity-triage.md`, plus `SCORECARD.md`, `LOG.md`, `SKILL.md`, `corpus/README.md`. Matches the sentence (59 texts scanned at the tip).
- **Looser (amendment-needed, D6-iii):** `seen_before` (231–233) uses a hyphen/alnum boundary regex. The sentence says the id "occurs in" the text, which is a literal occurrence. Measured: text containing `break-filter-js-from-html` makes `filter-js-from-html` never-read under the regex and seen under a literal scan. At the real tip the two agree (literal-seen 19 = regex-seen 19, delta `[]`), so the effect today is zero. Repair: `task in text`.
- Candidates and round-52 exclusion (236–246): P1 required, round-52 confirmed tasks excluded (from base-tip `confirmations.json`). Matches.
- `confirmed is True` (266), unknown test id (268), candidate membership (270), duplicate task (272, 287), reader not in authors and not `KengakuR53*` (reader check, ~276). Match.
- **Quote (265, 274): looser than "found inside the span"** (D2). Both quote and span are whitespace-normalised by `norm`, so a quote that is not a verbatim substring passes. Measured Y1: capture text with a double space, quote with a single space: `CONFIRM ... new_confirmed=1 rejected=0`. Length (`QUOTE_MIN_CHARS=20`, line 43) is counted after normalisation.
- **Span (265): different, cosmetic (D9).** `src[lineno-1:end_lineno]` starts at the `def` line, so decorator lines are outside the span (Y4 measured `@pytest.mark.parametrize` on the line before `def` is excluded). Class methods: span is the method's own lines; siblings and the class header are excluded. The sentence is silent on decorators; the code is stricter. Document it.
- **Report path (263, 278): looser (D1).** No check that the path is relative, free of `..`, or inside `.ufo/waves/round-53/`; `lane / rel` accepts an absolute path (`lane / "/abs"` is `/abs`). Measured V1 (`corpus/ReaderSeat/report.md`) and V2 (absolute, outside the lane): both `new_confirmed=1`.
- **Report names task (280): looser (D6-ii).** `r["task"] not in rep.read_text(...)` is a substring test. Measured (verify8 c): report text containing `t20` but not `t2` passes.
- Report digest (278): matches. Reader substring in report path (278): matches "path contains the reader's name" in practice.

### Leg 4 — PRIOR-ART (lines 297–360)

- **Fetched path (312–316, 314): looser (D3).** The check is `startswith("corpus/evidence/round53/fetched/") and is_file()`, with no `..`, absolute, or symlink check. Measured V3: `corpus/evidence/round53/fetched/../../../../../SECRET.txt` (resolving outside the lane) with the matching digest is accepted, `rows=1 ... rejected=0`.
- Digest (316): matches.
- **Quote (335): looser than "verbatim" (D2).** `8 <= len(q.split()) <= 25` is inclusive and matches the word band (no selftest case covers the band edges; see §4). `q not in norm(text)` is whitespace-normalised. Measured V4: archive `test_c merely` with a triple space and the quote with a single space: accepted.
- **Known rule (337): looser than "name the task or one of its test names" (D6-i).** `any(n in text ...)` and `task not in text` are substring tests. Measured verify8 b: archive containing `test_cxyz` satisfies test `test_cx`: `rows=1 known=1 rejected=0`.
- New rule (340–348): `len(sw) < 2` (341) is correct: a one-entry sweep is rejected (measured verify8 e: `REJECTED t2:new-needs-two-sweep-fetches`). **Looser than "sweep of ≥2 archived fetches" (D4):** no distinctness check on sweep entries (344–348). Measured X5: `sweep=[s1, s1]` accepted, `new=1 rejected=0`.
- Sweep names-the-task (344–348): substring (stricter than the sentence, cosmetic).
- The new row's own archive is not checked against the task name; the sentence does not require it, so this is consistent with the frozen text.
- **One row per task (350–351, 358): looser (D5).** `covered` is a set and rows are not deduplicated, so two valid rows for one task pass. Measured (verify8 a): two rows for `t2`, different URLs, `rows=2 tasks_covered=1/1 rejected=0`. The sentence says "one row per confirmed task".
- URL count (297–298, 350, 358): `url_key` lower-cases the URL and strips query, fragment and trailing slash, so `https://Ex.com/A` and `https://ex.com/a` count as one (X4 table). Stricter than "≥3 distinct URLs"; cosmetic (define the key in the claim).
- `example.org` (328) is a substring test over the whole URL: stricter; cosmetic.
- `covered == set(confirmed)` (358), `new >= 1`, `not rej`: match the sentence.

### Ordering proof (summary)

Holds only for the freeze file's first add versus the labels' first add (134–135). Does not cover the classifier's commit, later edits to the freeze file, or edits to the labels file (no digest, no last-touch check). Measured: V9 (freeze file first, labels second, classifier third, freeze file re-committed with the real digest) gives `FREEZE classifier_sha=ok order=freeze-before-labels`. verify2: classifier edited after the freeze commit with a rewritten freeze file gives `classifier_sha=ok order=freeze-before-labels`, while the sha at the freeze commit (`62fa6006…`) differs from the working-tree sha (`24e8f0d6…`) in that run.

## 4. Selftest review — 22 cases (frozen `a34838f`)

Mutant key: `M#`/`N#`/`X#` from `mutate.py`/`mutate2.py` (killed = case flips to FAIL when the named rule is neutralised). `Z#` from `verify5.py`.

| # | case | named rule | killed by | verdict |
|---|---|---|---|---|
| 1 | nothing-committed | FREEZE absent | not run | tests only the file-absence branch |
| 2 | tiny-fixture-control-vacuous | CONTROL_MIN | M19 | survives M1; asserts only that the tiny fixture fails the control |
| 3 | no-confirmations | CONFIRM_MIN | not killed (M20 survives) | **vacuous** for CONFIRM_MIN (prior-art's `bool(confirmed)` also fails it) |
| 4 | known-only-fails-score-rule | new ≥ 1 | M16 | non-vacuous |
| 5 | genuine-fixture-passes | positive control | Z2, Z3 | **the only acceptance case in the battery** |
| 6 | forged-confirmed-string | `confirmed is True` | M2 | isolating |
| 7 | forged-reader-is-author | reader ∈ authors | M5 | isolating (KengakuR53 prefix N8 survives) |
| 8 | forged-quote-outside-span | quote in span | M4 | isolating |
| 9 | forged-short-quote | quote ≥ 20 | M3, N15 | isolating |
| 10 | forged-report-names-other-task | report names task | M7 | isolating |
| 11 | forged-report-digest | report digest | M6 | isolating |
| 12 | forged-prior-art-example | example.org | M8 | isolating |
| 13 | forged-prior-art-unfetched | fetched exists | not run | non-vacuous, unmeasured |
| 14 | forged-prior-art-digest | fetched digest | M9, N11 | isolating |
| 15 | forged-prior-art-quote | quote in archive | N14 | isolating |
| 16 | forged-new-without-sweep | sweep present | M10 survives | **partly vacuous**: the case omits the key, so it never reaches the `len(sw) < 2` check; a one-entry sweep is untested |
| 17 | forged-capture-bytes | blob match | M11 | isolating |
| 18 | forged-population-shrunk | population sha | M12 | isolating |
| 19 | forged-labeler-is-author | labeler ∉ authors | M13 | isolating for M13; bad-row rule (M24) survives (see 21) |
| 20 | forged-one-labeler-twice | two distinct labelers | M14 | isolating |
| 21 | oracle-disagreement | disagreement ≤ 3 % | **M1 survives** (killed only by X1 = M1 + control) | **vacuous for its rule.** rc 1 comes from the control (line 203): this fixture has one decided Y, so `dis52 = 1 < 2·max(dis,1)` |
| 22 | classifier-edited-after-freeze | classifier sha | M15 | isolating |

Battery-wide: forcing the CONFIRM leg to always reject (Z3) passes 21 of 22 cases (only `genuine-fixture-passes` fails). Forcing `leg_pins` false (Z2) fails 18 and passes 4 (nothing-committed, forged-capture-bytes, forged-population-shrunk, classifier-edited-after-freeze). Forged cases assert `rc == 1` plus one reason string, so any counter that rejects everything passes them.

Rules with **no selftest case at all** (survived when neutralised): CONFIRM_MIN (M20), URL_MIN (M21), TESTS_TOTAL (M22), contested budget (M18), extra label rows (M23), bad label rows (M24, masked by the control), unclassified (Z4), `not rej` (N17), covered == confirmed (N16), freeze order (N6), authors non-empty (N7), KengakuR53 reader prefix (N8), duplicate task (N4), candidate membership (N3), r52 exclusion (N2), never-read guard (N1), task id vs index (N5), known-names-task (N9), sweep names task (N10), word band 8/25 (N12, N13), index and pin-tree sha (N18, N19), excluded blob (N20), absent count (M17, N21), file count 184 (N22), sweep ≥ 2 (M10).

## 5. Mutation results

- `mutate.py` (24 single-rule neutralisations; baseline `cases=22 failures=0`): **killed 15/24**. Survivors: M1 (disagree bound), M10 (sweep ≥ 2), M17 (absent counted), M18 (contested bound), M20 (CONFIRM_MIN), M21 (URL_MIN), M22 (TESTS_TOTAL), M23 (extra labels), M24 (bad label rows).
- `mutate2.py` (22 neutralisations + X1 + X2; X2 duplicates M1): **killed 4/24** (N11, N14, N15, X1). Survivors: N1–N10, N12, N13, N16–N22, X2.
- Combined: **19 of 48 runs killed.**
- `verify5.py` (Z-series, against `a34838f`): Z4 `not uncl`, Z5 `not bad`, Z6 `not extra`, Z7 sweep ≥ 2, Z8 absent, Z9 contested budget all survive.

## 6. Findings (frozen `a34838f` unless marked)

Class: `amendment-needed` changes behaviour under the frozen sentence; `cosmetic` changes nothing (documentation or a no-op).

| id | path:line | class | evidence (measured unless marked) | minimal repair |
|---|---|---|---|---|
| D1 | `plans/round53_c1_triage.py:263, 278` | amendment-needed | V1 `corpus/ReaderSeat/report.md` → `new_confirmed=1`; V2 absolute path outside the lane → `new_confirmed=1` | reject absolute, `..`, symlinks; require `(lane/rel).resolve().is_relative_to((lane/".ufo/waves/round-53").resolve())` |
| D2 | `:265, :274` (CONFIRM), `:335` (PRIOR-ART) | amendment-needed | Y1: capture with double space, quote with single space → `new_confirmed=1`; V4 triple-space archive accepted | compare raw `r["quote"] in raw_span` (no `norm`); length on the raw stripped quote |
| D3 | `:314` | amendment-needed | V3: `fetched/../../../../../SECRET.txt` (outside) with matching digest → `rows=1 rejected=0` | same confinement as D1 under `corpus/evidence/round53/fetched/` |
| D4 | `:340–348` | amendment-needed | X5: sweep `[s1, s1]` → `new=1 rejected=0` | require distinct resolved paths and digests across sweep entries |
| D5 | `:350–351, :358` | amendment-needed | verify8 a: two valid rows for `t2` → `rows=2 tasks_covered=1/1 rejected=0` | reject a second row for an already-covered task |
| D6-i | `:337` | amendment-needed | verify8 b: `test_cxyz` satisfies `test_cx` → `known=1 rejected=0` | token-boundary match for test and task names |
| D6-ii | `:280` | amendment-needed | verify8 c: report with `t20` only → accepted for `t2` | token-boundary match |
| D6-iii | `:231–233` | amendment-needed (zero effect at tip) | regex vs literal: `filter-js-from-html` never-read under regex, seen under literal; tip delta `[]` | `task in text` |
| D7 | `:115–118, :131–137` | amendment-needed | V9: classifier first committed after labels, freeze file re-committed with real digest → `order=freeze-before-labels`; verify2: classifier edited after freeze, freeze file rewritten → `classifier_sha=ok order=freeze-before-labels` | freeze file and classifier each added in one commit and never touched again; label files digest-pinned in the freeze file and added after it, never touched again (A1 does this; I did not verify it) |
| D8 | `:180–181` | amendment-needed (code-read, unmeasured) | no digest on `plans/round52_c1_grader_audit.py`; a control module that says P1 everywhere could pass the ≥10 check on decided N's | pin the module sha256 (A1 pins it as `R52_AUDIT_SHA`) |
| D1b | `:97, :99` | amendment-needed (code-read, unmeasured) | symlinked captures read through | reject symlinks |
| D9 | `:265` | cosmetic | Y4: decorator line outside span | document, or include the first decorator line |
| D10 | `:297–298, :328` | cosmetic | X4 table: `url_key` collapses case, query, fragment; `example.org` substring | define in the claim |
| D11 | `:374` | cosmetic | classifier module loaded before FREEZE judged; `ok` still ANDs `ok_fz` | add `ok_fz` to the guard |
| D12 | `:202–203` | cosmetic (no-op) | `max(1,len(decided))`, `max(dis,1)` equal the sentence in practice | none |
| D13 | `plans/round53_c1_extract.py` (`walk`, recursion into class bodies only) | cosmetic/latent | Real tree: 0 indented `def test_` outside the index (verify8 d), 305 indexed, 0 with a class. A test under a module-level `if`/`try` is not indexed (synthetic check) | none needed now |
| D14 | selftest `oracle-disagreement` (case 21), `forged-labeler-is-author` (19) | amendment-needed (test) | M1 and M24 survive: the control, not the named rule, fails these fixtures | add ≥2 decided Y and ≥2 decided N and a control stub that disagrees, so each oracle rule can fail alone |
| D15 | selftest (see §4) | amendment-needed (test) | 26 rules have no selftest case that fails when they are removed (the list in §4); the ≥2 sweep rule is one of them | one case per rule that flips only that rule |

Two notes on D7 and D14: the repairs describe what the frozen sentence should have said, and the A1 text reports it made similar changes. D7 is the most consequential: a seat that committed labels first and a classifier later would pass FREEZE with the frozen counter.

## 7. Real-tree measurements (read-only)

- Pins: `population_sha=ok pin_tree_sha=ok tests_index_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184`.
- Tests index: 305 tests, 88 tasks, `no_primary_capture=['sanitize-git-repo']`, `syntax_error=[]`, 0 with a class.
- Never-read at `BASE_TIP`: 59 texts scanned; literal-seen 19 = regex-seen 19 of 89 tasks (70 never-read); round-52 confirmed set has 8 tasks.
- `plans/round52-tasks.json` has 89 tasks, 184 capture paths; `plans/round52_c1_grader_audit.py` loaded for the control (181), not pinned.
- Not run: the ORACLE leg on the real lane (labels and classifier are off-limits to me, and the classifier file is absent).

## 8. Verification gaps (what I did not check)

- I did not verify any A1 fix. My runs of the A1 counter against my fixtures stopped at `FREEZE absent` (the A1 counter requires the eight-seat layout), so those "rejected" results are not evidence. A1's selftest case names include `forged-report-outside-wave-dir`, `forged-report-traversal`, `forged-sweep-file-twice`, `forged-report-names-task-inside-a-word`, `forged-prior-art-traversal`, which indicate coverage of D1, D3, D4, D6-ii; whether those cases fail on the right rule is unverified. A1 line 445 (`covered.add(task)`) shows no per-task row uniqueness check in my grep; I did not run a fixture for D5 against A1.
- The selftest count changed while I worked: 22 (`a34838f`), 42 (my copy at ~22:4x), 46 (copy at review end, sha `61d44a92…`); A1's text says 44. The receipt `c1-selftest.txt` now says 46. I did not determine which is current.
- I did not re-run the frozen counter's real-tree verdict (no classifier; ORACLE off-limits).
- No dependency was installed or upgraded.

## 9. Files produced

Deliverables (`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1RevCounter/`):
- `analyze.py` (read-only leg-1 and never-read measurements, url_key table)
- `mutate.py`, `mutate2.py` (mutation harnesses; see §2 for the counter source)
- `mutation_results.json`, `mutation_results_2.json`
- `verify.py`, `verify2.py` (run on both the frozen extraction and the A1 copy), `verify3.py`, `verify5.py`, `verify7.py`, `verify8.py` (frozen extraction only; fixture attacks)
- `cur_selftest.txt` (working-tree counter selftest output, `cases=46 failures=0`)
- `working-tree-counter-at-review.py` (copy of the working-tree counter, sha256 `61d44a92…cc9`; recorded for reproduction, not reviewed line by line)

Report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1RevCounter.md` (this file).

## 10. Tool and install record

- No installs, upgrades or package operations.
- `tool: write` attached "Made executable via chmod +x" to `.py` files I created in scratch without requesting it.
