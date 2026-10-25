import json
def run(src, order_vals, order):
    p=src
    for k in order:
        p=p.replace(k, order_vals[k])
    return p
src='[{"task_id": 0, "start_url": "__GITLAB__"}]'
print("W-A earlier->later (GITLAB value contains later token WIKIPEDIA):")
print("  ", run(src, {"__GITLAB__":"http://gitlab.invalid:10101/__WIKIPEDIA__","__WIKIPEDIA__":"http://wikipedia.invalid:10105"},
   ["__GITLAB__","__REDDIT__","__SHOPPING__","__SHOPPING_ADMIN__","__WIKIPEDIA__","__MAP__"]))
print("W-B later->earlier (WIKIPEDIA value contains earlier token GITLAB):")
print("  ", run(src, {"__GITLAB__":"http://gitlab.invalid:10101","__WIKIPEDIA__":"http://wikipedia.invalid:10105/__GITLAB__"},
   ["__GITLAB__","__REDDIT__","__SHOPPING__","__SHOPPING_ADMIN__","__WIKIPEDIA__","__MAP__"]))
print("W-C SHOPPING vs SHOPPING_ADMIN non-overlap check:")
print("   '__SHOPPING__' in '__SHOPPING_ADMIN__' ->", "__SHOPPING__" in "__SHOPPING_ADMIN__")
print("   '__SHOPPING_ADMIN__' in '__SHOPPING__' ->", "__SHOPPING_ADMIN__" in "__SHOPPING__")
print("W-D SHOPPING_ADMIN value containing __SHOPPING__ (earlier token, already consumed):")
print("  ", run(src, {"__SHOPPING__":"http://shopping.invalid:10103","__SHOPPING_ADMIN__":"http://shopping-admin.invalid:10104/__SHOPPING__"},
   ["__GITLAB__","__REDDIT__","__SHOPPING__","__SHOPPING_ADMIN__","__WIKIPEDIA__","__MAP__"]))
print("W-E SHOPPING value containing __SHOPPING_ADMIN__ (later token, WILL cascade):")
print("  ", run(src, {"__SHOPPING__":"http://shopping.invalid:10103/__SHOPPING_ADMIN__","__SHOPPING_ADMIN__":"http://shopping-admin.invalid:10104"},
   ["__GITLAB__","__REDDIT__","__SHOPPING__","__SHOPPING_ADMIN__","__WIKIPEDIA__","__MAP__"]))
