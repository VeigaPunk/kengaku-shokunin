# Round 51 — surface truth and routed-finding attribution (hyaku run 11, 2026-10-28)

L1 `KengakuR51`. Claims frozen at `e07f131c` (`plans/round-51-claims.md`), instrument amendment
A1 appended there before the scored after-run. Base tip `297e1792`; wave spec `4090c3db`.

- **R51-C1 (freshness 8→9)** — every surface `PROVINCE.md` declares is machine-checked by
  `plans/round51_surfaces.py` against `plans/round51-surfaces.json`.
- **R51-C2 (adjacency 8→9)** — every routed finding in `corpus/routed-findings.jsonl` names its
  owner lane and disposition, and every `fixed-verified` row's check re-derives in the run.

## Gate

Candidates opened this round (SOURCES contract v1 rule 1: URL, access date, ≤25-word located
quote):

| candidate | verdict | reason / flip |
|---|---|---|
| llama.cpp server API reference, `tools/server/README.md` @ tag `b7200` (`ab49f094`) — `https://raw.githubusercontent.com/ggml-org/llama.cpp/b7200/tools/server/README.md`, opened 2026-10-28 | **ADMIT → S178** (tier A, kind `docs`, status `mined`) | quote at `:1163` (20 words): "By default, model `id` field is the path to model file, specified via `-m` … a custom value … via `--alias` argument". It grounds the pin table in `corpus/knowledge/served-endpoint-identity-pin.md`: an `id` alone identifies no weights. Fetched bytes sha256 `fb4ab6f2e4db180bf9c8…` |
| Hugging Face Hub model-revision documentation, `https://huggingface.co/docs/hub/en/models-commits` (opened 2026-10-28) | **REJECT** | the canonical path returns HTTP 404; no stable primary URL was located in-round, so no located quote exists. Flip: a stable primary URL that documents revision pinning, with a locatable anchor |
| `tbench.ai` task hub / leaderboard (S169-era lead, re-checked r50) | **unchanged reject** | not re-opened this round; the r50 rejection stands (mutable, unpinned surface, no versioned per-task spec) |

Spot-check result: the admitted row's quote and location were re-opened by the L1 at the pinned
tag and are byte-identical to the fetched capture (`sha256 fb4ab6f2…`); the rejected row is a
404 measured in-round. Non-author spot-check of this Gate is the round-51 verifier's duty.

Census: round start (run at stage-2 start, not at the first minute — disclosed)
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0,
170 rows, tier A=146/B=22/C=2, status mined=154/queued=8/rejected=8. After S178: 171 rows,
`malformed=0`, census exit 0.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `number-drift` | `PROVINCE.md:112` said the SOURCES registry holds **25 rows** while it held **170** at the base tip (`claims/c1-before.txt` `NUMBER-DRIFT SF14`) | none before round 51 — no instrument counted a declared number | `count_claim` leg of `plans/round51_surfaces.py`; shown able to fail: `NUMBER-DRIFT 1` at base tip, and `C1MutManifest` mutation 2 fires the same leg |
| `stale-premise` | three surfaces described as resolving were absent: `~/Projects/webzites/repos/llm-wiki`, `~/archive/bench-arena`, `:34113` (`corpus/evidence/round51/surfaces/paths.txt`, `endpoints.txt`) | none — the r25 practice of dating an absence was never applied to these rows | dated `ABSENT 2026-10-28` markers + the `UNVERDICTED` leg (an absent row without an ISO date fails) |
| `landing` | round-50 closure D1/D3: wave outputs uncommitted and no `WAVE-DONE` before the report | hyaku addendum §2 | this round commits the spec/dispatch before writing `.ready`, waits for `WAVE-DONE`, and commits the wave reports as evidence |
| `attribution` | `corpus/routed-findings.jsonl` carried no owner or disposition field for 71 rows (`claims/c2-before.txt` `OWNERS attributed=0`) | none — the adjacency signal ("named with its owner and routed") was never operationalised in a check | the C2 predicate: owner ∈ fleet lanes, frozen disposition set, `fixed-verified` re-runs its check, `routed` needs a non-`kengaku` owner and a `next` |
| `vacuous` | the `DRIFT` leg compares two manifest fields (`prose` vs `state`), so it is self-consistency, not truth | `C1CritDeclareAllAbsent` (critic) | external reading audit: `CritProseRead` rules every `prose` value against the row text, and the report records the leg as self-consistency. Next round: derive `prose` from the row text or require a second reader's signature |
| `survivor` | the C2 counter's check environment was never exercised before data: 61/61 pre-existing checks are lane-relative, the frozen counter ran them from a scratch cwd, and its owner regex matched 0 lines of `shokunin.conf` (6 pass vs 43 pass; 7 real lanes rejected) | `C2ExecG`, `C2ExecH`, `C2MutLedger`, `CritSurvivor` — before the scored after-run | instrument amendment A1 in `plans/round-51-claims.md` (cwd=lane, timeout 90 s, owner universe from disk ∪ conf, `--ledger` resolved); selftest gap named: no selftest case ran a lane-relative check |

## Limits

- Both counters measure this lane's own declarations; a surface nobody declared and a finding
  nobody opened are invisible to them.
- `prose` is a recorded reading (see the `vacuous` row); the reading audit is external.
- Endpoint pins are point-in-time host state; the `STALE` leg is the intended detector.
- `accepted-risk` on an open row means "known, unfixed, carried in-lane with a re-runnable
  check"; it is not a fix.
- 10 of the 75 rows carry a *record-still-holds* check rather than a fix check, because the
  residual is uncheckable on this host (an unpulled image, a frozen counter, a text property that
  does not exist). They are marked `accepted-risk` and never `fixed-verified`.
