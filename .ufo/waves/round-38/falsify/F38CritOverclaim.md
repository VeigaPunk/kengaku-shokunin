# F38CritOverclaim — overclaims across round-38 prose (wave 2, falsify)

Seat: critic. Read-only on the lane; clone at `/fast/scratch/hyaku/kengaku-r38/F38CritOverclaim/lane`
(`git rev-parse --show-toplevel` = that path, `HEAD` = `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`,
`git status --porcelain | wc -l` = `0`). Frozen claims read first (`plans/round-38-claims.md`).
Receipts: `.ufo/waves/round-38/falsify/F38CritOverclaim/` (`probe-rerun.txt`, `nonelf-ldd-wrapper.txt`,
`nonelf-ldd-wrapper-probe.py`, `map-label-derivation.txt`, `map-label-derivation.py`, `upstream-refetch.txt`,
`upstream-Dockerfile-2fd12b88.txt`).

## Axes

- **calibration** — does each prose statement match its receipt and the frozen claim? (primary)
- **coverage** — does the prose claim more of the grader/benchmark than 22 synthetic cases can carry?
- **novelty** — is "first probed instance" consistent with the round's own prior-art ledger? (secondary)

## What I tested and did not falsify (calibration credit, before the findings)

| claim | location | command → output |
|---|---|---|
| probe reproduces byte-for-byte on a clean clone of the landed tip (entry falsifier b) | entry §The executed probe | `python3 plans/build_pmars_probe.py --lane . --work $S/probe` on the `--no-local` clone → `cases=22 observed_pass=7 observed_fail=15 mismatches=0`; `cmp` vs the committed receipt → `BYTE-EQUAL` (`probe-rerun.txt`) |
| re-fetch of both pinned URLs matches `SHA256SUMS` (entry falsifier a) | captures | `curl -sfL` `2fd12b88` → `test_outputs.py d9d2796d…f4e85`, `instruction.md 16068505…3b82`, both equal to the capture; `laude-institute` and `harbor-framework` serve identical bytes at the pin (`upstream-refetch.txt`), so "S100 is the same repository at the same commit" holds |
| 22 cases / 7 pass / 15 fail; 21-line `C_SRC`; zero-byte `src/dummy.c`; four base tags on all 22; narrow sets 3/4/5 | entry §Summary, §Requirement map | `awk '/^CASE/{n++} /observed=pass/{p++}'` → `cases=22 pass=7`; `C_SRC` lines 151-171 = 21; `stage_app` writes `b""`; my derivation script prints the carrier counts |
| the control-time run is disclosed honestly and does not taint pre-registration | entry:57-66 | predictions live in the frozen probe (`Case.predicted`, digest `32f0771c`, executed by P10 at control time), so the prediction set necessarily predates the first execution; only the author's *reading* was skipped. No finding |
| "second run byte-equal" | SKILL:582, README:451, SCORECARD:1345 | my independent re-run is byte-equal; wave-1 replays also byte-equal (`build/R38CritPytest.md:199`, `build/R38CritIndep.md:223`) |
| N21 "can only be killed as a mirror" | LOG:1120, lesson §Mistakes row 1 | `plans/round38_c1_verify.py:141` narrows `sums.splitlines()` to `[:1]` inside `any(...)`; the DEFECT set is monotone non-decreasing, so `ref DEFECT ∧ mutant ok` is unreachable — the explanation is sound |
| the `environment/Dockerfile:9` quote the entry marks "not captured" | entry §Contestable tags | fetched at the pin: line 9 is exactly `COPY warriors/flashpaper.red warriors/rave.red /app/` (`upstream-Dockerfile-2fd12b88.txt`, sha256 `ff0a9f76…8b25`); disclosure accurate. It is outside `SHA256SUMS`, so gate P3/P4 never sees it — operability note, not an overclaim |
| "the whole task can be passed by a fabricated artefact" | entry §Findings 1 | composition supported: four `P` + `test.sh:25-29` mapping (read) + `R38CritPytest` real-pytest parity 22/22. Not flagged |

## Findings

### O1 (high, calibration) — "a fabricated non-ELF artefact cannot pass it" is false; a 23rd state passes

**Attacks** `corpus/knowledge/tb2-build-pmars-grader.md:161`: "The X11 test fails closed on artefacts `ldd` cannot
read … so a fabricated **non-ELF** artefact cannot pass it" (universal clause), and `:82` "**Two different objects
are graded under the name `pmars`**".

**Counterexample** — the grader calls `ldd` by *bare name* through a shell (`test_outputs.py:53`), and Debian's
default `PATH` puts `/usr/local/bin` before `/usr/bin` — the same mechanism the entry itself uses for `path-split`.
Stage a **bash script** (not ELF) at `/usr/local/bin/pmars` plus a planted `/usr/local/bin/ldd`:

```
$ cd .ufo/waves/round-38/falsify/F38CritOverclaim
$ TMPDIR=<scratch> python3 nonelf-ldd-wrapper-probe.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin
harness rc=0
TEST test_pmars_works P
TEST test_headless_no_x11 P
TEST test_debian_source_used P
TEST test_built_from_source P
# PATH resolution inside the same sandbox:
/usr/local/bin/pmars
/usr/local/bin/ldd
ldd_rc=0
ALL_FOUR=True
```
(`nonelf-ldd-wrapper.txt`; same bwrap argv and `HARNESS_PY` as the frozen probe, capture digest `d9d2796d…`.)

So a non-ELF fabricated artefact passes all four tests; the `ldd` check fails closed only while `ldd` resolves to
the system one. The entry's own uncovered list already names "an `ldd` wrapper" — the positive universal
contradicts the limit one paragraph below it, and the object count is three (`pmars` bare, `ldd` bare,
`/usr/local/bin/pmars` absolute), not two. Related, undisclosed: `test.sh:10` sources `$HOME/.local/bin/env`
before pytest, so the verifier's `PATH` may prepend another writable directory ahead of `/usr/local/sbin`; the
probe models Debian's default order only (the `path-split` conclusion is unaffected).

**Impact** calibration (C2 prose), coverage (the `no-x11` reading "fails closed"). The frozen 22-case table, the
counter and every label are unaffected — this is prose-level.

**Minimal safe correction** replace the sentence with: "the X11 test fails closed on artefacts `ldd` cannot read
**only while `ldd` resolves to the system one**; an `ldd` planted earlier on `PATH` defeats it (wave-2
counterexample, outside the frozen table)"; and change "Two different objects" to "three names are resolved".

### O2 (medium, calibration) — the seven "derived" labels are four statistics, and one "not vacuous" reading is contradicted

**Attacks** `entry:151` "All seven labels are `partly`, and that is the round-38 finding at map level"; the header
claim "computed over **all** violating cases (round-37 closure D2)"; `entry:157` "`empty-tree` fails, so the line is
not vacuous — it fails only through the binary-presence check at `:24`".

**Counter-evidence** — deriving the labels from the receipt with the entry's own rule:

```
$ python3 .ufo/waves/round-38/falsify/F38CritOverclaim/map-label-derivation.py \
    /home/vgpnk/Projects/shokunin/kengaku-shokunin
tags sharing an identical carrier set AND identical fail-side set:
  carriers=22 fail_side=15 labels=['from-source', 'debian-source', 'extract-to-app', 'debugger-works']
  carriers= 3 fail_side= 2 labels=['no-x11']
  carriers= 4 fail_side= 3 labels=['install-path']
  carriers= 5 fail_side= 4 labels=['results-format']
sole case carrying all seven tags: ['empty-tree']
from-source: test_built_from_source (:73-85) on violating cases: P=18 F=4 | fails only in:
  ['empty-tree', 'src-no-c', 'no-src-dir', 'pmars-dir-elsewhere']
```
(`map-label-derivation.txt`.) Four of the seven labels are one measurement repeated: identical 22-case carrier set,
identical 15-case fail side. The single do-nothing case carries every tag, so `unenforced` is unreachable for any
tag in this table and the three-valued rule degenerates to two. `empty-tree` is `Art(kind="absent"), ()`
(`plans/build_pmars_probe.py:104-105`) and is `FFFF`, so it also fails `:63` and `:76`: "fails only through …
`:24`" is wrong, and a case that fails on presence/tree-shape is no evidence that `from-source` is non-vacuous —
the entry's own negative space says no line reads a build, and `test_built_from_source` passes on 18 of 22
violating cases. The map's `install-path` row cites `silent-binary` as the fail direction while `entry:191-193`
says that case "fails lines 7 and 9, not line 3's install clause"; the right witness `nonexec-binary`
(`receipt:17`) is omitted.

**Impact** calibration — the Q28/D2 fix claim ("derived, not chosen … over all violating cases") is mechanically
true but does not discriminate a tag-enforcing failure from an unrelated one. Labels, counter (`V7 rows=7
tags=7`) and frozen tags unaffected.

**Minimal safe correction** add a "fail-side witness assertion" column, cite `nonexec-binary` for `install-path`,
and replace the map-level sentence with: "no line of the instruction is fully enforced; `from-source` is enforced
by no assertion — `test_built_from_source` passes on 18/22 violating cases and its four failures are tree-shape
cases — and four of the seven labels share one carrier set."

### O3 (medium, calibration) — the SKILL decision table mis-states three of its thirteen mechanisms

**Attacks** `SKILL.md` §Decision table, rows 2, 11 and 18.

**(a) Row 2, `:832`** — "`exists()` only — no execute bit, **no real invocation of the installed file**
(`:24`, `:53`)". The row's own witnesses are produced *by* that invocation: `receipt:17`
`nonexec-binary … tests=FPPP … test_pmars_works:error=CalledProcessError`, `receipt:18` `silent-binary …
tests=FPPP`; `test_outputs.py:27-28,44` run bare `pmars`, which resolves to `/usr/local/bin/pmars` when nothing
earlier on `PATH` shadows it (my sandbox: `command -v pmars` → `/usr/local/bin/pmars`). The entry agrees:
`entry:227` "the behaviour tests do gate the installed file". So the install *assertion* is `exists()`-only, but
the file is invoked and its stdout graded.

**(b) Row 11, `:836`** — "`ldd` must print something". The code is
`assert lib not in ldd_output` (`test_outputs.py:57`); empty output satisfies it. The script/static cases fail
because `check_output` raises on a non-zero exit with empty stdout (`:12-16`), not because output is required.
My O1 receipt is the direct falsification: an `ldd` that prints nothing and exits 0 makes
`test_headless_no_x11` `P` (`nonelf-ldd-wrapper.txt`).

**(c) Row 18, `:843`** — "the first failure being `test_headless_no_x11:error=CalledProcessError`". In file order
the first failure is `test_pmars_works` (`receipt:4` shows `FFFF` with the error suffix only on
`test_headless_no_x11`); `test_headless_no_x11` is the first *error*, not the first failure, and `empty-tree`
fails `:24` by `AssertionError`.

**Impact** calibration — the SKILL table is the surface a later reviewer cites instead of re-reading the grader;
(a) and (b) both invert which assertion actually carries the verdict.

**Minimal safe correction** (a) "`Path.exists()` only, no execute-bit check and no absolute-path invocation; the
bare `pmars` calls resolve through `PATH`, so a non-runnable or silent install fails on **behaviour**"; (b) "`ldd`
must exit 0 and its stdout is then string-scanned; a non-zero exit with empty stdout re-raises, which is what
makes a script or a `-static` binary red"; (c) "the first failure is `test_pmars_works` (`AssertionError` at
`:24`); `test_headless_no_x11` is the first *error*".

### O4 (medium, novelty/calibration) — "first probed instance" drops the one upstream signal that could refute it

**Attacks** `entry:294` "Two prior-art notes specific to this task", `entry:300` "**The nearest prior statement is
an LLM audit**", `entry:314` "**"first probed instance for TB2 `build-pmars`"**", and `LOG.md:1132` ("Prior art:
TB2 #59 …; an LLM audit …; TB2.1 changed the instruction").

**Counter-evidence** the entry's own scout recorded a nearer hit and its limit:

```
$ sed -n '27p' .ufo/waves/round-38/build/R38ScoutPriorArt.md
| 13 | …/terminal-bench-2-1/pull/118 … | github-actions comment: "Reward hacking 🟡 … `e4f67b8d` ·
  build-pmars · judge verdict" … | a judge flagged one build-pmars trial as reward hacking. The verdict page
  returned HTTP 404 … | **unknown** … Cannot be rowed; may not concern the grader. |
$ grep -c "118" corpus/knowledge/tb2-build-pmars-grader.md
0
```
(the scout's `## Limits` repeats it: "a flagged trial remains an unexplained signal, not a hit about the grader").
A judge-flagged reward-hacking trial on this task is nearer than a static LLM audit and bears directly on
"first"; the six-state lexical negative is otherwise sound (`none of the 14 hits reports canned output, the
dlopen blind spot, …` survives). Also "Two prior-art notes" introduces four bullets.

**Impact** novelty (the only novelty-shaped statement the entry makes, despite saying "no novelty claim is
filed"), calibration (prior-art ledger completeness).

**Minimal safe correction** add the #118 bullet with the 404 and the scout's limit; qualify: "first executed,
sourced probe in this lane's search; one upstream `build-pmars` trial is judge-flagged reward hacking with the
verdict unretrievable, so an earlier exploit is not excluded"; fix the "two notes" count; mirror the clause in
`LOG.md:1132`.

### O5 (low, coverage/calibration) — "89 carry `tests/test.sh`" has no in-repo count

**Attacks** `PROVINCE.md:303` "…speak for the remaining 85 TB2 task graders (89 carry `tests/test.sh`; 4 are
read)" (inherited verbatim from `PROVINCE.md:276`).

**Counter-evidence** the registry's own anchors count directories and manifests only: S079 "92 root entries at
that commit, of which 89 are task directories carrying a task.toml"; the validity checklist re-derives "89 task
directories and 89 `task.toml` files" and never counts `tests/test.sh`. The only `test.sh` registry rows are S106,
S109, S113, S115 — four single files. Likely true, but ungrounded as written.

**Impact** coverage — a universal over 89 directories, in the paragraph that defines the lane's scope boundary.

**Minimal safe correction** "(89 task directories at the pin; 4 graders read)".

### O6 (low, calibration) — two count/wording defects in the summary prose

**Attacks** `corpus/README.md:71` "scores four pytest functions — binary presence, two debugger address lines, a
start-anchored `Results:` match, an `ldd` string scan and a one-level `/app/pmars-*` tree" (five mechanisms
listed for "four functions": the first three are one function, and the last item is two), and `entry:93` "every
passing case's output comes
from a program that ignores its `argv`".

**Counter-evidence** `test_outputs.py` has four functions — `test_pmars_works` (presence, two debugger checks,
battle), `test_headless_no_x11` (one looped assertion), `test_debian_source_used` (two), `test_built_from_source`
(three) — so README's five-item list is not "four"; `C_SRC` line 166 is `for (int i = 1; i < argc; i++) if (strcmp(argv[i], "-b") == 0) battle = 1;` and the
script variant loops over `"$@"` — both read `argv` to branch on `-b`. What is never read is the *warrior files*.

**Impact** calibration (reader trust in the index row / entry prose). Substantive claims unaffected.

**Minimal safe correction** README: "four pytest functions: one over the installed binary's presence and stdout
(debugger addresses, `Results:` prefix), one over `ldd` stdout, and two over the `/app/pmars-*` tree". Entry:
"never opens the warrior files it is handed".

### O7 (low, calibration) — "gate behaviours attributed 21/22" precedes the review the round says it needs

**Attacks** `LOG.md:1115` "gate behaviours attributed 21/22 (honest stop)", `SCORECARD.md:1334` (same title).

**Counter-evidence** the round's own lesson, `corpus/lessons/round-38.md:40-44`: battery38 modules are imported
into the counter's process, a monkeypatch "reaches `killed=20` with `wrong=0 sidechannel=0`", and "The landed
battery's code is reviewed by wave-2 seats; the counter's predicate alone is not evidence that a kill is honest".
The titles therefore assert attribution on a predicate the round itself says is insufficient, before that review.
The detailed lines (`killed=21 survived=1`, `PREDICATE C1 fail`) are accurate.

**Impact** calibration — the round title is the line most likely to be quoted without its body.

**Minimal safe correction** "21/22 under the attributed kill rule (battery38 code review pending at landing;
wave 2)".

## Per-file audit summary

| file | sections read against the receipt | outcome |
|---|---|---|
| `corpus/knowledge/tb2-build-pmars-grader.md` | Summary, four structural consequences, `## Located quotes`, `## Requirement map` + per-line reading, contestable tags, `## The executed probe` groups, 8 findings, `## What the probe does not show`, prior art, negative space, falsifier | supported except O1 (`:161`, `:82`), O2 (`:151`, `:157`, `install-path` citation), O4 (`:294`, `:300`, `:314`), O6 (`:93`) |
| `PROVINCE.md` round-38 paragraph | Core addition, scope refusals, disclosed ordering, adjacent | supported except O5 (`:303`) |
| `SKILL.md` build-provenance section + row 582 | invocation rule, decision table (13 rows), exit-code cell, receipt line cite | supported except O3 (rows 2 `:832`, 11 `:836`, 18 `:843`); `receipt:26` and the `receipt:5/8/9/10/11/12/13/16/17/18/19/22/23/24` cites are correct |
| `corpus/README.md` | index row 71, Frontier bullet 263, coverage bullet 291-303, evidence list 450-451 | supported except O6 (`:71`); "4 of 89", "not breadth", the 21-line/zero-byte description and the 3/4/5 narrow-tag counts all hold |
| `SCORECARD.md` | round header 1334, C1 row, C2 row 1345, capability rows 1355, no-harm block | supported except O7 (`:1334`); the C2 counting command and the 44→45 / 107→109 deltas match `measure-final.txt` |
| `LOG.md` | header 1115, C1 bullet, C2 bullet 1126-1133, prior art sentence 1132, tool-use bullet | supported except O4 (`:1132`) and O7 (`:1115`); "twelve wave-1 executor seats, 22 fixtures" holds (`ls plans/battery38/*.py` = 12; 86−64 = 22) |

Universal clauses flagged: entry `:161` ("cannot pass"), `:93` ("every passing case … ignores its `argv`"),
`:283` ("They were fixed before the first run" — defensible, see table), PROVINCE `:303` ("89 carry"), SKILL
`:832` ("no real invocation"), and the map's "no line … fully enforced" (supported, and if anything understated
for `from-source`).

Class claims: the entry makes none above "one edge class new to the lane's executed sample" (scoped, supported);
the only priority claim is "first probed instance" (O4), which the entry simultaneously disclaims as "no novelty
claim". No universal about TB2 graders beyond "the other 85" was found beyond O5. Count: seven findings;
O2, O3 and O6 each bundle two or three distinct mis-statements (the map's four-labels-one-statistic sentence,
the `install-path` citation and the "not vacuous" reading; SKILL rows 2, 11 and 18; README's four/five count and
"ignores its `argv`"), so the defective-statement count is 10.

VERDICT: overclaims-7
