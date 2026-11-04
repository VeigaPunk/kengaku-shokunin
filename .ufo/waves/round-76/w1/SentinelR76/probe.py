import argparse, contextlib, http.server, io, os, pathlib, subprocess, sys, threading, types
from unittest.mock import patch
W = pathlib.Path(__file__).resolve().parent
S = pathlib.Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')) / 'kengaku-r76/SentinelR76'
S.mkdir(parents=True, exist_ok=True)
def load(name):
    m = types.ModuleType(name)
    m.__file__ = str(W / (name + '.py'))
    exec(compile((W / (name + '.py')).read_text(), m.__file__, 'exec'), m.__dict__)
    return m
c1 = load('round76_c1_surface_resolver')
c2 = load('round76_c2_defect_discharge')
F = S / 'lane'; F.mkdir(exist_ok=True)
(S / 'outside.md').write_text('inert marker\n')
class Reader:
    def __init__(self, token): self.token = token
    def get(self, rel):
        return '## Surfaces\n| Surface | Path | What |\n|---|---|---|\n| crafted | `' + self.token + '` | fixture |\n'
for token in ['../outside.md', str(S / 'outside.md'), 'file:///nonexistent/sentinel', '~/../../nonexistent-sentinel']:
    try:
        defects, report = c1.census(F, Reader(token))
        print('ROW', repr(token), '=>', report, defects)
    except Exception as e: print('ROW-EXCEPTION', type(e).__name__, str(e))
# A non-local destination is intercepted before any socket is opened.
seen = []
class Response:
    status = 200
    def __enter__(self): return self
    def __exit__(self, *args): pass
def fake_open(url, **kwargs): seen.append(url); return Response()
with patch.object(c1.urllib.request, 'urlopen', fake_open):
    print('NONLOCAL-ROW', c1.census(F, Reader('http://192.0.2.1/sentinel')))
print('NONLOCAL-REQUEST-INTERCEPTED', seen)
# Only a loopback server is contacted; it redirects to another hostname, also loopback.
hits = []
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        hits.append((self.headers['Host'], self.path))
        if self.path == '/redirect':
            self.send_response(302); self.send_header('Location', 'http://localhost:%d/final' % self.server.server_port); self.end_headers()
        else: self.send_response(204); self.end_headers()
    def log_message(self, *args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
try:
    print('REDIRECT-ROW', c1.census(F, Reader('http://127.0.0.1:%d/redirect' % server.server_port)))
finally:
    server.shutdown(); server.server_close(); thread.join()
print('REDIRECT-HITS', hits)
# Hostname encoding is checked before connection; no traffic from this malformed host.
try: print('LONG-HOST', c1.http_status('http://' + 'a' * 300 + '.invalid/'))
except Exception as e: print('LONG-HOST-EXCEPTION', type(e).__name__, str(e))
for token in ['~/{a,{b,c}}/x', '~/' + '{a,b}' * 12]:
    targets = c1.expand_braces(token)
    print('BRACES', repr(token), 'targets=', len(targets), 'first=', targets[0], 'last=', targets[-1])
# Single alternatives make recursion grow without generating an explosive allocation.
try: c1.expand_braces('~/' + '{a}' * (sys.getrecursionlimit() + 10))
except Exception as e: print('BRACE-DEPTH-EXCEPTION', type(e).__name__)
# Receipt targets stay within our scratch, but outside the supplied fixture lane.
(F / 'PROVINCE.md').write_text(Reader('../outside.md').get('PROVINCE.md'))
out = S / 'c1-overwrite.txt'; out.write_text('DO NOT KEEP\n')
print('C1-RECEIPT-RC', c1.emit(F, 'worktree', out)); print('C1-OUTSIDE-LANE-OVERWRITTEN', out.read_text().startswith('LANE_TIP '))
out2 = S / 'c2-overwrite.txt'; out2.write_text('DO NOT KEEP\n')
with patch.object(c2, 'git', return_value=subprocess.CompletedProcess([], 0, 'fixture\n', '')):
    print('C2-BATTERY-RECEIPT-RC', c2.run_battery(argparse.Namespace(receipt=out2, lane=F), F, lambda: 0))
print('C2-OUTSIDE-LANE-OVERWRITTEN', out2.read_text().startswith('LANE_TIP '))
# Record constructed child argv, do not execute mutable lane scripts.
calls = []
def fake_run(argv, **kwargs):
    calls.append((argv, kwargs))
    return subprocess.CompletedProcess(argv, 0, '', '')
with patch.object(c2.subprocess, 'run', fake_run): c2.derive_selftest_counts(F, S / 'work')
for argv, kw in calls: print('C2-CHILD', repr(argv), repr(kw))
print('ROW-COMMAND-ONLY-REGEX', c2.check_trivial("echo 'sentinel'; SCORECARD.md"))
print('PROBE COMPLETE')
