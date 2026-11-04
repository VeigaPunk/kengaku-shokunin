# ConnectorR80 — sibling-overlap scan: located-receipt / subject-stamp standards across the fleet

seat: ConnectorR80 (kengaku round 80, wave w1, 14 seats) · role: connector · leaf, read-only outside this file.
date: 2026-11-04.

## Measured revisions

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse master
6669fe72e59718acc1a0f32a92849a544b0b2f1c
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor af51132d8919cedd14d3d3407ae5abc966d5d427 master; echo rc=$?
rc=0
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor dce7c275381c669e6489f1b795b1505d0824c262 master; echo rc=$?
rc=0
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --oneline -3 master
6669fe72 round-80: integration — six located replays minted and the ledger flipped (R80-C1), V1-V6 routed rows …
6250e94b round-80: freeze amendment A1 …
af51132d round-80: freeze — R80-C1 located-replay predicates/table/driver/gate + three losing controls, …
```

Tip `6669fe72` has advanced past freeze `af51132d` (both named here per the round rules); the scan
reads master bytes plus clearly-labelled worktree bytes. Worktree state at measurement
(`git status --porcelain`, abridged): `M plans/round80-restamp.json`; untracked
`corpus/evidence/round80/{c1-after,r79-c1-after,r79-c2-after}.txt` and `.ufo/waves/round-80/w1*`
seat reports — L1 integration in flight. I touched none of it.

## Method and scan caveats

1. Read inputs: `plans/round-80-claims.md` (frozen), `corpus/lessons/round-78-verifier-spotcheck.md`
   (the standard's origin: its §3 reject "a `LANE_TIP` line locates a receipt" is what R80-C1
   operationalises), and `corpus/lessons/round-79-verifier-spotcheck.md` §6 (V1–V6, the C2 debts).
2. Fleet scans with the `grep` tool, patterns `LANE_TIP|TOOL_SHA|MINTED_BY`,
   `OBSERVATIONS_BEGIN|TASK-UNDER-TEST|tb2-header|SUBJECT-ABSENT`, then per-lane follow-ups
   (`tool_sha256|measured_commit|RECEIPT-TOOL-DIGEST-MISMATCH|MISSING_PROVENANCE|TOOL_SHA256`,
   `^LANE_TIP |^MINTED_BY ` over all 20 sibling roots with `gitignore:false`).
3. **Caveat A (method-changing):** a fleet-root scan does not reach nested lane trees. The
   fleet-wide `LANE_TIP|TOOL_SHA|MINTED_BY` scan returned only the fleet's own
   `.ufo/reports/`, `MANIFEST.json` and `waves/hyaku` bytes (41 files, all fleet-root), while the
   same pattern inside `mado-shokunin` matches thousands of tracked files
   (`git -C mado-shokunin ls-files .ufo | wc -l` → 33955). The lanes are nested git repos; every
   sibling claim below was therefore re-verified **inside its own lane**, and tracked-ness with
   `git ls-files --error-unmatch` per file. A pattern scan of the fleet root alone would have
   (and here almost did) produced a false "no sibling implements stamps".
4. **Caveat B (tool):** glob path form `*-shokunin/**/*.py` silently matched nothing — pattern
   `receipt` over it returned "No matches found" while per-lane paths match thousands. Filed to
   `xd://report_issue`. Do not trust a zero from that path form.

## The R80-C1 standard (what siblings are compared against)

`plans/round80_c1_located_replay.py:60-62` — `REQUIRED = ("MEMBER", "SOURCE_RECEIPT", "SOURCE_SHA",
"TOOL", "TOOL_SHA", "LANE_TIP", "WORKTREE", "COMMAND", "EXIT", "MINTED_BY")`, plus subject line
`^# tb2 <member> grader probe` (`:61` SUBJECT), plus an `OBSERVATIONS_BEGIN/END` block that must
equal a fresh re-run of the frozen instrument at the measured tree (REV lines excluded), plus the
ledger row `executed / subject=tb2-header / round=80`. Verified in minted bytes at tip —
`corpus/evidence/round80/cancel-async-tasks-probe.txt:1-12` carries exactly: subject line, MEMBER,
SOURCE_RECEIPT+SOURCE_SHA, TOOL+TOOL_SHA, `LANE_TIP 6250e94b…` (an ancestor of the measured tip),
`WORKTREE clean`, COMMAND, `EXIT 0`, MINTED_BY, then CASE observation lines.

Kengaku's own lineage (for origin, no sibling involved): subject shape since round 35
(`plans/battery41/r_setup.py:93` plants `corpus/evidence/round35/tb2-grader-probe.txt`); stamp
grammar minted by `plans/round77_remint_r76_batteries.py` (fleet report
`.ufo/reports/round-77/kengaku.md:37` names LANE_TIP/TOOL_SHA/TOOL/WORKTREE/MINTED_BY/COMMAND/EXIT),
carried by `plans/round78_restamp.py:84-87` (adds the strip-so-exactly-one-stamp-governs rule), and
`plans/round80_c1_remint.py:132-143` (adds the OBSERVATIONS block, verbatim stdout minus REV).

## Matrix — lane → artifact → proves → overlap → route

| lane | artifact (tracked unless noted) | what it proves | overlap with R80-C1 | route |
|---|---|---|---|---|
| kengaku | `plans/round78_restamp.py:84-87` | receipts stamped LANE_TIP/TOOL/TOOL_SHA/WORKTREE/COMMAND/MINTED_BY/EXIT, one block governs | direct ancestor of the C1 stamp block; already emits MINTED_BY | none (own lineage) |
| kengaku | worktree `corpus/evidence/round80/r79-c1-after.txt` (untracked at measurement) | C2-V6 re-stamp of the round-79 after receipt at tip, full grammar incl. `MINTED_BY plans/round78_restamp.py sha256=15157a4c…` | the two claims' receipts already share one grammar | none — L1 lands it |
| souji | `tools/souji-receipt-run.py` — header `receipt=v1 rev= tool= tool_sha256= cmd= rc= utc=` + stdout/stderr fences (spec `.ufo/waves/round-23/make-spec.py:353-355`); `verify` `:334`, digest recompute `:177`, refusal `:352-353`, durable-ref check `:170-174, :356-358` | a receipt whose recorded tool digest is not the blob **at the receipt's own rev** is refused (`RECEIPT-TOOL-DIGEST-MISMATCH`), rev must be reachable from refs/heads\|tags\|remotes | TOOL_SHA-recompute leg ≈ identical mechanism; durable-rev ≈ LANE_TIP-reachable; cmd/rc ≈ COMMAND/EXIT. Missing: subject identity, WORKTREE, and any **reproduction** leg (stdout recorded, never re-run) | cite |
| mado | `.ufo/waves/round-18/receipt-check.py` — claim classes `:14-15`; MISSING_PROVENANCE `:126-127`; PRODUCER_MISMATCH `:128-129`; NOT_ANCESTOR `:27-29`; SHA_MISMATCH `:149-152`; STALE `:32-37` | every measurement receipt binds its producer tool to the revision the claim reads it at; tool_sha256 recomputed from `git show <measured_commit>:<tool>` | LANE_TIP-ancestor ≈ NOT_ANCESTOR; TOOL_SHA ≈ SHA_MISMATCH; producer identity has **no C1 counterpart** (C1 binds subject, not producer, beyond MINTED_BY). Evidence receipts (`round-14/evidence/after.txt:1-5`) carry command/measured_commit/gate_sha256/exit/stdout. Missing: subject stamp, reproduction | cite |
| tameshi | `.ufo/evidence/round-15/verify.py:110-119` — `PIN_TOOL_SHA256` + `PIN_MAINTAINED_TOOL_SHA256` ("the moved digest is appended, the round-15 blob pin above is untouched") | append-only instrument re-pinning: a moved tool digest is appended, never edited | the pin-discipline analog of R80-C2's append-only re-stamp; nothing C1 lacks | cite |
| kake | `.ufo/waves/round-77/controls/r77-hreflang-matrix.txt:44-50` | `tool_sha256=0762452f…` **equal to the blob at** `revision=a2cc5f51…` (`git cat-file -e` at `:14`), `revision_ok=yes head=…`, and named per-case `expected=/observed=/verdict=` lines; `:27-31` explicitly distinguishes "commit exists" from "tool exists at it" | outside kengaku, the only sibling receipt that pairs tool-digest-at-a-revision with observation cases — independent convergence on the round-78 flip | cite |
| kama | `.ufo/waves/round-29/repairs/echo-exit2/receipt.txt:2-6` | lowercase variant stamp: `tool_sha256 <sha>`, `lane_tip <sha>`, date, sentinel digests | partial: tool digest + lane tip, no MINTED_BY/WORKTREE/COMMAND/EXIT, no replay | cite |
| souji (2nd) | sentinel fixture `.ufo/waves/round-41/w2/R41w2sentinel01/driver/attack_freeze_check.py:21-22` | constants TOOL_SHA/LANE_TIP in an attack fixture | fixture, not a standard | none |
| chousa, kotodama, tsukuroi | e.g. chousa r68 `TOOL_SHA256` re-pin discipline, kotodama `claims.json` tool_sha256 pins, tsukuroi r41 frozen counter sha = receipt tool_sha256 (fleet `MANIFEST.json` rechecks fields) | instrument-pin class only; no receipt-stamp gate, no subject stamp, no replay | TOOL_SHA leg only | none |
| all other lanes (audio, game-dev-2d/3d, kagi, kaidoku, kaidoku-side kumitate, lore, mori, revenger, tabi, kotoba, kumitate, kasegi) | — | no located-receipt or subject-stamp standard found in tracked trees (`^LANE_TIP \|^MINTED_BY ` over all 20 sibling roots → only the rows above) | — | none |

**Contradiction stated plainly:** no sibling implements the R80-C1 standard's two decisive legs —
the **subject stamp** (`# tb2 <member> grader probe` naming *what* was measured) and the
**reproduction leg** (block equals a fresh re-run). Souji's own round-23 critic proved the ceiling
of digest-only receipts: a hand-forged receipt with a *correct* digest and impossible stdout
verifies `ok` (`.ufo/waves/round-23/w1/CritC2Value.md:158-161`, attack A1). R80-C1's replay leg
closes exactly that class; nothing in the fleet already had it.

## Report-out candidates (3, exact file:line)

1. `souji-shokunin/tools/souji-receipt-run.py:352-353` — `verify` recomputes
   `sha256(git cat-file blob <rev>:<tool>)` and refuses with `RECEIPT-TOOL-DIGEST-MISMATCH`
   (`verify=ok` at `:368`; durable-ref precondition `:170-174, :356-358`). It is generic
   (`--root <any repo>`, lane-relative tool path) and tracked — any lane can point it at its own
   receipts today. Report-out to lanes that still cite digest-less evidence receipts.
2. `mado-shokunin/.ufo/waves/round-18/receipt-check.py:14-15,149-152` — a reusable claim→receipt
   checker returning `MISSING_PROVENANCE / SHA_MISMATCH / STALE / NOT_ANCESTOR /
   PRODUCER_MISMATCH`; report-out as prior art wherever a spot-check hand-verifies those five
   properties (several lanes' verifier rechecks in fleet `MANIFEST.json` do exactly this by hand).
3. `kake-shokunin/.ufo/waves/round-77/controls/r77-hreflang-matrix.txt:27-31,44-50` — independent
   convergence on "tool digest equal to the blob at the named revision + named observation cases",
   reached during kake's own round-77 D1 repair. Report-out as evidence the R80-C1 shape is
   reachable outside kengaku without importing kengaku bytes.

## What kengaku must NOT absorb

1. **Souji's receipt-rev digest semantics.** R80-C1 recomputes TOOL_SHA **at the measured tip**;
   souji recomputes **at the receipt's own rev**. Swapping semantics would redefine the frozen
   predicate after data (freeze amendment `6250e94b` already fixed the block as verbatim stdout).
   Likewise souji's typed-string counter (`grep -rlE '^tool_sha256=…' census/ | wc -l`) must never
   replace the replay gate — it is the counted-as-capability-string anti-pattern souji's own
   critic named.
2. **Mado's free-form provenance spellings.** `receipt-check.py:60-67` accepts
   `tool=`, `tool_sha256:`, `"tool_sha256":` tokens *anywhere in the text*. R80-C1's stamp is a
   strict line-oriented block (`STAMP_RE ^([A-Z_]+) (.+)$`); loosening to anywhere-in-text would be
   precisely the weakening the `--mutants` battery kills.
3. **Tameshi's dual PIN_* constants.** `PIN_MAINTAINED_TOOL_SHA256`-style "which digest governs"
   forks have no place in the C1 counter: one REQUIRED tuple, one governing digest per stamp.
   Also: kengaku must not absorb any sibling receipt-runner as a second minting path — both round-80
   mint drivers (`plans/round80_c1_remint.py`, `plans/round78_restamp.py`) are already
   MINTED_BY-attributed and tracked; a third would be an unattributed writer.

## Proposed move (one, bounded — routed, not executed)

**Synthesis already true in bytes; name the remaining leg.** Round 80's two claims mint receipts
through two drivers, and the bytes show one grammar: C1 probes
(`corpus/evidence/round80/cancel-async-tasks-probe.txt:1-12`, tracked) and C2's re-stamped round-79
receipts (worktree `r79-c1-after.txt:1-6`) both carry LANE_TIP/TOOL/TOOL_SHA/WORKTREE/COMMAND/
MINTED_BY/EXIT. The asymmetry left is **reproduction**: only C1 receipts carry an OBSERVATIONS
block that must equal a fresh re-run. Move for round 81 (this round's predicates are frozen — zero
round-80 bytes change): give the C2 debt counter an optional replay leg that re-runs a re-stamped
receipt's COMMAND at its stamped LANE_TIP and compares observation lines under C1's REV-excluded
rule, with a mutant ("COMMAND replay diverges") added to the battery. Improves calibration (V6's
stampless-receipt class dies at the mechanism level, not per receipt); harms nothing — coverage
untouched, C1 counter untouched.

Risks: the C2 after-receipts' COMMANDs run a population gate whose counts legitimately move as the
ledger grows (a naive equality would false-red); the comparison must reuse C1's observation-form
whitelist (`^CASE |^case=|^cases=|^MISMATCH |^OBSERVED-U |^VECTOR |^PREDICATE R<n>-C<m>`) and
compare only stable forms, or pin `--rev` at the stamped tip. Verification: `--selftest` green
fixture + the new mutant killed + `--control-presence` still loses ×6+×6 before any data.

## Failures observed (exact commands and outputs)

1. `grep` tool, path `/home/vgpnk/Projects/shokunin/*-shokunin/**/*.py`, pattern `receipt`,
   gitignore true → `No matches found` (per-lane paths match thousands of files). Filed to
   `xd://report_issue`.
2. `read mado-shokunin/.ufo/waves/round-14/receipt.py` → `Path … not found`. Resolution: the file
   name appears only as a round-14 `dispatch.json` task description (`ReceiptBuild`); the landed,
   tracked checker is `.ufo/waves/round-18/receipt-check.py`. Cited accordingly.
3. `git -C souji-shokunin ls-files --error-unmatch census/round-23/records/gate-check-after.tsv`
   → rc≠0 (not in the index); the tracked round-23 receipt set names
   `gate-check-at-first-landing.tsv` instead (`git -C souji-shokunin ls-files
   census/round-23/records/ | head` → `agreement-after.tsv`, `…gate-check-at-first-landing.tsv`,
   …). Round-23 report prose cites the `-after` name; any kengaku citation must use the tracked
   name only.

## Tooling, scratch, adjacency

- Tool installs/upgrades: none. Pacman untouched (host-wide pause respected). No RULES.md channels used.
- Scratch: none needed — no fixture repo and no clone was required; all evidence is read-only
  `git`/`read`/`grep` over existing worktrees and indices. Nothing to clean.
- Adjacency: this seat wrote only `.ufo/waves/round-80/w1/ConnectorR80.md`; no sibling lane, plan,
  gate, corpus file or counter was read-modified, and no sibling scope is absorbed into kengaku
  (every sibling row above routes to cite/report-out/none; `Assimilation` remains governed by the
  open L0 `kengaku | round-54`).
