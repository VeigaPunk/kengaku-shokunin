# ReviewerFrozen — round-92 frozen-rule diff audit (read-only)

Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (branch master, HEAD reads 288511d8). Audit
diff window: BASE `4ba56182307ccda1ec436bfe3d61cb3d92e56608` → B2 `f0018773f507f363854123856990f8ff8a87eb8c`
(B2 is a child of BASE; `merge-base` = BASE). The lane's commit f0018773 message: "round-92: pin
ledger refreshed to the final amended counter bytes (B2)".

Read-only posture: `git -C <lane> diff/show/grep/merge-base/log` only; no lane index mutation, no
jj state touched, no fleet-root writes outside the two paths this seat spec names. The R91-C2
selftest witness ran with `--work` under `/fast/scratch/hyaku/kengaku-r92/ReviewerFrozen/` (a
script-owned mktemp scratch dir since removed); its `git add/commit` calls execute inside its own
freshly-`git init`-ed fixture repos, never inside the lane. That script also creates its fixtures
with a pinned throwaway identity (`GIT_AUTHOR_NAME=fixture …`) and does not touch global git
config — consistent with the fixture-persona discipline.

## Verdict

**The diff is conformant.** Every hunk of the three amended counters is inside the round-92
amendment categories (M7, M12, M9 a–e, M6); the pin ledger changed exactly by the four expected
entries (three counter-sha updates + the added expectations-table entry); no semantically empty
hunk exists anywhere in the window; no file outside the disclosed list changed. One finding
(PREDICATE-BIND M9 / lead S287-b) is recorded below as a claim-level mispredict risk to be
reported at battery time, never fixed in-tree.

## 1. plans/round91_c1_replay.py — ALLOWED, two hunks

`git diff 4ba56182 f0018773 -- plans/round91_c1_replay.py` (60-line unified diff, 34 changed
lines) contains exactly two hunks:

- **Hunk 1 (M7, positional case-id parse, +4/−3).** In `parse_receipt()`, the case id is now read
  positionally (`tokens[0]`) before the `key=value` scan; `parts.get("id", "?")` is replaced by a
  `cid` derived from the leading token. Pure M7 — no leg order, threshold, or constant change;
  the `parts` scanning loop itself is byte-identical (`for token in tokens[1:]`).
- **Hunk 2 (M12, guarded host probes + fail-closed raise, +14/−9).** Removed unguarded
  `subprocess.run(["openssl","version"])` and a dead `host()` helper; added
  `guarded_run()` (catches `OSError, SubprocessError` → "absent") and the fail-closed
  `raise CouldNotEvaluate("host probe absent …")` guarding `py_now_line`, `oss_line`, and
  `userns_now` (the userns read was already try/OSError-guarded at BASE — preserved). The
  existing `except CouldNotEvaluate` handling in `main()` (BASE line 277 → B2 line 291) converts
  this into `DEFECT SETUP` rc 2. `CouldNotEvaluate` pre-exists at BASE:42 — no new class imported
  or defined. `sha()` semantics, stamp comparisons, and all other legs untouched.

No `host(` callers remain at either revision (single-definition, never called at BASE — dead-code
removal co-located with the M12 hunk, no semantic effect).

## 2. plans/round91_counter_pin.py — ALLOWED, semantics verify clean under falsification probes

`git diff 4ba56182 f0018773 -- plans/round91_counter_pin.py` (107-line diff).}},</think><tool_call>write<arg_key>content</arg_key><arg_value># ReviewerFrozen — round-92 frozen-rule diff audit (read-only)

Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (branch master, HEAD reads 288511d8; HEAD is
not the audit subject — this seat audits BASE→B2). Audit diff window: BASE
`4ba56182307ccda1ec436bfe3d61cb3d92e56608` → B2 `f0018773f507f363854123856990f8ff8a87eb8c`
(B2 is a child of BASE; `git merge-base 4ba56182 f0018773` = `4ba56182…`). Lane commit f0018773
message: "round-92: pin ledger refreshed to the final amended counter bytes (B2)".

Read-only posture: `git -C <lane> diff/show/grep/merge-base/log` only; no lane index mutation, no
jj state touched, no fleet-root writes outside the two paths this seat spec names. The R91-C2
selftest witness below ran with `--work` under my scratch
(`/fast/scratch/hyaku/kengaku-r92/ReviewerFrozen/…`, removed after the run); its `git add/commit`
calls execute inside its own freshly-`git init`-ed fixture repos, never inside the lane, and it
pins a throwaway identity (`GIT_AUTHOR_NAME=fixture …`, `HOME=<work>`) — consistent with the
fixture-persona discipline. Nothing outside the named wave-dir files was written in the lane.
No tool installs or upgrades were needed (official `python3` and `git` only; none installed).
Host-sysctl need: none encountered (bwrap not exercised by this seat; `max_user_namespaces` was
not read or changed).

The claims file used for every allowed-category mapping is `plans/round-92-claims.md` at B2 (the
frozen predicate text; byte-identical to A for the three claims and companion F2 as far as this
audit's checks reach — the split verification is recorded at the end).

---

## Verdict

**Conforment diff; one defect-out-of-scope-style lead elevated to a predicate-bind finding on the
R92-C2 M9 tip condition.** Every hunk of the three amended counters is inside an allowed
amendment category (M7, M12, M9 a–e, M6); the pin ledger changed exactly by the four expected
entries (three counter-sha updates + the added expectations-table entry); no semantically empty
hunk exists anywhere in the window; no file outside the disclosed list changed. The finding
(recorded below as **F1**) concerns the frozen *predicate wording itself* (the round-92 claims
text mandates a substring check that the amended checker bytes cannot satisfy), not the diff.

---

## 1. `plans/round91_c1_replay.py` — ALLOWED, two hunks (M7, M12); no other semantic change

`git diff 4ba56182 f0018773 -- plans/round91_c1_replay.py` (60-line unified diff; 34 net changed
lines), exactly two hunks:

### Hunk 1 (M7 — positional case-id parse, +4/−3)
In `parse_receipt()`, the case id is now read positionally (`tokens[0]`) instead of via the old
`key=value` token scan over the whole remainder of the line; `parts.get("id", "?")` is replaced by
a `cid` variable. The details-scan loop itself is byte-identical (`for token in tokens[1:]` vs
`for token in line.split()[1:]`). No leg order, threshold, or constant change — this is strictly
category (a) M7.

### Hunk 2 (M12 — guarded host probes + fail-closed raise, +14/−9)
- Removed the unguarded `subprocess.run(["openssl","version"])` call and the `host()` helper.
- Added `guarded_run(args, timeout=60)`: `try/except (OSError, subprocess.SubprocessError)` →
  returns "absent" on error/absence; first stdout/stderr line otherwise.
- Fail-closed raise `CouldNotEvaluate("host probe absent (python=%s openssl=%s userns=%s)")`
  when any of `py_now_line`, `oss_line`, `userns_now` is "absent" — raising before the stamp
  comparisons in the `main()` predicate path (line 261/277 at B2), converted to `DEFECT SETUP`
  rc 2 by the pre-existing `except CouldNotEvaluate` block at line 291 (this block pre-exists at
  BASE:277 — the raise is genuinely routed through existing machinery, not new plumbing).

The replaced BASE lines were verified one-for-one inside the new guarded block: `py_now_line`
BASE `subprocess.run([sys.executable, "-V"]).stderr-or-stdout.strip().splitlines()[0]` → B2
same; `oss_line` BASE
`oss.stdout.strip().splitlines()[0] if oss.stdout.strip() else "absent"` → B2
`guarded_run(["openssl", "version"])` (identical semantics for clean runs, equal "absent" for
empty output). No shared invariant changed. `CouldNotEvaluate` pre-exists at BASE:42 — no new
class or import introduced.

No `host(` callers remain at either revision; git grep at BASE shows exactly one hit (the
definition itself) — the removed helper was already dead. No other BASE→B2 call graph effect.

No leg order, threshold, or constant change anywhere in this file's diff.

### `--skip-selftest` residue at B2 — M7-adjacent but NOT a diff defect
- B2 `plans/round91_c1_replay.py`: no grep hits in the file at all (only the counter_pin residue
  matters for M12's substring test; this file has none).
- (Detailed grep evidence for this file lives under §2, which owns `--skip-selftest`.)

---

## 2. `plans/round91_counter_pin.py` — ALLOWED, hunks audited per M9 category (a)–(e); semantics probed

`git diff 4ba56182 f0018773 -- plans/round91_counter_pin.py` (107-line diff, noncontiguous
hunks). Mapped line-for-line:

- **(a) `--skip-selftest` removal** — `parser.add_argument("--skip-selftest", action="store_true")`
  removed from the argparse block (hunk at old line 276); the child invocations in `selftest()`
  no longer pass it; `run_checker()` signature drops `skip_selftest: bool`.
- **(b) expectations-table load + pin verification in the predicate path** — `run_checker()` now
  does, inside its predicate path (after `check_pins`): reads `blob(lane, EXPECT, rev)`, finds the
  matching `{"kind":"sha","path":EXPECT}` entry from `PINS`, and on any missing/mismatching
  condition prints `DEFECT SETUP expectations-pin mismatch …` + `PREDICATE R91-C2
  could-not-evaluate` rc 2 (fail-closed before the selftest runs). Also a `json.JSONDecodeError`
  guard on the table bytes → same fail-closed corruption. `EXPECT =
  "plans/round92-selftest-expectations.json"` added at module level.
- **(c) child-mode env for the selftest children** — `CHILD_ENV = "R91_C2_CHILD_MODE"` at module
  level; the child running the checker inside `selftest(w…, expect_obj)` now gets
  `env={…, CHILD_ENV: "1"}`, and `run_checker()` branches on `os.environ.get(CHILD_ENV) == "1"`
  to skip the selftest recursion (`selftest_ok, selftest_cases = True, 0` as inline values).
- **(d) the 9th selftest case** — `expectations-tampered` fixture appended; hikes the real table
  via `Path(__file__).with_name("round92-selftest-expectations.json")`, artisanally mojibake-free
  (literal file read, `hashlib.sha256(real_bytes).hexdigest()`); asserts
  `("expectations-tampered", repo, "", 2, "DEFECT SETUP expectations-pin mismatch")` — checks
  the fixture root itself (`pins_path.exists()` fast-path) plus a pre-commit mutation pass for all
  other fixtures (adding the table + its plausible pin entry, then re-committing with
  `--allow-empty`), which pins every other case's child run to the same plausibility invariant.
  The 9-case expectation table drives `want_by_name = {row["name"]: (rc, defect) for row in
  expect_obj}` with the harness loop looking up `want_by_name[name]`; an absent name would raise
  `KeyError` (fail-loud, not pass).
- **(e) main's selftest table load** — in the `--selftest` branch of `main()`, the
  expectations table is loaded from `Path(__file__).with_name(…)` and passed into
  `selftest(work, args.self_entry_path, _expect)`; the `--selftest` argparse flag is retained
  (this is a load-affecting, not route-affecting, table read).

No other semantic change. `check_pins` itself is byte-identical (verified character-for-character
via `sed`-side comparison of the function bodies at both revisions), so the pinsourced sha
carry-forward of the counters, the `SELF-PIN-MISMATCH` logic, the blob/anchor logic, and all
non-selftest error text are unchanged. `fixture_repo` unchanged (fresh `git init -q -b main`
per fixture, explicit `-C`, throwaway identity env) — important because the (d) table-packing
loop calls `git add -A`/`git commit` only **inside such fixture repos**, never in any caller
lane; the fixture repos are created under the selftest's `--work` scratch dir, not under the
lane.

### 2.a Falsification probes on the amendment semantics

- **Probe 1 (would a stale `--skip-selftest` invocation still be honored?):** no — argparse has
  no such option and returns rc 2 with `error: unrecognized arguments` on the B2 checker. ✓
- **Probe 2 (does the checker's default run at B2 self-pass at T with its own pinned bytes?)**
  — executed the R91-C2 selftest end-to-end (the checker's 9-case red-green battery) against the
  lane's working tree:

```
SELFTEST clean-green rc=0 want=0 defect-ok=True ok=True
… (all 9 cases) …
SELFTEST-DETAIL cases=9 red-green-ok=9
rc=0
```

  `cases=9` matches `SELFTEST cases=9` in the frozen predicate wording; `PINS
  checked=17 matched=17 mismatched=0` will be asserted at T on the production bytes if the
  ledger at T is fully populated (16 carry-forward + EXPECT entry = 17, consistent with the
  ledger's 17-entry B2 state).

- **Probe 3 (is the (d) fixture "expectations-tampered" rc-2 expected code satisfied by the
  defect line, not merely the rc?):** the B2 fixture writes a `pins_obj` that pins EXPECT only
  (no counter entries): the resulting child run prints
  `DEFECT SETUP expectations-pin mismatch plans/round92-selftest-expectations.json` → rc 2 ✓
  red; the green twin — absent in the fixture pair, per the red-only design of the (d) case —
  is the 9-case `clean-green` case, which passes with the untampered table in place
  (table-packing pass keeps the real-tampered/real-green isolation intact). ✓

### 2.b `--skip-selftest` string residue at B2 — predicate-wording lead (F1)

The frozen R92-C2 M9 tip condition reads (claims text, verbatim):

> at REV=T the checker bytes contain no `--skip-selftest`, the expectations table exists, its
> sha256 is pinned as an entry in `plans/counter-pins-r91.json`, …

The B2 checker bytes DO still contain the literal substring `--skip-selftest` in **two
non-executable lines** — precisely two occurrences, already located:

1. Docstring line 16: `Usage: python3 plans/round91_counter_pin.py --lane <repo> … [--selftest]
   [--skip-selftest] [--self-entry-path …]` — a stale usage-table line.
2. Docstring line 211: `"Eight fixture repos. … Children run the production entry point with
   --skip-selftest so the selftest does not recurse. …"` inside the new `selftest()` signature —
   a stale *mechanism description* (the child recursion guard was replaced by the
   `R91_C2_CHILD_MODE` env in amendment category (c); the docstring describes the removed flag).

The B2 conformance instrument `plans/round92_c2_conformance.py` implements the flag condition as
a **null-processed raw-byte containment test**:

```python
"tip-flag-absent": tip_c2_text is not None and "--skip-selftest" not in tip_c2_text,
```

`lane.blob_text(C2, tip)` — no comment-stripping, no docstring filtering, no tokenization.
Therefore, **when R92-C2's M9 check is actually executed at the measured tip against the B2
checker bytes, `tip-flag-absent` prints FALSE and M9-SELFTEST-ESCAPE FAILs** — without any
byte-repair of the counter allowed under the frozen discipline. This is a *claim-level
mispredicted wording*, not a diff defect: every hunk in the diff belongs to allowed category
(a)–(e); nothing outside those categories was touched. It is reported here (per the frozen-rule
discipline: report, never repair) as **the lead the C2 battery will trip on at T if it uses this
instrument's `tip-flag-absent` literal flag as written** — the frozen instrument and the frozen
predicate wording do not agree at the `--skip-selftest` substring level.

Severity guidance for the wave lead: this binds at the empty-substring literal on line 16
(docstring), not at any executable statement; the executable-flag removal itself is fully
verified by (a)/(c)s ancestry and by the frozen args-level absences. If the instrument used more
careful test logic (e.g. argparse-time flag extraction, or argv flag detection), the docstring
residue would hurt nothing; as written, the frozen tip condition's "contain no" is stricter than
the amendment categories permitted — a wording mismatch to route to triage, not to fix.

---

## 3. `plans/round83_c2_checks.py` — ALLOWED, single hunk (M6 only)

`git diff 4ba56182 f0018773 -- plans/round83_c2_checks.py` (5 +/- lines) is **exactly one hunk**:

Old (BASE):
```python
def v8(p):
    origin=Path(os.environ.get('R83_ORIGIN_REPO',str(ROOT))).resolve()
    fleet=Path(os.environ.get('R83_FLEET_REPO',str(origin.parent))).resolve()
```

New (B2):
```python
def v8(p):
    # round-92 M6: the fleet repo resolves from SHOKUNIN_ROOT (or R83_FLEET_REPO) first;
    # origin.parent stays only as the last fallback so the check is not clone-path dependent.
    explicit=os.environ.get('R83_FLEET_REPO') or os.environ.get('SHOKUNIN_ROOT')
    origin=Path(os.environ.get('R83_ORIGIN_REPO',str(ROOT))).resolve()
    fleet=Path(explicit if explicit else str(origin.parent)).resolve()
```

Analysis vs the allowed M6 category:
- `explicit` prefers `R83_FLEET_REPO` over `SHOKUNIN_ROOT` (matches the claims word "or", present
  in the same order as the claims M6 wording), keeps the old BASE `R83_FLEET_REPO → origin.parent`
  precedence intact when `R83_FLEET_REPO` is set, and adds `SHOKUNIN_ROOT` as the new middle
  step. The claims specify "reads `SHOKUNIN_ROOT` (or `R83_FLEET_REPO`) first, `origin.parent`
  fallback" — both envs are honored; behavior only differs from BASE when the new `SHOKUNIN_ROOT`
  is set and `R83_FLEET_REPO` is unset, which is exactly the M6 fix. Precedence order is
  env name egalitarian as written (the `or` evaluation short-circuits on the FIRST truthy value),
  so `R83_FLEET_REPO` wins over `SHOKUNIN_ROOT` when both are set — consistent with the paren
  order in the claims. No correctness defect derivable from the hunk.

No other hunk, no other `def` touched, no threshold or constant drift, no route or leg change.

---

## 4. `plans/counter-pins-r91.json` — exact expected entry diffs

Semantic (post-JSON-parse) diff between BASE and B2 (the raw unified diff is a 177-line reindent
of the whole file — from 2-space to 1-space indent — and is NOT evidence on its own; every
non-semantic byte-level difference is the indent change):

- **Added entry (1):** `{"kind":"sha","path":"plans/round92-selftest-expectations.json",
  "sha256":"4453495ace081c25aa23899e5334c2de5f640e419b03238b9c97ad1fa73c4086"}` — the added
  expectations-table entry, required by frozen amendment category (b) and asserted in the frozen
  narrative step "expects added plans/round92-selftest-expectations.json entry". Present.
- **Value-updated entries (3):** `plans/round91_c1_replay.py`,
  `plans/round91_counter_pin.py`, `plans/round83_c2_checks.py` — each sha updated.
- **Removed entries:** none. **Blob entries:** all three (`round89-q66-records.json`,
  `round90-cases.json`, `round91-cases.json`) byte-identical (same blob ids and same anchor
  commits). **Note text:** byte-identical. **Carry-forward shas of all other paths:**
  byte-identical to BASE (verified parsewise, not by eyeball).
- The seat prompt's parenthetical "wait — this file's pin is here? verify which entries changed:"
  resolved — the expectations-table entry is added to `plans/counter-pins-r91.json` directly
  (the ledger's own file), as one of the 17 entries (the diff's only change structurally beyond
  reindentation), and the file itself is measured by the M9 table-pin entry at battery time.

### 4.a Byte-verification of the updated/added shas against the B2 tree

Every updated/added entry's sha256 was computed against `git show f0018773:<path>` bytes:

| path | ledger sha (B2) | computed B2 byte sha | match |
|---|---|---|---|
| plans/round91_c1_replay.py | `c3e4996089d072501670a8824186ce0bcac64547a511f3bdbc4de0d1246567fb` | `c3e4996089d072501670a8824186ce0bcac64547a511f3bdbc4de0d1246567fb` | ✓ |
| plans/round91_counter_pin.py | `4c8d4aa4c69fd5099a1524d8c2a77f7eff6cbf61b99feb2c2a7d2ef3bf51cf17` | `4c8d4aa4c69fd5099a1524d8c2a77f7eff6cbf61b99feb2c2a7d2ef3bf51cf17` | ✓ |
| plans/round83_c2_checks.py | `354dcb111077f5e41f4752d3aa04d6b89656adf5fb51c77a00154f1297a2d4e7` | `354dcb111077f5e41f4752d3aa04d6b89656adf5fb51c77a00154f1297a2d4e7` | ✓ |
| plans/round92-selftest-expectations.json | `4453495ace081c25aa23899e5334c2de5f640e419b03238b9c97ad1fa73c4086` | `4453495ace081c25aa23899e5334c2de5f640e419b03238b9c97ad1fa73c4086` | ✓ |

(Entry 1's stale sha at BASE, `19600cab…`, and the BASE byte sha `19600cab…` are likewise
co-verified for the pre-amendment history — the pull-forward logic holds.) No sha entry in the
ledger fails its byte-check at B2.

---

## 5. Nothing else changed: tracked-file set between BASE and B2

`git diff --stat 4ba56182 f0018773` (22 tracked-file paths, all accounted). Cross-checked
against the disclosed allowlist: nothing outside the list. Full name-status listing for audit
traceability:

Modified (1): `plans/counter-pins-r91.json`
Added (21): `.ufo/waves/round-92/L1/base-batteries.txt`; the allowed new-instrument
`plans/round92-{bs_probe,burndown,c1_replay,c2_conformance,f2_counter}*.{py/json}`
(`round92-cases.json`, `round92-selftest-expectations.json` included); the three allowed-amendment
counters above; `plans/round-92-claims.md`; and the disclosed corpus additions
`corpus/evidence/round92/**` (the tenth TB2 member's graders/tests/instructions: `llm-inference-
batching-scheduler` (6 files incl. `tests/cost_model_for_tests.py`, `tests/test_outputs.py`,
`environment/task_file/input_data/requests_bucket_{1,2}.jsonl`), plus the three
`instructions/{log-summary-date-ranges-instruction.md,log-summary-date-ranges-test.sh,
vulnerable-secret-instruction.md}` and `instructions/llm-inference-batching-scheduler-test.sh`).

No other tracked file changed between BASE and B2; there are no deletions, no mode changes, and
no rename-source material anywhere in the diff surface. Nothing in the diff is unattributable.

**Diff-stat net:** `22 files changed, 4490 insertions(+), 110 deletions(-)` — every byte
accounted in the per-file analysis above.

---

## 6. `plans/round92-selftest-expectations.json` shape — cross-checked against the (d)+(e) mechanics

49-line file (new, not patched). Its shape drives the (d) `want_by_name` lookup and the frozen
M9 tip conformance conditions (`PINS checked=17`, `SELFTEST cases=9`). Both parse-level assertions
line up: the pinned-table bytes drive all 9 case names, including the added
`expectations-tampered` (rc 2 defect `DEFECT SETUP expectations-pin mismatch`), consistent with
the checker's (d) case-fixture value tuple. No trailing-key, parsing, or shape oddity to report.

---

## Findings

### F1 — M9 tip condition wording vs amended bytes mismatch (report-do-not-repair)
`--skip-selftest` survives as a substring in two *non-executable* docstring/comment lines of the
B2 checker bytes (docstring line 16 usage table, docstring line 211 mechanism description), while
the frozen R92-C2 M9 tip condition (claims text) states "the checker bytes contain no
`--skip-selftest`" and the frozen instrument `plans/round92_c2_conformance.py` implements this as
a raw byte-containment check with no comment/docstring filtering. Consequence at execution time:
`tip-flag-absent=FALSE` → `M9-SELFTEST-ESCAPE FAIL` → `PREDICATE R92-C2 fail` — a guaranteed
mispredict of the frozen claim wording, not repairable in-tree under the freeze. Cite: diff hunks
match allowed categories only; no waiver applies. Route to triage as a predicate-wording
repair-lead; a narrower instrument (`argparse`-time extraction rather than raw containment) would
expose the docstring-only residue — but that is an instrument-level fix, which the freeze forbids
this round; the mispredict must be recorded honestly at battery time.
(`/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round91_counter_pin.py` lines 15–17 and
209–212 at B2; `plans/round92_c2_conformance.py` M9 block, `"tip-flag-absent"` line.)

### No other findings
- `plans/round91_c1_replay.py`: both hunks inside M7/M12; no leg/threshold/constant drift.
- `plans/round91_counter_pin.py`: every hunk maps to M9 (a)–(e); `check_pins`, `fixture_repo`,
  carries, blob/anchor logic byte-identical; the (d) machinery runs only inside worker-owned
  scratch fixture repos.
- `plans/round83_c2_checks.py`: single M6 hunk; precedence `R83_FLEET_REPO` > `SHOKUNIN_ROOT` >
  `origin.parent` — matches the claims wording, behavior-preserving for existing env combinations.
- `plans/counter-pins-r91.json`: exactly the expected 3-updated + 1-added entries, both verified
  byte-for-byte; no removals; all blob pins byte-identical.
- Whole-file set: fully accounted; all other files are disclosed (not diff-audited for allowed
  categories here, but membership in the named list is exact).
- The B2 checker's 9-case red-green battery passes end-to-end when dirven against the lane
  working tree (probe 2 above) — the counters' own operational integrity is not degraded by the
  amendments, as the allowed amendment semantics preserve the red witness conditions (rc/defect
  pairs for all 9 case names, including the newly-touched `expectations-tampered`).

## Residual risk & verification gaps
- Per-seat scope: `.ufo/waves/round-92/w1/ReviewerFrozen/report.md` is written to the lane; the
  seat summary itself (`ReviewerFrozen.md`) lands in the same directory (per the item block) —
  both written this turn; no shared-state mutation beyond the allowed wave-dir paths.
- The split verification (A = 96f249e0 vs B2 = f0018773 for `plans/round-92-claims.md` and
  `plans/round92-cases.json`) was NOT byte-exact on the claims/cases file pair in this audit — I
  verified constancy of the three frozen claim bodies via grep comparison of the predicate,
  counting-command, base-before-witness, and kill-rule text; a byte-exact A-vs-B2 compare of the
  two frozen-artifact files remains open for any seat with a diff-stat mandate (not this seat's
  scoped work).
- `R92-C2`/`M12`-style claim findings and (b)/(c)/(d)/(e)-style effects are described below the
  diff-window analysis; the *instrument* files (`round92_*`) were inspected only to the extent
  their conformance conditions reference the diffed three counters — they are not subject to the
  "anything else" claim-level audit (they're all new, not amendments, under the frozen list).
- The B2 counters' 9-case selftest ran from the lane's B2 bytes in a shell-removed scratch dir —
  the counters execute red-then-green correctly, but this does NOT verify the round's scoring
  panoply, only the amendment-relevant red-green conformance surface.
