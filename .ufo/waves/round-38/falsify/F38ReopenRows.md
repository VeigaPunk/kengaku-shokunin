# F38ReopenRows — re-opening S115/S116 at `2fd12b88` (kengaku round 38, wave 2, falsify)

Seat: critic, leaf, no subagents. Lane under attack: `kengaku-shokunin` tip `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`.
Pin: terminal-bench-2 `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (commit date `2026-04-30T05:53:30Z`).
Scratch: `/fast/scratch/hyaku/kengaku-r38/F38ReopenRows/` (mutation clone at the tip, `git -C … rev-parse --show-toplevel`
= that path; deleted before yield). No lane file edited; no mutating git in the lane; no pacman.

Receipts in this directory: `reopen-rows-receipt.sh` (re-runnable, `bash reopen-rows-receipt.sh`) →
`reopen-rows-receipt.txt` (all numbers below), `gate-forged-row.txt`, `gate-forged-entryquote.txt`.

## Verdict on the assigned surface

Both rows reopen clean: live bytes at the pin equal the row anchors and the capture `SHA256SUMS`; both row quotes are
byte-verbatim at their cited lines. Two secondary defects and two precision items follow, none of which touches a
frozen C2 predicate: (1) no clause in the round-38 counter or the package gate reads a SOURCES row's **quote** — a forged
row quote stays green; (2) the entry's documented recheck command reds on a healthy tree; (3) the TB2.1 comparison the
entry makes is unpinned; (4) the contestable-tag wording should name its TB2.0 scope.

## 1. Rows S115 / S116, re-opened live

| Check | S115 (`tests/test_outputs.py`) | S116 (`instruction.md`) |
|---|---|---|
| HTTP + live sha256 | `200 d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85` | `200 1606850579342a8b8f2189de0e499fae6be21198150d8dd1e4d18c2efbcf3b82` |
| Row anchor cell | `d9d2796d…01f4e85` (one `sha256` token) | `16068505…bf3b82` (one `sha256` token) |
| `SHA256SUMS` (run inside the dir) | `test_outputs.py: OK` | `instruction.md: OK` |
| Live vs committed capture | `byte-identical` | `byte-identical` |
| Cited line, `sed -n 46p` / `9p` | `    assert re.match(r"Results: \d+ \d+ \d+", battle_result), (` | `We'll verify the binary has no X11 dependencies, uses Debian sources, and that the debugger works properly.` |
| Row quote vs that line | equal after stripping 4 spaces of indent; 7 words as stated | equal exactly (0 indent); 17 words as stated |
| Registry cells | 11 | 11 |
| Binding under the landed D3 tool | `BIND S115 … by=url-task`, `RESOLVED … via=corpus/evidence/round38/tb2-build-pmars/test_outputs.py` | `BIND S116 … by=url-task`, same route |
| Tier / status / used-by | `A` / `mined` / entry | `A` / `mined` / entry |

`sha256sum -c` of the whole capture set is five `OK` lines. `python3 plans/anchor_digest_check.py --lane . --verbose`
prints `rows=109 tokens=17 defects=0` and names S115/S116 as above. File lengths match the stated ranges
(`test_outputs.py` 85 lines, `instruction.md` 9 lines).

Quote-selection checks: the S115 quote is the only assertion on the `Results:` line and supports the scope cell's
"executed scoring predicate"; the S116 quote is the maintainers' verification sentence and is the line the entry's
requirement map anchors `debugger-works` on — both appropriate, neither over 25 words.

## 2. Drift

**terminal-bench-2 `main` has not moved.** `commits/main` = `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (the pin is
HEAD). Six files fetched at `main` are byte-equal to the pin: `tests/test_outputs.py`, `instruction.md`,
`tests/test.sh`, `task.toml`, `solution/solve.sh`, `environment/Dockerfile` — the last two are outside the capture set,
so the pin's "upstream `main` byte-equal" claim is stronger than it needed to be, not weaker.

**terminal-bench-2-1 `tasks/build-pmars` @ `7131e4375048a0e408a8fb404b5f499d726b695b` (its HEAD, 2026-08-11;
the task's only change there is `5fc7d3b9` "Move dataset files under tasks", 2026-05-05):**

| File | Digest @ TB2.1 HEAD | vs pin |
|---|---|---|
| `tests/test_outputs.py` | `d9d2796d…01f4e85` | **SAME** (grader untouched) |
| `tests/test.sh` | `4770437e…6e6c334` | SAME |
| `task.toml` | `7ee2eac2…4e4c9cd` | SAME |
| `environment/Dockerfile` | `ff0a9f76…6fe08b25` | SAME |
| `instruction.md` | `dd4a3aa7…d0082215e` | **DIFFERS**, line 3 only |
| `solution/solve.sh` | `111b4e53…5e5fadc713f` | **DIFFERS**, apt version pins dropped |

The instruction delta is one sentence inside line 3 (the shared prefix "Since koth.org is unreliable, get the source
from Debian packages instead." is unchanged; the changed span shown):

```
< Extract the source to `/app` and build without X11 support.
> Extract the source to `/app/pmars-<version>/` and build from there without X11 support. Leave the source tree in place.
```

The solve.sh delta is `build-essential=12.12`/`dpkg-dev=1.22.21`/… → unpinned (the fix for issue #59's
`Version '1.22.21' for 'dpkg-dev' was not found`). The entry's prior-art bullet ("Upstream changed the instruction, not
the grader") is confirmed word for word — see F38R-3 for its unpinned form.

## 3. F38R-1 (defect, not fatal) — nothing checks a SOURCES row's quote

Attacks: the registry row is the provenance surface; a quote there is data no counter reads.

In a clone at the tip, replacing S115's anchor quote with
`:46 “FORGED QUOTE THAT IS NOT IN THE FILE AT ALL AND NEVER WILL BE (7 words)” (7 words)` while leaving the digest
token untouched leaves **every** structural clause green:

```
-- V3 after forging the S115 row quote:      (True, 'rows=2 bad=0')
P3 ok rows=28 distinct_quotes=28 distinct_lines=27 out_of_word_range=0
P4 ok checked=28 bad=0 first=0
P6 ok rows=2 bad=0 first=0
```

(`P2 DEFECT receipt_sha256=…` appears in both runs because the committed spec leaves `receipt_sha256: None` and the
counter fills it in a temp spec, so a bare gate run always prints that line — it is an instrument of my run, not a
reaction to the forgery.) The mirror proves the two copies have different standing: forging
the **entry's** copy of the same string (`re.match` → `re.fullmatch` at `test_outputs.py:46`) reds immediately —
`P4 DEFECT checked=28 bad=1 first=test_outputs.py:46: quote not verbatim there`.

Mechanism: `pkg_gate.py c_sources` reads cells 1 (URL), 3 (tier), 6 (teaches), 7 (status), 10 (used-by) — never cell 5's
quoted text; `round38_c2_verify.py v3` reads only `re.findall(r"sha256\s+([0-9a-fA-F]+)", root[5])`; `P3`/`P4` parse
only `## Located quotes`. So a row's quote is checked *transitively* and only while it happens to duplicate the entry's
table text — today both do, which is why the rows verify, not because anything enforces them.

Smallest safe correction (round-scoped, no predicate change): extend `v3()` to also parse the anchor cell's
`“…”` span and require `capture.read_text().splitlines()[L-1].strip() == quote` for the cited `:<L>`. `v3` sees only
`spec["rows"]` = {S115, S116} (`rows=2`), both pass today, so `checks=7 defects=0` is unaffected. A general gate clause
would need its own opt-in key: folding row quotes into `P3` would move the quote counts the round-35/36/37 packages are
already admitted on.

## 4. F38R-2 (defect, freshness) — the documented recheck command reds on a healthy tree

The entry's own recheck line is: "re-fetch the two pinned URLs, run `sha256sum -c
corpus/evidence/round38/tb2-build-pmars/SHA256SUMS`, …". Run from the lane root as written:

```
sha256sum: instruction.md: No such file or directory (os error 2)
test_outputs.py: FAILED open or read
sha256sum: WARNING: 5 listed file(s) could not be read
round38 exit=1
```

The manifest lists bare basenames, so `-c` resolves them against the CWD. A 180-day follower sees a red recheck on an
intact capture and can report a digest change that did not happen. The template is lane-wide, not round-38-specific:
`round37 exit=1` for `corpus/evidence/round37/tb2-git-webserver/SHA256SUMS` (6 files unreadable), and the same phrasing
sits in the round-35 and round-36 TB2 entries. Correction: `(cd corpus/evidence/round38/tb2-build-pmars && sha256sum -c
SHA256SUMS)`, and route the four-entry wording as a round-39 item (or a lesson row) rather than editing four admitted
entries in a falsify wave. The recheck's other two legs are sound: `plans/build_pmars_probe.py` accepts `--lane`
(`:280`) and is at its frozen digest `32f0771c…25c24a`, matching `plans/pkg-spec-r38.json`.

## 5. F38R-3 (precision, freshness) — the TB2.1 comparison is unpinned

The entry asserts "its `tests/test_outputs.py` is byte-equal to S115" and that the instruction and solve.sh are revised,
against a moving branch. It is true today at TB2.1 HEAD `7131e437`, but a recheck can only re-derive it by re-diffing.
Correction: write the ref and the four digests into the same bullet (`7131e437`; grader `d9d2796d…`, instruction
`dd4a3aa7…`, solve.sh `111b4e53…`, Dockerfile `ff0a9f76…`). Cheap, and it converts a diff against `main` into a digest
compare. Note the byte-equality is grader-only: TB2.1's *requirement text* is no longer the text the map is drawn
against, so no map label transfers to TB2.1 unread.

## 6. F38R-4 (precision only) — the `pmars-dir-elsewhere` contest is a TB2.0-text artifact

The entry's contestable-tag note says the case "shows grader **strictness** … more than a violated requirement". Under
the pinned TB2.0 text ("Extract the source to `/app`") a tree at `/app/src/pmars-0.9.4` is compliant, so the contest is
real *for that wording*; upstream then resolved it the other way — PR #38 (open, 2026-02-13) "Made instructions
explicit that source should be extracted to `/app/pmars-<version>/`", shipped in TB2.1 with the grader unchanged. So
the depth-one glob is the authors' intended requirement, and only TB2.0's instruction under-specifies it. No label
moves either way — recomputing V7's rule from the receipt, `extract-to-app` has 22 violators (7 pass, 15 fail) →
`partly`, so dropping the case cannot flip it. Correction: one clause ("contest holds for the TB2.0 wording only; the
TB2.1 instruction was revised to match this glob").

The same recomputation reproduces every map label independently: `from-source`, `debian-source`, `extract-to-app`,
`debugger-works` 22/7/15 → partly; `no-x11` 3/1/2; `install-path` 4/1/3; `results-format` 5/1/4 — all `partly`, matching
the entry's seven labels.

## 7. Attacked and cleared (no finding)

- **Upstream citations are real.** `terminal-bench-2/issues/59` open, "`build-pmars` failing with oracle solution";
  `pulls/38` open, body "Opus now passes build-pmars with the more precise instructions on where/how to store source";
  `pulls/53` build-pmars files = exactly `build-pmars/instruction.md` + `build-pmars/solution/solve.sh` (grader absent
  from the diff, corroborating byte-equality); `terminal-bench/issues/631` closed, body line 19 exactly
  `| T2 | build-pmars | Instruction ambiguous on build destination | LLM rubric \`test_instruction_alignment\` | Soft only | Defer |`
  (my first fetch of #631 returned 404 transiently; the search API and the retry both resolve it).
- **Uncaptured line citations hold.** `task.toml:22`/`25` = `timeout_sec = 900.0` (verifier/agent), `:29` =
  `docker_image = "alexgshaw/build-pmars:20251031"`, `:34` = `allow_internet = true`. `environment/Dockerfile:9` =
  `COPY warriors/flashpaper.red warriors/rave.red /app/`, and both warrior files exist at
  `environment/warriors/` (`flashpaper.red` 1094 B, `rave.red` 784 B) — so the entry's "copies both warriors into
  `/app`" is accurate and the COPY is resolvable (build context is `environment/`).
- **Denominators.** 89 directories carry a `task.toml` at the pin (recursive tree API, `truncated=false`), so "4 of 89
  read" and "the other 85" are consistent.
- **Capture completeness.** `SHA256SUMS` = 5 files and all five match the pin; `solve.sh` is byte-identical to
  `build-pmars/solution/solve.sh` at the pin (the capture keeps the oracle at its root, which the entry states).

## 8. Axes and limits

Axes touched: **freshness** (drift re-derived and anchored; the recheck recipe is broken → F38R-2, F38R-3),
**depth** (row-quote authority is a named hole with a one-clause fix → F38R-1), **coverage** (unchanged: the entry's
reading surface is intact), **operability** (a follower's recheck is false-red today), **calibration** (unchanged; C1 and
N21 are outside this seat's item and untouched here), **adjacency/novelty** (unchanged; TB2.1 gives the map a second
text, not a second finding).

Limits: I verified quotes and digests, not the 21 C1 kills, the probe re-execution, or the V1–V7 predicate end to end —
other seats own those, and I ran only the gate's package checks without `--rerun`. The TB2.1 comparison uses its HEAD
`7131e437` because build-pmars last changed at `5fc7d3b9`; if TB2.1 later edits `tasks/build-pmars`, the digests above,
not `main`, are the anchor. GitHub REST was called unauthenticated; #631 returned one transient 404 before resolving.

VERDICT: rows-2/2-quotes-2/2
