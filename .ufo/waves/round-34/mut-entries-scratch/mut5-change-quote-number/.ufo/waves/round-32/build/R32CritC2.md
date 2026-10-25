# R32CritC2 — attack on the C2 counter (`plans/round32_defects.py`, R1–R7)

Seat: critic, C2 (calibration). Access date 2026-10-25. Read-only on the lane; no production bytes touched.
Scratch: `/tmp/r32-critc2/` (harness + copies, < 1 MB). No tool installed, no pacman transaction (host-wide pause
respected); `python3` 3.14 and `git` only.

## Revisions pinned

| revision | identity | lines |
|---|---|---|
| frozen blob | `git show 0d32691:plans/round32_defects.py` → sha256 `4edb2796dae68caad52e26ec791dc070c43c90263d2304af8cdbf4f6acf0ecb8` | 248 |
| live snapshot A | sha256 `5c22ebef0da89a46da23173717cb1c70bebe7c31d26243dbc979948c43bead37` | 267 |
| live snapshot B (current at close) | sha256 `064289153d4b49431e135a2f8275affab2e845e25cde91ae45365f98ebdcdf06` | 269 |

The working tree was edited **twice** by an unattributed sibling seat during this review. It is **not** the mutation
tester, which confirmed by message that it holds no edit and that its copies live in `/tmp/r32-R32MutCounters/`.
Snapshot A added the `r31_report`/`r32_report` injection seams plus synthetic R1/R2 selftest fixtures; snapshot B
added `if item_id in ("R1", "R2"): continue` to the generic selftest loop (live :229-230). Neither edit touched an
R1–R7 predicate, so every escape below holds on all three revisions. Line citations are the frozen blob's unless
marked *live*. The full escape matrix was re-executed against snapshot B at close: all eight headline routes
(R1 negation, R1 wrong-commit, R2 repudiating citation, R3 wrong path, R4 registry prose, R5 `deadline`, R6 quote
locator, R7 "erratum is not peer-reviewed") are still GREEN.

Baseline reproduced on all three revisions: `checks=7 defects=7`, exit 1, and the seven `DEFECT` lines match
`.ufo/waves/round-32/claims/defects-before.txt` line for line. The frozen control is honest.

## Method

Copy of the counter with only `FLEET = Path(...)` repointed to `/tmp/r32-critc2/fleet`; lane copy at
`/tmp/r32-critc2/lane` holding `SKILL.md`, `corpus/lessons/round-30.md`, `round-31.md`,
`corpus/evidence/round31/gate-cli-exits.txt` (real bytes) and a git repo on `master`. Each scenario restores the
baseline, applies **one** minimal change, and calls the real check function. Nothing in the lane was written.

## Headline

Every check is a token-proximity test over one flat string. The shared primitive is

```python
64 def near(text, a, b, width=300, flags=re.I):
67     re.search(re.escape(a) + r".{0," + str(width) + r"}" + re.escape(b), text, flags) or ...
```

`re.escape` gives **no word boundaries** (substring match), `.` does **not** match `\n` (tokens must share one
physical line), and there is **no negation, section or row anchoring** except R4's single heading scan. Consequences:

- **Repair-free greens are the norm, not the exception.** Confirmed escapes: R1 ×5, R2 ×3 (+ ordering unproven),
  R3 ×3, R4 ×4, R5 ×4, R6 ×4, R7 ×4.
- **The only fake route the counter kills is R3's literal `can't open file` string.**
- The counter also **false-reds three honest repairs** (below), so it selects for the degenerate one-liner it can
  match rather than for good evidence.
- The counter's **own selftest went red when C2 was repaired** (frozen blob and snapshot A; closed by the owner at
  snapshot B).
- `*-red-on-empty` exercises **only each check's file-existence guard**, never its predicate: five predicate mutants
  — including deleting R4's heading test and R6's label test outright — pass `--selftest` with `failed=0`.
- The **"frozen seven" guard is a self-comparison** and can never fire — still open at snapshot B, independently
  confirmed by the mutation tester (M1).

## Per-item verdicts

### R1 — phantom hash `a44b5a8` superseded by `ae95fe0` → **ESCAPES (5 routes; 0 kills)**

Code: `near(text,"a44b5a8","superseded"|"erratum")` (:78) is same-line; then
`if "ae95fe0" not in text` (:80) is **file-wide**. The two conditions are independent, so the erratum never has to
name the real commit — the file merely has to contain the string.

| route | content appended to the round-31 report | verdict |
|---|---|---|
| a | ``- `a44b5a8` superseded by `a44b5a9`. Unrelated token deae95fe0.`` — wrong commit named, real hash only inside a longer hex | **GREEN** |
| b | ``- `a44b5a8` superseded by the report's own appendix; `ae95fe0` is NOT this erratum's locator.`` | **GREEN** |
| g | ``- the appendix is superseded; the phantom `a44b5a8` stands; see `ae95fe0` for the CLI fix.`` — `superseded` attaches to another noun | **GREEN** |
| h | ``- `a44b5a8` is NOT superseded; no erratum is owed; `ae95fe0` is a different fix.`` — explicit negation | **GREEN** |
| f | body **rewritten** (`:226` `a44b5a8`-class → `ae95fe0`-class) + note re-supplies the token: append-only violated, `a44b5a8` gone from the body | **GREEN** |

The counter never runs `git cat-file -t a44b5a8` (missing) or `-t ae95fe0` (a commit) — the string `cat-file` occurs
only in the :12 docstring — even though both are one `git()` call away and the module already owns `git()` (:58).
Route (f) shows the append-only proxy is circular: the
note that is supposed to *supersede* the token is also the thing that *supplies* it.

**False red:** a correct erratum with the commit on the next line —
```markdown
- `a44b5a8` is superseded by
  `ae95fe0` (the real locator-fix commit).
```
→ `no appended erratum supersedes the a44b5a8 citation`. `near()` cannot cross the newline. Only the one-liner
`- \`a44b5a8\` superseded by \`ae95fe0\`, the real locator-fix commit.` is green.

### R2 — round-32 report cites the final lane tip → **ESCAPES (3 routes; 0 kills)**

Code: `if tip not in read(R32_REPORT)` (:94). Substring, anywhere, any context.

| route | verdict |
|---|---|
| a | `Draft only. The lane tip \`<TIP>\` must not be cited until the report lands.` | **GREEN** |
| b | tip inside a stale receipt fence: `` ``` $ git rev-parse master   # <TIP>  <- stale, superseded ``` `` | **GREEN** |
| c | tip as a prefix of a longer token: `` commit range `<TIP>deadbeef` was rejected `` | **GREEN** |

**Ordering is not evidenced at all.** The frozen predicate says "the round-32 report **exists after the last lane
commit**"; the report lives in the fleet repo, untracked by the lane, and the counter compares no mtime, no commit
ancestry, no receipt timestamp. Demonstrated sequence: report written citing tip A → **GREEN**; lane commit B →
red; report **edited post-hoc** to cite B → **GREEN**, while the report still predates B. The check is therefore a
live string equality against `rev-parse master`, i.e. it forces the report to be re-edited after every lane commit —
which is the recurring ordering defect turned into a manual edit discipline, not proof of order.

**Structural:** `check_r2` reads only `R32_REPORT`. The routed item (the round-31 report never citing its final lane
commits) is **never re-derived**; R2 scores the *next* round's discipline. That is a proxy by the claim's own
wording, but the claim's label ("report exists after the last lane commit") reads as a closure that the counter
does not perform.

### R3 — round-31 CLI receipt regenerated with the corrected path → **ESCAPES (3 routes); KILLS 1**

Code: literal `"can't open file"` (:104), the four-token loop (:106), literal `"../../../../plans/sources_adopt.py"`
(:109). No path is ever resolved; no fixture digest, timestamp or command transcript is required.

Path arithmetic verified on the real lane from the receipt's own cwd `.ufo/waves/round-31/c3-fixtures`:
`../../../plans/sources_adopt.py` → `…/kengaku-shokunin/.ufo/plans/sources_adopt.py` **exists=NO** (the defect);
`../../../../plans/sources_adopt.py` → `…/kengaku-shokunin/plans/sources_adopt.py` **exists=YES** (the fix). The
blessed string is arithmetically right — but the counter only checks that the string *occurs*.

| route | receipt content | verdict |
|---|---|---|
| a′ | `run:` line still executes `../../../plans/sources_adopt.py`; blessed token only in a comment (`# corrected form ../../../../plans/sources_adopt.py (not re-run)`); all four exit tokens present | **GREEN** — wrong file still the executed one |
| b | fully hand-written: no `run:` line, no fixture identity, just `../../../../plans/sources_adopt.py` + `exit=0/8/9/2` | **GREEN** |
| c | wrong path kept, failure text reworded (`FileNotFoundError: [Errno 2] .ufo/plans/sources_adopt.py`) so it is not the literal string, blessed token present | **GREEN** |
| d | keeps the literal `can't open file` line | **RED (killed)** |

The verdict map is legitimate — `plans/sources_adopt.py:50-58` defines `EXIT_OK=0`, `EXIT_QUOTE_UNREADABLE=2`,
`EXIT_URL_MISMATCH=8`, `EXIT_URL_UNMAPPED=9` — so requiring `exit=8`/`exit=9` is sound. But `exit=2` is shared by the
usage guard *and* by CPython's own "script not found", which is why the literal-string test is the only thing
separating route (c) from the defect. The receipt is a text file with no provenance: nothing binds it to a run.

### R4 — `plans/sources_adopt.py` row in `SKILL.md` §Gate/probe registry → **ESCAPES (4 routes; 0 kills)**

Code: first match wins (`re.search`, :119), then the **last** `^#{1,4}\s+\S` line before it (:124-126), then
`(?i)(gate|probe|registry)` on that heading (:127). The comment on :122 claims "The row must sit under the
Gate/probe registry section, not in prose" — the code cannot tell prose from a row.

| route | placement | verdict |
|---|---|---|
| a | prose sentence under `## Planning-horizon & transcript-shape probes` (real heading, `SKILL.md:386`, **earlier** than the registry at `:560`, so it wins the first-match race) — no registry row anywhere | **GREEN** |
| b | prose under the real `## Gate/probe registry (PROTOCOL §Gate standard)` heading, no table row | **GREEN** |
| c | `` ```bash # probe registry \n plans/sources_adopt.py ``` `` — a shell comment inside a fence is accepted as the heading | **GREEN** |
| e | a table row under `### Probe notes (not the registry)` | **GREEN** |
| d | decoy under a heading with none of the three words | RED |

Route (b) is the sharpest: it is exactly the placement the check's own comment forbids, and it is green. Route (a)
also means the check can go green **without any row at all** while the registry table stays empty, and can go red on
a correct row if an earlier prose mention exists.

### R5 — `R31FxEntryBar` recorded dead in the round-32 seat ledger → **ESCAPES (4 routes; 0 kills)**

Code: `near(text, "R31FxEntryBar", "dead", width=160)` (:137). Substring, any section, no negation.

| route | content | verdict |
|---|---|---|
| a | `\| R31FxEntryBar \| missed its deadline, never reported \|` — `dead` matches inside `deadline` | **GREEN** |
| b | `\| R31FxEntryBar \| is not dead; no committed report exists \|` — explicit negation | **GREEN** |
| c | `## Non-claims` bullet: "the dead-link sweep did not cover `R31FxEntryBar`" — not a ledger, `dead` unrelated | **GREEN** |
| d | `## Frontier` bullet: "`R31FxEntryBar` slipped past the deadline" | **GREEN** |

Nothing cross-checks the round-31 wave registry to confirm the seat has no committed report, and nothing requires
the `## Seat ledger` section the message names. A lesson that says the seat is **alive** is green.

### R6 — lesson locators corrected → **ESCAPES (4 routes; 0 kills)**

Code: `near(text31,"verifier_mode.py",":39-40")` (:149) + label near `:39-40` (:151); then
`":72" in text30 and "82-83" in text30` (:164) + label near `:72` (:166-168).

Context: the stale locator is `corpus/lessons/round-31.md:57` (the S092 row inside §Gate, 8–91); the cell reads
``precedence docstring (`:35-38`)``. It is the **only** `:35-38` and the only `verifier_mode.py` in the file.

| route | note | verdict |
|---|---|---|
| b | ``- `verifier_mode.py:39-40` is the quote-mode guard; correction noted.`` — attaches `:39-40` to the **quote** locator, precedence cell untouched | **GREEN** |
| c | ``- the claim that `verifier_mode.py:39-40` needs a correction is wrong.`` — negation | **GREEN** |
| d | ``- is `verifier_mode.py` precedence `:35-38` or `:39-40`? correction TBD.`` — a question, not a correction | **GREEN** |
| e | rewrite the `:35-38` cell in place to `:39-40`, then append ``- `verifier_mode.py` `:35-38` superseded by `:39-40` — correction.`` — append-only violated, note re-supplies the "stale" token | **GREEN** |

Route (e) is the append-only hole: `":35-38" in text31` (:147) is satisfied by the correction note itself, so a
pure rewrite passes. Lesson-30's half is weaker still: `":72"` is a three-character token with no anchor, and any
line pairing it with `82-83` and `corrected`/`superseded` passes — including a note about a different document.

### R7 — round-30 `:66` S083/S086 grouping corrected → **ESCAPES (4 routes; 0 kills)**

Code: `near(text,"S086","without peer review"|"not peer-reviewed")` (:181) + `near(text,"S086","erratum"|"correction")`
(:185).

| route | content | verdict |
|---|---|---|
| b | ``- `S086`'s erratum is not peer-reviewed either.`` — means the **opposite**; both `near` calls satisfied | **GREEN** |
| c | ``- we cannot claim `S086` was published without peer review; erratum pending.`` — a denial | **GREEN** |
| d | erratum attached to the **Q2 tier cell** only ("`S086` tier is B, and the paper is not peer-reviewed; correction to the tier cell only") — the `:66` grouping left standing | **GREEN** |
| e | rewrite `:66` to `S083 peer-reviewed; S086 without peer review`, then append a token line — append-only violated | **GREEN** |

**False red (the intended repair):** the natural markdown form is rejected —
```markdown
## Erratum
- `S086` is published **without peer review**; the `:66` grouping is corrected.
```
→ `the S086 peer-review erratum is not labelled`, because the heading `## Erratum` is on the previous line and
`near()` cannot cross it. The label word must sit on the same physical line as `S086`; splitting the sentence across
two lines (`… erratum: the society publishes\n  without peer review.`) fails too.

## Selftest — `--selftest` red-on-empty, verified

Run on the real lane (frozen revision): `SELFTEST checks=7 failed=0`, exit 0. Case by case, what each one actually
tests:

| case | reads | honest? |
|---|---|---|
| `registry-complete` | `FROZEN == tuple((i,l) for i,l,_ in CHECKS)` where `FROZEN` **is built from `CHECKS`** (:202) | **tautology** — always True |
| `R1-red-on-empty` | the **absolute** fleet path `R31_REPORT` (:73, :75), not `empty` | **no** — a snapshot of fleet state; skipped at snapshot B |
| `R2-red-on-empty` | the absolute `R32_REPORT` (:86) and then `git -C empty rev-parse master` | **no** — passes on "report absent" *or* on "not a repo"; never the ordering predicate |
| `R3`–`R7` red-on-empty | lane-relative paths | **yes** — each returns the genuine missing-file reason |

Confirmed reasons on an empty dir: R3 `…gate-cli-exits.txt is unreadable at lane tip`, R4 `SKILL.md is unreadable`,
R5 `corpus/lessons/round-32.md does not exist yet…`, R6 `corpus/lessons/round-31.md is unreadable`,
R7 `corpus/lessons/round-30.md is unreadable`.

**The selftest breaks when C2 is repaired.** With a *valid* R1 erratum appended to the fleet round-31 report,
`check_r1(empty)` returns `""` (it read the fleet report, not the empty dir) and the case fails:

```
CASE R1-red-on-empty FAIL
SELFTEST checks=7 failed=1      (exit 1)
```

This held on the **live snapshot A** (267 lines) too, even after synthetic fixtures were added: the new
`R1-red-without-erratum` / `R1-green-with-erratum` / `R2-red-missing-report` cases all PASS, but the generic loop
(:211) still called `check_r1(empty)` with the default absolute path, so `R1-red-on-empty` still FAILed post-repair:

```
CASE R1-red-without-erratum PASS
CASE R1-green-with-erratum PASS
CASE R2-red-missing-report PASS
CASE R1-red-on-empty FAIL
SELFTEST checks=7 failed=1      (exit 1)
```

**Closed at snapshot B** (269 lines): the generic loop now skips the two fleet-path checks —
`if item_id in ("R1", "R2"): continue  # synthetic fixtures above; the live fleet paths would couple the run`
(live :229-230). Verified: with a valid R1 erratum in place, snapshot B prints `SELFTEST checks=7 failed=0`, exit 0.
The finding stands as a defect of the frozen blob and is closed in the working tree by its owner, not by this review.

Operational note for the record: before that edit, whoever landed the R1 erratum would have turned the round's own
preflight red, and the tempting repair was to loosen R1 — the exact failure mode round 31 recorded as
`survivor — the C2 counter greened its own repair`.

**The frozen-seven guard is still dead code at snapshot B.** `FROZEN` is defined at :202 *from* `CHECKS`; `main`'s
guard (:230) compares `FROZEN` to a tuple rebuilt from the same `CHECKS`, so it is a self-comparison. Re-reproduced
on the current bytes: deleting the `("R7", …)` row from `CHECKS` yields `checks=6 defects=6`, exit 1, and **no**
`DEFECT registry:` line. On a repaired tree the same mutant prints `checks=6 defects=0` and exits 0 while frozen
item R7 is still un-repaired — a false green against a predicate that names exactly seven checks. A copy with R7's
label renamed *and* an eighth check added also runs normally (`checks=8 defects=8`, `CASE registry-complete PASS`).

**Independent confirmation.** `L1Kengaku32.R32MutCounters` reached the same two conclusions by mutation, on the
frozen 248-line snapshot, in `.ufo/waves/round-32/build/R32MutCounters.md`: M1 (`:46`, "delete the frozen R7 check
from `CHECKS` (survived)") states at `:63` — "Selftest cannot tell that a frozen check was dropped:
`registry-complete` compares `FROZEN` against a tuple re-derived from the same `CHECKS` (tautology — it can never
fail for this mutation class), and no case asserts the count `checks=7`"; M3 is the R1/R2 state coupling. Two
independent seats, two methods (targeted fake routes vs mutation), same survivors — the two findings are not
artifacts of one reviewer's construction.

### Predicate mutations survive the selftest (extension confirmed)

Mechanism: **every check's first statement is a file-existence guard** (`if not path.is_file(): return …`), so a
`*-red-on-empty` case exercises only that guard and can never reach the predicate. R3–R7 therefore have **zero
non-empty violating fixtures**, and any mutation *after* the guard is invisible to `--selftest`. Measured on
snapshot B:

| mutant | `--selftest` | consequence |
|---|---|---|
| `near()` → `return True or bool(…)` | `failed=0`, exit 0 | on the unrepaired tree `defects` drops 7 → 6 with exit 1, i.e. two items stop re-deriving |
| R5 `near(…, width=160)` → `10000` | `failed=0`, exit 0 | seat 200 chars from `dead` on one line: original **RED**, mutant **GREEN** |
| R7 `near(…, width=250)` → `10000` | `failed=0`, exit 0 | label adjacent, phrase 300 chars away: original **RED**, mutant **GREEN** |
| R4 heading test → `if False:` | `failed=0`, exit 0 | the registry-section requirement is no longer checked at all |
| R6 `:39-40` label test → `if False:` | `failed=0`, exit 0 | the correction-label requirement is no longer checked at all |

The last two rows are the point: the predicates can be **deleted** and the selftest stays green, because no case ever
presents a file that exists. This is the mutation-tester's extension to the limit recorded under correction 9
(`R32MutCounters` postscript), and it widens item 8 from "add fixtures" to "**one non-empty violating fixture per
check is required for the counter to be testable at all**".

## Impacted axes

- **C2 calibration (direct).** The frozen predicate's kill rule is "an item that cannot be repaired … is reported as
  an open defect and C2 misses". The counter cannot distinguish repaired from unrepaired for six of seven items, so
  `defects=0` is not evidence that the seven routed defects closed. C2 can be declared met on bytes that leave the
  defects standing.
- **C1 / C3 separability: holds.** The read set is exactly the round-31 fleet report, the round-32 fleet report, the
  round-31 CLI receipt, `SKILL.md`, and lessons 30/31/32. No C1 or C3 artifact is read; R13 is satisfied.
- **Novelty / coverage: no impact.**
- **Append-only discipline (cross-cutting).** R1/R6/R7 proxy append-only with token presence, which the correction
  note itself re-supplies; there is no `git diff --numstat` prefix test anywhere in this counter, although round 31's
  own lesson (`corpus/lessons/round-31.md:130` region, `survivor` row) records that such a test is the fix.

## Smallest safe corrections (ranked, each a local edit)

1. **`near()` word boundaries + no-negation window.** Replace `re.escape(a)`/`re.escape(b)` with
   `r"(?<![0-9a-z])" + re.escape(a) + r"(?![0-9a-z])"` (kills `deadline`, `deae95fe0`) and reject a match whose
   intervening span contains `not |n't |no longer |cannot |never`. Single change, kills R1 a/b/g/h, R5 a/b, R7 b/c.
2. **Anchor every note to its section.** Generalise R4's heading scan into one helper: require the match offset to
   fall inside the section whose heading matches the item's named section (`## Seat ledger` for R5, `## Erratum`/the
   Gate table for R6/R7, `## Gate/probe registry` for R4). Kills R4 a/b/e, R5 c/d, R6 b, R7 d.
3. **Append-only for real.** For each lesson/report the counter reads, require
   `git diff --numstat <baseline> -- <path>` to show `0` deletions (prefix-only growth). Kills R1 f, R6 e, R7 e, and
   makes the "stale token still present" test meaningful.
4. **R1 identity.** Run `git cat-file -t a44b5a8` (must fail) and `git cat-file -t ae95fe0` (must be `commit`), and
   require both to sit in one erratum line with the label. Kills R1 a/b/g.
5. **R2 ordering evidence.** Require the tip citation on an explicitly labelled line (`final lane tip: <hash>`), and
   bind order: the report file's mtime (or a `date -u` receipt line inside it) must be ≥ the committer date of the
   cited commit. Kills R2 a/b/c and the post-hoc-edit route.
6. **R3 resolve, don't match.** Require a `run:` line carrying the cwd, resolve every referenced script path with
   `Path.resolve().is_file()`, require a sha256 per fixture, and accept `exit=2` only on a line whose stderr contains
   `usage:`. Kills R3 a′/b/c.
7. **R4 require a row.** The matched line must start with `|` and carry ≥4 cells, and the section heading must equal
   `## Gate/probe registry (PROTOCOL §Gate standard)` exactly. Kills R4 a/b/c/e.
8. **Selftest: decouple and mutate.** Delete `R1-red-on-empty`/`R2-red-on-empty` from the generic loop (**applied at
   snapshot B**, live :229-230) and give **every** check at least one non-empty violating fixture (the round-31
   `m3/m4/m5` survivor class). Today R3–R7 have none, so the five mutants tabulated above all pass `--selftest`;
   the acceptance test is that each of those mutants must turn the selftest red.
9. **Registry guard.** Replace `FROZEN = tuple(... from CHECKS)` with a literal
   `FROZEN = (("R1","round31-report-phantom-hash"), …, ("R7","round30-peer-review-erratum"))` so the guard can fire,
   and add an explicit `assert len(CHECKS) == 7` / a `checks=7` assertion in both `selftest` and `main` — the literal
   tuple catches deletion and renaming, the count makes the failure message name the class ("a frozen check was
   dropped", M1). Note the limit: no registry guard can catch a *predicate* mutation such as tautologising `near()`
   to `True` (R32MutCounters M2, `R32MutCounters.md:65`); that class is only caught by non-empty violating fixtures
   in the selftest (item 8).
10. **Allow multi-line prose** (`re.S` with a bounded window, or require a structured note block) so the honest
    erratum shapes rejected above stop being red.

## Tooling record

No install, no upgrade: `python3` 3.14 (host), `git` (host). No pacman transaction (host-wide pause). Scratch
`/tmp/r32-critc2/` ≈ 0.4 MB, self-contained, nothing deleted outside it.

VERDICT: attack-finished
