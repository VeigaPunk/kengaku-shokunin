# F41RevBatSrcExit — non-author honesty review of `plans/battery41/s_exit.py`

Seat: critic, round 41 wave 2 (falsify). Target: the standing battery module `plans/battery41/s_exit.py`
(sha256 `5f57cec90bc347963fd7a011b158d7d2991d1b7ef69dbde90187600f0c390a64`), which claims kills of S07
(`3>0`) and S11 (`5>0`) of `plans/round41_c1_verify.py`. This seat read every line of the module, rebuilt
its fixtures in scratch, re-ran the frozen counter against this module alone, and instrumented both
frozen `old -> new` edits to see whether the mutated line executes on the killing fixture. Nothing frozen
was edited; no lane file was written; no tool installed or upgraded (no pacman, no `uv`).

Pins and tip actually measured (the clone was made from the lane as found, one wave-2 commit past the
dispatch tip):

```
git -C $S/lane rev-parse HEAD                          -> d7c77895752a2a5f317fa22f2362416ada50a04b
sha256 plans/round41_c1_verify.py                      -> 8835a94b0ad62dc1f58c861e2025b7c4bc8c0b936c202c64e01bc8b43f53eaa8
sha256 plans/sources_adopt.py                          -> 38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0
sha256 plans/tip_receipts.py                           -> e4f49714299ca1f2a93303c59ac07e691cc45d6126ccf24e5eecab93733f88f3
```

All three equal `.ufo/waves/round-41/claims/frozen-digests.txt`, so the attribution run below used the
frozen counter, not a copy. Receipts: `falsify/F41RevBatSrcExit/attribution-run.txt`, `mutant-matrix.txt`,
`static-vectors.txt`.

## Attribution — holds

Command (inside the mandated envelope, then the counter's own nested read-only sandboxes):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent /usr/bin/python3 \
  "$S/lane/plans/round41_c1_verify.py" --lane "$S/lane" --battery-dir "$S/bat_only" \
  --only S07,S11 --work "$S/w" --jobs 4
```

`$S/bat_only` holds **only** `s_exit.py`, so every kill below is produced by this module alone
(`attribution-run.txt`):

```
PINS total=2 mismatched=0
FIXTURE s_exit-collision-admit tool=sources expect=exit-3 ... observed_rc=3 ... ok
FIXTURE s_exit-collision-indented tool=sources expect=exit-3 ... observed_rc=3 ... ok
FIXTURE s_exit-queued-admit tool=sources expect=exit-5 ... observed_rc=5 ... ok
FIXTURE s_exit-opened-elsewhere tool=sources expect=exit-5 ... observed_rc=5 ... ok
FIXTURE s_exit-attest-opened tool=sources expect=accept ... observed_rc=0 ... ok
FIXTURE s_exit-absent-id tool=sources expect=exit-5 ... observed_rc=5 ... ok
MUTANT S07 sources 3>0 killed by=s_exit-collision-admit
MUTANT S11 sources 5>0 killed by=s_exit-queued-admit
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
```

Every fixture's reference result equals its declaration, including the class set (empty for the sources
tool by contract). Two independent builds of the module (`--build-module` into `fxbuild/` and
`fxbuild2/`) are byte-identical (`diff -r` → `FIXTURE-BUILDS-IDENTICAL`), so no kill rests on a
nondeterministic build. No fixture id collides with another battery41 module (`grep -h 'fx("' ... | uniq -d`
empty).

## Mutated-line execution — holds for both mutants

I rebuilt the six fixtures with the counter's own `--build-module` child, then ran five variants of
`plans/sources_adopt.py` from scratch — reference, the two frozen edits, and each edit carrying one
`print` beside it — against every fixture with its built argv, cwd = fixture dir (`mutant-matrix.txt`):

```
--- s_exit-collision-admit (exit-3) ref rc=3        registry=3 staged=1 collisions=1 malformed=0 duplicates=0 defects=0
                                                   collisions: S122
--- s_exit-collision-admit (exit-3) S07 rc=0        (same report line, then the appended S122 row)
--- s_exit-collision-admit (exit-3) trace_S07 rc=0  TRACE S07 code=3 want=['S122'] refcond=True mutcond=False
--- s_exit-collision-indented (exit-3) trace_S07 rc=0  TRACE S07 code=3 want=['S131'] refcond=True mutcond=False
--- s_exit-queued-admit (exit-5) ref rc=5           missing: S150:not-mined
--- s_exit-queued-admit (exit-5) S11 rc=0           (no block, no refusal)
--- s_exit-queued-admit (exit-5) trace_S11 rc=0     TRACE S11 missing=['S150:not-mined']
--- s_exit-opened-elsewhere (exit-5) trace_S11 rc=0 TRACE S11 missing=['S160:not-opened-this-round']
```

So on its killing fixture S07's mutated condition evaluates (same `code=3`, `want` non-empty) and flips
`True → False`, letting the run reach `build_block` and exit 0; S11's mutated guard sees a non-empty
`missing` list and skips the `EXIT_REQUEST` return. Both lines are load-bearing, not dead sites.

The reference exits are also the *advertised* ones, not a neighbouring code: the collision fixtures print
`collisions=1 malformed=0 duplicates=0 defects=0` with `collisions: S122` / `collisions: S131`, so exit 3
comes from the collision branch, not from the malformed/duplicate fall-through on the same return; the
S11 fixtures print the build-block reasons (`not-mined`, `not-opened-this-round`).

## Wave-1 counterexample vectors — none used

Checked against the vectors named in the round-41 brief, per fixture, including the probe-stub strings
(the module writes none):

| vector | finding |
|---|---|
| counter scratch root / `variants/` / slot file | Not reachable and not used. No fixture carries a `{WORK}` token or any absolute token; the only argv paths are `corpus/SOURCES.md`, `.ufo/waves/round-41/SOURCES.append.md`, `corpus/knowledge/tb2-constraints-scheduling-grader.md` — all relative, resolved under the cwd the counter sets to the fixture dir. |
| `/proc`, env, ppid, cmdline | Module text carries none of the 24 `SIDECHANNEL` tokens (independent `grep -c -F` over all 24 → no hit; counter prints `sidechannel=0`). No `ctx.sh` call at all: builds use `ctx.write` only. |
| relative `../` | No token contains `..`; fixture trees contain exactly three regular files each (`static-vectors.txt`), so nothing is reached outside `d`. |
| sockets / SysV IPC | Not used; no subprocess is started by any builder. |
| reading tool or counter program text | Not used; no file is read by a builder and no path to the lane is passed. |
| probe stub branching on something other than its own bytes | No executable or symlink is written (`find ... \( -type l -o -type f -perm -u+x \)` → empty). The three files are the registry, the entry and the adoption package. |

The two receipts under `claims/witness/` are not read, imported, copied or referenced by `s_exit.py`
(`grep -n "witness\|w_sources\|w_receipts" plans/battery41/s_exit.py` → exit 1), and the attribution run
above reproduced both kills with no witness module present, so the kills are independent of
`w_sources.py`.

## Findings (counterexamples against the module's own claims)

**F1 — `s_exit-collision-indented`, comment names a shape the fixture does not build (comment defect, no
verdict impact).** `plans/battery41/s_exit.py:57` says "the duplicate is pasted 2 spaces indented under a
bullet". The package it writes is `HEAD + row("S140") + row("S131", indent="  ")`; `cat -A` of the built
file shows the indented row directly after `| S140 ... |` with **no bullet line anywhere**:

```
| S140 | ... | mined | 2026-10-24 | ...
  | S131 | ... | mined | 2026-10-26 | ...
```

I rebuilt the claimed shape (a `- a bullet line` inserted before the indented row) and it behaves
identically — reference exit 3 with `collisions: S131`, S07 exit 0 appending S131
(`mutant-matrix.txt`, `bullet-shape ref: 3`) — so the mis-statement is cosmetic, but as landed the fixture
does not exercise "under a bullet". The wave-1 report repeats the same wording
(`.ufo/waves/round-41/build/R41BatSrcExit.md:37`).

**F2 — `s_exit-absent-id`, comment claims isolation that the mutant does not have (comment defect, no
verdict impact).** `plans/battery41/s_exit.py:88` says the absent id is refused "(exit 5) before either
mutated line is reached". Half wrong: S07's edited line *is* reached and evaluated —
`TRACE S07 code=5 want=['S199'] refcond=True mutcond=False` — and, because the mutated condition is false
for a non-empty `want`, the S07 run then enters `build_block`, prints a **second** `missing: S199`, and is
saved from exit 0 only by the untouched `return EXIT_REQUEST` (`mutant-matrix.txt`). S11's line is indeed
not reached. The fixture's verdict (ref 5, S07 5, S11 5) is still correct; the stated mechanism is not.

**F3 — S11's advertisement is code-internal, not the sentence it quotes (calibration caveat, admission
relevant, not a fixture defect).** SKILL.md:573 reads "`5` requested id absent". The only reachable
instances of S11's mutated line are `not-mined` and `not-opened-this-round`: the literally advertised case
is intercepted by the unmutated `check()` first, which is exactly what `s_exit-absent-id` measures
(ref 5, S11 5). So the kill demonstrates `build_block`'s refusal — asserted by that function's own comment
and by main()'s printed message — and only *indirectly* connected to the quoted exit-5 sentence. The
counter labels it `indirect` and prints `ADVERTISED direct=1 indirect=1`, and the module's own comment
names the branch precisely, so nothing is misrepresented at the fixture level; but a strict reading that
credits only the quoted contract sentence would score S11 as a survivor and fail C1. That call belongs to
L1, and it should be recorded rather than silently absorbed into `killed=23`.

## Per-fixture verdicts

| fixture | claims | verdict | why |
|---|---|---|---|
| `s_exit-collision-admit` | S07 `3>0` | **honest** | Refuses with `collisions: S122`/rc 3; S07 appends the colliding mined row and exits 0. Mutation exercised (trace). |
| `s_exit-collision-indented` | S07 `3>0` (second shape) | **honest** (comment defect F1) | Same branch on a 2-space-indented duplicate: `collisions: S131`/rc 3 → S07 rc 0 appending it. The "under a bullet" description is not what was built. |
| `s_exit-queued-admit` | S11 `5>0` | **honest** | `check()` passes (`queued` ∈ `STATUSES`), `build_block` refuses `not-mined`/rc 5; S11 skips the refusal and exits 0. Mutation exercised (trace). |
| `s_exit-opened-elsewhere` | S11 `5>0` (second refusal) | **honest** | Stale `opened` 2026-09-30 without `--attest-opened` → `not-opened-this-round`/rc 5 → S11 rc 0. |
| `s_exit-attest-opened` | no kill (boundary) | **honest** | `--attest-opened` re-dates and appends: ref 0, S07 0, S11 0. Declared contrast, honestly reported as carrying no kill. |
| `s_exit-absent-id` | no kill (boundary) | **honest** (comment defect F2) | A requested id absent from the package refuses in `check()`/rc 5 for all three variants; the stated "before either mutated line" is wrong for S07. |

No fixture reaches its verdict through a wave-1 vector, so none is `dishonest`; none is `incidental` either
— in each killing fixture the advertised refusal is the observed reference behaviour and the mutant's exit
change is caused by the frozen edit.

## Impacted axes

- **Calibration**: 6/6 fixtures honest, 2/2 mutated lines executed. The two comment defects do not move a
  verdict, but F2 shows the boundary fixture's stated isolation is false for S07, and F3 is the S11
  advertisement question the closure has to answer explicitly.
- **Independence / duplicate authority**: no shared helper, no import, no path into `claims/witness/`; ids
  unique across battery41; builds deterministic.
- **Host safety**: every build and tool run stayed inside the mandated envelope; `~/.local/bin`, `/usr`,
  `/etc` and `$HOME` untouched; no git or jj mutation; writes confined to this report dir and
  `/fast/scratch/hyaku/kengaku-r41/F41RevBatSrcExit/`.

## Smallest safe correction

1. Edit two comments only (no fixture bytes, no counter change): `s_exit.py:57` drop "under a bullet", or
   make the shape real by emitting a bullet line before the indented row (verified behaviourally
   equivalent, still rc 3 → 0); `s_exit.py:88` replace "before either mutated line is reached" with the
   measured statement — `check()` returns 5 before `main()`'s gate, while S07 still traverses the gate into
   `build_block`.
2. At integration, record S11's kill as an indirect advertisement anchored to `build_block`'s refusal, so
   the `sources=10/10` floor is not read as ten kills of literally quoted contract sentences.

VERDICT: battery41-s_exit-honest-6/6-mutated-line-executed-2/2
