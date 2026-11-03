# Round 68 — kengaku

author: kengaku L1 round 68 attempt 1
date: 2026-11-03
lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
status: skeleton drafted by the SourcesRows scribe seat (wave w1). The L1 owns this file; the
placeholders below are the L1's to fill or remove.

## Gate

**Sources opened this round** (SOURCES contract v1 rule 1: URL, access date, ≤25-word located
quote). Byte captures: `.ufo/waves/round-68/w1/SourcesRows/sources/`; receipt:
`.ufo/waves/round-68/w1/SourcesRows/S240-receipt.md`; scout captures under
`.ufo/waves/round-68/w1/recon/`.

- **S240 — REJECTED as specified (CPython `Lib/http/client.py` at `v3.14.8`).**
  URL https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/http/client.py · accessed
  2026-11-03 (HTTP/2 200; 59576 bytes; sha256
  `016aa7664201a82f0f37ddfb11ed662dd1f07aa23c9470c6a3cb3278aa479230`; the scout capture
  `recon/S240-client-py.txt` is byte-identical).
  Located quote: `def __repr__(self):` — `:1559`, inside `class IncompleteRead` (`:1554`); it is
  the file's only `def __repr__` (`awk 'NR>=858 && NR<=1531 && /__repr__/'` → `0`). Scout receipt
  `recon/S240-receipt.md` (`S240 opened=True sha=016aa766…`) records the same line and concludes
  the format is not produced by `http.client.HTTPConnection`.
  Reason: the frozen row's anchor (`HTTPConnection.__repr__` line) does not exist —
  `class HTTPConnection` (`:858`) defines no `__repr__`/`__str__`, so `object.__repr__` renders
  `<http.client.HTTPConnection object at …>`. This source cannot ground the corrected clause's
  mechanism.
  Flip: a CPython release that adds `HTTPConnection.__repr__` rendering host and port as separate
  fields.
- **S240 — ADMITTED (replacement source: urllib3 `src/urllib3/connection.py` at `2.7.0`).**
  URL https://raw.githubusercontent.com/urllib3/urllib3/2.7.0/src/urllib3/connection.py ·
  accessed 2026-11-03 (HTTP/2 200; 42786 bytes; sha256
  `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532`; byte-identical to pip
  26.2.1's vendored `pip/_vendor/urllib3/connection.py`, `pip/_vendor/vendor.txt:11` →
  `urllib3==2.7.0`; scout capture `recon/S241-urllib3-2.7.0-connection.py` matches; scout receipt
  `recon/S241-receipt.md` gives the same `:164` quote for its secondary 2.7.0 capture — adopt the
  2.7.0 bytes, not the receipt's 2.5.0 primary, which has no renderer).
  Located quote: `return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})"` —
  `:164`, inside `def __str__` (`:163`), `class HTTPConnection` (`:82`). Chain:
  `NewConnectionError.__init__` formats `f"{conn}: {message}"` (`exceptions.py:148`, sha256
  `8503c7a2aa38cb0e3a7ac3525647225505d5520031580825b21e8c6f242d6be4`).
  Gate result: **admit** — host and port are separate fields, so the literal `localhost:8080` is
  not a form this renderer produces. Captured K2 stderr: `host='localhost'` ×5, `port=8080` ×5,
  `localhost:8080` ×0 (`corpus/evidence/round68/pypi/stderr/K2.txt`).
  Note on the CPython receipt's other quote (`:921`, `(self.host, self.port) =
  self._get_hostport(host, port)`): it shows separate *attributes*, not a rendering; relabelling
  the claims sentence as "stores host and port separately" would still not support
  `HTTPConnection.__repr__`.

**Admitted rows this round:** S240 (urllib3 2.7.0; option A in `w1/SourcesRows.md`).
*(placeholder — L1 confirms the id assignment)*
**Rejected rows this round:** the CPython `Lib/http/client.py` row as specified (see above).
*(placeholder — L1 records it; `plans/round-68-claims.md` §R68-C1's mechanism sentence and anchor
need a dated amendment section, never an edit)*
**Assimilation:** none this round (F4; L0 `kengaku | round-54` unresolved). *(placeholder — L1)*

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| reference-drift (wrong-sha citation) | `corpus/lessons/round-67-verifier-spotcheck.md` §5 item 1 — the round-67 report and `corpus/evidence/round67/pipe/a1-mutants.txt` cite `32bacf1d629e7d5809788ef7ea2183fd7b08a11b10c383cc9942e2f58842b836` (the pre-A1 probe at `dcc39ea3`) as the amended counter; the receipt of record binds `03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e` | none — the report quoted the sha from memory instead of re-hashing the committed bytes | the R68-C2 erratum (`plans/round-67-claims.md` `## Erratum (round 68)`): both shas named, golden value `03793f4f…`; gate E1 re-hashes the committed probe and the receipt at check time |
| number-drift (count drift) | `corpus/lessons/round-67-verifier-spotcheck.md` §5 item 2 — report and `LOG.md:2542` say A1 mutants "8 killed, 1 accepted"; the committed `a1-mutants.txt` shows 7 refused (rc 1) + 1 accepted by design = 8 mutants | none — the count was copied from prose, not re-derived from the committed file | the R68-C2 erratum states `7 refused` and `1 accepted by design`; gate E2 requires both substrings in the erratum section |

*(new rows from this wave's seats append below the table in the same four columns.)*

**Candidate row from this wave (not inserted above — L1 decision).** Class `attribution`: the
frozen `plans/round-68-claims.md` §R68-C1 mechanism sentence attributes the stderr rendering to
the `repr()` of an `http.client.HTTPConnection`, and the S240 spec anchors on
`HTTPConnection.__repr__` at `v3.14.8`; the opened bytes show no such method (CPython has none;
the renderer is urllib3 2.7.0 `HTTPConnection.__str__`). Evidence pointer:
`w1/SourcesRows/S240-receipt.md` §A–§B. Captured-by: none — no gate opens a source row's anchor
before the freeze; the row was written from memory of CPython's API. Fix: the lesson Gate rejects
the CPython row and admits urllib3 2.7.0; the claims doc gets a dated amendment section; the S240
row's anchor becomes a checked line of committed bytes. This is the same wrong-source-memory
family as the round-67 §5 item-1 row above, in a different carrier (a mechanism sentence, not a
sha).
