"""Test if map displays correctly."""
import pandas as pd
from india_map_helper import prepare_map_data
import plotly.express as px

print("Testing map display...")
df = pd.read_csv('processed_data/processed_data.csv')
map_df = prepare_map_data(df, 'AISI')

max_val = map_df['value'].max()
min_val = map_df['value'].min()
val_range = max_val - min_val if max_val > min_val else 1
map_df['marker_size'] = ((map_df['value'] - min_val) / val_range * 80 + 30) if val_range > 0 else 50

print(f"Data prepared: {len(map_df)} states")
print(f"Marker size range: {map_df['marker_size'].min():.1f} to {map_df['marker_size'].max():.1f}")

# Create map
fig = px.scatter_geo(
    map_df,
    lat='lat',
    lon='lon',
    size='marker_size',
    color='value',
    hover_name='state_display',
    projection='natural earth',
    height=600
)

fig.update_geos(
    center=dict(lat=20.5937, lon=78.9629),
    projection_scale=5
)

print("\n[OK] Map figure created successfully!")
print("Map should display in Streamlit dashboard.")
print("\nIf map doesn't show, check:")
print("1. Internet connection (for map tiles)")
print("2. Streamlit version (should be >= 1.28.0)")
print("3. Plotly version (should be >= 5.17.0)")
