"""
Forecasting and early warning using simple, explainable methods.
Trend extrapolation, rolling-window projections, stress momentum.
"""
import pandas as pd
import numpy as np
from scipy import stats


def trend_extrapolation(df, metric='ESS', periods=6):
    """
    Simple linear trend extrapolation.
    Fits trend to recent data and projects forward.
    """
    df = df.copy()
    df = df.sort_values(['state', 'district', 'year_month'])
    
    forecasts = []
    
    for (state, district), group in df.groupby(['state', 'district']):
        if metric not in group.columns:
            continue
        
        values = group[metric].dropna()
        if len(values) < 3:  # Need minimum data
            continue
        
        # Convert year_month to numeric for regression
        time_numeric = np.arange(len(values))
        
        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(time_numeric, values)
        
        # Project forward
        future_times = np.arange(len(values), len(values) + periods)
        future_values = intercept + slope * future_times
        
        # Store forecast
        last_month = group['year_month'].iloc[-1]
        for i, future_val in enumerate(future_values):
            forecasts.append({
                'state': state,
                'district': district,
                'forecast_period': i + 1,
                'forecast_value': max(0, future_val),  # No negative values
                'trend_slope': slope,
                'trend_strength': abs(r_value)
            })
    
    return pd.DataFrame(forecasts)


def rolling_window_projection(df, metric='ESS', window=6, periods=3):
    """
    Project based on recent rolling average and momentum.
    """
    df = df.copy()
    df = df.sort_values(['state', 'district', 'year_month'])
    
    projections = []
    
    for (state, district), group in df.groupby(['state', 'district']):
        if metric not in group.columns:
            continue
        
        values = group[metric].dropna()
        if len(values) < window:
            continue
        
        # Recent average and momentum
        recent_avg = values.tail(window).mean()
        recent_momentum = values.tail(2).diff().iloc[-1] if len(values) >= 2 else 0
        
        # Project forward with momentum decay
        for i in range(periods):
            projected = recent_avg + recent_momentum * (0.8 ** i)  # Momentum decays
            projections.append({
                'state': state,
                'district': district,
                'forecast_period': i + 1,
                'forecast_value': max(0, projected),
                'method': 'rolling_momentum'
            })
    
    return pd.DataFrame(projections)


def identify_early_warning_districts(df, metric='AISI', threshold=0.7, lookback=3):
    """
    Identify districts likely to enter high-stress zone.
    Based on recent trend and current level.
    """
    df = df.copy()
    df = df.sort_values(['state', 'district', 'year_month'])
    
    warnings = []
    
    for (state, district), group in df.groupby(['state', 'district']):
        if metric not in group.columns:
            continue
        
        values = group[metric].dropna()
        if len(values) < lookback:
            continue
        
        recent_values = values.tail(lookback)
        current_value = recent_values.iloc[-1]
        
        # Calculate trend
        if len(recent_values) >= 2:
            trend = (recent_values.iloc[-1] - recent_values.iloc[0]) / len(recent_values)
        else:
            trend = 0
        
        # Warning if approaching threshold or accelerating
        if current_value > threshold * 0.8 or (current_value > threshold * 0.6 and trend > 0.01):
            warnings.append({
                'state': state,
                'district': district,
                'current_value': current_value,
                'trend': trend,
                'risk_level': 'high' if current_value > threshold * 0.9 else 'medium',
                'months_to_threshold': max(1, int((threshold - current_value) / (trend + 0.001)))
            })
    
    return pd.DataFrame(warnings)
