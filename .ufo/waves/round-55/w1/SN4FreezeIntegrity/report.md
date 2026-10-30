# SN4FreezeIntegrity — seat report (round 55, w1)

Seat: freeze commit integrity + working-tree drift audit. Read-only + my wave dir only.
Full three-section audit: `.ufo/waves/round-55/w1/SN4FreezeIntegrity/integrity.md`.

## Verdict

- **Section 1 — freeze commit file list: MATCH.** `80afa61` (parent exactly the recorded
  base tip `798f5e9e…`, pure additions, 7 files / 413 insertions) contains exactly
  `plans/round-55-claims.md`, `plans/round55_c2_controls.py` and the five
  `.ufo/waves/round-55/claims/{c1-before, c2-before-abbreviated-selftest,
  c2-before-uv-decoy-script, c3-before, census-before}.txt` receipts. Nothing landed
  on top (`80afa61..HEAD` empty, HEAD == `80afa61`).
- **Section 2 — claims blob identity: MATCH.** Worktree `plans/round-55-claims.md`
  blob `8b2997ce…ea35e7` == committed blob; `git diff 80afa61 -- plans/round-55-claims.md`
  is 0 bytes. Corroborated `plans/round55_c2_controls.py` (`85813b1d…` both) and clean
  status for all five before-receipts.
- **Section 3 — drift vs declared scopes: NO OUT-OF-SCOPE WRITE, no finding.**
  Tracked edits: PROVINCE.md + corpus/README.md (declared: E9IndexAndReadme; content =
  the frozen claims' declared R55-C3 after-state, "13 of 89" narrowing) and
  corpus/SOURCES.md (declared: E8SourcesRows; S201/S202 exactly as claimed).
  Untracked: E2/E5/E6/E7/S3 declared instrument/entry/evidence/lesson files, all-seat
  report dirs under `w1/`, and orchestrator wave machinery
  (`build_spec_w1.py`, `w1-spec.json`, `w1-dispatch.json`, `w1-run.err`, `w1.ready`,
  `w1.ready.partial` — mtimes at/before dispatch; seat tasks referencing them say
  "Read" only, verified in S1CaseProse/C9AttackShare task texts). Forbidden zones
  (MANIFEST.json, .ufo/state/, .ufo/watchdog.log, fleet-root scripts/templates,
  .scratch/) untouched.

## What I ran (all exit 0 unless noted)

1. `git -C kengaku-shokunin show --stat 80afa61…` — expected 7-file list, got exactly it.
2. `git -C kengaku-shokunin log -1 --format='parents=%P …' 80afa61…` — parent `798f5e9e…`.
3. `git -C kengaku-shokunin rev-parse 80afa61:plans/round-55-claims.md` and
   `git hash-object plans/round-55-claims.md` → both `8b2997ce…`;
   `git diff 80afa61 -- plans/round-55-claims.md | wc -c` → 0.
4. `git -C kengaku-shokunin rev-parse 80afa61:plans/round55_c2_controls.py` and
   `git hash-object` → both `85813b1d…`; `git status --porcelain -- .ufo/waves/round-55/claims/`
   → empty.
5. `git -C kengaku-shokunin diff --name-only 80afa61…` → PROVINCE.md, corpus/README.md,
   corpus/SOURCES.md. `git status --porcelain` → same 3 `M` + untracked list (12 entries).
6. `git log --oneline 80afa61..HEAD` → empty; `rev-parse HEAD` → `80afa61…`.
7. Scope attribution: `jq -r '.taskCall.tasks[] …'` over
   `.ufo/waves/round-55/w1-dispatch.json` mapping every task to the lane paths it names;
   targeted extraction of S1CaseProse/C9AttackShare task texts to confirm their
   `w1-dispatch.json`/`w1-spec.json` mentions are read-only.
8. `stat -c '%y %n'` on the 12 drifted paths — provenance/mtimes
   (exit 1 only because `w1.ready.partial` vanished between status and stat; noted, not a defect).

## Files written

- `.ufo/waves/round-55/w1/SN4FreezeIntegrity/integrity.md` (the named Change target)
- `.ufo/waves/round-55/w1/SN4FreezeIntegrity.md` (Report-trailer path)
- `.ufo/waves/round-55/w1/SN4FreezeIntegrity/report.md` (this contract report copy)

## Defects found

- **None in scope.** No seat wrote outside its declared write scope; no frozen file or
  blob drifted; nothing landed on the freeze.

## Caveats / dead ends

- The three tracked edits are uncommitted, so authorship is not git-provable; attribution
  to E9/E8 rests on unique scope naming + exact content match with the frozen claims'
  after-state. Both hold; recorded as such rather than overstated.
- `w1.ready.partial` was deleted by the orchestrator mid-audit (existed at status time,
  gone at stat time) — machinery observation only.
- No installs performed; no network used; no mutating git/jj command run anywhere;
  scratch dir `/fast/scratch/hyaku/kengaku-r55/SN4FreezeIntegrity/` created and removed
  empty before yield.
