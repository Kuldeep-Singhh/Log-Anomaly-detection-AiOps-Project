import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import warnings

# Suppress sklearn warnings about feature names
warnings.filterwarnings("ignore", category=UserWarning)

class AnomalyDetector:
    def __init__(self, text_col='message', latency_col='latency', status_col='status'):
        self.text_col = text_col
        self.latency_col = latency_col
        self.status_col = status_col
        
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
        
    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['anomaly_text'] = False
        df['anomaly_stat'] = False
        df['anomaly_reason'] = ""

        # 1. Text Clustering (TF-IDF + KMeans)
        if self.text_col in df.columns and df[self.text_col].notna().any():
            valid_texts = df[df[self.text_col].notna()][self.text_col]
            if len(valid_texts) > 2: # need enough samples for 2 clusters
                try:
                    X = self.vectorizer.fit_transform(valid_texts)
                    clusters = self.kmeans.fit_predict(X)
                    
                    # Assume the smaller cluster is the anomaly cluster
                    counts = np.bincount(clusters)
                    
                    if len(counts) == 2:
                        anomaly_cluster_id = np.argmin(counts)
                        
                        # Map back to DataFrame
                        df.loc[valid_texts.index, 'cluster'] = clusters
                        df.loc[df['cluster'] == anomaly_cluster_id, 'anomaly_text'] = True
                        
                        # Add reason (use map/apply to append correctly without warnings)
                        df.loc[df['anomaly_text'], 'anomaly_reason'] += "Text Anomaly (Unusual Pattern). "
                except Exception as e:
                    pass # Handled gracefully if clustering fails
                    
        # 2. Statistical Analysis (3-Sigma on Latency)
        if self.latency_col in df.columns:
            latencies = df[self.latency_col].dropna()
            if len(latencies) > 0:
                mean = latencies.mean()
                std = latencies.std()
                if not pd.isna(std) and std > 0:
                    threshold = mean + 3 * std
                    df.loc[df[self.latency_col] > threshold, 'anomaly_stat'] = True
                    df.loc[df[self.latency_col] > threshold, 'anomaly_reason'] += f"High Latency (> {threshold:.2f}ms). "
        
        # 3. Simple Status Code Rule (e.g., 5xx errors are anomalies)
        if self.status_col in df.columns:
            df.loc[df[self.status_col] >= 500, 'anomaly_stat'] = True
            df.loc[df[self.status_col] >= 500, 'anomaly_reason'] += "Server Error (5xx). "

        df['is_anomaly'] = df['anomaly_text'] | df['anomaly_stat']
        return df
