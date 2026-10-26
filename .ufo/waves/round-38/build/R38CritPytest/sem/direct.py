import importlib.util, sys
spec = importlib.util.spec_from_file_location("m", "test_baseexc.py")
mod = importlib.util.module_from_spec(spec); sys.modules["m"] = mod; spec.loader.exec_module(mod)
for name in ("test_a", "test_b", "test_c", "test_d"):
    try:
        getattr(mod, name)(); print("TEST " + name + " P")
    except AssertionError:
        print("TEST " + name + " F")
    except Exception as e:
        print("TEST " + name + " F error=" + type(e).__name__)
