# R36QualityDraft — QUALITY criteria draft for round 36 (wave 1)

Seat: R36QualityDraft (scribe). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Drafted two criteria, Q24 and Q25, ready to append to `corpus/QUALITY.md` after its current last line
(295, `  §Mistakes.`). QUALITY.md was not edited (verified below).

## Insertion point

`corpus/QUALITY.md` is 295 lines; the last block is the Round35 criterion, ending at line 295 with
`  §Mistakes.` (`wc -l corpus/QUALITY.md` → `295 lines`). The draft below goes after it, so the file
keeps one `##` section per criterion and Q-numbering stays monotone (Q23 is the last id on disk).

## Paste-ready draft (append verbatim)

~~~~markdown

## Round36 criterion — a counter of record is attacked by its own junk

- **Q24 — a counter of record for an admitted-entry package is proved, before it scores any data, by a
  frozen battery built from the genuine package's own bytes: the genuine package must be accepted, every
  single-property junk mutant must be rejected, and an unevaluated run is never a rejection.** A counter
  that is only ever pointed at the package it was written for proves that package, not the check. The
  round-35 counter of record accepted all seven junk packages —
  `LEGACY accepted=7/7` (`.ufo/waves/round-36/claims/control-c1-legacy.txt`) — among them an entry of
  eight one-word quotes, `junk` teaches cells, a stub probe that prints the receipt, and an untracked
  leftover file; the same weakness let labelled-but-false D4/D5 lines pass
  (`corpus/lessons/round-35-verifier-spotcheck.md:86`, routed defect 1). So each round's counter carries
  a battery whose control receipts are committed at the freeze, and the cheapest all-junk package is
  built and scored by a seat that is not the counter's author *before* the round's first data receipt is
  committed. The tip-receipt clause is why the ordering matters: `plans/round36_c1_verify.py` runs
  `battery()` (`:217`) and only then the tip re-run inside `r35_d1` (`:267`), so a green aggregate
  cannot be reached by a counter that accepts everything or rejects everything.
  Measured at the criterion's creation (2026-10-25): `ls plans/pkg_gate.py` → `No such file or
  directory`, the counter prints `FIXTURES total=14 false_green=0 false_red=0 unevaluated=14`
  (`.ufo/waves/round-36/claims/control-c1-nothing.txt`), and the round-35 counter prints
  `LEGACY accepted=7/7` (same control set, committed in freeze commit `3241b86`).
  Check (executable, round-36 instance): `python3 plans/round36_c1_verify.py --lane .` must exit 0 and
  print `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0` then `PREDICATE C1 pass`. The
  battery is 14 fixtures built in a `mktemp` git repo from committed round-35 bytes
  (`build_package_fixtures`, `plans/round36_c1_verify.py:126`): P0 genuine plus seven single-property
  junk packages (P1..P7, P7 the all-junk combination) and six D4/D5 line fixtures. Name-blindness leg —
  copy P0 and P7 to directories that carry no fixture id and expect exit 0 and exit 1:
  `d=$(mktemp -d /tmp/k36-ren-XXXX); python3 - "$d" <<'PY'` … `import round36_c1_verify as c` …
  `for fid, want in (("P0", 0), ("P7", 1)):` … `print(fid, "renamed_rc", rc, "want", want)` `PY`
  → `renamed_rc 0` for P0 and `renamed_rc 1` for P7.
  Shown able to fail: the accept-everything control scores `false_green=11 false_red=0`
  (`control-c1-accept-all.txt`), the reject-everything control scores `false_green=0 false_red=3`
  (`control-c1-reject-all.txt`), and the no-gate control scores `unevaluated=14` (`control-c1-nothing.txt`);
  `unevaluated` is printed beside `false_green`/`false_red` so a crash cannot masquerade as a rejection.
  The proposal and its date are `considerthese/2026-10-25.md` §Self-improvement suggestions 2(c)
  ("includes a tip-receipt validator (every `corpus/evidence/**` receipt re-run and byte-compared)",
  2026-10-25) — this criterion takes the pre-data half of it and leaves the persistent ledger to Q23.
  Limits: the battery is single-property mutants, so a junk class no fixture occupies survives (P7 covers
  only the named properties combined, not new ones); 14 fixtures is a budget, not a search; the builder
  names its fixture directories `k36-P<n>-…`, so a gate that keyed on its `--root` basename would pass
  the battery — the rename leg is the cheap defence, not a proof; and no mechanical battery separates
  well-formed false prose from a true claim once every field parses, which stays a reviewer's job (Q10).
  Lesson: `corpus/lessons/round-36.md` §Mistakes (1).

## Round36 criterion — a frozen instrument is repaired in the open window, and its case table does not move

- **Q25 — a frozen instrument that fails its own determinism on the first real run is amended only
  before any seat has scored, by a commit that pins both digests, names the changed lines, and shows the
  deterministic case table byte-identical at both revisions.** Amendment 1 of round 36 is the instance:
  the frozen probe printed a `mkdtemp` path in two assertion texts
  (`corpus/evidence/round36/regex-log-probe-first-run.txt:21-22`), so the frozen W5 check "fresh run
  byte-equal to the receipt" could never hold; the repair replaced the temp directory with `<tmp>` in the
  printed text only (`plans/round-36-claims.md:123-140`), and the amended digest
  `d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc` is pinned in
  `plans/round36_c2_verify.py:41`. What keeps the amendment from being a rule change is the case table:
  `--dry` at the freeze commit and at the amended tip are byte-identical, and both equal the committed
  table `corpus/evidence/round36/regex-log-dry-cases-freeze.txt`. A repair that moved a prediction, a
  case, a check definition or a predicate sentence is a new claim and re-freezes.
  Check (executable, round-36 instance):
  `git show 3241b86:plans/regex_log_probe.py >/tmp/pre_probe.py &&
  python3 /tmp/pre_probe.py --dry | cmp - <(python3 plans/regex_log_probe.py --dry) && echo identical`
  → `identical`, and `sha256sum plans/regex_log_probe.py` gives the pinned `d58194c8…`. The remaining
  legs are the pins and the order: the note names both digests
  (`grep -n 'amended probe digest' plans/round-36-claims.md`), and the amendment commit is an ancestor of
  every commit that first adds a receipt scoring the instrument —
  `git merge-base --is-ancestor acbda2f3936838ba4849f14937fbecb8aed461e5 <first-scoring-commit>`.
  Shown able to fail: `cmp corpus/evidence/round36/regex-log-probe-first-run.txt
  corpus/evidence/round36/regex-log-probe.txt` exits 1 and differs on exactly lines 21-22 — the
  pre-amendment instrument cannot reproduce the receipt, which is the failure this criterion names; a
  `--dry` that differed would be caught by the `cmp` above.
  The question this criterion does not settle is open on the L0 queue: `revenger | round-69` asks whether
  an instrument defect (not the artifact under test) may be repaired pre-scoring as a new revision with a
  fresh red-before, or whether the claim must stand falsified and wait a round
  (`.ufo/l0-questions.md:160`); `kumitate | round-63` and `round-64` ask the neighbouring question —
  whether a post-freeze enlargement or relaxation of a control set is a ratchet or a rule change
  (`:167`, `:170`). This criterion takes the position both can live with: a repair is admissible only
  while the case table is unmoved and no seat has scored, and the window's admissibility stays the
  operator's.
  Limits: commit order is the only mechanical witness — an untracked seat build directory leaves no
  commit, so a seat that scored before the amendment and reported later is invisible to the ancestry
  check; `--dry` identity proves the printed case table only, so an amendment to a non-`--dry` code path
  (there was none here) would pass it; and the criterion does not decide whether a pre-scoring repair
  voids a claim, so a round that amends still reports the verdict either way.
  Lesson: `corpus/lessons/round-36.md` §Mistakes — pending at draft time (see Findings).
~~~~

## Name-blind leg (full snippet, tested)

Run from the lane root; writes only under `/tmp`:

```
d=$(mktemp -d /tmp/k36-ren-XXXX); python3 - "$d" <<'PY'
import pathlib, shutil, subprocess, sys, tempfile
sys.path.insert(0, "plans"); import round36_c1_verify as c
lane = pathlib.Path(".").resolve(); spec = c.load_spec(lane)
src = {i: d for i, _, _, d in c.build_package_fixtures(lane, spec, tempfile.mkdtemp(prefix="k36-bat-"))}
for fid, want in (("P0", 0), ("P7", 1)):
    dst = pathlib.Path(sys.argv[1]) / ("a" if want == 0 else "b")
    shutil.copytree(src[fid], dst)
    rc = subprocess.run([sys.executable, "plans/pkg_gate.py", "package", "--root", str(dst),
                         "--spec", "plans/pkg-spec-r35.json", "--require-clean-tree"]).returncode
    print(fid, "renamed_rc", rc, "want", want)
PY
rm -rf "$d"
```

Observed now (2026-10-25): `P0 renamed_rc 2 want 0` / `P7 renamed_rc 2 want 1`, with
`can't open file '…/plans/pkg_gate.py'` on stderr — the gate is absent, so both legs are `unevaluated`
today and the leg becomes decidable only when `plans/pkg_gate.py` lands.

## Evidence — every number with its command and output

| # | command | output |
|---|---|---|
| 1 | `wc -l corpus/QUALITY.md` | `295 corpus/QUALITY.md` (append after line 295) |
| 2 | `grep -n "^## \|^- \*\*Q" corpus/QUALITY.md` | last section `## Round35 criterion…` at 273, `Q23` at 275; no Round36 section |
| 3 | `cat .ufo/waves/round-36/claims/control-c1-legacy.txt` | `LEGACY accepted=7/7`, `exit=0` |
| 4 | `cat …/control-c1-accept-all.txt` | `FIXTURES total=14 false_green=11 false_red=0 unevaluated=0`, `PREDICATE C1 fail`, `exit=1` |
| 5 | `cat …/control-c1-reject-all.txt` | `FIXTURES total=14 false_green=0 false_red=3 unevaluated=0`, `PREDICATE C1 fail`, `exit=1` |
| 6 | `cat …/control-c1-nothing.txt` | `FIXTURES total=14 false_green=0 false_red=0 unevaluated=14`; `R35-D4 … round-36 lesson absent; recount 13 + 23 + 1 = 37 vs stated denominator 38` |
| 7 | `ls -la plans/pkg_gate.py` | `No such file or directory` (gate absent at draft time) |
| 8 | `grep -n "^def battery\|^def r35_d1\|^def build_package_fixtures\|^def run_gate\|^def legacy" plans/round36_c1_verify.py` | `126:build_package_fixtures`, `208:run_gate`, `217:battery`, `245:legacy`, `267:r35_d1` |
| 9 | `sha256sum plans/regex_log_probe.py` | `d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc` (matches the pin at `plans/round36_c2_verify.py:41`) |
| 10 | `python3 /tmp/pre_probe.py --dry > /tmp/pre.dry; python3 plans/regex_log_probe.py --dry > /tmp/post.dry; cmp …` | `DRY_IDENTICAL` (both exit 0) |
| 11 | `cmp /tmp/post.dry corpus/evidence/round36/regex-log-dry-cases-freeze.txt` | `DRY_EQUALS_FROZEN_TABLE` (25 lines of `--dry` output) |
| 12 | `diff regex-log-probe-first-run.txt regex-log-probe.txt` | differs at `21,22c21,22` only: `/tmp/tmp68j2v92s` and `/tmp/tmp7c39pj0f` → `<tmp>`; `diff_exit=1` |
| 13 | `git cat-file -t acbda2f…`; `git merge-base --is-ancestor acbda2f… HEAD` | `commit`; `AMENDMENT_ANCESTOR_OF_HEAD` (HEAD = `f9efce3` = `master`) |
| 14 | `git log --diff-filter=A --format='%h %s' -- .ufo/waves/round-36/claims/` | `3241b86 round-36: freeze claims, counters, probe, spec, ledger rows, controls` — the control receipts are in the freeze commit, i.e. before any data receipt |
| 15 | name-blind snippet above | `P0 renamed_rc 2 want 0`, `P7 renamed_rc 2 want 1` (unevaluated; gate absent) |
| 16 | `grep -n "Amendment 1\|amended probe digest" plans/round-36-claims.md` | `123:## Amendment 1 (pre-scoring instrument repair, disclosed; recorded after freeze \`3241b86c\`, before any seat dispatch)`, digest at `134` |
| 17 | `grep -n "revenger\|kumitate" .ufo/l0-questions.md` | `:156` revenger round-68, `:160` revenger round-69, `:167` kumitate round-63, `:170` kumitate round-64 |
| 18 | `sed -n '80,100p' corpus/lessons/round-35-verifier-spotcheck.md` | §5 item 1 "Frozen counters accept junk… `plans/round35_c1_verify.py` passes a stub probe plus one-word quotes; `plans/defect_ledger.py` D4/D5 accept labelled-but-false lines" (line 86) |
| 19 | `sed -n '36,52p' considerthese/2026-10-25.md` | line 44: "…(c) includes a tip-receipt validator (every `corpus/evidence/**` receipt re-run and byte-compared)" |
| 20 | `ls corpus/lessons/round-36.md` | `No such file or directory` (lesson not yet written; see Findings) |
| 21 | `grep -c "^## Round" corpus/QUALITY.md` | `7` sections on disk; none for round 36 |

Nothing in the draft is inferred: each clause maps to a row above. The two criteria are drafted, not
scored; Q24/Q25 are empty seats until the L1 appends them.

## Findings

1. **`corpus/lessons/round-36.md` does not exist yet** (`ls` → No such file; the C1 counter's own
   `r35_d4` prints `round-36 lesson absent` in every control receipt, row 6). Q24 cites
   `§Mistakes (1)` as instructed; **the L1 must confirm that section number when the lesson lands**
   (round-35's lesson puts the junk-acceptance mistake in `§Mistakes`; the spot-check's version is
   `corpus/lessons/round-35-verifier-spotcheck.md:86`). For the same reason the Q25 `Lesson:` line is
   marked pending rather than inventing a section.
2. **Q24's ordering leg is real but not yet exercised for C1 data.** The cheapest-junk control is in
   freeze commit `3241b86` (row 14) and `battery()` precedes the tip re-run in code (row 8), so the
   "before any data" clause is anchored twice; there is still no C1 data receipt at the tip in wave 1,
   so the commit-ancestry form of the leg cannot yet be run against one.
3. **`unevaluated` is load-bearing and is printed separately** (rows 5-6, 15): a missing gate yields
   `false_green=0 false_red=0` with `unevaluated=14`, so a criterion that read only the two error counts
   would green an absent gate. Q24 states the three counts together for this reason.
4. **The battery's fixture directories are named `k36-P0-…`/`k36-P7-…`** (row 15; builder at
   `plans/round36_c1_verify.py:126` uses `mkdtemp(prefix=f"k36-{pid}-")`). This is the overfitting
   surface wave 2 will attack; the rename leg is included in the criterion as the cheap mechanical
   defence and is explicitly stated as not a proof.
5. **Amendment 1 is fully grounded as a draftable criterion** (rows 9-13, 16): both digests pinned,
   `--dry` byte-identical, exactly two lines of printed text changed, amendment commit an ancestor of
   the tip, and `LEGACY`-style red-before evidence exists in the first-run receipt. The L0 questions
   (`revenger | round-69`, `kumitate | round-63/64`) are cited as the undecided question, not as a
   resolution.
6. **No QUALITY.md edit was made.** `git status --porcelain` showed only
   `?? .ufo/waves/round-36/build.ready`, `?? .ufo/waves/round-36/build/`,
   `?? .ufo/waves/round-36/integrate/` before and after this seat's writes; `corpus/` and `plans/` are
   untouched by me.

## Touched surfaces

- Written: `.ufo/waves/round-36/build/R36QualityDraft.md` (this report).
- Scratch: `mktemp -d /tmp/k36-ren-XXXX`, `/tmp/pre_probe.py`, `/tmp/pre.dry`, `/tmp/post.dry` — all
  under `/tmp`; the rename scratch dir was removed (`rm -rf "$d"`), the probe/dry files are left as
  cited evidence paths for a re-run.
- Read-only: `plans/round-36-claims.md`, `plans/round36_c1_verify.py`, `plans/round36_c2_verify.py`,
  `plans/regex_log_probe.py`, `corpus/QUALITY.md`, `corpus/lessons/round-35-verifier-spotcheck.md`,
  `corpus/defects-round35.jsonl`, `corpus/evidence/round36/*`, `.ufo/waves/round-36/claims/*`,
  `.ufo/l0-questions.md`, `considerthese/2026-10-25.md`. No git write; no jj command; no subagent.
- Install: none (no tool needed).

## Out of scope (not done, by rule)

- No edit to `corpus/QUALITY.md`, `corpus/lessons/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`,
  `SKILL.md`, `PROVINCE.md`.
- No gate implementation and no battery run against a real `plans/pkg_gate.py` (absent; the gate is
  another seat's surface). I did not re-run the counter to decorate the report — every counter line
  quoted is from the committed control receipts.
- No decision on the open L0 questions; Q25 records them as open.

VERDICT: quality-drafted-2-criteria
