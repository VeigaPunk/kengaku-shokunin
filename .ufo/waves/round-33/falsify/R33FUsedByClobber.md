# R33FUsedByClobber — S093 used-by and gate clobber

## Frozen S093 state

Inspected `plans/sources_adopt.py` `build_block` at lines 143–181 and the frozen registry row via `git show f0b20aea:corpus/SOURCES.md`. The S093 `used-by` cell at freeze already contains both `corpus/knowledge/benchmark-verifier-execution-model.md` and `corpus/knowledge/benchmark-grader-semantics.md`. The same exact S093 line is at current `HEAD`; `cmp` on extracted line 112 at freeze and HEAD printed `S093 ROW BYTE-IDENTICAL freeze vs HEAD`. `R33ReconPackage.md` §c.2 independently records this and attributes the existing entry pointer to round-32 commit `bcd2a6c`.

Therefore C1 did **not** change S093's used-by cell. The frozen clause that S093 “gains the entry” is inaccurate as a transition; the target-state membership was already true at freeze. New rows S103/S104 were the registry additions.

## Gate behavior and mutation probe

`build_block` constructs `used_by = ", ".join(admitted_entries)` and assigns `cells[10] = used_by` at line 179. It does not read/merge the row's existing used-by cell. Thus a staged row carrying a previous unrelated entry loses it in the output. This is observable in the ordinary gate path; the gate emits an append block, so the overwrite is not itself an in-place registry edit.

Scratch: `/tmp/r33-usedby-clobber/`. Fixture row S103 carried prior `used-by=corpus/knowledge/entryA.md`; command used for pristine and mutant:

```sh
python3 <script> --registry /tmp/r33-usedby-clobber/registry.md --package /tmp/r33-usedby-clobber/package.md --admit-ids S103 --entries corpus/knowledge/new-entry.md --access-date 2026-10-25 --scope-to-admit --out /tmp/r33-usedby-clobber/<variant>-out.md
```

Actual outputs:

```text
pristine: registry=2 staged=2 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote /tmp/r33-usedby-clobber/pristine-out.md rows=1
pristine used-by=[corpus/knowledge/new-entry.md]

mutant: registry=2 staged=2 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote /tmp/r33-usedby-clobber/mutant-out.md rows=1
mutant used-by=[corpus/knowledge/entryA.md, corpus/knowledge/new-entry.md]
```

Mutant was a one-line change at `cells[10]`: replace assignment with `cells[10] = ", ".join(filter(None, (cells[10], used_by)))`. The preservation detector expectation was that the output retain both the prior unrelated entry and the newly admitted entry. Pristine fails that expectation; the mutant satisfies it. Under the mutation-tester rule, pristine detector failure means the mutant is **inconclusive**, not a killed mutant. The observed clobber is nevertheless a coverage finding: the current gate does not preserve unrelated prior used-by values. No contract change is proposed.

The requested S093 gate attempt was also tried in the fixture: `--admit-ids S093` returned exit 0 and emitted the requested entry path, because the fixture's registry contains S091/S092, not S093. It is not evidence that the live gate can append S093: live registry S093 is already present and normal collision detection rejects re-append.

## Hashes and restoration

```text
pristine gate sha256: 38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0
mutated gate sha256:  9080815d357361175fe13c5bc8d6b62670f0eb05fbcbc464b92e9b86dda0cf44
restored gate sha256: 38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0
cmp pristine.py sources_adopt.py: RESTORED_BYTES_MATCH=1
```

Only `/tmp/r33-usedby-clobber/` was mutated. No lane source, index, git/JJ state, or production artifact was edited; no tools installed.

**Verdict:** `INCONCLUSIVE` for the preservation mutant by the mandated pristine-baseline rule; the current implementation demonstrably clobbers pre-existing unrelated used-by values in its emitted block. C1's S093 used-by state was already present at freeze, not changed by C1.
