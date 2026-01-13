"""
AISI: Aadhaar Identity Stress Index using PCA.
Unsupervised composite index to avoid subjective weighting.
"""
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def calculate_aisi(df):
    """
    Build AISI using PCA on ESS, MSP, YCR, DPI.
    Returns normalized 0-1 index with feature loadings.
    """
    df = df.copy()
    
    # Required features
    features = ['ESS', 'MSP', 'YCR', 'DPI']
    available_features = [f for f in features if f in df.columns]
    
    if len(available_features) < 2:
        # Fallback: simple average if PCA not possible
        df['AISI'] = df[available_features].mean(axis=1) if available_features else 0
        return df, {}
    
    # Prepare data (drop NaN)
    feature_data = df[available_features].dropna()
    if len(feature_data) == 0:
        df['AISI'] = 0
        return df, {}
    
    # Standardize
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(feature_data)
    
    # PCA - use first component as it captures maximum variance
    pca = PCA(n_components=1)
    pca_scores = pca.fit_transform(scaled_data)
    
    # Normalize to 0-1
    pca_min = pca_scores.min()
    pca_max = pca_scores.max()
    if pca_max > pca_min:
        aisi_normalized = (pca_scores - pca_min) / (pca_max - pca_min)
    else:
        aisi_normalized = np.zeros_like(pca_scores)
    
    # Map back to original dataframe
    df.loc[feature_data.index, 'AISI'] = aisi_normalized.flatten()
    df['AISI'] = df['AISI'].fillna(0)
    
    # Feature loadings (contribution to first component)
    loadings = pd.DataFrame({
        'feature': available_features,
        'loading': pca.components_[0],
        'explained_variance': pca.explained_variance_ratio_[0]
    })
    
    loadings_dict = {
        'loadings': loadings.to_dict('records'),
        'explained_variance': float(pca.explained_variance_ratio_[0]),
        'interpretation': f"First PC explains {pca.explained_variance_ratio_[0]:.1%} of variance. "
                         f"Features with higher absolute loadings contribute more to stress."
    }
    
    return df, loadings_dict
