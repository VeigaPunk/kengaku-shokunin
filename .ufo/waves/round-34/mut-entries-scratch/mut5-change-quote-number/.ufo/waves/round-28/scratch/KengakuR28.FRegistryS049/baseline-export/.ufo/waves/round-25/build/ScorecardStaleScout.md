# ScorecardStaleScout — SCORECARD present-tense claims false at base 6180e4f

Seat read-only. Base `6180e4f`; `git diff 6180e4f 3f371d2 -- SCORECARD.md` is empty, so the line numbers
below are both base and HEAD. Each finding re-derived by command; history-labelled sections excluded.

## Findings
**F1 `SCORECARD.md:557`** — Capabilities `sources-registry`: "rows 25 … `A=24 C=1` … `mined=18 queued=5 rejected=2`".
Observed: rows **26**, tiers **A=24 C=2**, statuses **mined=18 queued=5 rejected=3**; malformed 0 and the
dup/enum/mined-used-by checks are empty (those pass).
Commands: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `26`;
`awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md` → `A=24 C=2`;
same with `s=$9` → `mined=18 queued=5 rejected=3`.
Cause: `S026` (tier C, status `rejected`, "supersedes S023") added by `e21f9ea` after
`corpus/evidence/round24-sources/gate.md`'s final census, which still prints 25 / C=1 / rejected=2.

**F2 `SCORECARD.md:307`** — "All 149 checks recompute stored-vs-derived from committed bytes".
Observed: `python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS`, exit 0.
The D14 errata at `:618` supersedes the number **but anchors it at `SCORECARD.md:305`**; at base `:305`
reads "evidence, not a ruling." and the 149-checks line is `:307` (`grep -n "149 checks"` → `307:`, `618:`).
The correction's own pointer does not resolve to the claim.

**F3 `SCORECARD.md:14`** — "`../MISSION.md:14` assigns it" (novelty).
Observed: `awk 'NR==14' MISSION.md` → "to `SUBSTRATE_CMD` and the host/operator's global model routing.";
the kengaku axes line is `MISSION.md:24` (`axes: "novelty + calibration (LLM eval/research)"`).
Companion clause holds: `grep -n novelty ../AXES.md` → 0 hits, exit 1.

**F4 `SCORECARD.md:303`** — `"kama mint rests partly on this lane's r4 evidence"` … "Quoted from `../ROADMAP.md`".
Observed: `grep -n "rests partly" ROADMAP.md` → 0 hits; the phrase is absent. The substance is at
`ROADMAP.md:90-91` ("two independent endpoint-drift discoveries: kagi round-3 + kengaku round-4 reports"),
mint pending at `:93`. A paraphrase is presented as a quote.

**F5 `SCORECARD.md:564`** — "The lane's saturation line + stagnation window N are to be declared by the lane on its next round … not asserted by this conformance change."
Observed: the same `## Saturation` section at `:566` already carries "Round 24 declaration — saturation
line: 8 … stagnation window N: 4 rounds". Pending-obligation sentence self-contradicted (low severity).

## Pass (same method)
- `:555` grader tokens/exit 0 re-derive; `:556` freeze-check → `FREEZE-CHECK: reads=1 block_sha=1b2d6a01bfa431ec pinned=1b2d6a01bfa431ec stable=True -> OK`, exit 0 (row omits only the `reads=1` prefix).
- `:560`: `corpus/evidence/round24-census/after.txt` exists with `HEAD 94da19e` and all three capability
  commands; `base-99cf615.txt` exists.
- Intro availability claim still true: all 8 receipt paths ABSENT (`test -e` loop), incl. llm-wiki and
  `~/archive/bench-arena`.
- "No check touches the endpoint": `grep -c '/proc' grader.py` → 0; http strings are stored literals/comments.

## Excluded (history-scoped; for round-25 C2)
- `:401` (§Round 17): "`corpus/QUALITY.md` is absent" — false; `git ls-tree 6180e4f corpus/QUALITY.md`
  → blob `ca69481e` (added `94da19e`).
- Round-24 field `lessons_unindexed_excl_round24 5 → 0` re-derives **1**: `corpus/lessons/round-24-verifier-spotcheck.md`
  has no README row (added `a42bb40`, after the `94da19e` receipt); `sh plans/round24_census.sh` → `C1.lessons_unindexed_excl_round24 1`.
- Post-base: `:626-636` §Planned (round 25) labels C1 = calibration spot-check, C2 = novelty S011; prereg
  `plans/round-25-claims.md` (3f371d2) labels C1 = novelty intervals, C2 = calibration `state_check.py`,
  no spot-check claim.

Installs: none (coreutils/awk/python3 stdlib only).

VERDICT: FIVE present-tense SCORECARD claims are false at base 6180e4f — Capabilities SOURCES counts (26 / A=24 C=2 / rejected=3), the 149-check total (733) plus its mis-anchored D14 erratum, the `MISSION.md:14` anchor (now :24), a ROADMAP quote absent from ROADMAP.md, and a stale saturation pending-obligation sentence; the other re-run capability pointers reproduce.
