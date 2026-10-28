<!-- R50C2ExecCorrections paste status (silent in rendered Markdown).
     MEASURED: the twelve SUPERSEDED rows of `## Round 50 — C2 corrections` are ALREADY in SCORECARD.md at the
     lane tip c3372a9b (lines 2136-2156, landed 822f3b7), and `python3 plans/round50_c2_audit.py --lane .` at
     c3372a9b prints `POINTERS total=277 paths=218 hashes=59 resolved=277 exists=206 superseded=3
     never-landed=9 unresolved=0`, exit 0.
     THEREFORE: §1 below is the only text to append now (row-level reasons + evidence commands, one line per
     pointer, in the order the audit prints them). Do NOT re-paste §2: it is the already-landed block, included
     so the rows can be diffed verbatim; re-pasting it would duplicate every SUPERSEDED row.
     Appending §1 keeps the audit green (re-measured on a c3372a9b image with §1 appended: unresolved=0, exit 0). -->

## §1 — append this (delta only)

### Round 50 — C2 corrections — row evidence

One line per `SUPERSEDED` row above, in the order `python3 plans/round50_c2_audit.py --lane .` printed the
pointers before the block landed (`UNRESOLVED` lines at 5c56819, alphabetical). Evidence commands run at
c3372a9b; `git log --all --oneline -- <pointer>` empty is what licenses `never-landed`.

- `corpus/defects.json` -> `corpus/defects.jsonl` — the audit's extension alternation stops at `.json`, so every `corpus/defects.jsonl` mention (SCORECARD:563,1180,1420) yields a `.json` token; the round-35 ledger landed as `.jsonl`. Evidence: `test -e corpus/defects.jsonl` (exists) · `git log --all --oneline -- corpus/defects.json` (empty).
- `corpus/evidence/analyze.py` -> never-landed — SCORECARD:113 records the path drift itself (`test -e` → absent); the analyzer on disk is `corpus/evidence/round9-fleet/analyze.py`, so there is no lane path to re-point at. Evidence: `git log --all --oneline -- corpus/evidence/analyze.py` (empty).
- `corpus/evidence/round9-replication/predictions-r9.sh` -> `corpus/evidence/round9-replication/predictions-r9.md` — the round-9 prediction artifact is the `.md` that the guard `predictions-r9.sha256.repo` hashes (SCORECARD:97); no `.sh` name ever existed. Evidence: `test -e corpus/evidence/round9-replication/predictions-r9.md` (exists) · `git log --all --oneline -- corpus/evidence/round9-replication/predictions-r9.sh` (empty).
- `corpus/knowledge/repo-git-state.md` -> never-landed — PROVINCE:416 cites **Kasegi's** entry of that name as a sibling precedent; this lane never held a copy. Evidence: `git log --all --oneline -- corpus/knowledge/repo-git-state.md` (empty).
- `corpus/routed-findings.json` -> `corpus/routed-findings.jsonl` — same `.json` prefix effect on the routed-defect ledger (SCORECARD:1572,1650,1721,1804,1841,1915,2084), which landed as `.jsonl` with 71 rows. Evidence: `test -e corpus/routed-findings.jsonl` (exists) · `git log --all --oneline -- corpus/routed-findings.json` (empty).
- `plans/round34_c1_verify.py` -> never-landed — SCORECARD:1168 names it as round-34 C1's counting command; round 34 closed as an honest stop with no counter committed. Evidence: `git log --all --oneline -- plans/round34_c1_verify.py` (empty).
- `plans/round34_defects.py` -> never-landed — SCORECARD:1169 names it as a round-34 C2 tool ("both tools absent" at freeze) and it never landed. Evidence: `git log --all --oneline -- plans/round34_defects.py` (empty).
- `plans/round34_mutate.py` -> never-landed — same round-34 C2 row (SCORECARD:1169): the mutation harness existed only as wave-dir candidate evidence. Evidence: `git log --all --oneline -- plans/round34_mutate.py` (empty).
- `plans/round48_c1_verify.py` -> never-landed — SCORECARD:2104's "Frozen command" cell; round 48 closed not admitted with no stage-2 landing-tip run and no committed counter. Evidence: `git log --all --oneline -- plans/round48_c1_verify.py` (empty).
- `plans/round48_c2_verify.py` -> never-landed — SCORECARD:2105's "Frozen command" cell; the r48 C2 probe was candidate evidence only. Evidence: `git log --all --oneline -- plans/round48_c2_verify.py` (empty).
- `plans/round49_c1_verify.py` -> never-landed — SCORECARD:2119 itself says the frozen command "is not present at landing". Evidence: `git log --all --oneline -- plans/round49_c1_verify.py` (empty).
- `plans/round49_c2_verify.py` -> never-landed — SCORECARD:2120's "Frozen command" cell, same wording ("not present at landing"). Evidence: `git log --all --oneline -- plans/round49_c2_verify.py` (empty).

## §2 — already landed at 822f3b7 (SCORECARD.md:2136-2156); reference only, do not re-paste

## Round 50 — C2 corrections

Append-only (PROTOCOL.md: corrections are new text, never a rewrite). The counting command is
`python3 plans/round50_c2_audit.py --lane .`; the rule and the before measurement (`POINTERS total=275 …
unresolved=12`) are frozen in `plans/round-50-claims.md` §C2. Each row below resolves one pointer that the
self-assessment files still carry and that does not resolve at the tip. `never-landed` is used only where
`git log --all --oneline -- <pointer>` is empty: the path was named in a row before it existed and never entered
the lane's history.

SUPERSEDED corpus/defects.json -> corpus/defects.jsonl
SUPERSEDED corpus/evidence/analyze.py -> never-landed
SUPERSEDED corpus/evidence/round9-replication/predictions-r9.sh -> corpus/evidence/round9-replication/predictions-r9.md
SUPERSEDED corpus/knowledge/repo-git-state.md -> never-landed
SUPERSEDED corpus/routed-findings.json -> corpus/routed-findings.jsonl
SUPERSEDED plans/round34_c1_verify.py -> never-landed
SUPERSEDED plans/round34_defects.py -> never-landed
SUPERSEDED plans/round34_mutate.py -> never-landed
SUPERSEDED plans/round48_c1_verify.py -> never-landed
SUPERSEDED plans/round48_c2_verify.py -> never-landed
SUPERSEDED plans/round49_c1_verify.py -> never-landed
SUPERSEDED plans/round49_c2_verify.py -> never-landed
