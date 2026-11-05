# CriticClaims — hostile closure review of R94-C1 and R94-C2 (round 94, w1)

Seat: CriticClaims (leaf, `/skill:godspeed`). No subagents, no git mutation in the lane, no fleet-root writes.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Measured tip T `90c7677f0ba95d0930d93bda6a14aa50605ebe2e`.
Scratch: `/fast/scratch/hyaku/kengaku-r94/CriticClaims/` (clone `lane` detached at T; removed on exit). Every receipt cited below is copied into `receipts/` in this directory; nothing here cites scratch.
Host: `/proc/sys/user/max_user_namespaces` = 122865 (read only). Tool installs/updates: none. Sysctl and PATH unchanged.

## Verdicts

| claim | predicate at T (my run) | does the claim verify? |
|---|---|---|
| R94-C1 coverage | `PREDICATE R94-C1 pass`, 9/9 legs, 38 executed rows, rc 0 | **Verifies, narrowed.** It proves the captured grader runs offline and reproduces the 8×4 vector table written from dry-run observations (this host). It does not test the mechanism predictions; the frozen predicate cannot falsify them. |
| R94-C2 calibration | `PREDICATE R94-C2 pass`, W1–W5 all pass, 5 of 5, rc 0 | **Does not verify as calibration.** The predicate reproduces, but the 5→0 count is confounded (each false gate also fails three v2-only fixtures and W3), W3 is an echo that a stubbed battery passes, and the gate's own "edit later reverted is still a breach" clause is defeated by one `refs/replace` object. Calibration is in-sample: W5 mutants are one-to-one with W2 fixtures, and two were edited pre-P1 until green. |

No finding flips the verdict at T. Several would flip a verdict for a forgery that is frozen before F, or for a post-F ref change that W4 cannot see; these are stated where they apply.

## 1. Reproduced at T (my clone, not the receipts)

```
$ python3 plans/round94_c1_replay.py --lane . --rev 90c7677f0ba95d0930d93bda6a14aa50605ebe2e --work $S/c1/w
LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass
TARGET executed_rows=38 member=write-compressor located=1 executed=1 cases=8 legs=32 mismatches=0 defects=0
PREDICATE R94-C1 pass        (rc 0)            receipts/c1-at-T-my-run.txt
$ python3 plans/round94_c2_counter.py --lane . --rev 90c7677f0ba95d0930d93bda6a14aa50605ebe2e --work $S/c2/w
W1 pass | W2 pass (fixtures=12 ok=12) | W3 pass (SELFTEST cases=15 ok=15 ×2) | W4 pass (instruments=11 intact=11 broken=0)
W5 pass (null 12/12; K1..K7 killed=7)
TARGET legs_passed=5 of 5
PREDICATE R94-C2 pass        (rc 0)            receipts/c2-at-T-my-run.txt
```

Tabled bytes: the 11 paths in the frozen-instruments table hash to their table values at F and at T (`receipts/git-proof.txt`). `git rev-list --full-history F..T -- <path>` is 0 for all 11; `git log F..T -- plans/round-94-claims.md` is empty. **No tabled file changed after F.**

## 2. R94-C1 — coverage

### 2.1 What the frozen predicate tests

- `plans/round94_compressor_probe.py:232` (`ok = observed == case["predicted"]`) compares the replay against the `predicted` column of `plans/round94-cases.json`. That column was filled from dry-run observations. Its C08 entry is now `P,E:UnicodeDecodeError,P,2264`, while the P0 mechanism prediction in `.ufo/waves/round-94/L1/predictions-mechanism.txt` is `P,F,P,2264`. The `why` field discloses this, but the field is named `predicted` and holds the observed value.
- So `mismatches=0` says: the replay reproduces the dry-run table on this host. It is a golden-file test. It cannot refute the mechanism predictions, and the claim's "7 of 8 held" is never re-tested by the predicate.
- What the predicate does establish: the grader runs in bwrap (L6 re-runs the probe from `git archive` and compares the observation block), the ledger flip is real (L7), and the frozen probe and table are the bytes that produced the receipt (L4, L8, L9).

### 2.2 Sensitivity (positive): C1 does notice grader drift

I changed the grader's size wall 2500→2600 in a scratch archive of T, updated the pin in a scratch copy of the probe, and ran that copy (`receipts/c1-sensitivity-grader-size-wall-2600.txt`):

```
CASE C06 predicted=P,P,F,2564 observed=P,P,P,2564 ok=False
mismatches 1      (rc 1)
```

### 2.3 Predictions committed before any probe run — verified, with a caveat

- `bdcb1ec0` (P0, committer 18:55:46) contains `predictions-mechanism.txt` (`receipts/predictions-mechanism-P0.txt`). It is the only commit that carries it.
- The dry-run receipts (`dryrun-1.txt`, `dryrun-2.txt`) first appear in `997a6fe5` (P1, 18:57:43). Both stamp `LANE_TIP bdcb1ec0…`, so each probe ran with HEAD = P0, which contains the predictions. Dry runs 1–2 also show 7 of 8 held and C08 `E` (not `F`).
- Caveat: commit dates are self-reported (no signing). The ordering rests on the `LANE_TIP` stamp, which is consistent with the commit graph.

### 2.4 Undisclosed or unrecorded pre-freeze churn (minor)

- `dryrun-1.txt` has `TOOL_SHA 6c820857e3c0…`. The probe bytes at P1 and F are `3e1e1764…`. The `6c82` version is not in any commit (`git log --all -- plans/round94_compressor_probe.py` lists only P1). The probe was changed between dry runs 1 and 2 with no recoverable record of what changed.
- The C08 `why` text and the claim text say "dry runs 1–3". Only two dry-run receipts exist in git (`git ls-files | grep -c dryrun-3` = 0). `receipts/git-proof.txt`.

### 2.5 C08 depends on the inherited locale and was not pinned (minor)

- The sandbox inherits the host environment: `env -i FOO=bar bwrap … /usr/bin/env` prints `FOO=bar` (`receipts/env-locale-facts.txt`). L9 pins only Python, gcc and rustc versions, not `LANG`.
- The host has `LANG=en_US.UTF-8`. Python's default is UTF-8, and the inverted byte raises under UTF-8 (`UnicodeDecodeError`, same file). `subprocess.run(..., text=True)` inside the grader therefore raises on the corrupted output.
- [INFERENCE] Under a single-byte locale the same decode would succeed and the assertion would fail (`F`), which is the mechanism prediction. This host has no single-byte locale (`locale -a`: C, C.utf8, en_US.utf8, POSIX), so I could not show it empirically.
- Two environment variations on this host (minimal env, and padded env with `LC_ALL=C.UTF-8`) produced identical observation blocks (`receipts/c1-env-minimal.txt`, `receipts/c1-env-padded-LC_ALL-C.UTF-8.txt`). Both are UTF-8 mode, so this does not test the single-byte case.

### 2.6 Codegen fragility of the captured decoder (minor; corroborated, not re-run)

- `environment/decomp.c:75` (`printf("%s", buf)`) prints an uninitialised 10000-byte stack buffer. The lane's own note `corpus/evidence/round94/decomp-opt-divergence.txt` shows `gcc -O3` outputs 4870 bytes against the 4868-byte original.
- Sibling `.ufo/waves/round-94/w1/ExecC1Rerun/report.md` reports that a `gcc -O3` decode flips 3 of 8 vectors (C01 among them), and clang flips C07. I did not re-run those variants; I cite the sibling's receipts (`variant-gcc-O3.txt`, `variant-clang.txt`).
- The frozen predicate holds at the pinned invocation (grader's own `gcc -o decomp2 decomp.c`, default `-O0`; gcc version pinned by L9). The claim does not disclose this fragility in its Source or Kill-rule sections.

### 2.7 Source verification (CORPUS rule 1) — verified

I fetched all six upstream files at `2fd12b88` (`receipts/source-fetch-S297-S302.txt`). HTTP 200 for each, and each sha256 equals the pinned value: `tests/test_outputs.py` 809f…, `tests/original-decomp.c` 7f8d…, `tests/original-data.txt` 0fc4…, `solution/solve.sh` 0155…, `tests/test.sh` 4770…, `environment/Dockerfile` 9a58…. Ledger: 88 members; `file-artifact` 28→29 of 76, `stdout-inspection` 12→13 of 29, `subprocess-exec` 14→15 of 45; executed 37→38 (`receipts/ledger-denominators.txt`), matching the claim.

### 2.8 Universal clause check (C1)

The probe names the three test functions explicitly. The grader has exactly three `def test_` (checked at T), and its sha is pinned in L2, so a fourth test cannot appear without L2 failing. No gap found.

### 2.9 Cheaper control reaching the C1 predicate

None found. The P2 controls (ledger-only, member swap, sandbox outage) fail as stated. L6 re-runs the probe from `git archive`, so a receipt or ledger flip without a real grader run fails. Reaching the predicate requires running the frozen probe in a sandbox.

## 3. R94-C2 — calibration

### 3.1 The five-to-zero count is arithmetically true and confounded

I reproduced the x-head-not-rev false gate (`receipts/x-head-not-rev-false-gate-reproduced.txt`, forgery sha `b9f92e4c…` = P2 control header):

```
W2 w2-rev-below-head RED rc=1 want_rc=0 summary=(1, 0, 1) want=(1, 1, 0)   <- designated
W2 w2-treesame-merge RED rc=0 want_rc=1 ...                                <- v2-only
W2 w2-second-block   RED rc=0 want_rc=2 ...                                <- v2-only
W2 w2-duplicate-row  RED rc=0 want_rc=2 ...                                <- v2-only
W3 echo SELFTEST cases=10 ok=10 (x2)  -> W3 fail
W5 K1..K7 RED anchor-missing           -> W5 fail
TARGET legs_passed=2 of 5 (W1, W4 pass)
```

The P2 receipts show the same pattern for all five false gates (cited from `.ufo/waves/round-94/L1/controls/`, not re-run except x-head-not-rev): every one fails `w2-duplicate-row`, `w2-second-block` and `w2-treesame-merge` and W3 (`cases=10`) in addition to its designated fixture. So each "red at designated fixture" is accompanied by red on features the v1 gate lacks. The count therefore shows the v2 counter rejects v1 code; it does not isolate that each forgery is caught on its own defect. The isolating evidence is W5 on v2 CLI copies, which is a different measurement.

### 3.2 W3 is an echo; a gate with its battery stubbed passes 5 of 5 (major)

I replaced the gate's in-process battery with a constant 15-entry list that prints `SELFTEST cases=15 ok=15` without running any case, left everything else honest, and ran the counter with `--tool-file` (`receipts/x1-stub-battery-gate.py`, `receipts/x1-stub-battery-c2.txt`):

```
W3 echo SELFTEST cases=15 ok=15   (x2)
W3 pass
TARGET legs_passed=5 of 5
PREDICATE R94-C2 pass        (rc 0)
```

Wall time fell from 39.3 s to 6.9 s, showing the battery's fixture repos no longer ran. W3 checks the printed string, not the battery. W5 mutates only evaluate/parse_table/main, so it does not cover the battery either.

Scope of the reach: a gate with a stubbed battery must be frozen before F (W4 binds the lane's tabled gate bytes), so this does not flip the T verdict. Pre-freeze, it reaches the frozen predicate.

### 3.3 Gate universal clause defeated by one `refs/replace` (major)

The gate docstring says an edit later reverted "is still a breach" (`plans/round94_freeze_integrity.py:17`). The touched count is `git rev-list --full-history`, which honours replace refs. Commands and outputs (`receipts/attacks.txt`, section A):

```
A0 honest history (no replace refs):           touched=2  broken   rc 1
A1 replace refs present: 1 (edit commit replaced by an empty-diff commit)
   gate, default:                              touched=0  intact   PREDICATE pass  rc 0
A2 control, GIT_NO_REPLACE_OBJECTS=1:          touched=2  broken   rc 1
```

- The lane has zero replace refs now (`git for-each-ref refs/replace` = 0) and no `.git/info/grafts`. Replace refs are not versioned, so I cannot show they were absent at T; the ref state is a check at review time. T is not flipped.
- W4 cannot see a replace ref added after F: it reads tabled bytes and `rev-list` counts. A post-F edit hidden this way would pass the predicate.

### 3.4 Second table block with other fences is silently ignored (major, claim property)

`parse_table` only recognises the exact fence `` ```frozen-instruments ``. Four-backtick and tilde fences are not counted as blocks (`receipts/attacks.txt`, section C):

```
C1 four-backtick second block naming notes.md, notes edited after freeze:  instruments=1 intact=1  PREDICATE pass rc 0
C2 tilde second block, same:                                              instruments=1 intact=1  PREDICATE pass rc 0
C3 control, notes.md in the honored block, same edit:                     instruments=2 intact=1 broken=1 rc 1
```

The W-3 closure ("second table block ignored") holds only for one spelling. I checked: the F and T claims files contain exactly one fence (`grep` of `frozen` and fence lines at F and T), so the T verdict is unaffected.

### 3.5 Spelled duplicate rows are accepted (minor)

The duplicate check compares raw path strings. `probe.py` and `./probe.py` are two rows, and both are counted (`receipts/attacks.txt`, section B):

```
INSTRUMENT probe.py  ... verdict=broken:rev-bytes-differ+touched-after-freeze=1
INSTRUMENT ./probe.py ... verdict=broken:rev-bytes-differ+touched-after-freeze=1
FREEZE-INTEGRITY instruments=2 intact=0 broken=2
```

This is fail-closed here, so there is no false intact. The "listed twice → could-not-evaluate" clause holds only for exact strings, and the instrument count (W4 floor ≥ 8) is inflatable.

### 3.6 Calibration is in-sample; W5 was tuned pre-P1 (major)

- W5's seven mutants K1–K7 map one-to-one to W2 designated fixtures, and the mutants and W2 fixtures were written together from the same seven attacks. So W5 measures whether each W2 fixture is sensitive to its own defect. It does not add defect classes. It does add evidence that the fixtures are not vacuous: with my run, K1, K2, K3, K5, K6 and K7 each kill only their designated fixture; K4 kills its designated fixture plus the two other CNE fixtures (all expect rc 2).
- The P1 draft of the counter (`.ufo/waves/round-94/L1/c2-counter-dryrun1-prefix.py`, committed at P1) failed W5. I reproduced it at T (`receipts/c2-draft1-at-T.txt`):
  ```
  W5 K2-rev-minus-1 SURVIVED designated=w2-edit-then-unrelated red=-
  W5 K6-second-block-ignored SURVIVED designated=w2-second-block red=-
  TARGET legs_passed=4 of 5
  PREDICATE R94-C2 fail     (rc 1)
  ```
- The final counter (`receipts/c2-counter-final-T.py`) changes both: `w2-edit-then-unrelated` becomes `w2-edit-revert-unrelated`, which adds a revert commit (diff at `receipts/c2-draft1-vs-final-diff.txt`), and the second-block row now names `notes.md` instead of duplicating `probe.py`. Both edits are before P1 and the draft was committed, so they are disclosed. They are still fixture edits made to kill specific mutants, so the 7/7 is post-hoc.
- The claim's "5→0" set and the W5 set are the same in-sample attacks. No held-out forgery exists in the round, so the count is a regression test on known forgeries, not calibration.

### 3.7 Operability counted under calibration (minor)

Two of five legs are not calibration: W3 (echo of a printed line) and W4 (the round's own frozen-rule compliance check). They are reasonable checks, but `legs_passed=5 of 5` folds them into the calibration predicate.

### 3.8 Separability — verified as stated, one direction only

- C1 counter reads the frozen table (L4), the probe bytes (L8), the ledger (L7), the receipt, and the probe rerun. It reads neither the gate nor the C2 counter. Verified by reading `plans/round94_c1_replay.py`.
- C2 W1, W2, W3, W5 read the gate at T and the fixtures, not any C1 artifact. W4 reads the tabled bytes, which include C1's probe, cases and counter (rows 1–3). So C2 is red if any C1 instrument changes after F. The claim says C2 is verifiable without C1 landing, which holds; it does not say the reverse, and it is not true in the reverse sense.

### 3.9 Universal clauses the counter does not enumerate

- Replace refs defeat "edit later reverted is still a breach" (3.3).
- Alternate fences defeat "one table block" (3.4).
- Spelled duplicates defeat "listed twice is refused" (3.5).
- W3 does not verify battery execution (3.2).
- Nothing checks the battery's in-process cases against the CLI behaviour.

### 3.10 Cheaper control reaching the C2 predicate

Yes, pre-freeze: a gate with a stubbed battery (3.2) passes 5 of 5 at T. The P2 do-nothing (0 of 5) is correctly red.

## 4. Sibling overlap

- `.ufo/waves/round-94/w1/ExecC1Rerun/` re-measured C1 at T (pass) and ran codegen variants. Its variant receipts corroborate 2.6 (`gcc -O3` and clang flip vectors). Its determinism result is consistent with my env test (2.5).
- `.ufo/waves/round-94/w1/ExecC2Rerun/` holds the round-93 forgeries. The sha of `x-head-not-rev.py` matches the P2 header.
- No write overlap: my files are under `w1/CriticClaims/` and `w1/CriticClaims.md`.
- Lane state: `SCORECARD.md` and `SKILL.md` are modified and `.ufo/waves/round-94/L1/c2-dryrun1-reproduced.txt` is untracked (a post-T report-only run by the lane). None of them is tabled, and I did not cite the untracked file as evidence; I re-ran the draft at T myself.

## 5. Commands and receipts index

All in `receipts/`:

- `c1-at-T-my-run.txt`, `c2-at-T-my-run.txt` — the two official predicates at T, my clone.
- `x1-stub-battery-c2.txt`, `x1-stub-battery-gate.py` — 3.2.
- `attacks.sh`, `attacks.txt` — 3.3, 3.4, 3.5 (reproducible, builds fixtures in scratch and runs the gate at P1 bytes = T bytes).
- `x-head-not-rev-false-gate-reproduced.txt`, `x-head-not-rev-false-gate.py` — 3.1.
- `c2-draft1-at-T.txt`, `c2-counter-draft1-P1.py`, `c2-counter-final-T.py`, `c2-draft1-vs-final-diff.txt` — 3.6.
- `c1-sensitivity-grader-size-wall-2600.txt` — 2.2.
- `c1-env-minimal.txt`, `c1-env-padded-LC_ALL-C.UTF-8.txt`, `env-locale-facts.txt` — 2.5.
- `git-proof.txt` — tabled hashes, F..T history, commit times, LANE_TIP stamps, replace refs.
- `ledger-denominators.txt`, `source-fetch-S297-S302.txt` — 2.7.
- `dryrun-1-P1.txt`, `dryrun-2-P1.txt`, `predictions-mechanism-P0.txt`, `official-compressor-probe-T.txt` — 2.3.

Reproduce: from a clone at T, `python3 plans/round94_c1_replay.py --lane . --rev T --work DIR` and `python3 plans/round94_c2_counter.py --lane . --rev T --work DIR`; `attacks.sh` in `receipts/` reproduces section 3.3–3.5 given `GATE` pointing at the T gate.

## 6. Answers to the assignment questions

1. **Does C1 prove more than reproduction?** No. The predicate reproduces the dry-run table (2.1), and it is sensitive to grader drift (2.2). It does not prove the mechanism predictions (7/8), since the C08 table entry was set to the observed value.
2. **Are the P0 predictions committed before any probe run?** Yes, by the commit graph and LANE_TIP stamps (2.3). Commit dates are self-reported.
3. **Is C2 calibration or operability?** Mostly calibration (W1, W2, W5), with W3 (echo) and W4 (frozen-rule self-check) counted as legs (3.7).
4. **Is 5→0 honest?** The arithmetic is true (3.1). It is confounded by v2-only features and W3, and W5 isolation is in-sample (3.6). It does not measure discrimination of each forgery.
5. **Does W5 add discrimination beyond W2?** Fixture sensitivity only: it shows each designated W2 fixture turns red under its own defect injected in v2. It adds no defect classes, and two fixtures were edited pre-P1 until their mutants died (3.6).
6. **Are C1 and C2 causally separable?** As stated, yes, in the direction the claim asserts. W4 couples C2 to C1's tabled bytes (3.8).
7. **Universal clauses not enumerated?** Yes: replace refs, alternate fences, spelled duplicates, battery execution (3.9).
8. **Tabled file changed after F?** No (git proof; W4 touched=0 for all 11).

## 7. Tooling

No tool installed or updated. Commands used: `git` (read-only against the lane and against my clone), `python3`, `curl` (source fetch, HTTP 200 for six files), `bwrap` (through the probe), `sha256sum`, `locale`. Lane mutations: none. Host sysctl: read only.
