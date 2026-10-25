# Round 33 — renumbered assimilation, routed-defect closure, byte-retained catalogs (2026-10-25, hyaku run 7)

Baseline `112091c2d9`; frozen prereg `plans/round-33-claims.md` (freeze commits `f0b20aea` +
`c227e486`). Round shape: one v1 build wave of 36 seats + one v1 falsify wave of 36 seats
(dispatched inline via the orchestrator's `.ready` bridge; results recorded below).

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `benchmark-grader-semantics.md` (admission patch of the round-32 draft) | **Admitted** | Re-grounded this round: staged S094 → **S103** (Toolathlon `tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`), staged S097 → **S104** (arXiv 2412.05579v2), both opened 2026-10-25; S093 (already `mined`) gains the entry in `used-by`. The four round-32 refusal rows (S094, S097, S101, S102) stand unchanged — ids never reused (CORPUS.md rule 2). Gate receipts: `plans/sources_adopt.py` collision/schema gate `collisions=0 defects=0` exit 0; quote gate 4/4 located, 0 overlong, `url-map` bound exit 0 (`.ufo/waves/round-33/assimilation/gate-receipts.txt`). |
| Staged catalog rows S101/S102 (SWE-bench locked replay + release map) | **Rejected** | Not cited by the admitted entry; CORPUS.md rule 4 forbids appending rows no admitted entry cites. Their round-32 refusal rows stand. Flip: a later entry that cites them re-grounds them under unused ids. |
| Staged `judge-calibration-thresholds.md` (un-admitted kappa table) | **Rejected (carry-over)** | Still refused: its kappa figures (0.84/0.46/0.21) appear in no anchor cell (Q3); unchanged from rounds 29–30. |

## Assimilation record (operator directive, §10)

- Theme: *benchmark grader semantics* (package `merge/kengaku/`, 1 entry, 3 cited rows).
- **Renumber map (by document, never arithmetic):** staged S094 → lane **S103** (Toolathlon
  evaluation/main.py @ `9be8d8fe`, tier A); staged S097 → lane **S104** (arXiv 2412.05579v2,
  tier B preprint). S093 already `mined`; `used-by` gains the entry. Id lists: reg-ids
  S001–S102, staged ids through S104+, collisions S094/S097/S101/S102 (staged package) → the two
  adopted rows take S103/S104. Guard proof: `.ufo/waves/round-33/assimilation/idguard-*`.
- Re-grounded quotes (located this round): S103 `main.py:58` signature (0.1 default) vs `:280`
  executed call (0.05); S104 Abstract 20-word quote at `arxiv-2412.05579v2-abs.html` — the staged
  anchor's "LLMs-as-judges" quote verified in-capture (title `citation_title` line 116).
- `## Gate` records ≥1 admit (above) and ≥1 reject (S101/S102 catalog rows, threshold entry).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| landing | `.ufo/waves/round-32/` — 89 files sat untracked at a pushed tip (round-32 closure §5) | round-32 verifier spotcheck `## 5`; Q19 | committed under round 33 (`c227e486`); counter `plans/round33_defects.py` N1 now guards it at every tip |
| number-drift | `corpus/README.md` + committed draft `benchmark-grader-semantics.md` cited the *refused* ids S094/S097 — an entry file whose citations are rejected rows | none (Q21 names the pin, not the *row health*) | re-pointed to S103/S104 this round; V8 in `plans/round33_c1_verify.py` now fails if the refusal rows are overwritten |
| scope | staged S094 row misstated the executed tolerance (0.1 default vs 0.05 invoked) and overbroadened a fail-open claim (absent credentials fail *closed* via implicit `None`) | r32 falsify seats `FxFailOpen`, `FxTolerance`; entry `:47-53` corrected wording | stated precisely in S103's row + entry |
| reference-drift | staged S097 anchor dropped one L in "LLMs-as-judges" (round-32 refusal record) | r32 refusal row S097 | corrected in S104's anchor + entry `:64` |
| stale-premise | r32 C3's frozen predicate required zero missing fields while HF's default projection legitimately dropped four — a predicate that can never pass honestly | `catalogs/after.txt` hf_schema_delta=4 | round-33 C3 freezes a byte-retention + re-derivation predicate instead of a zero-delta one |
| landing (own round) | `git cat-file -t a44b5a8` fails in both repos — the round-31 report's "lane tip" is a phantom hash | round-31 verifier spotcheck §5 D1; `plans/round33_defects.py` N3 | appended erratum names `ae95fe0` (fleet commit `3d3ca566`); the token stays verbatim per append-only |

## Seat ledger

Wave-1 build: 36 seats dispatched via the orchestrator's inline spawn bridge
(`.ufo/waves/round-33/build.ready` → `build-results.json`). Reports live under
`.ufo/waves/round-33/build/`; dead seats (if any) are recorded against the registry after
results land. Wave-2 falsify: 36 seats (same bridge). Seat-level ledger appended below once
both results files land.

## Round-33 disclosures

- The round-32 closure (`corpus/lessons/round-32-verifier-spotcheck.md`) routed 6 items;
  N1–N6 all re-derive green (`corpus/evidence/round33/defects-after.txt`, `checks=6
  defects=0`, exit 0, at the landing tip).
- The four refusal rows at S094/S097/S101/S102 stand unchanged; the adopted rows are new
  ids S103/S104 (append-only, CORPUS.md rule 2).
- `corpus/QUALITY.md` gains **Q22** (a receipt is only evidence if something re-runs it at the
  tip) — considerthese/2026-10-25 proposal 2's cheap half; the persistent `defects.jsonl`
  ledger it sketches stays unimplemented debt, named in the criterion.
- considerthese/2026-10-25 proposal 3 landed as an L0 decision-packet append (fleet
  `l0-questions.md`, commit `22d28422`); proposal 1 (model-diverse verification) is
  operator-side and not lane-actionable.
