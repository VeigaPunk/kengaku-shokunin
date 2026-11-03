# S240 Receipt — CPython Lib/http/client.py at v3.14.8

- URL: https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/http/client.py
- HTTP status: 200
- Access date: 2026-11-03 UTC
- SHA256: 016aa7664201a82f0f37ddfb11ed662dd1f07aa23c9470c6a3cb3278aa479230
- Byte count: 59576
- Line count: 1598

## Located quotes and findings

1. `HTTPConnection` class definition and host/port separation:
   - Line 858: `class HTTPConnection:`
   - Line 921 located quote:
     `(self.host, self.port) = self._get_hostport(host, port)`
     (7 words; stores host and port as separate attributes, parsed by `_get_hostport` lines 965-983).

2. Representation methods in `Lib/http/client.py`:
   - `class HTTPConnection` defines NO `__repr__` and NO `__str__` method. It inherits `object.__repr__`, producing `<http.client.HTTPConnection object at 0x...>`.
   - The sole `__repr__` method in `Lib/http/client.py` is on `class IncompleteRead(HTTPException)`:
     Line 1559: `def __repr__(self):`
     Line 1564 located quote:
     `return '%s(%i bytes read%s)' % (self.__class__.__name__, len(self.partial), e)`
     (10 words).

3. Mechanism observation:
   - The literal `localhost:8080` is not produced by `HTTPConnection` because host and port are parsed and held separately (`self.host`, `self.port`).
   - However, the specific string format `HTTPConnection(host='localhost', port=8080)` observed in pip 26.2.1 stderr is NOT produced by `http.client.HTTPConnection`; it is produced by urllib3's `HTTPConnection.__str__` (in `urllib3.connection`, subclassing `http.client.HTTPConnection`) via `NewConnectionError` (see S241 receipt).

S240 opened=True sha=016aa7664201a82f0f37ddfb11ed662dd1f07aa23c9470c6a3cb3278aa479230
