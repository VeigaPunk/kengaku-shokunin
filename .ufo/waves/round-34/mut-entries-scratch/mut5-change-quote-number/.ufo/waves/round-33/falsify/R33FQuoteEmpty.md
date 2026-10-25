# R33FQuoteEmpty — zero-row quote gate vacuous pass

Seat: `R33FQuoteEmpty` (mutation-tester, leaf). Round 33 falsify wave (hyaku run 7), 2026-10-25.
Object: quote mode of `plans/sources_adopt.py` (`quote_check`, `:442`), measured at tip bytes
`sha256 38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0` (1083 lines).
Claim attacked: the C1 kill-rule clause "…(quote >25 words is refused; exit 6/7/8/9 paths of
`plans/sources_adopt.py` bind)" — read as the invariant that a green exit from the gate
evidences located, citation-bound quotes for the adopted rows.
Bounds kept: no lane file created, edited or deleted except this report; no git/jj command run
against the lane; no tool installed or upgraded (none needed). All execution happened in the
fresh sandbox `/tmp/r33f-quoteempty/` (rsync of the lane tree, `.git`/`.jj` excluded; the copied
gate hashed identical to the lane file before any run).

## 1. The probe (smallest behavior-bearing point, no source mutation)

The mutation is a degenerate *input*, not a code edit: a `--quote-file` whose bytes contain no
`| S### |` row, so `parse_rows` (`:95`) returns `rows=[]` and `bad=[]` — every non-`ROW_RE` line
is skipped silently (`:100-101`). With all six refusal buckets empty, `quote_check` falls
through to `return EXIT_OK, report` (`:569`) after zero loop iterations. Four zero-row shapes
probed, plus the lane's own shipped JSON:

| fixture | bytes |
|---|---|
| `q-empty.txt` | 0 bytes |
| `q-empty.json` | `[]` (valid JSON) |
| `q-empty-obj.json` | `{}` (valid JSON) |
| `q-norows.md` | markdown, table header, no S-rows |
| `.ufo/waves/round-33/assimilation/quotes.json` | the committed gate-note file (JSON) |

## 2. Expected detector

A quote file with zero quoted rows is a caller/type error — `--help` declares `--quote-file` as
"rows.txt whose anchor cells carry the quotes to validate" — so the gate should refuse it, or at
minimum its exit must be distinguishable from a pass that located every pinned quote. The
artifact side of the same flag pair already behaves that way (empty artifact ⇒ exit 2), so
refusing an empty quote set is in-contract, not new policy.

## 3. Battery — exact commands and observed outputs

Sandbox prep: `rsync -a --exclude='.jj' --exclude='.git' <lane>/ /tmp/r33f-quoteempty/lane/`;
kill-control fixtures were built from a verbatim 26-word span of
`captures/arxiv-2412.05579v2-abs.html` (substring presence asserted before use). Every command
below ran as `python3 /tmp/r33f-quoteempty/lane/plans/sources_adopt.py …` with cwd
`/tmp/r33f-quoteempty/lane`; full transcripts in `/tmp/r33f-quoteempty/battery.log`.

**Controls (baseline must pass, or every probe below is inconclusive):**

| case | command (suffix) | observed | exit |
|---|---|---|---|
| C0 | `--selftest` | `SELFTEST cases=17 failed=0` | 0 |
| C1 | `--quote-file …/append-rows.md --artifact …/captures --url-map …/url-map.json` | `QUOTE rows=2 spans=8 located=8 found=8 … mismatch=0 unmapped=0 urlmap=url-map.json entries=3` + 8 `ok …` lines | 0 |
| C2 | `--quote-file q-overlong.md …` (S998, 26-word verbatim span) | `REFUSED S998 overlong words=26 cap=25 at arxiv-2412.05579v2-abs.html` | **6** |
| C3 | `--quote-file q-absent.md …` (S997, 10 words in no capture) | `REFUSED S997 absent words=10 quote="this sentence does not appear in any captured artifact bytes"` | **7** |
| P8 | `--quote-file q-empty.txt --artifact /tmp/r33f-quoteempty/noart` (empty dir) | `QUOTE cap=25 problem=--artifact holds no UTF-8 text` | **2** |
| P9 | `--quote-file …/append-rows.md --artifact …/noart …` | same `problem=--artifact holds no UTF-8 text` | **2** |

The tool is not a no-op: overlong (6) and absent (7) refusals bind, and artifact emptiness is
refused (2) even with zero rows (P8) — the asymmetry below is specific to the quote-file side.

**Probes (the defect):**

| case | `--quote-file` | observed receipt (verbatim prefix) | exit |
|---|---|---|---|
| P1 | `q-empty.txt` (0 bytes) | `QUOTE rows=0 spans=0 located=0 found=0 overlong=0 absent=0 malformed=0 cap=25 artifacts=SHA256SUMS.txt,arxiv-2412.05579v2-abs.html,swebench-pro-tests-test.sh,toolathlon-ab-testing-evaluation-main.py,toolathlon-utils-evaluation-retry.py mismatch=0 unmapped=0 urlmap=url-map.json entries=3` | **0** |
| P2 | `q-empty.json` (`[]`) | identical line | **0** |
| P3 | `q-empty-obj.json` (`{}`) | identical line | **0** |
| P4 | `q-norows.md` | identical line | **0** |
| P5 | `…/assimilation/quotes.json` (lane's own) | identical line | **0** |
| P6 | `q-empty.json`, no `--url-map` | same minus `mismatch=0 unmapped=0 urlmap=…` fields | **0** |
| P7 | `q-foreign.md` — one row `S999` (not a pinned id), 20-word arxiv quote located + bound | `QUOTE rows=1 spans=1 located=1 …` + `ok S999 words=20 … bound=arxiv-…->https://arxiv.org/abs/2412.05579` | **0** |

## 4. What the receipt claims

For every zero-row probe the receipt is the **byte-identical green summary** of a full pass with
all counts zeroed, and the process exit is **0** — the same exit C1 returns for `rows=2
spans=8 located=8`. Three sharp edges:

1. **Exit status cannot distinguish "checked nothing" from "checked everything".** `main`'
   quote mode returns `quote_check`'s code directly (`:1034`); no branch requires
   `rows > 0`. The counts (`"rows": len(rows)`, `:547`) are truthful — the receipt does not
   lie about what it saw — but a consumer keying on exit reads "gate green".
2. **Nothing binds the pinned ids.** P7: a one-row file citing `S999` locates, binds, exits 0.
   The gate has no notion of "the rows this round must quote"; the kill rule's "exit 6/7/8/9
   bind" holds only under the precondition that the quote file carries the pinned rows — a
   precondition nothing enforces in the tool.
3. **No downstream counter re-runs or reads the gate.** `grep -c sources_adopt`
   `plans/adoption_check.py` `plans/round33_c1_verify.py` → `0 0`. The gate's green is coupled
   to C1 procedurally, so the vacuous pass propagates to any receipt that cites it.

The lane **ships** one trigger: the committed
`.ufo/waves/round-33/assimilation/quotes.json` parses to zero rows under `ROW_RE`
(`^( {0,3})\|[ \t]*(S[0-9]{3,})[ \t]*\|`, `:43`), so handing it to the documented gate command
yields P5's green receipt while checking nothing (its own `gate.note` discloses this; the
gate-consumable file is `append-rows.md`).

## 5. Verdict

**UNCAUGHT** — the vacuous pass reproduces at the measured tip bytes with zero source
mutation: every zero-row shape (`[]`, `{}`, 0-byte, header-only markdown, the lane's own
`quotes.json`) exits 0 with a receipt structurally identical to a complete pass, and a
foreign-id row passes the same way (P7). Baseline controls all behaved (C0 17/17, C1 exit 0,
C2 exit 6, C3 exit 7, P8/P9 exit 2), so the probes are conclusive, not artifacts of a broken
detector. This is a **coverage finding against the C1 kill-rule clause as an invariant**: the
refusal exits bind per-row but the gate can be satisfied while quoting nothing, so a green
quote-gate receipt alone evidences nothing. Not a contract change — as mutation tester I
record the survivor and leave the gate untouched. Independently converges with the build wave's
`R33RowDrafts.md` §5, `R33SourcesAdoptDry.md` §6.1 and `R33C1KillRule.md` #8 (all UNCAUGHT
there); this seat re-derived them from scratch fixtures rather than citing them.

Smallest in-contract repair shape (advice only, not applied): refuse `rows == 0` (mirror the
artifact-side `exit 2` at `load_artifact`'s "holds no UTF-8 text" branch) and/or require the
pinned ids under `--admit-ids`-style coupling; either would have killed P1–P5 and P7.

## 6. Restoration evidence

- Lane claim surface rolled before/after the battery:
  `{sha256(plans/sources_adopt.py) ++ sha256s(.ufo/waves/round-33/assimilation/**)} | sha256`
  → before `f9c6d61c3ed1805ea5b63d66d32a76f7178c7d95558c7f57e68458079d01c984`,
  after `f9c6d61c3ed1805ea5b63d66d32a76f7178c7d95558c7f57e68458079d01c984` — **unchanged**;
  nothing to restore because no lane byte was mutated (quote mode only reads; `--out` unused).
- `sha256 plans/sources_adopt.py`: `38492bf1…` before and after, identical in lane and sandbox.
- Sandbox retained for re-run: `/tmp/r33f-quoteempty/` (`run.sh`, `battery.log`, fixtures
  `q-*.md|.txt|.json`, `lane/` copy, empty-artifact fixture `noart/`).
- Writes: this report (dispatch Acceptance) and `/tmp/r33f-quoteempty/**` only. Installs:
  none.
