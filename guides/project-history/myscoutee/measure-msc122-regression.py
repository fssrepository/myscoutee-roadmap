#!/usr/bin/env python3
"""Read-only incremental MSC-122 regression usage; emits aggregates only."""
import argparse
import importlib.util
import pathlib
import sys
import json

sys.dont_write_bytecode = True
root = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('usage', root / 'measure-msc119.py')
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cutoff', required=True)
args = parser.parse_args()
result = usage.extract(
    'MSC-122', {
        'bf74f1c288658ea0': [('2026-10-15T17:50:00Z', args.cutoff)],
        'bcd5993b4416ed72': [('2026-10-17T05:00:00Z', args.cutoff)],
    }, args.cutoff, started='2026-10-15',
    include_archived_segments=True, allow_unpriced_models=True,
    note='Incremental template regression QA, seed/installer repairs, resource failure/recovery, corrections and closeout. Raw response IDs deduplicated. October 12 MSC-122 delivery is retained separately; this increment replaces its prior measurement rather than being appended twice. Final accounting/publication after cutoff is excluded. Task timing includes tool waits; cached input is within input and reasoning within output. Frozen rates; full cost unavailable for unpriced models.'
)
print(json.dumps(result, indent=2))
