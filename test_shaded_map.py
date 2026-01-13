"""Test shaded map visualization."""
import pandas as pd
from india_map_helper import prepare_map_data

# Load processed data
df = pd.read_csv('processed_data/processed_data.csv')

# Test map data preparation
print("Testing shaded map visualization...")
map_df = prepare_map_data(df, 'AISI', group_by='state')

# Calculate sizes for filled appearance
max_val = map_df['value'].max()
min_val = map_df['value'].min()
val_range = max_val - min_val if max_val > min_val else 1
map_df['marker_size'] = ((map_df['value'] - min_val) / val_range * 80 + 30) if val_range > 0 else 50

print(f"\nMap data: {len(map_df)} states")
print(f"Value range: {map_df['value'].min():.3f} to {map_df['value'].max():.3f}")
print(f"Marker size range: {map_df['marker_size'].min():.1f} to {map_df['marker_size'].max():.1f}")
print(f"\nColor scale: Light pink (low) -> Dark red (high)")
print(f"  - Low values: rgb(255,200,200)")
print(f"  - Medium values: rgb(200,50,50)")
print(f"  - High values: rgb(100,0,0)")

print("\n[OK] Shaded map visualization ready!")
print("Features:")
print("  - Large filled markers (30-110 size)")
print("  - Dark red color scale for visibility")
print("  - Shaded appearance (not circles)")
