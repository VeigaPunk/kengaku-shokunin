# Seat report — M6SourcesRowMutants

**Seat:** `M6SourcesRowMutants` (mutation-tester) · **Round:** kengaku 55, wave 1 (v2, build+attack)
**Date:** 2026-10-30 · **Lane:** `kengaku-shokunin` · **Frozen claims:** `plans/round-55-claims.md`
@ `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (read first; no predicate/counter/kill rule touched)

**Question under attack:** *Do the census/gate catch defective SOURCES rows?*

**Answer:** the frozen census catches 4 of the 5 injected row defects. It **misses** a sha256 pin
displaced out of the anchor cell (M2) — that defect is visible only to the lane's own
`plans/anchor_digest_check.py`, which is itself **already red** on this tip. Full ledger:
`.ufo/waves/round-55/w1/M6SourcesRowMutants/mutants.md`.

---

## 1. What I ran

Scratch root (created, used, deleted): `/fast/scratch/hyaku/kengaku-r55/M6SourcesRowMutants/`

```
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin \
        /fast/scratch/hyaku/kengaku-r55/M6SourcesRowMutants/lane      # exit 0, HEAD=80afa61
cp <lane>/corpus/SOURCES.md  <scratch>/lane/corpus/SOURCES.md          # working-tree draft rows (S201/S202)
cp <lane>/corpus/knowledge/tb2-chess-best-move-grader.md  <scratch>/lane/corpus/knowledge/
cp /home/vgpnk/Projects/shokunin/scripts/sources-census.sh <scratch>/tools/   # sha256 3fb72615…4a64e30 (identical)
```

Per mutant: restore pristine → apply exactly one defect to the S201 row → run three detectors.
Harness: `receipts/mutate.py` (mutant builder, asserts each mutation applied and changed the file),
`receipts/run.sh` (restore → mutate → D1 → D2 → D3).

### Detectors

| id | detector | provenance |
|---|---|---|
| D1 | `CORPUS.md` §Census manual command set — 7 commands (rows count; malformed `NF!=13`; tier histogram; status histogram; duplicate ids; enum violations + tier inflation; mined `used-by` paths that do not exist), run with cwd = scratch lane root on `corpus/SOURCES.md` | frozen fleet contract `/home/vgpnk/Projects/shokunin/CORPUS.md` |
| D2 | `bash scripts/sources-census.sh validate --file <scratch copy>` | fleet-root maintained CLI (byte-identical copy in scratch) |
| D3 | `python3 plans/anchor_digest_check.py --lane <scratch lane>` | the lane's own advertised SOURCES gate (SKILL.md row `anchor-digest-check`); supplementary — reported separately because it is the only detector with an anchor-content leg |

### Commands + exit codes

| run | D1 result | D2 exit | D3 exit / summary |
|---|---|---|---|
| baseline (pristine draft rows) | clean: rows=195, malformed=0, tier `A=166 B=24 C=5`, status `mined=174 queued=8 rejected=13`, dup ids none, enum none, missing used-by none | **0** (`file ok`; 15 pre-existing `W04` warnings) | **1** — `rows=195 tokens=94 defects=23` (pre-existing red) |
| base tip `80afa61` (committed registry) | clean: rows=193, malformed=0, dup none, enum none, used-by none | **0** | **1** — `rows=193 tokens=92 defects=21` |
| M1 drop one pipe (10 columns) | **caught**: malformed count `1` | **1** — `file E01 S201 fields=10` | **1** — `DEFECT S201 … class=row-malformed detail=cells=10-expected=11` |
| M2 sha256 token moved out of the anchor cell | **missed**: all seven commands clean | **0** — `file ok`, no `E*` line | **1** — `DEFECT S201 anchor token=a540714e… class=token-outside-anchor detail=sha256-claim-in-cell-7-of-11` |
| M3 tier `D` | **caught**: `tier S201 D`; histogram `D=1` | **1** — `file E06 S201 tier=D` | 1 (no new line — no enum leg) |
| M4 status `mined!` | **caught**: `status S201 mined!`; histogram `mined!=1` | **1** — `file E07 S201 status=mined!` | 1 (no new line) |
| M5 duplicate id | **caught**: duplicate-id list prints `S201`; rows 195→196 | **1** — `file E03 S201 duplicate id` + `file E04 S201 duplicate url … within scope …` | 1 — duplicate `DEFECT S201` line, `rows=196 tokens=95 defects=24` |

Mutation hashes (sha256 of the mutated scratch `corpus/SOURCES.md`): M1 `f6f8d48f…15dd0`,
M2 `230162ed…15c06`, M3 `50ccc262…dc0a`, M4 `4b188440…8b310`, M5 `05240967…1c120`; pristine
`1b8bd31430537cc8df4ca273bed54bca89dc32d2f9ecab42ac0c651369c7d8fa`.

## 2. Files I wrote (all inside the lane, only my seat's names)

* `.ufo/waves/round-55/w1/M6SourcesRowMutants.md` — scoped findings (the card's `Report:` path)
* `.ufo/waves/round-55/w1/M6SourcesRowMutants/mutants.md` — the caught/missed ledger
* `.ufo/waves/round-55/w1/M6SourcesRowMutants/report.md` — this report
* `.ufo/waves/round-55/w1/M6SourcesRowMutants/receipts/` — `baseline.txt`, `M1.txt`…`M5.txt`,
  `anchor-digest-check-basetip-80afa61.txt`, `anchor-digest-check-draftrows-full.txt`,
  `mutate.py`, `run.sh`, `pristine-SOURCES.md`

No tracked lane file was written by this seat. The lane's `PROVINCE.md`, `corpus/README.md` and
`corpus/SOURCES.md` were already modified in the working tree before this seat started (other seats /
L1); `corpus/SOURCES.md` still hashes to `1b8bd314…d8fa`, i.e. unchanged by me.

## 3. Defects found

1. **Census blind spot (the seat's assigned reviewer-eyes item).** A `sha256 <hex>` token moved out of
   the anchor cell (M2) is invisible to both frozen census command families: D1's seven commands all
   print clean values and D2 prints `file ok` with exit 0. The census checks id shape, column count,
   kind/tier/status enums, dates, URL duplication and `used-by` existence — it has **no anchor-content
   leg**. A row can therefore carry its digest pin in the wrong cell (or carry none) and the census
   stays green. Only `plans/anchor_digest_check.py` sees it (`class=token-outside-anchor`).
   *Lesson for the round:* a green census is not evidence that the pins are sound; the anchor-binding
   gate must be run alongside it, and it must be green first — which, per (2), it currently is not.
2. **The lane's advertised anchor gate is RED on this tip (pre-existing, not mutant-caused).**
   `plans/anchor_digest_check.py --lane .` → exit 1, `defects=23` at the draft state and
   `defects=21` at the committed base tip `80afa61` (ids S173–S193, all `class=anchor-unbound`).
   The round-55 draft rows add two more (`S201`, `S202`, both `anchor-unbound`). Since the kill rule
   of R55-C3 (c) is about the upstream identity check and the round's C3 receipt is the probe receipt,
   this redness is a lane-level observation the L1 should see before landing the new rows: the new
   rows' pins are not verifiable by the lane's own gate as the registry stands.
3. **S202's pinned digest is not resolvable from committed corpus evidence.** Token
   `sha256 6ba25be4…ce7a` is the digest of a file that exists only at
   `.ufo/waves/round-45/attempt1-unclaimed/corpus/evidence/round45/f1-census/chess-best-move/instruction.md`
   (verified with `sha256sum`; listed in that tree's `SHA256SUMS`), not under `corpus/evidence/`.
   `find corpus/evidence -name instruction.md` finds no `chess-best-move` capture. The gate line:
   `DEFECT S202 … class=anchor-unbound detail=no-capture-for-upstream-chess-best-move/instruction.md-task=chess-best-move`.
4. **S201's pin is true but the gate cannot bind it (evidence-tree locator gap).** The capture
   `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` exists, its sha256 is
   exactly the anchor token `a540714e…f286`, and the digest is listed in
   `corpus/evidence/round52/graders/SHA256SUMS` line 18 — yet the gate reports
   `class=anchor-unbound detail=no-capture-for-upstream-chess-best-move/tests/test_outputs.py-task=tests`,
   because that evidence tree has no `task.toml`/`PROVENANCE.md` locator, so the tool derives the task
   name `tests` instead of `chess-best-move`. Same root cause as the 21 base-tip defects.

I did **not** fix 2–4: `corpus/SOURCES.md`, the evidence tree and `plans/anchor_digest_check.py` are
other seats'/L1's files.

## 4. Dead ends / notes

* The seat card's `S901` fallback (mutate a copy of an existing row) was unnecessary: the DRAFT
  `S201`/`S202` rows were already present in the lane working tree at seat time, so S201 was the
  mutation target.
* `scripts/sources-census.sh` does not exist inside the lane; it lives in the fleet root
  (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`) and is shipped with the fleet-wide
  `CORPUS.md` census — the card's phrasing "scripts/sources-census.sh" resolves to the fleet root
  copy. I ran a byte-identical copy from scratch (sha256 `3fb72615…4a64e30`) and never wrote to the
  fleet root.
* `sources-census.sh validate --file` resolves `used-by` existence against the **file's
  parent-parent** directory, so the scratch copy had to live at `<scratch>/lane/corpus/SOURCES.md`
  for `E11` to have lane-root semantics; the scratch lane therefore also received
  `corpus/knowledge/tb2-chess-best-move-grader.md` (the `used-by` target of S201/S202).
* First attempt at the M2 mutation failed its own precondition (`sha256 token not in anchor cell`):
  my cell index was off by one (a row split on `|` has the anchor at index 6, not 7). Fixed in
  `mutate.py`; M2 was then applied and re-measured from the pristine base. The failed run left the
  scratch file byte-identical to pristine (sha256 unchanged), so no mutant state was contaminated.
* Two shell invocations returned "(no output)" while their redirections had actually written the
  expected files; the transcripts were re-verified by reading the files back, and every number quoted
  in this report comes from those files, not from the console echo.
* Not run (out of seat scope, so no claim is made about them): `plans/sources_adopt.py` (append-time
  gate, operates on a staged registry rather than on a registry file), `plans/round37_c2_verify.py`
  and the other lane counters that shell out to the fleet census — D2 already exercises the same
  fleet script directly.

## 5. Restoration / hygiene

* Pristine registry restored into the scratch lane before every mutant run; final scratch-lane
  `corpus/SOURCES.md` sha256 `1b8bd31430537cc8df4ca273bed54bca89dc32d2f9ecab42ac0c651369c7d8fa`
  = byte-identical to the lane's file at seat time.
* The lane repo was touched read-only (`git log/status/ls-tree/show/grep`); no mutating git or jj
  command was run anywhere, no sibling repo was touched, no fleet-root tracked file was written, no
  tool was installed.
* Scratch root `/fast/scratch/hyaku/kengaku-r55/M6SourcesRowMutants/` was deleted after the receipts
  were copied into `.ufo/waves/round-55/w1/M6SourcesRowMutants/receipts/`.
