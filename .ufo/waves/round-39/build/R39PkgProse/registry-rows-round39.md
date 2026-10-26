### (d) `SKILL.md` §Gate/probe registry — round-39 rows

*Paste target: `SKILL.md`, three rows appended to the `## Gate/probe registry (PROTOCOL §Gate standard)` table,
after the existing `tip-receipts` row, plus one addendum paragraph after the `Round-37 registry addendum`. Names
follow the table's own convention (the round-37/38 counters are `round37-c1-mutants` / `round38-c1-mutants`,
`round38-c2`); the round-39 claims file calls the same two instruments "the C1 counter" and "the C2 counter"
(`plans/round-39-claims.md` §C1/§C2).*

```markdown
| `git-leak-probe` | probe | `python3 plans/git_leak_probe.py --lane .` (`--dry` prints the 25 frozen cases, `violates=` tags and predictions with no sandbox; `--stage-check` builds each case's repository state and prints only stage exit codes, the grader module never imported; `--work DIR` scratch parent) | `0` every case yielded five test verdicts and the summary line printed — **prediction mismatches are on the summary line, never in the exit code** (`cases=25 … mismatches=0` is a data line; the probe exits 0 either way) · `1` `--stage-check` only: a case's setup or recipe stage exited non-zero · `2` setup (a capture not at its pinned digest, `/usr/bin/bwrap` or `/usr/bin/git` not executable, a case without five verdicts, duplicate case id / unknown tag / malformed prediction; the per-case child's internal exit `3` surfaces here, never as a verdict) | `python3 plans/round39_c2_verify.py --lane .` V1 (capture manifest, 7 files) and V5 (probe at its freeze digest, `--dry` byte-equal to the frozen table) | captures `corpus/evidence/round39/tb2-git-leak-recovery/` (S117 `test_outputs.py` `dc7b01c1…`, S118 `instruction.md` `54ac693f…`, plus setup/oracle/test/Dockerfile/task.toml + `SHA256SUMS`); its own `PINS` for the three captures it executes (`test_outputs.py`, `challenge-setup.sh`, `solve.sh`); probe digest `4961a50f…` and dry table `e92a5d6d…` pinned in `plans/round39_c2_verify.py` | scratch under `--work`/`$TMPDIR`, removed on exit; per-case `/app` and `/cap` exist only inside the sandbox | kengaku |
| `round39-c1-mutants` | gate | `python3 plans/round39_c1_verify.py --lane .` (`--battery r38` the round-36+37+38 battery only — the do-nothing control; `--battery-dir DIR` and `--only M01,M02` development selectors, which print `PREDICATE C1 n/a`; `--work DIR`) | `0` predicate holds: `PINS total=26 mismatched=0`, `BATTERY fixtures=<n> wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass` · `1` any survivor (which prints `exhibits=<directions>`), invalid mutant, null detection, `wrong>0`, `renamed_disagree>0`, `sidechannel>0`, a pin mismatch, or a gate digest change during the run (`invalid(gate file changed during the run)`) · `2` setup/usage (duplicate fixture id, a fixture returning a forbidden argv — a first token other than `package`/`d4-line`/`d5-line`, or a `--spec` outside the fixture dir — a module import/build failure) | controls `.ufo/waves/round-39/claims/`: `control-c1-nothing.txt` (`BATTERY fixtures=86`, `MUTANTS total=7 killed=3 survived=4`, `PREDICATE C1 fail`, `exit=1`), `control-c1-gate-edited.txt` (`PINS mismatched=1`, `invalid=7`), `control-c1-hostile-inproc.txt` (the round-38 in-process `run_gate` patch shipped as a battery39 module: `BATTERY fixtures=88`, unchanged `killed=3 survived=4`) | 26 input digests in its `PINS` (gate `ea638822…`, round-37/36 counters, round-35 spec, round-37 attribution audit, 9 battery37 and 12 battery38 modules); frozen MUTANTS M01–M07 with `adv`/`witness` cells; directions `silence`/`mirror`/`rc-silence`/`rc-mirror` | scratch under `--work`; gate copies written only after every child process exits and digest-checked after every muted run | kengaku |
| `round39-c2` | gate | `python3 plans/round39_c2_verify.py --lane .` (`--work DIR`) | `0` `checks=7 defects=0` then `PREDICATE C2 pass` · `1` any `Vn DEFECT <note>` (a check that raises prints `error <Class>: …` and is a defect, never a pass) · `2` usage (argparse) | itself; freeze control `control-c2-nothing.txt` is `checks=7 defects=4` (V2, V3, V4, V7), `PREDICATE C2 fail`, `exit=1`, and its embedded gate dispatch prints eight `P#` defects (P2, P3, P4, P6, P7, P8, P9, P10) because the receipt, entry and index rows are absent at freeze | spec `plans/pkg-spec-r39.json` `f62163ce…`, gate `ea638822…`, probe `4961a50f…`, dry table `e92a5d6d…` and the seven captures (`CAPTURES`) pinned in the counter | scratch under `--work` | kengaku |
```

**Addendum paragraph** (paste after `Round-37 registry addendum`, as `Round-39 registry addendum:`):

```markdown
Round-39 registry addendum: `git-leak-probe` is the first entry here whose graded state lives inside git — an
object store plus refs plus one flag file — so it is also the first with a `--stage-check` mode: each case's
repository state is built and its stage exit codes printed with the grader module never imported, which is what
the round-39 freeze's order-of-operations clause needed before the first recorded run
(`plans/round-39-claims.md` §Order of operations). A stage failure is exit `1` there and exit `2` in a graded
run, never a verdict; the case child's own exit `3` never reaches the caller. `round39-c1-mutants` keeps the
round-38 out-of-process module rule (`--build-module` is an internal flag; only JSON comes back) and adds the
four-way direction vocabulary `silence`/`mirror`/`rc-silence`/`rc-mirror`, so an exit-code flip is attributable
where the DEFECT set does not change — the round-38 rule could not see one. `round39-c2` is the round-38
counter's V1–V7 re-pointed with no check added or relaxed, and its V7 derives every requirement-map label from
all receipt cases carrying a tag, so a label picked from one convenient witness fails.
```

**Row-accuracy notes for the L1 (not part of the paste):**

- Kind: `git-leak-probe` = `probe` (it produces a receipt, not a verdict over a package); the other two = `gate`.
- `--battery r38` is the *do-nothing control* selector exactly as `round38-c1-mutants`'s `--battery r37` was;
  both print `PREDICATE C1 n/a` together with the other two development selectors.
- The `round39-c2` row deliberately records a **red** freeze state (`defects=4`), matching how the
  `round38-c2` row cites `control-c2-nothing.txt` (`defects=4`); it must not be read as a green.
- Nothing in these rows claims a live host surface or a Terminal-Bench run: the probe reads committed capture
  bytes and writes only its own sandbox; the two counters read the lane tree and a scratch dir.
