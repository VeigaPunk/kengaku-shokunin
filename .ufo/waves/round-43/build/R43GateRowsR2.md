# R43GateRowsR2 — closure R2: the S128 Gate row and the Dockerfile flip (S135)

Seat: scribe, kengaku round 43 wave 1. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` read-only at tip
`d33350fdb01ce27cbff47b04642fd2c1471e5c26`; everything below was measured in
`/fast/scratch/hyaku/kengaku-r43/R43GateRowsR2` (clean `git clone -q --shared`, toplevel asserted). No lane file was
written; no commit anywhere. Three drafts + receipts under `.ufo/waves/round-43/build/R43GateRowsR2/`.

Axes I moved on (godspeed):

| axis | move |
|---|---|
| **record completeness (D2)** | the missing `## Gate` row for S128 is drafted, with the issue re-opened fresh (URL, both access times, 9-word verbatim quote) |
| **mechanism anchoring (D3 flip)** | S135 drafted as a tier-B mechanism row for `environment/Dockerfile` @ `2fd12b88`, re-fetched and `cmp`-identical, bound by `url-task` to its own capture; the entry sentences citing it at `:65`, `:89`, `:94`, `:435-438` drafted as an append |
| **verifiability** | the row validated in a scratch clone of the registry: census exit 0 (E=0, W=15 unchanged), anchor tool `defects=0` on both `--evidence-ref head` and `index`, plus two red controls that make the green non-vacuous |

## 1. Fresh re-measurements (this seat, 2026-10-26)

| what | command | output |
|---|---|---|
| Dockerfile @ pin | `curl -sS -o df.Dockerfile -w 'HTTP=%{http_code} bytes=%{size_download}\n' https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/environment/Dockerfile` | `HTTP=200 bytes=321` at `19:10:24-0300` → `19:10:25-0300` |
| digest | `sha256sum df.Dockerfile` | `780c23986778f3e5f842567868af30b1135ed095ca9449e1c90b7f0e0483d3d4` |
| capture parity | `cmp df.Dockerfile lane/corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile` | `CMP=IDENTICAL` (rc 0) |
| size / line 3 | `wc -l df.Dockerfile`; `sed -n 1,10p` | `10`; line 3 `WORKDIR /app`; `:9-10` `COPY tests/sim.c /app`, `COPY gates.txt /app` |
| issue 9645 | `gh api repos/OpenAgentsInc/openagents/issues/9645` (rc 0, `19:10:24-0300`→`19:10:25-0300`) | `state=closed created_at=2026-09-25T09:01:50Z closed_at=2026-09-25T09:11:26Z`, title `Audit circuit grader coverage beyond its 48,401 input ceiling`, user `AtlantisPleb`, 13-line body |
| quote location | `jq -r '.body' issue.json \| grep -n '48,401'` | body line 3: "The official grader exercises 28 values, none above 48,401." — 9 words, ≤25, verbatim |

## 2. Draft (a) — `## Gate` row for S128 → `R43GateRowsR2/lesson-gate-row-S128.txt`

Insertion: **one new table line** in `corpus/lessons/round-42.md` `## Gate`, after the last table row (`solve.sh`,
`gates.txt`, line 46) and before the `Gate prose:` paragraph (line 48); addition only (`1 0` numstat).
It carries: the URL, first open `17:35 -03` by `R42ScoutPriorArt`, re-open `19:10:24 -03` by this seat, the `gh api`
state/created/closed fields, the quote with its location (`issue body line 3`, 9 words), the tier-B reason (third
party's report, prior art only — it builds no circuit and names none of the parse/ordering/cwd mechanics) and the flip
condition.

Discernment note that decides the shape: a separate `## Gate addendum` section at EOF would **not** be read by the
lane's own Gate parsers — `plans/round36_c1_verify.py:315` reads
`re.search(r"^## Gate\n(.*?)(?=^## |\Z)", …)`, i.e. the section must literally begin `## Gate`. Hence a row inside the
existing table, not a new heading. The same file also carries an optional **prose repair** for line 48-52 ("the three
admitted rows are exactly the three the spec pins"): once S128 and S135 land, that sentence is stale and would
contradict the table; the draft gives the appended correction and keeps the original intact.

## 3. Draft (b) — registry row S135 → `R43GateRowsR2/registry-row-S135.txt`

Insertion: one new line after S128 (line 143) — the last row of `## Registry`, still before `## Paths` (line 144), so
it stays inside the section (no `E12`). 11 cells: id `S135`; source = the pinned raw URL of
`circuit-fibsqrt/environment/Dockerfile`; kind `code` (the kind the registry already uses for executed harness files,
S106/S109 `tests/test.sh`); tier `B`; scope = "the build recipe of the image this one task is graded in … the
mechanism that fixes the working directory"; anchor = `commit 2fd12b88…, environment/Dockerfile:1-10, :3 "WORKDIR
/app" (2 words); sha256 780c2398…3d3d4`; teaches = cwd mechanism + the two `COPY` lines + the negative (no graded
predicate here); status `mined`; opened `2026-10-26`; recheck `180d` (the cadence S125-S128 carry); used-by
`corpus/knowledge/tb2-circuit-fibsqrt-grader.md`.

One correction found while drafting, worth recording: my first draft wrote `environment/Dockerfile:1-14`; the capture
is **10** lines (`wc -l` → `10`). Fixed to `:1-10` and every number below is from the corrected row.

### Entry sentences → `R43GateRowsR2/entry-sentences-S135.txt`

An append-only block at EOF of `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` (last line today `:449`) that cites
S135 at the four cwd statements — `:65` (`Dockerfile:3` is `WORKDIR /app`, `:9-10` the two copies), `:89` (`Initial
state` row), `:94` (`gates.txt` resolved against a cwd the harness fixes at `/app`), `:435-438` (the wave-1 note that
the receipt's cwd is the verifier's `WorkingDir=/app`, which makes Finding 6's cwd coincidence load-bearing) — and
states the flip as executed, not waived. It edits none of those lines.

## 4. Validation of the row in a scratch copy of the registry

| run | command (all under `envelope.sh`) | observed |
|---|---|---|
| baseline census | `sources-census.sh validate "$S/lane"` on the clean clone | `exit=0`, `E=0`, `W=15`, `lane ok` |
| baseline anchor | `anchor_digest_check.py --lane "$S/lane" --evidence-ref head` | `rows=121 tokens=27 defects=0` |
| **census, row staged** | `sources-census.sh validate "$S/lane"` (`git add` → `M  corpus/SOURCES.md`) | **`exit=0`, `E=0`, `W=15`** (the same 15 pre-existing `W04`), `lane ok` |
| census counts | `sources-census.sh census "$S/lane"` vs `census --root … kengaku` (lane) | `rows 121→122`, `tier.B 17→18`, `status.mined 105→106`, `tier.invalid 0`, `missing 0` |
| **anchor, head** | `anchor_digest_check.py --lane "$S/lane" --evidence-ref head --verbose` | **`rows=122 tokens=28 defects=0`**; `BIND S135 capture=corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile by=url-task`; `RESOLVED S135 digest=780c2398…d3d4 … listed=…/Dockerfile` |
| **anchor, index** | `… --evidence-ref index` | **`rows=122 tokens=28 defects=0`** |
| red control A | S135's anchor ← S125's real digest `6117b8ed…0438` | `exit=1`, `DEFECT S135 … class=digest-wrong-capture`, `defects=1` |
| red control B | same basename, URL re-pointed at `regex-log/environment/Dockerfile` | `exit=1`, `DEFECT S135 … class=anchor-unbound detail=no-capture-for-upstream-regex-log/environment/Dockerfile-task=environment` |

The file was restored byte-identically between controls (`sha256 666cd67…` → `fc8d853…` after the `:1-10` fix;
`git status` `M ` only, no unstaged diff). Envelope lines (Q32), one per class of run — full copies in
`R43GateRowsR2/RECEIPT.txt`:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind <S>/env <S>/env --bind <S>/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- …
ENVELOPE start 19:12:53 cwd=/fast/scratch/hyaku/kengaku-r43/R43GateRowsR2   (census validate, staged)
ENVELOPE end 19:12:55 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
ENVELOPE start 19:12:59 … (anchor head)   ENVELOPE end 19:13:01 exit=0 … unchanged
ENVELOPE start 19:12:59 … (anchor index)  ENVELOPE end 19:13:01 exit=0 … unchanged
ENVELOPE start 19:13:09 … (red A)         ENVELOPE end 19:13:10 exit=1 … unchanged
ENVELOPE start 19:13:12 … (red B)         ENVELOPE end 19:13:14 exit=1 … unchanged
ENVELOPE start 19:11:31 … (baseline census/anchor)  ENVELOPE end 19:11:33 exit=0 … unchanged
```

Every run printed `local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` — no measurement here is
bracketed by a `CHANGED` digest (round-42 D5 shape).

## 5. Decisions and limits (stated, not hidden)

- **S135 stays out of `plans/pkg-spec-r43.json`.** That spec's `entry_rules.row_tier` is `"A"` and its `rows` are
  S129-S134 (the feal grader); `plans/pkg_gate.py:187-215` would then demand an entry `source:` line for S135 and
  `tier=A` on the row. S135 is tier B by the task's own instruction, and the spec is frozen, so the citation belongs in
  the entry body, not the triad. Precedent: S128 is cited from `## Prior art` (`:446`) and appears in no `source:` line.
  Consequence for the L1: do **not** add S135 to a `pkg-spec` `rows` map without changing `entry_rules` (a frozen
  instrument).
- **Presence limit of the anchor tool, and why the green is not vacuous.** `anchor_digest_check.py` raises nothing for
  a row with no anchor token and reports `bound_rows=30 unbound_rows=92` at this tip, so `defects=0` alone does not
  prove *this* row binds. The evidence that it does is the verbose `BIND S135 … by=url-task` + `RESOLVED S135` lines,
  the `tokens` count moving 27→28 (the row's token is parsed), and red controls A and B failing in the two ways a wrong
  locator/token must fail.
- **Not run by me (out of scope):** the C2 counter `plans/round43_c2_verify.py`, the feal probe, `pkg_gate.py`, and
  `round_close.py`. My numbers say nothing about the feal entry or the C1 battery.
- **Warnings unchanged:** the 15 `W04` lines are the same set before and after (S040, S048, S057-S059, S064-S069,
  S071, S075, S076, S100); the new row adds no warning and no `E`.

## 6. Conflicts, verbatim, for the canonical judge

1. `corpus/lessons/round-42.md:48-52` — "Gate prose: the three admitted rows are exactly the three the spec pins
   (`plans/pkg-spec-r42.json` `rows` = S125, S126, S127; …)". After S128 and S135 the admitted set is five candidates;
   the sentence needs the appended correction drafted in §2 (append-only, original intact). Until then the table and
   the prose disagree — that is a landing-order risk, not a measurement conflict.
2. `corpus/lessons/round-42.md:44` — the Dockerfile reject was conditional: "Flip: if the entry keeps the `WORKDIR
   /app` sentence …, admit `Dockerfile` as a **tier-B mechanism row**". The entry keeps it (`:65`, `:89`, `:94`,
   `:435-438`), so S135 is the flip executed. No contradiction with the entry; the entry's own `:64` sentence calls
   `Dockerfile` "a capture of the harness", which the appended block supersedes by naming S135 (it does not rewrite
   `:64`).
3. Round-42 spot-check §3 recorded the S128 Gate row as a defect (D2) while `corpus/SOURCES.md:143` already carried
   the row; the two records were never reconciled. My draft adds the Gate row only; the registry row is unchanged.
4. Possible duplicate ownership, not a conflict I can settle: the wave-1 build dir already contains an **empty**
   `R43FlipCheck/` (checked `19:15`, `ls` → no files; `grep -rl 'S135\|S128' R43FlipCheck R43R42Defects` → no hit,
   and `R43R42Defects/` does not exist). If that seat also drafts an S135 row or an S128 Gate row, the L1 must land
   one shape only — the two must not both land, or the registry will carry two rows for one file.

## 7. Artifacts

All under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/build/R43GateRowsR2/` (84 KB total):

| file | content |
|---|---|
| `registry-row-S135.txt` | the exact S135 row line, cell-by-cell rationale, insertion point, evidence |
| `lesson-gate-row-S128.txt` | the exact S128 Gate row, insertion point, optional prose repair |
| `entry-sentences-S135.txt` | the appended entry block citing S135 at `:65`, `:89`, `:94`, `:435-438` |
| `RECEIPT.txt` | every command + output, envelope lines, fetch and `gh api` projections |
| `census-base.txt`, `census-final.txt` | census `validate` before/after (both exit 0, E=0, W=15) |
| `census-count-baseline.txt`, `census-count.txt` | census counts 121→122, tier.B 17→18 |
| `anchor-base.txt`, `anchor-final-head.txt`, `anchor-final-index.txt` | `defects=0`, `rows=122 tokens=28` |
| `anchor-red-A.txt`, `anchor-red-B.txt` | the two red controls |
| `refetch-sha.txt`, `issue-projection.txt` | Dockerfile digest/parity; issue fields + body line 3 |

Scratch `/fast/scratch/hyaku/kengaku-r43/R43GateRowsR2` removed with
`python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r43 R43GateRowsR2 "$S"`
after the receipts were copied out. No tool installed, no `pacman` transaction, nothing written to any PATH directory
(the envelope digest is identical across every run).

VERDICT: gate-rows-drafted-2-census-exit-0
