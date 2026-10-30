# Root cause — why `round35-c1-coverage`'s declared V4 fragment stopped matching

Seat: RV2Round35Fragment (round 55, wave 1, read-only). Lane head at measurement: `80afa613` (freeze); base tip `798f5e9e`.

## Verdict

1. **The V4 output wording never changed.** `plans/round35_c1_verify.py` has one history: it was added in `11d64530` (round-35 freeze) and nothing after it touches the file. The blob is identical in every commit that carries it:
   `97431502b94ab84d905916e64c05468508d46d57` (`11d64530`; `70c25a66`, `ffb6a42e`, `975bf2a6` are `refs/jj/keep/*` copies of the same freeze, not ancestors of HEAD). `git diff HEAD -- plans/round35_c1_verify.py` is empty. The premise "revisions touching the V4 output wording after the ledger was built" has no instance.
2. **What broke the fragment is the corpus, not the script.** V4 prints live counts and compares them to a constant frozen at round 35:
   ```
   plans/round35_c1_verify.py (added 11d64530, unchanged at HEAD), lines 154-155 at 11d64530:
   +    if not (len(files) == nidx == 42):
   +        return f"knowledge files={len(files)} index rows={nidx} (want 42/42)"
   ```
   Every knowledge entry landed after round 35 changes the printed numbers, so any fragment that quotes the numbers decays at the next knowledge commit.
3. **Truth vs wording.** The row's TRUE verdict changed exactly once, at round 36: green (exit 0) through `1d4084fa`, red (exit 1) from `805fe790`. Since round 36 the exit/state has been constant red (exit 1). The fragment's break at round 54 changed only the embedded numbers: verdict wording-only at that step. The round-36 step was a truth change (green→red), caused by the new knowledge file, not by wording.

## Causal chain

| step | commit (round) | knowledge `.md` count | V4 output (scripted) | effect |
|---|---|---|---|---|
| entry admitted | `4fe72a9a` (r35) | 42 | `V4 ok` | green |
| errata | `1d4084fa` (r35) | 42 | `V4 ok` | green |
| wave-1 integrate adds `corpus/knowledge/tb2-regex-log-grader.md` (+264) | `805fe790` (r36) | 43 | `V4 DEFECT knowledge files=43 index rows=43 (want 42/42)` | **first red: truth change** |
| r51 surface truth | `11e79380` / `30801b47` (r51) | 55 / 54 | `V4 DEFECT knowledge files=55 index rows=54 (want 42/42)` | red |
| r54 ledger measured at freeze tip | `6e0a1915` (r54) | 57 | `V4 DEFECT knowledge files=57 index rows=57 (want 42/42)` | the fragment copied into `plans/round54-entrytruth.json` |
| r54 retention commit adds `corpus/knowledge/external-anchor-freeze.md` (+42) | `9a0746be` (r54) | 57 → **58** | `V4 DEFECT knowledge files=58 index rows=58 (want 42/42)` | **declared fragment stops matching** |
| base tip / HEAD | `798f5e9e` / `80afa613` | 58 | `V4 DEFECT knowledge files=58 index rows=58 (want 42/42)` | red, exit 1 |

Counts for the intermediate revisions (43 through 56) come from `git ls-tree` per commit (`corpus/knowledge/*.md`) and the knowledge index rows in `corpus/README.md`; the eight rows marked scripted were produced by calling `v4()` from the file itself in a scratch clone.

## The declared fragments

| ledger | fragment declared | matches HEAD output? |
|---|---|---|
| `SKILL.md:623` registry cell (round 52) | "knowledge files == index rows == 42 — **stale: measured 55 files / 54 index rows at the base tip `30801b47` and at HEAD**" | cell's "at HEAD" claim is now false (HEAD = 58/58). Stale text, not a fragment match. |
| `plans/round53-tipstate.json` | `(want 42/42)` | **yes** (substring). Never stops matching: it matches any V4 red output, so it is a weak fragment. |
| `plans/round54-entrytruth.json` | `V4 DEFECT knowledge files=57 index rows=57 (want 42/42)` | **no.** `plans/round54_c2_entrytruth.py:338` tests `sp.get("evidence") not in r["out"]` (substring). Direct evaluation at HEAD: `"V4 DEFECT knowledge files=57 index rows=57 (want 42/42)" in "V4 DEFECT knowledge files=58 index rows=58 (want 42/42)"` → `False`. The round-54 counter would therefore report this row as `evidence_missing`. Not run end-to-end here (full counter executes all 78 rows). |

Note also: `W2RevRowsB.md` (round 52) paraphrases the round-35 output as `V4 DEFECT 55/54`; the verbatim output at that revision was `knowledge files=55 index rows=54 (want 42/42)`.

## Implication for round 55 (no edit made; reported for L1)

- R55-C2 (a) re-derives this row's fragment at the measured-after revision. Round 55's own C3 adds `corpus/knowledge/tb2-chess-best-move-grader.md`, which moves the counts again (58 → 59). A fragment taken before the C3 landing will be stale after it. The correction must be taken at the final measured-after revision.
- The V4 constant `42` is frozen; the round-55 rules forbid changing predicates mid-round. Recommend keeping the fragment as data only, and recording in the row that it decays with each knowledge commit.
- Defect for L1: `SKILL.md:623` says "measured 55 / 54 ... at HEAD", which is false at HEAD. Not edited by this seat.

## Confidence

High on the single-history / blob-identity claim (direct `git` evidence). High on the transition points (scripted V4 at 8 revisions + per-commit counts). High on the substring-mismatch mechanism (read from `round54_c2_entrytruth.py:338`). Medium on "the r54 counter would flag it": inferred from the predicate, not executed.

## Dead ends

- `git log -- plans/round35_c1_verify.py` (no `--all`) already shows the single commit; `--all`/`--follow`/`-S"V4"` only added the three jj-keep copies. No V4 wording revision exists in any ref.
- The full `plans/round35_c1_verify.py --lane` run was not used: V5 would invoke `uv run --with biopython` (network) and V6 the fleet census. V4 was exercised alone via `importlib`.
