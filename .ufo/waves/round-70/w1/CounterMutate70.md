# CounterMutate70 — R70-C1 checker mutation probe (kengaku round 70, wave w1)

Seat: mutation tester (leaf). Target of attack: `plans/round70_c1_nginx_probe.py`
`--check-receipt`, i.e. the re-deriving half of R70-C1's frozen predicate.
Lane tip at probe: `master` = `384e9c76415e78093623b3eaff262423a89dbc3e`
(`git -C L rev-parse master`, rc 0). Instrument sha256 at start and end of the probe:
`9aef6d33abc965f52a965b2f9197b78d257dc76003ddc124ca0e692a4fdbbe90`, equal to the committed
blob `master:plans/round70_c1_nginx_probe.py` (rc 0). Scratch: `S=/fast/scratch/hyaku/kengaku-r70/CounterMutate70`.
`L/plans/round70_c1_nginx_probe.py` was **never** modified (before/after sha equal, `git status
--porcelain` on that path empty); every mutant lives under `S/mut/<check>/`.

Frozen lines this probe prices (quoted from `plans/round-70-claims.md` §R70-C1):

> *Each of the seven frozen cases yields its frozen eight-leg vector, every one of the eight
> grader legs is observed `P` in at least one case and `F` in at least one case, each case
> line's `case_sha256` equals its frozen staged-input digest, and the receipt's PROBE,
> PROBE_BLOB and GRADER sha256 equal the committed bytes; the counter then prints
> `PREDICATE R70-C1 pass` and exits 0.*

## 1. What ran

Harness: `S/harness.py` (archived at `W/CounterMutate70/harness.py`), transcript at
`W/CounterMutate70/transcript.txt`. Every mutant is a byte copy of the frozen instrument with
exactly one check neutralised, staged in its own throwaway git repo so `probe_blob_sha` returns
a real blob instead of the `absent` escape (`git -C $D rev-parse --show-toplevel` asserted
equal to `$D` before each commit, rc 0; identity passed per-command with `-c user.name/-c
user.email`, never `git config`).

| # | command | rc |
|---|---|---|
| 1 | `sha256sum plans/round70_c1_nginx_probe.py` | 0 (9aef6d33…) |
| 2 | `git cat-file -p master:plans/round70_c1_nginx_probe.py \| sha256sum` | 0 (same 9aef6d33…) |
| 3 | `python3 harness.py` (baseline accept + selftest + 6-mutant matrix) | 0 |
| 4 | `python3 lane-baseline/plans/round70_c1_nginx_probe.py --check-receipt receipts/baseline.txt` | **0** |
| 5 | `… --selftest --work selftest-work` | **0** |
| 6 | `… --render-table --stage-sha stage` | 0 |
| 7 | `python3 holes.py` (edge probes H1–H3, first pass) | 0 |
| 8 | inline H1b/H3b/H4 probes | 0 |
| 9 | inline H5 probe (committed-probe post-run edit) | 0 |

Good receipt (the accept shape the frozen table needs, bound to the lane's own bytes):
`S/receipts/baseline.txt`, sha256 `c87b165d31ff6328cf5605548ae1062ec0fd470599c79106f5ea113f1af2f21e`,
accepted by the unmutated checker:

```
CHECK ok cases=7 legs=8 seen_p=8 seen_f=8
CHECK stored-predicate=pass derived=pass
PREDICATE R70-C1 pass
```

Selftest tally on the same pristine lane (rc 0):

```
RED r1-all-p rc=1 refused=True / r2-probe-sha … r7-probe-blob … (7/7 refused)
ACCEPT synthetic rc=0 accepted=True
PATH-INDEPENDENT sha_equal=True
STAGED-STATE changes_on_byte=True
SELFTEST red_refused=7/7 green_ok=0 accept_ok=1 ok=True
```

Freeze arithmetic and staged digests re-derive from bytes, not from the document
(`--render-table --stage-sha stage`, rc 0): `LEG-COVERAGE-FROZEN legs=8 seen_p=8 seen_f=8`,
and all seven `CASE-SHA` lines equal the instrument's `CASE_SHA` table byte for byte
(K1 `0cf77ab8…`, K2 `c072ee5f…`, K3 `286db51e…`, K4 `22ee1ff8…`, K5 `5690e1e1…`,
K6 `d4035f6f…`, K7 `07eb2fd3…`).

### Calibration control (why the matrix is not a false positive)

`check_receipt` binds the receipt to the **running** instrument (`own_sha256()`, line 598) and
to the committed blob (line 612). A mutant therefore changes its own `PROBE`/`PROBE_BLOB`
binding; feeding every mutant the baseline receipt makes `probe-sha` fire first and every
mutant looks "killed" for the wrong reason. The first harness pass did exactly that
(`DEFECT probe-sha 9aef6d33…` on 5 of 6 mutants, discarded). The v2 matrix regenerates the
receipt per mutant with `PROBE`/`PROBE_BLOB` bound to that mutant's own bytes, so the only
variable between the pristine run and a mutant run is the target check. Evidence that this
control is real: every mutant returns `MUTANT <check> good rc=0 defects=0`.

## 2. Mutation matrix — each check is load-bearing

Stimulus per check is a single targeted violation that the **pristine** checker refuses with
only that check's defect; the mutant must still accept the frozen good receipt and must accept
the bad stimulus.

| check (source line) | stimulus | pristine | mutant good | mutant bad | killed |
|---|---|---|---|---|---|
| leg-coverage loop (702) | foreign 2-case all-`P` table (no `F` witness) | rc 1, 8 defects | rc 0 | rc 0 | true |
| case-sha comparison (673) | K1 `case_sha256` = 64 zeros | rc 1, 1 defect | rc 0 | rc 0 | true |
| probe-blob binding (612, 614) | `PROBE_BLOB` = 64 zeros | rc 1, 2 defects | rc 0 | rc 0 | true |
| grader-file rehash (631) | grader file byte-flipped → `61a09105…` | rc 1, 1 defect | rc 0 | rc 0 | true |
| VECTOR/expected agreement (642, 685) | K3 `agree=False` | rc 1, 1 defect | rc 0 | rc 0 | true |
| case-set comparison (662) | extra `VECTOR K8 FFFFFFFF` | rc 1, 1 defect | rc 0 | rc 0 | true |

Required log lines:

```
MUTANT leg-coverage killed=True rc=0
MUTANT case-sha killed=True rc=0
MUTANT probe-blob killed=True rc=0
MUTANT grader-file killed=True rc=0
MUTANT vector-agreement killed=True rc=0
MUTANT case-set killed=True rc=0
```

(`rc` is the mutant's rc on the frozen good receipt, per the seat spec. `killed` uses the
pristine→mutant transition: pristine rc≠0 on the bad stimulus and mutant rc=0 on it, with
mutant rc=0 on the good receipt. A mutant that returned rc 0 on both good and bad **and** sat
on a stimulus the pristine checker also accepts is the surviving-mutant hole.)

The exact produced defects, for the record:

```
PRISTINE-BAD case-sha  rc=1 DEFECT case-sha K1 0000… != 0cf77ab8…
PRISTINE-BAD probe-blob rc=1 DEFECT probe-blob 0000… != 9aef6d33… ; DEFECT probe-blob-working-tree 0000… != 9aef6d33…
PRISTINE-BAD vector-agreement rc=1 DEFECT vector-agree K3 agree=False
PRISTINE-BAD case-set rc=1 DEFECT case-set got=['K1'…'K8'] want=['K1'…'K7']
PRISTINE-BAD leg-coverage rc=1 DEFECT leg-coverage test_nginx_installed p=2 f=0 (×8 legs)
PRISTINE-BAD grader-file rc=1 DEFECT grader-file-sha 61a09105…
```

Mutant diffs are single-check edits, verified by `diff -u` (archived at
`W/CounterMutate70/mutant-diffs.txt`); no mutant touches a second check. Mutant file hashes:

```
d18f048e…d132ac1f754f90  leg-coverage
db53dc5a…714f55f2f1c74bb  case-sha
c22801f9…d94bba9d2873ae23  probe-blob
21ee8d0c…844ec599572552e6  grader-file
b3cd6af1…5d2ce17ab4aecfdb  vector-agreement
b1bf7954…15ca2056d020e022  case-set
```

## 3. Holes named (surviving coverage gaps, not permission to change the contract)

**H1 — `probe-blob` fails open when the blob does not resolve (line 607–610).**

```python
live_blob = probe_blob_sha(lane_root()) if live_blob is None else live_blob
if live_blob == "absent":
    # An uncommitted probe cannot bind a blob; the frozen run is post-freeze.
    print("CHECK probe-blob=absent (uncommitted instrument)")
else:
    if got_blob != live_blob: ...
    if got_blob != own_sha256(): ...
```

Stimulus H1b: instrument bytes edited after the run (`PROBE` = `015d74325249…128f8f`), receipt
`PROBE_BLOB` forged to 64 zeros, lane not committed → **rc 0, `PREDICATE R70-C1 pass`**, with
only `CHECK probe-blob=absent (uncommitted instrument)` on stdout. The same forged receipt is
correctly refused (rc 1, `DEFECT probe-blob 015d74… != 9aef6d33…`) when the probe *is*
committed (H5), so the exposure is exactly the `absent` branch: a missing blob skips both
halves of the freeze-bytes bind instead of failing closed. For the real lane `master` carries
the probe, so this is reachable only through a path/branch lookup failure or a checker run from
a copy — narrow, but it is the one arm of the probe-blob check that can accept a forged
receipt.

**H2 — duplicate `VECTOR` lines are last-wins (line 638).** `vectors[parts[1]] = (…)`
overwrites, and only the surviving tuple is compared. Receipt with a contradictory
`VECTOR K1 FFFFFFFF expected FFFFFFFF agree=True` followed by the true line → rc 0,
`PREDICATE R70-C1 pass`. The receipt can carry an observation that contradicts the frozen
vector and still be accepted.

**H3 — duplicate `CASE` lines are last-wins (line 670).** Two well-formed `CASE K1` lines with
contradictory `case_sha256` → rc 0. (A malformed duplicate *is* caught: `DEFECT case-line`,
rc 1 — the field-count arm works.)

**H4 — the leg-coverage loop is unreachable through `--check-receipt` with the frozen table.**
Coverage is counted from `TEST` lines, and `leg-vector` (696) + `vector-mismatch` (682) force
those lines to equal `case["expected"]`; the frozen table has 8/8 coverage, so no receipt that
passes the vector checks can leave a leg uncovered. Dropping `TEST K1 test_nginx_running`
trips `leg-set`, `leg-vector` and `leg-missing` (rc 1) and leaves the coverage counters intact.
The loop is a *table invariant* (it fires only against a foreign table, as the matrix shows),
not a receipt guard; the claim's "any leg with no P or no F witness" kill rule is enforced by
the frozen table plus `--render-table`, and the loop is a backstop.

Minor: the `probe-blob-line` / `case-line` / `vector-line` field-count arms are load-bearing —
my first H1/H3 stimuli were malformed by my own line surgery and were refused
(`DEFECT probe-blob-line n=0`, rc 1; `DEFECT case-line …`, rc 1) before I corrected them.

## 4. Restoration and non-mutation evidence

- `L/plans/round70_c1_nginx_probe.py` sha256 `9aef6d33…` before the probe and after it
  (`unchanged=True`); `git -C L status --porcelain plans/round70_c1_nginx_probe.py` empty.
- Every mutated file lives under `S`; fixture lanes are throwaway git repos under `S/mut/*` and
  `S/lane-baseline`, each with `rev-parse --show-toplevel` asserted before its single commit.
- The corrupted grader byte was restored in each lane and re-hashed to `045cc716…`
  (`pristine grader restored: 045cc716…`, `restored sha True`); the H5 edited probe was
  restored byte-exactly.
- No commit, push, checkout or any mutating git command ran in L. `S` was removed after the
  artefacts were copied here; the whole matrix is reproducible from `W/CounterMutate70/harness.py`.
- Observed, not caused: at probe start and end the lane working tree was dirty on
  `plans/round-70-claims.md` (+12 lines = Amendment A1) and `plans/round70_c2_routed_defects.py`
  (+3/−1); no C1 predicate, case-table, vector or digest line is in that delta (checked with
  `git diff -U0 … | grep -E 'C1|K[1-7]|FROZEN|case_sha'`, only an E1 amendment sentence).

## Verdict

R70-C1's `--check-receipt` is **load-bearing at every one of its six assigned checks**: deleting
any single check turns a stimulus the pristine checker refuses (rc 1, exactly that defect) into
an accept (rc 0) while the frozen seven-case good receipt stays accepted (rc 0). Two
calibration holes survive and are named above: the `probe-blob` `absent` branch fails open
(H1), and duplicate `VECTOR`/`CASE` lines are last-wins (H2/H3). One check is CLI-unreachable
with the frozen table (H4) and functions as a table invariant. I did not edit the instrument,
the case table, a vector, a digest, the kill rule or any target; a rule I think is wrong is
reported here, not changed.
