# DepthGateRerun — kengaku round 70, wave w1

Seat: leaf executor. Item: re-run the lane's **depth** (R63-C2 decision-table) and
**provenance trio** gates at the current tip, and report which backticked paths the depth
gate resolves and whether the `network-service` row's `executed 2 of 8` line is the only row
naming the nginx replay.

Everything below is read-only against the lane: `SKILL.md`, the receipts, `plans/`, and the
round-69 captures were never modified. Captures live in `.ufo/waves/round-70/w1/DepthGateRerun/`
and every scratch byte was written under `/fast/scratch/hyaku/kengaku-r70/DepthGateRerun`
(removed at exit).

## State measured

| fact | value |
|---|---|
| lane tip | `384e9c76415e78093623b3eaff262423a89dbc3e` (`round-70 freeze: claims, instruments, wave spec+dispatch, census-before, controls`) |
| frozen base | `502893ad` — `git merge-base --is-ancestor 502893ad master` → rc 0 |
| `SKILL.md` | CLEAN at tip during the measurement, sha256 `b6217b18…78e9d` (`git diff --quiet SKILL.md` → rc 0); **dirtied by a sibling mid-wave** to `baf3c714…cd0` — see §5 |
| `corpus/evidence/round62/class-survey.txt` | CLEAN at tip, sha256 `ee30c698…45613` |
| `plans/round63_gate_checks.py` | sha256 `a98d9c0f…fe17` |
| `corpus/knowledge/tb2-nginx-request-logging-offline.md` | **DIRTY** (sibling seat in flight): worktree `3b7877a9…0abf`, committed `384e9c76` blob `ae70a630…80f9` |
| `corpus/evidence/round70/gates/trio-nginx.txt` | sha256 `01eb853f…09b2` |

Because `SKILL.md` and the receipt are clean, the depth measurement is a measurement of the
**committed** tip bytes. The entry file is dirty, so the trio run is separately repeated on the
committed blob (item 3 below).

## 1. Depth gate — R63-C2 `depth`

The seat instruction passes `--receipt L/corpus/evidence/round62/class-survey.txt`; `L` is the
lane root variable from the assignment header, not a directory name. Run literally it refuses:

```
$ python3 plans/round63_gate_checks.py depth --skill SKILL.md \
    --receipt L/corpus/evidence/round62/class-survey.txt --root .
SETUP cannot read L/corpus/evidence/round62/class-survey.txt: [Errno 2] No such file or directory: 'L/corpus/evidence/round62/class-survey.txt'
rc=2
```

That rc-2 `SETUP` is itself useful calibration: a wrong receipt path is refused, never scored
as a pass. The real run (cwd = L, lane-relative receipt):

```
$ python3 plans/round63_gate_checks.py depth --skill SKILL.md \
    --receipt corpus/evidence/round62/class-survey.txt --root .
ROWS n=16 class_match=True count_mismatch=0 paths total=34 resolved=34 share=1.00
PREDICATE R63-C2 pass
rc=0
```

`.ufo/waves/round-70/w1/DepthGateRerun/depth.txt` is that stdout verbatim, and it is
**byte-equal** to the round-69 landing capture (`cmp` rc 0 against
`corpus/evidence/round69/gates/depth-gate.txt`, sha256 `d65bbbda…6e22`). Two consequences:

- The tip reproduces the round-69 landing capture exactly — the depth gate has not drifted
  between round 69 and the round-70 freeze.
- The count `paths total=34` is the post-class-row side of R70-C2's E1 `LINE-DIFF`, whose
  pre-side is `paths total=33` (`.ufo/waves/round-69/w1/gates/depth-gate.txt`, sha256
  `f683297c…c9d9`, matches `corpus/evidence/round70/c2/depth-gate-provenance.txt`). A `diff` of
  the two captures changes exactly one line (`33 resolved=33` → `34 resolved=34`) and the
  provenance file's `ADDED-TOKEN` is precisely token 17 below.

Re-running with an absolute `--root /home/vgpnk/Projects/shokunin/kengaku-shokunin` prints the
identical `ROWS` line, rc 0 — the measurement does not depend on the `--root` spelling.

The gate's own control is green at this tip (`selftest.txt`):

```
SELFTEST GOOD rc=0 expect=0 n=16 class_match=True count_mismatch=0 finding=ok ok
SELFTEST BAD-COUNT rc=1 expect=1 n=16 class_match=True count_mismatch=1 finding=ok ok
SELFTEST NO-SECTION rc=1 expect=1 n=0 class_match=False count_mismatch=0 finding=ok ok
SELFTEST BAD-ESCAPE rc=1 expect=1 n=16 class_match=True count_mismatch=0 finding=ok ok
SELFTEST pass
```

Three independent sensitivity mutants on generated copies of `SKILL.md` (real file untouched,
copies under S) confirm the green run is not vacuous — each fails with the expected finding
(`depth-mutants.txt`):

```
M1-count-8-to-7:      rc=1  DETAIL count-mismatch=network-service:got=7,want=8
M2-unresolved-token:  rc=1  paths total=35 resolved=34 share=0.97
                             DETAIL unresolved=corpus/evidence/round70/absent-probe.txt
M3-dotdot-escape:     rc=1  DETAIL escape=../../escapee.json
                             DETAIL unresolved=../../escapee.json
```

## 2. Which backticked paths the depth gate resolves — 34 of 34

The gate harvests backticked tokens from the whole body of
`## Decision table — grader class → offline replay recipe` (`SKILL.md:60`), keeps only tokens
containing `/` that are URLs-free and end in `/` or one of `.py .md .json .txt .sh .lst .yml`,
de-duplicates, and requires every one to resolve root-confined. At the tip:

```
ROWS n=16 class_match=True count_mismatch=0 paths total=34 resolved=34 share=1.00
```

Per-row pointer cells (column 5): 16/16 rows carry at least one resolving token. All 34
resolved tokens (`depth-tokens.txt`), grouped by owning row topic:

- rounds 37–39 git-plumbing: `corpus/evidence/round37/git-webserver-probe.txt`, `plans/git_webserver_probe.py`, `corpus/evidence/round39/git-leak-probe.txt`, `plans/git_leak_probe.py`, `plans/build_pmars_probe.py`, `corpus/evidence/round38/build-pmars-probe.txt`
- round 40 db-state: `corpus/evidence/round40/db-wal-probe.txt`, `plans/db_wal_probe.py`
- round 43 shell-exec: `corpus/evidence/round43/feal-probe.txt`, `plans/feal_probe.py`
- round 52 grader files: `corpus/evidence/round52/graders/executed17.lst`, `…/kv-store-grpc/tests/test_outputs.py`, `…/pypi-server/tests/test_outputs.py`, `…/install-windows-3.11/tests/test_outputs.py`, `…/sqlite-with-gcov/tests/test_outputs.py`
- round 57 numeric-band: `corpus/evidence/round57/eigen-probe.txt`, `plans/round57_c2_eigen_probe.py`
- round 58: `corpus/evidence/round58/kl-probe.txt`, `plans/round58_c2_kl_probe.py`
- round 59: `corpus/evidence/round59/openssl-probe.txt`, `plans/round59_c1_openssl_probe.py`
- round 61 signal-delivery: `corpus/evidence/round61/cancel-async-probe.txt`, `plans/round61_c1_cancel_probe.py`
- round 62 census: `corpus/evidence/round62/class-survey.txt`
- round 63 pypi: `corpus/evidence/round63/pypi-probe-run1-literal-detector-fail.txt`
- round 64 kv-store: `corpus/evidence/round64/kvstore-probe.txt`
- round 65 sqlite: `plans/round65_c1_sqlite_probe.py`, `corpus/evidence/round65/sqlite-gcov-probe.txt`
- round 66/67 torch-pipeline: `plans/round66_c1_tensor_probe.py`, `plans/round67_c1_pipeline_probe.py`, `corpus/evidence/round67/pipe/receipt.txt`, `corpus/knowledge/tb2-torch-pipeline-parallel-offline.md`
- round 68 pypi finish: `plans/round68_c1_pypi_finish.py`
- nginx: `corpus/knowledge/tb2-nginx-request-logging-offline.md` (token 17 — the only nginx path the depth section mentions)

Zero escapes (`escape=None` on all 34) and zero unresolved.

Two calibration notes on that check, reported rather than acted on:

1. **The row-pointer check is existential, not member-scoped.** It passes a row when *any*
   token in column 5 resolves. `network-service`'s four pointer tokens are
   `…/kv-store-grpc/tests/test_outputs.py`, `round64/kvstore-probe.txt`,
   `round63/pypi-probe-run1-literal-detector-fail.txt`, `…/pypi-server/tests/test_outputs.py` —
   none of them is a pointer for `nginx-request-logging`, whose entry path sits in **column 2**
   (the executed/annotated cell). So the gate cannot witness that a *named* member has a
   pointer; it witnesses that the row is anchored to something. This is a scope fact about the
   frozen check, not a proposal to change it.
2. `container-image` has `count=0` (matching the receipt's `CLASS container-image count=0`) yet
   still contributes two resolving tokens; `class_match` accepts it because both sides agree
   on 16 classes and on the zero count.

## 3. Provenance trio gate — R63-C2 `trio`

```
$ python3 plans/round63_gate_checks.py trio corpus/knowledge/tb2-nginx-request-logging-offline.md
TRIO pass corpus/knowledge/tb2-nginx-request-logging-offline.md
rc=0
```

`.ufo/waves/round-70/w1/DepthGateRerun/trio.txt` is that stdout, and `cmp` against
`corpus/evidence/round70/gates/trio-nginx.txt` (sha256 `01eb853f…09b2`) is **byte-equal** — an
independent re-derivation of R70-C2's E2 clause at this tip (E2 itself belongs to the C2 seat;
this seat only corroborates the bytes). A second run is byte-identical
(`TRIO-DETERMINISTIC second-run-identical=True`).

The same gate run against the **committed** blob (`git show 384e9c76:…` into S) also passes
(`trio-committed-bytes.txt`), so the pass is not an artefact of the sibling's dirty file.

Trio scope, as observed in `plans/round63_gate_checks.py:118-144`: it reads the first
`TRIO_WINDOW = 12` lines, stops at the first `##`, and only checks that `source`, `verified-at`,
`recheck` appear in that order. It is a key-order gate, not a content gate — it passes on both
the committed blob (which still opens `source: S241 …`) and the dirty worktree copy. **The trio
receipt therefore cannot be evidence for R70-C2 E3/E4** (S242 naming, corrected anchor, leg-5
statement); those need E3/E4's own re-deriving checks.

## 4. Is the `network-service` row the only row naming the nginx replay?

**Yes.** Evidence at tip `384e9c76` with `SKILL.md` clean (measurement instant 21:47; the file
was dirtied afterwards, see §5):

```
grep -c  'executed 2 of 8' SKILL.md   -> 1
grep -c  'executed 3 of 8' SKILL.md   -> 0
grep -ci nginx             SKILL.md   -> 1
grep -n '^|' SKILL.md | grep -i nginx -> 78:| network-service | 8 | executed 2 of 8 (…
```

The single naming line is `SKILL.md:78`, and the verbatim clause inside it is:

> `round 69 `nginx-request-logging` replayed offline — five frozen vectors, 40/40 legs, but R69-C1 MISS on its leg-coverage clause, so the member is not counted`

with the row itself opening `executed 2 of 8 (round 64 `kv-store-grpc`; round 68 `pypi-server`
replayed offline, R68-C1 pass …; round 69 `nginx-request-logging` …)` and closing on the pointer
``the entry `corpus/knowledge/tb2-nginx-request-logging-offline.md` ``.

Counter-check on the obvious second candidate: the census (`class-survey.txt`, `CLASS
timing-wall count=9 members=…,nginx-request-logging,…`) classifies nginx under `timing-wall`
too, but `SKILL.md:79`'s `timing-wall` row reads only `executed` in its executed cell and names
no member at all (`nginx` not present on that line). So the nginx replay is named by exactly one
class row, `network-service`, and by that row's `executed 2 of 8` clause only. At the 21:47
measurement instant the round-70 before→after target `grep -c 'executed 3 of 8'` was still
**0**; a sibling's landing then flipped it to 1 (§5). The naming row stayed unique across both
instants — `grep -ci nginx SKILL.md` is 1 in both.

## 5. Re-check after a sibling edit landed mid-wave

While this report was being written, `SKILL.md` went dirty: `git diff SKILL.md` is one line —
the `network-service` row's prose `executed 2 of 8` → `executed 3 of 8` (`index 4c1d59a1..650b20c2`,
worktree sha256 `baf3c714…cd0`). That is another seat's C1 landing, not this seat's write.

Both gates were re-run on that worktree state (`depth-worktree.txt`, `trio-worktree.txt`):

```
$ python3 plans/round63_gate_checks.py depth --skill SKILL.md \
    --receipt corpus/evidence/round62/class-survey.txt --root .        -> rc 0
ROWS n=16 class_match=True count_mismatch=0 paths total=34 resolved=34 share=1.00
PREDICATE R63-C2 pass
$ python3 plans/round63_gate_checks.py trio corpus/knowledge/tb2-nginx-request-logging-offline.md
TRIO pass corpus/knowledge/tb2-nginx-request-logging-offline.md        -> rc 0
```

The `ROWS` line is **identical** to the committed-tip run, because the gate compares the count
cell (`8`) against the receipt and harvests path tokens; the `executed k of 8` prose is not
parsed. `grep -c 'executed 2 of 8'` is now 0 and `grep -c 'executed 3 of 8'` is 1 — the inverse
of §4's measurement instant. Both readings are recorded; §4 states the instant each was taken.

## Verdict

**Depth gate (R63-C2 `depth`): PASS at tip `384e9c76`** — `ROWS n=16 class_match=True
count_mismatch=0 paths total=34 resolved=34 share=1.00`, `PREDICATE R63-C2 pass`, rc 0; the
committed-tip capture is byte-equal to the round-69 landing capture, all 34 backticked paths
resolve root-confined, and three mutants (count, unresolved, `..` escape) each fail the
predicate, so the green is live rather than vacuous. The same green is re-derived on the
worktree carrying the sibling's class-row bump (§5), with an unchanged `ROWS` line.

**Provenance trio (R63-C2 `trio`): PASS** — `TRIO pass
corpus/knowledge/tb2-nginx-request-logging-offline.md`, rc 0, byte-equal to
`corpus/evidence/round70/gates/trio-nginx.txt` and deterministic across runs; it passes on both
the committed blob and the dirty worktree; it is a key-order gate and carries no witness for
content-level corrections.

**Class-row naming: `network-service` is the only row naming the nginx replay** in both
measured states — `grep -ci nginx SKILL.md` = 1 (`SKILL.md:78`) at the 21:47 clean-tip instant
and after the sibling's `executed 3 of 8` bump, via the quoted `executed 2 of 8` clause.

## Risks / open items (reported, nothing edited)

1. **Pointer-cell weakness**: `network-service` resolves on `kv-store-grpc`/`pypi-server`
   pointers while the nginx entry lives in column 2, so a green row-pointer check does not
   imply the named member is anchored in the pointer column.
2. **Trio cannot witness S241→S242**: both the committed blob and the working tree pass; E3/E4
   closure cannot be sourced from `trio-nginx.txt` alone.
3. **Dirty sibling inputs**: `SKILL.md` (class-row bump, landed mid-run — see §5), the knowledge
   entry, `corpus/README.md`, `corpus/SOURCES.md`, `plans/round-70-claims.md` and
   `plans/round70_c2_routed_defects.py` were uncommitted at different instants of this run. The
   depth numbers were taken on committed `SKILL.md` and re-derived on the dirty worktree; the
   trio numbers were re-derived on the committed blob as well as the worktree, so no reading
   silently mixes the two states.
4. Scratch `/fast/scratch/hyaku/kengaku-r70/DepthGateRerun` removed after the receipts were
   copied into `W`; no tool installs were needed (system `python3` 3.14.8).
