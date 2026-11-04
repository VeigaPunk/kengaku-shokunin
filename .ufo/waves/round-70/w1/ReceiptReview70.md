# ReceiptReview70 — adversarial review of the frozen R70-C1 `--check-receipt` (round 70, wave w1)

Scope: review only. The instrument (`plans/round70_c1_nginx_probe.py`, committed blob sha
`9aef6d33abc965f52a965b2f9197b78d257dc76003ddc124ca0e692a4fdbbe90`) and every predicate,
case table, vector, digest, kill rule and target were **not edited**. All forgeries and
fixtures live under `/fast/scratch/hyaku/kengaku-r70/ReceiptReview70/`; the only lane-side
write is this report. No tools were installed (none needed); pacman untouched.

## 0. Ground truth (verified before forging)

- Lane tip `git rev-parse master` = `384e9c76415e78093623b3eaff262423a89dbc3e`;
  `git cat-file blob master:plans/round70_c1_nginx_probe.py | sha256sum` =
  `9aef6d33…` = working-tree sha. The instrument is committed and unmodified since freeze,
  so the `PROBE_BLOB` arm binds.
- Grader bytes `045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0` =
  `GRADER_SHA256` constant = `corpus/evidence/round52/graders/SHA256SUMS:111`
  (`045cc716…  ./nginx-request-logging/tests/test_outputs.py`).
- `python3 plans/round70_c1_nginx_probe.py --check-receipt corpus/evidence/round70/nginx/receipt.txt`
  → rc 0, `CHECK ok cases=7 legs=8 seen_p=8 seen_f=8` / `PREDICATE R70-C1 pass` (genuine
  receipt accepted).
- `--render-table` → rc 0; table, `FROZEN-VECTOR PPPPPPPP/PPFPPPPP/PPPPPPFF/PPPPPFPP/FPPPFPPP/PFFFPPFF/PPPFPPPP`,
  `LEG-COVERAGE-FROZEN legs=8 seen_p=8 seen_f=8` and per-leg counts (installed p=6 f=1 …
  log_format p=5 f=2) byte-match the claims doc's frozen table.
- `--selftest --work $S/selftest` → rc 0: `SELFTEST red_refused=7/7 green_ok=0 accept_ok=1 ok=True`,
  `PATH-INDEPENDENT sha_equal=True`, `STAGED-STATE changes_on_byte=True`.

## 1. Clause map — frozen sentence → enforcing code (path:line)

Frozen sentence (plans/round-70-claims.md, R70-C1): *"Each of the seven frozen cases yields
its frozen eight-leg vector, every one of the eight grader legs is observed `P` in at least
one case and `F` in at least one case, each case line's `case_sha256` equals its frozen
staged-input digest, and the receipt's PROBE, PROBE_BLOB and GRADER sha256 equal the
committed bytes; the counter then prints `PREDICATE R70-C1 pass` and exits 0."*

| # | Clause | Enforcing code (`plans/round70_c1_nginx_probe.py`) |
|---|---|---|
| 1a | exactly the seven frozen cases | `case-set` :663 (sorted id-set equality against `CASES`); extra/dropped case refused |
| 1b | VECTOR line well-formed | :638–641 (6 tokens, `expected` at [3], `agree=` at [5]) |
| 1c | expected-field consistency | :642–643 |
| 1d | vector equals the case's frozen vector | :683–684 (`vector-mismatch`) |
| 1e | `agree=True` | :685–686 (`vector-agree`) |
| 1f | TEST leg set equals the 8 legs | :688–689 (`leg-set`) |
| 1g | vector re-derived from TEST lines | :690–692 (`leg-vector`) |
| 2 | every leg P in ≥1 case and F in ≥1 case | tallies :694–700 (exact `"P"`/`"F"` only; anything else → `leg-missing` :698–699), `leg-coverage` :701–702 |
| 3 | each CASE line's `case_sha256` = frozen digest | line shape :654–658; per-id equality vs frozen `CASE_SHA` :668–674 (`case-sha-missing` :672, `case-sha` :674); empty-table guard :665–666 |
| 4a | PROBE sha = committed bytes | :594–601 vs `own_sha256()` :296–297 (working tree), tied to the blob by 4c |
| 4b | PROBE_BLOB = committed blob | :602–615 vs `probe_blob_sha(lane_root())` :304–318 (`git cat-file blob master:…`) **and** vs working tree :613–615 (`probe-blob-working-tree`) |
| 4c | GRADER sha = committed bytes | line-vs-constant + pin :616–624; lane grader file re-hashed :626–632 |
| 5 | prints `PREDICATE R70-C1 pass`, exits 0 | stored line once, ends `" pass"` :705–710; SUMMARY once with `mismatches=0`+`setup=0` :703–705; verdict `derived_ok = not defects` :711; print/exit :719–720 |

No clause is implemented only in prose. Clause 3 is checkable offline only against the
frozen constant (the staged dir is ephemeral) — that trust boundary is the claims doc's own
named limitation (iv), and its re-derivable arms are exercised by `--selftest`
(PATH-INDEPENDENT / STAGED-STATE, both True today).

## 2. Forgery census (base = the genuine receipt; checker = the committed lane instrument)

Refused — rc 1, defect(s) that fired:

| family | mutation | defect |
|---|---|---|
| a1 | flip K1 leg 3 in TEST only | `leg-vector K1 legs=PPFPPPPP vector=PPPPPPPP` |
| a2 | flip K1 VECTOR only | `vector-expected-field` + `vector-mismatch K1 FPPPPPPP != PPPPPPPP` + `leg-vector` |
| a3 | flip K1 leg 1 in TEST **and** VECTOR (consistent) | `vector-mismatch K1 FPPPPPPP != PPPPPPPP` (frozen vector is the anchor) |
| b | drop the whole K6 case | `case-set` (6 of 7) + `case-sha-missing K6` + `leg-coverage test_nginx_running p=6 f=0` — K6 is leg 2's only F witness, so both clauses bite |
| c2 | K7 carries K1's frozen digest (clean line) | `case-sha K7 0cf77ab8… != 07eb2fd3…` |
| d1 | `agree=true` (6 tokens) | `vector-agree K1 agree=true` |
| d2 | 5-token VECTOR | `vector-line` + `case-set` |
| d3 | fields swapped, 6 tokens | `vector-line` + `case-set` |
| d4 | bogus vector `XXXXXXXX`, 6 tokens | `vector-expected-field` + `vector-mismatch` + `leg-vector` |
| e1 | two PROBE_BLOB lines | `probe-blob-line n=2` |
| e2 | PROBE_BLOB split across two lines | `probe-blob 9aef6d33 != 9aef6d33abc9…` + `probe-blob-working-tree` |
| f4 | TEST outcome `MISSING` | `leg-missing K5 test_nginx_installed` + `leg-coverage … f=0` |
| f5 | duplicate TEST line flipped | `leg-vector K1 legs=FPPPPPPP vector=PPPPPPPP` |
| f6 | stored `PREDICATE R70-C1 fail` | `stored-predicate` (a failed live run cannot be laundered) |
| f7 / f8 | SUMMARY dropped / `mismatches=1` | `summary` |
| f10 | swap whole K2↔K7 blocks | `case-sha` ×2 + `vector-mismatch` ×2 (per-id frozen digests block relabeling) |
| f11 | PROBE sha zeroed | `probe-sha` |
| f12 | PROBE_BLOB line absent | `probe-blob-line n=0` |
| f13 | `pin` removed | `grader-pin` |
| f14 | extra case K8 | `case-set` (8 vs 7) |

Accepted — the families a forger still passes:

- **A-1 (LOW) duplicate lines resolve last-write-wins.** `vectors[parts[1]] =` :644 and
  `case_shas[parts[1]] =` :659 overwrite silently; `legs.setdefault(...)` :650 likewise.
  A receipt carrying a contradictory but internally well-formed extra `VECTOR K1 FPPPPPPP
  expected FPPPPPPP agree=True` **before** the correct line is accepted with zero defects
  (`f2b_dup_vector_consistent_bad.txt`, rc 0); same for a duplicate `CASE K1 case_sha256=000…0`
  line (`f3_dup_case_conflict_last_wins.txt`, rc 0); a byte-identical duplicate VECTOR is
  also accepted (`f1`, benign). Under the frozen sentence such a receipt does *not* satisfy
  "each case line's `case_sha256` equals its frozen digest" — one of its lines does not —
  yet the checker passes it. Strictness gap only: the committed writer (`run_battery`
  :546–567) emits exactly one CASE / eight TEST / one VECTOR per case, and no accepted
  forgery changes the verdict of a single-occurrence receipt. Suggested (not applied): a
  `duplicate-line` defect branch on repeated `CASE <id>`/`VECTOR <id>`.
- **A-2 (LOW, latent) absent-blob arm leaves PROBE_BLOB unbound.** :607–611: if
  `master:plans/round70_c1_nginx_probe.py` is absent, the checker prints
  `CHECK probe-blob=absent (uncommitted instrument)` and skips both blob defects.
  Demonstrated in a scratch fixture (`fakelane-uncommitted`: grader committed, probe
  untracked): the genuine receipt passes rc 0 with the blob clause unverified. Dormant in
  this lane (probe committed at master, blob == working tree, verified above).
- **A-3 (INFO) receipt-side PORT / LEG-COVERAGE / PROBE_VERSION / `server_pid` /
  `sandbox_rc` are never validated.** A receipt with the PORT line dropped and
  `LEG-COVERAGE legs=8 seen_p=0 seen_f=0` forged is accepted (`f9`, rc 0) — those lines
  have no defect branch; coverage is instead re-derived from TEST lines, so the forged
  line is ignored rather than believed, and the printed `CHECK ok … seen_p=8 seen_f=8`
  comes from the checker's own tally. `server_pid`/`sandbox_rc` unchecked is exactly the
  claims doc's named limitation (i) (live witness is the committed sandbox captures).
- **A-4 (INFO) SUMMARY token counts are substring-checked only** (:703–705: `mismatches=0`,
  `setup=0` anywhere in the line); backstopped by `case-set` + `leg-set`/`leg-missing`, so
  no census escape exists through it.

## 3. Tamper-evidence demo (can an edited instrument bless a receipt?)

Fixture `S/fakelane`: byte-identical probe+grader, `git init -b master`, toplevel asserted,
committed with explicit identity; committed blob `9aef6d33…` == lane's. Then
`PROBE_VERSION = 1 → 2` (edited sha `152b751e…`):

1. edited checker vs genuine receipt → rc 1: `probe-sha` + `probe-blob-working-tree` — the
   receipt written by the original instrument cannot be checked by an edited one.
2. edited checker vs receipt with PROBE sha reforged to the edited bytes → rc 1:
   `probe-blob-working-tree 9aef6d33… != 152b751e…` — the working-tree tie (:615) holds.
3. edited checker vs receipt with PROBE **and** PROBE_BLOB reforged → rc 1:
   `probe-blob 152b751e… != 9aef6d33…` — the committed blob is the anchor.
4. control: original checker vs the fully-reforged receipt → rc 1 (`probe-sha` +
   `probe-blob` + `probe-blob-working-tree`).

Only a commit to `master:` can complete the forgery — outside every seat's power, and
auditable against the freeze commit named in the claims doc. This is the round-69
M-J/M-K repair doing what the claims say.

## 4. Residual risk and verification gaps

- No liveness: TEST lines are self-reported; a forger who hand-writes all 56 observations,
  all seven digests, all three shas and both summary lines passes — that is the claims
  doc's named limitation (i), not a checker defect. The live witness remains the committed
  sandbox captures (`corpus/evidence/round70/nginx/sandbox/`, e.g. `K1-sandbox.txt` with
  `server_pid=2831758`).
- `case_sha256` equality is to frozen constants; re-deriving them against staged bytes at
  check time would require re-staging (the `--render-table --stage-sha` arm does this, not
  `--check-receipt`). Limitation (iv) at freeze.
- Trust anchor is `master:` at check time (`probe_blob_sha` :311–315); a force-moved master
  could bless a doctored probe. Mitigated today: tip `384e9c76`, blob == working tree ==
  `9aef6d33…`. Recommend the close-out re-check that anchor.
- Gap not covered: I did not re-run the battery itself (another seat's item); my review
  takes the genuine receipt's content as given and tests the checker against it.

## 5. What I ran (commands → rc)

`git rev-parse master` / `git cat-file blob … | sha256sum` / `sha256sum` probe+grader →
match; `sed -n '111p' SHA256SUMS` → match; `--check-receipt <genuine>` → 0;
`--render-table` → 0; `--selftest --work $S/selftest` → 0; forgery battery
(`gen_forgeries.py`, 30 receipts under `$S/forgeries/`) → 26 refused rc 1 with the defects
tabulated above, 4 accepted (A-1 ×3, A-3 ×1); tamper fixture runs 1–4 → rc 1/1/1/1;
`fakelane-uncommitted` run → rc 0 (`CHECK probe-blob=absent`).
Bounds notes: all writes under `$S` and this report; fixture git activity confined to two
verified-toplevel scratch repos with explicit identity (one `git stash` inside the tamper
fixture to restore the pristine copy for run 4); no lane, fleet, `scripts/`, `templates/`,
`.ufo/state/` or sibling-lane writes; no tool installs.

## 6. Verdict

**`--check-receipt` implements the frozen R70-C1 sentence clause by clause as written —
every clause maps to enforcing code, none is prose-only, and none of the 30 forgeries lets
a single-occurrence receipt pass with any frozen vector, digest, sha, pin or coverage
requirement relaxed.** Residual findings, in severity order: (LOW) duplicate
`VECTOR`/`CASE` lines are resolved last-write-wins instead of refused (:644/:659 — f2b/f3
accepted); (LOW, latent) the absent-blob arm (:608–611) leaves PROBE_BLOB unbound if the
instrument is uncommitted; (INFO) receipt-side PORT/LEG-COVERAGE/PROBE_VERSION/server_pid/
sandbox_rc fields sit outside the checked surface (f9), consistent with the freeze's named
live-witness limitation. Recommend a duplicate-line defect branch at a future amendment;
not edited here by bound of the seat.
