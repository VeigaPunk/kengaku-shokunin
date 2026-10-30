# R11R52Carry — carried r52 repair reconstruction recipe (round 55)

Reconstructed evidence for the **refused** E3 round-52 C2 registry repair
(`.ufo/waves/round-54/w1/E3R52RegistryFix/`, refused by
`.ufo/waves/round-54/w1/R4R52Fix.md` DO-NOT-INTEGRATE). Both carried defects are
reproduced here on scratch copies only; the production counter
`plans/round52_c2_registry.py` is **unchanged** (round-55 claims: "production
counters stay untouched"; this seat writes no lane file).

- Measured tree: clean shared clone of the lane at freeze commit
  `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (round-55 claims freeze; parent
  `798f5e9ef30ef39291295565209b65a17343c00e` is the declared base tip).
- Old counter = `plans/round52_c2_registry.py` (production, sha256
  `9e6f41a457ec2d847f81d513d30545d982e0a118b4cfa8452af34e1d1a509e6b`).
- Patched counter = `.ufo/waves/round-54/w1/E3R52RegistryFix/round52_c2_registry.py`
  (sha256 `83667e8f23e75146584bca0ac94aeffb122e554571528c1c027e3c462754dc6d`).
- Mutant = patched with one in-memory replacement (the controls.json K7 mutation):
  `ok = not (missing or incomplete or entry_missing or unbacked or duplicate)` →
  `ok = not (missing or incomplete or unbacked or duplicate)`.
- All receipts referenced below are committed next to this recipe under `receipts/`.

## Defect 1 — the order-check regression (R4 P1)

**Check the patch touched:** `selftest_unbacked(cell, lane)` — the
SELFTEST-UNBACKED leg of the counter (`plans/round52_c2_registry.py:68-83`
production numbering). It decides whether a registry row's self-test cell
(column 5) advertises a flag the named script does not accept.

**Patch shape (E3 `delta.diff`):** the old code returned `False` for the *whole
cell* whenever any `no … --flag` phrase appeared (`re.search(r"\bno\b.{0,24}--[a-z][a-z0-9-]*")`).
The patch removes the blanket exemption and instead subtracts only the locally
negated flag: `negated = set(re.findall(r"\bno\b.{0,24}?(--[a-z][a-z0-9-]*)", cell, re.IGNORECASE))`,
`flags = sorted(set(FLAG.findall(cell)) - negated)`, then keeps the old rule
"one script in cell + all surviving flags absent from that script's body →
unbacked".

**The input that flips:** the committed `order-check` registry row,
`SKILL.md:590`, column 5 (verbatim):

```
no `--selftest` in the script; falsifiers are external — `plans/round40_c1_verify.py` mutants `O04` (`rc-silence`), `O12` (`rc-error`), `O14` (`error`), each witnessed pre-freeze (`.ufo/waves/round-40/claims/witness/`), and the measured controls `--receipt corpus/evidence/round39/git-leak-probe.txt` → `ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0`, exit 1; `--claims plans/round-99-claims.md` → `ORDER ERROR claims not committed in HEAD`, exit 2
```

Mechanism: the cell negates exactly one flag (`--selftest`) and its surviving
flags `--receipt`/`--claims` are controls of `plans/order_check.py` (which
accepts both: `plans/order_check.py:143-145` — `--lane`, `--claims`, `--receipt`
all `required=True`). But the cell's **sole `.py`-suffixed script mention** is
the external falsifier `plans/round40_c1_verify.py` (order_check.py is never
named with `.py` in this cell), and round40_c1_verify.py declares different
options (`:443-450`: `--lane --battery-dir --only --work --jobs --build-module
--dest --pristine`; no `--receipt`/`--claims`). So:

- Old: the blanket `no … --flag` match exempts the whole cell → no finding →
  row green.
- Patched: strips only `--selftest`; `scripts == [plans/round40_c1_verify.py]`,
  `flags == [--claims, --receipt]`; both absent from that body →
  `SELFTEST-UNBACKED \`order-check\`` → row red. The patch attributes the flags
  to the wrong script. (Verified at source level: `grep add_argument
  plans/round40_c1_verify.py` shows no `--receipt`/`--claims`; order_check.py
  requires both.)

**Observed flips (receipts A1–A4):**

- A1, both counters on the raw freeze clone: old exits 1 with only the r54
  surface (`MISSING 2` = `plans/round54_c1_anchor.py`, `plans/round54_c2_entrytruth.py` —
  the R55-C1 regression); patched exits 1 with the same `MISSING 2` **plus**
  `SELFTEST-UNBACKED 1 / \`order-check\``. The only output delta is the new
  finding. (`receipts/A1-old-lane.txt`, `receipts/A1-patched-lane.txt`.)
- A2, registry-closed clone (two complete flag-free rows for the round54
  counters inserted in the scratch clone's SKILL.md; fixture rows, lane file
  untouched): old → all legs 0, `PREDICATE R52-C2 pass`, exit 0
  (`receipts/A2-old-closed.txt`); patched → `SELFTEST-UNBACKED 1 / \`order-check\``,
  `PREDICATE R52-C2 fail`, exit 1 (`receipts/A2-patched-closed.txt`). Green lane
  turned red by the patch alone — the required no-harm failure.
- A3, row-level isolation over all 81 parsed rows: exactly one row's
  self-test predicate flips old→patched — `` `order-check` ``: `old=False
  patched=True` (`receipts/A3-row-isolation.txt`).
- A4, the patch's *intended* defect is real and the patch does catch it
  (R4's mixed-negation micro-fixture: one registry row
  `` `t` `` entry `python3 plans/tool_a.py`, self-test cell
  `no --selftest; python3 plans/tool_a.py --check`, `plans/tool_a.py` =
  `# no accepted flags`, advertised via SCORECARD.md): old masks the unbacked
  `--check` (pass, exit 0, `receipts/A4-old-negation.txt`); patched flags it
  (`SELFTEST-UNBACKED \`t\``, fail, exit 1, `receipts/A4-patched-negation.txt`).

So the naive strip-the-negated-flag fix repairs the narrow case and
simultaneously breaks the legitimate landed cell. Prior art already said this:
r52-w1 `C2RevCounterRule` B3 (a co-mentioned accepted flag masks an unsupported
one), and r52-w2 `W2RevRowsB` `receipts/probes/a3-fix-probe.py` — span-scoped
attribution ("flags count only inside a backtick span that begins
`python3 <script>`") reproduces all 74 row verdicts of the frozen counter AND
catches the masked claim, and its report warns verbatim that naive flag
stripping "FLAGS the landed order-check cell".

## Defect 2 — the masked K7 control (R4 P2)

**The control:** E3's added selftest case `K7-entry-missing` plus committed
fixture `fixture-k7.md` / `controls.json`. controls.json's frozen mutation is
"ok expression drops entry_missing"; the fixture's expected red state is
`ENTRY-MISSING 1; PREDICATE R52-C2 fail; exit 1` with `plans/ghost_tool.py`
absent.

**Which fixture the patch made invisible:** `fixture-k7.md` specifies *inserting*
the ghost row **into the complete registry table** ("do not create
plans/ghost_tool.py"), so ENTRY-MISSING is the only failing leg. The implemented
selftest (`delta.diff`, patched counter lines 199-206) instead **overwrites**
SKILL.md with a registry containing *only* the ghost row, while the fixture lane
still advertises `grader.py` and `plans/tool_a.py` (written at selftest start,
advertised by the fixture SCORECARD.md). Result: `MISSING 2` fires on every K7
run and independently forces `verdict(t) == 1`. The ENTRY-MISSING term can then
be removed from the verdict with no observable change — the
complete-table fixture from the seat's own controls.json/fixture-k7.md is the
one the implementation never exercised.

**Observed masking (receipts B1–B4):**

- B1, patched `--selftest` → `SELFTEST cases=6 failures=0`, exit 0; the K7 step
  visibly prints the confound: `ADVERTISED total=2 / REGISTERED total=1 rows=2 /
  MISSING 2 (grader.py, plans/tool_a.py) / ENTRY-MISSING 1 (plans/ghost_tool.py)
  / PREDICATE R52-C2 fail` (`receipts/B1-patched-selftest.txt`).
- B2, the exact controls.json mutation applied to a scratch copy
  (`counters/mutant_k7_round52_c2_registry.py`) → still
  `SELFTEST cases=6 failures=0`, exit 0, **including `SELFTEST ok
  K7-entry-missing`** (`receipts/B2-mutant-selftest.txt`). The new control does
  not kill the mutation it was built to kill.
- B3, in-process decomposition of both fixture shapes
  (`receipts/B3-k7-confound.txt`):
  - as-implemented (ghost-only registry): patched → `missing=[grader.py,
    plans/tool_a.py] entry_missing=[plans/ghost_tool.py] rc=1`; mutant → same
    legs, `rc=1` (MISSING masks the dropped term);
  - corrected per fixture-k7.md (ghost row inserted into the complete
    two-row table): patched → `missing=[] entry_missing=[plans/ghost_tool.py]
    rc=1`; mutant → `missing=[] entry_missing=[plans/ghost_tool.py] rc=0` —
    the control kills the mutation once the fixture is complete.
- B4, full `--lane` runs on the corrected fixture
  (`fixtures/k7-corrected`, kept in scratch, shape recorded below):
  old → `ENTRY-MISSING 1`, fail exit 1 (`receipts/B4-old-k7-corrected.txt`);
  patched → identical, fail exit 1 (`receipts/B4-patched-k7-corrected.txt`);
  mutant → prints `ENTRY-MISSING 1` but `PREDICATE R52-C2 pass`, exit 0
  (`receipts/B4-mutant_k7-k7-corrected.txt`). Note the K7 mutation target is
  the verdict wiring shared by old and patched — the control belongs to any
  landed repair of either.

## Runnable recipe (reproduces A1–B4 from a clean clone)

Prereqs: lane clone (shared) at `80afa613…`; scratch root
`/fast/scratch/hyaku/kengaku-r55/<seat>/`; python3 only. Set
`S=/fast/scratch/hyaku/kengaku-r55/<seat>`, `L=<lane clone>`,
`OLD=$L/plans/round52_c2_registry.py`,
`PATCHED=<lane>/.ufo/waves/round-54/w1/E3R52RegistryFix/round52_c2_registry.py`.
Run every step with `PYTHONDONTWRITEBYTECODE=1`; append `echo exit=$?` to each
counter run. Never edit `$OLD` or the lane.

1. **A1 raw-tip contrast.** `python3 $OLD --lane $L` → exit 1, `MISSING 2`
   (round54 pair), `SELFTEST-UNBACKED 0`. `python3 $PATCHED --lane $L` → exit 1,
   same `MISSING 2` plus `SELFTEST-UNBACKED 1 / \`order-check\``.
2. **A2 closed-registry flip (needs a writable lane copy).**
   `cp -al $L $S/lane-closed`; in `$S/lane-closed/SKILL.md` insert two complete,
   flag-free 8-cell rows (entry `python3 plans/round54_c1_anchor.py --lane .`
   and `python3 plans/round54_c2_entrytruth.py --lane . --source . --work DIR`,
   self-test cell `self-verifying; no flags accepted beyond entry`) immediately
   before the `round52-c2` row. `python3 $OLD --lane $S/lane-closed` → all legs
   0, pass, exit 0. `python3 $PATCHED --lane $S/lane-closed` →
   `SELFTEST-UNBACKED 1 / \`order-check\``, fail, exit 1. This is the red-before
   evidence: an all-green registry goes red solely because of the patch.
3. **A3 row isolation.** Parse `registry_block(SKILL.md)`, then for every parsed
   row compare `selftest_unbacked(row[4])` between `$OLD` and `$PATCHED`
   (load both via `importlib`); exactly one row flips — `` `order-check` ``,
   `False→True`. Cell text quoted in Defect 1 above.
4. **A4 intended-defect sanity.** Mini lane: `plans/tool_a.py` =
   `# no accepted flags`; `SCORECARD.md` = ``run `python3 plans/tool_a.py` ``;
   `SKILL.md` = `## Gate/probe registry` + 8-column header + one row
   ``| `t` | gate | `python3 plans/tool_a.py` | 0 ok | no --selftest; python3 plans/tool_a.py --check | none | read-only | kengaku |``.
   `$OLD` → pass exit 0 (the unbacked `--check` is masked); `$PATCHED` →
   `SELFTEST-UNBACKED \`t\``, fail exit 1.
5. **B1–B2 selftest mutation.** `python3 $PATCHED --lane $L --selftest` →
   `cases=6 failures=0`, exit 0. Build the mutant with the one-string
   replacement from the header; `--selftest` → identical output, exit 0,
   including `SELFTEST ok K7-entry-missing`. The K7 line in the B1 output
   (`MISSING 2` + `ENTRY-MISSING 1`) is the masking proof.
6. **B3 decomposition (optional, in-process).** Rebuild the K7-step tree twice —
   (a) SKILL.md registry = ghost row only; (b) SKILL.md registry = full two-row
   table + ghost row inserted; plans/ghost_tool.py absent in both. Call
   `collect()` and `verdict()` from each module. (a): both modules rc=1.
   (b): patched rc=1, mutant rc=0.
7. **B4 corrected-fixture end-to-end.** Mini lane `k7-corrected`: `plans/
   tool_a.py` = `# tool`; `grader.py` = `# grader`; `SCORECARD.md` =
   ``run `python3 plans/tool_a.py` and `python3 grader.py` ``; `SKILL.md` =
   registry header + rows `t`, `g` (self-test `none declared`) + the ghost row
   `| `ghost-tool` | gate | `python3 plans/ghost_tool.py --summary` | 0 ok | none | none | read-only | kengaku |`;
   do **not** create plans/ghost_tool.py. Run `$OLD`, `$PATCHED`, mutant:
   first two → `ENTRY-MISSING 1`, fail exit 1; mutant → `ENTRY-MISSING 1`
   printed, `PREDICATE R52-C2 pass`, exit 0.

## Fix directions (both already red-before/green-after in this recipe)

1. **Span-scoped attribution** in `selftest_unbacked` (r52-w2 W2RevRowsB
   `a3-fix-probe.py` prototype): attribute a flag only inside the backtick span
   that begins `python3 <script>`. Predicted: A2 patched-shape run keeps the
   order-check row green (its `--receipt`/`--claims` are not attributed to
   round40_c1_verify.py because that span names order_check.py... i.e. flags
   outside any `python3 …` span attach to the cell's entry script or are
   skipped per the prototype), while A4 still fails on `t`. A future seat must
   re-run A1–A4 against the actual patch and record receipts.
2. **K7 fixture correction:** insert the ghost row into the complete fixture
   table (per `fixture-k7.md`) instead of overwriting the registry. B4 is the
   red-before: with the corrected fixture the controls.json mutation flips the
   K7 verdict from fail to pass; with the as-implemented fixture it does not.

## Boundaries observed

No lane writes; production `plans/round52_c2_registry.py` byte-identical before
and after (sha256 above). No mutating git/jj in the fleet lane; the only
working-tree edit was inside the scratch hardlink copy `lane-closed` (SKILL.md
fixture rows). No tools installed. Scratch deleted after receipts were copied
into this directory.
