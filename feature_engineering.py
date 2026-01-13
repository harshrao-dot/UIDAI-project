"""
Core signal engineering: ESS, MSP, YCR, DPI
These are the foundation metrics for stress detection.
"""
import pandas as pd
import numpy as np


def calculate_ess(df):
    """
    Entry Stress Score (ESS)
    ESS = age_18_plus / total_enrolments
    Higher ESS = delayed identity acquisition
    """
    df = df.copy()
    # Handle column name variations
    age_18_col = 'age_18_greater' if 'age_18_greater' in df.columns else 'age_18_plus'
    if age_18_col not in df.columns:
        df['ESS'] = 0
        return df
    
    df['ESS'] = np.where(
        df['total_enrolments'] > 0,
        df[age_18_col] / df['total_enrolments'],
        0
    )
    return df


def calculate_msp(df):
    """
    Maintenance Stress Proxy (MSP)
    MSP = biometric_updates / total_enrolments
    Higher MSP = biometric instability / authentication friction
    """
    df = df.copy()
    # Merge biometric data if not already present
    if 'biometric_updates' not in df.columns:
        return df
    
    df['MSP'] = np.where(
        df['total_enrolments'] > 0,
        df['biometric_updates'] / (df['total_enrolments'] + 1),  # +1 to avoid extreme values
        0
    )
    return df


def calculate_ycr(df):
    """
    Youth Coverage Ratio (YCR)
    YCR = (age_0_5 + age_5_17) / total_enrolments
    Higher YCR = early-life inclusion indicator
    """
    df = df.copy()
    df['YCR'] = np.where(
        df['total_enrolments'] > 0,
        (df['age_0_5'] + df['age_5_17']) / df['total_enrolments'],
        0
    )
    return df


def calculate_dpi(df, demo_df):
    """
    Demographic Pressure Index (DPI)
    Derived from elderly population share, urban density, population growth
    DPI modifies Aadhaar stress because:
    - Aging populations need more biometric updates
    - High density = administrative friction
    - Growth = enrollment backlog risk
    """
    df = df.copy()
    
    # Check if demo_df has required columns
    required_cols = ['state', 'district', 'year_month', 'demo_age_17_', 'total_population']
    available_cols = [c for c in required_cols if c in demo_df.columns]
    
    if len(available_cols) < 4:  # Need at least state, district, year_month, and one demo column
        # Fallback: use enrollment data to estimate
        df['elderly_share'] = np.where(
            df['total_enrolments'] > 0,
            df['age_18_greater'] / df['total_enrolments'],
            0
        )
        df['pop_growth'] = 0  # Can't calculate without demographic data
        df['DPI'] = df['elderly_share']  # Simplified DPI
        return df
    
    # Merge demographic data
    merge_cols = ['state', 'district', 'year_month']
    demo_cols = [c for c in ['demo_age_17_', 'total_population'] if c in demo_df.columns]
    
    merged = df.merge(
        demo_df[merge_cols + demo_cols],
        on=merge_cols,
        how='left'
    )
    
    # Fill missing demographic data
    if 'total_population' not in merged.columns:
        merged['total_population'] = merged.get('total_enrolments', 0)
    if 'demo_age_17_' not in merged.columns:
        merged['demo_age_17_'] = merged.get('age_18_greater', 0)
    
    # Elderly share (using 17+ as proxy for adult/elderly)
    # Fallback to enrollment data if demographic not available
    if 'demo_age_17_' not in merged.columns:
        age_18_col = 'age_18_greater' if 'age_18_greater' in merged.columns else 'age_18_plus'
        if age_18_col in merged.columns:
            merged['demo_age_17_'] = merged[age_18_col]
        else:
            merged['demo_age_17_'] = 0
    
    merged['elderly_share'] = np.where(
        merged['total_population'] > 0,
        merged['demo_age_17_'] / merged['total_population'],
        0
    )
    
    # Population growth rate (month-over-month)
    merged = merged.sort_values(['state', 'district', 'year_month'])
    merged['pop_growth'] = merged.groupby(['state', 'district'])['total_population'].pct_change(fill_method=None)
    merged['pop_growth'] = merged['pop_growth'].fillna(0)
    
    # DPI: combination of elderly share and growth pressure
    # Higher elderly = more maintenance stress
    # Higher growth = enrollment backlog risk
    merged['DPI'] = (
        0.6 * merged['elderly_share'] +  # Aging pressure
        0.4 * np.clip(merged['pop_growth'], 0, 1)  # Growth pressure (clipped)
    )
    
    return merged


def engineer_all_features(enrolment_agg, biometric_agg, demographic_agg):
    """Combine all datasets and calculate all features."""
    # Merge enrolment and biometric at district-month level
    df = enrolment_agg.merge(
        biometric_agg,
        on=['state', 'district', 'year_month'],
        how='outer'
    )
    
    # Fill missing values
    df['biometric_updates'] = df['biometric_updates'].fillna(0)
    df['total_enrolments'] = df['total_enrolments'].fillna(0)
    df['age_0_5'] = df['age_0_5'].fillna(0)
    df['age_5_17'] = df['age_5_17'].fillna(0)
    df['age_18_greater'] = df['age_18_greater'].fillna(0)
    
    # Calculate core signals
    df = calculate_ess(df)
    df = calculate_msp(df)
    df = calculate_ycr(df)
    df = calculate_dpi(df, demographic_agg)
    
    return df
