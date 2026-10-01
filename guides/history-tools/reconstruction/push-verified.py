import pathlib,json,subprocess
P=pathlib.Path(__file__).parent;W=P.parent;leases=json.loads((P/'final-push-leases.json').read_text());rows=json.loads((P/'backup-commits.json').read_text());donefile=P/'final-push-results.json';done=json.loads(donefile.read_text()) if donefile.exists() else {}
def git(repo,*args):return subprocess.check_output(['git','-C',str(W/repo),*args],stderr=subprocess.STDOUT,text=True).strip()
repos=[r['repo'] for r in rows]+['myscoutee-roadmap']
for n,repo in enumerate(repos,1):
 head=git(repo,'rev-parse','HEAD');assert not git(repo,'status','--porcelain')
 if done.get(repo,{}).get('head')==head:continue
 remote=git(repo,'ls-remote','origin','refs/heads/master').split()[0];assert remote in [leases[repo],head],(repo,'Remote changed unexpectedly',remote)
 print('Push',n,'/',len(repos),repo,flush=True)
 if remote!=head:print(git(repo,'push','--force-with-lease=refs/heads/master:'+leases[repo],'origin','HEAD:refs/heads/master'),flush=True)
 assert git(repo,'ls-remote','origin','refs/heads/master').split()[0]==head
 assert git(repo,'rev-list','--left-right','--count','master...origin/master')=='0\t0'
 done[repo]={'head':head,'verified_remote':True,'ahead':0,'behind':0};donefile.write_text(json.dumps(done,indent=2)+'\n')
 print('Synchronized',repo,head[:12],flush=True)
print('All 12 repositories synchronized',flush=True)
