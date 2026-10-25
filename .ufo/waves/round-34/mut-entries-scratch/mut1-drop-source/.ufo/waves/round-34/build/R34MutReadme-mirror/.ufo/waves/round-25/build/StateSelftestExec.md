# StateSelftestExec — C2 mutation fixtures (round 25, build wave)

Seat KengakuR25.StateSelftestExec (executor, writer). Clone `/tmp/kengaku-r25-StateSelftestExec`, branch `r25-StateSelftestExec`,
observed base `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a` (= 6180e4f + claims/considerthese only). Every fixture byte comes from
`git show 6180e4f:<file>`. Nothing committed; live lane, jj state and index untouched.

## Files changed (clone, untracked: `git status` → `?? plans/fixtures/`)
`plans/fixtures/r25/state-check/`: EXPECTED.tsv + 7 fixtures. 777 files, 748,860 bytes apparent (git stores the 6 copies once).
Per fixture: `<fx>/PROTOCOL.md` (fleet PROTOCOL.md:439-451 verbatim, `cmp` exit 0; found by the peer's `root.parent/PROTOCOL.md`
lookup) + `<fx>/kengaku-shokunin/`, which is the `--root`.

## Tree listing (all-true; each mutant = all-true + one hunk)
    EXPECTED.tsv
    {all-true,p2a-wrong-token,p2b-dead-anchor,p2c-shonen-prose,p2d-unmarked-absent,p2e-dead-row,p2e-unindexed-file}/
      PROTOCOL.md
      kengaku-shokunin/SCORECARD.md      221 lines = base 1-169,551-561,582-622 (cmp exit 0); line 162 = base r14 novelty row
      kengaku-shokunin/SHONEN.md         canonical seed, one bare pointer per box: SKILL.md, LOG.md, corpus/README.md, PROVINCE.md
      kengaku-shokunin/PROVINCE.md       37 lines: base 1-11; 9 Surfaces rows (R1-R6 host paths -> ./host-only/… + **ABSENT**,
                                         R3 URL-only, R7-R9 verbatim); Refusals / Province map / Historical headings (all in base)
      kengaku-shokunin/corpus/README.md  143 lines = base 1-6,25-160 + 1 row appended after lessons/round-24.md (spotcheck lesson)
      kengaku-shokunin/corpus/SOURCES.md base minus the S026 row → census `rows: 25`, `A=24 C=1`, `mined=18 queued=5 rejected=2`,
                                         dup/enum/mined-path checks empty (the frozen CORPUS.md commands, run in the fixture root)
      kengaku-shokunin/grader.py, plans/attrib_probe.py   stand-ins printing the base output recorded in round24-census/after.txt
      kengaku-shokunin/SKILL.md, LOG.md, plans/attrib-r23-frozen.md   one-line placeholders
      kengaku-shokunin/corpus/knowledge/ 32 · lessons/ 26 · evidence/ 28 .log + 14 dirs (13 .keep, round24-census/after.txt verbatim)
    111 files per fixture (p2e-dead-row 110)

## EXPECTED.tsv (fixture · exit · mismatch_count · mismatch_id · injected_at · mutation)
    all-true            0 0 -                                                  none (3 OFFLINE_UNVERIFIABLE, 1 OUT_OF_POPULATION row)
    p2a-wrong-token     1 1 P2a.capability.offline-replay-gate                 SCORECARD.md:174 `CHECKS n=733 …` -> `n=734 …`
    p2b-dead-anchor     1 1 P2b.axis.novelty.anchor.1                          SCORECARD.md:209 `:162` -> `:1620` (file 221 lines)
    p2c-shonen-prose    1 1 P2c.box.1.evidence-line                            SHONEN.md:7 extra indented base box-1 prose line
    p2d-unmarked-absent 1 1 P2d.surface.Research notes (SSOT for eval craft).path PROVINCE.md:12 `**ABSENT**` dropped, path absent
    p2e-dead-row        1 1 P2e.row-to-file.knowledge/attrib-r21.md            file deleted, base row corpus/README.md:37 kept
    p2e-unindexed-file  1 1 P2e.file-to-row.knowledge/attrib-prior-art-r21.md  base row (README:36) deleted, file kept
Single mutation: `diff -r all-true <fx>` prints exactly one hunk per mutant. Ids are StateCheckExec's, confirmed by message, incl. (d)/(e).

## Prediction (filed before any run; state_check NOT run per wave rule)
Against peer `plans/state_check.py` sha256 `bf40fc16…73075` (21:49:50): all-true → `assertions=231 match=228 mismatch=0
offline_unverifiable=3` + 1 OUT_OF_POPULATION, exit 0. Each mutant → `assertions=231 match=227 mismatch=1 offline_unverifiable=3`,
exit 1. Split: P2a 3 · P2b 9 · P2c 9 · P2d 11 (3 OU) · P2e 99+100. Cross-check: my own parse of the base README index = 99 rows,
identical in order to the peer's README_INDEX_PATHS. Base on-disk set = those 99 + lessons/round-24-verifier-spotcheck.md.

## Findings
- F1 (base; peer adopted): SCORECARD.md:557 sources-registry states `A=24 C=1`, `mined=18 queued=5 rejected=2`. The CORPUS.md:135-141
  census on base SOURCES.md gives `rows: 26`, `tiers: A=24 C=2`, `statuses: mined=18 queued=5 rejected=3` (S026, e21f9ea). The peer
  used to mark this OFFLINE_UNVERIFIABLE; it now runs the census, so the BEFORE run should show this row as a mismatch.
- F2 (base; peer adopted): PROVINCE.md:14 Served local model. The old code `test -e`d `/proc/1299/cmdline` (pid reuse makes that
  host-dependent); rows whose first span is a URL are now offline_unverifiable.
- F3: with frozen populations, a new unindexed knowledge file is OUT_OF_POPULATION, not a mismatch. So p2e-unindexed uses a base file
  with its base row deleted, and C1's new knowledge entry is out of state_check's reach (the census must cover it).
- F4: `plans/fixtures` falls under round24_census.sh `for f in plans/*` (plans_indexed +1) with no README §plans row. F5: no `~` paths.

## Risks and check for L1
The peer reports no edits after bf40fc16 and says the ids are stable. The stable contract is exit + id + count; totals depend on the
implementation. Post-integration: `python3 plans/state_check.py --root plans/fixtures/r25/state-check/<root> --json` per row.
Digests: EXPECTED.tsv `db59f6d4…0adc7`; sorted-content manifest `7e2c9da1…4213b`; scratch generator (not committed)
`/tmp/kengaku-r25-StateSelftestExec-scratch/gen_state_fixtures.py` `dcea1a73…57bc7`.
Installs: none.
VERDICT: 7 fixture trees + EXPECTED.tsv built from base bytes, one diff-proven false assertion each, ids match peer impl bf40fc16; 2 base defects found and adopted.
