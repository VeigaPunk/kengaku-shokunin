# Python ast live-source receipt — SourcesAstR73

Axes: coverage and calibration. Source: https://docs.python.org/3/library/ast.html

## Capture

- Fetch started (UTC): `2026-11-04T02:46:48Z`.
- Executed: `curl -sS -D /fast/scratch/hyaku/kengaku-r73/SourcesAstR73/headers -o /fast/scratch/hyaku/kengaku-r73/SourcesAstR73/body --max-time 60 https://docs.python.org/3/library/ast.html`; stderr redirected to scratch `curl.err`.
- curl exit: **0**, stderr empty. Response: **HTTP/2 200**, `content-type: text/html`.
- HTTP date: `Wed, 04 Nov 2026 02:46:48 GMT`.
- HTTP last-modified: `Tue, 03 Nov 2026 17:54:14 GMT`.
- `wc -c`: **362493** bytes; `wc -l`: **3338**.
- SHA-256: **94bead0ac6482efc08bbc790acb1cff809ca4b8a9829a1def2245451a42fe809**.
- Body: `corpus/evidence/round73/sources/ast-docs.html`.
- Header excerpt: `corpus/evidence/round73/sources/ast-headers.txt` (selected raw-header lines, LF-normalized).
- Executed `cmp -s` between downloaded body and saved capture: identical branch printed `cmp=identical`; both `sha256sum` outputs matched the hash above.

## Located quotations

Line numbers refer to the captured HTML, not rendered browser text. Quotes below remove HTML tags and collapse layout whitespace only.

### ast.parse

URL: https://docs.python.org/3/library/ast.html#ast.parse

Anchor `id="ast.parse"`: capture **L2678**. Quote at **L2680** (7 words):

> Parse the source into an AST node.

Supporting mechanism: L2680–2683 describes equivalence to `compile` with `ast.PyCF_ONLY_AST` or `ast.PyCF_OPTIMIZED_AST`; anchor `id="ast.PyCF_ONLY_AST"` is at L3036, with this quote at **L3038–3039** (14 words):

> Generates and returns an abstract syntax tree instead of returning a compiled code object.

Supporting URL: https://docs.python.org/3/library/ast.html#ast.PyCF_ONLY_AST

Gap: the page explicitly describes parsing into an AST but does not explicitly say that `ast.parse` works “without executing it,” so that clause is an inference from the AST-return and separate-compilation descriptions, not a quotation.

Do not transfer the explicit non-execution wording at L2768–2771 to `ast.parse`: that passage describes `ast.literal_eval` instead.

### ast.walk

URL: https://docs.python.org/3/library/ast.html#ast.walk

Anchor `id="ast.walk"`: capture **L2862**. Quote at **L2864–2865** (18 words):

> Recursively yield all descendant nodes in the tree starting at node (including node itself), in no specified order.

This grounds recursive descendant traversal, including the root; it does not promise traversal order.

## Revision and opened date

Observed named version: **Python 3.15.2 documentation**, in the title at capture **L20** and navigation at **L3282**. Footer **L3328** states:

> Last updated on Nov 03, 2026 (17:52 UTC).

Use `opened: 2026-11-04` for the measured UTC retrieval date; retain the version/build stamp and capture SHA separately. The HTTP last-modified timestamp and footer update timestamp are different observed values; their cause was not investigated.

## Executed evidence checks

- `sha256sum` on downloaded and saved bodies: matching hash above; `wc -c` = 362493.
- Literal anchor searches: one occurrence each; `ast.parse` L2678, `ast.walk` L2862, `ast.PyCF_ONLY_AST` L3036.
- Literal search `without execut`: no hit, grep rc **1**; normalized-text checks also found zero occurrences of `does not execut` and `never execut`.
- Python HTML-tag removal/entity-unescape/whitespace-collapse comparison: all nine tested substrings matched their cited spans, printing `ALL_CHECKS_PASS`; primary parse quote 7 words, AST-return quote 14 words, walk quote 18 words. The script ran successfully (rc 0).

No registry predicate, counting command, target, repository code, or registry row was changed. No gate/audit outcome is claimed by this source receipt.
