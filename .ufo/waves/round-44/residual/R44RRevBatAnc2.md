# R44RRevBatAnc2 — residual review: battery44 U7/U9 anchor modules (kengaku round 44, 2026-10-26)

Scope: `plans/battery44/u7_twin_a.py`, `u7_twin_b.py` (mutant U7, twin captures) and `u9_worktree_a.py`,
`u9_worktree_b.py` (mutant U9, working-tree lessons), fixture by fixture, against
`plans/anchor_digest_check.py:94-101` (Round-39 twin-capture paragraph) and `:105-108` (errata read from
the working tree), at landing commit `2a263e5a56ef6d48d06805e1ccd106de5de9ba66` (clean shared clone,
toplevel verified). Axes: honest demonstration, realistic shape, honest `defects`/`expect`, not a
re-spelling of the witness `claims/witness/w_u.py`.

## Findings by severity

**Calibration defects: none.** Every check below came back green; nothing in the four modules is dishonest,
decorative, or a witness re-spelling.

**Minor (cosmetic, no effect on kills or declarations) — u7_twin_a row-count miscount.** The module
docstring, the fixture docstring, and the commit message all say "five-row registry" for
`u7_twin_a-rowpath-registry`, but the registry has four rows (`S500`–`S503`,
`plans/battery44/u7_twin_a.py:56-61`). A reader auditing fixture size from prose alone is misled by one row.
Suggest the L1 note it; nothing frozen changes.

**Observation (counter, not modules) — first-killer reporting understates coverage.** The counter prints one
killer per mutant (`killed by=u7_twin_a-rowpath-registry`, `killed by=u9_worktree_a-registry-wrong-capture`),
but my per-fixture re-run shows **all 6 U7 fixtures and all 5 U9 fixtures kill individually** (table below), so
the landed margin is larger than the MUTANT lines suggest.

**Honesty note on my own harness (no fixture defect).** My first per-fixture driver passed `--lane <fixture
root>` instead of each build's returned argv and produced `USAGE: no corpus/SOURCES.md under …` (rc 2) on the
8 fixtures whose repo is a subdirectory. That was a driver bug, corrected to use the build's argv tail; it is
recorded here because it initially looked like a fixture defect. It is not.

## Evidence

### 1. Counter `--only U7,U9` (envelope, exit 0)

Command: `claims/envelope.sh "$S/env" python3 plans/round44_c1_verify.py --lane "$S/lane" --only U7,U9 --work "$S/w"`.

```
ENVELOPE start 20:51:40 cwd=/fast/scratch/hyaku/kengaku-r44/R44RRevBatAnc2
FIXTURE u7_twin_a-rowpath-registry tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u7_twin_a-provenance-table tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u7_twin_a-url-two-tasks tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u7_twin_b-url-trio-identical tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u7_twin_b-prov-twin tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u7_twin_b-mixed-trio tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u9_worktree_a-registry-wrong-capture tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u9_worktree_a-history-abbrev tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u9_worktree_b-registry-erratum-appended tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u9_worktree_b-erratum-retargeted-history tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u9_worktree_b-erratum-completed-in-place tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT U7 anchor rc-mirror killed by=u7_twin_a-rowpath-registry attributed=L539 value=differs hits=6 -- plans/anchor_digest_check.py:98-99 'A token that resolves to several of the row's captures
MUTANT U9 anchor rc-mirror killed by=u9_worktree_a-registry-wrong-capture attributed=L384 value=differs hits=5 -- plans/anchor_digest_check.py:106-107 'lessons are read from the working tree for paths com
BATTERY fixtures=33 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=2/2 order=0/0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 20:51:43 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Full-battery context at the same commit: `MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0
unattributed=0`, `MUTANTS-BY-TOOL anchor=4/4 order=1/1`, `PREDICATE C1 pass`, envelope exit 0
(receipt `R44RRevBatAnc2/counter-full.txt`) — reproduces the L1's admission.

### 2. Per-fixture direction check (every fixture individually, not just the first killer)

Driver: build each fixture from nothing with a contract-shaped `ctx` (git identity pinned, toplevel
asserted), then run the unmodified tool and the exact frozen `old -> new` mutant copy (unique-match asserted)
on the build's argv, inside the envelope. Receipt: `R44RRevBatAnc2/per-fixture.txt`.

```
u7_twin_a-rowpath-registry        | ref 0 - | mut 1 ['capture-unanchored']    | YES YES
u7_twin_a-provenance-table        | ref 0 - | mut 1 ['capture-unanchored']    | YES YES
u7_twin_a-url-two-tasks           | ref 0 - | mut 1 ['capture-unanchored']    | YES YES
u7_twin_b-url-trio-identical      | ref 0 - | mut 1 ['capture-unanchored']    | YES YES
u7_twin_b-prov-twin               | ref 0 - | mut 1 ['capture-unanchored']    | YES YES
u7_twin_b-mixed-trio              | ref 0 - | mut 1 ['capture-unanchored']    | YES YES
u9_worktree_a-registry-wrong-capture | ref 0 - | mut 1 ['digest-wrong-capture'] | YES YES
u9_worktree_a-history-abbrev         | ref 0 - | mut 1 ['abbrev-unresolved']    | YES YES
u9_worktree_b-registry-erratum-appended | ref 0 - | mut 1 ['digest-unknown']    | YES YES
u9_worktree_b-erratum-retargeted-history | ref 0 - | mut 1 ['digest-unknown']    | YES YES
u9_worktree_b-erratum-completed-in-place | ref 0 - | mut 1 ['digest-unknown', 'erratum-incomplete'] | YES YES
```

Mechanism cross-check against the tool source: U7's span is the non-abbrev twin claim
(`claimed.update(hit)` after the sorted resolution, `anchor_digest_check.py:543-544`); `claimed` is reset
per row (`:486`), so the sibling row S500 in `rowpath-registry` cannot mask the kill; the unanchored check
needs `len(per) > 1` and `not ex` (`:551`), which only the twin rows meet. U9's span is
`:384` `text = f.read_text(...)` in `load_errata` (`:374`), fed by `tree_paths` = `git ls-tree HEAD`
(`:182-184`), i.e. committed paths read from the working tree — every U9 fixture commits its lesson first
and edits only the working tree, so HEAD really lacks the exemption. `u9_worktree_a-history-abbrev`
additionally flips the abbreviation's first hex digit (`a[0]` → `0`/`1`), so the 8-hex prefix resolves in
neither variant and the kill is the erratum alone; its committed S302 erratum stays green in both variants —
exactly the isolation the module docstring promises.

### 3. Honest `defects`/`expect`

All 11 fixtures declare `expect=accept, defects=[]`; the counter observed `observed_rc=0 observed=-` for all
11 and `wrong=0` over all 33. The mutant defect classes the module docstrings advertise are exactly the
classes observed: "digest-wrong-capture under U9" (u9_worktree_a), "abbrev-unresolved under U9"
(u9_worktree_a), "stale 64-hex anchor token" (u9_worktree_b; observed `digest-unknown`), and
`erratum-completed-in-place` additionally surfaces the tool's own `erratum-incomplete` class. Line citations
in the docstrings check out: `:98-99` twin sentence, `:106-107` working-tree sentence, `:384` the replaced
read.

### 4. Realistic shape

The registries reuse the lane's real 11-column SOURCES table (`| id | source | kind | tier | scope | anchor |
teaches | status | opened | recheck | used-by |`, anchor cell index 5, 11 cells — matches `NCELLS`/`ANCHOR_CELL`
at `anchor_digest_check.py:161-162` and the live `corpus/SOURCES.md`); u7_twin_b pins the same commit
(`2fd12b88…`) and task.toml/task-directory shapes the lane's real S079/S146 rows describe; evidence dirs,
`task.toml` slugs, `SHA256SUMS` manifests, `PROVENANCE.md` tables and `corpus/lessons/*.md` errata all have
real counterparts in the tool's documented binding routes (`anchor_digest_check.py:50-56`, `:262-270`).
Commits grow plausibly (captures → registry → mirror), and no fixture reaches outside its build directory.

### 5. Not a re-spelling of the witness

Witness (`w_u.py`, 100 lines): one U7 fixture (single row `S901`, row-path binding, one commit, two caps) and
one U9 fixture (fake `"e"*64` token, one lesson committed then dirtied). The four modules differ materially:

- 6 U7 fixtures over three binding routes the witness never touches: two-commit multi-row registry, provenance
  table grown one line per commit, pinned raw/blob URLs resolved via task.toml slugs — plus a three-capture
  trio and a twin+solo two-token row (exercises the multi-token branch of the same span).
- 5 U9 fixtures: real sibling-capture digest instead of a fake token; abbreviation with a deliberately
  non-resolving prefix plus a committed control erratum; retargeted erratum (HEAD text exempts a different
  row); completed-in-place erratum (HEAD text lacks the correction token); multi-row registry with manifest.
No module references the witness (grep for `witness|w_u` over the four files: no matches), imports only
`hashlib`, and the counter's `sidechannel=0` agrees with my own token scan (case-insensitive, exit 1/no
matches).

## Residual risk and verification gaps

- Kills are rc+class differences I re-ran; span-execution and site-record attribution remain the counter's
  legs f/g (`value=differs`, `hits=6`/`hits=5`) — I did not independently re-derive the site records.
- I did not audit `u5_*`, `u6_*`, `u14c_*` modules (other seats' slices) beyond what the shared BATTERY lines
  show, nor git-version sensitivity beyond this host's git.
- The counter remains a heuristic (`sidechannel` token scan; R1 pins four git keys); my non-author check of
  intent is the re-spelling comparison above, which is judgement, not proof.
- Scratch-temp directory churn under `/fast` showed no instability in 5 repeated runs (one counter + four
  driver runs); a single flaky failure was my harness bug, documented above.

Receipts (all < 6 KiB): `counter-only-U7-U9.txt`, `counter-full.txt`, `per-fixture.txt` under
`.ufo/waves/round-44/residual/R44RRevBatAnc2/`.

VERDICT: anchor-modules-2-honest-4/4
