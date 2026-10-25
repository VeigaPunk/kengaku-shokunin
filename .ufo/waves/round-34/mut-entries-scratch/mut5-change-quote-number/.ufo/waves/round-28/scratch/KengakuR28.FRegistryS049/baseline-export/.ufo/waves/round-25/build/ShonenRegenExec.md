# Round 25 — D17 SHONEN regeneration

## Files changed
- `/tmp/kengaku-r25-ShonenRegenExec/SHONEN.md` in private clone branch `r25-ShonenRegenExec`; observed base `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a`.
- Advisory report: `.ufo/waves/round-25/build/ShonenRegenExec.md`.

## Behavior
Regenerated the canonical checklist text with the repository name, all four marks `[~]`, and exactly one indented path-only evidence line beneath each box. No `[x]` marks or extra checklist prose.

## Final file (`SHONEN.md:1-12`)
```markdown
# kengaku-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  SKILL.md
- [~] At least one end-to-end domain task executed and logged in LOG.md
  LOG.md
- [~] Instructions executable by an agent without oral context
  corpus/README.md
- [~] No cross-domain bleed (PROVINCE.md still accurate)
  PROVINCE.md
```

## Retained evidence
`/home/vgpnk/Projects/shokunin/PROTOCOL.md:439-448` is the canonical seed. `diff -u` compared its seed lines (de-indented, `<name>` replaced with `kengaku-shokunin`) with `SHONEN.md` seed lines (1-5, 7, 9, 11); printed diff:
```diff
--- PROTOCOL-seed
+++ SHONEN-seed
@@ -2,7 +2,7 @@
 
 Promotion to shokunin requires all of:
 
-- [ ] SKILL.md contains real decision tables, error patterns, checklists, cited sources
-- [ ] At least one end-to-end domain task executed and logged in LOG.md
-- [ ] Instructions executable by an agent without oral context
-- [ ] No cross-domain bleed (PROVINCE.md still accurate)
+- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
+- [~] At least one end-to-end domain task executed and logged in LOG.md
+- [~] Instructions executable by an agent without oral context
+- [~] No cross-domain bleed (PROVINCE.md still accurate)
```
`direct_diff_exit=1` for the four required mark changes; after normalizing `[ ]` to `[~]`, `normalized_diff_exit=0` (exact seed match after required substitutions).

`test -e` every evidence pointer, from the private clone:
```text
test -e SKILL.md: PASS
test -e LOG.md: PASS
test -e corpus/README.md: PASS
test -e PROVINCE.md: PASS
```

Risks/blockers: none observed. Installs: none.
VERDICT: D17 regenerated; canonical seed matches after the required name/mark changes, and all four pointers resolve.