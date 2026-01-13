"""
Main pipeline: orchestrates all steps.
Loads data, applies transformations, generates insights.
"""
import pandas as pd
import pickle
from pathlib import Path

from data_loader import load_all_datasets
from data_preparation import (
    aggregate_enrolment, aggregate_biometric, aggregate_demographic,
    apply_transformations
)
from feature_engineering import engineer_all_features
from analysis import univariate_analysis, bivariate_analysis, trivariate_temporal_analysis
from advanced_analytics import (
    stress_quadrant_classification, calculate_persistence_index,
    calculate_rank_volatility, detect_shocks
)
from composite_index import calculate_aisi
from forecasting import trend_extrapolation, rolling_window_projection, identify_early_warning_districts


def run_full_pipeline(base_path='.'):
    """Execute complete pipeline."""
    print("Loading data from ZIP files...")
    enrolment, biometric, demographic = load_all_datasets(base_path)
    
    print("Aggregating data...")
    enrol_state, enrol_district = aggregate_enrolment(enrolment)
    bio_state, bio_district = aggregate_biometric(biometric)
    demo_state, demo_district = aggregate_demographic(demographic)
    
    print("Engineering features...")
    df = engineer_all_features(enrol_district, bio_district, demo_district)
    
    print("Applying transformations...")
    value_cols = ['ESS', 'MSP', 'YCR', 'DPI', 'total_enrolments', 'biometric_updates']
    available_cols = [c for c in value_cols if c in df.columns]
    df = apply_transformations(df, available_cols, pop_col='total_population')
    
    print("Calculating AISI...")
    df, aisi_loadings = calculate_aisi(df)
    
    print("Advanced analytics...")
    df = stress_quadrant_classification(df)
    persistence = calculate_persistence_index(df, metric='AISI')
    volatility = calculate_rank_volatility(df, metric='AISI')
    shocks = detect_shocks(df, metric='AISI')
    
    print("Analysis...")
    univariate_insights = univariate_analysis(df)
    bivariate_corr, bivariate_rels = bivariate_analysis(df)
    trivariate_results = trivariate_temporal_analysis(df)
    
    print("Forecasting...")
    forecasts_trend = trend_extrapolation(df, metric='AISI', periods=6)
    forecasts_rolling = rolling_window_projection(df, metric='AISI', periods=3)
    early_warnings = identify_early_warning_districts(df, metric='AISI')
    
    # Save processed data
    output_dir = Path('processed_data')
    output_dir.mkdir(exist_ok=True)
    
    df.to_csv(output_dir / 'processed_data.csv', index=False)
    persistence.to_csv(output_dir / 'persistence_index.csv', index=False)
    volatility.to_csv(output_dir / 'rank_volatility.csv', index=False)
    shocks.to_csv(output_dir / 'shock_detection.csv', index=False)
    early_warnings.to_csv(output_dir / 'early_warnings.csv', index=False)
    
    # Save insights
    results = {
        'data': df,
        'persistence': persistence,
        'volatility': volatility,
        'shocks': shocks,
        'early_warnings': early_warnings,
        'univariate_insights': univariate_insights,
        'bivariate_correlations': bivariate_corr,
        'bivariate_relationships': bivariate_rels,
        'trivariate_results': trivariate_results,
        'aisi_loadings': aisi_loadings,
        'forecasts_trend': forecasts_trend,
        'forecasts_rolling': forecasts_rolling
    }
    
    with open(output_dir / 'results.pkl', 'wb') as f:
        pickle.dump(results, f)
    
    print("Pipeline complete! Data saved to processed_data/")
    return results


if __name__ == '__main__':
    results = run_full_pipeline()
