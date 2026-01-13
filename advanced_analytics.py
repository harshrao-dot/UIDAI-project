"""
Advanced analytics: stress quadrants, persistence, volatility, shock detection.
"""
import pandas as pd
import numpy as np


def stress_quadrant_classification(df):
    """
    Classify districts into stress quadrants:
    - Stable: Low ESS, Low MSP
    - Entry-only stress: High ESS, Low MSP
    - Maintenance-only stress: Low ESS, High MSP
    - Critical dual stress: High ESS, High MSP
    """
    df = df.copy()
    
    if 'ESS' not in df.columns or 'MSP' not in df.columns:
        return df
    
    # Use medians as thresholds
    ess_median = df['ESS'].median()
    msp_median = df['MSP'].median()
    
    df['stress_quadrant'] = 'stable'
    df.loc[
        (df['ESS'] > ess_median) & (df['MSP'] <= msp_median),
        'stress_quadrant'
    ] = 'entry_only_stress'
    df.loc[
        (df['ESS'] <= ess_median) & (df['MSP'] > msp_median),
        'stress_quadrant'
    ] = 'maintenance_only_stress'
    df.loc[
        (df['ESS'] > ess_median) & (df['MSP'] > msp_median),
        'stress_quadrant'
    ] = 'critical_dual_stress'
    
    return df


def calculate_persistence_index(df, metric='ESS', top_quartile=True):
    """
    % of months district remains in top stress quartile.
    Higher persistence = structural problem, not temporary.
    """
    df = df.copy()
    
    if metric not in df.columns:
        return pd.DataFrame()
    
    # Calculate quartile threshold
    threshold = df[metric].quantile(0.75) if top_quartile else df[metric].quantile(0.25)
    
    # Mark high stress months
    df['high_stress'] = df[metric] > threshold
    
    # Calculate persistence
    persistence = df.groupby(['state', 'district']).agg({
        'high_stress': 'mean',  # Percentage of months in high stress
        'year_month': 'count'  # Total months observed
    }).reset_index()
    
    persistence.columns = ['state', 'district', 'persistence_index', 'total_months']
    
    return persistence


def calculate_rank_volatility(df, metric='ESS'):
    """
    How often district/state rank changes.
    High volatility = unstable, low volatility = entrenched inequality.
    """
    df = df.copy()
    
    if metric not in df.columns:
        return pd.DataFrame()
    
    # Calculate ranks per month
    df['rank'] = df.groupby('year_month')[metric].rank(ascending=False, method='dense')
    
    # Rank changes (month-over-month)
    df = df.sort_values(['state', 'district', 'year_month'])
    df['rank_change'] = df.groupby(['state', 'district'])['rank'].diff().abs()
    
    # Volatility = average rank change
    volatility = df.groupby(['state', 'district']).agg({
        'rank_change': 'mean',
        'rank': ['min', 'max', 'mean']
    }).reset_index()
    
    volatility.columns = ['state', 'district', 'rank_volatility', 'min_rank', 'max_rank', 'avg_rank']
    
    return volatility


def detect_shocks(df, metric='ESS', threshold_std=2.0):
    """
    Sudden synchronized spikes across regions.
    Detects systemic shocks vs local issues.
    """
    df = df.copy()
    
    if metric not in df.columns:
        return pd.DataFrame()
    
    # Calculate monthly national average
    monthly_avg = df.groupby('year_month')[metric].mean().reset_index()
    monthly_avg.columns = ['year_month', 'national_avg']
    
    # Calculate standard deviation
    monthly_std = df.groupby('year_month')[metric].std().reset_index()
    monthly_std.columns = ['year_month', 'national_std']
    
    monthly_stats = monthly_avg.merge(monthly_std, on='year_month')
    
    # Detect shock months (high average + high std = synchronized spike)
    monthly_stats['shock_score'] = (
        (monthly_stats['national_avg'] - monthly_stats['national_avg'].mean()) / monthly_stats['national_avg'].std() +
        (monthly_stats['national_std'] - monthly_stats['national_std'].mean()) / monthly_stats['national_std'].std()
    )
    
    monthly_stats['is_shock'] = monthly_stats['shock_score'] > threshold_std
    
    return monthly_stats
