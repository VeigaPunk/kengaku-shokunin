# r13-connector — round-13 re-dispatch ownership map (advisory, coverage axis)

Connector seat, steered round 13 re-dispatch, 2026-10-15. Baseline commit
`3f31e54c6e7aeddef13db11985b3c7a9dad9e0cf`. Inputs: `PROVINCE.md` (lane),
`/home/vgpnk/Projects/shokunin/MANIFEST.json` (fleet roster + round records),
sibling provinces `kama-shokunin/PROVINCE.md`, `kumitate-shokunin/PROVINCE.md`,
inherited `surface-receipt.json` (this directory) and
`corpus/lessons/round-13-coverage.md`, `corpus/lessons/round-16-recensus.md`.
Read-only outside the lane; no re-probe run — the receipt's absences and
endpoint `ECONNREFUSED` (observed 2026-10-15T04:49:50Z, surface-receipt.json:5)
are accepted as this round's measurement per contract.

## Move (one, bounded)

Replace the round-13 coverage chain's only **unresolvable handoff route** —
"the model-serving plane … no lane owns it; escalate to the integrator"
(`PROVINCE.md:24-25`) — with the **named current owner already rostered in the
fleet**, backed by exact pointers. This improves honest source-availability
coverage (every absent surface gains an addressable owner instead of a dangling
escalation) and corpus discovery (one index of ownership pointers for the
round-13-coverage evidence set). It claims **no** source restoration, **no**
endpoint repair, **no** new model result, **no** novelty, and **no** score
movement: the coverage anchor stays 7 under the existing declared-but-
unresolvable-surface cap; the round-16 audit already named this exact debt at
`corpus/lessons/round-16-recensus.md:27-28` ("`PROVINCE.md:24-25` says no lane
owns the serving plane; kama is rostered and owns endpoint identity. Reported,
not absorbed.") — this artifact completes the mapping, it does not re-litigate
it. Harm check: append-only here; nothing edited outside this file; sibling
scope is reported out, not absorbed.

## Current ownership map (evidence-backed)

| Domain | Current owner | Exact evidence |
|---|---|---|
| Evaluation & corpus interpretation ("is the model good", what a number means) | **kengaku** (this lane) | roster `/home/vgpnk/Projects/shokunin/MANIFEST.json:15-21` (`kengaku`, "LLM/model research & evaluation"); `kama-shokunin/PROVINCE.md:17` ("Refuses: model quality/eval (kengaku)"); lane keeps the r8–r14 process-pin as capability-*interpretation* evidence (`kengaku/PROVINCE.md:44`) |
| Endpoint / serving-plane identity, liveness, drift, probe conventions (`:34113`, `qwen-coder.service`, `llama-server` argv) | **kama** — detection/reporting; **operator** — writes & restoration | roster `MANIFEST.json:54-61` (`kama`, "local model serving & endpoint health", minted 2026-09-29); `kama-shokunin/PROVINCE.md:10` lists the surface row "`~/.config/systemd/user/qwen-coder.service` (llama-server, `127.0.0.1:34113`)" verbatim; `:12-13` served-model-id reconciliation + `/health /props /slots` probes; `:22-26` hard write boundary — unit files are operator-owned, "kama *detects and reports* stale pins, and the operator repoints them" |
| Routing / OMP route resolution, fallback policy, operational-failure taxonomy | **kumitate** (tooling owner) | roster `MANIFEST.json:30-37` ("orchestration & tooling (OMP, scripts, Rust runtime)"); lane's own refusal row `kengaku/PROVINCE.md:27-28`; kama defers "dispatch/route mechanism (kumitate)" `kama-shokunin/PROVINCE.md:18` |
| Source restoration (absent host paths: wiki, bench-arena trees, `~/.bailian`, bounties ledger) | **operator** (host state) | `kengaku/PROVINCE.md:76-81` ("Cause is operator-side host state, not lane state"); `kama-shokunin/PROVINCE.md:22-24` (operator repoints host config); `corpus/lessons/round-13-coverage.md:57-58` ("Source restoration and endpoint health belong to the operator and the current serving-plane owner, not kengaku"). Considered and rejected as routing targets: `chousa` owns general source-*research method* only, not host filesystem state (`MANIFEST.json:2307-2315`, mint notes); `kagi` owns secrets/vault ops (`MANIFEST.json:46-53`) — the absent paths are not credential material. |

## Is "unowned serving plane" stale? — Yes as a lane-ownership claim; one clause still true

- **Stale:** `kengaku/PROVINCE.md:24-25` ("no lane owns it; escalate to the
  integrator"), repeated at `:43-47` (round-10 report-out: "flag-change
  authority … stays unowned") and `:67-72` (round-11: "flag-change authority
  remains unowned"). kama was minted in probation on 2026-09-28
  (`MANIFEST.json:913-917`, round-11.5 record — and note the demand instances
  named there are "kagi r3 + **kengaku r4 endpoint-drift 8080->34113**": this
  lane's own r4 evidence was one of two reasons the serving plane got an owner),
  and its roster row is now published (`MANIFEST.json:54-61`) with verified
  lane rounds (first closure naming kama: `MANIFEST.json:1318-1320` `"kama": "ok"`;
  latest closure 2026-10-14, closed 2026-10-15T00:23:52Z: `kama: "ok"`,
  `lane_rounds.kama: 4` at `MANIFEST.json:2316-2336`). The row-withholding
  clause in the mint note ("Roster row withheld until >=3 verified self-iteration
  rounds", `:917`) is superseded by the published row.
- **Timing coincidence worth recording:** the lane's surface table was
  re-verified "round 14, 2026-09-29" (`kengaku/PROVINCE.md:8`) — the same day
  kama's roster row carries as `minted` (`MANIFEST.json:60`) — yet the
  round-9 refusal text above the table was never touched, and rounds 12/14
  closed with "No new serving plane report-out" (`:90-92`). So the stale
  wording survived two re-verifications; the lane ledger's own
  `SCORECARD.md:298-300` ("the mint decision is integrator-pending") was
  adjacency evidence frozen at mint time, not current truth.
- **Still true inside the stale wording:** flag-change *execution* on the unit
  file is not lane-ownable — kama's hard write boundary (`kama-shokunin/PROVINCE.md:22-26`)
  puts `~/.config/systemd` writes with the operator. What is no longer true is
  that *no lane* holds endpoint detection, reconciliation, and probe convention;
  "escalate to the integrator" is also falsifiable as a route: no roster id
  "integrator" exists among the 13 ids at `MANIFEST.json:5-110`.

## Bounded handoffs arising from `surface-receipt.json` (report, do not remediate)

1. `:34113/health` ECONNREFUSED + absent `qwen-coder.service`, jinja template,
   `/proc/1299/cmdline` (receipt `paths` + `endpoint`) → **kama** as
   endpoint-identity/liveness owner for detection + served-model reconciliation
   when a future endpoint returns; restoration execution (unit file, process
   start) → **operator**. This lane marks its `PROVINCE.md:14` surface
   historical-unavailable and keeps retained run bytes; it does not re-probe,
   restart, or write host config.
2. Absent `~/Projects/webzites/repos/llm-wiki`, both `bench-arena` trees,
   `~/.bailian`, `~/Projects/bounties/ledger/telemetry.jsonl` (receipt `paths`)
   → **operator** (host state). Source restoration is out of province by
   `round-13-coverage.md:57-58`; a retained digest in this corpus is not
   original bytes (lesson `:28-29`).
3. Ledger telemetry semantics → **kasegi**, already reported
   (`kengaku/PROVINCE.md:74-81`); no new evidence this session.
4. `telemetry_source=journal` taxonomy interaction → **kumitate**, already
   reported (`kengaku/PROVINCE.md:48-54`); routing ownership is restated in the
   map above, not newly escalated.

## Overlap needing report-out (not absorbed)

`kengaku/PROVINCE.md:14` (Served local model surface row) and
`kama-shokunin/PROVINCE.md:10` name the **same unit and port**. The split per
kama's boundary rule (`:17-20`: kama answers "is the thing at this baseURL the
model this config believes it is, right now", never "is the model good"):
endpoint identity/probe/reconciliation = kama; capability interpretation of the
pinned argv (q4_0-KV materiality etc.) = this lane, retained. Recommended
wording patch for PROVINCE.md `:24-25`, `:43-47`, `:67-72` — "escalate to the
integrator / authority unowned" → "owned by kama (detect/report); flag writes
operator-side (kama PROVINCE.md:22-26); interpretation kept in-lane" — is
**referred to the parent/integrator**, who owns README/SHONEN/SCORECARD/LOG/
lessons/final reports; this seat edits nothing else (assignment: "No other
edits"). No arbitration is claimed beyond the cited roster and province text.

## Risks and limits

- kama's closure `ok` (`MANIFEST.json:2316-2336`) is **lane-round status, not
  endpoint health**; it does not contradict the receipt's ECONNREFUSED and must
  not be read as restoration.
- If the fleet later alters the roster (rank shonen, probation lineage), this
  map is the stale-candidate; recheck `MANIFEST.json` roster + kama PROVINCE
  before reusing in a later round.
- I did not open kama's own round reports; ownership rests on the published
  roster row and province text only. `[INFERENCE]` flag: none used — every
  claim above has a literal cited line except the timing-coincidence remark,
  which cites both dates as printed.
- Coverage cap unchanged; index insertion of this file into `corpus/README.md`
  is parent-owned.

## Verification (reader-falsifiable, read-only)

`grep -n '"kama"' /home/vgpnk/Projects/shokunin/MANIFEST.json` → roster row at
`:54-61`, closures naming kama; `sed -n '3p;10p;17p;18p;22,26p'
/home/vgpnk/Projects/shokunin/kama-shokunin/PROVINCE.md` (read tool preferred)
→ domain, surface row, refusals, write boundary; `read PROVINCE.md:22-25,43-47,67-72`
→ the stale wording under correction; `read corpus/lessons/round-16-recensus.md:27-28`
→ pre-existing named debt this artifact completes; `read
corpus/evidence/round13-coverage/surface-receipt.json` → accepted observation.
No re-probe, no service touched, no outside write.
