"""
Helper functions for India map visualization.
State coordinates and mapping for choropleth visualization.
"""
import pandas as pd

# Indian states with approximate coordinates (centroids)
INDIA_STATE_COORDINATES = {
    'Andhra Pradesh': {'lat': 15.9129, 'lon': 79.7400},
    'Arunachal Pradesh': {'lat': 28.2180, 'lon': 94.7278},
    'Assam': {'lat': 26.2006, 'lon': 92.9376},
    'Bihar': {'lat': 25.0961, 'lon': 85.3131},
    'Chhattisgarh': {'lat': 21.2787, 'lon': 81.8661},
    'Goa': {'lat': 15.2993, 'lon': 74.1240},
    'Gujarat': {'lat': 23.0225, 'lon': 72.5714},
    'Haryana': {'lat': 29.0588, 'lon': 76.0856},
    'Himachal Pradesh': {'lat': 31.1048, 'lon': 77.1734},
    'Jammu and Kashmir': {'lat': 34.0837, 'lon': 74.7973},
    'Jharkhand': {'lat': 23.6102, 'lon': 85.2799},
    'Karnataka': {'lat': 15.3173, 'lon': 75.7139},
    'Kerala': {'lat': 10.8505, 'lon': 76.2711},
    'Madhya Pradesh': {'lat': 22.9734, 'lon': 78.6569},
    'Maharashtra': {'lat': 19.7515, 'lon': 75.7139},
    'Manipur': {'lat': 24.6637, 'lon': 93.9063},
    'Meghalaya': {'lat': 25.4670, 'lon': 91.3662},
    'Mizoram': {'lat': 23.1645, 'lon': 92.9376},
    'Nagaland': {'lat': 26.1584, 'lon': 94.5624},
    'Odisha': {'lat': 20.9517, 'lon': 85.0985},
    'Punjab': {'lat': 30.7333, 'lon': 76.7794},
    'Rajasthan': {'lat': 27.0238, 'lon': 74.2179},
    'Sikkim': {'lat': 27.5330, 'lon': 88.5122},
    'Tamil Nadu': {'lat': 11.1271, 'lon': 78.6569},
    'Telangana': {'lat': 18.1124, 'lon': 79.0193},
    'Tripura': {'lat': 23.9408, 'lon': 91.9882},
    'Uttar Pradesh': {'lat': 26.8467, 'lon': 80.9462},
    'Uttarakhand': {'lat': 30.0668, 'lon': 79.0193},
    'West Bengal': {'lat': 22.9868, 'lon': 87.8550},
    'Delhi': {'lat': 28.6139, 'lon': 77.2090},
    'Puducherry': {'lat': 11.9416, 'lon': 79.8083},
    'Ladakh': {'lat': 34.1526, 'lon': 77.5770},
    'Andaman and Nicobar Islands': {'lat': 11.7401, 'lon': 92.6586},
    'Chandigarh': {'lat': 30.7333, 'lon': 76.7794},
    'Dadra and Nagar Haveli and Daman and Diu': {'lat': 20.1809, 'lon': 73.0169},
    'Lakshadweep': {'lat': 10.5667, 'lon': 72.6417}
}

# State name normalization mapping (handle variations)
STATE_NAME_MAPPING = {
    'Jammu and Kashmir': 'Jammu and Kashmir',
    'J & K': 'Jammu and Kashmir',
    'J&K': 'Jammu and Kashmir',
    'Himachal': 'Himachal Pradesh',
    'Punjab': 'Punjab',
    'Uttarakhand': 'Uttarakhand',
    'Uttaranchal': 'Uttarakhand',
    'Haryana': 'Haryana',
    'Delhi': 'Delhi',
    'NCT of Delhi': 'Delhi',
    'Rajasthan': 'Rajasthan',
    'Uttar Pradesh': 'Uttar Pradesh',
    'UP': 'Uttar Pradesh',
    'Bihar': 'Bihar',
    'Sikkim': 'Sikkim',
    'Arunachal Pradesh': 'Arunachal Pradesh',
    'Nagaland': 'Nagaland',
    'Manipur': 'Manipur',
    'Mizoram': 'Mizoram',
    'Tripura': 'Tripura',
    'Meghalaya': 'Meghalaya',
    'Assam': 'Assam',
    'West Bengal': 'West Bengal',
    'Jharkhand': 'Jharkhand',
    'Odisha': 'Odisha',
    'Orissa': 'Odisha',
    'Chhattisgarh': 'Chhattisgarh',
    'Madhya Pradesh': 'Madhya Pradesh',
    'MP': 'Madhya Pradesh',
    'Gujarat': 'Gujarat',
    'Daman and Diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'Dadra and Nagar Haveli': 'Dadra and Nagar Haveli and Daman and Diu',
    'Maharashtra': 'Maharashtra',
    'Andhra Pradesh': 'Andhra Pradesh',
    'Karnataka': 'Karnataka',
    'Goa': 'Goa',
    'Kerala': 'Kerala',
    'Tamil Nadu': 'Tamil Nadu',
    'Puducherry': 'Puducherry',
    'Pondicherry': 'Puducherry',
    'Telangana': 'Telangana',
    'Andaman and Nicobar Islands': 'Andaman and Nicobar Islands',
    'Lakshadweep': 'Lakshadweep',
    'Chandigarh': 'Chandigarh',
    'Ladakh': 'Ladakh'
}


def normalize_state_name(state_name):
    """Normalize state names to standard format."""
    if pd.isna(state_name):
        return None
    s = str(state_name).strip()
    # Replace ampersand, remove stray characters and collapse whitespace
    s = s.replace('&', 'and').replace('�', '').replace('?', '').strip()
    s = ' '.join(s.split())

    # Handle numeric or invalid state names
    if s.isdigit() or len(s) < 3:
        return None

    s_lower = s.lower()
    # Handle common variations
    if 'andaman' in s_lower and 'nicobar' in s_lower:
        return 'Andaman and Nicobar Islands'
    if 'chhattisgarh' in s_lower or 'chhatisgarh' in s_lower:
        return 'Chhattisgarh'
    if 'jammu' in s_lower and 'kashmir' in s_lower:
        return 'Jammu and Kashmir'
    if 'dadra' in s_lower or 'daman' in s_lower or 'diu' in s_lower:
        return 'Dadra and Nagar Haveli and Daman and Diu'

    # Match mapping keys case-insensitively
    for k, v in STATE_NAME_MAPPING.items():
        if s.lower() == k.lower():
            return v

    return s


def normalize_district_name(district_name):
    """Normalize district names. Return None for invalid entries (numeric placeholders etc.)."""
    if pd.isna(district_name):
        return None
    d = str(district_name).strip()
    d = d.replace('&', 'and').replace('�', '').replace('?', '').strip()
    d = ' '.join(d.split())
    if d.isdigit() or len(d) < 2:
        return None
    return d


def get_state_coordinates(state_name):
    """Get coordinates for a state."""
    normalized = normalize_state_name(state_name)
    return INDIA_STATE_COORDINATES.get(normalized, {'lat': 20.5937, 'lon': 78.9629})  # Default: India center


def prepare_map_data(df, metric_col, group_by='state'):
    """
    Prepare data for India map visualization.
    Returns dataframe with coordinates and metric values.
    """
    # Aggregate by state
    if group_by == 'state':
        map_df = df.groupby('state')[metric_col].mean().reset_index()
        map_df.columns = ['state', 'value']
    else:
        # For district level, aggregate by state (can be enhanced later)
        map_df = df.groupby('state')[metric_col].mean().reset_index()
        map_df.columns = ['state', 'value']

    # Normalize state names and filter invalid ones
    map_df['state_normalized'] = map_df['state'].apply(normalize_state_name)
    map_df = map_df[map_df['state_normalized'].notna()].copy()

    # Add coordinates
    map_df['lat'] = map_df['state_normalized'].apply(lambda x: get_state_coordinates(x)['lat'])
    map_df['lon'] = map_df['state_normalized'].apply(lambda x: get_state_coordinates(x)['lon'])

    # Use normalized name for display but keep original for hover
    map_df['state_display'] = map_df['state_normalized']

    return map_df[['state', 'state_display', 'value', 'lat', 'lon']]


def try_load_india_geojson(paths=None):
    """Try to load a local India states GeoJSON from common filenames.
    Returns (geojson_obj, property_key) or (None, None) if not found.
    The property_key is the feature property name that holds the state name (e.g., 'ST_NM', 'NAME').
    """
    import json
    from pathlib import Path

    if paths is None:
        paths = ['india_states.geojson', 'data/india_states.geojson', 'processed_data/india_states.geojson']

    for p in paths:
        fp = Path(p)
        if fp.exists():
            try:
                geo = json.loads(fp.read_text(encoding='utf-8'))
                # Inspect properties of first feature to find suitable name key
                if 'features' in geo and len(geo['features']) > 0:
                    props = geo['features'][0].get('properties', {})
                    # Common keys
                    candidates = ['st_nm', 'ST_NM', 'STATE_NAME', 'state', 'name', 'NAME']
                    for c in candidates:
                        if c in props:
                            return geo, c
                    # fallback: pick first string property
                    for k, v in props.items():
                        if isinstance(v, str) and len(v) > 0:
                            return geo, k
                return geo, None
            except Exception:
                continue
    return None, None


def geojson_state_name_to_normalized(geojson, prop_key):
    """Return a mapping from normalized state name -> original geojson property name value."""
    mapping = {}
    if geojson is None or prop_key is None:
        return mapping
    for feat in geojson.get('features', []):
        props = feat.get('properties', {})
        raw = props.get(prop_key, '')
        norm = normalize_state_name(raw)
        if norm:
            mapping[norm] = raw
    return mapping
