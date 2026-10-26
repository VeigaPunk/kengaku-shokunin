"""Round-38 C1 battery38 (seat R38BatP3): mutant N02, clause P3, direction mirror.

N02 replaces `len(locs) >= rules["min_distinct_locations"]` with `>`, i.e. it stops accepting a package whose
Located-quotes table carries exactly min_distinct_locations distinct (capture, line) locations — the boundary
the frozen round-35 spec sits on (min_quotes=8, min_distinct_locations=8).

One fixture, one mutant: the GENUINE round-35 package (every clause already green) with its quote table cut
down to exactly min_distinct_locations data rows, each kept row genuine (so verbatim on its cited line, inside
the word range, unique text, unique location) and every other clause untouched. Reference: P3 ok, no DEFECT,
exit 0. Mutant: P3 DEFECT, exit 1. Mirror kill = reference printed P3 ok and the mutant prints it DEFECT.

The kept-row order is the genuine order (quotes 0..7 of the entry), so the fixture is deterministic and the
counter's renamed-copy rerun sees the same bytes.
"""

import pathlib

FID = "p3m-exact-min-distinct-locations"


def _keep(data_rows, want, row_re):
    """First `want` genuine data rows with pairwise distinct texts and pairwise distinct (capture, start)."""
    keep, texts, locs = [], set(), set()
    for line in data_rows:
        m = row_re.match(line)
        if not m:
            continue
        text, capture, start = m.group(1), m.group(2), int(m.group(3))
        if text in texts or (capture, start) in locs:
            continue
        texts.add(text)
        locs.add((capture, start))
        keep.append(line)
        if len(keep) == want:
            break
    return keep


def build(ctx, d):
    ctx.genuine_package(d)
    rules = ctx.spec["entry_rules"]
    want = int(rules["min_distinct_locations"])
    if int(rules["min_quotes"]) > want:
        raise RuntimeError("fixture would also break min_quotes")
    entry = d / pathlib.PurePosixPath(ctx.spec["entry"])
    text = entry.read_text()
    qr = ctx.r36.QUOTE_ROW

    def cut(data):
        kept = _keep(data, want, qr)
        if len(kept) != want:
            raise RuntimeError(f"genuine table has {len(kept)} usable rows, need {want}")
        return kept

    entry.write_text(ctx.r36.rewrite_quotes(text, cut))
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


FIXTURES = [{"fid": FID, "expect": "accept", "defects": [], "build": build}]
