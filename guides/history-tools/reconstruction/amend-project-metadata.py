import pathlib,json,subprocess,concurrent.futures,hashlib
P=pathlib.Path(__file__).parent;W=P.parent;rows=json.loads((P/'backup-commits.json').read_text());repos=[r['repo'] for r in rows]+['myscoutee-roadmap']
def git(repo,*args):return subprocess.check_output(['git','-C',str(W/repo),*args],text=True).strip()
def inspect(repo):
 head=git(repo,'rev-parse','HEAD');remote=git(repo,'ls-remote','origin','refs/heads/master').split()[0];assert head==remote,(repo,'Concurrent remote change');assert not git(repo,'diff','--cached','--name-only');return repo,head
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:leases=dict(pool.map(inspect,repos))
(P/'final-push-leases.json').write_text(json.dumps(leases,indent=2)+'\n')
for repo in repos:
 changed=git(repo,'diff','--name-only').splitlines();assert all(x.startswith('guides/project-history/') or (repo=='myscoutee-backend' and x=='frontend') or (repo=='myscoutee-roadmap' and x=='README.md') for x in changed),(repo,changed)
 git(repo,'add','--','guides/project-history')
 if repo=='myscoutee-backend':git(repo,'add','--','frontend')
 if repo=='myscoutee-roadmap':git(repo,'add','--','README.md')
 git(repo,'diff','--cached','--check');git(repo,'commit','--amend','--no-edit');head=git(repo,'rev-parse','HEAD');assert not git(repo,'status','--porcelain');assert git(repo,'show','-s','--format=%s').startswith(('[MSC-110]','[OLD-5]','[EKO-15]','[MATH-17]'))
 for r in rows:
  if r['repo']==repo:r['backup_head']=head
 print('Updated task-linked snapshot commit:',repo,head[:12],flush=True)
(P/'backup-commits.json').write_text(json.dumps(rows,indent=2)+'\n')
for name in json.loads((P/'portfolio-backup-folders.json').read_text()):
 d=pathlib.Path(name);root=pathlib.Path(subprocess.check_output(['git','-C',str(d),'rev-parse','--show-toplevel'],text=True).strip())
 for line in (d/'SHA256SUMS').read_text().splitlines():
  digest,name=line.split(None,1);data=subprocess.check_output(['git','-C',str(root),'show','HEAD:'+str((d/name.strip()).relative_to(root))]);assert hashlib.sha256(data).hexdigest()==digest
print('All committed snapshots verified from Git objects',flush=True)
