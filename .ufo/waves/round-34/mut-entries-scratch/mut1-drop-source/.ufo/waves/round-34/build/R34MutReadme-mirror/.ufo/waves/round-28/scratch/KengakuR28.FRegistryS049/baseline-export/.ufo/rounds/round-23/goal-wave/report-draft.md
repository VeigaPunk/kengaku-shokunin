# report-draft — kengaku round 23 (fleet report skeleton)

Scribe seat, round-23 goal wave. Written 2026-10-16; starting state captured
13:33–13:40Z at HEAD `407156f` (round-22 records; r22 evidence commit
`8a08483`). **This file writes nothing** — the round report is PARENT-owned and
lands at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-23/kengaku.md`
(round contract: `templates/round-prompt.md` §4). The skeleton carries the
contract's four required sections in order (work performed / landed changes /
before→after measurements / SHONEN). A contentless report counts the round as
failed, so every `[PARENT]` slot must resolve to a real receipt or the bullet
must state its absence with polling evidence — placeholders must not ship.

---

```markdown
# SHONEN — Round 23: opencode-go stream-path coverage
(coverage axis-move)

Starting commit `407156f`. Lane: kengaku-shokunin (LLM/model research &
evaluation). Wave: 32-seat flash (deepseek bucket, `cascade/deepseek-v4.1-flash`
— the operator switched back from zai after r22). One axis-move: coverage —
close the r22-carried opencode-go gap by characterizing the ds shim's stream
path, adding a stream-trial mode, and landing ≥10 on-target opencode-go GT
trials at the 0.80 bar. Falsifiable claim: **before** — opencode-go attribution
has 0 on-target trials (`corpus/evidence/attrib-r22-legs.log:310,345`) and the
stream path is uncharacterized (no `stream-*` subcommand in
`plans/attrib_probe.py`); **after** — the stream-path leg-selection mechanism
is pinned from shim source (quoted); a stream-trial mode lands ≥10 on-target
opencode-go GT trials (bar 0.80) with per-chunk features captured; IF stream
features differ materially the table is extended and RE-FROZEN as v3 BEFORE
trials; the r23 addendum updates the legs table honestly (including the
critic's self-selection-vs-attribution wording if client influence is the
mechanism).

## Work performed

- Stream-impl (mechanism pin + stream-trial mode): the stream-path
  leg-selection mechanism pinned from shim source, read-only, sha `42d86d99…`
  (byte-matches the r22 table's `shim_code_sha256`,
  `plans/attrib-r22-frozen.md:56`): the stream selector is the per-leg HTTP
  STATUS (`shim.py:249-278`); headers are relayed, never parsed
  (`shim.py:336-344`); the `FAIL_MARKERS` body scan is non-stream only
  (`shim.py:291-294`), so the r22 marker bait is structurally inert on stream
  — the stream path REMOVES a forcing lever. The instrument gains a
  `stream-trials` mode with per-chunk SSE frame capture — **landed mid-draft**
  (instrument sha `cce53a1637…` at 13:42:01Z, `--help` exit 0; requires
  `attrib-feature-table-v3` + a `stream_forcing` section,
  `plans/attrib_probe.py:723-746`); it was transiently non-runnable at
  13:41:03Z (sha `cb2388d0…`, `NameError: FROZEN_R23` at `:1128`, D23-s9).
  The v3 re-freeze decision: **v3 table LANDED 13:45:47Z**
  (`plans/attrib-r23-frozen.md`, `FROZEN … sha256:1b2d6a01…`,
  `attrib-feature-table-v3`, `stream_forcing.target: opencode-go`); the
  instrument-mode `stream-trials` run then executed and scored under it.
- Stream-trial-runner: (i) `corpus/evidence/attrib-r23-stream-trials.log`
  **landed 13:39:45Z** — a **scratch-driver, v2-pin, unscored**
  characterization run (14 blind `stream:true` trials, four body families
  insp/insplong/std/marker, 13:38:14–13:39:45Z), run under the r22 pin
  `77b8d4a0…` + instrument `bb6bd919…` because the `stream-trials` mode and
  v3 table did not exist at run time (the receipt discloses the DEVIATION,
  header `:7`); it read no journal by design (`:109`) and carries **no GT and
  no scoring** — characterization only, NOT the round's scored trials
  (D23-s10). (ii) `corpus/evidence/attrib-r23-stream.log` — **the SCORED
  instrument-mode run** (30 stream trials 13:46:41–13:49:28Z under the v3
  pin): `ACCURACY: 30/30 = 1.000 … -> PASS`; `GT counts {alibaba 6, hyper 24}`;
  **`STREAM TARGET opencode-go: on-target GT n=0 … -> FAIL`** — the target
  clause is NOT MET; the controls falsified candidates 1 and 2 (§1.4 of
  `scorecard-verdict-draft.md`). [PARENT: the coverage clause FAILED; the
  round's win is the mechanism pin + falsified controls + the 30/30 instrument
  result on what served, NOT opencode-go coverage.]
- Scorer-r23: the r23 addendum on `corpus/knowledge/attrib-r21.md:484+`
  (**landed 13:52Z**) — adjudicates the stream trials against the 0.80 bar with
  the natural/forced GT split, updates the legs table honestly, and carries the
  critic's
  self-selection-vs-attribution wording verbatim (the receipt's own
  `HONEST LIMIT (r23)` line — §1.4 of `scorecard-verdict-draft.md`). Its
  adjudication: the target clause is **NOT MET — 0 opencode-go on-target across
  ALL 104 r23 stream trials**; scored accuracy 1.000 everywhere (batch 1 14/14;
  batch 2 impl 30/30; batch 2 twin 30/30; combined 44/44 = 1.000, Wilson
  [0.920, 1.000]); the `stream-inspection` arm landed hyper 24/24.
- Lessons-distiller: `corpus/lessons/2026-10-16-round23-stream-surface.md`
  **landed 13:37Z** (untracked at draft time) — the request flag as an
  instrument surface: stream leg selection is status-only (the FAIL-marker
  scan is non-stream only, `shim.py:291-294`); the r22 marker bait cannot port
  to stream; the modes partition the feature set; the stream GT is
  header-evidenced (provenance asymmetry); NOT-RUN-with-reason if no
  header-stage forcing is disclosed. Independently reproduces the mechanism
  finding of `scorecard-verdict-draft.md` §1.1 from the same bytes.
- Scribe: the three drafts under `.ufo/rounds/round-23/goal-wave/` (this
  round's three files); zero requests, zero journal reads, shim source
  read-only and never executed (D23-s7).
- [PARENT: commit hash(es) carrying the above; LOG.md round-23 entry;
  SCORECARD.md round-23 section — drafted in
  `.ufo/rounds/round-23/goal-wave/`]

## Landed changes

- `plans/attrib_probe.py` — **landed mid-draft**: `stream-trials` mode added
  (stream-impl's sole write); sha `cce53a1637…` at 13:42:01Z, `--help` exit 0;
  requires v3 + a `stream_forcing` section. Transiently non-runnable at
  13:41:03Z (`cb2388d0…`, D23-s9).
- `plans/attrib-r23-frozen.md` (v3 table) — **landed 13:45:47Z**:
  `FROZEN: 2026-10-16T13:45:47Z sha256:1b2d6a01bfa431ec4e78bf89fd989f9ad500d10bb78634362a3c0e3bce794f87`,
  `version: attrib-feature-table-v3`, extends v2 `77b8d4a0…`,
  `stream_forcing.target: opencode-go`, budgets
  `{stream-inspection: 24, stream-marker: 3, stream-hint: 3}`; block-sha exit 0.
  **Postdates the runner's scratch trials** (D23-s10).
- `corpus/evidence/attrib-r23-stream-trials.log` — **landed 13:39:45Z**: a
  scratch-driver, v2-pin, **unscored** characterization run (14 blind stream
  trials); NOT the round's scored trials (D23-s10).
- `corpus/evidence/attrib-r23-stream.log` — **landed + scored** (the round's
  authoritative result): 30 stream trials 13:46:41–13:49:28Z under the v3 pin;
  `ACCURACY 30/30 = 1.000 PASS`; **`STREAM TARGET opencode-go: on-target GT n=0
  -> FAIL`**; the two forcing controls falsified candidates 1 and 2.
- `corpus/knowledge/attrib-r21.md` — r23 addendum (scorer-r23) — absent at
  13:51Z.
- `corpus/lessons/2026-10-16-round23-stream-surface.md` — **landed 13:37Z**
  (lessons-distiller; untracked at draft time).
- `.ufo/rounds/round-23/goal-wave/` — scribe drafts (this round's three
  files).
- [PARENT: commit hash(es); index rows in `corpus/README.md` for the new
  receipts (D23-s5: the evidence index ends at `round18-kimi-routing`,
  `corpus/README.md:91`); the inherited dirty bytes — the r22 lesson untracked
  and `plans/__pycache__/` at HEAD `407156f`, D23-s7]

## Before → after measurements

- Before (re-verified 13:33–13:40Z at `407156f`): opencode-go 0 on-target GT
  trials in both r22 runs (`attrib-r22-legs.log:310,345`;
  `target_stats.opencode-go.gt_on_target = 0`, `:362`); no stream-trial mode
  at HEAD (`plans/attrib_probe.py:114,620`; CLI subcommands `block-sha /
  freeze-check / trials / force-trials / score` only); live pin `77b8d4a0…`
  (`block-sha` exit 0); v1 pin `9f0244bb…` (exit 0); instrument sha
  `bb6bd919…`; shim sha `42d86d99…` (byte-matches the r22 table); runnable
  `.py`/`.sh` baseline 38.
- Mid-draft (13:37–13:45Z): the r23 lesson landed; the `stream-trials` mode
  landed (uncommitted); a scratch-driver stream receipt landed (unscored); the
  v3 table landed 13:45:47Z (`1b2d6a01…`).
- After (landed + scored by 13:50Z): the stream-path mechanism is pinned from
  source and confirmed by the v3 freeze's own `mechanism` field; the v3 table
  is frozen (`FROZEN: 2026-10-16T13:45:47Z sha256:1b2d6a01bfa431ec4e78bf89fd989f9ad500d10bb78634362a3c0e3bce794f87`);
  the instrument-mode run scored (`corpus/evidence/attrib-r23-stream.log`, 30
  stream trials 13:46:41–13:49:28Z): `ACCURACY: 30/30 = 1.000 (bar 0.80, min
  scored n 20) -> PASS`, `GT counts: {"alibaba-token-plan": 6, "hyper": 24}`,
  **`STREAM TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80,
  min on-target n 10) -> FAIL`**; ablations `hdr_tells` LOO 14/30, the other 12
  at 30/30. **The target clause FAILED**: opencode-go is 0 on-target — the r22
  gap is carried forward, not closed. The honest limit rides with every quoting
  surface and is STRICTER than r22's — receipt-verbatim: "the client's chosen
  body therefore SELF-SELECTS the serving leg — this is coverage of a
  client-influenced route, not of natural route weather." The round's win is
  the mechanism pin + the two empirically falsified forcing candidates
  (`stream-marker` → alibaba, `stream-hint` → alibaba) + the instrument's 30/30
  on what served.
- Standing-instrument property: the stream path is now a characterized surface
  of the P10 attribution health-check — a future instantiation re-runs it
  against a re-deployed shim under a fresh per-instantiation freeze, measuring
  attribution decay on both the non-stream and stream paths instead of
  re-deriving the mechanism from source.

## SHONEN

- [~] Real decision tables/error patterns/checklists/sources: the mechanism pin
  (§1.1 of `scorecard-verdict-draft.md`, quoted from `shim.py`) + the frozen
  table (v2, or v3 if re-frozen) are the decision surfaces; every filled value
  cites a landed receipt. [PARENT: marks stay [~] without a non-author
  verifier].
- [~] End-to-end domain task executed and logged: stream-path attribution
  trials with journal GT, scored at close; LOG.md round-23 entry drafts at
  `.ufo/rounds/round-23/goal-wave/log-entry-draft.md`. [PARENT: cite the
  landed LOG entry once integrated].
- [~] Instructions executable without oral context: the mechanism pin + frozen
  table + receipts are in-repo and self-gating (pin checks in code; the
  re-freeze policy names the superseded hash). [PARENT: marks stay [~] without
  a non-author verifier].
- [~] No cross-domain bleed: all requests localhost shims; credentials never
  read; the shim source is read-only and never executed; the journal read is
  the lane's own-probe GT pattern; any serving-plane finding (stream-path
  behaviour, leg-2 failure modes) routed to the integrator, not absorbed.
```

---

**Parent fill rules:** state at the 13:51Z poll: the r23 lesson landed 13:37Z
(`corpus/lessons/2026-10-16-round23-stream-surface.md`, untracked, folded into
`scorecard-verdict-draft.md` §1.3); the `stream-trials` mode landed (instrument
sha `cce53a1637…` at 13:42:01Z, after a transient `FROZEN_R23` NameError at
13:41:03Z, D23-s9); the **v3 table landed 13:45:47Z**
(`plans/attrib-r23-frozen.md`, `sha256:1b2d6a01…`); a scratch-driver
**unscored** stream receipt landed 13:39Z (D23-s10, predating the v3 freeze);
the instrument-mode `stream-trials` run under v3 **landed AND scored**
(`corpus/evidence/attrib-r23-stream.log`, 30 trials 13:46:41–13:49:28Z;
`ACCURACY 30/30 = 1.000 PASS`; **`STREAM TARGET opencode-go: on-target GT n=0
-> FAIL`**); the scorer addendum **landed 13:52Z**
(`corpus/knowledge/attrib-r21.md:484+`: 0 opencode-go on-target across all 104
r23 stream trials). All five seat artifacts have landed; no coverage slot
remains. Any residual slot resolves at integration from the landed bytes or
becomes an absence statement with polling evidence.
Quote landed artifacts verbatim; do not recompute scorer numbers. The remaining
`[PARENT]` markers are genuine parent-owned values: the close commit hash(es),
the LOG/SCORECARD/report integration citations, the grader re-run, the axis
verdict lines, index parity (D23-s5), the D23-s6 fleet-copy routing, and the
D23-s7 hygiene decision. **Carry the mechanism finding:** the stream path's leg
selector is the HTTP status and the marker
lever is absent on stream (`shim.py:249-294`) — a stream forcing design that
assumes a header-content selector or a working marker bait is falsified by the
source before any trial runs.
