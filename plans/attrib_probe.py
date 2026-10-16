#!/usr/bin/env python3
"""attrib_probe.py — blind cascade-leg attribution instrument (kengaku round 21).

Seat: instrument-impl. Registered claim (round-21 N1): a frozen feature-table
instrument attributes which cascade leg served a given response through the
fleet's chat shims, WITHOUT reading the shim journal at request time.

Blind rule (enforced in code): the string `journalctl` occurs ONLY inside
cmd_score below. cmd_trials never reads the journal, the unit's logs, or any
ground-truth source. The feature table + weights + decision rule live in
plans/attrib-r21-frozen.md inside the fenced block

    ```attrib-feature-table-v1 ... ```

whose exact byte range is sha256-pinned by the FROZEN line that follows it.
cmd_trials refuses to send anything unless that pin verifies.

Stdlib only. No credentials are read; no Authorization header is sent; all
traffic is localhost shim traffic (ds-flash-shim :8791, glm-flash-shim :8793).
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from http.client import HTTPConnection

FROZEN_DEFAULT = "plans/attrib-r21-frozen.md"
BLOCK_START = "```attrib-feature-table-v1\n"
BLOCK_END = "\n```\n"
FROZEN_LINE_RE = re.compile(r"^FROZEN: (\S+) sha256:([0-9a-f]{64})\s*$", re.M)

SHIMS = {
    "ds": {"port": 8791, "unit": "ds-flash-shim", "model": "deepseek-v4.1-flash"},
    "glm": {"port": 8793, "unit": "glm-flash-shim", "model": "glm-5.3-flash"},
}

COUNT_PROMPT = "Count from 1 to 30, space separated, numbers only. No other text."


def std_body(model):
    # Key order matches the r19 P4 receipt shape (233 bytes for glm-5.3-flash).
    return {
        "model": model,
        "messages": [{"role": "user", "content": COUNT_PROMPT}],
        "max_tokens": 16,
        "stream": True,
        "stream_options": {"include_usage": True},
    }


def err_body(model):
    # r19 F-2: the devin leg rejects temperature -> exercises the error path.
    b = std_body(model)
    out = {"model": b["model"], "messages": b["messages"], "max_tokens": 16,
           "temperature": 0, "stream": True, "stream_options": {"include_usage": True}}
    return out


# ---------------------------------------------------------------- freeze ----

def block_bytes(text):
    i = text.find(BLOCK_START)
    if i < 0:
        raise SystemExit("frozen table: block start marker not found")
    j = text.find(BLOCK_END, i)
    if j < 0:
        raise SystemExit("frozen table: block end marker not found")
    return text[i:j + len(BLOCK_END)]


def load_frozen(path):
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    bb = block_bytes(text)
    sha = hashlib.sha256(bb.encode("utf-8")).hexdigest()
    m = FROZEN_LINE_RE.search(text)
    table = json.loads(bb[len(BLOCK_START):bb.rfind(BLOCK_END)])
    return {"raw": raw, "block_sha": sha, "frozen_line": m, "table": table}


def verify_frozen(path, double_read=False):
    """Recompute the block hash and compare with the FROZEN line.

    double_read=True performs the r19-lesson guard: two reads >=2 s apart,
    both hashes must equal each other and the pinned hash."""
    reads = []
    for k in range(2 if double_read else 1):
        if k:
            time.sleep(2.0)
        info = load_frozen(path)
        reads.append(info)
    first = reads[0]
    if first["frozen_line"] is None:
        print("FREEZE-CHECK: FAIL — no FROZEN line in %s" % path)
        return None
    pinned = first["frozen_line"].group(2)
    stamps = [first["frozen_line"].group(1)]
    oks = [first["block_sha"] == pinned]
    for r in reads[1:]:
        oks.append(r["block_sha"] == pinned and r["frozen_line"].group(2) == pinned)
        stamps.append(r["frozen_line"].group(1))
    ok = all(oks)
    print("FREEZE-CHECK: reads=%d block_sha=%s pinned=%s stable=%s -> %s"
          % (len(reads), first["block_sha"][:16], pinned[:16], all(oks),
             "OK" if ok else "FAIL"))
    return {"ok": ok, "sha": pinned, "frozen_utc": stamps[0], "table": first["table"]}


# ----------------------------------------------------------- observation ----

REDACT_HEADERS = {"set-cookie"}


def capture(shim, body_bytes, timeout_s):
    """One POST through the shim. Returns an observation dict; no GT access."""
    s = SHIMS[shim]
    t0 = time.time()
    conn = HTTPConnection("127.0.0.1", s["port"], timeout=timeout_s)
    obs = {"t0_epoch": t0,
           "t0_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
           "body_len": len(body_bytes), "status": None, "headers": {},
           "wall_s": None, "ttfb_s": None, "sse_events": 0, "body_text": "",
           "first_data_s": None, "last_data_s": None, "error": None}
    try:
        conn.request("POST", "/v1/chat/completions", body=body_bytes,
                     headers={"Content-Type": "application/json",
                              "Accept": "text/event-stream"})
        send_done = time.time()
        resp = conn.getresponse()
        obs["ttfb_s"] = round(time.time() - send_done, 4)
        obs["status"] = resp.status
        for k, v in resp.getheaders():
            lk = k.lower()
            obs["headers"][lk] = ("<redacted:len=%d>" % len(v)) if lk in REDACT_HEADERS else v
        ctype = obs["headers"].get("content-type", "")
        if "text/event-stream" in ctype and resp.status == 200:
            chunks = []
            for raw in resp:
                line = raw.decode("utf-8", "replace").strip()
                now = time.time() - send_done
                if line.startswith("data:"):
                    payload = line[5:].strip()
                    if payload == "[DONE]":
                        continue
                    try:
                        ev = json.loads(payload)
                    except ValueError:
                        continue
                    obs["sse_events"] += 1
                    if obs["first_data_s"] is None:
                        obs["first_data_s"] = now
                    obs["last_data_s"] = now
                    chunks.append(ev)
            obs["chunks"] = chunks
            obs["body_text"] = json.dumps(chunks)[:2000]
        else:
            raw = resp.read()
            obs["body_text"] = raw.decode("utf-8", "replace")[:2000]
            obs["chunks"] = []
    except Exception as e:  # timeout / connection error — recorded, not retried
        obs["error"] = "%s: %s" % (type(e).__name__, e)
    finally:
        try:
            conn.close()
        except Exception:
            pass
    obs["wall_s"] = round(time.time() - t0, 4)
    return obs


def extract_features(obs, requested_model):
    f = {}
    hdr = obs["headers"]
    tells = []
    server = hdr.get("server", "").lower()
    if "istio-envoy" in server:
        tells.append("server:istio-envoy")
    for h in ("x-envoy-upstream-service-time", "req-cost-time", "req-arrive-time",
              "resp-start-time", "grpc-encoding", "grpc-accept-encoding"):
        if h in hdr:
            tells.append(h)
    if "google frontend" in server:
        tells.append("server:google-frontend")
    for h in ("x-ratelimit-limit-day", "x-ratelimit-remaining-day", "x-ratelimit-limit-hour"):
        if h in hdr:
            tells.append(h)
    if "cloudflare" in server:
        tells.append("server:cloudflare")
    for h in ("cf-ray", "cf-placement", "x-opencode-log-id", "x-opencode-endpoint-id",
              "x-opencode-upstream-model-id", "x-zen-model"):
        if h in hdr:
            tells.append(h)
    if "devin-openai-shim/2" in server:
        tells.append("server:devin-openai-shim/2")
    for h in ("x-log-id", "ga-traceid", "set-cookie", "alt-svc"):
        if h in hdr:
            tells.append(h)
    f["hdr_tells"] = tells

    # model echo class
    echo = None
    if obs.get("chunks"):
        for ev in obs["chunks"]:
            if isinstance(ev, dict) and ev.get("model"):
                echo = ev["model"]
                break
    else:
        try:
            echo = json.loads(obs["body_text"]).get("model")
        except (ValueError, AttributeError):
            echo = None
    if echo is None:
        f["model_echo"] = None
    elif echo == requested_model:
        f["model_echo"] = "requested"
    else:
        f["model_echo"] = "rewritten:%s" % echo

    # usage schema + prompt_tokens
    usage = None
    src = obs.get("chunks") or []
    for ev in reversed(src):
        if isinstance(ev, dict) and isinstance(ev.get("usage"), dict):
            usage = ev["usage"]
            break
    if usage is None:
        try:
            usage = json.loads(obs["body_text"]).get("usage")
        except (ValueError, AttributeError):
            usage = None
    utells = []
    if isinstance(usage, dict):
        pd = usage.get("prompt_tokens_details") or {}
        if "text_tokens" in pd:
            utells.append("usage:text_tokens")
        if "cached_tokens" in pd:
            utells.append("usage:cached_tokens")
        for k in ("hypercredits", "cost"):
            if k in usage:
                utells.append("usage:%s" % k)
    f["usage_tells"] = utells
    f["prompt_tokens"] = usage.get("prompt_tokens") if isinstance(usage, dict) else None

    # stream shape (any-delta span, the 5b-adjudicated basis)
    if obs.get("first_data_s") is not None:
        span_ms = (obs["last_data_s"] - obs["first_data_s"]) * 1000.0
        f["stream_span_ms"] = round(span_ms, 1)
        f["stream_span_class"] = "burst" if span_ms < 50.0 else "incremental"
    else:
        f["stream_span_ms"] = None
        f["stream_span_class"] = None

    # id class
    oid = None
    if obs.get("chunks"):
        for ev in obs["chunks"]:
            if isinstance(ev, dict) and ev.get("id"):
                oid = ev["id"]
                break
    else:
        try:
            oid = json.loads(obs["body_text"]).get("id")
        except (ValueError, AttributeError):
            oid = None
    f["id_value"] = oid
    if oid and oid == hdr.get("x-request-id"):
        f["id_class"] = "eq-x-request-id"
    elif oid and oid == hdr.get("x-log-id"):
        f["id_class"] = "eq-x-log-id"
    elif isinstance(oid, str) and oid.startswith("chatcmpl-"):
        f["id_class"] = "chatcmpl-uuid"
    elif isinstance(oid, str) and re.fullmatch(r"\d{14}[0-9a-f]{11}", oid):
        f["id_class"] = "date-prefixed"
    else:
        f["id_class"] = "other"

    # error wording (fires only on non-200)
    etells = []
    if obs["status"] is not None and obs["status"] != 200:
        for t in ("devin_shim_error", "invalid_argument", "trace ID:",
                  "data_inspection_failed"):
            if t in obs["body_text"]:
                etells.append(t)
    f["error_tells"] = etells

    f["wall_s"] = obs["wall_s"]
    f["status"] = obs["status"]
    return f


# -------------------------------------------------------------- scoring ----

def score_obs(table, shim_key, feats, weights=None):
    """Frozen additive model. Returns (scores, prediction, confidence, detail).

    `weights` is unused (weights always come from the table); ablations pass a
    deep-copied table with selected weights zeroed (score_with_weights)."""
    shim = table["shims"][shim_key]
    legs = shim["legs"]
    prof = shim["leg_profiles"]
    w = table["weights"]
    scores = {leg: 0.0 for leg in legs}
    detail = {}

    def tell_feature(field, weight_key):
        obs_set = set(feats[field])
        hits = {leg: len(obs_set & set(prof[leg].get(field, []))) for leg in legs}
        best = max(hits.values()) if hits else 0
        for leg in legs:
            x = (hits[leg] / best) if best > 0 else 0.0
            scores[leg] += w[weight_key] * x
            detail[field] = hits

    tell_feature("hdr_tells", "hdr_tells")
    tell_feature("usage_tells", "usage_tells")
    if feats["status"] != 200:
        tell_feature("error_tells", "error_tells")

    def class_feature(field, weight_key, profile_key):
        ov = feats[field]
        for leg in legs:
            expect = prof[leg].get(profile_key)
            x = 1.0 if (ov is not None and expect == ov) else 0.0
            scores[leg] += w[weight_key] * x
        detail[field] = {leg: prof[leg].get(profile_key) for leg in legs}

    class_feature("model_echo", "model_echo", "model_echo")

    def band_feature(field, weight_key, profile_key):
        ov = feats[field]
        for leg in legs:
            band = prof[leg].get(profile_key)
            x = 1.0 if (ov is not None and isinstance(band, list)
                        and band[0] <= ov <= band[1]) else 0.0
            scores[leg] += w[weight_key] * x
        detail[profile_key] = {leg: prof[leg].get(profile_key) for leg in legs}

    band_feature("prompt_tokens", "prompt_tokens_band", "prompt_tokens_band")
    band_feature("wall_s", "wall_band", "wall_band_s")
    class_feature("stream_span_class", "stream_span_class", "stream_span_class")

    obs_idc = feats["id_class"]
    for leg in legs:
        expect = prof[leg].get("id_class") or []
        x = 1.0 if (obs_idc in expect) else 0.0
        scores[leg] += w["id_class"] * x
    detail["id_class"] = {leg: prof[leg].get("id_class") for leg in legs}

    order = legs[:]
    pred = None
    if feats["status"] is not None and feats["status"] != 200:
        err_best = max((len(set(feats["error_tells"]) & set(prof[leg].get("error_tells", [])))
                        for leg in legs), default=0)
        if err_best == 0:
            pred = order[-1]  # frozen status-masking rule: roster-last leg
    if pred is None:
        best = max(scores.values())
        pred = next(leg for leg in order if scores[leg] == best)
    total = sum(scores.values())
    conf = (scores[pred] / total) if total > 0 else 0.0
    return scores, pred, round(conf, 3), detail


def score_with_weights(table, shim_key, feats, zero_features):
    """Deep-copy the weights with the named features zeroed (ablations)."""
    import copy
    t2 = copy.deepcopy(table)
    for k in zero_features:
        t2["weights"][k] = 0.0
    return score_obs(t2, shim_key, feats)


# ---------------------------------------------------------------- trials ----

def cmd_trials(args):
    shim = SHIMS[args.shim]
    fr = verify_frozen(args.frozen, double_read=False)
    if not fr or not fr["ok"]:
        print("trials: frozen-table verification FAILED — no request sent (exit 2)")
        return 2
    table = fr["table"]
    n_std = table["request_budget_per_shim"]["standard_trials"]
    n_err = table["request_budget_per_shim"]["error_path_trials"].get(shim["unit"], 0)
    spacing = table["trial_protocol"]["planned_spacing_s"]
    timeout = table["trial_protocol"]["client_timeout_s"]
    meta = {"kind": "meta", "shim": args.shim, "unit": shim["unit"], "port": shim["port"],
            "model": shim["model"], "frozen_sha256_at_start": fr["sha"],
            "frozen_utc": fr["frozen_utc"], "n_standard": n_std, "n_error_path": n_err,
            "instrument": "plans/attrib_probe.py",
            "instrument_sha256": hashlib.sha256(
                open(__file__, "rb").read()).hexdigest(),
            "blind_rule": "no journal read in this phase (journalctl exists only in cmd_score)"}
    out = open(args.out, "a")
    recpt = open(args.receipt, "a")
    def emit(line):
        print(line)
        out.write(line + "\n")
        recpt.write(line + "\n")
        out.flush()
        recpt.flush()
    emit("# attrib-r21-impl-%s-trials — instrument-impl seat, kengaku round 21" % args.shim)
    emit("# Target: 127.0.0.1:%d %s" % (shim["port"], shim["unit"]))
    emit("# Instrument: plans/attrib_probe.py sha256 %s" % meta["instrument_sha256"])
    emit("# Frozen table: %s anchor sha256 %s (FROZEN %s) — verified before first request"
         % (args.frozen, fr["sha"], fr["frozen_utc"]))
    emit("# Blind rule: no journal/GT read during trials; the score phase appends below AFTER all trials.")
    emit("# No Authorization header sent; no credential material read. Executions begin after this line.")
    emit(json.dumps(meta))

    body_std = json.dumps(std_body(shim["model"])).encode()
    body_err = json.dumps(err_body(shim["model"])).encode() if n_err else None
    trials = []
    tid = 0
    for kind in ["std"] * n_std + (["err"] * n_err if n_err else []):
        tid += 1
        body = body_std if kind == "std" else body_err
        obs = capture(args.shim, body, timeout)
        feats = extract_features(obs, shim["model"])
        scores, pred, conf, _ = score_obs(table, args.shim, feats, weights=None)
        rec = {"kind": "trial", "trial_id": tid, "class": kind, "obs": obs,
               "features": feats, "scores": scores, "prediction": pred,
               "confidence": conf}
        trials.append(rec)
        emit("=== [T%02d/%s] %s POST /v1/chat/completions (%s)"
             % (tid, "std" if kind == "std" else "err-path", obs["t0_utc"], kind))
        if obs["error"]:
            emit("    ERROR: %s (recorded, not retried; excluded from accuracy denominator)"
                 % obs["error"])
        else:
            emit("    status=%s wall=%.3fs ttfb=%.3fs span_ms=%s events=%d echo=%s id_class=%s pt=%s"
                 % (obs["status"], obs["wall_s"], obs["ttfb_s"] or -1,
                    feats["stream_span_ms"], obs["sse_events"],
                    feats["model_echo"], feats["id_class"], feats["prompt_tokens"]))
            emit("    hdr_tells: %s" % (",".join(feats["hdr_tells"]) or "(none)"))
            if feats["error_tells"]:
                emit("    error_tells: %s" % ",".join(feats["error_tells"]))
            emit("    body: %s" % obs["body_text"][:300].replace("\n", " "))
        emit("    prediction=%s confidence=%.3f scores=%s"
             % (pred, conf, json.dumps({k: round(v, 2) for k, v in scores.items()})))
        emit(json.dumps({"kind": "record", "trial_id": tid, "class": kind,
                         "features": feats, "prediction": pred,
                         "confidence": conf, "t0_epoch": obs["t0_epoch"],
                         "t0_utc": obs["t0_utc"], "body_len": obs["body_len"],
                         "status": obs["status"], "error": obs["error"]}))
        if tid < n_std + n_err:
            time.sleep(spacing)
    emit("# trials done: n=%d (std=%d err=%d) last_request_utc=%s — journal GT intentionally NOT read"
         % (len(trials), n_std, n_err,
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    out.close()
    recpt.close()
    return 0


# ----------------------------------------------------------------- score ----

TS_RE = re.compile(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})([+-]\d{4})")
REQ_RE = re.compile(r"rid=([0-9a-f]+) REQUEST model='([^']*)' stream=(True|False) bytes=(\d+)")
LEG_RE = re.compile(r"rid=([0-9a-f]+) leg=(\d+)/(\S+) (OK|FAIL) status=(\d+|None)")
ALLFAIL_RE = re.compile(r"rid=([0-9a-f]+) ALL LEGS FAILED")


def parse_ts(stamp, off):
    dt = datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%S")
    sign = 1 if off[0] == "+" else -1
    delta = timedelta(hours=int(off[1:3]), minutes=int(off[3:5])) * sign
    utc_naive = dt - delta  # UTC wall time; naive .timestamp() would re-apply
    # the host's local offset (anti-pattern 15 class), so compute epoch directly:
    return (utc_naive - datetime(1970, 1, 1)).total_seconds()  # epoch UTC


def cmd_score(args):
    shim = SHIMS[args.shim]
    fr = verify_frozen(args.frozen, double_read=False)
    if not fr or not fr["ok"]:
        print("score: frozen-table verification FAILED (exit 2)")
        return 2
    table = fr["table"]
    recs = []
    with open(args.trials) as f:
        for line in f:
            line = line.strip()
            if line.startswith("{"):
                r = json.loads(line)
                if r.get("kind") in ("meta", "record"):
                    recs.append(r)
    meta = next(r for r in recs if r["kind"] == "meta")
    trials = [r for r in recs if r["kind"] == "record"]
    t_lo = min(t["t0_epoch"] for t in trials) - 5
    t_hi = max(t["t0_epoch"] for t in trials) + 30

    # ---- the ONLY journal read in the instrument, after all trials ----
    cmd = ["journalctl", "--user", "-u", shim["unit"], "--since", "@%d" % int(t_lo),
           "--until", "@%d" % int(t_hi), "--no-pager"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    reqs, legs, allfail = [], {}, set()
    for line in out.stdout.splitlines():
        mts = TS_RE.search(line)
        if not mts:
            continue
        ts = parse_ts(mts.group(1), mts.group(2))
        m = REQ_RE.search(line)
        if m:
            reqs.append({"rid": m.group(1), "epoch": ts, "bytes": int(m.group(4)),
                         "model": m.group(2), "stream": m.group(3)})
            continue
        m = LEG_RE.search(line)
        if m:
            legs.setdefault(m.group(1), []).append(
                {"n": int(m.group(2)), "leg": m.group(3), "ok": m.group(4) == "OK",
                 "status": m.group(5), "epoch": ts})
            continue
        m = ALLFAIL_RE.search(line)
        if m:
            allfail.add(m.group(1))

    scored, excluded = [], []
    # greedy in-order assignment: trials and journal REQUEST stamps are both
    # strictly ordered; 1-second stamp truncation can pull the NEXT trial's
    # stamp into the previous trial's window, so a per-trial independent match
    # is ambiguous exactly there. Trials are sequential (>=2s spacing, one
    # request per step), so assign stamps to trials 1:1 in t0 order, taking
    # the earliest unused candidate in each trial's window.
    used = set()
    ordered = sorted(trials, key=lambda t: t["t0_epoch"])
    assign = {}
    for t in ordered:
        cands = [r for r in reqs if r["bytes"] == t["body_len"]
                 and (t["t0_epoch"] - 1.0) <= r["epoch"] <= (t["t0_epoch"] + 3.0)
                 and r["rid"] not in used]
        if not cands:
            cands = [r for r in reqs if r["bytes"] == t["body_len"]
                     and abs(r["epoch"] - t["t0_epoch"]) <= 5.0
                     and r["rid"] not in used]
        if len(cands) == 0:
            assign[id(t)] = None
            continue
        pick = min(cands, key=lambda r: r["epoch"])
        used.add(pick["rid"])
        assign[id(t)] = pick
    for t in trials:
        cands = assign.get(id(t))
        if cands is None:
            t["gt"] = "UNMATCHED"
            excluded.append((t, "UNMATCHED"))
            continue
        rid = cands["rid"]
        t["rid"] = rid
        chain = legs.get(rid, [])
        oks = [l for l in chain if l["ok"]]
        if oks:
            t["gt"] = oks[0]["leg"]
            t["gt_class"] = "served"
        elif chain:
            last = sorted(chain, key=lambda l: l["n"])[-1]
            t["gt"] = last["leg"]
            t["gt_class"] = "relay-last-fail"
        else:
            t["gt"] = "NO-LEG-LINES"
            excluded.append((t, t["gt"]))
            continue
        t["chain"] = "; ".join("%d/%s %s %s" % (l["n"], l["leg"],
                                                "OK" if l["ok"] else "FAIL", l["status"])
                               for l in chain) + ("; ALL-FAILED" if rid in allfail else "")
        scored.append(t)

    def accuracy(trs, zero=()):
        ok = 0
        for t in trs:
            _, pred, _, _ = score_with_weights(table, args.shim, t["features"], zero)
            if pred == t["gt"]:
                ok += 1
        return ok, len(trs)

    base_ok, base_n = accuracy(scored)
    w = table["weights"]
    ablations = {}
    for feat in w:
        ablations["loo:%s" % feat] = accuracy(scored, zero=(feat,))
    ablations["mimicry:header-strip(hdrid)"] = accuracy(scored, zero=("hdr_tells", "id_class"))
    ablations["mimicry:latency-pad"] = accuracy(scored, zero=("wall_band",))
    ablations["mimicry:echo-spoof"] = accuracy(scored, zero=("model_echo",))

    bar = table["bar"]
    lines = []
    lines.append("")
    lines.append("## GT + scoring at close (journal read AFTER all trials — %s)" %
                 datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    lines.append("# journal command: %s" % " ".join(cmd))
    lines.append("# journal stdout lines=%d request-lines=%d leg-rids=%d allfail=%d"
                 % (len(out.stdout.splitlines()), len(reqs), len(legs), len(allfail)))
    lines.append("# frozen table re-verified at scoring: sha256 %s" % fr["sha"])
    lines.append("")
    lines.append("| trial | class | prediction | GT | gt_class | chain | correct |")
    lines.append("|---|---|---|---|---|---|---|")
    for t in scored:
        lines.append("| T%02d | %s | %s | %s | %s | %s | %s |"
                     % (t["trial_id"], t["class"], t["prediction"], t["gt"],
                        t.get("gt_class", ""), t.get("chain", "")[:80],
                        "YES" if t["prediction"] == t["gt"] else "NO"))
    for t, why in excluded:
        lines.append("| T%02d | %s | %s | EXCLUDED:%s | — | — | — |"
                     % (t["trial_id"], t["class"], t["prediction"], why))
    gt_counts = {}
    for t in scored:
        gt_counts[t["gt"]] = gt_counts.get(t["gt"], 0) + 1
    lines.append("")
    lines.append("GT counts: %s" % json.dumps(gt_counts))
    acc = base_ok / base_n if base_n else 0.0
    verdict = ("PASS" if (base_n >= bar["min_scored_trials_per_shim"]
                          and acc >= bar["min"]) else "FAIL")
    lines.append("ACCURACY: %d/%d = %.3f (bar %.2f, min scored n %d) -> %s"
                 % (base_ok, base_n, acc, bar["min"],
                    bar["min_scored_trials_per_shim"], verdict))
    lines.append("per-leg GT counts mean honesty note: legs with 0 GT trials are UNTESTED by this run")
    lines.append("")
    lines.append("Mimicry/ablation accuracies (frozen protocol §mimicry):")
    for name, (ok, n) in ablations.items():
        lines.append("  %-34s %d/%d = %.3f" % (name, ok, n, ok / n if n else 0.0))
    summary = {"kind": "score_summary", "shim": args.shim, "accuracy": acc,
               "scored": base_n, "correct": base_ok, "verdict": verdict,
               "gt_counts": gt_counts, "excluded": [[t["trial_id"], w2] for t, w2 in excluded],
               "ablations": {k: {"ok": v[0], "n": v[1]} for k, v in ablations.items()},
               "frozen_sha256": fr["sha"]}
    lines.append(json.dumps(summary))
    text = "\n".join(lines) + "\n"
    with open(args.receipt, "a") as f:
        f.write(text)
    print(text)
    if args.out:
        with open(args.out, "a") as f:
            f.write(json.dumps(summary) + "\n")
    return 0 if verdict == "PASS" else 1


def cmd_block_sha(args):
    with open(args.frozen, "rb") as f:
        raw = f.read()
    print(hashlib.sha256(block_bytes(raw.decode("utf-8")).encode("utf-8")).hexdigest())
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("block-sha")
    p.add_argument("--frozen", default=FROZEN_DEFAULT)
    p = sub.add_parser("freeze-check")
    p.add_argument("--frozen", default=FROZEN_DEFAULT)
    p.add_argument("--double-read", action="store_true")
    p = sub.add_parser("trials")
    p.add_argument("--shim", required=True, choices=sorted(SHIMS))
    p.add_argument("--frozen", default=FROZEN_DEFAULT)
    p.add_argument("--out", required=True, help="JSONL scratch (kengaku-tmp)")
    p.add_argument("--receipt", required=True, help="corpus/evidence receipt log")
    p = sub.add_parser("score")
    p.add_argument("--shim", required=True, choices=sorted(SHIMS))
    p.add_argument("--frozen", default=FROZEN_DEFAULT)
    p.add_argument("--trials", required=True, help="JSONL scratch from trials")
    p.add_argument("--receipt", required=True, help="corpus/evidence receipt log (appended)")
    p.add_argument("--out", default=None, help="optional JSONL scratch for the summary")
    args = ap.parse_args()
    if args.cmd == "block-sha":
        return cmd_block_sha(args)
    if args.cmd == "freeze-check":
        r = verify_frozen(args.frozen, double_read=args.double_read)
        return 0 if (r and r["ok"]) else 2
    if args.cmd == "trials":
        return cmd_trials(args)
    if args.cmd == "score":
        return cmd_score(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
