# Round 61 claims freeze (kengaku, hyaku run 14, 2026-11-02)

Base `f97e5b7b81d02084b63042631e0f3a1897af25c7` (the round-60 verifier spot-check tip,
`admitted` with two status-neutral routed defects). This freeze is written and committed
BEFORE the round's first scored run of the probe (the r57–r60 discipline: plumbing is
proven only against toys — the new probe's `--selftest` is green at the base worktree,
receipt beside this file at `.ufo/waves/round-61/recon/selftest-base.txt`, `SELFTEST
toy-sigint got=P/F want=P/F ok` at REV `f97e5b7b`; `--render-table` green at the base
worktree, receipt at `.ufo/waves/round-61/recon/render-table-base.txt`). Instrument
self-pin: `plans/round61_c1_cancel_probe.py` sha256 at freeze — recorded in
`.ufo/waves/round-61/recon/probe-selfpin.txt` and in the SCORECARD round-61 section.

Environment: WSL Ubuntu-24.04 (python 3.12.3, bwrap 0.9.0, git 2.56.0; uv/pytest absent —
the r56 A3.4 canonical counter environment preserved; no environment mutation this round).
Measured on clean WSL-native-fs clones; every exit label in a receipt is captured inside
the runner script (the r60 lesson's harness rule: the host harness swallows `$?` for
inline chains and is never trusted).

Carry-in (round-60 non-author closure, `corpus/lessons/round-60-verifier-spotcheck.md`
§6, both status-neutral): **(D1)** the round-60 fleet-root erratum mirror is
content-complete but not byte-for-byte — 9 non-ASCII characters cp1252-double-encoded and
one surplus trailing blank line — fixed this round by the byte-true mirror + the dated
erratum appended to the round-60 mirror file (R61-C2, the claim's landing); the
authoritative append bytes in the fleet working tree are intact (re-measured this round,
receipt `mirror-fidelity-receipt.txt`), the orchestrator's landing is unaffected, the
fleet-root landing stays routed. **(D2)** the round-60 report's mistake-row undercount
("2 mistakes + 2 appended rows" vs the landed 3+2) — precision nit only; the lesson is
complete; the round-61 report names the correction; no lane artifact is edited for it.
Standing opens routed or closed with evidence (see the round-61 report): r50-c1 root
cause and the R56-F1 checker repair were CLOSED at round 58 (the SCORECARD round-58 rows;
re-verified green in the round-60 final receipts) — evidence cited, nothing re-opened.
The three L0 questions `kengaku | round-25/33/51` (coverage cap; decision packet; absent
surfaces) and the `kengaku | round-56` pair (L2 surface; ledger host column) remain OPEN —
routed around, nothing assumed answered. The round-52 push-protection L0 question is
already disposed by operator decision recorded in `corpus/evidence/round52/graders/EXCLUDED.md`
(2026-10-28: exclude the bytes rather than bypass push protection).

## R61-C1 / coverage (lowest owned axis, L0-capped) — the seventeenth grader read and executed: a NEW grader class, signal-propagated cancellation semantics

**The class is new to the executed corpus.** The seventeenth read TB2 task grader is
`cancel-async-tasks` (capture byte-identical to the round-52 population capture; sha256
`d6f510b51fafc81b4e9b5cc95535aa13491c8753e0e4171db42c45f4de460ee7`, the SHA256SUMS pin;
S224, opened live this round at the same pin and byte-compared). Its decisive legs spawn
the candidate as a child process, deliver SIGINT mid-flight (`proc.send_signal(signal.SIGINT)`,
capture :93/:126/:162) and count cleanup-marker lines in the captured stdout (:102-103,
:135-136, :171-172) — a **signal-propagated cancellation-semantics gate**: no executed
grader sends a signal to the candidate process (the sixteen executed graders assert on
files, tool output, timing walls, numeric bands, crypto credentials or filesystem
metadata; the round-59 survey's measured negatives stand, extended this round: a grep of
all 184 round-52 captures for `send_signal` names exactly this grader). The grader's own
docstrings name the two traps the class prices: a ThreadPoolExecutor that does not
propagate cancellation (:75) and the asyncio.gather queued-task trap (:144-145).

**Probe** `plans/round61_c1_cancel_probe.py` (the r58/r59 instrument shape, new file):
byte-pinned capture materialized read-only at /tests in a bwrap sandbox (`--unshare-all`,
/usr+/etc ro, /app writable, /proc /dev, probe-owned `python` shim at /stub — the capture
invokes `["python", "test.py", ...]`); the six test functions run directly (no pytest;
the capture imports none). The task's reference `test.py` simulator is NOT in the capture
population (the r52 capture program took `tests/test_outputs.py` + `tests/test.sh` per
task; no `tests/test.py` is committed anywhere in this lane) — the builder writes a
lane-authored simulator per case, declared in CASES, exactly the r58/r59 builder pattern.
Predictions are DERIVED at run time by `predict_legs()` from the case definitions (the
r59 lesson M-1 mechanism — generated, never retyped); `--render-table` prints the
generated table, `--check-receipt` cross-checks a receipt's observed vectors output-side
only; the sha-refusal kill class is inherited (the probe refuses on any capture byte
drift). Leg rule (frozen now, before the first capture run): a leg is P iff its test
function returns normally; F on AssertionError OR any other exception escaping the
function — `subprocess.TimeoutExpired` from the capture's own `timeout=5` (:28),
`timeout=10` (:56) and `communicate(timeout=5)` (:96/:129/:165) is the class's dominant
failure mode. Predicate `PREDICATE R61-C1 pass` iff mismatches=0 and setup=0; exit 0
pass, 1 fail, 2 setup (missing capture, bwrap absent — never a vacuous pass).

**Leg anchors** (every predicate grounded in the capture's own assertions): file
:10-12 (run.py exists); concur :17-37 (timeout :28; counts :35-37 — started==2,
finished==2, cleaned==2 inside the 5 s window); obey :40-68 (timeout :56; elapsed
bound :68 — `elapsed >= 6` with tasks at 3 s each); below :71-103 (sleep :92, signal
:93, communicate :96, counts :102-103); at :106-136 (identical shape, max=2); above
:139-172 (n=3, max=2 — exactly two started and two cleaned markers :171-172).

**The generated prediction table** (verbatim `--render-table` output at the base
worktree, REV `f97e5b7b`; the scored run's receipt re-derives it at the freeze tip):

```
| case | defect class exercised | file | concur | obey | below | at | above |
|---|---|---|---|---|---|---|---|
| compliant-signal-handler | none -- the compliant asyncio candidate | P | P | P | P | P | P |
| threadpool-uncancelled | ThreadPoolExecutor does not propagate cancellation (:77-79) | P | P | P | P | P | F |
| kbdint-no-handler | no SIGINT handler: KeyboardInterrupt kills the loop, tasks die uncleaned | P | P | P | F | F | F |
| sequential-sync | sequential execution: concurrency leg times out | F | P | F | F | F | F |
| cleanup-missing | no cleanup handler: the cleanup-marker count is zero | P | F | F | F | F | F |
| cleanup-double | cleanup marker printed twice per task | P | F | F | F | F | F |
| started-premature | started marker printed at submit time (accounting wart) | P | P | P | P | P | F |
| partial-cancel | handler cancels one task and abandons the other | P | P | P | F | F | F |
| ignore-sigint | SIG_IGN: the signal is swallowed, work completes anyway | P | P | P | P | P | F |
| late-cancel-cleanup | cleanup marker arrives after the 5 s communicate window | P | P | P | F | F | F |
| no-max-enforcement | max-concurrent ignored (semaphore absent) | P | F | P | P | P | F |
| no-run-py | run.py absent (artifact-absence is a leg failure, not setup) | F | P | P | P | P | P |
TABLE cases=12 legs=72 predicted_u=0 source=CASES+predict_legs
```

Zero U marks; every cell is a fixed function of the declared candidate behavior plus the
capture's fixed timing constants (tasks 3 s, SIGINT at 0.5 s, waits 5/10/5 s). The
falsifiable before→after, stated before the scored run:

- BEFORE (base `f97e5b7b`): the probe file, the r61 capture dir and the S224/S225 rows do
  not exist (`git cat-file -e f97e5b7b:plans/round61_c1_cancel_probe.py` fails;
  `git show f97e5b7b:PROVINCE.md | grep -c seventeenth` prints 0; SOURCES rows at base =
  216); the corpus has no executed grader whose decisive leg sends a signal.
- AFTER (the freeze tip and the scored run): the seventeenth grader read and executed —
  the battery's receipt at `corpus/evidence/round61/cancel-async-probe.txt` prices
  `cases=12 legs=72 mismatches=0 setup=0 predicted_u=0` and `PREDICATE R61-C1 pass`,
  exit 0; PROVINCE names the seventeenth grader (17 of 89 read); the knowledge entry +
  README index row land; the SKILL registry row + the entrytruth ledger row register the
  instrument (registration in the landing commit, the r58 lesson-3 rule); SOURCES
  216→218 (S224 grader capture; S225 the encoding index used by C2 — both opened this
  round, adopted through `plans/sources_adopt.py`).
- Score: **coverage HELD at 7** — the standing unanswered L0 cap `kengaku | round-25/33/51`
  (nothing assumed answered); the ground and the class line move, the capped number does
  not (the r56–r60 held shape).

Claim-sizing (§9): a do-nothing control cannot reach this — the probe, capture, sources
and PROVINCE ground are absent at base; the battery requires the new instrument to run
clean; the do-nothing round leaves `mismatches` unpriced and `PREDICATE R61-C1 fail`
(exit 1) at any tip (the probe's own absence is the control's red).

## R61-C2 / calibration (held at ceiling 10, exercised) — the round-60 mirror's byte-fidelity claim corrected: the byte-true mirror lands and the false claim is downgraded by dated erratum

The round-60 closure's routed defect D1 (status-neutral): the mirror landed at `e26b330e`
claims "byte-for-byte" and is false at the byte level. Measured this round at base and
re-measured at the freeze tip (receipt `.ufo/waves/round-61/mirror-fidelity-receipt.txt`,
every exit captured inside the runner): the authoritative append (the fleet working tree's
`+` lines for `.ufo/reports/round-58/kengaku.md`, still uncommitted at the measurement —
the orchestrator owns the landing; the append bytes are intact, confirmed) is 26 lines /
2141 bytes / sha256 `2a2f952ca9809c426d91ec22feb3713fb485e0d7e393dea0fd3cecf939af2a21`
with 9 non-ASCII characters (5 em-dashes, 4 arrows) and zero double-encoded sequences;
the round-60 mirror's block is content-complete, carries all 5 em-dash-class and 4
arrow-class cp1252-double-encoded sequences (27 mojibake characters; first differing byte
39, line 2) and one surplus trailing blank line (27 marker-to-marker lines vs the
append's 26). Grounding: S225 (the WHATWG windows-1252 index, opened this round) pins
byte 0x80→U+20AC (:7), 0x86→U+2020 (:13), 0x92→U+2019 (:25), 0x94→U+201D (:27),
0xE2→U+00E2 (:105) — exactly the mis-decode that produced the observed triples.

The landing (this freeze commit, causally separable from C1 — no shared artifact but this
claims doc): (a) the byte-true mirror `.ufo/waves/round-61/r58-report-corrections-append-byte-true.md`
— byte-identical to the authoritative append (cmp exit 0 in the receipt; 26 lines; the
append's own sha256; headerless so byte verification needs no marker-stripping step — the
step whose absence hid the defect); (b) the dated ERRATUM appended to the round-60 mirror
file naming the encoding defect (byte triples named), the line-count defect, the
correction, and the status downgrade (content-mirror of record vs byte-mirror of record);
(c) the fidelity receipt. The round-60 mirror file's historical bytes above the erratum
stay untouched (append-only; the defective bytes ARE the history the erratum describes).

- BEFORE (base `f97e5b7b`): the byte-true file does not exist (`git cat-file -e
  f97e5b7b:.ufo/waves/round-61/r58-report-corrections-append-byte-true.md` fails); the
  committed mirror block bytes at base are the defective ones (the census commands in the
  receipt re-run against them).
- AFTER: the byte-true mirror exists and byte-compares clean; the erratum is the dated
  correction of record; the round-61 SCORECARD/LOG/lesson entries name the class (the
  close-2 HARD STOP is honored: no erratum-priced fragment is re-quoted anywhere — these
  are not erratum-priced counting commands, but the discipline of naming-not-quoting
  applies to the mirror claim too).
- Score: **calibration HELD at 10, exercised** — the false byte-level claim of the
  previous round is caught (by the non-author), owned, downgraded where the evidence
  demands it, and replaced by a mechanically verifiable artifact; the score's rubric
  anchors (SHONEN/SCORECARD entries match observed repo state) are repaired, not
  re-numbered (the r58/r60 held shape). The mirror repair is protocol work on a routed
  defect, claimed because it is falsifiable and lands this round — not an exploratory
  claim; the counting commands are in the receipt, named there.

Claim-sizing (§9): a do-nothing control cannot reach this — at base the byte-true file is
absent and the false "byte-for-byte" claim stands uncorrected in five landed artifacts
(report, PROVINCE, SCORECARD, LOG, lesson); the do-nothing round leaves the defect
standing and the routed carry-in unaddressed.

## Separability, sources, L0

- R13 separability: C1 and C2 share no artifact but this claims doc — C1's artifacts are
  the probe, the r61 capture dir and its receipt; C2's are the byte-true mirror, the
  erratum append and the fidelity receipt. Either verifies without the other having
  landed.
- Sources opened this round (both staged and adopted BEFORE the scored run): **S224**
  (the seventeenth grader's capture at the pin, fetched live and byte-compared to the
  committed population capture; the sourced claim for C1 rests on it — the class line
  quotes its docstrings) and **S225** (the WHATWG windows-1252 index; the sourced claim
  for C2 rests on it — the encoding-defect naming). No rejections this round; no flips.
- Exploratory claims: none this round; both claims carry counting commands in receipts.
- L0: the coverage cap trio `kengaku | round-25/33/51` and the `kengaku | round-56` pair
  stay open; routed around; nothing assumed answered (the cap is why C1's score is HELD
  and not raised).

## Amendment 1 (dated 2026-11-02, the Q25-sanctioned re-freeze — written and committed BEFORE the second scored run; the cells above stay as written)

The first scored run (at the repair tip `b9920576`; receipt of record committed AS-IS at
`.ufo/waves/round-61/recon/c1-first-run-FAIL.txt` with its runner transcript
`c1-first-run-stdout.txt`: `cases=12 legs=72 mismatches=2 setup=0 predicted_u=0`,
`PREDICATE R61-C1 fail`, exit 1) caught the author THREE times, and the amended probe is
re-frozen per the r59→r60 mechanism (the observed run is never re-scored; the corrected
re-freeze is a new claim with a new scored run):

1. SIMULATOR DEFECT (a) — the simulator never read the declared `handler` property: the
   add_signal_handler branch was gated only on ignore_sigint, so the kbdint-no-handler
   case installed the cancelling handler and behaved exactly like the compliant case
   (predicted F/F/F on the three cancel legs, observed P/P/P). Fix: the amended simulator
   installs the cancelling loop handler only when the case declares handler=True; SIG_IGN
   wins when ignore_sigint is declared.
2. SIMULATOR DEFECT (b) — premature_start double-printed the started marker (once at
   submit AND once in the task body), so every count leg of started-premature saw twice
   the declared count and failed. Fix: the started marker prints at submit INSTEAD of in
   the task body when premature_start is declared (mark_started() no-ops in the body).
3. FREEZE-TRANSCRIPTION DEFECT — the embedded table above carried one hand-transcribed
   row: no-max-enforcement's concur/obey legs were swapped at transcription (the freeze
   row reads P/F/P/P/P/F; the generated table — and the first run's predicted AND
   observed vectors — read P/P/F/P/P/F). The r59 freeze-transcription class again, caught
   this round by diffing the amended `--render-table` output against the freeze's
   embedded block (receipt `.ufo/waves/round-61/recon/table-identity.txt`); the mined fix
   stands: the table of record is ALWAYS the tool's `--render-table` output, never a
   hand-copied rendering of it. The generated table below (verbatim at the amended tip)
   supersedes the block above for that one row; the other eleven rows are identical.

**The amended table of record** (verbatim `--render-table` output of the amended probe at
the amendment worktree, REV `b9920576` — the scored run's receipt re-derives it at its own
tip; identical to the freeze's block on 11 of 12 rows):

```
| case | defect class exercised | file | concur | obey | below | at | above |
|---|---|---|---|---|---|---|---|---|
| compliant-signal-handler | none -- the compliant asyncio candidate | P | P | P | P | P | P |
| threadpool-uncancelled | ThreadPoolExecutor does not propagate cancellation (:77-79) | P | P | P | P | P | F |
| kbdint-no-handler | no SIGINT handler: KeyboardInterrupt kills the loop, tasks die uncleaned | P | P | P | F | F | F |
| sequential-sync | sequential execution: concurrency leg times out | P | F | P | F | F | F |
| cleanup-missing | no cleanup handler: the cleanup-marker count is zero | P | F | F | F | F | F |
| cleanup-double | cleanup marker printed twice per task | P | F | F | F | F | F |
| started-premature | started marker printed at submit time (accounting wart) | P | P | P | P | P | F |
| partial-cancel | handler cancels one task and abandons the other | P | P | P | F | F | F |
| ignore-sigint | SIG_IGN: the signal is swallowed, work completes anyway | P | P | P | P | P | F |
| late-cancel-cleanup | cleanup marker arrives after the 5 s communicate window | P | P | P | F | F | F |
| no-max-enforcement | max-concurrent ignored (semaphore absent) | P | P | F | P | P | F |
| no-run-py | run.py absent (artifact-absence is a leg failure, not setup) | F | P | P | P | P | P |
TABLE cases=12 legs=72 predicted_u=0 source=CASES+predict_legs
```

Instrument self-pin superseded `7d448487170ae54dc373c5758cb3c522a4137f877a86330e94302be2fe5f9f59`
→ `92facdc762bdb29c581eb92b5951f0855bec0de7dc56c8d2308136c889fe7f87` (the intermediate `c1341c24…28272` fixed the simulator only and was never a receipt of record) (both digests named
per Q25; recorded in `.ufo/waves/round-61/recon/probe-selfpin.txt`). Unchanged: CASES
declarations, predict_legs, the leg rule, the leg anchors, the sandbox, the sha-refusal
kill class, the exit map, the capture pin, the zero-U property. The claim of record for
R61-C1 is the SECOND scored run of the amended probe; the first run's fail stands as
history and is mined in `corpus/lessons/round-61.md`.

**Amendment 1 addendum (dated 2026-11-02, still before the second scored run):** a fourth
defect, named before any receipt of record of the amended instrument — the prediction
MODEL shared defect (a)'s blind spot: predict_legs' asyncio else-branch asserted
"asyncio + handler" in its comment but never checked the handler property, so the model
predicted P on the below/at legs for kbdint-no-handler while its above formula (which
does check handler) predicted F — that split is exactly the first run's kbdint mismatch
shape (predicted F only at above, observed P everywhere: the broken simulator installed
the handler, agreeing with the else-branch below/at and disagreeing with the above
formula). The amended model checks handler explicitly (P on the cancel legs iff
handler=True for the asyncio family, keep-alive semantics for threads, ignore, late and
partial handled by their own branches). The amended generated table — which the block
above now embeds byte-identically from the tool's own `--render-table` output — prices
kbdint-no-handler P/P/P/F/F/F: identical to the freeze's embedded row for that case, so
the freeze block's only remaining defect stays the one transcribed row
(no-max-enforcement). The selftest stays green at the amended worktree (receipt
`recon/table-identity.txt` carries the full identity + selftest record).

**Amendment 1 addendum 2 (dated 2026-11-02, after the second scored run, before the
landing):** the freeze's claimed before-anchor for PROVINCE was wrong — the freeze says
`grep -c seventeenth` prints 0 at base, and the measured truth is **1** (the round-60
planned section's own sentence "a seventeenth grader only if a NEW grader class is
found" already contains the word). Measured against the base bytes via a clean clone's
object store (receipt `.ufo/waves/round-61/measurements.txt`, controls section, every
control re-run): the CORRECT before-anchor for the frontier move is `17 of 89` — count 0
at base (`16 of 89` count 3 at base), 1 at the landing tip. The claim's before→after is
unchanged in substance (no seventeenth-grader read-ground exists at base; the probe, the
capture, the knowledge entry and the frontier sentence are all absent at base — every
absence control returned rc=128); only the stated anchor command was wrong, and it is
corrected here rather than silently repaired.

## Precision erratum — round62, 2026-11-02

Amendment1's description of the hand-transcription defects undercounted them:
the preserved `.ufo/waves/round-61/recon/table-identity.txt` differs on THREE
lines, comprising separator + TWO data rows (sequential-sync and
no-max-enforcement), not just no-max-enforcement with eleven unchanged rows.
The mechanically embedded amended table remains as landed; no prior run or
prediction is rescored. Re-derived read-only this round in
`.ufo/waves/round-62/recon/precision-before.txt` and independently reviewed.
The same receipt binds the S225 pointer correction (pointer98→byte0xE2,
successor S230) and registry EOL precision:272LF/0CR at base,
274LF/274CR at freeze,274LF/0CR after repair. The local numstat total546
reproduces; the prior review's511 does not. See the appended round62 precision
erratum in `corpus/lessons/round-61.md`; all preceding bytes remain historical.
