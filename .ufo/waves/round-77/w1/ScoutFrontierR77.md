# ScoutFrontierR77 — kengaku round 77, wave w1, seat scout

**Role:** scout (leaf; no subagent dispatched). **Read-only:** no lane file edited, no git/jj mutation.
**Round:** kengaku 77 w1. **Freeze revision:** `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`
(`git log -1 --format=%H -- plans/round-77-claims.md`). **Base:** `07c97fcd` (`07c97fcd..9ebb8ed1` = 1 commit).
**Scratch:** `/fast/scratch/hyaku/kengaku-r77/ScoutFrontierR77/` (deleted before yield).
**Axes named:** coverage (C1's declaration universe, checked against the host rather than the declaration) and
calibration (a receipt stamp that cannot be re-derived, and an id-set re-derivation).

**As-of:** probes were run against the lane worktree at the freeze `9ebb8ed1`; the L1 advanced the tip to
`4f2ff9be` while this seat ran. The canonical table is byte-identical across that range
(`git diff 9ebb8ed1..4f2ff9be -- PROVINCE.md | grep -cE '^\+\\|'` → 0; no table row added or edited), and the
counter re-run at the new tip prints the same `SURFACES total=28 … DEFECTS n=0` and
`TARGET total=28 unlisted=0 live=27 agree=28 disagree=0` / `PREDICATE R77-C1 pass`, rc 0.

Method: every anchor below was probed by this seat with stdlib commands/scripts under the scratch root; the
counter `plans/round77_c1_declared_surfaces.py` was **run** for cross-check (at the freeze and at the new tip) but
**not imported**, and its receipts were not trusted. `python3 plans/round77_c1_declared_surfaces.py --lane .` writes nothing without
`--receipt` (verified in `main()`), so the run left the lane unchanged.

---

## 1. S253 re-open — the capture, digest and quote reproduce

```
$ curl -sL -m 60 -o $S/git-cat-file.html -w '%{http_code} %{size_download}\n' https://git-scm.com/docs/git-cat-file
200 79488
$ echo $?
0
```

```
$ sha256sum $S/git-cat-file.html
91805d9aec858f88581552fc1fe105a40a649544f872e72e6daff210a113e910  git-cat-file.html
$ wc -l $S/git-cat-file.html
2855 git-cat-file.html
```

| check | expected (S253 / claims) | observed | verdict |
|---|---|---|---|
| HTTP status | 200 | 200 | agree |
| size | 79 488 B | 79 488 B | agree |
| sha256 | `91805d9a…a113e910` | `91805d9aec858f88581552fc1fe105a40a649544f872e72e6daff210a113e910` | **match** |
| committed capture | `corpus/evidence/round77/sources/git-cat-file.html` | same sha256 | **match** |
| byte identity | — | `cmp` fresh vs committed → rc 0 | **identical** |
| quote location | capture line 2584 (claims: 2584–2585) | line 2584 ends with `&lt;object&gt;</span>`; line 2585 is `will be returned.</p>` | agree |
| quote words | ≤ 25 (row: 15) | 15 | agree |
| anchor | `git cat-file <type> <object>` | rendered text at line 2191: `<pre class="content"><em>git cat-file</em> &lt;type&gt; <span …>&lt;object&gt;</span>` | agree |

Evidence lines (fresh capture, verbatim):
```
2584:<p>If <span class='synopsis'><em>&lt;type&gt;</em></span> is specified, the raw (though uncompressed) contents of the <span class='synopsis'><em><span class="hover-term" data-term="object">&lt;object&gt;</span></em></span>
2585:will be returned.</p>
2191:<pre class="content"><em>git cat-file</em> &lt;type&gt; <span class="hover-term" data-term="object">&lt;object&gt;</span>
```
Whitespace-normalised rendered text contains the sentence `If <type> is specified, the raw (though uncompressed)
contents of the <object> will be returned.` verbatim, and contains the anchor `git cat-file <type> <object>`.
The literal HTML string is not contiguous (tags interleave inside the quote) — the row's quote is a rendered-text
quote, which is how the claims file words it ("15 words").

`corpus/SOURCES.md:269` (S253) is byte-unchanged vs `HEAD` (`git diff --stat HEAD -- corpus/SOURCES.md` → empty).
**No disagreement** with the claims or the row. The page self-reports "git-cat-file last updated in 2.56.0"
(capture line 1324), so the digest is a capture-time pin by construction, as declared.

---

## 2. Host surface truth — 28/28 canonical rows agree with the host

Rows parsed from `PROVINCE.md` heading `## Declared surfaces — canonical, machine-checked (round 77, 2026-11-04)`
(**line 1011**, 28 rows). Probes: `Path.exists` (with `~` expansion and brace expansion for
`/tmp/bench-r{4,5,6,7,7-l2-executor}`), `urllib.request` (3 s), `socket.create_connection`, `hashlib.sha256`,
a census-row regex `^\|[ \t]*S[0-9]{3,}[ \t]*\|`, and `git merge-base --is-ancestor`.

| # | row | kind | declared | observed | agree? |
|---|---|---|---|---|---|
| 1 | Research notes (SSOT for eval craft) | path | absent | absent | yes |
| 2 | Research notes (former wikillm path) | path | absent | absent | yes |
| 3 | Local benchmark battery | path | absent | absent | yes |
| 4 | Local benchmark battery (former path) | path | absent | absent | yes |
| 5 | Served local model (:34113) | http | absent | http=000 | yes |
| 6 | Served local model (:45669) | http | absent | http=000 | yes |
| 7 | Served local router (:1234) | http | present | http=415 | yes |
| 8 | Route telemetry | path | absent | absent | yes |
| 9 | Bounty-hunter tree | path | absent | absent | yes |
| 10 | Client CLI telemetry | path | absent | absent | yes |
| 11 | Client CLI sync state | path | absent | absent | yes |
| 12 | Model catalogs (local index) | path | absent | absent | yes |
| 13 | Model catalogs (remote APIs) | remote | remote | not probed (REMOTE 2026-11-04) | yes |
| 14 | Own probe artifacts | path | present | exists | yes |
| 15 | In-repo verdict gate | hash | present | sha256 90c87c886502…ae941f pin-match=True | yes |
| 16 | Attribution instrument | hash | present | sha256 489f938a198e…16e06b pin-match=True | yes |
| 17 | Attribution frozen tables | path | present | exists | yes |
| 18 | Corpus gate docs | path | present | exists | yes |
| 19 | Public-literature registry | count | present | rows=245 pin=245 | yes |
| 20 | ds-flash-shim source (read-only) | hash | present | sha256 42d86d99d426…15a386 pin-match=True | yes |
| 21 | Live probe endpoint | tcp | present | tcp=127.0.0.1:8791:open | yes |
| 22 | Public literature (cite anchor) | path | present | exists | yes |
| 23 | Open-model catalog digest | path | present | exists | yes |
| 24 | Interval re-verdict instrument | exec | present | receipt exit0, LANE_TIP 07c97fcd ancestor | yes |
| 25 | State-assertion check | exec | present | receipt exit0, LANE_TIP 07c97fcd ancestor | yes |
| 26 | Serving-stack process pin (rounds 10-14) | cmd | absent | 3/3 paths absent | yes |
| 27 | Ephemeral probe trees (rounds 4-7) | path | absent | absent | yes |
| 28 | Corpus index | path | present | exists | yes |

**Disagreements: none.** 28 rows, 28 agree, 0 disagree. Declared distribution `present=14 absent=13 remote=1`
(the counter prints the same). Cross-check: the counter's printed `SURFACE` verdicts equal my independent
observed verdicts on all 28 rows (`observed_vs_counter_mismatch []`).

Identity checks beyond the bare verdict:
- **:1234** — `ss -ltnp` → `LISTEN 127.0.0.1:1234 users:(("llama-server",pid=1505,fd=18))`;
  `systemctl --user is-active lfm3-server.service` → `active`; `show -p MainPID` → `MainPID=1505`.
  The row's "llama.cpp router, `lfm3-server.service`" holds (HTTP 415 is any-status-on-loopback = present).
- **:8791** — `ss` → `python3` pid 1145327; `/proc/1145327/cmdline` →
  `/usr/bin/python3 /home/vgpnk/.local/share/ds-flash-shim/shim.py`. The row's shim identity holds.
- **hash rows** — recomputed full digests match the abbreviated pins:
  `grader.py` `90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f` (pin `90c87c88…ae941f`);
  `plans/attrib_probe.py` `489f938a198e08cf8c30efc3ca24ea5fac90ef3909d80aec0b1f62c90616e06b` (pin `489f938a…16e06b`);
  `~/.local/share/ds-flash-shim/shim.py` `42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386` (pin `42d86d99…15a386`).
- **count row** — `corpus/SOURCES.md` has **245** lines matching the census-row pattern; pin `rows=245`.
- **exec rows** — both receipts exist, contain `exit 0`, and carry `LANE_TIP 07c97fcd…` with
  `git merge-base --is-ancestor 07c97fcd 9ebb8ed1` → rc 0 (direct parent).
- **cmd row** — all three anchors absent: `/proc/1299/cmdline`, `~/.config/systemd/user/qwen-coder.service`,
  `~/.config/llama/qwen-coder-godspeed.jinja`.
- **brace row** — 5 expanded targets, 5 absent: `/tmp/bench-r4`, `-r5`, `-r6`, `-r7`, `-r7-l2-executor`.
- **absent-prose checks** — `~/Projects` contains no `webzites/`, no `bounties/`, no `the-bounty-hunter`;
  `find ~/Projects -maxdepth 4 -name llm-wiki` and `find ~/archive …` return nothing; `~/archive` itself does not
  exist; `~/.bailian`, `~/bench-arena`, `~/archive/bench-arena` absent. The rows' absence prose is not stale.

Counter cross-check (read-only run; identical output at freeze `9ebb8ed1` and at tip `4f2ff9be`):
```
SURFACES total=28 present=14 absent=13 remote=1
UNLISTED n=0
RESOLVED live=27
AGREE agree=28 disagree=0
DEFECTS n=0
TARGET total=28 unlisted=0 live=27 agree=28 disagree=0
PREDICATE R77-C1 pass
```
rc 0. This is consistent with the frozen target, but it is **not** my evidence for the table above; the table is
the independent probe.

### 2a. Flag — the two new exec receipts stamp a `TOOL_SHA` that cannot be re-derived

`corpus/evidence/round77/exec-attrib-calibration.txt:2` and `exec-state-check.txt:2` both carry

```
TOOL_SHA 78f12c7ee63df6e81703f691fc8b1f2d7d60e03b76b67735507d1956ed90e44d
```

and both carry `LANE_TIP 07c97fcd2fcca74f72df1d3c6b9dfe662fd75b59`. At tip `4f2ff9be` each receipt gained a
`COMMAND` line naming the tool it runs; the `TOOL_SHA` line was not changed. Observed:
- the counter's sha256 at the freeze (`9ebb8ed1`), at tip `4f2ff9be`, and in the worktree is
  `229b1713373ce28b68e1f77d668e7d8edb9da80b6a2ab2e904c39219574485b2` — not `78f12c7e…`;
- `plans/round77_c1_declared_surfaces.py` does not exist at the receipts' own `LANE_TIP`
  (`git cat-file -e 07c97fcd:plans/round77_c1_declared_surfaces.py` → rc 128, "exists on disk, but not in
  '07c97fcd'"), so no committed tool bytes at that tip can carry that digest;
- no file under `plans/`, `corpus/evidence/round77/`, `.ufo/waves/round-77/` has sha256 `78f12c7e…`
  (bounded `find | sha256sum` scan, zero matches); both receipts carry the *same* stamp for *two different* tools,
  which rules out "the executed tool's own digest".

C1's frozen exec rule (`script exists` + receipt `exit 0` + `LANE_TIP` ancestor) never reads `TOOL_SHA`, so the
C1 target is unaffected and this is **not** a C1 kill. But it is the R76-V1 failure shape sitting in round 77's
own new evidence: a receipt stamp that names no reproducible tool. [INFERENCE] it is the digest of a pre-freeze
draft of the counter that minted the receipts before the final commit. Worth the L1's decision: either re-mint
with the landed counter (then `TOOL_SHA` re-derives at `4f2ff9be`) or state in the receipt/lesson that the stamp
is a draft digest.

---

## 3. considerthese sweep — proposal 2 has no implementing artifact

Exact command from the item, run at the freeze revision via `git grep` (worktree is being edited by the L1, so
this block is revision-pinned):

```
$ git grep -n 'tb2_grader_admit' 9ebb8ed1 -- plans corpus SCORECARD.md SKILL.md
9ebb8ed1:SCORECARD.md:2919:**Planned (round 67).** (1) C2's successor: a PROBE-binding predicate for the round-65 strict gate, frozen before data, using the committed R65 receipt's own instrument header and the committed probe bytes, with the fabricated fixture as red and the committed receipt as green; the counter's `LANE_ROOT_FALLBACK` and the `fabrication-declaration` scan limited to the BUILD/RUN/FILES/ENV field lines (ReceiptMutate d2 false positive). (2) Carry the open mistake rows 4–7 (dated corrections on the four real pointers `SKILL.md:686`, `SCORECARD.md:2885`, `LOG.md:2512`, round-65 report lines 14 and 78; census-before relabel; Q47 base; census pointer). (3) Consider the considerthese item 2 (`tb2_grader_admit.py`, one standing TB2 admission counter with a built-in filler control) as the round's frontier claim if it can be frozen with a filler control that stays red. L0 questions carried: `kengaku | round-25/33/51`, `kengaku | round-56`, `kengaku | round-63`, `kengaku | round-54`, `kengaku | round-66`.
9ebb8ed1:corpus/lessons/round-66.md:332:- **considerthese (one proposal, selected, not implemented).** `considerthese/2026-10-26.md`, item 2, verbatim: "One standing TB2 admission counter with a built-in filler control." Its implementing check (`grep -rn 'tb2_grader_admit' plans corpus SCORECARD.md`) returns 0 hits; the item stays unimplemented and is recorded as the next frontier candidate (SiblingOverlap seat, `.ufo/waves/round-66/w1/SiblingOverlap.md`).
9ebb8ed1:corpus/lessons/round-76-verifier-spotcheck.md:210:  `corpus/lessons/round-66.md:332` records proposal 2 (`tb2_grader_admit`) as unimplemented and my
9ebb8ed1:corpus/lessons/round-76-verifier-spotcheck.md:211:  sweep agrees: `grep -rn 'tb2_grader_admit' plans corpus SCORECARD.md SKILL.md` hits only that
9ebb8ed1:corpus/lessons/round-77.md:31:  landed as the round-62 class census. Proposal 2 (`tb2_grader_admit`, one standing parametrised TB2
9ebb8ed1:corpus/lessons/round-77.md:32:  admission counter with a committed filler control) is **open**: `grep -rn 'tb2_grader_admit' plans
9ebb8ed1:plans/round-77-claims.md:87:must record proposal 2 (`tb2_grader_admit`) as open; one capability name must hold in `PROVINCE.md`
9ebb8ed1:plans/round-77-claims.md:137:  inventory and the burn-down. `considerthese/2026-10-26.md` proposal 2 (`tb2_grader_admit`) is
9ebb8ed1:plans/round77_c2_defect_discharge.py:31:  V5  the considerthese re-adjudication is recorded with proposal 2 (`tb2_grader_admit`) open or
9ebb8ed1:plans/round77_c2_defect_discharge.py:258:        if "tb2_grader_admit" not in line:
9ebb8ed1:plans/round77_c2_defect_discharge.py:264:    return "fail", "no re-adjudication line for tb2_grader_admit"
9ebb8ed1:plans/round77_c2_defect_discharge.py:498:    (lane / LESSON77).write_text("# Round 77\n\n- considerthese proposal 2 `tb2_grader_admit` remains open.\n")
```

12 matches in 6 files. The only non-record hits are the C2 counter's own strings (`V5` leg, its fixture line, and
its lesson write-out) and the claims file's two mentions. **No line is an implementation of the proposal.**

Live worktree run of the literal item command `grep -rn 'tb2_grader_admit' plans corpus SCORECARD.md SKILL.md`,
captured while the L1 was editing (that state is now committed at tip `4f2ff9be`): 16 lines — 12 source lines
corresponding to the freeze set (the C2 counter sits at lines 266/272/512 in that revision), 3 hits in
`plans/__pycache__/round77_c2_defect_discharge.cpython-314.pyc` (lines 35/112/216, bytecode of the counter, not a
new artifact), and 1 ledger line new since the freeze. The 13 non-bytecode lines are:

```
plans/round-77-claims.md:87:must record proposal 2 (`tb2_grader_admit`) as open; one capability name must hold in `PROVINCE.md`
plans/round-77-claims.md:137:  inventory and the burn-down. `considerthese/2026-10-26.md` proposal 2 (`tb2_grader_admit`) is
plans/round77_c2_defect_discharge.py:31:  V5  the considerthese re-adjudication is recorded with proposal 2 (`tb2_grader_admit`) open or
plans/round77_c2_defect_discharge.py:266:        if "tb2_grader_admit" not in line:
plans/round77_c2_defect_discharge.py:272:    return "fail", "no re-adjudication line for tb2_grader_admit"
plans/round77_c2_defect_discharge.py:512:    (lane / LESSON77).write_text("# Round 77\n\n- considerthese proposal 2 `tb2_grader_admit` remains open.\n")
corpus/lessons/round-66.md:332:- **considerthese (one proposal, selected, not implemented).** `considerthese/2026-10-26.md`, item 2, verbatim: "One standing TB2 admission counter with a built-in filler control." Its implementing check (`grep -rn 'tb2_grader_admit' plans corpus SCORECARD.md`) returns 0 hits; the item stays unimplemented and is recorded as the next frontier candidate (SiblingOverlap seat, `.ufo/waves/round-66/w1/SiblingOverlap.md`).
corpus/lessons/round-76-verifier-spotcheck.md:210:  `corpus/lessons/round-66.md:332` records proposal 2 (`tb2_grader_admit`) as unimplemented and my
corpus/lessons/round-76-verifier-spotcheck.md:211:  sweep agrees: `grep -rn 'tb2_grader_admit' plans corpus SCORECARD.md SKILL.md` hits only that
corpus/lessons/round-77.md:31:  landed as the round-62 class census. Proposal 2 (`tb2_grader_admit`, one standing parametrised TB2
corpus/lessons/round-77.md:32:  admission counter with a committed filler control) is **open**: `grep -rn 'tb2_grader_admit' plans
corpus/routed-findings.jsonl:91:{"id": "R76-V5", "class": "contradicted-claim", "source": "corpus/lessons/round-76-verifier-spotcheck.md:208", "opened_round": 76, "status": "closed", "owner": "kengaku", "disposition": "fixed-verified", "close": "the round-77 lesson records the re-adjudication at 8da90eb7: proposal 1 and 3 implemented, proposal 2 (tb2_grader_admit) open, with the grep that proves no implementing artifact exists", "close_commit": "8da90eb7299435aceb9466d70344bba7046094b2", "verified_at": "2026-11-04", "blocker": null, "check": "# R76-V5: grep -q 'tb2_grader_admit' corpus/lessons/round-77.md", "note": "the lane's own record must be re-read before repeating a prior-art claim", "evidence_path": "corpus/lessons/round-77.md", "evidence_literal": "tb2_grader_admit"}
SCORECARD.md:2919:**Planned (round 67).** (1) C2's successor: a PROBE-binding predicate for the round-65 strict gate, frozen before data, using the committed R65 receipt's own instrument header and the committed probe bytes, with the fabricated fixture as red and the committed receipt as green; the counter's `LANE_ROOT_FALLBACK` and the `fabrication-declaration` scan limited to the BUILD/RUN/FILES/ENV field lines (ReceiptMutate d2 false positive). (2) Carry the open mistake rows 4–7 (dated corrections on the four real pointers `SKILL.md:686`, `SCORECARD.md:2885`, `LOG.md:2512`, round-65 report lines 14 and 78; census-before relabel; Q47 base; census pointer). (3) Consider the considerthese item 2 (`tb2_grader_admit.py`, one standing TB2 admission counter with a built-in filler control) as the round's frontier claim if it can be frozen with a filler control that stays red. L0 questions carried: `kengaku | round-25/33/51`, `kengaku | round-56`, `kengaku | round-63`, `kengaku | round-54`, `kengaku | round-66`.
```

(the only line in this block absent from the freeze set is `corpus/routed-findings.jsonl:91`, the C2 append —
`git show 9ebb8ed1:corpus/routed-findings.jsonl | grep -c R76-V` → 0 at the freeze, → 7 at tip `4f2ff9be`. The
ledger line parses as JSON and is 753 B at capture time.)

Implementing-artifact search, `"anywhere in the repo"`:
- `find . -path ./.git -prune -o -iname '*tb2*' -print` → no `tb2_grader_admit*` file. The `tb2*` names are all
  wave artifacts/reports (`.ufo/waves/round-34|35|38|44|45|46|52|53/...`), captures and per-round probes.
- `ls plans/tb2_grader_admit.py` → rc 2, "No such file or directory". No `plans/tb2_grader_admit.py` exists.
- `grep -rln 'tb2_grader_admit' /home/vgpnk/Projects/shokunin/scripts /home/vgpnk/Projects/shokunin/.ufo/prompts`
  → rc 1, no output (nothing in the fleet scripts or prompt tree).
- fleet-wide: `find /home/vgpnk/Projects/shokunin -maxdepth 4 -name 'tb2_grader_admit*' -not -path '*/.git/*'`
  → no output; `grep -rln 'tb2_grader_admit' /home/vgpnk/Projects/shokunin --include=*.py --exclude-dir=.git`
  → only `kengaku-shokunin/plans/round77_c2_defect_discharge.py` (the V5 leg). No lane, no script, no instrument.
- Proposal 2 text (`considerthese/2026-10-26.md:44-48`) asks for "a single parametrised `tb2_grader_admit.py`
  that digest-pins the spec, dry table and probe it reads …, ships a committed filler package that must stay red,
  and is re-run at every tip for all five admitted graders." No such instrument exists.

**Answer: proposal 2 remains open; no implementing artifact anywhere in the repo.** The round's own lesson says so
(`corpus/lessons/round-77.md:31-32`), consistent with `corpus/lessons/round-66.md:332` and
`corpus/lessons/round-76-verifier-spotcheck.md:210-211`.

### 3a. Flag — the round-66 implementing check has flipped meaning

`corpus/lessons/round-66.md:332` records proposal 2's implementing check as
`grep -rn 'tb2_grader_admit' plans corpus SCORECARD.md` returning **0 hits**. Re-run today from the lane root:
rc 0, 16 lines (13 source + 3 bytecode), because round 77 *names the proposal* in the claims, the lesson and the
C2 counter — not because an artifact appeared. A grep for the proposal's **name** is not a grep for its **artifact**; after this round the round-66
check can no longer distinguish "implemented" from "mentioned". The C2 V5 leg's own wording ("open" /
"no implementing artifact") is the right shape; the round-66 sentence is the one that needs a dated correction
if it is reused as a check.

---

## 4. Assimilation check — id-set re-derivation (adopt nothing)

The §10 pipeline (`0–3`-space anchor, `sort` without `-u`), run from the lane root with scratch paths abbreviated:

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md \
    | grep -oE 'S[0-9]+' | sort > staged-ids
$ comm -12 reg-ids staged-ids > collisions
```

| measure | value |
|---|---|
| registry id list (`corpus/SOURCES.md`) | **245** |
| staged id list (`SOURCES.append.md`) | **175** |
| collision count (`comm -12`) | **167** |
| duplicate ids within registry | 0 (`sort | uniq -d` → 0) |
| duplicate ids within staged | 0 |
| staged-only ids | 8 |
| registry-only ids | 78 |
| registry id range | S001 … S253 |
| staged id range | S077 … S251 |

Pattern sensitivity: the column-zero-only pattern (`^\|…`) yields **245 / 175 / 167** — identical to the
`0–3`-space anchor, because neither file has an indented id row (`grep -cE '^ {4,}\|'` → 0 for both;
`grep -cE '^ {1,3}\|[[:space:]]*S[0-9]'` → 0 for both). The indented-row case the prompt says the guard was
proven on is therefore **not exercised by this package's bytes**; the pattern is still the correct one and the
guard's fixture proof (round 32/43/44) is the evidence for the indented case, not this run.

**Adopt nothing.** 167 colliding ids is mass drift, not a renumber job; consistent with the claims'
"Assimilation: none" and the L0 `round-54` drift item.

### 4a. Flag — the claims' "~120-row renumber map" is not reproduced

`plans/round-77-claims.md` §Sources and frontier says adoption "would need a ~120-row renumber map". The id-set
pipeline measures **167** colliding ids (8 staged-only ids do not collide; 175 − 8 = 167). The direction is the
same, but the number is not reproducible from the staged bytes by the §10 pipeline. [INFERENCE] the ~120 counts
*admitted entries* rather than colliding *ids*; the L1 should either derive it from the admitted-entry list or
replace it with the measured 167. This is prose in the claims' Stated limits, not a frozen predicate field.

---

## 5. Findings summary (numbers, not adjectives)

1. **S253 reproduces**: HTTP 200, 79 488 B, sha256 `91805d9a…a113e910` = pin; fresh capture byte-identical to the
   committed capture (`cmp` rc 0); quote begins line 2584, ends line 2585, 15 words; anchor rendered at 2191.
2. **Canonical inventory is host-true**: 28/28 rows agree with independent probes; 0 disagreements; counter
   cross-check `AGREE agree=28 disagree=0`, `DEFECTS n=0`, `TARGET … unlisted=0 live=27 …`, rc 0.
3. **Proposal 2 (`tb2_grader_admit`) has no implementing artifact**: `plans/tb2_grader_admit.py` absent
   (`ls` rc 2), no `*tb2*` instrument anywhere in the lane, fleet-wide `find … -name 'tb2_grader_admit*'` empty,
   fleet scripts/prompts grep rc 1. It stays open.
4. **Assimilation id sets**: registry 245, staged 175, collisions **167**; bare and 0–3-space patterns coincide
   (no indented id rows); adopt nothing.
5. **Calibration flag (new evidence, outside C1's predicate)**: both round-77 exec receipts stamp
   `TOOL_SHA 78f12c7e…`, which matches no tool at any revision (counter at `9ebb8ed1`/`4f2ff9be` = `229b1713…`;
   counter absent at the receipts' `LANE_TIP 07c97fcd`). The C1 exec leg passes without reading it — the R76-V1
   class recurs in round 77's own receipts.
6. **Calibration flag (prose)**: round-66's implementing check for proposal 2 has flipped from 0 hits to
   non-zero purely because round 77 names the proposal; the claims' "~120-row renumber map" is not the measured
   167.

## 6. Remaining unknowns

- The provenance of `TOOL_SHA 78f12c7e…` (no file carries that digest today; a pre-freeze draft of the counter is
  the plausible source, unprovable from the repo).
- Whether the L1's in-flight `corpus/routed-findings.jsonl` and `plans/round77_c2_defect_discharge.py` edits reach
  C2's frozen target — C2 seats' question, not this seat's.
- Nothing else in this seat's four items is unresolved.

## 7. Command log (rc where meaningful)

| command | result |
|---|---|
| `curl … git-cat-file` | `200 79488`, rc 0 |
| `sha256sum git-cat-file.html` | `91805d9a…a113e910` |
| `cmp` fresh vs `corpus/evidence/round77/sources/git-cat-file.html` | rc 0 |
| `python3 resolve_rows.py` (this seat, stdlib only) | `ROWS parsed=28`, 28 agree / 0 disagree |
| `python3 plans/round77_c1_declared_surfaces.py --lane .` | `PREDICATE R77-C1 pass`, rc 0 |
| `ss -ltnp | grep -E ':(1234|8791)'` | `llama-server` pid 1505; `python3` pid 1145327 |
| `systemctl --user is-active lfm3-server.service` | `active` |
| `git merge-base --is-ancestor 07c97fcd 9ebb8ed1` | rc 0 |
| `git grep … 9ebb8ed1 -- plans corpus SCORECARD.md SKILL.md` | 12 matches / 6 files |
| `grep -rn 'tb2_grader_admit' plans corpus SCORECARD.md SKILL.md` (capture-time worktree) | 16 lines (13 source + 3 bytecode) |
| `grep -rn 'tb2_grader_admit' plans corpus SCORECARD.md` (round-66's own check, re-run) | rc 0, 16 lines — its recorded "0 hits" no longer holds |
| `ls plans/tb2_grader_admit.py` | rc 2 |
| `grep -rln … scripts .ufo/prompts` | rc 1 |
| `find /home/vgpnk/Projects/shokunin -maxdepth 4 -name 'tb2_grader_admit*'` | no output (no instrument anywhere in the fleet) |
| §10 id pipeline | 245 / 175 / 167 |
| `git status --porcelain` | this seat's only write is `.ufo/waves/round-77/w1/ScoutFrontierR77.md`; no production file touched |

Scratch dir `/fast/scratch/hyaku/kengaku-r77/ScoutFrontierR77/` is removed at yield.
