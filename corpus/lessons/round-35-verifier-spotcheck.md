author: hyaku closure (non-author integrator, @m_sonnet)

# Round 35 — non-author closure spot-check (kengaku, 2026-10-25)

Measured against lane tip `e7f0decda220ccc55bac4a4ba8f3e130af73bdca` (before: `5d0c73db432f75eea7d5f90b521811c6686fcb68`).
Dispatch digest (`.ufo/watchdog.log`, mutable, copied here):
`2026-10-25T16:20:00-03:00 launch kengaku round=35 pgid=1104327 driver=hyaku-inline attempt=1` ·
`2026-10-25T17:37:18-03:00 complete kengaku round=35; hyaku-inline attempt=1`.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-35/kengaku.md` | `kengaku-shokunin 38eee079…` (17:31:07, before the 17:37:18 complete line) — ok |
| `SHONEN` heading, one line per box | read report | `## SHONEN`, 4 lines, all `[~]` with pointers — ok |
| cited lane commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for all 8 cited hashes (freeze `11d64530`, `dfcd294c`, `4fe72a9a`, `6ac9611a`, `056e192a`, `dfee6fff`, `1d4084fa`, `e7f0decd`) | 8/8 `anc ok` |
| pushed, nothing uncommitted | `jj-lane.sh state …` ; `git -C lane status --porcelain --untracked-files=all` ; `git ls-remote origin refs/heads/master` | `local=remote=e7f0decd… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote `e7f0decd…` |
| prompt carries the template contract | grep of `.ufo/prompts/kengaku-round-35.md` (committed `9b786593`, lane identity) | SHONEN, L2 floor (≥8, one batched call), commit-then-push, push scope, L0 channel, report path, hash citation, Sources & frontier, trend verdicts, frontier step all present — ok |
| minimum report content | read report | work, evidence pointers, landed-changes table, Sources & frontier (counts + counting command), trend verdicts, stale-lane line all present — ok |

Fleet root `git status --porcelain --untracked-files=all` (excluding operator-side `.ufo/state`): `M .ufo/watchdog.log` and
`?? .ufo/waves/round-30/wave1/ScribeLesson.md` — the latter is another lane's round-30 file, not round-35 work (agrees with the report's misroot sweep).
No conformance defect that changes status. Status: `ok`.

## 2. Claims — re-measured vs evidence-verified

Re-measured by me over committed bytes (`git show <rev>:…`, `git archive e7f0decd` into a `mktemp` dir outside the lane):

| quantity | command | before (`5d0c73db`) | after (`e7f0decd`) | reported |
|---|---|---|---|---|
| SOURCES registry rows | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | 97 | 100 | 97→100 ✓ |
| malformed rows (NF≠13) | CORPUS census awk | 0 | 0 | — |
| knowledge files | `git ls-tree --name-only <rev> corpus/knowledge/ \| wc -l` | 41 | 42 | 41→42 ✓ |
| committed round-34 mirror paths (D2 roots) | `git ls-tree -r --name-only <rev> \| grep -c 'mut-entries-scratch\|R34MutRegistry/(mirror\|mut)/'` | 109413 | 0 | 109,413→0 ✓ |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | — | exit 0, 15 W04, `kengaku ok` | exit 0, 15 W04 ✓ |

- **C1 (coverage), re-measured.** In a clean archive of `e7f0decd` (`git init`, branch renamed `master`): `python3 plans/round35_c1_verify.py --lane .` → `V1 ok … V6 ok`, `checks=6 defects=0`, `PREDICATE C1 pass`, exit 0 (before, frozen: `checks=6 defects=5` per `claims/control-c1-nothing.txt`). V5 re-runs the probe, so the receipt `corpus/evidence/round35/tb2-grader-probe.txt` (`cases=18 observed_pass=5 observed_fail=13 mismatches=0`) is byte-equal to a fresh run. Beyond the counter I verified the content the counter is known not to prove (the lane's own limit): the three pinned files re-fetched live (`curl` from `raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/protein-assembly/`) hash to the S105/S106/S107 digests (`44a05a24…96582`, `9ede4664…267b5`, `1bb2af1d…003f7c5`); all 22 quotes of the entry's `## Located quotes` table appear at their stated `file:line` in the live files (22 ok, 0 miss; my own script); every quote is ≤25 words (max 19); the three S105–S107 anchor quotes are present at the stated lines (`test_outputs.py:42`, `test.sh:27` and `:21`, `instruction.md:29`) with 11/4/15 words (matches the post-errata counts). **Verified.**
- **C2 (calibration), re-measured.** Same archive: `python3 plans/defect_ledger.py --lane .` → D1–D5 `closed observed=pass agree=yes`, `rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE C2 pass`, exit 0 (before, frozen: `closed=0 … PREDICATE C2 fail`). Independent plain checks: D2 `committed_mirror_paths=0` (table above); D5 erratum present in `corpus/lessons/round-34.md:45` and the staged S091 quote (70 chars) found in the committed `nec-s091-reopen.html` after tag-strip + whitespace removal (my python), capture digest `sha256sum -c quarantine-SHA256SUMS` OK. **Verified**, with the limits below.
- **Caveat on running the lane's counters.** They are claim counters in the lane's `plans/`, executed in a temp copy, not a gate-registry run; `plans/round35_hardening.py` H1 is red only inside my history-less archive (no freeze commit to compare). In the real lane `git diff --stat 11d64530 e7f0decd -- plans/tb2_grader_probe.py plans/round35_c1_verify.py plans/defect_ledger.py` is empty and `git log 11d64530..e7f0decd -- <those>` is empty — no frozen instrument changed after the freeze (agrees with the report). I did not execute any other lane's gate.
- **Gate evidence verified, not executed:** probe self-evidence (three harness mutants detected, `R35ProbeHarnessMut.md`; independent grader 18/18, `R35IndepGrader.md`) is lane evidence I read but did not re-run beyond V5.

### No-harm audit

`git diff 5d0c73db e7f0decd -- SCORECARD.md`: +36 lines, 0 deletions; the only table edits are two appended capability rows (`pinned-grader-probe`, `routed-defect-ledger`, first-working round 35) plus an appended D4 correction, the round-35 section and an appended erratum. Every axis score is stated unchanged (coverage 7→7 held by the L0 cap, calibration 8→8 held, novelty 7, depth 9, operability 8, freshness 8, adjacency 8). The `corpus/README.md` diff adds an index row, a coverage bullet, a Frontier sub-bullet and two appended corrections; nothing removed. Both capability rows' commands re-ran (probe via V5; ledger directly).

### Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage (C1) | **improved** | predicate 5 defects→0 re-measured; knowledge 41→42, rows 97→100, Frontier clause discharged for one task (the lane honestly scopes it to `protein-assembly` only); score 7→7 held by the open L0 cap, so the verdict rests on the measured before→after, not a score move |
| calibration (C2) | **improved** | all five routed defects closed and re-measured (`mismatches=0`); the lane appended errata for its own over-claims (C2 "green at `dfcd294c`", README "executes `test.sh`", 2766→2768 nt, S105/S107 word counts) and states the counters' weakness in the report; score held 8→8 |
| novelty | unchanged | no claim, no change in SCORECARD |
| depth | unchanged | |
| operability | unchanged (capability rows entered with demonstrations) | |
| freshness | unchanged | |
| adjacency | unchanged | PROVINCE round-35 paragraph (read) scopes the addition to one function's offline behaviour and leaves runtime task validity, hosted judges and the other TB2 tasks open |

No axis harmed. Both claims verify. Neither claim was exploratory.

## 3. Discernment spot-check (`round-35.md` `## Gate`)

| item · decision | re-opened source | agree/disagree | reason |
|---|---|---|---|
| `knowledge/tb2-protein-assembly-grader.md` · **Admitted** | the entry; live `raw.githubusercontent.com/…/2fd12b88…/protein-assembly/{tests/test_outputs.py,tests/test.sh,instruction.md}` | **agree** | provenance trio first; all three sources hash-match; 22/22 located quotes resolve at stated lines; scope honestly bounded (code behaviour tier A, comments' PDB claims labelled self-report); appended `## Errata` marks the 2766→2768 nt, finding 1/3 narrowing, `non-acgt-base` confound and over-broad table header, so no admitted claim stands false and unmarked. |
| S105 `tests/test_outputs.py` @ `2fd12b88` · **Admitted (mined)** | same URL, sha256 + `sed -n 42p` | **agree** | digest `44a05a24…96582` matches; quote line 42 present, 11 words (≤25); tier A correct for "what the code asserts". |
| S106 `tests/test.sh` · **Admitted (mined)** | same, `sed -n '21p;27p'` | **agree** | digest `9ede4664…267b5` matches; `echo 1 > /logs/verifier/reward.txt` at :27 and `-w biopython==1.85 \` at :21 present. |
| S107 `instruction.md` · **Admitted (mined)** | same, `sed -n 29p` | **agree** | digest `1bb2af1d…003f7c5` matches; line 29 quote present, 15 words. |
| Quarantine S091 (NEC 技報) · **Re-grounded, not appended** | committed `.ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html` (sha OK) ; live `https://jpn.nec.com/techrep/journal/g23/n02/230212.html` | **agree** (reject-side: not appended) | quote is present in the committed reopen capture (tag-stripped, my python → True), so round 34's "quote absent" was false and the erratum is right; not appending is correct under CORPUS rule 4 (no admitted entry cites it). Live re-fetch from this host returned the 418-byte Access Denied page twice (default and browser UA), so the live leg is `unprovable` here; the verdict rests on the committed capture. |
| Package `toolathlon-grader-behaviour-probe-2026-10-23.md` (S130) · **Refused** | `/home/vgpnk/Projects/shokuknow/merge/kengaku/{SOURCES.append.md,knowledge/corpus/knowledge/toolathlon-grader-behaviour-probe-2026-10-23.md}` | **agree** | S130 is `own-work` whose locator `lanes/kengaku/round6/…` is not resolvable from this lane (lesson's reason, confirmed in `SOURCES.append.md:60`). Independent additional reason found by wave-1 scout and re-checked by me: the package's summary denominators say 38 but 13 + 23 + 1 = 37 rows — the lesson's Gate row omits this second reason. |
| Package `terminal-bench-release-identity.md` · **Refused** | `R35ScoutMergePkg.md`, live registry (`S100`, `S092` present, used by `benchmark-verifier-execution-model.md`) | **agree** | no uncovered ground; cites rows the registry already holds. |
| Package `grader-predicate-input-types.md` / fixture-probe amendment · **Held** | `R35ScoutMergePkg.md` | **agree** | held rather than admitted because the frozen claims precede the screen; a legitimate flip condition is stated. |

Newly written SOURCES rows re-opened: S105, S106, S107 (above) — URLs, digests, anchors, and ≤25-word quotes all check. S105 word count (11) and S107 (15) match the corrected anchors (the original 9/16 were the lane's own errors, already errata'd).
Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0, `kengaku ok`, 15 W04 (duplicate-URL-across-scopes, same set as before; S100 is the newest of them from round 33/34).

**Discernment conclusion:** agree on 4/4 admits sampled (entry, S105–S107) and 4/4 rejects/holds sampled (S091, Toolathlon, release-identity, held packages); the round-34 disagreement (D5, S091) was turned into a ledger row plus QUALITY Q23 with the lesson cited (`QUALITY.md` Q23 → `round-35.md` §Mistakes). The lane's own freeze-time miss (frozen counters weaker than their skip-control; junk package passes C1) is disclosed and its hardening is explicitly not yet a rule.

## 4. Trend verdicts

- **expansion — improved.** One admitted entry on ground the coverage map did not hold, each of S105–S107 `mined` with `used-by` resolving (census `kengaku ok`); one Frontier clause discharged for one task; two capability rows entered with demonstrations (counters re-run by me).
- **quality — improved.** 22/22 located quotes re-verified against live pinned bytes; three round-34 self-assessment errors (D3 manifest, D4 attribution, D5 refusal reason) corrected by appended entries with the live re-check; wave-2 errata mark the new entry's own over-statements. The lane's remaining weakness (counters accept junk) is disclosed, not hidden.
- **discernment — improved.** Outside spot-check agrees with the gate on all sampled admits and rejects; round-34's disagreement became a grounded criterion (Q23). The lane graded itself `unchanged`; I rule `improved` on the table's criteria (spot-check agrees on admits and rejects; a prior disagreement became a lesson with a grounded criterion). Caveat: the post-hoc hardening (H1–H6) is not yet a rule, so the freeze-time weakness is not yet learned in the strict sense — see routed item 1.

## 5. Routed defects (lane fixes next round; status-neutral)

1. **Frozen counters accept junk.** `plans/round35_c1_verify.py` passes a stub probe plus one-word quotes; `plans/defect_ledger.py` D4/D5 accept labelled-but-false lines. `plans/round35_hardening.py` is post-hoc and not a rule: promote H1–H6 into the next round's counters and have a critic seat build the junk-package control before freeze data.
2. **D1 is a working-tree check, D4/D5 token co-occurrence.** The ledger should read committed bytes (`git show <rev>:<path>`), as the lane's own erratum says.
3. **D2's roots are narrow.** At `e7f0decd` I count 21 committed paths matching `^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-` (all under `.ufo/waves/round-34/build/R34ReviewCounterC1Attacks/a3..a6/`; the report cites 28 by a different method). Extend the D2 check to nested `.ufo/waves/` recursion.
4. **Gate row omission.** The Toolathlon-package refusal row cites only the own-work locator reason; add the 38 vs 37 denominator reason (13+23+1) to the next `## Gate` if the package is revisited.
5. **S091 live leg.** NEC returns a 418-byte denial from this host; any future claim that depends on the page must cite the committed capture + digest, not live reachability.
6. **SHONEN (for the operator).** All four boxes remain `[~]` (author-asserted). The end-to-end-task box has non-author-checkable evidence in this round (`tb2-grader-probe.txt` re-run byte-equal by V5; the C1 counter passes on my archive). I did not tick it; promotion is operator-owned. I did not re-assess the SKILL.md, instructions-without-oral-context or no-bleed boxes this round.
