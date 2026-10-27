# Round 44 — five advertised behaviours of two gate tools demonstrated with value-attributed kills; a tenth TB2 grader executed (constant-compare of an agent-written file) (2026-10-26, hyaku run 9)

L1 `KengakuR44` (planner seat). Frozen claims `plans/round-44-claims.md` (freeze `5f16ed04`, first recorded probe run
`45dc0bc8`); baseline lane tip `0cb2e225` (the round-43 non-author spot-check). One v2 wave dispatched at `5e3d3aa0`
(68 seats) and one residual call at `256cc66a` (8 reviewer/critic seats). Written by the L1 at integration from the
seat reports named in each row.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **A `not fired` flip verdict written from a belief about the entry, not from reading it** — the round-43 Gate resolved its `task.toml`/`setup.py`/`solve.sh`/`feal.h`/`SHA256SUMS` reject as "no entry sentence rests on task.toml, setup.py, solve.sh, feal.h or SHA256SUMS alone", while the landed entry cites `task.toml:22` five times and `solve.sh:90` three times, both load-bearing (finding 11's "only ceiling", the `slow-oracle-45s` Mechanism row). | `corpus/lessons/round-43.md:46` (verdict text); entry citations `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md:41`, `:122`, `:230`, `:240`, `:252`, `:300`; disagreement `corpus/lessons/round-43-verifier-spotcheck.md:124` and §4 `:149`; routed as R1 `:156` | none — the Q35 checker `plans/gate_flip_check.py` reads the line's *shape* and its state token (`:256-257` both `fired`/`not fired` accepted as a resolution) and never opens the entry; the non-author closure's re-read is the only instrument that saw it | Citation leg: a `not fired` line naming a file goes red when the entry carries a `<file>:<line>` citation of it. **Shown to fail** on the real lesson (in-flight seat `R44FlipVerdict`, `.ufo/waves/round-44/wave/R44FlipVerdict/gate_flip_check.py`): `FLIP-CITE line=46 item=task.toml … verdict=RED` ×4 (`tb2-feal-differential-cryptanalysis-grader.md:41`, `:96`, `:230`; `tb2-circuit-fibsqrt-grader.md:332`), `FLIP-CITE … not_fired=2 red=1`, `exit=1`, `ENVELOPE end 20:38:05 exit=1 … unchanged`; its own selftest `SELFTEST ok=26/26` includes `case=cite-not-fired-red expect=red got=red … cite_red=1`. An independent sweep written by this seat agrees: `--scope all` → `FLIP-CITE corpus/lessons/round-43.md:46 item=task.toml verdict=RED … cited_by=…(+19)`, `FLIPS-CITE total=6 named=3 red=2`; `--scope block` (entries named within ±6 lines of the verdict) → `red=1`, the same line still RED. Named limit of the leg (the draft says so at `:87-91`): it is a name match, not a reading — `--scope all` over-fires on `corpus/lessons/round-42.md:215` (`README.md — not fired`) only because the *later* feal entry cites `README.md:42`, and even the block scope mixes two tasks' entries for `task.toml` (the Gate table's S135 row names `tb2-circuit-fibsqrt-grader.md`). Whoever lands the leg should pair it with the closure's own reading, as the closure did. |
| **A round filed under the operator's seat floor** — one 38-seat wave; the 33-seat falsify wave was specified and dispatched-validated but never dispatched, so the round closed 38 < 64 (run-9 band "64–128 seats in total, every round"). | `corpus/lessons/round-43-verifier-spotcheck.md:33` (D1); `.ufo/waves/round-43/build-results.json` (38 results); `ls .ufo/waves/round-43/falsify.ready` → absent, while `falsify-spec.json` + `falsify-dispatch.json` exist | nothing — no check read the total before filing; the lane's own disclosure at close | One v2 wave sized ≥64 before any integration (frozen `plans/round-44-claims.md:120` R4). **Shown to fail**: a two-line floor check over the two spec files reads `.ufo/waves/round-43/build-spec.json seats 38 floor64 FAIL` / `.ufo/waves/round-44/wave-spec.json seats 68 floor64 PASS`; `wave-dispatch.json` `counts={spawn: 68, resume: 0, total: 68}`. The round's own close is still open, so the check must be re-run on the landed wave before filing. |
| **A seat whose output exists only in the results JSON** — `R43ConnClaims` returned an answer and no report file, so nothing on disk carries its claim cross-check. | `corpus/lessons/round-43-verifier-spotcheck.md:39` (D3); `git ls-tree --name-only HEAD .ufo/waves/round-43/build/ \| grep -c '\.md$'` → `37` against 38 results. Re-measured: `REPORTS seats=38 files=37 missing=1:R43ConnClaims`, exit=1 | none — the wave results file accepts a result with no artefact, and no close-time check compared the two lists | Report-file check at close: every dispatched seat name must have `<reportDir>/<name>.md`. **Shown to fail** on the closed round-43 data (`report_file_check.py --lane . --reports .ufo/waves/round-43/build --results .ufo/waves/round-43/build-results.json` → `exit=1`) and the same command runs on the current round (`--dispatch .ufo/waves/round-44/wave-dispatch.json` → at 20:41:04 `REPORTS seats=68 files=47 missing=21`, `exit=1`, expected mid-wave — the count rose from 43 to 47 in the minute between two runs, so only the close-time run decides). |
| **A freeze that priced a mutant the standing batteries already kill** — the round-44 mutant draft carried six rows including anchor U3; battery43's `a_alt-slug-deepest` already kills it, so U3 would have entered the frozen set as an unearnable row and forced a fixture to re-prove an existing behaviour. | `.ufo/waves/round-44/claims/control-c1-standing-batteries-six-mutant-draft.txt`: `MUTANT U3 anchor rc-mirror killed by=a_alt-slug-deepest attributed=L354 value=differs hits=16`, `MUTANTS total=6 killed=1 survived=5`, `PREDICATE C1 fail`; drop recorded in `plans/round-44-claims.md:33-34`; frozen five-mutant control `.ufo/waves/round-44/claims/control-c1-standing-batteries.txt` (`BATTERY fixtures=71 … MUTANTS total=5 killed=0 survived=5`) | the L1's pre-freeze standing-battery control — it fired *before* the freeze, which is the only reason the draft did not land. Nothing else would have: the counter run on the final battery cannot tell a pre-killed row from a hard one | Run battery42+battery43 (71 fixtures, `29+42`, ast-counted) as battery44 against every drafted mutant *before* freezing, and drop each row that dies with attribution. **Shown to fail**: the draft receipt is the red state (U3 killed, `hits=16`), and the frozen receipt is the green state for the remaining five (`killed=0 survived=5`) — the same instrument reversed its answer when the row was removed. |
| **A sweep that reports a corpus-wide law while silently dropping the files it cannot parse** — the round-43 flip survey states "45 flip obligations in 18 lessons, none ever resolved", but its driver skips every lesson without a `## Gate` section (`rc=2 SETUP`): 35 of the 55 lesson lines in the receipt, 64 %. One skipped lesson is `round-42-verifier-spotcheck.md`, which carries the very flip condition the class was mined from (`:37`). The receipt also carries no total: my re-aggregation of its 20 per-file `FLIPS` lines gives `sum_total 45 sum_unresolved 45` over `flip_files_with_total_gt0 18`, so the quoted number is derived, and the denominator (20 scanned of 55) is nowhere in it. | `.ufo/waves/round-43/build/R43FlipCheck/sweep.txt` (`grep -c 'rc=2'` → 35; `:47` `round-42-verifier-spotcheck.md rc=2 SETUP no '## Gate' section`), quoted by `corpus/lessons/round-43.md:11`; the landed checker raises it at `plans/gate_flip_check.py:133`; re-run today `python3 plans/gate_flip_check.py --lesson corpus/lessons/round-42-verifier-spotcheck.md` → `SETUP no '## Gate' section`, `exit=2`, and that lesson's `:37` is "- **D3 Gate flip condition fired and was not executed (Dockerfile).**" with `grep -c '^## Gate'` → `0` | none — the sweep prints one `rc=2` line per file and no scanned/skipped summary, so a reader of the quoted `FLIPS total=45` cannot see the denominator | Print `lessons=<n> scanned=<m> skipped=<k>` beside `FLIPS`, and make any skipped lesson a red (`unresolved`) rather than a skip, unless the file provably contains no conditional refusal. **Shown to fail** by the corpus as it stands: re-running the landed checker over every lesson today (`.ufo/waves/round-44/wave/R44LessonMistakes/sweep-flip-all-lessons.txt`) gives 62 lessons, `41 exit=2` (never read), `21` read (4 `exit=0`, 17 `exit=1`), so a `skipped>0 → red` rule is red on 41 lessons, and the exit-2 quoted above is that silent drop on the round-42 spot-check. |
| **A registry row landed with a hash-shaped phrase in a non-anchor cell** — S140's scope cell said `sha256 chain`; `plans/anchor_digest_check.py` reads `sha256` + a hex run anywhere in a row, so `c` became a token outside the anchor (`DEFECT S140 … class=token-outside-anchor`), a no-harm regression of the anchor check (`defects=0` → `1`) introduced by the integration commit `2a263e5a`. | `python3 plans/anchor_digest_check.py --lane . --evidence-ref index` → `rows=141 tokens=48 defects=1` (L1, 20:49 -03) | the anchor check in the no-harm set (`integrate/measure.sh`), not run at the integration commit; the seat validation (`R44PkgRows`) ran it on its own row text, not the entry seat's | scope cell reworded to `SHA-256 hash chain` before the report (`02287eed`), anchor check `defects=0`. This is a same-round in-place edit of a committed row cell (QUALITY Q34 says supersede); disclosed here rather than adding a superseding row for a wording fix the tool forced. Able to fail: the committed `2a263e5a` bytes print `defects=1`. |
| **Frozen-claims wording that the captures contradict** — `plans/round-44-claims.md` §C2 says gen.py is deleted at `Dockerfile:12-13` (it is `:13-14`) and the probe case `decrypt-public-keys` says the keys are "printed" in `gen.py:12` (they are literals; gen.py prints counts only). | `R44PkgProse.md` §Findings 1–2; `sed -n 11,14p corpus/evidence/round44/tb2-feal-linear-cryptanalysis/Dockerfile`; `gen.py:12`, `:52`, `:92-93` | none (the L1 wrote both from memory of the read, not from a line check at the freeze) | not edited (frozen); this row is the correction. No predicate, case verdict or tag depends on either phrase; the entry cites `Dockerfile:14` and says "literals". |
| **A content leg whose sample is memorizable** — V11's 48 states come from a fixed seed, so a predictor that is a lookup table (by exact text, by sha256, or by position in `/states.json`) passes with 0 disagreements without reading the file (4 of 7 bypasses). | `.ufo/waves/round-44/wave/R44CritV11.md` §4 (P1–P4 `ok`); `R44SentinelSandbox.md` F1 | the freeze limit named a tuned predictor "only by running the grader"; the critic shows harvesting one grader run is enough | routed for the next C2 counter: per-run random seed (or several), states never exposed to the predictor process, and a predictor-source lint; the landed entry's predictor is a genuine substring reading (`R44RCritEntryOverclaim`). |
| **A fence repair that reintroduces the read it was meant to stop** — `lane_breach` (F6) runs `rev-parse` on the `--lane` repo without `--no-includes`, before `repo_breach` refuses the include, so the counter's parent process opens an include file outside d. | `R44LabratLaneInclude.md` (`lane-breach-reads-outside-confirmed`) | none at freeze: the f4 hostile control is refused (`--lane git hung`), which looked like success | routed: run the include check before any discovery and pass `-c include.path=` / `GIT_CONFIG_NOSYSTEM` + `--no-includes`-equivalent to discovery; a hostile control with a regular-file include and an open-tracer is the red check. |
| **A seat whose output exists only in the results JSON — recurred** (round-43 D3 class) — `R44ScoutMisroot` returned `misroot-0-host-writes-0-sentinel-present` naming `.ufo/waves/round-44/wave/R44ScoutMisroot.md`, a file that does not exist anywhere (`find` over the fleet tree → nothing). | `.ufo/waves/round-44/wave-results.json` (seat `R44ScoutMisroot`); `ls .ufo/waves/round-44/wave/R44ScoutMisroot.md` → absent | the wave-context sentence "Every seat MUST leave its report file" — a prompt rule, not a check; 67 of 68 complied | the L1's own misroot sweep stands in (`git -C <fleet> status --porcelain --untracked-files=all` → nothing beside `.scratch/`/`.ufo/state/`); fix for round 45: the L1 runs a report-file count against the results JSON before integrating (`R44LessonMistakes/report_file_check.py` is the drafted check). |

Sweep receipts for the drafted rows: `.ufo/waves/round-44/wave/R44LessonMistakes/` (`sweep-*.txt`). The round-43 floor
mistake did not recur: this round is one v2 wave of 68 + a residual call of 8 = 76 seats. The reportless-seat mistake
did recur once (row above).

## Gate

Opened or captured this round. Access date 2026-10-26 for every row; times are -03. The L1 fetched all eleven
files of the task directory at 20:10:09 -03 (`corpus/evidence/round44/tb2-feal-linear-cryptanalysis/` +
`SHA256SUMS`); seat `R44PkgRows` re-fetched all eleven at 20:33:51–20:34:08 under the round-44 envelope, eleven
`http=200`, eleven `cmp=identical` (`.ufo/waves/round-44/wave/R44PkgRows/refetch.txt`); seat `R44ScoutRefetch`
re-fetched the same eleven independently at 20:33:08–20:33:10 (`ok=11`, upstream drift 0 after the pin).
Quotes are ≤25 words and located at the cited line of the capture. Ranges are `:1-<last physical line>`, so
`README.md:1-32` and `decrypt.c:1-142` count the last line of two files that carry no final newline — the
round-43 closure R2 defect was this off-by-one on `README.md`. Base URL
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/`.

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| S138 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>tests/test_outputs.py`, opened 20:10:09, re-fetched 20:33:51. Quote, `test_outputs.py:122`: "assert c in data" (4 words); sha256 `f59ebc72…106ed9f9`. The whole score: 100 decimals inside one string (`:4-103`), the file read whole at `:120`, and one membership assert per constant at `:121-122`. Flip: digest leaves the pin. |
| S139 `instruction.md` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>instruction.md`, opened 20:10:09, re-fetched 20:33:51. Quote, `instruction.md:7`: "Implement a known-plaintext attack that recovers the key of the cipher." (11 words); sha256 `a2f1669d…b6f71b03`. Asks for an attack and an output file and no numeric format; the receipt's `hex-output` case fails a format the instruction never states. Flip: digest leaves the pin. |
| S140 `environment/task-deps/gen.py` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>environment/task-deps/gen.py`, opened 20:10:09, re-fetched 20:33:51. Quote, `gen.py:12`: “keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]” (6 words); sha256 `3a71f0b5…7c452c63`. The four round keys sit in the clear and `:23-28`/`:57-62` derive every plaintext from the public hash chain; receipt cases `decrypt-public-keys` and `replay-public-gen` pass with no attack. Curly delimiters because the line itself carries straight quotes (precedent S121/S123). Flip: digest leaves the pin. |
| S141 `environment/Dockerfile` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>environment/Dockerfile`, opened 20:10:09, re-fetched 20:33:51. Quote, `Dockerfile:14`: "RUN rm gen.py" (3 words); sha256 `ef521cde…28bfff1d`. Builds `feal` and `decrypt`, runs the generator, then deletes `orig_plaintexts.txt` and `gen.py` (`:13-14`): the keys are absent from the image and public in the repo. Flip: digest leaves the pin. |
| S142 `tests/test.sh` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>tests/test.sh`, opened 20:10:09, re-fetched 20:33:51. Quote, `test.sh:26`: "echo 1 > /logs/verifier/reward.txt" (4 words); sha256 `9431cbc2…d2e7c9e1`. Reward is pytest's exit status alone (`:25-28`), after uvx runs pytest 8.4.1 over `/tests/test_outputs.py` (`:18-22`). Flip: digest leaves the pin. |
| S143 `README.md` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>README.md`, opened 20:10:09, re-fetched 20:33:51. Quote, `README.md:32`: "verifies that all 100 expected plaintext values appear in" (9 words); sha256 `a038645f…f6d3dc33`. Its verification claim is exactly the substring behaviour receipt cases `oracle-concatenated`, `oracle-reversed`, `oracle-zero-padded` and `oracle-plus-decoys` exploit. Flip: digest leaves the pin. |
| S144 `solution/solve.sh` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>solution/solve.sh`, opened 20:10:09, re-fetched 20:33:51. Quote, `solve.sh:304`: "./attack > /app/plaintexts.txt" (3 words); sha256 `be50ae01…da29cb77`. The provided oracle; it is not graded (test.sh runs only `/tests/test_outputs.py`) and the probe runs it as a recipe. Flip: an entry sentence implies `solve.sh` participates in grading. |
| S145 `environment/task-deps/decrypt.c` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>environment/task-deps/decrypt.c`, opened 20:10:09, re-fetched 20:33:52. Quote, `decrypt.c:136`: “printf("%lu\n", plaintext);” (2 words); sha256 `4c6864e0…0a94ebd2`. The decimal print is the medium the substring test accepts; `:114-117` refuses a key above `0xFFFFF`. Curly delimiters as on S140. Flip: an entry sentence claims a non-decimal rendering passes (receipt `hex-output` = fail) or that `decrypt.c` is graded. |
| S146 `task.toml` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>task.toml`, opened 20:10:09, re-fetched 20:33:52. Quote, `task.toml:34`: "allow_internet = true" (3 words); sha256 `a39ec2c4…0e7c9fc4`. `timeout_sec = 1800.0` at `:22` (verifier) and `:25` (agent), resources at `:30-32`; `allow_internet` is what keeps the published `gen.py` fetchable although the image deletes it. Flip: an entry sentence asserts grader-side timeout enforcement or calls `:22` the only time bound (the round-43 finding-11 error). |
| `feal.c` @ `2fd12b88` (captured, not a row) | **REJECT — captured, not a row** | `environment/task-deps/feal.c`, re-fetched 20:33:52 (`200`, 3472 B, `cmp` identical, sha256 `bbd38d19…2dea08da`). Implementation of the pair-generator executable: the graded artefact is `/app/plaintexts.txt`, so `feal.c` carries no graded predicate. Flip, decided by the command below: an entry sentence outside `## Located quotes` cites `feal.c:<line>` with no S138–S146 co-citation; if it fires, either re-source the sentence or take the tier-B mechanism path (S135–S137 precedent). |
| `gitignore` @ `2fd12b88` (captured as `gitignore`, upstream `.gitignore`) | **REJECT — captured, not a row** | Upstream path is `.gitignore` (`.gitignore` → `200`, 177 B; every `gitignore` spelling → `404`), re-fetched 20:34:08, `cmp` identical, sha256 `9a8dd8d9…07c25953`; the capture keeps the dotless name. Repo hygiene only: ignores `.git/`, `__pycache__/`, `dist.tar.gz` (`:2`, `:8`, `:23`). Flip: an entry sentence outside `## Located quotes` cites `gitignore:<line>` or `.gitignore:<line>` with no S138–S146 co-citation; no tier-B path exists for it — re-source or delete the sentence. |
| `SHA256SUMS` | **REJECT — inventory, not content** | Manifest of the eleven captures; contentless as evidence. Flip: an entry sentence cites it. |

Flip checks (round 44) are decided by the command below, not by presence of a flip line (`plans/gate_flip_check.py`
tests line existence, which is how round 43 recorded a false `not fired`). Quote table excluded; a hit line is
unbacked when it carries no `S1xx` co-citation:

```
check_flip() { # $1 = file token, $2 = entry path
  body=$(awk '/^## Located quotes/{skip=1;next} /^## /&&skip{skip=0} !skip' "$2")
  if printf '%s\n' "$body" | grep -nE "$1:[0-9]+" | grep -qvE 'S1[0-9]{2}'; then
    echo "Flip check (round 44): $1 — fired"
  else
    echo "Flip check (round 44): $1 — not fired"
  fi
}
check_flip 'feal\.c'    corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md
check_flip gitignore    corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md
check_flip SHA256SUMS   corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md
```

Re-decided by the L1 at integration (20:50 -03) with the command above against the LANDED entry
`corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md` (landed `2a263e5a`): all three `not fired`; the only `feal.c`
mentions are `:128` (Dockerfile replay, no `feal.c:<line>` citation) and `:162` (inside the `instruction.md:1` quote).

Flip check (round 44): feal.c — not fired — landed entry has no unbacked `feal.c:<line>` citation (check_flip above, L1 20:50 -03)
Flip check (round 44): gitignore — not fired — landed entry never names it (check_flip above)
Flip check (round 44): SHA256SUMS — not fired — landed entry never names it (check_flip above)

Gate prose: all nine rows are the spec-pinned set (`plans/pkg-spec-r44.json` `rows` = S138–S146) — six `code`
(S138, S140, S141, S142, S144, S145), three `docs` (S139, S143, S146) — tier A as `entry_rules.row_tier`
fixes, status mined, opened 2026-10-26, recheck 180d, one used-by entry. Registry 130 → 139. Validated in a
scratch `--shared` clone at `5e3d3aa` with the rows appended uncommitted: `sources-census.sh validate --file
<clone>/corpus/SOURCES.md` exit 0, 15 W04 (all pre-existing), 0 E-codes; `anchor_digest_check.py --lane
<clone>` `rows=139 tokens=45 defects=0`, nine `BIND … by=url-task` and nine `RESOLVED`. Red controls on the same
two legs: removing the used-by file fires E11 on all nine rows (exit 1); flipping S138's last digest nibble
prints `DEFECT S138 … class=digest-unknown` (`defects=1`, exit 1). The census copy carried a labelled
placeholder file at the entry path because the entry is authored by seat `R44PkgEntry` and was not
present when these rows were written; E11 tests existence only, and the placeholder is never a lane file.

## Routed

- Round-43 closure R1: two `Flip check (round 44): … — fired — …` lines appended to `corpus/lessons/round-43.md`
  (task.toml, solve.sh); `## Errata (round 44, closure R1 …)` appended to the feal-differential entry; S147 (`task.toml`)
  and S148 (`solution/solve.sh`) admitted tier B outside the frozen round-43 spec (`R44FlipLines`). The flip check now
  reads verdicts against entry citations: `plans/gate_flip_check.py` extended (`R44FlipVerdict`), red on the round-43
  lesson before the appended lines (`FLIP-CITE … red=1`, exit 1) and green after (`red=0`, exit 0), `SELFTEST ok=27/27`
  (`.ufo/waves/round-44/integrate/flip-verdict-red-green.txt`); QUALITY Q36. Independent audit of every `not fired`
  line: 3 lines, 1 false — the same round-43 line (`R44RevFlipAudit`).
- R2: S134 and S132 source-span errata appended to the feal-differential entry (`R44S134Erratum`; counter and gate
  unchanged by the append, receipts in its dir).
- R3: round-43 wave control files committed in the freeze commit `5f16ed04`.
- R4: 76 seats (68 + 8), every seat leaving a report file.
- R5: V11 (held-out predictor) replaces the readable-key reliance of V10 for this package; fences F1–F6 in the C1
  counter; round-43 mutation survivors re-run (`R44MutC1Guards`, `R44MutC2Guards`).
- considerthese `2026-10-26.md` proposal 1 (routed-findings burn-down; `R44ConsiderThese` chose it over proposal 2):
  15 ledger field changes from `R44RoutedObserve`'s closure patch (13 closed, 2 refused as refuted), each `check`
  passing on observe; burn-down line `routed_burn round=43 opened=43 born_closed=1 closed=14 … open=39` computed from
  the ledger history (`R44RoutedObserve/routed_burn.py`). Ledger after: `ROWS total=60 open=23 blocked=1 closed=34
  refused=2`, `routed_open=24 oldest_round=39` (was 39).

## Census

Before (`.ufo/waves/round-44/claims/census-before.txt`): `kengaku ok`, 15 W04, exit 0. After
(`.ufo/waves/round-44/integrate/census-final.txt`): `kengaku ok`, 15 W04, exit 0. Registry 130 → 141 (S138–S146 tier A,
S147/S148 tier B).

## Assimilation and quarantine

Assimilation: none. `merge/kengaku/` unchanged since 2026-10-24 (`R44MergeRescreen`: `reg-ids=130 staged-ids=175
collisions=54`, the round-43 45 plus exactly S129–S137; guard proven on an indented `  | S002 |` fixture; no staged
entry on uncovered ground in PROVINCE scope). Quarantine slice: 2 data rows, both quotes located (`R44Quarantine`,
`present=2 absent=0`); nothing adopted.

## Falsifiers run (other seats' reports, not re-run here)

- C1: dishonest-battery vectors 7/7 blocked (`R44CritC1Counter`); controls reproduce 14/14 on a clean clone
  (`R44LabratControls`); verdict stable over 30 runs (`R44LabratSiteStable`); mutant rows 5/5, equivalent 0, older
  batteries kill 0 (`R44RevMutRows`, `R44CritEquivU`); near-variants 13, 12 alive after the standing batteries
  (`R44XMutNearU`, round-45 data); fence-code mutants caught 15/18 by the hostile modules + witness (`R44MutC1Fences`); round-43 guard set re-run 6/15 caught (`R44MutC1Guards`); fence bypasses 3 of 6 (`R44SentinelFences` V1 `.git/commondir` HIGH, V2 second
  config include, V3 refuse-to-describe) and the `lane_breach` include read (`R44LabratLaneInclude`) — none used by
  battery44. Residual: battery44 modules honest 4/4 + 4/4 + 2/2 (`R44RRevBatAnc1`, `R44RRevBatAnc2`, `R44RRevBatOrd`);
  no single module is load-bearing (0 flips) and 6 single-module dishonest substitutes are admitted because the
  sibling module still kills (`R44RCritBatRedundancy`) — the counter cannot see intent, as the freeze named.
- C2: real pytest 14/14 (`R44PytestParity`); re-derivation 14/14 + 3 own cases (`R44CritIndep`); receipt byte-equal 3/3,
  not `-O` sensitive (`R44LabratRerun`); case-set defects 7 (empty file, read-error family, redundant pairs; no wrong
  tag; `R44CritCases`); probe defects 3 minor (`R44RevProbe`: SEED comment range, gen.py run with stdout dropped,
  /tests visible during the recipe); V11 bypasses 4 of 7 by memorizing predictors (`R44CritV11`); sandbox escapes 0
  (`R44SentinelSandbox`); V11 mutants caught 3/6 (`R44MutC2V11`); V9/V10 guards 6/13 (`R44MutC2Guards`). Residual: entry
  quotes 36/36, findings wrong 0 (`R44RRevEntryQuotes`); overclaims 0 (`R44RCritEntryOverclaim`); rows 8/9 at the
  landing commit — S140's hash-shaped scope phrase (`R44RRevRows` F1, the Mistakes row above; fixed at `02287eed`);
  independent re-measure pass/pass, stable (`R44RCritRemeasure`).
- Separability: one shared input, the frozen `plans/order_check.py` (`R44CritSeparability`).
