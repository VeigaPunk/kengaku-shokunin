# SiblingOverlap — kengaku round 66, wave 1 (connector seat)

Read-only cross-lane overlap scan + one `considerthese/` selection.
Lane repo L = `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Seat dir W/SiblingOverlap.
Scratch S = `/fast/scratch/hyaku/kengaku-r66/SiblingOverlap` (created; no build performed).
Observed bytes for every value below are in `receipts.txt` (same directory) and in the
command transcripts quoted inline. No lane file, `considerthese/` file, `MANIFEST.json`,
fleet-root file or sibling lane was written or modified by this seat.
No tool was installed (tooling-only rule: install nothing unless the item names it).

---

## 1. Sibling `PROVINCE.md` overlap scan

Command (seat regex, verbatim):

```
cd /home/vgpnk/Projects/shokunin && for f in $(ls -d */PROVINCE.md | grep -v '^kengaku-shokunin/'); do
  grep -n -i -E 'torch|tensor.parallel|gloo|bwrap|sqlite.*gcov|kv-store|grader' "$f"; done
```

Scope: **20** sibling `PROVINCE.md` files exist (`kumitate-shokinin` has none; it is a
duplicate directory name, not a lane).

### Hits (path:line, one-line judgement)

| path:line | term | judgement |
|---|---|---|
| `kumitate-shokunin/PROVINCE.md:38` | `bwrap` | **Not sibling-owned ground.** The word sits inside kumitate's own round-73 host-correction paragraph about its kimi-census win32 portability repair ("cap-run/bwrap gate children", FIFO fixtures, POSIX chmod floors). It is a census-selftest sandbox, not a TB2 grader replay; kumitate owns OMP route resolution and fallback policy (kengaku `SKILL.md:3` arbitration clause), and R66-C1/C2 own no kumitate surface. |

**That is the only hit.** Per-term counts across all 20 sibling `PROVINCE.md` files
(`grep -c -i -E` per term, receipt R2):

```
term=torch hits=0   term=tensor.parallel hits=0   term=gloo hits=0
term=bwrap hits=1   term=sqlite.*gcov hits=0       term=kv-store hits=0
term=grader hits=0
```

### Extended near-miss scan (terms added beyond the seat regex; receipt R8)

Not in the seat regex, but adjacent enough to be judged explicitly, since a false
"sibling owns the sqlite ground" conclusion would be costly:

| path:line | term | judgement |
|---|---|---|
| `kagi-shokunin/PROVINCE.md:29` | `sqlite3` | **Not sibling-owned ground.** Host-tooling debt: kagi's own `transcript-scan`/`surface-census` selftests need a `sqlite3` binary (SETUP/127). It is a missing-binary note on kagi's tools, not a grader replay. |
| `kaidoku-shokunin/PROVINCE.md:352,356,358` | `SQLite` | **Not sibling-owned ground.** kaidoku's REA surface is a *catalog reader* (`inspect_sqlite_database`, node:sqlite worker, SQLite 3.53.4) that reports the SQLite catalog of a quiescent file and explicitly "is not an integrity check". R66-C2's ground is the opposite object: a **gcov-instrumented `sqlite3` compiled in place from the pinned amalgamation**, PATH-staged and bwrap-masked, graded as a build artefact. Different artefact, different claim. |

Arbitration check (ownership of the benchmark ground): `kasegi-shokunin/PROVINCE.md:50`
lists, under "Sibling lanes are reported, not absorbed", the line `kengaku — LLM evaluation
and benchmarks`. kengaku's own `SKILL.md:3` arbitration clause reserves to kengaku the
"measured capability effects" of offline replay grading. Nothing in any sibling `PROVINCE.md`
claims the TB2-grader-replay ground.

---

## 2. Sibling `plans/` + `corpus/` scan for this grader

Command (verbatim, one per sibling lane):

```
for d in */; do n=${d%/}; [ "$n" = kengaku-shokunin ] && continue
  for s in plans corpus; do [ -d "$n/$s" ] && \
    grep -rn -E 'torch-tensor-parallelism|tensor-parallel|offline-torch' "$n/$s"; done; done
```

**Result: `R3_FILES_WITH_HITS=0`.** No sibling lane's `plans/` or `corpus/` names this
grader, this capability name, or tensor parallelism at all.

Repo-wide cross-check (receipt R4), excluding kengaku — three files mention
`torch-tensor-parallelism`, and **all three are kengaku's own material, not a sibling
executing the grader**:

| path | what it actually is | judgement |
|---|---|---|
| `.ufo/reports/round-53/kengaku.md` | the fleet's own report **of kengaku** | not a sibling lane; no overlap. |
| `souji-shokunin/.ufo/waves/round-43/w1/R43connectorA.md:459` | souji's own sibling-overlap scan **quoting kengaku's corpus**: the matched line is `HEAD:corpus/lessons/round-52.md:56\|` … `torch-tensor-parallelism` … — a `HEAD:`-prefixed capture of a **kengaku** lesson row inside souji's report. | a citation of kengaku's registry row inside souji's scan output, not souji executing the grader. |
| `souji-shokunin/census/round-43/waves/w1/R43connectorA.md` | the census copy of the same file | same as above. |

Registry check (receipt R5): across all sibling `corpus/SOURCES.md`, only
`kengaku-shokunin/corpus/SOURCES.md` names `torch-tensor-parallelism` (1 line, S183).
**No sibling holds a registry row for this grader, so there is no cross-lane registry
collision to arbitrate.**

Residual-word check (receipt R6 + a follow-up): the only files in the fleet outside kengaku
whose *filename* matches `*torch*`/`*tensor*` are
`kumitate-shokunin/.ufo/waves/round-36/build/ConnectorChecklistConsumers.md` and
`tsukuroi-shokunin/.ufo/waves/round-17/falsify/FxOperatorChecks.md` — both match only
because of the substring `torCh` in "Consume**torCh**ecklist" / "Opera**torCh**ecks".
Word-boundary `torch` hits in sibling `corpus/` are incidental: a kaidoku ELF envelope JSON
(base64 blob) and kotodama mythology prose ("torch-bearing"). Word-boundary `gloo`: **0**
hits fleet-wide outside kengaku. No sibling lane has a `torch` tree or venv
(`find -maxdepth 3 -name torch -type d` outside kengaku → none).

**Finding (item 2): no sibling is executing this grader; no sibling owns any part of its
ground.** R66-C1's capability `offline-torch-tensor-parallel-grader-probe` is uncontested
across the fleet.

---

## 3. `considerthese/` selection — ONE item

### The file

Most recent by name and date: `kengaku-shokunin/considerthese/2026-10-26.md`
(siblings present: 2026-10-19 … 2026-10-26; 2026-10-26 is the latest).

### Items marked "proposals only" or "not implemented"

The file's section `## Self-improvement suggestions (proposals only; not acted on)` lists
three:

| # | heading | implemented by the lane? | evidence |
|---|---|---|---|
| 1 | "A routed-findings burn-down, not just a defect ledger." | **Yes** | `plans/routed_open.py:240` prints `routed_open={pending} oldest_round={oldest}`; `corpus/QUALITY.md:1128-1130` records "this criterion adopts proposal 1 of `considerthese/2026-10-26.md`"; `plans/round-41-claims.md:122-123` lands it as a rider. |
| 2 | "One standing TB2 admission counter with a built-in filler control." | **No** — see below | `grep -rn 'tb2_grader_admit' plans corpus SCORECARD.md` → **0 hits** (grep exit 1); `ls plans/tb2_grader_admit.py` → *No such file or directory*; `python3 plans/tb2_grader_admit.py --lane .` → exit 2. |
| 3 | "Batch the TB2 grader sweep and file the stability rider." | **Yes** | `corpus/evidence/round62/class-survey.txt`: `CLASS-CENSUS roster=89 … classes=16` and `EXECUTED-COVERAGE executed=17 … classes-uncovered=network-service,process-environment,db-state,container-image`; class histogram `.ufo/waves/round-43/build/R43ConsiderThese/hist.md`; stability rider `R40RegradeSweep` recorded at `corpus/lessons/round-40.md:31` ("five earlier TB2 graders, 15 end states graded twice"). |

### The pick — item 2, quoted verbatim (`considerthese/2026-10-26.md:44-49`)

> 2. **One standing TB2 admission counter with a built-in filler control.** `plans/round3{6,7,8,9}_c2_verify.py` are
>    per-round copies with the identical before state (`checks=7 defects=4`, V2/V3/V4/V7), and r36, r37 and r38 each
>    record the counter admitting a junk or informed-filler package. Proposal: a single parametrised
>    `tb2_grader_admit.py` that digest-pins the spec, dry table and probe it reads (the r37 V2 hole), ships a committed
>    filler package that must stay red, and is re-run at every tip for all five admitted graders. A counter that
>    admits filler should not appear in a verdict cell as the admission basis.

(Quote block sha256 `760e57a9ee3eb5d8855326dc387853cf386e3dad07ab4e1d78715e01b01a4b5d`.)

### The contradiction this pick exposes (reported, not edited)

`corpus/lessons/round-65.md:47` — committed at `edbb0bc0` — records:

> … its three "proposals only" items were already implemented before this round: proposal 1 … → `plans/routed_open.py`; **proposal 2 (standing grader-admission counter with a filler control) → the V9 counter (`LOG.md` rounds 44–45; `corpus/QUALITY.md` Q33)**; proposal 3 … → the round-62 class survey. **No still-unimplemented proposal remains in that file; none mined this round.**

Each of that sentence's three citations is contradicted by the lane's own bytes:

1. **Q33 is a different criterion.** `corpus/QUALITY.md:692-695`: Q33 is "a kill-direction
   cell carried from another round's campaign into this round's mutant table is re-derived
   from that campaign's own recorded reference/mutant outcome" — nothing about an admission
   counter or a filler control. The criterion that actually cites this proposal is **Q44**
   (`corpus/QUALITY.md:1170-1172`), and Q44 says the opposite of the lesson: *"This mines
   proposal 2 of `considerthese/2026-10-26.md` (opened 2026-10-30) … **It adopts the
   criterion, not a claim that the proposed standing TB2 counter has been implemented.**"*
2. **V9 is per-round and dies at r46.** `grep -ln 'V9' plans/*_c2_verify.py` → exactly four
   files: `round42_c2_verify.py`, `round43_c2_verify.py`, `round44_c2_verify.py`,
   `round45_c2_verify.py`. `grep -c 'V9' plans/round46_c2_verify.py` → **0**. It is a leg of
   four per-round copies, not a consolidated standing tool.
3. **The LOG citation points at the wrong round.** `grep -n 'V9' LOG.md` → one hit only,
   line 1283, inside the **Round 42** section (`## Round 42` at LOG.md:1278) — not "rounds
   44–45".
4. **The committed filler package exists but is wired to one per-round file.**
   `find plans -maxdepth 2 -iname '*filler*'` → `plans/filler46/` (with `entry.md`,
   `receipt.txt`, `dry-cases.txt`, `pkg-spec-filler.json`, `captures/`), and
   `grep -ln 'FILLER_LEGS\|filler46' plans/*.py` → **only** `plans/round46_c3_verify.py`.
   No counter after r46 exists at all (`ls plans/ | grep -E '^round(4[7-9]|5[0-9]|6[0-6])_.*(c2|c3)_verify'` → empty).
5. **The per-round copies are still 11.** `ls plans/ | grep -c '_c2_verify\.py'` → **11**
   (`round36_c2_verify.py` … `round46_c2_verify.py`).
6. **The lane's own earlier records already said so.** `corpus/lessons/round-45.md:108-110`
   ("not landed this round, carried to round 46"), `corpus/lessons/round-46.md:69-72` ("It is
   per-round, **not yet the single standing counter the proposal asks for**"),
   `corpus/lessons/round-48-verifier-spotcheck.md:50` ("mined, **stays open**"),
   `corpus/lessons/round-54.md:47-48` ("**No standing TB2 admission counter is claimed
   implemented.**"), and the wave seat notes
   `.ufo/waves/round-45/w1/R45Considerthese.md:28` ("`plans/tb2_grader_admit.py` **ABSENT**").
   The round-65 lesson line 47 is the lone outlier.

Consequence for this round: the R66 claims file's frontier step says "one `considerthese/`
item **if any qualifies**, is recorded in the lesson (see the wave's connector seat)". On
the round-65 lesson's reading, nothing qualifies and the frontier step is empty. On the
bytes, **exactly one item qualifies — item 2** — and the connector seat records it.

### Implementing-check command I would run

Non-implementation check (run today, observed):

```
grep -rn 'tb2_grader_admit' /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans \
      /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus \
      /home/vgpnk/Projects/shokunin/kengaku-shokunin/SCORECARD.md ; echo $?
```
→ `0` hits, `grep_exit=1`. (The seat's prescribed key-term check, run on the item's own
named artefact.)

Implementing-check a landed standing counter must pass — the acceptance command, stated
here and **not run** by this seat (the file does not exist):

```
python3 plans/tb2_grader_admit.py --lane .
```
must (a) exit 0 and print one admission verdict per admitted grader; (b) print
`FILLER refused` and exit non-zero against the committed filler package
`plans/filler46/` (the filler must stay red — a control that stops being red is not a
control); (c) be re-run at tip, i.e. appear as a row in `plans/round53-tipstate.json`'s
`rows` map alongside the existing `tip-receipts` and `routed-findings` rows; and (d) refuse
a receipt whose named spec/dry-table/probe digests do not match the committed bytes (the
r37 V2 hole).

---

## 4. One bounded proposed move (connector role)

**Move:** promote the item-2 gap from "a per-round fix" to "a class fix" by making the
round-66 strict-mode value-binding reusable, and record proposal 2 as this round's
`considerthese` item.

**Evidence (all measured this round):**

- R66-C2 fixes the *R65 instance* of a class defect: `plans/round65_c1_sqlite_probe.py:649`
  (`receipt_failures`) checks **field presence and self-consistent text only** — the
  round-65 lesson's own Mistakes row 5 records the reproduction ("a hand-written 2540-byte
  receipt with no compile, sandbox or driver run → `--check-receipt` rc 0").
- R66-C1 already owns the *stronger* half of the same binding, in a different file:
  `plans/round66_c1_tensor_probe.py:239-275` re-derives three of its four value checks from
  committed bytes — `PROBE sha` against `probe_sha()` (245-246), `case_sha` against
  `sha256()` of the committed case file (266-269), `junit_sha` against the committed junit
  bytes (270-272); only the `GRADER sha256=` line is a literal comparison to the pinned
  constant (243-244).
- The "re-run at every tip" half of proposal 2 is measurably absent for the very receipts
  this round relies on. Running `plans/tip_receipts.py`'s own functions over the lane:
  **46** candidate receipts under `corpus/evidence`, **13** covered, **33** skipped with
  `reason=no-committed-re-run-command`. Every R55+ probe receipt is skipped, including
  `corpus/evidence/round65/sqlite-gcov-probe.txt` — the committed receipt R66-C2's strict
  mode must accept — and the **R66 receipt of record
  `corpus/evidence/round66/tensor/receipt.txt` is not even a candidate**, because the
  tool's `CANDIDATE_RE = probe.*\.(?:txt|log)$` needs "probe" in the basename and its
  stem (`receipt`) resolves to no `plans/*.py`. Confirmed by running the tool:
  `python3 plans/tip_receipts.py --lane . --list` prints
  `receipt corpus/evidence/round65/sqlite-gcov-probe.txt skip reason=no-committed-re-run-command`.
  (The derivation failure is mechanical: receipt stem `sqlitegcovprobe` vs probe stem
  `round65c1sqliteprobe`; `STEM_RE = [^a-z0-9]+`, so they differ.)

**Compatible synthesis:** the two halves already exist in this round's own frozen code —
R66-C2's value-binding (`--strict`) for receipts and R66-C1's byte-re-derived
case/junit/probe digests for cases. Proposal 2 asks for exactly one artefact that carries
both and is re-run at tip for every admitted grader receipt. A single standing admission
counter that (i) re-derives each named value from the committed bytes it names, (ii) binds
the committed filler package that must stay red, and (iii) is re-run at tip for every
admitted grader receipt — **including the R66 tensor receipt, whose basename must therefore
carry "probe" or be mapped explicitly** — would be that artefact.

**Affected axes (declared this round: coverage C1, operability C2; seat judged on coverage,
operability, calibration):**

- **operability — improved (expected, not measured):** one class gate replaces eleven
  per-round admission copies and closes the tip-re-run hole for the R65 and R66 receipts of
  record. R66-C2's strict mode remains the per-round instance and is not narrowed.
- **calibration — improved:** the round's own lesson currently records proposal 2 as
  implemented on three wrong citations; recording it as still open, with the measured
  absence (`0` hits, 11 copies, 33 skipped receipts), is what makes the frontier step
  honest rather than empty.
- **coverage — not harmed and not claimed:** C1's predicate, frozen table and five cases are
  untouched; the L0 cap (`kengaku | round-25/33/51`) stays open; no coverage movement is
  asserted by this seat.

**Risks:**

- *Scope creep:* a standing counter that re-runs every admitted grader at tip touches 18
  `tb2-*-grader.md` entries and 20 `corpus/evidence` receipts — larger than one round.
  Mitigation: land it as an *added* tool over an explicit, named roster, never by editing a
  frozen counter or a committed receipt.
- *False-green risk:* a standing counter that aggregates verdicts can launder a per-round
  failure into an aggregate pass — the very pattern the r52/r57 lessons record
  (`laundered=2`, `MISSING 0`). Mitigation: per-grader verdicts must be printed
  individually, and the committed filler must stay red in the same invocation.
- *Tip-re-run cost:* re-running the admitted graders at tip is slower than a receipt
  byte-compare; a timeout that is not counted as a failure reintroduces a silent skip.
- *Blast radius of a rename:* renaming `corpus/evidence/round66/tensor/receipt.txt` to
  carry "probe" would change the path named in the frozen R66 claims file
  (`plans/round-66-claims.md`, "the receipt at `corpus/evidence/round66/tensor/receipt.txt`").
  **That file is frozen and no seat may edit it** — so any tip-mapping of the R66 receipt
  must be an *added mapping row* in the standing counter, not a rename of a frozen path.
  This seat proposes only; it edits nothing.
- *Precedent risk:* the per-round `V9`/`V13` legs are digest-pinned by their own rounds'
  counters; a consolidation must import them by path (the r43 precedent) rather than
  re-implement their rule, or the re-derivation contract (Q33/Q44) breaks.

**Verification (for the main agent — NOT run by this seat; stated so the claim is not
over-read):**

1. `grep -rn 'tb2_grader_admit' plans corpus SCORECARD.md` — must become non-empty when the
   tool lands (today: 0 hits, exit 1).
2. `python3 plans/tb2_grader_admit.py --lane .` — exit 0 with one verdict per admitted
   grader, and a **red** verdict against `plans/filler46/`.
3. `python3 plans/tip_receipts.py --lane . --list` — the skip line
   `receipt corpus/evidence/round65/sqlite-gcov-probe.txt skip reason=no-committed-re-run-command`
   must disappear, and `corpus/evidence/round66/tensor/receipt.txt` must appear as covered.
4. `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt`
   must still print `PREDICATE R66-C1 pass` (exit 0) — the standing counter must not narrow
   C1's predicate, and C1's frozen bytes must be untouched.
5. `python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round66/red/fabricated-r65.txt --strict`
   must still exit 1 with a `CHECK defect:` finding, and the committed R65 receipt must still
   exit 0 under `--strict` — R66-C2's kill rules must survive any consolidation.
6. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain` — the landing
   must add only new files (or explicitly dated, append-only edits to a named file); no
   frozen case, frozen table or committed receipt may change.

---

## 5. Item-by-item verdict summary

| # | seat item | verdict |
|---|---|---|
| 1 | PROVINCE.md overlap scan | **Done, 1 hit.** `kumitate-shokunin/PROVINCE.md:38` (`bwrap`) — not sibling-owned ground (kumitate's own census-selftest portability arm). Near-misses at `kagi:29` and `kaidoku:352,356,358` judged and recorded. Zero hits for torch / tensor.parallel / gloo / sqlite.*gcov / kv-store / grader. |
| 2 | Sibling `plans/`+`corpus/` scan | **Done, 0 hits.** No sibling executes or owns this grader. The 3 repo-wide out-of-lane mentions are kengaku's own material (fleet report; souji's scan quoting kengaku's `HEAD:corpus/lessons/round-52.md:56`). Only kengaku's `SOURCES.md` holds the row (S183). |
| 3 | `considerthese` selection | **Done, one pick.** Latest file `2026-10-26.md`; three "proposals only" items; 1 and 3 implemented; **2 not implemented** (0 hits, file absent, 11 per-round copies, filler wired to one file) → **proposal 2 selected**, quoted verbatim above, with the implementing-check commands. The round-65 lesson's contrary claim is reported with its three broken citations, not edited. |
| 4 | Write `W/SiblingOverlap/findings.md` | **Done** (this file); receipts in `W/SiblingOverlap/receipts.txt`. No `considerthese/` or lane file edited. |

**Tooling:** none installed. Nothing beyond the pre-existing host toolchain was needed;
no pacman, no uv install, no network fetch.
