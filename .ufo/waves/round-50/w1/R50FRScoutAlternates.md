# R50FRScoutAlternates

Seat: R50FRScoutAlternates (scout). Axes: source fidelity (primary git text, URL, status, date, digest); classification match against the frozen claims; revision pin. Read-only. No R50-C1 or R50-C2 admission.

REV: shared clone `/fast/scratch/hyaku/kengaku-r50/R50FRScoutAlternates/lane` at `c3372a9b24d3a200946a6b37dc0a31ed5c982cc1` (`git rev-parse --show-toplevel` equals that clone). Freeze `3b02d573d58cc6d2e0d27ef92ac0815354912252` is an ancestor of that clone (`merge-base --is-ancestor` exit 0) and of the live tip observed after the clone, `d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78` (2026-10-28 14:39:56 -0300, `round-50: scored C1 receipt…`). It is not an ancestor of the pre-freeze base tip `71f5f5f77591d8c3d19297ee9785436da45209e4`; that base is an ancestor of the freeze (exit 0). `plans/round-50-claims.md`, `n22_alternates_in_d.py`, `n17_replace_ref.py`, `corpus/knowledge/fixture-honest-geometry.md`, and `corpus/SOURCES.md` have an empty diff from the measured clone to `d45c5bb2`. Host `git --version`: `git version 2.56.0`.

## Alternates — relative entries

URL: https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitrepository-layout.adoc
Status: HTTP 200. Fetch date: Wed, 28 Oct 2026 17:39:19 GMT (HEAD) and the body fetch in the same minute. `Last-Modified` absent on raw.githubusercontent.com.
Rendered mirror: https://git-scm.com/docs/gitrepository-layout and https://git-scm.com/docs/gitrepository-layout/2.56.0 — HTTP 200, `Last-Modified: Mon, 26 Oct 2026 14:52:03 GMT` and `14:52:05 GMT` respectively (curl, 2026-10-28). Python urllib without a User-Agent got 403 on git-scm.com; curl did not.
Digest: sha256 `39ce8d137a30e1fd80eeae146b1c424e56f688f4ddd001259eb98543d3209439` (11890 bytes). Same digest as lane `corpus/SOURCES.md` row S173.
Tag: annotated `v2.56.0` object `2478544319491bbd2a42cc57a83e3d2f4730a280`, tagger Junio C Hamano, `2026-09-28T04:20:13Z`, message `Git 2.56`.
Local second copy: `man gitrepository-layout` from git 2.56.0 (`/usr/share/man/man5/gitrepository-layout.5.gz`) has the same sentences.

Quote, `objects/info/alternates`, lines 80–89:

```
objects/info/alternates::
	This file records paths to alternate object stores that
	this object store borrows objects from, one pathname per
	line. Note that not only native Git tools use it locally,
	but the HTTP fetcher also tries to use it remotely; this
	will usually work if you have relative paths (relative
	to the object database, not to the repository!) in your
	alternates file, but it will not work if you use absolute
	paths unless the absolute path in filesystem and web URL
	is the same. See also `objects/info/http-alternates`.
```

The file does not contain the word "security". The borrowed-store note is the numbered item under `objects::`, lines 44–50:

```
. You could be using the `objects/info/alternates` or
`$GIT_ALTERNATE_OBJECT_DIRECTORIES` mechanisms to 'borrow'
objects from other object stores.  A repository with this kind
of incomplete object store is not suitable to be published for
use with dumb transports but otherwise is OK as long as
`objects/info/alternates` points at the object stores it
borrows from.
```

## refs/replace — object id, not a store path

Same layout file, lines 116–120:

```
refs/replace/`<obj-sha1>`::
	records the SHA-1 of the object that replaces `<obj-sha1>`.
	This is similar to info/grafts and is internally used and
	maintained by linkgit:git-replace[1]. Such refs can be exchanged
	between repositories while grafts are not.
```

URL: https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc
Status: HTTP 200. Fetch date: Wed, 28 Oct 2026 17:39:19 GMT. Digest sha256 `3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631` (5398 bytes). Same digest as S176. Mirror https://git-scm.com/docs/git-replace HTTP 200, `Last-Modified: Mon, 26 Oct 2026 14:52:02 GMT`. Local `man git-replace` (git 2.56.0) matches.

Quote, lines 20–24 (S176's cited range):

```
Adds a 'replace' reference in `refs/replace/` namespace.

The name of the 'replace' reference is the SHA-1 of the object that is
replaced. The content of the 'replace' reference is the SHA-1 of the
replacement object.
```

Git documents that the ref name is an object SHA-1 and the ref content is an object SHA-1. It does not use the words "not a path". The path `refs/replace/<obj-sha1>` is a ref path whose final component is defined as that object id.

## Classification match

Frozen claims (`plans/round-50-claims.md`): the base fence refuses `n22-alternates-in-d` (`objects/info/alternates` naming a store inside `d`) and `n17-replace-ref` (`refs/replace`). Sourced basis names `gitrepository-layout(5)` `objects/info/alternates` and `refs/replace`. Knowledge row (`corpus/knowledge/fixture-honest-geometry.md`): n22 "records object stores the repository borrows from, one pathname per line" (S173); n17 "a ref whose name is the SHA of the replaced object" (S176). Module `plans/honest50/modules/novel50/n22_alternates_in_d.py` writes `../../../main/.git/objects` and says that path is relative to `lane/.git/objects`. Module `n17_replace_ref.py` says the filename "is a 40-hex object name, not a path escape".

Match:

- Relative base: docs say relative alternates are relative to the object database, not the repository. The n22 comment and the `../../../main/.git/objects` entry (from `lane/.git/objects` up to the fixture, then into `main/.git/objects`) follow that rule. Match.
- Borrowed store: docs call this borrowing, and say the incomplete store is OK when `objects/info/alternates` points at the stores it borrows from. Classifying an in-`d` pointer as an honest git state matches that sentence. The same sentence limits publication: the store is not suitable for dumb transports. The claims do not say n22 is a complete or publishable repository; honest means a documented store shape inside `d`. Match, with that limit.
- Containment is not a doc guarantee. A relative entry may leave the repository (`../` is still "relative to the object database"). The claims' honest class is this in-`d` instance, not every relative alternates line. Out-of-`d` alternates stay a refusal in the claims. The docs support the mechanism; they do not say "inside `d`".
- `refs/replace/<object>`: S176, the knowledge row, and `git-replace(1)` agree that the name is the SHA-1 of the replaced object. The layout page agrees the component is `<obj-sha1>` and that the file records the replacement object's SHA-1. The phrase "not a path" is the lane's inference in `n17_replace_ref.py`. It is the right inference (the name is an object id, not a path to another store) and it is not a verbatim documentation sentence.

## Limits

- Checked git v2.56.0 only (the version the claims and the host both name). No other tag.
- Did not re-run the fence or rebuild n22/n17. This seat did not measure whether git's resolver accepts the n22 line; the module text asserts `fsck`/`cat-file`, and that assertion was not re-executed here.
- The layout manual never labels the borrow paragraph as a security note. There is no separate "security" section for alternates in these two pages.

VERDICT: classification matches the v2.56.0 documentation. Relative alternates are pathnames relative to the object database; a borrowed store is a documented, incomplete store that is OK when the alternates file points at that store, and is not suitable for dumb-transport publication. `refs/replace/<object>` names an object SHA-1 (ref name = replaced object, content = replacement object). "Not a path" is a correct inference, not a quoted sentence.
