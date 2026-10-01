import json
from pathlib import Path
import subprocess

ROOT = Path('/home/USER/workspace')
OUT = Path(__file__).resolve().parent
manifest_path = OUT / 'manifest.json'
report = json.loads(manifest_path.read_text())


def save():
    manifest_path.write_text(json.dumps(report, indent=2) + '\n')


def git(repo, *args):
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True)
    with (OUT / 'publication.log').open('a') as log:
        log.write(f'{repo.name}: git {args!r}\n{result.stdout}{result.stderr}\n')
    if result.returncode:
        raise RuntimeError(f'{repo.name}: git {args}: {result.stderr}')
    return result.stdout.strip()


for row in report:
    assert row['status'] == 'prepared_and_verified'
    repo = ROOT / row['repo']
    old, new = row['old_master'], row['new_master']
    backup = row['backup_ref']
    assert git(repo, 'symbolic-ref', 'HEAD') == 'refs/heads/master'
    assert git(repo, 'status', '--porcelain=v1') == ''
    assert git(repo, 'rev-parse', 'master') == old
    assert git(repo, 'rev-parse', backup) == old
    assert git(repo, 'rev-parse', row['candidate_ref']) == new
    assert git(repo, 'rev-parse', old + '^{tree}') == git(repo, 'rev-parse', new + '^{tree}')
    tags_before = git(repo, 'ls-remote', 'origin', 'refs/tags/*')
    assert git(repo, 'ls-remote', 'origin', 'refs/heads/master').split()[0] == old
    assert not git(repo, 'ls-remote', 'origin', backup)
    args = ['push', '--atomic', f'--force-with-lease=refs/heads/master:{old}',
            f'--force-with-lease={backup}:', 'origin', f'{backup}:{backup}',
            f'{new}:refs/heads/master']
    git(repo, args[0], '--dry-run', *args[1:])
    row['status'] = 'publishing'
    row['remote_tags_before'] = tags_before
    save()
    git(repo, *args)
    row['status'] = 'remote_published'
    save()
    refs = dict(line.split()[::-1] for line in git(repo, 'ls-remote', 'origin', 'refs/heads/master', backup).splitlines())
    assert refs == {'refs/heads/master': new, backup: old}
    assert git(repo, 'ls-remote', 'origin', 'refs/tags/*') == tags_before
    git(repo, 'update-ref', '-m', 'Activate verified snapshot-preserving history consolidation', 'refs/heads/master', new, old)
    assert git(repo, 'status', '--porcelain=v1') == ''
    assert git(repo, 'rev-parse', 'HEAD') == new
    assert git(repo, 'rev-parse', 'origin/master') == new
    assert git(repo, 'for-each-ref', '--format=%(refname) %(objectname)', 'refs/tags') == row['tags_before']
    row['status'] = 'published_and_verified'
    save()
    print(f"{row['repo']}: local and remote master {new[:8]}, remote backup {old[:8]}, clean worktree and unchanged tags", flush=True)
