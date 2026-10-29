# W2MutC2 — mutation test of the frozen R52-C2 counter (wave 2, falsify)

Seat: W2MutC2 (mutation-tester, leaf). Judged on: operability. Read-only against the lane; every mutant is a scratch copy.

## Verdict

- **Attack partly landed.** The frozen counter's own guard is weaker than its predicate. Of 9 mutants, the frozen control set (K0–K4, as written in the claim) kills **7**. Two survive it: **M4** (registry extraction swallows SKILL.md) and **M5** (ENTRY-MISSING leg dropped). Each is killed only by a control I added (K5, K7). The counter's own `--selftest` kills **0 of 9**.
- **One counting hole in the frozen parser** (not a mutant; measured on the unmodified counter, M0): a registry row whose verdict map contains an escaped `\|` is silently dropped. A blank owner cell in that row passes `PREDICATE R52-C2 pass`.
- **The landed tip verdict is unchanged by these attacks.** The frozen counter on the committed tip prints `PREDICATE R52-C2 pass` (M0 = frozen file, sha256 `b9ce9439…b600`). The hole above means one registry row (SKILL.md line 609, `gate-flip-check`) is not checked by any leg, so "every registry row is complete" is verified for 74 of 75 data rows, not 75 of 75.

## Subject and scope

- Counter: `plans/round52_c2_registry.py`, lane tip `87301ba` (sha256 `b9ce943978434492ca68cdbdbc7ba047ae2b711726e5bf206d52817d0250b600`), identical to the file in the lane working tree.
- Base: `30801b47`. Tip: `87301ba`. Both read via `git archive` into scratch.
- Lane tree, fleet repo, sibling lanes, `.ufo/state/`, `templates/`, `scripts/` and `MANIFEST.json`: not written. No git mutation, no install.
- Scratch: `/fast/scratch/hyaku/kengaku-r52/w2-W2MutC2/` (removed before yield; receipts kept below).

## Commands run

```
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD            # 87301bacca90c03fa915716fbe6d7023762c5ab3
git -C <lane> archive HEAD    | tar -x -C <scratch>/tip                         # read-only
git -C <lane> archive 30801b47 | tar -x -C <scratch>/base                       # read-only
python3 <tip>/plans/round52_c2_registry.py --lane <tip>                         # baseline
python3 <tip>/plans/round52_c2_registry.py --lane <base>                        # baseline
python3 build_controls.py                                                       # scratch: builds K2..K7 symlink-mirror trees, SKILL.md overridden
cp tip/plans/round52_c2_registry.py mut/M{0..9}.py ; edit one line/block per copy (see table)
for m in M0..M9; for c in tip base K2 K3 K4 K5 K6 K7; do python3 mut/$m.py --lane <tree>; done
for m in M0..M9; python3 mut/$m.py --selftest --lane <tip>                      # TMPDIR=<scratch>/tmp
```

## Controls

Frozen (from `plans/round-52-claims.md` §C2) — all reproduced by M0:

| id | tree | expected | measured (M0) |
|---|---|---|---|
| K0 | tip (`87301ba`) | pass | `ADVERTISED 72`, `REGISTERED 72 rows=74`, all legs 0, `PREDICATE pass` |
| K1 c2-control-nothing | base (`30801b47`) | `MISSING 28` | `MISSING 28`, `PREDICATE fail` |
| K2 c2-control-empty-cells | tip, the 28 new rows with cells 4–8 blanked | `INCOMPLETE 28` | `INCOMPLETE 28`, `PREDICATE fail` |
| K3 c2-control-drop-row | tip minus `round28-census` row | `MISSING 1` | `MISSING 1`, `PREDICATE fail` |
| K4 c2-control-false-selftest | tip, `defect-ledger` self-test cell claims `--selftest` (script has none) | `SELFTEST-UNBACKED 1` | `SELFTEST-UNBACKED 1`, `PREDICATE fail` |

Added by this seat (not frozen; clearly extra):

| id | tree | measured (M0) | what it probes |
|---|---|---|---|
| K5 decoy-table | `round28-census` row moved into a different `## ` section | `MISSING 1`, `PREDICATE fail` | registry extraction is scoped to the registry section |
| K6 escaped-pipe-blank | owner cell of SKILL.md line 609 (`gate-flip-check`, verdict map contains `\|`) blanked | **`PREDICATE pass`** (rows=74 of 75) | parser drops the escaped-pipe row |
| K7 entry-missing | extra row `ghost-tool` with entry `python3 plans/ghost_tool.py` | `ENTRY-MISSING 1`, `PREDICATE fail` | the ENTRY-MISSING leg; no frozen control exercises it |

## Mutant table

Kill = predicate verdict on a control differs from the frozen counter's verdict on that same control (M0).

| id | mutation (one-line, on a copy) | frozen controls K0–K4 | added controls | `--selftest` | verdict |
|---|---|---|---|---|---|
| M1 | `CMD` → `python3 ([A-Za-z0-9_./-]+)` (advertised = any path token after `python3`) | K0 **fail**: `ADVERTISED 79`, `MISSING 6` (`plans/fixtures/r26/perturb_oracle.py`, `plans/fixtures/r28/acceptance.py`, `plans/fixtures/r29/mutation_witness.py`, `corpus/evidence/round11-power/recompute_r11.py`, `corpus/evidence/round12-ladder/recompute_r12.py`, `corpus/evidence/round9-fleet/test_harness.py`) | — | 3/3 ok (survives) | **killed by K0** (landed tip) |
| M9 | `CMD` → `([A-Za-z0-9_./-]+\.[a-z]+)` (any file with an extension, anywhere) | K0 **fail**: `ADVERTISED 493`, `MISSING 420` | — | 3/3 ok | **killed by K0** |
| M2 | `ok` drops `incomplete` | K2 **pass** (expected fail; `INCOMPLETE 28` printed, predicate pass) | — | 3/3 ok | **killed by K2** |
| M3 | `SELFTEST-UNBACKED` needs exactly two scripts (`len(scripts) != 2`) | K4 **pass** (expected fail) | — | 3/3 ok | **killed by K4** |
| M4 | `registry_block` returns the whole file (`return text`) | K0–K4 identical to M0 | K5 **pass** (expected fail; decoy row counted, `MISSING 0`, `REGISTERED rows=75`) | 3/3 ok | **survives frozen; killed by K5 (added)** |
| M5 | `ok` drops `entry_missing` | no frozen control has an ENTRY-MISSING row; K0–K4 identical to M0 | K7 **pass** (expected fail; `ENTRY-MISSING 1` printed) | 3/3 ok | **survives frozen; killed by K7 (added)** |
| M6 | delete the A3 negation guard (`\bno\b…--flag` → return False), lines 74–75 | K0 **fail**: `SELFTEST-UNBACKED 1` (`order-check`) — the A3 false positive reappears on the landed tip | K4 fail (2 unbacked) | 3/3 ok | **killed by K0** |
| M7 | drop the existence filter on the advertised set | K0 **fail**: `ADVERTISED 76`, `MISSING 4` (`plans/round48_c1_verify.py`, `round48_c2`, `round49_c1`, `round49_c2`; these are `SUPERSEDED … -> never-landed` pointers at SCORECARD.md:2154–2157, so the filter is load-bearing) | — | 3/3 ok | **killed by K0** |
| M8 | `selftest_unbacked` always `False` | K4 **pass** (expected fail) | — | 3/3 ok | **killed by K4** |

Totals: frozen controls kill **7/9** (M1, M2, M3, M6, M7, M8, M9 — M1/M6/M7/M9 only through the landed-tip pass control, not a dedicated negative). Frozen controls miss **M4 and M5**; the added controls K5 and K7 kill them. `--selftest` kills **0/9**: every mutant still prints `SELFTEST cases=3 failures=0`.

Full matrix: `receipts/matrix.txt`. Per-run outputs: `receipts/out/`. Diffs: `receipts/M*.diff`.

## Findings (what the attacks show)

1. **The four frozen controls do not exercise the ENTRY-MISSING leg.** M5 (drop it from `ok`) passes all four. The claim's control table therefore cannot fail a counter that ignores a whole leg. K7 is the minimal control that does.
2. **Registry extraction is unguarded.** M4 (swallow the whole SKILL.md) is equivalent to M0 on the landed tip because SKILL.md has no other 8-cell table, and it passes all four frozen controls. It is a latent defect: K5 shows a non-registry table can hide a missing instrument.
3. **`--selftest` tests the collected lists, not the verdict.** Its three cases assert on `collect()` output (`missing`, `incomplete`, `unbacked`) and never call `verdict()`. So a dropped `ok` term (M2, M5) is invisible to it, and it has no fixture for SELFTEST-UNBACKED, the A3 negation guard (M6), the ADVERTISED depth bound (M1/M9), or ENTRY-MISSING (M5). These are guarded only by the landed-tip pass (M1, M6, M7, M9) or by no control at all.
4. **Escaped-pipe row dropped (counter-level hole, measured on M0).** `parse_rows` splits on every `|` and keeps only rows that yield exactly 8 cells. SKILL.md line 609 (`gate-flip-check`, `--lesson <path>` row, verdict map containing `\|`) yields 9 cells and is dropped. Measured: registry table has 75 data rows; counter reads `rows=74`. K6 (owner cell blanked) → `PREDICATE pass`. The same name also appears on line 614 (`gate-flip-check`, a second row for the same script), so the dropped row is a duplicate name the counter cannot see either (round-51 D3's duplicate-id class). Impact: INCOMPLETE and SELFTEST-UNBACKED cannot fire on that row.
5. **Existence filter is load-bearing and correct.** M7 shows the four stale advertised names are pointers recorded as `SUPERSEDED … -> never-landed` (SCORECARD.md:2154–2157). The frozen rule `(a) exists at the tip` is what keeps them out.

## Suggested fixes (not applied — lane is out of this seat's write scope; for the L1 and a follow-on amendment)

- Add K5, K6 and K7 (and an A3 negated-cell fixture plus a `plans/fixtures/` depth fixture) to the counter's `--selftest`, and make the selftest call `verdict()` rather than `collect()` so the `ok` expression is exercised.
- Split rows on unescaped pipes (`(?<!\\)\|`) and unescape `\|` before counting cells, so the escaped-pipe row is counted.
- Any change to the frozen counter or its control set is new text under an append-only amendment; the current scored after-run is not re-set by this seat.

## Receipts (kept under the wave report dir)

- `receipts/build_controls.py` — builder for K2–K6; `receipts/build_k7.py` — builder for K7 (both ran unchanged in scratch)
- `receipts/matrix.txt` — mutant × control predicate matrix and selftest lines
- `receipts/out/` — per-run outputs
- `receipts/M1.diff` … `receipts/M9.diff` — mutation diffs against the frozen counter
- `receipts/sha256.txt` — digests of the frozen counter and M0

## Tooling

No installs or upgrades. Used `python3`, `git archive`/`git rev-parse` (read-only), `cp`, `diff`, `grep`.
