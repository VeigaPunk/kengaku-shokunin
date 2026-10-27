REV 42d5043afac952fcb43bf4798757785dd258cf85

# R46W2Lesson — attack on `corpus/lessons/round-46.md` (round 46, wave 2, falsify)

Lane tip `42d5043afac952fcb43bf4798757785dd258cf85`, clean `--no-local` clone at
`/fast/scratch/hyaku/kengaku-r46/R46W2Lesson/lane` (`rev-parse --show-toplevel` = clone dir; HEAD verified).
Every number below carries the command that produced it. No counter, fixture build or probe was run; all
work is reads over the lane plus network re-fetches into scratch. Host-safety rule honored (nothing written
outside scratch and this seat's report paths). Tools installed: none.

## Check 1 — `## Mistakes`: 10 rows, each with class / evidence / captured-by / fix shown able to fail

Structure: 10 rows, every row has a bold class, a command-level evidence cell, a captured-by cell (Q-rule or
"none" + why), and a fix with a red/green demonstration. Per-row verification at the tip:

1. **LOG rewrite in place (D1).** Reproduced: `git diff -U0 fbad1c5 3d9ea54 -- LOG.md` → hunks
   `@@ -1374 +1374 @@` and `@@ -1388 +1388 @@` (plus the append hunk `@@ -1392,0 +1393,22 @@` = the attempt-3
   note). `grep -cF '(A/B runs byte-equal)' LOG.md` → `1`, `grep -cF 'advertised fixture fence closed (10/10
   refused, 104 honest admitted)' LOG.md` → `1` — red 0/0 at the mistake, green 1/1 now: the correction entry
   exists (`LOG.md:1423` quotes the diff command; `:1426` old heading with `4290d64`/`3d9ea54`; `:1444`
   current line). Fix shown able to fail ✔.
2. **Gate with no per-row quote (D2).** Reproduced the strict parse exactly: round-45 →
   `admit_rows=8 without_quote_and_line=8`; round-46 → 16 gate rows (7 ACCEPT + 9 superseding), 0 without
   quote/line. ✔
3. **Receipts without `REV` (D3).** Evidence reproduced: `^REV [0-9a-f]{40}$` counts on the three round-45
   receipts = `0, 0, 0`. Fix partially realized — see **Finding F1**.
4. **Unnamed claims-file edits (D4).** `git rev-list fd4129eb..HEAD -- plans/round-46-claims.md` →
   `4fdeebaa546c…` only; the file names `cf7de6af` (instruments) and cannot name `4fdeeba` (carries the
   naming paragraph) — the row's stated limit is honored: the lesson header and `LOG.md:1455-1456` both name
   `4fdeebaa`. ✔
5. **Seats without report files.** Round-46 w1 close is green on its own check: `w1-results.json` →
   `results=35 seats=35 output None=0`, and `test -f` over all 35 seats → 35/35 reports present. ✔
6. **`teaches` paraphrase (S154→S163).** `'among guesses'` absent from the round-45 README capture (python
   `in` check → False); S163's quote is byte-exact at `README.md:31` of a 33-`splitlines()` capture (file has
   no trailing newline, so `wc -l` says 32 — the row's "33 lines" is the splitlines count and is right).
   Old S154 untouched (diff shows insertions only). ✔
7. **Predictor lone-CR (Q38).** The entry's Predictor block now reads
   `text.replace("\r\n", "\n").replace("\r", "\n")` — universal newlines; landing leg B
   `states=16 grader_pass=10 grader_fail=6 disagree=0` (`integrate/c2-landing.txt`); `## Errata (round 46)`
   present, `errata_marks=5/5`; the two red controls (`disagree=6`, `disagree=4`) are committed as
   `control-c2-*-replay.txt` at `4fdeebaa`. ✔
8. **V7 unsatisfiable tag set.** Verified from `polyglot-c-py-dry-cases-freeze.txt`: TAG lines = {single-file,
   python-run, c-build, both-print, fib-kth, stdout-only, toolchain}; union of `violates=` covers all but
   `both-print` and `toolchain` → V7 can never pass, exactly as claimed; `integrate/c3-landing.txt` prints
   `V7 DEFECT … tags missing=['both-print', 'toolchain']`. Fix landed as Q40 leg 1 (`corpus/QUALITY.md:1091`). ✔
9. **Pre-receipt control ran the probe.** `claims/control-c3-echo.txt:15` is verbatim
   `` gate: P10 DEFECT fresh probe output is not byte-equal to the receipt `` (line 15, as cited);
   `integrate/c3-landing.txt`: `V8 DEFECT order_exit=1`, `ORDER HIT …@4fdeebaa546c:15 kind=gate-p10`,
   `ORDER RESULT FAIL`. Fix landed as Q40 leg 2 (`QUALITY.md:1092-1093`). ✔
10. **Misrooted seat report.** `.ufo/waves/round-46/w1/R46CritC1Freeze.md` exists in the lane; fleet
    `.tower/quarantine/fleet-root-strays-20261027T0600/` contains `kengaku-shokukin`. ✔

Header tokens all resolve: `fd4129e` (stage 1), `cf7de6a` (stage-2 instruments; did **not** touch the claims
file — consistent), `4fdeeba` (amendment; claims file +26 lines, control receipts + runner), `7768716c`
("C1 stage-2 control receipts (21 controls, all `PREDICATE C1 fail`; base fence contradicted=22/32)").

## Check 2 — `## Gate`: URL + access date + ≤25-word located quote per new row (D2); ≥1 admit, ≥1 reject

- 9 new rows: 7 ACCEPT (S166–S172) + 2 REJECT (Docker Hub tag page; unpinned `main`). Every row has a URL
  (abbreviated `…2fd12b88…` with the expansion legend directly under the table) and `accessed 2026-10-27`.
  ≥1 admit (7) and ≥1 reject (2). ✔
- **All 7 ACCEPT quotes byte-exact at their cited lines** in the retained captures (raw reads):
  `test_outputs.py:27`, `test.sh:26`, `instruction.md:9` (ASCII apostrophe, exact), `solve.sh:14`,
  `Dockerfile:6`, `task.toml:34`, `README.md:22`. All ≤25 words (largest 9 whitespace tokens).
- **Drift re-measured today (2026-10-27):** `sha256sum -c SHA256SUMS` → 8/8 OK; independent
  `curl -fsSL` of all 8 files at the pin → 8/8 byte-identical to the captures; `main` instruction.md →
  byte-identical, `wc -c` = **339** — reproducing the REJECT row's "200, 339 bytes, byte-identical" claim.
- C2 superseding table (S157–S165): every cell matches the committed `corpus/SOURCES.md` rows (quote,
  location, words, capture lines, cited range; kinds corrected to `docs` in S159/S163/S165). Spot-verifications:
  S157 live fetch → 90 lines, `:87` = `matches = re.findall(pattern_text, log_text, re.MULTILINE)`, sha256
  `345c3bd0…` = row = retained round-36 capture; S160 `:30`, S161 `:17`, S164 `:63` raw-verified;
  round-45 capture set `sha256sum -c` → 9/9 OK. The receipt the section cites
  (`w1/R46ScribeC2Rows/receipt-live-reopen.txt`) exists and opens with `REV 42d5043a…`. ✔
- The two REJECT rows carry a located status/token cell instead of a document quote; row 2's fix and Q3 scope
  the quote rule to **admit** rows, so this is consistent, not a D2 violation (observation O3).

## Check 3 — old→new log of mutable-cell changes

`git diff 64ba8385 42d5043 -- corpus/SOURCES.md` → **16 insertions, 0 deletions, 0 modifications**: old rows
S108, S149–S156 keep every cell (status `mined`, `used-by` unchanged), so the lesson's "no mutable cell
changed, so there is no old→new log line; precedent S025/S036, S054/S064" is accurate. Entry-side corrections
carry `## Errata (round 46)` (leg C `errata_marks=5/5`). Tip census `^ {0,3}\| *S[0-9]{3}` = 165 rows, matching
the Census section; `claims/census-before.txt` shows 15 `W04` + `kengaku ok` + exit 0. ✔

## Findings by severity

**F1 (minor) — Mistake row 3's fix mechanism is not implemented anywhere in the lane.** The fix column states
"The harness that writes each receipt prepends `REV <40-hex>`". At the tip: `grep -cE '^REV [0-9a-f]{40}$'` is
**0** on all four `integrate/` receipts (they name the revision as `# … at lane commit 420eec9f…` /
`e9d2014…` header prose) and the 21+ stage-2 control receipts (written by `claims/stage2_controls.py`) carry
`# measured HEAD cf7de6af…` — no `REV` string at all; a scan of `plans/*.py` finds no tool that writes `REV`
lines. Only wave-2 sibling receipts (`w2/R46W2C2Rows/live-reopen.txt:1`, `revision.txt:1`) use the format.
D3/Q22 substance — every receipt a claim cites names the revision it measured — holds everywhere checked
(landing headers, control headers, w2 receipts); the defect is the fix sentence's factual claim versus the
round's own receipts, on which the row's own check stays red 0-per-receipt.

**Observations (not defects).** O1: landing receipts measure `420eec9f` (C1) and `e9d2014` (C2/C3/noharm), not
the tip; verified via `git diff --stat` that every post-run commit touches no counter input (C1 inputs
420eec9f→tip: empty; e9d2014→tip plans/corpus delta: QUALITY +21, corpus README +2, lesson +76,
routed-findings +11, `plans/log_appendonly.py` +271 new) — the "landing tip" predicate is carried by
input-immutability, not a re-run at `42d5043a`. O2: rows 2/3/4 fixes are probe-demonstrated rules, not landed
instruments — disclosed by the wave-1 seat itself (`w1/R46ScribeMistakes.md`: "demonstrated by scratch
fixtures, not by a landed gate"). O3: see Check 2.

## Residual risk and verification gaps

- I did not re-run the frozen counters (none needed for this item); landing receipts are taken as committed
  evidence, cross-checked for internal consistency, exact-quote match to the claims' predicate lines
  (`PINS 65`, `REFUSALS 20`, `SEALED 12`, `HONEST 104`, `CALIBRATION advertised=32`, C2 `checks=4 defects=0`,
  C3 `checks=13 defects=2`, `PREDICATE C3 fail`), and input-immutability after the runs.
- Remote re-fetch is a point-in-time measurement from this host on 2026-10-27; the pin remains the 180-day
  anchor, as the `main` REJECT row itself argues.
- Round-45 historical evidence (a3w1 seats with `output: None`) is taken from the committed round-45 results
  file as cited; not independently re-derivable.

## Receipts

Command transcript and decisive outputs: `.ufo/waves/round-46/w2/R46W2Lesson/verification-log.txt`.

VERDICT: lesson-defects-1
