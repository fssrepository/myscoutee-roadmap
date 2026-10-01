import json,pathlib,subprocess,concurrent.futures
P=pathlib.Path(__file__).parent;W=P.parent;rows=json.loads((P/'backup-commits.json').read_text());statefile=P/'push-results.json';done=json.loads(statefile.read_text()) if statefile.exists() else {}
def git(repo,*args):return subprocess.check_output(['git','-C',str(W/repo),*args],stderr=subprocess.STDOUT,text=True).strip()
def inspect(r):
 remote=git(r['repo'],'ls-remote','origin','refs/heads/master').split()[0]
 assert remote in [r['remote_original_head'],r['backup_head']],(r['repo'],'Remote changed; lease cannot safely replace',remote)
 assert git(r['repo'],'rev-parse','HEAD')==r['backup_head'];assert not git(r['repo'],'status','--porcelain')
 return r['repo'],remote
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for name,head in pool.map(inspect,rows):print('Preflight',name,head[:12],flush=True)
for n,r in enumerate(rows,1):
 repo=r['repo']
 if repo in done:continue
 print('Push',n,'/',len(rows),repo,flush=True)
 result=git(repo,'push','--force-with-lease=refs/heads/master:'+r['remote_original_head'],'origin','HEAD:refs/heads/master')
 print(result,flush=True)
 remote=git(repo,'ls-remote','origin','refs/heads/master').split()[0];assert remote==r['backup_head']
 assert git(repo,'rev-list','--left-right','--count','master...origin/master')=='0\t0'
 done[repo]={'head':remote,'verified_remote':True};statefile.write_text(json.dumps(done,indent=2)+'\n')
print(git('myscoutee-roadmap','push','origin','master'),flush=True)
assert git('myscoutee-roadmap','rev-list','--left-right','--count','master...origin/master')=='0\t0'
print('All masters synchronized',flush=True)
