"""Test pipeline step by step."""
from data_loader import load_all_datasets
from data_preparation import aggregate_enrolment, aggregate_biometric, aggregate_demographic, apply_transformations
from feature_engineering import engineer_all_features
from composite_index import calculate_aisi
from advanced_analytics import stress_quadrant_classification

print("=" * 60)
print("STEP 1: Loading data from ZIP files...")
print("=" * 60)
e, b, d = load_all_datasets('.')
print(f"[OK] Enrolment: {len(e)} rows")
print(f"[OK] Biometric: {len(b)} rows")
print(f"[OK] Demographic: {len(d)} rows")

print("\n" + "=" * 60)
print("STEP 2: Aggregating data...")
print("=" * 60)
es, ed = aggregate_enrolment(e)
bs, bd = aggregate_biometric(b)
ds, dd = aggregate_demographic(d)
print(f"[OK] Enrolment district-month: {len(ed)} rows")
print(f"[OK] Biometric district-month: {len(bd)} rows")
print(f"[OK] Demographic district-month: {len(dd)} rows")

print("\n" + "=" * 60)
print("STEP 3: Engineering features...")
print("=" * 60)
df = engineer_all_features(ed, bd, dd)
print(f"[OK] Final dataset: {len(df)} rows")
print(f"[OK] Features created: ESS, MSP, YCR, DPI")
print(f"  ESS range: {df['ESS'].min():.3f} to {df['ESS'].max():.3f}")
print(f"  MSP range: {df['MSP'].min():.3f} to {df['MSP'].max():.3f}")
print(f"  YCR range: {df['YCR'].min():.3f} to {df['YCR'].max():.3f}")
print(f"  DPI range: {df['DPI'].min():.3f} to {df['DPI'].max():.3f}")

print("\n" + "=" * 60)
print("STEP 4: Applying transformations...")
print("=" * 60)
value_cols = ['ESS', 'MSP', 'YCR', 'DPI', 'total_enrolments', 'biometric_updates']
available_cols = [c for c in value_cols if c in df.columns]
print(f"[OK] Applying transformations to: {available_cols}")
df = apply_transformations(df, available_cols, pop_col='total_population')
print(f"[OK] Transformations applied")

print("\n" + "=" * 60)
print("STEP 5: Calculating AISI...")
print("=" * 60)
df, aisi_loadings = calculate_aisi(df)
print(f"[OK] AISI calculated")
print(f"  AISI range: {df['AISI'].min():.3f} to {df['AISI'].max():.3f}")
if aisi_loadings:
    print(f"  Explained variance: {aisi_loadings.get('explained_variance', 0):.1%}")

print("\n" + "=" * 60)
print("STEP 6: Stress quadrant classification...")
print("=" * 60)
df = stress_quadrant_classification(df)
print(f"[OK] Quadrants assigned")
print(f"  Quadrant distribution:")
print(df['stress_quadrant'].value_counts())

print("\n" + "=" * 60)
print("[OK] ALL STEPS COMPLETED SUCCESSFULLY!")
print("=" * 60)
print(f"\nFinal dataset shape: {df.shape}")
print(f"Columns: {len(df.columns)}")
