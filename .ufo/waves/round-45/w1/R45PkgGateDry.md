# R45PkgGateDry — package-gate dry run against a mirror (round 45, wave 1)

Seat: `R45PkgGateDry`, executor, leaf. Lane repo `kengaku-shokunin`, no lane write except this report + subdir.
Scratch `S=/fast/scratch/hyaku/kengaku-r45/R45PkgGateDry` (deleted at the end).

**Question this seat answers:** run `plans/pkg_gate.py package --root <mirror> --spec plans/pkg-spec-r45.json
--rerun --require-clean-tree` against a mirror that holds only *drafts* (a stub entry carrying the frozen
structure, plus the SOURCES rows / README row+bullet a scribe would write from the spec), and enumerate exactly
what P1–P10 demand **beyond** those drafts — so the wave's scribes hit each requirement once.

**Answer in one line:** beyond the drafts the gate demands five content/freeze facts the drafts cannot imply —
a **pinned receipt digest** (P2), **≥10 verbatim located quotes** (P3/P4), a **manifest whose names equal the
spec's `capture` names** (P5), a **bare-stdout receipt** (P10), and a **clean worktree including the wave's own
report files** (P9). Everything else (P1, P6, P7, P8) the drafts already satisfy when written from the spec.

---

## 1. Method

1. Read the frozen claims (`plans/round-45-claims.md`), the frozen spec (`plans/pkg-spec-r45.json`) and the
   frozen gate (`plans/pkg_gate.py`, 398 lines) in full.
2. Built three mirrors in scratch, each a git repo whose `rev-parse --show-toplevel` is itself:
   * **mirror** = lane `HEAD` (`05b02e2`, the committed state at the freeze moment) + a stub entry + rows drafted
     from the spec only. This is the "before the entry exists" state the seat was asked to test.
   * **mirror2** = mirror + the three candidate fixes the first run implied (spec `capture` names → upstream
     values, receipt → bare probe stdout, entry → 14 real quotes). Used to isolate each clause.
   * **mirror3** = the live lane working tree with the wave's `.ufo/waves/round-45/` artifacts removed and
     everything committed. Used to show the gate can reach `defects=0`.
3. Ran a **37-probe mutation battery** (one mutation per clause) to record what each clause actually reads, not
   what its name suggests.
4. Every gate/probe run went through `claims/envelope.sh "$S/envN" …` (home read-only, `~/.cache` overlaid from
   scratch, `~/.local/bin` content digest before/after). Every ENVELOPE line is pasted with its result below;
   **no run reported `CHANGED`**, so no measurement is invalid.

Files quoted here live in `./` next to this report (`gate-pass1.txt` … `gate-mirror3.txt`, `battery2.txt`).

---

## 2. The five runs that frame the enumeration

### 2.1 Drafts only, from the committed freeze state → `defects=5`

`gate-pass1.txt` (mirror = lane `HEAD` 05b02e2 + stub entry + spec-derived rows):

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

Reading: the **structure the spec describes** (8 source lines, 11-cell SOURCES rows, README index row +
coverage bullet, both instruments at their pins) already passes P1/P6/P7/P8. The five defects are the real work.

### 2.2 The same drafts with `--rerun` → `defects=6`: P10 is a sixth, independent demand

`gate-pass2.txt` adds only `P10 DEFECT fresh probe output is not byte-equal to the receipt` (exit 1,
ENVELOPE `23:37:37 → 23:37:42 … unchanged`).

I proved the cause directly rather than inferring it (`fresh-probe.txt` vs the committed receipt):

```
$ diff <fresh probe stdout> corpus/evidence/round45/password-recovery-probe.txt
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

The probe's own 23 payload lines are byte-identical; **the three `ENVELOPE` wrapper lines are the whole
difference**. So P10 is not "re-run the probe and check the science" — it is "the receipt file must be exactly
the probe's stdout, with no host-safety wrapper captured into it". The committed receipt at freeze commit
`05b02e2` carried the wrapper (`grep -c ENVELOPE` = 3), so P10 could not pass until the receipt was re-captured
bare.

### 2.3 The three candidate fixes applied → `defects=2`, and each residual names its own cause

`gate-pass3.txt` (mirror2, effective spec, 14 quotes):

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
(ENVELOPE `23:40:58 → 23:41:03 … unchanged`.) P1 was already stale by the time it ran — the L1 had re-pinned
the probe mid-run (`f87a9ee…` → `9363e03e…`, see §4.1); P3's one out-of-range row was my own `PASSWORD_LENGTH=23`
quote at **1 word** (floor is 3), not a gate quirk.

### 2.4 Live lane tree, before its wave artifacts were committed → only P9

`gate-live.txt` (`--root` = the real lane, `23:41:27 → 23:41:32 … unchanged`): P1–P8 **and P10** all `ok`;
`P9 DEFECT untracked=159 first=.ufo/waves/round-45/make_wave2_spec.py`, `defects=1`.

### 2.5 Live lane tree after the artifacts were committed, and the clean mirror3 → `defects=0`

`gate-live2.txt` (`23:44:28 → 23:44:32 … unchanged`) and `gate-mirror3.txt` (`23:42:11 → 23:42:16 …
unchanged`) are both:

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

So the gate is reachable; the enumeration below is what stands between the drafts and that line.

---

## 3. Checklist keyed to the spec — what each clause demands beyond the drafts

`spec` = `plans/pkg-spec-r45.json`. Column "beyond the drafts" = the fact a scribe must supply that a
structure-only stub and spec-derived rows cannot.

| # | clause (gate fn) | spec fields it reads | demand beyond the drafts | first-run evidence |
|---|---|---|---|---|
| **P1** | `c_instruments` | `frozen_instruments` (2 pins) | every pinned rel path under the root must hash to its pin — **and the pin must be current**: the L1 re-pinned the probe mid-wave (`f87a9ee…`→`9363e03e…`), so any tree built before that re-pin reads `mismatched` | `P1 ok pinned=2` (pass1); `P1 DEFECT … mismatched=['plans/password_recovery_probe.py']` (pass3) |
| **P2** | `c_receipt` | `receipt`, `receipt_sha256` | **the digest must be pinned and must equal the receipt's bytes.** A `null` pin is not "unchecked": `got == None` is `False`, so `null` is a *guaranteed* defect that prints the true digest. The C2 counter works around this by writing an *effective* spec with the digest filled in (`round45_c2_verify.py:158`); a bare `pkg_gate.py … --spec plans/pkg-spec-r45.json` invocation does not | `P2 DEFECT receipt_sha256=587c8b34…` (pass1, spec pin was `null`) → `P2 ok receipt_sha256=pinned` (pass3/live) |
| **P3** | `c_quote_shape` | `entry_rules.min_quotes` (10), `min_distinct_locations` (10), `quote_words` [3,25] | a `## Located quotes` table whose **every** row matches `\| claim \| “text” \| \`capture:line\` \|` — curly quotes, backticked location, 3–25 words, ≥10 distinct texts, ≥10 distinct `(capture, start)` pairs. **Row 0 is consumed as the header**, so 10 quotes need 11 rows | `P3 DEFECT rows=0 …` (pass1); `P3 DEFECT … out_of_word_range=1` (pass3, 1-word quote) |
| **P4** | `c_quote_verbatim` | `capture_dir` + the quote's `capture` name | every quote must appear **verbatim** in the joined lines `start..end` of `capture_dir/<capture>`; the range must exist; the capture must be readable and path-safe | `P4 DEFECT no parsed quote` (pass1); `P4 ok checked=19` (live) |
| **P5** | `c_captures` | `capture_dir`, `rows[*].capture`, `rows[*].sha256` | `SHA256SUMS` must exist; every manifest line must parse; every named file must match; **every spec row's `capture` name must be a manifest key**; every quote's capture must be a manifest key; every non-dot top-level file in `capture_dir` must be listed | `P5 DEFECT manifest_entries=9 bad=5 first=S149: capture test_outputs.py is not pinned in the manifest` (pass1) |
| **P6** | `c_sources` | `rows[*].upstream/sha256`, `raw_base`, `entry_rules.row_tier/row_status/min_teaches_words` | exactly **one** 11-cell row per id in `corpus/SOURCES.md`; `cells[1]` must carry `raw_base + upstream` **verbatim**; `cells[3]`=tier, `cells[7]`=status, `cells[10]` must contain the entry path, `cells[6]` ≥8 words and pairwise distinct | `P6 ok rows=8` (pass1) — satisfied by spec-derived rows |
| **P7** | `c_provenance` | `rows`, `raw_base`, `entry_rules.verified_at` | one `source: S<id> … <raw_base+upstream>` line per id (a *second* line for the same id becomes a 2-element list and fails); `verified-at: 2026-10-26`; a `recheck:` line; a `## Negative space` section containing `falsifi(er\|ed\|es\|ability)` | `P7 ok source_lines=8` (pass1) |
| **P8** | `c_readme` | `entry`, `readme`, `receipt`, `rows` | exactly one `| \`knowledge/<entry>.md\` |` row **citing every registry id**; one `- ` coverage bullet naming the entry **and** `receipt` minus its first path segment (`evidence/round45/password-recovery-probe.txt`); the `knowledge/*.md` file set must equal the indexed set | `P8 ok index_rows=52 knowledge_files=52` (pass1) |
| **P9** | `c_clean_tree` | — (`--require-clean-tree`) | `git ls-files --others --exclude-standard` in the **root** must be empty — this counts the wave's own seat reports under `.ufo/waves/round-45/w1/`, not just package files | `P9 DEFECT untracked=1` (pass1, the stub entry); `P9 DEFECT untracked=159 first=.ufo/waves/round-45/make_wave2_spec.py` (gate-live) |
| **P10** | `c_rerun` | `receipt`, `probe_cmd` | the receipt must be **byte-equal to a fresh probe run's stdout** — no `ENVELOPE` wrapper, no timestamp, no host path. Runs `plans/password_recovery_probe.py --lane .` with `cwd = root`; uses `python3` when `Bio` imports, else `uv run --no-project --with biopython==1.85 python3` | `P10 DEFECT fresh probe output is not byte-equal to the receipt` (pass2) → `P10 ok probe_rerun=byte-equal bytes=4659` (live) |

### 3.1 Two clauses are traps for a wave that finishes in order

1. **P2 with `receipt_sha256: null`** — the freeze spec carried `null`. That is not "skip the check"; `c_receipt`
   compares `got == want`, and a hex digest never equals `None`, so a gate run that passes the frozen spec
   file *always* prints `P2 DEFECT receipt_sha256=<the true digest>`. Either the spec carries the digest, or the
   caller re-writes an effective spec exactly as `round45_c2_verify.py` does. **A scribe cannot fix this; the
   L1 must.**
2. **P9 counts wave bookkeeping.** Measured on the live lane mid-wave: `untracked=159`, all of them
   `.ufo/waves/round-45/**` (161 under `w1/`, plus `make_wave2_spec.py`, `w1.ready.dispatched`, `w2-spec.json`).
   A gate run against the lane root therefore fails P9 until those artifacts are committed — or the gate is run
   against a clean clone/mirror. **Landing order matters: commit, then gate.**

### 3.2 What the drafts already satisfy (do not spend scribe effort here)

Written straight from the spec, the SOURCES rows (11 cells, `raw_base+upstream` in cell 1, tier A, status
mined, ≥8 distinct teaches words, entry path in used-by), the eight `source:` lines, `verified-at:`,
`recheck:`, `## Negative space`, and the README index row + coverage bullet all pass on the first run
(`gate-pass1.txt`: `P1 ok, P6 ok, P7 ok, P8 ok`).

---

## 4. Mutation evidence — what each clause actually reads

`battery2.txt`: 37 probes, each = one fresh copy of the green mirror3, one mutation, then
`pkg_gate.py package --root <probe> --spec <probe>/plans/pkg-spec-r45.json` (the **probe's own** spec, so spec
mutations are visible). Envelope `23:42:50 → 23:44:27 exit=0 … unchanged` (v1) /
`… unchanged` (v2).

<!-- BATTERY_TABLE -->

## 5. Findings beyond the enumeration

### 5.1 The capture-dir naming is the one genuine freeze defect

At the freeze commit the capture directory was stored in **upstream layout** (`environment/Dockerfile`,
`tests/test_outputs.py`, `solution/solve.sh`, …) and `SHA256SUMS` listed those path-qualified names, while the
frozen spec's `rows[*].capture` names **flat basenames** (`Dockerfile`, `test_outputs.py`, `solve.sh`, …):

```
$ git show HEAD:corpus/evidence/round45/tb2-password-recovery/SHA256SUMS
6fabcb9e…  environment/Dockerfile
…
$ python3 -c "…spec rows…"   → {'S149': 'test_outputs.py', 'S152': 'Dockerfile', 'S155': 'solve.sh', …}
```

`c_captures` looks up `row["capture"]` in the manifest, so five of eight rows failed
(`S149, S151, S152, S153, S155` — exactly the rows whose `upstream` has a directory component). The spec's
`capture` field is a **basename under `capture_dir`**, not the upstream path; `upstream` is what P6/P7 put in
the URL. Two coherent resolutions, and the L1 took the first: flatten the capture tree + `SHA256SUMS` (all nine
digests unchanged) and re-point the probe's own read paths; or set `capture` to the path-qualified names.
**The digests never changed — only the names did.**

### 5.2 P10 requires a *bare* capture, so the envelope cannot be inside the receipt

The round-45 receipt was first captured by redirecting the envelope's stdout, which prepends/append three
`ENVELOPE` lines. Round-44's receipt has `grep -c ENVELOPE` = 0 and passes. The rule for the scribe: run the
probe under the envelope, but write **the probe's stdout only** into the receipt; paste the envelope lines in
the report (QUALITY Q32), never in the receipt.

### 5.3 The gate's own exit codes

`0` accept, `1` reject (≥1 defect), `2` setup/usage. `run_checks` maps an **exception inside a clause** to
`DEFECT` ("a clause that cannot run is a defect, never a pass"), so a malformed entry fails closed. `P9`/`P10`
are only evaluated when `--require-clean-tree`/`--rerun` are passed (`cmd_package` filters `PACKAGE_CHECKS`).

### 5.4 The gate does not read three things the counter does

`row_opened` (cells[8]) and the recheck cadence (cells[9]) are **not** checked by `c_sources` — the census tool
(`sources-census.sh validate`, E08/E09) is what enforces them. A row can pass the gate with a wrong `opened`
date. Likewise the gate never reads `## Case table` / `## Mechanism` / `## Requirement map` / `## Predictor`;
those are C2-counter demands (`round45_c2_verify.py` V7/V9/V10/V11). **Passing the gate is necessary, not
sufficient.**

---

## 6. Risks / blockers for the L1

- **P2 needs the digest pinned (or an effective spec).** The frozen spec's `null` is a guaranteed defect on any
  direct invocation. Not fixable by a scribe.
- **P9 needs a clean worktree, which the wave's own reports dirty.** Commit the `.ufo/waves/round-45/**`
  artifacts (or gate a clean clone) before the counter's `--require-clean-tree` run. Measured: `untracked=159`
  mid-wave vs `untracked=0` after the artifacts landed.
- **P10 needs the receipt to be bare stdout.** A receipt captured through the host-safety envelope fails.
- **P1 pins move.** The probe digest changed mid-wave (`f87a9ee…` → `9363e03e…`) and the spec was re-pinned to
  match; a gate run on a tree older than the re-pin reports `mismatched`.
- **P5's `capture` field is a basename, not the upstream path.** Mixing the two fails 5 of 8 rows.
- **The probe needs network the first time.** `Bio` is not importable on host `python3`, so P10 falls back to
  `uv run --no-project --with biopython==1.85`, which downloads biopython (3.1 MiB) + numpy. Verified inside the
  envelope: `Downloaded biopython … Installed 2 packages in 127ms … bio ok 1.85`. An offline gate run would
  fail P10 with `probe could not be re-run`.

---

## 7. Receipts

| file | bytes | sha256 |
|---|---|---|
| `gate-pass1.txt` | 1238 | `276b293feac6cf9bfe90d91517a3f7d88f5276a2fddf93cae9857df691426dbf` |
| `gate-pass2.txt` | 1309 | `40bf382d4639d0026114265a5b770c2db84131f4f421283b3d57267624057235` |
| `gate-pass3.txt` | 1164 | `60cda44c704d23a16167d2fc30a7a2b71af50df2c97b9bbe64b1093168febc7f` |
| `gate-live.txt` | 1193 | `9f3ae3864a5e45aee35fc8c1567133320c34915a699bfdc5ae92c1c624227c8f` |
| `gate-live2.txt` | 1153 | `96ed9c5bb5a2dcd65b289f3303953ccb14a645f617c4ff5dc6ab9d3aca710393` |
| `gate-mirror3.txt` | 1157 | `df3f13cd4d2bdc8bc03379af37ca8e24ad2ab178092744d39763de93c2ae436c` |

Tooling: nothing installed or upgraded; no PATH directory touched (every ENVELOPE digest `unchanged`).

VERDICT: gate-demands-enumerated-PENDING
