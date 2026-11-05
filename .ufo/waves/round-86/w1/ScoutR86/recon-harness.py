import ast, json, runpy, traceback
from pathlib import Path
path = "/tests/test_outputs.py"
names = [node.name for node in ast.parse(Path(path).read_bytes()).body
         if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
module = runpy.run_path(path)
results = []
for name in names:
    try:
        module[name]()
    except BaseException as error:
        tb = traceback.extract_tb(error.__traceback__)
        last = [f for f in tb if f.filename.endswith("test_outputs.py")]
        loc = f"{last[-1].lineno}:{last[-1].line}" if last else "?"
        results.append([name, type(error).__name__, loc])
    else:
        results.append([name, "P", ""])
print(json.dumps({"tests": results}))
