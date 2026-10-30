# R54-C2 independent row audit

Source clone: `/fast/scratch/hyaku/kengaku-r54/E6RowAudit01/clone`, created with `git clone --shared`; `git rev-parse --show-toplevel` returned that clone root. For each row, ran the exact declared `entry_argv` from that directory using the imported `hermetic_env` from `plans/round54_c2_entrytruth.py`, with row-specific `TMPDIR` under `/fast/scratch/hyaku/kengaku-r54/E6RowAudit01/` and 600-second subprocess timeout.

All script paths existed in the clone and all argv vectors were entry mode (no `--selftest`, `--help`/`-h`, `--dry`, or `--version`).

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| adoption-check | 1 | 1 | true | CONFIRMED |
| anchor-digest-check | 1 | 1 | true | CONFIRMED |
| attrib-probe | 0 | 0 | n/a (green row has no evidence field) | CONFIRMED |

## Commands and output tails

`adoption-check`

```text
python3 plans/adoption_check.py --lane . --expect .ufo/waves/round-33/claims/adoption-expect.json --census
exit=1
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=fail
```
The ledger's declared evidence fragment exactly matched the observed line.

`anchor-digest-check`

```text
python3 plans/anchor_digest_check.py --lane .
exit=1
DEFECT S191 anchor token=fe3c9111af175648440fc2b46fe81d256bd651cf9ccd5e00ba3a281391c77379 class=anchor-unbound detail=row-carries-no-capture-locator loc=corpus/SOURCES.md:206
DEFECT S192 anchor token=c87a8650fd772a462612755dc2e84b09af902524118fa0205938403c300a92b4 class=anchor-unbound detail=row-carries-no-capture-locator loc=corpus/SOURCES.md:207
DEFECT S193 anchor token=7ea938c578d4505b86feff2f596daee4e517c84a41807c147af65d32e8183f20 class=anchor-unbound detail=row-carries-no-capture-locator loc=corpus/SOURCES.md:208
rows=190 tokens=92 defects=21
```
The declared evidence fragment (the S173 defect line) appeared in observed output; the tail above shows final output lines. The run also emitted S174 onward, consistent with the final 21-defect count.

`attrib-probe`

```text
python3 plans/attrib_probe.py freeze-check --frozen plans/attrib-r23-frozen.md
exit=0
FREEZE-CHECK: reads=1 block_sha=1b2d6a01bfa431ec pinned=1b2d6a01bfa431ec stable=True -> OK
```
No evidence fragment is declared for this green ledger row.

No timeouts or mismatches. No tools installed or updated.
