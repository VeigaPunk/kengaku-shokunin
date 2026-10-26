"""battery43 a_err — erratum-exemption fixtures for the frozen near-variants NA7, NA20 and NA21 of
`plans/anchor_digest_check.py`.

Every fixture here is an anchor lane that the UNMODIFIED tool prints `defects=0` on (exit 0), and each
one makes a different line of the exemption code decide the verdict:

  NA7   `anchor_digest_check.py:112-113` — the erratum line's own token check. Dropping `t not in allowed`
        flags a correction digest that is committed evidence. Killed by f1/f2 (a lane that no exemption is
        needed for: the row is already repaired, the erratum is historical, and only the dropped guard
        turns it red) and by f3/f4/f6 (where the flag lands beside a live exemption).
  NA20  `anchor_digest_check.py:435` — `exempt.setdefault(...)` replaced by `pass`: exemption never granted.
        Killed by f3/f4/f5/f6, each green only because the row's stale token is excused.
  NA21  `anchor_digest_check.py:434` — `cited_wrong` membership keyed on the row ids instead of the row's
        anchor tokens, so it is always empty: the erratum line self-check loses its cited-token excuse and
        no exemption is granted. Killed by f3/f4/f5/f6; f5 is the shape that isolates it from NA7, because
        both tokens of the erratum line are row anchor tokens there.

No fixture is a re-spelling of the freeze direction module: each one uses a different registry shape
(single row with an explicit lane path, two rows bound by a provenance table, a stale token that is a
sibling's committed capture, a multi-capture row whose second capture is only a manifest entry, a row that
carries two anchor tokens, a provenance-bound row over three commits).
"""
import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")
LESSON = "corpus/lessons/round-43-a-err.md"


def digest(body):
    return hashlib.sha256(body).hexdigest()


def row(sid, source, anchor):
    return (f"| {sid} | {source} | capture | A | fixture-scalar | {anchor} | erratum exemption row | mined "
            f"| 2026-10-26 | 180d | - |\n")


def settle(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


def f1_repaired_row_historical_erratum(ctx, d):
    """One repaired row: its erratum is history, so only NA7's dropped allowed-guard turns the lane red."""
    r = ctx.init(d / "repo")
    hist = b"the capture this row named before it was repaired\n"
    live = b"the capture the repaired row names now\n"
    ctx.write(r / "corpus/evidence/round43/a-err1/hist.txt", hist)
    ctx.write(r / "corpus/evidence/round43/a-err1/live.txt", live)
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S431", "captured at corpus/evidence/round43/a-err1/live.txt",
                           f"sha256 {digest(live)}"))
    ctx.write(r / LESSON,
              f"Erratum (round 37): S431 anchor sha256 {digest(hist)} was the stale token; the capture "
              f"this row names now carries sha256 {digest(live)}.\n")
    settle(ctx, r, "one repaired row and its historical erratum")
    return ["--lane", str(r)]


def f2_two_rows_provenance_two_errata(ctx, d):
    """Two repaired rows bound by a provenance table, two historical errata over three commits."""
    r = ctx.init(d / "repo")
    hist_a, live_a = b"old capture of the first row\n", b"current capture of the first row\n"
    hist_b, live_b = b"old capture of the second row\n", b"current capture of the second row\n"
    ev = r / "corpus/evidence/round43/a-err2"
    ctx.write(ev / "hist-a.txt", hist_a)
    ctx.write(ev / "hist-b.txt", hist_b)
    ctx.write(ev / "live-a.txt", live_a)
    ctx.write(ev / "live-b.txt", live_b)
    ctx.write(ev / "PROVENANCE.md",
              "| row | capture |" + "\n|---|---|\n"
              + f"| S441 | `live-a.txt` | sha256 {digest(live_a)} |\n"
              + f"| S442 | `live-b.txt` | sha256 {digest(live_b)} |\n")
    settle(ctx, r, "evidence and its provenance table, before any row exists")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S441", "bound by the provenance table of round43/a-err2", f"sha256 {digest(live_a)}")
              + row("S442", "bound by the provenance table of round43/a-err2", f"sha256 {digest(live_b)}"))
    settle(ctx, r, "two repaired rows, both bound through the provenance table")
    ctx.write(r / LESSON,
              f"Erratum (round 37): S441 anchor sha256 {digest(hist_a)} was the stale token; the capture now "
              f"carries sha256 {digest(live_a)}.\n"
              f"Erratum (round 37): S442 anchor sha256 {digest(hist_b)} was the stale token; the capture now "
              f"carries sha256 {digest(live_b)}.\n")
    settle(ctx, r, "the two historical errata land after the repairs")
    return ["--lane", str(r)]


def f3_stale_token_is_a_sibling_capture(ctx, d):
    """The stale token is a sibling's committed capture: only the exemption keeps the row green."""
    r = ctx.init(d / "repo")
    other = b"another committed capture this lane holds\n"
    mine = b"the capture this row binds\n"
    ctx.write(r / "corpus/evidence/round43/a-err3/other.txt", other)
    ctx.write(r / "corpus/evidence/round43/a-err3/mine.txt", mine)
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S451", "captured at corpus/evidence/round43/a-err3/mine.txt",
                           f"sha256 {digest(other)}"))
    ctx.write(r / LESSON,
              f"Erratum (round 37): S451 anchor sha256 {digest(other)} was the stale token; the capture "
              f"this row binds carries sha256 {digest(mine)}.\n")
    settle(ctx, r, "one row whose stale token is a committed capture of another file")
    return ["--lane", str(r)]


def f4_manifest_only_second_capture(ctx, d):
    """A row naming two captures, the second only a SHA256SUMS entry: the exemption skips the unanchored one."""
    r = ctx.init(d / "repo")
    real = b"the capture with committed bytes\n"
    ghost = b"the capture this lane lists but never commits\n"
    ev = r / "corpus/evidence/round43/a-err4"
    ctx.write(ev / "real.txt", real)
    ctx.write(ev / "SHA256SUMS", f"{digest(ghost)}  ghost.bin\n")
    settle(ctx, r, "one committed capture and one manifest entry only")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S461",
                           "captured at corpus/evidence/round43/a-err4/ghost.bin and "
                           "corpus/evidence/round43/a-err4/real.txt",
                           f"sha256 {digest(b'neither file carries this token')}"))
    settle(ctx, r, "a two-capture row whose anchor token resolves no capture")
    ctx.write(r / LESSON,
              f"Erratum (round 37): S461 anchor sha256 {digest(b'neither file carries this token')} was the "
              f"stale token; the captures carry sha256 {digest(ghost)} and sha256 {digest(real)}.\n")
    settle(ctx, r, "the erratum names both of the row's captures")
    return ["--lane", str(r)]


def f5_row_carrying_both_tokens(ctx, d):
    """The row carries its right token AND a stale one, the erratum cites both: NA7 stays green, NA20/NA21 fall."""
    r = ctx.init(d / "repo")
    other = b"a committed capture the stale token belongs to\n"
    mine = b"the capture this row actually binds\n"
    ctx.write(r / "corpus/evidence/round43/a-err5/other.txt", other)
    ctx.write(r / "corpus/evidence/round43/a-err5/mine.txt", mine)
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S471", "captured at corpus/evidence/round43/a-err5/mine.txt",
                           f"sha256 {digest(mine)} sha256 {digest(other)}"))
    ctx.write(r / LESSON,
              f"Erratum (round 37): S471 anchor sha256 {digest(other)} is the stale token; the capture this "
              f"row binds carries sha256 {digest(mine)}.\n")
    settle(ctx, r, "an anchor cell carrying two tokens, one stale")
    return ["--lane", str(r)]


def f6_provenance_bound_unknown_stale(ctx, d):
    """A provenance-bound row whose stale token no committed file carries, across two commits."""
    r = ctx.init(d / "repo")
    mine = b"the capture the provenance table names\n"
    ev = r / "corpus/evidence/round43/a-err6"
    ctx.write(ev / "probe.txt", mine)
    ctx.write(ev / "PROVENANCE.md",
              "| row | capture | commit |" + "\n|---|---|---|\n"
              + f"| S481 | `probe.txt` | pinned by the provenance table |\n")
    settle(ctx, r, "the capture and the provenance table alone")
    ctx.write(r / "corpus/SOURCES.md",
              HEADER + row("S481", "bound by the provenance table of round43/a-err6",
                           f"sha256 {digest(b'no committed capture carries this token')}"))
    ctx.write(r / LESSON,
              f"Erratum (round 37): S481 anchor sha256 {digest(b'no committed capture carries this token')} "
              f"was the stale token; the capture carries sha256 {digest(mine)}.\n")
    settle(ctx, r, "the row and its erratum land after the capture")
    return ["--lane", str(r)]


FIXTURES = [
    {"fid": "a_err-f1-repaired-row-historical-erratum", "tool": "anchor", "expect": "accept",
     "defects": [], "build": f1_repaired_row_historical_erratum},
    {"fid": "a_err-f2-two-rows-provenance-two-errata", "tool": "anchor", "expect": "accept",
     "defects": [], "build": f2_two_rows_provenance_two_errata},
    {"fid": "a_err-f3-stale-token-sibling-capture", "tool": "anchor", "expect": "accept",
     "defects": [], "build": f3_stale_token_is_a_sibling_capture},
    {"fid": "a_err-f4-manifest-only-second-capture", "tool": "anchor", "expect": "accept",
     "defects": [], "build": f4_manifest_only_second_capture},
    {"fid": "a_err-f5-row-carrying-both-tokens", "tool": "anchor", "expect": "accept",
     "defects": [], "build": f5_row_carrying_both_tokens},
    {"fid": "a_err-f6-provenance-bound-unknown-stale", "tool": "anchor", "expect": "accept",
     "defects": [], "build": f6_provenance_bound_unknown_stale},
]
