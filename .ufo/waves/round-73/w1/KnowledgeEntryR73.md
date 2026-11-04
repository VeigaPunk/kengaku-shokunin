# KnowledgeEntryR73 — sourced knowledge draft

## Behavior and axes

Coverage / calibration. Drafted the requested entry, in the requested body order, at `corpus/evidence/round73/w1/knowledge-draft.md`. Its first lines are source / verified-at / recheck. It cites the scout's actual `#ast.parse`, `#ast.PyCF_ONLY_AST` and `#ast.walk` anchors, separates documentation from local measurements, and distinguishes declaration checks from behavioral verification. Intended destination remains `corpus/knowledge/instrument-registry-derivation.md`; only the L1 may land it.

## Gates and provenance

No gate, selftest, mutant, build, judge, credential scanner or landing verification was executed by this seat. All such results in the draft are explicitly attributed to receipts read, not claimed as this seat's executions. No runtime or tool was installed or updated. No git/jj mutation, commit, push, publication or deployment was performed.

Read the full frozen claims before any shell command. Read the corpus contract at fleet-root `CORPUS.md` after discovering that lane-root `CORPUS.md` does not exist; read required Godspeed and self-evaluation skills. No predicate, target, counting command or kill rule changed.

### Existing receipts read (not rerun)

| Receipt | Recorded command/date | Recorded outcome |
|---|---|---|
| `corpus/evidence/round73/c2-red-before.txt` | `python3 plans/round73_c2_registry_audit.py --lane <base tree>`, 2026-11-04T02:43:19Z | `INSTRUMENTS total=106 derived=registry rows=106`; `MISMATCH 2`; rc 1 |
| `corpus/evidence/round73/c2-control-frozen-tuple.txt` | old/new `--lane <fixture>`, 2026-11-04T02:43:05Z | old `DEFECTS n=0`, rc 0; new `MISMATCH 2`, rc 1 |
| `corpus/evidence/round73/c2-after.txt` | `python3 plans/round73_c2_registry_audit.py --lane .`, 2026-11-04T02:48:04Z | `INSTRUMENTS total=114 derived=registry rows=114`; `MISMATCH 0`; rc 0 |
| same | `python3 plans/round73_c2_registry_audit.py --selftest --work <scratch>`, same recorded timestamp | `SELFTEST arms=4 red=3 ok=True`; rc 0 |
| `corpus/evidence/round73/c1-after.txt` | `python3 plans/round52_c2_registry.py --lane .`, 2026-11-04T02:48:04Z | `ADVERTISED total=113`; `MISSING 0`; rc 0 |
| same | `python3 plans/round52_c2_registry.py --selftest`, same recorded timestamp | `SELFTEST cases=4 failures=0`; rc 0 |
| `corpus/evidence/round73/sources/ast-anchor.md` | scout's live-fetch and reproduction commands, capture 2026-11-04T02:46:48Z | located quotations and explicit non-execution inference gap; source provenance belongs to SourcesAstR73 |

## Findings / conflicts for canonical judgment

1. Exact frozen C2 denominator versus after receipt: frozen `INSTRUMENTS total=106 derived=registry rows=106`; recorded after `INSTRUMENTS total=114 derived=registry rows=114`. Both are quoted in the draft. `PREDICATE R73-C2 pass` is not a substitute for matching the frozen required lines.
2. Coverage target versus receipt: assignment says `ADVERTISED total=112`; after receipt says `ADVERTISED total=113`. Frozen sentence says `ADVERTISED total>=111`. These conflicting exact/threshold formulations are reported without adjudication or edits.
3. Audit claims do not establish semantic truth: `pinned-values` and `write-scope` are only nonempty-cell checks; self-test flags are textual; owner is a prefix; malformed-width rows are dropped; entry commands are not executed. The decision table says what is actually observed rather than upgrading “all fields priced” into a behavioral audit.
4. `ast.walk` is documented by the source but unused by this audit. Registry-derived universe comes from `parse_rows`/`run_checks`, not an AST traversal. The draft makes that distinction explicit.
5. Scout documents that “without executing” is inference, not a direct quotation. The draft preserves that limitation.
6. `corpus/SOURCES.md` search `^\| S249` returned no match at this seat's observation; draft marks S249 as a planned row with an existing capture, not a landed admission. L1 owns the row and admission state.
7. The instruments read the supplied working tree. Neither a docstring saying “committed bytes” nor a receipt describing a worktree establishes a clean landing revision. No landing hash is asserted here.

## Touched surfaces and cleanup

Only durable writes:
- `corpus/evidence/round73/w1/knowledge-draft.md`
- `.ufo/waves/round-73/w1/KnowledgeEntryR73.md`

Scratch command executed:

`mkdir -p /fast/scratch/hyaku/kengaku-r73/KnowledgeEntryR73 && cd /fast/scratch/hyaku/kengaku-r73/KnowledgeEntryR73 && pwd && df -h . | tail -1` — rc 0; printed the owned scratch path and capacity. No clone or fixture was created.

Cleanup command executed:

`rm -rf -- /fast/scratch/hyaku/kengaku-r73/KnowledgeEntryR73` — rc 0, no output. No /tmp file was created by this seat. No throwaway script remains.

## Investigation command outcomes / process defects

Source reads covered the frozen audit, amended advertisement gate, corpus contract, scout capture/anchor, round-72 lesson and the named historical seat reports. Historical report pointers are lane-relative in the draft, not fleet-report citations.

Exploratory commands were read-only shell listings/searches and JSON inspection. Two initial guessed locations failed and were resolved:
- read lane-root `CORPUS.md`: `Path ... not found`; discovered fleet-root contract via glob and read it.
- `wc -l .ufo/waves/round-72/SiblingOverlapR72.md .ufo/waves/round-72/C2RedBeforeR72.md .ufo/waves/round-72/RegistryAuditR72.md`: rc 1, each `No such file or directory`; located actual files under `w1` and read them.
- initial `ls corpus/evidence/round73/w1/` before directory creation ended the combined listing at rc 2; later discovered/read the created directory and scout artifacts.

Process defects of this seat: early exploration used shell ls/find/grep/sed/awk/head/tail despite specialized-tool preferences, and verbose commentary preceded the scribe output. Those did not modify lane bytes but are instruction-following defects, not evidence of product conformance. An early paragraph glossing the historical “six content fields” was removed before delivery because the source does not justify that extra interpretation.

## Out of scope / handoff

No product code, source row, lesson, index, corpus destination or frozen claim was edited. L1 must land the draft only with the intended S249 row and an accurately named landing state. Main-agent checks should compare actual landing output against all frozen required lines, validate the provenance trio and source-row/index linkage, and resolve the recorded count conflicts through canonical judgment. These are recommended checks, not exercised passes.

## Self-evaluation (not a gate)

Accuracy 4/5: precise function-level decision table and receipt attribution; state is a concurrent working-tree observation, not independently pinned. Completeness 4/5: all requested sections supplied, while source-row insertion remains explicitly outside this seat's write scope. Clarity 4/5: implementation limits are explicit, but the detailed table is necessarily dense. Actionability 4/5: draft is at the exact assigned landing-input path; canonical count conflict requires L1/judge handling. Conciseness 3/5: evidence detail makes this report and draft longer than ideal, retained to avoid laundering counts or scope. Overall 3.8/5. Highest-impact improvements: keep the landing denominator conflict visible; make the source-row linkage explicit when landing; retain the declaration-versus-behavior boundary. Expected user agreement: qualified, because no landing verification is represented as executed.

## Post-delivery admission instruction

KengakuR73 subsequently instructed an explicit hold pending a qualifying second-seat reread under Q10/Q13/Q14. Added `admission: hold` after the provenance trio in the draft. The coordinator also reports the original claims NOT ADMITTED and an appended E-R73-1; those are coordinator-reported status, not an independently executed judgment by this seat. Structural checks remain explicitly distinct from semantic truth and compile/run behavior.
