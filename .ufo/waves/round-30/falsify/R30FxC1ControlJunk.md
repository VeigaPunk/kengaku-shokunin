# R30FxC1ControlJunk — C1 control junk: the counter passes an entry whose quotes are invented

Seat: `L1Kengaku30.R30FxC1ControlJunk-3` (executor, calibration). Round 30 falsify wave, hyaku run 6.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, HEAD `363a4eb` (detached), round-30 bytes
uncommitted. Scratch root `/tmp/r30fx-c1controljunk/`. Lane writes: this file only. No installs, no
upgrades, no pacman transaction.

Counter under test: `plans/adoption_check.py`. Expect file: the lane's own
`.ufo/waves/round-30/adoption-expect.json`. Command shape, for every row below:

```
python3 plans/adoption_check.py --lane /tmp/r30fx-c1controljunk/<v>/kengaku-shokunin \
        --expect .ufo/waves/round-30/adoption-expect.json --census
```

Each `<v>` is a full copy of the lane (`rsync -a --exclude .git`) under its own census root with a
one-lane `shokunin.conf`, so the census subprocess validates the copy's registry, never the lane's.

**The counter moved under this seat.** Two revisions were measured, and every exit code below is
given for both:

| rev | sha256 of `plans/adoption_check.py` | what it is |
|---|---|---|
| R1 | `cb6fc038481b6462e7eb3bace6761033ffda88fc52669960348936b721b93af2` | `git show HEAD:` bytes — the counter the round froze and the C1 receipt was taken with |
| R2 | `f9f8188efb3612c1a1a9d7a3e2272255096b76bd3100d3dacdded63dd7d69926` | working tree mid-wave: a sibling falsify seat's patch adding `ids_ok`, `duplicates_ok`, `opened_ok`, `index_shape_ok` (git status `M plans/adoption_check.py`) |

R2 landed after my R1 pass; my findings are re-measured on it rather than assumed. R2 changes the
exit code only — the printed line is the same seven fields in both revisions, so no run below can be
told from another by its output text.

## Result: the junk entry exits 0 on both revisions

| # | bytes changed in the copy | printed line | exit R1 | exit R2 |
|---|---|---|---|---|
| b0 | none (baseline: the real entry) | `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok` | **0** | **0** |
| j1 | entry body replaced by six `source:` lines, each carrying **one fabricated quote**, + `verified-at: 2026-10-25` (1692 B) | identical | **0** | **0** |
| j2 | entry is **seven lines / 102 B total** (`source: S081` … `source: S086`, `verified-at: 2026-10-25`), zero quote bytes anywhere | identical | **0** | **0** |
| j3 | j1 with `S086` replaced by `S090` (that row's `used-by` appended in the copy) | identical | 0 | **1** |
| j4 | j1 with all six rows' `opened` cell set to `2025-01-01` | identical | 0 | **1** |
| n1 | j1 minus the `S086` line (liveness control) | `… cited_rows=5 rows_present=5 rows_mined=5 …` | 1 | 1 |
| n2 | j1 with `verified-at: 2026-10-24` (liveness control) | the same line j1 prints | 1 | 1 |

b0 reproduces the shipped receipt `corpus/evidence/round30/adoption-after.txt` byte for byte under
both revisions, so the harness is the round's own run and not a lookalike. j1 is the assigned attack:
shape met, truth absent, **exit 0**, same seven-field line as the real entry, and the copy's registry
passes `sources-census.sh validate` with exactly the lane's 14 `W04` warnings and no `E` finding.

Fabricated spans written in j1 (kept verbatim at
`/tmp/r30fx-c1controljunk/j1/kengaku-shokunin/corpus/knowledge/contamination-transparency-card.md`),
one per cited row, each in its source's register and each absent from every capture:

`"Every contamination figure is published with the benchmark release and never with the individual run."` (S081)
`"Publishing the full item pool is the strongest available evidence of contamination control."` (S082)
`"Cards are printed in the repository and their contents are never hidden from the model builder."` (S083)
`该方案已经覆盖全部主流数据集` (S084) · `方升体系从不重复使用任何测试题目` (S085)
`"Precision and recall of the detector are both reported as exactly 1.00."` (S086)

## The blind spot, stated exactly

The counter reads the entry for two things and only two: `^source: (S\d{3})` — the **id**, never the
bytes after it (`SOURCE_LINE_RE`) — and `^verified-at: <access_date>`. Everything else it counts comes
from the registry (`status` at cell index 7, `used-by` at index 10), the README index anchor, and the
census subprocess. Its docstring claims "landed state from committed bytes"; the frozen predicate in
`plans/round-30-claims.md` claims more ("the same condition in the counter's code"). Measured, the
code is narrower than that sentence, and j3/j4 show the gap is closable while quote truth is not
touched:

1. **Quote truth — the assigned gap, open on R1 and R2.** No quote is parsed. j1 (six invented
   quotes) and j2 (no quote text at all, 102 B) both score `cited_rows=6 … usedby_ok=1` and exit 0.
   The counter cannot distinguish an entry that located six spans from one that located none.
2. **Entry body is never read — open on R1 and R2.** j2 is the whole entry: six id lines and a date.
   The claim, the CG1–CG8 table and the coverage map the admission rests on contribute nothing.
3. **`opened` — open on R1, closed on R2.** j4 moves all six `opened` cells to `2025-01-01`: R1
   passes, R2 refuses (`opened_ok=0`). The frozen predicate names `opened=2026-10-25`; R1's code
   never read cell 8, and `sources-census.sh` `E08` only rejects non-dates.
4. **Cardinality, not identity — open on R1, closed on R2.** j3 cites S081–S085 plus S090 and R1
   prints `cited_rows=6`: `len(cited) == required` compared counts, and the expect file's `sources`
   arrays were never compared to the ids found. R2 compares sets and refuses.

n1/n2 show the checks that exist are live, not vacuous: one missing link drops to `cited_rows=5`
exit 1 under both revisions, and a one-day `verified-at` slip exits 1 while printing the green line.

Items 3 and 4 are **not my discovery and not my repair**: `corpus/lessons/round-30.md` §"Counter
blind spots (recorded, not smoothed)" names both (plus item 2), and the R2 patch is a sibling seat's.
What this seat adds is that each is now *measured* on the shipped counter, that 3 and 4 are dead on
the current bytes, and that 1 and 2 survive R2 intact — the two the round's own gate can already
settle for one and cannot settle at all for the other.

## Which round-30 artifact carries quote truth

`plans/sources_adopt.py` in quote mode — `--quote-file <rows> --artifact <capture>` (C3's new body;
exit 6 = over-long span, exit 7 = span absent from the artifact bytes). It is the only artifact in the
round that reads quote bytes. Differential against one 14-file capture bundle built from the wave-1
fetch dirs `/tmp/r30-R30SrcS08{1..6}`:

```
# real rows, copied verbatim from corpus/SOURCES.md
QUOTE rows=6 spans=13 located=11 found=11 overlong=0 absent=2 malformed=0 cap=25 ...
exit=7
# the j1 fabricated rows
QUOTE rows=6 spans=6  located=0  found=0  overlong=0 absent=6 malformed=0 cap=25 ...
exit=7
```

So the gate separates the two entries the C1 counter scored identically: 11/13 real spans locate,
0/6 invented spans locate, and every refusal is printed with its row and its quote. C1's counting
command never calls it, and no round-30 artifact records the gate's verdict on this entry's six rows.

The two real-span refusals are limits of my bundle, not evidence against the entry, and they bound
what the gate can decide:

- S083 span 1 (`a contamination-resistant design …`): the PDF text layer renders
  `contaminationresistant` — the hyphen is not extracted. Confirmed on a fresh
  `pdftotext -f 1 -l 1 /tmp/r30-R30SrcS083/S083.pdf`, which yields the same fused form.
- S085 span 1 (`“方升”测试体系提出…`): in `caict.txt` the span crosses a line break, and
  `normalize_text` converts only CRLF→LF, so a wrapped quote cannot locate.
- `load_artifact` skips every artifact that is not UTF-8, i.e. every PDF: S083, S085 and S086 are
  PDFs, so quote truth for half the cited rows depends on a caller-supplied text extraction.

## Does the lesson say so

Yes — the shape-only scope is stated plainly in §"Counter blind spots (recorded, not smoothed)":
"registry cell 8 (`opened`) is never read", "it compares the *cardinality* of cited ids, not their
identity", "the entry body and the coverage-map row are never read, so a six-line stub passes". It
also names the carrier for quote truth: "quote truth is carried by the six falsify re-reads, not by
the counter". Three qualifications, measured:

- The artifact the lesson names as the cover for `opened` — `corpus/evidence/round30/rows-opened.tsv`
  — has three tab-separated fields on every line (`id`, `status`, `teaches`) and **no opened date**.
  The value the lesson says is "re-derived" there is not in the file; checking it needs the registry.
  j4 is what that costs: on R1 nothing failed when the cells moved.
- The named quote-truth carrier is six wave-2 reports (`.ufo/waves/round-30/falsify/R30FxSrcS081.md`
  … `R30FxSrcS086.md`). Five are on disk at this read (S081–S084, S086); `R30FxSrcS085.md` is not yet
  written. Prose reports are not a machine check either way, and the gate that is one is not named
  in the lesson as C1's truth layer.
- The lesson never binds this round's own gate to C1's quote truth: C3's quote mode is described in
  the same lesson only under C3's `Measured` line.

Blind-spot verdict (counter shape): **CONFIRMED** — a fabricated entry exits 0 with the real entry's
own line on both counter revisions, and the round's quote-truth mechanism is a separate command that
refuses the same bytes with exit 7.

No anchored `VERDICT:` line is emitted: this seat is neither a source re-read nor the complete-set
review, so it carries no verdict on `corpus/knowledge/contamination-transparency-card.md`'s
admission. Its two refusals above are capture limits and are labelled as such.

## Limits of this seat

- Every run is on a `/tmp` copy; the lane's bytes were not modified, so nothing here attacks the
  committed C1 receipt itself, and j3's registry edit (`S090` `used-by` appended) is copy-only.
- My capture bundle is rebuilt from wave-1 scratch, not re-fetched: if a wave-1 capture was itself
  wrong, the 11/13 figure moves. No network fetch was attempted.
- The R1→R2 change was made by a sibling while this seat ran; I cite both hashes and did not review
  that patch beyond the four gates its diff adds.
- I did not run `sources_adopt.py --selftest`, `round30_defects.py`, or any build/lint/test: the
  parent owns post-integration gates.
- Reproducer: `/tmp/r30fx-c1controljunk/{b0,j1,j2,j3,j4,n1,n2}/kengaku-shokunin`, plus
  `captures/`, `real-quotes.txt`, `junk-quotes.txt`; each variant root carries its own
  `shokunin.conf`. R1 is pinned there as `adoption_check-R1.py` (`git show HEAD:` blob, sha256
  `cb6fc03…`), and j1/j2/n2 were re-run from that blob directly rather than inferred from the diff.
