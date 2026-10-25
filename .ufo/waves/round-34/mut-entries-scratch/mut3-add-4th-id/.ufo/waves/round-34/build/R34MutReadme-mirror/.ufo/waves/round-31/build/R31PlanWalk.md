# R31PlanWalk — bounded planning data-walk over the three frozen claims

Leaf seat, read-only. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Access date 2026-10-25.
Baseline lane tip `0883e72`. Nothing under the lane was created, edited or deleted except this file;
scratch lives in `/tmp/r31-R31PlanWalk/` (well under 60 MB).

## Method and drift disclosure

I read `plans/round-31-claims.md` first, then walked only the data each predicate reads, then ran the
three counting commands. **The lane was being repaired while I walked it.** Two of the three counters
changed bytes under me, so every measurement below carries the sha256 of the bytes that produced it.
Freeze-adjacent measurements (the ones the task asks for, i.e. the *before* state) were taken at
05:52–05:53 local, against the committed control receipts; the drift snapshot is 05:57:26-03:00.

| bytes | sha256 | used for |
|---|---|---|
| `plans/adoption_check.py` (unchanged since freeze) | `f9f8188e…d69926` | all C1 runs |
| `plans/round31_defects.py` at freeze | `f5da4186…6695cd` | the **before** C2 run |
| `plans/round31_defects.py` at snapshot | `2c320d58…4f3234` | the **current** C2 run |
| `plans/sources_adopt.py` at freeze | `886c406a…bd26b2` | first C3 read |
| `plans/sources_adopt.py` at snapshot | `4e49a3e2…f5573f` | the C3 run quoted (drifted `886c406a`→`3d42dbee`→`71a90ec0`→`39ba62b2`→`4e49a3e2`) |
| `git show 0883e72:plans/sources_adopt.py` | `47e60021…fef7922` | the C3 control |

A stray `usage: sources_adopt.py … --url-map needs --quote-file and --artifact` block appears
interleaved in two of my command outputs: that is a concurrent seat's probe on the shared session
shell, not my invocation. My own C3 lines are the `SELFTEST cases=…` lines and their exits.

---

## (a) C1 — `plans/adoption_check.py`

```
$ python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok
EXIT=1
```

**Exact line + exit:** `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok`, exit **1**.

Byte-diff against the committed control `.ufo/waves/round-31/claims/control-nothing.txt`: **identical**
(`diff` clean). The census subprocess inside it returned 0 on its own: my direct run of
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` printed
`14` `W04` lines, `0` `E`-codes and `kengaku ok …/corpus/SOURCES.md`, exit **0** — byte-identical to
`claims/census-before.txt`.

### Before-state: exactly what the counter prints — yes

All seven printed fields match the frozen control, including `census=ok`. The clause the frozen
predicate adds beyond the printed seven (`verified-at`, distinct ids, `opened`, one index row) is
computed and gates the exit code, not the line; at `entries=0` those are all false, consistent with
exit 1.

### Target reachable in one round — yes, and I proved it rather than argued it

I built the expected post-state in `/tmp/r31-R31PlanWalk/sim2/kengaku-shokunin/` (copy of
`corpus/knowledge`, `corpus/lessons`, `SOURCES.md`, `README.md`, the staged entry, plus a one-lane
`shokunin.conf`) and ran the unmodified counter against it:

```
$ python3 plans/adoption_check.py --lane /tmp/r31-R31PlanWalk/sim2/kengaku-shokunin \
    --expect .ufo/waves/round-31/adoption-expect.json --census
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok
exit=0
```

That is the frozen line verbatim, exit 0, with `census` reporting `ok` from a real census run over the
simulated registry (`E_codes=0`). **No counter change is needed** — the target is reachable on the
committed counter bytes.

Six landing preconditions fell out of the walk. Each is enforced by a named check, and each is a place
a verbatim append of the staged package fails:

1. **Rows must land inside `## Registry`** (`corpus/SOURCES.md:19`; next heading `## Paths` at `:111`).
   My first simulation appended at EOF and the census returned three lines
   `kengaku  E12  S092/S093/S100 row outside Registry section`.
2. **S093's escaped pipe must be de-escaped.** The staged row carries one `\|`
   (`SOURCES.append.md`, S093). The gate refuses it:
   `parse_rows` → `parsed_rows=0 malformed=[(3, 'S093', 'escaped-pipe')]` (`EXIT_MALFORMED`, and the
   selftest pins that as case `escaped-pipe-refused`). In the registry it would also be `NF=14` → census `E01`.
3. **The recheck prose must be normalized.** The staged cell is
   `2026-10-23 — re-verify at the next upstream release (Gate S092 below)`; appended verbatim the census
   printed three `E09` lines (`S092`, `S093`, `S100`) and exited 1. The gate's `--recheck 180d` default
   is the normalization that clears it.
4. **`used-by` must name only paths that exist here.** The staged cells name
   `corpus/knowledge/terminal-bench-release-identity.md` (S092, S100) and
   `corpus/knowledge/benchmark-grader-semantics.md` (S093). Neither is in this lane's
   `corpus/knowledge/` (39 files, no `terminal*` match), so census `E11` fires. Trimming to the new
   entry clears it.
5. **`opened` must be re-dated to 2026-10-25.** Staged is `2026-10-23`. Census `E08` only rejects
   *future* dates, so `2026-10-23` would keep `census=ok` while `rows_mined`/`opened_ok` in the counter
   fail — the counter, not the census, is what forces the re-date.
6. **The entry's `verified-at:` must be `2026-10-25`.** Staged is `2026-10-23`. This gates the exit
   code without appearing in the printed seven (`verified_at_ok == len(entries)`).

One unpinned drift: S100's URL `https://github.com/laude-institute/terminal-bench-2` is the same URL as
S079's, so the census `W04` count goes **14 → 15** (`kengaku  W04  S100 duplicate url
github.com/laude-institute/terminal-bench-2 across scopes`). Warnings do not change the census exit, and
no clause of C1 pins the count, so this lands silently. The claims file's own baseline sentence
("census exit 0 with 14 `W04`") becomes stale at 15.

Mid-repair observation at the snapshot: the entry file has landed (`entries=1`) but the registry rows
have not, so the counter now prints
`entries=1 indexed=0 cited_rows=3 rows_present=0 rows_mined=0 usedby_ok=0 census=ok`, exit 1 — an
intermediate state, not a verdict.

**VERDICT: C1 — before-state exact (line byte-identical to `control-nothing.txt`, exit 1); target reachable in one round on unchanged counter bytes (simulated post-state prints the frozen line, exit 0), conditional on the six landing constraints above; one unpinned receipt drift (W04 14→15).**

---

## (b) C2 — `plans/round31_defects.py --lane .`

Before, on the freeze-time counter bytes (`f5da4186…`):

```
$ python3 plans/round31_defects.py --lane .
DEFECT R1 log-delta-correction: no appended correction quotes the superseded delta wording (only the original occurrence exists)
DEFECT R2 lesson-q6-basis: no appended erratum states the admitted Q6 basis after the retracted one
DEFECT R3 lesson-q2-tier-cell: no appended erratum corrects the Q2 tier cell to S086 B
DEFECT R4 entry-duplicated-sentence: the entry carries the 'reconciled truth' sentence 2 times, not exactly once
DEFECT R5 entry-falsifier-clause: the falsifier bullet repeats 'populated (not "unknown")' 2 times, not exactly once
DEFECT R6 entry-staged-source-count: the entry still says three staged source rows are unregistered
DEFECT R7 entry-s2-only-field: the entry still claims the tri-state flag is the only new field, contradicting its R3 row
DEFECT R8 entry-licence-adjective: the entry names a CC0 licence no registry row records
DEFECT R9 round30-seat-reports-committed: .ufo/waves/round-30/build/R30DraftGate.md still differs from HEAD: M .ufo/waves/round-30/build/R30DraftGate.md
DEFECT R10 lesson-round-shape: no appended erratum corrects the falsify seat count to 33
checks=10 defects=10
EXIT=1
```

**Exact line + exit:** `checks=10 defects=10` after ten `DEFECT` lines, exit **1** — byte-identical to
`.ufo/waves/round-31/claims/defects-before.txt` (`diff` clean, ten lines + the total).

Current, on the drifted counter bytes (`2c320d58…`):

```
DEFECT R9 round30-seat-reports-committed: .ufo/waves/round-30/build/R30DraftGate.md still differs from HEAD: M .ufo/waves/round-30/build/R30DraftGate.md
checks=10 defects=1
EXIT=1
```

### Before-state: exactly what the counter prints — yes

Ten red items, the frozen `checks=10` total, exit 1. The counter also guards its own contract on every
run (`tuple((i, l) for i, l, _ in CHECKS) != FROZEN` prints `DEFECT registry: …` and exits 1) and
`--selftest` asserts each check is red on an empty tree, so a shrunken check list cannot print
`defects=0`.

### Target reachable in one round — yes, but only after the counter's own R6 rule changed

Current state is `defects=1`, and the one item left is R9. R9 is reachable by a single commit: all five
seat reports exist with 243 / 1281 / 417 / 396 / 447 lines (the check requires ≥100) and the worktree
`R30DraftGate.md` contains `Pass 9` once, so committing the worktree bytes clears it without touching
their content. That commit is the integrator's act, not mine.

**The caveat is R6, and it is the finding of this walk.** Under the *freeze-time* bytes, `check_r6`
credited a staged URL only by exact containment:

```python
registered = [url for url in urls if url.rstrip("/") in registry]
if unregistered != 2: return f"re-derived {unregistered} unregistered staged sources, the repair assumes 2"
```

The staged file cites `https://aclanthology.org/2026.gem-main.50.pdf`; the registry carries
`https://aclanthology.org/2026.gem-main.50/` (`corpus/SOURCES.md:23`, S001). I measured the predicate
over the three staged URLs: `registered=0`, `unregistered=3`. So **no entry text could satisfy R6**
under the frozen rule — the "two of its three" repair was refused with
`re-derived 3 unregistered staged sources, the repair assumes 2`. I tested the one repair that would
have worked without a counter change — grounding the `.pdf` locator in S001's `source` cell — and the
frozen rule then returned clean; that is a source-identity edit no item of R1-R10 names.

The counter has since been rewritten to a document-key rule
(`re.sub(r"\.pdf$", "", url.rstrip("/")).lower()` over registry URLs, plus a number-word parse instead of
a substring test), and R6 now clears on entry text alone. The change is **disclosed**, not silent: the
R6 seat report `.ufo/waves/round-31/build/R31DefR6.md` §F2 measures the same `rstrip`-in-registry
failure and proposes exactly this normalization. But it is a change to a predicate body after the
freeze, made because the frozen body was unsatisfiable — C2's `defects=0` was not reachable on the
bytes the claim froze. Under the claim's own sentence ("a predicate changed after a seat has scored is
not this claim's predicate") the repaired R6 is not the frozen R6.

**VERDICT: C2 — before-state exact (byte-identical to `defects-before.txt`, exit 1); target reachable in one round (now `defects=1`, R9 only, closable by committing five intact reports) — but reachable only after `check_r6`'s frozen rule was replaced, because the frozen rule returned `unregistered=3` against the `.50.pdf` vs `.50/` locator pair and refused every entry-text repair.**

---

## (c) C3 — `plans/sources_adopt.py`

```
$ python3 plans/sources_adopt.py --selftest
CASE collision-zero-indent PASS
CASE collision-one-space PASS
CASE collision-three-space PASS
CASE four-space-not-a-row PASS
CASE escaped-pipe-refused PASS
CASE prose-recheck-normalized PASS
CASE usedby-projected PASS
CASE duplicate-staged-id PASS
CASE clean-package-passes PASS
CASE missing-requested-id PASS
CASE quote-overlong-refused PASS
CASE quote-absent-refused PASS
CASE quote-located-accepted PASS
CASE quote-boundary-25-accepted PASS
CASE quote-url-bound-accepted PASS
CASE quote-url-mismatch-refused PASS
CASE quote-url-unmapped-refused PASS
SELFTEST cases=17 failed=0
EXIT=0
```

**Exact line + exit:** `SELFTEST cases=17 failed=0`, exit **0**.

Baseline control, from `git -C … show 0883e72:plans/sources_adopt.py > /tmp/r31-R31PlanWalk/base.py`
(sha256 `47e60021…fef7922`, 815 lines):

```
$ python3 /tmp/r31-R31PlanWalk/base.py --url-map /tmp/z
base.py: error: unrecognized arguments: --url-map /tmp/z
BASE_UM_EXIT=2

$ python3 /tmp/r31-R31PlanWalk/base.py --selftest
SELFTEST cases=14 failed=0
BASE_ST_EXIT=0
```

Both match `.ufo/waves/round-31/claims/gate-before.txt` (`url_map_exit=2`, `SELFTEST cases=14
failed=0`, `selftest_exit=0`; that receipt's `prog` is a renamed copy `r31-gate-baseline.py`, the bytes
are the same commit).

### Before-state: exactly what the counter prints — yes

`cases=14 failed=0` exit 0 for the baseline tool; `--url-map` unrecognized, argparse exit 2. The
target line `cases=17 failed=0` is **already printed** at the measured bytes, and the control cannot
reach it (14 cases, and the argument does not exist).

### The three new cases are failure-capable — checked by mutation, not by name

The three cases assert exit codes, not just messages: `quote-url-mismatch-refused` requires
`wrong_code == EXIT_URL_MISMATCH` with `EXIT_URL_MISMATCH = 8` (`plans/sources_adopt.py:55`),
`quote-url-unmapped-refused` requires `EXIT_URL_UNMAPPED = 9` (`:56`), and both require
`found == ["S024"]`, i.e. the bytes *did* contain the quote and the refusal is the citation. I mutated
`bind_failure` in a `/tmp` copy to accept every artifact unconditionally and re-ran the selftest:

```
SELFTEST cases=17 failed=2
  failed: quote-url-mismatch-refused quote-url-unmapped-refused
mut_selftest_exit=1
```

So the refusal pair is genuinely load-bearing. Note the asymmetry: `quote-url-bound-accepted` stays
green under that mutation — it is the accept-side case and is not failure-capable on its own; the
set of three is failure-capable only through the two refusals.

### Target reachable in one round — yes, already reached on the measured bytes

**VERDICT: C3 — before-state exact (`cases=14 failed=0`, `--url-map` exit 2, matching `gate-before.txt`); target met at the measured bytes (`SELFTEST cases=17 failed=0`, exit 0), the three new cases are failure-capable under mutation (two refusal cases go red), and the baseline cannot reach the target.**

---

## Predicate clauses a do-nothing round could satisfy

- **C1 — `census=ok`.** Already true before any work: `control-nothing.txt` itself prints `census=ok`.
  A receipt that quotes or greps the census field is satisfied by a round that changed nothing. Only
  the six non-zero fields carry information, and the frozen sentence's `verified-at` / `opened` /
  distinct-id / one-index-row clauses are invisible in the printed line (they gate the exit code only),
  so a transcript that quotes the line without the exit cannot separate a pass from a fail.
- **C1 — the `W04` count.** Nothing pins it; S100 adds a 15th and the claims file's "14 `W04`"
  baseline silently rots.
- **C2 — none of the ten.** Every check is red-on-empty (`--selftest` asserts it) and `CHECKS` is
  compared to `FROZEN` on every run, so inaction cannot produce `defects=0`. Two weak spots: R8 passes
  on a one-word deletion of `CC0` (the claim permits "grounded or dropped"), and `checks=10` prints
  identically before and after — it only means something beside `defects=`.
- **C3 — `SELFTEST cases=17 failed=0` is the whole machine-checked surface.** Three *vacuous*
  always-pass cases print the same line and exit 0; nothing in the counter enforces the predicate's
  "failure-capable" adjective (my mutation is the only evidence that today's three are). Also, the
  control clause "rejects the same invocation with argparse exit 2" **no longer separates the trees**:
  the new bytes also exit 2 on a bare `--url-map` (`sources_adopt.py: error: --url-map needs
  --quote-file and --artifact`). The separating signals are the case count (14 vs 17) and the stderr
  wording, not the exit code.

## Residual unknowns (not resolved here)

- **C1 kill rule not exercised.** I fetched nothing, so "a cited source whose located quote cannot be
  found at the pinned revision is refused for that row" is untested by me. The counter cannot see it;
  the gate's `--url-map` now can, but only when handed an artifact plus a map.
- **R9's commit** is unobserved (an integrator act; I never touch a lane Git index).
- **The C1 simulation trims `used-by`** to the new entry. If the integrator keeps the staged sibling
  paths (`terminal-bench-release-identity.md`, `benchmark-grader-semantics.md`), census `E11` fires and
  `census=ok` becomes `census=fail` unless those entries are also created.
- **Concurrent drift**: two counters changed bytes during the walk (`round31_defects.py`,
  `sources_adopt.py`). Every number above names the bytes that produced it; the C2 before-line is only
  reproducible from `f5da4186…`, which is no longer on disk.

No tool installs or upgrades were needed for this walk.
