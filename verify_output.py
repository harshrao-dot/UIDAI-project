"""Verify output files."""
import pandas as pd
from pathlib import Path

print("=" * 60)
print("Verifying Output Files")
print("=" * 60)

data_dir = Path('processed_data')

# Check main dataset
if (data_dir / 'processed_data.csv').exists():
    df = pd.read_csv(data_dir / 'processed_data.csv')
    print(f"\n[OK] processed_data.csv")
    print(f"  Rows: {len(df):,}")
    print(f"  Columns: {len(df.columns)}")
    if 'year_month' in df.columns:
        print(f"  Date range: {df['year_month'].min()} to {df['year_month'].max()}")
    if 'state' in df.columns:
        print(f"  States: {df['state'].nunique()}")
    if 'district' in df.columns:
        print(f"  Districts: {df['district'].nunique()}")
    if 'AISI' in df.columns:
        print(f"  AISI range: {df['AISI'].min():.3f} to {df['AISI'].max():.3f}")

# Check other files
files_to_check = [
    'persistence_index.csv',
    'rank_volatility.csv',
    'shock_detection.csv',
    'early_warnings.csv',
    'insights.json',
    'results.pkl'
]

for file in files_to_check:
    if (data_dir / file).exists():
        size = (data_dir / file).stat().st_size
        print(f"\n[OK] {file} ({size:,} bytes)")
    else:
        print(f"\n[WARNING] {file} not found")

print("\n" + "=" * 60)
print("Verification Complete!")
print("=" * 60)
