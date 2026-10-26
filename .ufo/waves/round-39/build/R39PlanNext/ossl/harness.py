import sys, importlib.util, traceback
spec = importlib.util.spec_from_file_location("g", "/tests/test_outputs.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for n in ["test_directory_structure","test_key_file","test_certificate_file","test_combined_pem_file","test_verification_file","test_python_verification_script"]:
    try:
        getattr(m, n)(); print("T", n, "PASS")
    except BaseException as e:
        print("T", n, "FAIL", type(e).__name__, str(e).replace("\n"," ")[:90])
