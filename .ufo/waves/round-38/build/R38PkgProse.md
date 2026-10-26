# R38PkgProse — C2 lane prose (PROVINCE / README §Frontier / SKILL decision table)

Seat: `R38PkgProse` (leaf). Round 38 wave 1, kengaku-shokunin, 2026-10-26. Lane root
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` (tip `2c5f4e0`, freeze `e0a3785`, receipt `e95cf55`).
Scope: **drafts only** — no lane file was edited, no commit, no gate/counter/probe run beyond the reproductions
listed in §2.

## Axes named

- **Coverage** — the drafts carry the executed receipt (22 cases, 7 pass / 15 fail, 0 mismatches) and the one new
  edge class (built artefact + source tree graded by presence, `ldd` text, directory shape, stdout regex).
- **Depth** — every SKILL row is bound to the assertion that decides it (`test_outputs.py:<L>`), the probe line that
  stages the state, and a receipt `CASE` id + line.
- **Adjacency** — the README draft also lands the two tokens `plans/pkg_gate.py` P8 actually checks (single-line
  coverage bullet, index row), and the report routes the open items (entry, SOURCES rows, issue #59) instead of
  absorbing them.

## §1 Deliverables

| file | paste target | shape |
|---|---|---|
| `.ufo/waves/round-38/build/R38PkgProse/PROVINCE-round38.md` | `PROVINCE.md`, after `## Round37 partial frontier admission (2026-10-26)` and its `**Reported out (round 37):**` paragraph | one `## Round38 partial frontier admission (2026-10-26)` section, 294-word paste block |
| `.ufo/waves/round-38/build/R38PkgProse/README-frontier-r38.md` | `corpus/README.md` | three blocks: **b1** §Frontier sub-bullet (the assignment's item), **b2** coverage bullet, **b3** knowledge index row |
| `.ufo/waves/round-38/build/R38PkgProse/SKILL-build-provenance-r38.md` | `SKILL.md`, after the round-37 section (`SKILL.md:755-806`) | `## Build-provenance TB2 grader — round 38`, 13-row decision table + green-meaning + limits |
| `.ufo/waves/round-38/build/R38PkgProse/derived-labels.txt` | evidence for the entry author / L1 | V7 label derivation from the receipt with its command |

Every SKILL row names at least one receipt `CASE` id; the table has **13** data rows.

## §2 Verification actually run

All commands from the lane root unless stated; scratch `S=/fast/scratch/hyaku/kengaku-r38/R38PkgProse`.

1. Captures intact:
   `sha256sum -c corpus/evidence/round38/tb2-build-pmars/SHA256SUMS` →
   `instruction.md: OK / solve.sh: OK / task.toml: OK / test.sh: OK / test_outputs.py: OK`.
2. Frozen instrument digests:
   `sha256sum plans/build_pmars_probe.py plans/pkg_gate.py plans/pkg-spec-r38.json corpus/evidence/round38/build-pmars-dry-cases-freeze.txt corpus/evidence/round38/build-pmars-probe.txt` →
   `32f0771c…5c24a`, `ea638822…edd41`, `bd9bfe71…13de2`, `93b4b60c…4df0`, `2408b477…4ef9` (probe, gate, spec, dry
   table, receipt). The receipt digest is not one of the counter's pins (the counter fills `receipt_sha256`); the
   other four equal the counter's frozen values (`plans/round38_c2_verify.py:63-69`).
3. Provenance: `git log --oneline -4` →
   `2c5f4e0 round-38: wave-1 build spec … against e95cf550` / `e95cf55 round-38: first recorded build-pmars probe
   run on a clean clone of e0a37853 (cases=22 observed_pass=7 observed_fail=15 mismatches=0; second run byte-equal)`
   / `e0a3785 round-38: freeze …` / `21e6251 round-37: wave-2 reports …`.
4. **Gate P8 reproduced on the drafts** (not on the lane): fresh copy of `corpus/README.md` + `corpus/SOURCES.md` +
   `corpus/knowledge/` into `$S/pkg`, b1/b2/b3 pasted at their stated positions, one stub entry file added, then
   `pkg_gate.c_readme(Package.load(...))` → `(True, 'index_rows=45 knowledge_files=45 bad=0 first=0')`. Before the
   b2 rewrite (multi-line bullet) the same call returned
   `(False, '… bad=1 first=no coverage bullet naming the entry and its receipt')`, which is why b2 is one line.
   Anchor counts in the untouched lane: 44 `corpus/knowledge/*.md`, 44 index rows.
5. SKILL table: 13 data rows parsed; every backticked case id in each row's cite column is a `CASE` id in the
   receipt (`ALL CITED IDS VALID: True`).
6. `derived-labels.txt` reproduced the V7 derivation; output is §3.1.
7. Upstream adjacent fetch (read-only):
   `curl -s https://api.github.com/repos/harbor-framework/terminal-bench-2/issues/59` → title
   `` `build-pmars` failing with oracle solution ``, `"state": "open"`, `created_at 2026-04-13T22:14:26Z`, author
   `sam571128`; body quotes the failing pin: ``E: Version '1.22.21' for 'dpkg-dev' was not found``.

Not run, deliberately: the probe (`--lane .`), the C2 counter, the gate, pytest, any pytest/uvx path, the task
image, the oracle. No tool was installed.

## §3 Findings (observations; each carries its source)

### 3.1 Every V7 label derives `partly`, not `enforced`

`derived-labels.txt` (command inside the file) over the receipt:

```
from-source      partly  violating=22 pass-among-them=7
no-x11           partly  violating= 3 pass-among-them=1  (canned-x11-dlopen)
debian-source    partly  violating=22 pass-among-them=7
extract-to-app   partly  violating=22 pass-among-them=7
install-path     partly  violating= 4 pass-among-them=1  (path-split)
results-format   partly  violating= 5 pass-among-them=1  (results-trailing-text)
debugger-works   partly  violating=22 pass-among-them=7
```

Rule applied verbatim from `plans/round38_c2_verify.py:216-222` (`derive`): all-fail → `enforced`, all-pass →
`unenforced`, else `partly`. Consequence for the entry author: no row of `## Requirement map` may be labelled
`enforced` or `unenforced` at this receipt. My SKILL draft states this once (`no instruction line is `enforced` by
this grader alone`) without claiming a class.

### 3.2 Test-letter order is the probe's tuple, not the file order

`plans/build_pmars_probe.py:61`: `TESTS = ("test_pmars_works", "test_headless_no_x11",
"test_debian_source_used", "test_built_from_source")`; the receipt's `tests=` string is that order. So
`PPFP` (`no-debian-dir`) is the third test failing, and `PPPF` (`src-no-c`, `no-src-dir`) the fourth. Any prose that
reads a letter position as a different test will be wrong; my drafts never name a letter position.

### 3.3 The seven receipt passes are the whole instruction-gap story

`receipt:5,9,11,16,19,21,23` = `canned-shape`, `canned-x11-dlopen`, `results-trailing-text`,
`canned-exit-nonzero`, `path-split`, `debian-is-file`, `c-is-dir`. Each is a state that violates at least the
gauntlet `from-source`/`debian-source`/`extract-to-app`/`debugger-works` (`plans/build_pmars_probe.py:76`) and is
still observed `pass`. The failing half is equally useful for a reviewer: `canned-x11-linked` (receipt:8) shows the
`ldd` scan does fire on a link-time X11 dependency, and `results-two-ints`/`results-negative` (receipt:10,13) show
the integer count and sign are enforced.

### 3.4 Gate P8 has two independent README requirements, and one of them is a single line

`plans/pkg_gate.py:233-256` (`c_readme`) requires: (a) exactly one index row whose first cell is
`` `knowledge/tb2-build-pmars-grader.md` `` and whose text contains both `S115` and `S116`; (b) a line starting
exactly `- ` that contains `tb2-build-pmars-grader.md` **and** `evidence/round38/build-pmars-probe.txt`; (c) the
set of `knowledge/*.md` names equal to the set of index rows. A wrapped markdown bullet satisfies neither check —
§2.4's first result is that failure. b1 (the §Frontier sub-bullet) is indented and does not satisfy (b); b2 exists
for that.

### 3.5 The registry rows do not exist yet

`grep -c "S115\|S116" corpus/SOURCES.md` → `0` (exit 1). The frozen spec and the counter expect both rows with an
11-cell registry row, tier `A`, status `mined`, a `sha256 <64 hex>` anchor equal to that row's own pin, and the
entry path in the used-by cell (`plans/pkg-spec-r38.json`; `plans/round38_c2_verify.py:127-146` V3;
`plans/pkg_gate.py:191-213` P6). My prose cites `S115, S116` because the frozen spec names them; until the rows
land, P6/V3/V6 are red independently of this prose. `corpus/knowledge/tb2-build-pmars-grader.md` likewise does not
exist (`ls corpus/knowledge | grep -i pmars` empty), so P8's file/index equality needs the entry in the same commit
as b3.

### 3.6 "14-line" lives only in prose: neither the claims nor the receipt carries it

Correction to an earlier reading in this report: `grep -n "14-line\|14 line" plans/round-38-claims.md` returns
nothing (exit 1), and so does the receipt. The phrase comes from the wave-1 seat brief's headline-observations
sentence ("a canned 14-line C program + empty debian/ dir + zero-byte src/dummy.c"), not from a frozen file. The
probe's `C_SRC` spans `plans/build_pmars_probe.py:151-171` (first line shared with the `C_SRC = r'''` assignment)
and is **21** content lines; my drafts say "canned 21-line C program" wherever a count appears. The entry draft
still carries the wrong count at `.ufo/waves/round-38/build/R38PkgEntry/entry.md:26,156,213` (`grep -n "14-line"`,
exit 0) — that file is the entry author's, not this seat's, so it is reported here for their fix, not edited.

### 3.7 Second-run byte equality is a commit claim I did not rerun

`e95cf55`'s subject asserts `second run byte-equal`; I read that line and did not execute the probe. My PROVINCE draft
attributes it to `e95cf55` ("the first recorded run `e95cf55` and a second run are byte-equal"), which is the
observed text, not a fresh observation of mine.

### 3.8 The reward path is read, not exercised

`test.sh:18-28`: `uvx … pytest … /tests/test_outputs.py -rA` then `if [ $? -eq 0 ]; then echo 1 > reward.txt`.
The probe imports the captured module and calls the four functions directly (`plans/build_pmars_probe.py:174-188`),
so the pytest/uvx path and the reward file are outside every case. Both my PROVINCE and SKILL drafts say this
explicitly so a later seat does not read `reward.txt` into the probe's receipt.

### 3.9 The empty-tree baseline fails by exception, not assertion

`receipt:4` carries `test_headless_no_x11:error=CalledProcessError`: with no binary, `ldd` exits non-zero with empty
stdout and `run_shell_command` re-raises (`test_outputs.py:12-15`). A reviewer comparing "do-nothing" against a
candidate must expect an error shape there, not an assertion message.

### 3.10 Upstream adjacent report on the oracle (routed, not rowed)

TB2 issue #59 ("`build-pmars` failing with oracle solution", open, 2026-04-13, `sam571128`) reports the oracle's
`apt-get install -pkg=version` pins failing in the container (`dpkg-dev=1.22.21` not found). It is about `solve.sh`,
not the four test functions, and this seat has no registry-row mandate. It is **not** in the PROVINCE draft; it is
named here so the seat that owns `corpus/SOURCES.md` and the entry's §Prior art can row or refuse it (the claims
route it: "to be re-opened and rowed or refused by a wave-1 seat", `plans/round-38-claims.md` §C2 limits).

## §4 Out of scope / not done

- The knowledge entry `corpus/knowledge/tb2-build-pmars-grader.md` (quotes, `## Requirement map`, `## Negative
  space`) — another seat's artifact; my drafts reference it but do not draft its rows.
- `corpus/SOURCES.md` rows S115/S116 — absent (§3.5); not written.
- Any edit to `PROVINCE.md`, `corpus/README.md`, `SKILL.md`, `corpus/SOURCES.md`, the gate, counters, probe, spec,
  dry table, captures or the C1 battery dir. `git status --porcelain` shows only untracked `.ufo/waves/round-38/*`
  paths; the drafts are the only files this seat wrote.
- No probe/counter/gate execution; no image, oracle or harness run; no second probe run; no network fetch other
  than the issue-#59 metadata read.

## §5 Scratch

`S=/fast/scratch/hyaku/kengaku-r38/R38PkgProse` was created for the P8 reproduction and removed before this report
was finished (`rm -rf -- "$S"`; `S` absent afterwards). Receipts live in the seat dir, not in scratch.

## §6 Artifact paths

- `.ufo/waves/round-38/build/R38PkgProse.md` (this report)
- `.ufo/waves/round-38/build/R38PkgProse/PROVINCE-round38.md`
- `.ufo/waves/round-38/build/R38PkgProse/README-frontier-r38.md`
- `.ufo/waves/round-38/build/R38PkgProse/SKILL-build-provenance-r38.md`
- `.ufo/waves/round-38/build/R38PkgProse/derived-labels.txt`

VERDICT: c2-prose-drafted-13-rows
