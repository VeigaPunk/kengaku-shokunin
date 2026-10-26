# R42RoutedRider — routed-findings rows for round-41 closure R1–R5 (round 42, wave 1)

Executor seat. Scope: draft the rows to APPEND to `corpus/routed-findings.jsonl` for the round-41 closure routed
items R1–R5 (`corpus/lessons/round-41-verifier-spotcheck.md:105,110,114,116,117`) plus the legal status-change rows for
older findings, each measured at the lane tip by its own `check`. I wrote only
`.ufo/waves/round-42/build/R42RoutedRider/` (draft rows + run receipt) and
`/fast/scratch/hyaku/kengaku-r42/R42RoutedRider/` (two `--shared` clones). No lane file, no corpus/plans edit, no
commit, no pacman/uv install (nothing installed).

Measurement basis: lane tip **`fda71ae033224e1d0ed5ddd0fdcb1b63a02f2473`** (committed bytes). The worktree carries 28
untracked round-42 paths (S125–S127, `integrate/`, wave build reports), so "at the tip" below means the clone unless a
fact is explicitly marked *worktree-only*.

Envelope (Q32) for every run:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent
```

| run | start | end | `ls -A /home/vgpnk/.local/bin \| sha256sum` before → after |
|---|---|---|---|
| empty-ledger baseline (`--selftest`, `--observe`) | 17:23:20 | 17:23:58 | `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18  -` → same |
| appended-rows run (`--selftest`, summary, `--observe`) | 17:28:54 | 17:28:54 | `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18  -` → same |

Clone guard: `git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r42/R42RoutedRider/lane`; every
git call named `-C`. Receipt with the full transcript: `.ufo/waves/round-42/build/R42RoutedRider/ledger-run.txt`
(1883 B). Draft rows: `.ufo/waves/round-42/build/R42RoutedRider/appended-rows.jsonl` (7862 B, 6 rows).

## 1. What I measured before drafting

`python3 plans/routed_open.py --lane <clone> --observe` on the empty (unmodified) ledger:

```
OBSERVE R39-R2 rc=1 observed=fail self=open
OBSERVE R39-R3 rc=1 observed=fail self=blocked
OBSERVE R39-R4 rc=2 observed=fail self=open
OBSERVE R40-R1 self=open observed=n/a
OBSERVE R40-R5 self=open observed=n/a
OBSERVE rows=10 mismatched=0
ROWS total=10 open=4 blocked=1 closed=5 refused=0
routed_open=5 oldest_round=39
```

So the ledger's own state is consistent (no closed row whose check fails, no open row whose check passes). The only
older findings whose status this round can legally change are ones whose check now passes; none do. There is exactly
one finding whose *content* the round-42 freeze discharges — R40-R1 — and its base row cannot be edited, so it gets an
appended status row (§3).

Facts behind the five new rows, each with the command that produced it (`--lane <clone>`, tip `fda71ae0`):

| fact | command | output |
|---|---|---|
| C1 repairs a–e + attribution f frozen | `sed -n 15,34p plans/round42_c1_verify.py`; `grep -n 'ro-bind-data\|unshare-ipc\|def path_ok' plans/round42_c1_verify.py` | docstring `:20-31`; code `:311` (`--ro-bind-data` fd), `:302` (`--unshare-ipc`, `--tmpfs /run`), `:343` (`def path_ok`), `:526` PINS, `:635` `unattributed` |
| red control for repair d only | `cat .ufo/waves/round-42/claims/control-c1-hostile-escape.txt` | `:4` `SETUP fixture 'h-esc42-relative-escape' of battery42/h_esc42.py breaks the contract`, `:5` `exit=2`; `ls .ufo/waves/round-42/claims/hostile/` → `h_esc42.py` (1 file) |
| a–c have no red control | counter docstring `:30-31`; freeze `plans/round-42-claims.md` `Other controls` | `Both tools execute no fixture code … so repairs a-c close vectors these two tools do not open`; freeze: `named as a limit, attacked in wave 1, not claimed` |
| uv assumption unpinned | `grep -n 'PINS' -A4 plans/round42_c1_verify.py`; `grep -n 'uv' plans/round42_c1_verify.py` | PINS holds the two tools only (`:96-99`); PATH keeps `/usr/local/bin` (`:108`); no `plans/battery42` at the tip; `F41RevBatCtl.md:89` calls the risk `environmental` |
| C1 predicate still red | `tail -6 .ufo/waves/round-42/claims/control-c1-nothing.txt` | `:19` `MUTANTS total=14 killed=0 survived=14 …`, `:23` `PREDICATE C1 fail` |
| V9 frozen + filler control red | `grep -n 'V9' plans/round42_c2_verify.py`; `cat .ufo/waves/round-42/claims/control-c2-filler.txt` | counter `:36-42`, `:297`, `:327`; control `:3` `CONTROL-C2-FILLER red-as-required` |
| no tier-B live-state reader | `grep -rln 'pulls/\|state=closed\|merged=' plans/*.py` | no hits |
| scratch sentinel + guard sentence present | `test -f /fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL`; `grep -c 'ROUND-ROOT-SENTINEL' .ufo/waves/round-42/build-spec.json` | exists; `3` |
| guard tool absent, measurement path *worktree-only* | `ls -A .ufo/waves/round-42/build/R42ScratchGuard`; `grep -c SENTINEL .ufo/waves/round-42/integrate/measure.sh .ufo/waves/round-42/claims/envelope.sh` | empty (seat in flight); `1` in the untracked `integrate/measure.sh`, `0` in committed `claims/envelope.sh` |
| Q32 forward leg green for this round's L1 receipts | `grep -lc ENVELOPE .ufo/waves/round-42/claims/*.txt \| wc -l` | `9` receipts with `ENVELOPE start/end` + unchanged listing digest (e.g. `control-c1-nothing.txt:1-2,24`) |
| rule 2 lives only out of lane | `grep -n 'mutable\|in place\|supersedes' /home/vgpnk/Projects/shokunin/CORPUS.md`; `grep -rn 'never in place\|mutable cell' corpus/*.md SKILL.md` | fleet `CORPUS.md:116-118` `Append-only. Only status, recheck and used-by change in place` … `supersedes S0NN —`; lane hits `0` |
| no in-place SOURCES edit this round | `git diff --numstat d69452cf HEAD -- corpus/SOURCES.md` | empty (`removed_lines=0`; S125–S127 still uncommitted) |
| F39MutDirection still refuses a non-round-38 list | `python3 plans/mutant_direction_check.py --lane . --counter plans/round42_c1_verify.py` | `exit 2`, `SETUP … missing=R37_REL,battery38_fixtures,attributed,FAMILY non_6_tuple_rows=14` |
| order gate cannot be repaired this round | `sha256sum plans/order_check.py` vs `PINS`/`frozen-digests.txt:8` | `948d5e1d…` both — a repair would fail `PINS-AFTER` |

## 2. The five round-42 rows (all `open`)

Discernment note on `open` vs `closed` for R1 and R3 — the two items the freeze *partly* closes: the freeze delivers the
counter repairs (R1) and V9 (R3), but R1 also demands *a red hostile control per repair* and a uv pin, and R3 also
demands a *tier-B live-state reader*. Neither residual exists at the tip, so both rows are `open` with the closed half
carried as evidence inside the row (and in §3's status row), not relabelled. A row that closed on its easy half would be
the exact defect the routed ledger exists to prevent.

| id | class | check (run from the lane root) | measured now |
|---|---|---|---|
| `R42-R1` | `c1-counter-soundness-residuals` | repairs a–e greps **and** `grep -rqs 'command -v uv\|/usr/local/bin/uv' plans/battery42/` | rc=2 — `plans/battery42` absent at the tip |
| `R42-R2` | `scratch-root-guard` | sentinel file **and** guard sentence in `build-spec.json` **and** `build/R42ScratchGuard/scratch_guard.py` **and** a sentinel grep in `integrate/measure.sh` **or** `claims/envelope.sh` | rc=1 — guard tool absent at the tip |
| `R42-R3` | `c2-filler-control` | `CONTROL-C2-FILLER red-as-required` **and** `"V9"` in the counter **and** `grep -rqs 'pulls/\|state=closed' plans/*.py` | rc=1 — no live-state reader |
| `R42-R4` | `sources-correction-rule` | `git diff d69452cf..HEAD -- corpus/SOURCES.md` has 0 removed lines **and** `never in place` stated in lane docs | rc=1 — the rule is not in-lane |
| `R42-R5` | `carried-residuals-bundle` | `python3 plans/mutant_direction_check.py --lane . --counter plans/round42_c1_verify.py` | rc=2 — F39MutDirection unchanged |

`R42-R5` gives one bundle item the check command the freeze asked for (`R5 (carried, one item via a wave-1 seat with a
check command)`); the other five items are recorded in the row's `note` with the evidence above.

## 3. Older-row status change (appended, never edited)

`plans/routed_open.py:33-34` refuses a second row for one id (`duplicate id … append nothing for an existing id`), so
a status change can only be a new id. `R40-R1.1` records R40-R1's transition to `closed`: the round-42 counter freezes
**all five** `F41C1Hardened` repairs plus attribution f (digest `559fca0c…` = `claims/frozen-digests.txt:2`), which is
exactly what R40-R1's note said it was waiting for (`routed to a re-frozen round-42 counter`). Its `check` pins those
repairs against removal and **passes** at the tip (`OBSERVE R40-R1.1 rc=0 observed=pass self=closed`). The row says in
its note what it does *not* claim: the a–c hostile controls and the uv pin are the residual, carried by `R42-R1`.

No other older row changes status: every one of the seven older rows with a check still observes what its status says
(`mismatched=0`), and the two without checks (R40-R1, R40-R5) are still open on their own notes' terms.

**Limit of this transition, named rather than hidden.** The tool's tally counts *rows*, so appending a closed row does
not decrement `routed_open`: 16 rows now read `open=9 blocked=1 closed=6`, `routed_open=10` (was 5). The burn-down number
therefore rises by the five new items and does not credit R40-R1's closure. Only an L1 rewrite of the base row would move
it, and the tool forbids editing. That is a property of `routed_open.py`, not of these rows — flagged for the L1 to rule
on (a `superseded-by` key would fix it; I did not touch the tool, it is outside my scope and it is a rider, not a claim).

## 4. Run receipt (scratch copy, rows appended)

```
SELFTEST 12/12                       (rc=0)
ROWS total=16 open=9 blocked=1 closed=6 refused=0
routed_open=10 oldest_round=39
OBSERVE R42-R1 rc=2 observed=fail self=open
OBSERVE R42-R2 rc=1 observed=fail self=open
OBSERVE R42-R3 rc=1 observed=fail self=open
OBSERVE R42-R4 rc=1 observed=fail self=open
OBSERVE R42-R5 rc=2 observed=fail self=open
OBSERVE R40-R1.1 rc=0 observed=pass self=closed
OBSERVE rows=16 mismatched=0
```

Every appended row validates (no `DEFECT line=` output, exit 0), and every check agrees with its row's status.

## 5. Rows to append (verbatim, one JSON object per line)

`plans/routed_open.py:33-34`'s row contract satisfied; append after `corpus/routed-findings.jsonl` line 10. Source
`.ufo/waves/round-42/build/R42RoutedRider/appended-rows.jsonl`:

```json
{"id": "R42-R1", "class": "c1-counter-soundness-residuals", "source": "corpus/lessons/round-41-verifier-spotcheck.md:105", "opened_round": 42, "status": "open", "close": null, "blocker": null, "check": "grep -q -- '--unshare-ipc' plans/round42_c1_verify.py && grep -q -- '--ro-bind-data' plans/round42_c1_verify.py && grep -q 'def path_ok' plans/round42_c1_verify.py && grep -q 'unattributed' plans/round42_c1_verify.py && grep -rqs 'command -v uv\\|/usr/local/bin/uv' plans/battery42/", "note": "…§1 evidence: repairs a-e + f frozen at :20-30/:311/:302/:343/:504/:526/:635 (digest 559fca0c = claims/frozen-digests.txt:2); red control only for d (claims/control-c1-hostile-escape.txt:4-5 exit=2); a-c unreachable per :30-31 = limit, attacked by wave-1 R42SentinelCounter; uv unpinned (F41RevBatCtl.md:89 environmental, PATH :108 keeps /usr/local/bin, no battery42); predicate red (control-c1-nothing.txt:19,:23)"}
{"id": "R42-R2", "class": "scratch-root-guard", "source": "corpus/lessons/round-41-verifier-spotcheck.md:110", "opened_round": 42, "status": "open", "close": null, "blocker": null, "check": "test -f /fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL && grep -q 'ROUND-ROOT-SENTINEL' .ufo/waves/round-42/build-spec.json && test -f .ufo/waves/round-42/build/R42ScratchGuard/scratch_guard.py && grep -qs 'SENTINEL' .ufo/waves/round-42/integrate/measure.sh .ufo/waves/round-42/claims/envelope.sh", "note": "…sentinel present; guard sentence 3x in build-spec.json; guard tool absent at the tip (seat in flight); sentinel check only in untracked integrate/measure.sh (1 hit), claims/envelope.sh 0; Q32 forward leg green — 9 claims/*.txt receipts carry ENVELOPE start/end + unchanged local/bin digest"}
{"id": "R42-R3", "class": "c2-filler-control", "source": "corpus/lessons/round-41-verifier-spotcheck.md:114", "opened_round": 42, "status": "open", "close": null, "blocker": null, "check": "grep -q 'CONTROL-C2-FILLER red-as-required' .ufo/waves/round-42/claims/control-c2-filler.txt && grep -q '\"V9\"' plans/round42_c2_verify.py && grep -rqs 'pulls/\\|state=closed' plans/*.py", "note": "…filler half CLOSED at freeze: V9 rules :36-42, case-table regex :297, check list :327; control-c2-filler.txt:1-3 (V9 DEFECT / V9 ok / red-as-required). open: no tier-B live-state reader — grep -rln 'pulls/|state=closed|merged=' plans/*.py -> 0 hits; the package has no tier-B row for V9 to read"}
{"id": "R42-R4", "class": "sources-correction-rule", "source": "corpus/lessons/round-41-verifier-spotcheck.md:116", "opened_round": 42, "status": "open", "close": null, "blocker": null, "check": "test \"$(git diff d69452cf..HEAD -- corpus/SOURCES.md | grep -c '^-[^-]')\" -eq 0 && grep -rqs 'never in place' corpus/QUALITY.md corpus/SOURCES.md", "note": "…rule 2 only in fleet CORPUS.md:116-118 (out of lane, read-only); no lane doc states it (0 hits); plans/sources_adopt.py guards appends, not in-place edits; invariant holds at the tip — SOURCES diff empty, removed_lines=0, S125-S127 uncommitted"}
{"id": "R42-R5", "class": "carried-residuals-bundle", "source": "corpus/lessons/round-41-verifier-spotcheck.md:117", "opened_round": 42, "status": "open", "close": null, "blocker": null, "check": "python3 plans/mutant_direction_check.py --lane . --counter plans/round42_c1_verify.py", "note": "…six carried items: F39MutDirection (the check; exit 2 SETUP missing=R37_REL,battery38_fixtures,attributed,FAMILY); F39OrderGateMut fail-open is freeze-blocked (order_check.py 948d5e1d = PINS :98 / frozen-digests :8); F39LedgerTip D1 (corpus/lessons/round-40.md:105-106); s_usage-03 (plans/battery41/s_usage.py:39,63, s_exit.py:60-62); 34 unpriced advertised rows (F41CritC1Count.md:61); 14 round_close/tip_receipts residuals (.ufo/waves/round-41/build/R41RoundCloseMut/receipts/)"}
{"id": "R40-R1.1", "class": "c1-counter-soundness", "source": "corpus/lessons/round-40-verifier-spotcheck.md:92", "opened_round": 40, "status": "closed", "close": "round-42 counter freezes all five F41C1Hardened repairs plus attribution: plans/round42_c1_verify.py:20-30, code :311 (--ro-bind-data fd), :302 (--unshare-ipc, --tmpfs /run), :343 (path_ok), :504 (relative-token contract), :635 (unattributed); digest 559fca0c9254e4c09f2406f75ba9559e370012ccb1ecdc91c9a944abbe0c6649 pinned at .ufo/waves/round-42/claims/frozen-digests.txt:2", "blocker": null, "check": "grep -q -- '--unshare-ipc' plans/round42_c1_verify.py && grep -q -- '--ro-bind-data' plans/round42_c1_verify.py && grep -q 'def path_ok' plans/round42_c1_verify.py && grep -q 'unattributed' plans/round42_c1_verify.py", "note": "…status change appended round 42 for R40-R1 (original row not edited; duplicate ids refused at plans/routed_open.py:33-34, so the tally still counts R40-R1 open — L1 decides whether to rewrite the base row at landing). Claims the repairs, not their hostile validation: a-c controls + uv pin carried by R42-R1"}
```

(The `…` inside `note` marks prose abridged **only in this report**; the full text is in
`.ufo/waves/round-42/build/R42RoutedRider/appended-rows.jsonl`, which is the file to append — do not retype from this
report.)

## 6. Risks and blockers

- **C1's own stem for these rows is red.** `plans/battery42` does not exist at the tip (`BATTERY fixtures=0`,
  `claims/control-c1-nothing.txt:19`), so `R42-R1` cannot be closed by anything I can measure now; its last check clause
  will start passing when a battery42 fixture (or a PINS entry) pins the `uv` assumption.
- **`R42-R2`'s fourth clause names an untracked file.** `integrate/measure.sh` is L1-owned and untracked at the tip
  (worktree-only: 1 `SENTINEL` hit). If the L1 does not commit `integrate/`, that clause can only satisfy through
  `claims/envelope.sh` — which is frozen this round. Suggested L1 fix: commit `integrate/measure.sh` as-is.
- **`R42-R4`'s second clause is a phrase test** (`never in place`). It is satisfiable by a one-line rule statement in
  `corpus/QUALITY.md`; I chose a phrase over an invented filename so the L1 controls the wording, and the behavioural
  clause (0 removed SOURCES lines since `d69452cf`) is independent of it.
- **Count inflation** (§3): `routed_open` 5 → 10 because rows are the unit and old rows cannot be edited. The five new
  items are real new work; the R40-R1 closure is real but uncounted by the tool.
- **Not claimed:** I did not run the C1/C2 counters (they need `plans/battery42` / the landing package and belong to the
  L1 gate); nothing here re-measures a claim predicate. `R42-R3`'s live-state reader may be ruled out of scope by the L1
  (this round's package holds no tier-B row) — I recorded it as open rather than deciding that for the lane.

VERDICT: routed-rows-16-open-10-oldest-39
