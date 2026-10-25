# Round 34 — frozen claims (kengaku, hyaku run 7, 2026-10-25)

Baseline: lane branch tip `5022357cc69334e83b5a2f76c34daea440077a57` (local = remote, `ahead=0`).
Registry 97 rows (ids ≤ S104; S105+ unused), `corpus/knowledge/` 41 files, 41 index rows,
census exit 0 with 15 `W04` (before receipt: `.ufo/waves/round-34/claims/census-before.txt`).
Two claims, two distinct axes, plus the frontier step (§2b) and the standing assimilation/
quarantine duty (§10). Frozen BEFORE any wave seat ran; a predicate changed after a seat has
scored is not this claim's predicate.

Lowest non-retired axis: **coverage 7**, tied with **novelty 7** (SCORECARD §Round 31/33).
No stagnation waiver: the saturation line is 8, novelty sits below it, and a capability
row entered at round 31. Tie-break per the lane's recorded rule: the claim most falsifiable
with the sources an on-host tool can open wins — C1 opens three pinned Terminal-Bench 2.0
files and lands a registry delta; a novelty claim needs a phenomenon probe and no
identity-verified endpoint exists (`corpus/README.md` §Frontier bullet 4). C1 carries the
lowest-axis obligation.

Round shape: **one v2 wave** (`ufo-wave-policy-v2.json`, band 64–128), 64 seats, build +
attack items together, ≥25% attack roles, m_flash majority. Routing per the operator's
run-7 role map (host route table `~/.omp/agent/config.yml`; no per-seat model). The §3
planner seat is held by the L1 (validator-frozen topology); a bounded planning data-walk
rides the R34ReconSources scout item and the connector items.

## C1 — coverage: the Terminal-Bench 2.0 task evaluator opened and grounded

**Surface this claim moves:** the frontier clause "Terminal-Bench 2.0's scoring code remains
open" (`corpus/README.md` §Frontier bullet printed279; round-31/33 narrowing left exactly this
clause standing). This claim opens **one pinned Terminal-Bench 2.0 task evaluator** —
task `protein-assembly` at commit
`2fd12b88aafdd04a52c298e3940bcb189f9766d6` (the latest commit of
`harbor-framework/terminal-bench-2`, the same tree S100 pins) — and grounds its comparison
against that task's **expected artifact** (the environment files the evaluator checks
against). The evaluator is `protein-assembly/tests/test.sh` (test runner; writes the reward)
plus `protein-assembly/tests/test_outputs.py` (the grading logic). The expected artifact is
`protein-assembly/environment/antibody.fasta` + `protein-assembly/environment/pdb_ids.txt`
(the subprotein sequences and PDB id list the grader's translation checks reference).

**Frozen predicate (one sentence, same condition in the counter's code, same label in the receipt):**

> `corpus/knowledge/terminal-bench-task-grader.md` exists with `source:` lines citing exactly
> the three ids S105, S106, S107 (three distinct), a `verified-at: 2026-10-25` line, and
> every one of those three cited rows present in `corpus/SOURCES.md` with `status=mined`,
> `opened=2026-10-25` and `used-by` naming the entry; the entry has exactly one index row in
> `corpus/README.md`; and
> `python3 plans/round34_c1_verify.py --lane .`
> prints `checks=8 defects=0` and exits 0.

**Counting command:** the last clause above (`plans/round34_c1_verify.py`, new this round:
V1 entry exists with the three `source:` ids; V2 `verified-at:` literal; V3 each of S105/
S106/S107 present with `status=mined` `opened=2026-10-25` `used-by` naming the entry; V4
exactly one README index row; V5 README coverage bullet carries the discharge sentence; V6
frontier bullet :279 keeps the other open clauses verbatim; V7 the freeze control receipt
exists and its text matches the committed `control-c1.txt`; V8 the captured evaluator bytes
match the committed `SHA256SUMS`).
**Control (committed at freeze):** `.ufo/waves/round-34/claims/control-c1.txt` — the same
census/cat-file probes on the pre-admission tree: `git cat-file -e` for the entry and each
new row fails (exit 128), registry rows = 97, and the counter on the pre-tree prints
`checks=8 defects=8` and exits 1.
**Kill rule:** a cited source whose located quote cannot be found in this round's captured
bytes at the pinned revision is refused for that row; if fewer than three of the cited rows
survive, the entry is not admitted and C1 is a recorded honest stop (registry delta 0). The
scratch id-collision guard (0–3 leading spaces, both id lists) runs before any append and its
proof fixture is committed under `.ufo/waves/round-34/assimilation/`; a nonempty `collisions`
file is expected (staged package still holds S105/S106/S107 names for *other* documents) and
is recorded, with the adopted ids continuing the lane's registry per CORPUS.md rule 2.
**Axis verdict shape:** the entry is new corpus bytes on ground the coverage map did not
hold (a TB2 task's own scoring code); the canonical coverage score stays 7 while the round-25
L0 coverage cap is open, so the row records the ledger delta and an `improved` trend, not a
raised number.

## C2 — calibration: the defect counter hardened against four mutant classes

**Surface this claim moves:** the four measured counter blind spots the round-33 falsify
wave and closure named — index-vs-HEAD, heading-only, width/newline, and
token-co-occurrence (`corpus/lessons/round-33.md` §Mistakes rows; round-33 verifier
spotcheck §5). This claim ships a new defect counter `plans/round34_defects.py`
(N1–N8) and a mutation harness `plans/round34_mutate.py` that applies one mutant per class
to a sandbox export of the lane and asserts the counter goes red on every mutant and stays
green on the clean tree (failing-before receipts for each class are committed before the
hardening is applied).

**Frozen predicate:**

> `python3 plans/round34_mutate.py` prints `MUTANTS total=8 detected=8` and exits 0 on the
> landed tree (each of the four classes: one red-before receipt committed under
> `.ufo/waves/round-34/falsify/red-before/`, the same class green-after in the harness run);
> `python3 plans/round34_defects.py --lane .` prints `checks=8 defects=0` and exits 0; and
> `python3 plans/round34_defects.py --selftest` and `python3 plans/round34_mutate.py
> --selftest` both exit 0. The do-nothing control (committed at freeze) prints both tools
> absent: `git cat-file -e` fails for `plans/round34_defects.py` and
> `plans/round34_mutate.py` (exit 128 each).

**Counting command:** the two commands above.
**Control (committed at freeze):** `.ufo/waves/round-34/claims/control-c2.txt`.
**Kill rule:** a mutant class whose detection cannot be shown failing-before then
green-after stays open and C2 misses; a partial receipt or a selftest alone is not closure.
The four classes map to checks as follows: index-vs-HEAD → N8 (knowledge files vs README
index rows, both directions); heading-only → N2/N7 (a `## Round <N>` heading with no section
content must fail); width/newline → N5/N6 (wrapped or RFC-width line variants of the pinned
line numbers must fail); token-co-occurrence → N3/N4 (the `near()` co-occurrence check must
not pass when the tokens exist in the file but not in the required relation).
**Separability:** reads only `plans/round34_defects.py`, `plans/round34_mutate.py`,
fixtures under `.ufo/waves/round-34/falsify/`, plus the repo surfaces its N-checks read
(SCORECARD, lessons, wave trees) — no artifact C1 creates (SOURCES rows S105–S109, knowledge
entries, README rows) and no artifact C1's counter reads.

## Frontier step (§2b), assimilation/quarantine (§10), considerthese, and disclosures

- **Sourced claim:** C1 rests on rows opened this round — S105/S106/S107's Gate records carry
  this round's access date and ≤25-word located quotes; the admitted entry cites them.
- **Census before → after:** `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin kengaku` (exit 0, 15 W04) recorded at freeze
  (`.ufo/waves/round-34/claims/census-before.txt`); rerun at round end and pasted in the
  report with its exit code.
- **Mistake mining:** `corpus/lessons/round-34.md` §Mistakes (class · evidence · captured-by
  · fix); at least the class-recurrence lesson (the routed-defect class that recurred
  D2: r30 → r31, per `considerthese/2026-10-25.md` proposal 2) and this round's own freeze/
  landing lessons ride in.
- **considerthese:** `considerthese/2026-10-25.md` proposal 2 (one persistent routed-defect
  ledger) is opened and mined: its cheap half lands as `QUALITY.md` Q23 — a defect class that
  recurs twice blocks pre-registration unless the round's counter includes a hardened check
  for that class — citing `considerthese/2026-10-25.md` + date; the persistent
  `corpus/defects.jsonl` ledger itself stays named debt. Proposal 1 remains operator-side;
  proposal 3 landed in round 33.
- **Quarantine (payload-absent rows):** the lane's full register slice
  (`.ufo/waves/round-34/assimilation/quarantine-slice` — rows S091 and S105 of the staged
  package) is hand-checked this round: fetch the cited source, locate the quote. Both
  sources are expected to resolve this round (NEC技報 page; Internet Archive snapshot of the
  METI page); each row that verifies is adopted under a new unused lane id (S108, S109) with
  the anchor located this round, cited by the admitted entry
  `corpus/knowledge/provider-selfreport-eval-limits.md`. Any row whose quote cannot be located
  is refused (fabrication class) with the reason in the Gate block. The source repo and the
  register stay read-only; verdicts land in `corpus/lessons/round-34.md` and the report.
- **Assimilation theme:** the package knowledge entries are screened by seats; admission is
  ONLY for entries that clear the per-entry gates (PROVINCE scope, QUALITY Q1–Q8/Q21, new
  coverage-map ground). The package's `terminal-bench-release-identity.md` (cites S100/S092,
  already mined) and `toolathlon-grader-contract-2026-10-23.md` (cites staged S114) are
  primary candidates for admission or refusal with reasons; verdicts land in the Gate.
- **Inherited state:** lane tip clean at baseline; no uncommitted lane-authored leftovers. The
  round-33 verifier spotcheck minor notes (lesson header seat-count wording; control prose vs
  receipt) are addressed in the round-34 lesson and this freeze (control receipts here pin the
  actual counter output, not prose).
