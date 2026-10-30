# Freeze integrity + working-tree drift audit — SN4FreezeIntegrity (round 55, w1)

Audit target: freeze commit `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` of
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, its claims blob, and every lane file
drifted since it, checked against the wave's declared write scopes
(`.ufo/waves/round-55/w1-dispatch.json`, `taskCall.tasks[*].task` + `registry.members`).
All git invocations read-only (`git -C …`, `rev-parse`, `hash-object`, `diff`, `status`,
`log`, `show`). Audit time: 2026-10-30 ~12:45–12:55 -0300.

## Section 1 — Freeze commit file list: MATCH (no finding)

`git -C <lane> show --stat 80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (exit 0):

| # | File | Stat |
|---|------|------|
| 1 | `.ufo/waves/round-55/claims/c1-before.txt` | 13 ++ |
| 2 | `.ufo/waves/round-55/claims/c2-before-abbreviated-selftest.txt` | 12 ++ |
| 3 | `.ufo/waves/round-55/claims/c2-before-uv-decoy-script.txt` | 12 ++ |
| 4 | `.ufo/waves/round-55/claims/c3-before.txt` | 10 ++ |
| 5 | `.ufo/waves/round-55/claims/census-before.txt` | 16 ++ |
| 6 | `plans/round-55-claims.md` | 151 +++++ |
| 7 | `plans/round55_c2_controls.py` | 199 +++ |

Exactly the expected 7 files (claims + controls builder + 5 before-receipts), `7 files
changed, 413 insertions(+)` — pure additions, no deletions, no extra file. Parentage:
`git log -1 --format='%P'` → `798f5e9ef30ef39291295565209b65a17343c00e`, exactly the
recorded base tip (author `kengaku-shokunin <kengaku@shokunin.local>`, 2026-10-30
11:53:35 -0300, subject "round-55: claims frozen before data …").
`git log --oneline 80afa61..HEAD` is empty and `git rev-parse HEAD` → `80afa61…`:
**nothing has landed on top of the freeze.**

## Section 2 — Claims blob identity: MATCH (no finding)

Working tree `plans/round-55-claims.md` is byte-identical to the frozen blob:

- committed: `git rev-parse 80afa61:plans/round-55-claims.md` → `8b2997ce3d44ccab3fed4843fbc895e4a7ea35e7`
- worktree: `git hash-object plans/round-55-claims.md` → `8b2997ce3d44ccab3fed4843fbc895e4a7ea35e7`
- `git diff 80afa61 -- plans/round-55-claims.md` → 0 bytes (empty diff)

Second frozen file corroborated: `plans/round55_c2_controls.py` committed
`85813b1da6aa4f9cc51174f612b5b048e197282b` == worktree `hash-object`. All five
before-receipts clean: `git status --porcelain -- .ufo/waves/round-55/claims/` → empty.
The frozen predicates, counters, kill rules and controls the wave is scoring against are
exactly the bytes at commit time.

## Section 3 — Drift since freeze vs declared write scopes: NO OUT-OF-SCOPE WRITE

HEAD == freeze commit, so all drift is working-tree drift:
`git diff --name-only 80afa61` (tracked, 3) + `git status --porcelain` (same 3 `M`
plus untracked). Every entry resolved against the dispatch's declared seat scopes:

| Drift entry | Declared owner (dispatch) | Content check | Verdict |
|---|---|---|---|
| `M PROVINCE.md` | **E9IndexAndReadme** (names PROVINCE.md) | +round-55 partial-frontier paragraph, "12 of 89 read" → "13 of 89" — the exact after-state the frozen claims declare for R55-C3 | in scope |
| `M corpus/README.md` | **E9IndexAndReadme** (names corpus/README.md) | +knowledge index row for `tb2-chess-best-move-grader.md`, +Frontier narrowing note (13 of 89), +round-55 evidence section — the claims' declared after-state | in scope |
| `M corpus/SOURCES.md` | **E8SourcesRows** (names corpus/SOURCES.md) | +S201 (grader, code A) and S202 (instruction, docs A), mined 2026-10-30, used-by the chess entry — the claims' declared rows | in scope |
| `?? plans/round55_c2_entryargv.py` | **E2EntryArgvCounter** (instrument author) | R55-C2 instrument, new file | in scope |
| `?? plans/round55_c3_chess_probe.py` | **E5ChessProbe** (instrument author) | R55-C3 probe, new file | in scope |
| `?? corpus/evidence/round55/` | **E6ChessReceipt** (writes chess-best-move-probe.txt there) | evidence dir | in scope |
| `?? corpus/knowledge/tb2-chess-best-move-grader.md` | **E7KnowledgeEntry** (writes the entry) | knowledge entry | in scope |
| `?? corpus/lessons/round-55.md` | **S3GateQuotes** (writes the round lesson / gate block) | lesson file | in scope |
| `?? .ufo/waves/round-55/{build_spec_w1.py, w1-spec.json, w1-dispatch.json, w1-run.err, w1.ready, w1.ready.partial}` | **Orchestrator/L1 wave machinery** — no seat declares writes to them | mtimes 12:19:59–12:21:00 (spec build → dispatch 12:20:53 → ready 12:21:00, i.e. at/before seat dispatch); seat tasks that reference `w1-dispatch.json`/`w1-spec.json` (S1CaseProse, C9AttackShare) say "Read …" only — verified in their task texts | orchestrator-owned, not a seat write |
| `?? .ufo/waves/round-55/w1/` | **All seats** — each seat's declared output dir `w1/<seat>*/` per dispatch | seat reports/receipts | in scope |

**Findings (seat writing outside its scope): none.** Attribution caveat, stated honestly:
the three tracked edits are uncommitted, so git carries no author; attribution rests on
(a) each file being named in exactly one seat's declared write scope and (b) the diff
content matching that claim-declared after-state line for line. Both hold for all three.

Forbidden zones clean: `MANIFEST.json`, `.ufo/state/`, `.ufo/watchdog.log`, fleet-root
`scripts/`/`templates/`, `.scratch/` — none appear in status or the diff. No mutating git
command was run by this seat.

Minor observation (not a violation): `.ufo/waves/round-55/w1.ready.partial` existed at
`status --porcelain` time and was gone when `stat` ran minutes later — orchestrator-managed
readiness marker, wave machinery live during the audit window.
