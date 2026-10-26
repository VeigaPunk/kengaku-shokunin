# R43BatOrdAlt — battery43 `o_alt`: attributed kills of the three frozen order mutants

Seat: executor, round 43 wave 1. Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only for this
seat); all work done on the clone `$S/lane`
(`S=/fast/scratch/hyaku/kengaku-r43/R43BatOrdAlt`, `git -C "$S/lane" rev-parse --show-toplevel` = that path).

Deliverable (module, stdlib only, no imports at all, 6 fixtures, fids all `o_alt-*`, 180 lines):
`.ufo/waves/round-43/build/R43BatOrdAlt/battery/o_alt.py`
`sha256 8555d3a663d9e58b6a7dcf6c7919dc91a7408deb5195ca41d550ce245e2d6e97`
Receipts: `dev-run2.txt` (`sha256 e995fddc…`), `full-run.txt` (`sha256 0ec4b5c3…`), `lb/*.txt` (12 variant runs).
`dev-run.txt` is the superseded first attempt (one `sidechannel` token left in a docstring, fixed before any result
was used); it is kept as the honest first observation.

Frozen artefacts were read, never touched: `plans/order_check.py` in full, `plans/round43_c1_verify.py` (contract,
`MUTANTS` rows NO5/NO7/NO22, tracer, legs f/g/h/i), `plans/round-43-claims.md`. `PINS total=2 mismatched=0` and
`PINS-AFTER mismatched=0` on every run below. `git -C <source lane> status --porcelain` shows only untracked
`.ufo/waves/round-43/build*/` entries from seats — no `plans/`, `corpus/` or top-level file changed.

## 1. The six fixtures (each one line: what it demonstrates)

| fid | mutant | direction | expect | shape |
|---|---|---|---|---|
| `o_alt-late-case-blob` | NO5 | rc-silence | reject | 4 commits; the `CASE`-shaped line lands in a claims blob **added by commit 3**, buried between 28 lines of prose; receipt at `corpus/evidence/round51/receipts/probe.txt` |
| `o_alt-inplace-gate-rewrite` | NO5 | rc-silence | reject | 5 commits; one claims blob, clean at the freeze commit, **rewritten at commit 4** to carry `P10 ok …` |
| `o_alt-fenced-echo` | NO7 | rc-mirror | accept | 4 commits; a fenced transcript holds the bare `P10 DEFECT receipt unreadable` (control, excused under both) and `gate: P10 DEFECT receipt unreadable: <path>` (the advertised exception) |
| `o_alt-two-echo-blobs` | NO7 | rc-mirror | accept | 5 commits; **two** claims blobs two commits apart, each carrying the echoed excuse with a different path/layout; receipt three directories deep |
| `o_alt-bare-ok-late` | NO22 | rc-silence | reject | 5 commits; a **bare `P10 ok`** (empty detail) added by a later edit of one blob; no `CASE` line anywhere |
| `o_alt-prefixed-ok-blob` | NO22 | rc-silence | reject | 4 commits; `gate: P10 ok fresh probe output is not byte-equal to the receipt` inside a larger blob added later |

`defects` is `[]` in every fixture (`order_check.py` prints no `class=` token; the counter's `classes()` returns
`frozenset()` for `tool != "anchor"`). Every repo is built with `ctx.init(d/<name>)` from nothing; no lane clone,
no path outside `d`; commits go through `ctx.git` (which refuses a repo that is not its own toplevel).

## 2. Development run — the required proof (envelope, clone, `--only NO5,NO7,NO22`)

```
python3 .../plans/round43_c1_verify.py --lane "$S/lane" \
    --battery-dir .../build/R43BatOrdAlt/battery --only NO5,NO7,NO22 --work "$S/w"
```
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r43/R43BatOrdAlt/env /fast/scratch/hyaku/kengaku-r43/R43BatOrdAlt/env --bind /fast/scratch/hyaku/kengaku-r43/R43BatOrdAlt/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round43_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r43/R43BatOrdAlt/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/build/R43BatOrdAlt/battery --only NO5,NO7,NO22 --work /fast/scratch/hyaku/kengaku-r43/R43BatOrdAlt/w
ENVELOPE start 19:09:29 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE o_alt-late-case-blob tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_alt-inplace-gate-rewrite tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_alt-fenced-echo tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE o_alt-two-echo-blobs tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE o_alt-bare-ok-late tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_alt-prefixed-ok-blob tool=order expect=reject declared=- observed_rc=1 observed=- ok
MUTANT NO5 order rc-silence killed by=o_alt-late-case-blob attributed=L120 value=differs hits=4 -- plans/order_check.py:14-16 'FAIL when any file committed under `.ufo/waves/round-NN/claims
MUTANT NO7 order rc-mirror killed by=o_alt-fenced-echo attributed=L60 value=differs hits=2 -- plans/order_check.py:56-57 'The one P10 detail the gate prints before executing anything, 
MUTANT NO22 order rc-silence killed by=o_alt-inplace-gate-rewrite attributed=L105 value=differs hits=3 -- plans/order_check.py:15-16 'a gate `P10` line whose detail is anything other than `receipt
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/0 order=3/3
ADVERTISED direct=3 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 19:09:32 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

The three span lines named by the counter are exactly the three `old` spans in the frozen `MUTANTS` rows:
`order_check.py:120` (`for commit in commits:`), `:60` (`EXECUTED_EXCUSE = re.compile(...)`) and `:105`
(`if m:`) — offsets from my copy are the tool's own lines (`attributed=L120/L60/L105`).

## 3. Load-bearing tables

Two questions were measured separately. (a) Which mutant flips when one fixture is removed? (b) Is each fixture
alone enough? Variant modules are copies of the deliverable with one appended list filter, kept in scratch only
(`$S/lb/<variant>/o_alt.py`), run through the same envelope and the same `--only NO5,NO7,NO22`.

### (a) remove one fixture — nothing flips (deliberate two-per-mutant redundancy)

| removed | NO5 | NO7 | NO22 | evidence |
|---|---|---|---|---|
| `o_alt-late-case-blob` | killed by inplace (hits 3) | killed fenced (2) | killed inplace (3) | `lb/rm-late-case-blob.txt` |
| `o_alt-inplace-gate-rewrite` | killed late-case (3) | killed fenced (2) | killed bare-ok (2) | `lb/rm-inplace-gate-rewrite.txt` |
| `o_alt-fenced-echo` | killed late-case (4) | killed two-echo (1) | killed inplace (3) | `lb/rm-fenced-echo.txt` |
| `o_alt-two-echo-blobs` | killed late-case (4) | killed fenced (1) | killed inplace (3) | `lb/rm-two-echo-blobs.txt` |
| `o_alt-bare-ok-late` | killed late-case (3) | killed fenced (2) | killed inplace (2) | `lb/rm-bare-ok-late.txt` |
| `o_alt-prefixed-ok-blob` | killed late-case (3) | killed fenced (2) | killed inplace (2) | `lb/rm-prefixed-ok-blob.txt` |

Every remove-one run: `BATTERY fixtures=5 wrong=0 tampered=0 sidechannel=0`,
`MUTANTS total=3 killed=3 survived=0 … unattributed=0`, `order=3/3`. So no single fixture is the only thing
holding a mutant down — which is what "at least two fixtures per mutant" buys. What each removal *does* change is
the exhibit count, i.e. that fixture's own kill contribution:

| fixture | exhibits (mutants it flips on its own) | shows up as |
|---|---|---|
| `o_alt-late-case-blob` | NO5 | hits 4→3 on NO5 when removed |
| `o_alt-inplace-gate-rewrite` | NO5, NO22 | NO5 4→3; NO22 3→2 and NO22's killer moves to bare-ok |
| `o_alt-fenced-echo` | NO7 | NO7 hits 2→1 |
| `o_alt-two-echo-blobs` | NO7 | NO7 hits 2→1 |
| `o_alt-bare-ok-late` | NO5, NO22 | NO22 3→2 |
| `o_alt-prefixed-ok-blob` | NO5, NO22 | NO5 4→3, NO22 3→2 |

### (b) one fixture alone — each fixture independently sustains a kill

| fixture alone | fixtures | killed | MUTANT line (receipt) |
|---|---|---|---|
| `o_alt-late-case-blob` | 1 | 1/3 | `NO5 … killed by=o_alt-late-case-blob attributed=L120 value=differs hits=1` (`lb/only-late-case-blob.txt`) |
| `o_alt-inplace-gate-rewrite` | 1 | 2/3 | `NO5` + `NO22 … killed by=o_alt-inplace-gate-rewrite attributed=L105 value=differs hits=1` (`lb/only-inplace-gate-rewrite.txt`) |
| `o_alt-fenced-echo` | 1 | 1/3 | `NO7 … killed by=o_alt-fenced-echo attributed=L60 value=differs hits=1` (`lb/only-fenced-echo.txt`) |
| `o_alt-two-echo-blobs` | 1 | 1/3 | `NO7 … killed by=o_alt-two-echo-blobs attributed=L60 value=differs hits=1` (`lb/only-two-echo-blobs.txt`) |
| `o_alt-bare-ok-late` | 1 | 2/3 | `NO5`, `NO22 … killed by=o_alt-bare-ok-late attributed=L105 value=differs hits=1` (`lb/only-bare-ok-late.txt`) |
| `o_alt-prefixed-ok-blob` | 1 | 2/3 | `NO5`, `NO22 … killed by=o_alt-prefixed-ok-blob attributed=L105 value=differs hits=1` (`lb/only-prefixed-ok-blob.txt`) |

All six solo runs print `fixtures=1 wrong=0 tampered=0 sidechannel=0` and `attributed=… value=differs`
(leg f span executed, leg g site record differs), with the other mutants `SURVIVED exhibits=none` as expected for
a single-shape module.

## 4. Full default counter on the clone (module installed at `$S/lane/plans/battery43/o_alt.py`)

```
ENVELOPE … python3 .../plans/round43_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r43/R43BatOrdAlt/lane --work /fast/scratch/hyaku/kengaku-r43/R43BatOrdAlt/wfull
ENVELOPE start 19:12:44 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE o_alt-late-case-blob tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_alt-inplace-gate-rewrite tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_alt-fenced-echo tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE o_alt-two-echo-blobs tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE o_alt-bare-ok-late tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_alt-prefixed-ok-blob tool=order expect=reject declared=- observed_rc=1 observed=- ok
MUTANT NA1 anchor silence SURVIVED exhibits=none
MUTANT NA5 anchor rc-mirror SURVIVED exhibits=none
MUTANT NA7 anchor rc-mirror SURVIVED exhibits=none
MUTANT NA18 anchor rc-mirror SURVIVED exhibits=none
MUTANT NA20 anchor rc-mirror SURVIVED exhibits=none
MUTANT NA21 anchor rc-mirror SURVIVED exhibits=none
MUTANT NO5 order rc-silence killed by=o_alt-late-case-blob attributed=L120 value=differs hits=4
MUTANT NO7 order rc-mirror killed by=o_alt-fenced-echo attributed=L60 value=differs hits=2
MUTANT NO22 order rc-silence killed by=o_alt-inplace-gate-rewrite attributed=L105 value=differs hits=3
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=9 killed=3 survived=6 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/6 order=3/3
ADVERTISED direct=8 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 19:12:47 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
(The six survivor lines are truncated here only for width; `full-run.txt` carries them in full.) The `anchor=0/6`
survival is exactly the wave-1 division of labour: this module owns `order` only. `order=3/3` is the seat's share of
`MUTANTS-BY-TOOL`.

## 5. Envelope evidence for every run

The 14 receipts quoted in this report (12 variant runs, the development run, the full default run) each carry an
`ENVELOPE end` line; the superseded `dev-run.txt` does too. Grouped over those 14:

```
7 exit=0 before=328be01808ba022f after=328be01808ba022f unchanged
7 exit=1 before=328be01808ba022f after=328be01808ba022f unchanged
```
(6 remove-one runs exit 0 — all three mutants killed; 6 solo runs + the full default run exit 1 — survivors;
the development run exits 0.) No run changed the `~/.local/bin` content digest, so no measurement here is
`INVALID`.

## 6. Not a re-spelling of the freeze-direction module (self-check, for the non-author reviewer)

The freeze module's order shapes are: a 3-commit lane whose `control.txt` is appended with `P10 DEFECT fresh probe
exit=1 cases=16`; and a 2-commit lane whose `control.txt` is one `P10 DEFECT receipt unreadable: plans/round-42-claims.md`
line. Mine differ in every axis the counter cannot see: commit counts (4–5 vs 2–3), claim-dir round numbers
(51–56), file names, blob shapes (28-line prose sandwich, 18-line prose + bare line, fenced block, two blobs),
the trigger text (`CASE` line vs `P10 ok` vs `gate: P10 …` vs echoed excuse with a deeper path), receipt depth
(1–3 directories), and the in-place-rewrite shape (same blob clean→dirty across commits), which the freeze set does
not contain. No module text, fixture body or helper is copied; the copy in `$S/lane/plans/battery43/` is a byte copy
of the deliverable and nothing imports any other battery or claims module.

## 7. Limits named

1. **Kills are result+site-record differences, not intent.** `o_alt-inplace-gate-rewrite`, `o_alt-bare-ok-late` and
   `o_alt-prefixed-ok-blob` each flip NO5 *and* NO22, because a `P10` line added at a later commit violates both
   advertised rules at once. This is disclosed overlap, not an extra mutant: the frozen list is unchanged.
2. **NO5 needs at least two commits touching the claims dir.** A lane with a single claims commit cannot distinguish
   `commits[:1]` from `commits`; my NO5 fixtures therefore all carry 4–5 commits, and the kill's `hits` count depends
   on how many of my blobs carry a hit line (2–4 depending on fixture mix).
3. **Leg g is a locals-digest argument.** The NO7 kill rides on the module frame's globals repr at the next line
   (the compiled pattern text differs), the NO5 kill on the number of loop iterations (record length), the NO22 kill
   on the next line number after `if m:`/`if False:`. A mutation whose only effect were state hidden inside an
   object repr would read `unattributed` (false negative); none of these three is of that kind — `unattributed=0`
   in every run.
4. **No anchor coverage here.** The full default counter still prints `PREDICATE C1 fail` and `anchor=0/6`; the six
   anchor mutants need anchor fixtures from the sibling seats. This module MUST NOT be read as a C1 pass.
5. **Host, not image.** bwrap 0.13.1, host python3, `--jobs 8` default; the module is stdlib-only with zero imports,
   so nothing about it depends on installed packages. Runtimes: ~3 s per counter invocation.
6. **Harness observation (not a lane defect).** With `bash` tool calls whose command nests bwrap, this seat's
   harness returned no stdout and exit 1 while the receipt file was written correctly (compare `dev-run2.txt`, which
   printed, with the later identical solo runs). All numbers above are quoted from the files, not from the terminal.
7. **Scratch was the only writable tree besides `/tmp`**; the clone at `$S/lane` got `plans/battery43/o_alt.py` and
   nothing else. No commit, no push, no lane write, no tool install in this seat (no package was added or upgraded).

Scratch `$S` was removed with `plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r43 R43BatOrdAlt "$S"`
after the receipts were copied here.

VERDICT: battery43-o_alt-killed-3/3-wrong-0
