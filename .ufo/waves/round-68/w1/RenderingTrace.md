# RenderingTrace — R68 w1: the pip stderr rendering chain behind the corrected K2 clause

Seat: RenderingTrace (read-only revenger mechanics seat). Date: 2026-11-03. No rule, claim, plan or
instrument was edited. Verdict: **chain grounded; the literal `localhost:8080` is not a form this
renderer can emit to stderr** — the frozen K2 clause is the right clause, but the frozen narrative's
S240 *attribution* (CPython `http/client.py` `HTTPConnection.__repr__`) is wrong and must be re-sourced
to urllib3 (details §5; the scout's own S240/S241 receipts already split it this way).

## 0. Inputs and runtime (measured, not assumed)

| item | value |
|---|---|
| round-68 K2 capture | `corpus/evidence/round68/pypi/stderr/K2.txt`, 7 lines, sha256 `dedbc20d70cc292e39eec807222312473313ee274e3a8db8476e3e0d8565375d` |
| round-63 K2 capture | `corpus/evidence/round63/k2-pip-stderr.txt`, 7 lines, sha256 `dedbc20d…375d` (byte-identical to the above; `cmp` rc 0) |
| interpreter | CPython 3.14.8 (`/usr/bin/python3`), stdlib source `/usr/lib/python3.14/http/client.py` |
| pip under test | 26.2.1 (venv built with `python3 -m venv`, bundled ensurepip) |
| urllib3 in pip | 2.7.0 vendored: `pip/_vendor/vendor.txt:11` → `urllib3==2.7.0` |
| probe invocation | `python -m pip install --index-url http://localhost:8080/simple vectorops==0.1.0`, stderr only, no verbosity flag (`plans/round63_c1_pypi_probe.py:382-387`) |
| port discipline | 8080 never bound and never contacted by this seat; live runs used 127.0.0.1:18099 (`ss -ltn` count 0 before the run) |

Determinism note: the two captures are byte-identical because the message carries no timestamp and the
run is fully determined (same pip build, same flags, same closed port). The fresh-run provenance is the
battery's own server log / witness (not this seat); nothing here infers beyond the bytes.

## 1. Occurrence counts in both captures (`grep -o | wc -l`; `grep -c` line counts agree)

| token | round-63 capture | round-68 capture |
|---|---|---|
| `host='localhost'` | 5 | 5 |
| `port=8080` | 5 | 5 |
| `localhost:8080` (the literal) | **0** | **0** |
| `Errno 111` | 5 | 5 |
| `Connection refused` | 5 | 5 |
| `NewConnectionError(` | 5 | 5 |

All five warnings have the same shape; line 1 (272 bytes), verbatim:

```
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError("HTTPConnection(host='localhost', port=8080): Failed to establish a new connection: [Errno 111] Connection refused")': /simple/vectorops/
```

Five warnings = five retries after the first attempt (`Retry(total=4..0)`), six connection attempts total
(counted live: six `Starting new HTTP connection` lines at `-vvv`).

## 2. The chain (socket refusal → stderr bytes), with located quotes (≤25 words)

Paths are inside the round-63 probe's venv; they are the bytes that ran. The vendored
`pip/_vendor/urllib3/connection.py` sha256 `668b37ab12835bdf8643a695a9f050551339b280742231f163fc575a925a1532`
equals the upstream urllib3 2.7.0 capture in `W/recon/S241-urllib3-2.7.0-connection.py`.

| # | layer | file:line | located quote |
|---|---|---|---|
| 1 | transport refusal becomes a urllib3 exception | `pip/_vendor/urllib3/connection.py:218-221` | `raise NewConnectionError(self, f"Failed to establish a new connection: {e}") from e` |
| 2 | the exception message embeds `str(conn)` | `pip/_vendor/urllib3/exceptions.py:145-148` | `super().__init__(f"{conn}: {message}")` |
| 3 | **renderer of `HTTPConnection(host='localhost', port=8080)`** | `pip/_vendor/urllib3/connection.py:163-164` | `return f"{type(self).__name__}(host={self.host!r}, port={self.port!r})"` |
| 4 | urllib3 `__repr__` is a wrapper over `__str__` (why either view has separate fields) | `pip/_vendor/urllib3/connection.py:166-167` | `return f"<{self} at {id(self):#x}>"` |
| 5 | the pool binds the raised error for the warning | `pip/_vendor/urllib3/connectionpool.py:848` | `err = e` |
| 6 | **the retry warning that prints it** | `pip/_vendor/urllib3/connectionpool.py:869-871` | `log.warning("Retrying (%r) after connection broken by '%r': %s", retries, err, url)` |
| 7 | `%r` of the `Retry` argument | `pip/_vendor/urllib3/util/retry.py:549-553` | `f"{type(self).__name__}(total={self.total}, connect={self.connect}, read={self.read}, redirect={self.redirect}, status={self.status})"` |
| 8 | the `%s` url is a relative target, never a host | `pip/_vendor/requests/adapters.py:592,696` | `url = request.path_url` … `resp = conn.urlopen(` |
| 9 | pip routes WARNING+ to stderr | `pip/_internal/utils/logging.py:371-377` | `"console_errors": {"level": "WARNING", "class": handler_classes["stream"], "console": _stderr_console,` |
| 10 | pip renders the `WARNING: ` prefix | `pip/_internal/utils/logging.py:139-142` | `if levelno < logging.ERROR:` / `return "WARNING: "` |
| 11 | pip routes <WARNING to stdout (`exclude_warnings`) | `pip/_internal/utils/logging.py:364-369` | `"console": {` … `"console": _stdout_console, "filters": ["exclude_subprocess", "exclude_warnings"],` |
| 12 | vendored debug logger level at default verbosity | `pip/_internal/utils/logging.py:312` | `vendored_log_level = "WARNING" if level in ["INFO", "ERROR"] else "DEBUG"` |

Named answers to the three asked sites:
- **(a) the renderer** — urllib3's `HTTPConnection.__str__` at `pip/_vendor/urllib3/connection.py:163-164`:
  `f"{type(self).__name__}(host={self.host!r}, port={self.port!r})"`. CPython's
  `http/client.py` contributes only the base class; it defines **no** `__repr__` (see §5).
- **(b) the urllib3 exception** — `NewConnectionError.__init__` at `pip/_vendor/urllib3/exceptions.py:145-148`
  builds `f"{conn}: {message}"`, i.e. `str(conn)` + the refusal text; the raise is at
  `connection.py:218-221`.
- **(c) the printing warning** — urllib3's `HTTPConnectionPool.urlopen` at
  `connectionpool.py:869-871` emits `log.warning("Retrying (%r) after connection broken by '%r': %s", …)`
  (pip has no retry warning of its own); pip is the layer that renders it to **stderr** with the
  `WARNING: ` prefix via the `console_errors` handler (`logging.py:371-377`, `139-142`).

Why the nesting looks as it does: `'%r'` on the exception uses `Exception.__repr__`, whose `args[0]` is
the already-rendered `str(conn) + ": " + message`; the outer single quotes are the format string's, and
the double quotes are `repr`'s choice because the message contains single quotes. So the innermost
`host='localhost', port=8080` comes from `str(conn)`, **not** from `repr(conn)`.

## 3. Live reproduction (port 18099; 8080 untouched)

Venv: `/fast/scratch/hyaku/kengaku-r68/RenderingTrace/venv` — Python 3.14.8, pip 26.2.1, vendored
urllib3 2.7.0. Commands and receipts: `W/RenderingTrace-live.txt`, `W/RenderingTrace-render-check.txt`.

1. **Default verbosity**, `--index-url http://localhost:18099/simple vectorops==0.1.0`: stderr is the
   same 7-line shape; after `sed 's/18099/8080/g'` it is **byte-identical** to the committed K2 capture
   (`cmp` rc 0; `live_normalized_lines_equal_capture=True`). Counts on the normalized copy: 5 / 5 / 0.
2. **In-memory 8080 render** (no socket, no listener): `HTTPConnection("localhost", 8080)` →
   `HTTPConnection(host='localhost', port=8080)`; `NewConnectionError(conn, "Failed to establish a new
   connection: [Errno 111] Connection refused")` → `repr` = exactly the inner text of the captured line.
   `str(err)` and `repr(err)` are both substrings of capture line 1 (`VERDICT pass`).
3. **`-vvv`** (max CLI verbosity): stderr still carries exactly 5 `WARNING` + 2 `ERROR` lines and **0**
   occurrences of the literal; stdout carries 13 (index echo, link/`fetch` lines, six
   `Starting new HTTP connection (n): localhost:18099`, the fetch-error and skip lines).

## 4. Falsifiable conclusion

**Question:** given this chain, can ANY stderr produced by this pip+CPython pairing contain the literal
`localhost:8080` in the connection-refused path?

**Answer: No — not at any pip CLI verbosity (default through `-vvv`), because the only stderr-visible
renderer composes the endpoint as two keyword fields.**

- The single stderr record in this path is the retry warning (row 6). Its three arguments are:
  `repr(Retry)` (no endpoint, row 7), `repr(err)` (endpoint as `host=…, port=…`, rows 2–4), and the
  request target `%s` (a relative path, `/simple/vectorops/`; row 8). None joins host and port with `:`.
- Layers that **can** produce the literal `host:port` (named, with stream):
  1. urllib3's debug connection line, `pip/_vendor/urllib3/connectionpool.py:241-245`
     (`"Starting new HTTP connection (%d): %s:%s", …, self.host, self.port or "80"`) → this renders
     `localhost:8080`. It is `DEBUG`, reaches only the stdout `console` handler, and is additionally
     suppressed at default verbosity by `vendored_log_level="WARNING"` (`logging.py:312`). Verified on
     stdout at `-vvv`, absent from stderr.
  2. pip's index-url echo, `pip/_internal/cli/req_command.py:473-475` + `models/search_scope.py:92-94`
     (`logger.info("Looking in indexes: …")`) → renders `http://localhost:8080/simple`. `INFO` ⇒ stdout.
  3. pip's URL echoes, `index/collector.py:304-305` (`logger.debug("Could not fetch URL %s: …")`) and
     `network/auth.py:381` (`logger.debug("Found index url %s", …)`) → stdout at `-vv`.
  `pip --log FILE` writes the DEBUG stream to that file, not stderr; pip exposes no CLI switch that
  sends DEBUG/INFO records to stderr.
- The only other stderr-visible URL-bearing warning in this neighbourhood,
  `network/session.py:503-510` ("The repository located at %s is not a trusted or secure host…"),
  formats `parsed.hostname` (session.py:450-454) — host without the port — so it too cannot carry the
  literal. It did not fire in the graded runs.
- **Stated caveat:** a third party that reconfigures logging (embedding pip as a library, or attaching a
  DEBUG→stderr handler to the root logger) could surface layer 1. That is not "this pairing" as invoked
  by the probe or by the pip CLI. Within the CLI contract, `literal-possible=False`.

## 5. Divergence from the frozen claim's mechanism attribution (reported, not edited)

The frozen claims doc (`plans/round-68-claims.md`, R68-C1 and F1) says the rendering is "the `repr()` of
an `http.client.HTTPConnection` (S240 … `HTTPConnection.__repr__` renders host and port as separate
fields)". Measured against the actual bytes:

- `https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/http/client.py` sha256
  `016aa7664201a82f0f37ddfb11ed662dd1f07aa23c9470c6a3cb3278aa479230` is byte-equal to the local
  `/usr/lib/python3.14/http/client.py` (`cmp` rc 0).
- `class HTTPConnection:` at line 858 defines **no** `__repr__` and **no** `__str__`;
  `http.client.HTTPConnection.__repr__ is object.__repr__` is `True` in the running interpreter, so its
  repr is `<http.client.HTTPConnection object at 0x…>`. The file's only `__repr__` (line 1559) belongs
  to `IncompleteRead`.
- The observed `HTTPConnection(host='localhost', port=8080)` is urllib3 2.7.0's `__str__`
  (`pip/_vendor/urllib3/connection.py:163-164`), pulled in by `NewConnectionError.__init__`
  (`exceptions.py:148`); urllib3's `repr()` (`connection.py:166-167`) merely wraps that `str`.

Consequence: the **conclusion** the claim rests on survives intact (host and port are held/rendered as
separate fields, so the literal cannot be produced on stderr). Only the **source attribution** is wrong:
the mechanism source is S241 (urllib3 2.7.0, `connection.py:163-164` + `exceptions.py:148`), while S240
(CPython `http/client.py`, `class HTTPConnection` and `(self.host, self.port) = self._get_hostport(…)`)
supports only the base-class/field-separation fact. The scout's `W/recon/S240-receipt.md` and
`W/recon/S241-receipt.md` independently reach the same split; my line numbers and the vendored-file
sha agree with them. The L1 should word the S240/S241 rows and the knowledge entry accordingly; the
frozen K2 clause itself needs no change. Nothing in the predicate depends on the citation text.

## 6. Bounds, installs, scratch

- No installs or upgrades (venv from bundled ensurepip; pip 26.2.1 and its vendored urllib3 2.7.0 came
  with the interpreter). No pacman/uv/npx use.
- No git/jj mutation; no writes in L outside `W/RenderingTrace.md`, `W/RenderingTrace-live.txt`,
  `W/RenderingTrace-render-check.txt`. Port 8080 never bound or contacted.
- Disclosed side effect: the default-verbosity probe run used pip's normal HTTP cache under
  `$HOME/.cache/pip` (pip's default; no repo, config or PATH writes).
- Scratch `/fast/scratch/hyaku/kengaku-r68/RenderingTrace` is deleted before yield.

Confidence: **high** — every layer is cited from the bytes that ran (venv source with hashes), the
live run's normalized stderr is byte-identical to the committed capture, the 8080 render is reproduced
exactly in memory, and the stdout/stderr split is demonstrated at both default and max verbosity.

TRACE grounded=True literal-possible=False
