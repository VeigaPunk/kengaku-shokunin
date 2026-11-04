# ReviewerC1R77 — R77-C1 adversarial review

Axes: coverage and calibration. Recommendation only; no admission/judgment or production edits.

## Findings, severity first

1. **High — unresolved secondary anchors can launder superseded surfaces into a full green.** `plans/round77_c1_declared_surfaces.py:398-405` resolves only `toks[0]` for hash/count/exec, but `:513-527` credits *every* anchor toward supersession. `g-count-wrong-file` declares registry A with `` `b.md` `a.md` ``, reads B, and claims A's supersession; `d-extra-unresolved-anchor` similarly carries nonexistent `gone.md` as the unprobed second token. Both CLI attacks returned rc 0, `UNLISTED n=0`, `RESOLVED live=27`, `AGREE agree=28 disagree=0`, `DEFECTS n=0`, pass. Stated survivor limit: coverage is anchor-text coverage, not resolved-identity coverage. Merely replacing the absent anchor without retaining it is caught (d, rc 1).

2. **High — fabricated execution evidence passes.** `:337-358` checks script existence, a substring `exit 0`, and ancestor stamp only; it does not establish receipt commitment, script identity, or an actual execution. Fixture script is `raise SystemExit(1)`; receipt is fabricated `LANE_TIP <ancestor>\nexit 0\n`. `f-forged-exec` returned rc 0 and the full target metrics. Stated survivor limit: even uncommitted fabricated receipt text counts as live execution. This is weaker than frozen C1's “committed run receipt”; unlike C2, C1 does not explicitly limit itself to syntactic receipt honesty.

3. **Medium — declared remote bypass accepts loopback.** `:408-409` returns remote for any recognized token without host classification. Replacing the remote API row with `http://127.0.0.1:9`, retaining REMOTE date, returned rc 0 with live=27/agree=28. Stated survivor limit: the sole non-live row need not actually be remote. The generic no-egress remote limit does not establish that a loopback surface is legitimately exempt.

4. **Medium — deleting declarations is visible only through cardinality, readily padded away.** `:518-529` uses current superseded tables, not their frozen universe; `:468-471` counts duplicate rows as live and never emits duplicate defects. Deleting the absent canonical row and its older declaration yielded `UNLISTED n=0`, defects=0 but rc 1 from total=27/live=26/agree=27. Adding one duplicate existing-path row restores rc 0. A 28-row inventory with only one repeated local path plus one remote row passes. Stated survivor limit: neither unique identities nor preservation of the older declaration universe is enforced. Noanchor padding is caught via NOANCHOR/agree, but live=27 remains unchanged even for those failed resolutions.

5. **Medium — declared verdict agreement is not actually checked symmetrically.** `:483-491` accepts an absent path with verdict cell `present ABSENT 2026-11-04`. `extra-contradictory-verdict` returned rc 0, agree=28, disagree=0. Stated survivor limit: AGREE is marker validation, not equality of the declaration's verdict word to the probe verdict.

6. **Medium — full sha256 pins ignore their interior.** `:314-321` truncates the parsed head to its first eight characters even when supplied a full digest. Changing the ninth hex character of a real 64-character digest yielded rc 0 (`extra-full-hash-interior-drift`). Stated survivor limit: a full digest is not verified as full; this does not establish a false result for the current intentionally shortened pins.

7. **Medium — --rev count fallback mixes trees.** `:324-332` falls back to worktree when the file is absent at the revision. Direct call with Reader(base, frozen revision), `b.md`, rows=1 returned `('present', 'rows=1 pin=1 path=b.md')`, while `git cat-file -e <rev>:b.md` returned rc 128: path exists on disk but not in revision. Stated survivor limit: count data need not belong to the requested tree, contrary to frozen claims :69-70. Separately, --rev path and exec checks intentionally remain host/worktree probes: the same --rev CLI first returned rc 0, then rc 1 with seven defects after replacing the scratch corpus symlink with an empty scratch directory. This is a reproducibility limit, not alone a violation of the explicitly live-host claim.

8. **Low — exact frozen TARGET line is never rendered.** `:566-567` omits `defects=0`, although frozen claims :47 and the assignment require it. The observed green run printed `TARGET total=28 unlisted=0 live=27 agree=28 disagree=0`; `DEFECTS n=0` appears separately. Numerical predicate enforces defects, but the promised literal output does not reproduce.

## Method and bounds

Read frozen claims in full before any command. Freeze lookup command `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format=%H -- plans/round-77-claims.md` returned rc 0, `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`. Diff command `git -C ... diff 07c97fcd -- plans/round77_c1_declared_surfaces.py` returned rc 0, 797 inserted lines. Counter bytes were copied into seat scratch before executing fixtures. No git mutations or installs occurred. `.git` symlinks supported read-only ancestor/tree queries; no clone or commits were needed.

LSP unavailable: `read xd://lsp` returned “No such tool”; no semantic references/definition/diagnostics result is claimed. Used literal grep for cited branches and claims/PROVINCE references, plus actual fixture execution. Grep patterns included `head\[:8\]|kind == "remote"|live \+=|canon_anchors.extend|toks\[0\]|path.read_text|master\^|metrics.get|TARGET total`. No canonical runtime routing/resume logic is changed by this scoped counter; resume_continuity_v1 and saturation are outside this assignment.

### Reproduction fixture recipe

All commands below ran via Python subprocess with captured stdout/stderr and exit status. The scratch prefix was `/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77`. A baseline fixture contains `exists.md` (text exists), `script.py` (`raise SystemExit(1)`), `a.md` (`| S001 | x |`), `b.md` (`| S001 | other |`), and a canonical markdown table with 27 uniquely named rows all declaring `path`, anchor `exists.md`, verdict present, plus one `remote` row at `https://example.invalid` with REMOTE 2026-11-04. Supersedes cells are Core:RowN but no older table exists except where specified. This establishes the minimal target-satisfying inventory, not a proposed production inventory.

Attack a replaces two rows with anchor `nothing` (not a recognized path), verdict present; duplicate-padding arm uses baseline unchanged. Attack b removes every canonical row. Attack c first changes row 0 to `gone.md`, absent ABSENT 2026-11-04, and adds a Core table row naming `gone.md`; deletion arm removes both, padded arm replaces with baseline. Attack d changes that canonical row to existing `exists.md`, present, retaining older gone.md; enhanced arm uses kind count with anchors `b.md` and `gone.md`, rows=1. Attack e changes remote anchor to loopback :9. Attack f changes row 0 to exec script.py with exit=0 receipt=forged.txt and the fabricated ancestor stamp. Attack g changes row 0 to count B then A with rows=1 and an older table declaring A. Extra verdict/hash arms are described above.

For h, scratch root `h-revision` symlinks each lane top-level entry and .git read-only. Both commands use frozen revision `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`. Between them only the scratch corpus symlink is unlinked and replaced by an empty scratch directory; lane corpus is untouched. The direct count fallback arm uses fixture b.md absent from that revision.

## Commands and complete captured outputs

### baseline

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline`

Exit: 0. 

```text
PROVINCE_REV worktree
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 present path Row0 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 2 present path Row1 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 3 present path Row2 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 4 present path Row3 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 5 present path Row4 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 6 present path Row5 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 7 present path Row6 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 8 present path Row7 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 9 present path Row8 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 10 present path Row9 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 11 present path Row10 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 12 present path Row11 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 13 present path Row12 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 14 present path Row13 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 15 present path Row14 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 16 present path Row15 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 17 present path Row16 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 18 present path Row17 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 19 present path Row18 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 20 present path Row19 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 21 present path Row20 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 22 present path Row21 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 23 present path Row22 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 24 present path Row23 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 25 present path Row24 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 26 present path Row25 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 27 present path Row26 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/baseline/exists.md
SURFACE 28 remote remote Remote urls=1
SURFACES total=28 present=27 absent=0 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=2 unique=2 sha256=0e42b7d8d218b769…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass

```

### a-noanchor-pad

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad`

Exit: 1. 

```text
PROVINCE_REV worktree
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 noanchor path Pad0 no-anchor
SURFACE 2 noanchor path Pad1 no-anchor
SURFACE 3 present path Row2 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 4 present path Row3 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 5 present path Row4 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 6 present path Row5 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 7 present path Row6 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 8 present path Row7 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 9 present path Row8 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 10 present path Row9 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 11 present path Row10 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 12 present path Row11 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 13 present path Row12 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 14 present path Row13 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 15 present path Row14 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 16 present path Row15 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 17 present path Row16 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 18 present path Row17 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 19 present path Row18 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 20 present path Row19 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 21 present path Row20 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 22 present path Row21 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 23 present path Row22 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 24 present path Row23 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 25 present path Row24 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 26 present path Row25 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 27 present path Row26 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-noanchor-pad/exists.md
SURFACE 28 remote remote Remote urls=1
SURFACES total=28 present=25 absent=0 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=26 disagree=2
DEFECTS n=2
IDENTITIES n=3 unique=3 sha256=be030f541ca5b66d…
DEFECT NOANCHOR 4 Pad0
DEFECT NOANCHOR 5 Pad1
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 fail

```

### a-duplicate-resolved-pad

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad`

Exit: 0. 

```text
PROVINCE_REV worktree
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 present path Row0 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 2 present path Row1 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 3 present path Row2 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 4 present path Row3 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 5 present path Row4 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 6 present path Row5 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 7 present path Row6 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 8 present path Row7 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 9 present path Row8 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 10 present path Row9 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 11 present path Row10 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 12 present path Row11 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 13 present path Row12 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 14 present path Row13 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 15 present path Row14 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 16 present path Row15 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 17 present path Row16 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 18 present path Row17 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 19 present path Row18 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 20 present path Row19 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 21 present path Row20 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 22 present path Row21 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 23 present path Row22 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 24 present path Row23 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 25 present path Row24 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 26 present path Row25 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 27 present path Row26 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/a-duplicate-resolved-pad/exists.md
SURFACE 28 remote remote Remote urls=1
SURFACES total=28 present=27 absent=0 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=2 unique=2 sha256=33ca3ea9982eadee…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass

```

### b-delete-canonical

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/b-delete-canonical`

Exit: 1. 

```text
PROVINCE_REV worktree
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE dirty
CANONICAL source=none rows=0
SURFACES total=0 present=0 absent=0 remote=0
UNLISTED n=0
RESOLVED live=0
AGREE agree=0 disagree=0
DEFECTS n=1
IDENTITIES n=0 unique=0 sha256=e3b0c44298fc1c14…
DEFECT CANONICAL-MISSING 0 no `## Declared surfaces` inventory in PROVINCE.md
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 fail

```

### c-before-delete

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete`

Exit: 0. 

```text
PROVINCE_REV worktree
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Missing path=gone.md
SURFACE 2 present path Row1 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 3 present path Row2 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 4 present path Row3 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 5 present path Row4 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 6 present path Row5 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 7 present path Row6 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 8 present path Row7 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 9 present path Row8 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 10 present path Row9 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 11 present path Row10 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 12 present path Row11 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 13 present path Row12 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 14 present path Row13 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 15 present path Row14 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 16 present path Row15 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 17 present path Row16 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 18 present path Row17 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 19 present path Row18 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 20 present path Row19 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 21 present path Row20 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 22 present path Row21 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 23 present path Row22 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 24 present path Row23 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 25 present path Row24 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 26 present path Row25 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 27 present path Row26 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-before-delete/exists.md
SURFACE 28 remote remote Remote urls=1
SURFACES total=28 present=26 absent=1 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=3 unique=3 sha256=ec66a6e3e44bcf78…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass

```

### c-delete-both

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both`

Exit: 1. 

```text
PROVINCE_REV worktree
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=27
SURFACE 1 present path Row1 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 2 present path Row2 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 3 present path Row3 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 4 present path Row4 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 5 present path Row5 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 6 present path Row6 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 7 present path Row7 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 8 present path Row8 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 9 present path Row9 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 10 present path Row10 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 11 present path Row11 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 12 present path Row12 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 13 present path Row13 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 14 present path Row14 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 15 present path Row15 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 16 present path Row16 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 17 present path Row17 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 18 present path Row18 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 19 present path Row19 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 20 present path Row20 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 21 present path Row21 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 22 present path Row22 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 23 present path Row23 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 24 present path Row24 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 25 present path Row25 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 26 present path Row26 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-both/exists.md
SURFACE 27 remote remote Remote urls=1
SURFACES total=27 present=26 absent=0 remote=1
UNLISTED n=0
RESOLVED live=26
AGREE agree=27 disagree=0
DEFECTS n=0
IDENTITIES n=2 unique=2 sha256=8d5a2ebbc4f579af…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 fail

```

### c-delete-and-pad

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad`

Exit: 0. 

```text
PROVINCE_REV worktree
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 present path Row0 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 2 present path Row1 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 3 present path Row2 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 4 present path Row3 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 5 present path Row4 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 6 present path Row5 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 7 present path Row6 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 8 present path Row7 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 9 present path Row8 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 10 present path Row9 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 11 present path Row10 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 12 present path Row11 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 13 present path Row12 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 14 present path Row13 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 15 present path Row14 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 16 present path Row15 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 17 present path Row16 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 18 present path Row17 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 19 present path Row18 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 20 present path Row19 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 21 present path Row20 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 22 present path Row21 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 23 present path Row22 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 24 present path Row23 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 25 present path Row24 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 26 present path Row25 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 27 present path Row26 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/c-delete-and-pad/exists.md
SURFACE 28 remote remote Remote urls=1
SURFACES total=28 present=27 absent=0 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=2 unique=2 sha256=e47c682dd1bb1fc5…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass

```

### d-substitute-anchor

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor`

Exit: 1. 

```text
PROVINCE_REV worktree
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 present path Missing path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 2 present path Row1 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 3 present path Row2 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 4 present path Row3 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 5 present path Row4 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 6 present path Row5 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 7 present path Row6 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 8 present path Row7 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 9 present path Row8 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 10 present path Row9 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 11 present path Row10 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 12 present path Row11 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 13 present path Row12 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 14 present path Row13 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 15 present path Row14 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 16 present path Row15 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 17 present path Row16 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 18 present path Row17 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 19 present path Row18 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 20 present path Row19 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 21 present path Row20 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 22 present path Row21 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 23 present path Row22 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 24 present path Row23 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 25 present path Row24 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 26 present path Row25 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 27 present path Row26 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-substitute-anchor/exists.md
SURFACE 28 remote remote Remote urls=1
SURFACES total=28 present=27 absent=0 remote=1
UNLISTED n=1
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=1
IDENTITIES n=2 unique=2 sha256=25e56fbcedcbf542…
DEFECT UNLISTED-SURFACE 36 ### Core: gone.md
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 fail

```

### e-loopback-remote

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote`

Exit: 0. 

```text
PROVINCE_REV worktree
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 present path Row0 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 2 present path Row1 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 3 present path Row2 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 4 present path Row3 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 5 present path Row4 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 6 present path Row5 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 7 present path Row6 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 8 present path Row7 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 9 present path Row8 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 10 present path Row9 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 11 present path Row10 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 12 present path Row11 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 13 present path Row12 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 14 present path Row13 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 15 present path Row14 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 16 present path Row15 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 17 present path Row16 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 18 present path Row17 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 19 present path Row18 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 20 present path Row19 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 21 present path Row20 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 22 present path Row21 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 23 present path Row22 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 24 present path Row23 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 25 present path Row24 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 26 present path Row25 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 27 present path Row26 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/e-loopback-remote/exists.md
SURFACE 28 remote remote Remote urls=1
SURFACES total=28 present=27 absent=0 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=2 unique=2 sha256=e833d55b72de7081…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass

```

### f-forged-exec

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec`

Exit: 0. 

```text
PROVINCE_REV worktree
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 present exec False execution receipt=forged.txt exit=0 tip=9ebb8ed1
SURFACE 2 present path Row1 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 3 present path Row2 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 4 present path Row3 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 5 present path Row4 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 6 present path Row5 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 7 present path Row6 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 8 present path Row7 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 9 present path Row8 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 10 present path Row9 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 11 present path Row10 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 12 present path Row11 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 13 present path Row12 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 14 present path Row13 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 15 present path Row14 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 16 present path Row15 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 17 present path Row16 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 18 present path Row17 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 19 present path Row18 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 20 present path Row19 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 21 present path Row20 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 22 present path Row21 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 23 present path Row22 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 24 present path Row23 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 25 present path Row24 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 26 present path Row25 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 27 present path Row26 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/f-forged-exec/exists.md
SURFACE 28 remote remote Remote urls=1
SURFACES total=28 present=27 absent=0 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=3 unique=3 sha256=5d0ab9fde641fc25…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass

```

### g-count-wrong-file

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file`

Exit: 0. 

```text
PROVINCE_REV worktree
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 present count Registry A rows=1 pin=1 path=b.md
SURFACE 2 present path Row1 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 3 present path Row2 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 4 present path Row3 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 5 present path Row4 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 6 present path Row5 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 7 present path Row6 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 8 present path Row7 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 9 present path Row8 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 10 present path Row9 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 11 present path Row10 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 12 present path Row11 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 13 present path Row12 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 14 present path Row13 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 15 present path Row14 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 16 present path Row15 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 17 present path Row16 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 18 present path Row17 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 19 present path Row18 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 20 present path Row19 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 21 present path Row20 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 22 present path Row21 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 23 present path Row22 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 24 present path Row23 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 25 present path Row24 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 26 present path Row25 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 27 present path Row26 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/g-count-wrong-file/exists.md
SURFACE 28 remote remote Remote urls=1
SURFACES total=28 present=27 absent=0 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=3 unique=3 sha256=a6b8ab2bcf860674…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass

```

### landing-worktree

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin`

Exit: 0. 

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=5f8bf0491e1a1c44…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass

```

### h-revision-before

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/h-revision --rev 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`

Exit: 0. 

```text
PROVINCE_REV 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 present path Own probe artifacts path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/h-revision/corpus/evidence
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/h-revision/plans/attrib-r21-frozen.md
SURFACE 18 present path Corpus gate docs path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/h-revision/corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 present path Public literature (cite anchor) path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/h-revision/corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 present path Open-model catalog digest path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/h-revision/corpus/knowledge/open-model-catalogs.md
SURFACE 24 present exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt exit=0 tip=07c97fcd
SURFACE 25 present exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt exit=0 tip=07c97fcd
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 present path Corpus index path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/h-revision/corpus/README.md
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=26 unique=26 sha256=f9e8ca1a59d3d52a…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass

```

### h-revision-after-local-corpus-removal

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/h-revision --rev 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`

Exit: 1. 

```text
PROVINCE_REV 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
LANE_TIP 9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Research notes (SSOT for eval craft) path=~/Projects/webzites/repos/llm-wiki
SURFACE 2 absent path Research notes (former wikillm path) path=~/wikillm/llm-wiki
SURFACE 3 absent path Local benchmark battery path=~/archive/bench-arena
SURFACE 4 absent path Local benchmark battery (former path) path=~/bench-arena
SURFACE 5 absent http Served local model (:34113) http=000
SURFACE 6 absent http Served local model (:45669) http=000
SURFACE 7 present http Served local router (:1234) http=415
SURFACE 8 absent path Route telemetry path=~/Projects/bounties/ledger/telemetry.jsonl
SURFACE 9 absent path Bounty-hunter tree path=~/Projects/the-bounty-hunter
SURFACE 10 absent path Client CLI telemetry path=~/.bailian/telemetry.jsonl
SURFACE 11 absent path Client CLI sync state path=~/.bailian/wiki-sync-state.json
SURFACE 12 absent path Model catalogs (local index) path=~/.bailian/skills/bailian-docs-llm-wiki/models/
SURFACE 13 remote remote Model catalogs (remote APIs) urls=2
SURFACE 14 absent path Own probe artifacts path=corpus/evidence/
SURFACE 15 present hash In-repo verdict gate sha256=90c87c88…ae941f pin=90c87c88…ae941f
SURFACE 16 present hash Attribution instrument sha256=489f938a…16e06b pin=489f938a…16e06b
SURFACE 17 present path Attribution frozen tables path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/h-revision/plans/attrib-r21-frozen.md
SURFACE 18 absent path Corpus gate docs path=corpus/QUALITY.md
SURFACE 19 present count Public-literature registry rows=245 pin=245 path=corpus/SOURCES.md
SURFACE 20 present hash ds-flash-shim source (read-only) sha256=42d86d99…15a386 pin=42d86d99…15a386
SURFACE 21 present tcp Live probe endpoint tcp=127.0.0.1:8791
SURFACE 22 absent path Public literature (cite anchor) path=corpus/knowledge/eval-prior-art-calibration.md
SURFACE 23 absent path Open-model catalog digest path=corpus/knowledge/open-model-catalogs.md
SURFACE 24 execunverified exec Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt absent
SURFACE 25 execunverified exec State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt absent
SURFACE 26 absent cmd Serving-stack process pin (rounds 10-14) path=/proc/1299/cmdline
SURFACE 27 absent path Ephemeral probe trees (rounds 4-7) path=/tmp/bench-r4 expanded=5 live=0
SURFACE 28 absent path Corpus index path=corpus/README.md
SURFACES total=28 present=7 absent=18 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=21 disagree=7
DEFECTS n=7
IDENTITIES n=27 unique=27 sha256=d91db8359900c4e1…
DEFECT STALE-TEXT 1036 Own probe artifacts
DEFECT STALE-TEXT 1040 Corpus gate docs
DEFECT STALE-TEXT 1044 Public literature (cite anchor)
DEFECT STALE-TEXT 1045 Open-model catalog digest
DEFECT EXEC-UNVERIFIED 1046 Interval re-verdict instrument receipt=corpus/evidence/round77/exec-attrib-calibration.txt absent
DEFECT EXEC-UNVERIFIED 1047 State-assertion check receipt=corpus/evidence/round77/exec-state-check.txt absent
DEFECT STALE-TEXT 1050 Corpus index
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 fail

```

### h-count-fallback

Command: `resolve_count(base, "b.md", "1", Reader(base, HEAD)); git cat-file -e HEAD:b.md`

Exit: direct function result (no process exit). git subprocess exit: 128. 

```text
('present', 'rows=1 pin=1 path=b.md')
STDERR:
fatal: path 'b.md' exists on disk, but not in '9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb'

```

### d-extra-unresolved-anchor

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor`

Exit: 0. 

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 present count Missing rows=1 pin=1 path=b.md
SURFACE 2 present path Row1 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 3 present path Row2 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 4 present path Row3 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 5 present path Row4 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 6 present path Row5 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 7 present path Row6 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 8 present path Row7 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 9 present path Row8 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 10 present path Row9 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 11 present path Row10 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 12 present path Row11 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 13 present path Row12 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 14 present path Row13 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 15 present path Row14 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 16 present path Row15 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 17 present path Row16 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 18 present path Row17 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 19 present path Row18 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 20 present path Row19 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 21 present path Row20 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 22 present path Row21 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 23 present path Row22 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 24 present path Row23 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 25 present path Row24 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 26 present path Row25 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 27 present path Row26 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/d-extra-unresolved-anchor/exists.md
SURFACE 28 remote remote Remote urls=1
SURFACES total=28 present=27 absent=0 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=3 unique=3 sha256=15bbf915dd2f8126…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass

```

### extra-contradictory-verdict

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict`

Exit: 0. 

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 absent path Missing path=gone.md
SURFACE 2 present path Row1 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 3 present path Row2 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 4 present path Row3 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 5 present path Row4 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 6 present path Row5 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 7 present path Row6 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 8 present path Row7 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 9 present path Row8 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 10 present path Row9 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 11 present path Row10 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 12 present path Row11 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 13 present path Row12 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 14 present path Row13 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 15 present path Row14 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 16 present path Row15 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 17 present path Row16 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 18 present path Row17 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 19 present path Row18 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 20 present path Row19 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 21 present path Row20 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 22 present path Row21 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 23 present path Row22 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 24 present path Row23 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 25 present path Row24 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 26 present path Row25 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 27 present path Row26 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-contradictory-verdict/exists.md
SURFACE 28 remote remote Remote urls=1
SURFACES total=28 present=26 absent=1 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=3 unique=3 sha256=2e1076836009cc35…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass

```

### extra-full-hash-interior-drift

Command: `python3 /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/counter.py --lane /fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift`

Exit: 0. 

```text
PROVINCE_REV worktree
LANE_TIP 8da90eb7299435aceb9466d70344bba7046094b2
WORKTREE dirty
CANONICAL source=## Declared surfaces rows=28
SURFACE 1 present hash Hash sha256=55d473e4…7e7a3d pin=55d473e4…
SURFACE 2 present path Row1 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 3 present path Row2 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 4 present path Row3 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 5 present path Row4 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 6 present path Row5 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 7 present path Row6 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 8 present path Row7 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 9 present path Row8 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 10 present path Row9 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 11 present path Row10 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 12 present path Row11 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 13 present path Row12 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 14 present path Row13 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 15 present path Row14 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 16 present path Row15 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 17 present path Row16 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 18 present path Row17 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 19 present path Row18 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 20 present path Row19 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 21 present path Row20 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 22 present path Row21 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 23 present path Row22 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 24 present path Row23 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 25 present path Row24 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 26 present path Row25 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 27 present path Row26 path=/fast/scratch/hyaku/kengaku-r77/ReviewerC1R77/extra-full-hash-interior-drift/exists.md
SURFACE 28 remote remote Remote urls=1
SURFACES total=28 present=27 absent=0 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
IDENTITIES n=3 unique=3 sha256=4fee4cedd4744f68…
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass

```

## Residual risk and verification gaps

No unrun check is called passing. All eight requested attack classes were exercised; fixture outputs do not prove the exact production inventory has been maliciously modified. Landing worktree counter returned rc 0, 28 rows/27 live/28 agree/0 defects. It reported WORKTREE dirty, so this is not a clean-tree closure receipt. Existing host HTTP :1234 answered 415, accepted by the documented any-nonzero-status rule; no capability/identity claim follows. No network redirect/egress attack or TCP malformed-port attack was performed. No end-to-end selftest/mutant battery was rerun: this report concerns adversarial counter behavior, not their original tallies.

Self-evaluation (1–5): accuracy 4 (dirty concurrent worktree, therefore no final-tip assertion); completeness 4 (eight requested classes plus three extra checks, no network redirect test); clarity 4 (full outputs lengthen report); actionability 4 (branch locations and minimal fixture recipes, no production edits authorized); conciseness 4 (raw outputs retained to satisfy receipt requirement). Mean 4.0. Highest-impact next action is to state the surviving identity/receipt/remote limits explicitly rather than claim these attacks are killed; frozen predicate must not be silently changed.

Cleanup: Python shutil.rmtree(seat scratch root) completed without exception; scratch exists=False. No scratch tree remains.
