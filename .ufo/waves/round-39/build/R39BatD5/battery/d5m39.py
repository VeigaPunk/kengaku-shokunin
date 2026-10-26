#!/usr/bin/env python3
"""battery39 module `d5m39` — the D5 tag-strip fixture that kills frozen mutant M07 (direction `mirror`).

Frozen mutant (`plans/round39_c1_verify.py`, M07, clause `D5`, direction `mirror`):
  old  `flat = re.sub(r"\\s+", "", re.sub(r"<[^>]+>", "", read(capture) or ""))`
  new  `flat = re.sub(r"\\s+", "", read(capture) or "")`
The mutant drops the tag strip, so it is STRICTER than the gate: a capture whose quote span
carries inline markup is accepted by the reference (`D5 ok`) and rejected by the mutant
(`D5 DEFECT`, `bad=['quote absent from the capture']`).  Pre-freeze witness, committed:
`.ufo/waves/round-38/falsify/F38XMutRerunMain/survivor-probeB.txt` — `REF tagged-capture: 0
['D5 ok directional=True digest_pinned=True bad=0']` / `X15 tagged-capture: 1 ["D5 DEFECT ..."]`.

Why the fixture is faithful to the frozen input it is built on.  The genuine D5 erratum line in
`corpus/lessons/round-34.md` (read through `ctx.d5_line()`) states the quote is present in
`nec-s091-reopen.html` "after tag-strip and whitespace removal, raw HTML line 276": tag strip is
part of the advertised reading, not a convenience.  The fixture therefore copies the frozen
capture dir, rewrites only the D5 capture so that the quote span itself carries inline markup
(bold/span/emphasis around the three thirds of the quote, inserted in place on the same raw
line), and re-pins that capture's manifest row to the new digest.  Measured on the built fixture:
60,335 -> 60,382 bytes, delta 47 = exactly the 47 bytes of inserted markup, 21 CR and 422 LF
bytes unchanged, so the erratum's "raw HTML line 276" and byte provenance keep pointing at the
same bytes and the rewrite adds markup only.  The quote occurs exactly once in the frozen capture
(asserted at build time), so after the rewrite the flat quote is present only once tags are
stripped; a build-time guard also re-checks that the tag-stripped capture text is unchanged.

`d5-line` runs exactly one clause, so the accept fixture declares `defects=[]` — the exact DEFECT
set the unmodified gate prints.  One fixture only, deliberately: with two M07-killing fixtures
neither would be individually load-bearing (removing one would leave the other a kill), and this
module's claim is that removing it makes M07 SURVIVE.
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import shutil

FID = "d5m39-tagged-quote-span"


def _mark_quote_span(text, quote):
    """Return `text` with the single `quote` occurrence wrapped in inline markup, in place."""
    hits = text.count(quote)
    if hits != 1:
        raise RuntimeError(f"fixture: the frozen capture carries the quote {hits} times, want exactly 1")
    i = text.index(quote)
    k1, k2 = len(quote) // 3, (2 * len(quote)) // 3
    marked = (
        "<b>" + quote[:k1] + "</b>"
        + '<span class="str-inner">' + quote[k1:k2] + "</span>"
        + "<em>" + quote[k2:] + "</em>"
    )
    out = text[:i] + marked + text[i + len(quote):]
    if out.count("\n") != text.count("\n"):
        raise RuntimeError("fixture: the rewrite moved the quote's raw line")
    if re.sub(r"<[^>]+>", "", out) != re.sub(r"<[^>]+>", "", text):
        raise RuntimeError("fixture: the rewrite changes the capture's tag-stripped text")
    return out


def _repin(manifest_text, capture_name, digest):
    """Rewrite every manifest row whose last field names the capture, leaving other rows byte-identical."""
    rows = []
    for row in manifest_text.splitlines():
        parts = row.split()
        if len(parts) >= 2 and parts[-1].endswith(capture_name):
            row = row.replace(parts[0], digest, 1)
        rows.append(row)
    return "\n".join(rows) + ("\n" if manifest_text.endswith("\n") else "")


def build(ctx, d):
    """Copy the frozen captures, tag the quote span in the D5 capture, re-pin its manifest row."""
    d = pathlib.Path(d)
    d5 = ctx.spec["d5"]
    capdir = d / "captures"
    shutil.copytree(ctx.d5_capture_dir(), capdir)
    cap = capdir / d5["capture_name"]
    before = cap.read_bytes().decode("utf-8")
    after = _mark_quote_span(before, d5["quote"])
    cap.write_bytes(after.encode("utf-8"))
    manifest = capdir / d5["manifest_name"]
    manifest.write_bytes(
        _repin(manifest.read_bytes().decode("utf-8"), d5["capture_name"],
               hashlib.sha256(cap.read_bytes()).hexdigest()).encode("utf-8")
    )
    line = d / "erratum.md"
    line.write_bytes((ctx.d5_line() + "\n").encode("utf-8"))
    return ["d5-line", "--file", str(line), "--capture-dir", str(capdir)]


FIXTURES = [
    {"fid": FID, "expect": "accept", "defects": [], "build": build},
]
