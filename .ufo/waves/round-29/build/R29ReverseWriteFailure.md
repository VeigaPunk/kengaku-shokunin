# R29 ReverseWriteFailure — write-before-parse ordering and error phases (static)

Seat: KengakuR28.R29ReverseWriteFailure-2 (revenger, leaf; actual writer: this seat, 2026-10-21).
Lane root: /home/vgpnk/Projects/shokunin/kengaku-shokunin. Read-only seat: only this report and no
other lane writes. No installs/updates performed (none needed; stdlib only). No REA MCP, no network,
no host env reads, no upstream code executed or imported, no config_files outputs created.

## Scope and method

Bounded static reverse walk of the pinned upstream generator's write/parse ordering and per-phase
failure surface. Method: bytes read once, sha256-pinned, `ast.parse` on the fixture text (analysis
of pinned source as inert data, the lane's declared methodology), plus an in-memory stdlib census of
the pinned raw fixture. No filesystem mutation, no execution of generator code.

Pins verified before analysis:
- plans/fixtures/r29/generate_test_data.py — sha256 45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd, 838 bytes, 27 lines, all-ASCII. Matches manifest.json pin and round-29-claims.md.
- plans/fixtures/r28/webarena/config_files/test.raw.json — sha256 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652, 880776 bytes / 880776 codepoints, all-ASCII. Matches manifest pin.
- plans/fixtures/r29/profiles.json — 3 profiles x 6 values, all *.invalid synthetic (per-file "purpose" fields declare controlled-substitution, non-deployment).

## Phase map (exact locations, AST lineno:col_offset, all SOURCE)

Module body inventory (AST): Expr(docstring) L1-2, Import json L3, ImportFrom wildcard L5,
FunctionDef main L8, If __main__ guard L26-27. Nothing else. Bare calls in whole file: open,
enumerate, main. Attribute uses: read, replace, write, loads, dump. No os/subprocess/shutil, no
unlink/remove/rmtree — no cleanup construct exists anywhere in the file.

| Phase | Location | Statement | Failure surface |
|---|---|---|---|
| A import | L5 | `from browser_env.env_config import *` | [SOURCE construct / INFERENCE timing] import-time module failure aborts before L9; a missing wildcard-bound constant instead raises NameError at first use (L11), after the raw read but before any write. |
| B read | L9:C4 with, L10:C8 call | open test.raw.json "r"; `raw = f.read()` | FileNotFoundError/OSError; nothing written. |
| C replace | L11,L12,L13,L14,L15,L16 (each :C4) | six sequential str.replace: GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP | NameError only (missing constant); pure in-memory. Cascade: each pass also rewrites tokens injected by earlier passes' values (witness below). |
| D write test.json | L17:C4 with open "w", L18:C8 `f.write(raw)` | FIRST filesystem mutation; "w" mode truncate-at-open | OSError; truncation-before-write partial window (truncate semantics = Python stdlib fact, INFERENCE label). |
| E parse | L20:C4 | `data = json.loads(raw)` | json.JSONDecodeError — FIRST parse, strictly AFTER phase D. |
| F per-task writes | L21:C4 for, L22:C8 with open f"config_files/{idx}.json" "w", L23:C12 json.dump(item, f, indent=2) | enumerate(data) index naming, not task_id | OSError mid-loop leaves prefix 0..k-1 only; no try/except anywhere (AST: zero Try nodes), so every phase failure is an uncaught traceback. |

Core ordering fact (SOURCE): the serialized projected text is fully persisted to
config_files/test.json (L17-18) before the first parse (L20). Consequence chain (INFERENCE from
stdlib semantics, in-memory witnesses below): a phase-E failure leaves a persisted, non-round-tripping
test.json containing the projected-but-invalid text, zero per-task files written by this run, and any
prior run's config_files/{idx}.json files left entirely stale — no cleanup construct exists to remove
them. On the frozen input the stale set would be 812 files (prior-run hypothesis = INFERENCE; file
count 812 = SOURCE parse census below). A mid-loop phase-F I/O failure leaves a written prefix named
by enumerate index, so the surviving file set is index-contiguous, not task-id contiguous.

## Census results (in-memory stdlib; units stated)

Commands: sha256 via hashlib on file bytes; ast.parse on fixture text; raw.count/raw.find on decoded
fixture (occurrence counts and offsets in Unicode CODEPOINT units, per the round's provenance rule);
json.loads of pinned bytes and of in-memory projected strings. No files written.

- Parsed pinned raw: 812 tasks, 812 distinct task_id values, task_id JSON type int, index==task_id
  (int equality) for all 812 — text-level agreement with forecast F4's frozen-input half.
- Raw occurrence counts (exact token, codepoint units): __GITLAB__ 385 (first offset 42249),
  __REDDIT__ 336 (26080), __SHOPPING__ 281 (20068), __SHOPPING_ADMIN__ 300 (172), __WIKIPEDIA__ 0
  (find = -1: token absent from frozen input; the L15 pass is a no-op here — supports F2's zero
  remaining known tokens), __MAP__ 133 (6238). __SHOPPING_ADMIN__ does not contain __SHOPPING__ as a
  substring, so the L13-before-L14 order does not double-count on this input (SOURCE strings;
  substring check = census).
- In-memory projection, exact order L11-16, then json.loads: distinct_origins parses 812 tasks;
  path_prefix parses 812; trailing_slash_sensitivity parses 812 (F1 text-level agreement; NOT a
  runtime/deployment claim — no browser, no site, no file output).
- Phase-E quote witness (in-memory only): profile value with an embedded double quote produces
  JSONDecodeError at char 43026 (line 1415, col 48 of projected text) "Expecting ',' delimiter" —
  i.e., failure strictly in phase E, after phase D would have persisted test.json. Demonstrates the
  write-before-parse window without repair/escaping (matches the selftest's decode-failure-not-repair
  class).
- Phase-C cascade witness (in-memory): a GITLAB value embedding the literal __MAP__ token: after the
  L11 pass the text held 518 __MAP__ occurrences (133 original + 385 injected); after the L16 pass, 0
  remain. Earlier passes' replacement VALUES are consumed by later passes — the ordering is
  semantically load-bearing, not just cosmetic.

## Source-vs-inference boundary and new-construct boundary

SOURCE (pinned bytes/AST): all locations and statements above; six-token order; write-before-parse
ordering; enumerate-index naming; indent=2, no sort_keys, ensure_ascii default at L23; absence of any
encoding= argument at all four opens; absence of any cleanup/deletion construct; zero try/except.
INFERENCE (labeled): per-phase exception types and truncate/partial-write windows (Python stdlib
semantics, not upstream text); persisted stale/corrupt on-disk consequences (runtime filesystem
behavior, not executed here); NameError timing for missing wildcard names. UNKNOWNS preserved:
upstream runtime behavior never observed (locale-dependent default encoding of the four encoding-less
opens is latent only — both pinned inputs are all-ASCII, so zero impact on frozen bytes; effect on
other inputs unknown); actual env_config values never read (credentials boundary honored); no claim
about any harness runtime not executed by this seat.

New constructs contributed by this seat (novelty boundary): the phase A–F map with exact L:C anchors;
the write-before-parse persistence window (corrupt test.json round-trips to a decode failure) and the
no-cleanup stale-{idx}.json surface; the index-contiguity of partial phase-F output; the two in-memory
witnesses. No prior art for this ordering surfaced in plans/ or corpus/ (regex sweep for
write-before-parse / test.json write/parse phrasing: zero matches). The round's required finding class
projection_json_invalid covers phase E detection but does not name the persisted-artifact or stale-file
surfaces; those are this seat's additions. Boundary of validity: frozen pinned inputs and synthetic
*.invalid profiles only; not deployment, not task-validity, not model/browser behavior, no runtime
validity claim. plans/config_projection.py itself is absent from this read-only worktree checkout
(matches the claims doc's baseline-absence expectation); its behavior is L1's to verify — this report
makes no claim about it.

VERDICT: PASS
