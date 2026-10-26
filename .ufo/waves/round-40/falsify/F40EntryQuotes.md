# F40EntryQuotes — quote, line-reference and case-letter audit of the C2 entry

Seat: critic (round 40, wave 2, falsify). Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, tip
`ec1005a2a28bc5cfdde7723374368ed4cc956eed` (read-only; nothing edited, no clone taken — this seat only reads and
re-fetches). Target: `corpus/knowledge/tb2-db-wal-recovery-grader.md` (the C2 admission), against
`corpus/evidence/round40/tb2-db-wal-recovery/` (8 captures + `SHA256SUMS`), `corpus/evidence/round40/db-wal-probe.txt`,
`plans/db_wal_probe.py`, and the wave-1 reports the entry cites. Receipts: `falsify/F40EntryQuotes/receipts.txt`
(sections R1-R6; every number below names the command and its output there).

Nothing was executed under `bwrap`: this seat runs no C1 counter, battery module or attack module, so the
host-safety battery wrapper has nothing to wrap. Two `curl` fetches and a handful of `read`/`grep`/`awk` pipelines.

## Axes

| axis | question | result |
|---|---|---|
| AX-Q quote fidelity | is every quoted string byte-exact at its cited line and 3-25 words? | **16/16 clean** (R1) |
| AX-L line-reference fidelity | does every `file:line` citation land on the content claimed? | 1 slip (`solve.sh:8`, D6); all others clean |
| AX-R receipt fidelity | do the case ids and per-test letters match `db-wal-probe.txt`? | **all match** (9 findings + map + falsifier) |
| AX-C claim-evidence coupling | does the cited evidence support the sentence as written? | 6 unsupported sentences (D1-D6) |

## 1. What holds, with the command that shows it

**1.1 Located-quotes table (§Located quotes): 16/16.** R1 takes each row's text between U+201C/U+201D, searches the
capture line by line, and checks the word count. Output: `RESULT rows=16 exact_at_cited_line=16 within_3_25_words=16`.
Every quote is a unique hit on exactly the cited line (7, 8, 8, 5, 8, 9, 9, 12, 11, 12 words in `test_outputs.py`;
13, 9, 9, 6, 13, 16 in `instruction.md`). No stray quote, no off-by-one.

**1.2 The captures are the pinned bytes.** Re-fetching the two S119/S120 URLs at `2fd12b88` gives
`88dc5c2a3abba75b… test_outputs.py` and `5a20375162921b89… instruction.md`, equal to `SHA256SUMS`; the table's
claim "identical to the pinned raw files at `2fd12b88`" holds, and the entry's falsifier (a) is not triggered.
`sha256sum -c SHA256SUMS` on all eight captures: all `OK`. `main.db-wal.encrypted` is 16512 B and starts `753d44c0`,
so §Prior art's "the XOR-0x42 file starts `753d44c0`" and finding 5's "16,512-byte encrypted WAL" hold; XOR 0x43
gives `367e0783` (finding 6) by the same bytes.

**1.3 §Prior art quotes.** Four quoted strings, each verified:
`build/R40ScoutPriorArt/tb21-pr3-body.md:13` (21 words) and the PR meta (`state=open merged=false created=2026-05-21`);
`tb-issue-2218-comment-6131410584.md:19` (9 words; comment dated 2026-10-12 per the scout report);
`harbor-issue-3607-body.md:26` (paraphrased, not quoted, and correctly so);
`wal.html` §4 (15 words, body offset 18026 sits between the §4 heading at 17592 and §5 at 18940);
`fileformat2.html` §4.1 ("0x377f0682 or 0x377f0683" under the "4.1. WAL File Format" heading).
The audit quote was re-fetched upstream at the cited commit, not trusted from the round-39 capture:
`https://raw.githubusercontent.com/JonathanGabor/terminal-bench-2-audit/35f11039/audit_results/20260120_125158/audit.txt:782`
`- Not all values are verified (e.g., values for records 3-11 aren't checked)` — exact, and the same file's
conclusion says "The test coverage is strong" with "Coverage rating: 4", so "rates the suite strong" holds.

**1.4 Line references.** Every `test_outputs.py` citation (`:9 :13 :17 :27 :33 :53 :58 :64 :80 :98`, ranges
`1-2 :14-18 :27-35 :43-44 :53-80 :88-89 :98-107`, and the bare `:14 :23 :30 :35 :40 :44 :49 :57-58 :58 :64-67
:70-80 :85 :89 :94`) lands on the claimed construct; `test.sh:18-22`, `:18-29`, `:25-29`, `task.toml:15 :22 :25
:29 :34`, `Dockerfile:3 :5-10 :12 :14-15` likewise. `grep -c 'main.db' test_outputs.py` = **0**, so "no function
in the file names `main.db` or `main.db-wal`" and falsifier (c) hold. Six `open()` calls plus one `os.path.exists`
at line 9, all on `/app/recovered.json` (R3).

**1.5 Case ids and letters.** Every case id in findings 1-9, in the requirement-map prose, in the falsifier list and
in the `Contestable tags` section exists in `db-wal-probe.txt`, and every letter string is byte-equal to the
receipt's `tests=` field (checked by hand against the 28 CASE lines; the map's lettered claims — `FFFFFFF`,
`PPPPPPP`, `PPPPFPF`, `PFFFFFF`, `PFPPFPF`, `PPPPFFP`, `PPPPFPP`, `PPFPPPP`, `PPFFFPP`, `PPPFFPP` — all match).
Tag counts recomputed by `awk` over the receipt: `fix-wal 23 (5 pass)`, `extract-all 15 (4)`, `eleven-records 10 (0)`,
`record-format 8 (2)`, `json-at-path 5 (0)`, `sorted-by-id 1 (0)`, 3 untagged — exactly the entry's numbers.
`cases=28 observed_pass=8 observed_fail=20 mismatches=0` and `regrade cases=28 differ=0` are verbatim in the receipt.
The two-witness arithmetic (5+18=23, 4+11=15, 2+5+... ) checks out.

## 2. Unsupported sentences (each a one-line text fix; none moves a finding, label or probe number)

### D1 — "six tags on four instruction lines" (AX-C) — `corpus/knowledge/tb2-db-wal-recovery-grader.md:125`
Quote: "The frozen table carries six tags on four instruction lines (`:7`, `:8`, `:9`, `:12`, `:13`)".
Counterexample: the entry's own list names **five** lines, and `plans/db_wal_probe.py:76-82` maps the six tags to
`7, 8, 9, 12, 13`. Evidence: R6 D1 prints the TAGS block; distinct lines = 5.
**Smallest correction:** "six tags on **five** instruction lines".

### D2 — `[]` is vacuously clean on four tests, not three (AX-C) — entry`:93-94` and `:239-240`
Quote (`:93-94`): "`[]` passes existence, structure and uniqueness (`PFPPFPF` in the receipt), so only length and
order-carrying tests do the work." Second locus (`:239-240`): "`[]` passes three tests vacuously".
Counterexample: `PFPPFPF` has P at positions 1, 3, 4, 6 in probe order (exists, valid, structure, sorted,
completeness, unique, wal) — existence, structure, **sorted**, uniqueness. `assert ids == sorted(ids)`
(`test_outputs.py:44`) passes on `[]` by the same vacuity, so "order-carrying tests do the work" is false of the
sorted test and the count is 4. Evidence: R2 `empty-list ... tests=PFPPFPF`.
**Smallest correction:** "passes existence, structure, sorted and uniqueness (`PFPPFPF`), so only the
length-carrying tests do the work"; at `:239-240`, "passes four tests vacuously".

### D3 — the five passing `fix-wal` violators are all literal exports (AX-C) — entry`:177`
Quote: "Under the frozen rule the label is `partly` either way (four of the five passing violators are literal
exports, not WAL states)."
Counterexample: all five passing violators are `mk.py` exports — probes `literals-never-open-db`,
`literals-names-1-2-wrong`, `truth-extra-field`, `truth-value-id3-wrong`, `truth-bool-value-id5` each have the
recipe `python3 /k/mk.py <variant>` (`plans/db_wal_probe.py:193,196,208,224,226`; R6 D3), and `mk.py` writes JSON
from `TRUTH` with no `sqlite3`. The entry's own line-7 paragraph lists all five as passing violators.
**Smallest correction:** "**all five** passing violators are literal exports, not WAL states".

### D4 — completeness fails on string ids by type, not by lexicographic order (AX-C) — entry`:232-233`
Quote: "`"1"` fails structure (`:33`), and also sorted and completeness because the lexicographic order of
`"1"…"11"` is not `1..11`".
Counterexample: `test_outputs.py:57-58` is `expected_ids = list(range(1, 12))` then `assert ids == expected_ids`;
a list of strings cannot equal a list of ints at any order, so completeness fails independently of ordering.
Only the sorted failure (`:44`) is lexicographic. Evidence: R6 D4.
**Smallest correction:** "…and also `sorted` (lexicographic order of `"1"…"11"`) and `completeness` (string ids
are not the int sequence `1..11`)".

### D5 — the receipt does not show `FileNotFoundError` "on all seven" (AX-R/AX-C) — entry`:197-198`
Quote: "The negative control `empty-app` is the same letters from an empty `/app`, and the receipt shows each
function's exception class (`FileNotFoundError` on all seven)."
Counterexample: the `empty-app` line carries six `error=FileNotFoundError` fields, not seven (R6 D5); the seventh
function, `test_recovered_json_exists`, fails its own `assert os.path.exists(...)` (`test_outputs.py:9`), and the
probe's harness prints a class only from `except Exception` — `except AssertionError` prints a bare `F`
(`plans/db_wal_probe.py:250-252`). So the receipt shows six classes and no class for the existence test, whose
exception is an `AssertionError`.
**Smallest correction:** "(`FileNotFoundError` on six; the existence assert is a bare `AssertionError`)".

### D6 — `solve.sh:8` is the comment, not the read-only open (AX-L) — entry`:220-221`
Quote: "The destructive read is published in the oracle itself — `solve.sh:8` opens the database read-only "to
avoid WAL interaction"".
Counterexample: `solve.sh:8` is `# Print current database content (read-only to avoid WAL interaction)`; the open
is `solve.sh:10`: `sqlite3 "file:/app/main.db?mode=ro" "SELECT id, name, value FROM items ORDER BY id;"` (R6 D6).
As cited, line 8 opens nothing, and the open it points at is the *avoidance* of the destructive read, not the
destructive read.
**Smallest correction:** "the hazard is recorded in the oracle's own comment — `solve.sh:8-10` queries
`mode=ro` \"to avoid WAL interaction\"".

## 3. Precision notes (true in substance; listed so the author can tighten, not counted as unsupported)

- **`json-at-path` cites 4 of its 5 cases** (entry`:135`, `:158-159`). The receipt tags `untouched` too
  (`FFFFFFF`); the `enforced` label survives (all 5 fail), but the sentence presents an incomplete basis for a
  label whose stated rule is "computed over **all** violating cases". One word fixes it: add `untouched`.
- **The line-12 paragraph lists 5 of the 6 failing `record-format` cases** (entry`:162-165`), omitting
  `truth-value-float-id1` (`PPFPPPP`, tagged `fix-wal,record-format`). The tag is cited in finding 7, so no claim
  is wrong; the paragraph reads as if exhaustive (2 pass + 5 fail = 7 of 8).
- **"all of them for export-content reasons" (entry`:144`)** holds for 16 of the 18 failing `fix-wal` cases; the
  two remaining fail on an export that is absent (`untouched`) or at the wrong path (`truth-wrong-path`), both
  `FileNotFoundError`. "export reasons (content, absence or path)" is exact.
- **"every one of them opens only `/app/recovered.json` (:9, …)" (entry`:11-12`)** — `:9` is `os.path.exists`, not
  an open; the six opens are `:14 :23 :40 :49 :85 :94`. The §Regrade restatement (six lines) is the correct form.

## 4. Consequence for the wave

- The quotes are clean: no located quote is misquoted, mislocated or out of the 3-25-word band; §Prior art's four
  quotes verify, including one re-fetched upstream at the cited commit.
- The receipt side is clean: every case id, letter string and tag count reproduces from
  `corpus/evidence/round40/db-wal-probe.txt`; nothing in the findings is invented or transposed.
- The damage is prose arithmetic and one line attribution (D1-D6): six sentences whose cited evidence does not
  support them as written, each repaired by editing that sentence. None of them weakens the entry's headline, its
  requirement map, its nine findings, or the `checks=7 defects=0` predicate — the corrections are consistent with
  the measured table and can be applied without re-running the probe.
- Untested here: the entry's falsifier (b) (a fresh `plans/db_wal_probe.py --lane .` run) and (d) (re-grading the
  two named states). Both are executor work under the battery wrapper, not critic work; I did not run them.

Hygiene: no lane write, no `git` command, no `systemd-run`/cron/at, no pacman, no install, no process left running.
Temp files created by the fetch/compare steps lived in `/dev/shm` and were deleted in the same command
(`ls /dev/shm | wc -l` = 0); no scratch clone was needed because nothing was built.

VERDICT: entry-quotes-16/16-unsupported-6
