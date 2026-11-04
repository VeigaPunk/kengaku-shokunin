# Round 75 — non-author verifier spot-check (closure)

author: hyaku closure (non-author integrator, @m_zfl)
lane: kengaku · lane-round 75 · base `4c4249a26a01aeb081915755076f74a7d6c88923` → tip
`5d9a0cccce42c6bd876a61622c27f06280cf2f9d`
report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-75/kengaku.md` (fleet commits
`c3d320ace239aadbb8bb60c27753a78c8709e7bb` + `aa5ebcd6e07764efda69d2bdf7f5e57669283cce`, author
`kengaku-shokunin <kengaku@shokunin.local>`)
watchdog digest (mutable `.ufo/watchdog.log`, copied at closure):
`2026-11-04T01:15:03-03:00 launch kengaku round=75 pgid=1837233 driver=hyaku-inline attempt=1` ·
`2026-11-04T01:40:15-03:00 complete kengaku round=75; hyaku-inline attempt=1`

I did not author this round. Numbers below were re-derived from committed bytes with plain
measurement (git/grep/awk/independent parse); the lane's gates and selftests were checked by their
committed receipts and code, never executed (PROTOCOL §Gate standard, Closure consequence).

## 1. Step-1 conformance

| check | command / observation | result |
|---|---|---|
| report authored by the lane identity | `git log --format='%an <%ae> %H' -- .ufo/reports/round-75/kengaku.md` → `kengaku-shokunin <kengaku@shokunin.local> c3d320ac…`, `… aa5ebcd6…`; both in fleet `origin/master` | pass |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` → 1; four `[~]` lines, one per `SHONEN.md` box, each with a pointer; no `[x]` written | pass |
| cited commits exist and are ancestors | `git merge-base --is-ancestor <h> master` for `4c4249a2`, `e462a649`, `43255758`, `08148cc4`, `66a93f6b`, `813b7403`, `9f8f0f21`, `b64203cf`, `5d9a0ccc` → all ancestor; `git ls-remote origin refs/heads/master` → `5d9a0ccc…` | pass |
| lane clean / pushed | `jj-lane.sh state` → `branch=master local=5d9a0ccc remote=5d9a0ccc ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty | pass |
| prompt carries the template contract | rendered `templates/round-prompt.md` (lane/round/fleet-root/axes substituted) vs `.ufo/prompts/kengaku-round-75.md` §1–§5: 140/140 lines identical except the working-dir placeholder resolving to `/home/…/kengaku-shokunin`; §6 hyaku addendum present; all five child-lane items present (report path, commit-then-push, `SHONEN` heading, hash-citation rule, push/write scope) | pass |
| report order | first report commit `c3d320ac` (01:38:47) cites landing tip `b64203cf`; the final lane commit `5d9a0ccc` lands 01:39:16; `aa5ebcd6` (01:39:36) rewrites the filed bytes to cite it | **defect, status-neutral** (R75-D1) |
| wave shape | `w1-validate.rc` → `rc=0`; one v1 wave, 13 seats (executor 3, scribe 3, reviewer 3, critic 1, mutation-tester 1, scout 1, connector 1); attack 5/13 = 38.5 %; connector 1; `w1-results.json` 13 results, 0 empty; 13 named seat reports + 3 scribe fragments under `.ufo/waves/round-75/w1/` | pass |
| planner seat | L1 holds it; data-walk rides scout `SourcesHostR75` per `plans/round-75-claims.md` | pass (claims doc; report states it) |
| report sections | Work performed, Landed changes, Before → after, Sources & frontier, Trend verdicts, SHONEN — present and ordered; not a marker (real committed work, 9 hashes) | pass |

Conformance defects, all status-neutral: R75-D1 (report filed before its final lane commit and
rewritten in place), R75-D2 (after-revision drift), R75-D5 (LOG drift), R75-D7 (round-74 lesson
reflowed in place). None bars admission.

## 2. Per-claim re-check

### R75-C1 / coverage — verifies (re-measured at the landing tip)

Surfaces enumerated from committed bytes with `git ls-tree`; index membership parsed by my own
script (rendered lines only: HTML comments and fences stripped, cells split on unescaped pipes,
every cell non-empty, first cell exactly `` `kind/file` ``; evidence universe = 66 first-level
directories under `corpus/evidence/`):

```
$ python3 /tmp/idx2.py 43255758ed7d74ea05c8e03686dd9ad37837f0cd \
                       5d9a0cccce42c6bd876a61622c27f06280cf2f9d
== 43255758
UNIVERSE knowledge files=74 indexed=70 missing=4 orphan=0
UNIVERSE lessons files=123 indexed=87 missing=36 orphan=0
UNIVERSE evidence dirs=66 indexed=46 missing=20 orphan=0
total_missing= 60
== 5d9a0ccc
UNIVERSE knowledge files=74 indexed=74 missing=0 orphan=0
UNIVERSE lessons files=123 indexed=123 missing=0 orphan=0
UNIVERSE evidence dirs=66 indexed=66 missing=0 orphan=0
total_missing= 0
```

The script is reproducible from this block (stdlib only; reads `corpus/README.md` and the tree at
each argument revision from `git show`/`git ls-tree`):

```python
import re, subprocess, sys
lane="/home/vgpnk/Projects/shokunin/kengaku-shokunin"
def git(*a): return subprocess.run(["git","-C",lane,*a],capture_output=True,text=True).stdout
for rev in sys.argv[1:]:
    r=git("show",f"{rev}:corpus/README.md")
    r=re.sub(r"<!--.*?-->","",r,flags=re.S); r=re.sub(r"^```.*?^```","",r,flags=re.S|re.M)
    rows={"knowledge":set(),"lessons":set()}
    for line in r.splitlines():
        if not line.lstrip().startswith("|"): continue
        cells=[c.strip() for c in re.split(r"(?<!\\)\|",line.strip())[1:-1]]
        if len(cells)<2 or not all(cells): continue
        m=re.fullmatch(r"`(knowledge|lessons)/([^`]+)`",cells[0])
        if m: rows[m.group(1)].add(m.group(2))
    ev=set(re.findall(r"corpus/evidence/([A-Za-z0-9_.-]+)/",r))
    for kind,d in (("knowledge","corpus/knowledge"),("lessons","corpus/lessons")):
        files=sorted({p.rsplit("/",1)[1] for p in git("ls-tree","-r","--name-only",rev,d).splitlines() if p.endswith(".md") and p.count("/")==2})
        miss=[f for f in files if f not in rows[kind]]; orph=sorted(x for x in rows[kind] if x not in files)
        print(f"UNIVERSE {kind} files={len(files)} indexed={len(files)-len(miss)} missing={len(miss)} orphan={len(orph)}")
    dirs=sorted({p.split("/")[2] for p in git("ls-tree","-r","--name-only",rev,"corpus/evidence").splitlines() if p.count("/")>=3})
    miss=[d for d in dirs if d not in ev]; orph=sorted(m for m in ev if m not in dirs)
    print(f"UNIVERSE evidence dirs={len(dirs)} indexed={len(dirs)-len(miss)} missing={len(miss)} orphan={len(orph)}")
```

The after lines are exactly the frozen target lines, 0 orphans both directions, at the landing tip;
the claim's kill rule is not triggered. The before state differs from the committed receipt by one
surface: `c1-before.txt` prints `indexed=71 missing=3` because it was produced by the pre-A3 counter
(prefix regex over raw bytes) that accepted the malformed `tb2-distribution-search-grader` row; under
the final A3 rule that row has empty cells and is skipped, so the before is 60 (4/36/20), not 59.
The after state and the repair are unaffected; the cross-version comparison is routed (R75-D3).

Selftest/control evidence (not executed): `c1-selftest-after.txt` → `SELFTEST cases=8 red=7
failures=0 ok=True`; `c1-control-rowshuffle.txt` → `NAIVE rows=6 surfaces=6 equal=True` while four
`MISSING*` defects print; `c1-selftest.txt` (before) → `cases=5 red=4`. The battery grew across
A4/A5; the target never narrowed.

### R75-C2 / calibration — verifies (evidence-verified, never executed)

```
$ ls corpus/evidence/round75/*.txt | wc -l
15
$ for f in corpus/evidence/round75/*.txt; do sed -n 's/^LANE_TIP //p' "$f"; done | \
    while read -r t; do git cat-file -e "$t^{commit}" && git merge-base --is-ancestor "$t" master \
      && echo "anc $t"; done | sort | uniq -c
     15 anc <each stamp>          # all 15 resolve and are ancestors of master; all print WORKTREE clean
$ git ls-tree -r --name-only 43255758 -- corpus/evidence/round74 | grep -c '\.txt$'
11                              # none carries LANE_TIP at 43255758 (0 occurrences)
$ git show 4c4249a2:SKILL.md | <registry rows>  → 116 ; 5d9a0ccc → 118
```

`c2-stamp-red-before.txt` (before): `STAMPS files=11 stamped=0 unstamped=11 …`,
`PREDICATE R75-C2 fail`, rc 1 — independently confirmed (11 round-74 `*.txt`, 0 stamps at the base).
`c2-after.txt` (after, stamped `9f8f0f21`): `MISMATCH 0`, `DEFECTS n=0`, `FLAGS ok n=0`,
`INSTRUMENTS total=118 rows=118`, `MUTANTS real=10 expected_matched=10 wrong_id=0 survived=0
null_arms=1 null_survived=1 total=11`, `STAMPS files=15 stamped=15 unstamped=0 unresolved=0
not_ancestor=0`, `PREDICATE R75-C2 pass`. My own count confirms 15 receipts, 15 resolvable ancestor
stamps and 118 registry rows (base 116). The mutant/null tallies are gate-internal; they are
evidence-verified from the committed receipt and `c2-selftest-after.txt` (`arms=5 failures=0
ok=True`), never re-executed.

### Re-measured vs evidence-verified

- **Re-measured by me:** C1 after tallies at `5d9a0ccc` and before tallies at `43255758` (own parse),
  surface counts, 15/15 stamp resolution and ancestry, 11/11 unstamped round-74 receipts, registry
  rows 116 → 118, SOURCES 242 → 243, census validate, commit ancestry, SCORECARD/PROVINCE/SKILL/LOG
  diff scope, wave counts, prompt fidelity, live re-fetch of S251.
- **Evidence-verified, not executed:** both selftests' arm lists, the C2 mutant matrix and null arm,
  the attribution control, both before receipts' gate-internal lines, and the seat replays.

## 3. Axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | **improved** | C1's target re-derives at `5d9a0ccc` (74/74, 123/123, 66/66, 0 orphan; before 60 under the final rule); the gate's selftest has 8 arms with 7 red and the control keeps four defects visible. Score held at **7** by the open L0 cap. |
| calibration | **improved** | C2 now prices kills by expected finding id (`wrong_id=1` on the same bytes where the round-74 metric printed 10/10), measures a null arm, derives its tallies, and validates 15/15 ancestor stamps; the stamp leg re-derives red on round-74's 11 unstamped receipts. Score held at **10**, exercised. |
| depth | unchanged | S251 + lesson Gate/Mistakes; no admitted knowledge entry; score 10 held |
| operability | unchanged | two new in-repo gates with selftest + mutant receipts; score 10 held |
| freshness | unchanged | S251 re-fetched byte-identically; `~/archive/bench-arena` absent re-measured and dated in `PROVINCE.md`; score 10 held |
| adjacency | unchanged | sibling duplication named and routed out, not absorbed; no new arbitration; score 9 held |
| novelty | unchanged | instrument and index work, no new construct claimed; score 8 held |

No owned axis harmed: `git diff 4c4249a2 5d9a0ccc -- SCORECARD.md` is `58 0`, a single appended
round-75 section, every prior score row untouched; `PROVINCE.md` `21 0`, `SKILL.md` `2 0`, `LOG.md`
`33 0`. The whole lane diff is 52 files, +8626/−4; the four deletions are three rewritten README
rows (the malformed row + two `admission: hold` markers) and one reflowed line in
`corpus/lessons/round-74.md` (R75-D7), none of them content loss.

## 4. Discernment spot-check (LEARNING.md — from outside)

| item | lane decision | re-opened source | agree? | reason |
|---|---|---|---|---|
| S251 — Git `git-rev-parse` documentation | **admit**, tier A docs, scope revision-name resolution / `--verify` acceptance | live `https://git-scm.com/docs/git-rev-parse` re-fetched: HTTP 200, **122459 B**, sha256 `00e3b1aa…587` — byte-identical to `corpus/evidence/round75/sources/git-rev-parse.html`; quote starts capture line 2720, 18 words | **agree** | quote is verbatim (wrapped across two lines), located, ≤25 words; tier A fits official Git docs on their own scope; the row is `mined` and both `used-by` paths exist |
| “A 40-hex string in a receipt proves the receipt measured that revision” | **reject** (flip: stamp revision **and** worktree state, produce from a clean clone at that revision) | same page, `--verify` text: “Verify that exactly one parameter is provided, and that it can be turned into a raw 20-byte SHA-1…”; `git merge-base --is-ancestor` is a separate command | **agree** | `--verify` resolves an object id; it certifies neither the tree that produced the printed numbers nor measurement provenance. The flip is the correct repair and is what A1/A2 implement. |
| “Presence of a flag string in a script body proves `argparse` acceptance” (S250 flip) | **reject**, implemented as the C2 `:entry:flag-not-declared:` leg | `corpus/evidence/round74/sources/argparse-docs.html`, sha256 `ad9095cd…` (matches row), capture line 908: “The `add_argument()` method must know whether an optional argument… or a positional argument… is expected.” | **agree** | the declaration lives in `add_argument`; a string constant elsewhere proves neither registration nor acceptance. Round 75 executes the flip (positional `add_argument` only; `TEXT-FALLBACK` reported) instead of only recording it. |

Newly written SOURCES row: `corpus/SOURCES.md:267` S251 — 11 cells, quote 18 words, anchor
`capture …:2720, anchor --verify`, sha256 pinned and matching the live fetch; `used-by`
`corpus/lessons/round-75.md, plans/round-75-claims.md` both exist.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kengaku` → rc 0; `ok` line; 25 `W04` duplicate-URL warnings, the same
25 present in both committed census receipts; rows **242 → 243**
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`), malformed rows 0, tiers `A=213 B=24 C=6`
(213+24+6 = 243). Spot-check grades: admit agree, both rejects agree.

## 5. Trend verdicts

- **expansion: unchanged.** No `corpus/knowledge/` entry was admitted (four candidates stay held),
  no capability row entered `SCORECARD.md`, and the one new SOURCES row is `mined` against the lesson
  and claims doc, not a knowledge entry. The index repair is a quality/coverage move on existing
  surfaces, not new ground. (I do not adopt the report's `improved` here.)
- **quality: improved.** The attributed registry audit supersedes the round-74 any-defect metric on
  identical fixture bytes (`killed=10/10` → `expected_matched=9/10 wrong_id=1`), receipts carry a
  git-validated measured revision, and the index gate rejects both false greens the seats built
  (comment-only README; `.md`-named directory). No admitted entry failed a re-check; the stale
  round-74 lesson line is corrected (R75-D7 notes the reflow).
- **discernment: improved.** This outside spot-check agrees with the gate on the admit and on both
  rejects (§4); the round's own review seats falsified both claims with executable counterexamples
  and the fixes are in the counters, disclosed as amendments, not smoothed. No new `QUALITY.md`
  criterion was needed because Q1/Q46/Q49/Q50 already cover the classes.

## 6. Routed defects and operator note

- **R75-D1 (report ordering / filed bytes) — routed, conformance only.** The report's first commit
  `c3d320ac` (01:38:47) preceded the final lane commit `5d9a0ccc` (01:39:16) and cited `b64203cf`;
  `aa5ebcd6` then rewrote the filed bytes. Land the report only after the last lane commit, and
  correct by a new erratum commit naming the superseded text, never by rewriting filed bytes.
- **R75-D2 (revision drift) — routed.** `SCORECARD.md` round-75 row cites the after state at
  `813b7403`; the committed receipts (`c1-after.txt`, `c2-after.txt`) stamp `9f8f0f21`, and the
  report's prose claims a re-derivation at `5d9a0ccc` for which no receipt is committed. Append the
  actual receipt revision (or commit the tip receipt).
- **R75-D3 (before/after measured under different gate versions) — routed.** `c1-before.txt` was
  produced by the pre-A3 raw-prefix counter (`missing=3`); under the final rendered-row rule the
  before is 60 (4/36/20), not 59. The after state is verified either way. State the final-rule
  before count or name the instrument change so the two states are not compared across versions;
  `plans/round-75-claims.md`'s header still says 58 (A1 corrects to 59).
- **R75-D4 (registry drift) — routed.** `SKILL.md` rows `round75-c1-index-parity` (self-test “5
  arms, 4 red”) and `round75-c2-registry-audit` (“4 arms”; pass map `expected_matched=9`; “9
  attributed mutants + 1 null arm”) are stale after A4/A5: actual selftests are `cases=8 red=7` and
  `arms=5`, and the after receipt prints `real=10 expected_matched=10 … total=11`.
- **R75-D5 (LOG drift) — routed.** `LOG.md` round 75 says the C1 selftest is `cases=7 red=6` (actual
  8/7) and that “after receipts were generated from clean clones at `43255758` and `66a93f6b`”
  (the after receipts stamp `9f8f0f21`; only `census-after.txt` stamps `66a93f6b`). `LOG.md` is
  append-only — add a correction entry naming these lines.
- **R75-D6 (unbacked assertion) — routed.** The report asserts “Both round-74 gates stay green at
  the landing tip” with no committed receipt; either commit the two tip receipts or cite their
  exact paths. (Consistent with the R75 supersets, but not evidenced.)
- **R75-D7 (in-place lesson edit) — routed.** `corpus/lessons/round-74.md` was reflowed and had the
  correction appended inside the same bullet (`7 1`), while the report says “the round-74 text is
  not rewritten”. Append corrections as their own entries; do not reflow filed lesson bytes.
- **For the operator (promotion-owned, never closure):** all four `SHONEN` boxes remain `[~]`
  lane-asserted. Boxes 1–4 look fully checkable by a non-author now — the registry, the two round-75
  gates with selftest/control receipts, the LOG round entry, and an accurate `PROVINCE.md` (including
  the dated `bench-arena` absence) are all resolvable pointers.
