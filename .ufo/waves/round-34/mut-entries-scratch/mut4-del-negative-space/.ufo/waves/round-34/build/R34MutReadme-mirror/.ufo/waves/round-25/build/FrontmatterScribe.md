# FrontmatterScribe — kengaku D18 conformance draft (round 25)

## Behavior

Drafted a replacement `description:` for `kengaku-shokunin/SKILL.md` lines 1–5 per the
PROTOCOL.md file-contract row (`PROTOCOL.md:429`): quoted triggers, one anti-trigger, and a
sibling-arbitration note. Draft is NOT applied to SKILL.md (scribe is read-only for the lane tree).

## Finding: current frontmatter is invalid YAML

- `kengaku-shokunin/SKILL.md:3` — PyYAML `safe_load` → `ScannerError: mapping values are not
  allowed here` at column 264 (`... corpora absent 2026-10-15). Rank: shonen.`). Cause: unquoted
  plain scalar containing `: ` (`Rank: shonen`). The shipped frontmatter does not parse.
- Fix in draft: wrap the value in double quotes (sibling convention, cf. `chousa-shokunin/SKILL.md:3`).

## Exact replacement text (single line, double-quoted scalar)

```yaml
description: "Domain specialist — LLM/model research & evaluation — scopes llm-wiki (~/Projects/webzites/repos/llm-wiki, absent at round-24 check; digests retained in corpus/knowledge/) and route telemetry (historical; ~/Projects/bounties/ledger/telemetry.jsonl absent, last resolved round 11). Triggers: 'model evaluation', 'eval calibration', 'benchmark grader', 'attribution probe', 'novelty pricing'. Anti-trigger: NOT serving-flag changes or endpoint remediation. Sibling arbitration: kotoba owns prompt and skill craft (kengaku keeps only measured capability effects); kumitate owns OMP route resolution and dispatch; kama owns local endpoint health and identity; chousa owns research method (question framing, citation chains); tameshi owns verification-fixture and test-generation craft. Rank: shonen."
```

Counts: 5 quoted triggers, 1 anti-trigger, 1 sibling-arbitration note covering all five named
siblings (kotoba, kumitate, kama, chousa, tameshi). `Rank: shonen.` retained.

## Validation (observed)

- PyYAML 6.0.3 (`python3 -c "import yaml"`, present, not installed): draft `safe_load` OK;
  description value is one line; triggers extracted = 5; `Rank: shonen` present.
- `npx -y js-yaml /tmp/fs-body.yml` (npm registry fetch, nothing installed globally): parsed to JSON
  with the identical description string.
- Historical-absence checks run today (`test -e`, `ss`):
  - ABSENT `~/Projects/webzites/repos/llm-wiki`
  - ABSENT `~/Projects/bounties/ledger/telemetry.jsonl`
  - ABSENT `~/archive/bench-arena`, ABSENT `~/bench-arena`
  - `ss -ltn 'sport = :34113'` → 0 listeners
  - PRESENT `grader.py`, `plans/attrib_probe.py` (not claimed absent)
  These match PROVINCE.md `## Province map — round 24` (Historical table).

## Sibling descriptions consulted (read-only)

- `chousa-shokunin/SKILL.md:3` — research method; quoted triggers + anti-trigger style.
- `kotoba-shokunin/SKILL.md:3-15` — owns prompt/skill craft; its sibling-boundary note names
  `kengaku` among the domain skills and says the fleet `SKILL.md` files are not router-visible.
- `kama-shokunin/SKILL.md:3` — "local model serving & endpoint health".
- `kumitate-shokunin/SKILL.md:3` — "OMP task/hub dispatch".
- `tameshi-shokunin/SKILL.md:3` — "verification-fixture craft" (no literal "test generation"
  phrase; the draft's "test-generation craft" follows the dispatch brief, not tameshi's own text).

## Out of scope / not done

- SKILL.md not edited. Applying the replacement is an integrator/lane write.
- Routing note: kotoba's own note (`kotoba-shokunin/SKILL.md:10-12`) lists five domain skills and
  does not list chousa, kama, or tameshi; the draft's arbitration note is therefore not yet
  reciprocated in kotoba's text.

## Tooling

- No installs. Used existing `python3` + PyYAML 6.0.3 and `npx -y js-yaml` (on-demand npm fetch).

## Findings index

1. `kengaku-shokunin/SKILL.md:3` — invalid YAML (`mapping values are not allowed here`) — defect.
2. Draft text above — parses under PyYAML and js-yaml.

VERDICT: current `SKILL.md` frontmatter fails YAML parse; quoted single-line replacement drafted, parses under PyYAML and js-yaml, not applied.
