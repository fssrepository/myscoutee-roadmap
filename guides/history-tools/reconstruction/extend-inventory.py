import json,pathlib,subprocess
P=pathlib.Path(__file__).parent;W=P.parent
repos=json.loads((P/'commits.json').read_text());oldmap={g['new']:g for r in json.loads((W/'history-cleanup-20260930-extra-repos/manifest.json').read_text()) for g in r['groups']}
def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args],text=True).strip()
for name in ['e-kozig','millennium-math-problems']:
 if any(r['path']==name for r in repos):continue
 p=W/name;rows=[]
 for sha in git(p,'rev-list','--reverse','master').splitlines():
  f=git(p,'show','-s','--format=%H%x00%aI%x00%cI%x00%s%x00%b',sha).split('\0',4);original=oldmap.get(sha,{}).get('original_commits',[sha]);dates=[git(p,'show','-s','--format=%aI',c) for c in original]
  rows.append(dict(sha=sha,author_date=f[1],commit_date=f[2],title=f[3],body=f[4],original_commits=original,original_start=min(dates),original_end=max(dates),files=git(p,'diff-tree','--root','--no-commit-id','--name-only','-r',sha).splitlines(),tree=git(p,'rev-parse',sha+'^{tree}')))
 repos.append(dict(path=name,remote=git(p,'remote','get-url','origin'),head=git(p,'rev-parse','master'),commits=rows))
 print(name,len(rows))
(P/'commits.json').write_text(json.dumps(repos,indent=2)+'\n')
