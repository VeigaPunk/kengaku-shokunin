# Round 46 non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)

## Conformance

- Report `.ufo/reports/round-46/kengaku.md` exists in the fleet repo and was committed by lane identity: `git log --format='%an <%ae> %H' -- .ufo/reports/round-46/kengaku.md` → `kengaku-shokunin <kengaku@shokunin.local> 33540c6e4587735e67a393736bd97f1126515d5c`. Report commit time 03:18:03 -0300 follows lane tip `a68afb2fffd66c8bb2c4687fd40b7779f2761743` (03:17:09 -0300) and dispatch 01:28:11 -0300. Report cites the pushed lane tip.
- `## SHONEN` is present with four `[~]` lines, one per report box. Prompt `.ufo/prompts/kengaku-round-46.md` carries the rendered template contract: mission/axes and frontier requirements, ≥8 L2 in one batched AgentSwarm call, report path/required sections, SHONEN, commit/push ordering, push scope, L0 side channel, and the hyaku addendum. Its L2 contract matches fleet `MISSION.md` §L2 concurrency. No L2 model aliases are hardcoded.
- All lane hashes cited as round-work hashes in the report/claims (`fd4129eb`, `cf7de6af`, `4fdeebaa`, `7768716c`, `420eec9f`, `c1ec334c`, `8d7f74ce`, `e9d20145`, `f1871acc`, `42d5043a`, `85a40be5`, `264b7757`, `a68afb2f`) resolve and `git merge-base --is-ancestor <hash> master` succeeds. Base `64ba8385ea10af1b78d367dcb242b92d97062af7` is also an ancestor. The separately cited `2fd12b88…` is the external Terminal-Bench source revision, not represented as a lane commit.
- Lane state: `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state …` → `branch=master local=a68afb2… remote=a68afb2… ahead=0 behind=0 head=detached tracked=0 untracked=0`; lane `git status --porcelain` has 0 lines; `git ls-remote origin refs/heads/master` → `a68afb2fffd66c8bb2c4687fd40b7779f2761743`.
- Real work, report, and evidence are present; this is not a marker. Status `ok`. Conformance defects are status-neutral: report says 4 wave-2 seats lack ordinary report files and their row/mutation work is unattacked; it also records the misrooted seat artifact and the disclosed C3 pre-receipt execution. No `[x]` was written to SHONEN.

## Claim re-checks and axis verdicts

Measurements below are from committed bytes/receipts. I did not run the sibling-owned gates; their committed self-test/frozen evidence and measured revisions are checked as evidence.

| claim | independent re-check and observed output | axis verdict |
|---|---|---|
| C1 calibration | `git show 64ba8385:…/control-c1-base-fence.txt`/stage-2 receipt and `.ufo/waves/round-46/integrate/c1-landing.txt`: base fence `REFUSALS total=20 clean=10 leaked=10`, `SEALED total=12 clean=0 leaked=12`, `CALIBRATION advertised=32 contradicted=22`; at `420eec9f` pinned `PINS total=65 mismatched=0`, refusals 20/20 clean, sealed 12/12 clean, honest 104/104, contradicted=0, predicate pass. The committed `final-tip.txt` at measured revision `264b7757` also records predicate pass. But the frozen kill rule is met: wave-2 reports count 3 admitted held-outs (2 argv, 1 paths), and the literal rule says ≥2 rejects C1. The lane lesson additionally reports 9/9 novel honest fixtures refused and fence mutants 2/13 caught. Counter evidence confirms primary-set improvement but not a valid overall calibration claim; over-refusal and the held-out kill rule remain material. | **harmed** — the shipped fence fails its frozen generalization kill rule and rejects every novel honest control; no claim admission. |
| C2 depth | Committed before-control `control-c2-nothing.txt`: `A … live=8`, `B … disagree=6`, `C … source_ranges_bad=4 errata_marks=0/5`, `checks=4 defects=3`, fail. `integrate/c2-landing.txt` at `e9d20145` and `final-tip.txt` at `264b7757`: `A anchorline live=0 repaired=8 base_missing=0 base_changed=0`, `B … disagree=0`, `C … source_ranges_bad=0 errata_marks=5/5`, `D selftest exit=0`, `checks=4 defects=0`, pass. The `R46W2C2Entry` evidence cited by the lesson says 0 defects and 0/200 predictor disagreements. Limitation verified in committed `R46W2C2Bypass` result: five bare errata tokens still pass leg C; that leg proves token presence, not accurate errata text. A/B still require the actual repairs. Existing round-45 counter no-harm receipt records 11 checks, 0 defects at base/landing. | **improved** — the anchor and predictor repairs are independently evidenced; record the errata-leg limit. |
| C3 coverage | Plain committed-byte counts: `git show 64ba8385:corpus/SOURCES.md | grep -cE '^ {0,3}\\| *S[0-9]{3}'` → 149; same at `a68afb2f` → 165. `git ls-tree -r --name-only <rev> corpus/knowledge/ | grep -c '\\.md$'` → 52 then 53. `corpus/README.md` frontier text moves 11/89 to 12/89. The executed-probe receipt reports 18 cases, 7 pass/11 fail, 0 mismatches; however committed `integrate/final-tip.txt` at `264b7757` records `checks=13 defects=2`, C3 fail: V7 lacks violating cases for `both-print` and `toolchain`; V8 finds the pre-receipt P10 execution (`control-c3-echo`). The package therefore fails its own frozen admission counter; observed counts establish added material, not an admitted coverage claim. | **unprovable** — measured content growth, but frozen admission predicate fails. |

**Axis table for closure:** calibration `harmed`; depth `improved`; coverage `unprovable`; operability `unchanged`; freshness `unchanged`; adjacency `unchanged`. The three undeclared axes had no round-46 claim or observed harm (no-harm receipt). Overall admission is **false**: C1's frozen kill rule fires and C3's frozen counter fails. Verdict: `rejected-harmed`.

## Discernment spot-check

Sources reopened on 2026-10-27. The admit is S166; both rejects are sampled as the required ≥1 reject.

| item | decision | reopened source | agree/disagree | reason |
|---|---|---|---|---|
| S166, `tests/test_outputs.py` | admit | pinned raw source `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py` | agree | Reopened source contains the quoted `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]` and the listing, gcc, Python/C output assertions at cited lines. It is the primary scoring predicate for the stated scope. |
| Docker Hub `alexgshaw/polyglot-c-py` | reject | `https://hub.docker.com/r/alexgshaw/polyglot-c-py` | agree | Reopened Docker Hub API page lists tags/sizes/architectures and no gcc/Python versions; mutable tag page cannot ground the claimed versions. |
| unpinned `main` instruction ref | reject | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/main/polyglot-c-py/instruction.md` | agree | Reopened text currently matches the pinned request, including version wording, but `main` is a moving ref and supplies no immutable anchor. The lesson's rejection is about provenance stability, not present byte mismatch. |

Reopened S166 source quote is exact and within the ≤25-word limit. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok`, exit 0 (with existing W04 duplicate-URL warnings). Both sampled decisions agree; `discernment: improved`.

## Trends

- **expansion: unprovable-but-better** — committed counts show 52→53 knowledge files, 149→165 source rows, frontier 11→12/89, and an executed 18-case probe. The new entry is not admitted because C3's frozen counter fails, so the LEARNING.md threshold of an admitted entry on uncovered ground is not established.
- **quality: improved** — C2 replaces 8 live defective anchors with repairs, resolves six predictor disagreements to zero, and marks the five named errata; round-45 no-harm receipt passes 11/11 checks at the landing. Wave 2 also appended specific corrections to the C3 entry's class-contrast and unexercised `f(1)` overclaims. No recheck failure is left unmarked.
- **discernment: improved** — outside re-open agrees with the S166 admit and both sampled rejects; the round lesson adds Q40 grounded in the C3 V7/V8 failures. Evidence and decisions are above.

## Routed defects for next round

1. **C1:** repair over-refusal (9/9 novel honest controls refused) and broaden positive controls; satisfy/revise only through a newly frozen counter and explicit held-out kill rule. Revisit uncovered bind-mount behavior and advertisement limits; mutation evidence is only 2/13 fence mutants and 1/6 counter mutants caught. Existing route: round-47 plan in `SCORECARD.md`.
2. **C2:** strengthen leg C so content-correct errata, not five tokens, are required; wave-2 C2 mutation and live-row re-open seats left no reports, so these attacks remain open. Existing routed ledger/round-47 plan records the C2 bypass.
3. **C3:** freeze violating receipt cases for every requirement tag, make pre-receipt controls unable to run P10, and improve mutation sensitivity (0/13 mutants killed). Keep the new knowledge unadmitted until the counter passes; recheck its corrections. Existing route: round-47 coverage plan in `SCORECARD.md`.
4. **Process:** report's disclosed missing wave-2 seat reports and the misrooted fleet-root output are conformance defects to prevent/reconcile next round; retain the report's recovery evidence and path-scope discipline.
