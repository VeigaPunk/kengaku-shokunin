# R49C2MutPins — C2 mutation probe

Axes named: **coverage** (assigned). No admission claim is made.

## Freeze and detector

Verified stage-1 commit `9d2900af41e4d1fc6022eff99010436fde6dbd93` exists (`cat-file -t` → `commit`), dated `2026-10-28 09:14:40 -0300`, and is an ancestor of lane HEAD `af88aab193e6034cb9b386472064e3c18fa90128` (`ANCESTOR-OK`). The freeze predates this measurement. Clone was checked out at the exact freeze REV.

The frozen tree has `plans/round46_c3_verify.py`; the stage-2 `plans/round49_c2_verify.py` and `plans/mutants49/` were absent. The bounded detector selected V1,V3,V4,V5(--dry only),V7,V9,V10,V12; no full probe, package gate, or ordering check was run.

Exact baseline command:

```sh
python3 -c 'import pathlib,sys,tempfile; sys.path.insert(0,"<clone>/plans"); import round46_c3_verify as c; lane=pathlib.Path("<clone>"); p=c.real_pkg(lane); w=tempfile.mkdtemp(prefix="baseline-",dir="<scratch>"); r=c.run_legs(lane,p,w,("V1","V3","V4","V5","V7","V9","V10","V12")); print("BOUNDED",sum(not ok for _,ok,_ in r),"of",len(r))'
```

Observed baseline output:

```text
V1 ok listed=8 wrong=0 extra=0
V3 ok rows=7 bad=0
V4 ok cases=18 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V7 DEFECT rows=5 tags=7 bad=["unparsed row '| instruction.md:7 | both-print | not exercised | '", "unparsed row '| instruction.md:9 | toolchain | not exercised | n", "tags missing=['both-print', 'toolchain'] duplicated=0"]
V9 ok case_rows=18/18 bad=0
V10 ok mechanism_rows=18/18 bad=0
V12 ok rows=7 defective=0 live=0
BOUNDED 1 of 8
```

## Mutation attempt and verdict

Attempted separate capture, probe, spec, receipt, dry-table, and entry variants, but created the variants with `cp -al`; these hard-linked files. The first `edit` therefore modified shared scratch inodes, contaminating the baseline clone and the supposed variants. The supposed mutant runs all printed `PACKAGE DEFECT ValueError plans/pkg-spec-r46.json is not at its freeze digest (receipt_sha256 masked)`; they are **not valid sensitivity measurements** and do not establish killed mutants. Their printed before/after hashes were equal, confirming that the mutation was shared rather than isolated. No kill/survive claim is made.

The incorrect test setup was discarded. I removed those scratch directories and recloned at the frozen REV. Restoration evidence: `RESTORED-CLONE-AT-FROZEN-REV`; `git rev-parse --show-toplevel` matched the clone directory, `git rev-parse HEAD` matched `9d2900af41e4d1fc6022eff99010436fde6dbd93`, and pristine spec SHA-256 was restored to `f9a0e3ccbe5c0643c98995d41d4da3821ef27ddd3f86eee87b5a562c99db3171`. No lane file was modified. Scratch clone was removed before yield.

Source provenance opened via the frozen round-48 lesson: `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py`, accessed 2026-10-27; located quote: `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]`.

Limits: stage-2 C2 verifier and mutant plan were not present at the frozen REV; the attempted mutant measurements are invalid due to the hardlink mistake. Exact commands run included the freeze `cat-file`/`log`/`merge-base` checks, `git clone --shared` and checkout, the bounded baseline Python invocation above, the attempted per-variant detector invocations, and fresh reclone/REV/spec-hash restoration check. No tools installed.

VERDICT: **INCONCLUSIVE — no valid mutant killed/survived result.** The clean baseline demonstrates the pre-existing V7 defect; the attempted mutation batch is discarded. Scratch clone removed before yield.
