ATTACKS: the `bodies=1,2,2,3` counts in corpus/evidence/round25-calibration/attrib-calibration-summary.txt — is the class column 1:1 with distinct prompt bodies?

Repro (pristine tip copy, /tmp/k25w2-KengakuR25.ScoutBodies, git archive 8ea41f9ed):
`python3 plans/attrib_calibration.py --root . --summary` → lines 3/13/25/38 print bodies=1 (r21-impl-ds), 2 (r21-impl-glm), 2 (r22-opencode), 3 (r23-stream); exit=0.
Mechanism: `bodies = len({r[1] for r in scored})` — the distinct **class-column strings**, not body bytes (plans/attrib_calibration.py:435).

Observed: class labels ARE 1:1 with distinct request-payload bytes in all four authoritative blocks.
- r21-impl-ds 20× `std` body_len 221; r21-impl-glm 20× `std` 215 + 2× `err` 233; r22 10× `force-hyper` 227 + 10× `force-opencode-go` 216; r23 24× `stream-inspection` 269 + 3× `stream-hint` 221 + 3× `stream-marker` 258 (`record` lines, each file).
- Reconstructed independently from plans/attrib_probe.py:41-139 + frozen budgets (r21 standard 20 / error ds 0, glm 2; r22 10/10; r23 24/3/3): counts match 1/2/2/3 exactly.

Break 1 — classes are NOT 1:1 with **prompts**, only with payloads. r21-impl-glm's `err` body is `std_body + temperature:0`: `std_body(m)["messages"] == err_body(m)["messages"]` is True; only key `temperature` differs. So that block is repeated sends of ONE prompt (COUNT_PROMPT) under two payloads; `bodies=2` overstates prompt clusters (true m=1). The lane's own frozen table says it: "standard_body + temperature:0" (plans/attrib-r21-frozen.md:47). Wording contested: knowledge says "1–3 prompt bodies" (corpus/knowledge/attribution-interval-calibration.md:79-80), claims §8 says the same (plans/round-25-claims.md:140). Conclusion unaffected and in fact strengthened (m=1 is still ≤3, still iid-fragile).

Break 2 — the count is unverified against the data it claims to count. It reads only the presentation class column; the per-trial `record` lines (same files, carrying authoritative `class` + `body_len`) are never compared. Counterexamples in scratch copies (lane files untouched):
- mutA2 (attrib-r21-impl-ds-trials.log only): class cells `std`→`body01..body20`, T ids preserved, no other byte class-relevant → `bodies=20`, `iid-fragile` **disappears**, `mismatches=0`, exit=0; the 20 records still say `std`/221.
- mutB (attrib-r21-impl-glm-trials.log only): 2 `err` rows → `std` → `bodies=1`, `mismatches=0`, exit=0; records still hold 2 `err`/233.
So a mislabeled class column passes every stored-line check; `bodies` is a claim about receipt text, not a derivation from trial payloads.

Break 3 (adjacent, frozen-table documentation): plans/attrib-r21-frozen.md:46 labels `standard_body` "233 bytes with glm-5.3-flash per probe-r19-P4-glm.log", but 233 bytes is exactly the P4 shape **with** temperature:0 (corpus/evidence/probe-r19-P4-glm.log:29) = `err_body`; the instrument's actual `std_body` is 215 bytes and matches the table's own keys_order (no temperature). The byte note belongs to the err body.

Scope gap (not a wrong number): `bodies=`/`iid-fragile` is attached only to the block `accuracy` estimate (plans/attrib_calibration.py:435-437,625-627); per-leg recall/specificity PASS lines in the same summary (r21-impl-ds recall:alibaba 20/20, specificity:hyper 20/20; r23 recall:hyper 24/24) and the pooled `sensitivity:` line carry no cluster count although they are trial-level over ≤3 bodies.

What survives: the four printed values are exact distinct-payload counts at the committed receipts; `iid-fragile` is correct on every PASSing accuracy line whether clustered by payload (2) or prompt (1); no stored verdict moves. What breaks: "1:1 with prompt bodies" (r21-impl-glm = 1 prompt / 2 payloads) and the implicit claim that the count is data-derived/unfalsifiable-by-relabel (mutation shows it is not checked against the record lines).

Installs: none (python3.14 stdlib only).

VERDICT: PARTIAL — values reproduce as distinct-payload counts (1/2/2/3) but are label-derived and not 1:1 with prompts (r21-impl-glm has 1 prompt across 2 payloads); the iid-fragile conclusion survives.
