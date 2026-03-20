import pandas as pd
import os

parquet_path = r'F:\PyTorch_GPU\AIS_trajectory_forecasting\Data\region_1_q1_merged_renamed.parquet'
df = pd.read_parquet(parquet_path)
print("Columns:", list(df.columns))
print("Shape:", df.shape)
print("Dtypes:\n", df.dtypes)
print("Sample:\n", df.head(3).to_string())
print("Nulls:\n", df.isnull().sum())
