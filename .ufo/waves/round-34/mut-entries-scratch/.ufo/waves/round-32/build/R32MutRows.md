# R32MutRows — mutation test of the S094/S097 row drafts against the adoption gate (C1)

Seat: `L1Kengaku32.R32MutRows` (mutation-tester, leaf). Date: 2026-10-25.
Bounds honored: scratch only in `/tmp/r32-R32MutRows/` (96 KB total << 60 MB); no productions edits;
no lane-repo writes except this report; no tool installs (python3 stdlib + curl already present;
zero installs to record).

## Baseline drafts under test

Drafted rows S094/S097 taken from the gate-built append block `R32GateBlock` (itself from the staged
`SOURCES.append.md`, normalized to the round-32 draft form: `opened=2026-10-25`, `recheck=180d`,
`used-by=corpus/knowledge/benchmark-grader-semantics.md`, `status=mined`). Both rows parse as exactly
11 cells. Captures: pinned Toolathlon `tasks/finalpool/ab-testing/evaluation/main.py` @
`9be8d8fe07a497b18ee61e3f2ae694e9797f39eb` (SHA-256 `3bad26b6…`, 14138 B) and arXiv 2412.05579v2
abs page (SHA-256 `44195c5f…`, 43661 B), copied from the scouts' fetches (digests match their reports).

| file | sha256 |
|---|---|
| rows-pristine.md (draft baseline) | `57c12fe4b91e1afc445502e672e36330155e3cddf215290affd892d1c22d2225` |
| rows-mut-a.md | `16821b3331e1ebbcd84d8d601f6250d4773baa0d54786813650b54b0ddd859d4` |
| rows-mut-b.md | `71003818621a53bb4ab4cc9cec96ed0d7a027d61b0962b1af2e579f4e8e95b3c` |
| rows-mut-c.md | `ddc4da62aab740d97ffeadacc33dd9667a85d9285600cf197bf93a7b5413a2b3` |
| rows-mut-d.md | `c14fc50534af0d96513d1ab423e30b4cf02c1ca3a35d4273ff88ebdcd11d28ba` |
| rows-mut-e.md | `ad4d481b07d15bb5f5265fec2dd2880eb0dd6087c92ae79f6807e7b90b5fe43c` |
| rows-corrected.md | `eb96a20dab05d0b6fedbfad245e45d052824dca76d53b3362f3998792c5572d9` |
| url-map.json | `d8cfc373f6d10eb4fc84c16f911cd12e9c75a67b44d390e38a691d25e306c3d0` |

## Detector baselines (pristine, before mutation)

All commands run from the lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

- Registry mode (strict, no scope): `python3 plans/sources_adopt.py --registry corpus/SOURCES.md --package /tmp/r32-R32MutRows/rows-pristine.md`
  → `registry=91 staged=2 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`, **EXIT=0**.
- Registry mode (admit/build): `--admit-ids S094,S097 --entries corpus/knowledge/benchmark-grader-semantics.md --access-date 2026-10-25 --recheck 180d`
  → same summary, block built with the two rows, **EXIT=0**.
- Quote mode: `--quote-file /tmp/r32-R32MutRows/rows-pristine.md --artifact /tmp/r32-R32MutRows/captures --url-map /tmp/r32-R32MutRows/url-map.json`
  → `QUOTE rows=2 spans=3 located=2 found=2 overlong=0 absent=1 malformed=0 cap=25 artifacts=arxiv-2412.05579v2.html,main.py mismatch=0 unmapped=0`
  with `REFUSED S097 absent words=20 quote="This paper presents a comprehensive survey of the LMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations."`, **EXIT=7**.

**Baseline finding (inconclusive, not a mutant):** the pristine drafted S097 quote fails the quote gate
because it is not a byte substring of the pinned capture: the staged draft reads `LMs-as-judges` while the
arXiv abstract bytes read `LLMs-as-judges` (the page contains the `LLMs` form at all three abstract render
positions; `LMs` appears only as a substring of `LLMs`). Replacing the typo with the byte-exact `LLMs-as-judges`
(`rows-corrected.md`) makes the baseline fully green: `QUOTE rows=2 spans=3 located=3 found=3 overlong=0
absent=0 malformed=0 mismatch=0 unmapped=0`, **EXIT=0**. So the adoption gate is healthy; the *draft row*
S097 needs the anchor corrected to `LLMs-as-judges` before C1's quote receipt can pass.

## Mutants and gate verdicts

All exit codes are the gate's own (`2` unreadable, `3` collision, `4` malformed, `5` request, `6` overlong,
`7` absent, `8`/`9` binding).

### M(a) escaped pipe inside a cell — S094 scope cell gains `\|`
- Quote mode: `QUOTE rows=1 … malformed=1`, `REFUSED` list holds S094, **EXIT=4** → **REFUSED**.
- Registry strict: `malformed=1`, `malformed: S094:escaped-pipe`, **EXIT=4** → **REFUSED**.

### M(b) prose recheck cell — S097 `recheck` becomes `2026-10-23 — re-verify at next revision`
- Registry strict: `defects=1 prose=1`, `defect S097: recheck-prose`, **EXIT=4** → **REFUSED**.
- Registry admit (no `--scope-to-admit`): same defect, **EXIT=4** (normalization to `180d` happens only
  under `--scope-to-admit`, per R32GateBlock's run).

### M(c) used-by pointing at a different entry — S094 `used-by` → `corpus/knowledge/benchmark-task-validity-checklist.md`
- Registry strict: `defects=0`, **EXIT=0** → **SURVIVED**.
- Registry admit: **EXIT=0**; the built block rewrites the cell to the admitted entry
  (`corpus/knowledge/benchmark-grader-semantics.md`). The gate *projects* `used-by` by design
  (round-29 attempt-2 claim: "a dangling-`used-by` row … must be rewritten to the admitted set only");
  no invocation of `sources_adopt.py` refuses a wrong `used-by`. The compensating check lives in the
  post-append `plans/adoption_check.py` `usedby_ok` receipt (`adoption-expect.json`), outside this tool.

### M(d) opened not 2026-10-25 — S094 `opened` → `2026-10-23`
- Registry admit, no `--attest-opened`: `missing: S094:not-opened-this-round`, **EXIT=5** → **REFUSED**.
- Registry strict (no admit): `defects=0`, **EXIT=0** (`opened` is not validated by `check()`; the refusal
  is the admit-path's `build_block` guard).

### M(e) 28-word anchor quote — S097 anchor span replaced by a locating 28-word byte substring of the capture
(`This paper presents … and Limitations. We begin by providing a systematic definition of`; 28 words, located)
- Quote mode: `overlong=1`, `REFUSED S097 overlong words=28 cap=25 at arxiv-2412.05579v2.html`, **EXIT=6**
  → **REFUSED**.

## Verdict

`VERDICT: survivor`

Four of five mutants are refused (M(a) exit 4, M(b) exit 4, M(d) exit 5, M(e) exit 6); **M(c) survives** —
the adoption gate does not refuse a `used-by` cell pointing at a different entry; it silently rewrites it
(and the strict registry check does not look at the cell at all).

## Restoration evidence

After all mutant runs, `rows-pristine.md` still hashes to `57c12fe4…` (untouched); every mutant and capture
is intact per the table above. No sibling files were modified; nothing in the lane repo was written except
this report.
