# ConnFleetScripts — fleet/kimi script overlap scan (round 25, read-only)

Scope: grep/read under `shokunin/scripts/` and `kimi-shokunin/scripts/` + referenced PROTOCOL gate surfaces;
lane tip `3f371d2`; no clone, no git/jj write, no endpoint, no install.
**S1 — SHONEN canonical-form verifier: none (ruling: none — real gap for P2c).** The only executable check is
`scripts/shokunin-watchdog.sh:144-163` `report_of` — SHONEN heading regex on *round reports* (`:148`,`:162`),
400-byte floor (`:54`,`:163`), digest baseline (`:141-142`); it never opens `SHONEN.md`. Same report-side duty:
`scripts/hyaku/inline.sh:110`, `scripts/hyaku/closure-prompt.md:21`, `templates/round-prompt.md:118`.
`kimi-shokunin/scripts/mint-agent.sh:66-69,91-98` copies the kit and prints probation; it verifies neither seed
nor boxes. Route: cite as report-side only; word C2 as the first executable SHONEN.md seed/evidence-line check.
**S2 — SCORECARD verifier: none in either script tree (ruling: adjacent).** `shokunin/.ufo/gates/root-ledgers.py:4-15,147-220`
grades only root SCORECARD/LOG (header, registry, aggregator order) and masks fences (`:150`); child-lane
capability/axis claims are never graded. `scripts/hyaku/closure-prompt.md:33` only tells the integrator to diff
and spot-read. Route: adopt fence-masking for P2a/P2b; do not present P2a/P2b as already covered.
**S3 — Lane-local predecessor is a probe, not a gate (ruling: duplicate population, different class).**
`plans/round24_census.sh:11-24,61-72` already ships P2e both directions (`unidx`, `dead_index_rows`,
`dead_plans_rows`), capability-row count (`:64`), README/PROVINCE counts and D10-D16 presence, then ends at
`:73 echo "C2.scorecard_state_defects_open $sd/6"` with no conditional exit — by `PROTOCOL.md:375` a probe that
cannot fail. Route: cite as P2e predecessor; state the delta (per-row tokens, anchor resolution, 0/1/2 exit,
`--selftest`); avoid its `C2.*` id prefix (collides with claim id C2).
**S4 — `2 = usage` is legal only if declared could-not-evaluate (ruling: convention, adopt).** `PROTOCOL.md:380`:
0 clean, 1 failed, every other code declared and mapped onto `clean|failed|could-not-evaluate`; undeclared
nonzero reads CNE. Precedents mapping 2 to CNE incl. usage: `SCORECARD.md:194` (closure-check "bad usage"),
`kagi-shokunin/SKILL.md:699` ("could-not-evaluate/setup"), `tabi-shokunin/SKILL.md:1614` ("bad args").
Counter-precedent: `SCORECARD.md:195` root-ledgers and `scripts/hyaku/jj-lane.sh:60` use `64` = usage;
`scripts/sources-census.sh:16-19` is four-valued. Route: row must read `2 -> could-not-evaluate (usage)`, no 64.
(Census copy/path already at ConnSoujiKaidoku F5/F6; kagi convention at ConnKagiKama F3.)
**S5 — Registry home + delivery (ruling: routing).** `PROTOCOL.md:398` sets a child lane's registry home as its
own SKILL.md; `kengaku-shokunin/SKILL.md:541` holds `hermetic-grader` (`:545`, 2->CNE) and `coverage-census`
(`:546`, probe). `PROTOCOL.md:418` (Delivery): closure grades no gate conformant until the row exists. Route:
append `state-check` + C1 `attrib-calibration` rows with the eight fields; `kengaku-shokunin/AGENTS.md` (5
lines) carries no gate duty — it arrives only through PROTOCOL.
**S6 — Self-test / two-evidences / revision duties (ruling: routing).** `PROTOCOL.md:385-397`: selftest asserts
exit code + stable finding id against committed expectations; a mutable-artifact gate ships a committed-snapshot
run with committed expected verdict, `expected.json` pins input digests, tamper is CNE, verdicts name the
revision. `scripts/hyaku/lane-addendum.md:56` requires wave-2 mutation-testing of every new gate. Route:
`state_check` prints root+revision (base `6180e4f`, landed `3f371d2`), selftest asserts exit+id, wave-2 budgets
a mutation seat.
**S7 — SHONEN seed source contradiction (ruling: state it, do not smooth).** `PROTOCOL.md:441-448` seed vs
`kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:455-462`: seed bytes identical, files not
(`sha256 886e459b...` vs `622b29a0...`; Gate Delivery line differs). `kimi-shokunin/templates/mint/SHONEN.md:1-6`
prepends a six-line `<!-- CANONICAL TEMPLATE ... -->` block while `PROTOCOL.md:432` allows only the box plus one
indented evidence line and says "no other prose" — a whole-file diff of a freshly minted lane fails P2c. Route:
P2c diffs seed block + per-box evidence lines only; report the kit preamble as protocol-owned, never strip it,
and pin which PROTOCOL copy state_check read.
**S8 — C1 prior-art sweep in scripts (ruling: none).**
`cd kengaku-shokunin && grep -rlE 'Clopper|Wilson|confidence interval' corpus/evidence/attrib-* plans/attrib*`
-> no output, exit 1; neither script tree has a CP/Wilson implementation. Prior art is scoped at
ConnSoujiKaidoku F9 (kaidoku r14 hand CP) and ConnKagiKama F9 (kagi typed verdicts). Route: cite those, narrow
the novelty sentence to the in-lane construct, never claim fleet-wide absence.
**S9 — Empty-population guard (ruling: adopt; cross-ref).** Only fleet-side null-input guard is watchdog's floor
+ digest baseline (`:54`,`:163`,`:141-142`). ConnKagiKama F5 already mandates `assertions==0 -> 2`;
`kagi-shokunin/corpus/claim-ledger.sh:73,114,995` shows the same fail-closed shape. Route: `state_check` empty
population -> exit 2 with `SETUP (population empty)` and a red selftest case; same for C1 with 0 parsed blocks.

VERDICT: no executable SHONEN canonical-form or child-lane SCORECARD verifier exists in either script tree (the
only SHONEN regex is report-side, `shokunin-watchdog.sh:162`); C2 must follow `PROTOCOL.md:380` by declaring
`2 -> could-not-evaluate (usage)`, register at `SKILL.md:541` per `:398/:418`, cite `round24_census.sh` as its
probe predecessor and `root-ledgers.py:150` fence-masking, and state the mint-kit SHONEN preamble contradiction.
Installs: none.
