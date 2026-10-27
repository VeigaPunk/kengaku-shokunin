# R44ReadmeIndex — README index parity (round 44, scribe)

Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; seat is a leaf (no subagents, no background
jobs, no `task`). Target file `corpus/README.md` (560 lines at read time) — **read only, not edited**: this
seat drafts for the L1.

Axes named: (1) index parity per corpus dir, (2) accuracy of every drafted description against the file it
describes, (3) paste-readiness (exact row shape, insertion point, no invented claims).

## 1. Measured parity

| surface | command | output |
|---|---|---|
| `lessons/` on disk | `ls corpus/lessons \| wc -l` | `62` |
| `lessons/` indexed | `grep -c '^\| `lessons/' corpus/README.md` | `33` |
| `lessons/` set diff | `comm -23 <(ls lessons \| sort -u) <(grep -oE '`lessons/[^`]+\.md`' README.md \| tr -d '`' \| sed 's\|^lessons/\|\|' \| sort -u)` | **29 filenames**, `0` indexed-but-absent |
| `knowledge/` parity | same two-step diff over `ls knowledge` vs `` `knowledge/…` `` | **50 vs 50, `comm -3` empty — complete, nothing to draft** |
| `evidence/` on disk | `ls -d corpus/evidence/*/` | `38` dirs |
| `evidence/` index-grade refs | `grep -oE '^[\|*-] `?evidence/[A-Za-z0-9._-]+/' README.md` (a table row **or** a bullet) | `30` distinct dirs |
| `evidence/` missing | `comm -23` over the two sets | `8`: `round29-attempt2`, `round30`, `round31`, `round32`, `round33`, `round41`, `round42`, `round44` |

Notes that change the count a reader will reproduce:
- `grep -c '^\| `evidence/' corpus/README.md` gives `23`, not 30 or 38, because every round-34+ dir is a
  **bullet** under its own `### Round-N evidence` section, not a table row. The dispatch's file-count
  metric (`66` entries via `ls evidence | wc -l`) counts 28 root-level `.log` receipts as well as dirs;
  `ls -d evidence/*/` = 38 is the dir count.
- `round29-attempt2` is **not** missing: it has its own section, `### `evidence/round29-attempt2/` — round-29
  attempt-2 adoption receipts` at `README.md:97`. It only looks missing to a dir-vs-row grep. Seven dirs
  therefore need new rows, which is what I drafted.
- The 29 missing lessons files are exactly `round-29-verifier-spotcheck.md` and `round-30.md` …
  `round-43-verifier-spotcheck.md` (rounds 30–43, lesson + spot-check each), i.e. every lesson from the
  round-30 boundary onward. The index stops at `round-16-recensus.md`/`round-13-coverage.md`.

## 2. What is drafted (43 rows)

| block | rows | content |
|---|---|---|
| A | **29** | `lessons/` index rows, same three-column shape as the existing table (`Entry \| Covers \| Evidence`) |
| B | 4 | new `### Round-30 to Round-33 evidence` section — one bullet per unindexed dir |
| C | 4 | `### Round-41 evidence` (capture dir, probe receipt + dry table, PR #245 capture, `plans/battery41/`) |
| D | 3 | `### Round-42 evidence` (capture dir, probe receipt + dry table, `plans/battery42/`) |
| E | 3 | `### Round-44 evidence` (capture dir, probe receipt + dry table, and a **conditional** `plans/battery44/` bullet) |

Insertion points (line numbers as read, `README.md` at 560 lines): Block A appends to the lessons table
(header `:106`, last row `:128`); Block B goes immediately before `### Round-34 evidence` (`:506`); Blocks C
and D immediately before `### Round-43 evidence` (`:556`), C then D; Block E at end of file.

## 3. Provenance of each description

No description was invented; each was read off the file it describes.

- **Lessons rows**: for all 29 files I read the head (frontmatter/`#` title/baseline-and-freeze paragraph)
  plus the `##`/`###` section list, and for rounds 30–43 the `## Gate` table rows. The `Covers` cell states
  what the file's own Gate/Mistakes sections say, including the honest-stop and refusal verdicts (round 34
  `0 admitted; 6 refused/held`, round 38 `killed=21 survived=1`, round 41 `23/23`, round 42 `14/14 …
  unattributed=0`, round 43 `9 killed`). The `Evidence` cell cites the claims file and receipt dir that the
  file itself names, plus the baseline/tip hashes each spot-check prints in its own head.
- **Round-30…33 bullets**: from `ls` of each dir plus the head of every receipt (`census-before/after`,
  `adoption-after`, `defects-after`, `quote-mode-*`, `gate-selftest-after`, `round32/catalogs/after.txt`,
  `round33/catalogs/after.txt`). Quoted numbers are the receipts' own lines (`checks=5 defects=0`,
  `SELFTEST cases=14 failed=0`, `checks=10 defects=0`, `checks=6 defects=0`, `hf_models=50 or_models=467`).
- **Round-41/42/44 bullets**: from `ls -la` of each capture dir, the `SHA256SUMS` line for every file, the
  probe receipt's first header lines (capture sha256s) and its own last two lines
  (`cases=25 observed_pass=6 observed_fail=19 mismatches=2`, `cases=16 … 7/9 … 0`, `cases=14 … 8/6 … 0`), plus
  the dry tables' final `cases=… predicted_pass=… predicted_fail=…` lines. Battery lines are quoted from
  `corpus/lessons/round-41.md:7` and `corpus/lessons/round-42.md:147` (landing measurements), not re-run.

## 4. Observations for the L1 (not pasted into README)

**O1 — the round-30 quote-mode receipt does not locate three rows in a source capture.**
`corpus/evidence/round30/quote-mode-six-rows.txt` (sha256 `63aa8ced9bb4424e2d1e88f655e2fe226a4d5f076938f0f854d2b5fcb334e847`)
lines 6 / 13 / 19 record `artifacts=.git/COMMIT_EDITMSG,.git/FETCH_HEAD,…` — a `.git` directory listing —
and the `ok S081` / `ok S082` / `ok S084` spans that follow are located at `.ufo/waves/round-30/build/R30RowSchema.md`,
`R30SrcS081.md`, `R30ConnCorpus.md`, `R30RevEntryQ1Q6.md` (the lane's own drafts), while lines 4 / 11 / 17
record `ls: cannot access '/tmp/r30fx-c3cli/cap/S081|S082|S084/*.html'`. The same file's S083 and S085 lines
are `REFUSED … absent` against pdftotext text, which matches the hyphen/newline limits printed on those lines;
`corpus/lessons/round-30.md:78-97` (§Sources opened this round) does record each row's quote with page/line.
I did not rewrite the row to claim otherwise and did not open this as a routed ledger row myself (write scope).

**O2 — untracked `__pycache__` inside three capture dirs.** `find corpus/evidence plans -name __pycache__`
lists `corpus/evidence/round35/tb2-eval/`, `corpus/evidence/round36/tb2-regex-log/`,
`corpus/evidence/round41/tb2-constraints-scheduling/` (plus five under `plans/`). `git ls-files
corpus/evidence/round41` shows none of them tracked and `.gitignore:2` is `__pycache__/`, so no shipped
capture is polluted — but they appear in a plain `ls` of a capture dir whose `SHA256SUMS` does not list them.

**O3 — round-44 capture naming.** The upstream repository dotfile is captured as `gitignore` (leading dot
dropped); `SHA256SUMS` covers it under that name and `plans/pkg-spec-r44.json` does not map it to a row.
Block E states this and says `feal.c` / `gitignore` are captures, not rows — nine of eleven files are rows
(S138–S146), which is what the spec's `rows` map contains.

**O4 — S138–S146 are not yet in the registry.** `corpus/SOURCES.md` holds `130` id rows
(`grep -oE '^\| S[0-9]{3}' corpus/SOURCES.md | sort -u | wc -l` → `130`), last id **S137** (feal
`environment/feal.py`), and `corpus/lessons/round-43.md` Gate prose puts the registry at `121 → 130` after
round 43. Block E therefore names S138–S146 as *this round's admission*; it must land in the same commit as
those rows or it pre-announces a registry state that does not exist.

**O5 — `plans/` index is stale (informational, out of scope).** `ls plans | wc -l` = `116` entries against
`63` distinct `plans/…` paths referenced anywhere in README (raw counts, different units — not a parity
measure). The `### `plans/` — plans, frozen instruments, and templates` table stops at round-27 artifacts:
`plans/battery40`–`battery43`, `plans/round4{0,1,2,3,4}_c{1,2}_verify.py`, `plans/pkg-spec-r4*.json`,
`plans/feal_probe.py`, `plans/feal_linear_probe.py`, `plans/pkg_gate.py` have no row. The dispatch named
lessons/knowledge/evidence only, so I drafted nothing here.

**O6 — Round-43 evidence section is already present and complete** (`README.md:556-560`, three bullets:
capture dir, probe receipt + dry table, `plans/battery43/`). I did not duplicate it; Blocks C and D are
inserted before it to keep round order, and E after it.

## 5. Verification performed (and not performed)

Read-only only: `ls`, `wc`, `comm`, `sort`, `grep`, `sha256sum`, `sed -n`, `git ls-files`, `git status
--porcelain`, and file reads. **No battery, counter, probe, fixture build, clone, or git/jj mutation ran**, so
no run could write inside or outside the sandbox and there are no `ENVELOPE` lines to paste (host-safety
envelope applies to battery/counter/fixture/probe runs; none were executed by this seat). Nothing here is an
execution claim about the frozen instruments — the receipt numbers I quote are read off committed files.

## 6. Out of scope / deliberately not done

- No edit to `corpus/README.md`, `corpus/lessons/`, `corpus/SOURCES.md`, `plans/`, the routed ledger, or any
  lane file; no commit, no jj command.
- No knowledge rows drafted — `comm -3` over `ls knowledge` vs `` `knowledge/…` `` is empty.
- Round-44 claim work (battery44, counters, package gate) belongs to other seats; the only round-44 content
  here is the evidence-section row set, with the `plans/battery44/` bullet marked conditional.

## 7. Paste-ready blocks

The following is the verbatim content of
`.ufo/waves/round-44/wave/R44ReadmeIndex/rows-paste-ready.md`
(101 lines, sha256 `f49383be4274185a87a79175dd6545bee13de3f34bb81468ed05b51ae68c7b13`), appended byte-for-byte
below this line.

# R44ReadmeIndex — paste-ready README blocks (draft for L1)

Target: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md` (560 lines at read time).
Nothing here is applied; the L1 pastes.

Insertion points (line numbers at read time):
- Block A → append to the `### `lessons/` — round lessons and audits (index)` table (header at `:106`, last row at `:128`).
- Block B → immediately before `### Round-34 evidence` (`:506`).
- Block C and Block D → immediately before `### Round-43 evidence` (`:556`), in this order.
- Block E → end of file (after the Round-43 block's last bullet, `:560`).

---

## Block A — 29 missing `lessons/` index rows

| Entry | Covers | Evidence |
|---|---|---|
| `lessons/round-29-verifier-spotcheck.md` | Non-author verification of round-29 attempt 2: C1/C2 re-measured from committed bytes, a non-author discernment sample, axis and trend verdicts, routed defects; no lane-authored file edited | `.ufo/reports/round-29/kengaku.md`; baseline `1f3b0f1e`, lane tip `2ff4b6f8` |
| `lessons/round-30.md` | Assimilation round 2 with a quote-validating gate: `contamination-transparency-card.md` admitted as the amendment round 29 demanded, `judge-calibration-thresholds.md` refused; routed-defect closure D1–D5; counter blind spots recorded unsmoothed | `plans/round-30-claims.md`; `corpus/evidence/round30/`; `.ufo/waves/round-30/` |
| `lessons/round-30-verifier-spotcheck.md` | Non-author closure spot-check of round 30's filed bytes plus its three appended errata | `.ufo/reports/round-30/kengaku.md`; baseline `363a4ebf`, tip `2dcf06c5` |
| `lessons/round-31.md` | One theme (*how a benchmark verifier runs*): `benchmark-verifier-execution-model.md` admitted re-grounded on S092/S093/S100, four packages refused; citation-bound adoption gate and its CLI exits | `plans/round-31-claims.md`; `corpus/evidence/round31/`; `.ufo/waves/round-31/` |
| `lessons/round-31-verifier-spotcheck.md` | Non-author spot-check of round 31: C1/C2 re-measured, C3 evidence-verified rather than executed | before `0883e72e`, after `87f0d32e` |
| `lessons/round-32.md` | Id-collision refusal of `benchmark-grader-semantics.md` (S094/S097/S101/S102 collide with live rows), catalog-freshness claim declared failed as measured, `catalog_probe.py` `mkdir` repair | `plans/round-32-claims.md`; `corpus/evidence/round32/` |
| `lessons/round-32-verifier-spotcheck.md` | Non-author spot-check of round 32: C1 re-measured from committed id lists and receipts, C2/C3 evidence-verified | before `f20a1097`, after `bcd2a6c0` |
| `lessons/round-33.md` | Renumbered assimilation (staged S094→S103, S097→S104) admitting `benchmark-grader-semantics.md`; catalog rows S101/S102 rejected; byte-retained catalog captures | `plans/round-33-claims.md`; `corpus/evidence/round33/` |
| `lessons/round-33-verifier-spotcheck.md` | Non-author spot-check of round 33 | before `112091c2`, after `4e6a8b1f` |
| `lessons/round-34.md` | Honest stop: C1/C2 counters not admitted (false greens in the frozen counter, mutants misaligned to checks), two quarantine rows refused, six package candidates refused or held; erratum appended round 35 | `plans/round-34-claims.md`; `.ufo/waves/round-34/build-results.json` |
| `lessons/round-34-verifier-spotcheck.md` | Non-author spot-check of round 34 | before `5022357c`, after `58a19f37` |
| `lessons/round-35.md` | One TB2 grader read and executed (`protein-assembly`, S105–S107 admitted); the four routed defects become the `defects.jsonl` ledger | `plans/round-35-claims.md`; `corpus/evidence/round35/` |
| `lessons/round-35-verifier-spotcheck.md` | Non-author closure spot-check of round 35 | before `5d0c73db`, after `e7f0decd` |
| `lessons/round-36.md` | Hardened package gate `plans/pkg_gate.py` plus the `regex-log` grader (S108–S110); Amendment 1 normalises the `mkdtemp` path in printed assertion text | `plans/round-36-claims.md`; `corpus/evidence/round36/` |
| `lessons/round-36-verifier-spotcheck.md` | Non-author closure spot-check of round 36 | before `b662a5d6`, after `0fb87f88` |
| `lessons/round-37.md` | Advertised gate classes made demonstrable (55/55 frozen mutants) and a third TB2 grader (`configure-git-webserver`, S111–S114); wave 2 finds near-variants only 23/36 killed | `plans/round-37-claims.md`; `corpus/evidence/round37/` |
| `lessons/round-37-verifier-spotcheck.md` | Non-author closure spot-check of round 37 | before `3ea9a1d9`, after `dc90676b` |
| `lessons/round-38.md` | Gate behaviours attributed 21/22 with one frozen direction mislabelled (N21) and a fourth TB2 grader (`build-pmars`, S115/S116); baseline erratum against the round-37 landing commit | `plans/round-38-claims.md`; `corpus/evidence/round38/` |
| `lessons/round-38-verifier-spotcheck.md` | Non-author closure spot-check of round 38 | before `fc1174f5`, after `1fa7af45` |
| `lessons/round-39.md` | Seven undemonstrated gate behaviours made demonstrable with witnessed directions, and a fifth TB2 grader (`git-leak-recovery`, S117/S118) | `plans/round-39-claims.md`; `corpus/evidence/round39/` |
| `lessons/round-39-verifier-spotcheck.md` | Non-author closure spot-check of round 39 | before `b2bdd425`, after `9d3aff94` |
| `lessons/round-40.md` | Three tripwire tools mutation-tested 21/21 and a sixth TB2 grader (`db-wal-recovery`, S119–S121); a pid-namespaced hostile control measures the class it closes | `plans/round-40-claims.md`; `corpus/evidence/round40/` |
| `lessons/round-40-verifier-spotcheck.md` | Non-author closure spot-check of round 40 | before `d3a6277f`, after `5b73c5e8` |
| `lessons/round-41.md` | A calibration battery that binds its own totals (48 fixtures, 23/23 mutants) and a seventh TB2 grader (`constraints-scheduling`, S122–S124); the reachability control named as a loophole | `plans/round-41-claims.md`; `corpus/evidence/round41/` |
| `lessons/round-41-verifier-spotcheck.md` | Non-author closure spot-check of round 41 | before `e50c1345`, after `e61aff6f` |
| `lessons/round-42.md` | A battery whose kills must be attributed (29 fixtures, 14/14 mutants) and an eighth TB2 grader (`circuit-fibsqrt`, S125–S128); two carried mistakes — a declared direction copied from a table, a kill credited to a fixture that did not produce it | `plans/round-42-claims.md`; `corpus/evidence/round42/` |
| `lessons/round-42-verifier-spotcheck.md` | Non-author closure spot-check of round 42 | before `d69452cf`, after `f9bbee69` |
| `lessons/round-43.md` | Nine near-variants killed with value-attributed kills and a ninth TB2 grader (`feal-differential-cryptanalysis`, S129–S137); three carried mistakes — a stale-line anchored edit, a freeze control whose own quote was one word, a counter's answer key shipped inside the counter | `plans/round-43-claims.md`; `corpus/evidence/round43/` |
| `lessons/round-43-verifier-spotcheck.md` | Non-author closure spot-check of round 43 | before `317148c4`, after `1838be94` |

---

## Block B — evidence dirs with no index-grade row (new section, insert before `### Round-34 evidence`)

### Round-30 to Round-33 evidence

- `evidence/round30/` — census before/after, the adoption receipt over the six admitted rows (`entries=1 … census=ok`, exit 0), the gate selftest (`SELFTEST cases=14 failed=0`), `rows-opened.tsv` (S081–S086 with `recheck=180d`), the C2 counter receipt (`checks=5 defects=0`), the hardened-counter control and the landing receipt. Its `quote-mode-six-rows.txt` (sha256 `63aa8ced…e847`) is the round's quote-mode run over the six rows: S083 and S085 are `REFUSED … absent`, and its opening `ls: cannot access '/tmp/r30fx-c3cli/cap/…'` lines record that the S081/S082/S084 source captures were absent when it ran (see `corpus/lessons/round-30.md` §Sources opened this round for the row quotes themselves).
- `evidence/round31/` — census and adoption after (`cited_rows=3 … census=ok`), C1 counter (`checks=6 defects=0`), C2 after states (`checks=10 defects=0`), gate selftests, the two quote-mode receipts (plain and `--url-map` bound, `located=7 found=7 overlong=0`), the neutered-gate failure-capability control, and `gate-cli-exits.txt` (regenerated round 32 from the committed C3 fixtures).
- `evidence/round32/` — the C1 counter (`checks=6 defects=0`), the refusing adoption gate (`census=fail`, exit 1 — the S094/S097/S101/S102 refusals), the C2 draft-state receipt (`checks=7 defects=5`, red on purpose), and `catalogs/` with the bounded HF/OpenRouter raw response bodies plus `SHA256SUMS`.
- `evidence/round33/` — census after, adoption after (`checks=8 defects=0`, exit 0), the C2 defect counter (`checks=6 defects=0`), and `catalogs/` (`hf.raw.json`, `or.raw.json`, `after.txt` recording `hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0`, `SHA256SUMS`).

---

## Block C — Round-41 evidence

### Round-41 evidence

- `evidence/round41/tb2-constraints-scheduling/` — the ten pinned `constraints-scheduling` files at terminal-bench-2 `2fd12b88` (`test_outputs.py`, `instruction.md`, `test.sh`, `solve.sh` = the task oracle, `task.toml`, `Dockerfile`, `README.md`, and the three input calendars `alice_calendar.ics`, `bob_calendar.ics`, `carol_calendar.ics`) with `SHA256SUMS`; `test_outputs.py` and `instruction.md` are rows S122, S123, and the three calendars carry the grader's own pinned digests.
- `evidence/round41/constraints-probe.txt` — receipt of `plans/constraints_probe.py` (25 frozen cases, `cases=25 observed_pass=6 observed_fail=19 mismatches=2`, `regrade cases=25 differ=0`); `evidence/round41/constraints-dry-cases-freeze.txt` — the frozen case table (`cases=25 predicted_pass=6 predicted_fail=19`, with `violates=` tags).
- `evidence/round41/pr245-body.md` — the captured TB2.1 PR #245 body for row S124 (`state=closed merged=false closed_at=2026-10-08T19:02:36Z`); its 55-fixture patch is quoted as the PR body's claim, never executed.
- `../plans/battery41/` — fixtures for `plans/round41_c1_verify.py` (`BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=23 killed=23 survived=0`).

## Block D — Round-42 evidence

### Round-42 evidence

- `evidence/round42/tb2-circuit-fibsqrt/` — the nine pinned `circuit-fibsqrt` files (`test_outputs.py`, `instruction.md`, `test.sh`, `solve.sh` = the task oracle, `task.toml`, `Dockerfile`, `README.md`, `sim.c`, and the shipped example `gates.txt`) with `SHA256SUMS`; `test_outputs.py`, `instruction.md` and `sim.c` are rows S125–S127.
- `evidence/round42/fibsqrt-probe.txt` — receipt of `plans/fibsqrt_probe.py` (16 frozen cases, `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0`); `evidence/round42/fibsqrt-dry-cases-freeze.txt` — the frozen case table (`cases=16 predicted_pass=7 predicted_fail=9`).
- `../plans/battery42/` — fixtures for `plans/round42_c1_verify.py` (`BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=14 killed=14 … unattributed=0`, attributed kill rule).

---

## Block E — Round-44 evidence (append at end of file)

### Round-44 evidence

- `evidence/round44/tb2-feal-linear-cryptanalysis/` — the eleven pinned `feal-linear-cryptanalysis` files at terminal-bench-2 `2fd12b88` (`test_outputs.py`, `instruction.md`, `test.sh`, `solve.sh` = the task oracle, `task.toml`, `Dockerfile`, `README.md`, `gen.py` = the generator the image seeds from and deletes (`Dockerfile:11` runs it, `:13-14` `rm orig_plaintexts.txt` / `rm gen.py`), `decrypt.c`, `feal.c` = the agent-visible cipher, and the repository dotfile captured as `gitignore`) + `SHA256SUMS`; fetched by the L1 2026-10-26 20:10:09 -03; rows S138–S146 pin nine of them (`feal.c` and `gitignore` are captures, not rows).
- `evidence/round44/feal-linear-probe.txt` — receipt of `plans/feal_linear_probe.py` (14 frozen cases, `cases=14 observed_pass=8 observed_fail=6 mismatches=0`, `regrade cases=14 differ=0`); `evidence/round44/feal-linear-dry-cases-freeze.txt` — the frozen case table (`cases=14 predicted_pass=8 predicted_fail=6`, with `violates=` tags and the four `TAG` lines that name `instruction.md:7`, `:8`, `:10`).
- `../plans/battery44/` — fixtures for `plans/round44_c1_verify.py` (span- and value-attributed kill rule). **Add this bullet only when the battery lands**: at drafting time `plans/battery44/` does not exist and the frozen claim is still open.

---

## Observation for the L1 (do not paste; route or dismiss)

`corpus/evidence/round30/quote-mode-six-rows.txt` (sha256 `63aa8ced9bb4424e2d1e88f655e2fe226a4d5f076938f0f854d2b5fcb334e847`)
lines 6, 13 and 19 record `artifacts=.git/COMMIT_EDITMSG,.git/FETCH_HEAD,…` — a `.git` directory
listing, not the source captures — and the `ok S081/S082/S084` spans that follow are located at the
lane's own drafts (`.ufo/waves/round-30/build/R30RowSchema.md`, `R30SrcS081.md`, `R30ConnCorpus.md`,
`R30RevEntryQ1Q6.md`), while lines 4, 11 and 17 record `ls: cannot access
'/tmp/r30fx-c3cli/cap/S081|S082|S084/*.html'`. Its S083/S085 lines are `REFUSED … absent` against
pdftotext text, which matches the hyphen/newline limits named on those lines; the row quotes
themselves are recorded with page/line in `corpus/lessons/round-30.md` §Sources opened this round.
Block B's round30 bullet therefore says where the receipt located the spans, without claiming a
source-capture location.

---

VERDICT: index-rows-drafted-43
