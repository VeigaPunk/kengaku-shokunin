# Chousa overlap scan — round 26

Axes: novelty (owned here; mapped to coverage/constructs) and calibration (no change proposed).

## Evidence
- `plans/round-26-claims.md:92-99,160-164`: C1's +1 requires a before-state, in-repo instrument, and prior-art verdict after a search across papers **and tooling registries (PyPI/GitHub)**; SOURCES rows require opening, URL/access date/≤25-word quote in `corpus/evidence/round26-sources/gate.md`.
- `corpus/QUALITY.md:7-8` and `corpus/SOURCES.md:11-17`: QUALITY owns Kengaku admission; SOURCES owns Kengaku's scoped A/B/C tiers and registry; the research method stays Chousa's. Each source row is only made after opening; evidence file retains the URL, access date, quote; tier is scope-specific.
- `corpus/QUALITY.md:24-33,61-78,97-104`: Q2 requires A/B support per claim (C is not sole support); Q3 caps anchored quotes at 25 words; Q8 retains rejected sources with reason and flip condition; Q9 requires rejection evidence about the same property; Q10 requires independent re-opening of citations/locations/numbers; Q13 requires cited second-seat reports to exist in the admitting commit, named by path.
- `chousa-shokunin/SKILL.md:17`: for “Research a question,” declare the question and frame it before searching; do not begin from a search box without a question. `SKILL.md:25-35` cautions that its hierarchy is Chousa's own construction and places learned source records in SOURCES while admission remains in QUALITY.
- Round-cache `build/CritNoveltyPriorArt.md:7-18,22-24` asserts prior art was opened in CheckList, JudgeSense, Judge-LS, and Probatio; it recommends holding novelty at 7 while retaining the lane-specific observable. **Evidence-state discrepancy:** the live `corpus/evidence/round26-sources/` directory is empty (directory listing), and `corpus/SOURCES.md:63-93` has S042 and round-25 search-log entries but no round-26 source rows/log. This does not prove the claimed openings did not happen; it means they are not yet evidenced as Kengaku SOURCES curation.

## One bounded move
Add the C1 search record to the designated Kengaku evidence/log surface with a declared question, separate paper and registry coverage, identified/screened/included/rejected/unopenable counts, and a stop rationale. Cite Chousa `SKILL.md:17` only for the question-first research-record rule; do not copy Chousa's gate, source taxonomy, or claim-verification method. Admit opened sources using Kengaku's own SOURCES fields and QUALITY rules, and keep a rejected lead plus flip condition. Before the knowledge entry is admitted, apply Q10/Q13 to its actual cited sources and returned report paths.

This sharpens novelty evidence by separating the already-published *metamorphic/invariance method* from C1's narrower empirical application to this lane's committed grader/population. It supports an honest held-at-7 decision rather than an unsupported +1; it does not change calibration or assert a new construct after registration. The cached critique and empty canonical source record remain an explicit unresolved discrepancy until the sources are actually opened and recorded.

Verification: inspected the round-26 pre-registration, Kengaku QUALITY/SOURCES, Chousa SKILL/PROVINCE, round-26 build cache and current evidence directory. No build/test/format check assigned or run. Installs: none.

VERDICT: Keep novelty at 7 on current prior-art evidence; finish the Kengaku source log and Q10/Q13 evidence before admission, citing Chousa SKILL.md:17 only for question-first framing.