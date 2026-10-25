# Round-8 horizon probe — pre-registered falsification (CriticR8)

Offline. Inputs: `corpus/evidence/round8-horizon/{horizon.py,critic-defects.md,results.jsonl}`, `/tmp/bench-r8/run.log`. All numbers below come from `/tmp/kengaku-r9/analyze.py` (run: `python3 /tmp/kengaku-r9/analyze.py`), which re-derives truth from `meta` with a byte-exact replica of the generator (matched all 10 problems) and recomputes B/C grading from logged fields. Line refs `h.py:` = horizon.py.

## 1. Fix-landing audit (16 defects)

| # | Verdict | Evidence |
|---|---------|----------|
| 1 checkpoint-INC | **partial** | Implemented (h.py:126-162, ckpts {4,7,10}, acks h.py:153). BUT the initial ask demands full state for CKPT too (h.py:129-131), turn 1 is logged as ack (h.py:137), and all 10 CKPT turn-1 replies are full states (36–52 ctok) — a full state sits in CKPT context for the whole episode. Latent gaps capped at ≤3 ops; "no self-copy scaffold" is overstated. |
| 2 single-digit deltas | **partial** | ADD 1–9, SUB 1–min(9,val) (h.py:81-85), NEW 2–9. Not clamped: SET 0–30 (h.py:79-80), init 3–30 (h.py:74), and MOV sums move whole (2-digit) counts (h.py:88-89). Promised 10-probe arithmetic covariate never run (no such cell in results.jsonl). |
| 3 edge cases | **landed** | RULES pins MOV-to-0, DEL removes, operands exist (h.py:108-116); generator: SUB only from >0 (h.py:84-85), MOV from ≠0 & distinct keys (h.py:87-91), NEW from disjoint `extra` pool (h.py:75, 97-99), DEL floor 4 keys (h.py:93-94) ⇒ no negatives, no DEL-then-NEW, no MOV a a. |
| 4 dual grading | **partial** | `nwrong` logged per graded turn (h.py:142-144); onset computed both protocols (h.py:134,140). No recovery-rate stat computed (recoverable: pid 2 INC wrong t1-6 → right t7-10); no pre-registration file exists in the round8 dir; INC-internal-curve caveat nowhere stated. |
| 5 output schema | **landed** | RULES: "all keys currently present (including zeros), integer values, any order" (h.py:116); grader parses to dict (h.py:119-123). |
| 6 corrupted key exercised | **not landed** | Intent present (h.py:185) but the fallback `rng.choice(list(state_mid))` (h.py:187) fired on pid 1: tail_touched={gaskets,rivets} are NEW-in-tail keys absent from state_mid ⇒ cand empty ⇒ corrupted `nails` (untouched by ops 8–10, `tailTouched=False` verified from meta). 1/8 corrupt pids has the exact structural hole defect #6 banned. |
| 7 hint×clean 2×2 | **landed** | All 4 cells, 8 pids each (h.py:204-209, 315-318; SUMMARY). |
| 8 historical value + 3-way | **partial** | 3-way coding landed and verified (h.py:214-216; my recompute matches all 16 corrupt outcomes). Historical-value loop (h.py:189-193) fired on 6/8 pids; the +5 fallback (h.py:194-195) fired on pids 1, 2 (from = true+5). Drift unstratified: 5–23. |
| 9 C ordering rule | **landed** | ORDER_NOTE in the rule ask (h.py:243-244, 254), absent from norule ask (h.py:258-260) as intended; conflict/benign asks byte-identical. All 4 conflict replies = [3], the unique minimal set (my recompute: minimal_sz=1, keep {1,2}). |
| 10 last-fence parser | **landed** | Last fenced block preferred (h.py:39-41), reversed-candidate fallback (h.py:42-47), json.loads only; got=null marks parse-fail; C logs explicit `parse` (h.py:265-266). Sensitivity run moot: 0/268 parse failures. |
| 11 ASCII C symbols | **landed** | A–D rows as lists (h.py:233-234). |
| 12 C-norule baseline | **landed** | C-norule (benign rows, no rule, h.py:258-262, 320-321) + C-MONO (h.py:291-299): benign 1/4 vs norule 4/4 vs MONO 4/4 separates rule-integration from transcript shape. |
| 13 pinned system prompt | **landed** | One SYSTEM, mandates the fenced block, ok-exception (h.py:18-19, 23); applied to every call in all cells. |
| 14 seeds>reps + fillers | **partial** | 10/8/4 seeds × n=1 (h.py:304) replaces 4×2 but is below the 12–16 ask; zero fillers; plan puts each pid's INC→MONO→CKPT back-to-back (h.py:314) and each pid's 4 B cells / 4 C cells adjacent (h.py:315-321) — maximal same-problem burst adjacency, the opposite of decorrelation. |
| 15 fixed op histogram | **not landed** | `gen_problem` free-samples with static weights (h.py:77-99); retry only enforces DEL+MOV+≥2 tail keys (h.py:101-103). Realized per-pid counts: SET 0–4, ADD 1–4, SUB 0–4, NEW 0–3 (my replica; retries depth 1 on pids 1, 2, 10). No op type is constant across problems. |
| 16 max_tokens/finish | **landed** | 8192 (h.py:14), finish logged on every record. Moot in effect: 258/258 finish-bearing records are stop (10 meta records carry no finish field), zero length-truncations. |

Docstring honesty (h.py:2-6): lists 12 fixes; does not claim a fixed histogram, fillers, or per-key grading — so the false advert is none; #15 is an unclaimed miss.

## 2. Artifact hunt — SUMMARY numbers vs harness

- **(a) Ack leaks → CKPT≈INC contamination: confirmed but one-sided.** 70 acks: 54 literal "ok" (2 ctok), 6× "ok\n```" (pid 4, 4 ctok — stray fence), and **10 full-state JSONs (36–52 ctok), all turn 1**, where the harness asked for full state (h.py:129-131) but logged an ungraded ack (h.py:137,148-152). Net effect: CKPT is *partially* scaffolded, biasing **against** the scaffold account (makes the CKPT collapse conservative), and turn 1 is excluded from CKPT's onset/acc. Ack-leak audit is possible only within the 80-char truncation (h.py:149); all 10 leaks fit.
- **(b) Final comparability: confirmed comparable.** CKPT graded exactly {4,7,10} × 10 pids (verified from records); `ckpt_oks[-1]` is turn 10 dict-exact vs truth[-1], identical criterion to INC turn 10. Caveat: CKPT's *onset/acc* are 3-point vs INC's 10-point — not comparable, and CKPT turn-1 (asked, ungraded) is invisible to both.
- **(c) Off-by-one: none.** Recomputed `truth[i]` for all 172 graded want-fields (A-INC 100, A-CKPT 30, A-MONO 10, B 32): **0 mismatches**. `run_inc` uses truth[i] at turn i+1 (h.py:139-140), correct. B's sim_corrupt is simulated from the corrupted mid state (h.py:197,214) — my recompute reproduces all logged outcomes.
- **(d) B transcript integrity: consistent.** Body = true states for ops 1–6 (h.py:202) + corrupted state labeled "After operation 7" (h.py:203) — the only detectable inconsistency is the op-7 value, and detection requires re-applying ops 1–7. States are sim_apply outputs, so they obey RULES (MOV leaves source at 0, DEL removes). Two holes: pid 1's corruption is undetectable via tail ops (see #6), and pids 1–2's corruption is a +5 fallback, not a historical value.
- **(e) `grade_state` extra keys (h.py:119-123): correct per RULES.** Union-of-keys diff counts hallucinated keys as wrong; RULES mandates emitting exactly the present keys (h.py:116). Latent lenience: dict equality coerces 5.0==5, so float values would pass the "integer values" rule — 0 non-integer floats in the corpus, so moot.
- **(f) `minimal_sz` semantics (h.py:284-287): correct.** sz=0 yields the empty combination = keep all 3 rows, i.e. minimal_sz is the minimum number of declared violations such that kept rows are column-conflict-free. Recompute: conflict minimal_sz=1 (unique set {3}); benign minimal_sz=0. `over_repair` correctly flags benign rep0 ([3] where 0 needed) and reps 1–3 ([2,3]). Note `over_repair` is **not** part of `ok` (h.py:288) — shipped C-benign 1/4 contains an over-repair "pass"; strict violations==[] is **0/4** (benign) vs 4/4 (conflict, one distinct output).
- **(g) `extract_json_block` fallback (h.py:42-47): acceptable, unexercised.** Handles 1 level of brace/bracket nesting; a C reply whose outer braces fail would fall through to individual row arrays, reversed order returns the last row (a list) → parse-fail, not silent misgrade. 0/268 records used the fallback.
- **Harness-side items not on the list:** (h) **burst coupling is the biggest artifact**: per pid, INC's final draw and MONO's single draw are 1 request apart on the *same problem* (run.log jobs 1–30; h.py:314), B's 4 conditions and C's 4 cells are adjacent blocks — with r7's lag-1 +0.26/+0.32 and 5–10-request horizon, cross-cell contrasts are correlated draws; (i) **seed-difficulty confound in B**: the 2 clean-plain failures are pids 4 and 8, and pid 8 fails all four B cells — failure tracks seed, not corruption; (j) corruption drawn with `Random(pid*31)` (h.py:186) — deterministic, same field in plain/hint (good for pairing); (k) temp 0.2 ≠ replay-identical, so within-cell reps are weak replications.

## 3. Claim triage

| Claim | Verdict | Reason |
|---|---|---|
| (i) INC advantage = scaffold assist, not horizon | **survives** | CKPT collapses 9/10→3/10→1/10 across ckpts 4/7/10 (INC 9/7/7) with ≤3-op latent gaps; paired@t10 INC>MONO 7:0, INC>CKPT 7:1. Caveats: turn-1 state anchor leaks into CKPT, and 7:0 is not ESS-significant (below). |
| (ii) hint does not help recovery | **bends** | Paired discordance 1:1 on corrupt (3/8 vs 3/8), 6/8 vs 6/8 clean; mirror flips (pid 4 vs pid 7) show seed-noise dominance — consistent with zero, but n=8/ESS≈4.3 cannot certify absence. |
| (iii) cannot integrate vacuous rule, applies binding one | **survives** | Direction holds twice (conflict 4/4 and norule 4/4 vs benign **0/4** strict — shipped 1/4 includes an over-repair). Effective n≈1–2 distinct outputs per C cell caps confidence; rep0's valid square leaves a patch-then-misreport alternative. |
| (iv) MONO 0/10 = hard 10-op latent ceiling | **bends** | Real (all finish=stop, so not truncation), but nwrong = [1,3,3,1,2,2,2,3,1,3]: 3/10 are single-key misses — graded decline, not a cliff; INC's own late onsets (7,6,9) and CKPT's collapse show the boundary is scaffold-dependent, not a fixed 10-op wall. |
| (v) 3/8 vs 6/8 shows propagation | **blocks** | Only 1/8 corrupt-plain trials propagated (pid 1 — the pid whose corrupted key was never tail-touched, weakest case); 4/8 failures are outcome=other, 2 of them healing the corrupted key and missing want by 1–2 keys; clean failures are the same hard seeds (4, 8); paired corruption effect 3:0, iid p=0.25. The delta is seed difficulty + generic arithmetic slip, not propagation. |

## 4. Cheapest decisive follow-ups (ranked by info/API-call)

ESS model: r7 lag-1 ρ≈0.3 ⇒ ESS≈0.54·n. Sign test α=0.05: unanimous needs ESS≥5.32 ⇒ **n≥10** pairs; one discordance p=2(k+1)2⁻ᵏ≤0.05 ⇒ **n≥17**.

1. **Replication cross-check — 0 new calls** (labrat's 8 pids × {INC, CKPT4710, CKPT710, MONO} already running; fresh seeds). Pre-registered falsifier for (i): **CKPT710 or CKPT4710 final-ok ≥5/8 while MONO ≤2/8 ⇒ (i) blocks** (scaffold removal didn't collapse the advantage ⇒ INC−MONO is protocol/horizon, not scaffold). CKPT ≤2/8 with INC ≥5/8 ⇒ (i) survives replication. Secondary: CKPT710<CKPT4710 gradient ⇒ forced-maintenance length matters (partial rescue of a horizon story). Power: 8 pairs, ESS≈4.3, 8:0 ⇒ p≈0.05–0.10 — treat as decisive description, not confirmatory.
2. **Arithmetic covariate — 10 calls** (defect #2's unpaid debt): 10 fresh single-op probes (ADD/SUB delta 1–9; include 2 two-digit MOV-sum ops), same SYSTEM/temp, n=1. 10/10 ⇒ arithmetic intact ⇒ (iv) is chaining, strengthens; ≤3/10 ⇒ MONO failures are quant-arithmetic artifacts, (iv) bends further; 4–9/10 ambiguous ⇒ rerun at 25 probes before interpreting MONO.
3. **B mechanism, holes closed — 24 calls**: 12 fresh seeds, corrupt-plain + clean-plain paired, corruption forced to a tail-touched key with a true historical value (delete fallbacks h.py:187,194-195), drift stratum 5–9. Decision rule on paired corrected-rate: unanimous direction at n=12 decides (v)'s mechanism; expect corrupt≈clean (propagation dead) or corrupt<<clean with >50% propagated outcomes ((v) revives). If 1 discordance, extend to 17.

## Confidence

- Audit verdicts (#1–16): **high** — code lines cited; generator replica matched all 10 problems incl. retry depths (pids 1,2,10 = 1 retry).
- (a) turn-1 leak, (b) comparability, (c) zero off-by-one, (d) transcript consistency, (f) minimal_sz: **high** — direct record recompute.
- (e) extra-keys grading, (g) parser: **high** on code semantics; **medium** on behavior (0 floats, 0 fallback uses — path unexercised in r8).
- Claim (i): **medium** — direction replicated in-corpus (CKPT 1/10), but CKPT control leaks a turn-1 anchor and 7:0 fails ESS-discounted α=0.05; replication is the decider.
- Claims (ii),(iv): **medium** — nulls/near-nulls at ESS≈4–5.
- Claim (iii): **medium** — direction robust across two contrasts, effective n≈1–2 outputs.
- Claim (v) blocks: **high** — 1/16 propagated outcomes is a direct count, mechanism term mislabeled regardless of power.
- Follow-up sample-size math: **medium** — inherits r7's ρ≈0.3 ESS model; if true ρ is lower, required n drops toward 6–8.
