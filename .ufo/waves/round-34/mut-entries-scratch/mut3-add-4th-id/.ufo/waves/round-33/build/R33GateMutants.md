# R33GateMutants — sources_adopt.py binding-mode mutation probe

Seat: `R33GateMutants-2` (leaf; no subagents). Date: 2026-10-25. Lane:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

Target: `plans/sources_adopt.py` (HEAD `2b4cef2`; hash
`38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0`).

Method: pristine → mutated → restored on a /tmp copy
(`/tmp/r33-R33GateMutants-2/`, 468K, <60 MB bound). Registers/captures copied;
the gate was run only from scratch. Lane originals byte-identical before/after
(sha256 listed below). No production edits; the only lane write is this file.

## Environment note (lane drift)

The brief's "tip c227e486, registry 95 rows" is stale: the lane moved while the
wave sat — HEAD is now `2b4cef2` (round-33 integration) and the live
`corpus/SOURCES.md` is 97 rows with S103/S104 already landed. Registry-mode runs
are normalised against the freeze-tip registry (`c227e486`, 95 rows) for the
pre-append baseline; quote-mode runs are independent of the registry. This raft
does not change any mutant verdict.

## Baselines (pristine detector)

| id | run | exit | verbatim tail |
|---|---|---|---|
| B1a | `--registry SOURCES.md (live,97) --package assimilation/append-package.md --admit-ids S103,S104 --scope-to-admit` | 3 | `registry=97 staged=2 collisions=2 malformed=0 duplicates=0 defects=0 prose=0` |
| B1b | same vs freeze-tip `SOURCES-freeze.md` (95 rows) | 0 | `registry=95 staged=2 collisions=0 … defects=0 prose=0` |
| B2 | quote mode **with committed `assimilation/url-map.json`** | **8** | `mismatch=2 unmapped=0 urlmap=url-map.json entries=3` — both S103 spans `REFUSED S103 url-mismatch` |
| B2b | quote mode with corrected repo-root map (`url-map-reporoot.json`) | 0 | `mismatch=0 unmapped=0 urlmap=url-map-reporoot.json entries=3` — all 4 spans `ok … bound=` |
| B3 | quote mode, no `--url-map` | 0 | `QUOTE rows=2 spans=4 located=4 found=4 overlong=0 absent=0 malformed=0 cap=25` (no `mismatch`/`unmapped`/`urlmap=` fields) |

B2 is a **baseline failure of the committed artifact**: the committed
`url-map.json` maps `toolathlon-ab-testing-evaluation-main.py` to the blob URL
`https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py`
while the S103 `source:` cell (append-package.md, quotes-rows.txt, and the landed
registry row) cites only the repo root `https://github.com/hkust-nlp/Toolathlon`.
`bind_failure` requires **exact normalized set membership** (`sources_adopt.py:436-439`),
no prefix matching, so the blob map can never bind the repo-root citation. The
committed green receipt `gate-receipts.txt` shows `bound=…->https://github.com/hkust-nlp/Toolathlon`
— i.e. the green receipt was produced with a repo-root map that the committed map
is not. The committed map is a stale artifact (hazard: C1's kill rule says S103
must resolve; with the committed map it does not).

## Mutant table

| mutant | input (vs corrected baseline B2b/B3) | expected exit | observed exit | verdict |
|---|---|---|---|---|
| (a) url-map maps Toolathlon capture to a different document | `url-map-mutant-wrongdoc.json`: toolathlon capture → `https://arxiv.org/abs/2412.05579` | 8 | 8 | killed (S103 spans `REFUSED S103 url-mismatch`; S104 unaffected) |
| (b) omit url-map | no `--url-map` | 0 (docstring `quote_check`: "Without the map the check is byte-presence only"; `--help`: url-map "needs --quote-file and --artifact") | 0 | survivor-by-contract (byte-presence check still green) |
| (c) quote 26+ words | `quotes-mutant-overlong.txt`: S105 anchor, 27-word verbatim substring of arxiv capture `"rapid advancement of Large Language Models (LLMs) has driven their expanding application across various fields. One of the most promising applications is their role as evaluators based"` (`overlong27.txt`) | 6 | 6 | killed (`REFUSED S105 overlong words=27 cap=25 at arxiv-2412.05579v2-abs.html`) |
| (d) quote absent from artifact | `quotes-mutant-absent.txt`: S105 anchor `"this sentence does not appear in any captured artifact bytes"` (10 words, in no capture) | 7 | 7 | killed (`REFUSED S105 absent words=10`) |
| (e) staged row's used-by prelists a different entry | S105 row with `used-by=corpus/knowledge/ghost.md`, admitted entry = `corpus/knowledge/benchmark-grader-semantics.md` | clobber (rewrite to admitted set) | exit 0; output block `used-by` cell contains only the admitted entry; `ghost.md` removed | gate **clobbers** (does not append); `build_block` `cells[10] = used_by` (`:179`) unconditionally rewrites; selftest case 7 pins the same contract |

Also observed: exit precedence `(sources_adopt.py:559-568)` malformed(4) →
overlong(6) → absent(7) → mismatch(8) → unmapped(9); `unmapped` exit 9 is only
reachable when a map is passed (no-map mode never enters binding, so exit 9 is
impossible without `--url-map`).

## Restoration evidence

Lane sha256 identical before and after the probe run (recomputed at end):

```
plans/sources_adopt.py                    38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0
corpus/SOURCES.md                         c26d1a860c74532796d127698260dcaf06ae5d1591fe4846f2d53e4e49e18e74
assimilation/url-map.json                 76c75639110cd95cf56e6cc1a5f0aa16fb129f02d9e818e9580454d15f5c9082
assimilation/quotes-rows.txt              aada22cb49f4b84cf602fba29c7352f164a6acbd61bd59b9c38b01b5b91f027b
assimilation/append-package.md            1c26b09a110c2beb436958ce24f3a5eb64d4649d2251c279eb91807dc1b7dcd9
```

All mutant work confined to `/tmp/r33-R33GateMutants-2/` (468K).

## Verdict / findings

- `VERDICT: gate-killed` — mutants (a), (c), (d) killed with exits 8/6/7;
  mutant (b) survives by design (contract: without url-map the gate checks byte
  presence only, exit 0); mutant (e) is not a refusal path — the gate clobbers a
  staged row's used-by to exactly the admitted entries (never appends), exit 0.
- **Coverage finding (real, not a mutant):** the committed `url-map.json` is
  stale/self-inconsistent — it fails exit 8 while the committed green receipt
  required a repo-root map. The C1 gate as committed does not admit S103; the
  repo-root map (as `gate-receipts.txt` shows was used) does. L1 should decide
  whether the map or the receipt wins; the C1 kill rule will otherwise not be
  satisfiable from the committed bytes.
- No tools installed (none needed; no pacman, no uv, no binaries). No lane files
  written except this report.
