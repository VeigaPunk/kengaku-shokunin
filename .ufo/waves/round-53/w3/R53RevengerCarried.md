# R53RevengerCarried — carried routed defects from the round-52 closure

Seat: R53RevengerCarried (revenger, leaf, wave 3). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Lane HEAD measured: **`9ead4476bf55b1ea6490d0204b668195db4a4d1d`** (`round-53: confirmations integrated ...`). The lane was at `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe` when the seat started and advanced during the run; the L1 landed only `corpus/evidence/round53/confirmations.json`, `.ufo/waves/round-53/w3-spec.json`, `w3-dispatch.json`, `w3.ready` (`git diff --stat b1f79a54 9ead4476`). No file in the three carried-defect scopes changed between the two hashes, so the findings hold at both.

Scope: read-only on the lane. Clone at `/fast/scratch/hyaku/kengaku-r53/R53RevengerCarried/lane` (`git clone -q --shared`; `git -C … rev-parse --show-toplevel` printed that path). No `git commit/add/push/stash/checkout/reset/pull`, no lane edit, no tool installed or upgraded. Proposed code lives only in this seat directory; nothing was landed.

## Summary

| # | Carried item | State at HEAD `9ead4476` | Proposed action for next round |
|---|---|---|---|
| (a) | untracked `tb2-paper-full.html` | **Absent.** No file of that name exists anywhere in the lane or fleet tree; never committed. Nothing for the L1 to delete. Three docs still name it. | Strike the item from the closure; scrub the three historical mentions only if the closure wants them; nothing to delete. |
| (b) | absolute host paths in round-52 `confirmations.json` | Round 52: **16 absolute paths**, one `source_file` per entry (16 entries), all under `…/kengaku-shokunin/.ufo/waves/round-52/w2/…`. Round 53 `confirmations.json`: **0** absolute paths, **20** entries, every `report` repo-relative under `.ufo/waves/round-53/w2/`. Wave-2 reader `confirmations-part.json` files: **0**. But the five wave-2 reader **`.md` reports carry 8 absolute-path lines** in prose, which no counter reads. | Leave round-52 JSON as append-only history (as the claim says). Before landing, rewrite the 8 prose lines in `C1ConfReadA/B/C/D/G.md` to repo-relative form (L1 or reader owners). Next round: the CONFIRM report leg covers only the JSON `report` field; extend it or add a grep leg for `/home/` over `corpus/evidence/round53/` and the wave-2 reader reports. |
| (c) | C2 `SELFTEST-UNBACKED` span-scoped negation + K5/K7 controls | **Still defective at HEAD.** Whole-cell negation masks claims; the selftest has 3 fixtures and tests `collect()` not the predicate, so every mutant of the counter below survives it. Proposed clause-scoped fix + 10-fixture selftest validated in scratch: all 5 mutants killed, lane still passes with 0 `SELFTEST-UNBACKED`. **Not landed.** | Land the 61+/61- diff in `proposed.diff` next round, as one change, with the attribution fix included (a span-only negation fix alone turns the lane red, see (c)(iii)). |

## (a) `tb2-paper-full.html`

Commands and results (lane HEAD `9ead4476`, fleet tree `/home/vgpnk/Projects/shokunin/kengaku-shokunin`):

```
find /home/vgpnk/Projects/shokunin/kengaku-shokunin -name 'tb2-paper-full.html' -not -path '*/.git/*'   -> (no output, exit 0)
find . -iname '*tb2*paper*' -not -path './.git/*'  -> only ./.ufo/waves/round-52/w2/W2ScoutPriorArtFresh/receipts/fetch/tb2-paper.html
git log --all --oneline -- '*tb2-paper-full*'      -> (empty: never committed)
git status --porcelain                              -> only ?? .ufo/waves/round-53/w3.ready.dispatched and ?? .ufo/waves/round-53/w3/
ls -la …/W2ScoutPriorArtFresh/receipts/fetch/       -> 13 files; no tb2-paper-full.html
```

- **Size / sha256 of `tb2-paper-full.html`: not measurable — the file does not exist.** Its name appears in the round-52 verifier lesson as "one untracked file … (>1 MiB seat fetch)"; the >1 MiB size there is the only size on record.
- The tracked sibling `…/receipts/fetch/tb2-paper.html` is **54,333 bytes, sha256 `60d50fa9f8fcabe6776af2548867f1df8a70a104dc509886bfe11d7e156c1734`**. It is a different file and is not the carried one.
- Citations (`grep -rn 'tb2-paper-full' … --include='*.md' --include='*.json' --exclude-dir=.git | head`): `corpus/lessons/round-52-verifier-spotcheck.md:19` and `:90` (the closure's own instruction to delete it), `plans/round-53-claims.md:148` (this carried item), `.ufo/waves/round-52/w2/W2ScoutPriorArtFresh/report.md:75` (the historical `curl -o fetch/tb2-paper-full.html` command), `.ufo/waves/round-53/w1/R53MistakeSweep/sweep.md:16`, and the dispatch/registry copies of this seat's item text. Nothing cites it as a dependency; the only live consumers are the closure text.
- I did not establish when or by which command the file was removed; no git record exists because it was never tracked.
- Tool line: none.

## (b) absolute host paths in evidence

Commands (`corpus/evidence/round52/confirmations.json` and `corpus/evidence/round53/`):

```
grep -c '/home/vgpnk' corpus/evidence/round52/confirmations.json                 -> 16 (16 entries)
  5 …/round-52/w2/W2ExecConfirmA/confirmations.json  5 …/W2ExecConfirmB  4 …/W2ExecConfirmC  2 …/W2RevConfirmations
grep -c '/home/' corpus/evidence/round53/confirmations.json                       -> 0   (20 entries; keys: confirmed, line, quote, reader, report, report_sha256, task, test_id, why)
grep -rl '/home/' corpus/evidence/round53 | wc -l                                  -> 0 files
grep -l '/home/' .ufo/waves/round-53/w2/C1ConfRead*/confirmations-part.json       -> 0 files (5 parts)
grep -n '/home/vgpnk' .ufo/waves/round-53/w2/C1ConfRead*.md                      -> 8 lines
```

- Round 52 JSON: all 16 `source_file` values are absolute. Landed history; per the claim it stays.
- Round 53 JSON: 20 `report` values, all `.ufo/waves/round-53/w2/C1ConfRead{A,B,C,D,G}.md`, none absolute. The counter's `inside()` (`plans/round53_c1_triage.py:86-96`) rejects absolute and `..` paths, so the rule holds for the JSON by construction.
- Gap: the 8 prose lines (`C1ConfReadA.md:5`, `B.md:7`, `C.md:5,47`, `D.md:29,30`, `G.md:7,9`) quote absolute `Deliverable:` paths. They are not in the counter's scope; the claim's wording "round-53 evidence files … use repo-relative paths only" is true of the JSON and false of these reports. `.ufo/waves/round-53/w2/swarm-registry.json` also holds 42 absolute paths; it is a dispatch record, not evidence.
- Proposed action: relativise the 8 lines before landing (the L1 integrates; I did not edit them).

## (c) C2 `SELFTEST-UNBACKED` span fix and K5/K7 controls

### Where the defect sits (lane HEAD `9ead4476`, `plans/round52_c2_registry.py`)

- L74-75, the whole-cell negation that masks any claim in a cell containing "no … --flag" within 24 characters:
  `if re.search(r"\bno\b.{0,24}--[a-z][a-z0-9-]*", cell):` / `return False`
- L84, the flag check is a conjunction over all flags, so one absent claim is hidden by a present one: `return all(f not in body for f in flags)`
- L163-185, the selftest has three fixtures only (`clean-fixture`, `missing-fixture`, `incomplete-fixture`); L187 prints `SELFTEST cases=3 failures={fails}`. None exercises `SELFTEST-UNBACKED`, `ENTRY-MISSING` (K7) or a decoy table (K5).
- L133, `ok = not (missing or incomplete or entry_missing or unbacked or duplicate)` is the predicate, but the selftest calls `collect()` and never `verdict()`, so it cannot see the predicate.
- Round-52 defect text, `corpus/lessons/round-52.md` (table row `false-premise-in-frozen-claim`): "the C2 selftest has 3 fixtures (`clean`, `missing`, `incomplete`) and none for the negated-flag or the false-selftest control". Amendment A6 (`plans/round-52-claims.md`): the K5 (decoy table) and K7 (entry-missing) controls are "unfrozen" and "survive in `--selftest`".

### Current counter at HEAD (the same numbers the L1 will re-declare)

`python3 plans/round52_c2_registry.py --lane .` → `ADVERTISED total=77`, `REGISTERED total=77 rows=79`, `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0`, `DUPLICATE 0`, `PREDICATE R52-C2 pass`, exit 0 (`c2-lane-verdict-current.txt`). `--selftest` → 3/3 ok, exit 0.

### Measured: the five mutants against the current selftest (survive) and against the proposal (killed)

Matrix in `mutant-matrix.txt`. Mutants applied to each file; `selftest_rc` is the self-test's own exit code.

| mutant | current `--selftest` | proposed `--selftest` | lane verdict under mutant |
|---|---|---|---|
| M1 entry-missing dropped from predicate | rc 0 (survives) | rc 1, `SELFTEST FAIL K7 entry-missing rc=0 want=1` | pass |
| M2 registry block not cut at next `## ` heading (decoy table counted) | rc 0 (survives) | rc 1, `SELFTEST FAIL K5 decoy-table rc=0 want=1` | pass |
| M3 negation disabled | rc 0 (survives) | rc 1, `SELFTEST FAIL negated-flag-honest rc=1 want=0` | **current: `SELFTEST-UNBACKED 1`, `PREDICATE fail`**; proposed: pass |
| M4 unbacked leg removed from predicate | rc 0 (survives) | rc 1 (3 fixtures fail) | pass |
| M5 unbacked check always empty | rc 0 (survives) | rc 1 (3 fixtures fail) | pass |

Reading: the three original fixtures cannot see any of the five; K5 and K7 as named in A6 are exactly M2 and M1 and both survive the current selftest. Current M3 is the negation mutant of the current file; on the real lane it turns the `order-check` row red, so the whole-cell negation is currently load-bearing for `order-check`.

### (c)(i) the proposed diff (validated in scratch; not landed)

- Files: `proposed.diff` (61 `+` / 61 `-` lines), full proposed file `round52_c2_registry.proposed.py`, both in this seat directory.
- `negated_flag(clause, flag)` and `selftest_unbacked(cell, lane)` rewritten: the cell is split on `;`, `,`, `(`, `)`, newline and `. `; a clause is checked only if it names exactly one script; a flag is claimed only if it appears un-negated in its own clause and the script lacks it; any claimed flag the script lacks is a claim (disjunction, which can only fail more than the old conjunction).
- `selftest(lane)` rewritten to ten fixtures that call `verdict()` and assert exit code plus the named leg: the original three, `K7 entry-missing`, `K5 decoy-table`, `false-selftest-claim`, `negated-flag-honest`, `negated-flag-masks-claim`, `cross-clause-flag-not-claimed`, `negation-in-other-clause-not-masking`. Imports `contextlib`, `io`.
- Results: proposed selftest `SELFTEST cases=10 failures=0`, exit 0; proposed lane verdict `SELFTEST-UNBACKED 0`, `PREDICATE R52-C2 pass`, exit 0; `rows 79 … differing: []` (current vs proposed flags on every registry row, `c2-row-attribution-check.txt`).

### (c)(ii) the selftest that could not fail

While building the honest-negation fixture I found the first version was vacuous: the cell `no `--selftest` in the script` names no script, so `scripts` is empty and the counter returns False whatever the negation logic does. Mutant "negation removed" survived that version. The fixture now names its script (`` `python3 plans/tool_a.py`: no `--selftest` in the script ``), and the negation-removed mutant is then killed. Each negation fixture must name a script or it proves nothing.

### (c)(iii) why the span fix alone is not enough

I first tried only the span-scoped negation (clause-scoped negation, script still taken from the whole cell). Observed result on the lane (run in scratch; that variant's file was overwritten by the final proposal, so its output is quoted from the run, not re-run from a kept file):

```
order-check cur= False prop= True | no `--selftest` in the script; falsifiers are external — `plans/round40_c1_verify.py` mutants …; `--receipt corpus/…` …; `--claims plans/round-99-claims.md` …
lane: SELFTEST-UNBACKED 1 `order-check`   PREDICATE R52-C2 fail   exit 1
```

Cause: the `order-check` self-test cell is a single cell naming `plans/round40_c1_verify.py` as its only script, while its `--receipt` and `--claims` flags belong to `plans/order_check.py` (the row's entry column; `plans/round40_c1_verify.py` contains neither flag; `plans/order_check.py` contains both). The whole-cell negation hides this mis-attribution by accident. The final proposal scopes script association to the clause too, so no clause pairs a script with those flags and the lane passes.

The `order-check` row itself is therefore a mis-attributed cell (the round-40 script is named as the self-test host for flags it does not take). Proposed action: rewrite that cell in a later round (the L1's registry work; I did not edit `SKILL.md`).

### (c)(iv) K5 and K7 status

- K7 (entry-missing): frozen only as the fixture `K7 entry-missing` in the proposal; the current selftest has no such fixture and mutant M1 survives it. Status: carried, now with a validated fixture (killed by M1).
- K5 (decoy table): frozen only as the fixture `K5 decoy-table` in the proposal; mutant M2 survives the current selftest and is killed by the proposal. Status: carried, validated.
- Neither control is frozen in a claims file yet; the next round must freeze them before the after-run, per the A6 wording "unfrozen".

## Commands run (in order, abbreviated)

```
git rev-parse HEAD (fleet) ; git status --short
find <fleet> -name 'tb2-paper-full.html' -not -path '*/.git/*'
grep -rn 'tb2-paper-full' <fleet> --include='*.md' --include='*.json' --exclude-dir=.git | head
grep -c '/home/vgpnk' corpus/evidence/round52/confirmations.json ; python3 json load of round52 and round53 confirmations.json
grep -n 'SELFTEST|K5|K7|span' plans/round52_c2_registry.py ; sed of registry lines 1-204 (read only)
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/R53RevengerCarried/lane ; git -C … rev-parse --show-toplevel
python3 plans/round52_c2_registry.py --lane . (clone) ; python3 plans/round52_c2_registry.py --selftest (clone)
python3 plans/round53_c1_triage.py --lane . (clone; observed tail: CONFIRM new_confirmed=20 rejected=0; PREDICATE R53-C1 fail on PRIOR-ART, outside this seat's item)
scratch: prop.py / prop2.py (build proposed file, mutate both files, run selftest and lane verdict per mutant), cmp.py (row-level flag comparison)
```

Disk: `/fast` 45% used at the last check (`df -h /fast`); `disk-guard.sh status` not run (no heavy pass). Scratch removed at exit.

## Files produced

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53RevengerCarried.md` (this report)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53RevengerCarried/carried-state.txt` (items a, b evidence)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53RevengerCarried/c2-lane-verdict-current.txt` (C2 verdict and selftest at `9ead4476`)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53RevengerCarried/c2-row-attribution-check.txt`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53RevengerCarried/mutant-matrix.txt`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53RevengerCarried/proposed.diff`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53RevengerCarried/round52_c2_registry.proposed.py`

## Confidence and limits

- (a) high: existence, absence, citations and history checked with four independent commands.
- (b) high for the counts; the 8 prose lines are a judgement on the claim's wording, stated as a gap.
- (c) high for the defects (five mutants measured, the lane-level consequence measured); medium for the proposal's generality: the clause split is a lexical rule over the registry's current prose and is validated only on the 79 lane rows and the ten fixtures. Residual: `body` containment is still a substring test (`--selftest` matches `--selftest-x`), not in scope here.
- No number in this report is estimated; the matrix and verdicts are copied from run output.

tool: none (no install or upgrade this seat).
