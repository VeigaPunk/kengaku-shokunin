# R46W2NoHarm — round 46 no-harm check

## Method and pins

Clean clones created under `/fast/scratch/hyaku/kengaku-r46/R46W2NoHarm/`. `git rev-parse --show-toplevel` / `HEAD` verified:
- TIP: `/fast/scratch/hyaku/kengaku-r46/R46W2NoHarm/lane`, `42d5043afac952fcb43bf4798757785dd258cf85`.
- Base: `/fast/scratch/hyaku/kengaku-r46/R46W2NoHarm/base`, `64ba8385ea10af1b78d367dcb242b92d97062af7`.

Every check ran through `.ufo/waves/round-46/claims/envelope.sh "$S/env"`; its start/end lines reported unchanged `local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398`. Both revision identities above are the exact checkout measured in each clone.

## Results (command → TIP / base)

1. `python3 plans/round45_c2_verify.py --lane .` → exit 0 / exit 0; both `checks=11 defects=0`, `PREDICATE C2 pass`. TIP V1 says listed=9, bad=0, extra=0; base likewise. **No harm.**
2. `python3 plans/round45_c1_verify.py --lane .` → exit 0 / exit 0; both `PREDICATE C1 pass`, `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; both `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`. TIP fence digest `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`; base `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`. The round-45 verifier remains pinned to the old 10-module refusal set and reports 10 advertised; its pass does not assess the repaired round-46 fence. **Given the fence changed, a changed fence digest is expected; no changed verdict is expected for this legacy counter.**
3. `python3 plans/round44_c1_verify.py --lane .` (as its docstring specifies) → exit 0 / exit 0; both `BATTERY fixtures=33 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0`, `PREDICATE C1 pass`. **No harm.**
4. `python3 plans/round44_c2_verify.py --lane .` (as its docstring specifies) → exit 0 / exit 0; both `checks=11 defects=0`, `PREDICATE C2 pass`. **No harm.**
5. `python3 plans/routed_open.py` → exit 0 / exit 0; TIP `ROWS total=71 open=27 blocked=1 closed=41 refused=2`, `routed_open=28 oldest_round=39`; base `ROWS total=60 open=23 blocked=1 closed=34 refused=2`, `routed_open=24 oldest_round=39`. The increase reflects newly recorded work; no command failure.
6. Exact requested `python3 plans/round_close.py --lane . --round 45` → exit 2 / exit 2, both `ROUND-CLOSE ERROR no census script (scripts/sources-census.sh); pass --census PATH`. This is an environment/discovery invocation issue, not a differential regression. Re-run with the documented explicit census option: `python3 plans/round_close.py --lane . --round 45 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` → exit 0 / exit 0, both `ROUND-CLOSE RESULT PASS exit=0`; two receipts passed ORDER and census reported `exit=0 warnings=15 verdict=PASS`. **No harm when supplied the required census dependency.**
7. `python3 plans/anchor_digest_check.py --lane .` → exit 0 / exit 0; TIP `rows=165 tokens=71 defects=0`; base `rows=149 tokens=55 defects=0`. **No harm.**
8. Census `.../scripts/sources-census.sh validate --file corpus/SOURCES.md` → exit 0 / exit 0, 15 identical W04 duplicate-URL warnings and final `file ok .../corpus/SOURCES.md` on each revision. **No harm.**

## Verdict

Among eight required check legs, zero are red at TIP and zero are red at base when round-close is run with its documented explicit `--census` dependency. The exact command as written for round-close is red at both revisions (exit 2), and is recorded above rather than hidden; the same invocation defect is not introduced by TIP.

VERDICT: noharm-legs-8-red-at-tip-0-red-at-base-0
