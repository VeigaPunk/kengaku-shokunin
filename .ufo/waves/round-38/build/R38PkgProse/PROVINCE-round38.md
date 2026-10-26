Paste target: `PROVINCE.md`, appended after `## Round37 partial frontier admission (2026-10-26)`
(and after its `**Reported out (round 37):**` paragraph). Nothing above it is edited.

## Round38 partial frontier admission (2026-10-26)

**Core addition:** offline execution of one more pinned Terminal-Bench 2.0 grader —
`build-pmars/tests/test_outputs.py` at terminal-bench-2 `2fd12b88` — over 22 frozen synthetic build states,
via `corpus/knowledge/tb2-build-pmars-grader.md` (S115, S116), `plans/build_pmars_probe.py` and receipt
`corpus/evidence/round38/build-pmars-probe.txt` (`cases=22 observed_pass=7 observed_fail=15 mismatches=0`;
the first recorded run `e95cf55` and a second run are byte-equal). The graded state is a class new to this
lane: a built executable plus a source tree, scored by file presence, a string scan of `ldd` stdout,
directory shape and a regex over program stdout — nothing is rebuilt. Each case runs the captured module's
four test functions directly in a per-case bubblewrap sandbox: private network/pid/ipc namespaces,
case-owned `/app` and `/usr/local/bin` + `/usr/local/sbin`, `/tests/test_outputs.py` bound read-only, a fixed
`PATH`; the canned artefacts are compiled on the host with `gcc`. `tests/test.sh` is read, not run: its
`uvx`/pytest path and its `/logs/verifier/reward.txt` write are outside the probe. It records how that
captured grader answers those synthetic states only: it does not run Terminal-Bench, the task image or the
oracle (`solve.sh` is captured and not executed), does not validate or certify the task, measure difficulty,
gameability or contamination, judge whether the grader's `Results:` and debugger address patterns are the
right ones, or speak for the remaining 85 TB2 task graders (89 carry `tests/test.sh`; 4 are read). Host bash
stands in for the image's shell, and host glibc and host `ldd` for the image's. Disclosed ordering: a
control-time gate rerun had already executed the probe once before the freeze and its output was discarded
unread (`plans/round-38-claims.md` §Disclosure); the receipt is the first recorded run. Adjacent: build and
package craft (tameshi), capture and citation method (chousa), deployment configuration and runtime task
validity (refused). The round35/36/37 paragraphs above stay as written; this paragraph narrows only their
"remaining TB2 tasks" clause for this one task.

Word count of the paste block above: 294.
