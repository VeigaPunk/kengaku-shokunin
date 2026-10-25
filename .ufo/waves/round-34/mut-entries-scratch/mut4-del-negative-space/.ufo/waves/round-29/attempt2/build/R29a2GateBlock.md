# R29a2GateBlock — draft of the round-29 attempt-2 Gate block

Seat: `L1Kengaku29.R29a2GateBlock` (leaf scribe). Assignment: draft the `## Attempt 2 (2026-10-25)`
Gate block for `corpus/lessons/round-29.md` at `/tmp/r29a2-GateBlock/gate.md` only. No production file
was created, edited or deleted; no campaign tool under `/home/vgpnk/Projects/shokuknow` was executed
(all campaign paths read-only); no tool installed or upgraded (nothing was needed, no pacman transaction
attempted); no subagent spawned.

**Bounds disclosure:** the report was first written with a relative path, which landed it at
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-29/attempt2/build/R29a2GateBlock.md` — outside this
lane. It was moved to this path and the three directories it had created at the fleet root were
removed (`rmdir` after `find round-29 -type f` showed my file was the only one); the fleet root now
holds no round-29 directory under `.ufo/waves/`.

## Behavior

Read the frozen claims (`plans/round-29-attempt2-claims.md`), the attempt-1 Gate shape
(`corpus/lessons/round-29.md`), then the current attempt-2 section, which L1 had already drafted and was
still editing during this seat. Re-opened S077/S078/S079/S080/S090 myself from their pinned URLs, and
checked both quarantine-register rows (S091, S105) against live and archived bytes. Drafted an 18-row
Gate table (candidate → decision → reason → flip condition) plus a 6-row Sources-opened table, then
linted the draft for flip coverage.

## Acceptance check on the draft

- Gate rows: 18, each with a non-`n/a` flip condition. Lint: every table row has ≥5 pipes and no Gate
  row lacks the string `Flip` (the six exception rows are the Sources-opened table, which uses its own
  schema). Command: python filter over `gate.md` lines starting with `| ` → `table rows total 24`,
  `rows without Flip: ['S077','S078','S079','S080','S090','S091']` (the sources rows only).
- Coverage of the assignment: (a) the entry + its five rows — entry row, S077, S078, S079, S080, S090;
  (b) rejected staged entries — `contamination-transparency-card.md`, `judge-calibration-thresholds.md`,
  `benchmark-grader-semantics.md`, plus the 168-row/64-entry scope bucket; (c) quarantine verdicts —
  register S091 and register S105; (d) Sources-opened table with access date 2026-10-25 and one row per
  S077/S078/S079/S080/S090 (plus S091), each with a ≤25-word quote and its location. Extras added for
  the milestone's second half: `plans/sources_adopt.py`, `plans/adoption_check.py`, registry accounting,
  the recheck-normalization row, the metered-command row.

## Measurements run by this seat (exact commands and outcomes)

| command | outcome |
|---|---|
| `curl -sSL --max-time 60 -o <file> <pinned URL>` for S077, S078, `v2/GATE.md`, S080, `task_config.json`, S090 | HTTP 200 for all; 41 842 / 6 858 / 1 659 / 16 883 / 227 / 53 390 bytes; sha256 `b0a7cb14…`, `dde4168f…`, `7c30b8d6…`, `d06165b5…`, `0aa31c18…`, `cbc50108…` |
| `curl … api.github.com/…/git/trees/2fd12b88…` and raw `protein-assembly/task.toml` | 200 / 26 062 B (tree, 92 entries: 89 trees + `.gitignore`, `LICENSE`, `README.md`) and 200 / 973 B (toml sha256 `d7149606…`); later the same API route returned 403 rate-limit (see F5) |
| `curl … api.github.com/…/git/trees/9be8d8fe…:tasks/finalpool` | 200, `truncated=false`, 109 entries = 108 trees + `task_conflict.json` |
| `grep`/text extraction over the fetched S090 bytes | both quote targets present; **no** date pattern and **no** `<time>` token in the served bytes |
| `curl -A '<browser UA>' https://jpn.nec.com/techrep/journal/g23/n02/230212.html` (twice, with and without UA) | **HTTP 403, 418 B "Access Denied"** both times |
| `curl http://web.archive.org/web/20240915125720id_/https://jpn.nec.com/…/230212.html` | 200, 60 132 B, sha256 `c861d18e…`; the staged S091 quote is present (§6.2) |
| `curl https://www.meti.go.jp/…/result_1/index.html` (original) | **403**, 5 045 B, `<title>` = 指定されたページまたはファイルは存在しません; hold-out text absent |
| `curl http://web.archive.org/web/20251118034714/https://www.meti.go.jp/…/index.html` | 200, 13 027 B, sha256 `4fa9b787…`; hold-out sentence, `Jaster-GENIAC-v0.1`, `JMT-Bench-GENIAC-v0.1` present; not-found string 0 occurrences |
| `curl https://www.tbench.ai/blog` | 200, 67 235 B; "Terminal-Bench 2.0 and Harbor Fri Nov 07 2025", "Terminal-Bench 2.1 Wed May 06 2026 — A revision of Terminal-Bench 2.0 that fixes 28 tasks", "Terminal-Bench 4.0 Fri Aug 28 2026" |
| `python3 plans/sources_adopt.py --selftest` | `SELFTEST cases=10 failed=0`, **exit 0**, ten `PASS` on three revisions (432-line, 447-line, and the committed 447-line tip) |
| `python3 plans/adoption_check.py --expect …/adoption-expect.json --census` | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`, **exit 0**; on an earlier revision the same run printed `… usedby_ok=1 verified_at=1 census=fail` with exit 1 |
| `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | exit 0, trailing line `kengaku ok …/corpus/SOURCES.md`, 14 pre-existing duplicate-URL warnings |
| `python3 plans/sources_adopt.py --registry corpus/SOURCES.md --package …/SOURCES.append.md --admit-ids S093 …` | `registry=81 staged=173 collisions=0 malformed=1 … malformed: S093:escaped-pipe`, **exit 4** |
| census-anchored row count on `corpus/SOURCES.md` vs `git show 8c14a5d:corpus/SOURCES.md` | 82 rows (A 76 / B 4 / C 2) vs 76 rows (A 70 / B 4 / C 2) |

## Findings (advice to L1; none of these is an integration)

| # | finding | evidence | why it matters |
|---|---|---|---|
| F1 | The current sources table calls "The verifier never runs in the agent's sandbox." **9 words**; it is **8** | `len("The verifier never runs in the agent's sandbox.".split())` → 8; `R29a2RevQuoteS078.md:59` reports 8 | A word count is a claim; 9 is a miscount that a Q3 re-read falsifies |
| F2 | The current Gate leaves S105 as "see the second hand-check verdict in the round report" and says the **row's quote** "reads like a fetch-failure page" — both wrong | bare-curl to the original METI URL → 403 with `<title>` 指定されたページまたはファイルは存在しません and no hold-out text; snapshot 20251118034714 → 200, 13 027 B, hold-out sentence present, not-found string 0×; `R29a2QuarS105.md` classes the payload "quote-column misbinding — error-shell quote" | The error text is the **register payload**, not the row's quote; a real verdict row is supplied in the draft |
| F2b | The staged S105 row's "[WITHDRAWN FROM METI …]" note is **not established** | `R29a2QuarS105.md`: live URL 200 / 10 768 B with browser-like headers, `last-modified: Thu, 25 Jun 2026` (page not withdrawn); my own browser-header request returned **202** / 2 463 B untitled body (challenge), so I confirm neither | The draft records both observations and makes striking the note a flip condition, not a silent edit |
| F3 | The cell-transition paragraph says "Registry 76 → 81 rows; tiers A 70 → 75" | measured 82 rows, A 76 / B 4 / C 2; the sixth row is S091 (ABC) at `corpus/SOURCES.md:106` | Stale by one row and one tier; census parity claims would be off |
| F4 | The frozen claim's clause 3 (and target case (d)) say a prose `recheck` normalizes to the **access date**; the implementation emits the default cadence `180d` and stamps the access date into `opened` | `plans/sources_adopt.py` `build_block`: `cells[9] = recheck_default` (`:137` `180d`, `:406` default) with the comment "never the access date itself: that would put every adopted row 0 days overdue"; case 6 named `prose-recheck-normalized` asserts `[10] == "180d"` and `[9] == "2026-10-25"` | The claim wording, not the code, is the defective side; and the case **name** encodes the claim's property while its assertion tests the negation — a reader of the PASS line credits an untested property |
| F5 | The entry's two count commands are metered `api.github.com` routes with two failure modes (301 moved, 403 rate-limit) | `R29a2SrcS079.md` §4, `R29a2RevQuoteS079.md` F6; my own tree call was 200 earlier and the same route later 403/280 B | `CORPUS.md` "A count carries its command": the command as published cannot reproduce the count |
| F6 | Campaign register row `kengaku / round2 / S091` and lane registry `S091` (ABC, `corpus/SOURCES.md:106`) share an id and denote different sources | `absent-defect-register.md:101` vs `corpus/SOURCES.md:106` | A later reader can cite the wrong S091; the draft labels the campaign row explicitly |
| F7 | Both quarantine live statuses are contested inside this round's receipts: S091 scout 200 / 60 335 B vs my three fetches 403 / 418 B; S105 scout 200 / 10 768 B vs my 202 / 2 463 B (and bare-client 403) | `R29a2QuarS091.md`, `R29a2QuarS105.md` fetch blocks vs my commands above | Both quotes are located in archived bytes I fetched; neither live disposition is asserted as mine |
| F8 | C2's control statement is weaker than `failed=0` suggests, but **not** in the way the five-mutant sample implied: all ten cases are killable by some mutant (10/10 on the earlier revision, 9/10 + a conjunction on the current one), while **four mutants leave the current suite green** (`h1_dead_anchor_switch`, `h5_no_status_rewrite`, `h6_no_opened_write`, `h7_no_scoped_prose_exemption`) and case 6 no longer isolates recheck normalization | `R29a2GateAudit.md` §3 kill matrix, §4 unseen mutants, §5; the earlier M2/M3 "survivors" in `R29a2FixtureMutations.md:38-41` are superseded on the current bytes by cases 5 and 10 | The draft's C2 row uses the later receipt and states the four unobservable capabilities instead of the stale 5/10 count |
| F9 | On revision `ee34914c…` the counter printed an extra `verified_at=1` field absent from the frozen target string; the current revision prints the frozen string verbatim | my two counter runs (`verified_at=1 … census=fail` then `… usedby_ok=1 census=ok`) | Closed, but recorded so a future extra field is an amendment, not a silent change |
| F10 | The sources-table preamble still says "Access date 2026-10-25 for all five rows" and "each row's own `recheck` is that ISO date"; the table now has six rows and every `recheck` cell is `180d` | `corpus/SOURCES.md:100-106` cell 10; `entry:7` | Two stale sentences in the section this draft replaces |

## Out of scope / not done

- Not re-derived: the entry's "6 lines across 3 tasks write integer literals" (`entry:53`) — no receipt
  exists in the build directory at write time; flagged unverified in the draft.
- No second-seat re-read was performed by this seat (Q10 stays with the reviewer seats); the draft
  cites their reports rather than restating them as my own observations.
- No outside closure, no round judgment, no integration, no commit.
- Campaign-side register files were read only; the register itself was not edited or regenerated.

## Artifact paths

- Draft Gate block: `/tmp/r29a2-GateBlock/gate.md` (26 431 B, 18 Gate rows + 6 source rows; every Gate row carries a flip condition).
- Fetched bytes and digests: `/tmp/r29a2-GateBlock/quotes/` (S077, S078, S078gate, S079toml,
  S079tree, S080, S080task, S090, S091snap, S091live2, S105, S105orig, tbblog).
- Refused-block receipt: `/tmp/r29a2-GateBlock/block-check.md` (not created — the run refused/errored
  before writing, which is the S093-class refusal behaviour).
- Landing commits observed at close: `8cf7b60` (adoption landing), `ff476d0` (prior art + repairs),
  `4b82ff7` (removes entry widenings, tightens used-by/census gating, widens the census row anchor);
  tree clean at `4b82ff7`, both gates re-run green there.
- Peer reports relied on (read-only): `.ufo/waves/round-29/attempt2/build/`
  `R29a2SrcS077.md`, `R29a2SrcS079.md`, `R29a2SrcS090.md`, `R29a2RevQuoteS077.md`,
  `R29a2RevQuoteS078.md`, `R29a2RevQuoteS079.md`, `R29a2RevQuoteS090.md`, `R29a2QuarS091.md`,
  `R29a2PriorArt.md`, `R29a2FixtureMutations.md`, `R29a2CritClaimC2.md`, `R29a2QuarS105.md`,
  `R29a2GateAudit.md`.
- This report: `.ufo/waves/round-29/attempt2/build/R29a2GateBlock.md`.
