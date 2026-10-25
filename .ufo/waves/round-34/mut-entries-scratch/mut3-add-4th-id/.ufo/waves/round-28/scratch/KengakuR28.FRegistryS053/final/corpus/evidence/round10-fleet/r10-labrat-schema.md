# r10-labrat-schema — empirical schema invariants of committed probe evidence

Re-run script: **`/tmp/kengaku-r10/schema_probe.py`** (`python3 /tmp/kengaku-r10/schema_probe.py`; stdlib-only, read-only, deterministic — verified byte-identical output under `PYTHONHASHSEED=1` vs `=99` vs default). Full output preserved at `/tmp/kengaku-r10/probe-output.txt`.

All facts below are script-observed output, not inference. Records: R8 268, R9 284 (exact line counts confirmed via `wc -l`).

## Per-file invariant table

| Invariant | R8 (round8-horizon/results.jsonl) | R9 (round9-replication/results-r9.jsonl) |
|---|---|---|
| cells | 13: meta(10), A-CKPT(30), A-CKPT-ack(70), A-INC(100), A-MONO(10), 4×B-*(8 each), 4×C-*(4 each) | 8: meta(8), A-CKPT4710(24), A-CKPT4710-ack(56), A-CKPT710(16), A-CKPT710-ack(64), A-INC(80), A-MONO(8), filler(28) |
| key-set variants per cell | exactly 1 everywhere | exactly 1 everywhere |
| pid universe | 1–10 (meta pids identical) | 101–108 (meta pids identical) |
| meta truth/ops | truth_len=ops_len=10 all pids; init 5 keys; `tail_touched` list[str] | same, 8 pids |
| consecutive equal truth states | none | **pid=108: truth[2]==truth[3]** (neutral op; harmless — see want rule) |
| A-cell turn coverage (uniform all pids) | A-INC 1..10; A-CKPT {4,7,10}; A-MONO {1} | A-INC 1..10; A-CKPT4710 {4,7,10}; A-CKPT710 {7,10}; A-MONO {1} |
| ack cells (no `ok`, carry pid/turn/raw) | A-CKPT-ack turns {1,2,3,5,6,8,9}, exact disjoint complement of A-CKPT within 1..10 | A-CKPT4710-ack {1,2,3,5,6,8,9} ↔ A-CKPT4710; A-CKPT710-ack {1,2,3,4,5,6,8,9} ↔ A-CKPT710 (both exact complements) |
| duplicate (cell,pid,turn) | 0 (graded); 0 (ack, on (pid,turn)); 0 on (cell,pid,turn,rep) for C cells | 0 (graded); 0 (ack) |
| `got` type | dict-or-None rule holds on all A/B; **C-MONO got = list-of-lists (4×4 square)**; C-trio got = dict `{violations, square}` | dict-or-None holds (no C cells in r9) |
| missing/empty `raw` | 0 anywhere (all 268 records with `raw` non-empty str) | 0 anywhere |
| **stored `want` == meta truth[turn-1]** | YES for A-CKPT (30/30), A-INC (100/100). NO for **A-MONO (0/10) and all 4 B cells (0/32): want == truth[9] = FINAL state while turn=1** | YES for A-CKPT4710 (24/24), A-CKPT710 (16/16), A-INC (80/80). NO for **A-MONO (0/8): want == truth[9] while turn=1** |
| ok == (got==want) | 0 violations (all 172 graded) | 0 violations (all 128 graded) |
| `nwrong` | present only on A-CKPT/A-INC/A-MONO; always == top-level key-diff count; **absent on B cells and ack** | present only on the 4 A cells; always consistent; absent on ack/filler |
| final graded turn per (cell,pid) finish=='stop' | HOLDS (all 172 graded finish='stop'; ack too) | **r9 claim HOLDS** (all 128 graded finish='stop'; ack + filler too) |
| B-cell shapes (corrupt_field,corrupt_from,outcome,healed) | clean-hint & clean-plain: 2 shapes each — (null,null,"corrected",true)×6, (null,null,"other",true)×2. corrupt-hint: 8 distinct (all healed=true; outcomes mixed corrected/other). corrupt-plain: 8 distinct (outcomes corrected/other/propagated; healed true/false, no 1:1 outcome↔healed rule). pids 1–8, turn=1 | no B cells |
| B corrupt_from | **NOT derivable**: == init[field] for only 8/16 corrupt records; == got[field] for 1/16 → must be compared verbatim from the record | n/a |
| C split | record counts 12 (conflict+benign+norule) vs 4 (C-MONO): CONFIRMED. Trio cells share one identical key-set; C-MONO lacks `over_repair`,`parse`,`preserved`,`viol_ok`. Flags: C-MONO ok=T,square_valid=T ×4; C-conflict ok=T,over_repair=F ×4; C-norule ok=T,over_repair=F ×4; C-benign = 1× ok=T + 3× (ok=F,square_valid=F,over_repair=T) | no C cells |
| `request_ts` | absent (0 records) | present on all 276 non-meta records, ISO str, range 2026-09-28T21:17:58Z..21:18:57Z; **absent on meta** |
| `usage` | present on all non-meta records, always keys {completion_tokens, prompt_tokens, prompt_tokens_details, total_tokens} | same (276 records) |
| `wall_s` | float on all 258 non-meta records | float on all 276 non-meta records |
| filler cell | none | 28 recs: **no pid, no turn, no rep, no ok**; raw always "ready"; finish "stop" |

## Anomalies the grader must special-case

1. **want semantics split** (the only hard mismatch class): `want == truth[turn-1]` holds ONLY for A-CKPT/A-CKPT4710/A-CKPT710/A-INC. For **A-MONO (both files) and all R8 B cells**, `want == truth[len-1]` (final state) while `turn==1`. A grader that recomputes `want` as `truth[turn-1]` uniformly will emit 50 false MISMATCHes (42 R8 + 8 R9).
2. **C-MONO `got` is a list (4×4 square), C-trio `got` is a dict** `{violations, square}` — any got-shape assumption must branch on cell. C-MONO also lacks the four trio-only boolean flags (`viol_ok`, `parse`, `preserved`, `over_repair`).
3. **`nwrong` absent on R8 B cells** (and ack/filler/meta everywhere); recomputation of `nwrong` must be conditioned on key presence.
4. **R9 `filler` records carry no pid/turn/rep** — any record keying by (cell,pid,turn) must whitelist/skip `filler` (and `meta`, which has no turn/usage/wall_s/request_ts).
5. **`request_ts` exists only in R9** (and only on non-meta records) — a cross-file uniform schema assumption breaks.
6. **R9 meta pid=108 has truth[2]==truth[3]** (a state-neutral op). Harmless for `want==truth[turn-1]` (verified 24/24, 80/80 etc.), but any "strictly increasing distinct states" assumption would be false.
7. **B `corrupt_from` is not recomputable from meta** (matches init[field] only 8/16, got[field] 1/16) — grader must compare it verbatim, never re-derive.
8. Non-anomalies worth asserting as invariants: zero duplicate (cell,pid,turn) among graded; zero empty/missing `raw`; `ok == (got==want)` universally; `finish=='stop'` on every graded/ack/filler record including every final graded turn per pid (r9 claim confirmed for R9 and also holds in R8); ack turns are exact disjoint complements of their graded family within 1..10.

Script exit code 0; anomaly count printed by the script: 2 (items covering anomaly 1 above, per file).

## Reproduce

```
python3 /tmp/kengaku-r10/schema_probe.py
# exit=0; identical output under PYTHONHASHSEED=1 / 99 / unset (diff-verified)
```
