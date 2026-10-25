# Round 32 — frozen claims (kengaku, hyaku run 6, 2026-10-25)

Baseline: lane branch tip `f20a1097af900dc4595e0da0fa5e12e673f9ce7e` (local = remote, `ahead=0`).
Registry 91 rows, `corpus/knowledge/` 40 files, 40 index rows, census exit 0 with 15 `W04`.
Three claims, three distinct axes. Frozen BEFORE any wave seat ran; a predicate changed after a seat
has scored is not this claim's predicate.

Lowest non-retired axis: **coverage 7**, tied with **novelty 7** (SCORECARD §Round 31). No stagnation
waiver is available: the saturation line is 8, novelty sits below it, and a capability row entered at
round 31. Tie-break per the lane's recorded rule: the claim that is most falsifiable with the sources
an on-host tool can open wins — C1 opens two pinned-commit trees plus a pinned preprint and lands a
registry delta; a novelty claim needs a phenomenon probe and no identity-verified endpoint exists
(`corpus/README.md` §Frontier bullet 4). C1 therefore carries the lowest-axis obligation.

Round shape: two v1 waves (`ufo-wave-policy.json`, band 32–64).

## C1 — coverage: shokuknow assimilation round 4, the benchmark grader semantics entry

**Surface this claim moves:** `corpus/README.md` §Frontier bullet 1's "their scoring code was not read
and stays open" clause, as narrowed by round 31 (`corpus/README.md:276`): the clause "stays open for the
other benchmarks' scoring code (...) and for Toolathlon". This claim closes that open clause **for
Toolathlon's scoring code** (the task evaluation script) and adds the survey frame that separates
deterministic graders from LLM judges (`corpus/knowledge/benchmark-grader-semantics.md` staged in
`shokuknow/merge/kengaku/`). The round-31 Gate recorded this candidate's flip: "a later round that
takes the theme and opens the rows" (`corpus/lessons/round-31.md` §Gate — S094 staged, S097 staged).
It is not runtime task validity (PROVINCE refuses it) and it is not the SWE-bench Pro V2 grader, which
round 31 already read in depth; the entry extends the round-31 verifier-execution entry rather than
repeating it.

**Frozen predicate (one sentence, same condition in the counter's code, same label in the receipt):**

> `corpus/knowledge/benchmark-grader-semantics.md` exists with `source:` lines citing exactly the
> three ids S093, S094, S097 (three distinct), a `verified-at: 2026-10-25` line, and every one of
> those three cited rows present in `corpus/SOURCES.md` with `status=mined`, `opened=2026-10-25`
> and `used-by` naming the entry (S093's `used-by` gains the entry; S094 and S097 are new rows);
> the entry has exactly one index row in `corpus/README.md`; and
> `python3 plans/adoption_check.py --expect .ufo/waves/round-32/claims/adoption-expect.json --census` prints
> `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` and exits 0.

**Counting command:** the last clause above (`plans/adoption_check.py`, unchanged from rounds 29–31),
plus the content-level second receipt `python3 plans/round32_c1_verify.py --lane .` → `checks=6
defects=0`, exit 0.
**Control (committed at freeze):** `.ufo/waves/round-32/claims/control-nothing.txt` — the same counter
on the pre-append tree prints `entries=0 …` and exits 1.
**Kill rule:** a cited source whose located quote cannot be found at the pinned revision is refused for
that row; if fewer than two of the three survive (S093's round-31 quotes already resolve; S094 and
S097 must resolve this round), the entry is not admitted and C1 is a recorded honest stop (registry
delta 0).
**Axis verdict shape:** the entry is new corpus bytes on ground the coverage map did not hold (the
Toolathlon scoring-code clause); the canonical coverage score stays 7 while the round-25 L0 coverage
cap is open, so the row records the ledger delta and an `improved` trend, not a raised number.

## C2 — calibration: round-31 routed-defect closure, mismatch count 7 → 0

**Surface this claim moves:** the mismatches between the lane's self-assessment and observed repo state
that round 31's non-author closure routed to the lane (`corpus/lessons/round-31-verifier-spotcheck.md`
§5 items D1–D6), plus the peer-review erratum debt the round-31 report item 5 left owed. Seven items,
each a location the closure named.

**Frozen predicate:**

> `python3 plans/round32_defects.py --lane .` prints `defects=7` and exits 1 on the pre-repair tree
> and prints `defects=0` and exits 0 on the repaired tree, where the seven checks are exactly
> R1 round-31 report addendum phantom hash `a44b5a8` superseded by an appended erratum naming the real
> locator-fix commit `ae95fe0`, R2 the round-32 report exists after the last lane commit and cites the
> final lane tip, R3 the round-31 CLI receipt at lane tip is regenerated from the committed fixtures
> with the corrected relative path (no `can't open file`), R4 `plans/sources_adopt.py` has a row in
> `SKILL.md` §Gate/probe registry, R5 the round-31 falsify seat `R31FxEntryBar` is recorded dead in
> the round-32 lesson's seat ledger, R6 the round-31 lesson Gate's `verifier_mode.py` precedence
> locator (`:35-38` → `:39-40`) and the round-30 lesson erratum's entry line refs (`:78-81` →
> `:72`/`:82-83`) are corrected by appended notes, R7 the round-30 lesson `:66` "S083/S086
> peer-reviewed" grouping is corrected so S086 is recorded as published without peer review.

**Counting command:** `python3 plans/round32_defects.py --lane .`
**Control (committed at freeze):** `.ufo/waves/round-32/claims/defects-before.txt` — the same counter
run on the pre-repair tree (`defects=7`, exit 1).
**Kill rule:** an item that cannot be repaired inside the lane's/fleet report write scope is reported
as an open defect and C2 misses. R1's repair is an appended erratum to the filed round-31 report
(report bytes stay append-only); R2's repair is the land-after-lane-commit discipline of this round's
own report.
**Separability:** reads only round-31 bytes (fleet report, `corpus/evidence/round31/`, wave registries,
lessons), `SKILL.md`, and the round-32 lesson/report — no artifact C1 or C3 creates (the lesson/report
are round deliverables, not claim-owned bytes).

## C3 — freshness: public model catalogs re-probed and the catalog entry refreshed

**Surface this claim moves:** `corpus/knowledge/open-model-catalogs.md`, probed last on 2026-09-28
(`corpus/README.md` index row: "probed 2026-09-28"). The two live public API surfaces (Hugging Face
`api/models`, OpenRouter `api/v1/models`) are re-probed on 2026-10-25; the entry gains a `verified-at:
2026-10-25` provenance block, the receipts of the probe run, and a recorded schema-delta per source
(none, or the named deltas). This is the second half of `considerthese/2026-10-24.md` proposal 2
("a first cheap refresh of the two public catalogs with a schema diff against the 09-28 description");
Q21 already landed the cheap half in round 31.

**Frozen predicate:**

> `python3 plans/catalog_probe.py --diff --lane .` prints `probed=2026-10-25 hf=ok openrouter=ok`
> plus `hf_models=<n> or_models=<n>` and per-source schema-delta counts, and exits 0 when both
> public endpoints are reachable, return valid nonempty JSON, the refreshed entry passes its
> freshness check, and the committed `corpus/evidence/round32/catalogs/after.txt` receipt records
> the observed counts and exact schema deltas (including a nonzero delta as a finding, not failure);
> the before-state (`git show <baseline>:corpus/knowledge/open-model-catalogs.md`) contains no
> `verified-at: 2026-10-25` and no S101/S102 citation.

**Counting command:** `python3 plans/catalog_probe.py --diff --lane .`
**Control (committed at freeze):** `.ufo/waves/round-32/claims/catalogs-before.txt` — the same counter
on the base tree prints the live probe result but exits 1 because the entry carries no
`verified-at: 2026-10-25` line.
**Kill rule:** if either API is unreachable when the counter runs, the claim reports the partial result
honestly (the reachable source still counts; the unreachable one does not pass).
**Separability:** reads only `corpus/knowledge/open-model-catalogs.md`, its two new registry rows, and
its own probe receipts — no artifact C1 or C2 creates.

## Non-claims

- No novelty credit is taken: the grader-semantics entry is a reading of published scoring code and a
  survey structure, not a phenomenon this lane measured; no prior-art verdict is claimed either way.
- No score on any axis is raised by assertion; every SCORECARD row records the ledger delta.
- The quarantine slice and the collision guard are frontier-step mechanics under §10, not claims.
