# ReviewC1 — R97-C1 case semantics and sandbox fidelity (round 97)

Scope: C1 coverage claim only — captured grader, hidden graph, solve.sh, tests/test.sh, the 18
variants, the modelled environment vs the actual pin scope, and the frozen predicate at T.
Reviewer: ReviewC1 (leaf). No production edits; lane read-only; scratch
`/fast/scratch/hyaku/kengaku-r97/ReviewC1` removed after receipts were copied.

## Verdict

**R97-C1: claims MET.** The frozen predicate reproduces independently at T, every gap claim
survives attack, and no defect found flips any frozen vector, the TARGET line, or the C landing.
Findings below are fidelity notes, none rising to a kill-rule trigger.

## Evidence (all receipts under `.ufo/waves/round-97/w1/ReviewC1/`)

- `replay.txt` — `python3 plans/round97_c1_replay.py --lane . --rev T --work <scratch>/rerun
  --grader-venv <scratch>/G` from the lane root: `LEGS L1=pass … L9=pass`, `TARGET executed_rows=41
  member=sparql-university cells=file-artifact:32 set_contains_base=1 located=1 executed=1 cases=18
  legs=72 mismatches=0 defects=0`, `PREDICATE R97-C1 pass`, rc 0 — byte-equal to the frozen
  predicate text.
- `probe-rerun.txt` — direct probe run, rc 0, mismatches 0, all 18 `observed == predicted`.
  Diff vs the committed `corpus/evidence/round97/sparql-probe.txt`: **only** `LANE_TIP`
  (8d9d2713 freeze vs f1083da6 T). Expected: the receipt was stamped at F, HEAD moved to T, and L3
  checks F ancestor-of T (passes). All CASE/DETAIL lines and stamps identical.
- Venv staged per contract: `uv venv -p 3.13` + `rdflib==7.1.4 pytest==8.4.1` → CPython 3.13.16,
  pyparsing 3.3.3 — identical to the receipt's GRADER_SIDE/GRADER_UNPINNED stamps. bwrap 0.13.1,
  userns 122865, uv 0.13.0 (host; no new tools installed).
- `gap-analysis.txt` (+ `gap-analysis.py`) — independent rdflib 7.1.4 execution of the solve query
  and every attacked transform against the hidden graph, outside the probe.
- Working tree at review start: HEAD = T f1083da6; all 10 frozen-instrument sha256 match the
  freeze table; F..T diff is exactly {SKILL.md, plans/grader-population-ledger.json,
  corpus/SOURCES.md, corpus/evidence/round97/sparql-probe.txt}; the three candidate files hash
  exactly to the candidate-bytes table.

## Findings by severity

**1. LOW — pin scope: the model stages 3 of test.sh's 4 uvx pins.** The captured
`tests/test.sh` runs `uvx -p 3.13 -w pytest==8.4.1 -w rdflib==7.1.4 -w pytest-json-ctrf==0.3.5
pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA`. The claim's parenthetical
"(python 3.13, rdflib 7.1.4, pytest 8.4.1)" and the probe (`GRADER_WANT`, GRADER_SIDE stamps)
model only three pins; `pytest-json-ctrf==0.3.5` is not staged and the reward leg drops
`--ctrf`, `-rA` and the plugin. Materiality: pytest-json-ctrf is reporting-only, so reward rc
equivalence holds for every modeled case (18/18 reproduced). Residual risk: if the real image's
plugin failed to import, real pytest would exit nonzero → real reward 0 where the model says 1;
nothing stamps the plugin version, so the receipts cannot rule this out. Cosmetic-to-low; no
vector flips.

**2. NOTE — current-date caveat on C06 is real but benign and bounded.** C06 replaces both
`2025-08-16` literals with `NOW()`. I ran the now-date query with fixed dates 2025-08-16,
2026-11-06, 2027-01-01, 2030-06-01, 2100-01-01: all return exactly the reference set. The hidden
graph's enrollment dates are all 2024-01 and its graduation dates all ≤ 2026-06-12, so any run
date ≥ ~2026-06-13 yields the same counts (Math201 current = 4 ≤ 10 keeps Dubois out; CS_NTUA 12,
NKUA ≥ 11, Berkeley 11 keep the four in). The only flip window is a clock before ~2025-06-02 —
unreachable for future L6 reruns. No unbounded date fragility.

**3. NOTE — C05 (EU criterion) verified beyond the receipt.** Deleting the EU VALUES block
changes nothing: added = removed = ∅. Professor-level check: the role+count filters admit exactly
{Stamou, Zerva, Tympas, Dimakis}; Dimakis's admission runs through Robotics_UPM (ES ∈ EU);
every excluded professor is excluded by count (Dubois 6, Smith 7, Mueller 0 current students) or
role (Voulodimos assistant), not by the EU filter. "Never decides any professor of the hidden
graph" holds.

**4. NOTE — C09 (per-department) verified.** The instruction-faithful subquery
(`probe.PER_DEPARTMENT`) returns the identical 4-row set as the aggregate solve query.
S319's caveat is accurate: solve.sh counts distinct students across ALL of a professor's
departments (cross-product join), not per department; on this graph both give the same set.
DISTINCT aggregates verified working (Dubois 6, Smith 7 excluded; Berkeley 11 admitted), so C15's
F is genuinely duplicate country strings, not an aggregate quirk.

**5. NOTE — the 18 variants do what advertised; transforms cannot silently no-op.** Each
solve-derived variant asserts its anchor occurs exactly `count` times in the solve.sh output
before editing (a changed solve.sh → rc 2 setup defect). Unified diffs of every variant are
minimal and match the declared edit (e.g. no-eu-filter removes exactly the 5-line VALUES block;
ask-query removes GROUP BY/HAVING and swaps the SELECT line). The 18 `app` kinds are unique and
1:1 with the case table; L4 pins the table bytes to the freeze sha; L8 pins the probe bytes.

**6. NOTE — reward leg is real pytest; legs are honest.** The in-sandbox harness runs
`sys.executable -I -B -m pytest -q -p no:cacheprovider /tests/test_outputs.py` and maps rc to the
reward bit — no derived bit. Legs 1–3 call the captured module's three test functions in file
order (definition order matches), catching AssertionError/other; no assertion is reimplemented.
The grader provably reads its own graph: `DATA_PATH = /tests/university_graph_test.ttl` (hidden
graph bound read-only at /tests; agent graph staged at /app; Dockerfile copies only the agent
graph). C17 verified both directions: solve query on the agent graph yields {Orfeas Menis, Pepe
Attanasio, Aristotle Tympas} — the hidden graph replaces two of the three names.
Row-count details confirmed: C11 8 rows/4 distinct passes the set comparison; C12 extra column
(vars professorName+countries+n) passes; C13 semicolon → string mismatch F; C16/C18
AttributeError via ResultRow attribute lookup.

**7. NOTE — population and C landing exact.** Ledger at T: 88 members, executed 41
(BASE 40), file-artifact executed 32 (BASE 31); member `sparql-university` unexecuted at BASE →
executed round 97 with receipt/subject=tb2-header/verdict=cases; executed member set ⊇ BASE set ∪
{member}, no removals. C lands exactly the candidate bytes (sha256-verified) plus the named
receipt; SKILL.md delta = 44 kind cells (C2's), the file-artifact cell 31→32 of 76 with the
round-97 note, the two probe rows (typed `probe`, self-test cell honestly "none — no
self-invocation mode"), the gate-census row and the C2 paragraph.

## Residual risk

- The pytest-json-ctrf omission (finding 1): theoretical only; no observed divergence.
- Sandbox fidelity is deliberately narrower than the task image (no apt/curl/uv install, no
  /logs writer, no `-rA`); all modeled-as-rc and disclosed in the probe docstring and S323/S324
  flip conditions. The prebuilt image `alexgshaw/sparql-university:20251031` is never pulled —
  accepted risk recorded in S324 with its flip.
- HOST_BASH/HOST_USERNS stamps are informational; L9 binds them to the measuring host only.
  GRADER_UNPINNED is stamped and uncompared (round-96 W-2) — my rerun resolved identical
  3.13.16/3.3.3 anyway.

## Verification gaps

- I did not pull or run the prebuilt task image; verifier-side equivalence rests on the captured
  test.sh bytes and the pinned venv (per the claim's own model).
- I did not re-run the P2 controls (positive/forgery/separability) — out of my C1 scope; the
  frozen controls receipts at e40fd0c2 cover them.
- pytest-json-ctrf's behavior in the real image is unobserved (finding 1).

Trailer: `.ufo/waves/round-97/w1/ReviewC1.md`
