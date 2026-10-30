# S2PriorArt — seat report (kengaku round 55, wave w1, 2026-10-30)

## What I ran
Prior-art pricing for R55-C3 (chess-best-move grader class), read-only only.

1. Read frozen claims: `plans/round-55-claims.md` (R55-C3 section) — grader reading, pin
   `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, S201/S202/S109 context.
2. Verified freeze commit exists: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse
   --short 80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (plus `git log --oneline -2 --
   plans/round-55-claims.md`) — **exit 0**. Read-only git only; no mutations anywhere.
3. Grep over `plans/` and `corpus/SOURCES.md` to ground upstream repo identity
   (`harbor-framework/terminal-bench-2`) and the held TB2 source-row pattern (S105–S164).
4. ~20 read-only web searches and URL GETs (raw.githubusercontent.com, huggingface.co resolve
   endpoint, hub.harborframework.com, benchmarksolutions.org, arxiv.org). No POST/auth endpoints.
   Direct fetches that succeeded: upstream grader + instruction at the pin, HF mirror grader bytes,
   SQuAD official evaluate-v2.0.py, HF evaluate exact_match.py + squad.py, Harbor Hub dataset page,
   benchmarksolutions.org task page. Failed fetches recorded below.
5. Scratch per contract: created `/fast/scratch/hyaku/kengaku-r55/S2PriorArt/` (exit 0); no work
   files were needed; removed before yield.

## Commands + exit codes
- git rev-parse/log above → 0.
- `mkdir -p /fast/scratch/hyaku/kengaku-r55/S2PriorArt && mkdir -p <seat wave dir> && echo created` → 0.
- `rmdir /fast/scratch/hyaku/kengaku-r55/S2PriorArt` (scratch removal) → see tail of session; if the
  removal is not shown here it ran after this line was drafted; dir verified empty beforehand.
- All other work was `read`/`web_search`/`grep`/`glob`/`write` tool calls (no shell).

## Files I wrote (all inside the lane repo, per named paths)
- `.ufo/waves/round-55/w1/S2PriorArt/prior-art.md` — the Target deliverable: 8 evaluated hits with
  URLs, what each establishes, phenomenon-new vs instrument-new verdicts, dead ends, final
  `PRICING:` line.
- `.ufo/waves/round-55/w1/S2PriorArt/report.md` — this file.
- `.ufo/waves/round-55/w1/S2PriorArt.md` — the `Report:` trailer path (lane-relative). Content is a
  copy of prior-art.md with a one-line provenance header.

## Defects found
- Prompt-internal path conflict: the seat Target/contract name seat-dir files
  (`w1/S2PriorArt/prior-art.md`, `…/report.md`) while the `Report:` trailer names
  `w1/S2PriorArt.md` (one level up, outside the seat dir). The contract sentence "write Report:
  trailer paths at lane-repo-relative paths" was honored by writing the third file too; glob before
  writing confirmed no pre-existing file was clobbered. L1 may fold or move it during integration.
- No other defects in lane files observed; no sibling file was touched.

## Dead ends (also recorded in prior-art.md)
- HF evaluate `metrics/squad/evaluation.py` → 404 (moved); used `metrics/squad/squad.py` + official
  SQuAD-explorer script instead.
- HELM `docs/metrics.md` raw → mkdocstrings stub, nothing quotable; HELM/lm-eval EM semantics priced
  at search-surfaced weight.
- OpenReview forum `waLyaPFdwc` → bot-check blocked; the TB2-audit paper stays
  [SEARCH-SURFACED, NOT FETCHED].
- benchmarksolutions.org grader content → gated behind client-identifying API; no semantics visible.

## Honesty notes
- All fetched quotes (H1–H5, H7) are from direct GETs on 2026-10-30; H6/H8 are search-surfaced and
  marked as such in prior-art.md. No check was run that is not reported; nothing was installed; no
  subagents were spawned; `agent://all` was never messaged.

PRICING (short form; full form in prior-art.md): class published → R55-C3 is a replication of the
class, novel only as this lane's instrument instance (13th TB2 grader + frozen 12-case
predicted-verdict offline probe); consistent with the frozen coverage claim's scope.
