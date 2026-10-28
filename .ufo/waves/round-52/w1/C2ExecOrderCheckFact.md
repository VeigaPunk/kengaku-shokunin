# C2ExecOrderCheckFact — facts on the `order-check` registry row's SELFTEST-UNBACKED leg

Seat: `C2ExecOrderCheckFact` (executor, wave 1 of 2). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Axis judged: operability (R52-C2). Leaf member — no dispatch, no lane edits, no commits, no mutating git/jj.

**Bottom line:** the row is **truthful**; the counter's failure is a **mis-attribution false positive**.
`plans/order_check.py` declares exactly three flags (`--lane`, `--claims`, `--receipt`, all required)
and has **no** self-test mode; the row's self-test cell says exactly that. The cell trips the frozen
rule only because it names the *falsifier* script `plans/round40_c1_verify.py` as its single `.py`
path while quoting flags that belong to `plans/order_check.py`. A truthful replacement cell text is
supplied below and is **measured** to clear the leg (`SELFTEST-UNBACKED 0`).

---

## 1. Revision measured

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
07ea2084053f5112ea797a653e6a3a96e8cf4a64
$ git -C ... log --oneline -3
07ea208 round-52: amendment A1 (per-test classification + hardened CONFIRMED leg) with disclosure receipt
1315234 round-52: freeze C1 (novelty) + C2 (operability) claims, counters, population and wave-1 spec
30801b4 round-51 verifier spot-check (integrator, hyaku): non-author admit/reject
$ git -C ... diff --stat 30801b479e3418c11089b8586178b6960216f364 HEAD -- SKILL.md plans/order_check.py plans/round52_c2_registry.py
 plans/round52_c2_registry.py | 194 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 194 insertions(+)
```

`SKILL.md` and `plans/order_check.py` are **byte-identical between the base tip `30801b47` and the
current HEAD**, so every measurement below holds at the base tip. `plans/round52_c2_registry.py` did
not exist at the base tip (it *is* the frozen counter, added in the freeze commit `1315234`).
Amendment A1 (`07ea208`) touched only `plans/round-52-claims.md` (C1 section, 50 appended lines),
`plans/round52_c1_grader_audit.py` and `.ufo/waves/round-52/claims/a1-observation.txt` —
**C2's rules and the C2 counter are untouched by A1**.

## 2. FACT A — the script's argparse block (`plans/order_check.py`)

Read raw, `plans/order_check.py:141-146`:

```
141 def main(argv: list[str] | None = None) -> int:
142     ap = argparse.ArgumentParser(description="order-of-operations gate (frozen probe before its receipt)")
143     ap.add_argument("--lane", required=True, help="lane (git work tree) to read; nothing is written")
144     ap.add_argument("--claims", required=True, help="the round's frozen claims file, repo-relative")
145     ap.add_argument("--receipt", required=True, help="the round's probe receipt, repo-relative")
146     args = ap.parse_args(argv)
```

- **Declared flags: exactly three** — `--lane` (required), `--claims` (required), `--receipt`
  (required). No sub-parsers, no other `add_argument` anywhere in the file.
- **No self-test flag.**

```
$ grep -n "selftest\|self-test\|self_test" plans/order_check.py   # -> no match (0 hits)
$ grep -n "add_argument" plans/order_check.py
143:    ap.add_argument("--lane", required=True, ...)
144:    ap.add_argument("--claims", required=True, ...)
145:    ap.add_argument("--receipt", required=True, ...)
```

The word "selftest" does not occur in the script's bytes at all. The row's own entry-cell note
("all three flags are required, `plans/order_check.py:143-145`") is **accurate**.

## 3. FACT B — the row's eight cells (`SKILL.md:590`)

`SKILL.md` line 590, `|`-split into the eight registry columns
(`name | kind | entry | verdict map | self-test | pinned values | write scope | owner`):

| # | column | cell text (verbatim) |
|---|---|---|
| 1 | name | `` `order-check` `` |
| 2 | kind | `gate` |
| 3 | entry | `` `python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round40/db-wal-probe.txt` (lane root; all three flags are required, `plans/order_check.py:143-145`) — Q30's order-of-operations gate `` |
| 4 | verdict map | `` `0` order holds: `ORDER ok no claims file committed at or before the receipt shows the frozen probe executed`, then `ORDER RESULT PASS` (`plans/order_check.py:204-206`) · `1` order broken: one `ORDER FAIL <clause> …` line per broken clause (`freeze-contains-receipt`, `receipt-before-claims`), one `ORDER HIT <path>@<commit>:<n> kind=<kind> …` line per claims blob that shows the probe executed, then `ORDER FAIL <clauses> hits=<n>` and `ORDER RESULT FAIL` (`plans/order_check.py:184-202`) · `2` could-not-evaluate: `ORDER ERROR <reason>` on stderr then `ORDER RESULT ERROR` — not a git work tree, claims or receipt never committed in HEAD, claims file not named `round-NN-claims.md`, path outside the lane, mid-scan `git cat-file` failure, argparse (`plans/order_check.py:151-175`, handler `:207-210`) `` |
| 5 | **self-test (the cell under audit)** | `` no `--selftest` in the script; falsifiers are external — `plans/round40_c1_verify.py` mutants `O04` (`rc-silence`), `O12` (`rc-error`), `O14` (`error`), each witnessed pre-freeze (`.ufo/waves/round-40/claims/witness/`), and the measured controls `--receipt corpus/evidence/round39/git-leak-probe.txt` → `ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0`, exit 1; `--claims plans/round-99-claims.md` → `ORDER ERROR claims not committed in HEAD`, exit 2 `` |
| 6 | pinned values | `` reads committed history only and pins nothing itself; the population is the claims file and the receipt named per run; the round-40 pair is `freeze bbb1095`, `receipt_commit 055748f`, `claims_dir .ufo/waves/round-40/claims/` `` |
| 7 | write scope | `` none — `rev-parse`, `log`, `rev-list`, `ls-tree`, `cat-file`, `merge-base --is-ancestor` only; writes nothing, imports no probe/gate/counter, never runs the probe it polices `` |
| 8 | owner | `kengaku` |

## 4. FACT C — every substantive claim in cell 5 is TRUE (measured)

| cell-5 claim | verdict | evidence |
|---|---|---|
| "no `--selftest` in the script" | **TRUE** | §2: 0 hits for `selftest`; argparse declares only `--lane/--claims/--receipt` |
| falsifiers are `plans/round40_c1_verify.py` mutants `O04` (`rc-silence`), `O12` (`rc-error`), `O14` (`error`) | **TRUE** | `plans/round40_c1_verify.py:209` `("O04", "order", "-", "rc-silence",`, `:215` `("O12", "order", "-", "rc-error",`, `:219` `("O14", "order", "-", "error",` — all three target the `order` instrument |
| "each witnessed pre-freeze (`.ufo/waves/round-40/claims/witness/`)" | **TRUE** | that dir exists: `w_anchor.py  w_ledger.py  w_order.py` |
| control `--receipt corpus/evidence/round39/git-leak-probe.txt` → `ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0`, exit 1 | **TRUE, reproduced byte-for-byte** | run below |
| control `--claims plans/round-99-claims.md` → `ORDER ERROR claims not committed in HEAD`, exit 2 | **TRUE, reproduced** | run below |

Commands (read-only; the gate spawns only `git` plumbing and writes nothing):

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt ; echo "exit=$?"
ORDER claims=plans/round-40-claims.md round=40 freeze=bbb109505670192035ef63d7c8b37733e99fa1a3
ORDER receipt=corpus/evidence/round39/git-leak-probe.txt receipt_commit=6a1eb5e1da4a435940b821e28530c31f3411549c claims_dir=.ufo/waves/round-40/claims/
ORDER FAIL freeze-contains-receipt bbb109505670192035ef63d7c8b37733e99fa1a3 already has corpus/evidence/round39/git-leak-probe.txt
ORDER FAIL receipt-before-claims 6a1eb5e1da4a435940b821e28530c31f3411549c is an ancestor of bbb109505670192035ef63d7c8b37733e99fa1a3
ORDER scanned commits=0 file_entries=0 distinct_blobs=0
ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0
ORDER RESULT FAIL
exit=1

$ python3 plans/order_check.py --lane . --claims plans/round-99-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt ; echo "exit=$?"
ORDER ERROR claims not committed in HEAD: plans/round-99-claims.md
ORDER RESULT ERROR
exit=2
```

The verdict-map cell is also accurate: `plans/order_check.py:184` = the `freeze-contains-receipt`
test, `:190` = the `receipt-before-claims` test, `:196` = the `ORDER HIT` print, `:201-202` =
`ORDER FAIL <clauses> hits=<n>` + `ORDER RESULT FAIL`, `:204-206` = `ORDER ok …` + `ORDER RESULT PASS`
+ `return 0`, `:207-210` = the `SetupError` handler (`ORDER ERROR` on stderr → `ORDER RESULT ERROR`
→ `return 2`).

**Conclusion of FACT C: no clause of the `order-check` row is false.** The row does not need a
content correction; it needs the self-test cell *rewritten so the counter attributes the flags to
the script they belong to*.

## 5. FACT D — why the frozen counter flags the row (mechanism, quoted)

`plans/round52_c2_registry.py:67-81` (raw):

```python
def selftest_unbacked(cell: str, lane: Path) -> bool:
    """True when the self-test cell names exactly one script and one flag that the
    named script does not accept.  Ambiguous cells are not counted."""
    scripts = sorted(set(re.findall(r"(?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py", cell)))
    flags = sorted(set(FLAG.findall(cell)))
    if len(scripts) != 1 or not flags:
        return False
    path = lane / scripts[0]
    if not path.exists():
        return False
    body = path.read_text(errors="replace")
    return all(f not in body for f in flags)
```

Applied to cell 5 of `SKILL.md:590`:

- `scripts` = **`{plans/round40_c1_verify.py}`** — exactly one, because cell 5's only `.py` path is
  the *falsifier* script; the **instrument's own path `plans/order_check.py` is absent from the cell**.
- `flags` (`FLAG = (--[a-z][a-z0-9-]*)`) = **`{--claims, --receipt, --selftest}`** — `--selftest`
  from the negation "no `--selftest` in the script", `--receipt`/`--claims` from the two control
  invocations. **All three belong to `plans/order_check.py`, not to `plans/round40_c1_verify.py`.**
- `plans/round40_c1_verify.py` declares `--lane, --battery-dir, --only, --work, --jobs,
  --build-module, --dest, --pristine` (`plans/round40_c1_verify.py:443-450`) and contains **no**
  `--claims`, `--receipt` or `--selftest` (`grep -n -- "--claims\|--receipt\|--selftest"
  plans/round40_c1_verify.py` → no match) ⇒ `all(f not in body …)` is **True** ⇒ the row is counted
  SELFTEST-UNBACKED.

So the counter attributes the instrument's flags to the wrong script. **It is a mis-attribution
false positive, not a false row.**

Two further facts the L1 should record:

1. **The claims prose and the frozen code disagree.** `plans/round-52-claims.md` §C2 says a row is
   selftest-unbacked when its cell "names exactly one script and one `--flag` that the named script
   does not accept (ambiguous cells are not counted, **and a cell that says the instrument has no
   self-test is accepted**)". The frozen counter implements the *ambiguous* exemption but **not** the
   "says the instrument has no self-test" exemption — it has no negation test at all. The
   `order-check` cell **does** say the instrument has no self-test, so by the claims' own prose it
   should already be accepted. (The counter is frozen; I did not change it. The workaround below
   satisfies the *code* without needing the missing exemption.)
2. **The counter's blind spot (measured):** of the 46 registry rows, only **17** name exactly one
   `.py` path in the self-test cell (i.e. are visible to this leg); **28 name no script at all**
   (so the leg cannot see them) and **1** (`config-projection`, `SKILL.md:572`) names two (ambiguous).
   After the fix this leg reads 0 for those 29 rows whether or not their claims are true — a coverage
   caveat for the round's own report (see §8).

## 6. FACT E — the frozen counter's before-state, reproduced

```
$ python3 plans/round52_c2_registry.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin
ADVERTISED total=72
REGISTERED total=44 rows=46
MISSING 28
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 1
  SELFTEST-UNBACKED `order-check`
PREDICATE R52-C2 fail        (exit 1)
```

Matches the claims file's frozen before-numbers exactly (MISSING 28, SELFTEST-UNBACKED 1
(`order-check`), exit 1).

## 7. The recommended truthful replacement cell

### 7.1 The recommended cell-5 text (self-test column of the `order-check` row)

```
no `--selftest` in the instrument: `plans/order_check.py` declares exactly three flags, `--lane`, `--claims`, `--receipt` (all required, `plans/order_check.py:143-145`); the falsifiers are external — the round-40 order mutants `O04` (`rc-silence`), `O12` (`rc-error`), `O14` (`error`), witnessed in `.ufo/waves/round-40/claims/witness/` — and the instrument's own measured controls: `python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt` → `ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0`, exit 1; `python3 plans/order_check.py --lane . --claims plans/round-99-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt` → `ORDER ERROR claims not committed in HEAD`, exit 2
```

### 7.2 Recommended companion edit — cell 6 (pinned values column)

Append to the existing cell-6 text (this column is not read by the `SELFTEST-UNBACKED` leg, so the
falsifier-script pointer can live here without mis-attribution):

```
; the round-40 order mutants `O04` (`rc-silence`), `O12` (`rc-error`), `O14` (`error`) that falsify this instrument are defined in `plans/round40_c1_verify.py` and were witnessed in `.ufo/waves/round-40/claims/witness/`
```

### 7.3 Why this text is truthful *and* clears the leg

- It **keeps the negation** ("no `--selftest` in the instrument") — the truth, unchanged.
- It **names the instrument's own path** `plans/order_check.py`, so the counter's single-script rule
  now attributes the flags to the script they belong to. `scripts = {plans/order_check.py}` (one),
  `flags = {--claims, --lane, --receipt, --selftest}`; `--claims`, `--lane` and `--receipt` all
  occur in `plans/order_check.py`'s bytes ⇒ `all(f not in body …)` is **False** ⇒ not counted.
  Because the cell also names a real flag, the cell stays **machine-checked** rather than merely
  ambiguous.
- It keeps every falsifier the cell had, verbatim in substance, and pins the two controls as
  *commands* (`python3 plans/order_check.py …`) so a reader can run them.
- It adds nothing that is not measured in §4.

### 7.4 Measured effect on a scratch copy (the lane tree was not touched)

Copy of the counter-relevant lane files into
`/fast/scratch/hyaku/kengaku-r52/C2ExecOrderCheckFact/tree/` (SKILL.md, SCORECARD.md, LOG.md,
`grader.py`, `plans/*.py`, `corpus/README.md`, `corpus/knowledge/`, `corpus/evidence/*/*.py`; 4.8 MB),
the row patched there, and the **frozen counter re-run against that copy**:

```
before patch (scratch copy):  ADVERTISED 72 · REGISTERED 44/rows 46 · MISSING 28 · INCOMPLETE 0 · ENTRY-MISSING 0 · SELFTEST-UNBACKED 1 (`order-check`) · PREDICATE R52-C2 fail (exit 1)
after  patch (scratch copy):  ADVERTISED 72 · REGISTERED 44/rows 46 · MISSING 28 · INCOMPLETE 0 · ENTRY-MISSING 0 · SELFTEST-UNBACKED 0 · PREDICATE R52-C2 fail (exit 1)
```

`MISSING 28` is untouched — the 28 missing rows are other seats' scope. Two candidate wordings were
both measured: one **without** the literal `--selftest` token and one **with** it (§7.1 ships the
"with" wording, since it is more explicit). Both give `SELFTEST-UNBACKED 0`; `INCOMPLETE 0` and
`rows 46` are preserved in both, i.e. the eight-cell parse is unaffected.

### 7.5 Alternative if the L1 prefers to keep cell 5 as one blob

Adding the falsifier script's path to cell 5 as well makes `scripts` = 2 ⇒ the cell becomes
"ambiguous" ⇒ not counted ⇒ the leg reads 0 as well. **Not recommended**: it clears the leg by
falling outside the counter's net instead of by being checkable, and it leaves the row's flags
attributed to nobody.

## 8. FACT F — audit of every other registry row (no second false claim found)

All 46 rows were parsed with the counter's own parser and checked against the scripts' bytes.

**Rows the counter does check (17 rows, exactly one script named):**

| row | SKILL.md line | cell flags | verdict |
|---|---|---|---|
| `hermetic-grader` | 564 | `--selftest` | `grader.py` declares `--selftest` ✓ |
| `interval-reverdict` | 566 | `--selftest` | `plans/attrib_calibration.py` declares it ✓ |
| `state-assertion-check` | 567 | `--selftest` | `plans/state_check.py` declares it ✓ |
| `grader-perturb` | 568 | `--selftest` | `plans/grader_perturb.py` declares it ✓ |
| `gate-timing` | 569 | `--commit`, `--lesson`, `--selftest` | `plans/gate_timing_check.py` declares all three ✓ |
| `benchmark-spec-audit` | 570 | `--selftest` | `plans/benchmark_spec_audit.py` declares it ✓ |
| `registry-reference-check` | 571 | `--selftest` | `plans/registry_check.py` declares it ✓ |
| `sources-adopt` | 573 | `--selftest` | `plans/sources_adopt.py` declares it ✓ |
| `package-gate` | 574 | `--lane` | `plans/round36_c1_verify.py` declares `--lane` ✓ |
| `regex-log-probe` | 576 | `--lane` | `plans/round36_c2_verify.py` ✓ |
| `git-webserver-probe` | 577 | `--dry`, `--lane`, `--rerun` | `--dry` belongs to `plans/git_webserver_probe.py` (declares it ✓), `--rerun` to the package gate `plans/pkg_gate.py:365` (`pp.add_argument("--rerun", …)` ✓), `--lane` to `plans/round37_c2_verify.py` ✓ — **truthful, but flags cross scripts** |
| `git-leak-probe` | 587 | `--dry`, `--lane` | `--dry` belongs to `plans/git_leak_probe.py` (declares it ✓) — truthful, flags cross scripts |
| **`order-check`** | **590** | `--claims`, `--receipt`, `--selftest` | **the only counter failure; mis-attribution, row is truthful (§4)** |
| `db-wal-probe` | 594 | `--dry`, `--lane`, `--stage-check` | `--dry`/`--stage-check` belong to `plans/db_wal_probe.py` (declares both ✓); `--lane` to `plans/round40_c2_verify.py` ✓ — **truthful**; see the near-miss note below |
| `constraints-probe` | 597 | `--dry` | belongs to `plans/constraints_probe.py` (declares it ✓) — truthful, flags cross scripts |
| `scratch-root-guard` | 608 | `--selftest` | `plans/scratch_guard.py` declares it ✓ |

**Rows the counter cannot check (28 name no `.py` path; `config-projection` names two) — checked by
hand against their own entry script's `add_argument` list:**

```
`config-projection`    572  plans/config_projection.py            --selftest:declared
`round36-c1-battery`   575  plans/round36_c1_verify.py            --legacy:declared
`round37-c1-mutants`   578  plans/round37_c2_verify.py            --battery:declared
`round37-c2`           579  plans/round37_c2_verify.py            (no flags in cell)
`anchor-digest-check`  580  plans/anchor_digest_check.py          --selftest: NEGATED — and indeed the script declares only --lane/--evidence-ref/--verbose
`ledger-tip`           581  plans/ledger_tip.py                    (no flags in cell)
`build-pmars-probe`    582  plans/build_pmars_probe.py            (no flags in cell)
`round38-c1-mutants`   583  plans/round38_c1_verify.py            (no flags in cell)
`round38-c2`           584  plans/round38_c2_verify.py            (no flags in cell)
`mutant-direction-check` 585 plans/mutant_direction_check.py      (no flags in cell)
`tip-receipts`         586  plans/tip_receipts.py                 (no flags in cell)
`round39-c1-mutants`   588  plans/round39_c1_verify.py            (no flags in cell)
`round39-c2`           589  plans/round39_c2_verify.py            (no flags in cell)
`round39-c1-audit`     591  plans/round39_c1_audit.py             --battery/--only:declared; --selftest: NEGATED — and indeed round39_c1_audit.py declares no --selftest
`round40-c1-mutants`   592  plans/round40_c1_verify.py            --only:declared
`round40-c2`           593  plans/round40_c2_verify.py            (no flags in cell)
`round41-c2`           596  plans/round41_c2_verify.py            (no flags in cell)
`round-close-check`    598  plans/round_close.py                  --selftest:declared
`round42-c1-mutants`   599  plans/round42_c1_verify.py            (no flags in cell)
`round42-c2`           600  plans/round42_c2_verify.py            (no flags in cell)
`fibsqrt-probe`        601  plans/fibsqrt_probe.py                --dry/--stage-check:declared
`round43-c1-mutants`   602  plans/round43_c1_verify.py            (no flags in cell)
`round43-c2`           603  plans/round43_c2_verify.py            (no flags in cell)
`feal-probe`           604  plans/feal_probe.py                   (no flags in cell)
`round44-c1-mutants`   605  plans/round44_c1_verify.py            (no flags in cell)
`round44-c2`           606  plans/round44_c2_verify.py            (no flags in cell)
`feal-linear-probe`    607  plans/feal_linear_probe.py            --stage-check:declared
```

**Result of FACT F: no second row's self-test claim can be disproved from the script bytes.**
Two rows carry *negated* claims ("this script has no `--selftest`") and both are true
(`plans/anchor_digest_check.py`, `plans/round39_c1_audit.py` declare no `--selftest`); every
affirmative flag mention resolves to a script that declares it.

**Near-miss latent false positive (the one thing to watch):** `db-wal-probe` (`SKILL.md:594`) names
`plans/round40_c2_verify.py` as its single `.py` path while the cell mentions `--stage-check`, which
that script does **not** declare (`plans/round40_c2_verify.py` declares only `--lane`, `--work`;
`--stage-check` is `plans/db_wal_probe.py`'s flag). The counter does not fire only because `--lane`
and `--dry` occur in `round40_c2_verify.py`'s body (as a subprocess argument), so `all(…)` is False.
The row is truthful as written. **If the L1 rewrites that cell (e.g. trimming the `--lane`
mention), the same mis-attribution would fire.** The same trap exists for `git-leak-probe` (587),
`constraints-probe` (597) and `git-webserver-probe` (577), whose cells mention probe-side flags
while naming a counter-side script.

## 9. Risks / blockers / notes for the L1

1. **The lane tree was not edited by this seat.** The §7 replacement is a *recommendation*; the L1
   owns the integration and the commit. Applying it changes only `SKILL.md:590` (cells 5 and 6).
2. **Frozen-code vs claims-prose mismatch** (§5.1): the claims file says a cell declaring "no
   self-test" is accepted; the frozen counter implements no such exemption. The §7 wording clears
   the leg under the *code*, so the round does not depend on the missing exemption. Worth naming in
   the round's lesson as the open `vacuous`-class shape (D3/D4 territory) — **not** a change to the
   frozen counter.
3. **Coverage caveat on the fixed leg** (§5.2): the `SELFTEST-UNBACKED` leg can only see the 17
   rows that name exactly one script path; 29 rows are outside its net. The after-run's
   `SELFTEST-UNBACKED 0` therefore means "no counted row claims an unbacked flag", not "every row's
   self-test claim was verified". The round report should say so.
4. **Amendment A1 does not touch C2** (§1): the C2 rules and counter are as frozen.
5. **Sibling overlap:** other wave-1 seats are drafting the 28 missing rows; my recommended cell is
   for the *existing* `order-check` row and does not collide with their work. The L1 should land the
   §7 edit together with the 28 new rows so the after-run is measured once.
6. No tools were installed or upgraded by this seat (no pacman, no uv tool, no npm) — nothing was
   needed beyond stock `python3`, `grep`, `git` (read-only) and `sed`/`awk` for quoting.

## 10. Exact commands run (all read-only against the lane; no mutating git/jj, no commits)

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
git rev-parse HEAD ; git log --oneline -3 ; git diff --stat 30801b479e3418c11089b8586178b6960216f364 HEAD -- SKILL.md plans/order_check.py plans/round52_c2_registry.py
git diff --stat 1315234 07ea208 ; git diff 1315234 07ea208 -- plans/round-52-claims.md
wc -l plans/order_check.py plans/round52_c2_registry.py SKILL.md
grep -n "add_argument\|ArgumentParser\|parse_args\|def main\|sys.exit" plans/order_check.py
grep -n "selftest\|self-test\|self_test" plans/order_check.py            # no match
grep -n -- "--claims\|--receipt\|--selftest" plans/round40_c1_verify.py # no match
grep -n "add_argument" plans/round40_c1_verify.py
grep -n "O04\|O12\|O14\|rc-silence\|rc-error" plans/round40_c1_verify.py
ls .ufo/waves/round-40/claims/witness/
python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt ; echo "exit=$?"
python3 plans/order_check.py --lane . --claims plans/round-99-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt ; echo "exit=$?"
python3 plans/round52_c2_registry.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin
# scratch-only (own scratch dir), never the lane tree:
python3 analyze.py            # per-row script/flag extraction with the counter's own regexes
python3 strict_check.py <lane> # flags not declared by the named script, with negation detection
python3 uncounted_rows.py <lane>
python3 patch_test.py          # patches the scratch copy's SKILL.md, re-runs the frozen counter
```

## 11. Files produced

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ExecOrderCheckFact/report.md`
  (this file — the wave-report path named in the seat's write scope)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ExecOrderCheckFact.md`
  (identical copy, at the path named in the seat item)
- Scratch (removed before yielding, per the scratch directive):
  `/fast/scratch/hyaku/kengaku-r52/C2ExecOrderCheckFact/{analyze.py, strict_check.py, uncounted_rows.py, patch_test.py, tree/}`.
  The scratch copy of the lane files existed only to measure the counter against a patched row; the
  lane tree itself was never written to.
