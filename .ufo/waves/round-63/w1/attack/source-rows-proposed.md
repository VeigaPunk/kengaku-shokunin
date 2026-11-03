# Proposed SOURCES.md rows — S228, S229 (SourceReview, round 63)

Schema from `corpus/SOURCES.md` line 21 (header):
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`
Form matched to S227 (status `mined`, recheck `180d`, dated `opened`). No `|` inside any cell.
`used-by` = the knowledge entry path per seat spec: `corpus/knowledge/tb2-network-service-offline-grader.md`.
The L1 appends these after its validation; captures cited below land with the wave.

---

| S228 | Terminal-Bench 2.0 pypi-server grader, tests/test_outputs.py at pin 2fd12b88 (raw.githubusercontent.com) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/pypi-server/tests/test_outputs.py | code | A | the grader's install and assertion contract — install() runs python -m pip install --index-url http://localhost:8080/simple vectorops==0.1.0 and test_api() then asserts four dotproduct values | re-opened live 2026-11-03 (curl -fsSL to raw.githubusercontent.com at the pin; sha256 82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c = corpus/evidence/round52/graders/SHA256SUMS line 134; cmp byte-identical to the lane capture corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py; re-open capture committed at .ufo/waves/round-63/w1/attack/S228-reopen.py, 3177 B / 88 lines); located quotes "localhost:8080" (:18, :30), "vectorops==0.1.0" (:31, :50), "assert v.dotproduct([1, 1], [0, 1]) == 1" (:85); note "pip install --index-url" is not a contiguous string — the argv is split one token per line (:24-32) with "--index-url" alone at :29 | the R63-C1 grader under execution: leg P iff test_api() returns normally after installing vectorops==0.1.0 from a localhost:8080 index; the four asserts fix dotproduct([1,1],[0,1])==1, ([1,1,0],[1,1,0])==2, ([1,1,0,0],[1,0,0,21.2])==1, ([1,-1,0,0.01],[0,0,10,0])==0 | mined | 2026-11-03 | 180d | corpus/knowledge/tb2-network-service-offline-grader.md |

| S229 | PEP 503 — Simple Repository API — https://peps.python.org/pep-0503/ | docs | A | the /simple/<project>/ index layout the C1 probe serves — base URL plus one HTML5 page per normalized project name, each an anchor list of file URLs | re-opened live 2026-11-03 (curl -fsSL to peps.python.org; sha256 5b97cb7e14fc1a384bdfaac70195763e0b3bfca5a4c5f70142c6e37d2c453c4f, 20398 B / 269 lines; cmp byte-identical to the scout capture .ufo/waves/round-63/w1/recon/S229-pep-0503.html; re-open capture committed at .ufo/waves/round-63/w1/attack/S229-reopen.html); located quotes "https://pypi.org/simple/foo/" (:149), "Below the root URL is another URL for each individual project contained within" (:165), "is replaced by the normalized name for that project" (:167) — the /<project>/ layout text sits in the h2 "Specification" section (:140); footer "Last modified: 2025-08-20 21:30:45 UTC" (:260) | the offline index recipe for R63-C1: a root page with one anchor per project, then a per-project page under the normalized name whose anchors link the file URLs (optionally with a #sha256= digest fragment) | mined | 2026-11-03 | 180d | corpus/knowledge/tb2-network-service-offline-grader.md |

---

Notes for the L1:
- All located quotes are ≤ 25 words (largest: 19) and were verified verbatim in the re-opened bytes by this seat (`source-review.md` has the commands).
- S228's quote cell deliberately records the non-contiguity of "pip install --index-url" so no later seat greps for it as one string.
- S229's sha256 is a point-in-time live-HTML capture (2026-11-03); the PEP footer date is the stability anchor.
