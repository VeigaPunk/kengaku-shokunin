# R40RevCounters — code review: `plans/round40_c1_verify.py`, `plans/round40_c2_verify.py`, `plans/db_wal_probe.py`

Round 40 wave 1, 2026-10-26. Reviewer seat; frozen bytes only read, never edited or run to verdict. No scratch
created (no executions), nothing installed. All citations are to the working tree at review time; lane tip seen
by this seat matches the frozen tool digests (checked: `sha256sum plans/pkg_gate.py` → `ea638822…edd41`, equal to
`round40_c2_verify.py:61` GATE_SHA256).

Method: full reads of the three scripts (576 + 284 + 386 lines), cross-reads of the three pinned tools' emission
sites, the captures (`test.sh`, `test_outputs.py`, `instruction.md`), the dry table, and a body diff of
`round40_c2_verify.py` against `round39_c2_verify.py`. Command for the ancestry check:
`diff <(sed -n '/^def v1/,/^def main/p' plans/round39_c2_verify.py) <(sed -n '/^def v1/,/^def main/p' plans/round40_c2_verify.py)`
→ sole difference is `pkg-spec-r39-effective.json` → `r40` (one line). So "no check added or relaxed"
(claims §C2) is verified byte-level.

## Findings by severity

### F1 [medium] C2 V6 executes an unpinned, out-of-lane program while the docstring claims every input is pinned
- `round40_c2_verify.py:67` — `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`; run at
  `:204-206`. The script is outside the lane (a "clean clone of the landing tip" does not contain it), and no
  digest pins it.
- `round40_c2_verify.py:10-11` — "Every input this counter reads that exists at the freeze is pinned here by
  digest: the spec template, the gate, the probe, the frozen dry table and the seven captures." The census
  script is an input read at the freeze and is not pinned: the sentence is false as written.
- False-green/false-red path: any edit (accidental or hostile) to the fleet-root script flips V6's verdict with
  zero detection — V6 is 1 of 7 checks, so it alone decides `checks=7 defects=0`.
- Ancestry: same unpinned constant in `round37_c2_verify.py:58`, `round38_c2_verify.py:63`,
  `round39_c2_verify.py:65` — carried, not new; but rounds 38–40 each re-assert the pin-everything sentence
  (`round38_c2_verify.py:9`, `round39_c2_verify.py:9`, `round40_c2_verify.py:10`).
- Recommendation to L1 (nothing frozen changes): either hash-pin the census script in V6 and fail on mismatch,
  or scope the docstring sentence to the enumerated inputs and name the census as an unpinned host dependency.

### F2 [medium-low] C1 contract hole: `build()`'s return value is char-split before validation
- `round40_c1_verify.py:296` — `argv = [str(t) for t in fx["build"](ctx, d)]` iterates whatever `build`
  returns. A module returning a bare slash-free string (e.g. `"reject"`) yields a per-character argv; every
  element is `str` and none is absolute, so the contract check at `:430-434` passes.
- Consequence: a vacuous fixture whose tool call is garbage still lands as `expect=error` (any tool refuses
  unknown args with exit 2) and then satisfies `exhibits` for the `error` direction (`:393-405`: ref rc=2,
  mutant rc 0/1) — an attributed kill from a meaningless fixture, feeding `MUTANTS … killed=…`.
- Fails closed in most other shapes: `None` → TypeError in the child (SETUP exit 2); any string containing
  `/` → `path_ok("/")` is False (`:326-330`) → ValueError.
- One-line fix (for the L1's next counter revision, not this freeze): require `isinstance(built, list)` in
  `build_module_child` before the list comprehension.

### F3 [low] C1 tamper fingerprint is metadata-only
- `round40_c1_verify.py:310-323` — the hash covers rel path, `st_mode`, `st_size`, `st_mtime_ns`, link target;
  file content is never read. A same-size in-place rewrite with `st_mtime_ns` restored evades `tampered`
  entirely, and the writer is the same user: `sandbox()` is `--dev-bind / /` (`:304`), so tool runs and build
  children may write anywhere writable on the host.
- Also invisible: creation/removal of empty directories (no files → no hash input), and `*.lock` /
  `.git/index` are excluded by suffix (`:317`) by design.
- Mitigation that does hold: the three tools themselves are content-checked before and after (`PINS` `:457`,
  `PINS-AFTER` `:561-562`) and every variant is digest-checked after its runs (`:541`), so the verdict-critical
  bytes cannot be silently altered — the gap is fixture-tree content only. Non-author battery review (named
  limit) is the real control; reviewers should know the fingerprint proves no *structural* change, not no
  content change.

### F4 [low] C1 sandbox isolates PIDs only — no FS confinement, no network unshare
- `round40_c1_verify.py:304` — `--dev-bind / / --proc /proc --unshare-pid --die-with-parent --new-session`;
  no `--unshare-net` (contrast the probe's sandbox, `db_wal_probe.py:262`, which unshares net/ipc/pid and
  ro-binds `/usr`).
- Consequence: build children (`:417-423`) and every reference/null/mutant run (`:380-381`) can read the real
  lane, write any user-writable path, and reach the network. All verdict-relevant targets are re-hashed after
  the fact (`:541`, `:546-550`, `:561-562`), so detection exists — but detection of a lane-tool overwrite means
  the bytes are already damaged when the counter runs against the live lane (`--lane .` in the frozen command).
  The claims' "measured on a clean clone of the landing tip" is what makes admission runs safe; the docstring's
  limits section names PATH/HOME inheritance but not FS/network exposure.
- Operational rule this yields: wave seats must run the C1 counter only with `--lane` pointing at a disposable
  clone (the fixture rule already mandates exactly this).

### F5 [low] C1 SIDECHANNEL scan is raw substring matching on common prose
- `round40_c1_verify.py:412-413` — `t in text` over `text.lower()`; tokens include `"fork"`, `"core."`,
  `"filter."` (`:92-94`). Innocent battery comments trip it: any "…the score. …" (contains `core.`), any
  mention of forking a branch, "profile." → `filter.`? (no — `profile.` contains `file.`? token is `filter.` —
  safe), but `score.`/`encore.`/`forked` all fire.
- Direction is fail-red (`sidechannel>0` → predicate fail, `:567-568`), so this is a trip-hazard for wave-1
  battery authors, not a false-green. Word-boundary matching (`re.search(rf"\b{re.escape(t)}", text)`) would
  remove the prose collisions while keeping every real token hit.

### F6 [low] C1 accepts `fid=""` and silently disables kill attribution for that fixture
- `round40_c1_verify.py:430` accepts any `str` fid, including `""`; then `by = by or fx["fid"]` (`:539`) treats
  the empty string as falsy, so a fixture that exhibits a kill records `SURVIVED` instead of `killed by=`.
  Fail-red (predicate fails honestly), but the receipt misattributes *why*, and the `FIXTURE` line prints a
  blank id. Fix: reject empty fid in the contract check.

## Operability notes (not defects)

- **Scratch/TMPDIR.** All three honor `--work` and create it if absent (c1 `:463-464`, c2 `:266`, probe
  `--work` mkdir with OSError handling; `mkdtemp(dir=a.work)` / `TemporaryDirectory(dir=a.work)`), and with no
  `--work` they fall to `tempfile`'s default = `$TMPDIR` (→ `/tmp` if unset). The frozen predicate commands say
  only `--lane .`, so the operator's "never /tmp" directive binds the *caller*: seats must `export TMPDIR="$S/w"`
  or pass `--work` explicitly. The tools themselves are compliant; restate this in the L1's command block.
- **Probe timeout path.** `db_wal_probe.py:291` has `timeout=300` with no `except TimeoutExpired` — a hung case
  exits via traceback (host paths on stderr, stdout receipt clean, exit ≠ 0: fail-closed). C1 handles the same
  case cleanly (`round40_c1_verify.py:382-383` → `("timeout", frozenset())`).
- **C2 v7 cases cell must cite bare ids.** `cited = re.findall(r"`([a-z0-9-]+)`", rest)` (`:250`) treats every
  backticked token in the trailing cells as a cited case; any explanatory backtick in the entry's map row
  false-reds V7. Entry authors: ids only in that column.
- **Dev-mode exit codes.** `--only`/`--battery-dir` → `PREDICATE C1 n/a`, exit 0 when wrong/tampered/side/
  survived/invalid/null are all zero and pins-after clean (`:563-566`) — killed is intentionally not required,
  correct for subset runs. A pin mismatch on tool X makes all X-mutants `invalid` (`:519`), so even dev runs
  surface tool edits.

## Verified clean (checked, no defect)

- **`classes()` per tool vs actual bytes.** anchor: `DEFECT … class=` tokens — emission sites
  `anchor_digest_check.py:459,465,478,490,504,510,525,530,535,554`; regex `round40_c1_verify.py:334-336`
  (`startswith("DEFECT ")`, `\bclass=(\S+)`) — matches, and no `detail=` string contains `class=`.
  ledger: `f"{r['id']} status={st} observed=… agree={yes|NO} …"` at `ledger_tip.py:242-244`; regex
  `:338-340` `^(\S+) status=\S+ observed=\S+ agree=NO\b` — matches (`\b` holds before space and EOL).
  order: `ORDER HIT {path}@{c}:{n} kind={kind}` at `order_check.py:196`, named
  `ORDER FAIL <name> <detail>` at `:184,189`, summary `ORDER FAIL <names> hits=<n>` at `:201`; regex
  `:341-347` captures `kind=` and named FAILs while the `" hits=" not in line` guard correctly excludes the
  summary — matches. One coupling to note: the named-FAIL regex needs a space after the name; true at all
  current sites, guaranteed only by the pin.
- **Runner thread-safety.** `itertools.count` `next()` is atomic; per-run work dirs `:370` (fresh `{WORK}` per
  reference, null and mutant run — a fixture cannot carry state across runs via `{WORK}`); `slots/*.py`
  written once before any run (`:348-350`) and ro-bound over the variant at a fixed path (`:378`); `ex.map`
  preserves order (`:388-391`); no shared mutable state. `--jobs 0` would raise ValueError (max_workers) —
  fail-closed, no validation nit worth a finding.
- **Pins.** C1 pins exactly the three tools (`:82-86`), re-hashed after (`:561-562`); witnesses are label
  strings only — the loop unpacks `_witness` (`:515`) and never reads it, as the docstring claims.
  **What else C1 reads:** `plans/battery40/*.py` (unpinned — the work under test; default battery dir
  `:471`), the lane HEAD clone for `ctx.lane` (unpinned by design), `/usr/bin/bwrap` (X_OK only, `:448-450`),
  `git` and `sys.executable` (unpinned toolchain), caller `PATH`/`HOME` (`:363`, named limit). It reads no C2
  artifact — separability as frozen. The unpinned toolchain (bwrap/git/python versions) is residual risk, not
  a defect: `GIT_CONFIG_COUNT` needs git ≥ 2.31, `init -b master` ≥ 2.28.
- **C2 checks.** V1–V7 byte-identical to round 39 except the effective-spec filename (diff above). Gate digest
  matches its pin (command in header). V5 re-hashes probe+dry then byte-compares a fresh `--dry` (`:196-200`).
  V4: order-sensitive id list vs frozen table, exactly one anchored summary line, pass/fail/mismatch counts
  recomputed from the CASE lines (`:174-190`); CASE lines lacking `violates=` fail to parse → count mismatch →
  defect (fail-closed). V7: label derived from ALL violating cases (`derive`, `:242-249`), frozen line number
  enforced (`:247`), duplicate/missing tags and uncited/foreign ids all defect (`:250-253`).
- **Probe sandbox.** `--unshare-net --unshare-pid --unshare-ipc --die-with-parent --new-session`, `/usr` and
  `/etc` ro, `/tmp` tmpfs, `/app` a fresh writable bind, `/cap` holds only `test_outputs.py` + `solve.sh`,
  cwd `/app`, `HOME=/tmp` (`:262-274`, `:288`) — matches the docstring sentence for sentence.
- **Recipe failure → exit 2.** harness: `if rc or mode == "stage": sys.exit(3 if rc else 0)` before
  `spec_from_file_location` (`db_wal_probe.py:240-244`) — grader never imported in stage mode; probe:
  `if rc != 0 or set(got) != set(TESTS) or set(again) != set(TESTS): … return 2` (`:361-364`). Verified.
- **Nothing host-specific in the receipt.** stdout = header comment with the pinned TB commit, `# capture …
  sha256=` lines, CASE lines (ids, P/F letters, exception *class names* only in `error=`), `regrade cases=…`,
  `cases=…` — no paths, times, versions; scratch under `--work`/`$TMPDIR` removed in `finally`. `--dry` is
  static data → byte-stable (V5's check is meaningful).
- **Regrade logic.** Second grading of the same end state, `regrade=same|DIFF:<letters>` reported per case and
  `regrade cases=… differ=` summary (`:365-372`); `rediff` never enters the verdict or the return code. Matches
  the stability rider.
- **Grader equivalence claims.** `test.sh:23-27` — `pytest … ; if [ $? -eq 0 ]; then echo 1 …`: reward 1 iff
  pytest exits 0, and pytest exits non-zero on both AssertionError and other exceptions, so all-P ⇔ exit 0 ⇔
  reward 1. `TESTS` order = grader file order (`test_outputs.py:7,12,21,38,47,83,92`). `TAGS` line numbers =
  `instruction.md:7,8,9,12,13,13` (read: lines 7-13). Case count 28 and 8 all-P predictions consistent with the
  frozen receipt headline (`cases=28 observed_pass=8 observed_fail=20 mismatches=0`).
- **Mutant table hygiene.** 21 rows (`:225`); `(direction == "silence") == (cls == "-")` guards the
  class/direction pairing (`:519-520`); `src.count(old) != 1` plus compile check make a drifted `old` string
  `invalid`, never a silent survive; O13 correctly absent (withdrawn as EQUIVALENT, recorded in the docstring).

## Residual risk

- Kill *quality* vs kill *existence*: a `silence` mutant crashing (rc=1) on any reject fixture counts as
  killed; an `error` mutant killed by a vacuous rc=2 fixture (F2). The `adv`/witness cells plus non-author
  battery review are the human control — admission should read which fixture killed what, not just the count.
- The order/ledger `classes()` regexes are format-coupled to pinned tool bytes; safe until a tool is
  legitimately edited, at which point PINS mismatch → all its mutants invalid (by design, not silent).
- Unpinned toolchain (bwrap path-pinned only, git, python3) and the unpinned census (F1) are the two inputs a
  lane-external change could move without any digest noticing; C1's verdict is otherwise fully digest-anchored.

## Verification gaps

- This seat executed none of the three scripts (frozen bytes; verdict runs belong to the wave executors).
  Every finding above is from source plus pinned-capture cross-reads; none is inferred from output I did not
  observe.
- `pkg_gate.py` is out of scope (frozen, separately reviewed): I verified only its pin and the V2 invocation
  (`--rerun --require-clean-tree`, receipt_sha256 filled by the counter, `:122-126`), not its P-checks.
- I did not re-derive the 21 `old` strings against tool bytes; `src.count(old) != 1` surfaces any drift as
  `invalid` during the real run, which is the cheaper check.

VERDICT: review-6-defects
