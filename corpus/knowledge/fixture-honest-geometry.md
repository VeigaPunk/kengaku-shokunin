source: corpus/SOURCES.md S173, S174, S175, S176, S177 (git v2.56.0 documentation: gitrepository-layout, git-init, git-worktree, git-replace, git-fetch), fetched 2026-10-28, captures at corpus/evidence/round50/*.adoc
verified-at: 2026-10-28 (round 50; population `plans/honest50/population.txt` pin b5197f94…, counter `plans/round50_c1_verify.py`)
recheck: `python3 plans/round50_c1_verify.py --lane .` prints `HONEST fixtures=126 admitted=126 refused=0`; the five cited classes rebuild from `plans/honest50/modules/{novel49,novel50}/*.py` and their identity pins.

# Fixture honest-geometry: what a git store may honestly look like inside a fixture

A fixture fence decides whether a fixture's git store, discovered repositories and argv stay inside the fixture
directory `d`. Deciding that by **shape** ("a plain init writes exactly these entries") over-refuses ordinary
repository states, because git itself writes more than a plain init writes. The documented states this lane's
population now holds, each with the source that documents it:

| class | documented shape | source |
|---|---|---|
| `n20` linked worktree | work tree carries a `.git` **file** naming `repo/.git/worktrees/<id>`; that entry carries a `gitdir` back-pointer | S175 (git-worktree), S173 (gitrepository-layout `worktrees/<id>/gitdir`) |
| `n21` separate gitdir | `git init --separate-git-dir` writes a text file `.git` holding the path to the real store | S174 (git-init), S173 (the "gitfile" mechanism) |
| `n22` alternates inside `d` | `objects/info/alternates` records object stores the repository borrows from, one pathname per line | S173 |
| `n17` replace refs | `refs/replace/<object>` is a ref whose **name** is the SHA of the replaced object | S176 (git-replace) |
| `n18` shallow boundary | `.git/shallow` is written and maintained by the shallow-clone mechanism; `FETCH_HEAD` records the fetched refs and their objects | S173 (shallow), S177 (git-fetch `FETCH_HEAD`) |

The consequence for the fence: a refusal keyed on `.git` being a directory, on `refs/heads|tags` being the only
ref namespaces, or on `objects/info` being empty refuses states that are inside `d` and that git writes by
documented mechanisms. The honest distinction is **containment after resolution**, not the entry name: a gitfile
whose target resolves inside `d` names a store that may be classified; one that resolves outside is a redirect.

## Measured, not asserted

- Base fence (`05d5fe03…`) on the frozen 126-fixture population: `HONEST fixtures=126 admitted=113 refused=13`
  (receipt `.ufo/waves/round-50/claims/c1-control-do-nothing.txt`).
- The 126 fixtures are the 104 battery fixtures of `plans/battery42|43|44` plus 22 novel documented classes
  (`plans/honest50/modules/{r46novel,novel48,novel49,novel50}`), each pinned by canonical tree digest in
  `plans/honest50/population.txt` (sha256 `b5197f94…`).
- The refusal leg is 20 frozen modules (`plans/refusals46/`) plus the blind set (`plans/sealed46/`, round-50
  `plans/sealed50/`); the counter's predicate sentence is in `plans/round-50-claims.md` §C1.

## Scope limits

The population is "states git itself writes", not "every state a third-party tool may write". A `commondir` file
on a standalone repository is **not** in the population: git writes `commondir` only for a linked worktree, which
`n20` already holds. io_uring and reads outside the scratch root are outside this counter (the round-46 counter
remains the instrument for the outside-read property). Identity pins are host-git-sensitive where git output is
(`hooks/*.sample`, `info/exclude`, `worktree --relative-paths`); a pin mismatch is reported, never silently
re-pinned.
