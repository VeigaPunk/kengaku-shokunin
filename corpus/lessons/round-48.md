# Round 48 — fence over-refusal repair under a v3 counter (R48-C1); TB2 polyglot-c-py admission under a Q40 counter (R48-C2) (2026-10-27, hyaku run 10)

L1 `KengakuR48` (planner seat). Frozen claims `plans/round-48-claims.md` (stage 1 `a543d920`). Baseline lane tip
`0f77f9b2` (hyaku run-9 wrap-up). One v2 wave, 64 seats (attack 41), dispatched inline via `w1.ready`
(`.ufo/waves/round-48/w1-dispatch.json`). WAVE-DONE was received for all 64 seats; seven settled seats left no report file (named below). Neither claim reached a committed stage-2 freeze; no admission or score change is asserted.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **A frozen requirement-tag set with no violating case makes a counter leg unsatisfiable** — r46's polyglot C3 froze `both-print` and `toolchain` tags without any case violating either; no amount of package work could satisfy V7. | `.ufo/waves/round-46/integrate/c3-landing.txt` (`V7 DEFECT … tags missing=['both-print', 'toolchain']`); mined from `corpus/lessons/round-46.md` Mistakes | **none** — Q24 checked junk controls but did not positively validate each leg's preconditions; the r46 stage-2 freeze also omitted the dry-run map | R48-C2's V15/V7 precondition check must reject the unchanged r46 table before scoring; only call the fix landed if a committed receipt shows the old table failing and a fully exercised table passing. |

## Gate

Sources opened directly by L1 on 2026-10-27; candidate source decisions below are not independent closure verdicts.

| candidate | L1 candidate decision | URL | accessed | located quote (≤25 words) |
|---|---|---|---|---|
| S166 — `tests/test_outputs.py` | ACCEPT as the primary scoring predicate for this claim: the committed pinned capture can ground the exact case table and the source was reopened at the same immutable commit | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py` | 2026-10-27 | `:27 “test_cases = [(42, \"267914296\"), (10, \"55\"), (0, \"0\")]”` (8 words) |
| Docker Hub tag `alexgshaw/polyglot-c-py:20251031` | REJECT for the claim that the image supplies the documented gcc/python versions: tag metadata identifies an image digest and size but publishes no installed package versions; flip only after digest-pinned manifest inspection or a version inventory at that digest | `https://hub.docker.com/v2/repositories/alexgshaw/polyglot-c-py/tags/20251031` | 2026-10-27 | `images[0].digest = “sha256:0f1c3b7816d70cf5551573fd6aeef76893f2ae3000be2419997b6871b5d987ed”` (2 JSON fields; no version field) |

The frozen C2 claim names S166 as its sourced basis, reopened by L1 on 2026-10-27. It is not admitted this round: the required hardened probe fails permitted stage-checks, and no stage-2 counter/receipt landed. S166 is not appended or otherwise changed.
Non-author spot-check: not yet available at filing. The scheduled closure should re-open at least the S166 admit and the Docker Hub reject; the L1 decisions above remain unverified by an outside reviewer.

## Claim evidence and verdicts


- **R48-C1 — calibration, unverified / not admitted; score 8→8 held.** Stage-1 freeze: `a543d92083557dd9b33ee674e9b99b03411f80af`. The v3 counter candidate and 120-fixture population exist only in seat evidence (`R48C1ExecCounter.md`, `R48C1ExecHonest.md`), not in a committed stage-2 tree. On a scratch clone of the freeze, the candidate counter measured the base fence as `HONEST fixtures=120 admitted=112 refused=8`, `PREDICATE R48-C1 fail`; the measured repair candidate in `R48C1ExecFenceA.md` admitted 120/120 honest fixtures and refused 20/20 refusal modules plus 12/12 sealed modules. The frozen control's `refused=9 minimum` did not reproduce: r46's nine were all caused by placeholder argv, and the re-authored base population yields eight refusals. The control still fails as required, but the mismatch is disclosed, not silently re-frozen. No stage-2 counter/pins/controls were committed, no clean-clone landing-tip run occurred, no frozen ≥12-mutant C1 battery was reported, and `R48C1ExecFenceB` did not produce a report. Thus the repair candidate is evidence, not a landed claim. Score unchanged; no capability row.
- **R48-C2 — coverage, not admitted; score 7→7 held (L0 cap remains).** Base evidence at r46 already fails V7/V8 (`.ufo/waves/round-46/integrate/c3-landing.txt`, REV `264b7757…`). At the r48 stage-1 freeze (`a543d920…`), the C2 counter candidate `--dry` reports V7 missing violations for `both-print`/`toolchain`; the controls are P10-disabled and fail. The case-author seat `R48C2ExecCases` left no report/artifact. `R48C2ExecProbe.md` establishes that the frozen `22b7779e…` candidate's allowed `--stage-check` fails 18/18 under the host's current thread load (`--nproc=48`) and its `mode="all"` path skips seed/recipe setup; no full probe run was made. Counter/control evidence is in `R48C2ExecCounter.md` and `R48C2ExecControls.md`; the new package is not verified at a committed landing tip. No stage-2 freeze, full probe run, score increase, or capability row.

- **Do-nothing control:** the base C1 fence fails its frozen 120-fixture honest leg (`112 admitted / 8 refused`). The C2 no-probe, filler and echo controls all print `PREDICATE R48-C2 fail` under the scratch candidate; the base case-table V7 defect remains. These are scratch control receipts, not committed stage-2 receipts.
- **Claim separation:** C1's fence/counter and honest population are disjoint from C2's probe/package/counter; no shared production path changed.
- **Round trend/outside review:** no admitted knowledge or capability (expansion unchanged); no lane corpus entry was found false or left unmarked (quality unchanged); L1's S166 and Docker Hub decisions are candidate gate decisions only, with no non-author spot-check before this report (discernment unchanged). The scheduled non-author closure remains required.
- **Tooling:** no tool installed or upgraded; no pacman transaction attempted.

## Considerthese mining

Proposal 2 in `considerthese/2026-10-26.md` (opened 2026-10-27): a standing TB2 admission counter with a built-in filler control. The cited evidence is real: the r36 C2 critic built a junk package that passed W1–W6 (`.ufo/waves/round-36/build/R36CritC2Counter.md:18-33,155-157`), and the r37 critic reports a ~2 KB inverse-prose filler package passing `checks=7 defects=0` (`.ufo/waves/round-37/build/R37CritC2Counter.md:8-14,32-42`). The r36–r39 verifier files remain per-round copies (`plans/round36_c2_verify.py`, `round37_c2_verify.py`, `round38_c2_verify.py`, `round39_c2_verify.py`; each has its own check count and CLI). This round's R48-C2 candidate remains package-scoped and does not implement the standing cross-package counter. The broader proposal remains open; require a parametrized counter, a committed filler-negative control, and re-run coverage of all five admitted graders before claiming it closed.

## Wave handoff

One v2 wave, 64 seats: connectors 4, critics 15, executors 10, mutation-testers 14, revenger 1, reviewers 12, scouts 3, scribes 4, sentinel 1. Attack roles (critic + mutation-tester + reviewer): 41/64. Planner seat: L1. Seven seats settled without a report file: `R48C1ExecFenceB` (last output ends during mount-proof mutant work), `R48C1ScoutPop` (last output ends during population-class reasoning), `R48C1HoMount` (last output ends during mount-fixture feasibility), `R48C1MutGit` (last output ends while drafting report), `R48C1MutExit` (final JSON names a missing report path), `R48C1RevClaim` (last output ends during mount-scope review), `R48C2ExecCases` (last output ends during candidate case-table amendment). `w1-results.json` carries no explicit error text/status for these seats; no error is fabricated. No residual call or second wave was dispatched.
