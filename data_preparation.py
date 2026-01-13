"""
Data preparation with all required transformations.
Aggregates at state-month and district-month levels.
"""
import pandas as pd
import numpy as np
from datetime import datetime


def parse_dates(df, date_col='date'):
    """Parse date column and extract year, month."""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], format='%d-%m-%Y', errors='coerce')
    df['year'] = df[date_col].dt.year
    df['month'] = df[date_col].dt.month
    df['year_month'] = df[date_col].dt.to_period('M')
    return df


def aggregate_enrolment(enrolment_df):
    """Aggregate enrolment data at state-month and district-month."""
    df = parse_dates(enrolment_df)
    
    # Calculate total enrolments (handle column name variations)
    age_18_col = 'age_18_greater' if 'age_18_greater' in df.columns else 'age_18_plus'
    if age_18_col not in df.columns:
        age_18_col = None
    
    if age_18_col:
        df['total_enrolments'] = df['age_0_5'] + df['age_5_17'] + df[age_18_col]
    else:
        df['total_enrolments'] = df['age_0_5'] + df['age_5_17']
    
    # State-month aggregation
    agg_cols = {
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'total_enrolments': 'sum'
    }
    age_18_col = 'age_18_greater' if 'age_18_greater' in df.columns else 'age_18_plus'
    if age_18_col in df.columns:
        agg_cols[age_18_col] = 'sum'
    
    state_month = df.groupby(['state', 'year_month']).agg(agg_cols).reset_index()
    if age_18_col and age_18_col not in state_month.columns:
        state_month[age_18_col] = 0
    
    # District-month aggregation
    district_month = df.groupby(['state', 'district', 'year_month']).agg(agg_cols).reset_index()
    if age_18_col and age_18_col not in district_month.columns:
        district_month[age_18_col] = 0
    
    # Standardize column name
    if 'age_18_greater' in state_month.columns:
        state_month['age_18_greater'] = state_month.get('age_18_greater', 0)
        district_month['age_18_greater'] = district_month.get('age_18_greater', 0)
    elif 'age_18_plus' in state_month.columns:
        state_month['age_18_greater'] = state_month['age_18_plus']
        district_month['age_18_greater'] = district_month['age_18_plus']
    else:
        state_month['age_18_greater'] = 0
        district_month['age_18_greater'] = 0
    
    return state_month, district_month


def aggregate_biometric(biometric_df):
    """Aggregate biometric update data."""
    df = parse_dates(biometric_df)
    
    # Total biometric updates
    df['biometric_updates'] = df['bio_age_5_17'] + df['bio_age_17_']
    
    state_month = df.groupby(['state', 'year_month']).agg({
        'biometric_updates': 'sum'
    }).reset_index()
    
    district_month = df.groupby(['state', 'district', 'year_month']).agg({
        'biometric_updates': 'sum'
    }).reset_index()
    
    return state_month, district_month


def aggregate_demographic(demographic_df):
    """Aggregate demographic data for normalization."""
    df = parse_dates(demographic_df)
    
    # Total population proxy
    df['total_population'] = df['demo_age_5_17'] + df['demo_age_17_']
    
    state_month = df.groupby(['state', 'year_month']).agg({
        'demo_age_5_17': 'sum',
        'demo_age_17_': 'sum',
        'total_population': 'sum'
    }).reset_index()
    
    district_month = df.groupby(['state', 'district', 'year_month']).agg({
        'demo_age_5_17': 'sum',
        'demo_age_17_': 'sum',
        'total_population': 'sum'
    }).reset_index()
    
    return state_month, district_month


def apply_transformations(df, value_cols, pop_col=None):
    """
    Apply all required transformations:
    - Log transform for skewed counts
    - Rolling averages (3 & 6 months)
    - Min-max scaling
    - Per-capita normalization
    - Z-score deviation
    - Lag features
    - Rate-of-change
    """
    df = df.copy()
    
    # Ensure we have required columns for grouping
    group_cols = []
    if 'state' in df.columns:
        group_cols.append('state')
    if 'district' in df.columns:
        group_cols.append('district')
    if 'year_month' in df.columns:
        group_cols.append('year_month')
    
    if group_cols:
        df = df.sort_values(group_cols).reset_index(drop=True)
    
    for col in value_cols:
        if col not in df.columns:
            continue
        
        # Log transform to handle skewness
        df[f'{col}_log'] = np.log1p(df[col].fillna(0))
        
        # Per-capita normalization if population available
        if pop_col and pop_col in df.columns:
            df[f'{col}_per_capita'] = df[col] / (df[pop_col] + 1)  # +1 to avoid div by zero
        
        # Rolling averages to suppress noise (only if we have grouping)
        if len(group_cols) >= 2:  # Need at least state and district
            grouping = group_cols[:-1]  # Exclude year_month for grouping
            df[f'{col}_rolling_3m'] = df.groupby(grouping)[col].transform(
                lambda x: x.rolling(window=3, min_periods=1).mean()
            )
            df[f'{col}_rolling_6m'] = df.groupby(grouping)[col].transform(
                lambda x: x.rolling(window=6, min_periods=1).mean()
            )
            
            # Lag features (previous month)
            df[f'{col}_lag1'] = df.groupby(grouping)[col].shift(1)
            
            # Rate of change / momentum
            df[f'{col}_roc'] = df.groupby(grouping)[col].pct_change()
            df[f'{col}_momentum'] = df[col] - df[f'{col}_lag1'].fillna(0)
    
    # Min-max scaling for cross-region comparability
    for col in value_cols:
        if col not in df.columns:
            continue
        col_min = df[col].min()
        col_max = df[col].max()
        if col_max > col_min:
            df[f'{col}_scaled'] = (df[col] - col_min) / (col_max - col_min)
    
    # Z-score deviation from national mean (inequality detection)
    for col in value_cols:
        if col not in df.columns:
            continue
        national_mean = df[col].mean()
        national_std = df[col].std()
        if national_std > 0:
            df[f'{col}_zscore'] = (df[col] - national_mean) / national_std
    
    return df
