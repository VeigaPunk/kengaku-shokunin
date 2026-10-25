# Round 21 — the freeze held the table and let the code float: what the attribution instrument's first live GT read taught

2026-10-16. One 32-seat flash wave (zai bucket) built and ran the N1
instrument: `plans/attrib_probe.py` plus the frozen feature table
`plans/attrib-r21-frozen.md` (FROZEN 2026-10-16T10:20:08Z sha256
`9f0244bb…`), ≥20 blind trials per shim against the two chat shims, journal
ground truth read only after all trials. Receipts:
`corpus/evidence/attrib-r21-{ds,glm}-trials.log` (trial-runner seats A/B)
and `attrib-r21-impl-{ds,glm}-trials.log` (instrument-impl's own validation
runs — 84 blind trials across the four files, 40 ds / 44 glm against frozen
budgets of 21/23; the duplicate execution is lesson 4). Prior-art note
`corpus/knowledge/attrib-prior-art-r21.md` (INSTRUMENT-NOVEL,
PHENOMENON-INCREMENTAL, landed 10:08:50Z). At lesson write time (~10:40Z)
the scorer's close-out (`corpus/knowledge/attrib-r21.md`) and the official
receipts' score sections had not landed; everything below cites landed
receipts only, and where the scorer's adjudication disagrees it supersedes.
The freeze-chain lessons are `2026-10-16-round19-freeze-chain.md`, the
grid-closure lessons `2026-10-16-round20-grid-closure.md`; this note records
what round 21 added. Every hash, pin, and count below was recomputed by this
seat from the landed bytes before citing it.

1. **The freeze discipline worked on exactly the surface it covered — the
   data — and every one of the round's failures lived on the surface it did
   not cover: the code.** The table's pin verified at freeze, at every
   trial start (`frozen_sha256_at_start` in all four receipts' meta lines),
   and after a post-freeze edit: the 10:28Z write was an append below the
   hashed block (a closing double-read line), and this seat's re-run —
   `python3 plans/attrib_probe.py freeze-check --double-read` →
   `FREEZE-CHECK: reads=2 block_sha=9f0244bb0aa4463c pinned=9f0244bb0aa4463c
   stable=True -> OK`, exit 0 — confirms the block untouched since freeze.
   The independent recompute of the block bytes reproduces
   `9f0244bb0aa4463c66981e5758a9a368ea0f0ea61b26882925f3ce7bbe6ba33c`
   exactly. But the instrument's own bytes were never under a pin: the
   trials ran under sha `b3e18c78…` (recorded in both trials metas), the
   GT matcher was patched mid-round (~10:26Z, lesson 2), and the scoring
   blocks were produced by a file that now hashes `effa7ea7…` — while the
   score sections record only the *table* sha (`frozen_sha256`), never the
   code sha that scored. The trials→scoring linkage is therefore
   prose-only (the impl seat's adjudication paragraph). Lesson: the freeze
   surface is the whole measurement pipeline. The table was frozen,
   double-read, and code-verified; the matcher that turns journal bytes
   into labels was mutable all round. Next instantiation pins the
   instrument file beside the table and records `instrument_sha256_at_
   scoring` in every score block — the r19 "hash the code that ran"
   clause (battery ordering chain) applied to the instrument, not just
   the plan.

2. **The scorer was never smoked against journal-shaped bytes, and it
   failed on its first live GT read while the trials phase ran clean.**
   The trials phase (sender, feature extractor, argmax) worked first
   try across 84 trials. The score phase's first journal read
   (impl-ds block, 2026-10-16T10:25:25Z) returned **every trial
   UNMATCHED**: `GT counts: {} / ACCURACY: 0/0 = 0.000 (bar 0.80, min
   scored n 20) -> FAIL`. Runner-A had already demonstrated why without
   touching the journal: the matcher's `parse_ts` applied the host's
   −0300 offset to a stamp that already carried it, shifting every
   parsed epoch +10800 s out of the ±3 s match window
   (`attrib-r21-ds-trials.log` addendum defect A, demonstrated on a
   canned line quoted from the landed `probe-r19-shim-ds-run.log:54`).
   The impl seat's adjudication names three matcher defects (A
   1-second stamp truncation, B local-offset epoch, C greedy in-order
   assignment), fixed between the ds and glm score runs — a second
   0/0 block at 10:25:58Z shows the first repair attempt did not take;
   the third block (10:26:11Z) and the glm block (10:27:03Z) score
   normally. The reusable move is runner-A's: **canned-GT smoke the
   scorer against landed journal lines from prior rounds before the
   first live read.** Prior receipts are already unblinded, so testing
   the GT join on them preserves the blind perfectly — r11's
   mock-smoke-the-runner lesson applied to the half of the instrument
   it was never applied to.

3. **A bookkeeping FAIL is not a mechanism FAIL — round 21 produced both
   kinds in one receipt and the frozen bar kept them separable.** The
   10:25:25Z FAIL meant "the GT join is broken; nothing was measured" —
   an instrument fault, not an attribution result. The 10:26:11Z FAIL
   meant the opposite:
   `ACCURACY: 18/18 = 1.000 (bar 0.80, min scored n 20) -> FAIL` — two
   trials `EXCLUDED:AMBIGUOUS(2)`, the denominator fell below the frozen
   `min_scored_trials_per_shim: 20`, and the bar **refused the shrunken
   denominator** despite perfect accuracy. Same verdict word, opposite
   mechanisms; only the receipts' detail distinguishes them. This is the
   third round running where a verdict's mechanism attribution is the
   finding (r19 3c: threshold drift, not a tier effect; r19 P6: class
   the 429 before scoring the mechanism). Standing rule the lane can now
   state outright: a verdict that cannot name its mechanism is
   uninterpretable, and a scoring gate should fail loudly on denominator
   shortfalls rather than rescale — the frozen bar did, and that refusal
   is the instrument working.

4. **A GT join key of bytes + a time window cannot distinguish your
   traffic from your twin's — and a recorded lesson is not a mechanism.**
   The frozen table pre-named the rid-collision hazard as the round's
   most likely silent failure (scribe draft D21-s7), and it materialized
   twice. (a) Even impl-ds's single-seat scoring lost two trials to
   `AMBIGUOUS(2)` via the ±5 s widening (T06/T10). (b) Two seats ran
   identical 215-byte trial bodies on the same shim with overlapping
   windows — impl-glm 10:22:32–10:24:41Z inside runner-B's
   10:21:42–10:24:04Z — putting **99 journal request-lines** in one
   scoring window (`--since @1792146147 --until @1792146311`). The
   duplicate execution itself is the r19 defect-7 pattern recurring
   (40 ds requests vs the frozen 21-request budget; 44 vs 23 on glm):
   r19's lesson said "the template should require a dispatch ledger",
   no ledger was built, and the wave duplicated work again — both seats
   disclosed it in-receipt (runner-A addendum item 1; runner-B addendum),
   which contains the damage but does not prevent the collision. The fix
   is structural, not memorial: either serialize trial windows across
   seats through a dispatch ledger, or freeze a per-seat join marker
   (nonce in the body, or seat-tagged journal lines) into the protocol
   at freeze time. A lesson that names a missing mechanism is a debt
   record; the debt comes due every wave until the mechanism exists.

5. **Mimicry ablations are an information-dependence lower bound, not a
   padding adversary — and the frozen protocol's honest_read clause is
   what kept the claim honest when every ablation passed.** The impl-glm
   score block shows all eleven ablations at 1.000 (22/22), including
   `mimicry:header-strip(hdrid)`. That does not show attribution
   surviving padding; it shows the feature set is *redundant* on this
   GT: header tells, the devin model-id rewrite, usage schema, and
   prompt-token bands each alone separate zai from glm-cascade devin
   (D2/D4 in the impl adjudication — even when billing bimodality 407/151
   or a 16 s wall pushed a band feature to abstain, the tell features
   carried). The published padding adversaries the prior-art note priced
   (Kurian's semantic-preserving output filtering; 2605.14786's timing
   randomization with classifier retraining) *inject or randomize*
   misleading signal; zeroing a weight only removes evidence. The frozen
   `honest_read` clause pre-committed the interpretation in advance, so
   the passing arm prices the claim at "no single feature is load-bearing
   on this GT" — not "attribution survives a motivated adversary", which
   this design cannot test (the legs are operator-side and cannot be
   padded from a client seat). Pre-registering the reading of the
   robustness arm is what kept a weak result from being sold as a strong
   one.

6. **GT collapse and the never-fired error path narrowed the claim, and
   the frozen table's §5 limits had pre-named both — the limits section
   did its job.** ds GT is single-leg (alibaba-token-plan ×18 scored);
   glm GT is two-leg (zai 13, devin 9); hyper is UNTESTED on both shims
   (0 GT trials, reported as the frozen table required, not averaged
   away). The accuracy numbers are real, but the claim they support is
   "attributes the legs that served", not "attributes the roster" — an
   80% bar met on a degenerate class distribution would have been a
   vacuous pass without the per-leg GT counts sitting beside it. The
   error-path arm never exercised the 400 relay live: zai accepts
   `temperature: 0`, so both err trials served 200 from leg-1 (impl
   adjudication D5) — `error_tells` remains validated by r19 receipts
   and mock-smoke only. And the abstention behaviour is the desired
   failure mode for band features: the 151-token devin billings scored
   the band 0 for *every* leg rather than misleading toward the frozen
   [326, 488] band — features that abstain beat features that guess.

7. **Relayed text outruns its own landed correction: the brief's
   conflated citation was corrected in-repo at 10:08:50Z and frozen into
   the table anyway ten minutes later.** The prior-art note's §5
   (`attrib-prior-art-r21.md:139-156`) shows LLMmap is arXiv
   2407.15847, not 2508.09021 (Kurian et al.) — yet
   `plans/attrib-r21-frozen.md:15` cites "LLMmap 2508.09021" inside the
   sha-pinned block, where the error is now permanent (errata-only; the
   pin cannot be edited). The DEFECT-B family repeats in the same
   table: the standard-body note says "233 bytes" — that is the
   r19 error-path body; the frozen std body is 215/221 B (runner-A
   addendum item 2). This is r11 lesson 6's "hashed bundles freeze
   typos" prediction, now instantiated twice in one freeze. The
   procedural gap: seats compose from the *brief*, not from the landed
   notes that supersede it. Before freezing any text, re-derive its
   citations and figures from the corpus artifacts that correct them —
   a freeze copies errors permanently and relocates the erratum outside
   the artifact it errors about.

Named leftovers for the scorer/parent (recorded, not patched from this
seat):

- **Instrument sha at scoring time is unrecorded** — score blocks carry
  `frozen_sha256` only; the b3e18c78 → effa7ea7 code change is visible
  only by comparing trials metas against the current file. Owner:
  instrument-impl, next instantiation (lesson 1).
- `cmd_block_sha` crashes (`TypeError: Strings must be encoded before
  hashing`, plans/attrib_probe.py:627) — this seat hit it; the freezer
  evidently hashed via another path since the pin reproduces. Cosmetic
  sibling: `datetime.utcnow()` deprecation warnings (runner-A addendum,
  items 2/3). Owner: instrument-impl.
- The conflated citation also sits in the scribe's
  `.ufo/rounds/round-21/goal-wave/log-entry-draft.md:68` — the fill-time
  correction is needed before LOG landing (the verdict draft already
  cites the correction at its :225-226).
- **r20 records-commit gap** (third instance of cited-but-uncommitted):
  `git show af0e3e6 --stat` lists 4 receipt logs while its message says
  "template gains freeze-after-last-edit guard" (`git show
  af0e3e6:plans/probe-battery-TEMPLATE.md | grep -c freeze-after-last-edit`
  → 0); `git show 3688f76:corpus/knowledge/probe-battery-r19.md` has no
  §10 (grep "## 10\." → 0) although the committed r20 SCORECARD section
  cites its numbers; `git ls-files corpus/lessons | grep 2026-10-16`
  returns only the round-19 file — the r20 lesson is untracked. The
  check is mechanical for the parent's landing step: every path a
  records commit cites must be tracked in that commit (`git status
  --porcelain` + `git ls-files` sweep before committing).
- Scorer close-out pending: `corpus/knowledge/attrib-r21.md` and the
  official receipts' score sections are that seat's to land; the
  aggregate verdict and the overlap adjudication (runner-B's glm window
  shares 92 s with impl-glm's) belong there.
- Hygiene: `plans/__pycache__/` (import side effect) should not land.
