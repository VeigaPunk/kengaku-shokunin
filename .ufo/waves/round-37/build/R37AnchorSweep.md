# R37AnchorSweep — anchor digest check (kengaku round 37, wave 1, executor)

Fixes the round-36 non-author spot-check routed item 1: `corpus/SOURCES.md` S110's anchor digest lost one
hex digit (`corpus/lessons/round-36-verifier-spotcheck.md` §5 item 1), and nothing in the lane compared a
row's digest with the capture manifest, so no counter could see it. Deliverables (all under
`.ufo/waves/round-37/build/R37AnchorSweep/`, nothing in the lane touched):

| file | sha256 | what |
|---|---|---|
| `anchor_digest_check.py` | `6d7afcd56a95c59f835be04a16263d43db4840cc8a4b111350be4d7cb8d9a323` | the check; draft for `plans/anchor_digest_check.py` |
| `fixture_matrix.py` | `88c751fec3870a20fe42dc7d31af3dc4a03afd2b19d0d58548cb26db8b01c973` | the falsifier harness (11 cases) |
| `fixture-receipt.txt` | — | full matrix receipt (case lines + every checker line) |
| `lane-run.txt`, `lane-run-verbose.txt` | — | the check on the lane at `44b7298` |
| `captures/` | manifest `cee207368b98889c81f1aeafd9066512ed37b8149939e314eb0a8cdd1f8dd036` | draft captures + `SHA256SUMS` (see §3) |

## 1. Contract

`python3 plans/anchor_digest_check.py --lane DIR [--evidence-ref head|index] [--verbose]`
→ exit 0 clean, 1 defects, 2 usage (bad args / no lane / no `corpus/SOURCES.md` / no git / any internal
error — a check that cannot run is never a pass). Stdlib only, writes no file, no temp file, git
subprocesses inherit `TMPDIR`. Output is one
`DEFECT <Sid> anchor token=<hex> class=<class> detail=<why> loc=corpus/SOURCES.md:<line>` line per defect
(or `loc=corpus/lessons/<f>:<line>` for erratum defects) and exactly one
`rows=<n> tokens=<n> defects=<n>`; `--verbose` adds `EVIDENCE|RESOLVED|ABBREV|EXEMPT|ERRATUM` lines before
them.

Rules, as implemented (docstring carries the full statement):

- rows are the **census shape** `^ {0,3}\|\s*(S\d{3,})\s*\|`, cells split after stripping outer pipes, 11
  cells expected, **anchor = cell 6**; a census-shaped row with ≠11 cells is `row-malformed`.
- a **token** is `sha256` + whitespace + hex, optional backticks, optional trailing `…`/`...`. S070 writes
  ``sha256 `45dd…` `` and S036 writes `sha256 afaae9dd…`; both are claims and both are scanned.
- a token **outside the anchor cell** is `token-outside-anchor`, always — otherwise "paste the bad digest
  somewhere else in the row" would pass.
- an **abbreviated** anchor token (trailing ellipsis) must be 8-63 lowercase hex and a **prefix of a member
  of A** (`abbrev-unresolved` otherwise) — an abbreviation is resolvable or it is a defect, never a free
  pass. S036's `afaae9dd…` resolves to `corpus/evidence/attrib-r23-stream.log`.
- every other anchor token must be **exactly 64 lowercase hex** (`digest-short`, `digest-long`,
  `digest-uppercase`) and a member of **A** (`digest-unknown`).
- **A** = sha256 of every blob under `corpus/evidence/` + every 64-hex digest listed by a `SHA256SUMS*`
  there. Evidence is read from git blobs (`HEAD:` / `:`), never from uncommitted working-tree bytes.
- **erratum exemption**: a line beginning `Erratum (round 37): S<id> anchor sha256` in a committed
  `corpus/lessons/*.md` exempts that row's anchor token from every anchor class when it carries the row's
  exact wrong token *and* ≥1 other token that is 64 lowercase hex in A. The erratum line is itself checked
  (`erratum-digest-unresolved`, `erratum-incomplete`). An erratum whose row has since been repaired stays
  valid — errata are append-only (`corpus/QUALITY.md` Q6), so there is no stale-erratum class.

## 2. Before → after

Before, on the lane at `44b7298` (fresh clone in the fixture run F0 and in place, identical output):

```
$ python3 .ufo/waves/round-37/build/R37AnchorSweep/anchor_digest_check.py --lane .
DEFECT S070 anchor token=45ddba7b…21cd class=digest-unknown detail=not-committed-evidence-and-not-in-a-SHA256SUMS loc=corpus/SOURCES.md:92
DEFECT S072 anchor token=081c8264…9287 class=digest-unknown … loc=corpus/SOURCES.md:94
DEFECT S073 anchor token=97b8671f…c7e2 class=digest-unknown … loc=corpus/SOURCES.md:95
DEFECT S074 anchor token=f996dfee…fe67 class=digest-unknown … loc=corpus/SOURCES.md:96
DEFECT S110 anchor token=4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c class=digest-short detail=63-hex loc=corpus/SOURCES.md:125
rows=103 tokens=11 defects=5      (exit 1)
```

`rows=103` equals the census row count (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
corpus/SOURCES.md` → 103); `tokens=11` counts S036, S070, S072, S073, S074, S105-S110 (S037's "sha256 in
the script" carries no hex and is not a token). `--verbose` shows 6 resolvable claims (S036 as a prefix,
S105-S109 via `round35|round36 …/SHA256SUMS`).

After, on a clone with the erratum (§4) **and** the captures (§3) staged — matrix case
`F2-erratum-plus-captures --evidence-ref index`:

```
rows=103 tokens=11 defects=0      (exit 0)
```

The erratum alone (case `F1-erratum-only`) clears S110 and leaves the four capture defects: `defects=4`,
`ids=S070,S072,S073,S074`. That is the honest intermediate — the frozen rule's escape hatch only covers a
*wrong* digest; a *true but uncaptured* one has to be captured. Both states are receipts, not prose.

## 3. What the four non-S110 flags are (new finding, not a false positive)

S070, S072, S073 and S074 state the sha256 of files they fetched at pinned commits in round 29. The claims
are **true** — I re-fetched all four at their own pins on 2026-10-26 and every digest equals the row:

```
45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd  838  generate_test_data.py  @ dce04686 (web-arena-x/webarena)
081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287  9717 README.md             @ dce04686
97b8671fc66518fbfed54467f9a64965bafa54d01702d922bfbb8b32c1b0c7e2  120  prepare.sh            @ dce04686
f996dfeef2bfb836fa79b20217cda36ecf428ed3965e3084e325626d7130fe67  8603 task.py               @ 4ccc7233 (ServiceNow/BrowserGym)
```

(command: `curl -sS --max-time 30` per pinned raw URL, then `sha256sum`). The defect they carry is that
**no committed byte under `corpus/evidence/` supports them**: nothing in the lane can re-check the claim,
which is the failure the lane already names ("a receipt is evidence only if something here re-runs it",
`corpus/lessons/round-36.md` §Mistakes). Byte-identical copies already exist in committed round-29 scratch
(`.ufo/waves/round-29/scratch/falsify/…`, and `plans/fixtures/r29/generate_test_data.py` for S070), so the
repair is a promotion, not a re-fetch.

Draft captures (`captures/`, staged in the fixture, for the L1 to land as
`corpus/evidence/round37/anchor-captures/`): `S070-generate_test_data.py`, `S072-README.md`,
`S073-prepare.sh`, `S074-task.py`, `PROVENANCE.md` (URL, commit, bytes, digest per row) and `SHA256SUMS`
(`sha256sum -c` → 5/5 OK). 19 KB total.

## 4. The erratum line (exact, tested verbatim)

Append to the errata block of `corpus/lessons/round-36.md` (where the S110 row and the round-36 erratum
precedent live; `corpus/lessons/round-37.md` works identically — the check scans every committed lesson):

```
Erratum (round 37): S110 anchor sha256 4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c is 63 hex digits (the `0` before `ea0f` was dropped in transcription); the capture's digest is sha256 4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c (corpus/evidence/round36/tb2-regex-log/SHA256SUMS, instruction.md).
```

It carries the wrong token (63 hex) and a 64-hex correction that is in `corpus/evidence/round36/tb2-regex-log/SHA256SUMS`.
The row itself is **not** edited (Q6: numbers are corrected by appended errata, never in place).

## 5. Falsifiers — 11 cases, all `ok`

`python3 fixture_matrix.py --lane <lane> --scratch <S> --captures <captures> --checker <check> --receipt
fixture-receipt.txt` (one `git clone -q --shared` per case, `--show-toplevel` asserted, index-only
`git add`, no commit, no mutating git command; matrix exit 0). Receipt: `fixture-receipt.txt`.

| case | defects | ids | classes | verdict |
|---|---|---|---|---|
| F0 lane as is (`head`) | 5 | S070,S072,S073,S074,S110 | digest-short, digest-unknown | ok |
| F1 erratum only (`head`) | 4 | S070,S072,S073,S074 | digest-unknown | ok |
| F2 erratum + captures (`index`) | 0 | — | — | ok |
| C7 captures staged, `head` mode | 4 | S070,S072,S073,S074 | digest-unknown | ok |
| **M1** erratum's correction → fabricated 64-hex | 3 | S110 | digest-short, erratum-digest-unresolved, erratum-incomplete | **killed** |
| **M2** anchor *and* correction → fabricated 64-hex (not in any manifest) | 2 | S110 | digest-unknown, erratum-incomplete | **killed** |
| **M3** S108 anchor shortened by one hex digit | 1 | S108 | digest-short | **killed** |
| **M4** S108 anchor uppercased | 1 | S108 | digest-uppercase | **killed** |
| **M5** S110 anchor fixed, the same 64-hex put in the teaches cell | 1 | S110 | token-outside-anchor | **killed** |
| C6 fabricated digest + *untracked* `SHA256SUMS.untracked` naming it | 1 | S110 | digest-unknown | ok (untracked manifest cannot launder) |
| NULL F2 re-run | 0, byte-identical stdout | — | — | ok |

Five mutants, five kills, each by its own class — not by a shared generic failure. M5 is the answer to the
cheapest wrong fix ("paste the digest elsewhere"): the anchor is valid in that mutant and the *only* defect
is the misplaced token.

Usage paths: `--lane /nonexistent` → 2, `--lane corpus` (no SOURCES.md) → 2, `--bogus` → 2,
`--evidence-ref bogus` → 2.

## 6. Decisions taken, and what they cost

- **Whole-row scan, anchor-cell rule.** Tokens are collected from every cell so a misplaced claim is seen;
  only the anchor cell's tokens are resolved. Cost: a legitimate digest mentioned in `teaches` prose would
  be flagged; no such row exists today (`tokens=11`, all in anchor cells).
- **Ellipsis = abbreviation, and abbreviations are resolved.** S036's 8-hex prefix is checked against A
  instead of being excused. Cost: a prefix claim needs a committed digest to point at; that is the point.
- **`--evidence-ref index` exists for fixtures.** Default is `head`, so an unpromoted capture never counts
  at integration; the index mode is how a seat that may not commit demonstrates the green state (C7 shows
  head mode still reports 4 on the same tree). Cost: one flag, printed by `--verbose`.
- **`--evidence-ref` reach is `corpus/evidence/` only**, as frozen. `plans/fixtures/r29/` also holds S070's
  bytes; I did not widen A to it, because a second root invites "which trees count" negotiation. If the L1
  prefers that root, S070 leaves the defect list without any capture — a one-line change to `EVIDENCE`.
- **Uppercase 64-hex is a defect** even though it denotes the same bytes: every manifest here writes
  lowercase, and a case-insensitive compare would hide a manifest written in another case (M4).

Limits, named: the check is observational — a resolved digest shows the claim matches committed bytes, not
that the bytes are the upstream originals (Q5: a retained digest is not the source; my live fetch is the
independent observation, and it is a one-day observation at immutable pins). The four captures make the
claims re-checkable in-lane; they are promotions of byte-identical copies, so they cannot by themselves
falsify the claims. The check says nothing about digests of *fragments* (line ranges) or about
`AFAAE9DD`-style short prefixes longer than 8 hex if a future row is careless in a different way.

## 7. For the L1 (integration, in this order)

1. `plans/anchor_digest_check.py` ← this seat's `anchor_digest_check.py` (byte-identical, do not re-wrap).
2. `corpus/evidence/round37/anchor-captures/` ← `captures/*` (5 files, `sha256sum -c` clean).
3. Append the erratum of §4 (one line) to `corpus/lessons/round-36.md`'s errata block.
4. `python3 plans/anchor_digest_check.py --lane .` → `rows=103 tokens=11 defects=0`, exit 0; then register
   the row in `SKILL.md` and, if wanted, one `QUALITY.md` line ("an anchor digest resolves to committed
   evidence or to an erratum that names the wrong token and a manifest digest").

Interaction worth knowing: rows S111-S113 (C2's this round) do not exist at `44b7298` (`grep -c
'S111\|S112\|S113' corpus/SOURCES.md` → 0), so this check currently says nothing about them; once the C2
seat lands them, this check covers C2's frozen V3 condition lane-wide (V3 tests only those three rows).

## 8. Axes

- **calibration — improved.** A routed defect now has a check that fails on the lane (5 defects,
  `digest-short` on S110 verbatim) and passes only when the claim is actually supported; 5/5 mutants killed
  by five distinct classes, plus a null, an untracked-manifest control and a mode control. The check also
  removes the "this row is right because I remember fetching it" class of claim for four more rows.
- **freshness — improved.** Four live re-fetches at immutable pins today, digests equal to the rows; the
  four unsupported claims are discovered now rather than in a future spot-check.
- **no harm.** No lane file written: `git -C <lane> status --porcelain` shows only other seats' untracked
  wave paths (`assimilation/`, `build/`, `prior-art/`, `make_falsify_spec.py`). No tool installed; stdlib
  Python 3, git and curl only. Scratch `/fast/scratch/hyaku/kengaku-r37/R37AnchorSweep/` created and
  deleted (`ls` → absent).

VERDICT: anchor-sweep-before-5-after-0-mutants-5/5
