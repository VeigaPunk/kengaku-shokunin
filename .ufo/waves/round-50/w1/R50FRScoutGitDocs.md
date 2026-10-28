# R50FRScoutGitDocs — git documentation rows for R50-C1

Axes: (1) located-quote — ≤25 whitespace words and a byte substring of the fetched file, section named; (2) pin-identity — HTTP status, access date, sha256 equals `corpus/evidence/round50/`; (3) manual-attribution — the manual the item names actually contains the term; (4) id-collision — proposal does not reuse S173–S177 or the historical gaps; (5) anchor-accuracy — a cited line range contains the quoted bytes.

REV c3372a9b24d3a200946a6b37dc0a31ed5c982cc1

Freeze `3b02d573d58cc6d2e0d27ef92ac0815354912252` is an ancestor of that tip (`git merge-base --is-ancestor` exit 0). Base `71f5f5f77591d8c3d19297ee9785436da45209e4` is an ancestor of the freeze (exit 0). Host `git version 2.56.0`. Measured on `git clone --shared` of the lane; `corpus/SOURCES.md` was not edited.

## Commands

```
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
git -C … merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
curl -sS -L -D "$name.hdr" -o "$name.body" -w '%{http_code}' <url>
sha256sum of each body, compared to corpus/evidence/round50/*.adoc
```

`HEAD` at measurement was `c3372a9b24d3a200946a6b37dc0a31ed5c982cc1` (2026-10-28 14:25:30 -0300, counter attribution repair). Sources commit `822f3b748306ec6918a415bc713f9688a3de20e7` is an ancestor and is the commit that adds S173–S177. Those five rows are absent at the freeze and at `71f5f5f` (registry 165 rows, last id S172). At REV the registry is 170 rows, last id S177. Historical gaps, not reusable: S087–S089, S095–S096, S098–S099.

## Fetches (access date 2026-10-28)

Pin is the raw tag file, not the unversioned HTML. Each adoc sha256 equals both the S173–S177 anchor cell and `corpus/evidence/round50/<file>`.

| body | HTTP | Date header | bytes | sha256 |
|---|---|---|---|---|
| `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc` | 200 | Wed, 28 Oct 2026 17:38:58 GMT | 11890 | `39ce8d137a30e1fd80eeae146b1c424e56f688f4ddd001259eb98543d3209439` |
| `…/git-init.adoc` | 200 | Wed, 28 Oct 2026 17:38:58 GMT | 6227 | `123096436d7d47b718483fdfbc1660446474a77b2a5b33212f5360af89ca2f95` |
| `…/git-worktree.adoc` | 200 | Wed, 28 Oct 2026 17:39:02 GMT | 22021 | `ee8a368564ace74a07e4a034e080b26fb1c3b35d17ef1fe41dcbfcc5595fe8dc` |
| `…/git-replace.adoc` | 200 | Wed, 28 Oct 2026 17:39:02 GMT | 5398 | `3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631` |
| `…/git-fetch.adoc` | 200 | Wed, 28 Oct 2026 17:39:02 GMT | 11825 | `fd225a09cb7bdb687cff4ba161cb1f337f2523eac5f83db5dbbbb1ef216fa41e` |
| `https://git-scm.com/docs/gitrepository-layout` | 200 | Wed, 28 Oct 2026 17:39:03 GMT | 64401 | page says "last updated in 2.49.0" and "2.49.1 → 2.56.0 no changes" |
| `https://git-scm.com/docs/git-init` | 200 | Wed, 28 Oct 2026 17:39:06 GMT | 60034 | "last updated in 2.54.0"; `--separate-git-dir` paragraph matches the adoc |
| `https://git-scm.com/docs/git-worktree` | 200 | Wed, 28 Oct 2026 17:39:06 GMT | 98918 | "last updated in 2.56.0" |
| `https://git-scm.com/docs/gitrepository-layout/2.56.0` | 301 then 200 | Wed, 28 Oct 2026 17:39:07 GMT | 629 | HTML stub redirecting to `/docs/gitrepository-layout/2.49.0` |
| `https://git-scm.com/docs/git-init/2.56.0` | 301 then 200 | Wed, 28 Oct 2026 17:39:10 GMT | 593 | stub redirecting to `/docs/git-init/2.54.0` |
| `https://git-scm.com/docs/git-worktree/2.56.0` | 200 | Wed, 28 Oct 2026 17:39:10 GMT | 98789 | full page, no stub |

`FETCH_HEAD` occurs 0 times in the layout adoc and 0 times in installed `gitrepository-layout(5)`. The filename `commondir` occurs 0 times in the worktree adoc and 0 times in installed `git-worktree(1)` (`GIT_COMMON_DIR` occurs 6 times in both). Installed `git-init(1)` has `separate\-git\-dir` 3 times (roff hyphen escapes, so a raw `separate-git-dir` count is 0).

Quote test replicated from `plans/sources_adopt.py` `normalize_text` (CRLF→LF only) plus `quote in text` and `len(quote.split())`. Not a `quote_check` process run. A quote that joins a wrapped line with a space is absent; the same words with the file's newline (and tab, when the next line is indented) are present.

## Located quotes (≤25 words)

`\n` and `\t` below are the file's own newline and tab.

1. `gitrepository-layout(5)` section `objects/info/alternates` (`:80-83`), 19 words, substring yes:
   `This file records paths to alternate object stores that\n\tthis object store borrows objects from, one pathname per\n\tline.`
2. `gitrepository-layout(5)` section `refs/replace/<obj-sha1>` (`:116-117`), 9 words, substring yes:
   `records the SHA-1 of the object that replaces `<obj-sha1>`.`
3. `gitrepository-layout(5)` section `shallow` (`:261-263`), 15 words, substring yes:
   `This is similar to `info/grafts` but is internally used\n\tand maintained by shallow clone mechanism.`
4. `FETCH_HEAD` is not a `gitrepository-layout(5)` section. `git-fetch(1)` DESCRIPTION (`:41-42`), 19 words, substring yes:
   `The names of refs that are fetched, together with the object names\nthey point at, are written to `.git/FETCH_HEAD`.`
5. `gitrepository-layout(5)` section `commondir` (`:272-273`), 12 words, substring yes:
   `The repository with commondir is\n\tincomplete without the repository pointed by "commondir".`
6. `git-init(1)` OPTIONS `--separate-git-dir=<git-dir>` (`:69-73`), 25 words, substring yes:
   `` `./.git/`, create a text file there containing the path to the actual\nrepository.  This file acts as a filesystem-agnostic Git symbolic link to the\nrepository. ``
7. `git-worktree(1)` does not name `commondir`. The gitfile + common-dir pair is DETAILS (`:363` heading, `:374-378`): `$GIT_DIR` points at `worktrees/<id>` and `$GIT_COMMON_DIR` points at the main store, both recorded in a `.git` file. Two substrings: 11 words `` `$GIT_COMMON_DIR` is set to point back to the main worktree's `$GIT_DIR` `` (`:376`); 17 words `These settings are made in a `.git` file located at\nthe top directory of the linked worktree.` (`:377-378`). The back-pointer file `worktrees/<id>/gitdir` is layout `:285-287`, 16 words, substring of the layout adoc only:
   `A text file containing the absolute path back to the .git file\n\tthat points to here.`
   The gitfile token itself is layout `:25-26`, 13 words: `` containing `gitdir: <path>` to point at the real\ndirectory that has the repository. ``

`git-replace(1)` DESCRIPTION is the name half that layout's `:117` does not say. `:20` (7 words, substring yes): `Adds a 'replace' reference in `refs/replace/` namespace.` `:22-23` (15 words, substring yes only with the newline): `The name of the 'replace' reference is the SHA-1 of the object that is\nreplaced.`

## Landed anchors vs these bytes

Lesson `corpus/lessons/round-50.md` quotes (space-joined) are not substrings, except S176's first sentence:

| lesson quote | words | `in` the cited adoc |
|---|---|---|
| S173 alternates sentence with spaces instead of `\n\t` | 19 | no |
| S174 through "symbolic link to the" | 23 | no |
| S175 "A text file containing the absolute path back to the .git file that points to here." | 16 | no in `git-worktree.adoc` (also no in the layout adoc once the newline and tab are removed) |
| S176 first sentence | 7 | yes (`:20`) |
| S176 second sentence, space-joined | 15 | no (`:22` ends at "is") |
| S177 FETCH_HEAD sentence, space-joined, backticks kept | 19 | no (`:41`/` :42` are split by a newline) |

S175's anchor `:285-292` on `git-worktree.adoc` is `--expire`'s `_<time>_`, then `--reason <string>`, then `_<worktree>_`. It does not contain a gitdir sentence. The sentence the lesson quotes is `gitrepository-layout.adoc:286-287` (`worktrees/<id>/gitdir`). S175's second range `:395-401` does match the worktree "update the `gitdir` file" paragraph.

S177's anchor `:42-43` starts one line late: the sentence begins at `:41`. `:43` is the following sentence (`may be used by scripts…`).

S174's anchor `:69-72` stops before `:73` `repository.`, the last word of the option paragraph.

S173's `:26-28` includes the word gitfile (`:27`) but not `` `gitdir: <path>` ``, which is `:25`. `:80-83` and `:261-273` do cover alternates, shallow, and commondir. `:116-120` (`refs/replace/<obj-sha1>`) is not in the S173 anchor.

## Proposed rows

No new id. Occupied this round: S173–S177. Next free id is S178; do not fill S087–S089, S095–S096, or S098–S099. Tier stays A (official manual at the host's git version). Kind stays `docs`. Status stays `mined`. Do not edit `SOURCES.md` from this seat.

| id | tier | scope | anchor to use |
|---|---|---|---|
| S173 | A | on-disk files git writes in a repository: gitfile, `objects/info/alternates`, `refs/replace/<obj-sha1>`, `shallow`, `commondir` | `gitrepository-layout.adoc` tag v2.56.0: `:24-28`, `:80-83`, `:116-120`, `:261-266`, `:268-273`; sha256 `39ce8d13…d3209439`. Add `:116-120`. Widen `:26-28` to `:24-28`. |
| S174 | A | `git init --separate-git-dir` writes a text file where `.git` would have been, holding the path of the real repository | `git-init.adoc:69-73` (not `:69-72`); sha256 `12309643…89ca2f95` |
| S175 | A | a linked worktree's `.git` file sets `$GIT_DIR` to `worktrees/<id>` and `$GIT_COMMON_DIR` back to the main store; `gitdir` is the back-pointer file. Not the filename `commondir` | replace `:285-292` with DETAILS `:374-378`; keep `:395-401`; sha256 `ee8a3685…595fe8dc` |
| S176 | A | a replace ref's name is the SHA-1 of the object replaced; its content is the replacement SHA-1 | `git-replace.adoc:20` and `:22-24`; sha256 `3f61be3f…74640631` |
| S177 | A | a completed fetch writes fetched ref names and object names to `.git/FETCH_HEAD`. Not a layout(5) entry | `git-fetch.adoc:41-42` (not `:42-43`); sha256 `fd225a09…216fa41e` |

`commondir` as a filename stays on S173. The worktree half of the pair stays on S175. `refs/replace/` 's directory entry stays on S173; the name/content rule stays on S176. `FETCH_HEAD` stays on S177. Opening S178+ would duplicate those URLs.

## Limits

Quotes are from the v2.56.0 adoc pin. The unversioned git-scm.com HTML agrees on the init paragraph and says layout did not change from 2.49.1 through 2.56.0, but those pages are not the pin (the `/2.56.0` layout and init URLs are redirect stubs). The substring test replicates `normalize_text` plus `in`; `plans/sources_adopt.py` `quote_check` was not executed. No R50-C1 or R50-C2 admission is claimed. Scratch `/fast/scratch/hyaku/kengaku-r50/R50FRScoutGitDocs` is removed before yield.

VERDICT: five manuals re-fetched HTTP 200 at v2.56.0 and match the landed capture sha256; keep ids S173–S177 (no new range); repair anchors S173 (`:24-28` and add `:116-120`), S174 (`:69-73`), S175 (drop `:285-292`, use `:374-378`), S177 (`:41-42`); `FETCH_HEAD` is git-fetch(1) only and the filename `commondir` is gitrepository-layout(5) only.
