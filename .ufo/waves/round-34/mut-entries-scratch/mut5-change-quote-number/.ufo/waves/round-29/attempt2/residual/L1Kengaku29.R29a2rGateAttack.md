# Round 29 attempt 2 — residual verification: attack the repaired gates

Seat: `L1Kengaku29.R29a2rGateAttack` (critic). Target tree `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
at `ff476d017107ec5ee3df735a16713c5967592b71`; both tools clean against HEAD
(`git status --porcelain plans/sources_adopt.py plans/adoption_check.py` → no output).
Scratch: `B=/tmp/r29a2r-gateattack`, `D=$B/d`. No repo writes besides this file; no installs.

Verdict: the four *repaired* defects hold on the intended path. Eight gaming paths survive; one of
them reproduces the frozen C1 target line from a round that opened nothing, with every command
exiting 0.

## 1. Repairs that hold (positive controls, observed)

| Repair | Command | Observed | Exit |
|---|---|---|---|
| 1-space-indented registry row collides (the proven false-green) | `python3 plans/sources_adopt.py --registry $D/reg_indent1.md --package $D/pkg_base.md --admit-ids S077 --scope-to-admit --entries corpus/knowledge/probe.md --access-date 2026-10-25 --out $D/out-d4.md` | `registry=1 staged=1 collisions=1 malformed=0 duplicates=0 defects=0 prose=0` / `  collisions: S077` | 3 |
| 4-space row is outside the census clause | `python3 plans/sources_adopt.py --registry $D/reg_empty.md --package $D/pkg_indent4.md --admit-ids S077 --scope-to-admit --entries corpus/knowledge/probe.md --access-date 2026-10-25 --out $D/out-g5.md` | `registry=0 staged=0 collisions=0 …` / `  missing: S077` | 5 |
| escaped pipe refused (case 5 is load-bearing: mutant drops the branch → `CASE escaped-pipe-refused FAIL`, exit 1) | `python3 $B/e/e4_escapepipe_disabled.py --selftest` | `SELFTEST cases=10 failed=1` / `  failed: escaped-pipe-refused` | 1 |
| `used-by` is an exact per-part match, not a substring | §3 rows C1/C2 | `usedby_ok=0` | 1 |
| staged duplicate id refused | `… --package $D/pkg_dup2.md --admit-ids S077 --scope-to-admit …` | `duplicates=1` / `  duplicates: S077` | 3 |
| frozen C1 target reproduced on the landed tree | `python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census` | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok` | 0 |
| C2 before-state | `git cat-file -e 1f3b0f1…:plans/sources_adopt.py` | `fatal: path 'plans/sources_adopt.py' exists on disk, but not in '1f3b0f1…'` | 128 |

`plans/adoption_check.py` raw line 93–96 is `rel in [part.strip() for part in registry[row_id][10].split(",")]`
— a first `read` rendering showed `rel in registry[row_id][10]`; the substring variant was then
tested and **failed**, so the committed exactness is real and the condensed rendering was not.

## 2. Attack rows

Legend: `B=/tmp/r29a2r-gateattack`, `D=$B/d`, run from the lane root.

| # | Attack | Command (exact) | Observed printed line | Exit | Gate caught? |
|---|---|---|---|---|---|
| a1 | Fabricated lane: entry body says no source was opened; registry rows keep `opened=2026-10-19`; `access_date=2026-10-25` | `python3 plans/adoption_check.py --lane $B/fx-a/kengaku-shokunin --expect $B/expect-a.json --census` | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok` | 0 | **NO** |
| a2 | Same, with the denial on the field the gate reads: `verified-at: 2026-10-25 (sources not re-opened this round; carried from the 2026-10-21 attempt)` | `python3 plans/adoption_check.py --lane $B/fx-a/kengaku-shokunin --expect $B/expect-a-parenthetical.json --census` | identical line | 0 | **NO** — regex is `^verified-at: <date>\b`, not end-anchored |
| a3 | Five ids on one `source:` line, four rows `queued`/`used-by=—`; expectation declares one id | `python3 plans/adoption_check.py --lane $B/fx-a3/kengaku-shokunin --expect $B/expect-a3.json --census` | `entries=1 indexed=1 cited_rows=1 rows_present=1 rows_mined=1 usedby_ok=1 census=ok` | 0 | **NO** — `SOURCE_LINE_RE` takes one id per line |
| a4 | Real lane, entry citing four ids on one line, expectation declares all four honestly (`agent-time-horizon-and-task-validity.md`) | `python3 plans/adoption_check.py --lane . --expect $B/expect-b-honest.json --census` | `entries=1 indexed=1 cited_rows=1 rows_present=1 rows_mined=1 usedby_ok=1 census=ok` (byte-identical to b1's pass line) | 1 | Yes, but only via exit code: the line carries no `required`, so `cited_rows=1` reads as 1-of-1 |
| b1 | Swapped `adoption-expect.json` naming an already-admitted round-24 entry (`agent-time-horizon-and-task-validity.md`, `verified-at: 2026-10-19`, zero new bytes) | `python3 plans/adoption_check.py --lane . --expect $B/expect-b-swapped.json --census` | `entries=1 indexed=1 cited_rows=1 rows_present=1 rows_mined=1 usedby_ok=1 census=ok` | 0 | **NO** — `round`/`attempt` are never read (`grep -n 'round\|attempt' plans/adoption_check.py` → docstring lines 2/4/6/10 only); five other pre-existing entries satisfy it the same way (S037, S007, S001, S009, S015) |
| c1 | Entry cites existing ids; `used-by` names a different existing entry (`corpus/knowledge/llm-judge-calibration.md`) | `python3 plans/adoption_check.py --lane $B/fx-c2/kengaku-shokunin --expect $B/expect-c2.json --census` | `… usedby_ok=0 census=ok` | 1 | Yes |
| c2 | `used-by` names a sibling lane's file whose path *contains* the entry path (`kasegi-shokunin/corpus/knowledge/…checklist.md`, file present on disk) | `python3 plans/adoption_check.py --lane $B/fx-c/kengaku-shokunin --expect $B/expect-c.json --census` | `… usedby_ok=0 census=ok` | 1 | Yes (exact-part match kills the substring false-green) |
| d1 | Assigned form: staged row duplicates a registry id, requested with `--scope-to-admit` | `python3 plans/sources_adopt.py --registry $D/reg_clean.md --package $D/pkg_base.md --admit-ids S077 --scope-to-admit --entries corpus/knowledge/probe.md --access-date 2026-10-25 --out $D/out-d1.md` | `registry=1 staged=1 collisions=1 …` / `  collisions: S077` | 3 | Yes |
| d2 | Duplicate in the *request* (`--admit-ids S077,S077`), staged once, registry empty | `python3 plans/sources_adopt.py --registry $D/reg_empty.md --package $D/pkg_base.md --admit-ids S077,S077 --entries corpus/knowledge/probe.md --access-date 2026-10-25 --out $D/out-d2.md` | `registry=0 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0` / `wrote … rows=2` | 0 | **NO** — `duplicate_ids` runs on staged ids only; the block holds S077 twice, and `sources-census.sh validate --file` on those bytes prints `file	E03	S077 duplicate id` (exit 1) |
| d3 | Registry row that fails the 11-cell parse is invisible to collision detection | `python3 plans/sources_adopt.py --registry $D/reg_malformed12.md --package $D/pkg_base.md --admit-ids S077 --scope-to-admit … --out $D/out-d5.md` | `registry=0 staged=1 collisions=0 …` / `wrote … rows=1` | 0 | **NO** (latent: `parse_rows(registry_text)` drops `bad`, so a malformed live row cannot collide; live `corpus/SOURCES.md` is E01-clean at this commit) |
| d4 | Scoped report suppresses a colliding row the package does carry | `python3 plans/sources_adopt.py --registry $D/reg_clean.md --package $D/pkg_collide_plus_clean.md --admit-ids S008 --scope-to-admit …` vs unscoped | `collisions=0 …` (scoped) vs `collisions=1` (same package, unscoped) | 0 / 3 | Refusal is correct per the documented scope; the printed count is post-filter and misstates the package |
| e1 | Selftest green with capability 2's status clause removed (`row_defects`) | `python3 $B/e/e1_status_disabled.py --selftest` then `… --package $D/pkg_bogus.md --admit-ids S077 --scope-to-admit …` | `SELFTEST cases=10 failed=0` (exit 0); CLI `wrote … rows=1`, emitted `status=mined` where committed refuses `defect S077: status=provisional` (4) | 0 | **NO** — all ten cases stage `status=mined` |
| e2 | Selftest green with the `--entries` guarantee removed from `main` | `python3 $B/e/e2_entries_guard_disabled.py --selftest` then the same CLI without `--entries` | `SELFTEST cases=10 failed=0`; CLI `wrote … rows=1`, used-by cell `—` where committed exits 2 | 0 | **NO** — the selftest never calls `main()` |
| e3 | Selftest green with capability 4's refusal removed (`if code != EXIT_OK` → `if not want`) | `python3 $B/e/e3_refusal_gate_disabled.py --selftest` then colliding append request | `SELFTEST cases=10 failed=0`; CLI prints `collisions=1` / `  collisions: S077` and then `wrote … rows=1` | 0 | **NO** — the mutant appends the colliding row while printing the collision |
| e4 | Control: same mutation class on the escaped-pipe branch | `python3 $B/e/e4_escapepipe_disabled.py --selftest` | `SELFTEST cases=10 failed=1` | 1 | Yes (case 5 is a control) |
| e5 | Control: recheck validation removed | `python3 $B/e/e5_recheck_disabled.py --selftest` | `SELFTEST cases=10 failed=1` / `  failed: missing-requested-id` | 1 | Yes |
| f1 | Status laundering: staged `status=rejected`, requested, registry empty | `python3 plans/sources_adopt.py --registry $D/reg_empty.md --package $D/pkg_rejected.md --admit-ids S077 --scope-to-admit --entries corpus/knowledge/probe.md --access-date 2026-10-25 --out $D/out-f1.md` | `defects=0` / `wrote … rows=1`; emitted cell is `mined` | 0 | **NO** — `build_block` forces `cells[7]="mined"` for any valid status |
| f2 | Same with `status=queued` | `… --package $D/pkg_queued.md … --out $D/out-f2.md` | `wrote … rows=1`; emitted `mined` | 0 | **NO** |
| g1 | `--entries` names a path that does not exist (capability 3: "a row naming an unadmitted entry never reaches the block") | `… --entries corpus/knowledge/never-admitted-anywhere.md --out $D/out-g1.md` | `wrote … rows=1`; used-by `corpus/knowledge/never-admitted-anywhere.md` | 0 | **NO** — the admitted set is caller-asserted; census later prints `E11 S077 missing used-by corpus/knowledge/never-admitted-anywhere.md` |
| g2 | `--access-date 2026-13-40` (not ISO) | `… --access-date 2026-13-40 --out $D/out-g2.md` | `wrote … rows=1`; opened cell `2026-13-40` | 0 | **NO** — census later `E08 S077 opened=2026-13-40` |
| g3 | `--recheck "next release"` on a prose-recheck row | `… --package $D/pkg_prose.md --recheck "next release" --out $D/out-g3.md` | `prose=1` / `  normalized recheck S077: 2026-10-23 — re-verify at next release` / `wrote … rows=1`; recheck cell `next release` | 0 | **NO** — the tool emits a cell its own `row_defects` would reject; `sources-census.sh validate --file` on those bytes prints `file	ok` (census is lenient here too, so a prose cadence enters the registry) |
| h1 | Two entries citing one shared source id (legitimate) | `python3 plans/adoption_check.py --lane $B/fx-a/kengaku-shokunin --expect $B/expect-a-shared.json --census` | `entries=2 indexed=2 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok` | 1 | False red: `cited` is a set union while `required` is a per-entry sum, so honest shared sourcing cannot pass — which pushes authors toward the a3 under-declaration |

## 3. Single most dangerous surviving path

**The gate manufactures the provenance the counter then consumes.** `build_block` writes
`cells[8] = access_date` and `cells[7] = "mined"` onto whatever row it is handed, and
`adoption_check` compares *no* `opened` cell to `access_date` — it trusts a self-declared
`verified-at:` line. So a round that opened nothing can produce the frozen target line exactly:

```
# step 1 — before: S077 absent from the fixture registry
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root $B/fx-chain kengaku
kengaku	ok	/tmp/r29a2r-gateattack/fx-chain/kengaku-shokunin/corpus/SOURCES.md          exit=0

# step 2 — append a row staged as queued, opened 2026-10-19, attributed to nothing
python3 plans/sources_adopt.py --registry $L/corpus/SOURCES.md --package $B/pkg-chain.md \
  --admit-ids S077 --scope-to-admit \
  --entries corpus/knowledge/benchmark-task-validity-checklist.md \
  --access-date 2026-10-25 --out $B/out-chain.md
registry=81 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote /tmp/r29a2r-gateattack/out-chain.md rows=1                                exit=0
# emitted: | S077 | … | fixture teaches | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-task-validity-checklist.md |

# step 3 — splice the emitted row into the registry (no source was fetched at any point)

# step 4 — counter on the manufactured state, entry's verified-at line admits the denial
python3 plans/adoption_check.py --lane $L --expect $B/expect-chain.json --census
entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok   exit=0
```

That is the frozen C1 line, word for word, from a tree where `queued`/`2026-10-19` became
`mined`/`2026-10-25` by command-line argument alone. C1's re-grounding duty ("every one of the
five sources is re-opened in this round") is therefore enforced by author honesty only: neither
tool reads a byte of any source, and the one field that would carry the evidence (`opened`) is
written by the tool from `--access-date`. Attacks a1/a2 show the same hole without step 2: an entry
whose text says "no URL was fetched on 2026-10-25" prints the frozen line, and a `verified-at:`
line that *contains* that denial still matches.

Impacted axes: C1 coverage (its acceptance instrument accepts fabrication), declared evidence
(the line has no denominator and no `required`), and C2 operability (the gate emits bytes the
census rejects with E03/E08/E11 while exiting 0).

## 4. Smallest safe corrections

1. `plans/adoption_check.py` (+3 lines in `main`): reject a `verified-at` line with any trailing
   text (`r"^verified-at: " + re.escape(access_date) + r"$"`), and add one counter
   `rows_fresh` = cited ids whose registry `opened` cell equals `access_date`, required == `required`.
   This alone turns a1, a2 and the chain red.
2. `plans/adoption_check.py` (+1 line): print `required` in the line
   (`cited_rows={len(cited)}/{required}`) so a4 and a3 are distinguishable without an exit code.
3. `plans/sources_adopt.py` (+4 lines in `build_block`/`main`): refuse when a staged row's `status`
   is not `mined` or its `opened` cell is not `--access-date` (instead of overwriting both), and
   validate `--access-date` against `ISO_DATE_RE` and `--recheck` against the recheck grammar before
   writing. Kills f1/f2/g2/g3 at source.
4. `plans/sources_adopt.py` (+2 lines): `if len(set(want_ids)) != len(want_ids): return EXIT_MALFORMED`
   in `check`, and refuse an `--entries` path that is not an existing `corpus/knowledge/*.md`
   (kills d2, g1), and fail closed when the *registry* parse leaves a row-shaped line unparsed
   (`collect` currently discards `bad` from the registry side, kills d3).
5. `plans/sources_adopt.py` (+1 line in `print_report`): print `collisions=<scoped>/<total>` so d4's
   `collisions=0` cannot be read as "this package is clean".
6. Add three selftest cases (status != mined, `main` without `--entries`, refusal path through
   `main`) so e1/e2/e3 cannot be green-by-deletion. Today no case stages a status other than
   `mined`, no case exercises the escaped-pipe refusal through `main()`, and no case runs `main()` at
   all — which is why e1, e2 and e3 each print `SELFTEST cases=10 failed=0` with the capability gone.

## 5. Reproduce

Fixtures live under `/tmp/r29a2r-gateattack` (`fx-a`, `fx-a3`, `fx-c`, `fx-c2`, `fx-chain`,
`fx-append-*`, `d/`, `e/`). Each fixture lane is a copy of the committed `corpus/` plus a
`shokunin.conf` carrying one `LANES` line, so the real fleet census resolves `kengaku` and runs
unstubbed; the only edited bytes are the registry rows and the fixture entries. Mutants in `e/` are
single-branch deletions from the committed file, each asserted to match exactly once before writing.
