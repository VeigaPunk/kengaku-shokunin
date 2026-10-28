# R50SentWaveHygiene — wave boundary audit (writes, secrets, /tmp, fleet/sibling, shared paths, git env, production edits)

Seat: R50SentWaveHygiene (critic), serving R50-C1 (novelty) + R50-C2 (calibration).
Item: audit the whole wave for boundary violations; one report with a per-seat disposition table and the exact
commands used. Read-only against the lane except this file and my scratch.

```
REV d6f2fce9889f429162c12f851bae41891bedf5cd   lane tip when the audit started (export 14:39:11)
REV d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78   tip at the first full measurement (export 14:39:56)
REV 3dda12f98a872e8863e125140bee1874454bb6fa   tip when the receipt re-run landed
REV 61f6257c80ad74101d02a4da8fcead4cdb9cee65   tip when the hardened counter landed
REV d52243afab26962c4ba2f469bf7917a491ce3870   tip when this report was first written
REV fa16b87                                     tip at post-audit verification (85102cf receipt, 8acd0f8/fa16b87 addenda)
REV 297e17927ba9342a87ba27a48cc5270a001de7cb   final state verified: receipt notes, F5 closed, receipt bytes unchanged
                                                F1/F2/F5 re-checked there and recorded as resolved (see those findings)
FREEZE 3b02d573d58cc6d2e0d27ef92ac0815354912252 is an ancestor of d45c5bb, d52243a, fa16b87 and 297e179
      (`git merge-base --is-ancestor` exit 0 for each; checked before any measurement and again at verification);
      the receipt's revision 61f6257 is likewise an ancestor of the final tip
SNAPSHOT 2026-10-28T14:50:08-03:00 (per-seat table) and 14:52 (re-count); the wave was still live
```

The lane advanced twice **during** this audit (d6f2fce -> d45c5bb at 14:39:56, then d45c5bb -> 3dda12f -> 61f6257
-> d52243a by 14:51). Every finding below names the revision it was measured on.

## Axes named

- **A1 — provenance of the C1 instrument (novelty).** Does the artifact the claim scores exist, at the revision the
  claim names, with no unrecorded instrument standing beside it?
- **A2 — artifact identity (calibration).** Are the wave's pointers aimed at files seats actually wrote, in the
  paths their items authorized, with no second writer behind a shared path?

## Method

Read-only against a `git clone --shared` of the lane in scratch; the live checkout was queried only with
`GIT_OPTIONAL_LOCKS=0 git status/log/show/rev-parse` and `sha256sum`/`stat` (no index refresh, no mutation).
Attribution comes from the harness transcripts of this wave's session
(`~/.omp/agent/sessions/-Projects-shokunin/2026-10-28T14-01-34-216Z_01a182d0-…/`), which record every `toolCall`
(tool name + arguments) per agent: 55 `R50*` agent transcripts (39 originals + 16 retries) and 58 279 toolCall
records in the session directory.

## Commands run (verbatim; the load-bearing ones)

```bash
# revision + ancestry (read-only, before any measurement)
git -C <lane> rev-parse HEAD
git -C <lane> merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD && echo ANCESTOR_OK
git -C <lane> reflog --date=iso -8
git -C <lane> log --format='%h|%an <%ae>|%cn|%s' 3b02d57..d45c5bb

# clone for measurement
S=/fast/scratch/hyaku/kengaku-r50/R50SentWaveHygiene; TMPDIR=$S
git clone --shared -q <lane> $S/lane-clone && git -C $S/lane-clone checkout -q 3b02d573d58cc6d2e0d27ef92ac0815354912252

# write-scope state of the live lane
GIT_OPTIONAL_LOCKS=0 git -C <lane> status --porcelain=v1 --untracked-files=all
sha256sum <lane>/plans/round50_c1_verify.py
GIT_OPTIONAL_LOCKS=0 git -C <lane> show HEAD:plans/round50_c1_verify.py | sha256sum
GIT_OPTIONAL_LOCKS=0 git -C <lane> show 3dda12f:plans/round50_c1_verify.py | sha256sum
GIT_OPTIONAL_LOCKS=0 git -C <lane> show 61f6257:plans/round50_c1_verify.py | sha256sum

# wave-dir inventory vs the dispatched spec
python3 <scratch>/map_spec_vs_files.py            # parses w1-spec.json, extracts "Report path (MUST exist at yield)"
ls -1 <lane>/.ufo/waves/round-50/w1 | wc -l
find <lane>/.ufo/waves/round-50 -type l -printf '%p -> %l\n'
find <lane>/.ufo/waves/round-50 -not -user vgpnk -printf '%u %p\n'

# secrets / env / tmp / fleet / pacman sweeps over every wave artifact
grep -rnIE 'ghp_[A-Za-z0-9]{20,}|github_pat_|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN (RSA|OPENSSH|EC|PGP) PRIVATE KEY|xox[baprs]-|AIza[0-9A-Za-z_-]{30,}' <w1> <claims>
grep -rnIiE 'passw(or)?d|credential|api[_-]?key|secret|bearer |netrc|\.git-credentials' <w1> <claims>
grep -rnI -E 'GIT_CONFIG_GLOBAL|GIT_CONFIG_NOSYSTEM|GIT_AUTHOR_(NAME|EMAIL)|GIT_COMMITTER_(NAME|EMAIL)|GIT_DIR=' <w1> <claims>
grep -rnoI 'export GIT_[A-Z_]*' <w1> <claims>
grep -rlI '/tmp/' <w1> <claims>; grep -rIoI '/tmp/[A-Za-z0-9._/-]*' <w1> <claims>
grep -rnI 'pacman' <w1>
grep -rhoIE '/home/vgpnk/Projects/shokunin/[A-Za-z0-9_.-]+' <w1> | sort | uniq -c
grep -rnIE '(cp|mv|install|rsync|tee|patch|git apply)[^\n]{0,120}(kengaku-shokunin/(plans|corpus|scripts))' <w1>
grep -rnIE '>\s*/home/vgpnk/Projects/shokunin/kengaku-shokunin/(plans|corpus|scripts|SCORECARD|LOG|SKILL|PROVINCE|SHONEN)' <w1>
grep -rnIE 'git\s+(-C\s+\S+\s+)?(commit|push|stash|checkout|reset|clean|rebase|cherry-pick|merge|add|rm |mv )' <w1>
grep -rniE '<alias-pattern-set>' <w1>          # the host's own alias alternation; elided here per the routing rule

# scratch discipline
find /fast/scratch/hyaku/kengaku-r50 -maxdepth 5 -path '*/.git/config' -exec git config -f {} --get remote.origin.url \;
for d in /fast/scratch/hyaku/kengaku-r50/*/lane*; do [ -f "$d/.git/objects/info/alternates" ] && echo SHARED $d || echo FULL $d; done
du -sh /fast/scratch/hyaku/kengaku-r50/*

# fleet root and sibling lanes (read-only)
GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin status --porcelain=v1
find /home/vgpnk/Projects/shokunin -maxdepth 1 -mindepth 1 -newermt '2026-10-28 14:17' -printf '%TH:%TM %p\n'
stat -c '%y %n' /home/vgpnk/Projects/shokunin/MANIFEST.json

# attribution: every edit/write tool call and every bash statement that touches a lane production path
python3 <scratch>/attrib.py     # walks 55 transcripts; prints (tool,path) for write|edit|ast_edit and
                                # bash statements whose text has a lane plans/corpus path AND a write operator
```

Tool installs this seat: **none** (nothing was needed; no pacman/uv/npx transaction attempted — pacman is paused
host-wide in any case).

## Class results

| # | class audited | result | evidence |
|---|---|---|---|
| 1 | writes outside the allowed paths (seats) | **clean** | 55 transcripts, every `write`/`edit`/`ast_edit` path is under `<lane>/.ufo/waves/round-50/w1/` or the seat's own `/fast/scratch/hyaku/kengaku-r50/<seat>`; 0 bash statements by a seat carry a lane `plans/`/`corpus/` path with a write operator |
| 2 | seats that edited production files | **clean (none)** | the only edit/write call sites on `plans/`, `corpus/` are `KengakuR50` (L1, the integrator): 17 calls incl. `round50_c1_verify.py` (1 write + 2 edits), `round50_c2_audit.py`, `honest50/*`, `controls50/*`, `round-50-claims.md`, `corpus/SOURCES.md`, `corpus/knowledge/fixture-honest-geometry.md`, `corpus/lessons/round-50.md` |
| 3 | secrets / credential material | **clean** | zero matches for the key/token/private-key pattern set across `w1/` and `claims/`; the only `credential` hit is prose (R50C1ConnOverlap quoting the fence's own limit: "not credential hygiene"), the only `password` hit is an unrelated corpus path (`tb2-password-recovery`). `shokunin.conf` was read by R50FRScribeGate (copied *into* scratch) and carries no secret material |
| 4 | `/tmp` citations | **clean for reports** | no `.md` in the wave dir cites `/tmp`; 3 code/receipt files carry the literal: `R50C1ExecSealedAudit/audit_sealed.py` (host-marker detector, `HOST_MARKERS = (b"/home/vgpnk", b"/fast/scratch", b"/tmp/")`), `R50C1ExecSealedAudit/controls-negative.txt` (negative-control marker `/tmp/ctl-abs-marker`), `C1CritBlind6/sealed/s6_second_store_mount.py` (`/tmp/x` in a kernel-EXDEV narrative). None is used as a work directory. (The three literals are quoted as the *occurrences found*, not as evidence
locations; every evidence location in this report is a lane-tree or wave-dir path.) All round-50 committed instruments pass `--work "$S"`; `git grep '/tmp' HEAD -- plans/round50_c1_verify.py plans/round50_c2_audit.py plans/controls50` = 0 |
| 5 | fleet-repo / sibling-lane touches | **clean (reads only)** | the only non-lane host paths in the wave are `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (reads + a `validate` run against a *scratch* fleetroot, authorized by the claims' frontier step) and `shokunin.conf` (read into scratch). Fleet `MANIFEST.json` mtime moved (14:33:51) with **byte-identical content** (`git diff` empty); the fleet's own round-50 commits are the orchestrator's. `kasegi-shokunin` mtime 14:19 is that lane's own live seat (`KasegiR43`), not a kengaku write. Fleet strays (`o.bin`, `oldrep1.out`, `oldrep2.out`) pre-date the wave (2026-10-27 16:58, 2026-10-28 09:10) |
| 6 | shared writer paths | **findings F6/F7** | all 72 spec scratch paths are unique, but 16 retry agents reuse their base seat's scratch **and report** path (sequential double-write observed on `w1/R50C1CritBlind2.md`); one seat owns two deliverable dirs (`C1ExecCleanRun/` + `R50C1ExecCleanRun/`) |
| 7 | leaked git env | **clean** | no seat report contains a line `export GIT_*`; env is set per child (`env … git`, `Ctx.ENV`) or inside `mktemp -d` subshells; the L1 `unset GIT_CONFIG_GLOBAL GIT_CONFIG_NOSYSTEM` before every `jj-lane.sh commit`. The round's push breakage was diagnosed by the L1 at 14:16:46–14:16:55 from `pushdiag/lane` (see F4); no seat pushed or committed anything |
| 8 | ownership / symlinks / out-of-tree links in the wave dir | **clean** | all files owned by `vgpnk`; no symlinks anywhere under `.ufo/waves/round-50` |

## Findings

### F1 — (novelty-relevant, HIGH at measurement time, mitigated while the audit ran) the lane carried an unrecorded instrument beside the scored one

At 14:35:39 `KengakuR50` rewrote `plans/round50_c1_verify.py` **in the live lane** (`python3 - <<'PY' … build_all`
-> random per-module parent + `PAD = 8` decoys), leaving the worktree at
`850ec7906e9658344b66e319a5c902ed4403519a55f33605b6f008ae90912999` while `HEAD` still held
`d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2` (the claims' recorded repair).
`git status` at 14:39 and 14:47: ` M plans/round50_c1_verify.py` — the only tracked modification in the lane.

Status at audit close: **mitigated**. `61f6257` lands that instrument and appends a second repair row
(`d8787b34 -> 850ec79`) that states the deviation from "a repair after the first scored run is not this claim's
instrument".

Residual risk observed at 14:51, since **closed by the integrator** (verified read-only at `fa16b87`): the receipt
`corpus/evidence/round50/c1-receipt.txt` then named `REV 3dda12f98a872e8863e125140bee1874454bb6fa`, whose
`plans/round50_c1_verify.py` hashes to `d8787b34` — a revision that does **not** contain the instrument the repair
row calls "the round's scored receipt … the post-repair re-run"; a third receipt on `61f6257` had been launched at
14:50:39 but not yet copied back. At `85102cf` the receipt was replaced and now reads, exactly:

```
REV 61f6257c80ad74101d02a4da8fcead4cdb9cee65
TREE dirty=0
FENCE /fast/scratch/hyaku/kengaku-r50/receipt3/lane/plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
```

and `git show 61f6257:plans/round50_c1_verify.py` = `850ec7906e9658344b66e319a5c902ed4403519a55f33605b6f008ae90912999`.
Receipt revision and the claims row's scored instrument now name the same tree, and `61f6257` is an ancestor of the
tip (`git merge-base --is-ancestor 61f6257 fa16b87` exit 0; the freeze remains an ancestor too). **F1 is resolved.**
The one loose end that survived in the *committed* receipt was F5 (the `FENCE` line's scratch path), closed at
`297e179` by a receipt-notes file that pins the durable digests (see F5).

### F2 — the integrator's command shape writes bytecode into production directories, invisible to `TREE dirty`

`plans/__pycache__` (14:44), `plans/controls50/__pycache__` (14:17), `plans/sealed50/__pycache__` (14:35) and
`plans/honest50/{,modules/*}/__pycache__` (14:09–14:12) exist because counters were run with **cwd = the live lane**
and `--lane .` (L1 transcript, e.g. 17:11:38, 17:26:50, 17:35:43, 17:39:23). `__pycache__/` is in `.gitignore`, so
the counter's own `TREE dirty` precheck cannot see these writes — `R50C1CritIdent` independently measured the same
class inside the fixture identity and asked for it in the `skipped` set.

Correction: run integration counters from a clone, or set `PYTHONDONTWRITEBYTECODE=1` for lane-cwd runs; record
`__pycache__` in the population's skipped set (no re-freeze needed for the latter).

Status at `fa16b87` (verified read-only): the four directories this audit named are **gone**
(`plans/__pycache__`, `plans/controls50/__pycache__`, `plans/sealed50/__pycache__`, `plans/honest50/__pycache__`),
the shipped path is clone-only with `PYTHONDONTWRITEBYTECODE=1` in the harness child, and the integrator recorded the
cleanup in its report addendum instead of cleaning silently. Thirteen older `__pycache__` dirs remain under
`plans/` (`battery37–44`, `honest50/modules/{r46novel,novel48,novel49,novel50}`, `refusals46`, `sealed46`; mtimes
2026-10-26 01:46–18:04 and 14:09–14:11) — written by the population builder importing module fixtures in place, not
by the counter, and not re-creatable by the shipped path. **F2 is resolved for the class this wave introduced**; the
residual dirs are pre-wave and gitignored, so they affect reproducibility (a masked identity, `R50C1CritIdent`'s
finding) rather than write scope.

### F3 — the lane was mutated mid-wave while attack seats were measuring it

L1 writes into the live lane during the wave: `cp … fence_r50.py plans/fixture_fence.py` at 14:36:00.889;
`plans/mutants50/c1-mutants.json` overwritten at 14:31:54 and 14:32:24; `cp -n …/C1CritBlind*/sealed/*.py
plans/sealed50/` at 14:34:38. Consequence, recorded by the seats themselves: `R50C1CritIdent`'s "Addendum (written
after the lane drifted under the measurement)" and `R50C1MutBypass`'s "WORKING-TREE 850ec790… (uncommitted,
another seat; HEAD still d8787b34)". Seats that read the lane at different minutes therefore report different
digests for the same paths.

This is the integrator's prerogative, not a violation — but it costs comparability. Correction: export once per
stabilization point and keep a quiet window while attack seats read, or have the ready file advertise the exact
digests in force so a seat can tell drift from noise.

### F4 — a full (non-shared) clone sits in wave scratch

`/fast/scratch/hyaku/kengaku-r50/pushdiag/lane` has **no** `objects/info/alternates` (629 MB) — it was cloned
`--no-local` at 14:16:46 to diagnose the broken push, against the operator rule "One live clone per seat
(`git clone --shared`); never a full mirror of the lane". Every other clone in the wave scratch is `--shared`
(verified by alternates presence: R50C1ExecRepair, ExecSealedAssemble, MutHostile, RevNoHarm, FRDistillFindings,
FRScribeMistake, FRScribeSources, RevReportShape, `receipt/lane`, my own). Correction: remove it at yield (L1
scratch, not a seat's), and diagnose from a shared clone with `GIT_TRACE`.

### F5 — a committed receipt cited a scratch path that will not exist (CLOSED at `297e179`)

`corpus/evidence/round50/c1-receipt.txt` carries
`FENCE /fast/scratch/hyaku/kengaku-r50/receipt3/lane/plans/fixture_fence.py sha256=57adce4a…`; by the scratch
discipline the wave's scratch is removed at yield, so the path half is unresolvable afterwards while the sha256 is
durable.

Status: **closed by the integrator without rewriting scored bytes.** `297e179` adds
`corpus/evidence/round50/c1-receipt-notes.txt`, which declares the `FENCE` path a run-measured fact and not an
evidence pointer, records the three durable digests (`plans/fixture_fence.py` `57adce4a…`, `plans/round50_c1_verify.py`
`850ec790…`, `plans/honest50/population.txt` `b5197f94…`), and gives a lane-only reproduction command at `61f6257`.
I verified the receipt bytes are unchanged between `85102cf` and `297e179`
(`sha256 b579c5e8a5b8011cc9dff2051e04ffed2441ef1ae4c5a4ac67087712b32936ba` in both). One residual nit in the new
file: its example reproduction clones into `/tmp/c1`, and a lane clone exceeds the operator's "files under 50 MB
only" allowance for `/tmp` — the recipe should say `--work /fast/scratch/...` for both the clone and the work root.

### F6 — retries share writer paths with their originals

16 retry agents in this wave (`R50C1CritAdmitAll-2`, `R50C1CritBlind2-3`, `R50C1CritBlind4-2`, `-5-2`, `-6-2`,
`R50C1CritIdent-3`, `R50C1ExecRepairB-2`, `R50C1ExecSealedAssemble-2`, `R50C1MutBypass-3`, `R50C1RevengerIntent-2`,
`R50C2CritHash-2`, `R50C2CritScope-2`, `R50C2ExecAudit-2`, `R50C2ExecVerifyTargets-2`, `R50FRScoutGitDocs-2`,
`R50FRScribeSources-3`) reuse the base item's text, hence the base scratch path and the base report path:
`R50C1CritBlind2` and `R50C1CritBlind2-3` both issued `write .ufo/waves/round-50/w1/R50C1CritBlind2.md`. Some
retries partly escaped (`R50C1CritBlind2b`, `R50C1CritBlind4b`, `R50C1CritPopScope2` were created), but the report
path stayed shared. All observed collisions were **sequential** (no concurrent double-write), and
`R50C1ExecAlternates`' scratch — which I caught mid-teardown at 14:45:36 — was gone by 14:45:50, exactly as its
report claims. Correction: retries take suffixed scratch *and* report paths from the dispatcher.

### F7 — one deliverable, two directories

`w1/C1ExecCleanRun/` and `w1/R50C1ExecCleanRun/` both exist for the same seat (its transcript writes
`C1ExecCleanRun/receipt-base-fence.txt`); `w1/C1ExecRepair/` and `w1/C1ExecRepairB/` are short-name dirs that collide
with the `R50C1ExecRepair*` seat prefixes. Each is inside the wave dir (allowed), but the short names make ownership
ambiguous and would collide if two seats ever used the same short prefix. Correction: one directory named for the
seat.

### F8 — the routing rule's alias strings appear in an artifact

`w1/R50RevReportShape.md:50` reproduces a gate's own alias-pattern alphabet verbatim (nine alternatives, one of them
a vendor prefix). No seat is attributed a model and no route claim is made — but the host rule is "NEVER name or
record a model alias in any artifact", and a later reader cannot tell a detector's pattern list from a route record.
Correction: cite the detector by digest, or describe it as "the alias pattern set" without enumerating aliases. This
report deliberately does not repeat the list.

### Clean by direct measurement (recorded so the L1 need not re-run it)

- 0 seat writes outside `w1/` + own scratch; 0 seat edits to `plans/`, `corpus/`, `SCORECARD.md`, `LOG.md`,
  `SKILL.md`, `PROVINCE.md`, `SHONEN.md`, `.ufo/state`.
- 0 seat `git commit/push/stash/checkout/reset` against the lane: every `checkout` in a seat transcript targets
  `$S/lane`, `$S/lane-clone`, `$S/lane50`, `$S/lane-tip` or `$S/fleetroot/kengaku-shokunin`; every clone's origin is
  the lane (`git config -f <clone>/.git/config remote.origin.url`).
- 0 pacman transactions (several seats state "none"; nothing was installed wave-wide per the transcripts).
- 0 secrets, 0 `/tmp` report citations, 0 symlinks, 0 non-`vgpnk` files in the wave tree.
- The one L1 write to a wrong absolute path — `write /home/vgpnk/Projects/shogunin/kengaku-shokunin/plans/honest50/
  modules/novel50/n22_alternates_in_d.py` (transposed `shogunin`) — targeted a directory that does not exist: no
  stray tree, nothing created, and the correct path was written immediately after. Recorded because an unguarded
  absolute path in a write call is how a wave loses a file.

## Per-seat disposition

Snapshot 2026-10-28T14:50:08-03:00 (re-count at 14:52: 53/72 reports present). `report` = the file named by that
seat's `Report path (MUST exist at yield)`; `receipts` = additional artifacts in the wave dir prefixed by the seat;
`scratch` = the seat's own scratch path. Absent reports belong to seats still running (see Limits), not to settled
seats without a file. Columns `/tmp`, `export GIT_*`, `pacman`, `lane write` are the class checks of §Class results
applied to that seat's report; every seat reads `none` for `lane write` because the transcript sweep found zero.

| seat | role | report | receipts in wave dir | /tmp cite | `export GIT_*` | pacman | lane write | scratch |
|---|---|---|---|---|---|---|---|---|
| R50C1ExecRepair | executor | yes | 1 | — | — | — | none | removed |
| R50C1ExecRepairB | executor | yes | 0 | — | — | — | none | removed |
| R50C1ExecGitfile | executor | yes | 0 | — | — | — | none | removed |
| R50C1ExecAlternates | executor | yes | 0 | — | — | — | none | removed |
| R50C1ExecRefs | executor | yes | 0 | — | — | — | none | removed |
| R50C1ExecFetchHead | executor | yes | 0 | — | — | — | none | removed |
| R50C1ExecMutRebase | executor | yes | 14 | — | — | — | none | removed |
| R50C1ExecMutAttrib | executor | yes | 12 | — | — | — | none | removed |
| R50C1ExecSealedAudit | executor | yes | 1 | **/tmp** | — | — | none | removed |
| R50C1ExecPopRepro | executor | yes | 0 | — | — | — | none | removed |
| R50C1ExecCounterSelftest | executor | yes | 0 | — | — | — | none | removed |
| R50C1ExecCleanRun | executor | yes | 1 | — | — | — | none | removed |
| R50C1ScribeLimit | scribe | yes | 0 | — | — | — | none | removed |
| R50C1ScribeEntry | scribe | yes | 0 | — | — | — | none | removed |
| R50C1ScoutPrior | scout | yes | 0 | — | — | — | none | removed |
| R50C1ConnOverlap | connector | yes | 0 | — | — | — | none | removed |
| R50C1SimplBudget | simplifier | yes | 0 | — | — | — | none | removed |
| R50C1CritPredicate | critic | yes | 0 | — | — | — | none | removed |
| R50C1CritDoNothing | critic | yes | 7 | — | — | — | none | removed |
| R50C1CritAdmitAll | critic | yes | 0 | — | — | — | none | removed |
| R50C1CritPopScope | critic | yes | 0 | — | — | — | none | removed |
| R50C1CritIdent | critic | yes | 0 | — | — | — | none | removed |
| R50C1CritBlind1 | critic | yes | 0 | — | — | — | none | removed |
| R50C1CritBlind2 | critic | yes | 1 | — | — | — | none | removed |
| R50C1CritBlind3 | critic | yes | 0 | — | — | — | none | removed |
| R50C1CritBlind4 | critic | yes | 0 | — | — | — | none | removed |
| R50C1CritBlind5 | critic | yes | 0 | — | — | — | none | removed |
| R50C1CritBlind6 | critic | yes | 0 | — | — | — | none | removed |
| R50C1RevRerun | reviewer | yes | 0 | — | — | — | none | removed |
| R50C1RevClaim | reviewer | yes | 0 | — | — | — | none | removed |
| R50C1RevNoHarm | reviewer | yes | 0 | — | — | — | none | removed |
| R50C1MutBypass | mutation-tester | yes | 0 | — | — | — | none | removed |
| R50C1MutSealed | mutation-tester | yes | 0 | — | — | — | none | removed |
| R50C1MutHostile | mutation-tester | **no** | 0 | — | — | — | none | on disk |
| R50C1LabratProbe | executor | yes | 0 | — | — | — | none | removed |
| R50C1RevengerIntent | revenger | yes | 0 | — | — | — | none | removed |
| R50C2ExecAudit | executor | yes | 0 | — | — | — | none | removed |
| R50C2ExecCorrections | executor | yes | 0 | — | — | — | none | removed |
| R50C2ExecVerifyTargets | executor | yes | 0 | — | — | — | none | removed |
| R50C2RevRerun | reviewer | yes | 0 | — | — | — | none | removed |
| R50C2CritScope | critic | yes | 0 | — | — | — | none | removed |
| R50C2CritNonVacuity | critic | yes | 0 | — | — | — | none | removed |
| R50C2CritHash | critic | yes | 0 | — | — | — | none | removed |
| R50C2ScribeCorrections | scribe | yes | 0 | — | — | — | none | removed |
| R50C2RevNoHarm | reviewer | yes | 0 | — | — | — | none | removed |
| R50FRScoutGitDocs | scout | yes | 0 | — | — | — | none | removed |
| R50FRScoutAlternates | scout | yes | 0 | — | — | — | none | removed |
| R50FRScribeSources | scribe | yes | 2 | — | — | — | none | removed |
| R50FRScribeGate | scribe | yes | 0 | — | — | — | none | removed |
| R50FRScribeMistake | scribe | yes | 0 | — | — | — | none | removed |
| R50FRExecCensus | executor | yes | 0 | — | — | — | none | removed |
| R50FRDistillFindings | reviewer | yes | 0 | — | — | — | none | removed |
| R50SentWaveHygiene | critic | **no** | 0 | — | — | — | none | this seat |
| R50RevReportShape | reviewer | yes | 0 | — | — | — | none | removed |
| R50C1ExecSealedAssemble | executor | yes | 0 | — | — | — | none | removed |
| R50C1ExecRepairDiff | executor | **no** | 0 | — | — | — | none | removed |
| R50C1ExecParity | executor | **no** | 0 | — | — | — | none | removed |
| R50C1ExecCounterHygiene | executor | **no** | 0 | — | — | — | none | removed |
| R50C1CritBlind7 | critic | **no** | 0 | — | — | — | none | removed |
| R50C1CritBlind8 | critic | **no** | 0 | — | — | — | none | removed |
| R50C1CritRepairWeaker | critic | **no** | 0 | — | — | — | none | removed |
| R50C1CritMount | critic | **no** | 0 | — | — | — | none | removed |
| R50C1CritHygiene | critic | **no** | 0 | — | — | — | none | removed |
| R50C1RevBlindIndependence | reviewer | **no** | 0 | — | — | — | none | removed |
| R50C1RevParity | reviewer | **no** | 0 | — | — | — | none | removed |
| R50C1MutRepairB | mutation-tester | **no** | 0 | — | — | — | none | removed |
| R50C1MutSealedBlind | mutation-tester | **no** | 0 | — | — | — | none | removed |
| R50C1ScoutGitVersion | scout | **no** | 0 | — | — | — | none | removed |
| R50C1ScoutPrev | scout | **no** | 0 | — | — | — | none | removed |
| R50C1ScribeSealedDoc | scribe | **no** | 0 | — | — | — | none | removed |
| R50FRScoutContractV1 | scout | **no** | 0 | — | — | — | none | removed |
| R50FRScribeLesson | scribe | **no** | 0 | — | — | — | none | removed |

reports present: 53/72; absent at this snapshot: 19

Nineteen seats had no report at 14:52 and were still live (their names carry no finding here):
`R50C1ExecRepairDiff`, `R50C1ExecParity`, `R50C1ExecCounterHygiene`, `R50C1CritBlind7`, `R50C1CritBlind8`,
`R50C1CritRepairWeaker`, `R50C1CritMount`, `R50C1CritHygiene`, `R50C1RevBlindIndependence`, `R50C1RevParity`,
`R50C1MutRepairB`, `R50C1MutSealedBlind`, `R50C1ScoutGitVersion`, `R50C1ScoutPrev`, `R50C1ScribeSealedDoc`,
`R50FRScoutContractV1`, `R50FRScribeLesson`, `R50C1MutHostile`, and this seat (report = this file).
`R50C1MutHostile` is the only one of them still holding scratch (102 MB `lane` + fixtures) — expected for a live
seat, a defect only if it yields without removing it.

## Limits

1. **Attribution is transcript-based.** It covers every tool call made through this harness (55 `R50*` agents,
   58 279 `toolCall` records). A target hidden inside a helper script executed by name (e.g. `python3
   <scratch>/x.py` that opens an absolute lane path) would not appear as a path argument. I mitigated this by
   scanning *every* bash statement for a lane `plans/`/`corpus/` substring together with any write operator
   (`>`, `>>`, `tee`, `cp`, `mv`, `sed -i`, `patch`, `write_text`, `open(...,'w')`, `cat >`, `touch`): 0 hits for
   seats, all hits for `KengakuR50`. I did not disassemble scratch scripts to prove the negative absolutely.
2. **The wave was live.** 19/72 seats had not yielded at 14:52; the lane moved from `d6f2fce` to `d52243a` during
   the audit. Every count above is timestamped; a later re-run will differ.
3. **I did not re-derive the claims' numbers.** Whether `HONEST 126/126`, `REFUSALS 20/20`, `SEALED 12+20`,
   `MUTANTS 15/15` are true is other seats' work. I checked only that the artifact a pointer names exists at the
   revision the pointer names.
4. **Host-level state is out of scope.** I did not audit `~/.gitconfig`, the credential helper, shell history, or
   processes outside this session; the env-leak finding rests on the transcripts (no seat exports `GIT_*`; the L1
   unsets before commits) plus the round-50 incident the scribe item already records.
5. **`plans/round50_c2_audit.py` has no frozen digest** in `plans/round-50-claims.md` (the claims freeze digests for
   the C1 counter, the population, the builder and the base fence; the C2 line names only the command). Its bytes at
   `d52243a` are `b911d03a08e396e5efdfaa434841300ccb5a452965c9d21c0c5fa56ea5dcaaef`. For C2 this is a provenance
   gap, not a boundary violation: an instrument that can be edited in place cannot be pinned by a judge.

## Scratch

`/fast/scratch/hyaku/kengaku-r50/R50SentWaveHygiene` (clone + tables) is removed before this yield; nothing in this
report depends on it surviving — every path quoted above is in the lane tree or in this wave dir.

VERDICT: **boundary-clean at seat level, and the integrator closed the three findings that touched an axis or its
evidence** — across 72 seats / 55 agent transcripts the audit found 0 writes outside the allowed paths, 0
production-file edits by a seat, 0 mutating git against the lane, 0 secrets, 0 `/tmp` citations in reports, 0
fleet-root or sibling-lane writes, and 0 leaked `GIT_*` exports in a seat's shell.

State of the findings at `297e179` (F1/F2 verified at `fa16b87`, re-verified here):
- **F1 resolved.** The receipt at `85102cf` names `REV 61f6257`, `TREE dirty=0`, and `61f6257`'s counter is
  `850ec79` — receipt revision and the claims row's scored instrument now name the same tree. Before that commit the
  receipt named `3dda12f`, whose counter was `d8787b34`: a real provenance gap at 14:51, now closed.
- **F2 resolved for the class this wave introduced.** The four lane-cwd `__pycache__` dirs are gone; the shipped
  path is clone-only with `PYTHONDONTWRITEBYTECODE=1`. Thirteen pre-wave dirs remain (module-dir imports) and belong
  to the identity/masking finding, not write scope.
- **F5 closed at `297e179`.** The receipt's `FENCE` scratch path is now declared non-load-bearing by
  `corpus/evidence/round50/c1-receipt-notes.txt`, which pins the three durable digests and a lane-only reproduction
  at `61f6257`; the scored receipt bytes are unchanged between `85102cf` and `297e179`. Residual nit: the notes'
  example reproduction clones into `/tmp`, above the 50 MB allowance — prefer `--work /fast/scratch/...` for both.
- **F3, F4, F6–F8 stand as written**: lane mutated mid-wave (cost comparability, not correctness), one full clone in
  L1 scratch, shared retry paths, duplicate deliverable dirs, and the alias pattern set in a gate table. None is a
  seat violation; none blocks C2, whose instrument is invoked by path and whose target set is the self-assessment
  files, not the lane's worktree state.
- **F9 (C2 instrument digest) stands**: `plans/round50_c2_audit.py` is still unpinned in the claims file.

Nothing in this report claims R50-C1 or R50-C2 admission; it measures write scope and artifact identity only.
