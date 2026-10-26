# R40ConnSibling — sibling-overlap scan, kengaku round 40 wave 1

Seat: R40ConnSibling (connector, leaf — no subagent dispatch). Read-only scan; no
fixtures, no installs, no lane writes anywhere. Frozen claims read in full first:
`plans/round-40-claims.md` (freeze `bbb10950…`): C1 = 21-frozen-mutant calibration of
the three tripwire tools via `plans/battery40` (kill directions incl. new `error` /
`rc-error`; counter soundness repairs A1 dying pid namespace, A3/A4/A5, fixture
fingerprints, sidechannel token scan, hostile-daemon control); C2 = pinned TB2
`db-wal-recovery` grader coverage (S119/S120, 28-case receipt, `regrade=` stability
rider; headline: destructive read-write open destroys the undecryptable WAL; "Fix the
WAL file" never checked; wrong-key XOR leaves 5 base rows).

## Axes

Adjacency (this seat's judged axis), coverage (the round's chosen axis; C2 is judged on
its counter). Calibration is touched only where a sibling's measured evidence sharpens a
frozen limit without editing anything frozen.

## Round surfaces scanned for

1. SQLite/WAL recovery and forensics graders; 2. JSON export graders; 3. mutation
testing of a lane's own gates; 4. bwrap sandboxes. Siblings: all 20 other
`*-shokunin` lanes, read-only (`PROVINCE.md`, `SKILL.md`, `corpus/README.md`,
`corpus/knowledge/`), prioritizing kagi (secrets/vault — its census reads a WAL-mode
SQLite DB), kaidoku + revenger (RE/forensics lanes), tameshi (verification-fixture
craft), kumitate (gate batteries, the fleet bounded runner), chousa (bwrap
provenance-falsification harness), mado/kake/mori/kotodama (bwrap counters), game-dev-2d
(JSON artifact verification).

## Overlaps found (6)

### 1. WAL destructive-read / snapshot-copy doctrine — kagi holds the host-side gate precedent → CITE

- `kagi-shokunin/corpus/surface-census.sh:271-275`: "Never open the live artifact: a
  read-only SQLite open can still touch `-shm`… A WAL-mode database is only current
  together with its `-wal`, so the snapshot carries the siblings when they are
  non-empty." The census `cp -p`s db plus non-empty `-wal`/`-shm` into `mktemp -d` and
  opens the copy `mode=ro`.
- Durable doctrine at `kagi-shokunin/corpus/knowledge/surface-census.md:129-131`
  (same snapshot rule), `:91` (unevaluable shapes read `UNVERIFIED`, exit 1,
  fail-closed — "a `CLEAN` summary over an unread shape class is the false-clean this
  gate exists to prevent").
- WAL-semantics selftest at `kagi-shokunin/.ufo/waves/round-23/parent-build/ClaimR11X07.md:57-62`:
  the gate's own WAL case switches to WAL, commits schema + one row, then `os._exit(0)`
  "so the closing checkpoint never runs"; the scan copies db+`-wal`+`-shm` and must exit 1;
  "Because the schema itself lives in the WAL, a reader blind to the WAL would see 16
  absent tables."

Why it matters: C2's two headline observations — the destructive plain-open trap and
"wrong-key XOR leaves 5 base rows" (a reader that never sees the WAL's committed
frames under-reads the database) — are the same hazard class kagi's gate documented
from the custody side on this host, with its own WAL-forensics selftest. Citing
converts C2's destructive-read trap from a single-probe finding into a
fleet-corroborated one. **Cite** (do not absorb: kagi's census is substrate custody,
its substrate is absent since round 18 and its host measurements are carried-forward
2026-09-28 records, re-correlated not re-derived — `kagi-shokunin/.ufo/waves/round-22/build/Entry23.md:111-115`).

### 2. SQLite tooling counters / two-reader oracle — kaidoku's R31 SQLite envelope → CITE (adjacent method only)

- `kaidoku-shokunin/tools/round-31/c1-sqlite-positive.py:2-6`: R31-C1 counter over REA
  6.5.0 `inspect-sqlite-database --schema-scope database`, binding each envelope's
  subject sha256 to the carrier's frozen sha256 and re-deriving from `git show` at the
  pinned rev.
- `kaidoku-shokunin/tools/round-31/sqlite_oracle.py:1-22`: an independent oracle with
  two readers that must agree — a byte-level SQLite file-format parser and the stdlib
  `sqlite3` opened "read-only and immutable so the file is never written."

Why it matters: kaidoku runs the same never-write-the-artifact-under-inspection
discipline against a SQLite substrate, and its counter is the closest sibling artifact
to "a counter over SQLite behaviour". It is a tool-behavior counter with an oracle,
not a recovery grader — **cite as adjacent method, no absorb**. Kengaku's C2 grades a
grader's coverage; nothing in kaidoku touches WAL recovery, XOR-encrypted WAL files,
or export JSON.

### 3. Gate-mutation kill predicate with re-run stability — kumitate K43 → CITE (direct precedent for the frozen `regrade=` rider)

- `kumitate-shokunin/scripts/gate-mutants.mjs:9-11`: K43 kill requires that "an
  immediate second run of the same mutated bytes meets the same conditions with the
  same sorted FAIL case names. An evaluable run that is not killed is SURVIVED; a
  disagreeing second run is UNSTABLE (exit-2 class). Each control is re-run after the
  mutants and must pass again." Clause at `:525` ("K43 (d): the second run must also
  kill"), selftest witnesses at `:1013`.

Why it matters: the frozen claims land `considerthese/2026-10-26.md` proposal 3's
stability rider as the probe's `regrade=` column ("every case is graded twice on the
same end state"). Kumitate's K43 is the fleet's standing precedent that a disagreeing
re-run is a *distinct verdict class*, not a kill and not a pass. **Cite** in the C2
entry's method note: the rider's design has a sibling precedent, so it reads as fleet
practice, not an ad-hoc add-on. Structural analogy only — K43 re-runs selftest mutants,
not a pinned grader.

### 4. Mutation-testing method ownership — tameshi owns the method; no kengaku leg exists → REPORT-OUT (already routed, re-confirmed)

- `tameshi-shokunin/PROVINCE.md:1-17`: owns "hermetic suites, mutation testing,
  fail-closed arms"; "Never edits a sibling's gate code (read-only probes;
  recommendations travel in round reports)".
- `tameshi-shokunin/tools/mutate-and-run.sh:1400-1434` (regression leg list): nine legs
  — js-kimi-census, kagi census, tsukuroi, mado-verify, kagi checklist-run, kumitate
  claims-check / round-gate / sources-check / cite-check — each run under an `env -i`
  sandbox home/tmp, **not** bwrap. `grep -n kengaku` over the tool returns nothing:
  tameshi has no recorded kengaku leg.
- Precedent already routed in-lane: `kengaku-shokunin/PROVINCE.md:282-284` (round-37
  paragraph): "mutation testing of a lane's own gate is a fleet-wide pattern, not
  kengaku ground — tameshi's `tools/mutate-and-run.sh` and kumitate's
  `gate-mutants.mjs` are the precedents"; round-38 fleet sandbox inventory at
  `kengaku-shokunin/PROVINCE.md:317-341` already rows tameshi's `mutate-and-run.sh`
  (`env -i` isolation, not bwrap, `:1418,1423,1428`).

Disposition: **report-out, already routed**. C1's `battery40` stays the frozen
counter's own work product; the routing needs no change this round — this scan
re-confirms it with current bytes and notes the absence of any kengaku leg in
tameshi's runner (tameshi may add `pkg_gate.py` only under its own opt-in protocol,
never editing the gate).

### 5. bwrap sandbox discipline — fleet inventory already landed in kengaku PROVINCE; two new citations for C1's threat model → CITE

Already inventoried at `kengaku-shokunin/PROVINCE.md:317-341` (round-38 fleet sandbox
table): tameshi defect-probes envelope + `env-diff.py` (`EXEC_UNAVAILABLE` when bwrap
missing); kumitate `cap-run.mjs:30-38,189-196` (`--ro-bind / / --unshare-pid
--die-with-parent --new-session --clearenv`; caller `--bind` refuses `/`, `/tmp`,
`/proc`, `/sys`, `/dev`, `/run`) — the closest sibling precedent for C1's A1
dying-pid-namespace control, since a detached hostile child dies with the same
machinery; mado `c1-r40-live-v2.py:19-22,480-496` (tools under `bwrap --unshare-all
--cap-drop ALL`, fresh `/proc` and `/dev`, tmpfs `/tmp`; no bwrap → `SETUP` exit 2,
"never a silent downgrade"); kake `sealed_count_v2.py:151-163` (jail whose pid
namespace cannot read the key file, the lane repo or the counter's cmdline);
mori `count-c2-a1.py:75-77`; kotodama's isolation-replay protocol. Tameshi's limit is
already cited via R39: `tameshi-shokunin/corpus/knowledge/guard-kill-closure.md:129`
(the envelope "is a sandbox for the probes, not a proof of containment for the tools
under test"; `/proc/1/environ` exposure at regression-tally-completeness.md:74).

Two citations are new this round and sharpen C1's frozen controls without touching
them:

- **Tool-forgery falsification under bwrap — chousa.** `.ufo/waves/round-35/w2/ExecPinModeChain.md:150-151`
  reproduces a bwrap harness that binds a non-GNU stub over `/usr/bin/grep` and
  `/bin/grep`; its F2 finding (`:155+`): "a forged `head` defeats the provenance check,
  and the gate then runs the wrong engine." This is the fleet's measured instance of
  the forgery class C1's fixtures exercise with forged repo content and the
  sidechannel scan guards against — same class, different substrate (PATH tool vs git
  object). **Cite** for C1's adjacent notes.
- **Bypass taxonomy — kaidoku carrier-guard.** `.ufo/waves/round-20/tools/carrier-guard.py:15-18`:
  "This is only a mode-bit guard: it does not prevent loader-mapped execution
  (e.g. ``ld-linux … <file>``), and root or another privileged actor can bypass or
  restore the mode-bit restriction. It also cannot prevent execution of a separate
  copy of a carrier." Kengaku's PROVINCE already rows this tool (`SKILL.md:606`); the
  docstring's named bypasses (loader-mapped, copy+exec, root restore) are the
  reference vocabulary for C1's hostile-daemon and tamper-fingerprint rationale: a
  control must name its own bypasses the way this guard does. **Cite.**

### 6. JSON-export verification adjacency — game-dev-2d and kaidoku hold method-adjacent, not grader, ground → DEFER (supports C2's novelty)

- `game-dev-2d-shokunin/corpus/README.md:16`: r58 save/load "round-trip JSON stable —
  headless Godot 4.7.2 distinct writer→read-only reader process … 87/87." JSON-artifact
  verification with separate writer and reader processes; game-save domain.
- `kaidoku-shokunin/corpus/knowledge/2026-10-13-r4-09-js-export-compare.md:89-100`:
  REA `compare-javascript-export-shapes` exercised (JSON Pointer `added`/`changed`/
  `removed` diffs); the arc3 c2 frontier item carrying it is recorded "now held"
  (`kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/claims/c2/RV-5/evidence/patch-apply-and-census.txt:37-39`).

Why it matters: C2's edge class — a graded JSON export whose source of truth is a
SQLite main DB plus an encrypted WAL — has **no holder in any sibling lane** (grep for
`terminal-bench|db-wal` across kagi/kaidoku/tameshi/kumitate/souji/kasegi/chousa/mado/
revenger corpora returned only kagi's own WAL-census files; no sibling pins a TB2
grader). game-dev-2d verifies JSON round-trips, kaidoku's export-shape item is held,
neither grades an export. **Defer** both (their domains stay theirs); the citation
value is that C2's grader class remains kengaku-unique — the coverage claim of a
sixth grader class is not anticipated by any sibling.

## Negative results (report-out — no overlap with the four surfaces)

- `revenger-shokunin`: no SQLite forensics — its only WAL hit is an Android developer-doc
  snapshot (`corpus/snapshots/dex-format.html:2432`, hibernation "Compatibility
  write-ahead logging"). Its forensics are binary/container byte evidence.
- `souji-shokunin`: git/jj repo hygiene; the r31 object-lifetime record R39 cited is
  git-side, not SQLite.
- `tsukuroi`, `kama`, `tabi`, `kotoba`, `kotodama`, `lore`, `audio`, `mori`, `kasegi`,
  `game-dev-3d`: no hits on SQLite/WAL recovery, JSON-export grading, gate mutation, or
  bwrap beyond the rows already named (mori's `count-c2-a1.py` bwrap row is already in
  kengaku's PROVINCE inventory).
- `chousa` otherwise: research-method owner; kengaku defers capture/citation method
  per its own PROVINCE; the round-35 bwrap harness is cited above as forgery-class
  evidence only.

## Proposed move (one, bounded)

Add one adjacent-citation clause to the wave-1 draft of
`corpus/knowledge/tb2-db-wal-recovery-grader.md` (C2's work product — not frozen),
under Limits/Adjacent, along these lines: the destructive-read trap and the
"database only current together with its `-wal`" semantics are independently
corroborated by kagi's custody-side gate doctrine (`surface-census.sh:271-275`,
`corpus/knowledge/surface-census.md:129-131`, with its own never-checkpointed WAL
selftest case, `ClaimR11X07.md:57-62` — noting kagi's substrate is absent and its
host measurements are carried-forward 2026-09-28 records); the probe's `regrade=`
stability rider follows kumitate's standing K43 practice of grading a disagreeing
re-run as its own verdict class (`gate-mutants.mjs:9-11,525`); and C1's forgery/
daemon controls name their threat model with chousa's measured forged-tool defeat
(`ExecPinModeChain.md` F2) and carrier-guard's self-declared bypass list
(`carrier-guard.py:15-18`). Effect: the coverage axis's headline finding becomes
fleet-corroborated rather than single-probe; the adjacency axis gains up to five new
sibling citations; calibration (C1) is untouched; nothing frozen — tools, counters,
probe, spec, gate, dry table, captures, receipt, claims — is modified. Draft only; L1
decides.

## Risks

- Kagi's substrate (the-janitor's `opencode.db`) has been absent since round 18; its
  host census rows are carried-forward measurements. The WAL selftest case is
  executable, but the citation must not imply current host verification of the census
  itself.
- K43's re-run clause grades selftest mutants of sibling gates, not a pinned external
  grader; the analogy to `regrade=` is structural (same "disagreeing re-run is a
  class" design), not an equivalence of verdict semantics.
- Chousa's F2 is a PATH-tool forgery defeating a version-provenance check; C1's
  fixtures forge repository content. Same class, different substrate — cite the class,
  never the mechanism transfer.
- Kaidoku's `compare-javascript-export-shapes` frontier item is recorded held, not
  admitted; if named at all, name it as held.
- Routing #4 is landed in kengaku PROVINCE since round 37; repeating it here is
  confirmation, not a new claim — do not relabel `battery40` as tameshi's.

## Verification (commands exercised, all read-only)

- `ls -d /home/vgpnk/Projects/shokunin/*-shokunin` → 21 lanes; per-lane existence check
  of `PROVINCE.md`/`SKILL.md`/`corpus/README.md` (all present; audio and game-dev-2d
  lack `SKILL.md`).
- `grep` (`WAL|write-ahead|sqlite3|SQLite`, `\bsqlite\b|write-ahead|\.db-wal`, `bwrap|
  bubblewrap`, `mutant|mutation`, `JSON export|…grader…json`, `terminal-bench|db-wal`)
  over the sibling trees — hits only at the file:line locations cited above; the
  unqualified `WAL` sweep's audio-lane hits are `WALL_*` wall-clock constants, not
  write-ahead log.
- `grep -n kengaku` over `tameshi-shokunin/tools/mutate-and-run.sh` → no matches (no
  kengaku leg).
- `sed -n` ranged reads of every cited file at the named lines (kagi `surface-census.sh`
  255-312 and `corpus/knowledge/surface-census.md` hits; kagi `ClaimR11X07.md` 55-70;
  kaidoku `c1-sqlite-positive.py`, `sqlite_oracle.py` 1-40, `carrier-guard.py` 1-55;
  kumitate `gate-mutants.mjs` 1-60 + grep for `UNSTABLE|second run` → `:9-11,525,1013`;
  tameshi `mutate-and-run.sh` 1400-1440; mado `c1-r40-live-v2.py` bwrap grep → `:19-22,
  480-496`; kake `sealed_count_v2.py` 150-165; chousa `ExecPinModeChain.md` 140-160;
  game-dev-2d `corpus/README.md:16`; kengaku `PROVINCE.md:317-341` inventory and
  `:282-284` r37 routing; kengaku `SKILL.md` round-37/38/39 gate-registry rows).
- Prior connector reports read for continuity: `.ufo/waves/round-39/build/R39ConnSibling.md`
  (6 overlaps, git-leak surfaces; bwrap method cites S093 + guard-kill-closure already
  landed there) and `R38ConnSibling.md` (existence confirmed in round-38 build dir).
- Frozen claims file read in full first, as instructed. No installs (none needed); no
  writes outside this report; no scratch created (no fixtures were built; the scan is
  read-only, so the /fast/scratch directive has nothing to bind).

Report: `.ufo/waves/round-40/build/R40ConnSibling.md`

VERDICT: sibling-overlap-6
