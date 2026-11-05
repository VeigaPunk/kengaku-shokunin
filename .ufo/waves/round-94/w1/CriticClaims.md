# CriticClaims — scoped findings, round 94 (R94-C1 coverage, R94-C2 calibration)

Full analysis, commands and outputs: `.ufo/waves/round-94/w1/CriticClaims/report.md`. Raw receipts: `.ufo/waves/round-94/w1/CriticClaims/receipts/`. Measured tip T `90c7677f0ba95d0930d93bda6a14aa50605ebe2e`.

## Verdicts

- **R94-C1 coverage — verifies, narrowed.** At T, `python3 plans/round94_c1_replay.py --lane . --rev T --work DIR` prints all nine legs pass, `TARGET executed_rows=38 member=write-compressor located=1 executed=1 cases=8 legs=32 mismatches=0 defects=0`, `PREDICATE R94-C1 pass`, rc 0 (reproduced from my clone). The predicate proves reproduction of the dry-run observation table on this host, not the mechanism predictions (the table's C08 entry is the observed vector).
- **R94-C2 calibration — does not verify as calibration.** At T, `python3 plans/round94_c2_counter.py --lane . --rev T --work DIR` prints W1–W5 pass, `TARGET legs_passed=5 of 5`, `PREDICATE R94-C2 pass`, rc 0 (reproduced). The 5→0 count is confounded and in-sample, W3 is an echo, and the gate's universal clauses have holes (findings below).

No finding flips the T verdict. Findings C2-F1, C2-F2 and C2-F3 would flip the predicate for a forgery frozen before F, or for a post-F ref change that W4 cannot see.

## Findings

FINDING C2-F1 major — W3 checks a printed `SELFTEST cases=15 ok=15` line, not the battery. With the gate's in-process battery replaced by a constant print (battery never runs), the counter still reports `TARGET legs_passed=5 of 5`, `PREDICATE R94-C2 pass`, rc 0 (wall 39.3 s → 6.9 s). Receipts: `receipts/x1-stub-battery-c2.txt`, `receipts/x1-stub-battery-gate.py`.

FINDING C2-F2 major — The gate's documented clause "an edit later reverted is still a breach" fails under one `refs/replace` object. Honest history: `touched=2 broken rc 1`. With the edit commit replaced by an empty-diff commit: `touched=0 intact`, `PREDICATE freeze-integrity pass`, rc 0. Control with `GIT_NO_REPLACE_OBJECTS=1`: `touched=2 broken rc 1`. The lane has zero replace refs now and no grafts file; W4 cannot detect a replace ref added after F. Receipts: `receipts/attacks.sh`, `receipts/attacks.txt` (section A). Fix belongs to round 95 (`git rev-list --no-replace-objects` or `GIT_NO_REPLACE_OBJECTS=1` in the gate's git calls).

FINDING C2-F3 major — "One table block" holds only for the exact fence `` ```frozen-instruments ``. A second block written with a four-backtick or tilde fence is ignored: a notes.md row edited after freeze gives `instruments=1 intact=1 PREDICATE pass rc 0`. Control with the row in the honored block: `broken=1 rc 1`. The F and T claims files each contain one fence, so T is unaffected. Receipts: `receipts/attacks.txt` (section C).

FINDING C2-F4 major — The 5→0 count is confounded and in-sample. Reproduced x-head-not-rev: its designated `w2-rev-below-head` is red, but so are `w2-treesame-merge`, `w2-second-block`, `w2-duplicate-row` (v2-only) and W3 (`cases=10`); all seven W5 mutants report `anchor-missing`. The P2 receipts show the same v2-only + W3 pattern for all five false gates. W5's K1–K7 map one-to-one to W2 designated fixtures, and the P1 counter draft failed W5 (K2 and K6 SURVIVED, `TARGET legs_passed=4 of 5`, `PREDICATE fail`, reproduced at T: `receipts/c2-draft1-at-T.txt`). The final counter edits `w2-edit-then-unrelated` (adds a revert commit) and the second-block row, both before P1 and disclosed by committing the draft. W5 7/7 is therefore post-hoc fixture tuning. Receipts: `receipts/x-head-not-rev-false-gate-reproduced.txt`, `receipts/c2-draft1-vs-final-diff.txt`.

FINDING C2-F5 minor — Spelled duplicate rows are accepted: `probe.py` and `./probe.py` are two rows, both counted (`instruments=2 broken=2 rc 1`). Fail-closed here (no false intact), but the "listed twice → could-not-evaluate" clause holds only for exact strings and the instrument count (W4 floor ≥ 8) is inflatable. Receipts: `receipts/attacks.txt` (section B).

FINDING C2-F6 minor — Two of five legs are operability, not calibration: W3 (echo of a printed line) and W4 (the round's own frozen-rule compliance check). The predicate `legs_passed=5 of 5` folds them into the calibration claim.

FINDING C1-F1 minor — The frozen predicate is a reproduction test. `plans/round94_compressor_probe.py:232` compares the replay with the `predicted` column of `plans/round94-cases.json`, which was filled from dry-run observations; C08's entry is the observed `P,E:UnicodeDecodeError,P,2264`, not the P0 prediction `P,F,P,2264`. The mechanism predictions are never tested by the predicate. The claim discloses the refutation in its `why` text; the field name and the "predictions" framing overstate what C1 proves. Sensitivity is positive: moving the grader's size wall to 2600 flips C06 (`mismatches 1`, rc 1; `receipts/c1-sensitivity-grader-size-wall-2600.txt`).

FINDING C1-F2 minor — Unrecorded pre-freeze churn. `dryrun-1.txt` used probe bytes `6c820857…` that exist in no commit; the probe changed between dry runs 1 and 2 with no recoverable record. The C08 `why` text says "dry runs 1–3", but only two dry-run receipts exist in git. The P0 commit (`bdcb1ec0`, the only one carrying the predictions) precedes both dry-run receipts, whose `LANE_TIP` stamps are `bdcb1ec0` (verified; `receipts/git-proof.txt`).

FINDING C1-F3 minor — C08's `E` outcome depends on the inherited locale, which L9 does not pin. `bwrap` passes the environment through (`env -i FOO=bar` → `FOO=bar` inside the sandbox); the host runs `LANG=en_US.UTF-8`; the inverted byte raises `UnicodeDecodeError` under UTF-8. [INFERENCE] A single-byte locale would decode without error and yield the predicted `F`; this host has no such locale, so it is not shown. Minimal and padded environments gave identical observation blocks (both UTF-8 mode). Receipts: `receipts/env-locale-facts.txt`, `receipts/c1-env-*.txt`.

FINDING C1-F4 minor — The captured decoder has undefined behaviour (`environment/decomp.c:75`, `printf("%s", buf)` over an uninitialised 10000-byte buffer). The lane's own note shows `gcc -O3` output of 4870 bytes against 4868. Sibling `.ufo/waves/round-94/w1/ExecC1Rerun/` reports that a `gcc -O3` decode flips 3 of 8 vectors (including C01) and clang flips C07 (corroborated from its receipts, not re-run by me). The frozen predicate holds at the pinned invocation (default `-O0`, gcc version pinned by L9). The claim does not disclose this fragility.

NOTE (not a finding) — No tabled file changed after F (`git rev-list --full-history F..T` = 0 for all 11 paths; `git log F..T -- plans/round-94-claims.md` empty; W4 `touched=0` ×11). Source verification passed: all six upstream files at `2fd12b88` return HTTP 200 and match their pinned sha256 (`receipts/source-fetch-S297-S302.txt`); ledger denominators 88 / 76 / 29 / 45 match (`receipts/ledger-denominators.txt`).

## Answers to the assignment's questions

- Does C1 prove more than reproduction? No (C1-F1).
- Are the P0 predictions committed before any probe run? Yes, by commit graph and LANE_TIP stamps; commit dates self-reported (C1-F2).
- Is C2 calibration or operability? Mostly calibration; W3 and W4 are operability (C2-F6).
- Is 5→0 honest? Arithmetic true; confounded and in-sample (C2-F4).
- Does W5 add discrimination beyond W2? Fixture sensitivity only; no new defect classes (C2-F4).
- Are C1 and C2 causally separable? As stated; W4 couples C2 to C1's tabled bytes in one direction.
- Universal clauses not enumerated? Yes: replace refs (C2-F2), alternate fences (C2-F3), spelled duplicates (C2-F5), battery execution (C2-F1).
- Was any tabled file changed after F? No.
- Cheaper control reaching the predicate: C1, none found (L6 re-runs the grader). C2, yes, pre-freeze: a stubbed-battery gate (C2-F1).

## Tool installs or updates

None. Host sysctl unchanged (`/proc/sys/user/max_user_namespaces` read only). Lane git: read-only commands only. Scratch clone and fixture repos removed on exit.

## Paths written

- `.ufo/waves/round-94/w1/CriticClaims.md` (this file)
- `.ufo/waves/round-94/w1/CriticClaims/report.md`
- `.ufo/waves/round-94/w1/CriticClaims/receipts/` (23 files: counter runs at T, attack script and output, false-gate reproduction, draft/final counter, sensitivity run, env/locale facts, git proof, ledger and source checks, dry-run and prediction copies)
