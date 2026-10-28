# R50FRScribeSources — SOURCES.md rows for round 50 (C1 sourced basis)

Seat: scribe, serving R50-C1+R50-C2. Read-only against the lane; no corpus file, plan, SCORECARD, LOG or state
file was edited, and no fence, counter or predicate was run. No admission of either claim is made.

**Axes named.** A1 located-quote byte-exactness (≤25 words, byte substring of the v2.56.0 pin, spans carried where
the lane's gate reads them); A2 census validity (zero `E` codes, no new warning class); A3 id/collision safety
(next free id, no history gaps); A4 anchor-to-claim match (the cited line range holds the cited bytes);
A5 provenance (revision, digest, status, access date, and who opened the source).

## REV

`REV d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78` — lane tip at measurement (`clone --shared` in scratch; registry
170 rows, last id S177). Freeze `3b02d573d58cc6d2e0d27ef92ac0815354912252` is an ancestor of that tip
(`git merge-base --is-ancestor … HEAD` → exit 0). The lane moved `d6f2fce → c3372a9 → 822f3b7 → d45c5bb` while
this seat ran; `corpus/SOURCES.md` has an empty diff from `d6f2fce` to `d45c5bb`, so the registry state measured
is stable across those tips.

## Deliverable

`.ufo/waves/round-50/w1/R50FRScribeSources-rows.md` — the rows, in the contract-v1 11-column shape, verbatim and
gated. Three options, one recommended:

- **Option A (recommended)** replacement rows for S173–S177: anchors repaired per both scout reports, quotes moved
  into the anchor cell as byte-exact single-line spans.
- **Option B** the same content as append-only superseding rows S178–S182, if a landed row may not be rewritten.
- **Option C** one optional `git-clone(1)` row (id S178, or S183 under Option B), **not recommended** this round —
  neither scout opened that page and the frozen claims do not name it.

`.ufo/waves/round-50/w1/R50FRScribeSources-git-clone.adoc` — byte copy of the `git-clone.adoc` capture so the
sha256 in Option C is checkable if the L1 commits it at `corpus/evidence/round50/git-clone.adoc`.

## Commands run (all from the scratch clone of the lane at the tip)

```
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"   # HEAD d45c5bb2…
git -C "$S/lane" merge-base --is-ancestor 3b02d573… HEAD                     # exit 0
sha256sum corpus/evidence/round50/*.adoc                                     # five digests re-computed
curl -sS -o git-clone.adoc -w '%{http_code}' https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-clone.adoc
python3 plans/sources_adopt.py --quote-file <rows> --artifact <caps dir> --url-map <map.json>
python3 plans/sources_adopt.py --registry corpus/SOURCES.md --package <rows> --admit-ids <ids> \
        --scope-to-admit --entries corpus/knowledge/fixture-honest-geometry.md \
        --access-date 2026-10-28 --recheck 180d --out <path>
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <registry copy inside the clone>
```

Capture digests re-computed here equal the digests in the landed anchor cells (S173 `39ce8d13…d3209439`,
S174 `12309643…89ca2f95`, S175 `ee8a3685…595fe8dc`, S176 `3f61be3f…74640631`, S177 `fd225a09…216fa41e`).
The one new fetch, `git-clone.adoc`, returned **HTTP 200**, 439 lines, sha256
`3116cc9ee8d1c7bbd12649e7203e813d2e4335b9bc9dd76d20ec87ce5f430123` on 2026-10-28.

## Observed outputs (verbatim)

Census on a copy of the tip registry, unmodified — the baseline:

```
file	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
[13 further W04 lines, all pre-existing, elided here]
file	ok	<scratch>/lane/corpus/SOURCES-testbase.md
```
(15 `W04` lines, 0 `E` lines, `validate` exit 0.)

The lane's own adoption gate on the **five landed** rows, quotes where they sit today:

```
QUOTE rows=5 spans=0 located=0 found=0 overlong=0 absent=0 malformed=5 cap=25 … urlmap=caps-map.json entries=5
  REFUSED S173 no-quote
  REFUSED S174 no-quote
  REFUSED S175 no-quote
  REFUSED S176 no-quote
  REFUSED S177 no-quote
EXIT=4
```

Same spans moved unchanged into the anchor cell:

```
QUOTE rows=3 spans=4 located=0 found=0 overlong=0 absent=4 malformed=0 cap=25 … entries=5
  REFUSED S174 absent words=11 quote="a text file there containing the path to the actual repository"
  REFUSED S176 absent words=7 quote="Adds a 'replace' reference in refs/replace/ namespace"
  REFUSED S176 absent words=9 quote="is the SHA-1 of the object that was replaced"
  REFUSED S177 absent words=19 quote="The names of refs that are fetched, together with the object names they point at, are written to .git/FETCH_HEAD"
EXIT=7
```

The repaired rows (Option A: 5 rows, 12 spans) and the superseding rows (Option B: 5 rows, 12 spans):

```
QUOTE rows=5 spans=12 located=12 found=12 overlong=0 absent=0 malformed=0 cap=25 … mismatch=0 unmapped=0 … entries=5
EXIT=0
```

Package gates:

```
Option B:  registry=170 staged=5 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
Option C:  registry=170 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
```

Census, per variant (each `validate`, row count, exit, findings):

| variant | rows | exit | E | W04 |
|---|---|---|---|---|
| tip registry, unmodified | 170 | 0 | 0 | 15 |
| Option A in place | 170 | 0 | 0 | 15 |
| Option A + `git-clone` row | 171 | 0 | 0 | 15 |
| Option B S178–S182 appended | 175 | 0 | 0 | 20 |

Shape probes on scratch copies: a row with one cell removed → `E01 S178 fields=10`, exit 1; rows appended at end
of file → `E12 S178 row outside Registry section`, exit 1; a superseding row that reuses its original's `scope`
text → `E04 S178 duplicate url … within scope …`, exit 1 (cleared by a distinct correction scope).

## Findings

1. **Both scouts landed and agree with the byte-level reading**: keep ids S173–S177, open no new id, repair
   anchors. S175's `:285-292` on `git-worktree.adoc` is `--expire`'s `_<time>_`, `--reason <string>` and
   `_<worktree>_`; the gitfile/`$GIT_COMMON_DIR` pair is DETAILS `:365-378`. S177 starts one line late
   (`:41`, not `:42`). S174 stops one line short (`:73`). S173 `:26-28` misses the `gitdir: <path>` token
   (`:25`) and omits the `refs/replace/<obj-sha1>` entry (`:116-120`).
2. **The five landed rows are not gate-validatable, for two independent reasons** (both witnessed above): the
   quoted spans sit in `teaches`, where `plans/sources_adopt.py` does not look; and the spans themselves are
   markup-stripped/space-joined, so they are not substrings of the pin. Repairing the anchors alone does not
   clear this; the spans have to be re-cut from the bytes.
3. **A registry row cannot carry a wrapped quote.** The contract's quote rule and the one-line table shape are in
   tension: a sentence that wraps in the adoc has a newline inside it, and `quote_check` normalises newlines only.
   The working form — already used by S086/S092 — is several single-line spans, one per source line, which is what
   Options A and B do (12 spans, all `located`).
4. **A superseding row must change its `scope` cell**, or the census refuses it as a duplicate of the row it
   supersedes (`E04`, measured). Append position matters too: after the last registry row, inside `## Registry`.
5. **The alternates leg needs no new source row**: the layout page has no `security` section (the word does not
   occur); the borrowed-store note is the numbered item under `objects::` at `:44-50`, and the relative base is
   `:85-86`. Both are inside the S173 anchor Option A sets, and "not a path" for `refs/replace` remains the lane's
   inference rather than a quoted sentence — S176's teaches now says it as the inference it is.

## Limits

- No fence, counter, predicate or C2 audit was executed here; nothing in this report is evidence for R50-C1 or
  R50-C2, and no admission is claimed.
- Byte-exactness is the gate's substring test against the committed captures, not an independent reading of the
  rendered manual; the unversioned git-scm.com pages are not the pin.
- The 15 pre-existing `W04` warnings belong to earlier rows; Option A changes none of them, Option B adds five of
  the same class.
- Option C's HTTP status, digest and line count are this seat's own fetch; no scout opened that page.
- I did not verify the repaired rows against `round50_c2_audit.py` — `corpus/SOURCES.md` is outside its frozen
  surface (SCORECARD/SHONEN/PROVINCE), so a row edit moves no C2 pointer; that is an expectation from the claims
  text, not a measurement of this seat.

## Scratch

`/fast/scratch/hyaku/kengaku-r50/R50FRScribeSources` held the `git clone --shared`, the registry copies, the
captures and the gate receipts. Every citable receipt is transcribed above or in
`R50FRScribeSources-rows.md`; the directory was removed before yield (`[ -e "$S" ]` false afterwards).

VERDICT: **rows drafted and gated, not applied.** The round-50 sourced basis needs an anchor-and-quote repair of
S173–S177, not a new id; Option A is clean on the census (170 rows, exit 0, 15 pre-existing `W04`, 0 `E`) and
green on the lane's own quote gate (12/12 spans located), Option B is the append-only equivalent at the cost of
five duplicate-URL warnings, and Option C is available but not recommended for this round.
