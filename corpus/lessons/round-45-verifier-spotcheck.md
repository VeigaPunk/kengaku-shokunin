# Round 45 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_opus)

Closure of lane-round `kengaku` 45. Base `9d5f9715ebb0343984171be312d44e681f96b9a8` → tip
`3d9ea54a558b40993dba251474535edbf33afa21`. Report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-45/kengaku.md`
(fleet commit `792165cedc0987399cd2bdc0d27143df535884d3`). Dispatched prompt: `.ufo/prompts/kengaku-round-45.md` (fleet).
Re-checks run 2026-10-27 by the closure session plus two read-only reviewer seats it dispatched
(`R45CloseC1Evidence`, `R45CloseC2Entry`); no lane gate or counter was executed.

**Verdict: status `ok`, admitted `false` (`rejected-harmed`).** C1 does not verify (its frozen counter is passed by a
keyed do-nothing control); C2's counted coverage move is real but its frozen admission rider — non-author review of the
predictor block — fails, and the round landed unmarked false detail (depth harmed). The lane reported both honestly.

## Driver digest (copied from `.ufo/watchdog.log`, mutable)

```
2026-10-26T21:50:23-03:00 launch kengaku round=45 pgid=204352 driver=hyaku-inline attempt=1
2026-10-26T22:48:23-03:00 lane-dead-no-report kengaku round=45; retry same round (hyaku-inline attempt=1: attempt 1 policy refusal; no report, wave, or commit)
2026-10-26T22:48:25-03:00 launch kengaku round=45 pgid=2860835 driver=hyaku-inline attempt=2
2026-10-27T00:16:15-03:00 lane-dead-no-report kengaku round=45; retry same round (hyaku-inline attempt=2: attempt 2 L1 KengakuR45-2 died in the orchestrator session exit 2026-10-26 23:57:36 -03 (SIGHUP during an operator omp update); no report (fleet report draft left uncommitted); w2 39 seats killed (5 reports, 3 outputs recovered); work salvaged to the lane branch fbad1c56)
2026-10-27T00:16:26-03:00 launch kengaku round=45 pgid=889659 driver=hyaku-inline attempt=3
2026-10-27T01:12:36-03:00 complete kengaku round=45; hyaku-inline attempt=3
```

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report landed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-45/kengaku.md` (fleet) | `kengaku-shokunin 792165cedc0987399cd2bdc0d27143df535884d3` (01:11:40 -03, after lane tip 01:11:27) | pass |
| `SHONEN` heading, one line per box | report `## SHONEN` vs `SHONEN.md` | 4 `[~]` lines for the 4 boxes; pointers resolve (`LOG.md:7`, `PROVINCE.md:129`, `corpus/lessons/round-8-aggregator-box3-coldrun.md:48`, `a3w1/R45RevProvince.md` `province-defects-0`) | pass |
| cited commits exist and are ancestors | `git merge-base --is-ancestor <h> refs/heads/master` for f660ae0, 3d9ea54, b4fcd35, 52d7486, 05b02e2, 7d062c0, 9271dda, 6decc71, 8f9a898, 0ac30a1, 4290d64, d4c0cdf, a448a47, fbad1c5 | all 14 `OK`; `cb2fae38` is cited as a non-commit digest (`git cat-file -t` → fatal, as the report says) | pass |
| lane pushed, clean | `scripts/hyaku/jj-lane.sh state …/kengaku-shokunin`; `git status --porcelain` | `branch=master local=remote=3d9ea54… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty | pass |
| prompt carries template contract | `diff <(sed -n 1,140p .ufo/prompts/kengaku-round-45.md) templates/round-prompt.md` | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions differ; §§1–5 verbatim; hyaku addendum §6 and §7 follow | pass |

Not a marker: real committed round work (14 lane commits, 830 files).

Conformance defects (status-neutral, routed in §5):
- D1 `LOG.md` in-place rewrite: two lines of the committed round-45 entry (`4290d64`) were rewritten at `3d9ea54`
  (`git diff -U0 fbad1c5 3d9ea54 -- LOG.md`: `@@ -1374` heading "advertised fixture fence closed (10/10 refused …)" and
  `@@ -1388` "(A/B runs byte-equal)" replaced). An appended note names the old heading, but LOG.md is append-only: the
  correction belongs in an appended entry, the superseded lines left standing.
- D2 lesson `## Gate` records no per-new-row ≤25-word quote with location (CORPUS.md §SOURCES rule 1); the quotes live
  only in the SOURCES `anchor` cells, three of which cite the wrong line (§3).
- D3 neither C1/C2 after-receipt (`integrate/measure-final.txt`, `integrate/a3-tip-c1.txt`, `a3-tip-c2.txt`) embeds the
  revision measured; attribution (`8f9a898`, `fbad1c5`) is report text only. Mitigated: `git diff --stat fbad1c5 3d9ea54 -- plans/`
  is empty and the entry/SOURCES are unchanged after `fbad1c5`; no counter was run at the final tip.
- D4 `plans/round-45-claims.md` changed at `52d7486` after freeze `b4fcd35` (S149–S157 → S149–S156, pre-data, 23:20
  before the first probe run 23:27); the "Freeze amendments" paragraph names only `9271dda`.
- D5 two `a3w1` seats reportless (`R45MutC1Instrument2`, `R45MutC2Checks`): the C1-instrument and C2-check mutation items
  are unattacked (disclosed).
- D6 S154 `teaches` puts a paraphrase in quote marks ('exists and contains the correct password among guesses'); the
  README at the pin has no such string (`grep -n 'among guesses' README.md` → nothing; the text is `:29-31`).

## 2. Claims

### C1 — calibration (`plans/fixture_fence.py` vs its frozen counter) — evidence-verified, not re-executed

| item | evidence / command | observed | vs report |
|---|---|---|---|
| before | `claims/control-c1-fence-r44.txt`, `control-c1-nothing.txt` | r44: `REFUSALS total=10 clean=3 leaked=3 read=4`, `contradicted=7`, `PREDICATE C1 fail`; nothing: `leaked=10`, `contradicted=10`, fail, exit 1 | confirmed |
| after | `integrate/measure-final.txt`, `integrate/a3-tip-c1.txt` | both `REFUSALS total=10 clean=10`, `HONEST 104/104`, `contradicted=0`, `PREDICATE C1 pass`, exit 0, fence sha `ac65c032…` = tip bytes | confirmed (D3) |
| keyed control | `claims/fences/keyed_name.py` (7 lines: refuse iff `"/refusals45-" in str(d)`), `claims/control-c1-fence-keyed_name.txt` | `clean=10`, `HONEST 104`, `contradicted=0`, `PREDICATE C1 pass`, exit 0 | confirmed — the frozen predicate is reachable without the work |
| blinded dev counter | `claims/dev-blind-c1.diff` (3 hunks), `dev-blind-c1-keyed.txt`, `dev-blind-c1-landed.txt` | keyed `contradicted=10` exit 1; landed `contradicted=0` exit 0 | confirmed (not the frozen predicate) |
| held-out | `a3w1/R45HoIncludeIf.md` 3, `R45HoCommondir2.md` 2, `R45HoSymlinks.md` 1, `R45HoArgvEnv.md` 1, `R45HoConfigKeys.md` 1 | 8 of 10 held-out modules admitted | confirmed |
| mutation | `a3w1/R45MutLandedFence.md` | `VERDICT: fence-mutants-caught-7/15` | confirmed |
| digests | `sha256sum -c .ufo/waves/round-45/claims/frozen-digests.txt` | 18/18 OK | confirmed (D4) |

Ruling: **does not verify.** Per the round contract's control rule a predicate a no-inspection control passes cannot
certify the work, and the held-out battery contradicts the fence's advertised contract 8 times out of 10. Axis
`calibration`: **unprovable** — not harmed: SCORECARD keeps 8, the capability table was not extended, and four
self-assessment overclaims were corrected with refuting commands (`git cat-file -t cb2fae38`; `cmp counter-a-run.txt counter-b-run.txt`).

### C2 — coverage (TB2 `password-recovery` grader) — counts re-measured, predicate evidence-verified

| item | command | observed | vs report |
|---|---|---|---|
| SOURCES rows | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\| *S[0-9]{3}'` | base 141 → tip 149; S149–S156 all tier A, `mined`, `used-by` path exists | confirmed |
| knowledge files | `git ls-tree -r --name-only <rev> corpus/knowledge \| wc -l` | 51 → 52 | confirmed |
| frontier | `git show <rev>:corpus/README.md \| grep -oE '[0-9]+ of 89 read'` | max 10 → `11 of 89 read` (`corpus/README.md:430`) | confirmed |
| provenance trio | head of `corpus/knowledge/tb2-password-recovery-grader.md` | `source:` S149–S156 @ `2fd12b88`, `verified-at: 2026-10-26`, `recheck: 180d` | confirmed |
| predicate | `integrate/a3-tip-c2.txt`, `claims/control-c2-nothing.txt` | after `checks=11 defects=0`, `PREDICATE C2 pass`; before `defects=8`, fail, exit 1 | confirmed |
| captures | `sha256sum -c SHA256SUMS` in `corpus/evidence/round45/tb2-password-recovery/` | 9/9 OK | confirmed |
| predictor review (frozen rider: "non-author review of the predictor block rides admission") | in-memory: grader = `TextIOWrapper(newline=None).read().strip().split("\n")` membership; predictor = entry `:198` `text.replace("\r\n","\n").strip().split("\n")` | `C+"\ra"`, `"x\r"+C`, `"x\n\r"+C` → grader True, predictor False; CRLF states agree. Entry prose `:150,:194` claims universal-newline reading the code does not implement; no marker in the entry | **fails** |
| row anchors | live re-open (below) | S152 `:15` blank (quote `:17`, outside cited 1–16); S153 `:28` is `echo 0 > …` (quote `:26`); S154 `:44` past a 32-line file (quote `:31`); no marker in rows or entry | defect, unmarked |

Ruling: **does not verify as admitted.** The counted move is real (rows, file, frontier), so axis `coverage` grades
**improved** on its measure (score capped at 7 by L0 `kengaku | round-33`, unchanged). The claim's own freeze makes
non-author predictor review part of admission; that review fails — the entry's `## Predictor`, presented as the grader's
rule, false-negatives three lone-CR classes. Axis `depth`: **harmed** — false detail and three mislocated anchors landed
and are left unmarked in `SOURCES.md` and the entry (recorded only in `corpus/lessons/round-45.md:60-61,96`).

### Other axes

`git diff 9d5f971 3d9ea54 -- SCORECARD.md`: appended round-45 section only, no score changed. `novelty` unchanged (no
claim; the census draft sits unclaimed in `attempt1-unclaimed/`); `operability` unchanged (`plans/pkg_gate.py` untouched
this round — last commit `805fe79`; its P10 `uv run --with biopython==1.85` pre-dates the round); `freshness` unchanged;
`adjacency` unchanged (`PROVINCE.md` +2 lines, `a3w1/R45RevProvince.md` `province-defects-0`).

| axis | verdict | basis |
|---|---|---|
| calibration | unprovable | C1 counter passed by keyed control; held-out 8/10 admitted |
| coverage | improved | 141→149 rows, 51→52 files, 10→11 of 89 (re-measured); claim not admitted (rider fails) |
| depth | harmed | unmarked predictor divergence + S152–S154 anchors |
| novelty | unchanged | no claim |
| operability | unchanged | gate untouched |
| freshness | unchanged | no re-verification claim |
| adjacency | unchanged | PROVINCE review 0 defects |

## 3. Discernment spot-check (`corpus/lessons/round-45.md` `## Gate`)

Re-opened 2026-10-27 at
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/`
(HTTP 200 each; sha256 prefixes `2dc14fc1` test_outputs.py, `6fabcb9e` Dockerfile, `4770437e` test.sh, `122bf15e`
README.md, `9fdde5d9` setup.sh, `9a8dd8d9` .gitignore, `cfd0362d` task.toml — all equal to the registry/`SHA256SUMS`).

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `tests/test_outputs.py` (S149) | admit | `…/tests/test_outputs.py` | agree | the executed predicate; anchor quote `assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses` (4 words) is verbatim at `:18` as cited |
| `README.md` (S154) | admit | `…/README.md` | agree on admit; disagree on row cells | authors' own description of the check (`:29-31`); but the anchor names `:44` in a 32-line file (quote at `:31`) and `teaches` quotes a string the file lacks (D6) |
| `environment/varsea-…dat` seeds | reject | `…/environment/setup.sh` | agree | `setup.sh:7,9,22` read `/dev/urandom`; a capture would record noise, not a fact; flip condition is concrete |
| `gitignore` capture | reject (as row) | `…/.gitignore` | agree | generic ignore list (`.git/`, `__pycache__/`, `dist.tar.gz`); `grep -i gitignore` on the entry → no sentence cites it |

SOURCES row quote check: S153 anchor quote `echo 1 > /logs/verifier/reward.txt` (6 words, ≤25) is verbatim in the
re-opened `test.sh`, at `:26`, not the cited `:28` (`:28` is `echo 0 > /logs/verifier/reward.txt`). S152 quote
`RUN bash /app/setup.sh` is at `:17`, not `:15`. Quotes exist; locations are wrong.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
→ 15 `W04` (S040…S100, duplicate-url-across-scopes, same ids as `claims/census-before.txt`), `kengaku ok`, exit 0 —
matches `integrate/a3-census-after.txt`.

## 4. Trend verdicts

- `expansion`: **improved** — one new entry on uncovered ground (`corpus/knowledge/tb2-password-recovery-grader.md`,
  51→52) citing 8 `mined` tier-A rows (141→149); frontier 10→11 of 89.
- `quality`: **harmed** — the new entry's predictor is false on lone-CR states and three row anchors cite the wrong line
  (one a line carrying the opposite reward value), all left unmarked in the entry and rows. Expansion with quality harmed
  is a trade, not admitted (LEARNING.md).
- `discernment`: **improved** — the sampled admits and rejects agree with the gate (the S154 disagreement is on row
  cells, already mined as an attempt-3 Mistakes row); Q39 (`corpus/QUALITY.md:1061`) cites its lesson and is shown able
  to fail (keyed control passes the frozen counter, fails the blinded one).

## 5. Routed defects (lane fixes next round)

1. Supersede S152, S153, S154 under Q34 with correct anchor lines/ranges and a verbatim S154 `teaches`; add the
   anchor-line check to the gate with a red fixture (lesson `:96` already routes it).
2. Mark or supersede the entry's `## Predictor` (lone-CR divergence; prose at `:150,:194` overclaims universal newline)
   and add lone-CR states to V11's held-out generator.
3. LOG.md: append a correction entry for the two in-place rewritten round-45 lines (D1); never rewrite committed LOG lines.
4. Lesson Gate: record the ≤25-word quote + location per new row (D2).
5. Receipts name the revision measured inside the receipt bytes (D3); run the frozen counters at the tip that ships the report.
6. Name every post-freeze claims-file edit (`52d7486`) in the amendment paragraph (D4).
7. Carried, lane-owned: re-freeze the C1 counter under Q39 with the held-out modules as frozen refusals;
   `R45CritV11Bypass` lookup predictors; `R45SentC2Grader` F1 (P10 unpinned `uv` fetch) and F2/F3 (P9); `R45CritIntent`
   brace-prefix bypass; re-attack the two unattacked mutation items (D5).

Operator notes: the four SHONEN boxes (`[~]`) carry resolvable pointers and look checkable by a non-author
(promotion is operator-owned). `a3w1/R45SentSeatAudit.md` H3: an unattributed `OpenBot-0.51.1-x86_64.AppImage` in
`~/.local/bin` (2026-10-26 23:36:46) — owner unknown.
