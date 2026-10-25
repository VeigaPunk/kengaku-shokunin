# OpenS060 — reopening of source row S060 (json-repair 0.64.1)

Writer/seat: KengakuR28.OpenS060-2 (read-only scout, author-side advice; not outside closure).
Scope: S060 only. The template items for own-work S056 and paper S038 are not this seat's target
(sibling seats `KengakuR28.OpenS056-2` and the S038 reopen seat hold those); nothing here opens or
judges S056/S038. Registry not edited. Scratch evidence: `.ufo/waves/round-28/scratch/OpenS060/`.

## Row under check (identical in baseline b9b2479 and current tree)

`corpus/SOURCES.md:82` — `| S060 | json-repair 0.64.1 — https://pypi.org/project/json-repair/ | tool | B | … | PyPI summary and README; wheel SHA256 1e1022f8…b9e0a | REJECTED for this frozen stdlib-only E0–E8 comparison … | rejected | 2026-10-21 | 90d | corpus/lessons/round-27.md |`
(byte-identical to `git show b9b24796…:corpus/SOURCES.md`, checked by the scan below).

## Opening (access date 2026-10-21)

| what | URL | result |
|---|---|---|
| Row URL, HTML | https://pypi.org/project/json-repair/ | HTTP 200 but body is a 3038-byte `<title>Client Challenge` bot-check page — no package content. Not counted as an opening. Saved `scratch/OpenS060/pypi-project.html` (sha256 32ed6315…18ea). |
| Same project, PyPI JSON API (official index metadata for the row URL) | https://pypi.org/pypi/json-repair/0.64.1/json | Opened. name `json-repair`, version `0.64.1`, requires_python `>=3.10`, homepage github.com/mangiucugna/json_repair. Latest-version endpoint https://pypi.org/pypi/json-repair/json also reports `0.64.1`, not yanked. |
| README as published on PyPI (the `description` field of the same JSON) | same | Opened, 19890 chars, saved `scratch/OpenS060/pypi-0.64.1-description.md` (sha256 44e35576…9895). |

Anchor confirmation:
- PyPI summary (JSON `info.summary`): “A package to repair broken json strings” (7 words) — matches the quote recorded in `corpus/lessons/round-27.md:53` and `corpus/evidence/round27-sources/gate.md:53-54`.
- Wheel `json_repair-0.64.1-py3-none-any.whl` sha256 from the PyPI JSON = `1e1022f8d9b5a24433f7e28c2ee5c4ef42256e11ff0eef8abf7cad17fc8b9e0a` — **exact match** with the row anchor; uploaded 2026-10-19T09:38:36Z. (Sdist sha256 `7640f80e…2f19`, for reference only.)

Located README quotes supporting the narrow `teaches` (line numbers are in the saved PyPI description):
- :12 “Repair malformed JSON from LLMs, APIs, logs, and user input in Python.” (12 words) — tool scope.
- :77 “Automatically completes missing values in JSON fields with reasonable defaults (like empty strings or null), ensuring validity.” (18 words) — “repairs add semantics”.
- :194 “If you force already-valid JSON through the repair parser, `json_repair` may still "repair" it and can change the resulting structure or values.” (22 words) — maintainer-stated semantic alteration.
- :388 “Please pin this library only on the major version!” (9 words) — “unfrozen dependency” (0.x major admits every minor release; the row's hash pin is the lane's own freeze, not upstream's).

Teaches/anchor verdict: the `teaches` cell is narrow (rejection scoped to the frozen stdlib-only E0–E8 comparison, with a preregistration flip) and is supported by the opened summary, README and exact wheel hash. The “probed” part of `scope` rests on round-27 probes recorded in `.ufo/waves/round-27/build/SrcJsonRepair.md` (probe command, outputs, uv install of 0.64.1); I did **not** re-run them (seat forbids executing upstream code), so probe outcomes are carried, not re-observed. Tier B for a community tool's self-description stays conservative and consistent with the SOURCES header (“`community` is never tier A”); tier/scope/anchor/teaches are immutable cells and unchanged.

## C2 literal-citation check (frozen population)

Command (read-only; `git show` at the population's `base_revision`, pattern from `population.json`):
`python3 - <<EOF … git show b9b24796…:<path> for each of the 35 knowledge_paths; count reference_pattern matches equal to S060 … EOF`
Observed output: `files 35 missing_at_base [] S060_hits {}`.
A current-tree `rg` for the same pattern under `corpus/` also finds no S060 in `corpus/knowledge/`; hits only in `corpus/SOURCES.md:82`, `corpus/README.md:306`, `corpus/evidence/round27-sources/gate.md:53`, `corpus/lessons/round-27.md:36,53,188,203` — none in the frozen 35.

| field | value |
|---|---|
| citing_files (frozen 35) | none (0) |
| status | `rejected` |
| used-by | `corpus/lessons/round-27.md` (a lesson path that literally cites S060 at :36/:53/:188/:203; permitted extra lesson path per claims:25) |
| missing_used_by | none |
| expected C2 finding | none — an uncited rejected row is explicitly “not an error” (claims:25) |

## Suggested mutable-cell changes

**None.** status `rejected`, recheck `90d`, used-by `corpus/lessons/round-27.md` are all consistent with the opened source and the frozen-population result; the lesson (:203) explicitly keeps S060 “lesson-only as a rejected policy candidate”. Observation only, not a requested change: recheck `90d` is a relative duration while older rows use absolute dates (e.g. S001 `2027-01-17`); S056 uses the same `90d` form and C2 does not validate recheck format, so no edit is advised.

## Tooling / limitations

- No installs or updates; tools used: curl, python3 stdlib, git (read-only `git show`), rg. No pacman, no REA MCP.
- Row URL's HTML view was bot-challenged; opening relies on PyPI's official JSON API for the same project/version (same method as round 27). Not a browser rendering of the page.
- Literal-reference coverage only, not semantic citation support; GitHub README at `main` not re-opened (PyPI-published description for 0.64.1 used instead, which is version-pinned).

VERDICT (scoped to S060): **PASS** — source reopened via PyPI JSON for 0.64.1, wheel hash matches exactly, summary and README quotes located, zero literal citations in the frozen 35-file population, status/used-by consistent; no registry change suggested. S056/S038: not assessed by this seat.
