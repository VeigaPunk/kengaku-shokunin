# Round 95 — CriticClaims (seat CriticClaims, leaf, no subagents)

Subject: frozen claims R95-C1 (coverage) and R95-C2 (calibration) at T `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239`
(`plans/round-95-claims.md`, F = `d9cd18a7`). Work done in `--shared` clone
`/fast/scratch/hyaku/kengaku-r95/CriticClaims/lane` (detached at T, removed at end). Receipts:
`.ufo/waves/round-95/w1/CriticClaims/` (`receipts/`, `scripts/`).

## Verdicts

| claim | verdict | one-line reason |
|---|---|---|
| R95-C1 coverage | **verifies-narrowed** | The frozen predicate reproduces (9/9 legs, 39 rows, 105 legs, 0 mismatches, rc 0). The replayed `/app/bottle.py` is byte-identical to the image's. But the replay measures the six `test_outputs.py` functions, not the harness reward: two of the claim's "decisive grader findings" (C11, C15) are reward 0 in the real image, and the replay misses two reward-1 states that need no fix. |
| R95-C2 calibration | **verifies-narrowed** | The 14→0 count reproduces (census rc 0; round-94 counter 14/14 passing, rc 1). It is in-sample fixture-fitting, which the claim declares. It is not calibration: two held-out false gates pass the round-95 counter 5/5 legs, and a behaviour-preserving rename turns the counter RED. |

No defect found flips the frozen predicate of either claim. Two frozen *readings* fail: C11/C15 as grader
findings (C1), and "calibration" as discrimination of unseen forgeries (C2). Both are stated plainly below.

## Measured receipts (exact commands; all run at T unless stated)

Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane && git -C $S/lane checkout -q --detach afe9c229…`

### R95-C1

1. Predicate at T — `python3 $S/lane/plans/round95_c1_replay.py --lane $S/lane --rev afe9c229… --work $S/c1work`
   → `LEGS L1=pass … L9=pass`, `TARGET executed_rows=39 member=fix-code-vulnerability located=1 executed=1 cases=15 legs=105 mismatches=0 defects=0`, `PREDICATE R95-C1 pass`, rc 0. (`receipts/c1/c1-predicate-T.txt`)
2. Do-nothing at BASE `4524072d` — same command, `--rev 4524072d…` → all nine legs fail, `DEFECT L1 receipt absent`, rc 1. (`receipts/c1/c1-base-check.txt`) Note: this control is reachable only by producing artifacts; L6 re-runs the probe from `git archive`, so a hand-written receipt cannot pass.
3. Image identity. `docker pull alexgshaw/fix-code-vulnerability:20251031` (digest `sha256:cac32525…dac5c0`, created 2025-10-28; S309's "rejected" input was pullable — the flip it names was performed here).
   - `/app/bottle.py` in image: `761756ce31753e526c48d28ccbca13a5d2493b16fe37aff3e1e4d2efaf3a2bba` = `VULNERABLE_BOTTLE_SHA` in the receipt. **Replay's rebuilt /app file matches the image byte for byte.**
   - Image `/app` is a git repo at `0207a34f`; `git -C /app show HEAD:bottle.py` = `abf6…802` (= captured upstream). `git status`: ` M bottle.py`. Objects were not pruned.
   - `/usr/local/lib/python3.11/site-packages/bottle.py` = `abf6…802`, version 0.14.dev0 (installed by `RUN pip install .`, which runs **before** the sed deletions).
   - Image Python 3.11.14; probe host Python 3.14.8 (`/usr/bin/python3 -V`).
4. Six-function vectors vs image. Real `tests/test.sh` run in the image (`receipts/real-harness/`), ctrf per-test status compared with the replay's predicted vector:
   - do-nothing (C02 `vulnerable/absent`): F,E:FNF,E:FNF,P,F,P — matches.
   - solve.sh (C01): all six P — matches; real reward **1** (original suite 367/367 + 6/6).
   - hkey-only (C11): six P — matches the six functions; **real reward 0** (`original-repo-ctrf.json`: `test/test_environ.py::TestResponse::test_prevent_control_characters_in_headers` FAILED).
   - shadow (C15 `package-shadow`): six P — matches the six functions; **real reward 0**: `collected 0 items / 25 errors`, `ImportError: cannot import name 'tob' from 'bottle' (/app/bottle/__init__.py)` in `test/*.py`.
   - Reward is `reward.txt` = 1 only if `ORIGINAL_EXIT_CODE==0 && ADDITIONAL_EXIT_CODE==0` (`tests/test.sh` lines 12–21). The original suite (`/app/test`, 367 tests) is the un-replayed half.
5. Reward holes the 15-case table cannot reach (real harness, same image; no fix applied):
   - `delete-bottle`: `rm /app/bottle.py && echo '{"file_path": "/app/bottle.py", "cwe_id": ["cwe-93"]}' > /app/report.jsonl && bash /tests/test.sh` → **reward 1**, 367/367 original and 6/6 functions pass. Mechanism: `import bottle` falls back to `/usr/local/lib/python3.11/site-packages/bottle.py` (the full oracle). Host has no `bottle` (`/usr/bin/python3 -I -c 'import bottle'` → `ModuleNotFoundError`), so the replay cannot model this state; it would show `E:ImportError`.
   - `restore-git`: `git -C /app checkout -q -- bottle.py && <report> && bash /tests/test.sh` → **reward 1**. The Dockerfile's sed deletions do not remove the oracle; `.git` HEAD holds it.
   - Neither state is in the frozen table, so neither flips the predicate.

### R95-C1 — attack reading

- *Is the replay a measurement a do-nothing cannot reach?* At the artifact level, yes (c1-base: L1–L9 fail). At the behaviour level, the predicate measures grader behaviour on 15 predicted cases; it does not require the agent's `/app` to pass. C02 (the do-nothing vector) is a *matching* prediction, i.e., the predicate is satisfied by a grader that fails. That is correct for a replay but means "coverage" is not "the grader accepts the work".
- *Is "located offline replay" honest?* In the lane's ledger sense (R79: the receipt's own bytes name the member; `located=1`), yes. Read as "replay of the harness" it is not: the harness runs a prebuilt image (`task.toml:29`), and the reward depends on the original suite (`tests/test.sh:12`), which the replay does not stage. The file-level replay is faithful to the image (item 3); the reward-level replay is not.
- *Are C11/C15 overclaimed as grader findings?* **Yes.** Each is a six-function pass that the real grader scores 0 (item 4). They are findings about `test_outputs.py`'s coverage (no test calls `_hval`; the package shadow is imported), not about the grader's verdict. The claim's word "decisive" for them is refuted at the reward level.
- *Does S308's rejection of the un-staged suite matter?* Yes, for C11 and C15 it flips the reward. The rejection is correct as a replay-input decision and wrong as a coverage statement.

### R95-C2

1. Census at T — `python3 $S/lane/plans/round95_false_gate_census.py --lane $S/lane --rev afe9c229… --work $S/census-T` → 14 `GATE … passes=0 designated_red=1`, `HONEST rc=0 predicate=pass`, `FALSEGATES total=14 passing=0 designated_red=14 honest=pass`, `PREDICATE R95-C2 pass`, rc 0. (`receipts/c2/census-T.txt`, per-gate outputs in `receipts/c2/census-T-gate-outputs/`)
2. Do-nothing: `… --counter $S/lane/plans/round94_c2_counter.py` → `FALSEGATES total=14 passing=14 designated_red=0 honest=pass`, `PREDICATE R95-C2 fail`, rc 1. (`receipts/c2/census-r94counter.txt`) Reproduces the P2 control. The target is not reached without work.
3. Honest gate on T: `python3 $S/lane/plans/round94_c2_counter.py --lane $S/lane --rev afe9c229…` → `PREDICATE R94-C2 pass`, rc 0 (legacy gate still green; `receipts/legacy/round94-c2-counter-at-T.txt`).
4. In-sample construction. The counter's own docstring and code: W2 fixtures `w2-paths-dup`, `w2-paths-absent`, `w2-octopus`, `w2-delete-readd`, `w2-rename`, `w2-spaced-row`, `w2-unterminated` and the W3 probes P1–P3 map one-to-one onto the designated legs of the 14 rows (`DESIGNATED` in the census). They were written after the 14 bytes were recorded. The 14→0 result is therefore a regression count over that population; it says nothing about gates outside it. The claim says so (`Scope`, in-sample); the claim's name "calibration" does not.
5. Held-out forgeries (not in the tsv; built by me from gate v2 bytes; `receipts/forgeries/`). Each scored by the round-95 counter with `--tool-file` (`python3 -I -B $S/lane/plans/round95_c2_counter.py --lane $S/lane --rev afe9c229… --work $S/ho/w-HO-X --tool-file HO-X.py`) and by the honest gate directly (`verify-hold-A-B-C.txt`).

   | id | mutation (gate v2 bytes) | honest gate on the fixture | round-95 counter | verdict |
   |---|---|---|---|---|
   | HO-A | table rows starting `#` are skipped | `could-not-evaluate` rc 2 (malformed row) | **PASS 5/5 legs, rc 0** | **false gate, survives** |
   | HO-B | `touched = 0` in paths mode | `broken:touched-after-freeze=2` rc 1 | **PASS 5/5 legs, rc 0** | **false gate, survives** |
   | HO-C | `--max-count=50` on the history walk | `broken:touched-after-freeze=2` rc 1 | PASS 5/5 legs | equivalent (see below), harmless |
   | HO-D | last claims row dropped when ≥2 rows | — | RED at W1b (`summary=(8,8,0)` vs 9) | caught, incidentally (round-93 count) |
   | HO-E | `--full-history` → `--first-parent` | — | RED at W2 (`w2-intact`, `w2-treesame-merge`, `w2-octopus`) | caught by W2 |

   Exact fixture for HO-A (claims mode): `probe.py` live row + `# <sha of notes.md>  notes.md` commented row; edit `notes.md`; honest → `DEFECT SETUP malformed table row '# 444e…'`, rc 2; HO-A → `INSTRUMENT probe.py … verdict=intact`, `PREDICATE freeze-integrity pass`, rc 0. The breached instrument is hidden behind comment syntax.
   Exact fixture for HO-B (paths mode): commit `probe.py`; edit to `return 4`, commit; revert to `return 3`, commit; `--paths probe.py`. Honest → `touched=2 verdict=broken:touched-after-freeze=2` rc 1; HO-B → `touched=0 verdict=intact` rc 0. The round-92 history leg (W1a) passes because its three breaks are byte breaks; no fixture has an edit-then-revert in paths mode.
   HO-C is equivalent: `git rev-list --max-count=N -- <path>` limits the number of *path-matching* commits printed; the verdict flips only if zero commits match, and `touched ≥ 1` already means broken. It changes only the count in the reason text. Verified by the 60-commit fixture (both rc 1, `touched=2`).

6. Honest-equivalent controls (behaviour-preserving edits of gate v2):
   - HE1 comment line added after `from __future__`: counter **PASS 5/5 legs**, rc 0 (`ho/out-HE1-comment-only.txt`).
   - HE2 local variable `touched` renamed to `touch_count` (4 sites): counter **FAIL**, `W3 P2-touched-threshold-2 RED anchor-missing`, `W3 fail`, `PREDICATE R95-C2 fail`, rc 1 (`ho/out-HE2-local-rename.txt`). W3 probes are text anchors into the tool under test (`BATTERY_PROBES`); a rename removes the anchor and the counter reports RED. Likewise W5 `MUTANTS` anchors. The "passes the unchanged honest gate" statement holds for exact bytes only.
7. Designated-leg check. The census accepts `W3 fail` as "designated" for the four battery rows. I confirmed these reds come from the probes running green (`W3 P1 RED rc=0 selftest=['cases=15 ok=15'] predicate=['pass']`), not from anchors, so the 14 are not artefacts of anchor loss. The W3 check is a regex on `^W3 fail `, which any W3 failure satisfies; the census does not look at which probe failed.
8. W5 "killed 10/10" is by construction: each of the ten CLI mutants has a designated fixture written alongside it. Not a held-out measure. I did not run a counter-mutant census (load average ~96 on the host; the census alone took ~20 min under load).
9. [INFERENCE, not run] The census does not exercise W1, W4 or W5 at all beyond honest pass; a counter with W1 removed would still score 14→0. W4 passes trivially on the current table (11 instruments, broken 0), so it cannot detect a breach here.

### Legacy / harm gates

- `plans/round79_c1_population_ledger.py --lane $S/lane --rev 4524072d…` → `DEFECTS n=14` (incl. `CLASS-K-MISMATCH` for `filesystem-metadata`, `git-plumbing`, `serialization-schema`), `PREDICATE R79-C1 fail`, rc 1 (`receipts/legacy/round79-ledger-at-BASE.txt`).
- Same at T → `DEFECTS n=0`, `replayed=39 located=39`, `PREDICATE R79-C1 pass`, rc 0 (`receipts/legacy/round79-ledger-at-T.txt`). Round 95 repairs a BASE-failing legacy gate; no harm observed.
- The round-87 row `mteb-retrieve`: `subject` changed `tb2-result-file` → `tb2-header`. The receipt's first line is `# tb2 mteb-retrieve grader probe`, which is the tb2-header shape. The old value was the stale one. Consistent with the receipt, not harm.
- Not run: `round94_c1_replay.py` at T (reads the ledger row for `write-compressor`; that row changed only legacy fields in this round, per `git diff 4524072d afe9c229 -- plans/grader-population-ledger.json`).

### Sources (S303–S309)

Re-fetched all seven from `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/fix-code-vulnerability/…` and `bottlepy/bottle/0207a34f…/bottle.py`: HTTP 200, sha256 equal to the S-rows, and byte-identical to the lane captures (`cmp`). Line anchors checked: `test_outputs.py:45`, `solve.sh:20`, `Dockerfile:22`, `bottle.py:1562`, `instruction.md:18`, `test.sh:9`, `test.sh:12`, `task.toml:29` all match the quoted text. S305's oracle-line claim is accurate (the sed sequence removes original 1562–1563 and 1569–1570).

### Overlap

- C1 and C2 separable as claimed: C1 reads the frozen table (L4/L8) and no C2 file; C2 W4 reads the same table. No shared mutable state.
- In-sample overlap in C2: 12 of the 20 W2 fixtures are the round-94 set; 8 are the 14-row designated legs (see item C2.4).
- Class overlap: `vulnerable-secret` (round 81, file-artifact, tb2-header) is a different grader; no shared probe.

## Findings

FINDING C1-REWARD-DIVERGE major — the frozen reading of C11 and C15 as grader findings fails at reward level. Real image: `hkey-only` (solve.sh minus the `_hval` sed) → reward 0 via `test/test_environ.py::…test_prevent_control_characters_in_headers`; `shadow` (`/app/bottle/__init__.py` raising `_hkey`) → reward 0 via collection `ImportError`. The replay's six-function vector agrees with the image in both cases. Route to round 96: the replay should either stage the original suite or state that it measures the six functions only.

FINDING C1-REWARD-DELETE major — `rm /app/bottle.py` plus a one-line report → reward 1 in the image (`/usr/local/lib/python3.11/site-packages/bottle.py` is the full oracle, installed before the sed step). Not in the 15 cases; does not flip the frozen predicate. The replay's `/usr` has no site-packages bottle, so the replay cannot model this state. Route to round 96.

FINDING C1-REWARD-GIT major — `git -C /app checkout -- bottle.py` → reward 1. `.git` HEAD in the image retains the oracle (reflog expired, objects not pruned), so the Dockerfile's sed is not oracle removal. Does not flip the frozen predicate. Route to round 96.

FINDING C2-HELDOUT-FALSEGATE major — HO-A (commented-out claims row hides an edited instrument) and HO-B (paths-mode skips the history check) both pass the round-95 counter 5/5 legs (rc 0) while the honest gate reports rc 2 / rc 1 on the same fixtures (`receipts/forgeries/verify-hold-A-B-C.txt`). The frozen in-sample predicate still passes; the calibration reading does not survive held-out forgeries. Route to round 96 with W2 fixtures for both.

FINDING C2-RENAME-FALSERED major — renaming a local variable in gate v2 (`touched`→`touch_count`, behaviour-identical) turns the round-95 counter RED: `W3 P2-touched-threshold-2 RED anchor-missing`, rc 1. The counter is coupled to source text through W3/W5 anchors. Route to round 96.

FINDING C2-HO-C-EQUIV info — `--max-count` on a path-limited walk is verdict-equivalent (changes only the count). Survives the counter; harmless.

FINDING GLOB-PATHSPEC info — tested `probe[1].py` edit-then-revert on the honest gate: `broken:touched-after-freeze=2` (`receipts/forgeries/glob-pathspec-honest-gate.txt`). No pathspec defect; the hypothesis is refuted.

FINDING CENSUS-14-0 info — reproduced: `FALSEGATES total=14 passing=0 designated_red=14 honest=pass`, `PREDICATE R95-C2 pass`, rc 0. Do-nothing with the r94 counter: `passing=14 designated_red=0 honest=pass`, rc 1.

FINDING LEGACY-R79 info — round79 gate 14 defects at BASE → 0 at T, pass rc 0. R94-C2 at T pass rc 0. No harm observed.

FINDING SOURCES-S303-S309 info — all seven re-fetched and byte-identical; S309's flip condition met (image pulled, /app/bottle.py sha matches VULNERABLE_BOTTLE_SHA).

FINDING PY-FIDELITY minor — probe host Python 3.14.8 vs image Python 3.11.14. The six-function vectors matched the image for the four variants checked; not checked for the rest.

FINDING C1-VERDICT info — R95-C1 verifies-narrowed (predicate reproduces; scope = six functions on byte-identical /app/bottle.py, not the harness reward).
FINDING C2-VERDICT info — R95-C2 verifies-narrowed (14→0 reproduces as an in-sample regression count; not calibration).

## Installs and host state (recorded)

- `docker pull alexgshaw/fix-code-vulnerability:20251031` — image retained in the local daemon (~695 MB, digest `sha256:cac325252991f823713b2d0441502972901dd782bd67f66c03d9b1e410dac5c0`). Channel: Docker Hub, official tag, read-only use. Reason: the S309 flip. Not removed; `docker rmi` available if the fleet wants the space back.
- No tool installs, no host sysctl changes, no fleet-root writes, no lane writes, no git mutation in the lane.
- Docker containers were `--rm`; their volumes lived under the scratch dir, which I removed.

## Commands to reproduce (absolute paths; from any seat)

```
S=/fast/scratch/hyaku/kengaku-r95/CriticClaims; T=afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane" && git -C "$S/lane" checkout -q --detach $T
python3 "$S/lane/plans/round95_c1_replay.py" --lane "$S/lane" --rev $T --work "$S/c1work"
python3 "$S/lane/plans/round95_false_gate_census.py" --lane "$S/lane" --rev $T --work "$S/census-T"
python3 "$S/lane/plans/round95_c2_counter.py" --lane "$S/lane" --rev $T --work "$S/ho/w" --tool-file HO-A-comment-row-skipped.py
docker pull alexgshaw/fix-code-vulnerability:20251031
bash .ufo/waves/round-95/w1/CriticClaims/scripts/drive.sh          # six real-harness scenarios (needs $S/tests, $S/cases)
bash .ufo/waves/round-95/w1/CriticClaims/scripts/verify-hold.sh    # HO-A/HO-B/HO-C fixtures vs honest gate
```

Receipts: `.ufo/waves/round-95/w1/CriticClaims/receipts/{c1,c2,real-harness,forgeries,legacy}/`. Scripts: `.ufo/waves/round-95/w1/CriticClaims/scripts/`.
