import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests

API_URL = "http://localhost:8000/predict"
API_URL_BATCH = "http://localhost:8000/predict-batch"

def prediction():
    # Feed the input

    # mpg
    origin = st.slider('Origin', 1,3,1)
    st.write(f"Your selected origin value is: {origin}")

    #acceleration
    acceleration = st.slider('Acceleration of car', 6.0,30.0,2.0)
    st.write(f"Your selected acceleration value is: {acceleration}")

    # horsepower
    horsepower = st.slider('Horsepower of car', 40.0,240.0,2.0)
    st.write(f"Your selected horsepower value is: {horsepower}")

    # model year
    # model_year = st.number_input('Model Year', min_value=1, max_value=3, step=1)
    # st.write(f"Your selected model year value is: {model_year}")

    # displacement 
    displacement = st.slider("Displacement of car", 60.0,460.0,2.0)
    st.write(f"Your selected displacement value is: {displacement}")

    # car brand
    brand = st.selectbox("Select your car brand", 
                        ['amc', 'audi', 'buick', 'chevrolet', 'chrysler', 'datsun', 'dodge','fiat','ford',
                        'honda', 'mazda', 'mercury', 'oldsmobile', 'peugeot', 'plymouth','pontiac', 
                        'toyota', 'volkswagen', 'volvo'])
    st.write(f"Your selected car brand is: {brand}")

    # car name
    # name = st.selectbox("Select your car", 
    #                 ['ford pinto','other','ford maverick','amc matador','toyota corolla','amc hornet',
    #                     'chevrolet impala','toyota corona','amc gremlin','peugeot 504','chevrolet chevette'])
    # st.write(f"Your selected car is: {name}")

    # weight
    weight = st.selectbox("Select your car weight group", 
                        ['1500 - 2000','2000 - 2500','2500 - 3000','3000 - 3500',
                        '3500 - 4000','4000 - 4500','up-to 5000'])
    st.write(f"Your selected car weight group is: {weight}")

    # cylinders
    cylinders = st.selectbox("Select number of cylinders", [3,4,5,6,7,8])
    st.write(f"Your selected number of cylinder engine is: {cylinders}")

    # model year
    year = st.selectbox("Select your car's model year", [70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82])
    st.write(f"Your selected car model year is: {year}")

    predict = st.button("Estimate",type='secondary')
    if predict:
        input_data = {
        # 'car name': [name],
        'brand': brand,
        'weight': weight,
        'displacement': float(displacement),
        'horsepower': float(horsepower),
        'cylinders': int(cylinders),
        'acceleration': float(acceleration),
        'year': int(year),
        'origin':int(origin),
        }
        
        response = requests.post(API_URL, json=input_data)

        if response.status_code == 200:

            prediction = response.json()["prediction"]

            st.success(f"{prediction}")

        else:
            print(response.status_code)
            print(response.text)
            st.error("Prediction failed")
        
        
       
def show_predict_page():
    st.title("Automotive fuel consumption prediction!")
    st.header("We need some infomartion here!", divider='violet')
    prediction()

