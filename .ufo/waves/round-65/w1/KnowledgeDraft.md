# KnowledgeDraft — round 65 w1 seat report (R65-C1 draft)

Seat: `KnowledgeDraft` (lane `kengaku`, round 65, wave w1, v1). Axis: coverage (C1, L0-capped).
Base tip `12a6255170bcc466029bf82037885fd69e20370f`.

## Behaviour

Drafted the two C1 artifacts the L1 lands on a `R65-C1` pass, and nothing else. No lane file was
edited: the only writes are two new files in this seat's directory under
`.ufo/waves/round-65/w1/KnowledgeDraft/`.

## Files written (both new, both in the seat dir)

1. `.ufo/waves/round-65/w1/KnowledgeDraft/tb2-sqlite-gcov-offline.md` — the knowledge entry the
   L1 lands at `corpus/knowledge/tb2-sqlite-gcov-offline.md` on a pass. 66 lines total (62 after
   the four provenance-trio lines), inside the ≤110-line body cap. Opens with the trio in the
   frozen order — `source: S232 …`, `verified-at: round 65 freeze (base 12a62551…; instrument
   receipt corpus/evidence/round65/sqlite-gcov-probe.txt)`, `recheck: python3
   plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt`
   — then `source: S233 …` for the amalgamation bytes. Body carries: the 3-leg contract with the
   grader's own assert texts and line numbers; the 5-case × 3-leg frozen vector table with each
   case's committed pre-freeze capture and digest; the two load-bearing mechanics (the
   `/dev/null` mask with its measured `PermissionError` surface; the compile-time-absolute
   `.gcda` path and the dual-bind / in-place-compile design); the class observation splitting
   `db-state` into toolchain-artifact state (`sqlite-with-gcov`, executed) vs query-plan/timing
   state (`query-optimize`, recipe-unexecuted); the named environment deltas.
2. `.ufo/waves/round-65/w1/KnowledgeDraft/skill-dbstate-flip.md` — the SKILL `db-state` row flip
   cell: the exact replacement row, a cell-by-cell diff against the base row, the gate
   requirement, and the scope of the change (one line of one file).

## Gates

| gate | command | result |
|---|---|---|
| provenance trio | `python3 -c "from round63_gate_checks import trio_missing; …"` on the draft entry | `trio_missing: []` — trio established in canonical order inside the window, before the first `## ` heading |
| source-id extraction | `re.compile(r"^source:[ \t]*(S[0-9]{3,})\b", re.MULTILINE)` over the draft | `['S232', 'S233']`, unique, in that order — matches `plans/adoption_check.py`'s `SOURCE_LINE_RE` expectation shape; both ids exist as registry rows in `corpus/SOURCES.md` |
| r63 depth gate, base | `python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt` | `ROWS n=16 class_match=True count_mismatch=0 paths total=26 resolved=26 share=1.00` / `PREDICATE R63-C2 pass` / exit 0 |
| r63 depth gate, flipped-row rehearsal | same gate, `--skill <scratch>/SKILL.md --root <scratch>` with the replacement row substituted verbatim from the flip cell | `ROWS n=16 class_match=True count_mismatch=0 paths total=28 resolved=28 share=1.00` / `PREDICATE R63-C2 pass` / exit 0 — the two new path tokens resolve, so the flip keeps the gate green on the same terms as the base row |

The flipped-row rehearsal ran entirely in scratch (`/fast/scratch/hyaku/kengaku-r65/KnowledgeDraft/gate-test`):
a symlink mirror of the lane's `corpus/` and `plans/` trees, stand-in files for the two paths
that exist only after the landing, and a scratch copy of `SKILL.md`. The lane's `SKILL.md` was not
edited — `git diff --stat -- SKILL.md` is empty. The rehearsal prices the flip's table mechanics
only; it says nothing about the predicate.

## Touched surfaces

- `.ufo/waves/round-65/w1/KnowledgeDraft/tb2-sqlite-gcov-offline.md` (new)
- `.ufo/waves/round-65/w1/KnowledgeDraft/skill-dbstate-flip.md` (new)

Nothing else. `SKILL.md`, `corpus/SOURCES.md`, `corpus/knowledge/`, `plans/round-65-claims.md`,
`corpus/evidence/round62/class-survey.txt` and the r62/r65 census receipts are untouched.
Scratch `/fast/scratch/hyaku/kengaku-r65/KnowledgeDraft/` was removed after the receipts above
were captured into this report.

## Out of scope (deliberately not done)

- Landing the entry at `corpus/knowledge/tb2-sqlite-gcov-offline.md`, editing `SKILL.md`, adding
  the `corpus/README.md` index row, and flipping S232/S233 `queued`→`mined` with `used-by` — all
  L1 work on a pass.
- Building `plans/round65_c1_sqlite_probe.py` and producing the receipt
  `corpus/evidence/round65/sqlite-gcov-probe.txt` — other seats' work; neither file exists yet in
  the lane, so the counting command cannot have been run by this seat.
- The dated LOG.md flip note and the round-65 lesson — other seats' work.
- Any edit to the frozen claims doc, the frozen vectors, the counters or the kill rules.

## Findings

- **The r63 depth gate constrains the flip's pointer cell.** `plans/round63_gate_checks.py`
  (`COLS=5`, `EXPECTED_CLASS_ROWS=16`) requires exactly five cells, an integer count cell equal to
  the census count, and a pointer cell whose backticked path tokens resolve under the lane root.
  The replacement row satisfies all three; the count cell stays `2`, so member counts are
  untouched.
- **The two new path tokens raise the gate's path total from 26 to 28.** Both must resolve at the
  landing tip — `plans/round65_c1_sqlite_probe.py` and `corpus/evidence/round65/sqlite-gcov-probe.txt`.
  They are the same two artifacts C1 produces, so they land with the flip; but if the L1 applies
  the row before the probe and receipt are committed, the gate's `share` drops and the row must
  wait. The rehearsal above reproduces the green case with stand-in files.
- **The class row's `executed` cell is the census statement, and the census is frozen.** The
  `db-state` count `2` comes from `corpus/evidence/round62/class-survey.txt` line 16
  (`CLASS db-state count=2 members=query-optimize,sqlite-with-gcov`) and is NOT re-measured. The
  flip changes only the `executed` cell to `executed 1 of 2`, naming `query-optimize` as still
  recipe-unexecuted with its reason.
- **The `query-optimize` reason is verifiable in committed bytes**, not asserted: the grader
  `corpus/evidence/round52/graders/query-optimize/tests/test_outputs.py` carries the median-ratio
  threshold at line 142 (`assert summary["solution"]["median_s"] <= 1.05 * summary["golden"]["median_s"]`)
  and the sha-pinned external database at line 78 (`expected_hash = "89eab7555b6b86a74b8e0ee5a7db7beec0b2575a45cd2b22fe132eae79f5ad5a"`
  over `/app/oewn.sqlite`). A median-ratio wall-clock threshold plus a sha-pinned external input
  is why those legs are not freezable offline on this host.
- **The entry's opening needs two `source:` lines, not one.** `plans/adoption_check.py` counts
  cited rows via `^source: (S\d+)` and requires the declared set to equal the expectation's set
  exactly; `S232` (the grader) and `S233` (the amalgamation) are distinct registry rows, so both
  are declared. The trio gate reads only the FIRST occurrence of each trio key inside the window,
  so the second `source:` line does not disturb it — confirmed by `trio_missing: []`.
- **G3 has no committed pre-freeze capture.** The four committed captures are G1, G2, G4, G5; G3's
  cell is frozen in the claims doc and is exercised by the scored battery. The entry says so
  rather than implying a capture exists.
- **Two host facts worth carrying into the L1's lesson:** under the `/dev/null` mask the grader
  raises `PermissionError: [Errno 13]` rather than `FileNotFoundError` (the masked path exists and
  is merely non-executable), and the host `sqlite3` 3.54.0 answers legs 1-2 in G5 while the
  lane-built binary reports 3.54.1 in G1/G4 — the two are distinguishable in the receipts.

## Tooling

No installs were performed. `pacman` was not touched (host-wide pause per the orchestrator
addendum), no PyPI open was made, and no port was bound. The host toolchain already provided
everything used: `gcc`/`gcov` 16.2.1, `bubblewrap` 0.13.1, `Python` 3.14.8, `uv` 0.13.0,
`sqlite3` 3.54.0 — all read from `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-65/w1/GraderRecon/host-state.txt`
and re-observed by this seat.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-65/w1/KnowledgeDraft/tb2-sqlite-gcov-offline.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-65/w1/KnowledgeDraft/skill-dbstate-flip.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-65/w1/KnowledgeDraft.md` (this report)
