source: R29DraftEntry scoped report — draft-only assignment for round29 C1 (generated-config projection frontier); writer seat R29DraftEntry
verified-at: 2026-10-21 — local reads of the pinned r29 fixtures and the draft file; no live URL access, no execution of upstream or projection code
writer: R29DraftEntry

# R29DraftEntry — scoped report

## Behavior

Wrote one prose draft: `.ufo/waves/round-29/drafts/webarena-config-projection.md` (7404 bytes, sha256 `7bf99d9b62d7da065f4ac4a443864acfa954e88923224fe79094269ccc25318e`). It documents the pinned upstream generator's six sequential text replacements, parse, and positional output naming, with source line anchors from the pinned local copy, and states the neutral-profile negative boundary. It proposes a README frontier clause as text only.

No corpus, SOURCES, README, index, plan, or code file was edited. No commit, push, or lane-state mutation.

## Commands and observed output

- `cat plans/fixtures/r29/generate_test_data.py` and `grep -n` over it: 27 lines; the six `raw.replace` calls are at lines 11–16; `json.loads` at line 20; `enumerate` loop at lines 21–23; wildcard import at line 5.
- `sha256sum plans/fixtures/r29/* plans/fixtures/r28/webarena/config_files/test.raw.json`:
  - `plans/fixtures/r29/generate_test_data.py` = `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` — matches manifest.
  - `plans/fixtures/r29/manifest.json` = `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` — matches the value named in the claims plan.
  - `plans/fixtures/r29/profiles.json` = `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` — matches manifest.
  - `plans/fixtures/r28/webarena/config_files/test.raw.json` = `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` — matches manifest and S068.
- Read `plans/round-29-claims.md`, `corpus/README.md` (Frontier and round28 paragraphs), `corpus/SOURCES.md` (S068–S069 rows), `corpus/lessons/round-28.md` (M78, S068 gate block), and the build spec entries for S070–S073.
- Dispatch entries for S070–S073 are proposals only; no rows were written for them.
- `sha256sum` of the written draft: `7bf99d9b…25318e`.

Not run: projection tool (`plans/config_projection.py` does not exist at base), any selftest, any build, any linter, any formatter, any census, any upstream import or execution, any read of host env, credential, or auth-state files, any benchmark endpoint request.

## Source status

- S068: existing row; its pinned raw file sha is confirmed above. Used-by link deferred.
- S070–S073: proposed. Anchors in the draft come from the pinned local generator copy and its sha. Live upstream URLs were not reopened by this seat; no row is written.
- The draft flags the wildcard-import target (`browser_env.env_config`) as unread and possibly credential-bearing.

## Findings

- The projection contract in the claims plan is consistent with the pinned generator text (six replacements in order, parse after replacement, positional output names).
- Two source-level observations are recorded as `[INFERENCE]` in the draft, not as measured facts: (a) output filename depends on list position, not `task_id`; (b) replacement is global over serialized text, so non-URL string fields may change.
- `__SHOPPING__` is not a substring of `__SHOPPING_ADMIN__` by string inspection. Recorded as inference; the projection's own selftest must check it.

## Measured facts

None. The draft contains no projection outputs, token counts, task counts, or per-task objects. The 812 × 3 = 2436 figure is labeled planned.

## Unknowns

- Non-URL replacement occurrences on the frozen input (F3).
- Whether index equals `task_id` for all 812 items (F4).
- Whether the upstream prepare/workflow caller uses the generator as read (S072/S073 not opened).
- Whether live upstream bytes equal the pinned copy (not re-fetched).

## Handoff to L1

- Add measured facts only after the projection tool runs under its own verification.
- Record the actual final writer before the Q10 re-read.
- Open S070–S073 live and decide their rows; the draft's anchors are pinned-local only.
- Re-read the exact final draft bytes; the draft's sha is in Behavior above.
- No corpus, index, or round admission from this seat.

VERDICT: PARTIAL
Scope: draft prose written with source-only anchors from pinned local bytes; no measured outputs; live source reopen and row decisions deferred to L1; not a round-level or corpus admission.
