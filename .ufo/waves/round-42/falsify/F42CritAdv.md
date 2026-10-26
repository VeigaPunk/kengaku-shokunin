# F42CritAdv — adjudication of R42RevMutRows's two `adv` cells and the XO5/XO6 relabel (round 42, wave 2)

Seat: critic (leaf). Date 2026-10-26. Scope: the frozen C1 `MUTANTS` table in
`plans/round42_c1_verify.py` at `508434ad55c709337065611691c426f05875492d`, adjudicated against the
tool files at the same commit. Nothing frozen was edited; my drafts go to the L1.

## 1. What I attack

1. The two `adv` cells R42RevMutRows flagged as "misquoted" — X3 (cite `:57-58`) and X7 (cite
   `:92-93`): quote the cited lines verbatim at the pinned commit, and classify each cell as misquote /
   misattribute / paraphrase.
2. The XO5/XO6 relabel `rc-silence` → `rc-mirror`: is it right?
3. The `adv_kind` split (13 `direct`, 1 `indirect`): is `indirect` right for XO6, and wrong for any
   other row?
4. Draft the erratum sentence for `corpus/lessons/round-42.md` (integration by the L1).

## 2. Method and pinned evidence

- Clone per lane rule: `git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin lane`;
  `git -C lane checkout -q 508434ad55c709337065611691c426f05875492d`; `git rev-parse --show-toplevel`
  → `/fast/scratch/hyaku/kengaku-r42/F42CritAdv/lane`; HEAD = `508434ad…`.
  The two tool files at the pin, sha256 (computed in the clone): `sha256sum plans/anchor_digest_check.py plans/order_check.py`
  → `11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2` (anchor),
  `948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc` (order) — the freeze's `PINS` values.
  Plans stable between the pinned docs commit and the present lane tip: `git diff
  508434ad…HEAD -- plans/anchor_digest_check.py plans/order_check.py plans/round42_c1_verify.py` → empty.
- All byte/word checks below run read-only in the clone (no battery, no envelope needed — no run
  writes anything).

## 3. X3 — verbatim quote and cite check

Frozen cell (round42_c1_verify.py:151-152):

> `plans/anchor_digest_check.py:57-58 'A provenance URL (an evidence markdown naming the same <repo>/<subpath>) is consulted when the task.toml route finds nothing'`

Cited lines 57-58 verbatim (anchor_digest_check.py @ 508434a):

- 57: `     `configure-git-webserver/tests/test_outputs.py` binds`
- 58: `     `corpus/evidence/round37/tb2-git-webserver/test_outputs.py` and nothing else, while S108's`

The quoted sentence actually sits at lines 59-61:

- 59: `     `regex-log/tests/test_outputs.py` binds `corpus/evidence/round36/tb2-regex-log/test_outputs.py`. A`
- 60: `     provenance URL (an evidence markdown naming the same `<repo>/<subpath>`) is consulted when the`
- 61: `     `task.toml` route finds nothing, which covers captures that are not whole task directories.`

Word check (normalized: backticks/`**` stripped, whitespace collapsed): all 18/18 quote tokens are
present token-exact in lines 59-61 (`missing from 59-61: []`); the cited range 57-58 shares only the
token `nothing` (from line 58's unrelated sentence "and nothing else") — 1/18, no quoted sequence.
**Verdict: wording is verbatim; only the line citation is wrong → misattribute (location), two lines
early; not a misquote of wording, not a paraphrase.**

## 4. X7 — verbatim quote and cite check

Frozen cell (round42_c1_verify.py:161-162):

> `plans/anchor_digest_check.py:92-93 'a token that is no committed capture at all is digest-unknown'`

Cited lines 92-93 verbatim:

- 92: `    `digest-unknown`.`
- 93: *(blank)*

The quoted sentence actually sits at lines 91-92:

- 91: `    row carrying another row's real digest); a token that is no committed capture at all is`
- 92: `    `digest-unknown`.`

Word check: 10/11 tokens are present token-exact in lines 91-92 (`missing from 91-92: ['digest-unknown']`
— line 92 carries `digest-unknown.` with a trailing period, so the full-token match is the punctuation
edge; the substring `digest-unknown` is present verbatim). The cited range 92-93 contains 0/11 quote
tokens. **Verdict: wording is verbatim; only the line citation is wrong → misattribute (location), one
line late at its start; not a misquote of wording, not a paraphrase.**

## 5. Origin and materiality

- Both wrong cites are carried verbatim from round-40 `F40XMutAnchor.md` §5: line 115 (X3) writes
  `"A provenance URL ... is consulted when the `task.toml` route finds nothing" (:57-58)`; line 117
  (X7) writes `"a token that is no committed capture at all is `digest-unknown`" (:92-93)`. The round-42
  table copied them unchanged (R42RevMutRows §4 agrees).
- Materiality: display-only. The counter's `main()` unpacks each row as
  `(mid, tool, cls, direction, adv_kind, label, _witness, old, new)` and uses `label` only for the
  printed `MUTANT … -- {label[:90]}` echo (round42_c1_verify.py:589-641); the predicate and the
  `invalid` checks consume id/tool/class/direction/adv_kind/old/new and never parse the quoted text or
  its cited range (`:596-597`). Neither wrong cite can flip C1. They remain defects inside a frozen
  artifact (counter uneditable this round) → named limit + erratum, not an in-place fix.

## 6. XO5/XO6 relabel rc-silence → rc-mirror: right

- Counter definitions (round42_c1_verify.py:448-451): `rc-silence` = `expect=reject` ∧ ref rc 1 →
  mut rc 0; `rc-mirror` = `expect=accept` ∧ ref rc 0 → mut rc 1.
- Frozen witness-run (`claims/witness-run.txt`): XO5 `killed by=w-xo5-post-receipt-blob
  attributed=L117 hits=1`, XO6 `killed by=w-xo6-p10-pass-line attributed=L53 hits=1`; both fixtures run
  `expect=accept … observed_rc=0` (ref 0 → mut 1 = rc-mirror).
- Control `claims/control-c1-direction-mislabel.txt`: with the round-40 labels declared, both rows print
  `MUTANT XO5/XO6 order rc-silence SURVIVED exhibits=0>1,rc-mirror` and `PREDICATE C1 fail` — the
  counter itself detects the rc-mirror shape and refuses the rc-silence claim. With `rc-mirror`
  declared, both die. The relabel is correct, necessary, and already reflected in the lesson
  (`corpus/lessons/round-42.md` first Mistakes row) and in the freeze text (`plans/round-42-claims.md:39-40`).

## 7. `adv_kind`: `indirect` right for XO6, wrong for none other

Convention (round-41, as used in the report): `direct` = the quoted sentence itself states the broken
behaviour; `indirect` = it follows from the quoted sentence plus the code; `none` = nothing advertises it.

- **XO6 (indirect) — right.** The quoted line is an inline comment
  (`order_check.py:52`: `# a gate output line, with or without the C2 counter's `gate: ` echo prefix`),
  which describes the regex's *shape*, not its verdict vocabulary. Whether `P10 PASS` is such a line is
  not decidable from the sentence: the gate prints only `ok`/`DEFECT` (`plans/pkg_gate.py:301`
  `print(f"{name} {'ok' if ok else 'DEFECT'} {note}")`) — that fact lives in code, not in the quote.
  The mutant adds `PASS` to the alternation, so the miss is sentence+code → `indirect` is exactly right,
  and the freeze's disclosure of the one indirect cell is accurate.
- **All other 13 (direct) — verified one by one against the quoted sentence** (quote shortened, full
  text at the cited lines):
  - X1: "Provenance row — a committed markdown … whose table line carries this row's id" — mutant
    kills the binding → sentence states it.
  - X3: "A provenance URL … is consulted when the task.toml route finds nothing" — mutant disables it →
    direct.
  - X6: "a 64-hex token that is a committed capture but not this row's is digest-wrong-capture" —
    mutant removes the class → direct.
  - X7: "a token that is no committed capture at all is digest-unknown" — mutant swaps the class → direct.
  - X9: "A row that matches the census regex but does not have 11 cells is a row-malformed defect" —
    mutant only defects >11 → direct.
  - X12: "matched **exactly** against the name = "<org>/<task>" a committed task.toml gives" — the
    mutant drops the slash-less fallback; the sentence states matching is against whatever name the
    task.toml gives (the `<org>/<task>` is an illustrative shape, not a constraint), so rejecting a
    slash-less name contradicts it → direct (closest call; still direct).
  - X13: "`--evidence-ref head` (default) reads HEAD blobs, so an unpromoted capture never counts" —
    mutant defaults to index → direct.
  - X14: "no 64-hex token … may be outside A unless it is the cited wrong token … (erratum-digest-
    unresolved)" — mutant stops recognizing uppercase tokens as hex → direct.
  - X15: "at least one other token that is 64 lowercase hex and a digest **of the capture that row
    names**" — mutant relaxes to any allowed digest → direct.
  - XO1: "FAIL when the freeze commit (the first commit adding <claims>) already contains <receipt>" —
    clause skipped → direct.
  - XO3: "FAIL when <receipt> was committed before <claims> (pre-registration inverted …)" — clause
    skipped → direct.
  - XO5: "Every blob ever committed under claims_dir up to and including `upto`" — mutant scans beyond
    `upto` → direct.
  - XO7: "a probe receipt line (the probe's per-case verdict record)" — mutant misses `observed=timeout`
    verdicts, which are still per-case verdict records → direct.
- So `indirect` is right for XO6 and *not* wrong for any other row: no other cell needs code beyond the
  quoted sentence. The frozen `ADVERTISED direct=13 indirect=1 none=0` tally is correct.

Minor claim-prose note: `plans/round-42-claims.md:30-31` says "Every `adv` cell quotes the tool's
docstring" — XO6's quote is an inline comment (line 52), not the module docstring; XO1/XO3 quote
docstring lines. This is loose wording in the freeze, not a defect in any cell.

## 8. Erratum sentence (draft for `corpus/lessons/round-42.md`)

Single sentence, ready for the Mistakes table or the named-limits block (L1 integrates; no frozen file
edited by me):

> Erratum (round 42): the frozen C1 `MUTANTS` rows X3 and X7 quote `plans/anchor_digest_check.py`
> verbatim but cite the wrong lines — X3 cites `:57-58` where the sentence sits at `:59-61`, X7 cites
> `:92-93` where it sits at `:91-92` — both carried from `F40XMutAnchor.md` §5; display-only (the
> predicate never parses `adv`), so no admission impact; correct the cites when the counter is next
> editable.

Suggested table row form (class | evidence pointer | captured-by | fix):

> **Two frozen C1 `adv` cells carry wrong line citations (wording verbatim)** — X3 cites
> `anchor_digest_check.py:57-58` for a sentence at `:59-61`; X7 cites `:92-93` for a sentence at
> `:91-92` | `.ufo/waves/round-42/build/R42RevMutRows.md` §4; verified at `508434ad…` (X3: 18/18
> tokens at 59-61, 1/18 at cited range; X7: 10/11 at 91-92, 0/11 at cited range) | `R42RevMutRows`
> (wave 1) | display-only (`adv` echoed as `label[:90]`, never parsed); erratum in this file; fix cites
> in round-43 counter.

## 9. Receipts

No receipt files were produced; all evidence is quoted above with locations. Scratch
`/fast/scratch/hyaku/kengaku-r42/F42CritAdv` (clone at 508434a) is removed on exit by the trap; only
the report dir below was written.

VERDICT: adv-errata-2
