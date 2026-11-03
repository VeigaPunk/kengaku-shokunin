# SourceReview — scoped findings (round 63 w1)

Non-author re-verification of the round's two sources. Seat dir: `.ufo/waves/round-63/w1/attack/` (full commands and outputs: `attack/source-review.md`; proposed rows: `attack/source-rows-proposed.md`). Frozen claims read first. Scout recon (`recon/recon.md`) appeared at poll check 8 of 20 (sleep 60); its captures were `cmp`-identical to my independent re-opens before any quote work.

## Verdicts

- **S228: verified.** Re-opened live from raw.githubusercontent.com at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`: sha256 `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` (= frozen pin, = `corpus/evidence/round52/graders/SHA256SUMS` line 134), 3177 B / 88 lines, `cmp` byte-identical to the lane capture and to the scout capture. Content matches the frozen contract: `install()` → `pip install --index-url http://localhost:8080/simple vectorops==0.1.0`; `test_api()` → four `dotproduct` asserts (:85–:88).
- **S229: verified.** Re-opened live from peps.python.org: sha256 `5b97cb7e14fc1a384bdfaac70195763e0b3bfca5a4c5f70142c6e37d2c453c4f`, 20398 B / 269 lines, `cmp` byte-identical to the scout capture. The `/simple/<project>/` layout text: base-URL sentence :144, note example `https://pypi.org/simple/foo/` :149, project-URL paragraph `/<project>/` + normalized name :165–:168 — all under h2 **`Specification`** (:140); footer `Last modified: 2025-08-20 21:30:45 UTC` :260.

## Scout quote check (all ≤ 25 words)

- S228: `localhost:8080` ✓ (:18, :30); `vectorops==0.1.0` ✓ (:31, :50); `pip install --index-url` correctly reported **absent** as a contiguous string (`grep -c -F` → 0; argv split across :24–:32, `--index-url` alone :29).
- S229: "The format of this URL is /<project>/ … normalized name for that project" (19 words) ✓ across :166–:167 (docutils markup interleaved; scout noted the wrapping); "Below the root URL is another URL for each individual project contained within a repository." (15 words) ✓ across :165–:166; heading and title ✓ (:140, :92).
- One minor citation nit, data still correct: the recon echoes `grep -n -i 'last-modified'` for the footer date, but the page bytes say `Last modified:` (space) — that hyphenated pattern returns 0; verified by `grep -n -i 'modified'` → :260.

## Independent check

Claims header prints base `c78749a5565dfd…`, which does not resolve (`git rev-parse` → unknown revision); the repository's commit is `c78749a565dfd…` ("round-62 verifier spot-check (integrator, hyaku): non-author admit/reject"). Scout finding confirmed independently; frozen file not edited — dated erratum is the L1's call.

## Residual risk

- S229 sha is a point-in-time live-HTML capture (same-day double-open agrees; the PEP footer date is the stability anchor). S228 sits at an immutable commit pin.
- Registry-schema note for the L1: both proposed rows follow the S227 form (status `mined`, recheck `180d`, tier A, 11 columns, no `|` in cells); `used-by` = `corpus/knowledge/tb2-network-service-offline-grader.md` per seat spec; captures cited in the anchor cells are the seat-dir files this wave lands.

## Tooling

No installs; only `curl`, coreutils, read-only `git` were used.
