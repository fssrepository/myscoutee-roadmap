import pathlib,json,subprocess,concurrent.futures
P=pathlib.Path(__file__).parent;W=P.parent;rows=json.loads((P/'backup-commits.json').read_text());S=json.loads((P/'portfolio-state.json').read_text());pre={r['repo']:r for r in json.loads((P/'pre-rewrite-state.json').read_text())}
def git(repo,*args,data=None):return subprocess.check_output(['git','-C',str(W/repo),*args],input=data,text=True).strip()
def inspect(r):
 remote=git(r['repo'],'ls-remote','origin','refs/heads/master').split()[0];assert remote in [r['remote_original_head'],r['backup_head']],(r['repo'],remote)
 return r['repo'],remote
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:leases=dict(pool.map(inspect,rows))
leases['myscoutee-roadmap']=git('myscoutee-roadmap','ls-remote','origin','refs/heads/master').split()[0]
assert leases['myscoutee-roadmap']=='c5e44445a007554901b246653837021bbda64b44' or git('myscoutee-roadmap','rev-parse',leases['myscoutee-roadmap'])==leases['myscoutee-roadmap']
(P/'final-push-leases.json').write_text(json.dumps(leases,indent=2)+'\n')
for r in rows:
 repo=r['repo'];assert git(repo,'rev-parse','HEAD')==r['backup_head'];assert not git(repo,'diff','--cached','--name-only')
 changed=git(repo,'diff','--name-only').splitlines();assert all(x.startswith('guides/project-history/') or (repo=='myscoutee-backend' and x=='frontend') for x in changed),(repo,changed)
 git(repo,'add','--','guides/project-history')
 if repo=='millennium-math-problems':git(repo,'add','-f','--','guides/project-history/tasks.csv')
 if repo=='myscoutee-backend':git(repo,'add','--','frontend')
 key='OLDMAINT' if repo=='myscoutee-old' else 'EKOMAINT' if repo=='e-kozig' else 'MATHMAINT' if repo=='millennium-math-problems' else 'MAINT';tid={'MAINT':'MSC-110','OLDMAINT':'OLD-5','EKOMAINT':'EKO-15','MATHMAINT':'MATH-17'}[key]
 git(repo,'diff','--cached','--check');git(repo,'commit','--amend','-m','['+tid+'] docs: preserve restorable Project history and effort records','-m','Task: '+S['issues'][key]['url'])
 r['backup_head']=git(repo,'rev-parse','HEAD');assert not git(repo,'status','--porcelain');assert git(repo,'show-ref','--tags')==pre[repo]['tags']
 changed=git(repo,'diff','--name-only',r['remote_original_head'],'HEAD').splitlines();assert all(x.startswith('guides/project-history/') or (repo=='myscoutee-backend' and x=='frontend') for x in changed)
 print('Final commit',repo,r['backup_head'][:12],tid,flush=True)
 (P/'backup-commits.json').write_text(json.dumps(rows,indent=2)+'\n')
repo='myscoutee-roadmap';git(repo,'add','--','README.md','guides/project-history');git(repo,'diff','--cached','--check');git(repo,'commit','--amend','-m','[MSC-110] docs: preserve separate Project budgets and restorable records','-m','Task: '+S['issues']['MAINT']['url'])
# Both commits in this newly created tracker belong to the administration task.
head=git(repo,'rev-parse','HEAD');parent=git(repo,'rev-parse','HEAD^');raw=git(repo,'cat-file','commit',parent);header,body=raw.split('\n\n',1);assert 'parent ' not in header
newparent=git(repo,'hash-object','-t','commit','-w','--stdin',data=header+'\n\n[MSC-110] '+body.rstrip()+'\n\nTask: '+S['issues']['MAINT']['url']+'\n')
raw=git(repo,'cat-file','commit',head);header,body=raw.split('\n\n',1);header=header.replace('parent '+parent,'parent '+newparent);newhead=git(repo,'hash-object','-t','commit','-w','--stdin',data=header+'\n\n'+body+'\n');git(repo,'update-ref','refs/heads/master',newhead,head);git(repo,'read-tree','HEAD');assert not git(repo,'status','--porcelain');print('Final tracker',newhead[:12],flush=True)
