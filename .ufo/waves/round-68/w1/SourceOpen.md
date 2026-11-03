# SourceOpen — S240 live opening, S241 candidate capture, and S228 re-verification

Round: 68 · Wave: w1 · Seat: SourceOpen (UFO-FSD scout) · Date: 2026-11-03 UTC  
Bounds: Read-only in lane repo; artifacts written exclusively to `W/recon/` and `W/SourceOpen.md`; scratch root `/fast/scratch/hyaku/kengaku-r68/SourceOpen` cleaned before exit.

---

## 1. Executive Summary

| Target | Action | HTTP / Cmp | SHA256 | Verdict |
|---|---|---|---|---|
| **S240** (CPython 3.14.8 `http/client.py`) | Fetch live via curl | 200 | `016aa7664201a82f0f37ddfb11ed662dd1f07aa23c9470c6a3cb3278aa479230` | **PASS / OPENED** |
| **S241** (urllib3 2.5.0 `connection.py`) | Fetch live via curl (prompt spec) | 200 | `88fe2981226da6eb17c9895e8f3367fa08a1ff0582c4c53eab2e8e53591a6a97` | **PASS / OPENED** |
| **S241b** (urllib3 2.7.0 `connection.py`) | Fetch live via curl (pip 26.2.1 vendor) | 200 | `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532` | **PASS / GROUNDED** |
| **S228** (`test_outputs.py` at pin 2fd12b88) | Re-verify vs round-63 capture | `cmp` clean (0 delta) | `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` | **PASS / MATCH** |

---

## 2. S240 Live Opening: CPython `Lib/http/client.py` at tag `v3.14.8`

- **URL:** `https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/http/client.py`
- **HTTP status:** 200 (captured in-runner)
- **SHA256:** `016aa7664201a82f0f37ddfb11ed662dd1f07aa23c9470c6a3cb3278aa479230`
- **Size:** 59,576 bytes · 1,598 lines
- **Committed wave path:** `W/recon/S240-client-py.txt`
- **Receipt:** `W/recon/S240-receipt.md`

### Findings on `HTTPConnection` Representation and Host/Port Parsing
1. **Class Header:** Line 858 defines `class HTTPConnection:`.
2. **Field Separation:** Line 921 in `HTTPConnection.__init__`:
   - Located quote (line 921, 7 words):
     `"(self.host, self.port) = self._get_hostport(host, port)"`
   - Host and port are parsed via `_get_hostport` (lines 965–983) and stored as distinct attributes `self.host` and `self.port`.
3. **Absence of `HTTPConnection.__repr__`:**
   - `HTTPConnection` defines **no** `__repr__` and **no** `__str__` in `Lib/http/client.py`. It inherits standard `object.__repr__`, which renders as `<http.client.HTTPConnection object at 0x...>`.
   - The sole `__repr__` method in `Lib/http/client.py` belongs to `class IncompleteRead(HTTPException)`:
     Line 1559: `def __repr__(self):`
     Line 1564 located quote (10 words):
     `"return '%s(%i bytes read%s)' % (self.__class__.__name__, len(self.partial), e)"`
4. **Scout Distinction (Mechanism vs Claim Hypothesis):**
   - The claims document (`plans/round-68-claims.md` line 94–96) posited:
     *"the rendering is the `repr()` of an `http.client.HTTPConnection` (S240, opened live this round — `HTTPConnection.__repr__` renders host and port as separate fields, so the literal `localhost:8080` is not a form this renderer can produce)."*
   - As observed directly from the fetched bytes: `Lib/http/client.py` **does** enforce host and port separation via `(self.host, self.port) = self._get_hostport(host, port)`, but does **not** define an `HTTPConnection.__repr__`.
   - The concrete string `HTTPConnection(host='localhost', port=8080)` emitted in pip 26.2.1 stderr actually originates in urllib3 (`HTTPConnection.__str__`, see S241 below).

---

## 3. S241 Candidate Row: urllib3 `src/urllib3/connection.py`

### Primary Capture: urllib3 2.5.0 (per seat specification)
- **URL:** `https://raw.githubusercontent.com/urllib3/urllib3/2.5.0/src/urllib3/connection.py`
- **HTTP status:** 200
- **SHA256:** `88fe2981226da6eb17c9895e8f3367fa08a1ff0582c4c53eab2e8e53591a6a97`
- **Size:** 42,613 bytes · 1,093 lines
- **Committed wave path:** `W/recon/S241-urllib3-connection.py`
- **NewConnectionError Raise Site:**
  - Lines 213–215 located quote (12 words):
    `"raise NewConnectionError(self, f\"Failed to establish a new connection: {e}\") from e"`
  - Note: In tag 2.5.0, `HTTPConnection` (line 82) does not define `__str__` or `__repr__`.

### Secondary Capture: urllib3 2.7.0 (pip 26.2.1 vendored version)
- **URL:** `https://raw.githubusercontent.com/urllib3/urllib3/2.7.0/src/urllib3/connection.py`
- **HTTP status:** 200
- **SHA256:** `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532`
- **Size:** 42,786 bytes · 1,099 lines
- **Committed wave path:** `W/recon/S241-urllib3-2.7.0-connection.py`
- **Receipt:** `W/recon/S241-receipt.md`
- **Renderer Quote:**
  - Line 164 located quote (5 words):
    `"return f\"{type(self).__name__}(host={self.host!r}, port={self.port!r})\""`
- **NewConnectionError Raise Site:**
  - Lines 219–221 located quote (12 words):
    `"raise NewConnectionError(self, f\"Failed to establish a new connection: {e}\") from e"`

### Full Mechanism Trace of pip 26.2.1 K2 Stderr
1. Host pip 26.2.1 vendors urllib3 2.7.0 (`pip/_vendor/vendor.txt:11`).
2. When attempting to connect to `http://localhost:8080/simple`, the connection fails with `ECONNREFUSED` (`[Errno 111] Connection refused`).
3. `urllib3.connection.HTTPConnection._new_conn()` catches `OSError` and raises `NewConnectionError(self, f"Failed to establish a new connection: {e}")`.
4. `NewConnectionError.__init__` in `urllib3.exceptions` runs `super().__init__(f"{conn}: {message}")`.
5. The f-string calls `str(conn)`, which invokes `HTTPConnection.__str__` (line 164), returning `HTTPConnection(host='localhost', port=8080)`.
6. Result: Neither layer ever concatenates `host:port` into `localhost:8080`.

---

## 4. S228 Re-verification: Terminal-Bench 2.0 `pypi-server/tests/test_outputs.py`

- **Committed capture path:** `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py`
- **Round-63 capture path:** `.ufo/waves/round-63/w1/recon/S228-pypi-test_outputs.py`
- **Byte comparison:**
  `cmp corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py .ufo/waves/round-63/w1/recon/S228-pypi-test_outputs.py`
  Exit status: `0` (byte-identical, 0 differences across all 3,177 bytes).
- **Re-hashed SHA256:**
  `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c`
  Matches frozen pin value, `corpus/evidence/round52/graders/SHA256SUMS:134`, and round-63 receipt of record.
- **Commit pin:** `2fd12b88aafdd04a52c298e3940bcb189f9766d6`.

---

## 5. Artifacts and Receipts in `W/recon/`

- `W/recon/S240-client-py.txt` (59,576 bytes, sha256 `016aa7664201a82f0f37ddfb11ed662dd1f07aa23c9470c6a3cb3278aa479230`)
- `W/recon/S240-receipt.md` (`S240 opened=True sha=016aa7664201a82f0f37ddfb11ed662dd1f07aa23c9470c6a3cb3278aa479230`)
- `W/recon/S241-urllib3-connection.py` (42,613 bytes, sha256 `88fe2981226da6eb17c9895e8f3367fa08a1ff0582c4c53eab2e8e53591a6a97`)
- `W/recon/S241-urllib3-2.7.0-connection.py` (42,786 bytes, sha256 `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532`)
- `W/recon/S241-receipt.md` (`S241 opened=True sha=88fe2981226da6eb17c9895e8f3367fa08a1ff0582c4c53eab2e8e53591a6a97`)

---

## 6. Recommendations for L1 Integration

1. **S240 Row in `corpus/SOURCES.md`:**  
   Ground S240 in `Lib/http/client.py` at line 921: `(self.host, self.port) = self._get_hostport(host, port)`. Clarify that `HTTPConnection` splits and stores `host` and `port` separately, while defining no custom `__repr__` (inherits `object.__repr__`).
2. **S241 Candidate Row in `corpus/SOURCES.md`:**  
   Adopt S241 as `urllib3 2.7.0` (or pair 2.5.0 with 2.7.0). urllib3 2.7.0 provides the literal renderer `HTTPConnection.__str__` (line 164) that formats `NewConnectionError` in `pip 26.2.1`.
3. **Claims Doc Reporting:**  
   Report the honest finding that `HTTPConnection.__repr__` does not exist in `http.client` at Python 3.14.8; the host/port separation is established by `http.client:921`, while the string representation `HTTPConnection(host='localhost', port=8080)` is produced by urllib3's `__str__`.
