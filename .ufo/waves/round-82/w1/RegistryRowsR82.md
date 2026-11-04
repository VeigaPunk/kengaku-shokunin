# R82-C1 — registry rows for claim-referenced instruments (seat `RegistryRowsR82`)

Lane `kengaku-shokunin`, round 82, wave w1, role scribe. Measured tip
`12f1029a45cf0097a3afd030d757bf93b87f8018` (freeze commit; `git rev-parse master`), base revision for every
"before"/byte check `a3a03ac31451e58f1742b9bccb73b72c2d90a95c`, claims frozen at
`plans/round-82-claims.md` (read in full first). Scratch:
`/fast/scratch/hyaku/kengaku-r82/RegistryRowsR82/` with one `git clone --shared` at `$S/clone`
(`git -C $S/clone rev-parse --show-toplevel` = `$S/clone`, `git status --porcelain` = 0 lines at clone time);
scratch deleted before yield. This seat wrote no lane byte except this report: `SKILL.md`,
`SCORECARD.md`, `LOG.md`, `corpus/README.md`, the counter and `plans/round82-sweep-map.json` are untouched.

Nothing here re-opens a frozen predicate, universe rule, control or kill rule. The four paths below are the
`MISSING 4` of R82-C1's BASE state (each referenced as a literal path by a claim-bearing document at BASE and
carrying no registry row); the two paths in §2 are the `UNCLASSIFIED 2`. Every cell below was made true by a
command in §4; the three cells/legs I could not execute are named `UNVERIFIED` in §7, never invented.

---

## 1. Deliverable A — four complete registry rows

Paste-ready for `SKILL.md` `## Gate/probe registry` (the header `| name | kind | entry | verdict map | self-test |
pinned values | write scope | owner |` already exists; each row has exactly eight cells, `kind` ∈ {`gate`,
`probe`}, the entry cell names a `plans/*.py` that exists at BASE and `ast.parse`s, the pinned-values and
write-scope cells are non-empty and not `n/a`, and the self-test cell either names a script plus a flag that
occurs in that script's source or says `none declared`).

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `log-appendonly` | gate | `python3 plans/log_appendonly.py --lane .` (lane root; `--path LOG.md`, `--since REV`, `--show-lines`, `--verbose`; no `--work`) | `0` no commit rewrote a committed log line (`violations=0`) · `1` a `VIOLATION <sha12> <date> deleted=<n> at=<lines> first="…"` line per offending commit, then `LOG-APPENDONLY commits=<n> violations=<k>` (measured at `12f1029a`: `commits=141 violations=9`, exit 1 — **red at this tip**, see §5 F1) · `2` SETUP (not a git repo, no git, or `--since <rev>` not an ancestor of HEAD) | `python3 plans/log_appendonly.py --selftest` (7 fixture repos GREEN, RED-EDIT, RED-DELETE, RED-MOVE, SINCE-FULL, SINCE-C1, SINCE-C2 plus BAD-SINCE; measured `SELFTEST pass`, exit 0) | no digest pins — the walk is over the measured tip; historical pair `commits=77 violations=7` at the round-46 base (`LOG.md:1479`); measured pair at `12f1029a` `commits=141 violations=9` | none — read-only git plumbing (`git log --full-history`, first-parent diffs, `GIT_OPTIONAL_LOCKS=0`, no index lock, no ref created); `--selftest` fixtures only under a `tempfile.mkdtemp()` honouring `TMPDIR` | kengaku |
| `round37-c1-attribution` | gate | `python3 plans/round37_c1_attribution.py --lane .` (lane root; `--work DIR` scratch parent, default `$TMPDIR`) | `0` every frozen mutant attributed (`ATTRIBUTED 55/55 UNATTRIBUTED=0`; measured at `12f1029a`, exit 0) · `1` at least one `ATTR <mid> <clause> UNATTRIBUTED` line, then `ATTRIBUTED <n>/55 UNATTRIBUTED=<m>` | none declared | `plans/pkg_gate.py` sha256 `ea63882240e6…` must equal `GATE_SHA256` (`plans/round37_c1_verify.py:58`); the 55 `MUTANTS` and the round-36+37 fixture batteries come from that counter; this is a post-hoc audit, not the frozen C1 rule | scratch under `--work` only (default `$TMPDIR`), removed on exit; the lane is read-only (counter and gate are read, gates are written only into that scratch dir) | kengaku |
| `round66-registry-check` | gate | `python3 plans/round66_registry_check.py quote corpus/lessons/round-66.md` and `python3 plans/round66_registry_check.py meta corpus/SOURCES.md [S### …]` (lane root; `--root DIR` defaults to `$KENGAKU_ROOT` else the script's parent) | `0` every selected check clean (`CHECK ok quote` / `CHECK ok meta`) · `1` a named finding (`CHECK defect: …` per quote miss / refused path / meta phrase, then `CHECK quote fail` or `CHECK meta fail`) — measured at `12f1029a`: quote `quotes=3 misses=0` exit 0, meta `rows=253 findings=3` exit 1 (row S234, `corpus/SOURCES.md:250`; see §5 F2) · `2` SETUP (lesson or registry absent, root without `corpus/evidence/`) or argparse usage | `python3 plans/round66_registry_check.py --selftest --work DIR` (13 named cases, measured all `True`, exit 0) | frozen `META_PHRASES` in code (`word bar`, `teaches is one benefit`, `same source and capture`); `teaches` column = header index, else fallback 6; a row must carry exactly 11 cells; a QUOTE needle must occur as literal bytes inside a capture that resolves under `corpus/evidence/` | none — read-only; selftest fixtures under `--work` and removed before exit | kengaku |
| `round80-c1-remint` | probe | `python3 plans/round80_c1_remint.py --lane <clean clone> --work <scratch>` (`--lane` required; `--only MEMBER` repeatable; `--python PATH`) | `0` every selected receipt minted and every selected ledger row flipped (`REMINT minted=<n> failed=0`; measured with an empty selection: `minted=0 failed=0`, exit 0) · `2` SETUP (worktree not clean before the run or after it, unresolved HEAD, ledger row absent) · `3` a probe run failed (`REMINT-FAIL <member>` with a `timeout`, `rc=` or `no observations` tail) | none declared | frozen table `plans/round80_probes.json` (6 members: cancel-async-tasks, chess-best-move, distribution-search, largest-eigenval, openssl-selfsigned-cert, protein-assembly) + `plans/grader-population-ledger.json`; each receipt stamps `SOURCE_SHA`, `TOOL_SHA`, `MINTED_BY_SHA`, `LANE_TIP` | `corpus/evidence/round80/<member>-probe.txt` receipts **and** an in-place rewrite of `plans/grader-population-ledger.json` (`plans/round80_c1_remint.py:181`); receipts + ledger only, clean tree required before and after; never against the lane | kengaku |

Note on the fourth row: the seat item's phrase "receipts only" is not what the bytes do — the driver also
rewrites the ledger at `:181` (see §5 F3). The row states both so the cell is true.

---

## 2. Deliverable B — two `EXCLUSIONS` entries (`class=support-module`)

Frozen-table shape for the R82-C1 counter (the counter itself is another seat's deliverable; this is the
content its `EXCLUSIONS` map needs). Byte evidence is read from `BASE_REV` bytes, exactly as the claim's rule
requires (no `argparse` import **and** no `__main__` block).

| path | class | byte evidence at `a3a03ac3` | imported by (at `a3a03ac3`) | why it cannot be a row |
|---|---|---|---|---|
| `plans/fixture_fence.py` | `support-module` | 991 lines; `grep -c argparse` = 0; `grep -c __main__` = 0; `ast.parse` imports = `os, pathlib, re, stat` only; top level is constants plus `_`-prefixed collectors and one public entry `def breach(d, argv, tool)` at `:918` — a library called by test drivers, no CLI | `plans/round45_c1_verify.py:62,110,263-268` (loads it by path via `importlib.util.spec_from_file_location`, after copying its bytes into the sandbox); `plans/round46_c1_verify.py:118,217,489`; `plans/round50_c1_verify.py:74,116,203-212`; digest-guarded by `plans/honest50/build_honest_population.py:68,385-399` (`BASE_FENCE_SHA`) | its verdict is a return value to a driver (`breach` → refusal/sentence), not an exit status; running it as `python3 plans/fixture_fence.py` prints nothing and tests nothing |
| `plans/policy_cases.py` | `support-module` | 85 lines; `grep -c argparse` = 0; `grep -c __main__` = 0; zero imports of its own; `ast.parse` top-level names = `CASES` only (59 rows over policies E0–E9, measured `len(CASES)=59`) | `plans/parser_policy_compare.py:29` (`sys.path.insert(0, plans dir)`), `:32` (`import policy_cases  # noqa: E402`), consumed at `:470,477,560` inside `_selftest_policy_cases` and the selftest dispatch | it is a hand-expected data table (fixture table), executed only through `parser_policy_compare.py --selftest`; it has no entry point and no verdict of its own |

---

## 3. Deliverable C — forward-direction note (which claim/round first referenced each instrument)

Top-level CLAUDE cursor is a no-op for this lane. Per row, the first claim-bearing reference at `BASE_REV` is:
`log-appendonly` — `LOG.md:1479` (inside the round-46 section opened at `LOG.md:1453`, "Round 46 (hyaku run 9,
2026-10-27)", repeated at `LOG.md:1490`), landed as `85a40be5` (2026-10-27, round 46); `round37-c1-attribution`
— `SCORECARD.md:1301` (inside the round-37 section opened at `SCORECARD.md:1272`, "Round 37 (hyaku run 8,
2026-10-26)", under `### Limits named at freeze, and found in wave 1`), landed as `357deceb` (2026-10-26, round
37); `round66-registry-check` — `LOG.md:2527` (round-66 section opened at `LOG.md:2521`) and the README index
`corpus/README.md:775` (section opened at `:769`), landed as `e02c2d90` (2026-11-03, round 66); and
`round80-c1-remint` — `corpus/README.md:1001` (section opened at `:995`, "Round-80 supporting artifacts
(2026-11-04)"), landed as `af51132d` (2026-11-04, round 80). The two excluded support modules are referenced
earlier still: `plans/fixture_fence.py` at `LOG.md:1381` (round-45 section, `:1374`) and `SCORECARD.md:2013`
(round-45 section, `:1998`), landed `8f9a898e` (round 45), and `plans/policy_cases.py` at
`corpus/README.md:503` (round-27 section, `:496`, path written `../plans/policy_cases.py`), landed `b5f62e5e`
(round 27). No other claim-bearing document at BASE names any of the six, so the audit's forward direction is
covered by exactly these lines.

---

## 4. Per-cell evidence — exact commands and outputs

All read-only runs used the scratch clone (`cd $S/clone`, `$S=/fast/scratch/hyaku/kengaku-r82/RegistryRowsR82`);
`$S/clone` was `git clone --shared` of the lane at `12f1029a` and its `HEAD` printed
`12f1029a45cf0097a3afd030d757bf93b87f8018` before any run. The lane itself was never a `--lane` target of a
writing tool.

### 4.0 Shared facts (entry existence, ast.parse, tip drift)

```
$ python3 - <<'EOF'   # for each of the four scripts: git show BASE:path | ast.parse, then git diff BASE..HEAD
plans/log_appendonly.py: exists_at_BASE=True ast_parse=True bytes=13159      BASE..tip diff: none
plans/round37_c1_attribution.py: exists_at_BASE=True ast_parse=True bytes=3762    BASE..tip diff: none
plans/round66_registry_check.py: exists_at_BASE=True ast_parse=True bytes=14260   BASE..tip diff: none
plans/round80_c1_remint.py: exists_at_BASE=True ast_parse=True bytes=7749         BASE..tip diff: none
EOF
$ for n in log-appendonly round37-c1-attribution round66-registry-check round80-c1-remint; do grep -c -- "$n" SKILL.md; done
0
0
0
0        # no name collision: the four rows do not exist yet at the tip
```

Exact command run: one `python3 - <<'EOF'` heredoc over the four paths calling
`subprocess.run(["git","show",f"{B}:{rel}"])`, `ast.parse`, and `git diff --stat BASE HEAD -- rel`; the four
`exists_at_BASE=True ast_parse=True` lines and the four `BASE..tip diff: none` lines above are verbatim from its
output (the block is condensed, not reformatted from other runs).

### 4.1 `log-appendonly`

`--help` (flags in the entry cell and the absence of `--work` are read off this output):

```
$ cd $S/clone && python3 plans/log_appendonly.py --help ; echo rc=$?
usage: log_appendonly.py [-h] [--lane LANE] [--path PATH] [--since SINCE]
                         [--show-lines] [--verbose] [--selftest]
options:
  --lane LANE | --path PATH | --since SINCE  bind the walk to <rev>..HEAD
  --show-lines | --verbose  print the walk reconciliation against plain git log | --selftest
rc=0
```

The verdict map's `0`/`1` legs and the tip measurement:

```
$ cd $S/clone && python3 plans/log_appendonly.py --lane . ; echo rc=$?
VIOLATION f147a2706961 2026-09-28 deleted=1 at=9 first="- 2026-09-28 — round 5: closed the last executable gap — full 33-task ba"
VIOLATION 28a2fbfb3e53 2026-10-13 deleted=7 at=22,23,24,25,26,27,28 first=""
VIOLATION 2f00932ddb52 2026-10-14 deleted=1 at=29 first="`.ufo/waves/shokunin12h-20261014-p1-repair/members/`."
VIOLATION 96c9d8fd7d23 2026-10-25 deleted=2 at=641,680 first="Registry 76 → 81 rows (5 tier-A additions; S090 upgraded from the packag"
VIOLATION 66c734c0a1e1 2026-10-25 deleted=3 at=935,936,937 first="hf_schema_delta=4 or_schema_delta=0`. OpenRouter's response exceeds the "
VIOLATION f660ae04a1c5 2026-10-27 deleted=2 at=1374,1388 first="## Round 45 (hyaku run 9, 2026-10-26) — advertised fixture fence closed "
VIOLATION 3d9ea54a558b 2026-10-27 deleted=2 at=1407,1408 first="- Wave `a3w1` (34 re-dispatched wave-2 items): held-out hostile modules "
VIOLATION 7864296ee02a 2026-10-28 deleted=1 at=1595 first="  after-measurement runs in a clean clone of the landing commit."
VIOLATION 3cc5cecb6752 2026-11-04 deleted=2 at=2990,2991 first="  carries a stamp that recomputes at its own revision. Before: `receipts"
LOG-APPENDONLY path=LOG.md head=12f1029a45cf
LOG-APPENDONLY commits=141 violations=9
rc=1
```

The `0` leg (a clean append-only history) and the `2` leg (setup, never a silent zero):

```
$ cd $S/clone && python3 plans/log_appendonly.py --selftest ; echo rc=$?
SELFTEST GREEN rc=0 want_rc=0 ok :: LOG-APPENDONLY commits=2 violations=0
SELFTEST RED-EDIT rc=1 want_rc=1 ok :: LOG-APPENDONLY commits=2 violations=1
SELFTEST RED-DELETE rc=1 want_rc=1 ok :: LOG-APPENDONLY commits=2 violations=1
SELFTEST RED-MOVE rc=1 want_rc=1 ok :: LOG-APPENDONLY commits=2 violations=1
SELFTEST SINCE-FULL rc=1 want_rc=1 ok :: LOG-APPENDONLY commits=3 violations=1
SELFTEST SINCE-C1 rc=1 want_rc=1 ok :: LOG-APPENDONLY commits=2 violations=1
SELFTEST SINCE-C2 rc=0 want_rc=0 ok :: LOG-APPENDONLY commits=1 violations=0
SELFTEST BAD-SINCE rc=2 want_rc=2 ok :: SETUP --since side: not an ancestor of HEAD
SELFTEST pass
rc=0

$ cd $S/clone && python3 plans/log_appendonly.py --lane . --since bogus ; echo rc=$?
SETUP --since bogus: not a commit
rc=2
```

Write-scope cell: the script opens files only for reading; the selftest fixture builder writes under
`tempfile.mkdtemp()` (`plans/log_appendonly.py:191` `selftest` → `:181` `_fixture`), `env["TMPDIR"]` is set at
`:131`, and `env["GIT_OPTIONAL_LOCKS"] = "0"` at `:132` is what takes no index lock. Read, not run: no code path
under `--lane` writes.

### 4.2 `round37-c1-attribution`

```
$ cd $S/clone && python3 plans/round37_c1_attribution.py --help ; echo rc=$?
usage: round37_c1_attribution.py [-h] [--lane LANE] [--work WORK]
options: --lane LANE | --work WORK
rc=0

$ mkdir -p $S/attrwork && cd $S/clone && python3 plans/round37_c1_attribution.py --lane . --work $S/attrwork
ATTR M01 P1 by=r36-P5 -- frozen instrument digest mismatch
ATTR M02 P2 by=p23-p2-receipt-deleted -- receipt unreadable
ATTR M03 P2 by=p23-p2-receipt-byte -- receipt digest differs from the pin
...                                   # 55 ATTR lines in total (grep -c '^ATTR ' = 55)
ATTR M55 D5 by=d5-m55-quote-absent -- d5 quote absent from the capture
ATTRIBUTED 55/55 UNATTRIBUTED=0
rc=0                                   # wall time 15.49 s
```

The `2` leg (SETUP) is cheap to reach and was exercised without touching the lane, with a two-file fake lane:

```
$ mkdir -p $S/fake/plans && cp $S/clone/plans/round37_c1_verify.py $S/clone/plans/pkg_gate.py $S/fake/plans/
$ printf '\n# tamper control\n' >> $S/fake/plans/pkg_gate.py
$ cd $S/clone && python3 plans/round37_c1_attribution.py --lane $S/fake --work $S/attrwork2 ; echo rc=$?
SETUP gate not at its freeze digest
rc=2
$ sha256sum $S/clone/plans/pkg_gate.py ; grep -n GATE_SHA256 $S/clone/plans/round37_c1_verify.py | head -1
ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41  ...
58:GATE_SHA256 = "ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41"
```

### 4.3 `round66-registry-check`

```
$ cd $S/clone && python3 plans/round66_registry_check.py --help ; echo rc=$?
usage: round66_registry_check.py [-h] [--root ROOT] [--selftest] [--work WORK] {quote,meta} ...
positional arguments: {quote,meta}
options: --root ROOT   lane root (default: $KENGAKU_ROOT or the script's parent)
         --selftest | --work WORK
rc=0

$ cd $S/clone && python3 plans/round66_registry_check.py --root . quote corpus/lessons/round-66.md ; echo rc=$?
QUOTE S183 capture=corpus/evidence/round66/sources/torch-tensor-parallelism-test_outputs.py result=FOUND needle='assert parallel_linear_path.exists(), …'
QUOTE S236 capture=corpus/evidence/round66/sources/sqlite-amalgamation-3540100.unzip-l.txt result=FOUND needle='sqlite-amalgamation-3540100/sqlite3.c'
QUOTE S237 capture=corpus/evidence/round66/sources/kv-store-grpc-test_outputs.py result=FOUND needle='assert result == 0, f"Port {port} is not listening - no real gRPC server is running"'
CHECK quote quotes=3 misses=0
CHECK ok quote
rc=0

$ cd $S/clone && python3 plans/round66_registry_check.py --root . meta corpus/SOURCES.md ; echo rc=$?
CHECK defect: meta S234 phrase='word bar' in teaches cell (line 250): "supersedes S230 — same source and capture, anchor quotes the grader's own f-string verbatim, teaches is one benefit within the word bar"
CHECK defect: meta S234 phrase='teaches is one benefit' in teaches cell (line 250): …
CHECK defect: meta S234 phrase='same source and capture' in teaches cell (line 250): …
CHECK meta rows=253 findings=3 teaches_column=6
CHECK meta fail
rc=1

$ cd $S/clone && python3 plans/round66_registry_check.py meta corpus/SOURCES.md S236 S237 ; echo rc=$?
CHECK meta rows=2 findings=0 teaches_column=6
CHECK ok meta
rc=0                                    # the 1 leg is row-attributed, not blanket-red

$ cd $S/clone && python3 plans/round66_registry_check.py quote corpus/lessons/nope.md ; echo rc=$?
SETUP lesson not found: corpus/lessons/nope.md
rc=2

$ cd $S/clone && mkdir -p $S/r66work && python3 plans/round66_registry_check.py --selftest --work $S/r66work ; echo rc=$?
SELFTEST {'quote_pass': True, 'quote_miss': True, 'quote_refuse_outside_evidence': True, 'quote_refuse_absolute': True, 'quote_no_gate': True, 'quote_empty_gate': True, 'meta_pass': True, 'meta_fail': True, 'meta_selection_clean': True, 'meta_selection_dirty': True, 'meta_no_header_fallback': True, 'meta_bad_shape': True, 'meta_missing_id': True}
rc=0
```

### 4.4 `round80-c1-remint` (never run against the lane)

```
$ cd $S/clone && python3 plans/round80_c1_remint.py --help ; echo rc=$?
usage: round80_c1_remint.py [-h] --lane LANE [--work WORK] [--python PYTHON] [--only ONLY]
rc=0

$ printf 'dirt\n' > $S/clone/SCRATCH-DIRT-TEST && cd $S/clone && python3 plans/round80_c1_remint.py --lane . --work $S/remintwork ; echo rc=$?
SETUP worktree not clean (1 paths); run in a fresh clone
rc=2
$ rm -f $S/clone/SCRATCH-DIRT-TEST && git -C $S/clone status --porcelain | wc -l
0

$ sha256sum $S/clone/plans/grader-population-ledger.json
15fb159dab8e3dbff36985f2a4ad7c6341a540eedb67dd1c1f820ac7387e1f44  plans/grader-population-ledger.json
$ ls $S/clone/corpus/evidence/round80 | wc -l
24
$ cd $S/clone && python3 plans/round80_c1_remint.py --lane . --work $S/remintwork --only no-such-member ; echo rc=$?
REMINT minted=0 failed=0
rc=0
$ sha256sum $S/clone/plans/grader-population-ledger.json ; git -C $S/clone status --porcelain | wc -l ; ls $S/clone/corpus/evidence/round80 | wc -l
15fb159dab8e3dbff36985f2a4ad7c6341a540eedb67dd1c1f820ac7387e1f44  plans/grader-population-ledger.json
0
24
```

That last run is the *only* execution leg this seat claims for the `0` cell: it reaches the write block
(`:178-181`) and rewrites the ledger byte-identically (sha unchanged, tree clean), so "writes only
`corpus/evidence/round80/` + the ledger" is measured for the ledger half and source-read for the receipt half.
Table size and write sites:

```
$ python3 -c "import json;d=json.load(open('plans/round80_probes.json'));print(len(d['members']), sorted(d['members']))"
6 ['cancel-async-tasks', 'chess-best-move', 'distribution-search', 'largest-eigenval', 'openssl-selfsigned-cert', 'protein-assembly']
$ grep -n "EVID\|LEDGER\|write_text" plans/round80_c1_remint.py
32:LEDGER = "plans/grader-population-ledger.json"
33:EVID = "corpus/evidence/round80"
178:    (lane / EVID).mkdir(parents=True, exist_ok=True)
180:        (lane / f"{EVID}/{m}-probe.txt").write_text(text)
181:    (lane / LEDGER).write_text(json.dumps(doc, indent=1) + "\n")
```

### 4.5 Exclusion evidence

```
$ B=a3a03ac31451e58f1742b9bccb73b72c2d90a95c
$ git show $B:plans/fixture_fence.py | grep -c argparse ; git show $B:plans/fixture_fence.py | grep -c __main__
0
0
$ git show $B:plans/policy_cases.py | grep -c argparse ; git show $B:plans/policy_cases.py | grep -c __main__
0
0
$ git show $B:plans/policy_cases.py | grep -n "^import \|^from " || echo "(none)"
(none)

$ python3 - <<'EOF'   # ast over BASE bytes
plans/fixture_fence.py: ast.parse=ok lines=991 imports=['os','pathlib','re','stat'] __main__blocks=[]
  top-level: constants + _-prefixed helpers, one public def breach(d, argv, tool) at :918
plans/policy_cases.py: ast.parse=ok lines=85 imports=[] __main__blocks=[]
  top-level names: ['CASES']
EOF

$ PYTHONDONTWRITEBYTECODE=1 python3 -c "import sys;sys.path.insert(0,'plans');import policy_cases as p;print(len(p.CASES))"
59
$ git show $B:plans/parser_policy_compare.py | sed -n '29,32p'
sys.path.insert(0, str(Path(__file__).resolve().parent))
import grader_perturb as gp  # noqa: E402
import policy_cases  # noqa: E402  hand-expected bounded synthetic cases
from attrib_calibration import clopper_pearson  # noqa: E402

$ for f in plans/round45_c1_verify.py plans/round46_c1_verify.py plans/round50_c1_verify.py plans/honest50/build_honest_population.py; do
    git show $B:$f | grep -n "fixture_fence\|spec_from_file_location\|FENCE_REL" ; done
plans/round45_c1_verify.py: 62 FENCE_REL = "plans/fixture_fence.py" · 110 spec_from_file_location("fixture_fence_under_test", sys.argv[1]) · 263-268 copies its bytes into the sandbox
plans/round46_c1_verify.py: 118 FENCE_REL · 217 spec_from_file_location · 489 fence under test defaults to lane/FENCE_REL
plans/round50_c1_verify.py:  74 FENCE_REL · 116 spec_from_file_location("fence_under_test", ...) · 203 --fence · 208-212 default lane/FENCE_REL
plans/honest50/build_honest_population.py: 68 FENCE_REL · 385-399 sha256 guard against BASE_FENCE_SHA
```

---

## 4.6 Row-shape self-check (the frozen row-quality rule, measured on the drafted bytes)

```
$ python3 - <<'EOF'   # parse the four rows out of this report, count cells, resolve entry + selftest flags
log-appendonly: cells=8 kind=gate entry_exists=True entry_parses=True
   selftest flags=['--selftest'] all_in_source=True
   pinned_not_na=True write_not_na=True verdict0=True verdict1=True nonempty=True
round37-c1-attribution: cells=8 kind=gate entry_exists=True entry_parses=True
   selftest: none declared (literal)
   pinned_not_na=True write_not_na=True verdict0=True verdict1=True nonempty=True
round66-registry-check: cells=8 kind=gate entry_exists=True entry_parses=True
   selftest flags=['--selftest', '--work'] all_in_source=True
   pinned_not_na=True write_not_na=True verdict0=True verdict1=True nonempty=True
round80-c1-remint: cells=8 kind=probe entry_exists=True entry_parses=True
   selftest: none declared (literal)
   pinned_not_na=True write_not_na=True verdict0=True verdict1=False nonempty=True
EOF
```

(`verdict1=False` on the probe row is the rule, not a miss: a `probe` row's map must declare `0`; this one
declares `0`/`2`/`3` because that is what the script returns.)

---

## 5. Findings

**F1 — `log-appendonly` is RED at the tip, and the newest violation is a round-78 in-place LOG rewrite by
`3cc5cecb`.** The gate's measured tip state is `commits=141 violations=9`, exit 1. This is not a defect of the
row; it is the tool doing its job. The ninth violation is the commit that landed 2026-11-04 03:12:43,
`round-78: round-78 receipts re-produced by the final counters (…); SCORECARD/LOG/lesson before values
re-stated under the final rule`, whose diff rewrites two already-committed LOG lines
(`@@ -2989,4 +2989,4 @@`, the R78-C2 before-values `receipts=16 located=3 unlocated=13 / DEFECTS n=27` →
`located=2 unlocated=14 / DEFECTS n=29`). The L1 must paste the row with the red recorded, not laundered: the
claim's row-quality rule only requires the map to declare `0` and `1`, not that the gate be green.

**F2 — `round66-registry-check` is GREEN on `quote` and RED on `meta` at the tip.** `meta corpus/SOURCES.md`
prints three findings, all on the *superseded* row S234 (`corpus/SOURCES.md:250`), which still carries all
three frozen meta phrases; `rows=253 findings=3`, exit 1. The row's entry cell therefore names both
subcommands and the `1` leg carries the measurement — a reader must not infer that `meta` is clean. A
sub-selection (`S236 S237`) is green, so the red is row-attributed.

**F3 — the item's "receipts only" write scope for `round80-c1-remint` is contradicted by its bytes.** The
driver writes `corpus/evidence/round80/<member>-probe.txt` (`:180`) **and** rewrites
`plans/grader-population-ledger.json` (`:181`) — unconditionally, even when no member is selected (measured:
`--only no-such-member` still rewrote the ledger, byte-identically). The registry cell names both paths so it
is true. This is the one place where this report overrides the seat item's parenthetical, on byte evidence.

**F4 — `--only <unknown>` exits 0.** `REMINT minted=0 failed=0`, exit 0: an empty selection is indistinguishable
from a complete one on the exit code (`:183` compares `len(staged)` to `len(chosen)`). Recorded as a limit of
the `0` cell in the row's verdict map ("every *selected* receipt"), not as a defect — the driver is not a
predicate gate.

**F5 — `round37-c1-attribution` has no `--selftest` and no `--work`-free mode.** Its `1` leg (a surviving
mutant) is source-read only (`:83`), and its own red evidence lives outside the script
(`SCORECARD.md:1301-1304`: landed `ATTRIBUTED 55/55`, hostile battery `ATTRIBUTED 6/55 UNATTRIBUTED=49` in
`.ufo/waves/round-37/integrate/c1-attribution-hostile.txt`). The self-test cell says `none declared` rather than
naming a flag that does not exist.

**F6 — both excluded modules are libraries, not CLIs.** Each has zero `argparse` and zero `__main__` at BASE,
and every consumer loads them by path or by `import` (no `python3 plans/<module>.py` invocation exists in the
lane's counters). `fixture_fence.py`'s only public entry is `breach`; `policy_cases.py` exports a single
`CASES` tuple.

---

## 6. What I attacked, and what I could not break

- Attacked the exclusion claim from both directions: token counts (`grep -c`) and an AST walk over BASE bytes.
  Both say the modules cannot be run as CLIs; I could not produce a CLI surface for either, so `support-module`
  holds and both must stay out of the registry.
- Attacked the `log-appendonly` `0` leg: `--selftest`'s GREEN fixture is a pure append (`commits=2
  violations=0`, rc 0) while RED-MOVE (a reordering) still counts as a rewrite — the tool is not satisfied by
  "the file still contains the line", which is the failure mode an append-only claim usually hides.
- Attacked the `round66 quote` refusal legs through the selftest: a capture outside `corpus/evidence/`, an
  absolute capture path, a lesson with no `## Gate` and an empty Gate are all findings (rc 1), so an empty
  input cannot pass vacuously.
- Attacked `round80-c1-remint`'s guard: a one-line dirty tree is refused before any run (`SETUP worktree not
  clean (1 paths)`, rc 2) and leaves the tree as it found it.
- Could not break: the four scripts' entry cells (all four parse at BASE and at the tip, no `BASE..tip` diff);
  the exclusion byte rule; the two tip-red states (F1, F2) are real measurements, not artifacts of the clone.

---

## 7. `UNVERIFIED` (named, not invented)

1. `round80-c1-remint`'s full six-member mint run (`exit 0` with `minted=6`) — **UNVERIFIED** by design: it
   writes receipts and rewrites the ledger, and the seat item forbids running it against the lane; the clone
   run would mutate the clone's ledger and receipts. Only the no-op selection reached the write block.
2. `round80-c1-remint`'s `3` leg (`REMINT-FAIL …`) — **UNVERIFIED**; no failing probe was induced (source:
   `:107,:111,:116,:162`).
3. `round37-c1-attribution`'s `1` leg (an `UNATTRIBUTED` mutant) — **UNVERIFIED**; producing one would require
   a fixture battery the script does not expose as a control (source: `:80,:83`).
4. `log-appendonly`'s `--verbose` `WALK` reconciliation line — **UNVERIFIED** (not run; flag existence is from
   `--help`, the line format from `plans/log_appendonly.py:155-157`).

Everything else in §1/§2 is backed by a command and its output in §4.

---

## 8. Return

- **Behavior delivered:** four paste-ready registry rows (eight non-empty cells each, kinds `gate`/`probe`,
  entries existing at BASE and `ast.parse`-clean, flags in the self-test cells occurring in the named scripts,
  pinned-values and write-scope cells non-empty) and two `support-module` EXCLUSIONS entries with BASE byte
  evidence and their importers, plus the forward-direction note.
- **Gates exercised:** `log-appendonly` (0/1/2 legs), `round37-c1-attribution` (0 and 2), `round66-registry-check`
  (0/1/2 and selftest 13/13), `round80-c1-remint` (`--help`, dirty-tree refusal, no-op exit 0).
- **Touched surfaces:** this report only, `.ufo/waves/round-82/w1/RegistryRowsR82.md`; scratch
  `/fast/scratch/hyaku/kengaku-r82/RegistryRowsR82/` (one `--shared` clone + fixture dirs, deleted before
  yield). No lane file other than this report was written, no commit/push/jj mutation was run, no counter was
  trusted over its bytes.
- **Out of scope (left to L1/other seats):** editing `SKILL.md`/`corpus/SOURCES.md` (F2's red is a landing
  decision, not this seat's edit), the counter `plans/round82_c1_plans_registry.py` itself, and any repair of
  the nine `log-appendonly` violations (F1) or of S234's meta phrases.
- **Tooling:** nothing installed or upgraded (no pacman transaction; the host-wide pacman pause is respected;
  no `uv tool`/`npm`/binary install was needed).
- **Artifact path:** `.ufo/waves/round-82/w1/RegistryRowsR82.md` (this file).
