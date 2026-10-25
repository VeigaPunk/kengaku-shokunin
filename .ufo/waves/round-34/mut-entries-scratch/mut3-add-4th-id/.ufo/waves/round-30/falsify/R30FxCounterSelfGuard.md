# R30FxCounterSelfGuard — can the C2 counter be neutered without the receipt noticing?

Seat: `L1Kengaku30.R30FxCounterSelfGuard-3` (mutation tester, wave 2). Target:
`plans/round30_defects.py`, the C2 counting command. Five assigned mutants, each run on a
`/tmp` copy of the counter against a `/tmp` replica of the lane. No lane bytes written except this
report. Nothing installed (python3 3.14.8, git, rsync, `/usr/bin/diff` were already present).

**Revision pinned.** The counter is **untracked** in the lane (`?? plans/round30_defects.py` at
`363a4eb`), so there is no `HEAD:` copy to pin. All runs below are on the worktree bytes
`sha256:114b2aad561a2a9ec188fe09d8dca6a0597f8fd4a7a0239ab82d383f2997ba53`, 222 lines, 9479 B,
snapshot kept at `/tmp/r30fx-CounterSelfGuard/r30_defects.live114b.py`.

> **Drift measured mid-probe.** At 04:33 the same path hashed `19ce5332…` (220 lines); at 04:39 it
> hashed `114b2aad…` (222 lines) — a sibling landed a D3 tightening
> (`if lesson_match and "line 75" not in lesson[…]: return "lesson prices the quote but no longer
> locates it at line 75"`). I re-derived the whole probe set on the newer bytes; both revisions gave
> the same five verdicts. A counting command with no revision pin is therefore a moving predicate:
> see §Side findings, F3.

## Baseline (the detector before mutation)

Two baselines, because D1 and D4 are HEAD properties. Baseline A was captured on the pre-drift
bytes `19ce5332…` in the replica, and re-measured directly on the live lane tree with the
pinned bytes `114b2aad…` at the end of this probe — identical output (`defects=2`, exit 1,
D1 and D4 red); that direct run reads the lane and writes nothing (its only side effect is
git's index stat refresh). Replica run:

```
$ cd /tmp/r30fx-CounterSelfGuard/lane     # git clone --shared of the lane + rsync of its worktree
$ python3 plans/round30_defects.py --lane .        # HEAD 363a4eb, round-30 repairs UNCOMMITTED
DEFECT D1 receipt-at-cited-path: receipt exists only in the worktree: corpus/evidence/round29-attempt2/control-nothing.txt is not committed at HEAD
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
DEFECT D4 uncommitted-wave-evidence: HEAD:.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md omits the addendum ('### D. Addendum'); the wave evidence is not landed
ok D5 s091-usedby-asymmetry: repaired
defects=2
EXIT=1
```

```
$ git add -A && git commit -m "scratch: commit the repair state"   # replica only; HEAD bdcc4b0
$ python3 plans/round30_defects.py --lane .                       # BASELINE B, used for all verdicts
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
EXIT=0
```

Baseline B is the state the frozen C2 predicate names ("prints `defects=0` and exits 0 on the
repaired tree"). It is green, so a mutant that leaves it green is a survivor, not an inconclusive.

Direct lane measurement, pinned revision (`out/lane-final.txt`):

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/round30_defects.py --lane .
DEFECT D1 receipt-at-cited-path: receipt exists only in the worktree: corpus/evidence/round29-attempt2/control-nothing.txt is not committed at HEAD
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
DEFECT D4 uncommitted-wave-evidence: HEAD:.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md omits the addendum ('### D. Addendum'); the wave evidence is not landed
ok D5 s091-usedby-asymmetry: repaired
defects=2
exit=1
```

## The five assigned mutants

Mutant sources: `/tmp/r30fx-CounterSelfGuard/mut-live/`; guard mutants:
`/tmp/r30fx-CounterSelfGuard/guard-live/`. Each was generated from the pinned bytes by an
asserted single-occurrence replacement (no hand-editing), then diffed against the pristine file.

### m1 — `CHECKS` replaced with an empty tuple

`m1_empty_checks.py` `sha256:f3da071129a2c541…`, 216 lines (`CHECKS = ()`).

```
$ python3 /tmp/r30fx-CounterSelfGuard/mut-live/m1_empty_checks.py --lane .
defects=0
EXIT=0
```

**Verdict: SURVIVED.** The claim's whole detector — `defects=0` and exit 0 — is unchanged. The
only trace is that the five `ok …` lines are gone (10 B output vs 201 B). Nothing in the claim's
receipt shape, and nothing in the tool, counts the items.

### m2 — `check_d2` returns `''` always

`m2_d2_green.py` `sha256:62148a8ac706f302…`, 197 lines (body replaced by `return ""`).

```
$ python3 /tmp/r30fx-CounterSelfGuard/mut-live/m2_d2_green.py --lane .
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
EXIT=0
```

**Verdict: SURVIVED — byte-identical output.** `cmp` against the pristine run: identical (201 B,
exit 0). D2 is the item whose repair the lesson records as having gone wrong once already
(`round-30.md` Mistakes: the emphasis strip made D2 red for *any* lesson bytes), so a D2 that
cannot be red is the single most dangerous neuter in the file, and on the repaired tree it is
completely invisible.

### m3 — `check_d1` accepts any file (HEAD test deleted)

`m3_d1_any_file.py` `sha256:9a4980466a095977…`, 220 lines:
`text = head_blob(lane, D1_PATH)` + the `is None` branch replaced by `text = path.read_text(…)`.

```
$ python3 /tmp/r30fx-CounterSelfGuard/mut-live/m3_d1_any_file.py --lane .
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
EXIT=0
```

**Verdict: SURVIVED — byte-identical output** (`cmp`: identical). It is not inert: on a tree where
the receipt exists but `HEAD` does not carry it, the mutation converts a real red into green —

```
# fixture F_D1U: branch from master, `git rm --cached` the receipt, commit the deletion
# HEAD commits the removal; the worktree still holds the bytes
$ python3 plans/round30_defects.py --lane .
DEFECT D1 receipt-at-cited-path: receipt exists only in the worktree: corpus/evidence/round29-attempt2/control-nothing.txt is not committed at HEAD
ok D2 … ok D3 … ok D4 … ok D5 …
defects=1
EXIT=1
$ python3 /tmp/r30fx-CounterSelfGuard/mut-live/m3_d1_any_file.py --lane .
ok D1 receipt-at-cited-path: repaired
ok D2 … ok D3 … ok D4 … ok D5 …
defects=0
EXIT=0
```

This is exactly the class of defect C2 exists to catch (round 29's D1: "the report cites a file
that was absent"), so the survivor is a coverage gap in the *test*, not in the mutation.

### m4 — `check_d4` skips the addendum test

`m4_d4_skip_addendum.py` `sha256:86b41e7e850b9cdb…`, 220 lines: the `if D4_MARKER not in text:`
block deleted, `git status` test kept.

```
$ python3 /tmp/r30fx-CounterSelfGuard/mut-live/m4_d4_skip_addendum.py --lane .
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
defects=0
EXIT=0
```

**Verdict: SURVIVED — byte-identical output** (`cmp`: identical). Behaviour-bearing on the tree the
clause was written for (a commit that discards the bytes):

```
# fixture F_D4X: branch from master, `git checkout 363a4eb -- <D4 path>`, commit (worktree clean)
$ grep -c "### D. Addendum" .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md   # → 0
$ python3 plans/round30_defects.py --lane .
ok D1 … ok D2 … ok D3 …
DEFECT D4 uncommitted-wave-evidence: HEAD:.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md omits the addendum ('### D. Addendum'); the wave evidence is not landed
ok D5 …
defects=1
EXIT=1
$ python3 /tmp/r30fx-CounterSelfGuard/mut-live/m4_d4_skip_addendum.py --lane .
ok D1 … ok D2 … ok D3 … ok D4 … ok D5 …
defects=0
EXIT=0
```

### m5 — nothing tightened, a sixth check added

"Tighten nothing but add a sixth check" implemented as the weakest possible sixth item: it asserts
the counter script exists, which is invariant while the counter runs.
`m5_sixth_noop.py` `sha256:7604dd314069adac…`, 227 lines:

```python
def check_d6(lane: Path) -> str:
    return "" if (lane / "plans" / "round30_defects.py").is_file() else "counter script absent"
…
    ("D5", "s091-usedby-asymmetry", check_d5),
    ("D6", "counter-file-present", check_d6),
```

```
$ python3 /tmp/r30fx-CounterSelfGuard/mut-live/m5_sixth_noop.py --lane .
ok D1 receipt-at-cited-path: repaired
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
ok D4 uncommitted-wave-evidence: repaired
ok D5 s091-usedby-asymmetry: repaired
ok D6 counter-file-present: repaired
defects=0
EXIT=0
```

**Verdict: SURVIVED.** Padding the item list: the claim's frozen predicate says "the five checks
are exactly D1 … D5", and after this mutation the tool has six, all green, exit 0. The predicate
sentence is prose; no machine check compares the item set to a literal, so the difference is only
visible to a human reading the five→six lines. This is the mutation that most directly falsifies
the claim's wording: the receipt's `defects=0` is compatible with *any* number of items, including
ones that cannot fail.

### m1–m5 summary

| mutant | shipped detector (`defects=` + exit) | output vs baseline | behaviour-bearing? |
|---|---|---|---|
| m1 `CHECKS=()` | `defects=0` exit 0 → **SURVIVED** | 5 `ok` lines vanish (10 B vs 201 B) | yes (suppresses all five) |
| m2 `check_d2 → ''` | `defects=0` exit 0 → **SURVIVED** | **byte-identical** (201 B) | yes (red→green on F_D2RED) |
| m3 `check_d1` any file | `defects=0` exit 0 → **SURVIVED** | **byte-identical** (201 B) | yes (red→green on F_D1U) |
| m4 `check_d4` no addendum | `defects=0` exit 0 → **SURVIVED** | **byte-identical** (201 B) | yes (red→green on F_D4X) |
| m5 sixth no-op check | `defects=0` exit 0 → **SURVIVED** | one `ok D6` added (238 B) | yes (contradicts "exactly five") |

5/5 survivors. The counter's own bytes can be emptied, stubbed green per item, and padded, and its
counting command still prints the claim's exact expected output. Only m1 and m5 change the transcript
at all, and neither touches the `defects=` line or the exit code.

## Guard proposal

Smallest guard that makes the neutering visible in the round receipt, in two tiers — the second tier
is only needed for the retargeting class (§F2):

- **Tier 1 (required):** a `--selftest` mode that (a) compares the live `CHECKS` registry — ids and
  labels, in order — against a literal `FROZEN_CHECKS`, and (b) proves **each item can be red** by
  running it against a committed temp-tree where every item is red for its own reason, asserting the
  expected reason substring, not merely "non-empty". `main()` also gains the item count in its
  summary line, so a receipt that only quotes the total still carries `checks=`.
- **Tier 2 (recommended):** a `FROZEN_PATHS` pin, because a check can also be neutered by moving its
  *target* (D1 pointed at an always-committed file) rather than by weakening its body.

Measured: kills all five assigned mutants plus the retargeting and guard-removal probes.

### Code shape (one 97-line block plus three `main()` edits; nothing else changed)

Insert after the `CHECKS` tuple, plus `import tempfile`; the fixtures reuse the existing constants
(`D1_PATH`, `LESSON`, `REGISTRY`, `D4_PATH`, `EXPECT`, `ENTRY`, `QUOTE`, `QUOTED_LINE`, `WAVE_LINE`),
the existing `subprocess`/`json` imports and the existing `head_blob`:

```python
# --- self-guard: the counter's own registry, and its own ability to go red -------------
# The lesson records the failure this answers: "A counter whose only output is a total cannot
# show which of its own edits broke it" (corpus/lessons/round-30.md, Mistakes). A total alone
# cannot distinguish a repaired tree from a counter whose checks were emptied, stubbed green,
# or padded with an item that can never fail.
FROZEN_CHECKS = (
    ("D1", "receipt-at-cited-path"),
    ("D2", "kappa-sweep-scope"),
    ("D3", "s078-line75-word-count"),
    ("D4", "uncommitted-wave-evidence"),
    ("D5", "s091-usedby-asymmetry"),
)
# Tier-2 pin: each item's target bytes. A retargeted check (D1 pointed at an always-committed
# file) keeps the registry and can stay red on its own fixture only if the fixture moves too —
# the pin is what makes the move itself visible.
FROZEN_PATHS = {
    "D1": "corpus/evidence/round29-attempt2/control-nothing.txt",
    "D2": "corpus/lessons/round-29.md",
    "D3": "corpus/SOURCES.md",
    "D4": ".ufo/waves/round-29/attempt2/build/R29a2CritEntry.md",
    "D5": ".ufo/waves/round-29/attempt2/adoption-expect.json",
}
LIVE_PATHS = {"D1": D1_PATH, "D2": LESSON, "D3": REGISTRY, "D4": D4_PATH, "D5": EXPECT}


# One red fixture per item, each red for that item's own reason and nothing else.
EXPECT_RED = {
    "D1": "is not committed at HEAD",
    "D2": "in the lane",
    "D3": "registry S078 prices the line-75 quote at",
    "D4": "omits the addendum",
    "D5": "records no S091 used-by asymmetry note",
}


def _fixture(root: Path) -> None:
    """Build a tree where every frozen item is red, then commit it (D1 needs a HEAD)."""
    (root / "corpus" / "lessons").mkdir(parents=True, exist_ok=True)
    (root / "corpus" / "evidence" / "round29-attempt2").mkdir(parents=True, exist_ok=True)
    (root / D4_PATH).parent.mkdir(parents=True, exist_ok=True)
    (root / ENTRY).parent.mkdir(parents=True, exist_ok=True)

    # D2: the measured sweep is rendered lane-wide again.
    (root / LESSON).write_text(
        "kappa — `grep -rn kappa corpus/knowledge/*.md` → 0 hits in the lane\n", encoding="utf-8"
    )
    # D3: the row prices the line-75 quote at 99 words.
    row = ["S078"] + ["x"] * 10
    row[5] = '"' + QUOTE + '" (99 words)'
    (root / REGISTRY).write_text("| " + " | ".join(row) + " |\n", encoding="utf-8")
    # D4: committed, clean, and missing the addendum.
    (root / D4_PATH).write_text("# wave evidence without the addendum\n", encoding="utf-8")
    # D5: neither repair branch is recorded.
    (root / EXPECT).write_text(json.dumps({"usedby_notes": {}}), encoding="utf-8")
    (root / ENTRY).write_text("# entry\n", encoding="utf-8")
    for cmd in (
        ["init", "-q"],
        ["add", "-A"],
        ["-c", "user.name=selftest", "-c", "user.email=selftest@localhost", "commit", "-q", "-m", "fixture"],
    ):
        proc = subprocess.run(["git", "-C", str(root), *cmd], capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            raise RuntimeError(f"fixture git {cmd[0]} failed: {proc.stderr.strip()}")
    # D1: written after the commit, so the bytes exist only in the worktree.
    (root / D1_PATH).write_text(
        "\n".join([QUOTED_LINE, WAVE_LINE, "exit code of that run: 1", ""]), encoding="utf-8"
    )


def selftest() -> int:
    failed = 0
    registry = tuple((item_id, label) for item_id, label, _ in CHECKS)
    if registry != FROZEN_CHECKS:
        failed += 1
        print(f"  failed: check registry {registry!r} != frozen {FROZEN_CHECKS!r}")
    if LIVE_PATHS != FROZEN_PATHS:
        failed += 1
        print(f"  failed: check targets {LIVE_PATHS!r} != frozen {FROZEN_PATHS!r}")
    with tempfile.TemporaryDirectory(prefix="r30-defects-selftest-") as tmp:
        root = Path(tmp)
        _fixture(root)
        for item_id, label, check in CHECKS:
            try:
                reason = check(root)
            except Exception as exc:  # a check that raises on its own fixture proves nothing
                failed += 1
                print(f"  failed: {item_id} {label}: raised {type(exc).__name__}: {exc}")
                continue
            want = EXPECT_RED.get(item_id)
            if want is None:
                failed += 1
                print(f"  failed: {item_id} {label}: no frozen red fixture for this item")
            elif want not in reason:
                failed += 1
                print(f"  failed: {item_id} {label}: red fixture said {reason!r}, want {want!r}")
    print(f"SELFTEST checks={len(FROZEN_CHECKS)} failed={failed}")
    return 0 if failed == 0 else 1
```

and in `main()`:

```python
    parser.add_argument("--selftest", action="store_true",
                        help="assert the frozen registry and that every item can go red")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
…
    print(f"checks={len(CHECKS)} defects={defects}")     # was: print(f"defects={defects}")
```

### The receipt shape it needs (this is the half that makes it visible)

The guard protects nothing unless the round receipt is required to carry both lines, adjacent to
the counting command's own output:

```
$ python3 plans/round30_defects.py --selftest ; echo "exit=$?"
SELFTEST checks=5 failed=0
exit=0
$ python3 plans/round30_defects.py --lane . ; echo "exit=$?"
ok D1 … ok D5 …
checks=5 defects=0
exit=0
```

Why both: the `checks=` field alone catches m1 and m5 (`checks=0 defects=0`, `checks=6 defects=0`)
but is blind to m2/m3/m4, whose count is still 5. The selftest is what catches an item that cannot
go red. Conversely the counter is what catches the opposite failure — an item that is always red,
which is the mistake the round already made once (`round-30.md` Mistakes: the emphasis strip made
D2 red for any lesson bytes): that shows up as `defects=1` on the repaired tree, so the pair covers
both directions for a single item. Absence of either line must count as red at closure.

### Guard measured against the mutants

Guarded body: `/tmp/r30fx-CounterSelfGuard/guard/round30_defects_guarded_live.py`
`sha256:66605a84d5c3f59d…`, 325 lines (same guard block re-applied to the pinned 222-line counter).
The five assigned mutations were re-applied to *that* file (`guard-live/`).

```
$ python3 …/round30_defects_guarded_live.py --selftest
SELFTEST checks=5 failed=0
EXIT=0
$ python3 …/round30_defects_guarded_live.py --lane .
ok D1 … ok D5 …
checks=5 defects=0
EXIT=0
```

| mutant of the guarded counter | `--selftest` output (tail) | exit | verdict |
|---|---|---|---|
| gm1 `CHECKS=()` | `failed: check registry () != frozen (…)` / `SELFTEST checks=5 failed=1` | 1 | KILLED |
| gm2 `check_d2 → ''` | `failed: D2 kappa-sweep-scope: red fixture said '', want 'in the lane'` / `SELFTEST checks=5 failed=1` | 1 | KILLED |
| gm3 `check_d1` any file | `failed: D1 receipt-at-cited-path: red fixture said '', want 'is not committed at HEAD'` / `SELFTEST checks=5 failed=1` | 1 | KILLED |
| gm4 `check_d4` no addendum | `failed: D4 uncommitted-wave-evidence: red fixture said '', want 'omits the addendum'` / `SELFTEST checks=5 failed=1` | 1 | KILLED |
| gm5 sixth no-op | `failed: check registry (… 'D6', 'counter-file-present') != frozen (…)` and `failed: D6 counter-file-present: no frozen red fixture for this item` / `SELFTEST checks=5 failed=2` | 1 | KILLED (twice) |
| gp1 (`D1_PATH` retargeted to `corpus/README.md`) | `failed: check targets {'D1': 'corpus/README.md', …} != frozen {…}` | 1 | KILLED by tier 2 only |
| gg1 (`--selftest` flag and guard block stripped) | `error: unrecognized arguments: --selftest` | 2 | **not killed** — the guard is removable; only the receipt's requirement on the `SELFTEST checks=5 failed=0` line makes the removal visible |

Full tails, verbatim (one representative, the double kill):

```
$ python3 …/guard-live/gm5_sixth_noop.py --selftest
  failed: check registry (('D1', 'receipt-at-cited-path'), ('D2', 'kappa-sweep-scope'), ('D3', 's078-line75-word-count'), ('D4', 'uncommitted-wave-evidence'), ('D5', 's091-usedby-asymmetry'), ('D6', 'counter-file-present')) != frozen (('D1', 'receipt-at-cited-path'), ('D2', 'kappa-sweep-scope'), ('D3', 's078-line75-word-count'), ('D4', 'uncommitted-wave-evidence'), ('D5', 's091-usedby-asymmetry'))
  failed: D6 counter-file-present: no frozen red fixture for this item
SELFTEST checks=5 failed=2
EXIT=1
```

## Residual limits of the proposal (recorded, not smoothed)

- **Removable, not tamper-proof.** gg1: delete the flag and `--selftest` exits 2. Only the receipt
  contract (both lines present, absence = red) closes this. Same for the pin: an operator could edit
  `FROZEN_CHECKS`/`FROZEN_PATHS` too, and no in-file device survives an in-file edit. What the guard
  buys is that the neuter must be *deliberate and multi-site*, and the receipt line moves.
- **One fixture per item, not per clause.** D1 has three assertions (path, quoted line, wave line,
  exit line). My fixture proves the path/HEAD clause can fail; a mutant that deletes only the
  `exit code of that run: 1` test would still be red on the fixture and green on the lane — it
  survives the guard. Full strength needs one fixture per clause (`EXPECT_RED` becomes a dict of
  clause→substring lists). I did not build that; it is the next tightening, not covered here.
- **The fixture is built from the same constants the checks read**, so moving a constant moves the
  check and its fixture together: the tier-1 red test stays green, and only the tier-2
  `LIVE_PATHS != FROZEN_PATHS` pin sees the move. A mutant that edits the constant *and* the pin is
  beyond any in-file guard.
- **git dependency.** `_fixture` shells out to `git`; without git the selftest raises (non-zero,
  loud) rather than silently passing — acceptable, but it means the guard is not a pure-python
  predicate.

## Side findings (outside the assigned probe, calibration)

- **F1 — the C2 freeze control is not reproducible from the shipped counter.**
  `.ufo/waves/round-30/claims/defects-before.txt` (7 lines, `sha256:040a882…`) prints
  `DEFECT D4 uncommitted-wave-evidence: .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md is
  uncommitted: M .ufo/…`. The shipped counter has no such message; its D4 text is
  `f"{D4_PATH} still differs from HEAD: {status.stdout.strip()}"`. So the control was produced by a
  revision that exists nowhere — the tool is untracked at `363a4eb`, so there is no `HEAD:` copy and
  no history either. D1's and D2's control lines do match current format strings verbatim. A control
  whose bytes no shipped revision can emit cannot be re-derived by a later reader.
- **F2 — retargeting is the cheap neuter the claim does not exclude.** C2's predicate names the five
  items by label, not by target bytes. `D1_PATH = "corpus/README.md"` gives
  `DEFECT D1 …: the committed receipt does not carry the report's quoted seven-field line verbatim`
  → `checks=5 defects=1` — i.e. red on the repaired tree, so the counter still refuses, while the
  item no longer reads the receipt the claim names. Direction of failure differs (false red, not
  false green), so this is a *predicate drift* risk rather than a green-washing one.
- **F3 — the counting command has no revision pin.** `plans/round30_defects.py` moved under this
  seat mid-probe (`19ce5332…` → `114b2aad…`, ~6 min apart) and is untracked, so "`defects=0`" in the
  receipt names a behaviour, not bytes. Minimal fix, one line in the receipt:
  `python3 plans/round30_defects.py --lane .` recorded together with
  `sha256:plans/round30_defects.py` (or run the blob: `git show <tip>:plans/round30_defects.py |
  python3 - --lane .`).
- **F4 — baseline A shows the claim's zero is a HEAD property, not a working-tree one.** On the live
  lane state (repairs present, uncommitted) the counter prints `defects=2`, exit 1. That is correct
  behaviour, but it means the C2 receipt must be generated after the commit that lands D1's receipt
  and D4's addendum, and a re-run before that commit is not a falsification of the claim.

## Restoration evidence

Nothing in the lane was edited; every mutation ran from `/tmp`. Restoration was verified by hash.

| object | before | after all runs |
|---|---|---|
| lane `plans/round30_defects.py` | `114b2aad561a2a9ec188fe09d8dca6a0597f8fd4a7a0239ab82d383f2997ba53` | same (read-only throughout) |
| replica `plans/round30_defects.py` | `114b2aad…` | same (mutants were separate files; never edited in place) |
| replica `corpus/evidence/round29-attempt2/control-nothing.txt` | `d31200d6d9a2552fbc95c5d76ec92caef44ffbe24cd14aeebbe4b2d621db6a73` | same after the F_D1U fixture (`git reset --hard master`) |
| replica `.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md` | `0d094c7f3dcbb2190955884f2effb3472b3e8b6f2b3d67e78ce87992f7b45d40` | same after the F_D4X fixture; addendum present (`grep -c` → 1) |
| replica `corpus/lessons/round-29.md` | committed bytes | same after F_D2RED (`git checkout --`) |
| replica git state | `master`, clean, HEAD `bdcc4b0` | `master`, `git status --porcelain` = 0 lines, fixture branches deleted, HEAD `bdcc4b0` |
| scratch root | `/tmp/r30fx-CounterSelfGuard/` (lane replica 484 MB + `mut/`, `mut-live/`, `guard/`, `guard-live/`, `out/`, snapshots) | retained for re-derivation; the lane replica is scratch, not lane evidence |

Scratch paths of everything cited: `r30_defects.live114b.py` (pinned counter),
`lane/` (replica), `mut-live/m1…m5`, `guard/round30_defects_guarded_live.py`,
`guard-live/gm1…gm5, gp1, gg1`, `out/base.txt` + `out/m1…m5.txt` (byte-comparison inputs).

No `VERDICT:` line: this seat is a mutation probe, not a source re-read or the complete-set review,
so the machine-read candidate/verdict contract does not apply and a stray anchored verdict would be
a false signal to `plans/gate_timing_check.py` Q10.
