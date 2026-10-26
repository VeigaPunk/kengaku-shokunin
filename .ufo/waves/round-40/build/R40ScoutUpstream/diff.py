import sqlite3,os,shutil,sys,tempfile,json,hashlib
C='/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round40/tb2-db-wal-recovery/'
wal=open(C+'main.db-wal.encrypted','rb').read()
def mk(d,key=None,walbytes=None):
    os.makedirs(d); shutil.copy(C+'main.db',d+'/main.db')
    w=walbytes if walbytes is not None else (bytes(b^key for b in wal) if key is not None else wal)
    open(d+'/main.db-wal','wb').write(w)
def rows(uri):
    c=sqlite3.connect(uri,uri=True); r=c.execute('select id,name,value from items order by id').fetchall(); c.close(); return r
def h(r): return hashlib.sha256(json.dumps(r).encode()).hexdigest()[:12]
out=[]
S=sys.argv[1]
print('lib',sqlite3.sqlite_version)
for label,key in [('enc-none',None),('xor42',0x42),('xor41',0x41),('xor00',0)]:
    for mode in ['ro','rw']:
        d=f'{S}/{label}-{mode}'; mk(d,key)
        try: r=rows(f'file:{d}/main.db?mode={mode}'); res=f'n={len(r)} h={h(r)}'
        except Exception as e: res='ERR '+type(e).__name__+':'+str(e)
        files=sorted(f for f in os.listdir(d)); sz={f:os.path.getsize(d+'/'+f) for f in files}
        print(label,mode,res,sz)
# truncated/odd WAL: header-only 32 bytes decrypted, partial frame
d=f'{S}/xor42-trunc'; full=bytes(b^0x42 for b in wal); mk(d,walbytes=full[:32+24+4096+100]); 
r=rows(f'file:{d}/main.db'); print('xor42-trunc-rw',len(r),h(r),sorted(os.listdir(d)))
# export with float id
d=f'{S}/xor42-types'; mk(d,0x42); c=sqlite3.connect(d+'/main.db'); print('types',c.execute('select id,typeof(id),typeof(name),typeof(value) from items').fetchall()[:3]); print(c.execute('pragma journal_mode').fetchall(), c.execute('pragma page_size').fetchall()); c.close()
