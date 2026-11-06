Author: kengaku (L1 KengakuR99)

# Round 99 — bn-fit-modify grader replay and row-scoped provenance bindings

BASE `2233a661`; P0 `f9d29eb3`; P1 `e219e785`; P2 `b08a0192`; F `24a5a555`; C = T `f72a8bc7`;
receipts `23d58036`; integration `fc65aa9a`; harm `182a40bc`; dated corrections after T `b71b990a` (word counts, M3) and `3fdecf31` (registry selftest cells, M5).
Frozen predicates: `plans/round-99-claims.md`. Receipts: `.ufo/waves/round-99/L1/c1-tip.txt`, `c2-tip.txt`,
`c1-base.txt`, `c2-base.txt`, `freeze-tip.txt`; controls `.ufo/waves/round-99/L1/controls/`.

## Gate

**Search.** Round-98 ConnectorOverlap §3 (`.ufo/waves/round-98/w1/ConnectorOverlap.md:91`) ranked
`bn-fit-modify` as the best leg count per unit cost among the unattempted members: 9 tests and pip-only
grading. The pinned tree listing (GitHub API, `2fd12b88:bn-fit-modify`) has 11 entries and 8 blobs. All
8 blobs were opened on 2026-11-06 between 10:28:43 and 10:28:48 -03, HTTP 200
(`.ufo/waves/round-99/L1/capture-time.txt`). The Dockerfile's dataset URL was opened the same minute.
It points at an unpinned `main`, and its bytes were byte-equal to commit `62ce2364`.

**Captures.** All are flat under `corpus/evidence/round99/tb2-bn-fit-modify/`, with `SHA256SUMS` and the
task's `task.toml` beside them, so the frozen anchor-digest gate binds the new rows by `url-task` (S339
binds by its row path).

**Stop rule.** One new member with a positive control, a no-work control, mechanism-specific negatives,
and the gaps located. No claim is made about any submitted solution. `.gitignore` was opened and not
captured (no byte of the grader or solution reads it).

| row | URL / access | located quote | decision / reason / flip |
|---|---|---|---|
| S334 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/bn-fit-modify/tests/test_outputs.py; 2026-11-06 | `tests/test_outputs.py:150`: assert p_value >= 0.001, ( (5 words) | mined, tier A: only column D is tested, by KS against hard-coded constants. Leads to C03, C13, C11/C12 and C07 |
| S335 | …/bn-fit-modify/tests/test.sh; 2026-11-06 | `tests/test.sh:22`: -w scipy==1.16.1 \ (3 words) | mined, tier A: python 3.13, pytest 8.4.1, pandas 2.3.2, scipy 1.16.1. Reward is 1 iff pytest exits 0 |
| S336 | …/bn-fit-modify/solution/solve.sh; 2026-11-06 | `solution/solve.sh:21`: learned_dag <- hc(samples) (3 words) | mined, tier A: the R/bnlearn positive control, run once offline. Its fit equals the grader constants |
| S337 | …/bn-fit-modify/instruction.md; 2026-11-06 | `instruction.md:20`: 3) Perform a causal intervention on Y, setting its value to 0.0. (12 words) | mined, tier A: the contract asks for Y = 0.0 in the sample, but no test reads Y (C03). The literal `to,from` header is ambiguous (C06) |
| S338 | …/bn-fit-modify/environment/Dockerfile; 2026-11-06 | `environment/Dockerfile:20`: RUN curl -fsSL "${BN_URL}" -o bn_sample_10k.csv (6 words) | mined, tier A: the input data comes from an unpinned branch of a personal repository |
| S339 | https://raw.githubusercontent.com/gdreiman1/t_bench_bn_dataset/62ce2364212a5f96278e9e5a83a3bde73abcc7e3/bn_sample_10k.csv; 2026-11-06 | `bn_sample_10k.csv:1`: "U","Y","R","D","M" (1 word) | mined, tier A: the dataset as of the pinned commit, byte-equal to `main` that day. C04 refits OLS on it. Recheck 90d (the upstream branch can move) |
| S340 | …/bn-fit-modify/task.toml; 2026-11-06 | `task.toml:29`: docker_image = "alexgshaw/bn-fit-modify:20251031" (3 words) | rejected, tier A: the prebuilt image is never pulled; a pinned venv models the grader side. Flip: pull the image and compare its verifier versions to GRADER_SIDE |
| S341 | …/bn-fit-modify/README.md; 2026-11-06 | `README.md:38`: Sampled data has 10,000 rows and follows the expected distribution for variable D (13 words) | rejected, tier B: a derivative of S334/S337 that no grader or replay byte reads. Flip: a claim about the README's own statements |

**Admit / reject for the closure spot-check:** admit S334 (A), reject S340 (A) and S341 (B).

**Registry old→new.** No existing SOURCES row changed. R99-C2 K6: `rows_changed=0` over its 12 rows, and
the diff from C onward touches only S334–S341. S334–S341 were added: 7 tier A, 1 tier B; 6 mined, 2
rejected. Rows went 325 → 333. There were no status, recheck or used-by changes to existing rows.

**Dated correction (after T, `b71b990a`).** The word counts of S334, S336, S337, S338 and S339 were typed
by hand at C and were wrong: 4→5, 4→3, 11→12, 5→6 and 5→1. They were recomputed as
`len(quote.split())`. `plans/anchor_line_check.py`: `live=5 cells=5` rc 1 at T, then `live=0 cells=0`
rc 0 after the correction (`.ufo/waves/round-99/L1/harm/anchor-line-T.txt`,
`anchor-line-corrected.txt`). See Mistake M3.

**Frontier.** Member `bn-fit-modify` moved from unexecuted to executed. In the ledger, executed went
42 → 43 and `file-artifact` went 33 → 34 of 76.

**Census.** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` was rc 0
at start (`L1/census-start.txt`). The end result is in `L1/census-end.txt`. The pre-append scratch
validation of the candidate registry, on a `git archive` mirror of P1, was rc 0 with 31 W04 warnings
(`L1/controls/candidate/sources-validate.txt`).

**Anchor re-verification (R99-C2).** Twelve existing rows are now bound by eight new three-column
`corpus/evidence/round<N>/PROVENANCE.md` files: S173–S177 (git v2.56.0 docs), S180 (TB2 README), S220,
S225 (WHATWG windows-1252 index), S270 (a 404 body), S285, S293 and S306. Each row's sha256 already
equalled committed bytes. Gate findings went 45 → 33 at T. The symmetric census shows that no outside BASE row's gate
findings or binding notes changed (`outside_removed=0 outside_added=0 outside_rebound=0`), and no new file
carries a URL. The census is finding-level, not row-level: deleting or rewriting an outside row that has
no gate note passes (CriticClaims F6, MutC2 M17), and 105 of the 313 outside rows carry no gate output at
all (F7).

**Assimilation:** none (inherited `merge/kengaku/` hold, L0 `kengaku | round-54`).

**considerthese:** `considerthese/2026-11-06.md` §1 proposal 2 (pick C1 members from the thinnest
ledger class). It was opened this round and its class arithmetic was re-derived at BASE from
`plans/grader-population-ledger.json`:

- `subprocess-exec` 15/45
- `crypto-credential` 4/12
- `shell-exec` 2/6
- `numeric-band` 4/10
- `filesystem-metadata` 4/10
- `file-artifact` 33/76

It landed as QUALITY Q86 (Mistake M4). Proposals 1 and 3 were not acted on.

**Ledger classification note (routed, not changed).** The ledger lists `bn-fit-modify` only as
`file-artifact`, yet its decisive test is a numeric-band KS threshold (C11/C12). The classes come from a
frozen `classes_source`, so the row is left unchanged and the discrepancy is routed.

## Round-98 routed defects — disposition

1. Provenance side channel (M4): R99-C2 K3 forbids a URL column in new provenance files. K7 is symmetric:
   removals, additions and re-bindings outside the population all count. In P2, the `url-channel`
   forgery re-binds S256 and fails K3/K4/K5/K7.
2. MutC2 survivors: M05/M18 (sha column unread) are killed by K4 (P2 `sha-column` fails K4 only).
   M11/M16 (a second line binding a byte-identical copy) are killed by K4/K5 (P2 `duplicate-line`).
   MutC1's counter self-integrity survivor is killed by C1 L11 and C2 K1-self (P2 `counter-edit` and
   `c2counter-edit` fail only that leg). The round-98 instruments themselves are untouched (Q79).
3. Receipt revision: both round-99 counters print `REV <full hash>` first (`L1/c1-tip.txt:1`,
   `L1/c2-tip.txt:1`).
4. L0 `kengaku | round-98` (coverage cap) and `kengaku | round-54` (assimilation hold) are carried and
   unanswered.

## Mistakes

| id | class | evidence | captured-by | fix / shown able to fail |
|---|---|---|---|---|
| M1 | prediction / stochastic verdict | `.ufo/waves/round-99/L1/dryrun/probe-dryrun-1.txt`: C11, a seeded draw at +0.03 sd, was predicted to pass but `test_sampled_data` returned F. The P0 arithmetic used the expected KS statistic and ignored seed noise: 49/200 seeds fail at that shift (`predictions-amendment-1.txt`) | Q74, partly: the dry run caught it before freeze. Nothing required a flip rate | C11/C12 became deterministic grids with exact statistics: D 0.0180, p 0.0030 passes; D 0.0200, p 0.00066 fails. QUALITY Q84. Able to fail: dry run 1 is the committed refutation |
| M2 | control harness / false pass | `.ufo/waves/round-99/L1/controls/c2-partial-run{1,2}.txt`: the `partial` forgery PASSED twice. `git rm` of an untracked copy failed (`fatal: pathspec … did not match`, in the runner's console output), so the fixture equalled the positive | none: the runner neither checked the step's exit status nor diffed the fixture against the positive. Caught by L1 reading the console | changed to `rm -f`. Re-run as `partial-fixed-run{1,2}`: fail, K4/K5, `still=1` (S306). QUALITY Q85 requires a tree-diff assertion. The invalid receipts stay committed and are labelled as invalid in the README |
| M3 | hand-typed word counts (the Q76 class, third recurrence after r93 W-7 and r94 M1) | at T `plans/anchor_line_check.py --lane .`: `live=5 cells=5` rc 1 (S334, S336–S339 `words:1`). At BASE: `live=0`, rc 0 | Q76: "a word count … is computed, never typed". It was not applied: the L1 did not run the gate before C | cells recomputed after T (`b71b990a`), live 0, rc 0. These are curation cells and no counter reads them, so the frozen C1 predicate at T is unaffected (C1 L10 reads the anchor-digest gate, not word counts). The fix departs from the claims file's "never repaired in round" clause and is disclosed here and in the report. Round-94 precedent: S299 was corrected after T. Able to fail: the T receipt above is the committed red |
| M4 | member selection against the lane's own evidence | `considerthese/2026-11-06.md` §1 proposal 2: the thinnest classes are `subprocess-exec` 15/45, `crypto-credential` 4/12, `shell-exec` 2/6 and `numeric-band` 4/10, yet round 99 picked a `file-artifact` member | none before this round | QUALITY Q86 (class arithmetic printed in the claims file). Round 100 planning input: ConnectorOverlap (c) |
| M5 | registry-cell convention not checked before C | ExecHarm (`.ufo/waves/round-99/w1/ExecHarm.md:30`): at T `plans/round82_c1_plans_registry.py --tip T` prints 4 new `DEFECT ROW-SELFTEST-UNBACKED` lines (round99-bnfit-probe, -c1-replay, -c2-rowscoped-bind, -provenance-build). BASE has 13 DEFECT and T has 17 (`.ufo/waves/round-99/L1/harm/r82c1-tip-*.txt`). The L1 battery missed this because the gate defaults `--tip` to `master`, so the battery's BASE and tip logs read the same tree | round82-c1 itself, which the L1 battery ran without `--tip`, so the run was not revision-scoped | selftest cells now open with `none declared —` (dated correction `3fdecf31`, SKILL.md only, read by no round-99 counter). Re-run: 13 DEFECT, set equal to BASE. Able to fail: the T receipt shows 17. Battery fix for round 100: pass `--tip REV` to every gate that defaults to `master` |

## Wave findings

Wave w1: 12 seats (ExecC1, ExecC2, ExecHarm, ExecKS, ReviewC1, ReviewC2, CriticClaims, MutC1, MutC2,
ScoutSources, ConnectorOverlap, ScribeLesson). Role mix: 4 executor, 2 reviewer, 1 critic, 2
mutation-tester, 1 scout, 1 connector, 1 scribe, so 5/12 seats were attack roles. The planner seat is
held by the L1, and ConnectorOverlap (c) supplied the bounded round-100 planning data-walk. The
validator refused `labrat` as a swarm role (`unknown_role`), so the KS hypothesis probe ran as executor
ExecKS. Reports are at `.ufo/waves/round-99/w1/<seat>.md`.

| seat / finding | observed verdict or defect | disposition |
|---|---|---|
| ExecC1 | counter pass at T, fail at BASE. Two probe reruns from `git archive` T have OBSERVATIONS byte-equal to the receipt. C03/C07/C11/C12 were rebuilt with its own code and seed and run under real pytest: C03 p 0.636 passes; C11 D 0.018001, p 0.003028 passes; C12 D 0.019995, p 0.000664 fails | C1 met, independently reproduced |
| ExecKS (hypothesis seat) | grid-shift edge 0.04869 ± 0.00004 sd. The marginal-only forgery passes 1998/2000 seeds (99.9 %, the KS α). The maintainer process passes 2000/2000. Both counters pass at T | knowledge entry figures confirmed. The edge is now stated as 0.0487 sd |
| ReviewC1 | V1–V5 pass: the hook is observe-only, the builder matches every `why`, reward is pytest's exit, and L1–L11 match the frozen text. An offline R re-run reproduced `learned_dag.csv` and `intervened_dag.csv` byte-identically, with fitted D equal to the constants. INFO: no `pytest-json-ctrf`. RESIDUAL: bnlearn 4.9 never exercised | no defect. Residuals carried |
| ExecC2 | its own 12/12 three-way equality check (capture = token = sha column) found one line per row and no URL. The per-row full gate diff BASE vs T, restricted to rows present at BASE, is exactly the 12 | C2 met, independently reproduced |
| ReviewC2 | V1–V9 pass. Population re-derived independently. Bindings are semantically right (S270 binds the 404 body the row itself anchors). S180/S225 twin ties resolve to the row's own round dir. No collateral change | no defect. O2 (the tie-break is safe only by today's data) carried |
| CriticClaims | F1: C1 L3 checks ancestry only, so a receipt whose `LANE_TIP` is rewritten to BASE still passes. F2: `located=1` is tautological. F3/F5/F9: SKILL cell, F..C file set and builder are unmeasured by any leg. F4: `SHA256SUMS` unpinned. **F6: C2's K7 is finding-level, not row-level** — deleting or rewriting an outside row with no gate note passes. F7: 105 of 313 outside rows carry no gate output. F8: a 4th column with a scheme-less URL passes K3. F10: "freshness" (drift against live surfaces) is a questionable axis name for a binding claim. F11: the runners still run `set -u` only | claim wording corrected to "finding-level" in README, SCORECARD and this lesson (not in the frozen claims file). All routed to round 100. F10 recorded as a disagreement for the operator and closure |
| MutC1 | 40 mutants: 30 killed, 10 survived. M04b (LANE_TIP → BASE, = F1); M11 (another member loses a class); M13/M14 (a correctly bound SOURCES row added or one removed: L10 is flag-only); M26 (LEG_ORDER swap); M31 (an extra file); M32 (SKILL cell); M33 (claims candidate sha); M34 (`mismatches` field); M38 (rev gate edited — C2 K1 catches it) | routed: successor legs for receipt-run identity, the F..C file set, and the new-row count |
| MutC2 | 24 mutants: 18 killed, 6 survived. M08 (fabricated id S999); M11/M12 (a 4th column); M16 (an outside row's unparsed token); M17 (deleting an invisible outside row, = F6); M21 (self-referential K1 neuter) | routed: a row-level census (SOURCES line equality for every BASE row), exactly three cells per line, and an id must exist in SOURCES |
| ExecHarm | 22 checks BASE vs T. No green→red from candidate bytes except round82-c1's 4 new `ROW-SELFTEST-UNBACKED` lines. The round-98 C1 counter fails at later revisions by construction (L7 set equality) | the r82c1 lines are fixed by dated correction `3fdecf31`; the DEFECT set now equals BASE's (M5). The r98-C1 design note is routed |
| ScoutSources | S334–S341 re-opened live: 8/8 agree (HTTP 200, sha, quote at the stated line). The dataset's unpinned `main` is still byte-equal to `62ce2364`. All 12 C2 rows were re-opened upstream and the live sha equals capture and provenance. Census rc 0. SS-18: the C1 predicate is blind to anchor line and word cells. SS-11: S225's "pointer 226" label slip predates this round | agree 19/19 on bytes. SS-18 is the M3 class (routed: a successor C1 leg runs `anchor_line_check` on new rows). SS-11 routed as a dated correction for a later round |
| ConnectorOverlap | (a) no sibling replays bn-fit-modify or uses row-scoped provenance. (b) C1/C2 bytes are disjoint: removing C2's files leaves C1's rows with 0 findings, and gate 45 = 33 + 12. (c) `min_class` is a three-way tie at 0.333 (crypto-credential 4/12, shell-exec 2/6, subprocess-exec 15/45). The cheapest thin-class candidates are cobol-modernization, extract-elf, adaptive-rejection-sampler, dna-insert and dna-assembly. 9 more anchor findings (digest-wrong-capture) clear with one three-column line each (measured 33 → 24) | round-100 planning input (Q86) |
| ScribeLesson | 23 items checked against receipts and recomputed. No correction changes a number, vector or verdict. Clarifications: C03/C04 are seeded draws (state flip rates, Q84); sd 14.09165 vs the grader's 14.0916; C05's row-names default vs the maintainer's explicit `row.names = FALSE`; C04's shift is +22.59 (1.48 sd); the lesson header must list both dated corrections | applied to the knowledge entry and the lesson header |
