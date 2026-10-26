# R43PkgRows — S129–S134 registry rows, Gate lines, and the measured registry state

Seat: `R43PkgRows` (scribe, kengaku round 43 wave 1). Lane `kengaku-shokunin`, lane HEAD at start of work
`d33350fdb01ce27cbff47b04642fd2c1471e5c26` (worktree dirty only with other seats' `.ufo/waves/round-43/…` trees; nothing
staged). I edited no lane file: the six rows, the Gate section and every receipt below are drafts in my own subdir.

**Axes named (godspeed posture).** (a) *Coverage* — six anchored captures of one grader, one row each, none duplicating
another's statement; (b) *freshness* — six pinned raw URLs re-fetched and byte-compared, access time to the second;
(c) *registry conformance* — 11 cells, one `sha256` token per anchor, `E=0`, `anchor_digest defects=0`;
(d) *landing safety* — every coupling the rows create (used-by, V3, V6) measured in a scratch copy before the L1
touches `corpus/SOURCES.md`; (e) *flip honesty* — the two Gate rejects carry a mechanical flip check, and the check was
run against the wave-1 entry draft rather than left to landing.

## 1. Behavior

- **Six rows drafted** in `sources-rows-S129-S134.md`, in the registry's exact 11-cell shape (template S125–S128): id,
  source name + pinned raw URL, kind, tier A, scope, anchor, teaches, `mined`, `2026-10-26`, `180d`, used-by
  `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md`. No `|` inside any cell.
- Each anchor cell carries **exactly one** `sha256 <64 hex>` token, equal to that row's `plans/pkg-spec-r43.json` pin
  and to the capture's bytes, plus a ≤25-word verbatim quote with its line.
- **Re-fetched** all six raw URLs and `cmp`-ed them against the committed captures: six `200`, six identical.
- **Validated** in a scratch copy of the registry (`sources-census.sh validate`) and on a staged clone
  (`anchor_digest_check.py`), plus the frozen counter's own V3/V6.
- **Drafted** the lesson `## Gate` table for the six admitted rows, two rejects (`Dockerfile`, `feal.py`) and one
  "captured, not rows" group, each with a checkable flip.

## 2. Re-fetch receipt (freshness)

Base `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis`;
compared against `corpus/evidence/round43/tb2-feal-differential-cryptanalysis/` (committed at HEAD). Times are UTC as
printed by `date -u` and -03 local for the L1's original fetch.

| row | upstream | http | fetched (UTC) | sha256 | cmp vs capture |
|---|---|---|---|---|---|
| S129 | `tests/test_outputs.py` | 200 | 2026-10-26T22:07:25Z (19:07:25 -03) | `585780e76d98094ad118d096f8c78f2281352dc9826e3687c4de152659631a3d` | identical |
| S130 | `instruction.md` | 200 | 2026-10-26T22:07:25Z (19:07:25 -03) | `b4093780b283e5c9838997769fb7bca090e3f4cbbd2d7cb275ba60cdfd722572` | identical |
| S131 | `tests/feal_module.c` | 200 | 2026-10-26T22:07:26Z (19:07:26 -03) | `1ae1c8a31b099b5742b35a3d6b1b70a2509d8d13d79ab74535e038e9a3379363` | identical |
| S132 | `tests/feal.c` | 200 | 2026-10-26T22:07:26Z (19:07:26 -03) | `bd4e9fb31e38073414d8a1930b2e67bc59eaee17e52f58133f781d297073e885` | identical |
| S133 | `tests/test.sh` | 200 | 2026-10-26T22:07:26Z (19:07:26 -03) | `106c27394c96343c03b4fbac14faac85542bce6628bccc66a5fe036d77f72daf` | identical |
| S134 | `README.md` | 200 | 2026-10-26T22:07:26Z (19:07:26 -03) | `887407c78513837d93f02231998419a0ce9b0cc0a0c600ed86cd30df5cb24e7f` | identical |

Command (one run, six files): `curl -sS --max-time 60 -o "$id" -w '%{http_code}' "$BASE/$sub"` then `sha256sum` and
`cmp -s "$id" "$CAP/$cap"`; receipt `refetch.txt` (sha256 `52eae1a7…c9b19665`). The six digits also equal the
`SHA256SUMS` entries in the capture directory (`SHA256SUMS` own digest `8c9123c1f1e42dd42b86e76e4f18c35fe1cdee1bfe48b9e05626c6d6ca844ab3d`).
The L1's first fetch of all twelve files was 2026-10-26 18:40 -03 (claims file); no byte changed between 18:40 and
19:07 -03.

Row-shape check (frozen counter's own rules, run over the draft):

```
S129 cells=11 anchor_tokens=['585780e7…631a3d'] sha256_in_other_cells=[] quote_words=4
S130 cells=11 anchor_tokens=['b4093780…d722572'] sha256_in_other_cells=[] quote_words=9
S131 cells=11 anchor_tokens=['1ae1c8a3…3379363'] sha256_in_other_cells=[] quote_words=11
S132 cells=11 anchor_tokens=['bd4e9fb3…073e885'] sha256_in_other_cells=[] quote_words=7
S133 cells=11 anchor_tokens=['106c2739…f72daf'] sha256_in_other_cells=[] quote_words=4
S134 cells=11 anchor_tokens=['887407c7…5cb24e7f'] sha256_in_other_cells=[] quote_words=8
```

(the abbreviated digests there are the script's `[:8]+"…"+[-8:]` form; the files carry the full 64 hex). Every quoted
phrase was located with `grep -Fn` at the line the anchor names: `test_outputs.py:30`, `instruction.md:3`,
`feal_module.c:52`, `feal.c:66`, `test.sh:26`, `README.md:35`.

## 3. The six rows (verbatim draft)

Source of truth: `sources-rows-S129-S134.md` (sha256 `4928c2f1…b2644b29`). Insert after S128, before `## Paths`.
Reproduced here so the L1 can paste without opening the file.

```
| S129 | Terminal-Bench 2.0 feal-differential-cryptanalysis grader (tests/test_outputs.py) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/tests/test_outputs.py | code | A | the executed scoring predicate of this one TB2 task at a pinned commit: one pytest function that builds the C reference extension, imports the agent's module into the grader's own interpreter, and compares one key, as this capture shows it | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, test_outputs.py:1-30, :30 "assert feal_in_c.get_keys()[5] == stolen" (4 words); sha256 585780e76d98094ad118d096f8c78f2281352dc9826e3687c4de152659631a3d | one test function, not a suite: it shells setup.py build_ext inside /tests at :20, appends /app and /tests to sys.path, then calls attack.attack(feal_in_c.encrypt) and asserts get_keys()[5] equals the returned object | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md |
| S130 | Terminal-Bench 2.0 feal-differential-cryptanalysis task instruction (instruction.md) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/instruction.md | docs | A | the request this one task states to the agent at a pinned commit: the file to write, the function signature, the value to return, and the time budget the grader is mapped against | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, instruction.md:1-6, :3 "Your attack should run in less than 30 seconds" (9 words); sha256 b4093780b283e5c9838997769fb7bca090e3f4cbbd2d7cb275ba60cdfd722572 | asks for /app/attack.py with attack(encrypt_fn) returning the uint32 key[5] under 30 seconds, and states that each of the six round keys comes from a 16-bit seed | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md |
| S131 | Terminal-Bench 2.0 feal-differential-cryptanalysis C extension (tests/feal_module.c) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/tests/feal_module.c | code | A | the CPython extension the grader compiles and imports at a pinned commit: the three methods it exports to Python, one of which hands the live six-key array back as a list | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, feal_module.c:1-68, :52 "Get the current keys as a list of 6 32-bit values" (11 words); sha256 1ae1c8a31b099b5742b35a3d6b1b70a2509d8d13d79ab74535e038e9a3379363 | the module named feal_in_c exports create_random_keys, encrypt and get_keys, and get_keys copies all six uint32 keys into a fresh Python list, so the answer is readable from inside the graded interpreter | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md |
| S132 | Terminal-Bench 2.0 feal-differential-cryptanalysis reference cipher (tests/feal.c) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/tests/feal.c | code | A | the reference FEAL-like cipher and its key schedule at a pinned commit: the clock-seeded rand derivation and the four-round Feistel core a differential attack is aimed at | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, feal.c:1-100, :66 "key[i] = (x * 1234567) & 0xFFFFFFFF" (7 words); sha256 bd4e9fb31e38073414d8a1930b2e67bc59eaee17e52f58133f781d297073e885 | create_random_keys seeds one srand(time(NULL)) per process and derives six keys as (rand() & 0xFFFF) * 1234567, which encrypt then uses across whitening, pre-mixing, four rounds and post-mixing | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md |
| S133 | Terminal-Bench 2.0 feal-differential-cryptanalysis verifier script (tests/test.sh) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/tests/test.sh | code | A | the verifier command that decides this task's reward at a pinned commit: apt and uv bootstrapping around one uvx pytest invocation, then one bit written from its exit status | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, test.sh:1-29, :26 "echo 1 > /logs/verifier/reward.txt" (4 words); sha256 106c27394c96343c03b4fbac14faac85542bce6628bccc66a5fe036d77f72daf | the reward is pytest's exit status alone, tested at :25 and written at :26 or :28, after pytest 8.4.1 runs under uvx python 3.13 with setuptools 80.9.0 and emits a ctrf json log | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md |
| S134 | Terminal-Bench 2.0 feal-differential-cryptanalysis README (README.md) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/README.md | docs | A | the task's own README at a pinned commit: the environment, resources and time limits it states, the verification steps it claims, and the skills it says are tested | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, README.md:1-35, :35 "Confirms the attack completes within the time limit" (8 words); sha256 887407c78513837d93f02231998419a0ce9b0cc0a0c600ed86cd30df5cb24e7f | states one CPU, 2048 MB, 30 minutes for the agent and 30 seconds for the attack, and claims the test confirms the time limit although test_outputs.py never times the call | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md |
```

Recheck date, both by `date -u -d '2026-10-26 +180 days'` and by `datetime.date(2026,10,26)+180d`: **2027-04-24**.

## 4. Validation receipts (every run envelope-bracketed)

All runs: `…/.ufo/waves/round-43/claims/envelope.sh "$S/env" <cmd>`; `$S=/fast/scratch/hyaku/kengaku-r43/R43PkgRows`.
`local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` on **every** run (no `INVALID`, nothing
installed, no PATH-dir write).

### 4.1 `sources-census.sh validate --file …` — three states

| state | command tail | exit | findings |
|---|---|---|---|
| lane registry, before the rows | `--file <lane>/corpus/SOURCES.md` | **0** | `E=0 W=15`, `file ok` |
| scratch copy **with** the six rows, **no** entry | `--file $S/census-noentry/corpus/SOURCES.md` | **1** | `E=6 W=15`; the six are exactly `E11 S129…S134 missing used-by corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` |
| scratch copy **with** the six rows **and** the entry on disk | `--file $S/census/corpus/SOURCES.md` | **0** | `E=0 W=15`, `file ok` |

ENVELOPE lines (first/last of the three):

```
ENVELOPE start 19:10:46 cwd=/home/vgpnk/Projects/shokunin
file	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
ENVELOPE end 19:10:48 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 19:10:03 cwd=/home/vgpnk/Projects/shokunin
file	E11	S134 missing used-by corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md
ENVELOPE end 19:10:05 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 19:09:54 cwd=/home/vgpnk/Projects/shokunin
file	ok	/fast/scratch/hyaku/kengaku-r43/R43PkgRows/census/corpus/SOURCES.md
ENVELOPE end 19:09:55 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

The scratch copy is a copy of the lane's `corpus/SOURCES.md` plus `corpus/knowledge/` and `corpus/lessons/` (so every
pre-existing `E11` resolves) plus a one-line placeholder at the entry path for the third state. The `W04` set (15
duplicate-URL warnings) is pre-existing and byte-identical in all three runs, so the rows add no finding of any class
when the entry is present. Receipts: `census-lane-baseline.txt`, `census-no-entry.txt`, `census-with-entry.txt`.

### 4.2 `anchor_digest_check.py --lane <clone>` after `git add corpus/SOURCES.md`

Clone `git clone -q --shared <lane> $S/lane`; `git -C $S/lane rev-parse --show-toplevel` → `…/R43PkgRows/lane`;
`git -C $S/lane diff --cached --stat` → `corpus/SOURCES.md | 6 ++++++`.

```
ENVELOPE start 19:10:11 cwd=/home/vgpnk/Projects/shokunin
EVIDENCE ref=head files=476 manifest_digests=72 rows=127 paths=547 bound_rows=35 unbound_rows=92
BIND S129 capture=corpus/evidence/round43/tb2-feal-differential-cryptanalysis/test_outputs.py by=url-task
BIND S130 capture=corpus/evidence/round43/tb2-feal-differential-cryptanalysis/instruction.md by=url-task
BIND S131 capture=corpus/evidence/round43/tb2-feal-differential-cryptanalysis/feal_module.c by=url-task
BIND S132 capture=corpus/evidence/round43/tb2-feal-differential-cryptanalysis/feal.c by=url-task
BIND S133 capture=corpus/evidence/round43/tb2-feal-differential-cryptanalysis/test.sh by=url-task
BIND S134 capture=corpus/evidence/round43/tb2-feal-differential-cryptanalysis/README.md by=url-task
rows=127 tokens=33 defects=0
ENVELOPE end 19:10:13 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Baseline on the same clone before the rows: `rows=121 tokens=27 defects=0` (exit 0). `--evidence-ref index` after
staging: `rows=127 tokens=33 defects=0`, exit 0 — identical (`anchor-index.txt`). Every new row binds to its own
capture, not to a union and not to a sibling capture.

### 4.3 The frozen counter's own V3 and V6 (`plans/round43_c2_verify.py`, imported, not edited)

```
ENVELOPE start 19:10:25 cwd=/home/vgpnk/Projects/shokunin
V3 ok rows=6 bad=0
V6 ok census_exit=0
ENVELOPE end 19:10:27 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`V3` is the counter's own rule: each spec row has an 11-cell registry row whose anchor cell carries exactly one
`sha256` token equal to the spec pin — `rows=6 bad=0`. `V6` is `sources-census.sh validate` on the clone's registry with
the entry placeholder on disk — `census_exit=0`. Without the entry the same V6 is `census_exit=1` with the six `E11`
lines above, so **the entry must land before or with the rows**; the rows cannot be green alone. Receipt `v3v6.txt`.

## 5. Lesson `## Gate` draft

`lesson-gate-draft.md` (sha256 `77cc7ce0…9464b8c8`): a `## Gate` section in the round-42 lesson shape — access date
2026-10-26 for every row, times -03, quotes ≤25 words at the cited line — with six **Admitted (mined, tier A)** rows,
each naming the URL, both fetch times (L1 18:40, this seat 19:07:25–26), the quote, the digest and a flip condition,
plus three reject-side rows:

- `Dockerfile` — **reject**, capture `c40553e4…af356a30`, quote `Dockerfile:4` "WORKDIR /app" (2 words).
  Flip, mechanical: `grep -nE 'Dockerfile|WORKDIR /app' corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md`
  non-empty → admit as a tier-B mechanism row.
- `feal.py` — **reject**, capture `23cc077b…2d2885dfe`, quote `feal.py:89` "main()  # noqa: F821" (4 words).
  Flip, mechanical: `grep -n 'feal\.py' …grader.md` non-empty → admit as a tier-B mechanism row.
- `task.toml`, `SHA256SUMS`, `setup.py`, `solve.sh`, `feal.h` — captured, not rows, each with the statement that would
  admit it.

**Both flips fire on the wave-1 entry draft already on disk.** The flips were run, not imagined:
`grep -nE 'Dockerfile|WORKDIR /app' .ufo/waves/round-43/build/R43PkgEntry/tb2-feal-differential-cryptanalysis-grader.md`
returns lines 69-71, 95, 149, 327, 377 — including the `Initial state` table row citing `Dockerfile:4`, `:6`, `:8`; and
`grep -n 'feal\.py'` on the same file returns 70-71, 209, 245, 248. The landing choice is therefore explicit: admit two
tier-B mechanism rows (ids the L1's) **or** delete the citing sentences. Carrying a fired flip unexecuted is the
round-42 defect (`round-42.md` Gate, `Dockerfile` row) this round's mined mistake names.

## 6. Findings

1. **The rows are green only with the used-by entry on disk.** Measured: `E=0` with it, exactly six `E11` without it,
   and no other class changes. `plans/round43_c2_verify.py` V6 will be `DEFECT` if the L1 lands `corpus/SOURCES.md`
   before `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md`. Landing order: entry, then rows (or both in
   one landing).
2. **Two Gate rejects fire against the current entry draft** (§5). This is the case where a flip condition written
   honestly says "admit", and the draft already needs the two files.
3. **`--file` resolution trap for scratch validation.** `sources-census.sh` resolves `used-by` against
   `realpath(dirname(<file>)/..)`, so a scratch copy at `<scratch>/SOURCES.md` (the shape my ticket suggested) reports
   every mined row's used-by as missing: measured `E=156`, exit 1 (`census-plain-path.txt`). The workable shape is
   `<scratch>/corpus/SOURCES.md` with `<scratch>/corpus/…` beside it; that is the shape of every green run in §4.1.
4. **Two prose facts the entry seat may need, recorded from the captures, not asserted as rows.** `README.md:35` claims
   the test "Confirms the attack completes within the time limit" while `test_outputs.py` imports only `os` and `sys`
   (`:3-4`) and never times the call — this is why S134 is admitted as a falsifiable statement rather than a restatement
   (the round-42 README refusal reason does not apply). And `/app/feal.py` cannot run as a script as shipped: `:89`
   calls `main()`, which the file never defines.
5. **No renumbering or collision.** S129–S134 were the first unused ids (`grep -c` over the registry: none of the six
   ids occurs before insertion; rows 121 → 127, tokens 27 → 33).

## 7. Out of scope / not done by me

- The entry `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` (another seat's draft; I only read it to
  run the flip checks), `corpus/README.md` index row and §Frontier, `PROVINCE.md`, the lesson file itself, and the
  registry's `## Paths` / `## Search log` entries — all L1 integration.
- I did not touch `corpus/SOURCES.md`, `plans/`, the counters, the probes, the spec, the gate, the captures or the
  receipt. I did not commit, stage, or push anywhere; the only `git add` was in my own scratch clone, whose
  `--show-toplevel` I asserted first.
- C1 (`plans/battery43`) and the C2 entry are other seats' work; I ran no counter attack and no probe.

## 8. Limits

- "Fresh" here means the pinned URL still serves the captured bytes at 19:07 -03 on 2026-10-26; it says nothing about
  the branch tip or later commits.
- Tier A is claimed for these six files at commit `2fd12b88…` only, and for the statements worded in the rows —
  nothing about TB2 as a benchmark.
- The 11-cell/one-token checks are the census's and the anchor checker's own rules; a reviewer still owes the
  non-author read of the `teaches` cells for distinctness (I kept them deliberately disjoint: predicate, request,
  extension surface, cipher/key schedule, reward mapping, README claims).
- Tooling: nothing installed or upgraded this seat (host `curl 8.23.0`, `python3`, `bwrap` at `/usr/bin/bwrap` already
  present); no pacman transaction attempted.

## 9. Artifacts (all under `.ufo/waves/round-43/build/R43PkgRows/`, 50,879 bytes in ten files)

| file | sha256 |
|---|---|
| `sources-rows-S129-S134.md` (the six rows) | `4928c2f1cc3f02dfab5b42a8ff366169c7f685ae897372c3925f6381b2644b29` |
| `lesson-gate-draft.md` (Gate table + prose) | `77cc7ce00433094341fd9c2085e14c32c96d6fadf49a49218bd5b36b9464b8c8` |
| `refetch.txt` | `52eae1a73c6d9e693e65373c9eaab19de563a8182189688352f7bd33c9b19665` |
| `census-lane-baseline.txt` | `2b7686702841b972b6021a7e75645307ee7b204b6c8c928062b4bdc0ea1c7225` |
| `census-no-entry.txt` | `db3f2f22102f0f8a284419d73d1da56013a4fb2c2e94efa00df6a52e54daba41` |
| `census-with-entry.txt` | `d46b8da63265917a040488cdc918998be6b01484367a429f346d1d1cad110d9a` |
| `census-plain-path.txt` | `c54723390d9a7766f44edd589f5c86a461474dbae1f77be901815443249929dc` |
| `anchor-head.txt` | `1ee9c3a127fcd241d6ac73ef4c7f046cab6a056c8f0f3533ef7a170987401585` |
| `anchor-index.txt` | `8cc8754ac72149a166ae435d7a28bae21e2dc4db7788b1ab2d8ac0b128bf3c41` |
| `v3v6.txt` | `2ec1afa3e42e4ae186b28e2fefdf6f7639f72fe1aa4bb740ae5696e7bca53fc5` |

Scratch `$S=/fast/scratch/hyaku/kengaku-r43/R43PkgRows` deleted with `plans/scratch_guard.py safe-rm` after the
receipts were copied out.

VERDICT: rows-drafted-6-census-exit-0
