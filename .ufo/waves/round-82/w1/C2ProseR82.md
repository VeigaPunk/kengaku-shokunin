# C2ProseR82 — R82-C2 prose repairs (V2, V3, V6)

Seat `C2ProseR82`, role scribe, kengaku round 82 wave w1 (12 seats), hyaku run 15 attempt 1.
Measured tip `12f1029a45cf0097a3afd030d757bf93b87f8018` (`git rev-parse master`, 2026-11-04
06:34:49 -0300 — the freeze commit; no integration commit existed when this report was written).
Base revision for every "before" state: `a3a03ac31451e58f1742b9bccb73b72c2d90a95c`. Frozen claims
read in full: `plans/round-82-claims.md`.

This seat wrote exactly one file: this report. No lane file was created, modified, committed or
pushed; no gate, counter, selftest, mutant battery or control was executed; no fixture repo and no
scratch tree were created (all analysis ran in-process, read-only). One network action: three
`curl` fetches of the S261 pinned upstream documents, to re-derive the S261 line anchors (§2.5).

Target bytes at the tip, so the integrator can confirm the same bytes are being edited:

```
$ sha256sum corpus/lessons/round-81.md corpus/SOURCES.md corpus/knowledge/tb2-file-artifact-replay-classes.md
ca60458ce55436f36537c16ff79ef618cd8f02fd646e2161edb0926aec92900f  corpus/lessons/round-81.md
d8ff325b8f99779ff6db45d311741268b6ac07fa813fbbbbaee123de051e3f6b  corpus/SOURCES.md
e5f3edf2b1ea64122a8f8de178bd96b0c7d35ca99cff5d50671f5948379a181c  corpus/knowledge/tb2-file-artifact-replay-classes.md
$ wc -l corpus/lessons/round-81.md corpus/SOURCES.md corpus/knowledge/tb2-file-artifact-replay-classes.md
   114 corpus/lessons/round-81.md
   309 corpus/SOURCES.md
    68 corpus/knowledge/tb2-file-artifact-replay-classes.md
```

Every file this report quotes — the three above, both round-81 receipts and both round-80 receipts
used for the S259 anchor — is byte-identical to `HEAD`: `git show HEAD:<path> | sha256sum` equals
`sha256sum <path>` for all seven (7/7 `same-as-HEAD`), so the working-tree bytes I measured are the
tip's bytes.

---

## 1. Method

Three surfaces, three measurements, no inference:

1. **Quote counts.** Every `(<n> words)` / `<n> words` claim in `corpus/lessons/round-81.md`
   (3 claims) and `corpus/SOURCES.md` (131 claims across 309 lines) was extracted with its quoted
   span and recomputed. A plain `grep -oE '\(?[0-9]+ words?\)?'` finds **132** strings in
   `SOURCES.md`; the 132nd is `SOURCES.md:237` `the old anchor annotated the :5 quote as (6 words)`,
   which quotes a superseded annotation instead of asserting a count, so 131 claims were scored.
   The span is taken from the quote delimiter that closes immediately before the count back to its
   opening delimiter (curly `“…”`, straight `"…"`, or backtick), accepting only gaps of ≤6
   characters (` (`, `; `, `, `); straight-quote nesting is resolved outward from the `:NN` anchor
   (the three such rows are named in §2.5). Wrapped quotes are joined before counting.
2. **Receipt line numbers.** `grep -n` over the two round-81 receipts for
   `MEMBER|MINTED_BY_SHA|OBSERVATIONS_BEGIN` and the first `CASE` line.
3. **Upstream anchors (S261).** `curl` of the three pinned `2fd12b88` documents, printing
   lines 1/6/9, to confirm the cited lines carry the quoted text.

The counting rule, stated so any reader can re-derive every number:

> **A quoted span's word count is the number of whitespace-separated tokens in the quoted text as
> printed (`len(quote.split())`): punctuation stays attached to its token, backticks and ellipses
> are tokens, and the count is of the printed fragment, never of the surrounding sentence.**

That is not this seat's invention: `plans/anchor_line_check.py` (landed, round 46/58) defines the
same test — "`(<K> words)` written right after the quote equals the quote's whitespace-token count
(`len(quote.split())`, the `wc -w` convention)" — and uses the S201 6-vs-5 miscount as its
`ESC-WORDS` falsifier fixture, which is one of the further mismatches in §2.5.

---

## 2. V2 — the annotation miscounts

### 2.1 Target values (recomputed)

```
$ python3 - <<'PY'
q=["# tb2 log-summary-date-ranges grader probe (round 81)",
   "Write a CSV file /app/summary.csv with the following structure (including the header):",
   "The goal is to extract this secret key and save it to /app/results.txt.",
   "Evaluates the ability to analyze date-stamped log files, calculate counts across multiple date ranges, and generate structured CSV output."]
for s in q: print(len(s.split()), s)
PY
7 # tb2 log-summary-date-ranges grader probe (round 81)
12 Write a CSV file /app/summary.csv with the following structure (including the header):
13 The goal is to extract this secret key and save it to /app/results.txt.
19 Evaluates the ability to analyze date-stamped log files, calculate counts across multiple date ranges, and generate structured CSV output.
```

So: S260's quote is **7**, S261's first quote is **12**, S261's second quote is **13**, and the
`task.toml` quote's **19** is already correct.

### 2.2 Receipt layout (recomputed)

```
$ grep -n "MEMBER\|MINTED_BY_SHA\|OBSERVATIONS_BEGIN" corpus/evidence/round81/log-summary-date-ranges-probe.txt
2:MEMBER log-summary-date-ranges
14:MINTED_BY_SHA eb6297f6b661fe54d4ca07d61bc89f07af379d7dac529da84d05d6fa84b5715d
15:OBSERVATIONS_BEGIN
$ sed -n '16p' corpus/evidence/round81/log-summary-date-ranges-probe.txt
CASE exact-15-rows predicted=P observed=P rc=0 legs=PP violates=-
$ wc -l corpus/evidence/round81/log-summary-date-ranges-probe.txt
30 corpus/evidence/round81/log-summary-date-ranges-probe.txt
```

`vulnerable-secret-probe.txt` has the identical layout (`2` MEMBER, `14` MINTED_BY_SHA,
`15` OBSERVATIONS_BEGIN, `16` first CASE). Therefore the stamp block is **2-14**, the
observations-begin marker is line **15**, and observations start at **16** — not `2-16`/`17`.
The receipt's own title line is 1, so the subject-plus-stamp anchor is **1-15** (the range the
lesson already states).

### 2.3 Corrected strings — `corpus/lessons/round-81.md` (Gate, S261 bullet)

The file's identity at the tip is in the header (sha256 and `wc -l`); `(14 words)` and `(17 words)`
each occur exactly once in the file, `(19 words)` once.

```text
:49  -  with the following structure (including the header):" (14 words); `vulnerable-secret/instruction.md:1`
:49  +  with the following structure (including the header):" (12 words); `vulnerable-secret/instruction.md:1`

:50  -  — "The goal is to extract this secret key and save it to `/app/results.txt`." (17 words);
:50  +  — "The goal is to extract this secret key and save it to `/app/results.txt`." (13 words);
```

`round-81.md:52` `(19 words)` is correct and must not be touched. `round-81.md:42`'s anchor
`:1-15` for S260 is also correct as it stands (it ends on `OBSERVATIONS_BEGIN`). The file's
continuation indent is two spaces; the diff above shows it stripped for readability, and the only
bytes that change are the counts themselves (`(14 words)`→`(12 words)`, `(17 words)`→`(13 words)`,
one occurrence each in this file).

Optional (not required by the frozen predicate, and not recommended if `u2` does exact-text
matching): append `Word counts are whitespace-split tokens of the quoted text.` to the S261 bullet.

**Companion block — a dated correction in the same lesson's `## Corrections` section.** The lesson
is the only in-place edit this claim needs, and the round-81 precedent (`R80-U1`, `R80-U6`) puts the
correction record there. Append to `corpus/lessons/round-81.md` §Corrections:

```markdown
- **R81-V2 — the S261 counts and the S260 anchor were overstated.** Re-read at the round-82 tip
  (`12f1029a`): the `instruction.md:9` quote is 12 whitespace-split tokens and the
  `vulnerable-secret/instruction.md:1` quote 13 (the cells said 14 and 17); the S260 receipt's stamp
  runs 2-14 (`MEMBER` at 2 through `MINTED_BY_SHA` at 14) with `OBSERVATIONS_BEGIN` at 15 and the
  first observation at 16, and its title quote is 7 tokens, not 9. The rule is `len(quote.split())`
  over the quoted text — the same test `plans/anchor_line_check.py` applies to every registry
  anchor. Corrected by **S262** (supersedes S260) and **S263** (supersedes S261); S260's and S261's
  own bytes are unchanged (QUALITY Q34).
```

This block is what makes the lesson a legitimate `close` artifact for the `R81-V2` row: its bytes
carry the id and the corrected literals (`12 whitespace-split tokens`, `stamp runs 2-14`,
`observations from 16`, `7 tokens`). The C2 counter seat picks which literal the row registers.

### 2.4 The SOURCES repair is a new row, not an in-place cell edit

`corpus/SOURCES.md` is append-only, and one of the two statements is this lane's own criterion:

- **`corpus/QUALITY.md:761` Q34** — "every cell of a `corpus/SOURCES.md` registry row except
  `status`, `recheck` and `used-by` is immutable under its id: a correction lands as a NEW row whose
  `teaches` cell opens `supersedes S0NN —`, and an in-place change is a rule-2 defect even when the
  round wrote the row itself and the cell it corrects is its own anchor." The `anchor` cell is a
  cell; S260's and S261's defects are both in it.
- **`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:47-51`, rule 2** (fleet-frozen) — "Append-only. Only
  `status`, `recheck` and `used-by` change in place … A correction is a new row whose `teaches` opens
  `supersedes S0NN —`."

The lane's own landed gate already implements that shape: `plans/anchor_line_check.py:27-29` says a
defective row "is `repaired` iff some row whose `teaches` cell opens `supersedes` naming its id is
itself captured, carries at least one line-cited quote, and has zero defects." (That gate also
applies the identical counting rule — its docstring's `words` statement is `len(quote.split())`,
"the `wc -w` convention", and its `ESC-WORDS` selftest fixture is "the landed S201 shape", i.e. the
6-vs-5 miscount I report in §2.5.)

So the V2 repair lands as **two new rows**; S260's and S261's bytes stay untouched. Next free ids in
this lane's namespace: **S262, S263** (`grep -oE '^\| S[0-9]+' corpus/SOURCES.md | sort -V | tail -1`
→ `| S261`; `grep -cE '^\| S26[23] ' corpus/SOURCES.md` → `0`).

#### Paste block — two rows, appended after S261 (11 cells, header `corpus/SOURCES.md:20`)

```markdown
| S262 | kengaku round-81 located replays — correction row superseding S260, same source and capture — plans/round81_log_summary_probe.py, plans/round81_vulnerable_secret_probe.py, plans/round81_probes.json, plans/round81_c1_new_members.py, corpus/evidence/round81/<member>-probe.txt (two) | own-work | A | two stdlib-only file-artifact population members replayed offline at the measured tip, with a pinned subject capture and a pinned replay environment | corpus/evidence/round81/log-summary-date-ranges-probe.txt:1-15 (subject at 1, stamp 2-14, OBSERVATIONS_BEGIN 15, observations from 16); quote “# tb2 log-summary-date-ranges grader probe (round 81)” (7 words, line 1); TOOL_SHA and HOST_PYTHON/HOST_OPENSSL in the stamp | supersedes S260 — the anchor placed the stamp at 2-16 with observations from 17 and counted the quote as 9 words; the stamped block runs 2-14 (MEMBER at 2 through MINTED_BY_SHA at 14), OBSERVATIONS_BEGIN is 15 and the first observation 16, and whitespace-split the quote is 7 tokens (“#”, “tb2”, “log-summary-date-ranges”, “grader”, “probe”, “(round”, “81)”); recorded by round 82’s R81-V2 repair | mined | 2026-11-04 | 2027-01-18 | corpus/knowledge/tb2-file-artifact-replay-classes.md, corpus/lessons/round-81.md, corpus/lessons/round-82.md |
| S263 | Terminal-Bench 2.0 pinned task documents (tree 2fd12b88) — correction row superseding S261, same source and capture — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/log-summary-date-ranges/instruction.md plus task.toml, vulnerable-secret/instruction.md, vulnerable-secret/task.toml | docs | A | what the two replayed tasks ask the agent to produce, at the pinned revision the round-52 capture came from | instruction.md:9 quote “Write a CSV file /app/summary.csv with the following structure (including the header):” (12 words); vulnerable-secret/instruction.md:1 quote “The goal is to extract this secret key and save it to /app/results.txt.” (13 words); fetched 2026-11-04T08:26:13Z | supersedes S261 — both counts were overstated: 14 → 12 and 17 → 13 whitespace-split tokens; both fragments are verbatim at the cited lines, re-fetched HTTP 200 at 2fd12b88 on 2026-11-04; recorded by round 82’s R81-V2 repair | mined | 2026-11-04 | on-release | corpus/knowledge/tb2-file-artifact-replay-classes.md, corpus/lessons/round-81.md, corpus/lessons/round-82.md |
```

Both `teaches` cells open exactly `supersedes S26N —`, which is the regex both landed tools use
(`plans/anchor_line_check.py:71`, `plans/round46_c3_verify.py:147`).

**Optional strengthening (gate-observable S262 anchor).** As drafted, neither S260 nor S262 is
visible to `plans/anchor_line_check.py`: the gate needs a line-cited quote in straight quotes
(`:N "…"`) plus a 64-hex `sha256` token naming a tracked capture, and S260's anchor has curly quotes
and no digest. If the L1 wants the corrected anchor actually policed, use this anchor cell for S262
instead — it parses as line 1, range 1-15 (30-line file, contains 1), `len(quote.split())` = 7, and
the digest is the tracked receipt's:

```text
corpus/evidence/round81/log-summary-date-ranges-probe.txt:1-15 (subject at 1, stamp 2-14, OBSERVATIONS_BEGIN 15, observations from 16), :1 "# tb2 log-summary-date-ranges grader probe (round 81)" (7 words); TOOL_SHA and HOST_PYTHON/HOST_OPENSSL in the stamp; sha256 7c8d3f5656edc2affbd594cc4c33c796e01dc51852d5b00100fc1a8455f81e78
```

S263 cannot be captured locally — its quotes live in the pinned upstream documents, and S261 carries
no evidence file for them — so it stays prose-verified (HTTP 200 re-fetch, §2.6).

#### Required companion — Gate bullets for the two new rows

Contract rule 1 requires every new row to be recorded in the round lesson's `## Gate` with URL,
access date and a ≤25-word quote with its location. For `corpus/lessons/round-82.md`:

```markdown
- **S262 (own-work, tier A, supersedes S260)** — `corpus/evidence/round81/log-summary-date-ranges-probe.txt`
  (and `vulnerable-secret-probe.txt`), re-anchored. Access 2026-11-04; anchor `:1-15` (subject at 1,
  stamp 2-14, `OBSERVATIONS_BEGIN` 15, observations from 16). Quote (`:1`):
  `# tb2 log-summary-date-ranges grader probe (round 81)` (7 words). Repairs R81-V2.
- **S263 (docs, tier A, supersedes S261)** — the pinned TB2 task documents at `2fd12b88`, re-fetched
  2026-11-04, HTTP 200 each. Quotes: `log-summary-date-ranges/instruction.md:9` — "Write a CSV file
  /app/summary.csv with the following structure (including the header):" (12 words);
  `vulnerable-secret/instruction.md:1` — "The goal is to extract this secret key and save it to
  `/app/results.txt`." (13 words). Repairs R81-V2.
```

#### The predicate reading this lands on — an L1 ruling, not a scribe edit

With S260/S261's own cells untouched, R82-C2's V2 sentence read literally ("what … S260/S261 state
equals a mechanically recomputed value") is still **false**. It is true only under the reading the
registry and `anchor_line_check.py` already use for defect state: an id's current statement is its
row plus its `supersedes` chain, so `S260`'s stated count is S262's 7 and `S261`'s are S263's 12/13.
`u2` must be written against whichever reading the L1 rules, and must say which. If the L1 instead
rules the literal row-dominant reading, the only way to satisfy it is the in-place edit in §2.4b,
which Q34 calls a rule-2 defect; Q34's own text records that no lane tool reads committed history to
enforce it, so that choice is a rule question, never a passing gate.

Two mechanical requirements follow for `u2` under either reading: it must assert the **presence** of
the superseding row(s) and their `supersedes S26N —` prefix itself, and it must not delegate that to
`plans/anchor_line_check.py` — that gate is blind to curly-quoted, capture-less rows (its `QUOTE_RE`
needs `:N "`, its `SHA_RE` a `sha256 <64hex>` token) and its `live=0` persists even if S262/S263 are
deleted. The straight-quote + `sha256` variant above makes the **word-count** leg real for the new
row; it supplies no presence leg.

#### 2.4b Fallback — the in-place patch (rule-2 defect under Q34; do not apply without the ruling)

```text
corpus/SOURCES.md:276  (row S260, anchor cell column)
-  corpus/evidence/round81/log-summary-date-ranges-probe.txt:1-17 (subject at 1, stamp 2-16, observations from 17); quote “# tb2 log-summary-date-ranges grader probe (round 81)” (9 words, line 1)
+  corpus/evidence/round81/log-summary-date-ranges-probe.txt:1-15 (subject at 1, stamp 2-14, OBSERVATIONS_BEGIN 15, observations from 16); quote “# tb2 log-summary-date-ranges grader probe (round 81)” (7 words, line 1)

corpus/SOURCES.md:277  (row S261, anchor cell column)
-  instruction.md:9 quote “Write a CSV file /app/summary.csv with the following structure (including the header):” (14 words); vulnerable-secret/instruction.md:1 quote “The goal is to extract this secret key and save it to /app/results.txt.” (17 words)
+  instruction.md:9 quote “Write a CSV file /app/summary.csv with the following structure (including the header):” (12 words); vulnerable-secret/instruction.md:1 quote “The goal is to extract this secret key and save it to /app/results.txt.” (13 words)
```

The search strings must include the surrounding anchors: in `SOURCES.md` `(14 words)` occurs 3 times
and `(17 words)` 5 times, so a bare count substitution would hit the wrong row. The `-` lines above
are byte-exact substrings of the tip (verified), the `+` lines are not present at the tip.

### 2.5 Further mismatches found (reported, not fixed — no guessing)

Every other count in both files was recomputed the same way. `round-81.md`'s third count (19) is
correct; the only lesson defects are the two above. In `corpus/SOURCES.md`, 12 rows disagree with
their own printed quote under the frozen rule — 9 genuine, 1 rule-dependent, 2 superseded history.
Line numbers at the tip:

| file:line | row | stated | computed | evidence for the correct value | class |
|---|---|---|---|---|---|
| `SOURCES.md:123` | S108 | 6 | **5** | the identical quote at `:172` (S157) states 5 | genuine |
| `SOURCES.md:157` | S140 | 9 | **4** | the printed quote is the truncated fragment `keys = ["0x68e63", ...]`; S217 (`:232`) quotes the full line and states 6 | superseded (S217) + truncated quote |
| `SOURCES.md:165` | S150 | 8 | **9** | S159 (`:174`) states 9 for the identical quote | genuine |
| `SOURCES.md:166` | S151 | 4 | **3** | S160 (`:175`) states 3 | genuine |
| `SOURCES.md:167` | S152 | 4 | **3** | S161 (`:176`) states 3 | genuine |
| `SOURCES.md:168` | S153 | 6 | **4** | S162 (`:177`), `:121`, `:124`, `:148`, `:182` all state 4 | genuine |
| `SOURCES.md:170` | S155 | 3 | **4** | S164 (`:179`) states 4 | genuine |
| `SOURCES.md:193` | S178 | 20 | **22** | 20 = 22 minus the two `…` separator tokens (`…` is a token under the frozen rule) | rule-dependent |
| `SOURCES.md:216` | S201 | 6 | **5** | S213 (`:228`) states 5 | genuine |
| `SOURCES.md:222` | S207 | 4 | **3** | no duplicate row; `solver = eigenpy.EigenSolver(matrix)` splits into 3 tokens | genuine |
| `SOURCES.md:223` | S208 | 17 | **16** | no duplicate row; the printed sentence splits into 16 tokens | genuine |
| `SOURCES.md:236` | S221 | 6 | **7** | S222 (`:237`) states 7 **and names the stale value**: "the old anchor annotated the `:5` quote as (6 words)" | superseded — leave as history |

Three rows that a naive parser reports as mismatches are **not** defects: `:126` (5), `:127` (3),
`:128` (7) carry nested straight quotes (`"assert "TEST PASSED" in result.stdout"`); counting from
the outer span reproduces the stated numbers exactly. `:49` of the lesson (`14 words → 12`) and the
two S261 counts are the only defects inside V2's named scope.

Two S259 anchor claims were re-derived and are correct: `lines 2-12` (MEMBER at 2, MINTED_BY_SHA at
12, `OBSERVATIONS_BEGIN` at 13 in `cancel-async-tasks-probe.txt`; `HISTORICAL-DIVERGENCE` at 13 in
`protein-assembly-probe.txt`). The lesson's `lines 1-10` is quoted **superseded S258 text**, not a
live anchor, and must not be "corrected".

### 2.6 Upstream anchors (S261) — re-derived, HTTP 200

```
$ for u in log-summary-date-ranges/instruction.md vulnerable-secret/instruction.md log-summary-date-ranges/task.toml; do
    curl -sS -o /dev/null -w "$u http=%{http_code}\n" \
      "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/$u"; done
log-summary-date-ranges/instruction.md http=200
vulnerable-secret/instruction.md http=200
log-summary-date-ranges/task.toml http=200
```

- `log-summary-date-ranges/instruction.md:9` = `Write a CSV file /app/summary.csv with the
  following structure (including the header):` ✔ (12 tokens, verbatim)
- `log-summary-date-ranges/task.toml:6` = `description = "Evaluates the ability to analyze
  date-stamped log files, …structured CSV output."` ✔ (quoted fragment 19 tokens, verbatim)
- `vulnerable-secret/instruction.md:1` = `Analyze the following program that contains a secret key.
  The goal is to extract this secret key and save it to \`/app/results.txt\`.` — the cited line is
  correct and the quoted fragment is verbatim **except** that line 1 writes `/app/results.txt`
  inside backticks while the S261 cell (and only that cell; the lesson keeps them) drops them.
  The token count is unaffected (13 either way). Recorded as a fidelity note, not a count defect.

---

## 3. V3 — the provenance trio

### 3.1 Insertion point

Target `corpus/knowledge/tb2-file-artifact-replay-classes.md`. Insert the three lines **as the first
three lines of the file**, followed by one blank line, before the existing H1
`# TB2 file-artifact graders: two stdlib-only replays and the host pin`. This is the layout of the
admitted entries (`corpus/knowledge/attribution-interval-calibration.md:1-5`), and it satisfies
`corpus/QUALITY.md` Q1, which requires the first three lines to *be* the trio.

### 3.2 Paste block

```markdown
source: S260 — own-work, `corpus/evidence/round81/log-summary-date-ranges-probe.txt:1-15` and `corpus/evidence/round81/vulnerable-secret-probe.txt:1-15` (subject at 1, stamp 2-14, `OBSERVATIONS_BEGIN` 15, observations from 16); S261 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/ — `log-summary-date-ranges/instruction.md:9`, `log-summary-date-ranges/task.toml:6`, `vulnerable-secret/instruction.md:1`; S256 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md — `corpus/evidence/round79/sources/tb2-readme.md:24`
verified-at: 2026-11-04 (round-82 tip 12f1029a45cf0097a3afd030d757bf93b87f8018)
recheck: 2026-12-04 (30d) — re-run `python3 plans/round81_log_summary_probe.py --lane . --work "$(mktemp -d)"` and `python3 plans/round81_vulnerable_secret_probe.py --lane . --work "$(mktemp -d)"`: each must print `cases=12 observed_pass=4 observed_fail=8 mismatches=0` and `PREDICATE R81-C1 pass` and exit 0, with `SUBJECT_SHA`/`TOOL_SHA`/`HOST_PYTHON`/`HOST_OPENSSL` matching the receipts; then `python3 plans/round81_c1_new_members.py --lane .` (its stamp leg prints `HOST-PYTHON-MISMATCH`/`HOST-OPENSSL-MISMATCH` at `plans/round81_c1_new_members.py:330-334`); re-open S261 if either tally moves
```

(One line each — the markdown block above wraps only for display; do not insert hard wraps.)

### 3.3 Why these bytes

- **`source:` ids.** The entry's load-bearing claims are the two offline replays (S260) and the
  pinned task documents (S261); its closing `Sources:` line already names S260, S261, S256, so S256
  is carried with its own anchor (`corpus/evidence/round79/sources/tb2-readme.md:24`, the harness
  README capture that fixes "TB2 run = containerized run").
- **Anchors.** `:1-15` is the corrected S260 anchor from §2.4 — V2 and V3 must land together, or V3
  cites an anchor V2 has not yet repaired. `verified-at` carries the tip measured here.
- **`recheck:` names the real instruments.** All three scripts exist at the tip
  (`plans/round81_log_summary_probe.py`, `plans/round81_vulnerable_secret_probe.py`,
  `plans/round81_c1_new_members.py`) and accept the named flags (the receipts' `COMMAND` lines show
  `--lane . --work …` for both probes; `python3 plans/round81_c1_new_members.py --help` lists
  `--lane`, `--rev`, `--work`, `--selftest`, `--mutants`). The expected literals
  `cases=12 observed_pass=4 observed_fail=8 mismatches=0` and `PREDICATE R81-C1 pass` are the tally
  and verdict lines committed in both receipts (`…-probe.txt:28-29`).
- **Not used as the recheck:** the round-82 counter (`plans/round82_c2_closure_debt.py`) is the
  *closure* instrument for this round's claim, not a re-derivation of the entry's replay, and it is
  not on disk at the tip — naming it would be a placeholder, which the item forbids.

### 3.4 Tip-refresh caveat

`verified-at:` pins the tip measured here. If integration lands commits after `12f1029a`, refresh
only the parenthetical sha to `git rev-parse master` at integration (the date `2026-11-04` and the
rest of the line stay). This is a one-token edit; do not re-date the entry.

---

## 4. V6 — the wave record

### 4.1 Status of the tally source: absent

```
$ ls .ufo/waves/round-82/w1-results.json .ufo/waves/round-82/w1/w1-results.json
ls: cannot access '.ufo/waves/round-82/w1-results.json': No such file or directory
ls: cannot access '.ufo/waves/round-82/w1/w1-results.json': No such file or directory
```

`.ufo/waves/round-82/` contains only `build_spec.py`, `w1-spec.json`, `w1.ready`,
`w1.ready.dispatched` and `w1/` (`swarm-registry.json`, `w1-dispatch.json`, `w1-validate.stderr`).
No results file exists at either candidate path, so the paragraph below carries the literal
`TALLY_PENDING` in place of every number, exactly as the item directs. **No tally was invented.**

### 4.2 Paragraph — target `corpus/lessons/round-82.md`

Insertion point: a new subsection in the wave-record area, immediately after the round's wave
composition sentence and before the per-seat findings — i.e. the position `## Wave findings (amended
after w1)` occupies in `corpus/lessons/round-80.md:114`. Suggested heading:
`### Attack share and the planner seat (R82-C2 V6)`.

```markdown
### Attack share and the planner seat (R82-C2 V6)

The round ran one v1 wave of TALLY_PENDING seats; `.ufo/waves/round-82/w1-results.json` gives the
role tally TALLY_PENDING. Against the campaign list (reviewer, critic, mutation-tester, labrat) the
wave carries TALLY_PENDING attack seats — `ReviewerR82`, `CriticR82`, `MutationR82` — TALLY_PENDING
of TALLY_PENDING = TALLY_PENDING %, the 25 % floor met (round 81 recorded 3/14 = 21 % on the same
list, and counted its sentinel to reach 29 %: spot-check C-D2). The mutation-tester seat `MutationR82`
is live: output length TALLY_PENDING, so the round has the independent mutation pass round 81 did not
deliver (`MutationGateR81` died with empty output, spot-check C-D3). No seat carries `planner`: the
L1 `KengakuR82` holds the canonical §3 planner seat under the orchestrator's 2026-10-19 ruling —
"the validator rejects `planner` — a frozen-topology seat, never a swarm role. You, the L1, hold the
canonical §3 planner seat; a bounded planning data-walk may ride a scout, connector or revenger
item. Record that mapping in the report; never bypass validation to add a planner"
(`scripts/hyaku/lane-addendum.md:251-255`, restating `.ufo/l0-questions.md:52`, the kama round-11 /
tsukuroi round-12 answer) — so the wave validator never sees a `planner` role and the round's plan
stayed with the L1 (`plans/round-82-claims.md`, freeze `12f1029a`).
```

### 4.3 Fill key — how to replace each `TALLY_PENDING`

Run once, then substitute in order of appearance:

```
python3 - <<'PY'
import json, collections
d = json.load(open('.ufo/waves/round-82/w1-results.json'))
c = collections.Counter(x['agent'] for x in d['results'])
attack = ('reviewer', 'critic', 'mutation-tester', 'labrat')
a = sum(c[k] for k in attack); tot = sum(c.values())
print('seats', d['seats'], 'results', len(d['results']))
print('roles', dict(c))
print('attack %d/%d = %.1f%%' % (a, tot, 100*a/tot))
print('attack seats', [x['name'] for x in d['results'] if x['agent'] in attack])
print('mutation-tester', [(x['name'], len(x.get('output') or '')) for x in d['results'] if x['agent'] == 'mutation-tester'])
PY
```

Occurrences in order of appearance: (1) `d['seats']`; (2) the role tally (e.g. `executor 5, scribe 2,
scout 1, connector 1, reviewer 1, critic 1, mutation-tester 1`); (3) and (4) the same attack-seat
count, once as prose and once as the fraction's numerator; (5) the denominator (`len(d['results'])`);
(6) the share `%.1f`; (7) the mutation-tester's output length. The round-81 file shows the schema
(`{lane, round, wave, seats, results:[{name, agent, output, note}]}`); a seat with `output == ""` is
dead and must be reported as dead, not dropped.

**If the mutation-tester's output length is 0**, the seat is dead and the frozen claim fails: replace
`is live: output length TALLY_PENDING` with `is dead (output length 0) — R82-C2 V6 fails on this
wave`, and record the dead seat in the report's defect list. Do not keep the "independent mutation
pass" sentence for a dead seat.

**If the measured share is below 25 %**, the frozen claim fails. Do not soften the sentence: replace
`the 25 % floor met` with `below the 25 % floor — R82-C2 V6 fails on this wave and the deficit is
reported, not smoothed`, and say so in the report's defect list.

### 4.4 Dispatch-declared roster — **not evidence, do not paste**

The results file is the only admissible tally. For orientation only, the *spec* at the tip declares
12 items (`python3 -c` over `.ufo/waves/round-82/w1-spec.json`, and `.ufo/waves/round-82/w1.ready.dispatched`
lists the same 12 names):

```
executor 5 (SweepGateR82, SweepHarvestR82, RegistryCounterR82, C2CounterR82, C2RepairR82)
scout 1 (PlansReconR82), scribe 2 (RegistryRowsR82, C2ProseR82), connector 1 (ConnectorR82)
reviewer 1 (ReviewerR82), critic 1 (CriticR82), mutation-tester 1 (MutationR82)
```

That would put the campaign-list attack share at 3/12 = 25.0 % with no labrat seat — but the spec
records what was *dispatched*, not what settled, and a dead seat still counts as dead. This block
must not be pasted into the lesson as a tally.

---

## 5. Findings for the L1 and the counter author (C2CounterR82 was messaged with the same)

1. **The results path in the frozen claim is not the harness's path.** The claim (and the `u6` spec)
   read `.ufo/waves/round-82/w1-results.json`; round 81's results landed at
   `.ufo/waves/round-81/w1/w1-results.json`, round 82's dispatch is
   `.ufo/waves/round-82/w1/w1-dispatch.json`, and round 82's `w1.ready` names that dispatch. If the
   run writes under `w1/`, a file must exist at the claim's path (a copy is the mechanical fix) or
   `u6` cannot pass on committed bytes. This is the single highest-risk item in V6.
2. **`u2` must join wrapped lines.** The lesson's S261 quotes wrap (`:48`→`:49`, `:51`→`:52`); a
   per-line quote extractor finds no quote and silently passes or silently fails. It must also take
   the outer span past nested straight quotes (`SOURCES.md:126-128`).
3. **`u2` must not "fix" labelled history.** Three strings here are historical quotations, not live
   claims: `round-81.md:38` / `SOURCES.md:275` quote S258's superseded `lines 1-10`;
   `SOURCES.md:236` (S221) states `6 words` where S222 (`:237`) supersedes it; and `SOURCES.md:237`
   itself repeats `the old anchor annotated the :5 quote as (6 words)` — the one `N words` string in
   `SOURCES.md` with no quote attached (the 132nd counted in §1). A checker that recomputes them
   without reading the supersede labels reports false defects, and one that treats the parenthetical
   quote as a claim finds nothing to count.

4. **`u3` should assert the trio is the first three lines**, not merely present (QUALITY Q1 says
   "the first three lines are"), plus: `source:` carries S260+S261, a URL, and an anchor; `recheck:`
   carries a date or cadence **and** at least one existing `plans/*.py` path.

5. **`u6` should read only the results file** and require a `mutation-tester` entry with non-empty
   `output`; deriving the tally from `w1-spec.json` would make the check self-fulfilling.

6. **S261 fidelity nuance (not a count defect).** `SOURCES.md:277`'s vulnerable-secret fragment drops
   the two backticks that upstream line 1 has around `/app/results.txt`; the lesson keeps them. No
   admit changes; the count is 13 either way. Left as-is because V2's mandate is the numbers, and
   changing quote text is a different repair.

7. **Worktree cleanliness: dirty when first measured, clean on re-measure — the mint rule survives in a
   narrower form.** First reading of this session, `git status --porcelain` printed three
   modifications outside this seat's scope:

   ```
    M corpus/evidence/round68/pypi/server-log.txt
    M corpus/evidence/round68/pypi/stderr/K1.txt
    M corpus/evidence/round68/pypi/stderr/K3.txt
   $ git diff -- corpus/evidence/round68/pypi/server-log.txt
   -127.0.0.1 - - [03/Nov/2026 19:58:58] "GET /simple/vectorops/ HTTP/1.1" 200 -
   +127.0.0.1 - - [04/Nov/2026 06:33:45] "GET /simple/vectorops/ HTTP/1.1" 200 -
   ```

   Re-measured at `2026-11-04T09:54:37Z`, all three are clean again
   (`git diff --numstat -- corpus/evidence/round68/pypi/` prints nothing), so a pre-freeze run's
   overwrite was reverted by another seat; the diff above is what it looked like, not the current
   state. What survives is the mint rule: the tree carries the round's own edits
   (`SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`, both knowledge entries,
   `corpus/lessons/round-81.md`), so a receipt minted from this worktree cannot honestly stamp
   `WORKTREE clean`; mint from a clean `git clone --shared` as the C2 repair item prescribes. Record
   whichever state you measure, **with its timestamp** — never this one.

8. **Shape-changing: SOURCES is append-only, so V2 cannot be a cell edit.** See §2.4 —
   `QUALITY.md:761` Q34 and `SOURCES-CONTRACT-v1.md` rule 2 both forbid in-place cell changes, and
   `plans/anchor_line_check.py:27-29` implements the supersede-row shape as the only "repaired"
   state. The repair is therefore **two new rows (S262, S263)**, plus the round-82 Gate bullets and
   the lesson's dated correction; S260's and S261's bytes stay untouched. A counter `u2` that reads
   `S260`/`S261` row-dominantly will fail on that shape — that is the L1's reading to rule, not a
   scribe's, and §2.4 states both sides.

9. **Adding two rows moves the registry count: `PROVINCE.md:1041` says `rows=253`** with
   `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`. After S262/S263 it is **255**, so the
   integrating seat must update that cell and its receipt; the frozen `253` readings in
   `SKILL.md:732` are stamped "measured at `12f1029a`" and stay true as history.

## 6. Limits

- No gate, counter, selftest, mutant or control was run by this seat; every gate number cited
  (round-81 `gates-clean.txt`, `c2-after.txt`, etc.) is read from committed bytes by others, and I
  make no claim about the round-82 counters, which are not on disk yet.
- The 12 rows in §2.5 are **reported, not repaired**: 9 are genuine count defects outside V2's named
  scope (the lesson and S260/S261), 1 is rule-dependent (S178, where 20 = 22 minus the two `…`
  separator tokens), and 2 are superseded-row history (S140 → S217, S221 → S222). Each value in that
  table is derived from the printed quote, with the duplicate-row or token-split evidence named,
  never guessed.
- The V6 paragraph is intentionally incomplete (`TALLY_PENDING`). It becomes evidence only when
  `.ufo/waves/round-82/w1-results.json` exists and §4.3's command has been run over it.
- V2's SOURCES half lands as two new rows (§2.4), not as cell edits, so `S260`/`S261` stay
  byte-unchanged; the frozen sentence's literal row-dominant reading is therefore an L1 ruling. The
  lesson half is in-place because the frozen V1 sentence ("the round-81 lesson's C2 paragraph states
  … as a dated correction") and the round-81 `R80-U1`/`R80-U6` precedent make the lesson the
  correction record.
- Network use was limited to the three `curl` fetches in §2.6; nothing was installed, and no
  `pacman` transaction was attempted (host-wide pause honoured).

---

## 7. Worktree state at hand-off (observed, read-only)

This seat wrote only its report, but other seats moved the shared worktree while it ran. Observed
with `git status --porcelain` and `git diff` at `2026-11-04T09:54:37Z` (read-only; I changed none of
these bytes):

```
 M SKILL.md                                             4 insertions  (C1 registry rows — not this seat)
 M corpus/README.md                                     (the round-81 spot-check index — C2 index leg)
 M corpus/knowledge/tb2-file-artifact-replay-classes.md 4 insertions  (the §3 trio, landed)
 M corpus/lessons/round-81.md                           2/2 lines     (the §2.3 count edits, landed)
 M corpus/SOURCES.md                                    2/2 lines     (Horn A — the §2.4b fallback, landed)
?? corpus/knowledge/tb2-replay-sweep-at-one-tip.md      (C3 knowledge entry, not this seat)
?? .ufo/waves/round-82/, corpus/evidence/round82/       (round scaffolding and receipts)
```

The three round-68 pypi evidence files recorded as modified in §5 item 7 are **clean** at this
reading; that item keeps both timestamps rather than the older one alone.

The `SOURCES.md` diff is byte-for-byte the §2.4b in-place patch:

```
-| S260 | … | corpus/evidence/round81/log-summary-date-ranges-probe.txt:1-17 (subject at 1, stamp 2-16, observations from 17); quote … (9 words, line 1); …
+| S260 | … | corpus/evidence/round81/log-summary-date-ranges-probe.txt:1-15 (subject at 1, stamp 2-14, OBSERVATIONS_BEGIN 15, observations from 16); quote … (7 words, line 1); …
-| S261 | … | …instruction.md:9 quote “…” (14 words); vulnerable-secret/instruction.md:1 quote “…” (17 words); …
+| S261 | … | …instruction.md:9 quote “…” (12 words); vulnerable-secret/instruction.md:1 quote “…” (13 words); …
```

So the worktree is currently on **Horn A** (literal predicate, rule-2 defect under Q34), while this
report's §2.4 delivers **Horn B** (append-only, S262/S263). Exactly one of the two may stand:

| state | frozen V2 sentence (literal) | QUALITY Q34 | admissible? |
|---|---|---|---|
| A — the two cells edited in place (worktree now) | true | **violated** (rule-2 defect, Q34's own anticipated case) | only with an L1 ruling that records the exception |
| B — cells reverted, S262/S263 appended, `u2` resolves each id through its supersede chain | true only under the chain reading | clean | preferred: L1 must adopt the chain reading in `u2` |
| A + B both | true | still violated, and the registry states the anchor twice | never |

Two integration gaps this hand-off measured:

1. **`R81-V2` is carried by no product artifact.** `grep -rl 'R81-V2' --include=*.md --include=*.py .`
   returns only the two seat reports under `.ufo/waves/round-82/w1/` (this report and
   `ConnectorR82.md`), never a lesson, registry row, knowledge entry or gate. Re-check with
   `grep -r` or `rg --hidden`: plain `rg -l 'R81-V2' .` prints nothing because `.ufo/` is a hidden
   directory, which makes the gap look different from what it is. C2 requires the row's `close` to be
   a tracked repair artifact carrying the id, so the §2.3 companion block must land in
   `corpus/lessons/round-81.md` §Corrections (`git diff --numstat` on that file is `2 2`, i.e. the
   count edits only, no correction block).
2. **The landed `recheck:` line is a trimmed variant of §3.2**: it drops the
   `HOST-PYTHON-MISMATCH`/`HOST-OPENSSL-MISMATCH` parenthetical and keeps the three real
   commands. That is still a valid recheck; `u3` must not require the parenthetical.
   The `source:` and `verified-at:` lines landed exactly as drafted.
