import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_fake_engagement():
    df = pd.read_csv('datasets/engagement.csv')
    
    # Feature engineering: Ratio of likes to views
    df['like_view_ratio'] = df['likes'] / df['views']
    
    model = IsolationForest(contamination=0.2, random_state=42)
    # Fit model to find anomalies (-1 means fake/anomaly, 1 means normal)
    df['is_fake'] = model.fit_predict(df[['views', 'like_view_ratio']])
    
    # Return videos flagged as bots
    fake_videos = df[df['is_fake'] == -1]['video_id'].tolist()
    return fake_videos