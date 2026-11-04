author: hyaku closure (non-author integrator, @m_zfl)
lane: kengaku · round: 72 · date: 2026-11-03
report: `.ufo/reports/round-72/kengaku.md` (fleet commit `ea803a5f`, lane identity); lane base `c6322972` → lane tip `db78d059` (remote `refs/heads/master` = `db78d059`)

# Round 72 — kengaku verifier spot-check (non-author)

I did not author this round. Everything below is re-derived from committed bytes at the lane tip
unless it says *evidence-verified*: lane-owned gates and selftests were checked by their committed
receipts, never executed (PROTOCOL §Gate standard, Closure consequence). Dispatch digest (copied
from `.ufo/watchdog.log`, which is mutable):
`2026-11-03T22:50:15-03:00 launch kengaku round=72 pgid=1515437 driver=hyaku-inline attempt=1` /
`2026-11-03T23:28:12-03:00 complete kengaku round=72; hyaku-inline attempt=1`.

## 1. Step-1 conformance

| item | check | observed |
|---|---|---|
| report landed by the lane | `git log --format='%an <%ae> %H' -1 -- .ufo/reports/round-72/kengaku.md` | `kengaku-shokunin <kengaku@shokunin.local> ea803a5f5c19e764594258685014e89bd4d25cb8`; ancestor of fleet `origin/master` (`git merge-base --is-ancestor ea803a5f origin/master` → yes) |
| SHONEN heading | `grep -c '^## SHONEN' report`; `[~]` lines vs `SHONEN.md` boxes | 1 heading; 4 `[~]` lines = 4 boxes, each with a pointer; no `[x]` |
| cited commits | `git cat-file -t` + `git merge-base --is-ancestor <h> master` | `c6322972`, `b6336136`, `db78d059` all exist and are ancestors of `master`. **Defect (a):** the report's "Landing" hash `08df910a461620741d433def3df38a8406efe9f` is **39 hex chars** (lines 5, 175, 187, 310) and resolves to no object (`git cat-file -t` → `fatal: Not a valid object name`); the real landing commit is `08df910ab461620741d433def3df38a8406efe9f` (the 8-char `08df910a` in the Landed-changes table resolves) |
| lane clean / pushed | `jj-lane.sh state`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=db78d059 remote=db78d059 ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote prints `db78d059` |
| prompt fidelity | rendered `templates/round-prompt.md` §1–5 (lane/round/fleet-root/axes substitutions) vs `.ufo/prompts/kengaku-round-72.md` §1–5 | `diff` empty except the working-dir token (template `<kengaku-repo>` → `kengaku-shokunin`); §6 hyaku addendum present; all five child-lane items present (report path, commit-then-push, SHONEN heading, hash citation, write scope) |
| L2 route map | prompt net map vs `~/.omp/agent/config.yml` `task.agentModelOverrides` | prompt "only reviewer `@m_zfl`; every other role `@m_flash`" = config exactly (reviewer `@m_zfl`; 17 other roles `@m_flash`) |
| wave shape | `w1-validate.rc`; `w1-spec.json`; `w1-results.json`; wave dir | rc 0; `items=16` = executor 6, scribe 3, reviewer 2, mutation-tester 2, critic 1, scout 1, connector 1 (attack 5/16 = 31.25 % ≥ 25 %; 1 connector ≤ 2); `seats=16`, 16 results; 16 seat reports on disk; `w1.ready`/`w1.ready.dispatched` present |
| planner seat | report + wave registry | recorded at report lines 35–37: validator rejects the `planner` role, the L1 holds the canonical §3 planner seat, the data-walk rode `SurfaceScoutR72`/`C2RedBeforeR72` — closes R71-R3's recording defect |
| report sections | order and presence | Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN, Addendum — all present |

**Conformance defects (status-neutral; routed in §6).** (a) the dead 39-char landing hash above.
(b) `corpus/evidence/round72/census-after.txt` records `LANE_TIP: b6336136…` while its
`RUN_AT: 2026-11-04T02:26:17Z` (23:26:17-03) is a landing-tree run and the file is added by
`08df910a`; the report bundles it with "the final counter receipts were re-run at that tip and
committed in `db78d059`", which is true of the other three files only (`git show --stat
db78d059` → `c2-controls-final.txt`, `c2-green.txt`, `final-c1-check.txt`). The census substance
(240 rows, rc 0, 25 `W04`) re-derives from committed bytes at `db78d059`. (c) the lesson's reject
ground (iii) quotes a sweep that does not reproduce (see §4). None of (a)–(c) is a marker: the
report names real committed work (`b6336136`, `db78d059` both resolve and are ancestors), so the
lane-round is `ok` with these as defects.

## 2. Claim re-checks

### R72-C1 — coverage (lowest non-retired axis, L0-capped at 7)

| measurement | command | base `c6322972` | tip `db78d059` |
|---|---|---|---|
| instrument absent → present | `git cat-file -e c6322972:plans/round72_c1_hf_probe.py` | rc 128 (path not in commit) | present |
| receipt of record | `git show db78d059:corpus/evidence/round72/hf/receipt.txt \| wc -c; \| sha256sum` | — | 3494 B, 40 lines, sha256 `fa060b7fa2e4…224087` (= report's `fa060b7f…4087`) |
| replicate identity | `git show db78d059:…/receipt-replicate.txt \| sha256sum` | — | same sha256 `fa060b7f…4087` |
| frozen vectors | `grep -cE '^VECTOR '`; `grep -c 'agree=True'` | — | 9 / 9 |
| leg coverage | parse `LEG-COVERAGE` | — | `legs=4 seen_p=4 seen_f=4` |
| summary | parse `SUMMARY` | — | `cases=9 legs=36 mismatches=0 setup=0 exc=2` |
| provenance | count `^PROVENANCE ` lines; read fields | — | exactly 1 line; `allowlist_seen=9/9`, `canary_seen=0`, `distinct=1`, `transformers_file=/venv/…/transformers/__init__.py` |
| per-case vectors | nine `sandbox/K*/manifest.json` → `derived` | — | K1 `PPPP`, K2 `PPFP`, K3 `PPFP`, K4 `PPPF`, K5 `PFPP`, K6 `PFFF`, K7 `FPPP`, K8 `FPPP`, K9 `PPPF` = the frozen table exactly |
| provenance per case | every manifest → `prov` | — | all nine `canary=ABSENT`, `cwd=/app`, `executable=/venv/bin/python3`; `env_keys` 11 for K1–K6/K9 and 10 for K7/K8 (the round's F1) |
| case digests | `grep -o 'case_sha256=…' \| sort -u \| wc -l` | — | 9 distinct; replicate carries the same nine |
| assert sites | `grep -o 'AssertionError[^"]*' sandbox/K9/manifest.json` / K4 | — | K9 `Error response should contain 'error' field`; K4 `API should return 400 for invalid request format` — the two `:107`/`:103` witnesses |
| stub before | `…/stub-before-v1.txt` | — | `SUMMARY cases=8 legs=32 mismatches=6 setup=0 exc=10`, `PREDICATE R71-C1 fail` |
| stub after / control | `…/stub-after-v2.txt`; `…/stub-control.txt` | — | `PROVENANCE … canary_seen=0 …, SUMMARY cases=9 … mismatches=0`, `PREDICATE R72-C1 pass`; `STUB-CONTROL exposed=False vectors_unchanged=True` |
| checker verdict | `hf/check.txt`; `final-c1-check.txt` | — | `DEFECTS n=0`, `PREDICATE R72-C1 pass`, rc 0; final run `LANE_TIP: 08df910ab…`, `RUN_AT: 2026-11-04T02:26:46Z` |
| selftest tally | `c1-selftest.txt` | — | `SELFTEST red_refused=8/8 accept_ok=1 state_sensitive=1 path_independent=1 ok=True` |

*Re-measured:* every number above over committed bytes (digests, vectors, provenance records,
case-digest uniqueness, before-state, captures).
*Evidence-verified, not executed:* the battery and `--check-receipt`/`--selftest` runs — their
committed receipts and revisions were checked; the gate was not run. **R72-C1 verifies.**

### R72-C2 — calibration (held at ceiling 10, exercised)

| measurement | command | base `c6322972` | tip `08df910a`/`db78d059` |
|---|---|---|---|
| gate red → green | `c2-red-before.txt`; `c2-green.txt` | `DEFECTS n=6` (`E1a` ×4 row-absent, `E1b no-errata-section`, `E2`), `PREDICATE R72-C2 fail`, `EXIT=1`, `LANE_TIP: c6322972` | `E1a ok`, `E1b ok`, `E1c ok`, `E2 ok`, `DEFECTS n=0`, `PREDICATE R72-C2 pass`, `EXIT=0`, `LANE_TIP: 08df910ab` |
| controls | `c2-controls.txt`; `c2-controls-final.txt` | — | `SELFTEST defects-in-fake=3 want=3 all-fail=True append-only-arm=True positional-arm=True parser-arm=True ok=True`; `MUTANTS total=7 killed=6 survived=0 invalid=0 null_detected=1`; `ARM accept-green=ok refuse-red=ok attribution=ok`; final re-run `SELFTEST_EXIT=0`, `MUTANTS_EXIT=0`, `LANE_TIP: 08df910ab` |
| registry rows | `git show db78d059:SKILL.md \| grep -nE 'round7[12]_c[12]'` | absent (`round71_` count 0 at base) | four rows at `SKILL.md:695-698` (8 cells each) |
| erratum | `grep -n '^## Errata' plans/round-71-claims.md` | absent | `137:## Errata — round 72 (2026-11-03)` |
| diff shape | `git diff --numstat c6322972 db78d059 -- SKILL.md plans/round-71-claims.md` | — | `5 0` / `20 0` (25 insertions, 0 deletions) |
| registry debt | `registry-debt.txt` | — | `ADVERTISED total=110 REGISTERED total=105 rows=107 MISSING 5 DUPLICATE 0`, `PREDICATE R52-C2 fail`, `EXIT=1` — the five are pre-existing, named and routed (R72-D1), not claimed closed |
| structural gates | `gates/depth-gate.txt`, `gates/trio.txt` | — | `ROWS n=16 class_match=True count_mismatch=0 paths total=36 resolved=36 share=1.00`, `PREDICATE R63-C2 pass`; `SWEEP files=72 trio_open=43 addendum=29 red=0`, `PREDICATE R64-C3 pass`; class-row counters `executed 4 of 8`→1 rc0 / `executed 3 of 8`→0 rc1 (wave report `DepthGateR72.md`) |

*Re-measured:* the two gate receipts, both control tallies, the four registry rows, the erratum,
the diff shapes, the structural-gate receipts, the debt output.
*Evidence-verified, not executed:* the C2 gate, its `--selftest` and `--mutants`. **R72-C2
verifies.**

### No axis harmed

`git diff --stat c6322972 db78d059 -- SCORECARD.md` → 76 insertions, 0 deletions (the round-72
section + the `Superseded (round 72)` pointer only; every prior axis row untouched). The whole lane
diff carries 0 deletions (`git diff --numstat c6322972 db78d059 | awk '{d+=$2} END {print d}'` →
`0`). `PROVINCE.md` unchanged. Depth and trio gates green; scores held or improved.

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | improved | grader replay now prices nine cases and both assert sites of leg 4 (`:103`/`:107`) under a provenance witness; frozen predicate `DEFECTS n=0`; score still held at 7 by the open L0 cap `kengaku | round-25/33/51` |
| calibration | improved | R71-R1/R71-R7 closed by a re-deriving gate `n=6` → `n=0` with selftest 3/3, 6/6 semantic kills and a demonstrated null; score held at ceiling 10, exercised |
| depth | unchanged | one new entry (held) + two tier-A rows; depth gate green; score 10 held |
| operability | unchanged | two instruments run, four registry rows accurate under the audit; score 10 held |
| freshness | unchanged | both new sources fetched live with sha256 and byte-identical re-fetch; score 10 held |
| adjacency | unchanged | `SiblingOverlapR72` found 12 surface-level sibling sites, named and routed, nothing absorbed; score 9 held |
| novelty | unchanged | no new instrument-level construct claimed (`--clearenv` restoration); score 8 held |

## 4. Discernment spot-check (non-author)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S247 — `bwrap(1)` manual at 0.13.1 | admit, tier A | live `curl https://man.archlinux.org/man/bwrap.1.en` → HTTP 200, **27981 B**, sha256 `708f56ee…68de7`; committed capture `corpus/evidence/round72/sources/bwrap.1.html`, quote at `:184-186` | **agree** | live bytes and digest are identical to the row and capture; the 15-word `--clearenv` quote is present verbatim at the named lines; the scope ("environment controls as the manual states them") is bounded by the row |
| S248 — HF model card `distilbert-base-uncased-finetuned-sst-2-english` | admit, tier A | live `curl …/raw/main/README.md` → HTTP 200, **10512 B**, sha256 `75f17282…7588851`; capture `:145`, 197 lines | **agree** | live bytes/digest identical; the 3-token `from_pretrained(...)` quote is at `:145`; the landing `197 lines` correction re-derives (`wc -l` → 197) |
| `merge/kengaku` entry `card-provenance-and-preregistration.md` | reject (reason + flip) | `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/card-provenance-and-preregistration.md` (4576 B, 54 lines); `MERGE-REPORT.md:50`; this lane's `corpus/SOURCES.md` | **agree on the decision; disagree with one stated ground** | grounds (i) blank line 1 / `source:` `:2-7`, `verified-at:` `:8`, `recheck:` `:9`, `ground:` `:10` and (ii) `S159`–`S164` resolve here to TB2 `password-recovery` files, the only URL the lane holds is `S081` for arXiv `2608.29463` — both re-derive. Ground (iii)'s quoted sweep `grep -rn 'N14\b\|N20\b' corpus plans` → "no rows" does **not** reproduce: it prints `plans/battery38/d4m.py:2,11,20` (round-38 mutant labels, not ground ids) and this lesson's own lines; no ground-id registry exists. The reject survives on (i)+(ii) |

New `SOURCES.md` rows carry ≤25-word located quotes (15 words for S247, 3 for S248) and both are
`status: mined`, `used-by: corpus/knowledge/tb2-hf-model-inference-provenance.md`. Census:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
→ rc 0, 240 rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` on committed bytes: 238 at
`c6322972` → 240 at `db78d059`), the same 25 pre-existing `W04`, `ok …/corpus/SOURCES.md`.

## 5. Trend verdicts

- **expansion: improved** — S247/S248 are new mined tier-A rows (census 238 → 240, re-measured),
  the README frontier bullet gains "Partly discharged round 72", and the `hf-model-inference`
  evidence moves to provenance-witnessed + assert-site-priced. Caveat, recorded: the round's new
  knowledge entry lands `admission: hold` (Q13/Q14 second wave absent), so the "net new admitted
  entries" leg is not exercised; the verdict rests on the frontier / new-source / evidence-reach
  observables, and the entry is named as held, not admitted.
- **quality: improved** — the round-71 routed defects close by a gate that moves `n=6` → `n=0`,
  killed 6/6 with an attribution arm and a deliberate null; the C1 selftest's 8/8 arms replace
  round-71's two defective arms; the four registry rows were audited (9/32 defective cells) and
  corrected before landing; the entry's three false statements were corrected before landing. No
  admitted entry was found false and left unmarked.
- **discernment: improved** — the non-author spot-check above agrees with both admits and with the
  reject decision, and the wave recorded its own instrument weaknesses (F1–F10: forged-receipt
  pass, presence-only erratum, duplicate-blind registry, 6/~13 priced refusal sites) rather than
  smoothing them; the entry is held rather than self-admitted.

## 6. Routed defects the lane must fix next round

1. **R72-V1 — dead landing-hash citation (conformance).** Report lines 5/175/187/310 cite
   `08df910a461620741d433def3df38a8406efe9f` (39 chars; no object). Correct hash:
   `08df910ab461620741d433def3df38a8406efe9f`. Fix by an erratum appended in the round-73 report
   naming the superseded text (filed reports are records — never rewrite); the SHONEN box-2
   pointer inherits the defect.
2. **R72-V2 — census-after revision label.** `corpus/evidence/round72/census-after.txt` says
   `LANE_TIP: b6336136…` for a landing-tree run (`RUN_AT` 23:26:17-03, file added by
   `08df910a`); the report bundles it with the tip re-runs committed in `db78d059`. Re-capture
   with the measured revision, or state the true revision in the erratum.
3. **R72-V3 — reject-ground sweep.** The lesson's ground (iii) claims its `N14`/`N20` sweep prints
   no rows; it prints three unrelated `plans/battery38/d4m.py` lines. Narrow the sweep to a ground
   registry (or drop the ground, which the reject does not need) and log the correction.
4. **R72-D1 (carried, lane-routed) — five pre-existing missing registry rows**
   (`round66_c1_tensor_probe`, `round69_c1_nginx_probe`, `round69_c2_routed_defects`,
   `round70_c1_nginx_probe`, `round70_c2_routed_defects`); `plans/round52_c2_registry.py` stays
   red until they land. Round 73's planned item 1.
5. **R71-R2 (carried, unclosed) — round-71 receipt-revision attribution**: the round-71 report
   attributed counters to `edaea66e` while the receipts' `REV` reads `c80fcdb3`; no round-72
   correction is on record. Append the erratum.
6. **Carried instrument limits (named by the lane, not defects of this claim):** forged-but-
   consistent receipts pass `--check-receipt`; `transformers_file` is prefix-checked; `E1b` is
   presence-only and `E1a` first-row-wins/frozen-set; the mutant matrix prices 6 of ~13 refusal
   sites; the knowledge entry stays `admission: hold` until a 2–4 seat `falsify` second wave.
   Round 73's planned items 2–4 target these.

## 7. Notes for the operator

All four `SHONEN.md` boxes carry `[~]` with pointers that resolve for a non-author (SKILL decision
table + depth gate receipt; the R72-C1 LOG entry → receipt of record; the entry's `recheck:`
command; `SiblingOverlapR72`). Box 2's pointer cites the dead landing hash in R72-V1; the receipt
itself is at `08df910ab`. No `[x]` was written — promotion is operator-owned. The knowledge entry
`corpus/knowledge/tb2-hf-model-inference-provenance.md` stays `admission: hold`;
`plans/gate_timing_check.py`'s `no admit rows … failed=1` is the honest state this round does not
change.
