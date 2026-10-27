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
