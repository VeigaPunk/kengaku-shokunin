# R30FxQ13Fixture — Q13/Q14/Q15 pre-landing proof in a throwaway repo

Seat: `L1Kengaku30.R30FxQ13Fixture-3` (executor, leaf). Item: prove, before the round-30 admitting
commit exists, whether that commit will satisfy `corpus/QUALITY.md` Q13/Q14/Q15 as implemented by
`plans/gate_timing_check.py`. No lane edits: every write outside this report went to
`/tmp/r30fx-q13fixture/`. No installs, no upgrades, no pacman transaction.

Candidate under test: `corpus/knowledge/contamination-transparency-card.md` (entry `writer: KengakuR30`).

VERDICT: FAIL — the round-30 Gate as committed today does not satisfy Q13; the checker exits 1 at
both pinned sandbox snapshots, one cited report can never pass as written, and four cited reports do
not exist yet. The identical checker exits 0 on the repaired Gate plus committed reports (proof in §6),
so the landing is fixable without touching the check.

---

## 1. What I actually built

The round-30 bytes are **uncommitted** (`git ls-tree -r --name-only HEAD -- .ufo/waves/round-30` →
0 paths), so "the lane tip" is *commit `363a4eb` + the dirty working tree*. Each snapshot was built as:

```sh
git -C <lane> archive 363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db | tar -x -C /tmp/r30fx-q13fixture/<snap>
git -C <lane> status --porcelain=v1 -uall | cut -c4- > files.txt      # 74 dirty paths at 07:40Z
rsync -a --files-from=files.txt <lane>/ /tmp/r30fx-q13fixture/<snap>/
cd /tmp/r30fx-q13fixture/<snap> && git init -q -b main && git add -A && git commit -q -m "…"
```

The checker used is the snapshot's own copy of `plans/gate_timing_check.py`,
`sha256 51c18a9e…b80a2a`, byte-identical to the lane's (`sha256sum` on both → same digest). Runs are
`python3 plans/gate_timing_check.py --lesson corpus/lessons/round-30.md --commit <sha>` with `cwd` =
the snapshot; `--repo` therefore defaults to the snapshot root, not the lane.

Pinned snapshots (the lane moved twice while I measured — its Gate row and report dir are being edited
by live peers — so every claim below is anchored to a hash):

| snapshot | sandbox commit | lesson sha256 | falsify registry sha256 | falsify `.md` in commit |
|---|---|---|---|---|
| S3 | `c61e24db3fe2cc49c7b1dad35be2e6671e92fc51` | `ad5bd018…98ee2` | `86bbd41f…9c5cf` | 3 (`DeadSeats`, `SrcS081`, `SrcS082`) |
| FINAL (07:41:28Z) | `5d79c82486123705b8dfa8717797b60253fa34c0` | `f32d5c2a…7e2e4` | `86bbd41f…9c5cf` | 4 (+ `Quotes`) |

Earlier snapshot A (`d6b4593`, lesson `…` pre-rewrite, **zero** falsify reports) is kept as the
red-before control.

## 2. The run, as-is (S3 — paste of stdout, exit code after)

```console
$ cd /tmp/r30fx-q13fixture/s3 && python3 plans/gate_timing_check.py \
      --lesson corpus/lessons/round-30.md --commit c61e24db3fe2cc49c7b1dad35be2e6671e92fc51
FAIL line 17 Gate admit: candidate='corpus/knowledge/contamination-transparency-card.md'
  cell[reason]: the design-vs-rival flip is met by mapping every field into the round-6 union table's own columns and declaring the delta (S1, S2 fields; R1's value set) instead of presenting a format; all six cited sources re-opened 2026-10-25 with ≤25-word located quotes; Q1 triad rebuilt (`verified-at: 2026-10-25`, `writer: KengakuR30`); the staged table the mapping reads is labelled unlanded, so no load-bearing claim rests on it (Q2). Second-seat re-reads for this admission: `.ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md` (VERDICT line), `.ufo/waves/round-30/falsify/R30FxEntryQ1Q3.md`, `.ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md`, `.ufo/waves/round-30/falsify/R30FxQuotes.md`, and the six per-source re-reads `.ufo/waves/round-30/fals…
  cited seat-report paths: '.ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md', '.ufo/waves/round-30/falsify/R30FxEntryQ1Q3.md', '.ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md', '.ufo/waves/round-30/falsify/R30FxQuotes.md', '.ufo/waves/round-30/falsify/R30FxSrcS081.md', 'R30FxSrcS086.md'
  existing returned second-seat report(s): .ufo/waves/round-30/falsify/R30FxSrcS081.md
  invalid cited second-seat report: .ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md (absent from commit tree)
  invalid cited second-seat report: .ufo/waves/round-30/falsify/R30FxEntryQ1Q3.md (absent from commit tree)
  invalid cited second-seat report: .ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md (absent from commit tree)
  invalid cited second-seat report: .ufo/waves/round-30/falsify/R30FxQuotes.md (absent from commit tree)
  unresolved bare report reference(s): R30FxSrcS086.md
  reasons: one or more cited second-seat reports fail identity/return checks; one or more bare report references do not resolve uniquely
gate_timing_check: commit=HEAD lesson=corpus/lessons/round-30.md admissions=1 passed=0 failed=1 second-seat-reports=3
EXIT=1
```

Same command at FINAL — one failure has *changed class*, which is the finding that matters:

```console
  existing returned second-seat report(s): .ufo/waves/round-30/falsify/R30FxSrcS081.md
  invalid cited second-seat report: .ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md (absent from commit tree)
  invalid cited second-seat report: .ufo/waves/round-30/falsify/R30FxEntryQ1Q3.md (absent from commit tree)
  invalid cited second-seat report: .ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md (absent from commit tree)
  invalid cited second-seat report: .ufo/waves/round-30/falsify/R30FxQuotes.md (report has no anchored VERDICT line; return is not established)
  unresolved bare report reference(s): R30FxSrcS086.md
gate_timing_check: commit=HEAD lesson=corpus/lessons/round-30.md admissions=1 passed=0 failed=1 second-seat-reports=4
EXIT=1
```

`R30FxQuotes.md` **exists and is cited**, and it still fails: it deliberately emits no verdict —
its own tail reads "No `VERDICT:` line is emitted here: this seat is neither the source re-read nor
the complete-set review". `R30FxDeadSeats.md` does the same on purpose ("`VERDICT:` line is
deliberately **not** emitted"). Both are correctly self-described but structurally unusable as a Q10
return, and `R30FxQuotes.md` is currently cited by the Gate. That red does not depend on any missing
file: it will persist after the falsify wave finishes.

## 3. Which report path and registry role the checker accepted

Accepted for real (committed wave output, not my bytes):

- **`.ufo/waves/round-30/falsify/R30FxSrcS081.md`**, registry seat `R30FxSrcS081`, role **`scout`** —
  counted as `existing returned second-seat report(s)` in both snapshots; its
  `VERDICT: PASS corpus/knowledge/contamination-transparency-card.md — …` line is at file line 255.
- **`.ufo/waves/round-30/falsify/R30FxSrcS082.md`**, role **`scout`** — proven sufficient *alone*: a
  sandbox-only mutant of the Gate row whose reason cell cites only `falsify/R30FxSrcS082.md` exits 0:

```console
PASS line 17 Gate admit: candidate='corpus/knowledge/contamination-transparency-card.md'
  cited seat-report paths: 'falsify/R30FxSrcS082.md'
  existing returned second-seat report(s): .ufo/waves/round-30/falsify/R30FxSrcS082.md
gate_timing_check: commit=HEAD lesson=corpus/lessons/round-30.md admissions=1 passed=1 failed=0 second-seat-reports=8
EXIT=0
```

Rejected for real: `R30FxQuotes.md` (role `scout`, no VERDICT line — §2) and, when I forced a
citation to it, `R30FxQ13Fixture.md` (this seat, role **`executor`**):
`(seat role 'executor' is not an allowed read-only reviewer)`. Reclassifying the same seat to
`reviewer` in a sandbox-only registry edit flips that run to exit 0 — the role string, not the
content, is the gate.

Registry census at both snapshots (`.ufo/waves/round-30/falsify/swarm-registry.json`, sha
`86bbd41f…`): 33 members — 12 scout, 8 reviewer, 5 critic, 1 revenger (**26 citable**) and 7 not
citable (5 executor, 1 mutation-tester, 1 connector). Every `agentId` is `null`, so Q14's identity
ladder reduces to the role string plus any `writer:`/`author:` declaration inside the report.

## 4. Why the current Gate cannot pass (three named blockers)

1. **A cited seat that is structurally incapable of a return.** `R30FxQuotes.md` is bookkeeping, says
   so, and carries no `VERDICT:` line; Q13/Q14 require an anchored verdict. Fix: stop citing it in the
   `reason` cell (it may stay cited in the prose §Round 30 admission and in the `read` column, which the
   checker never reads). Do **not** make a bookkeeping seat emit a verdict to satisfy a machine — that
   would assert a re-read the seat did not do.
2. **Four cited reports have not returned**: `R30FxEntryCompleteSet.md`, `R30FxEntryQ1Q3.md`,
   `R30FxEntryQ4Q6.md`, `R30FxSrcS086.md`. All-or-nothing: dropping just one (`S3D` below) keeps exit 1.
3. **One citation is written bare.** `… `.ufo/waves/round-30/falsify/R30FxSrcS081.md` …
   `R30FxSrcS086.md`` — the second path lost its `falsify/` prefix at the ellipsis, so the checker
   resolves it as a *bare name* (unique-basename rule) and reports
   `unresolved bare report reference(s): R30FxSrcS086.md` while the file is absent. It resolves once
   the file lands (proved in §6), but any same-named file under `build/` later makes it ambiguous.
   Write the full path.

Two things the current Gate already gets right, so they need no edit: the candidate cell is exactly
`corpus/knowledge/contamination-transparency-card.md`, and the citations sit in the **`reason`** column
(an earlier revision had them only in the 4th `read` column, which `audit_admission` never parses —
that revision also had candidate `contamination-transparency-card.md (package)`, which fails as
`admitted candidate is absent from the commit tree`).

## 5. Variant matrix (each a commit in `/tmp/r30fx-q13fixture/`)

| # | mutation | exit | decisive line |
|---|---|---|---|
| A | lane tip bytes, no falsify report, old Gate row | **1** | `candidate='contamination-transparency-card.md (package)'`; `cited seat-report paths: none`; `second-seat-reports=0` |
| B | + this seat's report (executor) only | **1** | `second-seat-reports=1`, still no citation |
| V1 | old Gate row repaired, citing the name the prose used (`falsify/FxEntryCompleteSet.md`) with that file present | **1** | `(seat is not in the committed wave registry)` — stem must equal the registry key byte-for-byte |
| V2 | same but renamed to the registry key `R30FxEntryCompleteSet.md` | **0** | clean PASS |
| V3 | six scout source re-reads `R30FxSrcS081..S086` cited | **0** | six `existing returned`, `second-seat-reports=6` |
| V4 | cite this seat's own report | **1** | `(seat role 'executor' is not an allowed read-only reviewer)` |
| V5 | V4 + registry role set to `reviewer` (sandbox only) | **0** | proves role string is the gate |
| V6 | V2's bytes present on disk, commit still old | **1** | inventory `0`; Q15 — a working-copy report buys nothing |
| V7 | cited report body says `VERDICT: FAIL` | **0** | verdict-blind: presence ≠ endorsement (as Q13 says) |
| V8 | reason cites `build/R30RevEntryQ1Q6.md` (role `reviewer` exists there) | **1** | cited but `build/` is silently dropped: `cited seat-report paths: '.ufo/…/build/R30RevEntryQ1Q6.md'` yet `no cited, existing, returned second-seat report` |
| V9 | candidate cell `contamination-transparency-card.md` (bare file name) | **1** | `admitted candidate is absent`; report then fails with `candidate has no committed writer: field` |
| V10 | candidate cell `knowledge/contamination-transparency-card.md` | **0** | `corpus/` prefix is tried automatically |
| S3D | projection with five of six cited reports | **1** | `(absent from commit tree)` — all-or-nothing |
| Q15 | cited reports on disk, graded at S3 | **1** | `second-seat-reports=3`, `git status` shows them `??` |
| lane tip `363a4eb` | real lesson path against the committed tip | **2** | `INPUT ERROR: cannot read corpus/lessons/round-30.md at 363a4eb: … exists on disk, but not in` |

## 6. The repaired landing, proven green (exit 0, sandbox commit)

Two-byte-class edits, nothing else: cite only verdict-bearing seats, each by full `falsify/` path.
With stand-ins for the four still-missing files (`R30FxEntryCompleteSet`, `R30FxEntryQ1Q3`,
`R30FxEntryQ4Q6`, `R30FxSrcS086`; labelled `SANDBOX STAND-IN` in their bodies) and the real
`R30FxSrcS081.md`, `R30FxQuotes.md`, `R30FxSrcS082.md`, `R30FxDeadSeats.md` committed alongside:

```console
$ cd /tmp/r30fx-q13fixture/final && python3 plans/gate_timing_check.py \
      --lesson corpus/lessons/round-30.md --commit HEAD
PASS line 17 Gate admit: candidate='corpus/knowledge/contamination-transparency-card.md'
  cited seat-report paths: 'falsify/R30FxEntryCompleteSet.md', 'falsify/R30FxEntryQ1Q3.md', 'falsify/R30FxEntryQ4Q6.md', 'falsify/R30FxSrcS081.md', 'falsify/R30FxSrcS086.md'
  existing returned second-seat report(s): .ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md, …/R30FxEntryQ1Q3.md, …/R30FxEntryQ4Q6.md, …/R30FxSrcS081.md, …/R30FxSrcS086.md
gate_timing_check: commit=HEAD lesson=corpus/lessons/round-30.md admissions=1 passed=1 failed=0 second-seat-reports=8
EXIT=0
```

And the same projection plus **this** report, which lands in the admitting commit:

```console
gate_timing_check: commit=HEAD lesson=corpus/lessons/round-30.md admissions=1 passed=1 failed=0 second-seat-reports=9
EXIT=0
```

So this seat's `executor`-role report is inert as long as it is not cited: it raises the inventory
and changes no verdict. Citing it is a red (§3). Re-run with **these** report bytes (not a stand-in)
copied into the same commit: `passed=1 failed=0 second-seat-reports=9`, `EXIT=0`, and the checker sees
in it an anchored `VERDICT:` line, the candidate path, and no `writer:`/`author:` declaration
(`REPORT_AUTHOR_RE` → `[]`).

Q14/Q15 mechanism, run from inside the snapshot copy (its own `--selftest`, not my mutants):

```console
$ python3 plans/gate_timing_check.py --selftest
[selftest] tree inventory matches requested commit (early=0, later=2; lesson unchanged)
[selftest] isolated sandbox Git leaves caller index untouched and hostile GIT_DIR/WORK_TREE/config/template/hooks do not escape
[selftest] production run_git ignores caller GIT_DIR/object directory; fresh bare victim and object sentinel unchanged
[selftest] ALL PASS (five allowed roles; connector/mutation-tester/simplifier and unknown roles rejected; declared writer/author/agentId conflicts red; worktree/parser/run_git mutants red; caller index and fresh bare victim unchanged)
EXIT=0
```

## 7. Checklist the real landing commit must satisfy

Structural (Q13/Q14/Q15, all machine-checked by the one command):

- [ ] `corpus/lessons/round-30.md` Gate: exactly one `admit` row; `candidate` cell =
      `corpus/knowledge/contamination-transparency-card.md`; citations inside the **`reason`** cell
      (not a 4th `read` column, not a 5th column).
- [ ] Drop `R30FxQuotes.md` from that reason cell (no verdict, by its own design). Cite only seats that
      emit `^VERDICT:` — currently `R30FxSrcS081`, `R30FxSrcS082` and whatever the two entry-review
      seats return.
- [ ] Every cited path is a **full** `.ufo/waves/round-30/falsify/<Seat>.md` path; written out, no
      `…` ellipsis swallowing a prefix, no bare names.
- [ ] Each cited file is committed in the **same** commit, mode `100644`, non-empty, contains
      `corpus/knowledge/contamination-transparency-card.md` (or the cell string) **and** a line starting
      `VERDICT: ` with a non-space character; no `writer:`/`author:` line naming `KengakuR30`.
- [ ] `.ufo/waves/round-30/falsify/swarm-registry.json` is in the same commit and maps each file's
      stem (byte-exact, case-sensitive) to role ∈ {reviewer, scout, critic, sentinel, revenger};
      no `agentId` equals `KengakuR30`.
- [ ] `git add` the whole `corpus/lessons/round-30.md`, `corpus/knowledge/contamination-transparency-card.md`
      and `.ufo/waves/round-30/` — the wave dir is untracked at `363a4eb`, so a `commit -a` leaves
      `second-seat-reports=0`.
- [ ] Re-run at the admitting sha and paste the exit code + the `… passed=N failed=0
      second-seat-reports=<N>` line; a run before the commit is exit **2**, not a green.
- [ ] No new `admit` row for anything without its own falsify report (one bad admit row reds the run).

Adjacent, not decided by this check: Q20 asks a gate-touching landing (`plans/*.py` changed this
round) for a run made in an archive-extracted tree of the landed sha with pinned count lines; this
check does not supply that.

## 8. Calibration notes and limits

- The checker is **structural**: it accepts a cited report whose verdict is `FAIL` (V7). Q13's
  "presence is not endorsement" is literal — the integrator still owns Q9/Q10 truth.
- `build/` reviews are silently worthless for Q13 even when a registered `reviewer` wrote them (V8):
  the path is printed as *cited* but never as *existing*. The round's 36 build reports cannot back the
  admit.
- Roles decide before content (V4/V5); stems decide before files (V1); candidate cells must resolve to
  a real committed file before `writer:` is even read (V9).
- My green runs are projections: four of the cited files were `SANDBOX STAND-IN` bytes written for this
  fixture, never production evidence, and the shas `c61e24d`/`5d79c82`/`201107a` are local to
  `/tmp/r30fx-q13fixture/`. The two real acceptances are `R30FxSrcS081.md`/`scout` and
  `R30FxSrcS082.md`/`scout`; the real rejection is `R30FxQuotes.md`/`scout`.
- The lane moved under me twice (Gate row rewritten, reports appearing). Everything above is pinned by
  the lesson/registry sha256 in §1; re-run the command yourself at the admitting sha before trusting
  any of it.
- Scratch: `/tmp/r30fx-q13fixture/{lane,lane2,s3,final,runs}/`, per-variant stdout in `runs/*.txt` and
  the branch set `v1-gate-name … repair` in each snapshot repo.
