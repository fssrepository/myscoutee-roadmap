#!/usr/bin/env python3
"""Read-only MSC-123 usage aggregation from explicitly scoped local sessions."""
import argparse, importlib.util, json, pathlib, sys
sys.dont_write_bytecode = True
root = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('usage', root / 'measure-msc119.py')
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cutoff', required=True)
args = parser.parse_args()
result = usage.extract('MSC-123', {
    'bcd5993b4416ed72': [
        ('2026-10-17T08:16:46.559Z', '2026-10-17T08:24:03.302Z'),
        ('2026-10-17T08:31:07.855Z', args.cutoff),
    ],
    'c867a492eb2e5063': [('2026-10-17T12:05:57.449Z', args.cutoff)],
    'bc918f7fa4fb771b': [('2026-10-17T12:41:38.840Z', args.cutoff)],
}, args.cutoff, started='2026-10-17', include_archived_segments=True,
allow_unpriced_models=True,
note='Deployment task: verified CodeQL/dependency changes, VMware packaging/data repairs, real-provider/device checks, reported defects and corrections, source consolidation, main/template signed release preparation, Components registry publication, requested template VMware installation/smoke, canonical app/template publication verification and the requested production Netcup 1.4.1 upgrade/verification through the cutoff. Excludes preceding template QA, its history/Pages/accounting work and the 08:24:03–08:31:07 prior-QA closeout discussion. Includes scoped concurrent clarification about native Back; response IDs deduplicated and active intervals unioned. Tool/build/network waits are included; idle gaps are not human work. Cached input is within input and reasoning within output. Frozen existing rates; unpriced models remain unpriced. Later accounting/publication bookkeeping is excluded, not estimated.')
print(json.dumps(result, indent=2))
