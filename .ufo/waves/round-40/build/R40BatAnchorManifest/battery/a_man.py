"""Battery40 module a_man: the anchor tool's two manifest views of one capture, one fixture per frozen
mutant A21 (the entry is case-folded) and A22 (the entry is an accepted view at all).

Both fixtures sit on the sentence ``plans/anchor_digest_check.py:44-46``: "the digest that entry lists, and
the digest of the committed file bytes, are both accepted views of that one capture". ``capture_digests``
unions the committed blob's digest with the digest ``<dir>/SHA256SUMS*`` lists for the same filename, and
``evidence_index`` lowercases the entry as it is read (``dig = m.group(1).lower()``). One capture therefore
has two accepted digests whenever the manifest and the bytes disagree.

  a_man-uppercase-manifest-entry  A21 rc-mirror. A capture whose SHA256SUMS entry spells its digest in
      UPPERCASE, and a row whose anchor is the lowercase form of that digest. The reference folds the entry
      and the anchor resolves through the manifest view (rc 0, no DEFECT). The mutant keeps the written
      case, so the row's token is neither the blob's digest nor any manifest digest: ``digest-unknown``,
      rc 1.
  a_man-stale-manifest-digest     A22 rc-mirror. A capture whose committed bytes changed while the manifest
      entry still lists the digest the row anchors. The reference accepts the manifest view (rc 0). The
      mutant's ``capture_digests`` answers with the blob view only, so the anchored digest is a committed
      capture belonging to no capture the row names: ``digest-wrong-capture``, rc 1.

Each fixture is its own one-row, one-capture repository (``ctx.init``), so no fixture depends on the lane's
own SOURCES.md, and the manifest digest is always the digest of bytes that are NOT the committed capture's
bytes - that disagreement is what makes the two views distinguishable. Co-located limit, measured in the
seat report: every fixture that kills A21 works by removing the manifest view, which is the view A22
deletes, so the uppercase fixture kills both and ``a_man-stale-manifest-digest`` is the second (narrower)
witness for A22.

stdlib only; no import-time side effects.
"""

import hashlib

CAPTURE = "test_outputs.py"
EVIDENCE = "corpus/evidence/round41/tb2-man"
ROW = ("| S900 | Terminal-Bench 2.0 manifest-view capture \u2014 {path} | code | A | "
       "one capture, two accepted views | sha256 {anchor} | manifest views | mined | 2026-10-26 | 180d | "
       "corpus/knowledge/x.md |")
SUMS = "{digest}  " + CAPTURE + "\n"


def manifest_digest():
    """The digest the manifest entry names: the digest of bytes that are not the capture's own bytes."""
    return hashlib.sha256(b"a_man manifest view, not the committed capture bytes\n").hexdigest()


def _repo(ctx, d, entry, anchor):
    """One committed row whose capture is bound by an explicit lane path and anchored on anchor; the
    manifest entry spells its digest as entry (the same digest, possibly in another case)."""
    path = f"{EVIDENCE}/{CAPTURE}"
    ctx.init(d)
    (d / "corpus/evidence/round41/tb2-man").mkdir(parents=True)
    (d / "corpus/SOURCES.md").write_text(
        "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
        "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n"
        + ROW.format(path=path, anchor=anchor) + "\n")
    (d / path).write_bytes(b"assert True  # a_man capture\n")
    (d / EVIDENCE / "SHA256SUMS").write_text(SUMS.format(digest=entry))
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-q", "-m", "a_man fixture")
    return d


def _uppercase_entry(ctx, d):
    """A21: the SHA256SUMS entry spells the anchored digest in UPPERCASE; the row anchors lowercase."""
    dig = manifest_digest()
    _repo(ctx, d, dig.upper(), dig)
    return ["--lane", str(d), "--evidence-ref", "head"]


def _stale_entry(ctx, d):
    """A22: the manifest still lists the anchored digest; the committed capture bytes are other bytes."""
    dig = manifest_digest()
    _repo(ctx, d, dig, dig)
    return ["--lane", str(d), "--evidence-ref", "head"]


FIXTURES = [
    {"fid": "a_man-stale-manifest-digest", "tool": "anchor", "expect": "accept", "defects": [],
     "build": _stale_entry},
    {"fid": "a_man-uppercase-manifest-entry", "tool": "anchor", "expect": "accept", "defects": [],
     "build": _uppercase_entry},
]
