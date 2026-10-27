# R45PkgGateDry — package-gate dry run against a mirror (round 45, wave 1)

Seat `R45PkgGateDry`, executor, leaf. Lane `kengaku-shokunin`. Wrote only this report + `./` receipts.
Scratch `S=/fast/scratch/hyaku/kengaku-r45/R45PkgGateDry` (removed at the end).

**Question.** Run `plans/pkg_gate.py package --root <mirror> --spec plans/pkg-spec-r45.json --rerun
--require-clean-tree` against a mirror holding only *drafts* — a stub entry carrying the frozen structure plus the
SOURCES rows / README row+bullet a scribe would write from the spec — and enumerate exactly what P1–P10 demand
**beyond** those drafts, so the wave's scribes hit each requirement once.

**Answer.** The drafts already satisfy P1, P6, P7 and P8 (spec-derived rows, source lines, `verified-at`,
`recheck`, `## Negative space`, README index row + bullet). Beyond them the gate demands **35 atomic facts**, of
which five are the ones a structure-only draft cannot imply:

1. **P2** — the receipt digest must be *pinned and equal*; `null` is not "unchecked", it is a guaranteed defect.
2. **P3/P4** — ≥10 distinct **verbatim** quotes, 3–25 words each, at ≥10 distinct `capture:start` locations.
3. **P5** — the capture manifest's names must equal the spec's `rows[*].capture` names (a basename under
   `capture_dir`, not the upstream path).
4. **P9** — the worktree must be clean, and that includes the wave's own `.ufo/waves/round-45/**` reports.
5. **P10** — the receipt must be byte-equal to the probe's **stdout alone**: an `ENVELOPE`-wrapped receipt
   fails even though the probe output inside it is identical.

---

## 1. Method

1. Read `plans/round-45-claims.md`, `plans/pkg-spec-r45.json` and `plans/pkg_gate.py` (398 lines) in full.
2. Built three scratch mirrors, each an independent git repo whose `git rev-parse --show-toplevel` is itself:
   * **mirror** — lane `HEAD` `05b02e2` (the freeze-time committed state) + stub entry + spec-derived rows. The
     "before the entry exists" state this seat was asked to test.
   * **mirror2** — mirror + the three fixes the first run implied (spec `capture` → upstream names, receipt →
     bare probe stdout, entry → 14 verbatim quotes). Used to isolate each clause.
   * **mirror3** — the live lane working tree with `.ufo/waves/round-45/` removed and everything committed.
     Shows the gate can reach `defects=0`.
3. Ran **44 mutation probes** (`battery2.txt`, 39; `battery3.txt`, 5) against the green mirror3, plus four
   one-off isolations (`probe-p2c`, `probe-p4c`, `probe-p3sec`, `gate-p9`). Each probe assigns the gate the
   **probe copy's own** `--spec`, so spec mutations are visible — v1 of the battery always passed the lane spec
   and was silently blind to every spec mutation.
4. Every gate/probe run went through `claims/envelope.sh "$S/envN" …`. All ENVELOPE digests report
   `unchanged` — no measurement below is invalidated.

---

## 2. The five framing runs (full gate output)

### 2.1 Drafts only, from the freeze-time tree → `defects=5`

`gate-pass1.txt`:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind …/env1 … --unshare-pid --die-with-parent -- python3 plans/pkg_gate.py package --root …/mirror --spec /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/pkg-spec-r45.json --require-clean-tree
ENVELOPE start 23:36:36 cwd=…/mirror
P1 ok pinned=2 mismatched=0
P2 DEFECT receipt_sha256=587c8b345f8b0341e90640f83b78eafa7c5d5c996cac5e2d0a52a1131a8df23e
P3 DEFECT rows=0 distinct_quotes=0 distinct_lines=0 out_of_word_range=0
P4 DEFECT no parsed quote
P5 DEFECT manifest_entries=9 bad=5 first=S149: capture test_outputs.py is not pinned in the manifest
P6 ok rows=8 bad=0 first=0
P7 ok source_lines=8 bad=0 first=0
P8 ok index_rows=52 knowledge_files=52 bad=0 first=0
P9 DEFECT untracked=1 first=corpus/knowledge/tb2-password-recovery-grader.md
defects=5
ENVELOPE end 23:36:38 exit=1 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

### 2.2 Same drafts, `--rerun` added → P10 is a sixth, independent demand

`gate-pass2.txt` adds only `P10 DEFECT fresh probe output is not byte-equal to the receipt` (`defects=6`,
ENVELOPE `23:37:37 → 23:37:42 … unchanged`). Cause measured, not inferred — fresh probe stdout vs the committed
receipt differed in exactly the wrapper lines:

```
$ diff <(python3 plans/password_recovery_probe.py --lane . ) corpus/evidence/round45/password-recovery-probe.txt
1,2c1,2
< ENVELOPE /usr/bin/bwrap … --bind …/env2 … -- python3 plans/password_recovery_probe.py --lane . --work …/env2/w-probe
< ENVELOPE start 23:37:01 cwd=…/mirror
---
> ENVELOPE /usr/bin/bwrap … --bind /fast/scratch/hyaku/kengaku-r45/L1/run … -- python3 plans/password_recovery_probe.py --lane . --work …/L1/w-probe
> ENVELOPE start 23:27:11 cwd=/home/vgpnk/Projects/shokunin/kengaku-shokunin
26c26
< ENVELOPE end 23:37:05 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
---
> ENVELOPE end 23:27:15 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

The 23 payload lines are byte-identical. The committed receipt at `05b02e2` carried three `ENVELOPE` lines
(`grep -c ENVELOPE` = 3); round 44's receipt has 0. **P10 is "the receipt is the probe's stdout, nothing else".**

### 2.3 Candidate fixes applied → `defects=2`, each residual self-naming

`gate-pass3.txt` (mirror2, effective spec, 14 quotes; ENVELOPE `23:40:58 → 23:41:03 … unchanged`):

```
P1 DEFECT pinned=2 mismatched=['plans/password_recovery_probe.py']
P2 ok receipt_sha256=pinned
P3 DEFECT rows=14 distinct_quotes=14 distinct_lines=14 out_of_word_range=1
P4 ok checked=14 bad=0 first=0
P5 ok manifest_entries=9 bad=0 first=0
P6 ok rows=8 bad=0 first=0
P7 ok source_lines=8 bad=0 first=0
P8 ok index_rows=52 knowledge_files=52 bad=0 first=0
P9 ok untracked=0 first=0
P10 ok probe_rerun=byte-equal bytes=4659
defects=2
```

P1 was stale by then — the L1 had re-pinned the probe mid-wave (`f87a9ee…` → `9363e03e…`). P3's single
`out_of_word_range` row was my own `PASSWORD_LENGTH=23` quote at **1 word** (floor 3), not a gate quirk.

### 2.4 Live lane tree before its wave artifacts were committed → only P9

`gate-live.txt` (`--root` = the real lane; ENVELOPE `23:41:27 → 23:41:32 … unchanged`):
P1–P8 **and P10** `ok`; `P9 DEFECT untracked=159 first=.ufo/waves/round-45/make_wave2_spec.py`; `defects=1`.
Composition of the untracked set (measured at 23:43, by then grown to 164 as more seats wrote): 161 files under
`.ufo/waves/round-45/w1/` plus `make_wave2_spec.py`, `w1.ready.dispatched`, `w2-spec.json` — the wave's own
bookkeeping, not package files.

### 2.5 Clean states → `defects=0`

`gate-live2.txt` (after the artifacts were committed; ENVELOPE `23:44:28 → 23:44:32 … unchanged`) and
`gate-mirror3.txt` (ENVELOPE `23:42:11 → 23:42:16 … unchanged`) are identical:

```
P1 ok pinned=2 mismatched=0
P2 ok receipt_sha256=pinned
P3 ok rows=19 distinct_quotes=19 distinct_lines=19 out_of_word_range=0
P4 ok checked=19 bad=0 first=0
P5 ok manifest_entries=9 bad=0 first=0
P6 ok rows=8 bad=0 first=0
P7 ok source_lines=8 bad=0 first=0
P8 ok index_rows=52 knowledge_files=52 bad=0 first=0
P9 ok untracked=0 first=0
P10 ok probe_rerun=byte-equal bytes=4659
defects=0
```

The gate is reachable. The ledger below is everything that stands between the drafts and that line.

---

## 3. The demand ledger — 35 atomic demands, keyed to the spec

`spec` = `plans/pkg-spec-r45.json`. "probe X" = the mutation in `battery2.txt` / `battery3.txt` that isolates it;
"source" = read from `plans/pkg_gate.py` at the cited line.

### P1 `c_instruments` (`pkg_gate.py:112-115`) — 1 demand
| # | demand | evidence |
|---|---|---|
| 1 | every `frozen_instruments` path under the root hashes to its pin — **and the pin is current** | probe `p1`: append one comment to `plans/password_recovery_probe.py` → `P1 DEFECT pinned=2 mismatched=['plans/password_recovery_probe.py']` |

### P2 `c_receipt` (`pkg_gate.py:117-121`) — 2 demands
| # | demand | evidence |
|---|---|---|
| 2 | `spec.receipt` must be readable | probe `p2c` (delete the receipt) → `P2 DEFECT receipt unreadable: corpus/evidence/round45/password-recovery-probe.txt` |
| 3 | `spec.receipt_sha256` must equal the receipt's bytes — **`null` is a guaranteed defect**, not a skip | probe `p2` (`0`*64) → `P2 DEFECT receipt_sha256=cf74f451…`; probe `p2b` (`null`) → identical `P2 DEFECT receipt_sha256=cf74f451…` |

### P3 `c_quote_shape` (`pkg_gate.py:123-136`) — 6 demands
| # | demand | evidence |
|---|---|---|
| 4 | a `## Located quotes` section | probe `p3sec` (rename the heading) → `P3 DEFECT no '## Located quotes' section` |
| 5 | every table row parses as `\| claim \| “text” \| \`cap:line\` \|` (curly quotes **and** backticked location) | probes `p3d` (extra cell) → `unparsed_rows=1`; `p3e` (no curly quotes) → `unparsed_rows=1`; `p3f` (no backticks) → `unparsed_rows=1` |
| 6 | ≥ `min_quotes` = 10 distinct quote texts | probe `p3floor` (9 rows) → `P3 DEFECT rows=9 distinct_quotes=9` |
| 7 | ≥ `min_distinct_locations` = 10 distinct `(capture, start)` pairs | probe `p3loc` (8 rows re-pointed at one location) → `distinct_lines` fell 19→11 |
| 8 | each quote within `quote_words` [3, 25] | probe `p3c` (1-word quote) → `out_of_word_range=1` |
| 9 | row 0 is consumed as the header — 10 quotes need 11 rows | source `:85` (`rows[1:]`) |

### P4 `c_quote_verbatim` (`pkg_gate.py:138-150`) — 3 demands
| # | demand | evidence |
|---|---|---|
| 10 | the capture resolves under `capture_dir` (relative, no `..`, readable) | probe `p4c` (capture renamed `nonexistent.md`) → `P4 DEFECT … nonexistent.md: unreadable capture` |
| 11 | the cited range lies inside the capture | probe `p4b` (`:999`) → `line range outside the capture` |
| 12 | the quote text appears verbatim in the joined `start..end` lines | probe `p4` (append `X`) → `quote not verbatim there` |

### P5 `c_captures` (`pkg_gate.py:152-182`) — 5 demands
| # | demand | evidence |
|---|---|---|
| 13 | `capture_dir/SHA256SUMS` exists and every line parses as `<64hex>  <name>` | probe `p5f` (a junk line) → `unparsed manifest line 'not-a-manifest-line'` |
| 14 | every listed file's bytes match its digest | probe `p5g` (tamper `test_outputs.py`) → `manifest digest does not match the bytes` |
| 15 | **every spec row's `capture` name is a manifest key with the row's digest** | probe `p5a`/`p5b`/`p5c` (drop `task.toml` / `README.md` / `setup.sh`) → `S156: capture task.toml is not pinned in the manifest`, etc. |
| 16 | every quote's capture is a manifest key | probe `p4c` also → `P5 DEFECT … quote capture nonexistent.md is not pinned in the manifest` |
| 17 | no non-dot top-level file in `capture_dir` outside the manifest | probe `p5e` (add `extra-capture.md`) → `capture file not covered by the manifest`; probe `p5d` (drop the `gitignore` line) → same message for `gitignore` |

### P6 `c_sources` (`pkg_gate.py:184-209`) — 7 demands
| # | demand | evidence |
|---|---|---|
| 18 | exactly one row per spec id | probe `p6e` (delete S152) → `S152: rows=0` |
| 19 | exactly 11 cells | probe `p6h` (10 cells) → `S149: cells=10` |
| 20 | `cells[1]` carries `raw_base + upstream` **verbatim** | probe `p6b` → `S149: url not the pinned raw path` |
| 21 | `cells[3]` = `row_tier` (`A`) | probe `p6a` (`B`) → `S149: tier='B'` |
| 22 | `cells[7]` = `row_status` (`mined`) | probe `p6g` (`queued`) → `S149: status='queued'` |
| 23 | `cells[10]` contains the entry path | probe `p6f` → `S149: used-by is not the entry` |
| 24 | `cells[6]` ≥ `min_teaches_words` (8) **and pairwise distinct across rows** | probe `p6c` → `S149: teaches words=2`; probe `p6d` → `teaches cells are not pairwise distinct` |

### P7 `c_provenance` (`pkg_gate.py:211-231`) — 5 demands
| # | demand | evidence |
|---|---|---|
| 25 | one `source: S<id> … <raw_base+upstream>` line per id (a second line for the same id fails: the value becomes a 2-element list) | probe `p7f` (delete S152's) → `S152: source line absent`; probe `p7d` (append `?x=1`) → `S149: source line not the pinned url` |
| 26 | `verified-at: 2026-10-26` | probe `p7a` → `verified-at line absent or not the frozen date` |
| 27 | a line matching `^recheck:\s*\S` | probe `p7b` → `recheck line absent` |
| 28 | a `## Negative space` section | probe `p7c` (renamed) → `no '## Negative space' section` |
| 29 | that section contains `falsifi(er\|ed\|es\|ability)` | probe `p7e` (token replaced) → `'## Negative space' carries no falsifier` |

### P8 `c_readme` (`pkg_gate.py:233-257`) — 4 demands
| # | demand | evidence |
|---|---|---|
| 30 | exactly one `\| \`knowledge/<entry>.md\` \|` index row | probe `p8a` (removed) → `index rows for knowledge/tb2-password-recovery-grader.md=0` |
| 31 | that row cites **every** registry id | probe `p8b` (`S149, ` stripped) → `index row does not cite every registry row` |
| 32 | a `- ` coverage bullet naming the entry **and** `receipt` minus its first segment (`evidence/round45/password-recovery-probe.txt`) | probe `p8c` → `no coverage bullet naming the entry and its receipt` |
| 33 | the `corpus/knowledge/*.md` set equals the indexed set | probe `p8d` (extra file) → `knowledge files=53 index rows=52` |

### P9 `c_clean_tree` (`pkg_gate.py:259-265`, only with `--require-clean-tree`) — 1 demand
| # | demand | evidence |
|---|---|---|
| 34 | `git ls-files --others --exclude-standard` in the **root** is empty | `gate-p9.txt`: one uncommitted root file → `P9 DEFECT untracked=1 first=stray-note.md`; live lane mid-wave → `untracked=159`, all `.ufo/waves/round-45/**` |

### P10 `c_rerun` (`pkg_gate.py:267-285`, only with `--rerun`) — 1 demand
| # | demand | evidence |
|---|---|---|
| 35 | the receipt equals a fresh probe run's **stdout** byte for byte (no wrapper, no timestamp, no host path) | probes `p10` (payload edited, spec re-pinned so P2 stays ok) and `p10b` (one `ENVELOPE` line prepended, spec re-pinned) → `P10 DEFECT fresh probe output is not byte-equal to the receipt`, `P2 ok`; §2.2 shows the wrapped-receipt origin |

---

## 4. Two ordering traps the wave must not hit

1. **P2 with `receipt_sha256: null` cannot pass.** `c_receipt` computes `got == want`; a hex digest never
   equals `None`, so a gate run that consumes the frozen spec file *always* prints
   `P2 DEFECT receipt_sha256=<true digest>` (probe `p2b`). The C2 counter avoids this by writing an
   **effective** spec with the digest filled in (`round45_c2_verify.py:154-155`, then `--spec <work>/pkg-spec-r45-effective.json` at `:158`).
   A direct `pkg_gate.py … --spec plans/pkg-spec-r45.json` invocation does not. **A scribe cannot fix this;
   the L1 must (pin the digest in the spec, or always gate through the counter's effective spec).**
2. **P9 counts wave bookkeeping.** Seat reports live under `.ufo/waves/round-45/w1/`, which `.gitignore`
   (`.ufo/interactive-sessions/` only) does not exclude, so a gate run against the lane root sees every
   uncommitted report as `untracked`. Measured: `untracked=159` mid-wave vs `untracked=0` after the artifacts
   landed. **Landing order: commit the wave artifacts, then gate — or gate a clean clone/mirror** (mirror3
   recipe: `tar` the lane minus `.git`, drop `.ufo/waves/round-45/`, `git init` + one commit).

## 5. Findings beyond the enumeration

### 5.1 The capture-dir naming was the one real freeze defect
At `05b02e2` the capture directory held the **upstream layout** and `SHA256SUMS` listed path-qualified names,
while the frozen spec's `rows[*].capture` names are **flat basenames**:

```
$ git show HEAD:corpus/evidence/round45/tb2-password-recovery/SHA256SUMS
6fabcb9e…  environment/Dockerfile
9fdde5d9…  environment/setup.sh
c5f9fc70…  solution/solve.sh
2dc14fc1…  tests/test_outputs.py
$ python3 -c '…spec rows…'
{'S149': 'test_outputs.py', 'S151': 'setup.sh', 'S152': 'Dockerfile', 'S153': 'test.sh', 'S155': 'solve.sh', …}
```

`c_captures` looks `row["capture"]` up in the manifest, so exactly the five rows whose `upstream` has a
directory component failed (`P5 … bad=5`). `capture` is a **basename under `capture_dir`**; `upstream` is the
path used in the URL. Two coherent fixes — flatten the capture tree + `SHA256SUMS` (all nine digests unchanged)
and re-point the probe's read paths, or set `capture` to the path-qualified names. The L1 took the first mid-wave and recorded
it as freeze amendment (1) in `plans/round-45-claims.md` ("captured in upstream directory layout but the spec row
`capture` fields name flat basenames — the tree was flattened to the r44 convention (`SHA256SUMS` rewritten, all
9 digests unchanged)"); `gate-pass1.txt` plus the `git show` above are the measured defect.

### 5.2 P10 forces the receipt to be a bare capture
The round-45 receipt was first captured by redirecting the envelope's stdout, which prepends `ENVELOPE …` and
appends `ENVELOPE end …`. Round 44's receipt has `grep -c ENVELOPE` = 0. Rule for the scribe: run the probe under
the envelope (host safety), but write **only the probe's stdout** into the receipt; the ENVELOPE lines belong in
the report (QUALITY Q32), never in the receipt.

### 5.3 Exit codes and fail-closed behaviour
`0` accept, `1` reject, `2` setup/usage. `run_checks` maps an exception inside a clause to `DEFECT`
("a clause that cannot run is a defect, never a pass"), so a malformed entry fails closed. `P9`/`P10` run only
when `--require-clean-tree`/`--rerun` are given (`cmd_package` filters `PACKAGE_CHECKS`, `:305-310`).

### 5.4 The gate reads less than the counter — passing it is necessary, not sufficient
`c_sources` never reads `cells[8]` (`opened`) or `cells[9]` (recheck cadence); the census tool enforces those
(E08/E09). And the gate never parses `## Case table`, `## Mechanism`, `## Requirement map` or `## Predictor` —
those are C2-counter demands (`round45_c2_verify.py` V7/V9/V10/V11). A package can be gate-green and
counter-red.

### 5.5 P10's runtime dependency
`Bio` is not importable on host `python3`, so `c_rerun` falls back to
`uv run --no-project --with biopython==1.85 python3 …`. Verified inside the envelope:
`Downloaded biopython (3.1MiB) … Installed 2 packages in 127ms … bio ok 1.85`. **An offline gate run would
fail P10** with `probe could not be re-run`. The probe itself imports only `pathlib`; the `Bio` probe is the
gate's proxy for "host python is usable".

## 6. Risks / blockers for the L1

- **P2** — pin `receipt_sha256` (or always gate through the counter's effective spec). The frozen `null` is a
  guaranteed defect on any direct invocation.
- **P9** — commit the `.ufo/waves/round-45/**` artifacts before the `--require-clean-tree` run, or gate a
  clean clone. Each new seat report re-dirties the tree.
- **P10** — the receipt must be bare stdout; a receipt captured through the envelope fails.
- **P1** — pins move. The probe digest changed mid-wave (`f87a9ee…` → `9363e03e…`) and the spec was re-pinned to
  match; a gate run older than the re-pin reports `mismatched`.
- **P5** — `capture` is a basename, `upstream` is the URL path; mixing them fails 5 of 8 rows.
- **P10 network** — the `biopython==1.85` fallback needs PyPI once per uv cache.

## 7. Receipts (in `./`)

| file | bytes | sha256 |
|---|---|---|
| `gate-pass1.txt` | 1238 | `276b293feac6cf9bfe90d91517a3f7d88f5276a2fddf93cae9857df691426dbf` |
| `gate-pass2.txt` | 1309 | `40bf382d4639d0026114265a5b770c2db84131f4f421283b3d57267624057235` |
| `gate-pass3.txt` | 1164 | `60cda44c704d23a16167d2fc30a7a2b71af50df2c97b9bbe64b1093168febc7f` |
| `gate-live.txt` | 1193 | `9f3ae3864a5e45aee35fc8c1567133320c34915a699bfdc5ae92c1c624227c8f` |
| `gate-live2.txt` | 1153 | `96ed9c5bb5a2dcd65b289f3303953ccb14a645f617c4ff5dc6ab9d3aca710393` |
| `gate-mirror3.txt` | 1157 | `df3f13cd4d2bdc8bc03379af37ca8e24ad2ab178092744d39763de93c2ae436c` |
| `gate-p9.txt` | 1124 | `fbff6930fc7a3fb2f33135653bee890d8739a8fe52af59592f5f6193ae0de32a` |
| `battery2.txt` | 15285 | `34622749f064727e16f8521be0732e65bc9c18e736e770ca456598de59186ea6` |
| `battery3.txt` | 1946 | `c03ec229fd4d9453a614894f4686162081d0e3cf8f8fd363f4583b7df5d5d3e9` |
| `probe-p2c.txt` | 398 | `ab63c6044443b1807831cef30c6cae240b522d32458958fb5cb2884011538eda` |
| `probe-p3sec.txt` | 1022 | `c44d18bcc874081cf3d94ef190b28cf0c2d96143e0aa458b50cf5dd2cdc99b9b` |
| `probe-p4c.txt` | 442 | `a204132245672e2f10a000923cab1f05ba4ae8f32d4f88196436d094d02e6ab6` |

ENVELOPE lines for the battery and P9/probe runs are embedded at the head of `battery2.txt`, `battery3.txt`,
`gate-p9.txt` and `probe-p3sec.txt`; every one reports `unchanged`. Tooling: **nothing installed or upgraded**,
no PATH directory touched.

VERDICT: gate-demands-enumerated-35
