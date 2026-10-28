# R50FRScribeGate — `## Gate` block draft for `corpus/lessons/round-50.md`

Seat: `R50FRScribeGate` (scribe, leaf — no subagent dispatch). Round 50, hyaku run 11, wave `w1`.
Item: draft the round-50 lesson Gate block — at least one ADMIT and one REJECT (with reason and flip condition),
access dates, ≤25-word located quotes, and the census command/output placeholders the L1 fills.

Axes served: **novelty (R50-C1)** — the five git-v2.56.0 rows are C1's sourced basis for the `n17`/`n18`/`n20`/`n21`/`n22`
honest classes; **calibration (R50-C2)** — every Gate quote is a pointer that must resolve to a located span, and the
census placeholders plus the machine-checked flip obligation are the audit surface. This seat claims no axis movement
and no R50-C1/R50-C2 admission.

    REV kengaku-shokunin tip=d6f2fce9889f429162c12f851bae41891bedf5cd   (branch=master, read-only)
    REV freeze        =3b02d573d58cc6d2e0d27ef92ac0815354912252   ancestor-of-tip=yes
    REV base          =71f5f5f77591d8c3d19297ee9785436da45209e4   (claims file; used only for the before-census)

Scratch: `/fast/scratch/hyaku/kengaku-r50/R50FRScribeGate` (TMPDIR exported there), removed before yield; every receipt
this report cites is pasted below, so no citable evidence lives in scratch. No tool installed, no pacman transaction, no
lane write, commit, push, stash or checkout; no production file touched.

## 1. Precondition run before any measurement

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && git rev-parse HEAD && git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD && echo ANCESTOR_OK && git log --oneline -3
d6f2fce9889f429162c12f851bae41891bedf5cd
ANCESTOR_OK
d6f2fce round-50: mutant battery frozen at the 15 witnessed rows; seven unwitnessed rows dropped and listed
6db0279 round-50: S3 fence repair (five documented git shapes resolved by containment), sealed50 hostile set, re-derived mutant battery, Q41 lesson
c3372a9 round-50: C1 counter open-window repair (module attribution keyed by path, not basename); predicate unchanged
```

## 2. Measurements

### 2.1 Capture integrity — draft sha256 column vs the registry rows

```
$ cd corpus/evidence/round50 && sha256sum *.adoc
fd225a09cb7bdb687cff4ba161cb1f337f2523eac5f83db5dbbbb1ef216fa41e  git-fetch.adoc
123096436d7d47b718483fdfbc1660446474a77b2a5b33212f5360af89ca2f95  git-init.adoc
3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631  git-replace.adoc
ee8a368564ace74a07e4a034e080b26fb1c3b35d17ef1fe41dcbfcc5595fe8dc  git-worktree.adoc
39ce8d137a30e1fd80eeae146b1c424e56f688f4ddd001259eb98543d3209439  gitrepository-layout.adoc
```

Each digest equals the `sha256` recorded in its `corpus/SOURCES.md` row (S173–S177: exact match on all five).

### 2.2 Quote presence and word counts

Scratch verifier: whitespace-normalize each quoted string, search it inside the **cited** line span of the capture, and
compare the parenthesized count.

```
S173 cite=80-83 words=19 declared=19 present=True
S174 cite=69-73 words=24 declared=24 present=True
S175 cite=396-400 words=24 declared=24 present=True
S176 cite=20-20 words=7 declared=7 present=True
S176 cite=22-23 words=15 declared=15 present=True
S177 cite=41-42 words=19 declared=19 present=True
S175~layout cite=286-287 words=16 declared=16 present=True
ALL_OK True
```

Every quote is ≤25 whitespace tokens (the cap `plans/sources_adopt.py` gates at), present in its cited span, and its
declared count is correct.

### 2.3 Census before → after

The census needs a fleet root carrying `shokunin.conf`; a bare clone root is refused — verbatim first attempt:

```
$ scripts/sources-census.sh validate --root <scratch>/fleetroot kengaku
ERROR: config not found: <scratch>/fleetroot/shokunin.conf
ERROR: unknown lane (not a dir, not in conf or root): kengaku
exit=2
```

With the fleet's own `shokunin.conf` copied into the scratch root and a `git clone --shared` at `71f5f5f` inside it:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <scratch>/fleetroot kengaku
kengaku	ok	<scratch>/fleetroot/kengaku-shokunin/corpus/SOURCES.md
exit=0   (16 lines)
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
exit=0   (16 lines)
$ diff census-before.txt census-after.txt
16c16
< kengaku	ok	<scratch>/fleetroot/kengaku-shokunin/corpus/SOURCES.md
---
> kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
```

Both runs emit the same 13 `W04` duplicate-URL warnings and `kengaku ok`; only the `ok`-line path differs. Registry
counts (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` on `git show 71f5f5f:corpus/SOURCES.md` and on the tip
file; same pattern for tiers and status): rows **165 → 170**; tier `A=141 B=22 C=2` → `A=146 B=22 C=2`; status
`mined=149` → `154`, `queued=8`, `rejected=8`. `git diff --numstat 71f5f5f 822f3b7 -- corpus/SOURCES.md` → `5	0`:
five added rows, **no existing row edited**.

### 2.4 The rejected candidate, re-measured (access date 2026-10-28)

```
$ for u in https://www.tbench.ai/ https://hub.harborframework.com/terminal-bench/4 https://www.tbench.ai/leaderboard; do curl -sS -o /dev/null -m 20 -w 'HTTP %{http_code} bytes=%{size_download}\n' "$u"; done; date -u +%FT%TZ
https://www.tbench.ai/ -> HTTP 200 bytes=145344
https://hub.harborframework.com/terminal-bench/4 -> HTTP 404 bytes=26304
https://www.tbench.ai/leaderboard -> HTTP 308 bytes=15
2026-10-28T17:41:28Z
$ curl -sSL -m 25 -o lb.html -w 'leaderboard final HTTP %{http_code} bytes=%{size_download} url=%{url_effective}\n' https://www.tbench.ai/leaderboard
leaderboard final HTTP 200 bytes=145344 url=https://www.tbench.ai/
$ grep -ciE 'test_outputs|task.yaml|sha256|digest' lb.html
0        # exit 1 — no pinned per-task spec or digest in the inspected bytes
```

Reason: the pinned hub path is gone (HTTP 404) and the leaderboard 308-redirects to a marketing root carrying no task
spec and no digest — mutable and unpinned, so it cannot back a row or a claim. Flip condition: a stable versioned
per-task endpoint (an immutable revision URL serving the task spec with a published digest) renders those bytes.

### 2.5 The flip obligation is machine-checked, not asserted

`plans/gate_flip_check.py` run read-only against three lesson copies; the lesson-repo root was a scratch dir holding a
copy of `corpus/knowledge/fixture-honest-geometry.md`, so the citation leg is live. Verbatim stdout:

Committed block (`corpus/lessons/round-50.md` as landed), **exit 0**:

```
FLIP-DETAIL lesson=<scratch>/gate/round-50-committed.md lesson_round=50 refused_rows=1 malformed_resolutions=0
FLIPS total=0 unresolved=0
FLIP-CITE entries=- missing=SOURCES.md not_fired=0 red=0
```

Draft block with the `Flip check (round 50)` line, **exit 0**:

```
FLIP line=32 flip_line=32 item=tbench.ai shapes=flip: resolution=line:36:not fired:round=50
FLIP-CITE line=36 item=tbench.ai state=not fired files=tbench.ai verdict=clear
FLIP-DETAIL lesson=<scratch>/gate/round-50-draft.md lesson_round=50 refused_rows=2 malformed_resolutions=0
FLIPS total=1 unresolved=0
FLIP-CITE entries=fixture-honest-geometry.md missing=SOURCES.md not_fired=1 red=0
```

Same draft with that one line deleted, **exit 1**:

```
FLIP line=32 flip_line=32 item=tbench.ai shapes=flip: resolution=unresolved:no-line
FLIP-DETAIL lesson=<scratch>/gate/round-50-noline.md lesson_round=50 refused_rows=2 malformed_resolutions=0
FLIPS total=1 unresolved=1
FLIP-CITE entries=fixture-honest-geometry.md missing=SOURCES.md not_fired=0 red=0
```

`refused_rows=2` is the reject row plus the census status line (`… rejected=…`), which the checker counts as a refusal
word but attaches no flip shape to — diagnostic only, no obligation, no red.

## 3. The block to land (verbatim)

3966 bytes, 27 lines, sha256 `129cdf0bd60ae7fe7df5e4c146a0b65b0b5b4f9d779083e94ce9db0e8078cae3`, computed over the
bytes printed between the fences (trailing newline included).

````markdown
## Gate

Candidates opened this round are `corpus/SOURCES.md` S173–S177, each accessed 2026-10-28 and fetched from
`https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/<doc>.adoc` at tag `v2.56.0`; the captures are
committed at `corpus/evidence/round50/<doc>.adoc`, and their sha256 equal the digests recorded in the rows. The
admitted rows are carried by the entry `corpus/knowledge/fixture-honest-geometry.md`. Quotes are ≤25 words (count in
parentheses) and located by line in the capture.

| candidate | decision | source (capture sha256) | accessed | located quote (≤25 words) |
|---|---|---|---|---|
| S173 | **ADMIT** — documents `objects/info/alternates` as a git write: the `n22` class, and why a shape keyed on an empty `objects/info` over-excludes it | gitrepository-layout `39ce8d13…` | 2026-10-28 | `:80-83` “This file records paths to alternate object stores that this object store borrows objects from, one pathname per line.” (19) |
| S174 | **ADMIT** — documents `--separate-git-dir` writing a `.git` text file inside the work tree: the `n21` class | git-init `12309643…` | 2026-10-28 | `:69-73` “create a text file there containing the path to the actual repository. This file acts as a filesystem-agnostic Git symbolic link to the repository.” (24) |
| S175 | **ADMIT** — documents both directions of the `n20` pointer pair: the `.git` gitfile names `worktrees/<id>`, the `gitdir` file names the work tree back. The `gitdir` file's own content is the layout capture at `gitrepository-layout.adoc:286-287`: “A text file containing the absolute path back to the .git file that points to here.” (16) | git-worktree `ee8a3685…` | 2026-10-28 | `:396-400` “For example, if a linked worktree is moved to `/newpath/test-next` and its `.git` file points to `/path/main/.git/worktrees/test-next`, then update `/path/main/.git/worktrees/test-next/gitdir` to reference `/newpath/test-next` instead.” (24) |
| S176 | **ADMIT** — documents `refs/replace` as a ref whose name is an object id: the `n17` class, which a check keyed on `refs/heads` and `refs/tags` misses | git-replace `3f61be3f…` | 2026-10-28 | `:20` “Adds a 'replace' reference in `refs/replace/` namespace.” (7) and `:22-23` “The name of the 'replace' reference is the SHA-1 of the object that is replaced.” (15) |
| S177 | **ADMIT** — documents the fetch write a plain-init allowlist misses: the `n18` class | git-fetch `fd225a09…` | 2026-10-28 | `:41-42` “The names of refs that are fetched, together with the object names they point at, are written to `.git/FETCH_HEAD`.” (19) |
| `tbench.ai` task hub / live leaderboard (carried lead) | **REJECT** — mutable and unpinned: re-measured 2026-10-28, the pinned hub path `hub.harborframework.com/terminal-bench/4` answers HTTP 404 (26304 bytes) and `www.tbench.ai/leaderboard` 308-redirects to the marketing root (HTTP 200, 145344 bytes) with no task spec or digest token in the inspected bytes, so no quotable per-task spec exists. Flip: a stable versioned per-task endpoint — an immutable revision URL serving the task spec together with a published digest — renders those bytes | carried lead, no capture | 2026-10-28 | none — no pinned per-task spec byte rendered |

Rows touched old→new: none (5 additions, 0 deletions in `corpus/SOURCES.md` at `822f3b7`).

Flip check (round 50): tbench.ai — not fired — pinned hub path still HTTP 404 on 2026-10-28; leaderboard redirects to a marketing page with no spec or digest.

Census (the L1 fills both outputs at landing):
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`

- before (round start, `71f5f5f`): `<CENSUS-BEFORE: paste stdout and exit code>`
- after (landing tip): `<CENSUS-AFTER: paste stdout and exit code>`
- registry: rows `<N-before>` -> `<N-after>`; tier `A=<…> B=<…> C=<…>`; status counts `mined=<…> queued=<…> rejected=<…>`
````

## 4. Findings on the committed block (`corpus/lessons/round-50.md:17-34`)

| # | pointer | finding | fix in the draft |
|---|---|---|---|
| F1 | `:27` | S175 attributes the sentence “A text file containing the absolute path back to the .git file that points to here.” to `git-worktree` `:285-292`; in the capture that range is the `--reason`/`lock` text. The sentence is at `corpus/evidence/round50/gitrepository-layout.adoc:286-287` (16 words, verified present). | S175 cites `git-worktree` `:396-400`; the `gitdir`-file content is cited as `gitrepository-layout.adoc:286-287`. |
| F2 | `:26` | S174 cites `:69-72`, but the quoted sentence ends at `git-init.adoc:73` (“repository.”). | cite `:69-73`; quote present, 24 words. |
| F3 | `:29` | S177 cites `:42-43`; the quote begins at `git-fetch.adoc:41` and ends at `:42`. | cite `:41-42`; 19 words. |
| F4 | `:28` | S176 cites `:20-24`; the two quoted fragments sit at `:20` and `:22-23` (`:24` is “replacement object.”). | cite `:20` and `:22-23` (7 + 15 words). |
| F5 | `:30` | **Structural, the one that matters:** the reject sits in a four-column table whose second cell is the *source*. `plans/gate_flip_check.py:24-26` reads the verdict from the second cell, so the round's only refusal is invisible: the committed lesson prints `FLIPS total=0 unresolved=0` and the single `refused_rows` is the census sentence's `rejected=8`. | candidate \| decision \| source \| accessed \| quote — the r48 layout (`corpus/lessons/round-48.md:7-11`), so the reject is a refusal row. |
| F6 | `:30` | The reject row carries no flip condition, and the lesson has no `Flip check (round 50):` line; with F5 fixed it would be an unresolved obligation (exit 1, measured). | the row carries `Flip: …`, and a `Flip check (round 50): tbench.ai — not fired — …` line resolves it (exit 0, measured). |
| F7 | `:32` | The census is prose (“`scripts/sources-census.sh validate …` exit 0 before and after”): no command line, no stdout, no placeholder. | the command plus `<CENSUS-BEFORE>` / `<CENSUS-AFTER>` / registry-count placeholders the L1 fills at landing. |
| F8 | `:25-30` | Quotes carry no word counts, while r48/r49 Gate rows do (`round-48.md:11` “(8 words)”). | counts in parentheses, each verified by 2.2. |

Verified, not a defect: the committed `:32` registry figures (`165 → 170`, `A=146/B=22/C=2`,
`mined=154/queued=8/rejected=8`) match this seat's measurement at `d6f2fce`.

## 5. Limits

- `gate_flip_check.py` ran on scratch copies of the lesson; `entries=fixture-honest-geometry.md` is a copy of the real
  entry, and `missing=SOURCES.md` is baseline — the committed lesson prints the same, because `corpus/SOURCES.md` does
  not resolve under `corpus/knowledge/`.
- The reject measurement is a live HTTP fetch from this host at `2026-10-28T17:41:28Z`; statuses and sizes can change,
  and by design no capture is committed for a rejected source.
- The before-census is this seat's own run on a `git clone --shared` at `71f5f5f` inside a scratch fleet root with a copy
  of the fleet `shokunin.conf`. The L1's round-start census at the fleet root is the authoritative `before`; the values
  here are candidates, not the landing census.
- Word counts are whitespace-token counts, the same convention the 25-word cap uses.
- The C1 counter, the mutant leg, the sealed legs and the C2 audit were **not** run by this seat; no admission is claimed
  for either claim.
- The draft names no model, alias or route.

## 6. Out of scope / not done

- No edit to `corpus/lessons/round-50.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`, `LOG.md`,
  `SKILL.md`, `plans/*` or `corpus/*`; no registry row appended; no commit, push, stash or checkout; no sibling repo.
- The census outputs behind the placeholders are the L1's to paste; this seat supplies the measured candidates only.

## 7. Scratch

`/fast/scratch/hyaku/kengaku-r50/R50FRScribeGate` removed before yield (verified absent: `test -d …` → exit 1). All
evidence this report uses is quoted above.

## VERDICT

**Draft delivered, ready to land with F1–F8 applied.** Five ADMITs (S173–S177, quotes located and ≤25 words, captures
sha256-matched to the rows) and one REJECT (`tbench.ai` hub / leaderboard: pinned path HTTP 404, leaderboard 308 to a
marketing page with no spec or digest, re-measured 2026-10-28) with a stated flip condition; access dates per row; census
command and output placeholders present. The committed Gate block is defective in eight recorded ways (F1–F8; F8
cosmetic), F5 the serious one: its reject is invisible to `plans/gate_flip_check.py`. No axis movement and no
R50-C1/R50-C2 admission claimed by this seat.
