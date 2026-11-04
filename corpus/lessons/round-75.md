# Round 75 — kengaku (2026-11-04 UTC)

Base `4c4249a26a01aeb081915755076f74a7d6c88923` (round-74 verifier spot-check).
R75-C1 targets coverage: a corpus index-parity gate over three disk-enumerated universes, plus the
repair of 59 drifted index surfaces. R75-C2 targets calibration: attributed mutant kills, a measured
null arm, derived tallies and revision-stamped receipts — the R74-D1/D4 classes.

## Gate

- **S251 admitted for `git rev-parse --verify` revision acceptance.** URL opened live by L1
  `KengakuR75` this round: `https://git-scm.com/docs/git-rev-parse`. Access date 2026-11-04 UTC.
  Document title `Git - git-rev-parse Documentation`. Capture
  `corpus/evidence/round75/sources/git-rev-parse.html`, HTTP 200, 122459 bytes, sha256
  `00e3b1aaf8ae9df59a7a6bb8224e19e825c628b7a0cd69a4f03aeda79c2be587`. Located anchor quote,
  capture line 2720, 18 words: **“Verify that exactly one parameter is provided, and that it can be
  turned into a raw 20-byte SHA-1”**. Kind docs, tier A for revision-name resolution and `--verify`
  acceptance. Registry change: absent → S251 `mined`, recheck `on-release`, used-by
  `corpus/lessons/round-75.md, plans/round-75-claims.md`.
- **Reject candidate:** “a 40-hex string in a receipt proves the receipt measured that revision”.
  The same page's `--verify` text establishes resolution of an object id, not that the named tree
  produced the printed numbers; ancestry is a different command (`git merge-base --is-ancestor`)
  and a hash can name a non-commit object. Flip: stamp the receipt with the revision *and* the
  worktree state, produce it from a clean clone at that revision, and keep the `WORKTREE` line as
  the part `--verify` does not certify.
- **Reject candidate:** “presence of a flag string in a script body proves `argparse` acceptance”
  (round-74's own reject, S250). Round 75 implements the flip rather than only recording it:
  `plans/round75_c2_registry_audit.py` refuses a flag that appears as a string literal when the
  script declares its CLI through `add_argument` (`:entry:flag-not-declared:`), and reports
  `TEXT-FALLBACK n=` for scripts with no `add_argument` call where only text presence is available.
- Knowledge entries: none admitted this round. **Four** held candidates stay held —
  `instrument-registry-derivation.md` (round 73), `registry-argv-and-flag-audit.md` (round 74),
  `tb2-hf-model-inference-offline.md` and `tb2-hf-model-inference-provenance.md` (rounds 71–72) —
  and every one now carries a README index row marked `admission: hold` (the two older rows lacked
  the marker until this round, per seat `EntryFalsifyR75`).
  `registry-argv-and-flag-audit.md` additionally **fails Q1 placement**: it opens with YAML, so
  `source:` is at line 16, `verified-at:` at line 8 and `recheck: on-release` at line 9 — a triple
  that names no re-check action. That is a held-entry defect for the next admission attempt, not
  something an index row can repair.
- Assimilation: none. No staged `merge/kengaku/` row was admitted; open L0 `kengaku | round-54`
  carried.

## Mistakes

| id / class | evidence pointer | captured-by | fix / disposition |
|---|---|---|---|
| M75-1 order — S251's `used-by` named `corpus/lessons/round-75.md` before that file existed | `sources-census.sh validate` → `E11 S251 missing used-by corpus/lessons/round-75.md` | the census's own used-by leg | Lesson file created in the same commit as the row; census re-run green before the round closes. |
| M75-2 instrument — the C1 selftest's clean arm failed because `drop_row=""` is a substring of every row, so every row was dropped | first `--selftest` run: `SELFTEST FAIL clean rc=1 want=0` | the selftest's own clean arm | `keep = [r for r in rows if not drop_row or drop_row not in r]`; clean arm green. |
| M75-3 control — the first fake-completion control compared 6 rows to 4 *files* and printed `equal=False`, so it asserted nothing | `--control-rowshuffle` first run: `NAIVE rows=6 files=4 equal=False`, `PREDICATE R75-C1-control fail` | the control's own pass condition | Count surfaces (files + evidence dirs = 6); control now prints `equal=True` while the gate still prints four `MISSING*` defects. |
| M75-4 fixture — the first off-target mutant was labelled `:self-test:empty` and its fixture produced exactly that defect, so it was a true kill, not an off-target kill | `mutate()` first run: `MUTANTS total=10 killed=8 … wrong_id=1` and `SELFTEST FAIL attribution` | the selftest's off-target arm | The off-target arm re-labels the *M3 fixture bytes* as if the mutation under test were an unhooked entry flag; `X-off-target` now yields `matched=False`. |
| M75-5 provenance — round 74's receipts carried no measured revision and one printed a tree that did not exist as a commit (R74-D1) | `corpus/lessons/round-74-verifier-spotcheck.md` §2 R74-D1 | the outside closure | Both round-75 instruments print `LANE_TIP`/`WORKTREE`; every round-75 receipt is produced from a clean clone at the freeze revision and `--check-stamps` refuses an unstamped, unresolvable or non-ancestor stamp. |
| M75-6 metric — round 74's mutant matrix counted a kill on *any* defect and printed literal `invalid=0 null_detected=1` with no null arm (R74-D4) | `plans/round74_c2_registry_audit.py:377-411` (r74 code) | the outside closure | Attributed kills + a measured null arm + derived tallies; `--control-attribute` shows round 74 scoring 10/10 where the attributed metric scores 9/10 with `wrong_id=1` on the same bytes. |
| M75-7 self-report — round 74's lesson still said the C1 Before receipt shows `MISSING 5` when it shows `MISSING 0` (R74-D2) | `corpus/lessons/round-74.md:51` vs `corpus/evidence/round74/c1-before.txt` | the outside closure | Correction appended in place as a dated line naming the receipt's actual value; the round-74 text is not rewritten. |
| M75-8 citation — the first README row for `tb2-torch-tensor-parallel-offline.md` cited `S235–S237`, which are the round-65/66 SQLite and kv-store rows, not this entry's source | seat `KnowledgeRowsR75` report; entry's own `source:` line cites S183, and `corpus/SOURCES.md` S236/S237 are SQLite and kv-store-grpc | the scribe seat read the entry instead of the neighbouring round's block | Row corrected to `S183 (tests/test_outputs.py:18–25,43–211)`; the same seat's Q1 finding on `registry-argv-and-flag-audit.md` (YAML front matter puts the triad outside the first three lines, and `recheck: on-release` names no action) is recorded here as a held-entry defect for the next admission attempt. |
| M75-9 counter-under-enforcement — `--check-stamps` printed `PREDICATE R75-C2 pass` with `LANE_TIP unknown` and `STAMPS files=0`, a counter narrower than its own frozen sentence | seat `C2MutantReplayR75` report (clone with `git clone --revision`, no `master` ref, evidence dir absent at A1) | the frozen sentence's `LANE_TIP <40-hex>` and `files=K stamped=K` (K>0) legs, which the counter did not implement | `check_stamps` now defects on `TIPTAG:unresolved` and `STAMPS:empty-dir`; Amendment A2 records it; the null arm was also rewritten to a whitespace-only delta after the same seat showed the old arm renamed a row. |
| M75-10 false-green — R75-C1 matched raw README bytes, so an HTML comment (or a code fence) listing every filename satisfied all three universes while nothing rendered as an index; a `.md`-named directory also counted as a knowledge file | seat `ClaimsCriticR75` counterexample (rc 0 with `missing=0` on a comment-only README) and `C1GateAuditR75` HIGH/MEDIUM | the frozen sentence's word *indexed*, which the counter read as *mentioned* | Counter strips HTML comments and fences, splits cells on unescaped pipes, requires a non-empty description cell per row, and enumerates regular files only; both counterexamples now print `PREDICATE R75-C1 fail`. |
| M75-11 false-green — R75-C2 treated `add_argument(..., help='--strict')` as declaring `--strict`, so a rejected option passed every counter | seat `ClaimsCriticR75`: `python3 tool_doc.py --strict` exits 2 (`unrecognized arguments`) while the audit printed `FLAGS ok n=0` and `PREDICATE R75-C2 pass` | S250's reject-flip, which the counter had implemented against *all* string constants instead of positional arguments | Only positional `add_argument` arguments register an option; the fixture now prints `DEFECT tool-doc:entry:flag-not-declared:--strict`. |
