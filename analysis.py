"""
Univariate, bivariate, and trivariate analysis with insights.
Data-backed insights, not descriptive fluff.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def univariate_analysis(df, metrics=['ESS', 'MSP', 'YCR', 'DPI']):
    """
    Distribution analysis with insights.
    Returns insights dict and plots data.
    """
    insights = {}
    
    for metric in metrics:
        if metric not in df.columns:
            continue
        
        values = df[metric].dropna()
        
        # Basic stats
        mean_val = values.mean()
        median_val = values.median()
        std_val = values.std()
        skew_val = stats.skew(values)
        
        # Outliers (IQR method)
        Q1 = values.quantile(0.25)
        Q3 = values.quantile(0.75)
        IQR = Q3 - Q1
        outliers = values[(values < Q1 - 1.5*IQR) | (values > Q3 + 1.5*IQR)]
        outlier_pct = len(outliers) / len(values) * 100
        
        # Long tail detection
        tail_threshold = values.quantile(0.95)
        tail_pct = (values > tail_threshold).sum() / len(values) * 100
        
        insights[metric] = {
            'mean': mean_val,
            'median': median_val,
            'std': std_val,
            'skewness': skew_val,
            'outlier_percentage': outlier_pct,
            'tail_percentage': tail_pct,
            'interpretation': generate_univariate_insight(metric, mean_val, median_val, skew_val, outlier_pct, tail_pct)
        }
    
    return insights


def generate_univariate_insight(metric, mean, median, skew, outlier_pct, tail_pct):
    """Generate human-readable insight."""
    if metric == 'ESS':
        if mean > 0.5:
            return f"High ESS (mean={mean:.2f}) indicates widespread delayed identity entry. {outlier_pct:.1f}% districts are extreme outliers."
        else:
            return f"Moderate ESS (mean={mean:.2f}) suggests most enrollments happen early, but {outlier_pct:.1f}% districts need attention."
    
    elif metric == 'MSP':
        if mean > 0.3:
            return f"High MSP (mean={mean:.2f}) signals significant biometric maintenance burden. Skewness={skew:.2f} shows concentration in few districts."
        else:
            return f"Low MSP (mean={mean:.2f}) indicates stable biometrics, but {outlier_pct:.1f}% districts face update stress."
    
    elif metric == 'YCR':
        if mean > 0.4:
            return f"Good YCR (mean={mean:.2f}) shows early-life inclusion. {tail_pct:.1f}% districts in top 5% need replication."
        else:
            return f"Low YCR (mean={mean:.2f}) indicates delayed youth enrollment. Policy intervention needed."
    
    elif metric == 'DPI':
        return f"DPI (mean={mean:.2f}) reflects demographic pressure. Skew={skew:.2f} indicates uneven aging patterns."
    
    return "Analysis complete."


def bivariate_analysis(df):
    """
    Structural relationships between metrics.
    Returns correlation matrix and relationship insights.
    """
    metrics = ['ESS', 'MSP', 'YCR', 'DPI']
    available_metrics = [m for m in metrics if m in df.columns]
    
    if len(available_metrics) < 2:
        return {}, {}
    
    # Correlation matrix
    corr_matrix = df[available_metrics].corr()
    
    # Key relationships
    relationships = {}
    
    if 'ESS' in df.columns and 'MSP' in df.columns:
        ess_msp_corr = df['ESS'].corr(df['MSP'])
        relationships['ESS_vs_MSP'] = {
            'correlation': ess_msp_corr,
            'insight': f"ESS-MSP correlation ({ess_msp_corr:.2f}) suggests {'synergistic' if ess_msp_corr > 0.3 else 'independent'} stress patterns."
        }
    
    if 'ESS' in df.columns and 'YCR' in df.columns:
        ess_ycr_corr = df['ESS'].corr(df['YCR'])
        relationships['ESS_vs_YCR'] = {
            'correlation': ess_ycr_corr,
            'insight': f"ESS-YCR correlation ({ess_ycr_corr:.2f}) indicates {'trade-off' if ess_ycr_corr < -0.3 else 'complementary'} between adult and youth enrollment."
        }
    
    if 'MSP' in df.columns and 'DPI' in df.columns:
        msp_dpi_corr = df['MSP'].corr(df['DPI'])
        relationships['MSP_vs_DPI'] = {
            'correlation': msp_dpi_corr,
            'insight': f"MSP-DPI correlation ({msp_dpi_corr:.2f}) shows {'strong' if abs(msp_dpi_corr) > 0.4 else 'weak'} link between demographics and biometric stress."
        }
    
    return corr_matrix, relationships


def trivariate_temporal_analysis(df):
    """
    District × Time × Stress analysis.
    Identifies structural vs temporary stress.
    """
    if 'ESS' not in df.columns or 'MSP' not in df.columns:
        return {}
    
    # Convert year_month to numeric for analysis
    df = df.copy()
    df['time_numeric'] = df['year_month'].astype(str).str.replace('-', '').astype(int)
    
    # Stress evolution
    district_stress = df.groupby(['state', 'district']).agg({
        'ESS': ['mean', 'std', 'max'],
        'MSP': ['mean', 'std', 'max'],
        'year_month': 'count'
    }).reset_index()
    
    district_stress.columns = ['state', 'district', 'ESS_mean', 'ESS_std', 'ESS_max', 
                               'MSP_mean', 'MSP_std', 'MSP_max', 'months_observed']
    
    # Classify stress patterns
    district_stress['stress_type'] = 'stable'
    district_stress.loc[
        (district_stress['ESS_mean'] > 0.5) & (district_stress['ESS_std'] < 0.1),
        'stress_type'
    ] = 'structural_entry_stress'
    district_stress.loc[
        (district_stress['MSP_mean'] > 0.3) & (district_stress['MSP_std'] < 0.1),
        'stress_type'
    ] = 'structural_maintenance_stress'
    district_stress.loc[
        (district_stress['ESS_std'] > 0.2) | (district_stress['MSP_std'] > 0.2),
        'stress_type'
    ] = 'volatile_stress'
    
    return district_stress
