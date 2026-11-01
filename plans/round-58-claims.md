# Round 58 claims freeze (kengaku, hyaku run 13, 2026-11-01)

Base `a6b209cf434dae69f924858b4ea9a1bcf015eecc` (the round-57 verifier spot-check tip).
This freeze is written and committed BEFORE the first execution of the round-58 probe
against the TB2 capture (the r57 discipline; the probe's plumbing is proven only against a
toy grader, `--selftest` 2/2). Probe instrument `plans/round58_c2_kl_probe.py` self-pin:
sha256 `51c192f2f98186acb439cb69c2e0370860c362e3bdcb267afea93cd547fa6760`.

Carry-in discharged first this round (before this freeze): the R57-W1 before-count erratum
is re-derived from base bytes (below) and every before-anchor this round cites is measured
against the base commit's bytes with `git show <base>:<path> | grep -c …` (the R57-W1 fix),
or run on a clean master clone at the base tip.

## R57-W1 erratum (carried from the round-57 non-author closure — dated, naming the negation)

The round-57 report/claims/SCORECARD cite the R57-C2 before-count
`grep -c 'fourteenth' PROVINCE.md` → **0** at base `c9ce9a71`. Re-measured against the
base commit's bytes, the true value is **1**: the round-56 PROVINCE section already
contained the word inside its own negation — "this round adds the oracle, **not a fourteenth
task**", `PROVINCE.md:683`. The honest before→after by the plain cited command is 1→3; 0→3
holds only for occurrences round 57 added. The load-bearing controls (S205 absent at base,
probe instrument absent at base, SOURCES 197 rows at base) were and remain true. Re-derived
this round from base bytes:

    git show c9ce9a71:PROVINCE.md | grep -c fourteenth   → 1  (line 683, the negation)
    git show a6b209cf:PROVINCE.md | grep -c fourteenth   → 3  (the negation + the two r57 occurrences)

Standing rule adopted (R57-W1 fix): every cited before-count is re-run against the base
commit's bytes before it is frozen, and **counting anchors must exclude negations** — where
a prose anchor could match a negation ("not a fifteenth …"), a structural anchor is used
instead (a SOURCES row id, an instrument path, a ROW-line pattern). This round's anchors
below are all structural; `fifteenth` is verified 0 at base from base bytes
(`git show a6b209cf:PROVINCE.md | grep -c fifteenth` → 0, rc 1) before it is used.

## R58-C1 / operability — the R56-F1 QUOTE_RE repair, its falsifier fixtures, and the defect it exposes

Routed twice (`corpus/routed-findings.jsonl` R56-F1, opened round 56, disposition
routed-to-future-claim; planned r57, carried): the r46 `plans/anchor_line_check.py`
QUOTE_RE (`"(.*?)"`, non-greedy, escape-blind) terminates at the first double-quote inside
an anchor cell's `\"` escape and ingests the trailing backslash, so S201's byte-true
escaped-quote anchor yields the truncated string
`assert sorted(move) == sorted(["g2g4\` — not a substring of the cited line — a FALSE
`line` defect. Falsifier fixtures (built this round BEFORE the fix, receipts
`.ufo/waves/round-58/recon/esc-falsifier.txt` for the OLD checker at base and
`esc-falsifier-fixed-checker.txt` for the repaired checker, each a git-tracked fixture lane
whose capture is the real chess-best-move capture, sha256 a540714e…8f286, anchors in the
landed single-backslash cell style):

- **fx-good** — escaped-quote anchor, byte-true quote on the cited line, CORRECT wc -w
  count (5): the OLD checker reports `ROW … state=live defects=line:1`, exit 1 — the false
  positive, reproduced (kill target). Prediction: the FIXED checker reports no defect for
  this row (exit 0, live=0).
- **fx-red** — escaped-quote anchor citing a line that does not hold the quote: the OLD
  checker reports `defects=line:1` — a TRUE positive. Prediction: the FIXED checker still
  reports `line:1` (exit 1) — the repair must not overcorrect.
- **fx-words** — escaped-quote anchor, byte-true quote, MIS-COUNTED words cell (6 where the
  quote's wc -w count is 5 — the landed S201 shape): the OLD checker reports
  `defects=line:1` — the words defect is HIDDEN by the parse bug. Prediction: the FIXED
  checker reports `defects=words:1` (exit 1) — the repair EXPOSES a real, previously
  invisible defect class.

Freeze-time prediction for the lane itself: with the fixed QUOTE_RE, S201's own anchor
parses whole for the first time; its `(6 words)` cell miscounts the quote (5 tokens by the
checker's own wc -w convention, `len(quote.split())`), so S201 flips from the false
`line:1` to a TRUE `words:1` — and lands `repaired` (not `live`) only when a superseding
row corrects the count. The fix therefore lands with **S213**, a Q34 supersession row for
S201 carrying the corrected `(5 words)` anchor (same commit, same capture sha), authored
this round; the checker then prints `ROW S201 state=repaired by=S213 defects=words:1`,
`live=0`, exit 0. The repair's gate-consequence chain, all frozen now:

- `plans/round46_c2_verify.py` leg A (anchorline) returns to `live=0 repaired=9`
  base_missing=0 base_changed=0 (measured green at r56's tip `1315234b` before S201
  existed; the counter imports `plans/anchor_line_check.py` live), leg D (the checker
  `--selftest`, now 6 cases incl. the three escaped-quote fixtures) stays exit 0 — so
  `round46_c2_verify` flips red→green: `PINS total=3 mismatched=0`, `checks=4 defects=0`,
  `PREDICATE C2 pass`, exit 0. The PINS dict's ALC digest is refreshed to the repaired
  checker's sha256 IN THE SAME LANDING (the frozen claim authorizes the gate change — this
  document is that freeze), and the SKILL registry row `round46-c2` cells carry the dated
  refresh. The entry-truth ledger row `round46-c2` (red since r56) is honestly re-declared
  green with the measured fragment, same landing.
- R56-F1's findings row closes (fix + falsifier fixtures + this freeze); a NEW finding row
  R58-F1 records the exposed S201 words miscount and its same-round supersession closure.

Counting commands (structural anchors, negation-free):
before at the base clone: `python3 plans/anchor_line_check.py --lane .` →
`ROW S201 state=live defects=line:1` … `ANCHORLINE … live=1 cells=1`, exit 1 (receipt
`recon/anchor-before.txt`); `python3 plans/round46_c2_verify.py --lane . --work <scratch>`
→ `A anchorline live=1 … DEFECT`, `PREDICATE C2 fail`, exit 1.
after at the landing tip: same two commands → `live=0` exit 0 and `PREDICATE C2 pass`
exit 0; `python3 plans/anchor_line_check.py --selftest` → 6/6 (RED, GREEN, JUNK unchanged;
fx-good clean; fx-red line:1; fx-words words:1). Target axis verdict: operability held at
10 (the gate's verdict becomes correct on the full registry sample; the score's ceiling
does not move — the freeze predicts "held 10", the close reports what measured).

## R58-C2 / freshness — the round50-c1 population-pin root cause, closed with evidence

Carried open twice (r56 corrections, r57 lesson): `python3 plans/round50_c1_verify.py
--lane .` at base prints `POPULATION fixtures=126 pin=b5197f94… mismatched=125`,
`PREDICATE R50-C1 fail`, exit 1 (receipt `recon/round50-before.txt`, full run) — the r50
pin freezes per-fixture canonical tree identities built on the round-50 host; on this host
(git 2.56.0, WSL Ubuntu-24.04) the identities drift. Root-cause evidence gathered this
round, BEFORE any disposition (receipts `recon/r50-ev3/`):

1. Per-fixture rebuild of all 126 population fixtures on this host: **0/126 match the
   pin** under the builder path (`recon/r50-ev3/table3.txt`), while the counter's own run
   the same day printed mismatched=125 — i.e. ONE fixture matched the pin under the
   counter's build and not under an independent rebuild seconds later: a fixture whose
   built identity is NOT reproducible run-to-run on this host. The double-build
   discriminator (`r50_table2.py`: every fixture built twice, identities compared) names
   the unstable fixture(s) (`recon/r50-ev2b/`).
2. The drifted identities' content is dominated by git-created store files — the fixture
   builders construct git repositories (`git init`/`git add`/… via the round-44 builder
   `Ctx`), and the store bytes (`hooks/*.sample` templates, `config` text, ref files) are
   produced by the git binary at build time, not by the modules' own content.
3. The pin was frozen by the round-50 host's git; this host's git is 2.56.0 (recorded in
   the receipt). Store bytes are git-build-dependent (template sets and config text move
   across git versions), so a cross-host byte-identity pin on git-created store files
   cannot re-resolve under a host change — the drift is a stable host property
   (125–126/126 across three independent rebuilds today), not landing rot.

Disposition (frozen now, executed in the same round): **re-pin the population on this
host** — rebuild all 126 fixtures, verify per-fixture build determinism (each fixture's
identity equal across two builds), write the new `plans/honest50/population.txt` preserving
every row's other columns, stamp `POPULATION_SHA` in `plans/round50_c1_verify.py` to the
new file's sha256, and date both (the old-host pin stays in git history).

The pre-freeze discriminator verdict (measured BEFORE this freeze, so this branch choice is
data, not hope): every fixture built twice on this host in the counter's own environment
(native-fs work dir, WSL Ubuntu-24.04) — `match_b1=1 unstable=0` (`recon/r50-ev2n/
table2.txt`): all 126 fixtures are build-deterministic here, exactly one matches the r50
pin (n10-empty-repo, the sole fixture whose build runs no git plumbing beyond `git init`;
it is stable and EQ-pin across three further rebuilds, `recon/r50-ev3n/stability.txt`), and
the other 125 deterministically differ. The fallback branch (an un-re-pinnable unstable
fixture) did not fire.

Prediction: after the re-pin (branch A), the counter at the landing tip prints
`POPULATION fixtures=126 pin=<new> mismatched=0 build_errors=0`, `HONEST fixtures=126
admitted=126 refused=0 error=0`, `REFUSALS total=20 clean=20 leaked=0`, both `SEALED …
leaked=0`, `MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met`, `PREDICATE R50-C1
pass`, exit 0 — and the entry-truth ledger row `round50-c1` (red since r56) is honestly
re-declared green same-landing. Target axis verdict: freshness — the drift instrument
class gets its stale pinned expectation root-caused and re-resolving on the live host;
freeze target 9→10 (the rubric's +1 anchor: every pinned expectation the lane carries
re-resolves in-repo; cap lines clear), close reports measured.

## R58-C3 / coverage — the fifteenth grader read and executed: the corpus's first tolerance-band gate (lowest owned axis, L0-capped)

Ground: terminal-bench-2 `distribution-search` @ the same pin `2fd12b88` — a task in the
lane's home domain (the instruction frames the construction as LLM-confidence metrics via
KL divergence, S212). The graded property is new to the corpus's executed sample: the
decisive leg asserts |KL(P||U) − 10| ≤ 1e-3 AND |KL(U||P) − 10| ≤ 1e-3 — a numeric
TOLERANCE BAND on two aggregated functionals, not an exact comparison. Class novelty
checked against the corpus's own taxonomy before the freeze: the 14 executed graders decide
exact properties (membership/multiset/regex/service/dual-runtime/exact-set/wall-clock); the
words "tolerance/divergence/entropy" appear in knowledge entries only as incidental prose
(checked this round; e.g. polyglot's "toolchain tolerance" is about gcc warnings). No
prior tolerance-band grader exists in the executed sample.

Predictions (the probe's 12 cases × 4 legs, 48 predictions, ZERO U — the deterministic
contrast with r57's timing gate; per-case static readings are in the probe docstring and
the oracle note):

| case | exists | shape | validity | kl |
|---|---|---|---|---|
| sol (the oracle solver's accepted point, frozen literals) | P | P | P | P |
| uniform (1/V everywhere) | P | P | P | F |
| kb-only-m7 (backward-solved two-level, kf=9.9715) | P | P | P | F |
| minzero (atom 0 = 0.0) | P | P | F | F |
| negatom (atom 0 negative) | P | P | F | F |
| nanatom (atom 0 nan) | P | P | F | F |
| sumdrift (sol × 1.001) | P | P | F | P |
| wrongvocab-m5 (100000 atoms) | P | F | P | F |
| twod (sol as (2, 75000)) | P | F | P | P |
| maxover (atom 0 = 1.2, rest negative) | P | P | F | F |
| tolbnd (middle level +5.2e-4 relative — a different distribution inside the band) | P | P | P | P |
| intcounts (raw integer counts) | P | P | F | P |

Static readings behind the non-obvious cells: the validity leg runs on the RAW array
(sumdrift's |sum−1| = 1e-3 fails its 1e-5 band; intcounts' max ≈ 4.5e11 fails max ≤ 1)
while the kl leg renormalizes first (sumdrift and intcounts pass it — leg 4 is blind to
scale); minzero's 0.0 atom breaks the backward-KL log domain (kb → +inf, kf → nan); twod
fails only ndim — P.size and np.sum are shape-agnostic. The `sol`/`tolbnd` constants are
frozen from an authoring-time run of the maintainer's own three-level solver (S211; values
in `corpus/evidence/round58/kl-oracle.md`).

Counting commands (structural anchors): before, from base bytes:
`git show a6b209cf:PROVINCE.md | grep -c fifteenth` → 0 (rc 1);
`git show a6b209cf:corpus/SOURCES.md | grep -c S209` → 0 (rc 1);
`git cat-file -e a6b209cf:plans/round58_c2_kl_probe.py` → absent. After:
`python3 plans/round58_c2_kl_probe.py --lane . --work <scratch> --receipt
corpus/evidence/round58/kl-probe.txt` → `cases=12 legs=48 mismatches=0 setup=0
predicted_u=0`, `PREDICATE R58-C3 pass`, exit 0; `grep -c fifteenth PROVINCE.md` → ≥1
(the round-58 section only; no negation uses the word — checked); `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
corpus/SOURCES.md` → 205 (201→205). Capture sha-refusal kill (after landing, scratch
clone, one byte appended): `SETUP grader sha256 … != frozen pin`, exit 2. Target axis
verdict: coverage predicate met with the score HELD at 7 (the standing unanswered L0
`kengaku | round-25/33/51` cap, the r56-C3/r57-C2 shape); the ground moves 14→15 of 89 and
the class line moves — the report says so instead of moving a capped number.

## Sources opened this round (the round-58 Gate; all at pin 2fd12b88, 2026-11-01, bytes hashed on arrival, captures committed)

| row | URL and location | access date | located quote (at most 25 words) | decision |
|---|---|---|---|---|
| S209 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/distribution-search/task.toml — task.toml:6 (`[task] description`) | 2026-11-01 | Tests the ability to find a probability distribution satisfying precise dual KL divergence constraints through numerical optimization. (17 words) | admit A — the task's machine-readable self-definition; declares the dual-KL construction objective; sha256 `70c8e73c…3b681` |
| S210 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/distribution-search/tests/test_outputs.py — tests/test_outputs.py:80 (`assert kf_error <= TOL`), :10 (TOL = 1e-3) | 2026-11-01 | assert kf_error <= TOL (4 words) | admit A — the executed scoring predicate; the decisive dual-tolerance leg; sha256 `02bca54d…4ed`; capture committed |
| S211 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/distribution-search/solution/solve.sh — solution/solve.sh:122 (the backward-KL residual) | 2026-11-01 | E2 = A * lh + B * lm + C * ll + V * (LOG_V + TARGET) (19 words) | admit A — the maintainer oracle: a three-level count-scan Newton, an explicit inverse construction; sha256 `19daaee1…8bbe`; capture committed |
| S212 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/distribution-search/instruction.md — instruction.md:3 | 2026-11-01 | The confidence of a token prediction in an LLM can be quantified using different metrics. (15 words) | admit A — the agent-facing instruction; the task is in the lane's home domain (LLM confidence via KL); sha256 `aba2e183…8915`; capture committed |

Sourced claim: R58-C3 rides S209–S212 + the oracle note + the probe receipt. Rejections
this round: none (all four opens admitted; the same fetch-hash-commit discipline).

Flip check: no existing SOURCES row's status/recheck/used-by cell changes this round,
EXCEPT the Q34 supersession pair in R58-C1 (S201 keeps its cells as landed; S213 is a NEW
row superseding it — the corrections convention; no in-place row rewrite).
