author: hyaku closure (non-author integrator, @m_opus)
round: 44
lane: kengaku
date: 2026-10-26
role: non-author integrator of record (closure)

# Round 44 — non-author verifier spot-check

## 1. Conformance (step 1)

- Report committed by lane identity: `git log --format='%an %ae' -- .ufo/reports/round-44/kengaku.md`
  → `kengaku-shokunin <kengaku@shokunin.local>` (commit `e7b06154`). ✔
- SHONEN heading present with 4 box lines (one per box). ✔
- Every cited lane commit exists and is an ancestor of `master`
  (`git merge-base --is-ancestor <hash> master` — 0cb2e225, 5f16ed04, 45dc0bc8, 5e3d3aa0,
  2a263e5a, 256cc66a, 02287eed, c2ff2114, 7857ce55 all `anc`). ✔
- Lane state `scripts/hyaku/jj-lane.sh state` → `ahead=0 behind=0 tracked=0 untracked=0`; `git status
  --porcelain` empty; `git ls-remote origin refs/heads/master` = `7857ce55…` (matches final lane hash). ✔
- Dispatched prompt carries the canonical `templates/round-prompt.md` contract: every non-placeholder
  template line present, no missing placeholders (diff of templates clean). ✔
- Notes: report committed 21:11:07 -03 cites final hash `7857ce55` (committed 21:19:02 +03);
  `e7b06154` (report) is an ancestor of `7857ce55`. Conformance defect: none. Marker check passed (real
  work, commits, measurement).

## 2. Claims re-check (step 2)

### C1 — calibration (five advertised behaviours of two gate tools) — evidence-verified
Owned by lane gate `plans/round44_c1_verify.py`; per PROTOCOL §Gate standard (Closure consequence) the
committed evidence was verified, not the sibling's gate executed.

Plain measurement over committed bytes (rebased against `7857ce55`):
- `plans/battery44/` = 10 modules at HEAD.
- `plans/anchor_digest_check.py` and `plans/order_check.py` unchanged between `0cb2e225` and
  `7857ce55` (`git diff --stat` empty) — tools unedited.
- `plans/round44_c1_verify.py` / `plans/round44_c2_verify.py` unchanged between freeze `5f16ed04` and
  `7857ce55` — frozen counters.
- Advertised labels present in tool sources: `digest-short` (2 hits), `digest-long` (2), worktree read
  (`:107`), `exit 2` setup-error branch (`order_check.py:26-27,41`).
- Committed evidence `.ufo/waves/round-44/integrate/measure-final.txt` (at `02287eed`) and
  `measure-tip.txt` (at `c2ff2114`): before `BATTERY fixtures=0`, `MUTANTS total=5 killed=0 survived=5`,
  `PREDICATE C1 fail`, exit 1 → after `fixtures=33 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=5
  killed=5 survived=0 invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=4/4 order=1/1`,
  `PINS total=2 mismatched=0`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, exit 0.
- Controls committed red-before: `control-c1-nothing.txt` (`killed=0 survived=5`, exit 1),
  `control-c1-standing-batteries.txt`, hostile f1–f6, witness, tool-edited etc.

Reported values match the committed evidence exactly. Verdict: calibration axis result **agrees**;
5/5 kills attributed (value=differs), 0 survivors, 0 unattributed.

### C2 — coverage (tenth TB2 grader, F1 constant-compare class) — re-measured + evidence-verified
Plain measurements over committed bytes (mine, against `7857ce55`):
- `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md` exists with `source:` S138–S146,
  `verified-at: 2026-10-26`, `recheck: 180d` trio, and a `## Located quotes` section.
- SOURCES row count (grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|') 130 → 141; rows
  S138–S146 present tier A, S147/S148 tier B; knowledge files 50 → 51.
- Captures `corpus/evidence/round44/tb2-feal-linear-cryptanalysis/`: 12 entries incl. SHA256SUMS
  (11 captured files). Spot sha256 checks on captures match the SOURCES row digests for S138–S146.
- Probe receipt `corpus/evidence/round44/feal-linear-probe.txt`: 14 `CASE` rows,
  `cases=14 observed_pass=8 observed_fail=6 mismatches=0`, `regrade cases=14 differ=0`.
- Evidence-verified (gate standard): measure-final/measure-tip C2 leg — `V1 ok listed=11 bad=0`,
  gates P1–P10 all `ok`, `V4 ok cases=14 mismatches_named=0/0`, `V5 ok probe=frozen dry_byte_equal=True`,
  `V8 ok order_exit=0 result=PASS`, `V11 ok states=48 grader_pass=24 grader_fail=24 disagree=0`,
  `checks=11 defects=0`, `PREDICATE C2 pass`, exit 0. Baseline red: `checks=11 defects=8` exit 1.
- `round_close --round 44` PASS (measure-final).

Reported count transitions match. Verdict: coverage result **agrees** (new executed grader class,
9 tier-A + 2 tier-B rows, frontier 10/89).

### No-harm
`git diff 0cb2e225 7857ce55 -- SCORECARD.md` adds only the round-44 section; no axis score changed.
`round_close` r41/r42/r43 PASS in measure-final; rounds 36–43 counters byte-equal, tip receipts, five
probes byte-equal, frozen digests r39–r44 OK. No axis harmed.

### Axis grades (table)
| axis | verdict |
|---|---|
| expansion | improved (knowledge 50→51; SOURCES 130→141; frontier TB2 10/89; C2 verified) |
| quality | unprovable-but-better (C1 5/5 kills verified; limits acknowledged: fence bypasses V1–V3, memorizable V11) |
| discernment | improved (spot-check below agrees with all sampled admit/reject; flip-verdict check red→green) |

## 3. Discernment spot-check (step 3)

Samples from `corpus/lessons/round-44.md` §Gate; sources re-opened at the pin `2fd12b88` (raw
githubusercontent for the pinned commit, and captured paths in the lane).

### Admits (re-opened: captured files at cited lines + sha256)
| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S138 `tests/test_outputs.py` | admit (mined, A) | capture `test_outputs.py:122` = `assert c in data` (4 words); sha256 f59ebc72… matches row | **agree** | quote verbatim at the cited line, ≤25 words, digest leaves the pin |
| S139 `instruction.md` | admit (mined, A) | capture `instruction.md:7` = "Implement a known-plaintext attack that recovers the key of the cipher." (11 words); sha256 a2f1669d… matches | **agree** | verbatim, located, ≤25 words |
| S140 `environment/task-deps/gen.py` | admit (mined, A) | capture `gen.py:12` = `keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]` (6 words); sha256 3a71f0b5… matches | **agree** | verbatim; curly delimiters justified (line carries straight quotes); digest matches |
| S141 `environment/Dockerfile` | admit (mined, A) | capture `Dockerfile:14` = `RUN rm gen.py` (3 words); sha256 ef521cded1… matches | **agree** | verbatim, located, ≤25 words |
| S142 `tests/test.sh` | admit (mined, A) | capture `test.sh:26` = `echo 1 > /logs/verifier/reward.txt` (4 words); sha256 9431cbc2… matches | **agree** | verbatim |
| S143 `README.md` | admit (mined, A) | capture `README.md:32` = "verifies that all 100 expected plaintext values appear in" (9 words); sha256 a038645f… matches | **agree** | verbatim (line continues but quote is ≤25 words) |
| S144 `solution/solve.sh` | admit (mined, A) | capture `solve.sh:304` = `./attack > /app/plaintexts.txt` (3 words); sha256 be50ae01… matches | **agree** | verbatim |
| S145 `environment/task-deps/decrypt.c` | admit (mined, A) | capture `decrypt.c:136` = `printf("%lu\n", plaintext);` (2 words); sha256 4c6864e0… matches | **agree** | verbatim; curly delimiters as S140 |
| S146 `task.toml` | admit (mined, A) | capture `task.toml:34` = `allow_internet = true` (3 words); sha256 a39ec2c4… matches | **agree** | verbatim |

### Rejects (re-opened: upstream at pin + entry citation scan)
| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `feal.c` | REJECT (captured, not a row) | upstream `…/feal-linear-cryptanalysis/environment/task-deps/feal.c` re-fetched: HTTP 200, 3472 B, sha256 bbd38d19… = captured. Entry body outside `## Located quotes` has no `feal.c:<line>` citation without S1xx co-citation (grep: none) | **agree** | captured and contentful, but carries no graded predicate; reject correct and flip condition clean |
| `gitignore` | REJECT (captured, not a row) | upstream `.gitignore` re-fetched: HTTP 200, 177 B, sha256 9a8dd8d9… = captured dotless file; the dotless spelling `gitignore` → HTTP 404 | **agree** | upstream path is `.gitignore`; capture keeps dotless name; repo hygiene only, no graded content; reject correct |
| `SHA256SUMS` | REJECT (inventory, not content) | manifest of the captures; entry never cites it | **agree** | contentless as evidence; reject correct |

### Newly written SOURCES row quote check
S138 quote "assert c in data" (4 words ≤25) verified verbatim at the cited capture line `test_outputs.py:122`; digest matches the row's pinned sha256.

### Census
`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0, `kengaku ok`,
15 W04 (all pre-existing duplicates), 0 E-codes — matches the report's after-census.

## 4. Routed defects the lane must fix next round

- `R44SentinelFences` V1–V3 remain open (commondir object-store delegate, second-config include,
  refuse-to-describe) — fence bypasses 3/6; none used by battery44 but the counter's fence goal is
  incomplete.
- `R44LabratLaneInclude` — `lane_breach` reads an include outside d in the parent process.
- `R44CritV11` — V11 fixed-seed sample is memorizable (4/7 lookup predictors pass); landed predictor is a
  substring reading; strengthen the held-out sample or freeze a non-memorizable seed scheme.
- Round-43 false `not fired` flip-line defect corrected this round (flip-verdict check red→green); keep
  the new check in the gate path.

## 5. Verdict

CLOSURE kengaku r44 status=ok admitted=true
