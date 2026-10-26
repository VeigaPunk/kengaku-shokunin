# R36MutLedgerChecks — mutation probe of the C1 ledger checks (r35_d1..r35_d4) and row/predicate logic

Seat: R36MutLedgerChecks (mutation-tester), kengaku round 36 WAVE 1, 2026-10-25.
Target: `plans/round36_c1_verify.py` (digest `d7c3687c…` = frozen), ledger `corpus/defects-round35.jsonl`, spec `plans/pkg-spec-r35.json` (digest `e085b435…` = frozen), capture `corpus/evidence/round36/toolathlon-package.md` (digest `00132ab0…` = frozen).
Lane HEAD at start and end: `f9efce3beb0705ec2e04ba3f8f449d10d64cc1dd` (unchanged; all six tracked digests re-hashed identical after the run — see §5). No lane file was written; all mutations lived in disposable `/tmp` fixture clones.

## 1. Method

Fixture protocol exactly per the tasking (both clones at the same lane HEAD, verified `rev-parse --show-toplevel`):

```
D=$(mktemp -d /tmp/k36mut-XXXX); git clone -q --no-checkout --shared <lane> "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone '/plans/**' '/corpus/**' '/SCORECARD.md' '/.ufo/waves/round-34/assimilation/captures/**'
git -C "$D/lane" checkout -q master   # toplevel verified == $D/lane
```

- Fixture A (d3/d4/gate probes): the 21 committed nested round-3x paths were dropped in a fixture prep commit (author/committer recorded `fixture <fixture@invalid>`; `git log -1 --format=%an <%ae>` → `fixture <fixture@invalid>`) so d3's pristine baseline is green. Mutant paths were committed with the same identity via index plumbing (`hash-object -w` + `update-index --add --cacheinfo`), one probe per mutant, each followed by a removal commit and a restored-state re-probe.
- Fixture B (ledger/counter probes): faithful master clone (21 paths present, ledger `beea6c2e…`, all 4 rows `open`), no commits.
- Detector: `/tmp/k36mut/mutprobe.py` imports the frozen counter module and calls `CHECKS[name](lane)` (exit 0 = pass, 3 = fail); full-counter runs use `python3 plans/round36_c1_verify.py --lane .` (cwd = fixture). Every probe ran on pristine → mutated → restored bytes.
- Baseline honesty note: `plans/pkg_gate.py` is absent at W1 (not yet landed), so every full-counter run carries the constant `FIXTURES total=14 false_green=0 false_red=0 unevaluated=14`. That constant is identical across pristine and all seven ledger mutants, so the attributable ledger-layer signals are the per-row `observed/agree/note` lines and the `rows=/closed=/mismatches=` counts; the exit-1s are over-determined (battery layer and row layer both red). The d3/d4 probes had genuinely green pristine baselines; the gate-stub probes have fully evaluated batteries (`unevaluated=0`), so their fg/fr/ue deltas are attributable. 37 detector runs total (29 check probes + 8 counter runs). Raw log: `log.json` beside this report.

## 2. r35_d3 — committed nested-path counter (invariant: counts exactly `^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-` at the branch tip)

Pristine after prep commit: `rc=0 CHECK r35_d3 ok=True note=committed_nested_wave_paths=0` (master itself has `n=21`, confirmed in fixture B: `committed_nested_wave_paths=21`).

| Mutant (committed file, `fixture <fixture@invalid>`) | Expected | Observed (exit, note) | Verdict |
|---|---|---|---|
| M1 `.ufo/waves/round-34/k36probe/.ufo/waves/round-34/deep.txt` | counted, check fails | `rc=3 ok=False committed_nested_wave_paths=1` | caught |
| M2 `.ufo/waves/round-28/k36probe/.ufo/waves/round-28/deep.txt` | NOT counted | `rc=0 ok=True committed_nested_wave_paths=0` | caught (directional holds) |
| M3 `.ufo/waves/round-34/k36shallow.txt` (depth 1) | NOT counted | `rc=0 ok=True committed_nested_wave_paths=0` | caught (directional holds) |
| M4 `.ufo/waves/round-30/k36probe/.ufo/waves/round-30/deep.txt` (range edge `3[0-9]`=30) | counted | `rc=3 ok=False committed_nested_wave_paths=1` | caught |

Every removal commit restored the green pristine: `rc=0 ok=True committed_nested_wave_paths=0` after each of the four mutants.

## 3. r35_d4 — Gate erratum line + recount from the committed package copy

Pristine (genuine line `Erratum (round 36): S130 recount from the committed package copy: 13 + 23 + 1 = 37, denominator 38.` inside `## Gate`, committed capture untouched): `rc=0 ok=True note=erratum_lines=1 recount=13 + 23 + 1 = 37 stated_denominator=38`. The recount is genuinely computed: capture rows 30/32/35/36 give parts 13/23/1, denominator row `| Outcome | Count | of 38 |`.

| Mutant | Expected | Observed (exit, note) | Verdict |
|---|---|---|---|
| M1 erratum sum wrong (`… 1 = 36`) | reject | `rc=3 ok=False erratum_lines=1 recount=13 + 23 + 1 = 37 stated_denominator=38` | caught |
| M2 omits `S130` | reject | `rc=3 ok=False erratum_lines=1` | caught |
| M3 line moved out of `## Gate` (section `## Gates`) | reject | `rc=3 ok=False erratum_lines=0` | caught |
| M4 erratum line twice | reject | `rc=3 ok=False erratum_lines=2` | caught |
| M5 right numbers, `denominator 39` stated | reject | `rc=3 ok=False erratum_lines=1` | caught |
| M5c capture denominator edited to 37 AND lesson restated `denominator 37` (all strings consistent) | reject via `sum(parts) != den` guard | `rc=3 ok=False erratum_lines=1 recount=13 + 23 + 1 = 37 stated_denominator=37` | caught — a doctored capture cannot be laundered by rewriting the lesson; the arithmetic guard fires |
| M6 committed package copy edited so the table sums to 38 (`| isolated and callable \| 14 \| 38 \|`) | line becomes a defect | `rc=3 ok=False erratum_lines=1 recount=14 + 23 + 1 = 38 stated_denominator=38` | caught, exactly as tasked |
| M7 lesson absent | reject | `rc=3 ok=False round-36 lesson absent; recount 13 + 23 + 1 = 37 vs stated denominator 38` | caught |
| M8 erratum line indented two spaces | reject (fails safe) | `rc=3 ok=False erratum_lines=0` | caught |

After every mutant the lesson and capture bytes were restored and hash-verified (`lesson_sha=5a20a45a…`, `cap_sha=00132ab0…` = frozen capture digest) — recorded per probe in `log.json`.

## 4. Gate-stub mutants against r35_d1/r35_d2 (battery fully evaluated, `unevaluated=0`)

Pristine with no gate: d1 `rc=3 fixtures=14 false_green=0 false_red=0 unevaluated=14 tip_package_rc=None`; d2 `rc=3 untracked_anywhere=0 line_fixtures_wrong=6/6`.

| Mutant | d1 observed | d2 observed | Verdict |
|---|---|---|---|
| stub gate `sys.exit(0)` (accept-all) | `rc=3 false_green=11 false_red=0 unevaluated=0 tip_package_rc=0` | `line_fixtures_wrong=4/6` | caught — fg=11 reproduces frozen control `control-c1-accept-all` |
| stub gate `sys.exit(1)` (reject-all) | `rc=3 false_green=0 false_red=3 unevaluated=0 tip_package_rc=1` | `line_fixtures_wrong=2/6` | caught — fr=3 reproduces frozen control `control-c1-reject-all` |
| stub gate `sys.exit(2)` (crash) | `rc=3 unevaluated=14 tip_package_rc=2` | `line_fixtures_wrong=6/6` | caught — crash counted as observed failure, never a rejection |
| stray untracked `plans/k36stray_probe.py` (no gate) | unchanged (d1 does not read the working tree) | `rc=3 untracked_anywhere=1 line_fixtures_wrong=6/6` | caught — the working-tree class lives in d2, consistent with the claims' separability |

Restoration: stubs were index-added then index-removed and unlinked; stray unlinked; d2 re-probed `untracked_anywhere=0` both times.

## 5. Ledger file / row / predicate mutants (fixture B = faithful master, full counter)

Pristine: `rc=1` … `R35-D3 status=open observed=fail agree=yes committed_nested_wave_paths=21` … `rows=4 closed=0 observed_pass=0 mismatches=0`, `PREDICATE C1 fail` (all four open rows agree with their failing checks).

| Mutant | Observed (exit, row line, counters) | Verdict |
|---|---|---|
| unknown check name `r35_dX` (row 1) | `rc=1`, `R35-D1 status=open observed=fail agree=yes unknown check 'r35_dX'`, `mismatches=0` | caught — unknown names resolve to `ok=False` (fail closed), never a pass, never a crash |
| unknown check + `status: closed` | `rc=1`, `agree=NO`, `rows=4 closed=1 … mismatches=1` | caught |
| `status: "Closed"` (capital, R35-D3) | `rc=1`, `R35-D3 status=Closed observed=fail agree=NO`, `mismatches=1` | caught — only exact lowercase `closed` counts |
| fifth row (duplicate of row 1) | `rc=1`, row printed twice, `rows=5 closed=0 observed_pass=0 mismatches=0`, `PREDICATE C1 fail` | caught — `len(rows)==4` gate rejects the count even with zero mismatches |
| empty ledger file | `rc=1`, `FIXTURES total=14 … unevaluated=14`, `rows=0 closed=0 observed_pass=0 mismatches=0` | caught — no crash, never exit 0 |
| missing ledger file | `rc=1`, `FIXTURES …` printed, then uncaught `FileNotFoundError: …/corpus/defects-round35.jsonl` traceback | caught — fail-loud but closed: never exit 0 |
| malformed JSON (row 1 truncated at char 20) | `rc=1`, `FIXTURES …` printed, then uncaught `json.decoder.JSONDecodeError: Unterminated string…` | caught — fail-loud but closed: never exit 0 |

In all seven mutants and pristine the counter printed `PREDICATE C1 fail` and exited 1 (baseline caveat of §1 applies to exit-code attribution; the row-level deltas above are the decisive signals and all moved as the invariant requires). Ledger bytes restored and hash-verified after every mutant (`sha=beea6c2e…` each time).

## 6. Restoration / lane-integrity evidence

- Before/after lane digests identical for all six tracked files (`round36_c1_verify.py d7c3687c…`, `pkg-spec-r35.json e085b435…`, ledger `beea6c2e…`, capture `00132ab0…`, `SCORECARD.md 563433ca…`, `corpus/lessons/round-34.md 8a52fade…`); lane HEAD `f9efce3b…` before == after (`log.json` records `lane_state before/after` + `lane_untouched ok=True`).
- Both fixture clones `rm -rf`'d at the end (`fixtures_removed ok=True`). Harness and raw log archived in this seat dir: `mutprobe.py`, `orchestrate.py`, `log.json`.
- No fixture-recognizing names/markers were used by any detector; mutants are pure byte/tree edits.

## 7. Coverage findings (limits for wave 2, not contract changes)

1. A committed file directly at depth 1 (e.g. `.ufo/waves/round-34/stray.txt`) is invisible to every ledger check: d3 deliberately requires nesting, d2 reads only untracked files. Within the frozen claim's scope ("R35-D3 claims the 21 round-34 paths only") — recorded as a limit.
2. An unknown check name on an `open` row yields `agree=yes` (no mismatch raised); the fail-closed is visible only in the row note. On a `closed` row it mismatches. A wave-2 attack could exploit the open-row silence only into a missing *mismatch*, never into a pass.
3. Missing/malformed ledger crashes with a traceback after the battery prints (fail-loud, exit 1) rather than emitting a row note — non-zero exit guaranteed, cosmetics only.
4. r35_d4's `errs` uses `startswith("Erratum (round 36):")`: an indented genuine line would be invisible (`erratum_lines=0`) → false red (safe direction).

All 24 mutants were detected or respected the directional requirement; none survived as a coverage hole beyond the recorded limits.

VERDICT: ledger-mutants-24/24
