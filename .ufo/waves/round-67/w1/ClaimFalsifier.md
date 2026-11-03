# ClaimFalsifier-5 — round 67 w1 — scoped findings (full log: `ClaimFalsifier/falsify.md`)

Frozen claims at `dcc39ea3`; both predicates re-run this session and both HOLD:

- `python3 plans/round67_c1_pipeline_probe.py --check-receipt corpus/evidence/round67/pipe/receipt.txt`
  → rc 0, `CHECK ok cases=6`, `PREDICATE R67-C1 pass`.
- Default R65 checker over the committed receipt → rc 0 `PREDICATE R65-C1 pass` (unchanged); the
  frozen s1-s6 clauses (re-implemented verbatim in `ClaimFalsifier/a3-forges/strict_reimpl.py`,
  constants imported from the committed probe bytes) REFUSE `round66/red/fabricated-r65.txt`
  (24 defects) and ACCEPT the committed R65 receipt.

## Attacks that landed (all are disclosure/scope gaps; none trips a kill rule)

1. **A2 (C1) — `--check-receipt` accepts a fully fabricated receipt.** A hand-written
   receipt + six hand-written pytest-shaped junit XMLs (true case shas, self-computed junit shas,
   frozen vectors, copied PROBE/GRADER/VENV lines) passes with rc 0 / `PREDICATE R67-C1 pass` —
   zero grader runs. The checker rejected two sloppier forgeries (unknown testcase name; stale
   junit sha), so it does re-derive from bytes — but nothing anchors the junit bytes to a run
   (my forged junits say `hostname="fabricated"`, zero times). C1's named limitations (i)/(ii) do
   NOT cover this; C2's claims text names the sibling limitation, C1 does not. Evidence:
   `ClaimFalsifier/a2-fabricated/` (receipt sha256 `0387c958…`).
2. **A1 (C1) — a non-compliant implementation earns a pass pattern the frozen table does not
   anticipate.** `ClaimFalsifier/a1-variant-pipeline_parallel.py` registers a no-op forward hook
   via `getattr(torch.nn.Module, "register_" + "forward_hook")` (neither forbidden literal in the
   file), never partitions, never sends/receives. Predicted `PPPF` from grader lines BEFORE the
   run; observed at world size 1 under the port lock: exists P, no_hooks P, ws1 P
   (`3 passed, 1 deselected in 3.97s`; ws2 predicted F by the :144 bound, not run per item).
   The six frozen vectors all stand; but `no_hooks` is a substring match, not a hook detector —
   an implementation can violate S239's hook ban and print green. Named limitation (i) covers
   only AFAB-vs-1F1B. Evidence: `ClaimFalsifier/a1-hooksplit-ws1.junit.xml`
   (sha256 `16caad15…`).
3. **A3 (C2) — strict s1-s6 accepts forged fixtures beyond the committed one.** Two one-line
   forges of the committed R65 receipt: `forge1` (ENV G5 version → `0.0.0-forged-no-such-binary`)
   is accepted by strict AND by the default gate; `forge2` (`LEG G3 2` verdict flipped against
   its VECTOR) is accepted by strict but REFUSED by default (`G3 leg-verdicts PFF != PPF`) —
   strict is weaker than the existing gate on LEG/CASE/FRAGMENT rows. Kill rule (a) names only
   the committed fixture, so no kill; the field-binding table in falsify.md gives the exact
   forgeable surface. Recommended (report-only): make strict require the default checker's clean
   pass, and state the limitation the way C2's own text already does. Evidence:
   `ClaimFalsifier/a3-forges/forge{1,2}-*.txt`.
4. **C2 builder risk (report-only):** s5 "every `NOBIND` line carries `delta=0`" — the committed
   receipt's battery NOBIND lines carry no `delta=` field; a literal all-lines implementation
   refuses the committed receipt and trips kill rule (b). Scope the clause to per-case NOBIND
   lines (the re-implementation did; committed receipt then ACCEPTs).

## A4 (calibration)

Every checkable sentence of the Frontier step and both Score paragraphs verified against
committed bytes: S238/S239 shas ✓, cmp-identical captures ✓, SHA256SUMS:169 ✓, rationale line
numbers (:19/:31/:91/:144/:157/:171) ✓, `grep -c '^PROBE'` → 0 ✓, R66-C2 lesson section ✓,
no `merge/` dir ✓, round-54 L0 rows carried ✓, C2 pre-freeze-read tokens (receipt :2, probe :114,
RUN driver, CC/GCOV/BWRAP) ✓, M-1 reproduction ✓, SKILL.md:81 `recipe-unexecuted` ✓, coverage-7
L0-cap ledger rows ✓. Verdict: no sentence overclaims its evidence; the defects are the two
missing C1 disclosures (A2, A1) and the s5 ambiguity (4). Minor wording wobble: the Target line's
"second/first" ordinals mix census-list order with claim order.

## Files written

- `.ufo/waves/round-67/w1/ClaimFalsifier.md` — this report.
- `.ufo/waves/round-67/w1/ClaimFalsifier/falsify.md` — full attack log: predictions before runs,
  observed outcomes, commands with exit codes, field-binding table.
- `.ufo/waves/round-67/w1/ClaimFalsifier/a1-variant-pipeline_parallel.py`,
  `a1-hooksplit-ws1.junit.xml` — A1 variant and observed junit.
- `.ufo/waves/round-67/w1/ClaimFalsifier/a2-fabricated/{receipt.txt,q1-ref.xml}` — A2 forgery
  that passed.
- `.ufo/waves/round-67/w1/ClaimFalsifier/a3-forges/{strict_reimpl.py,forge1-env-version.txt,
  forge2-leg-verdict.txt}` — A3 strict re-implementation and the two accepted forges.

No installs, no network, no git mutation; the one grader run was flock-wrapped; scratch
`/fast/scratch/hyaku/kengaku-r67/ClaimFalsifier` removed.
