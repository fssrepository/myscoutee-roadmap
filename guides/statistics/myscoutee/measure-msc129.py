#!/usr/bin/env python3
"""Read-only MSC-129 accounting through the Pages and viewer closeout."""
import argparse
import importlib.util
import json
import pathlib
import sys

sys.dont_write_bytecode = True
root = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('usage', root / 'measure-msc119.py')
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cutoff', default='2026-10-26T15:05:40Z')
args = parser.parse_args()
selections = {
    '6c9c555fa3936331': [('2026-10-25T16:21:25.922Z', '2026-10-26T14:19:19Z')],
    '8eb8fc5d3c82977c': [('2026-10-25T18:33:59.419Z', args.cutoff)],
    'e20c0f8a89fc098c': [('2026-10-26T01:21:36.848Z', args.cutoff)],
    '43a7e978d3500e43': [('2026-10-26T02:57:27.082Z', args.cutoff)],
    '071e3b7a4aab9410': [('2026-10-26T14:20:40Z', args.cutoff)],
}
result = usage.extract(
    'MSC-129', selections, args.cutoff, started='2026-10-25',
    include_archived_segments=True, allow_unpriced_models=True,
    note='Five retained root sessions: the CI/CD implementation and qualification, '
    'the related Git/runner learning guide, two GitLab access/terminal support '
    'sessions, and the Pages/viewer closeout continuation. Includes failed/reverted attempts, repeated corrections, registry '
    'and release exercises, backend/template target work, accepted template '
    'monolith/KVM/VMware reviews, Git consolidation, the three PDF manuals, '
    'permanent gh-pages/docs publication for both frontends and e-kozig, and shared document-viewer loading alignment '
    'through the cutoff. Separate GitHub budget advice and mathematical work are '
    'excluded. Unique response IDs are deduplicated globally; root active intervals '
    'are unioned and earlier task allocations subtracted. Tool/build/network waits '
    'count; idle gaps do not. Shared repository/template effort is counted once. '
    'Cached input is inside input and reasoning inside output. Final accounting '
    'and publication after cutoff are excluded. Existing frozen rates are reused; '
    'API equivalent is not billing. Account usage is a separate overlapping '
    'measurement, never added to task usage.'
)
print(json.dumps(result, indent=2))
