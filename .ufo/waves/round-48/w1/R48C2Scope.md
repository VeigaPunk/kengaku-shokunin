# R48C2Scope — scout report: entry + PROVINCE boundary vs sibling ownership; grader-interpretation vs benchmark/runtime/model performance

Seat: R48C2Scope (scout, @m_kfc), serving R48-C2 (coverage). Read-only item; no scored counter/probe
run made. Item: *check the entry and PROVINCE boundary against sibling ownership; distinguish grader
interpretation from benchmark/runtime/model performance.*

## Axes named

- **coverage** (seat axis): is the round-46 TB2 `polyglot-c-py` package's entry within kengaku's own
  ground, and does it add covered ground without absorbing sibling scope?
- **calibration** (secondary, godspeed axis walk): are the entry's claims measurement-shaped (grader
  interpretation) and not performance-shaped (benchmark/runtime/model)?

## Revision measured

REV a543d92083557dd9b33ee674e9b99b03411f80af (stage-1 freeze commit, 2026-10-27 06:53:29 -0300).
One live clone at the freeze commit under my scratch: `/fast/scratch/hyaku/kengaku-r48/R48C2Scope/lane`
(`git rev-parse --show-toplevel` verified == that dir before any read; clone `--shared`, worktree
checked out at the freeze).

## Freeze existence and ordering (measured, not assumed)

- `git cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af` → `commit`; lane log:
  `a543d920 … stage-1 freeze of C1 … and C2 …` → `453ddfd … w1 v2 dispatch evidence` (08:29:18)
  → `bf783c1 … w1 ready handoff marker` (08:29:33). The freeze **predates** every wave-1 artifact today.
- `git show a543d920:plans/round-48-claims.md | sha256sum` → `87e6075ff2c0…6786672`; live tree copy
  identical → the binding claims file is byte-frozen at the freeze commit.
- `git ls-tree a543d920 plans/ | grep round48` → empty: `plans/round48_c2_verify.py` and the stage-2
  literals/pins do not exist yet. No scored run is therefore possible or made from this seat; stage 2
  has not happened. All checks below are read-only committed-byte checks on the frozen tree.

## Commands run and observed outputs (evidence)

1. `python3 -c "import re,sys; …" corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`
   (the Q40 executable check, QUALITY.md:1091) → **`both-print toolchain`** — exactly QUALITY Q40's
   stated round-46 failing output; confirms from committed bytes that V7 is unsatisfiable on the
   frozen table (this is the defect R48-C2 stage 2 must repair by adding/re-wording cases, never
   re-wording tags).
2. Same check on `corpus/evidence/round45/password-recovery-dry-cases-freeze.txt` → **`-`** — the
   check discriminates (round-45 table is fully exercised).
3. `(cd corpus/evidence/round46/tb2-polyglot-c-py && sha256sum -c SHA256SUMS)` → all eight captures
   `OK` (test_outputs.py `b94a7a98…`, test.sh `4770437e…`, instruction.md `a57c0c0e…`, solve.sh
   `e768453a…`, Dockerfile `2eb537f2…`, task.toml `d31b9f60…`, README.md `591e27f9…`, gitignore OK).
4. `sha256sum plans/pkg_gate.py plans/polyglot_c_py_probe.py` → `ea638822…edd41` and
   `67a8f4a6…85f26` — both match `plans/pkg-spec-r46.json` `frozen_instruments` pins exactly.
5. `grep -n 'polyglot' PROVINCE.md corpus/README.md` → PROVINCE.md:648 (round-46 paragraph names
   `tb2-polyglot-c-py-grader.md` and `polyglot-c-py/tests/test_outputs.py` on one line — satisfies
   the r46 counter's V9 PROVINCE clause); README names it at :79 (coverage map), :308, :433
   (Frontier "Partly discharged round 46"), :644–645 (evidence index).
6. `ls corpus/knowledge/ | grep -c '^tb2-'` → `12`; entry's "twelfth exemplar" count is consistent
   with the tree.

## Findings

### F1 — the entry sits inside kengaku's province, confirmed from both sides of each boundary

- kengaku `PROVINCE.md` domain header: "LLM/model research & evaluation"; §Frontier names "agentic
  benchmark task-spec audits (Terminal-Bench 2.0 …)". The entry is exactly that: a read-and-execute
  of one pinned TB2 grader over lane-authored synthetic end states (`cases=18 observed_pass=7
  observed_fail=11 mismatches=0`, `regrade cases=18 differ=7`).
- The round-46 PROVINCE paragraph (PROVINCE.md:648) draws the boundary itself: "Polyglot construction
  as a technique, and how an agent should build the file, stay the task's and the authors' business —
  not this lane's." Same pattern as the round-44/45 paragraphs.
- **chousa** (`chousa-shokunin/PROVINCE.md:11`) refuses "model-quality or evaluation claims
  (→ kengaku)" — grader interpretation is kengaku's by the sibling's own text; capture/citation
  method stays chousa's and the package does not re-derive it (SOURCES rows S166–S172 follow the
  fleet-frozen contract-v1 census; the r46 spotcheck ran `sources-census.sh validate` → `kengaku ok`).
- **tameshi** (`tameshi-shokunin/PROVINCE.md:42`) refuses "model quality/eval (kengaku)" and owns
  only the reusable mutation/fixture method, never a sibling's gate. R48-C2's V14 battery mutates
  kengaku's own committed package bytes with wave-1 mutation-tester seats — the round-37 ruling
  (`PROVINCE.md` round-37 report-out) already scoped this as lane-local with tameshi cited as
  precedent, not absorbed. No boundary crossed.
- **kumitate** (`kumitate-shokunin/PROVINCE.md:24`): "kengaku evaluates agents, this lane arranges the seats
  around that judgment" — the C2 claim arranges nothing about seats; no overlap.
- **kotoba**: prompt/skill craft; the entry contains no prompt wording. **kama**: local LLM
  serving/endpoints; the probe's host `gcc`/`python3` are ordinary build tools inside the probe's own
  bwrap cases, not the model-serving plane, and no endpoint is touched. **kake**: web properties;
  none.

### F2 — grader interpretation is cleanly separated from benchmark/runtime/model performance

In-scope grader interpretation (measured, receipt-backed): the exact-listing assert taken before the
grader's own compile; the gcc leg writing `cmain` into the asserted directory (non-idempotency,
`regrade … differ=7`); three fixed-point literal comparisons on `stdout.strip()` of both runtimes;
the requirement map's `enforced`/`partly`/`not exercised` labels derived from the receipt; the
`leftover-cmain` instruction-vs-grader contradiction; the `toolchain` tag named by the requester but
enforced by no grader line.

Refused and actually absent from the entry's claims: **benchmark performance** ("no image run, no
agent, no trajectory"; `lookup-table` is recorded as grader semantics — three public fixed points —
not a difficulty or gameability claim; oracle correctness and prevalence refused); **runtime**
(Harbor verifier execution/retries/`/app` restoration explicitly out; the non-idempotency finding is
"measured by grading the same tree twice, not an observation of Harbor's verifier"); **model
performance** (nothing in the package runs a model; the `## Predictor` block is a static reading
contract over the counter's generator template, admitted unchanged, not a capability claim).
Measurement-environment limits are stated as limits (host gcc/python3 stand in for the image's
gcc 13.2.0 / python 3.12.3; pytest itself not run).

The one version-shaped sentence in the package — instruction.md:9 "I'm using python3 3.12.3 and gcc
13.2.0." — is quoted in the entry's own table as "the requester states a toolchain, **not a
constraint the grader checks**", and the round-48 lesson's `## Gate` rejected the Docker Hub tag
page for version claims (tag metadata publishes an image digest, no installed package versions).
So the package holds the toolchain as requester assertion + grader non-enforcement, not as verified
runtime fact. That is the correct discipline.

### F3 — the wave-2 errata are present and un-healed

The entry carries its round-46 wave-2 errata verbatim: (1) Summary/Finding-7 class contrast
overstated vs `tb2-feal-differential-cryptanalysis` (imports the agent module and calls its
`attack` function — the narrower true claim is no earlier exemplar *compiles* the graded artefact or
runs the same bytes under two runtimes); (2) `instruction.md:7` names `f(1)=1`, exercised by no
graded N and no frozen case. Neither erratum re-opens a sibling boundary.

### F4 — V9 naming clauses satisfied at the freeze; V7 defect confirmed from committed bytes

PROVINCE.md:648 names the entry and task on one line; README §Frontier names it (:433). The Q40
tag check prints `both-print toolchain` on the frozen table (F-evidence 1) — the exact class the
claims file's C2 delta (a) freezes a positive fix for at stage 2.

## Sources opened

Lane files and digest-verified captures at REV a543d920 (read in-clone; URLs are the pinned upstream
rows, captures byte-verified against `SHA256SUMS` — I did not re-fetch):

- S166 `tests/test_outputs.py` — `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py` — accessed 2026-10-27 (committed capture) — `:27 "test_cases = [(42, \"267914296\"), (10, \"55\"), (0, \"0\")]"` (8 words).
- S168 `instruction.md` — same base — accessed 2026-10-27 (committed capture) — `:9 "I'm using python3 3.12.3 and gcc 13.2.0."` (7 words).
- S169 `solution/solve.sh` — same base — accessed 2026-10-27 (committed capture) — `:12 "cat <<'EOF' > polyglot/main.py.c"` (4 words).
- S171 `task.toml` — same base — accessed 2026-10-27 (committed capture) — `:34 "allow_internet = true"` (3 words).
- S172 `README.md` — same base — accessed 2026-10-27 (committed capture) — `:24 "4. Test cases: f(0)=0, f(10)=55, f(42)=267914296"` (6 words).
- `corpus/knowledge/tb2-polyglot-c-py-grader.md`, `plans/pkg-spec-r46.json`,
  `plans/round46_c3_verify.py`, `corpus/evidence/round46/polyglot-c-py-{probe.txt,dry-cases-freeze.txt}`,
  `corpus/QUALITY.md` (Q40/Q30/Q24), `PROVINCE.md`, `corpus/README.md`, `plans/round-48-claims.md`,
  `corpus/lessons/round-46-verifier-spotcheck.md`, `corpus/lessons/round-48.md` — all lane-internal.
- Sibling provinces (read-only, live trees): `chousa-shokunin/PROVINCE.md:11`,
  `tameshi-shokunin/PROVINCE.md:42`, `kumitate-shokunin/PROVINCE.md:24`, `kotoba-shokunin/PROVINCE.md`,
  `kama-shokunin/PROVINCE.md`.

## Limits

- Stage-2 artifacts (`plans/round48_c2_verify.py`, the amended case table for `both-print`/`toolchain`,
  `<V>`, `<N>`, before-control receipts) do not exist yet; their adequacy is unverifiable from this
  seat. The amended cases' grader-interpretation quality (do they genuinely exercise "both runtimes
  must print" and the named-toolchain boundary?) can only be judged after stage 2 lands.
- Whether any of the 18 case verdicts flips under the image's gcc 13.2.0 / python 3.12.3 is
  unknowable from committed bytes (no image pull in-province; Docker Hub version claim rejected).
- The executed receipt is one historical run; a fresh probe re-run (P10) is forbidden pre-stage-2
  (Q30), so receipt-vs-runtime drift cannot be checked this wave.
- I did not re-open S167/S170 upstream (their captures verified by digest; the lane's registry
  contract treats digest-verified captures as the citable bytes).

## VERDICT

The round-46 `polyglot-c-py` entry and its PROVINCE paragraph sit squarely inside kengaku's
evaluation province — confirmed from kengaku's PROVINCE and from each sibling's own PROVINCE text —
and the package holds the grader-interpretation line cleanly: every finding is a measured property
of the captured scoring predicate, with benchmark performance, Harbor runtime behaviour and model
performance each explicitly refused and absent from the claims. The committed-bytes state matches
the claims file's description (V7 defect `both-print toolchain` present and frozen; digests, pins,
V9 naming all satisfied). No scored run made; no freeze, predicate or control altered. Scoped item
complete; no sibling-ownership boundary violation found.
