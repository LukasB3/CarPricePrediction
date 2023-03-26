import streamlit as st
import pickle 
import numpy as np
import pandas as pd
from get_data import load_data

def load_model():
    with open('saved_model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

model = data["model"]
preprocessor=data["preprocessor"]

df = load_data()
car_make = df['make'].unique()
car_models = df['model'].unique()
car_fuels = df['fuel'].unique()

def predict_page():
    st.title("Gebrauchtwagen Preis Deutschland")

    st.write("""### Bitte geben Sie die Daten Ihres Wunschautos an:""")

    sorted_car_make = sorted(car_make)
    make = st.selectbox("Marke", sorted_car_make)
    available_models = sorted(df[df['make'] == make]['model'].unique())
    care_model = st.selectbox("Model", available_models)
    car_fuel = st.selectbox("Kraftstoff", car_fuels)
    mileage = st.slider("Kilometerstand", 0, 300000, 50000)
    year = st.slider("Baujahr", 2011, 2021, 2020)

    ok = st.button("Zeige Preis an")

    if ok: 
        input_data = np.array([mileage, make, care_model, car_fuel, year])
        input_df = pd.DataFrame([input_data], columns=['mileage', 'make', 'model', 'fuel', 'year'])
        
        input_processed = preprocessor.transform(input_df)
        
        predicted_price = model.predict(input_processed)
        rounded_predicted_price = round(predicted_price[0], 2)
        
        st.write(f'Der voraussichtliche Preis des Autos beträgt: **{rounded_predicted_price} €**')
