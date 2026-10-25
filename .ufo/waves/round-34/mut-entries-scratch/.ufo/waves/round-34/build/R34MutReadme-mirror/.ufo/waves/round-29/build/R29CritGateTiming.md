# R29CritGateTiming — adversarial critique of round-29 Q10/Q13 gate timing

seat: R29CritGateTiming (role critic, build wave; registry agentId `KengakuR28.R29CritGateTiming-2`)
actual writer: KengakuR28.R29CritGateTiming-2 (read-only leaf; no subagents, no commits, no production edits)
lane HEAD at read time: 31934e5660f1814326c6472eefdfa0c41e642a2f (prereg); `.ufo/waves/round-29/` untracked
axes named: novelty (milestone axis). Impacted by this finding: canonical coverage/constructs admission
evidence (C1 knowledge entry), provenance/identity of returned reviews. Calibration, the score of 7 and
the frozen P2–P4 classes are untouched by this critique.

Scope boundary: this is a build-wave critic report. Under `plans/gate_timing_check.py` a build-wave
report is never Q10/Q13 support (only `falsify` / `wave-2` directories count), so nothing here is a
second-seat re-read or an approval of any candidate. r28 admission is operator-reported ground truth and
was NOT rechecked; r28 committed receipts are read only as prior-art failure evidence.

## Sources read (sha256 of bytes read)

| path | sha256 |
|---|---|
| plans/round-29-claims.md | 6b4ffee35ddf706a4a77e9daf9c647cbd85b484f8b652b7dbd84dbd6289e92c1 |
| plans/gate_timing_check.py | 51c18a9edfecba9cb6e15449b8063668f41225e98347c6221c6df7c2b0b80a2a |
| corpus/QUALITY.md (Q10, Q13–Q16) | faeb0e6014c8f28746c42e2eb8bb6dabb16982a3c5547ae747631871951f5c85 |
| corpus/lessons/round-28.md (Gate line 263, M85 lines 281–284, correction 278–279) | 0d705d56caba8a69368a8dbcc3a8f47a9ed8137c33d050adb98be292eb3983bc |

Also read: `corpus/evidence/round28-calibration/actual-gate.txt`, `actual-gate-corrected.txt`,
`actual-admission-byte-proof.json`, `actual-final-byte-proof.json`; `.ufo/waves/round-29/build/swarm-registry.json`;
first lines of `.ufo/waves/round-29/drafts/webarena-config-projection.md`.

## Verified quotes (programmatic: substring on stated line, `len(quote.split())`)

Script `.ufo/waves/round-29/scratch/R29CritGateTiming/quotes.py` (sha256 2fecb9ab…879287), output
`quotes-output.json.txt` (sha256 e16b615c…e0e1): `all_found True max_words 16`.

| path:line | words | quote |
|---|---|---|
| plans/round-29-claims.md:93 | 13 | "until complete eligible second-seat source/number re-reads return on exact final bytes, writer differs," |
| plans/round-29-claims.md:94 | 12 | "plain anchored VERDICT: PASS exists, and actual admitting commit includes reports/registry, entry," |
| plans/round-29-claims.md:95 | 7 | "Q13 is structural only; digest/actual-commit proof separate." |
| plans/round-29-claims.md:22 | 10 | "Measurement revision is the branch/helper landed revision, never detached HEAD." |
| corpus/QUALITY.md:106 | 4 | "Presence is not endorsement" |
| corpus/QUALITY.md:117 | 16 | "the checker grades the requested tree but does not discover that commit or interpret review conclusions." |
| corpus/lessons/round-28.md:263 | 10 | "Q13 actual-commit result and report-byte pins are recorded after landing" |
| corpus/lessons/round-28.md:278 | 9 | "First admitting commit df33fc83764975fd808b0945097b5d0c7aca3901 had two observed red checks," |
| corpus/lessons/round-28.md:279 | 6 | "These are not represented as passes." |
| plans/gate_timing_check.py:56 | 4 | `VERDICT_RE = re.compile(r"^VERDICT:\s*(\S.*?)\s*$", re.MULTILINE)` |

## Strongest actual objection

The round-29 prereg states three admission conditions — re-reads "on exact final bytes", a "plain
anchored VERDICT: PASS", and the "actual admitting commit" contents — but names only one gradeable instrument
(Q13, explicitly "structural only") and leaves the digest/actual-commit proof as an unnamed, untimed
"separate" step. The Q13 function counts any column-zero `VERDICT:` line of any value, anywhere, and never
hashes the candidate. And the r28 pattern the prereg inherits records the actual-commit result "after
landing". Together that means the stated conditions can be unmet in the tree that moves master, and
the defect is only discovered (if at all) in a later receipt commit. This is a timing defect, not a
truth defect: callback presence, report presence or a FAIL/PARTIAL line can structurally satisfy Q13.

### Prior-art evidence that this already happened (r28, committed receipts, not rechecked)

- `actual-gate.txt` (added in 78e6df8, i.e. after admitting commit df33fc8): Q13 on df33fc8
  `admissions=1 passed=0 failed=1`, exit=1; FFullEntry.md "report has no anchored VERDICT line".
- `actual-gate-corrected.txt` (added in ed26bdf): on 78e6df8 `passed=1 failed=0`, exit=0.
- My byte census of FFullEntry.md via `git show <c>:...` + `re.findall(r'^VERDICT:\s*(\S.*?)\s*$', t, re.M)`:
  df33fc8 → anchored verdicts `[]` (canonical-path mentions 7, v4-digest mentions 2);
  78e6df8 → `['PASS']` (8, 3). So the r28 admitting tree was red and master had already moved; the
  r28 lesson's own M85 row records the repair. The r29 prereg's "plain anchored" wording mines the
  symptom, but keeps the post-landing timing that let it land.

## Decisive bounded counterexample (in-memory, unchanged production function)

Probe `.ufo/waves/round-29/scratch/R29CritGateTiming/q13_probe.py` (sha256 ef5e960b…c731) imports
`plans/gate_timing_check.py` by path with bytecode disabled, builds a synthetic round-29 `falsify` tree in
memory (one registered `reviewer` seat `FEntrySeat`, candidate `knowledge/webarena-config-projection.md`
with `writer: R29DraftEntry`), and calls `audit_admission` exactly as `main()` does. No git, no network,
no lane writes outside my scratch (`plans/__pycache__` mtimes unchanged: newest 08:54:16 −0300).
Command: `PYTHONDONTWRITEBYTECODE=1 python3 -B q13_probe.py > probe-output.json` → exit=0;
output sha256 b4ac4f1facc5a6bc72b144e8a76ea15ecbd4118c400dc915ab6e127ab9944529.

| case | report content (abridged) | anchored verdicts found | report carries final sha | Q13 structural ok |
|---|---|---|---|---|
| C0 control | canonical path + final sha + plain PASS | PASS | yes | True |
| C1 | FAIL only | FAIL | yes | **True** |
| C2 | PARTIAL only | PARTIAL | yes | **True** |
| C3 | echoed seat-contract template `PASS/PARTIAL/FAIL`, no judgment | PASS/PARTIAL/FAIL | no | **True** |
| C4 | plain PASS bound to a stale digest; final bytes differ | PASS | no | **True** |
| C5 | early PASS, final section FAIL | PASS, FAIL | yes | **True** |
| C6 | PASS only inside a fenced code block | PASS | no | **True** |
| C7 | heading-form `### VERDICT: PASS` only (r28 M85 shape) | none | yes | False (no anchored line) |
| C8 | names only the drafts path, plain PASS | PASS | yes | False (candidate path not named) |
| C9 | C0 report, Gate prose "by the second seat" (space) | PASS | yes | False (generic reference) |

Units: 10 cases, each one admission row × one cited report; booleans are function return values, not
inferred. Six of ten (C1–C6) pass Q13 while violating either "plain anchored VERDICT: PASS" or
"exact final bytes". C7–C9 show the checker does discriminate format, path and generic prose, so the
gap is specific: verdict value, verdict finality/fencing, and digest binding are ungraded.

This is consistent with QUALITY Q13/Q14 by design ("Presence is not endorsement"; the checker does not
"interpret review conclusions"). The defect is not in the checker; it is that the r29 prereg relies on
an unspecified, post-landing "separate" proof to cover exactly those ungraded conditions.

## Secondary findings (bounded)

1. Build-wave exclusion (correct, but a planning trap): `is_second_wave` accepts only `falsify` or
   `wave-2`; all current round-29 reports, including this one, are under `build/`. No round-29 falsify
   registry or report exists at read time, so no Q10 re-read has returned yet; nothing is admissible now.
2. Draft-path trap (C8): the prereg keeps the candidate under `.ufo/waves/round-29/drafts/` until
   re-reads return, so reviewers will naturally cite the drafts path, which does not contain the
   substring `knowledge/webarena-config-projection.md`. Assignments must require the canonical path.
3. Writer identity form: the draft's line 3 is `writer: R29DraftEntry` (seat stem); the registry agentId
   is `KengakuR28.R29DraftEntry-2`, so the agentId comparison (gate_timing_check.py line 354) can never
   match a stem-form writer; only the seat-stem comparison guards self-review. If L1 edits the bytes
   after the scribe, the `writer:` line misattributes authorship (residual provenance risk, not proven).
4. Measurement/admission drift: the prereg measures at the "branch/helper landed revision" H, but the
   admitting commit A comes later. If A changes `plans/config_projection.py`, the oracle or the r29
   fixtures relative to H, the counted 812/3/2436 summary no longer describes A. r28's byte-proof JSON
   format (`matches_exercised_or_returned_bytes`) already covers this if computed at A.
5. Inherent, not a defect: a commit cannot contain its own hash, so the receipt naming A must land
   in a later commit. The defect is executing the check only after master moves, not recording it later.

## Smallest safe correction (procedure only; no code change; no stronger acceptance than declared)

Before master moves, L1 builds the admitting commit C on a side branch and runs, against C itself:

1. `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-29.md --commit C` → exit 0.
2. For every cited falsify report read via `git show C:<path>`: the last column-zero `^VERDICT:` line
   outside fenced code is byte-exactly `VERDICT: PASS`; the report contains the 64-hex sha256 of
   `git show C:corpus/knowledge/webarena-config-projection.md` and the canonical path; the Gate cell
   names that same digest.
3. The r28-format byte-proof JSON (candidate, cited reports, config_projection.py, oracle, r29 fixtures)
   computed at C equals the returned/exercised bytes (covers finding 4).
4. Land C by fast-forward only (landed SHA == checked SHA). Any red keeps master unmoved. The later
   receipt records `admission_commit: C` and the stdout captured before the ref update.

These steps only make the prereg's own lines 93–95 gradeable and correctly timed. They are a fixable
defect, not a tradeoff for the canonical judge. Flip condition: if L1 shows equivalent pre-landing
checks on the exact landed SHA, this objection is discharged.

## Not established / unknowns

- No claim that round-29 admission will fail; no r29 falsify reports exist to grade.
- I did not run the gate_timing_check CLI, its `--selftest`, any build/linter, or the r29 projection tool.
- r28 admission was not re-adjudicated; only committed receipt bytes were read.
- C1–C6 are synthetic fixtures for the unchanged function, not observed r29 reports.
- No installs or updates performed.

VERDICT: PARTIAL
