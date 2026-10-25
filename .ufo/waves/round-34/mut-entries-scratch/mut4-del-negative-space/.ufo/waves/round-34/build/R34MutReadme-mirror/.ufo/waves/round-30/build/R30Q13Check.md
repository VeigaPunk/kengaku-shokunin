# R30Q13Check — what the round-30 admitting commit must contain for Q13/Q14/Q15

Seat: `L1Kengaku30.R30Q13Check` (executor, leaf). Task: determine exactly what the round-30 admitting
commit must contain for `QUALITY.md` Q13/Q14/Q15 to pass, proven by a sandbox run that exits 0 plus a
red-before run that exits 1. No production edits: every write stayed in `/tmp/r30-Q13Check/` except this
report. No tool installs or upgrades were needed (python3/git already present; pacman untouched).

Access date for everything opened: 2026-10-25.

---

## 1. Answer

`plans/gate_timing_check.py` takes **no wave-registry argument**. It discovers the seat registry inside
the requested commit at the fixed path
`.ufo/waves/round-<N>/<second-wave-dir>/swarm-registry.json` (`plans/gate_timing_check.py:292`), where
`<second-wave-dir>` is `falsify` (case-insensitive) or anything matching `wave[-_ ]?0*2` —
`wave2`, `wave02`, `wave-2`, `wave-02`, `wave_2`, `wave_02`, `wave 2` (`:241-243`). The only
arguments are `--lesson`, `--commit`, `--repo`, `--selftest` (help text below, exit 0).

So the round-30 admitting commit must contain, **in its own tree**, four things:

1. `corpus/lessons/round-30.md` — a `## Gate` table whose header includes the cells `candidate`,
   `decision`, `reason`; one row with `decision` beginning `admit`; the `candidate` cell is the entry's
   repo path written with no version suffix; the `reason` cell names a second-seat report by path.
2. `.ufo/waves/round-30/falsify/<Seat>.md` — the cited report itself, mode `100644`, nonempty,
   containing the candidate path and an anchored `VERDICT:` line.
3. `.ufo/waves/round-30/falsify/swarm-registry.json` — in the **same** commit, mapping the report's
   filename stem to a role in `{reviewer, scout, critic, sentinel, revenger}`; this file is what makes the
   seat "registered". The lane's existing `.ufo/waves/round-30/build/swarm-registry.json` is invisible to
   the checker (proved red, M1/M2 below).
4. `corpus/knowledge/contamination-transparency-card.md` — the candidate, with a `writer:` line whose
   value is neither the cited report's filename stem, nor that seat's registry `agentId`, nor a
   `writer:`/`author:` declaration inside the report.

Nothing else is required: the checker does not read `LOG.md`, `SCORECARD.md`, the index, `yield.tsv`, or
any expect file. Q7 (index row) and Q6 (named extension) remain prose gates, not this check's input.

## 2. Checker contract, source-anchored

| Requirement | Mechanism | Anchor |
|---|---|---|
| `--repo` optional, defaults to the checker's parent repo | argparse | `:851-862` |
| Round inferred from path component `round-30.md`, else `# Round N` heading, else cited wave paths | `infer_round_number` | `:389-402` |
| Lesson must exist **in the commit**; otherwise INPUT ERROR exit 2 | `git show <commit>:<lesson>` | `:881-886` |
| Tree authority is the request commit, scoped to `.ufo/waves/round-30` | `git ls-tree -rl <commit> -- .ufo/waves/round-30` | `:893-897` |
| Gate section = heading matching `^Gate(\b\|[-:…])`, level-bounded | `parse_gate_admissions` | `:144-192` |
| Row audited only when `decision` matches `^admit(?:ted)?\b` (backticks/`*`/`_` stripped) | `is_admit` / `plain_cell` | `:136-141` |
| Header must contain candidate+decision+reason (extra columns allowed) | `{"candidate","decision","reason"}.issubset` | `:172` |
| Citation forms: full `.ufo/waves/round-N/<dir>/X.md`; relative `<dir>/X.md`; bare `X.md` if unique | `FULL_REPORT_RE`/`RELATIVE_REPORT_RE`/`BARE_REPORT_RE` | `:28-40`, `:202-231`, `:259-281` |
| Only second-wave dirs count; `build/` is dropped silently (no error, no credit) | `is_second_wave` | `:241-243`, `:277` |
| Registry path fixed at `.ufo/waves/round-N/<dir>/swarm-registry.json` | `load_members` | `:284-312` |
| Report must be `100644` and nonempty | mode/size guard | `:344-345` |
| Report stem must equal a registry member key (case-sensitive) | `members.get((dir, PurePosixPath(path).stem))` | `:336-346` |
| Role ∈ exactly 5 allowed values (Q14) | `ALLOWED_REPORT_ROLES` | `:24-26`, `:348-349` |
| Candidate must have a committed `writer:` and ctx: `writer` ≠ seat stem, ≠ seat `agentId`, ≠ report `writer:`/`author:` | identity ladder | `:55-57`, `:350-357` |
| Report must mention the candidate path and carry `^VERDICT:\s*\S` | `any(form in content …)` + `VERDICT_RE` | `:55-56`, `:358-361` |
| PASS = every admit row green, no generic refs, no unresolved bare refs | `ok = …` | `:376`, `:927-936` |

`python3 plans/gate_timing_check.py --help` → exit **0**:

```
usage: gate_timing_check.py [-h] [--lesson LESSON] [--commit COMMIT]
                            [--repo REPO] [--selftest]
...
  --repo REPO      repository containing the commit (default: this repository)
```

The lane's own `python3 plans/gate_timing_check.py --selftest` → exit **0**, tail:
`[selftest] ALL PASS (five allowed roles; connector/mutation-tester/simplifier and unknown roles rejected;
declared writer/author/agentId conflicts red; worktree/parser/run_git mutants red; caller index and fresh
bare victim unchanged)`. That selftest (not my mutants) is the evidence for symlink/empty-file/`INDEX.md`
rejection; my matrix below does not re-run those three.

## 3. Proven fixture set (byte-exact, green at sandbox commit `126145a`)

Sandbox: `git clone --no-hardlinks …/kengaku-shokunin /tmp/r30-Q13Check/repo` (exit 0). The checker
used is the clone's copy, `sha256 51c18a9edfecba9cb6e15449b8063668f41225e98347c6221c6df7c2b0b80a2a`, byte-identical
to the lane's `plans/gate_timing_check.py` (same sha256, verified).

**`corpus/lessons/round-30.md`** (`sha256 32bea7d9ba89595a3580131c15815dd9a972f400bfef93d9fec4099faa274d2f`)

```markdown
# Round 30 — shokuknow assimilation, contamination transparency

Baseline: lane branch tip at freeze. Waves: `build` (v1) then `falsify` (v1).

## Gate

| candidate | decision | reason | flip condition |
|---|---|---|---|
| `knowledge/contamination-transparency-card.md` | admit | Q1–Q9 self-check by the writer; Q10 second-seat re-read returned at `.ufo/waves/round-30/falsify/FR30ReReadSources.md`, whose seat is not the entry writer. | a cited quote that the second seat cannot re-find in its own fetch |
| a fourth rival card design | reject | This entry is an amendment to the tabulated designs, not a new design; round 29 rejected the rival framing on scope. | a separately tabulated design with its own Q1–Q8 gate |

## Sources opened this round

Access date 2026-10-25 for every row. Quotes are ≤25 whitespace words.
```

**`corpus/knowledge/contamination-transparency-card.md`** (`sha256 288a4ef983ae2c37511f341fa7757c28fa8a55ef083b725545e6aa5607a48cf6`)

```
source: S081 — https://example.invalid/a — §1; S082 — https://example.invalid/b — Abstract
verified-at: 2026-10-25
recheck: 2027-01-23 (90d) — re-open the six URLs and re-verify each quoted sentence
writer: KengakuR30

# Contamination transparency card — an amendment to the tabulated designs

## What this adds

Amends the existing contamination-detection entry: the card is a reporting
instrument for what a provider discloses, not a new detector.
```

**`.ufo/waves/round-30/falsify/swarm-registry.json`** (`sha256 a65922ebfed15b6965cfa46f541b9c5e3102680b44724e6b7f4f8884294cac4e`)

```json
{
  "schema": "ufo-swarm-registry-v1",
  "wave": "kengaku-r30-falsify",
  "createdAt": "2026-10-25T09:00:00.000Z",
  "updatedAt": "2026-10-25T09:00:00.000Z",
  "reportDir": ".ufo/waves/round-30/falsify",
  "members": {
    "FR30ReReadSources": {
      "kind": "spawn",
      "agentId": "KengakuR30.FR30ReReadSources",
      "role": "reviewer",
      "item": null,
      "axes": ["calibration"],
      "milestone": "Re-ground and admit the contamination-transparency amendment"
    }
  }
}
```

**`.ufo/waves/round-30/falsify/FR30ReReadSources.md`** (`sha256 7b72aaaa51bed252614b8c3a1310cd05eaf2825f3081ff496fe7116cbe3fd0c2`)

```markdown
# Q10 second-seat re-read — contamination transparency card

Seat: FR30ReReadSources (reviewer, registered in
`.ufo/waves/round-30/falsify/swarm-registry.json`)

Candidate re-read: `corpus/knowledge/contamination-transparency-card.md`

Every cited quote was re-fetched on 2026-10-25 and located byte-for-byte in my
own copy; every count cell was recomputed. Findings: none open.

VERDICT: PASS
```

Mode/size as committed (`git ls-tree -r 126145a`):

```
100644 blob acc2faa75280115377ce49a0d2d4f86561c8001a	.ufo/waves/round-30/falsify/FR30ReReadSources.md
100644 blob 9a850ddfa9daa6192a5cd93ae8fa92288a59c208	.ufo/waves/round-30/falsify/swarm-registry.json
100644 blob e6469f8fe7ef6f29db1f83b1d41c8e8683942029	corpus/knowledge/contamination-transparency-card.md
100644 blob d3a319ad4cb6a25da1723ec0100d1c2999f912ec	corpus/lessons/round-30.md
```

## 4. Commands and exit codes

```sh
# 0. sandbox
cp -a /home/vgpnk/Projects/shokunin/kengaku-shokunin /tmp/r30-Q13Check/repo   # (git clone used) -> 0
python3 plans/gate_timing_check.py --help                                      # -> 0

# 1. early commit: lesson + entry + falsify registry, NO report
git add corpus/lessons/round-30.md corpus/knowledge/contamination-transparency-card.md \
        .ufo/waves/round-30/falsify/swarm-registry.json
git commit -q -m "sandbox: lesson + candidate + falsify registry, no second-seat report"
#    -> 756f499717385f3934fa672323db9e0fc7e62c4f
python3 plans/gate_timing_check.py --lesson corpus/lessons/round-30.md \
        --commit 756f499 --repo /tmp/r30-Q13Check/repo                          # -> EXIT=1

# 2. report written to the working tree only, still at the same commit
python3 plans/gate_timing_check.py --lesson corpus/lessons/round-30.md \
        --commit 756f499 --repo /tmp/r30-Q13Check/repo                          # -> EXIT=1

# 3. commit the report; lesson bytes unchanged
git add .ufo/waves/round-30/falsify/FR30ReReadSources.md
git commit -q -m "sandbox: commit the cited second-seat report"
#    -> 126145a82aedc8faa9cc626389405509f0548e82
git diff --stat 756f499 126145a -- corpus/lessons/round-30.md                   # empty (identical lesson bytes)
python3 plans/gate_timing_check.py --lesson corpus/lessons/round-30.md \
        --commit 126145a --repo /tmp/r30-Q13Check/repo                          # -> EXIT=0
```

### Red-before, variant A — no report anywhere (exit 1)

```
FAIL line 9 Gate admit: candidate='knowledge/contamination-transparency-card.md'
  cell[reason]: Q1–Q9 self-check by the writer; Q10 second-seat re-read returned at `.ufo/waves/round-30/falsify/FR30ReReadSources.md`, whose seat is not the entry writer.
  cited seat-report paths: '.ufo/waves/round-30/falsify/FR30ReReadSources.md'
  invalid cited second-seat report: .ufo/waves/round-30/falsify/FR30ReReadSources.md (absent from commit tree)
  missing: no .ufo/waves/round-30/falsify/ report exists in commit 756f499
  reasons: no cited, existing, returned second-seat report for this round; one or more cited second-seat reports fail identity/return checks
gate_timing_check: commit=756f499 lesson=corpus/lessons/round-30.md admissions=1 passed=0 failed=1 second-seat-reports=0
EXIT=1
```

### Red-before, variant B — valid report on disk but uncommitted (exit 1, Q15 timing)

`git status --porcelain -- .ufo/waves/round-30/falsify` → `?? .ufo/waves/round-30/falsify/FR30ReReadSources.md`

```
FAIL line 9 Gate admit: candidate='knowledge/contamination-transparency-card.md'
  cell[reason]: Q1–Q9 self-check by the writer; Q10 second-seat re-read returned at `.ufo/waves/round-30/falsify/FR30ReReadSources.md`, whose seat is not the entry writer.
  cited seat-report paths: '.ufo/waves/round-30/falsify/FR30ReReadSources.md'
  invalid cited second-seat report: .ufo/waves/round-30/falsify/FR30ReReadSources.md (absent from commit tree)
  missing: no .ufo/waves/round-30/falsify/ report exists in commit 756f499
  reasons: no cited, existing, returned second-seat report for this round; one or more cited second-seat reports fail identity/return checks
gate_timing_check: commit=756f499 lesson=corpus/lessons/round-30.md admissions=1 passed=0 failed=1 second-seat-reports=0
EXIT=1
```

### Green (exit 0)

```
PASS line 9 Gate admit: candidate='knowledge/contamination-transparency-card.md'
  cited seat-report paths: '.ufo/waves/round-30/falsify/FR30ReReadSources.md'
  existing returned second-seat report(s): .ufo/waves/round-30/falsify/FR30ReReadSources.md
gate_timing_check: commit=126145a82aedc8faa9cc626389405509f0548e82 lesson=corpus/lessons/round-30.md admissions=1 passed=1 failed=0 second-seat-reports=1
EXIT=0
```

## 5. Mutant matrix (each one mutation from the green commit; preserved as branches `mut-M*`)

| # | mutation | exit | decisive line |
|---|---|---|---|
| M1 | registry moved to `build/swarm-registry.json` | **1** | `(seat is not in the committed wave registry)` |
| M2 | report committed under `build/R30RevEntryQ1Q6.md` and cited by that path | **1** | `missing: Gate does not name a valid second-seat report by path; the commit has 1 second-seat report(s)` — no `invalid` entry: `build/` citations are dropped silently |
| M3 | report declares `writer: KengakuR30` (= entry writer) | **1** | `(report writer/author declaration equals candidate writer 'KengakuR30')` |
| M4 | report without a `VERDICT:` line | **1** | `(report has no anchored VERDICT line; return is not established)` |
| M5 | Gate cell says `Q10 verified by wave-2 seats.` | **1** | `generic seat reference(s) (not report support): 'wave-2 seats'` |
| M6 | entry without `writer:` | **1** | `(candidate has no committed writer: field; self-review cannot be excluded)` |
| M7 | citation rewritten as `falsify/FR30ReReadSources.md` | **0** | PASS (relative form accepted) |
| M8 | citation rewritten as `FR30ReReadSources.md` | **0** | PASS (bare unique form accepted) |
| M9 | registry `agentId: KengakuR30` (= entry writer) | **1** | `(registry agentId equals the candidate writer 'KengakuR30')` |
| M10 | candidate cell `knowledge/…-card.md v1` | **1** | `reasons: admitted candidate is absent from the commit tree; …` |
| M11 | report mentions only `knowledge/contamination-transparency-card.md` | **0** | PASS (either the cell form or the resolved `corpus/…` form works) |
| M12 | second `admit` row supported by `wave-2 seats` | **1** | `admissions=2 passed=1 failed=1` — one bad admit row reds the whole run |
| M13 | report renamed `fr30rereadsources.md` (case) with the lesson updated | **1** | `(seat is not in the committed wave registry)` — stem must equal the registry key byte-for-byte |
| M14 | same structure under `wave-02/` instead of `falsify/` | **0** | PASS (second-wave dir aliases accepted) |
| M15 | `--lesson corpus/lessons/round-30.md --commit 363a4eb` (lesson not in that commit) | **2** | `INPUT ERROR: cannot read corpus/lessons/round-30.md at 363a4eb: fatal: path … exists on disk, but not in '363a4eb'` |

## 6. The recipe to apply to the real admitting commit

Run from `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

1. Gate row (byte shape proven above; substitute only the seat name, which must equal both the report
   filename stem and a key in the falsify registry):

   ```
   | `knowledge/contamination-transparency-card.md` | admit | Q1–Q9 self-check by the writer; Q10 second-seat re-read returned at `.ufo/waves/round-30/falsify/<Seat>.md`, whose seat is not the entry writer. | <flip condition> |
   ```

   - `candidate` = `knowledge/<entry>.md` (or `corpus/knowledge/<entry>.md`); **no** ` vN` suffix.
   - `reason` = one or more `.ufo/waves/round-30/falsify/<Seat>.md` paths; any number is fine but every
     one must exist, be registered and be green (all-or-nothing).
   - Do not write `wave-2 seats`, `falsify seats`, `the rest of the falsify wave`, `second seats` — each is
     a generic-reference failure.
   - Only `admit`/`admitted` rows are audited: `reject`, `deferred`, `landed` rows may cite anything.

2. Report `.ufo/waves/round-30/falsify/<Seat>.md`, committed, mode 100644, nonempty. Required header
   fields (nothing else is structurally required):
   - a line containing the candidate path — `knowledge/contamination-transparency-card.md` or
     `corpus/knowledge/contamination-transparency-card.md`;
   - a line beginning exactly `VERDICT: ` followed by a non-space character (`VERDICT: PASS`);
   - either **no** `writer:`/`author:` line, or one naming a value ≠ the entry's writer.

3. `.ufo/waves/round-30/falsify/swarm-registry.json`, committed, `members.<Seat>.role` ∈
   `reviewer|scout|critic|sentinel|revenger`, `agentId` ≠ the entry's `writer:` value.

4. Entry gains exactly one new line, `writer: <id>` (line 4 convention, matching
   `corpus/knowledge/webarena-config-projection.md:4`), with `<id>` ∉ {report stem, that seat's `agentId`}.

5. Add all four in the same commit — `.ufo/waves/round-30/` is untracked at HEAD, so a plain
   `git commit -a` will not carry them:

   ```sh
   git add corpus/lessons/round-30.md corpus/knowledge/contamination-transparency-card.md \
           .ufo/waves/round-30/falsify
   git commit -m "round-30: admit the contamination-transparency amendment with its second-seat re-read"
   python3 plans/gate_timing_check.py --lesson corpus/lessons/round-30.md --commit HEAD   # exit 0
   ```

## 7. Findings the admitting commit must respect

- **`build/` cannot carry Q13 support.** The lane's existing `.ufo/waves/round-30/build/swarm-registry.json`
  already lists `reviewer` seats (`R30RevEntryQ1Q6`, `R30RevGate`, `R30RevCounter`, …), but citing
  `.ufo/waves/round-30/build/R30RevEntryQ1Q6.md` is silently worthless: exit 1, and M2 shows the checker
  does not even flag the path as invalid. A `falsify/` (or `wave-02/`) report + registry in the same
  commit is mandatory. That is a real deliverable the round-30 admitting commit must add; it is not
  satisfied by the build wave's own registry.
- **`.ufo/waves/round-30/` is untracked**: `git ls-tree -r --name-only HEAD -- .ufo/waves/round-30` → 0
  files, `git status --porcelain .ufo/waves/round-30` → `?? .ufo/waves/round-30/`. Any admitting commit
  that only touches tracked paths leaves `second-seat-reports=0` and fails.
- **Not a `.gitignore` problem**: `git check-ignore -v .ufo/waves/round-30/falsify/X.md` → exit 1 (no
  ignore rule); only `.ufo/interactive-sessions/` is ignored. `git add` suffices; no `-f` needed.
- **Allowed roles exclude the lane's executors and connectors.** Q14's five roles are enforced at `:348`;
  a `mutation-tester`, `connector`, `scribe`, `executor` or `simplifier` report fails identity even if
  perfectly written. Round-30's build registry has 36 members — 21 in allowed roles (10 scout, 7 reviewer,
  3 critic, 1 revenger) and 15 not (6 executor, 4 scribe, 2 connector, 2 mutation-tester, 1 simplifier) —
  and, being under `build/`, that file is never read by this check at all.
- **Identity is a three-way inequality**: entry `writer:` ≠ report stem ≠ that seat's `agentId`, and the
  report must not declare the writer either. With the lane's convention `writer: KengakuR30`, the falsify
  registry must use sub-seat ids as `agentId` (or `null`), never `KengakuR30`.
- **Every admit row must be green** (M12). If the round-30 Gate carries an `admit` row for something with
  no report (e.g. an adopted registry row, or the C2/C3 artifacts), the run goes red even though the card
  itself is properly supported. Use `reject`/`deferred` for those rows, or give them their own falsify
  report.
- **Exit codes are distinguishable**: `2` = input error (lesson absent from the commit, unreadable repo,
  `--lesson`/`--commit` missing); `1` = at least one admit row failed; `0` = all green. Because the
  lesson must already exist in the commit, the check can only pass on the admitting commit itself — a
  pre-commit run against an earlier sha is exit 2, not a green.

## 8. Risks / blockers for the accepting seat

- My green commit is a sandbox commit; its sha (`126145a`) is local to `/tmp/r30-Q13Check/repo` and must
  not be cited as lane evidence. The real receipt is the exit-0 run against the lane's admitting commit.
- I did not create the round-30 admission; the falsify wave (registry + reviewer/scout reports) is
  still a missing deliverable in the lane, and until it exists no admitting commit can pass this check.
- Q13 also asserts prose facts this checker does not decide (all cited findings resolved, report is a
  real re-read): presence ≠ endorsement. My evidence is structural only.
