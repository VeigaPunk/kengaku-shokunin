# ConnSoujiKaidoku — sibling-overlap scan (round 25, C2 convention)

Read-only scan of `souji-shokunin/` and `kaidoku-shokunin/`. No sibling write; no install.

## Findings

**F1 — kaidoku `.ufo/gates/c1-census-v10.py` — ADJACENT (cite).** `:238` `0 PASS, 1 FAIL, 2 anchor failure`; `:239` `[--root|--json|--quiet|--selftest]`; `:255-293` explicit
`SCOPE` table of `file:start-end/origin/marker`, covering `PROVINCE.md`/`SKILL.md`/`SCORECARD.md` **only**:
no `SHONEN.md`, no `README.md` row — that absence is C2's honest novelty delta (P2c seed, P2e index).

**F2 — same file `:53-58` + `:67-70` — ADJACENT defect C2 MUST import.**
`:53-56` "a scoped file that cannot be read was absorbed as `lines=0 loci=0` … the run read PASS exit 0"
(measured: absent `SKILL.md`; same for zero-byte, truncated, directory, EACCES). `:67-70` fix = per-file
positive floor; C2's P2d `test -e` and P2e both-directions check share that silent-empty shape.

**F3 — kaidoku `.ufo/gates/citation-drift/citation-drift-probe.py:10-14,26-30` — DUPLICATE of P2b/P2c.**
Kinds `extracted|exact|anchor`; `extracted` "reads the number OUT of the citing line" and checks the target
line; `anchor` emits `citation_moved`; targets resolve "against Git objects, never the moving worktree".

**F4 — souji `tools/souji-landing-gate.py:31-34`, `:217-221` — ADJACENT, exit-map CONTRADICTION.**
`:217-221` "Any git failure that is not 'path absent' is EvalError (exit 2), never a finding (r17 S1)". C2 P2d
makes a failing `test -e` a mismatch (1) unless the row says `ABSENT`. Split: declared `ABSENT` = 0; bare
missing = 1; unreadable/unparseable = 2.

**F5 — souji `census/round-12/sources-census.sh:1-3` — DUPLICATE (verbatim fleet copy).**
"copied verbatim from … SOURCES-CONTRACT-v1.md"; bare greps, no `validate`. Canonical:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (modes census|validate|overdue|shared|selftest).

**F6 — `round-25-claims.md:103` — PATH HAZARD (fails as written).**
`scripts/sources-census.sh validate …` — `ls kengaku-shokunin/scripts` → `No such file or directory`.
Fleet tool `:16` exit map is four-valued (`… · 3 selftest failure`), so it cannot serve as C2's 0/1/2 contract.

**F7 — souji `census/round-13/count-claims.py:12-14`, `census/round-15/count-claims.py:1-8`,
`.ufo/waves/round-13/w1/BaselineMeasures.md:25` — ADJACENT (counting convention + hazard).**
Counting reads `git ls-tree`/`git show` "from that commit's tree … never … untracked material";
`BaselineMeasures.md:25` records the counterexample: `[ -e ]` "on the working tree, so an untracked F2 file
can satisfy a mined row". P2 must read `git show 6180e4f:<path>`; P2d must require tracked.

**F8 — `kumitate-shokunin/scripts/claims-check.mjs:52-55,139` — ADJACENT-REPORT-OUT (do not absorb).**
Re-derives SCORECARD claim cells (`NOTE_MISSING`, `SECTION_FILE_UNRESOLVED`); `0 match · 1 drift ·
2 fail-closed · 64 usage`. Adjacency row only; its `64` is not a convention to adopt.

**F9 — C1 prior art inside the fleet.** `kaidoku/.ufo/waves/round-14/w1/ReviewScoreContract.md:43` hand-computes
an exact CP interval ("2/2 detected: **[0.158, 1.000]**"); `.ufo/waves/kaika-w1/kengaku-art.md:149` carries
S011 `queued`. Instrument-scoped novelty survives; scope the sweep line; re-open S011 with a fresh quote.

## Rulings

| Path | Ruling | Action |
|---|---|---|
| kaidoku c1-census-v10.py (F1,F2) | adjacent | cite; claim SHONEN+README; import H1/G20 |
| kaidoku citation-drift-probe.py (F3) | duplicate | cite rev-pinned `extracted` convention |
| souji landing-gate.py (F4) | adjacent, contradiction | state 0/1/2 split |
| souji round-12/sources-census.sh (F5) | duplicate copy | cite fleet tool |
| claims doc :103 (F6) | path error | retarget fleet absolute |
| souji count-claims ×2 + BaselineMeasures :25 (F7) | adjacent + hazard | pin P2 to 6180e4f; no worktree `[ -e ]` |
| kumitate claims-check.mjs (F8) | report-out | adjacency row only |
| kaidoku r14 / kaika S011 (F9) | adjacent | scope sweep; re-open S011 |

VERDICT: C2's only true state-census precedent is kaidoku's `c1-census-v10.py`, which is blind to SHONEN and README (real delta) but whose H1 silent-empty class, plus souji's absent-path and selftest conventions, are fail-closed obligations C2 must import; F3/F5 are duplicates to cite, never rebuild. Installs: none.
