# Round 32 — R32RevFixes: review of the routed errata draft (D1 / D3 / D6 / R7)

Object reviewed: `.ufo/waves/round-32/build/R32DraftErrata.md`, **current copy** — 5 247 B, sha256
`db618b794e08ef28524974291c469987b8ffd6e0dce04c714ac14e8d824cd151`, mtime 09:48:16, 71 lines, four drafted texts
+ `VERDICT: errata-drafted`. Revision trail reviewed in place: `3664fe09` → `544e140b` → `db618b79`. The delta from
the copy certified in the previous pass is two lines of prose at `:25-26` (an execution note about `set +e`); it sits
**outside** the ` ```text ` receipt block — verified programmatically, `"set +e" in note` → `False` — so it cannot
inject a stale token into the regenerated receipt. All four checks were re-run on these exact bytes (below), not
carried over from the earlier copy.

Standard: the real predicates in `plans/round32_defects.py` (R1, R3, R6, R7), **executed** — not eyeballed —
against a `/tmp` tree carrying the drafted texts verbatim, appended to copies of the four target files. Every
factual claim in the draft was re-derived from committed bytes. No production file was written by this seat.

## End-to-end simulation (decisive evidence)

`/tmp/r32-R32RevFixes/sim4/` = copies of `.ufo/reports/round-31/kengaku.md`, `corpus/lessons/round-31.md`,
`corpus/lessons/round-30.md`, plus a receipt rebuilt as §(b) now instructs; the drafted (a)/(c)/(d) quote blocks and
the ` ```text ` correction note extracted programmatically from the current draft and applied; the module's path
globals repointed; the real check functions called:

```
receipt note: lines=8, contains can't-open-file=False
R1: PASS
R3: PASS
R6: PASS
R7: PASS
receipt: lines=24 can't-open-file=0 exits=[0, 8, 9, 0, 2]
```

Control for the one defect this review raised and the drafter fixed — same receipt file with the drafted correction
note *appended* to the tip copy instead of replaced:

```
R3 on append-only application: FAIL -> the tip receipt still contains 'can't open file' failure lines
```

Both runs use `check_r3` unmodified. The divergence is gone from the current draft because §(b) now says
"Regeneration **replaces** … wholesale … the stale `can't open file` block of the tip copy must not survive".

## Per-item result

| Item | Drafted text (current copy) | Predicate | Ground truth re-derived | Result |
|---|---|---|---|---|
| (a) D1 | erratum naming §"Erratum addendum (2026-10-25, trend-verdict seat)", the `a44b5a8`-class citation as bogus, "it is superseded", and `ae95fe0` with the two locators it fixed | R1 | `git cat-file -t a44b5a8` → `fatal: Not a valid object name`; `git rev-parse --disambiguate=a44b5a8` → empty; `ae95fe0` is an ancestor of `master`, subject "round-31: entry locator corrections (verifier_mode.py:18-21, :39-40) and final falsify evidence", diff carries `:22-23`→`:18-21` and `:35-38`→`:39-40` | **pass** |
| (b) D3 | wholesale replacement of `corpus/evidence/round31/gate-cli-exits.txt` from `.ufo/waves/round-31/c3-fixtures` with `../../../../plans/sources_adopt.py`; five commands; correction note | R3 | every drafted command executed verbatim: **map-ok=0, map-bad=8, map-unmapped=9, no map=0, url-map on registry path=2** (`sources_adopt.py: error: --url-map needs --quote-file and --artifact`, `plans/sources_adopt.py:1039-1040`); rebuilt file: 24 lines, 0 `can't open file`, five executed exit lines, all four exit tokens, corrected path | **pass** |
| (c) D6a | lesson-31 note: precedence locator `:39-40`, not `:35-38` | R6 (lesson31) | pin `6099b8cf…`: `verifier_mode.py:39-40` = "Order of precedence: explicit step mode > step environment implies / separate > inherit task-level resolution > default shared."; `:35-38` is the `resolve_step_verifier_mode` signature region | **pass** |
| (d) D6b | lesson-30 note: `contamination-transparency-card.md:78-81` stale → `:72` / `:82-83` in that entry | R6 (lesson30) | card `:72` = "So the delta is one field, and the rest is not a delta at all…"; `:82-83` = "…Two earlier readings of this paragraph (…one field, one placement, one value set") overclaimed; this is the corrected one"; `:78-81` now holds the strata paragraph, neither quote | **pass** |
| (e) R7 | lesson-30 erratum: `:66` "S083/S086 peer-reviewed" wrong for S086 | R7 | `corpus/SOURCES.md:110` (S086 cell): "the society publishes these proceedings **without peer review**"; lesson `:66`: "S081/S082 preprints vs S083/S086 peer-reviewed" | **pass** |

Append-only compliance: every superseded byte survives at tip — report `:226` (`a44b5a8`), lesson-31 `:57`
(`:35-38`), lesson-30 `:197` (`:78-81`) and `:66` (`peer-reviewed`) — so (a), (c), (d), (e) rewrite nothing; (b) is
the receipt regeneration the claim itself specifies, now labelled as such rather than as an append.

Draft's "Verified grounds" section, re-checked rather than accepted: `634ded8` is a real commit ("round-31: C3
receipts regenerated on landed bytes, S100 word count, lesson debt") and its receipt records `0 / 8 / 9 / 0 / 2` in
exactly the five slots the draft names; the cited spot-check window `:147-170` carries D1 (`:149`), D3 (`:154`),
D6 (`:165`) and the S086 carried debt (`:168`). No phantom-hash class of error in the draft itself.

## Findings — all four raised by this review are closed in the current bytes

- **F1 (was the only open defect, D3) — closed.** The artifact previously labelled D3 append-only and never said how
  the regenerated output enters the receipt file; the append reading fails R3 on its first clause (measured above,
  5 `can't open file` occurrences at tip). Now: scope line separates "append-only … D1, D6, and R7" from "the D3
  CLI-receipt regeneration (the receipt is regenerated wholesale …, not appended to)", and §(b) states the
  replacement and that the stale block must not survive. Verified by the PASS/FAIL pair above.
- **F2 (was medium, D3) — closed.** All five receipt lines are now regenerated commands, not prose: `no map` and
  the `--url-map` + `--registry/--package` guard included, both executed here (`0`, `2`). The guard exits before any
  file is opened, so the absent `corpus/SOURCES.append.md` is never touched — the note's parenthetical is accurate.
- **F3 (was minor, D1) — closed.** The erratum now locates the superseded sentence and names the two locators
  `ae95fe0` fixed, which is what makes the supersession checkable without trusting a token.
- **F4 (was minor, D6b) — closed.** The (d) note now names `corpus/knowledge/contamination-transparency-card.md`,
  so `:72`/`:82-83` cannot be misread as lesson-local refs.

## Residual risk / verification gaps

- **Application scope for D1.** The repair lands in the fleet repo (`.ufo/reports/round-31/kengaku.md`), which leaf
  seats are barred from writing. The draft is correct; the application needs the seat holding fleet-report write
  scope, else C2's kill rule applies and D1 is reported open.
- **D6 locators are a moving target.** `:72`/`:82-83` are correct at tip `6084cd3`; any later edit to the card
  re-stales them, and R6 only tests presence of both tokens plus a label.
- **The counter is a token test.** `near(…, ":72", "82-83", 300)` and `near(…, "S086", "without peer review", 250)`
  are satisfied by wording alone; the round-31 lesson's admission that `defects=0` is necessary-not-sufficient
  applies unchanged. The value of this review is the byte-level re-derivation and the simulation, not the green line.
- **Application hazard for the D3 commands — now carried by the draft itself.** The drafted block is correct in a
  normal shell but aborts under `set -e` on the first failing run: measured with an explicit `set -e` wrapper, the
  loop printed `url-map map-ok -> exit=0` and stopped (script exit 8), leaving a truncated receipt. The current draft
  folds this in as an execution note at `:25-26` ("run the block with `set +e` (or without errexit)…"), which I
  verified sits outside the ` ```text ` block and therefore cannot pollute the receipt. The failure is self-detecting
  anyway — R3 reported `the regenerated receipt lacks exit=8` on the truncated file — but it costs a cycle.
- **Counter provenance (sibling edit during this review) — checked against the freeze commit.** `git status` shows
  `plans/round32_defects.py` and `plans/catalog_probe.py` modified in the working tree by other seats. Comparing the
  **frozen** file (`git show 0d32691:plans/round32_defects.py`; `0d32691` and `6084cd3` are identical for it) against
  the working tree function by function: `check_r3`, `check_r6`, `check_r7` are **byte-identical**, and `check_r1`
  differs only in its signature and the path variable it reads (`read(R31_REPORT)` → `read(r31_report)`), with the
  decision logic from that line onward identical; `check_r2` gains the same fixture-path parameter, plus three new
  selftest cases. This review imported the **working-tree** copy, so every PASS above is against current bytes and
  against the frozen predicates. The frozen C2 control (`defects=7` on the pre-repair tree) should still be replayed
  after that edit, and the edit disclosed in the wave report — a predicate edited after a seat scored is exactly the
  case `plans/round-32-claims.md` says is not that claim's predicate. (The drafter has taken both actions.)
- **Not in scope here:** R2, R4, R5; whether the round-31 SCORECARD C3 row's "0 / 8 / 9 / 2" cell is restated after
  regeneration (D3's second half in the spot-check).
- **Tool installs:** none — no pacman, no uv, no binary fetch. Scratch stayed in `/tmp/r32-R32RevFixes/` (one ~5 KB
  `verifier_mode.py` fetch at the pinned commit).

VERDICT: errata-clean
