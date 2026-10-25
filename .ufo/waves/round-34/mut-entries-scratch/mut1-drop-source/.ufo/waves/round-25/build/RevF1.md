# RevF1 (godspeed) — W3ReviewKengaku F1 recheck at lane tip 3f371d2

Axes worked: F1-verdict accuracy at 3f371d2 · parallel cheap evidence · fix-actionability · report calibration. Scope: F1 only (read-only). Installs: none.

## Verdict on F1 — FIXED (verifyable at tip)

- Fixing commit: `e21f9ea` "round-24: post-review fixes" —
  `git log --format='%h %s' 06872d4db..3f371d2 -- corpus/SOURCES.md` → last commit touching the registry is e21f9ea; nothing after it (3f371d2 adds only plans/round-25-claims.md).
- `git show e21f9ea -- corpus/SOURCES.md` recheck-column changes: 19 rows `2027-01-17 (90d)` → `2027-01-17`; S024/S025 `each round` → `90d`. Exactly the 21 E09 rows from the review.
- Recheck column at tip (`awk -F'|'` over `^\| S[0-9]`, 26 rows): 19 × `2027-01-17`, 3 × `90d`, 4 × `on-release` — zero invalid forms remain.
- Old→new logged per contract rule 2: `corpus/lessons/round-24.md:130-137` ("Registry `recheck` cells, in place (contract rule 2), old → new") lists all 21 cells with both values.
- Fleet validator at tip, run by me (not copied from the lesson):
  `TZ=UTC bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok …/corpus/SOURCES.md`, exit 0. Default TZ (−03) → same `ok`, exit 0.
- E08 at tip: 0 (default-TZ run clean; F13's tool-side `epoch()` TZ bug no longer fires on this registry — fleet script advanced past `ff701da`/`6a1dd8c`).

## Fix shape (informational; no fix needed)

If it had been open, the smallest append-only fix would have been the one applied: in-place recheck-cell changes (allowed, rule 2) + old→new in the round lesson — exactly what e21f9ea did. No superseding row was required; no history was rewritten (commit is a normal child of `dc0e594`).

## Residual risk / gaps

- I verified exit 0 with the fleet script as it exists 2026-10-20 (`6a1dd8c` lineage), not the W3-era script binary; E09 acceptance rules are contract-derived and unchanged (`scripts/sources-census.sh:134` selftest still pins E09-bad-recheck), so the verdict holds.
- S024/S025 `each round` → `90d` is a semantic choice (re-check own-work logs every 90 days); contract-valid, not re-adjudicated here.
- F2–F5 (quote locations, S023 reason, overstated verdict) were fixed in the same commit per the lesson's §Corrections; out of my assigned scope, not re-verified.
- `corpus/SOURCES.md` rows at tip = 26 (25 + new S026), consistent with the review's "new row S026" note.

VERDICT: F1 fixed at tip 3f371d2 by commit e21f9ea (21 recheck cells corrected in place, old→new logged in corpus/lessons/round-24.md:130-137, fleet validator exits 0 in both TZ modes); no open remainder, no fix to append.
