# S5Connections — the chess entry's connections and limits sections (draft for E7)

Seat: `S5Connections` (connector/scribe, leaf, read-only). Date: 2026-10-30.
Lane repo: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, base tip
`80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (round-55 freeze; base `798f5e9e`).
Consumed by seat `E7KnowledgeEntry` (writer of `corpus/knowledge/tb2-chess-best-move-grader.md`).

Every claim below is tied to a named held file in this lane repo. Paths are lane-relative.
Nothing in this file was written by this seat except this file and the two receipts named in
§Evidence. The lane tree was read only; no git mutation was run.

---

## 1. Connections

One line each; each names what the chess entry **extends** and what it **never overwrites**.

1. **`corpus/knowledge/tb2-password-recovery-grader.md`** (r45) — extends that entry's
   *artefact* class (an agent-written text file whose contents the grader reads) with a second
   **comparison relation** over the same artefact kind, and never overwrites r45's own reading:
   r45's `## Predictor` block, its 16-case receipt, and its `## Errata (round 46)` items 1–5
   stay as written, and r45 remains the *second* F1 exemplar it calls itself
   (`tb2-password-recovery-grader.md:17-18`, "Its grader is the second exemplar of the
   **F1 constant-compare family**"). The chess grader is **not** a third F1 exemplar under
   r45's own wording
   (membership of one constant among a file's lines, `test_outputs.py:18`); it is a
   two-literal **multiset** comparison — see §3.
2. **`corpus/knowledge/tb2-polyglot-c-py-grader.md`** (r46) — extends the lane's
   executed-exemplar count from twelve to thirteen and its graded-artefact taxonomy with a
   class that is **not** executed by the grader, and never overwrites r46's dual-runtime class
   claim (r46's `## Class difference` sibling text and its `## Errata (round 46)` items 1–2):
   the chess grader neither compiles nor runs the graded bytes, so r46's narrowed claim that
   "no earlier exemplar *compiles* the graded artefact or runs the same bytes under two
   language runtimes" is untouched, and the chess entry claims no execution of its own.
3. **`corpus/knowledge/benchmark-verifier-execution-model.md`** — extends that entry's
   *runner-semantics* reading by one task and nothing else: the chess `tests/test.sh` is
   **byte-identical** to the held regex-log runner (`cmp` exit 0; both sha256
   `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334`, i.e. row **S109**), so
   the chess entry cites S109 for the harness reward mapping
   (`chess-best-move/tests/test.sh:18-22` uvx/pytest, `:25-28` → `/logs/verifier/reward.txt`)
   and opens **no third runner row** (round-55 Amendment A1). It never overwrites that
   entry's shared-mode resolution, `/tests` re-upload guarantee, or SWE-bench-Pro log-scan
   reading, and it makes **no claim** about where or how Harbor runs this verifier.
4. **`corpus/knowledge/tb2-grader-vacuity-triage.md`** (r52) — extends that entry's population
   triage from "89 graders classified as files" to "one of those 89 additionally read
   end-to-end and executed offline", and never overwrites the triage's counts or its
   `not admitted` verdict (`c1-after.txt`: `TASKS total=89`, `classified=88`,
   `presence_only_tests=33 tasks_with_presence_only=27`, `CANDIDATES total=29`): the
   chess-best-move grader is **not** among the 29 candidates and **not** among the 30 blind
   labels in `corpus/evidence/round52/labels.json`, and the chess entry therefore neither
   claims nor implies presence-only weakness. Recomputed with the committed classifier
   (`plans/round52_c1_grader_audit.py`, imported by this seat): file class **V3**
   (content-check), its single test **P3** (content/value) — see §Evidence.
5. **`corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md`** (r44) — extends the lane's
   *constant-compare family discussion* with the chess grader as a **contrast case** and never
   overwrites r44's class definition or its "Class difference from the round-43 feal entry"
   section; note the definitional overlap flagged in §4 item 1 below, which the L1 must rule on
   before the entry is admitted (this seat does not rule).

### Prior ground already held, which the chess entry must cite rather than re-derive

6. **`.ufo/waves/round-44/wave/R44LabratF1Leak/receipts/chess-derive.txt`** (tracked file) —
   already derives the position's checkmate-in-one set as `['e2e4', 'g2g4']` and records
   `grader expects ['e2e4', 'g2g4'] match True`. The chess entry may reference this as
   prior-art derivation; it must not restate it as its own finding, and it must not thereby
   claim to have established the image's contents.
7. **`.ufo/waves/round-45/attempt1-unclaimed/corpus/evidence/round45/f1-census/chess-best-move/`**
   (tracked; `sha256sum -c SHA256SUMS` over 107 lines → exit 0, all `OK`) — already holds the
   **whole task tree**: `instruction.md` (sha256 `6ba25be4…19ce7a`, the same digest as the
   round-55 S202 fetch), `task.toml`, `README.md`, `solution/solve.sh`, `environment/make.py`
   (the board generator, whose FEN literal is at `environment/make.py:118`) and
   `environment/Dockerfile`. The chess entry's `source:` rows should cite these held bytes
   rather than re-fetch. **Caveat for the L1:** `corpus/lessons/round-45.md:4` designates
   `.ufo/waves/round-45/attempt1-unclaimed/` as *"discarded drafts"* from the aborted round-45
   attempt 1, while git tracks all 113 files under it and their digests verify. Whether this
   tree is citable ground is an L1 decision this seat does not make; the entry should not cite
   it as admitted ground until that is ruled.
8. **`.ufo/waves/round-45/attempt1-unclaimed/plans/census-spec-r45.json`** — already names
   chess-best-move's `decide_lines: [25]` and `tokens_decide: ["g2g4","e2e4"]`, i.e. the exact
   assertion and token pair this round's grader is read for. The chess entry is the first to
   *execute* that assertion; it is not the first to *locate* it.

---

## 2. Limits — the full refusal list (PROVINCE round-37 style, adapted)

It records how that captured grader answers those synthetic states only: it does not run
Terminal-Bench, the task image (`task.toml:29` names `alexgshaw/chess-best-move:20251031`;
`allow_internet = true` at `:34`; the image is never pulled) or a harness (`tests/test.sh`'s
`uvx -p 3.13` / pytest 8.4.1 path and its `/logs/verifier/reward.txt` write are **read, not
run** — the runner is byte-identical to the held regex-log runner, S109), or a real
submission; it does not validate or certify a task, measure difficulty or gameability, judge
the assertion's correctness, measure contamination, or speak for the remaining **76** TB2 task
graders (89 carry `tests/test.sh`; **13** are read after this round). No capability row is
claimed (an instrument probe is not a capability; the round-52 ruling).

Additions that this entry's own evidence makes necessary, each tied to a held file:

- **No chess correctness is established.** `tests/test_outputs.py:10-20` is the authors' own
  docstring ("optimal checkmate-in-one moves"); the grader's two literals are the authors'
  assertion about their own fixture, and the entry compares the grader to itself, not to a
  board. The derivation of `['e2e4','g2g4']` as the mating set exists in the lane
  (`.ufo/waves/round-44/wave/R44LabratF1Leak/receipts/chess-derive.txt`) but is that receipt's
  ground, not this entry's.
- **No model behaviour, pass rate, or trajectory** is measured. The 12 frozen cases are
  constructed end states (`corpus/evidence/round55/chess-best-move-probe.txt:1-12`), not agents.
- **Host substitutes for the image.** Host `python3` stands in for the image's python; pytest
  itself is not run — the probe reproduces the one test function's verdict, which is the only
  thing `tests/test.sh:25-28` rewards. The board image is never rendered and never read; the
  FEN that generates it is only in the environment capture (§1 item 7), not in the graded path.
- **The 12 cases never exercise an absent or non-regular `/app/move.txt`.** The grader reads
  the file at `test_outputs.py:23` with no existence check of its own, so an absent file raises
  `FileNotFoundError` and a directory raises `IsADirectoryError` — and the frozen probe's own
  classifier (`plans/round55_c3_chess_probe.py:126-130`) maps any nonzero exit **without**
  `AssertionError` to `SETUP`, which aborts the whole run with exit 2 rather than recording a
  verdict. Recomputed by this seat against the committed probe module: missing file → `SETUP`
  (rc 1); empty file → `F` (rc 1, `AssertionError`). The frozen table has `empty-file` but no
  absent-file case, so r45's `nop` analogue does not exist here — this is a gap in the case
  table, not a property of the grader.
- **The probe is offline and synthetic.** Each case runs the captured grader in a per-case
  bubblewrap sandbox with a case-owned `/app` and `/tests` bound read-only; no network, no
  container, no task certification (`plans/round55_c3_chess_probe.py:7-16`).

---

## 3. Class boundary — r45 line-split membership vs r55 full-multiset equality

The two graders read the same artefact *kind* (an agent-written text file) and decide by
comparing it to embedded literals, but the **comparison relations are incomparable** — neither
implies the other, so r55 is not a stricter or looser r45.

**r45 — `password-recovery`** (`corpus/evidence/round45/tb2-password-recovery/test_outputs.py`):

```python
guesses = Path("/app/recovered_passwords.txt").read_text().strip().split("\n")   # :14
assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses, "Password not found"                 # :18
```

**r55 — `chess-best-move`** (`corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py`):

```python
move = Path("/app/move.txt").read_text().strip().split()                          # :23
assert sorted(move) == sorted(["g2g4", "e2e4"]), "File is wrong"                  # :25
```

The exact semantic differences, on the four axes the round's claim names:

1. **Partial credit — r45 grants it, r55 does not.** r45's operator is membership (`in`), so
   one correct line among any number of other lines suffices and every wrong line is invisible
   (r45's own receipt: `decoys-1000` is observed `pass`; `constant-joined` fails only because
   the constant is no longer a whole line). r55's operator is equality of two sorted lists, so
   the token multiset must be exactly `{g2g4, e2e4}`: `single-move-only` is observed `fail`
   (`chess-best-move-probe.txt:4`) — producing one of the two winning moves earns nothing.
2. **Order — free in both, but purchased differently.** r45 never compares order at all
   (`in` on a list). r55 compares `sorted(move)` with `sorted([...])`, so order is free
   (`reversed-order` observed `pass`, `:3`). The difference is not in order but in what
   order-freedom costs: r45's order-freedom comes with freedom over count, extra content and
   duplicates; r55's order-freedom is bought with exactness on all three.
3. **Duplicates — invisible to r45, fatal to r55.** r45's membership cannot see multiplicity:
   the same correct line repeated a thousand times still passes. r55 compares sorted *lists*,
   so multiplicities count — `duplicate-move` (`g2g4\ne2e4\ne2e4`) is observed `fail`
   (`:7`), and a duplicated token cannot stand in for a missing one.
4. **Normalization — different separator sets, and no case/width/Unicode folding in either.**
   r45 tokenizes by **line**: `split("\n")` after `read_text()`'s universal-newline
   translation (`\r\n` and a lone `\r` both become `\n`), so the separator set is exactly
   `U+000A` and a token must occupy a whole line (`constant-joined` fails). r55 tokenizes by
   **whitespace run**: `split()` with no argument separates on all 29 Unicode whitespace code
   points (space, tab, LF, CR, FF, VT, `U+0085`, `U+00A0` NBSP, `U+2000`–`U+200A`,
   `U+2028`/`U+2029`, `U+202F`, `U+205F`, `U+3000`), so `g2g4 e2e4` on one line is two tokens
   (observed `pass`, `:2`) where r45 would have seen one line. Neither grader applies case
   folding, digit-width folding or Unicode normalization: r55's `uppercase-white` and
   `fullwidth-unicode-digit` are both observed `fail` (`:5`, `:12`), and r45's `lower23`
   fails. A further consequence: r55's tokens must be whitespace-*separated*, so a joined
   `g2g4e2e4` on one line is a single token and fails. That joined state is **not** one of
   the 12 frozen cases (the frozen table is `plans/round55_c3_chess_probe.py:54-79`); it is
   measured only in this seat's own probe (§Evidence), and the receipt therefore does not
   carry it.
5. **Consequence — the two relations are incomparable.** `"g2g4 e2e4"` satisfies r55 and
   violates r45's line-membership shape; `"g2g4\nnope\n"` satisfies r45's shape and violates
   r55. Verified by this seat over 16 byte-level states (§Evidence): the two shapes disagree
   on 7 of 16, and each has a witness the other rejects.

What the r55 class **is**, stated positively: the graded artefact is an agent-written
**token file** judged by **order-insensitive full-multiset equality over whitespace-split
tokens** — the token multiset must equal the literal multiset exactly, with no partial
credit, no duplicate tolerance, and no case, digit-width or Unicode normalization. In the
lane's own vocabulary this is a *content-check* class, distinct from r44's whole-file
substring membership, r45's line membership, r36's **ordered** list equality
(`corpus/evidence/round36/tb2-regex-log/test_outputs.py:90`, `matches == expected_dates`),
r40's `ids == sorted(ids)` ordering check plus separate uniqueness check
(`corpus/evidence/round40/tb2-db-wal-recovery/test_outputs.py:44`, `:89`), and r46's
dual-runtime stdout equality.

---

## 4. Open items for the L1 / E7 (not decided by this seat)

1. **F1-family definitional overlap.** r44 names its family "a constant compare that cannot
   tell how the constant was obtained" (`corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md:78-80`),
   and r45 names itself the family's *second* exemplar. The chess grader is also a comparison
   against embedded literals, but by exact multiset rather than membership. The round-55 claim
   calls it a "graded artefact class new to this lane" and the landed README row calls it
   "distinct from round 45's line-split membership"
   (`corpus/README.md:84`). Under r44's own wording the chess grader is arguably F1-adjacent,
   so the entry should state which reading it takes and must **not** silently reclassify r44
   or r45. L1 ruling wanted.
2. **Citation status of the round-45 attempt-1 tree** (§1 item 7): tracked and
   digest-verified, but labelled "discarded drafts" in `corpus/lessons/round-45.md:4`.
3. **The refusal count in the seat brief was stale.** The brief asked for "86 graders still
   unread", which is round 37's figure (3 of 89 read, `PROVINCE.md:277`). At the round-55
   landing revision the correct figure is **76 remaining, 13 of 89 read**
   (`corpus/README.md:445`; the round-55 claim narrows "12 of 89 read" → "13 of 89"). The
   section above uses 76/13. Flagged rather than silently followed.
4. **Case-table gap** (§2): an absent `/app/move.txt` is a probe `SETUP`, not a verdict; if the
   L1 wants r45's `nop` analogue, the frozen case table must be amended as data before the
   after-run, not after.

---

## 5. Coverage delta against the entry E7 landed (for the L1)

`corpus/knowledge/tb2-chess-best-move-grader.md` landed while this seat was drafting (writer
`E7KnowledgeEntry`). It was written **independently** — it does not reference this file, and it
does not name any of the three "prior ground already held" items in §1. The entry is sound on
everything it does cover; the delta below is what it does **not** cover, stated so the L1 can
fold in what it wants before admission. **This seat did not and will not edit E7's file.**

| my item | covered by E7's landed entry? | note |
|---|---|---|
| §1.1 connection to r45 (`tb2-password-recovery-grader.md`) | **yes** — the entry's `## Connections` names `[[tb2-password-recovery-grader]]` and states the membership-vs-multiset distinction | my version additionally pins the F1-family overlap for an L1 ruling (§4.1), which the entry does not raise |
| §1.2 connection to r46 (`tb2-polyglot-c-py-grader.md`) | **no** — `grep -c polyglot` = 0 | the entry nowhere says it extends the executed-exemplar count 12→13 or that r46's dual-runtime class and its 2-item round-46 Errata are untouched |
| §1.3 connection to `benchmark-verifier-execution-model.md` | **yes** — `[[benchmark-verifier-execution-model]]` is named, with the S109 bridge | my version adds the explicit "never overwrites the shared-mode / `/tests`-upload / log-scan readings" clause; the entry's own Negative-space bullet "the runner's consumption" covers the same ground in the negative direction |
| §1.4 connection to the r52 triage (`tb2-grader-vacuity-triage.md`) | **no** — `grep -c triage`/`vacuity` = 0 | the entry does not record that its task is one of the r52 population's 89, is **not** among the 29 candidates nor the 30 blind labels, and carries the committed classifier's V3/P3 class (recomputed by this seat, §Evidence) — i.e. it is not a presence-only grader |
| §1.5 connection to r44 (`tb2-feal-linear-cryptanalysis-grader.md`) | **no** — `grep -c feal-linear` = 0 | same F1-family ruling as §4.1 |
| §1.6–1.8 prior ground: the r44 derivation receipt, the round-45 attempt-1 tree (whole task tree incl. `instruction.md` at the S202 digest), the round-45 census spec naming `decide_lines: [25]` | **no** — `grep -c R44LabratF1Leak\|attempt1\|f1-census` = 0 | the entry is thus the first in the lane to *execute* the assertion but does not record that r44 had already *derived* the pair `['e2e4','g2g4']`, nor that the chess task tree was already captured and digest-verified in-repo |
| §2 refusal list, r37-PROVINCE style (no image run, no harness run, no real submission, no task validity, no contamination, no model behaviour, remaining-grader count) | **partly** — the entry's `## Negative space` has 7 bullets covering chess correctness, task validity, the image's content, model/agent performance, contamination, the other 88 tasks, and the runner's consumption; it has **no `## Limits` section** and no "the harness's `tests/test.sh` was read, not run" statement in the refusal list (that fact appears once, in `## What test.sh does with the outcome`) | the entry's bullet "this is one task of 89 (the 13th grader … the frontier count moves 12 → 13 of 89, nothing more)" carries the count in the positive form; the r37 form's "remaining **76** … (89 carry `tests/test.sh`; **13** are read)" is what §2 gives, and the count itself is correct in both |
| §2 additions: host python3 stands in for the image's python and pytest is not run; the probe is offline and synthetic | **partly** — the entry's `## Source labels` says "under the host Python, inside a bubblewrap sandbox with the capture bound read-only at `/tests`" | the entry does not say in its limits that pytest itself is not run |
| §2 addition: **the 12 frozen cases never exercise an absent or non-regular `/app/move.txt`** (absent → `FileNotFoundError` → probe `SETUP` → whole run exit 2; a directory → `IsADirectoryError`), so r45's `nop` analogue does not exist in this round's evidence | **no** — the only hit for `absent\|missing\|nop\|FileNotFound\|setup` in the entry is the word "missing" in the multiset sense ("missing, extra, duplicated, case-shifted, width-shifted", `## Negative space`); no absent-file case, no `SETUP`, no `FileNotFoundError` | this is the one substantive limits item in this draft that the landed entry does not carry at all; §4.4 states the consequence for the L1 |
| §3 class boundary: partial credit / order / duplicates / normalization, each tied to receipt rows | **partly** — the entry's `## Mechanism` (5 numbered properties) covers all four axes against the receipt rows, and its `## Class note (the r45 distinction)` states the membership-vs-multiset boundary | the entry does not state the **incomparability** consequence (neither relation implies the other; witnesses `"g2g4 e2e4"` and `"g2g4\nnope\n"`), nor the exact separator-set difference (r45 `U+000A` only, after universal-newline translation; r55 all 29 Unicode whitespace code points) as a *named* difference — it says "one per line is enforced only as a token discipline" |

Everything E7 covers is correct as written; the rows above are gaps in *coverage*, not errors in
the landed entry. This seat's own §1–§3 remain the fuller draft, and §5 exists so the L1 can
decide what to fold in before admission.

---

## Evidence

Receipts written by this seat (copied into this seat's wave dir before the scratch was
removed):

- `.ufo/waves/round-55/w1/S5Connections/semdiff-class-boundary.py` — the class-boundary probe:
  transcribes both graders' predicates from the committed captures, compares the two shapes
  over 16 byte-level states, and reports the whitespace-separator set, the folding
  (non-)behaviour, the multiplicity semantics and the two incomparability witnesses.
- `.ufo/waves/round-55/w1/S5Connections/semdiff-class-boundary.out` — its output
  (`r55 predictions reproduced: 16/16 (mismatches=0)`; `shapes disagree on 7/16 cases`).

Re-runnable commands this seat ran (all read-only against the lane; no git mutation):

| command | exit | result |
|---|---|---|
| `sha256sum corpus/evidence/round52/graders/chess-best-move/tests/{test_outputs.py,test.sh}` | 0 | `a540714e…b8f286`, `4770437e…6c334` — match the frozen pins |
| `cmp corpus/evidence/round52/graders/chess-best-move/tests/test.sh corpus/evidence/round52/graders/regex-log/tests/test.sh` | 0 | identical (S109 runner identity) |
| `(cd .ufo/waves/round-45/attempt1-unclaimed/corpus/evidence/round45/f1-census && sha256sum -c SHA256SUMS)` | 0 | 107 lines, all `OK` |
| `grep "chess-best-move" SHA256SUMS \| sha256sum -c -` (same dir) | 0 | 9 chess files `OK` |
| `sha256sum .ufo/waves/round-45/attempt1-unclaimed/.../chess-best-move/{instruction.md,task.toml}` | 0 | `6ba25be4…19ce7a`, `d8f01d3c…2f9e` — the same digests E14 fetched upstream |
| `python3 -c "import importlib.util; … round52_c1_grader_audit.classify(<chess capture>)"` | 0 | file class `V3`, per-test `P3` |
| `python3 semdiff-class-boundary.py` | 0 | 16/16 r55 predictions reproduced; 7/16 shape disagreements; witnesses printed |
| probe-module check: import `plans/round55_c3_chess_probe.py`, call `run_in_sandbox` on a missing-file and an empty-file case | 0 | missing → `('SETUP', 1)`; empty → `('F', 1)` |

Tooling: no installs, no upgrades, no network calls beyond what is quoted above (none).
Scratch root `/fast/scratch/hyaku/kengaku-r55/S5Connections/` was removed after the receipts
were copied in.
