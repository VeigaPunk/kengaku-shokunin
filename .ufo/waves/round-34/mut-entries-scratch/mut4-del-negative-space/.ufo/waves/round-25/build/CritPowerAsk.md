# CritPowerAsk — critic report, r25 C1 power ask & interval rule (read-only)
Scope: attack `plans/round-25-claims.md:35-45` (verdict rule, n=17 ask, CP-vs-alternatives).
All math re-derived offline stdlib (log-space binomial tails + bisection; verified vs closed form
0.025^(1/n)). Instrument `plans/attrib_calibration.py` does not exist yet — this is pre-registration.

## Tightened power ask (pre-registered here before any instrument output; never loosens)
An estimate is PASS-feasible iff n ≥ N(e), e = observed errors:
N(0..5) = {17, 26, 34, 41, 48, 55} — CP95 two-sided lower bounds at the boundary:
(17,17)=0.8049, (25,26)=0.8036, (32,34)=0.8032, (38,41)=0.8008, (44,48)=0.8002, (50,55)=0.8005;
just-below rows all <0.80: (16,16)=0.7941, (24,25)=0.7965, (31,33)=0.7977. N(e>5) recompute on demand.
Construct meets the ask iff (a) every P1 estimate gets an interval verdict AND (b) the instrument
prints N(e) beside each INDETERMINATE row so the shortfall distance is legible.

## Findings
F1 claims.md:42-45 freezes only the zero-error threshold. "measured at or above its power ask only for
   blocks with n ≥ 17" is false for e≥1: at n=25 with 1 error CP lower=0.7965 → no PASS possible.
   The tightened N(e) table above is the correction. P5 (claims.md:56) predicts ≥1 incorrect trial;
   if it lands, N(e) binds immediately — the planner's single number would mis-report feasibility.
F2 claims.md:45 "legs below it are reported INDETERMINATE, never PASS" is overclaimed: underpowered
   legs WITH failures can FAIL — CP upper(0/5)=0.5218 <0.80. Verdict rule :35-36 is correct; the
   sentence must read "never PASS — INDETERMINATE or FAIL as the interval dictates."
F3 Rule-choice attack FAILS — two-sided CP is ratified: it is the strictest admissible rule and the
   only one compatible with a 4-outcome verdict. One-sided 95% lower hits bar at n=14 (0.8074) and can
   never FAIL (implicit upper=1). Wilson two-sided hits at n=16 (0.8064) — correctly sensitivity-only
   per :37-38. Jeffreys hits at n=11 — loosest; do not adopt. Correction: flag rows where CP and
   Wilson verdicts disagree (boundary-contested) in --summary.
F4 Multiplicity: ≥5 pre-dedup overall blocks + per-leg recall/specificity rows, each at per-estimate
   95%. claims.md:40 already labels the RG bound "conservative, not Bonferroni-exact" — extend the
   same label to the whole verdict set. Do NOT impose Bonferroni (frozen α=0.05 is per-estimate).
F5 Last-block scoping under-counts poolable power: attrib-r22-legs.log has two disjoint runs
   (:260-310 run-1, :312-362 run-2); last-block rule claims.md:30-31 scores only run-2 → hyper recall
   n=10 → CP(10,10)=(0.6915,1.0) INDETERMINATE, while the receipt's own addendum pools hyper 19/19
   (attrib-r22-legs.log:385-388) → CP(19,19)=(0.8235,1.0) PASS-feasible. Correction: keep the frozen
   authoritative verdict on the last block, but print a pooled-denominator sensitivity row when an
   earlier non-authoritative block's scored trial set is disjoint from the authoritative block's.
F6 4 of 9 P1 files have zero `## GT + scoring` blocks (r21-ds, r21-glm, r22-legs-hyper,
   r23-stream-trials — grep count 0) → trial-only per claims.md:30-31; the ask cannot be met there by
   construction. --summary must count them explicitly so "met" is judged only over contributing files.
F7 Contract ambiguity: "exit 0 = every stored point verdict re-derives from its own rows" — if read
   as verdict-letter equality, the instrument exits 1 precisely when it succeeds (stored PASS
   attrib-r22-legs.log:344 `10/10 -> PASS` must re-verdict INDETERMINATE; stored `0/0 -> FAIL` :345
   re-verdicts UNTESTED). Must mean count-recomputation consistency; a changed letter is a finding,
   not an error. --summary should print flip-category counts (PASS→INDET, FAIL→UNTESTED, etc.).
F8 Selftest gap (claims.md:62-63 mutants are necessary not sufficient): add pinned boundary fixtures —
   (16,16)→INDET, (17,17)→PASS, (24,25)→INDET, (25,26)→PASS, (0,5)→FAIL — plus constants
   CP(10,10)=(0.6915,1.0000), CP(19,19)=(0.8235,1.0000), CP(20,20)=(0.8316,1.0000). Makes the
   power gate executable, not just numeric.
F9 Ratified: two-sided is forced by the verdict rule itself (FAIL needs upper<bar); bar=0.80 reuse
   (attrib-r21-impl-ds-trials.log:297) is correct; dedup on identical trial tables (claims.md:32-33)
   is required — a miss would fake n=60 from the two r23-stream blocks (attrib-r23-stream.log:194,:258,
   same window @1792158396–@1792158594) inflating CP lower to 0.940.

## Smallest safe correction
Keep CP two-sided α=0.05 and verdict() untouched; (i) adopt the N(e) feasibility table above and print
it in --summary; (ii) reword claims.md:45 "INDETERMINATE" → "never PASS"; (iii) add F8 boundary
fixtures to --selftest; (iv) print pooled-denominator sensitivity rows per F5. No loosening anywhere.

## Falsifiable condition
This critique is wrong if the instrument produces a PASS at e≥1 with n<26 under a correctly
implemented two-sided CP95 — i.e. if pinned lower(25/26) ≠ 0.8036 (my bisection vs binom-tail is
reproducible in ~20 lines of stdlib).

VERDICT: power ask sound in spirit, under-specified in fact — tighten to N(e) table; keep CP two-sided; amend the INDETERMINATE-only sentence; instrument absent. Installs: none (stdlib only; pacman paused host-wide, unused).
