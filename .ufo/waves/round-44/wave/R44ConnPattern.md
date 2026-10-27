# R44ConnPattern — connector: the advertised-vs-demonstrated shape outside C1/C2

Seat: R44ConnPattern (connector, leaf). No subagents, no background jobs. Method: **cheap static evidence only** — reads of the frozen claims, the two tools, the counters, the gate, the flip gate, the probe+receipt, both batteries' `FIXTURES` declarations, SKILL.md's tool registry, SCORECARD capability rows and the round-43 closure spot-check; no counter/battery/probe was executed, so no envelope run was required.

## The shape

C1 and C2 are the same pattern under two presentations:

- **C1 (calibration)** — a tool docstring advertises a check; the count is how many advertised behaviours no fixture demonstrates.  C1's frozen list is the five `u` behaviours (U5 U6 U7 U9 U14c) that battery42+battery43 leave alive (`claims/control-c1-standing-batteries.txt`: `killed=0 survived=5`).
- **C2 (coverage)** — an instruction advertises a check; the captured grader demonstrably checks less (`test_outputs.py:121-122` `assert c in data` is a substring test over the whole file; `instruction.md` names no output format, so passing-without-attack shapes pass).

The connector's job: find *other* sites in the lane where a docstring/README/registry row advertises a check that no test demonstrates (C1 shape) or that is demonstrably weaker than advertised (C2 shape).

## Sites (10)

| # | site (file:line) | advertised (quote) | demonstrated / actual | shape |
|---|---|---|---|---|
| 1 | `plans/gate_flip_check.py:13-18` (rule) vs `:63-66` (limit) | "requires each [conditional refusal] to be resolved by a LATER line of the same lesson" | selftest 19/19 (SCORECARD:1888) proves only that a `Flip check (round N): …` **line exists**; the docstring itself says "the tool checks that a flip was *recorded*, never that the recorded consequence was the right one, so a `fired` line whose evidence contradicts its own landing passes" (`:64-66`). Concrete instance: round-43 Gate recorded `Flip check (round 43): task.toml — not fired` (`corpus/lessons/round-43.md:46`) while the entry cites `task.toml:22`; the non-author closure disagreed (§3) and wrote "the new checker cannot see because it tests that a line exists, not that its verdict is true" (`corpus/lessons/round-43-verifier-spotcheck.md:150-151`). Routed R1. | C2 (check weaker than advertised) |
| 2 | `plans/scratch_guard.py:17-18` vs SKILL.md:605 | "exit 2 when … the sentinel cannot be read (cannot evaluate)" | measured today: unreadable sentinel exits **1**, not 2; `--selftest` has no unreadable-sentinel case (SKILL.md:605 registry row: "check on an unreadable sentinel exits 1 today although `plans/scratch_guard.py:17-18` promises 2 (measured 2026-10-26, routed `R42-R6`)"). | C2 |
| 3 | `plans/order_check.py:29-31` | "Read-only by construction: the only commands issued are `rev-parse`, `log`, `rev-list`, `ls-tree`, `cat-file` and `merge-base --is-ancestor`. It writes nothing, touches no network, imports no probe, gate or counter, and never runs the probe it polices." | no fixture or counter observes any of this: C1's order fixtures assert exit-code directions only (frozen direction for order = U14c, the exit-2 claims-name guard), C2 V8 asserts one output line (`ORDER RESULT PASS`); nothing traces order_check's own subprocess set or writes. | C1 |
| 4 | `plans/anchor_digest_check.py:24` | "Read-only; stdlib only; writes no file." | no test demonstrates the no-write guarantee: the C1 counter's `TAMPERED` fingerprint covers only the fixture tree (`round44_c1_verify.py:909-913`), never whether the tool wrote elsewhere (work dirs, TMPDIR). | C1 |
| 5 | `plans/anchor_digest_check.py:31-32` | "Row set — the census shape (`plans/round37_c2_verify.py` SOURCE_ROW …), so this check and the census agree on what a row is." | agreement never jointly tested: C1 never runs the census; C2 V6 runs the census but never the anchor tool. | C1 |
| 6 | `plans/anchor_digest_check.py:88-92,97-98` | per-token defect classes `digest-short`, `digest-long`, `digest-uppercase`, `token-outside-anchor`, `abbrev-unresolved`, `capture-unanchored`, `anchor-unbound` | **no committed fixture declares any of the seven**: over battery42+battery43 the only declared defect classes are `row-malformed` (8), `digest-unknown` (4+2), `erratum-digest-unresolved` (2), `digest-wrong-capture` (2), `erratum-incomplete` (2) (`grep -rhoE '"defects": \[[^]]*\]' plans/battery42 plans/battery43 | sort | uniq -c`). Two of the seven — `digest-short`, `digest-long` — are exactly frozen C1 mutants U5/U6 → the C1 count is this class gap, measured for two of seven tokens. | C1 (the C1 shape itself) |
| 7 | `plans/round_close.py:42-44` | "Read-only: the only git commands are the ones `plans/order_check.py` itself issues, plus one `rev-parse` and `cat-file -e` here; … Nothing is written, no network is touched, no probe, gate or counter is imported or executed." | no counter or battery targets round_close at all — C1 names it as the third tool the counter does not mutate, with 17 reachable survivors carried as a limit (`round-44-claims.md:68-69`); its `--selftest` covers the five receipt-placement shapes, not the IO guarantees. | C1 |
| 8 | `plans/state_check.py:21-22` | "Exit 0 means all comparable frozen assertions match; 1 means any mismatch; 2 means usage, unreadable input, or empty population (never a vacuous PASS)." | `main()`'s exit-2 paths were unwitnessed at the round-41 data walk (SCORECARD:1634: L4694 `return 2`, L4701×2, L4703 empty population) and no committed battery targets state_check; only `--selftest`/`--summary` exist. | C1 |
| 9 | `plans/pkg_gate.py:12-13` | "An unparsed row, a manifest line that fails its own digest, a quote not verbatim on its cited line, and a receipt a fresh run does not reproduce are defects." | these failure modes were demonstrated by the round-37/38/39 mutation batteries for their specs; for `pkg-spec-r44.json` no red control exercises any clause's reject path — round-44 controls cover C1 fences and C2 predictor/nothing only, and C2 V2 exercises the gate's accept path once. | C1 (current-spec red control absent) |
| 10 | `plans/anchor_digest_check.py:73-77` | "`--evidence-ref index` reads the index blobs (…), identical to HEAD in a clean tree, and exists so a seat that may not commit (round-37 fixture seats are index-only) can demonstrate the green state of a tree whose captures are staged." | **no fixture passes `--evidence-ref` at all** (grep over battery42/battery43: zero argv uses; the only mentions are the argv-shape fence `round44_c1_verify.py:22,458,542`). battery42's x13 fixtures stage captures but run the default HEAD ref and expect `digest-unknown` — the advertised index mode is never executed. | C1 |

## Cross-claim reading

- The two frozen claims are *members* of the pattern, not the whole class: the same shape recurs at 10 sites; C1's five-mutant count is the priced slice of site 6 (U5/U6 = `digest-short`/`digest-long`), and C2's "grader checks less than the instruction" is the same structure as sites 1-2 (a checker/exit map that is weaker than its docstring).
- Site 6 is the most C1-like: the anchor tool's own docstring is the contract, and the seven classes with no fixture are precisely "advertised-but-undemonstrated" as round-43 `R43PlanNext` §B defines it; two of them are the frozen list.
- Sites 3/4/7/10 are the "self-description" leg: security/IO guarantees written into docstrings that no harness observes.

## Limits of this evidence

- Static only: "no test demonstrates" is inferred from committed artifacts (battery `FIXTURES` declarations, counter code, registry rows, selftest lists), not from executing anything.
- Site 9 has historical demonstrations for older specs; the claim is only that no *current-round* red control exists.
- Sites 7/8 overlap round-43 routed residuals (R5 carries C1 guards; state_check/round_close survivors are named limits in the frozen claims) — this connector reports them as additional instances of the same shape, not as new findings.
- The frozen surface was not touched; nothing here edits plans/, corpus/ or claims/.

VERDICT: pattern-10-sites
