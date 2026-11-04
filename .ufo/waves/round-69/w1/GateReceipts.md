# GateReceipts — round 69 w1

Axes: coverage and calibration. Leaf seat. I produced and byte-verified the two R69-C2 E7
gate receipts. No predicate, case table, vector, kill rule, target, gate script, claim, or
lane source was edited; no git/jj write command was run anywhere; no corpus file was written
by this seat.

Capture time: `2026-11-04T00:08:41Z` (lane working tree; HEAD `b288e8e0`, worktree carrying
uncommitted round-69 corrections from sibling seats).

## Deliverables (this seat's writes)

| path | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-69/w1/gates/depth-gate.txt` | 104 | `f683297c35998f66187475daf2f68333f62294fab9356d436cba459c02efc9d9` |
| `.ufo/waves/round-69/w1/gates/trio.txt` | 65 | `d877fe2fa696bf0cb45255fd159ef5fe92946f7d088237e282d92cd974922cb7` |
| `.ufo/waves/round-69/w1/GateReceipts.md` | this file | — |

Exact bytes (no shell prompt, no reformatting; each file ends with one `\n`):

```
ROWS n=16 class_match=True count_mismatch=0 paths total=33 resolved=33 share=1.00
PREDICATE R63-C2 pass
```

```
TRIO pass corpus/knowledge/tb2-network-service-offline-grader.md
```

Scratch: `S=/fast/scratch/hyaku/kengaku-r69/GateReceipts` (created with `mkdir -p`, used
explicitly, removed before yield; nothing from it is referenced by the report).

## Commands and return codes (item 1)

All ran with cwd = `L = /home/vgpnk/Projects/shokunin/kengaku-shokunin`, stdout captured to a
file, stderr captured to a separate file, rc captured immediately after each run.

1. `python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root .`
   → **rc 0**, stdout 104 bytes, stderr 0 bytes.
2. `python3 plans/round63_gate_checks.py trio corpus/knowledge/tb2-network-service-offline-grader.md`
   → **rc 0**, stdout 65 bytes, stderr 0 bytes.

Interpreter: `command -v python3` → `/usr/bin/python3`; `python3 -V` → `Python 3.14.8`.
E7 invokes `sys.executable`, which I confirmed is the same path `/usr/bin/python3`, so the
receipt bytes are produced by E7's exact interpreter and argv list.

Because stderr was 0 bytes on every run, "stdout" and "stdout+stderr" are the same byte
sequence for these commands; the committed files are the raw stdout stream.

## Byte-equality of the re-run (item 2)

| comparison | command | rc | result |
|---|---|---|---|
| run 1 vs run 2, depth | `diff -u depth.run1.out depth.run2.out` | 0 | empty output, byte-equal |
| run 1 vs run 2, trio | `diff -u trio.run1.out trio.run2.out` | 0 | empty output, byte-equal |
| committed vs run 3, depth | `diff -u gates/depth-gate.txt depth.run3.out` | 0 | empty output, byte-equal |
| committed vs run 3, trio | `diff -u gates/trio.txt trio.run3.out` | 0 | empty output, byte-equal |

`sha256sum` over the two run-1 and run-2 captures: depth `f683297c…c9d9` twice; trio
`d877fe2f…2cb7` twice — i.e. the outputs are deterministic across three independent
invocations spanning the sibling edits made at 21:06 local (`SKILL.md` mtime 21:06:25).

## E7 observed live, through the gate itself

I ran the C2 instrument read-only at the working tree (no `--selftest`, no writes; E1–E7 are
pure reads plus `git show`/subprocess argv):

```
python3 -B plans/round69_c2_routed_defects.py            → rc 0
E1 ok rows=4/4 missing=[] thin=[]
E2 ok headings=1 q50=True round68-lesson=True spotcheck=True
E3 ok inputs=6 differs=['SKILL.md'] problems=[]
E4 ok verified-at-lines=2 last-names-landing=True
E5 ok strict-lines=1
E6 ok rerecord-lines=1
E7 ok problems=[]
DEFECTS n=0
PREDICATE R69-C2 pass
```

E7's verdict is the byte comparison `fresh == DEPTH_RECEIPT` and `fresh == TRIO_RECEIPT`
with `run_command(root, argv)` (`subprocess.run(..., cwd=root, capture_output=True, text=True)`,
returning **stdout only**). The files E7 actually reads are
`corpus/evidence/round69/gates/{depth-gate.txt,trio.txt}`; those were placed by a sibling
seat before my run and are byte-identical to my captures:

```
f683297c35998f66187475daf2f68333f62294fab9356d436cba459c02efc9d9  .ufo/waves/round-69/w1/gates/depth-gate.txt
f683297c35998f66187475daf2f68333f62294fab9356d436cba459c02efc9d9  corpus/evidence/round69/gates/depth-gate.txt
d877fe2fa696bf0cb45255fd159ef5fe92946f7d088237e282d92cd974922cb7  .ufo/waves/round-69/w1/gates/trio.txt
d877fe2fa696bf0cb45255fd159ef5fe92946f7d088237e282d92cd974922cb7  corpus/evidence/round69/gates/trio.txt
```

`cmp` of both pairs: identical. I did not write the corpus copies (outside this seat's write
scope); they agree with the captures, so no copy action is owed at landing unless the bound
inputs change (see below).

## E7-shape replication (independent of the CLI)

Importing the gate (`python3 -B`, `sys.path` entry `plans`) and calling
`g.run_command('.', g.DEPTH_ARGV)` / `g.run_command('.', g.TRIO_ARGV)` from `L` returned
`rc depth=0 trio=0` and bytes that `cmp` to my committed receipts with rc 0. This is E7's
comparison path exactly, not an approximation of it. Observed argv:

```
DEPTH_ARGV = ['/usr/bin/python3', 'plans/round63_gate_checks.py', 'depth', '--skill', 'SKILL.md',
              '--receipt', 'corpus/evidence/round62/class-survey.txt', '--root', '.']
TRIO_ARGV  = ['/usr/bin/python3', 'plans/round63_gate_checks.py', 'trio',
              'corpus/knowledge/tb2-network-service-offline-grader.md']
```

## Calibration controls (all run; none touched a tracked file)

Every mutation was made on a copy under `S`; the lane stayed read-only.

| # | control | observed | verdict |
|---|---|---|---|
| A | depth receipt with one `CLASS … count=` raised by 1 | `count_mismatch=1`, `DETAIL count-mismatch=signal-delivery:got=1,want=2`, `PREDICATE R63-C2 fail`, rc 1 | receipt is priced, not decorative |
| B | depth receipt with the `CLASS signal-delivery` row dropped | `class_match=False`, `DETAIL receipt-classes=15 expected=16`, `DETAIL unknown-classes=signal-delivery`, `PREDICATE R63-C2 fail`, rc 1 | roster drift is caught |
| C | knowledge copy with `source:` removed | `TRIO fail missing=source file=…/knowledge-nosource.md`, rc 1 | proven in order, not by presence |
| D | knowledge copy with `source:`/`verified-at:` order inverted | `TRIO fail missing=verified-at file=…/knowledge-swapped.md`, rc 1 | order clause is live |
| E | depth report over `S/SKILL.exec3.md` (the C1 in-flight class-row edit applied: `executed 2 of 8` → `executed 3 of 8`) | `ROWS n=16 … paths total=33 resolved=33 share=1.00`, `PREDICATE R63-C2 pass`, rc 0 | C1's pending edit cannot invalidate the E7 receipt |
| F | depth report over a copy whose decision-table pointer token was made unresolvable (`corpus/does-not-exist-xyz.py`) | `paths total=34 resolved=33 share=0.97`, `DETAIL unresolved=corpus/does-not-exist-xyz.py`, `PREDICATE R63-C2 fail`, rc 1 | the section's path clause is live |
| G | `git show b288e8e0:SKILL.md` / `a518980e:SKILL.md` (identical bytes, sha256 `544ad8…83c5`) fed to depth with `--root .` | same `ROWS`/`PREDICATE` lines, rc 0 | E7's receipt is invariant across the freeze base and the round-68 tip; the working-tree delta is the four registry rows outside the priced section |
| H | `python3 -B plans/round69_c2_routed_defects.py --selftest --work S/selftest-work` | `SELFTEST defects-in-fake=7 want=7 all-fail=True`, `SELFTEST e7-stale-red=True rc=1`, selftest rc 0 | the gate's red arm and E7's stale-receipt arm both fire |

Control E is the coupling check: the depth receipt reads only the `## Decision table — grader
class → offline replay recipe` section, so neither C1's `executed 2 of 8` → `3 of 8` class row
nor C2's four appended registry rows (control G) move its bytes. Control A/B/F cover the three
ways the priced section could drift. This is why the E7 receipts were stable across the
sibling edits made during the wave.

## Binding, and what would invalidate the receipts

Bound inputs at capture (sha256, working tree):

| input | sha256 |
|---|---|
| `SKILL.md` | `ba596071c9053f309fc33fe62be0ad8eb1c426ffb527406447989d15a0ecf998` |
| `corpus/evidence/round62/class-survey.txt` | `ee30c6984c13985fe3efaa2d81c908b915da0f178ce5ca267bc0f0a37cd45613` |
| `corpus/knowledge/tb2-network-service-offline-grader.md` | `0b49a0541eb48aa82a2f73121199194074a4ce33c730c0d7657d6187724ed218` |
| `plans/round63_gate_checks.py` | `a98d9c0f75600ea4f99573d2ca291b1ffd97cffc18a53a3a65dce7b7941dfe17` |

Regeneration, if any of the first three changes before landing (must be run from `L`, and the
corpus copy must be replaced with the same bytes):

```
python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root .
python3 plans/round63_gate_checks.py trio corpus/knowledge/tb2-network-service-offline-grader.md
```

The depth output carries no absolute paths and `--root .` is relative, so the receipt is
cwd-independent for a fixed tree byte-set; only the inputs in the table above can move it
(measured in controls A/B/F/G). The trio output echoes its file argument, so a rename of the
knowledge entry would change line 1 and require regeneration.

## Findings an attacker should use

1. **E7 compares stdout only.** `run_command` returns `run.stdout`; stderr is discarded and rc
   is used only as a gate (`rc != 0` → `problems.append(f"{rel}:rc={rc}")` before any byte
   compare). A receipt therefore cannot launder a `SETUP` failure (those exit 2 on stderr with
   empty-ish stdout), but the converse hole is real: a run that emits diagnostics on stderr
   while printing the same stdout passes E7. At capture all three runs wrote 0 bytes to stderr,
   so the committed bytes carry the full transcript.
2. **The depth receipt is labelled `PREDICATE R63-C2`, not `R69-C2`.** E7 greps no text — it
   compares bytes — so a reader who greps for `PREDICATE R69-C2` in `depth-gate.txt` will find
   nothing while E7 is legitimately green. The `R69-C2` label lives only in the gate run.
3. **The receipts are insensitive to the two in-flight edit regions** (registry rows, class-row
   count), which is why they did not go stale mid-wave; they are sensitive to any
   `class-survey.txt` count/row drift or to a decision-table pointer token that stops
   resolving. Do not "refresh" the receipt after a class-table edit without re-running.
4. **Coupling between C1 and C2:** at capture, `grep -c 'executed 2 of 8' SKILL.md` = 1 and
   `grep -c 'executed 3 of 8' SKILL.md` = 0 — C1's class-row target was not yet landed — and
   control E shows landing it will not perturb E7's depth bytes. The two claims are causally
   separable through this receipt.
5. **`TRIO pass <argv path>` echoes the argument.** E7's `KNOWLEDGE` constant and the capture
   argv must match character for character; today both are
   `corpus/knowledge/tb2-network-service-offline-grader.md`.

## Commands NOT run

- The R69-C1 nginx battery (`plans/round69_c1_nginx_probe.py`), its `--check-receipt`, its
  `--render-table`, and anything binding 127.0.0.1:8080 or the `port-8080.lock` flock: not this
  seat's item; another seat owns the battery. I saw no `SETUP port-8080-occupied` line.
- No `git`/`jj` write command of any kind (no init/add/commit/stash/checkout/switch in the lane
  or anywhere else); no fixture git repo was needed.
- No write to `corpus/`, `SKILL.md`, `QUALITY.md`, `corpus/knowledge/*`, `corpus/lessons/*`,
  `plans/*`, `MANIFEST.json`, `LOG.md`, `SCORECARD.md`, `~/.local/bin`, or any sibling lane /
  the fleet repo.
- No package install or upgrade (nothing was missing for this seat); therefore the tooling
  log is empty and no `pacman` transaction was attempted.
- No build, lint, test, or formatter run (editing-wave rule; the parent owns the gate).
- No subagent spawned (leaf seat).

## Lane cleanliness

`git -C L status --porcelain` before and after my work shows the same entries: four modified
tracked files (`SKILL.md`, `corpus/QUALITY.md`, `corpus/knowledge/tb2-network-service-offline-grader.md`,
`corpus/lessons/round-68.md`) and four untracked paths (`.ufo/waves/round-69/w1.ready`,
`…/w1.ready.dispatched`, `.ufo/waves/round-69/w1/`, `corpus/evidence/round69/`). None of the
modifications are mine; my writes are the three files listed under Deliverables.
