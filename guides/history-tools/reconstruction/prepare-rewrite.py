import subprocess,json,pathlib
P=pathlib.Path(__file__).parent;W=pathlib.Path('/home/USER/workspace');repos=json.loads((P/'commits.json').read_text());tasks={t['key']:t for t in json.loads((P/'prepared-tasks.json').read_text())};links=json.loads((P/'commit-task-links.json').read_text());mapping={};out=[]
def git(p,*args,data=None):return subprocess.check_output(['git','-C',str(p),*args],input=data)
for ri in [1,0,2,3,4,5,6,7,8]:
 r=repos[ri];p=W/r['path'];local={};tree_changes=[]
 assert git(p,'rev-parse','master').decode().strip()==r['head']
 assert not git(p,'status','--porcelain').strip()
 for c in r['commits']:
  raw=git(p,'cat-file','commit',c['sha']);header,body=raw.split(b'\n\n',1);headers=header.splitlines();newheaders=[];oldtree=c['tree'];newtree=oldtree
  if ri==0:
   entries=git(p,'ls-tree','-z',oldtree).split(b'\0');rebuilt=[]
   for e in entries:
    if not e:continue
    mode_type_sha,name=e.split(b'\t',1);mode,typ,sha=mode_type_sha.split()
    if name==b'frontend' and mode==b'160000' and sha.decode() in mapping.get('myscoutee-backend/frontend',{}):
     newsha=mapping['myscoutee-backend/frontend'][sha.decode()].encode();e=mode+b' '+typ+b' '+newsha+b'\t'+name
     assert git(W/'myscoutee-backend/frontend','rev-parse',sha.decode()+'^{tree}')==git(W/'myscoutee-backend/frontend','rev-parse',newsha.decode()+'^{tree}')
    rebuilt.append(e)
   newtree=git(p,'mktree','-z',data=b'\0'.join(rebuilt)+b'\0').decode().strip()
  for h in headers:
   assert not h.startswith(b'gpgsig '),'Signed commit requires explicit handling'
   if h.startswith(b'parent '):h=b'parent '+local[h.split()[1].decode()].encode()
   if h.startswith(b'tree '):h=b'tree '+newtree.encode()
   newheaders.append(h)
  ids=sorted({tasks[k]['provisional_id'] for k in links[c['sha']]},key=lambda x:int(x.split('-')[1]));prefix='['+', '.join(ids)+'] '
  lines=body.decode().splitlines();lines[0]=prefix+lines[0];newbody='\n'.join(lines).rstrip()+'\n\nTasks: '+', '.join('fssrepository/myscoutee-roadmap#'+i.split('-')[1] for i in ids)+'\n'
  newraw=b'\n'.join(newheaders)+b'\n\n'+newbody.encode();newsha=git(p,'hash-object','-t','commit','-w','--stdin',data=newraw).decode().strip();local[c['sha']]=newsha
  if oldtree!=newtree:
   changed=git(p,'diff-tree','--no-commit-id','--name-only','-r',oldtree,newtree).decode().splitlines();assert changed==['frontend'],changed;tree_changes.append({'old':c['sha'],'new':newsha,'path':'frontend','reason':'Same source tree, rewritten submodule commit ID'})
 mapping[r['path']]=local;out.append({'repo':r['path'],'old_head':r['head'],'new_head':local[r['head']],'commits':len(local),'submodule_pointer_changes':tree_changes})
 print(r['path'],len(local),'commit messages prepared; gitlink updates',len(tree_changes),flush=True)
(P/'rewrite-map.json').write_text(json.dumps(mapping,indent=2)+'\n');(P/'rewrite-plan.json').write_text(json.dumps(out,indent=2)+'\n')
