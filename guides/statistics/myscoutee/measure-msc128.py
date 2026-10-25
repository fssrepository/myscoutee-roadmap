#!/usr/bin/env python3
"""Read-only MSC-128 accounting across its ten retained Codex sessions."""
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
parser.add_argument('--cutoff', default='2026-10-25T15:53:20.632Z')
args = parser.parse_args()
start = '2026-10-24T13:18:13.614Z'
selections = {key: [(start, args.cutoff)] for key in (
    '04509c60ee373d6b',  # Explicit MSC-127 -> MSC-128 boundary; shared fixes.
    'f80ad905fbf2537e',  # Released dependency/commit reconciliation.
    'c1219a885a1868fe',  # Shared frontend consolidation and corrections.
    '4030dd8bf812a9d0',  # Server, authentication and frontend follow-up.
    'b3d89618a787e272',  # Duplicate-language download investigation.
    '41616ec0f5d7200c',  # Startup JavaScript correction.
    '2bc8fda94f49db86',  # Profile, loading, localization and release work.
    '2d020897f1a566d0',  # Continuation, backend release and Netcup deployment.
    '58444100bdbdd8ed',  # Release-name corrections.
    '199178dbca52f3da',  # Template VMware, Pages and signed release.
)}
# Exclude the identifiable prior-task accounting blocks interleaved with the
# first implementation session. Boundaries follow recorded tool operations;
# attribution of mixed operations remains an estimate.
accounting_gaps = [
    ('13:23:10.977', '13:25:19.999'),
    ('13:28:39.472', '13:31:29.253'),
    ('13:31:46.251', '13:34:30.952'),
    ('13:37:45.069', '13:39:08.421'),
    ('13:39:53.044', '13:41:30.924'),
    ('13:49:24.184', '13:49:39.338'),
    ('13:50:03.505', '13:50:38.444'),
    ('13:51:58.778', '13:56:41.614'),
    ('13:57:16.275', '14:00:06.734'),
    ('14:00:30.045', '14:02:19.734'),
    ('14:03:54.347', '14:04:27.320'),
    ('14:08:53.140', '14:09:49.871'),
]
windows = []
cursor = start
for begin, end in accounting_gaps:
    begin, end = (f'2026-10-24T{value}Z' for value in (begin, end))
    windows.append((cursor, begin))
    cursor = end
windows.append((cursor, args.cutoff))
selections['04509c60ee373d6b'] = windows
result = usage.extract(
    'MSC-128', selections, args.cutoff, started='2026-10-24',
    include_archived_segments=True, allow_unpriced_models=True,
    note='Ten retained root sessions and their archived segments, including '
    'continuations, shared component/backend/frontend fixes, investigations, '
    'failed and reverted attempts, tests, packaging, VMware, Pages, source '
    'consolidation, both signed 1.5.0 releases and Netcup deployment. '
    'Identifiable prior-task accounting blocks in the mixed first session are '
    'excluded; mixed-operation attribution is estimated. Earlier MSC-127 work '
    'ends before the explicit MSC-128 boundary. Unique response IDs are '
    'deduplicated globally; root active intervals are unioned and prior '
    'allocated overlap subtracted. Tool/build/network waits count; idle gaps '
    'do not. Cached input is inside input and reasoning inside output. '
    'Shared/template work is allocated once. The failed continuation with no '
    'token records receives no invented usage. This final accounting session '
    'and unrelated mathematical work are excluded. Existing frozen rates and '
    'the October 24 supplement are reused; API equivalent is not billing. '
    'Account usage is a separate overlapping measurement, never added.'
)
print(json.dumps(result, indent=2))
