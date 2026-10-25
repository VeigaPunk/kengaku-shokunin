# ConnKagiKama — kagi/kama overlap scan for round 25 (read-only)

Scope: `grep`/`read` under `kagi-shokunin/` and `kama-shokunin/` only. No sibling byte written,
no git/jj command in any lane, no endpoint contacted. Base read: `kengaku-shokunin` working tree
at `3f371d2` (read-only).

| # | sibling path:line | ruling | what kengaku should cite or route |
|---|---|---|---|
| F1 | `kagi-shokunin/corpus/drift-pins.sh:1-10` | duplicate (mechanism, failed once) | v1 "printed live fingerprints and stored nothing: with no expected values committed in the repo it could not detect drift, so a stale line ref (MODEL_ENDPOINT L17->L19) survived four rounds". Kengaku has the same blind spot now: `plans/round24_census.sh:19-21` strips `[:§].*` then tests only `[ -e ]`, so a rotted `:line` on a live file is invisible. C2's P2b must resolve the integer against EOF, not just the path. Cite `knowledge/drift-gate.md:11-13`. |
| F2 | `kengaku-shokunin/plans/round24_census.sh:11,14,16,20,21` | duplicate (population) | P2e's both directions already ship at base (`unidx`, `dead_index_rows`, `dead_plans_rows`). Route: cite it as P2e's predecessor; C2's real delta is exit-coded assertions + anchor resolution. Do not present P2e as unfurnished ground — it is a port. |
| F3 | `kagi-shokunin/corpus/drift-pins.sh:19`; `scope-gate.sh:49-50`; `surface-census.sh:37-38`; `claim-ledger.sh:114` | duplicate (convention, adopt) | Four independent kagi gates: `0 clean / 1 any defect / 2 usage-setup` (setup printed as `SETUP (...)`, never a bare death). This is C2's exact contract. Cite these as the convention of record. Selftest form to copy: `revision-audit.py` — "each asserting the expected exit plus finding ID (or no findings for the clean control)" (`.ufo/waves/round-22/build/AuditPinHistory.md:9`). |
| F4 | `kama-shokunin/tools/kama-probe.sh:40-41,120`; `kama-ollama-evidence.py:464-465` | **contradiction — state it, do not smooth** | kama inverts: `0 reconciled / 2 drift / 1 probe error`, and its own tool docstring says "This exit map is not kama-probe's (there 1=probe error, 2=drift)". There is no fleet-wide map. Kengaku's `2=usage` matches kagi and **inverts kama-probe**; name the lineage explicitly, or a kama-informed reader reads kengaku exit 1 as an error rather than a finding. |
| F5 | `kagi-shokunin/corpus/surface-census.sh:874-879`; `claim-ledger.sh:73-74` | adjacent-report-out (vacuous pass) | "fail closed: a summary that passes zero probes is not evidence … round-11 critic CE1 proved the verbs path could print `CLEAN (pass=0 skip=10)` with exit 0, which a claim row could then accept"; "ZERO checked cells is a setup error (exit 2), never a clean run". Both kengaku summaries admit exactly this: `assertions=0 match=0 mismatch=0` exits 0, and C1 with 0 parsed blocks satisfies "every stored point verdict re-derives" vacuously. Route: `assertions==0 → 2`, `blocks==0 → 2` (or explicit `UNTESTED`), each a red selftest case. |
| F6 | `kagi-shokunin/corpus/surface-census.sh:15-16,32-38` | duplicate (marker encoding) | Absence-licitness is structural there: `class: asset` (absence = drift) vs `class: runtime` (absence = informational `ABSENT`, still exit 0). P2d instead substring-scans prose for the token. Live hazard: `kengaku-shokunin/PROVINCE.md:8` and `:12` carry lowercase `absent` (row 12's is a diverging sub-path on a *resolving* row); only `:15` carries `ABSENT`. A case-insensitive test mislabels row 12; a case-sensitive one is one editorial lowercase from a false mismatch. Classify the 9 rows asset/runtime in the fixture instead. |
| F7 | `kagi-shokunin/corpus/claim-ledger.tsv:17,19,23,50,53` | adjacent-report-out (pin shape) | Exact case counts pinned in claim rows force migration: `(121 cases)` pinned twice (R11-09/R18-03; recorded 108→121), `(47 cases)` noted "40 at c41af82". Kengaku P2a rows (`SCORECARD.md:555-557`) must match `failed=0` + a floor, never an integer case count. |
| F8 | `kama-shokunin/tools/sources-append-only.py:562-563` | adjacent-report-out (crash vs finding) | "a non-UTF-8 blob is a parse error (exit 2), not a traceback (exit 1)". Under C2, exit 1 *means* mismatch — an uncaught parse crash would mint a fake finding. Wrap extraction; unparseable input → 2; add a malformed-bytes fixture case. |
| F9 | `kagi-shokunin/corpus/feature-claims.py` (via `.ufo/waves/round-22/build/BuildQualifierGate.md:25`) | none (novelty survives, narrow it) | No interval prior art fleet-wide: `grep -rlniE 'clopper\|wilson\|binomial interval\|confidence interval' kagi-shokunin/{corpus,plans} kama-shokunin/{corpus,plans,tools}` → empty; kengaku sweep → empty. But kagi already "separate[s] false admissions, misses, misclassification and unjudgeable results rather than publishing one accuracy scalar". So typed verdicts are **not** the novelty — the exact CP interval + Rogan–Gladen bound is. Narrow the sentence or a sibling-informed critic calls it restatement. |
| F10 | `kama-shokunin/registry/endpoint-consumers.tsv` (notes column); `registry/history/DELTA.md:6-11` | adjacent-report-out (endpoint health) | Rows read "currently DEAD … a correct pin does not establish a live endpoint"; DELTA records `MODEL_OK -> DEAD` at `2026-10-14T12:42:32Z` for all three pins. Cite as the reason P2d's `offline-unverifiable` is a finding class, not a gap: live-probe precedent shows a correct pin survives the endpoint dying. |
| F11 | `kama-shokunin/tools/test-snapshot.sh:107,146,193` | adjacent-report-out (mode parity) | `RESULT pass=N fail=0`; cases assert "snapshot exit mirrors clean check" and "row-set change preserves drift exit 2". One cheap C2 selftest case: `--summary` exit == `--json` exit on the same fixture. |

## Top move (one bounded proposal)

Apply F5 to **both** kengaku instruments rather than only fixing C2: treat `assertions==0`
(state_check) and `blocks==0` (attrib_calibration) as exit 2 with a printed `SETUP (population
empty)` line, and add the two vacuity cases as red selftest fixtures. Rationale: the same
vacuous-pass defect was already *proved* against a claimed gate in kagi (round-11 CE1), so the
failure mode is not hypothetical; and it is the only scan item that touches both owned axes
(calibration: a green run over an empty population is a false calibration signal; novelty: it
makes the "new construct" claim survive a critic who asks what happens on 0 receipts).

- **Affected axes** — calibration ↑ (no false green), novelty ↑ (construct safe under a
  zero-input probe). No axis harmed: it adds one exit branch and two fixtures, changes no
  frozen population.
- **Risks** — `2` then absorbs both "usage" and "empty population"; F4 shows the fleet already
  overloads `2`, so print a distinguishable `SETUP (...)` line rather than relying on the code
  alone. A pre-registered `assertions=<n>` count (P2) must not be edited; the guard lives in
  behaviour, not in the claims file.
- **Verification** — `python3 plans/state_check.py --summary` on an empty/temporarily-emptied
  fixture root → exit 2 + `SETUP`; `python3 plans/attrib_calibration.py --root <fixture with 0
  receipts>` → exit 2; both red cases present in `--selftest`; then the real runs unchanged.

No tool installed or updated. No network, no sibling write.

VERDICT: C2's exit-code and selftest *form* are already settled by four kagi gates (adopt `0/1/2`, 2=usage) — not new; C1's interval construct is genuinely absent fleet-wide; kengaku's real defects are inherited (P2e already ships at `plans/round24_census.sh:20-21`, anchor stripping repeats kagi's L17→L19 failure) plus a vacuous-pass branch both kengaku instruments share — fix the zero-population exit before any verdict is recorded.
