# F42C1Rerun — C1 re-measured at `508434ad55c709337065611691c426f05875492d`, plus battery42 module ablation

Seat: F42C1Rerun (executor, wave 2 falsify). Attack surface: the C1 calibration counter and its battery —
NOT the landing bytes. Nothing in the lane was written; nothing here is a judgement of the round.

## Axes

1. **Determinism** — does the counter's verdict depend on hash seed, job count, clone path, `$HOME`, or `TMPDIR`?
2. **Load-bearing fixtures** — is each of the 5 battery42 modules actually responsible for a kill, or does the
   29-fixture battery contain decoration?
3. **Fail-closed** — when its own input is untrusted (pin mismatch), does the counter refuse to score kills?
4. **Host safety** — did any of my runs write outside scratch (the Q32 anti-tamper line)?

## Setup (clone + envelope, both recorded per run)

```
git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane
git -C $S/lane checkout -q 508434ad55c709337065611691c426f05875492d
git -C $S/lane rev-parse --show-toplevel  -> /fast/scratch/hyaku/kengaku-r42/F42C1Rerun/lane
git -C $S/lane rev-parse HEAD             -> 508434ad55c709337065611691c426f05875492d
```
`S=/fast/scratch/hyaku/kengaku-r42/F42C1Rerun`, `TMPDIR=$S/tmp`. Envelope used for every invocation
(wrapper `$S/c1run.sh`, `$S/ablate.sh`):

```
/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
  --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
  /usr/bin/env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOME=$S/<label>/home \
    LANG=C.UTF-8 LC_ALL=C.UTF-8 TMPDIR=$S/tmp PYTHONHASHSEED=<seed> PYTHONDONTWRITEBYTECODE=1 \
  /usr/bin/python3 <lane>/plans/round42_c1_verify.py --lane <lane> --work $S/<label>/w --jobs <n>
```
`date +%T` and the bin digest were written into each `<label>/meta.txt` by the wrapper itself (outside bwrap,
before/after). Nested bwrap (the counter's own `ro_sandbox`) worked under this outer envelope: `run1` alone made
275 inner sandbox runs (29 reference + 29 null + 9 anchor mutants × 18 anchor fixtures + 5 order mutants × 11
order fixtures), plus at most 14 traced re-runs.

## R1 — determinism and byte-equality

| run | seed | `--jobs` | wall (meta) | exit | `MUTANTS` line |
|---|---|---|---|---|---|
| run1 | `PYTHONHASHSEED=1` | 1 | 18:03:48 → 18:04:00 | 0 | `total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0` |
| run2 | `PYTHONHASHSEED=99` | 8 | 18:03:48 → 18:03:52 | 0 | same |

`run1` and `run2` were launched **concurrently** on separate `--work` roots and both exited 0.

Command for the comparison (`mf-c1` = the C1 block of `.ufo/waves/round-42/integrate/measure-final.txt`,
command line and `exit=` lines stripped, `--lane/--work` values masked):

```
awk '/^\$ python3 plans\/round42_c1_verify.py/,/^\$ python3 plans\/round42_c2_verify.py/' measure-final.txt |
  grep -v '^\$ ' | grep -v '^exit='  > mf-c1.txt
diff mf-c1.norm run1/out.txt     -> no output  "C1_BYTE_EQUAL_MEASURE_FINAL"
diff run1/out.txt run2/out.txt   -> no output  "IDENTICAL12"
sha256sum run1/out.txt run2/out.txt mf-c1.norm -> 2d509638f3dc89ba41f44dadb668e97bdddb0861ed064a0eab4a95a3225cd15f (all three)
```

So: all 50 stdout lines, byte-equal across
* two different hash seeds and job counts,
* a different clone path (`/fast/scratch/.../F42C1Rerun/lane` vs the L1's `/fast/scratch/.../L1/...`),
* a different `$HOME` (`$S/<label>/home`, a fresh empty dir) and `TMPDIR`,
* a narrower outer envelope (my `/home/vgpnk/.local/bin` `--ro-bind` vs the L1's whole-`/home/vgpnk` `--ro-bind`).

Including `MUTANT` attribution lines (`by=`/`attributed=L…`/`hits=`) and `PINS`/`PINS-AFTER`
(`total=2 mismatched=0`, `PINS-AFTER mismatched=0`), `BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0`,
`ADVERTISED direct=13 indirect=1 none=0`, `PREDICATE C1 pass`. The landing measurement is reproducible from a
clean clone at the docs commit under an independently-built envelope.

## R2 — battery42 module ablation (is every module load-bearing?)

Method: for each module `m`, a minimal lane (`anchor_digest_check.py`, `order_check.py`, `round42_c1_verify.py`,
`battery42/` minus `m.py`) in `$S/ablate/$m`, then the **default** invocation (no `--battery-dir`, no `--only`,
`--jobs 8`, `PYTHONHASHSEED=7`) so the real predicate is evaluated. Pins untouched, so the only changed input is
the battery.

| module removed | fixtures left | mutants flipped to `SURVIVED` | by-tool floors | predicate |
|---|---|---|---|---|
| `a_class.py` | 23 (−6) | X6, X14 | anchor=7/9 order=5/5 | fail |
| `a_route.py` | 23 (−6) | X1, X3, X12 | anchor=6/9 order=5/5 | fail |
| `a_row.py` | 23 (−6) | X9, X13, X15 | anchor=6/9 order=5/5 | fail |
| `o_clause.py` | 24 (−5) | XO1, XO3 | anchor=9/9 order=3/5 | fail |
| `o_scan.py` | 23 (−6) | XO5, XO6, XO7 | anchor=9/9 order=2/5 | fail |

6+6+6+5+6 = 29 fixtures; each removal leaves `BATTERY fixtures=N wrong=0 tampered=0 sidechannel=0`, so the
remaining fixtures still pass — the removal is surgical, not a build break. Every one of the five modules owns at
least two of the 14 kills, and removing it drops the predicate to `fail` (exit 1). **5/5 load-bearing.**

Two ablation-specific observations:

* **X7 is double-covered, not orphaned.** In the full run it is killed by `a_class-x7-fabricated-token` at
  `hits=6`. With `a_class.py` removed it is *still* killed, by `a_row-x13-staged-capture` at `hits=4`; in the other
  four ablations it is killed by `a_class-x7-fabricated-token` — `hits=6` for `a_route`, `o_clause` and `o_scan`,
  `hits=2` for `a_row`. The integers reconcile: of X7's six exhibits in the full battery, 4 come from `a_row`
  fixtures and 2 from `a_class` fixtures, so dropping `a_row` leaves 2 and dropping `a_class` leaves 4;
  `a_route` contributes none. Either module alone suffices to kill X7.
  The other 13 mutants do flip (2+3+3+2+3 = 13 flips, and the 13 are distinct).
* **A kill can migrate rather than disappear** (`X7` above). Attribution names the *first* hit that satisfies the
  span check, so a `by=` value is witness-order-dependent across batteries, while `killed` is not.

## R3 — fail-closed on untrusted input (operability)

Lane copy with one byte appended to `plans/order_check.py` (pin mismatch), everything else intact:

```
PINS total=2 mismatched=1 first=plans/order_check.py
MUTANT XO1 order rc-silence invalid -- ...        (likewise XO3, XO5, XO6, XO7 -> invalid)
MUTANTS total=14 killed=9 survived=0 invalid=5 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=9/9 order=0/5
PINS-AFTER mismatched=1
PREDICATE C1 fail                    exit=1
```

The mutated tool's mutants are marked `invalid` and are **not** counted as killed; the untouched tool still scores
9/9. The counter fails closed and does not silently renormalise its floors.

## Finding F1 — the Q32 receipt line `ls -A ~/.local/bin | sha256sum` is not self-comparable

Not a C1 defect: a defect in the receipt *format* every seat is told to carry. The same directory, same content,
one `mtime`, three invocations (`$S/bindigest-evidence.txt`):

```
dir /home/vgpnk/.local/bin mtime=2026-10-26 17:48:46.564447073 -0300   (unchanged throughout)
gnu_ls_en_US   77408cab9a10361a9f6025bab21f5f07933d94ce46e6a10b9117805d58811c11
gnu_ls_C       8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52
shell_builtin  8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52
LC_ALL=C sort(parent.ls) = LC_ALL=C sort(child.ls) = 8cf5b15…   (the two listings are permutations)
```

Cause: `/usr/bin/ls` sorts with `LC_COLLATE` (`en_US.UTF-8` here); the harness shell's `ls` is a shell builtin and
sorts bytewise. I hit this live: my pre-run probe printed `8cf5b15…` (builtin), the wrapper scripts printed
`77408ca…` (GNU ls), and the post-run probe printed `8cf5b15…` again — three values, zero writes, because
`~/.local/bin`'s mtime never moved and the two listings sort to the same digest.

Recommendation for the house rule (wave-3 / QUALITY Q32): pin both binary and locale, e.g.
`LC_ALL=C /usr/bin/ls -A /home/vgpnk/.local/bin | sha256sum` — or drop the ordering entirely with
`LC_ALL=C sort`. As written, a seat that takes its "before" digest in an interactive shell and its "after"
digest from a script will report a phantom tamper, and the reverse pairing can mask a real one (insert/delete of a
name that collates next to a neighbour still changes length, but a swap of two existing names does not).

Within my own runs the digests are comparable (same wrapper, same binary): **start and end digests are identical in
all 7 envelope invocations** — `77408ca…` for `run1`, `run2` and the 5 ablations — so none of my runs wrote to
`~/.local/bin`.

## Host safety

* `~/.local/bin`: digest constant `77408ca…` before and after each of the 7 invocations
  (`run1-meta.txt`, `run2-meta.txt`, `ablate-*-meta.txt`); directory mtime still `17:48:46`, i.e. no entry was
  created or removed in it during this seat's activity.
* Original lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`: never written. All work was in `$S/lane`
  (verified `rev-parse --show-toplevel` = `$S/lane` before every run); no `git add/commit/checkout/reset/stash`,
  no jj command. Its `HEAD` is now `3e8a2e5e19d638378175adbc11ffce150e57f0b5` (the lane has moved past the
  assigned docs commit; noted, not touched, not attacked).
* Scratch cleanup: `run1/w`, `run2/w`, `ablate/*/w` and `$S/tmp` are all empty after the runs — the counter's
  `finally: shutil.rmtree(root)` removed every `k42-c1-*` root; nothing left under `/tmp`.
* Writes confined to `$S` and the report dir (104 KiB of receipts). Nothing copied in from `corpus/` or `plans/`
  except the 100 KiB `*.txt` receipts listed below; no receipt over 1 MiB.

## Risks / limits of this seat

* Ablation is module-granular by assignment. It proves each **module** is load-bearing; it does not prove each
  **fixture** inside a module is. `a_class-x7-*` is demonstrably redundant with `a_row-x13-*` (X7), which is
  redundancy, not dead weight, but a fixture count like `fixtures=29` is not by itself 29 independent witnesses.
* I did not re-litigate the wave-1 limits (span-check vacuity for 8/14; the `log.showSignature`/`gpg.program`
  fixture vector; the writable tmpfs hidden lane; the `core.worktree` redirect). They stand as reported and are
  untouched by this re-measure: determinism says nothing about whether the spans are non-vacuous.
* `wall` times are the wrapper's own `date +%T` stamps; they are observations, not a cost claim (and `run1`/`run2`
  overlapped, so neither is a clean single-run timing).
* Byte-equality is against `measure-final.txt` as committed in the landing tree; if that file is regenerated from a
  different battery or a later commit, the equality claim no longer applies.

## Evidence (all under `.ufo/waves/round-42/falsify/F42C1Rerun/`)

| file | sha256 |
|---|---|
| `run1-out.txt` | `2d509638f3dc89ba41f44dadb668e97bdddb0861ed064a0eab4a95a3225cd15f` |
| `run2-out.txt` | `2d509638f3dc89ba41f44dadb668e97bdddb0861ed064a0eab4a95a3225cd15f` |
| `measure-final-c1-normalized.txt` | `2d509638f3dc89ba41f44dadb668e97bdddb0861ed064a0eab4a95a3225cd15f` |
| `run1-meta.txt` / `run2-meta.txt` | `a8ffec2b…` / `a5ce9d81…` (see dir) |
| `ablate-{a_class,a_route,a_row,o_clause,o_scan}-out.txt` | `b0d445c2…`, `acc80d53…`, `219b3dc1…`, `970be4bc…`, `6154b73d…` |
| `ablate-*-meta.txt` | `5c4a66a5…`, `1cf85da4…`, `07d7325d…`, `9df6ba15…`, `1c19486c…` |
| `tamper-pinmismatch-out.txt` | `5022fe57cb586c6d32ba6cfa7e5bf168b1d3540af2fa3927abb0ba7612bece57` |
| `bindigest-evidence.txt` | `9255a2c106df7ded4b556fdb9243f6cbc59e5385ecb9c6c8b2becb668cf08f81` |

Reproduction: the two wrapper scripts I used (`$S/c1run.sh`, `$S/ablate.sh`) lived only in scratch and were deleted
with it (547.7 MiB, via `plans/scratch_guard.py safe-rm`; round-root sentinel and sibling dirs untouched). §Setup
carries the exact envelope and argument vector, and the ablation is `cp` the four lane inputs minus one module,
then the same command with `PYTHONHASHSEED=7 --jobs 8`.

VERDICT: c1-rerun-equal-modules-loadbearing-5/5
