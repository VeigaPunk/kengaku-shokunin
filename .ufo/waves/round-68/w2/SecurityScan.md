# SecurityScan — round 68, attempt 2, wave w2 (seat 6/12)

Read-only security review of the new A2 report-contract gate
(`plans/round68_report_contract.py`), its path surface, content surface, selftest surface and
injection surface. 2026-11-03. Seat `SecurityScan-6`; lane `kengaku-shokunin`; scratch
`/fast/scratch/hyaku/kengaku-r68/SecurityScan-6` (deleted before yield). No tool was installed,
upgraded or removed; no git/jj write command was run; no listener was started on port 8080.

A2 (`.ufo/waves/round-68/w2` spec): "Security review of the new A2 gate (read-only on L; probes
in S/; write W/SecurityScan.md)." Findings are labelled **must-fix** / **should-fix** / **note**.
No file in L was written; every probe ran in S against a copy of the committed gate bytes.

---

## 0. Bytes under review, provenance, and lane state

| item | value | how verified |
|---|---|---|
| gate of record | `plans/round68_report_contract.py` sha256 `18fbfc2111d747ae9f40220333f0bbd56062c89e93bcd7c2477358228a0723f4` (244 lines) | `sha256sum`; `git show HEAD:plans/round68_report_contract.py \| sha256sum` |
| gate commits | committed at `7803bdd4` ("freeze A2"), unchanged at HEAD `27f649f8` ("freeze A3") | `git log`, `git diff --quiet -- plans/round68_report_contract.py` → clean at review start |
| lane tip | `27f649f8` == `origin/master` at review end | `git rev-parse HEAD` / `origin/master` |
| SHONEN control | `SHONEN.md` sha256 `e65634a0aa51362734c380db033a363535aa1f4433c5b3578269f00ac147d8a1`, 4 boxes | box keys derived at run time: `SKILL.md contains real decision tables,` · `At least one end-to-end domain` · `Instructions executable by an agent` · `No cross-domain bleed (PROVINCE.md still` |
| r1 red fixture | `.ufo/waves/round-68/w2/report-fixtures/attempt1-report.md` sha256 `0399cd5376d27e1c006075929a9b3511c820fc326b4a3751a4cd9b78b8573839` | `cmp` against `a7575677:.ufo/reports/round-68/kengaku.md` → identical; provenance of r1 is sound |
| frozen contract | `plans/round-68-claims.md` lines 363–383 (S1–S6, fixtures r1–r5, "Every check must fail on its own red fixture", printed tally `SELFTEST n=5 red-refused=4 green-ok=1`), kill rules 385–388 | read in full |
| environment | `/usr/bin/python3` 3.14.8, `strace`, `timeout` present | `which`, `python3 -V` |

**Lane drift observed during the review (not mine, not a gate defect).** At review start HEAD was
`7803bdd4` and the working tree was clean for the gate. Mid-review HEAD advanced to `27f649f8`
(A3 freeze, another seat) and tracked files plus the gate itself became modified in the working
tree (another seat's uncommitted work; the gate working-tree sha moved `18fbfc21…` → `dbd3f373…`
→ `f30ed746…` → `dd09a96…`). I did not touch any of those files. To keep the analysis stable I
probed `git show HEAD:plans/round68_report_contract.py` copied to `S/gate-record.py` (sha
`18fbfc21…`, 244 lines). At the two drift states captured inside the probe window (`dbd3f373…`,
`f30ed746…`) `def check()` was **byte-identical** to the record (2924 B), so the S1–S6 verdicts
below were re-checked against both byte sets. The last observed state (`dd09a96…`, 267 lines,
captured after the probes) changes `check()` only in S1/S6 line matching — `norm(line) == norm(heading)`
instead of `line.strip() == heading`, and an `H2_RE` match instead of `line.startswith("## ")`;
S2/S3/S4/S5 are unchanged and fences are still not handled — so every finding below stands, and
the drift's substantive change is the enlarged selftest (rule F3 and §4). Any landing must be
re-hashed and the content matrix re-run against the landed bytes.

---

## 1. Method

* Read `plans/round68_report_contract.py` in full (244 lines: `norm` 48, `box_keys` 52,
  `section` 62, `check` 76, `skeleton` 146, `selftest` 165, `main` 204), Amendment A2 item 3 in
  full, and the whole claims doc.
* All fixtures were built from the gate's **own green skeleton** (`S/work/r5-green.md`, produced by
  `--selftest`) so each mutation isolates exactly one surface; the compliant skeleton is the
  control (`C0` below).
* Where a probe needed the gate's exact behaviour, the copy of record was executed
  (`python3 S/gate-record.py …`); the live path was spot-checked separately (identical verdicts).
* Every probe used absolute paths; FIFO/`/dev/*` probes were bounded by `timeout 10` or a
  subprocess timeout (recorded below).

Notation in the probe tables: `G` = the gate copy of record, `SH` = the lane `SHONEN.md`,
`S` = the seat scratch root. rc is the process exit code (124 = `timeout` killed a hang).

---

## 2. Path surface — probes and observed behaviour

The gate accepts `--lane`, `--shonen`, `--work` and a positional `report` with no path
normalisation, no regular-file check and no size cap. Only two reads are lane-derived:
`<lane>/SHONEN.md` and `<lane>/.ufo/waves/round-68/w2/report-fixtures/attempt1-report.md`
(lines 167–171); everything else is taken as given (lines 213–228).

| # | command (cwd = S unless stated) | observed |
|---|---|---|
| P1 | `timeout 10 python3 G fifo-report --shonen SH` | **HANG**: no output, rc **124**. `Path.read_text` → `open(2)` on a FIFO blocks until a writer appears; there is no `O_NONBLOCK`, `stat` or timeout guard. |
| P2 | `timeout 10 python3 G work/r5-green.md --shonen fifo-shonen` | **HANG**, rc **124** (same mechanism on the control input). |
| P3 | `python3 G dir-report --shonen SH` | rc **2**: `SETUP could-not-evaluate [Errno 21] Is a directory: '…/dir-report'` — correct. |
| P4 | `python3 G work/r5-green.md --shonen dir-report` | rc **2**, same `Is a directory` message — correct. |
| P5 | `python3 G link-report --shonen SH` (symlink → `/etc/hostname`) | rc **1**, `S1 headings=0/6 …`, `S6 bytes=9` — the gate **reads outside the lane** and evaluates the target. Expected for an operator path, but nothing binds the read to the lane. |
| P6 | `python3 G loop-report --shonen SH` (self-symlink) | rc **2**: `SETUP could-not-evaluate [Errno 40] Too many levels of symbolic links` — correct. |
| P7 | `python3 G /dev/null --shonen SH` | rc **1**, 5 defects; no hang (character device that returns EOF). |
| P8 | `python3 G /dev/zero --shonen SH` with `RLIMIT_AS = 400 MiB` | rc **1** with an **uncaught** traceback ending `MemoryError` at `report = report_path.read_text(...)` — the whole file is read with no size bound (a large regular file has the same shape). |
| P9 | `python3 G unreadable.md --shonen SH` (mode 000) | rc **2**: `[Errno 13] Permission denied` — correct. |
| P10 | `python3 G work/r5-green.md --shonen SHONEN.md` from `cwd=<lane>` vs `cwd=<fleet root>` | rc **0** vs rc **2** `No such file or directory: 'SHONEN.md'` — `--shonen` is resolved against the **caller's cwd**, not against `--lane` (line 214), and the resolved path is never printed. |
| P11 | `python3 G work/r5-green.md --shonen <other lane>/SHONEN.md` (tabi; souji) | rc **0** for both — another lane's checklist satisfies S2 (box text is template-identical across lanes). |
| P12 | `python3 G --selftest --lane <lane>/plans/.. --work S/work2` | rc **0** — `Path(...).resolve()` normalises `..`. |
| P13 | `python3 G --selftest --lane S/fakelane --work S/work3` · `--lane <fleet>/souji-shokunin` | rc **2** `SELFTEST r1-attempt1 missing fixture …` — `--lane` redirects the red-fixture read set into any tree (fails only because the fixture is absent there). |
| P14 | `python3 G --selftest --lane <lane> --work S/work-file` (regular file) | rc **2**: `[Errno 17] File exists` — correct. |
| P15 | `ln -s S/work-target S/work-link; python3 G --selftest --lane <lane> --work S/work-link` | rc **0**; the five fixtures appeared **in `work-target`**, i.e. writes follow a symlinked `--work`. |
| P16 | `python3 G --selftest --lane <lane> --work S/sub/../work5` | rc **0**; fixtures in `S/work5` — `..` in `--work` is honoured. |
| P17 | pre-create `S/work-clobber/r5-green.md` = `SENTINEL…`; `python3 G --selftest --lane <lane> --work S/work-clobber` | rc **0**; sentinel silently replaced by the fixture (`r5-green.md` now starts `Claim R68-C1 re-derived`). Fixed fixture names are written with plain `write_text` (line 189), no `O_EXCL`. |
| P18 | no `--work`; `TMPDIR=S/faketmp` where `S/faketmp/r68-a2-selftest` is a pre-created symlink to `S/tmp-target` | rc **0**; the five fixtures were written **into the symlink target** — the default work dir is `Path(TMPDIR or /tmp)/"r68-a2-selftest"` (line 216), a predictable, reused, symlink-followed name. |
| P19 | `python3 G --selftest --lane <lane> --work S/work-fifo` with a **FIFO** named `r5-green.md` inside | **HANG**, rc **124** — the write side of the selftest can also block on a FIFO fixture name. (`--work` may also point inside the lane or at `/`; no guard — see F9.) |

**Answers to the three path questions.** *Read outside the lane:* yes — any absolute/relative
`report`/`--shonen` path, a symlink, or a redirected `--lane` is honoured; nothing records the
resolved paths (F6, F12). *Hang:* yes — FIFOs on the positional report (P1), `--shonen` (P2) and
inside `--work` (P19); `/dev/zero` exhausts memory (P8); invalid UTF-8 crashes (C14). *Write
outside `--work`:* no escape was observed — `strace` shows every write-capable `openat` under the
resolved `--work` (§4) — but a symlinked or pre-created `--work` redirects the writes to its target
(P15, P18), and existing files with the fixed fixture names are clobbered (P17).

---

## 3. Content surface — can a contentless report pass?

`C0` is the gate's own green skeleton (1215 B, all six checks ok, rc 0) and is the control for
every mutation. Verdicts are from `python3 S/gate-record.py <fixture> --shonen SH` (rc shown).

| # | fixture | what was changed | rc | key observed lines |
|---|---|---|---|---|
| C0 | `work/r5-green.md` | none (gate's green skeleton) | **0** | `DEFECTS n=0` `PREDICATE R68-A2 pass` |
| C1 | `s1_contentless.md` | the six headings and nothing else (131 B) | **1** | `S2 defect box-lines=0 want=4`; `S3 defect … =None`; `S4 defect rows=0`; `S6 defect bytes=131` |
| C2 | `s1b_padded.md` | six headings + 1.1 KB of neutral prose (no boxes/verdicts/rows) | **1** | `S2`, `S3`, `S4` defect; `S1`/`S6` ok (`bytes=1105 sections=6`) |
| C3 | `s2_literal_single_token.md` | measurements rows are **one backticked token each**, one cell: `\| claim \|` / `\| `x` \|` / `\| `y` \|` | **0** | `S4 ok rows=2 pointed=2`, `DEFECTS n=0` → **contentless measurements pass** |
| C4 | foreign `../../../../.ufo/reports/round-15/tabi.md` (tabi, round 15, 14008 B, sha `f3da2b9e…`) | none — **another lane's report, verbatim** | **0** | `DEFECTS n=0` `PREDICATE R68-A2 pass` → **a foreign report passes** |
| C5 | `c11_box_prefix_only.md` | each box line reduced to the box's first five words | **0** | `S2 ok box-lines=4 want=4 matched=4` — no evidence text required |
| C6 | `c7_one_real_row.md` | header row whose first cell is `\| `h` \|` + **one** data row | **0** | `S4 ok rows=2 pointed=2` — the header counts as a table row |
| C7 | `c14_all_fenced.md` | all six headings, the trend lines and the measurements table inside one fenced block | **0** | `S1 ok headings=6/6`; `S3 ok`; `S4 ok rows=2`; `S6 ok bytes=460 sections=6` |
| C8 | `c4_fenced_shonen.md` | the four real box lines removed; four checklist lines placed inside a code fence | **0** | `S2 ok box-lines=4 want=4 matched=4` → **fenced checklist lines count** |
| C9 | `c9_fenced_trends.md` · `c10_fenced_table.md` | trend lines / measurements table moved inside a fence | **0** · **0** | `S3 ok` · `S4 ok rows=2` |
| C10 | `c12_unknown_placeholder.md` | `XXX FILL-THIS-LATER` in a section | **0** | `S5 ok placeholders=[]` — the denylist is 5 exact substrings |
| C11 | `s5_todos.md` | the word `todos` in prose | **1** | `S5 defect placeholders=['TODO']` — substring scan, false positive |
| C12 | `c13_shonen_first.md` | `## SHONEN` first | **1** | `S1 defect … ordered=False` — order enforced (expected) |
| C13 | `s1_bold_heading.md` | `## **Work performed**` | **1** | `S1 defect … missing=['## Work performed']` — headings are matched literally |
| C14 | `badutf8.md` | report bytes contain `0xff` | **1** | uncaught `UnicodeDecodeError` traceback (no `SETUP`, no `DEFECTS` line) — rc 1 conflates crash with defects |
| C15 | `vacuous_shonen.md` + `--shonen empty-shonen.md` | empty SHONEN section and a checklist file with **zero** boxes | **0** | `S2 ok box-lines=0 want=0 matched=0`, `DEFECTS n=0` → **S2 is vacuous with 0 boxes** |
| C16 | foreign `../../../../.ufo/reports/round-67/kengaku.md` (own lane, prior round, 19754 B) | verbatim | **0** | `DEFECTS n=0` — a prior round's report passes this round's gate |
| C17 | `../../../../.ufo/reports/round-1/tabi.md` · `round-98/lore.md` | verbatim | **1** · **1** | S2/S3/S4 defects (box wording/backticked checkboxes; no tables) — older layouts fail |

**s3 sweep (scale check).** Loading the gate's own `check()` and testing every fleet report in
`.ufo/reports/*/*.md` against this lane's `SHONEN.md` at capture: **57 of 1063 reports pass
verbatim** (52 of them from other lanes: tabi 4, tameshi 3, kaidoku 7, mado 2, kama 1, tsukuroi 8,
kake 11, kagi 1, chousa 4, souji 8, kasegi 2, kotodama 1; plus 5 of this lane's own older rounds,
including `round-31`, `round-53`, `round-55`, `round-64`, `round-67`). Three passes were re-run
through the binary (`round-15/tabi.md`, `round-17/kaidoku.md`, `round-31/kengaku.md`, rc 0); the
count moves as other lanes write (`round-72/kake.md` is among the newest passers). The full list
was written to `S/s3-passes.txt` before scratch deletion.

**Verdict on the seat's item 3.** s1 does **not** pass (C1/C2) — good. s2 **passes** (C3) and s3
**passes** (C4/C16) — both are must-fix findings under this seat's rule ("a pass is a must-fix
finding"). The root cause is that S1–S6 are form checks: no check binds the report to this lane or
this round, and no check requires a measurements row to carry a command, a before/after value or
an existing evidence path.

---

## 4. Selftest surface — does `--selftest` write into L?

**No.** Verified with a syscall trace, not just a tree diff, because the lane tree was moving
under other seats during the review.

```
strace -f -qq -e trace=openat,mkdir,unlink,unlinkat,rename,renameat,creat \
  -o S/selftest2.strace timeout 120 python3 S/gate-record.py \
  --selftest --lane <lane> --work S/work-final
```

* write-capable `openat` (`O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND`) outside `S`: **none**;
* `mkdir`/`unlink`/`rename`/`creat` outside `S`: **none**;
* the only lane opens are reads:
  `openat(AT_FDCWD, "<lane>/SHONEN.md", O_RDONLY|O_CLOEXEC)` and
  `openat(AT_FDCWD, "<lane>/.ufo/waves/round-68/w2/report-fixtures/attempt1-report.md", O_RDONLY|O_CLOEXEC)`;
* the fixtures appeared only under `--work` (`r1-attempt1.md`, `r2-three-boxes.md`,
  `r3-no-discernment.md`, `r4-placeholder.md`, `r5-green.md` for the record bytes).

At the first selftest run the tracked lane state was identical before/after
(`git status --porcelain -uno` + `rev-parse HEAD` diffed clean). Later in the session the lane
gained another seat's edits (HEAD `7803bdd4` → `27f649f8`, six tracked files modified, including
the gate); **that drift is not attributable to the gate** — the trace above shows no lane writes,
and the drift began with an unrelated commit (A3) by another seat. Recorded so the L1 does not
misread `git status` as a gate write.

**Coverage of the frozen sentence "Every check must fail on its own red fixture."** The committed
selftest's five fixtures do not cover S4 or S6:

| fixture | target check(s) | observed defect sets (record bytes) |
|---|---|---|
| r1-attempt1 | S1, S2, S3 | `['S1','S2','S3']` — S4/S5/S6 **pass** on it |
| r2-three-boxes | S2 | `['S2']` |
| r3-no-discernment | S3 | `['S3']` |
| r4-placeholder | S5 | `['S5']` |
| r5-green | none (control) | `pass` |
| — | **S4, S6** | **no fixture** |

`SELFTEST n=5 red-refused=4 green-ok=1`, rc 0 — i.e. the printed tally is exactly A2's literal
string, but S4 and S6 are never shown capable of failing **in the selftest**. (They can fail:
C1/C3/C6/C7 show S4 defects, C1 shows S6 defects; the gate just does not prove it.) The working-tree
drift (another seat, uncommitted) adds `r6-wrong-labels`, `r7-order-swapped`, `r8-duplicate-heading`,
`r9-unpointed-rows` (S4) and `r10-minimal` (S1/S2/S3/S4/S6), later `r11-five-boxes`, and changes the
tally to `SELFTEST n=11 red-refused=10 green-ok=1`; `def check()` is unchanged. So the drift
addresses S4/S6 coverage but no longer prints A2's literal tally — either way A2 item 3 needs an
amendment to be true as written (see F3). At the drift states captured in the probe window
`def check()` was unchanged; the latest observed state (`dd09a96…`) also adds
`r12-spaced-dup-heading` and normalises the S1 heading match and the S6 section regex.

---

## 5. Injection surface — fenced checklist lines and friends

The checker is line-based and has no fence state anywhere (`section()` 62–74, `CHECK_RE` 63,
`PLACEHOLDERS` scan 133–136, table scan 114–130).

| # | fixture | observed |
|---|---|---|
| I1 | `c4_fenced_shonen.md`: the four real box lines deleted; four `- [x] …` lines placed inside a ` ```text ` fence under `## SHONEN` | `S2 ok box-lines=4 want=4 matched=4`, rc 0 — **S2 counts fenced checklist lines.** The injection is sufficient on its own: the report passes with no real checklist. |
| I2 | `c5_fenced_heading.md`: the compliant skeleton with a fenced `## SHONEN` line inside `## Work performed` | rc 1: `S1 defect … dup=['## SHONEN x2']` and `S2 defect box-lines=0 want=4` — a *compliant* report that merely quotes a heading in a fence is **rejected** (false negative; the fenced heading also hijacks `section()`'s first-hit lookup). |
| I3 | `c6_fenced_todo.md`: compliant skeleton with `TODO` inside a quoted code fence | rc 1: `S5 defect placeholders=['TODO']` — **false positive**; this lane's reports routinely quote log lines and headings. |
| I4 | `c9_fenced_trends.md` / `c10_fenced_table.md`: trend verdicts / measurements table inside a fence | rc 0 both: `S3 ok`, `S4 ok rows=2` — fenced trend words and fenced table rows satisfy the checks. |
| I5 | `c14_all_fenced.md`: all six headings plus the trend lines and the table inside one fence | rc 0: `S1 ok`, `S3 ok`, `S4 ok`, `S6 ok` — a report whose only "content" is a quoted block passes S1/S3/S4/S6. |
| I6 | S5 denylist: `c12_unknown_placeholder.md` (`XXX FILL-THIS-LATER`) | rc 0 — placeholders outside the five-substring list are invisible. |
| I7 | log injection | no report text is echoed: S1 prints the fixed heading list, S2/S3/S4 counts, S5 the fixed placeholder names. **No log-injection path found** (positive). |

---

## 6. Findings

### Summary

| id | severity | surface | one line |
|---|---|---|---|
| F1 | **must-fix** | content | form-only pass: a contentless report, a foreign report, or a prior-round report passes `DEFECTS n=0` (C3, C4, C5–C7, C16; 57/1063 fleet reports verbatim) |
| F2 | **must-fix** | content | S2 does not enforce the frozen "(4 boxes)": zero boxes + empty section passes; another lane's checklist passes (C15, P11) |
| F3 | **must-fix** | selftest | the committed selftest has no red fixture for S4 or S6, so A2's "Every check must fail on its own red fixture" is false for the record; the frozen fixture list makes it unrealizable |
| F4 | should-fix | injection | fence-blind parsing: fenced text satisfies S1/S2/S3/S4/S6 (false green) and a compliant report quoting a heading/TODO is rejected (false red) |
| F5 | should-fix | input | no regular-file/size/encoding guard: FIFO hang (rc 124), `/dev/zero` `MemoryError`, invalid UTF-8 traceback with rc 1 |
| F6 | should-fix | path | `--shonen` is cwd-relative, unresolved and unprinted; the same command line reads a different control from a different cwd |
| F7 | should-fix | write | default `--work` is a predictable, reused, symlink-followed path; fixed fixture names overwrite existing files silently |
| F8 | note | path | `--lane` is accepted but ignored in report-check mode |
| F9 | note | write | `--selftest --work` may point inside the lane or anywhere writable; conformant with "only under --work", but unguarded |
| F10 | note | content | content-strength details (S2 one-way prefix, `[ ]` accepted, S3 prose/prefix matching, S5 substring denylist, S6 lower bound, literal headings) |
| F11 | note | provenance | r1 fixture is not hash-pinned by the selftest; replacing it keeps `red-refused=4` without testing the real attempt-1 bytes |
| F12 | note | provenance | the gate prints no input identities; a log cannot show which report/SHONEN produced a verdict |

### F1 — **must-fix** — the gate's green certifies form only; a contentless or foreign report passes

* **Exploit path.** (a) An agent writes the six headings, four lines that begin with the SHONEN
  boxes' first five words, three `trend: verdict` lines and two table rows whose cells are any
  backticked token (`C3`); or (b) copies any historical fleet report that happens to satisfy the
  generic form (`C4`, 57/1063 verified); or (c) puts the tables/trends inside a code fence (`C7`).
  `python3 plans/round68_report_contract.py <report> --shonen SHONEN.md` prints `DEFECTS n=0` and
  `PREDICATE R68-A2 pass`, exits 0.
* **Evidence.** `C3` (`| `x` |`, `| `y` |`), `C5` (box lines truncated to five words), `C6`
  (header counted as a data row, one real row), `C7` (all content fenced), `C16`
  (`round-67/kengaku.md` verbatim, rc 0), the 57/1063 sweep. The A2 text itself asks only for
  "a backticked token or a 7+-hex commit hash" in S4 and "matched by the box's first five words"
  in S2 — the gate faithfully implements the frozen words; the frozen words are too weak.
* **Impact.** The round's own report contract is the evidence that attempt 1's defect is fixed.
  A green R68-A2 can be produced without a single round-68 measurement, and cannot distinguish
  this round's report from another lane's or a prior round's. That is a false-assurance defect in
  the record, not merely a usability gap.
* **Smallest remediation.** An A2 amendment (no seat may edit the frozen text in place): bind the
  report to the lane and round (H1 must name `kengaku` and `round 68`; require the two claim rows
  `R68-C1`/`R68-C2`), require ≥2 **data** rows excluding any header, require each row's backticked
  token to be the claim's frozen counting command or an existing lane-relative evidence path, and
  require each SHONEN box line to carry non-empty evidence text after the box words. If the
  amendment is not taken, record in the claims doc that R68-A2 green is a form check and stop
  citing it as content or origin evidence.

### F2 — **must-fix** — S2 drops the frozen "(4 boxes)" requirement and the S2 control is transferable

* **Exploit path.** Point `--shonen` at a checklist with zero boxes (or empty the lane's
  `SHONEN.md`) and supply a report with an empty `## SHONEN` section: `S2 ok box-lines=0 want=0
  matched=0`, overall rc 0 (`C15`). Separately, `--shonen` to another lane's `SHONEN.md` passes
  (`P11`), because the box wording is template-identical across lanes.
* **Evidence.** `empty_both` rc 0; `box_keys()` returns whatever the file holds
  (`plans/round68_report_contract.py:52-60`); the frozen sentence is
  `… one line per box in SHONEN.md (4 boxes)` (claims doc line 370).
* **Impact.** A truncated or replaced checklist silently disables the SHONEN control; the S2
  control has no lane binding. With the intact 4-box file the check behaves, so the scored path is
  unaffected — the defect is the missing guard and the predicate/implementation mismatch.
* **Smallest remediation.** After reading the control, require `len(box_keys(shonen)) == 4`
  (and `rc 2` with a clear `SETUP` line if not); resolve `--shonen` inside `--lane` by default and
  refuse a path outside it unless a new explicit flag is passed.

### F3 — **must-fix** (record) — the selftest does not prove S4/S6 can fail; A2's own sentence cannot be met by its frozen fixture list

* **Evidence.** `SELFTEST r1-attempt1 … defects=['S1','S2','S3']` (S4/S5/S6 pass on it);
  r2→S2, r3→S3, r4→S5; no fixture targets S4 or S6. A2 says "Every check must fail on its own red
  fixture" and fixes the tally as `SELFTEST n=5 red-refused=4 green-ok=1` (claims doc lines 382–383).
  The S4 and S6 checks *are* failable (C1/C3/C6/C7) — the selftest just never shows it, so a
  regression that disables S4 or S6 would leave the selftest green.
* **Impact.** A2's verification claim is not true of the committed gate; kill rule (b) ("a check
  cannot fail on its own red fixture → vacuous") is unmet for S4/S6 on the record bytes.
* **Smallest remediation.** Amend A2 to add `r6` (S4-only: rows without backticks/hash) and `r7`
  (S6-only: <400 B or <3 sections) and update the printed tally sentence. The uncommitted
  working-tree drift already moves in this direction (r9/r10/r11, `check()` unchanged) but changes
  the tally to `n=11 red-refused=10`, which contradicts A2's literal string without an amendment.

### F4 — **should-fix** — fence-blind parsing produces both false greens and false reds

* **Evidence.** I1 (`c4`: fenced box lines satisfy S2 with the real lines removed, rc 0),
  I2 (`c5`: fenced `## SHONEN` → S1 dup + S2 zero, a compliant report rejected), I3 (`c6`: fenced
  `TODO` → S5 defect), I4/I5 (`c9`, `c10`, `c14`: fenced trends/tables/headings satisfy
  S3/S4/S1/S6). `section()` stops only on a raw `## ` prefix and `check()` never tracks ` ``` `.
* **Impact.** A report can pass on quoted material; a report that quotes headings or log lines —
  normal in this lane's reports — is rejected with a misleading defect. Both directions were
  observed on the same checker.
* **Smallest remediation.** Add a fence-aware line filter (toggle on lines whose `strip()` starts
  with ```` ``` ````) and run S1–S5 on non-fenced lines only; apply the same filter to the
  heading scan, `section()`, `CHECK_RE`, the trend regex and the table scan.

### F5 — **should-fix** — non-regular inputs are neither bounded nor classified

* **Evidence.** P1/P2: FIFO report or `--shonen` blocks with no output — `timeout 10` → rc 124.
  P19: a FIFO named `r5-green.md` in `--work` blocks the selftest (rc 124). P8: `/dev/zero` with
  `RLIMIT_AS` 400 MiB → uncaught `MemoryError` traceback, rc 1. C14: invalid UTF-8 →
  uncaught `UnicodeDecodeError`, rc 1. Directories, symlink loops and unreadable files are
  correctly rc 2 (`SETUP`).
* **Impact.** A driver that runs the gate on a path that is not a regular file hangs forever (no
  output, no timeout); a crash exits 1, which the contract defines as "defects", so a caller
  checking only rc cannot distinguish a crash from a real defect verdict; a huge or unbounded
  source can exhaust the runner's memory.
* **Smallest remediation.** Before reading: `st = os.stat(path)`; require `stat.S_ISREG(st.st_mode)`
  and `st.st_size <= 1 MiB`; open with `O_NOFOLLOW` if symlinks are not wanted; wrap
  `read_text` in `except (OSError, UnicodeDecodeError)` → `SETUP could-not-evaluate …` rc 2.
  For the write side, create fixtures with `os.open(..., O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW)`.

### F6 — **should-fix** — `--shonen` is cwd-relative, unresolved, and unprinted

* **Evidence.** `shonen_path = Path(args.shonen) if args.shonen else lane / "SHONEN.md"`
  (line 214; no `.resolve()`, no join with `lane`). P10: identical argv, rc 0 from `cwd=<lane>` and
  rc 2 from `cwd=<fleet root>`. P11: another lane's file accepted. The gate never prints the paths
  or hashes it read.
* **Impact.** The "same command" produces a different control depending on where the driver stands;
  a driver that `cd`s away silently checks a different checklist (or fails late with a raw errno).
  With a crafted path it reads any file — already possible by absolute path, but the cwd
  dependence is what makes an accidental wrong control likely.
* **Smallest remediation.** `shonen_path = (Path(args.shonen) if args.shonen else lane / "SHONEN.md").resolve()`;
  if it is not under `lane`, refuse (rc 2) unless an explicit `--allow-foreign-shonen` is passed;
  print `INPUT report=<path> sha256=… shonen=<path> sha256=…` before the checks.

### F7 — **should-fix** — predictable, reused, symlink-followed default work dir; silent clobber

* **Evidence.** `work = Path(args.work) if args.work else Path(os.environ.get("TMPDIR", "/tmp")) / "r68-a2-selftest"`
  (line 216), `work.mkdir(parents=True, exist_ok=True)` (166), `path.write_text(...)` with fixed
  names `r1-attempt1.md`…`r5-green.md` (189). P18: a pre-created symlink at
  `$TMPDIR/r68-a2-selftest` redirected all five writes into its target. P17: an existing
  `r5-green.md` was replaced without warning. P19: a FIFO with a fixture name hangs the run.
* **Impact.** On a shared host, any local user who can create `/tmp/r68-a2-selftest` (or set the
  caller's `TMPDIR`) redirects the fixture writes to a directory of their choosing and controls
  the fixture contents the selftest believes it produced; on a single-user host the same
  mechanism silently overwrites files with those names. The fixtures are copies of tracked,
  non-secret text, so the information impact is low; the integrity/assurance impact is not.
* **Smallest remediation.** When `--work` is absent use `tempfile.mkdtemp(prefix="r68-a2-selftest.")`
  (mode 0700); create the five files with `O_EXCL|O_NOFOLLOW`; refuse a `--work` that resolves
  inside the lane or is not a directory owned by the caller.

### F8 — **note** — `--lane` is accepted but ignored in report-check mode

`--lane` (line 207) is only used for the default `--shonen` when `--shonen` is absent (214) and for
the selftest reads (167–171); with an explicit `--shonen` it has no effect on a report check. A
mistyped `--lane` passes silently. Print the effective lane/shonen paths (F6) so this cannot hide.

### F9 — **note** — `--selftest --work` may point into the lane or anywhere writable

No write outside the resolved `--work` was observed (§4, strace), which satisfies the A2 sentence
"built in scratch". But there is no assertion that `--work` is outside the lane (or outside `/`),
so `--work <lane>/plans` would create five untracked files in the lane; this is a caller error, not
a path escape.

### F10 — **note** — content-strength details of S1–S6

* S2 matching is one-directional `startswith`: a line that only begins with the box's first five
  words passes, and an all-`[ ]` section passes (state is not checked — the frozen text allows it).
* S3 matches its verdict words in prose and inside fences, and prefixes (`improved-ish` matches).
* S4 counts any `|`-line in the section; header rows whose first cell does not start with `claim`
  are counted as data rows (F1/C6), and a row qualifies with one backtick anywhere.
* S5 is a five-string substring scan, case-folded (`"todos"` hits `TODO`; `XXX FILL-THIS-LATER`
  does not hit).
* S6 is a lower bound only (`≥400 B`, `≥3` raw `## ` lines, fenced ones included).
* S1 matches headings literally (record: `line.strip() == heading`; latest drift: `norm(line) ==
  norm(heading)`): `## **Work performed**` is still a missing heading; trailing and interior extra
  spaces are accepted.

### F11 — **note** — the r1 fixture is not hash-pinned by the selftest

`selftest()` reads `<lane>/.ufo/waves/round-68/w2/report-fixtures/attempt1-report.md` and counts any
failure as `red-refused` (lines 168–171). The fixture is tracked and byte-identical to the fleet
report at `a7575677` (verified), but nothing in the selftest records that sha. Replacing the file
with any failing text keeps `red-refused=4` while no longer demonstrating that the real attempt-1
report fails — i.e. kill rule (a) ("the gate passes the attempt-1 report → vacuous") is only as
strong as an unpinned fixture. Remediation: embed the expected sha256 of the fixture (the C1
`PROBE`/`BASE-PROBE` pattern) and refuse rc 2 on mismatch.

### F12 — **note** — no input identity is printed

The gate prints no report path, no SHONEN path and no hashes. Combined with F6 this makes it
impossible to tell from a log which control produced a `PREDICATE R68-A2 pass`. Print a single
`INPUT report=<path> sha256=… shonen=<path> sha256=…` line before the checks; this also gives the
verdict a provenance binding for free.

---

## 7. What held (positive controls)

* Missing, directory, symlink-loop and permission-denied inputs all exit **2** with a single
  `SETUP could-not-evaluate …` line and no traceback (P3/P4/P6/P9).
* A six-heading report with no content is rejected (C1), as is the padded variant (C2); heading
  order and duplicates are rejected (C12; the frozen-required order is enforced); missing headings
  are rejected (C13).
* The attempt-1 report is rejected by the committed red fixture (`S1/S2/S3` defects), and the gate
  prints A2's literal `SELFTEST n=5 red-refused=4 green-ok=1` (rc 0) on the record bytes.
* `--selftest` writes only under `--work` (strace: no write-capable open outside the scratch root;
  lane opens are `O_RDONLY`), and the report-check path performs no writes at all.
* No report text is echoed into stdout/stderr, so there is no log-injection path (I7).
* Exit codes follow the documented 0/1/2 semantics for every OSError case; only the crash cases
  (F5) break the mapping.

---

## 8. Boundary observations for the L1 (not gate findings)

1. **Lane tree was not stable during w2.** At review start HEAD was `7803bdd4` and the gate was
   clean. Mid-review HEAD became `27f649f8` (A3 freeze) and another seat's uncommitted edits
   appeared on `SCORECARD.md`, `SKILL.md`, `corpus/SOURCES.md`, `corpus/lessons/round-68.md`,
   `plans/round-68-claims.md`, `plans/round68_capability_table.py` and
   `plans/round68_report_contract.py` (working-tree sha `dbd3f373…`, then `f30ed746…`, then
   `dd09a96…`/267 lines after the probes). I did not modify any of them; my probes used
   `git show HEAD:…`. Any landing check must re-hash the gate and re-run §3–§4 after the tree
   settles.
2. **The drift's selftest changes A2's printed contract.** The working-tree selftest adds
   r6–r11 and prints `SELFTEST n=11 red-refused=10 green-ok=1`. If that edit lands, A2 item 3's
   fixture sentence and its literal tally are both stale and need a dated amendment (the F3
   remediation). The latest drift also normalises heading matching (S1) and uses an `H2_RE` for the
   S6 section count; S2/S3/S4/S5 are unchanged.
3. **Sweep counts move.** The 57/1063 figure was captured while other lanes were writing
   `.ufo/reports/`; the gate-resident `check()` was used for the sweep, and three passers were
   re-confirmed through the binary. The class (form-only acceptance of foreign reports) does not
   depend on the exact count.

---

## 9. Reproduce

All commands from `S = /fast/scratch/hyaku/kengaku-r68/SecurityScan-6`, with
`G = S/gate-record.py` (sha `18fbfc21…`, from `git -C <lane> show HEAD:plans/round68_report_contract.py`)
and `SH = <lane>/SHONEN.md`:

```
# control + content matrix
python3 G work/r5-green.md --shonen SH
python3 G s2_literal_single_token.md --shonen SH
python3 G c11_box_prefix_only.md --shonen SH
python3 G c7_one_real_row.md --shonen SH
python3 G c14_all_fenced.md --shonen SH
python3 G c4_fenced_shonen.md --shonen SH
python3 G c5_fenced_heading.md --shonen SH
python3 G c6_fenced_todo.md --shonen SH
python3 G vacuous_shonen.md --shonen empty-shonen.md
python3 G badutf8.md --shonen SH
python3 G /home/vgpnk/Projects/shokunin/.ufo/reports/round-15/tabi.md --shonen SH
python3 G /home/vgpnk/Projects/shokunin/.ufo/reports/round-67/kengaku.md --shonen SH

# path matrix
timeout 10 python3 G fifo-report --shonen SH            # rc 124
timeout 10 python3 G work/r5-green.md --shonen fifo-shonen   # rc 124
python3 G dir-report --shonen SH                        # rc 2
python3 G link-report --shonen SH                       # symlink -> /etc/hostname, rc 1
python3 G loop-report --shonen SH                       # rc 2
python3 G work/r5-green.md --shonen SHONEN.md           # from <lane> rc 0; from fleet root rc 2
python3 G --selftest --lane <lane> --work work-link     # symlinked --work
TMPDIR=S/faketmp python3 G --selftest --lane <lane>     # pre-created symlink at $TMPDIR/r68-a2-selftest

# selftest write audit
strace -f -qq -e trace=openat,mkdir,unlink,unlinkat,rename,renameat,creat \
  -o selftest2.strace timeout 120 python3 G --selftest --lane <lane> --work work-final
```

---

## 10. Cleanup

The scratch root `/fast/scratch/hyaku/kengaku-r68/SecurityScan-6` (fixtures, gate copies,
probe JSON, strace logs, sweep list) was deleted before yield; the receipts are the commands and
observations above. Tools installed/upgraded/removed: **none**.
