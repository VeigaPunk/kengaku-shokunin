# R41BatRcvRun — C1 battery41 module `r_run.py` (mutants T03, T04, T13)

Seat: executor, kengaku round 41 wave 1. Scope: one battery module for the frozen C1 counter
`plans/round41_c1_verify.py`; no lane file, no frozen artefact, no lane clone was modified.

## Files written

| Path | What |
|---|---|
| `.ufo/waves/round-41/build/R41BatRcvRun/battery/r_run.py` | the module (123 lines, stdlib only, no imports at all) |
| `.ufo/waves/round-41/build/R41BatRcvRun/receipts/dev-T03-T04-T13.txt` | exact `--only T03,T04,T13` counter output |
| `.ufo/waves/round-41/build/R41BatRcvRun/receipts/load-bearing.txt` | exact drop-one table output |
| `.ufo/waves/round-41/build/R41BatRcvRun/receipts/full-counter.txt` | exact full default-counter output |
| `.ufo/waves/round-41/build/R41BatRcvRun.md` | this report |

Module sha256 `1ccb08aaf1353160da4b0d67d75686648516a900e31f2da7e7aef1e6a91982f2` (identical in
`$S/lane/plans/battery41/r_run.py` during the full run). No installs or upgrades were needed or made;
nothing was written to a PATH directory, `/usr`, `/etc` or `$HOME`. Scratch
`/fast/scratch/hyaku/kengaku-r41/R41BatRcvRun` removed at the end (receipts copied out first).

## Behaviour — four fixtures, one behaviour each

All four build a committed lane-shaped work tree inside the empty fixture dir (`ctx.init` +
`ctx.git add/commit` as `fixture`): `README.md`, `SKILL.md`, `corpus/README.md`,
`corpus/knowledge/fixture.md`, `plans/<x>_probe.py` stubs whose docstring carries the
`python3 plans/<x>_probe.py --lane .` line, and receipts under `corpus/evidence/`. Every probe is
mapped by the derived rule (receipt stem == script stem after the tool's own folding), so no fixture
edits the `RECEIPTS` table. argv is `--lane <d>/lane --work {WORK}`; every path is inside `d` or a
`{WORK}` token.

| fid | expect | declared class set (== observed on the unmodified tool) | demonstrates | kills |
|---|---|---|---|---|
| `r_run-t03-rc-nonzero-mixed` | `reject` (rc 1) | `control:differ`, `differ:corpus/evidence/round42/rc-ledger-probe.txt`, `equal:corpus/evidence/round42/census-probe.txt` | two mapped receipts, one probe prints its receipt bytes and exits 7: it is a `differ` while the clean receipt still supplies the automatic control | T03, and incidentally T06 |
| `r_run-t03-rc-nonzero-single` | `reject` (rc 1) | `differ:corpus/evidence/round43/audit-probe.txt` | second trigger: the only mapped receipt's probe exits 1 after printing the blob, so an `equal` verdict would leave the run with no control at all | T03 |
| `r_run-t04-temp-paths-masked` | `accept` (rc 0) | `skip:corpus/evidence/round36/regex-log-probe-first-run.txt:declared-nonreproducible-absolute-scratch-paths` | the table-mapped `temp-paths` receipt whose probe really calls `tempfile.mkdtemp()` and prints it: masked equality keeps the declared-bounded skip and exit 0 | T04 |
| `r_run-t13-auto-control-differ` | `accept` (rc 0) | `control:differ`, `equal:corpus/evidence/round42/stable-census-probe.txt`, `equal:corpus/evidence/round43/slot-audit-probe.txt` | two byte-equal receipts; the automatic control on the cheapest one must answer `differ`, so the green run exits 0 with the control line present | T13 |

Mutant branches exercised (frozen `old -> new` from the counter's `MUTANTS` table):
T03 `if run["exit"] != 0:` -> `if False:` (a non-zero probe exit becomes `equal`, so `reject` turns into rc 0);
T04 `if mask(fresh) == mask(blob):` -> `!=` (the declared-bounded skip becomes `differ`, rc 0 -> 1);
T13 `control_ok = control_ok and not same` -> `and same` (a correct `differ` control turns rc 0 into rc 1).

Shape difference from the pre-freeze witnesses: the witness fixtures use a single flat
`corpus/evidence/r/foo-probe.txt` with literal `X\n` blobs and a bare `--lane`; these use
round-numbered evidence dirs, multi-line blobs, docs the tool's `provenance()` reads, real
`mkdtemp()` output, and two-receipt layouts (T03 twice, T13 with two equals). The module imports
nothing, reads no witness file, and shares no code with `claims/witness/w_receipts.py`.

## Evidence 1 — assigned subset (every FIXTURE `ok`, `wrong=0 tampered=0 sidechannel=0`)

```
PINS total=2 mismatched=0
FIXTURE r_run-t03-rc-nonzero-mixed tool=receipts expect=reject declared=control:differ,differ:corpus/evidence/round42/rc-ledger-probe.txt,equal:corpus/evidence/round42/census-probe.txt observed_rc=1 observed=control:differ,differ:corpus/evidence/round42/rc-ledger-probe.txt,equal:corpus/evidence/round42/census-probe.txt ok
FIXTURE r_run-t03-rc-nonzero-single tool=receipts expect=reject declared=differ:corpus/evidence/round43/audit-probe.txt observed_rc=1 observed=differ:corpus/evidence/round43/audit-probe.txt ok
FIXTURE r_run-t04-temp-paths-masked tool=receipts expect=accept declared=skip:corpus/evidence/round36/regex-log-probe-first-run.txt:declared-nonreproducible-absolute-scratch-paths observed_rc=0 observed=skip:corpus/evidence/round36/regex-log-probe-first-run.txt:declared-nonreproducible-absolute-scratch-paths ok
FIXTURE r_run-t13-auto-control-differ tool=receipts expect=accept declared=control:differ,equal:corpus/evidence/round42/stable-census-probe.txt,equal:corpus/evidence/round43/slot-audit-probe.txt observed_rc=0 observed=control:differ,equal:corpus/evidence/round42/stable-census-probe.txt,equal:corpus/evidence/round43/slot-audit-probe.txt ok
MUTANT T03 receipts rc-silence killed by=r_run-t03-rc-nonzero-mixed -- plans/tip_receipts.py:30 '1 a `differ`, a failed control, or a probe that did not complete
MUTANT T04 receipts rc-mirror killed by=r_run-t04-temp-paths-masked -- plans/tip_receipts.py:21-23 'absolute mkdtemp paths are masked on both sides, so equality 
MUTANT T13 receipts rc-mirror killed by=r_run-t13-auto-control-differ -- plans/tip_receipts.py:26-27 'the comparator must answer `differ`. ... A control that answe
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=3/3 sources=0/0
ADVERTISED direct=3 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
exit=0
```

Command (envelope as mandated; lane = `--shared` clone at rev `fc79f2a49be0221e138b3885fa0d83bc43b31a42`,
tool pins `e4f49714…` / `38492bf1…` verified by the counter):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent python3 \
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round41_c1_verify.py --lane "$S/lane" \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-41/build/R41BatRcvRun/battery \
  --only T03,T04,T13 --work "$S/w"
```

## Evidence 2 — load-bearing table (each fixture removed in turn)

Variants = `battery/r_run.py` with exactly one `FIXTURES` entry removed, generated in scratch.

| removed fid | mutants still killed | flips to SURVIVED |
|---|---|---|
| `r_run-t03-rc-nonzero-mixed` | T03 (by `…-single`), T04, T13 | none |
| `r_run-t03-rc-nonzero-single` | T03 (by `…-mixed`), T04, T13 | none |
| `r_run-t04-temp-paths-masked` | T03, T13 | **T04** (`exhibits=none`) |
| `r_run-t13-auto-control-differ` | T03, T04 | **T13** (`exhibits=none`) |

Raw rows in `receipts/load-bearing.txt`; e.g. `drop2` prints `MUTANT T04 receipts rc-mirror SURVIVED
exhibits=none` and `MUTANTS total=3 killed=2 survived=1`. T03 is redundantly covered by its two
fixtures; T04 and T13 each have exactly one load-bearing fixture.

## Evidence 3 — full default counter with the module in `plans/battery41/`

```
MUTANT T03 receipts rc-silence killed by=r_run-t03-rc-nonzero-mixed -- plans/tip_receipts.py:30 '1 a `differ`, a failed control, or a probe that did not complete
MUTANT T04 receipts rc-mirror killed by=r_run-t04-temp-paths-masked -- plans/tip_receipts.py:21-23 'absolute mkdtemp paths are masked on both sides, so equality 
MUTANT T06 receipts rc-silence killed by=r_run-t03-rc-nonzero-mixed -- plans/tip_receipts.py:29-30 '0 every mapped receipt reproduces ... and the control reports
MUTANT T13 receipts rc-mirror killed by=r_run-t13-auto-control-differ -- plans/tip_receipts.py:26-27 'the comparator must answer `differ`. ... A control that answe
BATTERY fixtures=4 wrong=0 tampered=0 sidechannel=0
MUTANTS total=23 killed=4 survived=19 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=4/13 sources=0/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
exit=1
```

Remaining survivors are the other seats' mutants (T01/T02/T05/T07-T12, S01-S09/S11), expected for a
wave-1 module. `PREDICATE C1 fail` is the correct state with only this module in the battery.
T06 (`d == 0 and control_ok` -> `or`) is killed incidentally by `r_run-t03-rc-nonzero-mixed`
(reference rc 1, mutant rc 0 — the mixed fixture's `differ` plus a green control); it is not claimed
here and needs no fixture of its own for this seat, though the T06 owner should know it is already
covered. T10 now reports `exhibits=1>0,rc-silence` — a real difference on my fixtures, not a kill in
its declared `silence` class.

## Risks and limits

- A kill records a result difference in the declared direction, not the fixture's intent (freeze
  limit); `defects` equality is enforced by the counter's `FIXTURE … ok` line, not by my reading.
- `r_run-t04-temp-paths-masked` must use the fixed table key
  `corpus/evidence/round36/regex-log-probe-first-run.txt` (the tool's `RECEIPTS` table names it), so
  that receipt path is not a free choice; the probe's real `mkdtemp()` path is masked by the tool's
  own `MASK_RE` on both sides, which is what the fixture asserts.
- Two fixtures (T03, T13) rely on the tool's automatic control selection (cheapest byte-equal
  receipt); both layouts put the control on a genuinely equal receipt, so a change of selection rule
  would be visible as a `wrong` fixture, not a silent pass.
- The side-channel scan is a token heuristic; I also grepped the module against the counter's
  `SIDECHANNEL` tuple (0 hits) and it contains no imports at all.
- Full C1 still needs the other wave-1 modules and the sources floors (10/10); nothing here can
  reach `PREDICATE C1 pass` alone.

## Blockers

None. No frozen file was touched (`PINS mismatched=0`, `PINS-AFTER mismatched=0`; `git status
--porcelain -- plans/` in the lane is empty); no git/jj mutation in the lane; no subagents.

VERDICT: battery41-r_run-killed-3/3-wrong-0
