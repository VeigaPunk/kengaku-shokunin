# R38MapErratum — requirement-map erratum for the round-37 TB2 entry, and QUALITY Q28

Seat: scribe (leaf), round 38 wave 1, 2026-10-26. Target of the correction:
`corpus/knowledge/tb2-git-webserver-grader.md` (round-37 admitted entry) and `corpus/QUALITY.md`.
Lane tip read: `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e`. I edited no lane file: the two deliverables are
appendable drafts for the L1, filed under `.ufo/waves/round-38/build/R38MapErratum/`. Scratch
`/fast/scratch/hyaku/kengaku-r38/R38MapErratum` (clone + controls) removed after the receipts were copied.

## 1. Deliverables

| Artifact | What it is | Appends at | sha256 (filed) |
|---|---|---|---|
| `.ufo/waves/round-38/build/R38MapErratum/errata-tb2-git-webserver.md` | `## Errata (round 38)` section: corrected requirement map (3 rows), 4 per-row notes, 13-row overclaim ledger, unchanged-list | end of `corpus/knowledge/tb2-git-webserver-grader.md`, after `:291` (append-only; bytes above untouched) | `4caecfc10e50…59cb16ea` (154 lines) |
| `.ufo/waves/round-38/build/R38MapErratum/quality-q28.md` | `## Round38 criterion — a requirement-map label is derived from every violating case` + Q28 | end of `corpus/QUALITY.md`, after `:451` (after Q27) | `03eaa683a163…d92ba9d8` (45 lines) |
| `baseline.txt`, `after-append.txt`, `controls.txt`, `drive.py`, `ctl.py` | the receipts and drivers behind §3 | same dir | `SHA256SUMS` |

Exact digests: `sha256sum -c SHA256SUMS` → 7/7 `OK` in that directory (`SHA256SUMS` regenerated after the
last wording edit; it is the authority, not the abbreviated values above).

## 2. What the erratum corrects (each item with its falsifier)

| # | Entry anchor (filed bytes) | Filed claim | Correction of record | Falsified by |
|---|---|---|---|---|
| 1 | `:107` + prose `:122-124` | `\| instruction.md:9 \| enforced \|`; "Strictly enforced by the shell string comparison" | `partly`; cases `capitalised`, `leading-space`, `token-in-body`; the comparison is exact only for the body it compares while the verdict is a stdout substring | `F37CritC2Map` row 9; `F37CritC2Overclaim` F1; closure D2 (`lessons/round-37-verifier-spotcheck.md` §5) |
| 2 | `:106` + prose `:119-121` | row 8 `partly` resting on `catch-all-200` | witness `status-then-content-split`; `catch-all-200` satisfies line 8 as written and is not a violating pass | `F37CritC2Map` row 8 |
| 3 | prose `:116-118` | "The port half is enforced" | by-construction qualifier: `verify.sh:57,60` name `localhost:8080` literally, so `wrong-port-8081` prints the same `HTTP 000` as `no-server` — the case shows `:8080` must answer, not that a port is checked (label and cases stand) | `F37CritC2Map` row 7; `F37CritC2Overclaim` F2; entry's own §Case independence `:200-203` |
| 4-16 | `:33`,`:42-43`,`:58`,`:62-63`,`:66-67`,`:130`,`:133-134`,`:154`,`:162-163`,`:171`,`:196`/`:200-208`,`:222-224` | the twelve non-map overclaims | folded one per row in the erratum's §B ledger (F3-F13, with replacement wording) | `F37CritC2Overclaim` F3-F13 (F1/F2 are items 1/3) |

Row `1-6` (`:104`, `:111-115`) is **not** corrected: the Map seat re-tested it against `static-file-no-git`
and agreed. Total rows corrected = 3 (7 qualifier, 8 witness, 9 label) — the `-3-` in the verdict token names
that count.

## 3. Verification (every number with its command)

All in a `--shared` clone at `$S/lane`, toplevel verified equal to `$S/lane`, `TMPDIR="$S"`, clone removed.

| # | Command | Output |
|---|---|---|
| V1 | `git clone -q --shared … "$S/lane"`; `git -C "$S/lane" rev-parse --show-toplevel` | `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e`; toplevel equal |
| V2 | `python3 drive.py $S/lane` → `round37_c2_verify.v7(lane)` | `(True, 'rows=4 bad=0')` — the frozen round-37 V7 is **green on the wrong map** |
| V3 | same driver → `round38_c2_verify.v7(lane)` (no `tb2-build-pmars` entry yet) | `(False, 'receipt or entry absent')` |
| V4 | `round38_c2_verify.MAP_ROW.match(<round-37 row-9 line>)` | `None` — the round-37 three-cell row is not accepted by the round-38 four-cell parser (why the erratum restates in the entry's own format) |
| V5 | `round38_c2_verify.derive({...})` | `{'fail'} → enforced`, `{'pass'} → unenforced`, `{'fail','pass'} → partly` |
| V6 | append `errata-tb2-git-webserver.md` to the clone's entry, then `round37_c2_verify.v7(lane)` | `(True, 'rows=4 bad=0')` — unchanged; `diff` of the pre-append bytes against the first 291 lines → identical; `## Requirement map` count 1, `## Errata (round 38)` count 1 |
| V7 | control A: synthetic entry at the r38 entry path, 7 rows, each label derived and one violating case cited → `round38_c2_verify.v7(lane)` | `(True, 'rows=7 tags=7 bad=0')` — the harness and the format are sound |
| V8 | control B (round-37 shape: `results-format` labelled `enforced`, citing a failing violator, with a passing violator uncited) | `(False, "rows=7 tags=7 bad=['results-format: labelled enforced, receipt derives partly']")` — **the label leg fires** |
| V9 | control C: `no-x11` row cites `canned-shape`, which does not carry the tag | `(False, "bad=['no-x11: cites no case or a case that does not violate it']")` — the citation leg fires |
| V10 | control D: a three-cell round-37-style row | `(False, 'rows=6 tags=7 bad=["unparsed row …", "tags missing=[\'no-x11\'] duplicated=0"]')` |
| V11 | synthetic entry deleted | `(False, 'receipt or entry absent')` — no residue in the clone |

Controls A-D used only frozen inputs (the round-38 dry table, receipt, spec) plus a synthetic entry that a
driver wrote and removed inside the scratch clone; the synthetic file carried the header line
`# SYNTHETIC CONTROL — not an entry, never committed`. It is not evidence that a `tb2-build-pmars` entry
exists.

Facts I re-checked myself rather than inheriting:

| Check | Command | Output |
|---|---|---|
| the map's own definition | `sed -n '97,100p'` | `enforced` = violating case observed `fail`; `partly` = direction confirmed for one clause, free for another |
| the violating pass | `sed -n '35p' corpus/evidence/round37/git-webserver-probe.txt` | `CASE token-in-body … observed=pass` |
| the round-37 counter's V7 rule | `sed -n '192,201p' plans/round37_c2_verify.py` | it reads the verdicts of the **cited** cases only, one direction test per label |
| the round-38 V7 rule | `sed -n '239,248p' plans/round38_c2_verify.py` | violating set from `violates=`, `derive`, `label != want`, cited-id membership |
| frozen round-38 tags | `grep -c '^TAG ' corpus/evidence/round38/build-pmars-dry-cases-freeze.txt` | `7` |
| round-37 receipt carries no tags | `grep -c 'violates=' corpus/evidence/round37/git-webserver-probe.txt` (and the dry table) | `0`, `0` |
| F9's bad anchor | `sed -n '1,10p;40,43p' corpus/knowledge/webarena-task-spec-audit.md` | `:6` is the H1; `StringEvaluator` in `source:` `:1`, `URL` row `:40`, page-content row `:41` |
| F11's bind lines | `sed -n '209p;235p' plans/git_webserver_probe.py` | `--tmpfs /tmp`; `HOME=/work/home` |
| F4's mechanism | `cat .ufo/waves/round-37/falsify/F37CritC2Overclaim/diag-verify-stderr.txt` | `./git_test.exp: /usr/bin/expect: bad interpreter: No such file or directory` |
| F3's correction | `grep -n 'Three seconds' .ufo/waves/round-37/build/R37CritCases.md` | `:124` |
| the frozen counter was green over the wrong map | `cat .ufo/waves/round-37/falsify/F37CritC2Map/c2-verify-run.txt` | `V7 ok rows=4 bad=0` / `checks=7 defects=0` / `PREDICATE C2 pass` (sha256 `d0a608ca…`) |

Read from seats, not re-run by me: the 22-case probe execution, the full round-37 counter run (only its V7
function, V2 above), and the four post-hoc cases. Not verified: no case was re-executed and the task image was
not touched.

## 4. Findings

1. **The frozen round-37 V7 could not catch its own entry's worst row.** Measured: `v7 → (True, 'rows=4
   bad=0')` beside a row that says `enforced` while `token-in-body` is observed `pass`. The rule reads only
   cited cases, so the failing witness satisfies the direction and the passing violator never enters.
   Q28 + round-38 V7 is the fix, and control B shows the fix fires on exactly that shape.
2. **Every round-38 tag derives `partly` from the frozen receipt** — all seven (`from-source`, `no-x11`,
   `debian-source`, `extract-to-app`, `install-path`, `results-format`, `debugger-works`), each with
   `obs=['fail','pass']` (command: a 20-line driver over the frozen receipt and dry table; printed in §3's
   V7 inputs). Consequence for the C2 lander: a row labelled `enforced` or `unenforced` cannot pass V7, and a
   row citing a case outside the tag's violating set reddens the citation leg — seven rows, seven `partly`.
3. **The round-37 entry cannot be machine-re-derived.** No `violates=` tags in the receipt or the dry table,
   and the three-cell row layout fails `MAP_ROW`. So the correction is hand-adjudicated from two seats'
   receipts, and Q28 is written as a forward criterion, not a re-score of round 37 — stated as a limit inside
   both deliverables rather than glossed.
4. **One seat anchor was wrong and is corrected here**: F5's sentence ("the grader reads nothing from the
   filesystem and makes two HTTP requests") is at `:162-163`, not `:167-168`; `:167-168` is the
   case-independence caveat. Recorded in the erratum's §B preamble.
5. **Appending the erratum cannot disturb the frozen round-37 counter**: the `## Requirement map` section is
   parsed to the next `^## `, and the appended section is after it — measured green before and after the
   append (V2, V6). The erratum therefore leaves the frozen predicate's greenness intact while the correction
   of record lives in the file.
6. **Q28's honest limits** (in the criterion): the derived label is only as good as the frozen `violates=`
   tags; "violates" is a human judgement frozen pre-run, so the criterion moves the decision into a reviewable
   artifact without mechanising semantics; one label per tag collapses a two-clause line (row 7's port/push
   split is exactly that and still needs the prose qualifier); a thin tag set derives cheaply.

## 5. No-harm and out of scope

- No lane file edited, no commit, no `git add`, no mutating `jj`. `corpus/knowledge/tb2-git-webserver-grader.md`
  sha256 `6e3f8c77…4812a` and `corpus/QUALITY.md` sha256 `f1fc18ac…c5d99` are the same before and after this
  seat's work; every write went to `.ufo/waves/round-38/build/R38MapErratum/`.
- No tool installed or upgraded (nothing was needed); no pacman, no uv, no npx.
- Scratch deleted: `ls -d /fast/scratch/hyaku/kengaku-r38/R38MapErratum` → `No such file or directory`.
- Out of scope by assignment: D1 (committing round-37 wave-2 outputs), D3-D7, integrating these drafts (L1),
  the C1 battery work and every C2 counter change; wave 2.

VERDICT: erratum-3-rows-q28-drafted
