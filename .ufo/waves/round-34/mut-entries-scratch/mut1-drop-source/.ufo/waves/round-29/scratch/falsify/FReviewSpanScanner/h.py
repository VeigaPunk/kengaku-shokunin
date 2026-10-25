
import json, sys
sys.path.insert(0,"/tmp/r29span")
import importlib.util
spec=importlib.util.spec_from_file_location("cp_prod","/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py")
cp=importlib.util.module_from_spec(spec); spec.loader.exec_module(cp)
text = sys.argv[1]
try:
    doc = json.loads(text)          # audit_text does this FIRST
    spans = cp.string_spans(text)   # then this
    print("OK spans=%d" % len(spans))
except (OSError, ValueError, KeyError, TypeError, AssertionError, IndexError) as e:
    print("CAUGHT-BY-MAIN: %s: %s" % (type(e).__name__, e))
