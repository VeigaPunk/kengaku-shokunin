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
