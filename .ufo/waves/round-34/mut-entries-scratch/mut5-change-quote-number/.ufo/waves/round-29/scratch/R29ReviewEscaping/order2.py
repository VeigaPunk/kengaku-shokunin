ORDER=["__GITLAB__","__REDDIT__","__SHOPPING__","__SHOPPING_ADMIN__","__WIKIPEDIA__","__MAP__"]
def run(src, vals):
    p=src
    for k in ORDER:
        if k in vals: p=p.replace(k, vals[k])
    return p
src='[{"task_id": 0, "start_url": "__GITLAB__"}]'
W=[("W-A earlier token value contains LATER token __WIKIPEDIA__ (cascade expected)",
    {"__GITLAB__":"http://gitlab.invalid:10101/__WIKIPEDIA__","__WIKIPEDIA__":"http://wikipedia.invalid:10105"}),
   ("W-B later token value contains EARLIER token __GITLAB__ (no cascade expected)",
    {"__GITLAB__":"http://gitlab.invalid:10101","__WIKIPEDIA__":"http://wikipedia.invalid:10105/__GITLAB__"}),
   ("W-C __SHOPPING__ value contains LATER __SHOPPING_ADMIN__ (cascade expected)",
    {"__SHOPPING__":"http://shopping.invalid:10103/__SHOPPING_ADMIN__","__SHOPPING_ADMIN__":"http://shopping-admin.invalid:10104"}),
   ("W-D __SHOPPING_ADMIN__ value contains EARLIER __SHOPPING__ (no cascade expected)",
    {"__SHOPPING__":"http://shopping.invalid:10103","__SHOPPING_ADMIN__":"http://shopping-admin.invalid:10104/__SHOPPING__"})]
for label,vals in W:
    out=run(src,vals)
    print(label); print("   projected:",out)
    try: print("   parsed:",json.loads(out))
    except Exception as e: print("   parse error:",e)
print()
print("non-overlap: '__SHOPPING__' in '__SHOPPING_ADMIN__' ->", "__SHOPPING__" in "__SHOPPING_ADMIN__")
print("non-overlap: '__SHOPPING_ADMIN__' in '__SHOPPING__' ->", "__SHOPPING_ADMIN__" in "__SHOPPING__")
print("non-overlap: '__GITLAB__' vs '__REDDIT__' vs '__MAP__' vs '__WIKIPEDIA__' mutually:",
      all(a not in b for a in ["__GITLAB__","__REDDIT__","__MAP__","__WIKIPEDIA__"] for b in ["__GITLAB__","__REDDIT__","__MAP__","__WIKIPEDIA__"] if a!=b))
