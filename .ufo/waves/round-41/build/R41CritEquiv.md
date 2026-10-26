# R41CritEquiv — equivalence, incidental kills, and the advertised denominator (C1)

Seat: R41CritEquiv (critic, leaf). Round 41 wave 1, item R41CritEquiv. Judged on calibration.
Object of review: the 23 frozen mutants of `plans/round41_c1_verify.py` (freeze `8ef8b4f`), the two pinned
tools `plans/tip_receipts.py` (`e4f49714…`) and `plans/sources_adopt.py` (`38492bf1…`), and the claim's
denominator in `plans/round-41-claims.md` §C1. Nothing frozen was edited; nothing was committed; no fleet
or lane file was written.

## 0. Method and evidence

Every fixture and tool run below was executed inside the wave envelope, from a scratch clone of the lane
(`git clone -q --shared … /fast/scratch/hyaku/kengaku-r41/R41CritEquiv/lane`, `rev-parse --show-toplevel`
asserted equal to the clone), with the fixed system PATH and `HOME=/nonexistent`:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
      --proc /proc --unshare-pid --die-with-parent /usr/bin/python3 <probe> <lane-clone> <scratch>
```

I wrote my own fixtures (`equiv_probe.py`, 23 fixtures, one per mutant) and my own auxiliary checks
(`critic_checks.py`). Neither imports, copies nor reads
`.ufo/waves/round-41/claims/witness/w_receipts.py` / `w_sources.py`; the witness was consulted read-only
to learn what shapes are reachable. Mutant copies are byte-level `old -> new` substitutions taken from the
frozen `MUTANTS` table itself (each asserted to occur exactly once). Receipts archived beside this report:
`equiv_probe.py`, `equiv.json`, `equiv.err` (23/23 rows), `critic_checks.py`, `critic_checks.txt`,
`critic_checks.err`.

Measured summary of the run: `rows=23 direction_ok=23` (`equiv.json`); no fixture produced a `wrong`
reference result, so every mutant is reachable in its declared direction. The scratch directory was
reclaimed by something else at ~15:42 (two sibling seat dirs remained); all receipts were re-created from
scratch and archived under this report directory.

## 1. Equivalents: none

For each mutant there is at least one input where the reference and the mutant differ in the declared
direction, with the advertised clause as the cause. The table is the measured result; `cls` columns are the
frozen counter's own `classes()` output on stdout, so a `silence` kill is a printed-class difference and
the `rc-*`/pair kills are exit-code differences.

| mid | dir | my fixture (built from nothing) | ref | mut | ref classes / notes | ok |
|---|---|---|---|---|---|---|
| T01 | error | no `corpus/evidence/`, git root | 2 | 0 | `SETUP:` line, then green | ✔ |
| T02 | error | same lane (guard at `tip_receipts.py:241` removed) | 2 | 0 | `receipts=0` green run | ✔ |
| T03 | rc-silence | probe writes `X\n` then exits 3, receipt `X\n` | 1 | 0 | `differ:…` → `equal:…` | ✔ |
| T04 | rc-mirror | `round36/regex-log-probe-first-run.txt` (table row, kind `temp-paths`) | 0 | 1 | `skip:…:declared-nonreproducible…` → `differ:…` | ✔ |
| T05 | error | `--tamper corpus/evidence/nope.txt` | 2 | 1 | **traceback**, `KeyError` | ✔ |
| T06 | rc-silence | empty committed receipt + empty probe stdout | 1 | 0 | `control:unavailable` retained in stdout | ✔ |
| T07 | error | lane = plain subdirectory of a repo | 2 | 1 | **traceback**, `CalledProcessError` | ✔ |
| T08 | rc-mirror | `Run as: uv run …` (uv absent from fixed PATH; `uv` exists only at `~/.local/bin/uv`) | 0 | 1 | `skip:…:dependency-missing` → `differ:…` | ✔ |
| T09 | silence | receipt stem matched by two scripts (`foo_probe.py`, `fooprobe.py`) | 0 | 0 | `skip:…:no-committed-re-run-command` → `map:…:derived` | ✔ |
| T10 | silence | receipt `foo-probe.txt` + script `foo_probe.py` | 0 | 0 | `map:…:derived` → `skip:…` | ✔ |
| T11 | silence | table row `round35/tb2-grader-probe.txt` + its derivable script | 0 | 0 | `map:…:table` → `map:…:derived` | ✔ |
| T12 | silence | `corpus/evidence/r/foo-probe.log` only | 0 | 0 | `skip:…:no-committed-re-run-command` → no line | ✔ |
| T13 | rc-mirror | byte-equal receipt, automatic control | 0 | 1 | `control:differ` + `equal:…` | ✔ |
| S01 | 2>0 | quote mode + `--registry` | 2 | 0 | silent success | ✔ |
| S02 | 2>1 | no arguments | 2 | 1 | **traceback**, `AttributeError: 'NoneType' … 'read_text'` | ✔ |
| S03 | 2>5 | `--access-date 2026/10/25` + admit | 2 | 5 | mutant refuses via `missing: S900` | ✔ |
| S04 | 2>0 | `--registry/--package` + `--url-map {}` | 2 | 0 | flag silently ignored | ✔ |
| S05 | 2>0 | `--admit-ids` without `--entries` | 2 | 0 | block written | ✔ |
| S06 | 2>0 | `--recheck soon` | 2 | 0 | block written | ✔ |
| S07 | 3>0 | staged id == registry id, with `--admit-ids` | 3 | 0 | collision report, then block | ✔ |
| S08 | 2>1 | `--quote-file` alone | 2 | 1 | **traceback**, `AttributeError: 'NoneType' … 'is_file'` | ✔ |
| S09 | 2>9 | `--quote-file/--artifact/--url-map absent.json` | 2 | 9 | falls through to `EXIT_URL_UNMAPPED` | ✔ |
| S11 | 5>0 | requested row `status=queued` | 5 | 0 | `missing: S900` suppressed in both branches | ✔ |

`equivalents = 0`. Caveat carried from the claim: a kill records a result difference in the declared
direction, not the fixture's intent — §3 and §5 are where that caveat bites.

## 2. Incidental kills: 4 (`T05`, `T07`, `S02`, `S08`)

Each of these four mutants is killed while *crashing*: the declared direction accepts the mutant's exit
code, but the mutant never reaches an advertised branch. Exact observations (`critic_checks.txt`,
`equiv.json`):

| mid | reference | mutant | last stderr line |
|---|---|---|---|
| T05 | `SETUP: --tamper … is not a mapped receipt`, rc 2 | rc 1, traceback | `KeyError: 'corpus/evidence/nope.txt'` |
| T07 | `SETUP: --lane … is not a git work-tree root`, rc 2 | rc 1, traceback | `subprocess.CalledProcessError: … 'git','clone','-q','--shared','…/repo/sub' … status 128` |
| S02 | `error: --registry and --package are required …`, rc 2 | rc 1, traceback | `AttributeError: 'NoneType' object has no attribute 'read_text'` |
| S08 | `error: --quote-file and --artifact must be given together`, rc 2 | rc 1, traceback | `AttributeError: 'NoneType' object has no attribute 'is_file'` |

### 2a. Three of the four are crash-only by construction — no input can do better

* **T05** (`tip_receipts.py:336` `if unknown:` → `if False:`): the refusal is the *only* consumer of
  `unknown`. With it gone, `controls = tamper` (`:338`) contains an id that is not in `results` **by
  definition of unknown**, and the loop dereferences `results[rel]` (`:345`) → `KeyError`, always. Measured
  also with a mixed `--tamper <known>,<unknown>` list (`critic_checks.txt`): still `KeyError`, rc 1. No
  input makes this mutant accept-and-continue.
* **S02** (`sources_adopt.py:1041-1042` → `if False:`): the guard fires exactly when one of
  `--registry`/`--package` is `None`; `check()` → `collect()` reads `package.read_text()` (`:185`) then
  `registry.read_text()` (`:186`). Either side `None` ⇒ `AttributeError`, every time. Both sides measured
  (`--registry` only and `--package` only), both `AttributeError … 'read_text'`.
* **S08** (`sources_adopt.py:1018-1019` → `if False:`): the guard fires exactly when one of
  `--quote-file`/`--artifact` is `None`; `quote_check` calls `load_artifact(artifact)` (`:463`, needs
  `path.is_file()`) and then `quote_file.read_text()` (`:482`). Either side `None` ⇒ `AttributeError`. Both
  shapes measured (`--quote-file` alone: `'NoneType' … 'is_file'`; `--artifact` alone: `… 'read_text'`).

So for T05/S02/S08 the kill is real but the *evidence* is "the mutant crashes", never "the mutant
misbehaves as advertised". A fixture cannot fix this; only a different mutant (one whose fall-through is
non-crashing) could.

### 2b. T07 is incidental only as witnessed — a clean kill exists and was measured

The recorded witness (`w-t07-lane-is-subdir`, `witness-run.txt`) uses a lane that is a plain subdirectory
of another work tree. That lane can never be cloned (`git clone --shared …/repo/sub` →
`fatal: repository '…/repo/sub' does not exist`, rc 128, measured), so `main`'s unguarded
`subprocess.run(["git","clone",…], check=True)` (`tip_receipts.py:270`) raises and the process exits 1
with a traceback. The mutant's exit 1 is therefore a crash, not a behaviour.

A non-crashing route exists: a lane whose `core.worktree` names another directory is a genuine "not a
work-tree root" while still being a cloneable repository. Measured (`critic_checks.txt`):

```
toplevel= …/chk_cw/elsewhere
[T07 core.worktree lane]
  ref rc=2  SETUP: --lane … is not a git work-tree root (rev-parse says …/elsewhere)
  mut rc=0  receipts=1 byte_equal=1 differ=0 skipped=0
```

Recommendation for the wave's fixtures: build T07's fixture with `git config core.worktree <other dir>`
(inside the fixture) instead of a bare subdirectory, so the kill is attributable to the advertised branch.

## 3. Consequential defect (found through T07, no mutant covers it)

`tip_receipts.py:30-32` advertises `2 usage/setup (…, clone or cleanup failure, …)`. Both halves are
false in the unmutated tool:

* **clone failure** — the clone at `:270` is unguarded (`check=True`, no `try`). Measured on the unmutated
  tool by corrupting one blob object in an otherwise valid lane: `rc=1 traceback=True stdout=''`,
  `err_has_SETUP=False` (`critic_checks.txt`). A clone failure exits 1 with a traceback, not 2.
* **cleanup failure** — the only cleanup is `finally: shutil.rmtree(ws, ignore_errors=True)` (`:357`), which
  cannot raise; no path can report a cleanup failure with 2.

This is the advertisement-vs-code gap that made T07's kill look attributable when it is not: T07's
mutant does not lose a working refusal — it exposes a refusal the tool never implemented. It is not a
mutation-equivalence (the mutant differs from the reference), but it is a calibration limit for the claim.

## 4. Attribution mismatch: T06's advertised cell vs its recorded kill

T06 carries the round's only receipts-side `indirect` cell: "an unavailable control on an empty receipt is
a failed control". Its recorded witness is `w-t03-probe-exit-3` — a *differ* fixture with no equal
receipt, where `controls` is empty and `control_ok` stays `True` vacuously. Measured on that shape
(`critic_checks.txt`): `ref rc=1` (`differ=1`) and `mut rc=0` with the **same** stdout line
(`receipts=1 byte_equal=0 differ=1 skipped=0`). So the recorded kill demonstrates a different clause — "a
`differ` exits 1" (`tip_receipts.py:383`) — not the unavailable-control clause. The advertised route does
also kill it (my empty-receipt fixture: ref 1 with `control:unavailable`, mut 0), so the `adv` cell is
reachable; it is just not what the witness exercised. Cheap fix: use the empty-receipt fixture for T06.

## 5. Denominator honesty: 30 advertised behaviours have no mutant

Criterion (stated so the number is checkable): an advertised behaviour counts as **unlisted** when no
frozen mutant's `old -> new` changes the code that produces it, so *no fixture can ever calibrate it* — the
survivor count cannot move. I excluded rows whose implementing line is touched by a mutant even for a
different clause (e.g. "a `differ` exits 1" shares `tip_receipts.py:383` with T06; "absent git → 2" shares
`die()` with T01), and I excluded implementation output that is nowhere advertised. Last column: why.

### `plans/tip_receipts.py` — docstring (L4–36); `SKILL.md:586` duplicates the exit clauses (19)

| # | advertised (file:line) | implements | no mutant because |
|---|---|---|---|
| R1 | `--only SUBSTR` restricts the population (L4) | `:249` | line untouched by every mutant |
| R2 | `--jobs N` runs probes in parallel (L4) | `:298` | line untouched (observable only in timing) |
| R3 | `doc=` provenance: the same line SKILL/README quote (L8-9) | `provenance()` `:160` | untouched |
| R4 | the clone is of the lane at HEAD; toplevel and HEAD equality guards (L9-10) | `:269-276` | untouched (T07 mutates the pre-clone guard `:123`) |
| R5 | byte-compare fresh stdout with the committed blob; `first_diff` (L10-11) | `:326`, `first_diff()` `:186` | untouched (T03 short-circuits on probe exit `:314`; T04 mutates only `:319`) |
| R6 | a receipt the RECEIPTS table maps enters the comparison (L13) | `:245` | untouched (T11 mutates the override skip `:97`) |
| R7 | a derived mapping is `kind=byte` (L16) | `:101` | untouched (T09 mutates `:100`) |
| R8 | script gone → `skip reason=probe-script-absent` (L19-20) | `:287-288` | untouched (T08 mutates `:291`) |
| R9 | a `temp-paths` receipt is still re-run (L21) | `:296`, `:318` | untouched |
| R10 | any other difference on a `temp-paths` receipt is still `differ` (L23) | `:322-324` | untouched (T04 mutates the equal branch `:319`) |
| R11 | `--tamper` is repeatable and comma-splittable (L25) | `:333` | untouched |
| R12 | one byte is flipped and the same fresh output re-compared (L25-26) | `tamper_one_byte()` `:214`, `:350-351` | untouched (T13 mutates `:355`) |
| R13 | with no `--tamper`, the control runs on the **cheapest** byte-equal receipt (L26-27) | `:341` | untouched |
| R14 | clone failure → exit 2 (L31-32) | `:270` | untouched **and false**: measured rc 1 + traceback (§3) |
| R15 | cleanup failure → exit 2 (L31-32) | `:357` | untouched **and unreachable**: `ignore_errors=True` |
| R16 | the lane is read only (L34) | whole `main` | untouched |
| R17 | probe `TMPDIR`/`TEMP`/`TMP` inside the work dir (L35-36) | `run_probe()` `:201-212` | untouched |
| R18 | the work directory is removed on exit (L36) | `:357` | untouched |
| R19 | no receipt is ever written (L36) | whole `main` | untouched |

### `plans/sources_adopt.py` — `SKILL.md:573` row + `main()` parser messages (11)

| # | advertised (file:line) | implements | no mutant because |
|---|---|---|---|
| S1 | `0` gates an append and prints the append block (`SKILL.md:573`) | `:1073-1079` | untouched; S07's mutant reaches 0 *after a collision*, not on this path |
| S2 | `4` malformed staged row (`SKILL.md:573`) | `check()` `:231` | no mutant touches the malformed/duplicate refusal |
| S3 | `6` quote over the 25-word cap (`SKILL.md:573`) | `quote_check()` `:562` | untouched |
| S4 | `7` quote absent from the artifact (`SKILL.md:573`) | `:564` | untouched |
| S5 | `8` quote bound to a mismatched URL (`SKILL.md:573`) | `:566` | untouched |
| S6 | `9` quote has no url-map entry (`SKILL.md:573`) | `:568` | untouched (S09's mutant *reaches* 9 via the unreadable-map fall-through; the 8/9 rule is not mutated) |
| S7 | `--access-date is required when --admit-ids is given` | `:1048-1049` | no mutant — the list prices S03 (ISO format) and S05 (entries) but not this guard |
| S8 | `--attest-opened` re-dates the opened cell and prints `attested:` | `:1065-1067` | no mutant |
| S9 | `--out` writes the block and prints `wrote … rows=` | `:1074-1076` | no mutant |
| S10 | `--scope-to-admit` narrows refusals to the requested rows | `:1044`, `check()` `:211-229` | no mutant |
| S11 | `--selftest` (17 cases, `SKILL.md:573`) | `selftest()` `:621` | no mutant |

`unlisted-advertised = 19 + 11 = 30`.

Consequence for the claim's self-assessment: the 23-mutant list bounds *mutants*, not advertised
behaviours. `MUTANTS total=23 killed=23` can be printed while the 30 clauses above remain uncalibratable by any
fixture the wave can write — including two (R14, R15) that the unmutated tool contradicts today. The
honest reading of "calibration 23" is "23 mutants over an advertised surface of at least 53 distinct
clauses, 30 of which no mutant can price", and one of the two `indirect` cells (T06) was witnessed on a
different clause than it declares (§4).

## 6. Smallest safe correction (for the L1 / wave-1 executors; frozen files untouched)

1. **T07 fixture**: build it as a lane with `core.worktree` pointed at another directory in the fixture
   (§2b), so the kill is the advertised refusal rather than `CalledProcessError` in `git clone`. Cost: one
   `git config` in `build()`.
2. **T06 fixture**: use the empty-receipt / `control:unavailable` shape so the `indirect` cell is the one
   demonstrated, not the `differ` clause (§4). Cost: one fixture line (already measured to kill).
3. **Record the four crash-mediated kills as a named limit** in the C1 report: T05, S02, S08 are crash-only
   (direction classes were chosen so that exit 1 counts), and T07 was witnessed through a crash. Do not
   remove or relabel the mutants — the claim's kill rule already says a demonstrated limit is reported,
   not repaired. No edit to the two tools this round; fold R14/R15 (advertised exit-2 causes that are not
   implemented) into the round-41 lesson as a priced follow-up.

## 7. Commands that produced the numbers

```
# 23 independent fixtures, ref vs mutant, classes via the frozen counter's own parser
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent /usr/bin/python3 \
  .ufo/waves/round-41/build/R41CritEquiv/equiv_probe.py <lane-clone> <scratch>     # rows=23 direction_ok=23

# auxiliary checks (T07 clean route, subdir clone refusal, unmutated clone failure, S02/S08/T05 crash
# shapes, T06 differ vs control-unavailable)
bwrap … /usr/bin/python3 …/critic_checks.py <scratch> …/R41CritEquiv                 # critic_checks.txt

# clone of a subdirectory, measured directly
git clone -q --shared <repo>/sub <dest>    # fatal: repository '<repo>/sub' does not exist   rc=128

# uv is absent from the counter's fixed PATH (T08 reachability)
command -v uv                              # /home/vgpnk/.local/bin/uv (PATH excludes it)
```

VERDICT: equivalents-0-incidental-4-unlisted-advertised-30
