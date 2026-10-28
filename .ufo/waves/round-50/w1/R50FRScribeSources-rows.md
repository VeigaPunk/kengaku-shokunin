# R50FRScribeSources — SOURCES.md rows for round 50 (C1 sourced basis)

DRAFT for the L1 to apply. This seat edited no corpus file, ran no fence and claims no admission.

REV `d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78` (lane tip at measurement; registry 170 rows, last id S177).
Freeze `3b02d573d58cc6d2e0d27ef92ac0815354912252` is an ancestor of that tip (`git merge-base --is-ancestor` exit 0).

Inputs read in full: `.ufo/waves/round-50/w1/R50FRScoutGitDocs.md`, `.ufo/waves/round-50/w1/R50FRScoutAlternates.md`,
the five committed captures `corpus/evidence/round50/{gitrepository-layout,git-init,git-worktree,git-replace,git-fetch}.adoc`
(each sha256 re-computed here and equal to the digest its S173–S177 anchor cell records).

## What the two scouts bind

- **GitDocs**: five manuals re-fetched HTTP 200 at tag `v2.56.0`, digests equal the committed captures, access
  2026-10-28. Verdict: keep ids S173–S177, open no new id, and repair anchors — S173 widen `:26-28` to `:24-28`
  and add `:116-120`; S174 end at `:73`; S175 replace `:285-292` with DETAILS `:374-378`; S177 start at `:41`.
- **Alternates**: the layout page carries no `security` section and no such word; the borrowed-store note is the
  numbered item under `objects::`, `:44-50` ("not suitable to be published for use with dumb transports but
  otherwise is OK as long as `objects/info/alternates` points at the object stores it borrows from"); the relative
  base is `:85-86` ("relative to the object database, not to the repository"). `refs/replace/<obj-sha1>` names an
  object id in both pages; "not a path" is the lane's inference, not a quoted sentence.

## Measured defect in the landed rows (why the repair is the primary deliverable)

The lane's own adoption gate refuses all five landed rows, twice over, independently:

1. every quoted span sits in the `teaches` cell, so the gate's anchor column carries none — `no-quote`, exit 4;
2. after moving the spans into the anchor cell unchanged they are still `absent` from the captures — the landed
   spans are markup-stripped and space-joined, not byte substrings of the pin — exit 7.

```
$ python3 plans/sources_adopt.py --quote-file landed-rows.txt --artifact caps --url-map caps-map.json
QUOTE rows=5 spans=0 located=0 found=0 overlong=0 absent=0 malformed=5 cap=25 artifacts=git-fetch.adoc,git-init.adoc,git-replace.adoc,git-worktree.adoc,gitrepository-layout.adoc mismatch=0 unmapped=0 urlmap=caps-map.json entries=5
  REFUSED S173 no-quote
  REFUSED S174 no-quote
  REFUSED S175 no-quote
  REFUSED S176 no-quote
  REFUSED S177 no-quote
```

```
QUOTE rows=3 spans=4 located=0 found=0 overlong=0 absent=4 malformed=0 cap=25 artifacts=git-fetch.adoc,git-init.adoc,git-replace.adoc,git-worktree.adoc,gitrepository-layout.adoc mismatch=0 unmapped=0 urlmap=caps-map.json entries=5
  REFUSED S174 absent words=11 quote="a text file there containing the path to the actual repository"
  REFUSED S176 absent words=7 quote="Adds a 'replace' reference in refs/replace/ namespace"
  REFUSED S176 absent words=9 quote="is the SHA-1 of the object that is replaced"
  REFUSED S177 absent words=19 quote="The names of refs that are fetched, together with the object names they point at, are written to .git/FETCH_HEAD"
```

Consequence for calibration: `plans/sources_adopt.py --quote-file` cannot validate the round's own sourced basis,
and two anchor ranges do not hold the claim they are cited for. A registry row is a single line, so a quoted span
that wraps in the source cannot be carried verbatim: the repair uses one byte-exact span per source line, the way
S086/S092 already carry multiple spans.

## Option A — replacement rows for S173–S177 (recommended; no new id, no new census finding)

Apply in place: replace the five rows at `corpus/SOURCES.md:188-192` with these lines.

```
| S173 | Git repository layout (gitrepository-layout, git v2.56.0) — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc | docs | A | the on-disk shape git writes in a repository: the `.git` gitfile, `objects/info/alternates` and the base its entries resolve against, the `refs/replace/<obj-sha1>` directory entry, `shallow`, `commondir` and `worktrees` | tag v2.56.0, gitrepository-layout.adoc:24-28, :44-50, :80-89, :116-120, :261-273; sha256 39ce8d137a30e1fd80eeae146b1c424e56f688f4ddd001259eb98543d3209439; "This mechanism is called a 'gitfile' and is usually managed via the" and "will usually work if you have relative paths (relative" and "to the object database, not to the repository!) in your" and "records the SHA-1 of the object that replaces `<obj-sha1>`." | a `.git` FILE at the work-tree root is a documented gitfile holding a `gitdir: <path>` pointer, and alternates, shallow and commondir are documented git writes; an alternates entry is relative to the object database, not the repository root, and a borrowed store is documented as usable when the alternates file points at it, so refusing these by name over-refuses documented states | mined | 2026-10-28 | 180d | corpus/knowledge/fixture-honest-geometry.md |
| S174 | git-init `--separate-git-dir` (git v2.56.0) — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-init.adoc | docs | A | the documented creation of a store outside the work tree, named by a gitfile inside it | tag v2.56.0, git-init.adoc:69-73; sha256 123096436d7d47b718483fdfbc1660446474a77b2a5b33212f5360af89ca2f95; "`./.git/`, create a text file there containing the path to the actual" | `--separate-git-dir` writes a text file where `.git` would have been, holding the path of the actual repository and acting as a symbolic link, which is the honest class the base fence refused as a gitdir redirect | mined | 2026-10-28 | 180d | corpus/knowledge/fixture-honest-geometry.md |
| S175 | git-worktree (git v2.56.0) — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-worktree.adoc | docs | A | linked worktrees: the worktrees/<id>/gitdir back-pointer and the gitfile that names it | tag v2.56.0, git-worktree.adoc:365-378, :395-401, :408-410; sha256 ee8a368564ace74a07e4a034e080b26fb1c3b35d17ef1fe41dcbfcc5595fe8dc; "Within a linked worktree, `$GIT_DIR` is set to point to this private" and "(e.g. `/path/main/.git`). These settings are made in a `.git` file located at" and "If you manually move a linked worktree, you need to update the `gitdir` file" | inside a linked worktree `$GIT_DIR` is the private `worktrees/<id>` entry and `$GIT_COMMON_DIR` points back at the main store, with both recorded in a `.git` file at the worktree top and the entry`s `gitdir` file pointing back, so both pointers are ordinary git writes inside the fixture | mined | 2026-10-28 | 180d | corpus/knowledge/fixture-honest-geometry.md |
| S176 | git-replace (git v2.56.0) — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc | docs | A | the refs/replace namespace and what the name of a replace ref means | tag v2.56.0, git-replace.adoc:20, :22-24; sha256 3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631; "Adds a 'replace' reference in `refs/replace/` namespace." and "The name of the 'replace' reference is the SHA-1 of the object that is" | a replace ref is a ref in the `refs/replace/` namespace whose name is the SHA-1 of the replaced object, so a ref check keyed on refs/heads or refs/tags over-refuses it | mined | 2026-10-28 | 180d | corpus/knowledge/fixture-honest-geometry.md |
| S177 | git-fetch (git v2.56.0) — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-fetch.adoc | docs | A | what git writes to .git/FETCH_HEAD when a fetch completes | tag v2.56.0, git-fetch.adoc:41-42; sha256 fd225a09cb7bdb687cff4ba161cb1f337f2523eac5f83db5dbbbb1ef216fa41e; "The names of refs that are fetched, together with the object names" and "they point at, are written to `.git/FETCH_HEAD`.  This information" | a completed fetch writes the fetched ref names and their object names into `.git/FETCH_HEAD`, an ordinary git write that a plain-init allowlist misses | mined | 2026-10-28 | 180d | corpus/knowledge/fixture-honest-geometry.md |
```

Census on a copy of the tip registry with only these five rows replaced (170 rows):

```
file	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
file	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
file	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
file	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
file	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
file	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
file	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
file	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
file	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
file	ok	/fast/scratch/hyaku/kengaku-r50/R50FRScribeSources/lane/corpus/SOURCES-tv3inplace.md
```

## Option B — append-only superseding rows S178–S182 (if a landed row may not be rewritten)

Same content and same quoting, expressed as the corpus's existing supersession form. Five new rows, five new
pre-existing-class `W04` duplicate-URL warnings, no error. Append inside the `## Registry` table, after S177 —
appending at end of file is refused as `E12 row outside Registry section` (boundary probed here).

```
| S178 | Git repository layout (gitrepository-layout, git v2.56.0) — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc | docs | A | supersedes S173 — anchor and quote correction: the gitfile token, the alternates resolution base and the `refs/replace/<obj-sha1>` entry are cited at the lines that hold them, and the quotes are byte-exact spans of the v2.56.0 pin | tag v2.56.0, gitrepository-layout.adoc:24-28, :44-50, :80-89, :116-120, :261-273; sha256 39ce8d137a30e1fd80eeae146b1c424e56f688f4ddd001259eb98543d3209439; "This mechanism is called a 'gitfile' and is usually managed via the" and "will usually work if you have relative paths (relative" and "to the object database, not to the repository!) in your" and "records the SHA-1 of the object that replaces `<obj-sha1>`." | a `.git` FILE at the work-tree root is a documented gitfile holding a `gitdir: <path>` pointer, and alternates, shallow and commondir are documented git writes; an alternates entry is relative to the object database, not the repository root, and a borrowed store is documented as usable when the alternates file points at it, so refusing these by name over-refuses documented states | mined | 2026-10-28 | 180d | corpus/knowledge/fixture-honest-geometry.md |
| S179 | git-init `--separate-git-dir` (git v2.56.0) — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-init.adoc | docs | A | supersedes S174 — anchor and quote correction: the `--separate-git-dir` paragraph ends at git-init.adoc:73 | tag v2.56.0, git-init.adoc:69-73; sha256 123096436d7d47b718483fdfbc1660446474a77b2a5b33212f5360af89ca2f95; "`./.git/`, create a text file there containing the path to the actual" | `--separate-git-dir` writes a text file where `.git` would have been, holding the path of the actual repository and acting as a symbolic link, which is the honest class the base fence refused as a gitdir redirect | mined | 2026-10-28 | 180d | corpus/knowledge/fixture-honest-geometry.md |
| S180 | git-worktree (git v2.56.0) — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-worktree.adoc | docs | A | supersedes S175 — anchor correction: the gitfile and $GIT_COMMON_DIR pair is git-worktree.adoc DETAILS:374-378, not :285-292 | tag v2.56.0, git-worktree.adoc:365-378, :395-401, :408-410; sha256 ee8a368564ace74a07e4a034e080b26fb1c3b35d17ef1fe41dcbfcc5595fe8dc; "Within a linked worktree, `$GIT_DIR` is set to point to this private" and "(e.g. `/path/main/.git`). These settings are made in a `.git` file located at" and "If you manually move a linked worktree, you need to update the `gitdir` file" | inside a linked worktree `$GIT_DIR` is the private `worktrees/<id>` entry and `$GIT_COMMON_DIR` points back at the main store, with both recorded in a `.git` file at the worktree top and the entry`s `gitdir` file pointing back, so both pointers are ordinary git writes inside the fixture | mined | 2026-10-28 | 180d | corpus/knowledge/fixture-honest-geometry.md |
| S181 | git-replace (git v2.56.0) — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc | docs | A | supersedes S176 — anchor and quote correction: the replace name rule is git-replace.adoc:20 and :22-24 | tag v2.56.0, git-replace.adoc:20, :22-24; sha256 3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631; "Adds a 'replace' reference in `refs/replace/` namespace." and "The name of the 'replace' reference is the SHA-1 of the object that is" | a replace ref is a ref in the `refs/replace/` namespace whose name is the SHA-1 of the replaced object, so a ref check keyed on refs/heads or refs/tags over-refuses it | mined | 2026-10-28 | 180d | corpus/knowledge/fixture-honest-geometry.md |
| S182 | git-fetch (git v2.56.0) — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-fetch.adoc | docs | A | supersedes S177 — anchor and quote correction: the FETCH_HEAD sentence starts at git-fetch.adoc:41 | tag v2.56.0, git-fetch.adoc:41-42; sha256 fd225a09cb7bdb687cff4ba161cb1f337f2523eac5f83db5dbbbb1ef216fa41e; "The names of refs that are fetched, together with the object names" and "they point at, are written to `.git/FETCH_HEAD`.  This information" | a completed fetch writes the fetched ref names and their object names into `.git/FETCH_HEAD`, an ordinary git write that a plain-init allowlist misses | mined | 2026-10-28 | 180d | corpus/knowledge/fixture-honest-geometry.md |
```

Census on a copy of the tip registry with S178–S182 appended after S177 (175 rows):

```
file	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
file	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
file	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
file	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
file	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
file	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
file	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
file	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
file	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
file	W04	S178 duplicate url raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc across scopes
file	W04	S179 duplicate url raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-init.adoc across scopes
file	W04	S180 duplicate url raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-worktree.adoc across scopes
file	W04	S181 duplicate url raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc across scopes
file	W04	S182 duplicate url raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-fetch.adoc across scopes
file	ok	/fast/scratch/hyaku/kengaku-r50/R50FRScribeSources/lane/corpus/SOURCES-tv4sup.md
```

## Option C — one optional new source, `git-clone(1)`, NOT recommended for this round

Neither scout opened `git-clone.adoc`, and the frozen claims' sourced basis does not name it; the borrowed-store
mechanism it documents is already carried by S173 `:44-50` and `:80-89`. A row here would be a scribe-opened
source (this seat fetched it: HTTP 200, 439 lines, 2026-10-28, sha256
`3116cc9ee8d1c7bbd12649e7203e813d2e4335b9bc9dd76d20ec87ce5f430123`), and it would also need a line in
`corpus/knowledge/fixture-honest-geometry.md` to keep `used-by` honest. Included only so the L1 can adopt it
without re-deriving, with the exact digests, spans and gate output:

```
| S178 | git-clone `--shared`/`--reference`/`--dissociate` (git v2.56.0) — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-clone.adoc | docs | A | the borrowing dependency a local clone creates in `.git/objects/info/alternates`, its corruption warning, and `--dissociate` as the documented way to break the borrow | tag v2.56.0, git-clone.adoc:87-95, :107-131; sha256 3116cc9ee8d1c7bbd12649e7203e813d2e4335b9bc9dd76d20ec87ce5f430123; "NOTE: this is a possibly dangerous operation; do *not* use" and "by the cloned repository, then the cloned repository will become corrupt." | a local clone that borrows objects writes an ordinary `.git/objects/info/alternates` pointer, and git documents that the borrowed objects can be removed under the borrower — so the honest classification is containment of the borrowed store, not refusal of the pointer by name | mined | 2026-10-28 | 180d | corpus/knowledge/fixture-honest-geometry.md |
```

If Option B is used instead, the same row takes the next free id S183:

```
| S183 | git-clone `--shared`/`--reference`/`--dissociate` (git v2.56.0) — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-clone.adoc | docs | A | the borrowing dependency a local clone creates in `.git/objects/info/alternates`, its corruption warning, and `--dissociate` as the documented way to break the borrow | tag v2.56.0, git-clone.adoc:87-95, :107-131; sha256 3116cc9ee8d1c7bbd12649e7203e813d2e4335b9bc9dd76d20ec87ce5f430123; "NOTE: this is a possibly dangerous operation; do *not* use" and "by the cloned repository, then the cloned repository will become corrupt." | a local clone that borrows objects writes an ordinary `.git/objects/info/alternates` pointer, and git documents that the borrowed objects can be removed under the borrower — so the honest classification is containment of the borrowed store, not refusal of the pointer by name | mined | 2026-10-28 | 180d | corpus/knowledge/fixture-honest-geometry.md |
```

Package gate for this single row: `registry=170 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`
(exit 0); the Option B package gate, five rows, is `staged=5` with the same zeros — both in `## Receipts`.
Its sha256 is only checkable if the capture is committed at `corpus/evidence/round50/git-clone.adoc`; a byte copy
is provided beside this file as `R50FRScribeSources-git-clone.adoc`.

## Receipts (verbatim)

Census, unmodified tip registry (170 rows) — the baseline every variant is compared against:

```
file	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
file	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
file	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
file	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
file	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
file	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
file	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
file	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
file	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
file	ok	/fast/scratch/hyaku/kengaku-r50/R50FRScribeSources/lane/corpus/SOURCES-testbase.md
```

Registry with the Option A rows **and** the `git-clone` row (171 rows), the maximum this seat's drafts reach:

```
file	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
file	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
file	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
file	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
file	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
file	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
file	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
file	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
file	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
file	ok	/fast/scratch/hyaku/kengaku-r50/R50FRScribeSources/lane/corpus/SOURCES-tv3inplace178.md
```

Adoption-gate quote check, Option A rows (5 rows, 12 spans):

```
QUOTE rows=5 spans=12 located=12 found=12 overlong=0 absent=0 malformed=0 cap=25 artifacts=git-fetch.adoc,git-init.adoc,git-replace.adoc,git-worktree.adoc,gitrepository-layout.adoc mismatch=0 unmapped=0 urlmap=caps-map.json entries=5
  ok S173 words=12 at gitrepository-layout.adoc quote="This mechanism is called a 'gitfile' and is usually managed via the" bound=gitrepository-layout.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc
  ok S173 words=9 at gitrepository-layout.adoc quote="will usually work if you have relative paths (relative" bound=gitrepository-layout.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc
  ok S173 words=10 at gitrepository-layout.adoc quote="to the object database, not to the repository!) in your" bound=gitrepository-layout.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc
  ok S173 words=9 at gitrepository-layout.adoc quote="records the SHA-1 of the object that replaces `<obj-sha1>`." bound=gitrepository-layout.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc
  ok S174 words=12 at git-init.adoc quote="`./.git/`, create a text file there containing the path to the actual" bound=git-init.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-init.adoc
  ok S175 words=12 at git-worktree.adoc quote="Within a linked worktree, `$GIT_DIR` is set to point to this private" bound=git-worktree.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-worktree.adoc
  ok S175 words=12 at git-worktree.adoc quote="(e.g. `/path/main/.git`). These settings are made in a `.git` file located at" bound=git-worktree.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-worktree.adoc
  ok S175 words=14 at git-worktree.adoc quote="If you manually move a linked worktree, you need to update the `gitdir` file" bound=git-worktree.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-worktree.adoc
  ok S176 words=7 at git-replace.adoc quote="Adds a 'replace' reference in `refs/replace/` namespace." bound=git-replace.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc
  ok S176 words=14 at git-replace.adoc quote="The name of the 'replace' reference is the SHA-1 of the object that is" bound=git-replace.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc
  ok S177 words=12 at git-fetch.adoc quote="The names of refs that are fetched, together with the object names" bound=git-fetch.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-fetch.adoc
  ok S177 words=9 at git-fetch.adoc quote="they point at, are written to `.git/FETCH_HEAD`.  This information" bound=git-fetch.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-fetch.adoc
```

Adoption-gate quote check, Option B rows (5 rows, 12 spans):

```
QUOTE rows=5 spans=12 located=12 found=12 overlong=0 absent=0 malformed=0 cap=25 artifacts=git-fetch.adoc,git-init.adoc,git-replace.adoc,git-worktree.adoc,gitrepository-layout.adoc mismatch=0 unmapped=0 urlmap=caps-map.json entries=5
  ok S178 words=12 at gitrepository-layout.adoc quote="This mechanism is called a 'gitfile' and is usually managed via the" bound=gitrepository-layout.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc
  ok S178 words=9 at gitrepository-layout.adoc quote="will usually work if you have relative paths (relative" bound=gitrepository-layout.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc
  ok S178 words=10 at gitrepository-layout.adoc quote="to the object database, not to the repository!) in your" bound=gitrepository-layout.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc
  ok S178 words=9 at gitrepository-layout.adoc quote="records the SHA-1 of the object that replaces `<obj-sha1>`." bound=gitrepository-layout.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc
  ok S179 words=12 at git-init.adoc quote="`./.git/`, create a text file there containing the path to the actual" bound=git-init.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-init.adoc
  ok S180 words=12 at git-worktree.adoc quote="Within a linked worktree, `$GIT_DIR` is set to point to this private" bound=git-worktree.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-worktree.adoc
  ok S180 words=12 at git-worktree.adoc quote="(e.g. `/path/main/.git`). These settings are made in a `.git` file located at" bound=git-worktree.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-worktree.adoc
  ok S180 words=14 at git-worktree.adoc quote="If you manually move a linked worktree, you need to update the `gitdir` file" bound=git-worktree.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-worktree.adoc
  ok S181 words=7 at git-replace.adoc quote="Adds a 'replace' reference in `refs/replace/` namespace." bound=git-replace.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc
  ok S181 words=14 at git-replace.adoc quote="The name of the 'replace' reference is the SHA-1 of the object that is" bound=git-replace.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc
  ok S182 words=12 at git-fetch.adoc quote="The names of refs that are fetched, together with the object names" bound=git-fetch.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-fetch.adoc
  ok S182 words=9 at git-fetch.adoc quote="they point at, are written to `.git/FETCH_HEAD`.  This information" bound=git-fetch.adoc->https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-fetch.adoc
```

Adoption-gate package checks:

```
registry=170 staged=5 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote /fast/scratch/hyaku/kengaku-r50/R50FRScribeSources/append-supersede.md rows=5
registry=170 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote /fast/scratch/hyaku/kengaku-r50/R50FRScribeSources/append-block.md rows=1
```

Non-vacuity probe of the row shape: a copy of S178 with one cell removed is refused
`E01 S178 fields=10`, exit 1.

## Limits

- I did not run the fence, the counter or any C1/C2 predicate; nothing here is evidence for either claim.
- The five captures are the committed ones; every digest above was recomputed from those bytes, not re-fetched.
- Byte-exactness is asserted for the 12 spans the gate reports `located`; it is a substring test of the pin, not
  an independent reading of the rendered manual.
- The pre-existing 15 `W04` warnings are unchanged by Option A and are not this seat's to clear.
- `git-clone.adoc` is fetched by this seat only; its HTTP status and digest are this seat's measurement.
