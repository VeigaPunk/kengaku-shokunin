# Round 22 — natural coverage is weather, forced coverage is design: what closing the untested legs must not claim

2026-10-16. Round 22 is one axis-move (operability/coverage): cover the two
roster legs no round-21 trial reached — hyper and opencode-go, 0 GT trials
each — by forcing fallback through the ds cascade against the (extended,
re-frozen) feature table, and fold the attribution instrument into the
standing battery as probe-type P10. At lesson write time (11:33Z) the wave is
mid-flight: the fold has landed — `plans/probe-battery-TEMPLATE.md` gained
§11 "Probe-type P10 — attribution health-check" at 11:31:12Z (battery-fold-
impl seat), which already carries the forced-vs-natural wording, the ≥10
scored-trials floor, the 44-request etiquette scale, and the re-freeze
policy — but no r22 trials exist yet, the table is not yet re-frozen
(`python3 plans/attrib_probe.py block-sha` → `9f0244bb0aa4463c…ba33c`, exit
0, reproduced by this seat at 11:32Z), and the official r21 runner receipts
remain unscored (no `GT + scoring` section; grep count 0 at 11:32Z). This
note is therefore written from the landed r21 record — the four trial
receipts, the frozen table `plans/attrib-r21-frozen.md`, the scorer's
close-out `corpus/knowledge/attrib-r21.md`, and SCORECARD r21 — plus the
landed §11, and states what the round's trials must carry, before they exist
to confirm it. Where r22's landed receipts disagree, they supersede. The
prior lessons are `2026-10-16-round19-freeze-chain.md`,
`2026-10-16-round20-grid-closure.md`, and
`2026-10-16-round21-attribution-freeze-surface.md`; this note records what
the coverage move itself must learn from them. Every count, hash, and line
number below was recomputed by this seat from the landed bytes before citing
it.

1. **The r21 accuracy was real, but the coverage that produced it was
   weather — and weather is not a design property of the instrument.** The
   landed GT counts are verbatim in the receipts: ds
   `GT counts: {"alibaba-token-plan": 20}`
   (`attrib-r21-impl-ds-trials.log:296`), glm
   `GT counts: {"devin": 9, "zai": 13}`
   (`attrib-r21-impl-glm-trials.log:172`). Three of five roster legs
   exercised; hyper 0 on both shims, opencode-go 0 on ds — and the
   instrument itself prints the honesty line at every score block:
   `per-leg GT counts mean honesty note: legs with 0 GT trials are UNTESTED
   by this run`. The only leg diversity in the whole round came from
   transient zai 429 windows during one ~2½-minute window (scorer §8.2:
   "the round's best result is weather-dependent"); on a clean-zai day the
   glm GT collapses to one leg exactly as the frozen table's §5 pre-named.
   r21's lesson 6 recorded that the limits section did its job by naming
   the narrowing. This round's lesson is the other half: **a coverage
   number derived from fallback weather measures which legs happened to
   serve, not which legs the instrument can attribute.** The 42/42 = 1.000
   supports "attributes every leg that served" — the legs that did not
   serve were never measured, and no amount of accuracy on the served legs
   says anything about them. That is why SCORECARD r21 prices coverage
   "improved narrowly" and names hyper/opencode-go UNTESTED as the r22
   candidate (`SCORECARD.md:511`).

2. **Forcing closes the gap but changes the claim: forced coverage is a
   different claim than natural coverage, and the difference is
   mechanistic, not rhetorical.** The r22 design reaches hyper and
   opencode-go by forcing leg-1 (alibaba) to fail so the cascade falls
   through. Trials produced that way sample the cascade **under a failure
   condition the natural run never paid**: a forced-fallback wall includes
   the failed leg-1 attempt, so the latency bands the trials meet are
   fallback bands, not the steady-state bands the frozen table was built
   from (hyper [0.7, 3.0] from the direct-lane `probe-r19-hyper.log`
   receipts, 1485 ms POST; opencode-go [1.0, 6.5] from P7 TTFT 1724 ms +
   r18 M6 3356/4958 ms — `plans/attrib-r21-frozen.md:96,107`). If forced
   walls land outside those bands, the band features abstain — the desired
   failure mode (r21: features that abstain beat features that guess) —
   which means forced coverage validates the tells, schema quirks, and
   rewrite/echo classes far more than it validates the bands. The wording
   the round must carry, and the wording a future reader must not be
   allowed to blur: forced trials establish "the instrument attributes the
   leg under forced fallback"; they do not establish "the instrument
   attributes the leg in natural traffic". Both are worth having; they are
   not interchangeable, and a natural-coverage trial on these legs remains
   owed even after forced trials pass. Two corollaries for the receipts:
   (a) the forcing mechanism itself is part of the claim and must be
   disclosed in-receipt — "forced" is a design act, and an undisclosed
   forcing mechanism is indistinguishable from weather; (b) the ds
   error-path stays unforceable (frozen §1: the temperature body is
   servable on leg-1 alibaba, `error_path_trials: {"ds-flash-shim": 0}`),
   so forced ds fallback trials ride the standard body — the coverage gain
   is on the fallback legs, not on `error_tells`, which remain validated
   by r19 receipts and mock-smoke only.

3. **Extending the table means re-freezing BEFORE the first forced trial,
   and the extension must re-derive every filled value from landed bytes —
   the table's empty fields are the exact place where brief-composed
   errors would hide.** The r21 lesson 7 already instantiated the failure
   mode: the brief's conflated LLMmap citation was corrected in-repo at
   10:08:50Z and frozen over anyway ten minutes later. An r22 extension
   edits the most inference-laden part of the table: the hyper and
   opencode-go profiles carry marked-inferred values (opencode span class
   and id_class inferred from n=1; glm-hyper span class marked unverified
   post-redeploy) and **empty feature fields** — hyper `id_class: []` and
   `error_tells: []` (`plans/attrib-r21-frozen.md:98-99`), opencode-go
   `error_tells: []` (`:110`), glm-hyper `id_class: []` / `error_tells: []`
   (`:151-152`). Empty fields are not neutral bookkeeping: under the
   frozen additive rule a feature that cannot fire for a leg contributes 0
   to that leg only, which silently shifts relative weight toward the
   other legs — filling one is a change to the decision rule's behaviour
   on that shim, not a documentation edit. So: every value the extension
   fills needs a landed receipt behind it (r19/r21 bytes, not the wave
   brief); every value it leaves empty must be reported as still-empty in
   the r22 receipt; and the re-freeze must complete — new FROZEN line,
   double-read guard, receipts recording the new `frozen_sha256_at_start`
   — before the first forced request. The r19 BR-1 TOCTOU and the r21
   code-float lesson (lesson 1: "the freeze surface is the whole
   measurement pipeline") both say the same thing from opposite sides: the
   pin is the contract, and a pin that moves after traffic started is not
   a pin.

4. **The fold into P10 is what converts coverage honesty from a per-round
   virtue into a standing schema — and the landed §11 already carries the
   wording this lesson would have demanded.** The r20 lesson's rule — an
   aggregate over an open grid is a moving number; state `executed/total`
   beside it — applies to legs, not just probes: an attribution claim
   should state its per-leg GT counts beside the aggregate accuracy. The
   instrument already does that ("legs with 0 GT trials are UNTESTED by
   this run", printed at every score block); the landed TEMPLATE §11 now
   makes it a schema: per-leg GT counts reported and 0-GT legs named
   UNTESTED — never averaged away (`plans/probe-battery-TEMPLATE.md:465-
   468`); the ≥10 scored-trials floor with the r21 bar-refusal precedent
   (`:460-464`); the 44-request r21 scale as ceiling, not floor (`:475-
   484`); and the re-freeze policy — any feature-table change is a new
   freeze naming the superseded hash, trials run only under the new pin,
   and the instrument code is pinned beside the table
   (`instrument_sha256_at_start` / `instrument_sha256_at_scoring`, `:486-
   499` — closing r21 defect 2's code-float gap by schema). The clause this
   lesson exists to underline is already there verbatim: **"FORCED coverage
   is a different claim than natural coverage"** (`:503-510`), with the
   natural/forced GT split required in the probe's Frame field. What §11
   cannot do is run the trials: the schema's value is only as good as the
   next instantiation's compliance, and two debts stay live after it —
   (a) the re-freeze must actually happen BEFORE the first forced request
   (the sha is still `9f0244bb…` at 11:32Z; §11's policy is prose until a
   new FROZEN line exists), and (b) natural-coverage trials on hyper and
   opencode-go remain owed even after forced trials pass — §11 prices
   forced coverage as validating "the feature table against that leg's
   serve path", not discrimination under natural traffic, so a forced PASS
   must not be quoted as a natural PASS in any future close-out.

Named leftovers for the scorer/parent (recorded, not patched from this
seat):

- **The official r21 runner receipts remain unscored** (no `GT + scoring`
  section in either file; grep exit 1 at 11:29Z). Runner-B's T21
  error-path capture — a live 400 `devin_shim_error`/`invalid_argument`
  relay, blind-predicted `devin` at confidence 0.778
  (`corpus/evidence/attrib-r21-glm-trials.log:131-134`) — is the only
  live `error_tells` observation on record and sits in an unscored file;
  the owed scoring would adjudicate it. Owner per the round contract:
  scorer-r22 (the attrib note's r22 addendum).
- The r22 fold's TEMPLATE §11 + P10 schema landed mid-write (11:31:12Z,
  battery-fold-impl seat) — this lesson's §4 cites it as landed; the table
  extension + re-freeze are leg-coverage-impl's; the trials and receipts
  are the trial-runners'; this seat writes only this lesson file.
- If the forced-fallback trials cannot be produced (leg-1 alibaba refuses
  to fail through any disclosed mechanism), the honest outcome is
  NOT-RUN-with-reason on the coverage clause, not a redefinition of
  "coverage" — the r20 P9 precedent (an absence re-confirmation is a real
  scored outcome) is the model for scoring an absence honestly.
