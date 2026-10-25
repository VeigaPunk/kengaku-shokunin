# Evidence table — kengaku round 35 wave 2 (falsify) — seat F35ReportEvidence (scribe)

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, branch master.
Tip (landed): `dfee6fff631ebc5f623ba4506e5c7992a215401c` — verified `git -C <lane> rev-parse HEAD` at run time = `dfee6fff631ebc5f623ba4506e5c7992a215401c`.
Freeze claim: `11d64530179b78e33ba6074fc77d63d36ee7ac31` (commit `round-35: freeze claims, counters, probe, ledger, controls`).
Baseline (wave-1 start): `58a19f37312e1b22fd2a7957bdfc6bb7832aadd0`.
Frozen claims: `plans/round-35-claims.md` (freeze `11d64530`).

## 1. Claim predicates — before (freeze receipt) vs after (tip, read-only run)

Both counters are read-only (grep of `round35_c1_verify.py` and `defect_ledger.py` for write ops
(`open(...,'w'|'a'|'r+')`, `write_text`, `unlink`, `rmtree`, `os.remove`, `mkdir`, `.write(`): none found).

| Claim | Frozen predicate (command) | Before (freeze control) | After @ dfee6fff |
|---|---|---|---|
| C1 coverage | `python3 plans/round35_c1_verify.py --lane .` prints `checks=6 defects=0` and `PREDICATE C1 pass`, exit 0 | `claims/control-c1-nothing.txt`: `checks=6 defects=5`, `PREDICATE C1 fail`, `exit=1` (V1–V5 DEFECT, V6 ok) | V1 ok V2 ok V3 ok V4 ok V5 ok V6 ok; `checks=6 defects=0`; `PREDICATE C1 pass`; `exit=0` |
| C2 calibration | `python3 plans/defect_ledger.py --lane .` prints `rows=5 closed=5 observed_pass=5 mismatches=0` and `PREDICATE C2 pass`, exit 0 | `claims/control-c2-nothing.txt`: `rows=5 closed=0 observed_pass=0 mismatches=0`, `PREDICATE C2 fail`, `exit=1` (D1–D5 open/fail) | `rows=5 closed=5 observed_pass=5 mismatches=0`; `PREDICATE C2 pass`; `exit=0` |
| C1 cheapest skip-control (must stay red) | same command as C1 | `claims/control-c1-skip.txt`: `checks=6 defects=5`, `PREDICATE C1 fail`, `exit=1` (V1/V2/V3/V5/V6 DEFECT) | not rerun (control receipt from freeze; it is a counterexample fixture, not the landed state) |
| C2 cheapest skip-control (status-only flip, must stay red) | same command as C2 | `claims/control-c2-flip.txt`: `rows=5 closed=5 observed_pass=1 mismatches=4`, `PREDICATE C2 fail`, `exit=1` (D2–D5 agree=NO) | not rerun (control receipt from freeze; it is a counterexample fixture, not the landed state) |

### C1 after — full output
Command: `cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/round35_c1_verify.py --lane .`
```
V1 ok
V2 ok
V3 ok
V4 ok
V5 ok
V6 ok
checks=6 defects=0
PREDICATE C1 pass
exit=0
```

### C2 after — full output
Command: `cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/defect_ledger.py --lane .`
```
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
exit=0
```

Both predicates PASS at the landed tip; the freeze controls demonstrate each predicate could fail (C1 5 defects, C2 all rows open).

## 2. Census — before vs after

Command (both): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`

| Census | Exit | Summary | Output |
|---|---|---|---|
| Before (freeze) | 0 | 15 × W04 warnings + `kengaku ok` | `claims/census-before.txt` (16 stdout lines + runner-appended `exit=0`) |
| After @ dfee6fff | 0 | 15 × W04 warnings + `kengaku ok`; stdout byte-identical to before (`diff` clean; before file additionally carries the appended `exit=0` runner line) | see below (full 16-line stdout) |

Census after — full stdout (captured 2026-10-25 from the command above):
```
kengaku	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
kengaku	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
kengaku	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
kengaku	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
kengaku	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
kengaku	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
kengaku	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
kengaku	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
kengaku	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
```
Census state did not change between freeze and tip (same W04 set, exit 0 both).

## 3. Commits between baseline and tip

Command: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --format='%H %s' 58a19f37..dfee6fff631ebc5f623ba4506e5c7992a215401c`
(7 commits, oldest → newest)

| Commit | Subject |
|---|---|
| `5d0c73db432f75eea7d5f90b521811c6686fcb68` | round-34 verifier spot-check (integrator, hyaku): non-author admit/reject |
| `11d64530179b78e33ba6074fc77d63d36ee7ac31` | round-35: freeze claims, counters, probe, ledger, controls |
| `dfcd294c60a00215c55bc4ce0b620440cd5e402f` | round-35: C2 close round-34 routed defects D1-D5 (drafts committed, mirror roots deleted, manifest, D4/D5 corrections, ledger closed, Q23) |
| `4fe72a9aab65c59b3a740406024d928234a7e23f` | round-35: C1 admit TB2 protein-assembly grader entry, S105-S107, probe receipt; PROVINCE round35 paragraph; lesson; post-hoc hardening |
| `6ac9611a260d7dea20c1fccd52cbb28618c85ca5` | round-35: SCORECARD round-35 section + LOG entry |
| `056e192a2766c9d80f33f80c6d59d321e8687902` | round-35: lesson Gate package rejects + census receipts |
| `dfee6fff631ebc5f623ba4506e5c7992a215401c` | round-35: wave-1 evidence (32 seat reports, spec, dispatch, results) + lesson held admit-candidates |

## 4. Wave-1 seat ledger (`build-results.json`)

Source: ` /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-35/build-results.json` (schema: `lane` kengaku, `round` 35, `wave` build, `seats`, `results`).

| Metric | Value | Command |
|---|---|---|
| Seat count | 32 | `json.load(build-results.json)` → `d["seats"]` = 32, `len(d["results"])` = 32; dispatch registry `build-dispatch.json` also has 32 members |
| Role histogram (ledger `agent` field) | executor 10, scribe 6, scout 4, critic 3, mutation-tester 3, reviewer 3, connector 2, simplifier 1 (sum 32) | `collections.Counter(r["agent"] for r in d["results"])` |
| Dead seats | 0 of 32 — every ledger seat has a committed report file under `.ufo/waves/round-35/build/<seat>.md` (32/32 present, names match the ledger 1:1); all 32 reports end with a `VERDICT:` line (`grep -l "VERDICT" *.md` → 32). No seat-level error text exists in the ledger | `ls build/*.md` vs `d["results"][*]["name"]`; `grep -l "VERDICT" build/*.md` |
| Ledger output capture | all 32 records have `output: null`; the single shared `note` (the closest thing to an error annotation) reads verbatim: "orchestrator kernel restarted mid-wave; seat output was delivered to the orchestrator session but not retained — read the seat report file in the wave dir" | `json.dumps(d["results"][i])` |

Observations:
- The ledger records no per-seat result payloads (all `output: null`) and no per-seat error strings; the only annotation is the shared kernel-restart note quoted above. Dead-seat determination therefore rests on report presence + VERDICT completion: 0 dead.
- Role histogram from the ledger `agent` field matches the dispatch roles (executor/scribe/simplifier/scout/connector/reviewer/critic/mutation-tester).

## Provenance

- All "after" commands ran read-only against the live lane (cwd = lane root for the counters; no writes by any of the commands). Census script header states read-only (`reads corpus/SOURCES.md, writes only stdout or --out`).
- `git status --porcelain` at run time showed only the falsify-wave scratch (`.ufo/waves/round-35/falsify*`) as untracked; the C2 D1 check (`untracked=0`) is scoped to the round-34 wave tree and the three plan-tool paths (per `R35ConsiderMine.md` and `corpus/lessons/round-35.md`), consistent with that output.
- The skip/flip controls are quoted from their frozen receipts; they were not rerun (they are counterexample fixtures, not the landed state).
