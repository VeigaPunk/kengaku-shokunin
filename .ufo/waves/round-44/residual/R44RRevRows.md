# R44RRevRows — residual re-open of SOURCES rows S138-S146 (kengaku round 44, 2026-10-26)

Seat: R44RRevRows (reviewer, residual wave). Lane state audited: landing commit
`2a263e5a56ef6d48d06805e1ccd106de5de9ba66` (fresh `git clone -q --shared` into scratch,
`git rev-parse --show-toplevel` verified equal to the clone before any command; no git mutation anywhere).
Scratch: `/fast/scratch/hyaku/kengaku-r44/R44RRevRows` (removed at the end; receipts copied here first).
Tools installed this seat: none. Frozen files untouched: every command was read-only against lane/checkout content;
writes went only to my scratch and this report subtree.

## Method

Every run that could write (fetch, parse, census, digest check) ran under the round-44 envelope
(`.ufo/waves/round-44/claims/envelope.sh <env-scratch> <cmd>`); in all five envelope runs
`local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`, no INVALID. Raw receipts:
`fetch-receipt.txt`, `census-receipt.txt`, `anchor-digest-receipt.txt`, `rows-parse.txt` (this subdir).

1. Fresh fetch: for each of the 9 rows, `curl -fsS --max-time 60 <row URL> -o $S/fetch/<capture>`, then
   `cmp -s` against `corpus/evidence/round44/tb2-feal-linear-cryptanalysis/<capture>` and `sha256sum`.
2. Row parse (own script, `rows-parse.txt`): cells must be 11; anchor cell's `sha256 <hex>` must equal
   `plans/pkg-spec-r44.json` pin; row URL must equal `raw_base + upstream`; committed capture must exist and
   hash to the pin; used-by must be exactly `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md`.
3. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <clone>/corpus/SOURCES.md`.
4. `python3 <clone>/plans/anchor_digest_check.py --lane <clone>` (frozen tool, read-only), plus `--verbose` receipt,
   plus a pre-landing control on parent `5e3d3aa06c6b7000929ac3e62563a39159c4501f` (second scratch clone).

## Per-row table

Fresh-fetch time is the curl start (`date -Is`, host local -03:00); freeze fetch was 2026-10-26 20:10:09 -03
(claims). All 9 upstream fetches returned bytes IDENTICAL to their captures (cmp), so each fetched digest equals
both the capture digest and the spec pin.

| row | fetched at (curl start) | cmp vs capture | anchor sha256 == spec pin | cells | tier/status/opened/recheck | used-by == entry |
|---|---|---|---|---|---|---|
| S138 | 2026-10-26T20:48:49-03:00 | IDENTICAL | yes (`f59ebc72…d9f9`) | 11 | A / mined / 2026-10-26 / 180d | yes |
| S139 | 2026-10-26T20:48:49-03:00 | IDENTICAL | yes (`a2f1669d…b03`) | 11 | A / mined / 2026-10-26 / 180d | yes |
| S140 | 2026-10-26T20:48:49-03:00 | IDENTICAL | yes (`3a71f0b5…2c63`) | 11 | A / mined / 2026-10-26 / 180d | yes |
| S141 | 2026-10-26T20:48:50-03:00 | IDENTICAL | yes (`ef521cde…ff1d`) | 11 | A / mined / 2026-10-26 / 180d | yes |
| S142 | 2026-10-26T20:48:50-03:00 | IDENTICAL | yes (`9431cbc2…c9e1`) | 11 | A / mined / 2026-10-26 / 180d | yes |
| S143 | 2026-10-26T20:48:50-03:00 | IDENTICAL | yes (`a038645f…dc33`) | 11 | A / mined / 2026-10-26 / 180d | yes |
| S144 | 2026-10-26T20:48:50-03:00 | IDENTICAL | yes (`be50ae01…cb77`) | 11 | A / mined / 2026-10-26 / 180d | yes |
| S145 | 2026-10-26T20:48:51-03:00 | IDENTICAL | yes (`4c6864e0…ebd2`) | 11 | A / mined / 2026-10-26 / 180d | yes |
| S146 | 2026-10-26T20:48:51-03:00 | IDENTICAL | yes (`a39ec2c4…9fc4`) | 11 | A / mined / 2026-10-26 / 180d | yes |

Envelope lines (fetch run, representative; all runs in receipts):

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind $S/env-fetch $S/env-fetch --bind $S/env-fetch/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- bash $S/fetch.sh
ENVELOPE start 20:48:49 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 20:48:52 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

## Named command results

- `sources-census.sh validate --file <clone>/corpus/SOURCES.md` → **exit 0**, `file ok`, 15 `W04` warnings — all on
  pre-existing rows S040–S100 (duplicate URL across scopes); none names S138–S146. Receipt: `census-receipt.txt`.
- `python3 plans/anchor_digest_check.py --lane <clone>` → **exit 1**:
  `DEFECT S140 anchor token=c class=token-outside-anchor detail=sha256-claim-in-cell-5-of-11 loc=corpus/SOURCES.md:155`,
  `rows=139 tokens=46 defects=1`. Receipt: `anchor-digest-receipt.txt`.

## Findings by severity

**F1 (high, blocks row-level admission as-is): landed row S140 violates the frozen anchor-digest rule; the wave's
admission path could not see it.** `corpus/SOURCES.md:155` scope cell says "derives every plaintext and ciphertext
from a sha256 chain over seed and counter" (quote, 13 words). The frozen scanner's token regex
`sha256[ \t]+\`?([0-9A-Fa-f]+)` (`plans/anchor_digest_check.py:147`) parses `sha256 chain` as a digest claim with
token `c`; its rule "a token outside the anchor cell … always a defect, whatever its value" (:81) then fires as
`token-outside-anchor` in cell 5 of 11. The wave introduced this: the same tool on the pre-landing parent
`5e3d3aa06c6b7000929ac3e62563a39159c4501f` prints `rows=130 tokens=36 defects=0`, exit 0. The landing's own
admission never runs this tool: `round44_c2_verify.py` V3 (:160–171) collects tokens only from the anchor cell —
`re.findall(r"sha256\s+([0-9a-fA-F]+)", found[0][5])` at :168 — so a stray claim in any of the other 10 cells is
invisible to it; `pkg_gate.py` contains no anchor scan at all (grep for `anchor`: no match); census validate checks
NF/enums, not token placement. S140's anchor itself is fine (`RESOLVED S140 digest=3a71f0b5…` bound by=url-task);
the defect is purely the misplaced claim-shaped prose.

**F1 repair (draft for the L1; I edited nothing):** `corpus/SOURCES.md` is not in the freeze list (the frozen set is
the two tools, both counters, probe, spec, gate, dry table, captures, receipt, `.ufo/waves/round-44/claims/`), so a
one-word reword of the S140 scope cell removes the defect without touching any frozen artefact — any wording without
lowercase `sha256` followed by whitespace + hex-initial text outside the anchor cell works, e.g. "from a SHA-256
chain over seed and counter" (the frozen regex is case-sensitive lowercase `sha256[ \t]+`) or "from a hash chain
over seed and counter". After repair, `plans/anchor_digest_check.py --lane .` should print `defects=0`, exit 0; the
C2 counter (V3/V6) is insensitive to the change but a rerun is the L1's call.

**F2 (medium, admission-coverage gap, not a data defect): the C2 predicate can stay green while the frozen
anchor tool is red.** F1 is the concrete instance: `checks=11 defects=0 PREDICATE C2 pass` (L1-measured, and V3's
anchor-cell-only scan plus a gate with no anchor check explain why) coexists with `anchor_digest_check.py` exit 1.
The task list I was given (fetch, cmp, pin equality, 11 cells, used-by, census, anchor tool) is strictly stronger
than the counter's V3+V6 for this row set; recommend the landing checklist for future packages include a
`plans/anchor_digest_check.py --lane .` run (it is cheap, frozen, and read-only).

**F3 (info, tool limit, no action): the same regex makes prose a latent defect class.** Any future row whose
scope/teaches text contains lowercase `sha256 ` followed by a word starting with a hex letter (a…f) re-triggers
F1's shape; the tool is frozen, so registry wording is the only lever. Note the tool already scans 139 rows /
46 tokens with only this one defect, so exposure is otherwise clean.

## Verification of the non-defect claims (all confirmed)

- Freshness: 9/9 URLs fetched 20:48:49–20:48:51 -03 (envelope-bracketed) byte-identical to captures; digests equal
  `plans/pkg-spec-r44.json` pins and the committed `SHA256SUMS` (`sha256sum -c SHA256SUMS`: 11/11 OK, including the
  two row-less captures `feal.c`, `gitignore`).
- Shape: 9/9 rows parse as exactly 11 cells (census NF=13 agrees, exit 0); all tier A / mined / 2026-10-26 / 180d;
  URLs equal `raw_base + upstream` from the spec.
- used-by: all 9 rows name exactly `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md`, which exists in the
  clone.
- Clone state audited: `corpus/SOURCES.md` at the landing commit hashes to
  `af9051276ce4c552c882f143bf5cf22222a36e5006178364326d8270ba6c3718` (working tree = HEAD, no local edits).

## Residual risk and verification gaps

- I did not rerun `plans/round44_c2_verify.py` or `pkg_gate.py` (owned by other seats' scope); my V3/gate readings
  are source citations (`round44_c2_verify.py:160-171`, gate grep), not executions.
- `plans/anchor_digest_check.py` `--evidence-ref index` variant not run; default `head` covers the clean-clone
  reading the predicate names.
- The upstream content is pinned by commit SHA in the URL, so byte-equality was near-certain; the fetch still rules
  out repo-side rewrite/history edits at that ref and confirms availability.
- Scratch `/fast/scratch/hyaku/kengaku-r44/R44RRevRows` deleted after receipts were copied into this subdir.

VERDICT: rows-ok-8/9-census-exit-0
