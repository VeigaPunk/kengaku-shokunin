# F37CritC1Axis — is C1 a calibration claim? Per-mutant advertising audit

Seat: critic, round-37 wave 2. Target: C1 as frozen in `plans/round-37-claims.md` §C1 and as landed at tip
`357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5` (`plans/pkg_gate.py` sha256 `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`).
Question attacked: the claim calls the freeze count `survived=50` a *calibration* mismatch between three
self-assessment texts and observed tests. Every one of the 55 frozen mutants is checked against those three
texts; a mutant whose label has no advertising sentence cannot be a calibration mismatch.

**Answer: the axis is calibration, over-counted by 6.** 49 of the 55 mutants map to an advertising sentence
(24 at defect-class level, 25 at the SCORECARD component level); 6 map to nothing — M34–M39, the whole P8
README/index group and P9's non-git-root branch. The freeze mismatch count over advertised clauses is
**50 − 6 = 44**, not 50. The 5 classes demonstrated at freeze (M01, M05, M40, M47, M54) are all advertised,
so the demonstrated subset is 100% calibration-eligible; the over-count is entirely in the survivor column.

## 1. The three texts and what each advertises

| Text | Advertised surface | Citation (quote ≤25 words) |
|---|---|---|
| gate docstring | four named defect classes | `plans/pkg_gate.py:12-13` "An unparsed row, a manifest line that fails its own digest, a quote not verbatim on its cited line, and a receipt a fresh run does not reproduce are defects." |
| gate docstring | spec-driven parameters, hence checks | `plans/pkg_gate.py:9-10` "paths, digests, row ids, tier, status, quote bounds, labels and directional tokens come from --spec" |
| gate docstring | setup is not a defect | `plans/pkg_gate.py:7` "exit 0 = accept, 1 = reject, 2 = usage/setup" |
| QUALITY Q24 | five enumerated junk classes | `corpus/QUALITY.md:305-306` "an entry of eight one-word quotes, `junk` teaches cells, a stub probe that prints the receipt, and an untracked leftover file; … labelled-but-false D4/D5 lines" |
| QUALITY Q24 | property-level standard (no branch enumeration) | `corpus/QUALITY.md:300-301` "the genuine package must be accepted, every single-property junk mutant must be rejected" |
| SCORECARD capability row | six package components | `SCORECARD.md:564` "Accept or reject an admitted-entry package (entry, capture manifest, SOURCES rows, receipt, frozen instruments, clean tree)" |
| SCORECARD capability row | named properties | `SCORECARD.md:564` "every quote row must parse and be distinct and verbatim on its cited capture line, teaches cells carry >=8 distinct words, a stub probe dies on its digest pin" |
| SCORECARD capability row | options | `SCORECARD.md:564` "`--rerun` byte-compares the receipt, `--require-clean-tree` refuses any untracked file" |

Vocabulary probe (`grep -ic` over the three texts, command below): `README` 0/0/0, `index` 0/0/0, `bullet`
0/0/0, `knowledge files` 0/0/0, `git worktree` 0/0/0, `Negative space` 0/0/0, `verified-at` 0/0/0, `recheck`
0/0/0, `used-by` 0/0/0, `cells` 0/1/1. The words that carry the P8 checks and the P9 precondition appear in
none of the three texts.

## 2. Per-mutant map (all 55)

Tier **C** = defect class named (explicit sentence); **K** = only the SCORECARD component noun covers it;
**N** = no advertising sentence. Tier assignment is generous: any noun the reader can point at earns **K**.

| Mutant | Clause | Label | Advertising sentence | Tier |
|---|---|---|---|---|
| M01 | P1 | frozen instrument digest mismatch | `SCORECARD.md:564` "a stub probe dies on its digest pin"; `QUALITY.md:305` | C |
| M02 | P2 | receipt unreadable | `SCORECARD.md:564` component "receipt" | K |
| M03 | P2 | receipt digest differs from the pin | `SCORECARD.md:564` "against a spec of pinned digests" | K |
| M04 | P3 | no Located quotes section | `SCORECARD.md:564` "every quote row must parse" (no row ⇒ nothing parses) | K |
| M05 | P3 | an unparsed quote row | `plans/pkg_gate.py:12` "An unparsed row"; `SCORECARD.md:564` "must parse" | C |
| M06 | P3 | fewer distinct quotes than min_quotes | `SCORECARD.md:564` "must parse and be distinct" | C |
| M07 | P3 | fewer distinct located lines | `SCORECARD.md:564` "distinct … on its cited capture line" | C |
| M08 | P3 | a quote outside the word range | `plans/pkg_gate.py:9` "quote bounds"; `QUALITY.md:305` "eight one-word quotes" | C |
| M09 | P4 | no parsed quote | `SCORECARD.md:564` "every quote row must parse" | C |
| M10 | P4 | quote cites an unreadable capture | `SCORECARD.md:564` "verbatim on its cited capture line" (cannot be checked) | K |
| M11 | P4 | quote line range outside the capture | `SCORECARD.md:564` "on its cited capture line" | C |
| M12 | P4 | quote not verbatim on its cited line | `plans/pkg_gate.py:12-13`; `SCORECARD.md:564` | C |
| M13 | P5 | capture manifest absent | `SCORECARD.md:564` component "capture manifest" | K |
| M14 | P5 | unparsed manifest line | `SCORECARD.md:564` component "capture manifest" (docstring `:12` names only digest failure) | K |
| M15 | P5 | manifest digest ≠ capture bytes | `plans/pkg_gate.py:12` "a manifest line that fails its own digest" | C |
| M16 | P5 | row capture not pinned in the manifest | `SCORECARD.md:564` "against a spec of pinned digests" | K |
| M17 | P5 | manifest digest differs from the spec pin | `SCORECARD.md:564` "pinned digests" | C |
| M18 | P5 | quoted capture not pinned | `SCORECARD.md:564` component "capture manifest" | K |
| M19 | P5 | capture file not covered by the manifest | `SCORECARD.md:564` component "capture manifest" | K |
| M20 | P6 | registry row missing or duplicated | `SCORECARD.md:564` component "SOURCES rows" | K |
| M21 | P6 | registry row without 11 cells | `SCORECARD.md:564` component "SOURCES rows" | K |
| M22 | P6 | row url not the pinned raw path | `SCORECARD.md:564` component "SOURCES rows" | K |
| M23 | P6 | row tier wrong | `plans/pkg_gate.py:9` "tier … come from --spec" | C |
| M24 | P6 | row status wrong | `plans/pkg_gate.py:9` "status … come from --spec" | C |
| M25 | P6 | row used-by is not the entry | `SCORECARD.md:564` component "SOURCES rows" | K |
| M26 | P6 | teaches cell under min_teaches_words | `SCORECARD.md:564` "teaches cells carry >=8 distinct words"; `QUALITY.md:305` | C |
| M27 | P6 | teaches cells not pairwise distinct | `SCORECARD.md:564` "distinct words" | C |
| M28 | P7 | entry unreadable | `SCORECARD.md:564` component "entry" | K |
| M29 | P7 | source line absent / not pinned url | `SCORECARD.md:564` component "entry" | K |
| M30 | P7 | verified-at absent / not the frozen date | `SCORECARD.md:564` component "entry" only | K |
| M31 | P7 | recheck line absent | `SCORECARD.md:564` component "entry" only | K |
| M32 | P7 | no Negative space section | `SCORECARD.md:564` component "entry" only | K |
| M33 | P7 | Negative space carries no falsifier | `SCORECARD.md:564` component "entry" only | K |
| **M34** | P8 | README unreadable | **none** — "README" absent from all three texts | **N** |
| **M35** | P8 | index rows not exactly one | **none** — "index" absent from all three texts | **N** |
| **M36** | P8 | index row does not cite every registry row | **none** | **N** |
| **M37** | P8 | no coverage bullet naming entry and receipt | **none** — "bullet" absent | **N** |
| **M38** | P8 | knowledge files differ from index rows | **none** | **N** |
| **M39** | P9 | root is not a git worktree | **none** — `SCORECARD.md:564` advertises only "refuses any untracked file"; `plans/pkg_gate.py:7` assigns setup to exit 2 | **N** |
| M40 | P9 | untracked file present | `SCORECARD.md:564` "refuses any untracked file"; `QUALITY.md:305-306` | C |
| M41 | P10 | receipt unreadable at re-run | `SCORECARD.md:564` component "receipt" | K |
| M42 | P10 | fresh probe exits nonzero | `plans/pkg_gate.py:13` "a receipt a fresh run does not reproduce" | C |
| M43 | P10 | fresh probe output not byte-equal | `SCORECARD.md:564` "`--rerun` byte-compares the receipt" | C |
| M44 | D4 | d4 file unreadable | `SCORECARD.md:564` "the labelled D4/D5 correction lines" (file absent, not a label defect) | K |
| M45 | D4 | d4 file is not exactly one line | `SCORECARD.md:564` "correction lines" | K |
| M46 | D4 | d4 line does not carry the label | `plans/pkg_gate.py:9` "labels"; `SCORECARD.md:564` "labelled" | C |
| M47 | D4 | d4 directional pattern absent | `plans/pkg_gate.py:9` "directional tokens"; `QUALITY.md:306` | C |
| M48 | D5 | d5 file unreadable | `SCORECARD.md:564` "labelled D4/D5 correction lines" | K |
| M49 | D5 | d5 file is not exactly one line | `SCORECARD.md:564` "correction lines" | K |
| M50 | D5 | d5 line does not carry the label | `plans/pkg_gate.py:9` "labels" | C |
| M51 | D5 | d5 required token missing | `plans/pkg_gate.py:9` "directional tokens" | C |
| M52 | D5 | d5 forbidden token present | `plans/pkg_gate.py:9` "directional tokens" | C |
| M53 | D5 | d5 capture unreadable | `SCORECARD.md:564` "D4/D5 correction lines" (capture absent) | K |
| M54 | D5 | d5 capture digest not in the manifest | `SCORECARD.md:564` "pinned digests" | C |
| M55 | D5 | d5 quote absent from the capture | `SCORECARD.md:564` "verbatim on its cited capture line" | C |

Tier totals: **C 24, K 25, N 6** (24+25+6 = 55). Survivors at freeze = 50 = C 19 + K 25 + **N 6**.

## 3. The counterexample

M34–M39 are killed (so they count toward `killed=55` and toward the freeze `survived=50`), yet no sentence in
any of the three self-assessment texts names the property they silence. P8's README index, coverage bullet and
knowledge-file/index consistency checks are nowhere advertised — not in the docstring, not in Q24, and not in
the SCORECARD parenthetical, whose six components stop at "clean tree". M39 is worse than unadvertised: it is a
**setup** condition (the root is not a git repository), which `plans/pkg_gate.py:7` itself assigns to exit 2, and
which the freeze exclusion list (`plans/round-37-claims.md` §C1 "Excluded branches") does not name even though a
battery *can* vary it — `p910-not-a-git-repo` does (`plans/battery37/p910.py:100`).

Independent confirmation on my own clone of the tip (scratch, not the lane):

```
GATE plans/pkg_gate.py sha256=frozen
BATTERY fixtures=64 wrong=0 renamed_disagree=0
MUTANT M34 P8 killed by=p8-readme-deleted -- README unreadable
MUTANT M35 P8 killed by=p8-index-row-duplicated -- index rows for the entry not exactly one
MUTANT M36 P8 killed by=p8-index-row-missing-sid -- index row does not cite every registry row
MUTANT M37 P8 killed by=p8-coverage-bullet-removed -- no coverage bullet naming entry and receipt
MUTANT M38 P8 killed by=p7-m28-entry-deleted -- knowledge files differ from index rows
MUTANT M39 P9 killed by=p910-not-a-git-repo -- root is not a git worktree
MUTANTS total=6 killed=6 survived=0 invalid=0 null_detected=0
```
(`python3 plans/round37_c1_verify.py --lane . --only M34,M35,M36,M37,M38,M39`, receipt
`falsify/F37CritC1Axis/seat-run-m34-m39.txt`.) The predicate requires these kills:
`plans/round37_c1_verify.py:387-388` sets `good = … killed == TOTAL`, so the 6 are load-bearing for
`PREDICATE C1 pass` while contributing nothing to the calibration count.

## 4. Axis test against the addendum

Addendum test: a calibration claim counts mismatches between *self-assessment* and *observed repo state*. Applied:

- Self-assessment exists for 49/55 mutants (24 named classes + 25 component-level). A component noun is a real
  self-assessment sentence: `SCORECARD.md:564` says the gate accepts or rejects a package *on* entry, capture
  manifest, SOURCES rows, receipt, frozen instruments, clean tree. A gate advertised to judge "SOURCES rows" is
  advertised to reject a wrong tier/status/url row.
- Observed state is the battery: `BATTERY fixtures=64 wrong=0 renamed_disagree=0` at the tip.
- Mismatch count over advertised mutants at freeze: 44 survivors (19 C + 25 K). At the tip: 0. That is a
  genuine calibration closure, 44 → 0.
- The 6 N mutants are branch coverage with no advertisement to be mismatched against. Their fixtures
  (`plans/battery37/p8.py:110-120`, `plans/battery37/p910.py:100`) are coverage work, not calibration.

So the claim's *metric* is calibration and 88% of its count is earned; the claim's *headline number* is not.
`plans/round-37-claims.md:19` ("advertised package-gate clauses that no fixture demonstrates, 50 → 0"),
`corpus/QUALITY.md:416-417` ("50 of the classes … advertise") and `SCORECARD.md:566` ("Survivors are
advertised-but-undemonstrated clauses") each overstate by 6. This is a count defect inside a calibration claim,
not a category error: the axis survives, the number does not.

Upper bound if the docstring's setup sentence (`plans/pkg_gate.py:7`) is read to cover absent input files:
M02, M10, M13, M28, M41, M44, M48, M53 are all "file/capture unreadable or absent" branches whose tier is only
K, so the unadvertised set would rise to 14 and the mismatch count to 36. I do not adopt that reading — the gate
itself returns exit 1 on them, so the component advertisement is the fair hook — but the freeze exclusion list
should say which reading it intends, because it excluded `spec not found` / `root not a directory` and admitted
`root is not a git worktree` without a stated rule.

## 5. Secondary findings

1. **M38's kill is a co-occurrence, not a single-defect demonstration.** The reported killer is
   `p7-m28-entry-deleted`, a P7 fixture that declares `P7` — deleting the entry makes the knowledge-file and
   index-row sets differ, so P8's branch fires as a side effect. The isolating fixture exists
   (`plans/battery37/p8.py:118`, `p8-extra-knowledge-file`) but is not the reported killer because
   `plans/round37_c1_verify.py:347-351` reports the first differing fixture in build order. Same shape for M18
   (killed by `p4-capture-unreadable`) and M09 (killed by `p23-p3-heading-renamed`). Q27's limit names
   co-occurrence generally (`corpus/QUALITY.md:444-445`), so this is not a predicate defect — but the "killed
   by" column must not be read as "this fixture demonstrates this class" for those three.
2. **The self-assessment text moved inside the round.** Q27 supersedes Q24's middle clause
   (`corpus/QUALITY.md:448-450` "Supersedes Q24's middle clause … as the proof standard"). A before/after
   mismatch count should hold the self-assessment fixed; here the text being measured changed between the
   freeze receipt and the tip. Harmless for this count (Q24's superseded clause is property-level and enumerates
   no branch), but a calibration claim should state that the three texts were read at freeze and are unamended
   at the tip, or the count is not reproducible from the tip tree alone.
3. **The mutant table asserts advertising without citing it.** `plans/round37_c1_verify.py:62-178` gives each
   mutant an "advertised defect class" string; not one row carries a file:line. That is why the 6 N mutants went
   unnoticed — the claim had no mechanical test for "is this advertised". Wave 1 already conceded the point in
   prose: `.ufo/waves/round-37/build/R37RevClaims.md:69` "the 'advertised' framing is motivational, not the unit
   of count".

## 6. Smallest safe correction

Keep the predicate, the mutant list and the gate untouched (all frozen; `killed=55` is branch coverage and
passes). Change only the three count sentences:

1. `plans/round-37-claims.md:19` → "advertised package-gate clauses that no fixture demonstrates, **44** → 0",
   plus one sentence: 6 of the 55 frozen mutants (M34–M39) silence branches no self-assessment text advertises
   (P8 README/index/coverage-bullet/knowledge-file checks; P9 non-git root), so they are branch-coverage debt and
   are excluded from the mismatch count.
2. `corpus/QUALITY.md:416-417` → "**44** of the classes … advertise" (same one-sentence disclosure).
3. `SCORECARD.md:566` → "Survivors are advertised-but-undemonstrated clauses" gains "over the 49 mutants an
   advertising sentence covers; M34–M39 are coverage, not calibration".

Do not drop M34–M39 from the 55: `plans/round37_c1_verify.py:387` needs them for `killed=55`, and the round's
predicate is frozen. Removing them from the *count* costs nothing and makes the number true.

## Evidence (commands run by this seat)

- `sha256sum plans/pkg_gate.py` → `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` (freeze digest, lane and clone).
- `awk 'NR>=1&&NR<=16' plans/pkg_gate.py | grep -ic <term>`; `awk 'NR>=299&&NR<=329' corpus/QUALITY.md | grep -ic <term>`; `sed -n '564p' SCORECARD.md | grep -ic <term>` → README/index/bullet/knowledge files/git worktree/Negative space/verified-at/recheck/used-by = `0 0 0`.
- `grep -n "killed by=" .ufo/waves/round-37/claims/control-c1-nothing.txt` → M01, M05, M40, M47, M54 (all tier C); `MUTANTS total=55 killed=5 survived=50`.
- `grep -n "MUTANT M" .ufo/waves/round-37/integrate/measure-final.txt` → 55 kills, all clause ids P1–P10/D4/D5.
- `python3 -c "json.load(open('plans/pkg-spec-r35.json'))['entry_rules']"` → `min_quotes 8, min_distinct_locations 8, quote_words [3,25], min_teaches_words 8`.
- Clone of tip `357deceb…` in `/fast/scratch/hyaku/kengaku-r37/F37CritC1Axis/lane`; `--only M34..M39` run above; scratch removed.

VERDICT: c1-axis-calibration-unadvertised-6
