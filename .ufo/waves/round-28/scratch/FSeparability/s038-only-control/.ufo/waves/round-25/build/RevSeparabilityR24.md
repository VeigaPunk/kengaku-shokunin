# RevSeparabilityR24 — r24 C1/C2 capability_rows breach (verified, read-only)

## 1. Breach confirmed in the r24 design texts
- plans/round-24-claims.md:51 (C1 section): "Capability row `sources-registry` enters only if
  every contract census command runs clean on the landed file" — C1 declares the row's entry.
- plans/round-24-claims.md:64 (C2 section): "…and enters demonstrated capabilities"; :73
  `| C2.capability_rows | 0 | ≥1 |` — C2 counts the same rows. The §Separability promise
  (:80-87 "Neither claim's counts change when the other's files are reverted") is internally
  inconsistent with :73 from prereg time.
- plans/round24_census.sh:64 counts `C2.capability_rows` from SCORECARD `## Capabilities`;
  :68 closes defect D11 ("capabilities table empty") off the same count → a C1-created
  landing feeds C2's headline `scorecard_state_defects_open 6/6 → 0/6` (:124-126).
- Amendment 1.4 (:115-119) fixed only the lessons-file leak (round-24.md); Amendment 7
  (:131-134) made two of three rows claim-neutral (`grader.py`, `attrib_probe.py` predate
  r24), but `sources-registry` stays C1-created (entry-gate = C1's SOURCES.md census) while
  counted under C2.
- SCORECARD.md:551-560: three rows entered "by demonstration in round 24"; :557
  `sources-registry` evidence cites `corpus/SOURCES.md` + `corpus/evidence/round24-sources/gate.md`
  — both C1 artifacts — inside C2's counted table.
- Strict numeric revert test passes today (copy of landed tree minus `corpus/SOURCES.md` →
  `C2.capability_rows 3`, defects `0/6` unchanged; `C1.sources_rows absent`): the two
  claim-neutral rows carry the ≥1. The breach is credit, not count movement — a C1-created
  row counted as C2's state repair. Exactly the kaika W3 finding.

## 2. Reproduction (all offline, scratch in /tmp)
- Before: `corpus/evidence/round24-census/base-99cf615.txt:21` → `C2.capability_rows 0`;
  re-run v2 script on `git archive 99cf615` tree → `C2.capability_rows 0`, defects `6/6`.
- After: `corpus/evidence/round24-census/after.txt:26` → `3`; live tree (HEAD 3f371d2) →
  `C2.capability_rows 3`, `C2.scorecard_state_defects_open 0/6`.
- Presence-based proof: same copy with `grader.py` moved aside → still `capability_rows 3`,
  defects `0/6`. No check ties a counted row to a passing demonstration (AXES.md:62-64 prose
  only, unenforced).

## 3. Does any QUALITY/SKILL rule now prevent it? — No.
- corpus/QUALITY.md:82-95 (§Round-closure criteria R1–R10, landed r24): corrections, four
  artifacts, FAIL-logging, absent surfaces, errata, non-author, freeze tagging, lowest-axis
  header, coverage pre-flight, census anchoring — no separability/attribution criterion.
- SKILL.md: no claim-counting or separability rule (only unrelated "runner/grader …
  separable", :352-355).
- Fleet prose exists but has no mechanical check: ../AXES.md:30-32 "Claims must be **causally
  separable** … and name **distinct axes**"; ../AXES.md:62-64 rows enter "only through a
  round that demonstrates the capability running". r24 passed the numeric reading and still
  leaked credit.
- Adjudicated, not resolved: kaika W3 recommended REJECT —
  /home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kengaku-critic.md:10 "the preregistered
  separability claim is false: C1 requires the `sources-registry` capability row … while C2's
  `capability_rows` measure counts the same SCORECARD table"; :16. Orchestrator admitted with
  the AXES.md:15 calibration framing ("SHONEN.md/SCORECARD entries match observed repo
  state") and "critic dissent recorded" (corpus/lessons/round-24-verifier-spotcheck.md;
  LOG.md:259).
- r25 avoids recurrence by design only: P2 frozen at base so "C1's new SCORECARD rows are
  outside P2" (plans/round-25-claims.md:94-96) — a workaround for this round, not a durable
  QUALITY/SKILL rule.

## 4. Proposed closure criterion (add to corpus/QUALITY.md §Round-closure criteria as R11)
- **R11 — one artifact, one claim; evidence re-runs at close.** A census key counted under
  claim C measures only artifacts whose creation claim C's own section declares; a landing
  named as an outcome in two claim sections counts once, under the section that defines its
  entry-gate; and every capability row's evidence command re-runs clean in the round it
  enters — presence in a table is not a demonstration.
- Mechanical check A (attribution), per round N (verified discriminative on r24):
  `awk '/^## /{sec=$2} tolower($0) ~ /capabilit/ && sec ~ /^C[0-9]/ {print sec}' plans/round-24-claims.md | sort -u | wc -l`
  → prints `2` (C1 :19,:51; C2 :64,:73) — fires. Rule: result must be ≤1.
- Mechanical check B (live evidence): census v3 gains `C2.capability_rows_verified n/m` —
  for each `## Capabilities` row, run its evidence-cell command offline and require the row's
  verdict token (`PASS`/`OK`/census-clean) in the output; a row that fails or cannot run does
  not count toward `C2.capability_rows` or D11. r25's P2a (plans/state_check.py spec,
  round-25-claims.md:37-39) already implements this half for the 3 landed rows; R11
  generalizes it per round and adds the attribution half.

VERDICT: r24 breach confirmed — C1-created `sources-registry` row counted by C2's capability_rows/D11; no QUALITY/SKILL rule prevents recurrence (AXES.md prose only, r25 population-freeze is a workaround) — R11 proposed above with two mechanical checks. No tool installs (sh/awk only).
