Author: kengaku (L1 KengakuR97)

# Round 97 — SPARQL grader replay and truthful registry kind cells

BASE `4992cd0e`; P0 `5b41c1c3`; P1 `b2352135`; P2 `e40fd0c2`; F `8d9d2713`; C=T `f1083da6`.
Frozen predicates: `plans/round-97-claims.md`. Receipts: `.ufo/waves/round-97/L1/c1-tip.txt`, `c2-tip.txt`, `freeze-tip.txt`.

## Gate

Search: pinned TB2 unexecuted members; inspected task-tree API for eight candidates, chose self-contained SPARQL file-artifact grader. Nine sparql-university source files opened on 2026-11-06 at 01:01 -03, all HTTP 200. Six admitted as primary replay inputs/contracts, three rejected as unnecessary or derivative. Stop: one new member with a positive, no-work and mechanism-specific negatives; no general benchmark-quality claim.

| row | URL / access | located quote | decision / reason / flip |
|---|---|---|---|
| S317 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sparql-university/tests/test_outputs.py; 2026-11-06 | `tests/test_outputs.py:79`: assert result_set == reference_set, ( (5 words) | mined, tier A: the results test compares SETS of (name, sorted countries) built from row attributes: duplicate rows (C11), an extra projected column (C12) and a literal VALUES answer with no graph pattern (C10) all pass; a renamed variable raises AttributeError (C16) |
| S318 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sparql-university/tests/university_graph_test.ttl; 2026-11-06 | `tests/university_graph_test.ttl:157`: uni:worksIn uni:Engineering_Berkeley, uni:Robotics_UPM , uni:Physics_ETH . (6 words) | mined, tier A: every professor the EU criterion would exclude is excluded by the >10 rule too, so dropping the EU filter passes (C05); no professor separates per-department from aggregate counting (C09); graduations end 2026-06-12, so a NOW()-dated query passes (C06) |
| S319 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sparql-university/solution/solve.sh; 2026-11-06 | `solution/solve.sh:46`: HAVING(COUNT(DISTINCT ?student) > 10) (4 words) | mined, tier A: run unmodified it writes /app/solution.sparql and all three functions pass (C01); it counts distinct students across ALL of a professor's departments, not per department as the instruction states, and the test graph cannot tell the two apart (C09) |
| S320 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sparql-university/tests/test.sh; 2026-11-06 | `tests/test.sh:21`: -w rdflib==7.1.4 \ (3 words) | mined, tier A: uvx -p 3.13 with pytest 8.4.1 and rdflib 7.1.4 runs only /tests/test_outputs.py and writes reward 1 iff pytest exits 0; the replay's reward leg runs that pytest for real (no derived bit) |
| S321 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sparql-university/instruction.md; 2026-11-06 | `instruction.md:7`: 3. Among all departments they work in, at least one has more than 10 students currently enrolled in any classes taught in that department. (24 words) | mined, tier A: the stated contract is stricter than the graded one: an EU-agnostic query (C05), a NOW()-dated query (C06), duplicate rows (C11), an extra column (C12) and a hardcoded answer (C10) all pass |
| S322 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sparql-university/environment/university_graph.ttl; 2026-11-06 | `environment/university_graph.ttl:113`: uni:hasName "Orfeas Menis" ; (4 words) | mined, tier A: the agent graph names two professors the test graph replaces (Orfeas Menis, Pepe Attanasio), so a query that hardcodes the agent-graph answer fails (C17) while one that hardcodes the test answer passes (C10) |
| S323 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sparql-university/environment/Dockerfile; 2026-11-06 | `environment/Dockerfile:7`: COPY university_graph.ttl /app/ (3 words) | rejected, tier A: REJECTED as an input: ubuntu:24.04 plus the agent graph, no package pins; the replay stages the same /app bytes and never runs agent-side code beyond solve.sh's heredoc; flip: a case whose verdict depends on an agent-side tool |
| S324 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sparql-university/task.toml; 2026-11-06 | `task.toml:29`: docker_image = "alexgshaw/sparql-university:20251031" (3 words) | rejected, tier A: REJECTED as an input: the harness runs a prebuilt image the replay never pulls; the grader side is modelled by a pinned venv; flip: the image pulled and its /app and verifier versions compared to GRADER_SIDE |
| S325 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sparql-university/README.md; 2026-11-06 | `README.md:24`: 3. The query returns the correct set of professors and countries, matching reference results (4 professors expected) (17 words) | rejected, tier B: REJECTED: restates the instruction (S321) and carries no byte the grader or the replay reads; flip: a claim about the README's own statements |

Registry old→new: no existing SOURCES row changed. Added S317–S325: 8 tier A, 1 tier B; 6 mined, 3 rejected. Rows 308→317. Frontier member sparql-university unexecuted→executed; ledger executed 40→41, file-artifact 31→32/76. Source bytes and sha receipts: `.ufo/waves/round-97/L1/capture-sha.txt`; anchor gate `live=0 cells=0` in `L1/anchor-tip.txt`. Census command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`: start and end ok, rc0 (`L1/census-start.txt`, `L1/census-end.txt`).

Assimilation: none; inherited merge/kengaku hold L0 kengaku|round-54. No considerthese proposal adopted; source material was the pinned task itself.

## Round-96 routed defects — disposition

1. Permanent r93/r94/r95 freeze-history harm: retained honestly, no waiver and no closed-table edit. Successors deferred.
2. Seven standing reds: not claimed repaired. The absolute-L7 successors and r79 subject disagreement remain open.
3. Nondeterministic standing battery: its kind is now probe (one of the 44 retyped rows); no claim that its nondeterminism is cured.
4. Round96 self-test-none rows: both retyped probe; self-invocation capability not invented. The new census has eight isolated CLI fixtures with committed expected rc/finding IDs.
5. Merger missing wrong-pass cases: deferred, not folded into SPARQL member coverage. Unpinned-stamp comparison lesson applied to the new SPARQL replay only.
6. Candidate scope: C contains exactly three candidate-byte files plus the named receipt; prefreeze byte hashes and P2 candidate copies retained. Formal pre-push gate not acquired.
7. C2 mutation seat included in this wave, no old lost-seat credit claimed.
8. R95 reward scope, held-out false gates, round92 items and W-4 remain carried.

## Mistakes

| id | class | evidence | captured-by | fix / demonstrated failure |
|---|---|---|---|---|
| M1 | attribution | round96 spot-check routed defects 3–4: gate rows with self-test none; round97 C2 BASE receipt has 44 MISMATCH lines | PROTOCOL Gate standard Self-test | correct only kind cells, no frozen scripts; `c2-do-nothing.txt` fails44, `c2-positive.txt` passes0; no claim to add self-test capability to these tools |
| M2 | vacuous | `L1/dryrun/README.md`: solve sentinel was a str, so staging wrote literal solve instead of running solve.sh; 12 cases failed dry run | positive control, Q74 | distinguish sentinel before literal branch; final C01 passes unchanged solve; CASE/DETAIL observations show altered row sets and projections. Initial failing stdout overwritten, disclosed rather than reconstructed |
| M3 | landing | protocol/skills and Q80 read late in this round; no second agreeing run of each counter at the same revision was committed BEFORE F | Q80 | not retroactively fixable; P2 has one positive per counter, not two. Record conformance miss. Post-freeze reruns cannot backdate compliance |
| M4 | scope | detector measures a lexical selftest spelling, not full fixture quality or branch reachability | PROTOCOL Gate standard / Q68 | claim restricted to the frozen code-spelling population; no assertion that 84 remaining gates satisfy semantic self-test standard; wave attacks retained |

## Wave findings

WAVE-DONE received from Main: all 11 seats settled, no dead seats; `w1-results.json`. Role mix: 3 executor, 2 reviewer, 1 critic, 2 mutation-tester, 1 scout, 1 connector, 1 scribe (5/11 attack roles). Planner held by L1; connector supplied bounded planning data-walk.

| seat / finding | observed verdict or defect | disposition |
|---|---|---|
| ExecC1, ReviewC1 | replay BASE fail/T pass; two identical probe runs; real pytest agrees 18/18 | C1 measured met |
| ExecC2, ReviewC2 | independent AST/CLI audit: all44 demotions true; no false positive/negative in actual population; all44 scripts reject both selftest flags | C2 finite44→0 measured true, not general detector soundness |
| ExecHarm | candidate scope exact, ten frozen hashes match, measured gate rc and designated defect lines unchanged | no new green→red demonstrated in this battery |
| CriticClaims | both target blocks reproduce and no-work fails; notes omitted CTRF reporting pin | bounded verdict retained, not a protocol waiver |
| MutC1 | 19 C1 mutants/controls rejected; extra unearned member passes exit0 with wrong TARGET42; fake bwrap passes only non-frozen invocation | next counter must bind numeric targets and sandbox trust; not repaired |
| MutC2 | nine forged commits emit exact frozen C2 block; 16/18 selftest mutants survive, including deleting load-bearing add_parser regex | detector discrimination falsified; finite correction still true at T; successor required |
| ConnectorOverlap F1/F2 | C2-only prints ROWS169, not frozen171; SKILL candidate hash covers both claims | exact-string separability NOT demonstrated; C2 not admitted by L1 despite measured pass |
| ScoutSources | 9/9 live bytes/quotes agree; anchor-digest defects80→86 (six nested captures unbound); anchor-line live0 | inherited gate is already red, but six additional findings are new debt, not called no-harm universally |
| ScoutSources F2/F3 | NOW mechanism wording stale; S323 rejected input is nevertheless digest-pinned by probe | dated corrections below; immutable source-row text retained |
| ScribeLesson F1 | reconstruction counts13 solve variants, not unretained dryrun's12 errors | dryrun count cannot certify reconstruction; original staging distinction failure is the lesson |

### Dated corrections and admission (2026-11-06)

- S318: NOW() still passes, but at the measured date all dated graduations are past; the surviving undated students preserve the four-person answer. Reference-date counts12/12/12/11 become NOW counts12/12/11/11. The graph's last graduation date alone is not the full explanation.
- S323: rejected as an environment-implementation model, not literally absent from replay inputs: its Dockerfile digest participates in L2/PINS. No image execution is claimed.
- The wrapper also pins pytest-json-ctrf0.3.5. It is not staged; the probe reproduces the test-file reward, not CTRF reporting or arbitrary plugin-import failures. The narrower model is stated in the knowledge entry.
- R97-C1 target is met at T; R97-C2 target is met at T but **not admitted**: the exact frozen row-count block is not causally separable from C1. Q80's missing second committed prefreeze counter runs is an additional conformance defect, not retrospectively cured by the wave. No frozen instrument or predicate is repaired.
- Outside discernment spot-check remains pending closure. Seats dispatched by this lane are still the lane under LEARNING.md; their 9/9 reopening is not an outside spot-check.

### Additional mistakes mined

| id | class | evidence | captured-by | fix / shown able to fail |
|---|---|---|---|---|
| M5 | scope | ConnectorOverlap F1: c2-only row-count169 vs frozen171 | AXES causal separability | report C2 not admitted; successor freeze must declare invariant local populations; counter success is not exact predicate equality |
| M6 | survivor | MutC2 exact-block forgeries and add_parser deletion surviving selftest while making T fail | Q68/Q81 | finite correction retained, gate discrimination not claimed; successor must exercise dispatch forms and exact kind-change population |
| M7 | reference-drift | ScoutSources six new anchor-digest-unbound captures | anchor-digest-check | debt disclosed80→86, not suppressed by anchor-line green; successor resolution must retain nested URL path identity |
