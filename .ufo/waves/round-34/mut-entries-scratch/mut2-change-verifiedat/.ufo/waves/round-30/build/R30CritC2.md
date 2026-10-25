# R30CritC2 — falsifying C2: is `plans/round30_defects.py` a measurement or a restatement of its repairs?

Scope: attack four named surfaces of C2 (`plans/round-30-claims.md:52-70`), no production edits.
Lane probed read-only at HEAD `363a4eb` (round-29 verifier commit) and at the live worktree; all
mutation ran in `/tmp/r30-critc2/` (`lane/` = `git clone --no-hardlinks` of HEAD, `probe/` = the
mutated clone, harness `probe2.py`).

**Verdict up front.** Of the five checks, **one is a measurement (D3)**. D1, D2, D4 and D5 are
presence/polarity tests whose green state is produced by the repair's own bookkeeping artifact: the
file the repair creates (D1), a token the repair types into the lesson (D2), a git-status bit the
repair clears (D4), the JSON note the check tells the repair to write (D5). The suite is also
unguarded against the cheapest attack of all: the counter is the only artifact of the round that is
`?? untracked`, so editing five `return ""` statements makes `defects=0` with `rc=0` and nothing in
the repo can tell.

## Baselines I actually ran

| tree | command | result |
|---|---|---|
| clean `git clone` of lane HEAD `363a4eb` + worktree's `plans/round30_defects.py` | `python3 plans/round30_defects.py --lane .` | `defects=4`, `rc=1`, **D4 ok** |
| live lane worktree | same | `defects=1`, `rc=1` (only D4 red) |

The frozen predicate's first half is "prints `defects=5` … on the pre-repair tree"
(`plans/round-30-claims.md:54-55`). No commit reproduces `5`: the pre-repair bytes of the tree give
`4` (D4 green), and the counter itself is not in any commit (`git ls-files --error-unmatch
plans/round30_defects.py` → *did not match any file(s) known to git*; `git status --porcelain --
plans/` → `?? plans/round-30-claims.md`, `?? plans/round30_defects.py`). The "before" column is one
uncommitted worktree snapshot — a witness receipt (`claims/defects-before.txt`), not a replayable
state.

## Attack 1 — does a check pass without the routed defect repaired?

### D1 — PASSES on a fabricated receipt, and on an **uncommitted** one. Verdict: gameable, restatement.
`check_d1` (`plans/round30_defects.py:54-63`) reads `lane / D1_PATH` and tests two **unanchored
substrings**: `"entries=0" in text` (`:59`) and `"exit=1" in text` (`:61`). Evidence:

```
A1  receipt body = "not a control receipt\nno command was run\nentries=0 was typed by hand\n
                    the command did not exit=1 here\n"
    -> ok D1 receipt-at-cited-path: repaired
A1b receipt body = "entries=01 rows exist, exit=10 processes, nothing resolved\n"
    -> ok D1 receipt-at-cited-path: repaired
```

Three independent defects follow:

1. The routed item (§5 `corpus/lessons/round-29-verifier-spotcheck.md:120-124`) is *"no such path is
   **committed**"*. The live repair is **not committed** — `git status --porcelain --
   corpus/evidence/round29-attempt2/control-nothing.txt` → `?? corpus/evidence/round29-attempt2/control-nothing.txt`
   — and D1 still prints `repaired`. The check reads the filesystem where the defect names git.
2. `§5` offers two repairs: "Commit the receipt under the cited name **or cite the wave path**". The
   second is unreachable: `check_d1` never opens `.ufo/reports/round-29/kengaku.md` (which lives in
   the fleet repo at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-29/kengaku.md:124`), so a
   report-side fix can only ever score red. (Incidentally §5 says the report "cites … twice";
   `grep -c control-nothing` on that file = **1**.)
3. Provenance is unverified in both directions. The cited receipt's header claims "byte-identical
   control output"; the files are not byte-identical —
   `sha256 4b478db4…18e4bd` (cited) vs `c865a444…848cc7` (wave) — they share the `entries=` line
   (`entries=0 indexed=0 … verified_at=0 census=skipped`, compared equal) but not the five comment
   lines. And the report's quoted prefix omits `verified_at=0`, so the citation still does not quote
   the receipt's bytes after the repair. `check_d1` compares neither.

**Smallest tightening:** replace `path.read_text` with the committed blob and pin the provenance:

```python
blob = git(lane, "show", f"HEAD:{D1_PATH}")          # fails while untracked -> the word "committed" is now measured
wave = (lane / ".ufo/waves/round-29/attempt2/control.nothing.txt").read_text(encoding="utf-8")
line = next(l for l in wave.splitlines() if l.startswith("entries="))
if blob.returncode != 0 or line not in blob.stdout.splitlines():
    return "cited receipt is not committed, or its control line is not the wave receipt's control line"
```
plus one `^entries=0\b`/`^exit=1$` anchored test (`re.MULTILINE`) so `entries=01`/`exit=10` die.

### D2 — PASSES with the routed wording intact, and PASSES when the claim is deleted. Verdict: gameable.
`check_d2` (`:66-77`) iterates only lines containing the substring `kappa`, and per line rejects
`"in the lane"` (`:72`) then requires `"corpus/knowledge/*.md"` (`:74`). Two counterexamples:

```
C1 lesson: "… kappa scope corpus/knowledge/*.md." /
           "A test–retest ceiling is new; the sweep measured 0 hits in the lane."
   -> ok D2 kappa-sweep-scope: repaired          (routed wording survives verbatim, on a kappa-free line)
C2 lesson: "… kappa scope corpus/knowledge/*.md." /
           "… (`grep kappa` → 0 hits in the **lane**; corpus/knowledge/*.md)."
   -> ok D2 kappa-sweep-scope: repaired          (the §5 phrase itself, bolded, is invisible to :72)
C3 control, both on one line -> DEFECT D2 … still rendered 'in the lane'   (only the token test fires)
```

Two more properties make D2 a token test, not a measurement: (a) the early `return` at `:74` on the
*first* kappa line masks later lines — on pre-repair HEAD bytes the counter reports *"names no
measured scope"* rather than the routed defect at all, because line 231 (`Only per-variable kappa and
a`) trips before line 232 (`… 0 hits in the lane`) is read; the control receipt
`claims/defects-before.txt:2` therefore diagnoses the wrong defect. (b) A repair that **deletes** the
sweep sentence passes (`A2b`: `ok D2 … repaired` after replacing lines 231-232 with
`kappa: corpus/knowledge/*.md.`), i.e. removing the measured claim is scored as repairing it.

**Smallest tightening:** normalise emphasis, then judge the *sweep sentence*, not the line:

```python
flat = raw.replace("**", "").replace("*", "")
if re.search(r"0 hits\b.{0,6}\bin the lane", flat):   # fires on the §5 phrase in any decoration
    return "..."
if "0 hits" in flat and "corpus/knowledge/*.md" not in flat:
    return "the 0-hits sentence names no measured scope"
```
and drop the early return so every kappa sentence is judged (collect reasons, return the first).

### D3 — this one is real. Verdict: measurement (with one local-constant caveat).
`check_d3` (`:79-105`) recomputes `words(QUOTE) = 8` from the constant at `:32` and compares both
artifacts against it. Probe: setting registry **and** lesson to a wrong-but-equal `9` still fails
(`DEFECT D3 … registry S078 prices the line-75 quote at 9 words, actual 8`), and the true repair
(`9 words` → `8 words`) is the only green. Because `D3_ROW_RE` re-escapes the constant's quote bytes,
the registry cell must *contain* those bytes, so transcription drift is caught too. Caveat: the
"actual" is the counter's own copy of the quote, not S078's fetched artifact — a mis-transcribed
constant would validate a wrong count self-consistently. That gap belongs to C3's new quote
validation, not to C2.

**Tightening (one line):** derive the quote from the registry cell instead of the constant —
`m = re.search(r'"([^"]+)"\s*\((\d+) words\)', row[5])`, then compare `words(m.group(1))` with
`int(m.group(2))` and with the lesson's count.

### D4 — see Attack 2.

### D5 — PASSES on an empty note; scoring the *other* permitted repair as a defect. Verdict: restatement.
`check_d5` (`:120-137`) demands `expect["usedby_notes"]["S091"]` exists (`:125-127`), then requires
the entry **not** to cite S091 (`:136-137`). Probe: `{"usedby_notes": {"S091": ""}}` → `ok D5 …
repaired` — the check's green condition *is* the repair's own side effect, and the note's content is
never read. Conversely §5's option A ("cite it in the entry's prior-art section as a source") is
scored red: adding `source: S091` to the entry yields `DEFECT D5 … records no S091 used-by asymmetry
note`. The live repair is also **uncommitted** (` git diff` shows the `usedby_notes` block added to
`.ufo/waves/round-29/attempt2/adoption-expect.json`, which is ` M`), so the frozen round-29 evidence
file is being mutated in place to make a round-30 bit green.

**Smallest tightening:** make the check about *consistency*, and validate the note's bytes:

```python
note = str(notes.get("S091", "")).strip() if isinstance(notes, dict) else ""
cites = bool(re.search(r"^source:[ \t]*S091\b", entry, re.MULTILINE))
listed = "S091" in next(e for e in expect["entries"] if e["path"] == ENTRY)["sources"]
consistent = (note and "S091" in note and ENTRY in note and not cites) or (cites and listed and usedby_ok)
return "" if consistent else "S091 relation is neither noted nor cited-and-listed"
```

## Attack 2 — is D4 a real measurement? Verdict: **no; it measures local dirt, not landed evidence.**

`check_d4` (`:109-118`) passes whenever the path is tracked-or-present (`:110`) and
`git status --porcelain -- path` prints nothing (`:112-115`). Three greens that are not the repair:

1. **Clean HEAD is green while the routed defect's content is absent.** `git show
   HEAD:.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md | wc -l` = **692**; the worktree copy
   with the +22-line addendum = **714**. On a fresh clone the counter prints `ok D4 … repaired` — the
   addendum §5:130-132 requires ("commit it as wave evidence") is not in HEAD, and the check cannot
   say so. The routed defect is invisible from committed bytes: it existed only as worktree dirt.
2. **Discarding the evidence is green.** `git checkout -- <path>` (or `git stash`) restores case 1:
   the round-29 critic addendum is deleted and D4 reports repaired.
3. **A stub commit is green.** Probe: write `stub\n` over the file, `git commit` → `ok D4 …
   repaired`; content is never compared. (Committed *deletion* is correctly red — `:110-111` — so the
   only surviving content test is "does not exist".)

Corollary: a green D4 is time-unstable — any later write to that path re-opens it, so a passing run
does not prove the state called for; and the claim's own control concedes the point by substituting a
status line for a counted defect (`plans/round-30-claims.md:57-59`).

**Smallest tightening:** assert HEAD content, keep cleanliness as a secondary:

```python
blob = git(lane, "show", f"HEAD:{D4_PATH}")
if blob.returncode != 0:
    return f"{D4_PATH} is not committed: the wave evidence was not landed"
if "### D. Addendum — the 275/4/279 identity is exact (verified, not accepted)" not in blob.stdout:
    return "HEAD carries the evidence file without the critic addendum"
if (lane / D4_PATH).read_text(encoding="utf-8") != blob.stdout:
    return "worktree copy differs from HEAD (uncommitted edit)"
```

## Attack 3 — R13 separability: holds against C1, but the pre-registration does not meet R13 and one check reads a round-30-created byte.

R13 (`corpus/QUALITY.md:173`): *"No claim's counting command counts an artifact another claim of the
same round creates; each claim's count is re-run with the other claim's paths reverted and must not
move. Check: the round's pre-registration names each claim's population and its **freeze commit**,
and the report states the **revert test result**."*

- **Revert test (I ran it):** in a clone with C1's shape applied (card with six `source:` lines +
  `verified-at`, six appended `S0xx` rows, one `README.md` index row), `defects` was **4 before and 4
  after** — C2 does not move under C1's artifacts. No C1 path appears in the counter's constants
  (`:25-30`), and `cell()` (`:44-52`) matches one row id, so appended rows cannot perturb S078/S091.
  Separability from C1 holds.
- **But the counter does read a round-30-created byte.** `D1_PATH`
  (`corpus/evidence/round29-attempt2/control-nothing.txt`) does not exist at HEAD; it is created this
  round as the D1 repair. C2's separability sentence lists `corpus/evidence/round29-attempt2/` as
  *"round-29 bytes"* (`plans/round-30-claims.md:67-69`) — for the D1 target that is false: the
  directory pre-existed, the asserted member did not. Satisfying C2 requires a file that exists only
  because round 30 wrote it, so "reads only round-29 bytes" overstates the receipt.
- **D5 mutates frozen round-29 evidence in place.** The repair edits
  `.ufo/waves/round-29/attempt2/adoption-expect.json`, the file the kill rule uses as round-29's
  frozen control. I re-ran the round-29 gate on the edited file:
  `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=skipped`, `rc=1`
  (I ran **without** `--census`, so the exit code is not comparable to the frozen `exit 0` line;
  `cited_rows=5` does hold). The observation stands: after the repair, "round 29's expect file" is a
  round-30 artifact, and a reader cannot tell the round-29 bytes from the amended ones without git.
- **R13 form is unmet at the pre-registration:** C2 names no freeze commit (C3 does — it pins
  `git show <freeze-baseline>:plans/sources_adopt.py`), and no revert-test result is recorded. The
  before/after pair is a worktree pair, not a commit pair (see the baselines table).

**Smallest tightening:** in `plans/round-30-claims.md` C2, replace the separability parenthetical with
the freeze commit sha and the literal line `revert test: C1 artifacts applied → defects unchanged
(4 → 4)`, and state that the D1 target is created *by this round* but not by C1 — or, cleaner, keep
round-29 bytes untouched: have D5 read a round-30 sidecar
(`.ufo/waves/round-30/d5-usedby-note.json`) instead of editing the round-29 expect file.

## Attack 4 — can the suite be made green by editing the checker? **Yes, and it is unguarded.**

```
A6  plans/round30_defects.py with CHECKS replaced by ()
    -> defects=0    [rc=0]
```

The counter is inside the lane's own write scope (`plans/`), is untracked in every commit, and no
byte of it is pinned: `grep -rn round30_defects` over the lane finds only the claims text, the build
spec and the dispatch, no sha256. Compare C3, whose predicate explicitly requires the *pre-change*
bytes to reject the new invocation (`plans/round-30-claims.md:86-90`): C2 has no equivalent, so
"repair the tree" and "delete the checks" share one predicate. Note the guard C3 relies on does not
transfer: `git show <baseline>:plans/round30_defects.py` does not exist, because the counter has no
committed baseline.

**Smallest tightening (one edit):** give the counter a failure-capable `--selftest` and make the
frozen predicate name it:

```python
# six temp trees; each must go red for exactly its own item
cases = [("D1", junk_receipt), ("D2", bold_wording), ("D3", count_9), ("D4", stub_commit), ("D5", empty_note)]
# require: SELFTEST cases=5 killed=5 survived=0
```
plus append `sha256(plans/round30_defects.py)` to the header of
`.ufo/waves/round-30/claims/defects-before.txt` so a checker edit is visible against the freeze
receipt. With that, `defects=0` and `rc=0` alone no longer count as the C2 predicate.

## Score for the calibration axis

C2 as written is **4/5 self-restatement**: D1 (substring presence), D2 (token presence), D4 (git
cleanliness), D5 (the note the check asks for) each go green on an artifact that the act of repairing
creates, and D1/D5 go green while uncommitted; D3 alone recomputes. Two checks also reject repairs
that §5 explicitly permits (D1's report-side fix, D5's option A), so the counter is narrower than the
routed defect list it claims to re-derive. The upper-bound statement C2 may safely make is "five
routed items re-derive as *addressed*", not "5 → 0 mismatches measured"; with the five tightenings
above (D3 unchanged, one line extra) `defects=0` becomes falsifiable.

Tool installs/upgrades: none. No writes under `kengaku-shokunin` other than this file; the probe
harness lives at `/tmp/r30-critc2/probe2.py` and mutated only `/tmp` clones.
