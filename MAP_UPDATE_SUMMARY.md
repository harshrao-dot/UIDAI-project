# India Map Heatmap Update

## Changes Made

### ✅ Added India Map Visualization

**File Created**: `india_map_helper.py`
- Contains state coordinates (lat/lon) for all Indian states
- State name normalization to handle variations
- Function to prepare map data with coordinates

**File Updated**: `app.py`
- Replaced bar chart with actual geographical India map
- Uses `scatter_mapbox` for interactive map visualization
- Shows location-based colors (heatmap) based on selected metric
- Fallback to `scatter_geo` if mapbox doesn't work

## Features

### 🗺️ Interactive India Map
- **Location-based visualization**: States shown on actual India map
- **Color-coded heatmap**: Red scale based on metric value
- **Size encoding**: Larger bubbles for higher values
- **Hover information**: Shows state name and metric value
- **Zoomable**: Interactive map that can be zoomed and panned

### 📍 State Coverage
- All 60 states/UTs included
- Coordinates mapped for accurate positioning
- Handles state name variations automatically

### 🎨 Visualization Options
1. **Primary**: Mapbox scatter map (requires internet, uses OpenStreetMap)
2. **Fallback**: Plotly geo scatter (works offline, uses natural earth projection)

## How It Works

1. **Data Preparation**: 
   - Aggregates metric by state
   - Normalizes state names
   - Adds coordinates (lat/lon) for each state

2. **Map Creation**:
   - Uses plotly's `scatter_mapbox` for interactive map
   - Colors and sizes based on metric value
   - Centered on India (20.59°N, 78.96°E)

3. **User Interaction**:
   - Hover to see state name and value
   - Zoom in/out
   - Pan around the map

## Usage

The map automatically appears in the dashboard when you:
1. Select a metric (ESS, MSP, YCR, DPI, or AISI)
2. The map shows state-wise heatmap
3. Colors range from light (low values) to dark red (high values)

## Technical Details

- **Map Style**: OpenStreetMap (no token required)
- **Projection**: Geographic coordinates (lat/lon)
- **Color Scale**: Reds (light to dark)
- **Size Range**: Proportional to metric value
- **Height**: 600px

## Example

When viewing AISI metric:
- States with high AISI (high stress) appear as large, dark red bubbles
- States with low AISI (low stress) appear as small, light red bubbles
- Map shows geographical distribution of stress across India

## Notes

- Map requires internet connection for OpenStreetMap tiles
- If mapbox fails, automatically falls back to geo scatter
- State names are normalized to handle data variations
- Invalid state names are filtered out automatically
