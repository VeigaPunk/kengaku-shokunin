# R46W2C1HoStore — held-out git store indirection

Axes: calibration (primary); coverage of hostile store/ref patterns (secondary).

## Counterexample

Authored one new module, `heldout-refs-indirection`, using a fresh plain-init repository, then replacing `.git/refs` with a symlink to a sibling directory outside the fixture. This tests git refs store indirection; it is not a variant of either frozen inventory. `plans/sealed46/` already contains `s_refs_link.py` and `p_refs_redirect.py`, so the exact symlink surface is not novel; this probe is an independent hostile module corroborating that behavior, not a new bypass.

## Evidence

Clone identity: `git -C /fast/scratch/hyaku/kengaku-r46/R46W2C1HoStore/lane rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r46/R46W2C1HoStore/lane`; `git -C ... rev-parse HEAD` → `42d5043afac952fcb43bf4798757785dd258cf85`.

Ran the pinned counter machinery, one module only:

`envelope.sh "$S/env" python3 .../plans/round46_c1_verify.py --lane "$S/lane" --work "$S" --jobs 1 --refusals "$S/modules"`

The saved full receipt is `receipts/counter.txt`. Envelope declared the run, and ended `exit=1 local_bin_content_before=... after=... unchanged` (not exit 4 / INVALID). Relevant counter output:

- `FENCE-RUN refusal modules/h_refs_store.py heldout-refs-indirection BREACH touches=0 calls=468 -- BREACH lane/.git/refs is a symlink`
- `REFUSAL h_refs_store.py clean fixtures=1 admitted=0 hung=0 touches=0`
- `REFUSALS total=1 clean=1 leaked=0 read=0 hung=0 build_errors=0`
- `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`
- `PREDICATE C1 fail`, solely because override inventory has one module (`REASON refusals-total=1!=20`).

Counts: modules written **1**, admitted **0**, read **0**; module result **clean** (not HUNG). No leaked outside access observed. The counter run is a targeted inventory override, not a valid full C1 predicate measurement. Scratch removed by `scratch_guard.py safe-rm`.

## What survives / smallest correction

This counterexample does not falsify the landed fence: it refused the external refs link before admitting the fixture. The claimed store boundary survives this probe. No correction warranted from this evidence. Since the frozen sealed inventory already covers refs links, retain the distinction in future reporting: this is corroboration, not independent family novelty.

VERDICT: heldout-store-1-admitted-0-read-0