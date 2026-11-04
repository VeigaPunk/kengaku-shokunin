#!/usr/bin/env python3
"""Finite, read-only C1 endpoint experiment; writes only seat receipts and scratch."""
import hashlib
import http.server
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import threading
import urllib.request

sys.dont_write_bytecode = True
LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
OUT = LANE / '.ufo/waves/round-76/w1/LabratR76'
S = Path(sys.argv[1])
S.mkdir(parents=True, exist_ok=True)
source = LANE / 'plans/round76_c1_surface_resolver.py'
raw = source.read_bytes()
(OUT / 'resolver-tested.py').write_bytes(raw)
spec = importlib.util.spec_from_file_location('resolver_probe', OUT / 'resolver-tested.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
lines = []
def log(text):
    lines.append(text)
    print(text, flush=True)

log('AXES coverage=endpoint-verdict calibration=status-versus-service-identity substrate_changes=0')
log('SOURCE_SHA256 ' + hashlib.sha256(raw).hexdigest())
log('PYTHON ' + sys.version.split()[0])
(S / 'v1').mkdir()
wrong = b'{"object":"list","data":[{"id":"NOT-LFM3-1.7B","owned_by":"NOT-llamacpp"}]}\n'
(S / 'v1/models').write_bytes(wrong)
log('WRONG_IDENTITY_BYTES ' + repr(wrong))
server_cmd = [sys.executable, '-u', '-m', 'http.server', '0', '--bind', '127.0.0.1', '--directory', str(S)]
log('SERVER_COMMAND ' + repr(server_cmd))
with (S / 'server.stderr').open('w') as err:
    server = subprocess.Popen(server_cmd, stdout=subprocess.PIPE, stderr=err, text=True)
    try:
        startup = server.stdout.readline().strip()
        log('SERVER_STARTUP ' + startup)
        port = int(re.search(r'port (\d+)', startup).group(1))
        root = f'http://127.0.0.1:{port}'
        text = ('## Surfaces\n\n| Surface | Path / endpoint | What this lane does with it |\n'
                '|---|---|---|\n'
                f'| Declared model | `{root}/missing-health` | model id `LFM3-1.7B`, `owned_by=llamacpp` |\n'
                f'| Declared model identity | `{root}/v1/models` | model id `LFM3-1.7B`, `owned_by=llamacpp` |\n')
        (S / 'PROVINCE.md').write_text(text)
        (OUT / 'fixture-PROVINCE.md').write_text(text)
        log('FIXTURE_BYTES ' + repr(text.encode()))
        for path in ['/missing-health', '/v1/models']:
            url = root + path
            log('RESOLVE ' + url + ' ' + repr(gate.resolve('endpoint', url, S)))
        with urllib.request.urlopen(root + '/v1/models') as response:
            log('IDENTITY_RESPONSE_BYTES ' + repr(response.read()))
        rc = gate.emit(S, 'worktree', OUT / 'fixture-gate.txt')
        log('FIXTURE_GATE_RC ' + str(rc))
    finally:
        server.terminate()
        log('SERVER_WAIT_RC ' + str(server.wait(timeout=5)))

class Error500(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(500)
        self.end_headers()
        self.wfile.write(b'not the declared service\n')
    def log_message(self, *args):
        pass

with http.server.HTTPServer(('127.0.0.1', 0), Error500) as five:
    worker = threading.Thread(target=five.serve_forever)
    worker.start()
    try:
        url = f'http://127.0.0.1:{five.server_port}/health'
        log('RESOLVE_500 ' + repr(gate.resolve('endpoint', url, S)))
    finally:
        five.shutdown()
        worker.join()

for url in ['http://127.0.0.1:1234/health', 'http://127.0.0.1:45669/health']:
    cmd = ['curl', '--silent', '--show-error', '--max-time', '5', '--output', '/dev/null', '--write-out', '%{http_code}', url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    log('LIVE_COMMAND ' + repr(cmd))
    log('LIVE_RESULT ' + json.dumps({'url': url, 'rc': result.returncode, 'code': result.stdout, 'stderr': result.stderr}, sort_keys=True))
    log('LIVE_RESOLVE ' + url + ' ' + repr(gate.resolve('endpoint', url, S)))
(OUT / 'probe.txt').write_text('\n'.join(lines) + '\n')
