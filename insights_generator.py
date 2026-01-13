"""
Generate structured insights, suggestions, and future risk analysis.
Judge-ready insights that demonstrate policy understanding.
"""
import pandas as pd
import numpy as np


def generate_insights(results):
    """
    Generate all three categories of insights:
    1. WHAT DATA SHOWS (PRESENT)
    2. ADMINISTRATIVE SUGGESTIONS
    3. NEAR-FUTURE RISKS (2-5 YEARS)
    """
    df = results['data']
    persistence = results['persistence']
    early_warnings = results['early_warnings']
    univariate = results['univariate_insights']
    
    insights = {
        'present_findings': generate_present_insights(df, univariate, persistence),
        'administrative_suggestions': generate_administrative_suggestions(df, persistence, early_warnings),
        'future_risks': generate_future_risks(df, results['forecasts_trend'], early_warnings)
    }
    
    return insights


def generate_present_insights(df, univariate, persistence):
    """WHAT DATA SHOWS (PRESENT)"""
    insights = []
    
    # Age-based entry delays
    if 'ESS' in df.columns:
        high_ess_districts = df[df['ESS'] > df['ESS'].quantile(0.75)]
        insights.append({
            'category': 'Age-based Entry Delays',
            'finding': f"{len(high_ess_districts['district'].unique())} districts show ESS > 75th percentile, "
                      f"indicating delayed adult enrollment. Mean ESS = {df['ESS'].mean():.3f}.",
            'evidence': f"Top 10 districts by ESS: {', '.join(high_ess_districts.groupby('district')['ESS'].mean().nlargest(10).index.tolist())}"
        })
    
    # Demography-linked biometric stress
    if 'MSP' in df.columns and 'DPI' in df.columns:
        msp_dpi_corr = df['MSP'].corr(df['DPI'])
        insights.append({
            'category': 'Demography-Linked Biometric Stress',
            'finding': f"MSP-DPI correlation = {msp_dpi_corr:.3f}. "
                      f"{'Strong' if abs(msp_dpi_corr) > 0.4 else 'Moderate'} link between aging demographics and biometric maintenance burden.",
            'evidence': f"Districts with DPI > 0.6 have mean MSP = {df[df['DPI'] > 0.6]['MSP'].mean():.3f} vs national mean = {df['MSP'].mean():.3f}"
        })
    
    # Persistent vs temporary stress
    if len(persistence) > 0:
        high_persistence = persistence[persistence['persistence_index'] > 0.5]
        insights.append({
            'category': 'Persistent vs Temporary Stress',
            'finding': f"{len(high_persistence)} districts show >50% persistence in top stress quartile, "
                      f"indicating structural problems, not temporary spikes.",
            'evidence': f"Mean persistence = {persistence['persistence_index'].mean():.2%}, "
                      f"max = {persistence['persistence_index'].max():.2%}"
        })
    
    return insights


def generate_administrative_suggestions(df, persistence, early_warnings):
    """ADMINISTRATIVE SUGGESTIONS"""
    suggestions = []
    
    # Adult enrolment targeting
    if 'ESS' in df.columns:
        high_ess = df[df['ESS'] > df['ESS'].quantile(0.75)]
        suggestions.append({
            'area': 'Adult Enrolment Targeting',
            'suggestion': f"Prioritize {len(high_ess['district'].unique())} districts with ESS > 75th percentile. "
                         f"Deploy mobile enrollment units and awareness campaigns.",
            'rationale': 'High ESS indicates delayed identity acquisition, creating exclusion risk.'
        })
    
    # Early-life Aadhaar integration
    if 'YCR' in df.columns:
        low_ycr = df[df['YCR'] < df['YCR'].quantile(0.25)]
        suggestions.append({
            'area': 'Early-life Aadhaar Integration',
            'suggestion': f"Integrate Aadhaar enrollment with birth registration in {len(low_ycr['district'].unique())} low-YCR districts.",
            'rationale': 'Low YCR means delayed youth enrollment, increasing future ESS burden.'
        })
    
    # Biometric refresh strategies
    if 'MSP' in df.columns:
        high_msp = df[df['MSP'] > df['MSP'].quantile(0.75)]
        suggestions.append({
            'area': 'Biometric Refresh Strategies',
            'suggestion': f"Proactive biometric refresh campaigns in {len(high_msp['district'].unique())} high-MSP districts, "
                         f"especially for elderly populations.",
            'rationale': 'High MSP indicates authentication friction and potential failure risk.'
        })
    
    # Resource prioritization
    if len(persistence) > 0:
        top_persistent = persistence.nlargest(20, 'persistence_index')
        suggestions.append({
            'area': 'Resource Prioritization',
            'suggestion': f"Allocate resources to top 20 persistent-stress districts (persistence > {top_persistent['persistence_index'].min():.2%}). "
                         f"These require sustained intervention, not one-time campaigns.",
            'rationale': 'Persistence index identifies structural problems requiring long-term solutions.'
        })
    
    return suggestions


def generate_future_risks(df, forecasts, early_warnings):
    """NEAR-FUTURE RISKS (2-5 YEARS)"""
    risks = []
    
    # Rising MSP in aging districts
    if 'DPI' in df.columns and 'MSP' in df.columns:
        aging_districts = df[df['DPI'] > df['DPI'].quantile(0.75)]
        if len(aging_districts) > 0:
            current_msp = aging_districts['MSP'].mean()
            risks.append({
                'risk': 'Rising MSP in Aging Districts',
                'description': f"Districts with high DPI (elderly share) currently show MSP = {current_msp:.3f}. "
                              f"As population ages, biometric maintenance burden will escalate.",
                'timeframe': '2-3 years',
                'mitigation': 'Proactive biometric refresh programs before failure rates spike.'
            })
    
    # Future enrolment shocks
    if 'YCR' in df.columns:
        low_ycr_districts = df[df['YCR'] < df['YCR'].quantile(0.25)]
        risks.append({
            'risk': 'Future Enrolment Shocks',
            'description': f"{len(low_ycr_districts['district'].unique())} districts with low YCR will face "
                          f"adult enrollment backlog as current youth cohort ages without Aadhaar.",
            'timeframe': '3-5 years',
            'mitigation': 'Immediate youth enrollment drive to prevent future ESS spike.'
        })
    
    # Cost & failure risks
    if len(early_warnings) > 0:
        high_risk = early_warnings[early_warnings['risk_level'] == 'high']
        risks.append({
            'risk': 'Authentication Failure Risk',
            'description': f"{len(high_risk)} districts approaching high-stress threshold. "
                          f"Without intervention, authentication failures will increase, "
                          f"creating service delivery friction.",
            'timeframe': '6-12 months',
            'mitigation': 'Immediate targeted intervention in early-warning districts.'
        })
    
    return risks
