# C2ConnServing — serving-plane ownership map (kengaku round 51, wave 1)

Seat: connector. Item: *which ledger classes and which PROVINCE surfaces belong to kama
(serving plane, endpoint identity, model flags) versus this lane (interpretation of measured
capability); quote both sides; flag every row that must be `routed` to kama rather than absorbed.*

## Axes named

- **adjacency (primary — the judged axis, C2).** `AXES.md`'s signal is *"cross-domain evidence is
  named with its owner and routed, not absorbed"*. This seat supplies the owner-assignment rule for
  the serving-plane slice of `corpus/routed-findings.jsonl`, so the C2 attribution is not done by
  guesswork at landing.
- **freshness (secondary — C1, byproduct only).** The same split decides which `PROVINCE.md` rows
  this lane may correct in-lane (its own dependency record) and which assertions are the owner's to
  make.

## Base and revisions

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7      # kengaku-shokunin tip measured (child of stage-1 freeze e07f131)
REV 7ee8cbdf160f8c945954e4737e7a2f797e3b2987      # kama-shokunin tip quoted (PROVINCE.md, SKILL.md clean)
```

`git -C ../kama-shokunin status --porcelain PROVINCE.md SKILL.md` printed nothing, so every kama
quote below is from a committed, clean tree at `7ee8cbdf`.

## Commands run (verbatim) and what they printed

```
$ python3 plans/round51_surfaces.py --lane .
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (...)
  DETAIL DRIFT SF02 prose=present state=absent (...)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0 / ANCHOR-MISSING 0 / UNCOVERED 0 / SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
C1_EXIT=1

$ python3 plans/round51_routing.py --lane .
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
C2_EXIT=1
```

Both frozen before-receipts reproduce exactly at `4090c3db` (`c1-before.txt`: DRIFT 3, UNVERDICTED 1,
NUMBER-DRIFT 1, exit 1; `c2-before.txt`: rows=71, attributed=0, checks absent=10, exit 1).

```
$ python3 - <<'PY'   # ledger scan: does any row or check touch the serving plane?
rows=71  distinct_classes=64
serving tokens (34113|8791|8793|ds-flash-shim|kama|MODEL_OK|v1/models|127.0.0.1) in ANY field:  []
checks containing curl|http://|https://|ss -ltn|127.0.0.1|:8791|:8793|:34113|kama|v1/models:  0 of 71
empty checks (10): R40-R5 R42-R3-09 R42-R3-33 R42-R3-34 R42-R3-35 R42-R3-37 R45-S5-7b R45-S5-7c R45-S5-7d R45-S5-7e
rows containing the string "shim": R40-R2 only — and that is `crit_git_shim.py`, a git test shim, not ds-flash-shim
```

```
$ ss -ltn 'sport = :8791 or sport = :8793 or sport = :34113 or sport = :8080'
State  Recv-Q Send-Q Local Address:Port Peer Address:Port
LISTEN 0      512        127.0.0.1:8793      0.0.0.0:*
LISTEN 0      512        127.0.0.1:8791      0.0.0.0:*

$ ss -ltnp 'sport = :8793'
LISTEN 0 512 127.0.0.1:8793 0.0.0.0:* users:(("python3",pid=1516,fd=3))
$ tr '\0' ' ' < /proc/1516/cmdline
/usr/bin/python3 /home/vgpnk/.local/share/glm-flash-shim/shim.py

$ sha256sum ~/.local/share/ds-flash-shim/shim.py
42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386  (464 lines)
```

`shim.py:1-14` (read-only, no HTTP traffic sent to either port):

```
"""ds-flash-shim - OpenAI-compatible cascade shim (Python 3 stdlib only).

Exposes POST /v1/chat/completions and GET /v1/models on 127.0.0.1:8791 and
forwards every chat request through an ordered 3-leg provider cascade, ...
  1. alibaba-token-plan  POST https://token-plan.ap-southeast-1.maas.aliyuncs.com/...
  2. hyper        POST https://hyper.charm.land/v1/chat/completions
  3. opencode-go  POST https://opencode.ai/inference/go/v1/chat/completions
```

`shim.py:92-93`: `STATIC_MODELS = [ {"id": "deepseek-v4.1-flash", "object": "model", ...` — `/v1/models`
on `:8791` is a **static literal**, not served identity; `DS_LEG{1,2,3}_KEY` env vars carry provider
credentials.

```
$ python3 -c "import round51_routing as R; print(len(R.load_owners(Path('/home/vgpnk/Projects/shokunin'))))"
owners_loaded 17
['aggregator','chousa','kagi','kaidoku','kake','kama','kasegi','kengaku','kotoba','kotodama',
 'kumitate','mori','protocol','souji','tabi','tameshi','unowned:integrator']
accepted: kama yes, kagi yes, kumitate yes, protocol yes, aggregator yes, unowned:integrator yes
rejected: tsukuroi, lore  (both real lanes in shokunin.conf)
$ grep -cE '^[a-z][a-z0-9-]{2,15}:\s*\{' ../shokunin.conf   -> 0
$ grep -cE '^[a-z0-9_-]+\|' ../shokunin.conf                -> 23
```

## Both sides, quoted

### kama says the serving plane, endpoint identity and probe conventions are its ground

- `../shokunin.conf:52` — `kama|kama-shokunin|operability + calibration (local model serving and endpoint health)`
- `../kama-shokunin/PROVINCE.md:10` — "producer discovery & read-only service inspection of local
  serving ports | `tools/kama-probe.sh listeners` … kama governs discovering whatever serves these
  ports and never claims an installed server"
- `../kama-shokunin/PROVINCE.md:12` — "served-model-id reconciliation | `GET /v1/models` vs `--alias`
  vs the configured model id"
- `../kama-shokunin/PROVINCE.md:13` — "liveness/readiness probe conventions | `/health`, `/props`, `/slots`"
- `../kama-shokunin/PROVINCE.md:44-45` — "Boundary rule: kama answers *\"is the thing at this baseURL
  the model this config believes it is, right now\"* — never *\"is the model good\"* or *\"is the
  request safe\"*."
- `../kama-shokunin/PROVINCE.md:53-55` — "**Out of province → report, never absorb.** Anything found
  outside the domain is named in the round report for the owning lane."

### kama says it refuses three things this lane touches

- `../kama-shokunin/PROVINCE.md:42-43` — "**Refuses:** model quality/eval (**kengaku**), credential
  material & auth flows (**kagi**), dispatch/route mechanism (**kumitate**), remote web surfaces (kake)."
- `../kama-shokunin/SKILL.md:27-29` — "**Refuses (boundary, unchanged):** model quality/eval
  (kengaku), credential … (kumitate), remote web surfaces (kake). kama never answers \"is the model
  good\" …"
- `../kama-shokunin/PROVINCE.md:186` (verbatim tail) — "The adjacent processes the staged round-13
  amendment names (the agentic-api gateway, the Semantic Router) stay refused: **a gateway and a
  route-selection product are dispatch-side surfaces** (`corpus/knowledge/cross-lane-scope.md`),
  reported to the owning lane, not absorbed."
- `../kama-shokunin/SKILL.md:139` (decision table) — "Suspected route resolves to a loopback endpoint
  | Obtain only the nonsecret endpoint/alias metadata needed for that claim | Unverified until
  observed | **Route mechanisms belong to kumitate; credentials belong to kagi.** Do not copy a
  global config or environment into the corpus."

### kengaku says kama owns serving-plane health and endpoint identity

- `PROVINCE.md:136` (Adjacent) — "| **kama** | serving plane + endpoint identity — `SKILL.md` and
  `lessons/round-16-recensus.md` record that kama is rostered and owns serving-plane health/detection
  and endpoint identity; kengaku keeps *interpretation* evidence and never remediates flags
  (`--kv-unified`, q4_0 KV, `--parallel`) — flag-change authority is unowned/integrator |"
- `SKILL.md:504-506` — "…kama's snapshot `20261014T124232Z` independently records the unit deleted
  with no listener (`../kama-shokunin/PROVINCE.md`). **Serving-plane health and detection belong to
  kama**; restoration is operator-owned."
- `PROVINCE.md:202` — "Serving-plane restoration stays operator/kama-owned."
- `SKILL.md:3` (description, anti-trigger) — "…**Anti-trigger: not serving-flag changes, endpoint
  remediation or model-serving config.**"

### kengaku also says nobody owns it (the standing contradiction)

- `PROVINCE.md:24-25` — "**Not owned:** the model-serving plane (llama-server flags, slot/batch
  config) — **no lane owns it**; escalate to the integrator instead of remediating."
- `PROVINCE.md:44-47` — "…the process-level pin above is capability-*interpretation* evidence this
  lane keeps, but flag-change authority (KV quantization level, `--parallel`, context-shift policy)
  stays unowned…"
- `PROVINCE.md:72` — "…cross-model number drawn from :34113 — flag-change authority remains unowned."

## Contradictions, stated and not smoothed

**C-1 (ownership, live at the tip).** `PROVINCE.md:24-25` says *"no lane owns it"*; `PROVINCE.md:136`,
`SKILL.md:504-506` and kama's own `PROVINCE.md:10-13` say **kama owns serving-plane health/detection
and endpoint identity**. Both sentences are committed at `4090c3db`. Neither C1 nor C2 can see the
conflict: C1 checks presence, C2 checks ledger fields, and no counter reads ownership text. This is
the round-51 surface defect behind the map below — it must be reconciled append-only, not scored away.

**C-2 (predicate vs code, C2 instrument).** `plans/round-51-claims.md` (C2 predicate) says *"every
`owner` names a fleet lane from `../shokunin.conf`"*. The frozen counter cannot read that file:
`shokunin.conf` lists lanes as `LANES="` pipe rows (23 of them, 0 brace blocks) while
`round51_routing.py:49-58` matches `^[a-z][a-z0-9-]{2,15}:\s*\{`. The accepted vocabulary is therefore
the 17-name `FALLBACK_OWNERS` literal (measured above). Consequence for this seat: `kama`, `kumitate`,
`kagi`, `protocol`, `aggregator`, `unowned:integrator` are accepted; `tsukuroi` and `lore` are real
lanes and would be **rejected**. The counter is frozen, so the honest handling is a landing note, not
an edit — but every owner string this seat prescribes is drawn from the measured 17-name set.

**C-3 (`:8793`, freshness byproduct).** `PROVINCE.md:114` says "`127.0.0.1:8791` (ds-flash-shim,
read-only shim; `:8793` not probed this round)". Measured now: **both** `:8791` and `:8793` LISTEN;
`:8793` is `glm-flash-shim/shim.py` (pid 1516). The manifest has one entry for that row (SF16, probe
`ss` on 8791 only), so C1 cannot see the second listener. Correcting `:114` in place would add an
unmeasured assertion; the C1 landing needs a dated appended correction, not a silent rewrite.

## The decision rule (identity of the responder, never the port number)

> A port is not a province. **Serving plane = a process that itself holds model weights and answers
> `/health` + `/v1/models` with the identity of the thing it serves.** A loopback listener that
> forwards to remote legs, advertises a static model list, or selects among providers is a
> **route-selection product**: kama refuses it (`PROVINCE.md:186`), its mechanism is kumitate's
> (`kama/SKILL.md:139`), its keys are kagi's (`PROVINCE.md:42`).

Applying it to the measured artifacts:

| Responder | Is it a model server? | Owner of the *endpoint* fact |
|---|---|---|
| `:34113` llama-server (deleted; kama snapshot `20261014T124232Z` records the unit deleted) | yes, when present | **kama** (identity/health) |
| `:8791` `ds-flash-shim/shim.py` | no — 3 remote legs, static `/v1/models` id `deepseek-v4.1-flash`, `DS_LEG*_KEY` | **kumitate** (mechanism) + **kagi** (credentials); **not kama** |
| `:8793` `glm-flash-shim/shim.py` | no — same product family | **kumitate** + **kagi**; **not kama** |

## PROVINCE surface map

Manifest ids are from `plans/round51-surfaces.json` at `4090c3db`; line pins are `PROVINCE.md`.

| Surface (line) | What the row asserts | Owner of the assertion | kengaku keeps | Disposition of *this lane's* row |
|---|---|---|---|---|
| **SF03** `Served local model` (:14) | `:34113` `/v1/models`, `/health`, `/v1/chat/completions`, model id, `n_ctx=16384`, process pin with 41-token argv | **kama** — endpoint identity + liveness/readiness (`kama/PROVINCE.md:12-13`; `SKILL.md:505`) | the *capability interpretation* drawn from it (the r8/r9 numbers and their `--cache-type-k/v q4_0` premise) | **absorb + date it ABSENT.** kama already records the absence (`kama/PROVINCE.md:10`), so no re-probe is owed to kama; C1's fix is this lane dating its own dependency |
| Historical `:156` (`:34113` / `ss`) | no listener | kama | — | outside the manifest (see coverage note) |
| Historical `:157` (`/proc/1299/cmdline`, unit, jinja) | absent | **process observation = kama** (`kama/PROVINCE.md:10`); **flag-change authority = `unowned:integrator`** (`PROVINCE.md:44-47,:72`) | the argv *as a premise of interpretation* | **referral to `unowned:integrator`**, not routed to kama — kama's Owns table has no flag row and its boundary is identity, not flags |
| **SF15** `ds-flash-shim source (read-only)` (:113) | `sha256sum …/shim.py` = `42d86d99…15a386` (measured identical) | **not kama** — the artifact is a credential-bearing cascade router (`kama/PROVINCE.md:42` kagi/kumitate) | the **digest pin** itself: provenance of this lane's own attribution instrument | **absorb** (in-lane pin, no endpoint claim). Any *content* claim about legs/keys is a kumitate/kagi report-out |
| **SF16** `Live probe endpoint` (:114) | `ss -ltn 'sport = :8791'` → LISTEN | **not kama** — route-selection product refused at `kama/PROVINCE.md:186`; mechanism is kumitate's (`kama/SKILL.md:139`) | the **presence fact as an instrument dependency** (the attribution evidence flowed through it) | **absorb the presence fact; refer the mechanism.** Must not become an identity claim |
| SF01, SF02, SF04-SF14, SF17-SF19 | wiki / bench-arena / telemetry / catalogs / own evidence / gate / instruments / registry count | kengaku | all | absorb (no serving-plane content) |

**Coverage note (C1, byproduct).** The `### Historical` table (`PROVINCE.md:145-166`, 12 rows) and
`### Adjacent` (`:129-141`) declare surfaces too, but the manifest's `sections` are only
`"## Surfaces"` and `"### Core"`. Of the 12 Historical rows, two (`:156`, `:157`) are serving-plane
declarations and neither is machine-checked; `:156` restates the same `:34113` absence as SF03 under a
different check (`ss` vs `http`). C1's claim is therefore true of the two manifest sections only — a
landing note should say so rather than let "every surface PROVINCE.md declares" stand unqualified.

## Ledger class map

71 rows, **64 distinct classes**, all assigned; family counts measured, not estimated.

| Family | Classes | Rows | Owner | Why not kama |
|---|---|---|---|---|
| counter / guard / instrument soundness — incl. the near-miss rows `host-safety-envelope` (R40-R2), `envelope-drift-record` (R42-R3-32), `probe-work-dir-traceback` (R39-R2), `plan-host-dependent-cheat` (R42-R3-37), `c1-counter-soundness` (R40-R1/R40-R1.1) | 25 | 27 | **kengaku** | every defect sits in *this lane's* counter, guard or wave spec; the bwrap `--unshare-net` envelope is kengaku's own sandbox. A sandbox that cannot reach `:8791` is a kengaku instrument fact, not an endpoint-identity fact |
| doc citation / accuracy (`entry-*`, `lesson-*`, `criterion-*`, `frozen-cell-*`, `readme-*`, `scorecard-*`, `row-anchor-*`, `log-in-place-rewrite`, `receipt-without-revision`, …) | 30 | 33 | **kengaku** | all cite this lane's own `corpus/`, `SKILL.md`, `SCORECARD.md`, `LOG.md` |
| plan / claim-freeze hygiene (`plan-*` ×5, `v11-lookup-predictors`) | 6 | 6 | **kengaku** | the plan artefacts are this lane's frozen claims |
| fleet rule / process — `sources-correction-rule` (R42-R4), `round-close-unregistered` (R40-R3) | 2 | 2 | **`aggregator`** (fleet corpus review, `shokunin.conf:21`); row's own note: the rule "exists only outside the lane: …/CORPUS.md:116-118 … read-only" | fleet-side rule, not kama's |
| carried bundle (`carried-residuals-bundle` ×3) | 1 | 3 | **kengaku** | bundles of the above |

**Near-miss rows examined one by one and rejected for kama:**

- `R40-R2 host-safety-envelope` — contains the string `shim`, but the check greps
  `crit_git_shim.py` (a **git** test shim in `.ufo/waves/round-40/build/`). Unrelated to
  `ds-flash-shim`. Absorbed by kengaku.
- `R39-R2 probe-work-dir-traceback`, `R42-R3-32 envelope-drift-record`, `R42-R3-37 plan-host-dependent-cheat`
  — host *dependence* of this lane's own instruments; kama owns no artifact that would change.
- `R40-R1` / `R40-R1.1` / `R42-R1 c1-counter-soundness*` — the sandbox's inability to reach host
  sockets is a soundness property of the counter, not a serving-plane finding.
- `R42-R3-35 plan-missing-refusals` — a *plan* missing refusals; the refusal text it should carry is
  this lane's own, and C-1 above is the substantive gap it points at.

## Rows that must be `routed` to kama

**Measured answer: none. 0 of 71.** No ledger row names `34113`, `8791`, `8793`, `ds-flash-shim`,
`kama`, `MODEL_OK` or `v1/models` in any field, and none of the 71 checks touches the network. The
serving plane is absent from the ledger, not absorbed by it — so the correct C2 attribution for this
tip is `owner: kengaku` on the five families above, `owner: aggregator` on the two fleet-rule rows,
and **`routed` count 0**, which the predicate accepts (`NEXT violations=0` with zero routed rows).

**Forward rule (what a future row must carry so the map does not rot).** A row opened on any of these
classes is **not** absorbable and must carry `owner: kama`, `disposition: routed`, `next:` naming a
kama action: `endpoint-identity`, `served-model-id`, `liveness-probe`, `producer-discovery`,
`model-flag` (observation only — flag *change* goes to `unowned:integrator`), `baseURL-pin`.
Two classes must **never** be routed to kama despite looking like it: `route-mechanism` /
`fallback-policy` → `owner: kumitate`; `endpoint-credential` / `key-handling` → `owner: kagi`
(`kama/PROVINCE.md:42-43,186`; `kama/SKILL.md:139`). A `:8791`/`:8793` identity row would be a
category error: the shim's `/v1/models` is a static literal (`shim.py:92-93`), so `MODEL_MISMATCH`
would be true by construction and the row would measure nothing.

## Recommended landing text (append-only, for L1 — not applied by this seat)

1. `PROVINCE.md:24-25` reconciliation: "**Correction 2026-10-28 (round 51):** the `:24-25` "no lane
   owns it" sentence is superseded by `:136` and `SKILL.md:504-506`. Serving-plane health, detection
   and endpoint identity are kama's (`../kama-shokunin/PROVINCE.md:10-13`; `shokunin.conf:52`); this
   lane keeps interpretation evidence; flag-change authority stays `unowned:integrator`."
2. SF03 row: dated `ABSENT 2026-10-28` marker plus "kama's snapshot `20261014T124232Z` independently
   records the unit deleted" — the absence is already the owner's record, so no kama probe is owed.
3. `PROVINCE.md:114`: "**Correction 2026-10-28 (round 51):** `:8791` and `:8793` both LISTEN
   (`ss -ltn`); the responders are `ds-flash-shim/shim.py` and `glm-flash-shim/shim.py` —
   route-selection products, not model servers. kama refuses them (`../kama-shokunin/PROVINCE.md:186`);
   the mechanism is kumitate's, the keys are kagi's. This lane records presence only."
4. Limits sentence for C2: the counter's owner vocabulary is its frozen 17-name literal, not
   `../shokunin.conf` (C-2); a future owner string must be checked against that set, and `tsukuroi` /
   `lore` are real lanes that the frozen counter rejects.

## Risks

- **kama's line 186 is load-bearing and not mine.** If kama narrows or widens the gateway /
  route-selection refusal, the `:8791`/`:8793` assignment changes from kumitate to kama. Quoted at
  `7ee8cbdf`; re-read before landing.
- **`unowned:integrator` is a real accepted owner** (it is in the measured 17-name set), so routing
  SF03's *flags* there is executable — but it is a referral, not a routed finding, and C2's `next`
  rule does not require it; do not add a `next` that no one will execute.
- **The shim is credential-bearing.** Nothing in this lane may read `DS_LEG*_KEY`; the digest pin
  (`SF15`) and the docstring are sufficient provenance. `kama/SKILL.md:139` warns against copying
  config/environment into the corpus.
- **`MODEL_MISMATCH` by construction** on `:8791` (static model list) — the trap a naive
  "reconcile every endpoint" attribution would walk into.
- **C-2 vocabulary gap** could silently reject an otherwise correct attribution at landing; verify
  `owner in {measured 17}` before writing any row.

## Limits

- Point-in-time: `ss` sample at the moment of measurement; `:34113` absence is asserted by this
  lane's counter and by kama's snapshot, not re-probed here.
- No HTTP traffic was sent to `:8791`/`:8793`; the responder type comes from `ss -ltnp`, `/proc`
  cmdline and the shim's committed source, not from a request.
- Read-only against both lanes. kama quoted at `7ee8cbdf` (clean); kengaku measured at `4090c3db`.
- This seat assigns owners for the serving-plane slice and the five ledger families; it does not
  write any ledger row, and it did not run `--run-checks` (that is the C2 executor seats' work).
- Tooling: nothing installed, nothing upgraded (no pacman transaction attempted).

## VERDICT

Serving-plane ownership splits on **responder identity, not port number**: `:34113` is kama's
(endpoint identity + liveness, `kama/PROVINCE.md:10-13`); `:8791` and `:8793` are **not** kama's —
they are cascade/route-selection products that kama's own province refuses (`kama/PROVINCE.md:42-43,186`;
`kama/SKILL.md:139`), so their mechanism is kumitate's and their keys kagi's. `SF15` (shim digest) is
absorbable as an in-lane provenance pin; `SF03` is absorbed-and-dated because kama already records the
absence; `:157`'s flags are a referral to `unowned:integrator`. **Zero of 71 ledger rows must be
`routed` to kama** (measured: no serving token in any field, no networked check); the correct C2
attribution is kengaku ×69 rows / `aggregator` ×2 / routed ×0 (69+2 = 71). Two contradictions are stated, not
smoothed: kengaku's `:24-25` "no lane owns it" vs `:136`/`SKILL:505` "kama owns it" (C-1), and C2's
predicate text "from `../shokunin.conf`" vs its frozen 17-name owner literal (C-2).

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
