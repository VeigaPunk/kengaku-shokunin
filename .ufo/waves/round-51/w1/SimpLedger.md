# SimpLedger — which routed-ledger fields are dead weight

Seat: simplifier, kengaku round 51 wave 1 (hyaku run 11). Item: count per-field non-trivial use
over `corpus/routed-findings.jsonl`, decide keep/remove with the count as evidence, propose the
minimal row schema that still supports the C2 predicate. **The ledger was not edited.**

Axes named: **adjacency** (R51-C2, the axis this evidence serves). Not claimed or touched by this
seat: freshness (R51-C1), and every other axis. I judged no claim and ran neither counter's
scoring path.

Revision measured — the ledger bytes are the round-46 blob:

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7        (lane HEAD at measurement)
blob 2e819d7aa175137a43129edba932c3f853a51574      (HEAD:corpus/routed-findings.jsonl)
last-touch 85a40be 2026-10-27 02:42:51 -0300 round-46: … routed ledger rows …
sha256 39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d  corpus/routed-findings.jsonl
71 rows, 48957 bytes
```

`git status --porcelain corpus/ plans/ PROVINCE.md SCORECARD.md LOG.md SKILL.md` at the end of the
seat: empty (no lane write by this seat).

## 1. Commands run (all read-only against the lane)

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && git rev-parse HEAD
git rev-parse HEAD:corpus/routed-findings.jsonl
git log -1 --format='last-touch %h %ad %s' --date=iso -- corpus/routed-findings.jsonl
wc -lc corpus/routed-findings.jsonl ; sha256sum corpus/routed-findings.jsonl
cat .ufo/waves/round-51/claims/c2-before.txt
# per-field census, byte census, id/round redundancy, close-token taxonomy: python3 stdlib
#   (json + re + git cat-file -e) over corpus/routed-findings.jsonl, cwd = lane root
# per-field ablation + patched-counter experiment: python3 plans/round51_routing.py
#   --lane <scratch fixture> --scratch <scratch>   (13 + 6 cases; fixture lane built in scratch)
# consumer search: grep over plans/ for opened_round|blocker|routed-findings and get("note")
```

The frozen C2 before-receipt is reproduced verbatim here as the baseline this schema must move:

```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
PREDICATE R51-C2 fail
```

(`SOURCES resolved=71 missing=0` is the one field already fully load-bearing; `CLOSE_REFS
resolved=0` is vacuous, not a measurement — no row carries a disposition yet, so the counter's
denominator is `sum(fixed-historical)=0`.)

## 2. Field census — 71 rows

"non-trivial" = the field carries a value that says something (`null`/`""`/absent = trivial), per
the item's definition. "bytes" = `len(json.dumps(value))` summed over rows, so it is the field's
share of the 48957-byte file.

| field | non-trivial rows | distinct | bytes | share | machine consumer that reads the value |
|---|---|---|---|---|---|
| `id` | 71 | 71 (unique) | 724 | 1.5% | C2 detail lines (`rid`); `routed_open.py` duplicate-id guard |
| `class` | 71 | 64 (58 singletons) | 1774 | 3.6% | **none reads it**: C2 = key presence only; `routed_open.py:84-85` = non-empty-string only. Human tables only (r43/r44 wave reports print `id \| class \| source \| verdict`) |
| `source` | 71 | 67 | 3505 | 7.2% | C2 `SOURCE` (path must exist); `routed_open.py:57-69` (`<path>:<line>` must resolve to a non-blank line) |
| `opened_round` | 71 | 4 (`39,40,42,45`) | 142 | 0.3% | `routed_open.py:134` → `oldest_round=` in the round-close line. **Redundant**: the `id` prefix reproduces it on 71/71 rows (`R39-`,`R40-`,`R42-`,`R45-`) |
| `status` | 71 | 4 (`closed 41, open 27, refused 2, blocked 1`) | 517 | 1.1% | both tools (`routed_open.py:132-136`; C2 `STATUSES`) |
| `close` | 41 (= every `closed` row; 0 of 30 non-closed) | 29 | 6633 | 13.5% | C2 `CLOSE_REF` for `fixed-historical`; `routed_open.py:100-101` requires it when `closed` |
| `blocker` | 3 (exactly the 1 `blocked` + 2 `refused` rows) | 3 | 961 | 2.0% | `routed_open.py:102-103` requires it when `blocked`/`refused`; C2 never reads it |
| `check` | 61 (10 `null`, all `open`) | 61 | 6124 | 12.5% | C2 `CHECK` + `CHECK_FAILED`; `routed_open.py --observe` |
| `note` | 59 | 59 | 21066 | **43.0%** | **none reads it**: C2 = key presence only; `routed_open.py:107-109` = type check only (`isinstance(note, str)`). Grep for `get("note")` in `plans/` returns `routed_open.py:107` and an unrelated fixture module |
| `owner` | 0 | 0 | 0 | 0% | C2 `OWNER` — absent from all 71 rows (the axis gap) |
| `disposition` | 0 | 0 | 0 | 0% | C2 `DISPOSITION` — absent from all 71 rows |
| `next` | 0 | 0 | 0 | 0% | C2 `NEXT` — absent; required only for `routed`/`referral` |

Cross-field structure that decides the `note`/`close`/`blocker` split:

```
close&note 29 | close only 12 | note only 30 | neither 0
note-only rows = the 27 open + 2 refused + 1 blocked rows, exactly
blocker rows also carry note: 3/3
note/close textual containment (one inside the other): 0
```

So `note` is not duplicated prose: for the 30 non-closed rows it is the **only** prose, and it is
never a restatement of `close`.

## 3. Ablation — what the frozen C2 counter actually requires

Each case is a one-row fixture lane in scratch (`fix/lane/corpus/lessons/x.md` + `fix/shokunin.conf`),
run as `python3 plans/round51_routing.py --lane <fixture> --scratch <fixture>/work`. Verbatim:

```
baseline(all 11)           rc=0 PREDICATE R51-C2 pass
drop id                    rc=1   DETAIL FIELDS ? missing id | PREDICATE R51-C2 fail
drop class                 rc=1   DETAIL FIELDS R1 missing class | PREDICATE R51-C2 fail
drop source                rc=1   DETAIL FIELDS R1 missing source |   DETAIL SOURCE R1 source None does not resolve
drop opened_round          rc=1   DETAIL FIELDS R1 missing opened_round | PREDICATE R51-C2 fail
drop status                rc=1   DETAIL FIELDS R1 missing status |   DETAIL DISPOSITION R1 status None not in ['blocked', 'closed', 'open', 'refused']
drop owner                 rc=1   DETAIL FIELDS R1 missing owner |   DETAIL OWNER R1 has no owner
drop disposition           rc=1   DETAIL FIELDS R1 missing disposition |   DETAIL DISPOSITION R1 has no disposition
drop close                 rc=1   DETAIL FIELDS R1 missing close | PREDICATE R51-C2 fail
drop blocker               rc=1   DETAIL FIELDS R1 missing blocker | PREDICATE R51-C2 fail
drop check                 rc=1   DETAIL FIELDS R1 missing check |   DETAIL CHECK R1 has no check command
drop note                  rc=1   DETAIL FIELDS R1 missing note | PREDICATE R51-C2 fail
minimal(read-only set)     rc=1   DETAIL FIELDS R1 missing class,opened_round,close,blocker,note | PREDICATE R51-C2 fail
minimal+placeholders       rc=0 PREDICATE R51-C2 pass
```

`minimal(read-only set)` = `{id, source, status, owner, disposition, check}` — the only six keys the
counter reads **by value** for a `fixed-verified` row. `minimal+placeholders` adds
`class, opened_round, close, blocker, note` and passes, i.e. **for those five the counter checks
presence and nothing else** (`round51_routing.py:38-39` `FIELDS`, presence check `:91`). Reading the code
confirms it: `close` is read only under `disposition == "fixed-historical"` (`:132-145`), `next` only
under `routed|referral` (`:113-117`), `class`/`opened_round`/`blocker`/`note` are never read at all.

Proof that the two zero-consumer fields cost no predicate power — a scratch copy of the counter with
`FIELDS` trimmed to `(id, source, status, owner, disposition, close, blocker, check)`, run against a
3-row fixture that exercises the closed / open / routed+refused branches:

```
3-row full schema, frozen counter  rc=0 :: FIELDS complete=3 incomplete=0 | PREDICATE R51-C2 pass
3-row minus class+note, frozen     rc=1 :: FIELDS complete=0 incomplete=3 |   DETAIL FIELDS A missing class,note |   DETAIL FIELDS B missing class,note |   DETAIL FIELDS C missing class,note | PREDICATE R51-C2 fail
3-row minus class+note, patched    rc=0 :: FIELDS complete=3 incomplete=0 | PREDICATE R51-C2 pass
minus class only, patched          rc=0 :: FIELDS complete=3 incomplete=0 | PREDICATE R51-C2 pass
minus note only, patched           rc=0 :: FIELDS complete=3 incomplete=0 | PREDICATE R51-C2 pass
```

The trimmed `FIELDS` keeps `close`/`blocker` because `routed_open.py` requires them conditionally;
`class` and `note` are the only two whose removal changes no verdict.

## 4. Decisions — keep/remove, with the count as the reason

| field | decision | evidence |
|---|---|---|
| `id` | **keep** | 71/71 unique; the only per-row identity and the `routed_open.py` dedup key (`:82-83`); costs 1.5% of bytes |
| `class` | **keep as a human label; drop from C2 `FIELDS` in a successor counter** | value never read by any tool (ablation + code); 64 distinct over 71 rows with 58 singletons means it does not even collapse rows into groups — it is a second id. It is, however, the second column of every routed-queue table (`.ufo/waves/round-43/build/R43RoutedQueue.md:46-48`, `.ufo/waves/round-44/wave/R44RoutedPlan.md:17-25`), so the data is not worthless, only the schema enforcement is |
| `source` | **keep** | 71/71 non-trivial, 67 distinct, and the only field already green in the before-receipt (`SOURCES resolved=71 missing=0`) |
| `opened_round` | **keep** (derived) | 4 distinct values, 142 bytes; live consumer `routed_open.py:134` prints `oldest_round`. It is 100% derivable from the `id` prefix, but deleting it would force `routed_open.py` to parse ids — coupling worse than the duplication. Keep it, and let C2 stop enforcing presence if it ever trims |
| `status` | **keep** | both tools branch on it; 4 frozen values, 517 bytes |
| `close` | **keep, and normalize it** | 41/41 of the closed rows carry it and 0 of the 30 non-closed do — the invariant is exact. But see §5: only 18 of 41 are machine-resolvable as written |
| `blocker` | **keep** (conditional) | 3/3 non-null rows are exactly the blocked/refused rows; `routed_open.py` requires it there and rejects a blocked row without one (`--selftest` case `blocked-without-blocker`) |
| `check` | **keep — this is the axis** | 61 present, 10 absent; C2 demands non-empty on all 71, so the landing must add 10 checks (ids in §5) or attribute those rows non-`fixed-verified` |
| `note` | **keep, but it is prose, not schema** | 59 rows, **43.0% of the file**, and **the only field no consumer requires or reads** — C2 wants the key, `routed_open.py` type-checks it, nothing else touches it. Removing the *field* would strand the only prose of 30 rows; removing it from `FIELDS` loses zero predicate power. Recommendation: keep the key, stop treating it as schema |
| `owner` | **add (must)** | 0/71 present; the claim's whole signal. Adding `owner`+`disposition` to 71 rows costs ≥2911 bytes at minimal values (measured lower bound with 12-char values), against 22840 bytes that `class`+`note` occupy |
| `disposition` | **add (must)** | 0/71 present; 6 frozen values |
| `next` | **add (conditional)** | 0/71 present; bounded by the ≤30 rows that are not closed (27 open + 2 refused + 1 blocked), and only the `routed`/`referral` subset needs it |

Net: **no field is dead weight enough to delete this round**, and none can be deleted anyway — the
counter is frozen by `plans/round-51-claims.md` §C2 and the kill rule says rows are *re-attributed,
never deleted*. The one field that is dead weight **as schema** is `note` (43% of bytes, zero
consumers), followed by `class` (zero consumers, 58/64 singleton labels). Both are worth keeping as
row data and worth dropping from a successor counter's `FIELDS`.

## 5. Minimal row schema that still supports the C2 predicate

**C2-minimal (8 keys, 6 always + 2 conditional)** — proven to pass in §3 with the trimmed counter:

```json
{"id":"R45-S5-4","source":"corpus/lessons/round-46.md:12","status":"closed",
 "owner":"kengaku","disposition":"fixed-historical","check":"true",
 "close":"77ea425a corpus/lessons/round-46.md:12",
 "next":"round 52, kama"}
```

| key | when required | read by C2 as |
|---|---|---|
| `id` | always | message label only (and `routed_open.py` uniqueness) |
| `source` | always | must resolve on disk (`SOURCE`) |
| `status` | always | must be in `open|closed|refused|blocked` |
| `owner` | always | must be a fleet lane in `../shokunin.conf` or `unowned:integrator` |
| `disposition` | always | one of the 6 frozen values |
| `check` | always | non-empty; executed when `fixed-verified` |
| `close` | `disposition=fixed-historical` | first token must be a commit or a lane path |
| `next` | `disposition=routed|referral` | non-empty **and** owner ≠ `kengaku` |

Everything else — `class`, `opened_round`, `blocker`, `note` — is presence-only in C2. Adding them
back for the *other* live consumer (`plans/routed_open.py`, `REQUIRED` at `:43` = `id, class,
source, opened_round, status`, plus `close`-when-closed and `blocker`-when-blocked/refused) gives
the **union minimum of 11 keys + `next`**, which is exactly the current 11-field set plus `next`.
So the ledger's field list is already minimal for its two consumers; only `note` is carried by
neither.

## 6. Landing constraints these counts impose (adjacency, for the L1)

1. **10 rows cannot be `fixed-verified` without a new check** (all `open`, `check: null`):
   `R40-R5, R42-R3-09, R42-R3-33, R42-R3-34, R42-R3-35, R42-R3-37, R45-S5-7b, R45-S5-7c,
   R45-S5-7d, R45-S5-7e`. Either add a command or attribute them `routed`/`referral`/
   `accepted-risk`/`refused-out-of-scope` (each of those still needs an `owner`, and the first two
   need a `next`).
2. **23 of the 41 `closed` rows are not `CLOSE_REF`-ready as written.** Token taxonomy of
   `close.split()[0]`, measured with `git cat-file -e <tok>^{commit}` / path existence:

   ```
   hash-resolvable     14   e.g. R39-R1 'ec17216', R42-R2.2 '77ea425a'
   hash-dead            0
   path-resolvable      4   e.g. R42-R2.1 'plans/scratch_guard.py', R45-S5-4 'corpus/lessons/round-46.md'
   path-with-line       3   e.g. R40-R2 '.ufo/waves/round-41/build-spec.json:5'
   prose               20   e.g. R39-R5 'measured', R40-R1 'F1-F4'
   ```

   The counter's path branch is `(lane / tok).exists()` with **no `:line` stripping**
   (`round51_routing.py:143`), so a `path:line` first token fails even when the path exists —
   that is why `path-with-line` is its own bucket. A `fixed-historical` attribution therefore needs
   the `close` reworded to lead with a commit hash or a bare path, or a passing `check` (i.e.
   `fixed-verified`) instead.
3. **The 30 non-closed rows must keep their prose somewhere.** They have `close: null` and no
   `blocker` except the 3 blocked/refused ones, so `note` is the only place their state lives today.
   Any future schema that drops `note` must first give `open` rows a prose slot.
4. **`opened_round` is safe to keep even though it is derived**: `oldest_round` (the round-close
   line) reads it, and the `id` prefix reproduces it on 71/71 rows — a consistency check
   (`id` prefix == `opened_round`) would be cheap and is currently 71/71 clean.

## 7. Limits

- Counts are over the ledger at `4090c3db` (blob `2e819d7a`, last touched by `85a40be`). They are
  point-in-time; the wave's attribution will change the byte census and add three keys.
- "No consumer reads it" is a **text-search** result, not a semantic one: no language server answers
  for JSONL, so `grep` over `plans/` is the literal fallback and I record that unavailability. It
  covers the two tools that name the file (`routed_open.py`, `round51_routing.py`) and every
  `get("note")` in `plans/`; it does not prove no out-of-lane reader exists.
- I did not run `--run-checks` (that is the wave's check seats' work, and 71 × 60 s subprocesses is
  not this item); so "`check` present" is a presence count, not a green count.
- The trimmed-counter experiment used a scratch copy of the frozen instrument; it is a schema
  argument, not a proposal to edit `plans/round51_routing.py` (frozen this round).
- I did not decide any row's `owner`/`disposition`; the 3 `blocker` rows and the 10 check-less rows
  are listed as constraints, not attributed.
- Scratch `/fast/scratch/hyaku/kengaku-r51/SimpLedger` (36K: the two fixture lanes, `fix/` and
  `probe/`, plus the patched counter copy) was created for the experiments and removed before this
  seat yields — observed receipt: `after: ABSENT`; `test -e <scratch>` false, nothing left on disk.
  No `/tmp` path is cited as evidence anywhere in this report.

## 8. Verdict

Twelve fields measured over 71 rows. Seven carry machine-read values (`id, source, status, close,
blocker, check` + the conditional `next`), two must be added (`owner`, `disposition`), one is
derived-but-live (`opened_round`), and two are read by nothing (`class`, `note` — 46.6% of the file
between them). None is deletable this round: the frozen counter requires all 11 keys by presence
(proven by 11 ablations), and the kill rule forbids row deletion. The minimal schema that supports
C2 is 6 always-present keys plus 2 conditional ones; the union with the other live consumer
(`plans/routed_open.py`) is the current 11 plus `next`. The actionable simplification is not a
deletion but a demotion: stop enforcing `class` and `note` as schema in a successor counter, and
normalize `close` so that 23 of 41 closed rows become `CLOSE_REF`-resolvable.

VERDICT: schema-minimal-11-plus-next; dead-weight-as-schema = `note` (59 rows, 43.0% bytes, 0 consumers) and `class` (71 rows, 58/64 singleton, 0 consumers); keep-all-rows; 10 rows need a check, 23 need a `close` reword.
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
