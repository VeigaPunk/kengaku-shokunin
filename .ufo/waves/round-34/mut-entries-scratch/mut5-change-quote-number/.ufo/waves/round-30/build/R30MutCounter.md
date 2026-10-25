# R30 / C2 — mutation probe of `plans/round30_defects.py`

Seat: `L1Kengaku30.R30MutCounter` (leaf, mutation-tester). Date 2026-10-25.
Target under test: `plans/round30_defects.py` (sha256 `9a704064…f6429`) and the lesson/tree bytes its
checks read. Nothing in the lane was written; every mutation ran on `/tmp/r30-mutcounter/lane`, a
`cp -a` of the lane tree, with the pristine bytes kept in `/tmp/r30-mutcounter/orig/`.

## Method

- Scratch copy seeded at probe start. Seed hashes (side-by-side, the production lane matched on all
  four at copy time):

  | file | seed sha256 |
  |---|---|
  | `plans/round30_defects.py` | `9a7040648efa097eed27f1ca049a2b8eb68c5a53e588406b4c9bb06bec8f6429` |
  | `corpus/lessons/round-29.md` | `d3b58d9d3d7046391a7aa5559844bf32d071bff7da38cdb8828ad156c72607c4` |
  | `.ufo/waves/round-29/attempt2/adoption-expect.json` | `619feca30b7845de743fc144fb613e2c79f688cca032903b137c2d6addae06b5` |
  | `corpus/SOURCES.md` | `e18b32d9b2e3b19053a3d431eb4586713fe057d04477651e6d02be51e8908236` |
  | `corpus/evidence/round29-attempt2/control-nothing.txt` | `4b478db43d6f69d7447298db7103e37bb1a8b8109c5efff426d9a943dc18e4bd` |

- The live lane was **not** green at copy time (`defects=1`, D4: `R29a2CritEntry.md` uncommitted in
  the wave worktree, exactly the C2 control state). D4 is a git-state item, so to obtain a
  failure-free baseline I made one scratch-only commit in `/tmp` (`dd83a3d`, detached HEAD, no lane
  commit); the baseline then reads:

  ```
  ok D1 receipt-at-cited-path: repaired
  ok D2 kappa-sweep-scope: repaired
  ok D3 s078-line75-word-count: repaired
  ok D4 uncommitted-wave-evidence: repaired
  ok D5 s091-usedby-asymmetry: repaired
  defects=0
  EXIT=0
  ```

- Verdict rule as given by the tasking: on a tree that carries the defect, a mutated detector that
  still prints `defects=0` has **survived**. Every surviving mutant was therefore paired with a
  planted defect and with the pristine detector's output on the same bytes (kill evidence), so no
  verdict rests on a vacuous green tree.
- Each counter mutant was restored from `orig/` before the next probe; each tree mutant was restored
  from `orig/` or from the exact bytes moved aside.

## Results

| # | mutation | tree state | counter output | verdict |
|---|---|---|---|---|
| m1 | `plans/round30_defects.py:95`: `if lesson_count != words(QUOTE):` → `if lesson_count != lesson_count:` (check_d3 compares the lesson against itself; always false) — mutant counter `f7fced2e…0a34f4` | lesson L194 re-carrying round 29's defect: `"The verifier never runs in the agent's sandbox." — 9 words, line 75` (lesson `cf4dcddc…f13b4`); registry S078 still 8 | `ok D1 … / ok D2 … / ok D3 s078-line75-word-count: repaired / ok D4 … / ok D5 …` `defects=0`, `EXIT=0` | **survived** (pristine detector on the same bytes: `DEFECT D3 s078-line75-word-count: lesson prices the line-75 quote at 9 words, actual 8 (registry says 8)`, `defects=1`, EXIT=1). Green-tree check: mutant also prints `defects=0` → a pure blind spot, no false alarm to catch it. |
| m2 | `check_d1` reduced to a directory test: body → `if not path.is_dir(): return f"receipt absent at the cited path {D1_PATH}"; return ""` (both content assertions `entries=0` / `exit=1` deleted) — mutant counter `a856d957…28d53` | D1 path planted as a **directory** of that name, zero bytes (`corpus/evidence/round29-attempt2/control-nothing.txt/`) | `ok D1 receipt-at-cited-path: repaired / … / ok D5 …` `defects=0`, `EXIT=0` | **survived** (pristine: `DEFECT D1 receipt-at-cited-path: receipt absent at the cited path corpus/evidence/round29-attempt2/control-nothing.txt`, `defects=1`, EXIT=1). Two extra observations: (a) on the *correct* receipt file the mutant prints a false defect (`DEFECT D1 … receipt absent at the cited path`, `defects=1`) because a real file is not a directory — a green-tree assertion kills that half, but not the directory blind spot; (b) on a stub receipt carrying `entries=0` but no `exit=1` the mutant still fails, with the wrong reason (`receipt absent at the cited path` instead of `carries no exit=1 line`). |
| m3 | tree mutant, no counter change: "repair" D2 by deleting the kappa line outright — the two lines containing `kappa` (L232–233 of the lesson) removed; `grep -c kappa` 2 → 0; lesson `f12fc565…df968` | green elsewhere | `ok D1 … / DEFECT D2 kappa-sweep-scope: no kappa line in the lesson: the sweep the closure narrowed is gone / ok D3 … / ok D4 … / ok D5 …` `defects=1`, `EXIT=1` | **killed** — the vacuity guard `if not lines:` is load-bearing: deleting the evidence is not a repair. |
| m4 | `check_d5`: `if not isinstance(notes, dict) or "S091" not in notes:` → `if not notes:` (any non-empty `usedby_notes` accepted) — mutant counter `ff58d8dd…4978` | `usedby_notes` kept non-empty but re-keyed `"s091"`, i.e. the S091 asymmetry is no longer machine-recorded under the id the registry uses (expect `598a5a86…da63`) | `ok D1 … / ok D2 … / ok D3 … / ok D4 … / ok D5 s091-usedby-asymmetry: repaired` `defects=0`, `EXIT=0` | **survived** (pristine: `DEFECT D5 s091-usedby-asymmetry: adoption-expect.json records no S091 used-by asymmetry note`, `defects=1`, EXIT=1). Green-tree check: `defects=0` both ways → pure blind spot. Boundary of the blind spot, for the record: with `usedby_notes` deleted altogether the mutant still fails, because the key is absent and the dict is empty. |

### 3 survivors, 1 killed. Survivors and the tightening that kills each

**m1 (D3 self-comparison) — survived.** The lesson count is only ever compared to itself, so the
registry cross-check is the sole guard and any lesson-only mismatch is invisible. Tightening: derive
one oracle and compare all three artifacts against it, `if not (lesson_count == row_count ==
words(QUOTE)):`, and re-extract the quoted string from the registry anchor cell rather than trusting
`QUOTE` alone; add a failure-capable fixture — the round-29 shape (lesson 9, registry 8) must print
`DEFECT D3` — which the mutant fails.

**m2 (D1 directory-only) — survived.** `is_dir()` inverts the predicate for the real artifact and
drops both byte assertions. Tightening: keep `path.is_file()`, assert the receipt is a git blob
(`git cat-file -t :<D1_PATH>` == `blob`) so a directory cannot stand in, and keep the two content
assertions as a conjunction over the fetched bytes (`entries=0` **and** `exit=1`), each with its own
reason string; a fixture with a directory at the path must print `DEFECT D1`.

**m4 (any non-empty note) — survived.** Membership is not checked, so a mis-keyed or generic note
satisfies D5. Tightening: require exact key membership `"S091" in notes` **and** a non-empty note
body that names both `ENTRY` and the routed-defect id, plus a bidirectional set equality between the
registry's used-by ids for `ENTRY` and the keys of `usedby_notes`, plus a key-shape check
(`^S[0-9]{3}$`) so a lowercase key is refused.

## Adjacent coverage findings in the pristine detector (not part of the four assigned rows)

Two survivors that need no counter mutation — relevant to C2's calibration, because they let a
vacuous repair print `defects=0`:

1. **D5 accepts an empty note.** With the S091 note value set to `""` (bytes `bd410bb9…b09048`) the
   pristine counter prints `ok D5 s091-usedby-asymmetry: repaired`, `defects=0`, `EXIT=0`. D5
   verifies the key's presence, never that the note explains anything.
2. **D2 accepts a falsified count.** With the kappa line's measured result changed from `0 hits` to
   `12 hits` while still naming `corpus/knowledge/*.md` (lesson `2649086e…d878`), the pristine
   counter prints `ok D2 kappa-sweep-scope: repaired`, `defects=0`. D2 checks the scope string and
   the forbidden "in the lane" phrasing, not the number the scope measured.

Neither is a contract change; both are one-assertion tightenings (`notes["S091"].strip()` non-empty
and naming `ENTRY`; the count parsed and compared to a re-run of the scoped grep).

## Restoration evidence

- All four probed files back to seed hashes, verified after the last probe:
  `plans/round30_defects.py 9a704064…f6429`, `corpus/lessons/round-29.md d3b58d9d…07c4`,
  `adoption-expect.json 619feca3…06b5`, `corpus/SOURCES.md e18b32d9…8236`, receipt
  `4b478db4…e4bd` (the receipt was moved aside, never rewritten; its restored hash equals the
  production lane's copy byte for byte).
- Post-restoration run: all five `ok`, `defects=0`, `EXIT=0` — behaviourally identical to the
  pre-probe baseline.
- Lane untouched by this seat: `plans/round30_defects.py`, `adoption-expect.json`, `SOURCES.md` and
  the receipt in `/home/vgpnk/Projects/shokunin/kengaku-shokunin` carry the same hashes they had when
  I copied them, and the lane's `git status --porcelain` entry set is unchanged. One note for the
  integrator: the lane's `corpus/lessons/round-29.md` hash moved from `d3b58d9d…07c4` (my seed) to
  `3a0ab556…ee1d4` while I probed — a peer edit on that file (`L1Kengaku30` owns the S078 word-count
  correction), not mine. My verdicts were taken against the seeded `d3b58d9d…07c4` bytes, and the
  lane still carries its 2 kappa lines and the L194 quote, so the seeded defect sites remain
  representative.
- Nothing else added or removed: only this report file under `.ufo/waves/round-30/build/` and the
  scratch dir `/tmp/r30-mutcounter/` (`lane/`, `orig/`, `receipt.real`).
- No tool installed, upgraded or removed for this seat (no package manager transaction run; pacman
  is paused host-wide and was not touched). Python used is the host `python3`; no `uv`/`npx`
  installs were needed.

## One-line handoff for C2

`round30_defects.py` is a sound detector on the four routings it was written for **when read as a
one-way filter** (it kills the actual D2 and D3 defects, and D5's real absence), but its D3 lesson
clause, its D1 type+content predicate and its D5 key membership are each one-edit removable without
any output change, and D5/D2 accept content-free repairs — the counter has no failure-capable
selftest of its own, so C2's `defects=0` is necessary but not sufficient as evidence of closure.
