#!/usr/bin/env python3
"""Build the round-55 wave-1 (v2, 70 seats) spec. Run from the lane repo root."""
import json

GODSPEED = "/skill:godspeed\n\nYou are a Godspeed-enabled subagent.\n\n1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n3. **Keep moves that improve any axis and harm none.**\n4. **Don't aim — let the frontier walk itself.**\n\n## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.\n"

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
WAVE = "kengaku-r55-w1"
BASE = "798f5e9ef30ef39291295565209b65a17343c00e"
FREEZE_COMMIT = "80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb"
SCRATCH = "/fast/scratch/hyaku/kengaku-r55"

CONTEXT = f"""# Goal
kengaku round 55, one v2 wave (build+attack), 70 seats. You are ONE seat of this wave.
The round's three claims are FROZEN before data: read {LANE}/plans/round-55-claims.md
(commit {FREEZE_COMMIT}) first — predicates, counters, kill rules and controls are fixed there;
no seat may change them. Base tip {BASE}; the freeze plus before-receipts are already landed.
Claims: R55-C1 operability 8->9 (registry closure via plans/round52_c2_registry.py),
R55-C2 calibration 9->10 (entry-argv structural binding via NEW plans/round55_c2_entryargv.py),
R55-C3 coverage attempt (13th TB2 grader chess-best-move executed offline).
# Contract (every seat)
- Write ONLY the files your item names. Other seats own different files; never "fix" a sibling's
  file — report the defect in your output instead. The L1 integrates and commits; seats never run
  a mutating git/jj command anywhere (no add/commit/push/stash/checkout/reset; read-only git
  with -C is fine). Never touch: MANIFEST.json, .ufo/state/, .ufo/watchdog.log, the fleet
  root's scripts/ or templates/, any sibling repo, .scratch/.
- Scratch root for every clone/fixture/work dir: {SCRATCH}/<your-seat-name>/ (create it;
  mkdir -p; pass it explicitly; never rely on inherited TMPDIR; /tmp only for files <50 MB).
  A committed tool must honour a --work/--receipt argument and never hardcode /tmp.
  Before yielding, delete your scratch dir (trap 'rm -rf -- "$S"' EXIT / finally: shutil.rmtree),
  after copying receipts into your named outputs under {LANE}/.ufo/waves/round-55/w1/<your-seat-name>/.
- One live clone per seat: git clone --shared or git worktree add; never a full mirror.
- Every `Report:` trailer path in your prompt is relative to the lane repo — write it at
  {LANE}/<that path>. Write your final report as {LANE}/.ufo/waves/round-55/w1/<your-seat-name>/report.md
  (create the dir) with: what you ran, commands + exit codes, files you wrote, defects found,
  dead ends. An unrun check has NOT passed — report honestly.
- Host is shared: at most ~90 seats fleet-wide run at once; provider backoff — respect it and
  continue the same work; never restart a duplicate writer.
- Tooling authorization (operator 2026-10-19): you may install/upgrade tools that help via
  `uv tool install` / `npx` / official release binary into ~/.local/bin. ALL pacman transactions
  are PAUSED host-wide (never -S/-Sy/-Syu/-U/-R, never restart a host service). Record any
  install (tool, version, channel, reason) in your report.
- Network: read-only GETs to raw.githubusercontent.com / api.github.com / docs sites are fine.
  No POST/auth endpoints, no model-serving endpoints, no benchmark runs.
- Leaves: do not spawn subagents (the executor card's single read-only labrat probe excepted).
- Never message agent://all."""

A = ["operability"]
B = ["calibration"]
C = ["coverage"]
X = ["operability", "calibration"]
items = []


def add(name, role, axes, text):
    items.append({"name": name, "role": role, "axes": axes, "item": GODSPEED + text})


NEW_ROWS = ("round54-c1 (python3 plans/round54_c1_anchor.py), round54-c2 (python3 "
            "plans/round54_c2_entrytruth.py), round55-c2 (python3 plans/round55_c2_entryargv.py), "
            "round55-c2-controls (python3 plans/round55_c2_controls.py), round55-c3 "
            "(python3 plans/round55_c3_chess_probe.py)")

# ---------------- executors (16)
add("E1RegistryRows", "executor", A, f"""# Target
{LANE}/SKILL.md — ONLY the `## Gate/probe registry` table (nothing else in the file).
# Change
Append exactly five rows, in this order, to the registry table: {NEW_ROWS}.
Cell contract (8 columns: name | kind | entry | verdict map | self-test | pinned | scope | owner):
- entry cell: the first backtick span MUST be exactly `python3 plans/<script>.py` plus only flags
  the script actually implements — read each script's argparse FIRST
  (plans/round54_c1_anchor.py, plans/round54_c2_entrytruth.py, plans/round55_c2_controls.py
  already exist; plans/round55_c2_entryargv.py and plans/round55_c3_chess_probe.py are being
  built this wave with the frozen CLI contracts: entryargv `--lane --source --work --jobs
  --timeout --dry --selftest`; chess probe `--lane --receipt --selftest`). If a flag is not in
  the script body yet but IS in its frozen contract, write the row with that flag and note
  "flag per frozen contract" in the self-test cell.
- verdict map: `0`/`1`/`2` semantics copied from each script's docstring.
- self-test cell: name the script's real selftest flag if implemented (--selftest), else write
  `none declared` — never claim a flag the script lacks (the SELFTEST-UNBACKED leg greps the body).
- pinned: the sha256 (first 8+ chars) of each script file; scope: what the gate decides; owner: kengaku.
# Acceptance
`python3 plans/round52_c2_registry.py --lane {LANE}` printed on your tree afterwards reports
MISSING 0 (it may still report other legs until sibling seats land — that is expected; report
what you saw). No other SKILL.md byte changes (`git -C {LANE} diff --stat -- SKILL.md` names one file).
# Bounds
Write only SKILL.md. Scratch under {SCRATCH}/E1RegistryRows/.
""")

add("E2EntryArgvCounter", "executor", B, f"""# Target
NEW file {LANE}/plans/round55_c2_entryargv.py — the R55-C2 binding counter (frozen contract in
plans/round-55-claims.md §R55-C2; DO NOT modify plans/round54_c2_entrytruth.py — import it).
# Change
- Import the r54 module (importlib, same pattern as plans/round55_c2_controls.py::_load) and
  reuse registry_rows, row_script, load_ledger, hermetic_env, Worker, run_row, git_rev,
  MIN_REASON_WORDS, REGISTRY/LEDGER/SCHEMA constants.
- registry_entry_argv(line): parse the FIRST backtick span in the entry cell that starts with
  `python3`; shlex.split it; return the token list (None if absent).
- binding_static_legs(root): r54 static legs PLUS three new defect lists, each printed on its
  own ROWS-line field and its own `  <TAG> <name>: <why>` line:
  L1 ARGV-DEFECT — ledger row entry_argv tokens != registry cell tokens (exact list equality);
  L2 WRAPPER-DEFECT — argv[0] not in {{python3, python}}, or any argv token is a known wrapper
  (uv/pipx/poetry/npx/uvx) or starts with `-c` (inline program);
  L3 ABBREV-DEFECT — a flag token that does NOT appear verbatim in the script body but IS a
  proper prefix of a flag string that does appear (catches argparse prefix abbreviation
  without executing).
- evaluate(lane, source, work, jobs, timeout, dry): identical shape to r54's evaluate — same
  ROWS line plus `wrapper_defect=N abbrev_defect=N`, same RUN/TIPSTATE/MIGRATION lines, plus a
  `BINDING l1=N l2=N l3=N` line; predicate line `PREDICATE R55-C2 pass|fail`; exit 0/1/2.
  static_ok now also requires the three new defect lists empty. Execution per row uses the
  REGISTRY cell argv (identical to ledger argv once L1 is clean) through r54's Worker/run_row
  (hermetic env, scratch work dir argument, per-row timeout). `--dry` runs static legs only.
- CLI: `--lane --source --work --jobs --timeout --dry --selftest` exactly.
- --selftest (temp fixtures under the --work dir or TMPDIR, never /tmp hardcoded): (1) truthful
  fixture passes; (2) ledger-tampered argv fixture -> ARGV-DEFECT + fail; (3) uv wrapper fixture
  -> WRAPPER-DEFECT + fail; (4) --selft abbreviation fixture -> ABBREV-DEFECT + fail. Reuse the
  fixture-building shape of plans/round55_c2_controls.py (argparse gate whose --selft abbreviates).
# Acceptance
`python3 plans/round55_c2_entryargv.py --selftest` exits 0 printing one line per case;
`--dry --lane {LANE}` exits 0/1 with the ROWS line printing current static state (it WILL show
defects on the working tree mid-wave — expected; report them, fix nothing outside your file).
# Bounds
Write only plans/round55_c2_entryargv.py. Scratch under {SCRATCH}/E2EntryArgvCounter/.
""")

add("E3ControlsVerify", "executor", B, f"""# Target
Verify the frozen fixture builder {LANE}/plans/round55_c2_controls.py (already committed at
{FREEZE_COMMIT}); write nothing in the lane tree.
# Change
Run, capturing full output: (1) `python3 plans/round55_c2_controls.py --selftest`;
(2) `--case abbreviated-selftest --against r54`; (3) `--case uv-decoy-script --against r54`.
Compare each against the committed receipts {LANE}/.ufo/waves/round-55/claims/
c2-before-abbreviated-selftest.txt and c2-before-uv-decoy-script.txt: the PREDICATE/ROUTE/EXIT
lines must match (fixture revision hashes differ — that is expected; say so).
# Acceptance
report.md carries all three outputs, the diff-vs-receipt analysis, and any drift finding.
# Bounds
Scratch under {SCRATCH}/E3ControlsVerify/. No lane writes.
""")

add("E4LedgerTruth", "executor", B, f"""# Target
{LANE}/plans/round54-entrytruth.json — data corrections only (R55-C2's ledger truth step; the
file is the lane's self-assessment ledger, schema r54-entrytruth-v1, 78 rows).
# Change
Work on a clean shared clone at {BASE} + the working tree; measure BEFORE you declare.
1. Row `round35-c1-coverage`: run `python3 plans/round35_c1_verify.py --lane <clone>` — capture
   the FULL output. Its declared evidence fragment no longer appears (r54 receipt:
   EVIDENCE-MISSING round35-c1-coverage). Correct the row truthfully: entry_exit/entry_state
   from the observed run, evidence = a verbatim ≥6-char fragment of the CURRENT output, reason
   (red rows) ≥10 words explaining the current state. Commit the observed output as
   .ufo/waves/round-55/w1/E4LedgerTruth/round35-c1-output.txt.
2. Add ledger rows for the five registry rows landing this round ({NEW_ROWS}) — each declared
   from ITS OWN measured behavior via a r54-style hermetic run (import r54 module, Worker/
   run_row pattern, scratch work dir): round54-c1 and round54-c2 entries with their real flags;
   round55-c2 bare entry exits 2 SETUP (`SETUP --source and --work are required unless --dry`)
   — declare red with that evidence and a ≥10-word reason; round55-c2-controls bare entry runs
   argparse-required group (declare what you measure); round55-c3 bare entry runs the real
   probe (if its file is absent when you measure, declare truthfully what you observed and say
   the row needs the L1's re-measure at integration — do not guess).
3. Touch NO other row. Keep schema/keys/shapes identical to existing rows (chosen/entry_argv/
   entry_exit/entry_state/reason/evidence/timeout_s/sec as applicable).
# Acceptance
`python3 -c "import json;d=json.load(open('{LANE}/plans/round54-entrytruth.json'));print(len(d['rows']))"`
prints 83 (78 + 5) unless you measured otherwise — report the exact count. JSON parses; no row
elsewhere changed (diff shows only your edits).
# Bounds
Write only plans/round54-entrytruth.json + your report/outputs under
.ufo/waves/round-55/w1/E4LedgerTruth/. Scratch under {SCRATCH}/E4LedgerTruth/.
""")

CASES = [
    ("both-lowercase-two-lines", "g2g4\\ne2e4\\n", "PASS"),
    ("both-space-separated", "g2g4 e2e4", "PASS"),
    ("reversed-order", "e2e4 g2g4", "PASS"),
    ("single-move-only", "g2g4\\n", "FAIL"),
    ("uppercase-white", "G2G4\\ne2e4\\n", "FAIL"),
    ("extra-decoy-move", "g2g4\\ne2e4\\na2a3\\n", "FAIL"),
    ("duplicate-move", "g2g4\\ne2e4\\ne2e4\\n", "FAIL"),
    ("whitespace-padded", "  g2g4   e2e4  \\n\\n", "PASS"),
    ("empty-file", "", "FAIL"),
    ("crlf-line-endings", "g2g4\\r\\ne2e4\\r\\n", "PASS"),
    ("instruction-example-h1h8", "h1h8\\ne2e4\\n", "FAIL"),
    ("fullwidth-unicode-digit", "g\\uFF12g4\\ne2e4\\n", "FAIL"),
]
# Frozen requirement mapping (for the entry, not the probe): the 8 PASS/FAIL semantics are
# derived only from the grader's single assertion at tests/test_outputs.py:25; S1CaseProse
# owns the per-case requirement prose.

add("E5ChessProbe", "executor", C, f"""# Target
NEW file {LANE}/plans/round55_c3_chess_probe.py — the R55-C3 instrument (frozen contract in
plans/round-55-claims.md §R55-C3).
# Change
- Case table: EXACTLY these 12 frozen cases (name | move.txt bytes | predicted), embedded with
  predictions written NOW, before the first run — do not run the grader before the table is in
  the file:
{chr(10).join(f'  {n} | {b!r} | {p}' for n, b, p in CASES)}
- Per case: materialize /app/move.txt content in a case dir; materialize /tests/test_outputs.py
  as a byte-copy of {LANE}/corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py
  (read it, do not fetch the network); run in a bubblewrap sandbox:
  `bwrap --unshare-all --die-with-parent --ro-bind /tests <t> --bind <casedir> /app --tmpfs /tmp
   --tmpfs /home --proc /proc --dev /dev python3 -c "import sys; sys.path.insert(0,'/tests');
   import test_outputs as t; t.test_move_correct()"` (adapt bind targets to your layout; keep
  /tests read-only and /app case-owned and writable; verify bwrap exists else exit 2 SETUP).
- observed PASS = exit 0; observed FAIL = nonzero exit with AssertionError in output; anything
  else (bwrap error, missing file, OSError) = SETUP error for that case -> print it, exit 2.
- Output: one `CASE <name> predicted=<P|F> observed=<P|F> rc=<n>` line per case, then
  `cases=12 observed_pass=P observed_fail=F mismatches=M` where M counts observed!=predicted;
  final `PREDICATE R55-C3 pass` iff M==0 else `fail`; exit 0 iff pass, 1 fail, 2 setup.
- CLI: `--lane` (default .), `--receipt <path>` (also tee the full output there), `--selftest`:
  runs the same bwrap pipeline against a toy test file + toy artefacts (2 internal cases, one
  pass one fail) proving the plumbing without touching the TB2 capture; prints
  `SELFTEST cases=2 failures=N`.
- No network, no /tmp hardcode (scratch dirs under the --work argument or TMPDIR).
# Acceptance
`python3 plans/round55_c3_chess_probe.py --selftest` exits 0. Do NOT run the real 12-case
battery (a sibling seat runs it) — but if you do run it once to verify, keep the output and say
so in report.md; the prediction table is already frozen either way.
# Bounds
Write only plans/round55_c3_chess_probe.py. Scratch under {SCRATCH}/E5ChessProbe/.
""")

add("E6ChessReceipt", "executor", C, f"""# Target
{LANE}/corpus/evidence/round55/chess-best-move-probe.txt — the R55-C3 receipt (the run output).
# Change
Wait for {LANE}/plans/round55_c3_chess_probe.py to exist (check every 60 s, up to 25 min; if
still absent, report SETUP-absent honestly and stop). Then run TWICE from a clean shared clone
at the CURRENT lane tip:
  python3 plans/round55_c3_chess_probe.py --lane <clone> --receipt <scratch>/run1.txt
  python3 plans/round55_c3_chess_probe.py --lane <clone> --receipt <scratch>/run2.txt
Byte-compare run1 vs run2 (determinism; probe output must not embed timestamps/paths that
differ — if they differ, report the diff and the offending lines). Land the FIRST run's bytes at
corpus/evidence/round55/chess-best-move-probe.txt (mkdir -p the dir) and both runs + the cmp
result under .ufo/waves/round-55/w1/E6ChessReceipt/.
# Acceptance
The receipt's summary line reads `cases=12 observed_pass=P observed_fail=F mismatches=0` with
P+F=12 and `PREDICATE R55-C3 pass` — or, if any mismatch/setup, the receipt lands anyway and
your report says exactly what mismatched (an honest red receipt is landing evidence; do not
tune cases — they are frozen).
# Bounds
Write only corpus/evidence/round55/chess-best-move-probe.txt + your wave dir. Scratch under
{SCRATCH}/E6ChessReceipt/.
""")

add("E7KnowledgeEntry", "executor", C, f"""# Target
{LANE}/corpus/knowledge/tb2-chess-best-move-grader.md — the R55-C3 knowledge entry.
# Change
Wait (60 s steps, max 25 min) for {LANE}/corpus/evidence/round55/chess-best-move-probe.txt.
Write the entry per corpus/QUALITY.md Q1-Q17:
- first three lines: `source:` (S201 grader URL+anchor, S202 instruction URL+anchor, S109 runner —
  URLs in plans/round-55-claims.md §R55-C3 and the planned SOURCES rows in the E8 item text),
  `verified-at:` (today, this round's receipts), `recheck:` (the exact receipt re-run command).
- body (research-note structure per SKILL.md): one-line thesis; evidence table = the 12 frozen
  cases with predicted/observed raw from the receipt (copy, do not re-derive); mechanism section
  (order-insensitive full-multiset equality over whitespace-split tokens; no case/unicode
  normalization; strip+split tolerance; duplicates break equality; the instruction's example
  literal h1h8 is not a winner per the grader pair); limits section (does not establish chess
  correctness, task validity, the image's content, model performance, contamination; one task
  of 89; the graded artefact is an agent-authored token file — class distinction from r45's
  line-split membership F1 (password-recovery) — full-multiset equality, no partial credit).
- connections: [[benchmark-verifier-execution-model]], r45/r46 entries — one line each why.
- Q13/Q14: leave admission to the L1; put `second-seat re-read: pending (R3)` honestly.
If the receipt never lands, write NOTHING and report SETUP-absent.
# Acceptance
Entry exists, cites S201/S202/S109 with anchors + sha256 pins, carries the raw 12-row table,
and names its limits. No capability or score claim inside the entry.
# Bounds
Write only corpus/knowledge/tb2-chess-best-move-grader.md. Scratch {SCRATCH}/E7KnowledgeEntry/.
""")

S201_ROW = ("| S201 | Terminal-Bench 2.0 chess-best-move task grader (tests/test_outputs.py) — "
            "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
            "2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/tests/test_outputs.py | code | A | "
            "the executed scoring predicate of one Terminal-Bench 2.0 task at a pinned commit — "
            "which output property test_move_correct asserts and how — for the code's own behaviour; "
            "the docstring's mate-in-one reading is the authors' self-report | commit "
            "2fd12b88aafdd04a52c298e3940bcb189f9766d6, tests/test_outputs.py:25 \\\"assert sorted(move) == "
            "sorted([\\\\\\\"g2g4\\\\\\\", \\\\\\\"e2e4\\\\\\\"])\\\" (6 words); sha256 "
            "a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286 | the task score is one "
            "assertion: the whitespace-split token multiset of /app/move.txt must equal the sorted pair "
            "g2g4+e2e4 exactly — order-free, no partial credit, no case or unicode normalization | mined | "
            "2026-10-30 | 180d | corpus/knowledge/tb2-chess-best-move-grader.md |")
S202_ROW = ("| S202 | Terminal-Bench 2.0 chess-best-move task instruction (instruction.md) — "
            "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
            "2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/instruction.md | docs | A | "
            "the requirement bullets this one task states to the agent at a pinned commit, as the "
            "maintainer's own specification the grader is mapped against | commit "
            "2fd12b88aafdd04a52c298e3940bcb189f9766d6, instruction.md:1 \\\"If there are multiple winning "
            "moves, print them all, one per line.\\\" (12 words); sha256 "
            "6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a | one-line requirement "
            "sentence: read a board image, write best move(s) for white to /app/move.txt, all winning "
            "moves one per line — the grader hardcodes the two-move pair, so the plural rule is "
            "score-critical | mined | 2026-10-30 | 180d | corpus/knowledge/tb2-chess-best-move-grader.md |")

add("E8SourcesRows", "executor", C, f"""# Target
{LANE}/corpus/SOURCES.md — append exactly two rows (append-only; nothing else changes).
# Change
Verify first: the registry's highest existing id (grep the last S-row; expect S200) and that no
chess row exists. Then append, directly under the last row of the Registry table, these two rows
 verbatim (fix ONLY if the column count is wrong — 11 columns, no literal pipe inside cells):
{S201_ROW}
{S202_ROW}
Both rows were OPENED this round by the L1 (2026-10-30; upstream bytes fetched and sha-pinned;
quotes located at tests/test_outputs.py:25 and instruction.md:1). status mined with used-by the
entry path. Then run:
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
and save full output + exit code to .ufo/waves/round-55/w1/E8SourcesRows/census-after-rows.txt.
Exit 0 required (the 15 pre-existing W04 duplicate-URL warnings are known and fine; any NEW
W04/E03/E04 finding on YOUR rows is a defect to fix before yielding).
# Acceptance
`grep -cE '^\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|' {LANE}/corpus/SOURCES.md` prints 195
(193+2). Census exit 0.
# Bounds
Write only corpus/SOURCES.md + your wave dir. Scratch {SCRATCH}/E8SourcesRows/.
""")

README_PARA = ("- *Partly discharged round 55 (2026-10-30):* `knowledge/tb2-chess-best-move-grader.md` "
               "reads and executes a thirteenth Terminal-Bench 2.0 task's scoring code "
               "(`chess-best-move/tests/test_outputs.py` @ `2fd12b88`; S201, S202; runner semantics "
               "cite held S109 — the chess `test.sh` is byte-identical to the regex-log runner) against "
               "its `instruction.md`, probe `plans/round55_c3_chess_probe.py`, receipt "
               "`corpus/evidence/round55/chess-best-move-probe.txt`. The graded artefact is an "
               "agent-written move-token file judged by order-insensitive FULL-MULTISET equality over "
               "whitespace-split tokens — a class distinct from round 45's line-split membership: "
               "partial answers fail, order is free, duplicates break equality, and no case or unicode "
               "normalization exists, so the instruction's own example literal h1h8 would fail. "
               "`cases=12 observed_pass=P observed_fail=F mismatches=0` (fill from the receipt). "
               "The clause is **narrowed for that one task only**; it stays open for the remaining "
               "TB2 task graders (13 of 89 read), for any SWE-bench Pro V2 grader beyond the "
               "round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane).")

add("E9IndexAndReadme", "executor", C, f"""# Targets
{LANE}/corpus/README.md and {LANE}/PROVINCE.md — index parity + frontier narrowing (R55-C3 landing).
# Change
README.md: (1) add the knowledge index row for corpus/knowledge/tb2-chess-best-move-grader.md
(match the existing table's column shape exactly); (2) add the evidence row for
corpus/evidence/round55/ (dir + probe receipt; match the evidence table shape); (3) in `## Frontier`,
append as a new sub-bullet under the agentic-benchmark item: {README_PARA}
(adjust only the `observed_pass=P observed_fail=F` fill from the receipt if present; if the
receipt is absent when you finish, keep the literal `P`/`F` placeholders OUT — write
`cases=12` with the counts left as `(receipt pending at index time; see the receipt)`).
PROVINCE.md: append at the end a `## Round55 partial frontier admission (2026-10-30)` section
with one Core-addition paragraph: static interpretation + offline synthetic-fixture execution of
the chess-best-move grader at the pin; what it owns (reading/executing captured scoring code);
what it refuses (task image, harness, real submissions, runtime validity, contamination, model
behaviour, the remaining 86 unread graders); the 12->13 narrowing sentence; reported-out: none
absorbed. Match the established section style (round 37/38 paragraphs).
# Acceptance
`grep -c chess-best-move {LANE}/corpus/README.md` >= 3 and `{LANE}/PROVINCE.md` contains
`13 of 89 read`. Both files parse as before (no broken tables).
# Bounds
Write only README.md + PROVINCE.md + your wave dir. Scratch {SCRATCH}/E9IndexAndReadme/.
""")

add("E10NoharmRuns", "executor", X, f"""# Target
No-harm evidence for the round: the lane's standing gates still hold while round-55 bytes land.
# Change
From a clean shared clone at the CURRENT lane tip (re-clone fresh when you start; the tip moves
during the wave — record the rev you measured), run and capture (command + exit code each):
1. `python3 grader.py` (expect CHECKS n=733 mismatches=0, VERDICT PASS, exit 0)
2. `python3 grader.py --selftest` (expect ALL PASS, exit 0)
3. `python3 plans/round52_c2_registry.py --selftest` (expect SELFTEST cases=3 failures=0)
4. `python3 plans/round55_c2_controls.py --selftest` (expect cases=4 failures=0)
5. `python3 plans/round51_surfaces.py --lane <clone>` (expect ANCHORS 20/20 + PREDICATE R51-C1 pass)
6. `python3 plans/defect_ledger.py --lane <clone>` (record the open/closed counts verbatim)
7. `python3 plans/round54_c2_entrytruth.py --selftest` (expect its own selftest green)
Save each output under .ufo/waves/round-55/w1/E10NoharmRuns/<name>.txt with the rev recorded in
report.md. A non-green result is a FINDING, not something to fix — report it exactly.
# Acceptance
All seven outputs captured with exit codes; report.md lists rev + per-check verdict table.
# Bounds
No lane writes. Scratch {SCRATCH}/E10NoharmRuns/.
""")

add("E11SelftestReceipts", "executor", A, f"""# Target
C1 frozen leg 2 evidence: every registry row ADDED in round 55 had its self-test executed with
the observed verdict matching the row's verdict-map cell.
# Change
Wait (60 s steps, max 25 min) for the five new rows to appear in {LANE}/SKILL.md's
`## Gate/probe registry` ({NEW_ROWS}). For each row: extract the entry + self-test cells; run the
claimed self-test command from a clean shared clone at the current tip; capture output + exit;
compare to the verdict-map cell text. Save per-row receipts under
.ufo/waves/round-55/w1/E11SelftestReceipts/<row>.txt and a summary table in report.md.
Any mismatch (claimed flag absent, exit semantics differ) is a FINDING against C1 leg 2 —
report it exactly; do not edit SKILL.md (E1 owns it; the L1 arbitrates).
# Acceptance
Five receipts + summary; every mismatch named with command + exit + the cell text claimed.
# Bounds
No lane writes. Scratch {SCRATCH}/E11SelftestReceipts/.
""")

add("E12ScratchHygiene", "executor", X, f"""# Target
Scratch-discipline + disk audit for round 55 (addendum §7 duty).
# Change
1. `df -h /fast/scratch /tmp` — record free space.
2. Read the round's new/changed scripts (plans/round55_c2_controls.py and, when present,
   plans/round55_c2_entryargv.py, plans/round55_c3_chess_probe.py): verify no hardcoded /tmp,
   that work dirs honour an argument or TMPDIR, and that fixtures clean up. Report per script.
3. `find /fast/scratch/hyaku/kengaku-r55 -maxdepth 1 -type d | sort` — record seat dirs present
   (this is a mid-wave census, not a cleanup pass; do NOT delete other seats' dirs).
4. Check `ls /tmp` for any kengaku-r55 artifacts (expect none; report any).
# Acceptance
report.md carries the four sections with verbatim outputs; any violation named with file:line.
# Bounds
Read-only + your wave dir. Scratch {SCRATCH}/E12ScratchHygiene/.
""")

add("E13BindingScan", "executor", B, f"""# Target
Pre-integration data for R55-C2: enumerate how the CURRENT ledger/registry pair scores under
the frozen binding legs (before the new counter exists).
# Change
From a clean clone at the current tip: parse SKILL.md's registry rows (first backtick span
starting with python3 -> shlex tokens) and every ledger row in plans/round54-entrytruth.json.
Classify each of the 78 rows: L1-OK (tokens equal) / L1-DIFF (list the token diff);
L2 flag (argv[0] or wrapper/inline tokens); L3 flag (flag token not verbatim in the script body
but a proper prefix of one that is — read each referenced script's body). ALSO flag rows whose
registry cell command cannot be parsed (no backtick python3 span). Write the full 78-row table
to .ufo/waves/round-55/w1/E13BindingScan/binding-scan.tsv (columns: row, l1, l2, l3, note) and
a summary in report.md: counts per class + the list of rows E4/L1 must correct as data.
# Acceptance
Table covers all 78 rows; summary counts reconcile; at minimum the two r54 laundering routes are
absent from the REAL ledger (they were fixture-only) — say so explicitly.
# Bounds
No lane writes. Scratch {SCRATCH}/E13BindingScan/.
""")

add("E14CaptureIdentity", "executor", C, f"""# Target
Byte-identity receipt for the R55-C3 capture (the freeze asserts it; prove it on committed bytes).
# Change
1. sha256sum the in-repo captures: corpus/evidence/round52/graders/chess-best-move/tests/
   test_outputs.py, tests/test.sh, and regex-log/tests/test.sh (runner-identity cross-check:
   chess test.sh sha must equal 4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334
   AND equal the regex-log runner sha).
2. Fetch (read-only GET) the upstream files at pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6:
   chess-best-move/tests/test_outputs.py, tests/test.sh, instruction.md, task.toml from
   raw.githubusercontent.com/harbor-framework/terminal-bench-2/<pin>/...; sha256 each; compare.
3. `curl -fsS https://api.github.com/repos/harbor-framework/terminal-bench-2/commits/<pin>`
   — record sha + commit date (pin exists).
Save everything to .ufo/waves/round-55/w1/E14CaptureIdentity/identity.txt.
# Acceptance
All three sha256 pairs match (or every mismatch named — a mismatch fires the C3 kill rule).
# Bounds
Read-only + your wave dir. Scratch {SCRATCH}/E14CaptureIdentity/.
""")

add("E15DefectLedgerSweep", "executor", X, f"""# Target
Open routed-defect state for the round lesson (Q23 duty).
# Change
1. `python3 plans/defect_ledger.py --lane <clean clone>` — capture verbatim.
2. Read corpus/defects.jsonl: list every row with status open, each with its check name.
3. For each open row: run (or read, if the check is expensive) its named check at the tip and
   record still-open/closed-mismatch. In particular the r52-repair carry (order-check regression
   + masked K7 control): verify it is still an open row and name its check.
4. Write the table to .ufo/waves/round-55/w1/E15DefectLedgerSweep/open-rows.md.
# Acceptance
Every open row has a current state + evidence pointer; discrepancies named exactly.
# Bounds
No lane writes. Scratch {SCRATCH}/E15DefectLedgerSweep/.
""")

add("E16Drafts", "executor", X, f"""# Target
DRAFT files (NOT the shared files — the L1 splices): .ufo/waves/round-55/w1/E16Drafts/
log-entry.md, scorecard-section.md.
# Change
Read plans/round-55-claims.md + .ufo/waves/round-55/claims/*.txt (committed before-receipts) and
LOG.md's round-53/54 entries for house style. Draft:
1. log-entry.md — `## Round 55 ...` entry: base tip, freeze commit {FREEZE_COMMIT}, the three
   claims with their frozen before commands + observed before outputs (quote the receipts),
   wave shape placeholder `(wave w1: <N> seats, role mix — L1 fills after settle)`, and empty
   `### Round-55 measured close` subsection with placeholder markers the L1 fills.
2. scorecard-section.md — `### Planned (round 56)` skeleton + a `## Round 55` claims table with
   before column filled from the receipts and after cells marked `(measured close pending)`.
Mark every number you could not verify as `PENDING-L1`. Do not invent results.
# Acceptance
Two draft files, house style matched, no fabricated numbers.
# Bounds
Write only your wave dir. Scratch {SCRATCH}/E16Drafts/.
""")

# ---------------- scribes (6)
add("S1CaseProse", "scribe", C, f"""# Target
.ufo/waves/round-55/w1/S1CaseProse/case-requirements.md — prose mapping each of the 12 frozen
chess probe cases to the instruction requirement it exercises (E7 consumes).
# Change
Read the frozen case list in the E5 item of the wave spec (or .ufo/waves/round-55/w1-dispatch.json
once written) and the instruction text (S202 row). For each case: requirement exercised (quote
the instruction words), why the predicted verdict follows from the grader's ONE assertion
(tests/test_outputs.py:25), and what a contrary verdict would mean. Keep it under 120 lines.
# Acceptance
12 sections, each naming requirement + grader line + prediction rationale.
# Bounds
Write only your wave dir.
""")

add("S2PriorArt", "scribe", C, f"""# Target
.ufo/waves/round-55/w1/S2PriorArt/prior-art.md — prior-art pricing for the R55-C3 class claim.
# Change
Web-search (read-only): are public writeups/papers describing (a) the TB2 chess-best-move task
or its grader, (b) order-insensitive multiset/set-equality output graders in agent benchmarks,
(c) benchmark grader semantics surveys covering token-set scoring? For each hit: URL, what it
establishes, phenomenon-new vs instrument-new verdict for this lane's reading. Price honestly:
if the class is already published, say the entry is a replication of the class, novel only as
this lane's instrument instance.
# Acceptance
>=3 evaluated hits with URLs + verdicts; a final `PRICING:` line.
# Bounds
Write only your wave dir.
""")

add("S3GateQuotes", "scribe", C, f"""# Target
.ufo/waves/round-55/w1/S3GateQuotes/gate-block.md — the round lesson's `## Gate` row table for
the two new SOURCES rows (the L1 splices it into corpus/lessons/round-55.md).
# Change
Rows S201 + S202, columns: row | URL and location | access date | located quote (<=25 words) |
decision. Use exactly: S201 — URL .../chess-best-move/tests/test_outputs.py, location
tests/test_outputs.py:25, access 2026-10-30, quote: assert sorted(move) == sorted(["g2g4", "e2e4"])
(5 words), decision: admit A, executed scoring predicate for the code's own behaviour. S202 —
URL .../chess-best-move/instruction.md, location instruction.md:1, access 2026-10-30, quote:
If there are multiple winning moves, print them all, one per line. (12 words), decision: admit A,
maintainer requirement the grader is mapped against. Add the flip-check line: runner row dropped
as duplicate of S109 (byte-identical test.sh, sha 4770437e...) — no status/recheck/used-by cell
of any existing row changed.
# Acceptance
Table renders in md; quotes verbatim; the flip-check named.
# Bounds
Write only your wave dir.
""")

add("S4SearchLog", "scribe", C, f"""# Target
.ufo/waves/round-55/w1/S4SearchLog/search-log.md — the SOURCES.md Search-log note for this
round's bounded search (the L1 splices it).
# Change
Document the 13th-grader selection as a PRISMA-style bounded search: question (which TB2 task
grader to execute 13th), where (the in-repo round-52 capture set = 89 tasks at pin
2fd12b88, minus the 12 already read, minus the GH013-excluded sanitize-git-repo), screening
(candidates chess-best-move / cancel-async-tasks / dna-insert / count-dataset-tokens /
extract-elf screened by grader size + offline executability + no new capture needed), included
(chess-best-move: 25-line grader, stdlib-only, absolute-/app read executed under bwrap),
excluded (extract-elf 392 lines heavy; cancel-async-tasks 172 lines runtime-dependent;
dna-insert needs oligotm binary; count-dataset-tokens 13 lines but dataset-dependent constant),
stop rationale (one task per round is the established cadence). Counts: identified 89,
excluded 12 already-read + 1 push-protection-blocked + 4 screened-out = 17, included 1.
# Acceptance
One bounded-search note with all counts + reasons.
# Bounds
Write only your wave dir.
""")

add("S5Connections", "scribe", C, f"""# Target
.ufo/waves/round-55/w1/S5Connections/connections-and-limits.md — the entry's connections and
limits sections, drafted against the held corpus (E7 consumes).
# Change
Read corpus/knowledge/tb2-password-recovery-grader.md (r45), tb2-polyglot-c-py-grader.md (r46),
benchmark-verifier-execution-model.md. Draft: (1) connections — one line each naming what the
chess entry extends and never overwrites; (2) limits — what the chess entry does NOT establish
(the full refusal list from PROVINCE's round-37 style: no task image, no harness run, no real
submission, no task validity, no contamination, no model behaviour, 86 graders still unread);
(3) the class-boundary paragraph: r45 line-split membership vs r55 full-multiset equality —
name the exact semantic differences (partial credit, order, duplicates, normalization).
# Acceptance
Three sections, every claim tied to a named held file.
# Bounds
Write only your wave dir.
""")

add("S6ReadmeInventory", "scribe", C, f"""# Target
.ufo/waves/round-55/w1/S6ReadmeInventory/round55-artifacts.md — the corpus/README
`Round-55 supporting artifacts` section draft (the L1 splices).
# Change
Match the style of README's `## Round26 supporting artifacts` section. Inventory this round's
artifacts: plans/round-55-claims.md (freeze, {FREEZE_COMMIT}), plans/round55_c2_controls.py,
.ufo/waves/round-55/claims/* (five before receipts + census-before), and (pending, marked
PENDING-L1) the counter, probe, receipt, entry. One line each with path + what it is.
# Acceptance
Section draft matches house style; pending items explicitly marked.
# Bounds
Write only your wave dir.
""")

# ---------------- scouts (6)
add("SC1UpstreamContext", "scout", C, f"""# Target
.ufo/waves/round-55/w1/SC1UpstreamContext/context.md — upstream context for chess-best-move at
pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6.
# Change
Read-only GETs to raw.githubusercontent.com / api.github.com: (1) the task tree listing
(chess-best-move/ dir contents at the pin); (2) task.toml (difficulty medium, games category,
author, timeouts); (3) whether a solution/ dir exists and what it contains (names only);
(4) neighbors: which other tasks carry a `move.txt`-style token artefact. Write findings with
URLs + fetched bytes where short.
# Acceptance
Tree listing + task.toml summary + solution-dir names + neighbor note.
# Bounds
Read-only + your wave dir. No heavy fetches (<2 MB total).
""")

add("SC2DefectRowTruth", "scout", B, f"""# Target
.ufo/waves/round-55/w1/SC2DefectRowTruth/round35-truth.md — independent truth for the
round35-c1-coverage ledger row (double-run beside E4).
# Change
From a clean shared clone at the current tip: run `python3 plans/round35_c1_verify.py --lane
<clone>`; capture FULL stdout+stderr + exit. Identify the verdict lines (V1..Vn) and the exact
evidence fragment a truthful red declaration should carry NOW. Compare with the ledger's
declared fragment (plans/round54-entrytruth.json row round35-c1-coverage) and name precisely
which output lines changed vs the declared evidence.
# Acceptance
Full output captured; proposed fragment quoted verbatim; delta vs declared named.
# Bounds
No lane writes. Scratch {SCRATCH}/SC2DefectRowTruth/.
""")

add("SC3ArgvUniverse", "scout", B, f"""# Target
.ufo/waves/round-55/w1/SC3ArgvUniverse/universe.md — independent binding-leg scan (cross-check
for E13).
# Change
Implement your OWN scan (different code from E13's, same definition): registry cell first
backtick python3 span -> shlex tokens vs ledger entry_argv, per row of the 78; plus wrapper
tokens (uv/uvx/pipx/poetry/npx/-c) and flag-prefix abbreviation candidates (flag not verbatim
in script body but proper prefix of one that is). Output the full table + counts + the rows a
binding counter would flag TODAY.
# Acceptance
Table + counts; discrepancies vs E13's table (if theirs exists when you finish) named.
# Bounds
No lane writes. Scratch {SCRATCH}/SC3ArgvUniverse/.
""")

add("SC4ProbePrior", "scout", C, f"""# Target
.ufo/waves/round-55/w1/SC4ProbePrior/pattern.md — the established probe pattern, extracted.
# Change
Read plans/password_recovery_probe.py, plans/polyglot_c_py_probe.py, plans/build_pmars_probe.py:
extract (1) the exact bwrap flag pattern each uses (quote the lines), (2) how the frozen case
table + predictions are embedded (data structure), (3) how observed vs predicted and mismatches
are printed, (4) CLI conventions (--lane/--receipt/--selftest), (5) exit-code contract. Write
the pattern note so E5's implementation can be checked against it.
# Acceptance
All five items with file:line quotes.
# Bounds
Read-only + your wave dir.
""")

add("SC5VacuityRead", "scout", C, f"""# Target
.ufo/waves/round-55/w1/SC5VacuityRead/vacuity.md — independent semantic read of the chess
grader (second pair of eyes beside the entry).
# Change
Read corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py (25 lines) and
instruction.md. Enumerate EVERY pass/fail semantic you can derive: split() behavior (any
whitespace run), sorted() multiset equality (order-free, duplicates break), no strip per token
(split handles it), case sensitivity, unicode, the empty file, non-UTF8 bytes. Then the
instruction-vs-grader gaps: the board image the grader never looks at; the example literal
h1h8; the one-per-line guidance vs split() reality; multiple-winning-moves plural rule. End
with `GAPS:` list — anything a 12-case table could still mispredict.
# Acceptance
Semantics enumerated with line refs; GAPS list honest.
# Bounds
Read-only + your wave dir.
""")

add("SC6RegistryHealth", "scout", B, f"""# Target
.ufo/waves/round-55/w1/SC6RegistryHealth/health.md — registry/ledger health census at tip.
# Change
From a clean clone at the current tip: run the r54 counter dry
(`python3 plans/round54_c2_entrytruth.py --lane <clone> --dry`) and the r52 registry counter
(`python3 plans/round52_c2_registry.py --lane <clone>`); capture both. Also count: registry
rows, ledger rows, rows with entry_state red, rows with evidence cell, rows whose registry cell
carries a flag the script body does not contain (spot-check 5 rows by reading the scripts).
# Acceptance
Both counter outputs verbatim + your counts table.
# Bounds
No lane writes. Scratch {SCRATCH}/SC6RegistryHealth/.
""")

# ---------------- reviewers (12)
add("R1C1BeforeRepro", "reviewer", A, f"""# Target
Independent reproduction of the R55-C1 before-state (falsifier of the freeze's before receipt).
# Change
Fresh clean shared clone at {BASE}; run `python3 plans/round52_c2_registry.py --lane <clone>`;
capture output + exit. Compare with the committed .ufo/waves/round-55/claims/c1-before.txt:
MISSING set must be exactly {{plans/round54_c1_anchor.py, plans/round54_c2_entrytruth.py}},
ADVERTISED 79, REGISTERED 77, exit 1. Also verify the counter's advertised-universe scan cannot
miss an advertisement: pick 2 advertised scripts and confirm the files that advertise them are
among the scanned set (SCORECARD/SKILL/LOG/README/knowledge).
# Acceptance
report.md: your output, the diff vs receipt (expect byte-equal modulo the clone path), the
scan-completeness check.
# Bounds
No lane writes. Scratch {SCRATCH}/R1C1BeforeRepro/.
""")

add("R2C2FixturesRepro", "reviewer", B, f"""# Target
Independent rebuild of the two R55-C2 laundering fixtures (do NOT reuse
plans/round55_c2_controls.py — write your own minimal fixture builder) and re-demonstration of
the red-before state.
# Change
Build one-row scratch git fixtures (your own code) matching the frozen cases:
abbreviated-selftest (ledger argv `python3 plans/fixture_gate.py --selft`, argparse-prefix of
--selftest, declared green) and uv-decoy-script (uv wrapper + inline -c program, declared
green); registry cell `python3 plans/fixture_gate.py`; gate entry exits 1. Run the r54 counter
over both (import it unchanged): expect PREDICATE R54-C2 pass + exit 0 on both, and the registry
entry run directly exits 1. Compare with the committed before-receipts.
# Acceptance
Your fixtures reproduce the laundering; any divergence from the receipts named exactly.
# Bounds
No lane writes. Scratch {SCRATCH}/R2C2FixturesRepro/.
""")

add("R3ChessSourcesReopen", "reviewer", C, f"""# Target
Q10/Q13 second-seat re-read of the round's two new sources (S201 grader, S202 instruction).
# Change
Re-open BOTH upstream URLs at pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 (read-only GET).
Verify: (1) the located quotes are verbatim at the named locations (tests/test_outputs.py:25;
instruction.md:1); (2) sha256s match the freeze's pins (a540714e... for the grader,
6ba25be4... for the instruction); (3) the quotes are <=25 words; (4) the `teaches` cells' claims
follow from the quotes. Write the re-read record with agree/disagree per row to
.ufo/waves/round-55/w1/R3ChessSourcesReopen/reopen.md.
# Acceptance
Both rows re-opened with verdicts; any disagreement is a finding, not a fix.
# Bounds
Read-only + your wave dir.
""")

add("R4ClaimsSizing", "reviewer", X, f"""# Target
Adversarial sizing audit of plans/round-55-claims.md (frozen; you audit, never edit).
# Change
Check each claim: (1) after-state re-derivable with ONE command over committed bytes?
(2) universal clauses only over enumerated sets? (3) do-nothing control truly cannot reach the
target (name the cheapest skip-work control you can think of and show it fails the predicate);
(4) kill rules decidable? (5) any target a first-answer baseline would meet? Write findings to
.ufo/waves/round-55/w1/R4ClaimsSizing/findings.md with a severity per finding.
# Acceptance
Per-claim verdicts + concrete attack attempts you actually ran (commands + outputs).
# Bounds
No lane writes. Scratch {SCRATCH}/R4ClaimsSizing/.
""")

add("R5LedgerCorrectionAudit", "reviewer", B, f"""# Target
Audit E4's ledger corrections (bounded-wait for plans/round54-entrytruth.json to change; 60 s
steps, max 25 min; if unchanged, audit the PLAN in the E4 item text instead).
# Change
For row round35-c1-coverage: independently run `python3 plans/round35_c1_verify.py --lane
<clean clone>`; the new evidence fragment must be verbatim from YOUR output too. For each of the
five new rows: re-measure the entry yourself (hermetic env; scratch); the declared exit/state
must match YOUR measurement. Also verify no other row changed (`git -C <clone> diff` on the
ledger at integration is the L1's job — you compare current bytes vs the committed base ledger
at {BASE} via `git -C <clone> show {BASE}:plans/round54-entrytruth.json`).
# Acceptance
Per-row agree/disagree table with your measured exits.
# Bounds
No lane writes. Scratch {SCRATCH}/R5LedgerCorrectionAudit/.
""")

add("R6RegistryCellAudit", "reviewer", A, f"""# Target
Audit the five new SKILL.md registry rows (bounded-wait for them to appear; 60 s steps, max
25 min; if absent, audit the E1 item's cell contract instead and say which cells WILL be false).
# Change
For each new row: run the entry cell's command with --help-less care (use --dry or bare
invocation in a scratch clone; never a full 78-row run) and check the verdict-map cell's claimed
exit semantics; verify the self-test cell's flag exists in the script body (SELFTEST-UNBACKED
pre-check via `python3 plans/round52_c2_registry.py --lane <working tree>` AFTER E1+E2+E5 land —
if you run mid-wave and legs fire on absent sibling files, record that context honestly).
# Acceptance
Per-row cell-truth table; any false cell named with the observed vs claimed behavior.
# Bounds
No lane writes (read SKILL.md, run scripts from a clone). Scratch {SCRATCH}/R6RegistryCellAudit/.
""")

add("R7ProbeOracleAudit", "reviewer", C, f"""# Target
Oracle audit of plans/round55_c3_chess_probe.py (bounded-wait, 60 s steps, max 25 min).
# Change
Read the probe end to end. Verify: (1) the observed verdict derives ONLY from executing the
captured grader's own test function in bwrap — no lane-side reimplementation of the assertion;
(2) /tests is bound read-only and the capture is a byte-copy of the in-repo file (compare sha at
runtime); (3) the 12-case table matches the frozen list byte-for-byte (cases, bytes, predictions);
(4) a mismatch necessarily changes the printed M and the exit code; (5) no case's outcome can
depend on wall-clock/network/env. Write findings to .ufo/waves/round-55/w1/R7ProbeOracleAudit/.
# Acceptance
Five checked properties with evidence; any hole named with the attack input that would exploit it.
# Bounds
No lane writes. Scratch {SCRATCH}/R7ProbeOracleAudit/.
""")

add("R8CounterSoundness", "reviewer", B, f"""# Target
Soundness hunt in plans/round55_c2_entryargv.py (bounded-wait, 60 s steps, max 25 min; until it
lands, derive candidate routes from the frozen leg definitions in plans/round-55-claims.md and
the r54 counter's entry_mode_ok code).
# Change
Hunt FALSE-PASS routes: ledger argv tampering that survives L1 (unicode look-alikes in tokens?
shlex quoting divergences between cell text and JSON list?); wrapper forms L2 misses (python -m?
env? exec -a? direct interpreter path /usr/bin/python3?); abbreviation forms L3 misses (flags
built at runtime? combined short flags? --selftest=true?); L4 ground-truth gaps (evidence
fragment substring-spoofing by the script's own output?). For each candidate: write the exact
fixture (files + argv + ledger row) that would demonstrate it, into
.ufo/waves/round-55/w1/R8CounterSoundness/routes.md. Runnable attempts beat prose: build the top-2
fixtures and run them against the counter if it exists.
# Acceptance
Route list with demonstrable fixtures; each marked survives/fails-with-evidence.
# Bounds
No lane writes. Scratch {SCRATCH}/R8CounterSoundness/.
""")

add("R9HeldGroundCheck", "reviewer", C, f"""# Target
R55-C3 novelty-of-ground check: the 13th grader must not re-state held ground.
# Change
grep the corpus for chess/multiset ground: `grep -rn "chess" corpus/ PROVINCE.md --include="*.md"`;
`grep -rln "sorted(" corpus/knowledge/`; read the 12 tb2-* knowledge entries' class sentences.
Verify: (1) chess-best-move is absent from SOURCES/README/PROVINCE/knowledge before this round
(at {BASE}: `git -C <clone> grep -c chess-best-move {BASE} -- corpus PROVINCE.md` -> 0);
(2) no prior entry already describes full-multiset equality grading (r45 membership vs r55 —
quote the r45 class sentence); (3) the S201/S202 URLs are not near-duplicates of existing rows
(census W04 check at the pin + URL prefix compare).
# Acceptance
report.md: the three checks with commands + outputs + a held/verdict line each.
# Bounds
No lane writes. Scratch {SCRATCH}/R9HeldGroundCheck/.
""")

add("R10ScorecardBasis", "reviewer", X, f"""# Target
Verify the freeze's carried axis numbers against SCORECARD.md at the tip.
# Change
SCORECARD.md + the round-54 measured-close correction say: calibration 9, coverage 7 (L0 cap),
novelty 8, depth 9, operability 8 (harmed 9->8), freshness 9, adjacency 9. Locate each number's
row/line (file:line quotes) and confirm the freeze's §axis-state paragraph quotes them
faithfully. Also confirm the freeze's claim that no stagnation waiver is invoked is consistent
with the declared saturation line 8 / window 4 (SCORECARD `## Saturation`).
# Acceptance
Table: axis | scorecard line | freeze line | match.
# Bounds
Read-only + your wave dir.
""")

add("R11R52Carry", "reviewer", X, f"""# Target
The carried r52 repair, made concrete: the refused E3 patch's order-check regression and masked
K7 control (spot-check obligation 5; production counters stay untouched).
# Change
Read .ufo/waves/round-52/w2/ (R4's patch demonstration) and .ufo/waves/round-54/w1/E3R52RegistryFix.md.
Reconstruct: (1) which grader.py check the patch touched and what regression the order-check
demonstration showed (name the check + the input that flips); (2) the masked K7 control (which
fixture the patch made invisible). Reproduce BOTH on scratch copies (never edit grader.py in
place; copy to scratch, apply the patch idea, run the two demonstrations). Write the recipe +
observed outputs to .ufo/waves/round-55/w1/R11R52Carry/recipe.md so a future round can land the
fix with red-before evidence.
# Acceptance
Both demonstrations reproduced on scratch copies with outputs; the recipe is runnable.
# Bounds
No lane writes. Scratch {SCRATCH}/R11R52Carry/.
""")

add("R12ShonenEvidence", "reviewer", X, f"""# Target
Evidence for the report's SHONEN lines (the 4 promotion boxes are [~] asserted-by-author; you
provide the non-author evidence pointers).
# Change
For each SHONEN.md box: (1) SKILL decision tables/error patterns/checklists with cited sources —
verify 2 sampled citations resolve (run/visit them); (2) an end-to-end domain task executed and
logged — verify LOG.md's latest round entry names a real executed task with receipts;
(3) instructions executable without oral context — pick ONE instruction (e.g. the r55 controls
selftest) and execute it cold from the written bytes only; (4) no cross-domain bleed / PROVINCE
accurate — check PROVINCE.md's Core table entries still resolve (spot 3). Write per-box verdicts
+ pointers to .ufo/waves/round-55/w1/R12ShonenEvidence/boxes.md.
# Acceptance
Four boxes, each with evidence pointers you actually exercised.
# Bounds
No lane writes. Scratch {SCRATCH}/R12ShonenEvidence/.
""")

# ---------------- critics (10)
add("C1PredicateReach", "critic", A, f"""# Target
Falsify R55-C1: can the predicate pass without the repair being real?
# Change
Attack surfaces: (1) de-advertising — if LOG.md simply dropped the round-54 commands, MISSING
would empty without new rows; the spot-check obligation says register OR stop advertising. Is
de-advertising consistent with the frozen after-predicate ("the advertised set at that revision
includes every script this round's landing adds")? Read the freeze and rule; (2) registry-row
cells that are empty strings but whitespace-padded (INCOMPLETE leg's all() check); (3) duplicate
entry scripts across two rows (REGISTERED dict collapses — does a second row for the same script
hide a missing one?); (4) renaming a script so the advertisement regex misses it. For each: try
it on a scratch copy of the tree and report whether the counter still catches it.
# Acceptance
Four attempted bypasses with commands + observed counter output each.
# Bounds
No lane writes (scratch copies only). Scratch {SCRATCH}/C1PredicateReach/.
""")

add("C2BindingBypass", "critic", B, f"""# Target
Falsify R55-C2's binding legs BEFORE the counter lands: find routes the frozen L1-L4 miss.
# Change
From the leg definitions (plans/round-55-claims.md §R55-C2) + the r54 counter's entry_mode_ok:
construct concrete laundering fixtures for: (a) `python -m plans.gate` style entries; (b) argv[0]
as an absolute interpreter path (/usr/bin/python3) — L2 allows {{python3, python}} only; does the
REGISTRY cell convention ever use absolute paths? (check the 78 real registry cells); (c) ledger
argv equal to registry tokens but the SCRIPT swapped by a sibling file (import shadowing via
cwd/plans/__pycache__ — does the counter's hermetic env/clean clone protect?); (d) evidence
fragment substring spoof (a red script that prints another row's evidence string); (e) a registry
cell whose first backtick span is benign but a SECOND span carries the real command (parser takes
first — is that exploitable?). Build runnable fixtures for your top-3 and record observed
behavior under the r54 counter; the L1 replays them against the new counter at integration.
# Acceptance
>=5 routes analyzed, top-3 with runnable fixtures + observed outputs.
# Bounds
No lane writes. Scratch {SCRATCH}/C2BindingBypass/.
""")

add("C3VacuityAttack", "critic", C, f"""# Target
Falsify R55-C3's oracle: cases whose prediction the grader source underdetermines.
# Change
Read the 12 frozen cases (E5 item / spec) against the grader's one assertion. For each case,
derive the verdict YOURSELF from the assertion only (`Path('/app/move.txt').read_text().strip()
.split()` then sorted equality). Flag any case where your derivation differs from the frozen
prediction — that is a pre-run prediction error to surface BEFORE the receipt lands (the
predictions are frozen; an error must be reported, never silently tuned). Pay special attention
to: crlf case (does read_text() translate \\r\\n? open() defaults vs Path.read_text()), the
fullwidth digit case (which bytes exactly), whitespace-padded (strip+split order). Write your
independent 12-row table to .ufo/waves/round-55/w1/C3VacuityAttack/derivation.md.
# Acceptance
Your 12 derivations + delta vs frozen predictions; every delta named as a real prediction risk.
# Bounds
Read-only + your wave dir (do NOT run the grader; derive from source).
""")

add("C4ClassNovelty", "critic", C, f"""# Target
Is full-multiset equality REALLY a graded-artefact class new to this lane (the C3 entry's claim)?
# Change
Read corpus/knowledge/tb2-password-recovery-grader.md (r45: split-newline membership), 
tb2-regex-log-grader.md (r36), tb2-polyglot-c-py-grader.md (r46: dual-runtime literal compare),
tb2-protein-assembly-grader.md (r35: chain comparisons). For each: what does partial credit look
like, is order free, are duplicates possible, is normalization present? Then rule: does r55's
sorted-multiset equality differ on at least one axis every prior class treats differently, or is
it a re-label of r45's membership? Write the ruling with quotes to
.ufo/waves/round-55/w1/C4ClassNovelty/ruling.md. An honest "re-label" verdict caps the entry's
class claim and must be reported, not buried.
# Acceptance
Per-entry axis table + a final ruling.
# Bounds
Read-only + your wave dir.
""")

add("C5KillRuleScope", "critic", B, f"""# Target
Attack the R55-C2 kill rule's wording for holes (frozen text, plans/round-55-claims.md).
# Change
The rule: calibration held at 9 if any attack seat constructs a runnable fixture with ALL static
legs clean that passes the new counter while the registry-declared entry truly exits otherwise;
registry-cell hand-rewrites are excluded as documentation attacks. Probe: (1) does the exclusion
create a laundering lane where the LEDGER is honest but the REGISTRY cell lies (declared green
for a red entry)? Who catches that — name the exact other leg/seat; (2) "all static legs clean"
— enumerate exactly which fields that covers; is a row with bad_decl excluded from names and
therefore unexecuted (r54 evaluate skips bad_decl/argv_defect rows — could a row opt OUT of
execution by carrying a defect)? (3) is the rule decidable by the closure (one command)? Write
the analysis to .ufo/waves/round-55/w1/C5KillRuleScope/analysis.md with a sound/unsound verdict
per probe.
# Acceptance
Three probes analyzed with verdicts; any unsoundness is a report finding, not a rule edit.
# Bounds
Read-only + your wave dir.
""")

add("C6Separability", "critic", X, f"""# Target
Causally-separable audit of the three frozen claims.
# Change
AXES.md: each claim verifiable without the others having landed. Check: (1) R55-C2's after-run
executes the row round52-c2 whose TRUE green depends on R55-C1's rows landing — does that make
C2 non-separable, or is separability about verification (each counter independently runnable)
rather than pass-in-isolation? Read AXES.md's exact wording and rule; (2) C3 shares no instrument
with C1/C2 — verify; (3) the round's admission rule (every claim verifies AND no axis harmed):
which single landing could harm an axis (e.g. new registry rows with false cells harming
calibration)? Write the analysis + the verdict framing the report should use to
.ufo/waves/round-55/w1/C6Separability/analysis.md.
# Acceptance
Ruling on separability with quoted definitions + report-framing recommendation.
# Bounds
Read-only + your wave dir.
""")

add("C7IndexParity", "critic", C, f"""# Target
Coverage no-harm data: index parity both directions at landing time.
# Change
Bounded-wait until corpus/knowledge/tb2-chess-best-move-grader.md exists (60 s steps, max 25
min); then on the working tree: (1) count knowledge files vs README knowledge index rows;
(2) lessons files vs rows; (3) evidence dirs vs rows; (4) confirm the new entry + round55
evidence have rows (E9 owns them — if absent, that is the finding). Also confirm no OLD row went
stale (sample 5 rows -> files exist). Output the four parity numbers + findings to
.ufo/waves/round-55/w1/C7IndexParity/parity.md.
# Acceptance
Four parity counts + per-finding rows.
# Bounds
Read-only + your wave dir.
""")

add("C8TrendEvidence", "critic", X, f"""# Target
The evidence checklist each trend verdict needs at close (LEARNING.md definitions).
# Change
Read LEARNING.md's three-trends table + corpus/lessons/round-54-verifier-spotcheck.md §5 (last
round's verdicts: expansion unchanged, quality harmed, discernment improved). For EACH trend
write what a `improved`/`harmed`/`unchanged` verdict requires THIS round, which artifact would
carry it (receipt paths), and the trap that would make the verdict dishonest (e.g. calling the
registry repair "quality improved" while a new false cell sits uncaught). Save to
.ufo/waves/round-55/w1/C8TrendEvidence/checklist.md.
# Acceptance
Three checklists, each tied to named artifacts.
# Bounds
Read-only + your wave dir.
""")

add("C9AttackShare", "critic", X, f"""# Target
Derive and verify the round's strict attack share before dispatch is claimed as met.
# Change
Read .ufo/waves/round-55/w1-spec.json (when present) or w1-dispatch.json: count roles; strict
attack = reviewer+critic+mutation-tester (sentinels NOT counted — r54 spot-check ruling). Compute
n_attack/total; the floor is >=25% inside the 64-128 band. Also verify the band: total seats in
[64,128], maxLanes field, one wave. Write the formula + numbers to
.ufo/waves/round-55/w1/C9AttackShare/share.md.
# Acceptance
Numbers + floor verdict; any shortfall named loudly.
# Bounds
Read-only + your wave dir.
""")

add("C10AmendmentDiscipline", "critic", X, f"""# Target
Freeze-integrity audit: the frozen rules must not have drifted after {FREEZE_COMMIT}.
# Change
1. `git -C {LANE} show {FREEZE_COMMIT} --stat` — the freeze commit's file list; verify it
contains exactly plans/round-55-claims.md, plans/round55_c2_controls.py,
.ufo/waves/round-55/claims/ (5 files + census). 2. Re-run the three frozen before-commands
(c1 registry counter on a fresh {BASE} clone; both c2 control cases against r54; the three c3
absence checks at {BASE}) and diff against the committed receipts (modulo clone paths). 3. Check
plans/round-55-claims.md working-tree bytes == the committed blob (no unstated edit; the A1
amendment line is IN the committed bytes — verify).
# Acceptance
Three sections with outputs; any drift named exactly.
# Bounds
No lane writes. Scratch {SCRATCH}/C10AmendmentDiscipline/.
""")

# ---------------- mutation-testers (6)
add("M1RegistryMutants", "mutation-tester", A, f"""# Target
Mutation-test plans/round52_c2_registry.py (production counter — copy to scratch, never edit in
place).
# Change
Build a minimal fixture lane (plans/tool.py + SKILL registry + SCORECARD advertisement) in
scratch. Single-defect mutants, one per leg: (1) MISSING leg returns [] always; (2) INCOMPLETE
leg ignores empty cells; (3) ENTRY-MISSING leg skipped; (4) SELFTEST-UNBACKED returns False
always; (5) DUPLICATE check removed; (6) the advertised-universe regex narrowed (misses
knowledge/*.md). Each mutant must flip the observable result (exit code or a DEFECT line) on a
fixture that exercises that leg; record killed/survived per mutant to
.ufo/waves/round-55/w1/M1RegistryMutants/mutants.md. A surviving mutant = an
advertised-but-undemonstrated leg (finding, not a fix).
# Acceptance
Six mutants with kill evidence each.
# Bounds
Scratch copies only. Scratch {SCRATCH}/M1RegistryMutants/.
""")

add("M2EntryArgvMutants", "mutation-tester", B, f"""# Target
Mutation-test plans/round55_c2_entryargv.py's NEW legs (bounded-wait, 60 s steps, max 25 min;
scratch copy only).
# Change
Using the controls fixtures (import plans/round55_c2_controls.py's CASES or rebuild them):
single-leg silence mutants: (1) L1 comparison removed; (2) L2 wrapper check removed; (3) L3
abbreviation check removed; (4) L4 registry-cell ground truth replaced by ledger-argv execution
(the r54 behavior). Each mutant must flip the fixture outcome (killed fixture passes again = the
leg was load-bearing). Record per-mutant kill evidence to
.ufo/waves/round-55/w1/M2EntryArgvMutants/mutants.md; a surviving leg is dead weight (finding).
# Acceptance
Four mutants with kill evidence; the L4 mutant must re-introduce the laundering (proving L4 is
the load-bearing leg).
# Bounds
Scratch copies only. Scratch {SCRATCH}/M2EntryArgvMutants/.
""")

add("M3ChessProbeMutants", "mutation-tester", C, f"""# Target
Mutation-test plans/round55_c3_chess_probe.py (bounded-wait; scratch copy only).
# Change
Mutants on a copy: (1) invert verdict mapping (pass<->fail) — the receipt must flip to
mismatches>0 / PREDICATE fail; (2) mismatch counter skipped — summary must still change
(observed_pass/observed_fail swap) or the case lines must expose it (if NOTHING observable
changes, the mismatch leg is decorative — finding); (3) null mutant (reorder case execution) —
output must be equivalent (order-insensitive summary). Record to
.ufo/waves/round-55/w1/M3ChessProbeMutants/mutants.md with observed diffs.
# Acceptance
Three mutants with observed output diffs.
# Bounds
Scratch copies only. Scratch {SCRATCH}/M3ChessProbeMutants/.
""")

add("M4ControlsMutants", "mutation-tester", B, f"""# Target
Mutation-test plans/round55_c2_controls.py's fixture realism (scratch copy only).
# Change
Mutant A: gate argparse allow_abbrev=False -> the abbreviated-selftest case must FAIL to
demonstrate laundering against r54 (route dead) — proving the fixture really depends on argparse
abbreviation. Mutant B: gate entry exit flipped to 0 -> the true-entry check must flip the ROUTE
line to NOT demonstrated. Mutant C: ledger entry_exit flipped to 1/red -> the r54 counter must
flag a MISMATCH (not pass). Record observed outputs to
.ufo/waves/round-55/w1/M4ControlsMutants/mutants.md.
# Acceptance
Three mutants with observed flips.
# Bounds
Scratch copies only. Scratch {SCRATCH}/M4ControlsMutants/.
""")

add("M5LedgerDeclMutants", "mutation-tester", B, f"""# Target
Do ledger declarations bind? Mutate a COPY of plans/round54-entrytruth.json in scratch.
# Change
Mutant 1: flip one green row's entry_exit to 1 (keep state green) -> r54 counter must report
bad_decl (green!=exit0). Mutant 2: flip a green row's state to red with a bogus evidence ->
MISMATCH/LAUNDERED on execution. Mutant 3: delete a row -> missing=N + EXTRA? (observe which
direction fires). Mutant 4: duplicate a row's name in the JSON (object_pairs_hook no_dup) ->
ledger unreadable. Record observed outputs to .ufo/waves/round-55/w1/M5LedgerDeclMutants/mutants.md.
# Acceptance
Four mutants with observed counter behavior.
# Bounds
Scratch copies only. Scratch {SCRATCH}/M5LedgerDeclMutants/.
""")

add("M6SourcesRowMutants", "mutation-tester", C, f"""# Target
Do the census/gate catch defective SOURCES rows? Mutants on a scratch copy of corpus/SOURCES.md.
# Change
Build a scratch copy; apply one defect at a time to the DRAFT S201/S202 rows (or, if not yet
appended, to a copy of an existing row renamed S901): (1) drop one pipe (10 columns); (2) sha256
token moved out of the anchor cell; (3) tier 'D'; (4) status 'mined!' (enum break); (5) duplicate
id. Run the frozen census commands (CORPUS.md §Census + scripts/sources-census.sh validate
--file <scratch copy>) per mutant; record caught/missed to
.ufo/waves/round-55/w1/M6SourcesRowMutants/mutants.md — a missed defect is a reviewer-eyes item
(feeds the lesson).
# Acceptance
Five mutants with caught/missed per command.
# Bounds
Scratch copies only. Scratch {SCRATCH}/M6SourcesRowMutants/.
""")

# ---------------- sentinels (4)
add("SN1SecretScreen", "sentinel", X, f"""# Target
Push-protection / credential screen over every byte this round may commit.
# Change
Scan the lane working tree diff vs {BASE} (`git -C {LANE} diff --name-only {BASE}` + untracked
files under plans/, corpus/, .ufo/waves/round-55/) for credential-shaped strings:
ghp_[A-Za-z0-9]{{30,}}, github_pat_[A-Za-z0-9_]{20,}, hf_[A-Za-z0-9]{30,}, AKIA[0-9A-Z]{16},
xox[baprs]-, sk-[A-Za-z0-9]{20,}, -----BEGIN .* PRIVATE KEY-----, ops_ (1Password service),
connection strings (postgres://.*:.*@). The chess captures carry the TB2 canary GUID string —
that is a canary, not a secret: verify it matches the string already pushed at {BASE}
(git show {BASE}:corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py | sha256sum)
so no NEW canary byte lands. Report every hit with file:line; expected: zero real hits.
Write to .ufo/waves/round-55/w1/SN1SecretScreen/screen.md.
# Acceptance
Pattern list + scan counts + per-hit verdicts (real/canary/false-positive).
# Bounds
Read-only + your wave dir.
""")

add("SN2NetworkSafety", "sentinel", X, f"""# Target
Network-use receipt for the round: every fetch read-only and in-scope.
# Change
Read the round's fetching code/paths: plans/round55_c3_chess_probe.py (must be offline-only —
verify no urllib/requests/socket usage), the E14/SC1/SC3/R3 items' planned GETs (raw.
githubusercontent.com, api.github.com). grep the working tree's new files for network calls
(`grep -rn "requests\\|urllib\\|http://\\|https://" plans/round55_* corpus/knowledge/tb2-chess*`
when present). Verify no fetch can POST, authenticate, or reach a model-serving endpoint. Write
to .ufo/waves/round-55/w1/SN2NetworkSafety/network.md.
# Acceptance
Per-file verdict: offline-only / read-only-GET-in-scope; any violation named.
# Bounds
Read-only + your wave dir.
""")

add("SN3CorpusHygiene", "sentinel", X, f"""# Target
Corpus hygiene over the round's new corpus bytes.
# Change
When corpus/knowledge/tb2-chess-best-move-grader.md + the SOURCES rows exist (bounded-wait 25
min max): verify no credential material (CORPUS rule), no op:// refs, no session URLs, no
canary GUID quoted OUTSIDE its evidentiary context, quotes carry locations, the entry's claims
stay inside its quotes (Q3 spot-read 3 load-bearing sentences vs the sources).
# Acceptance
Checklist with per-item pass/fail + evidence.
# Bounds
Read-only + your wave dir.
""")

add("SN4FreezeIntegrity", "sentinel", X, f"""# Target
Freeze commit integrity + working-tree drift audit.
# Change
1. `git -C {LANE} show --stat {FREEZE_COMMIT}` — file list exactly: plans/round-55-claims.md,
plans/round55_c2_controls.py, .ufo/waves/round-55/claims/{{c1-before.txt,
c2-before-abbreviated-selftest.txt, c2-before-uv-decoy-script.txt, c3-before.txt,
census-before.txt}}. 2. Verify the working tree's plans/round-55-claims.md blob == committed
blob (`git -C {LANE} diff {FREEZE_COMMIT} -- plans/round-55-claims.md` empty). 3. List every
lane file modified since {FREEZE_COMMIT} (`git -C {LANE} diff --name-only {FREEZE_COMMIT}` +
status --porcelain) and check each against the wave's declared write scopes (a seat writing
outside its scope = finding). Write to .ufo/waves/round-55/w1/SN4FreezeIntegrity/integrity.md.
# Acceptance
Three sections; any out-of-scope write named with file + seat.
# Bounds
Read-only + your wave dir.
""")

# ---------------- revengers (3)
add("RV1EntryModeOk", "revenger", B, f"""# Target
Reverse-engineer why round-54's counter computed `entry_mode_ok` but never wired it into the
predicate (the hole R55-C2 closes).
# Change
Read plans/round54_c2_entrytruth.py history (`git -C {LANE} log --oneline -- <file>`,
`git show <rev>:<file>` for its birth revision), the r54 wave artifacts
(.ufo/waves/round-54/w1/R2C2Counter/review.md, E2LedgerRefine.md), and plans/round-54-claims.md.
Rule: was the leg deliberately deferred (a documented open window), an oversight, or a
predicate-scope decision (static legs vs execution legs)? Reconstruct the original intent with
evidence quotes. Write to .ufo/waves/round-55/w1/RV1EntryModeOk/findings.md.
# Acceptance
A dated reconstruction with evidence pointers; the intent question answered.
# Bounds
Read-only + your wave dir.
""")

add("RV2Round35Fragment", "revenger", B, f"""# Target
Why did round35-c1-coverage's declared evidence fragment stop matching the entry's output?
# Change
`git -C {LANE} log --oneline -- plans/round35_c1_verify.py` — find revisions touching the V4
output wording after the ledger was built; diff the wording (`git show <rev>:plans/
round35_c1_verify.py | grep -n "V4"`); name the exact change that broke the fragment and the
round that landed it. Also state whether the row's TRUE verdict (exit/state) changed or only the
wording. Write to .ufo/waves/round-55/w1/RV2Round35Fragment/root-cause.md.
# Acceptance
Root cause with revision hashes + the diff hunk; verdict wording-only vs truth-change.
# Bounds
Read-only + your wave dir.
""")

add("RV3R52PatchAnatomy", "revenger", X, f"""# Target
Anatomy of the refused r52 E3 patch (why order-check regressed and K7 got masked).
# Change
Read .ufo/waves/round-52/w2/*R4*/ (the patch review), .ufo/waves/round-54/w1/E3R52RegistryFix.md
and E8NoharmR53C2.md, and grader.py's r11 order check (grep -n "check_r11_ordering" grader.py).
Produce: the patch's claimed fix, the order-check regression mechanism, the K7 masking mechanism,
and what a correct fix must do differently. Write to
.ufo/waves/round-55/w1/RV3R52PatchAnatomy/anatomy.md.
# Acceptance
Mechanisms with code line refs; the correct-fix sketch.
# Bounds
Read-only + your wave dir.
""")

# ---------------- connectors (3)
add("CN1SiblingArgv", "connector", X, f"""# Target
Sibling overlap: does any sibling lane already own entry-argv binding / ledger-truth /
registry-closure instruments?
# Change
Scan sibling repos' tools dirs (read-only): ../kumitate-shokunin (gate registries), 
../tameshi-shokunin (mutation fences), ../chousa-shokunin (capture/citation), ../kama-shokunin
(endpoint identity pins). For each candidate: name + what it binds + one-line ruling
duplicate/adjacent/different-data. Also verify the r14 ruling (no sibling owns an
evidence-replay gate) still holds at current sibling HEADs for the NEW instruments (argv
binding, multiset grader probe). Write to .ufo/waves/round-55/w1/CN1SiblingArgv/overlap.md.
# Acceptance
Per-sibling ruling table + the standing-ruling re-check.
# Bounds
Read-only + your wave dir.
""")

add("CN2CrossSource", "connector", X, f"""# Target
Cross-source pattern: the 13 TB2 grader entries as one dataset.
# Change
Read the 12 held tb2-* knowledge entries (+ the new chess one when it lands). Build the class
table: task | graded artefact | grader operation (membership / literal / ldd-scan / chain-compare
/ multiset) | partial credit | receipt cases. Where does chess-best-move sit; which sibling
should receive the fleet-level pattern (tameshi: fixture craft? kotoba: instruction-vs-grader gap
craft?). Write to .ufo/waves/round-55/w1/CN2CrossSource/class-table.md.
# Acceptance
13-row table + the routing recommendation.
# Bounds
Read-only + your wave dir.
""")

add("CN3ReportOuts", "connector", X, f"""# Target
.ufo/waves/round-55/w1/CN3ReportOuts/routing.md — what this round routes OUT (evidence sent,
never absorbed).
# Change
Collect: (1) the standing L0 caps (round-25/33/51 coverage; round-52 GH013; round-54 assimilation
drift) — verify each is still unanswered in /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md;
(2) serving-plane status (do NOT probe endpoints; just note the standing refusal); (3) any
finding from the wave that belongs to another lane (name it + the owning lane). One routing line
per item, report-ready.
# Acceptance
Routing lines ready to paste; unanswered-L0 verification quoted.
# Bounds
Read-only + your wave dir.
""")

# ---------------- simplifiers (2)
add("SP1CounterScope", "simplifier", X, f"""# Target
YAGNI pass over plans/round55_c2_entryargv.py (bounded-wait; propose, never edit).
# Change
When the counter lands: is any leg redundant GIVEN the others (e.g. is L3 dead once L1 enforces
token equality — answer: L3 guards the registry cell itself, but check whether L2+L1 already
imply it)? Is any borrowed r54 machinery unused (dead imports/branches)? Propose minimal diffs
(no behavior change) to .ufo/waves/round-55/w1/SP1CounterScope/proposals.md; each proposal names
the leg it removes and why behavior is preserved (or why the leg must stay).
# Acceptance
Per-leg keep/remove ruling with reasoning.
# Bounds
Read-only + your wave dir.
""")

add("SP2RowCells", "simplifier", A, f"""# Target
Cell-verbosity pass over the five new SKILL.md registry rows (bounded-wait; propose diffs only).
# Change
When E1's rows land: compare their cell prose with the established house style (rows round52-c1/
round52-c2). Propose trims where a cell says what the entry cell already says; NEVER propose
dropping a truth-bearing cell (verdict map, self-test). Output unified diffs to
.ufo/waves/round-55/w1/SP2RowCells/trims.diff (the L1 applies or rejects).
# Acceptance
Diff output + per-hunk rationale.
# Bounds
Read-only + your wave dir.
""")

# ---------------- sonic (2)
add("SO1CensusSeries", "scribe", C, f"""# Target
.ufo/waves/round-55/w1/SO1CensusSeries/census-series.txt — the frozen census numbers before vs
working-tree-now.
# Change
Run the CORPUS.md §Census commands on (a) a clean clone at {BASE} and (b) the working tree:
rows count, malformed count, tier histogram, status histogram, duplicate-id check, enum
violations, mined-used-by existence. Paste both blocks with the command lines. (Do NOT run the
census --validate CLI here; the raw commands only, so the series is comparable.)
# Acceptance
Both blocks complete; deltas summarized in three lines.
# Bounds
Read-only + your wave dir. Scratch {SCRATCH}/SO1CensusSeries/.
""")

add("SO2ClassTable", "scout", C, f"""# Target
.ufo/waves/round-55/w1/SO2ClassTable/table.tsv — the 12 held TB2 entries' receipt numbers,
collected mechanically.
# Change
For each corpus/knowledge/tb2-*.md: extract task, probe path, receipt path, and the receipt's
`cases=N observed_pass=P observed_fail=F mismatches=M` line (grep the receipts under
corpus/evidence/round3*/round4*/). One TSV row each; missing receipt -> `RECEIPT-MISSING` (do not
guess). End with the totals line.
# Acceptance
12 rows + totals; only observed numbers.
# Bounds
Read-only + your wave dir.
""")

spec = {
    "wave": WAVE,
    "milestone": "kengaku round 55 wave 1 (v2, build+attack): registry closure (R55-C1, operability 8->9), entry-argv structural binding (R55-C2, calibration 9->10), 13th TB2 grader executed (R55-C3, coverage, L0-capped)",
    "reportDir": ".ufo/waves/round-55/w1",
    "maxLanes": 70,
    "axes": ["operability", "calibration", "coverage"],
    "context": CONTEXT,
    "items": items,
}
import os
os.makedirs(".ufo/waves/round-55", exist_ok=True)
with open(".ufo/waves/round-55/w1-spec.json", "w") as f:
    json.dump(spec, f, indent=1, ensure_ascii=False)
roles = {}
for it in items:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
attack = roles.get("reviewer", 0) + roles.get("critic", 0) + roles.get("mutation-tester", 0)
print(json.dumps(roles, indent=0))
print(f"items={len(items)} strict_attack={attack} share={attack/len(items):.3f}")
names = [i["name"] for i in items]
print("duplicates:", {n for n in names if names.count(n) > 1} or "none")
