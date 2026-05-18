import pandas as pd
from pathlib import Path


def main():
    src = Path('data/clean/events.csv')
    outdir = Path('data/transformed')
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(src)
    df['date'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d')

    df.to_csv(outdir / 'events.csv', index=False)


if __name__ == '__main__':
    main()
