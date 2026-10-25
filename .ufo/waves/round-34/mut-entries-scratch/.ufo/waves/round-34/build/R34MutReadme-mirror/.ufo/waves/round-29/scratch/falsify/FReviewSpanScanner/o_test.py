import importlib.util, json, sys, io, contextlib
PROD="/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py"
RAW_TEXT = sys.argv[1]; MODE = sys.argv[2] if len(sys.argv)>2 else "--json"
spec=importlib.util.spec_from_file_location("cp_prod",PROD); cp=importlib.util.module_from_spec(spec); spec.loader.exec_module(cp)
real=cp.read_pinned
def fake(root):
    m,v = real(root); v=dict(v); v[cp.RAW]=RAW_TEXT.encode('utf-8'); return m,v
cp.read_pinned=fake
sys.argv=["config_projection.py","--root","/home/vgpnk/Projects/shokunin/kengaku-shokunin",MODE]
buf=io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        code=cp.main()
    out=buf.getvalue()
    try: j=json.loads(out); print("EXIT",code,"| findings:",json.dumps(j.get("findings")))
    except Exception: print("EXIT",code,"| raw:",out[:200])
except BaseException as e:
    print("UNCAUGHT", type(e).__name__, e, "| uncaught => exit 1")
