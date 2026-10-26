# R37CritC2Counter — attacking `plans/round37_c2_verify.py`

Seat: R37CritC2Counter (critic, round 37 wave 1, hyaku run 8, 2026-10-26).
Contract read first: `plans/round-37-claims.md` (frozen, §C2), then the counter in full, then
`plans/pkg_gate.py`, `plans/pkg-spec-r37.json`, `plans/git_webserver_probe.py`, the receipt, the dry table and
all six captures. Nothing in the lane was edited; every experiment ran in a scratch clone.

**One-line result.** The cheapest package that satisfies V1–V7 is about 2 KB of filler: eight verbatim
fragments with meaningless claim cells, three registry rows whose *teaches* cells say "placeholder words", a
one-row requirement map, and prose that states the **exact inverse** of the receipt. It prints
`checks=7 defects=0` / `PREDICATE C2 pass` / exit 0. V7's own defence sentence ("A filler entry whose quotes
are verbatim but whose claims are not tied to the executed verdicts fails here.",
`plans/round37_c2_verify.py:28-29`) is false: a one-row map can cite one failing case and label all of
instruction.md:1-9 `enforced`. A second, independent defect: the spec the counter calls "the frozen
template" (`plans/round37_c2_verify.py:12`) is the one frozen input the counter never digests, and it supplies
P10's command — so a fabricated receipt passes as `probe_rerun=byte-equal` without the probe running.

## Setup (every path absolute)

```
S=/fast/scratch/hyaku/kengaku-r37/R37CritC2Counter; export TMPDIR=$S/tmp; mkdir -p "$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/fx/lane"
git -C "$S/fx/lane" rev-parse --show-toplevel   # -> $S/fx/lane  (checked before any write)
git -C "$S/fx/lane" rev-parse HEAD             # -> 44b7298ae1e03791173097cef0e898285f238870
```
Pristine copy `$S/fx/lane-pristine`; one `cp -a` per variant; edits applied by
`.ufo/waves/round-37/build/R37CritC2Counter/build_filler.py`; index-only `git -C "$D/<v>" add -A`
(no commit, no checkout, no reset). Each variant scored with
`cd "$D/<v>" && TMPDIR=… python3 plans/round37_c2_verify.py --lane . --work "$S/work-<v>"` (~53 s wall each;
the probe's 22 bwrap cases dominate). Full transcripts: `run-v*.txt` beside this report.

Baseline on the untouched clone: `checks=7 defects=4` (V2,V3,V4,V7), exit 1, matching
`claims/control-c2-nothing.txt`. P10 ran here (genuine receipt, `probe_rerun=byte-equal bytes=8443`),
so the probe is reproducible on this host and P10's machinery works. That is what makes the filler result
below meaningful: the same host, the same frozen inputs, a passing package.

## Variant table (all at lane tip 44b7298, all in scratch clones)

| id | change | V1 | V2 | V3 | V4 | V5 | V6 | V7 | predicate | exit |
|---|---|---|---|---|---|---|---|---|---|---|
| v1-filler | 8 junk quotes + one-row map + inverse prose; frozen spec, genuine receipt | ok | ok | ok | ok | ok | ok | **ok** | `checks=7 defects=0` `pass` | **0** |
| v2-map | two rows, both labels inverted (1-6 enforced, 7-9 unenforced) | ok | ok | ok | ok | ok | ok | **ok** | `checks=7 defects=0` `pass` | **0** |
| v3-receipt | v2 + one receipt line `observed=fail`→`pass`, summary adjusted | ok | **DEFECT** | ok | ok | ok | ok | ok | `checks=7 defects=1` `fail` | 1 |
| v4-spec | v2 + `probe_cmd` replaced by a `python3 -c` cat of the receipt | ok | ok | ok | ok | ok | ok | ok | `checks=7 defects=0` `pass` | **0** |
| v5-fabricated-spec | v1 + every `observed=fail`→`pass`, `match=yes` kept, summary `22/22/0` + v4's spec edit | ok | ok | ok | ok | ok | ok | ok | `checks=7 defects=0` `pass` | **0** |
| v6-fabricated-realprobe | v5's receipt, unmodified spec | ok | **DEFECT** | ok | ok | ok | ok | ok | `checks=7 defects=1` `fail` | 1 |
| v7-zeroreading | no claim at all; 8 quotes only from `test.sh`/`task.toml`/`solve.sh`; one-row map | ok | ok | ok | ok | ok | ok | ok | `checks=7 defects=0` `pass` | **0** |

`v1`, `v2`, `v7` leave **every frozen input byte-identical**: `plans/pkg-spec-r37.json` sha256
`4c61d103cff74021fec4dcedb27b6f5d85a3b5d6b11c1b4eda7df0ebe909c9b6` (= `claims/frozen-digests.txt`),
receipt sha256 `835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8` (the committed one),
probe/dry/captures untouched (V5 ok, V1 ok). The only files added or changed are the entry, three
`corpus/SOURCES.md` rows and `corpus/README.md`.

## Counterexample A — the cheapest passing package (v1)

Entry: `.ufo/waves/round-37/build/R37CritC2Counter/entry-v1-filler.md`, sha256
`2f72f7d8ae08c24e2713d1464637542ba1728fe98a80c6c6f817819867dafd8e`, 2545 bytes. Prose, verbatim:

> "the push runs under `expect` and its exit status decides the verdict, so a file served with no repository,
> hook or push is rejected; the status and the body are read from the same request; curl runs with `-L` and
> with a timeout; trailing whitespace, upper case, a carriage return and a byte-order mark are normalised
> before the comparison; and a body that merely contains the text `TEST PASSED` fails"

Six inversions of six receipt observations, one sentence each:

| entry claims | receipt (committed) |
|---|---|
| push status decides; static file rejected | `CASE static-file-no-git … observed=pass` — "a file served with no repository, hook or push" |
| status and body from the same request | `CASE status-then-content-split … observed=pass` — "status and content come from two separate requests" |
| curl with `-L` | `CASE redirect-301 … observed=fail` — "curl runs without -L" |
| curl with a timeout | `CASE slow-server-3s … observed=pass` — "curl is run without a timeout" |
| whitespace/case/CR/BOM normalised | `CASE capitalised|trailing-space|crlf|bom … observed=fail` |
| a `TEST PASSED` body fails | `CASE token-in-body … observed=pass` |

Requirement map (the whole table):

```
| Instruction lines | Verdict | Receipt cases |
|---|---|---|
| `instruction.md:1-9` | enforced | `no-server` |
```

V7 accepts it because `no-server` is observed `fail` and the range covers 1-9; it never asks whether
`no-server` (a case whose own note is `verify.sh:57-59 — nothing listens on :8080`) says anything about lines
1-6. One row, one citation, all nine lines "enforced": the reverse of the receipt's headline result, which
V7's docstring names as its target property.

Quotes (8 rows, `## Located quotes`): canary comment, canary GUID, `import subprocess` call, `pytest` runner
line, the `task.toml` description, an `apt-get` line, a `try_files` line, one `verify.sh` echo. Every quote is
verbatim and every claim cell is the word `filler`; P3/P4 are satisfied by copying fragments, not by reading.

Registry rows (`SOURCES-v1-rows.md:126-128`), all three clauses of `P6` green (`rows=3 bad=0`):

```
| S111 | filler — <raw url>/tests/test_outputs.py | code | A | filler scope 1 | sha256 526aee…6b37 | filler teaches cell 1 placeholder words that carry no content at all | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-git-webserver-grader.md |
```
The source description, the scope and the teaches cell are filler; only the URL, the digest and the used-by
path are real. `P6` counts words (`min_teaches_words=8`) and distinctness, never content.

README (`README-v1.md:70,234`): index row `| \`knowledge/tb2-git-webserver-grader.md\` | filler one-line
description | S111, S112, S113 |` and bullet `- filler: knowledge/tb2-git-webserver-grader.md
evidence/round37/git-webserver-probe.txt`; `P8 ok index_rows=44 knowledge_files=44`.

Counter output (`run-v1-filler.txt`):
```
V1 ok listed=6 bad=0 extra=0
    gate: P3 ok rows=8 distinct_quotes=8 distinct_lines=8 out_of_word_range=0
    gate: P4 ok checked=8 bad=0 first=0
    gate: P7 ok source_lines=3 bad=0 first=0
    gate: P8 ok index_rows=44 knowledge_files=44 bad=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=8443
    gate: defects=0
V2 ok gate_exit=0
V3 ok rows=3 bad=0
V4 ok cases=22 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=1 bad=0
checks=7 defects=0
PREDICATE C2 pass
exit=0
```

## Counterexample B — zero reading (v7)

`entry-v7-zeroreading.md` (sha256 `3963ef5f01705804c4764a6d973911587d0169d095705e79fc40f0051ec3ac91`,
1841 bytes) states **no claim at all** ("Nothing here describes the grader."), quotes only `test.sh:10`,
`task.toml:6,18,29,35`, `solve.sh:1,8,53` — none of the three source rows S111–S113 — and still passes
`checks=7 defects=0`. So the quote clauses carry no requirement that a quote comes from the graded artefact;
`P5` pins six captures and `P4` accepts any verbatim fragment of any of them. It also passes `P7` with a
**Negative space** section reading `No falsifier is named.` — `c_provenance` tests
`(?i)falsifi(er|ed|es|ability)` (`plans/pkg_gate.py:229`), which the clause's own negation matches.

## Counterexample C — map labels right, lines wrong (v2)

`entry-v2-map.md` (sha256 `857b05327b341ec84e6127e41b424ec00a4c85321ef3bf8fd5acfe93f08e0610`):

```
| `instruction.md:1-6` | enforced | `capitalised` |
| `instruction.md:7-9` | unenforced | `static-file-no-git` |
```
Both labels are inverted relative to what the cited cases say about those lines: `capitalised` is a
case-sensitivity failure of line 9, and `static-file-no-git` is the pass that shows lines 1-6 are **not**
enforced. V7 only requires "an `enforced` row cites a case observed `fail`" — label↔verdict agreement, never
line↔case agreement. `V7 ok rows=2 bad=0`, predicate pass.

## Receipt-side attack — the required control, and the hole it exposes

**R1 (frozen spec, edited receipt): caught.** v3 = v1's filler package with one receipt line changed
(`CASE no-server … observed=fail` → `observed=pass`) and the summary adjusted so V4 still agrees. Result
(`run-v3-receipt.txt`): `V4 ok cases=22 mismatches_named=0/0 bad=0`, `V7 ok rows=2 bad=0`, and
`gate: P10 DEFECT fresh probe output is not byte-equal to the receipt` → `V2 DEFECT gate_exit=1`,
`checks=7 defects=1`, exit 1. P10 does its job **while `probe_cmd` is the frozen one**.

**R2 (spec edit, fabricated receipt): passes.** v5 flips every `observed=fail` to `observed=pass` **and keeps
`match=yes`**, so 13 lines read `predicted=fail observed=pass match=yes`, and the summary becomes
`cases=22 observed_pass=22 observed_fail=0 mismatches=0` (receipt sha256
`149b8ec62031ab53338acb488a31cc2de0dc03e65a0c7acff0c04f1bed376ac0`, vs the genuine
`cases=22 observed_pass=9 observed_fail=13 mismatches=0`, sha256 `83550712…`). One edit to
`plans/pkg-spec-r37.json` (sha256 `ce09c3212ad03f8793b91815741dddcb85f21711d88895ba9f3c32e2da10fca0` v frozen
`4c61d103…`):

```
-  "plans/git_webserver_probe.py",
-  "--lane",
-  "."
+  "-c",
+  "import pathlib,sys;sys.stdout.write(pathlib.Path('corpus/evidence/round37/git-webserver-probe.txt').read_text())"
```
`P10` then prints `gate: P10 ok probe_rerun=byte-equal bytes=8443` and the predicate is
`checks=7 defects=0` / `pass` / exit 0 — with the probe never executed, a receipt that contradicts the
executed probe, `V4 ok` on it, and `V7 ok` on a map keyed to the fabricated verdicts. The counter's own
docstring relies on this very file ("the frozen template", line 12; "authenticity rests on P10", line 13)
and never compares it with the freeze digest `4c61d103…` that `claims/frozen-digests.txt:4` records. C1's
sibling counter does pin its instrument (`GATE_SHA256` at `plans/round37_c1_verify.py:58`, checked at
`:291`), so the asymmetry is local, not a house rule.

**R3 (isolation): the spec edit is the enabler.** v6 = v5's fabricated receipt with the unmodified spec →
`gate: P10 DEFECT fresh probe output is not byte-equal`, `V2 DEFECT`, exit 1. So R2 is not a second way to
fake a receipt; it is the missing digest check that turns P10 into a no-op.

**R4 (V4's bookkeeping is self-reported).** Even without the spec edit, v3/v5's receipts carry
`match=yes` on lines whose `observed` contradicts `predicted`. V4 parses `predicted=` only incidentally: it
counts `match=NO` occurrences and compares the summary to *the observed tokens it just read*
(`plans/round37_c2_verify.py:134-146`). It never recomputes `match` from `predicted` vs `observed` and never
checks `predicted` against the dry table, so `mismatches=0` is a claim the receipt makes about itself. Only
P10 stops it; with R2's spec hole, nothing does.

## Impacted axes

- **calibration (the axis this round is judged on).** The round-37 C2 admission condition is
  `checks=7 defects=0` measured on the landing tip. That condition is now demonstrated reachable by a package
  with zero understanding (v1, v7) using only frozen inputs, and by a package with a fabricated receipt (v5)
  using one editable input. Any C2 landing that reports `defects=0` inherits this uncertainty; the count of 7
  checks is not a count of 7 independent garrisons.
- **coverage.** The executed probe itself stands (V5, P10 with the frozen command, byte-equal on this host);
  the *entry* is what is unchecked. The claim's sentence "admitted with an executed probe" stays true; the
  implied "admitted because the entry records what the probe showed" does not.
- **operability.** A future seat can satisfy the same counter in ~2 KB and cannot tell from the output that it
  did; the counter should not be read as an entry-quality signal.
- **novelty / depth / freshness / adjacency.** Untouched by this finding.
- **Hidden regression to flag for the integrator.** If C2 lands with a map like v1's (a one-row `1-9
  enforced`), the round-36 routed item 3 defect (shape-only checking admitted a junk package) returns in the
  semantic layer, and the round-38 counter family inherits the same V7.

## Smallest safe corrections (for the L1; the frozen counter itself is not touched by this seat)

1. **V7 provenance (≈10 lines, no new data).** Derive the label from the receipt's own per-case instruction
   citation instead of from an arbitrary case's verdict: every `--` note that names `instruction.md:a-b` is
   already in the receipt (`static-file-no-git` → `instruction.md:1-6`, `wrong-port-8081` →
   `instruction.md:7`, `exact-no-newline` → `instruction.md:9`). Require each row's range to equal the range a
   cited case's note names, and the label to equal that case's observed verdict. v1, v2 and v7 all go red
   under this rule; the honest map does not (1-6 `unenforced` by `static-file-no-git`, 7 `enforced` by
   `wrong-port-8081`, 9 `partly` by `exact-no-newline` + `capitalised`).
2. **Pin the spec (2 lines).** Compare `plans/pkg-spec-r37.json` against `4c61d103…` before V2/V3/V4/V7 read
   it, exactly as `plans/round37_c1_verify.py:58,291` does for the gate. That closes R2 and restores P10 as
   "authenticity rests on P10".
3. **Recompute the receipt's own bookkeeping (≈4 lines).** In V4, recompute `match` from
   `predicted` vs `observed` and require the receipt's `match=` and `mismatches=` to agree with `predicted`
   and the frozen dry table. That closes R4 independently of R2.
4. **Minor.** Require the **Negative space** falsifier sentence not to be its own negation (v7's
   `No falsifier is named.` passes `plans/pkg_gate.py:229`), and require at least one quote from each of
   S111–S113 (v7 quotes none).

Items 1 and 2 are the smallest set that makes v1, v2, v5 and v7 red while leaving an honest package green.

## What I did not test (limits of this review)

- I did not run the oracle (`solve.sh`) or any real git push; the probe's stated limit (no oracle run) is
  untouched by this seat.
- I did not test import shadowing inside `plans/` (a `plans/re.py` on `sys.path[0]` when the gate or the probe
  is executed as a script), which would attack P10 and the gate without touching the spec; it is a live
  surface but a different, larger hole than the one assigned.
- I did not test a renamed-fixture analogue (C2 has no fixture battery); the renamed-run requirement is C1's.
- The bwrap probes are host-dependent; every claim above is from this host (Python 3.14.8, uv
  `--with biopython==1.85` cached, `/usr/bin/bwrap` present). Scratch `$S` was removed after the receipts in
  this directory were written.

VERDICT: cheapest-filler-c2-0-defects
