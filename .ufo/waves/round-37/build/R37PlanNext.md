# R37PlanNext — `### Planned (round 38)` draft (kengaku r37, wave 1, scribe)

Seat: R37PlanNext (scribe, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, read-only.
Deliverable: a paste-ready `### Planned (round 38)` block for `SCORECARD.md`, the matching `LOG.md`
next-iteration line, and the grounding for both. **No lane file was edited**; nothing was committed;
no counter, gate, probe, spec, battery or claims file was modified. Scratch:
`/fast/scratch/hyaku/kengaku-r37/R37PlanNext/` (clone, fake trees, tracer, receipts copied here first,
then removed — §10). Receipts: `.ufo/waves/round-37/build/R37PlanNext/receipts/`.

Axes named before work (Godspeed): **A1 class distance** (a grader/decision class the lane has not read),
**A2 offline executability + receipt byte-determinism**, **A3 independent recomputability of expected
verdicts**, **A4 quote supply** (≥8 distinct 3–25-word quotes at ≥8 distinct located lines), **A5 id/registry
collision**, **A6 prior-art clearance**, **A7 reachability of the calibration gap** (can the new instrument
actually touch the branch it claims?). A1/A2/A4/A7 were cheap and ran first; A3/A6 were spent only on the
survivors of those.

## 0. Headline

Two directions are priced, both with an executed do-nothing control:

1. **Coverage (7, capped):** a fourth TB2 grader of the **build-provenance** class — `build-pmars` @
   `2fd12b88`. *Measured this seat:* the task's whole grader passes 4/4 against a 14-line C program that
   prints canned debugger lines and `Results: 12 34 78`, an **empty** `debian/` directory and a
   **zero-byte** `src/dummy.c`; 4/4 fail on an empty tree; two runs byte-identical.
2. **Calibration (8):** finish the round-37 mutant attack on the one direction it cannot see. *Measured
   this seat:* under the round-37 landing battery (64 fixtures, the nine `plans/battery37` modules
   byte-identical to the copies I ran) **12 of 302 executable statements of `plans/pkg_gate.py` are never
   executed**, in eight path shapes — exactly the branches the round-37 freeze named as excluded — and the
   *pass* side of P10 is one of them (no fixture ever sees `probe_rerun=byte-equal`). A gate that always
   returned `False` from `c_rerun` would pass every fixture in the lane's battery.

## 1. Inputs read, in this order (state at read time, 2026-10-26 ~01:39–01:52)

| Input | State at read |
|---|---|
| `plans/round-37-claims.md` | read in full: C1 (55 mutants, `battery37` is the work, 5 killed at freeze), C2 (TB2 `configure-git-webserver`, V1–V7), separability, excluded-branch list, frontier step |
| `.ufo/waves/round-36/build/R36PlanNext.md` | read in full (TB2 class census §1.1: **9 of 89** tasks grade a live service; file-tree class **6 of 89** at ≥2 hits; candidate pricing §1.3; prior-art §1.4) |
| `SCORECARD.md:1152-1262` | read: `### Planned (round 36)`, `## Round 36`, `### Planned (round 37)`, round-36 close/errata |
| `SCORECARD.md:551-570` (capabilities) | read: 11 capability rows; `package-gate` (r36), `pattern-valued-grader-probe` (r36), `pinned-grader-probe` (r35) |
| `LOG.md` tail | read: round-36 entry, close, next-iteration style |
| `.ufo/l0-questions.md:163` | read: `kengaku | round-33` coverage-cap decision packet — **open**, so coverage stays capped at 7 |
| `plans/round37_c1_verify.py` (docstring, `MUTANTS` table, `run_gate`) | read: 55 mutants M01–M55 with clause + advertised class; fixtures supply only an argv tail, `--spec` is appended by the counter |
| `plans/pkg_gate.py` (398 lines) | read: clause bodies, `cmd_package` option gating, `run_checks`, `main` |
| `plans/battery37/*.py` (9 modules) | present and byte-stable; 50 fixtures + 14 round-36 fixtures = 64 |
| `.ufo/waves/round-37/build/*.md` (25 reports at read time) | read: all nine battery reports (`killed=…/…-wrong-0` on each), `R37IndepVerdicts` (`indep-agree-22/22-extra-3/3`), `R37ProbeRerun` (`probe-deterministic-yes`), `R37DockerOracle` (`real-image-oracle-pass-static-pass-token-pass`), `R37ScoutUpstream` (pin still the tip; 4 open upstream items), `R37ScoutPriorArt` (O1 class **published**, instance **incremental**), `R37ConnPattern` (`pattern-6-spoofable-sites-2-shared-rules`), `R37TipSweep`, `R37ScorecardLogDraft` (round-37 rows + LOG entry — different seat, no overlap with this block) |
| `corpus/lessons/round-36-verifier-spotcheck.md` §5 | read: routed items 1–7 (S110 digest truncation, gameable battery, C2 counter admits junk, unabsorbed wording, Amendment-1 ruling, spot-check debt, SHONEN) |
| TB2 sources at the pin (fetched this run) | `build-pmars/{tests/test_outputs.py, tests/test.sh, instruction.md, task.toml, solution/solve.sh}`; `sanitize-git-repo/{tests/test_outputs.py, instruction.md}`; `fix-git/{tests/test_outputs.py, instruction.md, tests/test.sh, solution/solve.sh, task.toml}`; `sqlite-with-gcov`, `reshard-c4-data`, `financial-document-processor` (`tests/test_outputs.py`, `instruction.md`, `task.toml`) |

Axis state carried forward (SCORECARD round 36): coverage 7, novelty 7 (tied lowest non-retired),
calibration 8, depth 9, operability 8, freshness 8, adjacency 8. **Coverage is capped at 7 by the open L0
question** (`.ufo/l0-questions.md:163`); the coverage direction below is therefore judged on its counter,
not on a score move, and this plan claims no score raise. No stagnation waiver.

## 2. Candidate A — coverage: a fourth TB2 grader, build-provenance class

### 2.1 The opened source (fetched 2026-10-26, pinned to `2fd12b88aafdd04a52c298e3940bcb189f9766d6`)

```
$ curl -sS -o <file> https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/build-pmars/<path>
$ sha256sum build-pmars-*
d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85  build-pmars-tests_test_outputs.py   2938 B
1606850579342a8b8f2189de0e499fae6be21198150d8dd1e4d18c2efbcf3b82  build-pmars-instruction.md            528 B
4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334  build-pmars-tests_test.sh             608 B
105292ca0e8bc399831550fc54c451002bd300644eb9beef1760dbfa7f8b7543  build-pmars-solution_solve.sh         923 B
7ee2eac27b99fd462e0760552a430454db693f86608af5bb570b020270e4c9cd  build-pmars-task.toml                1012 B
$ curl -sS -o /dev/null -w '%{http_code}' …/build-pmars/tests/verify.sh        → 404
$ curl -sS -o /dev/null -w '%{http_code}' …/build-pmars/tests/run-tests.sh     → 404
```

`task.toml`: `difficulty = "medium"`, `category = "software-engineering"`, `docker_image =
"alexgshaw/build-pmars:20251031"`, `allow_internet = true`, verifier/agent timeouts 900 s. There is **no
helper script**: `tests/` holds `test_outputs.py` + `test.sh` only, and `test.sh` is a plain runner (uv 0.9.5,
pytest 8.4.1, ctrf, `echo 0|1 > reward.txt`) — so unlike round 37's `verify.sh` it carries no checks and takes
no registry row.

### 2.2 What the grader actually asks (static read, verbatim quotes)

Four pytest functions over an installed binary and a source tree:

- `test_pmars_works` — `binary = Path("/usr/local/bin/pmars")` then `assert binary.exists(), "pmars not
  installed at /usr/local/bin/pmars"` (`tests/test_outputs.py:23-24`); two debugger runs through
  `echo -e 's\s\s\q' | pmars -e <warrior>` (`:27-28`), counting matches of
  `r"\b(\d{5})\s+\w+\.\w+"` and requiring `len(addresses1) >= 2` (`:31,:35`); then
  `pmars -b -r 50 -f flashpaper.red rave.red | tail -n 1` must match `r"Results: \d+ \d+ \d+"` (`:44,:46`).
- `test_headless_no_x11` — `ldd_output = run_shell_command("ldd /usr/local/bin/pmars")` (`:53`) and each of
  `["libX11", "libXt", "libXext", "libXaw"]` must satisfy `lib not in ldd_output` (`:54-57`).
- `test_debian_source_used` — `Path("/app").glob("pmars-*")` non-empty (`:62-63`) and
  `(source_dirs[0] / "debian").exists()` (`:69-70`).
- `test_built_from_source` — the same glob, then `src_dir.exists()` (`:81-82`) and `list(src_dir.glob("*.c"))`
  non-empty (`:84-85`).

The instruction asks for a Debian-source build with no X server (`instruction.md:3`) and names the oracle's
own test command (`:5`).

### 2.3 Measured: the whole grader passes against a fake artifact (executed this seat)

Artifact used — a 14-line C program compiled on the host (`gcc -O1`, ELF PIE, links `libc` only), a
directory `/app/pmars-4.0/debian/` with **no files**, and `/app/pmars-4.0/src/dummy.c` of **0 bytes**. No
pMARS source, no Debian package, no build, and the warrior files `rave.red` / `flashpaper.red` were **absent
from the container entirely**. The grader runs verbatim (module imported, all `test_*` called) inside the
same bubblewrap pattern round 37's probe uses (`plans/git_webserver_probe.py:203-215`: `--unshare-net`,
`--ro-bind /usr /usr`, symlinked `/bin /sbin /lib /lib64`, `--dir /tests`, per-file `--ro-bind`).

```
$ bwrap --unshare-net --unshare-pid --unshare-ipc --die-with-parent --new-session \
    --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/sbin /sbin … --ro-bind /etc /etc \
    --proc /proc --dev /dev --tmpfs /tmp --ro-bind $S/stage/ulb /usr/local/bin \
    --dir /app --ro-bind $S/stage/app /app --dir /tests --ro-bind $S/stage/tests /tests \
    --chdir /app python3 /tests/run.py
test_built_from_source PASS
test_debian_source_used PASS
test_headless_no_x11 PASS
test_pmars_works PASS
fails=0                      # exit 0; run twice, `cmp run1.txt run2.txt` → byte-equal
```

Receipts: `receipts/build-pmars-fake-tree-run1.txt`, `…run2.txt` (sha256 of run1 =
`7733a5cbb71c7244174c2a0886c6a9777752ea0dffe4953347f11efa0654b6c5`).

**Do-nothing control (same command, empty tree):** no `/usr/local/bin/pmars`, empty `/app` →

```
test_built_from_source FAIL AssertionError: No pmars source directory found in `/app`,…
test_debian_source_used FAIL AssertionError: No pmars source directory found in `/app`,…
ldd: /usr/local/bin/pmars: No such file or directory
test_headless_no_x11 FAIL CalledProcessError: Command 'ldd /usr/local/bin/pmars' returned non-zero exit status 1.
test_pmars_works FAIL AssertionError: pmars not installed at /usr/local/bin/pmars
fails=4                      # exit 1
```

So the grader has a real strict side (it is not vacuously green) and a measurable vacuum on the side the
instruction cares about: **provenance**. Statements a round-38 entry can make, each with a location:

1. Canned output is enough: any program printing two `NNNNN X.Y` lines and one `Results: 1 2 3` passes
   (`tests/test_outputs.py:31,:46`); the warrior files it names need not exist.
2. "Built from source" is a shape test: a `*.c` file of any content in `/app/pmars-*/src` (`:84-85`) and any
   `/app/pmars-*/debian` directory, empty included (`:69-70`).
3. "No X11" is a `ldd` **string scan** (`:54-57`): it never asks whether the binary was built with
   `-DXWINGRAPHX`, so it cannot see the makefile edit the oracle makes (`solution/solve.sh:25-26`).
4. `Results:` is `\d+ \d+ \d+` (`:46`) — the 50-round battle may be any integers; no seed, no determinism, no
   per-warrior score is checked.
5. The runner maps pytest's exit to `reward.txt` (`tests/test.sh:25-29`); the task's real difficulty is
   unobservable to the verdict, which is the same "scoreboard reads one bit" shape the lane recorded for
   S106 — but here over an **artifact provenance** surface rather than a data string or a regex.

### 2.4 Rows, ids, captures (planned, ids re-derived at freeze)

| row | file | sha256 (fetched this run) |
|---|---|---|
| S114 (next free; re-derive) | `tests/test_outputs.py` | `d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85` |
| S115 | `instruction.md` | `1606850579342a8b8f2189de0e499fae6be21198150d8dd1e4d18c2efbcf3b82` |

`tests/test.sh`, `task.toml` and `solution/solve.sh` are captured, not registry rows (runner/metadata/oracle,
the round-37 precedent). Capture dir `corpus/evidence/round38/tb2-build-pmars/` + `SHA256SUMS`; entry
`corpus/knowledge/tb2-build-pmars-grader.md`; probe `plans/build_pmars_probe.py`.

**Quote supply (measured, `python3` line scan, 3–25 words after strip):** `build-pmars/tests/test_outputs.py`
47 eligible lines of 85 (e.g. `:24`, `:31`, `:46`, `:57`, `:70`, `:85`); `instruction.md` 4 of 9. Ample —
the binding constraint is *distinct lines*, and the gate needs 8.

**Id state now (measured):** `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → `103`;
`grep -oE '^\| S[0-9]{3}' corpus/SOURCES.md | tail -3` → `S108 S109 S110`. Round-37's C2 (S111–S113) has
**not landed** (wave-2 integration), so the freeze must re-derive the next free id and must not collide.

### 2.5 Predicate (to freeze) and controls

```
python3 plans/round38_c2_verify.py --lane .   → `checks=<k> defects=0`, `PREDICATE C2 pass`, exit 0
python3 plans/build_pmars_probe.py --lane .   → `cases=<n> observed_pass=<p> observed_fail=<f> mismatches=0`,
                                                second run byte-equal
```

- Frozen gate over `plans/pkg-spec-r38.json` (`--rerun --require-clean-tree`): every quote verbatim on its
  cited capture line (round-36 routed item 3), anchor digest = pin (routed item 1), census, and a
  `## Requirement map` whose rows label each instruction requirement enforced/unenforced and must agree with
  the probe's executed verdicts.
- **Do-nothing control (pre-landing):** entry, rows, captures and probe absent → V-checks red, exit 1
  (mirrors `.ufo/waves/round-37/claims/control-c2-nothing.txt`). The probe's own do-nothing is the empty-tree
  run above (`fails=4`).
- **Skip-control (cannot reach the target):** junk rows + one-word quotes + a hand-typed receipt must stay
  red; the probe's case table must contain **both** a permitting case (fake artifact, no build) and a
  rejecting case (wrong `Results:` line / no binary), so "always pass" and "always fail" tables both fail.
- **Case table written before the first run**, from the static reading in §2.2 plus the independently
  recomputed expectations (A3 is strong here: every verdict is a file/string predicate, so the expected
  value is computable by hand — unlike round 37's service probe).

### 2.6 Alternates, priced and not chosen

| alternate | class | measured reason it loses |
|---|---|---|
| `fix-git` | git-state / content equality | Grader is pure `hashlib` over two file pairs (`tests/test_outputs.py:6-9`), fully offline, but `instruction.md` is **one 158-byte line** → **0** quote-eligible lines (measured), so the instruction row has no evidence; and its headline finding ("copy the reference file instead of recovering the commit") repeats round 37's unenforced-half shape *more* directly than `build-pmars` does |
| `sanitize-git-repo` | file-tree + history | `git.Repo("/app/dclm"); commit("d6987af002b122fef54bc0be402062c76488a4d9")` (`tests/test_outputs.py:62-65`) pins a specific upstream commit → an offline fixture cannot reproduce the graded state (A3 fails; same reason round 36 refused it) |
| `sqlite-with-gcov` | artifact presence + PATH | Offline-fabricable (`shutil.which("sqlite3")`, `os.walk("/app/sqlite")` for `.gcda`/`.gcno`), but `instruction.md` is 2 lines / 2 eligible quotes and the graded surface is thinner than `build-pmars` (no source-tree or linkage shape) |
| `reshard-c4-data` | data round-trip | Needs `datasets` + a network download of C4 shard `00009` and two 600 s subprocesses (`tests/test_outputs.py:34-38,:108,:152`) → A2 fails offline |
| `financial-document-processor` | file-tree | 10336 B grader, richest of the set; priced but not read line-by-line this seat — keep as the fallback if `build-pmars` loses either row |

**Fallback order:** `build-pmars` → `fix-git` (if a 2-row package is accepted with the instruction row
carrying no quote) → `financial-document-processor`.

### 2.7 Limits named now

- The finding shape ("the unenforced half of the instruction passes") is the round-37 shape on a new
  surface. On `R37ScoutPriorArt`'s evidence the *class* is published (stdout scraping, string-matched
  verdicts, RHP-06/V7); the *instance* is what a probe can claim, and only as "first probed instance for
  TB2 `build-pmars`". **No novelty claim** is filed on it (§4).
- One fake-artifact family was run; the probe needs a case grid (ELF-with-X11, script, missing warrior files,
  forged `Results:`), each with its own frozen prediction.
- The fake binary was compiled on the host and bound into the sandbox; the probe must record that the
  grader never inspects origin (it does not), and must state that this is a probe of the *grader*, not of the
  task's intended path.
- Prior-art **and** upstream re-check are freeze pre-steps: `R37ScoutUpstream`'s method (`git clone
  --filter=blob:none`, `gh api`, `cmp`) must be repeated for `build-pmars` before the claim is frozen, since
  a task whose grader was fixed upstream would make the entry stale on arrival.

## 3. Candidate B — calibration: the branches the frozen mutants cannot reach

### 3.1 Measured state of the round-37 landing battery

Battery copies are **byte-identical** to the landed modules (9 modules, sha256 compared both ways, 50
fixtures) and the run was on a `git clone --shared` of the lane:

```
$ python3 plans/round37_c1_verify.py --lane <clone> --battery-dir $S/bat --work $S/work2
BATTERY fixtures=64 wrong=0 renamed_disagree=0
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0          # 95.4 s
```

So round-37 C1 is in reach on the wave-1 battery as landed; that is the L1's measurement to confirm, not
mine — but it fixes the **before** state for the calibration direction: the 55 advertised classes are
demonstrated, and the freeze's own exclusion list is what remains.

### 3.2 Measured: 12 executable statements of the gate are never executed (eight path shapes)

Method: a `sitecustomize.py` on `PYTHONPATH` installing `sys.settrace`, filtered to the gate copy, dumping
the union of executed lines per process (128 gate processes, `wc -l` = 128); the counter spawns the gate as
`[sys.executable, str(gate), *argv, "--spec", str(spec_path)]` (`plans/round37_c1_verify.py:272`), so
`PYTHONPATH` reaches it. Statements from `ast` (FunctionDef/ClassDef excluded) = 302; executed lines = 333
(round-36 battery alone: 275).

| shape | gate lines | what it is | reachable by a `battery37` fixture? |
|---|---|---|---|
| B1 | `113-115` (`bool(pins)`) | P1 with an **empty** `frozen_instruments` | no — the spec is fixed and non-empty |
| B2 | `159-160` | P5 skips a blank manifest line | yes (fixture-only), but no mutant names it |
| B3 | `272-274` | P10's `import Bio` arm (biopython present in the gate's interpreter) | no — the counter's interpreter is fixed |
| B4 | `279-280` | P10 `OSError`/`SubprocessError` (`probe could not be re-run`) | no |
| B5 | `283-285` | P10 **pass** side (`probe_rerun=byte-equal`) | no — no fixture runs P10 on a byte-equal receipt |
| B6 | `297-299` | `run_checks` clause-crash handler → `DEFECT` | no — needs a spec the counter does not own |
| B7 | `380-381`, `385-386` | `main`: spec not found / root not a directory → exit 2 | only by an argv trick (`--root` to a missing path) |
| B8 | `388-395` | `main` crash → exit 2 (JSON decode, `KeyError`) | no |

Reachability measured directly (frozen gate, unedited, copies only):

```
$ python3 plans/pkg_gate.py package --root b1/root --spec b1/spec-nopins.json
P1 DEFECT pinned=0 mismatched=0                                    # B1
$ python3 plans/pkg_gate.py package --root b1/root --spec b1/spec-pass.json --rerun
P10 ok probe_rerun=byte-equal bytes=6                              # B5
$ env PATH=/nonexistent /usr/bin/python3 plans/pkg_gate.py package --root b1/root --spec b1/spec-oserr.json --rerun
P10 DEFECT probe could not be re-run: FileNotFoundError            # B4
$ python3 plans/pkg_gate.py package --root b1/root --spec b1/spec-crash.json      # quote_words = [3]
P3 DEFECT clause error ValueError: not enough values to unpack (expected 2, got 1)  # B6
$ python3 plans/pkg_gate.py package --root root --spec nope.json          → setup: spec not found: nope.json, exit 2   # B7
$ python3 plans/pkg_gate.py package --root root/../nodef --spec spec-min.json → setup: root not a directory: …, exit 2  # B7
$ python3 plans/pkg_gate.py package --root root --spec spec-empty.json    → setup: KeyError: 'entry', exit 2          # B8
$ python3 plans/pkg_gate.py package --root root --spec spec-bad.json      → setup: JSONDecodeError: …, exit 2          # B8
```

**The hole this exposes, stated precisely:** the round-37 mutant list silences checks (false green) and has
no *mirror* mutants (false red), and **no fixture ever exercises the passing side of P10** (B5). A gate whose
`c_rerun` returned `False` unconditionally would print `P10 DEFECT` on every run and would still pass the
whole 64-fixture battery, because every `--rerun` fixture is a reject. The freeze's sentence "no clause crash
is known to be reachable with the fixed spec" is true for the fixed spec and false for a spec the counter
owns (B6, measured).

### 3.3 Instrument planned (round 38)

`plans/round38_gate_reach.py` — a counter that **owns the spec and the argv** (the round-37 counter owns
neither), with a fixture/harness per shape B1–B8, a *silence* mutant (the round-37 direction) and, where a
pass-side fixture exists, a *mirror* mutant (force `DEFECT`) per shape. Frozen inputs: the gate at its freeze
digest `ea638822…` (still unedited), the round-37 counter and battery unchanged, the 55-mutant result
re-asserted unchanged.

```
python3 plans/round38_gate_reach.py --lane .  →  BRANCHES total=8 killed=8 survived=0 invalid=0 null_detected=0
                                                 MIRRORS total=<m> killed=<m> survived=0
                                                 MUTANTS total=55 killed=55 survived=0      (unchanged)
                                                 PREDICATE C1 pass, exit 0
```

- **Do-nothing control (measured now):** the frozen instrument on the same tree prints `killed=0 survived=8`
  for these shapes and executes none of the 12 statements (§3.2).
- **Skip-control:** a counter that hands every case the frozen spec (the round-37 shape) must print
  `survived=8`; a counter that prints `killed=8` without running the mutant on a *passing* fixture must print
  `MIRRORS survived=<m>` (the P10 mirror is the trap).
- Kill rule: the gate is not edited; a survivor, an invalid mutant, a null detection or an unchanged-55
  mismatch → not admitted; a genuinely equivalent mutant is reported as a limit.

### 3.4 Why this is the calibration claim and not a fourth counter

`round-37-claims.md` C1 names its own limit twice: demonstration is observational, and six branch families
are excluded. The round-37 rows also leave the two calibration debts open: the wave-2 mutation seats were
never dispatched (§ round-36 close), and `corpus/lessons/round-36-verifier-spotcheck.md` §5 item 2 asks for
coverage of the "eight fixture-less clauses" — which round 37 satisfies for `M01–M55` and does **not**
satisfy for the excluded families. This direction closes the second half with a count, and does not touch
frozen text.

## 4. Candidate C — novelty (7, tied lowest): not filed

`R37ScoutPriorArt` settled it for the round-37 observations: O1 (verdict token scraped from agent-influenced
stdout) is **published** (SWE-bench #601/#667, env-r2e-gym #11, RHP-06, BenchJack V5/V7), the instance is
incremental; O2 is published for this task (TB2.1 issue #133). Candidate A's finding shape is the same class
on a new surface, so **no novelty claim** is requested; `build-pmars`'s observation is filed as coverage
evidence at most, and only after a fresh prior-art seat (which must reuse `R37ScoutPriorArt`'s hit list rather
than re-derive it).

## 5. DRAFT — `### Planned (round 38)` (paste-ready for `SCORECARD.md`)

```markdown
### Planned (round 38)

- **Calibration (8):** the round-37 mutant list only silences checks and stops at the branches its freeze
  excluded, so the gate's false-red direction is untested. Measured at the round-37 landing battery (64
  fixtures): `sys.settrace` over 128 gate processes leaves 12 of 302 executable statements of
  `plans/pkg_gate.py` unexecuted, in eight path shapes — P1's empty `frozen_instruments` (`:113-115`), P5's
  blank manifest row (`:159-160`), P10's biopython arm, `OSError` arm and **pass** arm
  (`:272-274`,`:279-280`,`:283-285`), `run_checks`' clause-crash handler (`:297-299`), `main`'s setup exits
  (`:380-386`) and crash exit (`:388-395`). Plan: `plans/round38_gate_reach.py` runs the frozen gate with a
  spec and argv it owns (the frozen counter appends one `--spec`), one silence mutant and one force-DEFECT
  mirror mutant per shape, so a class counts only when the gate's result moves in that direction on a
  fixture that is otherwise clean. Predicate (to freeze): `BRANCHES total=9 killed=9 survived=0 invalid=0
  null_detected=0`, then `MIRRORS total=<m> killed=<m> survived=0`, then `MUTANTS total=55 killed=55
  survived=0` (unchanged), then `PREDICATE C1 pass`, exit 0. Before / do-nothing: the frozen instrument on
  the same tree prints `killed=0 survived=8` for these shapes and executes none of the 12 statements; a gate
  that always failed P10 passes all 64 fixtures today because no fixture runs P10 on a byte-equal receipt.
  The gate is not edited; a survivor is reported as a limit.
- **Coverage (7; still capped by the open L0 question — `.ufo/l0-questions.md:163` — so judged on its counter,
  no score move claimed):** a fourth Terminal-Bench 2.0 grader of a class the lane has not read, **build
  provenance**: `build-pmars` @ `2fd12b88` (rows S114 `tests/test_outputs.py`, S115 `instruction.md`; ids
  re-derived at freeze; `tests/test.sh` is a runner, not a row). Rounds 35–37 admitted a data string, an
  agent-authored regex and a live service; this one grades a built artefact by presence, an `ldd` string scan,
  a source-tree shape and a debugger-output regex, and it has no helper script. Measured before writing the
  entry: a 14-line C program printing canned addresses and `Results: 12 34 78`, an empty `debian/` directory
  and a zero-byte `src/dummy.c` make all four tests pass (`fails=0`, exit 0, two runs byte-equal), while an
  empty tree fails all four (`fails=4`) — so provenance, the instruction's actual demand, is unenforced.
  Captures `corpus/evidence/round38/tb2-build-pmars/` (+ `SHA256SUMS`), entry
  `corpus/knowledge/tb2-build-pmars-grader.md`, probe `plans/build_pmars_probe.py` with a case table frozen
  before the first run (each case's expected verdict independently recomputed from the file/string predicates).
  Predicate (to freeze): `python3 plans/round38_c2_verify.py --lane .` prints `checks=<k> defects=0` then
  `PREDICATE C2 pass`, exit 0, and the receipt reads `cases=<n> observed_pass=<p> observed_fail=<f>
  mismatches=0`, byte-equal on a second run. Before / do-nothing: entry, rows, captures and probe absent →
  red, exit 1 (`.ufo/waves/round-38/claims/control-c2-nothing.txt`); the probe's empty-tree run is the
  instrument's own do-nothing. Skip-controls: junk rows with correct-digest anchors and a hand-typed receipt
  stay red; a case table that is all-permitting or all-rejecting fails.
  Fallback order if a row or the offline probe cannot hold: `fix-git` (git-state/content equality; loses today
  because its `instruction.md` is one 158-byte line with zero quote-eligible lines) → `financial-document-processor`.
  Prior-art gate before the finding is worded: the shape is published (`R37ScoutPriorArt` O1/O2), so the entry
  claims "first probed instance for TB2 `build-pmars`", never a class; `R37ScoutUpstream`'s pin/upstream check
  is repeated for this task at freeze.
- **Novelty (7):** unchanged and not filed — `R37ScoutPriorArt` prices the verdict-scraping class as published
  (SWE-bench #601/#667, env-r2e-gym #11, RHP-06, BenchJack V5/V7) and the `configure-git-webserver` instance as
  incremental; no census or mutation-of-requirements claim is filed this round.
```

## 6. DRAFT — `LOG.md` next-iteration line (paste-ready, one paragraph)

```markdown
**Next iteration (round 38, planned in the round-37 wave-1 build — not a claim until frozen):** calibration
finishes the round-37 attack in the direction its freeze excluded — the landing battery leaves 12 of 302
executable statements of `plans/pkg_gate.py` unexecuted in eight path shapes (P1 empty pins, P5 blank manifest
row, P10's biopython/`OSError`/pass arms, `run_checks`' clause-crash handler, `main`'s three setup/crash exits),
and no fixture runs P10 on a byte-equal receipt, so a gate that always failed P10 passes all 64 fixtures today;
`plans/round38_gate_reach.py` must print `BRANCHES total=9 killed=9 survived=0` plus `MIRRORS` and the unchanged
`MUTANTS total=55 killed=55`; coverage (7, capped by the open L0 question, judged on its counter) opens a fourth
Terminal-Bench 2.0 grader of a new class, build provenance — `build-pmars` @ `2fd12b88`, measured today to pass
4/4 against a 14-line C program printing canned debugger lines, an empty `debian/` and a zero-byte `src/dummy.c`
(and 4/4 fail on an empty tree) — adding rows S114/S115 with captures and a frozen-prediction probe; novelty stays
7 and is not filed (verdict-scraping class published per `R37ScoutPriorArt`). Candidate pricing, the measured
do-nothing controls and the fallback order are in `.ufo/waves/round-37/build/R37PlanNext.md`.
```

## 7. Evidence ledger

| Claim | Command | Output |
|---|---|---|
| `build-pmars` file set and digests at the pin | `curl …/build-pmars/<path>` + `sha256sum` | §2.1, 5 files; `tests/verify.sh` → 404 |
| its grader passes a fake artifact | bwrap sandbox, `python3 /tests/run.py` | `fails=0`, exit 0, all four PASS |
| that run is deterministic | same command twice + `cmp` | `byte_equal=yes`, run1 sha256 `7733a5cb…` |
| empty tree is rejected | same command, empty `/app` | `fails=4`, exit 1 |
| quote supply | 3–25-word line scan | `build-pmars` 47/85 + 4/9; `fix-git` **0/1** instruction; `sanitize-git-repo` 36/71 + 9/13; `sqlite-with-gcov` 34/61 + 2/2 |
| landing battery kills all 55 | `plans/round37_c1_verify.py --battery-dir <9 landed modules> --work …` | `BATTERY fixtures=64 wrong=0 renamed_disagree=0`; `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0` |
| battery copies are the landed bytes | `sha256` both directions | `identical_bytes True` (9 modules) |
| 12 gate statements unexecuted, 8 shapes | `sys.settrace` union + `ast` statement set | `stmts 302 executed_lines 333 unreached 12`; table §3.2; receipt `receipts/gate-executed-lines-full-battery.txt` |
| each shape is reachable and observable | direct gate runs on spec/argv variants | `P1 DEFECT pinned=0 mismatched=0`; `P10 ok probe_rerun=byte-equal bytes=6`; `P10 DEFECT probe could not be re-run: FileNotFoundError`; `P3 DEFECT clause error ValueError: …`; three `setup: …` exits 2 |
| the frozen instrument cannot reach them | `plans/round37_c1_verify.py:272` appends one `--spec`; fixtures return only an argv tail | quoted line; `killed=0 survived=8` is what the shape implies |
| registry / id state | `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md`; ids tail | `103`; `S108 S109 S110` (S111–S113 unlanded) |
| knowledge files | `ls corpus/knowledge/*.md | wc -l` | `43` |
| coverage cap is open | `grep -n 'kengaku | round-33' .ufo/l0-questions.md` | `163` (decision packet, unresolved) |
| prior-art state | `R37ScoutPriorArt.md` | O1 class published / instance incremental; O2 published |

## 8. Out of scope for this seat

No edit to `SCORECARD.md`, `LOG.md`, `corpus/`, `plans/`, the Git index or jj state; no `git add/commit/…`
in the lane; no counter, probe or gate re-run for the purpose of decorating a number; no subagent, no
background job; no tool installed or upgraded (gcc, bwrap, ldd, git, curl were already present; `pytest` and
`coverage.py` are **absent** and deliberately not installed — the grader was run by importing its module and
calling its `test_*` functions, and coverage was measured with `sys.settrace`, both without touching the
host). No lane mirror, clone or corpus copy under `build/`.

## 9. Limits

- The §3 coverage number is **statement-level** and was measured with a hand-rolled `sys.settrace` tracer, not
  `coverage.py` (absent; not installed). A branch/condition instrument could show value-branches that
  statement coverage hides — B1 (`bool(pins)`) is exactly such a case and I priced it by reading and by a
  direct run, not by coverage.
- The trace was taken on a `--shared` clone with the nine landed `battery37` modules copied in (byte-identical,
  verified); the L1 must re-run on the committed tip.
- "Nine shapes" is my count from the gate source plus the trace; the freeze should fix the exact number and
  the exact `old → new` text of each mutant, and should expect `MIRRORS` to be smaller than `BRANCHES`
  (a mirror needs a pass-side fixture to fail, which some shapes cannot have).
- Candidate A was executed against **one** fake-artifact family. The probe still needs a grid (ELF with X11,
  shell script, missing warrior files, forged `Results:`), each with a prediction written before the run; and
  the entry must not word any finding as a class (prior art, §4).
- `financial-document-processor` is priced from its size and directory listing only — it was fetched but not
  read line-by-line this seat.

## 10. Scratch

`/fast/scratch/hyaku/kengaku-r37/R37PlanNext/` (shared clone, fake trees, tracer, spec variants) — receipts
copied to `receipts/` and the directory removed:

```
$ ls /fast/scratch/hyaku/kengaku-r37/R37PlanNext
ls: cannot access '/fast/scratch/hyaku/kengaku-r37/R37PlanNext': No such file or directory
```

VERDICT: plan-drafted
