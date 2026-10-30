# SP1CounterScope — scoped findings (r55 w1): YAGNI pass over plans/round55_c2_entryargv.py

Ruling: **keep all four binding legs; remove only dead module weight.** The counter was
never edited; every removal was proven behavior-preserving on a 7-fixture lab matrix plus
the counter's own selftest (byte-identical transcripts, receipts in
`.ufo/waves/round-55/w1/SP1CounterScope/evidence/`).

Per-leg ruling (acceptance):
- **L1 KEEP** — sole firer on FL1 (extra token `--quiet`: `l1=1 l2=0 l3=0`); the kill-rule
  surface (ledger-side tampering).
- **L2 KEEP** — sole firer on FB (`l1=0 l2=1 l3=0`): a registry cell itself declaring
  `-cprint(inline)` passes L1 (consistency) and L3 (no body-flag prefix) — only L2 fires.
- **L3 KEEP** — the seat question is answered **no**: L1 enforces ledger↔registry equality,
  so a registry cell that itself declares `--selft` is L1-clean and L2-clean; FA shows L3
  as the sole firer (`l1=0 l2=0 l3=1`). L3 guards the registry cell itself.
- **L4 KEEP** — the only leg that observes behavior (exit codes, evidence fragments).

Proposed removals (minimal diffs in `SP1CounterScope/proposals.md`, apply-ready):
1. drop `import time` (dead; r54 owns the clock).
2. drop write-only rebound globals `REGISTRY/LEDGER/SCHEMA/MIN_REASON_WORDS` (no in-tree
   reader; controls reads only `mod.evaluate`).
3. dedup local `_keep` → `m._keep` (byte-identical bodies; `m` in scope). The `HEAD_ROW`
   dedup was tried and rejected: `_mk_fixture` has no `m` → NameError (receipt kept).

Explicit keep rulings with disproof: the bad_decl half-clause is a latent no-op (r54 uses
bare names, the clause matches `name:` prefixes) but its removal changes behavior on
name-collision rows (pristine silently skips row `X`'s binding legs → `LAUNDERED X`); the
`isinstance(sp, dict)` guard is load-bearing (removal crashes on non-dict ledger rows with
AttributeError instead of clean BAD-DECL); L2/L3 shape guards and `INTERPRETERS`' `python`
are provably unreachable defense-in-depth; `job()`'s registry-argv recompute is the
documented L4 contract, not dead weight.

Integration risks for L1 (data items, not counter defects):
- 17 registry cells embed usage placeholders (`<lesson.md>`, `DIR`, `[--verbose]`, `REV`, …)
  that can never token-equal concrete ledger argv → 17 ARGV-DEFECT at the after-run unless
  cells are normalized first (adoption-check, anchor-digest-check, coverage-census,
  gate-flip-check, gate-timing, ledger-tip, mutant-direction-check, package-gate,
  round-close-check, round28-census, round50-c1, round53-c2, scratch-root-guard,
  sources-adopt, stage-scan, tb2-grader-probe, tip-receipts).
- `tb2-grader-probe` (cell `uv run --no-project --with biopython==1.85 python3 …`) is
  unpassable under frozen L1+L2: `registry_entry_argv` → None, and wrapper argvs are
  L2-killed. Needs a dated amendment before the after-run.
- Ledger today: 83 rows vs 78 registry rows (the 5 planned round-55 ledger additions print
  as EXTRA).

Baseline verified before analysis: r54 counter passes both frozen laundering fixtures
(exit 0, `PREDICATE R54-C2 pass`, true entry exit 1); r55 counter kills both (exit 1,
`ARGV-DEFECT` + `ABBREV`/`WRAPPER-DEFECT`); selftest 4/4. Full commands/exit codes:
`SP1CounterScope/report.md`. Installs: none. Scratch deleted.
