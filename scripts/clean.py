import re
import pandas as pd
from pathlib import Path


def normalize_event_type(val: str):
    if pd.isna(val):
        return None
    s = re.sub(r'[^A-Za-z]', '', str(val)).lower()
    mapping = {
        'buy': 'purchase',
        'purchase': 'purchase',
        'purchase!': 'purchase',
        'klick': 'click',
        'click': 'click',
        'view': 'view',
        'scroll': 'scroll',
        'login': 'login',
    }
    if s in mapping:
        return mapping[s]
    return None


def main():
    src = Path('data/raw/events.csv')
    outdir = Path('data/clean')
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(src, dtype=str)

    # drop rows with any missing fields
    df = df.dropna()

    # coerce duration to numeric and drop non-positive
    df['duration_seconds'] = pd.to_numeric(df['duration_seconds'], errors='coerce')
    df = df.dropna(subset=['duration_seconds'])
    df = df[df['duration_seconds'] > 0]

    # normalize event_type and drop invalid
    df['event_type'] = df['event_type'].apply(normalize_event_type)
    df = df.dropna(subset=['event_type'])

    # parse timestamps and normalize to ISO 8601 without microseconds
    df['timestamp'] = pd.to_datetime(df['timestamp'], infer_datetime_format=True, errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    df.to_csv(outdir / 'events.csv', index=False)


if __name__ == '__main__':
    main()
