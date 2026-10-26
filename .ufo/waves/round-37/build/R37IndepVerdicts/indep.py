#!/usr/bin/env python3
"""Round-37 C2 independent check: re-run the frozen 22 cases of the pinned TB2 grader receipt
WITHOUT the probe's bubblewrap, and compare verdicts per case.

    python3 indep.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
        --work /fast/scratch/hyaku/kengaku-r37/R37IndepVerdicts/work \
        --receipt <out.txt>

Isolation (deliberately different from plans/git_webserver_probe.py, which uses bwrap):
each case runs in its own `unshare --user --map-root-user --net --fork` namespace. The namespace
gets a fresh loopback (`ip link set lo up`), so :8080 is never the host's and no case can see
another case's server. HOME, cwd and TMPDIR are per-case directories under --work; verify.sh's
`mkdir -p ~/.ssh` / `~/.ssh/config` write therefore never touch the operator's home, and its
`git_test.exp` / `test_output.html` land in the per-case cwd. PATH contains only
bash, sleep, chmod, mkdir, cat plus curl (or wget for the wget cases): apt-get, expect and, for
the wget cases, curl are absent from PATH exactly as the receipt says. The verdict rule is
tests/test_outputs.py:13 applied to verify.sh's captured stdout: `"TEST PASSED" in stdout`.

Case table: parsed from the frozen table corpus/evidence/round37/git-webserver-dry-cases-freeze.txt
(`CASE <cid> tools=<..> predicted=<..> server=<json> -- <requirement>`), so the server behaviour is
the frozen one, not a retyped one. Receipt comparison: `observed=` per CASE line of
corpus/evidence/round37/git-webserver-probe.txt. The three extra cases and their predictions are
read from extras-predictions.txt next to this script (written before the first run).

Nothing is written outside --work and --receipt. Scratch case dirs are removed at exit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

CAP = "corpus/evidence/round37/tb2-git-webserver"
FREEZE = "corpus/evidence/round37/git-webserver-dry-cases-freeze.txt"
RECEIPT = "corpus/evidence/round37/git-webserver-probe.txt"
PINS = {
    "verify.sh": "1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05",
    "test_outputs.py": "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37",
}
BASE_TOOLS = ("bash", "sleep", "chmod", "mkdir", "cat")

SERVER_PY = r'''
import http.server, json, pathlib, socketserver, sys, time
cfg = json.loads(pathlib.Path(sys.argv[1]).read_text())
ready = pathlib.Path(sys.argv[2])
count = {"n": 0}
class H(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"
    def log_message(self, *a):
        pass
    def answer(self):
        if cfg.get("delay"):
            time.sleep(cfg["delay"])
        mode = cfg["mode"]
        headers = {}
        if mode == "catchall":
            status, body = 200, cfg["body"]
        elif mode == "sequence":
            if self.path != cfg["path"]:
                status, body = 404, ""
            else:
                seq = cfg["responses"]
                status, body = seq[min(count["n"], len(seq) - 1)]
                count["n"] += 1
        elif mode == "head200get404":
            if self.command == "HEAD":
                status, body = 200, cfg.get("body", "")
            else:
                status, body = 404, ""
        else:
            status, body, headers = cfg["routes"].get(self.path, [404, "", {}])
        data = body.encode("utf-8")
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)
    do_GET = answer
    do_HEAD = answer
class S(socketserver.TCPServer):
    allow_reuse_address = True
srv = S(("127.0.0.1", cfg["port"]), H)
ready.write_text("1")
srv.serve_forever()
'''

RUN_SH = r'''#!/usr/bin/bash
set -u
W="$1"
V="$2"
/usr/bin/ip link set lo up 2>/dev/null || { echo "__SETUP__ lo"; exit 3; }
SPID=""
if [ -s "$W/server.json" ]; then
  /usr/bin/python3 "$W/server.py" "$W/server.json" "$W/ready" >"$W/server.log" 2>&1 </dev/null &
  SPID=$!
  i=0
  while [ "$i" -lt 60 ]; do
    [ -e "$W/ready" ] && break
    /usr/bin/sleep 0.1
    i=$((i+1))
  done
  [ -e "$W/ready" ] || { echo "__SETUP__ server-not-ready"; kill "$SPID" 2>/dev/null; exit 3; }
fi
cd "$W/cwd" || exit 3
/usr/bin/bash "$V" >"$W/stdout.txt" 2>"$W/stderr.txt"
VRC=$?
if /usr/bin/grep -qF -- 'TEST PASSED' "$W/stdout.txt"; then RULE=pass; else RULE=fail; fi
echo "__RULE__ $RULE"
echo "__VRC__ $VRC"
if [ -n "$SPID" ]; then kill "$SPID" 2>/dev/null; wait "$SPID" 2>/dev/null; fi
exit 0
'''

FREEZE_LINE = re.compile(
    r"^CASE (?P<cid>\S+) tools=(?P<tools>\S+) predicted=(?P<predicted>\S+) server=(?P<rest>.*)$")
RECEIPT_LINE = re.compile(r"^CASE (?P<cid>\S+) .*observed=(?P<observed>\S+).*$")


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parse_freeze(p: pathlib.Path) -> list[dict]:
    dec = json.JSONDecoder()
    out = []
    for line in p.read_text().splitlines():
        m = FREEZE_LINE.match(line)
        if not m:
            continue
        rest = m.group("rest")
        server, end = dec.raw_decode(rest)
        tail = rest[end:].strip()
        requirement = tail[2:].strip() if tail.startswith("--") else tail
        out.append({"cid": m.group("cid"), "tools": m.group("tools"),
                    "predicted": m.group("predicted"), "server": server,
                    "requirement": requirement})
    return out


def parse_receipt(p: pathlib.Path) -> dict[str, str]:
    out = {}
    for line in p.read_text().splitlines():
        m = RECEIPT_LINE.match(line)
        if m:
            out[m.group("cid")] = m.group("observed")
    return out


def parse_predictions(p: pathlib.Path) -> dict[str, str]:
    out = {}
    for line in p.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^(?P<cid>\S+) predicted=(?P<v>pass|fail)\b", line)
        if m:
            out[m.group("cid")] = m.group("v")
    return out


def which(name: str) -> str:
    p = shutil.which(name)
    if not p:
        raise SystemExit(f"SETUP required tool missing: {name}")
    return p


def run_case(root: pathlib.Path, verify: pathlib.Path, cid: str, tools: str, server: dict,
             timeout: int = 300) -> dict:
    work = root / cid
    for sub in ("home", "cwd", "bin", "tmp"):
        (work / sub).mkdir(parents=True, exist_ok=True)
    names = list(BASE_TOOLS) + ([] if tools == "none" else [tools])
    for n in names:
        link = work / "bin" / n
        if link.exists() or link.is_symlink():
            link.unlink()
        link.symlink_to(which(n))
    (work / "server.json").write_text(json.dumps(server) if server else "")
    (work / "server.py").write_text(SERVER_PY)
    (work / "run.sh").write_text(RUN_SH)
    env = {"PATH": str(work / "bin"), "HOME": str(work / "home"), "TMPDIR": str(work / "tmp"),
           "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    argv = ["/usr/bin/unshare", "--user", "--map-root-user", "--net", "--fork", "--",
            "/usr/bin/bash", str(work / "run.sh"), str(work), str(verify)]
    r = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=timeout)
    stdout = (work / "stdout.txt").read_text(errors="replace") if (work / "stdout.txt").is_file() else ""
    stderr = (work / "stderr.txt").read_text(errors="replace") if (work / "stderr.txt").is_file() else ""
    rule = re.search(r"^__RULE__ (pass|fail)$", r.stdout, re.M)
    vrc = re.search(r"^__VRC__ (-?\d+)$", r.stdout, re.M)
    verdict = rule.group(1) if rule else f"SETUP:{r.returncode}"
    return {"cid": cid, "tools": tools, "verdict": verdict,
            "verify_rc": int(vrc.group(1)) if vrc else None,
            "stdout": stdout, "stderr": stderr, "setup": r.stdout.strip(), "rc": r.returncode}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/kengaku-shokunin")
    ap.add_argument("--work", required=True, help="scratch root (created; case dirs removed)")
    ap.add_argument("--receipt", default=None, help="write the printed receipt here too")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    cap = lane / CAP
    for name, digest in PINS.items():
        if not (cap / name).is_file() or sha256(cap / name) != digest:
            print(f"SETUP capture {name} missing or not at its pinned digest", file=sys.stderr)
            return 2
    freeze_p, receipt_p = lane / FREEZE, lane / RECEIPT
    cases = parse_freeze(freeze_p)
    if len(cases) != 22 or len({c["cid"] for c in cases}) != 22:
        print(f"SETUP freeze parsed {len(cases)} cases", file=sys.stderr)
        return 2
    receipt = parse_receipt(receipt_p)
    if len(receipt) != 22:
        print(f"SETUP receipt parsed {len(receipt)} observed verdicts", file=sys.stderr)
        return 2
    preds = parse_predictions(pathlib.Path(__file__).with_name("extras-predictions.txt"))
    extras = [
        {"cid": "x-token-line", "tools": "curl",
         "server": {"mode": "files", "port": 8080,
                    "routes": {"/hello.html": [200, "xx TEST PASSED yy\n", {}]}},
         "requirement": "body carries 'TEST PASSED' between other words on one line"},
        {"cid": "x-head200-get404", "tools": "curl",
         "server": {"mode": "head200get404", "port": 8080, "body": "hello world\n"},
         "requirement": "200 for HEAD, 404 for GET"},
        {"cid": "x-gzip-header", "tools": "curl",
         "server": {"mode": "files", "port": 8080,
                    "routes": {"/hello.html": [200, "hello world\n", {"Content-Encoding": "gzip"}]}},
         "requirement": "plain 'hello world' body served with Content-Encoding: gzip"},
    ]
    for e in extras:
        if e["cid"] not in preds:
            print(f"SETUP no recorded prediction for extra case {e['cid']}", file=sys.stderr)
            return 2

    root = pathlib.Path(a.work)
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    out: list[str] = []
    out.append("# independent re-run of the tb2 configure-git-webserver receipt (kengaku round 37)")
    out.append(f"# freeze sha256={sha256(freeze_p)} cases={len(cases)}")
    out.append(f"# receipt sha256={sha256(receipt_p)}")
    for name in sorted(PINS):
        out.append(f"# capture {name} sha256={sha256(cap / name)}")
    out.append("# isolation: unshare --user --map-root-user --net --fork; fresh loopback per case; "
               "PATH=bash,sleep,chmod,mkdir,cat(+curl|wget); HOME/cwd/TMPDIR per case")
    agree = disagree = pred_match = 0
    disagreements: list[str] = []
    try:
        for c in cases:
            res = run_case(root, cap / "verify.sh", c["cid"], c["tools"], c["server"])
            ref = receipt[c["cid"]]
            ok = res["verdict"] == ref
            agree += ok
            disagree += not ok
            pred_match += res["verdict"] == c["predicted"]
            if not ok:
                disagreements.append(c["cid"])
            out.append(f"CASE {c['cid']} tools={c['tools']} predicted={c['predicted']} "
                       f"receipt={ref} observed={res['verdict']} match_receipt={'yes' if ok else 'NO'} "
                       f"verify_rc={res['verify_rc']} -- {c['requirement']}")
            lines = res["stdout"].splitlines()
            out.append("  grader-stdout: " + (" | ".join(repr(x) for x in lines) if lines else "(none)"))
            if res["verdict"].startswith("SETUP"):
                err = res["stderr"].strip().splitlines()
                out.append("  setup: " + res["setup"].replace("\n", " | "))
                out.append("  verify-stderr: " + (" | ".join(repr(x) for x in err) if err else "(none)"))
        ex_match = 0
        for e in extras:
            res = run_case(root, cap / "verify.sh", e["cid"], e["tools"], e["server"])
            p = preds[e["cid"]]
            ok = res["verdict"] == p
            ex_match += ok
            out.append(f"EXTRA {e['cid']} tools={e['tools']} predicted={p} observed={res['verdict']} "
                       f"match={'yes' if ok else 'NO'} verify_rc={res['verify_rc']} -- {e['requirement']}")
            lines = res["stdout"].splitlines()
            out.append("  grader-stdout: " + (" | ".join(repr(x) for x in lines) if lines else "(none)"))
            if res["verdict"].startswith("SETUP"):
                out.append("  setup: " + res["setup"].replace("\n", " | "))
        out.append(f"cases={len(cases)} agree_receipt={agree} disagree_receipt={disagree} "
                   f"predicted_match={pred_match}")
        out.append(f"extras={len(extras)} extra_matched={ex_match}")
        if disagreements:
            out.append("DISAGREE " + " ".join(disagreements))
        out.append(f"INDEP agree={agree}/{len(cases)} extra={ex_match}/{len(extras)}")
    finally:
        if not a.keep:
            shutil.rmtree(root, ignore_errors=True)
    text = "\n".join(out) + "\n"
    sys.stdout.write(text)
    if a.receipt:
        pathlib.Path(a.receipt).write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
