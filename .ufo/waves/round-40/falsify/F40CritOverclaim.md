# F40CritOverclaim — overclaim hunt across the landed C2 text (round 40, wave 2 FALSIFY)

Seat: critic (leaf, no subagents). Lane read-only; nothing edited, admitted, integrated or shipped. No clone was
needed (every check is a read of committed bytes plus read-only `python3` over the receipt and the frozen dry
table); no process left running; nothing installed.

Tip under review: `ec1005a2a28bc5cfdde7723374368ed4cc956eed`. The landing measurement records
`TIP ec17216844585d0fecde9f1d4c4be0b78a3bf76f` (`.ufo/waves/round-40/integrate/measure-final.txt:1`), and every C2
byte under review is identical at that commit, at `ec1005a` and at HEAD `c9c793c`:

```
$ git diff --stat ec17216844585d0fecde9f1d4c4be0b78a3bf76f ec1005a2a28bc5cfdde7723374368ed4cc956eed -- \
    SKILL.md PROVINCE.md corpus/README.md corpus/SOURCES.md corpus/knowledge/tb2-db-wal-recovery-grader.md \
    plans/db_wal_probe.py plans/round40_c2_verify.py corpus/evidence/round40
(no output; rc=0)
```

so the frozen predicate `checks=7 defects=0` / `PREDICATE C2 pass` (`measure-final.txt:71-72`) does cover the text
judged here. Method: read the entry, the README index/coverage/frontier/evidence lines, the PROVINCE paragraph, the
SKILL section + registry rows, `corpus/SOURCES.md` S119-S121, the frozen claims, the receipt, the frozen dry table,
the captured grader/`test.sh`/`solve.sh`/`Dockerfile`/`task.toml`, `plans/db_wal_probe.py`, `plans/round40_c2_verify.py`,
and wave-1 `R40CritProbe` (D1-D8), `R40PkgProse`, `R40PkgEntry`, `R40CritSkipC2`, `R40CritClaims`, `R40RegradeSweep`,
`R40ScoutPriorArt`. Every number below carries its command; commands and raw output are in
`F40CritOverclaim/overclaim-receipts.txt`.

## 1. What holds (checked, not assumed) — the brief's five named risk areas

| brief risk | landed text | verdict |
|---|---|---|
| regrade wording (D1) | entry:28 "`regrade cases=28 differ=0`; a determinism read of the probe, not re-run stability"; entry §Regrade:245-253 "nearly tautological for this grader, and **not** re-run stability"; PROVINCE:425 "a same-process second call … not re-run stability"; SKILL:969 "a determinism read of the probe, not re-run stability"; README:498 "a same-process second call" | **holds**; the frozen claims' "proposal 3's stability rider" (`plans/round-40-claims.md:79`) is corrected in the entry, the lesson (`corpus/lessons/round-40.md:31`) and the seat report; the README coverage bullet quotes the number bare but never calls it stability |
| `fix-wal` label (D2) | entry:147 "the label is not evidence that the repair is checked at all: zero of the seven tests read `/app/main.db-wal`"; entry:148-158 says the headline is the measured statement | **holds in the entry**, not in the SKILL (F13) |
| wrong-key confound (D5) | entry:223-228 "the case's read-write extraction then discards the log … the case is therefore confounded"; SKILL row "which also discards the log; entry finding 6" | **holds**; the README index row still states the outcome as the key's (F14) |
| 0-byte WAL (D6) | entry:218-220 "leaves a 0-byte `main.db-wal`, and its decryptor XORs 0 bytes … the end state holds a 0-byte WAL, not no WAL" | **holds**; SKILL:994 says "nothing left to decrypt" but does not claim no WAL remains |
| "never opens" vs "hand-typed with wrong values" (D4) | entry:28-31 "The headline case is `literals-never-open-db`: hand-typed JSON … zeroes elsewhere, the database never opened — passes 7 of 7"; entry:202 "`literals-never-open-db` is not a correct export: nine of its eleven values are `0`" | **holds** — no landed line presents a hand-typed export as a correct one |

Also holding: D3 (no passing repair route ends with a repaired WAL: entry:148-152 names all three routes as 0-byte
plus checkpointed), D7 (the tag rule is stated as content-based for `extract-all`, entry:183-187), D8 (uneven tag
policy named, entry:187), the quote table (`measure-final.txt:56-57` `gate: P3 ok rows=16 … gate: P4 ok checked=16 bad=0`),
the capture digests (`sha256sum -c …/SHA256SUMS` → all eight `OK`), the receipt's own letters (parsed below), and the
prior-art citations S121/#2218/#3607 against their captures (PR `state=open merged=false created=2026-05-21`;
comment `2026-10-12`; issue `2026-10-10`).

Receipt facts recomputed from `corpus/evidence/round40/db-wal-probe.txt`:

```
plain-read-then-solve PPPPFPF passes=5 ['exists', 'valid', 'structure', 'sorted', 'unique']
empty-list PFPPFPF passes=4 ['exists', 'structure', 'sorted', 'unique']
json-at-path cases=5 failing=['empty-app', 'untouched', 'decrypt-in-place-no-json', 'truth-trailing-garbage', 'truth-wrong-path']
record-format cases=8 failing=['truth-value-float-id1', 'truth-wrapped-object', 'truth-ids-as-strings', 'truth-ids-as-floats', 'truth-name-null-id1', 'truth-value-string-id4']
tag_lines=['instruction.md:7', 'instruction.md:8', 'instruction.md:9', 'instruction.md:12', 'instruction.md:13', 'instruction.md:13'] distinct=5
```

## 2. Findings

Severity: **H** = a receipt number in the landed prose is wrong; **M** = the claim is stronger than the receipt or
cites the wrong witness; **L** = exactness defect that cannot move a label. Axis for every finding:
**calibration** (no coverage move — the 28-case sample is unchanged; no operability move — no tool changes).

---

**F1 (H, overclaim + false number). `corpus/knowledge/tb2-db-wal-recovery-grader.md:32-33`.**
Claim: “while the task's own `solve.sh` after one careless read-write `sqlite3` open scores 4 of 7
(`plain-read-then-solve`)”.
Counterexample: the receipt line for that case is `PPPPFPF`, five passes of seven.
Evidence: `python3` parse above → `plain-read-then-solve PPPPFPF passes=5`; the entry's own finding 5:215-217 says
“the task's own oracle then fails two **tests**”; `corpus/README.md:73` says “then fails 2 tests”. Three landed
statements, two of them wrong. This is also exactly the class wave-1 `R40CritSkipC2` §F showed the counter cannot
see: a false summary beside a green predicate (`measure-final.txt:71-72`).
Correction: “scores 5 of 7 (fails completeness and the WAL test)”. It matters beyond the numeral: “4 of 7” makes
the destructive read look worse than the receipt and simultaneously makes the oracle look faulty on its own — the
oracle alone is `oracle-solve-sh` 7/7 (`receipt:8`).

**F2 (M, overclaim). `PROVINCE.md:427-428`.**
Claim: “the instruction's repair step ("Fix the WAL file so SQLite can read it", `instruction.md:7`) is reachable
only through that export”.
Counterexample: two receipt cases in opposite directions show the export is not a channel for the repair —
`literals-never-open-db` (never repairs, never opens the database) passes 7/7 (`receipt:15`), and
`decrypt-in-place-no-json` (the only genuinely repaired WAL in the frozen table) fails 7/7 (`receipt:14`).
Evidence: the receipt lines; the entry itself:147 “the label is not evidence that the repair is checked at all”;
`corpus/README.md:267` uses the correct stronger wording “never read”.
Correction: “is graded only through that export, and no export content evidences it”.

**F3 (M, overclaim of count). `corpus/knowledge/tb2-db-wal-recovery-grader.md:52`.**
Claim: “the probe executes it once, as the `oracle-solve-sh` case's recipe inside the sandbox”.
Counterexample: `plans/db_wal_probe.py:172` and `:177` both run `bash /cap/solve.sh` — `oracle-solve-sh` and
`plain-read-then-solve`.
Evidence: `grep -n 'bash /cap/solve.sh' plans/db_wal_probe.py` → two hits (172, 177); `grep -c` → `2`. The receipt
shows the oracle executed twice with different results (`receipt:8` `PPPPPPP`, `receipt:10` `PPPPFPF`).
This is not pedantry: the second execution is the one finding 5 rests on, and “once” hides it, making the
destructive-read result look like a story about an external agent rather than the oracle running on a wrecked
`/app`. Same imprecision, weaker claim: `corpus/README.md:339` and entry:339 “runs as one case's recipe”.
Correction: “executes in two cases — as the oracle (`oracle-solve-sh`) and after a destructive read
(`plain-read-then-solve`)”.

**F4 (M, overclaim of scope). `corpus/README.md:73`.**
Claim: “one plain read-write `sqlite3` open destroys the encrypted log so the task's own oracle then fails 2 tests”.
Counterexample: the only build measured is the host's; the entry:266-269 says “The image's own sqlite version was
not fetched — no image pull … every version-specific behaviour of that build is untested here: in particular
whether its sqlite deletes an undecryptable WAL on a read-write open with the same trigger as 3.54.0”
(`task.toml:29` names `alexgshaw/db-wal-recovery:20251031`, never pulled). The index row states a property of the
task's environment from a stand-in; the entry and PROVINCE:445 carry the limit, the index row does not (the
frontier sub-bullet at `corpus/README.md:334` only reports the measured states' test letters and makes no
destruction claim, so it is not part of this finding).
Correction: append the scope — “destroys the encrypted log on the probe's host sqlite 3.54.0 (image untested)” — or
move the sentence behind the entry link.

**F5 (M, wrong witness). `SKILL.md:1015`.**
Claim: “`json-at-path` on five that include the empty-list and non-JSON states (`receipt:28,26`)”.
Counterexample: `empty-list` (`receipt:28`) does not carry `json-at-path`; its tags are
`fix-wal,extract-all,eleven-records`, and it passes test 1 (`PFPPFPF`). The five tagged cases are `receipt:6,7,14,26,27`
— `empty-app`, `untouched`, `decrypt-in-place-no-json`, `truth-trailing-garbage`, `truth-wrong-path`.
Evidence: the tag dump above (`json-at-path cases=5 failing=[…]`) and `CASE empty-list … violates=fix-wal,extract-all,eleven-records`.
The label itself is unaffected (all five tagged cases fail); the sentence's witness list overclaims by adding a
case that is not one.
Correction: replace `receipt:28` with `receipt:6,7,14` (or write “the empty-`/app` baseline”, as the same paragraph
does one sentence earlier).

**F6 (L, mechanism overstatement). `corpus/knowledge/tb2-db-wal-recovery-grader.md:11-12`, `corpus/README.md:73`,
`corpus/SOURCES.md:134`.**
Claim: “every one of them opens only `/app/recovered.json` (`:9`, `:14`, `:23`, `:40`, `:49`, `:85`, `:94`)”.
Counterexample: `test_recovered_json_exists` never opens the file — `grep -n 'exists("/app/recovered.json")'` →
`9:    assert os.path.exists("/app/recovered.json") …`; it is six opens plus one stat.
The substantive claim (no other path is read) holds; the index row and S119 repeat “read only the exported JSON”
including “existence”, which is a stat.
Correction: “every one of them touches only `/app/recovered.json` (six open it; test 1 only checks existence, `:9`)”.

**F7 (L, undercount contradicting its own citation). `corpus/knowledge/tb2-db-wal-recovery-grader.md:93` and `:239`.**
Claim: “**The empty and near-empty states are vacuously clean on three tests.** `[]` passes existence, structure and
uniqueness (`PFPPFPF`)”; and at :239 “`[]` passes three tests vacuously”.
Counterexample: `PFPPFPF` has four `P`s. Parsed: `empty-list PFPPFPF passes=4 ['exists', 'structure', 'sorted', 'unique']`.
The named three omit `sorted`, and the sentence's next clause (“only length and order-carrying tests do the work”)
is contradicted by the order test passing.
Correction: “`[]` passes four tests — existence, structure, sortedness and uniqueness (`PFPPFPF`) — so only the three
length-carrying tests do the work”.

**F8 (L, miscount). `corpus/knowledge/tb2-db-wal-recovery-grader.md:125`.**
Claim: “The frozen table carries six tags on four instruction lines (`:7`, `:8`, `:9`, `:12`, `:13`)”.
Counterexample: the five locations listed carry the six tags; the dry table's first six lines are the TAG lines.
Evidence: `tag_lines=[…] distinct=5`. The tag counts in the same paragraph (23/15/10/8/5/1) are correct.
Correction: “five instruction lines”.

**F9 (L, incomplete witness list). `corpus/knowledge/tb2-db-wal-recovery-grader.md:158-160`.**
Claim: “`enforced`: `empty-app`, `decrypt-in-place-no-json`, `truth-trailing-garbage` and `truth-wrong-path` all fail”.
Counterexample: `json-at-path` has five witnesses; `untouched` (`receipt:7`, `FFFFFFF`) is omitted.
Evidence: tag dump above. The label survives (all five fail) and V7 re-derives it from the receipt, so no label moves.
Correction: add `untouched`.

**F10 (L, incomplete witness list). `corpus/knowledge/tb2-db-wal-recovery-grader.md:162-166`.**
Claim: “while `truth-wrapped-object` (`PFFFFFF`), `truth-ids-as-strings` (`PPFFFPP`), `truth-ids-as-floats`
(`PPFPPPP`), `truth-value-string-id4` and `truth-name-null-id1` fail” — five of the six failing `record-format` cases;
`truth-value-float-id1` (`receipt:18`, `PPFPPPP`) is omitted.
Evidence: tag dump (`record-format … failing=['truth-value-float-id1', …]`). Label unaffected (the eighth case also fails).
Correction: add `truth-value-float-id1` (`PPFPPPP`).

**F11 (L, wrong line for an attributed action). `corpus/knowledge/tb2-db-wal-recovery-grader.md:221`.**
Claim: “The destructive read is published in the oracle itself — `solve.sh:8` opens the database read-only "to avoid
WAL interaction"”.
Counterexample: `solve.sh:8` is the comment; the read-only open is `solve.sh:10`.
Evidence: `sed -n '8p;10p' solve.sh` → line 8 `# Print current database content (read-only to avoid WAL interaction)`,
line 10 `sqlite3 "file:/app/main.db?mode=ro" …`. The entry attributes an open to a comment line; SKILL:994 correctly
cites `solve.sh:8-10`.
Correction: “`solve.sh:8-10` prints the warning and opens the database read-only”.

**F12 (L, uniformity overclaim). `corpus/knowledge/tb2-db-wal-recovery-grader.md:144`.**
Claim: “eighteen are observed `fail`, all of them for export-content reasons”.
Counterexample: `untouched` (`receipt:7`) is tagged `fix-wal` and fails with `FileNotFoundError` on all seven — there
is no export to have content.
Evidence: `CASE untouched … tests=FFFFFFF … test_recovered_json_is_valid:error=FileNotFoundError,…`. Seventeen fail
on export content, one on export absence. The sentence's point (none fails because of the WAL state) is correct.
Correction: “seventeen for export-content reasons and `untouched` for a missing export”.

**F13 (L, overclaim by omission; wave-1 D2 residue). `SKILL.md:1005-1015`.**
Claim: “`fix-wal` (`instruction.md:7`) `partly` — 23 cases, 5 observed pass” — followed by a caveat for `enforced`
only (“`enforced` here is a property of the frozen case set only …”).
Counterexample: the entry:147-148 carries the D2 correction (“the label is not evidence that the repair is checked at
all”), and the SKILL's own decision table (:992) says the WAL has no assertion behind it. A SKILL-only reader can take
`partly` as partial enforcement — the reading D2 forbids.
Correction: add one clause after the labels: “`partly` on `fix-wal` is a co-tagging artefact — no test reads the WAL”.

**F14 (L, confound dropped in the compressed row). `corpus/README.md:73`.**
Claim: “a wrong XOR key leaves the five base rows”.
Counterexample: the case is a wrong key **plus** a read-write extraction that discards the log; the entry finding 6
(:223-228) says “confounded” and the coverage bullet (`:267`) carries the full mechanism. The index row reads as a
claim about the key alone, and wave-1 D5 measured that a read-only wrong-key extraction is the only shape that
isolates the key.
Correction: “a wrong XOR key, then a read-write extraction, leaves the five base rows”.

## 3. Candidates tested and not sustained

- **`regrade` quoted bare (`corpus/README.md:267`).** The number appears without the same-process qualifier, but the
  bullet never calls it stability; the entry, PROVINCE, SKILL and evidence line all carry the qualifier. D1 is not
  overclaimed.
- **The frozen claims' “proposal 3's stability rider” (`plans/round-40-claims.md:79`).** The claims are frozen and
  uncorrected, but the landed entry §Regrade and the lesson (:31) name the correction explicitly, and the stability
  question is answered by `R40RegradeSweep` (15/15). No overclaim survives in the landed text.
- **“sixth grader class” (R40CritClaims §3).** The claims' ordinal conflation was not repeated: the entry says “one
  edge class new to the lane's **executed** grader sample”, the README says “sixth Terminal-Bench 2.0 task grader” /
  “sixth instance of the same ground”. Correction honoured.
- **`literals-never-open-db` described as evidence of a repair.** Not claimed anywhere; the entry states its nine
  zero values.
- **The `fix-wal` `partly` label as “partial enforcement” inside the entry.** Not claimed; :147-148 is explicit.
- **`corpus/README.md:267` grouping `truth-wrong-path` under “bounded by length, id multiset and the 22 pinned
  cells”.** Loose grouping, not a false statement (the case does fail, and the sentence's answers-surface list
  that follows is correct); I do not sustain it as an overclaim.
- **`measure-final.txt` records `TIP ec17216`, not `ec1005a`.** The C2 bytes are identical at both (diff above), so
  the SKILL row's “measured green at the landing tip” holds for the text judged; `ec1005a` adds the lesson, the
  SCORECARD/LOG and the wave-1 reports only.

## 4. Limits of this review

I read and recomputed; I did not re-run the probe or the C2 counter (the landing measurement already records
`gate: P10 ok probe_rerun=byte-equal bytes=8257` and `checks=7 defects=0`, and a re-run cannot change a prose
numeral). Host sqlite3 3.54.0 / python3 stand in for the image, as the entry says. No external fetch was made except
`https://www.sqlite.org/wal.html`, which confirms the entry's §4 quote verbatim (“Usually, the WAL file is deleted
automatically when the last connection to the database closes”) and the encrypted header XOR
(`753d44c0` → `0x37 0x7f 0x06 0x82`). These findings are text defects; they do not move the frozen C2 predicate or
any counter check, which is why they landed green, and each correction is compatible with the freeze (receipt, dry
table, probe and claims untouched).

VERDICT: overclaims-14
