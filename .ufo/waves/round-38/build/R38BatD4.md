# R38BatD4 — battery38 module `d4m.py` (mutants N19, N20)

Seat: R38BatD4 (executor, wave 1). Scratch: `/fast/scratch/hyaku/kengaku-r38/R38BatD4` (created, used, removed — verified gone).
No lane file was edited; nothing outside my report dir and my scratch dir was written; no mutating git/jj command was run
(only `git clone --shared` into scratch). No tool installed or upgraded.

## Deliverable

- Module: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-38/build/R38BatD4/battery/d4m.py`
- `sha256 4fd34339ab32627b65b2fd7ff11f0d1b99c45b02598c8591468b2badbc0d4488` (`sha256sum` on the deliverable; the copy tested
  in the clone `$S/lane/plans/battery38/d4m.py` hashed identically)
- Stdlib only (`pathlib`, `re`). Both fids carry the seat prefix `d4m-`. Counter side-channel token scan: `tokens: []`
  (`python3 -c "t=open(...).read(); print([x for x in ('/proc','ppid','cmdline','psutil','environ') if x in t])"` → `[]`).

## Mutants and fixtures

Frozen mutant text (`plans/round38_c1_verify.py:132-135`), both `D4 silence`:

- N19 `enumerate(spec["d4"]["patterns"], 1)` → `enumerate(spec["d4"]["patterns"][:-1], 1)` — "every directional pattern is
  checked, the last included"
- N20 `if not re.search(pat, lines[0])]` → `if not re.search(pat, lines[0], re.IGNORECASE)]` — "directional patterns match
  case-sensitively"

Both replacement strings occur exactly once in `plans/pkg_gate.py` (`gate_src.count(old) == 1` for each), so neither mutant is
rejected as `invalid`.

| fid | mutant | line it writes (inside `d`) | why it isolates |
|---|---|---|---|
| `d4m-n19-last-pattern-unmatched` | N19 | genuine D4 correction line with `selftest was green` → `selftest was fine` | only pattern 3 fails, and not by case (IGNORECASE run gives the same match vector), so N20 still fails it |
| `d4m-n20-pattern-case-differs` | N20 | genuine line with ``R34C2CounterDraft.md:8` records`` → ``R34C2CounterDraft.md:8` Records`` | only pattern 1 fails, only by case; N19 checks pattern 1 (it drops only the last) and still fails it |

Both `expect=reject`, `defects=["D4"]`, argv `["d4-line", "--file", <path inside d>]`, no `--spec` (frozen r35 spec appended
by the counter). Each builder re-derives its line from `ctx.d4_line()` and re-checks the premise against
`ctx.spec["d4"]["patterns"]` with `re` — a line that stops isolating its mutant raises instead of passing quietly.

Evidence of the isolation, direct branch runs in the clone (`ref.py` = unmodified `plans/pkg_gate.py`; `N19.py`/`N20.py` =
the two frozen substitutions applied once; `--spec plans/pkg-spec-r35.json`):

```
ref <- n19  rc=1  D4 DEFECT patterns=3 failed=['pattern3']
ref <- n20  rc=1  D4 DEFECT patterns=3 failed=['pattern1']
N19 <- n19  rc=0  D4 ok patterns=3 failed=0
N19 <- n20  rc=1  D4 DEFECT patterns=3 failed=['pattern1']
N20 <- n19  rc=1  D4 DEFECT patterns=3 failed=['pattern3']
N20 <- n20  rc=0  D4 ok patterns=3 failed=0
```

Perfect diagonal: each mutant turns to `D4 ok` only on its own fixture, and each fixture is `D4 DEFECT` on the unmodified
gate — i.e. the declared `["D4"]` equals the observed set (`D4` is the only clause `d4-line` runs).

## Proof run

Clone of the lane tip (`git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r38/R38BatD4/lane`; the
clone carries the module at `plans/battery38/d4m.py`), command exactly:

```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round38_c1_verify.py \
  --lane "$S/lane" --battery-dir "$S/lane/plans/battery38" --only N19,N20 --work "$S/w"
```

exit 0; full output saved at `receipts/c1-N19N20-full.txt` (72 lines) and pasted verbatim:

```
PINS total=14 mismatched=0
FIXTURE r36-P0 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-P1 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P2 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P3 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P4 expect=reject declared=- observed_rc=1 observed_defects=P6 ok
FIXTURE r36-P5 expect=reject declared=- observed_rc=1 observed_defects=P1 ok
FIXTURE r36-P6 expect=reject declared=- observed_rc=1 observed_defects=P9 ok
FIXTURE r36-P7 expect=reject declared=- observed_rc=1 observed_defects=P1,P3,P6,P9 ok
FIXTURE r36-L1 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L2 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L3 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L4 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L5 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE r36-L6 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE d4-m44-file-unreadable expect=reject declared=D4 observed_rc=1 observed_defects=D4 ok
FIXTURE d4-m45-not-one-line expect=reject declared=D4 observed_rc=1 observed_defects=D4 ok
FIXTURE d4-m46-label-not-carried expect=reject declared=D4 observed_rc=1 observed_defects=D4 ok
FIXTURE d5-m48-file-unreadable expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m49-two-lines expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m50-label-altered expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m51-require-missing expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m52-forbid-present expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m53-capture-missing expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE d5-m55-quote-absent expect=reject declared=D5 observed_rc=1 observed_defects=D5 ok
FIXTURE p23-p2-receipt-deleted expect=reject declared=P2 observed_rc=1 observed_defects=P2 ok
FIXTURE p23-p2-receipt-byte expect=reject declared=P2 observed_rc=1 observed_defects=P2 ok
FIXTURE p23-p3-heading-renamed expect=reject declared=P3,P4 observed_rc=1 observed_defects=P3,P4 ok
FIXTURE p23-p3-seven-texts expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
FIXTURE p23-p3-seven-locations expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
FIXTURE p23-p3-two-word-quote expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
FIXTURE p4-no-quote-row expect=reject declared=P3,P4 observed_rc=1 observed_defects=P3,P4 ok
FIXTURE p4-capture-unreadable expect=reject declared=P4,P5 observed_rc=1 observed_defects=P4,P5 ok
FIXTURE p4-line-outside expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
FIXTURE p4-one-char-off expect=reject declared=P4 observed_rc=1 observed_defects=P4 ok
FIXTURE p5-manifest-absent expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-manifest-unparsed-line expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-capture-bytes-stale-digest expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-row-capture-unpinned expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-manifest-digest-off-pin expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-quote-cites-unpinned expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p5-extra-capture-file expect=reject declared=P5 observed_rc=1 observed_defects=P5 ok
FIXTURE p6-m20-registry-row-duplicated expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m21-row-with-twelve-cells expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m22-url-off-the-pinned-raw-path expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m23-row-tier-b expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m24-row-status-queued expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m25-used-by-another-path expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m26-five-word-teaches-cell expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p6-m27-two-identical-teaches-cells expect=reject declared=P6 observed_rc=1 observed_defects=P6 ok
FIXTURE p7-m28-entry-deleted expect=reject declared=P3,P4,P7,P8 observed_rc=1 observed_defects=P3,P4,P7,P8 ok
FIXTURE p7-m29-source-url expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p7-m30-verified-at expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p7-m31-recheck-line expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p7-m32-negative-heading expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p7-m33-falsifier-word expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p8-readme-deleted expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p8-index-row-duplicated expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p8-index-row-missing-sid expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p8-coverage-bullet-removed expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p8-extra-knowledge-file expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p910-not-a-git-repo expect=reject declared=P9 observed_rc=1 observed_defects=P9 ok
FIXTURE p910-receipt-deleted expect=reject declared=P10,P2 observed_rc=1 observed_defects=P10,P2 ok
FIXTURE p910-probe-exits-1 expect=reject declared=P1,P10 observed_rc=1 observed_defects=P1,P10 ok
FIXTURE p910-receipt-one-byte expect=reject declared=P10,P2 observed_rc=1 observed_defects=P10,P2 ok
FIXTURE d4m-n19-last-pattern-unmatched expect=reject declared=D4 observed_rc=1 observed_defects=D4 ok
FIXTURE d4m-n20-pattern-case-differs expect=reject declared=D4 observed_rc=1 observed_defects=D4 ok
BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N19 D4 silence killed by=d4m-n19-last-pattern-unmatched -- every directional pattern is checked, the last included [F37XMutD4 X3]
MUTANT N20 D4 silence killed by=d4m-n20-pattern-case-differs -- directional patterns match case-sensitively [F37XMutD4 X4]
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

`BATTERY fixtures=66` = the frozen round-36 battery (14) + battery37 (50) + my 2; `renamed_disagree=0` is the counter's
relocated-directory run (my fixtures build paths from the directory handed in, so they move with it);
`null_detected=0`; `PINS total=14 mismatched=0` on the cloned tip.

## Load-bearing table

Each fixture deleted in turn (module copied to a fresh dir with that one `FIXTURES` entry removed), same command, same clone:

| kept | N19 | N20 | evidence |
|---|---|---|---|
| both (deliverable) | killed by `d4m-n19-last-pattern-unmatched` | killed by `d4m-n20-pattern-case-differs` | `receipts/c1-N19N20-full.txt` (`killed=2 survived=0`) |
| drop `d4m-n19-…` | **SURVIVED** | killed by `d4m-n20-…` | `receipts/c1-drop-n19.txt` (`killed=1 survived=1`, exit 1) |
| drop `d4m-n20-…` | killed by `d4m-n19-…` | **SURVIVED** | `receipts/c1-drop-n20.txt` (`killed=1 survived=1`, exit 1) |
| drop both (empty battery dir) | SURVIVED | SURVIVED | `MUTANTS total=2 killed=0 survived=2`, exit 1 |

Each fixture is load-bearing for its own mutant and for nothing else; no fixture is redundant.

## Note on the fixture design (measured, not assumed)

A first draft made `d4m-n20-…` differ in case inside the *last* pattern. That line also fails only the last pattern for a
non-case reason, so the N20 fixture killed **both** mutants and the N19 fixture became redundant (drop-N19 run printed
`N19 … killed by=d4m-n20-pattern-case-differs`). The delivered version moves the case difference into pattern 1, which N19
still checks; the diagonal above (two independent deletion runs) confirms the separation. Both premises are asserted inside
the builders, so a future spec change that collapses them raises rather than silently re-couples.

## Risks / limits

- The two fixtures were proved with `--battery-dir` (a dev run: `PREDICATE C1 n/a`). The full predicate needs the other
  wave-1 seats' modules in `plans/battery38/`; my module depends on nothing but `ctx.d4_line()`, `ctx.spec`, and the lane's
  `SCORECARD.md` line the round-36 helper already reads.
- N19's advertised sentence is "the last included": pattern order is spec data (`spec["d4"]["patterns"]` has 3 entries), so the
  fixture isolates the last entry by index, as the mutant does.
- Attribution is the counter's, not mine: both kills are `silence` on clause `D4`, family `d4-line`, declared set `["D4"]`
  equal to the reference's observed set.

VERDICT: battery38-d4m-killed-2/2-wrong-0
