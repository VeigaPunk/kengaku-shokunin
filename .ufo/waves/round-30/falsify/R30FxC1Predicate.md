# R30FxC1Predicate — C1's frozen sentence, clause by clause, against the landed bytes

Seat: falsify wave, leaf. Scope: **the predicate's wording**, not the counter's blind spots as such
(that is `falsify/R30FxC1Counter.md`, which this report credits and does not re-litigate).
Target: `plans/round-30-claims.md` §C1, the sentence frozen between "Frozen predicate" and "Counting
command". Candidate path under review: `corpus/knowledge/contamination-transparency-card.md`.

This seat is neither a source re-read nor the complete-set review, so **no `VERDICT:` gate line is
emitted**; the verdict below is on the predicate's re-derivability, not on the entry's admission.

Everything below was run by me on 2026-10-25. Nothing installed or upgraded (pacman paused host-wide;
no tool was needed — python3 3.14, git, bash, the fleet census script). Scratch:
`/tmp/r30fx-kengakuPred/` (`wt/` worktree copy, `baseg/` = `git archive HEAD`, `m1`…`m19` mutants,
`mkconf.sh` 21-byte harness conf, `matrix.sh`/`matrix2.sh`, `tamper.py`). No lane file edited.

---

## 0. Provenance first: there are no committed round-30 bytes to check

The ticket says "against committed bytes". At lane tip `363a4eb` there are none:

```
$ git status --short | grep -E 'contamination-transparency-card|SOURCES.md|README.md'
 M corpus/README.md
 M corpus/SOURCES.md
?? corpus/knowledge/contamination-transparency-card.md
$ git show HEAD:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3}'      → 82      (worktree: 88)
$ git show HEAD:corpus/README.md | grep -c '^| `knowledge/contamination-transparency-card.md` |' → 0
```

So the clause-by-clause check bifurcates, and this is the first seam:

| tree | result of the frozen counting command |
|---|---|
| worktree (what `adoption_check.py` actually reads) | `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok`, exit 0 |
| `git archive HEAD` + the expect file (= the committed tree today) | `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok`, **exit 1** |

The second line is byte-identical to `.ufo/waves/round-30/claims/control-nothing.txt`. In other words
**the committed tree today prints C1's own control line**: C1's pass exists only in the working
directory. The tool's docstring says the opposite — `plans/adoption_check.py:2` "Re-derive an adoption
round's landed state **from committed bytes**" and `:7` "It reads only committed corpus files, so a
do-nothing round scores zero" — while the code never invokes git (`grep -c git plans/adoption_check.py`
→ 0). A reader re-deriving "landed" from the docstring concludes something the code does not do; the
predicate's own word is the weaker "exists", which is why nothing catches it. This is the same class as
`R30CritC1.md` B6 (freeze has no git evidence) and `R30FxC1Counter.md` §3.12, applied to the *entry*
rather than the freeze: **the claim's bytes must be committed before "landed" is true, and no clause
says so.**

Every probe below was run on a `/tmp` copy or on the harness root — **I did not run the counting
command inside the lane** (read-only discipline). The in-place run of the same bytes is recorded by two
sibling seats (`R30CritC1.md:25`, `R30FxC1Counter.md:25`) and matches my harness output field for field;
the census leg was run in place read-only (`sources-census.sh validate … kengaku`, §2.3).

Reproduction harness (needed because the census leg wants a conf beside the lane parent):

```
$ cat /tmp/r30fx-kengakuPred/mkconf.sh        # rm -rf $root; cp -a $src $root/kengaku-shokunin
                                              # printf 'LANES="\nkengaku|kengaku-shokunin|falsify harness\n"\n'
$ cd /tmp/r30fx-kengakuPred/root_tgt/kengaku-shokunin \
  && python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census
entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok
exit=0
```

---

## 1. Clause-by-clause table

`holds?` = true of the landed worktree bytes, re-derived by me, not taken from a build report.
`machine` = what the frozen command does with the clause (§1 of `adoption_check.py`, unchanged from
round 29: `git status --porcelain plans/adoption_check.py` → empty).
`witness` = whether the clause is visible in the printed line the predicate quotes as its evidence.

| # | clause, as the sentence words it | landed-bytes evidence (my run) | holds? | machine | witness | brittle seam |
|---|---|---|---|---|---|---|
| P1 | `corpus/knowledge/contamination-transparency-card.md` **exists** | file present, 17 074 B / 177 lines, header block at `:1-9` then the entry body | **yes** | `present` (`:74-75`) — non-empty worktree file | yes (`entries=1`) | existence ≠ committed (§0); also "exists" is satisfiable by a 9-line stub (M16; `R30CritC1` B4) |
| P2 | `source:` lines citing **exactly the six ids S081 S082 S083 S084 S085 S086** | `grep -c '^source:'` → **6**; ids in file order S081…S086; id↔URL identity vs registry cell 1 → **6/6 match** | **yes** | `SOURCE_LINE_RE` (`:34`) collects ids; `len(cited) == required` (`:152`) compares a **count** | only as `cited_rows=6` | **identity never compared**: entry rewritten to `S001 S002 S004 S007 S008 S012` (all mined, none naming the entry) prints the exact frozen line, exit 0 (mine; `R30CritC1` B2, `R30FxC1Counter` §1b). "exactly the six ids" is a human clause |
| P3 | "(six distinct)" | six ids, six distinct | **yes** | set union ⇒ distinctness is tested *on the entry side* | via `cited_rows=6` | distinctness is tested where it costs nothing and untested where it matters: expect `sources=[S081,S081,S082,S083,S084,S085]` passes (`R30FxC1Counter` §1c c) |
| P4 | *(ticket clause, not in the sentence)* **no other S-id anywhere in the entry** | `\b[sS]\d+\b` → exactly `{S081,S082,S083,S084,S085,S086,S1,S2}`; no `S077`, no `S091`, no `S087+` | **yes, under a 3-digit reading** | nothing — no prose read | no | two seams: (a) the sentence **does not contain this clause at all**, so a body-only citation (the round-29 S091 shape, the staged S077 shape) is out of scope of C1's own predicate; (b) tokens `S1`/`S2` *are* in the entry as the delta-field labels, so the clause is true only under a width convention the sentence never states. Probe M7 (add `S091` in prose, no `source:` line) → exact frozen line, exit 0 |
| P5 | a **`verified-at: 2026-10-25`** line | `:7` `verified-at: 2026-10-25` — one occurrence | **yes** | `:79` regex against **expect.access_date**, not against a literal | **no** — gated, unprinted (`:124`, `:130`) | silent gate: M8 (`2026-10-25`→`2026-10-24`) prints `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok` **and exits 1**. The predicate names the printed line as the claim's evidence; one of its clauses can fail with a byte-identical line. A reader comparing output cannot see P5 fail |
| P6 | every cited row **present in `corpus/SOURCES.md`** | rows at lines 107-112 of the 88-row registry, 11 cells each | **yes** | `registry_rows()` (`:38-51`), cell-count gate `len(cells)!=11 → skip` (`:46`) | `rows_present=6` | presence is not identity: the row may be unidentifiable (blank `source` cell) and still "present" (`R30FxC1Counter` §1, §3.8) |
| P7 | … with **`status=mined`** | cell 7 = `mined` ×6 | **yes** | `registry[row_id][7] == "mined"` (`:88`) | `rows_mined=6` | **satisfied by construction**: the six rows are *created* mined — one contiguous append (`git diff` = `6 ++++++`, lines 107-112) that mints id, URL, status, `opened`, `used-by` and the quotes in one act, with `corpus/evidence/round30/rows-opened.tsv` as its own record. `rows_mined=6` therefore cannot distinguish six opens from one paste. It is one of the four clauses that *is* machine-tested (M4 `status=rejected` → `rows_mined=5`, exit 1) |
| P8 | … with **`opened=2026-10-25`** | cell 8 = `2026-10-25` ×6 | **yes** | **nothing**: no `opened` read anywhere (`grep -n opened plans/adoption_check.py` → 0 hits); census E08 only rejects *future* dates | no | two seams. (i) unread: M3 sets S083 `opened=2026-01-01` → exact frozen line, exit 0. (ii) *semantic*: `HEAD:SOURCES.md` has 82 rows and **no** S081–S086, so these ids are new — `opened` here records the day the row was minted, which for a new row is a tautology, and **cannot discriminate the flip's "re-open the cited sources in a later round"**. The re-open lives only in the campaign cross-reference (`recheck:` line + §Corrections), which nothing counted reads |
| P9 | … `used-by` **naming the entry** | cell 10 = `corpus/knowledge/contamination-transparency-card.md` ×6, and no other registry row names it (`rows whose used-by names the entry` → exactly S081-S086) | **yes** | `:93-98`, comma-split path membership, **over `entry["sources"]`** — the expect list, not the cited list | `usedby_ok=1` | the strictest and best clause (M5: S084 `used-by` → another entry ⇒ `usedby_ok=0`, exit 1). But because it iterates the expect file while P2 iterates the entry, **the two halves can be satisfied by disjoint six-row sets** (`R30FxC1Counter` §1b): P9 is about rows the entry never cites |
| P10 | the entry has **one index row** in `corpus/README.md` | exactly one `^| \`knowledge/contamination-transparency-card.md\` |` line (plus two non-table mentions, coverage map `:242` and frontier sub-bullet `:275`) | **yes** | `:76-78` — existential: `re.search` over the whole README | via `indexed=1` | (a) plurality untested: a second identical row → `indexed=1`, exit 0 (M6; `R30FxC1Counter` §1c d). (b) the code's own comment (`:76`) claims "a table line, **not a mention inside a comment**", but an HTML-commented table row still matches: M19 wraps the row in `<!--`/`-->` → `indexed=1`, **exit 0** (the sibling tested a fenced block, §1c f, not the comment shape the comment names). (c) the sentence does not say *which* README surface; the counter picks the index table, so C1's stated axis move (frontier bullet 2 → core) is outside this clause entirely (`R30CritC1:179`) |
| P11 | `python3 plans/adoption_check.py --expect … --census` prints `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok` and exits 0 | reproduced exactly, exit 0 (§0 harness) | **yes** | the line is produced by `:144-148`; `ok` requires all seven plus `args.census` (`:149-162`) | — | the `census=ok` field is **invariant under the claim**: see §3 below. Also the pass line is not portable: the *same bytes* under a `git archive`/`cp -a` at a root without `shokunin.conf` print `… census=fail`, exit 1 (§0). A reader who re-derives from a worktree copy gets a red line while the corpus bytes are identical |

Literals that hold and needed no special pleading: `recheck: 180d` ×6, `verified-at` on `:7`, file order
S081→S086, id↔URL 6/6, `plans/adoption_check.py` unchanged from round 29
(`git status --porcelain plans/adoption_check.py` empty), and round 29's own counter still green on the
landed tree (`entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`,
exit 0 — matches `corpus/evidence/round30/r29-counter-unchanged.txt`).

---

## 2. Clauses satisfied *by accident*

1. **P7 `status=mined`.** New rows arrive mined; nothing in the counted path would differ if the six
   sources had never been opened. The row's `mined` and the row's existence are one write
   (rows-opened.tsv is the same seat's prose record, not a fetch).
2. **P8 `opened=2026-10-25`.** True by construction for any row minted today; and, being unread, it is
   also true-by-typing. It cannot carry the flip it is supposed to witness because the lane had no
   S081–S086 row to re-open (HEAD: 82 rows).
3. **P11 `census=ok`.** Measured invariant: the census validates the registry, and it returns the same
   verdict for the pre-append 82-row registry and the landed 88-row one —

   ```
   $ sources-census.sh validate --root /home/vgpnk/Projects/shokunin --file <HEAD copy>/corpus/SOURCES.md
   file   W04 S040 … / W04 S076 … (14 identical warnings)   file   ok   …/corpus/SOURCES.md      exit=0
   $ sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
   kengaku W04 S040 … / W04 S076 … (the same 14 warnings)    kengaku ok …/kengaku-shokunin/corpus/SOURCES.md  exit=0
   ```

   So `census=ok` would print for a registry that never heard of round 30. Its only C1-sensitive code is
   **E11** (used-by target exists on disk): M13 (entry deleted) flips `census=fail`. Everything else the
   census adds is row hygiene (NF=13, enums, duplicate ids/URLs, E08 date validity) that the six rows
   happen to satisfy trivially.
4. **P2's "exactly the six ids"** is satisfied *in bytes* but the command's evidence for it is a
   cardinality — the clause is true the way a stopped clock is right. Verified: an entry citing
   `S001 S002 S004 S007 S008 S012` prints the frozen line, exit 0 (M1), and so does one citing three
   ids twice (M2/M11, 7 and 8 `source:` lines, 6 distinct).
5. **P10's "one"** is satisfied because nobody wrote a second row, not because a second row is
   impossible: duplicate row (M6) and HTML-commented row (M19) both pass.

## 3. Clauses the counter cannot test (beyond the sibling's list)

Overlap with `R30FxC1Counter.md` §3 and `R30CritC1.md` B1–B6 is credited there, not re-claimed. What I
found that those do not carry:

* **N1 — line multiplicity of `source:` lines.** The sibling shows *new distinct* ids are caught
  ("seventh `source:` id added → cited_rows=7, exit 1"). Duplicates are not: 8 lines with 6 distinct
  ids → `cited_rows=6`, exact frozen line, exit 0 (M11); same with 7 lines (M2). The sentence's word is
  "lines"; the command counts distinct ids. A reader who takes §2's "seventh id caught" as covering
  line count will mis-derive the predicate. (The landed entry has exactly 6, so this is a
  non-discrimination, not a defect in the bytes.)
* **N2 — comment-shaped index rows.** The code comment at `:76` names comments and tests them not at
  all; M19 (row inside `<!-- … -->`) passes. Distinct from the sibling's fenced-block probe.
* **N3 — locator completeness inside a `source:` line.** The S084 header says
  "`数据污染评估`, the two documented methods (html lines 344 and 397)" and then quotes **three** spans;
  the registry row places the third (`但如今开源社区往往只会公开模型参数而非训练数据集`) at **line 315**, and
  the string `315` does not occur anywhere in the entry (`ent.count("315")` → 0). So one quoted span in
  the landed entry has no locator in its own header. P2 tests only the id token per line, so this is
  invisible; the C3 quote gate (out of my scope) is the only thing that could see it.
* **N4 — the flip's re-open has no encoded state.** P8 is the only clause in the sentence that could
  witness "re-opened", and equality on a freshly minted row is true whatever the seat did. `recheck:
  180d — re-fetch S081–S086 … (next due 2027-04-23)` records the intent to re-fetch *later*, i.e. the
  entry itself says the re-fetch is future work. Whether the six sources were actually re-opened on
  2026-10-25 is attested only by `verified-at`/`opened` strings and by seat prose; the round's fetch
  captures are not in the lane (`corpus/evidence/round30/` = `adoption-after.txt`,
  `census-after.txt`, `gate-selftest-after.txt`, `r29-counter-unchanged.txt`, `rows-opened.tsv`). One
  partial, checkable signal in the bytes: of the 13 quoted spans, **8 do not occur in the staged
  shokuknow card** and 5 do (`目前该方案仅支持 GSM8K…`, `…C-Eval, MMLU…`, `采用动态方式构建…`,
  `一致したもの…`, and the bare `方升`), and S082's URL/locators were corrected from `/abs/` + `# Benchmark Governance` to
  `/html/…v2` + §7.3/§8.2 — evidence that re-location happened, which the frozen sentence cannot see and
  the control cannot reward.
* **N5 — the passport clause is silent about the four surfaces it names.** The sentence says "one index
  row"; the landed README carries **three** mentions (index `:65`, coverage `:242`, frontier `:275`).
  Only the first is tested; the claim's own axis verdict is about the third.

Already attributed elsewhere: entry content (B4/§3.1), `opened` unread (B1/§3.6), id identity
(B2/§1b), expect-file literal (M17: edit `access_date`→`2026-01-01` **and** entry `verified-at`→
`2026-01-01` → exit 0; same class as B6), kill rule with no code path (§3.7), census binding to a
sibling conf (§1g/h).

---

## 4. Verdict: is the predicate one sentence a reader can re-derive?

**As a description of the bytes: yes.** I re-derived all of §1 from six files and two commands in one
sitting, and every clause holds. Three literals were wrong-only-in-the-staged-version and are correct in
the landed entry (S082 URL/section, `verified-at`, S077 removed from the header).

**As a test: no.** The sentence claims a three-way identity — "one sentence, same condition in the
counter's code, same label in the receipt" (`plans/round-30-claims.md` §C1). Three of its conditions are
**not in the code**: identity of the six ids (P2/P3), uniqueness of the index row (P10), and
`opened=2026-10-25` (P8); one is in the code but **invisible in the receipt's line** (P5); one is
satisfied independently of the claim (P11 `census`); and one clause the ticket names ("no other S-id
anywhere") **is not in the sentence**. A reader applying the sentence literally — as the ticket does —
will accept eight `source:` lines, a body-only `S091`, `opened=2026-01-01`, two index rows, and a
commented-out index row: I ran all five and got the frozen pass line each time. Conversely the sentence
rejects nothing the command accepts.

Saturation read: the predicate is **not a false claim** — it is a *plumbing* claim wearing a *knowledge*
claim's sentence. The pass line is a real, monotone kill of the do-nothing round (§0 control reproduces
byte-for-byte), so C1 is not a "do-nothing scores" failure; it is an **under-specified sentence**, and
the sentence is the frozen artifact a reader is asked to re-derive.

## 5. Smallest safe corrections (recommended, not applied — this seat writes no lane byte but this file)

1. **Do not patch round 30.** The claims preamble forbids a predicate change after seats scored; a
   widened predicate is a round-31 claim, not this one. Record the divergence as the round-30 record:
   P2/P3/P8/P10 are byte-clauses with no code path, and P5 is a code-clause with no line.
2. **Round-31 shape:** four counted fields in the same command and one line —
   `ids_match=1` (set equality: cited ids == `entry["sources"]`), `source_lines=6` (`^source:` line
   count == `required`), `opened_ok=6` (`registry[id][8] == access_date`), `index_rows=1` (exact count
   of the anchored row, after stripping HTML comments and fenced blocks). That is ~10 lines in
   `adoption_check.py` and turns the four "accident" clauses into failures.
3. **Pin the expect file** by sha256 inside `plans/round-30-claims.md` (round 29 pinned its baseline;
   round 30 pins nothing), so `2026-10-25` and the six-id list cannot move silently.
4. **Locator hygiene for the landed entry:** add `line 315` to the S084 `source:` header (or move the
   third span out of that row). One-character-class fix, and it makes the row re-derivable without the
   registry beside it.
5. **If the flip's re-open is load-bearing**, give it a state: an expect field
   `"prior_open": {"S081": "2026-10-23", …}` compared against the campaign ids, or a row cell that
   records both dates. As frozen, "re-opened in a later round" and "minted today" are the same bytes.

---

## 6. Mutants I ran (each on a `/tmp` copy; lane untouched)

Every probe is `cp -a` of the worktree under a `/tmp` root with the 21-byte harness conf, then
`python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census`.
`pass line` below = `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok`.

| id | mutation | printed line | exit | what it proves |
|---|---|---|---|---|
| — | none (worktree copy) | pass line | **0** | baseline reproduces the frozen sentence |
| — | `git archive HEAD` + expect file | `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok` | **1** | committed tree prints C1's control line (§0) |
| M1 | six `source:` ids → `S001 S002 S004 S007 S008 S012` | pass line | **0** | identity of the six ids untested (P2/P3) |
| M2 | 7th `source:` line, duplicate `S081` | pass line | **0** | line count untested (N1) |
| M3 | S083 `opened=2026-01-01` | pass line | **0** | `opened` unread (P8) |
| M4 | S083 `status=rejected` | `… rows_mined=5 …` | **1** | `status` **is** tested (P7) |
| M5 | S084 `used-by` → another entry | `… usedby_ok=0 …` | **1** | `used-by` **is** tested (P9) |
| M6 | second identical README index row | pass line, `indexed=1` | **0** | "one" index row untested (P10a) |
| M7 | `S091` added in prose, no `source:` line | pass line | **0** | no-other-S-id clause untested (P4) |
| M8 | `verified-at: 2026-10-24` | pass line | **1** | silent gate: the receipt's line cannot witness P5 |
| M11 | 8 `source:` lines, 6 distinct | pass line | **0** | same as M2, at a larger multiplicity (N1) |
| M13 | entry file deleted | `entries=0 indexed=1 … usedby_ok=1 census=fail` | **1** | census E11 is the only C1-sensitive census code (§2.3) |
| M14 | one `source:` line indented 4 spaces | `… cited_rows=5 …` | **1** | `^source:` is column-0 strict — counter stricter than the sentence's word "lines" |
| M16 | entry body replaced by 6 `source:` lines + `verified-at` + `# Stub` | pass line | **0** | content untested (agrees with `R30CritC1` B4) |
| M17 | expect `access_date`→`2026-01-01` **and** entry `verified-at`→`2026-01-01` | pass line | **0** | the literal date is enforced only through a mutable, unpinned expect file |
| M19 | README index row wrapped in `<!--` … `-->` | pass line, `indexed=1` | **0** | `:76`'s comment claim ("not a mention inside a comment") is false (N2) |

Negative results kept (no defect in the bytes, only in the sentence): the ternary read of every clause
in §1 stands, `git status --porcelain plans/adoption_check.py` is empty (tool unchanged from round 29),
and round 29's own expect file still prints its frozen line on the landed tree.
