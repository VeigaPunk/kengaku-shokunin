# F39MutBattery — battery39 fixture-level mutation battery (kengaku round 39, wave 2 FALSIFY)

Seat F39MutBattery, 2026-10-26. Attack target: the 4 frozen battery39 fixtures (p1m→M02, p3m39→M03,
p7m39→M04, d5m39→M07) through the frozen C1 counter's own fixture/kill machinery. Lane tip measured:
`a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` (branch master), clean clone at
`/fast/scratch/hyaku/kengaku-r39/F39MutBattery/lane`, `git -C "$S/lane" rev-parse --show-toplevel` verified
equal to the clone before any write; every git call named `-C "$S/lane"`; no commit, no lane write.

Method: 4 modules × 3 one-line mutants applied with `edit` to scratch copies of `plans/battery39/`
(variant **D** declared defects changed, **R** defining edit removed, **M** edit moved to the first item /
below the bound), then the same bounded detector on pristine, each mutated copy — and byte-restored
evidence for the lane. Detector per run (cwd = the clone):

    python3 plans/round39_c1_verify.py --lane "$S/lane" --battery-dir "$S/bat-<V>" --work "$S/work-<V>"

`--battery-dir` keeps the counter's round-36+37+38 fixtures untouched and swaps only the battery39 source
dir; the mutant list and gate stay frozen (counter pins re-verified every run: `PINS total=26 mismatched=0`
in all 7 runs). The counter never mutates battery modules; mutated module copies live only in `$S/bat-*`.

## Baseline (pristine copy, full mutant set) — conclusive

`bat-base` = byte copy of `plans/battery39/` at the tip. 25.4 s, rc=0
(receipt `F39MutBattery/base.txt`):

    PINS total=26 mismatched=0
    BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0
    MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
    PREDICATE C1 n/a (non-default battery or mutant subset)

and `MUTANT M02 ... killed by=p1m-second-pin-appended-bytes`, `M03 ... by=p3m39-quote-one-word-above-upper-bound`,
`M04 ... by=p7m39-s105-two-source-lines`, `M07 ... by=d5m39-tagged-quote-span` — byte-equal attributions to
`.ufo/waves/round-39/integrate/measure-final.txt`. The harness is sound; every mutant result below is a
counter verdict, not a setup artifact.

## The 12 mutants and what caught them

"caught-by wrong" = a `FIXTURE ... WRONG` line (`plans/round39_c1_verify.py:324` `wrong += not ok`);
"caught-by kill" = the module's target mutant printing `SURVIVED` instead of `killed by=<fid>`
(`plans/round39_c1_verify.py:375,378`). All line references to module files are pristine-tip line numbers;
full diffs are receipts `F39MutBattery/mut-<V>-<module>.patch`.

| # | module | variant | one-line mutant (file:line) | counter output (receipt run-<V>.txt) | caught by |
|---|--------|---------|------------------------------|--------------------------------------|-----------|
| 1 | p1m | D | `p1m.py:39` `"defects": ["P1"]` → `["P9"]` | `FIXTURE p1m-second-pin-appended-bytes expect=reject declared=P9 observed_rc=1 observed_defects=P1 WRONG`; `MUTANT M02 P1 silence SURVIVED exhibits=rc-silence` | wrong + kill |
| 2 | p3m39 | D | `p3m39.py:71` `"defects": ["P3"]` → `["P4"]` | `FIXTURE p3m39-... declared=P4 observed_rc=1 observed_defects=P3 WRONG`; `M03 ... SURVIVED exhibits=rc-silence` | wrong + kill |
| 3 | p7m39 | D | `p7m39.py:62` `"defects": ["P7"]` → `["P9"]` | `FIXTURE p7m39-... declared=P9 observed_rc=1 observed_defects=P7 WRONG`; `M04 ... SURVIVED exhibits=rc-silence` | wrong + kill |
| 4 | d5m39 | D | `d5m39.py:93` `"defects": []` → `["D5"]` | `FIXTURE d5m39-tagged-quote-span expect=accept declared=D5 observed_rc=0 observed_defects=- WRONG`; `MUTANT M07 D5 mirror killed by=d5m39-tagged-quote-span` (kill retained) | wrong only |
| 5 | p1m | R | `p1m.py:34` `f.write_bytes(f.read_bytes() + OFF_PIN)` → `pass` | `FIXTURE p1m-... declared=P1 observed_rc=0 observed_defects=- WRONG`; `M02 ... SURVIVED exhibits=none` | wrong + kill |
| 6 | p3m39 | R | `p3m39.py:66` `entry.write_text(ctx.r36.rewrite_quotes(...))` → `pass` | `FIXTURE p3m39-... declared=P3 observed_rc=0 observed_defects=- WRONG`; `M03 ... SURVIVED exhibits=none` | wrong + kill |
| 7 | p7m39 | R | `p7m39.py:54` `second = (f"source: {SID} ...` → `f"note: {SID} ...` | `FIXTURE p7m39-... declared=P7 observed_rc=0 observed_defects=- WRONG`; `M04 ... SURVIVED exhibits=none` | wrong + kill |
| 8 | d5m39 | R | `d5m39.py:80` `after = _mark_quote_span(before, d5["quote"])` → `after = before` | fixture line stays `ok` (accept fixture still accepts — no WRONG); `MUTANT M07 D5 mirror SURVIVED exhibits=none` | kill only |
| 9 | p1m | M | `p1m.py:31` `rels[1]` → `rels[0]` (edit moved to the FIRST pinned instrument, the one M02 still checks) | fixture `ok` (`observed_rc=1 observed_defects=P1`); `M02 ... SURVIVED exhibits=none` | kill only |
| 10 | p3m39 | M | `p3m39.py:48` `want = ... + 1` → `want = int(rules["quote_words"][1])` (quote at, not above, the bound) | `FIXTURE p3m39-... declared=P3 observed_rc=0 observed_defects=- WRONG`; `M03 ... SURVIVED exhibits=none` | wrong + kill |
| 11 | p7m39 | M | `p7m39.py:57` `lines[:i + 1] + [second] + lines[i + 1:]` → `lines[:i] + [second] + lines[i:]` (second source line moved before the pinned line) | fixture `ok` (`observed_rc=1 observed_defects=P7`); `M04 ... SURVIVED exhibits=none` | kill only |
| 12 | d5m39 | M | `d5m39.py:80` `after = "<b>F39MutBattery probe</b>" + before` (markup moved to the first item of the file, off the quote span) | fixture `ok`; `MUTANT M07 D5 mirror SURVIVED exhibits=none` | kill only |

Run summaries (each with `BATTERY fixtures=90 renamed_disagree=0 sidechannel=0`, `PINS total=26 mismatched=0`,
`PREDICATE C1 n/a (non-default battery or mutant subset)`, exit 1):

    run-D:  BATTERY ... wrong=4   MUTANTS total=7 killed=4 survived=3 invalid=0 null_detected=0
    run-R:  BATTERY ... wrong=3   MUTANTS total=7 killed=3 survived=4 invalid=0 null_detected=0
    run-M:  BATTERY ... wrong=1   MUTANTS total=7 killed=3 survived=4 invalid=0 null_detected=0

Bonus 13th probe (variant R2, p7m39 only): literal deletion of the insertion,
`p7m39.py:57` → `return "\n".join(lines) + "\n"`, makes the entry edit a no-op; the counter refuses to
evaluate instead of passing (receipt `F39MutBattery/run-R2.txt`, exit 2):

    SETUP module battery39/p7m39.py failed to build (rc=1): ...
        raise RuntimeError("entry edit was a no-op")

So a literal no-op removal is fail-closed by the module's own build guard (`p7m39.py:38`) plus the
counter's SETUP path (`plans/round39_c1_verify.py` `SETUP ... return 2`), and the variant-7 semantic
removal is what the wrong/kill lines actually catch.

## Verdict tally

- caught (either mechanism): **12/12** — every one-line module mutant produces a named, attributable
  anomaly line (fixture fid and/or mutant id) and flips the run exit 0→1 (or →2 for the R2 SETUP abort).
- caught by the `WRONG` fixture line alone would be 8/12: variants D×4, R×3 (p1m, p3m39, p7m39), M×1
  (p3m39). Missed by `wrong`: #8, #9, #11, #12 — the accept-side edit removal and every position move that
  keeps the package red; for those, `wrong=0` and only the kill line sees the mutation.
- caught by the kill-line flip alone would be 11/12: all except #4. d5m39-D keeps M07 killed because the
  mirror direction never consults the declared set — `plans/round39_c1_verify.py:244`
  `return clause in ref[2] and clause in mut[1]  # mirror` — so only the fixture-vs-reference check at
  `:324` sees a mislabelled accept fixture. The converse holds for silence kills: relabelling a reject
  fixture (`declared = set(fx["defects"])` at `:241`) both wrongs it and disarms its kill, which is why
  #1–#3, #5–#7, #10 are caught twice.
- The two mechanisms are complementary; neither is sufficient alone. The frozen predicate sentence
  (plans/round-39-claims.md:43-44 `BATTERY fixtures=<n> wrong=0 ... MUTANTS total=7 killed=7 survived=0`)
  requires both halves to be zero, and the dev exit (`wrong == 0 and ... and survived == 0 ...`,
  `plans/round39_c1_verify.py:384-386`) fires on either.

Additional no-harm evidence, same runs: `renamed_disagree=0` and `null_detected=0` in baseline, D, R, M —
no mutated fixture induces path dependence or gate nondeterminism; `exhibits=` on every survivor names the
direction it did exhibit (`rc-silence` for #1–#3, `none` otherwise), so a mislabelled direction would be
visible in the receipt (Q29). Re-runs of D, R, M after all other work (`F39MutBattery/rerun-<V>.txt`) are
byte-identical to the first runs — the detector is deterministic on these inputs.

## Findings (receipts, not opinions)

1. No coverage gap found at this layer: all 12 one-line mutants are caught and attributed. The battery39
   fixtures are not gameable by a single line at the fixture level the way the wave-1 in-process/daemon
   attacks (A1/A3/A4/A5) were at the counter level.
2. Residual asymmetry worth recording: `d5m39` is the only module whose mutant (#4) survives the kill
   machinery — a mislabelled accept fixture would keep `killed=7` green forever if the `wrong` check were
   ever dropped. Symmetrically, p1m-M / p7m39-M / d5m39-R / d5m39-M would keep `wrong=0` green if the
   direction-checked kill were dropped. The frozen predicate needs both.
3. Position moves that keep the reference red and stay inside the mutant's narrowed view (first pin for
   M02, list order for M04's element-0 read) are invisible to `wrong`; they surface only as
   `SURVIVED exhibits=none`. Any future coverage claim for battery39 should quote the SURVIVED line, not
   the BATTERY line, as the sensitive signal.

## Restoration evidence

- Pristine module sha256 (pre-mutation, from the tip clone): d5m39
  `cb2edc678ccba64123694e7cf74f06a2990f72d9ca8b4025c1670ce828840538`, p1m
  `a82fa251ca1bd4041d8bec2badac3e6fe3ba53f2f1427baee685b5571e0c1c3e`, p3m39
  `fd16681e3ee0bb57e72779026fafccd3c0bf4b1cf603108574a39a297673d497`, p7m39
  `2c228ba8d4ceeb6f5311be5e8b7df98971e3ac287003b6520aa3e486c0558d2e`.
- Post-run sha256 of the same lane files: identical (recomputed after all 7 counter runs).
- `git -C "$S/lane" status --porcelain | wc -l` → `0`; `git -C "$S/lane" rev-parse HEAD` →
  `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`; toplevel = the scratch clone. No lane file, index, or jj
  state touched; all mutants and gate copies lived in `$S/bat-*` and the counter's `--work` roots, which
  the counter digest-checks and removes itself.
- Mutated-copy after-hashes (12 + R2) recorded in the transcript; diffs are the receipts
  `F39MutBattery/mut-*.patch`. Scratch `/fast/scratch/hyaku/kengaku-r39/F39MutBattery` deleted after the
  receipts were copied out; no process left running (`pgrep` clean mid-run, all work roots self-removed).
- Tooling: nothing installed or upgraded (existing python 3.14.8, git, coreutils only).
- Harness note (filed to report_issue): several `bash` calls returned empty captured stdout (and once
  `error: failed to redirect to <target>: No such file or directory (os error 2)`) while the redirected
  receipt files themselves were written completely; all evidence above was re-read from the receipts, and
  re-runs confirmed them byte-identically.

Receipts (relative to kengaku-shokunin): `.ufo/waves/round-39/falsify/F39MutBattery/{base,run-D,run-R,run-M,run-R2,rerun-D,rerun-R,rerun-M}.txt`, `.ufo/waves/round-39/falsify/F39MutBattery/mut-{D,R,M}-{p1m,p3m39,p7m39,d5m39}.patch`, `.ufo/waves/round-39/falsify/F39MutBattery/mut-R2-p7m39.patch`.

VERDICT: battery39-mutants-caught-12/12
