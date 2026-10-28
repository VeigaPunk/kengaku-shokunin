# C2ExecE — R51-C2 attribution of ledger rows 37–45 (0-based 36..44)

Seat: `C2ExecE`, executor. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Fragment delivered: `.ufo/waves/round-51/w1/C2ExecE.jsonl` (9 rows, one complete row object per line).
Scratch: `/fast/scratch/hyaku/kengaku-r51/C2ExecE` (created, used, removed before yield — see §9).

## 1. Axes named

- **adjacency** (the axis this seat moves, R51-C2 8→9): every routed finding names its owner lane and
  its disposition. My nine rows are the unit; the fragment is the evidence the L1 integrates.
- **freshness** (read-only observation, not claimed here): each of the nine rows' recorded state was
  re-measured at the tip rather than trusted from `status`/`close`. Three rows are still red and are
  labelled so, not greened.
- **calibration** (read-only observation): a disposition is only as good as its check. Every
  `fixed-verified` check I authored was mutation-probed against the artefact it re-derives, so the
  label cannot pass on prose or on a path that no longer exists.

## 2. Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

`git status --porcelain` at that revision showed no tracked modification when I started (only
untracked `.ufo/waves/round-50/*` and `.ufo/waves/round-51/*` wave files), so every lane reading below
is a committed-tree reading at `4090c3db`.

**The counter changed under me mid-seat.** At `15:33:21 -03` `plans/round51_routing.py` became
`M plans/round51_routing.py` (still uncommitted at yield): the check runner moved from
`cwd=str(tmp), timeout=60` to `cwd=str(lane), timeout=90` (`plans/round51_routing.py:129-132`). My
baseline receipt was taken at `15:29:09` on the committed bytes (`cwd=str(tmp)`); I re-ran the frozen
command afterwards on the working-tree bytes and got the identical numbers (§3). My fragment's checks
use `"$LANE/…"` absolute paths, so they pass under **both** versions — verified on both (§5).

**Concurrent lane activity (not mine).** While this seat ran, the L1's landing edits appeared in the
working tree: `M plans/round51_routing.py` (`15:33:21`), `M corpus/SOURCES.md` (`+1` line,
`15:37:06`), `M plans/round-51-claims.md` (`+27` lines, `15:37:26`). `corpus/routed-findings.jsonl`
stayed unmodified throughout (`git status --porcelain` never lists it). I re-ran every reading that
depends on a touched file after the last edit: the frozen command still prints the same numbers (§3),
and the row-40 scan `awk -F'|' '/^\| S[0-9]+/ && NF!=13' corpus/SOURCES.md | wc -l` → `0` after the
`SOURCES.md` append. I wrote nothing outside this report and the fragment.

## 3. Commands run (exact)

Frozen counter, before state, real lane, scratch dir supplied (read-only against the lane):

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
python3 plans/round51_routing.py --lane . --run-checks --scratch /fast/scratch/hyaku/kengaku-r51/C2ExecE/route
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
EXIT=1
```

This reproduces the frozen before receipt (`.ufo/waves/round-51/claims/c2-before.txt`: rows=71,
attributed=0, checks absent=10, exit 1) at `4090c3db` — and adds `SOURCES resolved=71 missing=0`,
i.e. all nine of my rows' `source` pointers resolve.

Per-row check execution in a scratch cwd with the instrument's own environment
(`cwd=<scratch>`, `LANE=<lane>`, `TMPDIR=<scratch>`), reading the fragment's checks:

```
R42-R3-18 accepted-risk    exit=1 out=''
R42-R3-19 accepted-risk    exit=1 out=''
R42-R3-20 fixed-verified   exit=0 out=''
R42-R3-21 fixed-verified   exit=0 out=''
R42-R3-22 fixed-verified   exit=0 out=''
R42-R3-23 fixed-verified   exit=0 out=''
R42-R3-24 fixed-verified   exit=0 out=''
R42-R3-25 fixed-verified   exit=0 out=''
R42-R3-26 accepted-risk    exit=1 out=''
```

Fragment validation: one `git clone --shared` (my single clone), the fragment spliced into a 71-row
ledger at indices 36..44, counter run against the clone:

```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=9 incomplete=62
OWNERS attributed=9 unattributed=62
DISPOSITIONS set=9 bad=62
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=6 passed=6 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
EXIT=1
```

Every one of my nine rows is complete, attributed, dispositioned, source-resolved and check-bearing;
all six `fixed-verified` checks exit 0 under the frozen instrument. The remaining `incomplete=62` /
`unattributed=62` / `bad=62` lines are the other seats' ranges (rows 0..35 and 45..70) and the
`PREDICATE fail` is that, not my nine rows.

Discrimination probes (each mutation applied to the fixture clone only; `ALL DISCRIMINATE`):

| probe | mutation | counter line |
|---|---|---|
| `bare-path` | row 38 check rewritten as `grep -qF 'C3 (D3)' corpus/QUALITY.md` | `CHECK_FAILED R42-R3-20` |
| `fake-fix` | row 38 `check: "false"` | `CHECK_FAILED R42-R3-20` |
| `strip-owner` | row 40 `owner` removed | `R42-R3-22 has no owner` |
| `absorbed-routed` | row 38 `routed` + `next`, owner `kengaku` | `absorbed, not routed` |
| `empty-check` | row 38 `check: ""` | `R42-R3-20 has no check command` |
| `d38` | `C3 (D3)` heading removed from `corpus/QUALITY.md` | `CHECK_FAILED R42-R3-20` |
| `d39a` | `NF!=13` removed from `corpus/QUALITY.md` | `CHECK_FAILED R42-R3-21` |
| `d39b` | a 4-field pipe row appended to `corpus/SOURCES.md` | `CHECK_FAILED R42-R3-21` |
| `d40` | `def parse_registry` renamed at `plans/registry_check.py:25` | `CHECK_FAILED R42-R3-22` |
| `d41` | `C6 (D6)` heading removed from `corpus/QUALITY.md` | `CHECK_FAILED R42-R3-23` |
| `d42` | `R42-R4` re-opened, no successor row | `CHECK_FAILED R42-R3-24` |
| `d43` | `plans/scratch_guard.py` stripped from the `R42-R2*` **check** fields | `CHECK_FAILED R42-R3-25` |

All probes were run before `15:33:21 -03`, i.e. against the **committed** check runner
(`cwd=<scratch>`); the `bare-path` row is the one that changes under the working-tree runner (§2, §5):
re-measured after the edit it passes, which is exactly the version-dependence reported in §6.1. The
twelve artefact/fake-fix probes are independent of cwd.

## 4. The nine rows

| # | id | class | owner | disposition | status | check exit |
|---|---|---|---|---|---|---|
| 37 | `R42-R3-18` | criterion-nonlanded-tool | `kengaku` | `accepted-risk` | open | 1 |
| 38 | `R42-R3-19` | criterion-cli-mismatch | `kengaku` | `accepted-risk` | open | 1 |
| 39 | `R42-R3-20` | criterion-unreachable-receipt | `kengaku` | `fixed-verified` | closed | 0 |
| 40 | `R42-R3-21` | criterion-false-sentence | `kengaku` | `fixed-verified` | closed | 0 |
| 41 | `R42-R3-22` | criterion-wrong-line-pin | `kengaku` | `fixed-verified` | closed | 0 |
| 42 | `R42-R3-23` | criterion-self-undermining-scope | `kengaku` | `fixed-verified` | closed | 0 |
| 43 | `R42-R3-24` | ledger-status-mismatch | `kengaku` | `fixed-verified` | closed | 0 |
| 44 | `R42-R3-25` | ledger-stale-check | `kengaku` | `fixed-verified` | closed | 0 |
| 45 | `R42-R3-26` | guard-exit-code | `kengaku` | `accepted-risk` | open | 1 |

### Ownership evidence (why `kengaku`, per row)

The owner universe is `shokunin.conf`'s `LANES` rows (23 lanes, `kengaku|kengaku-shokunin|novelty +
calibration (LLM and model research and evaluation)`). Every one of these nine findings is about an
artefact **inside this lane**, written by this lane's own round-42 falsify wave:

- rows 37–42: source `.ufo/waves/round-42/falsify/F42RevQuality.md`, lines `:13` `### D1 — HIGH, both
  criteria: the executable checks point at tools that were never landed in any commit`; `:26` `### D2
  — HIGH, both criteria: the Check command lines do not match the tools' CLIs`; `:35` `### D3 —
  MEDIUM, Q33: …`; `:50` `### D4 — MEDIUM, Q34: …`; `:67` `### D5 — LOW, Q34: wrong line pin for
  registry_check.py`; `:73` `### D6 — LOW, Q34: "No lane tool reads it from committed history" is
  self-undermining as landed`. Subject: `corpus/QUALITY.md` Q33/Q34 — this lane's own criteria.
- rows 43–45: source `.ufo/waves/round-42/falsify/F42RevRiders.md`, lines `:121` `**D1 (defect,
  ledger): R42-R4's check passes at the landing while the row says open …`, `:133` `**D2 (defect,
  stale check): R42-R2's clause 3 pins the uncommitted build copy, not the landed tool.**`, `:74`
  `**D3 (defect, doc/behavior): check on a root whose sentinel is unreadable exits 1; the docstring
  documents exit 2.**`. Subjects: this lane's own ledger and this lane's own `plans/scratch_guard.py`
  (`git -C <lane> cat-file -e HEAD:plans/scratch_guard.py` → exit 0, the tool is committed here).

No sibling lane holds these artefacts: `kumitate` owns "orchestration and tooling" fleet-wide, but
`plans/scratch_guard.py` is a kengaku-committed tool for the kengaku scratch root and `corpus/QUALITY.md`
is kengaku's own criteria document. `routed`/`referral` were therefore unavailable for any of the nine
rows (both require a non-`kengaku` owner), and I did not manufacture one.

### Row-by-row re-measurement

- **37 `R42-R3-18`** — `test -f plans/carried_direction_diff.py && test -f plans/sources_appendonly.py`
  → **exit 1**: neither file exists at the tip. Still red. The lane's recorded decision is the
  round-43 correction pair (`corpus/QUALITY.md:843-845` "A byte-identical landing alone would not make
  either Check runnable", `:865-868` C6 (D6) "landing `sources_appendonly.py` — C1's own fix — would
  falsify it"), i.e. the dead executable leg is **accepted**, not fixed and not routed. `accepted-risk`,
  status stays `open`.
- **38 `R42-R3-19`** — `python3 plans/sources_appendonly.py --lane .` → the tool is absent, so the CLI
  mismatch cannot be measured green; exit 1. Same accepted decision as row 37. `accepted-risk`, open.
- **39 `R42-R3-20`** — correction C3 (D3) is present: `corpus/QUALITY.md:846` `- **C3 (D3) — Q33 (b)
  cites a predicate line its own instruction cannot print.**` and its `:849-851` correction ("(b) keeps
  its discriminating lines … and names the default battery as the mode that additionally prints the
  predicate"). Check exit 0. `fixed-verified`.
- **40 `R42-R3-21`** — correction C4 (D4) cites the independent scan: `corpus/QUALITY.md:860` `The
  conclusion is nevertheless true: awk -F'|' '/^\| S[0-9]+/ && NF!=13' corpus/SOURCES.md | wc -l → 0`.
  My check re-derives both legs: citation present **and** the scan still returns 0
  (`awk … | wc -l` → `0`). Exit 0. `fixed-verified`.
- **41 `R42-R3-22`** — `corpus/QUALITY.md` cites `parse_registry … :25`, and the pin is truthful:
  `plans/registry_check.py:25:def parse_registry(text, source_ids):` (`:20` is `def safe_path(value):`).
  Check exit 0. `fixed-verified`.
- **42 `R42-R3-23`** — correction C6 (D6) present at `corpus/QUALITY.md:865` `- **C6 (D6) — the last
  sentence of :767 needs the creation-time scope.**`. Check exit 0. `fixed-verified`.
- **43 `R42-R3-24`** — `R42-R4` now reads `status: closed` (`corpus/routed-findings.jsonl:14`). Check
  exit 0. **Residual risk for the critic:** the row was flipped **in place** — `git show ff14d76` has
  `R42-R4 status= open`, `git show 77ea425` has `R42-R4 status= closed` on the same id, and no
  `R42-R4.1` successor row exists anywhere in the ledger. The finding itself asked for "an R40-R1.1-style
  appended closed row". The defect class (status/check mismatch) is gone; the mechanism is not the one
  the finding prescribed. I did not re-open the row (I am read-only and it is outside this seat's edit
  scope); the L1/critic should decide whether to append the successor row.
- **44 `R42-R3-25`** — a live check now pins the committed tool: `R42-R2.1`'s `check` is `test -f
  plans/scratch_guard.py && grep -qs 'safe-rm' plans/scratch_guard.py && python3 plans/scratch_guard.py
  --selftest …`, and `plans/scratch_guard.py` is committed at `HEAD`. Check exit 0. `fixed-verified`.
  **I had to tighten this check**: the original `grep -qE '"id": "R42-R2(\.[0-9]+)?".*plans/scratch_guard\.py'`
  also matches `R42-R2.1`'s **note** prose ("deleting plans/scratch_guard.py flips it red"), so it would
  pass with no live check pinning the tool — probe `d43` failed to discriminate until I required the
  mention inside a `check` field.
- **45 `R42-R3-26`** — live defect confirmed at the tip:
  ```
  SENTINEL .ROUND-ROOT-SENTINEL present=no reason=sentinel-unreadable:Permission denied
  ROOTFILES n=1 names=.ROUND-ROOT-SENTINEL
  TOTAL seats=0 bytes=0 size=0B
  CHECK red reason=sentinel-unreadable:Permission denied round=None want=* seats=0
  EXIT=1
  ```
  The docstring (`plans/scratch_guard.py:16-17`) still promises `exit 2 when … the sentinel cannot be
  read (cannot evaluate)`. Not fixed, not routable (kengaku's own tool). `accepted-risk`, open — the
  lane must branch on 1, not 2, until the tool is repaired.

## 5. Field changes I made to the nine rows

All original fields are preserved byte-for-byte **except `check` on all nine rows**, plus the added
`owner` and `disposition` (no `next` is needed: no row is `routed`/`referral`). The `check` rewrite is
not cosmetic:

- At the stage-1 freeze the counter ran every `fixed-verified` check with `cwd=<scratch>` and only
  `LANE`/`TMPDIR` in the environment, so a check written against bare lane-relative paths could not
  pass. Probe `bare-path` (`grep -qF 'C3 (D3)' corpus/QUALITY.md`) gave `CHECK_FAILED R42-R3-20` on
  those bytes; **all 61 existing ledger checks are written that way**.
- The working tree now carries an uncommitted repair (`cwd=str(lane)`, §2) under which the same bare
  path passes — measured: `VERIFIED ran=6 passed=6 failed=0` for the bare-path probe. So the anchoring
  requirement is version-dependent, and the L1 must not assume either behaviour: whichever bytes are
  measured, a check anchored as `"$LANE/<path>"` / `git -C "$LANE" …` passes. My fragment is written
  that way and was verified green on **both** versions (`cwd=<scratch>`: `VERIFIED ran=6 passed=6
  failed=0`; `cwd=<lane>`: `VERIFIED ran=6 passed=6 failed=0`).
- Three checks were strengthened beyond anchoring (rows 40, 41, 44) so that each re-derives the
  substance, not just the citation: row 40 also re-runs the `NF!=13` scan; row 41 also re-reads
  `plans/registry_check.py:25`; row 44 requires the tool name inside a `check` field and the tool to be
  committed at `HEAD`.

## 6. Attacks on R51-C2 found while doing this (for the L1 and the critic seats)

1. **Check cwd: the freeze and the working tree disagree (HIGH — the after measurement depends on which
   bytes are on disk).** Committed bytes (`e07f131`): `cwd=<scratch>`, so lane-relative checks fail
   (`CHECK_FAILED R42-R3-20` for the bare-path probe). Working-tree bytes (uncommitted, §2):
   `cwd=str(lane)`, so the same bare path passes (`VERIFIED ran=6 passed=6 failed=0`). The freeze commit
   and the tree that will be measured are therefore different instruments; the L1 should commit the
   repair (or revert it) before measuring, and say which one the receipt is from.
   Secondary hazard introduced by the repair: checks now execute **with cwd inside the lane working
   tree**, so any check that writes (redirects to a file, `git` mutation, a tool that emits into cwd)
   would dirty the lane during a measurement. Only `TMPDIR`-rooted writes are safe.
2. **The owner universe collapses outside the fleet root (HIGH for "measured in a clean clone").**
   `load_owners` reads `fleet = lane.parent`, then `shokunin.conf`'s `LANES` rows and every
   `*-shokunin` directory beside it. Measured:
   ```
   load_owners(fleet root)=24 load_owners(scratch parent)=17
   lost in scratch: ['audio', 'game-dev-2d', 'game-dev-3d', 'lore', 'mado', 'revenger', 'tsukuroi']
   ```
   Consequence, measured in my clone: `DETAIL OWNER R42-R3-26 owner 'tsukuroi' not a fleet lane` —
   `tsukuroi` **is** a `shokunin.conf` lane. Any row this wave routes to `lore`, `revenger`, `mado`,
   `tsukuroi`, `audio`, `game-dev-2d` or `game-dev-3d` will read as unattributed in a clean clone that
   is not placed beside `shokunin.conf` / the lane directories. My nine rows use `kengaku` only, so they
   are immune; the other 62 rows are not guaranteed to be.
3. **`--ledger` outside the lane crashes instead of reporting.** `python3 plans/round51_routing.py
   --lane <lane> --ledger <path outside lane>` →
   `ValueError: '/fast/scratch/…/owner-tsukuroi.jsonl' is not in the subpath of
   '/home/vgpnk/Projects/shokunin/kengaku-shokunin'` at `plans/round51_routing.py:85`
   (`ledger.relative_to(lane)`), traceback, exit 1. A robustness defect, not a predicate defect; it
   blocks any audit that wants to point the counter at a candidate ledger outside the tree.
4. **Row 43's original check could pass on prose** (see row 44 above) — a check that does not
   discriminate is a `fixed-verified` label with no instrument behind it.
5. **Row 42's closure was in place, not appended** (see row 43 above) — the check accepts either leg,
   so the counter cannot see the difference.

## 7. Limits

- Nine rows, one pass, one revision (`4090c3db`). I did not attribute rows outside 36..44 and did not
  run other seats' checks.
- `accepted-risk` is a judgement about **this lane's recorded decision**, not a claim that the defect is
  harmless. Rows 37/38 rest on the round-43 corrections C2/C6; row 45 rests on nothing but the live
  behaviour, and the L1 may prefer to repair `plans/scratch_guard.py` (exit 2 on an unreadable
  sentinel) instead of accepting it — in that case row 45 becomes `fixed-verified` with the same check.
- `fixed-verified` for rows 43/44 means "the check the row itself authored now exits 0", not "the
  mechanism the finding prescribed was used" (§4, row 43 residual risk).
- The fragment is a candidate, not a landing. The lane's `corpus/routed-findings.jsonl` is untouched
  (`git status --porcelain` shows no tracked modification from this seat).
- `prose`/`note` fields of the nine rows are reproduced verbatim, including their round-44 field-change
  trailers.

## 8. Report path and fragment

- Fragment: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-51/w1/C2ExecE.jsonl` (9 rows).
- Report: this file.

## 9. Scratch

`/fast/scratch/hyaku/kengaku-r51/C2ExecE` held one `git clone --shared`, the generator, the
discrimination harness and the route scratch dirs. `git -C <clone> rev-parse --show-toplevel` was
asserted to print the clone path before any fixture write. The whole tree was removed before this
report was yielded; nothing under `/tmp` is cited above and no scratch path is evidence for any claim.

VERDICT: PASS — nine rows (0-based 36..44) attributed and dispositioned in
`.ufo/waves/round-51/w1/C2ExecE.jsonl`: 6 `fixed-verified` with `"$LANE"`-anchored checks that exit 0
under both the committed and the current check runner and that discriminate against mutated artefacts,
3 `accepted-risk` with their live defects re-measured and left `open`; owner `kengaku` for all nine on
quoted lane-internal evidence; no row routed out, so no `next` field; 5 instrument defects reported for
the L1 (§6).
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
