# pkg-spec-r46.json — field notes (draft for L1 integration)

Draft location for the landing tip: `plans/pkg-spec-r46.json` (this directory holds the byte-identical draft,
sha256 `171feaff3addcdc1445e4188ff038167305610db57196cebcebf6fe73ecb84fd`). Schema is the round-45 schema
verbatim (`plans/pkg-spec-r45.json`, 13 top-level keys, no key added, none dropped) so `plans/pkg_gate.py`
and the round-45 C2 counter's V1–V11 re-pointed by the C3 counter read the same names.

## The 13 top-level fields

| field | value | why / which check reads it |
|---|---|---|
| `name` | `round-46 tb2-polyglot-c-py package` | label only; no check reads it (r45 carries one, kept for parity). |
| `entry` | `corpus/knowledge/tb2-polyglot-c-py-grader.md` | P3/P4 (Located quotes), P6 (`used-by` cell must contain exactly this path), P7 (`source:` lines), P8 (index row + coverage bullet name the basename). |
| `capture_dir` | `corpus/evidence/round46/tb2-polyglot-c-py` | P4 (quote captures resolved under it, path-safety checked), P5 (its `SHA256SUMS`). Claims §C3 fixes the same path. |
| `receipt` | `corpus/evidence/round46/polyglot-c-py-probe.txt` | P2 (digest), P8 (`receipt_rel` = `evidence/round46/polyglot-c-py-probe.txt` must appear in the coverage bullet), P10 (byte-compared against a fresh probe run). Claims §C3 fixes the same path. |
| `receipt_sha256` | **`PENDING-STAGE-2`** | P2. Cannot be filled now: QUALITY Q30 order rule forbids the probe's first recorded run before the stage-2 commit, so no receipt bytes exist. Fail-closed on purpose — the gate prints `P2 DEFECT receipt_sha256=PENDING-STAGE-2` until stage 2 pins it. **Fill command (stage 2, after the probe's first recorded run):** `sha256sum corpus/evidence/round46/polyglot-c-py-probe.txt`. |
| `probe_cmd` | `["plans/polyglot_c_py_probe.py", "--lane", "."]` | P10 executes exactly this argv with `cwd=<root>` and compares stdout to the receipt bytes. Mirrors the r45 form (`--lane .`), which the round-45 probe supports (`plans/password_recovery_probe.py:285`). Deliberately carries no `--work` or absolute path: the probe's `--work` defaults to `$TMPDIR`, so the caller's `TMPDIR` governs where it writes (see "P10 interpreter and scratch" below). |
| `sources` | `corpus/SOURCES.md` | P6 parses registry rows here. |
| `readme` | `corpus/README.md` | P8 index rows, coverage bullet, and the `knowledge_glob` ↔ index bijection. |
| `knowledge_glob` | `corpus/knowledge/*.md` | P8d: the set of files matching it must equal the set of index rows. Today both are 52 (`P8 DEFECT index_rows=52 knowledge_files=52` on the lane). |
| `raw_base` | `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/` | P6 (`raw_base + upstream` must be the cell's only URL), P7 (`source:` URL must be the same string). Pin is the claims' `2fd12b88…`. |
| `rows` | 7 rows, S166–S172 (below) | P5 (`capture` must be in the manifest at the row's digest), P6 (one 11-cell SOURCES row per id). |
| `frozen_instruments` | `plans/pkg_gate.py` = `ea63882…` (its live digest, `sha256sum plans/pkg_gate.py`), `plans/polyglot_c_py_probe.py` = `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d` | P1. The gate digest is the round-45 freeze digest, re-verified today. The probe digest is the C3 probe seat's artifact, re-hashed by this seat from `.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py` — so the L1 MUST copy that file to `plans/polyglot_c_py_probe.py` byte-verbatim, or `P1` goes red. Superseded pin: `67a8f4a68fcdf190…` (the probe's first draft, 27966 B) was replaced after the sandbox review; only this field moved. Verified with the new bytes: `P1 ok pinned=2 mismatched=0` (`gate-probe-pin.txt`). |
| `entry_rules` | see below | P3 (`min_quotes`, `min_distinct_locations`, `quote_words`), P6 (`row_tier`, `row_status`, `min_teaches_words`), P7 (`verified_at`). |

### `entry_rules` sub-keys

| key | value | consumed by |
|---|---|---|
| `verified_at` | `2026-10-27` | P7: the entry must contain the literal line `verified-at: 2026-10-27`. |
| `min_quotes` | `10` | P3: distinct quote texts ≥ 10. Round-45 bar, kept: 8 captures but ≥10 decisive lines is reachable (r45 had 16 quotes from 9 captures). |
| `min_distinct_locations` | `10` | P3: distinct `(capture, start-line)` pairs ≥ 10, so the entry must quote ≥10 different lines. |
| `quote_words` | `[3, 25]` | P3: every quote `3 ≤ words ≤ 25`; P4 also requires the text verbatim on its cited lines. |
| `min_teaches_words` | `8` | P6: every SOURCES `teaches` cell ≥ 8 words, and the 7 cells pairwise distinct. |
| `row_opened` | `2026-10-27` | not gate-read (P6 reads the cell, not this rule); records the claims' opening date so the scribe can copy it. |
| `row_tier` | `A` | P6: registry `tier` cell must be exactly `A` (source code / primary). |
| `row_status` | `mined` | P6: registry `status` cell must be exactly `mined`. |

## `rows` — the 7 rows (S166–S172) and the capture-only eighth

Row order follows the assignment's listing (grader first, then harness, instruction, oracle, image, metadata,
prose). Digests are upstream bytes at the pin, confirmed on two independent channels (pinned tarball via
`codeload` and per-file `raw.githubusercontent.com` fetches), and the captures must be byte copies, so the
capture digest equals the upstream digest.

| row | capture (in `capture_dir`) | upstream | sha256 | bytes |
|---|---|---|---|---|
| S166 | `test_outputs.py` | `tests/test_outputs.py` | `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec` | 1564 |
| S167 | `test.sh` | `tests/test.sh` | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` | 608 |
| S168 | `instruction.md` | `instruction.md` | `a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96` | 339 |
| S169 | `solve.sh` | `solution/solve.sh` | `e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0` | 1386 |
| S170 | `Dockerfile` | `environment/Dockerfile` | `2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a` | 195 |
| S171 | `task.toml` | `task.toml` | `d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea` | 850 |
| S172 | `README.md` | `README.md` | `591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881` | 1302 |
| — (capture only) | `gitignore` | `.gitignore` | `9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953` | 177 |

Why `gitignore` is a capture and not a row: round-45 precedent — `corpus/README.md:632` records that row ids
pin eight of the nine captures, "`gitignore` is a capture, not a row". The dotfile teaches nothing about the
grader and the grader/oracle never read it; P5 still requires it in `SHA256SUMS`, and it is admitted as
`gitignore` (dot stripped, same as the r45 capture name).

Why these are the whole admitted set: the pin's `polyglot-c-py` tree has exactly these 8 files
(`tar tzf` of the pinned tarball), all small; nothing else exists for the grader or oracle to depend on.
`environment/setup.sh` does **not** exist for this task (the r45 package had one), so no such row.

## Capture recipe (for the L1 / capture builder)

```bash
S=<scratch>; B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py
D=corpus/evidence/round46/tb2-polyglot-c-py; mkdir -p "$D"
for f in tests/test_outputs.py tests/test.sh instruction.md solution/solve.sh environment/Dockerfile task.toml README.md .gitignore; do
  out=$(echo "$f" | sed 's|.*/||; s|^\.||'); curl -fsS "$B/$f" -o "$D/$out"
done
(cd "$D" && sha256sum Dockerfile README.md gitignore instruction.md solve.sh task.toml test.sh test_outputs.py > SHA256SUMS)
```

`SHA256SUMS` must be `"<64 hex>  <name>"` per line (the gate's `MANIFEST_LINE`; two spaces, as `sha256sum`
writes it) and must list all 8 captures, nothing else. `gitignore` is saved as the capture name, not `.gitignore`.

## Probe handoff (measured, not assumed)

The C3 probe seat's draft lives at `.ufo/waves/round-46/w1/R46ExecC3Probe/`; this seat re-hashed it:

| artifact | bytes | sha256 |
|---|---|---|
| `polyglot_c_py_probe.py` | 31355 | `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d` |
| `polyglot-c-py-dry-cases-freeze.txt` | 5355 | `99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536` |

- The probe's own PINS are the seven row captures (not `gitignore`), equal to this spec's row digests.
- After the L1 copies the probe to `plans/polyglot_c_py_probe.py` it must re-measure; the spec's
  `frozen_instruments` pin is those bytes, so an exact copy prints `P1 ok pinned=2 mismatched=0` (`gate-probe-pin.txt`)
  and any drift is a red `P1` that may only be cleared by a named stage-2 amendment.
- The dry table has no spec field (as in round 45); the C3 counter pins it. Its 18 case ids in table order:
  `nop, oracle-solve-sh, lookup-table, python-only, c-only, extra-file, leftover-cmain, wrong-value, trailing-ws,
  nonzero-exit, stderr-noise, n-parsed-differently, compile-warning, regrade-same-state, empty-file, dir-in-place,
  crlf-source, value-plus-line`; summary `cases=18 predicted_pass=7 predicted_fail=11`; every second grade is
  predicted `F` because the grader's own `gcc` leaves `/app/polyglot/cmain`.
- Order rule status reported by the probe seat: only `--dry` (twice, byte-stable) and `--stage-check` (18/18) ran;
  the grader's test function was never imported or called. `receipt_sha256` therefore stays `PENDING-STAGE-2`.

## SOURCES cells the C3 scribe must write (P6 + round-45 V3 anchor style)

Each row: 11 cells `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` with

- `source` = `` `<upstream path>` — <raw_base><upstream path> `` — the URL must be the *only* URL in the cell and
  exactly `raw_base + upstream` (P6).
- `kind` = `code` for `test_outputs.py`, `test.sh`, `solve.sh`, `Dockerfile`; `docs` for `instruction.md`,
  `task.toml`, `README.md` — this round's C2 correction supersedes r45's `S156` with `kind` `code`→`docs`, so
  prose and the metadata manifest are `docs` here. P6 does not read this cell; it is consistency guidance.
- `tier` = `A`, `status` = `mined`, `opened` = `2026-10-27`, `recheck` = `180d` (round-45 precedent for the same
  pinned-commit task files, `S149`–`S156`; `on-release` stays for sources refreshed by a release).
- `anchor` must carry `sha256 <row digest>` literally, and — this round's C3 V12 plus the frozen
  `plans/anchor_line_check.py` — a line-cited quote `:<N> "<quote>"`, a `(<K> words)` count right after it, and a
  `<file>.<ext>:<a>-<b>` range holding N. Copy the validated cells below verbatim; each has exactly ONE 64-hex
  token in the whole row line (V12 rejects a second), no straight `"` inside the quote, and a digest that resolves
  to exactly one capture name.
- `teaches` ≥ 8 words, pairwise distinct.
- `used-by` must contain `corpus/knowledge/tb2-polyglot-c-py-grader.md`.

### Exact anchor cells (validated, copy verbatim)

| row | anchor cell |
|---|---|
| S166 | `test_outputs.py:1-46, :44 "assert python_out == expected and c_out == expected" (8 words); sha256 b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec` |
| S167 | `test.sh:1-29, :22 "pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA" (5 words); sha256 4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` |
| S168 | `instruction.md:1-9, :1 "Write me a single file in /app/polyglot/main.py.c which is a polyglot, that is, I can run" (16 words); sha256 a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96` |
| S169 | `solve.sh:1-57, :12 "cat <<'EOF' > polyglot/main.py.c" (4 words); sha256 e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0` |
| S170 | `:6 "RUN apt update -y && apt install -y gcc" (9 words); sha256 2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a` |
| S171 | `task.toml:1-41, :22 "timeout_sec = 900.0" (3 words); sha256 d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea` |
| S172 | `README.md:1-24, :4 "This task requires the agent to create a single polyglot source file" (12 words); sha256 591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881` |

Validation (02:27 -03, scratch lane with the 8 real captures staged in git, spec rows as the row set):

```
ANCHORLINE rows=7 cited=7 captured=7 uncaptured=0 defective=0 repaired=0 live=0 cells=0   (exit 0)
SELFTEST RED rc=1 ok | GREEN rc=0 ok | JUNK rc=1 ok | SELFTEST pass                          (exit 0)
```

and the counter's V12 resolution conditions re-checked by hand: `digests_in_line=1` and `resolves_to=[<capture>]`
for all 7 rows. `S170` carries no range token on purpose: `ARANGE` needs a `<name>.<ext>:` token and the file is
`environment/Dockerfile` with no extension — round 45's S152 (also a Dockerfile) likewise carried only
line+words. `S172`'s range end is 24, not 23: the file has 24 `splitlines()` lines and no trailing newline.

## Entry-side requirements this spec pins (checked by the sim, below)

- `verified-at: 2026-10-27`, a `recheck:` line, and a non-empty `## Negative space` section whose text matches
  `falsifi(er|ed|es|ability)` (P7).
- `source: S1NN <url>` once per row, each URL exactly `raw_base+upstream` (P7).
- `## Located quotes` table, one row per quote, 3 columns, form `| claim | “text” | `capture:N` |` (P3/P4);
  every cited capture must be in the manifest (P5).
- `corpus/README.md`: one index row for the entry citing all 7 row ids, plus a `- ` bullet naming the entry
  basename and `evidence/round46/polyglot-c-py-probe.txt` (P8).

## Evidence that the spec's fields are the right ones

1. `gate-on-lane.txt` — the draft run against the real lane (envelope): `defects=8`, and every line is a
   package-not-built prerequisite (`P1` probe PENDING, `P2` receipt absent, `P3`/`P4`/`P7` entry absent,
   `P5` manifest absent, `P6` rows=7 bad=7 `rows=0`, `P8` index row absent). No defect is a schema error, so the
   spec's key names are the ones the gate reads.
2. `gate-sim-ok.txt` — a scratch-only synthetic package (real captures, real digests, a synthetic entry with 15
   real quotes, 7 synthetic SOURCES rows, a stub probe) run through the same gate: `P1 ok … P8 ok P10 ok
   defects=0`. This proves every field is *satisfiable* in the shape the spec fixes (the probes' argv included,
   P10 byte-equal on 67 bytes). The sim never touched the lane and was deleted with the scratch dir.
3. Negative controls (`gate-ctl-*.txt`), each one pin moved: a capture byte (`P5 … manifest digest does not
   match the bytes`), a quote text (`P4 … quote not verbatim there`), a row digest in the spec (`P5 … S166:
   manifest digest differs from the spec pin`), a SOURCES URL (`P6 … url not the pinned raw path`), a receipt
   byte (`P2` digest + `P10 fresh probe output is not byte-equal`). Every pin this spec sets is enforced.

`P9` (clean tree) is a property of the landing tree, not a spec field; not exercised here. `P10` in the real
lane stays off until the stage-2 receipt exists (`--rerun` is forbidden on this package before stage 2 by Q30).

## Field-count

13 top-level fields, all read by at least one gate clause; 7 rows × 3 sub-fields + 1 capture-only file.

## Probe re-pin (after the sandbox review)

The probe seat replaced its file after `R46SentC3Sandbox-2` found the argv bounded nothing, and then made a
docstring-only edit carrying the sentinel's three disclosures (pid-namespace sharing, one 60 s budget across four
phases, and the fd-1 redirect not bounding the payload): prlimit prefix, sized
tmpfs `/tmp`+`/app` (no host bind), bounded `/dev`+`/dev/shm`, `--unshare-all` + `--hostname`, `--clearenv`/`--setenv`,
60 s timeout with a 1 MiB stdout cap, and both grade legs in one sandbox invocation. Measured here:
`sha256sum R46ExecC3Probe/polyglot_c_py_probe.py` = `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d` (31355 B, superseding `67a8f4a6…`/27966 B and
`a96e4226…`/30238 B; `ast.parse` ok, 48 top-level statements, 7236-character docstring). The dry table is byte-identical to the
earlier one (`99adfea6…`, 5355 B, 26 lines, `cases=18 predicted_pass=7 predicted_fail=11`), so the case ids, the
predictions and the counter's pins stand. `probe_cmd`, the receipt path and `PENDING-STAGE-2` are unchanged; only
`frozen_instruments["plans/polyglot_c_py_probe.py"]` moved, and with it the spec's own digest
(`171feaff3addcdc1445e4188ff038167305610db57196cebcebf6fe73ecb84fd`).

## P10 interpreter and scratch (measured)

`plans/pkg_gate.py` (frozen) picks P10's interpreter by trying `import Bio`, not by anything in this package:

```
python3 -c "import sys;print(sys.executable)"  -> /usr/bin/python3 3.14.8
python3 -c "import Bio"                        -> ModuleNotFoundError: No module named 'Bio'
command -v uv                                  -> /home/vgpnk/.local/bin/uv
```

So on this host P10 takes `["uv","run","--no-project","--with","biopython==1.85","python3"] + probe_cmd`:
measured 0.5 s and `Downloading numpy (15.9MiB)` + `Downloading biopython (3.1MiB)`, a managed CPython under
`~/.cache/uv/builds-v0/...`, and **143 MB** of cache writes — network-dependent, and outside bwrap unless the caller
brackets it. The probe itself imports no `Bio` (argparse/dataclasses/hashlib/os/pathlib/re/subprocess/sys/tempfile),
so the branch is pure gate overhead.

Both branches measured with a one-line probe that prints `sys.executable` and a receipt expecting
`/usr/bin/python3` (`branch-uv.txt`, `branch-stub.txt`):

| caller env | P10 |
|---|---|
| none | `P10 DEFECT fresh probe output is not byte-equal to the receipt` (uv branch: different interpreter line) |
| `PYTHONPATH=<scratch>/stubbio` with `stubbio/Bio/__init__.py` = `version = "1.85"` | `P10 ok probe_rerun=byte-equal bytes=24` (sys.executable branch) |

**Contract for whoever runs `--rerun`** (the C3 counter's V2): invoke the gate with `TMPDIR=<its scratch>` — this
spec's argv names no path, so `--work`/`/app` land under `$TMPDIR` — and with the `Bio` stub on `PYTHONPATH` to keep
the rerun offline and out of `~/.local/bin`/`~/.cache`. This is a caller contract, not a spec field: a frozen
lane instrument cannot name a host scratch path.
