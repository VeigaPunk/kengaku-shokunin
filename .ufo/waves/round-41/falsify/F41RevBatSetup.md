# F41RevBatSetup — non-author honesty review of `plans/battery41/r_setup.py` (T01, T02, T05, T07)

Date: 2026-10-26. Seat: F41RevBatSetup (leaf; no subagents used). Lane: kengaku-shokunin.
Receipts: `.ufo/waves/round-41/falsify/F41RevBatSetup/` — `attr-T01-T02-T05-T07.txt` (attribution run),
`trace-run.txt` (instrumented ref/mutant runs), `driver.py` (the driver that produced it).

Method: read all 118 lines of `plans/battery41/r_setup.py` including both probe-stub string literals;
attribution run of the frozen counter with a battery dir holding ONLY this module; per-fixture
mutated-line-execution proof by running instrumented reference and instrumented mutant (one stderr trace
line inserted immediately before the changed line) on fixtures rebuilt in scratch, through the counter's
own sandbox construction. All runs inside the orchestrator envelope
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>`
(plus a `--ro-bind` of the lane over itself; nesting with the counter's inner sandboxes works).

## 0. Environment facts

- `git -C <lane> rev-parse HEAD` → `d7c77895752a2a5f317fa22f2362416ada50a04b` ("round-41: wave-2 (falsify)
  spec and dispatch (34 seats)"), child of wave-1 landing `3d0058f` (visible as parent in `log --oneline -2`).
  The assignment named `3d0058f…` as tip; actual master tip is one dispatch commit further. No tool or
  battery byte differs: clone `plans/tip_receipts.py` sha256 `e4f49714…33f88f3` == counter PIN;
  `plans/sources_adopt.py` `38492bf1…f4103e0` == PIN; `battery41/r_setup.py` `a693fc51…f9a9c1d` identical
  in working tree and clone (`sha256sum`, both printed).
- Scratch `/fast/scratch/hyaku/kengaku-r41/F41RevBatSetup` used for clone/work/trace; removed at the end
  (guarded `case` check; verified gone). No writes outside the report dir and scratch.

## 1. Attribution — each mutant dies by THIS module (counter run)

Command (envelope abbreviated as `ENV` above; full line in the receipt):

```
ENV python3 <lane>/plans/round41_c1_verify.py --lane "$S/lane" \
    --battery-dir "$S/battery-r_setup" --only T01,T02,T05,T07 --work "$S/w"
```

`$S/battery-r_setup` contained only a byte-identical copy of `r_setup.py`. Output (full receipt
`attr-T01-T02-T05-T07.txt`):

```
PINS total=2 mismatched=0
FIXTURE r_setup-t01-lane-absent      … expect=error declared=- observed_rc=2 observed=- ok
FIXTURE r_setup-t01-not-a-repo       … observed_rc=2 ok          (all 8 fixtures: ok)
… (t02-no-evidence, t02-evidence-is-file, t05-tamper-absent, t05-tamper-unmapped,
   t07-lane-subdir, t07-nested-lane — all observed_rc=2, observed=-, ok)
MUTANT T01 receipts error killed by=r_setup-t01-lane-absent
MUTANT T02 receipts error killed by=r_setup-t02-no-evidence
MUTANT T05 receipts error killed by=r_setup-t05-tamper-absent
MUTANT T07 receipts error killed by=r_setup-t07-lane-subdir
BATTERY fixtures=8 wrong=0 tampered=0 sidechannel=0
MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=4/4 sources=0/0
ADVERTISED direct=4 indirect=0 none=0
PINS-AFTER mismatched=0
```

Each mutant is credited to a fixture this module's own header comment names for it; witness modules were
absent from the battery dir, so the kills cannot lean on them. No tamper, no sidechannel token, no
null-flakiness.

## 2. The mutated line executes on the killing fixture (non-vacuity)

Driver (receipt `driver.py`, output `trace-run.txt`): rebuilds each fixture with the counter's own `Ctx`,
inserts `sys.stderr.write("TRACE <id> …-site reached\n")` immediately before the original line
(reference) or the mutated line (mutant `old→new` taken from the frozen MUTANTS table), and runs both
through the counter's exact `ro_sandbox` + `Runner.env` + `{WORK}` expansion. Results:

| fixture | mutant | ref rc / trace / refusal | mut rc / trace / mechanism |
|---|---|---|---|
| r_setup-t01-lane-absent | T01 | 2, reached, `SETUP: … is not a directory` | 0, reached, die→exit 0 |
| r_setup-t01-not-a-repo | T01 | 2, reached, `SETUP: git rev-parse --show-toplevel failed: … not a git repository` | 0, reached, die→exit 0 |
| r_setup-t02-no-evidence | T02 | 2, reached, `SETUP: … has no corpus/evidence directory: not a kengaku lane?` | 0, reached, check→`if False`, `--list` exits 0 |
| r_setup-t02-evidence-is-file | T02 | 2, reached, same no-evidence message | 0, reached, same mechanism |
| r_setup-t05-tamper-absent | T05 | 2, reached, `SETUP: --tamper corpus/evidence/nope.txt is not a mapped receipt` | 1, reached, `results[tamper_id]` KeyError |
| r_setup-t05-tamper-unmapped | T05 | 2, reached, `SETUP: --tamper corpus/evidence/r/bar-probe.log is not a mapped receipt` | 1, reached, same KeyError |
| r_setup-t07-lane-subdir | T07 | 2, reached, `SETUP: … is not a git work-tree root (rev-parse says …/repo)` | 0, reached, prints `map:…:derived`, exit 0 |
| r_setup-t07-nested-lane | T07 | 2, reached, same work-tree-root message | 0, reached, prints `map:…:derived`, exit 0 |

4/4 mutated lines execute on their killing fixtures; the original line's refusal is what the reference
shows (rc 2), and flipping it changes the outcome exactly in the declared `error` direction (mut rc ∈ {0,1}).

## 3. Per-fixture honesty (vector audit + comment-vs-behaviour)

Wave-1 vectors checked against every fixture: counter scratch root / `variants/` / slot file reads;
`/proc`; relative `../` argv tokens; sockets; SysV IPC; reading tool or counter program text; probe stub
branching on anything but its own committed bytes.

Static audit of the 118 lines: the module imports nothing, opens nothing, reads nothing — its only
actions are `ctx.write`, `ctx.init`, `ctx.git`, and returning argv lists of paths built from the fixture
dir `d` (which the counter's `Ctx._inside` and `path_ok` confine). Grep for
`import|open(|read|proc|socket|environ|ppid|cmdline|witness|variant|slot|sys.path|__file__|..` hits only
docstring prose and the `PROBE` stub string (its own `import sys`). No fixture uses any wave-1 vector.

The one probe stub string (`r_setup.py:19-20`) is static: a docstring `Run as:` line plus
`import sys` / `sys.stdout.write("X\n")` — it branches on nothing, and in this module's fixtures the
`--list` fixtures never execute probes at all; on the t05 fixtures the reference dies before printing any
receipt line.

| fixture | advertised branch (comment) | demonstrated? | verdict |
|---|---|---|---|
| r_setup-t01-lane-absent | `--lane` names a path that does not exist → exit 2 | yes: `is not a directory` refusal, rc 2, no receipt/control lines (declared `defects=[]` matches `observed=-`) | honest |
| r_setup-t01-not-a-repo | "no work tree answers git" → exit 2 | yes: rev-parse fails (`not a git repository`), same `die()` exit-2 site. The printed reason is the absent-git branch of the docstring's exit-2 list rather than the work-tree-root sentence; same mutant site, same direction | honest |
| r_setup-t02-no-evidence | lane-shaped root with no `corpus/evidence` → exit 2 | yes: exact `has no corpus/evidence directory` refusal; with T02 flipped the tool classifies and exits 0 | honest |
| r_setup-t02-evidence-is-file | `corpus/evidence` is a regular file → exit 2 | yes: `is_dir()` false → same refusal; second trigger of the same branch as advertised | honest |
| r_setup-t05-tamper-absent | `--tamper` names a nonexistent receipt → exit 2 | yes: `is not a mapped receipt` refusal; mutant then crashes rc 1 (KeyError) — valid `error` direction | honest |
| r_setup-t05-tamper-unmapped | committed candidate the mapping leaves unmapped → exit 2 | yes: same refusal for a mapped-stem-mismatch receipt (`bar-probe.log` vs `foo_probe`); mutant rc 1 | honest |
| r_setup-t07-lane-subdir | `--lane` is a subdirectory of the work tree → exit 2 | yes: `is not a git work-tree root (rev-parse says …/repo)`; mutant classifies the subdir and exits 0 | honest |
| r_setup-t07-nested-lane | lane two levels deep, both levels lane-shaped | yes: same refusal naming the outer root; mutant classifies `nested/deeper` and exits 0 | honest |

Second shapes are genuinely distinct triggers (file-vs-absent for T02; unmapped-candidate-vs-absent-id for
T05; two-levels-deep-vs-one for T07; not-a-repo-vs-absent for T01), not reruns of the first shape.

**Verdict per fixture: honest — 8/8. No fixture reaches its verdict by any wave-1 counterexample vector;
no probe stub branches on anything (there is nothing to branch on); no fixture reads tool text, counter
text, scratch state, `/proc`, sockets, or IPC; no `../` argv token exists.**

## 4. Independence from the witness modules

`r_setup.py` shares no code with `claims/witness/w_receipts.py` / `w_sources.py`: its helpers
(`tree`, `listing`, `runner`) are its own; the witness module's `probe/lane/run` helpers are not imported
(the module imports nothing). Concepts overlap (no-evidence, subdir, tamper-unknown exist in both) but the
battery's builders differ in shape (evidence-as-file, nested-lane, tamper-unmapped, not-a-repo have no
witness counterpart). The counter never reads the witness directory — `WR` appears only inside MUTANTS
label strings — and §1 shows all four kills reproduce with a battery dir that contains only `r_setup.py`.
Independent: yes.

## 5. Observations (non-defects, recorded for calibration)

1. T01's mutated line is the single `die()` exit site (`raise SystemExit(2)`), so every one of the 8
   fixtures kills T01; the counter credits the first. Each fixture still demonstrates its own named
   refusal branch on the reference — no weakness, but T01's kill is the least shape-specific of the four.
2. `r_setup-t01-not-a-repo` advertises the is-a-work-tree check, but the trigger is the absent-repo git
   failure (a different `die()` call site feeding the same `raise SystemExit(2)` line). Same mutant, same
   direction, comment wording slightly broader than the message observed.
3. Under T05, the mutated run's rc 1 comes from an uncaught `KeyError` on the tamper id, not from a clean
   alternate path. `direction=error` accepts mut rc ∈ {0,1}, so the kill is valid; the fixture itself is
   honest because the reference run shows exactly the advertised refusal.

## 6. Residual risk / verification gaps

- I verified r_setup in isolation and its four claimed mutants. The other three battery modules
  (r_run, r_ctl, r_map, s_*) and the remaining 19 mutants are other seats' scope.
- The trace experiment rebuilds fixtures with the counter's own `Ctx` outside the counter's build-child
  bwrap (the tool runs themselves stay inner-bwrap'd); fixture bytes were not re-fingerprinted against the
  counter-built ones — the identical rc/class signatures (§1 vs §2) are the consistency evidence.
- Lane tip is `d7c7789` (wave-2 dispatch), not the `3d0058f` named in the assignment; both contain
  byte-identical pinned tools and battery module, so no finding depends on this.

VERDICT: battery41-r_setup-honest-8/8-mutated-line-executed-4/4
