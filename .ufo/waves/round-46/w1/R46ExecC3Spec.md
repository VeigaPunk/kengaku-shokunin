# R46ExecC3Spec — `plans/pkg-spec-r46.json` draft (round 46, wave 1, C3)

Seat: executor, C3 coverage (pinned TB2 `polyglot-c-py`). Lane: `kengaku-shokunin` @ `fd4129e` (base `64ba838`).
No lane file was edited: the spec and its notes are drafted under this seat's report subdir for the L1 to land as
`plans/pkg-spec-r46.json`. Nothing was committed, no graded case was executed, `pkg_gate.py --rerun` was never run
on the real package (QUALITY Q30).

## Deliverables

| path (lane-relative) | what |
|---|---|
| `.ufo/waves/round-46/w1/R46ExecC3Spec/pkg-spec-r46.json` | the draft spec, sha256 `171feaff3addcdc1445e4188ff038167305610db57196cebcebf6fe73ecb84fd`, 2180 bytes |
| `.ufo/waves/round-46/w1/R46ExecC3Spec/pkg-spec-r46.notes.md` | a note on every field, the capture recipe, the SOURCES cell contract, the entry-side contract |
| `.ufo/waves/round-46/w1/R46ExecC3Spec/gate-on-lane.txt` | draft spec run against the real lane (envelope) |
| `.ufo/waves/round-46/w1/R46ExecC3Spec/gate-sim-ok.txt`, `gate-sim.txt` | scratch synthetic package, P1–P8+P10 `defects=0` |
| `.ufo/waves/round-46/w1/R46ExecC3Spec/gate-ctl-*.txt` | five negative controls, one pin moved each |
| `.ufo/waves/round-46/w1/R46ExecC3Spec/anchors.json` | the 7 validated anchor cells, copy-ready |
| `.ufo/waves/round-46/w1/R46ExecC3Spec/anchorline.txt`, `anchorline-selftest.txt` | frozen anchor gate on those cells (`live=0`) and its selftest (`pass`) |
| `.ufo/waves/round-46/w1/R46ExecC3Spec/bio-branch.txt`, `branch-uv.txt`, `branch-stub.txt`, `uv-branch.txt` | the P10 interpreter branch, measured both ways |
| `.ufo/waves/round-46/w1/R46ExecC3Spec/anchor-cells-two-drafts.txt` | both row drafts measured under V12 (7 rows each, 0 defects) |

Landing instruction for the L1: copy `plans/polyglot_c_py_probe.py` byte-verbatim from
`.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py` (the probe pin is already the digest of those bytes),
copy the draft to `plans/pkg-spec-r46.json` unchanged, then fill the single remaining `PENDING-STAGE-2` value
(`receipt_sha256`) at the stage-2 amendment commit (exact command in the notes file).

## Spec shape

13 top-level keys — the round-45 schema verbatim (`plans/pkg-spec-r45.json`), no key added or dropped, so
`pkg_gate.py` and the round-45 C2 counter's V1–V11 (which C3 re-points) read the names they already read:

`name`, `entry` (`corpus/knowledge/tb2-polyglot-c-py-grader.md`), `capture_dir`
(`corpus/evidence/round46/tb2-polyglot-c-py`), `receipt` (`corpus/evidence/round46/polyglot-c-py-probe.txt`),
`receipt_sha256` (**`PENDING-STAGE-2`**), `probe_cmd` (`["plans/polyglot_c_py_probe.py","--lane","."]`), `sources`,
`readme`, `knowledge_glob`, `raw_base` (pin `2fd12b88…`, task dir `polyglot-c-py/`), `rows` (S166–S172),
`frozen_instruments` (`plans/pkg_gate.py` = `ea638822…`, live; `plans/polyglot_c_py_probe.py` =
`22b7779e…`, the probe seat's re-fixed artifact re-hashed here), `entry_rules` (`verified_at` 2026-10-27, min_quotes 10, min_distinct_locations 10,
quote_words [3,25], min_teaches_words 8, row_opened 2026-10-27, tier `A`, status `mined`).

Rows and the capture-only eighth file, digests confirmed on two independent channels (pinned `codeload` tarball
and per-file `raw.githubusercontent.com` fetches; both agree on all 8):

| row | capture | upstream | sha256 | bytes |
|---|---|---|---|---|
| S166 | `test_outputs.py` | `tests/test_outputs.py` | `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec` | 1564 |
| S167 | `test.sh` | `tests/test.sh` | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` | 608 |
| S168 | `instruction.md` | `instruction.md` | `a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96` | 339 |
| S169 | `solve.sh` | `solution/solve.sh` | `e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0` | 1386 |
| S170 | `Dockerfile` | `environment/Dockerfile` | `2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a` | 195 |
| S171 | `task.toml` | `task.toml` | `d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea` | 850 |
| S172 | `README.md` | `README.md` | `591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881` | 1302 |
| — capture only | `gitignore` | `.gitignore` | `9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953` | 177 |

`gitignore` is a capture without a row, exactly as round 45 recorded: rows pin eight of nine captures and
"`gitignore` is a capture, not a row" (`corpus/README.md:632`). P5 still requires it in `SHA256SUMS`. The pin's
whole `polyglot-c-py` tree is these 8 files (`tar tzf`), so the admitted set is complete; there is no
`environment/setup.sh` for this task.

One value is deliberately unfilled, fail-closed (the gate prints a DEFECT until stage 2):

- `receipt_sha256` — Q30 forbids the probe's first recorded run before the stage-2 commit, so no receipt bytes
  exist. Fill: `sha256sum corpus/evidence/round46/polyglot-c-py-probe.txt`.

The probe pin moved three times and is now terminal for this wave: the C3 probe seat first landed a 27966 B draft
(`67a8f4a6…`), replaced it after `R46SentC3Sandbox-2` showed the argv bounded nothing (30238 B, `a96e4226…`), then
made a docstring-only edit carrying the sentinel's three disclosures (31355 B, `22b7779e…`). This seat re-hashed the landed bytes —
`sha256sum .ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py` =
`22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d`, 31355 B — and with gate + probe present under
the spec's two pins the gate prints `P1 ok pinned=2 mismatched=0` (`gate-probe-pin.txt`, re-run at 02:34). Both
superseded digests belong to no landed file: the L1 must copy the 31355 B file, and `67a8f4a6…`/`a96e4226…` appear
in this report only as history. Independently verified on the final bytes: `ast.parse` succeeds, 48 top-level
statements, a 7236-character module docstring, and the docstring really does carry the three disclosures
(`pid`, `60 s`, `fd-1`/`MemoryError`/`nproc`/`die-with-parent`/`DIFF:-`). No retained copy of the 30238 B version
survives in this seat's scratch, so the "docstring-only" scope of that last edit is the probe seat's claim, not a
diff re-measured here; the dry table is measurable and unchanged (`99adfea6…`). The probe's own dry table is byte-identical across both versions
(`99adfea6…`), so no case, prediction or counter pin moved.

## Evidence

**1. Draft spec against the real lane** (every line is a not-built-yet prerequisite; no schema error):

```
ENVELOPE start 02:08:08 cwd=/fast/scratch/hyaku/kengaku-r46/R46ExecC3Spec
P1 DEFECT pinned=2 mismatched=['plans/polyglot_c_py_probe.py']
P2 DEFECT receipt unreadable: corpus/evidence/round46/polyglot-c-py-probe.txt
P3 DEFECT no '## Located quotes' section
P4 DEFECT no parsed quote
P5 DEFECT capture manifest absent: corpus/evidence/round46/tb2-polyglot-c-py/SHA256SUMS
P6 DEFECT rows=7 bad=7 first=S166: rows=0
P7 DEFECT entry unreadable
P8 DEFECT index_rows=52 knowledge_files=52 bad=2 first=index rows for knowledge/tb2-polyglot-c-py-grader.md=0
defects=8
ENVELOPE end 02:08:12 exit=1 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

Command: `envelope.sh "$S/env" python3 plans/pkg_gate.py package --root <lane> --spec "$S/pkg-spec-r46.json"`.

**2. The same fields, satisfied** — a scratch-only synthetic package (the real 8 captures at the real digests,
a synthetic entry with 15 real verbatim quotes, 7 synthetic SOURCES rows, a stub probe that prints the receipt;
never touched the lane, deleted with the scratch dir):

```
ENVELOPE start 02:10:03 cwd=/fast/scratch/hyaku/kengaku-r46/R46ExecC3Spec
P1 ok pinned=2 mismatched=0
P2 ok receipt_sha256=pinned
P3 ok rows=15 distinct_quotes=15 distinct_lines=15 out_of_word_range=0
P4 ok checked=15 bad=0 first=0
P5 ok manifest_entries=8 bad=0 first=0
P6 ok rows=7 bad=0 first=0
P7 ok source_lines=7 bad=0 first=0
P8 ok index_rows=1 knowledge_files=1 bad=0 first=0
P10 ok probe_rerun=byte-equal bytes=67
defects=0
ENVELOPE end 02:10:06 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

That run also proves the `probe_cmd` argv shape executes and reproduces the receipt byte-for-byte (P10) without
any graded case: the stub only prints text. P9 is a property of the landing tree (not a spec field) and was not
exercised; the sim is not a git worktree.

**3. Every pin bites** (`gate-ctl-*.txt`, each run bracketed by its own envelope, all `unchanged`):

| control | moved | gate line |
|---|---|---|
| `gate-ctl-capture-byte.txt` | one byte appended to `solve.sh` | `P5 DEFECT … solve.sh: manifest digest does not match the bytes` |
| `gate-ctl-quote-text.txt` | one space inside a quoted line's text | `P4 DEFECT … test_outputs.py:18: quote not verbatim there` |
| `gate-ctl-spec-pin.txt` | `S166` pin set to 64 zeros | `P5 DEFECT … S166: manifest digest differs from the spec pin` |
| `gate-ctl-sources-url.txt` | `tests/test.sh` → `tests/test_sh.py` in one cell | `P6 DEFECT … S167: url not the pinned raw path` |
| `gate-ctl-receipt-byte.txt` | one byte appended to the receipt | `P2 DEFECT receipt_sha256=7ac4fc7a…` + `P10 DEFECT fresh probe output is not byte-equal` |

**4. Probe pin, re-verified** (`gate-probe-pin.txt`) — the probe seat landed its draft after the first spec run,
so the probe pin was filled from the bytes and re-checked with both instruments present (no probe execution):

```
ENVELOPE start 02:14:23 cwd=/home/vgpnk/Projects/shokunin
P1 ok pinned=2 mismatched=0
P2 DEFECT receipt unreadable: corpus/evidence/round46/polyglot-c-py-probe.txt
…
defects=7
ENVELOPE end 02:14:27 exit=1 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

`sha256sum R46ExecC3Probe/polyglot_c_py_probe.py` = `22b7779e…f1e1`, 31355 B (re-pinned after the sandbox
review; the earlier `67a8f4a6…`/27966 B draft is superseded). After the L1 copies the file to
`plans/polyglot_c_py_probe.py` it must re-measure
`sha256sum plans/polyglot_c_py_probe.py`: an exact copy keeps `P1 ok`; any difference means the landed instrument
is not the probed one and the pin may only move in a named stage-2 amendment, never silently.
The dry table at `R46ExecC3Probe/polyglot-c-py-dry-cases-freeze.txt` is `99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536`
(26 lines: 7 TAG, 18 CASE, `cases=18 predicted_pass=7 predicted_fail=11`); the spec has no field for it — the C3
counter's V5 analogue pins it, as the r45 counter pinned its own dry freeze.

**5. Digest confirmation, two channels** (8/8 agree):

```
200 b94a7a98… tests/test_outputs.py   200 4770437e… tests/test.sh
200 a57c0c0e… instruction.md          200 e768453a… solution/solve.sh
200 2eb537f2… environment/Dockerfile  200 d31b9f60… task.toml
200 591e27f9… README.md               200 9a8dd8d9… .gitignore
```

## Notes the neighbouring seats need

- **C3 probe seat** (messaged): `probe_cmd` is `plans/polyglot_c_py_probe.py --lane .`; its full-run stdout must
  be byte-equal to the receipt; the capture names/digests and the row ids above are the contract.
- **C3 counter author**: the r45 counter's V1 hardcodes the capture set (9 names); the r46 analogue must hardcode
  these 8 names at these digests, including the row-less `gitignore`. The row ids are S166–S172, contiguous, in
  the order of the table. Pin the probe at `22b7779e…` (supersedes `67a8f4a6…`) and the dry table at `99adfea6…`; the receipt stays
  `PENDING-STAGE-2` until the first recorded run after stage 2 (its case ids, in table order, are the probe seat's
  18: `nop, oracle-solve-sh, lookup-table, python-only, c-only, extra-file, leftover-cmain, wrong-value,
  trailing-ws, nonzero-exit, stderr-noise, n-parsed-differently, compile-warning, regrade-same-state, empty-file,
  dir-in-place, crlf-source, value-plus-line`).
- **SOURCES scribe**: 11-cell rows, `source` cell with `<upstream path> — <raw_base><upstream path>` as its only
  URL, `kind` `code` for the four scripts/`Dockerfile` and `docs` for `instruction.md`/`task.toml`/`README.md`
  (this round's C2 correction moves `S156` to `docs`; both values are in the census enum
  `scripts/sources-census.sh:655`), `tier A`, `status mined`, `opened 2026-10-27`, `recheck 180d`, `anchor`
  carrying `sha256 <digest>`, `teaches` ≥ 8 words and pairwise distinct, `used-by` containing the entry path.
- **Entry author**: `verified-at: 2026-10-27`, a `recheck:` line, 7 `source:` lines, a `## Negative space` with a
  falsifier word, and ≥10 quotes of 3–25 words at ≥10 distinct lines — from these files that is reachable but
  tight (`instruction.md` has 9 lines, `Dockerfile` 6), so quotes should be spread over `test_outputs.py` (6+),
  `test.sh`, `instruction.md`, `solve.sh`, `README.md`, `task.toml`.

## Counter contract (V4/V10/V12) — what it changed in my rows

The C3 counter (`R46ExecC3Counter/round46_c3_verify.py`) reads rows S166–S172 from this spec and V12 re-implements
the anchor rule. Every row therefore needs a line-cited quote, a `(K words)` count, a `<file>.<ext>:<a>-<b>` range
where the filename has an extension, and exactly one 64-hex `sha256` token in the row line resolving to exactly one
capture. These cells are computed, not sketched:

| row | anchor cell |
|---|---|
| S166 | `test_outputs.py:1-46, :44 "assert python_out == expected and c_out == expected" (8 words); sha256 b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec` |
| S167 | `test.sh:1-29, :22 "pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA" (5 words); sha256 4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` |
| S168 | `instruction.md:1-9, :1 "Write me a single file in /app/polyglot/main.py.c which is a polyglot, that is, I can run" (16 words); sha256 a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96` |
| S169 | `solve.sh:1-57, :12 "cat <<'EOF' > polyglot/main.py.c" (4 words); sha256 e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0` |
| S170 | `:6 "RUN apt update -y && apt install -y gcc" (9 words); sha256 2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a` |
| S171 | `task.toml:1-41, :22 "timeout_sec = 900.0" (3 words); sha256 d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea` |
| S172 | `README.md:1-24, :4 "This task requires the agent to create a single polyglot source file" (12 words); sha256 591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881` |

Validation on a scratch lane holding the 8 real captures staged in git (no commit; `git ls-files` suffices for the
frozen tool), bracketed by the envelope:

```
ANCHORLINE rows=7 cited=7 captured=7 uncaptured=0 defective=0 repaired=0 live=0 cells=0
ENVELOPE end 02:28:01 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```

and the frozen tool's own selftest in the same envelope: `SELFTEST RED rc=1 ok / GREEN rc=0 ok / JUNK rc=1 ok /
SELFTEST pass`, exit 0. V12's extra conditions were re-checked against the same lane: `digests_in_line=1` and
`resolves_to=[<capture>]` for all 7 rows. Two deliberate shapes: `S170` has no range token because `ARANGE` needs a
`<name>.<ext>:` token and the file is `environment/Dockerfile` (round 45's S152, also a Dockerfile, likewise carried
line+words only); `S172`'s range ends at 24 because the file has 24 `splitlines()` lines with no trailing newline.

### Two row drafts exist; both are V12-clean (measured, corrects a peer claim)

`R46ScribeC3Rows/rows.md` and this seat's `anchors.json` carry different anchor cells for S166–S172. The entry
scribe reported Rows' cells as violating V12 ("straight double quotes inside the quoted text, one-quote-per-cell,
the 3-word floor") and proposed substituting mine wholesale. Measured against V12's own regexes with the captures
re-fetched at the pin, that is not so — **both sets pass**:

```
S166 rows quotes=3 defects=none | mine quotes=1 defects=none
S167 rows quotes=2 defects=none | mine quotes=1 defects=none
S168 rows quotes=3 defects=none | mine quotes=1 defects=none
S169 rows quotes=3 defects=none | mine quotes=1 defects=none
S170 rows quotes=2 defects=none | mine quotes=1 defects=none
S171 rows quotes=3 defects=none | mine quotes=1 defects=none
S172 rows quotes=3 defects=none | mine quotes=1 defects=none
```

Rows uses escaped inner quotes (`\"`), which V12 unescapes before the line compare, and V12 has neither a
one-quote-per-cell rule nor a word floor for registry cells (the 3-word floor is `entry_rules.quote_words`, applied
by P3 to the entry's `## Located quotes`). Both sets also carry exactly one 64-hex `sha256` token per row line and
resolve to the right capture. So the choice is editorial, not rule-driven: which cells read better for a
twelve-grader corpus, and whether 19 quotes in 7 cells is worth the extra surface. Either lands green; what must not
happen is a merge that mixes quote text from one set with word counts or ranges from the other.

### Cross-seat conflict the L1 must settle (not a spec defect)

The probe seat's frozen dry table has **18** case ids; the counter's `DECISIVE` map and its V4/V10 have **16**, and
only 4 ids are shared (`nop`, `oracle-solve-sh`, `extra-file`, `crlf-source`):

- probe table: `nop, oracle-solve-sh, lookup-table, python-only, c-only, extra-file, leftover-cmain, wrong-value,
  trailing-ws, nonzero-exit, stderr-noise, n-parsed-differently, compile-warning, regrade-same-state, empty-file,
  dir-in-place, crlf-source, value-plus-line` (`cases=18 predicted_pass=7 predicted_fail=11`);
- counter `DECISIVE`: `nop, oracle-solve-sh, literal-3case, wrong42, wrong10, zero-ignore-k, extra-file,
  stale-cmain, dir-main, py-syntax-error, c-syntax-error, stderr-c, float-python, float-c, no-print-python,
  crlf-source`.

With today's files `V4` returns "case ids differ from the frozen table" and `V10` returns "DECISIVE keys differ from
the frozen case ids". The dry table is not a spec field (round 45 did the same), so this spec neither causes nor can
fix it: the probe's table or the counter's map has to move before stage 2, and the counter's own comment already
expects the L1 to re-key `DECISIVE` against the probe's frozen ids. Reported to both seats and escalated to the L1,
which acked (02:35 -03): it will re-key `DECISIVE` to the probe's 18 frozen ids at stage 2 and treats
`receipt_sha256` as masked by the counter rather than pinned through this spec, so the `PENDING-STAGE-2` marker can
never become a silent pin. Open only until that stage-2 commit.

### P10 host-safety contract (measured, agrees with `R46SentC3Sandbox-2`)

`pkg_gate.py` chooses P10's interpreter by `import Bio`, not by this package:

```
/usr/bin/python3 3.14.8 | python3 -c "import Bio" -> ModuleNotFoundError: No module named 'Bio'
command -v uv -> /home/vgpnk/.local/bin/uv
uv run --no-project --with biopython==1.85 python3 -c "import Bio"  ->  Downloading numpy (15.9MiB),
   Downloading biopython (3.1MiB), managed CPython under ~/.cache/uv, 0.5 s, 143 MB of cache
```

So a bare `--rerun` runs unpinned PyPI code and a managed interpreter, and is network-dependent. Both branches were
driven with a probe printing `sys.executable`: with no env, P10 fails byte-comparison on the interpreter line; with
`PYTHONPATH=<scratch>/stubbio` (one-line `Bio/__init__.py`) it prints `P10 ok probe_rerun=byte-equal bytes=24`.
The polyglot probe imports no `Bio`, so the stub only steers the gate's branch. The contract for the C3 counter's
V2 is therefore: `TMPDIR=<its scratch>` (this spec's argv carries no path, so the probe's `--work`/`/app` follow
`$TMPDIR`) plus that stub on `PYTHONPATH`. `R46SentC3Sandbox-2` measured that the probe's `/app` is a host `--bind`
of `<work>/app` (24,891 bytes per C case, 7,483 per Python case) until it is a tmpfs, so `TMPDIR` is what keeps that
residue inside the caller's scratch; and that the probe's harness timeout is 1800 s invoked three times per case, so
a looping payload can outlast the task's own 900 s verifier unless the caller cuts wall-clock. Adding `--work` or an absolute path to `probe_cmd` is not an option — a
frozen lane instrument cannot name a host scratch path.

The counter seat has since adopted the contract in its dev copy — `PYTHONPATH=<work>/stubbio` plus `TMPDIR=<work>`,
measured `P10 ok probe_rerun=byte-equal bytes=2800` (`R46ExecC3Counter/control-v2-gate.txt`) — and reports that the
**pinned lane copy** `plans/round46_c3_verify.py` (@ `420eec9`) does not carry it yet (its §Delta 1). Until that copy
takes the fix, a stage-2 `--rerun` from the pinned counter will fetch numpy+biopython and run a managed CPython: the
spec cannot prevent it, the counter's own call site must.

## Risks

1. **One PENDING-STAGE-2 value** (`receipt_sha256`) must be filled at the stage-2 amendment or `P2` stays red; it
   is fail-closed by design, not a placeholder that can silently pass. The probe pin is already frozen at
   `22b7779e…` (supersedes the first draft `67a8f4a6…`), so the L1 must land those exact 31355 probe bytes — any
   reformat, or dropping in the older draft, turns `P1` red.
2. **Row-id drift**: if the C3 scribe numbers rows differently than S166–S172, P6 fails on every row and the
   counter's anchor-digest leg fails with it. The notes file pins the mapping.
3. **Capture-name drift**: `.gitignore` must be saved as `gitignore` (r45 convention); a literal `.gitignore`
   file in the capture dir would be skipped by P5's dotfile filter and the manifest line would not resolve.
4. **P5 strictness**: any stray file left in `corpus/evidence/round46/tb2-polyglot-c-py/` (only 8 captures +
   `SHA256SUMS` are allowed) is a defect; the manifest must use plain `sha256sum` spacing.
5. **Q30**: do not run `pkg_gate.py package --rerun` on the real package and do not record the probe's first run
   before the stage-2 commit; the spec's `--rerun` leg only becomes meaningful afterwards.
6. **Dry-table id divergence** (above): 18 probe ids vs 16 counter ids, 4 shared. C3 cannot pass V4/V10 while both
   files stand; the L1 has acked the stage-2 re-key of `DECISIVE`, so this is a scheduled fix, not an open blocker.
   The counter reports its dev copy re-keyed to the 18 ids, while the pinned `plans/round46_c3_verify.py` and the
   committed `plans/filler46/` dry table still carry 16 — both must move together, or V13's V10 leg defects on pin
   alignment rather than on filler content.
7. **P10 is not host-safe as a bare call**: without `TMPDIR` under scratch and the `Bio` stub on `PYTHONPATH`, the
   gate's rerun fetches numpy + biopython from PyPI and writes ~143 MB into `~/.cache` under a managed CPython. The
   spec cannot fix this in `probe_cmd`; the counter must pass the environment — its dev copy does, its pinned lane
   copy (`plans/round46_c3_verify.py` @ `420eec9`) does not yet (§Delta 1 in `R46ExecC3Counter`'s report).
8. **Two row drafts**: `R46ScribeC3Rows` and this seat both pass V12 (above). A merged cell that takes Rows' quoted
   text with my word count or range end is the one way this goes red; land one set of cells, not a blend.
9. **Anchor drift**: the 7 anchor cells above are validated against the frozen tool; a scribe that rewrites a quote,
   a line number, the word count or the range end turns V12 (and C2 leg A) red on that row. `S170` must stay
   range-less and `S172` must keep `1-24`.

## Tooling

Nothing installed or upgraded; no pacman, no `uv tool`. Host scratch `$S=/fast/scratch/hyaku/kengaku-r46/R46ExecC3Spec`
deleted with `plans/scratch_guard.py safe-rm` at the end of the seat.

VERDICT: pkg-spec-r46-rows-7-fields-checked-13
