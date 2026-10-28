# R49SentHygiene — wave-wide boundary/hygiene audit (sentinel, kengaku round 49 w1)

Seat: `R49SentHygiene` (sentinel), serving **R49-C1 + R49-C2** (calibration + coverage).
Item executed: *audit the whole wave for boundary violations: outside writes, secrets, `/tmp` citation,
fleet-repo touches, shared writer paths; one report with per-seat disposition.*

## Axes named (godspeed step 1)

| axis | this seat moves | this seat must not move |
|---|---|---|
| **calibration** (primary, audit side) | nothing measured about the fence; the audit establishes whether the wave's evidence can be trusted — producer discipline, artifact location, provenance integrity | no predicate line, control, kill rule, literal, fence byte, counter byte |
| **coverage** (primary, audit side) | nothing measured about the package; same role: confirm C2 artifacts exist where the L1 can pick them up and cite only citable paths | no case table, probe, spec, dry table or receipt content |
| operability / freshness / novelty / depth / adjacency | none | no score, no SCORECARD row, no LOG entry, no admission |

This seat is a **leaf**: read-only against the lane except this report. No counter or probe was executed; no
scored run was attempted (none can exist at the frozen base — see §1).

## 1. Freeze precondition (verified before any measurement)

`9d2900af41e4d1fc6022eff99010436fde6dbd93` is the stage-1 freeze commit and it **predates every measurement
this wave or this seat made**. Committer time is the authoritative one: the author date is a jj-export artifact
(the freeze carries the r48 closure's author timestamp).

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
commit
$ git -C … show -s --format='author=%ai committer=%ci' 9d2900af41e4d1fc6022eff99010436fde6dbd93
author=2026-10-27 09:58:06 -0300 committer=2026-10-28 09:14:40 -0300
$ git -C … log --oneline -3
af88aab round-49: w1 v2 wave spec + dispatch evidence (64 seats, 40 attack, policy v2 accepted)
9d2900a round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims
3a54833 round-48 verifier spot-check (integrator, hyaku): non-author admit/reject
```

- Wave start: `.ufo/waves/round-49/w1.ready` → `2026-10-28T09:20:02`; first seat writes observed at 09:19–09:20
  (scratch dirs). Freeze committer time 09:14:40 < 09:17 (first wave artifact) < 09:20 (dispatch). **Predates
  every measurement.**
- **No scored run was possible before the freeze, and none at it:** counters absent from the frozen tree —
  `git ls-tree -r 9d2900af --name-only | grep -cE 'round49_(c1|c2)_verify'` → `0`. `plans/fixture_fence.py` and
  the round-46 package are the only measurable inputs at the base; every "pass"/"fail" line in the wave reports
  is a dev-harness or control-tree result, never a scored claim (checked line by line, §3 F3 and F12).
- Revision measured (receipt discipline, Q22):
  ```
  REV af88aab193e6034cb9b386472064e3c18fa90128
  TREE 356 untracked files, all under .ufo/waves/round-49/w1 (no production byte changed)
  ```
  The frozen base measured is `9d2900af41e4d1fc6022eff99010436fde6dbd93`; `af88aab1` adds only the wave spec
  and dispatch files, so the production tree measured is the frozen base byte-for-byte.
- Claims file unamended since the freeze:
  ```
  $ git -C … show 9d2900af:plans/round-49-claims.md | sha256sum
  7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83  -
  $ sha256sum plans/round-49-claims.md
  7292f4e0ec4ae62ae7a721aff02169abd0bb107f678bfeabcf9490bab5f16c83  plans/round-49-claims.md
  ```

## 2. What was audited, and how

Audited surface (whole wave): `.ufo/waves/round-49/` (spec, dispatch, ready markers, registry, every report and
every seat artifact dir), the live lane working tree, the fleet root, `/tmp`, `~/.local/bin`, `~/.npm`,
`~/.local/share/uv`, and the wave scratch root `/fast/scratch/hyaku/kengaku-r49/`.

Mechanical checks, all read-only:

```
# write scope / outside writes
git -C LANE status --porcelain -uall            # every path a seat wrote, classified
find LANE/plans LANE/corpus LANE/scripts LANE/SCORECARD.md LANE/LOG.md -newermt '2026-10-28 09:17'
find /home/vgpnk/Projects/shokunin -maxdepth 3 -newermt '2026-10-28 09:17' -type f \
     -not -path '*/kengaku-shokunin/*' -not -path '*/kasegi-shokunin/*' -not -path '*/kama-shokunin/*' …
find ~/.local/bin ~/.local/share/uv ~/.npm -newermt '2026-10-28 09:17'
# per-seat write authorisation: w1/<seat>.md + any w1 path named in that seat's item text
#   (extracted from w1-spec.json items; 53 of 64 name only the report, 11 name a file or dir)
# secrets
grep -rInE '<privatekey|gh[pousr]_|AKIA|xox[baprs]-|sk-|AIza|password=|token=>' .ufo/waves/round-49/
find .ufo/waves/round-49 -type f \( -name '.env*' -o -name '*.pem' -o -name '*.key' -o -name '.netrc' \
     -o -name '.git-credentials' -o -name 'id_rsa*' \)
find .ufo/waves/round-49 -type f -perm -o+w
# /tmp
ls -la /tmp | grep -iE 'r49|kengaku-r49'; find /tmp -maxdepth 1 -newermt '2026-10-28 09:17' -size +50M
ls /tmp | grep -i 'r49'          # no host artefact of the sandbox-internal write test
# spec hygiene (r48 routed defects 1–2)
python3 -c '…w1-spec.json/w1-dispatch.json: items, model fields, report paths, scratch paths…'
grep -roiE '<13-token operator-alias pattern>' .ufo/waves/round-49/     # pattern not reproduced; see §6 for a token-free locator
# scratch discipline
find /fast/scratch/hyaku/kengaku-r49 -maxdepth 3 -name .git -type d   # alternates vs full objects
cat */*/.git/objects/info/alternates | sort -u
# cross-seat writer paths
#   every seat-authored .py/.sh scanned for /fast/scratch/hyaku/kengaku-r49/<other-seat>
# provenance integrity of transcribed deliverables
sha256sum -c MANIFEST.sha256 (R49C2ExecSpec); plan.json payload digests (R49C2ExecMutBattery);
modules.sha256 + population.sha256 vs w1 tree and git show 9d2900af:<path> (R49C1ExecHonest)
```

## 2b. Sources opened

No external URL was opened by this seat: every source is a committed lane file, a live lane path, or a host path
read through the shell. The URL / access-date / located-quote duty therefore does not apply; the one network
re-open in this wave (`S166`, `R49C2SourceReopen.md`) is that seat's record, not this one's.

## 3. Findings

| id | severity | finding | smallest remediation |
|---|---|---|---|
| **F1** | **medium** | **`__pycache__` bytecode inside the wave dir — including inside the C1 population deliverable tree.** Observed mid-wave: 5 dirs / 22 `.pyc`, among them `w1/R49C1ExecHonest/plans/honest49/__pycache__/build_honest_population.cpython-314.pyc` and `…/plans/honest49/modules/(r46novel|novel48|novel49)/__pycache__/*.pyc` — the exact tree that stage 2 copies into `plans/honest49/`. The seat removed those by close; one remains at close: `w1/R49C1ExecFenceA/__pycache__/fence_a.cpython-314.pyc`. Any re-run of the population builder recreates the four inside the deliverable tree. | Before the stage-2 copy, `find .ufo/waves/round-49/w1 -name __pycache__ -prune -exec rm -rf {} +`, and copy `plans/honest49/` with `__pycache__`/`*.pyc` excluded. Do not let bytecode into `plans/honest49/`. |
| **F2** | low | **Write-scope wording gap.** The wave text authorises only the report plus the item-named sibling path, but handovers need receipts/payload trees that cannot stay in scratch (scratch must be deleted; `/tmp` is not citable). Seats resolved this by writing under their own `w1/<seat>/`, which goes beyond the literal grant where the item named a single file: `R49C1ExecFenceB/` (`dev_harness.py`, `make_mutants.py`, `mutants/`, `receipts/` beside the named `fence_b.py`), `R49C2ExecCounter/receipts/` (beside the named `candidate.py`), and two **top-level** files whose items name no wave path at all: `w1/R49C1MutBattery.c1-mutants.json` and `w1/R49C2MutDup-runs.txt`. Seat dirs whose item names the directory (`R49C1ExecHonest/`, `R49C1ExecControls/receipts/`, `R49C2ExecCases/`, `R49C2ExecControls/receipts/`, `R49C2ExecMutBattery/`, `R49C2ExecSpec/`) are within scope. No production file was touched. | L1 states in the wave report that per-seat `w1/<seat>/` dirs are sanctioned evidence locations, and either accepts or relocates the two top-level files before committing. |
| **F3** | low | **One operator model-alias token in a wave artifact:** `w1/R49C2ExecCounter/receipts/fixture-history.txt:294`. The line is a verbatim `git log --oneline --graph --all` capture whose subject is the round-18 commit `f9d54f1` ("round-18: land … model-routing digest and evidence index"); the token is **already committed in the lane's history** — the commit exists at the frozen base — and cannot be removed without rewriting history. The token is **not reproduced in this report**; locate it with the command in §6. Spec, dispatch, ready markers, registry and context are alias-free (r48 routed defect 2 repaired at the spec layer). | L1 records it as inherited (preferred: redacting a log capture falsifies evidence) or masks the single token with a marker; either way it must be a stated, recorded decision. |
| **F4** | low | **Three seats used a full clone instead of `git clone --shared`:** `R49C1HoConfig/lane`, `R49C2Sandbox/lane`, `R49C1MutOrder/clone` — `remote.origin.url = file:///…/kengaku-shokunin`, no `objects/info/alternates`, 52 MB of objects each. Wave directive: "One live clone per seat (`git clone --shared`); never a full mirror of the lane." | Use `git clone --shared` (all other seat clones do; their alternates all resolve to the lane's `.git/objects`). |
| **F5** | low (resolved) | **Transient scratch-removal contradictions:** at 09:29 three seats that had written "removed" in their reports still held scratch — `R49C2ExecControls` 3.9 GB, `R49C2ExecProbe` 571 MB ("no scratch tree remains on disk"), `R49C1ScribeLimit` an empty dir. **All three were gone by close**; the only scratch dirs left are the three report-less seats and this seat, and no remaining seat both claims removal and holds a tree. | none beyond the standing rule: re-check `test ! -e "$S"` before yielding; an empty dir still counts. |
| **F6** | info | **No secrets.** 0 matches across the wave tree for private-key headers, GitHub/AWS/Slack/OpenAI-shaped tokens, `password=`/`token=` forms; no `.env*`, `*.pem`, `*.key`, `.netrc`, `.git-credentials`, `id_rsa*` files; no world-writable files. Long hex strings in reports are sha256 digests, not key material. | none |
| **F7** | info | **No host `/tmp` use and no `/tmp` citation.** Three pre-wave files whose names contain `r49` sit in `/tmp` (L1 preparation at 09:11 and two Oct-26 documents, all older than the wave); none is cited as evidence by any wave report, and none is reproduced here — the checklist command is in §6. No wave seat wrote to host `/tmp`: `find /tmp -maxdepth 1 -newermt '2026-10-28 09:17' -size +50M` is empty and no new `r49`-named entry exists. `R49C2Sandbox`'s `/tmp` mentions are sandbox-internal (the probe mounts `--tmpfs /tmp`; the write-test path it names does not exist on the host — checked). The committed probe `plans/polyglot_c_py_probe.py` hardcodes `/tmp` **only inside** its bubblewrap sandbox and takes its host work dir from `--work`/`$TMPDIR` (`tempfile.mkdtemp`, no `dir=` default) — not a host-`/tmp` hardcode. | none |
| **F8** | info | **No fleet-repo touch by this wave.** Fleet-root status is byte-identical to the pre-wave baseline (6 entries, all mtimes before 09:17): `M .ufo/reports/round-58/chousa.md`, `?? .scratch/closure-mado-r50.json`, `?? .scratch/source-routing-queue.md`, `?? o.bin`, `?? oldrep1.out`, `?? oldrep2.out`. Post-wave writes at fleet root are `.ufo/state/{disk-guard,inline-dispatcher}.log` (host dispatcher) and sibling-lane activity (`kasegi-shokunin`, `kama-shokunin`, `tsukuroi-shokunin`, `souji-shokunin`), plus `npm exec rea-agents@6.5.0` runs against `/fast/scratch/hyaku/kaidoku-r44/…` — attributable to those lanes' own agents, not to a kengaku r49 seat. | none |
| **F9** | info | **No lane production write.** HEAD is still `af88aab1…`; all 300+ untracked entries are under `.ufo/waves/round-49/w1/` (plus `w1.ready.dispatched`); `find plans corpus -newermt 09:17` → 0; reflog shows only the L1's jj exports; no stash, no new branch, no worktree. | none |
| **F10** | info | **No shared writer paths.** 64 items: 64 unique report paths, 64 unique scratch dirs, each derived from the seat name; no `model` field on any task; no role→alias map in context (r48 routed defects 1–2 repaired at the spec layer). Zero cross-seat scratch references in any seat-authored script. | none |
| **F11** | info | **Transcribed provenance verifies.** `R49C1ExecHonest`: `modules.sha256` 42/42 digests match (20 transcribed under `w1/…/plans/honest49/`, 22 resolved against `git show 9d2900af:<plans/battery4x/…>`), `population.sha256` matches `population.txt`, 124 fixtures in both `population.txt` and `identity.jsonl`. `R49C2ExecMutBattery`: `plan.json` 23 mutants, 23/23 payload digests match. `R49C2ExecSpec`: `MANIFEST.sha256` 13/13 OK; `pkg-spec-r49.json` parses with three open slots (`<PIN:stage-2>` ×2, `<PIN:stage-3>` ×1) and no absolute or `/tmp` path. | none (slots are stage-2/3 work by design) |
| **F12** | info | **No admission claims.** Every `PREDICATE R49-C1/C2 pass` line in a report is either (a) a scratch-only satisfiability copy explicitly marked non-deliverable (`R49C1ExecCounter` §6), (b) a dev-harness measurement of a fence candidate whose verdict says "No admission claimed" (`R49C1ExecFenceB`), (c) a description of what the counter *would* print (`R49C2ExecCounter` §clause table), or (d) inside a negation/counterfeit-mutant description (`R49C2Echo`, `R49C1MutExit`). No seat claims C1/C2 admission. | none |
| **F13** | info | **No package-manager activity by seats.** `~/.local/bin` untouched since the wave start; no `uv` installs; no `pacman`/`sudo`/`npx`/`npm -g` invocations in any seat-authored script (matches found were inside pre-existing lane copies of rounds 35–41 text). | none |
| **F14** | info | **Cited lane paths resolve.** Every non-prospective lane path cited by a report exists at `af88aab1`; the exceptions are sibling-lane paths (`kasegi-…`, `kumitate-…`, `revenger-…`, `tabi-…`, `chousa-…`) that a naive prefix scan truncates, scratch-clone staging paths written as commands (`plans/honest48/`, `plans/round48_c1_verify.py` — created inside the seat's clone, never claimed in the lane), and one transient observation (`w1.ready.partial`, quoted from live porcelain at 09:22 and since renamed). The report contract itself lives at the fleet root (`.ufo/prompts/kengaku-round-49.md`, 53,922 bytes, 08:59) and exists — the lane has no `.ufo/prompts/`, which is correct. | none |

## 4. `/tmp` and scratch accounting

- Wave scratch root at close: see §5; peak observed 27 GB (incl. `R49C1ExecControls` 12–17 GB of control trees and
  `R49C1ExecHonest` 529 MB of fixture work), against `/fast` 38% used. No seat placed a file in `/tmp`, so no
  `/tmp` size rule applied; the post-wave `/tmp` entries that do exist (§3 F7) top out at 572 KB, well inside the
  50 MB rule.
- Every alternates file under the wave scratch resolves to exactly one target:
  `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.git/objects`.
- No symlink in any seat scratch points into a sibling lane or the fleet repo.

## 5. Per-seat disposition (all 64 seats, measured 2026-10-28 09:50:29 )

Report presence is checked at the seat's **item-named absolute path**; scratch presence is the seat's own
`/fast/scratch/hyaku/kengaku-r49/<seat>/` directory. "clean" means: no `/tmp` citation, no secret-pattern hit,
no positive C1/C2-admission claim, scratch absent (or present only because the seat was still running at close).
This seat's own row is a pre-cleanup snapshot; §9 records that its scratch was deleted before yield.

| seat | role | report | scratch | notes |
|---|---|---|---|---|
| `R49C1ExecCounter` | executor | yes | removed | clean |
| `R49C1ExecFenceA` | executor | yes | removed | clean |
| `R49C1ExecFenceB` | executor | yes | removed | clean |
| `R49C1ExecHonest` | executor | yes | removed | clean |
| `R49C1ExecControls` | executor | yes | removed | clean |
| `R49C1ScribeSynth` | scribe | yes | removed | clean |
| `R49C1ScribeLimit` | scribe | yes | removed | clean |
| `R49C1ConnOverlap` | connector | yes | removed | clean |
| `R49C1ConnPattern` | connector | yes | removed | clean |
| `R49C1ScoutPop` | scout | yes | removed | clean |
| `R49C1Rerun` | reviewer | yes | removed | clean |
| `R49C1HonestInv` | reviewer | yes | removed | clean |
| `R49C1Overrefusal` | critic | yes | removed | clean |
| `R49C1HoArgv` | critic | yes | removed | clean |
| `R49C1HoPaths` | critic | yes | removed | clean |
| `R49C1HoStore` | critic | yes | removed | clean |
| `R49C1HoConfig` | critic | yes | removed | clean |
| `R49C1HoMount` | critic | yes | removed | clean |
| `R49C1MutNames` | mutation-tester | yes | removed | clean |
| `R49C1MutOrder` | mutation-tester | yes | removed | clean |
| `R49C1MutBoundary` | mutation-tester | yes | removed | clean |
| `R49C1MutGit` | mutation-tester | yes | removed | clean |
| `R49C1MutPending` | mutation-tester | yes | removed | clean |
| `R49C1MutCounterPins` | mutation-tester | yes | removed | clean |
| `R49C1MutExit` | mutation-tester | yes | removed | clean |
| `R49C1MutBattery` | mutation-tester | yes | removed | clean |
| `R49C1PredCounter` | critic | yes | removed | clean |
| `R49C1CritBase` | critic | yes | removed | clean |
| `R49C1CritPop` | critic | yes | removed | clean |
| `R49C1RevNoHarm` | reviewer | yes | removed | clean |
| `R49C1RevClaim` | reviewer | yes | removed | clean |
| `R49C2ExecCounter` | executor | yes | removed | clean |
| `R49C2ExecProbe` | executor | yes | removed | clean |
| `R49C2ExecCases` | executor | yes | removed | clean |
| `R49C2ExecControls` | executor | yes | removed | clean |
| `R49C2ExecMutBattery` | executor | yes | removed | clean |
| `R49C2ExecSpec` | executor | yes | removed | clean |
| `R49C2ScribeGate` | scribe | yes | removed | clean |
| `R49C2ScribeEntry` | scribe | yes | removed | clean |
| `R49C2ConnPrior` | connector | yes | removed | clean |
| `R49C2ConnCross` | connector | yes | removed | clean |
| `R49C2ScoutEntry` | scout | yes | removed | clean |
| `R49C2Rerun` | reviewer | yes | removed | clean |
| `R49C2TagInv` | reviewer | **no report** | present | scratch 571 MB at close |
| `R49C2PreReceipt` | critic | yes | removed | clean |
| `R49C2PosControl` | critic | yes | removed | clean |
| `R49C2Filler` | critic | yes | removed | clean |
| `R49C2Echo` | critic | yes | removed | clean |
| `R49C2MutTags` | mutation-tester | yes | removed | clean |
| `R49C2MutOrder` | mutation-tester | **no report** | present | scratch 571 MB at close |
| `R49C2MutPins` | mutation-tester | yes | removed | clean |
| `R49C2MutVerdict` | mutation-tester | yes | removed | clean |
| `R49C2MutReceipt` | mutation-tester | **no report** | present | scratch 571 MB at close |
| `R49C2MutDup` | mutation-tester | yes | removed | clean |
| `R49C2SourceReopen` | reviewer | yes | removed | clean |
| `R49C2Scope` | scout | yes | removed | clean |
| `R49C2CritDoNothing` | critic | yes | removed | clean |
| `R49C2RevAdmission` | reviewer | yes | removed | clean |
| `R49C2RevNoHarm` | reviewer | yes | removed | clean |
| `R49C2Sandbox` | critic | yes | removed | `/tmp` mention — cleared (§3 F7) |
| `R49SentHygiene` | sentinel | yes | present | scratch 571 MB at close |
| `R49RevReport` | reviewer | yes | removed | clean |
| `R49RevengerOverlap` | revenger | yes | removed | clean |
| `R49RevClosure` | reviewer | yes | removed | clean |

Wave totals at audit close: **61/64 reports** present (this report included), **3** seats still in flight
(`R49C2TagInv` (last scratch write 09:25), `R49C2MutOrder` (last scratch write 09:26), `R49C2MutReceipt` (last scratch write 09:31)); **4** scratch dirs on disk
(those in-flight seats plus this seat), **2282 MB** total; **356** files under `w1/`;
**356** untracked lane entries, **0** of them outside `.ufo/waves/round-49/w1`;
`__pycache__` dirs in `w1/`: **1** (`R49C1ExecFenceA/__pycache__`),
**1** `.pyc` files.

## 6. Observed outputs (verbatim, where they are evidence)

Write scope — every untracked lane path is inside the wave dir:

```
$ git -C …/kengaku-shokunin status --porcelain -uall | wc -l
356
$ git -C … status --porcelain -uall | grep -v 'w1'
(empty)
$ git -C … rev-parse HEAD
af88aab193e6034cb9b386472064e3c18fa90128
$ find plans corpus -newermt '2026-10-28 09:17' | wc -l
0
```

Lane git internals untouched by seats (last write is the L1's own export, before seats started):

```
$ stat -c '%y %n' .git/config .git/hooks
2026-10-28 08:59:36.343666841 -0300 .git/config
2026-10-13 16:50:59.736497771 -0300 .git/hooks
$ find .jj -newermt '2026-10-28 09:17' -type f -printf '%TY-%Tm-%Td %TH:%TM:%TS\n' | sort | tail -1
2026-10-28 09:18:21.943…            # L1 export; first seat scratch dir at 09:19
$ git stash list ; git worktree list
(no stashes) / one worktree: kengaku-shokunin af88aab (detached HEAD)
```

`__pycache__` residue inside the deliverable tree (F1):

```
$ find .ufo/waves/round-49/w1 -name '__pycache__' -o -name '*.pyc'
./R49C1ExecFenceA/__pycache__
./R49C1ExecFenceA/__pycache__/fence_a.cpython-314.pyc
./R49C1ExecHonest/plans/honest49/modules/novel49/__pycache__/*.pyc      # present earlier in the wave, 4 files
```
(Earlier samples during the wave found 5 such dirs / 22 `.pyc`, including
`R49C1ExecHonest/plans/honest49/__pycache__/build_honest_population.cpython-314.pyc` and
`modules/(r46novel|novel48|novel49)/__pycache__/`; the seats deleted most as they finished.)

Full clones instead of `--shared` (F4):

```
$ for d in R49C1HoConfig/lane R49C2Sandbox/lane R49C1MutOrder/clone; do git -C "$d" config --get remote.origin.url; done
file:///home/vgpnk/Projects/shokunin/kengaku-shokunin
file:///home/vgpnk/Projects/shokunin/kengaku-shokunin
file:///home/vgpnk/Projects/shokunin/kengaku-shokunin
$ du -sh R49C1HoConfig/lane/.git/objects R49C2Sandbox/lane/.git/objects R49C1MutOrder/clone/.git/objects
52M  52M  52M                      # no .git/objects/info/alternates in any of the three
```

The single alias occurrence (F3):

Token-free locator (the report does not reproduce the alias):

```
$ grep -rniE 'round-18: land .* model-routing digest' .ufo/waves/round-49
./w1/R49C2ExecCounter/receipts/fixture-history.txt:294:* f9d54f1 round-18: land <alias> model-routing digest and evidence index (parent M1-M6)
$ git -C … log --all --oneline --grep='model-routing digest'
f9d54f1 round-18: land <alias> model-routing digest and evidence index (parent M1-M6)   # pre-existing in lane history
```

Fleet root, unchanged from the pre-wave baseline (F8):

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .ufo/reports/round-58/chousa.md
?? .scratch/closure-mado-r50.json
?? .scratch/source-routing-queue.md
?? o.bin
?? oldrep1.out
?? oldrep2.out
$ stat -c '%y' o.bin oldrep1.out oldrep2.out        # 10-27 16:58, 10-28 09:10, 10-28 09:11 — all pre-wave
```

Host `/tmp` (F7):

```
$ ls -la /tmp | grep -icE 'r49|kengaku-r49'
3                              # all pre-wave: one L1 preparation file (09:11), two documents (10-26)
$ find /tmp -maxdepth 1 -newermt '2026-10-28 09:17' -type f | wc -l
23                             # none an r49 scratch tree; names are harness/other-lane artefacts
$ find /tmp -maxdepth 1 -newermt '2026-10-28 09:17' -type f -printf '%s
' | sort -rn | head -1
585591                         # largest entry = 572 KB, far under the 50 MB rule
$ find /tmp -maxdepth 1 -newermt '2026-10-28 09:17' -type f -size +50M | wc -l
0
```

The 23 post-wave `/tmp` entries are host-harness and other-workstream artefacts (`ecc-metrics-*`,
`claude-tool-count-*`, `hyakki-*` build logs, `zcode-*`), not this wave's scratch and not cited anywhere in the
wave. The sandbox-internal write-test path named by `R49C2Sandbox` is checked to be absent on the host (its probe
writes inside `--tmpfs /tmp`): the named path does not exist. Names of the three pre-wave files and of that
sandbox path are deliberately not reproduced here. Total post-wave `/tmp` volume: 1,215,891 bytes.

```

Secrets (F6): zero matches for private-key headers, `gh[pousr]_…`, `AKIA…`, `xox[baprs]-…`, `sk-…`, `AIza…`,
`password=`/`token=` forms across `.ufo/waves/round-49/`; no `.env*`/`*.pem`/`*.key`/`.netrc`/`.git-credentials`/
`id_rsa*`; no world-writable file. The only historical "secret-like" file in the lane
(`.ufo/waves/round-34/build/R34SentSecrets.md`) contains the *patterns*, not values. No package installs:
`~/.local/bin`, `~/.local/share/uv`, `~/.npm` show no seat activity; the `npm exec rea-agents@6.5.0` logs are
`/fast/scratch/hyaku/kaidoku-r44/…` (another lane).

Provenance integrity of transcribed deliverables (F11):

```
$ (cd w1/R49C2ExecSpec && sha256sum -c MANIFEST.sha256)          → 13/13 OK
$ plan.json (R49C2ExecMutBattery): 23 mutants, 23/23 payload digests match
$ modules.sha256 (R49C1ExecHonest): 42/42 match (20 local, 22 via git show 9d2900af:<plans/battery4x/…>)
$ population.sha256 → matches population.txt; 124 fixtures in population.txt and identity.jsonl
$ (cd w1/R49C1ExecControls/receipts && sha256sum -c INDEX.sha256) → 22/22 OK
```

## 7. One claim-stopper observation for the L1 (disclosed by its own seat, not a hygiene defect)

`w1/R49C1ExecControls/receipts/cand104mut-s1-control-c1-base-fence.txt` prints **`PREDICATE R49-C1 pass`**,
exit 0, on a **battery-only honest population (104)** with the mutants leg armed
(`LITERALS refusals=20 sealed=12 honest=104 mutants=12`, `PINS total=66 mismatched=0`). The seat discloses this
at the top of its report (`R49C1ExecControls.md:23-27`) and in §8: the do-nothing base-fence control's failure is
carried **entirely by the 20 novel honest classes**, so stage 2 must commit `plans/honest49/` (`<H>`=124)
**and** `plans/mutants49/c1-mutants.json` together — either alone lets a frozen control pass, and "a control that
passes refuses the counter". Not a boundary violation; recorded here because an under-filled `<H>` at stage 2 would
be a silent kill-rule contravention.

## 8. Limits

- Read-only audit. No counter/probe was executed by this seat; the freeze check is the only precondition required
  of it, and no scored run exists or could exist at the frozen base (`round49_*_verify.py` absent: count 0).
- **3 seats had no report at audit close** (R49C2TagInv, R49C2MutOrder, R49C2MutReceipt). Their
  scratch dirs are present but their last writes are 19–25 minutes old (R49C2TagInv: 09:25, R49C2MutOrder: 09:26, R49C2MutReceipt: 09:31), which is consistent with stalled seats but does **not** establish it — a long
  silent computation is possible. They are **unattributed, not cleared**: their final report may still land and
  their scratch may still be cleaned. 61 reports were present and audited.
- Attribution of concurrent activity is by timestamp and path identity, not by process inspection: sibling-lane
  writes (`kasegi-shokunin`, `kama-shokunin`, `tsukuroi-shokunin`, `souji-shokunin`, `kotoba-*`), host-dispatch
  logs (`.ufo/state/*`), `~/.gateguard`/`~/.grokbot` state and `kaidoku-r44` npm runs are all consistent with
  other agents and are not charged to this wave. No syscall tracing (strace/eBPF) was used; "no outside write" is
  a filesystem-state claim (git status, mtimes, tree listings), not a traced claim.
- The secrets sweep is pattern-based (11 classes) and filename-based; it is not entropy analysis and does not read
  binaries. Binary `.pyc` files were inspected only for stray text tokens.
- Report *content* beyond the five hygiene axes (measurements, claims, counters) was not re-derived; only
  mechanically checkable provenance (digests, manifests, paths) was re-verified.
- `.jj/` internals (6,101 ignored paths) are the lane's VCS store, pre-existing and untouched since the L1's
  export at 09:18:21; excluded from the write-scope count.

## 9. Scratch

`S=/fast/scratch/hyaku/kengaku-r49/R49SentHygiene` (TMPDIR exported there) holds only this seat's scratch
(one `git clone --shared` at the frozen base, the audit scripts, and the generator). **Deleted before yield.** No
receipt in this report depends on a scratch or `/tmp` path as citable evidence; every number above is
reproducible from the lane tree and the live filesystem with the commands printed in §2 and §6.

VERDICT: **wave-hygiene-audited — no lane production write, no fleet-repo touch, no secret, no `/tmp` citation,
no shared writer path, no admission claim, no scored run; 4 low/medium producer-discipline findings (F1 pycache in
the deliverable tree, F2 write-scope wording gap, F3 one inherited alias token, F4 three full clones) and 1
disclosed claim-stopper constraint for stage 2 (§7). 3 seats still in flight at close.**
