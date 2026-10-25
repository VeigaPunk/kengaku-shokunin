# Round 30 falsify — Q7 / Q8 / Q9 and index-coverage-frontier parity

Item: Q7 (landed and discoverable in the same commit), Q8 (rejections kept with reason and flip
condition), Q9 (a rejection's reason follows from its evidence), plus index row / coverage-map row /
frontier-discharge parity against the admission instruction. Leaf seat; no edits to the lane outside
this file; no installs (pacman paused host-wide, nothing needed; tools used: `git`, `grep`, `awk`,
`sha256sum`, `python3 plans/adoption_check.py`, one `curl`).

Candidate under audit: `corpus/knowledge/contamination-transparency-card.md`

VERDICT: FAIL

Three of three assigned criteria fail on the bytes as they stand. Q7 fails because nothing has
landed; Q8 fails because the flip-condition column was dropped on the way from draft to Gate; Q9
fails on one falsified reason (S105) that the round's own build seat had already corrected, plus one
wrong count and one rule applied to the wrong object.

## Bytes pinned

Lane tip `363a4eb` (`round-29 verifier spot-check (integrator, hyaku)`) — unchanged during the audit.
`git status --porcelain` → 18 entries, none of them round-30 content committed.

Both audited files were being edited by peers while this audit ran, so the pins below are the bytes
every citation in this report resolves against. Snapshots: `/tmp/r30fx-EntryQ7Q9/{round-30,entry}.snapshot.md`.

| artifact | md5 at audit close | observed moves during audit |
|---|---|---|
| `corpus/lessons/round-30.md` | `8b360305716f59150c2191d7f54f2bb2` | `ce437a33…` → `4b4073d7…` → `eeebe117…` → `8b360305…` |
| `corpus/knowledge/contamination-transparency-card.md` | `c378e7f2de91007bf03c4459e836cd56` | `d3cc2bef…` → `48231626…` → `c378e7f2…` |
| `corpus/README.md` | `b3fc6bb1c808b696b80a6bcd63a45ccb` | stable |
| `corpus/SOURCES.md` | `ef80b210995bb0faf960866d45068b6d` | stable |

Every Gate cell and entry cell cited below was re-verified against `8b360305…` / `c378e7f2…` at
04:47 local. One peer edit did change content this report would otherwise have got wrong: the admit
row's cited-report list shrank from five falsify reports to seven differently-named ones (see Q7.2);
the corrected reading is below.

## Q7 — landed and discoverable in the same commit: FAIL

**Q7.1 (high) — nothing has landed.** The entry, its index row, its coverage row and the frontier
discharge are all working-tree bytes; the last commit touching any of them is round 29's
(`ff476d0`, `git log -1 -- corpus/README.md`). Q7 is a landing-time test, so it can still go green,
but two sub-clauses are already violated rather than merely pending:

- `plans/round-30-claims.md` C1, C2 and C3 each say **"Control (committed at freeze)"**. None is
  committed: `.ufo/waves/round-30/` is untracked in its entirety, including
  `claims/control-nothing.txt`, `claims/defects-before.txt`, `claims/gate-before.txt`.
  Q7's clause "no support rests on … an unlanded working copy" is therefore already broken by the
  claim controls themselves, independent of when the admit commit happens.
- The Gate's `read` column points into `.ufo/waves/round-30/build/` (untracked) and its admission
  row names second-seat reports in `.ufo/waves/round-30/falsify/` (untracked).

**Q7.2 (high) — the Q10 second seat the Gate names does not exist.** `corpus/lessons/round-30.md:17`
cites `.ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md` as the first of the "second-seat
re-reads for this admission", and `:31` names it again as *the* Q10 second seat ("a `reviewer` seat
that did not write the entry re-opened all six sources and re-derived every number"). That file is
absent: `ls .ufo/waves/round-30/falsify/` → no `R30FxEntryCompleteSet.md` (24 other files, including
the six `R30FxSrcS081…S086.md` per-source re-reads, which do exist). Six per-source re-reads do not
substitute for the complete-set review the Gate cites, because Q10's requirement is a single seat
re-opening *all* six and re-deriving every number. Those bytes cannot land in the same commit as the
entry: they do not exist to be committed.

**Q7.3 (medium) — the coverage-map half of Q7 has no checker.** `plans/adoption_check.py:17,76-78`
counts only index table rows (`indexed`); `grep -n coverage plans/adoption_check.py
plans/round30_defects.py` → no hits. C1's frozen predicate asks for "one index row in
`corpus/README.md`" and never mentions the coverage row. A landed entry with an index row and **no**
coverage row prints `census=ok`. I ran the counter: `entries=1 indexed=1 cited_rows=6
rows_present=6 rows_mined=6 usedby_ok=1 census=ok`, exit 0 — it reproduces exactly as claimed, and it
is silent on the thing Q7 names.

**Q7.4 (medium) — the instruction the frontier discharge supersedes was edited in place.**
`git show HEAD:corpus/README.md:272` versus `corpus/README.md:274`: an 18-word parenthetical was
inserted into the superseded instruction —

> `… gate a knowledge entry on Q1–Q8` → `… gate a knowledge entry on Q1–Q8 (the entry's own
> answerability questions, labelled **CG1–CG8** in the landed entry so they cannot be confused with
> `QUALITY.md` Q1–Q8).`

The discharge at `README.md:275` now sits below a bullet that is no longer the bullet it supersedes.
QUALITY R1 and Q6 both require the old line to stay byte-identical and the correction to be
appended; the append happened and the rewrite happened too. Worse than style drift: the round's
reading of an ambiguous instruction was written *into* the instruction, so the discharge can no
longer be checked against the text it claims to discharge.

**Q7.5 (low, disclosed) — the flip's load-bearing relation is not lane-sourced.** `entry:36-45` pins
the campaign's round-6 staging file by absolute path and sha256
`66651007989a7fb5df4671f5f86e69ab1436517025a821afe8c451641a3533b9`; I re-derived the hash against
`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md`
— it matches byte-for-byte, and the file is tracked there (commit `d9583b5a`) and clean. So this is
not an unlanded working copy. It is still a discoverability cost Q7 exists to prevent: the amendment
claim (the thing the Gate admits) cannot be checked from this lane's commit, and neither the index
row (`README.md:65`) nor the coverage row (`README.md:242`) repeats the caveat the entry states at
`:123-125`.

Post-commit check that settles Q7 (run once the admit commit exists):
`git -C <lane> show --stat <sha>` must list the entry, `corpus/README.md` and `corpus/SOURCES.md`;
the `<sha>:corpus/README.md` blob must contain both the index row and the coverage row; every falsify
report the Gate cites must exist in that tree; and `git status --porcelain` must show no
round-30-owned path outside that commit.

## Q8 — rejections kept with reason and flip condition: FAIL

**Q8.1 (high) — the Gate table has no flip column.** `corpus/lessons/round-30.md:15` is
`|candidate|decision|reason|read|`. Seven non-admit rows (`:18` judge-calibration, `:19`
mitigation, `:20` card-publication, `:21` bulk, `:22` S091 register, `:23` S105 register — and the
`:17` admit row's "flip" is a *previous* flip being met, not a condition on this candidate) carry
zero flip conditions. No `rejected` SOURCES row was added either — `git diff --numstat
corpus/SOURCES.md` is `6 0`, all six mined (S081–S086). The flips were written and lost at landing:
`.ufo/waves/round-30/build/R30DraftGate.md:17` says "Every row carries reason, flip condition and
in-tree read pointers", and `:89-90` records a drafted flip ("nothing to flip").

**Q8.2 (high) — the two register rows lost flips that round 29 had recorded.** `round-29.md:182`
(S091) ends "… | an actual page failure on re-fetch, or the anchor text disappearing from the
article"; `round-29.md:183` (S105) ends "… | a re-fetch that renders the article rather than an error
page". Neither flip survives into `round-30.md:22-23`. This is not an omission in a new record; it is
a deletion from an existing one.

**Q8.3 (medium) — S105 was downgraded without new evidence.** The fleet report
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-29/kengaku.md:57-62` reads "`kengaku round3 S105`
→ **quote-present**; the quoted Japanese text is METI's WAF error shell returned to a bare client,
and the row's hold-out quote is present in the 200 snapshot", evidence `R29a2QuarS105.md` (present,
11,661 B, `.ufo/waves/round-29/attempt2/build/`). Round 30 records "unverifiable". A settled verdict
was reversed, and with Q8.1/Q8.2 there is now no flip saying what would settle it again.

**Q8.4 (low) — the entry's own three rejections do carry flips** (`entry:164`, `:167`, `:170`), so
Q8 holds for the *claim-level* rejections inside the entry. It is the seven *screened candidates* in
the Gate that have none. The two loci are not interchangeable: Q8 wants the candidate screening
record, and the entry's `## Rejected` section is not the Gate.

## Q9 — a rejection's reason follows from its evidence: FAIL

**Q9.1 (critical) — `round-30.md:23` is false against its own cited locator.** The row reads
"the payload is a Japanese page whose quoted text reads like a fetch-failure render". The payload I
fetched on 2026-10-25 from the row's URL
(`http://web.archive.org/web/20251118034714/https://www.meti.go.jp/policy/mono_info_service/geniac/selection_1/result_1/index.html`)
is HTTP **200**, 13,028 bytes, and contains the held-out-data sentence
`ホールド・アウトデータ(最終的な性能評価を行うための非公開のデータセット)を生成・評価を行いました` plus both
named benchmarks `Jaster-GENIAC-v0.1` and `JMT-Bench-GENIAC-v0.1`; occurrences of
`指定されたページまたはファイルは存在しません` ("the specified page or file does not exist"): **0**.

That string is exactly what the campaign **register** row holds —
`.ufo/waves/corpus-expansion-1/absent-defect-register.md:102`
(`kengaku | round3 | S105 | payload-absent | … | 指定されたページまたはファイルは存在しません`). Round 30
restated the register's classification without opening the source, so its reason describes a
different artefact than the row it rejects. The verdict family ("not a fabrication") is defensible;
the reason is refuted, and Q9's own text settles it: "A correct verdict with a wrong reason is a gate
failure." The row's `read` pointer is `.ufo/waves/round-30/assimilation/quarantine-slice` — 52 bytes,
`s091 payload-absent` / `s105 payload-absent` — which contains no payload at all, so the claimed
evidence is neither in the lane nor named.

**Q9.2 (high) — the round had the correction in hand and landed the refuted cell anyway.**
`.ufo/waves/round-30/build/R30DraftGate.md:77` — "S105's verdict is quote-present in the archived 200
snapshot per the fleet report"; `:92` flags three further Gate cells against the bytes, including the
"63". The build receipt and the Gate sit in the same untracked wave directory and disagree. That is
the failure mode the round's own `## Mistakes` section is about ("a repair that prints green"), one
layer up: a measured correction that never reached the record it corrects.

**Q9.3 (high) — the bulk row's entry count is wrong.** `round-30.md:21` says "remaining 63 staged
entries". Measured: `ls *.md | wc -l` → **65** and `grep -l "^source: S" *.md | wc -l` → **65** in
`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/`; `MERGE-REPORT.md:7` →
"proposed knowledge entries: **65**". The Gate decides four of them individually (`:17` admit, `:18`,
`:19`, `:20` reject) → **61** remaining. The build seat's derivation (`R30DraftGate.md:92`, 65 − 1 −
4 = **60**) additionally counts the folded stale duplicate. Either 60 or 61; 63 is reproducible only
by excluding two entries and then counting the three individually rejected ones a second time. The
row count in the same cell does re-derive: 175 staged rows (`SOURCES.append.md`) less the six
admitted = 169; its two escaped-pipe rows are S093 (NF=14) and S101 (NF=17), and 2 + 167 = 169.

**Q9.4 (medium) — the 63 was introduced during this wave**, after the drafting seat had already
written 60 into `R30DraftGate.md:77,92`. Observed during this audit: the row read "remaining
staged entries and 169 rows" on my first read and "remaining 63 staged entries and 169 staged rows"
on the second. I did not snapshot the earlier bytes, so that is a session observation and not a
pinned diff; the defect stands on the pinned bytes either way.

**Q9.5 (medium) — one rejection reasons with a rule that governs a different object.**
`round-30.md:19` rejects `contamination-mitigation-comparative-evidence-2026-10-23.md` with
"a second theme … sources S120/S121 not opened this round; CORPUS rule 4 — no row is appended that no
admitted entry cites". Rule 4 is a **row-append** rule; the object here is an entry. The
property-based reason the draft measured and the Gate dropped (`R30DraftGate.md` item 5) is correct
and re-derivable: staged `S120` (`SOURCES.append.md:50`) is the same document as lane `S001`
(`corpus/SOURCES.md:23`) — both `aclanthology.org/2026.gem-main.50`, same title, "Are LLM Benchmarks
Already Contaminated? A Systematic Review of Contamination Detection Methods" — i.e. Q6 one document
two rows, plus Q2 on a one-source argument when S121 was never opened. Q9 wants the reason that
follows from the evidence; the landed reason follows from a schedule.

**Q9.6 (medium) — the entry overstates its own rejection evidence.** `entry:163`: "its `ground:`
line explicitly declines the amendment relation the flip required". The staged
`contamination-transparency-card.md` ground line reads "… the *admission* of the card against the
lane's existing `knowledge/contamination-detection-and-transparency.md` vocabulary is the lane's
call, not this entry's" — it defers the relation to the lane and names only the vocabulary entry. It
never mentions the three tabulated designs, never says "amendment", "union", "AI Alliance", "CTC" or
"GEM" (grep → 0 hits). Deferring is not declining, and "explicitly" is unsupported. The other half of
the reason is true against the same bytes: it does present R1–R5/S1–S2 as *the* card format. Right
verdict, overstated reason — Q9 applies to the entry's own rejection log as much as to the Gate's.

**Q9.7 (pass, credit) — `judge-calibration-thresholds` reproduces.** `round-30.md:18`'s surviving
objection is Q3: kappa `0.46` / ceiling `0.84` at `:40-42` of the staged file appear in none of its
three `source:` anchors — `sed -n '1,12p' | grep -c "0\.46\|0\.84"` → 0, anchors being S078, S081,
S087; and `:73-75` no longer claims a missing threshold. Same property, same evidence.

**Q9.8 (pass, credit) — `card-publication-contracts` reproduces.** `S167` is `docs | C` in the
campaign (`SOURCES.append.md:97`, a machine rendering of arXiv 2606.09809) and the campaign holds
that paper at tier B (`SOURCES.append.md:56`, `S126`); the rejected entry's Chinese-framing claim
cites S167 alone (`card-publication-contracts.md:4` and its closing paragraph). Q2 tier floor is the
property, and the cited row is the evidence for it.

**Q9.9 (pass, with one overclaim) — S091.** The register payload
(`.ufo/waves/corpus-expansion-1/absent-defect-register.md:101`) is a truncated
`import re,html;…;pri` command line, exactly as `round-30.md:22` says. The same cell's "re-read this
round" is unsupported: `R30DraftGate.md`'s fourth recommended correction records that no round-30
fetch of the NEC page appears in the wave receipts.

## Index / coverage / frontier parity

| pair | verdict | evidence |
|---|---|---|
| entry ↔ index row | **parity holds** | `README.md:65` names the six-id set, "amendment … not a fourth card design", CG1-CG8 and the negative space; matches `entry:1-9` and `entry:79-103`. Exactly one index row (`grep -c '^| \`knowledge/contamination-transparency-card.md\`'` → 1) |
| index row ↔ coverage row | **parity holds** | `README.md:242` repeats the same id set and relation; the round-24 row it amends is the one it names (`README.md:241`) |
| coverage row ↔ entry | **parity holds** | four claims checked against the entry: amendment (not a design), R1-R5/S1-S2 mapping, CG1-CG8 gate, three "not" clauses (measurement / runtime judge / adopted card) — all present at `entry:51-78`, `:79-103`, `:104-129` |
| frontier discharge ↔ superseded instruction | **fails, three ways** | (a) the instruction was edited in place (Q7.4); (b) "no private-split or hidden-test-governance release was opened this round" is falsified by the discharge's own entry: **S083** was opened 2026-10-25 and is a peer-reviewed benchmark paper publishing a separated engine from hidden implementations plus a "practical threat model and refresh protocol" (`entry:3`; CG7 row `:94`). If the intended claim is "no maintainer-side governance *document*", that is what it must say; (c) "draft a card template" is discharged by a field-mapping table, not a template artefact — the entry itself says the card "is a format, not a finding" (`entry:106`) and supplies no fill-in instrument |
| entry internal pointer | **low defect** | `entry:146-147` reads "Coverage map: `corpus/README.md` row *Contamination transparency card format*. New: `Contamination transparency card format`." — the label is named twice |

Two parity facts cutting the other way, recorded so the verdict is not read as blanket distrust: the
entry's sha256 pin of the staging file re-derives exactly (Q7.5), and the entry's disclosure that the
mapping is "not lane-sourced" (`entry:123-125`) is honest — it is why Q7.5 is low rather than high.

## Residual risk

- The frontier's remaining limb ("benchmark-maintainer releases on hidden-test governance") had a live
  candidate in the round's own staged population: `S105` is a hold-out-data governance practice with
  named, versioned benchmarks, `status=mined`, `opened=2026-10-23`, `used-by`
  `cjk-benchmark-governance-2026-10-23.md` (`SOURCES.append.md:35`). It was rejected from a stale
  register classification rather than from its bytes, so the frontier sentence and the Gate now rest
  on each other.
- Both audited files were edited by peers during the audit (four md5s for the lesson, three for the
  entry). Findings are stated against the pins in §Bytes pinned; a later edit can move a cited line
  number without moving the defect.
- Q7's post-commit form is untested by construction: no commit exists, so "entry + index row +
  coverage row + frontier discharge in one commit" has been prepared, not demonstrated.

## Verification gaps (what I did not run)

- No `plans/gate_timing_check.py --lesson corpus/lessons/round-30.md --commit <sha>`: the Gate names
  `<admitting sha>` literally, so there is no commit to test (Q7.1).
- No re-fetch of the other five source locators — outside this item; their quotes belong to another
  seat.
- No `python3 plans/round30_defects.py --lane .`: that is C2's counter, not mine. C1's counter was run
  and reproduces.
- The S105 re-fetch is a single 2026-10-25 GET of the archive URL (13,028 B); I did not retry the
  original METI URL, which the staged row says now serves METI's own "Page Not Found".
