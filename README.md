# Aadhaar Identity Stress Early-Warning & Policy Intelligence System

A policy-grade decision support system for identifying and predicting Aadhaar enrollment and maintenance stress across Indian districts.

## Overview

This system treats Aadhaar as a life-cycle identity system, analyzing signals of:
- Delayed identity entry
- Biometric instability over age
- Administrative access friction
- Long-term exclusion risk

**This is NOT a visualization project. This is an early-warning + intervention prioritization system.**

## Project Structure

```
.
├── data_loader.py              # Load ZIP files, extract CSVs in-memory
├── data_preparation.py         # Aggregation, transformations
├── feature_engineering.py      # ESS, MSP, YCR, DPI calculation
├── analysis.py                 # Univariate, bivariate, trivariate analysis
├── advanced_analytics.py       # Stress quadrants, persistence, volatility, shocks
├── composite_index.py          # AISI calculation using PCA
├── forecasting.py              # Early warning and trend projection
├── insights_generator.py       # Structured insights and recommendations
├── main_pipeline.py            # Orchestrates entire pipeline
├── app.py                      # Streamlit dashboard
├── requirements.txt            # Python dependencies
└── processed_data/             # Output directory (created after running pipeline)
```

## Core Metrics

### ESS (Entry Stress Score)
- **Formula**: `age_18_plus / total_enrolments`
- **Interpretation**: Higher ESS = delayed identity acquisition

### MSP (Maintenance Stress Proxy)
- **Formula**: `biometric_updates / total_enrolments`
- **Interpretation**: Higher MSP = biometric instability / authentication friction

### YCR (Youth Coverage Ratio)
- **Formula**: `(age_0_5 + age_5_17) / total_enrolments`
- **Interpretation**: Higher YCR = early-life inclusion indicator

### DPI (Demographic Pressure Index)
- **Components**: Elderly share, population growth rate
- **Interpretation**: Aging populations need more biometric updates; high density = administrative friction

### AISI (Aadhaar Identity Stress Index)
- **Method**: PCA-based composite index (0-1 normalized)
- **Purpose**: Unsupervised aggregation to avoid subjective weighting

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure ZIP files are in project root:
- `api_data_aadhar_enrolment.zip`
- `api_data_aadhar_biometric.zip`
- `api_data_aadhar_demographic.zip`

## Usage

### Step 1: Run Data Pipeline

```bash
python main_pipeline.py
```

This will:
- Load all ZIP files and extract CSVs
- Aggregate at state-month and district-month levels
- Apply all transformations (log, rolling, scaling, per-capita, z-scores, lags, rates)
- Calculate ESS, MSP, YCR, DPI
- Compute AISI using PCA
- Perform advanced analytics (stress quadrants, persistence, volatility, shocks)
- Generate forecasts and early warnings
- Save processed data to `processed_data/`

### Step 2: Launch Dashboard

```bash
streamlit run app.py
```

The dashboard includes:
- **KPI Cards**: Mean ESS, MSP, AISI, Total Enrolments
- **India Heatmap**: State-level visualization of selected metric
- **Time-Series Trends**: District-level trends over time
- **ESS vs MSP Scatter**: Colored by AISI
- **District × Month Heatmap**: Temporal patterns
- **Stress Quadrant Visualization**: Classification of districts
- **Top/Bottom Stress Tables**: Rankings
- **Early Warning Districts**: Risk identification
- **Insights & Recommendations**: Present findings, administrative suggestions, future risks

## Key Features

### Data Transformations
- Log transform for skewed counts
- Rolling averages (3 & 6 months)
- Min-max scaling
- Per-capita normalization
- Z-score deviation from national mean
- Lag features (previous month)
- Rate-of-change / momentum

### Advanced Analytics
- **Stress Quadrant Classification**: Stable, Entry-only, Maintenance-only, Critical dual
- **Persistence Index**: % of months in top stress quartile
- **Rank Volatility**: Frequency of rank changes
- **Shock Detection**: Synchronized spikes across regions

### Forecasting
- Trend extrapolation (linear regression)
- Rolling-window projections with momentum
- Early warning identification (districts approaching high-stress threshold)

## Insights Structure

### 🔴 WHAT DATA SHOWS (PRESENT)
- Age-based entry delays
- Demography-linked biometric stress
- Persistent vs temporary stress regions

### 🟡 ADMINISTRATIVE SUGGESTIONS
- Adult enrolment targeting
- Early-life Aadhaar integration
- Biometric refresh strategies
- Resource prioritization via persistence score

### 🔮 NEAR-FUTURE RISKS (2-5 YEARS)
- Rising MSP in aging districts
- Future enrolment shocks due to low YCR
- Cost & failure risks if no intervention

## Code Philosophy

- **Practical**: No over-engineering
- **Human-written style**: Slightly imperfect, short comments explaining why
- **No fancy abstractions**: Direct, readable code
- **No unnecessary frameworks**: Uses standard libraries

## Output Files

After running the pipeline, `processed_data/` contains:
- `processed_data.csv`: Main dataset with all features
- `persistence_index.csv`: District persistence scores
- `rank_volatility.csv`: Rank change volatility
- `shock_detection.csv`: Detected shock months
- `early_warnings.csv`: Early warning districts
- `results.pkl`: Complete results object (for dashboard)

## Notes

- All data loading is in-memory from ZIP files
- No manual preprocessing required
- ZIP files are treated as authoritative data sources
- System handles missing data gracefully
- Dashboard is interactive and filterable by state, district, date range, and metric

## License

This project is developed for a national-level data analytics hackathon.
