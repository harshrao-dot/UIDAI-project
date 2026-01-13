"""
Load ZIP files and extract CSVs in-memory.
Treats ZIPs as authoritative data sources.
"""
import zipfile
import pandas as pd
import io
from pathlib import Path


def load_zip_data(zip_path):
    """Extract all CSVs from ZIP and concatenate in-memory."""
    dfs = []
    with zipfile.ZipFile(zip_path, 'r') as z:
        csv_files = [f for f in z.namelist() if f.endswith('.csv')]
        for csv_file in csv_files:
            with z.open(csv_file) as f:
                df = pd.read_csv(f)
                dfs.append(df)
    
    if not dfs:
        return pd.DataFrame()
    
    combined = pd.concat(dfs, ignore_index=True)
    return combined


def load_all_datasets(base_path='.'):
    """Load all three datasets from ZIP files."""
    enrolment = load_zip_data(Path(base_path) / 'api_data_aadhar_enrolment.zip')
    biometric = load_zip_data(Path(base_path) / 'api_data_aadhar_biometric.zip')
    demographic = load_zip_data(Path(base_path) / 'api_data_aadhar_demographic.zip')
    
    return enrolment, biometric, demographic
