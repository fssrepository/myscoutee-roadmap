import pathlib,json,subprocess
P=pathlib.Path(__file__).parent;W=pathlib.Path('/home/USER/workspace');plan=json.loads((P/'rewrite-plan.json').read_text());state=json.loads((P/'publish-state.json').read_text());assert len(state['issues'])==109 and all(i.get('populated') for i in state['issues'].values())
def g(p,*args):return subprocess.check_output(['git','-C',str(p),*args],text=True).strip()
# Check all repositories before changing any local refs.
for r in plan:
 p=W/r['repo'];assert g(p,'rev-parse','master')==r['old_head'];assert not g(p,'status','--porcelain');remote=g(p,'ls-remote','origin','refs/heads/master').split()[0];assert remote==r['old_head'],(r['repo'],'remote changed')
for r in plan:
 p=W/r['repo'];g(p,'update-ref','refs/history-backup/before-task-ids-20261001',r['old_head']);g(p,'update-ref','refs/heads/master',r['new_head'],r['old_head']);g(p,'read-tree','HEAD');print('Applied locally:',r['repo'],r['new_head'][:12],flush=True)
(P/'rewrite-applied.json').write_text(json.dumps(plan,indent=2)+'\n')
