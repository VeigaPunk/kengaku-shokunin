# SourceReopen — round 68 attempt 2, wave w2 (S240 live re-open + registry row audit)

Seat: SourceReopen (leaf; no dispatch). Access date **2026-11-03** (attempt 2). All lane reads are
read-only; no lane file was edited. Scratch root `/fast/scratch/hyaku/kengaku-r68/SourceReopen`
(deleted after this report; captures copied here first).

Lane state observed: landing `0e52fb5d` (attempt 1), tip at first read `7803bdd4` (A2 freeze), tip at
last read `27f649f8` (A3 freeze). The S240 row's committed bytes are identical at all three:
`sha256sum` of `corpus/SOURCES.md:255` = `a33d310ff098310c9066ffb6474c810024791acc9303375bee2d5bbd95eb20f4`
(also equal in the worktree before the concurrent edit noted in F1). `grep -cE '^\|[[:space:]]*S240[[:space:]]*\|'
corpus/SOURCES.md` → `1`.

## 1. Captures (HTTP status, bytes, sha256)

| source | URL | HTTP | bytes | lines | sha256 | saved |
|---|---|---|---|---|---|---|
| urllib3 `src/urllib3/connection.py` @ tag `2.7.0` | `https://raw.githubusercontent.com/urllib3/urllib3/2.7.0/src/urllib3/connection.py` | **HTTP/2 200** | **42786** | 1099 | **`668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532`** | `w2/SourceReopen/connection.py` |
| CPython `Lib/http/client.py` @ `v3.14.8` | `https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/http/client.py` | **HTTP/2 200** | **59576** | 1598 | **`016aa7664201a82f0f37ddfb11ed662dd1f07aa23c9470c6a3cb3278aa479230`** | `w2/SourceReopen/client.py` |

Both saved files were `cmp`-verified byte-identical to the fetched bytes; their sha256 re-checked
after copy (table values). The urllib3 capture **exactly matches the row's stated sha256 and 42786
bytes**; the CPython capture **exactly matches the lesson Gate's stated sha256 and 59576 bytes**.

Supporting captures (scratch only, not required here):
- urllib3 `exceptions.py` @ `2.7.0` — HTTP/2 200, 9945 B, sha256
  `8503c7a2aa38cb0e3a7ac3525647225505d5520031580825b21e8c6f242d6be4` (= the sha the lesson Gate
  cites); `:148` is `        super().__init__(f"{conn}: {message}")`.
- urllib3 `connection.py` @ `2.5.0` — HTTP/2 200, 42613 B, sha256
  `88fe2981226da6eb17c9895e8f3367fa08a1ff0582c4c53eab2e8e53591a6a97` (= the S241 receipt's primary
  capture); the file contains **no** `def __str__` / `def __repr__` at all (`grep -c` → 0), so the
  Gate's "adopt 2.7.0 bytes, not the 2.5.0 primary, which has no renderer" holds.
- **pip 26.2.1 wheel** (PyPI JSON HTTP 200; wheel HTTP 200, 1816632 B, sha256
  `71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e` = PyPI digest). Inside:
  `pip/__init__.py` `__version__ = "26.2.1"`; `pip/_vendor/vendor.txt:11` → `urllib3==2.7.0`;
  `pip/_vendor/urllib3/connection.py` sha256 `668b37ab…`, 42786 B, **byte-identical** to the raw
  2.7.0 fetch. The row's "pip 26.2.1's vendored urllib3==2.7.0" is therefore verified against
  the named pip release itself, not only inferred. (Host uv cache holds pip 26.2.2, whose vendored
  bytes are the same sha — an independent second witness.)

## 2. Located anchor (urllib3 2.7.0, `connection.py`)

```
82:  class HTTPConnection(_HTTPConnection):
163:     def __str__(self) -> str:
164:         return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})"
```
Located quote: `return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})"` — **`:164`**
(3 whitespace tokens, ≤25 words), inside `def __str__` (**`:163`**), inside `class HTTPConnection`
(**`:82`**, `_HTTPConnection` is `http.client.HTTPConnection` imported at `:13`). The row's anchor
text is that line verbatim, and its `:163`/`:82`/`exceptions.py:148` claims are all confirmed against
the opened bytes. Chain confirmed: `connection.py:219-221` raises
`NewConnectionError(self, f"Failed to establish a new connection: {e}")`; `exceptions.py:148`
formats `f"{conn}: {message}"`, which invokes `__str__`.

Precision note (not a defect): the same class also defines `__repr__` at `:166` →
`return f"<{self} at {id(self):#x}>"` (`:167`), i.e. repr delegates to `__str__` and wraps it;
`f"{conn}"` takes the `__str__` path, so `:163-164` is the operative renderer and neither path can
produce the contiguous literal `localhost:8080`.

## 3. Registry row audit — `corpus/SOURCES.md:255`

Header contract (`:21`): `id | source | kind | tier | scope | anchor | teaches | status | opened |
recheck | used-by`. Row parses to **11 content columns** (`NF=13` pipe-delimited, empty ends).

| col | value (summary) | verdict |
|---|---|---|
| id | `S240`, unique | ok |
| source | urllib3 `src/urllib3/connection.py` tag `2.7.0`; URL char-exact equal to the fetched URL | ok |
| kind/tier | `code` / `A` | ok |
| scope | "the endpoint rendering pip 26.2.1 embeds in connection-refused stderr … host and port as separate fields" | ok |
| anchor | `:164` verbatim quote + `:163`/`:82`/`exceptions.py:148` + sha256 + 42786 bytes | ok (all re-derived above; sha and size exact) |
| teaches | urllib3 `__str__` renders host/port as separate fields; literal absent; captured text carries `host='localhost'`, `port=8080` | ok (committed K2 capture: `host='localhost'` ×5, `port=8080` ×5, `localhost:8080` ×0, `Errno 111`/`Connection refused` ×5) |
| **status** | **`queued`** at HEAD | **MISMATCH — finding F1** (spec expects `mined`) |
| opened | `2026-11-03` | ok (today's access date) |
| recheck | `180d` | ok (same cadence as S236–S239) |
| used-by | `corpus/knowledge/tb2-network-service-offline-grader.md` | exists (13258 B); cites `S240` and the urllib3 `__str__` mechanism at `:124-135` |

Registry convention measured over all 232 rows: `mined 210`, `queued 9`, `rejected 13`; S240 is the
**only** `queued` row with a non-`—` `used-by`, and no `mined` row has `—`. A row whose `used-by`
knowledge entry already cites it is `mined` by this registry's own convention.

### F1 — status cell `queued` where the row is mined (finding; no edit by this seat)
- Committed bytes: `corpus/SOURCES.md:255` at `0e52fb5d`, `7803bdd4` and `27f649f8` all read
  status `queued` (line sha `a33d310f…`). The seat spec's expected tuple is (`mined`, `2026-11-03`,
  `180d`); opened/recheck match, status does not.
- Concurrent observation (not this seat's edit): during this seat's run the worktree row was changed
  by another process at `2026-11-03 20:31:39` local — field-by-field diff of HEAD vs worktree shows
  **only** column 8 changed: `queued` → `mined` (worktree row sha `1a5c348d…`; all other 10 columns
  byte-identical). This seat made no edit and does not claim it; the finding is against the
  committed bytes the round asks to re-derive.

## 4. Lesson Gate block — `corpus/lessons/round-68.md` §Gate

Both verdicts re-checked against the opened bytes:

- **CPython row REJECTED as specified** (Gate `:16-30`) — confirmed. `client.py` (200, sha above):
  `class HTTPConnection:` at **`:858`**, body through `:1531` (next top-level `class HTTPException`
  at `:1532`); an `awk` scan of `858–1531` for `__repr__|__str__` returns **0**; the file's only
  `def __repr__` is **`:1559` inside `class IncompleteRead` (`:1554`)**. Nuance: `:1566` carries the
  assignment `__str__ = object.__str__`, also inside `IncompleteRead`, outside `HTTPConnection` and
  not a `def` — the Gate's "only `def __repr__`" statement stands. Live interpreter check on
  Python 3.14.8: `repr()`, `str()` and `f"{...}"` of `http.client.HTTPConnection('localhost', 8080)`
  all render `<http.client.HTTPConnection object at 0x…>` (MRO `[HTTPConnection, object]`), so the
  rejected row's claimed anchor/rendering does not exist.
- **urllib3 2.7.0 ADMITTED** (Gate `:31-49`) — confirmed on every cited element: URL/HTTP 200,
  42786 B, sha256, `:82`/`:163`/`:164` quote, `exceptions.py:148` string and its sha, and the K2
  capture counts (`host='localhost'` ×5, `port=8080` ×5, `localhost:8080` ×0; `Errno 111` and
  `Connection refused` ×5). Sample committed text:
  `NewConnectionError("HTTPConnection(host='localhost', port=8080): Failed to establish a new connection: [Errno 111] Connection refused")`.
- Gate's cited captures exist and are byte-exact: `w1/recon/S240-client-py.txt` sha `016aa766…`,
  `w1/recon/S241-urllib3-2.7.0-connection.py` sha `668b37ab…`, `w1/recon/S241-urllib3-connection.py`
  sha `88fe2981…`; receipts `S240-receipt.md`, `S241-receipt.md` and `w1/RenderingTrace.md` exist.
  The S241 receipt's 2.7.0 raise-site lines (`:219-221`) and 2.5.0 lines (`:213-215`) both match the
  fetched bytes.

**Row verdict:** admitted source row is correct in source, anchor, sha, bytes, teaches, opened,
recheck and used-by; **status token is wrong on the committed bytes (F1)**. **Lesson verdict:** both
Gate verdicts hold; no correction needed beyond F1's status.

## 5. Adjacent observation (outside this seat's verdict; no edit)
Amendment A1 item 1 says "every claim-doc mention of S240's attribution reads 'urllib3
`HTTPConnection.__str__`'". The frozen R68-C1 body at `plans/round-68-claims.md:95` still reads "the
rendering is the `repr()` of an `http.client.HTTPConnection` (S240, …)". The frozen body cannot be
edited by design, so the universal "every" is inaccurate as written against the committed bytes;
A1 supersedes the sentence but the claims doc contains both attributions. Low severity, no predicate
effect; an A3 wording fix would close it. I made no edit.

## 6. Remaining unknowns
- None material to the row or Gate. Residual assumptions: raw.githubusercontent tag bytes were
  treated as the release bytes (the sha equality with the pip 26.2.1 wheel's vendored copy is the
  independent cross-check); the concurrent `queued → mined` worktree edit's author is not identified
  here (not this seat), and if it lands, F1 closes against a future commit.
- I re-counted the committed K2 capture but did not re-run the C1 battery (not this seat's item).

## 7. Reproduce
```
curl -sS -w '%{http_version} %{http_code}\n' -o connection.py \
  https://raw.githubusercontent.com/urllib3/urllib3/2.7.0/src/urllib3/connection.py
sha256sum connection.py   # 668b37ab…  42786 bytes
curl -sS -w '%{http_version} %{http_code}\n' -o client.py \
  https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/http/client.py
sha256sum client.py       # 016aa766…  59576 bytes
grep -n 'class HTTPConnection\|def __str__\|def __repr__' connection.py   # 82 / 163 / 166
awk 'NR>=858 && NR<=1531 && /__repr__|__str__/' client.py                 # no output
grep -n 'def __repr__' client.py                                          # only 1559
```
Tooling: nothing installed this round. Scratch `/fast/scratch/hyaku/kengaku-r68/SourceReopen` deleted
after copying `connection.py` and `client.py` into `w2/SourceReopen/`.
