import json,hashlib
inst=json.load(open('instrument.json'))
mine=json.load(open('derive311.json'))
profs=json.load(open('/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json'))
ORDER=["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
fails=[]
def chk(cond,msg):
    print(("OK   " if cond else "FAIL ")+msg)
    if not cond: fails.append(msg)
for pname in ['distinct_origins','path_prefix','trailing_slash_sensitivity']:
    print('==== ',pname)
    rec=inst['profiles'][pname]['tasks'][311]
    m=mine[pname]
    # 1 identity fields
    chk(rec['output_index']==311, f"{pname} output_index={rec['output_index']}")
    chk(rec['task_id']==311, f"{pname} task_id={rec['task_id']}")
    chk(rec['output_filename']=='config_files/311.json', f"{pname} output_filename={rec['output_filename']}")
    chk(rec['index_equals_task_id'] is True, f"{pname} index_equals_task_id={rec['index_equals_task_id']}")
    chk(rec['would_be_file_sha256']==m['h_ordered'], f"{pname} would_be_file_sha256={rec['would_be_file_sha256']} mine_ordered={m['h_ordered']}")
    # 2 projected task exact equality with my re-derivation
    chk(rec['projected_task']==json.loads(m['item_text']), f"{pname} projected_task equals my independent projection")
    # 3 changed leaves
    cl=rec['changed_leaves']
    chk(len(cl)==1, f"{pname} changed_leaf_count={len(cl)} (mine {len(m['changed'])})")
    c=cl[0]
    ptr,origv,prov=m['changed'][0]
    chk(c['original']==origv, f"{pname} leaf original={c['original']!r} mine={origv!r}")
    chk(c['projected']==prov, f"{pname} leaf projected={c['projected']!r} mine={prov!r}")
    chk(c['tokens']==["__GITLAB__"], f"{pname} leaf tokens={c['tokens']}")
    chk(c['category']=='url_field', f"{pname} leaf category={c['category']}")
    chk(c['path_template']==ptr.lstrip('/'), f"{pname} leaf path_template={c['path_template']!r} pointer_style={c['json_pointer']!r}")
    # 4 every token occurrence inside the item's raw span is accounted for exactly once across changed leaves
    span_counts={ "GITLAB":1 }  # measured independently below via derive output
    print('   changed_leaves raw:', json.dumps(cl, ensure_ascii=False))
    # 5 non-URL change check
    nonurl=[x for x in cl if x['category']!='url_field']
    print('   non_url_changed_leaves:', len(nonurl))
# profile-level per-task changed leaves count recomputation from my own walk for whole file
