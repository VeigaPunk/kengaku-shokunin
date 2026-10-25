import importlib.util, json, sys, io, contextlib
TARGET=sys.argv[1]; RAW_TEXT=sys.argv[2]
spec=importlib.util.spec_from_file_location("cp",TARGET); cp=importlib.util.module_from_spec(spec); spec.loader.exec_module(cp)
real=cp.read_pinned
def fake(root):
    m,v=real(root); v=dict(v); v[cp.RAW]=RAW_TEXT.encode('utf-8'); return m,v
cp.read_pinned=fake
sys.argv=["x","--root","/home/vgpnk/Projects/shokunin/kengaku-shokunin","--json"]
buf=io.StringIO()
try:
    with contextlib.redirect_stdout(buf): code=cp.main()
    print("EXIT",code,"| findings:",json.dumps(json.loads(buf.getvalue()).get("findings"))[:180])
except BaseException as e:
    print("UNCAUGHT",type(e).__name__,str(e)[:90],"| => process exit 1, traceback on stderr")
