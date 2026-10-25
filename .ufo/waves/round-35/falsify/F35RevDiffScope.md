# F35RevDiffScope — round-35 wave-2 falsification: diff/scope review

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` @ `dfee6fff631ebc5f623ba4506e5c7992a215401c` (master).
Range under review: `58a19f37312e1b22fd2a7957bdfc6bb7832aadd0..dfee6fff631ebc5f623ba4506e5c7992a215401c` (7 commits).
Freeze: `11d64530179b78e33ba6074fc77d63d36ee7ac31`. Frozen claims: `plans/round-35-claims.md` (Separability §, read in full).

## Axes attacked

- **A1 surface containment** — every changed path inside the round's declared surfaces (claims Separability § + the frozen instruments/controls the claims name + standard round bookkeeping + `.ufo/waves/round-35/` wave evidence).
- **A2 freeze integrity** — the frozen counters (`plans/round35_c1_verify.py`, `plans/defect_ledger.py`), probe (`plans/tb2_grader_probe.py`), claims file, and claims-dir controls are byte-identical from `11d64530` to the tip.
- **A3 deletion containment** — deletions are only the round-34 mirror/scratch roots.
- **A4 commit attribution** — which commit moved what, especially writes into `.ufo/waves/round-34/`.
- **A5 protected-content preservation** — modified tracked files are insertion-only; no row/section of any standing corpus or top-level doc deleted.

Range shape: `151 A / 109374 D / 8 M / 39 R100` —
`git -C <lane> diff --name-status 58a19f37 dfee6fff631ebc5f623ba4506e5c7992a215401c | cut -f1 | sort | uniq -c`
→ `151 A`, `109374 D`, `8 M`, `39 R100` (git warns rename detection was non-exhaustive; does not affect the A/D classification below). Total 109572 ✓.

## Checks run (agreement, with the evidence that would have shown disagreement)

1. **A2 frozen counters/probe byte-identical after freeze.**
   `git diff 11d6453 dfee6fff… -- plans/round35_c1_verify.py plans/tb2_grader_probe.py plans/defect_ledger.py` → **empty output, exit 0**. No post-freeze change to any frozen counter/probe/ledger. (Had there been one, that diff would have printed hunks — the falsifying observation space was exercised.)
2. **A2 claims file untouched post-freeze.** `git log --oneline 11d6453..dfee6fff… -- plans/round-35-claims.md` → empty. The only post-freeze commit touching the 3-path probe set (claims dir / hardening / claims.md) is `4fe72a9`; per-path `git show --stat 4fe72a9 -- plans/round-35-claims.md` is **empty** — that commit's claims-adjacent writes are two *new* files (see O1), not a frozen-rule edit.
3. **A2 freeze commit contents.** `git show --stat 11d6453` → exactly 12 artifacts, 721 insertions, 0 deletions: `claims/census-before.txt`, 5 `claims/control-*` files, `corpus/defects.jsonl`, `plans/defect_ledger.py`, `plans/round-35-claims.md`, `plans/round35_c1_verify.py`, `plans/tb2_grader_probe.py`. The frozen namespace is otherwise untouched post-freeze except O1's addition.
4. **A3 all 109,374 deletions under the round-34 roots.** Same `--name-status` piped to awk: `deleted-outside-round-34: 0`, `deleted-total: 109374`. Prefix histogram of the deleted set: `…/round-34/mut-entries-scratch/{mut1..mut5}` (5×17622 + 17616), `…/round-34/mut-entries-scratch/.ufo` (17521), `…/round-34/build/R34MutRegistry` (3082), residue = `mut-entries-scratch/{corpus 515, plans 136, considerthese 7, 8 top-level mirror files}`. All are round-34 mirror/scratch trees (the mut-entries scratch's full lane mirrors incl. its own AGENTS.md/SKILL.md/SCORECARD.md copies, and R34MutRegistry's mirror). **Zero deletions anywhere else in the lane.**
5. **A1 every added path in-scope.** All 151 A-paths fall in: `corpus/defects.jsonl` (C2), `corpus/evidence/round35/` (C1), `corpus/knowledge/tb2-protein-assembly-grader.md` (C1), `corpus/lessons/round-34-verifier-spotcheck.md` + `round-35.md` (C2's D-source and lesson), `plans/{defect_ledger,round35_c1_verify,tb2_grader_probe,round35_hardening}.py` + `plans/round-35-claims.md` (frozen instruments + post-hoc hardening, O1), `.ufo/waves/round-34/build/R34MutGrader.scratch/{pristine,mutated}.jsonl` (2, round-34 surface, commit dfcd294), and 137 files under `.ufo/waves/round-35/` (wave evidence, spec/dispatch/results, controls). No added path outside the round's envelope.
6. **A1/A5 the 8 modified files are pure insertions** (numstat over the range): `.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS +2` (D3 manifest erratum — Separability's declared "manifest"), `LOG.md +33`, `PROVINCE.md +12`, `SCORECARD.md +34` (incl. the D4 correction line), `corpus/QUALITY.md +24` (Q23), `corpus/README.md +10` (C1 frontier clause), `corpus/SOURCES.md +3`, `corpus/lessons/round-34.md +4` (D5 erratum). No deletions in any modified file — no standing row/section was removed.
7. **A5 SOURCES.md delta is exactly S105–S107.** `git diff 58a19f37 dfee6fff… -- corpus/SOURCES.md` → 3 added rows appended after S104, before `## Paths`; row ids S105 (`tests/test_outputs.py`), S106 (`tests/test.sh`), S107 (`instruction.md`), all pinned at `2fd12b88aafdd04a52c298e3940bcb189f9766d6` — matching the claims' source list. No existing row modified or dropped.
8. **A4 the baseline tail is clean.** `git show --stat 5d0c73d` (round-34 verifier spot-check, the only commit before the freeze) → exactly `corpus/lessons/round-34-verifier-spotcheck.md +80`. That file is C2's cited D-source (`round-34-verifier-spotcheck.md:75-79` per the claims). In-scope.
9. **A4 all writes into `.ufo/waves/round-34/` come from dfcd294** (`git log --oneline 58a19f37..dfee6fff… -- .ufo/waves/round-34/` → only dfcd294), the C2 commit whose own subject declares "drafts committed, mirror roots deleted, manifest, D4/D5 corrections" — i.e. the Separability §'s declared round-34 scratch/manifest/lesson-erratum surface. The 3 R100 renames into `.ufo/waves/round-34/drafts/round34_{c1_verify,defects,mutate}.py` and the 2 added scratch jsonl are that commit's declared work.
10. **Ancestry.** `git merge-base --is-ancestor` → `58a19f37` yes, `11d6453` yes (both under the tip; the audited range is the real round history).

## Findings by severity

**Decisive violations: none found.** No post-freeze change to any frozen rule; no changed path outside the declared surfaces; no deletion outside the round-34 mirror/scratch roots.

- **O1 (minor, informational) — post-freeze additions inside the frozen claims namespace.** `git diff --stat 11d6453 dfee6fff… -- .ufo/waves/round-35/claims/ plans/round35_hardening.py` → `.ufo/waves/round-35/claims/hardening-counterexamples.sh | 59 +` and `plans/round35_hardening.py | 131 +` (190 insertions), both added by `4fe72a9` ("post-hoc hardening"), plus receipt `corpus/evidence/round35/hardening-counterexamples.txt`. This changes **no frozen file** — the counters, probe, ledger, claims and the 5 controls are byte-identical post-freeze (checks 1–3) — and `plans/round35_hardening.py:2` self-declares "Round-35 POST-HOC hardening checks — NOT the rule of either frozen claim." Grep over `plans/` shows no frozen counter references "hardening" (hits only in unrelated r22/r25/r34 files and the hardening script itself), so nothing post-freeze is load-bearing for either predicate. Not a rule change; recorded because the claims dir now mixes frozen and non-frozen artifacts.
- **O2 (minor, calibration-relevant) — census receipts are byte-identical to round-34 mutation-registry outputs.** Three R100 pairs (from the range's rename list): `R34MutRegistry/mirror/corpus/evidence/round33/census-after.txt → .ufo/waves/round-35/claims/census-before.txt`; `R34MutRegistry/mut/m2-escaped-pipe/corpus/evidence/round33/census-after.txt → corpus/evidence/round35/census-before.txt`; `R34MutRegistry/mut/m1-column-count/corpus/evidence/round33/census-after.txt → corpus/evidence/round35/census-after.txt`. So the committed round-35 census receipts carry exactly the bytes of round-34's mutated-run census outputs. That is consistent only if the census output is invariant to those two mutations (m1 column-count, m2 escaped-pipe touch SOURCES-style rows, plausibly invisible to a lesson-freshness census). Paths are declared surfaces, and C1's V6 re-runs the census live at the tip, so the predicate does not lean on these receipts — but a calibration seat wanting the receipts to be honest round-35 artifacts should show census-output invariance under m1/m2 (or a fresh identical run).
- **O3 (cosmetic) — empty placeholder files created by renaming round-34 empty files** (`R35SimplifyTools/{old,new}_{c1,ledger}.{err,exit}` ← empty `.stderr`/`.exit` registry files). Zero-byte sources; no content concern.

## Residual risk & verification gaps

- Git skipped exhaustive rename detection (range too large), so some A/D pairs may be unreported renames; both the A-set and D-set were classified exhaustively regardless, so containment conclusions stand.
- I did not execute `plans/round35_c1_verify.py`, `plans/defect_ledger.py`, or the probe — predicate execution belongs to the C1/C2 seats; my checks are history/scope only.
- Per-commit attribution for `056e192`/`6ac9611`/`dfee6ff` rests on commit subjects plus the exhaustive range-level classification (their paths are all under `.ufo/waves/round-35/` and the corpus bookkeeping files).
- Session note: an earlier scratch dump under `/tmp/k35f-revdiff` vanished mid-session (a sibling reported the same pattern; no `rm` was run by this seat). All counts above were re-derived atomically in single pipelines.

VERDICT: scope-ok
