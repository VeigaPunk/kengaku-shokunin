# F39C1Rerun — the round-39 C1 counter and the post-hoc audit, re-measured at the landing tip (executor, wave 2)

Seat: executor (leaf). Target: re-run the frozen C1 counter `plans/round39_c1_verify.py` and the L1's post-hoc
`plans/round39_c1_audit.py` on a clean clone of `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` under two
interpreters and two `PYTHONHASHSEED` values, and diff the MUTANT/summary lines against
`.ufo/waves/round-39/integrate/measure-final.txt`.

Clone: `/fast/scratch/hyaku/kengaku-r39/F39C1Rerun/lane` — `git rev-parse --show-toplevel` =
`/fast/scratch/hyaku/kengaku-r39/F39C1Rerun/lane`, `rev-parse HEAD` = `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`,
`git status --porcelain | wc -l` = `0` before the first run and after the last. No lane file, no lane jj/Git
state and nothing under `/home/vgpnk/Projects/shokunin` was written; receipts are in this directory.

## 1. Axes named before the work

1. **Reproducibility** — does `measure-final.txt`'s C1 block reproduce from the tip, line for line?
2. **Interpreter / seed independence** — is any printed line an artifact of the 3.14 host, of dict/set
   ordering under a different hash seed, or of a single lucky run?
3. **Truth of the audit's new lines** — can `AUDIT C1 clean` ever read `dirty`, and does `AUDIT
   nondeterministic_kills=0` ever move? (A constant string is a mirror, not a measurement.)
4. **Closure of the wave-1 findings** — do the added checks actually stop A3 (unpinned battery37 file) and A4
   (pins hashed once)?

## 2. Commands (each run is one command; work dirs are fresh)

```
cd $S/lane
PYTHONHASHSEED=<0|12345> python3 plans/round39_c1_{verify,audit}.py --lane . --work $S/w-host-<seed>
PYTHONHASHSEED=<0|12345> uv run -p 3.13 --no-project python plans/round39_c1_{verify,audit}.py \
        --lane . --work $S/w-uv<seed>
```

Tools: `python3` 3.14.8 (host), `uv` 0.13.0 → `cpython-3.13.16`. No install or upgrade was needed, so no pacman,
`uv tool` or binary step was taken.

## 3. The 8 runs are byte-identical to each other and to the landing measurement

| Run | exit | output md5 |
|---|---|---|
| `round39_c1_verify.py`, python3 3.14.8, seed 0 | 0 | `fd581c3068673610469901309f04c902` |
| `round39_c1_verify.py`, python3 3.14.8, seed 12345 | 0 | `fd581c3068673610469901309f04c902` |
| `round39_c1_verify.py`, cpython 3.13.16, seed 0 | 0 | `fd581c3068673610469901309f04c902` |
| `round39_c1_verify.py`, cpython 3.13.16, seed 12345 | 0 | `fd581c3068673610469901309f04c902` |
| `round39_c1_audit.py`, python3 3.14.8, seed 0 | 0 | `983359f537c3a5cfe81377ea2c3079b8` |
| `round39_c1_audit.py`, python3 3.14.8, seed 12345 | 0 | `983359f537c3a5cfe81377ea2c3079b8` |
| `round39_c1_audit.py`, cpython 3.13.16, seed 0 | 0 | `983359f537c3a5cfe81377ea2c3079b8` |
| `round39_c1_audit.py`, cpython 3.13.16, seed 12345 | 0 | `983359f537c3a5cfe81377ea2c3079b8` |

Whole outputs are identical, not only the MUTANT lines: the 90 `FIXTURE` lines, `BATTERY …`, the seven `MUTANT`
lines, `MUTANTS …` and `PREDICATE C1 pass`. That is stronger than the required "diff the MUTANT/summary lines"
and it means no printed line depends on the interpreter (3.13 vs 3.14), on the hash seed, or on run order.
Receipts: `host-0-*.txt`, `host-12345-*.txt`, `uv313-0-*.txt`, `uv313-12345-*.txt`, all eight `.err` files empty.

## 4. Diff against `measure-final.txt`

* `mf-c1-block.txt` — the first `PINS total=26` … to the first `PREDICATE C1 pass` in `measure-final.txt`:
  101 lines, md5 `fd581c30…`. `diff` against my whole verify output: **empty**, i.e. `MUTANT M01`…`M07`
  (`killed by=d5m-n21-manifest-row-2`, `p1m-second-pin-appended-bytes`,
  `p3m39-quote-one-word-above-upper-bound`, `p7m39-s105-two-source-lines`, `p23-p2-receipt-deleted`, `r36-P0`,
  `d5m39-tagged-quote-span`), `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0`, `PREDICATE C1
  pass` all agree.
* `mf-audit-block.txt` — the block after the `round39_c1_audit.py` command line: 104 lines, md5 `983359f5…`.
  `diff` against my whole audit output: **empty**, including `PINS final total=26 mismatched=0`, `AUDIT
  nondeterministic_kills=0`, `AUDIT C1 clean`, `PREDICATE C1 pass`.
* Header caveat (receipt, not an opinion): `measure-final.txt:1` reads `TIP 34158b0ca0f7b527d60af0e612511f7f27aebcbc`,
  one commit *before* the claimed tip. The C1 surface is nonetheless identical at the two commits:
  `git rev-parse 34158b0:<path> a6832f5:<path>` gives the same blob for `plans/round39_c1_verify.py`
  (`415d4cd5…`), `plans/round39_c1_audit.py` (`9f33d9dc…`), `plans/pkg_gate.py` (`544135df…`) and the
  `plans/battery39` tree (`971b3e10…`); `git diff --name-only 34158b0 a6832f5 -- plans corpus` lists only
  `corpus/lessons/round-39.md`. So the measurement is of the claimed code state, but the header line names a
  commit a reader cannot reconcile with `a6832f5` from the header alone.
* `untracked_in_clone=0` in the header matches my clone (`git status --porcelain` = 0 lines).

## 5. Pin set independently re-hashed

The 26 digests declared in `plans/round39_c1_audit.py:71-109` were extracted and re-computed with the system
`sha256sum` in the clone; the two lists (`p-d.txt`, `p-o.txt`) sort-diff empty: **ALL_26_PINS_INDEPENDENTLY_MATCH**.
`PINS total=26 mismatched=0` is therefore not the script grading its own homework.

## 6. Controls — can the audit's new lines move? (each is my module in *my* clone, removed afterwards)

### 6.1 A4 (pin rewrite after the PINS line) — audit catches it, the frozen predicate does not

`a4-control-module.py` placed as `plans/battery39/f39c1_a4pinwrite.py`: one genuine-package fixture whose build
appends a byte to `plans/pkg_gate.py` and `plans/round37_c1_attribution.py`.

```
frozen verify: PINS total=26 mismatched=0 / BATTERY fixtures=91 wrong=0 renamed_disagree=0 sidechannel=0 /
               MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0 / PREDICATE C1 pass   exit 0
               sha256 after: 516facc4… 17ae8b5d…   (pins: ea638822… 7064cf1a…)
audit:         PINS final total=26 mismatched=2 first=plans/pkg_gate.py / AUDIT nondeterministic_kills=0 /
               AUDIT C1 dirty / PREDICATE C1 pass                                             exit 0
```

`a4b-audit.txt`, `a4-verify.txt`. The re-hash at `plans/round39_c1_audit.py:417` is the only line that noticed.

### 6.2 Mid-run `--spec` flip (wave-1 A1 shape) — `nondeterministic_kills` moves

`nondet-control-module.py` placed as `plans/battery39/aa_flipwitness.py`: the M02-witness fixture shape with its
own `--spec` inside the fixture root, plus a detached daemon that waits for `<root>/gates/M01.py` (the audit's
own mutant-phase marker) and then truncates `frozen_instruments` to its first entry, where P1 passes for the
genuine gate and the M02 mutant alike. Marker `2026-10-26T04:46:59.063631 flipped pins=['plans/tb2_grader_probe.py']`.

```
frozen verify: MUTANT M02 P1 silence killed by=f39c1-flip-spec-after-ref / MUTANTS … killed=7 survived=0 /
               PREDICATE C1 pass                                                              exit 0
audit:         AUDIT nondeterministic_kills=1 first=M02:f39c1-flip-spec-after-ref / AUDIT C1 dirty /
               PREDICATE C1 pass                                                              exit 0
```

`nondet-verify.txt`, `nondet-audit.txt`. The audit's re-run of *both* gates on the killing fixture
(`plans/round39_c1_audit.py:395-398`) rejects the kill and falls through to the honest M02 witness; the frozen
counter scores the swapped input as the kill.

### 6.3 A3 (unpinned battery37 module) — the audit refuses, the frozen counter imports it

`plans/battery37/zz_unpinned_a3.py` (an in-process `run_gate` patch):

```
audit:  PINS total=26 mismatched=1 first=plans/battery37/zz_unpinned_a3.py      exit 2
        stderr: AUDIT unpinned battery module present; refusing to import it
verify: PINS total=26 mismatched=0 / BATTERY fixtures=90 wrong=82 … killed=0 survived=7 / PREDICATE C1 fail  exit 1
```

`a3-audit.txt`, `a3-audit.err`, `a3-verify.txt`. (My patch forges every fixture, so the frozen counter fails on
`wrong=82`; I did not rebuild wave-1's targeted version — the receipt needed here is that the counter neither
pins nor refuses an added `plans/battery37` file, while the audit does, at
`plans/round39_c1_audit.py:280-286`.)

### 6.4 Restore — the clean verdict returns byte-for-byte

After removing both modules and restoring the two pinned files from a pristine copy
(`ea638822…`, `7064cf1a…`), the audit output md5 is again `983359f537c3a5cfe81377ea2c3079b8`, identical to the
baseline run (`clean2-audit.txt` vs `host-0-audit.txt`); `git status --porcelain` = 0. Each control result is
therefore attributable to its module, not to clone drift.

## 7. Findings

**F1 — the landing measurement reproduces (calibration credit stands).** 8/8 runs exit 0; the verify block is
101/101 lines and the audit block 104/104 lines identical to `measure-final.txt`, under python 3.14.8 *and*
cpython 3.13.16, under `PYTHONHASHSEED=0` *and* `12345`, and the 26 pins re-hash independently. Nothing in the
receipt depends on the host interpreter or on set/dict ordering.

**F2 — the header of the landing measurement names its parent commit.** `measure-final.txt:1` prints
`TIP 34158b0c…` while the claimed landing tip is `a6832f5`; C1's scripts, gate and battery39 tree are
blob-identical at both, and `a6832f5..master` (`acf4375`) touches only `.ufo/waves/round-39/falsify-*.json`.
The measurement is valid for the claimed tip, but the header does not say so; a seat that only reads line 1
cannot verify the claim without re-deriving the blobs (as §4 does).

**F3 — `AUDIT C1 clean|dirty` is a live measurement but an advisory one.** It moved in both controls
(`dirty` with `mismatched=2`; `dirty` with `nondeterministic_kills=1`) and returned to `clean` byte-identically.
But both dirty runs printed `PREDICATE C1 pass` and **exited 0**: `plans/round39_c1_audit.py:419` computes
`audit_clean = not final and not nondet and not mism`, while the returned predicate at `:425` is
`good = (not mism and …)` — `final` and `nondet` never enter it. The docstring states this intent ("the
predicate below keeps the frozen counter's numbers", `:13`), and the claims' admission rule is the frozen
counter alone (`plans/round-39-claims.md:42-45`), so the audit closes *visibility*, not *admission*: a parent
that keys on exit status or on the `PREDICATE C1 pass` line still admits a run whose kills were rejected as
nondeterministic or whose pins moved during the run.

**F4 — the wave-1 A3 and A4 gaps are closed in the audit, measured, not asserted.** A4: `PINS final
mismatched=2` where the frozen counter printed `mismatched=0` and `pass` (§6.1). A3: `exit 2` plus
`refusing to import it` on an unpinned `plans/battery37` file that the frozen counter imports in-process and
still reports `PINS total=26 mismatched=0` (§6.3).

**F5 — the wave-1 A1 shape still passes the frozen counter at this tip; the named limits do not cover it.**
`plans/round39_c1_verify.py:261` hashes the pins once, before any battery module runs, and nothing re-checks
fixture state between the reference capture and the mutant loop; my §6.2 module therefore gets
`MUTANT M02 … killed by=f39c1-flip-spec-after-ref` and `PREDICATE C1 pass`. The claims' named limits
(`plans/round-39-claims.md:59-61`) cover "a result difference … not the fixture's intent", the side-channel
token heuristic and a child process outliving its parent — none of which is the mechanism here (the input
changed between phases). This is inside the disclosed "battery39 code review by a non-author seat remains part
of admission", but the limit sentence is the wrong one for it.

## 8. Limits of this seat

* All runs are on one scratch clone of `a6832f5` in this guest; the counter's own 900 s child timeout was never
  approached (40–61 s wall per run).
* §6.2 depends on winning a race against the audit's phase transition; it won on the single attempt
  (marker time recorded), keyed on the audit's own `gates/M01.py`, so the window is a whole mutant, not
  microseconds. I did not repeat it.
* §6.3 does not reproduce wave-1's *passing* A3 module — only the pin-set/refusal contrast; the pass claim in
  wave 1 is left as that seat stated it.
* I did not test daemons against `PINS final` timing (i.e. a rewrite that happens after `:417`), nor the
  `--only`/`--battery-dir` dev flags (they print `PREDICATE C1 n/a`).
* No tool installs. Scratch `/fast/scratch/hyaku/kengaku-r39/F39C1Rerun` is removed at the end of this seat;
  every receipt above was copied here first.

## 9. Artifacts (this directory)

Matrix logs: `host-0-verify.txt`, `host-12345-verify.txt`, `uv313-0-verify.txt`, `uv313-12345-verify.txt`,
`host-0-audit.txt`, `host-12345-audit.txt`, `uv313-0-audit.txt`, `uv313-12345-audit.txt`.
Comparison bases: `mf-c1-block.txt` (101 lines), `mf-audit-block.txt` (104 lines), `p-d.txt`/`p-o.txt`
(declared vs recomputed pins). Controls: `a4-control-module.py`, `nondet-control-module.py`, `a4-verify.txt`,
`a4-audit.txt`, `a4b-audit.txt`, `nondet-verify.txt`, `nondet-audit.txt`, `a3-audit.txt`, `a3-audit.err`,
`a3-verify.txt`, `clean2-audit.txt`.

VERDICT: c1-rerun-pass-audit-clean-agree-yes
