import collections,json,pathlib,subprocess,sys
OUT=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('/home/USER/workspace/myscoutee-backend')
for name in sys.argv[1:]:
 p=ROOT/('frontend' if name=='frontend' else '.')
 raw=subprocess.check_output(['git','-C',str(p),'log','--reverse','--format=%x1e%H%x1f%ad%x1f%s%x1f%T%x1f%P','--date=short','--name-only','--no-renames','master']).decode('utf-8','replace')
 rows=[]
 for rec in raw.split('\x1e')[1:]:
  head,*paths=rec.strip().splitlines()
  sha,date,subject,tree,parents=head.split('\x1f')
  rows.append(dict(sha=sha,date=date,subject=subject,tree=tree,parents=parents.split(),files=[f for f in paths if f]))
 (OUT/f'{name}-inventory.json').write_text(json.dumps(rows,indent=2)+'\n')
 days=collections.defaultdict(list)
 for i,row in enumerate(rows): days[row['date']].append((i,row))
 lines=[]
 for day,items in days.items():
  fs=collections.Counter(f for _,r in items for f in r['files'] if f!='frontend' and not f.startswith(('docs/','guides/story/')))
  stems=collections.Counter(pathlib.Path(f).name for _,r in items for f in r['files'] if f not in ['frontend','README.md'] and not f.endswith(('.json','.png','.jpg','.webp','.xlsx','.pdf','.mp4','.svg')) and not f.startswith('docs/'))
  subs=collections.Counter(r['subject'] for _,r in items)
  lines.extend([f"{day} [{items[0][0]}..{items[-1][0]}] n={len(items)} end={items[-1][1]['sha'][:10]}", ' SUBJECTS '+ '; '.join(f'{s} ({c})' for s,c in subs.most_common(14)), ' FILES '+ '; '.join(f'{s} ({c})' for s,c in stems.most_common(12))])
 (OUT/f'{name}-days.txt').write_text('\n'.join(lines)+'\n')
 print(name,len(rows),'commits,',len(days),'days,',sum(len(r['parents'])>1 for r in rows),'merges',flush=True)
