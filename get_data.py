import pandas as pd
import streamlit as st

def drop_make(df, column='make', threshold=25, drop_value=['Porsche', 'Aston']):
    df_filtered = df.groupby(column).filter(lambda x: len(x) >= threshold)
    df_filtered = df_filtered[~df_filtered[column].isin(drop_value)]
    return df_filtered

def drop_model(df, column='model', threshold=5):
    df_filtered = df.groupby(column).filter(lambda x: len(x) >= threshold)
    return df_filtered

@st.cache_data
def load_data():
    df = pd.read_csv("data/autoscout24-germany-dataset.csv")
    df = df.dropna() 
    df = drop_make(df)
    df = drop_model(df)
    df = df[df['mileage'] <= 300000]
    df = df[df['price'] <= 100000]
    df = df[df['fuel'].isin(['Gasoline', 'Diesel'])]
    df = df[df['gear'].isin(['Manual', 'Automatic'])]
    df = df.drop('offerType', axis=1)
    df = df.drop('hp', axis=1)
    df = df.drop('gear', axis=1)
    return df