# Round 27 mistake candidates — RevengeMistakeMine

Axes: calibration (source-provenance and verdict-record accuracy); novelty unaffected. Read-only review; no installs.

## Ranked candidates

### 1. S038 cited but left queued and unused in the source registry — strongest; recommend new M55

- **Class:** reference-drift.
- **Evidence:** `corpus/knowledge/attribution-interval-calibration.md:144-145` cites S038 and uses its 60%-coverage warning in the admitted entry. `corpus/SOURCES.md:60` still marks S038 `queued` with `used-by` `—`. Git evidence: `git log --oneline -S 'S038 (Reiczigel et al. 2010, Introduction)' -- corpus/knowledge/attribution-interval-calibration.md` → `8239a56 round-25: falsify-wave revision...`; `git show 8239a56:corpus/SOURCES.md` has S038 `queued` / `—`. The same row's search-log note at `corpus/SOURCES.md:90` says it was not cited by any entry, now contradicted by the admitted entry.
- **Captured-by:** none for status/used-by consistency. Q2 (`corpus/QUALITY.md:24-30`) enforces tier/scope, not registry status or use. Round-27 P4e freezes only S043–S048 (`plans/round-27-claims.md:119-120`), so S038 is out of that check.
- **Red command and observed result:** `cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && grep -q 'S038 (Reiczigel' corpus/knowledge/attribution-interval-calibration.md && awk -F'|' '$2 ~ /S038/ {gsub(/[[:space:]]/, "", $9); gsub(/^[[:space:]]+|[[:space:]]+$/, "", $12); print "S038 status=[" $9 "] used-by=[" $12 "]"; if ($9 != "mined" || $12 != "corpus/knowledge/attribution-interval-calibration.md") {print "RED: cited source registry does not record this use"; exit 1}}' corpus/SOURCES.md` → `S038 status=[queued] used-by=[—]`; `RED: cited source registry does not record this use`; exit 1. Separately, `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` reports `kengaku ok` (W04 warnings only), exit 0.
- **Fix:** record the S038 old→new registry change (status `mined`, `used-by=corpus/knowledge/attribution-interval-calibration.md`) and add a registry/citation consistency check; red above must become green after the correction. This is a registry bookkeeping finding; it does not invalidate the source's scientific claim.

### 2. Round-24 lesson reverses the outside admit verdict — strong historical evidence, later corrected

- **Class:** DISC (verdict transcription).
- **Evidence:** `corpus/lessons/round-24.md:120` says the `llm-judge-calibration.md` admit was `disagree (partial)`. The cited verifier says `agree (admit)` at `.ufo/waves/kaika-w3/kengaku-review.md:95`; the outside spot-check independently says `agree` at `corpus/lessons/round-24-verifier-spotcheck.md:12`. The lane later acknowledges the misstatement in `round-24.md:162-167` (CorrF5). Red check: `cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && if grep -q 'Spot-check, admit — .*llm-judge-calibration.md.*disagree (partial)' corpus/lessons/round-24.md && grep -q '\\*\\*agree (admit)\\*\\*' /home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kengaku-review.md; then echo 'RED: round-24 lesson says disagree (partial); cited verifier says agree (admit)'; exit 1; fi` → mismatch message, exit 1.
- **Captured-by:** CorrF5 manual erratum, but no criterion/check; not among M01–M54. The original text is superseded by the appended correction, so this ranks below the live S038 registry drift.
- **Fix:** compare each recorded outside verdict against the referenced verifier row before publishing; the red check above should fail on the uncorrected claim.

## Confidence / scope

Candidate 1 is a high-confidence observable registry inconsistency; significance is limited to provenance bookkeeping, not the truth of the cited result. Candidate 2 is a high-confidence historical transcription error and was manually corrected. No source or lane files were changed; only this report is written.

VERDICT: S038's cited-but-queued registry state is the best uncaptured round-24–26 mistake; CorrF5 documents a second, already-corrected verdict-transcription miss. Installs: none.