# R46ScribeMistakes — round-46 lesson `## Mistakes` draft + LOG correction entry (scribe, wave 1)

Scope: draft the `## Mistakes` rows for `corpus/lessons/round-46.md` from the round-45 non-author closure
(`corpus/lessons/round-45-verifier-spotcheck.md` D1–D6 and §2) plus the round-45 lesson, and draft the append-only
LOG.md correction entry for closure D1. **Draft only** — no lane file was written, no frozen file touched, no frozen
counter executed. Sources read in full: the round-45 closure, `plans/round-46-claims.md`, `corpus/lessons/round-45.md`,
`corpus/SOURCES.md` rows S152–S154, `corpus/knowledge/tb2-password-recovery-grader.md`, `plans/round-46-claims.md`
stage-1 file, `plans/round46_c2_verify.py` (read, not run), `plans/anchor_line_check.py` docstring (read, not run),
the round-45 integrate receipts, `.ufo/waves/round-45/a3w1-results.json`.

Order-rule compliance: no repaired fence was run; `plans/round46_c2_verify.py` and `plans/anchor_line_check.py` were
not executed (their committed stage-1 control receipts were read instead); no C3 task case was run; nothing was built.

## Measurements (every number below carries its command)

One probe run under the round-46 envelope, 6 red/green classes:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46ScribeMistakes/env /fast/scratch/hyaku/kengaku-r46/R46ScribeMistakes/env --bind /fast/scratch/hyaku/kengaku-r46/R46ScribeMistakes/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /fast/scratch/hyaku/kengaku-r46/R46ScribeMistakes/mistakes_probe.py /fast/scratch/hyaku/kengaku-r46/R46ScribeMistakes/work
ENVELOPE start 02:13:40 cwd=/home/vgpnk/Projects/shokunin
MISTAKE-LEG log-appendonly red red_fixture=today_log old_heading=0 old_ab=0
MISTAKE-LEG log-appendonly green green_fixture=log+correction old_heading=1 old_ab=1 diff_cmd=True
MISTAKE-LEG gate-per-row-quote red red_fixture=round-45.md admit_rows=8 without_quote_and_line=8
MISTAKE-LEG gate-per-row-quote green green_fixture=two_quoted_rows admit_rows=2 without_quote_and_line=0
MISTAKE-LEG receipt-names-revision red red_fixture=round-45 receipts measure-final.txt=0 a3-tip-c1.txt=0 a3-tip-c2.txt=0
MISTAKE-LEG receipt-names-revision green green_fixture=one_rev_line rev_lines=1
MISTAKE-LEG claims-amendment-named red red_fixture=round-45_claims post_freeze_commits=2 unnamed=2 first=9271dda
MISTAKE-LEG claims-amendment-named green green_fixture=claims+naming sentence unnamed=0
MISTAKE-LEG seat-report-present red red_fixture=a3w1 seats=34 without_report=2 first=R45MutC1Instrument2
MISTAKE-LEG seat-report-present green green_fixture=two_reports without_report=0
MISTAKE-LEG teaches-quote-verbatim red red_fixture=S154 teaches_quote='exists and contains the correct password among guesses' in_capture=False capture_lines=33
MISTAKE-LEG teaches-quote-verbatim green green_fixture=S154_superseding_quote in_capture=True
MISTAKE-LEGS total=6 red_ok=6 green_ok=6
ENVELOPE end 02:13:43 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

Receipt: `R46ScribeMistakes/mistakes-probe.txt` (1904 B, sha256 `3e3a0d12…`); probe source:
`R46ScribeMistakes/mistakes_probe.py` (8550 B, sha256 `042a2564…`). The probe reads the lane read-only and writes only
under the scratch `work/` directory.

Independent measurements used for the rows (not from the probe):

| command | observed |
|---|---|
| `git diff -U0 fbad1c5 3d9ea54 -- LOG.md` | 2 hunks: `@@ -1374 +1374 @@` (heading) and `@@ -1388 +1388 @@` (the A/B sentence), plus a 22-line append at `@@ -1392,0 +1393` |
| `grep -cF '(A/B runs byte-equal)' LOG.md` | `0` |
| `grep -cF 'advertised fixture fence closed (10/10 refused, 104 honest admitted)' LOG.md` | `0` |
| `grep -n 'advertised fixture fence closed' LOG.md` | `1393:` — the appended note, truncated with `…` |
| `grep -cE '^REV [0-9a-f]{40}$'` on the three `integrate/` receipts | 0, 0, 0 |
| `grep -nE '[0-9a-f]{40}' .ufo/waves/round-45/integrate/measure-final.txt` | one hit, `:4 FENCE plans/fixture_fence.py sha256=ac65c032…` (a file digest, not a revision) |
| `git log --format='%h %ad %s' --date=format:'%H:%M' -- plans/round-45-claims.md` | `b4fcd35 21:24` (freeze), `52d7486 23:20`, `9271dda 23:42` |
| commit clocks `b4fcd35 21:24 / 52d7486 23:20 / 05b02e2 23:27 / 7d062c0 23:40 / 9271dda 23:42` | the second claims edit (23:42) **post-dates** the first recorded probe run (23:27) |
| `git show <rev>:plans/round-45-claims.md \| grep -c 9271dda` for revs b4fcd35, 9271dda, 52d7486, 3d9ea54, HEAD | `0` at every rev; `grep -c 52d7486` also `0`; `grep -c 7d062c0` → `1` at 9271dda and later |
| `git diff -U0 b4fcd35 52d7486 -- plans/round-45-claims.md` | `@@ -71 +71 @@` `rows S149–S157` → `rows S149–S156` |
| `grep -n 'states=48' .ufo/waves/round-45/integrate/a3-tip-c2.txt` | `24:V11 ok states=48 grader_pass=18 grader_fail=30 disagree=0` |
| `grep -n 'universal' corpus/knowledge/tb2-password-recovery-grader.md` | `150`, `194` (prose); `def predict` at `197` |
| `grep -n 'among guesses' corpus/evidence/round45/tb2-password-recovery/README.md` | exit 1, no hit; `wc -l` = 32, `splitlines()` = 33; the sentence `is among the recovered passwords` is at `:31` |
| `tail -6 .ufo/waves/round-46/claims/control-c2-nothing.txt` | `B predictor states=16 grader_pass=10 grader_fail=6 disagree=6 DEFECT` |
| `sed -n '1,8p' .ufo/waves/round-46/claims/control-c2-splitlines.txt` | `B predictor states=16 grader_pass=10 grader_fail=6 disagree=4 DEFECT` |
| `python3` strict parse of `corpus/lessons/round-45.md` `## Gate` | 8 rows with verdict cell `admit`, 0 carrying a quoted span, 0 carrying `:N` |

## Draft `## Mistakes` table for `corpus/lessons/round-46.md`

Rows 1–5 are the five required classes (D1–D4 plus the predictor overclaim); rows 6–7 carry the remaining
closure findings (D6, D5) because both recur as the same classes. `captured-by` names a QUALITY criterion or `none`;
`none` appears twice (rows 4 and 5).

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **A committed round entry rewritten in place** — commit `3d9ea54` rewrote two lines the round-45 entry committed at `4290d64`: the heading at `LOG.md:1374` and the "A/B runs byte-equal" sentence at `LOG.md:1388`. The appended attempt-3 note (`LOG.md:1393`) names the old heading only with an ellipsis, so the superseded bytes left the file. | `git diff -U0 fbad1c5 3d9ea54 -- LOG.md` (hunks `@@ -1374` and `@@ -1388`); `grep -cF '(A/B runs byte-equal)' LOG.md` → `0`; `grep -cF 'advertised fixture fence closed (10/10 refused, 104 honest admitted)' LOG.md` → `0`; closure D1 | **R1** (`corpus/QUALITY.md:161`) — its check is `grep -c '<old value>'` = 1, and it was never run at the close | Append the correction entry drafted below (it quotes both old and new lines and the diff command) and leave the rewrite standing; shown able to fail: on today's `LOG.md` the two old strings count `0/0` (red) and `1/1` once the entry is appended (green) — probe leg `log-appendonly`. |
| **A lesson `## Gate` with no per-row quote, location or word count** — `corpus/lessons/round-45.md` `## Gate` admits 8 rows and not one carries a ≤25-word quote or a `:N` location; the quotes exist only in the SOURCES `anchor` cells, three of which cite the wrong line. | strict parse of the Gate table: `admit_rows=8 without_quote_and_line=8`; closure D2; rule at `corpus/QUALITY.md:31-33` | **Q3** — the rule is written and prose-only; nothing parses the Gate table, so a Gate whose reasons are unquoted paraphrases passes | Each admit row carries `<file>:<N> "<quote>" (<K> words)`; shown able to fail: the same parse reddens 8/8 on round-45 and greens a two-row fixture (`without_quote_and_line=0`) — probe leg `gate-per-row-quote`. |
| **Counter receipts that do not name the revision they measured** — the three round-45 receipts embed no commit; the only 40-hex token is the fence sha256, a fact about a file rather than about the tree, and attribution (`8f9a898`, `fbad1c5`) is report prose only. | `grep -cE '^REV [0-9a-f]{40}$'` on `integrate/measure-final.txt`, `integrate/a3-tip-c1.txt`, `integrate/a3-tip-c2.txt` → 0 each; `measure-final.txt:4 FENCE … sha256=ac65c032…`; closure D3 | **Q22** (`corpus/QUALITY.md:257`) — "every receipt a claim cites must name the revision it was produced at"; no receipt was parsed for it | The harness that writes each receipt prepends `REV <40-hex>` (a receipt-byte change, not an edit to a frozen counter); check `grep -cE '^REV [0-9a-f]{40}$'` = 1 per receipt; red 0/3 on the round-45 receipts, green on a one-line fixture — probe leg `receipt-names-revision`. |
| **Post-freeze claims-file edits left unnamed, one of them after the first data run** — `plans/round-45-claims.md` was edited at `52d7486` (23:20) and again at `9271dda` (23:42), the latter after the first recorded probe run `05b02e2` (23:27); neither commit token appears anywhere in the file at the tip, and the `Freeze amendments` paragraph's only commit token is `7d062c0`, which never touched this file. | `git log --format='%h %ad %s' -- plans/round-45-claims.md` (3 commits); commit clocks above; probe `post_freeze_commits=2 unnamed=2 first=9271dda`; `git diff -U0 b4fcd35 52d7486 -- plans/round-45-claims.md` → `@@ -71` `S149–S157` → `S149–S156` | **none** — no QUALITY check reads a claims file's amendments (Q25's naming leg covers frozen instruments only); the round-45 file states the naming rule about itself and nothing enforces it | Round 46 declares the same rule (`plans/round-46-claims.md`: "Any other edit of this file after this commit is named … in a `Freeze amendments` paragraph"), so the close runs a check over `git rev-list fd4129eb..HEAD -- plans/round-46-claims.md` requiring every prior post-freeze commit's 7-hex to appear in the file; red on round-45 (`unnamed=2`), green with the naming sentence — probe leg `claims-amendment-named`. Limit: the commit that carries the naming paragraph cannot name itself, so the lesson or LOG must name it. |
| **Dispatched seats that leave no report file while the results record points at one** — two `a3w1` mutation-testers ended `output: None` with the note "read the seat report file in the wave dir"; one directory holds artifacts and no `.md`, the other no directory at all, so the C1-instrument and C2-check mutation items are unattacked. | `.ufo/waves/round-45/a3w1-results.json` (`R45MutC1Instrument2`, `R45MutC2Checks`); probe `seats=34 without_report=2`; `.ufo/waves/round-45/a3w1/R45MutC1Instrument2` holds `hostile mut receipts` only | **none** — Q19 records yield rows per dispatched seat, not report presence; no criterion makes "the report file exists" a check | Wave close runs `test -f .ufo/waves/round-N/<wave>/<seat>.md` over the results file and names every miss in the wave report; red 2/34 on a3w1, green on a two-report fixture — probe leg `seat-report-present`. |
| **A `teaches` cell quoting a paraphrase the source does not contain** — S154 `teaches` quotes 'exists and contains the correct password among guesses'; the README capture has no such string (the authors' words at `README.md:31` are "is among the recovered passwords"), and the same row's anchor cites `README.md:1-46` in a 33-line file. | `grep -n 'among guesses' corpus/evidence/round45/tb2-password-recovery/README.md` → exit 1; probe `in_capture=False capture_lines=33`; `corpus/SOURCES.md:169`; closure D6 | **Q3** — a quote may narrow, never widen; the row passed the gate because nothing compares a `teaches` quote with the capture (the anchor-line class is then on its second round, so Q30 binds the check) | Supersede S154 under Q34 with the verbatim `:31` sentence (round-46 C2 rows S157–S165); shown able to fail: `grep -F` of the old span reddens and of the new span greens — probe leg `teaches-quote-verbatim`. |
| **A `## Predictor` presented as the grader's exact rule that diverges on lone CR** — the prose at `:150` and `:194` says `read_text` runs universal-newline mode while the predictor block at `:197` implements `text.replace("\r\n", "\n")`, so three lone-CR states grade True and predict False; the round-45 V11 leg printed `disagree=0` because its generator never built a lone-CR state. | `corpus/knowledge/tb2-password-recovery-grader.md:150,194,197`; `integrate/a3-tip-c2.txt:24` (`states=48 … disagree=0`); closure §2 C2 (in-memory `C+"\ra"`, `"x\r"+C`, `"x\n\r"+C`); round-46 stage-1 controls `B … disagree=6` (`control-c2-nothing.txt`) and `disagree=4` (`control-c2-splitlines.txt`) | **Q38** (`corpus/QUALITY.md:1027`) — the executed-state leg existed and its state set did not separate the two readings | Round-46 C2 leg B over 16 frozen newline states (lone CR, LF-CR, CR-CR-LF, VT/FF/NEL/LS, CRLF controls) plus a `## Errata (round 46)` mark naming `lone-CR`; shown able to fail: two wrong predictors are red at base (6 and 4 disagreements) and the split `grader_pass=10 grader_fail=6` is non-vacuous. |

Row count 7; `captured-by` = `none` on 2 (the unnamed post-freeze claims edit; the reportless seats).

## LOG.md correction entry (append-only draft for D1)

Append at the end of `LOG.md` (no committed line edited):

````
### Round 45 LOG correction (round 46, 2026-10-27) — two round-45 lines rewritten in place; superseded bytes restored here (closure D1)

`corpus/lessons/round-45-verifier-spotcheck.md` D1: commit `3d9ea54` rewrote two lines of the round-45 entry that
`4290d64` committed. LOG.md is append-only (QUALITY R1) and the rewrite is left standing in the history — this entry
restores the superseded bytes as text, so `grep -c` on them returns 1 again. Diff command and both hunks:

```
git diff -U0 fbad1c5 3d9ea54 -- LOG.md
```

Old heading (committed `4290d64`, rewritten `3d9ea54`; LOG.md:1374):

```
## Round 45 (hyaku run 9, 2026-10-26) — advertised fixture fence closed (10/10 refused, 104 honest admitted); eleventh TB2 grader executed (second F1 exemplar)
```

Current heading (LOG.md:1374):

```
## Round 45 (hyaku run 9, 2026-10-26/27) — fixture fence landed, its frozen counter also passed by a path-keyed control (C1 not admitted); eleventh TB2 grader executed (second F1 exemplar; C2 predicate met, routed defects)
```

Old line (committed `4290d64`, rewritten `3d9ea54`; LOG.md:1388):

```
  counter `checks=11 defects=0`, `PREDICATE C2 pass` (A/B runs byte-equal); V11 `states=48 grader_pass=18
```

Current line (LOG.md:1388):

```
  counter `checks=11 defects=0`, `PREDICATE C2 pass` (A/B runs equal on every non-`ENVELOPE` line; not byte-equal — envelope scratch dirs/times differ; corrected attempt 3); V11 `states=48 grader_pass=18
```

The appended attempt-3 note at LOG.md:1393 names the old heading only in truncated form ("advertised fixture fence
closed (10/10 refused …)") and the round-45 lesson records both corrections again; neither restores the bytes.
````

Shown able to fail (probe leg `log-appendonly`): today `grep -cF` of each old string is `0`; with this entry appended
to a scratch copy they are `1` and `1` and the diff command is present. So the entry is what makes R1's check
(`grep -c '<old value>'` = 1) green, and deleting either quoted old line turns it red again.

## Conflicts reported verbatim (for the canonical judge)

1. Closure D4 (`corpus/lessons/round-45-verifier-spotcheck.md:48-49`) says: "the \"Freeze amendments\" paragraph
   names only `9271dda`." Measured at the tip (`HEAD` = `fd4129eb`, and at `3d9ea54`): `grep -c 9271dda
   plans/round-45-claims.md` → `0`, `grep -c 52d7486` → `0`, `grep -c 7d062c0` → `1`. The paragraph names no
   claims-file edit; the one commit token it carries (`7d062c0`) does not touch the file
   (`git log -- plans/round-45-claims.md` lists `b4fcd35`, `52d7486`, `9271dda` only). The draft row states the
   measured version, not the closure's sentence.
2. The same D4 sentence calls `52d7486` the whole change and "pre-data, 23:20 before the first probe run 23:27". A
   second claims-file edit exists at `9271dda` (23:42), i.e. 15 minutes **after** that probe run; the closure does not
   name it as post-data.
3. My first loose parse of the round-45 `## Gate` counted 10 "admit" rows because the word `admit` also appears in two
   reject rows' flip conditions; a strict verdict-cell parse gives 8 admit rows (S149–S156), which is the count used
   in row 2.

## Limits / out of scope

- Draft only. The L1 integrates the table into `corpus/lessons/round-46.md` and appends the LOG entry; this seat wrote
  no lane file beyond its two allowed paths. `git status --porcelain` in the lane: 0 modified tracked files, 8
  untracked entries, all wave artefacts under `.ufo/waves/round-46/` (this report and its subdir included).
- The Gate quote rule (row 2) and the receipt `REV` line (row 3) are demonstrated by scratch fixtures, not by a landed
  gate; neither is a frozen round-46 instrument, and adding `REV` to a frozen counter would be an instrument
  amendment, which is why the fix is placed in the harness that writes receipts.
- Row 5's fix is an operator/orchestrator-side inventory check (wave results file vs report files); the two a3w1 seats
  are unrecoverable per the closure, so the row records the class, not a rerun.
- Not re-executed by this seat: `plans/round45_c1_verify.py`, `plans/round45_c2_verify.py`, `plans/round-46` C2/C3
  counters, `plans/pkg_gate.py`, the fence, the C3 probe. Their committed receipts were read, not re-run.
- The round-45 C1 keyed-control class (QUALITY Q39) and the §2 hold-out tally are not drafted as `## Mistakes` rows
  here: they are the closure's C1 ruling and already carry a QUALITY criterion with committed red/green receipts; if
  the L1 wants them, they belong under `## What was demonstrated`, not `## Mistakes`.

## Artifacts

| path | what |
|---|---|
| `.ufo/waves/round-46/w1/R46ScribeMistakes.md` | this report |
| `.ufo/waves/round-46/w1/R46ScribeMistakes/mistakes-probe.txt` | envelope receipt of the 6 red/green legs (1904 B, sha256 `3e3a0d12…`) |
| `.ufo/waves/round-46/w1/R46ScribeMistakes/mistakes_probe.py` | probe source (8550 B, sha256 `042a2564…`) |

Scratch `/fast/scratch/hyaku/kengaku-r46/R46ScribeMistakes` removed with `plans/scratch_guard.py safe-rm` after the
receipts were copied out. No tool was installed or upgraded.

VERDICT: mistakes-rows-7-captured-by-none-2
