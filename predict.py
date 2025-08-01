import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the saved model
def load_model():
    with open('saved_model.pkl','rb') as file:
        data = pickle.load(file)
    return data

# Load the saved model
def load_preprocessor():
    with open('preprocessor.pkl','rb') as file:
        data = pickle.load(file)
    return data
    
model = load_model()
preprocessor = load_preprocessor()

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
        'car brand': [brand],
        'weight groups': [weight],
        'displacement': [displacement],
        'horsepower': [horsepower],
        'cylinders': [cylinders],
        'acceleration': [acceleration],
        'model year': [year],
        'origin':[origin],
        }

        input_df = pd.DataFrame(input_data)
        transformed_input = preprocessor.transform(input_df)
        predictions = model.predict(transformed_input)
        st.success(f"Your estimated car's mileage is: {round(predictions[0],2)} miles")
        
       
def show_predict_page():
    st.title("Automotive fuel consumption prediction!")
    st.header("We need some infomartion here!", divider='violet')
    prediction()

