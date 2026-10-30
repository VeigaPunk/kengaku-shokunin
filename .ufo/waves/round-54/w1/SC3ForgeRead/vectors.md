# Round 54 attack-vector map — SC3ForgeRead

Axes: novelty and calibration. Mapping only; no fixes, fixtures, tests or scoring.

## Evidence and confidence

Read the frozen `plans/round-54-claims.md` and both requested round-53 reports in full; skimmed `C1CritNeverRead.md`. Round-53 outcomes below are **observations reported by those critics**, not fresh reproductions. R54 coverage is a **claimed design mapping** supplemented by literal source inspection; no R54 pass/fail outcome was measured by this seat.

`xd://lsp` returned “No such tool”; semantic navigation was unavailable. Grep/read are literal-source fallback, not semantic reference proof. No installed tools or scratch trees.

Source abbreviations, relative to the lane:
- O: `.ufo/waves/round-53/w3/C1CritOracle2.md`.
- P: `.ufo/waves/round-53/w3/C2CritPredicate2.md`.
- N: `.ufo/waves/round-53/w3/C1CritNeverRead.md`.
- A: `plans/round54_c1_anchor.py`.
- E: `plans/round54_c2_entrytruth.py`.
- C: `plans/round54_c2_controls.py`.

## Frozen coverage quotations

These are exact excerpts from `plans/round-54-claims.md`; quote IDs in every table row answer whether coverage is actually claimed.

- **Q1 / BINDING:** “the digest the proof timestamps equals the recomputed sha256 of the committed bytes” followed by `git -C SOURCE show <freeze-rev>:plans/round-54-claims.md`.
- **Q2 / ATTESTATION:** “the proof carries ≥1 `BitcoinBlockHeaderAttestation`; walking the proof's op tree from the file digest to the attested digest reproduces that digest”.
- **Q3 / EXTERNAL-PIN:** “are fresh fetches made **this round** from ≥2 independent public Bitcoin block sources” and “header `nTime` is strictly earlier than the after-run wall-clock time recorded in the landing receipt (the freeze pre-dates scoring).”
- **Q4 / CONTROLS-a–d:** “(a) forged proof (one flipped byte in the serialized op path), (b) wrong-bundle (real proof, different digest), (c) pending-only proof (built offline, no Bitcoin attestation), (d) absent proof. Any control that verifies is a predicate failure.”
- **Q5 / internal-only negative:** “the r53-style FREEZE leg alone (git pins only) accepts a re-pinned post-hoc bundle (the C1CritOracle2 route, reproduced in-repo as a documented negative, no external fetch), demonstrating the construct the anchor removes”.
- **Q6 / entry-mode argv:** “(no `--selftest`/`--help`/`--dry`/`--version` in the declared argv)”.
- **Q7 / REGISTRY:** “exactly one `## Gate/probe registry` heading, zero duplicate/malformed rows, every row names a `python3 <script>` entry (unchanged parsing contract).”
- **Q8 / LEDGER:** “carries exactly the registry rows; each declares `entry_argv` in entry mode whose script matches the registry row's script; red rows carry a reason ≥ 10 words and a verbatim evidence fragment.”
- **Q9 / EXEC and LAUNDERED branch:** “every row re-executed hermetically in the clean clone; `mismatched=0`, `timeout=0`, `evidence_missing=0`; `LAUNDERED` (declared green, observed nonzero) = 0.”
- **Q10 / hermetic env control:** “a fixture gate that changes behaviour when a caller-supplied `GIT_CONFIG_GLOBAL` sets `user.name` must report identical observed exits with and without the poison under the counter's env”.
- **Q11 / source control:** “Clean tree: `git status --porcelain` empty; source rev == lane tip.”
- **Q12 / frozen-artifact process constraint:** “No frozen prior artifact is modified” followed by the named r53 files, `SKILL.md` and the claims file, which “stay byte-identical through the round.”

## Numbered vector table

| # | Demonstrated attack and reported outcome | Exact R54 leg/control mapped | Coverage claimed? | Residual / scope |
|---|---|---|---|---|
| 1 | O §4.3: rewrite freeze+label history, swap classifier for source-hash lookup, flip ten paired Y labels to N and re-pin digests. Four r53 legs green; overall predicate failed on unrelated missing prior art. | **BINDING**, **ATTESTATION**, **EXTERNAL-PIN**; **CONTROLS-b** wrong bundle, **-c** pending-only, **-d** absent proof are related negatives. Internal-only negative explicitly repeats the old weakness. | Yes: Q1–Q5. | New external object is the r54 **claims bytes**, not the r53 classifier/labels. Changing those while retaining claims bytes is not covered by BINDING. G1. No claim that a real R54 anchor passed was measured here. |
| 2 | O §4.2: committed post-freeze label edit, restored-after-edit, merge-commit edit, classifier edit, and classifier edit plus freeze rehash; all rejected by r53 history/digest checks. | No new leg protects those particular **r53 artifact bytes**; **BINDING** concerns r54 claims only. **CONTROLS-b** is a related wrong-digest test, not a replacement for r53 history checks. | Q1 explicitly names claims bytes; Q12 freezes the old counter. | Existing r53 rejection remains the reported protection. Do not misattribute these routes to C2 execution. G1 boundary. |
| 3 | O §2.3: answer key became available in the shared tree before five label seats finished. No evidence of copying established. | None of **BINDING / ATTESTATION / EXTERNAL-PIN / CONTROLS-a–d** measures reader independence. | No such claim. | Protocol exposure, not demonstrated collusion. G6. |
| 4 | O §§1–3: ambiguity sweep, independent classifier, merge recomputation, hand readings and directional control challenge. Oracle content survived; one independent-classifier disagreement. | No R54 integrity leg adjudicates classifier semantics. | No such claim. | Surviving content challenges, not uncovered successful attacks. |
| 5 | P A1: remove all ledger rows and rename registry heading. Rejected by r53. | **REGISTRY** heading count / nonempty registry. | Yes: Q7. | Literal A1 is still statically rejected; do not conflate with partial deletion below. |
| 6 | P A2: remove one row from registry **and** ledger; r53 rejected through pinned row set. | **LEDGER** checks ledger equals current registry, but no pinned population is claimed. | Q8 claims current-registry equality, not a fixed 78-name digest. Q12 forbids changing real SKILL.md. | Source-inspected regression candidate: no row-set digest check found in E. Consistent shrink can evade static equality, not yet reproduced end-to-end. G5. |
| 7 | P A3/A3b: `python3 -c pass` and shell wrapper argv. Rejected by r53. | **entry-mode argv** shape/interpreter/script checks. | Yes: Q8. | E `entry_mode_ok` rejects shell tokens including `-c`. Static source evidence; no fresh execution. |
| 8 | P A4/A5: non-git source and source at an older revision; rejected. | Source cleanliness/revision control, supporting **EXEC**. | Yes: Q11. | E:287–296 checks source git status and revision equality. |
| 9 | P A7: enormous ledger timeout versus small operator cap; killed at cap. | **EXEC** timeout requirement. | Yes: Q9. | E:190 retains `min(ledger, operator)`. Printed ledger budget rather than effective budget is cosmetic, not a timeout bypass. |
| 10 | P D1: twelve `--help` substitutions exceeded r53 help cap; rejected. | **entry-mode argv** rejects `--help` outright. | Yes: Q6. | Exact token statically blocked; no reliance on a fraction cap. |
| 11 | P B1/B2: one/seven genuinely red rows green via `--help`; C1/D3: one/all twelve via `--selftest`; D2: mixed help/selftest. All passed r53. | **entry-mode argv** blocks those flags; **LAUNDERED branch** catches green declaration when plain entry exits nonzero. | Yes: Q6/Q9. | C `closed` constructs truthful entry and falsely-green entry variants; this is narrower than all possible argv substitutions. G2. **CONTROLS-a** is a C1 proof control, not this C2 route. |
| 12 | P A10: change non-script arguments such as `--expect` path, retaining script; r53 passed. | Intended entry-mode coverage does not require full documented-argv equality. | Q8 explicitly says script matches; no quote claims exact argument identity. | E `entry_mode_ok` checks script plus exact forbidden-token set; E `run_row` executes ledger argv. Same-class residual candidate, no new reproduction. G2. |
| 13 | P A13: rewrite registry entry cell to a benign instrument, matching ledger; r53 passed. | No **entry-mode argv** or **LAUNDERED** check distinguishes rewritten cell from authentic cell; **Q12 process freeze** is relevant. | Q8 only checks script match; Q12 forbids actual SKILL.md changes. | No instrument cell-content pin observed. Fixture-level candidate; actual seat edit prohibited. G5. |
| 14 | P A9: replace gate bytes with always-exit-0; r53 passed. | None; **EXEC** compares declaration with observation, not instrument strength. | No instrument-strength claim. | P explicitly records r53 A1 carve-out. Accepted measurement boundary, not a newly demonstrated R54 defect. G7. |
| 15 | P A11/B4: row writes worker-local `.git/config`; following row reads it. Same fixture passed jobs=1 and failed jobs=4. | **hermetic env** and **ENV** control address caller-global config; not local worker persistence. | Q10 specifically names caller-supplied `GIT_CONFIG_GLOBAL`. | E `Worker.reset`:181–185 restores files, not `.git/config`. Residual candidate remains; do not claim caller-global poisoning and local persistence are identical. G3. |
| 16 | P A12: `timeout_s="2.5"` caused traceback with no PREDICATE line. | No static timeout-type validation leg identified. | Q9 requires zero timeouts but does not promise structured malformed-input verdicts. | E:190 retains unguarded `int()` before try. Nonzero crash is **not false PASS / not fail-open**; it is a structured-receipt gap. G4. Negative-timeout bypass was unobserved by P and remains unconfirmed. |
| 17 | P A6: borrow red evidence from another row; rejected. | **EVIDENCE fragment** in that row's own output. | Yes: Q8/Q9. | E:338–340 checks fragment against `r['out']`. |
| 18 | P A8: committed worker file leaks to next row; rejected. | Worker reset supporting **EXEC** scratch execution. | Q9 claims execution; no specific reset algorithm promised. | E `reset --hard` + `clean -ffdx` retains file reset, unlike local git configuration. |

## Non-attacks, control scope, and hygiene

P A14 worker GC did not damage source (`git fsck` passed); A15 honest jobs=1/jobs=4 both passed. These are negative controls, not successful attacks. C1 **CONTROLS-a** (flipped proof byte) has no exact successful r53 precursor in O; it is a new r54 proof-integrity negative. Q4 claims it, but this scout did not run it.

N distinguishes prior same-task readings from mere census hits, and frozen-blocklist eligibility from the broader claim “never examined.” It found broader historical overstatement, not a frozen-rule counterexample. R54 explicitly says “neither claim re-labels any TB2 test”; none of its proof/execution legs certifies historical novelty of those tests. N also warns that pipeline EXIT=0 need not be counter exit. R54 explicitly states “Exit 0 of the controls script marks 'route demonstrated', which is the defect evidence.” Keep the controls-script status separate from the nested predicate.

## Routed gaps / unresolved candidates

1. **G1 — Object boundary / instrument trust (C1).** External BINDING names claims bytes, not r53 classifier/labels or counter bytes. O §5's proposed counter-digest pin is absent from the frozen claims text. Retaining claims while replacing other artifacts is not checked by BINDING. Counter replacement is a trusted-verifier boundary, not a reproduced R54 PASS.
2. **G2 — Non-forbidden argv substitution (C2).** E `entry_mode_ok` checks only script and exact tokens `--selftest`, `--help`, `-h`, `--dry`, `--version`; `run_row` executes the ledger's argv. A10's changed argument or another instrument-specific benign invocation may remain. High-confidence source gap; end-to-end reproduction outstanding.
3. **G3 — Worker-local config (C2).** E `Worker.reset` does not restore `.git/config`; ENV control only tests caller-global config. A11/B4 mechanics remain source-visible. Jobs-dependent reproduction outstanding.
4. **G4 — Malformed timeout receipt (C2).** Unguarded `int(timeout_s)` remains outside the execution try. A12-style malformed input is expected to crash without a predicate line. This fails nonzero, not fail-open; negative-timeout bypass unproven.
5. **G5 — Registry population/cell pins (C2).** No r53-style fixed row-set pin found in E; static equality is against current registry. A2/A13 consistent rewrites are residual fixture candidates. Real SKILL.md changes are prohibited by Q12; distinguish process breach from admitted input.
6. **G6 — Blind-reader protocol.** No R54 leg addresses O's shared-answer-key exposure. No collusion proven; R54 does not commission another label experiment, so this is inherited protocol scope rather than a live classifier claim.
7. **G7 — Instrument strength.** A9 remains outside declaration-versus-observation measurement. P explicitly treated it as accepted scope, not a new objection.
8. **G8 — EXTERNAL-PIN provenance (C1; additional source-inferred candidate).** A:412–430 checks receipt field presence, matching header values and distinct `source` strings; `fetched_at` freshness/source authenticity are not checked there and verify is offline. Thus Q3 freshness/independent-public-source provenance requires external evidence. No forged-receipt experiment performed. An honest late re-stamp also needs a real Bitcoin confirmation and differs from the assignment-pinned digest; not a demonstrated attack here.

Only G2–G5 directly continue successful P attacks; G1/G6 continue O's integrity/protocol boundaries; G7 is explicitly accepted scope; G8 is an additional source-derived question. Confidence is high in the quoted/static facts, conditional in unexecuted route outcomes. No fixes proposed.
