import sys, json, importlib.util, pathlib, collections

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
SCRIPT = LANE + "/plans/config_projection.py"

events = []
def hook(name, args):
    if name == "open":
        events.append((name, str(args[0]), args[1]))
    elif name in ("socket.connect", "socket.getaddrinfo", "socket.gethostbyname", "urllib.Request"):
        events.append((name, repr(args[1])[:120], None))
sys.addaudithook(hook)

spec = importlib.util.spec_from_file_location("cfgproj", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mark = len(events)

result, code = mod.audit(pathlib.Path(LANE))
print("AUDIT_EXIT", code)
print("AUDIT_FINDINGS", json.dumps(result.get("findings"), sort_keys=True))

lane_events = [e for e in events[mark:] if LANE in e[1]]
print("LANE_FILE_OPENS", len(lane_events))
for e in lane_events:
    print("  OPEN", e[1].replace(LANE, "<LANE>"), e[2])
other = [e for e in events[mark:] if LANE not in e[1] and not str(e[1]).startswith("<") ]
net = [e for e in events[mark:] if e[0] != "open"]
print("NET_OR_OTHER_AUDIT_EVENTS", len(net))
for e in net[:40]:
    print("  NET", e[0], e[1])

# read-once census: count Path.read_bytes calls per path during one audit()
calls = collections.Counter()
orig_read_bytes = pathlib.Path.read_bytes
def counting(self):
    calls[str(self)] += 1
    return orig_read_bytes(self)
pathlib.Path.read_bytes = counting
result2, code2 = mod.audit(pathlib.Path(LANE))
pathlib.Path.read_bytes = orig_read_bytes
print("READ_BYTES_CALLS", json.dumps({k.replace(LANE, "<LANE>"): v for k, v in sorted(calls.items())}, sort_keys=True))
print("SECOND_AUDIT_EXIT", code2)
