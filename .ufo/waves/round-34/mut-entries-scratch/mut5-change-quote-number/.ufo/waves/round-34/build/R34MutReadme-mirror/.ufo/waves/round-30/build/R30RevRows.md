# R30RevRows — audit of proposed registry rows S081–S086

Seat: `L1Kengaku30.R30RevRows` (leaf reviewer, 2026-10-25). Scratch: `/tmp/r30-R30RevRows/`.
Nothing installed or upgraded (bash/gawk/python3/poppler already on PATH; no tool was missing).

## Inputs audited

`build/R30RowSchema.md` was **not present** at audit time (checked twice, 04:24–04:35). Per the
assignment the fallback applied: the staged rows in
`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md` lines 11–16 — **and** the
operative proposal they feed, the gate-normalized append block
`/tmp/r30-BuildAppend/block.txt` (produced by `plans/sources_adopt.py` from the staged rows).
The two differ only in `opened` (staged `2026-10-23` → normalized `2026-10-25`), `recheck`
(staged prose `2026-10-23 — re-verify…(Gate S08x)` → normalized `180d`), and `used-by`
(staged 2-path lists incl. `judge-calibration-thresholds.md`/`cjk-eval-venue-access.md` →
normalized `corpus/knowledge/contamination-transparency-card.md` alone). All checks below are
against the normalized block, which is what the census will see; staged-only leftovers are
named separately at the end.

## Census result

```
sh /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --file /tmp/r30-R30RevRows/only/corpus/SOURCES.md        # six rows alone + stub entry
→ file  ok  /tmp/r30-R30RevRows/only/corpus/SOURCES.md     EXIT=0
```

- **Zero E-findings on S081–S086** in isolation (no E01/E02/E03/E04/E05/E06/E07/E08/E09/E10/E11/E12),
  and zero W-findings. Scratch = header + separator + the six rows + stub
  `corpus/knowledge/contamination-transparency-card.md` so E11 reflects post-admission state.
- **Full-registry mirror** (live `corpus/SOURCES.md` + six rows appended inside `## Registry`,
  `/tmp/r30-R30RevRows/mirror/`): the six new rows contribute **no E-findings and no
  warnings**. All E11s in that run are pre-existing rows whose used-by targets are absent
  from the stub-only mirror tree — not from the proposal. Pre-existing W04 duplicates
  (S040, S048, S057–S059, S064–S069, S071, S075–S076) are unchanged; none of the six new
  URLs collide with any existing row (verified by re-implementing the census `url_of`
  normalization — scheme/fragment/trailing-slash stripped, host lowercased — against all
  82 live rows: zero same-URL-same-scope non-rejected pairs, zero cross-scope repeats).
- **E11 ordering caveat** (not a defect, a landing-order fact): run without the stub, the six
  rows each raise `E11 missing used-by corpus/knowledge/contamination-transparency-card.md`.
  The entry file must land in the same commit as (or before) the rows — C1's plan commits
  both together, so this is informational.
- **E03**: S081–S086 are the next unused ids (live registry tops out at S091; S081–S089 free;
  the block uses six of them once each). No duplicate-id finding.

## Per-row cell verdicts

Legend: cells = id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by.

| id | 11 cells (NF=13) | pipe-free | quote ≤25w | tier | URL dup | used-by exact | verdict |
|----|------------------|-----------|------------|------|---------|---------------|---------|
| S081 | PASS | PASS | **FAIL (30w)** + location ambiguity | B defensible | none | exact | **DEFECT** |
| S082 | PASS | PASS | PASS (11w, 17w) | B defensible | none | exact | **anchor section-name defect** |
| S083 | PASS | PASS | PASS (14w, 19w) | A defensible | none | exact | PASS (hyphen note) |
| S084 | PASS | PASS | PASS | A defensible | none | exact | PASS |
| S085 | PASS | PASS | PASS (CJK tokens) | B defensible | none | exact | **nested-quote ambiguity** |
| S086 | PASS | PASS | PASS (CJK tokens) | A defensible | none | exact | PASS |

### S081 — two defects in `anchor`

1. **Quote over the ≤25-word bar.** The anchor quotes
   `"We operationalize the taxonomy as a four-field disclosure protocol in which unknown is a
   valid entry, released under CC BY 4.0 with a JSON Schema, a validator, and worked
   examples."` — **30 whitespace words** (I counted). Contract v1 rule 1 and the round-29
   convention: every quoted span in a row grounds `teaches` at ≤25 words; a census of all 82
   live rows shows **zero** >25-word quoted spans — this would be the registry's first.
   Fix that stays honest: quote the second half alone —
   `"released under CC BY 4.0 with a JSON Schema, a validator, and worked examples"` (14 words)
   — or the short sentence `"Holding out a private test set closes the first of these alone."`
   (11 words, verified present, PDF abstract).
2. **Version ambiguity in the location.** The quote is attributed to `§ Abstract`. It is a
   byte-substring of the **PDF** abstract (verified by me: `/tmp/r30-R30RowSchema/s081.txt`
   line 28 wraps it mid-sentence) but the **abs-page/HTML abstract** reads "We operationalize
   **it** as a four-field…" (`operationalize the taxonomy` = 0 hits in `abs.html`, fetched
   2026-10-25 by both the Src seat and the RowSchema seat). `arXiv 2608.29463, § Abstract` is
   true of the PDF and false of the HTML — under "a quote names its location" the anchor
   should say `§ Abstract (PDF)` or `PDF p.1 abstract` to be checkable. Not a kill-rule
   refusal (the bytes exist in a fetched artifact) but the location is ambiguous as written.
   Note the teaches-cell claim "contamination acquired during a run is a property of that run"
   IS supported by the PDF abstract (`The fifth is acquired during evaluation; because it is
   a property of one run, it must be recorded with the reported score…`).

   Tier B: defensible — arXiv preprint, scope cell itself declares "not peer reviewed at the
   time of opening"; consistent with S097/S098 precedent.

### S082 — anchor section-name defect

Both quotes verified byte-present (11 and 17 words). But the anchor locates them at
`§ Benchmark Governance`; the fetched text (`/tmp/r30-R30RowSchema/s082.txt` lines 854–855,
942) places them inside **§7.3 "Governance Design: Protected Items and Procedural
Transparency"** under §7 "Governance Implications" — the paper has no section named
"Benchmark Governance". "A quote names its location" fails as written; correct the anchor to
`§7.3 Governance Design`. Tier B: defensible (working paper, self-declared).

### S083 — pass with a note

Both quotes verified (14w `…separating the publicly released game engine from hidden card
implementations`; 19w threat-model/refresh-protocol sentence). Minor: PDF text extraction
renders `contamination-resistant` as `contaminationresistant` (line-break dehyphenation), so a
naive byte-substring check against the *extracted text* fails although the printed glyph
string is faithful — worth normalizing hyphens in C3's gate or choosing the second quote as
the byte-substring anchor. Tier A: defensible — ACL Findings EACL 2026, DOI
10.18653/v1/2026.findings-eacl.353, peer-reviewed for its own design claim.

### S084 — pass

Quotes verified in the fresh fetch (`/tmp/r30-R30RowSchema/s084.html` lines 344, 315):
`目前该方案仅支持 GSM8K 数据集` and `这些问题还没有被广泛接受的解决方案`. Tier A:
defensible — official OpenCompass 0.4.0 documentation for its own documented procedures.
Anchor could additionally name the second method's coverage (`目前该方案仅支持 C-Eval, MMLU,
HellaSwag 和 ARC 数据集`, line 397) but omission is not a defect.

### S085 — nested-quote ambiguity (readability defect, not census-fatal)

`§ 5. 测试数据集的"污染"问题` verified (line 883 of fresh text). Both Chinese quotes verified
byte-present (whitespace-normalized; the adaptive-testing quote wraps at line 1013–1014).
**Defect:** the source's fullwidth quotes `“污染”`, `“刷榜”` were flattened to ASCII `"` inside
an already-`"…"`-quoted span, producing 12 ASCII quote marks in one cell; any `"…"`-pairing
reader (incl. a quote extractor for C3's gate) truncates the span at the first inner `"`,
yielding `产学研各界需要研究数据` instead of the full sentence. Restore `“”` for the inner
quotes (they are the source's actual glyphs) or switch the outer delimiters to 「」.
Tier B: defensible — CAICT institutional report, row itself records "no document number".

### S086 — pass

`§概要`/`§1 はじめに` verified (text lines 11/19, 27). Both Japanese quotes byte-present
(whitespace-normalized). Tier A: defensible — ANLP第31回年次大会 peer-reviewed proceedings,
p. 797, with the no-DOI caveat honestly recorded in `scope`.

## Staged-file leftovers (normalized away, but recorded)

The staged `SOURCES.append.md` rows — if anyone bypassed the gate — carry three additional
defects the normalization already repairs: `opened=2026-10-23` (wrong access date; E08-clean
but predicate-false), `recheck="2026-10-23 — re-verify at the next upstream release (Gate
S08x)"` (**E09**: starts with a digit so the census `symbolic()` test fails; it is neither ISO
nor `NNd` nor `[A-Za-z]…`), and `used-by` listing two paths including non-admitted entries
(`judge-calibration-thresholds.md`, `cjk-eval-venue-access.md`) — E11 landmines plus a
predicate violation ("name exactly the admitted entry"). The gate's normalization is load-
bearing; do not hand-append the staged rows.

## Summary

- Census on the proposal: **clean, exit 0** (warnings allowed; none raised for the new rows).
- E03/E04: **none** — all six ids unused, all six URLs unique under census normalization.
- Blocking defects: **S081** (30-word quote; ambiguous `§ Abstract` location across PDF/HTML
  versions), **S082** (anchor names a nonexistent `§ Benchmark Governance`; quotes live in
  §7.3), **S085** (inner fullwidth quotes flattened to ASCII, breaking quote-pair parsing).
- Non-blocking notes: S083 hyphen-extraction artifact for byte-substring gates; S084 anchor
  could add the second method's coverage sentence; all six `used-by` cells correctly name
  exactly the admitted entry `corpus/knowledge/contamination-transparency-card.md`, which
  must land with the rows to keep E11 clean.
