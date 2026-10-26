# R41BatRcvCtl — C1 battery41 module `r_ctl` (T06, T08)

Wave 1 executor. Lane clone only; nothing in the source lane was written, and no lane corpus/plans/ledger
file was touched. All C1 runs were wrapped in the mandated bwrap envelope.

## Axes

1. **Calibration** — do T06 and T08 die ATTRIBUTABLY in their declared directions on fixtures that are
   mine, not the witness's?
2. **Operability** — is every fixture's `defects` the exact class set the UNMODIFIED tool prints, and
   every `expect` the reference exit code, so the module can be dropped into `plans/battery41/` as-is?
3. **Reversibility** — is each mutant's kill load-bearing (does removal change the verdict)?
4. **Host safety** — no shared-PATH write, no `~/.local/bin` touch, scratch deleted.

## Deliverable

`.ufo/waves/round-41/build/R41BatRcvCtl/battery/r_ctl.py` (stdlib only; four fixtures, all `fid`s start
`r_ctl-`). **sha256 = 2fcbbcb7eb0017803b41ffb2c41a0fc5a3fd97854eda0afb3948bc44fa4aaaed**
(`sha256sum`, 4860 bytes).

No witness module is read, imported or copied: the module carries its own stub-probe text, its own lane
trees and its own receipt/script names. Where the witness used one flat `corpus/evidence/r/foo-probe.txt`
+ `plans/foo_probe.py` lane, mine use a committed lane with `README.md`/`SKILL.md`, dated
`corpus/evidence/round41|round35|round38|round36/` receipts, two-receipt plans, and one trigger
(`--tamper` on a skipped receipt) the witness never built.

### Fixtures (one behaviour each, every branch with a second trigger)

| fid | mutant / branch | shape | expect | `defects` (exact class set of the UNMODIFIED tool) |
|---|---|---|---|---|
| `r_ctl-t06-empty-equal-receipt` | T06 `return 0 if d == 0 and control_ok` | empty committed receipt reproduced by a probe printing nothing → `equal`, automatic byte-flip control has a zero-length blob → `unavailable` | reject (rc 1) | `equal:corpus/evidence/round41/r-ctl-probe.txt`, `control:unavailable` |
| `r_ctl-t06-tamper-on-skipped` | T06, second trigger | `--tamper` names a mapped receipt that was skipped (`dependency-missing`) → no fresh output → control `unavailable` | reject (rc 1) | `skip:corpus/evidence/round41/r-ctl-probe.txt:dependency-missing`, `control:unavailable` |
| `r_ctl-t08-derived-uv-absent` | T08 `elif shutil.which(argv[0]) is None` | derived registry layout: the derived receipt's `Run as:` starts `uv run`, `uv` is absent from the fixed PATH → `skip … dependency-missing`; a table-mapped receipt is `equal`, its control answers `differ` | accept (rc 0) | `skip:corpus/evidence/round41/r-ctl-probe.txt:dependency-missing`, `equal:corpus/evidence/round35/tb2-grader-probe.txt`, `control:differ` |
| `r_ctl-t08-table-uv-absent` | T08, second trigger | table registry layout: `round38/build-pmars-probe.txt` needs `uv` (skip), `round36/regex-log-probe.txt` is `equal`, control `differ` | accept (rc 0) | `skip:corpus/evidence/round38/build-pmars-probe.txt:dependency-missing`, `equal:corpus/evidence/round36/regex-log-probe.txt`, `control:differ` |

`uv` is present only at `/home/vgpnk/.local/bin/uv` (`command -v uv`), which the counter's fixed
`PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin` does not contain and the run sandbox
binds read-only — so `shutil.which("uv") is None` is a property of the harness, not of the fixture tree.

## Proof in my clone, inside the envelope

Clone: `git clone -q --shared <lane> /fast/scratch/hyaku/kengaku-r41/R41BatRcvCtl/lane`,
`git rev-parse --show-toplevel` → that path, HEAD `fc79f2a49be0221e138b3885fa0d83bc43b31a42`.

Command (verbatim; `$S=/fast/scratch/hyaku/kengaku-r41/R41BatRcvCtl`, `export TMPDIR="$S"`):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent \
  python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round41_c1_verify.py \
  --lane "$S/lane" \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-41/build/R41BatRcvCtl/battery \
  --only T06,T08 --work "$S/w"
```

Output (exit 0; retained at `build/R41BatRcvCtl/receipts/dev-only-T06-T08.txt`):

```
PINS total=2 mismatched=0
FIXTURE r_ctl-t06-empty-equal-receipt tool=receipts expect=reject declared=control:unavailable,equal:corpus/evidence/round41/r-ctl-probe.txt observed_rc=1 observed=control:unavailable,equal:corpus/evidence/round41/r-ctl-probe.txt ok
FIXTURE r_ctl-t06-tamper-on-skipped tool=receipts expect=reject declared=control:unavailable,skip:corpus/evidence/round41/r-ctl-probe.txt:dependency-missing observed_rc=1 observed=control:unavailable,skip:corpus/evidence/round41/r-ctl-probe.txt:dependency-missing ok
FIXTURE r_ctl-t08-derived-uv-absent tool=receipts expect=accept declared=control:differ,equal:corpus/evidence/round35/tb2-grader-probe.txt,skip:corpus/evidence/round41/r-ctl-probe.txt:dependency-missing observed_rc=0 observed=control:differ,equal:corpus/evidence/round35/tb2-grader-probe.txt,skip:corpus/evidence/round41/r-ctl-probe.txt:dependency-missing ok
FIXTURE r_ctl-t08-table-uv-absent tool=receipts expect=accept declared=control:differ,equal:corpus/evidence/round36/regex-log-probe.txt,skip:corpus/evidence/round38/build-pmars-probe.txt:dependency-missing observed_rc=0 observed=control:differ,equal:corpus/evidence/round36/regex-log-probe.txt,skip:corpus/evidence/round38/build-pmars-probe.txt:dependency-missing ok
MUTANT T06 receipts rc-silence killed by=r_ctl-t06-empty-equal-receipt -- plans/tip_receipts.py:29-30 '0 every mapped receipt reproduces ... and the control reports
MUTANT T08 receipts rc-mirror killed by=r_ctl-t08-derived-uv-absent -- plans/tip_receipts.py:19-21 'A mapped receipt whose script is gone, whose dependency is ab
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=2/2 sources=0/0
ADVERTISED direct=1 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Direction arithmetic, from the counter's `exhibits`: T06 (`rc-silence`) — every T06 fixture is
`expect=reject`, reference rc 1, mutant rc 0 (`d == 0 or control_ok` with `d == 0`). T08 (`rc-mirror`) —
every T08 fixture is `expect=accept`, reference rc 0, mutant rc 1 (`uv` executed → `FileNotFoundError` →
`exit=missing` → `differ`). No fixture enters the other mutant's direction (T06 fixtures are reject, T08
fixtures are accept).

## Load-bearing table (each fixture removed in turn)

Same envelope, `--battery-dir` a scratch copy of the module with a filter line appended
(`FIXTURES = [f for f in FIXTURES if f["fid"] != "<fid>"]`), `--only T06,T08`. Retained at
`build/R41BatRcvCtl/receipts/removal.txt`.

| removed | T06 | T08 |
|---|---|---|
| `r_ctl-t06-empty-equal-receipt` | still killed, **by=`r_ctl-t06-tamper-on-skipped`** | killed by `r_ctl-t08-derived-uv-absent` |
| `r_ctl-t06-tamper-on-skipped` | still killed, **by=`r_ctl-t06-empty-equal-receipt`** | killed by `r_ctl-t08-derived-uv-absent` |
| `r_ctl-t08-derived-uv-absent` | killed by `r_ctl-t06-empty-equal-receipt` | still killed, **by=`r_ctl-t08-table-uv-absent`** |
| `r_ctl-t08-table-uv-absent` | killed by `r_ctl-t06-empty-equal-receipt` | still killed, **by=`r_ctl-t08-derived-uv-absent`** |
| both `r_ctl-t06-*` | **SURVIVED `exhibits=none`** (`MUTANTS total=2 killed=1 survived=1`) | killed by `r_ctl-t08-derived-uv-absent` |
| both `r_ctl-t08-*` | killed by `r_ctl-t06-empty-equal-receipt` | **SURVIVED `exhibits=none`** (`MUTANTS total=2 killed=1 survived=1`) |

Reading: no single-fixture removal flips a mutant — each declared branch has two independent triggers, and
each trigger alone carries the kill (`killed by=` names the survivor). The kill is load-bearing at the
branch level: dropping a mutant's whole behaviour class flips it to `SURVIVED exhibits=none`. Every one of
the six partial runs reports `wrong=0 tampered=0 sidechannel=0 … null_detected=0`.

## Full default counter with the module in `plans/battery41/`

`cp` of the same file to `$S/lane/plans/battery41/r_ctl.py`, then:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent \
  python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round41_c1_verify.py --lane "$S/lane" --work "$S/w2"
```

Summary lines (exit 1 — the rest of the battery is other seats' work; retained at
`build/R41BatRcvCtl/receipts/full-default.txt`):

```
FIXTURE … (my four lines, all ok)
MUTANT T06 receipts rc-silence killed by=r_ctl-t06-empty-equal-receipt -- …
MUTANT T08 receipts rc-mirror killed by=r_ctl-t08-derived-uv-absent -- …
MUTANT T13 receipts rc-mirror killed by=r_ctl-t08-derived-uv-absent -- plans/tip_receipts.py:26-27 'the comparator must answer `differ`. ... A control that answe
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=23 killed=3 survived=20 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=3/13 sources=0/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
```

T13 is an incidental third kill: `control_ok = control_ok and same` flips an accept (rc 0) fixture whose
control answers `differ` to exit 1 — my T08 fixtures are exactly such accept fixtures. Reported, not
relied on. T10 shows `exhibits=1>0,1>2,rc-silence` on my trees but is declared `silence`, so it stays
`SURVIVED`; no fixture claims a T10 kill.

## Host safety and scope

- Every counter run (build + reference + null + mutant runs, and the six removal runs) executed under the
  mandated envelope `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs
  /run/user/1000 --proc /proc --unshare-pid --die-with-parent`; the counter then nests its own
  read-only sandboxes.
- `~/.local/bin` contents unchanged (only listed, never written); nothing was installed or upgraded
  (no tool needed); no pacman transaction; `uv` was used only as an absent-from-PATH name.
- Scratch `/fast/scratch/hyaku/kengaku-r41/R41BatRcvCtl` was created, used, and removed
  (`ls -d` → "No such file or directory") after copying receipts into this report dir. Nothing under
  `/tmp`; `TMPDIR` pointed at the scratch dir.
- Writes outside this report dir: none. Source lane untouched (clone HEAD == lane HEAD; `PINS mismatch=0`
  and `PINS-AFTER mismatched=0` show both tools byte-identical before and after). No git mutation in the
  source lane, no commit anywhere, `crit_git_shim.py` / `crit_ledger_selfread.py` untouched.
- Side-channel scan: my own scan of the module against the counter's token list prints `hits: []`; the
  counter prints `sidechannel=0`.

## Files written

- `.ufo/waves/round-41/build/R41BatRcvCtl/battery/r_ctl.py` (the module to copy into `plans/battery41/`)
- `.ufo/waves/round-41/build/R41BatRcvCtl/receipts/dev-only-T06-T08.txt`
- `.ufo/waves/round-41/build/R41BatRcvCtl/receipts/full-default.txt`
- `.ufo/waves/round-41/build/R41BatRcvCtl/receipts/removal.txt`

## Risks / limits

- A kill records an rc difference in the declared direction, not the fixture's intent: `anon` reviewer
  reading of the module stays necessary (the counter's own named limit).
- The two T06 fixtures differ in how the control becomes unusable (empty blob vs skipped-with-`--tamper`)
  but the observable is the same `control:unavailable`; a third shape would need a different tool branch.
- The redundancy is deliberate, so "remove one fixture" never flips a mutant; only removing a whole
  behaviour class does (table above). If the L1 prefers single-fixture load-bearing, delete either
  trigger per branch — each remaining fixture alone still kills.
- The module depends on `uv` staying off the fixed PATH; if the harness PATH ever gains `uv`, all four
  fixtures change (`dependency-missing` becomes a real run), which would surface as `WRONG` lines first.
- No build/lint/formatter was run: the counter is the harness and its `FIXTURE … ok` lines are the
  verification of record.

VERDICT: battery41-r_ctl-killed-2/2-wrong-0
