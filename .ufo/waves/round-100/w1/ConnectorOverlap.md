# ConnectorOverlap — round 100 (w1)

Seat: cross-lane scan + C1/C2 write-set disjointness + round-101 planning data-walk. No production
edits, no commits, no `task` calls. Every measurement below runs in one `git clone --shared` detached at
T `dbe0cefa607cf57f7f58346fce64bcc127144ca0` (scratch `/fast/scratch/hyaku/kengaku-r100/ConnectorOverlap`,
removed at exit); receipts in `.ufo/waves/round-100/w1/ConnectorOverlap/`.

Both frozen predicates were re-run at T from the clone and pass (receipts `c1-run-T.txt`, `c2-run-T.txt`):
C1 `L1..L13=pass`, `TARGET executed_rows=44 … defects=0`, `PREDICATE R100-C1 pass`; C2 `K1..K10=pass`,
`GATE defects base=33 ref=32 rev=23`, `PREDICATE R100-C2 pass`.

---

## (a) Cross-lane scan — both claims are lane-local, no collision

**A1 — no sibling lane replays `financial-document-processor` or any TB2 grader.** Fleet-wide
`grep -rl 'financial-document-processor|2fd12b88'` (excluding `.git/`) returns 47 hits outside
`kengaku-shokunin/`, and **none of them is a replay**: 33 are fleet-level `.ufo/reports/round-*/` files
(32 `kengaku.md`, 1 `souji.md`), one is the fleet `MANIFEST.json`, and the remaining 13 are other lanes'
connector seats *citing* kengaku's TB2 work in their own scans (kaidoku r41/r69/r87/r90, kake r92/r93).
Ten sibling lanes carry a `plans/` directory (kagi, kaidoku, kake, kama, kasegi, kotoba, mado, tabi,
tameshi, tsukuroi): **0** of them has a file under `plans/` matching `terminal-bench|tb2-|test_outputs.py`.
Receipt: `cross-lane-scan.txt`.

**A2 — no sibling lane binds SOURCES rows through `PROVENANCE.md`.** Seven `PROVENANCE.md` files exist
outside kengaku (kaidoku ×1, kake ×1, kama ×1, mado ×2, game-dev-3d ×2), all under `.ufo/waves/…` fixture
paths or a vendored knowledge tree; the only one containing an `S<id>`-shaped token is kaidoku's round-14
fixture, which uses its own `S`-id convention (`KaidokuR14.QuoteSourceFixtures`), not kengaku's. Every
kengaku-`S<id>`-bearing `PROVENANCE.md` in the fleet is kengaku's own (round-99/100 control fixtures plus
the three landed this round). R100-C2's three-cell form has no cross-lane borrower and no cross-lane
precedent to collide with.

Noted, not a defect: kengaku is already a cross-lane reference point — `kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/kengaku.json`
records a read of `plans/constraints_probe.py`, and `kake-shokunin/.ufo/waves/round-93/w1/ConnectorScope/receipts/sibling-scan.txt`
lists 14 kengaku hits including `S144`'s TB2 URL. So a change to kengaku's SOURCES rows is observable from
two other lanes; nothing in this round's write set touches a row those receipts cite (`S144` is untouched
by F..T).

Consequence: neither claim's evidence is duplicated or contested elsewhere in the fleet; the round's
findings below are all lane-internal.

---

## (b) C1/C2 write sets are disjoint — but the two claims interact through the gate's binding precedence

**B1 — write sets are disjoint at T, measured.** `git diff --name-status F..T` is exactly seven files
(`write-set-F-T.txt`):

| owner | paths |
|---|---|
| C1 | `M SKILL.md`, `M corpus/SOURCES.md`, `M plans/grader-population-ledger.json`, `A corpus/evidence/round100/fdp-probe.txt` |
| C2 | `A corpus/evidence/round52/PROVENANCE.md`, `A corpus/evidence/round58/PROVENANCE.md`, `A corpus/evidence/round94/PROVENANCE.md` |

Intersection empty. C1's `corpus/SOURCES.md` edit is a **pure append**: one hunk `@@ -357,0 +358,8 @@`,
0 deletion lines, 389→397 lines. The 23 gate findings at T sit at lines 193–316, so no finding's `loc`
shifts and no BASE row line moves — C2's K8 row-identity check is structurally insulated from C1's edit.

**B2 — the BASE→REF delta is a *masking*, not a binding (S295).** The exclusive gate prints 33 defects at
BASE and 32 at REF; the diff is **exactly one line** (`delta-BASE-REF.txt`):

```
< DEFECT S295 anchor token=- class=capture-unanchored
    detail=row-names-2-captures-1-anchor-token-none-resolves-capture-corpus/evidence/round53/pin-tree-2fd12b88.json
```

At BASE, S295 binds `by=row-path` to two captures (the round-52 grader and `round53/pin-tree-2fd12b88.json`);
its one anchor token resolves the grader and the pin-tree capture is unanchored. C1's P0 capture (pre-F)
adds `corpus/evidence/round100/tb2-financial-document-processor/` with a `task.toml`, so the row's TB2 URL
now binds `by=url-task`, `bind_row` returns **one** capture, and rule 3 (explicit lane path) is never
consulted. The finding disappears although the pin-tree capture is still unanchored.

Control **M2** (URL removed from S295's row at T, everything else at T): the finding returns,
`defects=24` (`M2-s295-url-removed.txt`). So the round's first cleared finding was **hidden, not bound**.

**B3 — the same precedence suppresses explicit locators lane-wide; the round moved 7 → 17 rows.**
`bind_row` returns the *first* route that yields a capture (provenance-row → upstream URL → explicit lane
path). Any `corpus/evidence/…` path a row also carries is then never examined. Census over
`anchor_digest_check.py --verbose` BIND lines (`locator-suppressed-census.py`,
`locator-suppressed-BASE-REF-T.txt`):

| revision | rows whose explicit `corpus/evidence/` path the gate never binds |
|---|---|
| BASE `78460376` | **7** (S205 S208 S209 S212 S230 S237 S336) |
| REF `5220b71d` | **8** (+S295) — C1's P0 capture |
| T `dbe0cefa` | **17** (+S210 S211 S219 S228 S232 S279 S281 S298 S344) — C2 +8, C1's new row +1 |

So C2's nine provenance bindings each silenced an explicit locator in eight of the nine rows, and C1
contributed two (S295, S344). This is a *second-order* effect of both claims: neither write set touches the
other's bytes, but each binding removes a locator from the gate's view.

**B4 — the obvious cheap repair is inert under the frozen gate.** S300's `abbrev-unresolved` token
`fa53d657…ab389` **is** the digest of a committed file —
`corpus/evidence/round94/graders/write-compressor/environment/main.rs`, sha256
`fa53d6572fca95903e30d2d953f1e428bb8b63513ff218ebee9bc60a425ab389` (measured). Naming that path in the row
(control **M3**) does **not** clear the finding: the row still binds `by=provenance-row` to
`solution/solve.sh` only, and the detail still reads `capture=…/solution/solve.sh`, `defects=23` unchanged.
The gate's rule 2 also joins the URL basename to the task directory, so a nested subpath
(`solution/solve.sh`, `environment/main.rs`) can never bind by URL at all — which is why S300 was
`anchor-unbound` ×2 at REF and only became visible once C2's round-94 provenance row landed.

The same patch under the **union** gate (control **M7**) clears the finding: `defects=40` and only the
`token-outside-anchor` remains (`M7-union-s300-names-mainrs.txt`). So the identical one-cell edit is inert
under the frozen gate and effective under union discovery — the difference is the binding, not the claim.

**B5 — C2's K4 closes the provenance route for non-POP rows.** K4: "every row id named in a `PROVENANCE.md`
absent at BASE is a POP id". A new provenance file in round 101 therefore cannot name S300, S202 or S242
unless the counter is re-frozen. Combined with B4, a multi-capture row that also carries a TB2 URL has **no
repair path** under the frozen instruments other than deleting a true claim.

---

## (c) Round-101 planning data-walk

**C1 — class arithmetic at T** (`class-arithmetic-T.txt`, from `plans/grader-population-ledger.json`,
88 members, 44 executed / 44 unexecuted):

```
shell-exec              2/6   0.3333   <- min (tie)
subprocess-exec        15/45  0.3333   <- min (tie)
filesystem-metadata     4/10  0.4000
numeric-band            4/10  0.4000
crypto-credential       5/12  0.4167   (was 4/12 at BASE; C1's flip landed exactly)
timing-wall             4/9   0.4444
stdout-inspection      13/29  0.4483
file-artifact          35/76  0.4605   (was 34/76 at BASE)
candidate-import        3/6   0.5000
db-state                1/2   0.5000
network-service         4/8   0.5000
git-plumbing            2/3   0.6667
process-environment     2/3   0.6667
serialization-schema    8/10  0.8000
signal-delivery         1/1   1.0000
```

`min_class` tie set at T = **{shell-exec 2/6, subprocess-exec 15/45}**, both exactly 1/3.

**C2 — the minimum is arithmetically immovable by any single member.** Both tied classes are exactly 1/3.
A shell-exec member gives 3/6 = 0.500 (min falls to subprocess-exec 0.333); a subprocess-exec member gives
16/45 = 0.3556 (min falls to shell-exec 0.333). The min only moves if **both** are lifted in the same round,
to 16/45 = 0.3556. And shell-exec has **no host-feasible member**: `git-multibranch` (grader 2 625 B, tree
10 280 B) shells `bash verify.sh` needing `expect` + `nginx` + sshd (expect **MISS**, nginx **MISS**, sshd
HAVE); `overfull-hbox` runs `/usr/bin/pdflatex` (texlive **MISS**); `qemu-startup` needs qemu (**MISS**);
`model-extraction-relu-logits` is candidate-library-blocked. So round 101 cannot raise `min_class`; it can
only break the tie.

**C3 — cheapest feasible unexecuted member per thin class** (`member-cost-thin-classes.txt`; cost = committed
grader bytes at `corpus/evidence/round52/graders/<task>/tests/test_outputs.py` + pinned tree bytes from
`corpus/evidence/round53/pin-tree-2fd12b88.json` + host probe 2026-11-06). All 44 unexecuted members already
have a committed grader capture, so the marginal cost of a replay is the **fixture**, not the grader bytes.

| thin class | cheapest feasible member | grader | tree | runtime | verdict |
|---|---|---|---|---|---|
| shell-exec | — | — | — | — | **none feasible** (expect/nginx/pdflatex/qemu all MISS) |
| subprocess-exec | `build-cython-ext` | 5 932 B | 12 229 B | stdlib-only grader; gcc HAVE, cython via uv | **feasible**, Σ lift **0.4687** over 4 classes |
| filesystem-metadata | `tune-mjcf` | 4 198 B | 14 764 B | `mujoco` via uv (MISS now) | **feasible**, Σ lift 0.3243 over 4 classes |
| numeric-band | `tune-mjcf` | 4 198 B | 14 764 B | same | same member |
| timing-wall | `tune-mjcf` | 4 198 B | 14 764 B | same | same member |
| crypto-credential | `custom-memory-heap-crash` | 6 062 B | 31 304 B | g++ HAVE; needs MD5-pinned upstream `/app` bytes (not committed) | feasible with one fetch |

`build-cython-ext` is also the Q86 tie-break answer: it sits in `subprocess-exec` (a tied min class) and has
the highest Σ marginal lift of any feasible member in the tied set (0.4687: git-plumbing 2/3→3/3,
numeric-band 4/10→5/10, subprocess-exec 15/45→16/45, file-artifact 35/76→36/76). `cobol-modernization`
(3 027 B grader, python-only) is the cheapest single-class member but lifts only 0.0354.

**C4 — the 23 remaining anchor-digest findings at T, grouped by class** (`findings-23-grouped.txt`;
23 findings over 21 rows):

| class / detail | n | rows | cheapest honest successor |
|---|---|---|---|
| `anchor-unbound` / `row-carries-no-capture-locator` | **17** | S178 S179 S184–S193 S229 S231 S233×2 S240 | live fetch + commit capture + name it. **0 of the 20 tokens tested (these 17 plus S202, S236, S242) has a committed copy** (measured against 1 677 corpus digests), so every one costs a fetch |
| `anchor-unbound` / `no-capture-for-upstream-<task>/instruction.md` | **2** | S202 `chess-best-move` (260 B), S242 `nginx-request-logging` (1 882 B) | commit `instruction.md` + a `task.toml` with `name = "terminal-bench/<task>"` in a new evidence dir — 2 tiny files each, no other fetch |
| `digest-unknown` / `not-committed-evidence` | **1** | S236 | the row names a committed *listing* capture (sha256 `236c1982…`) but claims the **zip** digest `0a9c8e34…`; commit the 2 990 966 B zip and name it, or drop the zip claim |
| `token-outside-anchor` / `sha256-claim-in-cell-N` | **2** | S213 cell 5, S300 cell 7 | S213's token is the two hex chars `be` parsed out of the prose **"sha256 below"**; S300 cell 7 carries the derived `data.comp` digest `3a905a56…9131`. Both are cell edits, **0 bytes** |
| `abbrev-unresolved` | **1** | S300 | `fa53d657…` is already committed (B4); under the frozen gate the only clearing edit is to stop claiming it |

**Measured cheapest honest increment: 3 cell edits, 0 bytes fetched, 23 → 20** — controls
`M4-s300-abbrev-to-path` (23→22), `M5-s213-reword` (23→22), `M6-s300-derived-digest-out-of-teaches` (23→22),
`M4M5M6-combined` (**23→20**).

---

## Proposed move (one, bounded)

**CO-1 — Round 101 should land a *union-discovery* gate copy as a second, non-scoring instrument, and
report the freshness count as a pair (frozen-gate bound count, union count) until the newly-visible
captures are anchored.**

Rationale, measured: the frozen gate's `bind_row` returns the first route that yields a capture, so a row
that names a second committed capture alongside a binding route can never express it. Round 100's bindings
therefore buy less than the headline: under a union-discovery variant of the same gate (identical round-39
token-per-capture semantics, only capture *discovery* unioned; `gate-union.py` in the receipts) the series
is **42 / 42 / 41** at BASE / REF / T, against **33 / 32 / 23** exclusive. The REF→T delta under union
(`union-delta-REF-T.txt`) is 8 `digest-wrong-capture` findings **relabelled** to `capture-unanchored`
(the token is now correctly bound, but the row's other named capture is visibly unanchored) plus S300's
2 `anchor-unbound` → 1 `abbrev-unresolved`. Net −1, not −9.

Why this improves an axis without harming another: it makes the *freshness* number re-checkable rather than
precedence-dependent, and it is the only route by which S295's pin-tree capture and S300's already-committed
`main.rs` digest become expressible at all (B2, B4, B5). Coverage is untouched — no population row changes —
so the capped coverage axis (7) is not put at risk.

Risks, stated plainly:

1. **The union number is worse than the frozen number** (41 vs 23). If the metric is swapped rather than
   paired, round 101's freshness score falls for doing the honest thing. Mitigation: the frozen gate stays
   the scoring instrument; union is diagnostic only.
2. **Round 39 already falsified a union** — of *token→digest*, not of *capture discovery*. The variant here
   keeps one token per capture: S295 still raises `capture-unanchored` under it (verified), so the round-39
   property is preserved. Any landed copy must carry that as a falsifier.
3. **A second gate is a new instrument** and needs its own do-nothing / forged / positive controls before it
   may be cited (Q80/Q85 shape). None exist yet; this seat provides only the three-point series.
4. **B5 blocks the provenance repair path**: K4 forbids a new `PROVENANCE.md` naming a non-POP id, so the
   rows that union discovery newly exposes cannot be fixed by C2's instrument in round 101 unless K4 is
   re-frozen. Without that, union discovery raises the count without a matching repair route.
5. **The three zero-fetch repairs are not free of side effects**: M4 (naming `main.rs`) adds S300 to the
   suppressed set (**17 → 18**, measured, `M4-suppressed-census.txt`) while removing a gate finding — the
   count improves, the visibility does not.

Verification the move must carry:

- Union gate at BASE / REF / T prints `42 / 42 / 41` and exits 1 at each (`gate-union-{BASE,REF,T}.txt`).
- The M3/M7 pair must hold: naming the committed `main.rs` in S300 leaves the frozen gate at 23 and the
  union gate at 40 (`M3-s300-names-committed-mainrs.txt`, `M7-union-s300-names-mainrs.txt`).
- Do-nothing at T reproduces 41; a forged second-capture token must fail; S295 must still raise
  `capture-unanchored` (round-39 property).
- The frozen gate must still print `33 / 32 / 23` on the same three revisions (already measured,
  `gate-{BASE,REF,T}.txt`) — the pair is the deliverable, not a replacement.
- If the three cell repairs land, the frozen gate must print 20 at the new T and the suppressed census must
  be re-run (expect 17 or 18, per risk 5).

---

## Receipts

`.ufo/waves/round-100/w1/ConnectorOverlap/`

| file | content |
|---|---|
| `c1-run-T.txt`, `c2-run-T.txt` | frozen predicates re-run at T from the clone (both `pass`) |
| `gate-BASE.txt`, `gate-REF.txt`, `gate-T.txt` (+ `.verbose.txt`) | frozen gate at BASE / REF / T: 33 / 32 / 23 |
| `delta-BASE-REF.txt` | the single S295 `capture-unanchored` line |
| `gate-union-{BASE,REF,T}.txt`, `gate-union.py`, `union-delta-REF-T.txt` | union-discovery variant: 42 / 42 / 41, REF→T delta |
| `locator-suppressed-census.py`, `locator-suppressed-BASE-REF-T.txt` | 7 / 8 / 17 rows with a suppressed explicit path |
| `M1…M7`, `M4M5M6-combined`, `M4-suppressed-census.txt` | seven gate controls (bogus path, URL removed, main.rs named exclusive vs union, three cell repairs) and M4's census side effect |
| `class-arithmetic-T.txt`, `member-cost-thin-classes.txt`, `findings-23-grouped.txt` | round-101 planning data |
| `write-set-F-T.txt`, `cross-lane-scan.txt` | F..T write set, append-only proof, fleet scan |
