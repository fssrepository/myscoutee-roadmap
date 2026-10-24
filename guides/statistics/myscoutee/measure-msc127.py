#!/usr/bin/env python3
"""Read-only MSC-127 accounting using the existing response-ID extractor."""
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
parser.add_argument('--cutoff', default='2026-10-24T13:18:13.613Z')
args = parser.parse_args()
selections = {
    # Continue after the measured MSC-126 delivery and its accounting turn.
    'f63318a2f5045701': [('2026-10-22T00:04:32.436Z', args.cutoff)],
    # Landing diagnostics explicitly assigned to MSC-127, including its investigation.
    '089cd9b25514ac92': [('2026-10-21T13:57:24.919Z', args.cutoff)],
    '31c3abbf525997e1': [('2026-10-22T01:14:47.143Z', args.cutoff)],
    'c763f7e5264d61e3': [('2026-10-22T11:37:32.243Z', args.cutoff)],
    'f221ac66f4c2294d': [('2026-10-22T12:35:49.672Z', args.cutoff)],
    '3dbe842d68bdb026': [('2026-10-22T12:42:05.719Z', args.cutoff)],
    'a5bc5fafed2e6c50': [('2026-10-22T13:01:22.575Z', args.cutoff)],
    'dced7db99333d410': [('2026-10-22T14:10:59.888Z', args.cutoff)],
    '1a976a0c28a6dbf2': [('2026-10-22T22:48:46.502Z', args.cutoff)],
    'b234ec500bc2c5d9': [('2026-10-23T14:29:45.600Z', args.cutoff)],
    'a7811f6269f21004': [('2026-10-23T14:51:01.598Z', args.cutoff)],
    # MyScoutee work in a mixed Sonar session; exclude the initial e-kozig work
    # and its later isolated Pages publication request.
    'ea7cd597fad068ed': [
        ('2026-10-24T00:07:41.899Z', '2026-10-24T01:57:13.776Z'),
        ('2026-10-24T02:00:43.820Z', args.cutoff),
    ],
    '02edba2f03802d78': [('2026-10-23T23:44:11.415Z', args.cutoff)],
    'bde9d41b2c906e04': [('2026-10-24T00:30:28.103Z', args.cutoff)],
    '44221dc82e41a8a2': [('2026-10-24T01:41:27.451Z', args.cutoff)],
    'cace1c5ab0782330': [('2026-10-24T02:49:18.776Z', args.cutoff)],
    '04509c60ee373d6b': [('2026-10-24T11:17:17.555Z', args.cutoff)],
}
result = usage.extract(
    'MSC-127', selections, args.cutoff, started='2026-10-21',
    include_archived_segments=True, allow_unpriced_models=True,
    note='Measured unique response usage across 17 selected root histories; task '
    'attribution follows explicit requests and the consolidated MSC-127 delivery. '
    'Includes landing diagnostics, Lighthouse follow-up, shared modules, Sonar, '
    'packaging, documentation/QA reorganization, releases, runtime checks, '
    'corrections and reverted attempts. Mixed Sonar windows exclude initial '
    'e-kozig work and its isolated Pages publication. Excludes separate advertising '
    'analysis, Higgsfield lookup, prior MSC-126 accounting, and MSC-128 work from '
    '2026-10-24T13:18:13.614Z onward. Root active intervals are unioned, tool waits '
    'included, idle gaps excluded, and previously allocated task time subtracted. '
    'Task attribution of mixed windows is an estimate. Cached input is inside '
    'input and reasoning inside output. Shared repository work is allocated once. '
    'Account totals and ChatGPT usage are separate overlapping views, never added '
    'to this measurement. The missing gpt-6.1-sol rate uses the documented October 24 supplement. Closure '
    'transfers outstanding qualification to MSC-128 and does not assert it passed.'
)
print(json.dumps(result, indent=2))
