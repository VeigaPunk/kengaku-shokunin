# C2CritPredicate2 — wave-3 critic report (round 53, claim C2)

**Seat**: `C2CritPredicate2` (critic) · **Lane**: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
**Attack target**: `plans/round53_c2_tipstate.py` (sha256 `942d589d3012659edba783898e68a82649b99936ed18b15e2cb5026c65cf57cc`)
plus the ledger `plans/round53-tipstate.json` (78 rows).
**Lane tip I ran at**: `9ead4476bf55b1ea6490d0204b668195db4a4d1d` (the build-time tip in the brief,
`b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe`, advanced by one commit; `git diff b1f79a54..9ead4476 --stat`
shows **no change to `plans/round53_c2_tipstate.py`** — only wave-3 dispatch/spec files and
`corpus/evidence/round53/confirmations.json` — so the counter I attacked is byte-identical to the
one named in the brief. The L1 reconciles the tip).
**Scratch**: `/fast/scratch/hyaku/kengaku-r53/C2CritPredicate2/` (clone `lane/`, clean shared clone
`source/`, fixture repos under `fix/`, receipts under `out/`). Every fixture repo was created with
`git -C "$D" init -q` under a `mktemp`-style dir inside the seat scratch; the lane tree was only ever
read (`git archive HEAD` / `git show`).
**Tooling**: no new tool installed. Python 3.14 (`python3 --version` → 3.14.x, the host interpreter),
`git` and `uv` (`/home/vgpnk/.local/bin/uv`, already present) were the only binaries used.

---

## 1. Verdict in one paragraph

**A1 and A3 closed the wave-1 route list for the *static* legs** — heading rename, row-count
shortfall, `python3 -c pass`, shell wrappers, non-git source, older-commit source, and the timeout
cap are all caught, and the counter's own `--selftest` passes **52 cases, 0 failures**. **But the
executed leg has a hole that A1/A3 did not close, and it is the leg the whole claim rests on**:
`entry_mismatch` compares only the **script path** of the ledger argv against the script named in
the registry cell — never the argv's **arguments**, never the **command the cell actually
documents**, and never the exit the documented command produces. A ledger that re-points a
genuinely-red row at a flag that prints usage and exits 0 (`--help`, `--selftest`) is certified
`PREDICATE R53-C2 pass` with `entry_mismatch=0 bad_decl=0 bad_reason=0 row_set_pinned=ok`. The
`--help` cap (10 % of rows) is the only barrier, and the `selftest` kind has **no** cap at all, so
**all twelve red rows can be laundered green in one committed file** (`plans/round53-tipstate.json`).
This is the round-52 lesson `false-registry-cell` recurring one level down: the counter verifies the
ledger against itself, never against the registry's own documented command.

Two further residuals: a row that writes `.git/config` contaminates the next row on the same worker
(A3's `git reset --hard` + `git clean -ffdx` does not restore `.git/config`), which makes the
verdict **depend on `--jobs`**; and a malformed `timeout_s` string kills the counter with a
traceback **before any `PREDICATE` line is printed** (repeat of wave-1 F1, unclosed by A3).

**Recommendation to the L1**: C2 as frozen cannot be admitted on the executed leg alone. The
smallest safe correction is in §6.

---

## 2. What the counter's `--selftest` prints (the receipt the brief asks for)

```
$ TMPDIR=$S/tmp python3 plans/round53_c2_tipstate.py --selftest
...
SELFTEST env-token-not-visible-to-row rc=0 ok
SELFTEST row-commit-does-not-leak-to-next-row rc=0 ok
SELFTEST operator-timeout-caps-the-ledger-timeout rc=1 ok
SELFTEST ledger-duplicate-json-key rc=1 ok
SELFTEST source-not-a-git-tree rc=1 ok
SELFTEST dirty-source-tree rc=1 ok
SELFTEST source-older-than-lane rc=1 ok
SELFTEST pinned-row-set-honest rc=0 ok
SELFTEST pinned-row-set-deletion rc=1 ok
SELFTEST pinned-row-set-extra-row rc=1 ok
SELFTEST pinned-extra-name-missing rc=1 ok
SELFTEST frozen-constants ok
SELFTEST cases=52 failures=0
```
rc=0. Full receipt: `.ufo/waves/round-53/w3/C2CritPredicate2/selftest.txt` (copied from
`out/selftest.txt`).

---

## 3. The honest baseline on the real tree (the number the L1 needs)

```
$ python3 plans/round53_c2_tipstate.py --lane . --source <clean shared clone of 9ead4476> --work <scratch> --jobs 4 --timeout 900
ROWS registry=78 ledger=78 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok
ARGV entry=74 selftest=4 help=0 help_limit=7.8
SOURCE rev=9ead4476bf55b1ea6490d0204b668195db4a4d1d clean=yes lane_rev_equal=yes
  MISMATCH round53-c1 declared exit=0 observed exit=1 sec=0.8
RUN executed=78 timeout=0 mismatched=1 evidence_missing=0
TIPSTATE declared_green=66 declared_red=12 observed_green=65 observed_red=13
PREDICATE R53-C2 fail
rc=1 elapsed=311s
```
Receipt: `out/baseline.txt`. **The single mismatch is `round53-c1`**: at this tip
`plans/round53_c1_triage.py --lane .` prints `PRIOR-ART rows=0 tasks_covered=0/20 known=0 new=0
urls=0` and exits 1 — the PRIOR-ART leg has no rows yet (wave-2's prior-art work has not landed),
so the C1 row is **red at the tip while the committed ledger declares it green**. This is a
ledger-staleness finding the L1 must fix before any C2 run can pass; it is *not* a counter defect.
The C2 counter caught it correctly.

---

## 4. The attacks

Sixteen attacks, each a fixture + the real counter invoked by the real command shape. Fixtures
export the lane's committed tree verbatim, so the registry row set, the `row_set_pinned` digest and
the `FROZEN_NAMES_SHA` all hold unless the attack targets them. Attack scripts are under
`.ufo/waves/round-53/w3/C2CritPredicate2/scripts/`, receipts under the same directory.

**Fixture construction** (all attacks): the lane tree is exported with `git archive HEAD` into a
`git init` repo under the seat scratch; every row's script is replaced by a trivial
`print('stub ok'); sys.exit(0)` stub **except** `plans/round53_c2_tipstate.py` (the counter under
test), and except the rows a given attack needs real; the ledger is then written and committed;
a clean shared clone of that fixture is the `--source`.

### 4.1 The wave-1 route list — all CAUGHT (A1/A3 hold)

| # | Attack | Verdict | Evidence line |
|---|---|---|---|
| A1 | Ledger zero rows + heading renamed to `## Registry` | **CAUGHT** | `ROWS registry=0 ledger=0 ... headings=0 row_set_pinned=BAD` → `PREDICATE R53-C2 fail` (`out/a1-zero-rows-renamed-heading.txt`) |
| A2 | 77 of 78 rows (one row deleted from registry **and** ledger) | **CAUGHT** | `ROWS registry=77 ledger=77 ... row_set_pinned=BAD` → fail (`out/a2-77-of-78-rows.txt`) |
| A3 | argv `python3 -c pass <script>` | **CAUGHT** | `ENTRY-MISMATCH adoption-check` → fail (`out/a3-python-c-pass.txt`) |
| A3b | argv `sh -c "python3 plans/...; exit 0" plans/...` | **CAUGHT** | `ENTRY-MISMATCH adoption-check` → fail (`out/a3b-shell-wrapper.txt`) |
| A4 | `--source` = a plain directory (no `.git`) | **CAUGHT** | `SOURCE not a git work tree clean=NO` → fail (`out/a4-source-non-git.txt`) |
| A5 | `--source` = an older commit than the lane | **CAUGHT** | `SOURCE rev=af4ebb29... clean=yes lane_rev_equal=NO` → fail (`out/a5-source-older-commit.txt`) |
| A7 | ledger `timeout_s=100000` above the operator cap `--timeout 5` | **CAUGHT** | `TIMEOUT adoption-check after 100000s` + `TIMEOUT round53-c2 after 5s`, `RUN … timeout=2` → fail (`out/a7-timeout-above-operator-cap.txt`) — note the row was killed at the **operator's** 5 s, i.e. A3's cap holds; the printed "after 100000s" is the *ledger's* number, not the effective one (cosmetic, §5.5) |
| D1 | 12 red rows re-declared green via `--help` (15.4 % > the 10 % cap) | **CAUGHT** | `ARGV entry=62 selftest=4 help=12 help_limit=7.8` → fail (`out/d1-launder-all-twelve-via-help.txt`) |

### 4.2 The residual routes — LANDED (these are the findings)

| # | Attack | Verdict | Evidence |
|---|---|---|---|
| **B1** | **One genuinely-red row (`round51-surfaces`) re-declared green by pointing its argv at `--help`** | **LANDED** | `PREDICATE R53-C2 pass` (`out/b1-launder-red-row-via-help.txt`) |
| **B2** | **Seven red rows re-declared green via `--help`** (7/78 = 8.97 %, under the 10 % cap) | **LANDED** | `ARGV entry=67 selftest=4 help=7 help_limit=7.8` … `PREDICATE R53-C2 pass` (`out/b2-launder-seven-red-rows.txt`) |
| **C1** | **One red row re-declared green via `--selftest` and `kind=selftest`** (no cap on selftest) | **LANDED** | `ARGV entry=73 selftest=5 help=0` … `PREDICATE R53-C2 pass` (`out/c1-launder-via-selftest-kind.txt`) |
| **D3** | **All twelve red rows re-declared green via `--selftest`** (selftest kind uncapped) | **LANDED** | `ARGV entry=62 selftest=16 help=0` … `PREDICATE R53-C2 pass` (`out/d3-launder-all-twelve-via-selftest.txt`) |
| **D2** | Mixed: 7 via `--help` + 5 via `--selftest` → all twelve laundered | **LANDED** | `ARGV entry=62 selftest=9 help=7 help_limit=7.8` … `PREDICATE R53-C2 pass` (`out/d2-mixed-laundering.txt`) |
| **A10** | Ledger argv's **arguments** replaced (`--expect` → a different path) while the script path is unchanged | **LANDED** | `PREDICATE R53-C2 pass` (`out/a10-argv-argument-substitution.txt`) |
| **A13** | The registry's **entry cell** rewritten to name a different instrument (`plans/always_ok.py`); row *names* untouched so the pin still holds | **LANDED** | `ROWS registry=78 ... row_set_pinned=ok`, `PREDICATE R53-C2 pass` (`out/a13-registry-cell-rewritten.txt`) |
| **A9** | A gate that cannot fail (instrument bytes replaced by `always exit 0`) declared green | **LANDED** | `PREDICATE R53-C2 pass` (`out/a9-always-exit-0-gate.txt`) — but see §5.4: this one is **explicitly out of scope** by A1 |
| **A11/B4** | A row writes `.git/config` in its worker; the next row reads it | **LANDED** | jobs=1 → `PREDICATE R53-C2 pass`; jobs=4 → `MISMATCH anchor-digest-check declared exit=0 observed exit=1` → `PREDICATE R53-C2 fail` — **same tree, same ledger, different verdict** (`out/b4.comparison.txt`, `out/a11-git-config-contamination-jobs1.txt`, `out/a11-git-config-contamination-jobs4.txt`) |
| **A12** | Ledger `timeout_s` = the string `"2.5"` | **LANDED (crash)** | `ValueError: invalid literal for int() with base 10: '2.5'` at `plans/round53_c2_tipstate.py:129`, **no `PREDICATE` line at all** (`out/a12-timeout-string.txt`) |

### 4.3 Controls (proving the fixtures are honest)

| Control | Result | Receipt |
|---|---|---|
| All 78 rows green, all scripts stubbed → counter must pass | `PREDICATE R53-C2 pass` | `out/control.txt` |
| Same tree + same honest ledger, `--jobs 1` vs `--jobs 4` | **both** `PREDICATE R53-C2 pass` — the verdict is deterministic when nothing contaminates | `out/a15-jobs1.txt`, `out/a15-jobs4.txt` |
| A worker that runs `git gc --prune=now` in the `--shared` clone | `PREDICATE R53-C2 pass`, and the source repo still passes `git fsck` (rc=0) — no object-store damage | `out/a14-worker-git-gc.txt`, `out/a14-worker-git-gc.after` |
| A red row whose `evidence` fragment is borrowed from **another** row's output | **CAUGHT**: `EVIDENCE-MISSING` (the fragment must be in *its own* output) | `out/a6-evidence-from-other-row.txt` |
| A row that commits inside its worker and leaks to the next row | **CAUGHT** (A3's reset holds for *file* leaks) | `out/a8-commit-leaks-to-next-row.txt` |

---

## 5. The findings, with the mechanism

### 5.1 FINDING 1 (highest) — the executed leg never checks the argv's arguments, so red rows can be laundered green

**Mechanism.** `plans/round53_c2_tipstate.py:78-82` extracts the script from the registry cell:

```python
def row_script(line: str) -> str | None:
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    entry = cells[2] if len(cells) > 2 else ""
    m = SCRIPT.search(entry)          # the FIRST "python3 <path>.py" in the entry cell
    return m.group(1) if m else None
```

and `:149-159` checks the ledger argv against that path:

```python
if argv[0] == "python3":
    return argv[1] == script           # the SCRIPT PATH — nothing else
```

So `entry_mismatch` asks *"does the ledger name the same file?"* and never *"does the ledger run the
command the registry documents?"*. The registry cell for `round51-surfaces` is
`` `python3 plans/round51_surfaces.py --lane .` `` (lane root; …), but the ledger may say
`["python3", "plans/round51_surfaces.py", "--help"]` and the counter compares the exit of
`--help` (0) with the declared exit (0) — never running `--lane .` at all.

**Why it is not a "gate that cannot fail" case (which A1 puts out of scope).** A1's carve-out says
*"a C2 ledger entry for a gate that cannot fail (a script that always exits 0) is still truthful;
the counter measures declaration against observation, not the strength of the instrument."* That
carve-out is about the **instrument's strength**. Here the instrument is **unchanged and genuinely
red**; the ledger simply points at a *different invocation of the same instrument* whose exit code
says nothing about the row's tip-state. The registry cell documents the verdict map
(`` `0` frozen predicate holds … · `1` any of DRIFT, STALE, … NUMBER-DRIFT … non-zero ``); the
counter's `PREDICATE R53-C2 pass` certifies a **registry cell that is still false**, because the
documented command was never executed. The claim's own words — *"every registry row has exactly
one entry … each entry's argv names the same script as its row's entry cell"* — make the *script* the
object of comparison, and the "same script" reading is what makes the laundering possible.

**Concretely (B1).** On the real lane tree, `round51-surfaces` is red at the tip. Its documented
command exits 1:

```
$ python3 plans/round51_surfaces.py --lane .
exit=1
ANCHORS total=20 dup=0 missing=0
DRIFT 0
STALE 3
  DETAIL STALE SF10 probe=absent state=present (digest 584f158b does not start with pin 90c87c88)
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 171, probe says SOURCES rows=186
RESOLVE observed_present=11 floor=13 verdict=violated
```
(receipt `out/b1.documented-command-output.txt`; the ledger's committed `evidence` for this row is
`NUMBER-DRIFT SF14 row claims 171, probe says SOURCES rows=186` — the same defect.)

With **one committed file** (`plans/round53-tipstate.json`) changed so that this row's argv is
`["python3","plans/round51_surfaces.py","--help"]`, `kind=selftest`/`help`, `exit=0`,
`state=green`, and its `evidence`/`reason` removed, the counter prints:

```
ROWS registry=78 ledger=78 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok
ARGV entry=73 selftest=4 help=1 help_limit=7.8
SOURCE rev=50778f74dd0b5933b755de52328c0b3dcaaf23f6 clean=yes lane_rev_equal=yes
RUN executed=78 timeout=0 mismatched=0 evidence_missing=0
TIPSTATE declared_green=78 declared_red=0 observed_green=78 observed_red=0
PREDICATE R53-C2 pass
```
(`out/b1-launder-red-row-via-help.txt`; registry cell quoted at `out/b1.registry-cell.txt`).

**Scale.** The `--help` cap is the only barrier and it is a *fraction* cap, not a *red-row* cap:
7 rows of 78 (8.97 %) are allowed (B2 → pass). The `selftest` kind has **no** cap at all, so all
twelve red rows can be laundered at once (D3 → `ARGV entry=62 selftest=16 help=0` …
`PREDICATE R53-C2 pass`; D2 mixes 7 help + 5 selftest → pass). The counter's own `kind_ok`
(`:162-165`) only requires the *kind* to agree with the argv's flags — it does not require the
argv to be the command the registry documents.

**Why this matters for the axis.** C2 is a **calibration** claim: the point is that the registry's
self-assessment is *true at the tip*. If a single committed JSON file can flip a red row to green
without touching a single instrument, the counter certifies a **false registry cell** — the exact
round-52 defect the round claims to close (`false-registry-cell`, `plans/round-53-claims.md`
"Carried routed defects"). The wave-1 attacks (C2CritLedgerReach) attacked the *static* legs and
never tried this: they forged the ledger's **row set**, **argv shape** and **declared exit codes**,
but never tried **re-pointing the argv at a different flag of the same script**.

**Smallest safe correction** (in priority order):
1. **Compare the whole argv, not just the script.** Extract the *documented* command from the
   registry cell (the first backticked command in cell 2) and require the ledger argv to be that
   command — modulo a whitelisted, cell-declared variation (`--selftest` only when cell 4 documents
   it). This makes `entry_mismatch` mean what its name says.
2. **Or: run the documented command too.** For every row, re-execute the *cell's* command and
   require the ledger's declared exit to match **that** exit as well. Under this rule B1/B2/C1/D2/D3
   all fail (`round51-surfaces --lane .` exits 1, the ledger declared 0).
3. **Close the `selftest` gap** by applying the 10 % fraction cap to `selftest` as well (or by
   requiring a selftest row's cell 4 to document the exact argv).
4. **Pin the registry cells, not just the row names.** `FROZEN_NAMES_SHA` pins the *sorted row
   names* only; the *entry cell* that says which instrument a row runs is unpinned, so A13 (cell
   rewritten to `plans/always_ok.py`) also passes with `row_set_pinned=ok`. A digest over
   `name → documented command` closes A13 and A10 together.

### 5.2 FINDING 2 — the verdict depends on `--jobs`: A3's worker reset does not restore `.git/config`

`Worker.reset()` (`:127-135`) does `git reset --q --hard <clone-rev>` then `git clean -q -ffdx`.
Neither restores `.git/config`, which lives in the worker's `.git` directory, not in the work tree.
A row that runs `git config --local <key> <value>` therefore contaminates the **next row on the same
worker**. Measured (B4, `out/b4.comparison.txt`): identical tree, identical ledger,

```
=== jobs=1 (rc=0) ===                       === jobs=4 (rc=1) ===
RUN executed=78 timeout=0 mismatched=0       MISMATCH anchor-digest-check declared exit=0 observed exit=1 sec=0.1
PREDICATE R53-C2 pass                       RUN executed=78 timeout=0 mismatched=1 evidence_missing=0
                                            PREDICATE R53-C2 fail
```
The honest-ledger control (A15) is deterministic across the same two `--jobs` values (both pass),
so the flip is caused by the contamination, not by scheduling noise. A3 fixed the *file*-leak
variant (A8 is CAUGHT) but not the *config*-leak variant — the wave-1 finding **B1 "git-config-carries"**
survives A3.

**Smallest safe correction**: after `reset --hard` + `clean -ffdx`, also restore the config — e.g.
`git config --local --replace-all` back to the clone's original, or simplest and safest: **re-create
the worker clone between rows** (or at least `rm -rf .git/config` and re-`git init`), or run each row
in a **fresh** clone. A cheaper variant: `git -C <dir> config --local --list` is snapshotted at clone
time and restored with `git config --local --replace-all` per key.

### 5.3 FINDING 3 — a malformed `timeout_s` kills the counter before the verdict

`run_row` computes `t = min(int(spec.get("timeout_s") or default_timeout), default_timeout)`
(`:129`) **outside** any try/except, and `int("2.5")` raises. The exception escapes
`run_row` → `ThreadPoolExecutor.map` → `main`, so the process dies with a traceback and **no
`PREDICATE` line is printed at all** (`out/a12-timeout-string.txt`):

```
  File ".../plans/round53_c2_tipstate.py", line 129, in run_row
    t = min(int(spec.get("timeout_s") or default_timeout), default_timeout)
ValueError: invalid literal for int() with base 10: '2.5'
```
rc=1, no verdict line. This is wave-1 **F1** ("timeout-string"), unclosed by A3 (A3 added the cap
but kept the unguarded `int()`). The counter must **fail closed with a `PREDICATE R53-C2 fail`
line**, not die: a receipt with no verdict line cannot be distinguished from a crash of the harness.
The same unguarded parse shape would also accept a negative `timeout_s` (a `subprocess.run` timeout
of `-1` means "no timeout" in some code paths).

**Smallest safe correction**: validate `timeout_s` in the static legs (must be an `int` > 0) and
reject it with `BAD-DECL`, or wrap the `int()` in `try/except` and set `rc="ERROR"`.

### 5.4 FINDING 4 (already out of scope by A1 — reported for completeness, not as a new objection)

**A9 — the instrument's bytes are unpinned.** Replacing a row's script with `always exit 0` and
declaring it green passes (`out/a9-always-exit-0-gate.txt`). A1 names this explicitly
(*"A C2 ledger entry for a gate that cannot fail … is still truthful"*), so it is **not** a counter
defect and I do not treat it as one. It is worth recording that A1's carve-out covers the
*instrument*; it does **not** cover the *argv* (Finding 1), which is a different object and is
unmentioned. Note also that in the real tree the 78 row scripts are **not** digest-pinned anywhere
(only `plans/round53_c1_classify.py` and the label files are), so a lane edit to a gate's script
would silently change its tip-state with no counter noticing — but that is the accepted trade.

### 5.5 Cosmetic (not a defect, noted for the receipt)

- `TIMEOUT <row> after <n>s` prints the **ledger's** `timeout_s`, not the **effective** timeout
  (`out/a7-timeout-above-operator-cap.txt` shows `TIMEOUT adoption-check after 100000s` while the row
  was killed at the operator's 5 s). The receipt therefore misstates the elapsed budget; the
  behaviour is correct.
- The `RUN` line counts `executed` over the rows that survived the static legs, so a run with
  `entry_mismatch>0` prints `executed=77` for 78 registry rows. Harmless, but a reader can
  mis-read `executed=77` as "one row was skipped".

---

## 6. The smallest safe correction (for the L1)

The C2 counter needs **one** new leg to close Finding 1, plus two small fixes:

**(a) The documented-command leg (closes B1, B2, C1, D2, D3, A10, A13).** For each registry row,
extract the **documented** command from the cell (the first backticked command in cell 2 — the
registry already writes every entry that way) and re-execute **that** command in the scratch clone,
requiring its exit to equal the ledger's declared exit. Concretely, in `static_legs` keep the
documented argv next to `script`, and in the run loop execute **both** the ledger argv and the
documented argv; a row passes only if **both** observed exits equal the declared exit. Under this
rule:

* B1/B2/C1/D2/D3 → the documented `round51_surfaces.py --lane .` exits 1 while the ledger declared
  0 → `MISMATCH` → fail.
* A10 → the documented `--expect <expect.json>` differs from the ledger's → `MISMATCH` → fail.
* A13 → the cell's documented command is `plans/adoption_check.py …` but the ledger says
  `plans/always_ok.py` → the documented command's exit is compared → fail.

This is one extra `subprocess.run` per row (78 rows) and needs no new digest, no new constant, and
no change to any frozen threshold — so it does **not** require a new amendment to the claim text,
only to the counter.

**(b) The `selftest` cap (closes D3/D2).** Apply `MAX_HELP_FRACTION` to `selftest` as well, or
require a selftest row's cell 4 to document exactly the ledger's argv. *(Optional if (a) lands:
with (a), the laundered rows fail on the documented command regardless of kind.)*

**(c) The worker reset (closes Finding 2).** Restore `.git/config` between rows, or re-create the
worker clone per row.

**(d) The `timeout_s` parse (closes Finding 3).** Validate `timeout_s` in the static legs (int > 0)
and report `BAD-DECL`, or catch the `ValueError` and emit `rc="ERROR"`.

With (a) alone, the 12 currently-red rows are protected; the C1 row's `PRIOR-ART` red (§3) would
still be caught. **My recommendation is that C2 not be admitted until (a) lands and is shown to fail
B1/B2/C1/D2/D3**, because the counter's `PREDICATE R53-C2 pass` currently certifies a registry
whose documented commands were never executed — which is the exact property the claim asserts.

---

## 7. Files produced (all inside the seat directory; scratch removed at exit)

* Report: `.ufo/waves/round-53/w3/C2CritPredicate2.md` (this file).
* Receipts (one file per attack, plus the suite logs): `.ufo/waves/round-53/w3/C2CritPredicate2/`
  — `control.txt`, `baseline.txt`, `selftest.txt`, `a1…a15*.txt`, `b1…b4*.txt`,
  `c1…c4*.txt`, `d1…d3*.txt`, `e0…e1*.txt`, `attacks*.log`, `summary*.json`,
  `b1.registry-cell.txt`, `b1.documented-command-output.txt`, `b4.comparison.txt`,
  `e.mismatched-rows.txt`, `a14-worker-git-gc.{before,after}`.
* Attack drivers (reproducible): `.ufo/waves/round-53/w3/C2CritPredicate2/scripts/`
  — `harness.py` (fixture builder), `attacks.py` (A-suite), `attacks_b.py` (B-suite),
  `attacks_c.py` (C-suite), `attacks_d.py` (D-suite), `attacks_e.py` (E-suite, real tree),
  `measure.sh`, `selftest-exits.sh`, `redrow-exits.sh`, `baseline.sh`.

Every attack is reproducible with one command from the seat scratch, e.g.

```sh
cd /fast/scratch/hyaku/kengaku-r53/C2CritPredicate2
python3 attacks_b.py      # B1-B4
python3 attacks_d.py      # D1-D3
```

The lane tree was never modified: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status
--porcelain` shows only the orchestrator's own untracked wave-3 files plus my seat directory; no
`git add/commit/push/stash/checkout/reset/pull` was run in the lane or the fleet repo, and every
fixture git call named `-C "$D"`.

---

## 8. Note on the instrumented tool outputs

No tool output was inconsistent with its described behaviour, except one worth recording for the
harness: `subprocess.run(..., timeout=<int>)` treats a **negative** timeout as "no timeout" in some
code paths, and the counter's `timeout_s` is parsed without a lower bound (§5.3), so a ledger
`timeout_s: -1` is a latent way to make a row run unbounded. I did not observe it fire (the
operator's `--timeout` cap is applied as a `min()`, which keeps the effective value non-negative
only when `default_timeout` is positive — it is, at 900).
