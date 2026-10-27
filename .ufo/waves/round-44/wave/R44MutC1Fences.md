# R44MutC1Fences — mutation test of the round-44 C1 fences (kengaku round 44, 2026-10-26)

Seat: R44MutC1Fences (mutation-tester, leaf). Target: the NEW guard code of
`plans/round44_c1_verify.py` (`pin_git`, `repo_breach`, `argv_shape_breach`, `lane_breach`,
`order_argv_breach`, plus the three new constants `GIT_TIMEOUT`/`ANCHOR_OPTS`/`ORDER_SHAPE`;
`diff plans/round43_c1_verify.py plans/round44_c1_verify.py`). Lane repo untouched: work ran on a
scratch copy; the frozen file hashed `6cf05323bafa9cdb…` before the first run and `6cf05323bafa9cdb…`
after the last (sha256, unchanged). Tools still match `PINS` (`11bb2cad…`, `948d5e1d…`).

## Method (the bounded behavioral detector)

- 18 single-edit mutants + a pristine `REF` copy, each a one-`old`-to-`new` replacement asserted to
  occur exactly once (`receipts/mutate.py`; per-mutant sha256 in `receipts/results.jsonl`).
- One detector per run, always the same: `claims/envelope.sh "$S/env" timeout 60 python3
  <variant> --battery-dir <B> --lane "$S/lane" --only U14c --work "$S/w"` — development mode,
  inside the round-44 envelope (home read-only, `~/.local/bin` digest watched). 162 recorded runs,
  **0** with a `CHANGED`/`INVALID` envelope digest (`grep -l 'CHANGED\|INVALID' out/*.txt | wc -l` → 0).
- Batteries B: the six frozen hostile modules `claims/hostile/f1…f6` (one per dir), the honest
  witness `claims/witness/w_u.py`, and ten drafted fixtures (below). REF baseline: all six hostiles
  REFUSED with their designed messages, witness ADMITTED (`BATTERY fixtures=6 wrong=0 …
  MUTANTS total=1 killed=1`), every drafted hostile REFUSED, the drafted honest fixture ADMITTED.
- A guard mutant is **caught** when a hostile module is admitted or stalls (hang = the F4 stall
  returns), or an honest fixture is refused. Everything ran under `S=/fast/scratch/hyaku/kengaku-r44/R44MutC1Fences`,
  lane clone `$S/lane` (`rev-parse --show-toplevel` verified = `$S/lane`), `TMPDIR=$S`.

## Result table (18 mutants: 15 caught, 3 survived)

| id | single edit (function: what broke) | pristine → mutated on the six hostiles + witness | caught by | verdict |
|---|---|---|---|---|
| PG1 | `pin_git`: drop `timeout=GIT_TIMEOUT` | all six REFUSED, witness ADMITTED (no hostile blocks any `pin_git` call) | draft **f4b** (decoy repo, FIFO `.git/config`): REF `decoy/git hung` after 30 s → PG1 **HANG** rc=124 | caught |
| PG2 | `pin_git`: drop `GIT_CEILING_DIRECTORIES` | all six REFUSED, witness ADMITTED (every hostile repo is valid, discovery stops at itself) | draft **hceiling** (honest: valid repo AT d's parent + empty `d/broken/.git` inside): REF ADMITTED → PG2 REFUSED `broken/rev-parse --show-toplevel=<parent>` — honest fixture refused | caught |
| PG3 | `pin_git`: `stdin=None` (inherit) | identical output everywhere | — | **survived** (null: no parent-side git command reads stdin; observable only if the counter's own stdin were hostile) |
| GT1 | `GIT_TIMEOUT = 30` → `0` | witness REFUSED `u3-row-path-binds … --lane git hung` | witness | caught |
| OS1 | `ORDER_SHAPE` pair order swapped | witness REFUSED `u14c … not the contract shape ['--lane','--receipt','--claims']` | witness | caught |
| AO1 | `ANCHOR_OPTS` drops `--lane` | witness REFUSED `anchor argv token '--lane' is not an exact option` | witness | caught |
| RB1 | `repo_breach`: `.git` FILE check off | f1 still REFUSED — `lane_breach`'s `--absolute-git-dir` half fires first (f1 is double-covered); witness ADMITTED | draft **f1b** (gitdir redirect with BOTH rev-parses inside d): REF `./.git is a file (gitdir redirect)` → RB1 ADMITTED (`killed=0`, exit 1) | caught |
| RB2 | `repo_breach`: 200000-entry bound off | all six REFUSED (no hostile builds a big tree), witness ADMITTED | draft **f12** (200050 dirs): REF `fixture tree exceeds 200000 entries` → RB2 ADMITTED | caught |
| RB3 | `repo_breach`: alternates check off | **f5 ADMITTED** (`BATTERY fixtures=1 wrong=0 … killed=1`) | f5 | caught |
| RB4 | `repo_breach`: config-include check off | f4 still REFUSED — `lane_breach`'s rev-parse follows the FIFO include and its own 30 s timeout refuses (`--lane git hung`); witness ADMITTED | draft **f4c** (include → PLAIN file outside d): REF `lane/.git/config carries an include` → RB4 ADMITTED (`wrong=0`, exit 1) | caught |
| RB5 | `repo_breach`: rev-parse containment (`ok`) off | all six REFUSED, witness ADMITTED — f2's escape is refused by `lane_breach` before `repo_breach` runs | — | **survived** (redundant: every reachable toplevel/gitdir escape also fires RB6, `lane_breach`, RB1 or the `.git`-symlink check; the one candidate primitive, `.git/commondir`, makes git reject the repo outright — measured, `exp2` §A: `fatal: not a git repository`, rc=128) |
| RB6 | `repo_breach`: `core.worktree` value leg off | f2 still REFUSED (its refusal line is `lane_breach`'s `--show-toplevel`), witness ADMITTED | draft **f2c** (bare gitdir at `d/r/.git` + `co.re.worktree ../wt`): toplevel fails rc=128 (leg RB5 quiet), REF `r/core.worktree=../wt` → RB6 ADMITTED | caught |
| AS1 | `argv_shape`: order shape off | f3 REFUSED by accident — `SETUP '--claims'` (the `vals[opt]` KeyError in `order_argv_breach`), not by the guard; witness ADMITTED | draft **f3c** (extra trailing token, all values pair): REF `not the contract shape` → AS1 ADMITTED | caught |
| AS2 | `argv_shape`: anchor exact-option check off | identical admission decisions (witness ADMITTED) | draft **f7** (`--verb` abbreviation): REF `token '--verb' is not an exact option` → AS2 `SETUP '--verb'` (KeyError in the consume step) | **survived** (equivalent-null: refusal message changes, admit/refuse decisions do not — any unknown anchor token KeyErrors at `ANCHOR_OPTS[t]`) |
| AS3 | `argv_shape`: value flags consume 1 token | witness REFUSED `anchor argv token '<path>' is not an exact option` | witness | caught |
| LB1 | `lane_breach`: containment off | **f6 ADMITTED**; f1's refusal moves to `repo_breach`'s file check (cross-evidence of f1 double-cover) | f6 | caught |
| LB2 | `lane_breach`: drop its own timeout | **f4 HANG** rc=124 (rev-parse follows the FIFO include, nothing kills it) | f4 (stall) and draft **f8** (`--lane` repo itself has FIFO config): REF `--lane git hung` after 30 s → LB2 HANG rc=124 | caught |
| OA1 | `order_argv`: HEAD-blob leg off | all six REFUSED (f3 is refused by the shape leg first), witness ADMITTED | draft **f3b** (exact contract argv, `--claims` is a TREE at HEAD): REF `--claims … is a tree at HEAD, not a blob` → OA1 ADMITTED (with `wrong=1`) | caught |

Caught: 15/18 — 7 by the frozen six+witness alone (RB3, LB1, LB2, GT1, OS1, AO1, AS3), 8 only after
drafting the missing fixture (PG1, PG2, RB1, RB2, RB4, RB6, AS1, OA1). Survived: 3 (PG3, RB5, AS2),
each a limit, not a fixable gap — see below.

## Drafted fixtures (all in `drafts/`, each run against pristine + its target)

| draft | targets | pristine | target mutant |
|---|---|---|---|
| f1b_gitdir_inside | RB1 | REFUSED `.git is a file (gitdir redirect)` | ADMITTED |
| f2c_bare_worktree | RB6 | REFUSED `r/core.worktree=../wt` | ADMITTED |
| f3b_tree_exact | OA1 | REFUSED `is a tree at HEAD, not a blob` | ADMITTED (`wrong=1`) |
| f3c_extra_token | AS1 | REFUSED `not the contract shape` | ADMITTED |
| f4b_decoy_fifo | PG1 | REFUSED `decoy/git hung` (~30 s) | HANG rc=124 |
| f4c_plain_include | RB4 | REFUSED `carries an include` | ADMITTED |
| f7_anchor_abbrev | AS2 (demonstrator) | REFUSED `not an exact option` | REFUSED by KeyError accident |
| f8_lane_fifo | LB2 | REFUSED `--lane git hung` (~30 s) | HANG rc=124 |
| f12_wide | RB2 | REFUSED `exceeds 200000 entries` | ADMITTED |
| hceiling_above | PG2 (honest-direction) | ADMITTED (`wrong=0`) | REFUSED `--show-toplevel=<parent>` — honest refusal |

All ten dodge the counter's SIDECHANNEL token list (e.g. `"co"+"re.worktree"`), as the frozen
hostiles do. Note: frozen hostile `f6_above.py` itself trips the heuristic (`sidechannel=1`,
token `inspect`) — pre-existing, cosmetic, does not affect admission.

## Findings for the L1 (counter improvement candidates; I edited nothing)

1. **f4 is stopped twice, f1 twice, f2 by the wrong guard.** f4's include is refused by the include
   leg AND (if that leg dies) by `lane_breach`'s timeout; f1 by `lane_breach --absolute-git-dir` AND
   `repo_breach`'s file check; f2's SETUP line is `lane_breach`'s, so `repo_breach`'s rev-parse
   containment (RB5) is shadowed for any `--lane` repo. RB5 is back-to-back redundant with RB6 over
   every reachable surface (`.git/commondir`, the only core.worktree-free escape candidate, makes
   git refuse the repo — measured). Redundancy is defense in depth, but it hides which fixture
   actually exercises which leg; a per-leg hostile (like my drafts) is the only way to see it.
2. **AS2's anchor leg fails soft by accident.** With the token check off, the consume step
   `ANCHOR_OPTS[t]` raises KeyError and `build_battery`'s `except` turns it into a SETUP refusal —
   same decision, different mechanism. A `.get(t)`-style consume (refusing unknown tokens at the
   consume step by design) would make the two legs independent. AS1 shows the same pattern for
   order (`SETUP '--claims'`).
3. **The timeout fences are the only stall guards and both are load-bearing**: PG1/LB2 mutants
   reintroduce unbounded stalls that only the two FIFO drafts observe; no frozen hostile hangs under
   the round-44 counter (f4's round-43 `exit=124` became an instant include refusal).
4. **PG3 (stdin) is unobservable in this harness** — nothing on the parent side reads stdin; the
   fence matters only if the counter itself were driven from a hostile pipe.

## Evidence

- `receipts/results.jsonl` — 162 rows (mutant, battery, rc, verdict, SETUP/BATTERY line).
- `receipts/` — every run's full output including its ENVELOPE lines (all `unchanged` digests),
  plus `mutate.py` (mutant table + sha256s) and `driver.py`.
- Design experiments (`exp`, `exp2`, envelope-wrapped): FIFO `.git/config` blocks even
  `git rev-parse --show-toplevel` (rc=124 at 5 s); `.git` file redirect keeps both rev-parses
  inside d; bare+`co.re.worktree` fails toplevel rc=128 while `config --get` returns the value;
  `.git/commondir` is not honored through discovery (`fatal: not a git repository`).
- Scratch: `/fast/scratch/hyaku/kengaku-r44/R44MutC1Fences` (removed after the report; no lane,
  fleet, or home writes; no pacman/uv installs made).

VERDICT: fence-mutants-caught-15/18
