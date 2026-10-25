# RowOpenAIEvalsJson — round 27 build report (seat: KengakuR27.RowOpenAIEvalsJson)

Scope: one SOURCES row + gate line for openai/evals `json_match.py` (answer-extraction policy only). Draft only; no SOURCES.md, gate.md, or lane tree written.

## Opened source (2026-10-21)
- URL: https://github.com/openai/evals/blob/main/evals/elsuite/basic/json_match.py (raw fetched via raw.githubusercontent.com, main branch)
- Last commit touching file (GitHub API, `commits?path=`, newest first): `4b7a66bd45f06156656e021e170e7574f6cde3f5`, 2023-10-27 ("Added Icelandic inflection eval; JsonMatch eval function (#1387)").
- Fetched bytes: 106 lines, sha256 `6cc971f9a360a89b628595f1de5b030bd38969f2160cca75bcf11ee7aa0795e8`, saved at `/tmp/kengaku-r27-RowOpenAIEvalsJson/json_match.py`.
- Extraction behavior, verbatim from the file:
  - L76 `sampled = result.get_completions()[0]`
  - L80 `sampled_json = json.loads(sampled)` inside `try:`
  - L82 `# If the sampled string is not valid JSON, it will never match`
  - L83 `sampled_json = None` on `ValueError`. No fence stripping, no substring/bare-match fallback, no first/last selection.
- Docstring L43–44 (comparison semantics, not extraction): "The decoded JSON objects are compared elementwise and must match exactly."

## (1) Draft SOURCES.md row (11 cells, matching existing rows)
Note: the header of `corpus/SOURCES.md` (line 21) and every existing row have **11** pipe cells, not 13 as the assignment states. I matched the file. The "13-column" wording in `round-27-claims.md` (line 143 area / C1 text) is inconsistent with the registry and should be corrected by the integrator.

`| S0xx | openai/evals `evals/elsuite/basic/json_match.py` (JsonMatch eval) — https://github.com/openai/evals/blob/main/evals/elsuite/basic/json_match.py | code | A | what the openai/evals JsonMatch harness does with the whole sampled completion: one json.loads, no fence or substring extraction (answer-extraction policy only) | json_match.py:76, :80, :82–83 (eval_sample); commit 4b7a66bd (2023-10-27), sha256 6cc971f9… | a published harness reads the entire completion as JSON in a single json.loads and maps a decode failure to None (never matches); it implements no fenced-block or bare-match extraction, so it is one real strict-whole reference point, not evidence that strict-whole is the correct policy | queued | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md |`

Tier A is scoped to the harness's own code path only (maintainer source code for its own behavior), not to extraction accuracy in general.

## (2) gate.md line (not written to the lane; draft)
`S0xx | https://github.com/openai/evals/blob/main/evals/elsuite/basic/json_match.py | accessed 2026-10-21 | commit 4b7a66bd45f06156656e021e170e7574f6cde3f5 (2023-10-27); raw main, 106 lines, sha256 6cc971f9a360a89b628595f1de5b030bd38969f2160cca75bcf11ee7aa0795e8 | json_match.py:80–82 (eval_sample) | "If the sampled string is not valid JSON, it will never match"`
- Quote length: 12 words (≤25). Located at L82; the code it annotates is L80 `sampled_json = json.loads(sampled)`.

## (3) Policy grounding
- Grounds **E4 strict-whole** only. The source's semantics are `json.loads(raw)` with ValueError→None.
- Grounds **none** of E0–E3, E5–E8 (no fence logic, no bare-match logic, no decode-scan logic).
- Deviation to resolve: the pre-registration E4 is `json.loads(raw.strip())`; the source does **not** strip. Checked locally (python3 stdlib, 2026-10-21): `json.loads` rejects `"\x0c{…}"`, `"\x1c{…}"`, `"\xa0{…}"`, which `strip()`+`loads` accepts; both accept leading/trailing ASCII space/newline.
- Population check (my own one-off, not the instrument): across all 5942 `raw` strings in the four pinned jsonl files (round8/9/11/12), `json.loads(raw)` and `json.loads(raw.strip())` disagree on **0** records. So the strip deviation cannot move any E4 verdict on the 1964 population; it is a wording/fidelity point to record in the knowledge entry, not a result change. No amendment required unless the critic wants the source-exact form.

## Installs / tool use
- No installs. Used `curl` (existing), `sha256sum`, `grep`, `python3` stdlib (PYTHONDONTWRITEBYTECODE=1). GitHub API call for commit lookup, unauthenticated.

## Files written
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-27/build/RowOpenAIEvalsJson.md` (this report).
- `/tmp/kengaku-r27-RowOpenAIEvalsJson/json_match.py` (saved fetch), sha256 `6cc971f9a360a89b628595f1de5b030bd38969f2160cca75bcf11ee7aa0795e8`.

## Open items for integrator
1. Reconcile "13-column" wording with the 11-column registry (claims file vs SOURCES.md line 21).
2. Decide whether E4 keeps `.strip()` (current pre-registration text) or moves to source-exact `json.loads(raw)`; population result is identical either way (0 differences).
3. Assign the S0xx id (next free is S049 per the registry note in the claims file; the S0xx placeholder was left as instructed).

VERDICT: openai/evals JsonMatch is a primary, tier-A source for the strict-whole policy E4 only (json.loads on the whole completion, no extraction); the strip deviation changes 0 of 5942 pinned raw strings.
