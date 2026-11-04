# C1GateReplayR75 — independent replay

Axes: coverage and calibration. Read the frozen claims and A1 in full before any command. Production files unchanged; only this report persists. No installations, commits, pushes, or git/jj mutations were performed. No subagent dispatched. No LSP endpoint/tool was available in this seat; symbol work used the instrument's text, not an empty LSP response.

## Pinned setup and stamps

`git clone --shared --revision=43255758 ...` returned 128 (abbreviated revision not accepted by clone). `git rev-parse 43255758^{commit}` returned 0 and `43255758ed7d74ea05c8e03686dd9ad37837f0cd`. Cloning with that full revision returned 0. `git rev-parse HEAD` in the scratch clone returned 0 and the same full hash. This is a detached, clean A1 clone, not the landing tree.

The exact requested commands default to `--rev master`; that ref is absent in this detached `--revision` clone. Their first lines were `LANE_TIP unknown` and `WORKTREE clean`. Thus the requested 40-hex first-line condition does **not** reproduce with these exact commands/clone shape. Explicit `--rev HEAD` resolves the measured commit and prints `LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd` / `WORKTREE clean`. This is a clone-ref dependency, not evidence of a dirty tree.

The verdict path prints the stamp pair twice (main lines 209–211 and emit line 116), unlike the retained verdict receipt's single pair. Selftest/control each print it once. All line citations below were independently grepped in the pinned script or current receipt bytes.

## Reproduction and byte comparisons

Exact default verdict rc=1, selftest rc=0, control rc=0. Explicit HEAD verdict rc=1, selftest rc=0, control rc=0. A1 is the frozen **before** state: 3 knowledge + 36 lessons + 20 evidence missing = 59; it is not expected to reproduce the repaired landing target.

Compared live explicit-HEAD stdout with the current `c1-before.txt`, `c1-selftest.txt`, and `c1-control-rowshuffle.txt` using `cmp -s - RECEIPT` (stdin=stdout): verdict comparison rc=1; selftest rc=0; control rc=0. Removing only the verdict's duplicate first stamp pair makes that comparison rc=0. Therefore full verdict stdout is **not byte-identical**; both other modes **are byte-identical** with explicit HEAD. The receipts were comparison inputs only, never substitutes for running the instrument.

The control printed exactly four defects: `MISSING knowledge/b.md`, `MISSING lessons/round-1.md`, `MISSING lessons/round-2.md`, `MISSING-EVIDENCE d2`, alongside `NAIVE rows=6 surfaces=6 equal=True`; control rc=0. It discriminates against row counting on the measured bytes. The implementation's control success condition (line 193) checks only nonempty defects and equal counts, not exactly four, so the exact observed four matters.

## Missing-arm attack

Copied the pinned instrument to untracked scratch `plans/c1_replay_attack.py`. Added exactly this sixth case at the battery's tuple, leaving census unchanged:

```python
("fenced-knowledge", {"drop_row": "knowledge/b.md", "orphan_row": "```\n| `knowledge/b.md` | fixture | src |\n```"}, 1, "MISSING knowledge/b.md"),
```

`python3 plans/c1_replay_attack.py --selftest --rev HEAD --work <scratch>/attack` returned 1: the five original cases pass, but `SELFTEST FAIL fenced-knowledge rc=0 want=1`; summary `SELFTEST cases=6 red=5 failures=1 ok=False`.

A separate scratch fixture driver using the **unmodified** instrument's `build_fixture`, `census`, and `emit` returned 0 and produced the retained output below. It built and changed real on-disk fixture bytes, not mocked return values. Missing arms and measured outcomes:

| Missing arm | Observed outcome | False green? |
|---|---|---|
| Knowledge row only inside fenced code | census rc=0; emit rc=0 and `PREDICATE R75-C1 pass` | Yes against rendered-table index semantics; parser line 45 matches row-shaped code. If frozen "row form" is intentionally lexical regardless of Markdown context, this is a semantic boundary, not proof of violating that narrower predicate. |
| Trailing space inside knowledge path | census rc=1; MISSING b.md + ORPHAN b.md-space | No, correctly rejected. |
| Additional case-different knowledge row B.md | census rc=1; ORPHAN B.md | No, correctly rejected on this filesystem. |
| Orphan lesson row | census rc=1; ORPHAN lessons/ghost.md | No, correctly rejected. |
| Orphan evidence mention | census rc=1; ORPHAN-EVIDENCE ghost | No, correctly rejected. |
| Replace knowledge/b.md regular file with directory named b.md, keep row | census rc=0, files=2 indexed=2 | Yes against the declared **files** universe: only one regular knowledge file remains, but line 78 uses glob without is_file. This is a type-check omission, not a claim that normal corpus directories currently exploit it. |

Neither extra orphan direction nor the whitespace/case/type/Markdown-context cases appear in the original five-case battery (grepped/read script lines 153–159). No production battery/predicate/target/control/kill rule was changed. Neither false-green fixture demonstrates that the unmodified 74/123/66 landing corpus currently contains that attack; they demonstrate acceptance on crafted real bytes.

## Exact retained replay evidence

### Exact default commands

`python3 plans/round75_c1_index_parity.py --lane .` — rc=1

```text
LANE_TIP unknown
WORKTREE clean
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=74 indexed=71 missing=3 orphan=0
UNIVERSE lessons files=123 indexed=87 missing=36 orphan=0
UNIVERSE evidence dirs=66 indexed=46 missing=20 orphan=0
MISSING knowledge/instrument-registry-derivation.md
MISSING knowledge/registry-argv-and-flag-audit.md
MISSING knowledge/tb2-torch-tensor-parallel-offline.md
MISSING lessons/round-44-verifier-spotcheck.md
MISSING lessons/round-46-verifier-spotcheck.md
MISSING lessons/round-47-verifier-spotcheck.md
MISSING lessons/round-48-verifier-spotcheck.md
MISSING lessons/round-49.md
MISSING lessons/round-50-verifier-spotcheck.md
MISSING lessons/round-50.md
MISSING lessons/round-51-verifier-spotcheck.md
MISSING lessons/round-52-verifier-spotcheck.md
MISSING lessons/round-53-verifier-spotcheck.md
MISSING lessons/round-54-verifier-spotcheck.md
MISSING lessons/round-55-verifier-spotcheck.md
MISSING lessons/round-56-verifier-spotcheck.md
MISSING lessons/round-57-verifier-spotcheck.md
MISSING lessons/round-58-verifier-spotcheck.md
MISSING lessons/round-59-verifier-spotcheck.md
MISSING lessons/round-60-verifier-spotcheck.md
MISSING lessons/round-61-verifier-spotcheck.md
MISSING lessons/round-62-verifier-spotcheck.md
MISSING lessons/round-63-verifier-spotcheck.md
MISSING lessons/round-64-verifier-spotcheck.md
MISSING lessons/round-65-verifier-spotcheck.md
MISSING lessons/round-66-verifier-spotcheck.md
MISSING lessons/round-66.md
MISSING lessons/round-67-verifier-spotcheck.md
MISSING lessons/round-67.md
MISSING lessons/round-68-verifier-spotcheck.md
MISSING lessons/round-69-verifier-spotcheck.md
MISSING lessons/round-70-verifier-spotcheck.md
MISSING lessons/round-71-verifier-spotcheck.md
MISSING lessons/round-72-verifier-spotcheck.md
MISSING lessons/round-73-verifier-spotcheck.md
MISSING lessons/round-73.md
MISSING lessons/round-74-verifier-spotcheck.md
MISSING lessons/round-74.md
MISSING lessons/round-75.md
MISSING-EVIDENCE round10-fleet
MISSING-EVIDENCE round11-fleet
MISSING-EVIDENCE round12-fleet
MISSING-EVIDENCE round13-coverage
MISSING-EVIDENCE round24-census
MISSING-EVIDENCE round24-sources
MISSING-EVIDENCE round25-calibration
MISSING-EVIDENCE round25-sources
MISSING-EVIDENCE round26-calibration
MISSING-EVIDENCE round26-sources
MISSING-EVIDENCE round27-calibration
MISSING-EVIDENCE round27-sources
MISSING-EVIDENCE round28-calibration
MISSING-EVIDENCE round29-attempt2
MISSING-EVIDENCE round29-calibration
MISSING-EVIDENCE round34
MISSING-EVIDENCE round53
MISSING-EVIDENCE round54
MISSING-EVIDENCE round60
MISSING-EVIDENCE round75
PREDICATE R75-C1 fail
```

`python3 plans/round75_c1_index_parity.py --selftest --work /fast/scratch/hyaku/kengaku-r75/C1GateReplayR75/selftest` — rc=0

```text
LANE_TIP unknown
WORKTREE clean
SELFTEST ok clean rc=0 want=0
SELFTEST ok missing-knowledge rc=1 want=1
SELFTEST ok missing-lesson rc=1 want=1
SELFTEST ok missing-evidence rc=1 want=1
SELFTEST ok orphan-knowledge rc=1 want=1
SELFTEST cases=5 red=4 failures=0 ok=True
```

`python3 plans/round75_c1_index_parity.py --control-rowshuffle --work /fast/scratch/hyaku/kengaku-r75/C1GateReplayR75/control` — rc=0

```text
LANE_TIP unknown
WORKTREE clean
NAIVE rows=6 surfaces=6 equal=True
UNIVERSE knowledge files=2 indexed=1 missing=1 orphan=0
UNIVERSE lessons files=2 indexed=0 missing=2 orphan=0
UNIVERSE evidence dirs=2 indexed=1 missing=1 orphan=0
MISSING knowledge/b.md
MISSING lessons/round-1.md
MISSING lessons/round-2.md
MISSING-EVIDENCE d2
PREDICATE R75-C1-control pass
```

`git rev-parse HEAD` — rc=0

```text
43255758ed7d74ea05c8e03686dd9ad37837f0cd
```

### Explicit HEAD commands

`python3 plans/round75_c1_index_parity.py --lane . --rev HEAD` — rc=1

```text
LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd
WORKTREE clean
LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd
WORKTREE clean
UNIVERSE knowledge files=74 indexed=71 missing=3 orphan=0
UNIVERSE lessons files=123 indexed=87 missing=36 orphan=0
UNIVERSE evidence dirs=66 indexed=46 missing=20 orphan=0
MISSING knowledge/instrument-registry-derivation.md
MISSING knowledge/registry-argv-and-flag-audit.md
MISSING knowledge/tb2-torch-tensor-parallel-offline.md
MISSING lessons/round-44-verifier-spotcheck.md
MISSING lessons/round-46-verifier-spotcheck.md
MISSING lessons/round-47-verifier-spotcheck.md
MISSING lessons/round-48-verifier-spotcheck.md
MISSING lessons/round-49.md
MISSING lessons/round-50-verifier-spotcheck.md
MISSING lessons/round-50.md
MISSING lessons/round-51-verifier-spotcheck.md
MISSING lessons/round-52-verifier-spotcheck.md
MISSING lessons/round-53-verifier-spotcheck.md
MISSING lessons/round-54-verifier-spotcheck.md
MISSING lessons/round-55-verifier-spotcheck.md
MISSING lessons/round-56-verifier-spotcheck.md
MISSING lessons/round-57-verifier-spotcheck.md
MISSING lessons/round-58-verifier-spotcheck.md
MISSING lessons/round-59-verifier-spotcheck.md
MISSING lessons/round-60-verifier-spotcheck.md
MISSING lessons/round-61-verifier-spotcheck.md
MISSING lessons/round-62-verifier-spotcheck.md
MISSING lessons/round-63-verifier-spotcheck.md
MISSING lessons/round-64-verifier-spotcheck.md
MISSING lessons/round-65-verifier-spotcheck.md
MISSING lessons/round-66-verifier-spotcheck.md
MISSING lessons/round-66.md
MISSING lessons/round-67-verifier-spotcheck.md
MISSING lessons/round-67.md
MISSING lessons/round-68-verifier-spotcheck.md
MISSING lessons/round-69-verifier-spotcheck.md
MISSING lessons/round-70-verifier-spotcheck.md
MISSING lessons/round-71-verifier-spotcheck.md
MISSING lessons/round-72-verifier-spotcheck.md
MISSING lessons/round-73-verifier-spotcheck.md
MISSING lessons/round-73.md
MISSING lessons/round-74-verifier-spotcheck.md
MISSING lessons/round-74.md
MISSING lessons/round-75.md
MISSING-EVIDENCE round10-fleet
MISSING-EVIDENCE round11-fleet
MISSING-EVIDENCE round12-fleet
MISSING-EVIDENCE round13-coverage
MISSING-EVIDENCE round24-census
MISSING-EVIDENCE round24-sources
MISSING-EVIDENCE round25-calibration
MISSING-EVIDENCE round25-sources
MISSING-EVIDENCE round26-calibration
MISSING-EVIDENCE round26-sources
MISSING-EVIDENCE round27-calibration
MISSING-EVIDENCE round27-sources
MISSING-EVIDENCE round28-calibration
MISSING-EVIDENCE round29-attempt2
MISSING-EVIDENCE round29-calibration
MISSING-EVIDENCE round34
MISSING-EVIDENCE round53
MISSING-EVIDENCE round54
MISSING-EVIDENCE round60
MISSING-EVIDENCE round75
PREDICATE R75-C1 fail
```

`python3 plans/round75_c1_index_parity.py --selftest --work /fast/scratch/hyaku/kengaku-r75/C1GateReplayR75/selftest --rev HEAD` — rc=0

```text
LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd
WORKTREE clean
SELFTEST ok clean rc=0 want=0
SELFTEST ok missing-knowledge rc=1 want=1
SELFTEST ok missing-lesson rc=1 want=1
SELFTEST ok missing-evidence rc=1 want=1
SELFTEST ok orphan-knowledge rc=1 want=1
SELFTEST cases=5 red=4 failures=0 ok=True
```

`python3 plans/round75_c1_index_parity.py --control-rowshuffle --work /fast/scratch/hyaku/kengaku-r75/C1GateReplayR75/control --rev HEAD` — rc=0

```text
LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd
WORKTREE clean
NAIVE rows=6 surfaces=6 equal=True
UNIVERSE knowledge files=2 indexed=1 missing=1 orphan=0
UNIVERSE lessons files=2 indexed=0 missing=2 orphan=0
UNIVERSE evidence dirs=2 indexed=1 missing=1 orphan=0
MISSING knowledge/b.md
MISSING lessons/round-1.md
MISSING lessons/round-2.md
MISSING-EVIDENCE d2
PREDICATE R75-C1-control pass
```

### Sixth-arm battery — rc=1

```text
LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd
WORKTREE clean
SELFTEST ok clean rc=0 want=0
SELFTEST ok missing-knowledge rc=1 want=1
SELFTEST ok missing-lesson rc=1 want=1
SELFTEST ok missing-evidence rc=1 want=1
SELFTEST ok orphan-knowledge rc=1 want=1
SELFTEST FAIL fenced-knowledge rc=0 want=1
SELFTEST cases=6 red=5 failures=1 ok=False
```

### Real-byte fixture driver — rc=0

```text
ARM fenced-knowledge
UNIVERSE knowledge files=2 indexed=2 missing=0 orphan=0
UNIVERSE lessons files=2 indexed=2 missing=0 orphan=0
UNIVERSE evidence dirs=2 indexed=2 missing=0 orphan=0
CENSUS_RC 0
README_BYTES '# fixture README\n\n| `knowledge/a.md` | fixture | src |\n```\n| `knowledge/b.md` | fixture | src |\n```\n| `lessons/round-1.md` | fixture | ptr |\n| `lessons/round-2.md` | fixture | ptr |\n\n- `corpus/evidence/d2/` fixture\n- `corpus/evidence/d1/` fixture\n'
LANE_TIP unknown
WORKTREE clean
UNIVERSE knowledge files=2 indexed=2 missing=0 orphan=0
UNIVERSE lessons files=2 indexed=2 missing=0 orphan=0
UNIVERSE evidence dirs=2 indexed=2 missing=0 orphan=0
PREDICATE R75-C1 pass
EMIT_RC 0
ARM trailing-space
UNIVERSE knowledge files=2 indexed=1 missing=1 orphan=1
UNIVERSE lessons files=2 indexed=2 missing=0 orphan=0
UNIVERSE evidence dirs=2 indexed=2 missing=0 orphan=0
MISSING knowledge/b.md
ORPHAN knowledge/b.md 
CENSUS_RC 1
ARM case-duplicate
UNIVERSE knowledge files=2 indexed=2 missing=0 orphan=1
UNIVERSE lessons files=2 indexed=2 missing=0 orphan=0
UNIVERSE evidence dirs=2 indexed=2 missing=0 orphan=0
ORPHAN knowledge/B.md
CENSUS_RC 1
ARM orphan-lesson
UNIVERSE knowledge files=2 indexed=2 missing=0 orphan=0
UNIVERSE lessons files=2 indexed=2 missing=0 orphan=1
UNIVERSE evidence dirs=2 indexed=2 missing=0 orphan=0
ORPHAN lessons/ghost.md
CENSUS_RC 1
ARM orphan-evidence
UNIVERSE knowledge files=2 indexed=2 missing=0 orphan=0
UNIVERSE lessons files=2 indexed=2 missing=0 orphan=0
UNIVERSE evidence dirs=2 indexed=2 missing=0 orphan=1
ORPHAN-EVIDENCE ghost
CENSUS_RC 1
ARM directory-md
UNIVERSE knowledge files=2 indexed=2 missing=0 orphan=0
UNIVERSE lessons files=2 indexed=2 missing=0 orphan=0
UNIVERSE evidence dirs=2 indexed=2 missing=0 orphan=0
CENSUS_RC 0
```

## Scope, cleanup, risks, and handoff

`rm -rf /fast/scratch/hyaku/kengaku-r75/C1GateReplayR75` returned 0 before this report was written; exclusive scratch removed. Commands and all replay outputs are retained above; the attack copy and fixtures were intentionally removed. No persistent implementation/proposal file was requested or produced. Only the assigned report changed. No landing-tip replay was performed: assignment pinned A1; L1 owns landing verification.

Risks for L1: detached-ref `unknown` stamps, duplicate verdict stamps, an absent regular-file type guard, and Markdown context ambiguity. Existing adversarial whitespace/case/orphan tests pass but are absent from the five-case battery. Suggested integration checks: the frozen landing command and target counts, first-two-line revision identity, receipt/stdout byte comparison, and typed-file/context arms if those interpretations are adopted without changing the frozen claim.

Self-evaluation (1–5): accuracy 4 (crafted fixtures establish parser behavior, not a current landing exploit); completeness 5 (three modes, stamps, sixth arm, real-byte probes, comparisons, cleanup retained); clarity 4 (raw output is long but preserves auditability); actionability 4 (L1 must decide Markdown semantics within frozen bounds); conciseness 4 (full before receipt retained for exact evidence). Overall 4.2. Improvements: retain duplicate-stamp distinction when pricing receipts; type-check the declared file universe; do not conflate crafted green fixtures with current corpus compromise. Would the user agree? Evidence supports the bounded findings; semantic qualification is explicit.
