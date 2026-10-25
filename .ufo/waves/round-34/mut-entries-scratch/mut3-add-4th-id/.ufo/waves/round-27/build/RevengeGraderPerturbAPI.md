# Kengaku R27 — grader_perturb API reconnaissance

Axes: API reuse; side-effect/state safety; frozen-grader dispatch fidelity.
Scope: `plans/grader_perturb.py` SHA-256 `a9f75f4ca52668509433d9eb860d57c82df760ba8d4ce2148327a775cfb2165f`.

## Minimal import (executed)
```python
import sys
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans")
import grader_perturb as gp
pop = gp.build_population("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
assert len(pop) == 1964 and not gp._LAST["errors"]
```
Command: `PYTHONDONTWRITEBYTECODE=1 python3 -c 'import sys; sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans"); import grader_perturb as gp; pop = gp.build_population("/home/vgpnk/Projects/shokunin/kengaku-shokunin"); assert len(pop) == 1964 and not gp._LAST["errors"]; print("OK population", len(pop), "excluded", gp._LAST["excluded"], "errors", len(gp._LAST["errors"]))'` → `OK population 1964 excluded 0 errors 0`, exit 0. `plans/grader_perturb.py:187-256`.

## Reuse surface / purity
- Input-only helpers: `format_class` (`:54-62`), `_expected_for` (`:121-166`), `_answer_fence`/`_answer_span`/`_dump_like` (`:279-324`), transform helpers and `apply_family` (`:325-466`), `_verdict`/`_previous_truth`/`_unit_key` (`:469-488`), `_dedup_stats` (`:726-736`). They compute from arguments and fixed constants; `format_class` uses the committed fence regex (`:35`, `:54-62`), so a non-`json` fence classifies as `DANGLE`.
- `regrade` is read-only/deterministic once configured, but depends on mutable module global `_GRADER` (`:259-276`). `_grader_for` also reads `_GRADER.GRADED_CELLS` for the round-12 branch (`:168-184`).
- Stateful/I/O: `_load_module` registers modules in `sys.modules` (`:70-78`); `_configure` rebinds `_GRADER`, `_CP`, `_ROOT` (`:80-90`); `build_population` reads pinned files and rebinds/mutates `_LAST` (`:187-256`); `family_stats` can auto-configure and appends failures to `_LAST["errors"]` (`:504-528`); `_interval` calls cached CP (`:499-501`); `_summary` reads `_LAST` (`:739-784`).

## Configuration and records
- Call `build_population(root)` first. `root` must resolve to a tree with `grader.py` and `plans/attrib_calibration.py`; population loading also requires the four pinned JSONL paths (`:22-33`, `:80-90`, `:187-208`). `_configure` names loaded modules `_r26_grader_<sha1(root)[:10]>` and `_r26_calibration_<sha1(root)[:10]>` (`:70-90`).
- `_GRADER` must expose `extract_json_block`, `states_along`, `seq_states_along`, `GRADED_CELLS`, `CONFLICT_ROWS`, `BENIGN_ROWS`, `grade_state`, `grade_seq`, `valid_latin`, and `grade_c` (`grader_perturb.py:102-119,168-184,261-275`; definitions `grader.py:116-117,121-134,213-225,232-268,1569,2107-2123`). `_CP` is `attrib_calibration.clopper_pearson`; it is used by family statistics, not `regrade` (`grader_perturb.py:87-90,499-501`).
- `Rec` is frozen: `file,line,cell,pid,turn,grader,raw,want,stored_ok,previous=None,rep=None` (`:39-52`); population creation passes `previous` from truth replay and `rep` from the row (`:226-228`). It is not safely hashable when `want` is a dict/list: observed `TypeError: unhashable type: 'dict'`.

## Dispatch and traps
- `_grader_for`: round-8 C-* → `c`, eligible A-/B- → `state`; round-9 eligible A- → `state`; round-11 only `A-CKPT4710`/`A-CKPT710` → `state`; round-12 T-DENSE/T-SPARSE → `seq`, `GRADED_CELLS` → `state` (`:168-184`).
- `regrade` extracts once via `_GRADER.extract_json_block`; `state` → `grade_state(got,want)[0]`, `seq` → `grade_seq(got,want)[0]`. For `c`, `C-MONO` → `valid_latin(got)`; `C-conflict` → `grade_c(got, CONFLICT_ROWS, True)`; `C-benign` → `grade_c(got, BENIGN_ROWS, True)`; `C-norule` → `grade_c(got, BENIGN_ROWS, False)`; other C cell raises `KeyError`, unknown grader raises `ValueError` (`:259-276`).
- Import itself does not configure or exit: placeholders only (`:64-67`), CLI exit is guarded by `if __name__ == "__main__"` (`:841-842`; grader likewise `grader.py:5730-5737`). `regrade` before configuration was observed to raise `AttributeError: 'NoneType' object has no attribute 'extract_json_block'`.
- `_LAST` is rebound on every build (`:189-192`): use `gp._LAST` after each call; `from grader_perturb import _LAST` holds a stale dict. Pin mismatch is recorded, not raised: `/tmp` blank-line mutation returned 1964 records with one `_LAST["errors"]` entry. Duplicate `meta` pid instead raises uncaught `ValueError` (`:102-111,212-215`). Always assert clean `_LAST`; return length alone is insufficient.
- Policy reuse: `regrade` resolves the extractor attribute dynamically (`:261`), so temporarily swap `gp._GRADER.extract_json_block` only after clean population build, and restore in `finally`. Whole-output JSON mechanism probe changed 1012/1964 verdicts; building while swapped retained 952 and excluded 1012; restore + rebuild returned 1964, zero errors. Do not baseline-build inside the swap.
- First `_CP(k,n)` lazily imports a second grader copy as `_kengaku_grader` via `attrib_calibration._load_betai` (`attrib_calibration.py:107-126,143-152`); it is separate from the `_GRADER` module object.

Evidence: `python3 plans/grader_perturb.py --summary` → exit 0, `TOTAL population=1964 excluded=0 audited_verdicts=15168 policy_checks=909 families_with_interval_verdict=9`; direct regrade matched stored `ok` for all 1964 records. `PYTHONDONTWRITEBYTECODE=1` probes left lane `.pyc` inventory unchanged. Temporary files/copies stayed under `/tmp`.
Installations: none.
VERDICT: Reusable offline after explicit `build_population(root)`; protect against `_LAST` rebinding and scope extractor swaps to post-build `regrade` calls.
