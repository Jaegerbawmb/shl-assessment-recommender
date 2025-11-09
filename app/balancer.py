import pandas as pd
import numpy as np

def has_type(x, t):
    """Safely check whether a test type (e.g., 'K') exists in x."""
    if isinstance(x, (list, tuple, set)):
        return t in x
    if isinstance(x, str):
        return t in x
    if isinstance(x, np.ndarray):
        return t in x.tolist()
    return False

def balance_kp(query, df, k=5):
    """
    Balances Knowledge (K), Personality (P), and other test types in recommendations.
    Always returns a DataFrame (never None).
    """
    try:
        k_bucket = df[df['test_types'].apply(lambda t: has_type(t, 'K'))]
        p_bucket = df[df['test_types'].apply(lambda t: has_type(t, 'P'))]
        other = df[~df.index.isin(k_bucket.index.union(p_bucket.index))]

        frames = [k_bucket, p_bucket, other]
        out = pd.concat(frames).drop_duplicates(subset=['url']).head(k)
        return out.reset_index(drop=True)

    except Exception as e:
        print(f"[Balancer Warning] {e}")
        return df.head(k).reset_index(drop=True)
