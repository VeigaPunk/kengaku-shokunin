# F38RevBatA — battery38 b1run.py + mainx.py attack (round 38 wave 2, falsify)

Seat: reviewer, calibration lane. Target: `plans/battery38/b1run.py` (N01, N16) and
`plans/battery38/mainx.py` (N17, N18) — for each fixture: does it demonstrate the ADVERTISED
behaviour its mutant names (the `adv` cell in `plans/round38_c1_verify.py` MUTANTS), or does it
kill incidentally (tailored `defects`, a spec the gate would never see, a second clause doing the
work)? Side channels (gate-file reads, timing, env, argv inspection, fixture-name keying) and the
delete-each-fixture necessity test. Landing tip under attack: `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`.

Axes: calibration (are the 4 kills attributable and advertised), operability (do the counter and
fixtures behave as their docstrings claim under adversarial mutation of the battery itself).

## Method

All work in `S=/fast/scratch/hyaku/kengaku-r38/F38RevBatA` (clone at the landing tip, `PINS
total=14 mismatched=0` on every run; scratch deleted at the end). Counter invoked exactly as
specified: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round38_c1_verify.py
--lane "$S/lane" --only <mutants> --work "$S/w"`. Evidence receipts in this directory:
`run-a-4mutants-intact.txt`, `deletion-tests.txt`, `ref-vs-mutant-evidence.txt`, `driver.py`.

1. Intact-clone run, `--only N01,N16,N17,N18` → `BATTERY fixtures=86 wrong=0 renamed_disagree=0
   sidechannel=0`, `MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0`, each killed by
   exactly its own fixture (`run-a-4mutants-intact.txt`).
2. Delete-each-fixture test (clone edits confined to the two modules' `FIXTURES` lists;
   `deletion-tests.txt`):
   - delete `b1run-n01-empty-pins` → `MUTANT N01 P1 silence SURVIVED` (fixtures=85)
   - delete `b1run-n16-clause-crash` → `MUTANT N16 RUN silence SURVIVED` (fixtures=85)
   - delete `mainx-root-not-a-directory` → `MUTANT N17 MAIN silence SURVIVED` (fixtures=84)
   - delete `mainx-spec-invalid-json` → `MUTANT N18 MAIN silence SURVIVED` (fixtures=84)
   - delete all four → all four SURVIVED (fixtures=82): no other r36/battery37/battery38 fixture
     substitutes. Every kill is UNIQUELY attributable to its fixture.
   - clone restored byte-exact afterwards (sha256 of both modules equal to the fleet tree;
     recorded at the end of `deletion-tests.txt`).
3. Reference-vs-mutant mechanism run (`driver.py`, output in `ref-vs-mutant-evidence.txt`): each
   fixture dir rebuilt via the counter's own `r37.Ctx` + `build()`, then reference and frozen
   mutant gate executed on the same argv, full rc/stdout/stderr captured.

## Per-fixture adjudication

### b1run-n01-empty-pins → N01 (P1, silence) — CLEAN

Advertised: "an empty frozen_instruments pin set is not an accept". Citation verified real:
SCORECARD.md:564 `package-gate` row contains "against a spec of pinned digests"; R37PlanNext §3.2
B1 names the shape ("P1 with an **empty** `frozen_instruments`"; "no — the spec is fixed and
non-empty" — i.e. precisely the gap this fixture closes). Mechanism (direct run): ref prints
`P1 DEFECT pinned=0 mismatched=0`, rc=1; mutant prints `P1 ok pinned=0 mismatched=0`, rc=0. The
ONLY differing clause is P1 — the clause the mutant edits (`c_instruments`,
`bool(pins) and not bad` → `not bad`) and the clause in the `adv` cell; rc flips 1→0, so the
demonstrated failure is the advertised false accept, not a side effect. The fixture-owned spec is
not a "spec the gate would never see" in the gameable sense: it is the genuine round-35 spec with
`frozen_instruments` emptied, over genuine package bytes — the empty-pins scenario cannot be
expressed with the counter-owned spec, which is exactly why B1 was undemonstrated in round 37
(claims §C1 sanctions fixture-owned specs for shapes B1/B6/B8). `defects: ["P1"]` is enforced by
the counter against the reference's observed set (`res[1] == frozenset(declared)`), so no
tailored over-declaration is possible; P2–P9 are all `ok` in both runs, so no second clause does
the work. P9 stays clean because the fixture `git_add`s its spec (`ctx.git_add`, index only).

### b1run-n16-clause-crash → N16 (RUN, silence) — CLEAN

Advertised: "a clause that cannot run is a defect, never a pass" — the run_checks comment in the
gate source (`except Exception as e:  # a clause that cannot run is a defect, never a pass`) and
R37PlanNext B6. Mechanism: `c_quote_shape` begins `lo, hi = rules["quote_words"]`; the fixture's
`entry_rules.quote_words = [3]` raises `ValueError: not enough values to unpack (expected 2, got
1)` at that unpack. Ref: `P3 DEFECT clause error ValueError: ...`, rc=1. Mutant: `P3 ok clause
error ValueError: ...`, rc=0 — the crash handler's note text is preserved verbatim while the
verdict flips, i.e. the mutant demonstrably maps a clause error onto a pass, the exact advertised
violation. Only P3 differs; the fixture declares exactly `["P3"]`, enforced equal to the observed
reference set. The spec mutation is the minimal way to reach B6 at all: the gate tolerates every
malformed PACKAGE byte (`read()` → None paths), so a clause can only be made to raise through a
spec value, which the counter does not own — the fixture-owned spec here is the sanctioned shape,
not a smuggled oracle. P1 shows `pinned=3` in both runs: this fixture does not borrow the N01
empty-pins shape.

### mainx-root-not-a-directory → N17 (MAIN, silence) — CLEAN

Advertised: "a --root that is not a directory is a setup error, exit 2" (gate docstring "exit 0 =
accept, 1 = reject, 2 = usage/setup"; R37PlanNext B7, whose own note predicted the mechanism:
"only by an argv trick (`--root` to a missing path)" — mainx does exactly that and nothing more).
Mechanism: ref prints `setup: root not a directory: ...` to stderr, rc=2, no clause lines; mutant
(`if False:`) falls through to `cmd_package` on the missing tree and exits 1 with nine clause
DEFECTs — matching mainx's module docstring claim ("falls through into `cmd_package` on a missing
tree, whose clauses report DEFECT and exit 1") exactly; I verified the mechanism rather than
trusting the docstring. Kill per the frozen MAIN rule (expect=error, ref rc==2, mutant rc==1);
the observable difference is the advertised exit contract itself. Note for the record (not a
defect): the mutant's failure direction here is a wrong exit code (2→1), not a false accept — the
mutant still refuses the package, just with the wrong exit class and a wall of bogus clause
DEFECTs. The `d` directory stays empty on purpose and the builder raises if `absent-root`
somehow exists; the renamed-copy check passes (renamed_disagree=0), so no path-marker keying.

### mainx-spec-invalid-json → N18 (MAIN, silence) — CLEAN

Advertised: "an unexpected crash never maps onto 0 or 1" (gate docstring). Mechanism: spec bytes
`{"rows": {\n` → `json.loads` raises `JSONDecodeError` inside main's try (spec load precedes the
root guard in `main` — mainx's ordering claim checked against the gate source and confirmed
true); ref: stderr `setup: JSONDecodeError: Expecting property name enclosed in double quotes:
line 2 column 1 (char 11)`, rc=2. Mutant (`return 2` → `return 0`): same stderr line, rc=0, zero
stdout — the crash is mapped onto accept with no diagnostics, the exact advertised violation.
`defects: []` enforced; no clause ever runs, so no clause side channel exists.

## Side-channel audit (both modules, full source read + grep)

`grep -iE '\bos\b|sys\.|argv|getenv|environ|time|inspect|subprocess|open\(|exec|eval|getattr|__import__|base64|/proc|ppid|cmdline|psutil|importlib|pkg_gate|\.lane|fid'`
over both files hits only innocuous substrings: the `fid` label strings, `import-time` (docstring),
`RuntimeError` (contains "time"), and the helper name `_package_argv`. No `os`, no `sys`, no env
or argv access, no timing, no file reads outside the fixture dir, no dynamic code loading, no
reference to the gate file or the lane. `mainx.py` imports nothing at all; `b1run.py` imports only
`copy` and `json`.

Structural closure (why these fixtures could not hide a side channel even in principle): the
counter materializes all gate copies (`gdir`) only AFTER every `build()` has returned, and
`build()` returns a static argv — a fixture cannot know which gate copy it will face, and the
null-detector re-run (`null_detected=0` in every run) would expose non-determinism. Fixture-name
keying is impossible through the gate ("never asks what the caller calls its fixture and never
inspects a path for a fixture marker", gate docstring; empirically `renamed_disagree=0` in all
six runs). The counter additionally enforces, for battery38 fixtures, that a fixture-owned
`--spec` path resolves inside the fixture's own directory.

## Findings

**0 defects in `plans/battery38/b1run.py` and `plans/battery38/mainx.py`.** All four kills are
attributable under the frozen kill rule, demonstrate exactly the behaviour their `adv` cell names
(citations verified: SCORECARD.md:564; R37PlanNext §3.2 B1/B6/B7/B8; gate docstring and run_checks
comment), are uniquely produced by their fixture (deletion tests), and use no side channel,
fixture-name keying, or second-clause work. mainx's two mechanism claims in its module docstring
(spec-load-before-root-guard; fall-through to clause DEFECTs exit 1) are both true — verified by
direct mutant execution, not by trusting the docstring.

Residual observations (about the harness, not defects in these modules; both already flagged as
limits in the frozen claims):

1. The side-channel token scan (`/proc`, `ppid`, `cmdline`, `psutil`, `environ`) cannot see
   `sys.argv`: a fixture's `build()` runs inside the counter process, so `import sys; sys.argv`
   would reveal `--only`/`--battery-dir` dev-mode flags with zero scanned tokens. Neither module
   imports `sys` (grep receipt above); the claims already call the scan "a heuristic, not a proof"
   and prescribe non-author review — this report is that review for these two modules. If the
   harness ever wants to close it, `"sys.argv"`/`"import sys"` is the missing token pair, at the
   cost of false positives on any module that legitimately imports sys.
2. `build()` receives the shared `Ctx`; a fixture that mutated `ctx.spec` in place would poison
   every later fixture's default spec (an ordering side channel the counter does not re-check).
   Both modules use `copy.deepcopy(ctx.spec)` and never touch `ctx` state — correct pattern; worth
   keeping on the checklist for future battery modules.

Residual risk: low. The four fixtures are minimal, single-purpose, and their kills collapse to a
one-clause (N01, N16) or one-exit-path (N17, N18) difference under direct ref-vs-mutant diffing;
nothing in either module survives adversarial reading.

Verification gaps: none within seat scope. The other ten battery38 modules, the N21
silence-vs-mirror question, and the full 22-mutant predicate receipt are other seats' scope; my
six counter runs all printed `PINS total=14 mismatched=0` and `BATTERY ... wrong=0
renamed_disagree=0 sidechannel=0` on the landing-tip clone, consistent with the landing receipt
`MUTANTS total=22 killed=21 survived=1`.

VERDICT: battery-b1run-mainx-attack-0-defects
