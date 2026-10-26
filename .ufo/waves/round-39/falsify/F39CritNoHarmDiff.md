# F39CritNoHarmDiff — no-harm diff (kengaku round 39, wave 2, falsify)

Seat: critic. Target: what wave 1 and the L1 landed, measured at lane tip
`a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`. Base `b2bdd425` (round-38 tip, `b2bdd42 round-38 verifier spot-check`).

Fixture (fixture rule): `S=/fast/scratch/hyaku/kengaku-r39/F39CritNoHarmDiff`, `git clone -q --no-local` of the lane,
`git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r39/F39CritNoHarmDiff/lane`,
`git -C "$S/lane" rev-parse HEAD` → `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`. All runs below are in that clone,
`TMPDIR` inside `$S`. Scratch removed at the end. Receipts: `falsify/F39CritNoHarmDiff/`.

Axes named: (1) removed lines over lane-authored docs; (2) removed behaviours in the three edited `plans/` tools;
(3) every round-36..38 counter at the tip vs the landing measurement; (4) doc claims that the measured tip contradicts.

---

## 1. Removed lines: 0 over every lane-authored doc

```
$ git -C <lane> diff --numstat b2bdd425 a6832f53 -- SCORECARD.md LOG.md SKILL.md PROVINCE.md SHONEN.md \
     corpus/SOURCES.md corpus/README.md corpus/QUALITY.md corpus/knowledge corpus/lessons
34 0 LOG.md            50 0 PROVINCE.md        47 0 SCORECARD.md        69 0 SKILL.md
51 0 corpus/QUALITY.md 24 0 corpus/README.md   2  0 corpus/SOURCES.md
42 0 corpus/knowledge/tb2-build-pmars-grader.md
346 0 corpus/knowledge/tb2-git-leak-recovery-grader.md
25 0 corpus/knowledge/tb2-git-webserver-grader.md
26 0 corpus/knowledge/tb2-regex-log-grader.md
45 0 corpus/lessons/round-38.md                67 0 corpus/lessons/round-39.md
--- added/removed totals over that scope ---   added=828 removed=0
```
`SHONEN.md` is unchanged (absent from the diff; last touched `9d8a00d`). Receipt: `diff-numstat.txt`.

Whole diff `b2bdd425..a6832f53` (incl. `.ufo/` evidence): `added=58662 removed=65`, and the 65 removed lines sit
in exactly three files — `plans/anchor_digest_check.py` (70+/13-), `plans/ledger_tip.py` (56+/31-),
`plans/mutant_direction_check.py` (105+/21-). No file is deleted and no file is renamed
(`git diff -M --diff-filter=DR --numstat` → empty). Receipt: `diff-numstat.txt`.

So the no-harm question about declarations is answered clean: no doc line, no registry row, no lesson sentence and no
knowledge entry was removed this round. The round only appends to prose.

## 2. Removed behaviours in the three edited plans tools

`removed-lines.txt` holds every removed line verbatim.

### 2.1 `plans/anchor_digest_check.py` (13 removed)
| # | removed behaviour | replacement | reachable at tip? |
|---|---|---|---|
| A1 | a row naming N>1 captures could satisfy its anchor with **one** token (digests of all named captures were unioned into `digs`) | `captures[sid]` per-capture map; every named capture must be `claimed`, else `DEFECT … class=capture-unanchored` | **no** — 0 rows name 2 captures (`--verbose`: `BIND+ lines: 0`, `CAPTURES lines: 0`); `rows=111 tokens=19 defects=0`, exit 0 |
| A2 | verbose `ABBREV` note without a capture name; verbose `RESOLVED` note was an `elif verbose` with no state kept | same notes plus `capture=`; `claimed.update(hit)` on both branches | verbose text only; no consumer |
| A3 | docstring sentence "This copy binds each token to the capture **the row itself names**" (singular) | the round-39 paragraph: token → capture, not the union | prose, and the removed sentence was the weaker claim |

No check was deleted: `digest-short/long/uppercase`, `digest-wrong-capture`, `digest-unknown`,
`abbrev-unresolved`, `token-outside-anchor`, `row-malformed` and the erratum exemption are unchanged in kind.
The only behaviour removed is the union acceptance (A1), which is the `F38AnchorFix` F1 harm; at the tip it is dormant,
so no tip state went green→red.

### 2.2 `plans/ledger_tip.py` (31 removed)
| # | removed behaviour | replacement |
|---|---|---|
| L1 | "A ref the clone already carries is left untouched" — `bind_pin_refs` used a carried `refs/heads/master` even when it named a commit other than the one under audit | `audit_pin_refs`: resolves once, prints `REF AUDIT … state=match` when it equals the tip, binds the sha into every module, and **REFUSEs (exit 2)** when it names another commit |
| L2 | row lines and the per-ledger `LEDGER` line were printed as computed, so a refusal raised by a later ledger or a check body left earlier ledger statements on stdout | statements buffered in `statements`, flushed only after every ledger is evaluated |
| L3 | (format, not behaviour) `REF BIND ref=… rev=… source_ref=…` | `REF BIND ref=… rev=… tip=… source_ref=…`, plus the new `REF AUDIT` line |

L1 is a real **green→exit-2 reclassification** for one clone shape, and I reproduced it as a paired control
(`paired-ledger-stale-ref.txt`), fixture = copy of the tip clone with `HEAD=34158b0c`, `refs/heads/master=acf4375`:

```
landed tool : TIP commit=34158b0c… ; REFUSE stale pin ref: refs/heads/master resolves to acf4375… but the commit
              under audit is 34158b0c… ; plans/defect_ledger.py would observe a different tree      exit=2
round-38    : rows=9 closed=9 observed_pass=9 mismatches=0                                             exit=0
```
The removed behaviour was a **false green**: the round-38 tool printed `TIP commit=34158b0c` while its pin rows read
`master=acf4375`. So L1 removes a wrong-tree pass and replaces it with a loud exit 2 that names both revisions — the
exit class `2` is the one `SKILL.md:581` already assigns to clone refusal. Price: any seat or receipt that ran
`ledger_tip --lane <clone>` on a clone whose `refs/heads/master` has since moved now gets exit 2 where round 38 gave
`rows=9 … exit 0`. That is the documented fleet shape detail worth knowing: my own fixture clone at the assignment tip
is exactly it (`HEAD=a6832f53`, and the lane's `refs/heads/master` is now `acf437542b00ae1723eba9dcc79d46af2e40d96e`,
the wave-2 dispatch commit). `--source` cloning of a detached clone still takes the `REF BIND` path and is green
(`counters-at-tip.txt` tail).

L2 closes a violation of the tool's own stated refusal contract ("`REFUSE <reason>` … and no summary line") and removes
no green path: for a run that does not refuse, the buffered order is the printed order.

### 2.3 `plans/mutant_direction_check.py` (21 removed)
| # | removed behaviour | replacement |
|---|---|---|
| D1 | `observed=invalid` (a frozen pair no longer matches the gate once) printed with **no** INVALID marker and exited 0 | `observed=invalid INVALID`, `invalid` counted, `LEGS mutants=… invalid=…` line, exit **3** when nothing is mislabelled |
| D2 | `UNWITNESSED` from the single leg always exited 0 | two legs decide; `ok` vs `UNWITNESSED` (and `MISLABELLED` vs `ok`) becomes `LEGS-DISAGREE`, exit **3**; `MISLABELLED` from either leg is the verdict (`legs=<a>,<b>` appended when the legs differ) |
| D3 | a counter with a different list surface raised `AttributeError` (traceback, exit 1) | `SETUP … missing=… non_6_tuple_rows=…` on stderr, exit **2** |
| D4 | the printed `observed=` set was leg 1's set | union of both legs (`seen | other`) |
| D5 | `bad` counter name | `mis`, and the `DIRECTIONS total=<n> mislabelled=<m>` line kept verbatim |

Leg 1 is kept verbatim in code (comment `# leg 1: the round-38 rule, kept verbatim`), so no check that could fail before
was deleted; what was removed is the exit-0 classification of `invalid` and of a one-legged `UNWITNESSED`.

## 3. Round-36..38 counters at the tip

`counters-at-tip.txt` (full tails + exits). Summary, and the same lines in
`.ufo/waves/round-39/integrate/measure-final.txt` (TIP `34158b0c`) for comparison:

| instrument | at `a6832f53` | measure-final (`34158b0c`) |
|---|---|---|
| `round36_c1_verify.py` | `rows=4 … mismatches=0`, `PREDICATE C1 pass`, exit 0 | same, exit 0 |
| `round36_c2_verify.py` | `checks=6 defects=0`, `PREDICATE C2 pass`, exit 0 | same |
| `round37_c1_verify.py` | `BATTERY fixtures=64 wrong=0`, `MUTANTS total=55 killed=55 survived=0`, `PREDICATE C1 pass`, exit 0 | same (line 451/507/508) |
| `round37_c1_attribution.py` | `ATTRIBUTED 55/55 UNATTRIBUTED=0`, exit 0 | not in measure.sh |
| `round37_c2_verify.py` | `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 | same |
| `round38_c1_verify.py` | `PINS total=14 mismatched=0`, `BATTERY fixtures=86 wrong=0`, `MUTANTS total=22 killed=21 survived=1`, `PREDICATE C1 fail`, **exit 1** | identical (360-362) |
| `round38_c2_verify.py` | `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 | same |
| `mutant_direction_check.py` | `DIR N21 D5 … MISLABELLED`, `LEGS mutants=22 disagree=0 invalid=0`, `DIRECTIONS total=22 mislabelled=1`, **exit 1** | identical (565-567) |
| `anchor_digest_check.py` | `rows=111 tokens=19 defects=0`, exit 0 | identical (569) |
| `ledger_tip.py --source` | `rows=9 closed=9 observed_pass=9 mismatches=0`, exit 0 | identical (614-615) |
| `order_check.py` round 39 / round 38 | `ORDER RESULT PASS` exit 0 / `ORDER RESULT FAIL hits=1` exit 1 | identical (239-240, 247-248) |
| `sources-census.sh validate` | `ok`, exit 0, `registry_rows=111 knowledge_files=46 index_rows=46` | identical |
| `sha256sum -c …/frozen-digests.txt` | 9/9 `OK`, exit 0 | identical |

No counter, no tool and no census result differs between the assignment tip and the landing measurement. Three of them
are red **at the landing measurement too** (`round38_c1` exit 1, `mutant_direction_check` exit 1, `order_check` round 38
exit 1), so they are inherited state, not round-39 regressions; `round38_c1_verify.py` is not modified this round
(absent from the numstat), and its `killed=21 survived=1` is the round-38 N21 shape recorded in `QUALITY.md:505-513`.

## 4. Attacks

**A-1 — the mutant-direction exit surface is not what its two live contract rows say.**
`SKILL.md:585` enumerates exactly two outcomes for the row ("`0` every frozen mutant's declared kill direction is
observed or unwitnessed · `1` a `MISLABELLED` mutant") and `corpus/QUALITY.md:511` says "exit 1 iff `m > 0`". The
landed tool returns three: `plans/mutant_direction_check.py:176` `return 1 if mis else (3 if (split or invalid) else 0)`,
and prints a line (`:174`) neither row mentions. Counterexample, same tampered tree, both tools (`direction-exit-surface.txt`):

```
landed (a6832f53) : DIR N20 D4 declared=silence observed=invalid INVALID / LEGS mutants=22 invalid=1 /
                    DIRECTIONS total=22 mislabelled=0                                   exit=3
round-38 (b2bdd425): DIR N20 D4 declared=silence observed=invalid /
                    DIRECTIONS total=22 mislabelled=0                                   exit=0
```
Impacted axes: contract/operability (a caller reading Q29 as "`m=0` ⇒ 0" downgrades a red to a pass), claims
(authority for the exit code lives in two docs that no longer enumerate it). A second reachable path exits 2
(`--counter plans/round39_c1_verify.py` → `SETUP … exit=2`), also undocumented in that row.
Smallest safe correction: doc-only — rewrite the `SKILL.md:585` status cell to
`0 ok both legs · 1 MISLABELLED from either leg · 2 setup (counter without the round-38 surface) · 3 INVALID or
LEGS-DISAGREE with no mislabel`, and add the `LEGS mutants=… disagree=… invalid=…` line to `QUALITY.md:511`. No code
change: the behaviour is the improvement the round claims (Q29 hostile-independent-leg), only its enumeration is stale.
This finding is a documentation defect, not a green→red on the tip (`invalid=0`, `disagree=0` there).

**A-2 — "every no-harm instrument green at the landing tip" is contradicted by the file it cites.**
`LOG.md:1179` at the tip: "every no-harm instrument green at the landing tip (`integrate/measure-final.txt`)."
The cited file carries three non-green results: line 360-362 `MUTANTS total=22 killed=21 survived=1` /
`PREDICATE C1 fail` / `exit=1`; line 566-567 `DIRECTIONS total=22 mislabelled=1` / `exit=1`; line 247-248
`ORDER RESULT FAIL` / `exit=1` (`claims-vs-measure.txt`). `SCORECARD.md:1388` is accurate on the first and third and
silent on the second. Impacted axes: provenance/precision of the round's own no-harm claim; a reader who takes the LOG
sentence as the measured state inherits three false "green" cells. Smallest safe correction: replace the LOG clause with
the measured enumeration and the reason each red is inherited, e.g. "every no-harm instrument re-run at the landing tip:
round-36/37 C1+C2 pass, round-38 C1 `killed=21 survived=1` as landed (N21 unreachable), round-38 C2 pass, direction
check `mislabelled=1` (N21, as landed), anchor `defects=0`, ledger-tip `mismatches=0`, census 0, digests 9/9,
`order_check` r39 PASS / r38 FAIL (the gate's retroactive finding)". One sentence, no other edit.

**A-3 (accepted as a fix, recorded so the tradeoff is not silent) — the ledger stale-ref removal changes one tip-shaped
input from exit 0 to exit 2.** Evidence in §2.2. The removed behaviour was a wrong-tree green, so the trade is right, but
it is a *contract* change and the tool's row (`SKILL.md:581`) still describes the output only as
`rows=… mismatches=…`: it does not mention `REF AUDIT`/`REF BIND` provenance lines or the stale-ref refusal. Either name
them in the row or state in it that a stale `refs/heads/master` is a `2`; a one-line addition.

**A-4 (provenance, not a defect) — `measure-final.txt` names `TIP 34158b0ca0f7b527d60af0e612511f7f27aebcbc`, not the
tip this seat was told to measure.** `34158b0c` is the parent of `a6832f53`; the two commits differ only by docs, the
census-after file, the audit replays and the wave-2 generator (the numstat above shows the doc-only delta). Every counter
result is identical at both (§3), so the landing measurement still describes the tip for the no-harm question — but the
file's own `TIP` line should not be read as naming the tip in any later round.

## 5. What I did not find

- No doc, lesson, knowledge, registry or README line was removed (§1).
- The three tools' own docstrings no longer assert anything their code contradicts: the anchor tool's removed singular
  claim is replaced, `ledger_tip`'s removed "normal clones, byte-identical output" sentence is gone (and is indeed now
  false — `REF AUDIT` adds a line), the direction tool's removed single-leg/exit-0 sentences are replaced.
- No consumer parses the changed output shapes: `grep -rn "REF BIND|REF AUDIT"` outside the tool finds only `.ufo`
  wave-1 harnesses (`plans/`, `scripts/`, `SKILL.md`, `QUALITY.md` clean); `DIRECTIONS total=`/`mislabelled=` has no
  parser; `REF AUDIT`/`capture-unanchored`/`stale pin ref` appear in no live doc. One wave-1 harness detail worth
  passing to round 40: `R39PlanNext/h_ledger.py:119` mutates the pre-fix `REF BIND` print string, so on the landed tool
  its L04 is a `SETUP needle count 0` no-op (`out_ledger_r5.txt`), not a killed mutant.

Axes improved by the moves I would keep: A-1 and A-2 are doc-only corrections that raise the contract and provenance
axes and harm none; A-3 is a one-line row addition; A-4 is a wording guard for the next round's citations.

VERDICT: no-harm-removed-lines-0
