# Round 54 — round-53 spot-check debt coverage

Axes: novelty, calibration. Documentary scout mapping only; no score/admission judgment or counter execution. Read `plans/round-54-claims.md` in full and `corpus/lessons/round-53-verifier-spotcheck.md` items 1–10. Paths below are lane-relative unless explicitly fleet-relative. Observations are a mid-wave snapshot, not proof of final integration.

| R53 item | Debt | R54 artifact addressing it | Evidence status / remaining gap |
|---|---|---|---|
| 1 | Coordinated internal history forgery can preserve FREEZE/ORACLE agreement; C1 integrity not proven. | Frozen `plans/round-54-claims.md`, Claim 1: `plans/round54_c1_anchor.py` BINDING, ATTESTATION, EXTERNAL PIN, CONTROLS; target bundle `corpus/evidence/round54/anchor/{claims.ots,header.bin,anchor.json,block-explorer-*.json}` and `c1-after.txt`; internal-only negative control. | Addressed by the registered external-anchor construct, **not certified closed by this scout**. The claim requires confirmed Bitcoin attestation, ≥2 agreeing fresh independent explorer receipts and pre-scoring time; pending proof is explicitly insufficient and kills the claim if it cannot confirm. Full after-run success remains for the anchor/counter seats and outside closure. |
| 2 | Selected `--selftest`/`--help` argv can launder a failing entry; inherited git config contaminates worker exits. | Frozen Claim 2: `plans/round54_c2_entrytruth.py` LEDGER/EXEC/ENV legs, `plans/round54-entrytruth.json`, builder `plans/round54_build_entrytruth.py`, controls `plans/round54_c2_controls.py`. Receipts `.ufo/waves/round-54/claims/c2-route-r53.txt`, `c2-route-closed.txt`, `c2-env-poison.txt`. | Observed closed-route receipt lines 8–16: forged green entry declaration yields `LAUNDERED fixture-gate declared green, entry exit=1`, `laundered=1`, predicate fail; truthful control lines 1–7 passes. Poison receipt lines 1–3 says inherited env `LEAKED`, hermetic env `BLOCKED`, control holds. These are retained fixture receipts, not this seat's reruns or proof of every laundering variant/full 78-row execution. |
| 3 | Never-read is not never-examined: earlier machine receipts contain task names; the R53 blocklist is narrow. | **Not addressed this round as a new never-examined guarantee.** Frozen claims introduction explicitly says neither claim re-labels any TB2 test; R54 concerns externally anchored freeze and entry-truth execution, not a broader exposure census. | Debt is honored through scope/wording restraint, not repaired retrospectively. No inference from R54-C1 success to unseen-task novelty is warranted; R53's narrower finding remains. |
| 4 | R53 mutation detectors incomplete: C1 20/42 killed (22 witness-bearing survivors); C2 28/69 in wave 1; proposed augmentations were not post-score rule edits. | `.ufo/waves/round-54/build_spec_w1.py:587–641` assigns M1C1Mutants (≥10 C1 mutants), M2C2Mutants (≥10 C2), M3BuilderMutants (≥6 builder), M4R52FixMutants (≥6 E3 repair); intended outputs `w1/<seat>/mutants.md` plus the specified patches. | **Assigned attack coverage, not complete debt discharge.** A glob over `w1/M*` returned no published mutation deliverables at inspection. These batteries target R54/E3, not a demonstrated re-kill of all old R53 survivors; no frozen R53 detector edit is claimed. Actual survivor tables and detector receipts remain necessary. |
| 7 | Carried R52 SELFTEST-UNBACKED negation repair and unfrozen K5/K7 controls were unlanded. | Proposed patched copy `w1/E3R52RegistryFix/round52_c2_registry.py`, `delta.diff`, `fixture-k5.md`, `fixture-k7.md`, `controls.json`, old/patched lane and selftest receipts. Independent review `w1/R4R52Fix.md`; M4R52FixMutants assignment. All wave paths have prefix `.ufo/waves/round-54/`. | **Addressed by a delivered proposal, not safely closed/integrated.** E3 report says old selftest 3/3, patched 6/6, old lane pass versus patched `SELFTEST-UNBACKED order-check`/fail. R4 review lines 1–10 says **DO-NOT-INTEGRATE**: existing green row falsely reddened (P1), K7 selftest survives removal of ENTRY-MISSING verdict logic due to unrelated MISSING failures (P2). R4 confirms the intended mixed-negation fixture is caught. Preserve both observations; proposal existence/selftest tally is not clearance. |

## Item 6 — coverage cap L0s remain unanswered in the queue

Source: fleet `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`.

Executed literal search with the grep tool:

```text
pattern: kengaku.*round-(25|33|51)
path: /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md
```

It returned four matching question rows: lines 72, 73, 163, 200. Line 73 is the separate novelty-verdict-conversion question, **not** one of the three coverage debts. The three requested lines are:

```text
72:kengaku | round-25 | Coverage cap (re-filed; first written only in .ufo/reports/round-24/kengaku.md:221 and never queued — lesson round-25 M23): does a surface explicitly retired to PROVINCE.md §Historical (absent, not governed, dated test -e receipt, now also marked ABSENT on its ## Surfaces row) still count as "declared-but-unresolvable" for the coverage rubric cap? Until ruled, kengaku coverage stays capped at 7.
163:kengaku | round-33 | decision packet: what committed evidence lifts the round-25 L0 coverage cap (SCORECARD coverage held at 7 across four rounds of real expansion)? Candidate classes: (a) a PROVINCE.md coverage-surfaces section with N newly resolving surfaces, (b) N further rounds of net-new admitted entries, (c) a rubric change the operator names, (d) the cap stays until the absent surfaces return.
200:kengaku | round-51 | three surfaces PROVINCE.md declared as resolving are absent on this host at 2026-10-28 and are now dated ABSENT with receipts: ~/Projects/webzites/repos/llm-wiki, ~/archive/bench-arena, ~/Projects/bounties/ledger/telemetry.jsonl. Restore them, or retire them from the lane province? Rounded around this round (probes only; no claim depends on them). Ledger row R51-R3.
```

Additional executed grep-tool search:

```text
pattern: ^kengaku.*(coverage|Coverage|round-25|round-33|round-51|RESOLVED|ANSWER)
path: /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md
```

Observed matches: 35, 72, 73, 163, 200. No matching kengaku answer/resolution row was returned; the three coverage entries remain questions without an answer annotation. **Conclusion limited to this queue:** still unanswered, consistent with the frozen R54 `Axis choice and the lowest axis` section; coverage stays 7 and is not claimed. This is not a claim that no off-queue operator communication exists.

## Evidence boundaries

High confidence in documentary mapping and quoted queue lines. Counter outcomes above are read receipts/peer reports, not independently exercised behavior. No exported contract was semantically traced; no LSP tool is exposed in this seat's tool inventory, and literal searches are documentary evidence only. No production edits, git/jj mutations, tests, network requests, installations, or scratch directories were made by this seat.
