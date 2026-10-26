# R39PkgEntry — C2 package draft (kengaku round 39, wave 1)

Seat: `R39PkgEntry` (scribe). Target: draft the C2 coverage package for the L1 — entry, SOURCES rows, README index
row + coverage bullet — and prove the draft against the frozen counter on a scratch clone. Lane repo read-only; all
writes went to `.ufo/waves/round-39/build/R39PkgEntry/` and to `/fast/scratch/hyaku/kengaku-r39/R39PkgEntry/`
(deleted). No lane file, fleet-root file, sibling lane, lane index or jj state was touched.

## 1. Deliverables (draft artifacts, for the L1 to integrate)

| Artifact | Bytes / lines | sha256 | Becomes |
|---|---|---|---|
| `.ufo/waves/round-39/build/R39PkgEntry/entry.md` | 29210 / 314 | `f70f3e598afcf76f2b2d30bde9de015726f26520e6b4f6ac93be644d306cbdf8` | `corpus/knowledge/tb2-git-leak-recovery-grader.md` |
| `.ufo/waves/round-39/build/R39PkgEntry/rows.md` | 2037 / 2 | `a9be1e4e92c57a854759c1e8e50ec9da82287f6359d4f59ec63b8d9d567a37db` | rows `S117`/`S118` in `corpus/SOURCES.md` |
| `.ufo/waves/round-39/build/R39PkgEntry/readme.md` | 2405 / 8 | `a121815587605b4801fb602b248c67b5ab5d144044ba762e450227469b17d79f` | one index row + one coverage bullet in `corpus/README.md` |
| `.ufo/waves/round-39/build/R39PkgEntry/c2-counter-output.txt` | 753 | — | verbatim counter output (saved receipt) |

`rows.md` carries the two rows only (the census-parsed table lines); `readme.md` carries the two README lines plus
a placement note. Nothing from `corpus/`, `plans/`, a lane mirror or a clone was copied into the build dir.

## 2. Proof — frozen counter, `checks=7 defects=0`

Scratch clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin
/fast/scratch/hyaku/kengaku-r39/R39PkgEntry/lane`; `git rev-parse --show-toplevel` printed exactly that path;
clone HEAD `750473847af9c7a461487ba3a589b5519fac5ed8`. Drafts placed at their final lane paths, then
`git -C "$S/lane" add -A` (index-only). `TMPDIR` and `--work` pointed into the scratch dir.

```
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round39_c2_verify.py --lane "$S/lane" --work "$S/w"
V1 ok listed=7 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=29 distinct_quotes=29 distinct_lines=29 out_of_word_range=0
    gate: P4 ok checked=29 bad=0 first=0
    gate: P5 ok manifest_entries=7 bad=0 first=0
    gate: P6 ok rows=2 bad=0 first=0
    gate: P7 ok source_lines=2 bad=0 first=0
    gate: P8 ok index_rows=46 knowledge_files=46 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=5867
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=25 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 tags=4 bad=0
checks=7 defects=0
PREDICATE C2 pass
EXIT=0
```

Three earlier runs printed the same `checks=7 defects=0` (the last two after content edits); the saved receipt is
the final one. The frozen do-nothing control in the claims file reads `checks=7 defects=4` (V2, V3, V4, V7), so the
draft moves every clause it can.

Independent instruments, all in the same clone:

```
$ python3 plans/git_leak_probe.py --lane .   # direct rerun, not through the gate
real 0m1.373s   EXIT=0   stderr 0 bytes
$ cmp probe-rerun.txt corpus/evidence/round39/git-leak-probe.txt  -> BYTE_EQUAL
cases=25 observed_pass=13 observed_fail=12 mismatches=0        # receipt is 5867 bytes
$ (cd corpus/evidence/round39/tb2-git-leak-recovery && sha256sum -c SHA256SUMS)
Dockerfile: OK  challenge-setup.sh: OK  instruction.md: OK  solve.sh: OK
task.toml: OK  test.sh: OK  test_outputs.py: OK                RECHECK_EXIT=0
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <clone>/corpus/SOURCES.md
... pre-existing W04 duplicate-url warnings (S040, S048, S057-S059, S064-S069, S071, S075, S076, S100) ...
file ok <clone>/corpus/SOURCES.md                              CENSUS_EXIT=0
$ git -C "$S/lane" status --short
M  corpus/README.md
M  corpus/SOURCES.md
A  corpus/knowledge/tb2-git-leak-recovery-grader.md
$ git -C "$S/lane" diff --cached --stat
3 files changed, 317 insertions(+)
```

The recheck line in the entry is the command above, written as
`(cd corpus/evidence/round39/tb2-git-leak-recovery && sha256sum -c SHA256SUMS)` from the lane root and green as
written (round-38 closure R4). `git status` shows the only changes are the three intended files: every frozen input
(gate, spec, probe, dry table, captures incl. `SHA256SUMS`, receipt, the C1 pins) was byte-identical in the clone,
which is also what `P1`/`P5`/`V1`/`V5` assert. No `git add`/`commit`/`checkout`/`reset`/`stash` and no jj command
ran in the lane; the clone was index-only and then deleted with its whole scratch root.

Limits of this proof, stated plainly: the predicate was measured on a **scratch clone of clone HEAD
`7504738`**, not on the landing tip after integration; the L1's landing run is the authority. `P9` was satisfied
with the drafts staged, as the fixture rule allows; the L1 must land them committed.

## 3. What the entry contains

Shape copied from `corpus/knowledge/tb2-build-pmars-grader.md`: two `source:` lines with the exact pinned raw URLs
(S117 `git-leak-recovery/tests/test_outputs.py`, S118 `git-leak-recovery/instruction.md`), `verified-at:
2026-10-26`, one `recheck:` line.

- **Summary** — the five pytest functions, the reward mapping, the graded state as *refs + object-store text + one
  flag file + a pinned non-dot work-tree checksum*, the receipt headline, the passing-vacuum cases and their
  failing counter-cases, and the class relation: a new executed edge class (repository history) relative to the
  four earlier TB2 entries; it narrows the README §Frontier TB2 clause for this task only (5 of 89 read).
- **Source labels** — S117/S118 primary for *what the grader checks*; `task.toml` metadata read only for the
  declared image, timeouts and internet policy; `solve.sh` tier C, read never run; captures of the setup read for
  the initial-state shape; receipt tier A for its own scope. The prediction-before-first-run disclosure is carried,
  including that the second receipt is byte-equal and that one prediction (`oracle-solve-sh`) came from the
  round-38 pilot.
- **What is graded (static reading)** — eight-row mechanism table with line ranges (entry point, reward, flag file,
  the two `log --all` searches, init message, dangling objects, work-tree checksum) and four structural
  consequences.
- **Located quotes** — 29 rows, 29 distinct quote texts, 29 distinct locations (25 `test_outputs.py` lines +
  instruction lines 1, 3, 4, 5, 7, 9), every quote 3–25 words and byte-verbatim at its line; the gate's `P4`
  checks all 29 (`checked=29 bad=0`). Backslash escapes are the file's bytes.
- **Requirement map** — exactly one row per frozen TAG, in the frozen four-cell format, with the tag's frozen
  `instruction.md` line and case ids cited in backticks that all violate the tag.
- **Findings 1–9**, each tied to receipt case ids (below).
- **What the probe does not show** — five named limits (image never pulled / host git, unprivileged setup,
  `test.sh` not executed, the oracle row is a pilot observation, the 25 cases are the whole surface).
- **Prior art** — a marked `PRIOR-ART-PLACEHOLDER` line: `.ufo/waves/round-39/build/R39ScoutPriorArt.md` did not
  exist when this draft was written (its build subdir appeared during the run but was still empty; no `.md`
  report). The L1 must replace that single line with the scout's rows, or with the sentence that it found none.
  The claim is stated at "first probed instance for TB2 `git-leak-recovery`" only.
- **Negative space** — the exclusions, plus an explicit falsifier keyed to digests, the fresh probe summary line,
  named case flips, and grader lines that would have to read what the entry says they do not.

## 4. Requirement map — labels derived, not chosen

Derivation run against the frozen receipt and dry table (same rule as `V7`): per tag, collect every case whose
`violates=` carries it, then `enforced` iff all `fail`, `unenforced` iff all `pass`, else `partly`.

```
recover-secret    -> enforced  (5 violating: empty-app, untouched, flag-extra-text, flag-is-directory, flag-in-repo-only)
secret-gone       -> partly    (16 violating: 8 fail, 8 pass)
files-untouched   -> enforced  (2 violating: empty-app, readme-edited)
messages-untouched-> partly    (3 violating: empty-app fail; message-rewritten, history-rebuilt pass)
```

22 of the 25 cases carry a tag; `oracle-solve-sh`, `clean-echo` and `flag-padded-crlf` carry none (checked with
`grep -c "^CASE .*violates= "` → 3). The entry states this and names the three.

## 5. Findings from the work (substantive)

1. **Do-nothing = 4/5.** `untouched` (`FPPPP`): only the flag test fails on the task's initial state;
   `empty-app` (`FFFFF`) is the negative control. The task's whole delta is one file's presence.
2. **One `echo` = 5/5 with the secret still in the repo.** `echo-only`, `echo-reflog-expire`, `echo-gc-only`
   (all `PPPPP`): `log --all` cannot see an unreferenced commit, and `cat-file -p` of a dangling commit prints
   tree/parent/author/message, never the blob under it, so the secret blob reachable from that commit is never
   read. `dangling-secret-blob` and `dangling-secret-commit` (`PPPFP`) show test 4 firing when the object itself
   carries the text.
3. **Ref kind decides visibility.** `branch-keeps-leak`, `commit-message-secret`, `notes-secret` (`PFPPP`) fail
   through `log --all` / `-S`; `blob-ref-keeps-secret`, `tag-message-secret`, `stash-secret` (`PPPPP`) pass — a blob
   ref, a tag message and a stash merge commit contribute no commit message or diff.
4. **Dot paths are outside both views.** `dotfile-in-worktree` and `config-secret` (`PPPPP`); the checksum's
   `-not -path '*/\.*'` and the absence of any config read. The strict side is `untracked-file-secret` and
   `readme-edited` (`PPPPF`) because the digest is pinned.
5. **Message preservation is one substring.** `message-rewritten` and `history-rebuilt` pass; test 3 only needs the
   init message to appear in `log --oneline --all`, and the setup writes it on both existing commits
   (`challenge-setup.sh:12`, `:22`).
6. **Flag channel is exact text.** `flag-padded-crlf` passes (`strip()`), `flag-extra-text` fails,
   `flag-is-directory` fails with `IsADirectoryError` (named in the receipt), `flag-in-repo-only` (`FPPPF`) fails
   twice (wrong path, changed checksum).
7. **The oracle's static-vs-pilot disagreement resolved on the host.** The frozen row expected `FPPPP` ("fsck honours
   reflogs → nothing dangling"); the round-38 pilot observed pass and the probe observed pass. Host reproduction of
   the `challenge-setup.sh` shape on git 2.56.0: `git fsck --lost-found` **does** report the reflog-only commit as
   `dangling commit 999424f0…` (identical with and without `--no-reflogs`), `cat-file -p` of it prints no file
   content, and `git show … | grep -o 'secret\[[^]]*\]'` prints the literal — which is the oracle's extraction path
   (`solve.sh:11-24`, read, not executed), so the observed pass is mechanically explained. The hash is the scratch
   reproduction's own (date-dependent); the entry says so.
8. **Contestable tags disclosed, not edited.** `empty-app → messages-untouched` is load-bearing (without it the tag
   derives `unenforced`, with it `partly`); `stash-secret → secret-gone` rests on the row's own "uncertain" note
   plus the observed pass; `dotfile-in-worktree → secret-gone` tags a work-tree dot file against the history clause
   because the instruction's wording is "anywhere in that repo". No label moves without them, and the frozen rule
   is applied as written.

## 6. Judgment calls and honest gaps

- **The placeholder line is the one deliberate gap.** Everything else in the entry is grounded in a capture line or
  a receipt case; prior art is the only section awaiting a peer's output. I did not invent scout rows or open
  external URLs (no `web_search` used this seat), so the entry claims a probed instance and nothing wider.
- **No mismatch case to name.** `mismatches=0`, so the V4 obligation (name every `match=NO` case) is vacuous; the
  entry still carries the pilot-derived prediction disclosure for `oracle-solve-sh`.
- **Host instruments.** git 2.56.0, host bash/coreutils and an unprivileged setup stand in for Ubuntu 24.04's apt
  git and the image's root build; the entry names all three and resolves none. The checksum's absolute-path binding
  (`find /app/repo …`) is why the probe must stage `/app/repo`; a path-shifted run would red test 5 for the wrong
  reason.
- **Quote supply.** 29 qualifying locations were available and used; the gate needs 8 distinct. Two candidate lines
  were dropped for word count (`"--all",` and `"--regexp-ignore-case",` are single tokens). Before the first gate
  run I checked every row with `sed -n '<n>p'` on the capture (29 rows, 0 mismatches, re-run after the final edit),
  and the gate's `P4` passed on each of the three counter runs. One early draft had inserted a space into the
  `find … -not -path '*/\.*'` quote; it was restored to the file's exact bytes before any run, and `P4` has been
  green since.

## 7. Axes (named, per Godspeed)

- **coverage** (the axis the round chose, capped at 7 by the open L0 question): one more TB2 grader admitted at
  source-code depth with an executed offline probe — 5 of 89 tasks read at `2fd12b88`, one new executed edge class
  (repository-history state). No score move is claimed.
- **depth**: the entry carries 29 located quotes, a derived map over all violating cases, nine findings each tied
  to case ids, and a mechanism resolved by host reproduction rather than asserted.
- **operability / freshness**: the recheck line is green as written and the probe reruns in ~1.4 s, so the entry is
  cheaply re-verifiable.
- No axis harmed: no frozen file edited, no claim widened, no lane file written.

## 8. L1 integration notes (exact)

1. Add `corpus/knowledge/tb2-git-leak-recovery-grader.md` = `entry.md` (29210 bytes) verbatim, after replacing the
   single `PRIOR-ART-PLACEHOLDER` line with the scout's rows or a "none found" sentence.
2. Insert the two rows of `rows.md` into `corpus/SOURCES.md` immediately after `S116` (registry table, before the
   `## Paths` section), unchanged.
3. Insert the index row of `readme.md` after the `knowledge/tb2-build-pmars-grader.md` row in `corpus/README.md`
   (line 71 at clone HEAD), and the coverage bullet after the round-38 TB2 bullet (line 263 at clone HEAD).
4. Nothing else: the PROVINCE paragraph and the §Frontier TB2 sub-bullet narrowing named in the claims are L1
   surfaces, and the entry's own wording for them is in its Summary.
5. Re-run `python3 plans/round39_c2_verify.py --lane .` on the landing clone; the expected line is
   `checks=7 defects=0` then `PREDICATE C2 pass`.

## 9. Tooling record

No install or upgrade was needed or made (no pacman, no `uv tool`, no binary fetch). Instruments used: the lane's
frozen scripts, system `git 2.56.0`, `python3`, `sha256sum`, `cmp`, and the fleet census validator. Scratch root
`/fast/scratch/hyaku/kengaku-r39/R39PkgEntry/` was removed before this report was written (`ls` of the parent shows
it gone; other seats' scratch dirs untouched).

VERDICT: c2-package-draft-checks-7-defects-0
