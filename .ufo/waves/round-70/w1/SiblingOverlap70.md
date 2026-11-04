# SiblingOverlap70 — sibling-overlap and prior-art scan for round-70 w1 ground

Role: connector (leaf). Snapshot taken 2026-11-03 ~21:50 host time, while the wave and the L1 were
landing files; every lane-state number below is a point-in-time observation and names its command.

Axes: **coverage** (did the scan reach the surfaces this round touches) and **calibration** (do
the round's records agree with the lane's existing instruments).

## 1. What I ran

| # | command | rc | result |
|---|---|---|---|
| 1 | `read L/plans/round-70-claims.md` (full, incl. Amendment A1) | 0 | two claims, seven-case table, E1–E8, kill rules read |
| 2 | `grep -n '^#\{1,3\} ' L/PROVINCE.md`; `sed -n '96,200p' L/PROVINCE.md` | 0 | Core/Frontier/Adjacent read; Adjacent owners table at `PROVINCE.md:130-146` |
| 3 | `git -C L rev-parse master` | 0 | `384e9c76415e78093623b3eaff262423a89dbc3e` (round-70 freeze commit) |
| 4 | `git -C L merge-base --is-ancestor 502893ad master` | 0 | base `502893ad` is an ancestor — C1's before-state target is well-formed |
| 5 | python regex census over `{kotoba,mori,kumitate,chousa,tameshi}-shokunin/{PROVINCE.md,corpus/knowledge/**.md}` + `kengaku-shokunin/{PROVINCE.md,corpus/knowledge/**.md}` for five exact term families (§2) | 0 | 34 sibling files / 48 matches; see table |
| 6 | `python3 plans/routed_open.py --lane .` (L) | 0 | `ROWS total=79 open=31 blocked=1 closed=45 refused=2`, `routed_open=32 oldest_round=39` |
| 7 | `grep -ril` fleet-wide for `burn-down\|burn down\|routed-findings` | 0 | `corpus/knowledge` = 0 hits; the surface lives in `SKILL.md:664` and `.ufo/reports/*` |
| 8 | `git -C L status --porcelain`; `git -C L diff master` | 0 | L1 landing in flight: 7 modified lane files + `corpus/evidence/round70/` untracked |
| 9 | `test -e L/corpus/evidence/round70/nginx/check.txt` | 1 | **absent** (the entry cites it; §5.3) |

Tool installs: none. No network. No frozen file edited.

## 2. Counts — term-level vs surface-level

Patterns (case-insensitive, file = PROVINCE.md + corpus/knowledge/**.md):

- a-leg: `leg-coverage|leg coverage|eight-leg|seen_p|seen_f|per-leg|test leg`
- b-routed: `routed[- ]defects?`
- b-nonaut: `non-author closure|non-author (spot-?check|review)`
- c-case_sha: `case_sha256`
- c-staged: `staged[- ]state|staged[- ]input|staged digest`

| family | sibling files / matches | kengaku files / matches | surface-level? |
|---|---|---|---|
| a-leg | tameshi 6 / 11; others 0 | 8 / 28 | 2 of the 6 tameshi files are surface-level (S1, S2) |
| b-routed | kotoba 4/5, mori 1/1, kumitate 3/3, chousa 2/2, tameshi 2/4 = 12 / 15 | 2 / 4 | 2 surface-level (S3, S4) |
| b-nonaut | kotoba 2/2, mori 5/7, kumitate 4/4, chousa 4/4, tameshi 3/3 = 18 / 20 | 8 / 8 | 1 surface-level inside it (S5) |
| c-case_sha | **0 / 0** | 3 / 3 | none — kengaku-internal (I1) |
| c-staged | chousa 1 / 2 | 1 / 3 | none (term-level only) |
| **total (dedup)** | **34 files / 48 matches** | — | **6 surface-level (S1–S6), 5 adjacent (A1–A5), remainder term-level** |

The generic word `witness` was deliberately excluded from the count: it matches 51 sibling files /
236 times (kotoba 54, mori 40, chousa 45, tameshi 114) across unrelated domains (journal witnesses,
verdict machines, argv attribution). It was screened by hand; only S1/S3 below are about witness
*scope* in a gate.

**Definitive negative results (worth as much as the hits):** no sibling lane has `case_sha256`, no
sibling lane has `leg-coverage` for a grader's test legs, `burn-down` appears in **zero** files in
any lane's `corpus/knowledge` or PROVINCE, and the only `Terminal-Bench` content in sibling
knowledge is a topology-paper citation (`kumitate …/multi-agent-coordinator-topologies.md:29,53,83`,
S197: architecture study, not grader legs). TB2 grader leg semantics are kengaku's alone.

## 3. Surface-level hits — each with decision

| id | path:line | what it is | decision |
|---|---|---|---|
| **S1** | `tameshi-shokunin/corpus/knowledge/witness-equivalence-rule.md:25-26` | "kill + `vector` — behavioral **difference** on the named len-9 vector … (Vector length 9 is enforced at validation; shorter vectors only compare crash signatures, never tally behavior)" | **absorb as citation** — C1's eight-token `VECTOR` rule is an instance of this rule; do not present the length-enforcement idea as new to the fleet |
| **S2** | `tameshi-shokunin/corpus/knowledge/runner-tally-audit.md:11` | "The runner's own run-time guard (`npass + nfail + nsetup != nlegs`) only checks a sum, so a loop with one operand duplicated and another dropped still sums to nine and prints PASS. This check fails it by name." | **absorb as citation** — C1's per-leg `seen_p/seen_f` is the same class (sum-blind pitfall), one grader instance of it |
| **S3** | `tameshi-shokunin/corpus/knowledge/guard-kill-closure.md:3,21,27` | recheck runs `defect-probes.py` → `DEFECT_PROBES: open=11 closed=0 total=11`; `:21` pristine selftest must run first, nonzero = evaluation error; `:27-29` "closed certifies only that the named round-17 mutant now kills the selftest" | **absorb as citation; route any general law** — C2's `DEFECTS n=8 → 0` over D1–D8 is a lane-local instance of tameshi's open/closed closure ruler. Copy `:21` (a crashing check is an evaluation error, never a pass) — C2 already does this at `plans/round70_c2_routed_defects.py:343-344` |
| **S4** | `kotoba-shokunin/corpus/knowledge/compound-clause-citation-round63.md:139-141` | "`r62 routed defects closed 0 of 5`, exit 1 … at the round-63 measured rev → `5 of 5`, exit 0" with a verifier + `--self-test` | **no route, no absorb** — gate-shaped routed-defect counter already exists in another lane; subject (citation repairs) differs; it proves C2's shape is conventional, not novel |
| **S5** | `kotoba-shokunin/corpus/knowledge/frontmatter-rule-authorities-round48.md:185` | "Commands that read `/fast/scratch/…` point at uncommitted bytes and are dated provenance only, not re-derivable by a non-author. Routed defect R4 is therefore partly addressed, not closed." | **absorb as precedent** — the exact precedent for C2's kill rule ("prose-only is not closed") and a check that C2's own artifacts are committed bytes (E1 provenance file and E6 receipt are) |
| **S6** | `chousa-shokunin/corpus/knowledge/receipt-digest-provenance-r67.md:5,11,15` | "A receipt digest is evidence only when it re-derives from committed bytes"; pin only committed bytes; name `OUT_OF_TREE`; "re-derivability is provenance, not truth" | **absorb as compliance** — C1's `PROBE`/`PROBE_BLOB`/`GRADER` pins and C2's E1 `SHA` lines must satisfy this rule as written; the rule statement itself stays chousa's |

### Adjacent (surface echo, different object — recorded so a cross-lane reader is not misled)

| id | path:line | relation |
|---|---|---|
| A1 | `tameshi…/witness-scoped-kill-verdict.md:10-23` | defect-row witness assertion; `killed` vs `accidental` — classification of which defect row moved, not which grader leg |
| A2 | `tameshi…/replay-projection-hardening.md:63-65` | a routed-defect **disposition table** with no re-deriving check — the exact shape C2's kill rule forbids; cite as counterexample, not pattern |
| A3 | `mori…/uptime-win-r70.md:56` | "Round-71 correction … routed defect D1, r70 closure section 6" — same `D<n>` vocabulary in the **same round**, different lane/subject (Windows liveness). C2's ids must always be qualified "round-69 spot-check D3", never bare "D3" |
| A4 | `kotoba…/skill-eval-artefacts-round70.md` (F4) | "recording PASS or FAIL with specific evidence" for skill evals — kotoba's grading craft; C1 measures one grader's legs, not grading craft |
| A5 | `chousa-shokunin/.ufo/waves/round-61/w1/RevC1LegsH2.md:11,51` | "leg-coverage gap" for chousa's own hazard legs (final-state blind spot); shared word, different surface |

## 4. Routes (lane + what it owns) and contested scope

| lane | owns (quote) | this round's relation |
|---|---|---|
| **tameshi** | `PROVINCE.md:7-17` "**Owns:** the method … **Refuses:** product domains — every lane's gate remains its own; tameshi owns only the reusable craft (a pattern is admitted from evidence in TWO independent lanes before it is claimed general)"; `:44-45` "report, never absorb" | C2's gate code is kengaku's; the *craft* sentence ("a re-deriving gate closes routed defects") is tameshi's to state and requires two lanes. **Route** any generalization; keep the round's claims as lane instances |
| **chousa** | `PROVINCE.md:136` research method; `receipt-digest-provenance-r67.md` receipt-digest provenance | C1/C2 are **compliance instances** of the receipt-digest rule. **Route**: none pending; cite, do not restate |
| **protocol / aggregator** | `L/PROVINCE.md:140` "fleet process — a fleet-wide preregistration/replay-gate standard and closeout carry-over gates were referred round 11/12–14, not imposed" | C1's case-table/digest convention and C2's gate stay **lane-local**; a fleet standard would be a route, not a claim |
| **kotoba** | `L/PROVINCE.md:128-131` prompt/skill-craft, render/trigger behaviour | S4/S5 are precedent only; A4 (skill-eval PASS/FAIL craft) stays kotoba's. No route |
| **mori** | uptime/liveness context | A3: vocabulary overlap only; qualify defect ids |

**Contested scope this round must not absorb:** (i) any fleet-wide burn-down/replay-gate standard
(protocol/aggregator, `PROVINCE.md:140`); (ii) tameshi's reusable-craft law (needs two lanes);
(iii) chousa's receipt-digest provenance rule statement; (iv) mori's `D<n>` ids — same round, same
token, different subject, so an unqualified "D1" is ambiguous fleet-wide as of round 70.

## 5. In-lane contradictions found (the real collisions are kengaku-internal, not sibling)

### 5.1 The lane already owns a routed-findings burn-down instrument, and C2 closes eight defects outside it

- The instrument: `SKILL.md:664` registers `| routed-findings | gate | python3 plans/routed_open.py --lane . …` with a measured tally; the files exist: `plans/routed_open.py` (10,877 B) and `corpus/routed-findings.jsonl` (79 rows).
- Live run (§1 #6): `ROWS total=79 open=31 blocked=1 closed=45 refused=2` / `routed_open=32 oldest_round=39`, rc 0.
- The lane's **established convention** is that non-author spot-check routed defects are ledger rows: 29 rows cite `*-verifier-spotcheck.md` (rounds 39/40/41/42/45 — e.g. `R39-R1`, disposition `fixed-verified`, with a `close:` and a re-runnable `check:`).
- Round-70 C2 closes round-69 spot-check **D1–D8** and `grep -c 'round-69-verifier-spotcheck' corpus/routed-findings.jsonl` → **0**. A reader using the lane's burn-down gate sees no trace of this round's closure; a reader of C2 sees closure with no ledger row.
- Contradiction between two lane reports, stated as found: `.ufo/reports/round-41/kengaku.md:132` "Assimilation: `considerthese/2026-10-26.md` proposal 1 (routed-findings burn-down) → `plans/routed_open.py` + `corpus/routed-findings.jsonl`" **vs** `.ufo/reports/round-69/kengaku.md:133` "The 2026-10-26 proposal 1 (a routed-findings burn-down ledger) remains unimplemented and is reported still-open". The artifacts and §1 #6 resolve it: the lane instrument exists and validates; the round-69 sentence is stale and needs a **dated, append-only** correction in the round-70 record — never an edit to round-69's report.

**Proposed move (one, bounded).** At close, after the C2 green run at the landing tip, append eight
rows `R69-D1 … R69-D8` to `corpus/routed-findings.jsonl`, sourced at the exact lesson lines
(`corpus/lessons/round-69-verifier-spotcheck.md:170,177,181,187,190,192,196,199`), `status=closed`,
`disposition=fixed-verified`, `close` naming the C2 E-check and the landing commit, and an **offline**
`check` (grep/sha over committed bytes, never the nginx battery). Then `routed_open.py` reports the
burn-down and `round51-routing`'s row legs re-derive it.

- Affected axes: **calibration improved** (closure becomes visible in the instrument a non-author already runs; premise: ledger has 29 spot-check rows, so the precedent is the lane's own). **Coverage: unchanged** (no predicate, table, vector, digest, kill rule or target is touched; rows are post-freeze lane bookkeeping).
- Risks/harms: (a) `round51_routing.py --run-checks` **executes** `fixed-verified` checks — a battery-shaped `check:` would bind port 8080 during another gate run, so the checks must be grep/sha only; (b) the ledger gate requires `source` to resolve `<path>:<line>` to a **non-blank** line and refuses duplicate ids (`plans/routed_open.py:72-111`) — all eight lines above are non-blank headers today, and no `R69-*` id exists; (c) a `closed` row asserts closure in a second instrument, so rows must be appended only after C2's green run, never before.
- Verification: `python3 plans/routed_open.py --lane .` → `ROWS total=87 open=31 blocked=1 closed=53 refused=2`, no `DEFECT line=` output, rc 0; `--list | grep -c 'R69-D'` → 8; `python3 plans/round51_routing.py --lane .` clean row legs; negative control on a **scratch copy** of the ledger (flip one row to `open`) must move `routed_open` by one.

### 5.2 The entry's executable `recheck:` still names the round-69 failing instrument

`corpus/knowledge/tb2-nginx-request-logging-offline.md:3` reads: "`python3 plans/round69_c1_nginx_probe.py --lane . --work <scratch> --receipt <path>` must reproduce the five frozen vectors … `--check-receipt` reports the two leg-coverage defects (the honest MISS of record)." The same file's line 77 (landed this round) says "`PREDICATE R70-C1 pass`; the checker re-derives it". A reader who runs the entry's `recheck:` — the corpus's executable contract — reproduces the pre-correction state and the file's own headline claim fails. No seat assignment and no C1 before→after target names this line. Fix: update `recheck:` to the round-70 instrument (seven vectors, staged-input digest), keeping the round-69 MISS as history in the addendum (which already does it). In-lane; single writer is the L1.

### 5.3 The landed addendum cites a path no seat produces

Entry line 78 cites `corpus/evidence/round70/nginx/check.txt` with "rc 0", but that path is **absent**
(§1 #9) while `W/NginxBatteryR70/check.txt` exists and reads `CHECK ok cases=7 legs=8 seen_p=8 seen_f=8`
/ `CHECK stored-predicate=pass derived=pass` / `PREDICATE R70-C1 pass` / `rc=0`. No seat's assignment
writes the corpus path (NginxBatteryR70's step 4 writes the W path). Fix: copy the W transcript to the
cited corpus path before commit, or cite the W path. In-lane; L1.

### 5.4 `case_sha256` is overloaded inside this lane (prior-art collision, kengaku-internal)

- `corpus/knowledge/tb2-torch-pipeline-parallel-offline.md:42` / `tb2-torch-tensor-parallel-offline.md:44` present `case_sha256` as the CASE-line sha of the case's candidate file (`plans/round67_c1_pipeline_probe.py:203`: `sha256(app / CASE_FILE) … else "none"`).
- `corpus/knowledge/tb2-nginx-request-logging-offline.md:45` (round-69 text) records it as a **whole case-tree** digest that varies across runs.
- Round 70 redefines it for nginx as **staged candidate inputs only** (`plans/round70_c1_nginx_probe.py:20-23,157,331`; receipt `CASE K1 case_sha256=0cf77ab8…`).
Three rounds, three scopes, one field name, no entry states the scope. Not a sibling collision
(sibling hits: 0) — the correction is in-lane: the nginx entry and the round-70 lesson should state
that `case_sha256` is **probe-local** and name its scope per probe; do not let it read as a lane-wide
identity. (Related, different notion: `kumitate …/receipt-identity-canonicalization.md:16-20` — a
receipt's record digest over canonical JSON; do not conflate.)

## 6. Verdict

For the item this seat attacks — sibling-overlap and prior-art collision with round-70's ground:
**no sibling lane owns or collides with R70-C1's surface** (0 sibling `case_sha256`, 0 sibling
grader-leg coverage, 0 `Terminal-Bench` grader content), and the only surface-level craft precedents
(S1–S3, S6) are correctly absorbed as citations under tameshi's and chousa's ownership rather than
claimed. The substantive collision is **in-lane**: R70-C2 closes eight routed defects alongside the
lane's own registered burn-down gate (`SKILL.md:664`, `plans/routed_open.py`,
`corpus/routed-findings.jsonl` — 29 spot-check-sourced rows, 0 for round 69), and the round's landed
text has two dangling contracts (`recheck:` at entry:3, `check.txt` cited at entry:77 and absent).
Absorb all four in-lane, route nothing new, and restate that neither claim is a fleet standard.

Calibration: three of the four in-lane findings were invisible to a `corpus/knowledge`-only scan —
`burn-down` has zero knowledge hits — so the scan reaching `SKILL.md:664` and `.ufo/reports/` is the
load-bearing coverage step; a knowledge-only census would have reported a false all-clear.
