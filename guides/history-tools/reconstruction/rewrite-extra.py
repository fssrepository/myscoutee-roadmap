import json,pathlib,subprocess
P=pathlib.Path(__file__).parent;W=P.parent
R=json.loads((P/'commits.json').read_text());T={t['key']:t for t in json.loads((P/'prepared-tasks.json').read_text())};links=json.loads((P/'commit-task-links.json').read_text());S=json.loads((P/'portfolio-state.json').read_text());maps=json.loads((P/'rewrite-map.json').read_text());plan=json.loads((P/'rewrite-plan.json').read_text());pre=json.loads((P/'pre-rewrite-state.json').read_text())
def git(p,*args,data=None):return subprocess.check_output(['git','-C',str(p),*args],input=data)
for ri in [8,9,10]:
 r=R[ri];p=W/r['path'];current=git(p,'rev-parse','master').decode().strip();assert not git(p,'diff','--name-only').strip() and not git(p,'diff','--cached','--name-only').strip()
 expected=maps.get(r['path'],{}).get(r['head'],r['head']);assert current==expected
 if not any(x['repo']==r['path'] for x in pre):pre.append({'repo':r['path'],'head':r['head'],'branch':'master','status':'','tags':git(p,'show-ref','--tags').decode().strip()})
 local={}
 for c in r['commits']:
  raw=git(p,'cat-file','commit',c['sha']);head,body=raw.split(b'\n\n',1);headers=[]
  for h in head.splitlines():
   assert not h.startswith(b'gpgsig ')
   if h.startswith(b'parent '):h=b'parent '+local[h.split()[1].decode()].encode()
   headers.append(h)
  ks=links[c['sha']];ids=[T[k]['provisional_id'] for k in ks];lines=body.decode().splitlines();lines[0]='['+', '.join(ids)+'] '+lines[0]
  newbody='\n'.join(lines).rstrip()+'\n\nTasks: '+', '.join('fssrepository/myscoutee-roadmap#'+str(S['issues'][k]['number']) for k in ks)+'\n'
  new=git(p,'hash-object','-t','commit','-w','--stdin',data=b'\n'.join(headers)+b'\n\n'+newbody.encode()).decode().strip();local[c['sha']]=new
  assert git(p,'rev-parse',new+'^{tree}').decode().strip()==c['tree']
 git(p,'update-ref','refs/heads/master',local[r['head']],current);git(p,'read-tree','HEAD')
 maps[r['path']]=local;plan=[x for x in plan if x['repo']!=r['path']];plan.append({'repo':r['path'],'old_head':r['head'],'new_head':local[r['head']],'commits':len(local),'submodule_pointer_changes':[]})
 print('Metadata-only rewrite:',r['path'],len(local),'identical trees',flush=True)
(P/'rewrite-map.json').write_text(json.dumps(maps,indent=2)+'\n');(P/'rewrite-plan.json').write_text(json.dumps(plan,indent=2)+'\n');(P/'pre-rewrite-state.json').write_text(json.dumps(pre,indent=2)+'\n')
