author: hyaku closure (non-author integrator, @m_zfl)

# Round 100 — non-author verifier spot-check (kengaku)

Closure of lane-round kengaku r100. BASE `7846037679de77d050141c785996471801e5a19a`, lane HEAD after the
round `83cde63266b53204ef888dc3dae5a8194b24c9bd`, freeze F `54df15ca1f9b689b25c6ffc3b2fccd1253bdd6c2`,
measured T `dbe0cefa607cf57f7f58346fce64bcc127144ca0`. Report `.ufo/reports/round-100/kengaku.md` (fleet
repo). Driver digest copied from `.ufo/watchdog.log` (lines 3000, 3003):
`2026-11-06T12:03:27-03:00 launch kengaku round=100 pgid=4062617 driver=hyaku-inline attempt=1`;
`2026-11-06T15:01:10-03:00 complete kengaku round=100; hyaku-inline attempt=1`.
All measurements below were run by this reviewer on 2026-11-06 over committed bytes (`git show REV:path`)
or live upstream URLs. No lane gate or probe was executed (§Gate standard, Closure consequence).

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H a=%aI c=%cI' -- .ufo/reports/round-100/kengaku.md` | `kengaku-shokunin <kengaku@shokunin.local> 6e8d4ab0… a=13:46:57 c=15:00:34 -03:00` (committed after lane HEAD 14:59:27, before completion 15:01:10) | pass (author date precedes the settlement commit; jj author-date artefact, noted) |
| `SHONEN` heading, one line per box | read report §SHONEN | four `[~]` lines, each with an evidence pointer | pass |
| cited commits exist and are ancestors of `master` | `git cat-file -e H^{commit} && git merge-base --is-ancestor H master` for fb0f125c, 4df35de8, 934b984a, f07c026e, 5220b71d, 54df15ca, dbe0cefa, d8ed39bd, e40b332a, cd0705f6, 83cde632 (+ BASE) | 11/11 ok, all authored `kengaku-shokunin`; BASE ok (`protocol-shokunin`) | pass |
| pushed, no uncommitted round work | `scripts/hyaku/jj-lane.sh state …/kengaku-shokunin`; `git status --porcelain` | `branch=master local=83cde632… remote=83cde632… ahead=0 behind=0 head=detached tracked=0 untracked=2`; untracked = `.ufo/waves/round-97/w1.ready{,.dispatched}` (orchestrator markers, disclosed) | pass |
| remote tip | `git ls-remote origin refs/heads/master` | `83cde63266b53204ef888dc3dae5a8194b24c9bd` | pass |
| prompt carries template contract | `diff <(sed -n 1,140p .ufo/prompts/kengaku-round-100.md) templates/round-prompt.md` | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions; §1–§5 verbatim; hyaku addendum §6 onward | pass |
| wave settled | `git ls-tree 83cde632 .ufo/waves/round-100/w1/`; `w1-results.json` | 11 seat reports (ConnectorOverlap, CriticClaims, ExecC1, ExecC2, ExecHarm, ExecOCR, MutC1, MutC2, ReviewC1, ReviewC2, ScoutSources); results `seats:12`; ScribeLesson dead, disclosed | pass (dead seat noted) |

Not a marker: eleven round commits, a probe receipt and two measured claims.

## Claims — re-check

Re-measured = plain counts I ran myself; evidence-verified = committed receipt of a lane instrument read,
not executed.

### Freeze integrity (both claims)

- Re-measured: the 16 `frozen-instruments` sha256 lines of `plans/round-100-claims.md` against
  `git show 83cde632:path | sha256sum` → **16/16 ok** at the lane tip; the 6 `candidate-bytes` files hash
  identically at T and at tip (`726dcdc8…`, `d0df8332…`, `1f4c2354…`, `18be616b…`, `a910b60a…`, `974ba21d…`
  = the frozen values).
- Re-measured: `git diff --name-status F T` = the 6 candidate files + `corpus/evidence/round100/fdp-probe.txt`
  — exactly the frozen allowance.
- Re-measured: `sha256sum -c SHA256SUMS` over a `git archive 83cde632` extraction:
  `tb2-financial-document-processor/` 25/25 OK, `fdp-solution/` 15/15 OK.

### R100-C1 — coverage (eighteenth offline TB2 replay, `financial-document-processor`)

- Re-measured (jq over `plans/grader-population-ledger.json`): `.members|length` 88 at BASE and tip;
  executed BASE 43 → tip 44; `crypto-credential` executed 4/12 → 5/12; `file-artifact` 34/76 → 35/76.
  The member's row flips from `status unexecuted, reason unattempted` to `status executed, reason replayed,
  round 100, receipt corpus/evidence/round100/fdp-probe.txt`. `SKILL.md:74` reads `executed 35 of 76`;
  `SKILL.md:77` reads `executed 5 of 12`.
- Re-measured: receipt `fdp-probe.txt` → `grep -cE '^CASE .* ok=True'` 15, final `mismatches 0`,
  `LANE_TIP 54df15ca…` (= F), `SUBJECT_SHA 978f506a…`.
- Re-measured live: upstream `…/2fd12b88…/financial-document-processor/tests/test_outputs.py` sha256 =
  `978f506ad5c1bfaf28f9bc774dfe4347d33d046ca009b8496eb513956b7f5a9a` (= capture). Mechanism spot-read of
  the live grader: `hashlib.file_digest(f, "sha512")` (l.14) collected into `set()` (l.57, l.89) and compared
  by equality (l.66) → duplicates collapse (C08); `test_original_documents_dir_empty` counts
  `documents_dir.iterdir()` entries with `is_file()` only (l.222) → copies in a subdirectory pass (C07); the
  amount checks are `abs(…) < 0.01` (l.208, l.212) → strict band (C11/C12); the total row is compared to the
  hard-coded `{"total_amount": 81315.20, "vat_amount": 5402.48}` (l.174) with no summation or position check
  (C03). The located gaps follow from these bytes.
- Evidence-verified: `L1/c1-base.txt` `REV 78460376…`, `PREDICATE R100-C1 fail`, rc=1; `L1/c1-tip.txt`
  `REV dbe0cefa…`, `LEGS L1..L13=pass`, `TARGET executed_rows=44 member=financial-document-processor
  cells=crypto-credential:5,file-artifact:35 … cases=15 legs=120 mismatches=0 new_rows=8 … defects=0`,
  `PREDICATE R100-C1 pass`, rc=0. Matches the report. MutC1 F1 (TARGET printed, not asserted) does not
  affect this ruling: every TARGET field I could count independently (44, 5/12, 35/76, 15 cases,
  mismatches 0, 8 new rows) was re-measured above.
- Verdict: **verified**; axis `coverage` **improved** (score held 7 at the L0 cap; the move is measured by
  the ledger).

### R100-C2 — freshness (9 wrongly bound rows re-bound to their URLs' own committed files)

- Re-measured, independent of the lane counter: for each of the 9 rows in the three new
  `corpus/evidence/round{52,58,94}/PROVENANCE.md` files (S210, S219, S228, S232, S279, S281; S211; S298,
  S300), `git show 83cde632:corpus/evidence/round<N>/<file> | sha256sum` equals the PROVENANCE sha256
  cell (9/9), the BASE SOURCES row carries that digest (9/9), and the row's pinned URL ends in the same
  upstream path as the bound file (9/9; e.g. S298 → `write-compressor/tests/original-decomp.c`, S300 →
  `write-compressor/solution/solve.sh`). Every PROVENANCE table has three cells and no URL.
- Re-measured live (2026-11-06): S300 `01550b7d…`, S210 `02bca54d…`, S298 `7f8d9ef6…` — upstream bytes still
  hash to the row digest (3/3 sampled).
- Re-measured: `git diff 78460376 83cde632 -- corpus/SOURCES.md | grep '^-' | grep -v '^---' | wc -l` = 0
  → no BASE row line removed or edited (consistent with K8 `base_rows_not_equal=0`).
- Evidence-verified: `L1/c2-base.txt` `PREDICATE R100-C2 fail` rc=1 (`pop=9 cleared=0`); `L1/c2-tip.txt`
  `REF 5220b71d…` (= F~1), `GATE defects base=33 ref=32 rev=23`, `LEGS K1..K10=pass`,
  `TARGET pop=9 cleared=9 still=0 … base_rows=333 base_rows_not_equal=0 new_provenance_files=3 …`,
  `PREDICATE R100-C2 pass` rc=0. Matches the report.
- Verdict: **verified**; axis `freshness` **improved** (score held at ceiling 10; the move is 9 live-verified
  re-bindings, gate 32 → 23 from REF).

### No owned axis harmed

- `git diff 78460376 83cde632 -- SCORECARD.md`: one appended `## Round 100` section only (+58 lines, 0
  removed); scores stated: coverage 7, freshness 10, novelty 8, depth 10, operability 10, calibration 10,
  adjacency 9 — all held, none lowered. `PROVINCE.md` and `SHONEN.md` unchanged (`git diff --stat`).
- Evidence-verified: `L1/harm/README.md` — every check rc unchanged BASE → T (23/23), finding-set deltas
  limited to the C2 clears, S295/S300 reclass, and per-member count drift in already-red r77c1/r78c1/r81c1/
  r82c3; frozen-instruments union of 8 historical tables, 99 rows, 0 differ at T.

### Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | improved | ledger 43 → 44 executed, crypto-credential 4 → 5/12 (re-measured) |
| freshness | improved | 9/9 bindings re-derived, 3 live re-fetches equal (re-measured) |
| novelty | unchanged | no claim; score 8 held |
| depth | unchanged | no claim; score 10 held |
| operability | unchanged | no claim; score 10 held |
| calibration | unchanged | no claim; score 10 held |
| adjacency | unchanged | no claim; score 9 held |

## Discernment spot-check (`corpus/lessons/round-100.md` §Gate)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S342 | admit (A, mined) | live `…/financial-document-processor/tests/test_outputs.py` l.66 | agree | line 66 reads `assert actual_file_hashes == expected_original_documents, (` verbatim (5 words ≤ 25); the file is the grader the replay runs and its sha256 equals the capture |
| S348 | reject (A) | live `…/financial-document-processor/task.toml` l.29 | agree | line 29 reads `docker_image = "alexgshaw/financial-document-processor:20251031"`; the replay never pulls the image, so as a replay input it is correctly rejected with a stated flip |
| S349 | reject (B) | live `…/financial-document-processor/README.md` l.40 + grader l.174–187 | agree | README l.40 is `6. Correct summation in the final "total" row`; the grader compares the `total` row to hard-coded constants with no summation or position check, and probe case C03 (11 total rows) passes — the README's verification claim is contradicted by the bytes |

SOURCES row re-opened: S342 in `corpus/SOURCES.md`@83cde632 — quote cell
`tests/test_outputs.py:66 quote “assert actual_file_hashes == expected_original_documents, (” (5 words)`,
≤25 words, verbatim at the live line.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → rc=0,
`kengaku ok`, 32 W04 (new W04 = S342 duplicate URL across scopes, disclosed in the report).

## Trend verdicts

- **expansion: improved** — new `corpus/knowledge/tb2-financial-document-processor-grader.md` (sha512-set
  plus lookup-by-key grading, not held at BASE), indexed in `corpus/README.md` §Round-100 coverage-map
  addition; ledger 43 → 44; SOURCES 333 → 341 (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`).
- **quality: improved** — 9 wrongly bound digests re-bound to their URLs' own files with live re-verification;
  zero BASE SOURCES lines changed; Q87–Q89 added (`corpus/QUALITY.md:1417-1419`), each lesson-grounded; no
  post-T correction.
- **discernment: improved** — this non-author spot-check agrees with 3/3 sampled gate decisions (1 admit,
  2 rejects) with reasons above; the lane's own ScoutSources agreement is lane-internal and not counted.

## Routed defects (lane fixes next round)

1. Gate standard: `round100-prefreeze-check` is registered as a **gate** with
   `none declared — no self-invocation mode`; a gate needs a self-test over isolated fixtures asserting exit
   code and a stable finding id. Add one or re-register it as a probe.
2. MutC1 F1 and 19/47 survivors: assert the TARGET fields in-counter (lane already plans this).
3. MutC2 T21: a duplicated same-id SOURCES row is invisible to K8/K10/L10 — count rows by line.
4. CriticClaims F1 (receipt run identity self-reported), F2 (C2 does not bind C1-owned candidate files),
   F3 (K9 checks a receipt, not liveness); ReviewC2 minors.
5. Dead seat ScribeLesson (no report after 2 h 13 min) — conformance note; its scratch is not evidence.
6. Census W04 count 31 → 32 (S342 cross-scope duplicate URL): warning only; resolve or annotate the scope.

Operator note: SHONEN boxes 1–4 are `[~]` with resolvable pointers; box 2 (end-to-end task executed and
logged: `fdp-probe.txt` + `LOG.md:3741`) looks checkable by a non-author. No `[x]` written here.
