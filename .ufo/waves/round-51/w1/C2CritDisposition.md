# C2CritDisposition — disposition semantics attack (kengaku round 51, C2)

Seat: `C2CritDisposition` (critic). Item: attack the C2 disposition semantics — find rows that
can be marked `fixed-verified` while the underlying claim is false (a check that passes
vacuously), or `accepted-risk` while it is really an unowned defect; construct them in scratch,
run the frozen counter, report whether it passes, then state a stricter rule and its cost.

**Axes named:** `adjacency` (the axis C2 claims) and `calibration` (the axis a vacuous
`fixed-verified` would falsely attest — the ledger's dispositions are self-assessment).
`freshness` (C1) untouched; no C1 file was read for measurement beyond the claims.

**Revision measured:**

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7      (lane master tip at measurement)
    parent of the frozen instrument: e07f131cf7037e58a21db6e1f3986cf401ad257c (stage-1 freeze)
    ledger at this revision: 71 rows, 0 with `owner`, 0 with `disposition`
```

Scratch: `/fast/scratch/hyaku/kengaku-r51/C2CritDisposition` (one `git clone --shared` at
`.../lane`; `git -C .../lane rev-parse --show-toplevel` → that same directory, checked before
every write; the clone's ledger was restored by `cp` from a saved copy, never by a git command).
`df -h /fast` → `804G 252G 552G 32% /fast`.

## Bottom line

**The frozen counter passes on every attack.** Eight constructed ledgers — two synthetic
`fixed-verified`/`accepted-risk` attacks, one built from four *real* rows with their original
check bytes, one cross-lane absorption, one status contradiction, one single-path fill, one
commit-only `fixed-historical`, and one run without `--run-checks` — each print
`PREDICATE R51-C2 pass` and exit 0.

The instrument is **faithful to the frozen predicate** (verified: the base-tip run reproduces
`c2-before.txt` line for line). The defect is that the predicate is **satisfiable vacuously**:
it measures field presence and process exit codes, never the binding between a disposition and
the finding it describes. The five frozen controls do not cover any of the eight classes below,
so the kill rule ("fails if any control passes") cannot fire.

## Method — exact commands

All fixture runs are the frozen command verbatim, in the scratch clone, `cwd = .../lane`,
`TMPDIR = .../work/<fixture>`:

```sh
python3 plans/round51_routing.py --lane . --run-checks      # every fixture except fg
python3 plans/round51_routing.py --lane .                   # fg only (no --run-checks)
python3 plans/round51_routing.py --selftest                 # instrument self-check
```

Each fixture starts from the real 71-row ledger and rewrites one row (or fills all), so every
run reports `rows=71`; the non-attacked rows get the cheapest green fill the counter accepts
(`owner=kengaku, disposition=fixed-historical, close=<existing path>, check="true"`), so any
failure would be attributable to the attacked row alone.

## 1. Harness fidelity — the baseline reproduces the committed receipt

```sh
python3 plans/round51_routing.py --lane . --run-checks     # pristine ledger, clone @ 4090c3d
```
```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
EXIT 1
```

Identical to `.ufo/waves/round-51/claims/c2-before.txt` (same ten counters, same verdict). The
fixture harness is the real instrument, not a re-implementation. `--selftest` →
`[selftest] cases=11 failures=0` / `[selftest] ALL PASS`, exit 0.

## 2. Mechanism: the counter runs checks where the lane does not exist

`check()` runs each check with `cwd=<scratch dir>` and only `LANE=<lane>` in the environment:

```python
out = subprocess.run(["bash", "-lc", cmd], cwd=str(tmp), ... env={**os.environ, "TMPDIR": ..., "LANE": str(lane)})
```

**0 of the 61 existing checks use `$LANE`.** All 61 are relative-path commands written for a
lane-root cwd. I ran every check twice, in the counter's scratch cwd and in the lane cwd:

| cell | n | rows |
|---|---|---|
| pass in scratch **and** lane | 2 | R39-R5 R42-R3-03 |
| **fail in scratch, pass in lane** | **41** | R39-R1 R40-R1..R4 R42-R2 R42-R4 R40-R1.1 R42-R2.1 R42-R2.2 R42-R3-01/04/10..17/20..25/28..31/38..41 R45-S5-1..6,7a |
| **pass in scratch, fail in lane** | **4** | **R39-R2 R42-R3-07 R42-R3-08 R42-R3-26** |
| fail in both | 14 | R39-R3 R39-R4 R42-R1 R42-R3 R42-R5 R42-R6 R42-R3-02/05/06/18/19/27/32/36 |

Representative cwd-only failure (R39-R1), verbatim in the scratch cwd:

```
CMD: grep -q '^| `order-check`' SKILL.md && grep -q '^| `round39-c1-audit`' SKILL.md
grep: SKILL.md: No such file or directory
EXIT 2          # passes in the lane cwd
```

So the counter's cwd makes **absence the default state**, and the check idioms split by how they
read absence: positively-phrased checks fail (41), **negatively-phrased checks pass** (4). This
is the pressure gradient that produces the attack below: to reach `CHECK_FAILED 0` with the
frozen command, the L1 must rewrite 55 checks, and the cheapest rewrite that passes is `true`.

## 3. `fixed-verified` with a check that passes vacuously

### 3a. Synthetic — `check: "true"` on a row whose own note says the defect is live

Fixture `fa-vacuous-true`, row `R39-R2` (its own `note`, unchanged, records the defect:
"absent `--work` raises FileNotFoundError from tempfile.mkdtemp (plans/git_leak_probe.py:258)
and exits 1"):

```json
{"id": "R39-R2", "status": "open", "owner": "kengaku", "disposition": "fixed-verified",
 "check": "true", "close": null, "blocker": null}
```

```sh
python3 plans/round51_routing.py --lane . --run-checks
```
```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=71 incomplete=0
OWNERS attributed=71 unattributed=0
DISPOSITIONS set=71 bad=0
SOURCES resolved=71 missing=0
CHECKS present=71 absent=0
VERIFIED ran=1 passed=1 failed=0
CLOSE_REFS resolved=70 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
EXIT 0
```

The underlying claim is **false**, proved locally at the tip (not taken from the note):

```sh
python3 plans/git_leak_probe.py --lane . --work "$S/absent-work"
```
```
Traceback (most recent call last):
  File ".../lane/plans/git_leak_probe.py", line 301, in <module>
    sys.exit(main())
  File ".../lane/plans/git_leak_probe.py", line 258, in main
    root = pathlib.Path(tempfile.mkdtemp(prefix="k39-glr-", dir=a.work))
FileNotFoundError: [Errno 2] No such file or directory: '.../absent-work/k39-glr-hbykj32c'
EXIT 1
```

`status: "open"` with `disposition: "fixed-verified"` is also accepted — the counter never
cross-checks the two fields.

### 3b. Synthetic — a real failing check masked with `|| true`

Fixture `fb-masked-check`, same row:

```json
{"id": "R39-R2", "status": "open", "owner": "kengaku", "disposition": "fixed-verified",
 "check": "python3 \"$LANE/plans/git_leak_probe.py\" --lane \"$LANE\" --work \"$TMPDIR/absent-work\" >/dev/null 2>&1 || true"}
```

`VERIFIED ran=1 passed=1 failed=0` … `PREDICATE R51-C2 pass`, exit 0. Unmasked, the same
command exits **1** (`unmasked-check: EXIT 1`). A one-token mask is invisible to the counter.

### 3c. **Real rows, original check bytes untouched — no rewrite needed at all**

Fixture `fi-real-row`: the four rows that pass in the scratch cwd and fail in the lane
(`R39-R2 R42-R3-07 R42-R3-08 R42-R3-26`) marked `disposition=fixed-verified`, `status=open`,
**`check` left exactly as committed**:

```sh
python3 plans/round51_routing.py --lane . --run-checks
```
```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=71 incomplete=0
OWNERS attributed=71 unattributed=0
DISPOSITIONS set=71 bad=0
SOURCES resolved=71 missing=0
CHECKS present=71 absent=0
VERIFIED ran=4 passed=4 failed=0
CLOSE_REFS resolved=67 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
EXIT 0
```

Four live defects become "verified fixes" by adding one field. The two idioms that make it work
are both already in the ledger:

```
R39-R2     :: ... python3 plans/git_leak_probe.py --lane . --work "$d/absent" ...; [ "$rc" -eq 2 ] || [ "$rc" -eq 0 ]
R42-R3-07  :: ! grep -qF 'equal to the receipt row' SKILL.md
R42-R3-08  :: ! grep -qF 'biopython==1.85' plans/pkg_gate.py
R42-R3-26  :: ... python3 plans/scratch_guard.py check "$d" ...; [ "$rc" -eq 2 ]
```

Measured, same row, both cwds:

```
lane-cwd EXIT=1          # the defect is live
tmp-cwd  EXIT=0          # the counter's cwd
missing-script EXIT=2    # plans/git_leak_probe.py does not resolve in the scratch cwd;
                         # the check accepts rc==2 as success
```

`! grep` over a file that is absent is exit 0 by construction. **This is not a hypothetical
attack: the frozen command certifies these four rows today.**

## 4. `accepted-risk` on an unowned defect

Fixture `fc-accepted-risk-unowned`:

```json
{"id": "R39-R2", "status": "open", "owner": "unowned:integrator",
 "disposition": "accepted-risk", "check": "false", "close": null, "blocker": null, "note": null}
```

```
VERIFIED ran=0 passed=0 failed=0
PREDICATE R51-C2 pass
EXIT 0
```

`accepted-risk` carries **no clause at all**: no rationale, no ISO date, no `next`, no owner
restriction, and its `check` is never executed (`check: "false"` is accepted). Worse,
`unowned:integrator` sits in `FALLBACK_OWNERS`, so the summary line reads
`OWNERS attributed=71 unattributed=0` while one row names **no lane** — the false-provenance
line the axis exists to prevent. The claims permit this by wording ("every `owner` names a fleet
lane … (or `unowned:integrator`)"), but the axis's signal is "named with its owner": a defect
owned by nobody, parked as risk, with no written decision, scores as attributed.

## 5. Cross-lane absorption (`owner=kama` + `fixed-verified`)

Fixture `fd-cross-lane-absorb`: `{"owner": "kama", "disposition": "fixed-verified", "check": "true"}`
→ `PREDICATE R51-C2 pass`, exit 0.

The only ownership constraint in the counter is on `routed`/`referral`
(`if owner == "kengaku": NEXT violation`). `fixed-verified` has **no** ownership constraint, so
kengaku can declare another lane's finding fixed — the exact "absorbed, not routed" failure the
axis measures — and the counter is silent. The asymmetry is one-sided: `routed` cannot be owned
by kengaku, `fixed-verified` can be owned by anyone.

## 6. `fixed-historical` close resolves to anything that exists

- `fe-historical-any-commit`: `close: "4090c3db79d11279ab5e5121ba25e74aa316e6e7"` (a commit that
  does not touch the finding) → `CLOSE_REFS resolved=71 missing=0`, pass, exit 0.
  The clause is `git cat-file -e <tok>^{commit}` — any commit in the object database satisfies it.
- `ff-single-close-fill`: **all 71 rows** get `disposition=fixed-historical` and the *same*
  `close: "corpus/lessons/round-50-verifier-spotcheck.md"` → `FIELDS complete=71`,
  `OWNERS attributed=71`, `CLOSE_REFS resolved=71`, `PREDICATE R51-C2 pass`, exit 0.

A ~10-line fill turns the whole ledger green with zero provenance. This is the cheapest way to
meet the C2 after-target, and the counter cannot distinguish it from real attribution.

## 7. The pass line does not attest the run-checks clause

Fixture `fg-no-run-checks`: `disposition=fixed-verified, check="false"`, run **without**
`--run-checks`:

```
VERIFIED ran=0 passed=0 failed=0
PREDICATE R51-C2 pass
EXIT 0
```

`check()` never fails for the missing flag. The instrument prints the same
`PREDICATE R51-C2 pass` whether or not a single check ran, so the line cannot be cited as
evidence for the claim's clause "every `fixed-verified` row's check exits 0 **in this run**".
The frozen command does pass `--run-checks`; the laxity is that nothing enforces it.

## 8. Fixture results

| # | fixture | attack | frozen command | exit | predicate |
|---|---|---|---|---|---|
| fa | `fa-vacuous-true` | `fixed-verified` + `check:"true"`, claim false (probe exit 1) | `--run-checks` | 0 | **pass** |
| fb | `fb-masked-check` | real failing check + `\|\| true` | `--run-checks` | 0 | **pass** |
| fc | `fc-accepted-risk-unowned` | `accepted-risk` on `unowned:integrator`, no rationale/date/next | `--run-checks` | 0 | **pass** |
| fd | `fd-cross-lane-absorb` | `owner:kama` + `fixed-verified` | `--run-checks` | 0 | **pass** |
| fe | `fe-historical-any-commit` | `fixed-historical` close = unrelated commit | `--run-checks` | 0 | **pass** |
| ff | `ff-single-close-fill` | all 71 rows, one disposition, one close path | `--run-checks` | 0 | **pass** |
| fg | `fg-no-run-checks` | `fixed-verified` + `check:"false"`, no flag | *(no flag)* | 0 | **pass** |
| fi | `fi-real-row` | 4 real rows, original check bytes, `status:open` | `--run-checks` | 0 | **pass** |

Two required counterexamples: **fa/fi (fixed-verified, false claim, vacuous check)** and
**fc (accepted-risk, unowned defect)**. Both pass.

## 9. What the ledger actually contains (cost baseline for any stricter rule)

Running the 61 committed checks in a cwd where the lane resolves:

```
lane-cwd wall total 0.94s over 61 checks
lane-cwd failing ids (18): R39-R2 R39-R3 R39-R4 R42-R1 R42-R3 R42-R3-02 R42-R3-05 R42-R3-06
  R42-R3-07 R42-R3-08 R42-R3-18 R42-R3-19 R42-R3-26 R42-R3-27 R42-R3-32 R42-R3-36 R42-R5 R42-R6
```

**18 rows describe defects that are still live at the tip.** They cannot honestly be
`fixed-verified`; the honest dispositions are `open` + `accepted-risk` (with a written rationale)
or `routed` (with an owner and a `next`). A full `--run-checks` pass costs 0.43–0.48 s in the
scratch cwd and 0.94 s in the lane cwd — machine cost is not the constraint; curation is.

## 10. A stricter rule, and what it costs

| rule | clause | closes | machine cost | decision cost |
|---|---|---|---|---|
| **S0** | if any row is `fixed-verified` and `--run-checks` is absent, the predicate **fails** (or prints `pass (checks not run)`) | fg | ~4 lines, 0 s | none |
| **S1** | reject no-op/mask check strings: `^\s*(true\|:\|exit 0)\s*$`, `\|\|\s*true`, `;\s*true`, `\|\|\s*exit 0`, `\|\|\s*:`, `\|\| exit 0` | fa, fb | ~10 lines regex, 0 s; **0 existing rows match** (measured: no mask pattern, no `check:"true"` in the 61) | none today; applies to new rows |
| **S2** | run checks with the lane as cwd (`cwd=lane`, `TMPDIR` still scratch) **or** require every check to reference `$LANE` | fi, and the 41 false-failures | 2-line change, or 61 mechanical `"$LANE/"` prefixes; +0.5 s | 61 edits; then 18 rows fail honestly |
| **S3** | owner/status/disposition consistency: `fixed-verified`/`fixed-historical` ⇒ `status=closed` **and** `owner=kengaku`; `accepted-risk` ⇒ `owner` is a named lane (not `unowned:integrator`), `note` carries a rationale + ISO date, `next` names the review round; `unowned:integrator` allowed only with `status=open` and disposition in `{routed, referral}` | fc, fd | 0 s | ~28 written decisions (10 no-check rows + 18 live rows); any genuinely unowned finding must be escalated as an L0 question instead of parked |
| **S4** | `fixed-historical` `close` must be a commit whose diff touches the row's `source` path, or a new `fix_path` | fe, ff | one `git diff-tree` per row (<10 ms) | needs a `fix_path` field wherever the fix landed in another file (e.g. lesson-sourced rows fixed in `SKILL.md`), else the rule produces false failures |
| **S5** | `source` line must exist (`line ≤ wc -l` of the file), not just the file | the D5-class pointer laxity (round-50 §6 D5) | ~3 lines, 0 s | none |

**Differential verification** (the rule that would actually bind a `fixed-verified` to its
claim): every such check must exit **non-zero at the pre-fix revision** and 0 at the tip.
Machine cost is trivial here — a second pass is ~0.5–1 s — but it needs a per-row `fixed_at`
revision, a materialized base worktree, and curation for rows whose fix predates the ledger's
own history. That is real work, and it belongs to the 9-band, not to this round.

**Cheapest honest subset: S0 + S1 + S3** (zero/near-zero machine cost, decision cost only).
**S2 is the highest-value single change** — it makes the 61 existing checks meaningful and
removes the pressure toward `true` — but it changes the frozen instrument, so it cannot land
inside round 51.

## 11. Smallest safe correction

The predicate is frozen before data and the five controls are fixed, so **round 51 cannot
tighten it without breaking its own freeze**. The safe correction therefore has two parts:

1. **Now, at landing (integrity commitment, no predicate change).** The L1 must refuse the
   vacuous class it is permitted to use: do not mark any of the four `pass-in-scratch,
   fail-in-lane` rows, nor the fourteen `fail-in-both` rows, `fixed-verified`. Record the 18
   live rows as `open` with `accepted-risk` (dated rationale, named accepting lane) or `routed`
   (non-kengaku owner + `next`). State this refusal in the round lesson, because the counter
   would not have caught the alternative.
2. **Round 52 instrument.** Freeze S0 + S1 + S3 (+ S2 as an option) with **these eight fixtures
   as mandatory failing controls** — each is a *passing* control today, which is precisely the
   falsification. S5 belongs with the C1/D5 pointer work.

Impacted axes: `adjacency` (the claim's own signal — an unowned defect scored as attributed, a
kama-owned finding scored as kengaku-fixed); `calibration` (a green `PREDICATE R51-C2 pass` line
that four live defects satisfy). Neither bars C1; C2's *claim* survives, but only if the landing
does not take the vacuous path.

## Limits

- Measured at tip `4090c3d` in one scratch clone; the ledger has no `owner`/`disposition` yet, so
  every fixture is my construction over the real 71 rows, not the L1's eventual attribution.
- I proved the underlying claim false for **R39-R2** (probe traceback, exit 1) and proved the
  cwd mechanism for **R39-R1** (`grep: SKILL.md: No such file or directory`). For
  `R42-R3-07/08/26` I report the 2×2 cell and the idiom (`! grep` on an absent file,
  `rc==2` accepted on a missing script); I did not independently verify the subject of each of
  the other 17 lane-cwd failures.
- The 41 "fail in scratch, pass in lane" rows are attributed to relative paths by the 2×2 and
  the measured fact that **0 of 61 checks use `$LANE`**; I did not rewrite each one to confirm.
- No network check was run; no production file, fleet file or sibling repo was touched; no
  commit, push or mutating git command was issued anywhere.
- Scratch tree `/fast/scratch/hyaku/kengaku-r51/C2CritDisposition` **removed** before yield
  (clone, fixtures, logs, work dirs). Free space seen at start: 552 G on `/fast`.
- No tool was installed or upgraded for this seat.

VERDICT: **C2's instrument is conformant and its five controls hold, but the frozen predicate is
vacuously satisfiable — 8/8 constructed rows pass, including 4 real rows with unmodified check
bytes whose defects are live at the tip. Round 51 may land C2 only by refusing the vacuous
dispositions by hand; S0+S1+S3 (and these fixtures as failing controls) must be frozen into the
round-52 instrument.**
