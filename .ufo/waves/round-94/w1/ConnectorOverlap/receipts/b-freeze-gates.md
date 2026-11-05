# Receipt (b) — frozen-instrument gates, freeze-commit compares, mutant counting, 2026-11-05

Queries (over 21 sibling lanes + fleet scripts/, tracked `;!**/.ufo/**` and full, both run):
`(?i)(frozen.?instrument|--full-history|TREESAME|freeze.?integrity)`;
`(?i)(freeze_integrity|check-freeze|freeze-order|freeze_edited|counter_not_frozen)`;
`(?i)mutant`; `(?i)(null copy|cli.?path|copy of the (gate|counter)|gate.{0,40}shutil.copy)`.
Lane HEADs as in receipts/a-tb2-scan.md.

## kaidoku-shokunin (c19d57cd2e65) — TRACKED, the strongest overlap

- `tools/round-44/c2-counter.py:595-598`:
  `def freeze_integrity(root, freeze, rev, frozen_spec, declared=(), frozen_dirs=()):` / `"""(changed_paths, notes).
  A changed frozen path is exit 2, never a pass."""`; called at :1194-1198 → `result['frozen_path_changed']`.
- `tools/round-49/c2-mismatch.py:67-70`: "equals its FREEZE blob; otherwise exit 2 `frozen_path_changed` (never "met").
  The counter also exits 2 `counter_not_frozen` when its own bytes differ from `tools/round-49/c2-mismatch.py` at
  FREEZE, and records both digests." Implementation :699-703 (`res['reason'] = 'counter_not_frozen'`).
- `tools/round-50/c1-counter.py:156-159` (docstring): "`receipt_fresh` — EVERY commit that adds the receipt path in the
  full history of REV (`git log -m --full-history --diff-filter=A`; the default simplified history hid a pre-freeze add
  behind a TREESAME merge in round 49) is a strict descendant of --freeze". Code :1574-1579. `counter_not_frozen`
  docstring :268-269; class :1929-1930; battery vectors :3475-3479 (alt counter bytes → exit 2 counter_not_frozen).
- `tools/round-50/c2-record.py:34-38`: "(4) The frozen-path walk (`git -c core.quotePath=false log --full-history -m
  --no-renames --name-status -z`, plus a blob-and-mode compare of every frozen path at FREEZE and REV) sees renames,
  quoted names, mode changes, added files and touch-and-restore. (5) The counter exits 2 `counter_not_frozen` when its
  own bytes differ from `tools/round-50/c2-record.py` at FREEZE." Walk :216-220; self-check :1294-1297.
  **Alt-path counter copy in the battery** :1591-1595 (`run('counter bytes differ from FREEZE -> counter_not_frozen',
  G, F, 2, None, 'counter_not_frozen', counter=alt)` … `os.unlink(alt)`).
- `tools/round-50/selftest-r49-c2.py:28-32,47-49,125-128,378-382`: hermetic self-test of the frozen r49 counter over
  fixture clones of the real history; mutation mode "rebuild FREEZE and BASE (planning only, in the clone) with the
  counter blob replaced by `mutant_bytes`, so the mutant passes its own counter_not_frozen guard and the selftest can be
  asked whether it notices a behaviourally different counter"; fixtures `x-counter-bytes` ("counter copy with one
  appended line: counter_not_frozen"), `x-frozen-edit`, `x-frozen-add`, `x-frozen-plan`; expected outputs in
  `tools/round-50/selftest-r49-c2.expected.json:402-406` (`"reason": "counter_not_frozen"`, `x-freeze-not-ancestor`).
- `corpus/lessons/round-49.md:52`: "Counter misses and limits found after the freeze (frozen, reported, not patched):
  C1 freeze walk accepts added files whose names git quotes … and copy-status adds, and `receipt_fresh` is blind to a
  TREESAME-merge add …; C2's walk over-refuses a merge shape (F4); provenance-prefix and `core.quotePath` clauses have
  no witness and three constant mutants are invisible".
- `plans/round-49-claims.md:42-43`: CritFreeze findings → "C1 walk aligned (adds, non-ASCII names); C2 exits 2
  `counter_not_frozen` …; the rest are **disclosed limits**" — the disclosed list includes "refs/replace, grafts and
  squashes are invisible". `plans/round-50-claims.md:46`: "…`counter_not_frozen`; `--full-history`; `oracle_rederived_ok`".
- `SKILL.md:1929-1942` (tracked registry): rows for tools/round-48/record2.py, round-49/c2-mismatch.py,
  round-50/c1-counter.py, round-50/c2-record.py, round-50/selftest-r49-c2.py, round-53/sqfs-triage-v6.py — exit-2
  semantics "frozen_path_changed, counter_not_frozen" advertised fleet-wide.

## mado-shokunin (24ba2a9ddac2) — TRACKED standing gate

- `quality/check-freeze-order.py` (397 lines; read :1-143): docstring — "was the round freeze committed strictly before
  the wave launched?"; FREEZE set `.ufo/waves/round-N/{claims-frozen.md,registration.md,frozen-tables.json}`; FREEZE
  commit = earliest first-parent-chain commit where every freeze file's blob equals its REV blob;
  `freeze_edited:<file>` when a freeze file's first-appearance blob differs from REV; verdict OK iff freeze committer
  time strictly earlier than `.ufo/waves/round-N/<W>/swarm-registry.json` createdAt; declared limits :11-14 include
  "an edit to a freeze file that is later reverted leaves the blob equal and reads OK" and committer-date backdating.
  Key code :120-124: `p = git(repo, ["log", "--first-parent", "--full-history", "--format=%H", tip, "--"] + fset, work)`.

## kumitate-shokunin (1325caf47a25) — plumbing only

- `scripts/plan-before-ready.sh:154-157` `oldest_add()` and :181-183 `map_first_add()`:
  `git -C "$1" log "$REV_RESOLVED" --full-history --diff-filter=A --format='%H%x09%ct' -- "$2" | tail -n 1` —
  plan/readme-gate first-add mapping for plan-before-ready gating. Not freeze-integrity.
- Wave history: `.ufo/waves/round-69/` ledger probe mutation battery ("7/20 mutants wrong" — stray copy visible at fleet
  root `kumitate-shokinin/kumitate-shokunin/.ufo/waves/round-69/w1/K69ExecBaseCounter.md`).

## mori-shokunin (5013f0be8ac9) — same plumbing, different predicate

- `tools/mori-sources-appendonly.py:236-237`: `git log --format=%H%x09%P --reverse --full-history <rev> -- <path>` —
  append-only registry supersede timing (`corpus/knowledge/gate-ancestry-r39.md:43-48,74-77`; SCORECARD.md:2228; the
  lane's own TREESAME drop lesson :31-32 "the default `git log -- corpus/SOURCES.md` walk silently drops TREESAME
  commits (6531ac60 … 53 vs 52 commits)"). Their `corpus/evidence/git-log-docs.html` is a captured git-log manual
  (documentation ground, matches TREESAME/--full-history queries incidentally).

## Practice-level (wave-history receipts, no standing tracked gate)

- chousa: r31 F2-1 `.ufo/waves/round-31/build/ReviewClaimsDesign31.md:15` ("freeze integrity — operative counters
  diverge from the frozen commit"); r46 `.ufo/waves/round-46/w1/ExecCounterRun.md:141-144` (F2 freeze integrity binds
  three claims; 16 edits after the counter-freeze commit); r48 `.ufo/waves/round-48/w2/VerifyFrozenClaim.md:8`
  (`git show 4bbd234:corpus/evidence/round48/claims.md | sha256sum` == on-disk; `git diff d4e6ef0..HEAD --
  tools/inference-ground.py` empty); r49 `.ufo/waves/round-49/w1/ReviewFreezeEq.md` (freeze commit precedes tool commit;
  no counter/claims byte changed after freeze); r50 `.ufo/waves/round-50/w2/R50CritErratum.md` (attacks the post-freeze
  disclosure; verdict "defect found, in the disclosure, not in the counters").
- kotoba: `corpus/lessons/round-82.md:91` freeze-ordering mined ("the round's no-harm base battery was captured after the
  plan-only commit, not before it … next round: a pre-freeze gate that refuses the plan"); `plans/round-82-addendum-1.md:13`.
- kotodama: `reports/round-14/fix-runner-hash.md:31-33,87-91` (runner bytes == admission-commit blob via
  `git log --all --full-history --format=%H -- <runner>` + sha per commit); `reports/round-14/verify-3.md:16-17`.
- kake: `corpus/lessons/round-43.md:1` ("freeze-order repair"), `round-43-verifier-spotcheck.md:201-204`.
- souji: `SCORECARD.md:1589` (r61 erratum: control receipts added by the freeze commit, proven via
  `git log --diff-filter=A --no-renames --full-history --format=%H -- census/round-60/controls/c1-do-nothing.txt`).
- audio: `corpus/live/r79-boundary/` "freeze-order" hits are PipeWire **stream** freeze experiments
  (`r79b_freeze_order.py:9,227-231`, `RECEIPTS.md:39`) — false friend, excluded.

## Mutation-culture adjacency (technique, not gate-CLI-copy)

- audio (f9da7ee97e0b): `corpus/live/r89-reverify/mut.py:2-26` ("revert-the-fix mutants on the COMMITTED bytes, run in
  scratch trees (never the frozen tree)"; M1/M2), `battery-mut.sh:2-5`, `census-summary.py:13,104-107` (mutant census
  arms), `PROVENANCE.txt:7-10` (mutant shas), `r90-simplifier/flake_census.py:16-22` (mutant trees), r94
  `r94s_evidence_arm_entailment.txt:28-29` ("A mutation tester would score the dropped arm an equivalent mutant"),
  `r79-critic/forge1-measure_audio.py` (forged driver copy). Their forges/mutants target their own measurement driver —
  same spirit as W5, different object, no CLI-entry redirection of a gate.
- No sibling uses the words "null copy"/"null mutant" for an unmutated gate copy; kengaku W5's null-CLI-copy +
  K1–K7-at-designated-fixture shape remains unique in the fleet as a *tabled* instrument.

Conclusion (b): owners = kaidoku (tracked counter family; mechanism-duplicate, object-complement) and mado (tracked
chronology gate; complement with an explicit revert-semantics contradiction). Everyone else is practice or plumbing.
Nothing to absorb; cross-cite in round 95 (R-N2/R-N3), plus the refs/replace disclosure note (R-N1).
