import numpy as np

# In a real scenario, this would use SHAP
# import shap

def get_modulating_factors(model, X_query):
    """
    Compute modulating factors (meteorological, temporal, seasonal) for a forecast.
    Does NOT return pollution sources.
    """
    # Mocking SHAP values
    feature_names = X_query.columns.tolist() if hasattr(X_query, 'columns') else [f"f{i}" for i in range(len(X_query))]
    shap_values = np.random.uniform(-10, 10, len(feature_names))
    
    modulating_bucket_map = {
        "hour_of_day": "temporal pattern",
        "day_of_week": "temporal pattern",
        "wind_speed": "meteorological",
        "humidity": "meteorological",
        "temperature": "meteorological",
        "lag_1h": "persistence/trend",
        "lag_24h": "persistence/trend",
        "rolling_mean_24h": "persistence/trend",
        "is_burning_season": "seasonal/calendar",
        "month": "seasonal/calendar"
    }
    
    factors = {
        "meteorological": 0.0,
        "temporal pattern": 0.0,
        "persistence/trend": 0.0,
        "seasonal/calendar": 0.0
    }
    
    for fname, val in zip(feature_names, shap_values):
        bucket = modulating_bucket_map.get(fname, "other")
        if bucket in factors:
            factors[bucket] += abs(val)  # aggregate magnitude of effect
            
    # Normalize for UI rendering
    total = sum(factors.values()) + 1e-6
    return {k: round(v/total, 2) for k, v in factors.items()}
