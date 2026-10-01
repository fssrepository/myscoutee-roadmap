# Extends the explicit-lease atomic publication used for the smaller repositories.
import hashlib,json,os,pathlib,subprocess
OUT=pathlib.Path(__file__).resolve().parent
mp=OUT/'manifest.json'
rows=json.loads(mp.read_text())
archive=json.loads((OUT/'submodule-archive.json').read_text())


def save():mp.write_text(json.dumps(rows,indent=2)+'\n')


def git(p,*args,binary=False):
 r=subprocess.run(['git','-C',str(p),*args],capture_output=True,text=not binary)
 with (OUT/'publication.log').open('a') as f:
  f.write(f'{p}: git {args!r}\n')
  if not binary:f.write(r.stdout+r.stderr+'\n')
 if r.returncode:raise RuntimeError(f'{p}: {args}: {r.stderr}')
 return r.stdout if binary else r.stdout.strip()


# Complete dry runs and local/remote state checks for both repos before publication.
commands={}
for row in rows:
 assert row['status']=='prepared_and_verified'
 p=pathlib.Path(row['path']);old=row['old_master'];new=row['new_master']
 assert git(p,'symbolic-ref','HEAD')=='refs/heads/master'
 assert git(p,'status','--porcelain=v1')==''
 assert git(p,'rev-parse','HEAD')==old
 assert git(p,'rev-parse',row['candidate_ref'])==new
 assert git(p,'rev-parse',row['backup_ref'])==old
 assert hashlib.sha256(git(p,'ls-files','--stage','-z',binary=True)).hexdigest()==row['index_sha256_before']
 assert git(p,'ls-remote','origin','refs/heads/master').split()[0]==old
 assert git(p,'ls-remote','origin','refs/tags/*')==row['remote_tags_before']
 refs=[row['backup_ref']]
 if row['repo']=='frontend':
  refs.append(archive['ref'])
  assert git(p,'rev-parse',archive['ref'])==archive['commit']
 for ref in refs:assert not git(p,'ls-remote','origin',ref)
 args=['push','--atomic',f'--force-with-lease=refs/heads/master:{old}']
 args += [f'--force-with-lease={ref}:' for ref in refs]
 args += ['origin']+[f'{ref}:{ref}' for ref in refs]+[f'{new}:refs/heads/master']
 git(p,args[0],'--dry-run',*args[1:]);commands[row['repo']]=args
 print(row['repo']+': guarded atomic push dry run passed',flush=True)

# Frontend backups and new master must be available before publishing backend links.
for row in rows:
 p=pathlib.Path(row['path']);old=row['old_master'];new=row['new_master']
 assert git(p,'status','--porcelain=v1')==''
 assert git(p,'rev-parse','HEAD')==old
 row['status']='publishing';save()
 git(p,*commands[row['repo']])
 row['status']='remote_published';save()
 expected={'refs/heads/master':new,row['backup_ref']:old}
 if row['repo']=='frontend':expected[archive['ref']]=archive['commit']
 actual=dict(line.split()[::-1] for line in git(p,'ls-remote','origin',*expected).splitlines())
 assert actual==expected,(actual,expected)
 assert git(p,'ls-remote','origin','refs/tags/*')==row['remote_tags_before']
 print(row['repo']+': remote master and backups verified; release tags unchanged',flush=True)

# Move local refs and the parent gitlink index without checking out application files.
frontend,backend=rows
assert frontend['repo']=='frontend' and backend['repo']=='backend'
for row in rows:
 p=pathlib.Path(row['path'])
 assert hashlib.sha256(git(p,'ls-files','--stage','-z',binary=True)).hexdigest()==row['index_sha256_before']
 assert git(p,'diff','--name-only','--ignore-submodules=all')==''
 git(p,'update-ref','-m','Activate verified consolidated master history','refs/heads/master',row['new_master'],row['old_master'])
git(pathlib.Path(backend['path']),'update-index','--cacheinfo',f"160000,{frontend['new_master']},frontend")
for row in rows:
 p=pathlib.Path(row['path'])
 assert git(p,'rev-parse','HEAD')==row['new_master']==git(p,'rev-parse','origin/master')
 assert git(p,'status','--porcelain=v1')==''
 assert git(p,'rev-list','--left-right','--count','HEAD...@{upstream}')=='0\t0'
 assert git(p,'for-each-ref','--format=%(refname) %(objectname)','refs/tags')==row['tags_before']
 # Notify HEAD-file watchers without changing its symbolic-reference contents.
 head=pathlib.Path(git(p,'rev-parse','--absolute-git-dir'))/'HEAD'
 contents=head.read_bytes();os.utime(head,None);assert head.read_bytes()==contents
 row['status']='published_and_verified';save()
 print(f"{row['repo']}: local master synchronized; clean worktree; 0 incoming / 0 outgoing",flush=True)
