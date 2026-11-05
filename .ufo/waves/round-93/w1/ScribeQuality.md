# ScribeQuality — round 93, wave w1 — seat report

Lane `kengaku-shokunin` @ `22972a317185216596b3dfe1c189e98d1eb86787` (measured tip T).
Scratch: `/fast/scratch/hyaku/kengaku-r93/ScribeQuality` (a `git clone --shared` of the lane
checked out detached at T; removed after the receipts were copied). The lane tree, the lane git
index and the fleet root were not mutated; no commit, no push, no subagent.

## Deliverables (both drafts, for the L1 to integrate)

| file | what it is |
|---|---|
| `.ufo/waves/round-93/w1/ScribeQuality/quality-criterion.md` | one new `corpus/QUALITY.md` criterion (Q73, subject to the L1's numbering) making "a `frozen-instruments` sha256 table in the claims file **plus** a green freeze-integrity gate at the measured tip" a precondition for any claim verdict "met as frozen"; cites round-92 lesson M8 and this round's `plans/round93_freeze_integrity.py`; carries a measured red witness |
| `.ufo/waves/round-93/w1/ScribeQuality/lesson-gate.md` | the round-93 lesson `## Gate` block for S290–S296 in the format of `corpus/lessons/round-92.md` `## Gate` (six columns: candidate · decision · access · located quote and location · reason · flip), every cell taken from the SOURCES rows, with the values I could not confirm marked inline |
| `.ufo/waves/round-93/w1/ScribeQuality/receipts/` | raw receipts: `source-verification.txt` (S290–S296 value verification), `raw-receipts.txt` (gate and counter runs), `gate-at-tip.txt`, `gate-r92-history.txt`, `c2-counter-at-tip.txt`, `capture-verification.txt` |

## Behaviour (what this seat did)

1. Read the frozen claims (`plans/round-93-claims.md`), the frozen-instruments table, the
   freeze-integrity gate (`plans/round93_freeze_integrity.py`), the C2 counter, the round-92
   lesson's `## Gate` block, and the file's last three `corpus/QUALITY.md` criteria (Q70–Q72).
2. Re-fetched every pinned URL for S290–S296 from `raw.githubusercontent.com` at
   `2fd12b88aafdd04a52c298e3940bcb189f9766d6` on 2026-11-05: all HTTP 200, all byte counts and
   sha256 values equal to the SOURCES rows. Re-fetched all 63 test programs (63/63 HTTP 200) and
   re-derived S293's sorted-manifest digest.
3. Verified every located quote at its cited line and every word count against the bytes.
4. Ran the freeze-integrity gate read-only at the measured tip (green, `broken=0`) and on the
   lane's real round-92 history (red, `broken=3`, rc 1) — the red witness the new criterion cites.
5. Ran the C2 counter at the measured tip (`PREDICATE R93-C2 pass`, rc 0) and the SOURCES census
   (`validate` exit 0, `kengaku ok`; `census` 288 rows).
6. Measured the C07 semantics the S290 row rests on, in a Python 3.13 venv with the pytest 8.4.1
   the wrapper pins: a non-`None` return from a test function is a warning, not a failure.

## Gates passed / not passed (in-round, for this seat's own work)

- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0,
  `kengaku ok` (30 pre-existing W04 duplicate-url warnings; no E-code; the seven new rows carry
  no warning of their own).
- `scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kengaku` → `rows 288`,
  `tier.A 258`, `status.mined 257`, `status.rejected 23` (281 rows at round start + 7).
- Freeze-integrity gate at T → `FREEZE-INTEGRITY instruments=9 intact=9 broken=0`,
  `PREDICATE freeze-integrity pass`, rc 0.
- Freeze-integrity gate on the round-92 history → `FREEZE-INTEGRITY instruments=4 intact=1
  broken=3`, `PREDICATE freeze-integrity fail`, rc 1.
- C2 counter at T → `W1 pass`, `W2 pass`, `W3 pass`, `W4 pass`, `TARGET legs_passed=4 of 4`,
  `PREDICATE R93-C2 pass`, rc 0.

## Touched surfaces

Written (all inside this seat's wave dir; nothing else on disk was created or changed):

- `.ufo/waves/round-93/w1/ScribeQuality/quality-criterion.md`
- `.ufo/waves/round-93/w1/ScribeQuality/lesson-gate.md`
- `.ufo/waves/round-93/w1/ScribeQuality/report.md`
- `.ufo/waves/round-93/w1/ScribeQuality/receipts/{source-verification.txt,raw-receipts.txt,gate-at-tip.txt,gate-r92-history.txt,c2-counter-at-tip.txt,capture-verification.txt}`

Read-only: the lane tree, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/lessons/round-92.md`,
`corpus/lessons/round-93.md`, `plans/round-93-claims.md`, `plans/round93_freeze_integrity.py`,
`plans/round93_c2_counter.py`, `plans/round93-cases.json`, `corpus/evidence/round93/**`,
`corpus/evidence/round52/graders/**`, `corpus/evidence/round53/pin-tree-2fd12b88.json`, and the
fleet-root `scripts/sources-census.sh` (executed read-only; it writes only stdout).

## Out of scope (not claimed, not answered)

- The open L0 questions in `.ufo/l0-questions.md` (coverage cap, in-tree pin residual, admission
  of repaired-instrument measurements, WAVE-DONE addressing) — untouched.
- The round-92 routed defects 2–6 that the claims file explicitly does not claim (gate-v3
  override vacuity, planted-marker skip, unpinned round-92 counters, unguarded
  `cost_model_for_tests.py`, and the M8 fix itself, which is the L1's to land). This seat drafts
  the criterion and the Gate text; it does not repair an instrument and does not close a routed
  defect.
- No instrument was changed. The frozen-instruments table at F is intact at T (measured above), so
  nothing in this round's verdict path is voided by this seat.

## Findings

**FINDING SQ-1 minor** — `corpus/lessons/round-93.md` (committed `fb79ef74`) carries a wrong
truncated digest in its Gate row for S292: `e2c5b0ac…10512`. The true digest is
`e2c5b0ac2bef4801a1891e13c108813381877426c1a7f01bab86b4fc1f712510` — its last five characters
are `12510`, and the string `10512` does not occur in it at all, so the row as filed does not
point at the bytes it names. Exact check:
`python3 -c "v='e2c5b0ac2bef4801a1891e13c108813381877426c1a7f01bab86b4fc1f712510'; print(v.endswith('10512'), '10512' in v, v[-6:])"`
→ `False False 712510`. This does **not** flip a verdict: the SOURCES row's full digest is
correct, the capture matches it byte for byte, and the lesson's cell is an abbreviation only. The
round-92 M8 lesson (filed lesson bytes are never rewritten in place, QUALITY Q55) means the
correction is an erratum row or a new commit naming the superseded text, not an in-place edit.
The draft `lesson-gate.md` uses the correct `e2c5b0ac…712510`.

**FINDING SQ-2 minor** — the SOURCES row S295 states "the 17 environment documents (about 4.2 MB
of jpg/pdf)". The count (17) and the mix (11 `.jpg` + 6 `.pdf`) are exact, but the size is not:
the 17 documents at the pinned tree
(`corpus/evidence/round53/pin-tree-2fd12b88.json`) total **4,002,650 B = 3.82 MiB = 4.00 MB**,
and the whole task tree is 4,031,474 B = 3.84 MiB. Exact check:
`python3 -c "import json;d=json.load(open('corpus/evidence/round53/pin-tree-2fd12b88.json'));s=[x['size'] for x in d['blobs'] if '/environment/documents/' in x['path']];print(len(s),sum(s),sum(s)/1048576)"`
→ `17 4002650 3.817…`. The figure overstates by about 5 %. It does **not** flip a verdict: the
rejection rests on the pinned sha512 digests and on pandas being absent, both confirmed — all 17
upstream documents' sha512 digests match the grader's 17 pinned digests one for one. The row is
frozen in the registry; the draft Gate marks the figure "not confirmed" and gives the measured
size.

**FINDING SQ-3 minor** — the SOURCES rows S295 and S296 say "not captured in the lane". They are
not in the round-93 capture tree, but both files *are* in the lane, byte-identical to the rows'
sha256, under `corpus/evidence/round52/graders/`. Exact check:
`sha256sum corpus/evidence/round52/graders/financial-document-processor/tests/test_outputs.py`
→ `978f506ad5c1bfaf28f9bc774dfe4347d33d046ca009b8496eb513956b7f5a9a` (equal to S295) and
`sha256sum corpus/evidence/round52/graders/large-scale-text-editing/tests/test_outputs.py`
→ `f5e69f4fedeefa23197745888a5847161529f454e6b5c32a4057363d9ae4cd43` (equal to S296). The cell is
false as written and a reader auditing the digest against the lane will find the bytes. The
draft Gate states the true provenance instead of repeating it.

**FINDING SQ-4 info** — S293's manifest digest `227d7bd1…e1be8f` reproduces, but only over the
`sha256sum` listing (paths included, sorted); the bare-hash variant hashes to `c6f397ff…d746`
and a path-prefixed variant to `a4a2892d…681e`. The row states the value but not the recipe, so
a reader cannot rebuild it from the row alone. The draft Gate names the recipe.

**FINDING SQ-5 info** — the lane working tree already carries an uncommitted
`## Round93 freeze-integrity lesson` section in `corpus/QUALITY.md` with a `Q73` and a `Q74`
(`git status` → ` M corpus/QUALITY.md`; `git diff corpus/QUALITY.md` shows only those two added
lines). That `Q73` is the same criterion this seat was asked to draft. The L1 must land one, not
two: `quality-criterion.md` is numbered Q73 (the next free number in the committed file) and the
draft says to renumber it to Q75 if the working-tree pair is kept.

**FINDING SQ-6 info** — the committed round-93 lesson's Gate block paraphrases the SOURCES rows
rather than reproducing them, dropping the S290 "passes with no evaluator (case C07)" fact and the
S293 "32 in test/, 31 in shadow_test/" split, and repeating the S295 size figure and the
"not captured in the lane" cells. The draft `lesson-gate.md` takes every cell from the row and
marks the two cells it could not confirm.

## Notes on measurement honesty

- The gate and the C2 counter were run against a detached `git clone --shared` of the lane in
  scratch, not against the lane working tree, so no gate output in this report depends on
  uncommitted lane bytes.
- The C07 pytest measurement is a host measurement on Python 3.13.16 / pytest 8.4.1 — the exact
  versions `tests/test.sh` pins — not a byte-identity claim about the upstream image.
- No tool was installed on the host. `uv` (0.13.0, already present) was used to create a
  throwaway venv in scratch and to install `pytest==8.4.1` into it; the venv lives under the
  scratch dir and is removed with it. No `pacman` operation was run (pacman is paused host-wide).

## Paths written

- `.ufo/waves/round-93/w1/ScribeQuality/quality-criterion.md`
- `.ufo/waves/round-93/w1/ScribeQuality/lesson-gate.md`
- `.ufo/waves/round-93/w1/ScribeQuality/report.md`
- `.ufo/waves/round-93/w1/ScribeQuality/receipts/source-verification.txt`
- `.ufo/waves/round-93/w1/ScribeQuality/receipts/raw-receipts.txt`
- `.ufo/waves/round-93/w1/ScribeQuality/receipts/gate-at-tip.txt`
- `.ufo/waves/round-93/w1/ScribeQuality/receipts/gate-r92-history.txt`
- `.ufo/waves/round-93/w1/ScribeQuality/receipts/c2-counter-at-tip.txt`
- `.ufo/waves/round-93/w1/ScribeQuality/receipts/capture-verification.txt`
