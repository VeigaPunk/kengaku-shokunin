# S241 Receipt — urllib3 src/urllib3/connection.py (Candidate Row)

## Primary Capture (urllib3 2.5.0 as specified in seat prompt)

- URL: https://raw.githubusercontent.com/urllib3/urllib3/2.5.0/src/urllib3/connection.py
- HTTP status: 200
- Access date: 2026-11-03 UTC
- SHA256: 88fe2981226da6eb17c9895e8f3367fa08a1ff0582c4c53eab2e8e53591a6a97
- Byte count: 42613
- Line count: 1093
- Local file: W/recon/S241-urllib3-connection.py

### Located quote at NewConnectionError raise site:
- Lines 213-215:
  `raise NewConnectionError(self, f"Failed to establish a new connection: {e}") from e`
  (12 words).

### Findings on urllib3 2.5.0:
- `class HTTPConnection(_HTTPConnection)` begins at line 82 (subclassing `http.client.HTTPConnection`).
- In version 2.5.0, `HTTPConnection` does NOT define `__str__` or `__repr__`.

---

## Secondary Capture (urllib3 2.7.0, vendored by pip 26.2.1)

- URL: https://raw.githubusercontent.com/urllib3/urllib3/2.7.0/src/urllib3/connection.py
- HTTP status: 200
- Access date: 2026-11-03 UTC
- SHA256: 668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532
- Byte count: 42786
- Line count: 1099
- Local file: W/recon/S241-urllib3-2.7.0-connection.py

### Located quotes in urllib3 2.7.0:
1. `HTTPConnection.__str__` renderer:
   - Lines 163-164:
     `def __str__(self) -> str:`
     `    return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})"`
     Located quote (line 164, 5 words):
     `return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})"`

2. NewConnectionError raise site:
   - Lines 219-221:
     `raise NewConnectionError(self, f"Failed to establish a new connection: {e}") from e`
     (12 words).

### Causal chain to pip 26.2.1 stderr:
`pip 26.2.1` vendors `urllib3 2.7.0` (`pip/_vendor/vendor.txt:11`). When pip attempts to connect to `http://localhost:8080/simple`, the OS connection fails with `ECONNREFUSED` (`[Errno 111] Connection refused`). `_new_conn()` catches `OSError` and executes `raise NewConnectionError(self, f"Failed to establish a new connection: {e}") from e`. `NewConnectionError.__init__` in `urllib3/exceptions.py` evaluates `super().__init__(f"{conn}: {message}")`, which formats `self` via `HTTPConnection.__str__`. This produces the exact string `HTTPConnection(host='localhost', port=8080): Failed to establish a new connection: [Errno 111] Connection refused`.

S241 opened=True sha=88fe2981226da6eb17c9895e8f3367fa08a1ff0582c4c53eab2e8e53591a6a97
