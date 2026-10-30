# C5KillRuleScope — attack on the R55-C2 kill-rule wording (3 probes)

Seat: C5KillRuleScope (kengaku round 55, w1, v2 build+attack).
Frozen text under attack — `plans/round-55-claims.md`, R55-C2 "Kill rule (frozen)":

> calibration HELD at 9 and the claim not admitted if any attack seat constructs a runnable
> fixture with ALL static legs clean that passes `plans/round55_c2_entryargv.py` at the
> measured-after revision while the row's registry-declared entry truly exits otherwise —
> i.e., a soundness break, not a documentation rewrite. (Rewriting the reviewed SKILL
> registry cell by hand is a documentation attack already carried by the r52 row-audit
> legs and reviewer cell audits; it does not fire this rule. LEDGER-side tampering that
> the binding legs fail to flag does.)

Method. Read the frozen claims and the three instruments (`plans/round55_c2_entryargv.py`
[in-flight, copied verbatim into the scratch clone], `plans/round54_c2_entrytruth.py`,
`plans/round52_c2_registry.py`); built three git fixtures under the seat scratch (each its
own toplevel, guard asserted before/after every fixture git mutation); ran the counter and
the r52 counter against them. Instrument selftest first: 4/4 PASS (`--selftest --work`, exit 0).
All fixture runs are receipts in `receipts/` beside this file.

---

## Probe 1 — does the registry-cell exclusion create a laundering lane (honest LEDGER, lying REGISTRY cell declared green for a red entry)?

**Verdict: UNSOUND** (scope/wording — the exclusion's named carrier does not exist and the
real mechanical carrier is scope-limited; finding, not a rule edit).

Counterexample (fixture `p1-laundering`, receipt `p1-laundering.r55.txt` / `.r52.txt` /
`p1.true-exit.txt`):
- registry ENTRY cell left honest (`python3 plans/fixture_gate.py`); verdict-map cell
  hand-rewritten `` `0` ok · `1` ok `` — declares green for a red entry;
- LEDGER honest: declares `entry_state=red, entry_exit=1` with reason ≥10 words and evidence;
- the entry truly exits 1 (independent plain-env run: `true entry exit=1`).

Observed: the C2 counter prints `PREDICATE R55-C2 pass`, exit 0
(`RUN executed=1 … laundered=0`, `TIPSTATE … declared_red=1 observed_red=1`), and the r52
counter prints `PREDICATE R52-C2 pass`, exit 0. The lie sails through both counters.

Mechanism: TIPSTATE compares LEDGER-declared green/red against hermetically observed exit;
no leg ever parses the verdict-map cell — by construction only `cells[2]` (entry,
`round54_c2_entrytruth.py:87`, `round55_c2_entryargv.py:91`) and the r52 name-separator
check (`round52_c2_registry.py:57`) read registry cells. The r52 row-audit legs
(`collect`, `round52_c2_registry.py:87-139`) are MISSING / INCOMPLETE / ENTRY-MISSING /
SELFTEST-UNBACKED / DUPLICATE — all static completeness checks; none re-executes a cell.

Who catches it, named exactly:
1. **R55-C1 frozen leg 2 (truth spot-leg)** and the **R55-C1 kill rule** — they execute each
   round-55-added row's named self-test and compare it with the verdict-map cell. Frozen
   scope: "registry row added in round 55" only — this round's 5 rows
   (`round54-c1`, `round54-c2`, `round55-c2`, `round55-c2-controls`, `round55-c3`).
   A lying cell on any of the ~75 pre-round-55 rows is out of scope for both.
2. **r52 row-audit legs** — demonstrated static; do NOT carry verdict-map truth. The
   parenthetical's claim "already carried by the r52 row-audit legs" is not borne out.
3. **reviewer cell audits** — this wave's human reviewer seats reading the registry block;
   one-shot, human, not a frozen leg.
4. **C2's own legs** — blind to `cells[3]` (demonstrated above).

Residual exposure: a hand-rewritten verdict-map cell on a pre-existing row passes both
counters; only human review stands between it and admission. The honest ledger still
measures the entry red, so this does not by itself defeat the C2 after-predicate — but it
is exactly the "LEDGER honest / REGISTRY cell lies" split the probe posits, and the rule
text asserts a carrier that does not exist as described.

Smallest safe correction (amendment row — seats may not edit the freeze): restate the
parenthetical as "carried by R55-C1's frozen leg 2 and kill rule for round-55-added rows,
and by reviewer cell audits for all other rows; the r52 row-audit legs are static
completeness checks and do not re-execute cells", optionally plus an L1-side extension of
the leg-2 spot to the full registry at the measured-after revision.

---

## Probe 2 — "ALL static legs clean": exact enumeration; can a row opt OUT of execution by carrying a defect?

**Verdict: SOUND** (the opt-out lane is loud and self-defeating; one benign wording omission).

Field enumeration — code truth (`round55_c2_entryargv.py:216-219` `static_ok` over the r54
`static_legs`, `round54_c2_entrytruth.py:209-237`):

1. `headings == 1` — exactly one `## Gate/probe registry` heading;
2. no `ledger_err` — ledger present, schema `r54-entrytruth-v1`, no duplicate JSON keys;
3. `missing == 0` — every registry row has a ledger row;
4. `extra == 0` — every ledger row has a registry row;
5. `argv_defect == 0` — r54 `entry_mode_ok` (`round54_c2_entrytruth.py:146-164`: argv shape
   ≥2 tokens, no shell wrapper among `sh/bash/dash/zsh/env/cat/true/-c`, no non-entry flag
   `--selftest/--help/-h/--dry/--version`, script match, interpreter `python3`/`uv`-form)
   **plus** r55 L1 ledger↔registry argv token-identity (folded into the same list,
   `binding_static_legs`, `round55_c2_entryargv.py:131`);
6. `wrapper_defect == 0` — L2: `argv[0] ∈ {python3, python}`, no `uv/pipx/poetry/npx/uvx`
   token, no inline `-c…` program token;
7. `abbrev_defect == 0` — L3: no flag token that is a strict prefix of a flag appearing in
   the row's own script body;
8. `bad_decl == 0` — ledger row is a dict; `entry_exit` int non-bool; `entry_state ∈
   {green, red}`; `(green) ⟺ (exit == 0)`; red rows carry `reason` ≥10 words and
   `evidence` ≥6 chars;
9. `duplicate_names == 0`;
10. `bad_table_lines == 0` — malformed non-separator table lines; **printed in the ROWS
    line but omitted from the frozen text's enumeration**;
plus `n_reg > 0`.

The frozen text enumerates 1, 3, 4, 5, 6, 7, 8, 9 — omitting `bad_table_lines` and the two
preconditions. Direction is safe: the code is strictly stricter than the words (a
`bad_table_lines`-dirty fixture fails the code while the text stays silent). Wording
imprecision, not a hole.

Opt-out experiment. r54 skips `bad_decl` and `argv_defect` rows from execution; r55
additionally skips `wrapper_defect` and `abbrev_defect` rows
(`round55_c2_entryargv.py:237-241`). Demonstrated:
- `p2a-baddecl-optout`: single row carrying `bad_decl` (`entry_state="amber"`) →
  `ROWS … bad_decl=1`, `RUN executed=0` against `registry=1`, `PREDICATE R55-C2 fail`;
- `p2b-argvdefect-optout`: two rows, one clean + one `argv_defect` → `argv_defect=1`,
  `RUN executed=1` against `registry=2`, `PREDICATE R55-C2 fail`.

So yes — a row can opt out of execution by carrying a defect, but the opt-out is loud and
self-defeating on every lane the rule cares about: (i) it dirties a named static leg,
violating the kill rule's own "ALL static legs clean" premise — a defect-carrying fixture
cannot fire the rule; (ii) the counter exits 1, so the fixture does not "pass
`plans/round55_c2_entryargv.py`"; (iii) for the lane's own after-run, `executed < registry
rows` breaks the after-predicate (`executed == n_reg`, `round55_c2_entryargv.py:303`).
Every skip class maps one-to-one onto a printed static-leg counter — no silent opt-out channel.

---

## Probe 3 — is the rule decidable by the closure (one command)?

**Verdict: SOUND as a firing rule; UNSOUND wording if "decidable by the closure (one
command)" is read literally** — the minimal decision procedure is the closure PLUS one
independent, non-hermetic execution of the registry-declared entry (procedural, not exploitable).

Fixture `p3-sandbox-gaming` (receipts `p3-sandbox-gaming.r55.txt`, `p3.true-exit.txt`):
the entry exits 0 when it detects the r54 hermetic sandbox (`GIT_CONFIG_SYSTEM=/dev/null`,
`hermetic_env`, `round54_c2_entrytruth.py:134-152`) and 1 in a plain environment.
Registry cell honest; ledger declares green@0. Observed: the closure prints
`RUN executed=1 … observed_green=1`, `PREDICATE R55-C2 pass`, exit 0; the independent
plain-env run of the registry-declared entry exits 1.

Two consequences:
(a) **The kill rule fires on this fixture as worded** — all static legs clean, counter
passes, the registry-declared entry truly exits otherwise, nothing hand-rewritten: a
genuine soundness break (hermetic observation ≠ true behaviour) and explicitly "not a
documentation rewrite". The exclusion does not shield it. The rule reaches
environment-gaming that no static leg can see — the instrument is correctly the weakest
point the rule defends.
(b) **Decidability**: the closure alone cannot establish "truly exits otherwise" — by
construction it reports only its own hermetic observation. Deciding the rule for a claimed
fixture takes the closure plus one independent non-hermetic execution of the
registry-declared entry (two commands). The canonical pattern already exists in the frozen
before-receipts: `plans/round55_c2_controls.py` demonstrates the registry-declared entry's
true exit 1 separately from the counter run. The universal reading ("no such fixture
exists at the measured-after revision") is not one-command decidable at all — it is a
soundness property over all conceivable fixtures; the closure is a per-fixture checker.

Severity: procedural/wording only — an attack seat must publish the second run as evidence
for the rule to fire, and the L1's receipt pattern already demands exactly that.

---

## Cross-cutting

- Impacted axes: **calibration** (C2, primary — all three probes); **operability** (C1,
  via the probe-1 coupling: C1's leg 2 is the only mechanical verdict-map truth-checker and
  it is round-55-addition-scoped).
- Probe-1 is the only finding needing a correction, and it lands as a dated amendment row
  or as L1-side spot-leg data — never a seat-side rule edit. Probes 2–3 need no rule change.
- No counter, ledger, registry, or claims file was modified. All fixtures ran in the seat
  scratch against a shared clone at the freeze commit `80afa613` with the in-flight
  instrument copied verbatim.
