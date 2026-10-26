# R39BatP3 — battery39 module for frozen mutant M03 (P3 upper word bound, silence)

Seat: R39BatP3 (wave 1 executor, round 39). Lane repo read-only; all work in a scratch clone.
Scratch: `/fast/scratch/hyaku/kengaku-r39/R39BatP3/` (clone `--shared`, `git -C ... rev-parse --show-toplevel`
verified as the clone path; deleted at the end).

## Deliverable

| item | value |
|---|---|
| module (L1 copies to `plans/battery39/p3m39.py`) | `.ufo/waves/round-39/build/R39BatP3/battery/p3m39.py` |
| sha256 | `fd16681e3ee0bb57e72779026fafccd3c0bf4b1cf603108574a39a297673d497` |
| fixture id | `p3m39-quote-one-word-above-upper-bound` |
| `expect` / `defects` | `reject` / `["P3"]` |
| argv tail | `["package", "--root", <d>, "--require-clean-tree"]` (frozen r35 spec appended by the counter) |
| imports | `pathlib` only; no side-channel tokens (`grep -c -E '/proc\|ppid\|cmdline\|psutil\|environ'` → `0`) |
| gate digest used | `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` (= `PINS`, unmodified) |

## What the fixture is

M03 is `short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi]` →
`... if not lo <= q.words <= hi + 1]` (`plans/round39_c1_verify.py` `MUTANTS` M03; the byte pair occurs exactly
once in the gate), declared direction `silence`: the reference flags a quote one word above the spec's upper
bound, the mutant accepts it. Pre-freeze witness: `.ufo/waves/round-38/falsify/F38XMutP/witness-run.txt` W-X05
(`ref P3,P4,P9 -> mut P4,P9 flip=P3->P3-ok`).

One fixture, one mutant. It builds the GENUINE round-35 package (`ctx.genuine_package`), then replaces the **last**
`## Located quotes` data row with a row whose text is the upper bound **plus one word** —
`entry_rules.quote_words` is `[3, 25]`, so the text is exactly **26 words** — cited at `task.toml:6`.
The 26 words are taken from the fixture's **own copied bytes** (last 26 words of the first capture line carrying
≥26 words) and are a byte substring of that line, so P4 (verbatim) stays `ok` and P3 is the only clause that can
flip. Row count, distinct texts and distinct locations are untouched (22 / 22 / 22 ≫ min 8), so the mutant's P3 is
`ok` on counts as well. Word count, line number and capture name are derived at build time, never hardcoded.

Fixture row exactly as built (`receipt-04-fixture-notes.txt`):

```
| the task states its codon-optimisation and GC constraint objective | “the ability to design a fusion protein gBlock by querying bioinformatics APIs, selecting proteins based on spectral properties, and applying codon optimization with GC content constraints."” | `task.toml:6` |
QUOTE_WORDS 26 VERBATIM_IN task.toml:6
```

Reference vs mutant on the built package, clause notes (same receipt):

```
--- REF rc=1
    P3 DEFECT rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=1
    P4 ok checked=22 bad=0 first=0
    P9 ok untracked=0 first=0
    defects=1
--- M03 rc=0
    P3 ok rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=0
    P4 ok checked=22 bad=0 first=0
    P9 ok untracked=0 first=0
    defects=0
```

So the pair (reference, mutant) satisfies `silence` for P3 with both exits in {0,1}: reference prints
`P3 DEFECT`, the fixture declares `P3`, the mutant prints `P3 ok`. Because P4/P9 are green on both sides, the
mutant's only difference from the reference on this fixture is P3's verdict and the resulting exit flip — the
attribution is not carried by a second broken clause.

Design note (declared, not hidden): the alternative route — a invented 26-word text that is *not* on the cited
lines — was rejected only because it would make P4 fire as well and force `defects=["P3","P4"]`. Both routes are
legitimate under the counter's rule; the verbatim route is strictly more isolated, and the observed defect set is
`{P3}` in either case for the kill test. If a future edit makes the derived capture text unverbatim, the counter
prints `WRONG` on `observed_defects` and the fix is to redeclare `["P3","P4"]` — not to widen the bound.

## Evidence 1 — M03-only development run (predicate n/a, all 87 fixtures sane)

```
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round39_c1_verify.py --lane "$S/lane" \
    --battery-dir .../.ufo/waves/round-39/build/R39BatP3/battery --only M03 --work "$S/w"
FIXTURE p3m39-quote-one-word-above-upper-bound expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
BATTERY fixtures=87 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M03 P3 silence killed by=p3m39-quote-one-word-above-upper-bound -- a quote one word above the spec's upper word bound is a defect [gate docstring 'quote bounds ... come from --spec']
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

exit 0. Full 92-line output, including all 87 `FIXTURE` lines (all `ok`, including every round-36/37/38 line):
`receipt-01-only-m03.txt`. `null_detected=0` (a byte-identical gate copy reproduces every reference result) and
`renamed_disagree=0` (every fixture rebuilt at a renamed path agrees).

## Evidence 2 — load-bearing (delete the fixture in turn → M03 SURVIVED)

`receipt-02-load-bearing.txt`, both legs run with `--only M03`:

```
$ python3 plans/round39_c1_verify.py --lane "$S/lane" --battery-dir $S/nofx --only M03 --work $S/w2
  # (a) same module with `FIXTURES = []` — the fixture deleted in place
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M03 P3 silence SURVIVED exhibits=none -- a quote one word above the spec's upper word bound is a defect [...]
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0

$ python3 plans/round39_c1_verify.py --lane "$S/lane" --battery-dir $S/empty --only M03 --work $S/w2
  # (b) no battery39 module at all
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M03 P3 silence SURVIVED exhibits=none -- a quote one word above the spec's upper word bound is a defect [...]
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
```

`exhibits=none` is the stronger statement: with the fixture gone, M03 differs from the reference on **no**
fixture in **any** declared direction — the module is the sole source of the kill, and no other battery fixture
even moves the word window.

## Evidence 3 — full default counter with the module in `plans/battery39/`

Module copied to `$S/lane/plans/battery39/p3m39.py` (sha256 identical to the deliverable), then run from the
clone root. `receipt-03-full-default.txt`, exit 1:

```
PINS total=26 mismatched=0
FIXTURE p3m39-quote-one-word-above-upper-bound expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
BATTERY fixtures=87 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M01 D5 mirror killed by=d5m-n21-manifest-row-2 -- ...
MUTANT M02 P1 silence SURVIVED exhibits=none -- ...
MUTANT M03 P3 silence killed by=p3m39-quote-one-word-above-upper-bound -- ...
MUTANT M04 P7 silence SURVIVED exhibits=none -- ...
MUTANT M05 RUN rc-silence killed by=p23-p2-receipt-deleted -- ...
MUTANT M06 MAIN rc-mirror killed by=r36-P0 -- ...
MUTANT M07 D5 mirror SURVIVED exhibits=none -- ...
MUTANTS total=7 killed=4 survived=3 invalid=0 null_detected=0
PREDICATE C1 fail
```

This is the expected wave-1 state: M01/M05/M06 are the pre-existing round-36/37/38 kills, **M03 is the kill this
seat adds**, and M02 (P1) / M04 (P7) / M07 (D5) are the other wave-1 seats' assignments. `PREDICATE C1 fail` on
this seat's clone is not attributable to this module (the counter's own `dev` flag reports `wrong=0
renamed_disagree=0 sidechannel=0 null_detected=0`). The full predicate is the L1's post-integration gate.

## Risks / limits

- The fixture's verdict depends on the *last* data row of the genuine table being replaceable; if the landing tip
  changes the round-35 entry's quote table, `rewrite_quotes(...)` still replaces the last row and the row is
  re-derived from the copy — but `P4` would then have to be re-checked (the derivation asserts verbatimness from
  the same bytes, so `defects=["P3"]` stays correct as long as the counter's `WRONG` line is read in admission).
- The quote is taken from `task.toml`, a pinned capture the genuine entry does not otherwise quote (its table
  cites `test_outputs.py`, `test.sh` and `instruction.md`). `task.toml` is `SHA256SUMS`-pinned, so P5's
  "quote capture is pinned in the manifest" holds, and the spec's registry rows are untouched; a reviewer should
  still note that the package under test now quotes a fourth capture file.
- `silence` is declared and proven; this fixture would also satisfy `rc-silence` (mutant exit 0 < reference exit 1)
  but the counter only consults the declared direction, and no relabel is needed.
- Side-channel: module source has zero tokens; the heuristic review by a non-author seat still applies per the
  frozen claims' stated limit.

## Files written

- `.ufo/waves/round-39/build/R39BatP3/battery/p3m39.py` (deliverable)
- `.ufo/waves/round-39/build/R39BatP3/receipt-01-only-m03.txt`, `-02-load-bearing.txt`,
  `-03-full-default.txt`, `-04-fixture-notes.txt`
- `.ufo/waves/round-39/build/R39BatP3.md` (this report)

Nothing under the lane's `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`, `PROVINCE.md`,
`SHONEN.md`, its jj state or its Git index was written; the scratch clone and `/fast/scratch/hyaku/kengaku-r39/R39BatP3`
were removed.

VERDICT: battery39-p3m39-M03-killed-wrong-0
