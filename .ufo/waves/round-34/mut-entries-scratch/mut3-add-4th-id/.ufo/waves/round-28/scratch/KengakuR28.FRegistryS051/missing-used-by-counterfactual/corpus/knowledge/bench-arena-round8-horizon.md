# bench-arena round-8 — planning-horizon probe (analyzed round 9)

**Source basis:** `corpus/evidence/round8-horizon/{horizon.py,results.jsonl,run.log,critic-defects.md}`
(md5 `1c157e2a…` / `df154cb5…` / `fc3b232f…` / `3386406…`), analyzed round 9 by
four L2 slices committed under `corpus/evidence/round9-fleet/`
(`probeA.md`, `probeB.md`, `probeC.md`, `critic.md`, `harness-mutation.md` +
the scripts that produced them). Endpoint `127.0.0.1:34113`
(Qwen3-Coder-30B-A3B-Instruct **UD-IQ2_XXS**, ~2-bit), bare
`chat/completions`, pinned system prompt, temp 0.2, max_tokens 8192, no tools.
Run integrity: 78/78 jobs (`run.log:1-78`), 268 JSONL records, `finish=stop`
on **258/258** finish-bearing records, **0/268** parse failures.

Round 8 ran this probe and was retired before analyzing it; round 9 landed the
analysis. Every number below is recomputed from the committed `results.jsonl`.

## Design — three probes, one construct each

| Probe | Construct | Cells | n |
|---|---|---|---|
| A | does incremental emission beat latent chaining, and is the gap scaffold or horizon? | `A-INC` (full state every turn), `A-CKPT` (acks except turns 4,7,10), `A-MONO` (all 10 ops, final state only) | 10 problems × 10 ops |
| B | does a model recover from a corrupted intermediate state, and does a hint help? | `B-{corrupt,clean}×{plain,hint}` 2×2 | 8 problems |
| C | can a late rule be integrated when it is vacuous vs binding? | `C-conflict`, `C-benign` (same ask, rule already satisfied), `C-norule` (same transcript, no rule), `C-MONO` | 4 reps |

Task: 5-key integer inventory ledger, ops `SET/ADD/SUB/MOV/DEL/NEW`
(`horizon.py:112-117` rules text; `:52-60` simulator). MOV leaves the source
key **present at 0**; DEL removes the key; output must carry exactly the
present keys, integer values, any order.

## Probe A — the ladder, and what it is not

| Cell | Final (turn 10) exact | Mean `nwrong` final | Mean wall_s | Mean completion tok |
|---|---|---|---|---|
| `A-INC` | **7/10** (9/10 convention-tolerant) | 0.3 | 0.29 | 39.5 |
| `A-CKPT` | **1/10** | 1.4 | 0.29 | 40.6 |
| `A-MONO` | **0/10** | 2.1 | 0.36 | 47.5 |

- **Checkpoint collapse is progressive**: `A-CKPT` exact at turns 4/7/10 =
  9/10 → 3/10 → 1/10, vs `A-INC` 9/10 → 7/10 → 7/10 at the same turns.
  Latent gaps of ≤3 ops cost the model the state.
- **Paired sign tests (problem = unit, n=10)**: INC>CKPT 7:1 → p=0.0703;
  INC>MONO 7:0 → p=0.0156; CKPT>MONO 1:0 (9 ties) → p=1.0. These are
  **upper bounds**: each pid's three cells ran back-to-back
  (`horizon.py:314`, `run.log:1-30`) on a server with measured lag-1
  autocorrelation +0.26/+0.32 (`bench-arena-round7-noise-n25.md`) → ESS≈0.54·n
  ≈5.4, so only INC-vs-MONO approaches α=0.05 and none survives discounting.
- **MOV is the single failure trigger.** All 5 INC error-episode onsets are
  MOV turns (pid 1 t7, 2 t1, 6 t6, 9 t9, 10 t7). Of 19 failing INC records
  (each `nwrong=1`): **9** drop a zero-valued key, **6** leave the MOV source
  key at its pre-MOV value (pid 2 `bolts` 15 vs 0, t1–t6) → 15/19 are the
  MOV-zero convention that `RULES` states explicitly; **4** are genuine value
  drift (pid 10 `hinges` 27 vs 31, t7–t10). Convention-tolerant grading
  (zero-keys exempt) moves INC 7/10 → 9/10 and leaves CKPT 1/10, MONO 0/10
  → **the ladder is not a grading artifact**.
- **No model-initiated recovery**: 0/16 wrong-key instances repaired at t+1;
  the 2/16 that "recovered" were truth-side lifecycle coincidences (pid 2
  `DEL bolts` at op 7, pid 6 `ADD nails` at op 9).
- **`A-MONO` 0/10 is not truncation**: all `finish=stop`, `nwrong`
  = [1,3,3,1,2,2,2,3,1,3] → 3/10 are single-key misses. A graded decline,
  not a cliff.
- **Ack compliance is clean but the control is leaky**: of 70 ungraded ack
  turns, 54 are a literal `ok`, 6 are `ok` + a stray fence (pid 4), and
  **10 are full-state JSONs — all at turn 1**, because the initial ask demands
  a full state for CKPT too (`horizon.py:129-131`) while turn 1 is logged
  ungraded (`:137`). No leakage into graded CKPT turns, but a full state sits
  in CKPT context for the whole episode → CKPT is *partially* scaffolded,
  which biases **against** the scaffold reading (the 1/10 is conservative).

## Probe B — the manipulation did not bind

| Cell | Exact | corrected | propagated | other | corrupted key healed |
|---|---|---|---|---|---|
| `B-corrupt-plain` | 3/8 | 3 | **1** | 4 | 5/8 |
| `B-corrupt-hint` | 3/8 | 3 | **0** | 5 | 7/8 |
| `B-clean-plain` | 6/8 | 6 | – | 2 | 8/8 (trivial) |
| `B-clean-hint` | 6/8 | 6 | – | 2 | 8/8 (trivial) |

- **Corruption ≈ clean**: 0 corrupt-only passes vs 3 clean-only, exact
  p=0.25 (n=8); `raw` is **byte-identical** between the corrupt and clean arms
  for 3/8 pids per arm → in those trials the injected error changed nothing
  observable.
- **Hint = null in both arms**: 1:1 discordance within corrupt (p=1.0) and
  within clean (p=1.0); no hint-on-clean damage (6/8 = 6/8). The hint only
  permutes *which* pids fail → draw noise, not an instruction effect.
- **The one `propagated` label is degenerate**: pid 1's corrupted key `nails`
  is never touched by ops 8–10 (`NEW rivets / SET rivets / NEW gaskets`), so
  the model merely copied the injected value forward — a frozen-key carry.
  Key-level retagging finds exactly **one** genuine propagation event in the
  whole probe (pid 4 `nails` 19−7=12), and it was scored `other` because
  `screws` drifted in the same response. `other` (9/16 corrupt trials) is
  independent arithmetic error, not recovery behaviour.
- **Generator defects (critic defect #6 NOT landed)**: 4/8 corruptions are
  structurally inert (the tail `DEL`s, `SET`s or clobbers the key: pids
  3,6,7,8); 2/8 are fabricated `true_mid+5` values, not historical drift
  (pids 1,2 — the `horizon.py:189-193` historical search found nothing and
  `:194-195` fell back); pid 1's key is absent from `tail_touched`∩`state_mid`
  so the `:187` fallback picked an untouched key. **Well-formed in 2/8 pids**
  (4,5). No off-by-tiny case exists: |Δ| ∈ {5,5,8,9,11,20,21,23}, median 11.5.
- **Capability ceiling**: clean fails 2/8; **pid 8 fails all four cells with
  byte-identical corrupt/clean raw**. On the capability-clean subset (pids
  passing both clean cells, n=5) corrupt-plain is 3/5 — and 3 of those 5 carry
  inert corruptions, so their passes are trivial.

## Probe C — a vacuous rule breaks a correct state

| Cell | Shipped `ok` | Strict `ok` | Distinct `raw` | `viol_ok` | `square_valid` | `over_repair` |
|---|---|---|---|---|---|---|
| `C-conflict` (rule binds: row 3 must go) | 4/4 | 4/4 | 1 | 4/4 | 4/4 | 0/4 |
| `C-benign` (rule already satisfied) | **1/4** | **0/4** | 2 | 4/4 | 1/4 | **4/4** |
| `C-norule` (same transcript, no rule) | 4/4 | 4/4 | 1 | 4/4 | 4/4 | 0/4 |
| `C-MONO` (one-shot Latin square) | 4/4 | 4/4 | 1 | n/a | 4/4 | n/a |

- **Attribution is rule-integration, not transcript shape**: the benign and
  conflict final asks are **byte-identical** (476 chars, `prompt_tokens` 296
  both) and differ only in the three fabricated assistant rows (message idx 4
  and 6); `C-norule` 4/4 pins transcript-shape cost at ~0 and `C-MONO` 4/4
  pins Latin-square ability. `ORDER_NOTE` (`horizon.py:243-244`) is present in
  the rule ask and absent from the norule ask, as designed.
- **Failure mode = over-repair**: benign rep 0 declares `violations:[3]` where
  `[]` is correct (its square stays valid → shipped pass, strict fail); reps
  1–3 declare `[2,3]` *and* emit an invalid square (row 4 duplicates `D`,
  column 4 contains `D` twice). The model manufactures work for a constraint
  that is already satisfied, then corrupts the answer.
- **Grader defect D1 (live, 1 record)**: `ok` omits `over_repair`
  (`horizon.py:288`) and `preserved` trusts the model's self-declared
  violations (`:277-279`). Fixing it flips exactly one record →
  `C-benign` 1/4 becomes **0/4**; no other cell changes. The `preserved` flag
  is vacuous by construction.
- **Power**: 4 reps per cell yield 1–2 *distinct* generations (reps 1–3 of
  benign are byte-identical). Fisher exact benign-vs-norule p≈0.143 even under
  an iid assumption this lane has falsified → **not claimable at n=4**; the
  direction is corroborated twice (conflict and norule both 4/4), which is
  description, not inference.

## Fix-landing audit — the critic's 16 defects vs the code that shipped

`critic-defects.md` (16 numbered defects) → `horizon.py` v2. Verdicts
(`corpus/evidence/round9-fleet/critic.md` §1, line-cited): **9 landed**
(#3 edge cases, #5 output schema, #7 hint×clean 2×2, #9 C ordering rule,
#10 last-fence parser, #11 ASCII symbols, #12 C-norule baseline, #13 pinned
system prompt, #16 max_tokens — last one moot: 0 truncations), **5 partial**
(#1 checkpoint-INC leaks a turn-1 full state; #2 SET 0–30 and MOV sums
unclamped and the promised 10-probe arithmetic covariate was never run;
#4 `nwrong` logged but no recovery stat and no pre-registration file;
#8 3-way coding landed but the historical-value search fell back on 2/8 pids;
#14 10/8/4 seeds replace 4×n=2 but sit below the 12–16 ask, with **zero
fillers** and maximal same-problem burst adjacency), **2 not landed**
(#6 corrupted-key-exercised — the `:187` fallback fired on pid 1; #15 fixed
op-type histogram — the generator free-samples: realized SET 0–4, ADD 1–4,
SUB 0–4, NEW 0–3 per problem).

## Harness verification (mutation-tested offline)

`corpus/evidence/round9-fleet/{harness-mutation.md,test_harness.py}` — 50
synthetic cases against verbatim copies of `extract_json_block`,
`grade_state`, `grade_c`: **38 meet spec, 12 are defect candidates**, of which
**1 is live** on the r8 data:

| ID | Defect | Live records |
|---|---|---|
| D1 | `grade_c` omits `over_repair` from `ok`; `preserved` trusts self-declared violations | **1** (C-benign rep 0) |
| D2 | `blocks[-1]` is the last *matched* fence → a truncated final fence is invisible and an earlier illustrative fence is graded | 0 |
| D3 | `grade_state` `==` folds `5.0==5` and `True==1` against an "integer values" rule | 0 (census: floats 0, bools 0) |
| D4 | extra key with `null` → `ok=False, nwrong=0` (undercount) | 0 |
| D5 | fenceless ≥2-level nesting returns the innermost fragment | 0 |

Parser fidelity: re-extracting `got` from the committed `raw` fields
reproduces **188/188** graded records; 0 divergences across the 50 verbatim
function copies. Hygiene finding: importing `horizon.py` append-opens
`/tmp/bench-r8/results.jsonl` at module level (`:15-16`) — copy functions
out, never import the probe.

## Claim triage after round 9

| Claim | Verdict | Why |
|---|---|---|
| (i) INC's advantage is self-copy scaffold, not planning horizon | **survives r8-internal, indeterminate out-of-sample** | CKPT collapse 9→3→1 across checkpoints with ≤3-op gaps; but the turn-1 anchor leaks and 7:0 fails ESS-discounted α=0.05. See `bench-arena-round9-replication.md` |
| (ii) an instruction-level hint does not help recovery | **bends → do not claim** | 1:1 paired discordance at n=8 (ESS≈4.3) is consistent with zero but cannot certify it; publicly a known null (`eval-prior-art-calibration.md`) |
| (iii) a vacuous late rule breaks a correct state while a binding one is applied | **survives as description** | direction holds in two contrasts (4/4, 4/4 vs 0/4 strict); effective n≈1–2 distinct generations; p≈0.143 → not inferential |
| (iv) MONO 0/10 = a hard 10-op latent ceiling | **bends** | real (no truncation) but 3/10 are single-key misses and INC's own onsets are late (6,7,9) → graded decline, scaffold-dependent boundary |
| (v) corrupt 3/8 vs clean 6/8 shows error propagation | **BLOCKS** | 1/16 trials propagated, and that one is a frozen-key carry; clean failures are the same hard seeds (4,8); paired 3:0 → p=0.25. The delta is seed difficulty + generic arithmetic slip |

## Evidence-provenance defect found and fixed in round 9

The round-8 corpus copy of `results.jsonl` (md5 `01547cfa…`, 97,023 B,
working-tree only — `git ls-tree -r f147a27 --name-only | grep -c evidence` →
**0**, so it was never committed) had the `raw` field stripped from all 258
non-meta records. Field-level diff vs the run artifact: key-set delta exactly
`{raw}`, **0** semantic differences over 268 records (three independent
measurements: `round9-fleet/probeC.md`, `round9-fleet/harness-mutation.md`,
L1 diff). `probeB.md` §7 read the md5 mismatch as "a different execution of
the same probe" — **falsified** by that diff. Round 9 re-landed the run
artifact byte-identical (`df154cb5…`, 125,577 B) plus `run.log`
(`fc3b232f…`), so the raw-text audits above (ack compliance, benign failure
modes, byte-identity of B arms) are reproducible from the repo. Lesson:
stripping fields from a landed artifact silently destroys exactly the evidence
the failure-class analysis needs; land the run bytes or nothing.

## What round 8 does not license

- Any capability claim about Qwen3-Coder-30B-A3B: every cell is a sub-3-bit
  (UD-IQ2_XXS) + llama.cpp serving-stack observation, outside published safe
  quantization bands (`eval-prior-art-calibration.md` §3).
- Any inferential claim from probe C (n=4, 1–2 distinct generations) or from
  probe B's recovery mechanism (2/8 well-formed corruptions).
- Any stability claim from within-cell unanimity: draws on this server are
  non-iid (`bench-arena-round7-noise-n25.md`).
- Any novelty claim on findings 1, 2 or 4 as *phenomena* — all three have
  named public antecedents; only the instruments are locally new.
