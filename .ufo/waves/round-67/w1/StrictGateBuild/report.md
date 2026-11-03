# StrictGateBuild — R67-C2 strict-mode proposal (r67 w1)

Seat: StrictGateBuild. Frozen claims: `plans/round-67-claims.md` R67-C2 (commit dcc39ea3).
Committed probe, read-only: `plans/round65_c1_sqlite_probe.py`
sha256 `f44b72834d8662cb6986e192dfbdf236daf6c99a174768294e504f7b634db4eb`.
Proposal: `.ufo/waves/round-67/w1/StrictGateBuild/proposed/round65_c1_sqlite_probe.py`
sha256 `27e8b41ffb36cf0b1e4c55055edf0129e3cab13c4c1093ce7121275968e3d857`.
Unified diff of the two files: `strict.diff` (only additions; the default predicate
functions `receipt_failures`/`check_receipt` are untouched, and the only `main` change is
the `--strict` argparse flag plus the two-line branch).

## 1. Implementation map

Line numbers are in the proposal file. Clause text is the frozen s1–s6 text; nothing was
narrowed.

| clause | implementation | what it checks |
|---|---|---|
| s1 | 822–845 | parses `PROBE_VERSION` from `LANE/plans/round65_c1_sqlite_probe.py` (`^PROBE_VERSION\s*=\s*"([^"]+)"`, :828–830); requires the `# instrument plans/round65_c1_sqlite_probe.py version=<V>` header and every recorded V equal to it (:835–845) |
| s2 | 847–860 | receipt `GRADER sha256` equals `GRADER_SHA256` (:848–852) **and** `sha256_file(LANE/GRADER_REL)` equals it (:853–860) |
| s3 | 862–867 | receipt `AMALG sha256` equals `AMALG_SHA256` |
| s4 | 869–889 | `TOOLCHAIN gcc/gcov/bwrap` not empty and not `fabricated`, and equal to the first version token on the receipt's `CC`/`GCOV`/`BWRAP` lines; python is not cross-checked (claim's named limitation) |
| s5 | 891–920 | every `RUN` line carries `rc=0` and `driver="/usr/bin/python3 /ctl/driver.py"` (:894–908); every case-scoped `NOBIND` line carries `delta=0` (:909–915); per-case `NOBIND`, `BUILD`, `FILES`, `ENV` presence for G1–G5 (:916–920) |
| s6 | 922–947 | every `VECTOR` line equals `FROZEN_VECTORS`, once per case; duplicates and unknown case names are defects |

Supporting pieces: `strict_lane()` :806–808 (`pathlib.Path(__file__).resolve().parents[1]`),
`strict_tokens()` :811–814, `check_receipt_strict()` :949–964 (base `receipt_failures`
plus `strict_failures`; prints one `CHECK defect: <clause> ...` per strict defect; rc 0
only when both lists are empty), `--strict` flag :1153–1154 and branch :1159–1162.

The checkable tree was `S/StrictGateBuild/lane/` with `plans/` (proposal copy, sha256
above) and `corpus -> /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus`; `LANE`
resolved to that tree (`receipts/h-checkable-tree.txt`). The scratch tree was reaped after
the runs; the proposal and every receipt below are in this seat dir.

## 2. Required runs (receipts in `receipts/`)

| receipt | command (from the receipt's own `# cmd:` line) | rc | observed |
|---|---|---|---|
| `a-strict-fabricated.txt` | `--check-receipt corpus/evidence/round66/red/fabricated-r65.txt --strict` | **1** | 24 `CHECK defect:` lines: s1 header-missing (1), s4 line-missing (3), s5 run-line/rc and driver (10), s5 files/env line-missing (10); `PREDICATE R65-C1 strict-fail` |
| `b-strict-committed.txt` | `--check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt --strict` | **0** | `PREDICATE R65-C1 strict-pass`; no defect |
| `c-default-committed.txt` | `--check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt` (default) | **0** | `CHECK ok cases=5`, `PREDICATE R65-C1 pass`; stdout identical to the committed tree (below) |
| `d-default-fabricated.txt` | `--check-receipt corpus/evidence/round66/red/fabricated-r65.txt` (default) | **0** | `CHECK ok cases=5`, `PREDICATE R65-C1 pass` — the pre-existing defect; the claim does not change it |
| `e-committed-tree-default.txt` | from `L`: `PYTHONDONTWRITEBYTECODE=1 python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt` | **0** | same output as (c) |
| `f-default-diff.txt` | `diff -u <c stdout> <e stdout>; cmp -s …` | diff **0**, cmp **0** | both stdout sha256 `a2031df7b62c67b88ed89c56532e13ba5e6a95a8c93d9e8bd33713520957fc52` |

Default-mode output over the committed receipt is byte-identical between the unmodified
`L` copy and the proposal (`f-default-diff.txt`; raw stdout kept as
`c-default-committed.stdout` and `e-committed-tree-default.stdout`).

The four required rc values: **(a) 1, (b) 0, (c) 0, (d) 0**.

## 3. Per-clause calibration (mutations of the committed receipt, scratch-only)

Each mutant differs from the committed receipt by one substitution
(`receipts/mutants.diff`); each strict run exits 1 and reports exactly the intended
clause (one defect line apiece).

| mutant | clause | first defect |
|---|---|---|
| `mut-s1-header-version` | s1 | `s1 header-version 'r65-c1/2' != probe PROBE_VERSION 'r65-c1/1'` |
| `mut-s2-grader-sha` | s2 | `s2 grader-sha 000… != b165f850…` |
| `mut-s2-grader-bytes-drift` | s2 (bytes half) | lane capture appended one byte: `s2 grader-bytes-sha 400bae16… != b165f850…` (receipt sha still correct) |
| `mut-s3-amalg-sha` | s3 | `s3 amalgamation-sha 000… != 0a9c8e34…` |
| `mut-s4-toolchain` | s4 | `s4 toolchain-gcc 'fabricated' is fabricated/empty` |
| `mut-s5-run-rc` | s5 | `s5 run-line rc=1 != 0` |
| `mut-s5-driver` | s5 | `s5 run-driver '/usr/bin/python3 /ctl/driver2.py' != '/usr/bin/python3 /ctl/driver.py'` |
| `mut-s5-env-missing` | s5 | `s5 G3 env-line-missing` |
| `mut-s5-nobind-delta` | s5 | `s5 nobind delta=1 != 0` |
| `mut-s6-vector` | s6 | `s6 G4 vector P/P/P != P/P/F` |

Default mode on the failing `mut-s6-vector` is also identical between `L` and the
proposal (`g-default-on-mutant-diff.txt`, diff rc 0; both exit 1 with the same two
`CHECK fail` lines). This is stronger than the required committed-receipt comparison:
the unchanged path is invariant on failing inputs too.

Which clauses are decisive on the fabricated fixture: **s1, s4, s5** (24 defects). s2,
s3 and s6 pass on it because the fixture copies the correct grader sha, amalgamation sha
and VECTOR table; they are load-bearing against value drift (mutants above), not against
this fixture. The claim's named limitation stands: a hand-copied full receipt (header,
CC/GCOV/BWRAP, RUN/FILES/ENV included) would pass strict.

## 4. Clause that cannot be enforced literally from the committed receipt

**s5's `NOBIND` sub-clause.** The frozen wording is “every `NOBIND` line carries
`delta=0`”. The committed receipt also contains two session-level lines,
`NOBIND before-battery listeners=… probe_pid=… probe_listening=…` and the matching
`NOBIND after-battery …` (written by the committed probe at its lines 522 and 620), which
by construction carry no `delta` token. A literal “every line starting with `NOBIND`”
check therefore refuses the committed receipt, i.e. trips kill rule (b). The
implementation excludes exactly those two session markers (`STRICT_SESSION_NOBIND`,
proposal :803) and enforces `delta=0` on every case-scoped `NOBIND G*` line, plus
presence of one `NOBIND G<n>` line per case. No per-case requirement was narrowed. If the
freeze is meant literally, the claim cannot be admitted without a freeze edit; this seat
did not edit it.

Other scope notes, not clause narrowing:

- s1 reads the probe file beside the checker. In the checkable tree that is the proposal
  copy; `strict.diff` shows the `PROBE_VERSION = "r65-c1/1"` line is untouched, and when
  the proposal lands in `L` the same path is the committed file.
- s2's byte half needs `LANE/corpus/…`; the checkable tree supplied it via the corpus
  symlink, and the drift mutant proves the bytes are actually hashed rather than assumed.
- s4's python field is not cross-checked (the receipt has no python line) — the claim's
  own named limitation, left as frozen.
- `check_receipt_strict()` also runs the unchanged base `receipt_failures`; strict can
  never accept a receipt the default refuses. The fabricated fixture passes the base
  predicate, so all 24 defects above come from s1/s4/s5.

## 5. Bounds observed

- No battery, no sandbox, no listener, no use of 127.0.0.1:12355, no port-lock wrap
  needed (no grader invocation). Nothing installed.
- No writes in `L` other than this seat dir `W/StrictGateBuild/` and the trailer
  `W/StrictGateBuild.md`. `git -C L status --porcelain` shows only untracked wave
  entries; no tracked file modified, no git/jj mutation.
- Scratch `S/StrictGateBuild/` reaped after every cited output was copied into
  `receipts/`.

## 6. Files written

- `proposed/round65_c1_sqlite_probe.py` — the proposal.
- `strict.diff` — hashes + `diff -u` committed vs proposal (diff rc 1 = they differ, as intended).
- `receipts/a-strict-fabricated.txt`, `b-strict-committed.txt`, `c-default-committed.txt`,
  `d-default-fabricated.txt`, `e-committed-tree-default.txt`, `f-default-diff.txt`,
  `g-default-on-mutant-diff.txt`, `h-checkable-tree.txt`, `mutants.diff`,
  `mut-s1-header-version.txt`, `mut-s2-grader-sha.txt`, `mut-s2-grader-bytes-drift.txt`,
  `mut-s3-amalg-sha.txt`, `mut-s4-toolchain.txt`, `mut-s5-run-rc.txt`,
  `mut-s5-driver.txt`, `mut-s5-env-missing.txt`, `mut-s5-nobind-delta.txt`,
  `mut-s6-vector.txt`, plus the four raw stdout captures `*.stdout`.
