# R38CritC1Counter — attack on `plans/round38_c1_verify.py`

Seat: critic, kengaku round 38 wave 1. Target: the frozen C1 counter, not the task owner.
Lane clone: `/fast/scratch/hyaku/kengaku-r38/R38CritC1Counter/lane` at `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e`;
`PINS total=14 mismatched=0` at that tip (`receipts/h1.out`), so the frozen inputs under test are the ones the
claims name. Scratch deleted at the end; modules and outputs copied to this seat's dir first.

**Result: `PREDICATE C1 pass` is reachable twice without demonstrating one advertised behaviour (H1, H2), 21 of 22
kills are forgeable with no counter patch and no injected module (H3), and the 22nd is *unreachable in its frozen
direction by any fixture at all* (H-N21).** So a green C1 line is not evidence that the gate's advertised
behaviours are demonstrated; worse, the frozen predicate is unsatisfiable honestly, so the honest executor will
report a stop and only a fabricating battery can print green.

## Ranked holes (cheapest attack first)

| # | Hole | Attack cost | Counter line it defeats | Measured |
|---|---|---|---|---|
| H-N21 | N21's frozen `direction` is wrong: the mutation is monotone-decreasing, so its reachable kill is a *mirror*, never `silence` | 0 (read the mutant) | `MUTANTS` row N21, `plans/round38_c1_verify.py:140` | 24/24 d5 states give `silence_attributable False` |
| H1 | battery38 modules are imported *into the counter's own process* | 17 lines, 1 fixture | `mod = load(f, ...)` `:172` | `PREDICATE C1 pass`, exit 0 |
| H2 | a fixture-owned `--spec` names `probe_cmd`, which the reference gate executes; a shadow stdlib module planted in the counter's gate dir fabricates every mutant run | 96 lines, 3 fixtures | `:245` spec allowance + gate `c_rerun` exec | `PREDICATE C1 pass`, exit 0; 19/22 credits land on frozen fixtures that kill 0/22 |
| H3 | `build` runs once; ref, renamed, null and every mutant grade the *same mutable directory*, and a `--rerun` probe counts its own invocations | 119 lines, 7 fixtures | `:237-320` (one build, one dir) | `killed=21 survived=1`, `wrong=0`, `renamed=0`, `null_detected=0` |
| H4 | only `--spec` is confined to `d`; `--root`/`--file`/`--capture-dir` are free, so a fixture that never touches `d` is accepted and `renamed_disagree=0` is vacuous | 30 lines, 1 fixture | `:245` vs no check on other paths; `:276` | accept; 4 probe runs, one cwd |
| H5 | `null_gate` is a byte-for-byte copy of the reference gate, so `null_detected` can only see drift between the ref run and the null run — never a forgery keyed on the mutant filename or the invocation index | 0 | `:281-284` | `null_detected=0` while healing at n≥3 (`receipts/h5.out`) |

### H-N21 — the frozen list pins an unreachable direction (root cause)

`N21` claims "the capture digest is looked up in every manifest row, not only the first" in direction `silence`
(`plans/round38_c1_verify.py:140`), but the mutation only *shortens* the scan:

```
-    for parts in (row.split() for row in sums.splitlines()))
+    for parts in (row.split() for row in sums.splitlines()[:1]))
```

`pinned = any(...)` over a prefix of the rows is monotone: truncation can turn `pinned` True→False, never
False→True. `pinned` is the only term the mutation touches, and `not pinned` is the only manifest defect
(`plans/pkg_gate.py:349-352`), so the mutant's D5 defect set is a superset of the reference's on every possible
input. `silence` requires the reverse (`:202-203`: reference DEFECT, mutant not).

Evidence — all 24 reachable d5 states (7 manifest shapes × 3 line shapes, `modules/n21_d5_space.py`), reference vs
N21 mutant run side by side (`receipts/n21_direction_table.txt`):

```
n21s-digest-on-line2-ok                0      ok     1      DEFECT False
n21s-blank-lines-ok                    0      ok     1      DEFECT False
n21s-digest-on-line1-ok                0      ok     0      ok     False
...
silence_attributable False  (24/24)
```

The only direction it *can* be killed is mirror. A clean accept-side fixture (`modules/n21_mirror_accept_side.py`,
manifests `decoy row 1 / genuine row 2`) is scored as nothing (`receipts/n21_mirror_accept_side.txt`):

```
FIXTURE n21-accept-side expect=accept declared=- observed_rc=0 observed_defects=- ok
MUTANT N21 D5 silence SURVIVED -- the capture digest is looked up in every manifest row, not only the first
== direct gate stdout on the same fixture ==
ref  rc=0 defects=- ok=['D5']
N21  rc=1 defects=['D5'] ok=-
== counter reading of that fixture, both directions ==
silence = False | mirror = True
```

`attributed` also refuses the mirror reading because the direction is frozen. And `d5-line` has no
execution/state hook, so unlike every package-family clause N21 cannot even be faked by tree state: only H1/H2
(poison the interpreter) reach it. Seat `R38BatD5` reaches the same conclusion independently — its manifest-shape
matrix gives `superset=True` for all eight shapes and `d5m-n21-manifest-row-2 vs N21: silence=False mirror=True`
(`.ufo/waves/round-38/build/R38BatD5/receipt-probe.txt`), and its verdict already reports the honest stop at
21/22. Consequence: `MUTANTS total=22 killed=22` is not attainable by honest
fixtures; the frozen kill rule's "any survivor … → C1 not admitted, reported as an honest stop"
(`plans/round-38-claims.md` §C1) will fire at landing, and the only green line is a lie. Distinguish these: N21 is
not a "mutant later shown equivalent" (the claims' named limit) — it is killable, in the opposite direction to the
one the counter demands.

### H1 — battery modules run inside the counter process

`battery38_fixtures` executes module source in the counter itself (`plans/round38_c1_verify.py:172`:
`mod = load(f, f"kengaku_b38_{f.stem}")`), after `PINS` was printed and before any fixture is built. A module's
top level therefore owns `sys.modules["__main__"]`. `modules/h1_inproc.py` is 17 lines:

```python
_c = sys.modules["__main__"]
_c.attributed = lambda clause, direction, fx, argv, ref, mut: True
```

plus one empty-directory reject fixture. The channel itself was found independently in this wave by
`R38CritClaims` §Junk/D8 (`.ufo/waves/round-38/build/R38CritClaims.md`, 20/22 with a wrapper that filters mutant
output); this seat's delta is the smallest module that reaches the *full* predicate (`killed=22`) and the credit
ledger below. Full predicate, on `plans/battery38` in the clone
(`receipts/h1.out`, exit 0):

```
PINS total=14 mismatched=0
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=22 killed=22 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```

Every credit is bogus, and all 22 are *attributed to the frozen round-36 fixtures* (`killed by=r36-*` ×22) —
fixtures the do-nothing control proves kill 0/22 (`.ufo/waves/round-38/claims/control-c1-nothing.txt`). The
sidechannel scan is irrelevant here: no banned token is used. Any Python plugin loader has this property; the
counter's job is to not be the thing the plugin can rewrite.

### H2 — the fixture-owned `--spec` is an execution vector

The counter confines `--spec` to the fixture dir (`:245`) and the claims name that as the limit: "the counter only
checks that the spec path is inside the fixture dir" (`plans/round-38-claims.md` §C1). That check is not a safety
bound, because the spec is executable configuration: `c_rerun` runs `p["probe_cmd"]` (`plans/pkg_gate.py:267-278`),

```
r = subprocess.run(cmd, cwd=str(p.root), capture_output=True, text=True, timeout=600)
```

so a fixture chooses a command the *reference* gate runs, from inside the fixture tree, **after** the counter has
created its gate directory (refs run after `gdir.mkdir()` + `ref_gate.write_text`, `:250-253`). The execution vector
itself is independently reported by `R38SentinelProbe` F1 (`.ufo/waves/round-38/build/R38SentinelProbe.md` §1/F1) as
a secrets/network finding; this seat's delta is that the same door forges the C1 verdicts and reaches
`PREDICATE C1 pass`. The probe writes a
shadow `hashlib.py` into that directory; every later gate run — mutant gates are `python3 <gdir>/N01.py`, whose
`sys.path[0]` is `gdir` — imports the shadow, which keys on `os.path.basename(sys.argv[0])`
(`modules/h2_shadow_full.py`):

```python
if _name.startswith("N") and _name.endswith(".py"):
    if _name[:-3] in _mirror:
        print(_mirror[_name[:-3]] + " DEFECT fabricated-by-shadow-module")
    os._exit(1)
```

For every other gate name it re-exports the real module, so `ref.py`, `null.py` and the renamed runs stay
byte-honest. `receipts/h2min.out` — minimal battery, **3 fixtures, 96 lines**, real predicate, exit 0:

```
FIXTURE h2-plant expect=reject declared=P1,P3,P4,P5,P6,P7,P8 observed_rc=1 observed_defects=P1,P3,P4,P5,P6,P7,P8 ok
FIXTURE h2-main17 expect=error declared=- observed_rc=2 observed_defects=- ok
FIXTURE h2-main18 expect=error declared=- observed_rc=2 observed_defects=- ok
BATTERY fixtures=67 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=22 killed=22 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```

**The `killed by=` field becomes false evidence.** Credits from that run: `r36-*` ×10, `p23-p3-heading-renamed`
×4, `p910-receipt-deleted` ×2, `p7-m28-entry-deleted` ×2, `h2-main17` ×2, `p4-capture-unreadable` ×1, `h2-plant`
×1 — i.e. 19/22 credits point at pinned frozen fixtures whose measured kill count is 0/22. Two credits are
individually disprovable: N18 is credited to `h2-main17` although the N18 mutant exits 2 on that fixture (only the
shadow made it 1 — `receipts/n18_credit_check.txt`: `ref 2`, `N18 2`), and N04 is credited to
`p4-capture-unreadable` which the control shows surviving. The seven-fixture
variant (`receipts/h2.out`) shows the same pass with each clause family separately fabricated.

### H3 — one fixture directory, many graded runs

`build` is called exactly once per fixture (`:237-249`) and that directory is then graded by the reference, by the
renamed copy's re-run, by the null copy, and by every mutant. Nothing re-materialises the tree. A fixture whose
`--rerun` probe counts its own invocations (counter outside `d`, so the renamed copy does not fork it) can change
the tree between the null run and the mutant loop, one line apart from a version the sentinels can see. Order is
measured, not assumed (`receipts/h4log.txt`, one accept fixture, four runs): `ref n=1`, `renamed n=2`,
`null n=3`, `mutant n=4`, all in the same directory.

`modules/h3_state_heal.py`, seven fixtures, no patching and no injected module: `h3-heal` starts as a tree whose
every clause is DEFECT and, at n≥3, copies the genuine package in (heal log: `heal n=1 at f064`,
`heal n=2 at x55433q`, `heal n=3 at f064`, … 21 lines = 1 ref + 1 renamed + 1 null + 18 package mutants);
`h3-break` starts as a genuine accept and, at n≥3, truncates the quote table, appends a blank manifest line and
tampers the receipt. `receipts/h3.out`:

```
BATTERY fixtures=71 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N01 P1 silence killed by=h3-heal ...
MUTANT N02 P3 mirror killed by=h3-break ...
MUTANT N03 P4 silence killed by=h3-heal ...
...
MUTANT N22 D5 silence killed by=h3-d5-prefix ...
MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0
```

16 of those kills are `h3-heal` (13) / `h3-break` (3), i.e. the mutant never ran on the tree the reference graded: N03's
"every quote is checked, not only the first" is credited by a fixture whose reference had *no parseable quote at
all* (the heal gave the mutant run eight). The remaining honest fixtures (N17, N18, N19, N20, N22) are ordinary
work. Only N21 survives — see H-N21.

### H4 — path confinement stops at `--spec`; `renamed_disagree=0` can be vacuous

`:245` constrains only the `--spec` argument. `--root`, `--file`, `--capture-dir` are unchecked, and `:276`
(`nargv = [t.replace(str(d), str(nd)) for t in argv]`) only substitutes `str(d)`. So a fixture that never mentions
`d` is graded identically by the "renamed" re-run: the check reports 0 while testing nothing. `modules/h4_root_beside_d.py`
builds a genuine package at `<root>/h4-pkg`, returns `--root <root>/h4-pkg`, and its probe logs cwd per invocation
(`receipts/h4.out`, `receipts/h4log.txt`):

```
FIXTURE h4-root-beside-d expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N15 P10 mirror killed by=h4-root-beside-d -- ...

c1-pj4bse5p/h4-pkg 1
c1-pj4bse5p/h4-pkg 2
c1-pj4bse5p/h4-pkg 3
c1-pj4bse5p/h4-pkg 4
```

Four runs, one directory: invocation 2 is the "renamed" run and it graded the very tree the reference graded. Note
also what this buys a *hostile* fixture: the same freedom lets a battery point the gate at the lane itself (or any
writable tree), and `--spec` can name absolute `entry`/`readme`/`capture_dir`/`frozen_instruments` paths, so a
fixture's "package" need not exist inside `d` at all.

### H5 — the null is the reference

`null_gate.write_text(gate_src)` (`:281-282`) writes the *unmutated* gate source to `null.py`, so
`run_gate(null_gate, ...) != ref[j]` (`:284`) can only fire when the environment or the fixture tree changed
between the reference run and the null run. It cannot see a gate that lies for `N*.py`, nor a heal that lands
after the null run's own clause evaluation. Measured: `h5-before-print` heals at n≥3 *before* its probe prints —
`null_detected=0`, N03 credited (`receipts/h5.out`) — because every clause is evaluated before P10 runs, so even
the coarser placement is invisible. Combined with the renamed run grading a throwaway copy (H3's log: n=2 at
`x55433q`), the two sentinels bracket exactly n≤3 and the attacker needs n≥3 at a `d`-cwd invocation. The pass
line's `null_detected=0` therefore means "nothing drifted", not "nothing lied".

## Impacted axes

- **calibration (the C1 claim's own axis)** — damaged at the root: the frozen mutant table mis-declares one
  direction, so `killed=22` cannot be earned; and the counter's own controls cannot distinguish demonstrable
  kills from fabricated ones. C1 as frozen cannot be admitted on evidence.
- **depth** — the kill rule was hardened in round 37 against "any result differs"; the surviving gaps are
  lifecycle (shared tree, one build) and privilege (in-process import, fixture-chosen command), not the rule text.
- **operability** — the landing runbook ("`PREDICATE C1 pass` on a clean clone") would go green on a lying
  battery; the only gate left is the claims' non-author code review, which is exactly what this report supplies.
- **coverage / novelty / freshness / adjacency** — untouched by this seat.

## Smallest safe correction (in order)

1. **N21 (blocks everything).** Either flip the frozen direction to `mirror` (the truncation only ever adds a
   defect) or drop N21 and re-freeze `TOTAL=21`; a frozen-artifact change, so the L1 decides. Add a pre-freeze
   feasibility probe: for each mutant, build one candidate fixture per direction and assert the declared direction
   is reachable before the list is frozen. Until then the honest wave-1 result is 21/22 and C1 is an honest stop.
2. **H1 (one binding).** Capture `_attributed = attributed`, `_mutants = MUTANTS`, `_run_gate = run_gate` before
   loading any battery and call the captured names in the mutant loop; after loading, assert identity. Robust form:
   import battery modules in a subprocess and pass fixtures back as data (build callables cannot survive that, so
   the cheap form is: load each module in a fresh subprocess whose only output is the fixture list, with builders
   named, not inherited).
3. **H2 (one flag + one field check).** Run every gate with `python3 -P` so the gate directory is not on
   `sys.path`, and require a fixture-owned spec's `probe_cmd` to be byte-equal to the frozen one, or refuse P10 for
   fixture-owned specs. Independently worth flagging upstream: `c_rerun` executes `probe_cmd` from the spec with
   `cwd=root` and the caller's privileges — a spec is executable configuration in the gate, not data.
4. **H3 (one copytree).** Re-materialise per graded run: call `build` into a fresh directory for the null run and
   for each mutant run (or copy `d`). Fixtures are small; the 65-fixture × 23-run matrix already dominates cost.
   This also makes `killed by=` a real witness, which is what H2 abuses.
5. **H4 (extend :245).** Constrain *every* path-valued argv element (`--root`, `--file`, `--capture-dir`) to `d`
   and require at least one argv token to contain `str(d)`, so the renamed re-run substitutes a real path.
6. **H5 (rename + real null).** With (4) in place, run the null on a re-materialised tree; then the check means
   determinism, which is what it measures. Rename the counter's `null` to `repeat` until a behaviour-preserving
   mutant exists.

## Checked and found sound (no hole)

- `--spec` symlink escape: `pathlib.Path(...).resolve().is_relative_to(d.resolve())` (`:245`) follows links, so a
  symlink out of `d` is refused.
- `defects: None` is refused for battery38 (`:261`), so a reject fixture must pin its clause set (it is still
  accepted for the frozen r36 fixtures, which declares nothing — not exploitable from `plans/battery38`).
- Subcommand family gating (`:192-194`) is correct; `MAIN` is deliberately family-free.
- Mutant digest re-check after the run (`:302`, `:312`) catches a mutant file rewritten mid-run.
- `PINS` covers every frozen input this seat relied on: 14/14 matched at the tip used here.

## Cross-seat corroboration (what is new here, what is not)

| Finding | Independently found in this wave | Delta in this seat |
|---|---|---|
| in-process battery import (H1) | `R38CritClaims` §Junk/D8, 20/22 | smallest module reaching the *full* predicate, and the fully-false credit ledger |
| `probe_cmd` execution (H2) | `R38SentinelProbe` F1 (secrets/network) | the same door forges mutant verdicts → `PREDICATE C1 pass`; false witness credits |
| N21 direction is wrong (H-N21) | `R38BatD5` §Limits + `receipt-probe.txt` | exhaustive 24-state table with `attributed` called directly; statement that the predicate is unsatisfiable, not just unearned |
| shared mutable fixture dir (H3) | not reported by any seat I read | first forgery that needs no patch and no injected module |
| path confinement stops at `--spec` (H4) | `R38SentinelProbe` finding 4 tests only the `--spec` rule | the other three path arguments and the vacuous renamed check |
| null is the reference (H5) | not reported | measured invisibility of a heal at n≥3 |

## Limits of this review

Host python 3.14.8 with `Bio` absent, so every P10 probe ran through
`uv run --no-project --with biopython==1.85 python3` (cached, 0.013s) — the exec path is the same, one interpreter
further out. A gate-hardening claim about `ldd`/glibc is not involved here. H3's invocation counting is
order-sensitive by construction: it depends on the measured order (ref → renamed → null → mutants), which I
recorded rather than assumed. I did not test the C2 counter or any lane file; nothing in the lane, `plans/` or
`corpus/` was written (all writes in the clone and this seat's dir).

VERDICT: c1-counter-holes-6
