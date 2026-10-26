import importlib.util, sys
spec = importlib.util.spec_from_file_location("g", "/tests/test_outputs.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for run in (1, 2):
    try:
        m.test_fibonacci_polyglot(); print("GRADE", run, "PASS")
    except BaseException as e:
        print("GRADE", run, "FAIL", type(e).__name__, str(e).replace("\n", " ")[:110])
