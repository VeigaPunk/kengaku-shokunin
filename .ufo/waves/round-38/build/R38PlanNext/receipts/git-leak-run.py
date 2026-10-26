import importlib.util,sys,traceback
spec=importlib.util.spec_from_file_location("t","/tests/test_outputs.py");m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
f=0
for n in sorted(x for x in dir(m) if x.startswith("test_")):
    try: getattr(m,n)();print(n,"PASS")
    except BaseException as e: f+=1;print(n,"FAIL",type(e).__name__,str(e).splitlines()[0][:90] if str(e) else "")
print("fails=%d"%f);sys.exit(1 if f else 0)
