# R30FxConsiderthese — Q20 audited against its own source, its own probes, and the bytes it names

Role: leaf falsify seat (kengaku round 30, hyaku run 6). Target: the Q20 criterion the round landed from
`considerthese/2026-10-24.md` proposal 1. I read the four artifacts named in the assignment, then re-ran every
gate Q20 names, in trees I extracted myself. **No lane write except this file. No edit, no commit, no package
transaction.** Scratch: `/tmp/r30fx-considerthese/` (lane HEAD `363a4eb`, working tree carrying round-30's
uncommitted bytes; all mutations done on `cp -a` copies of an extraction, never on lane bytes).

**The lane landed mid-audit.** At the start of this seat the tree was dirty at tip `363a4eb`; it is now
`623c1fc9b083a9b3def3b9f66f5518628e01b6a5` — `round-30: assimilation round 2 (contamination-transparency
amendment), routed-defect closure D1-D5, quote-validating adoption gate`, 2026-10-25 04:45:51 -0300, 102 files.
I re-ran every gate against a `git archive 623c1fc` extraction (`/tmp/r30fx-considerthese/land623`) and diffed
the landed Q20 against the bytes I had read: `diff` → **identical**, so every clause verdict below holds of the
landed text. Pre-landing measurements are kept where they are the only ones that can separate "before" from
"after" (the 10→14 selftest move), and are labelled as such.

Artifacts read:
- `corpus/QUALITY.md:196-217` (section header + Q20; byte-identical at `363a4eb` working tree and at `623c1fc`)
- `considerthese/2026-10-24.md:16-25` (proposal 1) and the file's own date line
- `corpus/lessons/round-30.md:24` (the considerthese row)
- `.ufo/waves/round-30/build/R30Considerthese.md` (the seat's 15-gate roster, §4 draft, §5 probes P1/P2/P3)

---

## 1. Clause verdicts

| # | Clause in Q20 | Verdict | Evidence (all re-run by me today) |
|---|---|---|---|
| A | cites the proposal **and a date**: `considerthese/2026-10-24.md` §Self-improvement suggestions 1 (2026-10-24) | **PASS** | File exists; its header is `## Self-improvement suggestions (proposals only; nothing acted on)` at `:16`, item 1 spans `:18-25` ("Run the gates on every push …"), and the file's own date line reads `# considerthese — 2026-10-24`. Section+item resolve unambiguously. Weakness only: no line range (Q19 gives `:44-49`), so a reader resolves by heading, not offset. |
| B1 | `git archive <sha> \| tar -x -C <tmp>` is the extraction form | **PASS** | `git archive 363a4eb \| tar -x -C /tmp/r30fx-considerthese/tree` → `EXTRACT_EXIT=0`; extraction contains `.ufo/` (7703 tracked files) and no `.git`. |
| B2 | `python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1` **plus** its `VERDICT: PASS` | **PASS** | Extracted tip `363a4eb`: `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully re-derives offline`, exit 0. Extracted **landing** `623c1fc`: byte-identical two lines, exit 0. Working tree: identical. |
| B3 | `plans/sources_adopt.py --selftest` → a `SELFTEST cases=N failed=0` line | **PASS at the landing, unpinned** | Extracted tip `363a4eb` prints `SELFTEST cases=10 failed=0`, exit 0; extracted **landing** `623c1fc` prints `SELFTEST cases=14 failed=0`, exit 0. The literal `N` never appears in any output: it is a metavariable, so this row has no pinned integer (finding M1). |
| B4 | `plans/registry_check.py --selftest` → CASE count | **PASS** | `SELFTEST clean cases=15 …`, exit 0 at `363a4eb` and at `623c1fc`. |
| B5 | `plans/config_projection.py --selftest` → CASE count | **PASS** | `SELFTEST clean cases=31 …`, exit 0 at both. |
| B6 | `plans/benchmark_spec_audit.py --selftest` → CASE count | **PASS** | `SELFTEST clean cases=67 …`, exit 0 at both. |
| B7 | `python3 plans/state_check.py --summary` "still applies separately" | **PASS on the working tree, AMBIGUOUS under extraction** | Working tree: `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5` + `VERDICT: PASS`, exit 0. Extracted `363a4eb` **and** extracted landing `623c1fc`: `match=316 … offline_unverifiable=7`, `VERDICT: PASS`, exit 0. Cause located: `plans/state_check.py:2680` needs `(candidate/".git")`; an extraction has none. Q20 names no environment (finding M3). |
| B8 | "the fleet census still apply separately" | **PARTIAL** | The noun has no command anywhere in `corpus/QUALITY.md` (only hit: line 208 itself). The only in-repo command is `corpus/lessons/round-29-verifier-spotcheck.md:38`: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`. I ran it → exit 0, 15 lines (14×`W04` + `ok`). Runnable, undiscoverable from Q20. |
| B9 | **Check:** run the named gates inside the extracted tree *and diff the count lines against the previous landing's receipt* | **FAIL as written** | There is no command, no receipt path, no format, and no commit→receipt map (finding **F1**). Q20's neighbours in the same file (R4, R10, R11, R12, R14) each state a runnable command; so did the seat's own draft (`R30Considerthese.md:137-148`, a `grep -qx` chain the seat proved exits 0 green / 1 on a deleted check). The landed text dropped it. |
| C1 | limit: "an exit-code-only criterion loses (deleting two `grader.py` selftest cases leaves `ALL PASS`, exit 0)" | **PASS as measurement** | Reproduced on `/tmp/r30fx-considerthese/del2` (S6+S7 case blocks removed): `EXIT=0`, **6** `[selftest] PASS` lines, final line `[selftest] ALL PASS`. Identical to the seat's P1. |
| C2 | limit: "— the pinned integer is the detector" (i.e. the remedy for C1) | **FAIL** | On the same del2 tree, every gate Q20 names is green: `grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1` + `VERDICT: PASS`, exit 0; `sources_adopt` cases=10 failed=0 exit 0; `registry_check`, `config_projection`, `benchmark_spec_audit` exit 0. The pinned integer is unchanged by the very attack the sentence cites. The real detector is the `[selftest] PASS` line count (7→6), which Q20 does not name and no roster row produces (finding **F2**). |
| C3 | limit: "the integer detects shrinkage, not correctness (a tautologised assertion keeps n=733)" | **PASS, both halves** | Shrinkage: deleting `rep.eq("r11.census.requests", …)` (`grader.py:1064` at tip) → `CHECKS n=732`, `VERDICT: PASS`, exit 0 (exit code and verdict blind, integer detects). Correctness: replacing the same assertion's RHS with a copy of its LHS → `CHECKS n=733`, `VERDICT: PASS`, exit 0, and all five roster gates green. Matches the seat's P2/P3. |
| C4 | limit: "this is not a non-author verifier (`QUALITY.md` R6 stands — **only a workflow run would make it one**)" | **FAIL (the parenthetical)** | `corpus/QUALITY.md:166` R6: "A verifier counts as non-author only when the report names an id outside the round's dispatch roster." No workflow requirement. The lane's own tip is a non-workflow non-author path: `363a4eb round-29 verifier spot-check (integrator, hyaku): non-author admit/reject`. The proposal says "the **cheapest** mechanical non-author verifier", not the only one. Finding **F4**. |
| C5 | limit: "cannot cover `plans/adoption_check.py`, **which is red by design**" | **IMPRECISE, conclusion holds** | `plans/adoption_check.py` has no `--selftest` at all (`add_argument`: `--lane`, `--expect`, `--census` only) — so the non-coverage conclusion is right. "Red by design" is not: with `--census` from the lane it is **green** (`corpus/evidence/round30/adoption-after.txt` → `entries=1 … census=ok` / `exit=0`; my extraction run without `--census` → `entries=1 … census=skipped`, exit 1, because `plans/adoption_check.py:131` sets `census_code = 1  # an unrun census is not a pass`). And in any `/tmp` extraction it is red **even with** `--census`: `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=fail`, exit 1, because `:132-137` derives the lane name from `lane.parent`/`lane.name` and shells to `CENSUS = /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (`:35`). Finding **M5**. |
| C6 | limit: "or the two selftests that print no count" | **PASS on the number, unnamed** | Enumerated every `plans/*.py` accepting `--selftest` (9 tools) in the landing extraction: `attrib_calibration` → `18 checks`; `benchmark_spec_audit` `cases=67`; `config_projection` `cases=31`; `grader_perturb` `caught=12`; `parser_policy_compare` `cases=59`; `registry_check` `cases=15`; `sources_adopt` `cases=14`; **`gate_timing_check` NONE**; **`state_check` NONE**. Exactly two, as stated — but Q20 never names them, and it *does* name `state_check.py --summary` elsewhere in the same bullet, so a reader can conclude state_check is covered. Finding **L3**. |
| D1 | "A commit touching `grader.py`, `plans/*.py`, `plans/*.sh`, the `corpus/SOURCES.md` schema or `.github/` must cite a run **extracted from the commit**" | **PARTIAL** | The trigger fires on the actual landing (`623c1fc`: `plans/*.py` ×3, `corpus/SOURCES.md` +6 rows) and on any sourcing round. But the run cannot exist *inside* the commit it certifies (the sha does not exist until after the commit), and Q20 says nothing about who appends the receipt, where, or in which commit — see D3/M2. |
| D2 | "A count that differs from the previous commit is a failure unless **the same commit's diff explains old→new with a reason**" | **FAIL as an acceptance condition** | A diff has no reasons (it has code), and "previous commit" vs "previous landing's receipt" (next sentence) are two different bases. The criterion's own landing is the first test: `sources_adopt` moves 10→14; the four added cases are `quote-overlong-refused`, `quote-absent-refused`, `quote-boundary-25-accepted`, `quote-located-accepted` (`comm -13` over the CASE labels), while frozen C3 (`plans/round-30-claims.md:79-81`) says "including two new failure-capable cases", and a peer critic already flags the arithmetic as unexplained (`R30CritC3.md:25`: "10 existing + 2 named = 12 ≠ 14"). Finding **M4**. |
| D3 | applies to the commit that lands it | **NOT SATISFIED** | `623c1fc` fires Q20 on its own trigger set: it changes `plans/sources_adopt.py` (+343), `plans/adoption_check.py` (+34), `plans/round30_defects.py` (new, 222) and `corpus/SOURCES.md` (+6). Its tree contains **no** reference to `623c1fc` (`git grep -c 623c1fc HEAD` → empty) and no extraction receipt: the committed receipts are `corpus/evidence/round30/gate-selftest-after.txt` (`SELFTEST cases=14 failed=0` / `exit=0`), `adoption-after.txt`, `census-after.txt`, `claims/gate-before.txt` — none binds a sha or a tree, and `LOG.md:833` says the gates were "re-run in the round's build seats", i.e. a working-copy run — precisely what Q20 excludes. Finding **M2**. |
| E1 | title: "a landing that touches **a gate** carries a mechanical run made outside the working copy" | **FAIL vs its own roster** | A commit touching a gate outside the five-row roster satisfies Q20 with a run that never exercises the touched gate. Probe on `/tmp/r30fx-considerthese/loophole`: `plans/grader_perturb.py` mutated to expect `caught=13` → its own gate `SELFTEST MUTATION-CATCH FAIL: caught=12 expected=13`, `SELFTEST TOTAL families=10 branch_cases=10 failed=1`, **exit 1**; meanwhile `grader.py` n=733 PASS, `sources_adopt` cases=10 failed=0, `registry_check` 15, `config_projection` 31, `benchmark_spec_audit` 67 — every gate Q20 names, green. The seat's draft closed this with "plus the touched tool's own row when the change is not one of those four" (`R30Considerthese.md:143-144`); landed Q20 dropped the sentence. Finding **F3**. |
| E2 | claims no more than a mechanical run proves | **MOSTLY PASS, one provenance gap** | Correctly disclaims correctness (C3) and non-author (C4, modulo its error). But "must **cite** a run made in a landing tree extracted from the commit" is testimonial: nothing in the lane compares a pasted receipt to a tree, so a receipt copied from the working copy is indistinguishable from an extracted one by every in-lane mechanism. Q20 is a citation standard whose central provenance guarantee is unenforced — it does not say so. Folded into **F1**'s residual risk. |
| F1 | absence checks: `ls .github` → no such file or directory; `grep -n 'author-observed, never non-author closure' LOG.md` → `LOG.md:372` | **PASS** | `ls .github` → `ls: cannot access '.github': No such file or directory`, exit 2; `git log --all --oneline -- .github` → 0 lines; `grep -n …` → `372:  actual-commit measurement follows. Receipts are author-observed, never non-author closure.` |
| G1 | consistency with the lesson row | **DRIFT** | `corpus/lessons/round-30.md:24` says Q20 was "drafted against **15** gates that run offline in ≤2 s". The seat measured 15 (build report G1-G15) and drafted **9** pinned rows; Q20 names **5**. A reader of the lesson row expects 15. Finding **L4**. |

---

## 2. Findings, by severity

### F1 — HIGH (operability). The Check clause is not a command and names no receipt.
`QUALITY.md:207-208`: "Check: run the named gates inside the extracted tree and diff the count lines against the
previous landing's receipt". No command, no path, no format, no mapping from a commit to a receipt. The artifacts
that exist are per-round and one-sided: `.ufo/waves/round-30/claims/gate-before.txt` (before only:
`SELFTEST cases=10 failed=0` / `selftest_exit=0`), `corpus/evidence/round30/gate-selftest-after.txt` (after only),
`corpus/evidence/round29-calibration/actual-gate.txt` (a Q13 `gate_timing_check` receipt, not a count receipt),
`LOG.md:702` (counts in prose). Nothing in `corpus/QUALITY.md` defines "receipt" or a receipt location; every
neighbouring criterion states a runnable command. The seat had one and the landing removed it. A fresh agent can
reproduce the roster (I did) but cannot perform the second half of the Check.

### F2 — HIGH (calibration). The stated remedy for the selftest-deletion attack is not implemented, and is false.
Q20: "an exit-code-only criterion loses (deleting two `grader.py` selftest cases leaves `ALL PASS`, exit 0) — the
pinned integer is the detector". Reproduced: after deleting S6+S7, **all five roster gates pass**, `grader.py`
still prints `CHECKS n=733 mismatches=0 errata_pinned=1` and `VERDICT: PASS`, exit 0. The pinned integer is blind
to this attack; the detector is the `[selftest] PASS` count, which the seat's draft required ("`[selftest] ALL
PASS` with seven `[selftest] PASS` lines") and landed Q20 does not require — `grader.py --selftest` is not in the
roster at all. The clause therefore teaches a remedy the criterion does not perform.

### F3 — HIGH (calibration). Narrowed roster vs. a trigger that still fires on every gate.
Trigger covers `plans/*.py` (14 files, 9 with `--selftest`); the roster covers 5 gates. A landing that breaks
`plans/grader_perturb.py`, `plans/parser_policy_compare.py` or `plans/attrib_calibration.py` — or
`grader.py --selftest` — satisfies Q20 with a fully green receipt (loophole probe above: touched gate exit 1,
`failed=1`; all five roster gates exit 0). The title promises coverage of "a landing that touches a gate"; the
body delivers coverage of five named gates plus whatever the author volunteers. Fix is one sentence (the seat's
own "plus the touched tool's own row"), and its absence is the difference between the draft and the landing.

### F4 — MEDIUM-HIGH (overclaim). "only a workflow run would make it one" contradicts R6 and the lane's practice.
`QUALITY.md:166` (R6) defines non-author by roster membership of the verifier id, with no workflow anywhere in it;
`363a4eb` is itself the commit "round-29 verifier spot-check (integrator, hyaku): non-author admit/reject". The
proposal's own words are "the cheapest mechanical non-author verifier available". A reader who takes Q20 at face
value will believe no non-author closure is possible without GitHub Actions, which is false and would retire a
mechanism the lane already uses.

### M1 — MEDIUM. Four of the five roster rows carry no pinned integer.
Only `grader.py` has a literal (`n=733`). `sources_adopt` prints a literal `N`; registry/config/benchmark are
"their CASE counts" with no value. So "the pinned count line of every gate it names" is true for one gate. The
entire pinning load falls on the count-diff rule — which is exactly the part F1 shows is unimplementable.

### M2 — MEDIUM. No artifact says who appends the receipt, and the first gate-touching landing has none.
"a gate run made in a landing tree extracted from the commit" requires the commit to exist first, so the receipt
necessarily post-dates it; Q20 does not say whether it is amended in, appended in a follow-up, or written to
`corpus/evidence/round<N>/`. The actual landing shows what happens without that rule: `623c1fc` changes
`plans/sources_adopt.py` (+343), `plans/adoption_check.py` (+34), `plans/round30_defects.py` (new, 222) and
`corpus/SOURCES.md` (+6) — a full firing of Q20's trigger — yet `git grep -c 623c1fc HEAD` returns nothing, none
of the committed receipts in `corpus/evidence/round30/` binds a sha or a tree, and `LOG.md:833` records the gates
as "re-run in the round's build seats" (a working-copy run, the exact thing Q20 excludes). No round-30 artifact
plans a post-landing extraction (`grep -rln 'post-landing' .ufo/waves/round-30/` → nothing). Q20 landing without
its own first receipt is defensible only if the criterion says so; it does not.

### M3 — MEDIUM. `registry_check`/`config_projection`/`benchmark_spec_audit` counts are environment-stable; `state_check` is not.
`state_check.py --summary` reports `match=318 offline_unverifiable=5` in the working tree and `match=316
offline_unverifiable=7` in an extraction of the same bytes, because `plans/state_check.py:2680` requires `.git`.
Q20 invokes both environments in one sentence ("inside the extracted tree … `state_check.py --summary` … still
apply separately") and says nothing about the shift, so a fresh agent diffing the summary against a lane receipt
sees a two-assertion discrepancy that is an artefact of the criterion's own instruction sequence.

### M4 — MEDIUM. "the same commit's **diff** explains old→new with a reason" names an artifact that cannot carry a reason.
What the landing actually did: `LOG.md` §C3 states "Selftest 10 → 14 cases; the ten original cases keep their
names and verdicts and the five pre-existing invocations are stdout/exit identical" — old, new and a reason, in
the same commit but in prose, not in the diff. The four added `CASE` labels are `quote-overlong-refused`,
`quote-absent-refused`, `quote-boundary-25-accepted`, `quote-located-accepted` (`comm -13` over the CASE labels of
`363a4eb` vs `623c1fc`), while the frozen claim (`plans/round-30-claims.md:79-81`) names two as failure-capable
and `R30CritC3.md:25` flags the arithmetic ("10 existing + 2 named = 12 ≠ 14 … two cases unspecified"). So the
round satisfied the rule in substance and not in letter; a future landing is owed a rule it can satisfy as
written. Say "the round's receipt states `old=`, `new=`, `reason=`", or drop "diff".

### M5 — MEDIUM. "red by design" misdescribes `adoption_check.py`, and the extraction instruction makes it red anyway.
Two independent reasons it is outside the roster: (1) it has no `--selftest`; (2) its `--census` step is
path-dependent (`plans/adoption_check.py:132-137` builds the lane name from `lane.parent`/`lane.name` and shells
to a hardcoded fleet path at `:35`), so in a `/tmp` extraction it prints `census=fail` and exits 1 regardless of
the landing's health. A fresh agent following Q20's
extraction instruction and then running the "red by design" gate will see a red and cannot tell it from a real
breakage. Say "no `--selftest`; `--census` is fleet-path dependent" instead.

### L1 — LOW. "the fleet census" is undefined inside QUALITY.md.
No command in the file; the only discoverable one is a round-29 lesson line. I ran it: exit 0, 15 lines. Resolvable
by search, not by reading the criterion.

### L2 — LOW. `cases=N` reads as a literal to a fresh agent.
The single gate Q20 pins a count for is `sources_adopt`, and at this landing its value moves 10→14. Until L1-style
wording ("the receipt states the value; a change is governed by the count rule below") replaces `N`, the row is
self-inconsistent with "pinned".

### L3 — LOW. The two count-less selftests are never named (they are `gate_timing_check` and `state_check`).
Verified by enumerating all nine `--selftest` tools in the landing extraction. Naming them costs four words and
removes an enumeration step.

### L4 — LOW. Lesson-row drift: "drafted against 15 gates" vs Q20's 5.
`corpus/lessons/round-30.md:24`. The seat's roster was 15 rows (G1-G15), its draft pinned 9, the criterion names 5.
The row should say "5 of the 15 measured", or the criterion should be widened to match the row.

### L5 — LOW. Exit-code capture is a trap the criterion does not warn about.
Q20 requires "printing the exit code"; the tools print counts to stdout. `python3 plans/sources_adopt.py --selftest
2>&1 | head -3` → `PIPESTATUS0=1` on a passing gate (broken pipe), while the direct run exits 0. Any receipt
captured through `head`/`tail`/`grep -m` records a false failure. One sentence ("capture `$?` before any
truncating pipe") prevents a class of false reds.

---

## 3. What checked out

- Every gate Q20 names exists, runs offline today, and prints exactly the line attributed to it, both in a `git
  archive 363a4eb` extraction and in a simulated landing extraction (clone → commit working tree → `git archive`),
  where `sources_adopt` moves to `cases=14`.
- The extraction form works verbatim: `git archive 363a4eb | tar -x -C …` exit 0, `.github` absent from the
  extracted tree exactly as Q20's absence check says.
- `state_check.py --summary` exits 0 with `mismatch=0` and `VERDICT: PASS` in both environments; the count shift is
  disclosed above, not a mismatch.
- The three limits the seat measured are reproducible on my own copies: exit code blind to deleted selftest cases
  (`ALL PASS`, exit 0, 6 PASS lines); integer blind to a tautologised assertion (`n=733`, `VERDICT: PASS`, exit 0);
  integer detects a deleted replay check (`n=732`, exit 0). The seat's numbers are honest.
- The proposal's two premises hold byte for byte (`ls .github` exit 2; `LOG.md:372` verbatim), and the criterion
  correctly refuses to claim non-author status for its own receipts.
- `grader.py` is stable across this landing: `n=733`, `errata_pinned=1`, `VERDICT: PASS`, exit 0 on the working
  tree, so the pinned literal is not stale yet.

---

## 4. Executable by a fresh agent without oral context?

**Partly.** The mechanical half is: a fresh agent can extract, run the five named gates, and match four count
lines and one replay line exactly (I did, twice, from scratch). The judgment half is not: the Check gives no
command, "the previous landing's receipt" has no location, `cases=N` is not a value, "the fleet census" has no
command in QUALITY.md, the two count-less selftests are unnamed, "the `corpus/SOURCES.md` schema" has no boundary
(a fresh agent cannot decide whether appending rows S081-S086 fires Q20; I judged it does not, because
`plans/sources_adopt.py:14` defines the schema as the 11-cell staged-row contract, but that is my inference, not
the criterion's), and the count-diff verdict depends on a reason the criterion says lives in a diff. Two clauses
are actively wrong for a reader: "the pinned integer is the detector" (F2) and "only a workflow run would make it
[non-author]" (F4).

VERDICT: FAIL — Q20's five-gate roster is executable and reproducible byte for byte, but its Check clause, its
count-diff rule, and two of its four stated limits do not survive contact with the bytes; the criterion is
satisfiable by a green run that never exercises the gate the commit touched.

---

## 5. What must change for Q20 to pass (short, since this seat does not edit)

1. Restore an executable Check (the seat's `grep -qx` chain, updated to `cases=14` for this landing, or a count
   diff against a named receipt path such as `corpus/evidence/round<N>/gate-<tool>-after.txt`).
2. Add the seat's dropped sentence: "plus the touched tool's own row when the change is not one of these five."
3. Replace "only a workflow run would make it one" with R6's rule as written (a verifier id outside the dispatch
   roster).
4. Either pin `sources_adopt` to a value and let the count rule govern moves, or delete "pinned … of every gate it
   names".
5. Name the two count-less selftests; name the fleet-census command; say which environment `state_check --summary`
   applies in and that `offline_unverifiable` moves by two under extraction.
6. Say who produces the post-landing receipt, in which commit, and at which path.

## 6. Residual risk and verification gaps

- I did not find, and did not exhaustively exclude, a checked-in fixture that already pins `n=733`:
  `grep -rn 733 plans/*.py plans/fixtures` returns no gate expectation. If one exists, Q20's first row is a
  transcription rather than a new pin.
- The provenance of a pasted receipt is unverifiable in-lane by construction; I did not attempt to build a
  verifier for it, and Q20 claims none. That is the criterion's largest unstated residual risk, not a bug I can
  close.
- I audited the criterion, not the C1 entry: this report names no candidate path and gives no entry verdict, and
  must not be cited as a C1 second-seat re-read.
- Simulated landing: I committed the working tree in a throwaway clone under `/tmp` to get a real `git archive`
  landing sha; the lane was never committed to, amended, or checked out.

## 7. Tooling record

No installs, no upgrades, no package-manager transactions (`pacman` is paused host-wide; nothing needed one).
Tools used: `git`, `python3`, `rsync`, `comm`, `diff`, `tar`. `/usr/bin/time` is absent on this host, so no wall
times are claimed. Scratch: `/tmp/r30fx-considerthese/{tree,del2,taut,shrink,loophole,clone,landed}`; the lane
received only this file.
