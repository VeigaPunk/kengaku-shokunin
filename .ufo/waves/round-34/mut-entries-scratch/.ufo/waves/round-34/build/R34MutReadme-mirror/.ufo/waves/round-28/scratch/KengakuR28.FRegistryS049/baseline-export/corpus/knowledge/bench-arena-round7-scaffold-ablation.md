# bench-arena round-7 — scaffold-delta ablation

Fourth executed eval by this domain (2026-09-28). Closed the round-6 open
gap: the 5 scaffold-determined flips showed *which* harness won, not *why*.
Method: capture the verbatim opencode `raw` wire request once, then replay
it component-by-component via direct API.

## Capturing the verbatim scaffold request

Temporary `cap34113` provider in `~/.config/opencode/opencode.json` →
logging proxy `127.0.0.1:18099` → upstream `127.0.0.1:34113`; ran
`opencode run --agent raw` on task 08. Config restored byte-identical after
capture. Captured request: `/tmp/bench-r7/capture/001-*-req.json` (ephemeral).

### What opencode actually sends (raw agent, no tools enabled)

| Component | v2 opencode raw | r5/r6/r7 direct API |
|---|---|---|
| system msg | agent prompt ("You are a raw code generator…", ~150 chars) + powered-by line + `<env>` block + `<available_skills>` catalog — **94% of the ~12K chars is the skills catalog** (18 skills) | none |
| `tools`/`tool_choice` | `[janitor_auth, skill]` + `auto` — despite `tools:{...:false}` in agent config, these two slip through; chat template injects the `<tool_call>` format block (~400 tok) | none |
| temperature | absent → llama-server default **0.8** | 0.2 |
| max_tokens | 32000 | 4096 |
| stream | true | false |
| user msg | `prompt.md` verbatim | `prompt.md` verbatim |
| thinking | `qwen-coder-godspeed.jinja` has **no think branch** — `enable_thinking` flag is a no-op on this endpoint | same |

Prompt sizes: full scaffold ≈ +4.7K tok (E1 4,831–5,184 vs E0 116–469);
system alone ≈ +4.3K tok (E3−E0 = 4,331–4,333; tools+format block =
E1−E3 = 382). v2 sessions logged input+cache_read = 4,309–4,674 across
all 33 `qwenlocal-v2-*` sessions (opencode.db message/part tables,
measured 2026-09-28).

## Ablation matrix and result

Tasks: all 5 scaffold-determined flips. E0=API baseline (anchor n=1);
E1=verbatim scaffold replay; E2=E1−system; E3=E1−tools; E4=E1+temp 0.2;
n=3 each. **E5** (added post-critic): bare API at temp 0.8, n=3 on
03/08/13 — fills the {no-system × high-temp} cell missing from E0–E4.
Graded by repo `grade.sh` (`BENCH_ROOT=/tmp/bench-r7`).

| Task | v2 | API r6 | E0 | E1 replay | E2 −sys | E3 −tools | E4 +t0.2 |
|---|---|---|---|---|---|---|---|
| 03-extract-isodatetimes | P | FFF | F | H F F | HHH | FFF | FFF |
| 08-sql-group-window | F | PPP | P | PPP | HHH | PPP | PFF |
| 12-knapsack-reconstruct | F | PPP | F | PPP | FHH | PPF | PPP |
| 13-stack-min | P | FFF | F | PPP | HHH | PPP | PPP |
| 31-mutable-default-arg | F | PPP | P | FFP | HHH | FFF | FPP |

(`H` = HARNESS_DEFECT: no closed fence. **E5** bare-API@0.8 post-critic
cell: 03=FFF, 08=PPP, 13=PFF — see verdict item 3; 12/31 not run.)

## Verdict — decomposition of the "scaffold-determined" class

1. **Tools-without-system is fatal** (E2): 14/15 cells ended
   `finish=tool_calls`, 13/15 with empty `content` (one —
   12-knapsack E2-r2 — emitted 368 B of unfenced prose alongside the
   call); graded HARNESS_DEFECT 14/15. Directly observed call:
   `skill(name="min_stack")` on a repeat probe; r7 `run.py` persisted
   only `content`, so per-cell call names are inferred from
   `finish_reason` — labrat's temp-0.2 repro (`/tmp/bench-r7-l2-labrat/`)
   confirms the mechanism on all 3 probed tasks: 9/9 `tool_calls`
   invoking `skill(name=<task-shaped-name>)` — and shows the trap is
   **temperature-invariant** (9/9 at temp 0.2 vs 14/15 at 0.8).
   opencode's scaffolding *exists in practice*; raw `tools` + no
   instructing system prompt = harness defect, not a capability signal.
   **Never send `tools` + `tool_choice:auto` without a system prompt
   that pins the output contract.**

2. **System prompt drives strategy selection** (13-stack-min): bare-API
   emits the sorted-stack MinStack (index-0 anchor → ghost/lost minima —
   IndexError on the fixed scenario, `test_rc=1`) in E0, all 3 r6 reps,
   AND r5 — **byte-identical sha `d268ef61…` across all 5 bare-API
   draws**. Every scaffolded run (v2 + E1/E3/E4 = 10 code sols) emits a
   correct family (9/10 min-at-top monotone — E1-r2 **byte-identical to
   v2's sol**; 1 paired-mirror variant). Hypergeometric: P(all 5
   sorted-stack draws land bare-API by chance) = 1/C(15,5) ≈ 0.0003.
   Scaffold contains ZERO stack/algorithm/O(1) tokens (grep audit) →
   non-semantic context mass shifts the family, not steering. The test
   catches the *correctness* bug (`get_min()==min(remaining)` asserted
   after every op, ~20 ms), not the O(n) pop itself.
   **Residual**: persona-line vs skills-mass vs sheer length not
   isolated — a length-matched empty/padded system is the next ablation.

3. **Temperature matters — but only on bare prompts** (E5 fills the
   critic-flagged missing cell): bare-API at temp 0.8 on 13 → P F F
   (r1 emitted a *different* correct min-at-top variant `3d1d8578`;
   r2/r3 byte-identical to the `d268ef61` sorted-stack FAIL). The family
   choice gets TWO pushes — scaffold presence (reliable: 10/10 code sols
   correct-family across E1/E3/E4) and decode temperature on the bare
   prompt (partial: 1/3 escapes at 0.8, 0/5 at 0.2). E4's two 08-FAILs
   at temp 0.2 likewise show temp moves *boundary* tasks under scaffold
   without reversing the strategy-determined one. Full factorial on 13:
   bare@0.2 = sorted 5/5; bare@0.8 = sorted 2/3 + canonical 1/3;
   scaffold@0.8 = canonical 6/6; scaffold@0.2 = canonical 3/3.
   `enable_thinking` remains confirmed inert (template has no think
   branch) — prior "thinking off" claims need the caveat.

4. **Three "scaffold" flips were actually sampling noise / boundary:**
   - **03** — v2's lone PASS was a lucky draw; scaffold replay cannot
     recover it (0/9 across E1/E3/E4, 1 fence-loss H). Reclassify:
     noise-tilted-FAIL, not scaffold-determined.
   - **08** — v2's FAIL was a subtly-wrong SQL variant (global average in
     `HAVING` instead of per-region); all scaffolded reps PASS except 2
     noise F at temp 0.2 (E4). Reclassify: noise, wide-shallow SQL space.
   - **31** — mixed under every scaffolded condition (FFP / FFF / FPP);
     borderline predict-output task. Reclassify: sampling noise.
   - **12** — mostly noise (E3-r3 and E0 once FAIL); weak scaffold pull
     toward PASS.
   - **Net reclassification of the r6 flip set (8 tasks): 1 true
     scaffold-determination (13), 1 strategy-bound (06), 6
     noise/boundary (03, 08, 09, 12, 20, 31).** Of the 5 labeled
     scaffold-determined in r6, only 13 survives ablation.

## Prediction-calibration delta

- Predicted "decoding (temp) dominant" — **wrong**: temp changed almost
  nothing under scaffold; system presence was the real lever (E3≈E1≈E4 ≫
  E2). Correctly anticipated the alternative on prompt semantics but
  mis-weighted which variable mattered.
- The second-order lesson stands: at temp 0.8 `tool_choice:auto` +
  injected tool-format text is a *behavioral attractor* — the model grabs
  the offered affordance. Output-contract system text isn't decoration;
  it's the only thing keeping fenced answers fenced.

## Reproduce

```
# /tmp/bench-r7/{run.py,proxy.py,predictions.md,sysmsg-v2.txt,capture/,
#   out/,graded/,report-kq-r7-*.v2.csv,telemetry-kq-r7.csv}
BENCH_ROOT=/tmp/bench-r7 bash ~/bench-arena/grade.sh kq-r7-E{0..4}[-r{1..3}]
```

Config touched: `~/.config/opencode/opencode.json` — `cap34113` provider
added for capture, then file restored byte-identical
(`/tmp/bench-r7/opencode.json.bak`).
