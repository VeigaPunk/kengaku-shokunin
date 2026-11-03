# S240 source-open receipt — round 68, wave 1 (seat SourcesRows)

Opened 2026-11-03 by `curl` (HTTP/2, no proxy) from the fleet host
(linux 7.2.11-arch1-1). Scratch root `/fast/scratch/hyaku/kengaku-r68/SourcesRows`
(deleted before yield); byte copies kept under
`.ufo/waves/round-68/w1/SourcesRows/sources/` (sha256 re-checked after copy).

## A. CPython `Lib/http/client.py` at tag `v3.14.8` — the frozen claim's named source

| field | value |
|---|---|
| URL | https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/http/client.py |
| HTTP | 200 (HTTP/2); `content-type: text/plain; charset=utf-8` |
| etag | `"cad3bbcbad09f350e25e28803fb2bc0b59276e1ffcb0f2d962d2ca4ea3cce6d9"` |
| bytes | 59576 |
| sha256 | `016aa7664201a82f0f37ddfb11ed662dd1f07aa23c9470c6a3cb3278aa479230` |
| capture | `SourcesRows/sources/client-py-v3.14.8.txt` |
| scout | `.ufo/waves/round-68/w1/recon/S240-client-py.txt` — same size, same sha256 (independent open by seat SourceOpen) |

Sweep (commands and outputs, all on the capture):

```
grep -n 'class HTTPConnection' client.py                         -> 858:class HTTPConnection:
grep -n 'def __repr__' client.py                                 -> 1559:    def __repr__(self):
awk 'NR>=858 && NR<=1531 && /__repr__/ {c++} END{print c+0}'     -> 0
class map: :1501 else:  :1502 class HTTPSConnection(HTTPConnection):  :1532 class HTTPException(Exception):
class at :1554 is IncompleteRead; its __repr__ at :1559 is the file's only one
```

**Finding.** `class HTTPConnection` (`:858`) defines no `__repr__` and no `__str__`; it inherits
`object.__repr__`, which renders `<http.client.HTTPConnection object at 0x...>`. The anchor the
frozen claims doc names ("the `HTTPConnection.__repr__` line number at tag v3.14.8") **does not
exist**. The claims doc's mechanism sentence — "the rendering is the `repr()` of an
`http.client.HTTPConnection`" — is contradicted by these bytes. The literal `localhost:8080`
remains unproducible in the captured stderr, but not for the stated reason and not by this class.

Located quote (rejection evidence; the file's only `__repr__`, outside `HTTPConnection`):

```
QUOTE S240-REJECT | SourcesRows/sources/client-py-v3.14.8.txt:1559 | def __repr__(self):
```

Context: `:1554 class IncompleteRead(HTTPException):`; the quote is 4 whitespace-token words.
`grep -c -F 'def __repr__(self):'` on the capture → 1 (line 1559).

## B. urllib3 `src/urllib3/connection.py` at tag `2.7.0` — the true renderer

| field | value |
|---|---|
| URL | https://raw.githubusercontent.com/urllib3/urllib3/2.7.0/src/urllib3/connection.py |
| HTTP | 200 (HTTP/2) |
| etag | `"f6cdbfa65c53118a296a476e84958326221522fe3317cc52206d4f7f9415f5f0"` |
| bytes | 42786 |
| sha256 | `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532` |
| vendor | byte-identical to `pip/_vendor/urllib3/connection.py` in the round's scored venv (`pip 26.2.1`; `pip/_vendor/vendor.txt:11` → `urllib3==2.7.0`), same sha256 |
| capture | `SourcesRows/sources/urllib3-2.7.0-connection.py` |
| scout | `.ufo/waves/round-68/w1/recon/S241-urllib3-2.7.0-connection.py` — same size, same sha256 |

Lines:

```
:82   class HTTPConnection(_HTTPConnection):
:163  def __str__(self) -> str:
:164      return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})"
:166  def __repr__(self) -> str:
:167      return f"<{self} at {id(self):#x}>"
```

Companion file opened the same way:

| field | value |
|---|---|
| URL | https://raw.githubusercontent.com/urllib3/urllib3/2.7.0/src/urllib3/exceptions.py |
| HTTP | 200 |
| bytes | 9945 |
| sha256 | `8503c7a2aa38cb0e3a7ac3525647225505d5520031580825b21e8c6f242d6be4` |
| capture | `SourcesRows/sources/urllib3-2.7.0-exceptions.py` |

```
:142  class NewConnectionError(ConnectTimeoutError, HTTPError):
:145      def __init__(self, conn: HTTPConnection, message: str) -> None:
:148          super().__init__(f"{conn}: {message}")
```

`{conn}` formats through `HTTPConnection.__str__`; pip's warning line is this f-string plus
urllib3's message, wrapped by `NewConnectionError(...)`.

Located quote (admission evidence; 3 whitespace-token words):

```
QUOTE S240 | SourcesRows/sources/urllib3-2.7.0-connection.py:164 | return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})"
```

## C. The captured stderr the frozen clause reads

`corpus/evidence/round68/pypi/stderr/K2.txt` — 7 lines, sha256
`dedbc20d70cc292e39eec807222312473313ee274e3a8db8476e3e0d8565375d`:

```
grep -c "host='localhost'" -> 5
grep -c "port=8080"        -> 5
grep -c "localhost:8080"   -> 0
grep -c "Errno 111"        -> 5
```

Line 1 verbatim (read-only; same text as the round-63 capture):

```
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError("HTTPConnection(host='localhost', port=8080): Failed to establish a new connection: [Errno 111] Connection refused")': /simple/vectorops/
```

## D. Scout-capture discrepancy (reported to SourceOpen, 2026-11-03)

`recon/S241-urllib3-connection.py` — 42613 bytes, sha256
`88fe2981226da6eb17c9895e8f3367fa08a1ff0582c4c53eab2e8e53591a6a97` — is urllib3 2.5.0 (per the
scout's own reply): no `__str__`/`__repr__` on `HTTPConnection` and no
`host={self.host!r}` text, so it cannot ground the rendering. The 2.7.0 capture appeared at
`recon/S241-urllib3-2.7.0-connection.py` at 20:04 with the sha in §B. The scout's markdown
receipts (`recon/S240-receipt.md`, S241 receipts) were still absent at this receipt's write time;
the captures above carry the bytes.

## E. Consequence for the frozen claim (this seat edits no rule)

- R68-C1's frozen predicate reads only the captured stderr; it is **unaffected** by the
  misattribution.
- R68-C1's "Sourced:" sentence and the S240 row spec are **not supported** by the named CPython
  bytes. A dated amendment section (never an edit) is the L1's call.
- The counting anchor `grep -cE '^\|[[:space:]]*S240[[:space:]]*\|' corpus/SOURCES.md` → 1 is
  satisfiable by one S240 row. `SourcesRows.md` drafts option A (S240 = urllib3 2.7.0, paste-ready)
  and option B (S240 = CPython rejected row + urllib3 at a new id), with the trade-off stated.
