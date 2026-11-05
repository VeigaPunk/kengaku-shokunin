author: kengaku (L1 KengakuR91, hyaku run 15 attempt 1)

# Kengaku round 91 — lesson

Lane `kengaku-shokunin`, branch `master`. Frozen claims commit A `cd0c116e` (`plans/round-91-claims.md`, `plans/round91-cases.json`); instruments commit B `386184a6`; checker correction and pin regeneration B2 `b836a862` (made before any scoring, see Mistakes M3); receipt, ledger flip and sources commit C; the measured tip and the triage commit are named in LOG.md and the round report. Wave evidence: `.ufo/waves/round-91/w1/`.

## Gate

Candidates opened this round (CORPUS rule 1: each row written only after its source was opened here, with URL, access date and a located quote).

| candidate | decision | access | located quote and location | reason | flip |
|---|---|---|---|---|---|
| S281 `modernize-scientific-stack/tests/test_outputs.py` @ `2fd12b88` (member replay only) | **admit** (tier A, scope `member replay only`) | 2026-11-05, `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/modernize-scientific-stack/tests/test_outputs.py`, HTTP 200, 2330 B, sha256 `0c24195f…02a977`, byte-identical to the round-52 capture (`cmp`) | line 27: `assert "Station 101" in output, "Must output Station 101 results"` (10 whitespace-split words) | the captured module defines two named test functions (`def` at lines 11 and 46) over a staged `/app` script, CSV and dependency file; it is the sole source of the ten frozen predicted vectors (`plans/round91-cases.json`), so the claim rests on it | the pinned grader bytes change at `2fd12b88` |
| S282 `modernize-scientific-stack/tests/test.sh` @ `2fd12b88` (harness wrapper) | **reject** | 2026-11-05, same base URL with `tests/test.sh`, HTTP 200, 721 B, sha256 `e868c854…f0281`, byte-identical to nothing held before (first capture) | line 5: `apt-get install -y curl` (network install, 4 words) | the wrapper adds no grader semantics beyond `test_outputs.py` (S281), and its replay needs apt, curl and uv over the network, which the offline replay forbids | a claim about verifier-harness behaviour (reward.txt mapping, uvx exit semantics) opened as its own replay with the network legs pinned |

Round-start census (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`): exit 0, `kengaku ok`, 272 rows. Round-end census: recorded in LOG.md after S281/S282 landed.

## Mistakes

Class · evidence pointer · captured-by · fix. Each fix is named with the evidence it was shown against; fixes that are not yet able to fail are routed, not claimed.

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | **prediction-unit (round-90 M3 continued)** | `plans/round-91-claims.md` predicted legs/pins/selftest counts as bare numbers in places (C2 selftest `6` fixture cases; the C2 pin count `K`); the measured checker has 8 selftest cases and 16 pinned entries | the do-nothing and selftest runs, measured after freeze | counts predicted with their formula (`legs=10*2=20`); the C2 mispredicts are recorded as mispredicts in SCORECARD, not repaired in the frozen text |
| M2 | **frozen-text line-range error** | `plans/round-91-claims.md` (C1 Move) cites the grader's test functions at `lines 16–42` and `lines 45–48`; the fetched bytes define `test_modernized_code_runs` at line 11 and `test_dependency_file_exists` at line 46 (`grep -n '^def ' msts-test_outputs.py`) | this lesson's Gate, when the located quotes were checked | disclosed here and in the report; the frozen text is not repaired after freeze. The located quotes (lines 27, 29, 5) are the citation of record |
| M3 | **checker fixtures wrong, found by the checker's own selftest before any data** | at B `386184a6` the C2 selftest was 4/8: blob pins were computed as sha256 of content where git's blob id is sha1 over `blob <n>\0`; the "absent" fixture path existed in the fixture; the self-pin case never reached the self check (the pin mismatched at the git level first); the child process ran with `PATH` only | the selftest run (`SELFTEST … red-green-ok=4`), before the first measured revision | fixtures rewritten (`git_blob_id`, `plans91/missing.txt`, a stale committed checker at the self path, a two-commit anchor fixture), the child environment carries `HOME`, the pin ledger regenerated, and the corrected checker committed as B2 `b836a862` before any scoring. Disclosed: the pinned commit moved from B to B2. Result at B2: selftest 8/8 red-for-named-reason, C2 pass 16/16 |
| M4 | **vacuous able-to-fail control** | the first F1 wrong-line fixture printed `WRONG-LINE-CAUGHT False` for two reasons: a 7-cell row (the checker reads the anchor only from 11-cell rows) and a row id `S9T1` that fails the checker's `S\d{3,}` pattern; read as a repair regression at first | the F1 counter itself, on its first run | fixture padded to 11 cells with id `S991`, bound to a sha-pinned capture; after the fix the control is caught (`WRONG-LINE-CAUGHT True`) and the BASE checker shows `PARSE-ABSENT` for all four blind-spot rows |
| M5 | **repair leaves blind-spot quotes unverified** | after the QUOTE_RE repair, S260/S261/S265/S266 parse (cited 72 → 84) and `live=0` holds, but all four rows carry no `sha256` pin in their anchor cell, so their quotes are cited and not captured-checked (`UNCAPTURED S260 … S266` in the checker output) | the checker output; this is a limit of the rows, not a checker defect | recorded as a limit. Verifying those quotes needs a capture-pin in a supersede row, a registry edit that is not made this round (CORPUS rule 2: append-only, one correction per row) |
| M6 | **frozen C3 text says the R82-V8 repair lands; the implementation does not** | `plans/round-91-claims.md` (C3 Move) names a repair of `plans/round83_c2_checks.py` deriving the fleet root from "the lane root's parent"; the lane root's parent is not the fleet repo unless the lane sits under it, and `origin.parent` (the current default) is the same expression. No code change was made to `round83_c2_checks.py` | this round's review of the claim text against the checker (`R83_FLEET_REPO` default at line 168) | not repaired (no defensible fix in the time the round allows; a fix that names `SHOKUNIN_ROOT` changes the checker's meaning and would need its own frozen claim). The R82-V8 check still passes from the lane root, which is what the gate runs |

## Routed to round 92

1. The R82-V8 clone-path dependence (M6): a checker that resolves the fleet repo from an explicit `SHOKUNIN_ROOT` or a pinned path, with its own counter.
2. The four blind-spot rows' capture pins (M5): one supersede row per row, each naming its capture sha, with the located quote verified in the same round.
3. C1 coverage: the next offline member from the ledger's own class arithmetic (the `filesystem-metadata` class is now 3 of 10 and still the thinnest; candidates in `.ufo/waves/round-89/w1/ScoutR89/next.md` §4.2).

## Honest limits of this round's evidence

- The C1 replay grades a lane-authored fixture (the staged `/app` tree, the script, the CSV and the dependency file are fixtures), so the ten vectors describe the captured bytes on this host's toolchain (python 3.14.8, bwrap 0.13.1), not Terminal-Bench's harness or a real submission.
- The C1 receipt's `WORKTREE` stamp reads `dirty:1` because the receipt file itself was untracked when the stamp was written; L9 does not check the worktree field.
- The C2 pin commit is B2 (`b836a862`), not B (`386184a6`); the B→B2 move is disclosed in M3 and is the only change to pinned bytes before any scoring.

## Measured outcome at tip C and after triage commit D `cefabd44`

| claim | verdict on its frozen predicate | measured |
|---|---|---|
| R91-C1 | **not met** | tip C `a8de3e69`: `TARGET executed=0 cases=10 legs=20 mismatches=10 defects=10`, rc 1, all DEFECT lines `L5 receipt names unknown case ?` (M7). The probe receipt shows ten of ten `ok=True`. |
| R91-C2 | **met** on the conjunction its predicate states | `PINS checked=16 matched=16 mismatched=0`, `SELFTEST cases=8 red-green-ok=8`, rc 0 at C. Residuals below (M9, M10). |
| R91-C3 | **not met** | D `cefabd44`: `freeze=refused oldest_pending_round=82 pending=1 parked=26 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=46 resolutions=74 checks_run=123 overrides=3`, three `DEFECT override-unjustified` (R42-R2, R42-R3-33, R42-R3-37), rc 1. The selftest run separately is 13 of 13 green, and the gate's PREDICATE line does not compute it (M8). |
| R91-F1 (companion) | met on its own predicate | tip C: `PARSED S260=1,S261=2,S265=1,S266=2`, `live=0`, `WRONG-LINE-CAUGHT True`, rc 0. |

## Mistakes, round 91 wave and triage (class · evidence · captured-by · fix)

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M7 | **parser reads the wrong token; the counter's own receipt is the witness** | `plans/round91_c1_replay.py` `parse_receipt()` takes `parts.get("id","?")` over `key=value` tokens; CASE lines carry the id as token 2. ExecC1Battery `parser-fix` (id = `line.split()[1]`, predicate untouched, scratch copy) passes: `TARGET executed=1 cases=10 legs=20 mismatches=0 defects=0`, rc 0. | the first tip measurement (this lesson's table) and ExecC1Battery control 2 | **not repaired after measurement** (the frozen rule: a frozen element that looks wrong is reported). Routed to round 92 under a new frozen predicate, with the probe receipt's ten `ok=True` lines as the red-then-green witness. |
| M8 | **predicate line omits a clause the predicate sentence states** | `plans/round91_burndown.py` `main()` runs `selftest()` only under `--selftest`; the PREDICATE line never includes it. The claim's predicate says the selftest battery is green. ReviewerPredicate F3 and SentinelForge D2 found it independently. The C2 checker runs its selftest in its predicate path (M5 fix); C3 did not carry that fix. | ReviewerPredicate F3, SentinelForge D2 (both wave seats) | routed to round 92: the gate runs its selftest in its default predicate path and fails on any red case. |
| M9 | **C2 residual, two routes, one of them through a selftest weakening** | ExecC2Battery control 6: a one-commit rewrite of the checker and its pin ledger passes with `--skip-selftest` (rc 0, as the claim disclosed). Control 7b: a weakened red-case expectation plus a regenerated pin passes in the default run (rc 0, `SELFTEST red-green-ok=8`). Control 5b: an uncommitted self-leg bypass passes with `--skip-selftest` and fails in the default run. | ExecC2Battery; SentinelForge 5b | disclosed; the operator ruling on in-tree pins is in `.ufo/l0-questions.md` (`kengaku | round-91`). Routed to round 92: the in-path selftest must also pin its own expected-rc table. |
| M10 | **gate accepts a closed row whose check is trivially true, and a blocked row whose owner names nothing** | SentinelForge forgeries 3 and 4 (fixture): a supersede row closed with `check: "true"` and a one-sentence reason is admitted (`freeze=admitted`, rc 0); a blocked row with owner `x` is admitted. The claim's kill rule names checks that are false to the tree; a true check is not false. | SentinelForge (wave seat) | routed to round 92: a closing check must reference a path or a commit that the row's own evidence names, and a blocked owner must resolve to a lane id in `shokunin.conf`. |
| M11 | **the gate's check runner reads the working tree, not the measured revision** | `run_check` uses `cwd=lane_root`; SentinelForge D3 ran the BASE-worktree gate and got the same 114 checks at tip, so the do-nothing control does not measure BASE checks unless `--lane` is at BASE. | SentinelForge D3 | routed to round 92: checks run in a `git worktree` at the measured revision. |
| M12 | **unguarded subprocess crashes the counter with an uncaught exception, rc 1 and no PREDICATE line** | `plans/round91_c1_replay.py` L9 calls `subprocess.run(["openssl","version"])` without a guard; with `openssl` absent from PATH the run dies with `FileNotFoundError` (SentinelForge D1). The claim's contract is exit 2 `could-not-evaluate`. | SentinelForge D1 | routed to round 92: every host probe in a counter is wrapped to `DEFECT SETUP`. |
| M13 | **triage supersedes the superseding row, and the one-level gate ignores it** | eight round-91 rows supersede round-90 rows (`R82-F1-R91`, `R51-R1..R4-R91`, `R42-R2-R91`, `R42-R3-33-R91`, `R42-R3-37-R91`); `plans/round91_burndown.py` builds `supersedes_by_target` once, so a supersede of a supersede is inert. Measured: `oldest_pending_round=82 pending=1`, the only effective open row is `R82-F1` through `R82-F1-R90`. The gate's own clause did not cover a two-level chain, and the triage prompt did not forbid one. | the gate's D verdict (this section) | the triage cannot repair this inside round 91 without an append-only second-level rule. Routed to round 92: a chain-aware supersede, with its own selftest case; the three round-90 override rows need `override_reason` through the same rule. |
| M14 | **a judgment close is recorded with a mechanical-sounding disposition** | R84-V9-R91 closes "prospective condition met by the freeze": its check proves the freeze's Before exists, which is true, but the finding asked for a future-file condition. The disposition `fixed-verified` overstates a judgment. | this lesson's review of triage A | recorded as a judgment in the report; the disposition word is not changed in the appended row (append-only). |

## Routed to round 92 (replaces the list above where they overlap)

1. C1: the `parse_receipt` case-id token (M7), the host-probe guard (M12), with the probe's ten `ok=True` lines as witness.
2. C3: the selftest in the predicate path (M8), the chain-aware supersede (M13), the closing-check reference rule and the lane-id owner rule (M10), checks at the measured revision (M11).
3. C2: the selftest's expected-rc table pinned in the predicate path (M9).
4. The four blind-spot rows' capture pins (M5 of the list above) and R82-V8 (M6).
5. C1 coverage: the next offline member from the ledger's class arithmetic.
