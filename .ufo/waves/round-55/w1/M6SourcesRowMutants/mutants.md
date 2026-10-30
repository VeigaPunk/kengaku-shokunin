# M6SourcesRowMutants — mutant ledger: does the frozen SOURCES census/gate catch defective rows?

Seat `M6SourcesRowMutants`, kengaku round 55 wave 1 (v2, build+attack). Date 2026-10-30.
Lane `kengaku-shokunin`. Frozen claims read: `plans/round-55-claims.md` @ `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`
(round-55 predicates/counters untouched by this seat).

## What was mutated (one defect at a time, scratch copy only)

Population: the round-55 **DRAFT** rows are present in the lane working tree, so the DRAFT rows
were used (the `S901`-fallback in the seat card was not needed):

* `corpus/SOURCES.md:216` — `| S201 | Terminal-Bench 2.0 chess-best-move task grader (tests/test_outputs.py) — …`
* `corpus/SOURCES.md:217` — `| S202 | Terminal-Bench 2.0 chess-best-move task instruction (instruction.md) — …`

All five mutants were applied to **S201** in a scratch copy of `corpus/SOURCES.md`
(`/fast/scratch/hyaku/kengaku-r55/M6SourcesRowMutants/lane/corpus/SOURCES.md`, a `git clone --shared`
of the lane at `80afa61`, with the lane's working-tree `corpus/SOURCES.md` copied in).
The lane repo itself was never modified. Pristine source of truth:
`receipts/pristine-SOURCES.md`, sha256 `1b8bd31430537cc8df4ca273bed54bca89dc32d2f9ecab42ac0c651369c7d8fa`
(byte-identical to the lane's `corpus/SOURCES.md` at seat time).

| id | defect injected into S201 | mutant sha256 |
|---|---|---|
| M1 | one pipe dropped (the pipe between the **anchor** cell and the **teaches** cell) → row has **10 columns** | `f6f8d48fd6175e5c4c11b0cf63cae761e9f9abe886c7e6a4fd3c223a90415dd0` |
| M2 | sha256 token **moved out of the anchor cell** into the teaches cell (`sha256 a540714e…` now in cell 7) | `230162ed2dd0745d291e48be8d51fdfa6a69d6e1af6013290152ec1407715c06` |
| M3 | **tier** `A` → `D` | `50ccc262924075dbecba657f67fa3d724473502ee09475f486b81afd51c1dc0a` |
| M4 | **status** `mined` → `mined!` (enum break) | `4b1884406e854924d1fdce1cfc769d5c436ed0ae324b0c63e248ed889318b310` |
| M5 | **duplicate id** (verbatim copy of the S201 row inserted after it) | `05240967a95b2e477c544affc829b0cef1961a07b7572c1591da2e0fea71c120` |

## Detectors run per mutant (frozen census commands)

* **D1 — `CORPUS.md` §Census manual command set** (fleet root `/home/vgpnk/Projects/shokunin/CORPUS.md`,
  §"Census — run from the lane root"): 7 commands, run with cwd = scratch lane root on
  `corpus/SOURCES.md`: (a) rows count, (b) malformed rows `NF!=13` (must print 0), (c) tier histogram,
  (d) status histogram, (e) duplicate ids (must print nothing), (f) enum violations + tier inflation
  (must print nothing), (g) mined rows whose `used-by` paths do not exist (must print nothing).
* **D2 — `scripts/sources-census.sh validate --file <scratch copy>`** (fleet root script, byte-identical
  copy used, sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`).
* **D3 — the lane's own advertised SOURCES gate `plans/anchor_digest_check.py --lane <scratch lane>`**
  (SKILL.md row `anchor-digest-check`). Supplementary to the seat's frozen command list; it is the
  only detector in this lane that has an **anchor-content** leg, so it is reported separately.

## Baseline (control) — must be clean for any "caught" verdict to be meaningful

* D1: rows=195, malformed=0, tier `A=166 B=24 C=5`, status `mined=174 queued=8 rejected=13`,
  duplicate ids → nothing, enum violations → nothing, missing `used-by` → nothing. **Clean.**
* D2: `file ok …`, **exit 0**; the only output is 15 pre-existing `W04 duplicate url … across scopes`
  warnings (warnings do not affect the exit code). **Clean.**
* D3: **exit 1, `rows=195 tokens=94 defects=23`** — the lane's anchor gate is already RED at this
  tip (see "Pre-existing defects" below), so D3 is read **differentially** (new/changed `DEFECT` lines
  naming S201/S202), not by exit code.
* Base tip check (committed `80afa61` `corpus/SOURCES.md`, receipt
  `receipts/anchor-digest-check-basetip-80afa61.txt`): census clean (rows=193, malformed=0, D2 exit 0),
  D3 `rows=193 tokens=92 defects=21`.

## Results — caught / missed

| mutant | D1 `CORPUS.md` §Census | D2 `sources-census.sh validate --file` | D3 lane `anchor_digest_check.py` | verdict |
|---|---|---|---|---|
| **M1** drop one pipe (10 columns) | **CAUGHT** — D1b prints `1` (must be 0) | **CAUGHT** — `file E01 S201 fields=10`, exit 1 | **CAUGHT** — `DEFECT S201 … class=row-malformed detail=cells=10-expected=11` (replaces the baseline `anchor-unbound` line for S201) | killed by the frozen census |
| **M2** sha256 token out of the anchor cell | **MISSED** — all 7 commands clean: rows 195, malformed 0, tier/status histograms unchanged, no duplicate id, no enum violation, no missing `used-by` | **MISSED** — exit 0, `file ok`, no `E*` line | **CAUGHT** — `DEFECT S201 anchor token=a540714e… class=token-outside-anchor detail=sha256-claim-in-cell-7-of-11 loc=corpus/SOURCES.md:216` | **SURVIVED the frozen census** (killed only by the lane's own anchor gate) |
| **M3** tier `D` | **CAUGHT** — D1f prints `tier S201 D`; D1c histogram `A=165 B=24 C=5 D=1` | **CAUGHT** — `file E06 S201 tier=D`, exit 1 | missed (no new D3 line; the tool has no enum leg) | killed by the frozen census |
| **M4** status `mined!` | **CAUGHT** — D1f prints `status S201 mined!`; D1d histogram `mined=173 mined!=1 queued=8 rejected=13` | **CAUGHT** — `file E07 S201 status=mined!`, exit 1 | missed (no new D3 line) | killed by the frozen census |
| **M5** duplicate id | **CAUGHT** — D1e prints `S201`; D1a rows 195→196 | **CAUGHT** — `file E03 S201 duplicate id` **and** `file E04 S201 duplicate url … within scope …`, exit 1 | caught (second identical `DEFECT S201` line; `rows=196 tokens=95 defects=24`) | killed by the frozen census |

**Coverage summary:** the frozen census (D1 ∪ D2) kills **4 of 5** mutants. The survivor is **M2** —
a sha256 pin displaced out of the anchor cell — which is exactly the reviewer-eyes item this seat was
asked to surface.

### M2 — the missed defect, stated plainly

The census has **no anchor-content leg**. Its checks are: id shape/duplication, column count, kind/tier/
status enums, opened/recheck dates, URL duplication, and `used-by` path existence. A row whose
`sha256 <hex>` token has been moved from the anchor cell into any other cell is **structurally
indistinguishable from a clean row** for both D1 and D2 (D2 prints `file ok`, exit 0). The only
detector in the lane that sees it is `plans/anchor_digest_check.py`, whose `token-outside-anchor` leg
prints `sha256-claim-in-cell-7-of-11`.

Consequence for the round: if the round-55 rows are landed with their pins displaced (or with the
digest simply dropped from the anchor cell — same blind spot), **the frozen census stays green** and
the pin silently stops being a pin. The lane's advertised `anchor-digest-check` gate would catch the
displacement, but that gate is *already red* on this lane (below), so a green census is not sufficient
evidence that the pins are sound.

## Pre-existing defects found (not caused by the mutants; reported, not fixed — not my files)

1. **The lane's advertised anchor gate is RED at this tip.** `plans/anchor_digest_check.py --lane .`
   → exit 1, `rows=195 tokens=94 defects=23`, all `class=anchor-unbound`:
   * at the committed base tip `80afa61` it is already red: `rows=193 tokens=92 defects=21`,
     ids S173–S193 (receipt `receipts/anchor-digest-check-basetip-80afa61.txt`);
   * the round-55 DRAFT rows **add two more**: S201 and S202, both `class=anchor-unbound`.
2. **S202's pin is not resolvable from committed corpus evidence.** The anchor token
   `sha256 6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a` is the digest of a file
   that exists only at
   `.ufo/waves/round-45/attempt1-unclaimed/corpus/evidence/round45/f1-census/chess-best-move/instruction.md`
   (verified by `sha256sum`; also listed in that tree's `SHA256SUMS` line 4) — **not** under
   `corpus/evidence/`. `find corpus/evidence -name instruction.md` returns no `chess-best-move`
   capture. The gate's defect line: `DEFECT S202 … class=anchor-unbound
   detail=no-capture-for-upstream-chess-best-move/instruction.md-task=chess-best-move`.
3. **S201's pin is true but the gate cannot bind it.** The capture
   `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` exists and its sha256 is
   exactly the anchor token `a540714e…` (verified; also listed in
   `corpus/evidence/round52/graders/SHA256SUMS` line 18). The gate still reports
   `class=anchor-unbound detail=no-capture-for-upstream-chess-best-move/tests/test_outputs.py-task=tests`
   because the round-52 graders tree has no `task.toml`/`PROVENANCE.md` locator, so the tool's
   row→capture derivation resolves the task name to `tests` instead of `chess-best-move`. This is a
   locator gap in the evidence tree (rows S173–S193 are affected the same way), not a wrong pin.

## Restoration evidence

* Pristine copy restored into the scratch lane before every mutant run (`run.sh` copies
  `pristine/SOURCES.md` → `lane/corpus/SOURCES.md` first); final scratch-lane state verified
  sha256 `1b8bd31430537cc8df4ca273bed54bca89dc32d2f9ecab42ac0c651369c7d8fa` = the lane's
  `corpus/SOURCES.md` at seat time (byte-identical).
* The lane repo was never mutated: only read-only `git` (`log`, `status`, `ls-tree`, `show`,
  `grep`) plus file copies; `git status --porcelain` in the lane shows no change to any tracked file
  caused by this seat (this seat's writes are confined to
  `.ufo/waves/round-55/w1/M6SourcesRowMutants*`).
* Scratch root `/fast/scratch/hyaku/kengaku-r55/M6SourcesRowMutants/` deleted after the receipts were
  copied into `.ufo/waves/round-55/w1/M6SourcesRowMutants/receipts/`.

## Receipts (this directory)

| file | content |
|---|---|
| `receipts/baseline.txt` | full D1+D2+D3 transcript, pristine draft rows (control) |
| `receipts/M1.txt` … `receipts/M5.txt` | full D1+D2+D3 transcript per mutant |
| `receipts/anchor-digest-check-basetip-80afa61.txt` | D3 at the committed base tip (21 defects) |
| `receipts/anchor-digest-check-draftrows-full.txt` | D3 with the draft rows (23 defects) |
| `receipts/mutate.py` | the mutant builder (one defect per invocation, asserts it applied) |
| `receipts/run.sh` | the detector runner (restore → mutate → D1 → D2 → D3) |
| `receipts/pristine-SOURCES.md` | the pristine registry copy used as the base (sha256 `1b8bd314…`) |
