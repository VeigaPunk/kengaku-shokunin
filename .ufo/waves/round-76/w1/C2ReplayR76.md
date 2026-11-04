# C2ReplayR76 — independent C2 before-state replay

Axes: coverage (all seven legs and scoped ids), calibration (independent derivations, actual process exits, no status-only proof).

## Commands and retained evidence

Read the frozen claims in full before commands; read the discharge gate, including its fixtures and entry point. No production edits, git mutations, clones, installs, external-state changes, or background jobs. LSP is not exposed by this seat's tool inventory; inspected Python source directly.

Created the seat scratch and evidence directories with:

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r76/C2ReplayR76 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-76/w1/C2ReplayR76
```

rc 0. Executed from the lane directory:

```sh
S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r76/C2ReplayR76"; trap 'rm -rf -- "$S"' EXIT; python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-76/w1/C2ReplayR76/replay.py
```

Driver rc 0; the trap removed the seat scratch. Retained driver `C2ReplayR76/replay.py` independently parses README and ledger; it does not import the discharge gate. Child commands and full stdout/stderr/rc are retained in adjacent `.txt` files:

```sh
/usr/bin/python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-76/w1/C2ReplayR76/before_sandbox.py /fast/scratch/hyaku/kengaku-r76/C2ReplayR76/before plans/round76_c2_defect_discharge.py
/usr/bin/python3 plans/round75_c1_index_parity.py --selftest --work /fast/scratch/hyaku/kengaku-r76/C2ReplayR76/c1
/usr/bin/python3 plans/round75_c2_registry_audit.py --selftest --work /fast/scratch/hyaku/kengaku-r76/C2ReplayR76/c2
```

Exits respectively 1, 0, 0. The first runs the gate with `sys.argv = [script, '--lane', '.', '--rev', 'fda63968']`. **The exact bare before command was not executed:** `emit()` unconditionally calls `mkdir` on `/fast/scratch/hyaku/kengaku-r76/c2`, outside this seat's allowed scratch, and ignores `--work` there. Retained `before_sandbox.py` redirects only that exact `Path.mkdir` destination to seat scratch; all input reads, gate calculations, and revision arguments remain unchanged. Rev mode never subsequently uses the work directory.

Independent Git calls (all read-only; each invoked with `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin`):

```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show fda63968:corpus/evidence/round75/c1-after.txt
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse --verify 9f8f0f2180821d165f60e400277f192d92afbbce^{commit}
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 43255758:corpus/README.md
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-tree -r --name-only 43255758 corpus
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show fda63968:corpus/lessons/round-75-verifier-spotcheck.md
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show fda63968:corpus/routed-findings.jsonl
```

All rc 0 (driver raises on a nonzero Git exit). Worktree comparisons read only the corresponding three receipt/lesson/ledger files. The requested shell grep/sort scope extraction was implemented independently with sorted regex matches, not run as a shell pipeline. Specialized grep also located every id in the closure.

## Verbatim before output

Full evidence: `.ufo/waves/round-76/w1/C2ReplayR76/before.txt`.

```text
SCOPE-SOURCE corpus/lessons/round-75-verifier-spotcheck.md
LEG D1 FAIL QUALITY criterion cites R75-D1 + lesson
LEG D2 FAIL SCORECARD line with R75-D2, stamp 9f8f0f218082, 5d9a0ccc
LEG D3 FAIL SCORECARD line with R75-D3, total 60, split 4/36/20 at 43255758
LEG D4 PENDING needs the two round-75 selftests (rev mode)
LEG D5 PENDING needs the selftest counts (rev mode)
LEG D6 FAIL r74-c1-tip.txt=missing/no-stamp r74-c2-tip.txt=missing/no-stamp
LEG D7 FAIL round-74 lesson appended correction naming R75-D7
LEDGER R75-D1 MISSING-ROW
LEDGER R75-D2 MISSING-ROW
LEDGER R75-D3 MISSING-ROW
LEDGER R75-D4 MISSING-ROW
LEDGER R75-D5 MISSING-ROW
LEDGER R75-D6 MISSING-ROW
LEDGER R75-D7 MISSING-ROW
SCOPE ids=7 registered=0 closed=0 open=7 discharged=0 legs_passed=0 legs_pending=2 wrong=12
PREDICATE R76-C2 fail
RC 1
```

## Independent derivations

Evidence: `C2ReplayR76/independent.txt`, `missing-paths.json`, `r75-c1-selftest.txt`, `r75-c2-selftest.txt`.

```text
STAMP fda63968 LANE_TIP 9f8f0f2180821d165f60e400277f192d92afbbce
STAMP-RESOLVES 9f8f0f2180821d165f60e400277f192d92afbbce
STAMP worktree LANE_TIP 9f8f0f2180821d165f60e400277f192d92afbbce
INDEX knowledge disk=74 indexed=70 missing=4
INDEX lessons disk=123 indexed=87 missing=36
INDEX evidence disk=66 indexed=46 missing=20
FINAL-RULE total=60 split=4/36/20 revision=43255758
IDS fda63968 R75-D1,R75-D2,R75-D3,R75-D4,R75-D5,R75-D6,R75-D7
LEDGER-INDEPENDENT fda63968 matching=0 ids=[]
SELFTEST cases=8 red=7 failures=0 ok=True
SELFTEST arms=5 failures=0 ok=True
```

README derivation strips HTML comment spans and fenced blocks, scans unescaped pipe delimiters into cells, requires at least two cells and every cell nonempty, and accepts only backtick-wrapped `knowledge/…` or `lessons/…` first cells. Disk inventory is Git's tree, not current filesystem state. Missing names are retained, not just totals. Evidence directories are compared with mentions in the rendered text as the frozen gate specifies.

The selftests stamped `6977019bdf56a88921e14f728167da8f5726c1fc` and `WORKTREE dirty`; these are actual live-wave runs, not clean-commit receipts. The base ledger held zero scoped ids. The concurrently changing worktree ledger already held seven by the independent read; that observation is not a claim of committed closure or successful discharge.

## Numbered findings

1. **MEDIUM — frozen before tally is not reproduced.** `plans/round-76-claims.md` R76-C2 Before says `legs_pending=0 wrong=14`; observed gate emits `legs_pending=2 wrong=12`. Concrete reproducer is base revision `fda63968` plus unchanged gate branches `if rev_mode or not deriv['c1c']` for D4/D5. They deliberately emit PENDING; the five other failing legs plus seven missing rows total 12. The predicate still fails rc 1. Do not silently rewrite frozen text. Routed to KengakuR76 with the actual output.
2. **LOW — before command violates seat scratch bounds unless contained.** `plans/round76_c2_defect_discharge.py`, `emit()`, hard-codes `/fast/scratch/hyaku/kengaku-r76/c2`; CLI `--work` does not reach that mkdir. Only that mkdir was redirected for this replay. Exact standalone command remains unexecuted under the unmodified environment.
3. **INFO — independent evidence agrees with all requested value derivations.** Stamp is full SHA `9f8f0f2180821d165f60e400277f192d92afbbce`, final-rule before is 60 = 4/36/20, and both actual round75 selftest summary lines match the expected 8/7 and 5. See retained receipts above.
4. **INFO — base scope and omission independently confirmed.** Exactly R75-D1 through D7 occur in the base closure and none has a base ledger row. This establishes absence, not subsequent closure.

## Exact integration bytes by leg

These are concrete correction text suggestions matching the inspected leg conditions; only L1 may integrate. Commit actual evidence, not merely the minimal grep tokens.

| Leg | Committed file | Literal bytes / required placement |
|---|---|---|
| D1 | `corpus/QUALITY.md` | `R75-D1: Land reports after the final lane commit; append errata rather than rewrite filed bytes. See corpus/lessons/round-75-verifier-spotcheck.md.` Put both tokens together, within the four-line block beginning at the first R75-D1. |
| D2 | `SCORECARD.md` | `R75-D2 correction: committed after receipts stamp 9f8f0f2180821d165f60e400277f192d92afbbce; report tip 5d9a0ccc had no committed re-derivation receipt.` All three matching tokens on an R75-D2 line. |
| D3 | `SCORECARD.md` | `R75-D3 correction: final-rule before at 43255758 is 60 (4/36/20).` Keep id, 60, and 4/36/20 on the same line. |
| D4 | `SKILL.md` | In the existing `round75-c1-index-parity` row, literal `cases=8 red=7`; in the existing `round75-c2-registry-audit` row, literal `arms=5`. Preserve full existing row schema. |
| D5 | `LOG.md` | `R75-D5 correction: C1 selftest cases=8 red=7; after receipts stamp 9f8f0f2180821d165f60e400277f192d92afbbce, not the earlier claimed revisions.` Keep the counts and full stamp in the six-line block beginning with the first R75-D5. The gate does not require the C2 arms token here. |
| D6 | `corpus/evidence/round76/r74-c1-tip.txt` and `corpus/evidence/round76/r74-c2-tip.txt` | Actual executed receipts must contain respectively `PREDICATE R74-C1 pass` and `PREDICATE R74-C2 pass`, plus a line beginning `LANE_TIP ` followed by the actual measured ancestor commit. No fabricated stamp or synthetic pass receipt suffices as evidence. |
| D7 | `corpus/lessons/round-74.md` | Append a separate `## Correction (round 76)` heading and `R75-D7: The earlier round-74 lesson correction was reflowed in place; future corrections are separate appended entries.` Preserve existing filed text. |

Shared ledger requirements for each of the seven ids: append a JSON object to `corpus/routed-findings.jsonl` with exact id, `"status":"closed"`, dated `verified_at` (for example `"2026-11-04"`), and a full 40-hex `close_commit` naming the real committed discharge ancestor. `check` must contain both a recognized committed path token and a quoted literal of at least three characters, e.g. D1 `grep -q 'R75-D1' corpus/QUALITY.md`, D2/D3 `grep -q 'R75-D2' SCORECARD.md` / `grep -q 'R75-D3' SCORECARD.md`, D4 `grep -q 'cases=8 red=7' SKILL.md`, D5 `grep -q 'R75-D5' LOG.md`, D6 `grep -q 'PREDICATE R74-C1 pass' corpus/evidence/round76/r74-c1-tip.txt`, D7 `grep -q 'R75-D7' corpus/lessons/round-74.md`. These checks are text-shape examples; gate legs separately inspect the values and receipts. The inspected checker does not execute ledger `check` strings.

S252 handling in inspected source: resolved commit followed by `merge-base --is-ancestor`; rc 0 means ancestor, rc 1 means not-ancestor, other rc means error. An unresolved revision is a separate pre-probe state. Each receipt stamp and ledger close commit must resolve and be an ancestor of the measured tip. I did not run mutation/git fixture batteries or create commits.

## Limits and self-assessment

No landing-tip C2 predicate run, no new R74 gate runs, and no claim that seven closed worktree rows satisfy their ancestry or discharge legs. Parent owns integrated checks. The frozen discrepancy was reported, not repaired. No tool installation/update occurred.

Self-evaluation: accuracy 4/5 (sandboxed before command, not the bare invocation); completeness 4/5 (all assigned independent derivations and D1–D7 integration literals retained; no post-integration verdict); clarity 4/5 (full outputs separated from interpretation, but long command paths); actionability 5/5 (file/literal/placement mapping plus actual receipt caveat); conciseness 4/5 (audit trace costs length). Overall 4.2/5. Improvements: parent should retain a formally approved frozen-before discrepancy disposition and run the final unmodified gate in its authorized scratch environment. Would the user agree? The explicit caveats prevent treating this replay as a clean after receipt.

## Parent disposition received after replay

KengakuR76 confirmed both findings: Amendment A1 records the actual Before tally (`legs_pending=2 wrong=12`) without changing predicate/target/control/kill rules, and the parent reports an `emit()`/`--work` fix pending its next commit. Those are parent-reported dispositions, not independently verified here; original replay receipts remain unchanged.

**Leg-only vs CLI:** this was **CLI replay with one filesystem-path redirection**, not a leg-only replay. No gate functions were called directly by the independent derivation driver. `before_sandbox.py` calls `runpy.run_path(..., run_name="__main__")`; the gate itself executes its normal `main() → emit() → derivations()/legs()/ledger_report()` flow with the stated argv. Both round75 selftests were direct subprocess CLI executions. The README/stamp/ledger derivations are separate independent code.
