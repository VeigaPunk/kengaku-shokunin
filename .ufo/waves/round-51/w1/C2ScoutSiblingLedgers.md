# C2ScoutSiblingLedgers — sibling corpus ledgers

Seat: C2ScoutSiblingLedgers (scout). Axis judged: **adjacency**.
Lane: `kengaku-shokunin`. Stage-1 freeze: `e07f131cf7037e58a21db6e1f3986cf401ad257c` (ancestor of the measured kengaku HEAD; `corpus/routed-findings.jsonl` and `corpus/defects.jsonl` have an empty diff against that freeze).
No tool installed (pacman paused; nothing this seat needed beyond stdlib).

## Axes

1. **Presence** — for each sibling, does `corpus/` keep a routed-findings ledger, a defects ledger, or neither, and at which path.
2. **Field set** — keys actually stored, set against the frozen R51-C2 set `id, class, source, opened_round, status, owner, disposition, close, blocker, check, note` (`plans/round51_routing.py` `FIELDS`).
3. **Locality** — whether adding `owner` + `disposition` to kengaku's jsonl closes a shared fleet schema, or only this lane's file.

## Selection

Twenty sibling lanes from `shokunin.conf` (everything except `kengaku`) had `corpus/` walked for filenames containing `routed`, `defect`, `ledger`, `disposition`, or `finding`. Exact-name hits under those corpora:

- `routed-findings.jsonl`: 0
- `defects.jsonl`: 0
- `routed-defects.json`: 1 (`tameshi-shokunin/corpus/routed-defects.json`)
- `closure-dispositions.json`: 1 (`kagi-shokunin/corpus/closure-dispositions.json`)

The three deep reads are the two sole standing hits plus the first conf-order corpus that the name scan called empty (`kotoba`). That third pick was by filename, before its contents were parsed. `chousa` is noted under Limits and is not one of the three.

All three files are `git ls-files`-tracked. `git status --porcelain -- corpus` was empty (0 lines) in each sibling and in kengaku. Measurements are those HEADs' trees, not a scratch clone.

## Commands

```sh
git -C <lane> rev-parse HEAD
git -C <lane> rev-parse --show-toplevel
git -C <lane> status --porcelain -- corpus
git -C <lane> ls-files -- corpus/<ledger>
git -C kengaku-shokunin merge-base --is-ancestor e07f131cf7037e58a21db6e1f3986cf401ad257c HEAD
git -C kengaku-shokunin diff --stat e07f131cf7037e58a21db6e1f3986cf401ad257c HEAD -- corpus/routed-findings.jsonl corpus/defects.jsonl
```

Plus a Python walk of each sibling `corpus/` (filename census) and `json.loads` key-unions of the three files and of kengaku's two ledgers. No `plans/round51_routing.py` run: that counter reads this lane, not siblings.

`freeze_is_ancestor=yes`. The diff --stat for the two kengaku ledgers printed nothing.

## REV

```
REV kengaku 4090c3db79d11279ab5e5121ba25e74aa316e6e7
REV freeze e07f131cf7037e58a21db6e1f3986cf401ad257c
REV tameshi fa48c06c3669355fd80e8722eb733c1d6dfdd2f8
REV kagi 69b61db46be4ed955994f6f1d1cba522bc5f4e97
REV kotoba 47dbe8781657de563ff867caca6244d28e3db504
```

Kengaku baseline at that HEAD (unchanged vs freeze): `corpus/routed-findings.jsonl` is 71 JSONL rows, key union exactly `id, class, source, opened_round, status, close, blocker, check, note` — no `owner`, no `disposition`. Row 1 is `R39-R1`. `corpus/defects.jsonl` is 5 rows, key union `id, class, opened_round, source, check, status, closed_round, recurrence_of` — also no `owner`, no `disposition`.

## 1. tameshi — defects ledger

Path: `tameshi-shokunin/corpus/routed-defects.json` (973 lines). Not a routed-findings ledger.

Document keys: `schema`, `round`, `note`, `defects`.
`schema` = `tameshi-routed-defects-v1`, `round` = 50, `defects` n = 49.

Row key sets (every row):

| n | keys |
|---|------|
| 30 | `commit, evidence, id, note, seat, status` |
| 7 | `evidence, id, note, reason, seat, status` |
| 6 | `commit, evidence, id, note, reason, seat, status` |
| 5 | `evidence, id, note, seat, status` |
| 1 | `evidence, id, reason, seat, status` |

Always present: `id`, `status`, `evidence`, `seat`. `note` on 48/49. `commit` key on 36, non-null on 31. `reason` key on 14.
`evidence[]` objects (105): exactly `path`, `lines`, `excerpt`.

`status` counts: `fixed` 31, `declined` 11, `open` 7.
`owner` key: 0. `disposition` key: 0.
Every `fixed` row has a non-null `commit`; every `declined` row has `reason`; declined/open `commit` values that exist are JSON null (R40.5 at line 72).

R51 overlap: `id`, `status`, `note`. Missing: `class`, `source`, `opened_round`, `owner`, `disposition`, `close`, `blocker`, `check`.

Header (`:1-4`) and a declined row (`:63-75`) were read. `commit` here is a fixing commit of tameshi itself, not an owning lane.

## 2. kagi — neither of those two names; a closure-disposition ledger

Path: `kagi-shokunin/corpus/closure-dispositions.json` (112 lines), checked by `corpus/closure-dispositions.py` in the same directory. Not `routed-findings.jsonl`, not `defects.jsonl`.

Document keys: `schema`, `source`, `source_sha256`, `dispositions`.
`schema` = `kagi-closure-dispositions-v1`. `source` = `corpus/lessons/round-22-verifier-spotcheck.md`.

All 15 rows share one key set: `id, class, disposition, note, pointer`.
`class`: `routed-defect` 9, `spot-decision` 5, `adjudication` 1.
`disposition` values in the file: `fixed` 6, `no-action` 5, `reported` 3, `operator-owned` 1, `rejected` 0.
`owner` key: 0.

The checker (`closure-dispositions.py:21-25`, `:62`) freezes `KINDS = {fixed, reported, rejected, no-action, operator-owned}`. That vocabulary is not the R51 set `fixed-verified | fixed-historical | routed | referral | accepted-risk | refused-out-of-scope`. A `fixed` row points at a path (`D1` at `:48-53`, `pointer` `corpus/lessons/round-23.md#Routed defect dispositions`); it does not name a fleet lane.

R51 overlap: `id`, `class`, `disposition`, `note`. Missing: `source` (document-level only), `opened_round`, `status`, `owner`, `close`, `blocker`, `check`. Extra: `pointer`.

## 3. kotoba — a routed-findings record inside a knowledge file, not a defects ledger

No `corpus/routed-findings.jsonl` and no `corpus/defects.jsonl`. Corpus top is `QUALITY.md`, `README.md`, `SOURCES.md`, `knowledge/`, `lessons/` (158 files). The only structured data file the walk found is:

`kotoba-shokunin/corpus/knowledge/sibling-citation-routing-round16.json` (2971 lines).

Top keys: `schema`, `round`, `date`, `axis`, `before_lane_commit`, `instrument`, `observation_scope`, `population_sha256`, `sources`, `observations`, `findings`, `routes`, `scalar_score`.
`schema` = `kotoba-sibling-citation-routing-v1`, `round` = 16, `axis` = `adjacency`.

This is not nothing. `findings` (n = 14, starts `:2680`) is a routed-findings record. Every row has the same keys:

`action, actionable, class, evidence, id, issue, lane, line, owner, raw, reason, route, token`

`owner` is present on 14/14 and equals `lane` on 14/14 (`kasegi` 5, `kumitate` 5, `kagi` 2, `kake` 1, `kengaku` 1). First row `r16adj-01` (`:2682-2696`) has `"owner": "kagi"`. There is no `disposition` key. `route` is null on 10 and a route id on 4.

`routes` (n = 3, starts `:2927`) keys: `finding_ids, id, owner, status, via`. Each `owner` is `kake`, `kasegi`, or `kumitate`; `via` is `["protocol", "aggregator"]`; `status` is the string `prepared-for-integrator; owner acknowledgment and mirror not observed`.

`sources[]` (5) keys: `lane, contextual_head, input_identity, sha256, subjects, checked_after_exclusions, exclusions, projection, excerpts` — citation census, not findings. `observations[]` (226): `lane, line, raw, resolved, token`.

R51 overlap on a finding: `id`, `class`, `owner`. Missing: `source`, `opened_round`, `status`, `disposition`, `close`, `blocker`, `check`, `note`. The `owner` values are fleet lane ids, which is what R51-C2 asks kengaku's ledger to gain. The file is a round-16 knowledge record, not a standing jsonl a row-counter over `corpus/routed-findings.jsonl` would see.

## Locality

The R51 edit surface (`corpus/routed-findings.jsonl` plus `owner` and `disposition`) is **lane-local as a file**. No sibling corpus contains that filename or `defects.jsonl`. Repairing kengaku's 71 rows does not update a shared fleet ledger.

It is **not a uniform fleet gap on `owner`**. tameshi (49) and kagi (15) store no `owner`. kotoba's 14 findings all store `owner`. kagi already stores `disposition`, under a different closed vocabulary, with no lane owner. tameshi stores `status` (`fixed|declined|open`) and no `disposition`.

So the round's schema repair attributes kengaku's own rows. It does not close the sibling contracts, and it is not inventing an `owner` field the fleet has never used: kotoba already names the owner lane on each finding and again on each route.

## Limits

- Filename census is not a parse of every JSON under every sibling `corpus/`. audio, lore, revenger, tabi, and chousa have many `ledger` / `disposition` run artifacts. Those were not schema-parsed. The exact-name result (0 `routed-findings.jsonl`, 0 `defects.jsonl`) is a full `rglob` of each sibling `corpus/`.
- Also seen, not one of the three: `chousa-shokunin/corpus/evidence/round40/routed-defect-dispositions.json` (tracked, 40 lines). It is a four-key map `R2`–`R5`, each `{status, evidence, decision}` (`corrected` / `not-reproduced`). No `owner`, no `disposition`. Round evidence, not a standing ledger.
- Nested `evidence` / `owner` counts are from `json.loads` of the working trees above, not from re-running either lane's checker.
- Scratch `/fast/scratch/hyaku/kengaku-r51/C2ScoutSiblingLedgers` was created, held no clone and no receipt, and `rm -rf` left it absent (`ABSENT`).

VERDICT: lane-local file, not a fleet-wide missing-owner gap. tameshi keeps a defects ledger with no owner and no disposition; kagi keeps a closure-disposition ledger (different disposition vocabulary, no owner); kotoba keeps a routed-findings record whose 14 rows all name owner and whose 3 routes name owner, and keeps no defects ledger. Zero sibling corpora contain routed-findings.jsonl or defects.jsonl.
