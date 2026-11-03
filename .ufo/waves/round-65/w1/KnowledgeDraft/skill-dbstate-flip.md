# SKILL.md `db-state` row — flip cell for round 65 (R65-C1)

Target: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/SKILL.md`, the `db-state` row of the
decision table `## Decision table — grader class → offline replay recipe` (line 83 at base tip
`12a6255170bcc466029bf82037885fd69e20370f`).

**This cell is applied by the L1 only on a R65-C1 pass.** If the predicate fails, SKILL.md keeps
its base bytes — the flip is not applied on a MISS.

## Full replacement row (apply verbatim)

Replace the whole base row

```
| db-state | 2 | recipe-unexecuted | would need a replay that stages the database state the grader opens (its own sqlite or server-side state) inside the sandbox and lets the grader query it; no committed probe replays this class. | `corpus/evidence/round62/class-survey.txt`, `corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py` |
```

with this single row:

```
| db-state | 2 | executed 1 of 2 (round 65, R65-C1 pass): sqlite-with-gcov replayed offline; query-optimize stays recipe-unexecuted (a median-ratio timing threshold and a sha-pinned external database make its legs not freezable offline on this host) | a lane-built gcov-instrumented `sqlite3` compiled in place from the pinned SQLite amalgamation (S233) and staged on PATH inside the bwrap house shape, with the host `/usr/bin/sqlite3` masked by a read-only `/dev/null` bind so a pass can only come from the lane-built candidate, and the case dir bound at both `/app` and its host absolute path so the compile-time-absolute `.gcda` path resolves inside the sandbox; the grader's own three legs decide each case. The probe is `plans/round65_c1_sqlite_probe.py` and its receipt of record is `corpus/evidence/round65/sqlite-gcov-probe.txt`. The `query-optimize` member stays recipe-unexecuted: its median-ratio timing threshold (`solution median ≤ 1.05 × golden median`) and its sha-pinned external database make its legs not freezable offline on this host. | `corpus/evidence/round62/class-survey.txt`, `corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py`, `corpus/evidence/round65/sqlite-gcov-probe.txt`, `plans/round65_c1_sqlite_probe.py` |
```

## Cell-by-cell diff against the base row

| cell | base | replacement |
|---|---|---|
| class | `db-state` | unchanged |
| count | `2` | unchanged — member counts are untouched (the r63 depth gate's `count_mismatch=0` depends on it) |
| executed | `recipe-unexecuted` | `executed 1 of 2 (round 65, R65-C1 pass): sqlite-with-gcov replayed offline; query-optimize stays recipe-unexecuted (a median-ratio timing threshold and a sha-pinned external database make its legs not freezable offline on this host)` |
| replay recipe | `would need a replay that stages the database state the grader opens …; no committed probe replays this class.` | the executed mechanics (in-place gcov build from S233, PATH staging, `/dev/null` mask, dual bind for the compile-time-absolute `.gcda` path, the grader's own three legs deciding), naming `plans/round65_c1_sqlite_probe.py` and `corpus/evidence/round65/sqlite-gcov-probe.txt`; the `query-optimize` recipe-unexecuted reason is retained in this cell as well as in the status cell |
| receipt pointer | `corpus/evidence/round62/class-survey.txt`, `corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py` | both kept, plus the new receipt `corpus/evidence/round65/sqlite-gcov-probe.txt` and the probe `plans/round65_c1_sqlite_probe.py` |

## Why the row cannot be applied before the pass

- The status cell asserts `R65-C1 pass`. The predicate is the frozen one in
  `plans/round-65-claims.md`; the counting command is
  `python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt; echo $?`
  → last line `PREDICATE R65-C1 pass`, exit 0.
- The row's status cell is the class-census statement "one of two members executed". The other
  member (`query-optimize`) is named explicitly as still recipe-unexecuted, with its reason
  (`corpus/evidence/round52/graders/query-optimize/tests/test_outputs.py`: the median-ratio
  threshold `assert summary["solution"]["median_s"] <= 1.05 * summary["golden"]["median_s"]` at
  line 142, and the sha-pinned external database `expected_hash = "89eab7555b6b86a74b8e0ee5a7db7beec0b2575a45cd2b22fe132eae79f5ad5a"`
  at line 78 over `/app/oewn.sqlite`). Those two facts make its legs not freezable offline on
  this host — the named reason the row reads `1 of 2` and not `executed`.

## The r63 depth gate after the flip

The claims doc requires the r63 depth gate to be re-run after the flip and to stay green
(`ROWS n=16 class_match=True count_mismatch=0`). The replacement row preserves the gate's
mechanics:

- five cells (`class | count | executed | replay recipe | receipt pointer`), count cell `2`;
- the pointer cell keeps at least one resolvable path token (all four of the listed paths are
  lane-relative and resolve);
- the new backticked path tokens in the row (`plans/round65_c1_sqlite_probe.py`,
  `corpus/evidence/round65/sqlite-gcov-probe.txt`) are lane-relative, contain no `..`, and
  resolve once the probe and receipt are committed — which is the same landing that applies this
  row.

Observed at base tip `12a6255170bcc466029bf82037885fd69e20370f`, before any flip:

```
$ python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt
ROWS n=16 class_match=True count_mismatch=0 paths total=26 resolved=26 share=1.00
PREDICATE R63-C2 pass
exit=0
```

**Flipped-row rehearsal** (this seat, scratch only — the lane's SKILL.md was NOT edited). The
replacement row above was extracted verbatim from this file and substituted into a scratch copy of
SKILL.md; the scratch root mirrored the lane's `corpus/` and `plans/` trees by symlink and
carried stand-in files for the two paths that exist only after the landing (`plans/round65_c1_sqlite_probe.py`,
`corpus/evidence/round65/sqlite-gcov-probe.txt`):

```
$ python3 plans/round63_gate_checks.py depth --skill <scratch>/SKILL.md \
    --receipt corpus/evidence/round62/class-survey.txt --root <scratch>
ROWS n=16 class_match=True count_mismatch=0 paths total=28 resolved=28 share=1.00
PREDICATE R63-C2 pass
exit=0
```

The two new path tokens raise the total from 26 to 28 and both resolve, so the flipped row keeps
the gate green on the same terms as the base row. This rehearsal says nothing about the
predicate: it prices the flip's table mechanics only.

The class-census receipt `corpus/evidence/round62/class-survey.txt` is frozen r62 evidence and is
NOT edited by this flip.

## Scope of this cell

This cell changes ONE line of ONE file (SKILL.md, the `db-state` row). It does not touch:
`plans/round-65-claims.md` (frozen), the probe or its receipt, `corpus/SOURCES.md`, the r62
census receipt, or any other class row. The dated flip note goes in LOG.md by the L1 (the claims
doc: "the flip is recorded in SKILL + LOG + the round report"); the knowledge entry
`corpus/knowledge/tb2-sqlite-gcov-offline.md` (S232/S233 cited) is admitted by the L1 on the same
pass.
