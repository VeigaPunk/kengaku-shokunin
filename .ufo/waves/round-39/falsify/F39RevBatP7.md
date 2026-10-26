# F39RevBatP7 — p7m39 (M04, two source lines for one sid) — wave 2 falsify review

Lane tip measured: `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` (branch master). Scratch
`/fast/scratch/hyaku/kengaku-r39/F39RevBatP7` (deleted after receipts copied out; contents listed at bottom).
Fixture rule honored: clone verified `toplevel: /fast/scratch/hyaku/kengaku-r39/F39RevBatP7/lane`,
`head: a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`, `status: 0 dirty paths` (proc `verify-clone`); every git
call named `-C "$S/lane"`; no lane file written; no commit anywhere.

## Findings by severity

**No calibration defects found.** Three observations, none affecting the kill, the predicate, or attribution:

1. **(info) The `pinned == other` guard is stricter than the kill requires.** `plans/battery39/p7m39.py:52-53`
   `raise RuntimeError("second source url must differ from the pinned one")` forbids the degenerate
   second line that cites the pinned URL itself — but E2 below shows that variant also kills M04. The
   landed fixture therefore cannot express one valid kill shape; harmless (the fixture that exists kills),
   and the guard doubles as a build-time tripwire (E5b).
2. **(info) Docstring witness label mismatch.** `plans/battery39/p7m39.py:13-14` cites "`W-X15`
   (`.../F38XMutP/witness-run.txt`: `ref_defects=P7,P9 mut_defects=P9`)"; the on-disk line is
   `witness-run.txt:3` `WITNESS wx15 mutant=X15 ref_rc=1 ref_defects=P7,P9 mut_rc=1 mut_defects=P9
   flip=P7->P7-ok ok` — label spelled `wx15`, substance matches exactly. Cosmetic; the counter never
   reads witnesses (`round39_c1_verify.py:41` docstring) so this cannot move the predicate.
3. **(info) Corpus bytes are load-bearing, every failure mode loud** — see Q3.

## Q1 — Is the P7 DEFECT caused by the duplicate line alone? **Yes.**

Reference gate builds `prov` from every `source:` match: `plans/pkg_gate.py:218`
`prov.setdefault(m.group(1), []).append(m.group(2))`, then `plans/pkg_gate.py:220`
`if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:` — whole-list compare, so ANY second
URL-bearing `source: S105` line defects P7. M04 replaces that test first-element-only
(`plans/round39_c1_verify.py:133` `if (prov.get(sid) or [""])[0] != p.spec["raw_base"] + row["upstream"]:`).

The landed fixture deviates from the genuine package in exactly two ways: the inserted line
(`p7m39.py:54-55`, citing S107 `instruction.md`) and staging (`ctx.git_add`, keeping P9 green).

- E4 (clause diff, same fixture dir, ref gate vs M04 gate): `reference rc=1 | M04 rc=0 |
  stdout identical: False`; unified diff `e4-clause-diff.txt` changes ONLY
  `-P7 DEFECT source_lines=3 bad=1 first=S105: source line not the pinned url` /
  `+P7 ok source_lines=3 bad=0 first=0` and `-defects=1` / `+defects=0`; P1-P6, P8 (`index_rows=46
  knowledge_files=46`), P9 (`untracked=0`) identical and ok; stderr empty both runs
  (`e4-ref-stdout.txt`, `e4-m04-stdout.txt`, `e4-stderr.txt`).
- E3 control (staged genuine, NO second line, `p7m39ctl_staged_genuine.py`): counter dev run
  `python3 plans/round39_c1_verify.py --lane . --only M04 --battery-dir "$S/batvar" --work "$S/e23-work"`
  prints `FIXTURE p7m39ctl-staged-genuine expect=accept declared=- observed_rc=0 observed_defects=- ok`
  (`e23-ab.txt`). Staging alone leaves P7 green, so the inserted line is necessary; E4 shows it is
  sufficient; no other clause moves. The docstring claim "no other DEFECT clause"
  (`p7m39.py:23-24`) is verified.

## Q2 — Would the fixture still kill if the second line were the pinned URL? **Yes — demonstrated.**

E2 (`p7m39var_same_url.py`, identical build except `second` cites `pinned` itself, guard bypassed): same dev
run prints `FIXTURE p7m39var-s105-same-url-twice expect=reject declared=P7 observed_rc=1
observed_defects=P7 ok` and `MUTANT M04 P7 silence killed by=p7m39var-s105-same-url-twice`
(`e23-ab.txt`; `MUTANTS total=1 killed=1`; the control fixture did not exhibit, confirming attribution to
the two-line variant). Mechanism: reference list-compare `[pinned, pinned] != [pinned]` still defects P7;
M04 reads element 0 only. Kill rule satisfied (`round39_c1_verify.py:243`
`return clause in ref[1] and clause in declared and clause not in mut[1]` under direction
`round39_c1_verify.py:21`). So the kill does NOT depend on the second URL differing; the landed guard
(findings #1) merely excludes this variant.

Landed kill re-verified: E1 full run `python3 plans/round39_c1_verify.py --lane . --work "$S"` on my own
clean clone prints `FIXTURE p7m39-s105-two-source-lines expect=reject declared=P7 observed_rc=1
observed_defects=P7 ok`, `BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0`,
`MUTANT M04 P7 silence killed by=p7m39-s105-two-source-lines`, `MUTANTS total=7 killed=7 survived=0
invalid=0 null_detected=0`, `PREDICATE C1 pass`, `exit=0` (`e1-full-counter.txt`) — same lines as the
frozen landing measurement `measure-final.txt:94,95,99,103,104`.

## Q3 — Dependency on corpus bytes a later round's edit would break: **load-bearing, always loud.**

`ctx.genuine_package` copies the committed round-35 package from lane bytes (`round37_c1_verify.py:198-206`;
entry `corpus/knowledge/tb2-protein-assembly-grader.md`, raw_base `.../protein-assembly/`, S105
`tests/test_outputs.py`, S107 `instruction.md` — spec extraction receipt in `e4-built.json` run log). None of
these corpus bytes are in the 26 pins; the fixture rides on them:

- **Entry `source: S105 ` line count** — guard `p7m39.py:49`
  `raise RuntimeError(f"expected exactly one {SID} source line, found {len(hits)}")`. E5a (planted a second
  native S105 line in the entry, fresh clone at tip): `--build-module ... rc=1` with exactly that
  RuntimeError (`e5a.err`). Same shape the round-39 lesson already caught once:
  `corpus/lessons/round-39.md:44` "the next C1 run printed `SETUP module battery38/p7m.py failed to build
  (rc=1) ... expected exactly one 'recheck:', found 5`" — the counter's SETUP refusal (exit 2) is the
  designed catch.
- **S105/S107 rows and distinct upstreams** — `p7m39.py:50-51` indexes `spec["rows"]` (missing row =
  child KeyError, loud); equal upstreams trip `p7m39.py:53` (`e5b.err`, `rc=1` with that RuntimeError).
- **Whole genuine package defect-free** — any future corpus defect makes `observed_defects != ["P7"]`
  and the fixture prints WRONG (`wrong=1` → predicate fail); the lesson records this shape as
  `wrong=51` (`corpus/lessons/round-39.md:47`).
- **Spec↔corpus desync** — E5c (S105 upstream drifted to `tests/test_outputs.py.drift`, entry unchanged):
  counter exits 2 before p7m39 even runs — `SETUP module battery38/p6m.py failed to build (rc=1):
  RuntimeError: S105 source cell carries the pinned url 0 times, wanted exactly one` plus
  `PINS total=26 mismatched=1 first=plans/pkg-spec-r35.json` (`e5c-drift.txt`).

No silent path: a corpus edit that defeats the kill necessarily keeps P7 DEFECT under M04 too
(mutant and reference then agree on `prov[0] != pinned`), which prints `SURVIVED` and reds
`MUTANTS survived`; drift that changes the observed defect set reds `wrong`; drift that breaks the build
reds SETUP exit 2. The kill cannot survive a corpus edit undetected.

## Residual risk and verification gaps

- E2/E3 ran dev mode (`--battery-dir` replaces battery39; `fixtures=88` = 90 − 4 landed + 2 variants),
  `PREDICATE C1 n/a` by design — attribution rests on the FIXTURE/MUTANT lines, which are printed.
- The `--only M04` scan breaks at the first exhibit; "killed by" is the first killer in scan order, and the
  control fixture sitting before the variant in glob order exhibited nothing, so the E2 attribution is sound.
- The witness file was read (label check) but the wx15 gate run itself was not re-executed; the counter
  never reads it, and the E2/E4 flip reproduces the same direction live, so nothing rides on it.
- Gate, counter, and spec are digest-pinned (`PINS total=26 mismatched=0` in every run above); mutant
  strings live in the pinned counter, so M04's bytes cannot drift without `invalid`/`mismatched` going red.

## Receipts (this dir)

`e1-full-counter.txt` (E1), `e23-ab.txt` (E2+E3), `e4-built.json`, `e4-ref-stdout.txt`,
`e4-m04-stdout.txt`, `e4-clause-diff.txt`, `e4-stderr.txt` (E4), `e5a.err`, `e5b.err` (E5a/E5b),
`e5c-drift.txt` (E5c), `p7m39var_same_url.py`, `p7m39ctl_staged_genuine.py` (variant sources).
Commands are quoted inline above; scratch tree (clones `lane`, `lane-e5a`, `lane-e5b`, `lane-e5c`, work
dirs, built fixtures) was removed after these copies were taken. No lane file was modified.

VERDICT: p7m39-honest
