# R41BatSrcUsage — battery41 module for the sources_adopt.py usage refusals (S02, S03, S05, S06)

Seat: executor, round 41 wave 1 (hyaku run 9, 2026-10-26). Deliverable: one battery41 module with
fixtures that ATTRIBUTABLY kill frozen mutants S02, S03, S05, S06 of `plans/round41_c1_verify.py`
in their declared directions, proved in a clone inside the mandated envelope.

## 1. Module

- Path: `.ufo/waves/round-41/build/R41BatSrcUsage/battery/s_usage.py` (130 lines, stdlib only, no
  imports at all; every fid starts `s_usage-`; `sha256 c9ca3abe3d4b5dff02d9196e026ab31f7b37347d0866769ac509116fc07afeff`).
- 8 fixtures, all `tool=sources`, all `expect=error` (reference exit 2), all `defects=[]` (the
  sources tool has no classes; the counter refuses a non-empty set for it).
- The module reads nothing at run time: no witness import/copy, no tool text, no lane access.
  Independent shape from `claims/witness/w_sources.py` b02/b03/b05/b06: every fixture builds a
  lane-shaped tree — `corpus/SOURCES.md` registry with two real-shaped rows (S118 mined, S124
  queued/`on-release`) plus a `corpus/SOURCES.append.md` package table — instead of the witness's
  bare `reg.md`/`pkg.md`, and each guard is triggered twice where it has two operands.
- Token scan of the module text (lowercased) against the counter's SIDECHANNEL tuple: no hits
  (`fids: 8`, `token hits: []`); the counter itself reports `sidechannel=0`.

| fid | mutant (declared direction) | behaviour demonstrated | reference rc | mutant rc |
|---|---|---|---|---|
| `s_usage-02-registry-without-package` | S02 (`2>1`) | `--registry` given, `--package` forgotten (first operand of `if not args.registry or not args.package`) | 2 | 1 |
| `s_usage-02-package-without-registry` | S02 (`2>1`) | `--package` readable, `--registry` forgotten (second operand; `check(pkg, None)` crashes) | 2 | 1 |
| `s_usage-03-dotted-access-date` | S03 (`2>5`) | `--access-date 26.10.2026` refused as usage *before* any row is built; mutant falls through to `build_block` with a row whose `opened` differs → `EXIT_REQUEST` | 2 | 5 |
| `s_usage-03-single-digit-month-duplicate-request` | S03 (`2>5`) | second trigger: `--access-date 2026-1-5` is non-ISO, and the requested id is duplicated so the mutant's 5 comes from `duplicate-request`, not from the opened cell | 2 | 5 |
| `s_usage-05-two-ids-without-entries` | S05 (`2>0`) | `--admit-ids S131,S132` with no `--entries` (used-by has no fallback); mutant appends both rows with `—` as used-by | 2 | 0 |
| `s_usage-05-empty-entries-value` | S05 (`2>0`) | `--entries ""` — the flag is present but empty, same refusal (`not args.entries`) | 2 | 0 |
| `s_usage-06-recheck-cadence-word` | S06 (`2>0`) | `--recheck monthly` (not ISO, not `<N>d`, not symbolic); mutant builds the block with the packaged `180d` cell intact | 2 | 0 |
| `s_usage-06-recheck-prose-scoped-row` | S06 (`2>0`) | scoped adoption (`--scope-to-admit`) of a row whose recheck cell is prose, `--recheck "every 30 days"`: the CLI default the guard protects would rewrite that cell; mutant normalises it and exits 0 | 2 | 0 |

## 2. Scoped proof (mandated command, exact output)

```
S=/fast/scratch/hyaku/kengaku-r41/R41BatSrcUsage; export TMPDIR="$S"
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
  --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
  python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round41_c1_verify.py \
  --lane "$S/lane" --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-41/build/R41BatSrcUsage/battery \
  --only S02,S03,S05,S06 --work "$S/w"
```

```
PINS total=2 mismatched=0
FIXTURE s_usage-02-registry-without-package tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_usage-02-package-without-registry tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_usage-03-dotted-access-date tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_usage-03-single-digit-month-duplicate-request tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_usage-05-two-ids-without-entries tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_usage-05-empty-entries-value tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_usage-06-recheck-cadence-word tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_usage-06-recheck-prose-scoped-row tool=sources expect=error declared=- observed_rc=2 observed=- ok
MUTANT S02 sources 2>1 killed by=s_usage-02-registry-without-package -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1042 '--registry and --package are 
MUTANT S03 sources 2>5 killed by=s_usage-03-dotted-access-date -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1053 '--access-date must be an ISO 
MUTANT S05 sources 2>0 killed by=s_usage-05-two-ids-without-entries -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1051 '--entries is required when --
MUTANT S06 sources 2>0 killed by=s_usage-06-recheck-cadence-word -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1059 '--recheck must be an ISO date
BATTERY fixtures=8 wrong=0 tampered=0 sidechannel=0
MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=0/0 sources=4/4
ADVERTISED direct=4 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
rc=0
```

`wrong=0 tampered=0 sidechannel=0 null_detected=0`, every FIXTURE line `ok`, all four mutants
`killed by=` one of my fids. Receipt copy: `scoped-run.txt`.

## 3. Load-bearing table

Single-fixture removal (7 fixtures left, `--only S02,S03,S05,S06`; full output in
`loadbearing-single.txt`). **No single fixture is load-bearing**: each behaviour has two
independent triggers, so removing one leaves its twin killing the same mutant.

| removed fixture | mutant that flips to SURVIVED | kill seen instead |
|---|---|---|
| `s_usage-02-registry-without-package` | none | S02 by `s_usage-02-package-without-registry` |
| `s_usage-02-package-without-registry` | none | S02 by `s_usage-02-registry-without-package` |
| `s_usage-03-dotted-access-date` | none | S03 by `s_usage-03-single-digit-month-duplicate-request` |
| `s_usage-03-single-digit-month-duplicate-request` | none | S03 by `s_usage-03-dotted-access-date` |
| `s_usage-05-two-ids-without-entries` | none | S05 by `s_usage-05-empty-entries-value` |
| `s_usage-05-empty-entries-value` | none | S05 by `s_usage-05-two-ids-without-entries` |
| `s_usage-06-recheck-cadence-word` | none | S06 by `s_usage-06-recheck-prose-scoped-row` |
| `s_usage-06-recheck-prose-scoped-row` | none | S06 by `s_usage-06-recheck-cadence-word` |

To show the group is load-bearing, both fixtures of one mutant were then removed together
(`loadbearing-pairs.txt`), and exactly the intended mutant flips:

| removed pair | result |
|---|---|
| both `s_usage-02-*` | `MUTANT S02 sources 2>1 SURVIVED exhibits=none`; S03/S05/S06 still killed; `MUTANTS total=4 killed=3 survived=1` |
| both `s_usage-03-*` | `MUTANT S03 sources 2>5 SURVIVED exhibits=none`; `killed=3 survived=1` |
| both `s_usage-05-*` | `MUTANT S05 sources 2>0 SURVIVED exhibits=none`; `killed=3 survived=1` |
| both `s_usage-06-*` | `MUTANT S06 sources 2>0 SURVIVED exhibits=none`; `killed=3 survived=1` |

Every fixture is therefore attributable (`killed by=<fid>` names it) and its mutant's kill depends
only on this module's fixtures.

## 4. Full default counter run

Module copied to `$S/lane/plans/battery41/s_usage.py` (clone of the lane at `fc79f2a4`, tools at
their frozen pins `e4f49714…` / `38492bf1…`; clone toplevel asserted before the write;
`git -C "$S/lane" status --porcelain` = `?? plans/battery41/` only, nothing committed):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
  --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
  python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round41_c1_verify.py \
  --lane "$S/lane" --work "$S/w2"
```

```
MUTANT T01 receipts error SURVIVED exhibits=none ...
[... T02–T13, S01, S04, S07–S09, S11 SURVIVED exhibits=none: no other module was present ...]
MUTANT S02 sources 2>1 killed by=s_usage-02-registry-without-package -- ...
MUTANT S03 sources 2>5 killed by=s_usage-03-dotted-access-date -- ...
MUTANT S05 sources 2>0 killed by=s_usage-05-two-ids-without-entries -- ...
MUTANT S06 sources 2>0 killed by=s_usage-06-recheck-cadence-word -- ...
BATTERY fixtures=8 wrong=0 tampered=0 sidechannel=0
MUTANTS total=23 killed=4 survived=19 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=0/13 sources=4/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
rc=1
```

`PREDICATE C1 fail` / 19 survivors are expected here: `plans/battery41` in this clone holds only
my module, so the 13 receipts mutants and the six sources mutants owned by other wave-1 seats have
no fixture yet. My module contributes exactly `sources=4/10` with `wrong=0`, `tampered=0`,
`sidechannel=0`, `null_detected=0`. Full output: `full-run.txt`.

## 5. Host safety and bounds

- Every counter/battery/fixture run went through the mandated envelope
  (`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin … --tmpfs /run/user/1000 --proc /proc
  --unshare-pid --die-with-parent`); the counter nested its own read-only sandboxes inside it.
- Nothing was written to `~/.local/bin`, `/usr`, `/etc` or `$HOME`: the module's builds write only
  inside the counter's fixture dirs (`tampered=0` — the content-digest fingerprints are unchanged
  after every run), and no fixture writes into the fixture tree at tool time (the tool runs
  read-only there; no `--out` is used).
- `crit_git_shim.py` / `crit_ledger_selfread.py`: untouched; no shim, no PATH write, no git
  mutation (one index-free clone under scratch, nothing committed, `git` called only with
  `-C` on that clone).
- Writes outside my scratch: only
  `.ufo/waves/round-41/build/R41BatSrcUsage/{battery/s_usage.py, scoped-run.txt,
  loadbearing-single.txt, loadbearing-pairs.txt, full-run.txt, this report}` (created 15:38).
  No lane file was edited; `PINS-AFTER mismatched=0` on both runs proves the frozen tools are intact.
- No tool installs or updates were needed (`bwrap`, `python3` already present).
- Scratch `/fast/scratch/hyaku/kengaku-r41/R41BatSrcUsage` is deleted before this seat ends.

## 6. Risks / limits

- S02's mutant exit is 1 from an uncaught `AttributeError` on the `None` path argument, not a second
  usage refusal. The frozen direction is exactly `2>1`, so the kill is attributable as declared,
  but the mutant dies by crash — the same limit the freeze names for the whole corpus ("a kill
  records a result difference in the declared direction, not the fixture's intent").
- `s_usage-05-empty-entries-value` passes `--entries ""`; argparse accepts the empty value, so the
  refusal really is `not args.entries` and not a parser complaint (observed rc 2, mutant rc 0).
- `s_usage-06-recheck-prose-scoped-row` depends on `--scope-to-admit` filtering the prose-recheck
  defect before the guard; that path is exercised only in the mutant run (`0`), the reference stops
  at the recheck guard (`2`). If a later round narrows `main()`'s guard order, this fixture stays a
  valid `error` case, but its mutant delta would move.

VERDICT: battery41-s_usage-killed-4/4-wrong-0
