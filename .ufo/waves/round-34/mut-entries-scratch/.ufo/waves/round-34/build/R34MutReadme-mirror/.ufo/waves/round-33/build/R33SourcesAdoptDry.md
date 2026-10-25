# R33SourcesAdoptDry — adoption-gate dry-run on the S103/S104 rows

Seat: leaf, lane `kengaku-shokunin`, round 33 (hyaku run 7), 2026-10-25.
Scope: run `plans/sources_adopt.py` against a **/tmp copy** of `corpus/SOURCES.md` plus the lane's
staged rows, captures and url-map; record what the gate accepts, what it refuses, and with which
exit code. Nothing was written under the lane except this report; the real registry was never a
`--registry` argument, and no git/jj command was run beyond read-only `git show`/`git status`.

Inputs actually used (sha256 of the exact bytes):

| input | path | sha256 |
|---|---|---|
| registry, pre-append | `/tmp/r33-R33SourcesAdoptDry/SOURCES.head.md` (`git show HEAD:corpus/SOURCES.md`, 95 rows) | `e2a7758002308bba275d1fb1d60a2a6a56d82659d092d0202bdd16af5030b910` |
| registry, in-flight worktree | `/tmp/r33-R33SourcesAdoptDry/SOURCES.md` (97 rows) | `c26d1a860c74532796d127698260dcaf06ae5d1591fe4846f2d53e4e49e18e74` |
| staged rows | `.ufo/waves/round-33/assimilation/append-rows.md` | `9d00d4a1f068efebf90fad4e711a12e5994257715dd6e4660b265a8a2726aace` |
| quote rows (older) | `.ufo/waves/round-33/assimilation/quotes-rows.txt` | `aada22cb49f4b84cf602fba29c7352f164a6acbd61bd59b9c38b01b5b91f027b` |
| url map | `.ufo/waves/round-33/assimilation/url-map.json` | `76c75639110cd95cf56e6cc1a5f0aa16fb129f02d9e818e9580454d15f5c9082` |
| captures dir | `.ufo/waves/round-33/assimilation/captures/` | `sha256sum -c SHA256SUMS.txt` → all 3 OK |

`append-rows.md` and `quotes.json` did not exist when this seat started (14:24); both appeared at
14:26 from a sibling seat. All acceptance numbers below are therefore taken from the **current**
lane artifacts (F-runs), with the earlier `append-block.md`/`quotes-rows.txt` runs kept as the
comparison set (R-runs). The produced append block is byte-identical to `append-rows.md`
(`cmp` → identical, sha `9d00d4a1…`).

## 1. The tool's own `--help` (verbatim)

```
$ python3 plans/sources_adopt.py --help
usage: sources_adopt.py [-h] [--selftest] [--registry REGISTRY]
                        [--package PACKAGE] [--admit-ids ADMIT_IDS]
                        [--entries ENTRIES] [--access-date ACCESS_DATE]
                        [--recheck RECHECK] [--out OUT]
                        [--quote-file QUOTE_FILE] [--artifact ARTIFACT]
                        [--url-map URL_MAP] [--attest-opened]
                        [--scope-to-admit]

Source-adoption gate for kengaku's corpus registry.

options:
  -h, --help            show this help message and exit
  --selftest
  --registry REGISTRY   live corpus/SOURCES.md
  --package PACKAGE     SOURCES.append.md to check
  --admit-ids ADMIT_IDS
                        comma-separated ids to append
  --entries ENTRIES     comma-separated admitted entry paths
  --access-date ACCESS_DATE
                        ISO date frozen for this adoption
  --recheck RECHECK     recheck value written when a staged cell is prose (a
                        cadence or a future ISO date)
  --out OUT             write the append block here
  --quote-file QUOTE_FILE
                        rows.txt whose anchor cells carry the quotes to
                        validate (needs --artifact)
  --artifact ARTIFACT   source file or directory the quotes must occur in
                        (needs --quote-file)
  --url-map URL_MAP     JSON object mapping artifact name to a URL that row
                        cites -- for a capture of a pinned file this is the
                        citation (repo or file URL), not the raw fetch URL
                        (needs --quote-file and --artifact)
  --attest-opened       assert the requested rows were opened on --access-date
                        (re-dates their opened cell)
  --scope-to-admit      refuse only the requested rows' defects (default: any
                        staged defect refuses)
EXIT=0
```

Two modes are exclusive: `--registry/--package` (row structure, id collisions, block building)
and `--quote-file/--artifact` (quote locatedness + citation binding). `--url-map` belongs only to
the second.

## 2. The requested invocation shape is refused by the tool itself

The assigned command (`--registry … --quote-file … --url-map …`) is **not a legal invocation**:

```
### V2 — literal task-specified form against the lane artifacts
$ python3 plans/sources_adopt.py --registry /tmp/r33-R33SourcesAdoptDry/SOURCES.head.md \
    --quote-file .ufo/waves/round-33/assimilation/quotes.json \
    --url-map .ufo/waves/round-33/assimilation/url-map.json
usage: sources_adopt.py [-h] [--selftest] [--registry REGISTRY] … [--scope-to-admit]
sources_adopt.py: error: --quote-file and --artifact must be given together
EXIT=2
```

Same refusal when a real rows file is supplied (R1, exit 2, identical message). The gate is a
two-pass tool: registry pass, then quote pass. The commands that actually ran are the split form.

## 3. Registry pass — the rows are admitted on the pre-append registry

```
### F1 — registry mode, pre-append copy (HEAD, 95 rows) + lane append-rows.md
$ python3 plans/sources_adopt.py --registry /tmp/r33-R33SourcesAdoptDry/SOURCES.head.md \
    --package .ufo/waves/round-33/assimilation/append-rows.md
registry=95 staged=2 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
EXIT=0
```

```
### F2 — admit dry-run, --out into /tmp only
$ python3 plans/sources_adopt.py --registry /tmp/r33-R33SourcesAdoptDry/SOURCES.head.md \
    --package .ufo/waves/round-33/assimilation/append-rows.md \
    --admit-ids S103,S104 --entries corpus/knowledge/benchmark-grader-semantics.md \
    --access-date 2026-10-25 --out /tmp/r33-R33SourcesAdoptDry/adopt-block-final.md
registry=95 staged=2 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote /tmp/r33-R33SourcesAdoptDry/adopt-block-final.md rows=2
EXIT=0
```

`cmp` of that output against `append-rows.md` → identical (`9d00d4a1…`): the gate rewrote the
caller's rows byte for byte, so `opened=2026-10-25`, `recheck=180d` and `used-by=corpus/knowledge/
benchmark-grader-semantics.md` are what an append would commit.

**The same command on today's worktree registry refuses:**

```
### F5 — in-flight working-tree registry (97 rows) + lane append rows
registry=97 staged=2 collisions=2 malformed=0 duplicates=0 defects=0 prose=0
  collisions: S103 S104
EXIT=3
```

`corpus/SOURCES.md` **already carries S103/S104 uncommitted** (`git status`: ` M corpus/SOURCES.md`;
`git show HEAD:corpus/SOURCES.md | grep -c '^| S'` → 95, worktree → 97, rows at `:118`, `:119`).
So the dry-run green is only meaningful against the pre-append bytes; after integration the gate
*must* print `collisions=2`, and that is not a row defect. **Do not append again.**

## 4. Quote pass — 8 of 8 spans locate and bind

```
### F3 — quote mode against the lane artifacts (rows + captures + authored map)
$ python3 plans/sources_adopt.py \
    --quote-file .ufo/waves/round-33/assimilation/append-rows.md \
    --artifact   .ufo/waves/round-33/assimilation/captures \
    --url-map    .ufo/waves/round-33/assimilation/url-map.json
QUOTE rows=2 spans=8 located=8 found=8 overlong=0 absent=0 malformed=0 cap=25
      artifacts=SHA256SUMS.txt,arxiv-2412.05579v2-abs.html,swebench-pro-tests-test.sh,
      toolathlon-ab-testing-evaluation-main.py,toolathlon-utils-evaluation-retry.py
      mismatch=0 unmapped=0 urlmap=url-map.json entries=3
  ok S103 words=11 at toolathlon-ab-testing-evaluation-main.py quote="def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:" bound=toolathlon-ab-testing-evaluation-main.py->https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py
  ok S103 words=5 at toolathlon-ab-testing-evaluation-main.py quote="# Validate with 0.05% tolerance" bound=…->https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py
  ok S103 words=3 at toolathlon-ab-testing-evaluation-main.py quote="validate_record_data(actual_records, expected_records, tolerance_pct=0.05)" bound=…(same URL)
  ok S103 words=11 at toolathlon-ab-testing-evaluation-main.py quote="return True  # Don't fail evaluation if we can't check logs" bound=…(same URL)
  ok S103 words=4 at toolathlon-ab-testing-evaluation-main.py quote="if not check_abtesting_logging_bucket_clean(task_launch_time, task_eval_time):" bound=…(same URL)
  ok S104 words=8 at arxiv-2412.05579v2-abs.html quote="LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods" bound=arxiv-2412.05579v2-abs.html->https://arxiv.org/abs/2412.05579
  ok S104 words=20 at arxiv-2412.05579v2-abs.html quote="This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations." bound=…(same URL)
  ok S104 words=6 at arxiv-2412.05579v2-abs.html quote="60 pages, comprehensive and continuously updated" bound=…(same URL)
EXIT=0
```

The `bound=…(same URL)` elisions are only formatting in this report; the raw run printed the full
URL on every line. Without the map (byte presence only) the same 8 spans report `ok` and `EXIT=0`
(F4). Before the artifacts were tightened, the older pair (`append-block.md` + `quotes-rows.txt`,
4 spans, repo-root citation) also passed: `rows=2 spans=4 located=4 … EXIT=0` — the current rows
are strictly stronger (8 spans, pinned-blob citation).

### Accepted / refused table

| row | gate pass | spans | words | cited URL bound | exit | verdict |
|---|---|---|---|---|---|---|
| S103 | registry (F1/F2) | 2 cells, 11 cols | — | — | 0 | `VERDICT: gate-accept` |
| S104 | registry (F1/F2) | 2 cells, 11 cols | — | — | 0 | `VERDICT: gate-accept` |
| S103 | quote (F3) | 5 | 11, 5, 3, 11, 4 (all ≤25) | pinned blob URL `…/blob/9be8d8fe…/tasks/finalpool/ab-testing/evaluation/main.py` | 0 | `VERDICT: gate-accept` |
| S104 | quote (F3) | 3 | 8, 20, 6 (all ≤25) | `https://arxiv.org/abs/2412.05579` | 0 | `VERDICT: gate-accept` |
| S103 | registry on in-flight tree (F5) | — | — | — | 3 | `VERDICT: gate-refuse` (id already present; expected, not a row fault) |

No row is refused on the pre-append bytes. Every span is ≤ 25 words, so the kill rule's
"quote >25 words is refused" clause is not triggered.

## 5. Negative controls — every refusal path was exercised, with its exit code

| id | mutation | command shape | measured | exit |
|---|---|---|---|---|
| N1 | S104 abstract span paraphrased (8 words) | quote mode + map | `absent=1`, `REFUSED S104 absent` | 7 |
| N2b | S104 span replaced by a real 30-word abstract run | quote mode + map | `overlong=1`, `located=3` (it *does* occur, still refused) | 6 |
| N3 | capture mapped to the arXiv URL it does not cite | quote mode + wrong map | `mismatch=2`, S103 both spans refused | 8 |
| N4 | empty `{}` map | quote mode | `unmapped=4`, all four refused | 9 |
| N5 | S104 row truncated to 10 cells | quote mode | `rows=1`, `malformed=1` | 4 |
| N6 | S103 duplicate row indented 2 spaces in the registry copy | registry mode | `registry=96 … collisions=1` → `S103` | 3 |
| N7 | same duplicate indented 4 spaces | registry mode | `registry=95 … collisions=0` — the 0–3-space anchor does not see it | 0 |
| N8 | `--admit-ids S105` (absent from package) | registry mode | `missing: S105` | 5 |
| N9 | `--artifact` names no path | quote mode | `problem=--artifact names no file or directory` | 2 |
| N10 | `--quote-file` unreadable | quote mode | `problem=--quote-file is unreadable` | 2 |
| P1 | row cites the pinned blob URL, map agrees | quote mode | 8/8 `ok`, bound to the blob URL | 0 |
| P2 | S103 `source` cell with no URL | quote mode | `REFUSED S103 cites-no-url` ×2 | 8 |
| — | `--selftest` | — | `SELFTEST cases=17 failed=0` | 0 |

Exit codes therefore map to: 0 accept · 2 unreadable artifact/quote file (and argparse misuse) ·
3 id collision · 4 malformed row · 5 requested id missing · 6 quote over 25 words · 7 quote absent
from the bytes · 8 capture bound to a URL the row does not cite (incl. `cites-no-url`) ·
9 capture has no map entry.

## 6. Falsifiers found (things that look green and are not)

1. **`quotes.json` is a hollow pass, and the lane now ships one.** `--quote-file` parses markdown
   `| S### |` rows (`ROW_RE`), not JSON. Handing the lane's `quotes.json` to the gate:
   ```
   $ python3 plans/sources_adopt.py --quote-file .ufo/waves/round-33/assimilation/quotes.json \
       --artifact .ufo/waves/round-33/assimilation/captures \
       --url-map .ufo/waves/round-33/assimilation/url-map.json
   QUOTE rows=0 spans=0 located=0 found=0 overlong=0 absent=0 malformed=0 cap=25 … mismatch=0 unmapped=0 entries=3
   EXIT=0
   ```
   `rows=0` + `EXIT=0` validates nothing. Any receipt that quotes this command as evidence is
   worthless. The only gate-consumable quote input is `append-rows.md`. (`quotes.json`'s own
   `gate.note` says this; the failure mode is that the tool does not enforce it.)
2. **Repo-root citations bind loosely.** `bind_failure` reads cell 1 only, so a capture answers any
   URL prefix it is mapped to. The earlier rows cited `https://github.com/hkust-nlp/Toolathlon`
   and passed (R5), even though the cited document is one file in that tree. The current
   `append-rows.md` plus `url-map.json` now cite/bind the **pinned blob URL** (F3/P1), which closes
   round-31's coarse-root gap for S103. Keep that form; do not regress to the repo root.
3. **Id-guard boundary.** A duplicate id row indented 4 spaces is invisible to both the census
   anchor and the collision guard (N7). Append rows at column 0. `--selftest` pins this as
   `four-space-not-a-row PASS`, so it is documented behaviour, not a bug to route.
4. **The gate cannot check attribution, only membership.** It proves the quoted bytes occur in a
   capture mapped to a cited URL. It does not prove the prose around the quote is true. I checked
   the two repaired claims by hand against the capture (next section) because the gate is silent
   on them.

## 7. Hand-verification of the two repaired statements (gate-blind content)

Capture `toolathlon-ab-testing-evaluation-main.py`, sha256 `3bad26b6…`, re-fetched this round from
`https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py`
→ **`cmp` identical, sha256 identical**. Same for `…/utils/evaluation/retry.py` (`db11e66e…`).
All five S103 spans therefore sit at the pinned revision, not merely in a local file.

- **Executed tolerance is 0.05, not the 0.1 default.** `:58` declares
  `tolerance_pct: float = 0.1`; `:279` is `        # Validate with 0.05% tolerance`; `:280` is
  `        validate_record_data(actual_records, expected_records, tolerance_pct=0.05)`. A grep for
  `validate_record_data(` finds the definition and this single call, so 0.05 is the operative
  value. The repaired wording ("the tolerance the sole call site passes rather than the signature
  default") is correct.
- **Fail-open exceptions vs fail-closed credential absence.** With exact indentation read from the
  capture (`:168-218`): the entire body — including
  `entries = list(client.list_entries(` at `:192` — is inside
  `if project_id_from_creds and credentials:` (`:176`, body at 12 spaces). When the service-account
  file is missing, `get_project_id_and_credentials` returns `None, None` at `:120`/`:123`, the `if`
  is skipped, the `try` block ends **without a return**, and the function returns implicit `None`.
  `validate_task_completion` then runs `if not check_abtesting_logging_bucket_clean(task_launch_time, task_eval_time):` (`:234`)
  → `not None` is true → `raise ValueError(...)` → `_check_completion` returns `(False, …)` →
  `exit(1)`. Credential absence therefore **fails the task** (fail closed). Separately,
  `except Exception as e: … return True  # Don't fail evaluation if we can't check logs`
  (`:216-218`) makes *other* caught exceptions pass (fail open). Both halves of the repaired row
  text match the bytes. Note that an earlier flattened dump of this file made the `if` body look
  unindented and would have inverted this conclusion — the indentation was read directly.
- `retry.py:44-45` is `DEFAULT_MAX_ATTEMPTS = 3` / `DEFAULT_POLL_S = 5`, as the entry says; the
  wrapper is applied to the completion check only (`grade_with_retry(_check_completion)`), not to
  the record comparison.

## 8. Risks and hand-off notes for the L1

- **Do not append twice.** The worktree registry already holds S103/S104 (`:118-119`, uncommitted).
  The gate's accept receipt is F1/F2 against `git show HEAD:corpus/SOURCES.md`.
- **Run the quote pass only with `append-rows.md`**, never with `quotes.json` (hollow pass, §6.1).
- **Do not combine `--registry` with `--quote-file`**; exit 2 is the tool refusing, not a finding.
- The lane holds two different entry byte-states: `corpus/knowledge/benchmark-grader-semantics.md`
  (`89e8530…`) and `.ufo/waves/round-33/assimilation/entry-patched.md` (`6eed24f…`). The patched
  file is the newer, longer admission text (adds the reading-basis block, `PROVINCE.md:219-220`,
  and the `corpus/README.md:276/278` citations). The gate is indifferent — it only writes `used-by`
  into the rows — so the L1 must pick and land one; C1's counter reads the `corpus/knowledge/`
  path, so that is the path that has to end up carrying the patched bytes.
- Captures are lane evidence and committable; I wrote nothing into `captures/`. Scratch lives in
  `/tmp/r33-R33SourcesAdoptDry/` (receipts `receipt-main.txt`, `receipt-final.txt`,
  `receipt-negatives*.txt`, `receipt-binding.txt`, `receipt-vacuous.txt`), well under 60 MB.
- No tool was installed or upgraded this round (nothing was needed; `python3` 3.14 from the host).

## 9. What the main agent should run at the tip

```
python3 plans/sources_adopt.py --registry /tmp/<pre-append copy> --package .ufo/waves/round-33/assimilation/append-rows.md
python3 plans/sources_adopt.py --quote-file .ufo/waves/round-33/assimilation/append-rows.md \
    --artifact .ufo/waves/round-33/assimilation/captures --url-map .ufo/waves/round-33/assimilation/url-map.json
python3 plans/sources_adopt.py --selftest
python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census
```
Expected: `collisions=0 … EXIT=0` on the pre-append copy; `rows=2 spans=8 located=8 … EXIT=0`;
`cases=17 failed=0`; then C1's own counter. On the post-append tree the first command will report
`collisions=2` — that is the duplicate-append guard working, not a regression.
