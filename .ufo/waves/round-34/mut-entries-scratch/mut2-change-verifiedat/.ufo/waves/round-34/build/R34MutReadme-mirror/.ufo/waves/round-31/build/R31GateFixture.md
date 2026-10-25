# R31GateFixture — C3 scratch proof: `--url-map` binding is failure-capable

Round 31, lane kengaku-shokunin, claim C3 (`plans/round-31-claims.md`, "the adoption gate binds
the capture to the row's cited URL"). Leaf seat: no subagent dispatch, no production edit, one
report file. Scratch: `/tmp/r31-R31GateFixture/` (376 KB, nothing deleted outside it).

Lane tip at the time of this seat: `0883e72ef8474ca42ac1a54eb0273079f1507035` (`git log -1`).
Access date for this round: 2026-10-25. No tool was installed or upgraded by this seat.

## 0. What was copied, and one finding about the lane working tree

| file in scratch | origin | sha256 |
|---|---|---|
| `baseline.py` | `git show 0883e72:plans/sources_adopt.py` (pristine committed bytes, 815 lines) | `47e60021966318c9f36d4cab8e1464a8cd333db114eca3c1689d206cdfef7922` |
| `sources_adopt.py` | `baseline.py` + the prototype below (1008 lines) | `6d7fa16a53b895473b0a8df7bb235ed0d47cd0e77cbc7ff9c1785f54d7ea1c3c` |
| `mutant-no-binding.py` | `sources_adopt.py` with the 10-line enforcement block deleted | `85ad8e0115503f2b333d8e3d0176df80eeb9376e7fb10b2065068dee1558914a` |
| `sources_adopt.inflight.py` | copy of the **lane working tree** file taken at seat start | `edc60be07b6640bf498ad65eaeeca701b05955234f138fdf5eb279d244832e4d` |
| `sources_adopt.tree-latest.py` | copy of the lane working tree file taken later in the seat | `39ba62b22915bdcf6943dc2a860bd338a77cbd1d9b92064ab75edd54cda9bc71` |

**Finding (ground truth, not a plan): the lane working tree is dirty while this wave is in
flight, and it is moving under the seat.** `git status --porcelain plans/sources_adopt.py` → ` M
plans/sources_adopt.py`; `git diff --stat plans/sources_adopt.py` → `1 file changed, 129
insertions(+), 5 deletions(-)` at seat start. Two snapshots, both read-only copies into scratch:

| snapshot | lane file sha256 | `--selftest` | CLI `--quote-file/--artifact` |
|---|---|---|---|
| `sources_adopt.inflight.py` (seat start) | `edc60be07b6640bf498ad65eaeeca701b05955234f138fdf5eb279d244832e4d` | `cases=14` | `--url-map` → `NameError: name 'json' is not defined`, exit 1 |
| `sources_adopt.tree-latest.py` (later) | `39ba62b22915bdcf6943dc2a860bd338a77cbd1d9b92064ab75edd54cda9bc71` | `cases=17 failed=0` | **dead: exit 2, `--registry and --package are required unless --selftest`** |

Seat-start snapshot, verbatim:

```
$ python3 sources_adopt.inflight.py --selftest | tail -2
CASE quote-boundary-25-accepted PASS
SELFTEST cases=14 failed=0

$ python3 sources_adopt.inflight.py --quote-file cli/rows.txt --artifact cli/capture.txt \
      --url-map cli/map-ok.json
    except (OSError, json.JSONDecodeError) as error:
                     ^^^^
NameError: name 'json' is not defined. Did you forget to import 'json'?
EXIT=1
```

Later snapshot: the in-process cases now pass, but the CLI dispatch is broken — the quote block was
moved under `elif args.url_map:` **after** a `parser.error(...)`, so it is unreachable and every
quote invocation falls through to the registry branch (`logs/10`, `logs/11`, `logs/12`):

```
$ python3 sources_adopt.tree-latest.py --selftest | tail -4
CASE quote-url-bound-accepted PASS
CASE quote-url-mismatch-refused PASS
CASE quote-url-unmapped-refused PASS
SELFTEST cases=17 failed=0
EXIT=0

$ python3 sources_adopt.tree-latest.py --quote-file cli/rows.txt --artifact cli/capture.txt \
      --url-map cli/map-ok.json
sources_adopt.tree-latest.py: error: --registry and --package are required unless --selftest
EXIT=2

$ python3 sources_adopt.tree-latest.py --quote-file cli/rows.txt --artifact cli/capture.txt
sources_adopt.tree-latest.py: error: --registry and --package are required unless --selftest
EXIT=2
```

That second command is the pre-existing capability 5 with no `--url-map` at all: it is dead in the
working tree, and the working tree's own selftest cannot see it because its cases call
`quote_check()` in process and never `main()`. This is exactly why the C3 predicate is stated as a
`--selftest` count *plus* a control invocation: a case count alone does not prove the flag works.

The proof below is against the **committed** baseline, which is what the frozen predicate's control
names (`git show 0883e72:plans/sources_adopt.py`). The L1 must land the diff in §5 on the committed
bytes (or bring the working tree to the state in `apply/plans/sources_adopt.py`) — the diff does not
apply to the dirty copy, for the reason recorded in §6.

## 1. (a) Baseline behaviour — the control cannot reach the target

`--url-map` on the pristine bytes (this is the exact invocation form the claim requires, not a
bare flag):

```
$ python3 baseline.py --quote-file cli/rows.txt --artifact cli/capture.txt --url-map cli/map-ok.json
usage: baseline.py [-h] [--selftest] [--registry REGISTRY] [--package PACKAGE]
                   [--admit-ids ADMIT_IDS] [--entries ENTRIES]
                   [--access-date ACCESS_DATE] [--recheck RECHECK] [--out OUT]
                   [--quote-file QUOTE_FILE] [--artifact ARTIFACT]
                   [--attest-opened] [--scope-to-admit]
baseline.py: error: unrecognized arguments: --url-map cli/map-ok.json
EXIT=2
```

(`logs/02-baseline-urlmap.txt`. The same run with a bare `--url-map /tmp/.../urlmap.json` gives
the identical argparse text and `EXIT=2`.)

Baseline selftest, verbatim (`logs/01-baseline-selftest.txt`):

```
CASE collision-zero-indent PASS
CASE collision-one-space PASS
CASE collision-three-space PASS
CASE four-space-not-a-row PASS
CASE escaped-pipe-refused PASS
CASE prose-recheck-normalized PASS
CASE usedby-projected PASS
CASE duplicate-staged-id PASS
CASE clean-package-passes PASS
CASE missing-requested-id PASS
CASE quote-overlong-refused PASS
CASE quote-absent-refused PASS
CASE quote-located-accepted PASS
CASE quote-boundary-25-accepted PASS
SELFTEST cases=14 failed=0
EXIT=0
```

Both control facts in the frozen predicate hold on the committed bytes: argparse exit **2** and
`cases=14`.

## 2. (b) The prototype, in the /tmp copy only

Minimal surface, no new module, no change to any existing exit code or to the registry branch:

* `EXIT_URL_MISMATCH = 8`, `EXIT_URL_UNMAPPED = 9`, plus `import json`.
* `SOURCE_COLUMN = 1` (the `source` cell carries `title — URL`), `URL_RE`, `cited_urls()`,
  `normalize_url()`, `load_url_map()`, `bind_citation()`.
* `quote_check(..., url_map=None)`: binding runs **only** for a span that located inside the cap,
  so the documented refusal order becomes `2, 4, 6, 7, 8, 9` — an absent quote is absent whatever
  its capture was fetched from, and an unmapped artifact is only reachable once there is a located
  quote to bind.
* `main`: `--url-map` argument; unreadable/non-object map → `parser.error` (exit 2, caller defect,
  never a binding verdict); `--url-map` without `--quote-file/--artifact` → `parser.error`.
* `print_quote_report` gains `mismatch={mis} unmapped={unm}`; the per-row detail lines name the
  artifact and both URLs, so a refusal is repairable from the receipt.

Normalisation is deliberately narrow: fragment dropped, trailing slash dropped, scheme and host
lowered; path stays case-sensitive, a subpath is a different document, `http` is not `https`.

### CLI evidence (real invocations, `logs/05-proto-cli-*.txt`)

```
$ python3 sources_adopt.py --quote-file cli/rows.txt --artifact cli/capture.txt --url-map cli/map-ok.json
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 mismatch=0 unmapped=0 cap=25 artifacts=capture.txt
  ok S930 words=9 at capture.txt quote="the harness resolves the verifier outside the agent sandbox"
  ok S930 artifact capture.txt bound to https://example.invalid/x
EXIT=0

$ python3 sources_adopt.py --quote-file cli/rows.txt --artifact cli/capture.txt --url-map cli/map-wrong.json
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 mismatch=1 unmapped=0 cap=25 artifacts=capture.txt
  ok S930 words=9 at capture.txt quote="the harness resolves the verifier outside the agent sandbox"
  REFUSED S930 artifact capture.txt maps to https://example.invalid/y but cites https://example.invalid/x
EXIT=8

$ python3 sources_adopt.py --quote-file cli/rows.txt --artifact cli/capture.txt --url-map cli/map-empty.json
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 mismatch=0 unmapped=1 cap=25 artifacts=capture.txt
  ok S930 words=9 at capture.txt quote="the harness resolves the verifier outside the agent sandbox"
  REFUSED S930 artifact capture.txt has no --url-map entry
EXIT=9
```

`cli/rows.txt` is a registry-shaped row whose `source` cell cites `https://example.invalid/x` and
whose anchor cell quotes a sentence that is present in `cli/capture.txt`; the three runs differ
only in the map file (`cli/map-ok.json`, `cli/map-wrong.json`, `cli/map-empty.json`).

Backwards compatibility and caller-error paths:

```
$ python3 sources_adopt.py --quote-file cli/rows.txt --artifact cli/capture.txt      # no --url-map
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 mismatch=0 unmapped=0 cap=25 artifacts=capture.txt
  ok S930 words=9 at capture.txt quote="the harness resolves the verifier outside the agent sandbox"
EXIT=0                                                        # logs/07-proto-nomap.txt

$ python3 sources_adopt.py --quote-file cli/rows-nourl.txt --artifact cli/capture.txt --url-map cli/map-ok.json
  ok S931 words=9 at capture.txt quote="the harness resolves the verifier outside the agent sandbox"
  REFUSED S931 artifact capture.txt maps to https://example.invalid/x but cites <no-url>
EXIT=8                                                        # logs/08-proto-nourl.txt
                                                              # a row citing no URL cannot bind

$ python3 sources_adopt.py --quote-file cli/rows.txt --artifact cli/capture.txt --url-map cli/map-notjson.json
sources_adopt.py: error: --url-map is unreadable: Expecting ',' delimiter: line 2 column 1 (char 44)
EXIT=2                                                        # logs/09-proto-badmap.txt

$ python3 sources_adopt.py --url-map cli/map-ok.json
sources_adopt.py: error: --url-map requires --quote-file and --artifact
EXIT=2
```

## 3. (c) Three new selftest cases — failure-capable, shown both ways

Cases 15–17 are appended after the existing case 14 and use the file's own `case()` helper:

* `urlmap-cited-url-accepted` — located quote, artifact mapped to the cited URL (written as
  `https://EXAMPLE.invalid/x/#section-2`, so scheme/host case, a fragment and a trailing slash are
  exercised as the *same* document). Asserts `EXIT_OK`, empty `url_mismatch`/`url_unmapped`, **and
  that the receipt carries the binding line** (`len(quotes) == 2` and one `bound to` detail) —
  otherwise the accept would be "no refusal happened", which the unmodified body also satisfies.
* `urlmap-mismatch-refused` — same row/artifact mapped to `https://example.invalid/y`, and again to
  the subpath `https://example.invalid/x/deeper`: both `EXIT_URL_MISMATCH` (8), with `located` and
  `found` still recorded (the refusal is the citation, not the bytes).
* `urlmap-unmapped-refused` — empty map: `EXIT_URL_UNMAPPED` (9); plus the precedence assertion
  that the same unmapped artifact with a quote that is *absent* still exits 7.

### With the binding code — PASS (`logs/03-proto-selftest.txt`)

```
CASE collision-zero-indent PASS
CASE collision-one-space PASS
CASE collision-three-space PASS
CASE four-space-not-a-row PASS
CASE escaped-pipe-refused PASS
CASE prose-recheck-normalized PASS
CASE usedby-projected PASS
CASE duplicate-staged-id PASS
CASE clean-package-passes PASS
CASE missing-requested-id PASS
CASE quote-overlong-refused PASS
CASE quote-absent-refused PASS
CASE quote-located-accepted PASS
CASE quote-boundary-25-accepted PASS
CASE urlmap-cited-url-accepted PASS
CASE urlmap-mismatch-refused PASS
CASE urlmap-unmapped-refused PASS
SELFTEST cases=17 failed=0
EXIT=0
```

### With the binding code removed — all three new cases FAIL (`logs/04-mutant-selftest.txt`)

The mutant is the prototype with exactly this block deleted (nothing else; `diff -u` of the two):

```
@@ -497,16 +497,6 @@
             else:
                 located.append(row.row_id)
                 details.append(("ok", f'{row.row_id} words={count} at {where} quote="{quote}"'))
-                if url_map is not None:
-                    verdict, detail = bind_citation(row, where, url_map)
-                    if verdict == "mismatch":
-                        mismatch.append(row.row_id)
-                        details.append(("REFUSED", detail))
-                    elif verdict == "unmapped":
-                        unmapped.append(row.row_id)
-                        details.append(("REFUSED", detail))
-                    else:
-                        details.append(("ok", detail))
     report.update(
```

Run:

```
CASE collision-zero-indent PASS
CASE collision-one-space PASS
CASE collision-three-space PASS
CASE four-space-not-a-row PASS
CASE escaped-pipe-refused PASS
CASE prose-recheck-normalized PASS
CASE usedby-projected PASS
CASE duplicate-staged-id PASS
CASE clean-package-passes PASS
CASE missing-requested-id PASS
CASE quote-overlong-refused PASS
CASE quote-absent-refused PASS
CASE quote-located-accepted PASS
CASE quote-boundary-25-accepted PASS
CASE urlmap-cited-url-accepted FAIL
CASE urlmap-mismatch-refused FAIL
CASE urlmap-unmapped-refused FAIL
SELFTEST cases=17 failed=3
  failed: urlmap-cited-url-accepted urlmap-mismatch-refused urlmap-unmapped-refused
EXIT=1
```

The fourteen pre-existing cases still pass on the mutant, so the three failures are caused by the
removal and not by a broken fixture. At the CLI level the mutant reproduces the round-30 gap the
claim is about — a capture of a *different* document greens the row:

```
$ python3 mutant-no-binding.py --quote-file cli/rows.txt --artifact cli/capture.txt --url-map cli/map-wrong.json
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 mismatch=0 unmapped=0 cap=25 artifacts=capture.txt
  ok S930 words=9 at capture.txt quote="the harness resolves the verifier outside the agent sandbox"
EXIT=0
```

(`logs/06-mutant-cli-wrong.txt`; the same mutant run against `map-ok.json` and `map-empty.json`
also exits 0, `logs/06-mutant-cli-ok.txt`, `logs/06-mutant-cli-empty.txt`.)

## 4. Applicability of the diff

The diff in §5 is generated from `baseline.py` and applies cleanly to the committed blob:

```
$ cp baseline.py apply/plans/sources_adopt.py && cd apply && patch -p1 --dry-run < ../gate.diff
checking file plans/sources_adopt.py
$ patch -p1 < ../gate.diff >/dev/null && sha256sum plans/sources_adopt.py
6d7fa16a53b895473b0a8df7bb235ed0d47cd0e77cbc7ff9c1785f54d7ea1c3c  plans/sources_adopt.py
```

Byte-identical to the prototype that produced the two selftest runs, and the patched tree prints
`SELFTEST cases=17 failed=0`.

## 5. Exact diff to apply to the lane file (against `0883e72:plans/sources_adopt.py`)

```diff
--- a/plans/sources_adopt.py
+++ b/plans/sources_adopt.py
@@ -20,7 +20,10 @@
      duplicate staged id, or a nonempty collision set;
   5. quote validation (`--quote-file`/`--artifact`): every quoted span in a supplied
      row's anchor cell is measured against the contract's <=25-word cap and located
-     as a byte substring of the named artifact, with its own exit codes.
+     as a byte substring of the named artifact, with its own exit codes;
+  6. capture-to-citation binding (`--url-map`): the artifact that located a quote must be
+     mapped to the URL that row's `source` cell cites, so a capture of some other document
+     cannot satisfy a row it happens to share a sentence with.
 
 Scope: registry row mechanics and quote presence only. Source truth, tier judgement
 and the census itself stay where they are (CORPUS.md contract v1; census is
@@ -29,6 +32,7 @@
 from __future__ import annotations
 
 import argparse
+import json
 import re
 import sys
 import tempfile
@@ -48,6 +52,8 @@
 EXIT_REQUEST = 5
 EXIT_QUOTE_TOO_LONG = 6
 EXIT_QUOTE_ABSENT = 7
+EXIT_URL_MISMATCH = 8  # the artifact that located the quote is mapped to a different document
+EXIT_URL_UNMAPPED = 9  # the artifact that located the quote has no --url-map entry
 
 
 class Row:
@@ -337,7 +343,85 @@
     return next((name for name, text in loaded if needle in text), "")
 
 
-def quote_check(quote_file: Path, artifact: Path, cap: int = QUOTE_WORDS) -> tuple[int, dict[str, object]]:
+# ------------------------------------------------------------------- citation binding
+
+# The anchor cell is not where a row cites its document: `source` (cell 1) carries
+# "title — URL". A row can therefore locate its quote in a capture of a *different*
+# document, which is the gap round 30 disclosed. `--url-map` closes it by naming the
+# document each artifact was fetched from.
+SOURCE_COLUMN = 1
+URL_RE = re.compile(r"https?://[^\s|]+")
+
+
+def cited_urls(cell: str) -> list[str]:
+    """Every http(s) URL the row's `source` cell carries, trailing punctuation trimmed."""
+    return [url.rstrip(".,;:)]}") for url in URL_RE.findall(cell)]
+
+
+def normalize_url(url: str) -> str:
+    """Comparable form of a URL: no fragment, no trailing slash, scheme and host lowered.
+
+    Deliberately narrow. The path stays case-sensitive (GitHub paths are), a subpath is a
+    different document, and `http` is not `https`: those are the three cases a looser
+    normalisation would silently pass, and each of them is a wrong citation, not a
+    formatting difference.
+    """
+    text = url.strip().split("#", 1)[0]
+    match = re.match(r"^(https?)://([^/]*)(.*)$", text, re.IGNORECASE)
+    if not match:
+        return text
+    scheme, host, rest = match.group(1).lower(), match.group(2).lower(), match.group(3)
+    return f"{scheme}://{host}{rest}".rstrip("/")
+
+
+def load_url_map(path: Path) -> tuple[dict[str, str], str]:
+    """Return ({artifact name: url}, problem).
+
+    The map is a flat JSON object: `{"<artifact name>": "<url>"}` where the key is the
+    name `load_artifact` prints for that capture (a file artifact's basename, a directory
+    artifact's relative path). A nested shape is refused rather than guessed: a map the
+    gate half-understands is worse than no map.
+    """
+    try:
+        data = json.loads(path.read_text(encoding="utf-8"))
+    except (OSError, json.JSONDecodeError) as error:
+        return {}, f"--url-map is unreadable: {error}"
+    if not isinstance(data, dict):
+        return {}, "--url-map must be a JSON object of artifact name to URL"
+    mapping: dict[str, str] = {}
+    for key, value in data.items():
+        if not isinstance(key, str) or not isinstance(value, str):
+            return {}, "--url-map must map strings to strings"
+        mapping[key] = value
+    return mapping, ""
+
+
+def bind_citation(row: Row, artifact_name: str, url_map: dict[str, str]) -> tuple[str, str]:
+    """Return (verdict, detail) for a quote located in `artifact_name`.
+
+    `ok` when the artifact is mapped to a URL the row's `source` cell cites; `mismatch`
+    when it is mapped to any other document; `unmapped` when the map does not name the
+    artifact at all. A row that cites no URL cannot bind, so it is a mismatch rather than
+    a silent pass: there is no citation for the capture to be the citation of.
+    """
+    cited = [normalize_url(url) for url in cited_urls(row.cell(SOURCE_COLUMN))]
+    if artifact_name not in url_map:
+        return "unmapped", f"{row.row_id} artifact {artifact_name} has no --url-map entry"
+    captured = normalize_url(url_map[artifact_name])
+    if captured not in cited:
+        return "mismatch", (
+            f"{row.row_id} artifact {artifact_name} maps to {url_map[artifact_name]} "
+            f"but cites {', '.join(cited) if cited else '<no-url>'}"
+        )
+    return "ok", f"{row.row_id} artifact {artifact_name} bound to {url_map[artifact_name]}"
+
+
+def quote_check(
+    quote_file: Path,
+    artifact: Path,
+    cap: int = QUOTE_WORDS,
+    url_map: dict[str, str] | None = None,
+) -> tuple[int, dict[str, object]]:
     """Validate the quoted text each supplied row's anchor cell carries.
 
     Two refusals, deliberately separable: a span longer than `cap` words (exit 6)
@@ -347,6 +431,13 @@
     unparsable row, a cell with no or an unbalanced quoted span) exit 4, and an
     unreadable artifact exits 2. The first refusal in the order 2, 4, 6, 7 wins;
     every refused row is still named, so one run surfaces all of them.
+
+    With `url_map` the locatedness test is bound to the citation: a span that
+    located in an artifact mapped to a URL the row does not cite exits 8, and one
+    whose artifact the map does not name exits 9. Both run only for a span that
+    located inside the cap, so the order is 2, 4, 6, 7, 8, 9 -- an absent quote is
+    absent whatever its capture was fetched from, and an unmapped artifact is only
+    reachable once there is a located quote to bind.
     """
     loaded, problem = load_artifact(artifact)
     report: dict[str, object] = {
@@ -358,6 +449,8 @@
         "overlong": [],
         "absent": [],
         "malformed": [],
+        "url_mismatch": [],
+        "url_unmapped": [],
         "artifacts": [name for name, _ in loaded],
         "problem": problem,
         "quotes": [],
@@ -369,6 +462,8 @@
     found: list[str] = []
     overlong: list[str] = []
     absent: list[str] = []
+    mismatch: list[str] = []
+    unmapped: list[str] = []
     malformed = [f"{row_id}:{reason}" for _, row_id, reason in bad]
     details: list[tuple[str, str]] = []
     spans_total = 0
@@ -402,6 +497,16 @@
             else:
                 located.append(row.row_id)
                 details.append(("ok", f'{row.row_id} words={count} at {where} quote="{quote}"'))
+                if url_map is not None:
+                    verdict, detail = bind_citation(row, where, url_map)
+                    if verdict == "mismatch":
+                        mismatch.append(row.row_id)
+                        details.append(("REFUSED", detail))
+                    elif verdict == "unmapped":
+                        unmapped.append(row.row_id)
+                        details.append(("REFUSED", detail))
+                    else:
+                        details.append(("ok", detail))
     report.update(
         {
             "rows": len(rows),
@@ -411,6 +516,8 @@
             "overlong": overlong,
             "absent": absent,
             "malformed": malformed,
+            "url_mismatch": mismatch,
+            "url_unmapped": unmapped,
             "quotes": details,
         }
     )
@@ -420,6 +527,10 @@
         return EXIT_QUOTE_TOO_LONG, report
     if absent:
         return EXIT_QUOTE_ABSENT, report
+    if mismatch:
+        return EXIT_URL_MISMATCH, report
+    if unmapped:
+        return EXIT_URL_UNMAPPED, report
     return EXIT_OK, report
 
 
@@ -429,7 +540,8 @@
         return
     print(
         "QUOTE rows={rows} spans={spans} located={loc} found={found} overlong={long} "
-        "absent={absent} malformed={mal} cap={cap} artifacts={arts}".format(
+        "absent={absent} malformed={mal} mismatch={mis} unmapped={unm} cap={cap} "
+        "artifacts={arts}".format(
             rows=report["rows"],
             spans=report["spans"],
             loc=len(report["located"]),
@@ -437,6 +549,8 @@
             long=len(report["overlong"]),
             absent=len(report["absent"]),
             mal=len(report["malformed"]),
+            mis=len(report["url_mismatch"]),
+            unm=len(report["url_unmapped"]),
             cap=report["cap"],
             arts=",".join(report["artifacts"]),
         )
@@ -715,6 +829,70 @@
             and qreport["cap"] == 25,
         )
 
+        # 15. a quote located in an artifact mapped to the URL the row cites is accepted,
+        #     and the receipt names the binding: scheme/host case, a fragment and a
+        #     trailing slash are the same document, never a refusal
+        bound_quote = "the harness resolves the verifier outside the agent sandbox"
+        art = write("artifact-bound.txt", f"intro\n{bound_quote}.\n")
+        qfile = write("quotes-bound.txt", HEADER + quote_row("S024", f'line 7: "{bound_quote}"'))
+        url_map = {"artifact-bound.txt": "https://EXAMPLE.invalid/x/#section-2"}
+        loaded_map, map_problem = load_url_map(write("urlmap-ok.json", json.dumps(url_map)))
+        code, qreport = quote_check(qfile, art, url_map=url_map)
+        bound_details = [detail for label, detail in qreport["quotes"] if "bound to" in detail]
+        case(
+            "urlmap-cited-url-accepted",
+            code == EXIT_OK
+            and qreport["located"] == ["S024"]
+            and qreport["url_mismatch"] == []
+            and qreport["url_unmapped"] == []
+            # the accept is a binding that happened, not merely a refusal that did not:
+            # the receipt carries the located line plus the binding line
+            and len(qreport["quotes"]) == 2
+            and len(bound_details) == 1
+            and "artifact-bound.txt" in bound_details[0]
+            and loaded_map == url_map
+            and not map_problem
+            and normalize_url("https://Example.INVALID/x/#frag") == "https://example.invalid/x"
+            and cited_urls(GOOD_ROW.split("|")[2]) == ["https://example.invalid/x"],
+        )
+
+        # 16. the same located quote in an artifact mapped to a different document is
+        #     refused with 8, and a subpath of the cited URL is a different document too
+        code, qreport = quote_check(qfile, art, url_map={"artifact-bound.txt": "https://example.invalid/y"})
+        deeper_code, deeper_report = quote_check(
+            qfile, art, url_map={"artifact-bound.txt": "https://example.invalid/x/deeper"}
+        )
+        case(
+            "urlmap-mismatch-refused",
+            code == EXIT_URL_MISMATCH
+            and qreport["url_mismatch"] == ["S024"]
+            and qreport["url_unmapped"] == []
+            # locatedness is still recorded: the refusal is the citation, not the bytes
+            and qreport["located"] == ["S024"]
+            and qreport["found"] == ["S024"]
+            and deeper_code == EXIT_URL_MISMATCH
+            and deeper_report["url_mismatch"] == ["S024"],
+        )
+
+        # 17. a located quote whose artifact the map does not name is refused with 9,
+        #     and absence (7) still outranks binding: an unmapped artifact cannot turn
+        #     an absent quote into a binding verdict
+        code, qreport = quote_check(qfile, art, url_map={})
+        absent_q = write(
+            "quotes-bound-absent.txt", HEADER + quote_row("S025", 'line 7: "not in the capture"')
+        )
+        absent_code, absent_report = quote_check(absent_q, art, url_map={})
+        case(
+            "urlmap-unmapped-refused",
+            code == EXIT_URL_UNMAPPED
+            and qreport["url_unmapped"] == ["S024"]
+            and qreport["url_mismatch"] == []
+            and qreport["located"] == ["S024"]
+            and absent_code == EXIT_QUOTE_ABSENT
+            and absent_report["absent"] == ["S025"]
+            and absent_report["url_unmapped"] == [],
+        )
+
     failed = [name for name, passed in cases if not passed]
     print(f"SELFTEST cases={len(cases)} failed={len(failed)}")
     if failed:
@@ -748,6 +926,12 @@
         help="source file or directory the quotes must occur in (needs --quote-file)",
     )
     parser.add_argument(
+        "--url-map",
+        type=Path,
+        help='JSON object mapping each artifact name to the URL it was fetched from '
+        "(needs --quote-file/--artifact; a located quote must bind to a URL its row cites)",
+    )
+    parser.add_argument(
         "--attest-opened",
         action="store_true",
         help="assert the requested rows were opened on --access-date (re-dates their opened cell)",
@@ -767,9 +951,18 @@
         # work and exited 0 (found by the round-30 regression seat).
         if args.registry or args.package:
             parser.error("--quote-file/--artifact cannot be combined with --registry/--package")
-        code, report = quote_check(args.quote_file, args.artifact)
+        url_map = None
+        if args.url_map:
+            url_map, problem = load_url_map(args.url_map)
+            # An unreadable map is a caller defect, not a row defect: refuse it with the
+            # usage exit (2) so it can never read as a binding verdict (8 or 9).
+            if problem:
+                parser.error(problem)
+        code, report = quote_check(args.quote_file, args.artifact, url_map=url_map)
         print_quote_report(report)
         return code
+    if args.url_map:
+        parser.error("--url-map requires --quote-file and --artifact")
     if not args.registry or not args.package:
         parser.error("--registry and --package are required unless --selftest")
     want = [item for item in args.admit_ids.split(",") if item]
```

## 6. Risks / notes for the L1

1. **Dirty working tree (highest).** `plans/sources_adopt.py` was already modified when this seat
   started (129 insertions, sha `edc60be…`), and it changed again during the seat
   (sha `39ba62b2…`). The latest working-tree copy prints `SELFTEST cases=17 failed=0` but **its
   quote CLI is dead**: `--quote-file/--artifact` with or without `--url-map` exits 2 with
   `--registry and --package are required unless --selftest`, because its quote block sits under
   `elif args.url_map:` after a `parser.error(...)` and is unreachable. That also kills the
   pre-existing capability 5 in the working tree, and no in-process selftest case can see it.
   Applying §5 to the dirty copy is refused by `patch --dry-run`: `Reversed (or previously applied)
   patch detected!`, `15 out of 15 hunks ignored` (`PATCH_DRYRUN_EXIT=1`). Land §5 on the committed
   bytes, or bring the working tree to the state in `apply/plans/sources_adopt.py`, then re-run
   `--selftest` for `SELFTEST cases=17 failed=0` **and** one real
   `--quote-file/--artifact/--url-map` invocation for exit 0 before claiming C3.
2. The frozen predicate also asserts the control line `git show 0883e72:plans/sources_adopt.py`
   rejects the invocation with argparse exit 2 — reproduced above verbatim, so that clause is met.
3. `--url-map` is accepted only together with `--quote-file/--artifact`; the registry branch is
   untouched, and all fourteen pre-existing cases still pass unchanged, so no existing caller of
   this gate changes behaviour.
4. No exit code was reused: 8 and 9 were free (existing set `0,2,3,4,5,6,7`).
5. No tool install, no pacman transaction, no write outside `/tmp/r31-R31GateFixture/` and this
   report; the lane file, `.ufo/state`, and the shokuknow tree were read only.

VERDICT: PASS — on the committed baseline (`0883e72`) the control cannot reach the target (argparse exit 2, `cases=14`), the /tmp prototype reaches `SELFTEST cases=17 failed=0` with real CLI exits 0/8/9, and all three new cases FAIL (`cases=17 failed=3`, exit 1) when the binding block alone is removed; landing requires the L1 to apply the §5 diff to the committed bytes because the lane working tree currently holds a different, non-reaching in-flight edit.
