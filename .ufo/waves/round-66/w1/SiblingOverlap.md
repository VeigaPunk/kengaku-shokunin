# SiblingOverlap — kengaku round 66, wave 1 (connector seat)

Read-only cross-lane overlap scan + one `considerthese/` selection. Full findings and
receipts: `.ufo/waves/round-66/w1/SiblingOverlap/findings.md` and
`.ufo/waves/round-66/w1/SiblingOverlap/receipts.txt`.
Nothing outside my seat dir was written; no `considerthese/` or lane file edited; no tool
installed.

## Key lines (15)

1. **Item 1 — sibling PROVINCE scan: 20 sibling `PROVINCE.md` files exist; exactly ONE hit.**
   `kumitate-shokunin/PROVINCE.md:38` (term `bwrap`) — **not sibling-owned ground**: it is
   kumitate's own round-73 census-selftest portability arm ("cap-run/bwrap gate children"),
   not a TB2 grader replay; kumitate owns OMP route resolution (kengaku `SKILL.md:3`).
2. **Per-term counts across all 20 sibling PROVINCE files:** `torch hits=0`,
   `tensor.parallel hits=0`, `gloo hits=0`, `bwrap hits=1`, `sqlite.*gcov hits=0`,
   `kv-store hits=0`, `grader hits=0` (command in receipts R2).
3. **Near-misses judged (extended scan):** `kagi-shokunin/PROVINCE.md:29` (`sqlite3`
   binary for kagi's own selftests) and `kaidoku-shokunin/PROVINCE.md:352,356,358` (REA's
   *catalog reader*, "not an integrity check") — **neither is sibling-owned ground** for
   R66-C2's gcov-instrumented, amalgamation-built `sqlite3` artefact.
4. **Ownership:** `kasegi-shokunin/PROVINCE.md:50` lists kengaku as "LLM evaluation and
   benchmarks" among lanes "reported, not absorbed"; no sibling claims the replay ground.
5. **Item 2 — sibling `plans/`+`corpus/` scan: `R3_FILES_WITH_HITS=0`.** No sibling lane
   names `torch-tensor-parallelism`, `tensor-parallel` or `offline-torch`; **no sibling is
   executing this grader** — the expected finding for a novel ground.
6. **Out-of-lane mentions are kengaku's own material, not sibling execution:**
   `.ufo/reports/round-53/kengaku.md`; `souji-shokunin/.ufo/waves/round-43/w1/R43connectorA.md:459`
   (souji's scan quoting kengaku's `HEAD:corpus/lessons/round-52.md:56`); its census copy.
7. **Registry:** only `kengaku-shokunin/corpus/SOURCES.md` names the grader (S183, 1 line) —
   no cross-lane registry collision. Word-boundary `gloo` = 0 outside kengaku; no sibling
   torch tree/venv; the only `*torch*` filenames elsewhere are `torCh` in
   "Consume**torCh**ecklist"/"Opera**torCh**ecks".
8. **Item 3 — file:** latest `considerthese/2026-10-26.md`; three "proposals only" items.
   Item 1 (routed-findings burn-down) **implemented** (`plans/routed_open.py:240` prints
   `routed_open=… oldest_round=…`); item 3 (class census + stability rider) **implemented**
   (`corpus/evidence/round62/class-survey.txt` `CLASS-CENSUS roster=89 … classes=16`,
   `EXECUTED-COVERAGE executed=17`; `R40RegradeSweep` at `corpus/lessons/round-40.md:31`).
9. **PICKED — item 2, verbatim (`considerthese/2026-10-26.md:44-49`, block sha256
   `760e57a9…`):** "**One standing TB2 admission counter with a built-in filler control.**
   … Proposal: a single parametrised `tb2_grader_admit.py` that digest-pins the spec, dry
   table and probe it reads (the r37 V2 hole), ships a committed filler package that must
   stay red, and is re-run at every tip for all five admitted graders. A counter that admits
   filler should not appear in a verdict cell as the admission basis."
10. **Implementing-check:** `grep -rn 'tb2_grader_admit' plans corpus SCORECARD.md` → **0
    hits, exit 1**; `python3 plans/tb2_grader_admit.py --lane .` → **exit 2** (file absent).
    A landed tool must exit 0 per admitted grader, print a **red** verdict against
    `plans/filler46/`, and appear as a tip row in `plans/round53-tipstate.json`.
11. **Contradiction found (reported, NOT edited):** `corpus/lessons/round-65.md:47` claims
    proposal 2 was implemented "→ the V9 counter (`LOG.md` rounds 44–45; `corpus/QUALITY.md`
    Q33)" and "No still-unimplemented proposal remains". All three citations are wrong:
    Q33 (`QUALITY.md:692-695`) is about kill-direction cells, and Q44 (`:1170-1172`) says
    "It adopts the criterion, **not a claim that the proposed standing TB2 counter has been
    implemented**"; `grep -n 'V9' LOG.md` has ONE hit (line 1283, inside the **Round 42**
    section at :1278), not rounds 44–45; and `grep -ln 'V9' plans/*_c2_verify.py` → only
    r42/43/44/45 copies, `grep -c 'V9' plans/round46_c2_verify.py` → **0**.
12. **Further confirmation item 2 is unimplemented:** 11 `_c2_verify.py` copies remain; the
    committed filler `plans/filler46/` is referenced by **only** `plans/round46_c3_verify.py`;
    no counter exists after r46; and `corpus/lessons/round-45.md:108-110`,
    `round-46.md:69-72` ("per-round, not yet the single standing counter the proposal asks
    for"), `round-48-verifier-spotcheck.md:50`, `round-54.md:47-48` ("No standing TB2
    admission counter is claimed implemented") already said so — the r65 lesson is the lone
    outlier.
13. **Proposed move (one, bounded):** make R66-C2's value-binding reusable rather than
    per-round, and record proposal 2 as this round's `considerthese` item. R66-C1 already
    holds the stronger half — `plans/round66_c1_tensor_probe.py:239-275` re-derives
    `PROBE sha` (245-246), `case_sha` (266-269) and `junit_sha` (270-272) from committed
    bytes, while `plans/round65_c1_sqlite_probe.py:649` checks text/presence only (the M-1
    fabrication class). Synthesis: one standing counter that re-derives named values from
    bytes, binds the red filler, and is re-run at tip for every admitted grader receipt.
14. **Second-order effect measured:** the "re-run at every tip" half is absent for this
    round's own receipts — `plans/tip_receipts.py`'s own functions give **46** candidates /
    **13** covered / **33** skipped (`reason=no-committed-re-run-command`), including
    `corpus/evidence/round65/sqlite-gcov-probe.txt` (the receipt R66-C2 must accept) and
    the R66 receipt of record `corpus/evidence/round66/tensor/receipt.txt`, which is not
    even a candidate (`CANDIDATE_RE = probe.*\.(?:txt|log)$`; stem `receipt` resolves to no
    `plans/*.py`).
15. **Risks / axis effect (expected, not measured):** operability improved (one class gate
    vs 11 per-round copies; tip hole closed), calibration improved (the round's own
    frontier step is currently empty because of the false "already implemented" record),
    coverage **not harmed and not claimed** (C1's frozen table/cases/predicate untouched,
    L0 cap still open). Key risk: `plans/round-66-claims.md` is **frozen** and names
    `corpus/evidence/round66/tensor/receipt.txt`, so any tip-mapping must be an **added
    mapping row**, never a rename of a frozen path; and a standing counter must import
    r42–r46's digest-pinned legs by path (the r43 precedent) rather than re-implement
    them, or the r52/r57 laundering pattern (`laundered=2`) returns.

## Files written
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-66/w1/SiblingOverlap.md` (this report)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-66/w1/SiblingOverlap/findings.md` (full findings)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-66/w1/SiblingOverlap/receipts.txt` (observed bytes, R1–R9)

Scratch `/fast/scratch/hyaku/kengaku-r66/SiblingOverlap` was created and is empty (no clone,
tree, venv, fixture or counter was needed); removed at yield.
