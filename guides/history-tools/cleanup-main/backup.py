import hashlib,json,pathlib,subprocess
OUT=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('/home/USER/workspace/myscoutee-backend')
backup='refs/heads/backup/master-before-history-cleanup-20260930'
rows=[]
for name,p in [('frontend',ROOT/'frontend'),('backend',ROOT)]:
 def g(*a):
  r=subprocess.run(['git','-C',str(p),*a],text=True,capture_output=True)
  if r.returncode: raise RuntimeError(str(a)+'\n'+r.stderr)
  return r.stdout.strip()
 assert g('status','--porcelain=v1')==''
 assert g('rev-parse','--is-shallow-repository')=='false'
 assert not g('for-each-ref','--format=%(refname)',backup,'refs/heads/cleanup/master-history-20260930','refs/replace')
 old=g('rev-parse','master')
 assert g('ls-remote','origin','refs/heads/master').split()[0]==old
 row=dict(repo=name,path=str(p),old_master=old,backup_ref=backup,tags_before=g('for-each-ref','--format=%(refname) %(objectname)','refs/tags'),remote_tags_before=g('ls-remote','origin','refs/tags/*'),refs_before=g('show-ref'),old_count=int(g('rev-list','--count',old)))
 (OUT/f'{name}-refs-before.txt').write_text(row['refs_before']+'\n')
 bundle=OUT/f'{name}-before.bundle'
 assert not bundle.exists()
 print(name+': creating complete bundle',flush=True)
 g('-c','pack.threads=2','-c','pack.windowMemory=64m','bundle','create',str(bundle),'--all')
 verified=g('bundle','verify',str(bundle))
 row['bundle']=str(bundle)
 h=hashlib.sha256()
 with bundle.open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 row['bundle_sha256']=h.hexdigest()
 g('update-ref','-m','Preserve master before history consolidation',backup,old,'0'*40)
 rows.append(row)
 (OUT/'backups.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(name+': complete bundle verified and backup branch created',flush=True)
