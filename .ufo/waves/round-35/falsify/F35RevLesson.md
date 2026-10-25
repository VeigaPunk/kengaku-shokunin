# F35RevLesson — falsify review of `corpus/lessons/round-35.md` (round 35, wave 2, 2026-10-25)

Seat: F35RevLesson (reviewer). Lane tip judged: `dfee6fff631ebc5f623ba4506e5c7992a215401c` (`git rev-parse master` → same). Baseline `58a19f37…`; freeze `11d64530179b78e33ba6074fc77d63d36ee7ac31` (object exists, `git cat-file -t` → `commit`; `git diff 11d64530..master -- plans/round-35-claims.md` → empty).

Method: no lsp server exists for corpus Markdown — every semantic check below is grounded in git-tree bytes (`git show master:`), executed read-only lane counters, or a per-rule fixture clone (shared `--no-checkout` clone, sparse checkout, `checkout dfee6fff…`, `git rev-parse --show-toplevel` verified equal to the clone before any write, commits only inside the clone as `fixture <fixture@invalid>`, exact-path `rm -rf` at the end). No lane file was edited. Text grep was used only as the literal fallback and each hit was confirmed against tree bytes or a receipt.

## Findings by severity

### F1 — HIGH: the QUALITY Q13 executable check is red at the landed tip and at the admitting commit; no admit cites a second-seat re-read report

Q13 (`corpus/QUALITY.md`): "an admit lands only after its second-seat re-read is on record … the Gate cell names each such report by repo-relative path … Check: `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-35.md --commit <admitting commit>` exits 0."

**Layer A — the landed Gate table defeats the checker's parser.** `plans/gate_timing_check.py:169-183` only recognizes a Gate header containing the columns `{candidate, decision, reason}`; round-35's header is `| Candidate | Verdict | Reason and flip condition |` (round-35.md:7). Every row is therefore skipped (`header is None`) and zero admits are found:

```
$ python3 plans/gate_timing_check.py --lesson corpus/lessons/round-35.md --commit dfee6fff631ebc5f623ba4506e5c7992a215401c
gate_timing_check: FAIL: no admit rows in ## Gate of corpus/lessons/round-35.md at dfee6fff…
gate_timing_check: admissions=0 passed=0 failed=1
exit=1
```

Same exit=1 "no admit rows" at the admitting commit `4fe72a9aab65…` (which adds the entry + lesson), and at `6ac9611`, `056e192`. Control: the parseable schema `| candidate | decision | reason |` exists in the lessons of rounds 25–29 (`grep -rl '| candidate | decision | reason |' corpus/lessons/` → round-25…round-29); rounds 32–35 switched to `| Candidate | Verdict …`. Round 35 is the first round with entry admits since round 29, so the round-32 header regression bites here for the first time.

**Layer B — on the merits, no admit cell names any second-seat report.** In a fixture clone at the tip, with only the header schema corrected (one-line change, committed inside the clone as `fixture`), the checker parses all four admit rows and every one fails:

```
== P1 Q13 layer 2: fix Gate header schema to candidate/decision/reason, re-run Q13 check
$ python3 plans/gate_timing_check.py --lesson corpus/lessons/round-35.md --commit HEAD   [rc=1]
FAIL line 11 Gate admit: candidate='knowledge/tb2-protein-assembly-grader.md (C1)'
  cited seat-report paths: none
  reasons: admitted candidate is absent from the commit tree; no cited, existing, returned second-seat report for this round
FAIL line 12 Gate admit: candidate='S105 tests/testoutputs.py @ 2fd12b88'   … cited seat-report paths: none
FAIL line 13 Gate admit: candidate='S106 tests/test.sh @ 2fd12b88'          … cited seat-report paths: none
FAIL line 14 Gate admit: candidate='S107 instruction.md @ 2fd12b88'         … cited seat-report paths: none
```

The C1 cell's only "re-check" citation is a script (`plans/round35_c1_verify.py` V3), which is not a second-seat report. Wave-1 re-read reports that could be cited do exist in the tip tree (`.ufo/waves/round-35/build/` has 32 committed reports incl. `R35IndepGrader.md`, `R35RevClaims.md`), but no Gate cell names any repo-relative path — the only repo-relative report citation in a Gate row sits on the non-admit S091 row (`.ufo/waves/round-35/build/R35ScoutQuarantine.md`). Note also the ` (C1)` suffix defeats candidate-path resolution ("admitted candidate is absent from the commit tree") even though `corpus/knowledge/tb2-protein-assembly-grader.md` is in the tree.

Timing note: Q13 requires the support inside the admitting commit (`4fe72a9`); that cannot be retrofitted. Repair path: cite the in-tree wave-1 reports by repo-relative path in the Gate cells, land the falsify reports, re-run the checker, and append an erratum acknowledging the timing half for `4fe72a9` (R1-style, no rewrite).

### F2 — MEDIUM: `## Mistakes` row 5 ("probe case label confounded") is the only fix not shown able to fail; no frozen check guards it

Rows 1–4 are guarded: row 1 by hardening H5 counterexamples CE3/CE4 plus ledger `R34-D5` red at freeze; rows 2–3 by ledger rows `R34-D2`/`R34-D3` red at freeze (`.ufo/waves/round-35/claims/control-c2-nothing.txt` — I read it: all five rows `observed=fail` at freeze, `PREDICATE C2 fail`, exit=1); row 4 by H1–H5 on CE1–CE5 (`corpus/evidence/round35/hardening-counterexamples.txt` — I read it: CE1 fails H1+H2+H3, CE2 H4, CE3 H5, CE4 H5, CE5 H2, exactly as the lesson claims).

Row 5's fix ("the entry states the confound and lists the three instruction bullets no case exercises; the frozen case table is unchanged") has content in the entry (tip bytes: case-table row at entry line 65 `do not repeat a protein (stated for the antibody binder; the probe repeats the donor)`; the three-bullet list at entry lines 81–84, citing `R35RevProbePred`) — but nothing frozen fails when that content is deleted. Fixture repro (same clone, tip bytes, baseline `checks=6 defects=0` and `hardening run=5 failed=0`):

```
== P2 row-5 fix guard: delete the confound case row from the entry, re-run both counters
$ python3 plans/round35_c1_verify.py --lane .   [rc=0]
V1..V6 ok / checks=6 defects=0 / PREDICATE C1 pass
$ python3 plans/round35_hardening.py --repo . --lane . --skip H6   [rc=0]
H1..H5 ok / hardening run=5 failed=0
```

`plans/round35_hardening.py:26` hashes only the three instruments (`FROZEN = ["plans/tb2_grader_probe.py", "plans/round35_c1_verify.py", "plans/defect_ledger.py"]`) — the entry is not protected by H1, and no V-check reads the confound row. The gate item "each fix is shown able to fail" is unmet for row 5.

### F3 — LOW: false word-count annotations in the new rows S105 and S107, under the counter's own counting convention

V3 enforces the ≤25-word rule on whitespace tokens (`plans/round35_c1_verify.py:128` `if len(quote.split()) > 25`). Measured (`printf '%s' '<quote>' | wc -w`): S105 quote = **11** tokens (row and lesson annotate "(9 words)"); S107 = **15** tokens (annotated "(16 words)"); S106 = 4 (annotated "(4 words)" — correct, and computed by the same whitespace convention, so the convention is also applied inconsistently within the same round's rows). Neither quote breaches ≤25, so Q3 holds; the annotations are false numbers in admitted rows, and no frozen check reads them — fixture P3: correcting "(9 words)"→"(11 words)" and "(16 words)"→"(15 words)" keeps `checks=6 defects=0` (rc=0). Q10's "numbers re-read by a second seat" is the bar these miss.

### O1 — observation (not counted): uncommitted round-owned edits in the lane worktree during wave 2

`git status --porcelain` (observed 2026-10-25, during wave 2): 7 lines, including ` M corpus/README.md` (+1 line: "Correction (round-35 falsify wave)…") and ` M corpus/knowledge/tb2-protein-assembly-grader.md` (+21 lines: "## Errata (appended round 35, falsify wave…"), plus 5 untracked `falsify/` peer reports. These are the round-34-D1 class ("uncommitted round work"); they must be committed (or restored) before the round closes. Not attributed to a seat; state may have moved since.

## Agreement items — each with the check that would have falsified it

1. **Gate composition.** Gate holds 4 admits (C1 entry; S105/S106/S107 "Admitted (mined)") and 5 non-admit dispositions. "≥1 reject from the assimilation set" holds: `toolathlon-grader-behaviour-probe-2026-10-23.md` and `terminal-bench-release-identity.md` **Refused**; S091 re-grounded/not appended; S105-staged not appended; `grader-predicate-input-types.md` held — each matching wave-1 receipts I read (`R35ScoutMergePkg.md` §REFUSE R2/R7, §ADMIT-CANDIDATE A1; `R35IdGuard.md`: 21 collisions S077–S104, indented-`S002` guard proof, quarantine slice 2 rows). The canonical build requirement (`.ufo/waves/round-35/build-spec.json`, R35LessonDraft task) is "≥1 reject from the assimilation set" — satisfied. Zero assimilation candidates admitted is consistent with the CORPUS rule 4 reasoning recorded in the dispositions themselves. (Admits come from the frozen claims pipeline, not the assimilation set; that is the spec'd shape, not a defect.)
2. **New SOURCES rows.** S105/S106/S107: pinned raw URLs, tier A, `mined`, access date 2026-10-25, 180d recheck, used-by the entry (V2 clauses verified at tip in my fixture P0). Quotes located and byte-verified by me: `test_outputs.py:42` = `assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (`; `test.sh:27` = `echo 1 > /logs/verifier/reward.txt` and `:21` = `-w biopython==1.85`; `instruction.md:29` = `The GS linkers … 5 and 20 amino acids long.` (`:raw:` reads). I recomputed the three sha256 myself; all equal the row pins (`44a05a24…96582`, `9ede4664…267b5`, `1bb2af1d…003f7c5`). Quote lengths 11/4/15 whitespace tokens — all ≤25 (annotation blemish → F3).
3. **Mistakes table format.** 5 rows × exactly `class | evidence pointer | captured-by | fix` ✓. Evidence pointers verified: `round-34-verifier-spotcheck.md:31` is the D2 row (106,323 blobs / 1650.6 MiB) and `:64` the D5 S091 disagree row ✓; wave-1 reports cited (`R35CritControls.md` line 108 `checks=6 defects=0` on the junk package; `R35CritC2.md` §2–3 D4/D5 false-but-labelled counterexamples; `R35MutC1Quotes.md` M4 SURVIVES; `R35MutC1V4V5.md` M8 SURVIVES; `R35RevProbePred.md` F1) all exist and say what the lesson says ✓. Fixes able to fail: rows 1–4 yes (receipts read; see F2), row 5 no (F2).
4. **Census.** Before/after pasted with exit codes ✓; receipts `census-before.txt`/`census-after.txt` byte-identical (`diff` → exit 0), each ending `exit=0`; my fresh re-run of the lesson's exact command reproduces 15 W04 + `kengaku ok` + exit=0. Registry 97 → 100 by my own grep at both revs (`git show 58a19f37…:corpus/SOURCES.md | grep -cE …` → 97; tip → 100). `git diff --stat 58a19f37..master` on the round's files: SOURCES +3, README +10, round-34.md +4, round-35.md +43, QUALITY.md +24 — pure insertions, so "added by tier 3/0/0", "rows touched old→new: none" hold; README diff shows the index row (line 68), coverage-map bullet (line 257) and frontier discharge (line 282) landing in the same commit range as the entry (Q7 ✓).
5. **Round-34 erratum.** Appended (`round-34.md` diff = +4 lines only; the old "quote absent" Gate row survives byte-intact at round-34.md:11 — R1 append-only holds). Erratum facts re-verified by me: `nec-s091-reopen.html` is 60,335 B and the staged RAKUDA quote is present at raw line 276 after tag-strip (grep hit = 1); erratum cites `round-34-verifier-spotcheck.md:64`, which is exactly the S091 disagree row ✓.
6. **Q23 (`corpus/QUALITY.md`).** Consistent with the landed implementation: `corpus/defects.jsonl` holds the five round-34 rows with per-row checks, sources `spotcheck.md:75-79`, and `recurrence_of` recorded-not-enforced; Q23's cited red receipts exist and show what it claims (`control-c2-nothing.txt`: five rows red at freeze; `control-c2-flip.txt`: `rows=5 closed=5 observed_pass=1 mismatches=4`, exit=1); `plans/round-33-claims.md:87` is the cited N1 line ✓. At the tip my own run reproduces the frozen C2 predicate: `rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE C2 pass`, exit=0 ✓. Q23's limits paragraph matches the lesson's assimilation record (parts (b)/(c) not implemented) ✓.

## Residual risk and verification gaps

- Upstream bytes were not re-fetched live; the pinned raw URLs + local capture digests (which I recomputed) are the canonical bytes, and the entry's falsifier names the re-fetch procedure.
- `gate_timing_check.py`'s seat-registry/role logic beyond parse + citation behavior was not re-derived; P1 exercised parsing and citation absence only.
- The entry's 22-row quote table was not re-verified line-by-line by me (V3 green at tip in my own fixture run, H2 receipt `rows=22 unparsed=0`; I spot-verified 3 quotes byte-exact).
- O1 is unattributed and may have changed since observation.
- Wave-1 receipt equality claims (C1 V5) were re-run green in my fixture but the probe's internal predictions-vs-observations mapping was not independently re-audited (other seats own C1 depth).

VERDICT: lesson-3-defects
