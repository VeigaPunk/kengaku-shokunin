# LessonsInventoryScout — round 25 (read-only)

Base observed: `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a round-25: pre-registration` (lane at `/home/vgpnk/Projects/shokunin/kengaku-shokunin`). No edits made outside this report.

## Commands and outputs

Command 1 — corpus enumeration and heading counts (anchored, GNU grep):
```
$ cd corpus/lessons && ls *.md | wc -l
26
$ grep -lE '^## Gate$' *.md | sort
round-13-coverage.md
round-24.md
$ grep -lE '^## Mistakes$' *.md | sort
round-24.md
$ comm -12 <(grep -lE '^## Gate$' *.md|sort) <(grep -lE '^## Mistakes$' *.md|sort)
round-24.md
```
Command 2 — operator-*.md existence (exact glob, then whole-lane case-insensitive find):
```
$ cd corpus/lessons && ls operator-*.md
ls: cannot access 'operator-*.md': No such file or directory
$ find . -iname '*operator*' -not -path './.git/*' -not -path './.jj/*'
(no output; exit 0 → zero matches)
```
Command 3 — independent cross-check with ripgrep:
```
$ rg -n '^## (Gate|Mistakes)$' corpus/lessons
corpus/lessons/round-13-coverage.md:24:## Gate
corpus/lessons/round-24.md:7:## Mistakes
corpus/lessons/round-24.md:56:## Gate
```
Command 4 — tracking/integrity of the population:
```
$ git ls-files corpus/lessons | wc -l        -> 26
$ git status --porcelain --untracked-files=all corpus/lessons  -> (empty)
$ file corpus/lessons/*.md | grep -i crlf    -> no CRLF
$ ls -la (lessons)                           -> no symlinks, no dotfiles
```

## Findings

1. Population is exactly 26 `corpus/lessons/*.md`, all git-tracked, none untracked, no CRLF, no symlinks/dotfiles (`git ls-files` 26 vs directory listing 26; command 4). [OBSERVED]
2. Files carrying `^## Gate$` (2): `corpus/lessons/round-13-coverage.md:24`, `corpus/lessons/round-24.md:56`. [OBSERVED]
3. Files carrying `^## Mistakes$` (1): `corpus/lessons/round-24.md:7`. [OBSERVED]
4. Intersection (both headings): exactly `corpus/lessons/round-24.md` — 1 of 26 (3.8%). Gate-only: `round-13-coverage.md`. Neither (24): `2026-10-16-round19-freeze-chain.md`, `2026-10-16-round20-grid-closure.md`, `2026-10-16-round21-attribution-freeze-surface.md`, `2026-10-16-round22-leg-coverage-forcing.md`, `2026-10-16-round23-stream-surface.md`, `round-1-aggregator-audit.md`, `round-1.md`, `round-11.md`, `round-12.md`, `round-13.md`, `round-14.md`, `round-16-recensus.md`, `round-24-verifier-spotcheck.md`, `round-3.md`, `round-4-aggregator-audit.md`, `round-4.md`, `round-5-aggregator-audit.md`, `round-5.md`, `round-6-aggregator-audit.md`, `round-7.md`, `round-8-aggregator-box3-coldrun.md`, `round-8.md`, `round-9-aggregator-corpus-verdict.md`, `round-9.md`. [OBSERVED]
5. Near-miss that is correctly excluded by the anchor: `corpus/lessons/round-8-aggregator-box3-coldrun.md:33` `## Gated steps (cannot cold-execute)` — different heading, not a match. No trailing-space or case variants exist (grep `^## (Gate|Mistakes)[[:space:]]+$` and `^#+ +(GATE|MISTAKES)` → none). [OBSERVED]
6. `corpus/lessons/operator-*.md` do NOT exist: exact glob fails; `find . -iname '*operator*'` over the whole lane returns zero results. Operator teachings have no represented file in this corpus, so any "operator teachings needing reflection" item cannot be discharged from a file that does not exist. [OBSERVED for absence; the location of such teachings, if any, is outside this lane and was not searched — out of scope.]
7. `corpus/lessons/round-25.md` is ABSENT at base. The round-25 frontier step (`plans/round-25-claims.md:102`, "`corpus/lessons/round-25.md` `## Mistakes`: mine at least one with a red-before demonstration") therefore creates a new file; the base corpus offers `round-24.md` as the only both-headings precedent to follow. [OBSERVED]
8. Historical cross-check: `round-13-coverage.md` Gate text (line 24 onward) states lessons "were 18 files / 17 indexed, with `round-16-recensus.md` missing". Current population is 26 tracked files; I did not re-derive index parity (P2e is another seat's population) and make no claim about it. [OBSERVED historical text; parity UNTESTED here]

## Confidence
Findings 1–7: high — grep and rg agree; git tracking and filesystem listing agree; absence confirmed by whole-lane `find`. Finding 8: index parity deliberately unclaimed, not measured.

## Installs

None. No pacman/uv/npx/cargo transaction was run; no network contact.

VERDICT: 26 lesson files, all tracked; `^## Gate$` in 2 (`round-13-coverage.md:24`, `round-24.md:56`), `^## Mistakes$` in 1 (`round-24.md:7`), both in exactly `round-24.md`; zero `operator-*.md` anywhere in the lane; `round-25.md` absent.
