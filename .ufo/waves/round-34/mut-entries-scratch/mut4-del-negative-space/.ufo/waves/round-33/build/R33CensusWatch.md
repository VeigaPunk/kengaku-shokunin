# R33CensusWatch — freshness re-verification receipts (round 33, hyaku run 7)

Seat: census/receipts leaf. Writes: only `.ufo/waves/round-33/build/receipts/*` (5 files) and this report.
No production edits, no scratch tree under `/tmp` needed, no tool installs (nothing missing).
Access date: 2026-10-25. Tree observed: lane HEAD `7895588` (`78955888542258ba369f5aa72c200c913b4c3c90`),
with in-flight sibling edits present (see §Tree state). Receipts captured 14:22:46–14:22:59 -0300.

## Deliverables and exit codes

All five commands ran in `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, stdout+stderr redirected to the
receipt file (raw, unedited). Exit codes captured by the wrapper shell immediately after each run.

| # | command (lane cwd) | receipt | exit | expected | observed |
|---|---|---|---|---|---|
| 1 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | `census-t1.txt` | **0** | 0, 15 W04 | 0, 15 W04 lines + `kengaku ok` |
| 2 | `python3 grader.py` | `grader.txt` | **0** | CHECKS n=733 mismatches=0, VERDICT PASS | n=733 mismatches=0, PASS |
| 3 | `python3 plans/sources_adopt.py --selftest` | `adopt-selftest.txt` | **0** | selftest pass | `cases=17 failed=0` |
| 4 | `python3 plans/state_check.py --selftest` | `state-selftest.txt` | **0** | selftest pass | `[selftest] ALL PASS …` |
| 5 | `git status --porcelain` | `status.txt` | **0** | clean capture | 11 paths (4 ` M`, 7 `??`) |

`VERDICT: receipts-taken`

## Exact retained evidence (verbatim lines)

`census-t1.txt` (16 lines): 15 `W04` warnings, then
`kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md`.
No `E` codes. W04 ids: S040 S048 S057 S058 S059 S064 S065 S066 S067 S068 S069 S071 S075 S076 S100.
Set is **identical** to the freeze control `.ufo/waves/round-33/claims/census-before.txt`
(`diff` on the W04 lines prints no differences), so the two appended rows (S103/S104) added no new duplicate.

`grader.txt` (2 lines):
```
CHECKS n=733 mismatches=0 errata_pinned=1
VERDICT: PASS — stored evidence fully re-derives offline
```
(`errata_pinned=1` is the grader's own extra counter, emitted at `grader.py:5724`; the claim's expected
`CHECKS n=733 mismatches=0` prefix is present unchanged.)

`adopt-selftest.txt` (18 lines): 17 `CASE … PASS` lines (collision-zero/one/three-space, four-space-not-a-row,
escaped-pipe, prose-recheck, usedby-projected, duplicate-staged-id, clean-package, missing-requested-id,
quote absent/overlong/boundary-25/url-bound/url-mismatch/url-unmapped, quote-located) and
`SELFTEST cases=17 failed=0`.

`state-selftest.txt` (27 lines): all `selftest ok …` mutation-red and supersession lines, terminal
`[selftest] ALL PASS (canonical seed, pointers, out-of-population box, pointer-only, R25–R29-E exact-token
supersession, P2/P3 R27/R29 corrections, P4 R27-only supersession, P2e/P3c OUT_OF_POPULATION retention,
P3a–P3e and P4a–P4e red mutations)`.

`status.txt` (11 lines, exit 0):
```
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/knowledge/benchmark-grader-semantics.md
 M plans/round33_c1_verify.py
?? .ufo/waves/round-33/assimilation/
?? .ufo/waves/round-33/build-dispatch.json
?? .ufo/waves/round-33/build-spec.json
?? .ufo/waves/round-33/build-validate-err.txt
?? .ufo/waves/round-33/build.ready
?? .ufo/waves/round-33/build.ready.dispatched
?? .ufo/waves/round-33/build/
```

### Receipt digests (sha256) and sizes

```
1f8ee8741bafe7743d81190a7e5203c01974f69e720c18679c51c444035ab7f3  census-t1.txt       1505 B
279121d07b1f3a62408a162277341dd3a38e3c5c678ed97b8ad61aaf0a0be044  grader.txt           101 B
4bc9973e1b4bcbf0ca7959684cee8da908eb49b694b80b6a8def0783df56c5c8  adopt-selftest.txt   580 B
64956a1ca28e1650e96dbfb1f4088fd6d581e0250cb79fd4dd9675f9954f9d9c  state-selftest.txt  2058 B
3bca03cb49b9a46415640e82c4b56079ee4ccc5949b8266d1c495c314bdf415b  status.txt           397 B
```

## Tree state at receipt time (mid-integration, not post-integration gate)

These receipts were taken while sibling seats' edits were still uncommitted, and the numbers reflect that:

- Registry reads **97** `| S### |` rows (95 at freeze + the new S103/S104 already appended in the working tree);
  `corpus/knowledge/` holds **41** files (the repaired draft present in-tree); `corpus/README.md` has 196
  table lines. Row S093/S094/S097/S101/S102/S103/S104 all resolve, with S094/S097/S101/S102 still carrying their
  round-32 refusal wording ("supersedes S0xx — … refused …").
- Therefore census-t1 is a **post-append** census, not the 95-row baseline; it still exits 0 with the same 15 W04,
  which is the property the task asked to observe.
- `M plans/round33_c1_verify.py` is a sibling's in-flight counter edit, not this seat's write.

The L1 must re-run these five commands after all seats land / integration commit; this file is a wave-time
snapshot and must not be cited as the post-integration gate result.

## Freshness notes / falsifiers that now hold

- Census: exit 0 with exactly 15 W04, W04 set unchanged from freeze; no new duplicate introduced by S103/S104.
- Grader: 733 checks, 0 mismatches, offline re-derivation still passes with the in-tree draft edits present.
- Both selftests green (17/17 cases; full state_check selftest), so the adoption and state counters are
  trustworthy before any post-integration assertion.
- `git status --porcelain` is non-empty by design at wave time; it will be the baseline the L1 diffs against after
  integration, so a clean-tree claim cannot be made from this receipt.

## Risks / blockers

- None blocking this seat. The only risk is misuse: quoting these exit codes as the final gate while the tree
  still contains the 4 modified + 7 untracked paths above.
- No installs, no network fetches, no writes outside `build/` and `build/receipts/`; fleet repo, shokuknow,
  `.ufo/state`, sinks, and the Git index untouched.

`VERDICT: receipts-taken`
