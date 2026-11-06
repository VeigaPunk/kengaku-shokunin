Author: kengaku (L1 KengakuR98)

# Round 98 — regex-chess grader replay and nested-capture provenance bindings

BASE `49a1c4f1`; P0 `5584a6f7`; P1 `350d0e59`; (operator `febd88b9` considerthese); P2 `c71f04e6`;
F `e1a3afd9`; C = T `8e37fc65`; receipts `363fa03c`.
Frozen predicates: `plans/round-98-claims.md`. Receipts: `.ufo/waves/round-98/L1/c1-tip.txt`, `c2-tip.txt`,
`c1-base.txt`, `c2-base.txt`, `freeze-tip.txt`; controls `.ufo/waves/round-98/L1/controls/`.

## Gate

Search: the 40 `unattempted` ledger members; inspected four test files at the pinned commit
(`crack-7z-hash`, `regex-chess`, `mteb-leaderboard`, `bn-fit-modify`) and chose `regex-chess`: a
self-contained python grader whose acceptance rule (per-line membership, count, forgiving fallback,
fixed public positions) carries testable mechanisms; the other three check one literal answer or need
pandas/scipy fits. Eight regex-chess files opened 2026-11-06 08:03 -03 (`.ufo/waves/round-98/L1/capture-time.txt`),
all HTTP 200, captured flat under `corpus/evidence/round98/tb2-regex-chess/` with `SHA256SUMS`.
Five admitted as replay inputs or contract, three rejected. Stop: one new member with a positive, a
no-work control and mechanism-specific negatives; no claim about any submitted solution.

| row | URL / access | located quote | decision / reason / flip |
|---|---|---|---|
| S326 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-chess/tests/test_outputs.py; 2026-11-06 | `tests/test_outputs.py:35`: assert x in python_chess_moves or x.rpartition(" ")[0]+" -" in python_chess_moves, ( (11 words) | mined, tier A: per-line membership plus an equal count (C04 duplicate-for-omission passes); the `rpartition` fallback forgives the last field (C07 invented en-passant passes; C08 castling not forgiven); fixed public games (C09 lookup table passes; C10 one missing entry fails its game only) |
| S327 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-chess/tests/test.sh; 2026-11-06 | `tests/test.sh:21`: -w chess==1.11.2 \ (3 words) | mined, tier A: python 3.13, pytest 8.4.1, chess 1.11.2; reward 1 iff pytest exits 0; the replay's reward leg is pytest's own exit |
| S328 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-chess/solution/solve.sh; 2026-11-06 | `solution/solve.sh:4`: gzip -d > re.json (4 words) | mined, tier A: decodes a 40460-pair re.json; run unmodified it passes all four tests (C01) in about four minutes |
| S329 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-chess/instruction.md; 2026-11-06 | `instruction.md:27`: You can look at the provided check.py to verify if your solution is correct. You will be tested on other positions as well. (23 words) | mined, tier A: the stated contract (a fully correct generator, other positions) is stricter than the graded one: C04, C07 and C09 pass |
| S330 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-chess/environment/Dockerfile; 2026-11-06 | `environment/Dockerfile:5`: RUN pip install chess (4 words) | mined, tier A: python:3.13-slim-bookworm, unpinned chess; solve.sh needs only bash/python/gzip, so the replay runs it with the pinned python 3.13 venv |
| S331 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-chess/environment/check.py; 2026-11-06 | `environment/check.py:98`: def test_morphy_opera_game(self): (2 words) | rejected, tier A: the grader never imports it; it checks a different game than the hidden three; flip: a case whose verdict depends on what the agent could self-check |
| S332 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-chess/task.toml; 2026-11-06 | `task.toml:29`: docker_image = "alexgshaw/regex-chess:20251031" (3 words) | rejected, tier A: prebuilt image never pulled; grader side is a pinned venv; flip: the image pulled and its verifier versions compared to GRADER_SIDE |
| S333 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-chess/README.md; 2026-11-06 | `README.md:33`: Compares generated moves against the `python-chess` library to ensure all legal moves are generated (no more, no fewer) (18 words) | rejected, tier B: derivative of S329 and carries no byte the grader reads; its "no more, no fewer" is exactly what C04 shows the count check does not guarantee; flip: a claim about the README's own statements |

Registry old→new: no existing SOURCES row changed (R98-C2 K5: `rows_changed=0` over its 39 rows; the
C diff of `corpus/SOURCES.md` is insert-only). Added S326–S333: 7 tier A, 1 tier B; 5 mined, 3 rejected.
Rows 317→325. Status/recheck/used-by changes to existing rows: none. Frontier member `regex-chess`
unexecuted→executed; ledger executed 41→42, `file-artifact` 32→33 of 76, `serialization-schema` 7→8 of
10. Census `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`: start rc 0
(`L1/census-start.txt`), end rc 0 (`L1/census-end.txt`). Pre-append scratch validation of the candidate
registry on a `git archive` mirror: rc 0 (`L1/controls/candidate/sources-validate.txt`).

Anchor re-verification (R98-C2): 39 existing rows whose digests named committed nested captures the
frozen gate could not reach are now bound by `corpus/evidence/PROVENANCE.md`; gate findings 86 → 45 at
T (39 population rows plus 2 rows outside the population that the provenance URLs also resolve; no row
present at BASE gained a defect class, K7). The 45 remaining findings are unchanged debt.

Assimilation: none (inherited `merge/kengaku/` hold, L0 `kengaku | round-54`). considerthese: proposal 5
of `considerthese/2026-11-05.md` §1 (operator ruling on the coverage L0 cap) mined into L0
`kengaku | round-98` in the fleet `.ufo/l0-questions.md`; the reflection's claim (coverage 7 every round
since r79 while executed members rose) was re-checked against `SCORECARD.md` round sections 79–97 and the
ledger at T (42 executed). Proposals 1–4 not acted on. `considerthese/2026-11-06.md` (operator commit
`febd88b9`, landed mid-round) not mined this round.

### Dated corrections carried (round-97 spot-check routed defect 4)

- S318 (2026-11-06, unchanged row text): the NOW()-dated query still passes because undated students keep
  the four-person answer; the graph's last graduation date alone is not the explanation.
- S323 (2026-11-06, unchanged row text): rejected as an environment model, yet its digest is pinned by the
  round-97 replay's L2 and is now also bound by `corpus/evidence/PROVENANCE.md` (C2 population).

## Round-97 routed defects — disposition

1. Nested captures unbound (80→86): R98-C2 binds 39 rows including the six round-97 captures (S317–S320,
   S322, S323); gate findings 86→45 at T. New round-98 captures are flat, so C1's eight rows add no finding
   (C1 L10, `new_rows_flagged=0`).
2. Claim-local predicates and Q80: both predicates name only claim-local quantities (C1: member set
   equality and rows added after BASE; C2: a frozen 39-row population and BASE rows only); every counter
   has two committed agreeing prefreeze runs before F (`controls/*-run{1,2}.txt`, P2 `c71f04e6`).
3. MutC2 survivors of the round-97 census: not addressed; the census is not reused or claimed.
4. S318/S323 wording: carried above, rows not rewritten.
5. `.ufo/waves/round-97/w1.ready{,.dispatched}` untracked: left for the orchestrator (not lane-authored).

## Mistakes

| id | class | evidence | captured-by | fix / shown able to fail |
|---|---|---|---|---|
| M1 | verdict-channel | `.ufo/waves/round-98/L1/dryrun/probe-dryrun-1.txt` (every leg `MISSING`: the summary regex required `/tests/test_outputs.py`), `probe-dryrun-2.txt` (C11/C12 `E:assert`, C02 `E:`: pytest's short summary prints rewritten assert text, not an exception type) | P0 mechanism predictions + positive control C01 (Q74) — the probe never reached freeze | verdicts now come from an observe-only `pytest_runtest_makereport` hook (`call.excinfo.typename`) with pytest's own exit as reward; dry run 3 12/12. Able to fail: dry runs 1–2 are the committed failing outputs of the old channel |
| M2 | reference-drift | round-97 spot-check §5.1: six nested captures added anchor-digest findings 80→86; rounds 52 and 92–96 had done the same (39 rows at BASE) | `anchor-digest-check` (it flagged them; the lane routed instead of binding at capture time) | flat captures for new members plus a provenance binding for old ones; able to fail: `controls/c2-do-nothing-run*.txt` `still=39`, `c2-partial-run*.txt` `still=1`, C1 L10 counts rows added after BASE |
| M3 | process | operator commit `febd88b9` (considerthese) landed on `master` between P1 and P2 and the helper rebased P2 onto it | none (expected operator behaviour) | disclosed; it touches only `considerthese/2026-11-06.md`, read by no round-98 instrument (`git show --stat febd88b9`) |
| M4 | scope / side-channel | ReviewC2 F1–F3, ExecC2 §3 (`.ufo/waves/round-98/w1/`): the URL column of `corpus/evidence/PROVENANCE.md` also feeds the gate's `prov_url` fallback, so two rows OUTSIDE the population changed verdict at T (S230 `digest-wrong-capture` → clean; S213 `anchor-unbound` cleared, its `token-outside-anchor` kept) and two clean rows re-bound (S237, S272). Gate findings fell 86 → 45 = 41, not 39; the P2 positive receipts already printed `GATE defects base=86 rev=45` and the claims file declared that line informational without explaining the 2 | none — K7 is addition-only by design and the claims text waved the GATE line off | not repaired in round (frozen). Disclosed in SCORECARD and report; routed to round 99: a three-column provenance table (row, file, sha) or a symmetric outside-population census (removals and re-bindings). Every token involved resolves to the true capture bytes (ExecC2 §3: no (sid, class) pair new at T), so no defect is masked; the lesson is that an informational count that disagrees with the claim's own number is a finding to explain before F |

## Wave findings

WAVE-DONE received from Main: all 11 seats settled, no dead seats (`.ufo/waves/round-98/w1-results.json`, 11
results with output). Role mix: 3 executor, 2 reviewer, 1 critic, 2 mutation-tester, 1 scout, 1 connector,
1 scribe (5/11 attack roles). Planner held by L1; ConnectorOverlap supplied the bounded planning data-walk.

| seat / finding | observed verdict or defect | disposition |
|---|---|---|
| ExecC1 | counter pass at T, fail at BASE; probe run twice from `git archive` T, OBSERVATIONS byte-equal to the receipt; all 12 DETAIL digests rebuilt by hand; C04/C07/C09 re-run under real pytest outside the probe (rc 0); C04's missing move on the start position is g1f3 (Nf3), duplicated g1h3 | C1 met, independently reproduced |
| ReviewC1 | hook faithful (setup/teardown fail closed, `MISSING` fails closed), reward = pytest exit, C09 a fair adversarial artefact, LANE_TIP = F, L7/L10 match the frozen text; INFO: `pytest-json-ctrf` not staged, L3 accepts any ancestor | no defect; INFO carried |
| CriticClaims | C1 verifies as declared; C2 verifies on its frozen predicate but its effect is 41 cleared findings, not 39; C1-5 unenumerated clauses (SKILL cells unread, admission not checked by L10, ctrf pin, C01's prediction filed after one timing run of solve.sh) | C2 side effect → M4; C1-5 item 4 recorded below |
| ExecC2 | own 39/39 conjunct check without the round-98 counter; 41 = 39 + S213 + S230; no (sid, class) pair new at T | C2 met; side effect quantified |
| ReviewC2 | F1 (material): PROVENANCE URL column clears S230 `digest-wrong-capture` via `prov_url`; F2 S213; F3 S237/S272 re-bound; F4 K7 addition-only | lesson M4; `L1/outside-pop-census.txt` confirms 4 BASE rows; routed |
| MutC2 | 29 mutants, 21 killed, 8 survived: K4 reads only the first `BIND` line (M11/M16 second binding to a byte-identical copy), sha and URL columns unread (M05/M18), S306 out of scope (M15), K2/K3/K6 not sole killers | routed to round 99; predicate at T unaffected |
| MutC1 | 18 input mutants all killed, capture mutant refused rc 2, valid-row control passes; survivors: counter self-integrity (no leg binds the counter's own bytes; freeze rule enforces it) and unread informational receipt fields | routed; no repair |
| ExecHarm | 22 standing checks BASE vs T: no green→red, no new DEFECT; anchor 86→45; round94 freeze-integrity on round 98 13/13 intact | no harm (agrees with L1 battery, which adds r82-c3 29→30 `STATUS-LINE-MISSING regex-chess`, the per-member frozen-declaration delta) |
| ScoutSources | S326–S333 re-opened live: HTTP 200, bytes/sha/quotes equal; five population rows (S181, S276, S290, S310, S322) re-open to their tokens; census rc 0 | agree 13/13 |
| ConnectorOverlap | C1/C2 disjoint bytes; no sibling replays regex-chess or uses provenance bindings; next cheapest replays: mteb-leaderboard, crack-7z-hash, count-dataset-tokens, bn-fit-modify (best legs per cost), train-fasttext | round-99 planning input |
| ScribeLesson | every knowledge-table vector matches the receipt; corrections A–E (C10 witness scope, C08 castling invisible at 47/108 positions, C09 offline precompute, C05/C06 split, `E:` prefix) | applied to `corpus/knowledge/tb2-regex-chess-grader.md`; the 47/108 figure re-derived by L1 (108 calls, 47 with castling `-`) |

### Additional mistake mined

| id | class | evidence | captured-by | fix / shown able to fail |
|---|---|---|---|---|
| M5 | calibration wording | CriticClaims C1-5 item 4: `plans/round-98-claims.md` says predictions were filed "before any case ran", but one unmodified solve.sh grading run (the C01 configuration, a timing run) preceded the predictions file, whose own header says so | Q74 (predictions before first request) — partly: the header disclosed it | wording overclaims for C01 only; C02–C12 were ex ante. Next freeze states the exact set of runs that preceded predictions |
