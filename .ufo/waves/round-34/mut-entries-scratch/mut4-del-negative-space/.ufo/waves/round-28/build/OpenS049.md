# OpenS049 — round-28 re-open of S049 (author-side advice, not outside closure)

Seat/writer: KengakuR28.OpenS049-2 (scout, read-only). Axis: calibration (C2). Access date 2026-10-21.
Scratch evidence: `.ufo/waves/round-28/scratch/OpenS049/` (`extraction.py`, `gsm8k.yaml`, `gsm8k-cot.yaml`, `commit.json`, `contents.json`, `sha256.txt`).
No registry, knowledge, lesson or production edits. No upstream code imported or executed (the files were only fetched and read as text). No tools installed or updated.

## Row under test (corpus/SOURCES.md:71, identical at baseline b9b24796)

`| S049 | lm-evaluation-harness regex filter — https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/lm_eval/filters/extraction.py | code | A | its own regex first/last-match selection, not JSON extraction validity | RegexFilter :27, :47–49; d6de8164; GSM8K strict/flexible yaml | group_select chooses one findall match; ... | mined | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md |`

## Opening

Commands observed (all HTTP 200):
- `curl https://raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/d6de81643928d653435c431bae19945d41d32520/lm_eval/filters/extraction.py`, which has SHA-256 `eb976bb36d5d3e93faafe6d065678e24b4474e78cd4fce1e730e2b8f49b9fda0`, 247 lines and 9001 bytes.
- Cross-check: `https://api.github.com/repos/EleutherAI/lm-evaluation-harness/contents/lm_eval/filters/extraction.py?ref=d6de8164…` returned blob `e61fe4f0b8f8b4b5ee0b76755d6701d59d39d505`, which equals the local `git hash-object` result. The decoded SHA-256 is the same value. Line 27 of the decoded content is `group_select: int = 0,`.
- `https://api.github.com/repos/EleutherAI/lm-evaluation-harness/commits/d6de8164…` resolves to full SHA `d6de81643928d653435c431bae19945d41d32520`, committed 2026-09-14T10:51:05Z.
- The same commit's `lm_eval/tasks/gsm8k/gsm8k.yaml` (SHA-256 `82eb1780…8833`) and `lm_eval/tasks/gsm8k/gsm8k-cot.yaml` (SHA-256 `7c9dd256…bc96`) were also fetched.

The extraction.py SHA-256 is **byte-identical** to the hash recorded in round 27 at `corpus/evidence/round27-sources/gate.md:8`.

Located quotes (each ≤25 words):

| URL (at d6de8164) | location | quote |
|---|---|---|
| …/lm_eval/filters/extraction.py | RegexFilter `__init__` :27 | `group_select: int = 0,` |
| …/lm_eval/filters/extraction.py | RegexFilter.apply :47–49 | `match = self.regex.findall(resp)` / `if match:` / `match = match[self.group_select]` |
| …/lm_eval/tasks/gsm8k/gsm8k.yaml | filter_list :38–42 | `name: "flexible-extract"` … `group_select: -1` (:41) |

## Teaches, scope and anchor against the opened bytes

- **Scope** is "its own regex first/last-match selection, not JSON extraction validity." It is confirmed and narrow. `RegexFilter` (:15–62) runs `findall` and then indexes the matches by `group_select`. The file contains no `json` token anywhere.
- **Teaches** is "group_select chooses one findall match; first and last selection are published harness choices." This is confirmed by two pieces of evidence:
  - The default `group_select` is 0 (:27). `gsm8k.yaml` strict-match (:33–37) omits the option, so it selects the first match. flexible-extract sets `group_select: -1` (:41), which selects the last match.
  - `gsm8k-cot.yaml` repeats the same pairing: strict-match at :47–51, and flexible-extract with `group_select: -1` at :52–57.

  Two nuances are not stated in the row but do not contradict it:
  - When the pattern has multiple capture groups, `findall` returns tuples. After the index is applied, the code keeps the first non-empty group (:50–55), strips it (:56), and falls back to `"[invalid]"` when nothing matches (:28, :58).
  - The following `take_first` step selects among repeated responses, not among regex matches.
- **Anchor `RegexFilter :27, :47–49` is correct** on these bytes. Line 27 declares the default selector, and lines 47–49 contain `findall`, the match test, and the `group_select` index.

### Finding F1: the round-27 "25, not 27" correction is wrong (reference drift, outside the C2 literal contract)

Round 27's falsify seat (`.ufo/waves/round-27/falsify/FSourceS049.md:10–11`) reported different line numbers:
- `group_select: int = 0` at line 25;
- the selector at lines 46–48 and line 48;
- line 27 as `) -> None:`.

That correction was propagated to:
- `corpus/evidence/round27-sources/gate.md:48–49` ("default-selector declaration is extraction.py:25, not27");
- `corpus/lessons/round-27.md:155–156` (M61);
- the admitted knowledge header `corpus/knowledge/extraction-policy-comparison.md:1`, which reads `extraction.py:25,47–49`.

On the SHA-identical bytes, every one of the falsify seat's line numbers is 2 too low:
- line 25 is `self,`;
- line 27 is `group_select: int = 0,`;
- line 29 is `) -> None:`;
- line 49 is `match = match[self.group_select]`.

Consequences:
- The original registry anchor `:27` and the quote location `:47–49` are correct.
- The knowledge header's `:25` is a mis-anchor. Its `:47–49` is correct.
- [INFERENCE] The round-27 reader's tool probably dropped or offset two leading lines; I did not observe its view.

This is a location error only. The quote text and the substantive claim (first/last ordering precedent, not a JSON-policy port) remain accurate.

Suggested disposition for L1: record in the round-28 lesson that M61's "25, not 27" is superseded, with this SHA as evidence. Correct `extraction-policy-comparison.md:1` from `:25` to `:27` only if a separately disclosed knowledge correction is in scope this round. Do not rewrite historical round-27 lesson or gate text. The registry needs no change because its anchor is already right, and anchor is not a mutable cell in any case.

## C2 literal-citation check (frozen 35-path population)

The check used the population's `reference_pattern` `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` and read every path both through `git show b9b24796…:<path>` and from the working tree. All 35 paths were present, and the two reads gave the same result:

- citing_files: `corpus/knowledge/extraction-policy-comparison.md` only, at lines 1 and 17;
- used_by: `corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md`;
- missing_used_by: none. The extra lesson path is allowed by the contract;
- status: `mined`. A cited row must be mined, which holds;
- recheck: `2027-01-19`, which equals opened 2026-10-21 + 90 days.

Suggested mutable-cell change after opening: **none**. Status, recheck and used-by are already consistent with the frozen literal contract. The re-open date equals the existing `opened` value, so no recheck refresh is needed.

## Out of scope for this seat

The template's S056 and S038 instructions belong to the separate OpenS056 and OpenS038 seats listed in `.ufo/waves/round-28/build-assignments.json`. I did not open them here and make no claim about them.

## Limitations

- Line numbers are raw-file line numbers at the pinned commit. I did not inspect GitHub's rendered blob view in a browser.
- The literal check is reference completeness only. It is not semantic citation support.
- F1 is an author-side observation, not outside closure.

VERDICT: **PASS (scoped to S049)**. The source was re-opened byte-identically. Its scope, teaches and anchor are confirmed, and the row needs no mutable-cell change under C2. One reference-drift finding (F1) points the other way from round 27: the registry's `:27` is correct, and round 27's `:25` correction, as carried in the knowledge header and lesson M61, is wrong.
