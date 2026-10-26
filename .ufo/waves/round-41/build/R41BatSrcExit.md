# R41BatSrcExit — battery41 `s_exit`: sources_adopt CLI exit pairs for S07 and S11

Seat: executor, round 41 wave 1. Deliverable: `battery/s_exit.py` (sha256
`5f57cec90bc347963fd7a011b158d7d2991d1b7ef69dbde90187600f0c390a64`, 5 205 B). Nothing frozen was
touched; no lane file was edited; no subagent, background job or orchestration runtime was used.

## Axes

1. **Calibration** — two frozen survivors (S07 `3>0`, S11 `5>0`) killed attributably by fixtures whose
   reference exits and class sets match the declaration exactly.
2. **Operability** — six self-building fixtures, one behaviour each, stdlib only, no lane clone, no
   witness import; the module is drop-in for `plans/battery41/`.
3. **Host safety** — every build and tool run inside the mandated bwrap envelope; nothing written to a
   PATH directory, `$HOME`, `/usr`, `/etc`, the lane, or the fleet root.

## Mutant branches the fixtures open

| mutant | tool | direction | branch (frozen `old -> new`) | frozen `adv` |
|---|---|---|---|---|
| S07 | sources | `3>0` | `plans/sources_adopt.py:1046` `    if code != EXIT_OK or not want:` → `    if code != EXIT_OK and not want:` — `check()`'s refusal is skipped whenever `--admit-ids` was given, so the run falls through to `build_block` and exits 0 | `SKILL.md:573` '`3` staged/registry id collision' |
| S11 | sources | `5>0` | `plans/sources_adopt.py:1068` `    if missing:` → `    if False:` — `main()`'s post-`build_block` refusal (the `build_block` return at `:156` carries `not-mined` / `not-opened-this-round`) is skipped, so the run writes a block and exits 0 | `SKILL.md:573` '`5` requested id absent' (`indirect`) |

The pairing is exactly the two frozen lines: S07 must trip on the `check()` exit being non-zero, S11 on
`build_block`'s `missing` list. A fixture that both mutants traverse identically cannot kill either, which
is why the two boundary fixtures below are recorded as contrasts, not as kills.

## Fixtures (one behaviour each; `defects` is `[]` for the sources tool by contract)

Every fixture builds a lane-shaped tree from nothing inside its own directory: `corpus/SOURCES.md`
(multi-row registry), `corpus/knowledge/tb2-constraints-scheduling-grader.md` (entry the `used-by` cell
cites), `.ufo/waves/round-41/SOURCES.append.md` (adoption package). argv paths are relative to that
directory (the counter runs the tool with `cwd=<fixture dir>`), so no absolute path escapes `d`.

| fid | behaviour demonstrated | mutant | expect | reference exit | mutant exit |
|---|---|---|---|---|---|
| `s_exit-collision-admit` | staged row re-uses live id `S122` while `--admit-ids S122` names it; the row is `mined` and opened on the access date, so a mutated run appends it | S07 | exit-3 | 3 | 0 |
| `s_exit-collision-indented` | same branch, different shape: the duplicate `S131` is pasted **2 spaces indented** under a bullet (the census anchor accepts 0-3 leading spaces) beside a clean new row `S140` | S07 | exit-3 | 3 | 0 |
| `s_exit-queued-admit` | requested row `S150` is `queued` — a legal staged status, so `check()` passes and `build_block` refuses `not-mined` | S11 | exit-5 | 5 | 0 |
| `s_exit-opened-elsewhere` | requested row `S160` is `mined` but opened 2026-09-30 (access date 2026-10-26) and not attested → `not-opened-this-round` (the second `main()` refusal) | S11 | exit-5 | 5 | 0 |
| `s_exit-attest-opened` | boundary of that branch: the same stale `opened` cell with `--attest-opened` is re-dated and appended | — | accept | 0 | 0 |
| `s_exit-absent-id` | boundary not claimed here: an id absent from the package refuses inside `check()` (exit 5) before either mutated line — the round-41 S10 withdrawal, recorded not relabelled | — | exit-5 | 5 | 5 |

All six fixture shapes differ from the pre-freeze witness `claims/witness/w_sources.py` (its `reg.md` /
`pkg.md` flat pair, id `S900`, dates 2026-10-25, no indented row, no `--attest-opened`, no absent-id
contrast); the module neither imports, copies nor reads that witness at run time — its builders are
written here and share no helper with it.

## Proof run (targeted), exact command and output

```
S=/fast/scratch/hyaku/kengaku-r41/R41BatSrcExit; export TMPDIR="$S/tmp"
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent /usr/bin/python3 \
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round41_c1_verify.py \
  --lane "$S/lane" --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-41/build/R41BatSrcExit/battery \
  --only S07,S11 --work "$S/w"
```

```
PINS total=2 mismatched=0
FIXTURE s_exit-collision-admit tool=sources expect=exit-3 declared=- observed_rc=3 observed=- ok
FIXTURE s_exit-collision-indented tool=sources expect=exit-3 declared=- observed_rc=3 observed=- ok
FIXTURE s_exit-queued-admit tool=sources expect=exit-5 declared=- observed_rc=5 observed=- ok
FIXTURE s_exit-opened-elsewhere tool=sources expect=exit-5 declared=- observed_rc=5 observed=- ok
FIXTURE s_exit-attest-opened tool=sources expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE s_exit-absent-id tool=sources expect=exit-5 declared=- observed_rc=5 observed=- ok
MUTANT S07 sources 3>0 killed by=s_exit-collision-admit -- SKILL.md:573 '`3` staged/registry id collision'
MUTANT S11 sources 5>0 killed by=s_exit-queued-admit -- SKILL.md:573 '`5` requested id absent' (main() also refuses a requested row that is not `m
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=0/0 sources=2/2
ADVERTISED direct=1 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Receipt: `receipts/targeted-run.txt`. `wrong=0` covers the reference exit and class set of all six
fixtures; `null_detected=0` is a second unmodified run per fixture; `tampered=0` is the post-run tree
fingerprint; `sidechannel=0` is the counter's token scan (independently re-checked with a grep over the
24 tokens: no hit, and the module text carries none of them, including in comments and ids).

## Load-bearing table

**Remove one fixture at a time** (`grep -v "fx(\"<fid>\""` on a scratch copy; 5 fixtures left; same
envelope, `--only S07,S11`):

| removed | S07 | S11 |
|---|---|---|
| `s_exit-collision-admit` | killed by=`s_exit-collision-indented` | killed by=`s_exit-queued-admit` |
| `s_exit-collision-indented` | killed by=`s_exit-collision-admit` | killed by=`s_exit-queued-admit` |
| `s_exit-queued-admit` | killed by=`s_exit-collision-admit` | killed by=`s_exit-opened-elsewhere` |
| `s_exit-opened-elsewhere` | killed by=`s_exit-collision-admit` | killed by=`s_exit-queued-admit` |
| `s_exit-attest-opened` | killed by=`s_exit-collision-admit` | killed by=`s_exit-queued-admit` |
| `s_exit-absent-id` | killed by=`s_exit-collision-admit` | killed by=`s_exit-queued-admit` |

No single removal flips a mutant to SURVIVED: each mutant has **two** killing fixtures (mandated — the
second shape for S07, the second `main()` refusal for S11). So the aggregate table is not discriminating;
the sufficiency direction is (`awk` keeps only the named `fx(...)` line, 1 fixture, same envelope):

| fixture alone | S07 | S11 |
|---|---|---|
| `s_exit-collision-admit` | killed by=`s_exit-collision-admit` | SURVIVED |
| `s_exit-collision-indented` | killed by=`s_exit-collision-indented` | SURVIVED |
| `s_exit-queued-admit` | SURVIVED | killed by=`s_exit-queued-admit` |
| `s_exit-opened-elsewhere` | SURVIVED | killed by=`s_exit-opened-elsewhere` |
| `s_exit-attest-opened` | SURVIVED | SURVIVED (contrast by design) |
| `s_exit-absent-id` | SURVIVED | SURVIVED (contrast by design) |

Every one of the four killing fixtures kills its mutant **on its own** (`BATTERY fixtures=1 wrong=0`), and
the two contrasts kill nothing, as designed. Receipts: `receipts/load-bearing/rm-*.txt`, `solo-*.txt`.

## Full default counter (module installed in the clone's `plans/battery41/`)

```
cp battery/s_exit.py "$S/lane/plans/battery41/"
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent /usr/bin/python3 \
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round41_c1_verify.py --lane "$S/lane" --work "$S/w2"
```

```
MUTANT T01 receipts error SURVIVED exhibits=none -- plans/tip_receipts.py:30-32 '2 usage/setup (lane not a git work-tree root, no `corpus/evid
MUTANT T02 receipts error SURVIVED exhibits=none -- plans/tip_receipts.py:30-31 '2 usage/setup (..., no `corpus/evidence/`, ...)'
MUTANT T03 receipts rc-silence SURVIVED exhibits=none -- plans/tip_receipts.py:30 '1 a `differ`, a failed control, or a probe that did not complete
MUTANT T04 receipts rc-mirror SURVIVED exhibits=none -- plans/tip_receipts.py:21-23 'absolute mkdtemp paths are masked on both sides, so equality 
MUTANT T05 receipts error SURVIVED exhibits=none -- plans/tip_receipts.py:31-32 '2 usage/setup (..., unknown `--tamper` id)'
MUTANT T06 receipts rc-silence SURVIVED exhibits=none -- plans/tip_receipts.py:29-30 '0 every mapped receipt reproduces ... and the control reports
MUTANT T07 receipts error SURVIVED exhibits=none -- plans/tip_receipts.py:30-31 '2 usage/setup (lane not a git work-tree root, ...)'
MUTANT T08 receipts rc-mirror SURVIVED exhibits=none -- plans/tip_receipts.py:19-21 'A mapped receipt whose script is gone, whose dependency is ab
MUTANT T09 receipts silence SURVIVED exhibits=none -- plans/tip_receipts.py:13-14 'if its own basename resolves to exactly one committed `plans/
MUTANT T10 receipts silence SURVIVED exhibits=none -- plans/tip_receipts.py:15-16 'with non-alphanumerics dropped and case folded, the receipt s
MUTANT T11 receipts silence SURVIVED exhibits=none -- plans/tip_receipts.py:13-14 'A file enters the byte-comparison if the RECEIPTS table maps 
MUTANT T12 receipts silence SURVIVED exhibits=none -- plans/tip_receipts.py:12 'Population, stated mechanically: committed files `corpus/evidenc
MUTANT T13 receipts rc-mirror SURVIVED exhibits=none -- plans/tip_receipts.py:26-27 'the comparator must answer `differ`. ... A control that answe
MUTANT S01 sources 2>0 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1020-1021 '# Exclusive: before this
MUTANT S02 sources 2>1 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1042 '--registry and --package are 
MUTANT S03 sources 2>5 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1053 '--access-date must be an ISO 
MUTANT S04 sources 2>0 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1035-1036 '`--url-map` alone reache
MUTANT S05 sources 2>0 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1051 '--entries is required when --
MUTANT S06 sources 2>0 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1059 '--recheck must be an ISO date
MUTANT S07 sources 3>0 killed by=s_exit-collision-admit -- SKILL.md:573 '`3` staged/registry id collision'
MUTANT S08 sources 2>1 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1019 '--quote-file and --artifact m
MUTANT S09 sources 2>9 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error or unreadable quote artifact'; plans/sources_adopt.py:1028 '
MUTANT S11 sources 5>0 killed by=s_exit-queued-admit -- SKILL.md:573 '`5` requested id absent' (main() also refuses a requested row that is not `m
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=23 killed=2 survived=21 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=0/13 sources=2/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
```

`PREDICATE C1 fail` here is the expected partial-wave result (21 survivors are the other seats' work);
my two mutants are killed, `wrong/tampered/sidechannel/null_detected` all 0, both tool pins unchanged.
Receipt: `receipts/full-run.txt`.

## Module digest

```
sha256  5f57cec90bc347963fd7a011b158d7d2991d1b7ef69dbde90187600f0c390a64  s_exit.py
sha256  38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0  plans/sources_adopt.py  (frozen pin, unchanged)
```

## Host safety

- Every build (counter's own `bwrap --ro-bind / /` with the lane hidden) and every tool run (read-only
  host, fixed system PATH, `--unshare-net`) ran inside the mandated outer envelope
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000
  --proc /proc --unshare-pid --die-with-parent`.
- Nothing was written to `~/.local/bin`, `/usr`, `/etc`, `$HOME`, the lane, or the fleet root. The only
  writes are this report dir (`battery/`, `receipts/`) and scratch
  `/fast/scratch/hyaku/kengaku-r41/R41BatSrcExit/`, deleted at the end of the seat. No git mutation: the
  clone was written only to place the module in its `plans/battery41/` for the full run, with no
  `add`/`commit`.
- Neutralized modules `crit_git_shim.py` / `crit_ledger_selfread.py` untouched; no tool installed or
  upgraded (no pacman, no `uv`), so nothing to record.

## Risks and limits

1. **Attribution, not intent** (freeze limit): the kills are result differences in the declared
   direction (`3>0`, `5>0`); S07's own kill is the *first* matching fixture the counter meets, so with two
   S07 shapes "killed by" names `s_exit-collision-admit` only — the solo table is what shows the indented
   shape is independently sufficient.
2. **Redundancy is deliberate** (spec: a second shape for S07, a second `main()` refusal for S11), so the
   aggregate removal table cannot flip a mutant; the sufficiency table carries the load-bearing claim.
3. **`s_exit-absent-id` is rc-equivalent for both mutants** (5 vs 5) — the round-41 S10 withdrawal,
   reproduced here as a boundary; it is a contrast fixture, not a second kill mechanism.
4. The lane-shaped tree is **constructed**, never cloned from the lane (no lane copy exists in the
   fixture); the registry/package paths are the lane's real relative paths, which is the realism claim,
   not a copy of lane bytes.
5. The `sources` tool reports by exit code only; `defects=[]` is therefore exact, not an omission.

VERDICT: battery41-s_exit-killed-2/2-wrong-0
