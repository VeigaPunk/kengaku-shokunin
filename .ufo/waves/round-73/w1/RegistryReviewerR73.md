# RegistryReviewerR73 — wave w1 report (round 73, reviewer seat)

Item: source review of `plans/round52_c2_registry.py` and `plans/round73_c2_registry_audit.py`
against PROTOCOL §Gate and the frozen sentences. Full numbered findings with line numbers and
counter-examples: `corpus/evidence/round73/w1/registry-review.md` (22.4 KB). No instrument was
edited; no battery or verdict CLI run (replay seat owns runs); all numbers below are static
derivations using the instruments' own pure functions over the landing bytes, rc 0.

## Provenance

- Freeze `255c261d` contains the PRE-A1 gate (`plans_seen` count 0 in that blob); the audit is
  unchanged since freeze. Landing `ea41880f` = HEAD adds the A1 arm + 8 rows. Base `d96c3e62`
  gate has no `--universe`.
- Claims file: A1/A2 committed in `ea41880f`; `## Erratum E-R73-1` (timestamp fix + non-admission
  of both originals) exists only as an UNCOMMITTED worktree modification at review time.

## Findings by severity

1. HIGH (operational, audit): `--selftest`/`--mutants` `finally: shutil.rmtree(work)`
   (audit L327, L397) deletes the ENTIRE `--work` directory named on the command line, not only
   its fixtures; `--work .` at the lane root would delete the lane. Contradicts the row's write
   scope and §Gate scope. Lets nothing through in the predicate; a destructive side channel.
2. MEDIUM (original-C1, gate): the freeze-commit arm `r73 = ok ∧ full ∧ plans_only ≥ 1` is
   UNSATISFIABLE — registered instruments are advertised by their own SKILL.md entry cell, so
   `plans_only ⊆ missing` and `ok ⇒ plans_only = ∅` ⇒ rc 0 unreachable. Confirmed by the L1's
   `a1-red-green.txt` (all five legs 0 → fail, rc 1). E-R73-1's non-admission of original C1 is
   code-consistent. A1's `plans_seen` arm (gate L158-163) is the minimal repair; the original
   frozen SENTENCE holds under the amended bytes (static: 113 advertised ≥ 111, MISSING 0,
   plans_seen 82, rc 0).
3. MEDIUM (row drift, gate): row `round52-c2` (SKILL.md:663) keys `0`↔"PREDICATE R52-C2 pass"
   and `1`↔"defects … R52-C2 fail", but the amended rc rule (gate L163) exits 1 on a green
   legacy run (landing bytes: legacy advertised = 113, all legs 0 — exactly this case).
4. MEDIUM (selftest vacuity, audit): arm 2's disjunction (L310) passes on the kind defect alone,
   so a total D3 regression stays selftest-green (only mutant M4 would catch it); arm 1 asserts
   only `d == 0` (L301); `red=3`/`arms=4` are literals (L324) — the quoted tally is decorative;
   no arm covers D1 or the unbacked-selftest leg; neither instrument's selftest asserts an exit
   code (§Gate self-test clause only partially met; the gate's ENTRY-MISSING/SELFTEST-UNBACKED
   arms are absent and the row declares it).
5. MEDIUM (D4 pairing, audit): `revision not in items[owners[0]]` (L190) is presence, not
   pairing — the live round-71 erratum item 1 contains BOTH hashes, so it passes for either
   pinned revision; extra numbered items and post-block numbered lists (to-EOF, L179) unpriced.
6. LOW ×9: gate L111 advertised-absent filter; gate L72 no columns leg; gate header-as-row
   (live: REGISTERED rows=115 vs audit 114); gate L91/L95/L101 selftest-cell escapes; gate L55
   silent ad-file skip; gate L36 CMD narrower than the claims' stated universe (declared);
   gate L242 selftest gated on lane SKILL.md; audit L115 absent self-test script never unbacked;
   audit L128/L147 whitespace-cell escape; audit L140 dead `.upper()` union; audit L94-106
   `command_flags` dead — and NO instrument prices the ENTRY cell's declared flags against the
   script (a row entry naming `--universe {full,legacy}` is checked by nothing); audit L209
   `total==rows` reader-side only.
7. AMENDMENT-TEXT drift: A1 restates the After-target as `total=113` while asserting
   "unchanged" (original section says 112); and the widening adds ZERO instruments to the
   advertised set at the landing bytes (legacy = full = 113), so the original "2 instruments
   enter through the plans/ leg" is false post-landing and nowhere retracted. A2 is honest and
   consistent (114 = rows = scripts; corrected rows price clean; errata statically green).

## Drift (frozen sentence vs prints)

No mismatch: every required substring is printed format-exact by the current bytes (gate:
UNIVERSE/ADVERTISED/5 legs/PREDICATE R73-C1/SELFTEST cases=4; audit: INSTRUMENTS/PARSED/D1-D4/
MISMATCH/PREDICATE R73-C2/SELFTEST arms=4/MUTANTS total=7). Exit codes: both return {0,1,2};
`2` declared in both rows and real; uncaught crashes exit 1 (classed failed, not
could-not-evaluate) in both.

## Two evidences

Neither instrument embeds or verifies a digest-pinned committed snapshot with expected verdict
(§Gate Two-evidences); the audit's only persisted expectations are the ERRATUM_ITEMS constants
(L52-55) and its row self-declares "structural, no digests"; neither prints the revision it
measured.

## RECIPE

Frozen predicate == code predicate for the GATE only under the A1 bytes at `ea41880f` (the
freeze-commit bytes could never print it); frozen-as-amended predicate == code predicate for
the AUDIT at print level, with the denominator equality reader-side and D4 weaker than its
wording.

## What I ran (all rc 0)

`mkdir -p` scratch; read-only git (`rev-parse`, `log`, `status --porcelain`, `show <rev>:<path>`,
`merge-base --is-ancestor`, `diff`); greps for line pins; one Python probe per derivation batch
importing the two modules and calling `collect`/`parse_rows`/`price_row`/`check_errata` over the
landing bytes (outputs quoted in the evidence file); read of `a1-red-green.txt`. No tool
installed or upgraded (none needed). Scratch removed; nothing left in `/tmp`.
