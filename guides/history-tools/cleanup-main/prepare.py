# Extends the snapshot/commit-tree workflow used for the six smaller repositories.
import hashlib,json,os,pathlib,subprocess,textwrap
OUT=pathlib.Path(__file__).resolve().parent
plan=json.loads((OUT/'plan.json').read_text())
backups=json.loads((OUT/'backups.json').read_text())
CANDIDATE='refs/heads/cleanup/master-history-20260930'
ZERO='0'*40


def git(p,*args,input=None,env=None,binary=False):
 r=subprocess.run(['git','-C',str(p),*args],input=input,capture_output=True,text=not binary,env=env)
 if r.returncode:raise RuntimeError(str(args)+'\n'+str(r.stderr))
 return r.stdout if binary else r.stdout.strip()


manifest=[]
frontend_new=None
for before in backups:
 name=before['repo'];p=pathlib.Path(before['path']);old=before['old_master']
 assert git(p,'rev-parse','master')==old
 assert git(p,'symbolic-ref','HEAD')=='refs/heads/master'
 assert git(p,'status','--porcelain=v1')==''
 assert git(p,'rev-parse','--is-shallow-repository')=='false'
 assert not git(p,'for-each-ref','--format=%(refname)',CANDIDATE,'refs/replace')
 assert git(p,'for-each-ref','--format=%(refname) %(objectname)','refs/tags')==before['tags_before']
 index_before=git(p,'ls-files','--stage','-z',binary=True)
 authors={}
 for line in git(p,'log','--format=%H%x09%an%x09%ae%x09%aI',old).splitlines():
  sha,author,email,date=line.split('\t');authors[sha]=(author,email,date)
 entries=[];parent=None;seen=set()
 for group in plan[name]:
  endpoint=group['endpoint'];tree=group['source_tree']
  assert git(p,'rev-parse',endpoint+'^{tree}')==tree
  assert not seen.intersection(group['original_commits'])
  seen.update(group['original_commits'])
  transformation=None
  if name=='backend' and endpoint==old:
   assert frontend_new
   listing=git(p,'ls-tree','-z',tree,binary=True)
   old_link=group['frontend_gitlink'].split()[2]
   old_entry=f'160000 commit {old_link}\tfrontend'.encode()
   new_entry=f'160000 commit {frontend_new}\tfrontend'.encode()
   parts=listing.split(b'\0')
   assert parts.count(old_entry)==1
   parts[parts.index(old_entry)]=new_entry
   tree=git(p,'mktree','-z',input=b'\0'.join(parts),binary=True).decode().strip()
   assert git(p,'ls-tree','-r','-z',tree,binary=True).replace(new_entry,old_entry)==git(p,'ls-tree','-r','-z',group['source_tree'],binary=True)
   fp=pathlib.Path(backups[0]['path'])
   assert git(fp,'rev-parse',old_link+'^{tree}')==git(fp,'rev-parse',frontend_new+'^{tree}')
   transformation=dict(path='frontend',old_gitlink=old_link,new_gitlink=frontend_new,identical_frontend_tree=git(fp,'rev-parse',frontend_new+'^{tree}'))
  author,email,date=authors[endpoint]
  contributors=[]
  for sha in group['original_commits']:
   a,e,_=authors[sha]
   if (a,e)!=(author,email) and (a,e) not in contributors:contributors.append((a,e))
  message=group['title']+'\n\n'+textwrap.fill(group['body'],width=76)+'\n\nOriginal-snapshot: '+endpoint+'\n'
  for a,e in contributors:message+=f'Co-authored-by: {a} <{e}>\n'
  env=os.environ.copy();env.update(GIT_AUTHOR_NAME=author,GIT_AUTHOR_EMAIL=email,GIT_AUTHOR_DATE=date)
  args=['commit-tree',tree]+(['-p',parent] if parent else [])
  new=git(p,*args,input=message,env=env)
  assert git(p,'rev-parse',new+'^{tree}')==tree
  assert git(p,'show','-s','--format=%P',new)==(parent or '')
  if transformation is None:assert git(p,'diff','--raw',endpoint,new)==''
  entry={**group,'new':new,'tree':tree,'message':message,'transformation':transformation}
  entries.append(entry);parent=new
 assert seen==set(git(p,'rev-list',old).splitlines())
 assert git(p,'rev-list','--count',parent)==str(len(entries))
 assert git(p,'rev-list','--count','--merges',parent)=='0'
 git(p,'update-ref','-m','Prepare verified snapshot-preserving consolidated history',CANDIDATE,parent,ZERO)
 assert index_before==git(p,'ls-files','--stage','-z',binary=True)
 assert git(p,'status','--porcelain=v1')==''
 assert git(p,'rev-parse','master')==old
 assert git(p,'for-each-ref','--format=%(refname) %(objectname)','refs/tags')==before['tags_before']
 tag_map={}
 for tag in git(p,'tag','--list').splitlines():
  old_tag=git(p,'rev-parse',tag+'^{commit}')
  match=next(e for e in entries if e['endpoint']==old_tag)
  assert match['transformation'] is None
  assert git(p,'rev-parse',old_tag+'^{tree}')==match['tree']
  tag_map[tag]=dict(original_commit=old_tag,equivalent_new_commit=match['new'],identical_tree=match['tree'])
 row={**before,'candidate_ref':CANDIDATE,'new_master':parent,'new_count':len(entries),'groups':entries,'tag_equivalents':tag_map,'index_sha256_before':hashlib.sha256(index_before).hexdigest(),'status':'prepared_and_verified'}
 manifest.append(row)
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 if name=='frontend':frontend_new=parent
 print(f'{name}: {before["old_count"]} -> {len(entries)}; master unchanged; every snapshot and release boundary verified',flush=True)
 print('Candidate:',parent,flush=True)
 if name=='backend':print('Only final-tree metadata difference:',git(p,'diff','--raw','--no-abbrev',old,parent),flush=True)
