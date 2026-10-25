# R30FxC2Recheck — independent D1–D5 re-run, round 30 falsify wave

Seat: `L1Kengaku30.R30FxC2Recheck-3` (leaf, no dispatch). Lane: `kengaku-shokunin`.
Date of all runs: 2026-10-25. Substrate: **HEAD `363a4eb`** plus the round-30 worktree, which is
**dirty** (`M corpus/lessons/round-29.md`, `M corpus/SOURCES.md`, `M corpus/README.md`,
`M corpus/QUALITY.md`, `M plans/sources_adopt.py`, `M .ufo/waves/round-29/attempt2/adoption-expect.json`,
`M .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md`; untracked `corpus/evidence/round29-attempt2/control-nothing.txt`,
`corpus/knowledge/contamination-transparency-card.md`, `corpus/lessons/round-30.md`, `plans/round30_defects.py`,
`plans/round-30-claims.md`, `corpus/evidence/round30/`, `.ufo/waves/round-30/`). Every "HEAD" statement below
was taken with `git -C <lane> show HEAD:<path>` / `cat-file -p`, never from the worktree.
Tooling installed: **none** (no pacman transaction, no `uv`, no binary). All scratch work under
`/tmp/r30fx-c2recheck/` (archives of `8c14a5d` and `1f3b0f1`, a `prerepair` git repo holding HEAD bytes,
a `repaired` git repo holding worktree bytes). Lane writes: **this report only**; no dispatch, no background
jobs, `.ufo/state`/`watchdog.log`/`MANIFEST.json` untouched.

Axis: **calibration**. Item: re-run D1–D5 from `corpus/lessons/round-29-verifier-spotcheck.md` §5 and judge
whether each repair answers the routed sentence or a neighbouring one. This seat is not a source re-read and
not the complete-set review, so it carries no `VERDICT:` line.

---

## 0. Required command (pasted verbatim)

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok
exit=0
```

Byte-identical (modulo the trailing `exit=` line) to
`corpus/evidence/round29-attempt2/adoption-measured.txt` (HEAD) and to
`corpus/evidence/round30/r29-counter-unchanged.txt`; `cited_rows=5` holds, so C2's kill rule ("D5's repair
must leave round 29's frozen counter fields unchanged") is satisfied by measurement, not assertion.

---

## 1. Item-by-item

| item | command(s) run | output (essential) | repaired at HEAD? | answers the routed wording? |
|---|---|---|---|---|
| **D1** receipt at cited name | `git cat-file -p HEAD:corpus/evidence/round29-attempt2/control-nothing.txt`; `git status --porcelain -- <same>`; `sed -n '3p' <worktree file>`; `git show d4090261:<fleet>.ufo/reports/round-29/kengaku.md` lines 122–124 | `fatal: path 'corpus/evidence/round29-attempt2/control-nothing.txt' exists on disk, but not in 'HEAD'`; `?? corpus/evidence/round29-attempt2/control-nothing.txt`; worktree line 3 = `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped`, which **is** the report's quoted line | **NO** — untracked only | Yes on the *branch* (receipt under the cited name carrying the quoted line + the wave's eight-field variant + exit 1), but unlanded, so the defect stands at HEAD. Two fidelity caveats in §3. |
| **D2** kappa scope + count | `grep -rn kappa corpus/knowledge/*.md`; `git grep -li kappa 2ff4b6f -- \| wc -l`; `git grep -li kappa 363a4eb -- \| wc -l`; `git grep -li kappa -- \| wc -l`; `git grep -n kappa HEAD -- '.ufo/waves/round-29/*'` | scope command: **no output, exit 1** (0 hits); lane-wide: **65** at `2ff4b6f`, **66** at HEAD `363a4eb` (extra = `corpus/lessons/round-29-verifier-spotcheck.md`), **67** in the live worktree (extras = spotcheck **and `LOG.md`**, worktree lines 801/827). HEAD lesson still says `grep kappa` → 0 hits **in the lane**; worktree narrows it | **NO** — the narrowed sentence exists only as a worktree edit of `corpus/lessons/round-29.md` (`M`) | Yes for the routed half: it names the command's own scope (`corpus/knowledge/*.md`) and discloses the lane-wide figure instead of claiming it away — and the scan's command is confirmed at `HEAD:.ufo/waves/round-29/attempt2/build/R29a2RejectScan.md:102` (`grep -rn 'kappa' corpus/knowledge/*.md` → 0 hits). The *added* lane-wide clause is an adjacent disclosure that is already wrong (§3 F2). |
| **D3** S078 line-75 word count | `git show HEAD:corpus/lessons/round-29.md \| sed -n '194p'`; worktree same line; `git show HEAD:corpus/SOURCES.md \| sed -n '101p'`; `printf "%s" "The verifier never runs in the agent's sandbox." \| wc -w` | HEAD lesson: `— 9 words, line 75`; worktree lesson: `— 8 words, line 75`; SOURCES row anchor cell: `"The verifier never runs in the agent's sandbox." (8 words)`; `wc -w` = **8** | **NO** — HEAD still 9 | Yes, exactly: the cell now equals the row and the independently derived `wc -w`. No adjacent substitution. |
| **D4** uncommitted wave evidence | `git show HEAD:.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md \| wc -l` (692); `wc -l <` worktree (714); `git diff --numstat` (22/0); `grep -n 'Addendum'` both sides; `git status --porcelain --` that path | HEAD blob **omits** `### D. Addendum`; worktree line 694 carries `### D. Addendum — the 275/4/279 identity is exact (verified, not accepted)` (+22 lines, 0 deletions); status ` M .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md` | **NO** | Yes on the chosen branch ("commit it as wave evidence"): the bytes to commit are the routed 22-line addendum, unchanged. Unlanded. |
| **D5** S091 asymmetry | `git show HEAD:.ufo/waves/round-29/attempt2/adoption-expect.json`; worktree `json.load`; `git show HEAD:corpus/SOURCES.md \| grep -n S091`; `git show HEAD:corpus/knowledge/benchmark-task-validity-checklist.md \| grep -n 'S091\|ABC'`; the required counter command | HEAD expect: 4 keys, **no** `usedby_notes`; worktree adds `usedby_notes.S091` (≥10 words, names the entry, says the note is inert). Registry row S091 `used-by` = `corpus/lessons/round-29.md, corpus/knowledge/benchmark-task-validity-checklist.md`; entry `source:` lines = S077,S078,S079,S080,S090 only, while the entry quotes S091 at lines 25 and 103–111. Counter output unchanged, `cited_rows=5`, exit 0 | **NO** — the note is a worktree edit of a round-29 artifact | Yes, second branch verbatim ("record the asymmetry in `adoption-expect.json`"), and the chosen branch is the only one that keeps the frozen fields (measured on a scratch copy: injecting a `source: S091 …` line printed `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=skipped`, i.e. `cited_rows` 5 → 6; `plans/adoption_check.py:81,115`). |

Aggregate: `python3 plans/round30_defects.py --lane .` →

```
DEFECT D1 receipt-at-cited-path: receipt exists only in the worktree: corpus/evidence/round29-attempt2/control-nothing.txt is not committed at HEAD
ok D2 kappa-sweep-scope: repaired
ok D3 s078-line75-word-count: repaired
DEFECT D4 uncommitted-wave-evidence: HEAD:.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md omits the addendum ('### D. Addendum'); the wave evidence is not landed
ok D5 s091-usedby-asymmetry: repaired
defects=2
exit=1
```

---

## 2. Counter calibration (mutation matrix, all on `/tmp` copies)

The round-30 lesson claims the D-items "gained their own failure-capable assertions". I tested that.

| scratch repo | bytes | result |
|---|---|---|
| `prerepair` (HEAD blobs committed) | HEAD versions of lesson/SOURCES/entry/expect + addendum-less D4 file + no receipt | `defects=5`, exit 1 — **reproduces `claims/defects-before.txt`** (same five messages, D4 worded by blob instead of status because the scratch committed the file) |
| `repaired` (worktree blobs committed) | current worktree bytes + receipt + addendum | `defects=0`, exit 0 — **the 5→0 ladder is real and reachable; nothing but the commit blocks it** |
| M1 | kappa sentence re-rendered `… → 0 hits, so the sweep is clean across the whole lane` (scope string kept) | `defects=0` — **survives**: the D2 assertion is a literal `"in the lane"` test, not a scope test |
| M2 | `→ 0 hits` → `→ 1 hits` on the scoped line | `DEFECT D2 … states 1 hits, corpus/knowledge/*.md holds 0` — caught |
| M4 | `usedby_notes.S091` → `"ok"` | `DEFECT D5 … note is empty, too short…` — caught |
| M5 | receipt `# exit code of that run: 0` | `DEFECT D1 … carries no exit=1 line` — caught |
| M6 | receipt reduced to the two field lines + `exit=1`, provenance header deleted | `defects=0` — **survives**: D1 verifies three substrings, not that a run produced them |

---

## 3. Findings, most severe first

**F1 (HIGH — claim vs HEAD bytes). C2's frozen predicate is unmet at HEAD; D1 and D4 are open.**
`plans/round-30-claims.md` §C2 freezes "prints `defects=0` and exits 0 on the repaired tree"; HEAD gives
`defects=2`, exit 1, and `git cat-file -p HEAD:corpus/evidence/round29-attempt2/control-nothing.txt` is
exit 128 while HEAD's `R29a2CritEntry.md` is 692 lines without `### D. Addendum`. The round is honest about
*when* the zero is expected — `corpus/lessons/round-30.md` §Measured says "after the commit that lands D1's
receipt and D4's wave evidence", and `build/R30DefectState.md` (lines 74, 107, 143, 233–237) and
`build/R30CritC2.md` (line 33) already record "staged, uncommitted" / "gameable" — so this is an unlanded
claim, not a fabricated one. It still cannot be reported green: if falsify closes without that commit, C2
misses, and the §Measured line's parenthetical is the only thing standing between it and a false 0.

**F2 (MEDIUM — the D2 repair's own added number is already false, and nothing checks it).**
The worktree sentence reads "finds 65 files at the round-29 tip `2ff4b6f` and 66 at round 30 — the extra file
is `corpus/lessons/round-29-verifier-spotcheck.md` itself." 65 at `2ff4b6f` is right; 66 is right **only at
HEAD `363a4eb`**. The live worktree gives **67**, with two extras, because round 30's own `LOG.md` edit
(`M LOG.md`, lines 801 and 827) mentions kappa. The tree that will carry the sentence therefore contradicts
it. `check_d2` re-derives only the scoped `→ 0 hits` count (`plans/round30_defects.py:108-117`); M1 shows a
same-class false-scope rendering passes with `defects=0`. So the D2 row is repaired for the routed sentence
and defective in the honesty clause it added: the number should be pinned to a commit ("at `363a4eb`") or
dropped.

**F3 (MEDIUM — mixed substrate: three "repaired" verdicts rest on uncommitted bytes).**
`check_d1` (`plans/round30_defects.py:73`) and `check_d4` (`:150`) gate on `HEAD:` blobs via `head_blob`
(`:68`); `check_d2` (`:92`), `check_d3` (`:120`) and
`check_d5` read `lane/<path>` from the worktree. Consequence, measured above: `ok D2`, `ok D3`, `ok D5` are
emitted while none of those three repairs is committed — HEAD's lesson still prices the quote at 9 words and
says "0 hits in the lane", and HEAD's expect file has no `usedby_notes`. A reader who takes `defects=0` as
"the five repairs are landed" is wrong by three items; the module docstring's "committed/live lane bytes" is
the only disclosure. The round's own standard for D1/D4 (judge the committed blob) is not applied to
D2/D3/D5.

**F4 (LOW — the D1 receipt's provenance sentence is false as written).**
`corpus/evidence/round29-attempt2/control-nothing.txt` (worktree) says "Both forms were reproduced on
2026-10-25 from a scratch `git archive` of the round-29 baseline `1f3b0f1…`". That tree cannot produce either
form: `git log --diff-filter=A -- plans/adoption_check.py` → `8c14a5d`, and
`/tmp/r30fx-c2recheck/b1f/plans/adoption_check.py` does not exist after extracting `1f3b0f1`. What I could
reproduce:
- `8c14a5d` tree as-is → `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 verified_at=0 census=skipped`, exit 1 — **byte-identical to `.ufo/waves/round-29/attempt2/control.nothing.txt:3`**;
- `1f3b0f1` tree + `8c14a5d`'s counter+expect → the same eight-field line, exit 1;
- `1f3b0f1` tree + HEAD's counter+expect → `… usedby_ok=0 census=skipped`, exit 1, i.e. the report's seven-field line.
So the claim holds only under an unstated "tree content from `1f3b0f1`, tooling overlaid" reading. M6 shows
`check_d1` would accept a receipt with the header deleted, so this is unpoliced text inside the artifact the
defect is about.

**F5 (LOW — the D1 repair is a reconstruction, and its report pointer resolves outside the lane).**
No committed artifact ever existed at `corpus/evidence/round29-attempt2/control-nothing.txt`; the new file is
authored on 2026-10-25 from the two reproducible forms. Its header labels that, which is the honest handling
of "commit the receipt under the cited name" when only the wave file was ever captured — but a reader cannot
tell a captured receipt from this one by shape (M6). The header also points at
`.ufo/reports/round-29/kengaku.md`, which resolves in the **fleet** repo (`d4090261`), not in the lane
(`kengaku-shokunin/.ufo/reports/` holds only `round-17`); the lane-relative path in the receipt is dead.

**F6 (INFO — verifier wording carried forward uncorrected).** D1 says the report "cites
`corpus/evidence/round29-attempt2/control-nothing.txt` twice". The fleet report mentions it **once**
(`.ufo/reports/round-29/kengaku.md:124`, beside the wave path). `plans/round30_defects.py`'s docstring
already drops "twice"; the check does not depend on the count. Recorded so the count is not inherited as fact.

**F7 (INFO — verified exact, no action).** D3 is an exact repair (lesson cell 8 = SOURCES cell 8 =
`wc -w` 8) with no adjacent drift. D5's note records the asymmetry the registry asserts, the entry's quoted
S091 is real (entry lines 25, 103–111), and the round-29 counter's seven fields are unchanged
(`entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`, exit 0). D4's staged
bytes are the routed +22-line addendum and no other change (22/0 numstat).

---

## 4. Residual risk and verification gaps

- **Time-of-check drift.** Peers are editing the lane now; the lane-wide kappa count moved 66 → 67 between
  my third and sixth run (`M LOG.md` appeared). F2's number is a snapshot, and its *point* is that the
  sentence is not pinned to one.
- **`plans/round30_defects.py` has no history** (untracked), so the lesson's Mistakes entry about the first
  D2 repair's `re.sub(r"[*_`]", "", raw)` cannot be verified against bytes. I did not treat it as true or
  false; it is unverifiable until committed.
- Scratch repos use `git init` locals; census is path-dependent (round-29 residual F6), so I ran the required
  `--census` command only in place. The `repaired` scratch's `defects=0` is therefore a statement about the
  five predicates, not about census.
- I did not verify C1 (the C1 entry's own claims) or C3 (`sources_adopt.py` selftest); both are other seats'
  scope. My D1 quote check used the fleet report at `d4090261`, the only committed copy of it.
- **Action the lane still owes**, from the routed wording and measured here: commit D1's receipt, D4's
  addendum, and the D2/D3/D5 worktree edits in one landing; then `defects=0`/exit 0 is the *committed* state
  (it is reachable — the `repaired` scratch proves it) and C2's predicate is met rather than deferred.
