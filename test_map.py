"""Test India map visualization."""
import pandas as pd
from pathlib import Path
from india_map_helper import prepare_map_data

# Load processed data
df = pd.read_csv('processed_data/processed_data.csv')

# Test map data preparation
print("Testing map data preparation...")
map_df = prepare_map_data(df, 'AISI', group_by='state')

print(f"\nMap data prepared:")
print(f"States: {len(map_df)}")
print(f"\nSample data:")
print(map_df.head(10))

print(f"\nValue range: {map_df['value'].min():.3f} to {map_df['value'].max():.3f}")
print(f"\nCoordinates range:")
print(f"Lat: {map_df['lat'].min():.2f} to {map_df['lat'].max():.2f}")
print(f"Lon: {map_df['lon'].min():.2f} to {map_df['lon'].max():.2f}")

print("\n[OK] Map data preparation successful!")
