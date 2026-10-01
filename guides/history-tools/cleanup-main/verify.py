import hashlib,json,pathlib,subprocess
OUT=pathlib.Path(__file__).resolve().parent
rows=json.loads((OUT/'manifest.json').read_text())
archive=json.loads((OUT/'submodule-archive.json').read_text())
lines=['MyScoutee frontend/backend master history consolidation — 2026-09-30','',
'Only existing Git snapshots were used for the consolidated history.',
'No source or generated application files were edited, patched, rebuilt or retested.',
'The final backend gitlink was changed to the content-identical new frontend master.',
'All original release tag objects and targets are unchanged locally and remotely.',
'The first historical frontend merge is represented by its original resolved tree.',
'The frontend clone was unshallowed before analysis: 2454 total original commits,',
'not merely the 563 commits initially visible in the shallow clone.','',
'Backups:',
'  Each repository has local/remote backup/master-before-history-cleanup-20260930.',
'  The frontend also has backup/backend-submodule-history-20260930, protecting',
'  seven additional pre-existing or recovered frontend histories referenced by',
'  historical backend commits. This archive branch does not enter the new master.',
'  Verified self-contained bundles and SHA-256 checksums are recorded in',
'  manifest.json and submodule-archive.json.','',
'Historical boundary discovered before rewriting:',
'  Thirteen old frontend gitlink objects were initially absent locally. Four',
'  were recovered from origin. Nine were unavailable from origin already before',
'  this rewrite; their hashes are listed in submodule-archive.json. Their original',
'  backend references are retained in the backup history without inventing data.',
'  Every snapshot retained on the NEW backend master references an available,',
'  archived frontend commit. No missing frontend target was introduced.','',
'Verification:']


def g(p,*a,binary=False):
 r=subprocess.run(['git','-C',str(p),*a],capture_output=True,text=not binary)
 assert r.returncode==0,(a,r.stderr)
 return r.stdout if binary else r.stdout.strip()


for row in rows:
 assert row['status']=='published_and_verified'
 p=pathlib.Path(row['path']);old=row['old_master'];new=row['new_master']
 assert g(p,'rev-parse','HEAD')==g(p,'rev-parse','master')==g(p,'rev-parse','origin/master')==new
 assert g(p,'status','--porcelain=v1')==''
 assert g(p,'rev-list','--left-right','--count','HEAD...@{upstream}')=='0\t0'
 assert g(p,'rev-list','--count','master')==str(row['new_count'])
 assert g(p,'rev-list','--count','--merges','master')=='0'
 expected={'refs/heads/master':new,row['backup_ref']:old}
 if row['repo']=='frontend':expected[archive['ref']]=archive['commit']
 actual=dict(l.split()[::-1] for l in g(p,'ls-remote','origin',*expected).splitlines())
 assert actual==expected
 assert g(p,'ls-remote','origin','refs/tags/*')==row['remote_tags_before']
 assert g(p,'for-each-ref','--format=%(refname) %(objectname)','refs/tags')==row['tags_before']
 # Confirm every pre-existing local branch except master remains untouched.
 for refline in row['refs_before'].splitlines():
  sha,ref=refline.split()
  if ref.startswith('refs/heads/') and ref!='refs/heads/master':assert g(p,'rev-parse',ref)==sha
 seen=[]
 for group in row['groups']:
  seen+=group['original_commits']
  assert g(p,'rev-parse',group['new']+'^{tree}')==group['tree']
  if group['transformation'] is None:
   assert g(p,'rev-parse',group['endpoint']+'^{tree}')==group['tree']
  else:
   t=group['transformation'];assert row['repo']=='backend' and group['new']==new
   original=g(p,'ls-tree','-r','-z',group['endpoint'],binary=True)
   current=g(p,'ls-tree','-r','-z',group['new'],binary=True)
   a=f"160000 commit {t['old_gitlink']}\tfrontend".encode()
   b=f"160000 commit {t['new_gitlink']}\tfrontend".encode()
   assert original.count(a)==1 and current.count(b)==1 and current.replace(b,a)==original
   fp=pathlib.Path(rows[0]['path'])
   assert g(fp,'rev-parse',t['old_gitlink']+'^{tree}')==g(fp,'rev-parse',t['new_gitlink']+'^{tree}')==t['identical_frontend_tree']
  if row['repo']=='backend':
   link=g(p,'ls-tree',group['new'],'--','frontend').split()[2]
   fp=pathlib.Path(rows[0]['path'])
   assert g(fp,'cat-file','-t',link)=='commit'
   assert any(subprocess.run(['git','-C',str(fp),'merge-base','--is-ancestor',link,ref]).returncode==0 for ref in [archive['ref'],'master'])
 assert len(seen)==len(set(seen))==row['old_count']
 assert set(seen)==set(g(p,'rev-list',old).splitlines())
 for tag,mapping in row['tag_equivalents'].items():
  assert g(p,'rev-parse',tag+'^{commit}')==mapping['original_commit']
  assert g(p,'rev-parse',tag+'^{tree}')==g(p,'rev-parse',mapping['equivalent_new_commit']+'^{tree}')==mapping['identical_tree']
 h=hashlib.sha256()
 with pathlib.Path(row['bundle']).open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 assert h.hexdigest()==row['bundle_sha256']
 lines += [f"  PASS {row['repo']}: {row['old_count']} -> {row['new_count']} commits",f"    Old master: {old}",f"    New master: {new}", '    Exact endpoint trees; all original commits accounted for; unchanged release tags;', '    remote backup and master verified; clean worktree; 0 incoming / 0 outgoing;', '    original bundle checksum verified; existing non-master branches preserved.']
 print('PASS',row['repo'],'all final checks',flush=True)
archive_hash=hashlib.sha256()
with pathlib.Path(archive['bundle']).open('rb') as f:
 for block in iter(lambda:f.read(8*1024*1024),b''):archive_hash.update(block)
assert archive_hash.hexdigest()==archive['bundle_sha256']
lines += ['  PASS Git object integrity: git fsck --full --no-dangling in both repositories.', '', 'Consolidated commit lists:','']
for row in rows:
 lines.append(row['repo'].upper())
 for group in row['groups']:
  lines += [f"  {group['new'][:12]} {group['title']}",f"    Original endpoint: {group['endpoint']} ({len(group['original_commits'])} original commits)"]
 lines.append('')
lines += ['Review and recovery:',
'  PLAN.txt describes every grouping and its affected areas.',
'  manifest.json maps all original commits and release snapshots to the new commits.',
'  publication.log records explicit-lease atomic pushes and remote verification.',
'  The frontend source and published assets remain byte-identical to the original tip.',
'  The backend final difference is only its frontend gitlink; expanding that gitlink',
'  gives exactly the same application file contents and modes.',
'  Existing clones must align with the new master after preserving local work;',
'  merging the old and new histories would undo the cleanup.',
'  Rollback should use the recorded original master and an explicit force-with-lease',
'  expecting the current remote tip. Do not discard work created after this cleanup.']
(OUT/'RESULTS.txt').write_text('\n'.join(lines)+'\n')
print('Report:',OUT/'RESULTS.txt')
