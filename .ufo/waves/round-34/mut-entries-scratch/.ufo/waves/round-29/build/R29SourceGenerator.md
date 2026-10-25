# R29 source opening — S070 primary generator behavior/order

**Seat:** `KengakuR28.R29SourceGenerator-2` (actual writer: same)
**Report:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/build/R29SourceGenerator.md`
**Claim reference:** C1 in `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-29-claims.md`; manifest `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/manifest.json` sha256 `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`.
**Scope:** live opening of the pinned upstream generator plus one byte-retaining fetch, and a proposed S070 row. No production edit, no `corpus/SOURCES.md` write, no upstream import/execution, no `browser_env/env_config.py` fetch, no host environment/credential/auth-state read, no endpoint beyond the one pinned raw URL.
**Tool installs/updates:** none.

## Godspeed axes this seat moves

| Axis | Question | This seat's move |
|---|---|---|
| Novelty | Does the row add the generator step that S061/S068 do not cover? | Adds the pinned script's own ordered transformation and positional filenames, not another raw-task-content row. |
| Fidelity | Do the live bytes equal the frozen fixture? | URL read and byte-retaining fetch; the retained sha256 and `cmp` both match the fixture and manifest pin. |
| Safety | Is the inert wildcard import kept inert? | The script was read as text only; `env_config` was never fetched, imported, or executed. |
| Observability | Are the claims line-located and counted? | Exact URL, date, lines 8–23, a ≤25-word located quote, programmatic word count, retained byte hash. |

## Opening record (observed)

| Field | Observed value |
|---|---|
| URL | `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/scripts/generate_test_data.py` |
| Revision | `dce04686a56253aefba7b18a4fa0937cf1dc987b` |
| Accessed | 2026-10-21 |
| Accesses | URL opened once with the read tool (text/plain) and fetched once with `curl -fsSL` to retain bytes; only the retained curl bytes were hashed and compared. No second fetch was used for the census. |
| Content type (read tool) | `text/plain` |
| Retained length/hash (curl bytes) | 838 bytes; sha256 `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` |
| Retained bytes | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29SourceGenerator-2/generate_test_data.upstream.py` |
| Local pinned fixture | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py`, 838 bytes, same sha256; `cmp` → `IDENTICAL` |
| Manifest pin | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/manifest.json` sha256 equals `f6390b92…bf87`; its `replacement_order` lists `GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP`, matching the six RHS names at source lines 11–16 in the same order |
| Source extent | 27 lines; `wc -w` on the whole file = 87 |

### Located quote (exact, lines 11–16)

```text
    raw = raw.replace("__GITLAB__", GITLAB)
    raw = raw.replace("__REDDIT__", REDDIT)
    raw = raw.replace("__SHOPPING__", SHOPPING)
    raw = raw.replace("__SHOPPING_ADMIN__", SHOPPING_ADMIN)
    raw = raw.replace("__WIKIPEDIA__", WIKIPEDIA)
    raw = raw.replace("__MAP__", MAP)
```

- Location: `scripts/generate_test_data.py:11–16` (six contiguous source lines).
- **Actual programmatic word count:** `24`, computed as `len(quote.split())` over the exact block; each line contributes 4 whitespace-delimited words.
- Method boundary: this is a whitespace `str.split()` count, not a Python-token or AST-token count. A tokenizer count differs and is not claimed equivalent.

### Observed source sequence (static reading, lines 8–23)

| Lines | Observed |
|---|---|
| 9–10 | Opens `config_files/test.raw.json` in text mode and reads the whole file into `raw`. |
| 11–16 | Six sequential `raw.replace("__TOKEN__", NAME)` assignments in the order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP. |
| 17–18 | Writes the replaced text to `config_files/test.json` before any parse. |
| 20 | Calls `json.loads(raw)` on the replaced text; no repair branch is present in the 27-line file. |
| 21–23 | `for idx, item in enumerate(data):` writes `config_files/{idx}.json` with `json.dump(item, f, indent=2)`; the filename is the list position, not `item["task_id"]`. |
| 26–27 | Guarded `main()` entry point; the module is a script, not an import to execute. |
| 5 | `from browser_env.env_config import *` supplies replacement values from outside this lane; not read, imported, or executed. |

## Programmatic receipts

Commands were run from the lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin` unless the working directory is stated. Outputs below are observed, not inferred.

```text
$ cd .ufo/waves/round-29/scratch/KengakuR28.R29SourceGenerator-2
$ curl -fsSL --max-time 30 -o generate_test_data.upstream.py \
    'https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/scripts/generate_test_data.py'
# command chain completed; retained file hashed below

$ sha256sum generate_test_data.upstream.py
45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd  generate_test_data.upstream.py

$ wc -c -l -w generate_test_data.upstream.py
 27  87 838 generate_test_data.upstream.py

$ cmp generate_test_data.upstream.py /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py && echo IDENTICAL
IDENTICAL

$ sha256sum plans/fixtures/r29/generate_test_data.py plans/fixtures/r29/manifest.json
45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd  plans/fixtures/r29/generate_test_data.py
f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87  plans/fixtures/r29/manifest.json
```

Python census over the retained bytes:

```text
file_bytes 838
file_lines 27
file_split_words 87
line11_words 4
line21_words 5
block_split_words 24
```

The quoted block itself spans lines 11–16 (six physical lines), established by the `nl -ba` listing, not by a word-count operation.

Word counts are `len(str.split())`; line counts are physical line counts after UTF-8 decode.

## Proposed S070 row (NOT written; for L1/scribe to admit)

```text
| S070 | WebArena generated-config generator behavior and placeholder order — https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/scripts/generate_test_data.py | code | A | this pinned script's own six ordered serialized-text replacements, aggregate write, JSON parse and enumerate-index per-task filenames; not benchmark task success, task validity, deployment configuration, env_config values or runtime behavior | dce04686, main:8–23; ordered replacements:11–16 (`__GITLAB__`, `__REDDIT__`, `__SHOPPING__`, `__SHOPPING_ADMIN__`, `__WIKIPEDIA__`, `__MAP__`); `json.loads`:20; enumerate-index:21–23; live bytes 838, sha256 `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | six global `str.replace` passes run on serialized text in the listed order before any parse; the aggregate text is written first; `json.loads` has no visible repair step; per-task filenames use the enumerate index, not `task_id`; source behavior only | mined | 2026-10-21 | on-release | — (pending admission; do not preclaim) |
```

Row notes and admission conditions:

- **New row, no supersession.** S070 does not supersede S061/S068: those cover raw-task content (`config_files/test.raw.json`); S070 covers the transformation script's own behavior and order.
- **Used-by is deliberately `—`.** The draft at `.ufo/waves/round-29/drafts/webarena-config-projection.md` cites a proposed S070, but a draft path is not a corpus used-by. The admitting commit should fill actual `corpus/knowledge/…` and `corpus/lessons/round-29.md` paths only after those entries land; do not copy a pending path as if it existed.
- **Quote placement.** The ≤25-word located quote and its count live in this evidence report; the registry row carries line anchors and the byte pin, matching the S068/S069 anchor style.
- **No task-success claim.** The scope and "teaches" cells exclude benchmark task success, task validity, generated-config deployment, scorer behavior and model performance.

## Source-versus-runtime boundaries and remaining unknowns

- **Script not executed or imported.** No `config_files/test.json` or per-task file was created; no runtime output was observed. `env_config` was not fetched, read, imported, or resolved, so replacement values and any credential material in it remain unobserved and out of scope.
- **`index == task_id` is unmeasured here.** It is a property of a particular parsed list, not of the code; the code observation is only that the filename uses `enumerate` position.
- **Non-URL replacement occurrences are unmeasured here.** The replacements are global over serialized text; which string leaves they hit on the frozen input is data-dependent and belongs to the projection execution. "Global" is Python `str.replace` default semantics (no count argument at lines 11–16), not an occurrence census.
- **Upstream availability is dated.** The URL served these bytes on 2026-10-21 at the pinned revision. No claim is made about future availability or other revisions; recheck is `on-release`.
- **Counting method is explicit.** Quote length 24 is a whitespace `str.split()` result. No inferred word counts, line counts or token counts are asserted under another method.
- **This report is author-side evidence, not closure.** It does not write or admit a SOURCES row, does not discharge Q10, does not run the projection, does not alter scores or calibration, and is not a round admission.

VERDICT: PASS

Scoped to: live opening of the pinned generator at `dce04686`, byte identity with the frozen 838-byte fixture, manifest replacement-order cross-check, and a bounded S070 row proposal grounded in lines 8–23 with a 24-word located quote. Does not certify projection execution, oracle agreement, benchmark task success, task validity, deployment configuration or runtime behavior.
