# CN1SiblingArgv — sibling overlap scan: entry-argv binding / ledger-truth / registry-closure

Seat: `CN1SiblingArgv` (connector, leaf, read-only). Date 2026-10-30. Lane `kengaku-shokunin`, base `798f5e9e…`.

**Question:** does any sibling lane already own entry-argv binding / ledger-truth /
registry-closure instruments? Plus: does the r14 standing ruling (no sibling owns an
evidence-replay gate) still hold at current sibling HEADs for the NEW round-55
instruments (argv binding `plans/round55_c2_entryargv.py`, multiset grader probe
`plans/round55_c3_chess_probe.py`)?

**Method:** read-only scan of the four named siblings' instrument dirs —
`kumitate-shokunin/scripts/` (it has no `tools/`; `scripts/` is its instrument dir),
`tameshi-shokunin/tools/`, `chousa-shokunin/tools/`, `kama-shokunin/tools/` — headers
and docstrings read in full for every name- or keyword-matching candidate; keyword
sweeps (`entry_argv|abbrev|wrapper|multiset|chess`, `advertised|registered|closure`,
`ledger`) across all four dirs to catch non-name candidates. No edits anywhere;
no subagent dispatch; no network.

**Sibling HEADs (re-derived this scan):**

| sibling | HEAD | dir scanned |
|---|---|---|
| kumitate-shokunin | `1e00955a657a5b955992e23915143e7b3e261bb4` | `scripts/` (35 entries; no `tools/`) |
| tameshi-shokunin | `9806562c7efc816bd979923e702ef39bc41cade7` | `tools/` (44 entries + `registry.json`) |
| chousa-shokunin | `a6b6f9396a825558edd1fdddaa2b43cb5f0a6bfe` | `tools/` (19 entries) |
| kama-shokunin | `3325e8ed86a5468156c963b98686d3598aa22e5f` | `tools/` (~90 entries) |

Note: fleet root also holds `kumitate-shokunin/`; it resolves to the same HEAD
`1e00955a…` as `kumitate-shokunin` (same repo, second mount). Scanned once.
`__pycache__/*.pyc` hits (e.g. a `chess` byte-sequence false positive in
`round59-c2-counter.cpython-314.pyc`) are excluded as binary noise.

## Per-sibling ruling table

### kumitate-shokunin @ 1e00955a — gate registries

| candidate | what it binds | ruling |
|---|---|---|
| `scripts/routed-ledger.mjs` (contract `kumitate-routed-ledger-v2`, r68) | Every verifier-spotcheck routed ITEM ↦ ≥1 row of `corpus/routed-ledger.md`, bound by a located 3–25-word quote unique in the section; closed/wontfix rows bind an answer at an exact `path:line` + quote inside the lane | **ADJACENT** — ledger-truth family, different data: routed-defect items ↔ ledger rows, not a counter ledger's declared `entry_argv`/evidence-fragment/exit-truth |
| `scripts/receipt-evidence.mjs` (contract `kumitate-receipt-evidence-v1`, r58) | A directory of attested receipts scored AS EVIDENCE at a judged rev: (1) LEDGER — every receipt verifies under `receipt-attest.mjs verify`; (2) REPRODUCTION — each receipt's recorded argv re-run inside a `git archive` extraction must reproduce the recorded exit and stdout/stderr sha256; (3) FRESHNESS — nonce sweep | **ADJACENT** — the closest sibling neighbor to an "evidence-replay gate" in the broad sense (hermetic re-execution to re-derive a verdict), but the replayed object is a recorded command invocation (argv+exit+output hashes), not committed model-probe records/statistics and not a TB2 grader |
| `scripts/receipt-attest.mjs` (v3, r53) | Records an invocation (argv, exit, stdout/stderr hashes, nonce); `verify --ledger` scans the WHOLE ledger dir and reads nonce reuse as REPLAY | **ADJACENT** — receipt anti-replay, different data |
| `scripts/counter-pins.mjs` (contract `kumitate-counter-pins-v1`, r54) | Lane's frozen round counters byte-identical to plan-frozen sha256 pins | **DIFFERENT-DATA** — pin integrity, not advertised-set closure or argv binding |
| `scripts/counter-rerun.mjs` (r48) | One counter run K times; final summary line byte-stable across runs | **DIFFERENT-DATA** — repeatability, not binding |
| `scripts/anchor-truth.mjs` (r38), `scripts/bind-oracle.mjs` (r49), `scripts/gate-mutants.mjs` (K43), `scripts/round-gate.mjs` | anchor truth vs pinned upstream; mount-namespace bind oracle; mutant-kill fence for kumitate's own gates; lane-local round-close pre-check | **DIFFERENT-DATA** (four separate instruments) |

### tameshi-shokunin @ 9806562c — mutation fences

| candidate | what it binds | ruling |
|---|---|---|
| `tools/command-binding.py` (schema `command-binding-v1`) | Declared required-command receipts against a digest-pinned, caller-owned expected bundle: exact name, argv (no shell normalization), canonical absolute cwd, full 40-hex revision, integer exit, required stdout tokens must all match | **ADJACENT** — the nearest neighbor to R55-C2's L1 argv-identity leg, but the trusted object is a caller-owned expected bundle, not the lane SKILL registry's declared entry row; it has no ledger↔registry binding, no interpreter-identity/wrapper leg, no flag-prefix-abbreviation leg (its own argparse merely sets `allow_abbrev=False`); execution-truth is not per-row hermetic ground truth against a registry declaration |
| `tools/registry-check.py` (r17 monitor, hardened) | Replays EVERY active row of `tools/registry.json` (schema `tameshi-entry-registry-v1`: name/kind/argv/expect.exit/stdout_contains/timeout/source/status) and reports how many rows still return their registered outcome; hermetic exec, cwd = lane root, scrubbed `GIT_*` env, shell=False | **ADJACENT** — same family as R55-C2's L4 (per-row execution ground truth of a declared registry) and as registry-truth monitors; different data: tameshi's own JSON registry (no SKILL-registry↔ledger binding, no wrapper/abbrev legs, stdout needles ≠ declared evidence fragments, no advertised-vs-registered closure) |
| `tools/registry-replay.py` (successor of r23 replay instrument) | Replays frozen registry requirements and projects a binding bundle; refuses to publish when any runner row did not hold (`RUNNER_NOT_HELD`) | **ADJACENT** — replays tameshi command rows, not model-probe evidence; different data |
| `tools/receipt-revision-gate.py` (r54/55, defect ER-R54-1) | Binds a receipt's `rev=` tokens to the certified revision: equality, ancestor, or path-identical content; named refusal codes, exit 3 refusals | **ADJACENT** — receipt↔revision binding; different data |
| `tools/executor-source-pin.py` | Declared executor source blobs at candidate rev == blobs at trusted rev | **DIFFERENT-DATA** — blob pin, not argv/ledger binding |
| `tools/golden-verdict.py` (r38) | Three-outcome golden comparison (diff exit 0/1/>1) | **DIFFERENT-DATA** |
| remaining: `mutate-and-run.sh`, `shrink-case.py`, `staged-id-guard.py`, `pbt-staged-id.py`, `tally-audit{,-v2,-v3}.py`, `write-path-census{,-v2,-v3,-v4}.py`, `witness-metadata.py`, `trace-inputs.py`, `env-diff.py`, `repeat-control.py`, `cold-read-forecast.py`, `bash-witness-study.py`, `context-capture.py`, `evidence-disposition.py`, `pin-disposition.py`, `mte-interop.py`, `round21-measure.py`, `receipt-measure.py`, `receipt-window.py`, `wave-accounting.py`, `wave-parent-settle.py`, `wave-route-mix.py` | mutation fences, tally hygiene, wave accounting, witness metadata | **DIFFERENT-DATA** (bulk ruling; headers read or keyword-swept, none binds entry-argv/ledger/registry-closure objects) |

### chousa-shokunin @ a6b6f93 — capture/citation

| candidate | what it binds | ruling |
|---|---|---|
| `tools/argv-witness.py` (r36) | Per-record, out-of-band witness that the pinned grep matcher ENGINE received a query for each record — one NUL-delimited argv record per engine invocation, attributed per record | **DIFFERENT-DATA** — name collision with "argv binding" only; it witnesses a research gate's matcher mechanism, never binds a ledger row's entry argv to a registry declaration |
| `tools/mechanism-witness.py` (r35) | PS4-trace witness that the gate's matcher functions were entered | **DIFFERENT-DATA** |
| `tools/receipt-pin.py` (r65) | A research receipt's header consistency (REVISION/EXIT/SHA256/path) against the pinned git blob (`git cat-file`, committed bytes never working tree) | **ADJACENT** — receipt↔blob consistency; explicitly "NOT execution authenticity", no ledger/registry binding |
| `tools/assimilate-rows.py` | Section-10 SOURCES assimilation; selftest compares expected-vs-observed FINDING lines "as multisets (a duplicated finding is a difference)" | **DIFFERENT-DATA** w.r.t. the multiset grader probe — the multiset object here is FINDING-line multisets in a selftest expected file, not grader verdict semantics over an artefact class; no TB2/chess surface |
| remaining: `research-gate.sh`, `lane-preflight.py`, `claims-audit{,-v2}.py`, `freeze-check.py`, `capture-{fetch,text}.py`, `build-spans.py`, `inference-ground.py`, `quote-reopen.py`, `store-record-audit.py`, `quarantine-check.py`, `absent-split.py`, `parent-lifetime.sh` | capture/citation gates and claim audits | **DIFFERENT-DATA** (bulk ruling) |

### kama-shokunin @ 3325e8ed — endpoint identity pins

| candidate | what it binds | ruling |
|---|---|---|
| `tools/gate-registry-check.py` (r28 repair, r34 widening) | Instrument-registry gate, occurrence + meaning: population = tracked counter paths (`.ufo/waves/round-*/count-*.py`, `tools/round<N>-*.py`); registry = the `\| Name \| Kind / entry command \| Exit map \| Self-test / pinned values \| Write scope \|` tables in SKILL.md; defects = thin-row / empty-entry / empty-exit-map / missing-path | **ADJACENT** — the nearest neighbor to R55-C1 registry closure, same advertised-vs-registered family, but DIFFERENT-DATA on both sides: population is tracked paths (not the advertised text set in LOG/SCORECARD/SKILL/README/knowledge), registry is SKILL.md tables (not a structured registry with verdict maps + self-test backing), legs are row-shape defects (not MISSING/INCOMPLETE/ENTRY-MISSING/SELFTEST-UNBACKED/DUPLICATE over advertised set × registry rows) |
| `tools/round43-registry-audit.py` | Self-description vs tree; `flags` leg binds each registered counter row's declared `--flag` tokens to `add_argument("--flag")` calls in the counter source at TIP | **ADJACENT** — declarative flag binding (registry cell ↔ source declaration), not ledger↔registry argv identity, no wrapper/abbrev legs, no execution |
| `tools/digest-ledger.py` (r38+) | Classifies every 64-hex token the lane's docs cite against the blob set (`registry/digest-ledger.tsv`) | **ADJACENT** — digest ledger; different data |
| `tools/round44-verdict-ledger-audit.py` | For every round × trend, lane self verdict beside outside-closure verdict, each read off a cited line; SCORECARD names disagreements | **ADJACENT** — verdict ledger; different data |
| `tools/instrument-agreement.py` | Runs one instrument N times over one tree; agreement = all digests equal | **DIFFERENT-DATA** — repeatability |
| `tools/round5x-replay-*-audit.py` family (`round47-live-replay-audit` … `round56-replay-code-audit`) + `tools/kama-live-replay.py` + `tools/kama-llamacpp-live.py` + `tools/echo-recheck.py` | Audits of the llama-server LIVE-replay probe: archive bytes read out of the running server's memory vs an independent download, memfd seals, no LD_PRELOAD/LD_AUDIT code-injection env, two-pass observation, post-exit re-hash | **DIFFERENT-DATA** — process/endpoint identity of a live server; replays nothing committed in the r14 sense |
| remaining: `append-only-audit.py`, `sources-append-only.py`, `release-recheck*.py`, `round3x–round64-*-audit.py` census family, `gguf-identity.py`, `hexrun-census.py`, `kama-{probe.sh,context-capacity,ollama-evidence,ollama-live,completion-live}`, `manifest-crosscheck.py`, `pin-{watch,trigger-consumed}.py`, `planned-pointer-check.py`, `prereg-time-check.py`, `report-landing-audit.py`, `seat-{report-immutability,yield}.py`, `shortcut-tally.py`, `test-snapshot.sh` | append-only/census/pin hygiene | **DIFFERENT-DATA** (bulk ruling) |

## Standing-ruling re-check: the r14 "no sibling owns an evidence-replay gate" ruling at current HEADs

The r14 ruling (SCORECARD r11/r14 rows; `corpus/evidence/round14-fleet/r14-connector.md`) was scoped by
the r11 connector to a *specific* object: "a hermetic, offline recomputation of committed **model-probe
records** and their derived run-summary/analysis" (`corpus/evidence/round11-fleet/r11-connector.md` §2).

**For the new round-55 instruments, at the HEADs above, the ruling still holds — with one explicit
narrowing of scope:**

1. **argv binding (`plans/round55_c2_entryargv.py`, R55-C2).** The sibling replay/binding instruments
   that exist at these HEADs — tameshi `registry-check.py` (re-execute registered argv rows),
   tameshi `registry-replay.py` (replay frozen registry requirements → binding bundle), tameshi
   `command-binding.py` (exact argv/exit/cwd/rev binding vs trusted expected bundle), kumitate
   `receipt-evidence.mjs` (recorded-argv reproduction inside a git-archive extraction), kama
   `round43-registry-audit.py` flags leg (declared `--flag` ↔ `add_argument`) — all replay or bind
   **their own lane's declared command sets** against their own trusted objects. NONE binds a
   *ledger row's* `entry_argv` token-equal to a *SKILL-registry declared entry*, none carries an
   interpreter-identity/no-wrapper leg (uv/pipx/poetry argv[0], inline `-c` programs), none a
   flag-prefix-abbreviation leg, none executes per-row ground truth against a registry declaration
   with declared evidence fragments. → **No sibling owner for the argv-binding instrument.
   DUPLICATE-INSTRUMENT RISK: NONE** (adjacent precedent to cite: tameshi `command-binding.py`,
   tameshi `registry-check.py`, kama `gate-registry-check.py`).

2. **Multiset grader probe (`plans/round55_c3_chess_probe.py`, R55-C3).** No sibling instrument models
   TB2 grader verdict semantics at all: `chess` appears nowhere in the four siblings' instrument dirs
   (only a `.pyc` byte false positive); TB2 is kengaku's own frontier. The only "multiset" in the scan
   is chousa `assimilate-rows.py`'s selftest expected-file comparison (FINDING-line multisets) — same
   mathematical object (order-insensitive multiset equality), different surface, different purpose.
   → **No sibling owner for the multiset grader probe. DUPLICATE-INSTRUMENT RISK: NONE.**

3. **Narrowing of scope (stated, not smoothed):** in the *broad* sense — "replay declared commands to
   re-derive a verdict" — tameshi (`registry-check.py`, `registry-replay.py`) and kumitate
   (`receipt-evidence.mjs`) already own replay-style gates over their own registries/receipts. The r14
   ruling's *model-probe* definition is untouched, but round-55 claims should not assert fleet novelty
   for "replay" per se; the novel construct is the **binding** (ledger↔registry argv identity +
   wrapper/abbrev legs + advertised-set closure), for which no sibling owner exists at these HEADs.

## Defects / anomalies observed (report-only, per contract)

- `kumitate-shokunin/` and `kumitate-shokunin/` both exist at fleet root and resolve to the same
  HEAD (`1e00955a…`) — second mount of the same repo, not a distinct lane. Scanned once.
- `kumitate-shokunin` has no `tools/` directory; the seat prompt's "tools dirs" for it is `scripts/`.
  All four siblings were reachable read-only; no write defects seen.
- Nothing at these HEADs contradicts the seat's premise: the four named siblings own gate registries
  (kumitate), mutation fences (tameshi), capture/citation (chousa), endpoint identity pins (kama) —
  and none owns an entry-argv binding, a ledger-entry-truth counter of the R55-C2 shape, a multiset
  grader probe, or an advertised-vs-registered closure gate of the R55-C1 shape.

No installs. No network. No writes outside this seat's wave dir. No subagents dispatched.
