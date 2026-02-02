import pandas as pd
from sklearn.preprocessing import LabelEncoder

def clean_data(df):
    df = df.copy()

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna(df[col].mode()[0])
            df[col] = LabelEncoder().fit_transform(df[col])
        else:
            df[col] = df[col].fillna(df[col].mean())

    return df
