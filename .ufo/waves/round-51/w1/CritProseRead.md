# CritProseRead — round 51, C1 `prose` independent reading audit

Seat: `CritProseRead` (critic). Lane: `kengaku-shokunin`. Item: read all 19 `PROVINCE.md`
rows myself and rule each manifest `prose` value RIGHT/WRONG with the sentence relied on.
Read-only against the lane; this file is the only artifact I wrote.

## Axes named

- **A1 — reading correctness.** For each of the 19 entries: does `prose` state what the row
  actually asserts about the probed target?
- **A2 — reading-rule consistency.** Two rows of the same textual shape (path list in the
  Path/endpoint cell + identical dated `ABSENT` marker in the third cell) must not be read
  one way in one entry and the other way in another.
- **A3 — independent corroboration.** Each row's state claim is re-measured against the host
  and the lane tree, so the audit does not inherit the manifest's own probes.

A move is kept only if it improves A1 without harming A2 or A3.

## Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

`PROVINCE.md` is byte-identical from the frozen base tip `297e1792` to `4090c3db`:
`git diff --stat 297e179..HEAD -- PROVINCE.md` prints nothing (only `plans/round51-surfaces.json`
and `plans/round51_surfaces.py` differ). The row text I audited is therefore the frozen
stage-1 text; the frozen claims file names base tip `297e1792`, and the counter's own `REV`
line prints the clone tip, `4090c3db`.

## Commands run (verbatim)

```sh
# 1. frozen counter, clean --shared clone in my scratch
git clone --shared -q /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r51/CritProseRead/lane
cd /fast/scratch/hyaku/kengaku-r51/CritProseRead/lane && python3 plans/round51_surfaces.py --lane .
# 2. lane's canonical surface instrument (QUALITY R14), same clone
python3 plans/state_check.py --summary
python3 plans/state_check.py --json          # extracted P2d.surface.* assertions
# 3. independent host/tree probe of every named target
for p in "$HOME/Projects/webzites/repos/llm-wiki" "$HOME/archive/bench-arena" ... ; do test -e "$p" && echo PRESENT || echo ABSENT; done
ss -ltn 'sport = :8791'; ss -ltn 'sport = :34113'
curl -sS -m 3 -o /dev/null -w "%{http_code}\n" http://127.0.0.1:34113/health
sha256sum grader.py plans/attrib_probe.py "$HOME/.local/share/ds-flash-shim/shim.py"
# 4. the rows' own literal commands (SF11 loop, SF18/SF19 summaries)
for d in round8-horizon round9-replication round9-fleet round10-fleet round11-power round11-fleet round12-ladder round12-fleet round13-ack-state round13-coverage round14-fleet round18-kimi-routing; do test -d corpus/evidence/$d || echo missing $d; done
python3 plans/attrib_calibration.py --summary
# 5. row provenance / marker semantics
git show 8ea41f9 -- PROVINCE.md
grep -n "R4\|R14" corpus/QUALITY.md
```

## Observed outputs (verbatim, evidence)

Frozen counter, reproduced exactly against the before receipt
(`.ufo/waves/round-51/claims/c1-before.txt`):

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

Lane's own surface instrument at the same revision:

```
assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5
P2d.surface.Research notes (SSOT for eval craft).path | MATCH | {"path": "~/Projects/webzites/repos/llm-wiki", "resolved_path": "/home/vgpnk/Projects/webzites/repos/llm-wiki", "exists": false, "ABSENT_marked": true}
P2d.surface.Local benchmark battery.path | MATCH | {"path": "~/archive/bench-arena/", "resolved_path": "/home/vgpnk/archive/bench-arena", "exists": false, "ABSENT_marked": true}
P2d.surface.Served local model.availability | OFFLINE_UNVERIFIABLE | {"path": null, "url_or_endpoint": true, ...}
P2d.surface.Route telemetry.path | MATCH | {"path": "~/Projects/bounties/ledger/telemetry.jsonl", ..., "exists": false, "ABSENT_marked": true}
P2d.surface.Client CLI telemetry.path | MATCH | {"path": "~/.bailian/telemetry.jsonl", ..., "exists": false, "ABSENT_marked": true}
P2d.surface.Model catalogs.path | MATCH | {"path": "~/.bailian/skills/bailian-docs-llm-wiki/models", ..., "exists": false, "ABSENT_marked": true}
P2d.surface.Own probe artifacts.path | MATCH | {..., "exists": true, "ABSENT_marked": false}
P2d.surface.In-repo gate.path | MATCH | {..., "exists": true, "ABSENT_marked": false}
P2d.surface.Public literature.path | MATCH | {..., "exists": true, "ABSENT_marked": false}
```

Host/tree probe (A3):

```
ABSENT  /home/vgpnk/Projects/webzites/repos/llm-wiki
ABSENT  /home/vgpnk/archive/bench-arena          # `ls -d ~/archive` -> No such file or directory
ABSENT  /home/vgpnk/Projects/bounties/ledger/telemetry.jsonl
ABSENT  /home/vgpnk/.bailian/telemetry.jsonl
ABSENT  /home/vgpnk/.bailian/skills/bailian-docs-llm-wiki/models/index.md
PRESENT /home/vgpnk/.local/share/ds-flash-shim/shim.py
PRESENT corpus/evidence/{round8-horizon,round9-replication,round9-fleet,round10-fleet,round11-power,round11-fleet,round12-ladder,round12-fleet,round13-ack-state,round13-coverage,round14-fleet,round18-kimi-routing}
PRESENT grader.py, corpus/QUALITY.md, corpus/SOURCES.md
PRESENT corpus/knowledge/eval-prior-art-calibration.md, corpus/knowledge/attrib-prior-art-r21.md
PRESENT plans/{attrib_probe.py,attrib_calibration.py,state_check.py,attrib-r21-frozen.md,attrib-r22-frozen.md,attrib-r23-frozen.md}
ABSENT  knowledge/eval-prior-art-calibration.md   # the Core row's literal text; see §Adjacent
```

```
-- :8791 --   LISTEN 0 512 127.0.0.1:8791 0.0.0.0:*
-- :34113 --  (no rows)
curl: (7) Failed to connect to 127.0.0.1:34113 after 0 ms: Could not connect to server / 000
90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f  grader.py
489f938a198e08cf8c30efc3ca24ea5fac90ef3909d80aec0b1f62c90616e06b  plans/attrib_probe.py
42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386  ~/.local/share/ds-flash-shim/shim.py
attrib_calibration rc=0 ; state_check rc=0
SF11 loop: prints nothing (all twelve dirs present)
```

Marker semantics in the lane's own record (A2 ground): `corpus/QUALITY.md:164` R4 —
"absent surfaces are marked where they are declared … carries `ABSENT <date>`";
`corpus/QUALITY.md:174` R14 — a `## Surfaces` row with a missing first local path is
MISMATCH "unless the row carries `**ABSENT**` or `**ABSENT <date>**`";
`corpus/lessons/round-25.md:17` M26 — "PROVINCE `## Surfaces` kept four absent first paths
unmarked … dated ABSENT markers make them MATCH" (the four are L12/L13/L16/L17; L14's marker
covers the `/proc` pid pin, per `.ufo/waves/round-25/falsify/RevengeFirstLocalPath.md:12-14`).

## Rulings — 19/19

Reading rule applied uniformly (derived from the manifest's own definition, "`present` means the
row asserts the target resolves"): `present` iff the row contains an **assertion** that the
probed target is reachable/working; a bare path listing in the Path/endpoint cell is a
presupposition of location, not an assertion, and a dated `ABSENT` marker naming the target is
the row's state statement.

| id | row | prose | ruling | sentence relied on |
|---|---|---|---|---|
| SF01 | 12 | present | **WRONG — correct reading `absent`** | "**ABSENT 2026-10-20** (round 25: first local path fails `test -e`; superseded by §Province map)" — see §The one WRONG |
| SF02 | 13 | present | RIGHT | "`tasks/`, `grade.sh`, `loop.sh`, `report-grok45.csv`, `report-qwenlocal*.csv`, `telemetry-qwenlocal-v2.csv` **all resolve at the archive path**" — an affirmative present claim; see §Trap |
| SF03 | 14 | present | RIGHT | "identity re-probed via `/v1/models` + `/health` **200 each round**" — an affirmative present claim; see §Trap |
| SF04 | 15 | absent | RIGHT | "`~/Projects/bounties/ledger/telemetry.jsonl` — **ABSENT**, reconfirmed round 14 …"; "never treat the path as live" |
| SF05 | 16 | absent | RIGHT | "quota-vs-auth failure split, poll-verb rule **ABSENT 2026-10-20** (round 25: first local path fails `test -e`…)" |
| SF06 | 17 | absent | RIGHT | "selection fields, open-weight twins **ABSENT 2026-10-20** (round 25: first local path fails `test -e`…)" |
| SF07 | 18 | present | RIGHT | "durable run bytes + analyses + L2 fleet artifacts"; all ten named trees measured present |
| SF08 | 19 | present | RIGHT | "`grader.py` (repo root; `python3 grader.py` → exit 0/1/2; `--selftest` S0–S7)"; file present |
| SF09 | 20 | present | RIGHT | "(URLs in `corpus/knowledge/eval-prior-art-calibration.md`)"; that file measured present |
| SF10 | 108 | present | RIGHT | "present; `90c87c88…ae941f`"; measured sha256 `90c87c88…ae941f` |
| SF11 | 109 | present | RIGHT | "all present; plus 28 root receipt logs"; the row's own loop prints nothing |
| SF12 | 110 | present | RIGHT | "all present; probe sha256 today `489f938a…16e06b`"; measured `489f938a…16e06b` |
| SF13 | 111 | present | RIGHT | "present (admission bar Q1–Q8 + round-closure criteria, created round 24)"; `corpus/QUALITY.md` present |
| SF14 | 112 | present | RIGHT | "present; 25 rows …" — the file is present (the count is `count_claim`'s business, not `prose`'s) |
| SF15 | 113 | present | RIGHT | "present; `42d86d99…15a386`"; measured `42d86d99…15a386` |
| SF16 | 114 | present | RIGHT | "LISTEN on `127.0.0.1:8791`"; measured `LISTEN 0 512 127.0.0.1:8791` |
| SF17 | 115 | present | RIGHT (with caveat) | "URLs cited in `knowledge/eval-prior-art-calibration.md`, `attrib-prior-art-r21.md`, and the ART dossier" — corpus-relative shorthand per `corpus/README.md:4`; both re-based files present. Literal repo-root paths are absent — see §Adjacent |
| SF18 | 116 | present | RIGHT | "exit 0 / exit 0"; measured `attrib_calibration --summary` rc=0 |
| SF19 | 117 | present | RIGHT | "exit 0 / exit 0 on the landed tree"; measured `state_check.py --summary` rc=0 |

**18 RIGHT, 1 WRONG.**

## The one WRONG — SF01 (row 12, `Research notes (SSOT for eval craft)`)

- **Recorded reading:** `prose = present`, `why = "the row's first path cell asserts the wiki tree
  resolves; round-15/25 rows already mark the older ~/wikillm path absent"`.
- **Correct reading:** `absent`.
- **Row text that proves it:** "…the `~/wikillm/llm-wiki` path does **not** exist here
  (`test -e` → absent) **ABSENT 2026-10-20** (round 25: **first local path fails `test -e`**;
  superseded by §Province map)". The row's first local path is the Path/endpoint cell's
  `~/Projects/webzites/repos/llm-wiki` — measured by the lane's own parser:
  `P2d.surface.Research notes (SSOT for eval craft).path` observed
  `{"path": "~/Projects/webzites/repos/llm-wiki", "exists": false, "ABSENT_marked": true}`.
- **Why the `why` cannot stand:** it attributes the marker to "the older ~/wikillm path", but the
  row already declares that path absent *before* the marker ("`test -e` → absent"), so a marker
  reading "first local path fails" would be both redundant and mislabelled. The marker is the
  first path's dated absence, and there is no other sentence in the row asserting that the
  llm-wiki tree resolves (the cell names the location and enumerates six subpaths — a
  presupposition, not an assertion; the row's only other clause is the purpose "digest into
  `corpus/knowledge/eval-*` entries").
- **A2 counterexample (the decisive one):** the same shape — paths in column 2, the identical
  marker string `**ABSENT 2026-10-20** (round 25: first local path fails `test -e`; superseded by
  §Province map)` in column 3 — is read `absent` for SF05 (row 16) and SF06 (row 17) and
  `present` for SF01 (row 12). One of the two readings must be wrong; SF05/SF06 are the correct
  ones (their rows assert absence, and nothing else), so SF01 is the outlier. SF02 and SF03 are
  *not* symmetric outliers: each carries an explicit present-tense reachability assertion
  ("all resolve at the archive path"; "200 each round") that SF01 lacks.

## Trap the RIGHTs must not be laundered through

- **SF02** is self-contradictory: column 2 asserts "all resolve at the archive path", column 3
  carries a dated marker whose parenthetical names the first local path (`~/archive/bench-arena/`,
  absent — `~/archive` does not exist at all). `prose = present` is a correct reading of the
  presence assertion, and the DRIFT is genuine **because that sentence is false and undated**.
  The landing fix must retract the "all resolve" clause (append-only erratum). Flipping
  `prose` to `absent` would silence the counter while leaving a false present-tense sentence in
  the row — self-certification of exactly the kind this seat exists to catch.
- **SF03** is a genuine row defect, not a marker conflict: the marker's nearest referent is the
  pid pin ("hermetic gates pin committed bytes, never `/proc` **ABSENT 2026-10-20**"), endpoint-first
  rows are `OFFLINE_UNVERIFIABLE` in the lane's own instrument, and round-25 M26 counts four
  absent first paths (L12/L13/L16/L17) — L14 is not one. The row asserts `200 each round`;
  measured: no listener on `:34113`, `curl` connect failed. Correction needed, DRIFT genuine.

## Impact on the claim

- The frozen before receipt is a faithful measurement of a defective manifest: `DRIFT 3` is
  produced partly by a wrong recorded reading, not by a row that asserts resolution. With SF01
  read correctly, the tip's DRIFT count is **2** (SF02, SF03), and row 12 needs no correction
  (it is already dated and truthful).
- The claims file's C1 "Before" paragraph ("DRIFT 3 (SF01 llm-wiki, SF02 bench-arena, SF03 served
  model — rows still assert they resolve)") overstates by one and misstates SF01's row.
- **Smallest safe correction (for the L1, who lands):** record a stage-1 amendment in the lane's
  own precedent form (round-25 Amendment 1 `710409f`) setting SF01's `prose` to `absent` with the
  sentence above, re-run `python3 plans/round51_surfaces.py --lane .` and re-receipt
  `DRIFT 2` under `.ufo/waves/round-51/claims/`. Do **not** silently flip the frozen field, and do
  **not** "correct" row 12: a second erratum appended there while `prose` stays `present` leaves
  `DRIFT 1` and the predicate still fails.

## Adjacent (outside my item, reported because it bears on row-reading integrity)

- **SF17 probe re-basing.** Row 115 names `knowledge/eval-prior-art-calibration.md` and
  `attrib-prior-art-r21.md`; both are absent as repo-root paths (`ls: cannot access 'knowledge'`),
  and the manifest probes `corpus/knowledge/…` instead. The re-basing is defensible
  (`corpus/README.md:4` uses `knowledge/`/`lessons/` as corpus-relative names) but silent: a
  stricter literal reading would call the row's pointers stale, and no counter would see it.
- **Probe coverage is narrower than the rows it audits** (A3 limit, not a `prose` error): SF07
  tests 5 of the 10 declared evidence trees, SF11 7 of the 12 loop dirs, SF17 2 of its 3 pointers
  ("the ART dossier" untested), SF09/SF17 never contact the URLs their rows name.

## Limits

- `count_claim` (SF14, 25 vs probe 170) was **not** re-derived by me; my item is the `prose` field.
- Endpoint and port states are point-in-time (2026-10-28, this session): `:34113` dead, `:8791`
  listening. A later listener on `:34113` would flip SF03's `state`, not its `prose`.
- I did not re-run `grader.py` (only its sha256) nor `plans/attrib_calibration.py --selftest`;
  the rows' stated exit-0 results were checked for `--summary` only.
- I read the 19 rows and their manifest entries; I did not audit the counter's own logic
  (separate seats) nor the `ANCHOR`/`UNCOVERED`/`NUMBER-DRIFT` legs.
- Scratch `/fast/scratch/hyaku/kengaku-r51/CritProseRead` was removed before yield (verified);
  no fixture git mutation was performed (clone only, `git -C` on the clone).

VERDICT: **FAIL (one wrong reading)** — 18/19 `prose` values RIGHT; SF01 (row 12) is WRONG and
must read `absent`, which makes the tip's DRIFT count 2, not 3; SF02 and SF03 are RIGHT and their
DRIFTs are genuine row defects that must be fixed by retracting the row text, never by flipping
the frozen reading.
