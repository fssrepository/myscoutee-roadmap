#!/usr/bin/env python3
"""Read-only MSC-130 measurement across the retained laboratory sessions."""
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
parser.add_argument('--cutoff', default='2026-10-28T04:07:42Z')
args = parser.parse_args()
selections = {
    '9f52a21a1b678434': [('2026-10-27T16:01:22Z', '2026-10-27T18:42:40Z')],
    'b53ebba18ef40bcf': [('2026-10-27T16:04:48Z', '2026-10-27T23:14:45Z')],
    '224bd35bade8b0ce': [('2026-10-27T16:07:14Z', '2026-10-28T01:50:45Z')],
    'eacf49d7a3122868': [('2026-10-27T17:31:37Z', '2026-10-27T23:50:47Z')],
    'ec54d9b3213677ec': [('2026-10-27T17:52:33Z', '2026-10-27T19:31:21Z')],
    'dc3325ee794f002c': [('2026-10-27T19:36:24Z', '2026-10-27T19:40:47Z')],
    '36fe09488a29180c': [('2026-10-27T23:19:24Z', '2026-10-27T23:31:14Z')],
    '87735e6182029ed2': [('2026-10-27T23:24:35Z', '2026-10-27T23:55:09Z')],
    'd58232a850239eb4': [('2026-10-27T23:51:21Z', '2026-10-27T23:52:23Z')],
    'd7d47dd452f3cbbf': [('2026-10-27T23:57:00Z', '2026-10-27T23:58:07Z')],
    'a0ae8a6af61f33bc': [('2026-10-28T00:01:36Z', '2026-10-28T00:22:31Z')],
    '240c9ad14bb86bbb': [('2026-10-28T01:52:45Z', '2026-10-28T01:57:37Z')],
    '0849002038137dea': [('2026-10-28T02:06:18Z', '2026-10-28T04:07:43Z')],
    '81946ddbb7888815': [('2026-10-28T03:45:53Z', '2026-10-28T04:00:20Z')],
}
result = usage.extract(
    'MSC-130', selections, args.cutoff, started='2026-10-27',
    include_archived_segments=True,
    note='Fourteen retained root sessions cover the Elastic, Big Data, security, '
    'infrastructure, architecture and 2FA laboratories, follow-up standards and '
    'Git/documentation work through the cutoff. Independent AI Pilot, e-kozig, '
    'earlier CI/CD and Kafka lookup work are excluded. Unique response IDs are '
    'deduplicated; active intervals are unioned, with earlier task allocation '
    'subtracted. Shared repository effort is counted once. Tool/network/build '
    'waits count; idle gaps and later closure/accounting work do not. Cached '
    'input is inside input and reasoning inside output. The account heatmap is '
    'an overlapping, separately measured view; no separate ChatGPT conversation '
    'token total is available. API equivalent is an estimate, not billing.'
)
print(json.dumps(result, indent=2))
