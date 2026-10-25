# Stored verdicts vs replay extractor

Axis: novelty / C1; scope is the four frozen response populations, not perturbation outcomes.

## Reconstructed contract

- `grader.py:121-134` parses the last matching fenced block with `json.loads`; on failure/no fence, it scans brace/bracket candidates in reverse, tries `json.loads` on each, and returns `None` if none parse.
- The parser regex literals and flags, fallback regex and order, exception handling, and JSON parser calls match in `round8-horizon/horizon.py:38-47`, `round9-replication/replicate.py:38-47`, `round11-power/probe_r11.py:47-56`, and `round12-ladder/probe_r12.py:51-60`. No behavioral extractor divergence is present in these checked-in sources.
- Strict source-byte identity is not literal: `grader.py` expands the compact `try: return ...` / `except Exception: ...` statements into multiline statements. The regex strings and parsing/fallback operations are unchanged (the grader itself describes this as “byte-faithful semantics,” `grader.py:120`).

## Evidence chain: stored `ok` and `raw`

- Round 8: `horizon.py:139-146` computes `got` from `r["content"]`, grades it, and logs both `ok` and the same full content as `raw`; C-cell records do likewise via `grade_c` at `:263-267`.
- Round 9: `run_r9.py:1-4` imports `p` from `/tmp/kengaku-r9/replicate.py`; `:19-24` invokes `p.extract_json_block`, grades, and logs `ok` plus full `raw`. The checked-in `replicate.py:38-47` matches the grader parser. `replication.md:69` identifies the temporary run script/source-copy paths.
- Round 11: `run_r11.py:35-37` imports `probe_r11.py`; `:68-72` uses its extractor and writes `ok` with the same response as `raw`. `ordering.log:4-7` pins that probe before launch. `sha256sum .../round11-power/probe_r11.py` returned `cf754d78e9065d679aa64872766be748a9d349fc13acdc5d03c5ba41447bdaa7`, matching the recorded hash.
- Round 12: `run_r12.py:58-60,91-108` imports `probe_r12.py`, parses the same response, grades family 1 with `grade_state` and family 2 with `grade_seq`, then logs `ok` and full `raw`. `ordering.log:4-7` and `results-r12.jsonl:1` pin the machinery. `sha256sum .../round12-ladder/probe_r12.py` returned `1871697f5c3410adf3c17297138e76416cdeb63194038324eec067abe6b90662`, matching both.
- C1 freezes records with `raw` and stored `ok`, and admits only those whose baseline re-grade reproduces the stored verdict (`plans/round-26-claims.md:42-53`). Thus every included stored `ok` is required to equal the grader replay; mismatches are excluded, not silently treated as same-origin.

## Divergence / limits

- `run_r9.py` is a wrapper, not a parser definition. Its historical parser is loaded from `/tmp/kengaku-r9/replicate.py`; the retained `ordering.log` has timestamps only (`round9-replication/ordering.log:1-2`), with no probe-script hash. The checked-in source matches, but exact historical temporary-file bytes are not independently hash-proven. Round 8 also has no retained run-script hash.
- `read xd://lsp` returned “No such tool” (LSP absent); used literal grep as fallback for symbol/source mapping. No endpoint, probe, or test was run.

VERDICT: No regex/fallback/JSON-parsing divergence found; stored verdicts are produced alongside the raw response by the corresponding parser/grade path, and C1 enforces replay equality for included records. R11/R12 provenance is hash-closed; R9 (temporary import) and R8 are not hash-closed. Confidence: high on source-level parser equivalence, medium on historical R8/R9 byte provenance. Installs: none.