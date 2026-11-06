# CriticClaims — round 100 (R100-C1 coverage, R100-C2 freshness)

Seat: critic (leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; BASE `78460376`;
F `54df15ca1f9b689b25c6ffc3b2fccd1253bdd6c2`; T `dbe0cefa607cf57f7f58346fce64bcc127144ca0`;
receipts `d8ed39bd`. Method: one `git clone --shared` detached at T under
`/fast/scratch/hyaku/kengaku-r100/CriticClaims/`, an own `uv venv -p 3.13` with pytest 8.4.1 /
pandas 2.3.2 / pytest-json-ctrf 0.3.5, every command run from the clone root with `TMPDIR` set to
the scratch. No production edit, no commit in the lane, no task call. All receipts under
`.ufo/waves/round-100/w1/CriticClaims/`; the fixture commits named below are children of T in the
ephemeral clone and their patches are saved (`fixture-*.patch`).

## Independent reproduction (my runs, not the lane's receipts)

| check | result | receipt |
|---|---|---|
| C1 at T | `LEGS L1..L13=pass`; `TARGET executed_rows=44 member=financial-document-processor cells=crypto-credential:5,file-artifact:35 set_equals_base_plus_member=1 located=1 executed=1 cases=15 legs=120 mismatches=0 new_rows=8 new_rows_flagged=0 new_rows_line_live=0 changed_outside_table=0 defects=0`; `PREDICATE R100-C1 pass`, rc 0 | `CriticClaims/c1-at-T.txt` |
| C2 at T | `REF 5220b71d…`; `GATE defects base=33 ref=32 rev=23`; `LEGS K1..K10=pass`; `TARGET pop=9 cleared=9 still=0 outside_rows=324 outside_removed=0 outside_added=0 outside_rebound=0 base_rows=333 base_rows_not_equal=0 new_provenance_files=3 url_channel_files=0 not_three_cells=0 ids_not_in_pop=0 live_rows=9 rows_changed=0 captures_changed=0`; `PREDICATE R100-C2 pass`, rc 0 | `CriticClaims/c2-at-T.txt` |
| probe at T | 49 lines; the committed receipt and this run differ on **one line only** (`LANE_TIP`) | `CriticClaims/probe-at-T.txt`, `receipt-diff.txt` |
| digest gate at T | `rows=341 tokens=225 defects=23` | `CriticClaims/gates-at-T.txt` |
| line gate at T | `live=0 cited=147 captured=134 uncaptured=13 defective=10 repaired=10` | `CriticClaims/gates-at-T.txt` |
| pre-freeze check BASE→T | `PREFREEZE new=0 gone=0 … VERDICT clean` | `CriticClaims/gates-at-T.txt` |
| census at T | rc 0, 32 `W04` (31 at BASE; the new one is S342's cross-scope duplicate URL — disclosed in the lesson and LOG) | `CriticClaims/gates-at-T.txt` |
| freeze integrity | 16/16 `frozen-instruments` hash at F **and** T; 6/6 `candidate-bytes` hash at T; `git diff --name-status F T` = the 6 candidate files + the receipt | `CriticClaims/freeze-integrity.txt` |
| historical frozen union | 76 claims files at T, 8 with a `frozen-instruments` block, 99 rows, **0 differ at T** | `CriticClaims/frozen-union.txt` |
| live re-fetch (independent) | 9/9 pinned URLs HTTP 200, sha256 **and** byte count exactly the POP token/size | `CriticClaims/live-refetch-independent.txt` |
| S295 across revisions | BASE: `DEFECT S295 … capture-unanchored`; REF and T: `BIND S295 … by=url-task`, no DEFECT | `CriticClaims/s295-across-revs.txt` |

Both frozen predicates reproduce exactly at T. The findings below are about what the predicates
*bind*, not about whether they pass.

## Findings

### F1 — L3 + L6 do not bind receipt identity (severity: **medium**; claim wording / false-provenance risk)

**Counterexample.** Run `plans/round100_fdp_probe.py` at T. Its output differs from the committed
`corpus/evidence/round100/fdp-probe.txt` on exactly one line: `LANE_TIP dbe0cefa…` instead of
`LANE_TIP 54df15ca…` (`receipt-diff.txt`). Replace that one line with F and the file becomes
**byte-identical to the committed blob** — `git add -A` in the clone reports "nothing to commit".
So the committed receipt is equally consistent with a run at T and with a run at F. L3 compares a
self-reported field (`probe:410` prints `git -C lane rev-parse HEAD`) to F; L6 compares the
observation block plus `TOOL_SHA`/`CASE_TABLE_SHA`/`GRADER_SIDE`, all invariant F→T (`RERUN_STAMPS`
excludes `LANE_TIP`; the L6 rerun runs from a `git archive`, where `LANE_TIP` is `absent`). A
receipt produced at T with `LANE_TIP` edited to F passes all 13 legs.

**Evidence.** `probe-at-T.txt` (my run at T), `receipt-diff.txt` (one-line diff),
`receipt-identity-proof.txt` (the edited T-run receipt's blob hash equals the committed blob's,
`ce1ebeea…`), `fixture-t-run-receipt.patch` / `c1-t-run-receipt.txt` (the T-run receipt left at
`LANE_TIP=T` fails **L3 only**), `.ufo/waves/round-100/L1/controls/c1-receipt-identity-run1.txt`
(the P2 control rewrites `LANE_TIP` to BASE — a *wrong* value — which L3 catches). The round's own
lesson lists L3 as a mutation survivor (`corpus/lessons/round-100.md`, "Mutation survivors: C1 L3
(run identity = F)"). The P2 battery has no control for a T-run receipt whose field is set to F.

**Impacted axes.** coverage (the replay's "located" identity), calibration (the claim says "run
identity"; the leg checks a claim).

**Smallest safe correction.** Reword the claim and L3's docstring to "the receipt's self-reported
`LANE_TIP` equals F". Route to round 101 a real binding: commit the receipt at F (then ancestry
binds it, but the frozen clause "C lands … the receipt" must change) or have the probe emit a tree
hash of the lane at run time and compare it to F's tree — still self-reported, but at least the
tree, not just a commit id.

### F2 — C2's standalone predicate does not bind the candidate files it does not own (severity: **medium-low**; separability gap)

**Counterexample A.** At T + one appended SOURCES row (`S999`, a copy of an existing row shape),
`round100_c2_rowcensus_bind.py` prints `LEGS K1..K10=pass` and `PREDICATE R100-C2 pass`; the C1
counter at the same revision fails `L10 (new_rows=9)` and `L12 (SOURCES sha)`. K8 checks only that
BASE rows survive (deletions/rewrites), not that no row was added; K10's `outside_table` checks
*paths* (SOURCES.md is in `candidate-bytes`), and `own_bad` checks shas only for `new_prov`.

**Counterexample B.** At T + SKILL.md `crypto-credential` cell `5 → 4`, C2 prints `K1..K10=pass`;
C1 fails `L12 (SKILL.md)`. Same code path: K10 never compares `candidates[p]` to the blob at rev for
SKILL.md, the ledger or SOURCES.md.

**Evidence.** `fixture-added-row.patch` + `c2-added-row.txt` (C2 pass) + `c1-added-row.txt` (C1
fail); `fixture-skill-cell.patch` + `c2-skill-cell.txt` (C2 pass) + `c1-skill-cell.txt` (C1 fail);
`.ufo/waves/round-100/L1/controls/c2-outside-row-delete-run1.txt` (the P2 control kills deletion,
K8 only). The claim's clause "no
gate byte, SOURCES row, capture or existing provenance file changes" is therefore enforced at the
joint measurement by C1's L10/L12, not by C2's predicate. "C2 is verifiable without C1" is true for
C2's *change*, not for C2's *clause*.

**Impacted axes.** freshness (C2's own clause), coverage (the joint measurement is sound at T).

**Smallest safe correction.** In K10, require `candidates[p] == sha(blob(rev, p))` for **every**
changed path in `candidates`, not only `new_prov`; route to round 101.

### F3 — the live re-fetch receipt is repo-derivable; K9 is a consistency check, not a liveness proof (severity: **medium** for the freshness evidence; the claim itself is true)

**Counterexample.** Every field K9 checks in `.ufo/waves/round-100/L1/c2-live-refetch.txt` is
derivable from committed bytes: the nine `bytes=` values equal the committed capture sizes exactly
(2600, 11386, 5878, 3177, 2166, 3034, 2330, 1262, 24841), the `sha256=` values are the POP tokens,
and the `url=` values are the POP urls. A pre-freeze fabricated receipt with those nine lines would
pass K9; no network is needed to produce it. So `live_rows=9` does not establish that any fetch
happened — it establishes that a pinned receipt says so.

**Evidence.** `live-refetch-derivable.txt` (the byte-count table), `c2-at-T.txt` (K9 pass).
Independent check, which is what makes the claim true: I re-fetched all nine URLs at review time —
HTTP 200, exact sha256 and byte counts (`live-refetch-independent.txt`).

**Impacted axes.** freshness (the axis's evidence).

**Smallest safe correction.** Say in the claim that K9 binds a receipt, not a fetch, and record the
independent re-fetch as the freshness evidence. A live-check gate (fetch + hash at measurement time)
is a round-101 candidate; it cannot be part of an offline T.

### F4 — C2's `freshness` label is defensible this round, but the TARGET's delta is provenance (severity: **low**)

`AXES.md:14` defines freshness as "Drift detection — skill claims re-verified against live surfaces;
stale items flagged or fixed". Round-99 CriticClaims F10 said C2 re-verified nothing live; round 100
adds the nine-URL re-fetch, so the label is satisfied this round. But the TARGET's discriminating
numbers (`cleared=9`, `new_provenance_files=3`) are the gate blind-spot repair; the freshness act is
the pre-freeze receipt, not measured at T. The claim says "held at ceiling 10" — held, not moved, so
there is no score overclaim. The lesson and LOG should separate "freshness: 9/9 live
re-verifications" from "provenance: 9 findings cleared".

**Impacted axes.** freshness.

**Smallest safe correction.** Split the headline as above; no predicate change.

### F5 — Q86 member choice and tie-break: defensible (severity: **info**)

The ledger at BASE has the three-way 0.333 tie the claim states (`crypto-credential` 4/12,
`shell-exec` 2/6, `subprocess-exec` 15/45). CO-7 says the tie is under-determined; CO-9 and
`.ufo/waves/round-99/w1/ConnectorOverlap/cost_table_T.txt` name the exact blockers for the four
`shell-exec` members (`git-multibranch` nginx+sshd+git; `qemu-startup` QEMU+Alpine+telnet+expect;
`model-extraction-relu-logits` candidate library; `overfull-hbox` apt texlive at test time) and price
fdp at +0.083 for a 4.03 MB tree with pandas 2.3.2 already staged in round 99's venv. fdp's class
membership comes from the frozen class survey (`crypto-credential` detector =
`hashlib|sha1|sha256|md5|openssl|gpg|hmac`; fdp's grader uses `hashlib.file_digest(…, "sha512")`).
Two imprecisions, neither load-bearing: (a) the lift leaves the *minimum* class fraction at 0.333
(`shell-exec`/`subprocess-exec`) — the lesson says this, the claims file's "min_class" sentence could
be read as if the min moved; (b) the SKILL cell's prose ("credential and certificate artefacts …
openssl calls") describes the certificate members, not fdp's invoice hashing — a prose gap in a
regex-literal class, not a class error.

**Impacted axes.** coverage.

### F6 — C1/C2 separability: predicate-level yes, instrument-level no, disclosed (severity: **low**)

C1's P0 capture re-binds S295 by `url-task` and clears its `capture-unanchored` finding (33→32); I
reproduced it: at BASE S295 carries the DEFECT, at REF and T it binds to the round100 capture and the
DEFECT is gone (`s295-across-revs.txt`). C2's censuses start at REF = F~1, which already holds the
P0 capture, so C2's TARGET does not blame C1 for S295. The claim discloses this (amendment 1,
`GATE defects base=33 ref=32 rev=23`). The P2 controls confirm the matrix: c1only passes C1 and
fails C2 (`still=9`); c2only passes C2 and fails C1. Residual: the round's 33→23 gate delta is 9 C2
+ 1 C1-P0; the claim says "9 findings cleared (32 → 23 from REF)" — honest.

**Impacted axes.** coverage, freshness.

### F7 — no frozen-clause violation in the landed commits (severity: **none**)

`git diff --name-status F T` is exactly the six `candidate-bytes` files plus
`corpus/evidence/round100/fdp-probe.txt`; 16/16 frozen-instrument hashes match at F and T; 6/6
candidate hashes match at T; the pre-freeze check is `VERDICT clean` (new=0); 76 claims files / 99
historical frozen rows, 0 differ at T; the P0 predictions file's 15 vectors equal the frozen table's
15; the ledger diff BASE→T is exactly the fdp member flip; the wave is 12 seats (4 attack = 33 %,
1 connector) with no `model` key, dispatched after T; the integration commit adds docs and evidence
only. No clause violation found.

**Impacted axes.** all.

### F8 — no do-nothing or cheaper control reaches either TARGET (severity: **none** for the TARGETs; the freshness receipt caveat is F3)

C1: the BASE receipt fails 12/13 legs; the P2 battery kills do-nothing, c2only, extra-member,
forged-receipt, receipt-identity, counter-edit, extra-file, skill-cell, extra-row and typed-words;
positive and both pass. The TARGET requires the probe (L6 rerun), the 15-case table (L5), the ledger
flip (L7), the eight rows (L10) and the file set (L12). C2: the BASE receipt fails 6/10 legs; the P2
battery kills do-nothing, c1only, partial, url-channel, duplicate-line, sha-column, fabricated-id,
fourth-cell, outside-rebind, outside-row-delete, row-edit, gate-edit, capture-edit, c2counter-edit,
live-forged and c2-extra-file; positive and both pass. The TARGET requires the nine provenance lines
(K4/K5) and the three files (K3/K10). The only cheaper paths I found are F2 (a corrupted non-owned
candidate file passes C2) and F3 (a fabricated live receipt passes K9).

## Verdict list

- F1 LIMITATION — a probe run at T differs from the committed receipt only in `LANE_TIP`, and the one-line edit makes it byte-identical, so L3+L6 cannot distinguish a run at F from a run at T — `.ufo/waves/round-100/w1/CriticClaims/receipt-diff.txt`
- F2 GAP — C2 prints `K1..K10=pass` on T plus an added SOURCES row and on T plus a corrupted SKILL cell, while C1 fails L10/L12 there, so C2's "no SOURCES row changes" clause is enforced only by C1 — `.ufo/waves/round-100/w1/CriticClaims/c2-added-row.txt`
- F3 LIMITATION — every K9-checked field of the live receipt (byte counts, sha256, urls) is derivable from committed bytes, so `live_rows=9` is a receipt check, not a liveness proof; my independent 9/9 re-fetch is what makes the claim true — `.ufo/waves/round-100/w1/CriticClaims/live-refetch-derivable.txt`
- F4 PASS-WITH-CAVEAT — the `freshness` label is defensible this round because the live re-fetch answers round-99 F10, but the TARGET's delta (`cleared=9`) is the provenance binding, not the freshness act — `.ufo/waves/round-100/w1/CriticClaims/c2-at-T.txt`
- F5 PASS — the Q86 tie-break is supported by CO-7/CO-9 and the cost table (exact blockers for the four shell-exec members; fdp +0.083 with pandas already staged), with the min still 0.333 after the lift — `.ufo/waves/round-99/w1/ConnectorOverlap/cost_table_T.txt`
- F6 PASS-WITH-CAVEAT — C1's P0 capture clears S295's `capture-unanchored` finding (33→32) and C2's REF = F~1 absorbs it, so the predicates are separable and the instrument coupling is disclosed — `.ufo/waves/round-100/w1/CriticClaims/s295-across-revs.txt`
- F7 PASS — `git diff F T` is exactly the six candidate files plus the receipt, 16/16 frozen instruments and 6/6 candidates hash, the pre-freeze check is clean, and 99 historical frozen rows are unchanged — `.ufo/waves/round-100/w1/CriticClaims/freeze-integrity.txt`
- F8 PASS — both TARGETs reproduce at T and no do-nothing or cheaper control reaches either, except the F2/F3 paths above — `.ufo/waves/round-100/w1/CriticClaims/c1-at-T.txt`

## What I did not test

- I did not run the P2 control battery itself (the lane's 32 controls x2 are receipts; I read the
  README table and spot-checked ten receipts, and ran my own three forgery fixtures).
- I did not re-run the maintainer OCR solution; I verified its committed output equals C01's summary
  sha (`08724ad9…`) and that the fixture pins hash.
- I did not test the host's `bwrap`/user-namespace limits beyond the probe's own setup checks.
