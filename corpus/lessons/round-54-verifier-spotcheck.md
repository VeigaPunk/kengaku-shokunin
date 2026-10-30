# Round 54 verifier spot-check — kengaku

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-10-30
report: `.ufo/reports/round-54/kengaku.md` (fleet commit `0dea9cb04e69eddc59c7f54c9029a606c2a69b53`, author/committer `kengaku-shokunin`)
lane base `6c919180260ea545589c2c0a007a06f554b529d3` → tip `16ef40fda5b32b93abd3d79f7e1cae48ee46585b`

Dispatch digest (from the closure prompt; matches `.ufo/watchdog.log` live):
`2026-10-30T07:19:43-03:00 launch kengaku round=54 pgid=1572639 driver=hyaku-inline attempt=1` /
`2026-10-30T08:59:05-03:00 complete kengaku round=54; hyaku-inline attempt=1`.

## 1. Conformance results

| check | command (abridged) | observed | verdict |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-54/kengaku.md` | `kengaku-shokunin 0dea9cb0…` | pass |
| SHONEN heading + boxes | `grep -c '^## SHONEN' <report>`; box lines vs `SHONEN.md` | 1 heading; 4 `[~]` lines = 4 boxes | pass |
| cited commits exist + ancestry | `git cat-file -t` + `merge-base --is-ancestor <h> master` × 5 (17f90355, 6e0a1915, 62e9bba5, 9a0746be, 16ef40fd) + base 6c919180 | all type=commit, all ancestors | pass |
| pushed / no leftovers | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain` | `local=16ef40fd remote=16ef40fd ahead=0`, tracked=0 untracked=0, porcelain empty | pass |
| remote tip | `git ls-remote origin refs/heads/master` | `16ef40fda5b32b93abd3d79f7e1cae48ee46585b` | pass |
| prompt carries template contract | diff vs `templates/round-prompt.md` | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions in §§1–5; hyaku addendum §6 appended | pass |
| report lands after lane work | commit timestamps | lane tip cI 08:55:58-03:00 < report commit cI 08:58:31-03:00 (driver complete 08:59:05) | pass |
| report not a marker | report content | real committed work, 5 cited hashes, all sections present | status ok (not failed-marker) |

Observations (status-neutral): report commit author-date 08:55:04-03:00 precedes the lane-tip
commit time by 54 s (committer-date 08:58:31; ancestry and remote checks are the binding tests
and both pass). Fifteen empty terminal outputs and one partial C1Forge output (377 chars,
`w1-results.json`) provide no clearance, as the report itself states.

**Conformance defect (lane-declared, closure re-derived):** strict qualifying attack share
reviewer5+critic7+mutation-tester4 = **16/66 = 24.24%**, below the ≥25% floor. Closure recount
over `w1-results.json`: executor35, scribe3, scout5, reviewer5, critic7, mutation-tester4,
sentinel2, revenger2, connector2, simplifier1, total 66, no planner role, 66 in the 64–128 v2
band. Initial 18/66 counted sentinels and is not floor proof. Status-neutral.

## 2. Per-claim re-checks

Method note: both claims rest on lane-owned gates/counters, so per PROTOCOL §Gate standard
(Closure consequence) closure **evidence-verified** them — committed receipts, counter code
paths and frozen predicates over committed bytes; **no sibling gate was executed**. Everything
in §1 and §3 was **re-measured** by closure directly.

### R54-C1 — novelty 8→9 "externally anchored measurement freeze" — NOT ADMITTED (agree)

- Frozen claims unchanged: `git diff 17f90355 16ef40fd -- plans/round-54-claims.md` → empty (same blob `db977487`).
- Before receipt `corpus/evidence/round54/c1-before.txt` names `rev 6c919180…`, records `SETUP anchor absent`, `PREDICATE R54-C1 fail`, `exit=1`; anchor dir absent at base (`git ls-tree 6c919180` empty).
- After state at tip: `anchor.json` present (`stamped_at 2026-10-30T10:49:37+00:00`, `calendars: []`, header/confirmation deferred by its own note); `header.bin` **absent** (`git ls-tree` empty).
- Counter code path (read, not run): `plans/round54_c1_anchor.py:317-320` — `if not header_p.is_file(): … "PREDICATE R54-C1 fail"; return 1`. The fail is derivable from committed bytes alone.
- After receipt `integrate/c1-after.txt` names `REV 9a0746be…` (the report's declared measured-after revision), `PREDICATE R54-C1 fail`, `EXIT 1`.
- Reviewer evidence `w1/R1C1Counter.md`: raw-stream deserialization defects reject ordinary proofs and controls alike; digest identity check substitutes for op-path reachability — selftest 8/8 was inadequate positive-path evidence.
- No externally validated completed anchor is claimed anywhere; SCORECARD holds novelty 8→8.

Verdict: **improved=no; unchanged; claim honestly failed.** No capability enters.

### R54-C2 — calibration 9→10 "entry-argv registry truth with hermetic execution" — NOT ADMITTED (agree)

- `plans/round54-entrytruth.json` (tip): jq over committed bytes → `rows: 78`, `declared_green: 62`, `declared_red: 16` (declaration counts; final observations live in the receipt).
- After receipt `integrate/c2-after.txt` at tip: `REV 9a0746be…`, `RUN executed=78 timeout=0 mismatched=0 evidence_missing=1 laundered=1`, `TIPSTATE entry_declared_green=62 entry_declared_red=16 observed_green=61 observed_red=17`, `MIGRATION redeclared=4 r53_green_nonentry=4`, `PREDICATE R54-C2 fail`, `EXIT 1` — matches the report's quoted block byte-for-byte.
- Kill rule (declared at freeze in `plans/round-54-claims.md`, before data): calibration held at 9 if any attack seat produces a row passing the r54 counter while true entry behavior disagrees. `w1/R2C2Counter/laundering-probes.txt` records two such false passes (`abbreviated-selftest`, `uv-decoy-script`: true entry exit=1, counter `laundered=0`, `PREDICATE R54-C2 pass`, `EXIT 0`). Counter code `plans/round54_c2_entrytruth.py:329-340,358-361` shows the laundering/evidence-missing branches and the conjunctive predicate. The frozen claim-level kill rule fires.
- Route control `claims/c2-route-r53.txt`: unmodified r53 counter passes a selftest-green/entry-red forged fixture (`PREDICATE R53-C2 pass`, `ROUTE laundering demonstrated (r53 rc=0)`) — red-before shown able to fail.
- Operability harm receipt `integrate/round52-c2-regression.txt`: `ADVERTISED total=79`, `REGISTERED total=77 rows=79`, `MISSING plans/round54_c1_anchor.py`, `MISSING plans/round54_c2_entrytruth.py`, `PREDICATE R52-C2 fail`, exit 1.
- Counter honours `--work/--jobs/--timeout`; no hardcoded `/tmp` (scratch discipline).

Verdict: **calibration 9→9 held; frozen kill rule fired; claim honestly failed.** The
operability regression is real, committed, and retained (SKILL.md frozen unchanged by rule) —
**operability harmed 9→8**.

## 3. No-owned-axis-harmed check (re-measured)

`git diff 6c919180 16ef40fd -- SCORECARD.md` is **additive only** (one hunk: the Round-54
section + measured-close correction); no prior score row edited. Axis state carried from r53
(SCORECARD:2278): calibration 9, coverage 7 (open L0 cap r25/33/51), novelty 8, depth 9,
operability 9, freshness 9, adjacency 9. Round-54 outcome: novelty unchanged (8→8 held),
calibration unchanged (9→9 held), coverage/depth/freshness/adjacency unchanged, **operability
harmed 9→8** (explicitly superseded in the SCORECARD measured-close, not silently held).

Per-axis verdicts: novelty `unchanged`; calibration `unchanged`; coverage `unchanged`; depth
`unchanged`; freshness `unchanged`; adjacency `unchanged`; operability `harmed`.

## 4. Discernment spot-check (outside, non-author)

Sample: the round Gate's complete new-row set (3 rows — 2 admits, 1 reject; SOURCES diff shows
exactly these 3 additions, no old-cell changes). Every source re-opened live on 2026-10-30.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S198 OpenTimestamps — How it Works | admit A (existence-not-correctness) | https://opentimestamps.org/ §How it Works | **agree** | Located quote verified verbatim: "A timestamp proves that some data existed prior to some point in time." (13 words ≤25). Tier A docs is right for the timestamp-semantics scope; the admit's interpretation is exactly what the source states. |
| S199 OTS Client README — Usage/upgrade | admit A (pending-vs-confirmed lifecycle) | README.md @ master, line 82 | **agree** | Quote verified verbatim: "You can also upgrade an incomplete timestamp, which adds the path to the Bitcoin blockchain to the timestamp itself" (20 words ≤25). Official client docs; correctly grounds submission ≠ confirmation. |
| S200 python-opentimestamps notary.py | reject as sole chain-membership/novelty evidence | notary.py @ master, line 240 (BitcoinBlockHeaderAttestation docstring) | **agree** | Quote verified verbatim: "The commitment digest will be the merkleroot of the blockheader." (10 words ≤25). The docstring records only digest==merkleroot + block height; nothing establishes canonical-chain membership (a fork's header would verify the same way) or preregistration novelty. Rejecting it as sole support is sound taste; keeping it as a row with flip condition is the contract's shape. |

Gate agreement on admits **and** rejects → LEARNING.md discernment observable met.

Census (re-run by closure): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` →
`kengaku ok …/corpus/SOURCES.md`, exit 0, same 15 pre-existing W04 duplicate-URL warnings
(S040…S100). Manual frozen counts: rows 193 (190→193), malformed 0, tiers A=164 B=24 C=5,
status mined=172 rejected=13 queued=8 — matches `integrate/census-end.txt` and the report.

## 5. Trend verdicts (with evidence)

- **expansion: unchanged** — no capability admitted (`capabilities_added: []`), no uncovered
  coverage-map ground entered: the single new knowledge entry (`external-anchor-freeze.md`,
  README-indexed, cites S198/S199) is bounded sourced interpretation of a failed instrument,
  on ground the r53 freeze surface already worked; no frontier-to-core credit claimed.
- **quality: harmed** — the registry-closure regression (advertised79/registered77/missing2,
  exit 1, `integrate/round52-c2-regression.txt`) is a real, retained operability regression
  (9→8) exposed by the round's own canonical run and recorded, not waived; no trade admitted.
- **discernment: improved** — the outside spot-check (this file, non-author) agrees with the
  gate on all sampled admits and the reject (§4), completing the check the lane correctly left
  open; Q44 and the grounded r52-patch refusal add grounded criteria without self-attestation.

## 6. Routed defects / obligations for the lane's next round

1. **Registry closure (operability repair):** under a newly frozen rule, either register
   `plans/round54_c1_anchor.py` and `plans/round54_c2_entrytruth.py` or stop advertising them,
   so the round52-c2 counter closes again; then remeasure the entry ledger **after**
   documentation integration (this round's measured-close lesson).
2. **C1 prerequisite:** land a real canonical positive OTS proof that parses (fix the
   raw-reader/walker defects R1 demonstrated) before re-freezing any anchor claim.
3. **C2 prerequisite:** structurally bind interpreter + entry argv (abbreviation and uv-decoy
   routes both survive) before another registry-truth claim.
4. **Attack-share floor:** dispatch ≥25% strict attack roles (reviewer+critic+mutation-tester)
   inside the 64–128 band; sentinels do not count toward it.
5. **Carry r52 repair:** the refused E3 patch's order-check regression and masked K7 control
   stay open until fixed; production r52 counter intentionally unchanged this round.
6. **Operator-owned (for notes, not this closure):** all four SHONEN boxes carry only `[~]`;
   boxes 1–4 look checkable by a non-author from LOG/SKILL/PROVINCE receipts — promotion
   review remains operator-owned; this closure writes no `[x]`.
