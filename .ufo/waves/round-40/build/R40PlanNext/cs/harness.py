import importlib.util
spec = importlib.util.spec_from_file_location("g", "/tests/test_outputs.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for n in [x for x in dir(m) if x.startswith("test_")]:
    try:
        getattr(m, n)(); print("T", n, "PASS")
    except BaseException as e:
        print("T", n, "FAIL", type(e).__name__, str(e).replace("\n"," ")[:80])
