# Quick Start Guide

## Prerequisites
- Python 3.8+
- ZIP files in project root:
  - `api_data_aadhar_enrolment.zip`
  - `api_data_aadhar_biometric.zip`
  - `api_data_aadhar_demographic.zip`

## Installation

```bash
pip install -r requirements.txt
```

## Running the System

### Option 1: Full Pipeline with Insights (Recommended)

```bash
python run_pipeline.py
```

This will:
- Process all data
- Generate insights
- Print findings to console
- Save all outputs to `processed_data/`

### Option 2: Pipeline Only

```bash
python main_pipeline.py
```

### Option 3: Dashboard Only (if data already processed)

```bash
streamlit run app.py
```

## Expected Output

After running the pipeline, you should see:

1. **Console Output**: Progress messages and insights
2. **processed_data/ folder** with:
   - `processed_data.csv` - Main dataset
   - `persistence_index.csv` - District persistence scores
   - `rank_volatility.csv` - Rank change analysis
   - `shock_detection.csv` - Detected shock months
   - `early_warnings.csv` - Early warning districts
   - `results.pkl` - Complete results (for dashboard)
   - `insights.json` - Structured insights (if using run_pipeline.py)

## Dashboard Features

Once you run `streamlit run app.py`, you can:

1. **Filter by**: State, District, Date Range, Metric
2. **View**: KPIs, Heatmaps, Trends, Scatter plots, Quadrants
3. **Analyze**: Top/Bottom stress districts, Early warnings
4. **Get Insights**: Present findings, Suggestions, Future risks

## Troubleshooting

### "Processed data not found"
- Run `python run_pipeline.py` first to generate data

### "No module named X"
- Install dependencies: `pip install -r requirements.txt`

### ZIP file errors
- Ensure ZIP files are in the project root directory
- Check that ZIP files are not corrupted

### Memory issues
- The system loads all CSVs in-memory
- For very large datasets, consider processing in batches (modify data_loader.py)

## Next Steps

1. Review `processed_data/insights.json` for structured insights
2. Explore the dashboard interactively
3. Export specific analyses from the dashboard
4. Use early warnings for policy prioritization
