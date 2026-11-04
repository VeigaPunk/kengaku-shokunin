# ConnectorR82 — sibling-overlap scan, kengaku round 82 w1

Seat `ConnectorR82`, role connector, kengaku round 82 wave w1 (12 seats), hyaku run 15 attempt 1.
Measured tip `12f1029a45cf0097a3afd030d757bf93b87f8018` (`git rev-parse master`, read twice: before the
scan and again after the last evidence command — unchanged, and equal to the freeze commit).
Base revision for every "before" state: `a3a03ac31451e58f1742b9bccb73b72c2d90a95c`. Frozen claims
`plans/round-82-claims.md` read in full before any sibling command.

This seat wrote exactly one file: this report. No lane/sibling file was created, modified, committed
or pushed; no fixture repo, no clone, no gate, no counter and no selftest was run (every command
below is read-only: `git rev-parse`, `git ls-tree`, `rg`, `sed`, `nl`, and one in-process Python
read of committed bytes). Scratch dir `/fast/scratch/hyaku/kengaku-r82/ConnectorR82` was created by
the seat rule and removed before yield (`rm -rf -- /fast/scratch/hyaku/kengaku-r82/ConnectorR82`);
nothing was ever written into it. No tool was installed or upgraded.

---

## 1. Method

Four measurements, each re-runnable:

```sh
cd /home/vgpnk/Projects/shokunin
# (i) mechanism census across the 20 sibling lanes, docstring-level, wave/report/fixture trees excluded
#     (in-process walk; needle sets per mechanism, see §2)
# (ii) medium pass: every .mjs/.js/.sh in the same exclusion set (tabi/kumitate are .mjs lanes)
# (iii) token probes for the distinguishing predicates
rg -n --glob '*.py' -e 'unrunnable' -e 'reproduced' -e 'diverged' . | grep -v '^./kengaku-shokunin/'
rg -ln --glob '*.py' -e 'revert' . | grep -v '^./kengaku-shokunin/' | grep -Ev '/(\.ufo/waves|reports|corpus/live|fixtures|tests)/'
# (iv) id/URL collision probe
rg -n '^\| *S262 ' */corpus/SOURCES.md
rg -c 'https?://' kengaku-shokunin/plans/grader-population-ledger.json kengaku-shokunin/plans/round82-sweep-map.json
```

Search bound (stated so the negative claims are readable): the census reads the first 3 000 bytes of
every `.py`/`.mjs`/`.js`/`.sh` under each lane, excluding `/.ufo/waves/`, `/.ufo/evidence/`,
`/.ufo/reports/`, `/reports/`, `/corpus/live/`, `/fixtures/`, `/tests/`, `/.git/`, `/archive/`,
`/.scratch/`, `/.tower/`, `/node_modules/`. A gate that implements a mechanism without naming it in
its header is invisible to this pass; §6 states that residual.

---

## 2. Per-lane nearest mechanism (`path:line`)

`—` = no mechanism found in the lane's non-wave, non-fixture surface. "near" = same mechanism,
different universe/binding; "adj." = adjacent class only.

### (a) registry completeness — a gate auditing a lane's gate table against the scripts the lane holds

| lane | nearest | class |
|---|---|---|
| tabi | `scripts/check-gate-registry.mjs:22-46` — gate set **derived from the bytes** ("never from the registry itself, so the registry cannot vouch for its own completeness"), findings `e1-missing-row` / `e2-field-incomplete` / `e3-row-script-absent`; names `PROTOCOL.md` §Gate standard as its owner standard | **near** |
| tsukuroi | `tools/check-registry-coverage.py:2` + `:267-302` — universe = committed `tools/`, per-row cells, `REGISTRY-ROW-ORPHAN` "registry row names absent regular tool" | near |
| kama | `tools/gate-registry-check.py:11-21`, `:34-35`, `:230` — population = `.ufo/waves/round-*/count-*.py` + `tools/round<N>-*.py`; `registered/unregistered/defective`, `missing-path:PATH`; prose-only = unregistered | near |
| kotoba | `verifiers/check_gate_registry.py:17-19` (universe = `verifiers/*.py|*.sh` at rev), `:25-40` (8-cell row, entry cell must contain the path, verdict map, selftest flag must be a live handler) | near |
| mori | `tools/mori-gate-registry.py:14-21` — 8-cell tables anywhere in the registry file; entry path must resolve at rev; `wrong_row` | near |
| kake | `.ufo/waves/round-74/c74_registry_gap.py:7-14` — frozen 8-counter population, row required, "a prose mention outside such a row never counts", first backticked `.py` must `git cat-file -e`; **a frozen round counter in a wave dir, not a standing gate** | near (prior art) |
| kaidoku | `tools/round-71/registry-census.py:20-28` — row grammar v2; tool cell path must exist at rev | adj. |
| souji | `tools/souji-landing-gate.py:6-8` — "a registry-cited script that does not parse landed as unverified candidate" | adj. |
| tameshi | `tools/registry-figure-bind.py:2-11` — registry *figures* vs the instrument's current output | adj. |
| revenger | `corpus/check_embedded_outputs.py:5-9` — self-describes its own registration ("Registered gate (SKILL.md `## Gate registry`)") | adj. |
| chousa | `corpus/evidence/round56/c1-gate.py:2-9` — "the registered gate of `tools/build-spans.py` (SKILL.md registry)" — instance, not completeness | adj. |
| kotodama | `tools/check-gate-battery.py:2-12` — executes "the seven structural gate selftests, plus the baseline check over all ten registered gates" | adj. |
| game-dev-3d | `reports/round-107/mutations/gate-control-matrix.sh:1` | adj. |
| kagi | `corpus/scope-gate.sh:1-12` — ownership partition of surfaces, not a registry | — |
| kumitate | `scripts/counter-pins.mjs:2-8` — counter byte pins, not row completeness | — |
| audio, game-dev-2d, lore | — | — |

### (b) closure-debt discharge from the newest spot-check

| lane | nearest | class |
|---|---|---|
| kumitate | `scripts/routed-ledger.mjs:13-18` — reads **every** routed section of **every** `corpus/lessons/round-N-verifier-spotcheck.md`, `UNLEDGERED` per item, quote of 3-25 words unique in its section, and every closed/wontfix row binds by `path:line` + a quote at that **exact** line (`ANSWER_DEAD`), `ROW_CONTRADICTED` | **near** |
| tameshi | `tools/defect-bind.py:2-8` — "A non-author closure routes defects … as prose. Without a counter, 'closed' is an assertion … turns each routed defect into one declared row" | near |
| tsukuroi | `tools/check-r74-routed-r75.py:1-24` — four items of `round-74-verifier-spotcheck.md` §7, committed bytes only, block rule, `DECOY-DISTANT` | near |
| kasegi | `corpus/instruments/r45-routed-defects.py:2-8` — five status-bearing items of `round-44-verifier-spotcheck.md` §6, per-item limb with bound artifact bytes | near |
| kotoba | `verifiers/check_routed_repairs.py`, `verifiers/check_r83_routed_repairs.py` (per-round routed-repair verifiers) | near |
| mori | `tools/mori-routed-check.py:2-13` — round-23 routed items R1-R4 re-derived at a pinned rev, git objects only | near |
| kagi | `corpus/closure-dispositions.py:6-30`, `:106` — closure record → obligation ids (`D<n>`, `SPOT-<NN>`, `ADJ`), exactly one typed disposition each, `fixed` pointer must carry the id (+`#anchor`) and the source is sha256-pinned | near |
| mado | `quality/check-control-receipts.py:2-5` — "Round-27 successor of the QUALITY criterion 36 checker (round-26 spot-check §7 repairs 2 and 5)" | adj. |
| kama | `tools/round69-newest-closure-counter.py:2-10` — resolves the newest non-author closure and checks the SCORECARD pointer **names it** (pointer freshness, not discharge) | adj. |
| kaidoku | `tools/round-66/closure-boundary.py:2-8` — repairs a counter's own boundary defect routed by the round-65 closure | adj. |
| chousa | `tools/digest-in-tree.py:2-6` — routed defect "before-receipt pinned a sha256 from uncommitted bytes" closed as a class gate | adj. |
| audio, game-dev-2d, game-dev-3d, kake, kotodama, lore, revenger, souji, tabi | — | — |

### (c) population sweep — re-run a lane's own instruments at one tip and classify

| lane | nearest | class |
|---|---|---|
| tameshi | `tools/registry-check.py:2-20` — "replays every active row of `tools/registry.json` and reports how many rows still return their registered outcome" (per-row `argv`, `expect`, `timeout_s`); `tools/registry-replay.py:2-14` — refuses to publish when any runner row did not hold (`RUNNER_NOT_HELD`), projection into a bundle | **near** |
| kotoba | `verifiers/check_tip_battery.py:4-10` — runs the lane's own six-gate battery at `--rev`, prints "tip battery exit 0: N of 6" | near |
| kotodama | `tools/check-gate-battery.py:2-12`, `:54` — seven gate selftests in an isolated mirror + baseline over all ten registered gates, before/after sha256 path-set snapshot | near |
| souji | `census/round-17/gate-replays.py:2-20` — replays one gate at five pinned revs, compares **exit code + exact finding multiset** against `gate-replays-expected.json`, reports divergence | near (projection only) |
| kake | `scripts/receipt_replay.py:2-8` — replays a digest-pinned receipt set at one revision | adj. |
| kumitate | `scripts/counter-rerun.mjs:4-14` — K runs of one counter, `AGREE`/`DISAGREE` (the determinism leg only); `scripts/control-replay.mjs:2-14` | adj. |
| mado | `quality/population-suite.py:2-8` — offline gate over the population checker, built-in fixtures | adj. |
| revenger | `reports/round-88/receipt_sweep.py:3-6` — extends a receipt rule to **every** `corpus/SOURCES.md` row | adj. |
| kaidoku | `tools/round-62/base-binding-sweep.py:2-24` (re-derives each receipt's base binding; no execution), `tools/round-34/replay-gate.py` | adj. |
| tsukuroi | `tools/recheck-*.sh` (`recheck-registry-r61.sh:1-14` etc.) — re-check live registry rows, `match|drift` per row | adj. |
| chousa | `corpus/evidence/round63/controls/run-exhibit-receipts.py:2-8` — runs exhibit receipts for one battery | adj. |
| audio, game-dev-2d, game-dev-3d, kagi, kasegi, lore, mori, tabi | — | — |

---

## 3. Rulings

**No duplicate exists in any lane for any of the three instruments.** Each ruling names the nearest
mechanism and the property that separates it.

1. **C1 vs the fleet.** `PROTOCOL.md:375` §Gate standard is the fleet-wide standard and **protocol
   owns it**; its `Registry` bullet (`PROTOCOL.md:398`) fixes the home ("a child lane's *registry
   home* is its own `SKILL.md`") and the eight row fields, and its `Delivery` bullet
   (`PROTOCOL.md:418`) makes a registry row a closure condition ("closure grades no gate conformant
   until its registry row exists"). The standard requires the **row**, not the script's existence.
   R82-C1 adds three predicates the standard does not carry: (i) a universe **derived from
   claim-bearing documents at a pinned revision** (not from the registry and not from a path
   pattern), (ii) a `support-module` exclusion **proved from the file's own bytes** (no `argparse`,
   no `__main__`), (iii) the reverse direction over the **entry cell** of every row.
   → **adjacent-but-different** to tabi (near), tsukuroi, kama, kotoba, mori, kake. The script-exists
   reverse direction is fleet *practice* (tabi `e3`, tsukuroi `REGISTRY-ROW-ORPHAN`, kama
   `missing-path`), never fleet *text*; C1 may cite it as precedent, and must not claim it as new.
2. **C2 vs the fleet.** `kumitate-shokunin/scripts/routed-ledger.mjs` (round 68) is the most complete
   lane instance: every routed section of every spot-check, one ledger row per item, quote binding,
   and a closed/wontfix row that must bind `path:line` + a quote at that exact line. Kengaku's
   difference is the **binding surface and the sensitivity leg**: JSONL rows whose `close` artifact's
   bytes must carry the id **and** the row's `evidence_literal`, plus a `check` that must fail when
   the repair is reverted to BASE. `rg -ln --glob '*.py' -e 'revert'` over the whole fleet,
   excluding kengaku and the wave/report/fixture trees, returns **no lane gate** (only
   `research/round-18-kimi-model-routing/...`, a domain script tree, is a false positive); the same
   probe over `.mjs`/`.sh`/`.js` returns only `scripts/hyaku/jj-lane.sh` (the fleet driver, not a lane
   gate), and `rg -e 'fails when reverted|revert.*base|reverted to'` over every sibling `.py`/`.mjs`
   returns nothing.
   → **adjacent-but-different**; the sensitivity leg is genuinely new.
   **Absorbable (this lane may adopt, cheaply):** kumitate's (i) "every routed section, not only the
   first" (a file with two routed sections must contribute two — a real loss class for any counter
   that reads only the first heading), (ii) `ROW_CONTRADICTED` (no `(round,item)` with two non-open
   rows), (iii) quote ≥ 3 words and unique within its section. These are hardening rules for
   `plans/round82_c2_checks.py`, not a second gate.
3. **C3 vs the fleet.** `unrunnable`, and the three-class vocabulary, appear in **no** sibling file:
   `rg -n --glob '*.py' -e 'unrunnable' -e 'reproduced' -e 'diverged' .` (fleet root, kengaku
   excluded) returns zero lane hits. `HISTOGRAM` outside kengaku appears only as a wave-spec
   requirement line (`kotodama-shokunin/.ufo/waves/round-64/gen-w1.py:200`), never as an emitted
   line from a gate. The nearest analogues are tameshi (`registry-check` per-row replay with expected
   outcome, two classes) and souji (`gate-replays` projection multiset, one instrument at five revs).
   → **adjacent-but-different**. C3's novel predicates: a **frozen map** (26 members, instrument +
   argv + receipt), the **projection reused from the receipt** with `diverged:<n>` counted in
   projection lines, a third `unrunnable:<code>` class, `COMMAND` equality against the reconstructed
   argv, and staged writes. Its two-runs-agree leg has a direct fleet precedent
   (`kumitate/scripts/counter-rerun.mjs:4-14`) — cite it as prior art, do not present determinism as
   new.
4. **Name overloading, not overlap.** "registry" in this fleet names at least three different
   objects: the SKILL.md gate table (C1's object), the Windows registry read plane
   (`tsukuroi-shokunin/tools/recheck-registry-r61.sh:1-8`, `S262` = `sc.exe query`), and the SOURCES
   registry (`chousa`'s instrument rows). A similarity search on the word alone produces three false
   positives; the mechanism, not the name, is the unit.

---

## 4. SOURCES ids and the URL question

**Ids are lane-scoped; no collision is possible, and none was found.** Kengaku's registry ends at
S261 (`corpus/SOURCES.md:276-277`) and contains **no** S262+ row:
`rg -n 'S26[2-9]' corpus/SOURCES.md plans/` → no match. Eight sibling lanes already carry an S262 whose
content is unrelated to each other and to anything kengaku would write:

| lane | path:line | S262 is |
|---|---|---|
| kaidoku | `kaidoku-shokunin/corpus/SOURCES.md:179` | `gitrevisions` docs (revision spelling) |
| kake | `kake-shokunin/corpus/SOURCES.md:152` | Google canonicalization doc |
| kotodama | `kotodama-shokunin/corpus/SOURCES.md:291` | quai Branly hybridity article |
| mori | `mori-shokunin/corpus/SOURCES.md:243` | ROMA OOM paper (OpenAlex abstract) |
| revenger | `revenger-shokunin/corpus/SOURCES.md:277` | Il2CppInspectorRedux README |
| souji | `souji-shokunin/corpus/SOURCES.md:222` | `symlink(2)` man page (rejected) |
| tameshi | `tameshi-shokunin/corpus/SOURCES.md:137` | flaky-test reruns paper |
| tsukuroi | `tsukuroi-shokunin/corpus/SOURCES.md:271` | `sc.exe query` Learn page |

Consequence for this round: if C2's V2 repair takes the contract-clean shape (§5), it consumes
**kengaku S262** and that is safe — the number is free in this lane's namespace and carries no
cross-lane meaning. The real hazard is the opposite: a **fleet-scoped** file citing a bare id is
ambiguous today — `.ufo/l0-questions.md:141` ("mori | round-42 | … (S262, ROMA/TSC)") and
`.ufo/l0-questions.md:247` ("tsukuroi | round-57 | … S266/S262's documented sentence") both prefix the
lane, and that is the convention that must hold.

**URL.** Round 82 opens no URL: `rg -n 'https?://' plans/round-82-claims.md plans/round82-sweep-map.json`
→ no match, and `rg -c 'https?://' plans/grader-population-ledger.json` → no match (88 members, all
offline instrument descriptions). So no URL collision is possible. The round's only live URLs are
inherited from S260/S261 (the pinned `2fd12b88` Terminal-Bench tree); no sibling cites them
(`rg -n 'log-summary-date-ranges|vulnerable-secret' --glob '*.md' --glob '*.json' .` outside kengaku →
no lane hit; the only hits are `MANIFEST.json` entries describing kengaku's own rounds).

---

## 5. Contradiction found while checking §4 — R82-C2 V2 vs the lane's own Q34

This is not a sibling overlap; it surfaced from the id/URL probe and it can decide C2, so it is
recorded with its evidence rather than smoothed.

**Measurement (my own, independent of the C2 seats; same numbers they report).** Extracting the two
rows and splitting the quoted spans on whitespace:

```sh
python3 - <<'PY'   # in-process read of corpus/SOURCES.md at the tip
lines = open('corpus/SOURCES.md').read().split('\n')
for i,l in enumerate(lines,1):
    if l.startswith('| S260 ') or l.startswith('| S261 '):
        for c in [x.strip() for x in l.strip('|').split('|')]:
            for q in __import__('re').findall('“([^”]+)”', c):
                print(i, len(q.split()), q[:80])
PY
276 7 # tb2 log-summary-date-ranges grader probe (round 81)
277 12 Write a CSV file /app/summary.csv with the following structure (including the header):
277 13 The goal is to extract this secret key and save it to /app/results.txt.
```

The rows state 9 / 14 / 17. The receipt layout is

```sh
nl -ba corpus/evidence/round81/log-summary-date-ranges-probe.txt | sed -n '1,16p'
1  # tb2 log-summary-date-ranges grader probe (round 81)
2  MEMBER log-summary-date-ranges
…
14 MINTED_BY_SHA eb6297f6…
15 OBSERVATIONS_BEGIN
16 CASE exact-15-rows predicted=P observed=P rc=0 legs=PP violates=-
```

so the stamp block is 2-14 and observations start at 16, where S260 states `:1-17 (subject at 1, stamp
2-16, observations from 17)`. The counts live in cell 5 = the **`anchor`** column (header
`corpus/SOURCES.md:20`: `| id | source | kind | tier | scope | anchor | teaches | status | opened |
recheck | used-by |`).

**Two frozen rules forbid the in-place fix that the C2 scribe's §2.4 specifies.**

- `corpus/QUALITY.md:761` (**Q34**, lane criterion, frozen round 42): "every cell of a
  `corpus/SOURCES.md` registry row except `status`, `recheck` and `used-by` is immutable under its id:
  a correction lands as a NEW row whose `teaches` cell opens `supersedes S0NN —`, and an in-place
  change is a rule-2 defect **even when the round wrote the row itself and the cell it corrects is its
  own anchor**." This round's case is the anticipated case, verbatim.
- `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:48-50` (fleet-frozen authority, restated at
  `CORPUS.md:116-118`): "Only `status`, `recheck` and `used-by` change in place … A correction is a
  new row whose `teaches` opens `supersedes S0NN —`." `PROTOCOL.md:435` binds the lane to it.

Lane practice agrees with the rule: the 15 correcting rows (`S064←S054`, `S067←S066`, `S068←S061`, …)
are all **new** rows whose `teaches` opens `supersedes`.

**The two horns, stated and not resolved here.**

- *Horn A (in-place).* Patch `corpus/SOURCES.md:276-277` anchor cells → V2's frozen sentence becomes
  literally true, and the edit is a rule-2 defect under Q34 and the fleet contract. My first pass said
  "nothing catches it"; **that was too broad and I correct it here from a run, not from reading.** The
  append-only-by-history checker is still absent (`plans/sources_appendonly.py`; the only copy is
  `.ufo/waves/round-42/build/R42QualityDraft/sources_appendonly.py`), but a different Q34 gate is
  landed: `plans/anchor_line_check.py` — referenced 4×/2×/1× by SCORECARD/LOG/corpus/README at BASE
  (so inside R82-C1's universe) and registered in `SKILL.md` at the tip. It enforces the supersede-chain
  reading plus the `len(quote.split())` word rule, and at the tip it prints

  ```
  $ PYTHONDONTWRITEBYTECODE=1 python3 -B plans/anchor_line_check.py --lane .
  ANCHORLINE rows=253 cited=72 captured=64 uncaptured=8 defective=10 repaired=10 live=0 cells=0
  rc=0
  ```

  It is green **because it cannot see these two rows**: `QUOTE_RE` (`plans/anchor_line_check.py:67`)
  requires `:<N> "<straight-quoted>" (<K> words)` and `SHA_RE` (`:70`) requires a `sha256 <64 hex>`
  capture; S260/S261 write curly quotes and carry no `sha256` token, so they fall outside `cited=72`.
  An in-place edit of the two anchor cells would therefore still pass every gate in the round. But the
  same run prints **10 `state=repaired` rows** (`S108←S157`, `S150←S159`, `S151←S160`, `S152←S161`,
  `S153←S162`, `S154←S163`, `S155←S164`, `S201←S213`, `S221←S222`, `S149←S158`): supersede-chain repair
  is the lane's operational shape, not a proposal.
- *Horn B (superseding row).* Add kengaku S262 (`supersedes S260 —` / `S261 —`, restating 7/12/13 and
  `:1-15`/2-14/16) → satisfies Q34 and the fleet contract. It makes V2 true under the "registry's
  newest statement per id" reading, which is exactly the reading `anchor_line_check.py` already
  operationalises; V2's frozen sentence names S260/S261's own bytes, so under a literal reading it
  stays false. The residual is therefore a **reading**, not an unstated lane practice.

Either horn needs the L1/integrator to rule, because re-freezing a predicate is barred by the round's
own rules ("Never re-open a frozen predicate, universe rule, control or kill rule"). I have messaged
`C2ProseR82`, `C2RepairR82`, `C2CounterR82` and `Main` with the evidence; I edited nothing.

Second-order effect worth recording beyond this round: Q34 has two legs and only one is enforced. The
**row-shape** leg (a correction is a new superseding row; word/line/range of a shaped anchor) is landed
in `plans/anchor_line_check.py` and green at the tip. The **history** leg ("an in-place change is a
rule-2 defect"), which is the leg an in-place edit of S260/S261 would trip, is the one the criterion
itself calls "written twice and enforced nowhere" (`corpus/QUALITY.md:764`) and is still a draft under
`.ufo/waves/round-42/build/`. A round that lands the 16th in-place victim would lengthen that red list
while every gate stays green — and the two V2 rows, written in curly quotes without a `sha256` capture,
are exactly the shape the green gate cannot see. That is the calibration surface, not the coverage
surface.

---

## 6. What `PROVINCE.md` adjacency (9, held) should record this round

**A routing line, not a score move.** Current reading: the round-81 scores block carries
`adjacency **9** (held; the connector's sibling scan is the wave's evidence)` at `SCORECARD.md:3855`
(the same convention at `:3496`, `:3606`, `:3662`, `:3791`; the last literal `| adjacency | 8 |` table
rows are `:632`, `:699`). Nothing this round was arbitrated by an owner, and PROVINCE's own
`### Adjacent` table (`PROVINCE.md:151-161`) already names **protocol / aggregator** as
the owner of "a fleet-wide preregistration/replay-gate standard … referred round 11/12-14, not
imposed". That referral now has a concrete object: `PROTOCOL.md:375` §Gate standard and
`PROTOCOL.md:398` (registry home = lane SKILL.md). So the rule ("evidence sent, not absorbed") is
already satisfied by an existing owner; **no bump**, and no new owner is needed.

The routing line to add to `PROVINCE.md` §Adjacent (or to the round report's report-out list, if the
L1 prefers not to touch PROVINCE for a non-claim round) carries four payloads:

1. **protocol** — the round's three counters are instances of `PROTOCOL.md:375` §Gate standard, and
   C1's derived universe + bytes-proved `support-module` exclusion are *extensions* the standard does
   not state; the two fleet hardening rules that C2 should absorb (`routed-ledger.mjs:13-18`: every
   routed section, `ROW_CONTRADICTED`) and one that C3 already cites (`counter-rerun.mjs:4-14`:
   repeat-run agreement) come from kumitate, not from a standard.
2. **protocol** (second payload, the sharp one) — the V2/S260-S261 repair collides with
   `SOURCES-CONTRACT-v1.md:48-50`, and this lane's Q34 (`corpus/QUALITY.md:761`) enforces only its
   row-shape leg (`plans/anchor_line_check.py`, green at the tip) while its history leg stays a draft.
   The ask is narrow: confirm that a superseding row is the contract's "current statement" for an id
   (the reading the landed gate already implements) and rule whether the history leg should land. The
   contract is not amended by this lane.
3. **kumitate** — evidence that its `routed-ledger` shape is the closest fleet analogue and that
   kengaku's routed rows differ in binding surface (JSONL + `evidence_literal` + revert sensitivity);
   sent so kumitate's next revision does not treat the two as the same object.
4. **tabi** — evidence that its `check-gate-registry` `e1/e2/e3` scheme is the closest fleet analogue
   to C1 and that kengaku's C1 is a second, differently-derived instance; sent so the two lanes do not
   converge on incompatible row grammars silently.

No id is consumed, no URL is claimed, no scope moves. This is the "routing line" option, and it is
what I recommend.

---

## 7. One bounded proposal

**Make V2's repair visible to the gate the lane already runs.** Two new rows S262/S263 written in
`plans/anchor_line_check.py`'s own grammar — straight-quoted quote, a `sha256 <64hex>` capture token,
`teaches` opening `supersedes S26N —` — so the word/line/range legs V2 needs are covered by a landed,
already-green gate instead of by another new counter. Measured at the tip: `ANCHORLINE rows=253
cited=72 captured=64 uncaptured=8 defective=10 repaired=10 live=0 cells=0` (rc 0). One limit has to be
stated in `u2` rather than assumed: the gate cannot fail when a row is *deleted* (`live=0` persists), so
V2's revert-sensitivity leg must assert the two rows' presence, their `supersedes` prefix, and exit 0
with no `ROW S262`/`ROW S263` defect line. That assertion is the check; the gate supplies the
word-count leg. Landing the history leg (`plans/sources_appendonly.py`) is a separate optional ask, and
it is outside my write scope either way — this is a recommendation to the L1, not an edit.

- **Built bytes already carry this shape.** `plans/anchor_line_check.py` prints `state=repaired` for
  ten rows today (`S108←S157` … `S221←S222`), and `tameshi-shokunin/tools/defect-bind.py:2-8` /
  `kumitate-shokunin/scripts/routed-ledger.mjs:13-18` turn a prose close into a re-derivable row the
  same way. The still-prose leg is Q34's history rule, not its row shape.
- **Affected axes.** Calibration (C2) is protected: a repair that passes `u2` while breaking Q34 would
  score calibration on a contract violation. Coverage (C1) is untouched — Q34's object
  (`corpus/SOURCES.md`) is outside C1's universe, so the two claims stay causally separable.
  Freshness (C3) is untouched. Adjacency is unchanged in score and better grounded (the protocol
  routing line above).
- **Why not "fix V2 in place":** that is Horn A in §5, and it is the one action the round's own
  criteria name as a defect.

---

## 8. Risks

1. **Negative evidence is bounded.** "No sibling owns X" holds for the search surface in §1. A gate
   that implements the mechanism without naming it in its first 3 000 bytes is invisible. The tag
   `near` above means "same mechanism, different universe"; anything I marked `—` could still have a
   sibling gate I did not read.
2. **Sibling tips move.** I read each lane's working tree, not a pinned revision: a sibling gate added
   after this scan is not covered. Kengaku's own measurement is pinned (`12f1029a`).
3. **`unrunnable` is a vocabulary claim, not a mechanism claim.** Another lane could run an
   equivalent sweep with two classes and different words; tameshi's `registry-check` is exactly that
   shape. C3 should cite it as prior art.
4. **The Q34 finding is a reading of two frozen texts, not an arbitration.** If the integrator rules
   that a quote-count correction inside the `anchor` cell is not a "correction" under rule 2, Horn A
   opens and my §5 routing payload 2 is moot. I state the texts; I did not decide them.
5. **This report recommends, it does not land.** Everything in §7 needs an L1 action outside my write
   scope.

---

## 9. What I attacked, and what I could not break

- **Attacked:** the assumption that R82-C1 is new. It is not entirely: tabi (`e3`), tsukuroi
  (`REGISTRY-ROW-ORPHAN`), kama (`missing-path`) and kake's c74 all check that a registry entry names
  an existing script. **Could not break** the narrower novelty: none derives its universe from
  claim-bearing documents, and none verifies a support-module exclusion from the file's own bytes
  (no `argparse` **and** no `__main__`).
- **Attacked:** the assumption that R82-C2's routed-row shape is new. kumitate's `routed-ledger` and
  tameshi's `defect-bind` already bind spot-check items to ledger rows. **Could not break** the
  novelty of the revert-sensitivity leg — no lane gate in the fleet carries one.
- **Attacked:** the assumption that R82-C3's sweep is new. tameshi replays a whole registry per row,
  souji compares a projection multiset at five revs, kumitate polices repeat-run determinism.
  **Could not break** the novelty of a frozen 26-member map + three-class classification + histogram;
  no sibling emits `unrunnable`.
- **Attacked:** the SOURCES id question from both directions (id ownership, URL reuse). **Could not
  break** lane-scoping: eight S262 rows with eight different sources is conclusive. **Could not find**
  any sibling citing the round-81 Terminal-Bench URLs.
- **Attacked:** the round's own C2 numbers, expecting the seats to be wrong. They are right (7/12/13,
  stamp 2-14, obs 16) — and the *repair shape* they propose is the thing that fails, against the
  lane's own Q34. That is the finding I did not expect and could not break.
- **Did not attack, by rule:** the frozen predicates, the universes, the controls, the kill rules, and
  any sibling's committed bytes.

---

## 10. Corrections to this report after peer contact (audit trail)

Two items changed after the first write; both are stated so the L1 reads the corrected version, not the
first one.

1. **"The Q34 checker is not landed" was too broad.** `C2ProseR82` pointed at
   `plans/anchor_line_check.py`; I read it and ran it read-only at the tip
   (`PYTHONDONTWRITEBYTECODE=1 python3 -B plans/anchor_line_check.py --lane .` →
   `ANCHORLINE rows=253 cited=72 captured=64 uncaptured=8 defective=10 repaired=10 live=0 cells=0`,
   rc 0). It is landed, it is referenced by all three claim-bearing documents at BASE (SCORECARD 4×,
   LOG 2×, `corpus/README.md` 1×, so it is inside R82-C1's universe), and it enforces Q34's
   supersede-chain reading plus the `len(quote.split())` rule. What stays true: it cannot see S260/S261
   (curly quotes, no `sha256` capture token — `QUOTE_RE` at `:67`, `SHA_RE` at `:70`), and Q34's
   history leg is still a draft. §5 and §7 now carry the corrected statement.
2. **Worktree state at my last reading** (measured, because it decides whether any C2 receipt can
   honestly stamp `WORKTREE clean`): `git status --porcelain` →
   `M SKILL.md`, `?? .ufo/waves/round-82/`, `?? corpus/evidence/round82/census-before.txt`,
   `?? corpus/evidence/round82/fetch/`. `SKILL.md` is another seat's in-flight registry edit, not mine.
   A `WORKTREE clean` receipt (V1) minted here would be false; it must come from a clean
   `git clone --shared` of `12f1029a`. I sent this to `C2RepairR82` (whose seat owns V1); the harness
   later reported that peer's wake turn exhausted five 429 retries, so the durable copy of this blocker
   is the one in my message to `Main`, not the peer message.
3. **One count that will move.** `plans/anchor_line_check.py` prints `rows=253`, matching
   `PROVINCE.md:1041`'s `rows=253` cell. Landing S262/S263 makes it 255; that PROVINCE cell is an
   integrating-seat edit (the L1 or the C2 seat), not mine.
4. **Horn A is no longer hypothetical: it is in the worktree, uncommitted, as of 06:51.** The exact
   bytes another seat left in `corpus/SOURCES.md` are the in-place form of §5:

   ```
   $ git diff --stat corpus/SOURCES.md
    corpus/SOURCES.md | 4 ++--
   $ git diff -U0 corpus/SOURCES.md
   -S260 … :1-17 (subject at 1, stamp 2-16, observations from 17); quote … (9 words, line 1)
   +S260 … :1-15 (subject at 1, stamp 2-14, OBSERVATIONS_BEGIN 15, observations from 16); quote … (7 words, line 1)
   -S261 … (14 words); vulnerable-secret/instruction.md:1 … (17 words)
   +S261 … (12 words); vulnerable-secret/instruction.md:1 … (13 words)
   ```

   With those bytes in place I re-ran the landed gate, and it stays green while seeing nothing:

   ```
   $ PYTHONDONTWRITEBYTECODE=1 python3 -B plans/anchor_line_check.py --lane .
   ANCHORLINE rows=253 cited=72 captured=64 uncaptured=8 defective=10 repaired=10 live=0 cells=0
   (zero `ROW S260` / `ROW S261` lines)
   ```

   So the round's own Q34 defect can land while every gate in the round prints clean — the exact
   invisibility §5 predicted, now measured rather than argued. I escalated the diff and the gate output
   to `Main` and to `C2ProseR82` (whose revised yield says it adopted the superseding-row shape, so the
   worktree and its report disagree). I changed none of these files; my only write is this report.
5. **No *product* artifact carries `R81-V2` at this reading, and the lesson edit is counts-only.** My
   first run of this check omitted `--hidden`, so it silently skipped `.ufo/`; `C2ProseR82` caught the
   scope error and this is the corrected measurement:

   ```
   $ rg -ln --hidden 'R81-V2' kengaku-shokunin
   kengaku-shokunin/.ufo/waves/round-82/w1/C2ProseR82.md
   kengaku-shokunin/.ufo/waves/round-82/w1/ConnectorR82.md
   $ git diff -U0 corpus/lessons/round-81.md
   -… (14 words); …            +… (12 words); …
   -… (17 words);              +… (13 words);
   ```

   Only the two seat reports carry the id; no product surface does (no §Corrections block in the
   lesson, no S262/S263 row, no `routed-findings.jsonl` row). The counts are corrected in the worktree,
   so C2's `close`-carries-the-id leg cannot pass until a tracked repair artifact carries `R81-V2`. The
   same correction applies to my three novelty probes: re-running them with `--hidden` changes nothing
   (`unrunnable` → no sibling hit; `revert` → only `research/round-18-…` domain scripts and
   `scripts/hyaku/jj-lane.sh`), so §3's rulings hold with `.ufo/` included, not just excluded.

---

## 11. Evidence index (every command above, in order of first use)

| # | command | what it establishes |
|---|---|---|
| 1 | `git -C kengaku-shokunin rev-parse master` (twice) | tip `12f1029a…`, unchanged across the seat |
| 2 | lane walk over `.py`/`.mjs`/`.sh` headers, exclusions per §1 | the three per-lane mechanism tables |
| 3 | `rg -n --glob '*.py' -e unrunnable -e reproduced -e diverged .` (kengaku excluded) | zero lane hits: C3's vocabulary is new |
| 4 | `rg -ln -e revert` over sibling `.py`, then `.mjs/.sh/.js`; `rg 'fails when reverted\|revert.*base\|reverted to'` | no sibling gate has a revert-sensitivity leg |
| 5 | `rg -n '^\| *S262 ' */corpus/SOURCES.md` | eight lane-local S262 rows, eight different sources |
| 6 | `rg 'https?://'` over claims/map/ledger | round 82 opens no URL |
| 7 | in-process extraction of S260/S261 cells | 7 / 12 / 13 words against stated 9 / 14 / 17 |
| 8 | `nl -ba corpus/evidence/round81/log-summary-date-ranges-probe.txt` | MEMBER 2, MINTED_BY_SHA 14, OBSERVATIONS_BEGIN 15, first CASE 16 |
| 9 | `rg -n 'Q34 —' corpus/QUALITY.md`; `sed -n '48,50p' …SOURCES-CONTRACT-v1.md` | the two frozen append-only rules |
| 10 | `rg -n '^- \*\*Registry\.\*\*…' PROTOCOL.md`; file-contract row | protocol owns the standard (`:398`, `:418`, `:435`) |
| 11 | `PYTHONDONTWRITEBYTECODE=1 python3 -B plans/anchor_line_check.py --lane .` (twice: pre- and post-edit bytes) | `live=0`; the Q34 gate is landed, and blind to S260/S261 |
| 12 | `git status --porcelain`; `git diff -U0 corpus/SOURCES.md` | the worktree carries the in-place edit and three other seat edits |
| 13 | `rg -n 'rows=253' PROVINCE.md`; `grep -cE '^\|…S[0-9]{3,}…\|' corpus/SOURCES.md` | 253 rows; the PROVINCE cell that moves to 255 |
