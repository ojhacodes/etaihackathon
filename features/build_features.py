import pandas as pd
import numpy as np

def build_features(df, horizon_hours=24):
    """
    Build features for the forecasting model (LightGBM).
    Returns X and y (target AQI/PM2.5 at t+horizon_hours).
    """
    df = df.copy()
    df.sort_index(inplace=True)
    
    # Lag features
    df['lag_1h'] = df['pollutant_avg'].shift(1)
    df['lag_3h'] = df['pollutant_avg'].shift(3)
    df['lag_6h'] = df['pollutant_avg'].shift(6)
    df['lag_24h'] = df['pollutant_avg'].shift(24)
    df['lag_48h'] = df['pollutant_avg'].shift(48)
    
    # Rolling stats
    df['rolling_mean_6h'] = df['pollutant_avg'].rolling(window=6).mean()
    df['rolling_std_6h'] = df['pollutant_avg'].rolling(window=6).std()
    df['rolling_mean_24h'] = df['pollutant_avg'].rolling(window=24).mean()
    df['rolling_mean_72h'] = df['pollutant_avg'].rolling(window=72).mean()
    
    # Target
    df['target'] = df['pollutant_avg'].shift(-horizon_hours)
    
    # Drop NaNs created by shifting
    df.dropna(inplace=True)
    
    # Calendar features (assuming index is datetime)
    df['hour_of_day'] = df.index.hour
    df['day_of_week'] = df.index.dayofweek
    df['month'] = df.index.month
    
    # Meteorlogical features (mocking if absent)
    if 'wind_speed' not in df.columns:
        df['wind_speed'] = np.random.uniform(0, 10, len(df))
    if 'humidity' not in df.columns:
        df['humidity'] = np.random.uniform(30, 90, len(df))
    if 'temperature' not in df.columns:
        df['temperature'] = np.random.uniform(10, 40, len(df))
        
    X = df[['lag_1h', 'lag_3h', 'lag_6h', 'lag_24h', 'lag_48h', 
            'rolling_mean_6h', 'rolling_std_6h', 'rolling_mean_24h', 'rolling_mean_72h',
            'hour_of_day', 'day_of_week', 'month', 'wind_speed', 'humidity', 'temperature']]
    y = df['target']
    
    return X, y
