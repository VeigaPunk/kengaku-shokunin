# Round 80 — kengaku (hyaku run 15, attempt 1, 2026-11-04)

Base `dce7c275381c669e6489f1b795b1505d0824c262` (round-79 verifier spot-check). Freeze
`af51132d8919cedd14d3d3407ae5abc966d5d427`; freeze amendment A1
`6250e94b2adaff8cd22d32f7ab45024f092e3235` (the receipt block is the instrument's verbatim stdout,
`REV <commit>` lines stripped, and the gate compares the whole block). Two claims, both frozen in
`plans/round-80-claims.md` before any receipt was minted: R80-C1 (coverage) and R80-C2 (calibration).
One v1 wave, 14 seats.

## Gate

- **S258 admitted** for the lane's own located-replay instrument set — the six receipts
  `corpus/evidence/round80/<member>-probe.txt`, the frozen table `plans/round80_probes.json` and the
  gate `plans/round80_c1_located_replay.py`. `own-work` is a listed contract kind (CORPUS.md,
  SOURCES contract v1) and tier A because every byte is re-runnable in-repo. Opened 2026-11-04 UTC
  by L1 `KengakuR80`. Located quote, `corpus/evidence/round80/cancel-async-tasks-probe.txt` line 1,
  **"# tb2 cancel-async-tasks grader probe (round 80 re-mint)"** (8 words), the frozen subject shape
  every receipt starts with. Receipt sha256s: `cancel-async-tasks 7923b6dc…`,
  `chess-best-move b32f4b37…`, `distribution-search fd337d12…`, `largest-eigenval 9179d62d…`,
  `openssl-selfsigned-cert 08c10b0d…`, `protein-assembly 82b910af…`. Registry change: absent →
  S258 `mined`, recheck `90d`, used-by `corpus/lessons/round-80.md`, `SCORECARD.md`.
- **Reject candidate:** "a located replay is a container run." The receipts are in-process offline
  replays of the stored grader bytes; S256 records that a Terminal-Bench 2.0 run is a containerized
  run, and `PROVINCE.md` refuses the runtime surface. Flip: a container-run receipt that names the
  task and the container image, with the image digest pinned.
- **Reject candidate:** "the re-minted numbers are the historical numbers." Two members diverge:
  `largest-eigenval`'s `eig-bare-speed-s10` is `predicted=U` (the probe itself marks it
  observed-only) and now observes `F` where the historical receipt recorded `P`;
  `openssl-selfsigned-cert`'s tip derivation no longer predicts the two historical mismatches
  (`perm-loose`, `key-1024`), so its fresh block has `mismatches=0` where history had 2. Both
  receipts carry `HISTORICAL-DIVERGENCE <n>` and keep the historical receipt's sha; the gate reports
  `historical=differs` and never counts a divergence as a pass. Flip: a re-mint whose block equals
  the historical observation lines and the gate prints `historical=same`.
- **Assimilation: none.** `/home/vgpnk/Projects/shokuknow/merge/kengaku/` stays unadopted; the mass
  id drift is open at L0 `kengaku | round-54`. `considerthese/2026-10-26.md`: proposal 1
  (routed-findings burn-down) is used again for the six V ids; proposal 2 (`tb2_grader_admit`) stays
  open; proposal 3 (batch sweep + class histogram) is now unblocked by the 24 located members and is
  named as round-81 work, not implemented this round.

## Census and instrument readings

- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` at round start:
  rc 0, 249 registry rows, 26 `W04` warnings (`corpus/evidence/round80/census-before.txt`).
- R80-C1 before (`corpus/evidence/round80/c1-before.txt`, measured at `dce7c275`): six
  `RECEIPT-UNTRACKED`, `DEFECTS n=6`, `located=0 reproduced=0 ledger_flipped=0`, rc 1.
- R80-C1 batteries (`corpus/evidence/round80/c1-selftest.txt`, `c1-mutants.txt`, three
  `c1-control-*.txt`): `SELFTEST cases=16 red=14 failures=0`, `MUTANTS real=6 killed=6 survived=0`,
  every control `target_reached=False` (flip-ledger 138 defects, header-only 126, copy-observations
  2 with `REPRODUCTION-MISMATCH`).
- R80-C2 before (`corpus/evidence/round80/c2-before.txt`, at `dce7c275`): six
  `DEBT-UNREGISTERED`, `INDEX … indexed=no`, `DEFECTS n=7`, rc 1.
- R80-C2 batteries (`c2-selftest.txt`, `c2-mutants.txt`, `c2-control-presence.txt`):
  `SELFTEST cases=9 red=8 failures=0`, `MUTANTS real=4 killed=4 survived=0`, control
  `target_reached=False`.
- Reason histogram unchanged this round: `unattempted` 57, `candidate-library-required` 3,
  `browser-required` 2, `vm-required` 1, `external-db-required` 1. The six flips do not touch an
  unexecuted reason; they move debt into `executed`.

## Mistakes

- **M80-1 · class `unverified-reproducibility-claim` · evidence `corpus/lessons/round-79.md`
  §Wave findings ("All six `executed-unlocated` probes are re-runnable today") · captured-by
  `none` (no criterion required opening each probe's entry path on this host) · fix
  `plans/round80_probes.json` + `plans/round80_c1_remint.py`.** The round-79 lesson asserted all six
  probes re-run today; on this host `python3 plans/tb2_grader_probe.py` died with
  `ModuleNotFoundError: No module named 'Bio'` (observed 2026-11-04 04:11, first smoke run), so the
  protein replay was not runnable as written. The fix records each probe's interpreter prefix in the
  frozen table (`uv run --no-project --with biopython python3` for protein) and the driver/gate both
  use it; the fix can fail — remove the `prefix` from the table and the protein leg dies with the
  same `ModuleNotFoundError`, which the gate reports as `REPRODUCTION-EXIT`.

- **M80-2 · class `historical-observation-drift` · evidence `corpus/evidence/round59/openssl-probe.txt`
  versus `corpus/evidence/round80/openssl-selfsigned-cert-probe.txt` · captured-by the R80-C1
  historical-divergence leg (`plans/round80_c1_located_replay.py` `DIVERGENCE-UNNOTED`) · fix: keep
  the historical receipt and its sha, mint the instrument's actual stdout, and state
  `HISTORICAL-DIVERGENCE <n>`.** The round-59 receipt records two prediction mismatches
  (`perm-loose`, `key-1024`) and `PREDICATE R59-C1 fail`; the tip's instrument predicts and observes
  `P/F/P/P/P/P` for both (its derivation was corrected after round 59), so the fresh block has
  `mismatches=0` and `PREDICATE R59-C1 pass`. The fix can fail: delete the divergence line and the
  gate prints `DEFECT DIVERGENCE-UNNOTED` (`corpus/evidence/round80/c1-selftest.txt` case
  `divergence-unnoted`).

## Corrections (round-79 spot-check routed ids, discharged here)

- **R79-V1** — the round-79 report claimed the retired `round78-c1` gate's verdict was re-verified in
  `gates-clean.txt`; that block printed `SETUP unresolved revision 'worktree'` / `EXIT 1`. The
  spot-check's second repair option is taken rather than a prose retraction:
  `python3 plans/round78_c1_class_member_ledger.py --lane . --rev 148801a6` prints
  `PREDICATE R78-C1 pass`, committed with a stamp at
  `corpus/evidence/round80/v1-r78-c1-at-148801a6.txt`.
- **R79-V2** — round-79's Sources & frontier said "25 `W04` … unchanged in both". Wrong: the census
  receipts report **25 before, 26 after** (the `diff` adds S256's duplicate-URL line); rc 0 in both.
  W04 is a warning class, not a failure.
- **R79-V3** — round-79's "13 rows said a bare `executed`" is off by one. At the round-79 base
  `660ec0b9`, the `SKILL.md` grader table has 12 bare `executed` cells plus one `recipe-unexecuted`
  (`container-image`) — i.e. **13 unquantified** rows, not 13 bare-executed rows. (At this round's
  base `dce7c275` all 16 cells are already quantified: round 79 landed them.)
- **R79-V4** — R78-D4's S254 anchor is re-stated: the 15-word quote spans **capture lines 2322–2326**
  of the tracked capture `corpus/evidence/round78/sources/git-status.html` — two sentences
  ("Show untracked files." at 2322; "The mode parameter is used to specify the handling of untracked
  files." at 2326) — not one sentence at line 2322. (The round-79 lesson named a
  `corpus/evidence/round79/sources/git-status.txt` path; that file is absent.)
- **R79-V5** — **S256 duplicate-URL kept**: S256 repeats S180's URL for a distinct scope (the
  harness's own execution model, which grounds the R79 blocker taxonomy and this round's
  replay-surface limit). Scoping it out would leave that taxonomy unsourced; the new `W04` is stated
  in this lesson's census reading instead of hidden.
- **R79-V6** — the round-79 after receipts carried no revision stamp. Both counters are re-minted at
  the round-80 tip by `plans/round78_restamp.py` (`plans/round80-restamp.json`):
  `corpus/evidence/round80/r79-c1-after.txt` and `r79-c2-after.txt` each carry
  `LANE_TIP`/`TOOL`/`TOOL_SHA`/`WORKTREE`/`COMMAND`/`EXIT`.
- All six ids are `corpus/routed-findings.jsonl` rows `R79-V1`…`R79-V6`, gated by
  `plans/round80_c2_spotcheck_debt.py`.

## Wave findings (amended after w1)

_(filled in after the wave settles; the L1 integrates every finding that changes committed bytes)_
