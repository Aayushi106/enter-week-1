# import all necesary libraries
import pandas as pd  # data manipulation 
import numpy as np
import joblib
import pickle
import streamlit as st

# load the model and structure
model = joblib.load("Pollution_model.pkl")
model_cols = joblib.load("model_columns.pkl")

# lets create an user interface
st.title("Water pollution predictor")
st.write("Predict the water pollutants based on year and station ID")

# user inputs
year_input = st.number_input("Enter year", min_value= 2000, max_value=2100, value=2022)
station_id = st.text_input("Enter station ID", value='1')

# To encode and then predict
if st.button('Predict'):
    if not station_id:
        st.warning('Please enter the station ID')
    else:
        #Prepare the input
        input_df = pd.DataFrame({'year': [year_input], 'id':[station_id]})
        input_encoded = pd.get_dummies(input_df, columns=['id'])

        #Align with model cols
        for col in model_cols:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[model_cols]

        #predict
        predicted_pollutants = model.predict(input_encoded)[0]
        pollutants = ['O2','NO3', 'NO2', 'SO4', 'PO4', 'CL']

        st.subheader(f"Predicted pllutant levels for the station '{station_id}' in {year_input}:")
        predicted_values = {}
        for p, val in zip(pollutants, predicted_pollutants):
            st.write(f'{p}:{val:.2f}')