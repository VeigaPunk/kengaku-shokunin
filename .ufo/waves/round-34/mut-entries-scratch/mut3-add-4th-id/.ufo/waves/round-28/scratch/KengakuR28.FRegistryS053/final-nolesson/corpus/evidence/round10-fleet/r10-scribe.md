# ScribeReport — r10 evidence channel

Deliverable: `local://r10-report-draft.md` (61 lines, 18 placeholder lines, draft-only — L1 lands `.ufo/reports/round-10/kengaku.md`; nothing was written inside `kengaku-shokunin/`).

## Verification log (commands + terse output)

1. `git ls-tree -r 2575be6 --name-only | grep -cE '\.(py|sh)$'` → `12`; listing = 9× `corpus/evidence/round9-fleet/*.py` + `round8-horizon/horizon.py` + `round9-replication/{replicate.py,run_r9.py}` (L1's figure reproduced).
2. `find . \( -name '*.py' -o -name '*.sh' \) -not -path './.git/*' | wc -l` → `12` (same 12 paths; no `.sh`), while `SCORECARD.md:58` records this command → `11`. `git ls-tree -r f147a27 --name-only | grep -cE '\.(py|sh)$'` → `0` (before-side holds).
3. `test -e corpus/evidence/analyze.py` → exit `1`; `ls corpus/evidence/` → `round8-horizon round9-fleet round9-replication`. So `SCORECARD.md:83`'s named grader source does not exist; the analyzer on disk is `corpus/evidence/round9-fleet/analyze.py`.
4. `awk '/SUMMARY/{f=1} f' corpus/evidence/round8-horizon/run.log | head -25` → `=== SUMMARY ===` + exactly 11 count lines (A-INC 7/10, A-MONO 0/10, A-CKPT 1/10, B-corrupt-plain 3/8, B-corrupt-hint 3/8, B-clean-plain 6/8, B-clean-hint 6/8, C-conflict 4/4, C-benign 1/4, C-norule 4/4, C-MONO 4/4) — grounds the "11 SUMMARY lines" scope in the draft's move section.
5. `grep -n '## Planned\|Falsifiable target' SCORECARD.md` → `79:## Planned (next axis-move)`, `86:… Falsifiable target:`, `87:` (the `≥ 12` line) — the draft's citation `:79` / `:86-90` matches.
6. `git log --oneline -3` → `1bd17ec` (HEAD) / `2575be6` (round-9) / `3175e69`; `git status --porcelain` → empty (read-only against the repo; no git writes run).
7. `ls .ufo/reports/round-10/` → `kagi.md kake.md kasegi.md kotoba.md protocol.md` (no kengaku.md yet — L1 lands it).

## Provenance of the L2 fleet table

Rows transcribed from each peer's own dispatch brief via `read history://<Id>:1-22` on 2026-09-28 19:0x (ScoutEndpoint, ScoutWiki, ScoutBench, CriticScorecard, ReviewerCites, ConnectorSiblings, LabratSchema, MutationHarness, ExecutorDocs) — task text and `local://r10-*.md` artifact names are the briefs' own `# Target`/`# Acceptance` fields, not inferred. Roster cross-check: `read history://` lists all 11 sessions (Main + 10 L2) running.

## Open items handed to L1

- The draft's `{{WHICH_FILE_WAS_12TH}}`: which `.py` landed after SCORECARD's 11-count was taken is not recorded anywhere I could reach (single round-9 commit `2575be6`; working-tree mtimes are checkout-uniform) — stated as unrecorded rather than guessed.
- `{{RUNNABLE_COUNT_AFTER}}` must be re-measured after `grader.py` lands (expected 13 given the base of 12, not 12 given SCORECARD's stale base).
