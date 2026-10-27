# R44PkgRows — nine registry rows S138–S146 and the round-44 `## Gate` block

Seat: scribe (leaf, no subagents). Written 20:32–20:47 -03, 2026-10-26. Lane tip at read time
`5e3d3aa06c6b7000929ac3e62563a39159c4501f`. Read-only reads of the frozen inputs: `plans/pkg-spec-r44.json`,
`plans/round-44-claims.md`, `corpus/SOURCES.md` (header + S129–S137), `corpus/lessons/round-43-verifier-spotcheck.md`
§5, `corpus/lessons/round-43.md` `## Gate`, the eleven captures, the receipt, the wave reports
`R44CritGateRows.md` / `R44ScoutRefetch.md`. Wrote only `.ufo/waves/round-44/wave/R44PkgRows*` and my scratch
`/fast/scratch/hyaku/kengaku-r44/R44PkgRows` (removed at the end). No lane file, corpus file, plan, jj or git index was
touched; no commits; no tool installs (nothing needed installing); `PROVINCE.md`, `corpus/README.md`,
`corpus/SOURCES.md` and the entry file in the lane were already modified/untracked by other seats when I started.

## 1. Deliverable

- **Rows** — nine 11-cell rows S138–S146, drafted verbatim in
  `.ufo/waves/round-44/wave/R44PkgRows/rows-S138-S146.md`; insert point is immediately after S137 (line 152 in the
  lane copy, before `## Paths`). Registry 130 → 139.
- **Gate block** — `.ufo/waves/round-44/wave/R44PkgRows/gate-block.md`, a complete `## Gate` section for
  `corpus/lessons/round-44.md` (that file does not exist yet; the block is written to be appended as-is).
- **Validation** — `validate.sh` (re-runnable), `refetch.sh`, `rowcheck.py`, and their outputs
  (`validate.txt`, `refetch.txt`, `refetch-gitignore.txt`, `rowcheck.txt`, `census-green.txt`, `census-red.txt`,
  `anchor-verbose.txt`).

Both acceptance gates measured green, each with a red control:

| gate | command | observed |
|---|---|---|
| census | `sources-census.sh validate --file <clone>/corpus/SOURCES.md` | exit **0**, `0` E-codes, `15` W04 (all pre-existing: S040 S048 S057 S058 S059 S064 S065 S066 S067 S068 S069 S071 S075 S076 S100) |
| anchor | `python3 plans/anchor_digest_check.py --lane <clone>` | `rows=139 tokens=45 defects=0`, exit **0**; nine `BIND … by=url-task`, nine `RESOLVED` |
| census red control | same, with the used-by file removed | exit **1**, `E11` on all nine rows (9 lines) |
| anchor red control | same, S138's last digest nibble flipped | `DEFECT S138 … class=digest-unknown`, `defects=1`, exit **1** |

## 2. Freshness — eleven files re-fetched and byte-compared

`refetch.sh` at 20:33:51–20:33:52 -03 (`refetch.txt`), plus the `.gitignore` path probe at 20:42:23
(`refetch-gitignore.txt`). All against
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/`.

| time | capture | upstream | http | bytes | cmp |
|---|---|---|---|---|---|
| 20:33:51 | test_outputs.py | tests/test_outputs.py | 200 | 2914 | identical |
| 20:33:51 | instruction.md | instruction.md | 200 | 618 | identical |
| 20:33:51 | gen.py | environment/task-deps/gen.py | 200 | 3496 | identical |
| 20:33:51 | Dockerfile | environment/Dockerfile | 200 | 386 | identical |
| 20:33:51 | test.sh | tests/test.sh | 200 | 611 | identical |
| 20:33:51 | README.md | README.md | 200 | 1810 | identical |
| 20:33:51 | solve.sh | solution/solve.sh | 200 | 7724 | identical |
| 20:33:52 | decrypt.c | environment/task-deps/decrypt.c | 200 | 3982 | identical |
| 20:33:52 | task.toml | task.toml | 200 | 917 | identical |
| 20:33:52 | feal.c | environment/task-deps/feal.c | 200 | 3472 | identical |
| 20:42:23 | gitignore | `.gitignore` | 200 | 177 | identical |
| 20:42:23 | gitignore | `gitignore` | **404** | 14 | DIFFERS (error body) |

The capture is named `gitignore`; upstream it is `.gitignore` (probe of four spellings: `.gitignore` 200,
`gitignore` 404, `environment/task-deps/.gitignore` 404, `tests/gitignore` 404; the pinned git tree lists
`.gitignore`, 177 B). This is recorded in the Gate reject row so a reader can re-check the one path that is not
`<task>/<capture>`. Independent corroboration: seat `R44ScoutRefetch` fetched the same eleven at 20:33:08–20:33:10
(`ok=11`, upstream drift 0 after the pin). My digests equal `SHA256SUMS` and the nine spec pins exactly:

```
$ (cd corpus/evidence/round44/tb2-feal-linear-cryptanalysis && sha256sum *)
ef521cde…28bfff1d  Dockerfile      a038645f…f6d3dc33  README.md
9ecc3aeb…8c726eb7  SHA256SUMS      4c6864e0…0a94ebd2  decrypt.c
bbd38d19…2dea08da  feal.c          3a71f0b5…7c452c63  gen.py
9a8dd8d9…07c25953  gitignore       a2f1669d…b6f71b03  instruction.md
be50ae01…da29cb77  solve.sh        a39ec2c4…0e7c9fc4  task.toml
9431cbc2…d2e7c9e1  test.sh         f59ebc72…106ed9f9  test_outputs.py
```

ENVELOPE lines for this leg (`q32`):
```
ENVELOPE start 20:33:51 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 20:33:53 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 20:42:23 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 20:42:25 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

## 3. The nine rows

Cell 2 carries the exact pinned URL (`<raw_base><upstream>`, checked equal to `pkg-spec-r44.json` for all nine, not
just by basename); cell 6 carries exactly one `sha256 <pin>` token plus a locator; tier `A`, status `mined`, opened
`2026-10-26`, recheck `180d`, used-by `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md` (spec `entry_rules`).
Each quote is a verbatim substring of the cited physical line; ranges count the last line of files without a final
newline (`README.md:1-32`, `decrypt.c:1-142`), which is the round-43 closure R2 off-by-one.

```
$ python3 rowcheck.py rows-S138-S146.md
ROWS parsed=9
OK S138 capture=test_outputs.py line=122 verbatim=True words=4/4 sha256_pin=True cells=11
OK S139 capture=instruction.md line=7 verbatim=True words=11/11 sha256_pin=True cells=11
OK S140 capture=gen.py line=12 verbatim=True words=6/6 sha256_pin=True cells=11
OK S141 capture=Dockerfile line=14 verbatim=True words=3/3 sha256_pin=True cells=11
OK S142 capture=test.sh line=26 verbatim=True words=4/4 sha256_pin=True cells=11
OK S143 capture=README.md line=32 verbatim=True words=9/9 sha256_pin=True cells=11
OK S144 capture=solve.sh line=304 verbatim=True words=3/3 sha256_pin=True cells=11
OK S145 capture=decrypt.c line=136 verbatim=True words=2/2 sha256_pin=True cells=11
OK S146 capture=task.toml line=34 verbatim=True words=3/3 sha256_pin=True cells=11
DEFECTS 0
```

| row | kind | anchor quote (line) | teaches, in one line |
|---|---|---|---|
| S138 | code | `assert c in data` (:122, 4 w) | one pytest function: 100 decimals in one string (:4-103), whole file at :120, membership only |
| S139 | docs | `Implement a known-plaintext attack that recovers the key of the cipher.` (:7, 11 w) | attack + output file named, no numeric format; `hex-output` fails an unstated rule |
| S140 | code | “keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]” (:12, 6 w) | keys literal; every plaintext = sha256(seed_hash+counter)[:8] (:23-28, :57-62), counters 0-31 / 32-131 |
| S141 | code | `RUN rm gen.py` (:14, 3 w) | image builds feal+decrypt, runs the generator, deletes orig_plaintexts.txt and gen.py |
| S142 | code | `echo 1 > /logs/verifier/reward.txt` (:26, 4 w) | reward is pytest exit status alone; no timing, no format inspection |
| S143 | docs | `verifies that all 100 expected plaintext values appear in` (:32, 9 w) | 1 CPU/2 GB/10 GB (:21), 30 min each (:22), and the membership claim the receipt exploits |
| S144 | code | `./attack > /app/plaintexts.txt` (:304, 3 w) | the oracle; `./decrypt` at :289; not graded by test.sh |
| S145 | code | “printf("%lu\n", plaintext);” (:136, 2 w) | decimal medium (:132-137); 20-bit mask (:31-35); >0xFFFFF refused (:114-117) |
| S146 | docs | `allow_internet = true` (:34, 3 w) | name+image (:5, :29), both 1800 s (:22, :25), resources (:30-32), network flag |

S140 and S145 use curly quote delimiters because the quoted line itself contains straight double quotes (precedent:
S121/S123 in this registry). Every other anchor uses straight quotes.

## 4. Gate block and reject rows

`gate-block.md` holds the round-43-shaped section: header (access date, both fetch times, quote discipline, base URL),
nine admitted rows each with reason + digest-flip condition, three rejects, the flip-check command, and gate prose.

Rejects, each with a reason and a flip a reader can decide against the landed entry (closure R1):

| reject | reason | flip (decided by command, not by a flip line) |
|---|---|---|
| `feal.c` (captured, 3472 B) | implementation of the pair-generator executable; the graded artefact is `/app/plaintexts.txt`, so it holds no graded predicate | an entry sentence outside `## Located quotes` cites `feal.c:<line>` with no S138–S146 co-citation → re-source, or take the tier-B mechanism path (S135–S137 precedent) |
| `gitignore` (upstream `.gitignore`, 177 B) | repo hygiene only (`.git/`, `__pycache__/`, `dist.tar.gz`) | a citation of `gitignore:<line>` or `.gitignore:<line>` with no S138–S146 co-citation → re-source or delete; no tier-B path exists |
| `SHA256SUMS` | capture inventory; contentless as evidence | an entry sentence cites it |

Flip verdicts, run 20:44 -03 against the lane entry `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md`
(sha256 prefix `bf0dee2a0d2b9025`), command as printed in the Gate block:

```
Flip check (round 44): feal\.c — not fired
Flip check (round 44): gitignore — not fired
Flip check (round 44): SHA256SUMS — not fired
```
Supporting facts: the entry names `feal.c` only at `:127` (a `Dockerfile:3-14`-backed build-table row) and `:161`
(inside an `instruction.md:1` quote); it never says `gitignore` or `SHA256SUMS` (grep hits 0). All nine ids S138–S146
appear in the entry (2–4 hits each), so V9's requirement is met by that entry, and the three `not fired` verdicts are
honest against it at that time; they must be re-decided if the entry body changes.

## 5. Conflict with the rows already in the lane (reported, not resolved by me)

Between 20:38 and 20:42 another seat/L1 wrote a *different* S138–S146 into the lane (`corpus/SOURCES.md:153-161`) and
the entry file. Whole-row comparison, my draft vs that landed draft:

- identical: ids, URLs (byte-equal for all nine), kind, tier A, `mined`, `2026-10-26`, `180d`, used-by, all nine
  `sha256` pins.
- different: source labels (`task request` vs `task instruction`, `sequence generator` vs `pair generator`, …), anchor
  style, teaches wording.

Measured defects in the landed rows (`census-lane-20-43.txt`, `lane-rows-as-found-20-42.txt`):

1. **Anchor check is red on the lane as landed.** `anchor_digest_check.py --lane .` →
   `DEFECT S140 anchor token=c class=token-outside-anchor detail=sha256-claim-in-cell-5-of-11 loc=corpus/SOURCES.md:155`,
   `rows=139 tokens=46 defects=1`, exit 1. Cause: S140's teaches cell reads "…a **sha256 chain** over seed and counter";
   the tool reads any `sha256` + hex-run outside the anchor cell as a claim (`c` here, from "chain") and defects it.
   My draft's S140 teaches says "sha256 of their concatenation", which produces no token — the same tool prints
   `rows=139 tokens=45 defects=0` on my copy. Fix in the lane is a wording change only ("hash chain over seed and
   counter" or "sha256 of …").
2. **S145 range is short by one.** Landed row `:160` and entry `:8` both say `decrypt.c:1-141`; the capture has **142**
   physical lines (`awk 'END{print NR}'` → 142, last byte `}`, no final newline) and the quote in that row points at
   `:136`. My draft writes `:1-142`. This is the closure R2 shape recurring on a different file.
3. **S140's landed quote is elided, not verbatim.** `:12 "keys = ["0x68e63", ...]" (9 words)` contains a `...` that no
   line carries, and its 9-word count cannot be checked against the line. My draft quotes the full line (6 words,
   verbatim, curly-delimited).
4. **Six of nine landed anchors carry no quoted snippet** (S141 S142 S143 S144 S145 S146 carry `:NN label` locators
   only); S138 (4 w) and S139 (4 w) do. The round-43 nine rows all carried one, and the Gate block promises quotes
   ≤25 words at a cited line. Not a validator failure — a citation-strength difference the L1 now owns.

I did not edit the lane. The L1 chooses: take `rows-S138-S146.md` (validator-green as measured) or keep the landed rows
and apply items 1–3.

## 6. Gates, envelope, scratch

```
ENVELOPE start 20:40:20 cwd=/home/vgpnk/Projects/shokunin
TIP 5e3d3aa06c6b7000929ac3e62563a39159c4501f untracked_in_clone=2
ROWS 139
DRAFT-EQUALS-LANDED yes
ROWCHECK_exit=0
CENSUS_exit_code=0
CENSUS W04=15 E-codes=0
CENSUS_red_exit_code=1
ANCHOR_exit=0
rows=139 tokens=45 defects=0
ANCHOR_mutant_exit=1
ENVELOPE end 20:40:28 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
```
ENVELOPE start 20:43:25 cwd=/home/vgpnk/Projects/shokunin
CENSUS_lane_exit=0
E_codes=0
W04=15
DEFECT S140 anchor token=c class=token-outside-anchor detail=sha256-claim-in-cell-5-of-11 loc=corpus/SOURCES.md:155
rows=139 tokens=46 defects=1
ANCHOR_lane_exit=1
ENVELOPE end 20:43:27 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Clone discipline: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`,
`git -C "$S/lane" rev-parse --show-toplevel` → `$S/lane`, HEAD `5e3d3aa…`; rows appended uncommitted (nothing
committed anywhere); `$S/lane_mut` was a second throwaway clone for the digest red control and was deleted.
The census E11 leg needed a file at the used-by path, so the clone carried a labelled placeholder at
`corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md` (430 B, first line `# PLACEHOLDER — R44PkgRows validation
stand-in only`); it is not an entry and was never copied into the lane — the red control proves the check reads it.
Scratch removed with `scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r44 R44PkgRows /fast/scratch/hyaku/kengaku-r44/R44PkgRows`.

## 7. Out of scope (stated, not done)

No counter (`round44_c1_verify.py`, `round44_c2_verify.py`, `pkg_gate.py`) and no probe was run — not this seat's
assignment; the only validators run were census, anchor, and my own row checks. No entry content review beyond the
three flip checks. No edits to `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`, `PROVINCE.md`,
`SHONEN.md`, the lane's git/jj state, or any PATH directory. No install, no commit, no push.

## 8. Limits

- The census green state depends on the entry file existing; without it E11 is red by design (measured as the red
  control).
- Freshness covers bytes only; I did not check upstream history beyond `R44ScoutRefetch`'s drift-0 comparison (pin is
  the default-branch HEAD, quoted there).
- Two anchor cells use curly delimiters, so a consumer that demands straight quotes should read S140/S145 with that in
  mind; the quoted text is byte-verbatim.
- S143's quote ends mid-sentence ("…appear in") deliberately, to stay inside 25 words and inside the line.

## Artifacts

`.ufo/waves/round-44/wave/R44PkgRows/`: `rows-S138-S146.md` (draft rows), `gate-block.md` (Gate section), `rowcheck.py`
+ `rowcheck.txt`, `refetch.sh` + `refetch.txt` + `refetch-gitignore.txt`, `validate.sh` + `validate.txt`,
`census-green.txt`, `census-red.txt`, `census-lane-20-43.txt`, `lane-rows-as-found-20-42.txt`, `anchor-verbose.txt`.
Largest file 14,879 B.

VERDICT: rows-drafted-9-census-exit-0-anchor-defects-0
