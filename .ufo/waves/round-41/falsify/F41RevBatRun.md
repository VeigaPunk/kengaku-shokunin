# F41RevBatRun — non-author honesty review of `plans/battery41/r_run.py` (kills claimed: T03, T04, T13)

Seat: reviewer, kengaku round 41 wave 2 (falsify), 2026-10-26. Target bytes (sha256, canonical lane = clone):
`plans/battery41/r_run.py` `1ccb08aa…`, `plans/round41_c1_verify.py` `8835a94b…` (= frozen-digests), `plans/tip_receipts.py`
`e4f49714…` (= frozen-digests). Clone HEAD `d7c7789` ("round-41: wave-2 (falsify) spec and dispatch") is a descendant of the
goal tip `3d0058fb`; `git diff --stat 3d0058fb..HEAD` over the three files is empty. Every counter/battery/fixture run below
executed inside the mandated envelope `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs
/run/user/1000 --proc /proc --unshare-pid --die-with-parent`; scratch `/fast/scratch/hyaku/kengaku-r41/F41RevBatRun`
(toplevel check passed, `git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane`; deleted after receipts were copied). No
`lsp` device exists in this seat's tool inventory, so semantic checks are text-level plus runtime; nothing installed.

Receipts (this dir): `attrib-r-run-only-T03-T04-T13.txt` (counter run), `line-exec-traces.txt` (instrumented ref/mutant
pairs), `fixture-inventories.txt` (committed files of each rebuilt fixture lane). Driver: scratch `driver.py` (not copied;
mechanism described in §3).

## 1. What the module is

`r_run.py` (123 lines) declares 4 fixtures, all `tool=receipts`, and claims in its docstring to kill T03, T04 and T13. It
contains exactly three helpers and four builders; I read every line including every string it writes into fixtures:

- `probe(name, out, rc, body)` (r_run.py:17-24) — the only code the fixtures commit under `plans/*.py`. Its emitted stub is
  `"""Fixture probe.\n\n  python3 plans/<name>.py --lane .\n"""\nimport sys\n` + (`body` or `sys.stdout.write(<fixed>)`) +
  `sys.exit(<rc>)`. **The stub is an unconditional writer: it imports only `sys` (fixture 3 additionally `tempfile`), reads
  nothing, branches on nothing** — it cannot key on phase, slot content, `variants/`, `/proc`, env, cwd or anything else.
- `lane(ctx, d, files, sub="lane")` (r_run.py:27-41) — builds the tree with `ctx.init/ctx.write/ctx.git` only, one commit.
- `argv(root)` (r_run.py:44-45) — `["--lane", str(root), "--work", "{WORK}"]`: the lane path is **absolute inside the
  fixture dir** (`root = d/"lane"`), no `..`, no relative tokens, so the wave-1 F4/A3 relative-argv escape is not exercised.
- Module source carries no SIDECHANNEL token and no runtime-assembled token either (no `open(`/`read_text`/`read_bytes`/
  `environ`/`socket`/`__file__`/`importlib`/`inspect`/`sys.path`/`chmod`/`fork` anywhere — grep receipt in §1 of my notes;
  the only grep hit for `slots` is the receipt *content* string `"slot audit probe\nslots=5\n…"` at r_run.py:95, data not
  code). The counter's own scan agrees: `sidechannel=0` (attrib receipt).

## 2. Per-fixture vector audit (Q1)

Fixture lanes contain only the files the builder names (inventories receipt: docs + receipts + probes, nothing else
executable — the tool executes only the fixture's committed `plans/*.py`).

### 2.1 `r_run-t03-rc-nonzero-mixed` (expect=reject; credited kill of T03)
Builds two receipts + two probes: `census_probe.py` prints its receipt bytes, exit 0; `rc_ledger_probe.py` prints its
receipt bytes, **exit 7**. Comment (r_run.py:48-50): "a mapped probe that prints its receipt bytes and exits non-zero is a
`differ` (exit 1) even though a second, clean receipt still supplies the automatic tamper control." Reference run confirms
exactly that: `receipt …/rc-ledger-probe.txt differ probe exit=7` + `equal` on census + `control … verdict=differ` on
census, rc=1 (line-exec-traces.txt). Under T03 (`if run["exit"] != 0:` → `if False:`, tip_receipts.py:314) the same
exit-7 probe is byte-compared instead → `equal bytes=39`, `d=0`, control on census still passes → rc=0. The advertised
sentence (tip_receipts.py:30, "1 a `differ`, … or a probe that did not complete (exit != 0)") is demonstrated, and the
mutated line decides the flip (§3). **No vector used. Honest.**

### 2.2 `r_run-t03-rc-nonzero-single` (expect=reject; second T03 trigger)
One receipt, one probe printing its bytes and exiting 1. Reference: `differ probe exit=1`, no control (no equal receipt),
rc=1. Under T03: `equal`, control runs on that receipt and passes, rc=0. Demonstrates the same advertised sentence in its
purest form (the mutated branch is the only thing between red and green). **No vector used. Honest** — with one comment
nit (§6.2): the clause "a verdict of `equal` would leave the run with no control at all" is literally false of the mutant
run, which *does* print a control line (on audit-probe.txt) and passes it; it is the *reference* run that has no control.

### 2.3 `r_run-t04-temp-paths-masked` (expect=accept; credited kill of T04)
Uses the tool's only table-mapped `temp-paths` receipt, `corpus/evidence/round36/regex-log-probe-first-run.txt`
(tip_receipts.py:103), with a probe that really calls `tempfile.mkdtemp()` and a committed blob shaped like the real
round-36 receipt (`scratch=/tmp/tmp8kq2zr41`). Reference: masked equality → `skip
reason=declared-nonreproducible-absolute-scratch-paths`, rc=0. Under T04 (`==` → `!=`, tip_receipts.py:319): `differ
masked bytes differ: -`, rc=1. This is precisely the wave-1 dead-site concern inverted: the critic showed T04 creditable
on fixtures where the temp-paths block never runs (derived `byte` receipts); **this fixture enters the block in both
phases** (`TRACE … kind='temp-paths'` fires in ref and mutant). Demonstrates the advertised masking sentence
(tip_receipts.py:21-23). **No vector used. Honest.**

### 2.4 `r_run-t13-auto-control-differ` (expect=accept; credited kill of T13)
Two byte-equal receipts (28 and 35 bytes), both probes exit 0 → both `equal`; the automatic control picks the cheapest
(`min` by blob length, tip_receipts.py:341) = stable-census, flips byte 14 `0x70->0x71`, answers `differ`, rc=0. Under T13
(`control_ok = control_ok and not same` → `and same`, tip_receipts.py:355): `same=False` forces `control_ok=False` → rc=1.
Demonstrates the advertised sentence (tip_receipts.py:26-27, "the comparator must answer `differ`. … A control that
answers `equal` exits 1."). **No vector used. Honest.**

Vector summary across all four: no slot/`variants/` read (stubs read nothing at all), no `/proc`, no relative argv, no
sockets, no SysV IPC, no tool/counter program-text read, no probe branching on anything but its committed bytes. The
module never reads any file — it only writes through `ctx`.

## 3. Attribution and mutated-line execution (Q2)

Attribution command (battery dir holding only this module; envelope; `counter_rc=0`):

```
bwrap <envelope> /usr/bin/python3 "$S/lane/plans/round41_c1_verify.py" --lane "$S/lane" \
  --battery-dir "$S/bat/r_run" --only T03,T04,T13 --work "$S/w" --jobs 4
```

Output (receipt `attrib-r-run-only-T03-T04-T13.txt`): `PINS total=2 mismatched=0`; all four `FIXTURE … ok` lines with
declared == observed class sets; `MUTANT T03 … killed by=r_run-t03-rc-nonzero-mixed`; `MUTANT T04 … killed by=
r_run-t04-temp-paths-masked`; `MUTANT T13 … killed by=r_run-t13-auto-control-differ`; `BATTERY fixtures=4 wrong=0
tampered=0 sidechannel=0`; `MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0`; `PINS-AFTER mismatched=0`.
All three kills are by THIS module's fixtures. `null_detected=0` matches the unconditional stubs (deterministic).

Line-execution proof: `driver.py` rebuilt all four fixtures with the counter's own `Ctx` (same `build_module_child`
sequence), applied the frozen `old→new` bytes taken verbatim from the counter's `MUTANTS` entries (counter:138-141,
142-147, 184-187), inserted one stderr trace immediately **before** each changed line, and ran reference-with-trace and
mutant-with-trace on the same rebuilt lane through the counter's own `ro_sandbox` shape (`writable=(work,tmp)`,
`ro_binds=((variant, slot),)`, fixed PATH, `Runner.env`-equivalent). Receipt `line-exec-traces.txt`; key lines:

| mutant | fixture | ref | mutant |
|---|---|---|---|
| T03 | r_run-t03-rc-nonzero-mixed | `TRACE-T03-ref … rc-ledger-probe.txt' exit=7` → `differ probe exit=7`, rc=1 | `TRACE-T03-mut … exit=7` → `equal bytes=39`, rc=0 |
| T03 | r_run-t03-rc-nonzero-single | `TRACE-T03-ref … audit-probe.txt' exit=1` → `differ`, rc=1 | `TRACE-T03-mut … exit=1` → `equal`, rc=0 |
| T04 | r_run-t04-temp-paths-masked | `TRACE-T04-ref … kind='temp-paths'` → `skip declared-nonreproducible…`, rc=0 | `TRACE-T04-mut … kind='temp-paths'` → `differ masked bytes differ: -`, rc=1 |
| T13 | r_run-t13-auto-control-differ | `TRACE-T13-ref … same=False` → control `verdict=differ`, rc=0 | `TRACE-T13-mut … same=False` → rc=1 |

Each trace fires on the killing fixture in **both** phases, and in each pair the mutated line's *value* (not a side
effect) decides the verdict: T03's condition sees the same `exit=7`/`exit=1` and flips `differ→equal`; T04's comparison
sees the same masked-equal bytes and flips `skip→differ`; T13's `same=False` flips `control_ok True→False`. These are
live-site kills — the wave-1 dead-site credit (T03/T04 on fixtures where the changed line never runs) does not apply to
this module's credited fixtures. **mutated-line-executed 3/3.**

## 4. Witness independence (Q3)

Witness modules: `.ufo/waves/round-41/claims/witness/w_receipts.py` (12 fixtures) and `w_sources.py`. Checks:

- r_run.py contains no reference to the witness path, `.ufo/`, or `claims/`, and performs no file reads at all (§1), so no
  runtime read of witness modules is possible; the fixture lanes contain only their own files (inventories receipt).
- Code is not derived: `probe()` differs (fixed `python3` run-as + `body` parameter + "Fixture probe." docstring vs the
  witness's configurable `runas` + "Stub probe."); `lane()` adds the provenance docs the witness's `lane()` lacks; no
  shared receipt bytes (witness uses `"X\n"` / `"path /tmp/tmpAAAAAA11/x\n"`; r_run uses full-shaped receipts).
- Concept overlap is confined to what the tool forces: T04 must use the table's only `temp-paths` receipt path, and every
  receipts fixture is a receipt+probe pair. Within that constraint the constructions are distinct — the witness's T04
  probe writes a static string with two hard-coded tmp tokens, r_run's probe really calls `mkdtemp()` and its blob mirrors
  the real round-36 receipt; the T03 witnesses use exit 3 at `corpus/evidence/r/foo-probe.txt`, r_run uses exits 7 and 1
  at round42/43 paths; the T13 witness is single-receipt, r_run's is two-receipt with the cheapest-selection path.
- All four fixtures kill their mutants by themselves (each FIXTURE line `ok` with the module's own declared set; the
  credited `killed by=` fixtures are this module's).

**Independent: yes, all four.**

## 5. Fixture verdicts

| fixture | verdict | key evidence |
|---|---|---|
| r_run-t03-rc-nonzero-mixed | **honest** | §2.1 + §3 row 1 |
| r_run-t03-rc-nonzero-single | **honest** | §2.2 + §3 row 2 (comment nit §6.2) |
| r_run-t04-temp-paths-masked | **honest** | §2.3 + §3 row 3 |
| r_run-t13-auto-control-differ | **honest** | §2.4 + §3 row 4 |

## 6. Findings

1. **Docstring wording (cosmetic).** r_run.py:2-3 says "Frozen mutants T03, T04 and T13 of `plans/round41_c1_verify.py`" —
   they are mutants *of* `plans/tip_receipts.py` *defined in* `round41_c1_verify.py`. No behavioral impact.
2. **Fixture-2 comment clause (cosmetic, factually loose).** "a verdict of `equal` would leave the run with no control at
   all" (r_run.py:56-57): measured the opposite way — under the mutant the run *has* a control (on audit-probe.txt) and it
   passes (`control … verdict=differ`, rc=0); the reference run is the one with no control. The fixture's mechanics and its
   T03 trigger are unaffected.
3. **Counter-level residual (not chargeable to this module).** The frozen counter still cannot exclude the A1′/F1
   slot-oracle channel or runtime-assembled side-channel tokens for *other* modules; r_run passes only because its stubs
   are unconditional writers, which I verified by reading every emitted byte. Non-author review remains load-bearing, as
   the frozen claims already state.

## 7. Limits

- The instrumented runs used the counter's own `ro_sandbox`/`WORK_TOKEN`/env shape but under my driver, with fixture dirs
  at `$S/fix` instead of the counter's scratch root (path values only); verdicts and class sets match the counter's own
  FIXTURE lines, so the reproduction is faithful.
- `sidechannel=0` remains a source-text scan (A8); my audit adds the runtime reading of every emitted stub.
- Scratch `/fast/scratch/hyaku/kengaku-r41/F41RevBatRun` deleted after receipts were copied (guard-checked `rm -rf`).

Report: .ufo/waves/round-41/falsify/F41RevBatRun.md
VERDICT: battery41-r_run-honest-4/4-mutated-line-executed-3/3
