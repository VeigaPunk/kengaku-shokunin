# log-entry-draft — kengaku round 23

Scribe seat, round-23 goal wave. Written 2026-10-16; starting state captured
13:33–13:40Z at HEAD `407156f` (round-22 records; the r22 evidence commit is
`8a08483`). **This file writes nothing** — `LOG.md` is PARENT-owned; the block
below is a paste-ready entry in the round-19/20/21/22 LOG idiom
(`## <n> — <title>` section; see `LOG.md` §19–§22). `[PARENT]` markers and
`{{PLACEHOLDER}}` slots resolve from landed artifacts at integration time;
every resolved value must quote its receipt (lane rules: "Every change appends
a LOG.md entry with the evidence that motivated it"; "Never fabricate domain
knowledge"). Placeholders must not ship — an unresolved slot becomes an
absence statement with polling evidence. No scalar axis verdicts.

---

```markdown
## Round 23 — opencode-go stream-path coverage (goal wave)

**Round 23 (2026-10-16).** Motivating evidence: the r22 close named one gap —
opencode-go took 0 on-target GT trials in both runs (the compliant-echo marker
bait starves against reasoning models), and registered r23 as forcing
opencode-go via the ds shim's STREAM path (`corpus/knowledge/attrib-r21.md:466-
471`; `SCORECARD.md:543-545`). Landed (evidence commit [PARENT: hash]):
(a) the stream-path leg-selection mechanism is pinned from shim source,
quoted — read-only, sha `42d86d99…` (byte-matches the r22 table's
`shim_code_sha256`): the stream selector is the per-leg HTTP STATUS
(402/403/429/5xx/400-`data_inspection_failed` -> next leg; 200 -> serve and
stream, `shim.py:249-278`); headers are relayed (`shim.py:336-344`) but never
parsed for the leg choice; the `FAIL_MARKERS` body scan (`shim.py:291-294`) is
NON-STREAM ONLY — so the r22 echo-marker bait is structurally inert on stream
and the stream path REMOVES a forcing lever rather than adding one
(the authoritative pin is `plans/attrib-r23-frozen.md:44-50`, stream-impl's,
which quotes `shim.py:270-278`, `:291-294`, `:210-217`, `:249-268`,
`:299-315` and falsifies candidate 1 (marker bait) and candidate 2 (client
hint) by code: "on stream:true the shim picks the leg from the response
HEADERS before any body byte … and RETURNS BEFORE the FAIL-marker scan …
so a 200 marker bait CANNOT force a fallthrough on the stream path …
NO client hint selects a leg … leg-2->leg-3 needs leg-2 to fail, which no
body forces (candidate 3: reachable only probabilistically)"). (b) A
stream-trial mode landed in the
instrument (`stream-trials`; instrument sha256
`cce53a16373966e1c1f71f7c7a981e7b81a397865087f347f36ebc6217284781` at 13:42:01Z;
per-chunk SSE frame capture); the feature table was **extended and RE-FROZEN as
v3 BEFORE the instrument-mode trials**: `plans/attrib-r23-frozen.md`
`FROZEN: 2026-10-16T13:45:47Z
sha256:1b2d6a01bfa431ec4e78bf89fd989f9ad500d10bb78634362a3c0e3bce794f87`
(`version: attrib-feature-table-v3`, extends v2 `77b8d4a0…`,
`stream_forcing.target: opencode-go`, budgets
`{stream-inspection: 24, stream-marker: 3, stream-hint: 3}`; block-sha exit 0).
The runner's earlier scratch-driver receipt (13:38–13:39Z) predates
this freeze and is unscored; only the instrument-mode run under v3 is the
round's scored trials (D23-s10).
(c) Stream trials: **the target clause FAILED, landed honestly** —
`corpus/evidence/attrib-r23-stream.log`, 30 stream trials 13:46:41–13:49:28Z
under the v3 pin: `ACCURACY: 30/30 = 1.000 (bar 0.80, min scored n 20) -> PASS`;
`GT counts: {"alibaba-token-plan": 6, "hyper": 24}`;
`STREAM TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80,
min on-target n 10) -> FAIL`. Controls falsified the two candidates as
predicted: `stream-marker` 3/3 → alibaba (marker bait inert on stream),
`stream-hint` 3/3 → alibaba (no client hint selects a leg), `stream-inspection`
24/24 → hyper (leg-1 bait cascades; leg-2 never fails, so leg-3 is unreached).
Ablations: `hdr_tells` LOO 14/30; the other 12 at 30/30. Scored against journal
GT read ONLY after ALL trials (structural blind rule: `journalctl` occurs only
inside `cmd_score`); the honest limit rides with every quoting surface and is
STRICTER than r22's — receipt-verbatim: "the client's chosen body therefore
SELF-SELECTS the serving leg — this is coverage of a client-influenced route,
not of natural route weather." (d) The r23 addendum on
`corpus/knowledge/attrib-r21.md` (`:484+`, scorer-r23, landed 13:52Z) updates
the legs table honestly: the target clause is **NOT MET — 0 opencode-go
on-target across ALL 104 r23 stream trials** (batch 1 runner 14, batch 2 impl
30, batch 2 twin 30, verifier 30 unscored); scored accuracy 1.000 everywhere
(batch 1 14/14; batch 2 impl 30/30; batch 2 twin 30/30; combined main receipt
44/44 = 1.000, Wilson [0.920, 1.000]); the `stream-inspection` arm landed hyper
24/24 (the r22 T03 leg-2 failure did not reproduce); the falsifier seat recorded
alibaba serving a streamed body literally containing `usage limit` with no
fallthrough; the v3 `feature_extension_ruling` freezes the per-chunk features as
captured-but-weightless. The self-selection wording above is the critic's
clause-(d) statement and is carried verbatim. Lesson:
`corpus/lessons/2026-10-16-round23-stream-surface.md` (landed 13:37Z,
lessons-distiller) — the request flag is an instrument surface: the `stream`
flag selects a second leg-selection surface (status-only; the FAIL-marker scan
is non-stream only, `shim.py:291-294`), so the r22 marker bait cannot port to
stream and only the leg-1 content-inspection bait survives the flag; the
modes partition the feature set (`body_schema`/`id_in_body` abstain on stream,
`stream_span_class` abstains on non-stream), so a v3 must declare the
mode→feature mapping; the stream GT is header-evidenced while the non-stream GT
is body-evidenced (provenance asymmetry); if no header-stage forcing is
disclosed, the opencode-go clause is NOT-RUN-with-reason. Wave: 32 seats,
deepseek flash bucket (`cascade/deepseek-v4.1-flash`; the operator switched
back from zai after r22).

**Boundaries held.** Small localhost stream requests only ({{REQUEST_COUNT —
enumerated before the freeze}}; ≥2.5 s spacing; no retries); credentials never
read; the shim source is read-only and was never executed; journal reads are
read-only GT after ALL trials; seats committed nothing; parent integrated under
the kengaku lane identity.

**Honest note (the coverage clause FAILED as landed).** opencode-go took 0
on-target GT trials (n=0 < 10) — the r22 gap is carried forward, not closed.
The round's win is the mechanism pin + the two empirically falsified forcing
candidates + the instrument's 30/30 on what served; it must never be redefined
into "coverage of opencode-go" or "instrument exists". The honest next lever is
a header-stage / upstream-status mechanism (r20 P9 precedent: an absence scored
honestly is a landed result).
```

---

**Fill sources:** the mechanism pin + stream-trial mode + v3 table are
stream-impl's (`plans/attrib_probe.py`, sha `cce53a1637…`; `plans/attrib-r23-frozen.md`,
FROZEN 13:45:47Z `1b2d6a01…`); the stream-trial receipts are stream-trial-runner's
(`corpus/evidence/attrib-r23-stream.log` — the SCORED v3 run; `attrib-r23-stream-trials.log`
— the earlier scratch-driver run, D23-s10); the r23 addendum is scorer-r23's
(`corpus/knowledge/attrib-r21.md:484+`, **landed 13:52Z**); the lesson
landed 13:37Z (`corpus/lessons/2026-10-16-round23-stream-surface.md`, untracked).
**State at the 13:56Z poll:** all five seat artifacts have landed — the
mechanism pin + v3 freeze + the scored instrument-mode run + the r23 lesson +
the scorer addendum; the round's coverage clause is NOT MET (opencode-go 0
on-target). Dates: the lane's LOG dates are local dates of
the work (2026-10-16 UTC, local −03); the parent picks the entry date at commit
time (round-14 precedent).
