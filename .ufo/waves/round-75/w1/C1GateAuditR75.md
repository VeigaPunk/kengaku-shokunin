# C1GateAuditR75 — scoped adversarial review

Axes: coverage (enumerated surfaces and both parity directions), calibration (false greens versus declared exclusions). Recommendation only; no admission or claim judgment.

## Scope and provenance

Read `plans/round-75-claims.md` in full (128 lines), including A1, before commands. Reviewed the actual added-file diff with `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff 4c4249a2 43255758 -- plans/round75_c1_index_parity.py` (rc 0). Captured canonical A1 bytes with `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show 43255758:plans/round75_c1_index_parity.py` (rc 0), SHA256 `b1597c4edf46eb961d4430d487f86034018ab63b13d8b4b84c154e623146545f`. All 20 fixture commands below execute those same bytes, not a reimplemented census. Production changed during the audit (stdout duplicate-stamp adjustment observed in search), so findings and line numbers are explicitly A1-pinned. No production edits, git mutations, clone, installation, subagent, or alternate audit runtime.

`read xd://lsp` returned `No such tool: xd://lsp`; no server/status/references/definition/diagnostics route is available. Used literal grep fallback on frozen `gate.py` and on the lane gate/claims/README; grep is not semantic proof. Runtime fixture outputs supply the behavioral evidence.

## Findings, severity order

### HIGH — non-rendered README text can satisfy the index leg

Evidence: A1 `plans/round75_c1_index_parity.py:45,72,80-85,92-96`; canonical pass/return is `emit`, lines 104-121, with dispatch at 218. `ROW.match` visits every source line without Markdown fence/comment state. Remove the only genuine index row for `knowledge/a.md` and append these exact bytes:

````markdown
## Examples

```text
| `knowledge/a.md` | fixture | src |
```
````

`fenced-row`: rc 0, `UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0`, `PREDICATE R75-C1 pass`. Replacing the fenced example with `<!--\n| `knowledge/a.md` | fixture | src |\n-->\n` also passes (`html-comment-row`, rc 0), although no rendered index row exists. The rendered code example is not an index table; the comment is not rendered at all.

The target-size pair has exactly 74 knowledge files, 123 lessons, 66 evidence directories. Files are `knowledge/000.md` through `073.md`, `lessons/000.md` through `122.md`; evidence directories `d000` through `d065`. All have ordinary rows/mentions except knowledge/000.md. Without any extra text (`target-hidden-knowledge`), rc 1 and `MISSING knowledge/000.md`. Add only the fenced example above with `a.md` replaced by `000.md` (`target-fenced-knowledge`): rc 0 and **all three frozen target universe lines plus `PREDICATE R75-C1 pass`**. Thus YES: the missing=0 landing count/predicate lines can be false green with a genuinely absent rendered index entry. This does not reproduce a clean committed landing stamp: scratch fixtures deliberately have `LANE_TIP unknown`.

`fenced-evidence` similarly moves the only evidence mention into ` ```text\ncorpus/evidence/d1/\n``` ` and returns rc 0, evidence `dirs=1 indexed=1 missing=0 orphan=0`. Evidence's frozen rule is a *mention*, not necessarily a table row, so this arm documents permissiveness rather than independently redefining the frozen rule.

Recommendation: distinguish Markdown code/comments from actual index-bearing text without imposing a new section-location requirement on the existing repair rows.

### MEDIUM — a directory with .md suffix is counted as a knowledge file

Evidence: A1 `plans/round75_c1_index_parity.py:78,81-88` uses `base.glob('*.md')` without `is_file()`. In `directory-as-md`, replace the actual `corpus/knowledge/a.md` file with an empty directory of the same name, retaining its README row. Command returns rc 0, `UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0`, `PREDICATE R75-C1 pass`. The reverse leg claims a file exists, but only a directory exists. This differs from the frozen contract's knowledge **files** (claims lines 22-26,34). NO directly unindexed file is hidden by this exact fixture, but a nonexistent-file index row and inflated file count pass; a real knowledge file may be replaced by a directory without changing counts. Recommendation: type-check enumerated knowledge/lesson entries.

### INFO — exact-byte filename mismatches correctly fail (required attack a)

On disk `a.md`; README first cell respectively `| `knowledge/a.md ` |`, `| `knowledge/A.md` |`: each rc 1, `MISSING knowledge/a.md`; ORPHAN is respectively `knowledge/a.md ` (one trailing U+0020) and `knowledge/A.md`. Unicode arm: disk filename `caf\u00e9.md` (NFC), README `cafe\u0301.md` (NFD); rc 1, `MISSING knowledge/café.md` and `ORPHAN knowledge/café.md`. Each knowledge line is `files=1 indexed=0 missing=1 orphan=1`. Literal set membership at A1 lines 80-85 does not strip, casefold, or normalize. NO false green.

### INFO — nested knowledge file is excluded as declared (required attack b)

`nested-file` adds `corpus/knowledge/sub/x.md`, without a README row. rc 0, knowledge `files=1 indexed=1 missing=0 orphan=0`. The nested file is invisible, but the frozen universe explicitly says `corpus/knowledge/*.md`, not `**/*.md` (claims 22-23; gate 19-22,47-49,78). NO violation of the declared universe; do not expand it post-freeze. The base fixture's counted top-level file remains indexed.

### INFO — evidence types and symlinks behave consistently (required attack c)

Evidence: A1 lines 91,94 call `Path.is_dir()`, which follows symlinks.

- `evidence-file`: replace d1 directory with a regular file while retaining `corpus/evidence/d1/` mention: rc 1, `dirs=0 indexed=0 missing=0 orphan=1`, `ORPHAN-EVIDENCE d1`.
- `evidence-file-link`, `evidence-broken-link`: d1 symlink to a regular file or missing target, same rc 1/output.
- `evidence-dir-link`: d1 symlink to the fixture's real external directory: rc 0, `dirs=1 indexed=1 missing=0 orphan=0`. This is a resolving directory path, not an arbitrary file. The freeze does not forbid resolving symlink directories or require physical containment.
- `missing-dir-link`: retain normal d1 and add unmentioned `link` symlink to a real directory: rc 1, `dirs=2 indexed=1 missing=1 orphan=0`, `MISSING-EVIDENCE link`. A resolving symlink directory cannot hide from `dirs=` through symlink status alone.

NO demonstrated genuinely unindexed declared evidence directory with missing=0 from these type attacks. External target contents/provenance are not covered by this gate's index-parity contract.

### INFO — tables in other sections are accepted (required attack d)

`other-section-table` removes the original knowledge row and appends exactly `## Unrelated historical examples\n\n| Example | Meaning |\n| --- | --- |\n| `knowledge/a.md` | fixture | src |\n`. rc 0, knowledge `files=1 indexed=1 missing=0 orphan=0`. The regex is section-agnostic. The freeze does not prescribe section boundaries; the actual repair also adds supplemental index tables (README search lines 868-875). A rendered index-capable row elsewhere is not independently a proved false green. Distinguish this from the non-table fenced/commented source in HIGH above. No spurious MISSING fires.

### INFO — reverse legs reject actual absent targets (required attack e)

Add `| `knowledge/ghost.md` | fixture | src |`: `orphan-row`, rc 1, `ORPHAN knowledge/ghost.md`, knowledge `files=1 indexed=1 missing=0 orphan=1`. Lesson counterpart: `orphan-lesson`, rc 1, `ORPHAN lessons/ghost.md`. Add `- `corpus/evidence/ghost/` fixture`: `orphan-evidence`, rc 1, `ORPHAN-EVIDENCE ghost`, evidence `dirs=1 indexed=1 missing=0 orphan=1`. All print `PREDICATE R75-C1 fail`; missing=0 alone is not mistaken for an overall pass.

## Fixture method and command receipts

All fixtures were created only under `/fast/scratch/hyaku/kengaku-r75/C1GateAuditR75/`. No repository clone was needed or created. Baseline exact README bytes (UTF-8, newline terminated):

```text
| `knowledge/a.md` | fixture | src |
| `lessons/round-1.md` | fixture | ptr |
- `corpus/evidence/d1/` fixture
```

Baseline filesystem: regular files `corpus/knowledge/a.md` (`# a\n`) and `corpus/lessons/round-1.md` (`# lesson\n`), directory `corpus/evidence/d1/`. Each case applies only the changes described above. The target-size fixtures use the enumerated names above, `# fixture\n` file content, same row format and one `- `corpus/evidence/<name>/` fixture` mention per evidence directory.

For every case the actual command was `python3 /fast/scratch/hyaku/kengaku-r75/C1GateAuditR75/gate.py --lane /fast/scratch/hyaku/kengaku-r75/C1GateAuditR75/<case>`, with subprocess cwd equal to the seat scratch root. Captured stdout and exit codes follow; stderr was empty for every case. These are actual CLI exits, not inferred return values.

### Receipt: clean (rc 0)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=0
PREDICATE R75-C1 pass
```

### Receipt: trailing-space (rc 1)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=0 missing=1 orphan=1
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=0
MISSING knowledge/a.md
ORPHAN knowledge/a.md 
PREDICATE R75-C1 fail
```

### Receipt: different-case (rc 1)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=0 missing=1 orphan=1
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=0
MISSING knowledge/a.md
ORPHAN knowledge/A.md
PREDICATE R75-C1 fail
```

### Receipt: unicode-normalized (rc 1)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=0 missing=1 orphan=1
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=0
MISSING knowledge/café.md
ORPHAN knowledge/café.md
PREDICATE R75-C1 fail
```

### Receipt: nested-file (rc 0)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=0
PREDICATE R75-C1 pass
```

### Receipt: evidence-file (rc 1)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=0 indexed=0 missing=0 orphan=1
ORPHAN-EVIDENCE d1
PREDICATE R75-C1 fail
```

### Receipt: evidence-dir-link (rc 0)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=0
PREDICATE R75-C1 pass
```

### Receipt: evidence-file-link (rc 1)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=0 indexed=0 missing=0 orphan=1
ORPHAN-EVIDENCE d1
PREDICATE R75-C1 fail
```

### Receipt: evidence-broken-link (rc 1)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=0 indexed=0 missing=0 orphan=1
ORPHAN-EVIDENCE d1
PREDICATE R75-C1 fail
```

### Receipt: fenced-row (rc 0)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=0
PREDICATE R75-C1 pass
```

### Receipt: other-section-table (rc 0)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=0
PREDICATE R75-C1 pass
```

### Receipt: fenced-evidence (rc 0)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=0
PREDICATE R75-C1 pass
```

### Receipt: orphan-row (rc 1)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=1
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=0
ORPHAN knowledge/ghost.md
PREDICATE R75-C1 fail
```

### Receipt: orphan-evidence (rc 1)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=1
ORPHAN-EVIDENCE ghost
PREDICATE R75-C1 fail
```

### Receipt: directory-as-md (rc 0)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=0
PREDICATE R75-C1 pass
```

### Receipt: html-comment-row (rc 0)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=0
PREDICATE R75-C1 pass
```

### Receipt: target-fenced-knowledge (rc 0)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=74 indexed=74 missing=0 orphan=0
UNIVERSE lessons files=123 indexed=123 missing=0 orphan=0
UNIVERSE evidence dirs=66 indexed=66 missing=0 orphan=0
PREDICATE R75-C1 pass
```

### Receipt: target-hidden-knowledge (rc 1)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=74 indexed=73 missing=1 orphan=0
UNIVERSE lessons files=123 indexed=123 missing=0 orphan=0
UNIVERSE evidence dirs=66 indexed=66 missing=0 orphan=0
MISSING knowledge/000.md
PREDICATE R75-C1 fail
```

### Receipt: missing-dir-link (rc 1)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=0
UNIVERSE evidence dirs=2 indexed=1 missing=1 orphan=0
MISSING-EVIDENCE link
PREDICATE R75-C1 fail
```

### Receipt: orphan-lesson (rc 1)

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=1 indexed=1 missing=0 orphan=0
UNIVERSE lessons files=1 indexed=1 missing=0 orphan=1
UNIVERSE evidence dirs=1 indexed=1 missing=0 orphan=0
ORPHAN lessons/ghost.md
PREDICATE R75-C1 fail
```

## Residual risk and verification gaps

- Twenty real-disk CLI fixture arms were run; no landing-tree full predicate, clean-commit stamp, selftest, or C2 audit was run by this seat. Small fixtures exercise census semantics; the target-size fenced arm reproduces the exact target count lines, not committed-tree provenance.
- Review is pinned to A1 bytes. Later landing edits require owner verification; this report does not claim they are reviewed or repaired.
- No resume, rerouting, saturation, or second runtime exists in this C1 script; those generic review axes are not an observed property of this gate.
- No semantic LSP proof is available because the device is not mounted.
- Scratch root removed before handoff (cleanup result recorded below). Production files intentionally unchanged; deliverable is this report only.

## Self-evaluation

Accuracy 4/5: actual CLI receipts and A1 hash; no LSP semantic evidence. Completeness 4/5: all five requested attack families plus target-sized pair, but no landing replay. Clarity 4/5: findings separate frozen exclusions from false greens; raw receipts add length. Actionability 4/5: line-level causes and fixture bytes supplied, owner still must implement/verify. Conciseness 4/5: retained 20 receipts to preserve exact evidence. Overall 4.0/5. Improvement priority: owner replays the high finding against the final landing bytes after any repair; do not treat the scratch stamp as a landing measurement. Would the user agree: likely, because explicit gaps prevent overclaiming.

Cleanup: `shutil.rmtree(Path("/fast/scratch/hyaku/kengaku-r75/C1GateAuditR75"))` completed without exception; `not scratch.exists()` → `True`. No scratch tree remains.
