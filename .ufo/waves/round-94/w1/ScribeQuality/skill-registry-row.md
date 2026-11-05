# ScribeQuality — draft SKILL.md gate-registry row (freeze-integrity, v2)

Seat ScribeQuality (leaf scribe). Draft only; the L1 integrates into `SKILL.md`. Nothing here
is committed; the lane was read-only.

## Where the row goes and what shape it takes

`SKILL.md:592` holds `## Gate/probe registry (PROTOCOL §Gate standard)` and `SKILL.md:594`
the table header:

```
| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
```

Eight columns, ten pipe-separated cells per row (`| a | b | c | d | e | f | g | h |` splits
into 10 with the empty first and last). The proposed row below uses exactly those eight
columns and that shape.

## Proposed row

```
| `freeze-integrity` | gate | `python3 plans/round94_freeze_integrity.py --lane . --freeze F --rev T (--claims plans/round-N-claims.md \| --paths P ...) --work DIR` (v2, round 94 — current; v1 `plans/round93_freeze_integrity.py` superseded: default history simplification and first-block-only parsing) | `0` every tabled instrument intact and the battery green (`PREDICATE freeze-integrity pass`) · `1` a breach (`INSTRUMENT <path> … verdict=broken:<reasons>`) or a red battery case · `2` could-not-evaluate (`DEFECT SETUP <reason>` then `PREDICATE freeze-integrity could-not-evaluate`): unresolved revision, freeze not an ancestor of --rev, claims file absent at the freeze, table absent/empty/unterminated, more than one `frozen-instruments` block, malformed table row, duplicate table path, path absent at the freeze, no `--paths` given, duplicate `--paths`, `rev-list` failed, or exactly one of `--claims`/`--paths` required (argparse usage errors also exit 2) | in-process battery, no flag: every invocation prints `BATTERY B01…B15` lines and `SELFTEST cases=15 ok=15` (no `--selftest` flag exists — argparse rejects it, rc 2; no skip channel, no marker file, no child re-entry). The two rc-2 paths that fail before the battery (argparse usage error; `--claims` and `--paths` both or neither given) print no `SELFTEST` line, so `SELFTEST cases=15 ok=15` appears only on a run that reaches the battery — the round-94 counter's W3 leg requires exactly that string | the claims file's ```` ```frozen-instruments ```` block read at --freeze (sha256 per path; one block only, duplicate paths refused); judged by `plans/round94_c2_counter.py` (W1–W5; CLI-path mutants K1–K7, the unmutated CLI copy keeps all 12 W2 fixtures) | read-only on the lane (git plumbing: `rev-parse`, `show`, `rev-list --full-history`, `merge-base`); writes only under `--work` — fixture repos there, and the battery dir is removed afterwards. An empty `--work` *inside* the lane is not refused and is left behind, but no tracked file changes (git status stays clean) | kengaku |
```

## Column-by-column, with the source of every claim

**name** — `freeze-integrity`. No name collision: the table already has `anchor-line-check`
(`SKILL.md:682`), `anchor-digest-check` (`:612`) and `gate-timing` (`:601`), but nothing named
`freeze-integrity`; `grep -c "freeze-integrity" SKILL.md` = 1 (this row) at the tip.

**kind** — `gate`. The tool's own exit map is 0/1/2 and it is registered as a gate in the
same table as `anchor-line-check`.

**entry** — the argparse surface, read from `plans/round94_freeze_integrity.py:main`:
`--lane` (default `.`), `--freeze` (required), `--rev` (required), `--claims`, `--paths`
(nargs `+`), `--work` (required). Exactly one of `--claims`/`--paths` is required; supplying
both or neither is rc 2 (`DEFECT SETUP exactly one of --claims/--paths is required`).
The v1 naming follows the item: v2 `plans/round94_freeze_integrity.py` is current, v1
`plans/round93_freeze_integrity.py` is superseded. v1's two named defects are read from v1's
own bytes, not from the round-93 lesson: `plans/round93_freeze_integrity.py:110` uses
`git rev-list {f}..{t} -- {p}` with no `--full-history` (default history simplification), and
v1's `parse_table` `break`s at the first closing fence (first block only) and has no
duplicate-path check.

**verdict map** — from v2's `main` and `evaluate`. Exit 0 requires `not broken and
bat_ok == len(bat)`. Exit 1 is a broken instrument (`INSTRUMENT <path> … verdict=broken:<reasons>`)
or a red battery case. Exit 2 is every `CouldNotEvaluate` the code raises plus argparse's own
usage exit; the full list is enumerated in the cell so a reader can map a printed
`DEFECT SETUP` line to a cause.

**self-test** — the spelling is the in-process battery, not a flag: `plans/round94_freeze_integrity.py:326-327`
prints one `BATTERY <id> ok|RED got=…` line per case and then `SELFTEST cases=15 ok=15`.
`--selftest` does not exist (argparse: `unrecognized arguments: --selftest`, rc 2 — measured).
Two rc-2 paths return before the battery runs and therefore print no `SELFTEST` line
(measured): argparse usage error, and `--claims`+`--paths` both/neither. `plans/round94_c2_counter.py`
pins the exact string `SELFTEST cases=15 ok=15` (its `SELFTEST` constant) and echoes it in
W3, so the row states where the string is guaranteed.

**pinned values** — the gate's input is the claims file's `frozen-instruments` table read at
`--freeze`, one sha256 per path; v2 refuses a second block, an unterminated block and a
duplicate path. The judge is `plans/round94_c2_counter.py` (W1–W5, CLI-path mutants K1–K7,
null copy keeps 12/12).

**write scope** — v2 issues only read-only git plumbing and creates fixture repos under
`--work`; `shutil.rmtree` removes the battery dir in a `finally`. It does **not** refuse a
`--work` inside the lane the way several other lane counters do (e.g. `round38-c1` "refused
inside the lane"); measured: `--work ./inlane` inside a lane clone leaves an empty `inlane/`
directory and `git status --porcelain` stays empty (no tracked file changes).

**owner** — `kengaku` (the lane's owner, as in every other row of this table).

## Sibling overlap the L1 must resolve — the row already exists, uncommitted

The lane's working tree **already carries an uncommitted `freeze-integrity` row** at
`SKILL.md:698` (`git status` shows ` M SKILL.md`; `git show d04e6664:SKILL.md` has no such
row), written at 19:04:37, i.e. right after the w1 dispatch commit `d04e6664` (19:04:13).
`SCORECARD.md` likewise carries an uncommitted `freeze-integrity gate` capabilities row
(`git diff SCORECARD.md`, +1 line) — the two carried round-93 closure conformance items the
round-94 claims file names ("SKILL.md registry row, `## Capabilities` row"). So the L1 is
already writing this row itself, and my seat was asked to draft it too. This draft is
therefore a **review of the L1's row**, with the differences below; the L1 keeps its row.

Measured differences between the L1's working-tree row (SKILL.md:698) and the draft above:

1. **"printed on every run"** (L1, self-test cell) is not literally true: the two rc-2 paths
   that return before the battery print no `SELFTEST` line (measured; `receipt-inlane-workdir.txt`
   and the run above). The draft states the exception. This is a wording precision, not a
   verdict change — the counter's W3 leg exercises a normal run, where the string is present.
2. **rc-2 cause list** (L1, verdict-map cell) omits five causes the code raises:
   `claims file … absent at freeze`, `malformed table row`, `no paths given`,
   `duplicate --paths`, `rev-list failed`, and argparse's own usage exit. The draft lists
   them; every one was reproduced (see `receipt-rc2-causes.txt`).
3. **write scope** (L1): "none in the lane — read-only git; fixture repos only under `--work`"
   is true of the lane's *tracked bytes* but not of the filesystem: an empty `--work`
   directory inside the lane is left behind (the gate does not refuse an in-lane `--work`).
   The draft says so.
4. **placement**: the L1's row sits at `SKILL.md:698`, the last line of the *first* table
   block (the committed file has a blank line at 698 separating the round-68 block from the
   round-71…89 block that ends at `SKILL.md:759` with `round89-claim-figures`). Appending
   after `:759` puts the round-94 row at the end of the whole registry, which is where the
   chronological ordering of the second block puts it. Cosmetic; the L1's choice.
5. The L1's row's four-backtick fence spelling
   (`` ```` ```frozen-instruments ```` ``) is valid CommonMark: a 4-backtick code span whose
   content is ` ```frozen-instruments ` with the one leading and one trailing space stripped.
   It renders as intended; no change needed.

## Bound on this draft

A registry row says how to run an instrument and what its exits mean. It asserts nothing
about a round's verdict; the verdict lives in the round's claims file and its receipts. The
row names v2 as current and v1 as superseded, which is a statement about the lane's
instruments, not about R94-C1 or R94-C2.
