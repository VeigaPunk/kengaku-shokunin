# R31DefR8 — R8 licence grounding: "the CC0 card"

Seat: L1Kengaku31.R31DefR8 (reviewer, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Baseline lane tip `0883e72ef8474ca42ac1a54eb0273079f1507035`. Access date for every source opened this
seat: **2026-10-25**. No production edits made by this seat; the entry change quoted in §(c) was made by
another seat at 05:51:57 and is reviewed here, not authored here.

Defect under review (`plans/round31_defects.py:28-29`, routed from
`corpus/lessons/round-30-verifier-spotcheck.md:182-183`):

> R8  the entry names "the CC0 card" at :139; no registry row records a CC0 licence for
>     that design, so the adjective is ungrounded.

Anchor check on the frozen tree: `git show 0883e72:corpus/knowledge/contamination-transparency-card.md | grep -n 'CC0'`
→ `139:  (R1 strata, S1's acquired type) are common — a decision rule the CC0 card cannot supply on its own,`
— the routed line pointer is correct at HEAD.

---

## (a) Every licence claim in the lane registry, with its row id

Registry has 88 rows (`grep -c '^| S[0-9]' corpus/SOURCES.md` → `88`).

Sweep, as assigned:

```
$ grep -n -i 'cc0\|cc by\|creative commons' corpus/SOURCES.md
105:| S081 | Benchmark Contamination: A Taxonomy Organized by Defeated Mitigation — https://arxiv.org/abs/2608.29463 | paper | B | ... the abstract also announces the release of its JSON Schema, validator and worked examples (CC BY 4.0) | arXiv 2608.29463 v1, abs page (HTML) line 124: "because it is a property of one run, ...
```

Widened sweep for the whole licence family (to catch spellings the assigned pattern misses):

```
$ grep -n -i -o '.\{0,60\}\(licen\|apache\|mit license\|public domain\|cc0\|cc by\|creative commons\).\{0,60\}' corpus/SOURCES.md
105: release of its JSON Schema, validator and worked examples (CC BY 4.0) | arXiv 2608.29463 v1, abs page (HTML) line 124: "beca
132:itory inventory discovered raw tasks, evaluator, helper and LICENSE:4 identified/screened files,3 new source rows S061–S063,
132:LICENSE retained without separate row. Existing13 source rows reo
```

Line 132 is a search-notes bullet (`Round28 task-spec/reference-consistency search`, `corpus/SOURCES.md:132`),
not a table row: it records that a repository inventory counted four `LICENSE`-named files and retained them
without a separate row. It makes **no licence-grant claim**.

So the lane registry holds **exactly one licence claim**:

| Row | Licence string | What the string is attached to | Cell |
|---|---|---|---|
| S081 (`corpus/SOURCES.md:105`) | `(CC BY 4.0)` | the arXiv taxonomy paper's released four-field disclosure protocol — "its JSON Schema, validator and worked examples" | the *what-it-supports* cell |

Two properties of that one claim matter for R8:

1. **It is not about a card design.** S081's CC BY 4.0 attaches to the paper's own protocol release; the
   entry's three tabulated designs are the AI Alliance maintainer template, the CTC v1.1 form and the GEM
   §7 proposal. No row in the registry is any of those three: `grep -n -i 'contamination-disclosure-paper\|Jangulo7\|DISCLOSURE.md' corpus/SOURCES.md`
   → no output, and `AI Alliance` appears in no row.
2. **Its anchor cell does not quote it.** S081's anchor cell quotes three spans (the one-run rule, the five
   types, the two-variables sentence) and never the licence sentence; the licence lives only in the support
   cell. Freshness check this seat, one page, to see whether the recorded string is at least true:

```
$ curl -fsSL -A 'kengaku-review/1.0' https://arxiv.org/abs/2608.29463 -o arxiv-2608.29463.html
bytes=44646  sha256=4c81bd3c180736318ed03e31968fa4d109b94025ec596203dbc4e963b396908a
<title>[2608.29463] Benchmark Contamination: A Taxonomy Organized by Defeated Mitigation</title>
line 124: "…We operationalize it as a four-field disclosure protocol in which &#34;unknown&#34; is a valid
           entry, released under CC BY 4.0 with a JSON Schema, a validator, and worked examples. Two coders…"
```

S081's `(CC BY 4.0)` is true at its cited locator (abs page line 124, matching the row's own locator). The
defect is therefore *not* in S081; it is that the entry imported a licence word that no row carries.

## (b) Does any row support "CC0" for the design the entry names?

**No — for every reading of "the design the entry names".** Four independent records, all read this seat:

| Record | CC0? | What it records |
|---|---|---|
| Lane registry, 88 rows | none | only S081's `CC BY 4.0` (paper protocol, not a card) |
| Staged append `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md` (read-only, 181 lines) | none | `grep -i cc0` hits are commit-hash substrings, not licence strings: `9aa0ff9d943d5b8c08cc0f92c6bdccd37f66447b` (S163, append line 93) and its `08cc0f92…` prefix |
| Staged schema file `knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md:89` | none | "The CTC v1.1 form is a **protocol artefact**, released CC BY 4.0 with a validator, but the lane has not found it published inside a benchmark release." No licence string for the AI Alliance template or the GEM §7 proposal anywhere in that file |
| Staged row S132 (append line 62), pinned commit `4dba1ed9b2ace8b71a2edcd5fa6ce0337cf08ba6` | none | anchor: header line `"Version 1.1 · CC BY 4.0 · 2026"`; `status=mined`, `opened=2026-10-24`, `used-by corpus/knowledge/card-design-arbitration.md` |

S132's `used-by` target does not exist in this lane (`ls corpus/knowledge/card-design-arbitration.md` →
`No such file or directory`), which is the second proof that the row is **staged, not lane-admitted** — the
entry already says as much ("That file is **staged, not lane-admitted**").

Live settlement of the artefact itself — the single page named by S132, fetched once, hashed:

```
$ curl -fsSL 'https://raw.githubusercontent.com/Jangulo7/contamination-disclosure-paper/4dba1ed9b2ace8b71a2edcd5fa6ce0337cf08ba6/DISCLOSURE.md' -o disclosure-v1.1.md
bytes=14181  sha256=80363c6110d9795cce24cbb64349ed3bae75ca7697e69cb8ecfa1f382f38a3cb
line 1: "# Contamination Disclosure v1.1 — the four fields"
line 3: "**Version 1.1 · CC BY 4.0 · 2026**"      (od -c: `* * V e r s i o n   1 . 1   302 267   C C   B Y   4 . 0 …`)
licence tokens anywhere else in the file: none (grep -i 'cc0|cc by|creative commons|licen' → line 3 only)
```

Every record that names the card's licence says **CC BY 4.0**; **no record says CC0**. The adjective is
ungrounded, and it is the wrong licence in kind as well as in string: CC0 is a public-domain dedication with
no attribution term, CC BY 4.0 requires attribution — an entry that silently converts one into the other
misstates the artefact's reuse terms.

Referent note (why no reading rescues the word): the sentence does not name a design. The only design the
entry describes as released is "the released CTC v1.1 form" (mapping-table column header), i.e. the artefact
above → CC BY 4.0. If "the CC0 card" instead means "a single published card instance", then it names no
design at all and still carries a licence no row records. Either way R8 is a true positive.

## (c) Minimal honest repair — and the state of the tree

Three candidate repairs, ranked against the lane's own admission rules:

1. **Drop the adjective (chosen, and already applied).** The sentence's function is logical, not
   attributive: one release's card cannot supply a population-level decision rule. The licence carries no
   weight in the argument, so removing it loses nothing and asserts nothing.
2. **Name CC BY 4.0.** Wrong repair *now*: the only row that records it for the card (S132) is staged and
   outside the entry's declared citation set ("this entry's citation set is exactly S081–S086"), and the one
   registry row that does record `CC BY 4.0` (S081) attaches it to the paper's protocol, not to the form.
   Writing it here would swap one ungrounded adjective for another of the same class.
3. **Mark it unverified** ("licence unverified in this lane"). Honest but noisy: the sentence needs no
   licence at all, so this adds a caveat where deletion is exact.

Applied in the worktree by another seat (05:51:57, not this seat's edit), hunk `@@ -135,8 +137,8 @@`:

```diff
-  and populated (not "unknown") would show that the fields this entry's sources measured as rare
-  (R1 strata, S1's acquired type) are common — a decision rule the CC0 card cannot supply on its own,
+  would show that the fields this entry's sources measured as rare
+  (R1 strata, S1's acquired type) are common — a decision rule the card design cannot supply on its own,
```

Reviewed as correct: the bullet survives, the referent is now design-neutral, no licence token remains
(`grep -n -i 'licen\|cc by\|cc0' corpus/knowledge/contamination-transparency-card.md` → rc=1). If a later
round wants the licence word back, the order of operations is: admit S132 (fix its `used-by` path first),
then cite `DISCLOSURE.md:3` at commit `4dba1ed9…` with sha256 `80363c6110d9795cce24cbb64349ed3bae75ca7697e69cb8ecfa1f382f38a3cb`.

Counter evidence (run this seat, before and after the other seat's repair):

```
before: DEFECT R8 entry-licence-adjective: the entry names a CC0 licence no registry row records
        checks=10 defects=10   exit=1
after : checks=10 defects=6    exit=1   (R8 absent; remaining R1 R2 R3 R6 R9 R10 are other seats' items)
```

Residual risk, stated so R8's green is not over-read: `check_r8` (`plans/round31_defects.py:196-203`) is
lexical — it returns clean whenever the entry contains no `CC0`, without checking that the replacement text
is grounded. A future edit could pass R8 by writing a different unrecorded licence (or by deleting the
bullet). Green on R8 means "no CC0 string", **not** "licence grounded"; the grounding evidence is §(a)–(b)
of this report, not the counter.

## Tooling / disk

No installs or upgrades this seat (pacman untouched per the host-wide pause). Scratch: `/tmp/r31-R31DefR8/`,
two files, 58,827 bytes total (`arxiv-2608.29463.html` 44,646 B; `disclosure-v1.1.md` 14,181 B). Nothing
written outside this report path.

## VERDICT

VERDICT: R8 CONFIRMED AND CLOSED — no registry row supports "CC0" for any card design (88 rows, zero CC0; the sole licence claim is S081's CC BY 4.0, re-verified at abs line 124, sha256 4c81bd3c…), the released card's recorded licence is CC BY 4.0 (staged S132; pinned `DISCLOSURE.md:3` sha256 80363c61…), and the applied repair — dropping the adjective — is the minimal honest fix; residual: `check_r8` is lexical, so its green proves only the absence of the string, not a grounded licence.
