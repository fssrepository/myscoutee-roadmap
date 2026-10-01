import collections,json,pathlib,subprocess
OUT=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('/home/USER/workspace/myscoutee-backend')
plan={}
review=[]
for name in ['frontend','backend']:
 p=ROOT/('frontend' if name=='frontend' else '.')
 def g(*a): return subprocess.check_output(['git','-C',str(p),*a],text=True).strip()
 rows=json.loads((OUT/f'{name}-inventory.json').read_text())
 bysha={r['sha']:r for r in rows}
 mainline=g('rev-list','--first-parent','--reverse','master').splitlines()
 position={s:i for i,s in enumerate(mainline)}
 groups=[];parent=None;seen=set();review.append(name.upper())
 for line in (OUT/f'{name}-phases.txt').read_text().splitlines():
  spec,title,body=line.split('|',2)
  if spec.startswith('2026-'):
   choices=[s for s in mainline if bysha[s]['date']<=spec]
   end=choices[-1]
  else:end=g('rev-parse',spec+'^{commit}')
  assert end in position and (parent is None or position[end]>position[parent]),(name,spec,title)
  originals=g('rev-list','--reverse',end,*(['--not',parent] if parent else [])).splitlines()
  assert not seen.intersection(originals)
  seen.update(originals)
  files=collections.Counter(f for s in originals for f in bysha[s]['files'])
  group=dict(endpoint=end,title=title,body=body,original_commits=originals,source_tree=bysha[end]['tree'],start_date=bysha[originals[0]]['date'],end_date=bysha[end]['date'])
  if name=='backend':group['frontend_gitlink']=g('ls-tree',end,'--','frontend')
  groups.append(group)
  review += [f"{len(groups):02d}. {title}",f"    {originals[0][:10]} .. {end[:10]} / {len(originals)} commits / {group['start_date']} .. {group['end_date']}", '    Areas: '+', '.join(f for f,c in files.most_common(8))]
  parent=end
 assert seen==set(bysha),(name,len(seen),len(bysha))
 endpoints={x['endpoint'] for x in groups}
 for tag in g('tag','--list').splitlines():assert g('rev-parse',tag+'^{commit}') in endpoints,(name,tag)
 plan[name]=groups
 review.append('')
 print(name,len(rows),'->',len(groups))
(OUT/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
(OUT/'PLAN.txt').write_text('\n'.join(review)+'\n')
