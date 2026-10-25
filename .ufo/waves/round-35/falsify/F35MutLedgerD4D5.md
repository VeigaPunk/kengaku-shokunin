# F35MutLedgerD4D5 — wave 2 falsify: mutation-test r34_d4 / r34_d5 on the landed round

Target: kengaku round 35 wave 2 (falsify), seat F35MutLedgerD4D5 (executor). Lane tip
`dfee6fff631ebc5f623ba4506e5c7992a215401c` (master), frozen claims
`plans/round-35-claims.md` (freeze `11d64530`). Checker under attack:
`plans/defect_ledger.py` `r34_d4` / `r34_d5` (C2 calibration predicate).

## Baseline (landed tip, read-only in lane)

`python3 plans/defect_ledger.py --lane .` → `rows=5 closed=5 observed_pass=5 mismatches=0`,
`PREDICATE C2 pass`, exit 0. `python3 plans/round35_c1_verify.py --lane .` →
`checks=6 defects=0`, `PREDICATE C1 pass`, exit 0. C1 is out of this seat's scope; none of the
mutants below touch C1 surfaces (SCORECARD.md, round-34 build reports, round-34/35 lessons, the
nec-s091-reopen.html capture are not read by the C1 counter).

## Method (fixture rule)

```
D=$(mktemp -d /tmp/k35f-XXXX)
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone 'corpus/**' 'plans/**' 'SCORECARD.md' '.ufo/waves/round-34/**'
git -C "$D/lane" checkout -q dfee6fff631ebc5f623ba4506e5c7992a215401c
# `git rev-parse --show-toplevel` == "$D/lane" verified before any write
```

Each mutant was applied to the pristine clone with the `edit` tool, then run:

```
cd "$D/lane" && python3 plans/defect_ledger.py --lane .
```

Full stdout of every run is retained verbatim in
`.ufo/waves/round-35/falsify/F35MutLedgerD4D5/m<1..6>-*.txt` and `p1-false-green-line.txt`.
No lane file was edited; no git/jj mutation ran in the lane; no tools installed; fixture removed
(`rm -rf`).

## D4 mutants (SCORECARD correction line / round-34 draft line 8)

`r34_d4` reads `R34C2CounterDraft.md[7]` and `R34MutC2Harness.md[11:13]` (observation), then
requires exactly one `SCORECARD.md` line starting `- **D4 correction (round 34 C2):**` that
contains all four tokens `R34C2CounterDraft.md:8`, `cases=10 failed=0`,
`R34MutC2Harness.md:12`, `SELFTEST green failed`.

| mutant | edit | ledger result | killed |
|---|---|---|---|
| M1 | remove `cases=10 failed=0` from the D4 correction line (fixture `SCORECARD.md:1176`) | `R34-D4 status=closed observed=fail agree=NO correction_lines=1` → `rows=5 closed=5 observed_pass=4 mismatches=1`, `PREDICATE C2 fail`, exit 1 | yes |
| M2 | duplicate the D4 correction line | `R34-D4 status=closed observed=fail agree=NO correction_lines=2` → same red tail, exit 1 | yes |
| M3 | change `R34C2CounterDraft.md:8` `SELFTEST cases=10 failed=0` → `cases=10 failed=1` | `R34-D4 status=closed observed=fail agree=NO observation changed: cited draft/harness lines no longer hold` → exit 1 | yes |

## D5 mutants (erratum / round-35 Mistakes row / capture quote)

`r34_d5` tag-strips+flattens `nec-s091-reopen.html` and requires the staged quote; requires
exactly one `round-34.md` line starting `Erratum (round 35):` containing `nec-s091-reopen.html`
and `present`; requires a `round-35.md` §Mistakes row starting `|` and containing `S091`.

| mutant | edit | ledger result | killed |
|---|---|---|---|
| M4 | remove `present` from the erratum (`round-34.md:45`: "is present in" → "is located in") | `R34-D5 status=closed observed=fail agree=NO erratum_lines=0 r35_mistake_row=True` → exit 1 | yes |
| M5 | move the S091 Mistakes row out of the table (`round-35.md:25` leading `|` → `-`) | `R34-D5 status=closed observed=fail agree=NO erratum_lines=1 r35_mistake_row=False` → exit 1 | yes |
| M6 | corrupt the staged quote in `nec-s091-reopen.html:276` (sentence → `QUOTE_REMOVED`) | `R34-D5 status=closed observed=fail agree=NO observation changed: quote not in nec-s091-reopen.html` → exit 1 | yes |

## P1 probe — one FALSE but well-labelled D4 line (claims the harness was green)

Replaced the honest correction line with a line that asserts the opposite of the truth while
containing every required token:

```
- **D4 correction (round 34 C2):** the mutation harness's selftest was green — `R34MutC2Harness.md:12` shows no `SELFTEST green failed` line, and the counter draft's selftest at `R34C2CounterDraft.md:8` records `SELFTEST cases=10 failed=0`.
```

Result:

```
R34-D4 status=closed observed=pass agree=yes correction_lines=1
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
```

**exit 0 — the false line passes the full C2 counter.** The `r34_d4` check is pure token
co-occurrence; it never asserts direction, so a correction line that says the harness was green
(the negation of the defect record — `R34MutC2Harness.md:12-13` actually reads `SELFTEST green
failed (1)`, exit 1) certifies the D4 closure. This confirms on the landed bytes the weakness
wave-1 `R35CritC2` predicted, and it is a live hole in the frozen predicate: the D4 correction
text can be wrong in the exact dimension the defect is about (green vs red selftest) and the
counter still passes.

## Counts

Killed 6/6 required mutants (M1–M6 each turn the frozen C2 predicate red: `PREDICATE C2 fail`,
exit 1, `mismatches=1`). Probe P1 (false-but-labelled D4 line) survives: it is accepted by the
counter — not a kill, a documented weakness. No other row flipped in any run (D1/D2/D3 stayed
green everywhere; D1 remained green because fixture clones are clean and the mutated files are
tracked).

## Risks / notes

- D4/D5 checks verify token presence, not direction; the honest repair (exact quoted order, `is
  present`) is also accepted, so the falsifier is the false-but-labelled text, not the honest one.
- D5's observation half is genuine (quote is present in the capture); a capture edit (M6) is
  caught. Only the self-assessment text checks accept lies.
- C1 counter untouched; C2 output lines are the only gate this seat exercised.

VERDICT: d4d5-killed-6/6
