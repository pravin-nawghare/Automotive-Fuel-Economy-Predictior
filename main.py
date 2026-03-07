from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, Literal
import pickle
import requests
import json
import pandas as pd
import numpy as np


app = FastAPI()

# Column mapping (API → Model expected columns)
COLUMN_MAPPING = {
    "brand": "car brand",
    "weight": "weight groups",
    "year": "model year"
}

class LoadFiles:

    # Load the saved model
    @staticmethod
    def load_model():
        with open('saved_model.pkl','rb') as file:
            data = pickle.load(file)
        return data

    # Load the saved preprocessor model
    @staticmethod
    def load_preprocessor():
        with open('preprocessor.pkl','rb') as file:
            data = pickle.load(file)
        return data

model = LoadFiles.load_model()
preprocessor = LoadFiles.load_preprocessor()

class InputData(BaseModel):
    brand: Annotated[str, Field(...,description='Enter the brand name of car')]
    weight: Annotated[str, Field(..., description='Enter the range of weight of the car')]
    displacement: Annotated[float, Field(..., description='Displacement of the engine', lt=461, gt=59)]
    horsepower: Annotated[float, Field(..., description='Horsepower of engine',gt=39,lt=241)]
    cylinders: Annotated[int, Field(..., description='Number of cylinders in the car', gt=2,lt=9)]
    acceleration: Annotated[float, Field(..., description='Amount of acceleration car produces',gt=5,lt=7)]
    year: Annotated[int, Field(..., description='What is the manufacturing year of the car')]
    origin: Annotated[int, Field(..., description='Which of the car is')]

@app.get('/')
def home():
    return {'message':'This is the home page'}

@app.post('/predict')
def predict(data:InputData):
    test_data = data.model_dump() # converted into python dict
    # convert to dataframe
    
    final_input = pd.DataFrame([test_data])
    # Rename columns
    final_input.rename(columns=COLUMN_MAPPING, inplace=True)
    try:
        transformed_input = preprocessor.transform(final_input)
        predictions = model.predict(transformed_input)
        return {'status':'success',
                'prediction':f"Your estimated car's mileage is: {round(predictions.tolist()[0],2)} miles"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/predict-batch")
def predict_batch(data: list[InputData]):

    try:
        input_data = [item.model_dump() for item in data]

        df = pd.DataFrame(input_data)

        df.rename(columns=COLUMN_MAPPING, inplace=True)

        transformed = preprocessor.transform(df)
        predictions = model.predict(transformed)

        return { 'status':'success',
            "predictions": f"Your estimated car's mileage is: {predictions.tolist()[0]} miles"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

