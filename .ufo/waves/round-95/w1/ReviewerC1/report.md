# ReviewerC1 — surgical review of R95-C1 instruments at T afe9c229

Scope: `plans/round95_vuln_probe.py`, `plans/round95-cases.json`, `plans/round95_c1_replay.py`
(diffed against `plans/round94_c1_replay.py`), the frozen-instrument table, and the path history
F→T. Lane untouched; all runs in a `git clone --shared` at T under
`/fast/scratch/hyaku/kengaku-r95/ReviewerC1/` (removed after copying receipts here).

## Bottom line

- No defect found flips the frozen R95-C1 predicate at T. The counter passes at T, rc 0.
- One major fidelity defect (F1) and two minor coverage/scope items (F2, F3). F1 would flip a
  leg of any absent-`/app/bottle.py` case; no such case is tabled, so the frozen 15-case predicate
  is unaffected. Routed to round 96; not repaired here.

## Checks performed

1. **Frozen rows, F vs T** (`raw/frozen-rows.txt`). 11 of 11 rows parsed from the
   `frozen-instruments` block of `plans/round-95-claims.md` at F `d9cd18a7`. Each path's blob sha256
   equals the table value at F and at T `afe9c229`. `ALL_ROWS_EQUAL=True`.
   `git log --full-history d9cd18a7..afe9c229 -- <11 paths>` → rc 0, empty stdout.
   `git diff --stat F T -- <11 paths>` → empty.

2. **Counter re-run at T** (`raw/c1-counter-at-T.txt`). Command, from the clone at T:
   `/usr/bin/python3 -I -B $CLONE/plans/round95_c1_replay.py --lane $CLONE --rev afe9c229... --work $S/w-c1`
   → `LEGS L1=pass ... L9=pass`, `TARGET executed_rows=39 member=fix-code-vulnerability located=1 executed=1 cases=15 legs=105 mismatches=0 defects=0`,
   `PREDICATE R95-C1 pass`, rc 0, 14.7 s.

3. **Probe re-run at T** (`raw/probe-rerun-at-T.txt`). Observation block is byte-equal to the
   official receipt `corpus/evidence/round95/vuln-probe.txt` (`sed -n /OBSERVATIONS_BEGIN/,/END/p` diff, rc 0).
   Stamps: VULNERABLE_BOTTLE_SHA 761756ce…, TOOL_SHA 932e66b1…, CASE_TABLE_SHA ff361d14…, all equal to F pins.
   Only `LANE_TIP` differs (T vs the receipt's F), which L3 accepts as an ancestor.

4. **`vulnerable()` vs the Dockerfile's two sed deletions** (`raw/sed-model-check.txt`).
   Upstream capture: 4580 `\n`; zero CR, FF, VT, FS/GS/RS, NEL, LS/PS, so `str.splitlines` and sed
   line numbering agree. Original lines 1562–1563 are the `_hkey` control-character check (`if` + `raise`).
   The second sed (`1567,1568d`) runs on the post-first file, so it removes original lines 1569–1570,
   the `_hval` check. `vulnerable()` reproduces this sequential model exactly: length 175565 and
   equal bytes. Its difflib output against upstream shows exactly those two blocks removed.
   Upstream capture sha256 also equals the GitHub raw file at `bottlepy/bottle@0207a34f`
   (`raw/upstream-github-sha.txt`).

5. **Import order vs real pytest 8.4.1** (`raw/real-pytest-vs-harness.txt`,
   `raw/real-pytest-py311-vs-predicted.txt`). Staged cases C01, C02, C07, C10, C13, C15 were run under
   bubblewrap with the test.sh invocation `python -m pytest --ctrf … /tests/test_outputs.py -rA`, cwd /app.
   Run on Python 3.11.17, the image's version (`python:3.11-slim`), and on Python 3.14.8.
   Per-test outcomes match the predicted vectors. Pass/fail is identical everywhere. The only label
   difference: the harness says `E:ValueError` where pytest says `FAILED`. Both are non-pass.
   `/tests` precedes `/app` in the harness, but `/tests` holds no bottle module, so that order is immaterial.
   The order that does matter is `/app` vs the image's site-packages. That is F1.

6. **Vacuity and leg coverage** (from the table). Per-leg value sets:
   - `exists`: P/F. `vul_file`: P/F/E:FNF/E:JSON. `cwe_id`: P/F/E:FNF/E:KeyError/E:JSON.
   - `hkey_error`: P/F. `imported`: `/app/bottle.py` / `/app/bottle/__init__.py`.
   - `hkey_basic`: P or E:ValueError only. `hkey_real`: P or E:ValueError only. **No case yields F on either.**
   Each case's docstring reason was observed to hold in the real pytest runs above. No leg passes for a reason other than its docstring.
   The normalization legs cannot be falsified by any tabled case. See F2.

7. **Counter mutants** (`raw/counter-mutants.txt`, all in a scratch clone; lane untouched, clone restored to T):
   - M1 receipt observation of C03 flipped → rc 1, `L5 fail`, `L6 fail` (`equal=False`). Bites.
   - M3 table `predicted` of C11 flipped → rc 1, `L4`, `L5`, `L6`, `L9` fail. Bites.
   - M4 receipt stamp VULNERABLE_BOTTLE_SHA altered → rc 1, `L6 fail stamps_equal=False`. Bites.
   - M2 first-occurrence `"verdict": "cases"` edit landed on `build-pmars` (23 rows carry it). The
     counter's L7 checks only this member's legacy fields, so rc 0 was correct. The mistake was mine.
   - M2b targeted edit on the `fix-code-vulnerability` row → rc 1, `L7 fail legacy_fields=False`. Bites.

## Findings

FINDING F1 major — The probe's sandbox is not the image's import environment.
- Dockerfile order: `RUN pip install .` (bottle installed into the image's site-packages from the unmodified
  upstream source) runs before the two `sed -i` oracle deletions. Those deletions touch only `/app/bottle.py`.
  So a second, unpatched `bottle` is importable in the real image. The probe's bwrap sandbox binds
  only `/usr`, `/etc`, `/app`, `/tests`, so it has no such copy. This placement is an [INFERENCE] from the
  Dockerfile; I did not have the image.
- Measured (`raw/absent-bottle-model.txt`): case = `/app` with only `report.jsonl` (solve report), no `bottle.py`.
  - Probe model (no site-packages copy): rc 1; `test_hkey_basic_cases`, `test_hkey_error_cases`,
    `test_hkey_real_world_examples` FAILED with ModuleNotFoundError.
  - Image model (upstream copy in venv site-packages, pytest 8.4.1 on 3.14): rc 0, **6 passed**.
    So deleting `/app/bottle.py` passes the grader in the image model, and the replay as built would call it failing.
- The `imported` leg cannot represent this resolution. Under the image model C15 still passes
  (rc 0, 6 passed), so the shadow case stands.
- Verdict effect: **does not flip R95-C1 as frozen** (no tabled case has `/app/bottle.py` absent). It would flip
  any absent-bottle case added in round 96. Route to R96: model site-packages in the sandbox and add an
  absent-bottle case. The claim text "the file the grader's `from bottle import _hkey` resolved to" is only
  true for the present-file cases.

FINDING F2 minor — No tabled case exercises the normalization legs' failure branch.
- `hkey_basic` and `hkey_real` are P or E only across all 15 cases. Neither yields F.
  A regression in normalization is therefore not shown by the counter. Example it would miss: `_hkey` returning
  `key.title()` without `.replace('_','-')`. `"content_type".title()` = `"Content_Type"` ≠ `"Content-Type"`, so the
  grader would fail `hkey_basic` there, but no tabled case shows it.
- Not vacuous (the legs can differ), but unexercised. Route to R96: add a title-only-normalization case.

FINDING F3 minor — Scope: the replay is the six test functions only, not the TB2 reward.
- `tests/test.sh` runs `python -m pytest --ctrf … -rA` from /app first (the bottle repo's own tests under /app/test),
  and then the captured `test_outputs.py`. Reward = both exit 0. The probe replays only the second run. The claims file
  rejects test.sh as a replay input, and the claim wording says "six test functions". So this is declared, not hidden,
  but "replayed" in the ledger must not be read as reward replay. The /app/test suite is not captured.

FINDING F4 info — Harness outcome vocabulary (`E:<Type>` vs pytest `FAILED`) differs in label only. Pass/fail
equivalence verified on 6 cases under both Python versions. No verdict effect.

FINDING F5 info — Frozen-table and path-history checks are clean (see Checks 1). Every instrument row hashes equal at F and T,
and no commit touched them after F.

FINDING none for the frozen predicate: `LEGS L1..L9 pass`, `PREDICATE R95-C1 pass`, rc 0 at T (re-run, Check 2).

## Verification gaps

- The image itself was not available. F1's site-packages placement is inferred from the captured Dockerfile.
- The bottle repo's own test suite (the first pytest run) was not captured. Its outcome is unknown. See F3.
- Under pytest, the C02 `exists` leg reports FAILED where the harness reports F; same outcome, label differs.

## Tool installs (recorded per operator directive)

- `uv pip install pytest==8.4.1 pytest-json-ctrf==0.3.5` into scratch venvs `venv-host` (host /usr/bin/python3 3.14.8)
  and `venv-311` (uv-managed cpython 3.11.17, pre-existing interpreter). Channel: uv. Reason: real pytest run
  to test import order. Scratch only; no PATH or system change. uv 0.13.0 was pre-existing and not installed by this seat.
- No pacman. No `~/.local/bin` writes. No sysctl change. bwrap used as-is (/usr/bin/bwrap).

## Raw receipts

`raw/frozen-rows.txt`, `raw/c1-counter-at-T.txt`, `raw/probe-rerun-at-T.txt`, `raw/sed-model-check.txt`,
`raw/upstream-github-sha.txt`, `raw/real-pytest-vs-harness.txt`, `raw/real-pytest-py311-vs-predicted.txt`,
`raw/absent-bottle-model.txt`, `raw/counter-mutants.txt`, `raw/tool-install-record.txt`.
