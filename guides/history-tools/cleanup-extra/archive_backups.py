import json,pathlib,subprocess
ROOT=pathlib.Path('/home/USER/workspace');OUT=pathlib.Path(__file__).resolve().parent
sources=[ROOT/'history-cleanup-20260930-small-repos',ROOT/'history-cleanup-20260930-main-repos']
report=[]

def g(p,*args,input=None):
 r=subprocess.run(['git','-C',str(p),*args],capture_output=True,text=True,input=input)
 with (OUT/'archive-migration.log').open('a') as f:f.write(f'{p}: git {args!r}\n{r.stdout}{r.stderr}\n')
 if r.returncode:raise RuntimeError(r.stderr)
 return r.stdout.strip()

for source in sources:
 manifest=json.loads((source/'manifest.json').read_text())
 for row in manifest:
  p=pathlib.Path(row.get('path',str(ROOT/row['repo'])))
  refs=[(row['backup_ref'],row['old_master'])]
  if row['repo']=='frontend':
   archive=json.loads((source/'submodule-archive.json').read_text())
   refs.append((archive['ref'],archive['commit']))
  assert pathlib.Path(row['bundle']).is_file()
  local_master=g(p,'rev-parse','master')
  before=dict(line.split()[::-1] for line in g(p,'ls-remote','origin','refs/heads/master','refs/tags/*',*[x[0] for x in refs]).splitlines())
  tag_before=g(p,'for-each-ref','--format=%(refname) %(objectname)','refs/tags')
  changes=[]
  for branch,sha in refs:
   tag=branch.replace('refs/heads/backup/','refs/tags/archive/',1)
   assert before.get(branch)==g(p,'rev-parse',branch)==sha
   assert tag not in before
   assert not g(p,'for-each-ref','--format=%(refname)',tag)
   assert 'branch '+branch not in g(p,'worktree','list','--porcelain')
   changes.append(dict(old_branch=branch,archive_tag=tag,commit=sha))
  args=['push','--atomic']
  for c in changes:args += [f"--force-with-lease={c['old_branch']}:{c['commit']}",f"--force-with-lease={c['archive_tag']}:"]
  args+=['origin']
  for c in changes:args += [f"{c['commit']}:{c['archive_tag']}",':'+c['old_branch']]
  g(p,args[0],'--dry-run',*args[1:]);g(p,*args)
  after=dict(line.split()[::-1] for line in g(p,'ls-remote','origin','refs/heads/master','refs/tags/*',*[x[0] for x in refs]).splitlines())
  expected={k:v for k,v in before.items() if k not in [c['old_branch'] for c in changes]}
  expected.update({c['archive_tag']:c['commit'] for c in changes})
  assert after==expected
  txn='start\n'
  for c in changes:txn+=f"create {c['archive_tag']} {c['commit']}\ndelete {c['old_branch']} {c['commit']}\n"
  txn+='prepare\ncommit\n'
  g(p,'update-ref','--stdin',input=txn)
  assert g(p,'rev-parse','master')==local_master
  for line in tag_before.splitlines():
   ref,sha=line.split();assert g(p,'rev-parse',ref)==sha
  row['archive_migration']=changes
  row['current_backup_ref']=changes[0]['archive_tag']
  report.append(dict(repo=row['repo'],path=str(p),changes=changes,master_unchanged=local_master,status='converted_and_verified'))
  (OUT/'archive-migration.json').write_text(json.dumps(report,indent=2)+'\n')
  (source/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
  print(f"{row['repo']}: {len(changes)} backup branch(es) converted to archive tags; master and original tags unchanged",flush=True)
 notice=('CURRENT RECOVERY REFERENCES: backup branches created by the history cleanup\n'
         'have been converted to archive/* tags, pointing to the exact same commits.\n'
         'See /home/USER/workspace/history-cleanup-20260930-extra-repos/archive-migration.json.\n'
         'The original release tags and masters are unchanged by this conversion.\n'
         'The evidence below records the original publication, before that conversion.\n\n')
 results=source/'RESULTS.txt'
 results.write_text(notice+results.read_text())
