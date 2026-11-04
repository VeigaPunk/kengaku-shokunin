# RegistryReviewerR74 — 8-field review of the `round74-c1` / `round74-c2` SKILL.md rows

Scope: the two new registry rows (`SKILL.md:706-707`, working tree) against the eight-field
gate/probe standard (header `SKILL.md:589`; PROTOCOL.md §Gate standard, fleet root). All runs
executed 2026-11-04. No lane mutation performed; all scratch under
`/fast/scratch/hyaku/kengaku-r74/RegistryReviewerR74/` (cleaned).

## Review matrix

| Field / check | `round74-c1` (SKILL.md:706) | `round74-c2` (SKILL.md:707) |
|---|---|---|
| 1. Exactly 8 columns | **PASS** — mechanical split of the raw line yields 8 cells | **PASS** — 8 cells |
| 2. kind = `gate` | **PASS** — `gate` | **PASS** — `gate` |
| 3. Entry resolves to existing Python script, parses cleanly | **PASS** — `plans/round74_c1_registry.py` exists (13090 B, committed at tip `cea7ebf3`); `ast.parse` clean | **PASS** — `plans/round74_c2_registry_audit.py` exists (18874 B, committed); `ast.parse` clean |
| 4. Verdict map declares `0` clean and `1` failed | **PASS** — `` `0` pass (`PREDICATE R74-C1 pass`) · `1` fail (MISSING, INCOMPLETE, ENTRY-MISSING, SELFTEST-UNBACKED, DUPLICATE) · `2` setup ``; script: `return 0 if r74 else 1` (`round74_c1_registry.py:206`), `return 2` on SETUP ERROR (`:292`) | **PASS** — `` `0` pass (`MISMATCH 0`, `PREDICATE R74-C2 pass`) · `1` fail (any D1–D4 or MALFORMED defect) · `2` setup ``; `return 0 if total == 0 else 1` (`:256`), `return 2` on SETUP ERROR (`:430`) |
| 5. Self-test command resolves, working `--selftest` | **PASS** — ran `python3 plans/round74_c1_registry.py --selftest`: 4 × `SELFTEST ok …`, `SELFTEST cases=4 failures=0`, rc 0 (matches frozen sentence) | **PASS** — ran `--selftest --work <seat subdir>`: 4 arms, `SELFTEST arms=4 red=3 ok=True`, rc 0 (matches frozen sentence); flags `--selftest --mutants --work` present in argparse (`:416-419`) |
| 6. Pinned values + write scope non-empty and accurate | **PASS** — "pinned universe: decoupled self-assessment docs" matches the scanner (`SELF_FILES` + SKILL.md-outside-registry-block + `corpus/knowledge/*.md` + `plans/*.md`, `:51`, `:72-99`); "read-only" verified: entry run left clone and lane byte-identical, self-test builds fixtures in `tempfile.TemporaryDirectory()` (`:215`) | **PASS** — "pinned fields: 8 columns, gate or probe kinds, kengaku owner, 2 errata items" matches `COLUMNS` (8-tuple), `KINDS=("gate","probe")`, `OWNER_PREFIX="kengaku"`, `ERRATUM_ITEMS` (2 items, `:52-58`) and D4 enforcement (`:208-228`); "read-only in lane; scratch under --work" verified: entry run wrote nothing in clone; selftest/mutants write only an owned child of `--work` and rmtree it in `finally` (`:318-371`, `:407-408`) |
| 7. Owner begins with `kengaku` | **PASS** — `kengaku` | **PASS** — `kengaku` |

Declared flags cross-check: c1 row lists `--lane --universe --selftest` = argparse exactly
(`:283-285`); c2 row lists `--lane --selftest --mutants --work` = argparse exactly (`:416-419`).

## Executed verification

- `--selftest` (both rows): pass, outputs byte-match the frozen sentences.
- c2 `--mutants --work <scratch>`: `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=1`, rc 0.
- c1 entry on the lane **working tree** (the state containing these rows): `UNIVERSE mode=decoupled
  files=136 plans_seen=90 self_advertising_prevented=True`, `ADVERTISED total=116`,
  `REGISTERED total=116 rows=116`, `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`,
  `SELFTEST-UNBACKED 0`, `DUPLICATE 0`, `PREDICATE R74-C1 pass`, rc 0 — equals the frozen "after" target.
- c2 entry on working tree: `INSTRUMENTS total=116 … rows=116`, `PARSED scripts=116 failed=0`,
  D1–D4/MALFORMED all `ok n=0`, `MISMATCH 0`, `DEFECTS n=0`, `PREDICATE R74-C2 pass`, rc 0.
- Same entries in a shared clone at committed tip `cea7ebf3`: c1 = `ADVERTISED total=116`,
  `REGISTERED total=114 rows=114`, `MISSING plans/round74_c1_registry.py`,
  `MISSING plans/round74_c2_registry_audit.py`, rc 1; c2 = `INSTRUMENTS total=114`, rc 0.

## Findings by severity

No blocking or major defects. Both rows conform to the eight-field standard and both gates are
green and discriminating on the working tree.

- **LOW (state, not a row defect) — rows are uncommitted.** At committed tip `cea7ebf3` the lane has
  ` M SKILL.md` (evidence: `git status`); the two rows exist only in the working tree, so the
  committed-tip c1 run is red with exactly the two round-74 instruments unregistered — a live
  demonstration that the decoupled gate is not circularly self-satisfied, but also proof the
  landing-tip predicate (`REGISTERED total=116`) holds **only if these rows land in the same
  integration commit** as everything else at the tip.
- **LOW — verdict-map labels.** Rows say `0 pass / 1 fail / 2 setup` where the Gate standard's
  canonical classes are `clean | failed | could-not-evaluate`. Codes `0` and `1` are declared (item-4
  requirement met), `2` is declared and factually maps to could-not-evaluate (SETUP ERROR exit 2 in
  both scripts; argparse usage also exits 2). Sibling rows (round69-c2, round73-c2) label `2`
  `could-not-evaluate`; harmonizing the label would be cosmetic, not required — c2's own D2 check
  already accepts these cells (`1` present; "fail" ∈ DEFECT_WORDS, `:62`).
- **LOW — c2 self-test `--work` pin.** The row pins `--work /fast/scratch/hyaku/kengaku-r74` (the
  shared scratch root, no seat subdir). Safe today — the script creates an owned child and removes
  it in `finally`, and its internal default is `…/c2-audit` — but under wave scratch discipline a
  re-running seat should substitute its own subdir (as this review did).

## Residual risk and verification gaps

- rc-2 (`setup`) paths were verified in source, not executed; argparse-usage exit 2 is Python-default.
- c2's row self-test was executed with `--work <seat subdir of the pinned root>`, not the literal
  shared-root path (wave scratch rule 3); behavior is path-independent by construction (owned child dir).
- c1 `--universe legacy` control was not re-run here; covered by committed receipt
  `corpus/evidence/round74/c1-before.txt` per the frozen claims file.
- The landing-tip 116/116 result was measured on the working tree, not a commit (no commit exists
  with the rows yet); re-derivation at the tip is the orchestrator's landing check.
