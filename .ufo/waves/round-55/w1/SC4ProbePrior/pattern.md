# Established TB2-grader probe pattern (extracted from three lane exemplars)

Seat `SC4ProbePrior`, kengaku round 55 wave 1. **Read-only.** Sources, all in the lane repo
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`:

| exemplar | role | cases | receipt (committed) |
|---|---|---|---|
| `plans/build_pmars_probe.py` (r38 C2) | oldest, single-run | 22 | `corpus/evidence/round38/build-pmars-probe.txt` |
| `plans/password_recovery_probe.py` (r45 C2) | two-run (`regrade`) | 16 | `corpus/evidence/round45/password-recovery-probe.txt` |
| `plans/polyglot_c_py_probe.py` (r46 C3) | two-run + `--stage-check` shape parse | 18 | `corpus/evidence/round46/polyglot-c-py-probe.txt` |

Purpose: a checklist E5's `plans/round55_c3_chess_probe.py` can be checked against line by line.
§6 lists the places the current draft **deviates** from the pattern; each is evidence-backed
(commands and exit codes in §7).

---

## 1. The bwrap flag pattern (exact lines)

All three exemplars build the sandbox argv in a module-level function named `sandbox_argv`,
in this fixed order. `plans/password_recovery_probe.py:213-226`:

```python
213: def sandbox_argv(cap, work):
214:     argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
215:             "--ro-bind", "/usr", "/usr"]
216:     for link in ("/bin", "/sbin", "/lib", "/lib64"):
217:         if os.path.islink(link):
218:             argv += ["--symlink", os.readlink(link), link]
219:     argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
220:              "--ro-bind", str(work / "zeros.bin"), "/dev/urandom",
221:              "--bind", str(work / "app"), "/app", "--ro-bind", str(work / "tests"), "/tests", "--dir", "/pub"]
...
224:     argv += ["--ro-bind", str(work / "seed.sh"), "/seed.sh", "--ro-bind", str(work / "recipe.sh"), "/recipe.sh",
225:              "--ro-bind", str(work / "harness.py"), "/harness.py", "--chdir", "/app"]
226:     return argv
```

`plans/polyglot_c_py_probe.py:349-363` is the same function, byte-identical in the shared part
(`--unshare-net --unshare-pid --unshare-ipc --die-with-parent --new-session`, `--ro-bind /usr /usr`,
the `/bin /sbin /lib /lib64` symlink loop, `--ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp`,
`--chdir /app` at the end), differing only in the per-task binds (`--dir /pub --dir /tpl`,
`--bind work/app /app`, `--ro-bind work/tests /tests`).

`plans/build_pmars_probe.py:239-252` is the same again, with the pmars-specific binds:

```python
240:     argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
241:             "--ro-bind", "/usr", "/usr"]
242:     for link in ("/bin", "/sbin", "/lib", "/lib64"):
243:         if os.path.islink(link):
244:             argv += ["--symlink", os.readlink(link), link]
245:     argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
246:              "--ro-bind", str(work / "ulb"), "/usr/local/bin",
247:              "--ro-bind", str(work / "ulsb"), "/usr/local/sbin",
248:              "--ro-bind", str(work / "app"), "/app",
249:              "--dir", "/tests", "--ro-bind", str(cap / "test_outputs.py"), "/tests/test_outputs.py",
250:              "--ro-bind", str(work / "harness.py"), "/harness.py",
251:              "--chdir", "/app"]
252:     return argv
```

**The invariant set (all three):** `--unshare-net --unshare-pid --unshare-ipc --die-with-parent
--new-session`; `--ro-bind /usr /usr`; the four-link symlink loop; `--ro-bind /etc /etc --proc /proc
--dev /dev --tmpfs /tmp`; the grader directory bound **read-only** at `/tests`; `/app` bound
**writable** (`--bind`, not `--ro-bind`); `--chdir /app` last.

Constants: `BWRAP = "/usr/bin/bwrap"` (`password_recovery_probe.py:77`, `polyglot_c_py_probe.py:84`,
`build_pmars_probe.py:59`); `PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"`
(`:80`, `:87`, `:62`). Sandbox env is a fixed dict, e.g. `password_recovery_probe.py:229-230`:

```python
229: ENV = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1",
230:        "PYTHONDONTWRITEBYTECODE": "1"}
```

(`polyglot_c_py_probe.py:366-367` adds `"TMPDIR": "/tmp"`.)

**Grader execution inside the sandbox** — the exemplars never shell out to pytest; they write a
tiny pytest-free harness and call the captured test functions directly, mapping each to one
letter. `password_recovery_probe.py:175-205` (harness) and `:233-236`:

```python
233: def harness(cap, work, mode):
234:     p = subprocess.run(sandbox_argv(cap, work) + ["/usr/bin/python3", "/harness.py", mode],
235:                        env=ENV, capture_output=True, text=True, timeout=1800)
236:     return p.returncode, p.stdout
```

The harness prints `TEST <name> P` / `TEST <name> F` / `TEST <name> F error=<ClassName>`
(`password_recovery_probe.py:195-205`, `build_pmars_probe.py:174-187`), where `AssertionError` → `F`
and **any other exception → `F` with its class named** (`build_pmars_probe.py:185-186`:
`except Exception as e: print("TEST " + name + " F error=" + type(e).__name__)`).
The grader module is imported from the read-only `/tests` copy via `importlib`
(`password_recovery_probe.py:191-193`, `build_pmars_probe.py:176-178`).

---

## 2. How the frozen case table and its predictions are embedded

Three module-level constants, always in this order, always **above** `main()`:

* `PINS` — capture digests, `password_recovery_probe.py:69-74`, `polyglot_c_py_probe.py:73-81`,
  `build_pmars_probe.py:55-58`.
* `TAGS` — a dict mapping a requirement tag to the instruction line that states it,
  `password_recovery_probe.py:83-92`:
  ```python
  83: TAGS = {
  84:     "forensic": "instruction.md:1",       # recover the PASSWORD from the deleted file
  85:     "write-file": "instruction.md:9",     # write ... to the file: /app/recovered_passwords.txt
  ...
  ```
  same in `polyglot_c_py_probe.py:90-107` and `build_pmars_probe.py:66-73`.
* `CASES` — a list of a **frozen dataclass**, one instance per case
  (`password_recovery_probe.py:102-109`, `polyglot_c_py_probe.py:172-180`,
  `build_pmars_probe.py:92-100`):
  ```python
  102: @dataclasses.dataclass(frozen=True)
  103: class Case:
  104:     cid: str
  105:     predicted: str          # one letter per TESTS entry; '-' = earlier test already failed
  106:     violates: tuple
  107:     requirement: str
  108:     recipe: str = ""        # bash run in /app after the image seed, before grading
  ```
  `TESTS` (the ordered tuple of captured test-function names) sits with the other constants:
  `password_recovery_probe.py:79` `TESTS = ("test_recovery_file_exists", "test_password_match")`,
  `polyglot_c_py_probe.py:86` `TESTS = ("test_fibonacci_polyglot",)`,
  `build_pmars_probe.py:61` (four pmars tests).

**The prediction is a per-test letter string, not a boolean.** `"P"` = that test returns,
`"F"` = it raises, `"-"` = never reached because an earlier test already failed
(`password_recovery_probe.py:105`). `overall()` collapses it to pass/fail
(`password_recovery_probe.py:279-281`):

```python
279: def overall(letters):
280:     return "pass" if letters == "P" * len(TESTS) else "fail"
```

Each case also carries `violates` (a tuple of `TAGS` keys — which instruction requirements the
case does *not* satisfy) and a one-line `requirement` prose explaining what the case is.

**The table is frozen twice over:** (a) in source, as the dataclass list; (b) as a committed
**dry table receipt**, produced by `--dry` before the first graded run and byte-compared later.
`password_recovery_probe.py:299-308` is the `--dry` printer; the committed freeze receipt is
`corpus/evidence/round45/password-recovery-dry-cases-freeze.txt` and a fresh `--dry` today is
byte-equal to it (verified, §7). Same for r46
(`corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`) and r38
(`corpus/evidence/round38/build-pmars-dry-cases-freeze.txt`).

**Table self-validation before any case runs** (malformed table ⇒ exit 2):
`password_recovery_probe.py:293-298`:

```python
293:     ids = [c.cid for c in CASES]
294:     if len(set(ids)) != len(ids) or any(not re.fullmatch(r"[a-z0-9_-]+", i) for i in ids) \
295:             or any(t not in TAGS for c in CASES for t in c.violates) \
296:             or any(len(c.predicted) != len(TESTS) or set(c.predicted) - {"P", "F", "-"} for c in CASES):
297:         print("SETUP duplicate or malformed case id, unknown tag or malformed prediction", file=sys.stderr)
298:         return 2
```

(p46 adds the `regrade` and `expect` checks at `:443-450`; pmars checks ids and tags at `:287-290`.)

---

## 3. How observed vs predicted and mismatches are printed

**Per case, one `CASE` line** carrying the prediction, the observation, both letter strings, an
explicit `match=yes|NO`, the violated tags and the requirement prose.
`password_recovery_probe.py:352-355`:

```python
352:             print(f"CASE {c.cid} predicted={overall(c.predicted)} observed={obs} tests={l1}"
353:                   f" predicted_tests={c.predicted} match={'yes' if match else 'NO'}"
354:                   f" regrade={'same' if l2 == l1 else 'DIFF:' + l2}"
355:                   f" violates={','.join(c.violates)}{' ' + n1 if n1 else ''} -- {c.requirement}")
```

`polyglot_c_py_probe.py:514-517` is the same shape; `build_pmars_probe.py:340-342` is the same
minus the `regrade=` field (pmars does not re-grade).

**The verdict is derived from the letter string, not from a boolean:**
`password_recovery_probe.py:261-277` parses `TEST ` lines into letters and
`build_pmars_probe.py:333-335` does the same for pmars.

**Counters and the summary line**, `password_recovery_probe.py:356-358`:

```python
356:         print(f"regrade cases={len(CASES)} differ={rediff}")
357:         print(f"cases={len(CASES)} observed_pass={npass} observed_fail={nfail} mismatches={mism}")
358:         return 0
```

`polyglot_c_py_probe.py:518-520` and `build_pmars_probe.py:343-344` print the identical
`cases=<n> observed_pass=<p> observed_fail=<f> mismatches=<m>` line (p45/p46 also print the
`regrade cases=<n> differ=<k>` line above it). This exact line shape is what the lane's own
counters parse: `plans/round46_c3_verify.py:134`
`SUMMARY = re.compile(r"^cases=(\d+) observed_pass=(\d+) observed_fail=(\d+) mismatches=(\d+)$")`
and `:307`
`re.match(r"^CASE (\S+) predicted=(pass|fail) observed=(pass|fail) .*?\bviolates=(\S*)", line)`.

**Receipt preamble** (capture provenance, printed once before the case lines):
`password_recovery_probe.py:335-337`:

```python
335:         print("# tb2 password-recovery grader probe (kengaku round 45) @ terminal-bench-2 2fd12b88")
336:         for name in sorted(PINS):
337:             print(f"# capture {name} sha256={PINS[name]}")
```

**The receipt is bare stdout.** Lane lesson `corpus/lessons/round-45.md:13`: a receipt committed
with envelope framing around the instrument's bytes fails the gate's P10 byte-equality check
("the receipt is bare probe stdout"). The r38/r45/r46 receipts contain exactly the probe's
stdout and nothing else.

---

## 4. CLI conventions

| flag | password_recovery | polyglot_c_py | build_pmars | note |
|---|---|---|---|---|
| `--lane` | `:285` default `"."` | `:435` default `"."` | `:280` default `"."` | lane repo root; `lane = pathlib.Path(a.lane).resolve()` |
| `--work` | `:289` | `:439` | `:283` | scratch **parent**, `default=None` → `$TMPDIR` |
| `--dry` | `:287` | `:437` | `:281` | prints the frozen table, no sandbox |
| `--stage-check` | `:288` | `:438` | — | builds end states, never grades |
| `--smoke` | — | — | `:282` | exercises the bwrap plumbing only |

`--dry` and `--stage-check` are a **mutually exclusive group** in the two later exemplars
(`password_recovery_probe.py:286-288`, `polyglot_c_py_probe.py:436-438`).

Two conventions come from elsewhere in the lane, not from these three probes:

* **`--selftest`** is the *counter/gate* convention: `plans/round52_c2_registry.py:194`
  `ap.add_argument("--selftest", action="store_true")` (its `selftest()` at `:138-188` builds
  throwaway fixture trees and prints `SELFTEST cases=3 failures=<k>`), and
  `plans/registry_check.py:146`. R55-C2's instrument spec names `--selftest` explicitly
  (`plans/round-55-claims.md`, R55-C2 instrument bullet).
* **`--receipt`** is a *file-writing* convention: `plans/attrib_probe.py:1137`
  `p.add_argument("--receipt", required=True, help="corpus/evidence receipt log")` (appends,
  `:546`), and `plans/order_check.py:145` (`--receipt` = the receipt under audit, read-only).
  None of the three exemplars has `--receipt`: their receipt file is produced by the caller
  redirecting stdout.

---

## 5. Exit-code contract

**Probe exemplars (all three identical in shape):**

| code | meaning | evidence |
|---|---|---|
| `0` | the battery ran and the summary line printed — **mismatches never change the exit code** | `password_recovery_probe.py:357-358`, `polyglot_c_py_probe.py:519-520`, `build_pmars_probe.py:343-344` |
| `1` | **only** the auxiliary mode failed: `--stage-check` had a bad end state (`password_recovery_probe.py:334`, `polyglot_c_py_probe.py:495`) or `--smoke` did not answer (`build_pmars_probe.py:317`) | same lines |
| `2` | setup error — malformed case table, capture missing/off its pinned digest, required tool not executable, uncreatable `--work`, or a case's recipe exiting non-zero | `password_recovery_probe.py:298, 313, 317, 323, 344`; `polyglot_c_py_probe.py:450, 465, 469, 475, 505`; `build_pmars_probe.py:290, 303, 307, 332` |

The lane's registry states this contract verbatim for the probe rows —
`SKILL.md:615` (`password-recovery-probe`): "**prediction mismatches are on the summary line, never
in the exit code**"; `SKILL.md:616` (`polyglot-c-py-probe`): same; `SKILL.md:582`
(`build-pmars-probe`): "`0` every case yielded four verdicts (the receipt's `match=` column
carries prediction agreement) · `2` setup".

**Counter convention (different, and what R55-C1's registry rows describe):** a counter prints
`PREDICATE <id> pass|fail` and exits `0` on pass, `1` on fail, `2` on setup —
`plans/round52_c2_registry.py:133-135`, `plans/round46_c3_verify.py:906-909`
(`print(f"PREDICATE C3 {'pass' if defects == 0 else 'fail'}")` / `return 0 if defects == 0 else 1`).

**Scratch lifecycle:** the exemplars create their own temp root *inside* `--work` and delete
only that root, leaving the caller's `--work` in place:
`password_recovery_probe.py:324` `root = pathlib.Path(tempfile.mkdtemp(prefix="k45-prp-", dir=a.work))`
with `finally: shutil.rmtree(root, ignore_errors=True)` at `:359-360`; and `--work` itself is
created if absent (`:318-323`, `return 2` if it cannot be). pmars does **not** create `--work`
(`build_pmars_probe.py:308`) — an absent `--work` raises `FileNotFoundError` there.

---

## 6. Where the current draft (`plans/round55_c3_chess_probe.py`) deviates

The draft is **not** part of the freeze commit (`git cat-file -e 80afa613:plans/round55_c3_chess_probe.py`
→ "exists on disk, but not in '80afa613'"; `git status --porcelain` → `?? plans/round55_c3_chess_probe.py`).
Deviations below are for E5/L1 to reconcile; this seat changed nothing.

1. **bwrap flags (§1).** Draft `:100` uses `["--unshare-all", "--die-with-parent", "--ro-bind", "/usr", "/usr"]`
   — no `--unshare-net/--unshare-pid/--unshare-ipc`, no `--new-session`; `:104-105` adds a
   `--ro-bind` branch for a non-symlink lib dir; `:108` adds `--tmpfs /home`.
   *Measured:* functional on this host — the draft's own battery returns the expected verdicts
   (§7) and `os.getuid()` is 1000 inside the sandbox. Deviation is in form, not in effect.
2. **Grader execution (§1).** Draft `:41-42` runs an inline `-c` program
   (`PROG = "import sys; sys.path.insert(0, '/tests'); import test_outputs as t; t.test_move_correct()"`)
   instead of a bound harness file that imports the grader and prints `TEST <name> P/F` lines.
   Consequence, measured (§7): the draft's classifier treats **any** non-zero exit whose output
   lacks the literal `AssertionError` as a *setup* error (`:126-130`), whereas the exemplars
   classify any non-AssertionError exception as a **case verdict** `F error=<Class>`
   (`build_pmars_probe.py:185-186`). A grader raising e.g. `IsADirectoryError` is `F` in the
   pattern and `SETUP` in the draft.
3. **Predictions are not per-test letters and the case table is not a frozen dataclass (§2).**
   Draft `:54-79` is a list of plain tuples `(name, content_bytes, "P"/"F")`; there is no `Case`
   dataclass, no `TAGS` dict, no `violates=` per case, no `requirement` prose, and no
   `--dry` mode / committed dry-table freeze receipt. The claims require "each mapped to one
   instruction requirement" (`plans/round-55-claims.md`, R55-C3 instrument bullet) — the draft's
   cases carry only source comments.
4. **No table self-validation (§2).** The draft never checks duplicate ids or prediction
   alphabet; its only setup path is the grader-digest check (`:135-143`).
5. **CASE line shape (§3).** Draft `:173` prints `CASE <name> predicted=P observed=P rc=0` — no
   `match=yes|NO`, no `violates=`, no `tests=`/`predicted_tests=` letters. The summary line
   `:174-175` *does* match `SUMMARY` (`round46_c3_verify.py:134`), but a future counter reusing
   the r46 receipt parser (`:307`, which requires `predicted=(pass|fail) observed=(pass|fail)`
   and `violates=`) would parse **zero** cases from this receipt.
6. **Exit codes (§5).** Draft `:179-183` returns `1` on a mismatch and prints
   `PREDICATE R55-C3 fail`; the exemplars return `0` with mismatches on the summary line only.
   R55-C3's own text requires the receipt to commit with `mismatches=0` and does not freeze an
   exit code, so this is a defensible choice — but the R55-C1 registry row for `round55-c3` must
   state the *actual* verdict-map cell, and it will differ from every other probe row in
   `SKILL.md` (which all say mismatches never affect the exit code).
7. **`--work` is destroyed wholesale.** Draft `:228` treats `--work` as the work directory and
   `:242-243` `shutil.rmtree(work, ignore_errors=True)` deletes **the whole caller's directory**,
   including unrelated files. The exemplars delete only their own `mkdtemp` root inside it and
   leave the caller's directory (and its contents) intact.
   *Measured:* a `--work` dir pre-populated with `precious/data.txt` came back **deleted** after
   the draft's run (§7).
8. **The summary line can report `mismatches=0` while a case went unevaluated.** Draft `:161-166`
   records a `SETUP` case, `:167-172` counts only P/F verdicts toward pass/fail and only counts
   a mismatch when `observed != predicted`, and `:174-175` prints the summary *before* the
   `SETUP` check at `:176-178`. *Measured:* with one case forced to SETUP, the run printed
   `cases=12 observed_pass=4 observed_fail=7 mismatches=0` — 4+7 ≠ 12 — then `SETUP cases=…`,
   exit 2. R55-C3's kill rule (a) is "a probe run where an observed≠predicted case is not counted
   as a mismatch"; the lane's own detector for this shape is `round46_c3_verify.py:331-335`
   (`p + f == n`), which the printed summary line violates.

---

## 7. What I ran (commands + exit codes), and what I did not

All runs were read-only against the lane repo; the only writes were to my own scratch
`/fast/scratch/hyaku/kengaku-r55/SC4ProbePrior/` (deleted at the end) and to this seat's wave
directory.

```
$ python3 plans/password_recovery_probe.py --lane . --dry | cmp - corpus/evidence/round45/password-recovery-dry-cases-freeze.txt
  → byte-equal (exit 0)
$ python3 plans/polyglot_c_py_probe.py --lane . --dry | cmp - corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt
  → byte-equal (exit 0)
$ python3 plans/round55_c3_chess_probe.py --lane . --work <scratch>/chess --selftest
  → "SELFTEST cases=2 failures=0", exit 0
$ python3 plans/round55_c3_chess_probe.py --lane . --work <scratch>/chess
  → "cases=12 observed_pass=5 observed_fail=7 mismatches=0", "PREDICATE R55-C3 pass", exit 0
$ (copy of the draft with one prediction flipped) python3 … --work <scratch>/mwork
  → "cases=12 … mismatches=1", "PREDICATE R55-C3 fail", exit 1     # a mismatch IS counted
$ (copy of the draft with one case forced to SETUP) python3 … --work <scratch>/smw
  → "cases=12 observed_pass=4 observed_fail=7 mismatches=0" + "SETUP cases=both-lowercase-two-lines", exit 2
$ (draft with --work pre-populated with precious/data.txt) python3 … --work <scratch>/wtest
  → exit 0, and <scratch>/wtest was DELETED (pattern would keep it)
$ python3 plans/round55_c3_chess_probe.py --lane . --work <scratch>/rcpt/w --receipt <scrpt>/rcpt/r.txt
  → receipt byte-identical to stdout (cmp exit 0)
$ python3 plans/build_pmars_probe.py --lane . --work <absent>/does-not-exist --smoke
  → FileNotFoundError traceback (exit 1; pmars does not create --work)
$ python3 plans/password_recovery_probe.py --lane . --work <scratch>/wkeep   (wkeep pre-populated)
  → exit 0, wkeep/precious/f.txt still present (pattern keeps the caller's --work)
$ bwrap with /app/move.txt as a directory, draft's flags
  → IsADirectoryError, no "AssertionError" in output → draft would score SETUP, pattern scores F error=IsADirectoryError
$ git cat-file -e 80afa613:plans/round55_c3_chess_probe.py → absent at the freeze commit
```

**Not run (out of scope, and honestly reported):** I did not run the two frozen laundering
fixtures for R55-C2, did not run `plans/round52_c2_registry.py`, did not run any upstream fetch or
benchmark, and did not execute `plans/round55_c2_entryargv.py` (it does not exist in the tree at
this revision — `plans/round55_c2_entryargv.py` is absent). I ran no mutating git/jj command.
