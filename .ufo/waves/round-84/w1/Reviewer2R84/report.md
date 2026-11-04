# Reviewer2R84 — independent attack on R84-C1 (prediction derivation and do-nothing control)

role: reviewer
seat: Reviewer2R84
candidate: gcode-to-text
candidate writer: KengakuR84
wave: round 84, wave 1 (leaf attack seat; no production bytes edited)
frozen plan: `plans/round-84-claims.md` at commit `b12a9d46806cb8d69fe48fac0f4efff0b266e4c2`
base revision: `4087b2f8369fb0c317a8460725a607681ff2fd7f`
host: Linux 7.2.11-arch1-1, python 3.14.8, bubblewrap 0.13.1
tooling: no installs or upgrades were needed and none were made (no pacman, uv, npm or cargo
transaction); no service or config was touched.
declarations: the candidate writer is declared mid-line (`candidate writer: KengakuR84`)
because the round-84 Gate checker treats a report line starting with `writer:` or `author:`
that names the candidate writer as a self-review defect; only mid-line text is safe here.

## 0. Scope and method

This seat attacks R84-C1 from two directions that the claim's own instrument cannot
close: (a) an independent derivation of the eight predicted P/F vectors from the captured
grader source alone, before looking at the probe or the case table, and (b) an independent
bubblewrap re-execution of the same eight cases with a driver written from the source, not
from the lane's probe. Nothing in the frozen claim, the case table, the counter, the probe
or the population ledger was modified. All writes are under
`.ufo/waves/round-84/w1/Reviewer2R84/` and the seat scratch directory.

Inputs actually read for the attack:
- `corpus/evidence/round52/graders/gcode-to-text/tests/test_outputs.py`
  sha256 `6b049dc626aa103b20d165552e5cb39ba02c6803b04ba06a43d79435b5f701a6` (pin prefix
  `6b049dc626aa103b` confirmed; byte-identical at BASE and at `b12a9d46`).
- the frozen case table inside `plans/round-84-claims.md` (the claim's own source).
Not read before the derivation was written: `plans/round84-cases.json`,
`plans/round84_gcode_probe.py` (both ABSENT from BASE and from `b12a9d46` anyway; see §5).

## 1. Independent derivation (source only)

The captured module has exactly two test functions, in definition order:

1. `test_hello_file_exists`: `assert Path("/app/out.txt").exists()`.
   `P` iff the path resolves to an existing entry; `F` (AssertionError) iff absent.
   An empty regular file exists, so it passes leg 1.
2. `test_hello_file_content`: `assert Path("/app/out.txt").read_text().strip() == "flag{gc0d3_iz_ch4LLenGiNg}"`.
   `P` iff the decoded text stripped of all Unicode whitespace equals the flag exactly
   (case-sensitive). `F` via AssertionError on any other decoded text; `F` via
   FileNotFoundError when absent. Any other exception (UnicodeDecodeError from
   `read_text()` on non-UTF-8 bytes, IsADirectoryError/PermissionError on an unusable
   path) escapes the two classified types and is therefore a SETUP under the claim's own
   classification.

Derived vectors (exists/content), same order as the frozen table:
`missing F/F, empty P/F, exact P/P, padded P/P, uppercase P/F, suffix P/F,
prefix-only P/F, wrong-flag P/F`. Nine P legs, seven F legs; the only P/P class is
`exact` modulo whitespace padding, which follows directly from `str.strip()`.

Full derivation, per-case reasoning and the derivation-side defects are in
`.ufo/waves/round-84/w1/Reviewer2R84/derived-vectors.txt`.

## 2. Derived versus frozen table

Frozen predicted column (claims table): `F/F P/F P/P P/P P/F P/F P/F P/F`.
Derived from the source:              `F/F P/F P/P P/P P/F P/F P/F P/F`.

**Disagreements: 0 of 8.** No frozen case is mispredicted by the claim; every case id,
staged byte description and vector is consistent with the captured AST. The claim's
statement that `padded` passes both legs is correct only because the pad is whitespace:
`" \n" + exact + "\t\n"` is removed entirely by `str.strip()`.

## 3. Independent bubblewrap re-execution (attack, not the lane gate)

Harness: `bwrap --unshare-all --ro-bind /usr /usr --ro-bind /etc /etc
--symlink usr/lib /lib --symlink usr/lib /lib64 --proc /proc --dev /dev
--bind CASE /app --ro-bind <grader>/tests /tests --ro-bind <driver> /driver
python3 /driver/two_leg.py`. The driver imports `/tests/test_outputs.py` unmodified,
calls its top-level `test_*` functions in AST definition order, and classifies
AssertionError | FileNotFoundError as F, normal return as P, anything else as SETUP.
Case staging is byte-exact from the frozen table; `missing` stages no `out.txt`.

Observed (full transcript: `.ufo/waves/round-84/w1/Reviewer2R84/attack-run.txt`):

| id | predicted | observed | leg detail |
|---|---|---|---|
| missing | F/F | F/F | exists=AssertionError; content=FileNotFoundError |
| empty | P/F | P/F | exists=ok; content=AssertionError |
| exact | P/P | P/P | both ok |
| padded | P/P | P/P | both ok |
| uppercase | P/F | P/F | exists=ok; content=AssertionError |
| suffix | P/F | P/F | exists=ok; content=AssertionError |
| prefix-only | P/F | P/F | exists=ok; content=AssertionError |
| wrong-flag | P/F | P/F | exists=ok; content=AssertionError |

`cases=8 mismatches=0 setup_defects=0`, `PREDICATE R84-PROBE pass`, harness exit 0.
The independent run reproduces the claim's predicted vector for all eight cases and
sixteen legs; the counter's 16-leg claim is arithmetically correct.

Extra probes (not part of the frozen eight; attack evidence only):
- 0-byte `out.txt` -> `P/F` (identical to `empty`; `read_text()` on an empty file does
  not raise). The table's `empty` case is therefore safe.
- non-UTF-8 `out.txt` (`b"\xff\xfe"`) -> `P/SETUP` (`UnicodeDecodeError`). **A non-UTF-8
  file makes leg 2 a SETUP, not an F. The frozen table contains no such case.**
- `out.txt` staged as a directory -> `P/SETUP` (`IsADirectoryError`). Also uncovered.

## 4. Do-nothing control

Predicted outcome from the claims: at a revision with no receipt,
`TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0 defects=>=1`,
`PREDICATE R84-C1 fail`, exit 1, and the do-nothing control must print
`target_reached=False`.

Can staging nothing satisfy the frozen predicate? No. The target is a conjunction that
includes `located=1`, `executed=1`, `cases=8` and `legs=16` over the receipt
`corpus/evidence/round84/gcode-to-text-probe.txt`. With nothing staged there is no
receipt file, so `located=0` fails immediately, and `cases/legs` cannot be counted because
no observed leg exists. Independently of the counter, staging nothing also produces the
`missing` vector `F/F` at the grader level, which is the claim's own "before" behaviour.
The predicate is therefore satisfiable only by writing a receipt file, which is the
intended witness and not a bypass of the control.

Residual attack surface (see finding A3): the predicate is a predicate over receipt
*bytes*. A fabricated receipt that carries a complete stamp and the *correct* vectors is
indistinguishable to any offline counter, and the claim's fabricated-observations control
only exercises *wrong* vectors. The do-nothing control proves "no receipt -> fail"; it
does not prove "receipt came from a real run". That is an evidentiary limit of the
frozen predicate, not a violation of it.

## 5. Kill-rule comparison and artifact presence

Each observed leg equals its predicted vector (no kill-rule trigger), no setup exception
occurred in the eight frozen cases (no trigger), and the subject sha256 equals the pin
`6b049dc626aa103b...` at both BASE and the frozen plan commit (no trigger). The
missing-receipt-field and control-reaches-target triggers are not evaluable from here
because the receipt and the counter do not exist yet:

- `plans/round84_c1_replay.py` — ABSENT at BASE and at `b12a9d46`
- `plans/round84_gcode_probe.py` — ABSENT at BASE and at `b12a9d46`
- `plans/round84-cases.json` — ABSENT at BASE and at `b12a9d46`
- `corpus/evidence/round84/gcode-to-text-probe.txt` — ABSENT at BASE and at `b12a9d46`
- `corpus/lessons/round-84.md` (and its S271 Gate row) — ABSENT at BASE and at `b12a9d46`

Base figures independently recomputed from `plans/grader-population-ledger.json`
(sha256 `1695ec760c4d152767a4db84b5797416983c2272cc95c013cb285e0f315621ad`, identical at
BASE and `b12a9d46`): members 88, executed 27, unexecuted 61, file-artifact class 76 of 88
with 19 executed; the `gcode-to-text` entry is `status=unexecuted`, classes
`["file-artifact"]`, evidence `no-blocker: tests/test_outputs.py sha256=6b049dc626aa103b`.
All four "before" figures in the claim (27/61, 19 of 76) match the ledger, and the
"after" figures 28/60 and 20 of 76 are the correct single-member increments.

## 6. Findings, by severity

### R84-C1

A1 (minor, coverage gap in the frozen case table). The eight cases are all
UTF-8-decodable regular files or absent. The SETUP branch of the claim's own
classification is therefore never exercised: a non-UTF-8 file and a directory both yield
SETUP (observed above). Consequence: `defects=0` on the eight cases is guaranteed by table
composition, not by the instrument's handling of the branch. The table is frozen and must
not be changed; the counter's mutant set should include a mutant that classifies a SETUP as
`F` (and one that classifies AssertionError as SETUP), otherwise the classification code is
unexercised. Not a kill-rule trigger; no vector is wrong.

A2 (minor, reproducibility of the stated sandbox). The claim's recipe — "`/usr` and `/etc`
read-only, the case directory bound as `/app`, the grader read-only at `/tests`" — cannot
start the interpreter on this host as literally written: `/usr/bin/python3` needs
`/lib64/ld-linux-x86-64.so.2`, and both `/lib` and `/lib64` are symlinks into `usr/lib`
that do not exist in a fresh bwrap root. My first run failed exactly there
(`execvp /usr/bin/python3: No such file or directory`), and a second binding mistake
(binding the grader root instead of its `tests/` directory) failed with
`/tests/test_outputs.py: No such file or directory`. Both are plumbing, not grader
changes, but the receipt's reconstructed COMMAND must include the `/lib` and `/lib64`
symlinks (or equivalent binds) and must bind the `tests/` directory itself at `/tests`,
or the receipt is not reproducible from its own stamp. Suggested receipt-side fix only;
the frozen predicate need not change.

A3 (major, inherent evidentiary limit of the predicate). The target is verified against
receipt bytes; every "host-pinned" field (`HOST_PYTHON`, `HOST_OPENSSL`, `LANE_TIP`,
`WORKTREE`, `COMMAND`) is self-declared and copyable, and the claim says the COMMAND is
"never executed from the receipt". A fabricated receipt with a complete stamp and the
correct vectors is therefore indistinguishable from a real one by any offline counter,
while the claim's fabricated-observations control only catches *wrong* vectors. This does
not falsify the predicate; it bounds what the predicate proves. Recommendation for the L1
(not a frozen edit): have the receipt embed the per-case driver stdout line-for-line and
have the counter re-parse the OBSERVATIONS block and require it to equal its own
re-execution case by case (so a forgery must also forge the exact stdout shape), and
commit the receipt in the same commit as the counter run so the receipt cannot be
back-filled silently. Even then the evidence is "reproducible", not "provably executed".

A4 (minor, undefined BASE field). The claim's before-line prints `defects=>=1` at BASE,
but BASE runs zero cases, so under the stated definition ("any other exception = setup
defect") the defect count is 0. The printed `>=1` implies a second defect definition
(e.g. "member unexecuted" or "receipt absent" also counts as a defect) that the claim
does not state. Reconcile the field's meaning in the counter's output legend, or print
`defects=0` at BASE; either way the counter predicate (`executed=0`, `located=0`) already
makes BASE red, so this is documentation, not a scoring break.

A5 (informational, fidelity note). The captured harness (`tests/test.sh`) runs the module
under pytest 8.4.1 on CPython 3.13 and maps any non-zero pytest exit to `reward 0`; under
pytest a FileNotFoundError is an *error*, not a *failure*. The claim's two-leg model maps
both to F, which matches the reward mapping but is a modelling choice. The claim scopes
itself to the two functions, so no action is required; the receipt should not describe
pytest's failure/error distinction as part of the measured surface.

### R84-C2 (adjacent, blocking, raised because this seat is a cited second-seat reader)

B1 (BLOCKER for Q13). `plans/gate_timing_check.py` (sha256
`51c18a9edfecba9cb6e15449b8063668f41225e98347c6221c6df7c2b0b80a2a`, unchanged from
`b12a9d46`) only resolves a cited report when its wave directory is `falsify` or matches
`wave[-_ ]?0*2` (`is_second_wave`), and `wave_directory` requires exactly five path
components (`.ufo/waves/round-N/<dir>/<file>.md`). The fleet's round-84 wave directory is
`w1` (rounds 82 and 83 both committed `w1/swarm-registry.json`; every seat's output path is
`w1/<Seat>/`). Measured, not inferred: with a synthetic round-84 tree, a `w1` citation
yields `resolve_citations -> reports=[]`, `audit ok=False`, reason
`no cited, existing, returned second-seat report for this round` — including when the
`w1` member is injected manually, so the failure is the directory filter, not the
registry. A `wave2` citation of the same bytes and registry yields `audit ok=True`. A
seat-directory citation (`w1/Reviewer2R84/report.md`) is six components and is invisible
to `wave_directory` entirely. Transcript: `q13-probe.txt`. The same result holds through
the real CLI on a throwaway fixture repository (entry with a `writer:` line, a
candidate/decision/reason Gate admit row, a five-component report and a `swarm-registry`
in the same directory): with the report under `w1/` the checker exits 1 with
`missing: no .ufo/waves/round-84/falsify/ report exists in commit 5fec6f31...`; with the
identical tree and report under `wave2/` it exits 0 with `passed=1`. Transcript:
`q13-cli-fixture.txt`. The fixture is scratch-only; no lane or fleet commit was created.

Therefore R84-C2's Q13 arm
cannot reach exit 0 for any report committed under `.ufo/waves/round-84/w1/`, and the
claim freezes the check to `plans/gate_timing_check.py --lesson corpus/lessons/round-84.md
--commit REV` with exit 0. The minimal honest paths visible: (i) commit this round's cited
re-read report plus a `swarm-registry.json` under `.ufo/waves/round-84/wave2/` (accepted
by the checker; adds a directory the wave contract does not name, so the L1 must judge
whether that is honest naming rather than a workaround), or (ii) extend `is_second_wave`
to accept `w1` — but that edits the frozen instrument mid-round and should be treated as a
retune the kill rule forbids unless declared as such up front. I do not decide; I report
the measurement.

B2 (BLOCKER for Q13). The checker reads the candidate's writer with
`^writer:` from the entry bytes; `candidate_writer(corpus/knowledge/tb2-code-from-image-offline.md
at BASE) = None`, because the entry has no `writer:` or `author:` line (verified by grep
and by the module call; transcript `q13-probe-parser.txt`). With `writer is None` every
cited report is invalid: `candidate has no committed writer: field; self-review cannot be
excluded`. The entry is 32 lines and its first three lines are `source:`, `verified-at:`,
`recheck:` as Q1 requires, so a `writer:` line must be added below them by the integrating
seat, and must differ from any writer declared in the cited report.

B3 (major for Q13). `parse_gate_admissions` only recognises a table whose header contains
`candidate`, `decision` and `reason` cells. The actual round-83 Gate uses a source table
(`id and decision | URL or own-work location | access date | located quote | reason /
flip`), which parses to `gate_found=True, admissions=0` (measured on the BASE bytes of
`corpus/lessons/round-83.md`). The round-84 lesson's Gate therefore needs a separate
admission row `| corpus/knowledge/tb2-code-from-image-offline.md | admit | ... cited
report ... |` in addition to the S271 source table, or the checker sees no admission to
audit.

B4 (minor, path shape of this report). The L1 amendment asks for
`.ufo/waves/round-84/w1/Reviewer2R84/report.md`. That path is six components and cannot
be cited by the checker (see B1). The citable shape is
`.ufo/waves/round-84/<dir>/Reviewer2R84.md`. Both files exist here with the same body, so
the L1 can cite the five-component one if a checker-accepted directory exists. The
engine's report-side conditions were self-checked against these exact bytes: with a
synthetic candidate entry carrying `writer: KengakuR84` and the report placed at a
checker-accepted `wave2` path, `audit_admission` returns `ok=True`; `REPORT_AUTHOR_RE`
finds no declaration line and `VERDICT_RE` finds the anchored line (transcript
`q13-probe-parser.txt`).

## 7. Q1/Q21/Q13 re-read of the round-83 admitted entry at BASE

Candidate bytes: `corpus/knowledge/tb2-code-from-image-offline.md` at
`4087b2f8369fb0c317a8460725a607681ff2fd7f`, sha256
`fc42c76cb5a05c131a5fec4d2aa3e441d9627841d130a54d1b616f2042675271`, 32 lines.

- **Q1 = 1 (defect).** First three lines are exactly `source:`, `verified-at:`,
  `recheck:` (correct key order, no BOM, no blank line). But the `recheck:` line is
  `recheck: python3 plans/round83_c1_replay.py --lane . --work DIR` — it names a
  re-check *action* and no ISO date and no cadence. Q1 requires the date or cadence, so
  the entry fails Q1 as admitted.
- **Q21 = 1 (defect).** The `source:` line does carry a 40-hex pin
  (`2fd12b88aafdd04a52c298e3940bcb189f9766d6`, inside the S267 URL), so the first
  conjunct holds; the `recheck:` line names neither that pin nor a re-pin cadence, so the
  second conjunct fails. Q21 is the conjunction, hence a defect.
- **Q13 = 1 (defect).** No successor admission exists at BASE:
  `corpus/lessons/round-84.md` is absent from both BASE and `b12a9d46`, so there is no
  `## Gate` admission and no cited second-seat report. Independently, even after a
  successor admission is written, B1/B2/B3 above show the frozen checker would still
  return non-zero for a `w1` citation and for an entry without a `writer:` field.

My re-read therefore confirms the claim's BASE triple `q1=1 q21=1 q13=1, defects=3`.
The repair is the L1's integration step (dated round-84 correction paragraph plus the
successor Gate); this seat neither repairs nor admits the entry. The base bytes do not
meet the lane's admission bar, and my verdict line below records that, not an endorsement.

VERDICT: FAIL-AT-BASE — Q1=1, Q21=1, Q13=1 for corpus/knowledge/tb2-code-from-image-offline.md (sha256 fc42c76c...); entry not admissible as committed, repair is the L1's integration step, and Q13 additionally needs the w1-citation blocker resolved.

## 8. R84-C1 final verdict

final verdict: agree

The frozen predicted vectors reproduce the captured grader's two functions exactly
(8/8 cases, 16/16 legs, 0 mismatches, 0 setup defects) under an independently written
driver and an independently staged bubblewrap run; the subject sha256 matches the pin at
BASE and at the frozen plan commit; the base ledger figures match the claim's before-state;
and staging nothing cannot satisfy the frozen predicate. The findings above (A1–A5) are
coverage/reproducibility limits that the L1 can fold into receipt and mutant design
without changing the frozen predicate, target, case table, control set or kill rule. The
R84-C2 Q13 findings (B1–B4) are, by contrast, blockers for the other claim and are
reported here because this seat is one of the reports that claim intends to cite.
