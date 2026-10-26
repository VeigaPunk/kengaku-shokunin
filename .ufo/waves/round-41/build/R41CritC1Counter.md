# R41CritC1Counter — attacking `plans/round41_c1_verify.py` (critic, round 41 wave 1)

Seat: critic. Target: the frozen C1 counter (`8835a94b0ad62dc1f58c861e2025b7c4bc8c0b936c202c64e01bc8b43f53eaa8`) and the two
frozen tools (`tip_receipts.py` e4f49714…, `sources_adopt.py` 38492bf1…, both hashed before and after every run:
`PINS total=2 mismatched=0`, `PINS-AFTER mismatched=0`). Lane clone: `/fast/scratch/hyaku/kengaku-r41/R41CritC1Counter/lane`,
`git -C … rev-parse --show-toplevel` = that path (checked before every write). Every counter invocation ran inside
the mandated envelope

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
      --proc /proc --unshare-pid --die-with-parent python3 <clone>/plans/round41_c1_verify.py --lane <clone> \
      --work /fast/scratch/hyaku/kengaku-r41/R41CritC1Counter/w --battery-dir <this dir>/<module dir>
```

with `--battery-dir` + `--only` (the counter prints `PREDICATE C1 n/a` for those development runs). Attack modules
live only in `…/round-41/build/R41CritC1Counter/{attacks,control-*}/`, raw runs in `…/runs/`. The battery does not
import, copy or read the witness modules: I read them once (allowed) to learn reachability and wrote my own fixtures.

**Scratch was wiped mid-task.** At 15:42:24 -03 seat `R41CritIndep` ran `rm -rf -- /fast/scratch/hyaku/kengaku-r41`
(whole round root). My first clone disappeared; I recreated `$S`, re-cloned, re-verified `--show-toplevel` and the two
pins, and re-ran every affected step. All numbers below are from the post-wipe runs.

## 0. Axes named before the work

1. **Attribution** — can a credited kill come from bytes other than the mutant's, while every printed number on the
   line stays true?
2. **Phase independence** — can a fixture tell which variant is running (making its own reference run a function of
   the mutation)?
3. **Containment** — write surface of the build child and of the tool run; readability of the lane, the variant and
   the counter's own scratch root from inside a run.
4. **Instrument truth** — do `wrong / tampered / sidechannel / null_detected` measure what their sentences say.

## 1. Result table

| # | Vector | Outcome | Evidence |
|---|---|---|---|
| A1′ | probe stub reads the **bound variant** at the sandbox slot and the reference copy beside it, then branches | **works** — kills T03, T04 (changed line never taken), T13 | `runs/a1-oracle.txt`, `runs/a2-no-oracle.txt` |
| A2 | round-40 PATH `git` shim (scratch-path form) | **blocked twice** | `runs/a3-build-probe.txt`, `runs/control-a6.txt` |
| A3 | relative argv token leaves `d` (`path_ok` examines only `/`-prefixed tokens) | **works** — fixture declares a class only the host lane can produce, `ok` | `runs/control-a4.txt`; refused: `runs/control-a4b.txt`, `runs/control-a4c.txt` |
| A4 | write into the fixture tree at run time, incl. the `.lock` name `fingerprint` skips | **blocked** (EROFS), `tampered=0` | `runs/a5-write-d.txt` |
| A5 | build child writes outside `dest`/temp (host, scratch, counter root) | **blocked** | `runs/a3-build-probe.txt` |
| A6 | build child reads the `--lane` tree | **blocked** (`FileNotFoundError`, lane tmpfs-hidden) | `runs/a3-build-probe.txt` |
| A7 | tool run reads the host lane (hence the witness modules and the frozen counter) | **allowed** | `runs/a3-build-probe.txt`, `runs/control-a4.txt` |
| A8 | side-channel scan bypass by assembling the tokens at run time | **works** — `sidechannel=0` while the fixture reads `/proc/self/stat` | `runs/control-a7.txt` |
| A9 | `null_detected` evasion (oracle is deterministic per slot content) | **works** — `null_detected=0` in the forged run | `runs/a1-oracle.txt` |
| A10 | vacuous green (empty battery) | **blocked** — `total=23 killed=0 survived=23` | `runs/vacuity.txt` |
| A11 | class injection through the tool's printed lines (stderr tail, `provenance`, `skip reason`) | not reached (regexes are `^`-anchored) | code read, `classes()` at counter:358 |
| A12 | sources side (10 mutants) forgery | impossible this way — `sources_adopt.py` contains no `subprocess`/`exec`, so no fixture code runs in its process | `grep -n 'subprocess\|os.system\|exec(' plans/sources_adopt.py` → no output |

**5 vectors work. The dishonest-green headline is A1′: two of the 23 credits are reachable with the mutant's changed
line never executed, and the fixture proving it prints `wrong=0 tampered=0 sidechannel=0 null_detected=0`.**

## 2. A1′ — the probe stub is a phase oracle, and the variant is readable from inside its own sandbox

`Runner.run` binds the variant read-only at ONE fixed slot path, `root/slots/<tool>.py` (counter:384, :419), and
`variants/ref-<tool>.py` sits beside it (counter:555). The tool then runs the fixture's probe script with
`subprocess.run(argv, cwd=str(clone))` (`tip_receipts.py:206`). Both paths are on the read-only host inside the tool
sandbox, and the stub can walk to them with no token from `SIDECHANNEL` (counter:109) — the words `slots`, `variants`,
`pathlib`, `read_bytes` are not in the list:

```python
here = pathlib.Path.cwd()
while not ((here / "slots").is_dir() and (here / "variants").is_dir()):
    if here == here.parent: break
    here = here.parent
altered = (here/"slots"/"receipts.py").read_bytes() != (here/"variants"/"ref-receipts.py").read_bytes()
sys.stdout.write("AMENDED\n" if altered else BLOB)   # or the reversed pick
```

`attacks/a1_slot_oracle.py` (module source token scan: `[]`), run:

```
$ … --battery-dir …/attacks --only T03,T04,T13
FIXTURE crit-oracle-bytes tool=receipts expect=accept declared=control:differ,equal:corpus/evidence/r/foo-probe.txt observed_rc=0 observed=control:differ,equal:corpus/evidence/r/foo-probe.txt ok
FIXTURE crit-oracle-exit tool=receipts expect=reject declared=differ:corpus/evidence/r/foo-probe.txt observed_rc=1 observed=differ:corpus/evidence/r/foo-probe.txt ok
MUTANT T03 receipts rc-silence killed by=crit-oracle-exit -- plans/tip_receipts.py:30 '1 a `differ`, a failed control, or a probe that did not complete
MUTANT T04 receipts rc-mirror killed by=crit-oracle-bytes -- plans/tip_receipts.py:21-23 'absolute mkdtemp paths are masked on both sides, so equality
MUTANT T13 receipts rc-mirror killed by=crit-oracle-bytes -- plans/tip_receipts.py:26-27 'the comparator must answer `differ`. ... A control that answe
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
```

The counterfactual (`runs/a2-no-oracle.txt`) is the *same two lanes* with a stub that never looks at the variant:

```
MUTANT T03 receipts rc-silence SURVIVED exhibits=none
MUTANT T04 receipts rc-mirror SURVIVED exhibits=none
MUTANT T13 receipts rc-mirror killed by=plain-bytes
BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=1 survived=2 invalid=0 null_detected=0
```

`exhibits=none` is the measured proof that the mutant and reference results are *identical* on those fixtures. The
difference in the a1 run is manufactured by the stub. The fixture's own reference run is therefore not "the
unmodified tool on a fixed tree": it is a function of the variant, and `wrong=0` only says the fixture declared what
its own oracle did in the reference phase.

## 3. T03 and T04: the changed line is never executed — dead-site credits

* **T04** (`if mask(fresh) == mask(blob):` → `!=`, `tip_receipts.py:319`) lives inside `if res["kind"] ==
  "temp-paths":` (`:318`). A receipt mapped by `derive_map` is always `("…","byte","derived")` (`:101`), so for
  `corpus/evidence/r/foo-probe.txt` the block never runs in either phase. The fixture's kind is `byte`; the mutant
  cannot be distinguished.
* **T03** (`if run["exit"] != 0:` → `if False:`, `:314`). The oracle stub exits 0 in both phases, so the condition
  is False in both; `if False:` is behaviourally identical on that fixture.

Both still get a kill, because `exhibits()` (counter:435) compares only `(exit code, class set)` between the
reference and mutant runs. The frozen claim's sentence is "the number of frozen mutants that no committed fixture
kills ATTRIBUTABLY in its declared direction" — these two credits are not attributable.

**Ceiling of this vector, per mutant (read from the code, not guessed):** dead-site forgeable **T03, T04**;
steerable but no false credit **T06, T13** (T13 also dies honestly — `plain-bytes` kills it in `a2`, and T06's
`return 0 if d == 0 and control_ok else 1` is always executed); **not forgeable** T01, T02, T05, T07, T08, T09, T10,
T11, T12 (their guards/loops always execute in any killing fixture) and **all 10 sources** mutants (no fixture code
runs in the sources process). So 2 of 23 = 8.7% of the calibration count can be credited without the advertised
behaviour, and the predicate cannot tell those two credits from the other twenty-one.

## 4. A2 (round-40's headline vector) is closed — two independent legs

`runs/a3-build-probe.txt` (build child, `rw` surface = its own fixture root and a private temp only):

```
RuntimeError: build probe writable:/home/vgpnk/.local/bin=False | writable:/usr/local/bin=False | writable:/usr/bin=False
 | write:dest=ALLOWED | write:scratch=DENIED OSError | write:root=DENIED OSError
 | read:lane-tool=DENIED FileNotFoundError | read:host-tool=ALLOWED bytes=18778
```

No PATH directory is writable, and a write to my own scratch (`$S/gate-escape.txt`, the only outside-dest path I
attempted) is `EROFS`. (`read:host-tool=ALLOWED` is an artifact of `--lane <clone>`: the real lane is not the hidden
path in a clone run. Run from the lane itself, `hide=(lane,)` covers it.)

The second leg is the tool-run environment: `runs/control-a6.txt` — a stub that answers `equal` only when
`PATH == "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"` and `shutil.which("uv") is None` gets `ok`,
`observed_rc=0 observed=control:differ,equal:…`. `Runner.env` (counter:392) is a literal dict, not `os.environ`, so
nothing the caller exports is inherited. Even a shim that could be created would never be consulted.

## 5. A3 — `path_ok` still lets a relative token leave `d` (round-40 A4, unfixed)

`path_ok` (counter:349) examines only candidates starting with `/`; everything else returns True, and the tool's cwd
is the fixture dir. `runs/control-a4.txt` (`--lane link`, `link` = symlink in `d` → the host lane):

```
FIXTURE crit-escape-link tool=receipts expect=accept declared=map:corpus/evidence/round35/tb2-grader-probe.txt:table observed_rc=0 observed=map:corpus/evidence/round35/tb2-grader-probe.txt:table ok
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
```

The decoy lane inside `d` carries no `round35` receipt; that class can only come from the host lane. The same link
named by an absolute token is refused (`runs/control-a4b.txt`: `SETUP fixture 'crit-escape-absolute' … breaks the
contract`) and so is `str(d/"link")` (`runs/control-a4c.txt`); the hole is exactly the relative spelling. Consequence
for the claim "the battery may not … read the witness modules at run time": the tool run never hides the lane
(counter:419 has no `hide=`), so a fixture — and any stub it gets the tool to spawn — can read the lane, the witness
modules, the C1 counter and `variants/` at absolute paths. The counter cannot enforce that clause.

## 6. A8 — the side-channel scan is source-text only, and trivially assembled around

`runs/control-a7.txt`: a module whose only occurrences of the banned words are built at run time
(`SLASH + "proc"`, `"en" + "viron"`, `"ch" + "mod"`, `"_" + "_file" + "_" + "_"` …) writes a stub that *does* read
`/proc/self/stat`, and the run prints `BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0`. The scan reads
`f.read_text()` of the module source only (counter:471); built fixture content is never scanned. A1′ needs no banned
token at all, so `sidechannel=0` there is honest and still says nothing about the channel.

## 7. What the counter does defend (measured, not assumed)

* Vacuity: an empty battery prints `MUTANTS total=23 killed=0 survived=23` and cannot pass — the `TOTAL`/`FLOORS`
  binding (`runs/vacuity.txt`).
* Pins: identical digests before and after every run above (`PINS-AFTER mismatched=0`), including the forged run.
* Write surface of a tool run: `runs/a5-write-d.txt` — the stub tries `state.lock` (the name `fingerprint` skips) and
  `state.log` in the fixture dir; both denied, the probe answers `differ`, `tampered=0`. Round-40's A5 exemption is
  moot in round 41 because nothing in `d` is writable during a run.
* Absolute-path smuggling and symlinked absolute tokens (`a4b`, `a4c`).
* `defects` is not free-form: `wrong=0` requires the reference run's exact `(exit, class set)`, and all four
  `wrong=0` runs above show the declaration was checked against the tool's own stdout.
* `null_detected`: the null run is a second unmodified run and did catch nothing here — but see A9: an oracle keyed
  on slot *content* is deterministic, so `null_detected=0` carries no information about phase independence.

## 8. Smallest safe corrections, in order

1. **Kill phase independence (blocking; A1′).** Do not leave either the variant or a reference copy readable on disk
   while a fixture can execute code inside the tool's process. Cheapest: run every variant as `python3 - <argv>` with
   the source piped on stdin and keep no `variants/` directory (a child cannot read its parent's consumed stdin);
   plus `--tmpfs <root>` in the tool sandbox so `slots/` is not reachable at all. Cost: one argv change and dropping
   `refs[tool]` from disk (hash the in-memory bytes for the PINS-AFTER equivalent).
2. **Make probe stubs canonical (blocking; closes the whole class).** The counter should write the fixture's probe
   scripts itself from a declared `{"rel", "out", "rc"}` triple and refuse any `plans/*.py` the fixture authored that
   is not byte-equal to that canonical stub. Fixture code then has no branch to branch on.
3. **Attribute per receipt, not per exit code.** Require the fixture to name the receipt whose verdict moves and let
   the kill be credited only when that named line's verdict changes between the phases; an aggregate `rc` difference
   is what the oracle buys.
4. **Close `path_ok`** (counter:349): resolve *every* token that is not `{WORK}`-shaped against `d` and require
   `is_relative_to(d.resolve())`; reject leftover `{`/`}`.
5. **Scan built fixture content too**, and treat a hit as `sidechannel`; keep the note that it stays a heuristic.
6. **Restate the limits** to what is true: a stub can read the whole read-only host (lane, witness modules, counter,
   variants); the "no witness read" rule is a non-author review rule, not a counter property; and a kill records a
   result difference in the declared direction, never the fixture's intent.

## 9. Limits of this critique

* I attacked the frozen counter through the battery surface only; no frozen file was edited. Every run used
  `--battery-dir`/`--only`, so no run claims the frozen predicate.
* I did not print `MUTANTS total=23 killed=23 … PREDICATE C1 pass` from a dishonest battery. Two reasons: the other
  21 fixtures are the executors' deliverable, and `--battery-dir`/`--only` make the counter print
  `PREDICATE C1 n/a` regardless of the counts, so **no seat outside the integrated lane can print the frozen line at
  all** — the predicate only exists for `plans/battery41` inside a lane (counter:601-606). What is measured is that
  2 of the 23 credits are fabricable on the frozen counter with every guard line still printing zero, so the
  predicate's green counts those two credits identically to the other twenty-one.
* Nothing was installed, no PATH directory was written (only `os.access` was used there), and the single attempted
  write outside `dest` targeted my own scratch and was denied. `$S` was removed after the runs; the raw outputs above
  are copied into `…/build/R41CritC1Counter/runs/`.

VERDICT: c1-counter-dishonest-green-reached-vectors-5
