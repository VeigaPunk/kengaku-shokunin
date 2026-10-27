# R46ExecC3Capture — TB2 `polyglot-c-py` capture at the pin (round 46, wave 1)

Seat: executor, leaf. Scope executed: capture every file of `polyglot-c-py` at terminal-bench-2
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`, flat basenames per round-45 convention, `SHA256SUMS`, one re-fetch with
`cmp`, and the same paths at upstream HEAD for drift. No lane file was written; nothing in `~/.local/bin`, `plans/`,
`corpus/` or a shared PATH directory was touched.

Deliverable (the only lane write, both under my seat dir):
`.ufo/waves/round-46/w1/R46ExecC3Capture/tb2-polyglot-c-py/` — 8 captures + `SHA256SUMS`;
`.ufo/waves/round-46/w1/R46ExecC3Capture/capture-receipt.txt` (raw envelope stdout, 3801 B) and
`capture-table.txt` (the table below, machine-greppable).

## 1. Tree at the pin — 8 entries, all regular blobs

`curl -sS "https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88…?recursive=1"` →
`HTTP 403`, body `{"message":"API rate limit exceeded for 179.218.13.209. …}` (unauthenticated; also 403 on the bare
tree endpoint). **Tree authority taken instead from git**, which is complete for the commit (trees are not lazy in a
`--filter=blob:none` clone):

```
git clone -q --filter=blob:none --no-checkout https://github.com/harbor-framework/terminal-bench-2.git "$S/tb2"
git -C "$S/tb2" ls-tree -r --long 2fd12b88aafdd04a52c298e3940bcb189f9766d6 -- polyglot-c-py
```

8 rows, every one `100644 blob`:

| upstream path | capture | blob (git, pin) | bytes (git) |
|---|---|---|---|
| `polyglot-c-py/.gitignore` | `gitignore` | `ecd089e8ac7767b9bdb6f3ac247c8d033f7565ab` | 177 |
| `polyglot-c-py/README.md` | `README.md` | `99c24b1ced574157d68a64fb7f41d5be0eb9765e` | 1302 |
| `polyglot-c-py/environment/Dockerfile` | `Dockerfile` | `3d06d0c3263ef799a46da2bdb6877e20a0227791` | 195 |
| `polyglot-c-py/instruction.md` | `instruction.md` | `31039ba18f88567191d599ecf0a76d50f5beee47` | 339 |
| `polyglot-c-py/solution/solve.sh` | `solve.sh` | `0b3fee242a501389348e379494749ec2c9ae871e` | 1386 |
| `polyglot-c-py/task.toml` | `task.toml` | `52ff891a3fd5f7e4a987e8ec514d02c636bd7c11` | 850 |
| `polyglot-c-py/tests/test.sh` | `test.sh` | `cb4a41a45e4b23f4d1f1392fd68f6e47c5dbbf57` | 608 |
| `polyglot-c-py/tests/test_outputs.py` | `test_outputs.py` | `e3d4b2b3ac689c9ea5546ae764e813ad65f2adb9` | 1564 |

Consequences a C3 row/probe author must not lose: **no symlink, no submodule, no executable mode anywhere in the task
directory** (all `100644`, so `solution/solve.sh` and `tests/test.sh` are *not* executable upstream — invoke them as
`bash <path>`). There is no `setup.sh` in this task (unlike round-45 `password-recovery`), so a C3 row must not invent
one.

## 2. Capture table — path → bytes → lines → sha256

`sha256` is of the delivered capture bytes; `bytes`/`lines` measured on the delivered files.

| upstream | capture | bytes | lines | words | sha256 |
|---|---|---:|---:|---:|---|
| `.gitignore` | `gitignore` | 177 | 23 | 24 | `9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953` |
| `README.md` | `README.md` | 1302 | 23 | 182 | `591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881` |
| `environment/Dockerfile` | `Dockerfile` | 195 | 6 | 25 | `2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a` |
| `instruction.md` | `instruction.md` | 339 | 9 | 52 | `a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96` |
| `solution/solve.sh` | `solve.sh` | 1386 | 57 | 222 | `e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0` |
| `task.toml` | `task.toml` | 850 | 41 | 102 | `d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea` |
| `tests/test.sh` | `test.sh` | 608 | 29 | 89 | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` |
| `tests/test_outputs.py` | `test_outputs.py` | 1564 | 46 | 162 | `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec` |
| **total** | 8 files | **6421** | 234 | 858 | `SHA256SUMS` = 617 B, sha256 `a44b38ea85e4611f62cd93104923e70f1e516200b2084d5f7500f8d50e26c496` |

`SHA256SUMS` (round-45 byte format, `sha256␠␠name`, sorted by capture name):

```
9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953  gitignore
591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881  README.md
2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a  Dockerfile
a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96  instruction.md
e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0  solve.sh
d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea  task.toml
4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334  test.sh
b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec  test_outputs.py
```

Verification of the delivered copy: `cd …/tb2-polyglot-c-py && sha256sum -c SHA256SUMS` → 8× `: OK`; 8 lines, 0
duplicate names.

Newline state of the captures (relevant to C2's only-CR leg and to C3's held-out predictor kinds): **0 CRLF lines and
0 lone CR in all 8**; 7 of 8 end with `\n`, `README.md` ends with the byte `0x36` (`6`) and therefore has **no trailing
newline**.

Line-count convention (matters for S166+ anchor cells; peer `R46ScribeC3Rows` independently fetched the same bytes):
the `lines` column above is `wc -l`, i.e. newline-terminated lines. For the 7 files ending in `\n` that equals the
logical line count; `README.md` is `wc -l` 23 but **24 logical lines** — line 24 is
`4. Test cases: f(0)=0, f(10)=55, f(42)=267914296` with no terminating newline, so a `README.md:24 "…"` anchor is legal
and a naive "last legal index = `wc -l`" rule would wrongly report it out of range.

## 3. Re-fetch and drift

Re-fetch: every file downloaded a second time from the same pinned raw URL into `$S/fetch2` and `cmp -s` against fetch
1 — `REFETCH total=8 identical=8`.

Independent of HTTP, each capture was also `cmp`ed against the commit's own blob (`git -C "$S/tb2" cat-file blob
2fd12b88…:polyglot-c-py/<path>`, blobs fetched on demand by the promisor) — `GITBLOB matched=8/8`.

Drift at HEAD: `HEAD` raw URL (default branch) for the same 8 paths — `HEAD drift_files=0 of 8`. **This drift figure is
measured but degenerate, and should be reported as such:** the pin *is* the current default-branch tip —

```
git -C "$S/tb2" rev-parse HEAD                    -> 2fd12b88aafdd04a52c298e3940bcb189f9766d6
git -C "$S/tb2" rev-parse origin/HEAD             -> 2fd12b88aafdd04a52c298e3940bcb189f9766d6   (-> origin/main, branch `main`)
git -C "$S/tb2" log -1 --format='%H %ci %s'       -> 2fd12b88… 2026-04-29 22:53:30 -0700 Add task metadata to task manifests
```

So "0 drift" here certifies *the capture matches the commit*, not that the task has been stable over time. If C3's
freshness wording needs a non-degenerate drift number, it must be measured against a later commit, which does not exist
upstream yet.

## 4. Envelope (host-safety rule)

Every fetch/cmp/blob pass ran inside the round-46 envelope with `~/.local/bin` read-only; the shipped
`capture.sh` wrote only inside `$S`. Pasted verbatim:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46ExecC3Capture/env /fast/scratch/hyaku/kengaku-r46/R46ExecC3Capture/env --bind /fast/scratch/hyaku/kengaku-r46/R46ExecC3Capture/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- bash /fast/scratch/hyaku/kengaku-r46/R46ExecC3Capture/capture.sh /fast/scratch/hyaku/kengaku-r46/R46ExecC3Capture
ENVELOPE start 02:05:16 cwd=/fast/scratch/hyaku/kengaku-r46/R46ExecC3Capture
…
ENVELOPE end 02:05:23 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

Command: `envelope.sh "$S/env" bash "$S/capture.sh" "$S"` (outer exit 0; `RESULT fail=0 files=8`). No tool was
installed; no `pacman`, no `uv tool`, nothing added to a PATH directory.

## 5. Findings the C3 entry/counter should carry (observed at the pin)

1. **Mechanism, with exact order** (`test_outputs.py`): `os.listdir("/app/polyglot") == ["main.py.c"]` is asserted
   *first* (`:17-20`), then `gcc … -o /app/polyglot/cmain` (`:23-25`) writes the second file into that same directory,
   then per case `python3 …/main.py.c N` (`:30-36`) and `/app/polyglot/cmain N` (`:37-43`), both `.strip()`ped and both
   compared to the same expected string (`:44-46`). Cases `[(42, "267914296"), (10, "55"), (0, "0")]` (`:27`). No
   timing, no source inspection — the claims' class wording holds.
2. **Two different Pythons, not one.** `tests/test.sh:18-22` runs the harness under `uvx -p 3.13 … pytest==8.4.1`,
   while the graded `python3` of `test_outputs.py:31` is resolved from the *task image's* PATH (`Dockerfile:2`
   `FROM ubuntu:24.04`, `Dockerfile:6` installs `gcc` only; `instruction.md:9` claims "python3 3.12.3 and gcc
   13.2.0"). The entry must not state that the polyglot is graded by 3.13. [INFERENCE] that the verifier shell shares
   the task container, so subprocess `python3` = image 3.12.3; not observed here (no image pulled, no graded case run —
   Q30 order rule respected: this seat ran no case of the task).
3. **Two of the eight captures are task-independent harness bytes.** `test.sh` and `gitignore` are byte-identical to
   round-45 `password-recovery`'s captures (`cmp` → `SAME-as-round45 test.sh`, `SAME-as-round45 gitignore`; the other
   six differ). Any C3 leg that decides "this package is about polyglot-c-py" from the presence of those two files —
   or a filler package that ships them — is testable-but-weak; the discriminating bytes are `test_outputs.py`,
   `instruction.md`, `task.toml`, `solve.sh`, `README.md`, `Dockerfile`.
4. **Quirk in `solve.sh`:** line 1 is the canary comment and `#!/bin/bash` sits on `:2`, so the file has no effective
   shebang and no exec bit; the reference solution only works as `bash solution/solve.sh` from `WORKDIR /app`
   (`Dockerfile:4`), writing `polyglot/main.py.c` relatively (`solve.sh:11-12`).
5. **`task.toml` facts worth a row cell:** `docker_image = "alexgshaw/polyglot-c-py:20251031"` (`:29`), `cpus = 1`,
   `memory_mb = 2048`, `allow_internet = true` (`:30-34`), `timeout_sec = 900.0` for verifier and agent (`:22`, `:25`),
   `difficulty = "medium"`, author Nicholas Carlini (`:9`, `:15`).

## 6. Candidate stage-2 material for `plans/pkg-spec-r46.json` (for the L1, not written by me)

```json
"raw_base": "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/",
"capture_dir": "corpus/evidence/round46/tb2-polyglot-c-py",
"rows": {
  "S166": {"capture": "test_outputs.py",  "upstream": "tests/test_outputs.py",  "sha256": "b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec"},
  "S167": {"capture": "instruction.md",   "upstream": "instruction.md",         "sha256": "a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96"},
  "S168": {"capture": "Dockerfile",       "upstream": "environment/Dockerfile",  "sha256": "2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a"},
  "S169": {"capture": "test.sh",          "upstream": "tests/test.sh",           "sha256": "4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334"},
  "S170": {"capture": "README.md",        "upstream": "README.md",               "sha256": "591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881"},
  "S171": {"capture": "solve.sh",         "upstream": "solution/solve.sh",       "sha256": "e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0"},
  "S172": {"capture": "task.toml",        "upstream": "task.toml",               "sha256": "d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea"},
  "S173": {"capture": "gitignore",        "upstream": ".gitignore",              "sha256": "9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953"}
}
```

Row ids/ordering are the L1's call (the claims only pin "rows from S166"); the capture names, upstream paths, sha256s
and line counts above are measured. If the counter needs an ordered row→capture map, prefer
`test_outputs.py, instruction.md, Dockerfile, test.sh, README.md, solve.sh, task.toml, gitignore` (the round-45 spec's
S149–S156 order extended by the two remaining files), and note that the L1 must copy these captures into
`corpus/evidence/round46/tb2-polyglot-c-py/` — this seat wrote them only under its own report subdir.

## 7. Receipts retained

- `.ufo/waves/round-46/w1/R46ExecC3Capture/tb2-polyglot-c-py/` — 8 captures + `SHA256SUMS` (total 7038 B incl. sums).
- `.ufo/waves/round-46/w1/R46ExecC3Capture/capture-receipt.txt` — full envelope + every FETCH/REFETCH/HEAD/GITBLOB/ROW
  line quoted in §1–§4 (3801 B).
- `.ufo/waves/round-46/w1/R46ExecC3Capture/capture-table.txt` — §2 table with git blob ids, greppable.
- Line/word counts and newline stats above were produced by `wc -l/-w`, `stat -c %s`, `sha256sum` and a `re` non-`\n`
  `\r` count on the delivered files (§2, §1).

## 8. Limits / blockers

- GitHub tree API unavailable (HTTP 403, unauthenticated rate limit); tree taken from `git ls-tree` at the commit —
  equivalent authority, recorded above so the L1 need not re-derive it.
- "Head drift 0/8" is degenerate (pin == `origin/main` tip); it is *not* evidence of stability over time.
- Nothing was pulled from Docker Hub and no graded case was executed (Q30 order rule); `task.toml`'s `docker_image`
  tag was read, not resolved, so its digest is unverified by this seat.
- Only possibility of an incomplete capture is a path the commit does not track; the commit tracks exactly the 8 files
  listed and `git ls-tree` shows no symlink or submodule entry that could hide further content.

VERDICT: polyglot-captures-8-refetch-identical-8/8-head-drift-0
