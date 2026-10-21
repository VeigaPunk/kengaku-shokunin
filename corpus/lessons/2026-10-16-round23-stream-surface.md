# Round 23 — the request flag is an instrument surface: what the shim's stream path changes about both the forcing and the features

2026-10-16. Round 23 is one axis-move (coverage): reach the one roster leg
no round has ever measured — opencode-go, 0 on-target GT trials — through the
ds shim's **stream path**, which the r22 record explicitly left
uncharacterized (`plans/attrib-r22-frozen.md:76`: "the shim's stream:true path
chooses the leg from response HEADERS before any body byte and never scans for
FAIL markers … a marker bait cannot force a fallthrough on a streamed
request"). This note is written at 13:33Z with the wave **mid-flight**: no
round-23 artifact has landed — no `stream-trial` mode, no v3 table, no
round-23 receipt, no `.ufo/rounds/round-23/` directory (verified: `grep -rn
"stream-trial\|stream_trial\|v3\|attrib-r23" plans/ corpus/` returns only
unrelated `v3` hits; `find . -newermt "2026-10-16 12:00" -type f` returns
nothing outside `.git`/`__pycache__`). Everything below is therefore derived
from bytes that HAVE landed: the operator's shim source read-only
(`~/.local/share/ds-flash-shim/shim.py`, sha256
`42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386` —
recomputed by this seat and byte-equal to the pin carried in **both** frozen
tables), the instrument `plans/attrib_probe.py` (bb6bd919…), the frozen v1/v2
tables (block shas `9f0244bb…ba33c` and `77b8d4a0…90238`, both reproduced by
this seat: `block-sha` exit 0, `freeze-check --double-read` → `stable=True ->
OK`, exit 0), and the landed r22 record + addendum. Where the round's landed
receipts disagree, they supersede this note. The prior lessons are
`2026-10-16-round19-freeze-chain.md`, `2026-10-16-round20-grid-closure.md`,
`2026-10-16-round21-attribution-freeze-surface.md`, and
`2026-10-16-round22-leg-coverage-forcing.md`; this note records what the
stream-path move itself must learn from them.

1. **The `stream` flag selects a second leg-selection surface, not a
   transport detail — and the shim says so in its own docstring.** The landed
   shim's module docstring states the mechanism outright: *"for `stream: true`
   the leg is chosen from the response HEADERS before any body byte is
   streamed; the successful leg's bytes are then relayed to the caller as-is"*
   (`shim.py:25-27`). The code matches: after the status checks, the request
   splits at `if stream:` (`shim.py:270`), and the streaming branch returns an
   `ok` verdict from headers alone — `return {"ok": True, "status": status,
   "headers": resp_headers, "body": None, "resp": resp, "conn": conn}`
   (`:277-278`) — before the non-stream branch ever reads the body
   (`data = resp.read()`, `:281`) or inspects it for a failure marker
   (`marker = _marker_in(data)`, `:291`). `_marker_in` is defined at `:184`
   and called exactly once, at `:291` — inside the non-stream path only. So
   the FAIL-marker scan that classifies a leg's 200 as a failure **does not
   exist** on the stream path: the shim trusts the status line. The
   consequence for this lane is not a nuance: a "leg" is a different object on
   each path. On `stream:false` a leg is served only if its status is 200 AND
   its body lacks a marker (`:291-294`); on `stream:true` a leg is served if
   its status is 200, full stop. The r21 lesson's clause "the freeze surface is
   the whole measurement pipeline" is right, and this is its second half: the
   pipeline has a branch, and each branch is its own surface.

2. **The forcing mechanisms do not transfer across the flag — and that is a
   mechanism fact, not a hypothesis.** The r22 opencode-go forcing is a
   **body-stage** mechanism: it asks a compliant leg to echo a FAIL-marker
   substring ("usage limit", in `FAIL_MARKERS`, `shim.py:65-90`) so the shim
   itself classifies that leg's 200 as a failure and advances
   (`shim.py:291-294`). On `stream:true` that path is never reached — the
   marker is never looked for — so **no marker bait can force a fallthrough on
   a streamed request**; the shim will accept the first 200 it sees and relay
   it. Only one forcing survives the flag: the leg-1 content-inspection bait.
   The `400` + `data_inspection_failed` fallthrough (`shim.py:254-268`) is
   evaluated **before** the `if stream:` split (`:270`), so a streamed request
   whose leg-1 body trips alibaba's filter still cascades — the r22
   force-hyper mechanism works on both paths, the r22 force-opencode-go
   mechanism works on neither path reliably (it already starved on
   `stream:false`, `plans/attrib-r22-frozen.md:285-295`) and structurally
   cannot work on `stream:true`. The lesson the round must carry: **a stream
   forcing for opencode-go cannot be the marker bait ported over; it must be a
   header-stage or upstream-status mechanism** (a leg that 429s/5xxs on its
   own, or an upstream that returns a failing status before headers). If no
   such mechanism is available from the operator side, the honest outcome on
   that target is NOT-RUN-with-reason, not a redefinition of "forced
   coverage" — the r20 P9 precedent (an absence re-confirmed is a real scored
   outcome), restated by the r22 lesson's third named leftover.

3. **The feature vector flips with the flag, so a stream trial population
   silently re-weights the additive rule.** The r22 extensions `body_schema`
   and `id_in_body` are computed **only when `stream is False`** — the
   instrument guards them (`plans/attrib_probe.py:355-369`: `if obs.get("stream")
   is False and obs["status"] == 200 and not obs.get("error")`), and its own
   comment says they "fire only on stream:false responses (the forcing
   variants); on stream:true trials they are None and contribute 0 to every
   leg." The v1 stream-shape feature is the mirror image: `stream_span_class`
   is computed only when stream data events were seen (`:310-317`,
   `if obs.get("first_data_s") is not None`), i.e. only on `stream:true` — it
   cannot fire on a `stream:false` trial. So the two modes partition the
   feature set: **`body_schema`/`id_in_body` abstain on every stream trial,
   and `stream_span_class` abstains on every non-stream trial.** Under the
   frozen additive rule a feature that cannot fire contributes 0 to every leg,
   which shifts relative weight toward the features that do fire (the r22
   lesson's §3 made this point for empty table fields; the request flag is the
   same lever from the code side). The design consequence: a v3 table that
   simply **adds** stream trials to the v2 population changes which features
   carry the decision without changing a single weight — and it must say so,
   because a reader comparing the two modes' accuracies would otherwise be
   comparing two different instruments. The right shape is either (a) two
   declared feature subsets keyed by request mode, frozen in the block, or (b)
   an explicit in-block statement of which features abstain per mode, so the
   abstention is a designed fact and not a silent re-weighting.

4. **The ground truth changes surface too: on the stream path the shim's
   served-leg verdict is header-evidenced, while its sibling's is
   body-evidenced.** The instrument's GT join reads the journal's `leg=N/NAME
   OK|FAIL` lines (`plans/attrib_probe.py:713-717`, `:762-770`) and takes the
   first `OK` leg as the served leg (`:763-766`). But those `OK` lines are
   produced by `run_cascade` from `attempt_leg`'s `ok` verdict
   (`shim.py:305-307`) — and `ok` means different things per flag: header-200
   on `stream:true` (`:277-278`), header-200-AND-no-body-marker on
   `stream:false` (`:291-296`). So a stream trial's ground truth is decided by
   a code path that never read the body, while its non-stream sibling's ground
   truth is decided by a path that did. This is not a defect in the
   instrument — it faithfully records what the shim did — but it is a
   **provenance asymmetry the receipt must state**: "served leg" is not the
   same predicate on the two modes, so a stream GT and a non-stream GT are not
   interchangeable evidence about the legs. It also sharpens r22's honest
   limit: even the *GT* for stream trials is header-determined, so a stream
   trial cannot detect a leg whose headers say 200 but whose body is a quota
   refusal — on the stream path the shim would not detect it either, so the
   trial measures the shim's own (header-only) notion of serving, which is the
   thing the caller actually experiences, but is not the same claim as "the
   leg produced a real completion."

5. **Freezing a feature table without pinning the request mode freezes an
   under-specified instrument — and the v2 block already shows the gap in
   miniature.** The v2 table pinned the forcing bodies' mode explicitly
   (`trial_protocol.forcing_bodies[*].stream: false`) and even wrote the
   stream-path note into the block (`plans/attrib-r22-frozen.md:76`), but the
   feature rows' firing conditions were left implicit in the instrument's
   code. The r21 lesson 1 demanded the instrument bytes be pinned beside the
   table; the r22 table did that (`instrument_sha256_at_freeze` +
   `instrument_sha256_at_scoring`). The r23 refinement: pinning the code is
   necessary but not sufficient when the code **branches on an input the table
   does not name** — the mode→feature mapping must be in the frozen block, or
   a reader cannot tell which features were live for a given trial set without
   reading the code at the trial's sha. Concretely, a v3 stream instantiation
   must: (a) re-derive from the shim code which features can fire on
   `stream:true` (`stream_span_class` yes; `body_schema`/`id_in_body` no) and
   put that mapping in the block; (b) RE-FREEZE as v3 before the first stream
   request, with the r19 double-read guard and the FROZEN line appended after
   hashing; (c) expect the forcing mechanism itself to change (lesson 2) and
   freeze the new mechanism with the same disclosure the v2 block used
   (`shim_code_sha256` — which reproduces to `42d86d99…` and still matches);
   and (d) record the mode in the GT join (the v2 stream-flag hardening,
   `plans/attrib_probe.py:734-740`, already does this for `stream:false`
   forcing — the stream mode needs its mirror).

Named leftovers for the scorer/parent (recorded, not patched from this
seat):

- **The r23 premise is unconfirmed at this note's write time.** No
  stream-trial mode, no v3 table, and no round-23 receipt exist in the lane as
  of 13:33Z (greps above). This note is a **design-time prediction grounded in
  the landed shim code-read and the landed r22 record**, exactly as the r22
  lesson was written before its trials existed; the round's landed receipts
  supersede it. If stream features turn out to be materially different from
  the non-stream features (as lessons 2-4 predict), the table must be extended
  and **re-frozen as v3 BEFORE any stream trial** — a post-trial re-freeze is
  not a freeze (the r19 BR-1 / r21 TOCTOU family).
- **opencode-go on the stream path needs a header-stage forcing.** The r22
  marker bait cannot be ported (lesson 2). If no header-stage mechanism is
  disclosed and frozen, the honest clause outcome is NOT-RUN-with-reason on
  the opencode-go target, carrying the r22 gap forward rather than papering it
  over. Owner: stream-impl (mechanism + v3 table) then stream-trial-runner
  (trials/receipt), per the round's write ownership.
- **Twin-traffic join hazard, third recurrence (r21 defect-7).** The v2
  stream-flag GT-join hardening separates `stream:false` forcing rids from
  `stream:true` std traffic, but it relies on the byte-length + stream-flag
  pair; if r23 runs **both** a stream forcing and a non-stream forcing
  concurrently with identical bodies, the join can again collide (the r22
  addendum's "Twin traffic" item shows the same-body collision survived the
  flag hardening). The structural fix the r21 lesson 4 named — a per-seat
  nonce or seat-tagged join marker frozen into the protocol — is still unpaid
  after three rounds; the stream mode is the natural place to land it, because
  a stream body is not scanned by the shim and can carry a caller-visible
  nonce in the prompt without changing leg selection.
- **Records-commit gap (parent landing step).** At this note's write time the
  r22 lesson file is untracked: `git status --porcelain` lists `??
  corpus/lessons/2026-10-16-round22-leg-coverage-forcing.md` (and `??
  plans/__pycache__/`). This is the r21-named "cited-but-uncommitted" family;
  the parent's landing sweep should track every cited path in the same commit.
  `plans/__pycache__/` should not land.

## Erratum (appended round 25, 2026-10-20; QUALITY R5)

The mid-flight premise above ("no round-23 artifact has landed", written 13:33Z) is superseded by the landed
receipt `corpus/evidence/attrib-r23-stream.log:233-239` (score block 13:49:42Z; authoritative block
`:258-320`): 30/30 attribution accuracy and STREAM TARGET opencode-go n=0. Round 25 re-verdicts that
STREAM TARGET line UNTESTED (`plans/attrib_calibration.py`).
