# C1MutCounter — wave-1 mutation probe of the frozen counter's `--selftest` (R53-C1)

Seat: `C1MutCounter` (mutation-tester, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, base `1373b6c` (claims `a34838f`). Target: `plans/round53_c1_triage.py`, sha256 `1ba1a800…931bf` (identical at `a34838f` and `1373b6c`). Lane tree not edited; the proposed kill cases are a diff, not a landed change.

## Result

- The frozen 22-case `--selftest` kills **25 of 81** single-edit mutants (31%). **56 survive.** The null mutant (N00) is not killed, as required.
- A 47-case kill-case diff (`survivor-kill-cases.diff`, verified to patch pristine byte-for-byte to `triage_ext.py`, and to pass 69/69 on pristine) kills **77 of 81**. The four survivors (P04, P09, P10, A18) are verdict-equivalent; reasons below.
- Three findings go beyond the mutants and are measured on fixtures (details below): **(F1)** a joint edit of the classifier and its recorded digest in a later commit still passes FREEZE; **(F2)** editing `author_seats` after the freeze flips a labeler-is-author rejection into a decided label while FREEZE stays `ok=True`; **(F4)** the selftest never executes the real CFG constants, so pins and limits are latent until the real tree lands.
- This seat does not admit or reject C1. It reports that the frozen selftest is weak, that F1–F2 are gaps in the predicate's trust model, and what would close them.

## Scope, blindness, writes

- Read: the claims file in full; the counter in full; `plans/round53_c1_extract.py` (the index builder the selftest imports). I did **not** open any label file, any `C1Label*` directory, any `C1ExecClassifier*` path, or any other label seat's file. I ran one existence check (`ls`) on `plans/round53_c1_classify.py` in my lane clone: it is absent at `1373b6c`. I read no classifier content and ran no classifier.
- Writes: scratch under `/fast/scratch/hyaku/kengaku-r53/C1MutCounter/` (lane clone, probe clone, fixtures; removed before yield). Deliverables under `.ufo/waves/round-53/w1/C1MutCounter/`. Fleet repo: read-only (`rev-parse`, `status`, `log`, and `clone --shared` as the source). No `git commit/add/stash/checkout/reset`. Fixtures ran `git -C "$D"`, with `$D` from `mktemp -d -p` under scratch.
- Tools: none installed or upgraded. Only the Python stdlib and `patch` were used.
- `tool: read` returned "Path … not found" for `/fast/scratch/hyaku/kengaku-r53/C1MutCounter/lane/plans/round53_c1_triage.py` although `wc -l` on the same absolute path succeeded; I read a copy at another path instead.

## Commands run (exact, in order)

1. `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/C1MutCounter/lane && git -C lane rev-parse --show-toplevel` → the lane scratch path.
2. `git show a34838f:plans/round53_c1_triage.py | sha256sum` and `sha256sum plans/round53_c1_triage.py` → both `1ba1a800774af9b78cd26079ea504b5b3bc419cfd185a49706072ad165b931bf`.
3. `TMPDIR=…/tmp python3 plans/round53_c1_triage.py --selftest` → rc 0, `SELFTEST cases=22 failures=0`, 1.4 s.
4. `python3 mutate.py` (frozen base) → `TOTAL mutants=81 killed=25 survived=56 restored_sha_ok=True`; log `work/run2.log`.
5. `python3 make_ext.py` → `triage_ext.py` (797 lines) and `survivor-kill-cases.diff` (232 diff lines); then the file was copied into the lane's `plans/` and `python3 plans/round53_c1_triage.py --selftest` run there (lane restored to pristine afterwards) → rc 0, `cases=69 failures=0`, 47 new case lines.
6. `BASE_FILE=…/triage_ext.py python3 mutate.py` → `TOTAL mutants=81 killed=77 survived=4 restored_sha_ok=True`; null not killed. Log `work/run_ext2.log`.
7. `patch -s` of `survivor-kill-cases.diff` onto a copy of pristine → `cmp` with `triage_ext.py` identical.
8. `git clone -q --shared … probe` (clean clone, `rev-parse --show-toplevel` checked) and `python3 probe_real.py` → 20 real-tree probes via `python3 plans/round53_c1_triage.py --lane .` (the 12 CONST mutants and 8 PINS/FREEZE/CONFIRM mutants).
9. Fixture experiments F1 and F2 (`mktemp -d -p …`, `git -C "$D"`, fixture classifier stub, freeze and labels committed, later edit committed); see F1, F2.

Real-tree base on the clean clone (rc 1, the expected pre-classifier state):
`PINS population_sha=ok pin_tree_sha=ok tests_index_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184`, `FREEZE absent freeze=False classifier=False labels=False`, `ORACLE not evaluable …`, `CONFIRM new_confirmed=0`, `PRIOR-ART rows=0`, `PREDICATE R53-C1 fail`.

## Method

- Each mutant replaces one substring that occurs exactly once on one line of the frozen file (asserted), compiles, runs `--selftest` under a fresh `TMPDIR`, and is restored and sha-checked. Line numbers are from `1373b6c`; the extension adds code only after line 547, so mutant lines are unchanged in `triage_ext.py`.
- Kill: selftest rc ≠ 0, or its `cases=… failures=…` line differs from the base, or the selftest raises. Kills by raising are marked `crash`.
- Equivalence is argued from the code and confirmed by no kill under the extended suite. It is not machine-proved.
- Real-tree probe: each CONST/PINS mutant run through the real CLI on the clean clone; "visible" means stdout or rc differs from base.
- The mutant count (81) exceeds the "about 30" requested so every clause named in the spec has at least one row. All requested classes are present.

## Findings

**F1 (measured) — a joint classifier-plus-digest edit passes FREEZE.** Fixture: freeze committed with `classifier_sha256` and `author_seats`; labels committed later; then, in a third commit, the classifier was rewritten and `classifier_sha256` in the freeze JSON was re-recorded. `leg_freeze` → `ok=True`, `FREEZE classifier_sha=ok order=freeze-before-labels`. The "classifier-edited-after-freeze" case only catches a naive edit that leaves the digest stale. The predicate's trust in the freeze JSON is not pinned by digest and the order check only inspects the first-add commit, so the "never edited after the freeze commit" rule is not enforced. The frozen counter has no pin on `plans/round53-c1-freeze.json` (`leg_freeze` reads it from the working tree, lines 121–141).

**F2 (measured) — `author_seats` is editable after the freeze.** Same fixture, with labels by `AuthorSeat` and `L3`. Before the edit: `freeze_ok=True`, `authors=['AuthorSeat']`, `labels_bad=1`. After a later commit that sets `author_seats` to `['Other']`: `freeze_ok=True`, `order=freeze-before-labels`, `authors=['Other']`, `labels_bad=0`, `decided=1`. The classifier author's own label is accepted. The frozen fixture `forged-labeler-is-author` only checks the unedited list.

**F3 (reading, not executed) — the ORACLE-CONTROL classifier is unpinned.** `r52_classes` loads `plans/round52_c1_grader_audit.py` from the working tree (line 181). `leg_pins` digests only `round52-tasks.json`, the pin tree, `tests-index.json`, and the captures. The control threshold (`ctl_ok`, lines 197–203) therefore depends on an unpinned file. The claim's sentence "every input the predicate trusts is pinned by a digest constant or by git history" does not hold for this file.

**F4 (measured) — the selftest never executes the real CFG.** The selftest rebinds `cfg` to fixture values (`POP_SHA`, `PIN_TREE_SHA`, `TESTS_INDEX_SHA`, `TESTS_TOTAL=3`, `CAPTURES_EXPECTED=2`, `EXCLUDED_*`, `CONFIRM_MIN=1`, `URL_MIN=1`, `BASE_TIP`). Constant mutants C01–C03, C08, C09, C12 therefore all survive the frozen suite by construction. The real-tree probe shows which are visible today:

| constant mutant | real-tree visible at `1373b6c` |
|---|---|
| C01 `POP_SHA` digit | yes (`population_sha=BAD`) |
| C12 `EXCLUDED_BLOB` digit | yes (`excluded_blob=BAD`) |
| C02 `TESTS_TOTAL`, C03 `CAPTURES_EXPECTED`, C08 `CONFIRM_MIN`, C09 `URL_MIN` | no: ORACLE/PRIOR-ART lines are not printed until the classifier and confirmations land |

The kill-case diff adds `ext-frozen-constants`, which compares the module constants to frozen literals and kills all of them.

**F5 — advertised clauses with no fixture (56 frozen survivors, grouped).**
- PINS: tests-index digest clause (P11); excluded capture present (P12).
- FREEZE: ancestry check (F04) and the order clause (F05), with no fixture where labels precede the freeze; the author-list non-empty clause at leg level (F06, equivalent at verdict level).
- LABELS: three labelers (L01); domain check for `X` labels (L03); disagreeing pair decided (L04); missing row (L05, killed only by a crash); labelers not a list (L06); extra row (O05, killed); bad-row clause (O07, needs a 100-test fixture).
- ORACLE: unclassified (O06, needs scale); tests-count clause (O08); control clause in the leg (O11, killed by a direct call); boundaries `dis<=lim` (O09), contested `<=` (O10), denominator (O12); threshold values C04–C07 (scale).
- CONFIRM: never-read blocklist (K12, K13); candidacy (K02); duplicate (K03); reader prefix (K06) and reader-in-path (K07); def-line span (K09); task/test-id consistency (K10); quote-length 19/20 (C10, C11, K05).
- PRIOR-ART: task-confirmed (A01); verdict domain (A02); URL shape (A04); word bounds 7/8/26 (A05–A07); known-row naming (A09, A10); sweep count (A11); sweep task-name and test-name (A12, A13); fetch prefix (A14); one rejected row (A17); whole sweep branch (A19, already killed).

**F6 — one kill is a crash, not a verdict.** L05 (missing label row) is killed only because the selftest raises when the missing-row branch is removed. The extension adds `ext-label-row-missing`, which exercises the branch.

## The four equivalent survivors

- **P04** `if pop_ok or pin_ok:` — `ok` (line 106) still requires `pop_ok and pin_ok`, so the verdict is unchanged; only PINS detail text differs.
- **P09** drop `and absent == 0` — with `match == CAPTURES_EXPECTED`, `bad == 0`, and `files == EXPECTED+1` (all still checked), `absent` is 0 identically.
- **P10** `match >= CAPTURES_EXPECTED` — `match` is at most the number of non-excluded captures, which equals `EXPECTED`; `bad==0` and `absent==0` remain, so the value is the same.
- **A18** drop `bool(confirmed)` — with no confirmed task every prior-art row is rejected (`task-not-confirmed`), so `urls>=URL_MIN` (≥1) and `not rej` already fail.

## Kill cases (the diff) and what they are

`survivor-kill-cases.diff` is a diff against `plans/round53_c1_triage.py`. It adds, inside `selftest()`: a reversed-history case in a temp repo where the labels are first committed before the freeze file (`ext-freeze-after-labels`); leg-level FREEZE checks for the order clause and for an empty author list (`ext-freeze-leg-order-clause`, `ext-freeze-leg-empty-authors`); label cases; confirm and prior-art boundary and rejection cases; a 100-test scale fixture for O06, O07, O09, O10, O12, C04–C07 (cases `ext-scale-*`); a direct `leg_oracle` call for the control clause; base-commit variants for never-read (`ext-candidate-seen-in-base-excluded`, `ext-candidate-r52-confirmed-excluded`); and `ext-frozen-constants`. Each case was run against the mutants: all 77 non-equivalent mutants fail at least one of the new or old cases (`mutants.md`, column "+kill cases").

Landing these changes the frozen counter's bytes. The claims' amendment rule applies (a dated entry, before-state re-derivable), or they can live in a separate control script that imports the frozen counter. I did not apply them.

## Recommendation for the L1 (not acted on)

1. Pin `plans/round53-c1-freeze.json` by digest in the counter (or pin `classifier_sha256` and the author list as constants). This closes F1 and F2.
2. Pin or git-check `plans/round52_c1_grader_audit.py` (F3).
3. Land the kill cases (or the frozen-constants tripwire) so the selftest executes the real constants (F4).

## Mutation table

Killed/survived per suite, with the case that kills. `frozen suite` = the frozen 22-case selftest; `+kill cases` = with the diff; `real-tree` = the probe on the clean clone, visible or not at the base tip.

| id | group | line | mutation (old → new) | what it is | frozen suite | +kill cases | real-tree |
|---|---|---|---|---|---|---|---|
| P01 | PINS | 81 | `== cfg["POP_SHA"]` → `!= cfg["POP_SHA"]` | pop digest comparison inverted | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (48 FAIL) | y |
| P02 | PINS | 82 | `== cfg["PIN_TREE_SHA"]` → `!= cfg["PIN_TREE_SHA"]` | pin-tree digest comparison inverted | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (47 FAIL) | — |
| P03 | PINS | 83 | `== cfg["TESTS_INDEX_SHA"]` → `!= cfg["TESTS_INDEX_SHA"]` | tests-index digest comparison inverted | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (47 FAIL) | — |
| P04 | PINS | 86 | `if pop_ok and pin_ok:` → `if pop_ok or pin_ok:` | population walk gated by OR | n | n (equivalent) | — |
| P05 | PINS | 94 | `if p == cfg["EXCLUDED_PATH"]:` → `if p != cfg["EXCLUDED_PATH"]:` | excluded path test inverted | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (47 FAIL) | — |
| P06 | PINS | 95 | `(not f.exists())` → `(f.exists())` | excluded capture must be absent: clause dropped | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (47 FAIL) | — |
| P07 | PINS | 97 | `if not f.is_file():` → `if f.is_file():` | absent capture counter inverted | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (47 FAIL) | — |
| P08 | PINS | 99 | `== blobs.get(p):` → `!= blobs.get(p):` | blob-SHA1 match inverted | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (46 FAIL) | y |
| P09 | PINS | 106 | ` and absent == 0` → (deleted) | absent==0 clause dropped (equivalent given blob_bad/match) | n | n (equivalent) | — |
| P10 | PINS | 106 | `match == cfg["CAPTURES_EXPECTED"]` → `match >= cfg["CAPTURES_EXPECTED"]` | captures equality relaxed to >= (equivalent given files==EXPECTED+1) | n | n (equivalent) | — |
| P11 | PINS | 106 | `pop_ok and pin_ok and idx_ok and` → `pop_ok and pin_ok and` | tests-index digest clause dropped from PINS verdict | n | y — ext-tests-index-digest (1 FAIL) | n |
| P12 | PINS | 107 | `exc_ok and ` → (deleted) | excluded-blob clause dropped from PINS verdict | n | y — ext-excluded-capture-present (1 FAIL) | n |
| P13 | PINS | 107 | `+ 1)` → `+ 0)` | population count off by one (EXPECTED+0) | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (46 FAIL) | — |
| F01 | FREEZE | 131 | `sha256_file(clf) == d.get` → `sha256_file(clf) != d.get` | classifier digest comparison inverted | y — genuine-fixture-passes | y — genuine-fixture-passes (7 FAIL) | — |
| F02 | FREEZE | 134 | `if c_fz and c_lab and c_fz != c_lab:` → `if c_fz and c_lab and c_fz == c_lab:` | freeze-before-labels order test inverted | y — genuine-fixture-passes | y — genuine-fixture-passes (6 FAIL) | n |
| F03 | FREEZE | 135 | `)[0] == 0` → `)[0] != 0` | is-ancestor test inverted | y — genuine-fixture-passes | y — genuine-fixture-passes (8 FAIL) | — |
| F04 | FREEZE | 135 | `order = git(lane, "merge-base", "--is-ancestor", c_fz, c_lab)[0] == 0` → `order = True` | ancestry check dropped | n | y — ext-freeze-after-labels (2 FAIL) | n |
| F05 | FREEZE | 137 | `ok = sha_ok and order and` → `ok = sha_ok and` | freeze ordering clause dropped from FREEZE verdict | n | y — ext-freeze-leg-order-clause (1 FAIL) | — |
| F06 | FREEZE | 137 | ` and bool(info["authors"])` → (deleted) | non-empty author_seats clause dropped (equivalent: verdict gates on authors at L374) | n | y — ext-freeze-leg-empty-authors (1 FAIL) | — |
| L01 | LABELS | 150 | `len(set(r["labelers"])) != 2` → `len(set(r["labelers"])) < 2` | two-distinct-labelers test relaxed to <2 | n | y — ext-labelers-three-distinct (1 FAIL) | — |
| L02 | LABELS | 152 | ` or set(r["labelers"]) & authors` → (deleted) | labeler-is-author rejection branch deleted | y — forged-labeler-is-author | y — forged-labeler-is-author (1 FAIL) | — |
| L03 | LABELS | 152 | ` or any(x not in ("Y", "N", "U") for x in r["labels"])` → (deleted) | label-domain rejection branch deleted | n | y — ext-label-domain-X (2 FAIL) | — |
| L04 | LABELS | 156 | `if a == b and a in ("Y", "N"):` → `if a in ("Y", "N"):` | agreement requirement dropped: disagreeing pair decided | n | y — ext-label-disagree-contested (3 FAIL) | — |
| L05 | LABELS | 150 | `(not isinstance(r, dict) or ` → `(` | missing-row (non-dict) rejection branch deleted | n | y — traceback (0 FAIL) | — |
| L06 | LABELS | 150 | `not isinstance(r.get("labelers"), list) or ` → (deleted) | labelers-is-list rejection branch deleted | n | y — ext-labelers-not-a-list (1 FAIL) | — |
| O01 | ORACLE | 198 | `if (v2[t] == "P1") != (y == "Y")` → `if (v2[t] == "P1") == (y == "Y")` | v2 disagreement count inverted | y — genuine-fixture-passes | y — genuine-fixture-passes (10 FAIL) | — |
| O02 | ORACLE | 199 | `if (r52[t] == "P1") != (y == "Y")` → `if (r52[t] == "P1") == (y == "Y")` | r52 control disagreement count inverted | y — genuine-fixture-passes | y — genuine-fixture-passes (10 FAIL) | — |
| O03 | ORACLE | 203 | `dis52 >= CONTROL_RATIO * max(dis, 1)` → `dis52 > CONTROL_RATIO * max(dis, 1)` | control ratio >= relaxed to > | y — genuine-fixture-passes | y — genuine-fixture-passes (6 FAIL) | — |
| O04 | ORACLE | 203 | ` and dis52 >= CONTROL_MIN` → (deleted) | control minimum clause dropped | y — tiny-fixture-control-vacuous | y — tiny-fixture-control-vacuous (2 FAIL) | — |
| O05 | ORACLE | 204 | `and not extra and` → `and` | extra label-row clause dropped | n | y — ext-extra-label-row (1 FAIL) | — |
| O06 | ORACLE | 204 | `and not uncl and` → `and` | unclassified=0 clause dropped | n | y — ext-scale-unclassified-10 (1 FAIL) | — |
| O07 | ORACLE | 204 | `ok = (n == cfg["TESTS_TOTAL"] and not bad and` → `ok = (n == cfg["TESTS_TOTAL"] and` | bad-label-row clause dropped | n | y — ext-scale-bad-label-row (1 FAIL) | — |
| O08 | ORACLE | 204 | `n == cfg["TESTS_TOTAL"] and ` → (deleted) | tests-count clause dropped (equivalent given TESTS_INDEX_SHA pin) | n | y — ext-tests-total-mismatch (1 FAIL) | — |
| O09 | ORACLE | 205 | `and dis <= lim` → `and dis < lim` | disagreement limit <= relaxed to < (boundary) | n | y — ext-scale-disagree-at-limit-3 (1 FAIL) | — |
| O10 | ORACLE | 205 | `len(contested) <= ORACLE_MAX_CONTESTED * n` → `len(contested) < ORACLE_MAX_CONTESTED * n` | contested limit <= relaxed to < (boundary) | n | y — ext-scale-contested-at-limit-15 (1 FAIL) | — |
| O11 | ORACLE | 205 | `and ctl_ok)` → `)` | ORACLE-CONTROL clause dropped from verdict | n | y — ext-oracle-control-clause-in-leg (2 FAIL) | — |
| O12 | ORACLE | 202 | `lim = ORACLE_MAX_DISAGREE * max(1, len(decided))` → `lim = ORACLE_MAX_DISAGREE * max(1, len(ids))` | disagreement denominator: decided -> all tests | n | y — ext-scale-disagree-3-of-85-decided (1 FAIL) | — |
| K01 | CONFIRM | 266 | `if r.get("confirmed") is not True:` → `if not r.get("confirmed"):` | confirmed weakened from `is not True` to falsy | y — forged-confirmed-string | y — forged-confirmed-string (1 FAIL) | — |
| K02 | CONFIRM | 270 | `elif r["task"] not in cand or tid not in {x["id"] for x in cand[r["task"]]}:` → `elif False:` | never-read / v2-P1 candidacy check deleted | n | y — ext-candidate-v2-P0-rejected (3 FAIL) | — |
| K03 | CONFIRM | 272 | `elif r["task"] in seen_tasks:` → `elif False:` | duplicate-task rejection deleted | n | y — ext-duplicate-task-row (1 FAIL) | — |
| K04 | CONFIRM | 274 | `< QUOTE_MIN_CHARS or norm(r["quote"]) not in span:` → `< QUOTE_MIN_CHARS:` | quote-inside-test-span check deleted | y — forged-quote-outside-span | y — forged-quote-outside-span (1 FAIL) | — |
| K05 | CONFIRM | 274 | `< QUOTE_MIN_CHARS or` → `<= QUOTE_MIN_CHARS or` | quote length >= 20 relaxed to > 20 (boundary) | n | y — ext-quote-exactly-20-chars (1 FAIL) | n |
| K06 | CONFIRM | 276 | ` or r["reader"].startswith("KengakuR53")` → (deleted) | KengakuR53 reader rejection deleted | n | y — ext-reader-KengakuR53-prefix (1 FAIL) | — |
| K07 | CONFIRM | 278 | ` or r["reader"] not in str(rep)` → (deleted) | reader-name-in-report-path check deleted | n | y — ext-reader-not-in-report-path (1 FAIL) | — |
| K08 | CONFIRM | 280 | `elif r["task"] not in rep.read_text(encoding="utf-8", errors="replace"):` → `elif False:` | report-names-task check deleted | y — forged-report-names-other-task | y — forged-report-names-other-task (1 FAIL) | — |
| K09 | CONFIRM | 265 | `src[t["lineno"] - 1:t["end_lineno"]]` → `src[t["lineno"]:t["end_lineno"]]` | test span drops its def line | n | y — ext-quote-spans-def-line (1 FAIL) | — |
| K10 | CONFIRM | 268 | `elif t is None or t["task"] != r.get("task"):` → `elif t is None:` | test_id/task consistency check deleted (reason text changes only) | n | y — ext-task-testid-mismatch (1 FAIL) | — |
| K11 | CONFIRM | 289 | `ok = len(good) >= cfg["CONFIRM_MIN"]` → `ok = len(good) > cfg["CONFIRM_MIN"]` | CONFIRM minimum >= relaxed to > (cfg-level, fixture overrides) | y — genuine-fixture-passes | y — genuine-fixture-passes (6 FAIL) | n |
| A01 | PRIOR-ART | 324 | `if task not in confirmed:` → `if False:` | task-confirmed check deleted in prior-art | n | y — ext-prior-art-unconfirmed-task-row (1 FAIL) | — |
| A02 | PRIOR-ART | 326 | `elif v not in ("phenomenon-new", "phenomenon-known"):` → `elif False:` | verdict-domain check deleted | n | y — ext-prior-art-bad-verdict (1 FAIL) | — |
| A03 | PRIOR-ART | 328 | ` or "example.org" in r["url"]` → (deleted) | example.org rejection deleted (sole-check route) | y — forged-prior-art-example | y — forged-prior-art-example (1 FAIL) | — |
| A04 | PRIOR-ART | 328 | `elif not re.match(r"https?://[^/\s]+\.[^/\s]+/", str(r.get("url", "")) + "/") or` → `elif` | URL shape check deleted | n | y — ext-prior-art-url-not-a-url (2 FAIL) | — |
| A05 | PRIOR-ART | 335 | `8 <= len(q.split()) <= 25` → `7 <= len(q.split()) <= 25` | quote word-count lower bound 8 -> 7 | n | y — ext-quote-7-words-rejected (1 FAIL) | — |
| A06 | PRIOR-ART | 335 | `8 <= len(q.split()) <= 25` → `8 < len(q.split()) <= 25` | quote word-count lower bound <= swapped to < (8 excluded) | n | y — ext-quote-8-words-accepted (1 FAIL) | — |
| A07 | PRIOR-ART | 335 | `len(q.split()) <= 25` → `len(q.split()) <= 26` | quote word-count upper bound 25 -> 26 | n | y — ext-quote-26-words-rejected (1 FAIL) | — |
| A08 | PRIOR-ART | 335 | ` or q not in norm(text):` → `:` | quote-in-archive check deleted | y — forged-prior-art-quote | y — forged-prior-art-quote (1 FAIL) | — |
| A09 | PRIOR-ART | 337 | ` and task not in text:` → `:` | known-row: task-name-in-fetch alternative deleted | n | y — ext-known-names-task-not-tests (1 FAIL) | — |
| A10 | PRIOR-ART | 337 | `elif v == "phenomenon-known" and not any(n in text for n in tests_of.get(task, [])) and task not in text:` → `elif False:` | known-row naming check deleted | n | y — ext-known-names-neither-rejected (1 FAIL) | — |
| A11 | PRIOR-ART | 341 | `if not isinstance(sw, list) or len(sw) < 2:` → `if not isinstance(sw, list) or len(sw) < 1:` | new-row sweep minimum 2 -> 1 | n | y — ext-new-one-sweep-rejected (1 FAIL) | — |
| A12 | PRIOR-ART | 346 | `if st is None or task in st or any(` → `if st is None or any(` | sweep: task-name check deleted | n | y — ext-sweep-names-task-rejected (1 FAIL) | — |
| A13 | PRIOR-ART | 346 | ` or any(n in st for n in tests_of.get(task, [])):` → `:` | sweep: test-name check deleted | n | y — ext-sweep-names-test-rejected (1 FAIL) | — |
| A14 | PRIOR-ART | 314 | `if not str(r.get(key, "")).startswith(f"{RUN_DIR}/fetched/") or not f.is_file():` → `if not f.is_file():` | fetch-path-under-fetched/ check deleted | n | y — ext-fetch-outside-fetched-dir (1 FAIL) | — |
| A15 | PRIOR-ART | 316 | `if sha256_file(f) != r.get(key + "_sha256"):` → `if sha256_file(f) == r.get(key + "_sha256"):` | fetch digest comparison inverted | y — genuine-fixture-passes | y — genuine-fixture-passes (15 FAIL) | — |
| A16 | PRIOR-ART | 358 | `and new >= 1 and not rej` → `and new >= 0 and not rej` | new>=1 score rule relaxed to >=0 | y — known-only-fails-score-rule | y — known-only-fails-score-rule (1 FAIL) | — |
| A17 | PRIOR-ART | 358 | ` and not rej` → (deleted) | one-rejected-row rule deleted | n | y — ext-prior-art-unconfirmed-task-row (4 FAIL) | — |
| A18 | PRIOR-ART | 358 | `bool(confirmed) and ` → (deleted) | non-empty confirmed clause dropped (equivalent: rej/covered gates) | n | n (equivalent) | — |
| C01 | CONST | 29 | `0230b68c666c` → `0230b68d666c` | POP_SHA first digits (CFG; selftest overrides cfg) | n | y — ext-frozen-constants (1 FAIL) | y |
| C02 | CONST | 32 | `TESTS_TOTAL = 305` → `TESTS_TOTAL = 306` | TESTS_TOTAL 305->306 (CFG; selftest overrides) | n | y — ext-frozen-constants (1 FAIL) | n |
| C03 | CONST | 33 | `CAPTURES_EXPECTED = 183` → `CAPTURES_EXPECTED = 182` | CAPTURES_EXPECTED 183->182 (CFG; selftest overrides) | n | y — ext-frozen-constants (1 FAIL) | n |
| C04 | CONST | 37 | `ORACLE_MAX_DISAGREE = 0.03` → `ORACLE_MAX_DISAGREE = 0.5` | ORACLE_MAX_DISAGREE 0.03->0.5 | n | y — ext-scale-disagree-over-limit-4 (3 FAIL) | n |
| C05 | CONST | 38 | `ORACLE_MAX_CONTESTED = 0.15` → `ORACLE_MAX_CONTESTED = 0.5` | ORACLE_MAX_CONTESTED 0.15->0.5 | n | y — ext-scale-contested-over-limit-16 (2 FAIL) | n |
| C06 | CONST | 39 | `CONTROL_RATIO = 2` → `CONTROL_RATIO = 1` | CONTROL_RATIO 2->1 | n | y — ext-scale-control-ratio-1-vs-2 (2 FAIL) | n |
| C07 | CONST | 40 | `CONTROL_MIN = 10` → `CONTROL_MIN = 11` | CONTROL_MIN 10->11 (selftest rebinds to 1 except one case) | n | y — ext-scale-control-min-at-10 (2 FAIL) | n |
| C08 | CONST | 41 | `CONFIRM_MIN = 3` → `CONFIRM_MIN = 2` | CONFIRM_MIN 3->2 (CFG; selftest overrides) | n | y — ext-frozen-constants (1 FAIL) | n |
| C09 | CONST | 42 | `URL_MIN = 3` → `URL_MIN = 2` | URL_MIN 3->2 (CFG; selftest overrides) | n | y — ext-frozen-constants (1 FAIL) | n |
| C10 | CONST | 43 | `QUOTE_MIN_CHARS = 20` → `QUOTE_MIN_CHARS = 19` | QUOTE_MIN_CHARS 20->19 | n | y — ext-quote-19-chars-rejected (2 FAIL) | n |
| C11 | CONST | 43 | `QUOTE_MIN_CHARS = 20` → `QUOTE_MIN_CHARS = 21` | QUOTE_MIN_CHARS 20->21 | n | y — ext-quote-exactly-20-chars (2 FAIL) | n |
| C12 | CONST | 35 | `EXCLUDED_BLOB = "3269e74e` → `EXCLUDED_BLOB = "3269e74f` | EXCLUDED_BLOB first digits (CFG; selftest overrides) | n | y — ext-frozen-constants (1 FAIL) | y |
| K12 | CONFIRM | 240 | ` and not seen_before(t["task"], texts)` → (deleted) | never-read check: task-seen-in-base-texts exclusion deleted | n | y — ext-candidate-seen-in-base-excluded (1 FAIL) | — |
| K13 | CONFIRM | 240 | ` and t["task"] not in r52_conf` → (deleted) | never-read check: round-52-confirmed exclusion deleted | n | y — ext-candidate-r52-confirmed-excluded (1 FAIL) | — |
| A19 | PRIOR-ART | 339 | `elif v == "phenomenon-new":` → `elif False:` | whole sweep check (phenomenon-new) deleted | y — forged-new-without-sweep | y — forged-new-without-sweep (4 FAIL) | — |

Files (absolute): /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1MutCounter/mutants.md · /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1MutCounter/results-pristine-suite.json · /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1MutCounter/results-kill-cases-suite.json · /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1MutCounter/probe-real-tree.json · /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1MutCounter/survivor-kill-cases.diff · /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1MutCounter/triage_ext.py · /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1MutCounter/selftest-pristine.out · /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1MutCounter/selftest-with-kill-cases.out · /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1MutCounter/mutate.py · /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1MutCounter/make_ext.py · /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1MutCounter/probe_real.py. The scripts reference the scratch tree (removed at exit); copies are kept here.

Report contract: this file is the seat report; the table lists every mutant with its killing case.
