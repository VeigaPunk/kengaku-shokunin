# F39RevBatP1 — code review of `plans/battery39/p1m.py` (the M02 kill)

Seat F39RevBatP1, kengaku round 39 wave 2 (FALSIFY), 2026-10-26. Lane tip reviewed: `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`
(clean scratch clone at `/fast/scratch/hyaku/kengaku-r39/F39RevBatP1/lane`, `git status --porcelain` = 0 lines; deleted after the runs).
Scope: does p1m.py's one fixture honestly exhibit M02's advertised behaviour (a non-first frozen instrument off its pin),
with no state that changes between the counter's phases, no side channel, exact declared defects — and is it load-bearing?
Method: source read + counter runs (`--battery-dir`, `--only M02`) + direct gate probes + byte-level state snapshots.
All commands and full outputs are recorded verbatim in `.ufo/waves/round-39/falsify/F39RevBatP1/` (receipts listed at the end).
Every number below was produced twice (an ad-hoc pass, then the recorded pass); the two passes agree on every line.

## 0. What M02 advertises

`plans/round39_c1_verify.py:116-121` freezes M02 as clause `P1`, direction `silence`, one byte-level edit of the gate:

- old (`:120`): `bad = [rel for rel, dig in pins.items() if sha256(p.root / rel) != dig]`
- new (`:121`): `bad = [rel for rel, dig in list(pins.items())[:1] if sha256(p.root / rel) != dig]`

Advertisement (`:117`): "every frozen instrument is checked against its pin, not only the first". The gate's swept line is
`plans/pkg_gate.py:114` inside `c_instruments` (`:112-115`), where `pins = p.spec.get("frozen_instruments", {})` (`:113`).
Pre-freeze witness on record, verified: `.ufo/waves/round-38/falsify/F38XMutP/witness-run.txt:1`
`WITNESS wx01 mutant=X01 ref_rc=1 ref_defects=P1,P9 mut_rc=1 mut_defects=P9 flip=P1->P1-ok ok`. The counter never reads the
witness (docstring, `plans/round39_c1_verify.py:44-45`); the battery fixture is the kill carrier under review.

## 1. The module

`plans/battery39/p1m.py` is 39 lines: docstring (`:1-19`), `import pathlib` (`:21`), `OFF_PIN = b"\n# p1m off-pin witness byte\n"` (`:23`),
one `build` (`:26-36`), one FIXTURES entry (`:39`):

```python
FIXTURES = [{"fid": "p1m-second-pin-appended-bytes", "expect": "reject", "defects": ["P1"], "build": build}]
```

`build` (`:26-36`): `ctx.genuine_package(d)` (`:27`), read pin order from the spec `rels = list(ctx.spec["frozen_instruments"])` (`:28`),
guard `len(rels) < 2` → RuntimeError (`:29-30`), target the SECOND pin `f = d / pathlib.PurePosixPath(rels[1])` (`:31`),
guard absent file → RuntimeError (`:32-33`), append `f.write_bytes(f.read_bytes() + OFF_PIN)` (`:34`), stage `ctx.git_add(d)` (`:35`),
return `["package", "--root", str(d), "--require-clean-tree"]` (`:36`).

## 2. Finding A — the advertised behaviour is exhibited, and honestly (non-first pin)

- **Pin order is read, never hardcoded** (`p1m.py:28`), as the docstring claims (`:13`). The spec carries exactly three pins, in order
  `plans/tb2_grader_probe.py`, `plans/round35_c1_verify.py`, `plans/defect_ledger.py` (`plans/pkg-spec-r35.json:33-37`), so `rels[1]`
  is the second pin. Both the counter's `ctx.spec` (`plans/round36_c1_verify.py:51-52`, `json.loads`) and the gate
  (`plans/pkg_gate.py:382`, `json.loads`) parse the same file order-preservingly, so the mutant's `list(pins.items())[:1]` is
  exactly `rels[0]` = `plans/tb2_grader_probe.py` — the pin the fixture leaves genuine. The fixture therefore sits precisely in
  the mutant's blind spot, not merely somewhere in the pin map.
- **Probe receipt** (`.ufo/waves/round-39/falsify/F39RevBatP1/probe-direct.txt`, fixture built via the counter's own
  `--build-module` child, rc=0): `pin plans/tb2_grader_probe.py: sha-match=True offpin-present=False`;
  `pin plans/round35_c1_verify.py: sha-match=False offpin-present=True`; `pin plans/defect_ledger.py: sha-match=True offpin-present=False`.
  The corrupted file ends `sys.exit(main())\n\n# p1m off-pin witness byte\n` — exactly `OFF_PIN` (`p1m.py:23`) appended after the
  genuine last line, nothing else touched.
- **Reference run** on the fixture (full gate stdout in the receipt): `P1 DEFECT pinned=3 mismatched=['plans/round35_c1_verify.py']`,
  `P2 ok` … `P9 ok untracked=0 first=0`, `defects=1`, rc=1. **Mutant run**: `P1 ok pinned=3 mismatched=0`, `defects=0`, rc=0.
  That is the declared silence, clause-level, on a non-first pin.
- **Counter attribution**: `MUTANT M02 P1 silence killed by=p1m-second-pin-appended-bytes` in the isolated run
  (`run-a-iso.txt`, `--battery-dir` = scratch dir holding only `p1m.py`, `MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0`, RC=0)
  and in the full landed-battery context (`run-a-full.txt`, `--battery-dir $S/lane/plans/battery39`, `BATTERY fixtures=90 wrong=0`,
  same kill line, RC=0). No other battery39 module is needed for the M02 kill.

## 3. Finding B — no state changes between the counter's phases

The fixture directory experiences, in order: child build → reference run → renamed `copytree` read → null-gate run → mutant run
(and, under the L1 audit, a reference re-run and mutant re-run after the kill: `plans/round39_c1_audit.py:395-398`). Checks:

- Byte-level sha256 snapshot of **every file under the fixture dir including `.git`**, taken around each phase
  (probe-direct.txt): `STATE build->run1 changed: []`, `STATE run1->run2 changed: []`, `STATE run2->mut changed: []`.
  Not even git's index is rewritten by a gate run (`c_clean_tree` is `git ls-files --others --exclude-standard` only,
  `plans/pkg_gate.py:259-265`).
- The reference run twice on the same dir is byte-identical (`REF RUN2 rc=1 identical=True`).
- The L1 audit's own A1 re-check passes on this module: `run-audit-iso.txt` prints `AUDIT nondeterministic_kills=0`,
  `PINS final total=26 mismatched=0`, `AUDIT C1 clean`, RC=0.
- The staged state is built once and static: `git diff --cached --stat` shows the package staged, `git diff --quiet` rc=0
  (no unstaged drift), `git ls-files --others` empty. `ctx.git_add` is `git(d, "add", "-A")` — "index only: no commit, no identity"
  (`plans/round37_c1_verify.py:207-208`); `ctx.genuine_package` git-inits d and copies the package with the "index not updated"
  (`plans/round37_c1_verify.py:198-206`), so the staging happens exactly once, in the build child.

## 4. Finding C — no side channel

- The counter's own token sweep (`/proc`, `ppid`, `cmdline`, `psutil`, `environ`, `plans/round39_c1_verify.py:59`) reports
  `sidechannel=0` in all three counter runs (`BATTERY fixtures=… sidechannel=0` in run-a-iso.txt, run-a-full.txt, run-b-noedit.txt).
- By read of the source: `build` writes only under `d` (package copy `:27`, append `:34`, index `:35`); the returned argv carries no
  `--spec`, so the counter appends the frozen lane spec (`plans/round39_c1_verify.py`, `run_gate`) and the fixture cannot steer the
  spec; the module reads nothing about the harness process.

## 5. Finding D — exact declared defects

Declared `expect=reject`, `defects=["P1"]` (`p1m.py:39`). Observed on the reference: rc=1 and DEFECT set exactly `{P1}`
(`FIXTURE p1m-second-pin-appended-bytes expect=reject declared=P1 observed_rc=1 observed_defects=P1 ok` in run-a-iso.txt and
run-a-full.txt — the counter compares the observed set for equality, `plans/round39_c1_verify.py` fixture loop). The full gate
stdout (probe-direct.txt) shows `P2 ok` … `P9 ok`, `defects=1`: no undeclared clause fires, none declared goes missing.
`--require-clean-tree` (`p1m.py:36`) makes P9 run and pass — the staged modification is invisible to the untracked-files check,
exactly as the docstring promises (`p1m.py:15-16`).

## 6. Finding E — load-bearing (fixture's edit removed)

One-line delta in a scratch copy (`bat39-noedit/p1m.py:34`): `f.write_bytes(f.read_bytes() + OFF_PIN)` → `f.write_bytes(f.read_bytes())`;
`diff` against the verbatim copy shows that single line, nothing else. Counter run (`run-b-noedit.txt`, `--battery-dir bat39-noedit --only M02`):

```
FIXTURE p1m-second-pin-appended-bytes expect=reject declared=P1 observed_rc=0 observed_defects=- WRONG
BATTERY fixtures=87 wrong=1 renamed_disagree=0 sidechannel=0
MUTANT M02 P1 silence SURVIVED exhibits=none -- …
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
RC=1
```

With the append gone the package is fully green (rc=0), the declared defect set no longer holds, and M02 exhibits nothing on any
fixture — `SURVIVED exhibits=none`. The appended byte is the sole carrier of the M02 kill, matching the docstring's claim
(`p1m.py:17-18`).

## 7. Observations (recorded; none is a defect in p1m.py)

- **O1 — derivative rc flip.** Because P1 is the fixture's only defect, silencing it also flips rc 1→0, so the pair also satisfies
  `rc-silence` on this fixture. The kill rule uses the declared direction (`silence`), which is the clause-level truth and what the
  witness recorded; the rc flip is a logical consequence, not a mislabel. No action.
- **O2 — `git add -A` is load-bearing for P9.** `genuine_package` leaves the index empty, so without `:35` every package file is
  untracked and P9 fires. The docstring's "index-only `git add`" wording (`p1m.py:15`) matches the helper
  (`plans/round37_c1_verify.py:208`).
- **O3 — package bytes come from the lane worktree.** `copy_package` does `shutil.copy2(lane / rel, dest / rel)`
  (`plans/round36_c1_verify.py:55-70`), i.e. worktree, not committed bytes. On the measurement surface (clean clone of the tip)
  worktree == HEAD, and the spec pins self-protect: a tampered worktree instrument trips P1 in the reference run, making the
  fixture WRONG rather than producing a false kill. Pre-existing round-36 helper property, outside p1m.py; no action here.
- **O4 — pin-order coupling fails safe.** The kill depends on the gate's `pins` dict order matching the spec order (both
  `json.loads` of the same file). If a future gate reordered pins such that the corrupted file became the mutant's first pin, the
  mutant would catch the corruption and M02 would print `SURVIVED` — a visible survivor, never a false pass.

## 8. Receipts (all under `.ufo/waves/round-39/falsify/F39RevBatP1/`)

| file | command (header line inside) | key result |
|---|---|---|
| `run-a-iso.txt` | `python3 plans/round39_c1_verify.py --lane $S/lane --battery-dir $S/bat39 --only M02 --work $S` | `BATTERY fixtures=87 wrong=0 renamed_disagree=0 sidechannel=0`; `MUTANT M02 P1 silence killed by=p1m-second-pin-appended-bytes`; `MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0`; RC=0 |
| `run-a-full.txt` | same with `--battery-dir $S/lane/plans/battery39` | `BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0`; same kill line; RC=0 |
| `run-b-noedit.txt` | same with `--battery-dir $S/bat39-noedit` | fixture `WRONG` (observed_rc=0), `MUTANT M02 … SURVIVED exhibits=none`, `killed=0 survived=1`; RC=1 |
| `run-audit-iso.txt` | `python3 plans/round39_c1_audit.py --lane $S/lane --battery-dir $S/bat39 --only M02 --work $S` | `PINS final total=26 mismatched=0`; `AUDIT nondeterministic_kills=0`; `AUDIT C1 clean`; RC=0 |
| `probe-direct.txt` | `--build-module` child + direct `pkg_gate.py` / M02-gate runs + sha256 snapshots | pin states, full ref/mutant stdout, `STATE … changed: []` ×3, `REF RUN2 identical=True` |

`$S` = `/fast/scratch/hyaku/kengaku-r39/F39RevBatP1` (deleted after the runs; receipts copied out first). No lane file was edited;
no git state in the lane was touched; no process was left running.

## 9. Verdict

The single fixture does what its docstring declares, in the order the docstring declares: the second pinned instrument
(`plans/round35_c1_verify.py`) carries appended bytes over an otherwise genuine package, the first pin stays genuine, the
reference prints exactly `P1 DEFECT` and exits 1, the M02 mutant prints `P1 ok` and exits 0, nothing in the fixture directory
changes between the counter's phases (byte-level snapshots empty; audit A1 clean), there is no side channel, the declared defect
set is exact, and removing the fixture's edit makes M02 survive. No defect found.

VERDICT: p1m-honest
