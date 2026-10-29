# C2RevCounter — review of `plans/round53_c2_tipstate.py` against the frozen R53-C2 predicate

Seat: reviewer (wave 1, build). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scope: line-by-line review of the C2 counter against `plans/round-53-claims.md` (Claim 2, commit `a34838f`)
and against `SKILL.md`'s *Gate/probe registry*. The counter was **not** edited by this seat.

**Target note (the artifact moved twice under this review).** The claims freeze the counter at `a34838f`.
The lane tree carried a rewritten counter during this seat's window, which the L1 then committed as
**amendment A1** (`d40b705`, "amendment A1 (both counters hardened after wave-1 attacks)") and later
**A2** (added the `stage-scan` row; `plans/round-53-claims.md` §Amendments now carries both, dated
2026-10-28, before any scored run). Findings below are therefore stated twice where they differ:
**[FROZEN a34838f]** = the artifact the frozen predicate binds, **[A1/A2 = current HEAD+tree]** = the
artifact that will actually be scored. Line numbers for the frozen file are from
`git show a34838f:plans/round53_c2_tipstate.py` (377 lines); line numbers for the current file are from
the working tree (572 lines).

## Summary (classed)

| id | finding | where (current tip / frozen) | class | status |
|---|---|---|---|---|
| F1 | `Worker.reset` resets to the clone's *current* HEAD, so a row that commits leaves that commit for the next row on the same worker | `counter:116-120` (A1 tree) / `frozen:97-100` | `amendment-needed` | open; repair verified on a scratch copy (two lines) |
| F2 | `git clean -fdx` leaves a nested git repo a row created | `counter:119` / `frozen:100` | `amendment-needed` | open; `-ffdx` removes it; same fix as F1 |
| F3 | ledger `timeout_s` overrides the operator's `--timeout` | `counter:125` / `frozen:105` | `amendment-needed` | open; 0 of 78 rows use it today |
| N1 | committed ledger (`1ebf61f`) fails a clean-clone run: 17 of 77 declarations wrong; working tree flips 16 rows uncommitted | `plans/round53-tipstate.json` | ledger defect, blocks the claim | open; not a counter defect |
| F4 | `--help` / shell / wrapper argv launders red to green; registry read from the lane, not the tree under test | frozen only | `amendment-needed` (frozen) | **closed by A1/A2** (re-verified) |
| F5 | `__dups__` magic key collides with a row name | frozen | `cosmetic` | closed by A1 |
| F6 | `row_script` could not parse `uv run` entries | frozen | `cosmetic` | closed by A1 |

Parsing answers: `registry_rows` finds exactly the 75 frozen rows (77 at `1ebf61f`, 78 now with A2) with no
unparsed data rows; `row_script` returns `None` for 0 rows. `--jobs` > 1 is isolated per clone and shares only
the object store (measured); TMPDIR reaches the child; `clean -fdx` removes ignored files but not nested repos.

## Commands run (all reads of the lane; all fixtures under `/fast/scratch/hyaku/kengaku-r53/C2RevCounter/`)

```sh
# registry parsing
python3 -c "import importlib.util,json; ..."      # registry_rows / row_script on SKILL.md
awk 'NR>=560 && NR<737 && /^\|/' SKILL.md | wc -l  # 77 pipe lines in the registry block (manual count)
grep -c '^| *`' SKILL.md                          # header+rows
python3 plans/round53_c2_tipstate.py --lane . --dry
python3 plans/round53_c2_tipstate.py --lane . --source <clone> --work <scratch> [--jobs N]
python3 plans/round53_c2_tipstate.py --selftest
git show a34838f:plans/round53_c2_tipstate.py > <scratch>/frozen_c2.py
git diff a34838f -- plans/round53_c2_tipstate.py
git clone -q --no-hardlinks <lane> <scratch>/src && git -C <scratch>/src checkout -q 536925b…
```

Fixtures were created only with `git -C "$D" init -q` inside
`/fast/scratch/hyaku/kengaku-r53/C2RevCounter/`; `git rev-parse --show-toplevel` was asserted before
each fixture commit. No file outside this seat's directory and that scratch root was written.

---

## 1. Answers to the assigned questions

### 1.1 Does `registry_rows` find exactly the 75 rows? — **YES, exactly, and no more.**

Manual count of table rows in the registry block (`SKILL.md` lines 560–736): **77 pipe lines** = 1 header
+ 1 separator + **75 data rows**. `registry_rows` returns **75** names, all unique, and the set is
**identical** to the frozen `.ufo/waves/round-53/c2-row-names.json` (75 entries; symmetric difference
empty in both directions).

- Rows whose first cell is *not* a single backticked name: **none in the data rows.** The two non-matching
  pipe lines are the header (`| name | kind | …`) and the separator (`|---|---|…`), both correctly skipped.
- Every row has exactly 8 cells; `cells[2]` (the `entry` column) is therefore the entry cell for all 75.
- After A2 the registry is **78** rows (75 frozen + `round53-c1`, `round53-c2`, `stage-scan`); the counter's
  `FROZEN_NAMES_SHA` + `EXTRA_NAMES` pin reproduces that set exactly (`row_set_pinned=ok`).
- **[A1]** fixed a real defect here: the frozen `registry_rows` matched the heading with a bare
  `text.find("## Gate/probe registry")` (frozen line 40–46), so a heading renamed to `## Registry` gave
  `registry=0` **silently**, and a second `## Gate/probe registry` heading was invisible. A1 pins the
  heading line-anchored and requires exactly one (frozen `registry_block` → A1 `registry_block`,
  `headings=N`).

### 1.2 Does `row_script` find the entry script for every row? — **YES: 0 rows return `None`.**

All 77/78 rows resolve a script, all resolve to an existing file in the lane, and all 75/77/78 script paths
start with `plans/`, `corpus/` or `grader.py`. No row uses `uv run`, no row's entry cell lacks a
`python3 ….py` token, and **no row has the script only in a later backticked span** — `SCRIPT.search`
operates on `cells[2]`, the entry cell, and every entry cell carries its own `python3 <script>` token.

Two residual parsing facts (both cosmetic, neither wrong today):
- `scratch-root-guard` is the **only** row whose entry cell contains two `python3` tokens
  (`plans/scratch_guard.py` twice — `check <root>` and `safe-rm <root> <seat> <path>`). `row_script` takes
  the first, which is the same script, so the result is right.
- The frozen `SCRIPT` regex is anchored to `python3 ` + a path under `plans|corpus|grader`. An entry cell
  using `python3 -m`, `sh -c`, or `uv run python3` would yield `None` → the row could never be satisfied.
  **[A1]** replaced this with `argv_ok(argv, script)` (current lines 145–156), which accepts
  `python3 <script> …` and `uv … python3 <script> …` and rejects shells, `-c` and wrappers — and it
  requires the argv to *name the same script*, which is what the frozen predicate asks for.

### 1.3 Is `--jobs` > 1 safe when two rows write the same file in their separate clones? — **YES, with one caveat.**

Measured:
- Each worker owns a distinct clone (`work/w<i>/src`); `git clone -q --shared` gives every worker its own
  working tree and its own `HEAD`.
- Two rows writing the *same relative file* under `--jobs 4`: **no collision** — each row's write lands in
  its own clone; `RUN executed=2 … mismatched=0`.
- The **shared object store** is the `alternates` link to the source's `.git/objects`. A commit made in
  worker 0's clone is **not** visible in worker 1's clone and **not** in the source
  (`w0 sees it: True`, `w1 sees it: False`, `SOURCE sees it: False`). `git gc --prune=now` inside a
  `--shared` clone leaves the source's objects intact (`source still has the commit: True`), so the shared
  store is **not** corrupted by a worker running gc.
- **Whether F1 caused the *real* full-run mismatches is NOT established by this seat** — see §5: an isolation
  run (one row per fresh clone) shows the seven red->green rows it tested are wrong in the *ledger*, not
  contaminated. F1 is a real hole with a synthetic reproduction; its real-world share of the 17 mismatches
  is unmeasured.
- **Caveat (defect, below):** `--jobs` does **not** change the per-worker reset semantics; a row that
  *commits* inside its clone leaves committed artifacts behind for the **next row on the same worker**.
  With `--jobs 1` that is every subsequent row; with `--jobs 4` it is every fourth row. Jobs > 1 makes the
  contamination *less* frequent, not absent.

### 1.4 Does `Worker.reset` leave state between rows? — **YES. This is the one real surviving defect.**

- `clean -fdx` **does** remove ignored files (`-x` is present): a row-created `ignored.txt` is gone after
  reset (`ignored file removed by clean -fdx: True`). Untracked files are removed too.
- **`clean -fdx` does NOT remove a nested git repository** — it needs `-ff`:
  `nested repo survives clean -fdx: True`; `clean -ffdx` removes it. A row that runs `git init` in its cwd
  leaves a nested repo that `reset` cannot clear.
- **The decisive hole:** `git reset -q --hard` is issued **with no ref**, so it resets to the clone's
  **current** `HEAD` — which a row may have moved by committing. Measured: base rev `f6b9fda2` → a row
  commits → `reset` → `HEAD` is still `3c4e5532` (the row's commit), the committed file **survives**
  (`COMMITTED.txt survives reset: True`), and `git status` is **empty** — the contamination is invisible.
  **[A1] kept `reset -q --hard` without a ref** (current lines 116–120); it only added `check=True` and
  reordered clean-before-reset. It did **not** pin the reset target.
- **Synthetic end-to-end consequence, measured on the current counter with the 78-row registry:** row
  `adoption-check` commits a file; the next row on the same worker, `anchor-digest-check`, is written to
  exit 1 iff that file exists; the counter reports
  `MISMATCH anchor-digest-check declared exit=0 observed exit=1` — i.e. **one row's observed exit is
  determined by the previous row's committed artifact, not by the tree.** A row can therefore make the
  *next* row's tip-state a lie in either direction (a false red here; the same mechanism inverted gives a
  false green).

### 1.5 Does `TMPDIR` per row reach the child? — **YES.**

Measured: the child sees `TMPDIR=<work>/tmp-<row>` and `os.path.isdir(TMPDIR)` is `True`; the directory is
removed after the row (`tmp dir removed after the row: True`). The per-row dir is derived from the row name
(`re.sub(r'[^A-Za-z0-9_.-]', '_', name)`), so two rows cannot collide on it.
**[A1]** additionally scrubs credential-shaped variables before the child starts: a row seeing
`R53C2_FAKE_TOKEN` in its environment is reported as `SECRET_PRESENT= False` (frozen counter passed the
full environment through unchanged).

### 1.6 `--selftest` — run in a scratch clone, each case read for vacuity

`python3 plans/round53_c2_tipstate.py --selftest` → **`cases=50 failures=0`** (current artifact);
the frozen artifact gave **`cases=12 failures=0`**. Every case asserts a *specific* marker line plus the
exit code, and each was re-derived by hand; the twelve frozen cases are all **non-vacuous**:
`truthful` (rc 0, `PREDICATE R53-C2 pass` **and** `declared_green=1 declared_red=1 observed_green=1
observed_red=1`), `forged-all-green` (must show `MISMATCH b declared exit=0 observed exit=1`),
`forged-all-red`, `missing-ledger-row`, `extra-ledger-row`, `ledger-points-elsewhere`,
`red-evidence-absent`, `red-reason-thin` (`reason="broken"` → 1 word < 10), `state-exit-inconsistent`,
`timeout`, `help-only-argv` (asserts `ARGV entry=0 selftest=0 help=2` — the *share* rule, not just a
rejected help row), `partial-run-never-passes` (asserts `PREDICATE R53-C2 fail`).
The 38 A1 cases are likewise marker-asserting, and the four pin cases mutate `FROZEN_NAMES_SHA` /
`EXTRA_NAMES` and restore them, so they are self-contained.

Two **vacuity** observations on the current selftest (both cosmetic, neither hides a leg):
- `evidence-null` asserts `want_out=("Traceback",)` — i.e. it asserts the counter does **not** print a
  traceback. Good. But the frozen counter **did** raise `KeyError: 'evidence'` on a red row whose ledger
  entry lacked the `evidence` key (frozen line 240, `sp["evidence"]` after `static_legs` had already
  flagged it `bad_reason`): an uncaught exception, exit 1 by traceback rather than by predicate. **[A1]**
  fixed it (`evidence` must be a string → `BAD-REASON`, no crash); the current counter prints
  `BAD-REASON b` and `PREDICATE R53-C2 fail`.
- The frozen `timeout` case relies on `timeout_s` **in the ledger**, i.e. the ledger sets its own timeout
  budget — see F3.

---

## 2. Defects

### F1 — `Worker.reset` resets to the clone's *current* HEAD, so a row that commits contaminates the next row on the same worker — **amendment-needed**

- Where: frozen `plans/round53_c2_tipstate.py:97-100` (`Worker.reset`, `git reset -q --hard` with no ref);
  current `plans/round53_c2_tipstate.py:116-120` (same call, still no ref).
- Evidence (current counter, real 78-row registry, `--jobs 1`): `MISMATCH anchor-digest-check declared
  exit=0 observed exit=1` — the observer row's exit is set by the previous row's committed file.
  Unit-level: base `f6b9fda2` → row commits → `reset` → `HEAD` = `3c4e5532` (the row's commit),
  `COMMITTED.txt survives reset: True`, `git status` empty.
- Why it matters: the frozen predicate's executed leg is "re-executes every argv in a scratch clone and
  observes exactly the declared exit code". A row's observed exit must be a property of the **tree**, not
  of the previous row's writes. As written, one row can forge the next row's tip-state, in either
  direction, and the counter cannot tell.
- Minimal repair (one line + one): capture the source's rev at clone time and reset to it —
  in `Worker.__init__`, `self.base = subprocess.run(["git","-C",str(self.dir),"rev-parse","HEAD"],…).stdout.strip()`,
  and in `reset` use `["git","-C",str(self.dir),"reset","-q","--hard",self.base]` instead of the ref-less form;
  also use `clean -q -ffdx` so a nested repo a row created is removed.
- **The repair is verified.** A patched copy of the current counter (only those two changes, in a scratch
  file — the lane's counter was **not** edited) run against the *same* 78-row fixture that produced the
  `MISMATCH` above yields `RUN executed=78 timeout=0 mismatched=0 evidence_missing=0` and
  `PREDICATE R53-C2 pass`: the observer row now sees the clean tree. The patched file is
  `.ufo/waves/round-53/w1/C2RevCounter/patched_c2.py` (a scratch artefact, not a proposed landing edit).

### N1 — the committed ledger does not reproduce on a clean clone: 17 of 77 declared states are wrong — **not a counter defect; a ledger defect that blocks the claim**

- Where: `plans/round53-tipstate.json` at commit `1ebf61f` (the committed ledger); the uncommitted working-tree
  copy differs from it in 16 rows.
- Evidence (verbatim in `.ufo/waves/round-53/w1/C2RevCounter/full-run.txt`): a full run of the counter on a
  clean clone of `1ebf61f` (77 rows, `--jobs 6`) ends `RUN executed=77 timeout=0 mismatched=17
  evidence_missing=1` and `PREDICATE R53-C2 fail`. The 16 rows declared `exit=1 state=red` that exit 0 on the
  clean clone are: `ledger-tip, package-gate, round36-c1-battery, round36-c2, round37-c1-mutants, round37-c2,
  round38-c2, round39-c1-audit, round39-c1-mutants, round39-c2, round40-c2, round41-c2, round42-c2, round43-c2,
  round44-c2, round45-c2`. The 17th mismatch is the reverse: `round53-c1` is declared `exit=0 green` and
  observes `exit=1` on that clone. `round40-c1-mutants` is declared red with evidence `BATTERY fixtures=21
  wrong=11 tampered=0 sidechannel=0`, exits 1 as declared, and its fragment is absent from the clean-clone output
  (`EVIDENCE-MISSING`).
- **Isolation (rules out contamination for these rows):** the seven red->green rows
  (`ledger-tip, package-gate, round36-c2, round38-c2, round40-c2, round41-c2, round45-c2`) were re-run with
  `--jobs 7`, so every row had its own fresh clone and no prior row on its worker: all seven still exit 0
  (`isolation-run.txt`). The declarations are therefore wrong for these rows on a fresh tree, not because an
  earlier row left state behind.
- **The uncommitted working tree has already flipped those 16 rows to green** (`ledger-working-vs-committed.txt`:
  `changed=16 added=['stage-scan'] removed=[]`). That matches the clean-clone observation, but it is an uncommitted
  edit made after the `1ebf61f` measurement; no run of the counter on the flipped ledger exists in this seat's
  evidence. `round53-c1` is still declared green in the working tree.
- Why it matters: the ledger's red declarations were measured in the lane tree, not on a clean clone, so they
  describe the lane's state (untracked `.ufo/` evidence, ignored files, prior runs) rather than the tip. That is
  the exact failure C2 exists to catch (round-52 `false-registry-cell`).
- Repair (ledger, not counter): commit the ledger after re-deriving every row on a clean clone of the commit
  that carries it, and re-run the counter on that clone. Do not hand-set any `exit`/`state` to match an observation
  without the observation being in the run that is committed beside it. `round53-c1` must be re-declared from its
  observed clean-clone exit.

### F2 — a row's nested git repository survives `clean -fdx` — **amendment-needed** (subsumed by F1's repair)

- Where: frozen line 100 and current line 119 (`git clean -q -fdx`).
- Evidence: `nested repo survives clean -fdx: True`; the same command with `-ffdx` removes it.
- Why it matters: a row that runs `git init` in its cwd (several registry rows create fixture repos —
  `round_close.py` builds five two-commit fixtures) leaves a nested repo whose files the next row on that
  worker can read. `--jobs > 1` bounds the blast radius to the rows sharing a worker; it does not remove it.
- Minimal repair: `clean -q -ffdx` (double `-f` removes nested repositories).

### F3 — the ledger sets its own timeout budget, overriding the operator's `--timeout` — **amendment-needed**

- Where: frozen line 123 and current line 125: `t = int(spec.get("timeout_s") or default_timeout)`.
- Evidence: operator passes `--timeout 1`; the ledger entry says `timeout_s: 6`; measured elapsed **6.0 s**
  and the row was reported `TIMEOUT a after 6s`. Without the ledger key the same row times out at 1 s
  (measured 1.0 s).
- Why it matters: the timeout is the counter's own control on a hung instrument, and the frozen predicate
  requires "**no timeout**" (`timeout=0`). Letting the artifact under measurement choose the budget means a
  ledger can raise the budget for a row that hangs — the leg that is supposed to catch a hung instrument is
  under the ledger's control. (The landed ledger `plans/round53-tipstate.json` currently declares
  `timeout_s` on **0 of 78** rows, so today's ledger does not exploit it; the *counter* still allows it.)
- Minimal repair: take the timeout from the CLI only — `t = default_timeout` — or clamp:
  `t = min(default_timeout, int(spec.get("timeout_s") or default_timeout))`. If the ledger key is kept for
  provenance, it should be capped by, not substituted for, the counter's budget.

### F4 — [FROZEN a34838f only] the frozen counter can be passed by a ledger whose argv never runs the instrument — **fixed by A1**

- Where: frozen lines 64–69 (`row_script` / `SCRIPT`) and 144 (`script not in argv`).
- Evidence against the frozen artifact: appending `--help` to a red instrument's argv
  (`["python3","plans/a.py","--help"]`, kind `entry`) → `PREDICATE R53-C2 pass`, while the instrument's real
  entry exits 1. On the real registry, `plans/state_check.py --summary` exits **1** but
  `plans/state_check.py --help` exits **0**; same for `plans/round51_surfaces.py` (**1** vs **0**) — so
  `--help` laundering turns 22+ real reds green. A static probe with `--help` appended to **all 75** rows
  passed every static leg with `entry_mismatch=0`.
- Also against the frozen artifact: the lane's `SKILL.md` could be truncated and the ledger truncated with
  it, and the frozen counter passed (`PREDICATE R53-C2 pass`, `registry=1`) while the source tip still had
  2 rows — the frozen counter read the registry from `--lane`, not from the tree under test.
- Status: **[A1] closed both.** The current counter reads registry+ledger from `--source`, requires
  `--source` to be a clean git work tree whose HEAD equals the lane's HEAD (`lane_rev_equal`), pins the row
  set by digest, and requires the argv to *be* `python3 <script> …` / `uv … python3 <script> …` with
  `kind` matching the argv's own flags (`--help` ⇔ `help`, `--selftest` ⇔ `selftest`). Re-verified on the
  current artifact: `--help` on a red row now yields `BAD-DECL a`; a truncated registry yields
  `row_set_pinned=BAD`; a non-git source yields `SOURCE not a git work tree clean=NO`.
  **No action needed for F4** — recorded because the frozen predicate binds the frozen artifact, and the
  before-state is re-derivable from `a34838f`.

### F5 — [cosmetic] the frozen `registry_rows` collided with a row literally named `__dups__` — **fixed by A1**

- Where: frozen lines 48–61 (`rows["__dups__"] = …` used a magic key inside the same dict it returned).
- Evidence: a registry row named `` `__dups__` `` would have been overwritten by the duplicate-name
  bookkeeping. The frozen selftest had no case for it; the current artifact has one
  (`row-named-dups-marker`) and returns the row tuple separately. **Fixed; no action.**

### F6 — [cosmetic] `row_script` cannot parse a `uv run` / non-`python3` / `-m` entry — **fixed by A1**

See §1.2. The frozen counter would have made such a row permanently unsatisfiable; the current artifact
accepts `uv … python3 <script> …` and has the `uv-run-entry` case. **Fixed; no action.**

---

## 3. Verification of the frozen predicate, clause by clause (current artifact)

| Frozen predicate clause | Current counter | Status |
|---|---|---|
| every registry row has exactly one entry (`missing=0 extra=0 duplicate_names=0`) | `static_legs` + the digest pin | **met** (`missing=0 extra=0 duplicate_names=0`, `row_set_pinned=ok`) |
| each entry's argv names the same script as its row's entry cell (`entry_mismatch=0`) | `argv_ok(argv, row_script(row))` | **met** (`entry_mismatch=0`) |
| `kind` ∈ {entry, selftest, help} | `kind_ok` (derived from the argv's own flags) | **met**; stricter than the frozen text, which is allowed |
| a declared exit consistent with its `state` (`bad_decl=0`) | `bad_decl` | **met** |
| at most 10 % of rows may be `help`-kind | `help_ok`, `MAX_HELP_FRACTION=0.10` | **met** (78 rows → limit 7.8; landed ledger has `help=0`) |
| every red row: reason ≥ 10 words + verbatim evidence (`bad_reason=0`) | `bad_reason` (words by `.split()`, evidence ≥ 6 chars and a string) | **met** (landed ledger: 28 red rows, min reason 27 words) |
| the counter re-executes every argv in a scratch clone and observes exactly the declared exit, no timeout (`executed = registry`, `mismatched=0 timeout=0`) | `run_row` + `evaluate` | **met in form**, but the *isolation* of the scratch clone is broken by F1/F2 — one row's commit can set the next row's observed exit. |
| every red row's evidence fragment present in the observed output (`evidence_missing=0`) | `sp["evidence"] not in r["out"]` | **met** |
| the source clone being clean (`clean=yes`) | `git status --porcelain` on `--source` + `lane_rev_equal` | **met**; A1 also rejects a non-git source and a source older than the lane |
| a run with `--only` never passes | `ok = … and only is None` | **met** |
| ledger schema / duplicate JSON key / evidence must be a string | `load_ledger` + `no_dup` object hook | **met** (A1) |

**Measured on the landed ledger** (`plans/round53-tipstate.json`, 78 rows, re-measured after A2 added
`stage-scan`): `schema=r53-tipstate-v1`, **50 green / 28 red**, kinds **74 entry / 4 selftest / 0 help**,
**0** rows with `timeout_s`, **0** rows with a leftover `<placeholder>`, **0** rows whose `kind` disagrees
with its argv flags, every red row's reason **≥ 24 words**, every red row's evidence **≥ 11 chars**.
One row (`round-close-check`) carries an absolute path in a *flag* — `--census
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` — which points at the **fleet** tree, not at the
lane; it is a read of a stable script, not an escape into mutable lane state, so it does not trigger the
residual risk noted in §4.

## 4. Residual risk and verification gaps

- **F1/F2 are the open items** and they are *calibration*-bearing: the executed leg is the whole point of
  C2, and it is not yet per-row hermetic against a committing or repo-creating row. Repair is two lines
  (`reset --hard <pinned rev>`, `clean -ffdx`) and is testable with the existing harness.
- **F3** is a control handed to the artifact under measurement; today's ledger does not use it, but the
  counter still permits it.
- **Registry size moved during this review**: 75 (frozen) → 77 (A1 added `round53-c1`, `round53-c2`) → 78
  (A2 added `stage-scan`). The counter's digest pin tracks it exactly (`row_set_pinned=ok` at each step);
  every measurement in §3 is on the current **78**-row tree, and §1.1's 75-row figures are the frozen
  base-tip ones.
- The `--jobs` axis was measured on file-write isolation, clone separation and shared-object-store
  integrity; a row that writes **outside** its clone (an absolute path in an argv flag) was tested and does
  reach the live lane (`observed exit=0` where the clone would have given 1) — **[A1]** does not constrain
  argv *values*, only the interpreter and the script token, so an argv flag pointing at the live lane still
  escapes the scratch clone. The landed ledger's 78 argvs were checked for this: 0 carry an absolute path
  or a `<placeholder>`, so the landed ledger is clean, but the counter would not catch it.
- The frozen `c2-before-head.txt` receipt and the frozen 12-case selftest receipt are re-derivable from
  `a34838f`; the current receipts (`cases=50`) live in the tree and the claims file records A1/A2 with the
  before-state re-derivable. **This seat verified the frozen before-state reproduces exactly**: running the
  frozen counter against a clean clone of the base tip `536925b…` yields
  `ROWS registry=75 ledger=0 missing=75 …` and `PREDICATE R53-C2 fail`, exit 1 — byte-identical to
  `.ufo/waves/round-53/claims/c2-before-head.txt`.
- **Not verified here (out of this seat's scope):** the C1 side and any scored run of the committed ledger
  after N1 is repaired. The full-tree run this seat *did* complete is on `1ebf61f` (77 rows, pre-A2); it is
  reported in §5, not on the current 78-row tip.

## 5. Full-tree run and isolation (measured)

**Full run** on a clean clone of `1ebf61f` (the commit that carries the ledger; 77 rows; pre-A2), `--jobs 6`,
wall time 437.7 s. Verbatim output: `.ufo/waves/round-53/w1/C2RevCounter/full-run.txt`. The wrapper did not
record the raw exit; `main()` returns 1 on `PREDICATE R53-C2 fail`, so the exit is 1 by the counter's own code.

- `ROWS registry=77 ledger=77 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0
  bad_table_lines=0 headings=1 row_set_pinned=ok`; `SOURCE rev=1ebf61f… clean=yes lane_rev_equal=yes`.
- `RUN executed=77 timeout=0 mismatched=17 evidence_missing=1`; `TIPSTATE declared_green=49 declared_red=28
  observed_green=64 observed_red=13`; `PREDICATE R53-C2 fail`.
- The 17 mismatches and their causes are in N1 (§2).

**Isolation** (`isolation-run.txt`): the seven red->green rows re-run with `--jobs 7` (one fresh clone each, no
prior row on its worker): `mismatched=7`, all observed 0. This rules out row-to-row contamination as the cause
of those seven declarations; it does not rule it out for the other ten, which were not isolated.

**Current tip (78 rows, A2):** `--dry` on the lane tree gives `ROWS registry=78 ledger=78 … row_set_pinned=ok`,
`ARGV entry=74 selftest=4 help=0`, exit 0 (static legs only). No scored run of the current tip was made: the
working-tree ledger is uncommitted and differs from the committed one in 16 rows (N1), so a run of it would
measure an unlanded artefact.

**Measured cost, for the scheduler:** the registry's slowest declared rows took 452 s (`round37-c1-mutants`),
249 s (`round39-c1-audit`, `round39-c1-mutants`) and 140 s (`round42-c2`) on a loaded host. A full scored run
at `--jobs 6` is ~7–8 minutes wall; the default `--timeout 900` is close to the slowest row, so a loaded host
will time rows out.

## 6. Files produced

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2RevCounter.md` — this report.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2RevCounter/` — the probe
  scripts used above (`probe1.py` … `probe13.py`), `frozen_c2.py` (the frozen artifact extracted with
  `git show a34838f:plans/round53_c2_tipstate.py`), `patched_c2.py` (a scratch copy with the F1 two-line repair;
  not a landing edit), `full-run.txt` (verbatim full run), `isolation-run.txt` (verbatim isolation run),
  `ledger-committed-1ebf61f.json` (the committed ledger, `git show 1ebf61f:`), and
  `ledger-working-vs-committed.txt` (the 16 changed rows).
- No file outside those two paths and `/fast/scratch/hyaku/kengaku-r53/C2RevCounter/` was written or
  modified; the lane tree was only read. The scratch directory is removed before yield.

**Tooling:** no package was installed for this seat — the review used the system `python3` (3.14) and
`git` only, both already present. No `pacman`/`uv`/`npx` transaction was performed, so nothing to record
under the tooling directive.
