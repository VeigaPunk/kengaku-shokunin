# ConnectorOverlap — round 99 (w1)

Seat: cross-lane / cross-claim scan + round-100 planning data-walk. No production edits, no commits in the
lane. Every measurement below is in a `git clone --shared` detached at T `f72a8bc7` (scratch
`/fast/scratch/hyaku/kengaku-r99/ConnectorOverlap`, removed at exit); receipts in
`.ufo/waves/round-99/w1/ConnectorOverlap/`.

## (a) Cross-lane and cross-claim scan

**No sibling lane replays `bn-fit-modify` — or any TB2 grader.** `grep -rl 'bn-fit-modify'` over
`/home/vgpnk/Projects/shokunin` returns zero hits outside `kengaku-shokunin/`. `grep -rl 'terminal-bench'`
over tracked `*.md|*.json|*.py` (excluding `.git/` and `.ufo/`) returns only fleet `MANIFEST.json` — whose
matches are kengaku's own r96–r98 replay entries (lines 53068, 53112, 53283) — and kengaku itself. Six
sampled lanes (chousa, kotoba, kagi, kaidoku, tameshi, kasegi) carry **0** tracked TB2 references.

**No sibling lane uses row-scoped provenance.** The only non-kengaku `PROVENANCE.md` consumer is
`game-dev-3d-shokunin/reports/round-107/mutations/adv1-patch-A.py`, which greps a *pinned-commit* table
(`| pinned commit |`) out of a vendored tree's PROVENANCE.md — a different convention (pin declaration, not
row→file→sha256). R99-C2's three-column form has no cross-lane precedent to collide with and no sibling
borrower.

**The C1 byte table holds at T.** `git diff --name-status F..T` is exactly the 11 `candidate-bytes` paths
plus `corpus/evidence/round99/bnfit-probe.txt` — 12 files, no extras, none missing. All 11 blobs hash to
their table sha256 at T; all 18 `frozen-instruments` paths hash to their table sha256 at T. Ledger
arithmetic re-derived independently at BASE/F/T: 88 members; executed 42 → 42 → **43**; file-artifact
33/76 → 33/76 → **34/76**. The claim's `42->43` and `file-artifact 33->34 of 76` are exact.

## (b) Do C1 and C2 touch disjoint bytes? — yes, measured

Write sets from the diff: **C1** = `SKILL.md`, `corpus/SOURCES.md`, `plans/grader-population-ledger.json`
(+ the receipt); **C2** = the eight `corpus/evidence/round<N>/PROVENANCE.md`. Intersection empty; no file is
modified by both. Read sets overlap only on read-only instruments (`corpus/SOURCES.md`,
`plans/anchor_digest_check.py`, `plans/round-99-claims.md`, `gate-base.py`).

Separability measured in the clone (three scratch commits, then reset to T):

| tree state | gate defects | note |
|---|---|---|
| T | 33 | frozen target |
| T − 8 C2 PROVENANCE files (C1 bytes intact) | **45** | 0 defects on C1's S334–S341; 12 on C2's population rows |
| T + 9 provenance lines (experiment) | 24 | S210 S211 S219 S228 S232 S279 S281 S298 S300(01550b7d) cleared |
| T + 9 lines + S295 token (experiment) | 23 | S295 `capture-unanchored` cleared |

So C1's L10 (`new_rows_flagged=0`) is **invariant to C2's bytes**, and C2's 12 cleared rows are exactly the
45→33 delta — no interaction term. C2's counter at T prints `PREDICATE R99-C2 pass` with
`outside_rows=313 outside_removed=0 outside_added=0 outside_rebound=0` even though C1 rewrote the same
`SOURCES.md` C2 reads: K7's outside population is BASE-derived, so C1's eight added rows cannot enter it.
The shared input is inert in both directions — measured, not assumed.

## (c) Round-100 planning data-walk

### c.1 Class arithmetic at T (`plans/grader-population-ledger.json`, 88 members, executed 43)

| class | exec/total | frac | remaining | lift/member |
|---|---|---|---|---|
| crypto-credential | 4/12 | 0.333 | 8 | **0.083** |
| shell-exec | 2/6 | 0.333 | 4 | **0.167** |
| subprocess-exec | 15/45 | 0.333 | 30 | **0.022** |
| filesystem-metadata | 4/10 | 0.400 | 6 | 0.100 |
| numeric-band | 4/10 | 0.400 | 6 | 0.100 |
| timing-wall | 4/9 | 0.444 | 5 | 0.111 |
| file-artifact | 34/76 | 0.447 | 42 | 0.013 |
| stdout-inspection | 13/29 | 0.448 | 16 | 0.034 |
| candidate-import | 3/6 | 0.500 | 3 | 0.167 |
| db-state | 1/2 | 0.500 | 1 | 0.500 |
| network-service | 4/8 | 0.500 | 4 | 0.125 |
| git-plumbing | 2/3 | 0.667 | 1 | 0.333 |
| process-environment | 2/3 | 0.667 | 1 | 0.333 |
| serialization-schema | 8/10 | 0.800 | 2 | 0.100 |
| signal-delivery | 1/1 | 1.000 | 0 | — |

`min_class` = **0.333, a three-way tie**: crypto-credential 4/12, shell-exec 2/6, subprocess-exec 15/45. The
tie is not cosmetic — marginal lift per member differs 7.6× across the tied classes (0.167 / 0.083 / 0.022).
The proposal's example text names crypto-credential as "thinnest"; that is one of three, and it is not the
largest-lift one.

### c.2 The five cheapest unexecuted members whose classes include a thinnest class

Cost rubric: **T** toolchain install weight, **F** fixture bytes at the pin, **S** positive control
(maintainer `solve.sh` size), **N** test functions. Bytes are the pinned tree at `2fd12b88`
(`corpus/evidence/round53/pin-tree-2fd12b88.json`); `bn-fit-modify`'s own tree is **15,420 B** for scale.

| # | member | classes | tree B (env) | tests | cost drivers |
|---|---|---|---|---|---|
| 1 | `cobol-modernization` | file-artifact, subprocess-exec | 19,266 (6,387) | 3 | python only; grader overwrites `/app/data/*.DAT` + `/app/src/INPUT.DAT` itself (they must exist first — 6.4 KB env); `solve.sh` 4,555 B |
| 2 | `extract-elf` | file-artifact, serialization-schema, subprocess-exec | 26,558 (428) | 2 | gcc + node already on host; grader writes `/app/new.c` itself and compiles it; `solve.sh` 9,479 B |
| 3 | `adaptive-rejection-sampler` | file-artifact, numeric-band, stdout-inspection, subprocess-exec | 37,849 (5,812) | 9 | R already staged (`/fast/scratch/kengaku-r99/renv/bin/Rscript`); grader writes its own test script; venv pins numpy 2.3.3 / scipy 1.16.2 (a second venv beside round 99's numpy 2.5.4); `solve.sh` 15,365 B |
| 4 | `dna-insert` | file-artifact, numeric-band, stdout-inspection, subprocess-exec | 17,443 (7,462) | 1 | `primer3`/`oligotm` via conda-forge (small); sequences embedded in the grader; `solve.sh` 1,358 B |
| 5 | `dna-assembly` | file-artifact, numeric-band, stdout-inspection, subprocess-exec | 31,070 (7,936) | 1 | same `primer3` toolchain; sequences embedded; `solve.sh` 3,540 B |

All five above sit in `subprocess-exec` (the 45-member class): **+0.022 each**.

Runner-up, and the counter-example to byte-based pricing: `prove-plus-comm` has the **smallest tree**
(5,900 B) but needs `coqc` (a large Coq install); `gpt2-codegolf` has a 9,301 B tree but fetches a ~500 MB
checkpoint at build (not in the tree — its env is 416 B) [INFERENCE on the checkpoint size]. Tree bytes
alone misprice both.

### c.3 The frontier this exposes

The five cheapest eligible members buy +0.022 on the axis. The cheapest member that buys **+0.083**
(crypto-credential) is `financial-document-processor`: 4,031,474 B tree of which 4,004,665 B is the 17
sha512-pinned documents, `pandas==2.3.2` is already the round-99 grader pin, `solve.sh` 11,635 B. The other
cheap crypto-credential member is `winning-avg-corewars` (23,779 B tree, `pmars` built from source, 8,332 B
of warriors, `solve.sh` 7,042 B). `shell-exec`'s +0.167 is **locked**: its four remaining members are
`git-multibranch` (nginx + sshd + git over localhost), `overfull-hbox` (its fixture runs
`apt install texlive` at test time), `qemu-startup` (QEMU + Alpine + telnet), `model-extraction-relu-logits`
(ledger reason `candidate-library-required`).

### c.4 Remaining anchor-digest findings at T, grouped, with the cheapest successor path

33 findings on 29 rows. Grouped by row kind × defect class (`findings_by_class_T.txt`):

| group | n | rows | cheapest successor path |
|---|---|---|---|
| code / digest-wrong-capture | 8 | S210 S211 S219 S228 S232 S279 S281 S298 | **measured**: one three-column provenance line each (the token *is* a committed file's sha256); 33→24, zero network |
| code / anchor-unbound | 5 | S233×2, S240, S300×2 | S300 `01550b7d` = provenance line (measured); S300 `fa53d657` = replace the 8-hex abbreviation with the full 64-hex of the committed `environment/main.rs`; S240 = fetch `urllib3/connection.py` @2.7.0 (one small source file) + capture; S233×2 = the 2,990,966 B amalgamation zip and its page were never committed (only the unzip listing, whose digest is not the token) → commit the zip **or** retract 2 tokens |
| docs / anchor-unbound | 7 | S178 S184 S185 S193 S202 S231 S242 | fetch + capture, all small text (README, PR body, news page, leaderboard, 2 `instruction.md`, gRPC docs) then one provenance line each; S178's token is 20 hex and must be re-derived whole |
| paper / anchor-unbound | 4 | S187 S188 S189 S190 | retract the digest (arXiv id + section is the citation; PDFs are large next to text captures) — a policy call, not a byte cost |
| code / token-outside-anchor | 2 | S213 `be`, S300 `3a905a56` | cell edits, zero network: S213's 2-hex fragment sits in the teaches cell; S300's is an 8-hex abbreviation of a committed digest |
| community / anchor-unbound | 2 | S191 S192 | tier C rows: retract the token (community is never tier A) |
| dataset / anchor-unbound | 2 | S179 S186 | S179's raw tree document is 372,898 B and fetchable (the committed round53 pin-tree is a 139,342 B filtered form, digest `96b47248…`, not the token); S186's card is small; fetch + capture |
| spec / anchor-unbound | 1 | S229 | fetch PEP 503 text (~30 KB) + capture |
| code / digest-unknown | 1 | S236 | same amalgamation digest as S233: commit the zip or retract |
| code / capture-unanchored | 1 | S295 | **measured**: one anchor token (the pin-tree capture's own sha256 `96b47248…`); 24→23 |

Cheapest-first for round 100: **10 findings for zero network bytes** (9 provenance lines + 1 anchor token,
measured), then 3 cell edits, then the small fetches (7 docs + spec + S240 + 2 dataset), then the 3 MB
amalgamation decision, then the paper/community retractions.

## Evidence, affected axes, proposed move, risks, verification

**Affected axes.** Coverage (C1 member selection: which member a round buys) and freshness (the
anchor-digest backlog: 33 findings at T, 10 of them clearable from committed bytes alone).

**Proposed move (one, bounded, round 100, planning only — no repair in round).** The C1 pre-freeze check
prints `min_class` **and the tie set**, then ranks eligible members by *marginal class lift ÷ replay cost*,
with cost read from committed evidence (pin-tree bytes + a host tool probe), not prose. Under that rule the
round-100 pick is `financial-document-processor` (or `winning-avg-corewars`), not the cheapest
`subprocess-exec` member.

**Why it is non-obvious.** The proposal's own rule ("refuse a member whose every class is above
min_class") is satisfied by all five cheapest members and would leave the skew untouched: the thin classes
are thin *because* their remaining members are the environment-heavy ones. Cost-aware ranking is what turns
the min_class rule into actual lift — +0.083 for 4 MB versus +0.022 for 19 KB.

**Risks (second-order).**
1. *The provenance route is exclusive.* `bind_row` returns `provenance-row` bindings first and only, so a
   provenance line **replaces** the row's URL-derived capture set. That is what makes the 9 clears cheap —
   and it is also what lets a wrong row hide behind a line (the gate's documented "row is the only witness"
   limit). Extending the mechanism from 12 to 21 rows widens that hole by 75%; each line must be paired with
   the byte-identity check (K4's sha column) and the symmetric census (K7).
2. *Cheap ≠ honest for S298.* The row names `decomp-opt-divergence.txt` but carries `decomp.c`'s digest.
   Retargeting the row's anchor cell to the `decomp.c` capture is the honest fix; a provenance line is the
   cheap one. The two are not equivalent under the gate's binding limits.
3. *S295's fix edits the gate's own input* (`SOURCES.md`). A round that both edits rows and claims a defect
   drop must freeze the row bytes in its claims table the way C2 froze its population.
4. *min_class is a three-way tie at T.* A rule that prints one `min_class` without a tie-break silently
   picks the alphabetically first (crypto-credential) — which is what the proposal's example text does.
5. *Cost is author-supplied unless derived.* The pin-tree capture makes the byte half objective; the
   toolchain half (Coq vs primer3 vs a staged R) still needs a host probe recorded in the claim.

**Verification actually run** (receipts in `.ufo/waves/round-99/w1/ConnectorOverlap/`):
`gate_T.txt` (33 defects, rc 1), `gate_prov.txt` (24), `gate_prov2.txt` (23), `gate_noC2.txt` (45, 0 on
S334–S341), `c2_at_T.txt` (`PREDICATE R99-C2 pass`), `byte_table_T.txt` (diff set equality, 11+18 sha256
checks, ledger arithmetic at BASE/F/T, write-set intersection), `class_table_T.txt`, `cost_table_T.txt`,
`findings_by_class_T.txt`. **Not run by me:** the C1 replay and its venv (ExecC1-2 owns it), any gate other
than `anchor_digest_check.py`, the sources census.

## Verdict list

- **CO-1** cross-lane replay duplication — **none found**: no sibling lane replays `bn-fit-modify` or any TB2 grader (0 hits outside kengaku; fleet `MANIFEST.json` matches are kengaku's own r96–r98 entries) — `byte_table_T.txt`, fleet grep.
- **CO-2** cross-lane row-scoped provenance — **none found**: the only non-kengaku `PROVENANCE.md` consumer reads a pinned-commit table, a different convention — `game-dev-3d-shokunin/reports/round-107/mutations/adv1-patch-A.py`.
- **CO-3** C1 byte table at T — **holds**: diff F..T = 11 candidate-bytes + 1 receipt exactly; 11/11 and 18/18 sha256 match — `.ufo/waves/round-99/w1/ConnectorOverlap/byte_table_T.txt`.
- **CO-4** ledger arithmetic — **holds**: 88 members, executed 42→42→43, file-artifact 33/76→33/76→34/76 at BASE/F/T — same receipt.
- **CO-5** C1/C2 write disjointness — **disjoint**: C1 {SKILL.md, SOURCES.md, ledger} ∩ C2 {8 PROVENANCE.md} = ∅ — `gate_noC2.txt`.
- **CO-6** C1/C2 separability — **holds, measured**: C2 stripped → 45 defects with 0 on S334–S341; C2's 12 rows are exactly the 45→33 delta — `gate_noC2.txt`, `c2_at_T.txt`.
- **CO-7** min_class at T — **three-way tie at 0.333** (crypto-credential 4/12, shell-exec 2/6, subprocess-exec 15/45); the proposal's single-class reading is under-determined — `class_table_T.txt`.
- **CO-8** five cheapest eligible members — **cobol-modernization, extract-elf, adaptive-rejection-sampler, dna-insert, dna-assembly** (17–38 KB trees, 0–1 small installs); all buy only +0.022 — `cost_table_T.txt`.
- **CO-9** cheapest thin-class lift — **financial-document-processor** (+0.083 for a 4.03 MB tree, pandas already pinned) beats the five cheapest on lift per replay; shell-exec's +0.167 is locked behind network/VM/apt — `cost_table_T.txt`.
- **CO-10** anchor-digest backlog at T — **33 findings, 10 clearable from committed bytes with zero network** (9 provenance lines + 1 anchor token), measured 33→24→23 — `gate_prov.txt`, `gate_prov2.txt`, `findings_by_class_T.txt`.
- **CO-11** provenance route side channel — **risk confirmed by design**: `bind_row` returns provenance-row bindings exclusively and first, so the cheap clears trade gate independence for bytes; needs K4 byte-identity + K7 census per line — `plans/anchor_digest_check.py:313-321`.
