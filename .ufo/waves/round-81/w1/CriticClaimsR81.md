# CriticClaimsR81 — coverage / calibration

Read-only attack report. No lane implementation edits, commits, installs, or runtime delegation. Frozen claims read in full before commands. Initial master was `60123c7f7bb8abd06c7d273a3f09c70889b81e25`; the later clean shared clone measured `7ca4947796cb2429aef725c43eb2ee2339e2ba46`. The branch moved during this seat; these are explicitly different observations, not one immutable measurement.

## Findings and smallest safe corrections

### C1: executable evidence is stronger than a ledger flip

The committed instruments import `/cap/test_outputs.py` and call two log-summary / three vulnerable-secret test functions in bubblewrap sandboxes over 12 constructed artifacts each. They verify a literal capture SHA before running. Thus the inspected instruments are not canned printers. The successful clean-clone counter reproduced 13 projected lines per member and the population gate reported 26 executed, zero unlocated. The ledger-only skip lost.

Selection is maximum assert count with all ties retained, not alphabetical selection: `derive_universe` sorts only iteration order and retains every candidate at `max(asserts.values())`. Both before and after runs printed eleven candidates, maximum five, and the same two members.

**Fixable implementation gap, coverage:** `check()` calls `derive_universe(base_doc, tree)`: the ledger comes from BASE_REV, but capture existence/imports/assert counts come from the measured tree. The frozen universe definition requires the base captures. [INFERENCE] A later committed capture edit could change eligibility or the maximum and therefore change the universe. No such adversarial edit was built or scored here. Smallest correction: derive against a BASE_REV tree while retaining measured-tree capture SHA checks for replay. This is a counter implementation issue, not permission to reopen the frozen rule.

**Trust boundary, coverage:** the tool SHA binds a receipt to measured-tree instrument bytes, not independently to the freeze revision. [INFERENCE] A committed replacement printer plus updated receipt hashes can reproduce its own output; this counter alone does not establish that arbitrary replacement code runs the grader. No replacement-printer control was executed, so this is not a demonstrated target-reaching control. The inspected actual tools do run the captures. Smallest safe correction is explicit immutable instrument provenance/review; do not claim the replay counter itself proves arbitrary instrument honesty.

**Environment limitation:** receipts explicitly stamp `Python 3.14.8` and OpenSSL 3.6.5. Counter source compares both fields to freshly queried host values and emits HOST-PYTHON-MISMATCH / HOST-OPENSSL-MISMATCH. This is checkable by another reader, but version strings do not identify all interpreter/library/bwrap bytes, and the sandbox invokes `/usr/bin/python3` independently of the outer configurable interpreter. No real drift injection was executed by this seat; drift failure is source evidence, not an exercised result.

### C2: six closures passed, including counter sensitivity

Command:

`python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round81_c2_spotcheck_debt.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --work /fast/scratch/hyaku/kengaku-r81/CriticClaimsR81/w2`

Output:

```text
DEBT-TOTAL ids=6 registered=6 closed=6 checks_passed=6
INDEX corpus/lessons/round-80-verifier-spotcheck.md indexed=yes
DEFECTS n=0
TARGET ids=6 closed=6 checks_passed=6 indexed=yes
PREDICATE R81-C2 pass
RC=0
```

Source inspection confirms verdict mode calls sensitivity, which replaces each row's evidence_path with base bytes (or deletes a new file) and demands its check fail. The zero-defect run therefore reports sensitivity success for all six. This is not six independently logged full-base check executions: restoring one repair artifact is narrower than checking out the whole base.

| Id | Tracked close artifact | Literal id present, as checked by successful counter | Repair-removal check |
|---|---|---|---|
| R80-U1 | corpus/SOURCES.md S259 | yes; `supersedes S258` also required | fails with SOURCES base bytes |
| R80-U2 | SCORECARD.md erratum | yes; `e985e56a` also required | fails with SCORECARD base bytes |
| R80-U3 | corpus/evidence/round81/census-rows.txt | yes; `rows=249` also required | fails when new receipt deleted |
| R80-U4 | corpus/evidence/round81/r80-u4-red-before.txt | yes; Bio error literal also required | fails when new receipt deleted |
| R80-U5 | SKILL.md registry | yes; round80 gate name also required | fails with SKILL base bytes |
| R80-U6 | corpus/lessons/round-81.md Corrections | yes | fails when new lesson deleted |

U1/U2/U5/U6 are documentation/registry repairs, not new runtime behavior; U2 and U6 are principally prose corrections. That is consistent with their routed defects. U3/U4 carry command/negative-run receipts. I did not independently execute each row's check against a full base checkout and therefore do not assert that stronger test passed.

**Fixable implementation gap, calibration:** the C2 close resolver accepts a reachable commit as an alternative to a tracked file; that branch checks ancestry but not the id/evidence_literal in repair bytes. The actual six rows use tracked artifact paths, so this is not an observed false closure among them. Smallest correction: enforce the frozen tracked-artifact requirement rather than accepting bare commit ancestry.

## Exercised before/after evidence

Commands used absolute counter and lane paths, with --work under this seat's scratch.

C1 before:

`python3 $L/plans/round81_c1_new_members.py --lane $L --rev 4e833e9f --work $S/w`

```text
CANDIDATES n=11 rule=stdlib-only-unattempted-max-asserts asserts=5 code-from-image,count-dataset-tokens,crack-7z-hash,extract-moves-from-video,fix-ocaml-gc,gcode-to-text,log-summary-date-ranges,mteb-leaderboard,mteb-retrieve,sqlite-db-truncate,vulnerable-secret
UNIVERSE members=2 log-summary-date-ranges,vulnerable-secret
LEDGER-GATE skipped=4e833e9f
DEFECT RECEIPT-UNTRACKED log-summary-date-ranges corpus/evidence/round81/log-summary-date-ranges-probe.txt
DEFECT RECEIPT-UNTRACKED vulnerable-secret corpus/evidence/round81/vulnerable-secret-probe.txt
DEFECTS n=2
TARGET members=2 located=0 reproduced=0 ledger_flipped=0 defects=2
PREDICATE R81-C1 fail
RC=1
```

Initial live-worktree after command was the same without --rev. It failed while another seat was editing a tracked wave deliverable:

```text
LEDGER-GATE rc=0 LEDGER rows=88 executed=26 unlocated=0 unexecuted=62
DEFECT WORKTREE-DIRTY log-summary-date-ranges M .ufo/waves/round-81/w1/ProbeVulnSecretR81.py
DEFECT WORKTREE-DIRTY vulnerable-secret M .ufo/waves/round-81/w1/ProbeVulnSecretR81.py
DEFECTS n=2
TARGET members=2 located=0 reproduced=0 ledger_flipped=2 defects=2
PREDICATE R81-C1 fail
RC=1
```

This is a real refusal of dirty measurement, not a clean-tip failure. One permitted shared clone was then created:

`git clone --shared -q $L $S/clone`

`python3 $L/plans/round81_c1_new_members.py --lane $S/clone --work $S/wc`

```text
CLONE tip 7ca4947796cb2429aef725c43eb2ee2339e2ba46
UNIVERSE members=2 log-summary-date-ranges,vulnerable-secret
LOCATED log-summary-date-ranges receipt=corpus/evidence/round81/log-summary-date-ranges-probe.txt subject=tb2-header verdict=predicate
REPRODUCED log-summary-date-ranges lines=13
LOCATED vulnerable-secret receipt=corpus/evidence/round81/vulnerable-secret-probe.txt subject=tb2-header verdict=predicate
REPRODUCED vulnerable-secret lines=13
LEDGER-GATE rc=0 LEDGER rows=88 executed=26 unlocated=0 unexecuted=62
DEFECTS n=0
TARGET members=2 located=2 reproduced=2 ledger_flipped=2 defects=0
PREDICATE R81-C1 pass
RC=0
```

C2 before:

`python3 $L/plans/round81_c2_spotcheck_debt.py --lane $L --rev 4e833e9f --work $S/w2`

```text
DEFECT DEBT-UNREGISTERED R80-U1
DEFECT DEBT-UNREGISTERED R80-U2
DEFECT DEBT-UNREGISTERED R80-U3
DEFECT DEBT-UNREGISTERED R80-U4
DEFECT DEBT-UNREGISTERED R80-U5
DEFECT DEBT-UNREGISTERED R80-U6
DEFECT INDEX-MISSING corpus/lessons/round-80-verifier-spotcheck.md
DEFECTS n=7
TARGET ids=6 closed=0 checks_passed=0 indexed=no
PREDICATE R81-C2 fail
RC=1
```

## Cheapest skips scored with frozen counters

For each C1 switch, ran `python3 $L/plans/round81_c1_new_members.py --<switch> --work $S/w`; C2 ran `python3 $L/plans/round81_c2_spotcheck_debt.py --control-presence --lane $L --work $S/w2`. These invoke the counters' fixture builders, not handcrafted lane edits.

```text
CONTROL flip-ledger-only located=0 ledger_flipped=0 defects=2 codes=RECEIPT-UNTRACKED target_reached=False
CONTROL header-only located=0 ledger_flipped=2 defects=50 codes=COMMAND-TOOLLESS,EXIT-NONZERO,HOST-OPENSSL-MISMATCH,HOST-PYTHON-MISMATCH,LEDGER-VERDICT,MINTED-BY,OBS-EMPTY,STAMP-MEMBER,STAMP-MISSING,SUBJECT-CAPTURE,SUBJECT-SHA-MISMATCH,TOOL-PATH,TOOL-SHA-MISMATCH target_reached=False
CONTROL copy-observations located=1 ledger_flipped=1 defects=1 codes=REPRODUCTION-MISMATCH target_reached=False
CONTROL presence ids=6 closed=6 defects=18 codes=CHECK-TRIVIAL,CLOSE-NOT-REPAIR,SOURCE-LINE
CONTROL presence target_reached=False
```

Control stdout was filtered through `grep -E 'CONTROL|DEFECT'`; the printed RC=0 in that shell was the filter's exit status, not independently captured counter status. The target_reached=False lines are the reliable scored observations. No exercised cheap control reached target.

Could not break: receipt replay on committed clone; ledger-only/header-only/foreign-observation skips; C2 close-the-routing-file plus true-check skip; six actual rows' repair sensitivity. Untested boundaries explicitly remain source-level findings above; no fabricated no-op-tool or drift-control result is claimed. L1 requested wrap-up before further adversarial fixtures.

## Review self-evaluation

Accuracy 4: executed outputs are separated from source inferences; full-base per-id executions are not claimed. Completeness 3: no custom printer or real host-drift fixture, and no independently logged six full-base commands. Clarity 4: per-id matrix distinguishes sensitivity from full-base execution. Actionability 4: smallest corrections name exact resolver/universe boundaries. Conciseness 3: evidence blocks are intentionally retained for audit. Overall 3.6/5. Highest-impact improvement would be custom no-op and full-base fixtures, not broader narrative; these were not run following L1's stop instruction.
