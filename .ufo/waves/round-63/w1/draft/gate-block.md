## Gate

Gate block for the two source rows opened this round (seat `KnowledgeDraft`, 2026-11-03; splice
target `corpus/lessons/round-63.md` `## Gate` table). Both rows are opened by URL, dated by
access date, and each carries a quote **located** in the lane's own copy of the bytes under
`.ufo/waves/round-63/w1/recon/`, re-checked with `grep -n -F` in this seat. Quotes are at most
25 words each (`wc -w`).

| row | URL | access date | located quote (≤25 words) | file and line in the lane's own copy | `wc -w` | verdict |
|---|---|---|---|---|---|---|
| S228 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/pypi-server/tests/test_outputs.py | 2026-11-03 | `assert v.dotproduct([1, 1], [0, 1]) == 1` | `.ufo/waves/round-63/w1/recon/S228-pypi-test_outputs.py:85` | 7 | **LOCATED** — `grep -n -F 'assert v.dotproduct([1, 1], [0, 1]) == 1' .ufo/waves/round-63/w1/recon/S228-pypi-test_outputs.py` → `85:    assert v.dotproduct([1, 1], [0, 1]) == 1` |
| S229 | https://peps.python.org/pep-0503/ | 2026-11-03 | `Below the root URL is another URL for each individual project contained within` | `.ufo/waves/round-63/w1/recon/S229-pep-0503.html:165` | 13 | **LOCATED** — `grep -n -F 'Below the root URL is another URL for each individual project contained within' .ufo/waves/round-63/w1/recon/S229-pep-0503.html` → `165:<p>Below the root URL is another URL for each individual project contained within` |

Supporting located quotes for the same two rows (also re-checked with `grep -n -F`, same
copies, same access date):

| row | located quote (≤25 words) | file and line | `wc -w` | verdict |
|---|---|---|---|---|
| S228 | `"http://localhost:8080/simple",` | `.ufo/waves/round-63/w1/recon/S228-pypi-test_outputs.py:30` | 1 | **LOCATED** — `grep -n -F '"http://localhost:8080/simple",'` → `30:        "http://localhost:8080/simple",` |
| S228 | `assert v.dotproduct([1, -1, 0, 0.01], [0, 0, 10, 0]) == 0` | `.ufo/waves/round-63/w1/recon/S228-pypi-test_outputs.py:88` | 7 | **LOCATED** — `grep -n -F` → `88:    assert v.dotproduct([1, -1, 0, 0.01], [0, 0, 10, 0]) == 0` |
| S229 | `is replaced by the normalized name for that project, so a project named` | `.ufo/waves/round-63/w1/recon/S229-pep-0503.html:167` | 13 | **LOCATED** — `grep -n -F` → `167:is replaced by the normalized name for that project, so a project named` |

No quote is UNLOCATED: every quote above was found verbatim in the lane's own copy of the
bytes by the named `grep -n -F` command, and every quote is at most 25 words.

### Byte identity of the copies the quotes were located in

| copy | bytes | sha256 | provenance |
|---|---|---|---|
| `.ufo/waves/round-63/w1/recon/S228-pypi-test_outputs.py` | 3177 | `82c63517…650be4c` | equals `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` (the lane's committed capture) and equals `SHA256SUMS` line 134 `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` — so the located quote is the quote in the committed grader capture, not only in the fetched copy |
| `.ufo/waves/round-63/w1/recon/S229-pep-0503.html` | 20398 | `5b97cb7e…c453c4f` | this seat's own re-fetch of `https://peps.python.org/pep-0503/` on 2026-11-03 (`curl -sS -o s229_pep0503.html`, then `sha256sum`), byte-identical to the scout's copy |

### What each row is admitted for (scope)

- **S228** (tier A, kind `code`, scope: the grader's install and assertion contract) — admit.
  The pinned file at `2fd12b88aafdd04a52c298e3940bcb189f9766d6` is the grader this round's
  probe executes: its `install()` pins `--index-url http://localhost:8080/simple` and
  `vectorops==0.1.0` (lines 30-31) and its `test_api()` asserts four `dotproduct` values
  (lines 85-88). Tier A code, opened live 2026-11-03.
- **S229** (tier A, spec, scope: the `/simple/<name>/` index layout the probe serves) — admit.
  PEP 503 supplies the layout contract (root URL, then one URL per project at the project's
  normalized name) that the probe's lane-built index implements. Tier A spec, opened live
  2026-11-03.

Neither row's scope is widened here: S228 covers the grader's own install/assert contract
only (not the task's unfetched `test.py` simulator, not any solvability claim about a model),
and S229 covers the index layout only (not any statement about pip's behaviour, which the
lane measured directly in the K2 control receipt instead).

### Flip checks

- If either file's bytes change at the pin, the located quote's line number is void and the
  row needs a re-open with a fresh `grep -n -F` location.
- If the lane's own copy under `.ufo/waves/round-63/w1/recon/` is replaced by a different
  fetch, the location must be re-derived in that copy before the quote is re-admitted.
- A quote that is not found verbatim in the copy is to be marked **UNLOCATED** and dropped
  from the row; it is not to be re-worded to make it findable.
