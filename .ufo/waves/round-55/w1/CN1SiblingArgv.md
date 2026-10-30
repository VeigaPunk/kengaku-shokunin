# CN1SiblingArgv — scoped findings: sibling overlap for entry-argv binding / ledger-truth / registry-closure

Read-only scan of the four named siblings' instrument dirs at current HEADs
(kumitate `1e00955a` scripts/, tameshi `9806562c` tools/, chousa `a6b6f93` tools/,
kama `3325e8ed` tools/). Full evidence + per-instrument rulings:
`.ufo/waves/round-55/w1/CN1SiblingArgv/overlap.md`.

## Verdict

**No sibling lane owns an entry-argv binding, an R55-C2-shaped ledger-entry-truth
counter, an R55-C1-shaped advertised-vs-registered closure gate, or a multiset grader
probe. DUPLICATE-INSTRUMENT RISK: NONE for all three round-55 instruments** — build
may proceed; cite the adjacent precedents below, do not absorb.

| round-55 instrument | nearest sibling neighbor(s) | ruling |
|---|---|---|
| R55-C2 argv binding (`plans/round55_c2_entryargv.py`) | tameshi `tools/command-binding.py` (argv/exit/cwd/rev binding vs caller-owned expected bundle; no registry↔ledger binding, no wrapper/abbrev legs); tameshi `tools/registry-check.py` (re-executes own registry rows); kama `tools/round43-registry-audit.py` flags leg (`--flag` ↔ `add_argument`) | ADJACENT ×3, all different data — none binds ledger `entry_argv` token-equal to a SKILL-registry declared entry with interpreter-identity, no-wrapper, no-abbreviation legs and per-row hermetic ground truth |
| R55-C1 registry closure (`plans/round52_c2_registry.py`) | kama `tools/gate-registry-check.py` (occurrence+meaning gate: tracked counter paths ↔ SKILL.md tables, thin-row/empty-entry/missing-path legs) | ADJACENT, different data on both sides — kengaku's population is the advertised text set (LOG/SCORECARD/SKILL/README/knowledge) and the registry carries verdict maps + self-test backing with MISSING/INCOMPLETE/ENTRY-MISSING/SELFTEST-UNBACKED/DUPLICATE legs |
| R55-C3 multiset grader probe (`plans/round55_c3_chess_probe.py`) | chousa `tools/assimilate-rows.py` selftest ("comparison is of multisets") | DIFFERENT-DATA — FINDING-line multiset in an expected file, not grader verdict semantics; no TB2/chess surface exists in any sibling |
| ledger-truth (R55-C2 corrections) | kumitate `scripts/routed-ledger.mjs` (routed items ↔ ledger rows via located quotes); kama `tools/digest-ledger.py`; tameshi `tools/receipt-revision-gate.py` | ADJACENT ×3, different data — none checks a counter ledger's declared entry argv / evidence fragment / exit truth |

## Standing-ruling re-check (r14: "no sibling owns an evidence-replay gate")

**HOLDS at the four HEADs for both new instruments**, under the ruling's r11-scoped
definition (hermetic offline recomputation of committed *model-probe records* and
their derived statistics). Kama's `round5x-replay-*-audit.py` family audits a *live
llama-server process* (endpoint identity), and kumitate `receipt-evidence.mjs` /
tameshi `registry-replay.py` replay *recorded command invocations / registry rows* —
none recomputes committed model-probe records.

Narrowing stated for the record: in the broad "replay declared commands to re-derive
a verdict" sense, tameshi and kumitate already own replay-style gates over their own
objects, so round-55 claim text should claim novelty for the *binding* construct only
(ledger↔registry argv identity + wrapper/abbrev legs + advertised-set closure), which
has no sibling owner at these HEADs.

## Notes / defects (report-only)

- Fleet root mounts the kumitate repo twice (`kumitate-shokunin`, `kumitate-shokunin`),
  same HEAD `1e00955a` — one repo, scanned once.
- `kumitate-shokunin` has no `tools/`; its instrument dir is `scripts/`.
- No edits to any sibling file; no installs; no network; no scratch needed (read-only).
