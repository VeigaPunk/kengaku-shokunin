# R46W2C1HoArgv — held-out argv/env probes

Detector: pinned `plans/round46_c1_verify.py` from the cloned lane, with `--refusals` and `--sealed` both overridden to the scratch probe directory (the counter therefore runs each custom module in both groups). Each module has one fixture. The output reported both fixtures as `ADMIT`, `touches=0`; rollup `LEAKED` is the detector classification for admission, not a claim that an outside path was observed.

Clone identity: `git -C /fast/scratch/hyaku/kengaku-r46/R46W2C1HoArgv/lane rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r46/R46W2C1HoArgv/lane`; `git -C ... rev-parse HEAD` → `42d5043afac952fcb43bf4798757785dd258cf85`.

Modules written: 2. Module outputs:
- `h_anchor_dotdot.py` / `heldout-anchor-dotdot` (anchor): argv `--lane <lane>/../lane --verbose`; `FENCE-RUN ... ADMIT touches=0 calls=492`; rollup `LEAKED fixtures=1 admitted=1 hung=0 touches=0`.
- `h_order_token.py` / `heldout-order-env-token` (order): valid in-fixture lane, claims, and receipt values; `FENCE-RUN ... ADMIT touches=0 calls=517`; rollup `LEAKED fixtures=1 admitted=1 hung=0 touches=0`.

Counter totals from the same run: PINS total=65 mismatched=0; HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0; custom refusal total=2 leaked=2 read=0 hung=0 build_errors=0. The two probes were also counted under SEALED because the same directory was passed to both overrides. `PREDICATE C1 fail` is expected here because the testing override has only two modules rather than the frozen 20/12. No `READ` or `HUNG` result.

Envelope output: `ENVELOPE /usr/bin/bwrap ... -- /usr/bin/python3 ...round46_c1_verify.py ... --jobs 1 --seed 46`; exit line `ENVELOPE end ... exit=1 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged` (measurement valid; no exit-4/INVALID).

Interpretation: these fixtures do not establish an actual outside-directory access. The dot-dot argv token normalizes back inside the fixture; the order fixture uses ordinary in-fixture paths. Both were admitted with zero traced outside touches. Thus 2 admitted per detector classification, 0 reads; this is a coverage finding on these test inputs, not proof of a fence breach.

VERDICT: heldout-argv-2-admitted-2-read-0
