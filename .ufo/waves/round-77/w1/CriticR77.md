# CriticR77 — frozen-claim falsification

Axes: **coverage (C1)** and **calibration (C2)**. Review only; no adjudication, integration, production edits, git mutations, installs, or external runtime delegation.

## Apparatus and execution

Read the entire frozen claims file first. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format=%H -- plans/round-77-claims.md` exited 0 and printed `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`. Experiments subsequently measured worktree tip `8da90eb7299435aceb9466d70344bba7046094b2`; no claim that this is the final landing tip.

Both counters were read; cited code was located with the grep tool. Harness command: `python3 /fast/scratch/hyaku/kengaku-r77/CriticR77/attack.py`, process exit 0. Individual frozen `emit` return codes below are printed as `RETURN`. Harness substitutes only Reader.get input documents; original census, resolution, ancestry, SHA reads, target comparison and emit functions run unchanged against the real lane/host. Thus these are isolated input-overlay counterexamples, **not actual landing CLI receipts**. No fake counter result or ancestry function is installed. Full harness retained below because scratch is deleted at close.

## 1. Reachability without the work

### C1: 27 remote rows lose; 27 duplicate paths plus one remote catchall win

`C1-27-remote`: retain all 33 old anchored declarations, add 27 dated remote rows plus one path row. Observed `SURFACES total=28 present=1 absent=0 remote=27`, `UNLISTED n=0`, `RESOLVED live=1`, `AGREE agree=28 disagree=0`, `DEFECTS n=0`, `PREDICATE R77-C1 fail`, RETURN 1. Literal 27-remote shortcut does **not** meet frozen target.

Cheaper successful workaround: retain those older declarations; add 27 differently named `path` rows all probing existing `PROVINCE.md`, plus one `remote` row containing every older first-anchor token (local files and endpoints included). Every Supersedes cell is `unrelated`. Observed `SURFACES total=28 present=27 absent=0 remote=1`, `UNLISTED n=0`, `RESOLVED live=27`, `AGREE agree=28 disagree=0`, `DEFECTS n=0`, **`IDENTITIES n=2 unique=2`**, `PREDICATE R77-C1 pass`, RETURN 0. All 33 older anchored declarations remain, yet no old target needs probing; no hash/count/exec rows exist. Frozen numeric target admits this counterexample.

Evidence: C1 lines 407–409 return remote without checking token type; lines 469–471 deduplicate identities into a set but increment live by row; lines 515–526 credit any anchor appearing in any canonical row, independent of resolver kind and Supersedes. Duplicate names were not required. Thus declared coverage and actual resolved coverage are separate authorities.

Smallest safe correction (for adjudicator/integration owner, not performed): bind every carried old declaration to a validated typed canonical identity; validate Supersedes; reject duplicate resolved identities and remote classification of local anchors. Count only independently resolved carried identities. Since the apparatus is frozen, these defects cannot be repaired by silently substituting a stronger counter this round.

### C2: fabricated stamps and unrelated historical evidence meet the whole target

`C2-fabricated-receipts-unrelated-evidence`: two identical invented V1 documents contain only `LANE_TIP <current ancestor>` and actual SHA256 of the round-76 tool at that tip. No battery output/tallies. Three identical invented V7 documents contain only `LANE_TIP <tip>` and `EXIT 0`: **no TOOL_SHA and no PREDICATE line**. Synthetic correction/registry lines supply the exact other leg tokens. Seven ledger rows all close at pre-round base `07c97fcd` citing the same unrelated, genuinely committed literal `## Surfaces` in `PROVINCE.md`; their check is `grep "Surfaces" PROVINCE.md`.

Observed V1–V7 all `ok`; all seven `LEDGER R76-Vn ok close=07c97fcd evidence=PROVINCE.md`; `SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0`, `DEFECTS n=0`, `PREDICATE R77-C2 pass`, RETURN 0. No claimed rerun occurred.

Exact single-byte-identical receipt shared across V1 **and all V7 paths**, including V1's TOOL_SHA, does not pass: `C2-one-identical-sha-receipt` prints V1 ok but V7 TOOL_SHA mismatch, legs_passed=6 wrong=1, RETURN 1. Successful bypass requires two trivial payload variants, not literally one shared payload for every path. One payload suffices for both V1 paths; another suffices for all three V7 paths.

Evidence: C2 lines 191–195 compare V1 hashes but never require selftest/mutant result numbers; lines 292–298 make SHA optional and check predicate quality only if a predicate exists. Lines 370–372 require literal inclusion but never tie the literal to that finding or its leg. Claims lines 82 and 88–89 require stamps and passing rerun predicate, so missing V7 SHA/predicate is a **fixable contract defect**, not just a tradeoff. Requiring actual receipt content and binding each ledger id to its correct discharge evidence are smallest safe corrections. Honest-run provenance is separately a stated reviewer boundary: even mandatory correct hashes are freely forgeable; do not claim they prove execution. Frozen claims' rejected-provenance discussion does not make hash equality causal evidence.

## 2. Do-nothing base controls

Executed each command with absolute lane/script paths, no source substitution:

- `python3 plans/round77_c1_declared_surfaces.py --lane . --rev 07c97fcd` (paths expanded): exit 1; `CANONICAL source=none rows=0`, `UNLISTED n=33`, `RESOLVED live=0`, `AGREE agree=0 disagree=0`, `DEFECTS n=34`, `PREDICATE R77-C1 fail`.
- `python3 plans/round77_c2_defect_discharge.py --lane . --rev 07c97fcd` (paths expanded): exit 1; `SCOPE ids=7 registered=0 closed=0 open=0 discharged=0 legs_passed=0 legs_pending=2 wrong=12`, `DEFECTS n=12`, `PREDICATE R77-C2 fail`.

Neither do-nothing control reaches its target. Counter TARGET lines alone are unconditional specifications, not measurements; the passing predicate and measured fields matter.

## 3. Axis naming and saturation

Read SCORECARD.md lines 239–250 and located coverage/calibration with grep. Exact deciding rubric at line 247:

> | coverage | every surface the corpus *describes* is indexed **and** every index row exists on disk (both directions); `PROVINCE.md` enumerates surfaces that resolve | unindexed files on disk; declared-but-unresolvable surfaces; a gap line contradicted by an artifact already in the repo |

C1's intended three-table completeness/supersession move fits coverage rather than merely re-running round 76's single-table gate. Base counter actually found 33 anchored declarations not carried; intended target consolidates 28 rows. That is a new denominator, not 17 new external surfaces, and no scalar rise above the stated coverage-7 cap is supported. The successful two-identity counterexample means the present frozen numerical predicate does not establish that intended coverage improvement. C2's intended discharge/evidence-byte parity fits calibration (rubric line 245); no inference of improvement beyond ceiling 10 follows.

## 4. Separability

Harness `separable-C1-inventory-missing-C2` removes all canonical inventory bytes while retaining the shared capability name: C2 still prints full target and pass, RETURN 0. Companion negative run `broken-C1-of-separable-pair` on that PROVINCE input gives `CANONICAL source=none rows=0`, `DEFECT CANONICAL-MISSING`, C1 fail, RETURN 1.

Harness `separable-C2-ledger-empty-C1` supplies an empty ledger alongside the passing C1 inventory: C1 still prints live=27, agree=28, defects=0 and pass, RETURN 0. Companion `broken-C2-of-separable-pair` gives all seven MISSING ledger rows and C2 fail, RETURN 1 (also V6 fails because the preserved base prose still includes the obsolete name; wrong=8, not seven). These are isolated input experiments, not proof that an unmeasured final landing passes. Shared PROVINCE capability text is retained for the C2-positive direction; deleting all PROVINCE indiscriminately is not an independence test.

## 5. Target sizing / M76-5 class

C1's `total=28`, `live=27`, `agree=28`, and even `unlisted=0` can all be manufactured by this round's own inventory writes against a single preexisting file, as the passing two-identity experiment establishes. No independent unique-surface floor or immutable supersession mapping prevents saturation. `live` is a row-loop count, not unique work.

C2's seven registered/closed/discharged rows and seven legs can be manufactured by this round's ledger/correction/receipt writes with base evidence; the full passing fabrication establishes the collision. Seven underlying ids remain historical, but the denominator being historical does not independently price their discharge. Recommended disposition is evidence to the canonical judge, not changing the frozen thresholds or claiming these frozen counters are stronger than measured.

## Reproduction harness

The following is the executed input-overlay harness (sha256 `4c0e8606c93d2b694c27b6ddd5eab1380b5f64396a6db68b8fdbc56d1c5c6f94`). To reproduce, place it in the seat's authorized scratch root and run the command above. The two companion negative calls in §4 were made through the same emit_overlay function after loading definitions without replaying preceding calls. No installation was needed.

```python
import importlib.util, pathlib, subprocess, hashlib, json, re
LANE=pathlib.Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
def module(short, suffix):
 p=LANE/'plans'/('round77_'+short+'_'+suffix+'.py')
 s=importlib.util.spec_from_file_location(short,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
c1=module('c1','declared_surfaces'); c2=module('c2','defect_discharge')
base=c1.Reader(LANE,'07c97fcd').get('PROVINCE.md')
anchors=[]
for heading,_,cells in c1.superseded_rows(c1.Reader(LANE,'07c97fcd')):
 for cell in cells:
  a=c1.first_anchor(cell)
  if a: anchors.append(a); break
# Preserve all older declarations; supersedes is deliberately false, identities duplicate.
header='\n## Declared surfaces — canonical, machine-checked\n| Surface | Kind | Anchor | Verdict | Supersedes |\n|---|---|---|---|---|\n'
remote='| Catchall | remote | '+' '.join('`'+a+'`' for a in anchors)+' | REMOTE 2026-11-04 | unrelated |\n'
paths=''.join('| Duplicate '+str(i)+' | path | `PROVINCE.md` | present | unrelated |\n' for i in range(27))
c1pass=base+header+paths+remote
remote27=base+header+'| Only live | path | `PROVINCE.md` | present | unrelated |\n'+''.join('| Remote '+str(i)+' | remote | '+' '.join('`'+a+'`' for a in anchors)+' | REMOTE 2026-11-04 | unrelated |\n' for i in range(27))
def emit_overlay(m, overlay, label):
 original=m.Reader
 class Overlay(original):
  def get(self,rel): return overlay[rel] if rel in overlay else super().get(rel)
 m.Reader=Overlay
 try:
  print('EXPERIMENT',label)
  rc=m.emit(LANE,'worktree',None); print('RETURN',rc)
 finally: m.Reader=original
emit_overlay(c1,{'PROVINCE.md':remote27},'C1-27-remote')
emit_overlay(c1,{'PROVINCE.md':c1pass},'C1-duplicate-paths-remote-catchall')
r=c2.Reader(LANE,'worktree'); tip=r.tip
sha=r.blob_sha(tip,c2.R76_TOOL)
v1='LANE_TIP '+tip+'\nTOOL_SHA '+sha+'\n'
v7='LANE_TIP '+tip+'\nEXIT 0\n'
ledger=[]
for i in range(1,8): ledger.append(json.dumps({'id':'R76-V'+str(i),'status':'closed','close_commit':'07c97fcd','verified_at':'2026-11-04','check':'grep "Surfaces" PROVINCE.md','evidence_path':'PROVINCE.md','evidence_literal':'## Surfaces'}))
c2data={c2.LEDGER:'\n'.join(ledger),c2.R76_C1_SELFTEST:v1,c2.R76_C1_MUTANTS:v1,c2.SKILL:'round76-c1-surface-resolver cases=12 red=11 9/9 cases=14 red=13 12/12 NONLOCAL-ANCHOR ESCAPE-ANCHOR OVERFLOW-ANCHOR MALFORMED-DATE DUPLICATE-SURFACE MANIFEST-DRIFT EMPTY-SCOPE LEG-PENDING NEGATED-DISCHARGE',c2.LOG:'2026-11-04 agree=9 disagree=2 agree=8 disagree=3\nSecond-reviewer classes',c2.LESSON76:'2026-11-04 agree=9 disagree=2 agree=8 disagree=3',c2.SCORECARD:'2026-11-04 wrong=12 wrong=13\nprovince-surface-resolver-table-anchored',c2.PROVINCE:'province-surface-resolver-table-anchored',c2.LESSON77:'tb2_grader_admit open'}
for rel,tool in c2.RERUNS.values(): c2data[rel]=v7
emit_overlay(c2,c2data,'C2-fabricated-receipts-unrelated-evidence')
# Strict single shared receipt with TOOL_SHA cannot satisfy four differing tool hashes.
shared=dict(c2data)
for rel,tool in c2.RERUNS.values(): shared[rel]=v1+'EXIT 0\n'
emit_overlay(c2,shared,'C2-one-identical-sha-receipt')
# Independent deletion: broken C1 canonical inventory, C2 still green with capability intact.
emit_overlay(c2,{**c2data,c2.PROVINCE:'province-surface-resolver-table-anchored\n'},'separable-C1-inventory-missing-C2')
emit_overlay(c1,{'PROVINCE.md':c1pass,c2.LEDGER:''},'separable-C2-ledger-empty-C1')

```
