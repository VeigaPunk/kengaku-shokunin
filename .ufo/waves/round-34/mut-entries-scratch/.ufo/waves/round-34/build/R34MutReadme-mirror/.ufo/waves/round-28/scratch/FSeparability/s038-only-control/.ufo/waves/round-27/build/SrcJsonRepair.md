# SrcJsonRepair — json-repair (PyPI) as extraction-policy source

Axes (godspeed): novelty (policy prior art for C1) · calibration (decision hygiene: frozen E0–E8 untouched) · no scope growth (leaf seat, read-only).

## What json-repair does (all web accessed 2026-10-21)
- PyPI https://pypi.org/project/json-repair/ (JSON API fetch): "Latest: 0.64.1"; summary "A package to repair broken json strings" (7 words); requires-python >=3.10; homepage https://github.com/mangiucugna/json_repair/.
- README https://github.com/mangiucugna/json_repair/blob/main/README.md (raw `main`):
  - :12 "Repair malformed JSON from LLMs, APIs, logs, and user input in Python." (12 words)
  - :14 "Fix missing quotes, commas, brackets, comments, stray prose, and truncated values." (11 words)
  - :75-77 §Auto-Completion: completes missing values with defaults (empty string / null).
  - :250 strict mode raises on "multiple top-level elements" (fragment, 3 words) ⇒ default mode tolerates several top-level values.
  - :346 examples/repair_llm_output.py "repairs markdown-wrapped or prose-wrapped model output." (6 words) — the README's only fence mention; fence stripping is not a documented parser feature.
- Empirical probes — cmd `PYTHONDONTWRITEBYTECODE=1 /tmp/kengaku-r27-sjr-venv/bin/python /tmp/kengaku-r27-sjr-probe.py` → exit=0, version 0.64.1:
  - `'Here you go:\n```json\n{"n": 1}\n```\nHope that helps'` → `{'n': 1}` (prose + fence tolerated)
  - `'```json\n{"a": 1}\n```\ntext {"a": 2}'` → `{'a': 2}`; `'{"a": 2} junk {"a": 1}'` → `{'a': 1}` ⇒ **LAST top-level value wins, not first**
  - `'```output\n{"a": 1}\n```'` → `{'a': 1}`; bare-array fence → `[1, 2, 3]` (any/absent label passes via prose-skipping)
  - `'{"a": [1, 2'` → `{'a': [1, 2]}` (truncation completed); `"{'a': True, 'b': None,}"` → repaired
- Source level (installed wheel `json_repair-0.64.1-py3-none-any.whl`, PyPI sha256 `1e1022f8d9b5a24433f7e28c2ee5c4ef42256e11ff0eef8abf7cad17fc8b9e0a`):
  - `json_repair/parse_string_helpers/parse_json_llm_block.py:11-18` — "Extracts and normalizes JSON enclosed in ```json ... ``` blocks." (10 words); :14 literal prefix test `== "```json"` — only that exact label is fast-pathed.
  - `json_repair/json_repair.py:141-144` — `try_valid_json_suffix`: "Once the parser has found a top-level value after a prefix, raw decoding that value is still a safe, targeted fast path." (23 words) = trailing-text tolerance.
  - `grep '`' site-packages/json_repair/` → no ``` fence grammar beyond that literal path plus in-string fence preservation (`json_parser.py:84-86`).

## Decision — REJECTED as an E-policy source for round 27; QUEUED for future use
1. Frozen set: `plans/round-27-claims.md:33` freezes the policy table E0–E8; contract pins `POLICIES` to E0..E8 exactly and `:62` pins `TOTAL population=1964 policies=8 compared_verdicts=15712`; Q1–Q8 + 9×9 matrix are filed over that set. Adding E9 now is a post-hoc amendment of a frozen pre-registration (`:11`: amendments appended, never edited in place).
2. stdlib-only: `plans/round-27-claims.md:59` "stdlib only, offline" — json-repair is third-party PyPI, barred import; oracle `plans/fixtures/r27/policy_oracle.py` must be written from text only (`:63-64`) — a heuristic repair parser cannot be faithfully reimplemented stdlib-only.
3. Version drift: README:385 "Please pin this library only on the major version!" (9 words) while `0.*` includes every minor ⇒ semantics can change in any release; a frozen finite-population policy needs hash-pinned semantics (wheel sha256 above) — a fixtures change this round.
4. Semantics: repair (completing truncated/malformed spans) alters grader-input generation, not span selection; its selection axis (fence-agnostic, last-wins) duplicates E2/E8 coverage; truncation-completion collapses `none` cases, making the frozen `none=` metric non-comparable.

Queue (for KengakuR27; I wrote nothing in the lane):
- This round: admissible prior art for the C1 knowledge entry `corpus/knowledge/extraction-policy-comparison.md` — a published repair-based lenient extractor the frozen policies do not implement, supporting "construct published in kind" ⇒ novelty held at 7. If opened: SOURCES row S049, tier B tool (S045 evalmut precedent), quotes+URLs+date above; gate file `corpus/evidence/round27-sources/gate.md` per frontier rules.
- Later round only: `## Amendment N` adding E9 "repair-loads" with vendored pinned wheel under `plans/fixtures/r27/` + new oracle leg + prediction addendum; never mid-round.

Installs: uv 0.13.0 (preinstalled, unchanged); scratch `/tmp/kengaku-r27-sjr-venv` + `uv pip install json-repair==0.64.1` (channel: PyPI via uv; reason: empirical fence/trailing-text/first-vs-last check). No pacman transactions. Probe script `/tmp/kengaku-r27-sjr-probe.py` (scratch only).

VERDICT: json-repair 0.64.1 is a prose/fence-tolerant, truncation-completing, LAST-object-wins repair parser ("```json" literal fast path only) — rejected as a round-27 E-policy source (frozen E0–E8, stdlib-only, version drift); queued as S049-candidate prior art / future amended E9.
