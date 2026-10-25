# scorecard-verdict-draft — kengaku round 23 (coverage: opencode-go via the stream path)

Scribe seat, round-23 goal wave. Written 2026-10-16; starting state captured
13:33–13:40Z at HEAD `407156f` (round-22 records; the r22 evidence commit is
`8a08483`). **This file writes nothing** — every block below is a paste-ready
delta for a PARENT-owned file (`SCORECARD.md`, `LOG.md`); the parent
integrates under the kengaku lane identity. `[PARENT]` markers flag cells the
parent must confirm or fill from landed artifacts at integration time;
`{{PLACEHOLDER}}` slots resolve from landed artifacts or become an absence
statement with polling evidence — placeholders must not ship. No scalar axis
verdicts: verdicts are recorded per gate, per the round-16 idiom
(`corpus/lessons/round-16-recensus.md`).

Round-23 scope (one axis-move, COVERAGE — the r22-carried opencode-go gap):
characterize the ds shim's STREAM-path leg-selection mechanism from source
(read-only), add a stream-trial mode to the attribution instrument, and land
≥10 on-target opencode-go GT trials (bar 0.80 accuracy) with per-chunk
features captured; IF stream features differ materially, extend the feature
table and RE-FREEZE as v3 BEFORE any trial; the r23 addendum updates the legs
table honestly — including the critic's self-selection-vs-attribution wording
if client influence is the mechanism. Hard rules: freeze before trials;
journal GT read ONLY post-trials (structurally enforced — `journalctl` occurs
only inside `cmd_score`); small stream requests, ≥2.5 s spacing, localhost
shims only; credentials never read (shim source read-only, never executed).

Write ownership this round (per dispatch): stream-impl → `plans/attrib_probe.py`
(+ its v3 table if needed) only; stream-trial-runner → its receipt sections
only; scorer-r23 → the attrib note's r23 addendum only
(`corpus/knowledge/attrib-r21.md`); scribe → this directory only;
lessons-distiller → `corpus/lessons/` only. SCORECARD.md/LOG.md are
parent-owned. Everyone else: NO lane files.

## 0. Measured state at draft time (13:33–13:51Z)

| Quantity | Value | Command |
|---|---|---|
| HEAD | `407156f58013dd39e6ed0701cf55f14a1387d2fe` (`407156f`) | `git rev-parse HEAD` (13:35Z) |
| Working tree (lane) | `?? .ufo/interactive-sessions/`, `?? corpus/lessons/2026-10-16-round22-leg-coverage-forcing.md`, `?? plans/__pycache__/` — see D23-s7 | `git status --porcelain` |
| r22 live pin | `77b8d4a0be3dc3257a9179c00716c15afd51414fbb93dc1ca0718d5ce3590238` | `python3 plans/attrib_probe.py block-sha --frozen plans/attrib-r22-frozen.md` → exit 0 |
| r21 pin (v1 basis) | `9f0244bb0aa4463c66981e5758a9a368ea0f0ea61b26882925f3ce7bbe6ba33c` | `block-sha --frozen plans/attrib-r21-frozen.md` → exit 0 |
| Attribution instrument | `bb6bd9191677d72ac04b506b1ba01038369b2aaf5d72c79bb59fbd5c1ddf712c` (`plans/attrib_probe.py`) | `sha256sum plans/attrib_probe.py` |
| ds shim source | `42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386` — **byte-matches** the r22 table's `leg_forcing.shim_code_sha256` (`plans/attrib-r22-frozen.md:56`) | `sha256sum ~/.local/share/ds-flash-shim/shim.py` |
| opencode-go coverage (before) | **0 on-target GT trials** in both r22 runs: `TARGET opencode-go: on-target GT n=0 … -> FAIL` | `corpus/evidence/attrib-r22-legs.log:345` (run-2), `:310` `target_stats.opencode-go.gt_on_target = 0` |
| Stream-trial mode (before) | **absent** — the instrument's CLI had only `block-sha / freeze-check / trials / force-trials / score`; `cmd_force_trials` hardcodes `stream=False` | `grep -n add_parser plans/attrib_probe.py`; `plans/attrib_probe.py:620` |
| Stream-trial mode (landed mid-draft) | **landed 13:42Z**: CLI now has `stream-trials`; requires `attrib-feature-table-v3` with a `stream_forcing` section; captures per-chunk SSE frame shapes; instrument sha `cce53a1637…` at 13:42:01Z | `python3 plans/attrib_probe.py --help` → exit 0; `plans/attrib_probe.py:723-746` |
| v3 table | **landed 13:45:47Z**: `plans/attrib-r23-frozen.md`, `version: attrib-feature-table-v3`, `extends` v2 `77b8d4a0…`, `stream_forcing.target: opencode-go`, budgets `{stream-inspection: 24, stream-marker: 3, stream-hint: 3}`, `shim_code_sha256` `42d86d99…` (matches); block-sha `1b2d6a01bfa431ec4e78bf89fd989f9ad500d10bb78634362a3c0e3bce794f87`, exit 0. **Postdates the runner's scratch trials** (D23-s10) | `python3 plans/attrib_probe.py block-sha --frozen plans/attrib-r23-frozen.md` → exit 0; `plans/attrib-r23-frozen.md:34,40-50,214` |
| r23 stream-trials receipt | **landed 13:39:45Z**: `corpus/evidence/attrib-r23-stream-trials.log` — 14 blind `stream:true` trials (four body families: insp/insplong/std/marker) run by a **scratch driver** under the **v2 pin** `77b8d4a0…` + instrument `bb6bd919…`; **unscored, no GT**; discloses the deviation "stream-impl seat's stream-trial mode NOT present at run time" | receipt header `:1-10`; `:109` "n=14 … NO journal read by this seat" |
| r23 SCORED stream run | **landed + scored 13:49Z**: `corpus/evidence/attrib-r23-stream.log` — 30 stream trials 13:46:41–13:49:28Z under the v3 pin `1b2d6a01…`; `ACCURACY: 30/30 = 1.000 -> PASS`; `GT counts {alibaba 6, hyper 24}`; **`STREAM TARGET opencode-go: on-target GT n=0 … -> FAIL`** | `corpus/evidence/attrib-r23-stream.log:233-240,256`; §1.4 |
| Runnable files (operability baseline) | **38** committed `.py`/`.sh` at HEAD | `git ls-tree -r HEAD --name-only \| grep -cE '\.(py\|sh)$'` |
| Round-23 dir | **ABSENT** at 13:35Z (this draft creates it) | `ls .ufo/rounds/ \| grep round-23` → none |
| r23 lesson (sibling) | **landed 13:37Z**: `corpus/lessons/2026-10-16-round23-stream-surface.md` (untracked; independently reproduces the §1.1 mechanism from the same bytes) | `stat -c '%y %n'`; read in full (D23-s8) |
| Grader | [PARENT: re-run at close — no gate change registered this round; the r22 verdict is expected to stand unless new receipts change the replay set] | `python3 grader.py` |

## 1. The round's falsifiable claim, with receipts

**Before-claim (from the r22 close, the in-repo record):**

> "opencode-go: NOT COVERED — named gap. 0 on-target trials in both runs: …
> the next forcing mechanism is r23's registered claim."
> — `corpus/knowledge/attrib-r21.md:466-471` (Round-22 addendum)

> "r23 registered: opencode-go forcing via the stream-path header
> leg-selection (the v2 note documents why stream:false was chosen and what
> stream:true changes)."
> — `SCORECARD.md:543-545`

Scribe re-verification of the before-state (independent, 13:33–13:40Z):

- **The gap is real and numeric** — the r22 receipt's own `target_stats` prints
  `opencode-go: {"gt_on_target": 0, …}` in both runs (§0 row), and the shim
  landed every force-opencode-go trial on `alibaba-token-plan` (§1.2 below).
- **No stream-trial mode exists** — the instrument cannot currently send a
  `stream:true` forced trial: `cmd_force_trials` calls
  `capture(args.shim, body, timeout, stream=False)` (`plans/attrib_probe.py:620`)
  and `force_body` pins `"stream": False` (`:114`). So the round's second
  clause ("a stream-trial mode lands ≥10 on-target opencode-go GT trials")
  requires NEW instrument code — stream-impl's sole write this round.
- **The mechanism surface the r22 note named is the shim's own docstring, not
  a header parser** — see §1.1, which is the load-bearing finding of this
  draft.

**After-claim (this round's deliverable, dispatch wording):** (a) the
stream-path leg-selection mechanism is pinned from shim source, quoted; (b) a
stream-trial mode lands ≥10 on-target opencode-go GT trials at accuracy ≥ the
0.80 bar with per-chunk features captured; (c) if stream features differ
materially the table is extended and RE-FROZEN as v3 BEFORE trials; (d) the
r23 addendum updates the legs table honestly (including the critic's
self-selection-vs-attribution wording if client influence is the mechanism).

**Falsifiability shape (all legs can fail honestly):** the claim has a
*characterization* leg (the mechanism pinned from source), an *instrument*
leg (a stream-trial mode exists and runs), and a *coverage* leg (≥10 on-target
opencode-go GT trials at ≥0.80). §1.1 below finds that the stream path's
selector is the HTTP STATUS, and that the r22 echo-marker bait is structurally
inert on stream (`shim.py:270-294`) — so the coverage leg may be
**NOT-RUN-with-reason** if no disclosed mechanism forces leg-2 (hyper) to fail
by status. Per the r20 P9 / r22-lesson precedent, an absence scored honestly
is a landed result, not a failed round; the drafts must not launder a
NOT-RUN into a pass.

## 1.1 The stream-path leg-selection mechanism, pinned from shim source (read-only; quotes verbatim)

Read-only code-read of the operator's shim
(`~/.local/share/ds-flash-shim/shim.py`, sha `42d86d99…` — the same bytes the
r22 table pins). No shim state was changed; the file was never executed by
this seat.

- **The docstring (the sentence the r22 note cites):**
  `shim.py:25-27` — "Streaming: for `stream: true` the leg is chosen from the
  response HEADERS before any body byte is streamed; the successful leg's
  bytes are then relayed to the caller as-is."
- **What "chosen from the response HEADERS" actually is in code — the HTTP
  status, not header content.** `attempt_leg` (`shim.py:200-296`) advances the
  cascade on `FAIL_STATUSES = frozenset((402, 403, 429))` (`:61`, `:249`),
  on any 5xx (`:251`), and on a 400 whose body carries `data_inspection_failed`
  (`:254-265`). Everything else that is a 200 is a SUCCESS. The stream branch
  is `shim.py:270-278`:
  ```
  if stream:
      # Decide the leg from the headers, before streaming the body.
      …
      return {"ok": True, "status": status, "headers": resp_headers,
              "body": None, "resp": resp, "conn": conn}
  ```
  i.e. for a stream request, a 200 returns immediately with the body
  unread — the leg is fixed by the status line. `run_cascade`
  (`shim.py:299-315`) returns on the first leg whose `attempt_leg` returned
  `ok`; headers are relayed to the caller (`_relay_headers`,
  `shim.py:336-344`) but are **never parsed for the leg choice**. There is no
  header-content selector anywhere in the shim.
- **The FAIL_MARKER body scan is NON-STREAM ONLY.** The marker scan
  `marker = _marker_in(data)` (`shim.py:291-294`) sits AFTER the stream branch
  returns, on the non-stream path only (`_marker_in`, `shim.py:184-189`,
  `FAIL_MARKERS` at `:65-93`, incl. `"usage limit"` at `:77`). On a stream
  request that scan is unreachable — the shim cannot inspect a body it is
  streaming through.
- **Consequence (the mechanism, stated plainly):** the stream path's leg
  selector is the per-leg HTTP **status** (402/403/429/5xx/400-inspection →
  next leg; 200 → serve and stream). The r22 `stream_false_note`
  (`plans/attrib-r22-frozen.md:76`) is correct that stream differs from
  non-stream — but the difference is that the **marker lever is REMOVED on
  stream**, not that a new header lever is added. This is the mechanism the
  round asked to pin; stream-impl owns the authoritative pin and the r23
  addendum's legs-table wording.
- **The v3 freeze's own `mechanism` field confirms this and closes the
  client-influence question (landed 13:45:47Z,
  `plans/attrib-r23-frozen.md:44-50`).** Quoting the frozen text: "on
  stream:true the shim picks the leg from the response HEADERS before any body
  byte (shim.py:270-278 …) and RETURNS BEFORE the FAIL-marker scan at
  shim.py:291-294, so a 200 marker bait CANNOT force a fallthrough on the
  stream path (candidate 1 FALSIFIED by code). The shim builds its own upstream
  headers and never reads the caller's (shim.py:210-217), and run_cascade
  iterates the fixed LEGS list (shim.py:299-315), so NO client hint selects a
  leg (candidate 2 FALSIFIED by code). The only client-controllable stream
  advance is a leg-local non-200 that is not terminal (shim.py:249-268): …
  The one such failure a body can force is leg-1 alibaba's content-inspection
  400 … -> leg-2 hyper; leg-2->leg-3 needs leg-2 to fail, which no body forces
  (candidate 3: reachable only probabilistically …)". This is the
  self-selection-vs-attribution answer the round's clause (d) asked for: **no
  client influence selects the leg** (candidate 2 falsified by source), so the
  round's stream trials measure the SHIM's leg selection, not a client-side
  self-selection — and candidate 1's control body (`stream-marker`) plus
  candidate 2's control body (`stream-hint`, headers `X-Shim-Leg` /
  `X-Cascade-Leg`) are frozen into the v3 table to demonstrate both
  falsifications empirically.

**Forcing-lever consequence (design input, filed not decided):** to land a
stream trial on leg-3 opencode-go, BOTH leg-1 and leg-2 must fail by status
(or connection error / timeout — `shim.py:228-235`). The disclosed r22
levers reach only leg-1: the content-inspection bait kills alibaba on BOTH
paths (`shim.py:261`, ahead of the stream branch), and the echo-marker bait
is inert on stream (§1.1). No disclosed client-side mechanism yet forces
hyper (leg-2) to fail by status; a hyper 429/5xx is route weather, not a
forced condition. The v3 freeze states the same: the stream-inspection bait's
"Expected landing: leg-2 hyper on a normal response; leg-3 opencode-go only if
leg-2 also fails". So the coverage clause may honestly resolve to
NOT-RUN-with-reason (or a FAIL on the ≥10 bar with leg-3 reached only
probabilistically) — see D23-s3.

## 1.2 The r22 result this round inherits (receipt-verbatim)

| receipt | run | authoritative block | result |
|---|---|---|---|
| `corpus/evidence/attrib-r22-legs.log` | run-1 (T01-T20) | score block ~:294-345 | `ACCURACY: 20/20 = 1.000 … -> PASS`; GT counts `{hyper: 9, alibaba-token-plan: 10, opencode-go: 1}`; `TARGET hyper: 9/9 … (n<10) -> FAIL`; `TARGET opencode-go: on-target GT n=0 … -> FAIL` |
| `corpus/evidence/attrib-r22-legs.log` | run-2 (T01-T20) | score block ~:341-362 | `ACCURACY: 20/20 = 1.000 … -> PASS`; GT counts `{hyper: 10, alibaba-token-plan: 10}`; `TARGET hyper: 10/10 = 1.000 -> PASS`; `TARGET opencode-go: on-target GT n=0 … -> FAIL` |

The run-2 `score_summary` JSON (`:362`) carries
`"target_stats": {"opencode-go": {"gt_on_target": 0, "class_scored": 10,
"gt_distribution": {"alibaba-token-plan": 10}}}` — every force-opencode-go
trial served from leg-1. The one live opencode-go serve on record is run-1
T03 (chain `1/alibaba FAIL 400` → `2/hyper FAIL None` → `3/opencode-go OK
200`, blind-predicted correctly — `attrib-r22-legs.log:382-385`); it is
n=1, far below the ≥10 bar. **This is the before-state the round's coverage
clause must move.**

## 1.3 The r23 lesson landed mid-draft and independently confirms §1.1 (cross-ref)

At 13:37Z the lessons-distiller landed
`corpus/lessons/2026-10-16-round23-stream-surface.md` (untracked at draft time,
D23-s7). It was written from the SAME landed bytes (shim sha `42d86d99…`, the
instrument `bb6bd919…`, both frozen tables — all reproduced by that seat) and
reaches the same mechanism conclusion by an independent read. Two of its
findings are load-bearing for the drafts and are folded here:

- **Mode→feature partition (lesson 3):** `body_schema` / `id_in_body` are
  computed only when `stream is False` (`plans/attrib_probe.py:355-369`) and
  `stream_span_class` only when stream data events were seen (`:310-317`). So
  the two modes partition the feature set; under the additive rule a feature
  that cannot fire contributes 0 to every leg, which **shifts relative weight
  without changing any weight**. A v3 that simply adds stream trials to the v2
  population therefore compares two different instruments; the block must
  declare the mode→feature mapping (lesson 5) so the abstention is designed,
  not silent.
- **GT provenance asymmetry (lesson 4):** the journal's `OK` line is produced
  from `attempt_leg`'s `ok` verdict (`shim.py:305-307`), which means
  header-200 on `stream:true` but header-200-AND-no-body-marker on
  `stream:false`. A stream GT and a non-stream GT are therefore **not
  interchangeable evidence about the legs** — the receipt must state the
  asymmetry, and it sharpens the honest limit: a stream trial measures the
  shim's own header-only notion of serving, not "the leg produced a real
  completion."

Lesson 2 restates §1.1's forcing consequence (the marker bait cannot port to
stream; only the leg-1 content-inspection bait survives the flag; if no
header-stage forcing is available, the opencode-go clause is
NOT-RUN-with-reason) — the drafts and the lesson agree, and the lesson's
"Named leftovers" add the twin-traffic join hazard (D23-s8) and the
records-commit gap.

## 1.4 The r23 result as landed (receipt-verbatim; read 13:50Z)

The instrument-mode stream run under the v3 pin landed and scored:
`corpus/evidence/attrib-r23-stream.log`, 30 trials 13:46:41–13:49:28Z
(bodies `{stream-hint: 3, stream-inspection: 24, stream-marker: 3}`),
`frozen_sha256 1b2d6a01…`, instrument `cce53a1637…`. Authoritative block
verbatim:

```
GT counts: {"alibaba-token-plan": 6, "hyper": 24}
ACCURACY: 30/30 = 1.000 (bar 0.80, min scored n 20) -> PASS
per-leg GT counts mean honesty note: legs with 0 GT trials are UNTESTED by this run
BODY stream-hint: scored n=3, on-target(opencode-go) n=0, correct 0/0 = 0.000 | GT dist {'alibaba-token-plan': 3}
BODY stream-inspection: scored n=24, on-target(opencode-go) n=0, correct 0/0 = 0.000 | GT dist {'hyper': 24}
BODY stream-marker: scored n=3, on-target(opencode-go) n=0, correct 0/0 = 0.000 | GT dist {'alibaba-token-plan': 3}
STREAM TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL
HONEST LIMIT (r23): on the STREAM path the shim picks the leg from response HEADERS and never scans a 200 body for FAIL markers (shim.py:270-278 vs :291-294), so the only client-controllable advance is a leg-local non-200 (shim.py:249-268); the client's chosen body therefore SELF-SELECTS the serving leg — this is coverage of a client-influenced route, not of natural route weather.
```

**Reading (recorded, not patched):** the coverage clause is **NOT MET** —
opencode-go took **0 on-target GT trials** (n=0 < 10, FAIL). The round's
characterization clause is MET and empirically confirmed: the two controls
falsified exactly as §1.1/the v3 freeze predicted — `stream-marker` (candidate
1) landed leg-1 alibaba 3/3 (the marker bait is inert on stream), and
`stream-hint` (candidate 2) landed leg-1 alibaba 3/3 (no client header selects
a leg). `stream-inspection` (the only client-controllable advance) landed
leg-2 hyper 24/24: the leg-1 inspection bait cascades, but no body forces
leg-2 to fail, so leg-3 was never reached. The instrument itself scored
**30/30 = 1.000 PASS** on what served. Ablations: `hdr_tells` LOO 14/30
(load-bearing on this GT); all other 12 ablations 30/30. Ordering clean:
v3 freeze 13:45:47Z < first stream trial 13:46:41Z < score block (after
13:49:28Z); `journalctl` only in `cmd_score`.

**The self-selection wording (the round's clause (d), receipt-verbatim):** the
`HONEST LIMIT (r23)` line above is the critic's self-selection-vs-attribution
statement — on the stream path the client's chosen body self-selects the
serving leg, so this is coverage of a client-influenced route, not of natural
route weather. It is stricter than r22's forced-vs-natural limit and must ride
with every quoting surface.

**Scorer-r23's addendum (landed 13:52Z, `corpus/knowledge/attrib-r21.md:484+`)
— the round's final adjudication, quoted:** the target clause is **NOT MET —
0 opencode-go on-target across ALL 104 r23 stream trials** (batch 1 runner 14,
batch 2 impl 30, batch 2 twin 30, verifier 30 unscored). Scored accuracy
1.000 everywhere: batch 1 `14/14`, batch 2 impl `30/30`, batch 2 twin `30/30`;
combined main receipt `44/44 = 1.000`, Wilson `[0.920, 1.000]`. The
`stream-inspection` arm landed **hyper 24/24** — the probabilistic leg-2
failure that gave r22's single opencode-go serve (run-1 T03, 1/20) did **not**
reproduce (0/24). The addendum also records the falsifier seat's direct proof
that the marker bait is inert on stream: alibaba served a streamed body that
literally contained `usage limit` (raw-SSE offset 1889 of 7336 bytes) with
**no** fallthrough. The v3 `feature_extension_ruling` freezes the per-chunk
features as **captured-but-weightless** (no pre-trial per-leg cadence evidence
exists to freeze a discriminating profile, so adding one would be a guess); no
feature or weight changed from v2. The addendum's clause check marks the
mechanism pin **YES**, per-chunk capture **YES**, v3 re-freeze **YES for the
instrument-native run** (with the pre-v3 batch 1 deviation disclosed), and the
≥10-on-target clause **NOT MET**.

## 2. Verdict draft — coverage axis-move (paste-ready section)

```markdown
## Round 23 — opencode-go stream-path coverage (coverage axis-move, 2026-10-16)

One 32-seat flash wave (operator routing: deepseek bucket,
`cascade/deepseek-v4.1-flash` — switched back from zai). The r22 close named
one gap: opencode-go took 0 on-target GT trials (the echo-marker bait starves
against reasoning models), and registered r23 as forcing opencode-go via the
ds shim's STREAM path (`SCORECARD.md:543-545`). This round characterizes that
path from shim source, adds a stream-trial mode to the instrument, and runs
the stream trials against the frozen feature table — extending and
RE-FREEZING as v3 BEFORE any trial if stream features differ materially —
scored against post-trials journal GT.

| Axis | Verdict | Evidence / limit |
|---|---|---|
| **coverage** *(owned)* | **FAIL on the target clause, landed honestly (the r20 P9 shape)** — opencode-go NOT covered (0 on-target), but the mechanism is pinned and both forcing candidates are empirically falsified | Mechanism pinned from source: stream leg selection is STATUS-based; the marker lever is structurally absent on stream (`shim.py:25-27, 249-294, 336-344`) — quoted in §1.1, confirmed by the v3 freeze's `mechanism` field. Instrument: `stream-trials` mode, sha `cce53a1637…`. Trials (receipt `corpus/evidence/attrib-r23-stream.log`, 30 stream trials under v3): `ACCURACY: 30/30 = 1.000 (bar 0.80, min scored n 20) -> PASS`; `GT counts: {"alibaba-token-plan": 6, "hyper": 24}`; `STREAM TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL`. Controls: `stream-marker` 3/3 → alibaba (marker bait inert on stream), `stream-hint` 3/3 → alibaba (no client hint selects a leg), `stream-inspection` 24/24 → hyper (leg-1 bait cascades, leg-2 never fails → leg-3 unreached). Ablations: `hdr_tells` LOO 14/30; all other 12 at 30/30. Honest limit carried verbatim (stricter than r22's): the client's chosen body SELF-SELECTS the serving leg — coverage of a client-influenced route, not natural route weather. |
| calibration | [PARENT: verdict] | Freeze discipline: **v3 landed** — `FROZEN: 2026-10-16T13:45:47Z sha256:1b2d6a01bfa431ec4e78bf89fd989f9ad500d10bb78634362a3c0e3bce794f87` (`plans/attrib-r23-frozen.md`; `version: attrib-feature-table-v3`, extends v2 `77b8d4a0…`; block-sha exit 0). **Ordering clean for the scored run:** v3 freeze 13:45:47Z < first instrument-mode stream trial 13:46:41Z < last 13:49:28Z < score block; `journalctl` occurs only inside `cmd_score` (structural blind rule). **Caveat (D23-s10):** the runner's earlier scratch-driver trials (13:38–13:39Z) PREDATE the v3 freeze and ran under the v2 pin — they are characterization only, not the round's scored trials. |
| operability | [PARENT: verdict — a stream-trial mode lands in the standing P10 instrument] | `plans/attrib_probe.py` gained `stream-trials` (sha `cce53a1637…`); runnable baseline was 38 committed `.py`/`.sh` at `407156f`. |
| novelty | unchanged | Same instrument + GT protocol; the stream path is a new mechanism surface, not a new phenomenon (r21 prior-art scoping stands, `corpus/knowledge/attrib-prior-art-r21.md`). |
| depth | [PARENT: verdict] | The mechanism pin (§1.1) + the stream-feature comparison + the r23 addendum's honest legs-table update. |
| freshness | [PARENT: verdict] | Stream trials re-verify the live cascade this day; receipts carry UTC-stamped trial windows + per-chunk feature captures. |
| adjacency | unchanged | All requests localhost shims; credentials never read; shim source read-only (never executed); journal reads are the lane's own-probe GT post-trials; any serving-plane finding routed to the integrator. |

Honest ceiling: the round is host- and day-specific (the r19 note's §8 limit-2
idiom applies). The stream-path finding is a MECHANISM characterization, not a
serving claim: it says how the shim chooses a leg on `stream:true`, not that
any leg serves at a natural rate. The target clause **FAILED as landed**
(opencode-go 0 on-target, n=0 < 10): the mechanism is pinned, both forcing
candidates are empirically falsified, and the reason no forced stream trial
reaches leg-3 is named with its source lines — the r20 P9 precedent prices an
absence scored honestly, and this is that shape. The r22 opencode-go gap is
therefore **carried forward, not closed**: the stream path cannot force leg-3
with any disclosed client-side mechanism, so the honest next lever is a
header-stage / upstream-status mechanism (or acceptance that opencode-go is
reachable only by route weather). The instrument's own 30/30 = 1.000 says it
attributes correctly what served — it does not create coverage.
```

**[PARENT] Fill rules for the section above:**

1. The coverage cell above is resolved from the landed receipt
   (`corpus/evidence/attrib-r23-stream.log`, score block read 13:50Z) —
   quote it verbatim; do not recompute. The scorer-r23 addendum
   (`corpus/knowledge/attrib-r21.md`) supersedes where it disagrees.
2. The coverage cell must NOT be laundered: opencode-go is 0 on-target (FAIL);
   the round's win is the mechanism pin + the two falsified controls + the
   30/30 instrument result on what served — not coverage of opencode-go.
3. The self-selection `HONEST LIMIT (r23)` line (§1.4) must ride with every
   quoting surface.

## 3. Scribe findings (filed, not patched; each with its receipt)

- **D23-s1 (before-state re-verification — the round's premise holds at draft
  time):** opencode-go is 0 on-target in both r22 runs (§0 row,
  `attrib-r22-legs.log:310,345`); the stream path is uncharacterized in-repo
  and no stream-trial mode exists (`plans/attrib_probe.py:114,620`; CLI has no
  `stream-*` subcommand). The premise "opencode-go attribution has 0 on-target
  trials; the stream path is uncharacterized" is true at round start.
- **D23-s2 (the stream-path mechanism, pinned — the round's first clause is
  satisfiable from source alone):** §1.1 quotes `shim.py:25-27, 61, 184-189,
  200-296, 299-315, 336-344`. The selector is the HTTP status; headers are
  relayed, never parsed; the `FAIL_MARKERS` scan is non-stream only. The r22
  note's "picks the serving leg from RESPONSE HEADERS" is the shim's own
  docstring wording — accurate as the shim describes itself, but the operative
  content is the status line, and no header-content selector exists. stream-impl
  owns the authoritative pin; this draft files the verbatim quotes so the
  paste-ready blocks cannot propagate a "header-content selector" reading.
- **D23-s3 (the forcing-lever consequence — the coverage leg may be
  NOT-RUN-with-reason; flagged BEFORE trials, not at integration):** on stream,
  the r22 echo-marker bait cannot fire (§1.1 — `_marker_in` is unreachable on
  stream). Reaching leg-3 needs BOTH leg-1 and leg-2 to fail by status. The
  content-inspection bait kills leg-1 on both paths (`shim.py:261`); no
  disclosed client-side mechanism forces hyper (leg-2) to fail by status, and a
  hyper 429/5xx is weather. Client-side stream levers that could fail a leg:
  connection error / timeout (`shim.py:228-235`, not controllable from the
  request body), 402/403/429 (provider-side), 400 inspection (leg-1 only).
  The honest outcome if none lands: NOT-RUN-with-reason on the coverage clause
  (r20 P9 / `corpus/lessons/2026-10-16-round22-leg-coverage-forcing.md`
  "Named leftovers" last bullet). The stream-impl seat must decide the stream
  forcing design; this draft files the constraint and forbids a launder.
  **CONFIRMED by the landed run (§1.4):** `stream-inspection` landed leg-2
  hyper 24/24 — leg-3 was never reached; opencode-go 0 on-target. The
  prediction held; the clause FAILED as predicted, recorded not patched.
- **D23-s4 (feature-table consequence — when a v3 re-freeze is owed):** on
  `stream:true` trials the v2 features `body_schema` / `id_in_body` contribute
  0 (they fire only `stream is False`; `plans/attrib_probe.py:356-359`), and
  v1's `stream_span_class` (burst vs incremental) is the stream-shape feature
  (`:310-317`). So a stream trial uses v1's frozen stream profile unless the
  observed stream features differ materially from the frozen bands/tells — in
  which case the table extends and RE-FREEZES as v3 BEFORE the first stream
  trial (v2 `decision_rule` + `plans/probe-battery-TEMPLATE.md` §11 re-freeze
  policy: any table change = new freeze naming the superseded hash). The
  parent must not let a v3 freeze land after traffic starts (r19 BR-1 TOCTOU).
  **Mode partition + GT asymmetry (folded from the landed r23 lesson §3-4,
  §1.3):** the two modes partition the feature set (`body_schema`/`id_in_body`
  abstain on every stream trial; `stream_span_class` abstains on every
  non-stream trial), so adding stream trials to the v2 population silently
  re-weights the additive rule unless the block declares the mode→feature
  mapping (lesson 5); and a stream GT is header-evidenced while a non-stream
  GT is body-evidenced (`shim.py:305-307`), so the receipt must state the
  provenance asymmetry.
- **D23-s5 (index parity gap — inherited, parent-owned):** `corpus/README.md`'s
  `evidence/` index ends at `round18-kimi-routing` (`corpus/README.md:91`); the
  r19/r21/r22 attribution receipts
  (`corpus/evidence/attrib-r21-*.log`, `attrib-r22-*.log`) have no index rows
  (`grep -in attrib corpus/README.md` → no receipt-index hits). The r21 and r22
  report drafts both flagged "index rows" as owed; the gap persists at HEAD
  `407156f`. [PARENT: add rows or record the carry.]
- **D23-s6 (fleet-level report copy — confirm routing):** the round contract
  (`templates/round-prompt.md` §4) puts the fleet report at
  `.ufo/reports/round-<N>/<lane>.md` on the fleet repo. At 13:38Z the fleet
  reports tree has `round-18/kengaku.md` and nothing for rounds 19–23
  (`ls .ufo/reports/` → no `round-19..23` kengaku dir); the lane-local copies
  are `.ufo/rounds/round-2N/kengaku.md`. [PARENT: confirm whether the r21/r22
  fleet copies are owed and route the r23 report per the contract.]
- **D23-s7 (scribe self-disclosure, ordering-safe):** this seat issued ZERO
  HTTP requests to any probe target and read NO journal GT. Reads were lane
  files (`AGENTS.md`, `SCORECARD.md` r22 section, `LOG.md` tail,
  `plans/attrib_probe.py`, `plans/attrib-r22-frozen.md`,
  `corpus/knowledge/attrib-r21.md`, `corpus/evidence/attrib-r22-legs.log`,
  `corpus/lessons/2026-10-16-round22-leg-coverage-forcing.md`,
  `corpus/README.md`), the operator's shim source read-only
  (`~/.local/share/ds-flash-shim/shim.py` — never executed), the fleet
  template (`templates/round-prompt.md`), plus `date -u`. Nothing this seat did
  can enter an ordering audit. The working tree at draft time carries the r22
  lesson untracked and `plans/__pycache__/` (§0 row) — the r21 hygiene item
  (D21-s7 item 7) recurs.
- **D23-s8 (twin-traffic join hazard, third recurrence — folded from the landed
  r23 lesson):** the v2 stream-flag GT-join hardening
  (`plans/attrib_probe.py:734-740`) separates `stream:false` forcing rids from
  `stream:true` std traffic by the byte-length + stream-flag pair, but r23 may
  run BOTH a stream forcing and a non-stream forcing; identical bodies would
  again collide (the r22 addendum's "Twin traffic" item shows the same-body
  collision survived the flag hardening). The r21 lesson 4 structural fix (a
  per-seat nonce / seat-tagged join marker frozen into the protocol) is still
  unpaid after three rounds; the r23 lesson notes a stream body is not scanned
  by the shim, so it can carry a caller-visible nonce in the prompt without
  changing leg selection. [PARENT: decide whether the r23 trials freeze a join
  nonce; the r22 precedent resolved the collision by greedy in-order assignment
  and disclosed it in-receipt.]
- **D23-s9 (transient non-runnable instrument during the write window — the
  r21 D21-s12 class):** at 13:41:03Z `plans/attrib_probe.py` (sha `cb2388d0…`)
  crashed on every invocation: `NameError: name 'FROZEN_R23' is not defined`
  at `plans/attrib_probe.py:1128` (`--help` exit 1). It was runnable again by
  13:42:01Z (sha `cce53a1637…`, `--help` exit 0). No freeze pinned the broken
  bytes (the v3 table landed later, 13:45:47Z, under the fixed sha). Filed as
  the r19 DEFECT-3 / r21
  D21-s12 family: a freeze must not pin an instrument that cannot start —
  the pre-freeze mock-smoke discipline. The scribe's check was offline (no
  request, no shim execution).
- **D23-s10 (the landed stream-trials receipt is a scratch-driver,
  v2-pin, unscored run — NOT the round's instrument-mode coverage trials;
  flagged before integration):** `corpus/evidence/attrib-r23-stream-trials.log`
  (landed 13:39:45Z, 14 blind `stream:true` trials 13:38:14–13:39:45Z) ran
  under the **r22 v2 pin** `77b8d4a0…` and instrument `bb6bd919…` via a
  scratch driver (`/tmp/kengaku-tmp/r23-stream/driver.py`), because
  stream-impl's `stream-trials` mode and the v3 table did not exist at run
  time — the receipt discloses this as a DEVIATION (header `:7`). The receipt
  is **unscored** (no GT counts, no `ACCURACY` line; the runner read no journal
  by design, `:109`). So the round's coverage clause is NOT yet satisfied by
  landed bytes: it needs (a) the v3 table frozen BEFORE any instrument-mode
  stream trial, (b) the `stream-trials` run, (c) post-trial GT scoring. The
  scratch-driver trials are legitimate characterization evidence (four body
  families: insp/insplong/std/marker) but they predate the freeze the rule
  requires and carry no GT. [PARENT: do not cite the scratch receipt as the
  round's scored coverage result — the scored result is the v3 run
  (`corpus/evidence/attrib-r23-stream.log`), which landed and scored (FAIL,
  opencode-go 0 on-target; §1.4).]

## 4. Sources for every claim in this draft

- `SCORECARD.md:519-545` — the r22 section (hyper COVERED 10/10; opencode-go
  named gap; r23 registration).
- `corpus/knowledge/attrib-r21.md:454-483` — the Round-22 addendum (opencode-go
  NOT COVERED; the next forcing mechanism is r23's claim).
- `plans/attrib-r22-frozen.md` — the v2 table (`:56` shim sha; `:76` the
  stream_false_note; `:275-310` post-trials errata incl. the R22-1 instrument
  defect).
- `plans/attrib_probe.py` — the instrument (`:114` `stream: False` in
  `force_body`; `:310-317` stream-shape features; `:356-359` v2 features are
  non-stream-only; `:620` `capture(..., stream=False)`; `:734-740` the v2
  stream-flag GT join; CLI subcommands).
- `corpus/evidence/attrib-r22-legs.log` — the r22 runs' authoritative blocks
  (`:310`/`:345` target stats; `:362` score_summary JSON).
- `corpus/lessons/2026-10-16-round22-leg-coverage-forcing.md` — the r22 lesson
  (forced-vs-natural mechanism; "Named leftovers" incl. the NOT-RUN precedent).
- `corpus/lessons/2026-10-16-round23-stream-surface.md` — **landed 13:37Z**
  (lessons-distiller; untracked at draft time): §1-5 the stream-surface
  mechanism, the mode→feature partition, the GT provenance asymmetry, and the
  named leftovers (NOT-RUN; twin-traffic; records-commit gap).
- `~/.local/share/ds-flash-shim/shim.py` (read-only, sha `42d86d99…`) —
  `:25-27` stream docstring, `:61` FAIL_STATUSES, `:65-93` FAIL_MARKERS,
  `:184-189` `_marker_in`, `:200-296` `attempt_leg` (stream branch `:270-278`,
  marker scan `:291-294`), `:299-315` `run_cascade` (`:305-307` the `ok` line),
  `:336-344` `_relay_headers`.
- `corpus/README.md:73-91` — the evidence index (D23-s5 gap).
- `plans/attrib_probe.py` (r23 stream mode, sha `cce53a1637…` at 13:42:01Z) —
  `:1-35` module docstring (the r23 stream extension), `:49` `FROZEN_R23`,
  `:723-746` `cmd_stream_trials` (ds-only; requires v3 + `stream_forcing`),
  `:1128` the transient `FROZEN_R23` NameError (D23-s9).
- `corpus/evidence/attrib-r23-stream-trials.log` — **landed 13:39:45Z**
  (stream-trial-runner): header `:1-10` (v2 pin `77b8d4a0…`, instrument
  `bb6bd919…`, the DEVIATION line), `:109` "n=14 … NO journal read by this
  seat" (D23-s10).
- `templates/round-prompt.md` §4 — the fleet report contract (D23-s6).

## 5. Status at scribe handoff (updated on stat-verified mtimes only)

| seat-owned artifact | path | state at 13:51Z |
|---|---|---|
| stream-impl | `plans/attrib_probe.py` | **landed mid-draft**: `stream-trials` mode added (sha `cce53a1637…` at 13:42:01Z, `--help` exit 0); transiently non-runnable at 13:41:03Z (D23-s9) |
| stream-impl | `plans/attrib-r23-frozen.md` (v3 table) | **landed 13:45:47Z**: `FROZEN … sha256:1b2d6a01bfa431ec4e78bf89fd989f9ad500d10bb78634362a3c0e3bce794f87`, `attrib-feature-table-v3`, `stream_forcing.target: opencode-go`; block-sha exit 0. Postdates the runner's scratch trials (D23-s10) |
| stream-trial-runner | `corpus/evidence/attrib-r23-stream-trials.log` | **landed 13:39:45Z** — a scratch-driver, v2-pin, **unscored** characterization run (14 blind trials), NOT the instrument-mode coverage trials (D23-s10) |
| stream-trial-runner | `corpus/evidence/attrib-r23-stream.log` | **landed + SCORED** (30 stream trials 13:46:41–13:49:28Z under the v3 pin `1b2d6a01…` + instrument `cce53a1637…`): `ACCURACY: 30/30 = 1.000 -> PASS`; `GT counts {alibaba 6, hyper 24}`; **`STREAM TARGET opencode-go: on-target GT n=0 … -> FAIL`**; controls confirm candidates 1 and 2 falsified (§1.4) |
| scorer-r23 | the attrib note's r23 addendum (`corpus/knowledge/attrib-r21.md`) | **landed 13:52Z** (`:484+`): target clause **NOT MET — 0 opencode-go on-target across all 104 r23 stream trials**; scored 1.000 everywhere; combined 44/44 = 1.000 (Wilson [0.920, 1.000]) |
| scribe | this directory (three files) | **landed by this seat** |
| lessons-distiller | `corpus/lessons/2026-10-16-round23-stream-surface.md` | **landed 13:37Z** (untracked; folded into §1.3, D23-s4, D23-s8) |

All five seat artifacts have landed. Every paste-ready block above quotes only
landed artifacts; no `{{…}}` coverage slot remains. [PARENT: the integration
steps remain — LOG.md §23 entry,
SCORECARD.md round-23 section, the fleet report, index rows (D23-s5), grader
re-run, the axis verdict lines, the D23-s6 fleet-copy decision, and the D23-s10
ordering/scope adjudication (the scratch run is characterization only; the
v3 run is the scored one).]
