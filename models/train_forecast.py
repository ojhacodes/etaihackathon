import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import root_mean_squared_error
from pathlib import Path

# In a real project, we'd import build_features
# from features.build_features import build_features

def persistence_baseline_rmse(df, horizon_hours):
    """Calculate RMSE for persistence baseline (forecast = current value)."""
    # Assuming the data is already aligned such that target is t+horizon
    # and current value is at time t.
    if 'target' not in df.columns or 'pollutant_avg' not in df.columns:
        return np.nan
        
    y_true = df['target']
    y_pred = df['pollutant_avg']
    return root_mean_squared_error(y_true, y_pred)

def train_horizon_model(X, y, horizon_hours):
    """
    Train a LightGBM model for a specific horizon.
    Returns the trained model and validation RMSE.
    """
    # Simple time-based split (80/20)
    split_idx = int(len(X) * 0.8)
    X_train, X_val = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_val = y.iloc[:split_idx], y.iloc[split_idx:]
    
    model = lgb.LGBMRegressor(n_estimators=500, learning_rate=0.03, random_state=42)
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], callbacks=[lgb.early_stopping(50, verbose=False)])
    
    preds = model.predict(X_val)
    rmse = root_mean_squared_error(y_val, preds)
    
    return model, rmse

if __name__ == "__main__":
    print("Training models...")
    # Mock data for demonstration
    dates = pd.date_range("2024-01-01", periods=1000, freq="H")
    mock_df = pd.DataFrame({
        "pollutant_avg": np.random.uniform(50, 400, 1000)
    }, index=dates)
    
    # Simple features for mock
    mock_df['target'] = mock_df['pollutant_avg'].shift(-24)
    mock_df['lag_1h'] = mock_df['pollutant_avg'].shift(1)
    mock_df.dropna(inplace=True)
    
    X = mock_df[['pollutant_avg', 'lag_1h']]
    y = mock_df['target']
    
    baseline_rmse = persistence_baseline_rmse(mock_df, 24)
    model, model_rmse = train_horizon_model(X, y, 24)
    
    improvement_pct = (baseline_rmse - model_rmse) / baseline_rmse * 100
    
    print(f"24h Horizon Validation:")
    print(f"  Persistence RMSE: {baseline_rmse:.2f}")
    print(f"  Model RMSE:       {model_rmse:.2f}")
    print(f"  Improvement:      {improvement_pct:.1f}%")
