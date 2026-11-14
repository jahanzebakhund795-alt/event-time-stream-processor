"""Event Time Stream Processor. Synthetic portfolio demonstration."""
def run(data):
    width, lateness = data['window_seconds'], data['allowed_lateness_seconds']
    if width <= 0 or lateness < 0:
        raise ValueError('Window must be positive and lateness nonnegative')
    seen, windows, late, duplicates = set(), {}, [], 0
    maximum = float('-inf')
    for event in data['events']:
        if event['id'] in seen:
            duplicates += 1
            continue
        seen.add(event['id'])
        maximum = max(maximum, event['ts'])
        if event['ts'] < maximum - lateness:
            late.append(event['id'])
            continue
        start = event['ts'] // width * width
        windows[start] = windows.get(start, 0) + event['quantity']
    return {'windows': {str(k):v for k,v in sorted(windows.items())},
            'late_event_ids': late, 'duplicates': duplicates}



if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('sample.json'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(json.loads(args.input.read_text()))
    serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    if args.output:
        args.output.write_text(serialized + '\n')
    else:
        print(serialized)
