import json,pathlib,subprocess
P=pathlib.Path(__file__).parent;W=P.parent;R=json.loads((P/'commits.json').read_text());maps=json.loads((P/'rewrite-map.json').read_text());pre={r['repo']:r for r in json.loads((P/'pre-rewrite-state.json').read_text())};out=[]
def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args],text=True).strip()
for ri in [1,2,3,4,5,6,7,8,9,10,0]:
 r=R[ri];p=W/r['path'];expected=maps[r['path']][r['head']]
 assert git(p,'rev-parse','master')==expected,(r['path'],'Unexpected master change')
 assert not git(p,'diff','--cached','--name-only'),(r['path'],'Unrelated staged changes')
 tracked=git(p,'diff','--name-only').splitlines();assert not tracked or (ri==0 and tracked==['frontend']),(r['path'],tracked)
 assert git(p,'show-ref','--tags')==pre[r['path']]['tags'],(r['path'],'Tag changed')
 git(p,'add','--','guides/project-history')
 if ri==0:git(p,'add','--','frontend')
 staged=git(p,'diff','--cached','--name-only').splitlines();assert staged and all(x.startswith('guides/project-history/') or (ri==0 and x=='frontend') for x in staged)
 git(p,'diff','--cached','--check')
 title='[MSC-108] docs: preserve restorable Project history' if ri not in [8,9,10] else 'docs: preserve restorable Project tasks and historical evidence'
 git(p,'commit','-m',title)
 head=git(p,'rev-parse','HEAD');changed=git(p,'diff','--name-only',r['head'],head).splitlines();assert all(x.startswith('guides/project-history/') or (ri==0 and x=='frontend') for x in changed),(r['path'],changed)
 assert git(p,'rev-list','--count','master')==str(len(r['commits'])+1)
 assert not git(p,'status','--porcelain')
 out.append({'repo':r['path'],'remote_original_head':r['head'],'task_head':expected,'backup_head':head,'new_files':len(staged)})
 (P/'backup-commits.json').write_text(json.dumps(out,indent=2)+'\n')
 print('Committed',r['path'],head[:12],len(staged),'authorized paths; source content preserved',flush=True)
p=W/'myscoutee-roadmap';assert not git(p,'diff','--cached','--name-only')
git(p,'add','--','README.md','guides/project-history','tasks.csv','tasks.json','account-daily-usage.json');git(p,'diff','--cached','--check');git(p,'commit','-m','Separate project histories and preserve complete restorable records')
print('Central tracker',git(p,'rev-parse','HEAD'),flush=True)
