# Round 27 — state_check v3 supersession mutation probe
Axes: calibration/detector sensitivity; full-token integrity; population visibility; exact-byte isolation.
Scope: three independent one-line mutants, restored between probes; no v4 implementation or live source edits.
Private clone: /tmp/kengaku-r27-MutStateCheckSupersede; observed HEAD=11a7fc8c64dc5d634331be24ccf5936f84a11f03.
Clone command: git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/kengaku-r27-MutStateCheckSupersede && git -C /tmp/kengaku-r27-MutStateCheckSupersede switch -c r27-MutStateCheckSupersede 11a7fc8c64dc; exit 0.
Instrument path below: /tmp/kengaku-r27-MutStateCheckSupersede/plans/state_check.py (v3 frozen at that HEAD).
D(flag): env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/kengaku-r27-MutStateCheckSupersede python3 /tmp/kengaku-r27-MutStateCheckSupersede/plans/state_check.py --root /tmp/kengaku-r27-MutStateCheckSupersede <flag>.
D(--selftest) and D(--summary) ran concurrently at every pristine/mutated/restored stage (120-second timeout each).
Classification: KILLED requires a stock detector's nonzero exit after a passing baseline; stdout differences are recorded separately.

## Baseline and restoration outputs
Pristine and each of the three restorations: D(--selftest) exit 0; final line begins [selftest] ALL PASS; stderr empty.
Pristine and each restoration: D(--summary) exit 0; assertions=278 match=270 mismatch=0 superseded=5 offline_unverifiable=3.
Final summary line each time: VERDICT: PASS — all comparable frozen assertions match; OUT_OF_POPULATION lines=21.
Pristine/restored selftest stdout SHA256=1165d1554060701a3b794af7ff48721b7748021db0d2af20c216510416f34900.
Pristine/restored summary stdout SHA256=c1900a591d1d67b25e8b71f3cd854405b5ea50af476ede6da8d939be08153868.
All restored stdout/stderr, commands and exit codes equal their pristine records; no inconclusive baseline.

## M1 — future-round correction rejection: SURVIVED
plans/state_check.py:197: narrow SUPERSEDE_RE from R2[5-9]-E to R2[5-6]-E; leave both strict P3 regexes unchanged.
Expected detector: --selftest should exercise its advertised R25–R29-E correction acceptance, including R27.
Actual: D(--selftest) exit 0, stdout byte-identical to pristine, still advertises R25–R29-E exact-token supersession.
Actual: D(--summary) exit 0, stdout byte-identical to pristine (278/270/0/5/3; 21 OUT_OF_POPULATION lines).
[INFERENCE] P4 cannot trust the existing green selftest to establish R27 acceptance; the narrowed shared lookup excludes R27–R29.

## M2 — partial P3 token acceptance: KILLED by selftest, not summary
plans/state_check.py:1282: replace correction[1] == derived_tokens with a non-None guard and all(token in derived_tokens for token in correction[1]).
Expected detector: the existing partial-R26-E P3a fixture must reject a correction omitting a re-derived token.
Actual: D(--selftest) exit 1; stdout empty; stderr: selftest: partial R26-E token set superseded P3a.
Actual: D(--summary) exit 0; stdout byte-identical to pristine. The committed tree alone does not expose this weakening.
Bound: this probes P3's comparison, not the separate P2 census-equality branch at plans/state_check.py:617.

## M3 — suppress population disclosure: SURVIVED stock exit checks
plans/state_check.py:1848: remove OUT_OF_POPULATION from print_summary's emission set; leave assertion creation/counting unchanged.
Expected detector: a rendered-summary assertion must require the out-of-population disclosures; internal assertion checks alone cannot do so.
Actual: D(--selftest) exit 0; stdout byte-identical to pristine; D(--summary) exit 0 and the same PASS/header.
Actual summary OUT_OF_POPULATION lines: 21 → 0; exactly 21 output lines removed. Thus an external stdout census DOES detect this mutant.
Mutated summary stdout SHA256=7b60788ac228679cc643ca58346e1d989d592b5585808a4f91dd8b9b7f6323b3.
[INFERENCE] P4 admission cannot treat green --selftest plus the summary's PASS/header as proof that excluded assertions remain disclosed.

## Source hashes and exact restoration
Original SHA256 H=32a684ffcb3fb222b0360333f83c2e4654c19ec1c3ad6ed47016052401428089.
M1: before H; mutated 97ab7fbaa2fb6a4bb356b853d939155c10970d36b7e8b3a07679cb48cb14c391; restored H.
M2: before H; mutated ca9e8ea7d3bbd397c2cf155045cc0d78ca8c6f8ab6895dbb556e193bb64f3e07; restored H.
M3: before H; mutated 68bfa92258eb5871f23afd4ebab12cf9dd047a37b4f6a058d8838ba1ebdb6bb2; restored H.
Only edited file in clone: /tmp/kengaku-r27-MutStateCheckSupersede/plans/state_check.py; final SHA256=H (all mutants removed).
No installed/updated tools; no services, endpoint requests, later-round work, or sibling/live source mutations.
VERDICT: 1 killed, 2 survived the stock CLI exit checks; M3 additionally exposed by its missing 21 disclosure lines; all source bytes and detector outputs restored.
