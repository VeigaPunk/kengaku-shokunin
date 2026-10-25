import ast, json
SRC="/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py"
src=open(SRC).read()
tree=ast.parse(src)
seq=[]
for n in ast.walk(tree):
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="replace":
        if isinstance(n.func.value,ast.Name) and n.func.value.id=="raw" and n.args and isinstance(n.args[0],ast.Constant):
            seq.append((n.lineno,n.args[0].value,ast.unparse(n.args[1])))
seq.sort()
print("AST-extracted replace sequence (lineno, token, value_expr):")
for s in seq: print("  ",s)
print("count:",len(seq))
# enumerate index
for n in ast.walk(tree):
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="enumerate":
        print("enumerate call at line",n.lineno,ast.unparse(n))
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="dump":
        print("json.dump call at line",n.lineno,ast.unparse(n))
# wildcard import
for n in ast.walk(tree):
    if isinstance(n,ast.ImportFrom):
        print("ImportFrom:",ast.unparse(n), "names:", [a.name for a in n.names])
