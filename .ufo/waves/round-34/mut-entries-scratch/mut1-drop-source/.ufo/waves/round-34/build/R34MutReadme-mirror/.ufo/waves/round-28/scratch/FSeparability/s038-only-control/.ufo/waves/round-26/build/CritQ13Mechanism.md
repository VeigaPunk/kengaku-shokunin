# CritQ13Mechanism — attack on the Q13 gate-timing mechanism (round 26, build, critic, read-only)

Target: `plans/round-26-claims.md:20-26`, live uncommitted `corpus/QUALITY.md:97-106`, and the checker as written:
`/tmp/kengaku-r26-ExecGateTimingCheck-4/plans/gate_timing_check.py` (untracked; sha256 `ee6d6708…83f5`). Scratch `/tmp/critq13/mk.py`
(sha256 `d520ac23…bbce`) builds `/tmp/critq13-sbx` (one branch per case) and runs that checker; the lane and clones were only read.

## Counterexamples (exit = checker exit code)
1. **The red-before does not test timing.** `--lesson corpus/lessons/round-25.md` exits 1 at `8ea41f9`, `8239a56` (82
   falsify reports) and `9d8a00d` (87). The admit row is byte-identical at 8ea41f9 and 9d8a00d, so the red means "no report
   path cited", not "cited before it existed". `QUALITY.md:103-104` gives the timing reason, which overstates the red. The
   timing leg (`missing_second`, `:249`) runs only in selftest "absent path red" and my S7-L1 (exit=1).
2. **Wording luck: none in the exit code, some in the message.** S11 "Q10 re-read by the falsify wave" still exits 1, but
   `GENERIC_PATTERNS` (`:32-37`) misses the phrase and names nothing. S10 (one real path plus "the rest of the falsify wave")
   exits 0 with nothing flagged. The exit code never depends on generic references (`:270`, `:326-327`).
3. **The real luck was timing.** 8ea41f9 landed before any falsify report existed. 17 min later, at 8239a56, the registry
   had 87 members and 82 reports. The 5 missing include `RevEntryQBar` and `RevGateSection`, whose final VERDICTs say the
   landed entry fails Q10. S9 copies the 82 real reports; the cell cites only `falsify/ReopenS027.md` (SURVIVES) → **exit 0**.
4. **A cited report can contradict the admit.** S8 uses real bytes: the 8ea41f9 lesson and entry, with the cell citing
   `falsify/RevEntryQBar.md` and `falsify/RevGateSection.md` (9d8a00d bytes) → **exit 0**, though both verdicts say Q10
   breaks. S3 (`VERDICT: FAIL … do not admit`) also exits 0. Of the 26 falsify reports naming the entry at 9d8a00d, 4 say
   SURVIVES and 22 PARTIAL, so "cite ≥1 existing report" allows citing only the 4. Nine falsify reports contain more than
   one `VERDICT:` (CritTrendsFresh quotes a tool's `VERDICT: PASS` before its own final PARTIAL); a first-match parse misreads them.
5. **Placeholder reports pass.** S1 (empty `falsify/Stub.md`), S6 (integrator-written `falsify/INDEX.md`) and S5
   (`falsify/Link.md`, a symlink to `build/Writer.md`) each exit 0. Existence is the whole test (`:246`).
6. **Self-review passes.** S2 (cited seat == `writer:`) exits 0; the checker has no writer logic, yet `QUALITY.md:99-101`
   says "not the entry's writer" and "never cites a seat that has not returned". S4 (real path plus non-existent
   `LateSeat.md`) exits 0: unresolved bare names are printed, never failed (`:262-270`). No knowledge entry has a `writer:`
   field (`git grep -nE '^(writer|author)' e0037a8 -- corpus/knowledge` → 0), so fixture (d) has nothing to read in real
   entries. All four ExecGateTimingFixtures lessons (`late-report.md`, …) exit **2**: the checker requires basename
   `round-<N>.md` (`:398-400`). The fixtures' expected `FAIL,FAIL,PASS,FAIL` cannot be run as shipped.
7. **The caller picks the commit.** S7 exits 1 at the admitting commit and 0 one commit later; nothing checks that
   `--commit` admitted the entry. Real data separates them cheaply: `git cat-file -e 8ea41f9^:corpus/knowledge/attribution-interval-calibration.md`
   fails (8ea41f9 admits), while `9d8a00d^` already has the entry.
8. **The Gate-only scope misses other future-dated evidence.** At 8ea41f9, `round-25.md:5` cites
   `.ufo/waves/round-25/falsify/*.md` (0 matches in that tree) and says "(92 seats)" while the tree held 90 build reports
   (92 registry members; `SrcReiczigelExact` and `StateSelftestExec` landed later).

## Impacted axes
- **Calibration (owned):** Q13 can be green while Q10 fails (S8, S9: false PASS); `QUALITY.md`'s `Check:` line claims writer and return coverage the command does not test (false provenance).
- **Novelty/coverage:** the C1 entry's admission rides on Q13; an always-green gate repeats round 25's "admitted entry fails its bar" outcome. All items are fixable defects; the one real tradeoff is (d).

## Smallest safe correction (read-only git plus committed registry/spec JSON; every rule fails closed)
- (a) **Landing identity:** the candidate path must be absent at `<commit>^` and present at `<commit>`, else exit 1. Fixes 7.
- (b) **Real return:** count only full repo-relative paths (bare, relative or unresolved `.md` in an admit row is red, as
  `QUALITY.md:99` already says). The file must be mode 100644 and a member of its wave's `swarm-registry.json`, with role
  not scribe/executor and a name absent from earlier-wave registries; it must name the candidate path and end with a
  `^VERDICT:` line. The r25 registries are all `spawn` with no cross-wave names, so the tip stays green. Fixes 5, 6, fixture (d).
- (c) **Designated completeness:** every seat whose committed `<wave>-spec.json` prompt names the candidate must have its report in the
  tree and be cited. In r25 that is 5 seats; `RevEntryQBar` was absent at 8239a56 (red), all 5 present at 9d8a00d. Fixes 3 and cherry-picking.
- (d) **No silent contradiction:** each cited report's last `^VERDICT:` must start SURVIVES/PASS, or the cell pairs it
  with a correction `path:line` present in the same tree. The r25 designated verdicts are 1 SURVIVES and 4 PARTIAL, so 4
  dispositions are needed. Tradeoff for the judge: admits wait for corrections, matching the r25 closure's expansion ruling.
- (e) **Whole-lesson resolution:** every `.ufo/waves/round-N/…` path or glob anywhere in the lesson must match ≥1 blob at the commit. Fixes 8.
- (f) **Honest red:** re-word `QUALITY.md:103-104` to "no report path cited (same red at 9d8a00d)". Add S1–S9 as
  selftest/fixture cases. Rename the fixture lessons to `round-26.md`, one per case branch.

No installs or updates (python3 and git were present). Only lane file written: this report; scratch: `/tmp/critq13/mk.py`, `/tmp/critq13-sbx`.

VERDICT: Q13 as built is vacuous — real round-25 bytes pass while the cited reports say Q10 fails (S8, S9 exit 0), and placeholder, self-review and unreturned citations pass; its 8ea41f9 red does not depend on wording but does not test timing either (same red at 9d8a00d); fix with rules (a)–(f), with (d) the one tradeoff for the judge.
