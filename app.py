"""
Streamlit Dashboard: Aadhaar Identity Stress Early-Warning & Policy Intelligence System
Full-featured dashboard with all required panels and visualizations.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
from pathlib import Path
from india_map_helper import normalize_state_name, normalize_district_name



# if "theme" not in st.session_state:
#     st.session_state.theme = "light"

# with st.sidebar:
#     if st.button("Toggle Theme"):
#         st.session_state.theme = (
#             "dark" if st.session_state.theme == "light" else "light"
#         )

# def apply_theme(theme):
#     if theme == "dark":
#         st.markdown(
#             """
#             <style>
#             /* App background */
#             .stApp {
#                 background-color: #0e1117;
#                 color: #fafafa;
#             }

#             /* Sidebar */
#             section[data-testid="stSidebar"] {
#                 background-color: #161b22;
#             }

#             /* Text */
#             h1, h2, h3, h4, h5, h6, p, span, label, div {
#                 color: #fafafa !important;
#             }

#             /* Buttons */
#             button {
#                 background-color: #21262d !important;
#                 color: #fafafa !important;
#                 border: 1px solid #30363d !important;
#             }

#             /* Inputs */
#             input, textarea, select {
#                 background-color: #0e1117 !important;
#                 color: #fafafa !important;
#                 border: 1px solid #30363d !important;
#             }

#             /* Tables */
#             thead tr th {
#                 background-color: #161b22 !important;
#                 color: #fafafa !important;
#             }

#             tbody tr td {
#                 background-color: #0e1117 !important;
#                 color: #fafafa !important;
#             }
#             </style>
#             """,
#             unsafe_allow_html=True,
#         )

#     else:
#         st.markdown(
#             """
#             <style>
#             .stApp {
#                 background-color: #ffffff;
#                 color: #000000;
#             }

#             section[data-testid="stSidebar"] {
#                 background-color: #f0f2f6;
#             }

#             h1, h2, h3, h4, h5, h6, p, span, label, div {
#                 color: #000000 !important;
#             }

#             button {
#                 background-color: #ffffff !important;
#                 color: #000000 !important;
#                 border: 1px solid #cccccc !important;
#             }

#             input, textarea, select {
#                 background-color: #ffffff !important;
#                 color: #000000 !important;
#                 border: 1px solid #cccccc !important;
#             }

#             thead tr th {
#                 background-color: #f0f2f6 !important;
#                 color: #000000 !important;
#             }

#             tbody tr td {
#                 background-color: #ffffff !important;
#                 color: #000000 !important;
#             }
#             </style>
#             """,
#             unsafe_allow_html=True,
#         )
# apply_theme(st.session_state.theme)


# Page config
st.set_page_config(
    page_title="Aadhaar Identity Stress System",
    page_icon="🆔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .kpi-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_processed_data():
    """Load processed data and results."""
    data_path = Path('processed_data')
    
    if not (data_path / 'results.pkl').exists():
        st.error("Processed data not found. Please run main_pipeline.py first.")
        return None
    
    with open(data_path / 'results.pkl', 'rb') as f:
        results = pickle.load(f)
    
    return results


def load_dataframes():
    """Load CSV files if pickle not available."""
    data_path = Path('processed_data')
    df = pd.read_csv(data_path / 'processed_data.csv')
    
    results = {
        'data': df,
        'persistence': pd.read_csv(data_path / 'persistence_index.csv') if (data_path / 'persistence_index.csv').exists() else pd.DataFrame(),
        'early_warnings': pd.read_csv(data_path / 'early_warnings.csv') if (data_path / 'early_warnings.csv').exists() else pd.DataFrame(),
    }
    
    return results


def main():
    st.markdown('<div class="main-header">🆔 Aadhaar Identity Stress Early-Warning System</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data
    try:
        results = load_processed_data()
    except:
        results = load_dataframes()
    
    if results is None:
        return
    
    df = results['data']
    
    # Convert year_month to string for filtering
    if 'year_month' in df.columns:
        df['year_month_str'] = df['year_month'].astype(str)
    
    # Sidebar
    st.sidebar.header("Filters")
    
    # Normalize state and district names (avoid numeric placeholders like '100000' or stray symbols)
    df['state_normalized'] = df['state'].apply(normalize_state_name)
    df['district_normalized'] = df['district'].apply(normalize_district_name)

    # State dropdown (use normalized names)
    states = ['All'] + sorted(df['state_normalized'].dropna().unique().tolist())
    selected_state = st.sidebar.selectbox("Select State", states)
    
    # District dropdown (dynamic; use normalized district names filtered by normalized state)
    if selected_state != 'All':
        districts = ['All'] + sorted(df[df['state_normalized'] == selected_state]['district_normalized'].dropna().unique().tolist())
    else:
        districts = ['All'] + sorted(df['district_normalized'].dropna().unique().tolist())
    
    selected_district = st.sidebar.selectbox("Select District", districts)
    
    # Date range
    if 'year_month_str' in df.columns:
        date_range = sorted(df['year_month_str'].unique())
        if len(date_range) > 0:
            start_date = st.sidebar.selectbox("Start Date", date_range, index=0)
            end_date = st.sidebar.selectbox("End Date", date_range, index=len(date_range)-1)
        else:
            start_date = end_date = None
    else:
        start_date = end_date = None
    
    # Metric selector
    metrics = ['ESS', 'MSP', 'YCR', 'DPI', 'AISI']
    available_metrics = [m for m in metrics if m in df.columns]
    selected_metric = st.sidebar.selectbox("Select Metric", available_metrics)
    
    # Filter data (using normalized names)
    filtered_df = df.copy()
    if selected_state != 'All':
        filtered_df = filtered_df[filtered_df['state_normalized'] == selected_state]
    if selected_district != 'All':
        filtered_df = filtered_df[filtered_df['district_normalized'] == selected_district]
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['year_month_str'] >= start_date) & 
            (filtered_df['year_month_str'] <= end_date)
        ]
    
    # Main content
    # KPI Cards
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'ESS' in filtered_df.columns:
            st.metric("Mean ESS", f"{filtered_df['ESS'].mean():.3f}", 
                     delta=f"{filtered_df['ESS'].std():.3f} std")
    
    with col2:
        if 'MSP' in filtered_df.columns:
            st.metric("Mean MSP", f"{filtered_df['MSP'].mean():.3f}",
                     delta=f"{filtered_df['MSP'].std():.3f} std")
    
    with col3:
        if 'AISI' in filtered_df.columns:
            st.metric("Mean AISI", f"{filtered_df['AISI'].mean():.3f}",
                     delta=f"{filtered_df['AISI'].std():.3f} std")
    
    with col4:
        if 'total_enrolments' in filtered_df.columns:
            st.metric("Total Enrolments", f"{filtered_df['total_enrolments'].sum():,.0f}")
    
    st.markdown("---")
    
    # India Map Heatmap - Actual geographical map with location-based colors
    st.subheader(f"India Map Heatmap: {selected_metric}")
    
    if selected_metric in filtered_df.columns:
        from india_map_helper import prepare_map_data
        
        # Prepare map data with coordinates
        try:
            # ensure mapping uses normalized state names and drop invalid rows
            if 'state_normalized' in filtered_df.columns:
                temp_df = filtered_df[filtered_df['state_normalized'].notna()].copy()
                temp_df['state'] = temp_df['state_normalized']
            else:
                temp_df = filtered_df.copy()

            map_df = prepare_map_data(temp_df, selected_metric, group_by='state')

            if len(map_df) == 0:
                st.warning("No data available for map visualization.")
                return

            # Prefer filled choropleth if a local India states GeoJSON is available
            from india_map_helper import try_load_india_geojson, geojson_state_name_to_normalized
            geojson, geo_prop = try_load_india_geojson()

            if geojson is not None and geo_prop is not None:
                # Map geojson property names to our normalized state names
                geo_norm_map = geojson_state_name_to_normalized(geojson, geo_prop)
                # Keep only states present in both data and geojson
                map_df['state_for_geo'] = map_df['state_display'].apply(lambda s: geo_norm_map.get(s))
                choropleth_df = map_df.dropna(subset=['state_for_geo']).copy()

                if len(choropleth_df) == 0:
                    # No matching states; fall back to scatter
                    use_choropleth = False
                else:
                    use_choropleth = True
            else:
                use_choropleth = False

            if use_choropleth:
                # Create a filled choropleth using the GeoJSON (non-mapbox, avoids access token issues)
                min_val = choropleth_df['value'].min()
                max_val = choropleth_df['value'].max()

                fig_map = px.choropleth(
                    choropleth_df,
                    geojson=geojson,
                    locations='state_for_geo',
                    color='value',
                    featureidkey=f'properties.{geo_prop}',
                    hover_name='state_display',
                    hover_data={'value': ':.3f'},
                    color_continuous_scale='Reds',
                    range_color=(min_val, max_val),
                    projection='mercator',
                    title=f"{selected_metric} Choropleth Across Indian States",
                    height=650
                )
                # Make boundaries visible and colorbar clearer
                fig_map.update_traces(marker_line_width=0.5, marker_line_color='white')
                fig_map.update_layout(
                    margin=dict(l=0, r=0, t=40, b=0),
                    coloraxis_colorbar=dict(thickness=20, len=0.6, title={'text': selected_metric})
                )
                # Fit map to locations
                fig_map.update_geos(fitbounds="locations", visible=False)
                # Better hover template
                fig_map.update_traces(hovertemplate="<b>%{customdata[0]}</b><br>" + f"{selected_metric}: %{{z:.3f}}<extra></extra>")
                
                # Add text labels for values over the map
                fig_map.add_scattergeo(
                    lat=choropleth_df['lat'],
                    lon=choropleth_df['lon'],
                    text=choropleth_df.apply(lambda row: f"{row['value']:.2f}", axis=1),
                    mode='text',
                    textfont=dict(color='black', size=10, family="Arial, sans-serif"),
                    hoverinfo='skip'
                )
            else:
                # Create India map with shaded/filled regions - fallback to scatter_geo (no token needed)
                # Calculate normalized sizes for better visibility (larger, filled areas)
                max_val = map_df['value'].max()
                min_val = map_df['value'].min()
                val_range = max_val - min_val if max_val > min_val else 1

                # Scale sizes to create filled/shaded appearance
                map_df['marker_size'] = ((map_df['value'] - min_val) / val_range * 80 + 30) if val_range > 0 else 50

                # Use scatter_geo instead of mapbox (no token required, works offline)
                fig_map = px.scatter_geo(
                    map_df,
                    lat='lat',
                    lon='lon',
                    size='marker_size',
                    color='value',
                    hover_name='state_display',
                    hover_data={'value': ':.3f', 'state': True, 'marker_size': False},
                    color_continuous_scale=[[0, 'rgb(255,200,200)'], [0.2, 'rgb(255,100,100)'], 
                                          [0.5, 'rgb(200,50,50)'], [0.8, 'rgb(150,0,0)'], 
                                          [1, 'rgb(100,0,0)']],  # Very dark red scale
                    size_max=110,  # Large size for filled appearance
                    projection='natural earth',
                    title=f"{selected_metric} Heatmap Across Indian States (Shaded Regions)",
                    height=600
                )
            
                # Update traces to make them look like filled/shaded regions
                fig_map.update_traces(
                    marker=dict(
                        sizemode='diameter',
                        sizemin=30,  # Minimum size for visibility
                        opacity=0.85,  # Slightly transparent
                        line=dict(width=1.5, color='rgb(80,0,0)')  # Dark red border
                    ),
                    hovertemplate='<b>%{hovertext}</b><br>' +
                                f'{selected_metric}: %{{customdata[0]:.3f}}<extra></extra>',
                    customdata=map_df[['value']].values
                )
            
            # Center on India and zoom
            fig_map.update_geos(
                center=dict(lat=20.5937, lon=78.9629),
                projection_scale=5,  # Zoom level
                visible=True,
                resolution=50
            )
            
            # Darker color scale with better visibility
            fig_map.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                geo=dict(
                    bgcolor='rgba(0,0,0,0)',
                    showland=True,
                    landcolor='rgb(243,243,243)',
                    showocean=True,
                    oceancolor='rgb(230,245,255)',
                    showlakes=True,
                    lakecolor='rgb(230,245,255)',
                    showcountries=True,
                    countrycolor='rgb(200,200,200)'
                ),
                coloraxis=dict(
                    colorbar=dict(
                        title=dict(text=selected_metric, font=dict(size=14)),
                        thickness=20,
                        len=0.6
                    ),
                    cmin=min_val,
                    cmax=max_val,
                    colorscale=[[0, 'rgb(255,200,200)'], [0.2, 'rgb(255,100,100)'], 
                               [0.5, 'rgb(200,50,50)'], [0.8, 'rgb(150,0,0)'], 
                               [1, 'rgb(100,0,0)']]  # Very dark red scale for visibility
                )
            )
            
            # Display the map
            with st.spinner("Loading map..."):
                st.plotly_chart(fig_map, use_container_width=True)
            
        except Exception as e:
            st.error(f"Map visualization error: {str(e)}")
            import traceback
            with st.expander("Error Details (Click to expand)"):
                st.code(traceback.format_exc())
            st.info("Showing alternative visualization...")
            
            # Calculate sizes for filled appearance
            max_val = map_df['value'].max()
            min_val = map_df['value'].min()
            val_range = max_val - min_val if max_val > min_val else 1
            map_df['marker_size'] = ((map_df['value'] - min_val) / val_range * 80 + 30) if val_range > 0 else 50
            
            fig_geo = px.scatter_geo(
                map_df,
                lat='lat',
                lon='lon',
                size='marker_size',
                color='value',
                hover_name='state_display',
                hover_data={'value': ':.3f', 'state': True, 'marker_size': False},
                color_continuous_scale=[[0, 'rgb(255,200,200)'], [0.2, 'rgb(255,100,100)'], 
                                      [0.5, 'rgb(200,50,50)'], [0.8, 'rgb(150,0,0)'], 
                                      [1, 'rgb(100,0,0)']],  # Very dark red scale
                size_max=110,
                projection='natural earth',
                title=f"{selected_metric} Heatmap Across Indian States (Shaded Regions)",
                height=600
            )
            
            # Make markers filled and more visible
            fig_geo.update_traces(
                marker=dict(
                    sizemode='diameter',
                    sizemin=30,
                    opacity=0.85,
                    line=dict(width=1.5, color='rgb(80,0,0)')
                ),
                hovertemplate='<b>%{hovertext}</b><br>' +
                            f'{selected_metric}: %{{customdata[0]:.3f}}<extra></extra>',
                customdata=map_df[['value']].values
            )
            
            fig_geo.update_geos(
                center=dict(lat=20.5937, lon=78.9629),
                projection_scale=5
            )
            fig_geo.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                coloraxis=dict(
                    colorbar=dict(
                        title=dict(text=selected_metric, font=dict(size=14)),
                        thickness=20,
                        len=0.6
                    ),
                    cmin=min_val,
                    cmax=max_val,
                    colorscale=[[0, 'rgb(255,200,200)'], [0.2, 'rgb(255,100,100)'], 
                               [0.5, 'rgb(200,50,50)'], [0.8, 'rgb(150,0,0)'], 
                               [1, 'rgb(100,0,0)']]
                )
            )
            st.plotly_chart(fig_geo, use_container_width=True)
        
        # Also show bar chart for reference
        with st.expander("View State-wise Bar Chart (Alternative View)"):
            # Aggregate using normalized state names and drop invalid entries
            if 'state_normalized' in filtered_df.columns:
                state_agg = (
                    filtered_df
                    .dropna(subset=['state_normalized', selected_metric])
                    .groupby('state_normalized')[selected_metric]
                    .mean()
                    .reset_index()
                )
                state_agg.columns = ['state', 'value']
            else:
                state_agg = (
                    filtered_df
                    .dropna(subset=[selected_metric])
                    .groupby('state')[selected_metric]
                    .mean()
                    .reset_index()
                )
                state_agg.columns = ['state', 'value']

            state_agg = state_agg.sort_values('value', ascending=False)

            fig_bar = px.bar(
                state_agg,
                x='state',
                y='value',
                color='value',
                color_continuous_scale='Reds',
                title=f"{selected_metric} by State (Sorted)"
            )
            fig_bar.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # District Time-Series Trend
    st.subheader("District Time-Series Trend")
    
    if selected_district != 'All' and 'year_month_str' in filtered_df.columns:
        district_trend = filtered_df.groupby('year_month_str')[selected_metric].mean().reset_index()
        fig_trend = px.line(
            district_trend,
            x='year_month_str',
            y=selected_metric,
            title=f"{selected_metric} Trend Over Time"
        )
        fig_trend.update_layout(height=400)
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        # Show top districts (use normalized names)
        district_col = 'district_normalized' if 'district_normalized' in filtered_df.columns else 'district'
        if district_col in filtered_df.columns and selected_metric in filtered_df.columns:
            top_districts = (
                filtered_df
                .dropna(subset=[district_col, selected_metric])
                .groupby(district_col)[selected_metric]
                .mean()
                .nlargest(10)
                .reset_index()
            )
            top_districts = top_districts.rename(columns={district_col: 'district'})
            fig_trend = px.bar(
                top_districts,
                x='district',
                y=selected_metric,
                title=f"Top 10 Districts by {selected_metric}"
            )
            fig_trend.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_trend, use_container_width=True)
    
    # ESS vs MSP Scatter (colored by AISI)
    st.subheader("ESS vs MSP Scatter (Colored by AISI)")
    
    if all(m in filtered_df.columns for m in ['ESS', 'MSP', 'AISI']):
        scatter_df = filtered_df.groupby(['state', 'district']).agg({
            'ESS': 'mean',
            'MSP': 'mean',
            'AISI': 'mean'
        }).reset_index()
        
        fig_scatter = px.scatter(
            scatter_df,
            x='ESS',
            y='MSP',
            color='AISI',
            size='AISI',
            hover_data=['state', 'district'],
            color_continuous_scale='RdYlGn_r',
            title="ESS vs MSP (Size & Color = AISI)"
        )
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # District × Month Heatmap
    st.subheader("District × Month Heatmap")
    
    if selected_state != 'All' and 'year_month_str' in filtered_df.columns:
        heatmap_data = filtered_df.pivot_table(
            index='district',
            columns='year_month_str',
            values=selected_metric,
            aggfunc='mean'
        )
        
        fig_heatmap = px.imshow(
            heatmap_data,
            labels=dict(x="Month", y="District", color=selected_metric),
            color_continuous_scale='Reds',
            title=f"{selected_metric} Heatmap: Districts × Months"
        )
        fig_heatmap.update_layout(height=600)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Stress Quadrant Visualization
    st.subheader("Stress Quadrant Classification")
    
    if all(m in filtered_df.columns for m in ['ESS', 'MSP', 'stress_quadrant']):
        quadrant_df = filtered_df.groupby(['state', 'district']).agg({
            'ESS': 'mean',
            'MSP': 'mean',
            'stress_quadrant': 'first'
        }).reset_index()
        
        fig_quadrant = px.scatter(
            quadrant_df,
            x='ESS',
            y='MSP',
            color='stress_quadrant',
            hover_data=['state', 'district'],
            title="Stress Quadrants: ESS vs MSP"
        )
        
        # Add quadrant lines
        ess_median = quadrant_df['ESS'].median()
        msp_median = quadrant_df['MSP'].median()
        fig_quadrant.add_hline(y=msp_median, line_dash="dash", line_color="gray")
        fig_quadrant.add_vline(x=ess_median, line_dash="dash", line_color="gray")
        
        fig_quadrant.update_layout(height=500)
        st.plotly_chart(fig_quadrant, use_container_width=True)
    
    # Top & Bottom Stress Tables
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 High-Stress Districts")
        if 'AISI' in filtered_df.columns:
            # Use normalized names for clarity
            grp_cols = ['state_normalized', 'district_normalized'] if 'state_normalized' in filtered_df.columns else ['state', 'district']
            top_stress = (
                filtered_df
                .dropna(subset=[grp_cols[0], grp_cols[1], 'AISI'])
                .groupby(grp_cols)
                .agg({
                    'AISI': 'mean',
                    'ESS': 'mean',
                    'MSP': 'mean'
                })
                .reset_index()
                .nlargest(10, 'AISI')
            )
            top_stress = top_stress.rename(columns={grp_cols[0]: 'state', grp_cols[1]: 'district'})
            st.dataframe(top_stress, use_container_width=True)
    
    with col2:
        st.subheader("Top 10 Low-Stress Districts")
        if 'AISI' in filtered_df.columns:
            grp_cols = ['state_normalized', 'district_normalized'] if 'state_normalized' in filtered_df.columns else ['state', 'district']
            bottom_stress = (
                filtered_df
                .dropna(subset=[grp_cols[0], grp_cols[1], 'AISI'])
                .groupby(grp_cols)
                .agg({
                    'AISI': 'mean',
                    'ESS': 'mean',
                    'MSP': 'mean'
                })
                .reset_index()
                .nsmallest(10, 'AISI')
            )
            bottom_stress = bottom_stress.rename(columns={grp_cols[0]: 'state', grp_cols[1]: 'district'})
            st.dataframe(bottom_stress, use_container_width=True)
    
    # Early Warnings
    if 'early_warnings' in results and len(results['early_warnings']) > 0:
        st.subheader("Early Warning Districts")
        st.dataframe(results['early_warnings'], use_container_width=True)
    
    # Insights Section
    st.markdown("---")
    st.subheader("Insights & Policy Recommendations")
    
    # Present Findings
    st.markdown("### 🔴 WHAT DATA SHOWS (PRESENT)")
    
    if 'AISI' in filtered_df.columns:
        high_stress_count = len(filtered_df[filtered_df['AISI'] > 0.7])
        high_stress_pct = (high_stress_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
        st.info(f"**Critical Stress**: {high_stress_count} district-months ({high_stress_pct:.1f}%) show AISI > 0.7, "
               f"indicating critical stress requiring immediate intervention.")
    
    if 'ESS' in filtered_df.columns:
        high_ess = filtered_df[filtered_df['ESS'] > filtered_df['ESS'].quantile(0.75)]
        st.info(f"**Age-based Entry Delays**: {len(high_ess['district'].unique())} districts show ESS > 75th percentile "
               f"(mean ESS = {filtered_df['ESS'].mean():.3f}), indicating delayed adult enrollment.")
    
    if 'ESS' in filtered_df.columns and 'MSP' in filtered_df.columns:
        ess_msp_corr = filtered_df['ESS'].corr(filtered_df['MSP'])
        st.info(f"**Structural Relationship**: ESS-MSP correlation = {ess_msp_corr:.3f}. "
               f"{'Synergistic' if ess_msp_corr > 0.3 else 'Independent'} stress patterns observed.")
    
    if 'MSP' in filtered_df.columns and 'DPI' in filtered_df.columns:
        msp_dpi_corr = filtered_df['MSP'].corr(filtered_df['DPI'])
        st.info(f"**Demography-Linked Stress**: MSP-DPI correlation = {msp_dpi_corr:.3f}. "
               f"{'Strong' if abs(msp_dpi_corr) > 0.4 else 'Moderate'} link between aging demographics and biometric maintenance.")
    
    # Administrative Suggestions
    st.markdown("### 🟡 ADMINISTRATIVE SUGGESTIONS")
    
    if 'ESS' in filtered_df.columns:
        high_ess_districts = filtered_df[filtered_df['ESS'] > filtered_df['ESS'].quantile(0.75)]
        st.success(f"**Adult Enrolment Targeting**: Prioritize {len(high_ess_districts['district'].unique())} districts "
                  f"with ESS > 75th percentile. Deploy mobile enrollment units and awareness campaigns.")
    
    if 'YCR' in filtered_df.columns:
        low_ycr = filtered_df[filtered_df['YCR'] < filtered_df['YCR'].quantile(0.25)]
        st.success(f"**Early-life Integration**: Integrate Aadhaar enrollment with birth registration in "
                  f"{len(low_ycr['district'].unique())} low-YCR districts to prevent future enrollment backlog.")
    
    if 'MSP' in filtered_df.columns:
        high_msp = filtered_df[filtered_df['MSP'] > filtered_df['MSP'].quantile(0.75)]
        st.success(f"**Biometric Refresh**: Proactive biometric refresh campaigns in "
                  f"{len(high_msp['district'].unique())} high-MSP districts, especially for elderly populations.")
    
    # Future Risks
    st.markdown("### 🔮 NEAR-FUTURE RISKS (2-5 YEARS)")
    
    if 'DPI' in filtered_df.columns and 'MSP' in filtered_df.columns:
        aging_districts = filtered_df[filtered_df['DPI'] > filtered_df['DPI'].quantile(0.75)]
        if len(aging_districts) > 0:
            current_msp = aging_districts['MSP'].mean()
            st.warning(f"**Rising MSP in Aging Districts**: Districts with high DPI currently show MSP = {current_msp:.3f}. "
                      f"As population ages, biometric maintenance burden will escalate in 2-3 years.")
    
    if 'YCR' in filtered_df.columns:
        low_ycr_districts = filtered_df[filtered_df['YCR'] < filtered_df['YCR'].quantile(0.25)]
        st.warning(f"**Future Enrolment Shocks**: {len(low_ycr_districts['district'].unique())} districts with low YCR "
                  f"will face adult enrollment backlog as current youth cohort ages without Aadhaar (3-5 years).")
    
    if 'early_warnings' in results and len(results['early_warnings']) > 0:
        high_risk = results['early_warnings'][results['early_warnings']['risk_level'] == 'high']
        if len(high_risk) > 0:
            st.error(f"**Immediate Risk**: {len(high_risk)} districts approaching high-stress threshold. "
                    f"Authentication failure risk in 6-12 months without intervention.")


if __name__ == '__main__':
    main()
