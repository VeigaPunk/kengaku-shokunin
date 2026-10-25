# R32RevGate — row-draft and gate-mechanics review, round 32 C1

- Seat: `L1Kengaku32.R32RevGate` (reviewer, leaf). Lane:
  `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; claims freeze `plans/round-32-claims.md`
  (0d32691d); access date 2026-10-25.
- Object reviewed: `R32DraftRows.md` (row drafts S094/S097 + S093 `used-by` proposal), against
  the staged package `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`, the scout
  reports `R32SrcS094a/b.md`, `R32SrcS097.md`, `R32LearnC1.md`, the gate scripts
  `plans/adoption_check.py`, `plans/round32_c1_verify.py`, `plans/sources_adopt.py`, and the
  fleet census `scripts/sources-census.sh`.
- Captures checked byte-wise: S094 `main.py` (14,138 B, sha256 `3bad26b6…`), S094 `retry.py`
  (4,519 B, sha256 `db11e66e…`), S097 arXiv abs page v2 (43,661 B, sha256 `44195c5f…`),
  S093 `tests/test.sh` at `66f92766` (7,864 B, sha256 `b6f26eec…`; fetched to
  `/tmp/r32-R32RevGate/s093-test.sh`). All digests match the sibling seats' captures.

## Row-level checks (assignment items a–g)

| Check | Result | Evidence |
|---|---|---|
| (a) exactly 11 columns, no literal/escaped `\|` inside cells | PASS | parsed both draft rows: 11 cells each; no `|` or `\|` in any cell; byte sizes 1,777 (S094), 1,166 (S097) |
| (b) `opened=2026-10-25` for S094/S097; S093's existing `opened` stays valid | PASS | S094/S097 cell 8 = `2026-10-25`; S093 row (`corpus/SOURCES.md:112`) cell 8 unchanged = `2026-10-25` (opened_ok in adoption_check requires cell 8 == access date for all three cited rows) |
| (c) `used-by` exactly names the admitted entry | PASS | S094/S097 cell 10 = exactly `corpus/knowledge/benchmark-grader-semantics.md`; S093 cell 10 gains that path as second part (adoption_check splits on `,` and strips, so `usedby_ok` holds) |
| (d) S093 `used-by` change is old->new, append-only | PASS | mechanically verified on the live row: only cell 11 changes; old cell preserved byte-for-byte as prefix; `new == old.replace(old_cell, new_cell)`; 923 -> 971 bytes (+48) |
| (e) anchors are byte substrings of the captures | PASS | all 14 quoted spans in the draft anchors verified present in the pinned bytes (`main.py`, `retry.py`, `abs.html`); S093's three spans (`test.sh:33`, `:71`, `:214`) verified against the pinned fetch. S097 abstract quote uses the true `LLMs-as-judges` bytes (the staged row's `LMs-as-judges` would have been absent — fixed in this draft) |
| (f) recheck is a cadence, not prose | PASS | both new rows cell 9 = `180d` (census E09 accepts `NNd`); the staged cells' prose (`2026-10-23 — re-verify at …`) is replaced |
| (g) status mined | PASS | both new rows cell 7 = `mined`; S093 remains `mined` |

## Gate mechanics

- `adoption_check.py` row-side clauses (rows_present / rows_mined / usedby_ok / opened_ok) are
  satisfied by the draft's cells on a simulated append; `usedby_ok` requires the entry path among
  the comma-split parts of cell 10, which the S093 append preserves.
- Fleet census on the simulated append (real registry + two rows + stub entry): exit 0, findings
  identical to baseline (15 × W04, no E-code). E09 accepts `180d`; E08 accepts today's `opened`;
  E11 requires the entry file on disk (see ordering note below).
- `sources_adopt.py` quote gate (already exercised by `R32QuoteMode.md` on the staged rows)
  confirms the corrected S097 quote would bind; exit 7 in that run was caused by the staged
  `LMs-as-judges` typo the draft fixes.

## Findings by severity

None (no row-level defect in the reviewed draft).

Operational notes (not row defects, route to the Gate):
1. **Landing order is load-bearing (F6 in the draft).** Census E11 resolves every `used-by` path on
   disk; `corpus/knowledge/benchmark-grader-semantics.md` does not exist at baseline. Appending the
   rows before the entry file lands makes validate emit three E11 lines (S093's new path, S094,
   S097). Rows + entry + README index row must land in one commit, or entry-first.
2. The `--census` half of `adoption_check.py` and `round32_c1_verify.py --lane .` are unrun on the
   real landed tree (they need the entry/README bytes, other seats' deliverables). An unrun check
   has not passed.
3. Cosmetic citation variant: `R32DraftEntry.md` cites `arxiv.org/abs/2412.05579v2`; the row cites
   `arxiv.org/abs/2412.05579`. No counter compares them; align if the lane wants byte-equal citations.
4. The staged package contains non-C1 rows (e.g. S103 names an absent used-by path and would raise
   E11); they must be excluded by the collision guard, as the draft notes.

## Residual risk / verification gaps

- The row strings were validated against pinned bytes, not against a rendered page (S097 quote sits
  inside the `<blockquote class="abstract mathjax">`); byte-substring semantics hold as specified.
- S094 describes one Toolathlon task's evaluator (`ab-testing`) — the draft and entry both state
  that limit; it is not a benchmark-wide claim.
- Final gate receipts on the real landed tree remain to be run by the main agent after the entry and
  index row land (per note 2).

VERDICT: rows-clean
