# C2ExecOpenChecks — round 51, w1 executor (every OPEN routed-finding check, run and classified)

Seat: `C2ExecOpenChecks` (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Axes named: **adjacency** (R51-C2, the ledger's owner/disposition attribution) is the axis this
seat serves; **freshness** (R51-C1) is untouched by this seat. Nothing here is a claim about a
third axis.

Read first, in full: `plans/round-51-claims.md` (frozen stage-1 claims), then the frozen C2
instrument `plans/round51_routing.py` (all 240 lines, not the docstring only). This seat then ran
the `check` field of **every OPEN row** of `corpus/routed-findings.jsonl` (27 of 71 rows) in a
scratch cwd with `TMPDIR` set and a 60 s timeout per row, recorded exit code plus first output
line, and classified each row.

## 1. Revision and lane state

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

Stage-1 freeze is `e07f131cf7037e58a21db6e1f3986cf401ad257c`; HEAD is one commit later (`4090c3d`,
the wave-spec commit). The ledger is byte-identical between freeze and HEAD — the whole diff is
three wave files, none of them the ledger:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --name-only e07f131cf7037e58a21db6e1f3986cf401ad257c..HEAD
.ufo/waves/round-51/build_spec.py
.ufo/waves/round-51/w1-dispatch.json
.ufo/waves/round-51/w1-spec.json
$ git diff --stat e07f131..HEAD -- corpus/routed-findings.jsonl      # empty
```

So every exit code below is a measurement of the frozen stage-1 ledger. Row census at this
revision (`json.loads` per line): `total 71`, `open 27`, `closed 41`, `refused 2`, `blocked 1` —
`open = 27` matches the item. All 27 `source` pointers resolve in the lane (`(lane/src).exists()`
true for every open row); no open row has a missing source.

## 2. Method — three passes per row, same command, three working directories

The counter **as committed at `REV 4090c3d`** runs a check as
`subprocess.run(["bash","-lc",cmd], cwd=<scratch>, timeout=60, env={**os.environ, TMPDIR:<scratch>, LANE:<lane abs>})`
(`git show 4090c3d:plans/round51_routing.py`, lines 126-131). Pass A reproduces that exactly.
(The lane working tree is **not** clean at this file — an uncommitted edit changes `cwd` to the
lane and the timeout to 90 s; §8 measures both versions. Pass A/B/C below are direct `bash`
runs and do not depend on either version.) Pass B re-runs the same
command with `cwd` = the lane, to separate "the check's target is invisible from the scratch cwd"
from "the check's assertion is false". Pass C re-runs the command with the one-token repair
`cd "$LANE" && ` prefixed, from the scratch cwd, to show whether the check becomes honest.

Scratch root (NVMe, `df -h /fast` → `804G 250G 555G 32%` at start):

```
SCR=/fast/scratch/hyaku/kengaku-r51/C2ExecOpenChecks
mkdir -p "$SCR"/{work,tmp}          # work = cwd, tmp = TMPDIR
export TMPDIR=$SCR/tmp
```

Driver (`$SCR/run_checks.py`, stdlib only, no hardcoded `/tmp`): for each open row with a
non-empty `check`, run A then B, record `returncode`, stdout, stderr, elapsed; then pass C over
the same rows. One row timed out? None — the slowest check took 0.04 s.

Per-row first lines are reproduced verbatim in §3; the full stdout/stderr of all three passes was
captured in `$SCR/results.json` and `$SCR/passC.json` (scratch, removed before this seat yielded —
the load-bearing bytes are inlined below, nothing here cites a scratch path as evidence).

Counter-level demonstration (§4, F2) used a shared clone inside the same scratch:

```
$ git -C "$SCR" clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
$ git -C "$SCR/lane" rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r51/C2ExecOpenChecks/lane
```

## 3. The 27 OPEN rows — exit codes and classification

`rc A` = frozen-counter semantics (scratch cwd). `rc B` = lane cwd. `rc C` = `cd "$LANE" && <check>`
from the scratch cwd. A dash means the row has no check at all.

| id | class | check | rc A | rc B | rc C | first output line (A / B) | verdict |
|---|---|---|---|---|---|---|---|
| `R39-R2` | probe-work-dir-traceback | yes | **0** | 1 | 1 | A: `<no output>`<br>B: `<no output>` (traceback on stderr, see §5) | **needs-work** (A green is vacuous) |
| `R39-R4` | carried-residuals-bundle | yes | 2 | 2 | 2 | A: `python3: can't open file '…/work/plans/mutant_direction_check.py': [Errno 2] No such file or directory`<br>B: `SETUP counter plans/round39_c1_verify.py is not a round-38-list counter: missing=battery38_fixtures,attributed non_6_tuple_rows=7; this check reads the round-38 MUTANTS rows (id, clause, dir, adv, old, new) and its battery38 loader only` | **needs-work** |
| `R40-R5` | carried-residuals-bundle | **empty** | — | — | — | — | **not-a-check** |
| `R42-R1` | c1-counter-soundness-residuals | yes | 2 | 1 | 1 | A: `grep: plans/round42_c1_verify.py: No such file or directory`<br>B: `<no output>` | **needs-work** |
| `R42-R3` | c2-filler-control | yes | 2 | 1 | 1 | A: `grep: .ufo/waves/round-42/claims/control-c2-filler.txt: No such file or directory`<br>B: `<no output>` | **needs-work** |
| `R42-R5` | carried-residuals-bundle | yes | 2 | 2 | 2 | A: `python3: can't open file '…/work/plans/mutant_direction_check.py': [Errno 2] No such file or directory`<br>B: `SETUP counter plans/round42_c1_verify.py is not a round-38-list counter: missing=R37_REL,battery38_fixtures,attributed,FAMILY non_6_tuple_rows=14; this check reads the round-38 MUTANTS rows (id, clause, dir, adv, old, new) and its battery38 loader only` | **needs-work** |
| `R42-R6` | scratch-guard-exit-contract | yes | 2 | 1 | 1 | A: `<no output>`<br>B: `<no output>` | **needs-work** |
| `R42-R3-02` | registry-row-line-citation | yes | 2 | 1 | 1 | A: `grep: SKILL.md: No such file or directory`<br>B: `<no output>` | **needs-work** |
| `R42-R3-05` | entry-line-ref-off-by-one | yes | 2 | 1 | 1 | A: `grep: corpus/knowledge/tb2-circuit-fibsqrt-grader.md: No such file or directory`<br>B: `<no output>` | **needs-work** |
| `R42-R3-06` | readme-provenance-label | yes | 2 | 1 | 1 | A: `grep: corpus/README.md: No such file or directory`<br>B: `<no output>` | **needs-work** |
| `R42-R3-07` | registry-row-overstatement | yes | **0** | 1 | 1 | A: `grep: SKILL.md: No such file or directory`<br>B: `<no output>` | **needs-work** (A green is vacuous) |
| `R42-R3-08` | gate-undeclared-dependency | yes | **0** | 1 | 1 | A: `grep: plans/pkg_gate.py: No such file or directory`<br>B: `<no output>` | **needs-work** (A green is vacuous) |
| `R42-R3-09` | entry-vacuous-clause | **empty** | — | — | — | — | **not-a-check** |
| `R42-R3-18` | criterion-nonlanded-tool | yes | 1 | 1 | 1 | A: `<no output>`<br>B: `<no output>` | **stale-check** |
| `R42-R3-19` | criterion-cli-mismatch | yes | 1 | 1 | 1 | A: `<no output>`<br>B: `<no output>` | **stale-check** |
| `R42-R3-26` | guard-exit-code | yes | **0** | 1 | 1 | A: `<no output>`<br>B: `<no output>` | **needs-work** (A green is vacuous) |
| `R42-R3-27` | guard-selftest-gap | yes | 2 | 1 | 1 | A: `bash: line 1: test: : integer expected`<br>B: `<no output>` | **needs-work** |
| `R42-R3-32` | envelope-drift-record | yes | 2 | 1 | 1 | A: `grep: corpus/lessons/round-42.md: No such file or directory`<br>B: `<no output>` | **needs-work** |
| `R42-R3-33` | plan-mutant-numerator | **empty** | — | — | — | — | **not-a-check** |
| `R42-R3-34` | plan-missing-restore-control | **empty** | — | — | — | — | **not-a-check** |
| `R42-R3-35` | plan-missing-refusals | **empty** | — | — | — | — | **not-a-check** |
| `R42-R3-36` | plan-class-from-unfrozen-probe | yes | 1 | 1 | 1 | A: `ls: cannot access 'corpus/evidence/round43/': No such file or directory`<br>B: `<no output>` | **needs-work** |
| `R42-R3-37` | plan-host-dependent-cheat | **empty** | — | — | — | — | **not-a-check** |
| `R45-S5-7b` | v11-lookup-predictors | **empty** | — | — | — | — | **not-a-check** |
| `R45-S5-7c` | gate-p10-unpinned-uv | **empty** | — | — | — | — | **not-a-check** |
| `R45-S5-7d` | intent-brace-prefix | **empty** | — | — | — | — | **not-a-check** |
| `R45-S5-7e` | unattacked-mutation-items | **empty** | — | — | — | — | **not-a-check** |

Tally: **closable-now 0 · needs-work 15 · stale-check 2 · not-a-check 10** (27). Of the 17 rows
that carry a check, **0 pass in the lane cwd** and **4 pass only in the instrument's scratch cwd,
vacuously**.

## 4. Findings

### F1 — no open row is closable-now; the honest reading is "no defect in this set is fixed"

Every one of the 17 checks exits nonzero with the lane visible (`rc B` and `rc C` columns: 17/17
nonzero). Four of them (`R39-R2`, `R42-R3-07`, `R42-R3-08`, `R42-R3-26`) exit 0 in the frozen
counter's scratch cwd — not because the assertion holds but because the check cannot see its
target there. So a disposition of `fixed-verified` for **any** open row would be unsupported at
this revision, and for those four it would be a *false* green.

### F2 — the committed counter's check runner is cwd-blind, and four open rows exploit it

The mechanism (committed semantics, `cwd` = scratch; all reproduced in pass A above):

| row | check shape | why it greens in a scratch cwd | why it is red in the lane |
|---|---|---|---|
| `R39-R2` | `…; [ "$rc" -eq 2 ] \|\| [ "$rc" -eq 0 ]` | `plans/git_leak_probe.py` is absent from the scratch cwd, so `python3` exits **2**, which the check accepts | the probe **tracebacks** (`FileNotFoundError` on `mkdtemp(dir=…/absent)`) and exits 1 — the routed defect is live |
| `R42-R3-07` | `! grep -qF 'equal to the receipt row' SKILL.md` | `SKILL.md` absent → `grep` exits 2 → `!` turns it into 0 | the string is still at `SKILL.md:702` |
| `R42-R3-08` | `! grep -qF 'biopython==1.85' plans/pkg_gate.py` | same negation-over-a-missing-file artefact | the string is still at `plans/pkg_gate.py:276` |
| `R42-R3-26` | `…; [ "$rc" -eq 2 ]` on `plans/scratch_guard.py check "$d"` | the script is absent → `python3` exits 2 → accepted | the guard exits **1** where its docstring (`plans/scratch_guard.py:15-17`) promises 2 |

Counter-level demonstration, in a `git clone --shared` of the lane at `REV 4090c3d` (scratch only;
the lane itself untouched). Four open rows were given `owner=kengaku, disposition=fixed-verified`
and nothing else changed:

```
$ python3 plans/round51_routing.py --lane . --run-checks --scratch $SCR/cw
VERIFIED ran=4 passed=4 failed=0
…
PREDICATE R51-C2 fail          # still fails, on the ten empty checks (F4)
```

Four checks that are red in the lane were counted as four passes. Prefixing each of the four with
the one-token repair `cd "$LANE" && ` and re-running the same counter:

```
VERIFIED ran=4 passed=0 failed=4
  DETAIL CHECK_FAILED R39-R2 fixed-verified but check exits nonzero
  DETAIL CHECK_FAILED R42-R3-07 fixed-verified but check exits nonzero
  DETAIL CHECK_FAILED R42-R3-08 fixed-verified but check exits nonzero
  DETAIL CHECK_FAILED R42-R3-26 fixed-verified but check exits nonzero
PREDICATE R51-C2 fail
```

So the repair rule is mechanical and sufficient for this class: **every check that names a
lane-relative path must open with `cd "$LANE" && ` (or use `$LANE/…` absolute paths)**. The
counter exports `LANE` (committed `plans/round51_routing.py:129`), so no other change is needed.
13 of the 17 checks currently name a lane-relative path with no such prefix; all 17 should carry
it. The other leg — running checks with `cwd` = the lane — is already present as an **uncommitted
working-tree edit** (§8); it closes the same false-green without touching any ledger text. Either
leg is sufficient; applying both is harmless and keeps the checks correct whichever way the
instrument lands.

Related, and it constrains how the L1 can run controls: the counter prints
`ledger.relative_to(lane)` (`:118`), so a `--ledger` outside the lane raises
`ValueError: '…/ledger-copy.jsonl' is not in the subpath of '…/lane'` — measured under **both**
the committed version and the working-tree version (§8; the in-flight `.resolve()` on `--ledger`
does not help, `relative_to` still fails). A scratch ledger must live *inside* a lane copy, not
beside it.

### F3 — two checks are stale: they name files that never existed in any commit

`R42-R3-18` (`test -f plans/carried_direction_diff.py && test -f plans/sources_appendonly.py`) and
`R42-R3-19` (`python3 plans/sources_appendonly.py --lane . …`) point at two tools that are absent
from the tree and from the entire history:

```
$ git -C . log --oneline --all -- plans/sources_appendonly.py plans/carried_direction_diff.py | wc -l
0
$ ls plans/carried_direction_diff.py plans/sources_appendonly.py
ls: cannot access 'plans/carried_direction_diff.py': No such file or directory
ls: cannot access 'plans/sources_appendonly.py': No such file or directory
```

They are not "needs-work" in the sense of a small in-lane fix: the defect *is* that the criteria
name non-landed tools (`.ufo/waves/round-42/falsify/F42RevQuality.md:13`, D1). Two repairs are
measurable today, both read-only:

- point the checks at the tracked drafts, which do exist at `REV 4090c3d`:
  `test -f .ufo/waves/round-42/build/R42QualityDraft/carried_vs_rederived.py && test -f .ufo/waves/round-42/build/R42QualityDraft/sources_appendonly.py`
  → **rc 0** (measured); and
  `python3 .ufo/waves/round-42/build/R42QualityDraft/sources_appendonly.py . >/dev/null 2>&1; rc=$?; [ "$rc" -eq 0 ] || [ "$rc" -eq 1 ]`
  → **rc 0** (measured; the tool itself prints `SOURCES-APPENDONLY violations=16 arity=0` and exits 1, so this check greens on "the tool runs", not on "the defect is gone" — weak, and the L1 should prefer a check that asserts `violations=0`);
- or land the tools byte-identically (the alternative the falsify note already offered).

The CLI mismatch the row names is still live and separately measurable:
`python3 .ufo/waves/round-42/build/R42QualityDraft/sources_appendonly.py --lane .` →
`SETUP git log failed: fatal: cannot change to '--lane': No such file or directory`, **rc 2**
(the draft takes LANE positionally, `sources_appendonly.py:13`).

### F4 — ten rows carry no check, and the C2 predicate forbids that

`CHECKS absent=10` in `c2-before.txt` is exactly these ten open rows. `PREDICATE R51-C2` cannot
pass while any of them is empty, whatever their disposition, so the L1 needs a non-empty command
for each. Each proposal below is anchored on the row's own frozen source pointer (the file is
git-tracked) and was measured at `REV 4090c3d` from the scratch cwd with the repair prefix — all
ten exit **0**, so none of them changes a predicate reading on its own, and none is vacuous (the
file test runs first, so a deleted source reds the check):

| row | proposed `check` (measured rc 0) |
|---|---|
| `R40-R5` | `cd "$LANE" && test -f corpus/lessons/round-40-verifier-spotcheck.md && grep -qF "Carried: R3-from-r39" corpus/lessons/round-40-verifier-spotcheck.md` |
| `R42-R3-09` | `cd "$LANE" && test -f .ufo/waves/round-42/falsify/F42RevC2Package.md && grep -qF "D9 (nit) — entry:328" .ufo/waves/round-42/falsify/F42RevC2Package.md` |
| `R42-R3-33` | `cd "$LANE" && test -f .ufo/waves/round-42/falsify/F42CritPlanNext.md && grep -qF "mutant-list numerator is unbound" .ufo/waves/round-42/falsify/F42CritPlanNext.md` |
| `R42-R3-34` | `cd "$LANE" && test -f .ufo/waves/round-42/falsify/F42CritPlanNext.md && grep -qF "carried-cell red control is not specified" .ufo/waves/round-42/falsify/F42CritPlanNext.md` |
| `R42-R3-35` | `cd "$LANE" && test -f .ufo/waves/round-42/falsify/F42CritPlanNext.md && grep -qF "dishonest-green vectors" .ufo/waves/round-42/falsify/F42CritPlanNext.md` |
| `R42-R3-37` | `cd "$LANE" && test -f .ufo/waves/round-42/falsify/F42CritPlanNext.md && grep -qF "glibc/platform-dependent" .ufo/waves/round-42/falsify/F42CritPlanNext.md` |
| `R45-S5-7b` | `cd "$LANE" && test -f corpus/lessons/round-45-verifier-spotcheck.md && grep -qF "lookup predictors" corpus/lessons/round-45-verifier-spotcheck.md` |
| `R45-S5-7c` | `cd "$LANE" && test -f corpus/lessons/round-45-verifier-spotcheck.md && grep -qF "P10 unpinned" corpus/lessons/round-45-verifier-spotcheck.md` |
| `R45-S5-7d` | `cd "$LANE" && test -f corpus/lessons/round-45-verifier-spotcheck.md && grep -qF "brace-prefix bypass" corpus/lessons/round-45-verifier-spotcheck.md` |
| `R45-S5-7e` | `cd "$LANE" && test -f corpus/lessons/round-45-verifier-spotcheck.md && grep -qF "re-attack the two unattacked mutation items" corpus/lessons/round-45-verifier-spotcheck.md` |

These are evidence-pointer checks: they assert the routed finding's source still records the
defect. They are honest for the dispositions that do **not** run them (`routed`, `referral`,
`accepted-risk`, `refused-out-of-scope`, `fixed-historical` — the counter executes only
`fixed-verified` checks). If the L1 instead wants `fixed-verified` on any of these ten, the check
must assert the *fix*, not the source; `R42-R3-09` already has such a form and it is red today:
`! grep -qF "pytest's cache" corpus/knowledge/tb2-circuit-fibsqrt-grader.md` → **rc 1**, because
`corpus/knowledge/tb2-circuit-fibsqrt-grader.md:328` still reads
"this grader writes nothing outside its own `./sim` and pytest's cache."

### F5 — root-cause clusters: eight checks are three code edits, not eight

| cluster | rows | single fix | evidence |
|---|---|---|---|
| guard exit contract + selftest gap | `R42-R6`, `R42-R3-26`, `R42-R3-27` | make `plans/scratch_guard.py check` return **2** on `sentinel-unreadable` (docstring `:15-17` already promises it) and add the `check-sentinel-unreadable` selftest case | guard run: `CHECK red reason=sentinel-unreadable:Permission denied round=None want=* seats=0` → **rc 1**; selftest: `SELFTEST ok=36/36`, `grep -c 'check-sentinel-unreadable'` → **0** (check wants ≥37 and a `PASS exit=2` line) |
| mutant-direction loader | `R39-R4`, `R42-R5` | teach `plans/mutant_direction_check.py` the round-39/42 counter row shapes (or re-point both checks at a supported counter) | both counters refused with `SETUP … is not a round-38-list counter` rc 2 |
| carried-residuals bundle | `R40-R5` (no check), `R39-R4`, `R42-R5` | one decision: absorb or route out | `corpus/lessons/round-40-verifier-spotcheck.md:101` |

`R42-R3-02` and `R42-R3-05` are two separate one-line citation edits (`SKILL.md` has no `:238`:
`grep -c ':238' SKILL.md` → 0; the knowledge entry says `test_outputs.py:26-52`, the check wants
`26-53`).

## 5. Per-row fix scope for the L1 (what each needs-work row actually needs)

- **`R39-R2`** — `plans/git_leak_probe.py --work <absent dir>` must create the dir or exit 2 with a
  setup message (the row's own text, `corpus/lessons/round-39-verifier-spotcheck.md:134`). Today:
  ```
  Traceback (most recent call last):
    File ".../plans/git_leak_probe.py", line 301, in <module>
    File ".../plans/git_leak_probe.py", line 258, in main
      root = pathlib.Path(tempfile.mkdtemp(prefix="k39-glr-", dir=a.work))
  FileNotFoundError: [Errno 2] No such file or directory: '…/absent/k39-glr-0ivnob2m'
  rc=1
  ```
  Fix: wrap the `mkdtemp` in a setup guard → exit 2. Small, in-lane.
- **`R39-R4` / `R42-R5`** — direction check cannot load either counter; carried, not small.
- **`R42-R1`** — clauses 1-4 pass (`--unshare-ipc` 0, `--ro-bind-data` 0, `def path_ok` 0,
  `unattributed` 0); clause 5 fails: `grep -rqs 'command -v uv\|/usr/local/bin/uv' plans/battery42/`
  → **rc 1**, i.e. the `uv`-absence assumption the row asks to pin is still unpinned. Small
  (pin in `plans/battery42/` or the counter's PINS).
- **`R42-R3`** — clauses 1-2 pass (`CONTROL-C2-FILLER red-as-required` present; `"V9"` present in
  `plans/round42_c2_verify.py`); clause 3 fails: `grep -rqs 'pulls/\|state=closed' plans/*.py`
  → **rc 1**, the S124-style tier-B PR live-state reader the row asks for does not exist. Small.
- **`R42-R6` / `R42-R3-26` / `R42-R3-27`** — see F5; one guard edit closes three rows.
- **`R42-R3-02`** — `SKILL.md` row citation missing `:238`. One-line edit.
- **`R42-R3-05`** — entry cites `test_outputs.py:26-52`; `isqrt` ends at `:53`. One-line edit.
- **`R42-R3-06`** — `corpus/README.md:75` still labels S128 `(terminal-bench-2 @ 2fd12b88)`;
  the lane's own convention wants the OpenAgents-issue label. One-line edit.
- **`R42-R3-07`** — `SKILL.md:702` still carries "equal to the receipt row". Edit or accept.
- **`R42-R3-08`** — `plans/pkg_gate.py:276` still pins `biopython==1.85` for a stdlib-only probe.
- **`R42-R3-32`** — the anchor exists but the citation omits it:
  `.ufo/waves/round-42/integrate/measure-final.txt:938` reads
  `ENVELOPE end 17:52:40 exit=0 local_bin_listing_before=763032563d3739aa after=77408cab9a10361a CHANGED`,
  while `corpus/lessons/round-42.md:146` cites the file with no line number. Append-only
  correction, one line.
- **`R42-R3-36`** — `corpus/evidence/round43/` holds `feal-dry-cases-freeze.txt`,
  `feal-probe.txt`, `tb2-feal-differential-cryptanalysis` and **no** `prior-art` entry, while the
  raw prior-art material exists at `.ufo/waves/round-42/build/R42PlanNext/prior-art/`
  (`gh_issue_counts.txt`, `issues_detail.txt`). Fix: land a dated prior-art receipt there (the
  row's own fix text asks for exactly that). Small but requires a dated attestation.
- **`R40-R5`** plus the five `plan-*` rows and the four `R45-S5-*` rows — no check; see F4.

## 6. Limits

- This seat ran checks only; it did not attempt any fix, and did not touch `plans/`, `corpus/`,
  `PROVINCE.md`, `SKILL.md` or the ledger. Every fix scope above is a recommendation, not a change.
- Pass B (lane cwd) is a diagnostic, not a predicate under the committed instrument, which never
  runs a check from the lane; "rc B = 1" means only that the assertion is false when the target is
  visible. (§8: the in-flight working-tree edit makes the lane cwd the predicate cwd, in which
  case pass B *is* the predicate reading.)
- `rc C` shows the repair is necessary and sufficient for the cwd class only; it says nothing
  about whether a rewritten check is *strong*. Two of the rewrites I measured (`R42-R3-19`) green
  on "the tool runs" while the tool reports 16 violations, which is why §4/F3 flags it.
- The four false-green rows are demonstrated against a *clone* of the lane at `REV 4090c3d`; the
  demonstration's patched ledger is scratch-only and was deleted.
- Point-in-time: exit codes reflect the lane at `REV 4090c3d` (ledger byte-identical to the
  freeze `e07f131`). A sibling landing that edits `plans/scratch_guard.py`, `plans/git_leak_probe.py`
  or the knowledge entry would change specific rows above.
- No tool was installed or upgraded by this seat (nothing was needed; no pacman transaction was
  attempted).

## 8. Working-tree observation — the instrument is dirty, and the edit already closes F2

Not authored by this seat; observed while checking that nothing of mine had touched the lane
(`git status --porcelain` in the lane lists `M plans/round51_routing.py` — the only tracked
modification):

```
$ git diff --stat plans/round51_routing.py
 plans/round51_routing.py | 18 +++++++++++++-----
 1 file changed, 13 insertions(+), 5 deletions(-)
```

The diff (read-only) changes four things: `load_owners` now reads `id|repo|axes` rows from
`../shokunin.conf` and adds every `*-shokunin` directory as an owner; the check runner uses
`cwd=str(lane)` and `timeout=90` instead of `cwd=str(tmp)`/`60`; and `--ledger` is `.resolve()`d.

Measured effect on F2, with the same four rows patched to `fixed-verified` in a shared clone
(`cp` of the lane's working-tree instrument over the clone's copy, then the frozen command):

```
$ python3 plans/round51_routing.py --lane . --run-checks --scratch <scratch>/cw
VERIFIED ran=4 passed=0 failed=4
  DETAIL CHECK_FAILED R39-R2 fixed-verified but check exits nonzero
  DETAIL CHECK_FAILED R42-R3-07 fixed-verified but check exits nonzero
  DETAIL CHECK_FAILED R42-R3-08 fixed-verified but check exits nonzero
  DETAIL CHECK_FAILED R42-R3-26 fixed-verified but check exits nonzero
PREDICATE R51-C2 fail
```

So the in-flight edit closes the false-green **without any ledger text change**: the same four
rows go from `passed=4` to `passed=0`. Consequences the L1 should weigh:

- If that edit lands, my `cd "$LANE" &&` repair is redundant (still correct, still harmless) and
  the predicate reading for every check equals pass B above — 17/17 nonzero at this revision.
- If it does not land, the prefix is mandatory for any row marked `fixed-verified`.
- `--selftest` passes 11/11 under both versions (`[selftest] cases=11 failures=0` /
  `[selftest] ALL PASS`), so the loader change is not caught by the instrument's own selftest;
  the owner-universe widening is a live variable for the attribution seats (it decides which
  `owner` strings validate), not something this seat measured.
- `--ledger` outside the lane still raises `ValueError` under both versions (F2, last paragraph).

## 9. Scratch

`/fast/scratch/hyaku/kengaku-r51/C2ExecOpenChecks` (driver, `results.json`, `passC.json`, the
shared clone, `work/`, `tmp/`, the patched-ledger copy) was removed before this seat yielded. Free
space seen at start: `804G total, 250G used, 555G avail, 32%` on `/fast`. No scratch tree remains
on disk.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

VERDICT: 27 open rows run and classified — closable-now 0, needs-work 15, stale-check 2 (R42-R3-18, R42-R3-19: tools absent from every commit), not-a-check 10; no open row is honestly `fixed-verified` at REV 4090c3d, and four rows (R39-R2, R42-R3-07, R42-R3-08, R42-R3-26) green only vacuously under the committed counter's scratch cwd — measured `VERIFIED ran=4 passed=4` before and `ran=4 passed=0` after prefixing each check with `cd "$LANE" ` (and equally after substituting the lane's uncommitted instrument, which sets `cwd` to the lane); the ten empty checks block the C2 predicate and each has a measured, non-vacuous replacement in §4/F4.
