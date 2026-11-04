# CriticR76 — sentence falsification

Axes: **coverage** (declared-surface universe) and **calibration** (what counts as discharge). Review only; no production edits, integration, judgment, installations, or git mutations.

## Findings

1. **HIGH — C1's unrestricted sentence BREAKS; the explicitly table/first-anchor-scoped predicate survives this particular attack.** `PROVINCE.md:117–139`, outside `## Surfaces`, declares a separate `### Core` table under `## Province map`. Its introduction literally says **“Surfaces that resolve today, each with the check actually run and its result:”**. Concrete omitted surface: `plans/attrib_probe.py`, row “Attribution instrument + frozen tables” at line 132, declared present with a sha256. Another is `~/.local/share/ds-flash-shim/shim.py` at line 135. Both existed when probed. `table_rows()` in the frozen C1 counter stops at the next `## ` heading after the first `## Surfaces`; neither declaration enters its eleven-row census. This is not merely a historical URL mention: the Province map explicitly calls itself a supersession of the old Surfaces table (lines 119–122). Also `PROVINCE.md:114` declares `~/Projects/ufo-fsd-alpha` present outside the table; `test -d` returned 0. Counterexample bytes and frozen parser are preserved in `CriticR76/province-at-freeze.md` and `CriticR76/c1-frozen.py`.
   - Smallest safe correction: recognize the **existing frozen body** as table-only and do not use its result as proof of the heading's “every surface PROVINCE.md declares” sentence. An actual all-declarations claim needs an explicit authoritative inventory including the Province map (or a clean supersession of those declarations), not only another row added to the old table. This is a scope distinction for the canonical judge, not authority for me to amend the frozen claim.

2. **HIGH — C2's discharge sentence BREAKS: re-derived values can be quoted in an explicit non-discharge.** Tested against measured counter sha256 `d6615bd299856d9a0fc257f2a32eaf4c2de1238bde0e821a63f45f6f78dc1cd8`, including the later evidence-at-close hardening. The exact cheap SCORECARD line was:

   ```text
   - R75-D3 NOT discharged; defect remains OPEN; quoted values: the final-rule before is 60 (4/36/20).
   ```

   D2 was likewise negated while retaining its stamp and `5d9a0ccc`. Every ledger `close` said `NOT discharged: defect still open`; `status` remained `closed`. Genuine committed closure text containing the defect ids satisfied the new evidence binding. The gate accepted all seven:

   ```text
   LEG D2 ok SCORECARD line with R75-D2, stamp e551cec208bc, 5d9a0ccc
   LEG D3 ok SCORECARD line with R75-D3, total 60, split 4/36/20 at 43255758
   SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0
   PREDICATE R76-C2 pass
   NEGATED_GATE_RC 0
   ```

   Evidence: `CriticR76/negated-discharge-receipt.txt`, `negated-scorecard.txt`, `negated-ledger.jsonl`, `c2-measured.py`, `probe-driver.py`. D2/D3 legs check substring presence, not what those values assert; the ledger's human `close` text is not checked. The original frozen counter has the same presence-only D2/D3 tests. This is a false-positive discharge, not criticism of value derivation itself.
   - Smallest additional leg for this exact counterexample: fail when a discharge-bearing line or `close` explicitly asserts `NOT discharged`, `remains OPEN`, or `defect still open`. That narrow contradiction leg catches these bytes but is **not** a general semantic proof. The maintainable general correction is a typed correction record binding defect id, artifact/field, re-derived expected value, and explicit completion state, with consistency against the ledger; do not execute arbitrary ledger `check` strings as shell commands. Merely binding an arbitrary committed literal to close_commit does not supply this missing leg.

3. **HIGH — moving C1 counter does not reproduce the original freeze receipt.** Exact direct replay at `--rev fda63968` during the wave returned rc 1 with:

   ```text
   AGREE agree=8 disagree=3
   DEFECT STALE-TEXT 3 Served local model http://127.0.0.1:34113 asserts 'identity re-probed' while absent
   ```

   Original freeze receipt instead has `AGREE agree=9 disagree=2` and no row-3 defect. The live counter acquired two stale-text phrases and a whole-row scan; Amendment A4 subsequently documents the changed rule and regenerated before receipt. Thus this divergence is explained by counter evolution, **not host drift**. Preserve the distinction: an amended instrument's before-output is not the original frozen instrument's before-output. See `CriticR76/c1-moving-worktree-rerun.txt` versus `c1-frozen-before.txt`. Smallest correction: retain separately labeled original and amended before receipts with their counter revisions; do not overwrite their provenance or treat A4 as the original predicate.

4. **INFO — exact frozen before controls reproduce.** To isolate concurrency from actual before-state drift I loaded both counter files and receipts directly from freeze `42fad4827797e540c60a00821d3f2f5c18539632` and replayed base `fda63968f29f8f58dc2b28831acac879405b8326`. Both emit functions returned **1**, as expected for failing before states; both full receipt diffs were empty, including stamps. C1: `AGREE agree=9 disagree=2`. C2: `legs_pending=2 wrong=12`. The original claims prose's C2 `legs_pending=0 wrong=14` is inaccurate; later Amendment A1 explicitly corrects it. No unexplained frozen-byte before divergence was found.

## Commands and execution evidence

All lane paths below resolve under `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; scratch was `/fast/scratch/hyaku/kengaku-r76/CriticR76`.

- `python3 plans/round76_c1_surface_resolver.py --lane . --rev fda63968 --receipt /fast/scratch/hyaku/kengaku-r76/CriticR76/c1-before-rerun.txt` — rc **1**; moving-rule output quoted above.
- `python3 plans/round76_c2_defect_discharge.py --lane . --rev fda63968 --receipt /fast/scratch/hyaku/kengaku-r76/CriticR76/c2-before-rerun.txt --work /fast/scratch/hyaku/kengaku-r76/CriticR76/c2work` — rc **1**; `SCOPE ids=7 registered=0 closed=0 open=7 discharged=0 legs_passed=0 legs_pending=2 wrong=12`.
- `diff corpus/evidence/round76/c1-before.txt /fast/scratch/hyaku/kengaku-r76/CriticR76/c1-before-rerun.txt` — rc **1**, after the moving receipt was regenerated, only `< WORKTREE dirty` / `> WORKTREE clean` differed. This stamp-only difference is environmental, distinct from finding 3's original-freeze comparison.
- `diff corpus/evidence/round76/c2-before.txt /fast/scratch/hyaku/kengaku-r76/CriticR76/c2-before-rerun.txt` — rc **0** at comparison time.
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor fda63968f29f8f58dc2b28831acac879405b8326 42fad4827797e540c60a00821d3f2f5c18539632` — rc **0**.
- `test -d ~/Projects/ufo-fsd-alpha` — rc **0**. Python `Path.exists()` printed `OUTSIDE_TABLE_SHIM_EXISTS True` and `OUTSIDE_TABLE_ATTRIB_EXISTS True`.
- `python3 /fast/scratch/hyaku/kengaku-r76/CriticR76/probe.py` — driver rc **0**, gate rc **0** on final negating fixture. First fixture trial returned gate rc **1** because three defect ids were not in the selected committed evidence file; changed evidence_path to the actual round-75 closure, then all seven passed. No fabricated git history.
- `python3 /fast/scratch/hyaku/kengaku-r76/CriticR76/replay.py` — driver rc **1** after successful exact-frozen C1 replay (gate rc **1**, empty diff); stopped at C2 because frozen emit lacks a `work` argument (A2's known defect). No C2 invocation occurred in that failed step.
- C2 exact-frozen retry used Python Eval: import `CriticR76/c2-frozen.py`; replace only module `Path` construction of `/fast/scratch/hyaku/kengaku-r76/c2` with this seat's `S/'frozen-work'`; call `m.emit(L,'fda63968f29f8f58dc2b28831acac879405b8326',W/'c2-frozen-rerun.txt',probe=L)`. Returned **1**, full receipt diff empty. This redirection avoids writing another seat's/default scratch and changes no predicate or declared input. Frozen input bytes, both resulting receipts and diffs are retained under `CriticR76/`.

The fixture driver runs the real round-75 selftests through the C2 derivation, which printed `cases=8 red=7` and `arms=5`; I did not substitute those derivations. No standalone selftest exit-code claim is made. Python drivers preserved with evidence give exact fixture construction and library calls.

## Limits and conclusion

- **C1: BREAKS as the heading's all-PROVINCE sentence; the narrower frozen table-only body is not falsified merely by an outside-table declaration.**
- **C2: BREAKS as a claim that discharge itself is re-derived; the counter proves presence of re-derived literals and ledger metadata, and accepted an explicit negation of discharge.**
- Exact freeze before-state replay: **SURVIVES for both**, with the documented scratch-only C2 constructor redirection. Moving-counter C1 divergence is reported separately.
- Did not assess every other wave amendment, production after-state, or canonical Rust judgment. Live files and master advanced during review; saved source bytes and full receipts, rather than current line numbers or branch tips, identify the exercised counter. No production fixes proposed here were implemented.
- Self-check: accuracy 4/5 (stable receipts preserved; live concurrency required provenance separation); completeness 4/5 (all four assigned attacks covered; no exhaustive semantic verifier); clarity 4/5 (scope-vs-heading distinction explicit); actionability 4/5 (exact contradiction leg and broader limit supplied); conciseness 3/5 (extra replay provenance needed). No tool installs.
