# R42MutC2Counter — mutation test of the round-42 C2 counter

Seat: R42MutC2Counter (kengaku round 42, wave 1, hyaku run 9, 2026-10-26).
Target: `plans/round42_c2_verify.py` (sha256 `270097fdf1d25ee8…`, byte-identical at the freeze commit
`bc856d803576e182b6c3c12afc6b23f392071c25` and at the lane tip). Detectors: the two committed controls,
reproduced in a scratch clone — `control-c2-nothing.txt` (counter CLI on the freeze state) and
`c2_filler_control.py` (imports the counter's `v9` on filler/content mirrors). All runs inside the Q32
bwrap envelope. Nothing in the lane was written except this seat's report dir.

## Method

- Clone: `git clone -q --shared <lane> $S/lane`, checked out at the freeze commit; verified
  `rev-parse --show-toplevel` = the clone; verified `git diff bc856d8 HEAD -- plans/round42_c2_verify.py`
  empty and the clone's counter digest equals the lane's (`270097fd…`).
- Baselines (pristine counter, under bwrap): control A on the freeze state → `checks=9 defects=6`,
  `PREDICATE C2 fail`, exit 1 — matches the committed control except the expected P9 delta (the committed
  transcript ran pre-commit with `untracked=31`; a fresh clone has the controls tracked, `untracked=0`).
  Control B → `CONTROL filler V9 DEFECT …`, `CONTROL content V9 ok …`, `CONTROL-C2-FILLER red-as-required`,
  exit 0 — matches `control-c2-filler.txt`.
- Mutants: 237 single-line mutants over the counter's behavior lines (module pins/paths/regexes L57–84,
  `sha256`/`spec`/`dry` L87–112, `v1`–`v9` and helpers L115–313, predicate plumbing L316–338). Operators:
  comparison/boolean flips, `not`-drops, int/string constant changes, digest-pin first-char flips, regex
  quantifier/class/alternation tweaks, `bad.append` drops, `continue`→`pass`, return flips, CLI-argument
  string mutations, path-constant mutations, set-operation swaps. Every mutant compiles; each is one line.
- Catch criteria. Verdict-level (primary): the per-check ok/DEFECT flags, the `checks=9 defects=N` count,
  the `PREDICATE C2` line, the exit code (control A), or control B's `CONTROL filler/content V9` flags +
  `CONTROL-C2-FILLER` verdict + exit differ from the pristine baseline. Transcript-level (secondary): any
  stdout/stderr difference — the committed control is a transcript, so it pins this level too.
- Discipline: mutate → run A → run B → restore exact pristine bytes, per mutant; final digests verified
  (`270097fd…` in both the clone and the receipt-committed mirror). First sweep discarded: its control-B
  column contradicted direct re-runs (the filler control's `importlib` import writes `plans/__pycache__`
  into the mirror; without bytecode hygiene some B runs did not see the mutated source). Rerun with
  `PYTHONDONTWRITEBYTECODE=1`; spot re-runs (SPEC-pin, Dockerfile-pin) agree with the rerun.

## Results

`python3` sweep over 237 mutants × both controls (commands and outputs in `mutant_table.tsv`,
`baseline-A.txt`, `baseline-B.txt` in this dir):

| disposition | count |
|---|---|
| caught by the committed controls (verdict level) | 69 (46 by A only, 21 by B only, 2 by both) |
| caught only at transcript level (note-only changes; pinned by the committed transcript) | 32 |
| verdict-survivors → killed by the drafted controls (run-verified) | 159 |
| survivors, argued equivalent (no input distinguishes them) | 6 |
| survivors, named limits (control drafted/specified, not runnable at wave 1) | 3 |
| **total** | **237** |

Caught by the committed controls, highlights: all 9 `CAPTURES` digest pins and the probe/dry pins (V1/V5
flip green→red), the spec pin (control B crashes on the mutated `spec()`), all nine capture-name/path
mutations, `v1`'s digest-equality core, `v5`'s byte-equality, `v9`'s case-row regex and TASK constant
(control B's content mirror goes `BROKEN`), the predicate flip and exit flip (A: `pass`/exit 0 printed on
a 6-defect state).

## Drafted controls (one per survivor class) — `draft_c2_controls.py` in this dir

Same pattern as the freeze filler control: import the counter from `<lane>/plans/round42_c2_verify.py`,
build scratch mirrors, call the counter's own v-functions, require a specific verdict per mirror. Green on
the pristine counter for all nine groups (`draft-pristine-run.txt`, `draft7-pristine-run.txt`:
`DRAFT-CONTROLS groups=8 failed=0` / `groups=1 failed=0`); each listed mutant was applied to the mirror's
counter and the draft flipped (exit ≠ 0). Kill counts: D1 6, D2 13, D3 11, D4 42, D5 4, D6 57, D7 7,
D8 18, D9 1 = 159.

- **D1 v1 manifest** (6): good/`manifest absent`/`unparsed manifest line`/extra-line/tampered-bytes
  mirrors with exact notes — kills M120034, M125039, M127042, M129043, M129044, M129046 (early-return
  flips, `or`→`and` digest gate, extra-check drop, note f-strings).
- **D2 v2 gate invocation** (13): freeze mirror asserting the note prefix `spec=frozen gate=frozen` plus
  the printed `gate: P9`/`gate: P10 DEFECT receipt unreadable` lines and a whole-stdout shape check;
  tampered-spec mirror asserting `ValueError: spec template not at its freeze digest` exactly; tampered-gate
  mirror asserting the early return; receipt-present mirror with the gate stubbed asserting the effective
  spec's `receipt_sha256` equals the committed receipt digest; CLI run with a missing `--work` parent
  asserting no traceback; CLI shape check (kills `capture_output=False` leaks). Kills M072010 (GATE pin),
  B071214 (GATE_REL path), M096021, M134047, M135048, M135049, M136050, M139052, M140053, M140054
  (`--rerun` drop), M140055 (`--require-clean-tree` drop), M219113, M323197.
- **D3 v3 anchor rows** (11): good SOURCES mirror (3 valid 11-cell rows, anchors = spec pins) expecting
  `rows=3 bad=0` exactly, plus anchor-tampered/short-row/dup-row/0-space/4-space mirrors — kills M081014,
  M151058, M160059, M160060, M160061, M162063, M163064, M164066, M165067, M166068, M166070.
- **D4 v4 receipt** (42): good mirror (the committed receipt + minimal entry) expecting
  `cases=16 mismatches_named=0/0 bad=0` exactly; summary variants (pass=8, pass=9/fail=7, fail=9/pass=7,
  empty `cases=`, synthetic 14/2); match=NO unnamed/named; reordered ids; second summary line; tampered
  dry table asserting `ValueError: dry table not at its freeze digest` exactly; entry-absent exact note —
  kills the whole v4 block M101022–M205101 plus B082220, B082221, B172226, B172227, B186228, B189229
  (summary agreement, mismatch naming, id/regex parsing).
- **D5 v5 frozen probe** (4): good on the lane; tampered-probe mirror (comment appended to the probe)
  expecting the early return — kills M209103 (the `or`→`and` pin gate: the tampered probe still prints the
  frozen `--dry` table, so the mutant would admit it), M210104, M210105, M210106.
- **D6 v7 requirement map** (57): good mirror (the committed receipt + a correct 7-tag map derived from
  it) expecting `rows=7 tags=7 bad=0` exactly; wrong-label/wrong-line/missing-tag/dup-tag/
  cite-nonviolating/no-section/unparsed-row(empty backticked tag)/prose-line/unknown-tag/
  no-violating-case/empty-cases-cell/empty-backtick-cite/entry-absent mirrors — kills all derive() flips
  (M224116–M228122), the MAP_ROW regex mutants, and the whole v7 loop M238123–M271161 plus M267207/208,
  B083222, B083223.
- **D7 v8 order check** (7): run on a receipt-committed mirror (lane tip `fda71ae…`; verified
  `ORDER RESULT PASS`, exit 0, and that no claims/ blob trips the scan) expecting
  `order_exit=0 result=PASS` exactly plus a quiet-stdout check — kills M277162, M278163, M278165, M278166,
  B077217 (ORDER_REL path), B078218 (CLAIMS_REL path), B278232.
- **D8 v9 surfaces** (18): good full mirror expecting `case_rows=16/16 bad=0` exactly; province-only-task,
  frontier-wrong, ids-only-in-source-lines, empty-receipt+empty-table, verdict-flipped-row, no-case-table,
  empty-id-row, entry-absent exact note — kills M084019, M290167, M300174, M300175, M301177, M302179,
  M302180, M303181, M303182, M306184, M308185, M309187, M309188, M311189, M312192, M312193, M313194,
  M313196 (the V9 surface checks control B does not reach).
- **D9 main exception path** (1): bad-UTF-8 entry mirror, `main()` in process with `v2` stubbed — V7 and V9
  must stay `DEFECT` with `UnicodeDecodeError` — kills M333199 (`except`→`ok=True` would admit a crashing
  check).

## Survivors (9) — argued equivalents and limits

Equivalent (no input distinguishes mutant from pristine; no control can exist):

- M081015 `SOURCE_ROW` `S\d{3,}`→`S\d{2,}`: v3 looks up only the spec's row ids (S125–S127, three digits);
  a looser id regex only admits registry rows no counter check ever queries.
- M136051 `or "absent"`→`or "absnt"`: the fallback fires only when `sha256` returns None (receipt
  unreadable); the gate's `c_receipt` early-returns `receipt unreadable` on got-is-None before ever
  comparing `receipt_sha256` (pkg_gate.py c_receipt), so the string never reaches a comparison.
- M163065 v3 `([0-9a-fA-F]+)`→`(*)`: the pattern requires the literal `sha256\s+` prefix; an empty hex run
  yields `toks=[""]` vs pristine `[]` — both `!= [pin]`, same bad entry, same note.
- M213110 v5 `and`→`or` on `same = rc==0 and stdout==dry`: line 213 is reachable only when both pins
  verify (L209 early-returns otherwise); the frozen probe's `--dry` output is byte-equal to the frozen dry
  table by construction, so `same` is always True there.
- M264148 v7 cited `` `([a-z0-9-]+)` ``→`(*)`: an empty backticked cite yields `[""]` vs `[]`; both trip
  the identical `cites no case or a case that does not violate it` append.
- M278164 v8 `and`→`or`: order_check prints `ORDER RESULT PASS` iff it exits 0 (order_check.py main:
  exit 0 only after printing RESULT PASS; 1→FAIL, 2→ERROR), so the string test is redundant with `rc==0`.

Limits (real behavior deltas the wave-1 controls cannot reach):

- M218112 census subcommand `"validate"`→`"validat"`: the census script's argv loop treats an unknown
  positional as a lane name and leaves MODE at its default `census`
  (scripts/sources-census.sh:67-68 `census|validate|overdue|shared|selftest) MODE=$1`), and
  `census --file <SOURCES>` also exits 0 here (measured: `validate` exit 0, `validat` exit 0, both
  printing the same W04-warning summary shape). v6's token is not load-bearing on this host; a
  counter-level control cannot distinguish the two. The fix belongs in the census script (fleet-level,
  outside this lane and this seat's write scope).
- M337202 predicate `defects == 0`→`== 1` and M338204 exit flip `return 1 if defects == 0 else 1`:
  distinguishable only on a state with `defects=0` — the landing tip, which does not exist yet in wave 1.
  Drafted control (specified, unrun): on a clean clone of the landing tip, assert `PREDICATE C2 pass` and
  exit 0; both mutants print `fail`/exit 1 there. Cost note: the landing control's V2 runs the gate with
  `--rerun`, whose P10 re-runs the probe — measured 65 s per fresh run on this host (16 cases, byte-equal
  to the committed receipt, `regrade cases=16 differ=0`).

## Q32 envelope receipt

Every counter/control/fixture run in this seat executed inside:
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`
Baseline window (`baseline-envelope.txt`): start 17:25:44, end 17:25:51;
`ls -A /home/vgpnk/.local/bin | sha256sum` before `436b361f9d1edc4e…`, after `436b361f9d1edc4e…` —
unchanged. The sweep and all draft runs used the same envelope with a fixed system PATH
(`PATH=/usr/local/sbin:/usr/local/bin:/usr/bin`), `TMPDIR` inside the seat scratch, and
`PYTHONDONTWRITEBYTECODE=1`. No pacman transaction was run; no tool was installed or upgraded.

## Integrity

- Lane `plans/round42_c2_verify.py` sha256 before and after: `270097fdf1d25ee8…` (unchanged; the lane was
  never written except this seat's report dir).
- Scratch clone and the receipt-committed mirror both restored to `270097fd…` after every mutant and at
  the end (verified by digest after the sweep and after the kill loop).
- Lane dirt after the work: only `?? .ufo/waves/round-42/build/…` (all seats' reports) and the
  orchestrator's `build.ready` markers — no tracked file touched, no git/jj mutation anywhere.
- Scratch: `/fast/scratch/hyaku/kengaku-r42/R42MutC2Counter` (clone, headmirror, mutants/results/kills
  JSON, run outputs); removed after this report, target checked to start with the seat's own prefix.

## Files in this report dir

- `draft_c2_controls.py` — the nine drafted controls (green on pristine; kills per group above).
- `mutant_table.tsv` — all 237 mutants: id, line, class, caught_by, disposition.
- `baseline-A.txt`, `baseline-B.txt`, `baseline-envelope.txt` — pristine control runs + Q32 window.
- `draft-pristine-run.txt`, `draft7-pristine-run.txt` — the drafts' green runs on the pristine counter.

VERDICT: c2-counter-mutants-caught-228/237
