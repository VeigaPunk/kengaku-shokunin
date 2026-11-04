# Round 78 — kengaku (2026-11-04 UTC)

Base `3ae0ab54` (round-77 verifier spot-check). Freeze `2f9eeafb` (two claims, two counters, the
selected-member ledger, the three `SKILL.md` class-row pointers). Repair `cd2e25bb` (re-stamp driver
and its spec) and `f20a2f6f` (the 16 round-77 receipts located). R78-C1 targets coverage (lowest
non-retired axis, L0-capped at 7): the three partially-executed grader classes become a
machine-checked 12-member ledger. R78-C2 targets calibration (held at ceiling 10, exercised): every
verdict-bearing round-77/78 receipt becomes self-locating at its own stamp, and the round-77
closure's D1/D2/D3/D5 are repaired through it.

## Gate

- **S254 admitted** for the untracked-file semantics that make `WORKTREE clean` a claim about
  untracked paths and not only tracked ones. URL opened live by L1 `KengakuR78` this round:
  `https://git-scm.com/docs/git-status`. Access date 2026-11-04 UTC. Capture
  `corpus/evidence/round78/sources/git-status.html`, HTTP 200, 100 062 bytes, sha256
  `22ff28ff73f83696c4a503e9c92e7a15f4ded2f91d96cc5668ee79db0a1b0180`. Located quote, capture
  lines 2322–2324, 17 words: **"Show untracked files. The mode parameter is used to specify the
  handling of untracked files."** Kind `docs`, tier A for untracked-reporting semantics. Registry
  change: absent → S254 `mined`, recheck `on-release`, used-by `corpus/lessons/round-78.md`,
  `plans/round-78-claims.md`.
- **S255 admitted** as an `own-work` row for the population the C1 ledger expands: the round-62
  census receipt `corpus/evidence/round62/class-survey.txt` (sha256
  `ee30c6984c13985fe3efaa2d81c908b915da0f178ce5ca267bc0f0a37cd45613`, anchor its `CLASS … members=`
  and `EXECUTED-COVERAGE` lines). Quote: `EXECUTED-COVERAGE executed=17 classified=17
  classes-covered=12 classes-uncovered=network-service,process-environment,db-state,container-image`.
  `own-work` is a listed contract kind and tier A because the lane can re-run the instrument that
  produced it (`plans/round62_c1_class_survey.py`). Status `mined`, recheck `90d`, used-by as above.
- **Reject candidate:** "a class count in a prose table is evidence of class membership." The
  census receipt carries the member lists; a `k of n` cell does not. Flip: name every member and
  resolve one receipt per executed member (`plans/grader-selected-members.json`, R78-C1).
- **Reject candidate:** "a `LANE_TIP` line locates a receipt." The line alone says nothing about the
  tool bytes or the worktree state that produced the numbers. Flip: `TOOL` + `TOOL_SHA` recomputed at
  that tip, plus `COMMAND` (R78-C2). The control receipt `c2-control-stamp-only.txt` is the flip in
  action: trusting the stamp reaches `located=6` while four real defects remain.
- **Assimilation: none.** `/home/vgpnk/Projects/shokuknow/merge/kengaku/` was not adopted; the mass
  id drift stays open at L0 `kengaku | round-54`. `considerthese/2026-10-26.md`: proposals 1 and 3
  remain implemented from earlier rounds; proposal 2 (`tb2_grader_admit`) is still open
  (`grep -rn 'tb2_grader_admit' plans corpus SKILL.md` hits only `corpus/lessons/round-66.md:332`)
  and is not mined this round — no implementing artifact exists and it serves neither frozen claim.
- Knowledge entries: none admitted (both claims are instrument and ledger work; no new domain fact).

## Census and instrument readings

- `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → rc 0 at round start
  (245 rows, 25 `W04`, `/fast/scratch/hyaku/kengaku-r78/census-start.txt`) and rc 0 at round end
  (247 rows, same 25 `W04`, `corpus/evidence/round78/census-after.txt`).
- R78-C1 before (`--rev 3ae0ab54`, `corpus/evidence/round78/c1-before.txt`): `UNIVERSE classes=3
  members=12 pairs=13`, `LEDGER rows=0`, `DEFECTS n=21`, `TARGET … unaccounted=12 unbacked=0`,
  rc 1. After (`c1-after.txt`): `LEDGER rows=12 executed=7 unexecuted=5`, `DEFECTS n=0`,
  `TARGET classes=3 members=12 executed=7 unexecuted=5 unaccounted=0 unbacked=0`, rc 0.
- R78-C2 before (`--rev 3ae0ab54`, `c2-before.txt`): `UNIVERSE dirs=2 receipts=16`, `DEFECTS n=29`,
  `TARGET receipts=16 located=2 unlocated=14`, rc 1 — 11 `TOOL-UNNAMED`, 10 `COMMAND-ABSENT`,
  4 `PASS-UNLOCATED`, 2 `WORKTREE-ABSENT`, 2 `TOOL-UNPINNED` (the final block model; the first
  reading, 27/3/13, was taken before the parser read the last stamp block). After the repair (`c2-after.txt`): `DEFECTS n=0`,
  `TARGET receipts=<R> located=<R> unlocated=0`, rc 0.
- Batteries: C1 `SELFTEST cases=8 red=7`, `MUTANTS real=6 killed=6 survived=0`, control
  `target_reached=False`. C2 `SELFTEST cases=7 red=6`, `MUTANTS real=6 killed=6 survived=0`, control
  `stamped=6 located=6 real_defects=4 target_reached=False`.

## Mistakes

| id / class | evidence pointer | captured-by | fix / disposition |
|---|---|---|---|
| M78-1 stale-premise | `corpus/evidence/round77/c1-before.txt` printed `WORKTREE clean` for a gate that did not exist at `07c97fcd` (supplied untracked); its round-78 re-stamp block records the correction | `none` until this round — the round-77 closure saw it (D5) but no committed gate priced it | `plans/round78_c2_stamp_location.py` leg `SUPPLIED-BUT-CLEAN` fires exactly on that pair; the receipt now carries `TOOL-SUPPLIED` + `WORKTREE dirty` in its last stamp block |
| M78-2 number-drift | `corpus/evidence/round77/c1-selftest.txt` stamped `LANE_TIP 51ffc14f` with `TOOL_SHA a4777acf…`, while the counter at `51ffc14f` hashes `5a507c08…` — the pin belongs to `4f2ff9be` | R77-D2 (outside this lane) — the class had no in-repo counter | re-minted at `cd2e25bb` through `plans/round78_restamp.py`; the C2 gate recomputes `TOOL_SHA` at the receipt's own stamp (`TOOL-DRIFT`) |
| M78-3 vacuous | my own C1 `COVERAGE` leg compared `covered_census` against `covered + promoted` over the three-class ledger, so it could never fail; the mutant matrix reported `MUTANT coverage-regression SURVIVED` | the round's own `--mutants` matrix, before the claim was measured | leg replaced by a per-class check (`k>0` requires a ledger-backed executed member); the mutant now kills on `COVERAGE-REGRESSION` |
| M78-4 reference-drift | `corpus/evidence/round77/exec-attrib-calibration.txt` and `exec-state-check.txt` both pinned `TOOL_SHA 78f12c7e…`, which matches neither tool at their stamp (`attrib_calibration.py` `6656c0b5…`, `state_check.py` `4aa47a63…` at `07c97fcd`) | `none` — the round-77 receipts were not audited for digest identity | re-stamped append-only with the digest computed at `07c97fcd`; recorded as a named limit of the old receipts |
| M78-5 landing | producing the round-78 receipts from one clone made every receipt after the first stamp `WORKTREE dirty` (the driver writes into the tree it measures) | the driver's own `WORKTREE` line on the first batch | one fresh `git clone --shared` per receipt; every round-78 receipt stamps `WORKTREE clean` |

## Limits

- R78-C1 accounts for the five unexecuted members; it does not replay them. A replay is the next
  coverage move, one member per round as in rounds 63–72, and `filter-js-from-html` (selenium),
  `git-multibranch` (apt/ssh/nginx), `headless-terminal` (candidate library), `install-windows-3.11`
  (qemu) and `query-optimize` (external sha-pinned DB + median-timing leg) each need a surface the
  lane does not have today.
- The reason detectors are line-regex features over stored grader bytes: they price the mechanism a
  reason names, not the whole task. A member could be replayable in a way the detector's pattern does
  not anticipate; the counter cannot see that.
- R78-C2 checks stamps, not predicate truth. A receipt whose `TOOL_SHA` recomputes but whose numbers
  were produced by other inputs still passes; the round's own `exec-*` receipts are the closest live
  example (M78-4).
- `LANE_TIP` names the revision whose tool bytes and inputs were measured; the receipt file itself
  lands in a later commit, so the gate does not require the receipt to exist at its own stamp. A
  reader recomputes the tool digest there instead.
