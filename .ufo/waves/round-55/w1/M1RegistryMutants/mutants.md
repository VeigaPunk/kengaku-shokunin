# R55-W1 M1RegistryMutants — mutation probe of `plans/round52_c2_registry.py`

- Production bytes (read-only, never edited in place): `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c2_registry.py` sha256 `9e6f41a457ec2d847f81d513d30545d982e0a118b4cfa8452af34e1d1a509e6b`; lane HEAD `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (== frozen base tip); worktree clean for this file; scratch copy sha256 `9e6f41a457ec2d847f81d513d30545d982e0a118b4cfa8452af34e1d1a509e6b` (identical).
- Detector (identical on pristine/mutated/restored bytes): `python3 <counter-copy> --lane <fixture>`; fingerprint = the five defect counts + detail lines + exit code.
- Kill rule: focused fixture (built for that leg) flips exit 1→0 with its family count →0, AND the combined fixture loses exactly that family while every other family keeps the pristine count (orthogonality). A surviving mutant = an advertised-but-undemonstrated leg (coverage finding, contract unchanged).

## Baseline (pristine bytes)
| fixture | expectation | actual (exit/MISSING/INCOMPLETE/ENTRY-MISSING/UNBACKED/DUPLICATE) | match |
|---|---|---|---|
| `f1_missing` | 1/1/0/0/0/0 | 1/1/0/0/0/0 | yes |
| `f2_incomplete` | 1/0/1/0/0/0 | 1/0/1/0/0/0 | yes |
| `f3_entry_missing` | 1/0/0/1/0/0 | 1/0/0/1/0/0 | yes |
| `f4_unbacked` | 1/0/0/0/1/0 | 1/0/0/0/1/0 | yes |
| `f5_duplicate` | 1/0/0/0/0/1 | 1/0/0/0/0/1 | yes |
| `f6_knowledge` | 1/1/0/0/0/0 | 1/1/0/0/0/0 | yes |
| `combined` | 1/2/1/1/1/1 | 1/2/1/1/1/1 | yes |

## Mutants
| id | leg | single defect | focused fixture | pristine→mutant (focused) | combined family pristine→mutant | verdict | mutant sha256 |
|---|---|---|---|---|---|---|---|
| `M1-missing-always-empty` | MISSING | MISSING leg returns [] always (advertised-but-unregistered instruments invisible) | `f1_missing` | exit 1→0, [1/0/0/0/0]→[0/0/0/0/0] | missing 2→0 (want 0) | **killed** | `5b8ae1f7e62d0cea7d6352d4b322283c1ef38dd61ae42104607468aadc861f42` |
| `M2-incomplete-ignores-blanks` | INCOMPLETE | INCOMPLETE test all->any: fires only on fully-empty rows, which the separator guard already drops -> rows with blank cells are ignored | `f2_incomplete` | exit 1→0, [0/1/0/0/0]→[0/0/0/0/0] | incomplete 1→0 (want 0) | **killed** | `ad48df934cb5d6e07d5596e776bf6d4dad1e2381a5556bad9f2a0cf1bb99729b` |
| `M3-entry-missing-skipped` | ENTRY-MISSING | ENTRY-MISSING leg skipped (registry rows naming absent scripts pass) | `f3_entry_missing` | exit 1→0, [0/0/1/0/0]→[0/0/0/0/0] | entry_missing 1→0 (want 0) | **killed** | `15b22319bccd85d63efd7ffc2ae64c377cb7fa823d40ea8d1a13956985de015d` |
| `M4-selftest-unbacked-false` | SELFTEST-UNBACKED | selftest_unbacked() returns False always (unbacked self-test claims pass) | `f4_unbacked` | exit 1→0, [0/0/0/1/0]→[0/0/0/0/0] | unbacked 1→0 (want 0) | **killed** | `c9fcf63beb74dfffb79fbd7007632b8cd26e53bc64696a672e18889015cbf6b6` |
| `M5-duplicate-check-removed` | DUPLICATE | DUPLICATE check removed (registry rows may repeat a name) | `f5_duplicate` | exit 1→0, [0/0/0/0/1]→[0/0/0/0/0] | duplicate 1→0 (want 0) | **killed** | `a3bd11a83b12e9a89de4a241ae41ad34b37bd2848e67187ee4b3fceecebcca1a` |
| `M6-universe-drops-knowledge` | advertised-universe | self_assessment_files() no longer scans corpus/knowledge/*.md (instruments advertised only there become invisible to MISSING) | `f6_knowledge` | exit 1→0, [1/0/0/0/0]→[0/0/0/0/0] | missing 2→1 (want 1) | **killed** | `6b611f9d9cd8c9a097c696b161ff7f70e5253986c6a71c4a84d7b2c220903487` |

Family order in `[..]`: MISSING / INCOMPLETE / ENTRY-MISSING / SELFTEST-UNBACKED / DUPLICATE.

## Per-mutant detail
### M1-missing-always-empty — killed
- Mutation: `missing = sorted(set(adv) - set(reg))` → `missing = []` (occurrences matched: 1)
- Focused fixture `f1_missing` pristine exit 1, detail ['  MISSING plans/orphan_tool.py']
- Focused fixture mutant exit 0, detail []
- Combined pristine exit 1 detail ['  MISSING plans/kb_tool.py', '  MISSING plans/orphan_tool.py', '  INCOMPLETE-ROW `blank`', '  ENTRY-MISSING plans/ghost_tool.py', '  SELFTEST-UNBACKED `unbacked`', '  DUPLICATE-ROW `dup`']
- Combined mutant exit 1 detail ['  INCOMPLETE-ROW `blank`', '  ENTRY-MISSING plans/ghost_tool.py', '  SELFTEST-UNBACKED `unbacked`', '  DUPLICATE-ROW `dup`']

### M2-incomplete-ignores-blanks — killed
- Mutation: `incomplete = [r[0] for r in rows if not all(r)]` → `incomplete = [r[0] for r in rows if not any(r)]` (occurrences matched: 1)
- Focused fixture `f2_incomplete` pristine exit 1, detail ['  INCOMPLETE-ROW `t`']
- Focused fixture mutant exit 0, detail []
- Combined pristine exit 1 detail ['  MISSING plans/kb_tool.py', '  MISSING plans/orphan_tool.py', '  INCOMPLETE-ROW `blank`', '  ENTRY-MISSING plans/ghost_tool.py', '  SELFTEST-UNBACKED `unbacked`', '  DUPLICATE-ROW `dup`']
- Combined mutant exit 1 detail ['  MISSING plans/kb_tool.py', '  MISSING plans/orphan_tool.py', '  ENTRY-MISSING plans/ghost_tool.py', '  SELFTEST-UNBACKED `unbacked`', '  DUPLICATE-ROW `dup`']

### M3-entry-missing-skipped — killed
- Mutation: `entry_missing = sorted(s for s in reg if not (lane / s).exists())` → `entry_missing = []` (occurrences matched: 1)
- Focused fixture `f3_entry_missing` pristine exit 1, detail ['  ENTRY-MISSING plans/ghost_tool.py']
- Focused fixture mutant exit 0, detail []
- Combined pristine exit 1 detail ['  MISSING plans/kb_tool.py', '  MISSING plans/orphan_tool.py', '  INCOMPLETE-ROW `blank`', '  ENTRY-MISSING plans/ghost_tool.py', '  SELFTEST-UNBACKED `unbacked`', '  DUPLICATE-ROW `dup`']
- Combined mutant exit 1 detail ['  MISSING plans/kb_tool.py', '  MISSING plans/orphan_tool.py', '  INCOMPLETE-ROW `blank`', '  SELFTEST-UNBACKED `unbacked`', '  DUPLICATE-ROW `dup`']

### M4-selftest-unbacked-false — killed
- Mutation: `return all(f not in body for f in flags)` → `return False` (occurrences matched: 1)
- Focused fixture `f4_unbacked` pristine exit 1, detail ['  SELFTEST-UNBACKED `u`']
- Focused fixture mutant exit 0, detail []
- Combined pristine exit 1 detail ['  MISSING plans/kb_tool.py', '  MISSING plans/orphan_tool.py', '  INCOMPLETE-ROW `blank`', '  ENTRY-MISSING plans/ghost_tool.py', '  SELFTEST-UNBACKED `unbacked`', '  DUPLICATE-ROW `dup`']
- Combined mutant exit 1 detail ['  MISSING plans/kb_tool.py', '  MISSING plans/orphan_tool.py', '  INCOMPLETE-ROW `blank`', '  ENTRY-MISSING plans/ghost_tool.py', '  DUPLICATE-ROW `dup`']

### M5-duplicate-check-removed — killed
- Mutation: `duplicate = sorted({n for n in names if names.count(n) > 1})` → `duplicate = []` (occurrences matched: 1)
- Focused fixture `f5_duplicate` pristine exit 1, detail ['  DUPLICATE-ROW `t`']
- Focused fixture mutant exit 0, detail []
- Combined pristine exit 1 detail ['  MISSING plans/kb_tool.py', '  MISSING plans/orphan_tool.py', '  INCOMPLETE-ROW `blank`', '  ENTRY-MISSING plans/ghost_tool.py', '  SELFTEST-UNBACKED `unbacked`', '  DUPLICATE-ROW `dup`']
- Combined mutant exit 1 detail ['  MISSING plans/kb_tool.py', '  MISSING plans/orphan_tool.py', '  INCOMPLETE-ROW `blank`', '  ENTRY-MISSING plans/ghost_tool.py', '  SELFTEST-UNBACKED `unbacked`']

### M6-universe-drops-knowledge — killed
- Mutation: `files += sorted(kdir.glob("*.md"))` → `pass` (occurrences matched: 1)
- Focused fixture `f6_knowledge` pristine exit 1, detail ['  MISSING plans/kb_tool.py']
- Focused fixture mutant exit 0, detail []
- Combined pristine exit 1 detail ['  MISSING plans/kb_tool.py', '  MISSING plans/orphan_tool.py', '  INCOMPLETE-ROW `blank`', '  ENTRY-MISSING plans/ghost_tool.py', '  SELFTEST-UNBACKED `unbacked`', '  DUPLICATE-ROW `dup`']
- Combined mutant exit 1 detail ['  MISSING plans/orphan_tool.py', '  INCOMPLETE-ROW `blank`', '  ENTRY-MISSING plans/ghost_tool.py', '  SELFTEST-UNBACKED `unbacked`', '  DUPLICATE-ROW `dup`']

## Counter's own `--selftest` battery vs mutants (supplementary)
| variant | --selftest exit |
|---|---|
| pristine | 0 |
| M1-missing-always-empty | 1 |
| M2-incomplete-ignores-blanks | 1 |
| M3-entry-missing-skipped | 0 |
| M4-selftest-unbacked-false | 0 |
| M5-duplicate-check-removed | 0 |
| M6-universe-drops-knowledge | 0 |

The shipped 3-fixture battery (`--selftest`) detects only M1/M2 and is blind to: M3-entry-missing-skipped, M4-selftest-unbacked-false, M5-duplicate-check-removed, M6-universe-drops-knowledge — i.e. it exercises the MISSING and INCOMPLETE legs only.

## Restoration evidence
- Production sha256 after probe: `9e6f41a457ec2d847f81d513d30545d982e0a118b4cfa8452af34e1d1a509e6b` — unchanged: True
- Restored scratch copy sha256: `9e6f41a457ec2d847f81d513d30545d982e0a118b4cfa8452af34e1d1a509e6b`
- Detector on restored bytes vs pristine baseline on the combined fixture: identical output = True (exit 1, fingerprint fail)

## Findings
- 6/6 mutants killed; 0 survived (each survivor = an advertised-but-undemonstrated leg).
- Coverage note: the shipped `--selftest` battery covers clean/MISSING/INCOMPLETE only; the ENTRY-MISSING, SELFTEST-UNBACKED, DUPLICATE and knowledge-file legs of the advertised-universe have no self-test fixture in the tool itself.
