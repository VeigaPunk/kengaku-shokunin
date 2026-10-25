# FrontmatterScout — D18 input (round 25, read-only)
No lane write, no network, no installs; only this report. YAML census re-run locally (PyYAML 6.0.3).

## Contract (observed)
`PROTOCOL.md:429`:
> | `SKILL.md` | The specialist's craft: triggers, decision tables, error patterns, checklists, cited sources. Its frontmatter `description` carries quoted trigger strings, an anti-trigger, and a sibling-arbitration note — capability-and-scope-only descriptions misroute |

## Sibling exemplars that conform (observed; both YAML-parse)
1. `kotoba-shokunin/SKILL.md:3-15` — 8 quoted triggers; folded scalar, reflowed here:
> Prompt & skill craft — audits, writes, and rewrites SKILL.md / AGENTS.md / dispatch prompts / system prompts for trigger fidelity and decision density. Triggers: "skill file", "SKILL.md", "frontmatter description", "trigger words", "prompt craft", "write a skill", "audit this skill", "skill quality". Anti-triggers: general prompt engineering for model outputs (not skill files), runtime code changes, and domain content inside a skill's reference/ tree. Sibling boundary: the five `*-shokunin` domain skills (kagi, kake, kasegi, kengaku, kumitate) own their own SKILL.md content — this skill audits and reports; fixes route to the owning lane.
2. `souji-shokunin/SKILL.md:2` — 11 quoted triggers (caveat: no `name:` key):
> "Fleet repo & workspace hygiene (掃除). Triggers: 'clean', 'prune', 'sweep', 'stale artifacts', 'dead worktrees', 'duplicate config', 'scratch bloat', 'quarantine', 'hygiene census', 'obsidian ledger', 'can I delete this'. Anti-trigger: NEVER git history rewrite, NEVER credentials/secrets handling (kagi-shokunin owns credential hygiene), NEVER operator config, NEVER live/unpushed lane work; publishing and vault actions are operator-owned. Sibling arbitration: contested artifact ownership is reported to the integrator, never silently absorbed."

## Census (observed, 19 lanes)
`yaml.safe_load` on each frontmatter: 6/19 parse (chousa, kotoba, kotodama, lore, mori, souji); 13 raise
`ScannerError: mapping values are not allowed here`, incl. `kengaku SKILL.md:3` (unquoted `Rank: shonen`).
All-three textual conformance: kotoba, lore, souji, game-dev-3d (last fails YAML); kengaku 0/3, 0 quoted — a bare grep passes a file that cannot parse, so the proposal is validated against both.

## Proposed kengaku description (not applied — integrator/lane writes)
```yaml
description: >
  LLM/model research & evaluation — benchmark selection, contamination status,
  eval-battery design, ex-ante prediction and calibration scoring, power and
  interval derivation, attribution probes, and hermetic offline replay.
  Triggers: "which benchmark", "benchmark contamination", "eval battery",
  "ex-ante predictions", "Brier score", "power analysis", "confidence interval",
  "attribution probe", "hermetic grader", "route telemetry", "open-weight twin".
  Anti-trigger: NOT serving-plane health, endpoint identity, or serving-flag /
  quantization remediation — that is kama's province; this lane records endpoint
  identity only as a pinned premise and never changes a flag. Sibling
  arbitration: kotoba receives reusable prompt/skill-craft implications while
  kengaku keeps the measured capability effect (PROVINCE.md:134); kumitate owns
  OMP route resolution, dispatch and failure taxonomy (PROVINCE.md:137); kama
  owns serving-plane health and endpoint identity (PROVINCE.md:132); chousa owns
  question-framing → source-hierarchy → citation-chain method (PROVINCE.md:133;
  corpus/QUALITY.md:8); tameshi owns verification-fixture and mutation-battery
  craft — kengaku's `--selftest` is its own gate self-test, not a fixture service
  for other lanes. Contested scope is reported, never absorbed. Rank: shonen.
```
Validated: `safe_load` OK; 11 quoted triggers; anti-trigger, arbitration and rank present; all five
siblings named. `grep -qE 'Triggers: "\|Anti-trigger: NOT\|Sibling arbitration:'` holds under the folded
block (single-line double-quoted alternative if the check anchors on the key).

## Trigger provenance (observed)
benchmark selection `SKILL.md:23` · contamination `:63` · eval battery `:53,:334` · ex-ante/Brier `:556` · power `:155` + `corpus/evidence/round12-ladder/power_r12.py` · attribution `PROVINCE.md:110` · hermetic grader `SKILL.md:494` · route telemetry `:210` · catalogs/open-weight twin `:362`.

## Delta vs FrontmatterScribe.md:19
Same parse fix and five-sibling set; the scribe lists 5 triggers and scopes its anti-trigger to serving
flags only. `[INFERENCE]` the wider trigger list matches the lane's measured decision surface.

## Unknowns
- `plans/state_check.py` absent today; `round-25-claims.md:80` makes P2c the SHONEN check and `:109` calls
  D18 only "a frontmatter grep" — pattern unspecified.
- `tameshi` has no `PROVINCE.md` row (`:125-139`) → its boundary is `[INFERENCE]` from tameshi
  `SKILL.md:3,8`; reciprocal only after a PROVINCE append.
- `kotoba:12-15` says shokunin files sit outside omp skill discovery, so this description is
  registry/dispatch-facing; router-behaviour gain is unmeasured.

VERDICT: contract demands quoted triggers + one anti-trigger + sibling arbitration (`PROTOCOL.md:429`); kengaku carries none and its line-3 frontmatter fails YAML parse; kotoba and souji conform; the folded proposal parses, greps, and names all five sibling boundaries, with tameshi marked inference. Installs: none.
