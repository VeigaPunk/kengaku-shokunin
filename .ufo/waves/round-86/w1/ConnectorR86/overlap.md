# ConnectorR86 — sibling-overlap scan (round 86, read-only)

Scope: sibling lane repos under `/home/vgpnk/Projects/shokunin` (never written).
Two primitives this round uses:

- **P1 (R86-C1 leg L3-tip):** a receipt stamp field `LANE_TIP <40-hex>` whose value
  must be a resolvable commit that is an ancestor of the measured revision —
  `git cat-file -e <tip>^{commit}` + `git merge-base --is-ancestor <tip> <anchor>`
  at `kengaku-shokunin/plans/round86_c1_replay.py:316-327`.
- **P2 (R86-C2 leg P1-derive):** a frozen pointer (`SHONEN.md` box 4 →
  `PROVINCE.md:<line>`) whose line number is *derived* from the measured bytes
  (token occurs exactly once) rather than a hardcoded constant —
  `derive()` at `kengaku-shokunin/plans/round86_c2_repin.py:74-82`, cross-checked
  against `P3C_PINS` and `state_check.py --summary` (legs P2/P3/P4).

## P1 — replay receipt bound to a resolvable ancestor tip

`merge-base --is-ancestor` appears ~234 times across sibling `scripts/`,
`tools/`, `plans/` (grep census). The relevant question is not the primitive
(git ancestry is universal) but **a receipt/stamp carrying a declared tip that a
counter verifies against the measured revision**.

### Hits

1. **kama-shokunin — `tools/round72-receipt-tip-binding.py`** (and successors
   `round73-receipt-claim-binding.py`, `round74-receipt-claim-binding.py`,
   `round76-receipt-scope.py`, `round77-citation-baseline.py`).
   Classification: **DUPLICATE (same mechanism, different field name).**
   `round72-receipt-tip-binding.py:184-185` defines `_is_ancestor(repo, rev, tip)`
   as `git merge-base --is-ancestor`; `:424-440` requires every cited receipt to
   carry a `# tip=<40-hex>` / `# rev=<40-hex>` header among its first five lines,
   that header must resolve (`cat-file`) and be an ancestor of the measured tip,
   and the delta `<rev>..<tip>` must touch only declared record paths
   (`default_record_paths`, `:209-216`). Round 77 adds the baseline-receipt class:
   a `measured/before/` receipt binds when its header names an ancestor of its
   *introducing* commit and its bytes are identical at introduction and tip
   (`round77-citation-baseline.py:54-84`). The resolution path is the same as
   this lane's L3-tip — resolve the stamp, `cat-file -e`, `merge-base
   --is-ancestor` — but the field is `tip=`/`rev=` in a `#`-comment header rather
   than `LANE_TIP ` in a stamp block, and kama additionally binds the
   *record-only delta* between the receipt's revision and the tip, which this
   lane's L3 does not check.

2. **kaidoku-shokunin — `tools/round-44/c1-counter.py:1582-1583,2083`** (same
   pattern at rounds 39-42, 45, 49). Classification: **DUPLICATE (partial).**
   `receipt_fresh = first_add != freeze and is_ancestor(root, freeze, add)` —
   the receipt's *first-add commit* must descend from the freeze revision. This
   binds freshness (receipt minted after freeze) rather than tip-reachability
   (receipt names a revision that is an ancestor of the measured tip). Different
   direction of the same `merge-base` primitive; not the same mechanism.

3. **tabi-shokunin — `scripts/check-adjacency.mjs:216,407-413,1791`** and
   `scripts/check-user-round-contract.mjs:159-204`. Classification:
   **NEW-MECHANISM.** Tabi resolves the *lane tip itself* (attached HEAD branch
   or `refs/heads/master` fallback, strictly one `refs/heads/` ref, resolved to
   a commit, cached per root) and then requires cited commits to be reachable
   from it — the anchor is derived from repo state, not read from the receipt.
   This lane's L3 instead reads the declared `LANE_TIP` *from the receipt* and
   checks it against the measured revision. Tabi never trusts a self-declared
   tip field; kengaku does (the stamp is the claim being verified).

4. **tsukuroi-shokunin — `tools/_revision.py:156-192`** (imported by the
   round-18+ `--revision` tools) and `tools/check-revision-binding.py:175-182`.
   Classification: **NEW-MECHANISM.** A shared `bind()` that resolves a revision,
   verifies it is an ancestor of `refs/heads/<branch>` *and* of
   `refs/remotes/origin/<branch>` when present, with a frozen failure-id map
   (`E-REVISION-NOT-LANDED`, `E-REVISION-NOT-PUSHED`, `E-GIT-FAILED`). This is
   revision binding for *tool inputs*, not receipt-stamp verification; the
   two-level ancestry (branch + pushed remote) has no counterpart in L3-tip.

5. **kengaku-shokunin internal lineage** — `plans/round80_c1_located_replay.py:269-276`,
   `round81_c1_new_members.py:336-345`, `round83_c1_replay.py:402-415`,
   `round84_c1_replay.py:465-478`. Classification: **DUPLICATE of this lane's
   own prior mechanism.** R86-C1's L3-tip is the same check softened from
   "LANE_TIP equals measured tip" (r86 initial commit `0481a6d3`) to "resolvable
   ancestor of measured tip" (commit `c939e6b5`). The field name `LANE_TIP` was
   introduced by this lane at round 75 (`plans/round75_c1_index_parity.py`,
   commit `e462a649`, 2026-11-04). Fleet census: `LANE_TIP` as a receipt/stamp
   field exists **only in kengaku-shokunin** — every other lane's hit is either
   a lesson mentioning the word (`kake-shokunin/corpus/lessons/round-31.md:74`)
   or tabi's unrelated `LANE_TIPS` map variable (see hit 3). The named field is
   lane-local; the *mechanism* is fleet-common.

## P2 — derived self-assessment pin (line computed from bytes)

### Hits

1. **kaidoku-shokunin — `tools/round-79/pointer-bind.py` and
   `tools/round-80/pointer-bind.py`.** Classification: **DUPLICATE-adjacent /
   NEW-MECHANISM (verifies the pin, does not derive it).**
   `pointer-bind.py` binds each `PROVINCE.md` `path:line` pointer to the token
   it claims on the pointed line (`occurrence_context`, `bind`, `:118-163`),
   and `--control path-only` records the round-78 rule that ignored the line.
   This is the *checker* half of this lane's P4 (pin agrees with bytes); it
   still reads a **frozen line number** from the record — it does not compute
   the line from bytes. Round-80's strictness battery adds duplicate-pin and
   exact-token refusals. Resolution path: parse `path:N-M`, read lines
   `N..M`, require the declared token there. Kengaku's `derive()` inverts this:
   it *finds* the line of a unique token and requires the pin to equal it.

2. **kaidoku-shokunin — `tools/round-66/coverage-selfcheck.py:246-330`.**
   Classification: **DUPLICATE (same claim class, different atom).**
   `--selfcheck` re-derives two self-assessment atoms (SCORECARD coverage-row
   head score and cited `<mapped>/<files>` fraction) against the stem recipe at
   the measured revision and counts `mismatches` — the same "frozen
   self-assessment vs observed bytes" population as `state_check.py --summary`,
   but over coverage numbers rather than `path:line` pins. The mismatch-count
   shape (`mismatches = sum(1 for a in atoms if not a["ok"])`) is the closest
   sibling to this lane's `state_mismatches` leg.

3. **kagi-shokunin — `corpus/drift-pins.sh` (verify `:190-250`, pin `:260-360`).**
   Classification: **DUPLICATE (same repair philosophy, different substrate).**
   Symbol pins are `<path> <line> <ERE>` rows in `drift-symbols.tsv`; `--pin`
   re-derives the line via `grep -nE -m1` only when the ERE matches exactly once,
   refuses on GONE/AMBIG, and `MOVED` reports `pin->actual` (`:346-357`). This
   is byte-derived line re-pinning with a uniqueness guard — semantically the
   same move as `derive()` (`token occurs exactly once → its line`), applied to
   host files rather than `PROVINCE.md`, and with an explicit refuse-on-ambig
   rule this lane's counter also has (`token-count != 1` → `SetupDefect`).

4. **kumitate-shokunin — `scripts/routed-ledger.mjs:16-29,300-340`.**
   Classification: **NEW-MECHANISM (adjacent).** Ledger rows bind answers by
   `path:line` plus a quote located at that *exact* line — the pin is verified
   by quote-at-line, never derived. Same "pin must agree with bytes" family,
   opposite direction.

5. **kaidoku-shokunin — `tools/round-26/c2-calibration.py:162-190,221-240`** and
   `tools/round-36/c2-counter.py:45-55,153-165` (also round-38).
   Classification: **NEW-MECHANISM (section-range derivation).** These derive
   *section boundaries* from heading lines (`## Queue-drain craft`, last
   non-blank before next `## `) and compare stated vs derived ranges/counts —
   byte-derived geometry, but the derived value is a range/count, not a single
   pointer line fed back into a pin.

6. **chousa-shokunin — `tools/claims-audit.py:87-130`.** Classification:
   **NEW-MECHANISM.** Anchors *locate* statements in a claims file
   (`anchor in line`), then re-derive the fact; the anchor is a substring, not
   a computed `path:line` written back into a pin.

7. **mori-shokunin — `tools/mori-claim-sweep.py:45-90,161-170`.**
   Classification: **NEW-MECHANISM.** A self-assessment sweep that extracts
   lane pointers from SCORECARD/SHONEN/LOG and checks them against the tree —
   closest in *population* to `state_check.py`, but it checks pointer
   existence/resolution, not a pinned line number derived from bytes.

## Fleet-first assessment

- **P1 (ancestor-bound receipt tip):** the *mechanism* is fleet-common
  (`merge-base --is-ancestor` on a declared revision, ~234 call sites), but the
  *named stamp field* `LANE_TIP` and the specific leg shape (receipt stamp →
  resolvable + ancestor-of-measured, with forged-tip controls `LANE_TIP 000…`/
  `111…` at `round86_c1_replay.py:470,521`) are **kengaku-first**: introduced
  at round 75 (`e462a649`) and refined through rounds 80-84. Kama's
  `tip=`/`rev=` header binding (round 72, 2026-11-03/04) is the nearest sibling
  and is arguably earlier by hours; it additionally enforces a record-only
  delta that this lane lacks. Neither absorbs the other: different field,
  different extra legs.
- **P2 (byte-derived pin line):** **fleet-first for this exact shape.** No
  sibling computes a `path:line` pointer's line number from bytes and writes it
  back as the pin value. Kagi's `drift-pins.sh --pin` is the same *idea*
  (unique-match line refresh, refuse on GONE/AMBIG) on host files; kaidoku's
  `pointer-bind.py` verifies a stated line rather than deriving it; kaidoku's
  `coverage-selfcheck.py` and `c2-calibration.py` derive *other* quantities
  (fractions, section ranges). The kengaku repair is a new resolution path:
  derive → require pin == derived → require state_check's own output clean.

## Cheapest shared-standard candidate

**P2's uniqueness-guarded line derivation** is the cheapest candidate for a
shared standard: it is ~10 lines (`enumerate(splitlines())`, filter token,
require exactly one hit), already proven in two independent lanes (kagi's
`drift-pins.sh --pin` MOVED leg; kengaku's `derive()`), and generalizes to any
`file:line` pin. The owning lane for a fleet-wide standard would be the
**protocol/integrator** (fleet-root `PROTOCOL.md` / `shokunin.conf` owners),
not any single lane — no lane currently owns a cross-lane pin-derivation
contract. P1 is *not* a good standard candidate: the stamp field is
lane-local convention and kama's richer binding (ancestor + record-only delta)
arguably supersedes it if a standard is ever written.

## Contradictions / honest limits

- The frozen contract's `LANE_TIP` naming is kengaku-internal; calling it a
  "replay receipt bound to a resolvable ancestor tip" is accurate mechanically
  but the *field* has no fleet precedent — a reader should not expect sibling
  lanes to emit it.
- Kama's round-72 binding is stricter than this lane's L3 (adds the
  record-only-delta leg and the first-five-lines header window); if a shared
  standard emerges it should start from kama's shape, not kengaku's.
- Kagi's `drift-pins.sh` re-pin is operator-invoked (`--pin`), not
  counter-verified like `round86_c2_repin.py`'s P1-derive leg; the *derivation*
  overlaps but the *verification loop* does not.
- No instrument bytes were modified by this seat; this is a read-only report.
