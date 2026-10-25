# R25 NoveltySweepScout — existing interval/CI reporting on attribution accuracy

Read-only leaf (no dispatch, no lane writes). Lane master `3f371d2` (base `6180e4f`; `3f371d2` adds only `plans/round-25-claims.md`, +110 — `git show --stat`). Sweep excludes `.git/.jj/.ufo`.
Question: does anything already report an interval/bound for the attribution instrument's accuracy, per-leg recall or per-leg specificity, and does `grader.py` already hold a reusable CI helper?

## Commands and counts (whole lane)
```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
for p in 'Clopper' 'Wilson' 'betainc|incomplete beta|beta distribution|beta\.ppf' 'binomial|binom' 'rule of three' \
 'lower bound|lower-bound|lower_bound' 'confidence interval|confidence bound' '\bCI\b' 'proportion_confint|statsmodels|scipy|norm\.ppf|z-score'; do
  printf '%-45s %s\n' "$p" "$(grep -rInE "$p" --exclude-dir=.git --exclude-dir=.jj --exclude-dir=.ufo . | wc -l)"; done
```
Clopper 2 · Wilson 12 · beta/incomplete-beta 15 · binomial/binom 47 · rule of three 0 · lower bound 17 · "confidence interval" 6 · `\bCI\b` 80 · scipy/statsmodels/norm.ppf 5.
Frozen sweep, exactly as the plan writes it:
```
grep -rlE 'Clopper|Wilson|confidence interval' corpus/evidence/attrib-* plans/attrib*
→ (no output, exit 1)              # plan's "before" test HOLDS: 0 files
```
Broadened (`|confidence bound|exact interval|rule of three` added, `corpus/evidence/attrib-* plans/`) → `plans/round-25-claims.md` only.

## Hits that DO cover attribution accuracy
- `corpus/knowledge/attrib-r21.md:139` — Wilson 95% `[0.839, 1.000]` on ds 20/20, "this seat's computation". COVERS (descriptive point history).
- `corpus/knowledge/attrib-r21.md:154` — Wilson 95% `[0.851, 1.000]` on glm 22/22. COVERS.
- `corpus/knowledge/attrib-r21.md:156` — pooled 42/42 Wilson `[0.916, 1.000]`, self-labelled "a summary, not an independent n". COVERS with caveat.
- `corpus/knowledge/attrib-r21.md:374` — repeats both CIs in the "N is small … degenerate" caveat; lists per-leg n, gives **no per-leg CI**. PARTIAL.
- `corpus/knowledge/attrib-r21.md:129` — prose: "their arithmetic (counts, means, confidence intervals) from the receipts' own tables". Context, not a new estimate.
Honest "before": **0 exact (CP) intervals, 0 per-leg intervals, 0 interval-driven verdicts, 0 in-repo interval instrument; 3 descriptive Wilson CIs in one knowledge file.**

## Hits that do NOT cover attribution accuracy
- `SKILL.md:297`, `corpus/knowledge/bench-arena-round7-noise-n25.md:62` — "block-robust intervals, not per-draw Wilson": bench-arena methodology only.
- `SCORECARD.md:634` (base tree) — round-24 `## Planned (round 25)` C2 already says "Before: 0 calibrated-accuracy intervals for the instrument; after: 1": a plan, not an estimate; the construct is pre-declared at base. Note `SCORECARD.md:627-640` sets C1=calibration / C2=novelty, the reverse of `plans/round-25-claims.md` (C1=novelty / C2=calibration) — flag for the claims writer.
- t-test mean-difference CIs: `SCORECARD.md:144` (`95% CI [+0.147, +0.556]`), `LOG.md:18`, `corpus/knowledge/bench-arena-round11-power.md:39`, `bench-arena-round12-ladder.md:82,86,169,171`, `corpus/evidence/round14-fleet/r14-critic-landed.md:42`, `r14-scribe-drafts.md:214`, `grader.py:1121,1268-1271,1799,3516-3519`, r11/r12 evidence drafts.
- Prior-art neighbours already registered, not the instrument: `corpus/SOURCES.md:33` (S011 "sensitivity/specificity bias … with CIs"), `:41` (S019 CIs "for model accuracy"). No Clopper URL in SOURCES.md (only the plan's 2 mentions).

## Receipts and probe are interval-free
All 9 `corpus/evidence/attrib-*.log` → `CI=0 interval=0 Wilson=0 Clopper=0`. `grep -nE 'Wilson|Clopper|interval|1\.96|binom|betai' plans/attrib_probe.py` → rc=1, no matches (`confidence` there is the score ratio 0.538).

## grader.py reuse verdict (no second convention)
`grader.py:879 _betacf` (NR continued fraction) · `:915 betai(a,b,x)` regularised incomplete beta I_x(a,b) · `:945 _binom_cdf_le(n,k)` · `:933 t_crit` (bisection-on-tail). No CP/accuracy-CI wrapper: `dir(grader)` → `has clopper: False`, no `ci*`/`interval*` defs. Import side-effect-free (`if __name__ == "__main__"` at `:5730`); verified from `/tmp` with `python3 -B`: `betai(1,1,0.5)=0.5`, `_binom_cdf_le(10,8)=0.9892578125`; the probe wrote no bytecode (a gitignored `__pycache__/grader.cpython-314.pyc` appeared at 21:17:28 from another lane process, not this seat).
**Reuse `_betacf`/`betai`**, deriving CP bounds by bisection on `betai(k, n-k+1, p)` / `betai(k+1, n-k, 1-p)` (mirrors `t_crit`). **Do not reuse `_binom_cdf_le`**: it hardcodes p=0.5 (`/ 2.0**n`) — sign-test helper, not a general binomial CDF. Do not import the frozen evidence drafts, which duplicate `_betacf`/`betai` (`round11-fleet/grader_r11_draft.py:383,419`; `recompute_r11_draft.py:134,170`; `round11-power/recompute_r11.py:134,170`; `round12-fleet/grader_r12_draft.py:538,574`; `recompute_r12_draft.py:598,634`; `round12-ladder/recompute_r12.py:633,669`) and are immutable receipts.

VERDICT: C1 is genuinely new as *exact, per-leg, verdict-changing, in-repo* reporting, but the lane is not interval-free — 3 descriptive Wilson CIs at `corpus/knowledge/attrib-r21.md:139,154,156` (`:374` repeats) mean the claim must read "0 exact/CP + 0 per-leg + 0 interval verdicts + 0 instrument", not "0 interval estimates"; `grader.py` exposes `betai`/`_betacf` (`:915`,`:879`) to reuse and has no CP helper to duplicate.

Installs: none.
