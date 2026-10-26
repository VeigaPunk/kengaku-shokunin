# R36RevClaims — frozen-claims review (round 36, wave 1)

Scope: `plans/round-36-claims.md` (freeze `3241b86`, Amendment 1 `acbda2f`) against
`plans/round36_c1_verify.py`, `plans/round36_c2_verify.py`, the freeze controls in
`.ufo/waves/round-36/claims/`, and the frozen inputs (`plans/pkg-spec-r35.json`,
`corpus/defects-round35.jsonl`, `corpus/lessons/round-35-verifier-spotcheck.md`).
`plans/pkg_gate.py` does not exist yet (`ls plans/pkg_gate.py` → "No such file"), so every
C1 false-green/false-red statement below is a structural claim about the frozen predicate and
battery, not a run of a completed gate.

Everything was measured in a mktemp clone (`/tmp/k36-rev-E9iz/lane`, `git clone --shared`,
sparse `/corpus /plans /SCORECARD.md /.ufo/waves/round-34/assimilation`, `checkout master` →
`f9efce3`, `rev-parse --show-toplevel` = clone root, 0 untracked) plus one read-only live-lane
`git` read and one read-only census validate. No lane file was written.

---

## 1. Predicate identity (plan ↔ code ↔ receipt label)

**C1 — same sentence, one unimplemented qualifier.**
Claims:43-46: `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`, then
`rows=4 closed=4 observed_pass=4 mismatches=0`, then `PREDICATE C1 pass`, exit 0.
Code prints exactly those three label forms (`plans/round36_c1_verify.py:334,352,354`) and returns
0 iff `total==14 and fg==fr==ue==0 and len(rows)==4 and closed==4 and passed==4 and mism==0`
(`:353-355`). Controls match (`claims/control-c1-nothing.txt` last lines). **Labels: identical.**
The qualifier *“measured on a clean clone of the landing tip (no untracked files)”* (claims:45-46)
has no counterpart in code — see finding **FG2**.

**C2 — same sentence.**
Claims:75-76: `checks=6 defects=0` and `PREDICATE C2 pass`, exit 0. Code prints
`checks={len(checks)} defects={defects}` and `PREDICATE C2 {'pass'|'fail'}` and returns 0 iff
`defects==0` (`plans/round36_c2_verify.py:228-230`). Controls match
(`control-c2-nothing.txt`, `control-c2-skip.txt`). **Labels: identical.**
W1-W6 definitions in claims:76-80 track the code (W1 `:58`, W2 `:87`, W3 `:113`, W4 `:155`,
W5 `:171`, W6 `:199`); the only wording drift is finding **N1** (distinct “lines” vs distinct
spans).

---

## 2. Findings by severity

### FG1 (high) — the 14-fixture battery leaves most of the advertised gate semantics unfalsified

The claim promotes H1-H6 into one gate (claims:19-21) and the assignment fixes the gate's hardened
semantics (frozen-instrument pins; receipt pin; every quote row parses; ≥8 distinct 3-25-word
quotes at ≥8 distinct located lines, **each verbatim on the cited capture line(s)**; SOURCES
S105-S107 once each, 11 cells, tier A, status mined, pinned URL, used-by = the entry, teaches ≥8
words pairwise distinct; **capture SHA256SUMS pinned**; entry provenance trio + `## Negative space`
with a falsifier; **README index row + coverage bullet and knowledge files == index rows**;
`--require-clean-tree`; **`--rerun` re-runs the probe and byte-compares the receipt**; d4/d5
directional).

The battery's complete mutation set is `plans/round36_c1_verify.py:129-146` plus the six line
fixtures at `:175-206`:

| Advertised clause | Falsified by |
|---|---|
| every quote row parses | P3 (`mut_unparsed`, `:102-104`) |
| per-quote 3..25 words | P1 (`mut_one_word`, `:88-96`) |
| ≥8 distinct quotes/locations | P2 (`mut_duplicates`, `:98-100`) |
| teaches ≥8 words | P4 (`mut_teaches`, `:106-118`) |
| probe (frozen instrument) digest | P5 (`stub_probe`, `:120-123`) |
| no untracked file | P6/P7 |
| D4/D5 directional | L1-L6 (`:175-206`) |
| **quote verbatim on the cited capture line** | **none** — no fixture writes a parseable quote absent from its capture |
| **receipt sha256 pin** | **none** — no fixture alters `spec["receipt"]`; P5 only rewrites the probe |
| **capture SHA256SUMS** | **none** — no fixture edits a capture or its manifest |
| **SOURCES once-each / 11 cells / tier A / status mined / pinned URL / used-by** | **none** — P4 touches only cell 6 |
| **entry provenance trio** | **none** — no fixture drops a `source:` line |
| **`## Negative space` + falsifier** | **none** |
| **README index row + coverage bullet + knowledge/index parity** | **none** |
| **`--rerun` actually re-runs and compares** | **none** — only `r35_d1` passes the flag (`:272`), on the genuine package whose receipt already matches |

Consequence: a gate that implements exactly {row parses, 3-word minimum, distinctness, teaches ≥8,
probe digest, `git ls-files --others` empty} + the six D4/D5 regexes, and that treats `--rerun` as a
no-op, prints the frozen C1 target (P1-P7/L2/L3/L5/L6 reject, P0/L1/L4 accept) and returns 0 from
`r35_d1` on the genuine lane. It never reads the receipt, the capture manifest, the source lines,
the negative space, the README index/coverage rows, or the knowledge/index parity. Measured facts
supporting the “no fixture touches X” column: `grep -n 'receipt' plans/round36_c1_verify.py` hits
only the docstring/`stub_probe` read, and the only `--rerun` invocation is line 272; the recipes
handful contains no README/knowledge/entry-provenance mutation.
This is a *false green against the assignment's semantics*, not against the frozen label — the claim
pre-registers wave-2 mutation as the defence (claims:50-52) and that must be said in the C1 report and
in the ledger’s D1 note, otherwise “hardened gate” is stronger than what the counter can certify.

### FG2 (high) — “clean clone of the landing tip” is not checked; the working-tree class R35-D2 claims is only half closed

Claims:28 says the battery is “built in a `mktemp` git repo from committed round-35 bytes”;
claims:45-46 says the predicate is measured on a clean clone. Code reads the **working tree**:
`copy_package` does `shutil.copy2(lane / rel, dest / rel)` for entry/receipt/SOURCES/README/frozen
instruments and `glob`s `corpus/knowledge/*.md`, `corpus/lessons/*.md`
(`plans/round36_c1_verify.py:55-68`). No check reads `git show <rev>:<path>`, and `r35_d2`’s only
tree test is `git ls-files --others --exclude-standard` (`:279`) — which says nothing about
*tracked-but-modified* files. There is no `HEAD`/`git diff --quiet`/`git status` check anywhere in
the counter, so a dirty tracked tree yields the identical receipt.

The routed item is explicit: `corpus/lessons/round-35-verifier-spotcheck.md:87` — *“The ledger should
read committed bytes (`git show <rev>:<path>`), as the lane’s own erratum says.”* The round-36 row
text (claims:36-37) replaces that with *“no untracked file anywhere in the lane and the six D4/D5
line fixtures behave”*, and `d4_line`/`d5_line` read `(lane / spec[...]).read_text()`
(`plans/round36_c1_verify.py:161-175`). So R35-D2’s `closed` would close a narrower sentence than
the routed defect; the working-tree read itself is still in the ledger check.

Live-state evidence that the distinction is real: the lane is on a **detached HEAD**
(`git branch --show-current` prints nothing), `refs/heads/master` = `f9efce3`, and
`git status --porcelain` shows 5 untracked round-36 directories. `--lane .` run in that tree would
use the dirty `corpus/` bytes for every fixture except the untracked test; run in a clone it uses
committed bytes. The receipt cannot tell the two runs apart. Fix direction for the L1 (not applied):
record `HEAD` in the receipt and/or add `git diff --quiet` to `r35_d2`.

### FG3 / PIN (medium-high) — the frozen-digest block is stale and nothing enforces it

Claims:98-104 pins five sha256 values. Actual bytes:

```
$ sha256sum plans/regex_log_probe.py plans/round36_c1_verify.py plans/round36_c2_verify.py plans/pkg-spec-r35.json corpus/evidence/round36/toolathlon-package.md
d58194c8…  plans/regex_log_probe.py          # claims:101 says 34ab5dfd…
d7c3687c…  plans/round36_c1_verify.py        # matches claims:102
983ed65c…  plans/round36_c2_verify.py        # claims:103 says f70e6d3a…
e085b435…  plans/pkg-spec-r35.json           # matches claims:104
00132ab0…  corpus/evidence/round36/toolathlon-package.md  # matches claims:105
```

Amendment 1 (claims:123-138) records the amended probe digest `d58194c8…` but **never records the
amended `round36_c2_verify.py` digest**, and the frozen block is not updated, so the pin record is
internally contradictory for two of five files. No code reads the frozen table's values
(`grep -rn '34ab5dfd\|f70e6d3a\|e085b435\|00132ab0\|d7c3687c' plans/*.py` → exit 1, no hits); the
only digest any code pins is the amended probe (`plans/round36_c2_verify.py:41 PROBE_SHA256`) and
the round-35 spec pins. So the round-36 table is decorative: a mid-round edit of the C1 counter, the
C2 counter or `pkg-spec-r35.json` would be invisible unless it changed behaviour enough to move a
fixture.

### SEP (medium) — the Separability paragraph is false in the C2→C1 direction

Claims:94-95: *“Neither counter reads the other’s surfaces: C1 builds its battery from round-35
bytes…”*. `copy_package` copies `corpus/SOURCES.md`, `corpus/README.md` and **every**
`corpus/knowledge/*.md` into each fixture (`plans/round36_c1_verify.py:62-66`), i.e. C2’s entry, its
README index row and its three SOURCES rows. The advertised gate clause *“README index row + coverage
bullet and knowledge files == index rows”* therefore governs P0/L1/L4 acceptance and the `r35_d1` tip
run. A partial C2 landing — entry committed to `corpus/knowledge/` before the README row — makes
every genuine fixture reject (`false_red=1`), failing C1 through no C1 fault. The reverse is not
true: C1 adds no knowledge file and no SOURCES row, so C2’s W4 count and W6 census are independent
of C1. One-way coupling; the sentence should say so.

### FR1 (medium) — R35-D1’s `--rerun` rests on an environment prerequisite the spec does not encode

`plans/pkg-spec-r35.json` `probe_cmd` is `["plans/tb2_grader_probe.py", "--lane", "."]`. That command
is not runnable on this host as written:

```
$ python3 -c "import Bio"            → ModuleNotFoundError: No module named 'Bio'
$ uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .
  → rc=0, stdout byte-equal to corpus/evidence/round35/tb2-grader-probe.txt (cmp -s → BYTE-EQUAL)
```

`plans/tb2_grader_probe.py:11-13,145` requires Biopython and its docstring prescribes the uv wrapper.
The round-35 counter carries the fallback (`plans/round35_c1_verify.py:163-168`: try `import Bio`,
else `uv run --no-project --with biopython==1.85 python3 …`), but the round-36 spec does not, and the
claims do not name the prerequisite. A gate that executes the pinned `probe_cmd` faithfully returns
non-zero → `r35_d1` fails on a truthful landing (conditional **false red**). The receipt’s first line
embeds `biopython=1.85` (`corpus/evidence/round35/tb2-grader-probe.txt:1`), so any other resolution
also breaks the byte compare. Passable in this environment via uv; under-specified as frozen.

### GAP1 (medium) — C2 W1 is never shown able to fail, and its scope is the manifest, not the capture dir

Both C2 controls hold W1 green: `control-c2-nothing.txt` “W1 ok”, `control-c2-skip.txt` “W1 ok” — the
skip rewrites rows/entry/receipt only (`claims/make_c2_skip.py`). No control tampers a capture or
`SHA256SUMS`, so the claim’s “it cannot reach the target” is demonstrated only for W2/W3/W5 (+W6 by a
side effect). W1 also validates only files listed in `SHA256SUMS` (`plans/round36_c2_verify.py:58-84`);
unlisted files in the capture dir are invisible. The live lane already has
`corpus/evidence/round36/tb2-regex-log/__pycache__/` (`ls -l`), ignored by `.gitignore:2` — harmless
today, but “byte-identical capture” is strictly “the five listed digests”. Cheap control for wave 2:
flip one byte in `instruction.md` and show W1 red.

### N1 (low) — “≥8 distinct located lines” is implemented as distinct `(file,start,end)` spans

`plans/round36_c2_verify.py:149-150` adds `locs.add((fname, a, b))`; two quotes citing the same start
line with different end lines count as two locations. The C2 claim (claims:79-80) and C1’s rule say
“distinct located lines”. Edge-case divergence only.

### N2 (low) — ledger closure is partly self-asserted

`plans/round36_c1_verify.py:336-352` accepts a row as closed when `status=="closed" and check_passes`.
It does not check `closed_round`, nor the `id`/`class`/`source` values that claims:107-108 say are
frozen. A row marked `closed` with `closed_round: null`, or with its `class` rewritten, still prints
`rows=4 closed=4 observed_pass=4 mismatches=0`.

### N3 (low) — R35-D3’s regex and branch pin are footguns for a truthful landing

`NESTED_RE` (`plans/round36_c1_verify.py:42`) is `^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-`.
It also matches any **round-36** path with a nested mirror, e.g.
`.ufo/waves/round-36/build/<Seat>/.ufo/waves/round-36/…` — a seat scratch copy committed under the
build dir would fail C1 through no C1 fault. `r35_d3` reads `refs/heads/master` (`:292-296`) while
the lane currently sits on a detached HEAD; the claim never states that the landing must be committed
to `master`. Confirmed current value: 21 committed matches at `master` = `f9efce3` (`git ls-tree -r
refs/heads/master | grep -cE` → 21), matching claims:38-39. The 21 are 7 attack trees × 3 mirrored
files (`…/R34ReviewCounterC1Attacks/a3..a9/.ufo/waves/round-34/{assimilation/captures/tb2-eval/
{SHA256SUMS,test.sh},claims/control-c1.txt}`); each tree also keeps `corpus/{README.md,SOURCES.md,
knowledge/terminal-bench-task-grader.md}`, so deleting the 3 mirrored files does not empty a cited
directory.

### N4 (low) — C2 W4 parity is a count, not a bijection

`plans/round36_c2_verify.py:164-167`: `len(files) == nidx >= 43`, where `nidx` counts any README line
starting `` | `knowledge/ ``. A missing index row can be masked by a duplicate row elsewhere. The
delivered surface is separately covered (exact index row for the new entry at `:158-160`, coverage
bullet at `:160-162`), so this is a strength-of-invariant note. Reachability: freeze is 42 files / 42
rows (`ls corpus/knowledge/*.md | wc -l` → 42; `grep -c '^| \`knowledge/' corpus/README.md` → 42), so
the C2 landing (43/43) hits the boundary exactly; `control-c2-skip.txt` shows W4 ok at 43/43.

---

## 3. Are the checks unpassable on a *truthful* landing? (false-red inventory)

Verified passable:
- C1 P0’s genuine surface exists: 22 quote rows, all parse, 3-19 words, 22 distinct quotes/locations
  (`QUOTE_ROW` over `corpus/knowledge/tb2-protein-assembly-grader.md`); `## Negative space` with a
  `**Falsifier:**` (line 88-101); README index row (line 68) and a bullet inside `## Coverage map`
  (230-257); capture `SHA256SUMS` present; every spec pin matches lane bytes (receipt `2359d906…`,
  three instruments, S105-S107). So a faithful gate can accept P0.
- The six line fixtures all bite: D4 line contains both citations and `SELFTEST green failed`; the
  swap changes the line; the D5 line has `is present` and not `not present`; the capture quote is
  present and the manifest digest matches `b60af775…`; L6’s injected capture breaks that digest.
- C2: the amended probe is deterministic (two runs byte-equal to each other and to the receipt),
  `regex-log-probe.txt` summary is `cases=24 observed_pass=8 observed_fail=16 mismatches=0`, W6
  census is green live (`sources-census.sh validate --root … kengaku` → `kengaku ok`, exit 0,
  15 W04 warnings — warnings do not change status), W4’s 43/43 is reachable.
- C1 at freeze in a clean clone: `untracked_anywhere=0` (`r35_d2`), 21 nested paths, D4 recount
  13 + 23 + 1 = 37 vs `| Outcome | Count | of 38 |` (`corpus/evidence/round36/toolathlon-package.md:
  30-36`).
Conditional false reds: **FR1** (uv/Biopython), **SEP** (partial C2 landing), **N3** (a seat’s nested
scratch mirror or a non-`master` landing).
`--legacy` (7/7) is freeze-only: `plans/round35_c1_verify.py:155` still demands `42/42` knowledge
files, so after C2 lands (43/43) that control would read `accepted=0/7`. It is not part of the C1
predicate, but the claims’ freeze sentence (claims:48-49) is only reproducible at the freeze commit.

---

## 4. C1/C2 causal separability

- **C2 ⊥ C1**: W1 reads only `corpus/evidence/round36/tb2-regex-log/`; W2/W3/W4 read SOURCES/entry/
  README; W5 reads the probe + receipt; W6 validates SOURCES.md. None reads `plans/pkg_gate.py`,
  `corpus/defects-round35.jsonl`, the lesson, or SCORECARD. C1 adds no knowledge file and no SOURCES
  row, so C2’s counts and census are untouched by C1.
- **C1 → C2**: false as written (finding **SEP**). C1’s fixtures embed C2’s entry, README index row
  and S108-S110 rows, and the advertised knowledge/index parity clause makes P0/L1/L4 and the tip run
  depend on C2’s index consistency. The claim should read “C2 does not read C1’s surfaces; C1’s battery
  reads C2’s README/knowledge bytes and therefore must be measured after C2’s index row is in place”.

---

## 5. Is Amendment 1 correctly bounded?

**Content: yes, verified.** `git diff 3241b86 HEAD` shows exactly one changed line in
`plans/regex_log_probe.py` (line 127: `.replace(d, "<tmp>")`) and one in `plans/round36_c2_verify.py`
(`PROBE_SHA256`). Falsifiers run:
- freeze-commit probe (`git show 3241b86:plans/regex_log_probe.py`, sha256 `34ab5dfd…`) `--dry` vs
  amended `--dry`: `cmp` → identical; both byte-equal to
  `corpus/evidence/round36/regex-log-dry-cases-freeze.txt`.
- first-run receipt summary `cases=24 … mismatches=0` (claim: “all 24 matched before the repair”).
  After normalising the two mkdtemp-path tokens, first-run and amended receipts differ only in those
  path tokens (lines 21-22).
- two amended runs: `cmp` → identical; equal to `corpus/evidence/round36/regex-log-probe.txt`.
So the amendment’s “one line, dry untouched, predictions already matched, output deterministic” is
true.

**Boundedness of the pin: no (finding FG3/PIN).** The amendment records the new probe digest but not
the new counter digest, and the claims’ frozen-digest block (claims:98-104) still lists the
pre-amendment probe and counter values. Nothing reads the digests. The disclosed amendment is honest,
but the artifact state alone cannot distinguish it from an undocumented edit; the only record is the
claims paragraph. Whether a pre-scoring instrument repair voids a claim remains the open L0 question
disclosed at claims:136-138 — this review does not resolve it.

---

## 6. Residual risk and verification gaps

- **Overfit surface (pre-registered).** The battery uses fixed markers (` junk ` teaches, a
  straight-quote row, `plans/round35_scratch.py`, the two D4 citations, `is not present`). A gate
  matching those literals passes; wave 2 is the declared defence (claims:50-52).
- **Live-lane pycache.** `corpus/evidence/round36/tb2-regex-log/__pycache__/` and
  `corpus/evidence/round35/tb2-eval/__pycache__/` are created by running the probes in a lane. They
  are gitignored, so `r35_d2` and W1 ignore them, but a gate that compares a capture directory to its
  manifest by set equality would false-red the `r35_d1` tip run after any probe run in that tree.
- **Clone sparsity.** L4/L6 need `.ufo/waves/round-34/assimilation` and the package capture dir; the
  claim’s “clean clone” does not fix the sparse patterns. `claims/make-controls.sh` includes
  `/corpus /plans /SCORECARD.md /.ufo/waves/round-34/assimilation` — the measurement clone must match.
- **Counter self-pin.** Neither counter pins itself or the spec; FG3.
- **Verification gap.** No gate exists yet, so FG1’s minimal-gate construction is a structural
  argument over the frozen recipes, not an executed receipt. Everything else cited above was run in
  the clone and the outputs are quoted.

---

## 7. Verdict accounting

Two frozen claims reviewed. **Three false-green findings**: FG1 (battery does not falsify 8 of the
advertised clauses; a battery-shaped gate prints the target), FG2 (no clean-clone/HEAD check; the
working-tree read the R35-D2 route targets survives), FG3 (frozen-digest table stale and unenforced).
**Two false-red findings**: FR1 (`--rerun` needs Biopython 1.85/uv, not in the spec) and SEP
(partial C2 landing rejects C1’s genuine fixtures; N3’s nested seat scratch mirror / non-`master`
landing is the same class). The C2 predicate itself is sound and reachable; C2’s gaps are calibration gaps (W1 never
falsified, count-based parity), not green/red fires.

VERDICT: claims-review-2-false-green-3-false-red-2
