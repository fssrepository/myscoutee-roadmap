import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path('/home/USER/workspace')
OUT = Path(__file__).resolve().parent
BACKUP = 'refs/heads/backup/master-before-history-cleanup-20260930'
CANDIDATE = 'refs/heads/cleanup/master-history-20260930'
ZERO = '0' * 40


def git(repo, *args, input=None, env=None):
    result = subprocess.run(['git', '-C', str(repo), *args], input=input,
                            capture_output=True, text=True, env=env)
    if result.returncode:
        raise RuntimeError(f'{repo.name}: git {args}: {result.stderr}')
    return result.stdout.strip()


plan = json.loads((OUT / 'plan.json').read_text())
report = []
for name, groups in plan.items():
    repo = ROOT / name
    assert git(repo, 'symbolic-ref', 'HEAD') == 'refs/heads/master'
    assert git(repo, 'status', '--porcelain=v1') == ''
    assert git(repo, 'rev-parse', '--is-shallow-repository') == 'false'
    assert not git(repo, 'for-each-ref', '--format=%(refname)', 'refs/replace')
    assert git(repo, 'rev-list', '--count', '--merges', 'master') == '0'
    assert not git(repo, 'for-each-ref', '--format=%(refname)', BACKUP, CANDIDATE)
    old = git(repo, 'rev-parse', 'master')
    remote = git(repo, 'ls-remote', 'origin', 'refs/heads/master').split()[0]
    assert old == remote == git(repo, 'rev-parse', 'origin/master')
    commits = git(repo, 'rev-list', '--reverse', old).splitlines()
    endpoints = [git(repo, 'rev-parse', group[0]) for group in groups]
    assert endpoints[-1] == old
    indices = [commits.index(endpoint) for endpoint in endpoints]
    assert indices == sorted(set(indices))
    tags = git(repo, 'for-each-ref', '--format=%(refname) %(objectname)', 'refs/tags')
    for tag in git(repo, 'tag', '--list').splitlines():
        assert git(repo, 'rev-parse', f'{tag}^{{commit}}') in endpoints, tag
    assert not any(line.startswith('160000 ') for line in git(repo, 'ls-tree', '-r', old).splitlines())
    bundle = OUT / f'{name}-before.bundle'
    assert not bundle.exists()
    refs_before = git(repo, 'show-ref')
    (OUT / f'{name}-refs-before.txt').write_text(refs_before + '\n')
    (OUT / f'{name}-log-before.txt').write_text(git(repo, 'log', '--reverse', '--format=fuller', old) + '\n')
    git(repo, 'bundle', 'create', str(bundle), '--all')
    git(repo, 'bundle', 'verify', str(bundle))
    git(repo, 'update-ref', '-m', 'Preserve master before history consolidation', BACKUP, old, ZERO)
    entries = []
    parent = None
    start = 0
    for endpoint, end, (_, title, body) in zip(endpoints, indices, groups):
        originals = commits[start:end + 1]
        assert originals
        tree = git(repo, 'rev-parse', f'{endpoint}^{{tree}}')
        author = git(repo, 'show', '-s', '--format=%an%n%ae%n%aI', endpoint).splitlines()
        env = os.environ.copy()
        env.update(GIT_AUTHOR_NAME=author[0], GIT_AUTHOR_EMAIL=author[1], GIT_AUTHOR_DATE=author[2])
        message = f'{title}\n\n{body}\n\nOriginal-snapshot: {endpoint}\n'
        args = ['commit-tree', tree]
        if parent:
            args.extend(['-p', parent])
        new = git(repo, *args, input=message, env=env)
        assert git(repo, 'rev-parse', f'{new}^{{tree}}') == tree
        assert git(repo, 'diff', '--raw', endpoint, new) == ''
        actual_parents = git(repo, 'show', '-s', '--format=%P', new)
        assert actual_parents == (parent or '')
        entries.append({'title': title, 'new': new, 'tree': tree, 'original_endpoint': endpoint,
                        'original_commits': originals, 'message': message})
        parent = new
        start = end + 1
    assert start == len(commits)
    git(repo, 'update-ref', '-m', 'Prepare snapshot-preserving history consolidation', CANDIDATE, parent, ZERO)
    assert git(repo, 'rev-parse', f'{old}^{{tree}}') == git(repo, 'rev-parse', f'{parent}^{{tree}}')
    assert git(repo, 'rev-list', '--count', parent) == str(len(groups))
    assert git(repo, 'rev-parse', 'master') == old
    assert git(repo, 'status', '--porcelain=v1') == ''
    assert git(repo, 'for-each-ref', '--format=%(refname) %(objectname)', 'refs/tags') == tags
    row = {'repo': name, 'old_master': old, 'new_master': parent, 'backup_ref': BACKUP,
           'candidate_ref': CANDIDATE, 'bundle': str(bundle),
           'bundle_sha256': hashlib.sha256(bundle.read_bytes()).hexdigest(),
           'old_count': len(commits), 'new_count': len(groups), 'tags_before': tags,
           'groups': entries, 'status': 'prepared_and_verified'}
    report.append(row)
    (OUT / 'manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'{name}: {len(commits)} -> {len(groups)}, every endpoint tree identical; backup verified', flush=True)
    for entry in entries:
        print(f"  {len(entry['original_commits']):2} commits -> {entry['new'][:8]} {entry['title']}", flush=True)
