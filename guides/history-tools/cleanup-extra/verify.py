import hashlib,json,pathlib,subprocess,os
R=pathlib.Path('/home/USER/workspace');O=pathlib.Path(__file__).resolve().parent

def g(p,*args):
 q=subprocess.run(['git','-C',str(p),*args],capture_output=True,text=True)
 if q.returncode:raise RuntimeError(q.stderr)
 return q.stdout.strip()

def refs(s,reverse=False):
 return dict((line.split()[::-1] if reverse else line.split()) for line in s.splitlines())

migration=json.loads((O/'archive-migration.json').read_text())
for row in migration:
 p=pathlib.Path(row['path'])
 remote=refs(g(p,'ls-remote','origin','refs/heads/master','refs/heads/backup/*','refs/tags/archive/*'),True)
 assert remote['refs/heads/master']==row['master_unchanged']==g(p,'rev-parse','master')
 for c in row['changes']:
  assert c['old_branch'] not in remote
  assert not g(p,'for-each-ref','--format=%(objectname)',c['old_branch'])
  assert remote[c['archive_tag']]==c['commit']==g(p,'rev-parse',c['archive_tag'])
 print(row['repo']+': remote/local recovery tags verified; cleanup backup branches absent',flush=True)
for source in ['small-repos','main-repos']:
 for row in json.loads((R/('history-cleanup-20260930-'+source)/'manifest.json').read_text()):
  p=pathlib.Path(row.get('path',R/row['repo']))
  remote=refs(g(p,'ls-remote','origin','refs/tags/*'),True)
  for tag,sha in refs(row['tags_before']).items():assert remote[tag]==sha==g(p,'rev-parse',tag)

rows=json.loads((O/'manifest.json').read_text())
summary=['History cleanup: additional fssrepository repositories','', 'No tracked file content or mode changed. Original Git trees reused.', 'Original histories retained in local complete bundles and remote archive tags.', 'All original release tags across the previously processed repositories unchanged.', 'Task-created backup branches converted to archive tags (9 refs in 8 repositories).','']
for row in rows:
 p=R/row['repo'];old=row['old_master'];new=row['new_master'];backup=row['backup_ref']
 assert row['status']=='published_and_verified'
 assert g(p,'symbolic-ref','HEAD')=='refs/heads/master'
 assert g(p,'rev-parse','HEAD')==g(p,'rev-parse','origin/master')==new
 assert g(p,'status','--porcelain=v1')==''
 assert g(p,'rev-list','--left-right','--count','master...origin/master')=='0\t0'
 assert g(p,'rev-parse',old+'^{tree}')==g(p,'rev-parse',new+'^{tree}')
 assert g(p,'diff','--raw',old,new)==''
 assert int(g(p,'rev-list','--count',new))==row['new_count']
 originals=[]
 for group in row['groups']:
  assert group['tree']==g(p,'rev-parse',group['new']+'^{tree}')==g(p,'rev-parse',group['original_endpoint']+'^{tree}')
  originals.extend(group['original_commits'])
 assert originals==g(p,'rev-list','--reverse',old).splitlines()
 remote=refs(g(p,'ls-remote','origin','refs/heads/*','refs/tags/*'),True)
 before=refs((O/(row['repo']+'-refs-before.txt')).read_text(),True)
 expected={k:v for k,v in before.items() if k.startswith(('refs/heads/','refs/tags/'))}
 expected['refs/heads/master']=new;expected[backup]=old
 assert remote==expected
 local_tags=refs(g(p,'for-each-ref','--format=%(refname) %(objectname)','refs/tags'))
 expected_tags=refs(row['tags_before']);expected_tags[backup]=old
 assert local_tags==expected_tags
 h=hashlib.sha256()
 with open(row['bundle'],'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 assert h.hexdigest()==row['bundle_sha256']
 g(p,'bundle','verify',row['bundle'])
 print(row['repo']+': all tree, ref, commit-coverage and bundle checks passed; checking object integrity',flush=True)
 fsck=g(p,'fsck','--full','--no-dangling')
 (O/(row['repo']+'-fsck.txt')).write_text(fsck+'\n')
 head=pathlib.Path(g(p,'rev-parse','--absolute-git-dir'))/'HEAD';os.utime(head,None)
 summary += [f"{row['repo']}: {row['old_count']} -> {row['new_count']} commits",f'Local path: {p}',f'Original master: {old}',f'New local and remote master: {new}',f'Recovery tag: {backup}',f'Bundle: {row["bundle"]}',f'Bundle SHA256: {h.hexdigest()}','Verification: exact endpoint/final trees, full old-commit coverage, remote refs, clean 0/0 worktree, bundle integrity, git fsck --full passed.','']
 row['final_verification']='passed'
 print(row['repo']+': final verification passed',flush=True)
(O/'manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
(O/'RESULTS.txt').write_text('\n'.join(summary)+'\n')
